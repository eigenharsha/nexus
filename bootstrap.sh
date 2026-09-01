#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# bootstrap.sh — Nexus environment installer.
#
#   ./bootstrap.sh              install everything the 32 weeks need
#   ./bootstrap.sh --check      verify only; green/red per tool, no installs
#   ./bootstrap.sh --through 8  only what weeks 1-8 need (install or check)
#   ./bootstrap.sh --dry-run    print the commands, run nothing
#   ./bootstrap.sh --help
#
# Supported: macOS on Apple Silicon (Homebrew) and Debian/Ubuntu (apt).
# Idempotent: safe to re-run any number of times. Nothing is uninstalled, ever.
# ---------------------------------------------------------------------------
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_VERSION="3.12"
NODE_VERSION="20"

MODE="install"
THROUGH=32
DRY_RUN=0
NO_COLOR=0

if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ] && [ "${NO_COLOR:-0}" = "1" ]; then :; fi
if [ -t 1 ]; then
  C_RED=$'\033[31m'; C_GREEN=$'\033[32m'; C_YEL=$'\033[33m'
  C_DIM=$'\033[2m'; C_BOLD=$'\033[1m'; C_OFF=$'\033[0m'
else
  C_RED=''; C_GREEN=''; C_YEL=''; C_DIM=''; C_BOLD=''; C_OFF=''
fi

usage() {
  sed -n '3,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case "$1" in
    --check)    MODE="check"; shift ;;
    --through)  THROUGH="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --no-color) C_RED=''; C_GREEN=''; C_YEL=''; C_DIM=''; C_BOLD=''; C_OFF=''; shift ;;
    -h|--help)  usage; exit 0 ;;
    *) printf '%serror:%s unknown option %s\n' "$C_RED" "$C_OFF" "$1" >&2; usage; exit 2 ;;
  esac
done

case "$THROUGH" in
  ''|*[!0-9]*) printf '%serror:%s --through takes a week number 1-32\n' "$C_RED" "$C_OFF" >&2; exit 2 ;;
esac

# ---------------------------------------------------------------------------
# platform detection
# ---------------------------------------------------------------------------
OS="$(uname -s)"
ARCH="$(uname -m)"
PLATFORM="unsupported"
PKG=""

case "$OS" in
  Darwin)
    PLATFORM="macos"
    PKG="brew"
    ;;
  Linux)
    if command -v apt-get >/dev/null 2>&1; then
      PLATFORM="debian"; PKG="apt"
    else
      PLATFORM="linux-other"
    fi
    ;;
esac

# ---------------------------------------------------------------------------
# tool table:  key | binary | first week | apt package | brew formula | label
# A blank package field means "installed by a special-case function below".
# ---------------------------------------------------------------------------
TOOLS="
cc|cc|1|build-essential|__xcode__|C compiler (C17)
make|make|1|build-essential|__xcode__|make
valgrind|valgrind|1|valgrind|__skip_macos__|valgrind (Linux only; ASan is the macOS substitute)
git|git|2|git|git|git
vim|vim|2|vim|vim|vim
tmux|tmux|2|tmux|tmux|tmux
jq|jq|2|jq|jq|jq
shellcheck|shellcheck|2|shellcheck|shellcheck|shellcheck
bats|bats|2|bats|bats-core|bats (shell test runner)
uv|uv|3|__uv__|uv|uv (Python package manager)
python|python3|3|__uv__|__uv__|Python ${PYTHON_VERSION}
node|node|5|nodejs|node@${NODE_VERSION}|Node ${NODE_VERSION} LTS
docker|docker|7|__docker__|__cask_docker__|Docker 24+
psql|psql|7|postgresql-client|libpq|psql (Postgres 16 client)
tshark|tshark|10|tshark|wireshark|Wireshark / tshark
gnuplot|gnuplot|13|gnuplot|gnuplot|gnuplot (benchmark plots)
kind|kind|24|__kind__|kind|kind (local Kubernetes)
kubectl|kubectl|24|__kubectl__|kubernetes-cli|kubectl
ollama|ollama|26|__ollama__|__cask_ollama__|Ollama (local LLM serving)
"

# Python packages, week they are first needed. Installed into $REPO_ROOT/.venv.
PY_PACKAGES="
pytest|3
pytest-asyncio|4
mypy|3
ruff|3
hypothesis|3
fastapi|6
uvicorn|6
sqlalchemy|8
alembic|8
psycopg[binary]|7
numpy|11
scipy|12
matplotlib|13
pandas|16
duckdb|15
dlt|15
scikit-learn|17
xgboost|18
shap|18
torch|21
torchvision|22
onnxruntime|22
transformers|25
datasets|25
tokenizers|25
peft|26
trl|26
bitsandbytes|26
accelerate|26
pgvector|27
rank-bm25|28
sentence-transformers|27
langgraph|30
mcp|29
opentelemetry-sdk|32
langfuse|32
"

# ---------------------------------------------------------------------------
say()  { printf '%s\n' "$*"; }
hdr()  { printf '\n%s%s%s\n' "$C_BOLD" "$*" "$C_OFF"; }
info() { printf '%s%s%s\n' "$C_DIM" "$*" "$C_OFF"; }

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '%s+ %s%s\n' "$C_DIM" "$*" "$C_OFF"
    return 0
  fi
  "$@"
}

have() { command -v "$1" >/dev/null 2>&1; }

version_of() {
  case "$1" in
    cc)         cc --version 2>/dev/null | head -1 ;;
    python3)    "$(venv_python)" --version 2>/dev/null || python3 --version 2>/dev/null ;;
    node)       node --version 2>/dev/null ;;
    docker)     docker --version 2>/dev/null | sed 's/,.*//' ;;
    kubectl)    kubectl version --client -o yaml 2>/dev/null | sed -n 's/^  gitVersion: //p' | head -1 ;;
    *)          "$1" --version 2>/dev/null | head -1 ;;
  esac
}

venv_python() { printf '%s/.venv/bin/python' "$REPO_ROOT"; }

# ---------------------------------------------------------------------------
# installers
# ---------------------------------------------------------------------------
ensure_brew() {
  have brew && return 0
  hdr "Homebrew is not installed"
  say "Install it first (it is the one thing this script will not do for you, because it"
  say "changes your PATH and asks for your password):"
  say ""
  say '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  say ""
  return 1
}

apt_update_once() {
  [ -n "${_APT_UPDATED:-}" ] && return 0
  run sudo apt-get update -qq
  _APT_UPDATED=1
}

install_special() {
  # $1 = special token, $2 = tool key
  case "$1" in
    __xcode__)
      have cc && return 0
      info "installing Xcode command line tools (a GUI dialog may appear)"
      run xcode-select --install 2>/dev/null || true
      ;;
    __skip_macos__)
      info "valgrind has no working Apple Silicon build — labs fall back to -fsanitize=address,undefined"
      return 0
      ;;
    __uv__)
      have uv && return 0
      info "installing uv"
      run sh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
      export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
      ;;
    __docker__)
      have docker && return 0
      info "installing docker.io + compose plugin"
      apt_update_once
      run sudo apt-get install -y docker.io docker-compose-plugin
      run sudo usermod -aG docker "$USER" || true
      info "log out and back in for the docker group to take effect"
      ;;
    __cask_docker__)
      have docker && return 0
      run brew install --cask docker
      info "start Docker Desktop once by hand before Week 7"
      ;;
    __kind__)
      have kind && return 0
      info "installing kind"
      run sh -c 'curl -Lo /tmp/kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x /tmp/kind && sudo mv /tmp/kind /usr/local/bin/kind'
      ;;
    __kubectl__)
      have kubectl && return 0
      info "installing kubectl"
      run sh -c 'curl -Lo /tmp/kubectl "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && chmod +x /tmp/kubectl && sudo mv /tmp/kubectl /usr/local/bin/kubectl'
      ;;
    __ollama__)
      have ollama && return 0
      info "installing ollama"
      run sh -c 'curl -fsSL https://ollama.com/install.sh | sh'
      ;;
    __cask_ollama__)
      have ollama && return 0
      run brew install --cask ollama
      ;;
    *)
      return 1
      ;;
  esac
}

install_tool() {
  local key="$1" bin="$2" apt_pkg="$3" brew_pkg="$4"
  have "$bin" && return 0
  case "$PLATFORM" in
    macos)
      case "$brew_pkg" in
        __*__) install_special "$brew_pkg" "$key" ;;
        *)     ensure_brew || return 1; run brew install "$brew_pkg" ;;
      esac
      ;;
    debian)
      case "$apt_pkg" in
        __*__) install_special "$apt_pkg" "$key" ;;
        *)     apt_update_once; run sudo apt-get install -y "$apt_pkg" ;;
      esac
      ;;
    *)
      printf '%s  cannot auto-install %s on this platform — install it by hand%s\n' "$C_YEL" "$key" "$C_OFF"
      return 1
      ;;
  esac
}

setup_python_env() {
  hdr "Python ${PYTHON_VERSION} environment  ->  .venv/"
  if ! have uv; then
    install_special "__uv__" uv
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  fi
  have uv || { printf '%s  uv still not on PATH — open a new shell and re-run%s\n' "$C_RED" "$C_OFF"; return 1; }

  if [ ! -x "$(venv_python)" ]; then
    run uv venv --python "$PYTHON_VERSION" "$REPO_ROOT/.venv" || return 1
  else
    info ".venv already exists — leaving it alone"
  fi

  local want=()
  while IFS='|' read -r pkg wk; do
    [ -z "$pkg" ] && continue
    [ "$wk" -le "$THROUGH" ] && want+=("$pkg")
  done <<< "$(printf '%s\n' "$PY_PACKAGES" | sed '/^$/d')"

  if [ "${#want[@]}" -eq 0 ]; then
    info "no Python packages needed through week ${THROUGH} yet"
    return 0
  fi
  info "installing ${#want[@]} Python packages needed through week ${THROUGH}"
  # One resolver pass; uv is idempotent and skips what is already satisfied.
  run uv pip install --python "$(venv_python)" "${want[@]}" || {
    printf '%s  some packages failed. Retrying one at a time so one bad wheel does not block the rest.%s\n' "$C_YEL" "$C_OFF"
    for p in "${want[@]}"; do
      run uv pip install --python "$(venv_python)" "$p" >/dev/null 2>&1 \
        || printf '%s  skipped %s (no wheel for %s/%s)%s\n' "$C_YEL" "$p" "$OS" "$ARCH" "$C_OFF"
    done
  }
}

# ---------------------------------------------------------------------------
# check mode
# ---------------------------------------------------------------------------
check_all() {
  local ok=0 bad=0 warn=0

  hdr "Nexus environment check"
  printf '%splatform: %s (%s %s) · checking what weeks 1-%s need%s\n' \
     "$C_DIM" "$PLATFORM" "$OS" "$ARCH" "$THROUGH" "$C_OFF"
  printf '\n  %-4s  %-14s  %-40s  %s\n' "WEEK" "TOOL" "STATUS" ""
  printf '  %s\n' "----------------------------------------------------------------------"

  while IFS='|' read -r key bin week apt_pkg brew_pkg label; do
    [ -z "$key" ] && continue
    [ "$week" -gt "$THROUGH" ] && continue
    local optional=0
    if [ "$PLATFORM" = "macos" ] && [ "$brew_pkg" = "__skip_macos__" ]; then optional=1; fi
    if have "$bin"; then
      local v; v="$(version_of "$bin" | cut -c1-38)"
      printf '  %-4s  %s%-14s%s  %sok%s  %s\n' "w$week" "$C_BOLD" "$key" "$C_OFF" "$C_GREEN" "$C_OFF" "${C_DIM}${v}${C_OFF}"
      ok=$((ok + 1))
    elif [ "$optional" -eq 1 ]; then
      printf '  %-4s  %s%-14s%s  %sn/a%s %s\n' "w$week" "$C_BOLD" "$key" "$C_OFF" "$C_YEL" "$C_OFF" "${C_DIM}${label}${C_OFF}"
      warn=$((warn + 1))
    else
      printf '  %-4s  %s%-14s%s  %sMISSING%s  %s\n' "w$week" "$C_BOLD" "$key" "$C_OFF" "$C_RED" "$C_OFF" "${C_DIM}first needed in week ${week} — ${label}${C_OFF}"
      bad=$((bad + 1))
    fi
  done <<< "$(printf '%s\n' "$TOOLS" | sed '/^$/d')"

  # --- python env ---
  hdr "Python environment"
  if [ -x "$(venv_python)" ]; then
    printf '  %s%-14s%s  %sok%s  %s\n' "$C_BOLD" ".venv" "$C_OFF" "$C_GREEN" "$C_OFF" \
      "${C_DIM}$("$(venv_python)" --version 2>&1)${C_OFF}"
    ok=$((ok + 1))
    local pyok=0 pybad=0 missing=""
    while IFS='|' read -r pkg wk; do
      [ -z "$pkg" ] && continue
      [ "$wk" -gt "$THROUGH" ] && continue
      local mod="${pkg%%[*}"; mod="${mod//-/_}"
      case "$mod" in
        psycopg) mod="psycopg" ;;
        scikit_learn) mod="sklearn" ;;
        opentelemetry_sdk) mod="opentelemetry.sdk" ;;
        rank_bm25) mod="rank_bm25" ;;
      esac
      if "$(venv_python)" -c "import $mod" >/dev/null 2>&1; then
        pyok=$((pyok + 1))
      else
        pybad=$((pybad + 1)); missing="$missing $pkg(w$wk)"
      fi
    done <<< "$(printf '%s\n' "$PY_PACKAGES" | sed '/^$/d')"
    if [ "$pybad" -eq 0 ]; then
      printf '  %s%-14s%s  %sok%s  %s\n' "$C_BOLD" "packages" "$C_OFF" "$C_GREEN" "$C_OFF" "${C_DIM}${pyok} importable${C_OFF}"
      ok=$((ok + 1))
    else
      local head_missing rest
      head_missing="$(printf '%s' "$missing" | tr ' ' '\n' | sed '/^$/d' | head -6 | tr '\n' ' ')"
      rest=$((pybad - 6)); [ "$rest" -lt 0 ] && rest=0
      printf '  %s%-14s%s  %sMISSING%s  %s\n' "$C_BOLD" "packages" "$C_OFF" "$C_RED" "$C_OFF" \
        "${C_DIM}${pyok} importable, ${pybad} missing${C_OFF}"
      printf '                  %s%s%s\n' "$C_DIM" "$head_missing" "$C_OFF"
      [ "$rest" -gt 0 ] && printf '                  %s…and %d more%s\n' "$C_DIM" "$rest" "$C_OFF"
      bad=$((bad + 1))
    fi
  else
    printf '  %s%-14s%s  %sMISSING%s  %s\n' "$C_BOLD" ".venv" "$C_OFF" "$C_RED" "$C_OFF" \
      "${C_DIM}run ./bootstrap.sh — first needed in week 3${C_OFF}"
    bad=$((bad + 1))
  fi

  hdr "Result"
  printf '  %s%d ok%s · %s%d missing%s · %s%d not applicable%s\n' \
    "$C_GREEN" "$ok" "$C_OFF" "$C_RED" "$bad" "$C_OFF" "$C_YEL" "$warn" "$C_OFF"
  if [ "$bad" -gt 0 ]; then
    printf '\n  Fix with:  %s./bootstrap.sh%s\n' "$C_BOLD" "$C_OFF"
    printf '  Only need the next few weeks? %s./bootstrap.sh --through 8%s then %s--check --through 8%s.\n' \
      "$C_BOLD" "$C_OFF" "$C_BOLD" "$C_OFF"
    printf '  A red line for a week you have not reached yet is not urgent.\n'
    return 1
  fi
  printf '  You are ready for week %s.\n' "$THROUGH"
  return 0
}

# ---------------------------------------------------------------------------
install_all() {
  hdr "Nexus bootstrap · $PLATFORM ($OS $ARCH) · weeks 1-$THROUGH"
  case "$PLATFORM" in
    macos)
      [ "$ARCH" = "arm64" ] || info "note: tested on Apple Silicon; Intel macOS should work but is unverified"
      ensure_brew || exit 1
      ;;
    debian) info "using apt-get; sudo will be requested" ;;
    *)
      printf '%sUnsupported platform: %s %s%s\n' "$C_RED" "$OS" "$ARCH" "$C_OFF"
      printf 'Supported: macOS (Apple Silicon) and Debian/Ubuntu.\n'
      printf 'On Windows use WSL2 with Ubuntu 22.04+ and run this inside it.\n'
      exit 1
      ;;
  esac

  hdr "System tools"
  while IFS='|' read -r key bin week apt_pkg brew_pkg label; do
    [ -z "$key" ] && continue
    [ "$week" -gt "$THROUGH" ] && continue
    if have "$bin"; then
      printf '  %s%-14s%s %sok%s %s\n' "$C_BOLD" "$key" "$C_OFF" "$C_GREEN" "$C_OFF" "${C_DIM}already installed${C_OFF}"
    else
      printf '  %s%-14s%s installing… %s(week %s: %s)%s\n' "$C_BOLD" "$key" "$C_OFF" "$C_DIM" "$week" "$label" "$C_OFF"
      install_tool "$key" "$bin" "$apt_pkg" "$brew_pkg" \
        || printf '  %s%-14s%s %sfailed — install by hand%s\n' "$C_BOLD" "$key" "$C_OFF" "$C_YEL" "$C_OFF"
    fi
  done <<< "$(printf '%s\n' "$TOOLS" | sed '/^$/d')"

  setup_python_env

  hdr "Done"
  say "Now run:  ./bootstrap.sh --check"
  say ""
  say "Activate the Python environment in a shell with:"
  say "  source .venv/bin/activate"
  say "The lab Makefiles find .venv on their own, so you do not have to."
}

if [ "$MODE" = "check" ]; then
  check_all
  exit $?
fi
install_all
