/* sorts.c — YOUR WORK GOES HERE.
 *
 * basic track:    fill in the two TODOs below (sort_select, binary_search).
 * standard track: delete this file and write all four functions from scratch.
 * hard track:     plus sort_external.
 *
 * Build with:  make verify            (adds -Wall -Wextra -fsanitize=address,undefined)
 */
#include "sorts.h"

#include <stdlib.h>
#include <string.h>

int is_sorted(const int *a, size_t n)
{
    for (size_t i = 1; i < n; i++) {
        if (a[i - 1] > a[i]) return 0;
    }
    return 1;
}

/* -------------------------------------------------------------------------
 * TODO 1 — selection sort.
 *
 * For each position i, find the index of the smallest element in a[i..n)
 * and swap it into position i.
 *
 * Watch: n == 0. `size_t` is unsigned, so `n - 1` when n == 0 is a very large
 * number and your loop runs forever (or reads out of bounds, which ASan will
 * tell you about in some detail).
 * ------------------------------------------------------------------------- */
void sort_select(int *a, size_t n)
{
    (void)a;
    (void)n;
    /* TODO: implement selection sort here. */
}

/* -------------------------------------------------------------------------
 * TODO 2 — binary search.
 *
 * Maintain the invariant: if key is present, it is in a[lo..hi).
 * Return the index, or -1.
 *
 * Watch: compute the midpoint as lo + (hi - lo) / 2, not (lo + hi) / 2.
 * The second form overflows for large indices, and that overflow was a real
 * bug in java.util.Arrays for nine years.
 * ------------------------------------------------------------------------- */
long binary_search(const int *a, size_t n, int key)
{
    (void)a;
    (void)n;
    (void)key;
    /* TODO: implement binary search here. */
    return -1;
}

/* -------------------------------------------------------------------------
 * standard track — merge sort.
 * Allocate ONE scratch buffer at the top, not one per recursion level.
 * Free it on every return path, including the failure paths.
 * ------------------------------------------------------------------------- */
int sort_merge(int *a, size_t n)
{
    (void)a;
    (void)n;
    return -1; /* not implemented */
}

/* -------------------------------------------------------------------------
 * hard track — external merge sort.
 * Read a bounded chunk, sort it, spill it to a run file, repeat; then k-way
 * merge the run files with a min-heap. Clean the run files up on every path.
 * ------------------------------------------------------------------------- */
int sort_external(const char *in_path, const char *out_path, size_t mem_budget_bytes)
{
    (void)in_path;
    (void)out_path;
    (void)mem_budget_bytes;
    return -1; /* not implemented */
}
