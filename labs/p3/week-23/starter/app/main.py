"""The prediction service. YOUR WORK GOES HERE.

basic:    a FastAPI wrapper plus a Dockerfile that builds and runs locally.
standard: versioned artifact, validated I/O, /healthz vs /readyz, CI, deployed.
hard:     p95 < 300 ms including cold start, canary + automatic rollback.

The distinction the tests care about most:

  /healthz  — the PROCESS is alive. Cheap, no dependencies, never touches the model.
              If this fails the orchestrator restarts the container.
  /readyz   — the model is loaded AND a warm inference succeeded. If this fails the
              orchestrator takes the pod out of the load balancer but does NOT restart it.

They must be able to disagree: the test starts the app with the model file absent and
asserts /healthz is 200 while /readyz is 503. A service where both check the same thing
gets restart-looped during a slow model load, which is a real and very annoying outage.
"""
from __future__ import annotations

raise NotImplementedError("app/main.py — see standard/SPEC.md")
