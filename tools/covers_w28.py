#!/usr/bin/env python3
"""Week-28 covers — three-beat chapter maps (see tools/covers_lib.py)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from covers_lib import build, preview

W28 = "curriculum/p4/week-28/"
COVERS = {
W28+"index.mdx": {
  "id": "cover-w28",
  "alt": "The week's journey: keyword search finds codes, fusion merges both lists by rank, vague questions get rewritten, a sharper judge re-orders the shortlist, and caching makes it affordable.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 55, "y": 60},
    {"type": "box", "id": "s1", "x": 80, "y": 40, "w": 120, "h": 60, "label": "BM25", "size": 17, "color": "correct"},
    {"type": "text", "id": "t1", "x": 140, "y": 126, "text": "find the exact code", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b2", "n": 2, "x": 250, "y": 60},
    {"type": "box", "id": "s2", "x": 275, "y": 40, "w": 115, "h": 60, "label": "fuse", "size": 17, "color": "note"},
    {"type": "text", "id": "t2", "x": 332, "y": 126, "text": "two lists, one answer", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b3", "n": 3, "x": 440, "y": 60},
    {"type": "box", "id": "s3", "x": 465, "y": 40, "w": 115, "h": 60, "label": "rewrite", "size": 17, "color": "structure"},
    {"type": "text", "id": "t3", "x": 522, "y": 126, "text": "fix the question first", "size": 15, "color": "muted", "w": 150},
    {"type": "badge", "id": "b4", "n": 4, "x": 630, "y": 60},
    {"type": "box", "id": "s4", "x": 655, "y": 40, "w": 115, "h": 60, "label": "re-rank", "size": 17, "color": "correct"},
    {"type": "text", "id": "t4", "x": 712, "y": 126, "text": "sharpest judge, top 10", "size": 15, "color": "muted", "w": 160},
    {"type": "badge", "id": "b5", "n": 5, "x": 820, "y": 60},
    {"type": "box", "id": "s5", "x": 845, "y": 40, "w": 115, "h": 60, "label": "cache", "size": 17, "color": "note"},
    {"type": "text", "id": "t5", "x": 902, "y": 126, "text": "pay once, not forty times", "size": 15, "color": "muted", "w": 160},
    {"type": "box", "id": "res", "x": 300, "y": 178, "w": 400, "h": 58, "label": "search that finds meaning AND letters", "size": 18, "color": "correct", "fill": "hachure", "fill_gap": 15},
    {"type": "circled", "id": "term", "x": 150, "y": 205, "text": "week 28", "ring": "note"},
    {"type": "note", "id": "n", "x": 730, "y": 190, "w": 240, "text": "week 27 built the library. This week it gets good."},
    {"type": "text", "id": "dq", "x": 660, "y": 306, "text": "it starts with a code the map of meanings cannot see…", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 370, 300)},

W28+"1-sparse-retrieval-bm25.mdx": {
  "id": "cover-w28m1",
  "alt": "TX-4471 finds nothing on the map because a code has no meaning; the inverted index maps words to documents and finds it exactly; BM25 scores rare words higher and long documents lower.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "q", "x": 70, "y": 44, "w": 170, "h": 50, "label": "“TX-4471”", "size": 18},
    {"type": "box", "id": "miss", "x": 70, "y": 112, "w": 210, "h": 48, "label": "3 shipping passages", "size": 15, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 112, "w": 210, "h": 48, "style": "strike"},
    {"type": "text", "id": "t1", "x": 175, "y": 190, "text": "a code has no neighbourhood", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 360, "y": 62},
    {"type": "text", "id": "i1", "x": 520, "y": 66, "text": "“refund”  → doc 3, 91", "size": 17, "w": 999},
    {"type": "text", "id": "i2", "x": 520, "y": 98, "text": "“shipping” → doc 7, 12", "size": 17, "w": 999},
    {"type": "text", "id": "i3", "x": 524, "y": 132, "text": "“TX-4471” → doc 4,812 ✓", "size": 17, "color": "correct", "w": 999},
    {"type": "text", "id": "t2", "x": 520, "y": 174, "text": "the inverted index kept the letters", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 690, "y": 214},
    {"type": "text", "id": "t3", "x": 855, "y": 214, "text": "BM25, in one breath:", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "t3b", "x": 855, "y": 240, "text": "rare words count more,", "size": 16, "color": "structure", "w": 999},
    {"type": "text", "id": "t3c", "x": 855, "y": 262, "text": "long documents count less", "size": 16, "color": "structure", "w": 999},
    {"type": "circled", "id": "term", "x": 240, "y": 250, "text": "sparse retrieval", "ring": "note"},
    {"type": "note", "id": "n", "x": 340, "y": 226, "w": 300, "text": "a 1994 algorithm still beats a 2026 model on codes and names."},
    {"type": "text", "id": "dq", "x": 620, "y": 306, "text": "so run both — and merge two lists that disagree.", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

W28+"2-hybrid-search-fusion.mdx": {
  "id": "cover-w28m2",
  "alt": "Adding a 0.83 cosine to a 14.7 BM25 score is crossed out as meaningless; fusing on rank instead lifts the document both lists liked to the top.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "d1", "x": 70, "y": 44, "w": 150, "h": 46, "label": "by meaning: 0.83", "size": 14, "color": "structure"},
    {"type": "box", "id": "d2", "x": 70, "y": 100, "w": 150, "h": 46, "label": "by letters: 14.7", "size": 14, "color": "correct"},
    {"type": "text", "id": "t1", "x": 168, "y": 178, "text": "two different currencies", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 330, "y": 62},
    {"type": "box", "id": "add", "x": 355, "y": 44, "w": 240, "h": 56, "label": "0.83 + 14.7 = 15.53", "size": 17, "color": "error"},
    {"type": "crossout", "id": "x", "x": 355, "y": 44, "w": 240, "h": 56, "style": "strike"},
    {"type": "text", "id": "t2", "x": 475, "y": 128, "text": "like adding °C to miles —", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t2b", "x": 475, "y": 150, "text": "a number that means nothing", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 660, "y": 62},
    {"type": "text", "id": "f1", "x": 830, "y": 70, "text": "keep only the ranks:", "size": 16, "color": "muted", "w": 999},
    {"type": "text", "id": "f2", "x": 832, "y": 104, "text": "score = 1 / (k + rank)", "size": 20, "color": "note", "w": 999},
    {"type": "text", "id": "f3", "x": 832, "y": 138, "text": "add across both lists", "size": 16, "color": "note", "w": 999},
    {"type": "box", "id": "win", "x": 690, "y": 164, "w": 268, "h": 46, "label": "policy §4.2 — top of both ✓", "size": 14, "color": "correct"},
    {"type": "circled", "id": "term", "x": 230, "y": 250, "text": "rank fusion", "ring": "note"},
    {"type": "note", "id": "n", "x": 400, "y": 228, "w": 330, "text": "no normalising, no weighting, no tuning — and hard to beat."},
    {"type": "text", "id": "dq", "x": 640, "y": 306, "text": "but both searches trust the user's words. What if the question says nothing?", "size": 18, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

W28+"3-query-understanding-transformation.mdx": {
  "id": "cover-w28m3",
  "alt": "The question 'why is it broken' retrieves nothing and is crossed in red; rewritten with context it retrieves the right passage; HyDE drafts a fake answer and searches with that.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "q", "x": 70, "y": 44, "w": 200, "h": 50, "label": "“why is it broken”", "size": 17, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 44, "w": 200, "h": 50, "style": "strike"},
    {"type": "text", "id": "t1", "x": 170, "y": 124, "text": "no product · no version · no code", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t1b", "x": 170, "y": 148, "text": "nothing to match on", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 350, "y": 62},
    {"type": "box", "id": "rw", "x": 375, "y": 44, "w": 260, "h": 66, "label": "“mobile app crashes on login, v5.2”", "size": 13, "color": "correct"},
    {"type": "text", "id": "t2", "x": 505, "y": 138, "text": "rewrite · expand · decompose", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 678, "y": 56},
    {"type": "text", "id": "h1", "x": 856, "y": 76, "text": "HyDE: draft a FAKE answer,", "size": 16, "color": "note", "w": 999},
    {"type": "text", "id": "h2", "x": 850, "y": 96, "text": "then search with that", "size": 16, "color": "note", "w": 999},
    {"type": "text", "id": "h3", "x": 850, "y": 134, "text": "an answer speaks the", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "h4", "x": 850, "y": 156, "text": "document's language;", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "h5", "x": 850, "y": 178, "text": "a question does not", "size": 15, "color": "muted", "w": 999},
    {"type": "circled", "id": "term", "x": 250, "y": 240, "text": "query transformation", "ring": "note"},
    {"type": "note", "id": "n", "x": 430, "y": 222, "w": 330, "text": "fix the question, not the search. That is where the expertise lives."},
    {"type": "text", "id": "dq", "x": 640, "y": 306, "text": "top ten now relevant — but the best one sits seventh.", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

W28+"4-re-ranking-with-cross-encoders.mdx": {
  "id": "cover-w28m4",
  "alt": "The fast bi-encoder compares precomputed pins so question and passage never meet; the cross-encoder reads them together and moves the right passage from fourth to first.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "q1", "x": 70, "y": 44, "w": 90, "h": 44, "label": "question", "size": 14, "color": "structure"},
    {"type": "box", "id": "p1", "x": 190, "y": 44, "w": 90, "h": 44, "label": "passage", "size": 14, "color": "structure"},
    {"type": "text", "id": "t1", "x": 175, "y": 118, "text": "bi-encoder: pins compared,", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t1b", "x": 175, "y": 140, "text": "they never actually meet", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t1c", "x": 175, "y": 172, "text": "fast · shallow", "size": 16, "color": "structure", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 360, "y": 62},
    {"type": "box", "id": "cx", "x": 385, "y": 44, "w": 230, "h": 60, "label": "question + passage, read together", "size": 13, "color": "correct"},
    {"type": "text", "id": "t2", "x": 500, "y": 132, "text": "cross-encoder: nothing precomputed", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2b", "x": 500, "y": 164, "text": "sharp · far too slow for 10M", "size": 16, "color": "correct", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 680, "y": 62},
    {"type": "text", "id": "r1", "x": 850, "y": 72, "text": "before:  #4  the answer", "size": 17, "w": 999},
    {"type": "text", "id": "r2", "x": 850, "y": 106, "text": "after:   #1  the answer ✓", "size": 17, "color": "correct", "w": 999},
    {"type": "text", "id": "r3", "x": 850, "y": 150, "text": "10,000 CVs → shortlist of 10", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "r4", "x": 850, "y": 172, "text": "→ read those ten properly", "size": 15, "color": "muted", "w": 999},
    {"type": "circled", "id": "term", "x": 250, "y": 245, "text": "re-ranking", "ring": "note"},
    {"type": "note", "id": "n", "x": 420, "y": 226, "w": 340, "text": "fast filter, then the sharp judge — on ten, never on ten million."},
    {"type": "text", "id": "dq", "x": 660, "y": 306, "text": "four models per question. Now look at the bill.", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

W28+"5-caching-cost-production-rag-operations.mdx": {
  "id": "cover-w28m5",
  "alt": "Forty identical questions cost forty times; exact and prefix caches are safe; a loose semantic cache serves the password answer to a device question and is crossed out in red.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "text", "id": "q40", "x": 190, "y": 62, "text": "× 40 the same question", "size": 18, "w": 999},
    {"type": "bar", "id": "cost", "x": 90, "y": 84, "w": 190, "h": 18, "label": "", "value": "40 bills", "color": "error"},
    {"type": "text", "id": "t1", "x": 175, "y": 140, "text": "one answer, paid for forty times", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 355, "y": 62},
    {"type": "box", "id": "c1", "x": 380, "y": 44, "w": 230, "h": 40, "label": "exact match — free money", "size": 14, "color": "correct"},
    {"type": "box", "id": "c2", "x": 380, "y": 92, "w": 230, "h": 40, "label": "prompt prefix — cheap", "size": 14, "color": "correct"},
    {"type": "box", "id": "c3", "x": 380, "y": 140, "w": 230, "h": 40, "label": "semantic — careful", "size": 14, "color": "note"},
    {"type": "text", "id": "t2", "x": 495, "y": 204, "text": "three caches, three different bugs", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 680, "y": 62},
    {"type": "box", "id": "bad", "x": 700, "y": 44, "w": 270, "h": 66, "label": "“reset my device” → password answer", "size": 13, "color": "error"},
    {"type": "crossout", "id": "x", "x": 700, "y": 44, "w": 270, "h": 66, "style": "strike"},
    {"type": "text", "id": "t3", "x": 835, "y": 138, "text": "a loose threshold answers the", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t3b", "x": 835, "y": 160, "text": "wrong question — confidently", "size": 15, "color": "error", "w": 999},
    {"type": "circled", "id": "term", "x": 220, "y": 250, "text": "semantic cache", "ring": "note"},
    {"type": "note", "id": "n", "x": 330, "y": 246, "w": 340, "text": "the threshold is a product decision, measured — never a blog-post default."},
    {"type": "text", "id": "dq", "x": 640, "y": 306, "text": "good, cheap, cited — and still answering one question at a time.", "size": 18, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},
}
if __name__ == "__main__":
    build(COVERS)
    if "--preview" in sys.argv: preview(COVERS, "w28")
