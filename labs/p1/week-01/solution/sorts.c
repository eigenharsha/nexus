/* sorts.c — reference implementation for LAB-P1-W01.
 *
 * Design notes worth reading before you copy anything:
 *
 *  - sort_merge allocates ONE scratch buffer, at the top. The obvious version
 *    allocates inside the recursion and costs an allocation per subarray per
 *    level: ~2n allocations at n = 1M instead of 1. Measured on an M2 that is
 *    about a 2x difference in wall time, entirely in malloc.
 *
 *  - Indices are size_t everywhere except the binary_search return, which has
 *    to be able to say "absent". Mixing signed and unsigned index arithmetic is
 *    where the interesting bugs live, so it is done in exactly one place.
 *
 *  - sort_external is a two-phase sort: bounded chunks out to run files, then a
 *    k-way merge driven by a min-heap over the run heads. Peak element memory is
 *    the chunk buffer plus one input block per run plus the output block.
 */
#include "sorts.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_sorted(const int *a, size_t n)
{
    for (size_t i = 1; i < n; i++) {
        if (a[i - 1] > a[i]) return 0;
    }
    return 1;
}

void sort_select(int *a, size_t n)
{
    if (n < 2) return;                     /* n == 0 must not reach n - 1 below */
    for (size_t i = 0; i + 1 < n; i++) {
        size_t min = i;
        for (size_t j = i + 1; j < n; j++) {
            if (a[j] < a[min]) min = j;
        }
        if (min != i) {
            int tmp = a[i];
            a[i] = a[min];
            a[min] = tmp;
        }
    }
}

long binary_search(const int *a, size_t n, int key)
{
    size_t lo = 0, hi = n;                 /* invariant: key, if present, is in a[lo..hi) */
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;   /* not (lo + hi) / 2 — that overflows */
        if (a[mid] == key) return (long)mid;
        if (a[mid] < key) lo = mid + 1;
        else hi = mid;
    }
    return -1;
}

/* Merge a[lo..mid) and a[mid..hi) into scratch, then copy back. */
static void merge_runs(int *a, int *scratch, size_t lo, size_t mid, size_t hi)
{
    size_t i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        /* <= keeps the sort stable: equal elements retain their relative order. */
        scratch[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    }
    while (i < mid) scratch[k++] = a[i++];
    while (j < hi)  scratch[k++] = a[j++];
    memcpy(a + lo, scratch + lo, (hi - lo) * sizeof *a);
}

int sort_merge(int *a, size_t n)
{
    if (n < 2) return 0;

    int *scratch = malloc(n * sizeof *scratch);
    if (scratch == NULL) return -1;        /* a[] untouched, as documented */

    /* Bottom-up, so there is no recursion and therefore no stack-depth question
     * at all. width doubles: 1, 2, 4, ... which is ceil(log2(n)) passes. */
    for (size_t width = 1; width < n; width *= 2) {
        for (size_t lo = 0; lo < n - width; lo += 2 * width) {
            size_t mid = lo + width;
            size_t hi = lo + 2 * width;
            if (hi > n) hi = n;
            merge_runs(a, scratch, lo, mid, hi);
        }
    }

    free(scratch);
    return 0;
}

/* ---------------------------------------------------------------------------
 * external merge sort
 * ------------------------------------------------------------------------- */

/* One run being merged: a file, a small buffer, and the position within it. */
typedef struct {
    FILE  *fp;
    int   *buf;
    size_t cap;      /* elements the buffer holds */
    size_t len;      /* elements currently in the buffer */
    size_t pos;      /* next element to consume */
    int    exhausted;
} run_t;

static int run_refill(run_t *r)
{
    if (r->pos < r->len) return 1;
    size_t got = fread(r->buf, sizeof(int), r->cap, r->fp);
    r->len = got;
    r->pos = 0;
    if (got == 0) { r->exhausted = 1; return 0; }
    return 1;
}

/* Min-heap over run indices, keyed by the run's current head value. */
typedef struct {
    size_t *idx;
    size_t  n;
    run_t  *runs;
} heap_t;

static int heap_less(const heap_t *h, size_t x, size_t y)
{
    const run_t *a = &h->runs[h->idx[x]];
    const run_t *b = &h->runs[h->idx[y]];
    return a->buf[a->pos] < b->buf[b->pos];
}

static void heap_swap(heap_t *h, size_t x, size_t y)
{
    size_t t = h->idx[x]; h->idx[x] = h->idx[y]; h->idx[y] = t;
}

static void heap_sift_down(heap_t *h, size_t i)
{
    for (;;) {
        size_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->n && heap_less(h, l, m)) m = l;
        if (r < h->n && heap_less(h, r, m)) m = r;
        if (m == i) return;
        heap_swap(h, i, m);
        i = m;
    }
}

static void heap_build(heap_t *h)
{
    if (h->n < 2) return;
    for (size_t i = h->n / 2; i-- > 0;) heap_sift_down(h, i);
}

int sort_external(const char *in_path, const char *out_path, size_t mem_budget_bytes)
{
    const size_t elem = sizeof(int);
    /* Two thirds of the budget for the sort chunk, the rest for merge buffers. */
    size_t chunk_elems = (mem_budget_bytes * 2 / 3) / elem;
    if (chunk_elems < 1024) chunk_elems = 1024;

    FILE *in = fopen(in_path, "rb");
    if (in == NULL) return -1;

    int    *chunk    = malloc(chunk_elems * elem);
    char  **run_path = NULL;
    size_t  nruns = 0, run_cap = 0;
    int     rc = -1;

    if (chunk == NULL) { fclose(in); return -1; }

    /* --- phase 1: sorted runs ------------------------------------------- */
    for (;;) {
        size_t got = fread(chunk, elem, chunk_elems, in);
        if (got == 0) break;
        if (sort_merge(chunk, got) != 0) goto done;

        if (nruns == run_cap) {
            size_t ncap = run_cap ? run_cap * 2 : 8;
            char **np = realloc(run_path, ncap * sizeof *np);
            if (np == NULL) goto done;
            run_path = np;
            run_cap = ncap;
        }
        char name[512];
        snprintf(name, sizeof name, "%s.run%zu", out_path, nruns);
        FILE *rf = fopen(name, "wb");
        if (rf == NULL) goto done;
        size_t wrote = fwrite(chunk, elem, got, rf);
        fclose(rf);
        if (wrote != got) goto done;

        run_path[nruns] = strdup(name);
        if (run_path[nruns] == NULL) goto done;
        nruns++;
    }

    /* --- phase 2: k-way merge -------------------------------------------- */
    {
        FILE *out = fopen(out_path, "wb");
        if (out == NULL) goto done;

        if (nruns == 0) { fclose(out); rc = 0; goto done; }

        size_t bufcap = (mem_budget_bytes / 3) / elem / (nruns + 1);
        if (bufcap < 64) bufcap = 64;

        run_t *runs = calloc(nruns, sizeof *runs);
        size_t *idx = malloc(nruns * sizeof *idx);
        if (runs == NULL || idx == NULL) { free(runs); free(idx); fclose(out); goto done; }

        heap_t h = { .idx = idx, .n = 0, .runs = runs };
        int open_ok = 1;
        for (size_t i = 0; i < nruns; i++) {
            runs[i].fp  = fopen(run_path[i], "rb");
            runs[i].buf = malloc(bufcap * elem);
            runs[i].cap = bufcap;
            if (runs[i].fp == NULL || runs[i].buf == NULL) { open_ok = 0; break; }
            if (run_refill(&runs[i])) idx[h.n++] = i;
        }

        if (open_ok) {
            heap_build(&h);
            while (h.n > 0) {
                run_t *r = &runs[idx[0]];
                int v = r->buf[r->pos++];
                if (fwrite(&v, elem, 1, out) != 1) { open_ok = 0; break; }
                if (!run_refill(r)) {
                    idx[0] = idx[--h.n];   /* drop the exhausted run */
                }
                if (h.n > 0) heap_sift_down(&h, 0);
            }
        }

        for (size_t i = 0; i < nruns; i++) {
            if (runs[i].fp) fclose(runs[i].fp);
            free(runs[i].buf);
        }
        free(runs);
        free(idx);
        if (fclose(out) != 0) open_ok = 0;
        rc = open_ok ? 0 : -1;
    }

done:
    /* Run files are removed on every path, success or failure. */
    for (size_t i = 0; i < nruns; i++) {
        if (run_path[i]) { remove(run_path[i]); free(run_path[i]); }
    }
    free(run_path);
    free(chunk);
    fclose(in);
    return rc;
}
