#!/usr/bin/env bash
# Preview the GitHub Pages build locally.
#   ./serve.sh          serve the existing build on :8080
#   ./serve.sh --build  rebuild from site/*.mdx first, then serve
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--build" ]]; then
  source .venv/bin/activate
  python3 publish/convert.py
  (cd publish && python3 -m mkdocs build)
fi

[[ -d _site ]] || { echo "no _site/ - run: ./serve.sh --build"; exit 1; }
echo "serving http://127.0.0.1:8080  (ctrl-c to stop)"
cd _site && exec python3 -m http.server 8080 --bind 127.0.0.1
