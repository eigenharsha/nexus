# Phase 4 — Granular Task Breakdown (Weeks 25–32)
**Goal:** open the black box of LLMs, build retrieval that works at 10M+ documents, architect durable multi-agent systems, and operate them with evals, guardrails and tracing.

Every module below carries a **`VIS:`** line (the diagrams/sketches/animations to produce) and a **`REF:`** line (primary sources + papers). See `PLAN/03-visual-spec.md` and `PLAN/02-references-library.md`.

---

## T-P4-W25 — Week 25: Tokenizers & Transformer Internals

**Week outcome:** learner has written a BPE tokenizer and a causal Transformer from scratch, and can explain every tensor shape in the forward pass.

### `P4-W25-M1` — Text → tokens
- Micro-lessons: (a) why not words or characters; (b) Unicode & UTF-8 revisited; (c) Byte-Pair Encoding algorithm; (d) training a tokenizer (merges & vocabulary); (e) special tokens & chat templates; (f) tokenization's downstream effects
- **L1 Ground:** tokenize a sentence in a playground; count tokens; see that "strawberry" splits oddly.
- **L2 Build:** implement BPE training + encode/decode (`minbpe` style); vocabulary size trade-offs; why token counts differ by language (and what that costs non-English users in $); chat templates and special-token bugs.
- **L3 Edge:** tokenizer artifacts explaining real model failures (counting letters, arithmetic, code indentation); SentencePiece vs tiktoken vs BPE variants; vocabulary size vs embedding-matrix parameter count computed; the "glitch token" phenomenon.
- **VIS:** hand-drawn sketch of the merge table growing step by step; animated GIF of merges applied to one word; a "same sentence, 4 tokenizers" comparison strip.
- **REF:** Sennrich et al. 2016 (BPE); Kudo & Richardson 2018 (SentencePiece); Karpathy `minbpe` repo; tiktoken docs.
- **Hands-on:** train a BPE tokenizer on a 10 MB corpus; compare compression ratio and vocabulary against GPT-2's tokenizer.

### `P4-W25-M2` — Embeddings & positional information
- Micro-lessons: (a) token embeddings; (b) the embedding matrix as a lookup; (c) why order needs encoding; (d) sinusoidal vs learned positions; (e) RoPE; (f) context length
- **L1 Ground:** embeddings as coordinates for meaning; nearest neighbours of a word vector.
- **L2 Build:** implement the embedding layer; absolute vs rotary positions in code; how context length interacts with position encoding; the shape of `(batch, seq, d_model)` fixed in your head forever.
- **L3 Edge:** RoPE derivation and why it extrapolates better; position-interpolation/YaRN context extension; ALiBi; the memory cost of long context computed exactly.
- **VIS:** whiteboard sketch of the lookup table → vectors; animated rotation showing RoPE acting on a 2-D pair; a context-length vs memory chart.
- **REF:** Vaswani et al. 2017; Su et al. 2021 (RoPE); Press et al. 2021 (ALiBi); Chen et al. 2023 (Position Interpolation).
- **Hands-on:** implement sinusoidal and rotary encodings; visualize both and show the extrapolation difference.

### `P4-W25-M3` — Self-attention
- Micro-lessons: (a) the intuition: every token looks at every other; (b) Q, K, V; (c) scaled dot-product attention; (d) the causal mask; (e) multi-head attention; (f) attention shapes end to end
- **L1 Ground:** attention as "who should I pay attention to?" — a 4-word sentence scored by hand, on a whiteboard, in a table.
- **L2 Build:** implement scaled dot-product attention in PyTorch from scratch; the causal mask and why it's needed for generation; multi-head splitting/concatenation; verify against `nn.MultiheadAttention`.
- **L3 Edge:** the √d_k scaling derived; O(n²) cost in time and memory computed for n = 1k/8k/128k; FlashAttention's tiling trick (IO-aware, not approximate) explained; GQA/MQA and the KV-cache size reduction computed for a real model.
- **VIS:** the single most important animation of the course — an attention-matrix heatmap animating token by token as generation proceeds, with the causal mask visibly blocking the upper triangle; plus a hand-drawn Q/K/V sketch.
- **REF:** Vaswani et al. 2017; Dao et al. 2022 (FlashAttention); Ainslie et al. 2023 (GQA); Elhage et al. "A Mathematical Framework for Transformer Circuits".
- **Hands-on:** implement attention; then visualize real attention maps from a small pretrained model on a sentence and interpret three heads.

### `P4-W25-M4` — The Transformer block & the full decoder
- Micro-lessons: (a) residual connections; (b) LayerNorm/RMSNorm & pre-norm; (c) the feed-forward network; (d) stacking blocks; (e) the LM head & weight tying; (f) parameter counting
- **L1 Ground:** the block as a sandwich diagram; data flowing through, drawn by hand.
- **L2 Build:** implement a complete decoder block and stack it into a GPT; count parameters by hand and check against the model; train a tiny character-level model.
- **L3 Edge:** why the FFN is ~2/3 of parameters; SwiGLU; residual stream as a communication channel (interpretability view); pre-norm vs post-norm training stability; the exact parameter formula for a decoder given (layers, d_model, heads, vocab).
- **VIS:** an exploded-view hand-drawn architecture diagram with tensor shapes annotated at every arrow; an animated forward pass highlighting each sub-layer in sequence.
- **REF:** Radford et al. 2019 (GPT-2); Karpathy `nanoGPT`; Shazeer 2020 (GLU variants); Xiong et al. 2020 (pre-LN).
- **Hands-on:** train `nanoGPT`-style on a small corpus; report loss curve, parameter count, and samples at 3 training stages.

### `P4-W25-M5` — Generation, decoding & inference cost
- Micro-lessons: (a) next-token prediction & sampling; (b) temperature, top-k, top-p; (c) greedy vs beam search; (d) repetition penalties; (e) the KV cache; (f) prefill vs decode & the cost model
- **L1 Ground:** sample from a distribution at three temperatures and see the personality change.
- **L2 Build:** implement generation with a KV cache; measure the speedup; parameter recipes for deterministic vs creative output; structured/constrained decoding preview.
- **L3 Edge:** prefill (compute-bound) vs decode (memory-bandwidth-bound) — the single most important mental model for LLM cost and latency; KV-cache size formula computed for a 7B model at 8k context; continuous batching (vLLM) explained from this; tokens/sec ceilings from memory bandwidth.
- **VIS:** animated KV-cache growth per generated token; a prefill-vs-decode timeline diagram; a cost-per-1k-tokens calculator widget.
- **REF:** Kwon et al. 2023 (vLLM/PagedAttention); Holtzman et al. 2019 (nucleus sampling); Pope et al. 2022 (efficient Transformer inference).
- **Hands-on:** implement KV-caching yourself; measure tokens/sec with and without; compute and verify the memory formula.

### `LAB-P4-W25` — **`minbpe` + `nanoGPT` from scratch**
- `basic`: BPE encode/decode against a provided merge table; attention on a fixed example.
- `standard`: train your own BPE tokenizer, implement a full causal Transformer (attention, multi-head, block, stack, LM head), train on a corpus, generate text, implement KV-cached generation; every component unit-tested against PyTorch equivalents.
- `hard`: add RoPE + GQA + FlashAttention (via `scaled_dot_product_attention`), measure tokens/sec and memory at 3 context lengths, and produce the attention-visualization tool.
- **Ship it:** repo + an illustrated "how a Transformer works" explainer built from your own diagrams. Highest-signal portfolio piece for AI roles.

---

## T-P4-W26 — Week 26: Quantization, PEFT & Local Serving

**Week outcome:** learner fine-tunes a small model on their own hardware and serves it — with the memory arithmetic fully understood.

### `P4-W26-M1` — Numeric precision & quantization
- Micro-lessons: (a) FP32/FP16/BF16 layouts; (b) INT8/INT4 & scaling; (c) post-training quantization vs QAT; (d) GPTQ/AWQ; (e) GGUF & llama.cpp; (f) measuring quality loss
- **L1 Ground:** the Week-1 bit lesson pays off — the same number stored in 32, 16, 8 and 4 bits, shown side by side with the error.
- **L2 Build:** quantize a model with `bitsandbytes`; run GGUF quantizations in Ollama; measure size, speed and quality across Q8/Q5/Q4; per-channel vs per-tensor scaling.
- **L3 Edge:** outlier features and why naive INT8 fails (LLM.int8() insight); GPTQ's second-order approach vs AWQ's activation awareness; the quality/size Pareto curve measured on a real eval set; calibration-set selection effects.
- **VIS:** hand-drawn bit-layout comparison; an animated "float squeezed into 4 bits" visual; a Pareto plot of size vs quality with your own measurements.
- **REF:** Dettmers et al. 2022 (LLM.int8()); Frantar et al. 2022 (GPTQ); Lin et al. 2023 (AWQ); llama.cpp quantization docs.
- **Hands-on:** benchmark 5 quantization levels of one model: VRAM, tokens/sec, and score on a 50-question eval set; plot the Pareto frontier and pick a default.

### `P4-W26-M2` — Fine-tuning: when and why
- Micro-lessons: (a) prompting vs RAG vs fine-tuning decision framework; (b) full fine-tuning memory math; (c) instruction tuning; (d) dataset construction & quality; (e) catastrophic forgetting; (f) evaluation before/after
- **L1 Ground:** three ways to make a model do your task — try prompting first, always.
- **L2 Build:** the decision table with cost/latency/quality/maintenance columns; building a 500–2000 example instruction dataset; train/val split for fine-tuning; measuring the actual lift.
- **L3 Edge:** the VRAM formula from Week 21 applied to 7B/13B/70B; data quality beats data quantity (LIMA-style evidence); forgetting measured on a general benchmark after task tuning; when fine-tuning is the *wrong* answer (facts → use RAG).
- **VIS:** decision-tree sketch "should I fine-tune?"; a stacked-bar memory diagram (weights/grads/optimizer/activations) for full vs LoRA vs QLoRA.
- **REF:** Zhou et al. 2023 (LIMA); Ouyang et al. 2022 (InstructGPT); Hugging Face alignment handbook.
- **Hands-on:** build a 500-example dataset for a real task from your own job/project domain, with a documented quality rubric.

### `P4-W26-M3` — LoRA & QLoRA
- Micro-lessons: (a) low-rank adaptation intuition (Week 11 SVD pays off); (b) rank, alpha, target modules; (c) QLoRA: 4-bit base + LoRA adapters; (d) NF4 & double quantization; (e) training config & hyperparameters; (f) merging & serving adapters
- **L1 Ground:** LoRA as "a small patch on a frozen model" — the ΔW = BA sketch, drawn by hand with dimensions.
- **L2 Build:** full QLoRA run with `peft` + `trl` on a 3B model; parameter-count comparison (0.1% trainable); choosing `r`, `lora_alpha`, target modules; monitoring the loss; merging adapters back.
- **L3 Edge:** rank vs task-complexity empirically (sweep r = 4/8/16/64); paged optimizers; multi-adapter serving (one base, many tasks) and its economics; LoRA's failure cases vs full fine-tuning; DoRA/rsLoRA briefly.
- **VIS:** animated diagram of the frozen weight matrix with a thin B·A pathway added, dimensions labelled; a trainable-parameter bar chart.
- **REF:** Hu et al. 2021 (LoRA); Dettmers et al. 2023 (QLoRA); `peft` documentation.
- **Hands-on:** the rank sweep — train at 4 ranks, plot eval score vs trainable parameters vs VRAM, and justify your chosen default.

### `P4-W26-M4` — Structured output & tool-calling behaviour
- Micro-lessons: (a) why JSON compliance is hard; (b) prompt-only approaches and their failure rate; (c) constrained decoding (grammars, `outlines`); (d) fine-tuning for schema compliance; (e) tool-call formats; (f) validation & repair loops
- **L1 Ground:** ask a model for JSON 20 times; count the failures. That's the problem.
- **L2 Build:** Pydantic schema → JSON Schema → constrained generation (Week 6 pays off); a validate-and-repair loop; measuring compliance rate before and after fine-tuning.
- **L3 Edge:** how grammar-constrained decoding masks logits at each step (implement a tiny version); the quality cost of over-constraining; function-calling as a fine-tuned behaviour vs a decoding constraint, compared on accuracy and latency.
- **VIS:** animated token-by-token generation with a grammar mask greying out invalid tokens; a hand-drawn state machine for the JSON grammar.
- **REF:** Willard & Louf 2023 (outlines / efficient guided generation); Anthropic + OpenAI structured-output docs; `instructor` library.
- **Hands-on:** raise JSON validity from a measured baseline to >99% using three methods; report the compliance/latency trade-off for each.

### `P4-W26-M5` — Local & self-hosted serving
- Micro-lessons: (a) Ollama for local development; (b) vLLM architecture; (c) continuous batching & PagedAttention; (d) OpenAI-compatible APIs; (e) throughput vs latency tuning; (f) cost comparison vs hosted APIs
- **L1 Ground:** run a model locally with Ollama and call it from Python.
- **L2 Build:** serve the fine-tuned model with vLLM behind an OpenAI-compatible endpoint; adapter serving; concurrency settings; integrating it into the Week-6 FastAPI service.
- **L3 Edge:** PagedAttention's memory-fragmentation fix explained (it's the OS virtual-memory idea from Week 9); throughput vs latency curve measured at 1/8/32/128 concurrent requests; the break-even calculation between self-hosting and a hosted API at a given monthly token volume.
- **VIS:** animated continuous-batching timeline (requests joining/leaving a running batch) vs static batching; a paged-KV-cache block diagram.
- **REF:** Kwon et al. 2023 (vLLM); Ollama docs; vLLM production docs.
- **Hands-on:** produce the self-host vs API cost model for your own workload, with measured throughput as the input; state the crossover volume.

### `LAB-P4-W26` — **QLoRA fine-tune for strict structured output**
- `basic`: run a provided QLoRA config; verify the model loads and generates.
- `standard`: build a 500+ example dataset, QLoRA fine-tune a 3B model for a real structured-extraction task, achieve >99% schema-valid output measured on a held-out set, merge and serve via vLLM behind an OpenAI-compatible endpoint, integrate into the Week-6 service.
- `hard`: beat the base model + constrained decoding on both accuracy *and* cost; deliver the rank sweep, the quantization Pareto plot, and a written serve-vs-API cost analysis.
- **Ship it:** model card + adapter on Hugging Face + a reproducible training script. CPU/Colab fallback path documented.

---

## T-P4-W27 — Week 27: RAG I — Chunking, Embeddings & Vector Indexes

**Week outcome:** learner builds a retrieval system over 1,000+ real documents and can *measure* its quality rather than guess.

### `P4-W27-M1` — Why RAG, and the ingestion problem
- Micro-lessons: (a) parametric vs non-parametric knowledge; (b) the RAG pipeline end to end; (c) document parsing (PDF, HTML, tables, scans); (d) cleaning & metadata; (e) the ingestion failure modes; (f) evaluation-first mindset
- **L1 Ground:** ask a model about a private document — it can't. Add the text to the prompt — it can. That's RAG.
- **L2 Build:** a real parsing pipeline (PyMuPDF/unstructured), table and header handling, metadata extraction, and an ingestion quality report; garbage-in-garbage-out demonstrated with a badly parsed PDF.
- **L3 Edge:** parsing is where most RAG systems actually fail — measured: retrieval quality on well-parsed vs naively parsed corpora; OCR and layout-aware parsing; document-level vs passage-level metadata design.
- **VIS:** whiteboard sketch of the full RAG pipeline with failure points marked in red; a before/after of a mangled PDF parse.
- **REF:** Lewis et al. 2020 (RAG); Gao et al. 2023 (RAG survey); `unstructured` docs.
- **Hands-on:** parse 50 messy PDFs; produce a parse-quality scorecard and fix the worst 5 cases.

### `P4-W27-M2` — Chunking strategies
- Micro-lessons: (a) why chunk at all; (b) fixed-size & overlap; (c) recursive/structural chunking; (d) semantic chunking; (e) parent-child / small-to-big; (f) chunk metadata & context injection
- **L1 Ground:** the same document chunked three ways, printed side by side.
- **L2 Build:** implement each strategy; chunk-size vs retrieval-quality experiment on a real eval set; parent-child retrieval (embed small, return big); adding section headers to every chunk.
- **L3 Edge:** chunking is a hyperparameter, not a decision — sweep it and plot Recall@k vs chunk size; late chunking / contextual retrieval; the token-cost implications of chunk size on the generation step.
- **VIS:** animated document being split under each strategy, with the retrieved unit highlighted; hand-drawn parent-child diagram.
- **REF:** Anthropic "Contextual Retrieval"; LlamaIndex chunking docs; Günther et al. (late chunking).
- **Hands-on:** run the chunk-size sweep on your own corpus and publish the plot with a recommendation.

### `P4-W27-M3` — Embeddings for retrieval
- Micro-lessons: (a) what an embedding model is trained to do; (b) bi-encoders; (c) choosing a model (MTEB, size, dimension, language); (d) normalization & similarity metrics; (e) batching & cost; (f) domain adaptation
- **L1 Ground:** embed 10 sentences; print the similarity matrix; see semantics appear.
- **L2 Build:** embedding pipeline with batching and caching; model comparison on *your* data (not the leaderboard); dimension vs storage cost; handling long documents.
- **L3 Edge:** why leaderboard rank ≠ your task's rank (run the experiment and show a reversal); Matryoshka embeddings for adjustable dimensions; asymmetric query/document embedding; fine-tuning an embedding model on domain pairs and the measured lift.
- **VIS:** UMAP plot of your corpus embeddings colored by document type; a hand-drawn bi-encoder vs cross-encoder comparison.
- **REF:** Reimers & Gurevych 2019 (Sentence-BERT); MTEB benchmark; Kusupati et al. 2022 (Matryoshka).
- **Hands-on:** evaluate 4 embedding models on your own labelled query set; report Recall@10 and cost; choose one with justification.

### `P4-W27-M4` — Vector indexes: Flat, IVF, HNSW
- Micro-lessons: (a) exact vs approximate search; (b) brute-force cost; (c) IVF (clustering — Week 18 K-Means returns); (d) HNSW (graphs — Week 14 returns); (e) parameters (`M`, `ef_construction`, `ef_search`, `nprobe`); (f) index build vs query trade-offs
- **L1 Ground:** brute-force cosine search over 1,000 vectors, timed. Then 1M — and it hurts.
- **L2 Build:** pgvector with HNSW and IVFFlat; parameter tuning; measuring recall against the exact brute-force ground truth (from Week 14's lab); index build time and memory.
- **L3 Edge:** HNSW's skip-list-over-graph structure explained from first principles; the recall/latency/memory three-way trade-off measured across parameter grids; when Postgres+pgvector is enough vs a dedicated vector DB (honest thresholds with numbers); filtering + ANN interaction (pre- vs post-filter) and its correctness trap.
- **VIS:** **the key animation** — HNSW layered graph with a query descending through layers, greedily hopping; an IVF Voronoi-cell diagram with the probe list highlighted; a hand-drawn "why approximate is fine" sketch.
- **REF:** Malkov & Yashunin 2016 (HNSW); Johnson et al. 2017 (FAISS); pgvector docs.
- **Hands-on:** on 1M vectors, produce the recall-vs-QPS curve for HNSW at 5 parameter settings and for IVF at 5; pick an operating point and defend it.

### `P4-W27-M5` — Building & evaluating a retrieval system
- Micro-lessons: (a) storing chunks + vectors + metadata; (b) metadata filtering; (c) building an eval set; (d) retrieval metrics (Recall@k, MRR, NDCG — Week 19 returns); (e) the end-to-end RAG prompt; (f) citations & grounding
- **L1 Ground:** query → retrieve 5 chunks → stuff into a prompt → answer with citations.
- **L2 Build:** a proper eval set (50–200 query/relevant-chunk pairs, some generated, all reviewed), a retrieval evaluation script, and an ablation table showing each design choice's effect.
- **L3 Edge:** separating retrieval failure from generation failure diagnostically; the "lost in the middle" position effect measured; context-window budgeting; when more context makes answers worse.
- **VIS:** an ablation table rendered as a chart; a hand-drawn diagnosis flowchart "the answer was wrong — whose fault?".
- **REF:** Liu et al. 2023 (Lost in the Middle); RAGAS paper; BEIR benchmark.
- **Hands-on:** build the eval set and run the ablation; every subsequent RAG change in Week 28 must be justified against this baseline.

### `LAB-P4-W27` — **1,000-PDF retrieval system on pgvector/HNSW**
- `basic`: ingest 50 provided PDFs, chunk, embed, store, and query.
- `standard`: ingest 1,000 real PDFs — robust parsing, chosen chunking strategy, evaluated embedding model, pgvector + HNSW with tuned parameters, metadata filtering, a 100-query eval set, and a full ablation report with Recall@k and NDCG.
- `hard`: scale to 10M chunks (synthetically extended), report index build time, memory, p95 query latency and recall; implement filtered search correctly and prove it.
- **Ship it:** repo + `RETRIEVAL.md` with the ablation table and the HNSW parameter study.

---

## T-P4-W28 — Week 28: RAG II — Hybrid Search, Re-ranking & Caching

**Week outcome:** learner takes a working retrieval system to a production-quality one and can prove each improvement with numbers.

### `P4-W28-M1` — Sparse retrieval & BM25
- Micro-lessons: (a) keyword search & inverted indexes (Week 8/13 return); (b) TF-IDF → BM25; (c) the BM25 formula explained term by term; (d) tokenization & analyzers; (e) Postgres full-text search; (f) where sparse beats dense
- **L1 Ground:** search for an exact product code — dense embeddings fail, keyword search wins instantly.
- **L2 Build:** BM25 with `rank_bm25` and with Postgres `tsvector`/GIN; parameter `k1`/`b` tuning; analyzer choices; measuring on the Week-27 eval set.
- **L3 Edge:** BM25's saturation and length-normalization terms derived; SPLADE/learned sparse retrieval; why dense retrieval fails on rare entities, IDs, and numbers — with concrete measured examples from your corpus.
- **VIS:** hand-drawn inverted index; a per-term BM25 score-contribution bar chart for one query.
- **REF:** Robertson & Zaragoza 2009 (BM25); Formal et al. 2021 (SPLADE); Postgres FTS docs.
- **Hands-on:** find 10 queries in your corpus where BM25 beats dense and 10 where dense wins; categorize the pattern.

### `P4-W28-M2` — Hybrid search & fusion
- Micro-lessons: (a) why combine; (b) score normalization; (c) Reciprocal Rank Fusion; (d) weighted linear combination; (e) tuning the mix; (f) single-store vs multi-store architecture
- **L1 Ground:** run both retrievers on one query and merge the lists by hand.
- **L2 Build:** implement RRF and weighted fusion in Postgres (both indexes in one database); tune the weight on the eval set; measure the lift over each single method.
- **L3 Edge:** why RRF is robust without score calibration (and where weighted fusion still wins); fusion at scale — latency budget when running two retrievers; the marginal gain curve as you add methods.
- **VIS:** animated two-ranked-lists-merging visual; a lift chart (dense / sparse / hybrid) on your eval set.
- **REF:** Cormack et al. 2009 (RRF); Elastic/Weaviate hybrid-search docs; Azure AI Search hybrid evaluation write-ups.
- **Hands-on:** produce the three-way comparison table with CIs (Week 12 bootstrap) and state whether the lift is significant.

### `P4-W28-M3` — Query understanding & transformation
- Micro-lessons: (a) the query is the weak link; (b) query rewriting; (c) HyDE; (d) multi-query / query decomposition; (e) step-back prompting; (f) routing & intent classification
- **L1 Ground:** a vague question retrieves nothing; rewrite it and watch retrieval succeed.
- **L2 Build:** implement HyDE (generate a hypothetical answer, embed *that*), multi-query expansion with result fusion, and a router that picks retrieval strategy by intent; measure each on the eval set.
- **L3 Edge:** the latency and $ cost of each technique per query, tabulated against its measured gain — most teams add these blindly; when query expansion *hurts* (over-broadening); caching rewritten queries.
- **VIS:** hand-drawn flow of query → N rewrites → N retrievals → fusion; a gain-vs-latency scatter of all techniques tried.
- **REF:** Gao et al. 2022 (HyDE); Zheng et al. 2023 (Step-Back Prompting); Ma et al. 2023 (Query Rewriting for RAG).
- **Hands-on:** build the gain-vs-cost scatter plot for 6 query techniques and choose a production configuration.

### `P4-W28-M4` — Re-ranking with cross-encoders
- Micro-lessons: (a) bi-encoder vs cross-encoder; (b) the retrieve-then-rerank pattern; (c) choosing a re-ranker; (d) top-N selection and latency; (e) LLM-based re-ranking; (f) diversity (MMR)
- **L1 Ground:** the same 20 candidates, re-ordered by a cross-encoder — see the right answer jump to #1.
- **L2 Build:** add a cross-encoder over the top-50; measure NDCG lift and added latency; batch the re-ranking; choose N by the quality/latency curve.
- **L3 Edge:** why cross-encoders can't be used for first-stage retrieval (the O(N) cost computed); distillation of a cross-encoder into a bi-encoder; LLM re-rankers' cost/quality position; MMR for redundancy removal and when diversity beats relevance.
- **VIS:** animated re-ranking (list re-ordering with scores); a hand-drawn bi- vs cross-encoder architecture comparison.
- **REF:** Nogueira & Cho 2019 (passage re-ranking with BERT); Cohere/BGE re-ranker docs; Carbonell & Goldstein 1998 (MMR).
- **Hands-on:** plot NDCG and p95 latency vs re-rank depth N ∈ {10,20,50,100}; pick the operating point against a stated latency SLO.

### `P4-W28-M5` — Caching, cost & production RAG operations
- Micro-lessons: (a) the RAG cost model; (b) exact-match caching; (c) semantic caching with a similarity threshold; (d) cache invalidation on document updates; (e) incremental re-indexing; (f) monitoring retrieval quality in production
- **L1 Ground:** the same question asked twice — serve the second from cache in 5 ms.
- **L2 Build:** semantic cache with Redis + embeddings, threshold tuning against a false-hit rate, TTL and invalidation on re-index, incremental ingestion of new/changed documents (Week 15's incremental loading returns).
- **L3 Edge:** the false-hit danger of semantic caching (a wrong cached answer is worse than a slow one) — measure precision at several thresholds; cache stampede + request coalescing (Week 8 returns); per-query cost attribution; detecting retrieval-quality regressions without labels.
- **VIS:** hand-drawn cache-decision flowchart with the threshold band drawn on a similarity axis; a cost-per-query waterfall (embed / retrieve / rerank / generate).
- **REF:** GPTCache; Redis vector-search docs; Anthropic prompt-caching docs.
- **Hands-on:** measure hit rate, latency saving, $ saving and false-hit rate across 5 thresholds; recommend one and state the risk.

### `LAB-P4-W28` — **Production hybrid RAG**
- `basic`: add BM25 to the Week-27 system and fuse with RRF.
- `standard`: full pipeline — hybrid (BM25 + dense) → HyDE query rewriting → cross-encoder re-ranking → semantic cache → grounded generation with citations; every stage ablated on the Week-27 eval set with a final table showing quality, p95 latency and $/query.
- `hard`: hit a stated quality target under a stated latency and cost budget; add incremental re-indexing and prove cache correctness after a document update.
- **Ship it:** repo + `RAG-REPORT.md` — the ablation table is the artifact hiring managers will actually read.

---

## T-P4-W29 — Week 29: Agents I — Loops, Tools & MCP

**Week outcome:** learner builds an agent from scratch (no framework) and exposes real capabilities to it safely via a custom MCP server.

### `P4-W29-M1` — What an agent actually is
- Micro-lessons: (a) LLM call vs chain vs agent; (b) the Observe-Think-Act loop; (c) ReAct; (d) termination conditions; (e) when *not* to use an agent; (f) the reliability math of multi-step systems
- **L1 Ground:** build a 40-line agent loop with one tool — a calculator — and watch it reason.
- **L2 Build:** a from-scratch ReAct loop with tool dispatch, scratchpad management, max-iterations, and structured stop conditions; a decision table for chain vs agent.
- **L3 Edge:** compounding error — 95% per-step reliability over 10 steps = 60% end to end (the arithmetic every agent designer must internalize); why constrained workflows beat open agency for most business tasks; the autonomy/reliability trade-off curve.
- **VIS:** hand-drawn Observe-Think-Act loop; an animated trace of an agent's steps; a compounding-reliability chart.
- **REF:** Yao et al. 2022 (ReAct); Anthropic "Building Effective Agents"; Schick et al. 2023 (Toolformer).
- **Hands-on:** build the agent from scratch; then measure its success rate over 30 task instances and compute per-step reliability.

### `P4-W29-M2` — Tools & function calling
- Micro-lessons: (a) tool schemas (Week 6 Pydantic returns); (b) the tool-calling protocol; (c) writing good tool descriptions; (d) argument validation & error feedback; (e) tool result formatting; (f) tool-selection failures
- **L1 Ground:** give the model a weather tool; watch it decide to call it.
- **L2 Build:** a tool registry with Pydantic schemas, validation errors fed back as recoverable messages, idempotent and side-effect-safe tool design, result truncation for context budget.
- **L3 Edge:** tool-description quality measurably changes selection accuracy — run an ablation; tool-count degradation (accuracy vs number of tools available, measured); parallel tool calls; retry semantics for non-idempotent tools (Week 4 and Week 8 both return).
- **VIS:** hand-drawn tool-call round-trip sequence diagram; a chart of selection accuracy vs number of tools.
- **REF:** Anthropic tool-use docs; OpenAI function-calling docs; Patil et al. 2023 (Gorilla).
- **Hands-on:** measure tool-selection accuracy with 3, 10, and 30 tools available; then improve the 30-tool case with better descriptions and grouping.

### `P4-W29-M3` — Memory, context & state
- Micro-lessons: (a) the context window as a budget; (b) conversation memory strategies; (c) summarization & compaction; (d) retrieval as long-term memory (Week 27 returns); (e) scratchpads & working memory; (f) state serialization
- **L1 Ground:** an agent that forgets — then add memory and see it improve.
- **L2 Build:** a token budget manager, sliding window + summary hybrid, storing episodic memory in pgvector, structured state objects instead of raw transcript.
- **L3 Edge:** context rot / degradation with long contexts (measured on a needle task); what to keep vs summarize vs retrieve, as an explicit policy; cost of re-sending context every turn and prompt caching's effect (measure the $ difference).
- **VIS:** animated context window filling up and being compacted; a hand-drawn memory-hierarchy sketch (working / episodic / semantic).
- **REF:** Packer et al. 2023 (MemGPT); Anthropic prompt-caching + context-management docs; needle-in-a-haystack evaluations.
- **Hands-on:** run a 50-turn conversation under three memory strategies; report task success, tokens used and $ cost for each.

### `P4-W29-M4` — Model Context Protocol (MCP)
- Micro-lessons: (a) the M×N integration problem MCP solves; (b) architecture: hosts, clients, servers; (c) primitives: tools, resources, prompts; (d) transports (stdio, HTTP/SSE); (e) writing a server; (f) security model
- **L1 Ground:** connect an existing MCP server to a client and use its tools.
- **L2 Build:** write a custom MCP server exposing a local database and a restricted filesystem; typed tool definitions; error handling; testing the server standalone.
- **L3 Edge:** the security surface — a tool that can run shell commands is a remote-code-execution primitive; sandboxing, allow-lists, path traversal defence, read-only modes, and human-in-the-loop confirmation for destructive operations; prompt injection *through tool results* (setting up Week 31); transport choice and its trust implications (Week 10 returns).
- **VIS:** hand-drawn M×N → M+N diagram; an MCP request/response sequence diagram; a trust-boundary diagram with the dangerous edges marked in red.
- **REF:** MCP specification & official SDK docs; Anthropic MCP announcement + security guidance.
- **Hands-on:** write an MCP server giving an agent *safe* terminal access — allow-listed commands, timeout, output cap, no network, audit log — then try to break your own sandbox and document the attempts.

### `P4-W29-M5` — Pydantic AI & typed agents
- Micro-lessons: (a) typed agent frameworks; (b) dependency injection for agents; (c) structured result types; (d) validation & retries; (e) streaming; (f) testing agents deterministically
- **L1 Ground:** the same agent, rebuilt with Pydantic AI in a third of the lines.
- **L2 Build:** typed dependencies, result models, validators that trigger a retry, streaming partial results, and unit tests with a mocked model (so the test suite is fast and free).
- **L3 Edge:** framework vs from-scratch — the honest trade-off (control, debuggability, upgrade risk); making agent behaviour testable at all; deterministic replay of a recorded model trace as a regression test (the bridge to Week 31 evals).
- **VIS:** side-by-side sketch of the raw loop vs the framework-managed loop, with the framework's responsibilities shaded.
- **REF:** Pydantic AI docs; LangChain vs Pydantic AI design discussions.
- **Hands-on:** write a test suite for your agent that runs in under 10 seconds with zero API calls.

### `LAB-P4-W29` — **Agent from scratch + custom MCP server**
- `basic`: a ReAct loop with 2 tools and a max-iteration guard.
- `standard`: a from-scratch agent (tool registry, memory management, token budget, retries, structured stop conditions) plus a custom MCP server exposing a database and sandboxed terminal access; success measured over a 30-task benchmark; full test suite with a mocked model.
- `hard`: 30 tools with maintained selection accuracy; adversarial testing of the sandbox with a written report of every escape attempt and its mitigation.
- **Ship it:** repo + `SECURITY.md` documenting the MCP server's trust boundary. Rare and highly credible artifact.

---

## T-P4-W30 — Week 30: Agents II — LangGraph, Multi-Agent & Durability

**Week outcome:** learner architects a stateful multi-agent system that survives crashes — the capstone's backbone.

### `P4-W30-M1` — Graphs as the right abstraction
- Micro-lessons: (a) why linear chains break; (b) nodes, edges, conditional edges; (c) shared state schema; (d) cycles & loop control; (e) LangGraph basics; (f) visualizing the graph
- **L1 Ground:** draw your agent's flow as a graph on paper first; then it becomes code almost verbatim.
- **L2 Build:** a LangGraph app with typed state, conditional routing, and a cycle with a bounded iteration count; state reducers; graph visualization.
- **L3 Edge:** DAGs vs cyclic graphs and termination guarantees (Week 14's cycle detection returns); state-schema design determining what you can debug later; graph vs actor-model comparison.
- **VIS:** hand-drawn graph → generated LangGraph diagram side by side; an animated token traversing the graph with state shown at each node.
- **REF:** LangGraph documentation & conceptual guides; Anthropic "Building Effective Agents" (workflow patterns).
- **Hands-on:** convert your Week-29 from-scratch agent into a graph; diff the debuggability of the two.

### `P4-W30-M2` — Multi-agent patterns
- Micro-lessons: (a) when multiple agents beat one; (b) Orchestrator-Specialist; (c) Critic-Refiner; (d) Mixture of Agents / debate; (e) hand-off protocols; (f) shared vs isolated context
- **L1 Ground:** a writer agent and a critic agent improving a draft over 3 rounds.
- **L2 Build:** implement orchestrator-specialist routing with clear contracts between agents; a critic loop with an explicit rubric and a stopping rule; context isolation per specialist to control cost.
- **L3 Edge:** multi-agent is often *worse* — cost multiplies, errors compound, and coordination is a new failure surface; run the head-to-head (single strong agent vs your multi-agent system) on the same benchmark and report cost, latency and quality; when specialization genuinely wins.
- **VIS:** hand-drawn pattern catalogue (one sketch per pattern); a cost/quality scatter of single vs multi-agent runs.
- **REF:** Wu et al. 2023 (AutoGen); Wang et al. 2024 (Mixture-of-Agents); Anthropic multi-agent research-system write-up.
- **Hands-on:** the head-to-head benchmark — and be willing to conclude that single-agent wins.

### `P4-W30-M3` — Durable execution: checkpoint & resume
- Micro-lessons: (a) why agents must be durable; (b) checkpointers & thread IDs; (c) persistent backends (Postgres — Week 8 returns); (d) resuming after a crash; (e) time travel & state editing; (f) human-in-the-loop interrupts
- **L1 Ground:** kill the process mid-run; restart; watch it continue from the last node.
- **L2 Build:** a Postgres checkpointer, thread-scoped state, `interrupt()` for human approval before destructive actions, resume-from-edit for correcting an agent mid-flight.
- **L3 Edge:** exactly-once vs at-least-once semantics for tool side effects (Week 8's idempotency returns — a resumed agent must not re-charge a card); checkpoint size growth and pruning; what durable execution costs in latency, measured; comparison with Temporal-style workflow engines.
- **VIS:** animated crash-and-resume timeline showing checkpoints; hand-drawn state-machine sketch with the resume point marked.
- **REF:** LangGraph persistence docs; Temporal durable-execution concepts; the outbox pattern.
- **Hands-on:** build an agent whose tool charges money; crash it mid-transaction 20 times and prove no double-charge.

### `P4-W30-M4` — Resilience, budgets & failure handling
- Micro-lessons: (a) token & cost budgets per run; (b) timeouts and step limits; (c) deadlock and livelock in agent graphs; (d) retry vs escalate vs abort; (e) partial-failure recovery; (f) graceful degradation
- **L1 Ground:** an agent stuck in a loop, burning tokens — add a budget guard and watch it stop.
- **L2 Build:** a budget manager (tokens, $, wall-clock, steps) enforced at graph level; circuit breakers around flaky tools (Week 4 returns); escalation to a human with a structured summary.
- **L3 Edge:** detecting livelock (agent making calls but no progress) with a progress metric; the failure taxonomy for agent systems and a detector for each; designing for the 5% of runs that go wrong — because they will define your users' experience.
- **VIS:** hand-drawn failure-taxonomy tree; an annotated token-burn chart of a runaway run vs a guarded one.
- **REF:** LangGraph recursion/limits docs; SRE-style error-budget thinking applied to agents; published agent post-mortems.
- **Hands-on:** inject 6 failure types (tool timeout, malformed output, infinite loop, budget exhaustion, dependency down, contradictory instructions) and show correct handling of each.

### `P4-W30-M5` — Architecting a real agentic system
- Micro-lessons: (a) decomposing a business process into agents/tools; (b) deciding autonomy level per step; (c) the human-approval boundary; (d) integrating RAG (Week 28) and MCP (Week 29); (e) deployment shape; (f) documenting the design
- **L1 Ground:** map an incident-response runbook to a graph, on paper, before any code.
- **L2 Build:** the full incident auto-remediation architecture — planner, analyst, executor, plus RAG over runbooks and an MCP server for safe system access; approval gates for anything destructive.
- **L3 Edge:** blast-radius design (what's the worst thing this system can do, and what stops it?); staged autonomy rollout (suggest → approve → auto with rollback); auditability requirements; the organizational reality of shipping an autonomous system.
- **VIS:** the full system architecture as a hand-drawn whiteboard diagram, then a polished version — both published so learners see the progression from sketch to spec.
- **REF:** Anthropic agent-design guidance; LangGraph reference architectures; SRE incident-response literature.
- **Hands-on:** write the design document and the blast-radius analysis before writing the code.

### `LAB-P4-W30` — **Incident Auto-Remediation System**
- `basic`: a 3-node LangGraph (plan → analyze → report) with in-memory state.
- `standard`: planner + analyst + executor agents on LangGraph with typed state, Postgres checkpointing, human-approval interrupt before any remediation, RAG over a runbook corpus, MCP-served sandboxed terminal access, budget guards, and crash-resume proven by test.
- `hard`: survive 20 randomly-timed process kills with no duplicated side effects and no lost work; add a critic agent and show measured quality improvement; full failure-injection suite green.
- **Ship it:** repo + architecture doc + a recorded demo of a crash-and-resume. Capstone foundation.

---

## T-P4-W31 — Week 31: Evals & Defensive AI

**Week outcome:** learner can prove an AI system works and defend it against attack — the two things that separate a demo from a product.

### `P4-W31-M1` — Why evals, and how to build a dataset
- Micro-lessons: (a) vibes don't scale; (b) eval types (unit/reference/judge/human/production); (c) building a ground-truth set; (d) coverage & the error taxonomy; (e) eval maintenance; (f) eval-driven development
- **L1 Ground:** change one prompt word; run 20 saved cases; see 3 regress. That's why evals exist.
- **L2 Build:** a 100+ case eval set derived from real failures, an error taxonomy from manual review of 50 outputs, cheap deterministic assertions first (format, length, required entities, refusals), then the expensive ones.
- **L3 Edge:** eval-set construction bias; how many cases you need for a detectable difference (Week 12's power analysis applied); the offline/online gap; treating evals as a versioned product asset.
- **VIS:** hand-drawn eval pyramid (assertions → reference → judge → human); an error-taxonomy mind map from a real review session.
- **REF:** Hamel Husain's evals writing; OpenAI Evals; Anthropic evaluation guidance.
- **Hands-on:** manually review 50 outputs from your Week-30 system, build the error taxonomy, and convert the top 3 categories into automated checks.

### `P4-W31-M2` — LLM-as-a-Judge
- Micro-lessons: (a) the pattern; (b) judge prompt design & rubrics; (c) pairwise vs pointwise; (d) known biases (position, verbosity, self-preference); (e) validating the judge against humans; (f) cost control
- **L1 Ground:** have a model grade 10 answers against a rubric; then check its grades yourself.
- **L2 Build:** a judge with an explicit rubric and required reasoning; pairwise comparison with position swapping; agreement measured against your own human labels (Cohen's kappa).
- **L3 Edge:** an unvalidated judge is a random-number generator with good grammar — measure the agreement and refuse to ship below a threshold; position and verbosity bias demonstrated numerically; using a cheaper model as judge and where it breaks; judge-cost budgeting for CI.
- **VIS:** hand-drawn judge-pipeline sketch; a confusion matrix of judge vs human labels; a bias demonstration chart (score vs answer length).
- **REF:** Zheng et al. 2023 (MT-Bench / LLM-as-a-Judge); RAGAS; G-Eval.
- **Hands-on:** validate your judge against 50 human-labelled examples; report kappa; iterate the rubric until agreement is acceptable.

### `P4-W31-M3` — RAG & agent-specific evaluation
- Micro-lessons: (a) decomposing RAG failure (retrieval vs generation); (b) faithfulness/groundedness; (c) answer relevancy; (d) context precision/recall; (e) agent trajectory evaluation; (f) tool-call correctness
- **L1 Ground:** an answer that sounds right but isn't in the sources — detect it.
- **L2 Build:** RAGAS-style metrics implemented and run against the Week-28 system; hallucination detection by claim-level source attribution; trajectory evaluation for agents (did it take a sensible path, not just reach an answer?).
- **L3 Edge:** end-state vs trajectory evaluation and why both are needed; evaluating multi-step systems where step 3 fails because of step 1; attributing a regression to the specific component that caused it.
- **VIS:** hand-drawn "which component failed?" diagnostic tree; a per-component score dashboard mock.
- **REF:** Es et al. 2023 (RAGAS); TruLens; LangSmith evaluation docs.
- **Hands-on:** plant 5 different failure causes in the Week-30 system and verify your eval suite attributes each to the right component.

### `P4-W31-M4` — Prompt injection & defensive design
- Micro-lessons: (a) prompt injection vs jailbreaking; (b) direct vs indirect injection; (c) the RAG/tool injection surface; (d) data-vs-instruction separation; (e) least privilege for tools; (f) output handling & downstream sinks
- **L1 Ground:** hide an instruction inside a document; watch the agent obey it. That's the whole attack.
- **L2 Build:** defence in depth — input filtering, delimiting untrusted content, instruction hierarchy, tool allow-lists and scoping, human approval for destructive actions, output encoding before it reaches a shell/SQL/browser sink.
- **L3 Edge:** why prompt injection has no complete fix (it's the confused-deputy problem) — design so that a successful injection is *not catastrophic*; the dual-LLM / privilege-separation pattern; exfiltration via markdown images and tool arguments; threat-modelling your own Week-30 system with an attack tree.
- **VIS:** hand-drawn attack-tree for the incident system; a trust-boundary diagram with every untrusted-input entry point in red; an animated walkthrough of one successful injection.
- **REF:** Greshake et al. 2023 (indirect prompt injection); OWASP Top 10 for LLM Applications; Simon Willison's prompt-injection series; Anthropic safety-practice docs.
- **Hands-on:** red-team your own system: 15 documented attack attempts, which succeeded, and the mitigation shipped for each.

### `P4-W31-M5` — Guardrails & moderation
- Micro-lessons: (a) input vs output guardrails; (b) Llama Guard & classifier-based moderation; (c) NeMo Guardrails / rule-based flows; (d) PII detection & redaction; (e) topical scoping & refusals; (f) measuring guardrail cost (latency, false positives)
- **L1 Ground:** add an input classifier that blocks an obviously abusive request.
- **L2 Build:** a Llama Guard input layer plus output checks (PII, groundedness, policy) on the Week-30 system; a guardrail eval set with both attacks and benign lookalikes; false-positive rate measured.
- **L3 Edge:** guardrails that block real users are a product failure — tune with a stated FP budget; latency cost of each layer, measured; guardrails as a *layer*, not a *fix* (the real control is least privilege); logging blocked requests for review without storing sensitive data.
- **VIS:** hand-drawn request-path diagram with each guardrail as a gate; an FP/FN trade-off curve from your own measurements.
- **REF:** Inan et al. 2023 (Llama Guard); NeMo Guardrails docs; Microsoft Presidio (PII).
- **Hands-on:** measure guardrail FP rate against 100 benign requests and TP rate against 100 attacks; report the operating point and its latency cost.

### `LAB-P4-W31` — **Eval CI pipeline + guardrail layer**
- `basic`: 20 eval cases with assertions running locally.
- `standard`: a 100+ case eval suite (assertions + validated LLM-judge + RAG metrics) running in GitHub Actions on every prompt/code change, failing the build on regression, with a results comment on the PR; plus a Llama Guard input layer and output PII/groundedness checks, with measured FP/TP rates.
- `hard`: judge validated to a stated agreement threshold; full red-team report with 15 attacks and mitigations; eval suite runtime and cost kept under a stated budget.
- **Ship it:** repo + `EVALS.md` + `RED-TEAM.md`. *This is the artifact that most distinguishes a serious AI engineer from a demo builder.*

---

## T-P4-W32 — Week 32: LLMOps — Observability, Cost & Reliability

**Week outcome:** learner can see, price and operate an AI system in production.

### `P4-W32-M1` — Tracing & OpenTelemetry
- Micro-lessons: (a) logs vs metrics vs traces; (b) spans, traces, context propagation; (c) OTel concepts & SDK; (d) instrumenting an LLM app; (e) semantic conventions for GenAI; (f) sampling
- **L1 Ground:** wrap one LLM call in a span and view the trace.
- **L2 Build:** instrument the whole Week-30 graph — one trace per run, a span per node/tool/LLM call, with inputs, outputs, token counts, model and latency as attributes; context propagation across async boundaries.
- **L3 Edge:** cardinality explosion and cost of tracing at scale; sampling strategies that keep the interesting traces (tail sampling on errors/latency); the GenAI semantic conventions and why standardization matters for tool portability; PII in traces and how to redact at the SDK boundary.
- **VIS:** an annotated waterfall trace screenshot with each span labelled; hand-drawn parent/child span tree.
- **REF:** OpenTelemetry GenAI semantic conventions; OTel Python docs; Langfuse/LangSmith tracing docs.
- **Hands-on:** produce a trace of one agent run and annotate every span with what it cost in time and money.

### `P4-W32-M2` — Langfuse & the LLM observability stack
- Micro-lessons: (a) what LLM observability adds beyond APM; (b) Langfuse setup (self-hosted); (c) sessions, users, traces; (d) prompt management & versioning; (e) datasets from production traces; (f) online evaluation
- **L1 Ground:** send traces to Langfuse and browse a real conversation.
- **L2 Build:** self-hosted Langfuse via Docker Compose, prompt versioning with rollback, converting production failures into eval cases automatically (closing the loop with Week 31), scoring traces online.
- **L3 Edge:** the feedback flywheel — production traces → labelled dataset → eval suite → improved prompt → measured in production; build-vs-buy for observability; data-retention and privacy policy for stored traces.
- **VIS:** hand-drawn flywheel diagram; a screenshot walkthrough of a real failure investigated from trace to fix.
- **REF:** Langfuse docs; LangSmith docs; Arize Phoenix.
- **Hands-on:** take one production failure from trace → eval case → fix → verified in the next eval run; document the full loop.

### `P4-W32-M3` — Cost engineering
- Micro-lessons: (a) the token cost model; (b) per-request, per-user, per-feature attribution; (c) prompt caching; (d) model routing (cheap → expensive); (e) context trimming & compression; (f) budget alerts
- **L1 Ground:** price one agent run to the cent, by hand, from the token counts.
- **L2 Build:** cost attribution per agent step from trace attributes; prompt caching with measured savings; a router that sends easy queries to a small model with quality measured on the Week-31 evals; caching layers (semantic cache from Week 28 returns).
- **L3 Edge:** unit economics — cost per successful task, not per call (a cheap model that fails twice is expensive); the cost/quality frontier plotted for your own system; capacity planning and rate-limit handling; the build-vs-buy crossover recomputed with real numbers (Week 26 returns).
- **VIS:** a cost-waterfall chart per agent run; a cost-vs-quality frontier with your configurations plotted; hand-drawn routing-decision sketch.
- **REF:** provider pricing & prompt-caching docs; RouteLLM; FrugalGPT.
- **Hands-on:** cut your system's cost per successful task by ≥50% with no measured quality regression on the Week-31 eval suite; show the before/after table.

### `P4-W32-M4` — Reliability, latency & production operations
- Micro-lessons: (a) SLOs for AI systems; (b) latency budgets (TTFT vs total); (c) streaming for perceived performance; (d) fallbacks & multi-provider; (e) rate limits & queueing; (f) incident response for AI systems
- **L1 Ground:** stream a response and feel the latency difference without changing total time.
- **L2 Build:** an SLO with an error budget, TTFT vs total-latency instrumentation, provider fallback with a circuit breaker (Week 4 returns), queue + back-pressure under rate limits, a runbook for "the model is producing garbage".
- **L3 Edge:** non-determinism makes AI incidents different — you cannot always reproduce; what to log so you can; silent quality degradation after a provider's model update (detected by a scheduled eval run); a full post-mortem of a real AI incident.
- **VIS:** hand-drawn latency-budget breakdown; an animated streaming-vs-buffered perception comparison; an incident timeline sketch.
- **REF:** Google SRE book (SLOs, error budgets); provider status/versioning docs; published LLM incident post-mortems.
- **Hands-on:** run a game day on your Week-30 system: provider outage, rate limiting, a silently degraded model, and a prompt-injection attempt — diagnose all four from telemetry alone.

### `P4-W32-M5` — Deploying & maintaining an AI system
- Micro-lessons: (a) deployment shape for agent systems; (b) prompt/model/config versioning together; (c) staged rollout & shadow mode; (d) continuous evaluation on a schedule; (e) drift & model-update detection; (f) the maintenance burden
- **L1 Ground:** deploy the Week-30 system with Docker Compose; call it over HTTP.
- **L2 Build:** deploy on the Week-24 Kubernetes stack, versioned prompts as config, canary rollout with automated eval gates, scheduled nightly evals against production traffic samples, alerting on quality metrics not just errors.
- **L3 Edge:** the total cost of ownership of an agentic system (evals, traces, prompt maintenance, model deprecations) stated honestly; a deprecation/migration plan for when your model is retired; the organizational contract — who owns the prompts?
- **VIS:** the complete end-to-end system architecture, hand-drawn and then polished — from user request through guardrails, agents, RAG, tools, models, to traces and evals. The course's final "everything you built" poster.
- **REF:** provider model-deprecation policies; MLOps→LLMOps maturity write-ups; the Week-24 K8s references.
- **Hands-on:** produce the one-page architecture poster of your own capstone and present it in 5 minutes.

### `LAB-P4-W32` — **Full observability & cost control**
- `basic`: OTel spans around every LLM call, exported to a local collector.
- `standard`: full instrumentation of the Week-30 system — traces to self-hosted Langfuse, per-step token/cost attribution, prompt versioning, scheduled evals, dashboards, alerts, and a cost-reduction experiment with before/after numbers.
- `hard`: ≥50% cost reduction with no quality regression, a documented game-day, tail-sampling under load, and a published TCO analysis.
- **Ship it:** dashboards + `OPERATIONS.md` + the architecture poster.

---

## `T-P4-CAP` — Graduation Capstone: Distributed AI System
*(3-week overlay, runs alongside Weeks 30–32; defended after Week 32)*

**Brief:** design, build, operate and defend a stateful multi-agent system that solves a real problem — e.g. *Automated Code Reviewer* or *AI SRE Incident Responder*. It must be something you would let a colleague use.

**Required deliverables**
1. **Design document** — problem, users, decisions the system makes, autonomy boundary, blast-radius analysis, architecture diagram (hand-drawn draft + final).
2. **LangGraph multi-agent implementation** with typed state and durable Postgres checkpointing; proven crash-resume.
3. **Hybrid RAG** on pgvector (BM25 + dense + re-ranking) with a published ablation table.
4. **A locally-served fine-tuned SLM** via vLLM for at least one specialized step, with the cost/quality justification versus a hosted model.
5. **Custom MCP server** exposing real capabilities under a documented, tested trust boundary.
6. **Eval suite in CI** — assertions + validated LLM-judge + RAG metrics, gating every merge.
7. **Guardrails** — input moderation, output checks, and a red-team report with ≥15 attempted attacks.
8. **Full observability** — OpenTelemetry → Langfuse, per-step cost attribution, dashboards, alerts.
9. **Deployment** on Kubernetes with staged rollout and scheduled evals.
10. **Operations artifacts** — runbook, TCO analysis, post-mortem from a self-run game day.
11. **Defence** — 25-minute presentation + hostile Q&A covering: why this architecture, what breaks first, what it costs, how you know it works, and what you'd do with 3 more months.

**Rubric (100 pts):** architecture & design rigor 20 · retrieval quality (measured) 15 · agent reliability & durability 15 · evals & measurement 20 · security & guardrails 10 · observability & cost 10 · communication & defence 10.
**Automatic caps:** no eval suite → max 60 · no durability proof → max 70 · unmeasured claims → max 75.

---

## Phase 4 exit checkpoint (graduation)

1. Whiteboard the Transformer forward pass from tokens to logits, from memory.
2. Given a RAG system, diagnose whether a bad answer is a retrieval or generation failure — with evidence.
3. Compute the VRAM and $ cost of a proposed fine-tune or deployment before writing any code.
4. Red-team an agentic system and produce a prioritized mitigation list.
5. Defend the capstone under hostile questioning.
