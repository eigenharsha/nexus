"""A deterministic flaky HTTP server, for testing a downloader without the internet.

A test that hits a real CDN is not a test: it is slow, it fails for reasons that are not
your code, and it cannot reproduce the failure you actually care about. This fixture can,
on demand and reproducibly:

  * return 503 for the first N attempts of a path, then succeed
  * return 429 with a Retry-After header
  * truncate the body at a byte offset while still advertising the full Content-Length
  * stall past your timeout
  * honour a `Range: bytes=N-` header with a 206 and a Content-Range
  * return 404 (which must NOT be retried)

It also records what the client did, which is how the acceptance tests check the things
you cannot see from the client side: peak concurrency, the request timeline, and how many
times each destination file was opened for writing.

Everything is stdlib asyncio — no aiohttp, no httpx, nothing to install.
"""
from __future__ import annotations

import asyncio
import hashlib
import time
from dataclasses import dataclass, field


@dataclass
class FileSpec:
    body: bytes
    fail_first: int = 0          # 503 for this many attempts, then succeed
    status_when_failing: int = 503
    truncate_at: int | None = None  # send only this many bytes on the FIRST attempt
    stall_seconds: float = 0.0   # sleep before responding, on every attempt
    status: int = 200            # 404 to make it permanently absent
    attempts: int = 0
    supports_range: bool = True

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()


@dataclass
class RequestRecord:
    path: str
    at: float
    range_header: str | None
    status: int


class FlakyServer:
    def __init__(self) -> None:
        self.files: dict[str, FileSpec] = {}
        self.requests: list[RequestRecord] = []
        self._server: asyncio.AbstractServer | None = None
        self._active = 0
        self.max_concurrent = 0
        self.host = "127.0.0.1"
        self.port = 0
        self.started_at = 0.0

    # ------------------------------------------------------------------ setup
    def add(self, name: str, body: bytes, **kwargs: object) -> FileSpec:
        spec = FileSpec(body=body, **kwargs)  # type: ignore[arg-type]
        self.files[f"/{name}"] = spec
        return spec

    def url(self, name: str) -> str:
        return f"http://{self.host}:{self.port}/{name}"

    async def start(self) -> "FlakyServer":
        self._server = await asyncio.start_server(self._handle, self.host, 0)
        sock = self._server.sockets[0]
        self.port = sock.getsockname()[1]
        self.started_at = time.monotonic()
        return self

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()

    async def __aenter__(self) -> "FlakyServer":
        return await self.start()

    async def __aexit__(self, *exc: object) -> None:
        await self.stop()

    # ------------------------------------------------------- what the tests read
    def requests_for(self, name: str) -> list[RequestRecord]:
        return [r for r in self.requests if r.path == f"/{name}"]

    def peak_rate_per_minute(self, window: float = 60.0) -> float:
        """Highest request count in any `window`-second sliding window, scaled to /minute."""
        if not self.requests:
            return 0.0
        times = sorted(r.at for r in self.requests)
        best = 0
        j = 0
        for i, t in enumerate(times):
            while times[i] - times[j] > window:
                j += 1
            best = max(best, i - j + 1)
        return best * (60.0 / window)

    # ---------------------------------------------------------------- protocol
    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self._active += 1
        self.max_concurrent = max(self.max_concurrent, self._active)
        try:
            head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=10)
        except (asyncio.IncompleteReadError, asyncio.TimeoutError, ConnectionResetError):
            self._active -= 1
            writer.close()
            return

        try:
            lines = head.decode("latin-1").split("\r\n")
            method, target, _ = lines[0].split(" ", 2)
            headers = {}
            for line in lines[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

            spec = self.files.get(target)
            rng = headers.get("range")
            if spec is None:
                await self._respond(writer, 404, b"not found")
                self.requests.append(RequestRecord(target, time.monotonic(), rng, 404))
                return

            spec.attempts += 1
            attempt = spec.attempts

            if spec.stall_seconds:
                await asyncio.sleep(spec.stall_seconds)

            if spec.status != 200:
                await self._respond(writer, spec.status, b"gone")
                self.requests.append(RequestRecord(target, time.monotonic(), rng, spec.status))
                return

            if attempt <= spec.fail_first:
                extra = {"Retry-After": "0"} if spec.status_when_failing == 429 else None
                await self._respond(writer, spec.status_when_failing, b"try again", extra)
                self.requests.append(
                    RequestRecord(target, time.monotonic(), rng, spec.status_when_failing)
                )
                return

            body = spec.body
            status = 200
            extra_headers: dict[str, str] = {}
            if rng and spec.supports_range:
                # only `bytes=N-` is used by this lab
                start = int(rng.split("=", 1)[1].split("-", 1)[0])
                body = spec.body[start:]
                status = 206
                extra_headers["Content-Range"] = (
                    f"bytes {start}-{len(spec.body) - 1}/{len(spec.body)}"
                )

            truncate = spec.truncate_at is not None and attempt == 1
            await self._respond(
                writer, status, body, extra_headers,
                send_only=spec.truncate_at if truncate else None,
            )
            self.requests.append(RequestRecord(target, time.monotonic(), rng, status))
        except Exception:  # a broken client must not take the server down
            pass
        finally:
            self._active -= 1
            try:
                writer.close()
                await writer.wait_closed()
            except (ConnectionResetError, BrokenPipeError):
                pass

    async def _respond(
        self,
        writer: asyncio.StreamWriter,
        status: int,
        body: bytes,
        extra: dict[str, str] | None = None,
        send_only: int | None = None,
    ) -> None:
        reason = {200: "OK", 206: "Partial Content", 404: "Not Found",
                  410: "Gone", 429: "Too Many Requests", 503: "Service Unavailable"}.get(status, "OK")
        lines = [f"HTTP/1.1 {status} {reason}",
                 f"Content-Length: {len(body)}",
                 "Accept-Ranges: bytes",
                 "Connection: close"]
        for k, v in (extra or {}).items():
            lines.append(f"{k}: {v}")
        head = ("\r\n".join(lines) + "\r\n\r\n").encode("latin-1")
        writer.write(head)
        # Advertise the full length but send less: this is the silent-corruption case.
        payload = body if send_only is None else body[:send_only]
        for i in range(0, len(payload), 64 * 1024):
            writer.write(payload[i:i + 64 * 1024])
            await writer.drain()
        if not payload:
            await writer.drain()


@dataclass
class WriteWatch:
    """Counts how many times each path was opened for writing, so a test can prove
    no file was written twice."""

    opens: dict[str, int] = field(default_factory=dict)

    def record(self, path: str) -> None:
        self.opens[path] = self.opens.get(path, 0) + 1
