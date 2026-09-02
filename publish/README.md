# Publishing

The course is authored as **Mintlify MDX** under `site/`. Mintlify is a hosted
product — `mint` offers `dev`, `broken-links` and linting, but no `build` or
static export — so publishing anywhere other than Mintlify's own hosting means
rendering the same content with a different generator.

`convert.py` does that, targeting **MkDocs Material**, chosen because every
component the course actually uses has a real equivalent:

| Mintlify | MkDocs Material | Why it matters |
|---|---|---|
| `<Tabs>` / `<Tab>` | `pymdownx.tabbed` | the three layers (Ground / Build / Edge) |
| `<Accordion>` | `pymdownx.details` | the lab hint ladder and checkpoint answers — click to reveal |
| `<Note> <Warning> <Tip> <Info> <Check>` | admonitions | |
| `<Steps>` / `<Step>` | bold step headings | |
| `<Card>` / `<CardGroup>` | link lists | |
| `<Frame>` + light/dark `<img>` | `#only-light` / `#only-dark` | the 519 hand-drawn SVGs, theme-aware |

## Two options

```bash
# Mintlify hosting - nothing breaks, drip release works, 15 minutes
cd site && mint dev          # preview; then connect the repo at mintlify.com

# GitHub Pages - static, free, any host
python3 publish/convert.py
cd publish && python3 -m mkdocs build      # -> _site/
```

`.github/workflows/pages.yml` runs the second on every push to `main`.
Enable it once at **Settings → Pages → Source: GitHub Actions**.

## What differs on the static build

- **Drip release is gone.** Mintlify hides unreleased weeks via `hidden` groups in
  `docs.json`; MkDocs has no equivalent, so every week is visible. If you need
  paced release, either keep Mintlify or generate `nav` from a released-weeks list.
- **Hidden solutions are reachable.** They are already "hidden, not private" on
  Mintlify, but on a static build they also appear in search.
- Visual identity is Material's, not Mintlify's.

## The indentation trap

JSX indentation in the source is not a consistent multiple of four — a `<Tab>`
sits at 2 and an `<Accordion>` inside it at 8. Shifting a block uniformly leaves
nested markers at 6, which Markdown reads as neither a new block nor content:
the tab set silently fails to form and the three layers collapse into one page.
`normalise_blocks()` recurses instead, placing each marker at `depth × 4`. If you
change the converter, verify with:

```bash
python3 - <<'PY'
import glob
bad = sum(('???' in open(f, errors='ignore').read()) for f in glob.glob('_site/**/*.html', recursive=True))
print("pages with unrendered markers:", bad)   # must be 0
PY
```
