#!/usr/bin/env python3
"""
make_flagships.py - hand-authored specs for the flagship sketches.

These are the diagrams the course will be remembered for (PLAN/03-visual-spec.md
section 6), so their geometry is written by hand rather than compiled out of
prose. Running this writes tools/specs/*.json; build_diagrams.py then renders
them and they take precedence over any auto-compiled block with the same id.

  python3 tools/make_flagships.py && python3 tools/build_diagrams.py
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "specs"
SPECS: dict[str, dict] = {}


HERO = {   # PLAN/03-visual-spec.md section 6: hero id -> week
    "a01-stack-heap": ("A01", 1), "a03-binary-search": ("A03", 1),
    "a05-git-dag": ("A05", 2), "a07-blocking-vs-async": ("A07", 4),
    "a12-btree-vs-scan": ("A12", 8), "a15-memory-hierarchy": ("A15", 9),
    "a18-gradient-descent": ("A18", 11), "a28-backprop": ("A28", 21),
    "a32-attention": ("A32", 25), "a35-lora": ("A35", 26),
    "a37-hnsw": ("A37", 27), "a41-prompt-injection": ("A41", 31),
}


def spec(sid, title, alt, w, h, elements, tier="T1"):
    hero, week = HERO.get(sid, (None, None))
    SPECS[sid] = {"id": sid, "title": title, "alt": alt, "width": w,
                  "height": h, "tier": tier, "hero": hero, "week": week,
                  "elements": elements}


def box(i, x, y, w, h, label, color="structure", **kw):
    return dict(type="box", id=i, x=x, y=y, w=w, h=h, label=label,
                color=color, **kw)


def arrow(i, x1, y1, x2, y2, **kw):
    return dict(type="arrow", id=i, x1=x1, y1=y1, x2=x2, y2=y2, **kw)


def note(i, x, y, text, w=230, **kw):
    return dict(type="note", id=i, x=x, y=y, text=text, w=w, **kw)


def circled(i, x, y, text, ring="structure", **kw):
    return dict(type="circled", id=i, x=x, y=y, text=text, ring=ring, **kw)


def text(i, x, y, s, size=16, **kw):
    return dict(type="text", id=i, x=x, y=y, text=s, size=size, **kw)


def badge(i, x, y, n):
    return dict(type="badge", id=i, x=x, y=y, n=n)


# ===========================================================================
# A32 - self-attention with a causal mask   (the most important one)
# ===========================================================================
def a32_attention():
    toks = ["the", "cat", "sat", "down"]
    cell, x0, y0 = 62, 300, 190
    els = [
        text("hdr", 470, 92, "one 4-word sentence, one attention matrix", 17,
             color="muted"),
    ]
    # the sentence along the top, as query/key headers
    for j, t in enumerate(toks):
        els.append(text(f"k{j}", x0 + cell * j + cell / 2, y0 - 14, t, 18,
                        color="structure", bold=True, rotate=0))
    for i, t in enumerate(toks):
        els.append(text(f"q{i}", x0 - 12, y0 + cell * i + cell * 0.62, t, 18,
                        color="structure", bold=True, anchor="end", rotate=0))
    els.append(text("kl", x0 + cell * 2, y0 - 44, "KEYS  (what I can look at)",
                    15, color="muted"))
    els.append(text("ql", x0 - 126, y0 + cell * 2, "QUERIES", 15,
                    color="muted", rotate=-90))

    # real-ish post-softmax weights, causal
    weights = [[1.00, 0, 0, 0],
               [0.38, 0.62, 0, 0],
               [0.21, 0.44, 0.35, 0],
               [0.12, 0.29, 0.24, 0.35]]
    for i in range(4):
        for j in range(4):
            x, y = x0 + cell * j, y0 + cell * i
            allowed = j <= i
            els.append(box(f"c{i}{j}", x, y, cell, cell, "",
                           color="ink" if allowed else "error", width=1.4,
                           fill="hachure" if allowed else None,
                           fill_color="highlight" if weights[i][j] > 0.3
                           else "structure",
                           fill_gap=max(4, 13 - weights[i][j] * 12)))
            if allowed:
                els.append(text(f"w{i}{j}", x + cell / 2, y + cell * 0.62,
                                f"{weights[i][j]:.2f}", 16, rotate=0))
            else:
                els.append(dict(type="crossout", id=f"m{i}{j}", x=x + 10,
                                y=y + 10, w=cell - 20, h=cell - 20,
                                color="error"))
    # the mask itself, drawn as one heavy red staircase over the upper triangle
    els.append(dict(type="path", id="mask", color="error", width=3.0,
                    smooth=False, points=[
                        [x0, y0], [x0 + cell, y0], [x0 + cell, y0 + cell],
                        [x0 + cell * 2, y0 + cell],
                        [x0 + cell * 2, y0 + cell * 2],
                        [x0 + cell * 3, y0 + cell * 2],
                        [x0 + cell * 3, y0 + cell * 3],
                        [x0 + cell * 4, y0 + cell * 3],
                        [x0 + cell * 4, y0]]))
    els += [
        text("masklbl", 560, 128,
             "CAUSAL MASK - set to -inf BEFORE softmax", 17, color="error",
             bold=True, w=420),
        badge("b1", 216, y0 + cell * 0.5, 1),
        badge("b2", 216, y0 + cell * 1.5, 2),
        badge("b3", 216, y0 + cell * 2.5, 3),
        badge("b4", 216, y0 + cell * 3.5, 4),
        text("rowsum", x0 + cell * 4 + 28, y0 + cell * 2 + 10,
             "every row sums to 1.0", 15, color="muted", anchor="start", w=140),
        note("n1", 34, 236,
             "row i can only look LEFT and at itself. That one triangle of "
             "-inf is the whole difference between a translator and a "
             "next-token predictor.", w=176, leader=[250, 236]),
        note("n2", 34, 430,
             "\"sat\" attends 0.44 to \"cat\" - the subject. Nobody told it "
             "to.", w=176, leader=[292, 384]),
        circled("c1", 150, 560, "causal mask", ring="error", size=19),
        text("qkv", 520, 550,
             "scores = QKᵀ / √d_k  →  mask  →  softmax  →  × V", 18,
             bold=True, w=400),
        text("dk", 520, 582, "d_k = 64, so √d_k = 8 - without it the softmax "
                             "saturates and the gradients die", 14,
             color="muted", w=380),
        arrow("open", 600, 612, 720, 630, dashed=True, color="note",
              label="...now do it for 12 heads at once"),
    ]
    spec("a32-attention",
         "Self-attention: the matrix and the causal mask",
         "A four-by-four attention matrix for the sentence 'the cat sat down'. "
         "Each cell in the lower triangle carries its post-softmax weight, "
         "hachured more densely where the weight is larger; the upper triangle "
         "is crossed out in red and enclosed by a heavy red staircase labelled "
         "causal mask, showing that each token can attend only to itself and "
         "the tokens before it.",
         1000, 660, els, tier="T3")


# ===========================================================================
# A28 - backpropagation through a tiny graph
# ===========================================================================
def a28_backprop():
    y, bw, bh, pitch = 210, 132, 76, 172
    nodes = [("x", "x = 2.0", 70), ("mul", "· w\nw = 3.0", 242),
             ("add", "+ b\nb = 1.0", 414), ("relu", "ReLU", 586),
             ("loss", "L = (ŷ - y)²\n= 4.0", 758)]
    els = [text("fw", 480, 128, "FORWARD - numbers flow right →", 19,
                color="structure", bold=True)]
    for i, (nid, label, x) in enumerate(nodes):
        els.append(box(f"n-{nid}", x, y, bw, bh, label,
                       color="structure" if i < 4 else "error", size=17))
        if i:
            els.append(arrow(f"f{i}", nodes[i - 1][2] + bw + 3, y + bh / 2,
                             x - 4, y + bh / 2, color="structure"))
    for i, v in enumerate(["2.0", "6.0", "7.0", "7.0"]):
        els.append(text(f"v{i}", nodes[i][2] + bw / 2, y - 14, v, 18,
                        color="structure", bold=True, rotate=0))

    # backward pass: long green arrows under the graph, right to left
    by = y + bh + 62
    els.append(text("bw", 480, by + 116, "← BACKWARD - gradients flow left",
                    19, color="correct", bold=True))
    grads = ["∂L/∂ŷ = 4.0", "∂L/∂z = 4.0 (ReLU passes it)",
             "∂L/∂b = 4.0", "∂L/∂w = 4.0 · x = 8.0"]
    for i in range(4):
        x1 = nodes[4 - i][2] + bw / 2
        x2 = nodes[3 - i][2] + bw / 2
        els.append(arrow(f"g{i}", x1, by, x2 + 6, by, color="correct",
                         curve=0.10, width=2.4))
        els.append(text(f"gl{i}", (x1 + x2) / 2, by + (36 if i % 2 == 0 else 62),
                        grads[i], 15, color="correct", w=168, rotate=0))
        els.append(badge(f"gb{i}", x1 + 6, by - 28, i + 1))
    els += [
        arrow("upd", 308, by - 18, 308, y + bh + 6, color="correct",
              width=2.4),
        text("updl", 200, by - 34, "w ← 3.0 - 0.1·8.0 = 2.2", 16,
             color="correct", bold=True, w=210, rotate=0),
        note("n1", 48, 540,
             "the backward pass costs ~2x the forward pass and reuses every "
             "value the forward pass computed. That is why activations sit in "
             "memory, and why batch size is the first thing that blows up "
             "your VRAM.", w=250),
        note("n2", 700, 540,
             "ReLU's gradient is 1 or 0. Nothing in between. When it is 0 that "
             "unit learns NOTHING this step - the dead-ReLU problem.", w=240),
        circled("c1", 470, 512, "chain rule", ring="correct", size=20),
        text("cr", 470, 566,
             "∂L/∂w = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂w   —   multiply along the path, "
             "sum over paths", 15, color="muted", w=380),
        arrow("open", 420, 646, 548, 662, dashed=True, color="note",
              label="...now two layers, and 4 paths"),
    ]
    spec("a28-backprop",
         "Backpropagation through a tiny graph",
         "A five-node computation graph drawn left to right in blue for the "
         "forward pass with the intermediate values written above each node, "
         "and long green arrows running right to left underneath carrying the "
         "partial derivatives, ending in a weight update that moves w from "
         "3.0 to 2.2.",
         1000, 640, els, tier="T3")


# ===========================================================================
# A37 - HNSW: the layered graph and the greedy descent
# ===========================================================================
def a37_hnsw():
    els = []
    layers = [
        ("Layer 2 - 3 nodes", 190, [(220, 190), (500, 175), (770, 200)]),
        ("Layer 1 - 9 nodes", 330, [(150, 330), (280, 315), (400, 345),
                                    (520, 320), (640, 340), (770, 325)]),
        ("Layer 0 - ALL 100k nodes", 490,
         [(120, 490), (200, 505), (285, 480), (365, 500), (445, 485),
          (525, 505), (605, 483), (685, 500), (765, 487), (845, 500)]),
    ]
    for li, (label, ly, pts) in enumerate(layers):
        els.append(dict(type="line", id=f"sep{li}", x1=70, y1=ly - 52,
                        x2=930, y2=ly - 52, dashed=True, color="muted",
                        width=1.4))
        els.append(text(f"ll{li}", 78, ly - 62, label, 15, color="muted",
                        anchor="start", rotate=0))
        for k in range(len(pts) - 1):
            els.append(dict(type="line", id=f"e{li}-{k}", x1=pts[k][0],
                            y1=pts[k][1], x2=pts[k + 1][0], y2=pts[k + 1][1],
                            color="muted", width=1.3))
        if li == 2:
            for k in range(0, len(pts) - 2):
                els.append(dict(type="line", id=f"x{li}-{k}", x1=pts[k][0],
                                y1=pts[k][1], x2=pts[k + 2][0],
                                y2=pts[k + 2][1], color="muted", width=1.1,
                                curve=0.14))
        for k, (px, py) in enumerate(pts):
            els.append(dict(type="ellipse", id=f"n{li}-{k}", cx=px, cy=py,
                            rx=15, ry=13, color="structure", width=1.6))

    # the query's greedy path down the layers
    path = [(500, 175), (280, 315), (400, 345), (365, 500), (445, 485)]
    for k in range(len(path) - 1):
        els.append(arrow(f"hop{k}", path[k][0], path[k][1] + 14,
                         path[k + 1][0], path[k + 1][1] - 14, color="error",
                         width=2.6, curve=0.12))
        els.append(badge(f"hb{k}", (path[k][0] + path[k + 1][0]) / 2 - 26,
                         (path[k][1] + path[k + 1][1]) / 2, k + 1))
    els += [
        arrow("enter", 500, 100, 500, 156, color="error", width=2.6),
        text("q", 500, 88, "query vector enters at the TOP", 17, color="error",
             bold=True),
        dict(type="ellipse", id="hit", cx=445, cy=485, rx=26, ry=22,
             color="correct", width=2.6),
        text("hitl", 445, 545, "nearest neighbour", 15, color="correct",
             rotate=0),
        note("n1", 60, 130,
             "the top layer is the motorway: few nodes, huge jumps. Layer 0 is "
             "the last mile. Same trick as a skip list.", w=200),
        note("n2", 60, 590,
             "greedy means it can be WRONG. ef_search is you paying latency for "
             "recall - measure both or you are guessing.", w=280),
        circled("c1", 620, 600, "greedy descent", size=19),
        text("nums", 820, 585, "100k vectors\n~12 hops\n1.9 ms p50\nrecall@10 "
                               "0.94 at ef=64", 15, color="muted", w=170),
        arrow("open", 700, 640, 830, 656, dashed=True, color="note",
              label="...what breaks at 10M?"),
    ]
    spec("a37-hnsw",
         "HNSW: hopping down the layers",
         "A three-layer navigable small-world graph. A query enters at the "
         "sparse top layer and follows numbered red hops greedily down through "
         "the denser layers to layer zero, where the nearest neighbour is "
         "ringed in green.",
         1000, 690, els, tier="T3")


# ===========================================================================
# A01 - stack, heap and the dangling pointer
# ===========================================================================
def a01_stack_heap():
    els = [
        text("sl", 200, 120, "STACK  (grows down, freed automatically)", 16,
             color="muted"),
        text("hl", 700, 120, "HEAP  (you own it)", 16, color="muted"),
        box("f1", 90, 140, 230, 62, "main()", color="structure"),
        box("f2", 90, 214, 230, 62, "parse_line()", color="structure"),
        box("f3", 90, 288, 230, 62, "make_buf()", color="structure"),
        text("sp", 344, 300, "← stack pointer", 15, color="muted",
             anchor="start"),
        box("heap", 600, 250, 230, 80, "malloc(1024)\n0x7f3a...c40",
            color="correct", fill="hachure", fill_color="correct"),
        badge("b1", 70, 320, 1),
        badge("b2", 560, 290, 2),
        badge("b3", 70, 246, 3),
        badge("b4", 500, 178, 4),
        arrow("a1", 324, 318, 592, 292, color="correct",
              label="returns a pointer", label_y=290),
        dict(type="crossout", id="pop", x=90, y=288, w=230, h=62,
             color="error"),
        text("popl", 205, 372, "make_buf returns → its frame is GONE", 15,
             color="error"),
        arrow("a2", 324, 240, 592, 276, color="error", width=2.6, curve=-0.12,
              label="buf still holds 0x7f3a...c40", label_y=214),
        text("ok", 700, 350, "the 1024 bytes are still perfectly fine", 15,
             color="muted"),
        note("n1", 60, 430,
             "the memory did not disappear. The NAME for it did - and nothing "
             "will ever free it. Both halves of that sentence are a different "
             "bug: use-after-free and a leak.", w=300),
        note("n2", 620, 420,
             "Python does this for you with refcounts (week 3). C does not. "
             "Rust makes the compiler check it. Same picture, three answers.",
             w=250),
        circled("c1", 470, 490, "dangling pointer", ring="error", size=20),
        text("free", 470, 545, "who calls free()?  the caller. Write it in the "
                               "docstring or it will not happen.", 15,
             color="muted", w=420),
        arrow("open", 620, 570, 750, 588, dashed=True, color="note",
              label="...and if two names hold it?"),
    ]
    spec("a01-stack-heap",
         "Stack, heap, and the pointer that outlived its frame",
         "Three stack frames drawn as boxes on the left and a heap allocation "
         "on the right. A green arrow shows make_buf returning a pointer; the "
         "make_buf frame is then crossed out in red, and a red arrow shows the "
         "caller still holding the address of memory whose owning frame is "
         "gone.",
         960, 620, els, tier="T3")


# ===========================================================================
# A15 - memory hierarchy, latency bars to scale
# ===========================================================================
def a15_memory():
    rows = [
        ("L1 cache", 1.0, "~1 ns", "correct", "1 second"),
        ("L2 cache", 4.0, "~4 ns", "correct", "4 seconds"),
        ("L3 cache", 12.0, "~12 ns", "structure", "12 seconds"),
        ("DRAM", 80.0, "~80 ns", "note", "1.5 minutes"),
        ("NVMe SSD", 90_000.0, "~90 µs", "error", "1 day"),
        ("network RTT (same AZ)", 500_000.0, "~500 µs", "error", "6 days"),
        ("spinning disk seek", 10_000_000.0, "~10 ms", "error", "4 months"),
    ]
    import math
    els = [text("hdr", 480, 110,
                "bar length is log-scaled - the true scale would not fit on a "
                "screen, or in a building", 15, color="muted", w=700)]
    x0, y = 280, 150
    for i, (label, ns, val, col, human) in enumerate(rows):
        w = 26 + math.log10(ns) * 64
        els.append(dict(type="bar", id=f"b{i}", x=x0, y=y, w=w, h=26,
                        label=label, value=val, color=col, size=16))
        els.append(text(f"h{i}", 950, y + 20, human, 15, color="muted",
                        anchor="end", rotate=0))
        y += 42
    els += [
        text("hh", 950, 132, "if 1 ns were 1 second:", 15, color="muted",
             anchor="end"),
        note("n1", 60, 480,
             "L1 to DRAM is 80x. DRAM to SSD is another 1000x. Your algorithm "
             "does not get to ignore this: a cache-friendly O(n²) beats a "
             "pointer-chasing O(n log n) more often than anyone admits.",
             w=330),
        note("n2", 640, 470,
             "this is the whole reason B-trees exist (week 8), and the whole "
             "reason a KV cache exists (week 25).", w=270),
        circled("c1", 470, 560, "locality of reference", size=19),
        dict(type="highlight", id="hl", x=278, y=150 + 42 * 4 - 4, w=430, h=34),
        arrow("open", 620, 600, 750, 618, dashed=True, color="note",
              label="...measure yours"),
    ]
    spec("a15-memory-hierarchy",
         "The memory hierarchy, with the latencies written in",
         "Seven hachured bars, log-scaled, running from a one-nanosecond L1 "
         "cache hit to a ten-millisecond disk seek, each labelled with its real "
         "latency and with a human-scale equivalent on the right showing that "
         "if an L1 hit took one second, a disk seek would take four months.",
         1000, 650, els, tier="T3")


# ===========================================================================
# A35 - LoRA: the frozen matrix and the thin B·A path
# ===========================================================================
def a35_lora():
    WX, WY, WW, WH = 200, 160, 240, 150          # the frozen matrix
    AX, AY, AW, AH = 200, 384, 104, 116          # A
    BX = 336                                     # B
    PX, PY = 620, 300                            # the sum
    els = [
        box("w", WX, WY, WW, WH, "W  (frozen)\n4096 × 4096", color="muted",
            fill="hachure", fill_color="muted", fill_gap=12, size=20),
        text("wp", WX + WW / 2, WY + WH + 22,
             "16,777,216 parameters — none of them move", 15, color="muted"),
        text("snow", WX + WW / 2, WY - 18, "❄ gradients never reach this", 15,
             color="structure"),
        box("a", AX, AY, AW, AH, "A\n8 × 4096", color="correct",
            fill="hachure", fill_color="correct", size=17),
        box("b", BX, AY, AW, AH, "B\n4096 × 8", color="correct",
            fill="hachure", fill_color="correct", size=17),
        arrow("ab", AX + AW + 3, AY + AH / 2, BX - 4, AY + AH / 2,
              color="correct"),
        text("ap", AX + AW / 2, AY + AH + 22, "32,768", 15, color="correct"),
        text("bp", BX + AW / 2, AY + AH + 22, "32,768", 15, color="correct"),
        text("init", 560, AY + 30,
             "B is initialised to ZERO, so B·A·x = 0 on step 0 — the model is "
             "byte-for-byte unchanged until you train it", 14, color="muted",
             w=250, anchor="start"),

        # x fans out: up into the frozen path, down into the adapter
        text("x", 84, 292, "x", 22, bold=True),
        arrow("in-w", 106, 292, WX - 6, WY + WH / 2, color="ink", curve=-0.10),
        arrow("in-a", 106, 306, AX - 6, AY + AH / 2, color="correct",
              curve=0.10),

        arrow("w-out", WX + WW + 4, WY + WH / 2, PX - 32, PY - 12,
              color="ink", curve=-0.06),
        arrow("b-out", BX + AW + 4, AY + AH / 2, PX - 32, PY + 14,
              color="correct", curve=0.06, width=2.4),
        dict(type="ellipse", id="plus", cx=PX, cy=PY, rx=28, ry=28, label="+",
             color="ink", size=28),
        arrow("out", PX + 32, PY, PX + 130, PY, color="ink"),
        text("h", PX + 152, PY + 6, "h", 22, bold=True),

        badge("b1", 130, 250, 1),
        badge("b2", 176, AY - 16, 2),
        badge("b3", PX + 4, PY - 48, 3),

        text("eq", 470, 570, "h = Wx + (B·A)x        rank r = 8,  α = 16", 21,
             bold=True, w=460),
        dict(type="highlight", id="hl", x=268, y=602, w=404, h=34),
        text("count", 470, 626, "65,536 trainable of 16.8M   =   0.39%", 20,
             bold=True),
        note("n1", 700, 150,
             "you are not compressing the model. You are betting the UPDATE is "
             "low-rank. For instruction tuning that bet pays. For teaching it a "
             "new language it does not.", w=230),
        note("n2", 700, 400,
             "merge B·A back into W at deploy time and inference costs exactly "
             "zero extra — but then you cannot hot-swap adapters. Pick one.",
             w=230),
        circled("c1", 150, 500, "low-rank update", ring="correct", size=19),
        arrow("open", 700, 660, 830, 676, dashed=True, color="note",
              label="...what does r = 1 cost you?"),
    ]
    spec("a35-lora",
         "LoRA: a frozen matrix and a thin trainable detour",
         "A large hachured grey matrix W labelled frozen, holding 16.8 million "
         "parameters that never move, and beneath it a much thinner green path "
         "through two rank-eight matrices A and B holding 65,536 trainable "
         "parameters. Both paths meet at a sum node; the highlighted line "
         "underneath reads 0.39 percent trainable.",
         1000, 710, els, tier="T3")


def main():
    a32_attention(); a28_backprop(); a37_hnsw()
    a01_stack_heap(); a15_memory(); a35_lora()
    from flagships_b import extend
    extend(SPECS, spec, box, arrow, note, circled, text, badge)
    OUT.mkdir(parents=True, exist_ok=True)
    for sid, s in SPECS.items():
        (OUT / f"{sid}.json").write_text(
            json.dumps(s, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"wrote tools/specs/{sid}.json  ({len(s['elements'])} elements)")
    print(f"\n{len(SPECS)} flagship specs")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
