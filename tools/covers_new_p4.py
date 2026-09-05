#!/usr/bin/env python3
"""Covers for the four new Phase-4 chapters. Facts checked: ReAct is Yao et al.
2022 (reasoning + acting interleaved); the frameworks named exist and are
described by their actual design (LangGraph graph-based, smolagents writes
Python, CrewAI roles, OpenAI Agents SDK multi-provider)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from covers_lib import build, preview
COVERS = {
"curriculum/p4/week-25/0-talking-to-the-model.mdx": {
  "id": "cover-w25m0",
  "alt": "A vague request gets a vague answer and is crossed out; a specific one states audience, length and format; eight techniques with a decision table.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "vague", "x": 70, "y": 44, "w": 210, "h": 44, "label": "“Summarise this.”", "size": 15, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 44, "w": 210, "h": 44, "style": "strike"},
    {"type": "box", "id": "spec", "x": 70, "y": 100, "w": 240, "h": 62, "label": "“Two sentences, for a manager. State the problem and what they want.”", "size": 10, "color": "correct"},
    {"type": "text", "id": "t1", "x": 186, "y": 194, "text": "the model did nothing wrong —", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t1b", "x": 186, "y": 216, "text": "you did not say what you meant", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 400, "y": 62},
    {"type": "text", "id": "k1", "x": 545, "y": 64, "text": "just ask (zero-shot)", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "k2", "x": 545, "y": 88, "text": "show, don't tell (few-shot)", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "k3", "x": 545, "y": 112, "text": "room to think (chain of thought)", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "k4", "x": 545, "y": 136, "text": "fence the data · ask for a shape", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "k5", "x": 545, "y": 160, "text": "scope the role · chain the calls", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "t2", "x": 545, "y": 200, "text": "eight techniques, each with a before and after", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 232},
    {"type": "text", "id": "t3", "x": 832, "y": 244, "text": "two things prompting can NEVER do:", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t3b", "x": 832, "y": 268, "text": "teach facts · change habits", "size": 14, "color": "error", "w": 999},
    {"type": "circled", "id": "term", "x": 200, "y": 258, "text": "the prompt", "ring": "note"},
    {"type": "note", "id": "n", "x": 320, "y": 250, "w": 280, "text": "read everything · knows nothing about you · never asks."},
    {"type": "text", "id": "dq", "x": 620, "y": 306, "text": "and what happens to your note the moment it arrives?", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

"curriculum/p4/week-29/6-agent-architectures-and-harnesses.mdx": {
  "id": "cover-w29m6",
  "alt": "Four ways to send someone shopping map to four agent architectures; a ReAct transcript of thought, action and observation; and the harness that decides survival.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 100},
    {"type": "text", "id": "s1", "x": 200, "y": 60, "text": "improvises → ReAct", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "s2", "x": 200, "y": 86, "text": "plans first → plan-then-execute", "size": 16, "w": 999},
    {"type": "text", "id": "s3", "x": 200, "y": 112, "text": "checks the basket → reflection", "size": 16, "w": 999},
    {"type": "text", "id": "s4", "x": 200, "y": 138, "text": "a team → multi-agent", "size": 16, "w": 999},
    {"type": "text", "id": "t1", "x": 190, "y": 180, "text": "four ways to send someone", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t1b", "x": 190, "y": 202, "text": "to the shops", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 400, "y": 62},
    {"type": "text", "id": "r1", "x": 560, "y": 64, "text": "Thought: I need August revenue.", "size": 14, "color": "structure", "w": 999},
    {"type": "text", "id": "r2", "x": 560, "y": 88, "text": "Action:  run_sql(…)", "size": 14, "color": "note", "w": 999},
    {"type": "text", "id": "r3", "x": 560, "y": 112, "text": "Observation: 184,220", "size": 14, "color": "correct", "w": 999},
    {"type": "text", "id": "r4", "x": 560, "y": 136, "text": "Thought: I need July too…", "size": 14, "color": "structure", "w": 999},
    {"type": "text", "id": "t2", "x": 560, "y": 176, "text": "the thought is written down, so the", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2b", "x": 560, "y": 198, "text": "next step can use the last result", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 230},
    {"type": "text", "id": "t3", "x": 830, "y": 242, "text": "the harness: validation · budgets", "size": 15, "color": "note", "w": 999},
    {"type": "text", "id": "t3b", "x": 830, "y": 266, "text": "errors · tracing — most of a framework", "size": 15, "color": "note", "w": 999},
    {"type": "circled", "id": "term", "x": 200, "y": 252, "text": "ReAct", "ring": "note"},
    {"type": "note", "id": "n", "x": 320, "y": 250, "w": 280, "text": "architecture gets the diagram. The harness decides survival."},
    {"type": "text", "id": "dq", "x": 620, "y": 306, "text": "one worker, however good. Real work branches — Week 30.", "size": 18, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

"curriculum/p4/week-26/0-choosing-a-model.mdx": {
  "id": "cover-w26m0",
  "alt": "Hiring a professor for every question is crossed out; the quality-cost-speed triangle; and the rule: the cheapest model that clears your bar, proven on twenty of your own cases.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "prof", "x": 70, "y": 44, "w": 220, "h": 50, "label": "hire the professor for everything", "size": 12, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 44, "w": 220, "h": 50, "style": "strike"},
    {"type": "text", "id": "t1", "x": 180, "y": 124, "text": "…then complain about the bill", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t1b", "x": 180, "y": 162, "text": "one question, a million times a month", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 400, "y": 62},
    {"type": "text", "id": "q1", "x": 545, "y": 66, "text": "quality", "size": 17, "color": "correct", "w": 999},
    {"type": "text", "id": "q2", "x": 545, "y": 94, "text": "cost", "size": 17, "color": "note", "w": 999},
    {"type": "text", "id": "q3", "x": 545, "y": 122, "text": "speed", "size": 17, "color": "structure", "w": 999},
    {"type": "text", "id": "t2", "x": 545, "y": 162, "text": "pick any two — so route the easy work", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2b", "x": 545, "y": 184, "text": "to a small model and keep the big one", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2c", "x": 545, "y": 206, "text": "for the hard 5%", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 62},
    {"type": "box", "id": "rule", "x": 725, "y": 44, "w": 230, "h": 56, "label": "cheapest that clears the bar", "size": 13, "color": "correct"},
    {"type": "text", "id": "t3", "x": 840, "y": 126, "text": "not the best model —", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "t3b", "x": 840, "y": 148, "text": "the difference is margin, forever", "size": 15, "color": "correct", "w": 999},
    {"type": "text", "id": "t3c", "x": 840, "y": 186, "text": "proven on twenty of YOUR cases,", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t3d", "x": 840, "y": 208, "text": "never on a leaderboard", "size": 15, "color": "muted", "w": 999},
    {"type": "circled", "id": "term", "x": 200, "y": 250, "text": "the bake-off", "ring": "note"},
    {"type": "note", "id": "n", "x": 340, "y": 236, "w": 290, "text": "your first week's question, answered with evidence."},
    {"type": "text", "id": "dq", "x": 620, "y": 306, "text": "and it is 16 GB of numbers that will not fit your card.", "size": 18, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},

"curriculum/p4/week-27/0-when-the-input-is-not-text.mdx": {
  "id": "cover-w27m0",
  "alt": "A pasted screenshot defeats a text-only system; images become patches that join the text sequence; and a text-only pipeline silently discards the diagram that mattered.",
  "elements": [
    {"type": "badge", "id": "b1", "n": 1, "x": 48, "y": 62},
    {"type": "box", "id": "shot", "x": 70, "y": 44, "w": 210, "h": 60, "label": "the user pastes a screenshot", "size": 13, "color": "structure"},
    {"type": "box", "id": "no", "x": 70, "y": 116, "w": 210, "h": 44, "label": "“I can only read text”", "size": 14, "color": "error"},
    {"type": "crossout", "id": "x", "x": 70, "y": 116, "w": 210, "h": 44, "style": "strike"},
    {"type": "text", "id": "t1", "x": 176, "y": 192, "text": "they did the most helpful thing", "size": 15, "color": "error", "w": 999},
    {"type": "text", "id": "t1b", "x": 176, "y": 214, "text": "they could think of", "size": 15, "color": "error", "w": 999},
    {"type": "badge", "id": "b2", "n": 2, "x": 380, "y": 62},
    {"type": "text", "id": "p1", "x": 540, "y": 68, "text": "cut into patches →", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "p2", "x": 540, "y": 94, "text": "each becomes numbers →", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "p3", "x": 540, "y": 120, "text": "same sequence as your text tiles", "size": 16, "color": "correct", "w": 999},
    {"type": "text", "id": "t2", "x": 540, "y": 162, "text": "nothing new was invented — the same", "size": 15, "color": "muted", "w": 999},
    {"type": "text", "id": "t2b", "x": 540, "y": 184, "text": "machine was fed something else", "size": 15, "color": "muted", "w": 999},
    {"type": "badge", "id": "b3", "n": 3, "x": 700, "y": 214},
    {"type": "text", "id": "t3", "x": 858, "y": 226, "text": "meaning in the pixels → send the image", "size": 14, "color": "correct", "w": 999},
    {"type": "text", "id": "t3b", "x": 858, "y": 248, "text": "text trapped in a scan → OCR is cheaper", "size": 14, "color": "note", "w": 999},
    {"type": "text", "id": "t3c", "x": 858, "y": 272, "text": "and a text-only pipeline eats your diagrams", "size": 14, "color": "error", "w": 999},
    {"type": "circled", "id": "term", "x": 200, "y": 252, "text": "multimodal", "ring": "note"},
    {"type": "note", "id": "n", "x": 340, "y": 234, "w": 290, "text": "one model · one stream · several kinds of input."},
    {"type": "text", "id": "dq", "x": 620, "y": 306, "text": "now put a pile of your own documents in front of it.", "size": 19, "color": "note"},
  ], "arrow": (150, 300, 340, 300)},
}
if __name__ == "__main__":
    build(COVERS)
    if "--preview" in sys.argv: preview(COVERS, "newp4")
