"""Reference implementation for LAB-P1-W04 — the async concurrent downloader.

Stdlib only: `asyncio.open_connection` and a small HTTP/1.1 GET. No aiohttp, no httpx.
That is not asceticism — it is so that every failure mode in this file is one you can
see, rather than one buried in a library's retry policy.

Three things this file is built around:

1. **A semaphore bounds concurrency, not rate.** Eight concurrent requests that each
   take 10 ms is 800 req/s, which blows a 500-req/min budget by 96x. You need both a
   semaphore and a token bucket, and they do different jobs.

2. **Nothing is materialised.** Specs are consumed from an iterator and bodies are
   streamed to disk in `chunk_size` pieces. `await response.read()` on a 2 GB file is
   how a downloader with a 300 MB ceiling dies.

3. **A partial file is never left where a complete one belongs.** Writes go to
   `<dest>.part` and are renamed into place only after the length and checksum agree.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
import sys
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

__all__ = [
    "DownloadError",
    "DownloadSpec",
    "Downloader",
    "HttpError",
    "Result",
    "TokenBucket",
    "download_all",
]


class DownloadError(Exception):
    """Any failure that is ours rather than the network's."""


class HttpError(DownloadError):
    def __init__(self, status: int, url: str) -> None:
        super().__init__(f"HTTP {status} for {url}")
        self.status = status
        self.url = url

    @property
    def retryable(self) -> bool:
        # 5xx and 429 are worth another go. 404 never is: retrying a 404 four times
        # is four times the load for the same answer.
        return self.status >= 500 or self.status == 429


class ChecksumMismatch(DownloadError):
    pass


class TruncatedResponse(DownloadError):
    pass


@dataclass(slots=True)
class DownloadSpec:
    url: str
    dest: Path
    sha256: str | None = None


@dataclass(slots=True)
class Result:
    url: str
    dest: Path
    ok: bool
    bytes: int = 0
    attempts: int = 0
    resumed_from: int = 0
    skipped: bool = False
    error: str | None = None


# --------------------------------------------------------------------------- rate
class TokenBucket:
    """Classic token bucket. `rate` tokens per second, burst up to `capacity`.

    Async-safe: a single lock serialises the refill-and-take, so N coroutines cannot
    each observe the same token.
    """

    def __init__(self, rate_per_second: float, capacity: float | None = None) -> None:
        if rate_per_second <= 0:
            raise ValueError("rate must be positive")
        self.rate = rate_per_second
        self.capacity = capacity if capacity is not None else max(1.0, rate_per_second)
        self._tokens = self.capacity
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    @classmethod
    def per_minute(cls, requests_per_minute: float, burst: float | None = None) -> "TokenBucket":
        return cls(requests_per_minute / 60.0, burst)

    async def take(self, n: float = 1.0) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                self._tokens = min(self.capacity, self._tokens + (now - self._updated) * self.rate)
                self._updated = now
                if self._tokens >= n:
                    self._tokens -= n
                    return
                deficit = n - self._tokens
                wait = deficit / self.rate
            await asyncio.sleep(wait)


# --------------------------------------------------------------------------- http
@dataclass(slots=True)
class _Response:
    status: int
    headers: dict[str, str]
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    @property
    def content_length(self) -> int | None:
        raw = self.headers.get("content-length")
        return int(raw) if raw is not None else None


async def _open(url: str, start_byte: int, timeout: float) -> _Response:
    parts = urlsplit(url)
    if parts.scheme != "http":
        raise DownloadError(f"only http:// is supported by this client, got {parts.scheme!r}")
    host = parts.hostname or "localhost"
    port = parts.port or 80
    target = parts.path or "/"
    if parts.query:
        target += "?" + parts.query

    reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
    lines = [f"GET {target} HTTP/1.1", f"Host: {host}:{port}",
             "User-Agent: nexus-downloader/1.0", "Accept-Encoding: identity",
             "Connection: close"]
    if start_byte:
        lines.append(f"Range: bytes={start_byte}-")
    writer.write(("\r\n".join(lines) + "\r\n\r\n").encode("latin-1"))
    await writer.drain()

    head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout)
    text = head.decode("latin-1").split("\r\n")
    status = int(text[0].split(" ", 2)[1])
    headers = {}
    for line in text[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return _Response(status, headers, reader, writer)


# ---------------------------------------------------------------------- downloader
class Downloader:
    def __init__(
        self,
        *,
        concurrency: int = 8,
        max_retries: int = 4,
        backoff_base: float = 0.05,
        backoff_cap: float = 5.0,
        timeout: float = 10.0,
        chunk_size: int = 64 * 1024,
        rate_limit_per_minute: float | None = None,
        burst: float | None = None,
        log: Callable[[dict[str, object]], None] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        if concurrency < 1:
            raise ValueError("concurrency must be at least 1")
        self.concurrency = concurrency
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self.timeout = timeout
        self.chunk_size = chunk_size
        self._sem = asyncio.Semaphore(concurrency)
        self._bucket = (
            TokenBucket.per_minute(rate_limit_per_minute, burst)
            if rate_limit_per_minute
            else None
        )
        self._log = log or _default_log
        self._rng = rng or random.Random(0xC0FFEE)
        self.in_flight = 0
        self.peak_in_flight = 0

    # -- one attempt ------------------------------------------------------
    async def _attempt(self, spec: DownloadSpec, attempt: int) -> Result:
        part = spec.dest.with_suffix(spec.dest.suffix + ".part")
        start = part.stat().st_size if part.exists() else 0
        digest = hashlib.sha256()
        if start:
            with part.open("rb") as fh:
                for block in iter(lambda: fh.read(1 << 20), b""):
                    digest.update(block)

        if self._bucket is not None:
            await self._bucket.take()

        began = time.monotonic()
        resp = await _open(spec.url, start, self.timeout)
        try:
            if resp.status not in (200, 206):
                raise HttpError(resp.status, spec.url)
            if start and resp.status == 200:
                # The server ignored our Range; start over rather than concatenate.
                start = 0
                digest = hashlib.sha256()
                part.unlink(missing_ok=True)

            expected = resp.content_length
            written = 0
            spec.dest.parent.mkdir(parents=True, exist_ok=True)
            mode = "ab" if start else "wb"
            with part.open(mode) as fh:
                while True:
                    chunk = await asyncio.wait_for(
                        resp.reader.read(self.chunk_size), self.timeout
                    )
                    if not chunk:
                        break
                    fh.write(chunk)
                    digest.update(chunk)
                    written += len(chunk)
                fh.flush()
                os.fsync(fh.fileno())

            if expected is not None and written != expected:
                raise TruncatedResponse(
                    f"{spec.url}: expected {expected} bytes, got {written}"
                )
            if spec.sha256 is not None and digest.hexdigest() != spec.sha256:
                # A wrong body is worse than no body. Throw the partial away so the
                # retry starts clean rather than resuming into corruption.
                part.unlink(missing_ok=True)
                raise ChecksumMismatch(f"{spec.url}: sha256 mismatch")

            os.replace(part, spec.dest)   # atomic: a reader never sees a partial file
            total = start + written
            self._log({
                "event": "downloaded", "url": spec.url, "attempt": attempt,
                "status": resp.status, "bytes": total, "resumed_from": start,
                "duration_ms": round((time.monotonic() - began) * 1000, 2),
            })
            return Result(spec.url, spec.dest, True, total, attempt, start)
        finally:
            resp.writer.close()
            try:
                await resp.writer.wait_closed()
            except (ConnectionResetError, BrokenPipeError):
                pass

    # -- retries ----------------------------------------------------------
    async def fetch(self, spec: DownloadSpec) -> Result:
        if spec.dest.exists():
            # Already complete. Skipping means zero network calls, which is what makes
            # a re-run after a crash cheap.
            self._log({"event": "skipped", "url": spec.url, "dest": str(spec.dest)})
            return Result(spec.url, spec.dest, True, spec.dest.stat().st_size, 0, skipped=True)

        last: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            async with self._sem:
                self.in_flight += 1
                self.peak_in_flight = max(self.peak_in_flight, self.in_flight)
                try:
                    return await self._attempt(spec, attempt)
                except asyncio.CancelledError:
                    raise
                except HttpError as exc:
                    last = exc
                    self._log({"event": "attempt_failed", "url": spec.url,
                               "attempt": attempt, "status": exc.status,
                               "error": str(exc), "retryable": exc.retryable})
                    if not exc.retryable:
                        break
                except (TruncatedResponse, ChecksumMismatch, asyncio.TimeoutError,
                        ConnectionError, OSError) as exc:
                    last = exc
                    self._log({"event": "attempt_failed", "url": spec.url,
                               "attempt": attempt, "error": f"{type(exc).__name__}: {exc}"})
                finally:
                    self.in_flight -= 1

            if attempt < self.max_retries:
                # Exponential backoff with full jitter: without the jitter, N clients
                # that failed together retry together, forever.
                window = min(self.backoff_cap, self.backoff_base * (2 ** (attempt - 1)))
                await asyncio.sleep(self._rng.uniform(0, window))

        self._log({"event": "failed", "url": spec.url, "error": str(last)})
        return Result(spec.url, spec.dest, False, 0, self.max_retries, error=str(last))

    # -- the whole job ----------------------------------------------------
    async def run(self, specs: Iterable[DownloadSpec]) -> list[Result]:
        """Stream the work through a bounded worker pool.

        Deliberately NOT `asyncio.gather(*[...])`: that builds one task per spec up
        front, so 10,000 URLs is 10,000 live Task objects before a byte moves. This
        version keeps `concurrency` tasks alive regardless of how many specs there are.
        """
        queue: asyncio.Queue[DownloadSpec | None] = asyncio.Queue(maxsize=self.concurrency * 2)
        results: list[Result] = []
        results_lock = asyncio.Lock()

        async def worker() -> None:
            while True:
                spec = await queue.get()
                try:
                    if spec is None:
                        return
                    result = await self.fetch(spec)
                    async with results_lock:
                        results.append(result)
                finally:
                    queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(self.concurrency)]
        try:
            for spec in specs:
                await queue.put(spec)
            for _ in workers:
                await queue.put(None)
            await asyncio.gather(*workers)
        except (asyncio.CancelledError, KeyboardInterrupt):
            # Cancel in flight, then WAIT for the cleanup to finish. Cancelling and
            # returning immediately is how you end up with a half-written .part file
            # and a process that exits before the finally blocks run.
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            self._log({"event": "cancelled", "completed": len(results)})
            raise
        return results


def _default_log(record: dict[str, object]) -> None:
    print(json.dumps(record, sort_keys=True), file=sys.stderr)


# ------------------------------------------------------------------------- basic
async def download_all(urls: list[str], dest_dir: Path) -> list[Path]:
    """`basic` track: fetch every URL concurrently, print a progress counter.

    `return_exceptions=True` matters: without it, one failure cancels the gather and
    you lose the results of everything that already succeeded.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    total = len(urls)
    done = 0
    lock = asyncio.Lock()

    async def one(index: int, url: str) -> Path:
        nonlocal done
        dest = dest_dir / f"{index:04d}_{Path(urlsplit(url).path).name or 'index'}"
        resp = await _open(url, 0, 10.0)
        try:
            if resp.status != 200:
                raise HttpError(resp.status, url)
            body = bytearray()
            while chunk := await resp.reader.read(64 * 1024):
                body.extend(chunk)
            dest.write_bytes(bytes(body))
        finally:
            resp.writer.close()
        async with lock:
            done += 1
            print(f"[{done}/{total}] {url}")
        return dest

    outcomes = await asyncio.gather(
        *(one(i, u) for i, u in enumerate(urls)), return_exceptions=True
    )
    paths: list[Path] = []
    for url, outcome in zip(urls, outcomes, strict=True):
        if isinstance(outcome, BaseException):
            raise DownloadError(f"{url}: {outcome}") from outcome
        paths.append(outcome)
    return paths
