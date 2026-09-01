# Phase 1 — Granular Task Breakdown (Weeks 1–8)
**Goal:** zero programming background → building, testing, containerizing and securing asynchronous web backends with a real relational database.

Each **module** = one lesson file written in all 3 layers (see `PLAN/00-content-spec.md`).
Each module ID maps to `content/phase-1/week-NN/MX-slug.md` and a lab under `labs/phase-1/week-NN/`.

---

## T-P1-W01 — Week 1: Algorithmic Thinking & Memory Foundations (C)

**Week outcome:** learner can explain what happens between typing code and the CPU running it, manage memory by hand, and implement + measure classic algorithms with zero leaks.
**Why C first:** every abstraction later (Python objects, tensors, GPU memory, KV-cache) is a lie told on top of malloc. Learn the truth once.

### `P1-W01-M1` — How a computer represents everything
- Micro-lessons: (a) bits, bytes, words; (b) integers, two's complement, overflow; (c) text: ASCII → UTF-8; (d) pixels, audio, and why "everything is a number"
- **L1 Ground:** counting in binary by hand, the light-switch analogy, converting your name to bytes.
- **L2 Build:** signed vs unsigned bugs, integer overflow in real CVEs, endianness when parsing binary files/network packets, `hexdump` a file you made.
- **L3 Edge:** IEEE-754 floats — why `0.1+0.2 != 0.3`, denormals, and how FP16/BF16/FP8 (Week 26 quantization) are just fewer bits in the same layout. Compute the exact representable range of BF16.
- **Hands-on:** write `binviz.c` that prints the bit pattern of any int/float/char the user passes; verify against `hexdump -C`.

### `P1-W01-M2` — From source code to running process
- Micro-lessons: (a) preprocess → compile → assemble → link; (b) object files and symbols; (c) the process address space; (d) reading a tiny bit of assembly
- **L1 Ground:** what `gcc hello.c` actually does, in four pictures.
- **L2 Build:** `gcc -E/-S/-c`, static vs dynamic linking, why "undefined reference" happens, `nm`/`ldd`, header guards, `Makefile` basics.
- **L3 Edge:** ABI & calling conventions, `-O0` vs `-O2` on the same function in Godbolt, why the optimizer deleted your benchmark loop.
- **Hands-on:** take one `.c` file, produce and inspect all 4 intermediate artifacts; write a Makefile that builds debug + release targets.

### `P1-W01-M3` — Stack, heap, and pointers
- Micro-lessons: (a) variables and addresses; (b) stack frames & scope; (c) `malloc`/`free`/`realloc`; (d) pointer arithmetic & arrays; (e) structs and memory layout
- **L1 Ground:** the "house address vs house" analogy; drawing a stack frame on paper for a 3-function call chain.
- **L2 Build:** ownership discipline (who frees?), dangling pointers, double-free, off-by-one, `strcpy` vs `strncpy`, null-terminator bugs; struct padding & alignment.
- **L3 Edge:** the allocator itself — bins, arenas, fragmentation; why `malloc(1)` costs 32 bytes; ASan/Valgrind internals (redzones, shadow memory); a deliberate stack-overflow demo and what canaries do.
- **Hands-on:** implement a tiny bump allocator + free-list allocator in ~150 lines and benchmark against `malloc`.

### `P1-W01-M4` — Algorithms & asymptotic complexity
- Micro-lessons: (a) what "faster" means; (b) Big-O/Ω/Θ intuitively; (c) selection sort; (d) merge sort & divide-and-conquer; (e) binary search & invariants
- **L1 Ground:** counting operations by hand on n=8; the phone-book analogy for binary search; growth-rate table (n vs n log n vs n²) at n = 10 / 1k / 1M.
- **L2 Build:** recursion + recurrence relations, in-place vs extra memory, stability, when O(n²) beats O(n log n) (small n, cache locality), correct binary-search boundary conditions.
- **L3 Edge:** cache effects & memory hierarchy — measure why merge sort's memory traffic hurts; branch misprediction; introsort/timsort hybrids in real stdlibs; read `qsort` source.
- **Hands-on:** implement all three; plot measured runtime vs n on log-log axes and fit the exponent.

### `P1-W01-M5` — Correctness, debugging & memory safety tooling
- Micro-lessons: (a) reading compiler errors; (b) `printf` debugging vs `gdb`; (c) Valgrind & AddressSanitizer; (d) writing your first tests; (e) undefined behavior
- **L1 Ground:** a guided bug hunt: 5 broken programs, find and fix each with the tool named.
- **L2 Build:** `gdb` workflow (breakpoints, watchpoints, backtrace), interpreting Valgrind output line-by-line, `-fsanitize=address,undefined`, assertions as executable documentation.
- **L3 Edge:** what UB lets the compiler legally do to your program (with a Godbolt example where UB deletes a security check); fuzzing intro with `afl`/`libFuzzer`.
- **Hands-on:** given a leaky, UB-ridden 300-line C program, get it to zero Valgrind errors and zero sanitizer warnings without changing behavior.

### `LAB-P1-W01` — **Sorting & Search Toolkit in C**
- `basic`: fill in TODOs for selection sort + binary search against provided tests.
- `standard`: implement selection sort, merge sort, binary search, plus a benchmark harness writing CSV; must be leak-free under Valgrind.
- `hard`: sort a 50M-element file that does not fit in your RAM budget (external merge sort), report wall time and peak RSS.
- **Ship it:** GitHub repo + README with the log-log runtime plot and a paragraph explaining the fitted exponent.
- **Rubric:** correctness / memory-clean / benchmark quality / written explanation.

---

## T-P1-W02 — Week 2: Terminal Literacy, Version Control & Vim

**Week outcome:** learner lives in the terminal, automates a real recurring chore, and uses Git the way a team uses it (branches, conflicts, SSH, history surgery).

### `P1-W02-M1` — The shell & filesystem as a system
- Micro-lessons: (a) what a shell is; (b) paths, permissions, ownership; (c) processes, jobs, signals; (d) environment variables & `PATH`
- **L1 Ground:** navigating, creating, moving, deleting; `chmod` explained with the 3×3 grid; killing a runaway process.
- **L2 Build:** `PATH` resolution order, `.zshrc`/`.bashrc` vs login shells, `nohup`/`&`/`jobs`/`trap`, exit codes and why they matter in CI, `set -euo pipefail`.
- **L3 Edge:** file descriptors & the `/proc` view of a process, `strace`/`dtruss` on a simple command, how `sudo` and setuid actually work, umask.
- **Hands-on:** reconstruct what a mystery binary does using only `strace`, `lsof`, and `ps`.

### `P1-W02-M2` — Text processing & pipelines
- Micro-lessons: (a) stdin/stdout/stderr & redirection; (b) `grep` + regex; (c) `sed`/`awk`/`cut`/`sort`/`uniq`; (d) `find` + `xargs`; (e) `jq` for JSON
- **L1 Ground:** build one pipeline step by step, printing intermediate output each time.
- **L2 Build:** regex properly (anchors, classes, groups, greedy vs lazy, backreferences); log-analysis recipes; safe `find -print0 | xargs -0`.
- **L3 Edge:** catastrophic backtracking (ReDoS) with a measured example; when to stop shell-scripting and switch to Python; GNU vs BSD tool differences that break scripts on macOS.
- **Hands-on:** from a 1 GB nginx log, produce top-20 endpoints by p95 latency using only shell tools; time it.

### `P1-W02-M3` — Bash scripting & automation
- Micro-lessons: (a) variables, quoting, expansion; (b) conditionals & loops; (c) functions & arguments; (d) cron/launchd & systemd timers; (e) `shellcheck`
- **L1 Ground:** a 20-line backup script written together, line by line.
- **L2 Build:** quoting rules that prevent 90% of bugs, argument parsing, idempotency, locking (`flock`) so two cron runs don't collide, structured logging, error traps.
- **L3 Edge:** signal handling and cleanup on `SIGTERM`, race conditions in scripts, why production automation eventually moves off bash — and the exact thresholds where it should.
- **Hands-on:** write a script that is safely re-runnable 100× and provably does nothing the second time.

### `P1-W02-M4` — Git: the model, not the commands
- Micro-lessons: (a) commits as a DAG of snapshots; (b) branches & HEAD; (c) merge vs rebase; (d) conflicts; (e) remotes, PRs, and review flow
- **L1 Ground:** draw the commit graph after every command; init → commit → branch → merge, with `git log --graph` after each step.
- **L2 Build:** real branching strategy, atomic commits + good messages, `rebase -i` to clean history, `stash`, `cherry-pick`, `.gitignore`, resolving a genuine 3-way conflict, PR review etiquette.
- **L3 Edge:** the object database — blobs/trees/commits, content-addressing, `git cat-file`, packfiles; `reflog` + `fsck` to recover "lost" work; `bisect` to find a regression in 40 commits; hooks and monorepo-scale pain.
- **Hands-on:** given a repo with a bug introduced somewhere in 200 commits, find it with `git bisect run`.

### `P1-W02-M5` — SSH, keys & remote work + Vim survival
- Micro-lessons: (a) public-key crypto in 10 minutes; (b) generating/using keys, `ssh-agent`, `~/.ssh/config`; (c) `scp`/`rsync`/port-forwarding; (d) Vim modal editing; (e) `tmux`
- **L1 Ground:** generate a key, add it to GitHub, push over SSH; Vim: open, edit, save, quit, and never be trapped again.
- **L2 Build:** key types (ed25519 vs RSA), passphrases + agent forwarding risk, jump hosts, local/remote port forwarding for debugging a remote DB, Vim motions/registers/macros, tmux sessions surviving disconnects.
- **L3 Edge:** how the SSH handshake works (KEX, host-key trust, TOFU), what a man-in-the-middle actually gets, hardening `sshd_config`; certificate-based auth instead of `authorized_keys`.
- **Hands-on:** tunnel to a Postgres running on a remote box and query it locally with zero ports exposed publicly.

### `LAB-P1-W02` — **Self-Reporting System Monitor**
- `basic`: bash script that samples CPU/memory once and prints a formatted report.
- `standard`: daemonized sampler (cron/launchd) that writes a rolling metrics file, generates a markdown report, and commits + pushes to a Git repo over SSH — idempotent, locked, logged.
- `hard`: add alert thresholds, `SIGTERM`-safe shutdown, log rotation, and a `git bisect`-friendly commit history; survive being killed mid-write without corrupting the metrics file.
- **Ship it:** public repo whose commit history is *itself* generated by the lab.

---

## T-P1-W03 — Week 3: Python Core & Object-Oriented Design

**Week outcome:** learner writes idiomatic, typed, tested Python and designs classes that a reviewer would approve.

### `P1-W03-M1` — Python's model: objects, names & memory
- Micro-lessons: (a) everything is an object; (b) names vs values (binding, not assignment); (c) mutability & aliasing bugs; (d) reference counting & GC; (e) `id`, `is` vs `==`
- **L1 Ground:** the "sticky note on a box" model; predicting the output of 10 aliasing puzzles.
- **L2 Build:** mutable default arguments, shallow vs deep copy, `__hash__`/`__eq__` contract, when to use `dataclass(frozen=True)`.
- **L3 Edge:** CPython object headers and why an `int` costs 28 bytes; small-int and string interning; refcount + cycle collector; `__slots__` memory savings measured on 1M objects.
- **Hands-on:** measure memory of 1M records as dict / class / `__slots__` class / `dataclass` / NamedTuple; write up the trade-off.

### `P1-W03-M2` — Data structures and complexity in practice
- Micro-lessons: (a) list/tuple/set/dict semantics; (b) comprehensions & generators; (c) `collections` (`deque`, `Counter`, `defaultdict`); (d) iterators & laziness; (e) `itertools`
- **L1 Ground:** pick the right container for 8 everyday problems.
- **L2 Build:** operation costs table (list insert vs deque, `in` on list vs set), generator pipelines for memory-bounded processing, `yield`, exhaustion bugs.
- **L3 Edge:** dict implementation — open addressing, compact dicts, insertion order guarantee; hash collision behavior and `PYTHONHASHSEED`; measured cost of `list.insert(0,…)` at 1M elements.
- **Hands-on:** process a 2 GB JSONL file under a 200 MB RSS ceiling using generators; prove the ceiling with `/usr/bin/time -v`.

### `P1-W03-M3` — Functions, errors, and the standard library
- Micro-lessons: (a) args/kwargs, defaults, keyword-only; (b) exceptions & custom exception hierarchies; (c) context managers; (d) modules, packages, imports; (e) `pathlib`, `json`, `datetime`, `logging`
- **L1 Ground:** try/except/else/finally with a file that might not exist.
- **L2 Build:** exception design (what to raise, what to let propagate), `with` + `contextlib`, structured logging instead of `print`, timezone-aware datetimes, import system & circular-import fixes.
- **L3 Edge:** `sys.modules` and import machinery, `__init__.py` packaging pitfalls, exception performance, `logging` handler/filter architecture at scale, retries with jitter.
- **Hands-on:** convert a `print`-debugged script into structured JSON logs with correlation IDs.

### `P1-W03-M4` — Object-oriented design done properly
- Micro-lessons: (a) classes, instances, `self`; (b) encapsulation & properties; (c) inheritance, MRO, composition; (d) `@classmethod` vs `@staticmethod` vs instance methods; (e) dunder methods & protocols; (f) ABCs and `Protocol`
- **L1 Ground:** model a `BankAccount` with validation; the exact difference between the three method types, with a `from_csv` factory as the motivating example.
- **L2 Build:** composition over inheritance with a refactor, SOLID applied to a real module, `@property` for computed/validated fields, duck typing vs `Protocol`, `__repr__`/`__eq__`/`__iter__`/`__enter__`.
- **L3 Edge:** the descriptor protocol (how `@property` is *implemented*), metaclasses and `__init_subclass__`, C3 linearization on a diamond, `attrs`/`pydantic` internals preview.
- **Hands-on:** implement `@property` from scratch as a descriptor class; make it pass the same tests as the builtin.

### `P1-W03-M5` — Professional Python: typing, testing, tooling, packaging
- Micro-lessons: (a) type hints & `mypy`; (b) `pytest` (fixtures, parametrize, mocks); (c) `ruff`/formatting; (d) `uv`, virtual envs, dependency pinning; (e) project layout & publishing
- **L1 Ground:** add types + 5 tests to a 60-line script.
- **L2 Build:** generics, `Optional`/unions, `TypedDict`, protocols; fixture scopes, parametrized tests, `monkeypatch`, coverage that means something; `pyproject.toml`, lockfiles, reproducible envs; pre-commit hooks.
- **L3 Edge:** gradual typing at scale, `mypy --strict` migration strategy, why type hints are erased at runtime and what `pydantic` does about it; test flakiness, property-based testing with `hypothesis`.
- **Hands-on:** find a real bug in provided code using `hypothesis` that the example-based tests miss.

### `LAB-P1-W03` — **`ledger` — a typed, tested, packaged Python library**
- `basic`: implement `Account`/`Transaction` classes to pass provided tests.
- `standard`: full library — validation via properties, custom exceptions, `Protocol`-based storage backend (memory + JSON file), 90%+ meaningful coverage, `mypy --strict` clean, `ruff` clean, installable via `uv`.
- `hard`: add a second storage backend without modifying core code (prove Open/Closed), plus `hypothesis` invariant tests (balance never drifts under any sequence of ops).
- **Ship it:** publish to TestPyPI; README with API docs.

---

## T-P1-W04 — Week 4: Concurrency, Parallelism & `asyncio`

**Week outcome:** learner can correctly choose between threads, processes and async, and build an async I/O pipeline that is fast, bounded and resilient.

### `P1-W04-M1` — Concurrency vs parallelism vs the GIL
- Micro-lessons: (a) the two words, precisely; (b) CPU-bound vs I/O-bound; (c) what the GIL is and isn't; (d) choosing a model
- **L1 Ground:** the "one chef, many pots" analogy; measure the same workload three ways.
- **L2 Build:** decision table (threads / processes / asyncio / native lib releasing the GIL); Amdahl's law with a real measured speedup curve.
- **L3 Edge:** GIL internals & switch interval, free-threaded CPython (3.13+ `--disable-gil`) status and what it changes, NumPy/BLAS releasing the GIL, subinterpreters.
- **Hands-on:** benchmark matrix: {CPU-bound, I/O-bound} × {sequential, threads, processes, asyncio}; produce the table and defend every cell.

### `P1-W04-M2` — Threads and shared state
- Micro-lessons: (a) `threading` basics; (b) race conditions; (c) locks, RLock, semaphores, events; (d) `queue.Queue` & producer-consumer; (e) `ThreadPoolExecutor`
- **L1 Ground:** watch a counter give the wrong answer, then fix it with a lock.
- **L2 Build:** lock granularity, deadlock (and the 4 conditions), thread-safe designs preferring queues over shared mutable state, thread pools for I/O, timeouts everywhere.
- **L3 Edge:** memory model & visibility, lock contention measured, false sharing, why "just add threads" stops scaling; `concurrent.futures` internals.
- **Hands-on:** reproduce a deadlock deliberately, capture it with `faulthandler`/`py-spy`, then fix by lock ordering.

### `P1-W04-M3` — Processes and true parallelism
- Micro-lessons: (a) `multiprocessing` & start methods; (b) pickling boundaries; (c) IPC: pipes, queues, shared memory; (d) `ProcessPoolExecutor`; (e) when to leave Python
- **L1 Ground:** parallelize a CPU-heavy loop and measure the speedup on your core count.
- **L2 Build:** fork vs spawn (and the macOS/Windows gotcha), serialization cost dominating small tasks, chunking strategy, `shared_memory` for big arrays, graceful shutdown.
- **L3 Edge:** copy-on-write and why forked workers still blow up RSS, NUMA effects, oversubscription with BLAS threads (`OMP_NUM_THREADS`) — a very common silent 5× slowdown in ML jobs.
- **Hands-on:** find the task size at which process-pool overhead is repaid; plot the crossover.

### `P1-W04-M4` — `asyncio`: the event loop from first principles
- Micro-lessons: (a) blocking vs non-blocking I/O; (b) coroutines, `async`/`await`; (c) tasks, `gather`, `TaskGroup`; (d) cancellation & timeouts; (e) async context managers & iterators; (f) mixing sync code (`to_thread`, `run_in_executor`)
- **L1 Ground:** the restaurant-waiter analogy; sequential vs `gather` on 20 HTTP calls, with timings.
- **L2 Build:** `aiohttp`/`httpx` clients with connection pooling, bounded concurrency via `Semaphore`, retries with exponential backoff + jitter, `asyncio.timeout`, structured concurrency with `TaskGroup`, never blocking the loop.
- **L3 Edge:** write a mini event loop over `selectors` to prove there's no magic; `uvloop` benchmark; back-pressure; debugging with `asyncio` debug mode and slow-callback warnings; task-cancellation edge cases that corrupt state.
- **Hands-on:** implement a 120-line event loop that runs your own coroutines.

### `P1-W04-M5` — Reliability patterns for I/O-heavy systems
- Micro-lessons: (a) retries & idempotency; (b) rate limiting; (c) circuit breakers; (d) timeouts & deadlines; (e) progress, cancellation, resumability
- **L1 Ground:** add a retry loop to a flaky download.
- **L2 Build:** token-bucket limiter implementation, honoring `Retry-After`/429, budget-based deadlines propagated through calls, resumable downloads via HTTP `Range`, checkpointing.
- **L3 Edge:** retry storms & thundering herd (with math), jitter strategies compared, circuit-breaker state machine, tail latency and why p99 matters more than mean; queueing theory intuition (Little's law).
- **Hands-on:** simulate a flaky server (30% failures, random latency) and tune your client to maximize throughput without exceeding a rate limit.

### `LAB-P1-W04` — **Async Concurrent Downloader**
- `basic`: `asyncio.gather` over a URL list with a progress counter.
- `standard`: class-based downloader — bounded concurrency, per-file progress bars, retries with backoff, checksum verification, resumable via `Range`, graceful `Ctrl-C` cancellation, structured logs, tests against a local flaky-server fixture.
- `hard`: 10,000 URLs under a 500-req/min limit and a 300 MB memory ceiling; produce a throughput/latency report and prove no file was corrupted or double-written.
- **Ship it:** repo + benchmark README comparing sync/threaded/async on the identical workload.

---

## T-P1-W05 — Week 5: Web Plumbing — HTTP, HTML, CSS, ES6

**Week outcome:** learner understands the client-server contract end to end and can build a clean, responsive frontend that consumes an API.

### `P1-W05-M1` — How the web actually works
- Micro-lessons: (a) DNS → TCP → TLS → HTTP; (b) request/response anatomy; (c) methods, status codes, headers; (d) statelessness, cookies, sessions, tokens; (e) caching
- **L1 Ground:** trace one URL from typing to pixels; read a real request in DevTools.
- **L2 Build:** idempotency & safety of methods, content negotiation, `Cache-Control`/ETag, cookies (`HttpOnly`, `SameSite`, `Secure`) vs bearer tokens, redirects, compression.
- **L3 Edge:** HTTP/1.1 vs 2 vs 3 (head-of-line blocking, multiplexing, QUIC) with measured waterfall differences; TLS handshake cost, keep-alive, connection reuse economics.
- **Hands-on:** `curl -v` + Wireshark/DevTools comparison of an HTTP/1.1 vs HTTP/2 page load; write up what changed.

### `P1-W05-M2` — HTML5 & semantic structure
- Micro-lessons: (a) document structure; (b) semantic elements; (c) forms & inputs; (d) accessibility basics (ARIA, labels, focus); (e) meta/SEO
- **L1 Ground:** build a resume page with proper headings, lists, and a form.
- **L2 Build:** form validation attributes, semantic markup driving accessibility, keyboard navigation, screen-reader testing, why div-soup costs you.
- **L3 Edge:** the parser & critical rendering path, render-blocking resources, `defer`/`async`, Core Web Vitals (LCP/CLS/INP) measured on your own page.
- **Hands-on:** run Lighthouse on your page; get accessibility ≥ 95 and explain each fix.

### `P1-W05-M3` — CSS & responsive layout
- Micro-lessons: (a) selectors, specificity, cascade; (b) box model; (c) Flexbox; (d) Grid; (e) media queries & responsive units; (f) custom properties
- **L1 Ground:** center a div three ways and know why each works.
- **L2 Build:** layout decision guide (Flex vs Grid), mobile-first breakpoints, design tokens with CSS variables, dark mode via `prefers-color-scheme`, avoiding layout thrash.
- **L3 Edge:** layout/paint/composite pipeline in DevTools, containment, `will-change` misuse, measuring CLS caused by a font swap.
- **Hands-on:** rebuild a given layout to be pixel-correct at 360 px, 768 px and 1440 px with no horizontal scroll.

### `P1-W05-M4` — Modern JavaScript (ES6+)
- Micro-lessons: (a) types, `let`/`const`, scope; (b) functions, arrow functions, `this`; (c) arrays/objects, destructuring, spread; (d) modules; (e) promises & `async/await`; (f) error handling
- **L1 Ground:** the same "download 3 things" program written with callbacks, then promises, then `async/await`.
- **L2 Build:** the event loop, microtask vs macrotask queues, `Promise.all/allSettled/race`, `AbortController` for cancellation, module bundling basics.
- **L3 Edge:** predicting the exact output order of an interleaved `setTimeout`/promise/`await` puzzle; closures & memory leaks; why the browser event loop and Python's `asyncio` are the same idea.
- **Hands-on:** write the async control-flow puzzle, predict the output, then verify.

### `P1-W05-M5` — DOM, events & talking to an API
- Micro-lessons: (a) DOM tree & selection; (b) creating/updating nodes; (c) events, bubbling, delegation; (d) `fetch` + JSON; (e) loading/error/empty states; (f) CORS
- **L1 Ground:** a button that fetches and renders a list.
- **L2 Build:** event delegation for dynamic lists, debounce/throttle, optimistic UI, rendering all four states (loading/empty/error/success), the CORS preflight explained properly, XSS-safe rendering (`textContent` not `innerHTML`).
- **L3 Edge:** reflow costs and batching DOM writes measured on 10k rows; virtualized lists; why frameworks exist (and what they cost); CSP headers.
- **Hands-on:** render 50,000 rows without freezing the tab; measure before/after with the Performance panel.

### `LAB-P1-W05` — **Static frontend against a public API**
- `basic`: fetch and render a list with loading + error states.
- `standard`: responsive, accessible SPA-ish page — search with debounce, pagination, dark mode, all four UI states, no framework, Lighthouse ≥ 90 across the board.
- `hard`: add offline caching, request cancellation on rapid typing, and a virtualized list for 50k items.
- **Ship it:** deploy free (GitHub Pages/Netlify) and link it.

---

## T-P1-W06 — Week 6: REST APIs with FastAPI & Pydantic

**Week outcome:** learner designs and ships a validated, documented, secured, tested async API — the backbone every later phase deploys.

### `P1-W06-M1` — REST design & API contracts
- Micro-lessons: (a) resources & URL design; (b) methods → semantics; (c) status codes that mean something; (d) pagination, filtering, sorting; (e) versioning; (f) OpenAPI
- **L1 Ground:** design the URL/method/status table for a to-do API before writing code.
- **L2 Build:** consistent error envelope, cursor vs offset pagination (and why cursor wins at scale), partial updates (`PATCH`), idempotency keys for POST, API versioning strategies, contract-first with OpenAPI.
- **L3 Edge:** REST vs GraphQL vs gRPC decision framework with latency/payload numbers; HATEOAS reality check; backward-compatibility rules and how you break clients.
- **Hands-on:** review a deliberately bad API spec and produce a corrected one with justifications.

### `P1-W06-M2` — FastAPI fundamentals
- Micro-lessons: (a) app, routers, path/query params; (b) request bodies & response models; (c) dependency injection; (d) async endpoints; (e) background tasks; (f) middleware
- **L1 Ground:** three endpoints, auto-docs at `/docs`, tested in the browser.
- **L2 Build:** `APIRouter` structure for a real project layout, `Depends` for DB sessions/auth/config, `response_model` + `exclude_unset`, lifespan events, middleware for request IDs and timing, sync-vs-async endpoint choice (and the threadpool trap).
- **L3 Edge:** Starlette/ASGI underneath, ASGI vs WSGI, how DI resolution and caching works, `--workers` vs event loop concurrency, uvicorn/gunicorn tuning with a measured throughput table.
- **Hands-on:** load-test the same endpoint as sync-def vs async-def under a blocking call; explain the collapse.

### `P1-W06-M3` — Pydantic v2: validation as a contract
- Micro-lessons: (a) models & field types; (b) validators; (c) nested & generic models; (d) serialization aliases; (e) settings management; (f) error shaping
- **L1 Ground:** reject bad input with a clear message, without a single `if`.
- **L2 Build:** `field_validator`/`model_validator`, strict vs lax coercion, custom types, `BaseSettings` for 12-factor config, translating validation errors into a stable client-facing error format.
- **L3 Edge:** `pydantic-core` in Rust and its measured speed vs v1; validation cost on hot paths; JSON Schema generation — the same mechanism you'll use in Week 26 for LLM structured output and in Week 29 for tool schemas.
- **Hands-on:** benchmark validation of 100k payloads; then generate the JSON Schema and hand it to an LLM as a tool definition (forward link to Phase 4).

### `P1-W06-M4` — Security, auth & hardening
- Micro-lessons: (a) authN vs authZ; (b) password hashing; (c) JWT & sessions; (d) OAuth2 flows conceptually; (e) CORS, CSRF, rate limiting; (f) secrets management
- **L1 Ground:** add login with hashed passwords and a protected route.
- **L2 Build:** `argon2`/`bcrypt` correctly, access + refresh tokens, token expiry/revocation, scopes & role checks as dependencies, CORS configured tightly, rate limiting, input size limits, never logging secrets.
- **L3 Edge:** JWT footguns (`alg:none`, key confusion, no revocation), timing attacks and constant-time compare, OWASP API Top 10 walked through with an exploit demo on a deliberately vulnerable version of the app.
- **Hands-on:** attack the provided vulnerable API (IDOR, mass assignment, JWT tamper), then patch each hole and prove it with a test.

### `P1-W06-M5` — Testing, docs & deployment
- Micro-lessons: (a) `TestClient`/`httpx` async tests; (b) fixtures & test DBs; (c) mocking external calls; (d) `gunicorn`+`uvicorn` workers; (e) health checks, config, logging
- **L1 Ground:** write 5 endpoint tests that run in under a second.
- **L2 Build:** test pyramid for APIs, dependency overrides, transactional test isolation, contract tests from OpenAPI, `/healthz` + readiness vs liveness, 12-factor config, structured request logging with correlation IDs.
- **L3 Edge:** performance testing with `locust`/`k6` — find the knee of the throughput curve; connection-pool sizing math; graceful shutdown & in-flight request draining (matters again in Week 24 K8s).
- **Hands-on:** produce a load-test report: RPS vs p50/p95/p99, identify the bottleneck, fix one thing, re-measure.

### `LAB-P1-W06` — **"Resume Tailor" full-stack service**
- `basic`: POST resume text + job description → returns a formatted markdown response (rule-based, no LLM yet); Week-5 frontend wired up.
- `standard`: full FastAPI service — Pydantic request/response models, file upload with size/type limits, auth, rate limiting, structured errors, 25+ tests, OpenAPI docs, async I/O, load-test report.
- `hard`: add idempotency keys, background job processing with status polling, and a p95 < 200 ms target under 50 concurrent users.
- **Ship it:** deployed publicly (Fly.io/Render free tier) with a README architecture diagram. This service is upgraded with an LLM in Week 26 and instrumented in Week 32 — keep it.

---

## T-P1-W07 — Week 7: Relational Theory, Modelling & SQL

**Week outcome:** learner can model a non-trivial domain in normalized form and write the analytical SQL that most "data" jobs actually require.

### `P1-W07-M1` — Relational model & normalization
- Micro-lessons: (a) relations, keys, constraints; (b) functional dependencies; (c) 1NF/2NF/3NF/BCNF; (d) when to denormalize; (e) relational algebra ↔ SQL
- **L1 Ground:** take one messy spreadsheet and normalize it step by step, drawing the tables at each stage.
- **L2 Build:** primary/foreign/unique/check constraints as correctness guarantees, surrogate vs natural keys, nullable-column design, deliberate denormalization for read paths with the cost stated.
- **L3 Edge:** BCNF vs 3NF anomalies with a concrete counterexample; how the optimizer uses constraints to rewrite queries; schema design for OLTP vs OLAP (forward link to Week 15).
- **Hands-on:** given an un-normalized 30-column table, produce a 3NF schema + migration SQL + proof that no data is lost.

### `P1-W07-M2` — ER modelling & schema design
- Micro-lessons: (a) entities, relationships, cardinality; (b) 1:1 / 1:N / M:N and junction tables; (c) inheritance patterns; (d) soft deletes, audit columns, temporal data; (e) enums, JSONB, arrays
- **L1 Ground:** draw the ER diagram for an e-commerce store, then generate DDL from it.
- **L2 Build:** modelling money (never floats), timestamps with time zones, status state machines, `JSONB` — when it's right and when it's laziness, migration discipline.
- **L3 Edge:** schema evolution without downtime (expand/contract pattern), multi-tenancy models (row / schema / database) compared, partitioning strategy for a 500M-row orders table.
- **Hands-on:** write the zero-downtime migration plan for renaming a heavily-used column on a live table.

### `P1-W07-M3` — SQL I: querying
- Micro-lessons: (a) SELECT/WHERE/ORDER/LIMIT; (b) JOIN types with real Venn/row-level intuition; (c) GROUP BY & aggregates; (d) HAVING vs WHERE; (e) subqueries & CTEs; (f) set operations
- **L1 Ground:** 25 progressively harder queries on a seeded database, answers included.
- **L2 Build:** join semantics with duplicates and NULLs (the classic silent bug), correlated subqueries vs joins, readable CTE-based composition, `EXISTS` vs `IN` vs `JOIN`.
- **L3 Edge:** how the planner turns your query into a tree; join algorithms (nested loop / hash / merge) and when each is chosen; reading `EXPLAIN ANALYZE` line by line.
- **Hands-on:** rewrite 5 slow queries; show the plan before and after with timings.

### `P1-W07-M4` — SQL II: analytical SQL
- Micro-lessons: (a) window functions; (b) `RANK`/`ROW_NUMBER`/`LAG`/`LEAD`; (c) running totals & moving averages; (d) recursive CTEs; (e) pivoting; (f) date/time bucketing
- **L1 Ground:** "top 3 products per category" solved with a window function.
- **L2 Build:** frames (`ROWS` vs `RANGE`), cohort/retention analysis, funnel analysis, sessionization, deduplication with `ROW_NUMBER`, gaps-and-islands.
- **L3 Edge:** window-function execution cost, sort avoidance via indexes, when to push work to the DB vs pull into Pandas (with measured crossover on 10M rows).
- **Hands-on:** produce a monthly cohort-retention matrix in a single query.

### `P1-W07-M5` — Postgres in practice
- Micro-lessons: (a) psql & pgAdmin; (b) data types & extensions; (c) roles & permissions; (d) backup/restore; (e) `EXPLAIN` basics; (f) seeding & fixtures
- **L1 Ground:** install Postgres via Docker, load a sample dataset, run your first query.
- **L2 Build:** `psql` productivity, `COPY` for bulk load (vs 100k INSERTs — measure it), least-privilege roles for an app user, `pg_dump`/restore drills, connection basics.
- **L3 Edge:** MVCC and where dead tuples come from, autovacuum tuning, bloat detection, `pg_stat_statements` to find the top 5 costly queries on a live system.
- **Hands-on:** deliberately bloat a table, detect it with catalog queries, and reclaim the space.

### `LAB-P1-W07` — **E-commerce schema & analytics suite**
- `basic`: complete a partial schema and write 15 given queries.
- `standard`: design the full normalized schema (users, products, inventory, carts, orders, payments, refunds, reviews), seed 1M rows, write 20 analytical queries including cohort retention and top-N-per-group, all with `EXPLAIN ANALYZE` evidence.
- `hard`: hit stated latency targets on 10M rows using indexing and query rewrites; document every index with the query it serves and its write-cost.
- **Ship it:** repo with `schema.sql`, `seed.py`, `queries/`, and a performance write-up.

---

## T-P1-W08 — Week 8: Transactions, Indexing & SQLAlchemy

**Week outcome:** learner can guarantee correctness under concurrency and make an application's data layer fast and safe. This is the week that separates "it works on my laptop" from production.

### `P1-W08-M1` — Transactions & ACID for real
- Micro-lessons: (a) ACID defined precisely; (b) `BEGIN`/`COMMIT`/`ROLLBACK`; (c) savepoints; (d) transaction scope in application code; (e) error handling & retries
- **L1 Ground:** the bank-transfer example — break it mid-way, watch money vanish, then wrap it in a transaction.
- **L2 Build:** transaction boundaries in a web request, keeping transactions short, avoiding external calls inside a transaction, retry-on-serialization-failure, unit-of-work pattern.
- **L3 Edge:** how WAL gives you durability; `fsync` and the durability/performance dial (`synchronous_commit`); two-phase commit and why distributed transactions are usually the wrong answer; the outbox pattern instead.
- **Hands-on:** kill the database process mid-transaction and prove recovery leaves no partial write.

### `P1-W08-M2` — Isolation levels & concurrency anomalies
- Micro-lessons: (a) dirty read, non-repeatable read, phantom; (b) Read Committed / Repeatable Read / Serializable; (c) lost update; (d) write skew; (e) pessimistic vs optimistic locking
- **L1 Ground:** run two `psql` sessions side by side and *see* each anomaly happen.
- **L2 Build:** `SELECT … FOR UPDATE` vs optimistic version columns, `SERIALIZABLE` + retry loop, choosing an isolation level per use case, the classic inventory oversell bug.
- **L3 Edge:** Postgres MVCC snapshots & SSI implementation, deadlock detection and how to read the log, measured throughput cost of `SERIALIZABLE` vs `READ COMMITTED` under contention.
- **Hands-on:** write a concurrency test with 200 parallel buyers for 10 items; prove exactly 10 sell — under every isolation strategy, with a throughput comparison.

### `P1-W08-M3` — Indexing & query performance
- Micro-lessons: (a) what an index is; (b) B-Tree structure; (c) composite indexes & column order; (d) covering/partial/expression indexes; (e) GIN/GiST/BRIN/HNSW overview; (f) index maintenance cost
- **L1 Ground:** run one query on 1M rows without an index, add the index, re-measure. Feel the 1000×.
- **L2 Build:** left-most prefix rule, selectivity & cardinality, why the planner ignores your index, index-only scans, partial indexes for soft-deleted rows, write amplification.
- **L3 Edge:** B-Tree page splits & fill factor; when a sequential scan is genuinely faster; GIN for full-text (used again in Week 28 BM25) and HNSW for vectors (Week 27) — same concept, different distance function; index bloat and `REINDEX CONCURRENTLY`.
- **Hands-on:** given 10 queries, propose the minimum index set; justify each and measure the insert-throughput penalty.

### `P1-W08-M4` — SQLAlchemy 2.0 & the ORM boundary
- Micro-lessons: (a) Core vs ORM; (b) declarative models & relationships; (c) sessions & identity map; (d) lazy vs eager loading; (e) Alembic migrations; (f) async SQLAlchemy with FastAPI
- **L1 Ground:** map the Week-7 schema to models and do CRUD.
- **L2 Build:** relationship loading strategies (`selectinload`/`joinedload`), killing N+1 queries (with the SQL log as proof), session lifecycle per request via `Depends`, Alembic autogenerate + review, dropping to raw SQL when the ORM is the wrong tool.
- **L3 Edge:** the identity map & unit of work internals, flush ordering, bulk operations vs ORM overhead measured at 100k rows, connection pool sizing (`pool_size`, `max_overflow`) and pool exhaustion under load.
- **Hands-on:** find and fix 3 N+1 problems in a provided codebase; show query counts before/after.

### `P1-W08-M5` — Putting it together: a correct, fast data layer
- Micro-lessons: (a) repository pattern; (b) testing with transactional rollback; (c) seeding & factories; (d) observability of queries; (e) caching layers and invalidation
- **L1 Ground:** wrap DB access behind a repository interface and swap it in tests.
- **L2 Build:** test isolation via nested transactions, factory-generated fixtures, slow-query logging, read replicas conceptually, cache-aside with TTL and the invalidation trap.
- **L3 Edge:** connection pooling at scale (PgBouncer modes), cache stampede + request coalescing (this exact pattern returns as semantic caching in Week 28), consistency vs staleness trade-offs.
- **Hands-on:** add a cache in front of the hottest query; measure hit rate, latency, and demonstrate a stale-read scenario, then fix it.

### `LAB-P1-W08` — **Concurrency-safe checkout service**
- `basic`: transactional checkout endpoint passing provided single-user tests.
- `standard`: FastAPI + async SQLAlchemy checkout — payment verification and inventory decrement in one transaction, optimistic locking, idempotency keys, Alembic migrations, and a concurrency test suite proving zero oversells with 200 concurrent buyers.
- `hard`: sustain a target RPS with p95 < 150 ms under contention; deliver a written comparison of pessimistic vs optimistic vs serializable strategies with measured throughput, plus a deadlock reproduction and its fix.
- **Ship it:** repo + `CONCURRENCY.md` explaining the chosen strategy — this is a genuinely strong interview artifact for both personas.

---

## Phase 1 exit checkpoint (gate to Phase 2)

The learner must, unaided and in one sitting:
1. Explain what happens from `malloc` to a Python object to an HTTP response.
2. Ship a small FastAPI + Postgres feature with tests, migrations and an index, from a written ticket.
3. Prove correctness under concurrent load.
4. Present a 5-minute walkthrough of their Week-8 repo, answering "why" at each layer.

**Portfolio after Phase 1:** 8 public repos, 1 deployed frontend, 1 deployed API.
