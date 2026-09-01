/* bench.c — the measurement half of the lab. Writes CSV; plot it yourself.
 *
 *   ./bench > bench/results.csv
 *   gnuplot bench/plot.gnuplot
 *
 * Columns: algo,n,trial,nanoseconds
 *
 * Read this before you trust any number it prints:
 *   - The array is regenerated for every trial, so no run benefits from the
 *     previous one having already sorted it.
 *   - The result is consumed (`sink`) so -O2 cannot delete the sort as dead code.
 *     Deleting the benchmark loop is the single most common way to measure zero.
 *   - Three trials per point and the MINIMUM is what you should plot: the minimum
 *     is the closest thing to "the machine with nothing else running".
 */
#include "sorts.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static unsigned int rng_state = 0xC0FFEEu;
static unsigned int rng_next(void)
{
    unsigned int x = rng_state;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    return (rng_state = x);
}

static double now_ns(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e9 + (double)ts.tv_nsec;
}

static volatile long long sink = 0;

int main(int argc, char **argv)
{
    const size_t sizes[]  = {1000, 3000, 10000, 30000, 100000, 300000, 1000000};
    const size_t nsizes   = sizeof sizes / sizeof *sizes;
    const int    trials   = 3;
    /* Selection sort is O(n^2): a million elements is ~10^12 comparisons and
     * you would still be waiting tomorrow. Cap it where it stops being useful. */
    const size_t select_cap = (argc > 1) ? (size_t)strtoul(argv[1], NULL, 10) : 30000;

    printf("algo,n,trial,nanoseconds\n");

    for (size_t s = 0; s < nsizes; s++) {
        size_t n = sizes[s];
        for (int t = 0; t < trials; t++) {
            int *a = malloc(n * sizeof *a);
            if (!a) { fprintf(stderr, "out of memory at n=%zu\n", n); return 1; }

            if (n <= select_cap) {
                for (size_t i = 0; i < n; i++) a[i] = (int)rng_next();
                double t0 = now_ns();
                sort_select(a, n);
                double t1 = now_ns();
                sink += a[n / 2];
                printf("selection,%zu,%d,%.0f\n", n, t, t1 - t0);
            }

            for (size_t i = 0; i < n; i++) a[i] = (int)rng_next();
            double m0 = now_ns();
            (void)sort_merge(a, n);
            double m1 = now_ns();
            sink += a[n / 2];
            printf("merge,%zu,%d,%.0f\n", n, t, m1 - m0);

            /* Search is measured over 1000 probes so the timer has something to
             * resolve; a single binary search is ~200 ns and below clock noise. */
            double b0 = now_ns();
            for (int p = 0; p < 1000; p++) sink += binary_search(a, n, a[rng_next() % n]);
            double b1 = now_ns();
            printf("search_x1000,%zu,%d,%.0f\n", n, t, b1 - b0);

            free(a);
        }
    }

    if (sink == 0x7FFFFFFFFFFFFFFFLL) fprintf(stderr, "impossible\n");
    return 0;
}
