# `standard` — LAB-P3-W24

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-9 h

## Acceptance criteria

- Full manifests: Deployment, Service, Ingress, ConfigMap, Secret, liveness/readiness/startup
  probes, and resource requests and limits that you chose from measured usage rather than guessed.
- A HorizontalPodAutoscaler scaling on CPU, demonstrated scaling up under load and back down.
- A TensorFlow Serving deployment alongside the FastAPI one, with the trade-off written down.
- Prometheus metrics exposed by the service and scraped, plus a Grafana dashboard with request
  rate, latency percentiles, error rate and pod count.
- A load-test report showing the scale-up behaviour with the timing of each phase.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Resource requests are the whole game in Kubernetes and everyone guesses them. Measure actual
usage under load first, set requests at roughly the p50 and limits at the p99, and write down
what you observed — that paragraph is what a platform engineer will read first.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
