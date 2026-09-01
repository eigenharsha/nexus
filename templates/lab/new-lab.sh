#!/usr/bin/env bash
# new-lab.sh — stamp out a new Nexus lab from templates/lab/.
#
#   templates/lab/new-lab.sh \
#       --id LAB-P1-W01 --week 1 --phase p1 --lang c \
#       --title "Sorting & Search Toolkit in C" \
#       --timebox "6-8 h"
#
# Creates labs/<phase>/week-<NN>/ with the full template, placeholders substituted, and the
# files that do not apply to the chosen language removed.
set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$TEMPLATE_DIR/../.." && pwd)"

ID=""; TITLE=""; WEEK=""; PHASE=""; LANG="python"
TIMEBOX="6-8 h"; TB_BASIC="1-2 h"; TB_STANDARD="4-6 h"; TB_HARD="4-8 h"
DEST=""; FORCE=0

die() { printf '\033[31merror:\033[0m %s\n' "$*" >&2; exit 1; }

usage() {
  sed -n "2,9p" "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  cat <<'USAGE'
Options:
  --id ID              lab id, e.g. LAB-P1-W01                (required)
  --title TITLE        human title                            (required)
  --week N             week number 1-32                       (required)
  --phase pN           p1 | p2 | p3 | p4                      (required)
  --lang L             python | c | shell | hdl               (default: python)
  --timebox S          honest total estimate                  (default: 6-8 h)
  --timebox-basic S    (default: 1-2 h)
  --timebox-standard S (default: 4-6 h)
  --timebox-hard S     (default: 4-8 h)
  --dest PATH          override the destination directory
  --force              overwrite an existing lab directory
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --id)               ID="$2"; shift 2 ;;
    --title)            TITLE="$2"; shift 2 ;;
    --week)             WEEK="$2"; shift 2 ;;
    --phase)            PHASE="$2"; shift 2 ;;
    --lang)             LANG="$2"; shift 2 ;;
    --timebox)          TIMEBOX="$2"; shift 2 ;;
    --timebox-basic)    TB_BASIC="$2"; shift 2 ;;
    --timebox-standard) TB_STANDARD="$2"; shift 2 ;;
    --timebox-hard)     TB_HARD="$2"; shift 2 ;;
    --dest)             DEST="$2"; shift 2 ;;
    --force)            FORCE=1; shift ;;
    -h|--help)          usage; exit 0 ;;
    *)                  die "unknown option: $1  (try --help)" ;;
  esac
done

[ -n "$ID" ]    || die "--id is required"
[ -n "$TITLE" ] || die "--title is required"
[ -n "$WEEK" ]  || die "--week is required"
[ -n "$PHASE" ] || die "--phase is required"
case "$LANG" in python|c|shell|hdl) ;; *) die "--lang must be python, c, shell or hdl" ;; esac
case "$PHASE" in p1|p2|p3|p4) ;; *) die "--phase must be p1, p2, p3 or p4" ;; esac

WEEK_PADDED="$(printf '%02d' "$WEEK")"
case "$PHASE" in
  p1) PHASE_NAME="Phase 1 · Foundations" ;;
  p2) PHASE_NAME="Phase 2 · Systems & Data" ;;
  p3) PHASE_NAME="Phase 3 · Machine Learning" ;;
  p4) PHASE_NAME="Phase 4 · Generative AI" ;;
esac

if [ -n "$DEST" ]; then
  # An explicit --dest is used verbatim; LAB_PATH is what the README tells the
  # learner to `cd` into, so it has to follow.
  case "$DEST" in
    "$REPO_ROOT"/*) LAB_PATH="${DEST#"$REPO_ROOT"/}" ;;
    *)              LAB_PATH="$DEST" ;;
  esac
else
  DEST="$REPO_ROOT/labs/$PHASE/week-$WEEK_PADDED"
  LAB_PATH="labs/$PHASE/week-$WEEK_PADDED"
fi

if [ -e "$DEST" ] && [ "$FORCE" -ne 1 ]; then
  die "$DEST already exists (pass --force to overwrite)"
fi

rm -rf "$DEST"
mkdir -p "$(dirname "$DEST")"
cp -R "$TEMPLATE_DIR" "$DEST"
rm -f "$DEST/new-lab.sh"

# --- language pruning -------------------------------------------------------
case "$LANG" in
  python|hdl)
    rm -f "$DEST/tests/nexus_test.h" "$DEST/bin/bats-lite.sh"
    rmdir "$DEST/bin" 2>/dev/null || true
    ;;
  c)
    rm -f "$DEST/tests/conftest.py" "$DEST/tests/test_placeholder.py" \
          "$DEST/pytest.ini" "$DEST/bin/bats-lite.sh"
    rmdir "$DEST/bin" 2>/dev/null || true
    ;;
  shell)
    rm -f "$DEST/tests/nexus_test.h" "$DEST/tests/conftest.py" \
          "$DEST/tests/test_placeholder.py" "$DEST/pytest.ini"
    ;;
esac

# --- placeholder substitution ----------------------------------------------
# sed treats & and \ specially on the replacement side; a title like
# "Sorting & Search Toolkit in C" silently becomes the whole match without this.
esc() { printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'; }

E_ID="$(esc "$ID")";               E_TITLE="$(esc "$TITLE")"
E_PHASE_NAME="$(esc "$PHASE_NAME")"; E_LAB_PATH="$(esc "$LAB_PATH")"
E_TIMEBOX="$(esc "$TIMEBOX")";     E_TB_BASIC="$(esc "$TB_BASIC")"
E_TB_STANDARD="$(esc "$TB_STANDARD")"; E_TB_HARD="$(esc "$TB_HARD")"

subst() {
  local f="$1"
  LC_ALL=C sed -e "s|{{LAB_ID}}|$E_ID|g" \
      -e "s|{{LAB_TITLE}}|$E_TITLE|g" \
      -e "s|{{WEEK}}|$WEEK|g" \
      -e "s|{{PHASE}}|$PHASE|g" \
      -e "s|{{PHASE_NAME}}|$E_PHASE_NAME|g" \
      -e "s|{{LANG}}|$LANG|g" \
      -e "s|{{LAB_PATH}}|$E_LAB_PATH|g" \
      -e "s|{{TIMEBOX}}|$E_TIMEBOX|g" \
      -e "s|{{TIMEBOX_BASIC}}|$E_TB_BASIC|g" \
      -e "s|{{TIMEBOX_STANDARD}}|$E_TB_STANDARD|g" \
      -e "s|{{TIMEBOX_HARD}}|$E_TB_HARD|g" \
      "$f" > "$f.tmp" && mv "$f.tmp" "$f"
}

while IFS= read -r f; do subst "$f"; done < <(
  find "$DEST" -type f \( -name '*.md' -o -name 'Makefile' -o -name '*.mk' \)
)

printf '\033[32mcreated\033[0m %s  (%s, %s)\n' "$LAB_PATH" "$ID" "$LANG"
printf '  next: fill in the {{TICKET}}, {{...}}_CRITERIA and {{SHIP}} placeholders in README.md and the SPECs,\n'
printf '        then write tests/ and solution/ until `make contract` passes.\n'
