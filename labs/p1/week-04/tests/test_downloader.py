"""Acceptance tests for LAB-P1-W04 — the async concurrent downloader.

Every test runs against `tests/flaky_server.py`, a local asyncio HTTP server with a
deterministic failure policy. No network, no flakes that are not on purpose.
"""
from __future__ import annotations

import asyncio
import hashlib
import time
import tracemalloc
from pathlib import Path

import pytest

from downloader import DownloadSpec, Downloader, TokenBucket, download_all

from .flaky_server import FlakyServer


def _run(coro):  # noqa: ANN001, ANN202
    return asyncio.run(coro)


def body(n: int, seed: int = 0) -> bytes:
    return bytes((i * 7 + seed) % 251 for i in range(n))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ============================================================== basic
@pytest.mark.basic
def test_download_all_fetches_every_url(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            payloads = [body(1000 + i, i) for i in range(5)]
            for i, p in enumerate(payloads):
                srv.add(f"f{i}", p)
            urls = [srv.url(f"f{i}") for i in range(5)]
            paths = await download_all(urls, tmp_path)
            assert len(paths) == 5
            for p, expected in zip(paths, payloads, strict=True):
                assert p.read_bytes() == expected

    _run(main())


@pytest.mark.basic
def test_download_all_preserves_input_order(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            for i in range(4):
                srv.add(f"f{i}", body(200 + i * 500, i))
            urls = [srv.url(f"f{i}") for i in range(4)]
            paths = await download_all(urls, tmp_path)
            sizes = [p.stat().st_size for p in paths]
            assert sizes == [200, 700, 1200, 1700]

    _run(main())


# ============================================================== standard
@pytest.mark.standard
def test_concurrency_is_bounded(tmp_path: Path) -> None:
    """The server counts concurrent connections. The bound is not advisory."""

    async def main() -> None:
        async with FlakyServer() as srv:
            for i in range(40):
                srv.add(f"f{i}", body(50_000, i), stall_seconds=0.02)
            dl = Downloader(concurrency=4, log=lambda r: None)
            specs = [DownloadSpec(srv.url(f"f{i}"), tmp_path / f"f{i}") for i in range(40)]
            results = await dl.run(specs)
            assert all(r.ok for r in results), [r.error for r in results if not r.ok]
            assert srv.max_concurrent <= 4, f"server saw {srv.max_concurrent} concurrent sockets"
            assert dl.peak_in_flight <= 4

    _run(main())


@pytest.mark.standard
def test_retries_5xx_with_backoff_then_succeeds(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            payload = body(4096)
            srv.add("flaky", payload, fail_first=3)
            logs: list[dict[str, object]] = []
            dl = Downloader(max_retries=5, backoff_base=0.001, log=logs.append)
            result = await dl.fetch(DownloadSpec(srv.url("flaky"), tmp_path / "flaky"))
            assert result.ok
            assert result.attempts == 4
            assert (tmp_path / "flaky").read_bytes() == payload
            assert sum(1 for r in logs if r["event"] == "attempt_failed") == 3

    _run(main())


@pytest.mark.standard
def test_retries_429(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("throttled", body(512), fail_first=2, status_when_failing=429)
            dl = Downloader(max_retries=4, backoff_base=0.001, log=lambda r: None)
            assert (await dl.fetch(DownloadSpec(srv.url("throttled"), tmp_path / "t"))).ok

    _run(main())


@pytest.mark.standard
def test_404_is_not_retried(tmp_path: Path) -> None:
    """Retrying a permanent failure four times is four times the load for one answer."""

    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("gone", b"", status=404)
            dl = Downloader(max_retries=5, backoff_base=0.001, log=lambda r: None)
            result = await dl.fetch(DownloadSpec(srv.url("gone"), tmp_path / "gone"))
            assert not result.ok
            assert len(srv.requests_for("gone")) == 1, "a 404 must be attempted exactly once"

    _run(main())


@pytest.mark.standard
def test_truncated_body_is_detected_and_retried(tmp_path: Path) -> None:
    """The server advertises the full Content-Length and sends half of it. This is the
    silent-corruption case the ticket describes: status 200, wrong file."""

    async def main() -> None:
        async with FlakyServer() as srv:
            payload = body(20_000, 3)
            srv.add("half", payload, truncate_at=9_000)
            dl = Downloader(max_retries=3, backoff_base=0.001, log=lambda r: None)
            result = await dl.fetch(DownloadSpec(srv.url("half"), tmp_path / "half"))
            assert result.ok
            assert (tmp_path / "half").read_bytes() == payload

    _run(main())


@pytest.mark.standard
def test_checksum_mismatch_fails_and_leaves_no_file(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("f", body(2048))
            dl = Downloader(max_retries=2, backoff_base=0.001, log=lambda r: None)
            spec = DownloadSpec(srv.url("f"), tmp_path / "f", sha256=sha(b"something else"))
            result = await dl.fetch(spec)
            assert not result.ok
            assert not (tmp_path / "f").exists()
            assert not (tmp_path / "f.part").exists(), "a corrupt partial must not survive"

    _run(main())


@pytest.mark.standard
def test_checksum_match_passes(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            payload = body(3000, 9)
            srv.add("f", payload)
            dl = Downloader(log=lambda r: None)
            r = await dl.fetch(DownloadSpec(srv.url("f"), tmp_path / "f", sha256=sha(payload)))
            assert r.ok and (tmp_path / "f").read_bytes() == payload

    _run(main())


@pytest.mark.standard
def test_resumes_from_a_partial_file_with_range(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            payload = body(30_000, 5)
            srv.add("big", payload)
            # Pretend a previous run died after 12,000 bytes.
            (tmp_path / "big.part").write_bytes(payload[:12_000])

            dl = Downloader(log=lambda r: None)
            result = await dl.fetch(DownloadSpec(srv.url("big"), tmp_path / "big"))
            assert result.ok
            assert result.resumed_from == 12_000
            assert (tmp_path / "big").read_bytes() == payload

            reqs = srv.requests_for("big")
            assert reqs[-1].range_header == "bytes=12000-", "must send a Range header"
            assert reqs[-1].status == 206

    _run(main())


@pytest.mark.standard
def test_completed_file_is_skipped_with_no_network_call(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("done", body(100))
            (tmp_path / "done").write_bytes(body(100))
            dl = Downloader(log=lambda r: None)
            result = await dl.fetch(DownloadSpec(srv.url("done"), tmp_path / "done"))
            assert result.ok and result.skipped
            assert srv.requests_for("done") == [], "a completed file must cost zero requests"

    _run(main())


@pytest.mark.standard
def test_cancellation_is_graceful(tmp_path: Path) -> None:
    """Ctrl-C must cancel in flight, await the cleanup, and leave no complete-looking
    file that is actually partial."""

    async def main() -> None:
        async with FlakyServer() as srv:
            for i in range(30):
                srv.add(f"f{i}", body(80_000, i), stall_seconds=0.15)
            dl = Downloader(concurrency=3, timeout=5.0, log=lambda r: None)
            specs = [DownloadSpec(srv.url(f"f{i}"), tmp_path / f"f{i}") for i in range(30)]
            task = asyncio.create_task(dl.run(specs))
            await asyncio.sleep(0.2)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

            # Every file that exists without a .part sibling must be complete.
            for f in tmp_path.glob("f*"):
                if f.suffix == ".part":
                    continue
                assert f.stat().st_size == 80_000, f"{f.name} is a partial file in a final name"

    _run(main())


@pytest.mark.standard
def test_structured_logs_are_json_shaped(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("f", body(1000), fail_first=1)
            logs: list[dict[str, object]] = []
            dl = Downloader(max_retries=3, backoff_base=0.001, log=logs.append)
            await dl.fetch(DownloadSpec(srv.url("f"), tmp_path / "f"))
            ok = [r for r in logs if r["event"] == "downloaded"]
            assert ok, "a successful download must be logged"
            record = ok[0]
            for key in ("url", "attempt", "status", "bytes", "duration_ms"):
                assert key in record, f"log record is missing {key!r}"
            import json
            json.dumps(record)  # must be serialisable

    _run(main())


@pytest.mark.standard
def test_one_failure_does_not_lose_the_others(tmp_path: Path) -> None:
    async def main() -> None:
        async with FlakyServer() as srv:
            for i in range(6):
                srv.add(f"f{i}", body(500, i))
            srv.add("bad", b"", status=404)
            dl = Downloader(max_retries=2, backoff_base=0.001, log=lambda r: None)
            specs = [DownloadSpec(srv.url(f"f{i}"), tmp_path / f"f{i}") for i in range(6)]
            specs.append(DownloadSpec(srv.url("bad"), tmp_path / "bad"))
            results = await dl.run(specs)
            assert len(results) == 7
            assert sum(1 for r in results if r.ok) == 6
            assert sum(1 for r in results if not r.ok) == 1

    _run(main())


# ============================================================== hard
@pytest.mark.hard
def test_token_bucket_rate() -> None:
    """The limiter on its own, before it is anywhere near a socket."""

    async def main() -> None:
        bucket = TokenBucket.per_minute(600, burst=1)  # 10/s, no burst
        began = time.monotonic()
        for _ in range(11):
            await bucket.take()
        elapsed = time.monotonic() - began
        # 1 free token + 10 at 10/s = at least 1.0 s, and not absurdly more.
        assert 0.9 <= elapsed <= 2.5, f"11 takes at 10/s took {elapsed:.2f}s"

    _run(main())


@pytest.mark.hard
def test_rate_limit_is_respected_end_to_end(tmp_path: Path) -> None:
    """Measured from the SERVER's request log, which is the only honest place to
    measure it. A semaphore alone passes the concurrency test and fails this one."""

    async def main() -> None:
        async with FlakyServer() as srv:
            n = 30
            for i in range(n):
                srv.add(f"f{i}", body(200, i))
            dl = Downloader(concurrency=10, rate_limit_per_minute=900, burst=2,
                            log=lambda r: None)  # 15 req/s
            specs = [DownloadSpec(srv.url(f"f{i}"), tmp_path / f"f{i}") for i in range(n)]
            began = time.monotonic()
            results = await dl.run(specs)
            elapsed = time.monotonic() - began
            assert all(r.ok for r in results)
            # 30 requests at 15/s with a burst of 2 cannot finish faster than ~1.87 s.
            assert elapsed >= 1.6, f"finished in {elapsed:.2f}s — the rate limit was not applied"
            observed = srv.peak_rate_per_minute(window=1.0)
            assert observed <= 900 * 2.5, f"peak observed rate {observed:.0f}/min"

    _run(main())


@pytest.mark.hard
def test_body_is_streamed_not_materialised(tmp_path: Path) -> None:
    """Serve 8 MB and assert peak Python allocation stays far below it. This fails
    immediately for any implementation that does `body = await response.read()`."""

    async def main() -> None:
        async with FlakyServer() as srv:
            payload = body(8 * 1024 * 1024, 11)
            srv.add("big", payload)
            dl = Downloader(chunk_size=64 * 1024, log=lambda r: None)
            tracemalloc.start()
            tracemalloc.reset_peak()
            result = await dl.fetch(DownloadSpec(srv.url("big"), tmp_path / "big"))
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            assert result.ok
            assert (tmp_path / "big").stat().st_size == len(payload)
            assert peak < 2 * 1024 * 1024, (
                f"peak allocation was {peak / 1e6:.1f} MB for an 8 MB file — "
                f"the body is being materialised instead of streamed"
            )

    _run(main())


@pytest.mark.hard
def test_many_specs_do_not_allocate_a_task_each(tmp_path: Path) -> None:
    """2,000 specs through a pool of 8. `asyncio.gather(*[...])` over the whole list
    creates 2,000 Task objects before a byte moves; the memory ceiling is what makes
    that a bug rather than a style preference."""

    async def main() -> None:
        async with FlakyServer() as srv:
            srv.add("tiny", body(64))
            dl = Downloader(concurrency=8, log=lambda r: None)
            specs = (DownloadSpec(srv.url("tiny"), tmp_path / f"t{i}") for i in range(2000))

            peak_tasks = 0

            async def watch() -> None:
                nonlocal peak_tasks
                while True:
                    peak_tasks = max(peak_tasks, len(asyncio.all_tasks()))
                    await asyncio.sleep(0.005)

            watcher = asyncio.create_task(watch())
            results = await dl.run(specs)
            watcher.cancel()
            assert len(results) == 2000
            assert all(r.ok for r in results)
            assert peak_tasks < 100, (
                f"{peak_tasks} live tasks for 2,000 specs — the work is being "
                f"materialised up front"
            )

    _run(main())


@pytest.mark.hard
def test_no_file_is_written_twice(tmp_path: Path) -> None:
    """Re-running the whole job must cost zero writes for anything already complete."""

    async def main() -> None:
        async with FlakyServer() as srv:
            payloads = {f"f{i}": body(4000, i) for i in range(20)}
            for name, p in payloads.items():
                srv.add(name, p)
            specs = [
                DownloadSpec(srv.url(n), tmp_path / n, sha256=sha(p))
                for n, p in payloads.items()
            ]
            dl = Downloader(concurrency=6, log=lambda r: None)

            first = await dl.run(specs)
            assert all(r.ok for r in first)
            requests_after_first = len(srv.requests)

            second = await dl.run(specs)
            assert all(r.ok and r.skipped for r in second)
            assert len(srv.requests) == requests_after_first, (
                "the second run made network requests for files that were already complete"
            )
            for name, p in payloads.items():
                assert (tmp_path / name).read_bytes() == p

    _run(main())
