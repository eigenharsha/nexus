# Source-linking brief — READ FIRST

## The task

Every module page ends in **Sources & further reading** with three buckets (Primary docs, Papers,
Go deeper). Today ~2,330 of those entries are plain text. A reader who wants to follow one has to
copy the title into a search engine. Make them clickable.

## The rule that overrides everything

**Never invent a URL.** A confident-looking link to a page that does not exist is worse than no
link: it wastes the reader's time and destroys trust in every other link on the page. This course
just went through a full audit for fabricated data — do not add fabricated links to it.

You may add a link in exactly three cases:

1. **Mechanically derivable from an identifier already in the text.** These are safe and need no
   checking:
   - `arXiv:2401.12345` → `https://arxiv.org/abs/2401.12345`
   - A DOI `10.1145/103162.103163` → `https://doi.org/10.1145/103162.103163`
   - `RFC 9110` → `https://www.rfc-editor.org/rfc/rfc9110`
   - `PEP 3156` → `https://peps.python.org/pep-3156/`
   - A man page → `https://man7.org/linux/man-pages/man1/<name>.1.html` (Linux) — only when the
     entry is about the Linux tool.
2. **An official documentation root you are certain of** — `https://docs.python.org/3/`,
   `https://www.postgresql.org/docs/16/`, `https://fastapi.tiangolo.com/`,
   `https://pytorch.org/docs/stable/`, `https://scikit-learn.org/stable/`,
   `https://kubernetes.io/docs/`, `https://docs.docker.com/`, and similar. Prefer the **specific
   page** only when you are certain of its path; otherwise link the section root. A correct
   shallow link beats a guessed deep one.
3. **Verified with WebFetch.** If you want to link something not covered above and think it
   matters, fetch it first and confirm it is the right page. Use this sparingly — it is slow.

If none of the three applies, **leave the entry as plain text.** That is an acceptable outcome
and is the correct one for: ISO and IEEE standards behind paywalls, printed books, and anything
you are merely fairly sure about.

## Special cases, decided for you

- **ISO/IEC and IEEE standards** — no free canonical URL. Leave unlinked, or link the official
  catalogue page only if you are certain (e.g. `https://www.iso.org/standard/74528.html` for
  C17 — verify with WebFetch before using it).
- **Books** (Bryant & O'Hallaron, Kleppmann, ESL, Strang) — link the publisher or the author's
  official page if you are certain; otherwise leave plain. ESL is free at
  `https://hastie.su.domains/ElemStatLearn/` — that one is safe.
- **Classic papers with a well-known free copy** — Goldberg 1991 is at
  `https://doi.org/10.1145/103162.103163`. Dijkstra 1959 is at
  `https://doi.org/10.1007/BF01386390`. Prefer DOI over a random PDF mirror.
- **Anthropic / OpenAI docs** — `https://docs.claude.com/` and `https://platform.openai.com/docs/`
  roots are safe; deep paths change often, so link the root or a section you are sure of.

## Formatting

Keep the existing structure and the one-sentence takeaway. Only the title becomes a link:

```
- **[Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point
  Arithmetic." *ACM Computing Surveys* 23(1), 5–48.](https://doi.org/10.1145/103162.103163)**
  One-sentence takeaway: ...
```

Keep the bold. Keep the takeaway outside the link. Do not restructure the section, do not add or
remove entries, and do not change any wording.

## MDX safety

These are `.mdx` files. A raw `{` or `<` in prose breaks the build. URLs are fine inside
`(...)`, but if a URL contains a bare `<` or `{`, percent-encode it. After editing, run
`python3 validate.py` and confirm 0 errors.

## Do not

- Do not edit anything outside the **Sources & further reading** section of your assigned pages.
- Do not touch `solutions/`, `tools/`, or `PLAN/`.
- Do not add links to entries that already have one.

## Report

Tell me: how many entries you linked, how many you deliberately left plain and why, and any
entry where you were tempted to guess and stopped.
