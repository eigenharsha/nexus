#!/usr/bin/env bats
# Acceptance tests for LAB-P1-W02 — Self-Reporting System Monitor.
#
# $NEXUS_IMPL points at the implementation directory (starter/ or solution/);
# $NEXUS_TRACK is basic | standard | hard. Guard higher-track tests with skip_below.

setup() {
  MONITOR="$NEXUS_IMPL/monitor.sh"
  WORK="$(mktemp -d)"
}

teardown() {
  [ -n "${WORK:-}" ] && rm -rf "$WORK"
}

# Skip a test whose track is above the one `make verify` was invoked with.
skip_below() {
  case "$NEXUS_TRACK:$1" in
    basic:standard|basic:hard|standard:hard) skip "needs track $1" ;;
  esac
}

# --- basic ------------------------------------------------------------
@test "basic: `monitor.sh` samples CPU load and memory once and prints a formatted report to…" {
  echo "not implemented yet — see basic/SPEC.md" >&2
  return 1
}

@test "basic: Works on both macOS and Linux (the memory command differs; detect, do not…" {
  echo "not implemented yet — see basic/SPEC.md" >&2
  return 1
}

@test "basic: Exits 0 on success and non-zero with a message on stderr if a required tool is…" {
  echo "not implemented yet — see basic/SPEC.md" >&2
  return 1
}

@test "basic: Passes `shellcheck` with no warnings." {
  echo "not implemented yet — see basic/SPEC.md" >&2
  return 1
}

# --- standard ------------------------------------------------------------
@test "standard: `monitor.sh sample` appends one record to `metrics.tsv` and rotates it at a…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: `monitor.sh report` renders `REPORT.md` from the metrics file: current values,…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: `monitor.sh publish` commits and pushes over SSH, and is a no-op when nothing…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: **Idempotent:** two `sample` runs inside the same interval produce exactly one…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: **Locked:** concurrent invocations do not interleave writes (`flock`, or an…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: **Logged:** every run writes a structured line to `monitor.log` with a…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: `set -euo pipefail` and an `ERR` trap that reports the failing line." {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

@test "standard: Installable as a cron entry (Linux) or a launchd plist (macOS) by `monitor.sh…" {
  skip_below standard
  echo "not implemented yet — see standard/SPEC.md" >&2
  return 1
}

# --- hard ------------------------------------------------------------
@test "hard: Alert thresholds in a config file; crossing one writes an `ALERT` line and…" {
  skip_below hard
  echo "not implemented yet — see hard/SPEC.md" >&2
  return 1
}

@test "hard: `trap` handlers clean up the lock and any temp file on `SIGTERM` / `SIGINT` /…" {
  skip_below hard
  echo "not implemented yet — see hard/SPEC.md" >&2
  return 1
}

@test "hard: Log rotation at a size bound, keeping N generations." {
  skip_below hard
  echo "not implemented yet — see hard/SPEC.md" >&2
  return 1
}

@test "hard: The kill-storm test (`tests/kill_storm.bats`) passes: 100 randomly-timed…" {
  skip_below hard
  echo "not implemented yet — see hard/SPEC.md" >&2
  return 1
}

@test "hard: Commit history is `git bisect`-friendly: one commit per sample, message…" {
  skip_below hard
  echo "not implemented yet — see hard/SPEC.md" >&2
  return 1
}
