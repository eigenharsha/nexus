# syntax=docker/dockerfile:1.7
# Multi-stage build. The 600 MB limit is the constraint that forces this: a naive
# `pip install torch` image is about 2.5 GB, and the acceptance test measures the
# final image size.
#
# TODO (standard):
#   1. Install the CPU-only torch wheel (--index-url https://download.pytorch.org/whl/cpu)
#      — the default wheel bundles CUDA and is ~2 GB of it.
#   2. Build the venv in the builder stage, COPY it into a slim runtime stage.
#   3. Do not COPY the training data, the notebooks, or the .git directory. Use .dockerignore.
#   4. Run as a non-root user.
#   5. HEALTHCHECK hitting /healthz.

# ---------- builder ----------
FROM python:3.12-slim AS builder
WORKDIR /build
# TODO: create the venv and install requirements here.

# ---------- runtime ----------
FROM python:3.12-slim AS runtime
WORKDIR /app
# TODO: copy the venv and the application, set PATH, create the user, expose 8000,
# add the HEALTHCHECK, and set the CMD.
CMD ["python", "-c", "raise SystemExit('not implemented — see standard/SPEC.md')"]
