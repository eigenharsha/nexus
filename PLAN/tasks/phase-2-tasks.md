# Phase 2 — Granular Task Breakdown (Weeks 9–16)
**Goal:** see through every abstraction below your code (gates → CPU → sockets), acquire the math that ML is actually made of, master DSA, and build automated data pipelines.

---

## T-P2-W09 — Week 9: Digital Logic → CPU (Nand2Tetris Part I)

**Week outcome:** learner has built a working 16-bit ALU and register file from NAND gates and can explain how `a + b` becomes electricity.

### `P2-W09-M1` — Boolean algebra & logic gates
- Micro-lessons: (a) truth tables; (b) AND/OR/NOT/NAND/NOR/XOR; (c) NAND completeness; (d) De Morgan's laws; (e) canonical forms & simplification
- **L1 Ground:** build AND, OR, NOT from NAND in the simulator; verify each truth table.
- **L2 Build:** expression simplification (Karnaugh maps), gate count as a cost function, multi-bit versions, buses.
- **L3 Edge:** propagation delay & the critical path; transistor-level CMOS view of a NAND; why NAND is the cheapest primitive in silicon; power vs speed.
- **Hands-on:** implement `Not`, `And`, `Or`, `Xor`, `Mux`, `DMux`, and their 16-bit/multi-way variants; minimize gate count and report it.

### `P2-W09-M2` — Combinational arithmetic
- Micro-lessons: (a) half adder; (b) full adder; (c) ripple-carry 16-bit adder; (d) incrementer; (e) two's-complement negation
- **L1 Ground:** add two 4-bit numbers by hand through the gate diagram.
- **L2 Build:** compose adders into `Add16`, handle overflow, build `Inc16`.
- **L3 Edge:** ripple-carry delay is O(n) — build/analyze a carry-lookahead adder and compare critical-path depth; this is why CPU clock speeds plateaued.
- **Hands-on:** measure (count) gate depth of ripple vs lookahead for 16, 32, 64 bits; plot it.

### `P2-W09-M3` — The ALU
- Micro-lessons: (a) control bits as a mini instruction set; (b) pre-setting inputs; (c) the operation table; (d) status outputs (`zr`, `ng`)
- **L1 Ground:** walk the 6 control bits and trace one operation end to end.
- **L2 Build:** implement the full Hack ALU passing all provided tests; explain how 6 bits express 18 functions.
- **L3 Edge:** compare with a real ISA's ALU (RISC-V `ADD`/`SUB`/`SLT`); flags and how they drive branches; why flags create pipeline hazards.
- **Hands-on:** **the 16-bit ALU** — the week's centerpiece.

### `P2-W09-M4` — Sequential logic, memory & clock
- Micro-lessons: (a) feedback & the clock; (b) D flip-flop; (c) registers; (d) RAM hierarchy; (e) program counter
- **L1 Ground:** why a circuit needs a clock to "remember".
- **L2 Build:** `Bit` → `Register` → `RAM8` → `RAM64` → `RAM16K`, `PC` with load/inc/reset.
- **L3 Edge:** SRAM vs DRAM (refresh, density, cost per bit); the memory hierarchy L1/L2/L3/DRAM/SSD with real latency numbers (ns → ms) — the table you will use to reason about performance for the rest of your career; cache lines and locality.
- **Hands-on:** write a C program demonstrating cache-line effects (row-major vs column-major traversal); explain the 5–10× gap using the numbers from this lesson.

### `P2-W09-M5` — From CPU to program
- Micro-lessons: (a) fetch-decode-execute; (b) instruction encoding; (c) registers vs memory; (d) machine code → assembly → high-level; (e) the modern CPU (pipeline, superscalar, speculation)
- **L1 Ground:** hand-execute 5 instructions on paper.
- **L2 Build:** write a short Hack assembly program; map a C `for` loop to its assembly.
- **L3 Edge:** pipelining, branch prediction, out-of-order execution, SIMD (AVX/NEON) — and the direct line from SIMD to GPU tensor cores in Phase 3; Spectre in one paragraph.
- **Hands-on:** show a 3× speedup on a numeric loop purely by making it branch-predictable and vectorizable; verify with `perf`/Instruments.

### `LAB-P2-W09` — **Build the Hack computer's ALU & memory**
- `basic`: gates + adders with provided test scripts.
- `standard`: full ALU + register file + RAM16K + PC, all tests green, gate-count report.
- `hard`: carry-lookahead variant + a written critical-path analysis; plus the C cache-locality benchmark with measured numbers.
- **Ship it:** repo with HDL files, test output, and a "how a computer adds" explainer post.

---

## T-P2-W10 — Week 10: Networking & Raw Sockets

**Week outcome:** learner can build a concurrent network server from raw sockets and diagnose network problems with packet-level evidence.

### `P2-W10-M1` — The network stack
- Micro-lessons: (a) layered model; (b) Ethernet/IP/TCP/HTTP as nesting dolls; (c) IP addressing, subnets, NAT; (d) DNS; (e) ports & sockets
- **L1 Ground:** follow one packet from your laptop to a server and back, layer by layer.
- **L2 Build:** `ping`/`traceroute`/`dig`/`netstat`/`ss` diagnostics, MTU & fragmentation, NAT's consequences for peer-to-peer, private vs public addressing.
- **L3 Edge:** open a Wireshark capture and read the actual bytes of each header; DNS resolution path & caching layers; anycast; how a CDN changes the picture.
- **Hands-on:** capture and annotate a full TLS-terminated HTTP request at the byte level.

### `P2-W10-M2` — TCP vs UDP
- Micro-lessons: (a) three-way handshake; (b) sequence numbers, ACKs, retransmission; (c) flow control & windows; (d) congestion control; (e) UDP and when to use it; (f) connection teardown & TIME_WAIT
- **L1 Ground:** watch a handshake in Wireshark; identify SYN, SYN-ACK, ACK.
- **L2 Build:** why TCP streams have no message boundaries (the #1 beginner bug), Nagle's algorithm & `TCP_NODELAY`, keep-alives, socket timeouts, `SO_REUSEADDR`.
- **L3 Edge:** congestion-control algorithms (Reno vs CUBIC vs BBR) and bandwidth-delay product math; head-of-line blocking motivating QUIC/HTTP-3; measuring throughput vs latency with `iperf3` under simulated loss (`tc netem`).
- **Hands-on:** inject 2% packet loss and 100 ms latency; measure throughput collapse and explain it with the BDP formula.

### `P2-W10-M3` — Socket programming
- Micro-lessons: (a) socket lifecycle (`socket`/`bind`/`listen`/`accept`/`connect`); (b) send/recv and partial reads; (c) framing protocols; (d) blocking vs non-blocking; (e) `select`/`epoll`/`kqueue`
- **L1 Ground:** an echo server + client in 30 lines.
- **L2 Build:** length-prefixed framing, robust `recv_exactly`, graceful shutdown, error handling for `ECONNRESET`/`EPIPE`, backlog sizing.
- **L3 Edge:** the C10K problem; thread-per-connection vs event-driven measured side by side; zero-copy (`sendfile`), kernel buffers, and where `asyncio` (Week 4) sits on this map.
- **Hands-on:** implement the same server three ways (threads, `selectors`, `asyncio`) and benchmark to 1,000 concurrent connections.

### `P2-W10-M4` — Designing an application protocol
- Micro-lessons: (a) text vs binary protocols; (b) message framing & schemas; (c) request/response vs streaming vs pub-sub; (d) versioning; (e) heartbeats & reconnection
- **L1 Ground:** design a 5-command chat protocol on paper, then implement two commands.
- **L2 Build:** a documented wire protocol with versioning, heartbeats, reconnect with backoff, and back-pressure; serialization choices (JSON vs MsgPack vs Protobuf) with size/speed numbers.
- **L3 Edge:** protocol evolution without breaking old clients; WebSockets & SSE compared; how gRPC frames over HTTP/2 — and the direct relevance to MCP transports in Week 30.
- **Hands-on:** benchmark JSON vs MsgPack vs Protobuf on 100k messages: bytes on wire, encode/decode time.

### `P2-W10-M5` — Network security & operations basics
- Micro-lessons: (a) TLS: what it guarantees; (b) certificates & trust chains; (c) firewalls & ports; (d) common attacks (MITM, spoofing, amplification); (e) observability of network issues
- **L1 Ground:** generate a self-signed cert and serve HTTPS locally.
- **L2 Build:** TLS termination patterns, cert rotation, `openssl s_client` debugging, verifying certificates properly in clients (the "verify=False" disaster), timeouts as a security control.
- **L3 Edge:** TLS 1.3 handshake reduction and 0-RTT replay risk; mTLS for service-to-service; how a reverse proxy/load balancer changes client IP, timeouts and keep-alives — all of which resurface in Week 24 (K8s).
- **Hands-on:** intercept your own traffic with a local MITM proxy; then make the client correctly refuse it.

### `LAB-P2-W10` — **Multi-threaded TCP chat server (raw sockets)**
- `basic`: echo server + single client.
- `standard`: multi-room chat — length-prefixed protocol, concurrent clients, nicknames, join/leave, broadcast, graceful disconnect handling, protocol spec document, and a Wireshark trace proving framing works.
- `hard`: 1,000 concurrent clients on an event loop with back-pressure and heartbeats; report memory per connection and p99 message latency; survive `tc netem` loss.
- **Ship it:** repo with `PROTOCOL.md`, benchmark report, and packet captures.

---

## T-P2-W11 — Week 11: Linear Algebra & Calculus for AI

**Week outcome:** learner can read the math in an ML paper and implement it. Every concept is taught *as the thing it becomes* later (embeddings, attention, gradients).

### `P2-W11-M1` — Vectors & vector spaces
- Micro-lessons: (a) vectors as data points and as directions; (b) norms (L1/L2/L∞); (c) dot product, angle, projection; (d) cosine similarity; (e) basis, span, independence; (f) high-dimensional geometry
- **L1 Ground:** 2-D drawings for everything; compute a dot product by hand; "similar documents = small angle".
- **L2 Build:** implement norms/dot/projection in NumPy; normalize embeddings; cosine vs Euclidean and when each is right (exact setup used in Week 27 retrieval).
- **L3 Edge:** the curse of dimensionality — empirically show that in 1000-D, random vectors are nearly orthogonal and distances concentrate; the direct consequence for ANN search and why HNSW exists.
- **Hands-on:** simulate distance concentration across d = 2 … 4096 and plot it; write the implication for vector search in your own words.

### `P2-W11-M2` — Matrices & linear transformations
- Micro-lessons: (a) matrices as transformations; (b) matrix multiplication (three interpretations); (c) transpose, inverse, rank, determinant; (d) systems of equations; (e) special matrices
- **L1 Ground:** watch a matrix rotate/scale/shear a shape; multiply 2×2 by hand.
- **L2 Build:** implement matmul from scratch, then vectorize with NumPy and measure the gap; broadcasting rules; shape-debugging discipline (the #1 source of deep-learning errors).
- **L3 Edge:** memory layout, cache blocking, and why BLAS is 100× your loop — implement a tiled matmul and measure GFLOPS; batched matmul as the shape of every Transformer layer; `float32` vs `float16` numerics.
- **Hands-on:** naive → vectorized → tiled matmul benchmark with a GFLOPS table and a written explanation of the gap.

### `P2-W11-M3` — Eigen-decomposition, SVD & PCA
- Micro-lessons: (a) eigenvalues/eigenvectors intuitively; (b) diagonalization; (c) SVD; (d) PCA as a use of SVD; (e) low-rank approximation
- **L1 Ground:** the "directions that don't change" picture; PCA on 2-D data plotted.
- **L2 Build:** implement power iteration for the top eigenvector; PCA via SVD on a real dataset; explained-variance selection; whitening.
- **L3 Edge:** low-rank approximation of an image (compression vs rank plot) — **this is exactly LoRA** (Week 26): show the parameter-count math for rank-8 adapters on a 4096×4096 matrix; condition number and numerical stability.
- **Hands-on:** compress an image at ranks 5/20/50/200; then compute LoRA parameter savings for a real model and state the compression ratio.

### `P2-W11-M4` — Calculus & the chain rule
- Micro-lessons: (a) derivatives as rate of change; (b) partial derivatives; (c) gradient & directional derivative; (d) chain rule; (e) Jacobian & Hessian; (f) numerical vs analytic differentiation
- **L1 Ground:** slope by hand; finite-difference derivative in 5 lines of Python.
- **L2 Build:** gradients of the functions you'll actually differentiate (MSE, cross-entropy, sigmoid, softmax, ReLU) derived on paper and verified numerically.
- **L3 Edge:** forward vs reverse-mode autodiff and why reverse mode wins when outputs ≪ inputs; build a 100-line reverse-mode autodiff engine (direct precursor to Week 21); numerical precision of finite differences.
- **Hands-on:** `gradcheck` — verify your analytic gradients against numerical ones to 1e-7.

### `P2-W11-M5` — Optimization
- Micro-lessons: (a) minima, convexity; (b) gradient descent & learning rate; (c) SGD & mini-batches; (d) momentum, RMSProp, Adam; (e) learning-rate schedules; (f) constrained/regularized objectives
- **L1 Ground:** roll a ball down a 1-D curve; watch divergence when the learning rate is too big.
- **L2 Build:** implement GD, SGD, momentum, Adam from scratch on a 2-D loss surface; visualize trajectories; batch-size effects.
- **L3 Edge:** convergence conditions, saddle points in high dimensions, sharp vs flat minima and generalization, warmup + cosine decay as used in LLM training, gradient clipping; why Adam's memory cost = 2× params (the number that drives Week 26 QLoRA math).
- **Hands-on:** race 5 optimizers on Rosenbrock and on a noisy quadratic; produce the trajectory plots and a recommendation.

### `LAB-P2-W11` — **`nanomath`: a from-scratch math library**
- `basic`: dot product, matrix transpose, matmul with tests.
- `standard`: vectors/matrices, norms, matmul, inverse (Gauss-Jordan), power iteration for eigenvalues, SVD-based PCA, numerical gradient, and a 100-line reverse-mode autodiff engine — all with tests against NumPy to 1e-6.
- `hard`: tiled matmul beating naive by ≥10×; autodiff supporting a 2-layer network trained end to end; benchmark report.
- **Ship it:** repo + a written "math for ML" cheat sheet the learner authored themselves.

---

## T-P2-W12 — Week 12: Probability, Statistics & Experimentation

**Week outcome:** learner can reason under uncertainty, run and interpret an A/B test, and avoid the statistical errors that ruin ML projects.

### `P2-W12-M1` — Probability foundations
- Micro-lessons: (a) sample spaces & events; (b) conditional probability; (c) independence; (d) Bayes' theorem; (e) random variables; (f) expectation & variance
- **L1 Ground:** dice and coins; the medical-test paradox (99% accurate test, rare disease) worked slowly.
- **L2 Build:** Bayes in code (spam filter from scratch), law of total probability, simulation as a way to check any probability answer.
- **L3 Edge:** base-rate neglect in production ML — precision at 0.1% prevalence (sets up Week 20 fraud detection); the exact same arithmetic applied to a model's confusion matrix.
- **Hands-on:** build a naive Bayes spam classifier from scratch; then compute its real-world precision at three different base rates.

### `P2-W12-M2` — Distributions
- Micro-lessons: (a) PMF/PDF/CDF; (b) Bernoulli/Binomial/Poisson; (c) Normal; (d) Exponential & heavy tails; (e) sampling; (f) Law of Large Numbers & CLT
- **L1 Ground:** simulate each distribution and look at the histogram.
- **L2 Build:** picking the right distribution for a real quantity; QQ plots; log-normal latency data and why "average latency" lies; CLT demonstrated by simulation.
- **L3 Edge:** heavy tails in systems (latency, file sizes, token counts): why p99 ≫ mean, and how to size capacity; sampling bias in training data.
- **Hands-on:** analyze a real latency dataset; report mean/p50/p95/p99, show the histogram, and explain why an SLA on the mean is meaningless.

### `P2-W12-M3` — Statistical inference
- Micro-lessons: (a) population vs sample; (b) estimators, bias, variance; (c) confidence intervals; (d) hypothesis testing & p-values; (e) t-test, chi-square, Mann-Whitney; (f) bootstrap
- **L1 Ground:** estimate a mean from a sample and see the interval shrink with n.
- **L2 Build:** choosing the right test, one- vs two-tailed, effect size vs significance, bootstrap CIs for anything (including model metrics).
- **L3 Edge:** what a p-value is *not*; multiple-comparison correction; p-hacking; power analysis; how this maps directly to comparing two model versions or two prompts (Week 33 evals).
- **Hands-on:** bootstrap a 95% CI around a model's F1 score; decide whether model B is genuinely better than model A.

### `P2-W12-M4` — Experimentation & A/B testing
- Micro-lessons: (a) randomization; (b) metrics: primary, guardrail, proxy; (c) sample-size calculation; (d) running the test; (e) reading the result; (f) common pitfalls
- **L1 Ground:** design an A/B test for a button color, end to end.
- **L2 Build:** MDE and sample-size math, sequential-testing dangers, novelty effects, SRM checks, segmentation traps, decision rules written before launch.
- **L3 Edge:** CUPED variance reduction, network effects/interference, switchback tests, online-vs-offline metric divergence — this is exactly the eval problem in Week 33.
- **Hands-on:** given a results dataset with a subtle SRM problem, produce the correct (negative) conclusion and defend it.

### `P2-W12-M5` — Exploratory statistics & correlation
- Micro-lessons: (a) descriptive statistics; (b) correlation vs causation; (c) Pearson vs Spearman; (d) Simpson's paradox; (e) confounders; (f) causal thinking basics
- **L1 Ground:** compute correlations and be shown a spurious one.
- **L2 Build:** correlation matrices for feature selection, multicollinearity, detecting Simpson's paradox by segmenting, DAGs for confounders.
- **L3 Edge:** causal inference primer (potential outcomes, DiD, propensity scores) and when an ML model is answering a causal question it cannot answer.
- **Hands-on:** find a Simpson's-paradox reversal in a provided dataset; write the correct interpretation.

### `LAB-P2-W12` — **A/B test analyzer + Bayes classifier**
- `basic`: compute means, CIs and a t-test on given data.
- `standard`: CLI tool — sample-size calculator, SRM check, primary/guardrail metrics, bootstrap CIs, effect size, and a written decision; plus a from-scratch naive Bayes classifier with evaluation.
- `hard`: add sequential-testing correction and CUPED variance reduction; demonstrate the reduction in required sample size numerically.
- **Ship it:** repo + a one-page "how to read an A/B test" guide.

---

## T-P2-W13 — Week 13: DSA I — Complexity & Linear Structures

**Week outcome:** learner implements the core data structures from scratch, benchmarks them, and can pass a technical screen.

### `P2-W13-M1` — Complexity analysis properly
- Micro-lessons: (a) counting operations; (b) Big-O/Ω/Θ; (c) best/average/worst; (d) amortized analysis; (e) space complexity; (f) recurrence relations & Master theorem
- **L1 Ground:** classify 15 snippets by complexity.
- **L2 Build:** amortized cost of dynamic-array growth (derive the 2× doubling result), recursion tree method, complexity of the operations you use daily.
- **L3 Edge:** where Big-O lies — constants, cache behavior, and the crossover point; measure an O(n) linked list losing to an O(n) array by 10×.
- **Hands-on:** benchmark 6 operations across sizes; produce an empirical complexity table and reconcile it with theory.

### `P2-W13-M2` — Arrays, strings & two-pointer techniques
- Micro-lessons: (a) dynamic arrays; (b) prefix sums; (c) two pointers; (d) sliding window; (e) string algorithms; (f) in-place manipulation
- **L1 Ground:** reverse an array in place; sum a subarray with prefix sums.
- **L2 Build:** the sliding-window template that solves a whole class of problems; two-pointer patterns; string tokenization performance.
- **L3 Edge:** KMP/Rabin-Karp; why substring search matters for BM25 tokenization (Week 28); Unicode & normalization pitfalls in text pipelines (returns in Week 25 tokenizers).
- **Hands-on:** 6 classic array/string problems, timed.

### `P2-W13-M3` — Linked lists, stacks & queues
- Micro-lessons: (a) singly/doubly linked lists; (b) stack; (c) queue & deque; (d) circular buffers; (e) monotonic stack/queue
- **L1 Ground:** implement a linked list with insert/delete/traverse, drawing pointers each step.
- **L2 Build:** LRU cache from scratch (hash map + doubly linked list) — the exact structure behind every cache you will build later; ring buffer for streaming; monotonic stack for next-greater-element.
- **L3 Edge:** memory locality: array-backed deque vs pointer-chasing list, measured; intrusive lists; lock-free queue overview.
- **Hands-on:** implement an LRU cache with O(1) get/put and prove it with tests + a benchmark.

### `P2-W13-M4` — Hash tables from scratch
- Micro-lessons: (a) hashing & hash functions; (b) collisions; (c) chaining; (d) open addressing; (e) load factor & resizing; (f) sets & multimaps
- **L1 Ground:** hand-trace inserting 5 keys into a table of size 4.
- **L2 Build:** full hash table with chaining, dynamic resize, iteration, and deletion; measure vs `dict`.
- **L3 Edge:** open addressing vs chaining under load-factor sweep (measured); hash quality, clustering, and adversarial collision DoS; consistent hashing for sharding (used again for distributed vector stores).
- **Hands-on:** implement both collision strategies; benchmark across load factors 0.3 → 0.95; plot and explain.

### `P2-W13-M5` — Sorting, searching & problem-solving method
- Micro-lessons: (a) comparison sorts revisited; (b) counting/radix sort; (c) binary search variants & on-answer search; (d) heaps and top-K; (e) how to attack an unseen problem; (f) interview communication
- **L1 Ground:** the 4-step method: restate → examples → brute force → optimize.
- **L2 Build:** binary search on the answer, `heapq` for top-K streaming, `k`-way merge, stability requirements.
- **L3 Edge:** external sorting (revisit Week 1 hard lab), distributed sort, top-K over an unbounded stream with bounded memory (count-min sketch, reservoir sampling) — the practical basis for large-scale retrieval later.
- **Hands-on:** find the top-100 items in a 10M-element stream using ≤1 MB of memory.

### `LAB-P2-W13` — **`pycollections`: structures from scratch + benchmark harness**
- `basic`: hash table with chaining passing provided tests.
- `standard`: hash table (chaining + open addressing), dynamic array, doubly linked list, LRU cache, min-heap — all tested, plus a benchmark harness producing complexity plots.
- `hard`: beat `dict` on a specialized workload (e.g., integer keys, known size) and prove it; add a count-min sketch and measure its error bounds empirically.
- **Ship it:** repo + a written "what I learned about constants vs Big-O" report.

---

## T-P2-W14 — Week 14: DSA II — Trees, Graphs & Dynamic Programming

**Week outcome:** learner can model problems as trees/graphs, apply DP, and solve medium interview problems reliably.

### `P2-W14-M1` — Trees & binary search trees
- Micro-lessons: (a) tree terminology; (b) traversals (DFS pre/in/post, BFS); (c) BST insert/search/delete; (d) balance & rotations; (e) AVL/Red-Black overview; (f) tries
- **L1 Ground:** traverse a tree on paper four ways; build a BST from 7 numbers.
- **L2 Build:** recursive and iterative traversals, BST validation, tree problems template, trie for prefix search/autocomplete.
- **L3 Edge:** why databases use B-Trees, not BSTs — fan-out, node size, and disk pages (connects straight to Week 8 indexing); self-balancing cost; measure degenerate-BST worst case.
- **Hands-on:** build a trie-based autocomplete over 100k words; compare memory & latency with a sorted-array binary search.

### `P2-W14-M2` — Heaps, priority queues & intervals
- Micro-lessons: (a) heap property & array representation; (b) heapify, push, pop; (c) heapsort; (d) priority queues in scheduling; (e) interval problems
- **L1 Ground:** build a min-heap step by step from an array.
- **L2 Build:** implement a heap from scratch; merge k sorted lists; task scheduler; meeting-rooms interval problems.
- **L3 Edge:** d-ary heaps, Fibonacci heap theory vs practice, heap use inside Dijkstra and inside HNSW's candidate queue (Week 27) — the same structure twice.
- **Hands-on:** implement a bounded priority queue and use it for a top-K nearest-neighbor search over 1M vectors (brute force) — timed, as a baseline for Week 27.

### `P2-W14-M3` — Graphs & traversal
- Micro-lessons: (a) representations (adjacency list/matrix); (b) BFS & shortest path on unweighted graphs; (c) DFS, cycles, topological sort; (d) connected components; (e) union-find; (f) bipartite check
- **L1 Ground:** model a friend network; run BFS by hand.
- **L2 Build:** grid problems as graphs (islands, flood fill), topological sort for dependency resolution (this is literally your build system and Week 32's agent graph), union-find with path compression.
- **L3 Edge:** graph representation memory/perf trade-offs at 10M edges; cycle detection in agent workflows and deadlock detection (Week 32); traversal order effects on cache.
- **Hands-on:** detect a cycle in a real dependency graph (e.g., a `package.json` tree) and print the cycle path.

### `P2-W14-M4` — Weighted shortest paths & greedy algorithms
- Micro-lessons: (a) Dijkstra; (b) why Dijkstra fails with negative weights; (c) Bellman-Ford; (d) A*; (e) MST (Kruskal/Prim); (f) greedy correctness
- **L1 Ground:** run Dijkstra by hand on a 6-node graph.
- **L2 Build:** implement Dijkstra with a heap; build a route planner on real city data; when greedy is provably correct.
- **L3 Edge:** A* heuristics and admissibility — and the direct analogy to beam search / best-first planning in LLM agents; bidirectional search; contraction hierarchies at map scale.
- **Hands-on:** route planner over an OpenStreetMap extract; compare Dijkstra vs A* node expansions and runtime.

### `P2-W14-M5` — Dynamic programming
- Micro-lessons: (a) overlapping subproblems & optimal substructure; (b) memoization → tabulation; (c) 1-D DP; (d) 2-D grid DP; (e) knapsack family; (f) string DP (edit distance, LCS)
- **L1 Ground:** Fibonacci: naive → memoized → tabulated, with call counts at each stage.
- **L2 Build:** the 5-step DP recipe (state, transition, base, order, answer) applied to 8 problems; space optimization.
- **L3 Edge:** edit distance as the basis of diff tools and of fuzzy retrieval; DP on trees; when DP is exponential anyway; comparing DP to beam search for sequence decoding (Week 25).
- **Hands-on:** implement edit distance with backtracking to output the actual alignment; use it to build a mini `diff`.

### `LAB-P2-W14` — **15 medium problems + route planner**
- `basic`: 8 guided problems with hints and reference solutions.
- `standard`: 15 medium problems (trees, graphs, DP) solved with written complexity analysis for each; plus a Dijkstra route planner CLI on real map data.
- `hard`: A* with a custom heuristic beating Dijkstra by ≥3× on node expansions; a written proof sketch of admissibility.
- **Ship it:** a "problem-solving journal" repo — for each problem: the approach, the failed first idea, and the final complexity. Strong interview prep artifact.

---

## T-P2-W15 — Week 15: Data Engineering — Ingestion & Pipelines

**Week outcome:** learner builds an automated, incremental, schema-evolving pipeline that runs unattended — the skill that most directly and immediately pays off in a working professional's day job.

### `P2-W15-M1` — Data engineering landscape
- Micro-lessons: (a) ETL vs ELT; (b) batch vs streaming; (c) OLTP vs OLAP vs lakehouse; (d) file formats (CSV/JSON/Parquet/Arrow); (e) idempotency & replayability; (f) orchestration overview
- **L1 Ground:** move data from an API to a database once, by hand — then feel why you'd automate it.
- **L2 Build:** choosing batch vs streaming with a decision table; Parquet vs CSV measured (size, read speed, column pruning); designing pipelines to be re-runnable.
- **L3 Edge:** columnar storage internals (row groups, encoding, predicate pushdown) with measured scan reduction; the modern lakehouse table formats (Iceberg/Delta) in one page; data contracts.
- **Hands-on:** convert a 5 GB CSV to Parquet; measure size, full-scan time and single-column-scan time; explain the numbers.

### `P2-W15-M2` — Extracting from APIs
- Micro-lessons: (a) REST clients & auth; (b) pagination patterns (offset, cursor, link header); (c) rate limits & backoff; (d) incremental extraction with watermarks; (e) error handling & resumability; (f) API-to-schema mapping
- **L1 Ground:** pull one page of a public API and save it.
- **L2 Build:** a generic paginator, respecting 429/`Retry-After`, state persistence for incremental runs, partial-failure recovery, structured logging of every run.
- **L3 Edge:** designing for API changes, deduplication semantics (at-least-once vs exactly-once), backfill strategy without re-hammering the source, parallel extraction with a rate budget (reuses Week 4 patterns).
- **Hands-on:** extract 100k records across pages under a rate limit, resume correctly after a forced crash at record 43,000.

### `P2-W15-M3` — Web scraping
- Micro-lessons: (a) HTML parsing with BeautifulSoup; (b) selectors & robust extraction; (c) sessions, headers, cookies; (d) dynamic/JS-rendered pages; (e) politeness, robots.txt, legality/ethics; (f) anti-fragile scrapers
- **L1 Ground:** scrape a static table into a DataFrame.
- **L2 Build:** resilient selectors, retry + caching layer so re-runs don't re-fetch, `robots.txt` and rate-limit compliance, structured extraction into a schema, monitoring for layout changes.
- **L3 Edge:** headless browser only when necessary (cost comparison vs HTTP), parsing performance (`lxml` vs `html.parser` measured), detecting silent breakage, and the legal/ethical boundary written plainly.
- **Hands-on:** build a scraper with a snapshot-test suite so layout changes fail loudly in CI instead of silently producing nulls.

### `P2-W15-M4` — `dlt`: declarative pipelines
- Micro-lessons: (a) sources, resources, pipelines; (b) write dispositions (replace/append/merge); (c) incremental loading & cursors; (d) schema inference & evolution; (e) normalization of nested data; (f) state & destinations
- **L1 Ground:** a 15-line `dlt` pipeline from a REST API into DuckDB.
- **L2 Build:** merge/upsert with primary keys, incremental cursors, handling nested JSON into child tables, schema contracts (`freeze`/`evolve`/`discard`), running the same pipeline into a different destination.
- **L3 Edge:** what `dlt` generates under the hood (staging, normalization, schema hashes); handling breaking upstream schema changes; comparing `dlt` vs hand-rolled vs Airbyte/Fivetran on cost and control; deduplication correctness proofs.
- **Hands-on:** force three upstream schema changes (new field, type change, removed field) and show how each is handled — with the resulting table state.

### `P2-W15-M5` — Storage, warehousing & orchestration
- Micro-lessons: (a) DuckDB as a local warehouse; (b) star schema & dimensional modelling; (c) SCD Type 2; (d) partitioning & file layout; (e) scheduling (cron → Airflow/Dagster/Prefect concepts); (f) data quality tests
- **L1 Ground:** query Parquet files directly with DuckDB, no loading step.
- **L2 Build:** fact/dimension modelling for the ingested data, SCD2 for changing dimensions, partitioned layout, a scheduled run with alerting, data-quality assertions (row counts, null rates, freshness).
- **L3 Edge:** DuckDB's vectorized execution and why it beats Pandas on 10M rows (measured); when you actually need Spark (with the honest threshold); lineage and backfill orchestration; the cost of a bad partition key.
- **Hands-on:** benchmark the same aggregation in Pandas / Polars / DuckDB on 10M rows; report time and peak memory, and pick a default.

### `LAB-P2-W15` — **Incremental financial-records pipeline**
- `basic`: `dlt` pipeline from a provided REST API into DuckDB, full refresh.
- `standard`: scrape + API extract of unstructured financial records → normalized, deduplicated, incrementally merged into DuckDB with schema evolution enabled; scheduled; data-quality checks; run-report artifact; safe to re-run and to resume after a crash.
- `hard`: 5M rows with partitioned Parquet output, SCD2 dimension, backfill script, and a written cost/latency analysis; prove exactly-once semantics for the merge.
- **Ship it:** repo + `PIPELINE.md` with a dataflow diagram. *This is the single most directly job-applicable artifact of Phase 2 for the working professional.*

---

## T-P2-W16 — Week 16: Pandas, EDA & Automated Analysis

**Week outcome:** learner turns raw data into a defensible analysis, automatically — and builds the feature intuition that Phase 3 depends on.

### `P2-W16-M1` — NumPy properly
- Micro-lessons: (a) ndarray, dtype, shape; (b) vectorization; (c) broadcasting; (d) indexing & masking; (e) axis semantics; (f) views vs copies
- **L1 Ground:** replace a Python loop with a vectorized expression and measure the speedup.
- **L2 Build:** broadcasting rules mastered with 10 shape puzzles, boolean masking for filtering, `axis=` intuition that will save you in PyTorch, avoiding accidental copies.
- **L3 Edge:** memory layout (C vs F order), strides, `np.einsum`, when NumPy silently copies your 4 GB array; float precision accumulation error in large sums (and `np.float64` vs `float32` in ML).
- **Hands-on:** shape-debugging drill: 12 broken array operations to diagnose and fix from the error message alone.

### `P2-W16-M2` — Pandas for real work
- Micro-lessons: (a) Series/DataFrame; (b) selection (`loc`/`iloc`); (c) filtering & assignment; (d) groupby-apply-combine; (e) merges & joins; (f) reshaping (pivot/melt); (g) time series & resampling
- **L1 Ground:** load a CSV and answer 10 questions about it.
- **L2 Build:** method chaining for readable pipelines, `groupby.agg` with named aggregations, join validation (`validate=`) to catch fan-out bugs, `SettingWithCopyWarning` explained and eliminated, dtypes & categoricals for memory.
- **L3 Edge:** memory profiling a DataFrame and cutting it 5× with dtypes; Pandas vs Polars vs DuckDB decision guide with measurements; `apply` as a performance trap (measure the 100× penalty); chunked processing for out-of-core data.
- **Hands-on:** take a 3 GB dataset to a working analysis on a 8 GB laptop; document every memory decision.

### `P2-W16-M3` — Data cleaning
- Micro-lessons: (a) missing data mechanisms (MCAR/MAR/MNAR); (b) imputation strategies; (c) duplicates & entity resolution; (d) outliers: detect vs remove vs keep; (e) type/unit/encoding fixes; (f) validation rules
- **L1 Ground:** clean a small messy dataset step by step.
- **L2 Build:** an imputation decision table, `MissingIndicator` as a feature, IQR/z-score/isolation-forest outlier detection compared, deduplication with fuzzy matching, `pandera`/Great-Expectations-style validation.
- **L3 Edge:** how imputation choices leak information across a train/test split (the bug that inflates every beginner's score — set up here, paid off in Week 19); missingness as signal; when to drop rows vs columns, with the bias implications.
- **Hands-on:** show numerically how imputing before splitting inflates test accuracy, then fix it with a pipeline.

### `P2-W16-M4` — Exploratory Data Analysis
- Micro-lessons: (a) the EDA checklist; (b) univariate analysis; (c) bivariate & target relationships; (d) correlation & multicollinearity; (e) segmentation; (f) writing the findings
- **L1 Ground:** run the full checklist on one dataset, guided.
- **L2 Build:** a repeatable EDA function library; target leakage detection during EDA; class-imbalance discovery; distribution shift between train and holdout; documenting hypotheses.
- **L3 Edge:** EDA as hypothesis generation, not decoration; automating profile reports and knowing their blind spots; detecting data drift with statistical tests (returns in Week 34 monitoring).
- **Hands-on:** produce a 2-page EDA memo for a stakeholder — findings, risks, and a recommended modelling approach.

### `P2-W16-M5` — Visualization that communicates
- Micro-lessons: (a) matplotlib model (figure/axes); (b) seaborn statistical plots; (c) choosing the right chart; (d) distributions, relationships, comparisons, composition; (e) annotation & narrative; (f) plot automation
- **L1 Ground:** build 6 chart types on the same dataset.
- **L2 Build:** small multiples, log scales for skewed data, avoiding misleading axes, colorblind-safe palettes, publishing plots from a script (never a notebook screenshot).
- **L3 Edge:** perceptual accuracy of encodings, plotting 10M points honestly (datashading/binning), automated report generation into HTML/PDF.
- **Hands-on:** rebuild a deliberately misleading chart into an honest one and write the critique.

### `LAB-P2-W16` — **Automated EDA dashboard**
- `basic`: guided notebook producing 8 required plots on a provided dataset.
- `standard`: a CLI tool — point it at any CSV/Parquet and get an HTML report: schema, missingness, distributions, outliers, correlations, target relationships, leakage warnings, and a written summary; tested on 3 different datasets.
- `hard`: handle a 10M-row file within a fixed memory budget; add drift comparison between two datasets with statistical tests; sub-60-second runtime.
- **Ship it:** publishable tool + report artifacts. Pairs with the Week-15 pipeline into one "raw source → analysis" system.

---

## Phase 2 exit checkpoint (gate to Phase 3)

1. Explain the path from a NAND gate to a `numpy` dot product, naming every layer.
2. Given a slow query/loop/pipeline, find the bottleneck with evidence and fix it.
3. Derive a gradient by hand and verify it numerically.
4. Build an incremental pipeline from an unfamiliar API in under 3 hours.
5. Solve two unseen medium DSA problems with correct complexity analysis, thinking aloud.

**Portfolio after Phase 2:** ALU repo, chat server, `nanomath`, DSA journal, data pipeline, EDA tool.
