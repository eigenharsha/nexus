# Labs

One lab a week, thirty-two weeks. Each is written as a **ticket** — the problem the way a
colleague would hand it to you — and has **three tracks** cut from the same problem, so a
beginner and a senior engineer can do the same lab and both get their money's worth.

There is no instructor. `make verify` is the grader, and `make contract` is what proves the
grader is honest.

```bash
cd labs/p1/week-01
make help                    # what this lab can do
cat standard/SPEC.md         # the acceptance criteria
$EDITOR starter/             # your work goes here
make verify                  # TRACK=standard against starter/ — red until you finish
make verify TRACK=basic      # the scaffolded track
make verify IMPL=solution    # the reference implementation — green
make contract                # asserts solution green AND starter red
make bench                   # where the lab has a performance target
make ship                    # prints this lab's ship-it checklist
```

## The three-track model

The same ticket, three altitudes. You can climb mid-lab — the tests for the lower track keep
passing, because `make verify TRACK=hard` runs basic + standard + hard.

| Track | You are given | You write | Who starts here |
|---|---|---|---|
| `basic` | ~60% of the code, TODOs marked with a one-line hint above each | the marked TODOs | you have not done this before |
| `standard` | a spec and a test suite, nothing else | the implementation, from an empty file | you ship code for a living |
| `hard` | the same spec plus a constraint the `standard` solution **fails** | a better implementation, with numbers | `standard` is green and you want the interview story |

The `hard` track is never "the same thing but longer". It always adds a constraint that
breaks the obvious solution: a memory ceiling that defeats `asyncio.gather`, a load factor
that defeats a naive hash table, a 64 MB budget that defeats `malloc(n * sizeof(int))`.

## How `make verify` works

Every lab has the same Makefile, which is four lab-specific lines plus `include lab.mk`.
`lab.mk` is the shared engine and dispatches on `LANG`:

| `LANG` | Runner | Notes |
|---|---|---|
| `python` | `pytest`, with the implementation dir first on `PYTHONPATH` | markers `basic` / `standard` / `hard`, cumulative |
| `c` | `tests/nexus_test.h`, a 90-line dependency-free harness | always built with `-Wall -Wextra -fsanitize=address,undefined` |
| `shell` | `bats`, or the bundled `bin/bats-lite.sh` when bats is absent | so a missing tool never fails your lab for you |
| `hdl` | `tests/run_hdl.py`, driving the Nand2Tetris hardware simulator | needs the simulator; the error message says where to get it |

Two variables control everything:

- **`TRACK`** — `basic`, `standard` (default) or `hard`.
- **`IMPL`** — which directory is under test: `starter` (default, your work) or `solution`.

The interpreter is found by walking up to the directory containing `bootstrap.sh` and using
its `.venv` if there is one. You never have to activate anything.

### `make contract`

A test suite that passes against an empty starter is not a test suite. `make contract`
asserts both halves in one command:

```
$ make contract
==> contract check: LAB-P1-W01 track=standard
  PASS  solution/ is green
  PASS  starter/ is red (as it must be)
contract holds
```

If `make verify IMPL=solution` is red on a fresh clone, that is a bug in the course, not in
your machine. Open an issue with the output of `./bootstrap.sh --check`.

## The rubric

Every lab is scored 0–3 on four dimensions, 12 points total. `make verify` decides
Correctness for you; you grade the other three honestly, **before** opening `solution/`.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Correctness** | `make verify` fails | happy path only | edge cases handled | adversarial inputs handled |
| **Code quality** | it works | readable | tested and typed | a reviewer would approve unchanged |
| **Performance** | never measured | measured once | meets the stated budget | beats the budget, with evidence |
| **Explanation** | none | a README exists | reasoning documented | trade-offs defended in writing |

Two rules that decide most of the score:

1. **You cannot score above 1 on Performance without a number in your README.** "It felt
   fast" is a 0. Every `hard` track has a budget; state what you measured against it.
2. **A 3 on Explanation means you wrote down the option you rejected and why.** That
   paragraph is the highest-value thing in your portfolio repo and it is the one everybody
   skips. It is also, in practice, what most interviews actually test.

Each lab's `RUBRIC.md` says what those levels mean for that specific lab.

## Ship it

Every lab ends in something committed, deployed, containerized or measured. A lab never ends
at "it printed the right thing". `make ship` prints the checklist for the lab you are in.

At least one lab per week must be publishable to GitHub with a README you would link from a
CV. That is the actual output of this course: not thirty-two green test runs, but a dozen
repositories you can talk about for forty-five minutes each.

## Which labs ship a worked solution

Six labs ship a complete, executed `starter/` + `solution/` + test suite, with real measured
output pasted into their README. They are the reference for what the other twenty-six should
become, and they are the ones to read first if you want to see the intended shape of a lab.

| Week | Lab | What is verified |
|---|---|---|
| 01 | Sorting & Search Toolkit in C | 562 assertions, ASan/UBSan clean, external merge sort under a 128 KB budget; measured log-log exponents (selection 1.930, merge 1.125) |
| 03 | `ledger` typed Python library | 25 tests, `mypy --strict` clean, `ruff` clean, `hypothesis` invariants over 3 storage backends |
| 04 | Async concurrent downloader | 19 tests against a local deterministic flaky-server fixture; sequential vs threads vs asyncio benchmark |
| 13 | `pycollections` + benchmark harness | 21 tests; measured load-factor curve, heapify vs push, growth-factor trade, count-min error vs bound |
| 17 | `scratchml` regression from NumPy | 24 tests; coefficients match scikit-learn to 8.5e-14 (OLS) and 2.3e-4 (logistic) |
| 21 | `nanograd` autograd engine | 29 tests; gradcheck < 1e-6 on 13 ops; **97.3% on real MNIST in 17 s of pure NumPy**; checkpointing saves 88% of the retained graph |

The other twenty-six ship the ticket, the three track specs with precise acceptance criteria,
a working Makefile, and a test skeleton with one named, documented test per criterion. Their
`make verify` is red out of the box, which is the correct starting state for a lab — but the
assertions and the reference implementation are not written yet, and their READMEs say so.

## The full index


### Phase 1 · Foundations

| Week | Lab | Language | Time box | Status |
|---|---|---|---|---|
| 01 | [`LAB-P1-W01` — Sorting & Search Toolkit in C](p1/week-01/) | c | 8-10 h | **verified** |
| 02 | [`LAB-P1-W02` — Self-Reporting System Monitor](p1/week-02/) | shell | 6-8 h | scaffold |
| 03 | [`LAB-P1-W03` — `ledger` — a typed, tested, packaged Python library](p1/week-03/) | python | 8-10 h | **verified** |
| 04 | [`LAB-P1-W04` — Async Concurrent Downloader](p1/week-04/) | python | 8-10 h | **verified** |
| 05 | [`LAB-P1-W05` — Static frontend against a public API](p1/week-05/) | python | 6-8 h | scaffold |
| 06 | [`LAB-P1-W06` — "Resume Tailor" full-stack service](p1/week-06/) | python | 10-12 h | scaffold |
| 07 | [`LAB-P1-W07` — E-commerce schema & analytics suite](p1/week-07/) | python | 10-12 h | scaffold |
| 08 | [`LAB-P1-W08` — Concurrency-safe checkout service](p1/week-08/) | python | 12-14 h | scaffold |

### Phase 2 · Systems & Data

| Week | Lab | Language | Time box | Status |
|---|---|---|---|---|
| 09 | [`LAB-P2-W09` — Build the Hack computer's ALU & memory](p2/week-09/) | hdl | 10-12 h | scaffold |
| 10 | [`LAB-P2-W10` — Multi-threaded TCP chat server (raw sockets)](p2/week-10/) | python | 10-12 h | scaffold |
| 11 | [`LAB-P2-W11` — `nanomath`: a from-scratch math library](p2/week-11/) | python | 10-12 h | scaffold |
| 12 | [`LAB-P2-W12` — A/B test analyzer + Bayes classifier](p2/week-12/) | python | 8-10 h | scaffold |
| 13 | [`LAB-P2-W13` — `pycollections`: structures from scratch + benchmark harness](p2/week-13/) | python | 10-12 h | **verified** |
| 14 | [`LAB-P2-W14` — 15 medium problems + route planner](p2/week-14/) | python | 12-15 h | scaffold |
| 15 | [`LAB-P2-W15` — Incremental financial-records pipeline](p2/week-15/) | python | 12-14 h | scaffold |
| 16 | [`LAB-P2-W16` — Automated EDA dashboard](p2/week-16/) | python | 10-12 h | scaffold |

### Phase 3 · Machine Learning

| Week | Lab | Language | Time box | Status |
|---|---|---|---|---|
| 17 | [`LAB-P3-W17` — `scratchml`: regression & classification from NumPy](p3/week-17/) | python | 10-12 h | **verified** |
| 18 | [`LAB-P3-W18` — Customer churn: end-to-end tabular modelling](p3/week-18/) | python | 12-14 h | scaffold |
| 19 | [`LAB-P3-W19` — Evaluation harness](p3/week-19/) | python | 10-12 h | scaffold |
| 20 | [`LAB-P3-W20` — Credit-card fraud detection](p3/week-20/) | python | 12-14 h | scaffold |
| 21 | [`LAB-P3-W21` — `nanograd`: autograd + neural net from scratch](p3/week-21/) | python | 12-15 h | **verified** |
| 22 | [`LAB-P3-W22` — Blood-cell image classifier (>=90% test accuracy)](p3/week-22/) | python | 12-14 h | scaffold |
| 23 | [`LAB-P3-W23` — Containerized prediction service → serverless](p3/week-23/) | python | 12-14 h | scaffold |
| 24 | [`LAB-P3-W24` — Kubernetes model-serving cluster](p3/week-24/) | python | 12-15 h | scaffold |

### Phase 4 · Generative AI

| Week | Lab | Language | Time box | Status |
|---|---|---|---|---|
| 25 | [`LAB-P4-W25` — `minbpe` + `nanoGPT` from scratch](p4/week-25/) | python | 14-16 h | scaffold |
| 26 | [`LAB-P4-W26` — QLoRA fine-tune for strict structured output](p4/week-26/) | python | 14-16 h | scaffold |
| 27 | [`LAB-P4-W27` — 1,000-PDF retrieval system on pgvector/HNSW](p4/week-27/) | python | 14-16 h | scaffold |
| 28 | [`LAB-P4-W28` — Production hybrid RAG](p4/week-28/) | python | 14-16 h | scaffold |
| 29 | [`LAB-P4-W29` — Agent from scratch + custom MCP server](p4/week-29/) | python | 14-16 h | scaffold |
| 30 | [`LAB-P4-W30` — Incident Auto-Remediation System](p4/week-30/) | python | 16-18 h | scaffold |
| 31 | [`LAB-P4-W31` — Eval CI pipeline + guardrail layer](p4/week-31/) | python | 14-16 h | scaffold |
| 32 | [`LAB-P4-W32` — Full observability & cost control](p4/week-32/) | python | 14-16 h | scaffold |

## Creating a new lab

```bash
templates/lab/new-lab.sh \
    --id LAB-P1-W01 --week 1 --phase p1 --lang c \
    --title "Sorting & Search Toolkit in C" \
    --timebox "8-10 h"
```

It copies `templates/lab/`, substitutes the placeholders, and removes the files that do not
apply to the chosen language. Then fill in the `{{TICKET}}`, `{{...}}_CRITERIA` and
`{{SHIP}}` placeholders and write `tests/` and `solution/` until `make contract` passes.

`templates/lab/` is the canonical layout:

```
templates/lab/
├── README.md          the ticket, with placeholders
├── RUBRIC.md          the 0-3 rubric
├── Makefile           four lab-specific lines + include lab.mk
├── lab.mk             the shared verify / contract / bench engine
├── pytest.ini         track markers
├── new-lab.sh         the stamper
├── basic/SPEC.md      standard/SPEC.md      hard/SPEC.md
├── starter/           solution/
├── tests/             conftest.py · nexus_test.h (C) · test skeleton
└── bin/bats-lite.sh   a bats subset, for when bats is not installed
```

## If you get stuck

1. Twenty minutes stuck, then read the *Common mistakes* table in the week's module pages.
2. Then re-read Layer 1 of the module the lab tests.
3. Then `solution/`, one function at a time — and delete-and-rewrite the function you read.

Reading a solution before you have a failing attempt of your own converts a six-hour skill
into a six-minute read. The tests cannot tell the difference; an interviewer can.
