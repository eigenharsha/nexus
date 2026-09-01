"""Sequential vs threaded vs async, on the identical workload against the local
flaky server. This is the ship-it deliverable for LAB-P1-W04.

    make bench IMPL=solution

The workload is deliberately I/O bound with a small body: 60 files of 32 KB, each
with a 20 ms server-side stall. That is the shape of the real ingest job — the time
is latency, not bytes — and it is the shape where the three strategies differ most.
"""
from __future__ import annotations

import asyncio
import http.client
import shutil
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tests.flaky_server import FlakyServer  # noqa: E402

from downloader import DownloadSpec, Downloader  # noqa: E402

N_FILES = 60
SIZE = 32 * 1024
STALL = 0.02


def fetch_blocking(url: str, dest: Path) -> int:
    parts = urlsplit(url)
    conn = http.client.HTTPConnection(parts.hostname, parts.port, timeout=10)
    try:
        conn.request("GET", parts.path)
        resp = conn.getresponse()
        data = resp.read()
        dest.write_bytes(data)
        return len(data)
    finally:
        conn.close()


def start_server_in_thread() -> tuple[FlakyServer, threading.Thread, asyncio.AbstractEventLoop]:
    """The server must live on its own event loop in its own thread.

    The sequential and threaded clients block; if the server shared their loop, a
    blocking recv would stop the server from ever answering it. That deadlock is
    itself worth understanding — it is exactly what happens when you put a blocking
    call inside a coroutine.
    """
    loop = asyncio.new_event_loop()
    srv = FlakyServer()
    ready = threading.Event()

    def run() -> None:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(srv.start())
        loop.call_soon(ready.set)
        loop.run_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    ready.wait(5)
    return srv, thread, loop


def main() -> None:
    out = Path("bench")
    out.mkdir(exist_ok=True)
    # Start from an empty tree: the downloader skips files that already exist, which
    # is correct behaviour and would turn a second benchmark run into a no-op.
    for stale in out.glob("*/"):
        shutil.rmtree(stale, ignore_errors=True)
    rows: list[tuple[str, float, float]] = []

    srv, thread, loop = start_server_in_thread()
    try:
        for i in range(N_FILES):
            srv.add(f"f{i}", bytes((i + j) % 251 for j in range(SIZE)), stall_seconds=STALL)
        urls = [srv.url(f"f{i}") for i in range(N_FILES)]

        # --- sequential --------------------------------------------------
        d = out / "seq"; d.mkdir(exist_ok=True)
        t0 = time.monotonic()
        for i, u in enumerate(urls):
            fetch_blocking(u, d / f"f{i}")
        rows.append(("sequential", time.monotonic() - t0, 1))

        # --- threads -----------------------------------------------------
        for workers in (8, 32):
            d = out / f"threads{workers}"; d.mkdir(exist_ok=True)
            t0 = time.monotonic()
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(lambda iu: fetch_blocking(iu[1], d / f"f{iu[0]}"),
                              list(enumerate(urls))))
            rows.append((f"threads x{workers}", time.monotonic() - t0, workers))

        # --- asyncio -----------------------------------------------------
        for conc in (8, 32):
            d = out / f"async{conc}"; d.mkdir(exist_ok=True)

            async def run_async(directory: Path = d, concurrency: int = conc) -> float:
                dl = Downloader(concurrency=concurrency, log=lambda r: None)
                specs = [DownloadSpec(u, directory / f"f{i}") for i, u in enumerate(urls)]
                t = time.monotonic()
                results = await dl.run(specs)
                assert all(r.ok for r in results)
                return time.monotonic() - t

            rows.append((f"asyncio x{conc}", asyncio.run(run_async()), conc))
    finally:
        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=2)

    base = rows[0][1]
    print(f"\n{N_FILES} files x {SIZE // 1024} KB, {int(STALL * 1000)} ms server stall each\n")
    print(f"  {'strategy':<16} {'wall (s)':>9} {'files/s':>9} {'speedup':>9}")
    print("  " + "-" * 47)
    lines = []
    for name, elapsed, _ in rows:
        line = f"  {name:<16} {elapsed:>9.2f} {N_FILES / elapsed:>9.1f} {base / elapsed:>8.1f}x"
        print(line)
        lines.append(f"| {name} | {elapsed:.2f} | {N_FILES / elapsed:.1f} | {base / elapsed:.1f}x |")
    (out / "results.md").write_text(
        "| strategy | wall (s) | files/s | speedup |\n|---|---|---|---|\n" + "\n".join(lines) + "\n"
    )
    print(f"\nwrote {out / 'results.md'}")


if __name__ == "__main__":
    main()
