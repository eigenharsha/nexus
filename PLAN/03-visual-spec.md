# Nexus — Visual & Diagram Production Spec (v1)

**Principle:** in this course the diagram is not decoration for the text — for most concepts *the diagram is the explanation*, and the prose is the caption. If a learner reads only the sketches for a lesson, they should still get the idea.

**Aesthetic:** every diagram looks like a good teacher drew it on a whiteboard while explaining it to one student. Hand-drawn, slightly imperfect, annotated in the margins, with the mistakes crossed out rather than erased. Not corporate. Not clip-art. Not an AI-slick gradient illustration.

---

## 1. Why hand-drawn

Polished vector diagrams read as *reference material* — the eye skims them. Hand-drawn sketches read as *someone thinking* — the eye follows the stroke order and reconstructs the reasoning. For a beginner (Aarav) this is the difference between "I saw a diagram" and "I watched someone work it out." For the professional (Meera) the rough work signals that a real engineer made this, not a content mill.

So: **whiteboard/Excalidraw style is the house style**, not an occasional flourish.

---

## 2. Toolchain

| Purpose | Tool | Output |
|---|---|---|
| Primary authoring | **Excalidraw** (hand-drawn/rough style) | `.excalidraw` (editable) + `.svg` + `.png` |
| Generation from description | the repo's **`/diagram` skill** — English or Mermaid in, `.excalidraw` + SVG + PNG out | triplet, committed together |
| Structural/flow diagrams where hand-drawn adds nothing (dependency graphs, big pipelines) | **Mermaid** (renders natively in Mintlify) | inline code fence |
| Build-up sequences ("frame 1 of 4") | Excalidraw frames exported per-step | `-01.svg` … `-04.svg` |
| True animation | animated SVG (CSS/SMIL) — preferred; short muted MP4/WebM for anything longer than ~8 s | `.svg` / `.mp4` |
| Interactive widgets | small self-contained React/JS in MDX | component |
| Screen recordings (tooling, terminal) | asciinema for terminal, muted MP4 for GUI | embed |

**Rule:** always commit the `.excalidraw` source next to the export. A diagram nobody can edit is technical debt.

---

## 3. The house style (exact values)

```
Font              Excalifont / Virgil (hand-drawn). Never Helvetica/Inter inside a sketch.
Roughness         1–2 (visible wobble; 0 looks fake-clean, 3 is illegible)
Stroke width      2 (bold, whiteboard-marker weight)
Fill style        hachure (cross-hatch) — never solid fills for emphasis

Ink (default)     #1e1e1e
Structure/boxes   #1971c2  (blue)
Correct path      #2f9e44  (green)
Error / warning   #e03131  (red)  — used for "this is the bug", failure modes, trust boundaries
Secondary note    #f08c00  (amber) — margin notes, "remember:", asides
Highlighter       #ffec99 background fill on the one thing that matters most
Paper (light)     #fffdf7
Paper (dark)      #1a1a19 with ink lightened to #e8e6e3
```

**Every diagram ships in both light and dark variants** (Mintlify respects the reader's theme). Export `name.svg` and `name-dark.svg`.

---

## 4. The authenticity rules (what makes it feel real)

These are mandatory, not optional flavour:

1. **Show the rough work.** Keep the intermediate arithmetic, the half-labelled axis, the arrow that was redrawn. Don't clean it up.
2. **Cross out, don't delete.** When a diagram shows a wrong approach first (e.g. "why this naive design fails"), strike it through in red and draw the fix beside it.
3. **Margin notes in the teacher's voice.** Amber, smaller, slightly slanted: *"careful — this is where everyone gets it wrong"*, *"remember week 11?"*, *"this number is the whole point"*.
4. **Circle the key term** the first time it appears in a diagram, the way you'd circle it on a board.
5. **Number the strokes.** Where order matters, use ①②③ so the reader replays the drawing in the right sequence.
6. **Hand-write the numbers.** Real measured values, written in, not tabulated — `~340 ms` next to the slow path, `12×` next to the arrow.
7. **Leave one thing unfinished.** A dangling "…and then?" arrow into the exercise. The sketch should end where the learner's work begins.
8. **No stock icons, no gradients, no drop shadows, no 3-D.** Ever.

**Anti-patterns (auto-reject):** perfectly aligned boxes; a legend nobody needs; five colors with no meaning; an AI-generated "illustration" of a robot; a diagram that just restates the section heading.

---

## 5. The four visual tiers (which concepts get what)

| Tier | What it is | Applies to | Budget |
|---|---|---|---|
| **T1 — Sketch** | one static hand-drawn Excalidraw SVG (light + dark) | **every module, minimum one** | ~30 min each |
| **T2 — Build-up** | 3–5 progressive frames revealed by a stepper, so the diagram assembles as the explanation proceeds | every module whose idea has *steps* (algorithms, protocols, pipelines) | ~1 h each |
| **T3 — Animation** | true motion — animated SVG or short video | the ~40 "hero concepts" listed in §6 | ~3 h each |
| **T4 — Interactive** | the learner changes a parameter and the picture responds | the ~15 concepts where intuition comes from *fiddling* (§7) | ~6 h each |

Every lesson file therefore contains, at minimum: **1× T1 per module**, plus whatever tier the concept earns.

---

## 6. Hero animations (T3) — the shortlist

These are the images the course will be remembered for. Each gets a dedicated task.

| # | Week | Animation | What it must show |
|---|---|---|---|
| A01 | 1 | Stack vs heap during a function call chain | frames pushing/popping; a `malloc`'d block outliving the frame; the dangling pointer turning red |
| A02 | 1 | Merge sort recursion | the array splitting down, then merging back up, with the comparison counter ticking |
| A03 | 1 | Binary search | the window halving, with the invariant written beside each step |
| A04 | 2 | A shell pipeline | text flowing through `grep → sort → uniq`, transforming at each stage |
| A05 | 2 | Git commit DAG | branch → commits → merge vs rebase, side by side, same starting graph |
| A06 | 3 | Names, objects and reference counts | two names binding to one list; mutation seen through both; refcount changing |
| A07 | 4 | Blocking vs async I/O | two timelines: the waiter standing still vs serving other tables |
| A08 | 4 | The event loop | tasks entering the queue, awaiting, resuming — with the loop rotating |
| A09 | 5 | HTTP request lifecycle | DNS → TCP → TLS → request → response, with time cost on each segment |
| A10 | 6 | Pydantic validation | a bad payload hitting the schema and bouncing, field by field |
| A11 | 7 | JOIN types | two tables' rows physically combining, one JOIN type at a time |
| A12 | 8 | B-Tree index lookup | descending the tree, pages loading, vs a full scan racing alongside and losing |
| A13 | 8 | Two concurrent transactions | the lost-update anomaly happening in real time, then the lock preventing it |
| A14 | 9 | NAND → half adder → 16-bit adder | gates composing upward, carry rippling left to right |
| A15 | 9 | Memory hierarchy | a request falling through L1 → L2 → L3 → DRAM → SSD with latency bars to scale |
| A16 | 10 | TCP three-way handshake + retransmission | packets crossing, one lost, the retry firing |
| A17 | 11 | Matrix as a transformation | a shape rotating/shearing under the matrix, with the numbers changing |
| A18 | 11 | Gradient descent on a loss surface | the ball rolling; then too-high LR diverging; then momentum overshooting |
| A19 | 11 | SVD / low-rank approximation | an image degrading as rank drops — the visual that makes LoRA obvious later |
| A20 | 12 | Central limit theorem | sample means piling into a normal curve |
| A21 | 13 | Hash table insert & collision | keys hashing into buckets, a chain forming, then a resize rehashing everything |
| A22 | 14 | Dijkstra | the frontier expanding across the graph, distances updating |
| A23 | 14 | DP table filling | the grid populating cell by cell with the recurrence shown |
| A24 | 15 | Incremental pipeline run | new rows only, merging into the target; the watermark advancing |
| A25 | 17 | Logistic regression training | the decision boundary rotating into place as loss falls |
| A26 | 18 | Gradient boosting | residuals shrinking as each tree is added |
| A27 | 19 | Threshold sliding on a PR curve | confusion matrix updating live as the threshold moves |
| A28 | 21 | **Backpropagation** | forward pass, loss, then gradients flowing backwards through the graph, weights nudging |
| A29 | 22 | Convolution | the kernel sliding over the image, feature map filling in |
| A30 | 24 | Kubernetes HPA | load rising, pods spawning, latency recovering — with the lag windows marked |
| A31 | 25 | BPE merges | the merge table growing; a word's tokenization changing as merges apply |
| A32 | 25 | **Self-attention** | the attention matrix filling token by token, causal mask blocking the future — *the single most important animation in the course* |
| A33 | 25 | KV cache | the cache growing per generated token; recompute-vs-cache shown side by side |
| A34 | 26 | Quantization | a float's bits being squeezed 32 → 16 → 8 → 4, with the error accumulating |
| A35 | 26 | LoRA | the frozen weight matrix with the thin B·A path lighting up; parameter counts ticking |
| A36 | 27 | Chunking strategies | one document split three ways, the retrieved unit highlighted in each |
| A37 | 27 | **HNSW search** | the layered graph, a query entering at the top layer and hopping greedily down |
| A38 | 28 | Hybrid fusion | two ranked lists merging via RRF, the right answer climbing to #1 |
| A39 | 29 | Agent ReAct loop | thought → action → observation cycling, the scratchpad filling |
| A40 | 30 | Checkpoint & resume | the graph executing, the process dying, and resuming from the last checkpoint |
| A41 | 31 | Prompt injection | a hidden instruction inside a retrieved document being read and obeyed — with the trust boundary breach in red |
| A42 | 32 | A distributed trace | spans nesting into a waterfall, with cost accumulating per span |

## 7. Interactive widgets (T4) — the shortlist

| Week | Widget | The parameter the learner moves |
|---|---|---|
| 1 | Big-O grower | n, and watch operation counts diverge |
| 11 | Gradient descent playground | learning rate, momentum, starting point |
| 11 | Vector similarity | drag two vectors, watch cosine vs Euclidean disagree |
| 12 | Sampling & CLT | sample size, distribution shape |
| 17 | Bias-variance | polynomial degree on a fixed dataset |
| 19 | Threshold explorer | decision threshold → confusion matrix + cost |
| 21 | Neural net playground | layers, width, activation, on a 2-D dataset |
| 22 | Convolution kernel editor | edit the 3×3 kernel, see the filtered image |
| 25 | Tokenizer explorer | type text, see tokens and count across tokenizers |
| 25 | Attention inspector | pick a token, see what it attends to |
| 25 | Sampling parameters | temperature, top-k, top-p on a real distribution |
| 26 | VRAM calculator | model size, precision, batch, context → memory + "fits on your GPU?" |
| 27 | HNSW parameter explorer | M, ef → recall vs latency |
| 28 | RAG cost calculator | chunk size, top-k, re-rank depth, model → $/query and latency |
| 32 | Cost attribution | token counts per step → cost waterfall |

---

## 8. Per-lesson visual requirements (added to the lesson template)

Section **2. The mental model** must open with the module's T1 sketch.
A new mandatory section is inserted before Resources:

```
## 9b. The whiteboard
   - The full sketch set for this module (T1 always; T2/T3/T4 where earned)
   - "Draw it yourself" prompt: reproduce this diagram from memory, then compare
   - Blank version of the key diagram (labels removed) as a self-test
```

**"Draw it yourself" is a graded activity.** Every week's assessment includes reproducing one diagram from memory — it is the cheapest, highest-retention exercise in the whole course.

---

## 9. Production workflow per diagram

1. Write the one sentence the diagram must make obvious. If you can't, don't draw it.
2. Sketch it *badly* first, by hand or in Excalidraw, with the rough work visible.
3. Run it past the "Aarav test": would a beginner know what to look at first?
4. Apply the house style values (§3) and the authenticity rules (§4).
5. Export light + dark SVG, commit the `.excalidraw` source alongside.
6. Write the alt-text — a full sentence describing what the diagram shows, for accessibility and for search.
7. Register it in `assets/diagram-index.md` with its ID, week, tier and source file.

---

## 10. Accessibility & performance

- Every diagram needs descriptive alt text (not "diagram of attention").
- Never encode meaning in colour alone — pair red with a ✗, green with a ✓, and label the lines.
- SVG preferred over PNG (scales, small, themeable). Target < 200 KB per sketch, < 2 MB per animation.
- Animations must not autoplay-loop distractingly: play once on scroll into view, with a replay button; respect `prefers-reduced-motion`.
- Every animation has a static fallback frame that carries the same information.
