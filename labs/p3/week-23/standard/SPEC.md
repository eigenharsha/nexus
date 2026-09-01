# `standard` — LAB-P3-W23

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 7-8 h

## Acceptance criteria

- A versioned model artifact: the file, its sha256, the training commit, and the metrics it
  achieved, all recorded and served at `/version`.
- Validated request and response models; an out-of-range input returns 422 with a useful message.
- `/healthz` (process is alive) and `/readyz` (model loaded and a warm inference succeeded) — and
  they must be able to disagree, which the test checks by starting the app with the model absent.
- A multi-stage Docker build under **600 MB** final image size, asserted by the test.
- `docker compose` stack bringing the service up with its dependencies.
- GitHub Actions CI building the image, running the tests inside it, and pushing on a tag.
- Deployed to AWS Lambda behind API Gateway (or a documented equivalent free-tier target).
- A load test and a cost report: cost per 1,000 predictions with the arithmetic shown.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The 600 MB limit is what forces the multi-stage build and the CPU-only torch wheel. A naive
`pip install torch` image is about 2.5 GB and will not fit in a Lambda container image without
work. That constraint is the lab.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
