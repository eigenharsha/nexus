# Set up your machine

One script. macOS on Apple Silicon, or Debian/Ubuntu Linux. Do this before Week 1 — the first
lab compiles C with AddressSanitizer on day one and you do not want to be fighting a toolchain
at the same time.

```bash
git clone https://github.com/nexus-course/nexus.git
cd nexus
./bootstrap.sh
./bootstrap.sh --check
```

Every line of `--check` should be green before Week 1. If one is not, that is the first
debugging exercise of the course, and the output tells you which tool and which week needs it.

## What it does

| | |
|---|---|
| Installs system tools | via Homebrew on macOS, `apt-get` on Debian/Ubuntu |
| Creates `.venv/` | Python 3.12, managed by [uv](https://docs.astral.sh/uv/) |
| Installs Python packages | pinned per week — `pytest` in week 3, `torch` in week 21, `peft` in week 26 |
| Never uninstalls anything | it will not touch a tool you already have |
| Is idempotent | run it as many times as you like; the second run is a no-op |

The lab `Makefile`s find `.venv/` on their own by walking up to the directory containing
`bootstrap.sh`. You never have to remember to activate anything.

## Options

```bash
./bootstrap.sh                  # everything, all 34 weeks
./bootstrap.sh --through 8      # only what weeks 1-8 need  (a much smaller download)
./bootstrap.sh --check          # verify only; green/red per tool, installs nothing
./bootstrap.sh --check --through 8
./bootstrap.sh --dry-run        # print every command it would run, run none
./bootstrap.sh --no-color       # for CI logs
./bootstrap.sh --help
```

`--through N` is the useful one on a slow connection or a small disk. PyTorch alone is about
2.5 GB; if you are in week 3 there is no reason to have it yet.

## What gets installed, and the week you first need it

| Tool | Version | First used | Why |
|---|---|---|---|
| `cc` / `clang`, `make` | C17 | Week 1 | the whole first week is C |
| `valgrind` | latest | Week 1 | leak checking (**Linux only** — see below) |
| `git`, `vim`, `tmux`, `jq` | latest | Week 2 | terminal literacy week |
| `shellcheck`, `bats` | latest | Week 2 | the week-2 lab is graded by `bats` |
| `uv` + Python | 3.12 | Week 3 | every Python lab from here on |
| Node | 20 LTS | Week 5 | the one frontend week |
| Docker | 24+ | Week 7 | Postgres runs in a container; week 23 builds images |
| `psql` | 16 client | Week 7 | SQL weeks |
| Wireshark / `tshark` | latest | Week 10 | packet-level evidence for the socket lab |
| `gnuplot` | latest | Week 13 | complexity plots from the benchmark harness |
| `kind`, `kubectl` | latest | Week 24 | local Kubernetes cluster |
| Ollama | latest | Week 26 | local model serving, and the CPU fallback path |
| PyTorch | 2.x | Week 21 | the deep learning half |

## Platform notes

### macOS (Apple Silicon)

Homebrew is the one prerequisite `bootstrap.sh` will not install for you, because it modifies
your shell profile and asks for your password. If you do not have it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Valgrind does not work on Apple Silicon.** There is no maintained arm64 macOS port. Every lab
that asks for a memory check therefore uses `-fsanitize=address,undefined` instead, which
catches the same class of bug and is what the Makefiles run by default:

```bash
make memcheck        # valgrind if you have it, AddressSanitizer + LeakSanitizer if you do not
```

`--check` shows valgrind as `n/a` rather than red on macOS. That is correct, not a failure.

Docker Desktop needs to be launched by hand once after install before the daemon will answer.

### Debian / Ubuntu

`apt-get` steps use `sudo` and will prompt. After the Docker install you must log out and back
in for your user's new `docker` group membership to apply — otherwise every `docker` command
says "permission denied" and it looks like the install failed.

Ubuntu 22.04 or newer. On 20.04 the system Python is too old for some wheels; `uv` installs its
own Python 3.12, so the venv is fine, but a few system packages are not.

### Windows

Use WSL2 with Ubuntu 22.04+ and run everything inside it. Native Windows is not supported.
Sockets (week 10), Valgrind (week 1), and Kubernetes (week 24) all behave differently in ways
that will cost you hours you should be spending on the actual material.

## Cost

The whole 34 weeks is designed to cost **under $50** of cloud spend. Everything that can run
locally does. The GPU weeks (21, 22, 25, 26) have a documented CPU or free-Colab fallback path;
they are slower, not impossible. Nothing in the course requires a paid model API — week 26
serves a local model with Ollama and vLLM, and the agent weeks run against it.

## When something is red

1. Re-run `./bootstrap.sh`. About half of all failures are a transient download.
2. Run `./bootstrap.sh --dry-run` and execute the failing command by hand — the error you get
   directly is almost always clearer than the one the script swallows.
3. If a tool is only needed in week 24 and you are in week 3, ignore it and move on. Use
   `--check --through <your week>` so the output only shows what actually blocks you today.

## Verifying a lab works

```bash
cd labs/p1/week-01
make help
make verify IMPL=solution    # should be green
make verify                  # should be red — that is the starter, and it is your job
make contract                # asserts both of the above in one command
```

If `make verify IMPL=solution` is red on a fresh clone, that is a bug in the course, not in your
machine. Open an issue with the output of `./bootstrap.sh --check`.
