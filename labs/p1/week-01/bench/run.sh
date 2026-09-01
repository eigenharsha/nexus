#!/usr/bin/env sh
# Build and run the benchmark for one implementation directory.
#   sh bench/run.sh solution
# Optimized build (-O2, no sanitizers): sanitizers cost 2-20x and would make
# every number meaningless.
set -eu
IMPL="${1:-solution}"
OUT="bench/results.$IMPL.csv"
mkdir -p build bench
cc -std=c17 -Wall -Wextra -O2 -I"$IMPL" "$IMPL/bench.c" "$IMPL/sorts.c" -o "build/bench.$IMPL" -lm
"./build/bench.$IMPL" > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT" | tr -d ' ') rows)"
echo
echo "minimum of 3 trials, nanoseconds:"
awk -F, 'NR>1 { k=$1","$2; if (!(k in m) || $4+0 < m[k]) m[k]=$4+0 }
         END { for (k in m) print k","m[k] }' "$OUT" | sort -t, -k1,1 -k2,2n |
  awk -F, 'BEGIN{printf "  %-14s %10s %14s\n","algo","n","ns"} {printf "  %-14s %10s %14s\n",$1,$2,$3}'
echo
echo "next: gnuplot bench/plot.gnuplot   (log-log; fit the exponent)"
