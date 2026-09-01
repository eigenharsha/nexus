"""LAB-P1-W04 — the async concurrent downloader. YOUR WORK GOES HERE.

basic:    implement `download_all` with asyncio.gather + a progress counter.
standard: implement the `Downloader` class per standard/SPEC.md.
hard:     add the token bucket and make `run` stream instead of materialising.

Stdlib only. `_open` below is given to you — a minimal HTTP/1.1 GET over
`asyncio.open_connection` — so that the lab is about concurrency, retries and
correctness rather than about parsing HTTP. Everything else is yours.

Read `tests/flaky_server.py` before you start. It is the spec for the failure
modes you have to survive, and it is more precise than any prose could be.
"""
from __future__ import annotations

import asyncio
import random
from collections.abc import Callable, Iterable
from dataclasses import dataclass
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
        # TODO (standard): 5xx and 429 are worth another go. 404 never is.
        raise NotImplementedError("HttpError.retryable")


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


class TokenBucket:
    """TODO (hard): `rate` tokens per second, burst up to `capacity`.

    Async-safe — hold a lock across refill-and-take, or N coroutines will each see
    the same token and you will sail straight through the rate limit.
    """

    def __init__(self, rate_per_second: float, capacity: float | None = None) -> None:
        raise NotImplementedError("TokenBucket")

    @classmethod
    def per_minute(cls, requests_per_minute: float, burst: float | None = None) -> "TokenBucket":
        return cls(requests_per_minute / 60.0, burst)

    async def take(self, n: float = 1.0) -> None:
        raise NotImplementedError("TokenBucket.take")


# --------------------------------------------------------------------------- given
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
    """A minimal HTTP/1.1 GET. Given to you — do not spend the lab on this."""
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


# ---------------------------------------------------------------------- your work
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
        # The tests read `peak_in_flight`; keep it accurate.
        self.peak_in_flight = 0
        raise NotImplementedError("Downloader.__init__")

    async def fetch(self, spec: DownloadSpec) -> Result:
        """One file, with retries.

        Order of business:
          1. dest already exists -> skip, with zero network calls
          2. a .part file exists -> resume with `Range: bytes=N-`
          3. stream the body to <dest>.part in chunk_size pieces
          4. check the length against Content-Length; check the sha256 if given
          5. os.replace(.part, dest)  — atomic, so a reader never sees a partial file
        """
        raise NotImplementedError("Downloader.fetch")

    async def run(self, specs: Iterable[DownloadSpec]) -> list[Result]:
        """The whole job.

        NOT `asyncio.gather(*[self.fetch(s) for s in specs])` — that builds one Task
        per spec before a byte moves, and 10,000 of them will not fit in the hard
        track's memory ceiling. Use a bounded queue and `concurrency` workers.

        On cancellation: cancel the workers, then AWAIT them, then re-raise. Returning
        without awaiting leaves half-written files behind.
        """
        raise NotImplementedError("Downloader.run")


async def download_all(urls: list[str], dest_dir: Path) -> list[Path]:
    """`basic` track.

    Fetch every URL concurrently with `asyncio.gather`, print `[k/n] <url>` as each
    one lands, and return the destination paths **in the same order as the input**.

    Pass `return_exceptions=True`: without it, one failure cancels the gather and
    you throw away every result that had already succeeded.
    """
    raise NotImplementedError("download_all")
