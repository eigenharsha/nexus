# Nexus — Master Task Board (Level 0–2)

Level 0 = program-wide infrastructure · Level 1 = phase · Level 2 = week.
Level 3 (module) and Level 4 (lesson/lab) live in `PLAN/tasks/phase-N-tasks.md`.

**Status legend:** `TODO` · `WIP` · `REVIEW` · `DONE`

---

## Level 0 — Program infrastructure (must land before Week 1 content)

| ID | Task | Output | Depends on | Est. | Status |
|---|---|---|---|---|---|
| T-000 | Lock content spec + 3-layer definition | `PLAN/00-content-spec.md` | — | done | DONE |
| T-001 | Lock master + granular task board | `PLAN/01-master-board.md`, `PLAN/tasks/*` | T-000 | done | DONE |
| T-002 | Repo scaffold: `content/`, `labs/`, `decks/`, `assets/`, `tests/` | directory tree + README | T-001 | 1 h | TODO |
| T-003 | Lesson template file + `new-lesson.sh` generator | `templates/lesson.md`, script | T-000 | 1 h | TODO |
| T-004 | Lab template (starter/solution/basic/standard/hard + `make verify`) | `templates/lab/` | T-000 | 2 h | TODO |
| T-005 | Environment bootstrap doc + install script (macOS ARM + Linux) | `SETUP.md`, `bootstrap.sh` | — | 3 h | TODO |
| T-006 | Diagram conventions + Mermaid style guide | `PLAN/diagram-guide.md` | — | 1 h | TODO |
| T-007 | Assessment bank format + auto-grader harness | `assessments/`, `grade.py` | T-003 | 3 h | TODO |
| T-008 | Anki deck pipeline (markdown → .apkg) | `decks/build.py` | T-003 | 2 h | TODO |
| T-009 | Two persona journey maps (Aarav / Meera) week-by-week | `PLAN/personas.md` | T-000 | 2 h | TODO |
| T-010 | Prerequisite/dependency graph across all 34 weeks | `PLAN/dep-graph.md` (Mermaid) | T-001 | 2 h | TODO |
| T-011 | Cost & hardware budget doc (incl. no-GPU fallback paths) | `PLAN/hardware-and-cost.md` | — | 2 h | TODO |
| T-012 | Capstone + midterm project specs and rubrics | `PLAN/projects/` | T-001 | 4 h | TODO |
| T-013 | Instructor guide: how to teach each layer, live-session plan | `PLAN/instructor-guide.md` | T-000 | 3 h | TODO |
| T-014 | Publication pipeline (markdown → web artifact / PDF) | `publish/` | T-002 | 3 h | TODO |

---

## Level 1 — Phases

| ID | Phase | Weeks | Content units | Labs | Exit artifact | Status |
|---|---|---|---|---|---|---|
| T-P1 | Computational Thinking, Systems & SWE Core | 1–8 | 40 modules / ~130 micro-lessons | 24 | Containerized async FastAPI + Postgres service, tested & deployed | TODO |
| T-P2 | Math, Low-Level Systems & Data Engineering | 9–16 | 40 modules / ~128 micro-lessons | 22 | 16-bit ALU + TCP server + `dlt`→DuckDB pipeline + EDA dashboard | TODO |
| T-P3 | Classical ML & Giga-Scale MLOps | 17–24 | 40 modules / ~132 micro-lessons | 24 | **Midterm:** dockerized, K8s-served prediction API | TODO |
| T-P4 | Generative AI, RAG & Multi-Agent Systems | 25–32 | 40 modules / ~136 micro-lessons | 26 | **Capstone:** stateful multi-agent system w/ RAG, MCP, evals, tracing | TODO |

---

## Level 2 — Weeks

### Phase 1 — Weeks 1–8

| ID | Week | Title | Modules | Lab deliverable | Depends | Status |
|---|---|---|---|---|---|---|
| T-P1-W01 | 1 | Algorithmic Thinking & Memory Foundations (C) | 5 | Sorting/search suite in C, zero Valgrind leaks | T-005 | TODO |
| T-P1-W02 | 2 | Terminal, Git, Vim, SSH | 5 | CPU-monitor bash daemon auto-pushing to Git over SSH | W01 | TODO |
| T-P1-W03 | 3 | Python Core & Object-Oriented Design | 5 | Typed OOP library w/ tests + packaging | W02 | TODO |
| T-P1-W04 | 4 | Concurrency, Parallelism & `asyncio` | 5 | Async concurrent file downloader w/ progress + retries | W03 | TODO |
| T-P1-W05 | 5 | Web Plumbing: HTTP, HTML, CSS, ES6 | 5 | Responsive frontend that talks to a real API | W04 | TODO |
| T-P1-W06 | 6 | REST APIs with FastAPI + Pydantic | 5 | "Resume Tailor" full-stack app (frontend + FastAPI) | W05 | TODO |
| T-P1-W07 | 7 | Relational Theory, Modelling & SQL | 5 | Normalized e-commerce schema + analytical SQL suite | W06 | TODO |
| T-P1-W08 | 8 | Transactions, Indexing & SQLAlchemy | 5 | Concurrency-safe checkout: zero double-purchase under load | W07 | TODO |

### Phase 2 — Weeks 9–16

| ID | Week | Title | Modules | Lab deliverable | Depends | Status |
|---|---|---|---|---|---|---|
| T-P2-W09 | 9 | Digital Logic → CPU (Nand2Tetris I) | 5 | 16-bit ALU + registers built from NAND | W01 | TODO |
| T-P2-W10 | 10 | Networking & Raw Sockets | 5 | Multi-threaded TCP chat server + Wireshark trace report | W09, W04 | TODO |
| T-P2-W11 | 11 | Linear Algebra & Calculus for AI | 5 | `nanomath`: dot/matmul/eig/SVD/numeric gradients from scratch | W03 | TODO |
| T-P2-W12 | 12 | Probability, Statistics & Experimentation | 5 | A/B test analyzer + Bayes classifier from scratch | W11 | TODO |
| T-P2-W13 | 13 | DSA I: Complexity & Linear Structures | 5 | Custom hash table with chaining + benchmark harness | W03 | TODO |
| T-P2-W14 | 14 | DSA II: Trees, Graphs & Dynamic Programming | 5 | 15 medium problems + Dijkstra route planner | W13 | TODO |
| T-P2-W15 | 15 | Data Engineering: Ingestion & Pipelines (`dlt`, DuckDB) | 5 | Incremental scraping pipeline w/ schema evolution | W06, W08 | TODO |
| T-P2-W16 | 16 | Pandas, EDA & Automated Analysis | 5 | Auto-generated EDA dashboard (distributions, outliers, correlations) | W15, W12 | TODO |

### Phase 3 — Weeks 17–24

| ID | Week | Title | Modules | Lab deliverable | Depends | Status |
|---|---|---|---|---|---|---|
| T-P3-W17 | 17 | Supervised Learning from Scratch | 5 | NumPy-only Linear + Logistic Regression class w/ GD | W11, W16 | TODO |
| T-P3-W18 | 18 | Trees, Ensembles & Unsupervised Learning | 5 | Churn model: XGBoost + tuning + clustering segmentation | W17 | TODO |
| T-P3-W19 | 19 | Evaluation, Metrics & Validation | 5 | Leakage-proof CV harness + metric report generator | W18 | TODO |
| T-P3-W20 | 20 | Feature Engineering & Imbalanced Data | 5 | Fraud pipeline: threshold optimization on PR curve | W19 | TODO |
| T-P3-W21 | 21 | Neural Networks & Backpropagation | 5 | 2-layer NN + autograd engine from scratch (NumPy) | W17, W11 | TODO |
| T-P3-W22 | 22 | PyTorch, CNNs & Transfer Learning | 5 | Blood-cell CNN classifier ≥90% test accuracy | W21 | TODO |
| T-P3-W23 | 23 | MLOps I: Packaging, Docker & Serverless | 5 | Model API in Docker → AWS Lambda + API Gateway | W22, W06 | TODO |
| T-P3-W24 | 24 | MLOps II: Kubernetes & Model Serving | 5 | HPA-scaled serving on `kind` + load test report | W23 | TODO |
| T-P3-MID | — | **Midterm project** (2-week overlay on W23–24) | — | End-to-end ML system, deployed + defended | W24 | TODO |

### Phase 4 — Weeks 25–32

| ID | Week | Title | Modules | Lab deliverable | Depends | Status |
|---|---|---|---|---|---|---|
| T-P4-W25 | 25 | Tokenizers & Transformer Internals | 5 | `minbpe` tokenizer + causal Transformer block from scratch | W22 | TODO |
| T-P4-W26 | 26 | Quantization, PEFT & Local Serving | 5 | QLoRA-tuned 3B model emitting strict JSON + vLLM serve | W25 | TODO |
| T-P4-W27 | 27 | RAG I: Chunking, Embeddings & Vector Indexes | 5 | 1,000-PDF pgvector/HNSW index with measured recall | W08, W26 | TODO |
| T-P4-W28 | 28 | RAG II: Hybrid Search, Re-ranking & Caching | 5 | BM25+dense hybrid + HyDE + cross-encoder rerank + semantic cache | W27 | TODO |
| T-P4-W29 | 29 | Agents I: Loops, Tools & MCP | 5 | ReAct agent from scratch + custom MCP server | W26, W06 | TODO |
| T-P4-W30 | 30 | Agents II: LangGraph, Multi-Agent & Durability | 5 | Incident auto-remediation graph w/ checkpoint & resume | W29 | TODO |
| T-P4-W31 | 31 | Evals & Defensive AI | 5 | LLM-as-judge suite in GitHub Actions + Llama Guard layer | W30, W28 | TODO |
| T-P4-W32 | 32 | LLMOps: Observability, Cost & Reliability | 5 | OpenTelemetry + Langfuse tracing w/ per-step cost attribution | W31 | TODO |
| T-P4-CAP | — | **Capstone** (3-week overlay on W30–32) | — | Distributed multi-agent system, defended | W32 | TODO |

---

## Per-week task template (applies to every T-Px-Wnn)

Each week task expands into exactly these sub-tasks:

| Sub-ID | Task | Definition of done |
|---|---|---|
| `.A` | Week overview + learning objectives + dependency note | objectives are testable verbs, not "understand" |
| `.B` | Module & lesson decomposition | every lesson has a 1-line outcome |
| `.C` | Write Layer 1 for all lessons | passes beginner-jargon check |
| `.D` | Write Layer 2 for all lessons | reference impl runs + tests pass |
| `.E` | Write Layer 3 for all lessons | contains real numbers + failure modes |
| `.F` | Build lab (basic/standard/hard + tests + rubric) | `make verify` green on solution, red on starter |
| `.G` | Diagrams | Mermaid renders; every structural concept has one |
| `.H` | Assessment bank (8 concept + 1 code + 3 interview per lesson) | auto-grader runs |
| `.I` | "Apply at work" section for both personas | 3 concrete job scenarios each |
| `.J` | Anki deck + 5-minute explain prompt | deck builds |
| `.K` | Technical review pass against §5 reject criteria | zero reject flags |
| `.L` | Beginner-readability pass (Aarav simulation) | no undefined term in Layer 1 |

---

## Suggested build order

1. **T-000 → T-014** (infrastructure) — 1 pass, ~30 h.
2. **Vertical slice pilot:** build **Week 1 completely** (all 12 sub-tasks) as the reference implementation of the spec. Review, adjust spec, then scale.
3. Then phases in order 1 → 2 → 3 → 4, week by week, because dependencies are strictly forward.
4. Projects (`T-P3-MID`, `T-P4-CAP`) authored after their prerequisite weeks are drafted.
