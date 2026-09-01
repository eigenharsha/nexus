# gnuplot bench/plot.gnuplot
# Log-log runtime vs n, with a power-law fit so you can read the exponent off
# the fit rather than guess it from the shape of the line.
set datafile separator ","
set terminal pngcairo size 1000,700 font "Helvetica,12"
set output "bench/runtime.png"
set logscale xy
set xlabel "n (elements)"
set ylabel "time (ns), minimum of 3 trials"
set title "LAB-P1-W01 — sorting runtime, log-log"
set key left top
set grid

# Minimum of the trials for each (algo, n).
! awk -F, 'NR>1 { k=$1","$2; if (!(k in m) || $4+0 < m[k]) m[k]=$4+0 } \
           END { for (k in m) print k","m[k] }' bench/results.solution.csv \
  | sort -t, -k1,1 -k2,2n > bench/min.csv

sel(x) = a1 * x**b1
mrg(x) = a2 * x**b2
a1 = 1; b1 = 2; a2 = 1; b2 = 1
fit sel(x) "< grep '^selection,' bench/min.csv" using 2:3 via a1, b1
fit mrg(x) "< grep '^merge,'     bench/min.csv" using 2:3 via a2, b2

plot "< grep '^selection,' bench/min.csv" using 2:3 with points pt 7 title "selection", \
     sel(x) with lines title sprintf("fit: %.2e * n^{%.3f}", a1, b1), \
     "< grep '^merge,'     bench/min.csv" using 2:3 with points pt 5 title "merge", \
     mrg(x) with lines title sprintf("fit: %.2e * n^{%.3f}", a2, b2)

print sprintf("selection fitted exponent: %.3f", b1)
print sprintf("merge     fitted exponent: %.3f", b2)
