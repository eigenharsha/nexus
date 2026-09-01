#!/usr/bin/env bash
# bats-lite.sh — runs the subset of bats syntax the Nexus labs use, with no bats installed.
#
# Supports:  @test "name" { ... }  ·  setup()  ·  teardown()  ·  $status $output
#            run CMD  ·  skip [reason]
# Install real bats when you can (`brew install bats-core`); this exists so `make verify`
# never fails for a reason that is not your code.
set -uo pipefail

skip() {
  printf '__BATS_LITE_SKIP__%s\n' "${1:-}"
  exit 0
}

run() {
  output="$("$@" 2>&1)"
  status=$?
  # shellcheck disable=SC2034
  lines=()
  while IFS= read -r _l; do lines+=("$_l"); done <<< "$output"
  return 0
}
export -f run 2>/dev/null || true

total=0; failed=0
for file in "$@"; do
  [ -f "$file" ] || continue
  printf '\033[1m%s\033[0m\n' "$file"
  # Rewrite `@test "name" {` into `nx_test_N() {` and collect the names.
  tmp="$(mktemp -t batslite.XXXXXX)"
  awk '
    /^[[:space:]]*@test[[:space:]]/ {
      n++
      name = $0
      sub(/^[[:space:]]*@test[[:space:]]*"/, "", name)
      sub(/"[[:space:]]*\{[[:space:]]*$/, "", name)
      names[n] = name
      printf "nx_test_%d() {\n", n
      next
    }
    { print }
    END {
      printf "NX_TEST_COUNT=%d\n", n
      for (i = 1; i <= n; i++) {
        gsub(/'"'"'/, "'"'"'\\'"'"''"'"'", names[i])
        printf "NX_TEST_NAME_%d='"'"'%s'"'"'\n", i, names[i]
      }
    }
  ' "$file" > "$tmp"

  ( # subshell so each file gets a clean environment
    # shellcheck disable=SC1090
    source "$tmp"
    rc=0
    for i in $(seq 1 "${NX_TEST_COUNT:-0}"); do
      nameref="NX_TEST_NAME_$i"
      name="${!nameref}"
      out="$( set +e; declare -F setup >/dev/null && setup; "nx_test_$i"; ec=$?; declare -F teardown >/dev/null && teardown; exit $ec )"
      ec=$?
      case "$out" in
        __BATS_LITE_SKIP__*)
          printf '  \033[2mskip    %s (%s)\033[0m\n' "$name" "${out#__BATS_LITE_SKIP__}"
          continue
          ;;
      esac
      if [ $ec -eq 0 ]; then
        printf '  \033[32mok\033[0m      %s\n' "$name"
      else
        printf '  \033[31mnot ok\033[0m  %s\n' "$name"
        [ -n "$out" ] && printf '%s\n' "$out" | sed 's/^/            /'
        rc=1
      fi
    done
    exit $rc
  )
  rc=$?
  total=$((total + 1))
  [ $rc -ne 0 ] && failed=$((failed + 1))
  rm -f "$tmp"
done

if [ "$failed" -gt 0 ]; then
  printf '\n\033[31m%d of %d test files failed\033[0m\n' "$failed" "$total"
  exit 1
fi
printf '\n\033[32mall %d test files passed\033[0m\n' "$total"
