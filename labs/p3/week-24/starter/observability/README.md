# observability/

TODO (standard):

- expose Prometheus metrics from the service (`prometheus_client`, `/metrics`)
- install kube-prometheus-stack via Helm on the kind cluster
- a Grafana dashboard with: request rate, latency p50/p95/p99, error rate, pod count

The dashboard JSON belongs in this directory, committed. A dashboard that only exists
in someone's browser is not observability, it is a screenshot.

The four panels above are not arbitrary — they are the RED method (Rate, Errors,
Duration) plus the one thing RED does not cover for an autoscaled service, which is
whether the autoscaler is doing anything.
