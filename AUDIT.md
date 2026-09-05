# Number Provenance Audit — final record

Every numeric claim in the 160 modules was audited and labelled. This file records the outcome
so the result is inspectable rather than merely asserted. Learner-facing statement:
`start/about-the-numbers.mdx`. Authoring rule: `PLAN/00-content-spec.md` §5c.

## Result across all 34 weeks

| Class | Claim sites | Covers |
|---|---|---|
| **Measured** | ~1,150 | Weeks 1–20 and 29 in full; local Docker, image sizes, `kind` clusters, Ollama on Apple Silicon |
| **Reference figure** | ~335 | Every CUDA GPU (RTX 4090, A100, H100, A10G, T4), every named cloud instance, weeks 27–28 retrieval quality, week 23 CI, week 25 tokenizers |
| **Derived** | ~61 | VRAM arithmetic, KV-cache bytes/token, LoRA parameter counts, roofline ridge points, BM25, RRF, Amdahl, Little's law, IEEE-754 and UTF-8 results |
| **Cited finding** | 11 | NVIDIA SyncBN overhead, Valgrind's 10–50× slowdown, Selivanov's uvloop 2–4×, Anthropic contextual retrieval, Kwon et al. KV waste, Elor & Averbuch-Elor on SMOTE |
| **Modelled composite** | 10 | First-person operating histories in weeks 30–32, and the week 19 war stories |

**~400 claims relabelled · 7 corrections upward · 1 broken cross-reference fixed · 148 provenance
links across 131 files.**

### What was deliberately *not* labelled

Seventy war stories in Phases 3 and 4 are third-person industry anecdotes — "a payments team",
"an ad-tech team" — making no first-person claim about our own systems. Under the line drawn
during the audit these are legitimate teaching devices and carry no label. Labelling seventy
honest anecdotes would dilute a label that currently means something specific. Only *first-person*
production histories were a problem, and those are relabelled.

## Why the audit happened

Eight authoring agents wrote ~1.47M words. One described its own benchmark machines in its final
report as *"consistent invented reference hardware"*. A check across the site then found ~255
claims phrased "Measured on…" citing GPUs and cloud instances that do not exist here — the build
ran entirely on a macOS arm64 laptop with no CUDA and no cloud access.

## Two failure modes found

1. **Invented hardware.** Detectable by inspection: check what is installed.
2. **Invented elapsed time.** *"Measured over four months"*, *"three detections in eight months"*,
   *"14 rollouts in five months"* — for a system never deployed. Not detectable by checking
   hardware, and more persuasive than the first, because a production history reads like earned
   experience.

## Evidence that survives in the repo

| Artifact | Backs |
|---|---|
| `evidence/phase-1-w05-08-measurements.md` | ~80 claims with reproduction commands; verbatim PostgreSQL SSI and deadlock output |
| `evidence/phase-2-w13-16/` | 60 benchmark scripts and result files |
| `/private/tmp/nexus-env`, `nexus-old`, `nexusvenv`, `nexus/pytool/.venv*` | Authoring environments; version strings match cited figures |
| `~/scikit_learn_data/` | Dataset caches timestamped inside the authoring window |

## Corrections made *upward*

Four claims were strengthened, not weakened: UTF-8 byte counts, the `0.1+0.2` ULP example, an
IEEE-754 error-accumulation table, and a ResNet-18 FLOP count. All are fixed by standards or
arithmetic, so "measured" was understating them — a reader can reproduce the digits, not merely
the magnitude.

## Three procedural errors by the audit itself, and their fixes

1. **Too few environments searched.** A week-18 downgrade was ordered on a two-venv search; ten
   existed. `lightgbm 4.7.0` and `umap-learn 0.5.12` were in `/private/tmp/nexus-env` at exactly
   the cited versions. Reverted.
2. **Too shallow a search.** `find / -maxdepth 5 -type d -name site-packages` returns 3 hits;
   `-maxdepth 10` returns 96. Depth is the whole game.
3. **An observation that inverted its meaning.** Week 20's pickle-fragility module *requires* an
   old-version environment, so a version mismatch there is evidence *for* a measurement.

**The rule held every time; the inputs failed every time.** Which is what the course tells
students about benchmarks.
