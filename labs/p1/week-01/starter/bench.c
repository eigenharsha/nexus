/* bench.c — the benchmark harness. YOUR WORK (standard track).
 *
 * Required output on stdout, exactly these columns:
 *     algo,n,trial,nanoseconds
 * for algo in {selection, merge, search_x1000}, n from 1,000 to 1,000,000,
 * at least 3 trials per point.
 *
 * Three things that will make your numbers wrong if you skip them:
 *   1. Regenerate the array for every trial. Sorting an already-sorted array
 *      measures something else entirely.
 *   2. Consume the result (a volatile accumulator works) so -O2 cannot delete
 *      the sort as dead code. If merge sort measures 4 ns at n=1M, this is why.
 *   3. Cap selection sort. n=1M is ~10^12 comparisons.
 */
#include "sorts.h"

#include <stdio.h>

int main(void)
{
    printf("algo,n,trial,nanoseconds\n");
    /* TODO: implement the benchmark harness. */
    return 0;
}
