# `basic` — LAB-P1-W06

**For:** you have not done this before. About 60% of the code is written; the gaps are marked
`TODO`. Every TODO has a one-line hint above it.

**Time box:** 2 h

## What you must make true

- `POST /tailor` accepting `{resume_text, job_description}` returns formatted Markdown.
- Pydantic models for both request and response; a missing field returns 422 with a useful body.
- Wire the Week-5 frontend to it.

## Acceptance

```bash
make verify TRACK=basic
```

Green means every `TODO` in the files listed above is filled in correctly.

## Hints are not cheating here

The point of `basic` is to see the shape of a correct solution while typing it. If you finish in
under half the time box, do `standard` from an empty file — that is where the learning is.
