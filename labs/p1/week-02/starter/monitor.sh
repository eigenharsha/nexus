#!/usr/bin/env bash
# monitor.sh — YOUR WORK GOES HERE.
#
#   ./monitor.sh sample     append one record to metrics.tsv   (standard)
#   ./monitor.sh report     render REPORT.md from metrics.tsv  (standard)
#   ./monitor.sh publish    commit + push over SSH, no-op if unchanged (standard)
#   ./monitor.sh install    install a cron entry / launchd plist (standard)
#   ./monitor.sh once       print a formatted one-shot report   (basic)
#
# basic:    implement `once`.
# standard: the rest, idempotent, locked, logged.
# hard:     alert thresholds, SIGTERM-safe shutdown, log rotation, and survival of
#           100 randomly-timed kills with no corrupt metrics file.
#
# The atomic-write pattern is the whole lab: write to metrics.tsv.tmp, then `mv` it
# into place. `mv` within one filesystem is atomic; `>>` is not, and that is why the
# kill-storm test exists.

set -euo pipefail

# TODO: this script must work on BOTH macOS and Linux. The commands differ:
#   load:    uptime | ... (both)          or  /proc/loadavg (Linux only)
#   memory:  vm_stat (macOS)              or  free -b / /proc/meminfo (Linux)
# Detect with `uname -s`; do not assume.

usage() {
  sed -n '3,11p' "$0" | sed 's/^# \{0,1\}//'
}

cmd_once() {
  # TODO (basic): sample CPU load and memory once and print a formatted report.
  # Exit non-zero with a message on stderr if a tool you need is missing.
  echo "not implemented: once" >&2
  return 1
}

main() {
  case "${1:-}" in
    once)    cmd_once ;;
    sample)  echo "not implemented: sample" >&2; return 1 ;;
    report)  echo "not implemented: report" >&2; return 1 ;;
    publish) echo "not implemented: publish" >&2; return 1 ;;
    install) echo "not implemented: install" >&2; return 1 ;;
    -h|--help|"") usage ;;
    *) echo "unknown command: $1" >&2; usage; return 2 ;;
  esac
}

main "$@"
