# ---------------------------------------------------------------------------
# lab.mk — the shared verification engine for every Nexus lab.
#
# Every lab's Makefile sets a handful of variables and then `include lab.mk`.
# Nothing below is lab-specific.
#
#   make verify                 run TRACK (default: standard) against IMPL (default: starter)
#   make verify TRACK=basic     run the scaffolded track
#   make verify IMPL=solution   run against the reference implementation
#   make solution               shorthand for IMPL=solution
#   make contract               prove the tests are honest: GREEN on solution, RED on starter
#   make bench                  run the benchmark harness (labs with a perf target)
#   make ship                   the checklist this lab must end on
#   make clean
#   make help
# ---------------------------------------------------------------------------

TRACK ?= standard
IMPL  ?= starter
LANG  ?= python

# --- repo root + interpreter discovery -------------------------------------
REPO_ROOT := $(shell d="$(CURDIR)"; while [ "$$d" != "/" ] && [ ! -f "$$d/bootstrap.sh" ]; do d=$$(dirname "$$d"); done; echo "$$d")
ifeq ($(wildcard $(REPO_ROOT)/.venv/bin/python),)
PY ?= python3
else
PY ?= $(REPO_ROOT)/.venv/bin/python
endif

UNAME_S := $(shell uname -s)
# LeakSanitizer only exists on Linux; on macOS ASan still catches overflows and
# use-after-free, and `make memcheck` is where leak checking lives there.
ifeq ($(UNAME_S),Linux)
ASAN_OPTS ?= detect_leaks=1
else
ASAN_OPTS ?= detect_leaks=0
endif

CC       ?= cc
CFLAGS   ?= -std=c17 -Wall -Wextra -Wpedantic -g -O1
SANFLAGS ?= -fsanitize=address,undefined -fno-omit-frame-pointer
BUILD    := build

VALID_TRACKS := basic standard hard
ifeq ($(filter $(TRACK),$(VALID_TRACKS)),)
$(error TRACK must be one of: $(VALID_TRACKS)  (got "$(TRACK)"))
endif

# Tracks are cumulative: climbing to `standard` must not break `basic`.
TRACK_EXPR_basic    := basic or all
TRACK_EXPR_standard := basic or standard or all
TRACK_EXPR_hard     := basic or standard or hard or all
TRACK_EXPR          := $(TRACK_EXPR_$(TRACK))
TRACK_LEVEL_basic    := 1
TRACK_LEVEL_standard := 2
TRACK_LEVEL_hard     := 3
TRACK_LEVEL          := $(TRACK_LEVEL_$(TRACK))

GREEN := \033[32m
RED   := \033[31m
DIM   := \033[2m
BOLD  := \033[1m
OFF   := \033[0m

.DEFAULT_GOAL := help
.PHONY: help verify solution contract bench ship clean lint typecheck memcheck _verify_impl

help:
	@printf '$(BOLD)%s$(OFF)  ($(LANG))\n' "$(LAB_ID) — $(LAB_TITLE)"
	@printf '$(DIM)time box: $(LAB_TIMEBOX)$(OFF)\n\n'
	@printf '  make verify                 tests for TRACK=$(TRACK) against IMPL=$(IMPL)\n'
	@printf '  make verify TRACK=basic     the scaffolded track\n'
	@printf '  make verify TRACK=hard      the track with the extra constraint\n'
	@printf '  make solution               run the same tests against solution/\n'
	@printf '  make contract               prove the tests are honest (solution green, starter red)\n'
	@printf '  make bench                  benchmark harness\n'
	@printf '  make ship                   the "ship it" checklist\n'
	@printf '  make clean\n'

# ---------------------------------------------------------------------------
# verify
# ---------------------------------------------------------------------------
verify:
	@printf '$(BOLD)==> %s · track=%s · impl=%s$(OFF)\n' "$(LAB_ID)" "$(TRACK)" "$(IMPL)"
	@$(MAKE) --no-print-directory _verify_impl TRACK=$(TRACK) IMPL=$(IMPL)

solution:
	@$(MAKE) --no-print-directory verify IMPL=solution TRACK=$(TRACK)

# --- python ----------------------------------------------------------------
ifeq ($(LANG),python)
PYTEST_ARGS ?= -q
_verify_impl:
	@test -d "$(IMPL)" || { printf '$(RED)no such implementation dir: %s$(OFF)\n' "$(IMPL)"; exit 2; }
	@PYTHONPATH="$(CURDIR)/$(IMPL):$(CURDIR)" NEXUS_TRACK=$(TRACK) NEXUS_IMPL=$(IMPL) \
		$(PY) -m pytest tests -m "$(TRACK_EXPR)" $(PYTEST_ARGS)

lint:
	@$(PY) -m ruff check $(IMPL) tests 2>/dev/null || printf '$(DIM)ruff not installed — skipped$(OFF)\n'

typecheck:
	@$(PY) -m mypy --strict $(IMPL) 2>/dev/null || printf '$(DIM)mypy not installed — skipped$(OFF)\n'
endif

# --- c ---------------------------------------------------------------------
ifeq ($(LANG),c)
TEST_SRC ?= $(wildcard tests/test_*.c)
IMPL_SRC  = $(filter-out $(IMPL)/main.c $(IMPL)/bench.c,$(wildcard $(IMPL)/*.c))
_verify_impl:
	@test -d "$(IMPL)" || { printf '$(RED)no such implementation dir: %s$(OFF)\n' "$(IMPL)"; exit 2; }
	@mkdir -p $(BUILD)
	@rc=0; \
	for t in $(TEST_SRC); do \
	  out="$(BUILD)/$$(basename $$t .c).$(IMPL)"; \
	  $(CC) $(CFLAGS) $(SANFLAGS) -DNEXUS_TRACK_LEVEL=$(TRACK_LEVEL) \
	     -I$(IMPL) -Itests $$t $(IMPL_SRC) -o $$out -lm || { rc=1; continue; }; \
	  NEXUS_TRACK=$(TRACK) ASAN_OPTIONS=$(ASAN_OPTS) $$out || rc=1; \
	done; \
	exit $$rc

memcheck: 
	@mkdir -p $(BUILD)
	@if command -v valgrind >/dev/null 2>&1; then \
	  for t in $(TEST_SRC); do \
	    out="$(BUILD)/$$(basename $$t .c).vg"; \
	    $(CC) $(CFLAGS) -DNEXUS_TRACK_LEVEL=$(TRACK_LEVEL) -I$(IMPL) -Itests $$t $(IMPL_SRC) -o $$out -lm; \
	    valgrind --leak-check=full --error-exitcode=99 $$out || exit 1; \
	  done; \
	else \
	  printf '$(DIM)valgrind unavailable (normal on macOS/ARM) — using AddressSanitizer + LeakSanitizer instead$(OFF)\n'; \
	  $(MAKE) --no-print-directory _verify_impl; \
	fi
endif

# --- shell -----------------------------------------------------------------
ifeq ($(LANG),shell)
BATS_FILES ?= $(wildcard tests/*.bats)
_verify_impl:
	@test -d "$(IMPL)" || { printf '$(RED)no such implementation dir: %s$(OFF)\n' "$(IMPL)"; exit 2; }
	@if command -v bats >/dev/null 2>&1; then \
	  NEXUS_TRACK=$(TRACK) NEXUS_IMPL=$(CURDIR)/$(IMPL) bats $(BATS_FILES); \
	else \
	  printf '$(DIM)bats not installed — using the bundled bats-lite runner$(OFF)\n'; \
	  NEXUS_TRACK=$(TRACK) NEXUS_IMPL=$(CURDIR)/$(IMPL) bin/bats-lite.sh $(BATS_FILES); \
	fi

lint:
	@command -v shellcheck >/dev/null 2>&1 && shellcheck $(IMPL)/*.sh || printf '$(DIM)shellcheck not installed — skipped$(OFF)\n'
endif

# --- hdl (nand2tetris hardware simulator) ----------------------------------
ifeq ($(LANG),hdl)
_verify_impl:
	@NEXUS_TRACK=$(TRACK) $(PY) tests/run_hdl.py --impl $(IMPL) --track $(TRACK)
endif

# ---------------------------------------------------------------------------
# contract — the tests are only worth anything if they can tell the two apart
# ---------------------------------------------------------------------------
contract:
	@printf '$(BOLD)==> contract check: %s track=%s$(OFF)\n' "$(LAB_ID)" "$(TRACK)"
	@if $(MAKE) --no-print-directory _verify_impl IMPL=solution TRACK=$(TRACK) >$(BUILD)-contract.sol.log 2>&1; then \
	   printf '  $(GREEN)PASS$(OFF)  solution/ is green\n'; \
	 else \
	   printf '  $(RED)FAIL$(OFF)  solution/ is NOT green — the reference implementation is broken\n'; \
	   tail -25 $(BUILD)-contract.sol.log; exit 1; \
	 fi
	@if $(MAKE) --no-print-directory _verify_impl IMPL=starter TRACK=$(TRACK) >$(BUILD)-contract.start.log 2>&1; then \
	   printf '  $(RED)FAIL$(OFF)  starter/ is green — the tests do not actually test anything\n'; exit 1; \
	 else \
	   printf '  $(GREEN)PASS$(OFF)  starter/ is red (as it must be)\n'; \
	 fi
	@rm -f $(BUILD)-contract.sol.log $(BUILD)-contract.start.log
	@printf '$(GREEN)contract holds$(OFF)\n'

# ---------------------------------------------------------------------------
ifndef BENCH_CMD
bench:
	@printf '$(DIM)$(LAB_ID) has no benchmark target.$(OFF)\n'
else
bench:
	@$(BENCH_CMD)
endif

ship:
	@printf '$(BOLD)Ship it — %s$(OFF)\n' "$(LAB_ID)"
	@sed -n '/^## Ship it/,/^## /p' README.md | sed '$$d'

clean:
	@rm -rf $(BUILD) .pytest_cache **/__pycache__ __pycache__ *.log build-contract.*.log
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@printf 'cleaned\n'
