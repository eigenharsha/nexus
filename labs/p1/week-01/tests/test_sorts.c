/* Acceptance tests for LAB-P1-W01 — Sorting & Search Toolkit in C.
 *
 * Compiled against whichever implementation directory `make verify` selects:
 *   make verify              -> starter/   (red, that is the point)
 *   make verify IMPL=solution -> solution/ (green)
 *
 * Every case runs under -fsanitize=address,undefined with detect_leaks=1, so a
 * leaked scratch buffer is a test failure, not a warning you can scroll past.
 */
#include "nexus_test.h"
#include "sorts.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Deterministic PRNG so a failing run is reproducible. xorshift32. */
static unsigned int rng_state = 0x12345678u;
static unsigned int rng_next(void)
{
    unsigned int x = rng_state;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    return (rng_state = x);
}

static int *make_random(size_t n)
{
    int *a = malloc(n * sizeof *a);
    if (!a) { fprintf(stderr, "test allocation failed\n"); exit(2); }
    for (size_t i = 0; i < n; i++) a[i] = (int)(rng_next() % 1000000u) - 500000;
    return a;
}

/* ------------------------------------------------------------------ basic */

static void test_is_sorted(void)
{
    int asc[]  = {1, 2, 2, 3};
    int desc[] = {3, 2, 1};
    NX_ASSERT(is_sorted(asc, 4));
    NX_ASSERT(!is_sorted(desc, 3));
    NX_ASSERT_MSG(is_sorted(NULL, 0), "an empty array is sorted");
    NX_ASSERT_MSG(is_sorted(asc, 1), "a one-element array is sorted");
}

static void test_select_sorts(void)
{
    int a[] = {5, 3, 9, 1, 3, -7, 0};
    sort_select(a, 7);
    NX_ASSERT_MSG(is_sorted(a, 7), "sort_select did not produce a sorted array");
    NX_ASSERT_EQ_INT(a[0], -7);
    NX_ASSERT_EQ_INT(a[6], 9);
}

static void test_select_edge_cases(void)
{
    int one[] = {42};
    sort_select(NULL, 0);              /* must not crash or read anything */
    sort_select(one, 1);
    NX_ASSERT_EQ_INT(one[0], 42);

    int equal[] = {7, 7, 7, 7};
    sort_select(equal, 4);
    NX_ASSERT(is_sorted(equal, 4));

    int rev[] = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
    sort_select(rev, 10);
    NX_ASSERT(is_sorted(rev, 10));
    NX_ASSERT_EQ_INT(rev[0], 0);
}

static void test_select_is_a_permutation(void)
{
    /* Sorting must not invent or lose elements — the failure mode a naive
     * "swap with the wrong index" bug produces. */
    size_t n = 2000;
    int *a = make_random(n);
    long long before = 0, after = 0;
    for (size_t i = 0; i < n; i++) before += a[i];
    sort_select(a, n);
    for (size_t i = 0; i < n; i++) after += a[i];
    NX_ASSERT(is_sorted(a, n));
    NX_ASSERT_MSG(before == after, "sum changed: elements were lost or duplicated");
    free(a);
}

static void test_binary_search_finds(void)
{
    int a[] = {-9, -1, 0, 3, 7, 7, 11, 40};
    NX_ASSERT_EQ_INT(binary_search(a, 8, -9), 0);
    NX_ASSERT_EQ_INT(binary_search(a, 8, 40), 7);
    NX_ASSERT_EQ_INT(binary_search(a, 8, 3), 3);
    long dup = binary_search(a, 8, 7);
    NX_ASSERT_MSG(dup == 4 || dup == 5, "any index of a duplicate is acceptable");
}

static void test_binary_search_absent(void)
{
    int a[] = {1, 3, 5, 7};
    NX_ASSERT_EQ_INT(binary_search(a, 4, 0), -1);
    NX_ASSERT_EQ_INT(binary_search(a, 4, 4), -1);
    NX_ASSERT_EQ_INT(binary_search(a, 4, 100), -1);
    NX_ASSERT_MSG(binary_search(NULL, 0, 1) == -1, "empty array: must return -1, not crash");
    int one[] = {5};
    NX_ASSERT_EQ_INT(binary_search(one, 1, 5), 0);
    NX_ASSERT_EQ_INT(binary_search(one, 1, 6), -1);
}

static void test_binary_search_all_equal_terminates(void)
{
    /* A wrong loop condition here hangs forever rather than failing. */
    size_t n = 4096;
    int *a = malloc(n * sizeof *a);
    for (size_t i = 0; i < n; i++) a[i] = 5;
    NX_ASSERT(binary_search(a, n, 5) >= 0);
    NX_ASSERT_EQ_INT(binary_search(a, n, 4), -1);
    free(a);
}

/* --------------------------------------------------------------- standard */

static void test_merge_sorts(void)
{
    int a[] = {5, 3, 9, 1, 3, -7, 0};
    NX_ASSERT_EQ_INT(sort_merge(a, 7), 0);
    NX_ASSERT(is_sorted(a, 7));
    NX_ASSERT_EQ_INT(a[0], -7);
}

static void test_merge_edge_cases(void)
{
    int one[] = {42};
    NX_ASSERT_EQ_INT(sort_merge(NULL, 0), 0);
    NX_ASSERT_EQ_INT(sort_merge(one, 1), 0);
    NX_ASSERT_EQ_INT(one[0], 42);

    int two[] = {2, 1};
    NX_ASSERT_EQ_INT(sort_merge(two, 2), 0);
    NX_ASSERT_EQ_INT(two[0], 1);
    NX_ASSERT_EQ_INT(two[1], 2);
}

static void test_merge_odd_length(void)
{
    /* Bottom-up merges get the tail wrong when n is not a power of two.
     * 7, 13 and 1000 are the three sizes that catch it. */
    size_t sizes[] = {3, 7, 13, 1000, 1023, 1024, 1025};
    for (size_t s = 0; s < sizeof sizes / sizeof *sizes; s++) {
        size_t n = sizes[s];
        int *a = make_random(n);
        NX_ASSERT_EQ_INT(sort_merge(a, n), 0);
        NX_ASSERT_MSG(is_sorted(a, n), "sort_merge failed at a non-power-of-two length");
        free(a);
    }
}

static void test_merge_large_and_is_permutation(void)
{
    size_t n = 200000;
    int *a = make_random(n);
    long long before = 0, after = 0;
    for (size_t i = 0; i < n; i++) before += a[i];
    NX_ASSERT_EQ_INT(sort_merge(a, n), 0);
    for (size_t i = 0; i < n; i++) after += a[i];
    NX_ASSERT(is_sorted(a, n));
    NX_ASSERT_MSG(before == after, "sum changed: sort_merge lost or duplicated elements");
    free(a);
}

static void test_merge_agrees_with_select(void)
{
    size_t n = 3000;
    int *a = make_random(n);
    int *b = malloc(n * sizeof *b);
    memcpy(b, a, n * sizeof *b);
    sort_select(a, n);
    NX_ASSERT_EQ_INT(sort_merge(b, n), 0);
    NX_ASSERT_MSG(memcmp(a, b, n * sizeof *a) == 0,
                  "the two sorts disagree on the same input");
    free(a);
    free(b);
}

static void test_search_over_sorted_million(void)
{
    size_t n = 1000000;
    int *a = malloc(n * sizeof *a);
    for (size_t i = 0; i < n; i++) a[i] = (int)i * 2;   /* every even number */
    for (size_t probe = 0; probe < 500; probe++) {
        size_t i = rng_next() % n;
        NX_ASSERT_EQ_INT(binary_search(a, n, (int)i * 2), (long)i);
    }
    NX_ASSERT_EQ_INT(binary_search(a, n, 1), -1);       /* odd: never present */
    free(a);
}

/* ------------------------------------------------------------------- hard */

static void write_random_file(const char *path, size_t n)
{
    FILE *f = fopen(path, "wb");
    if (!f) { fprintf(stderr, "cannot write %s\n", path); exit(2); }
    for (size_t i = 0; i < n; i++) {
        int v = (int)(rng_next() % 2000000u) - 1000000;
        fwrite(&v, sizeof v, 1, f);
    }
    fclose(f);
}

static void test_external_sort(void)
{
    const char *in = "build/ext_in.bin";
    const char *out = "build/ext_out.bin";
    size_t n = 300000;                      /* 1.2 MB of data ... */
    size_t budget = 128 * 1024;             /* ... through a 128 KB budget */

    write_random_file(in, n);
    int rc = sort_external(in, out, budget);
    NX_ASSERT_EQ_INT(rc, 0);
    if (rc != 0) return;

    FILE *f = fopen(out, "rb");
    NX_ASSERT_MSG(f != NULL, "no output file was produced");
    if (!f) return;

    size_t count = 0;
    int prev = 0, v;
    long long sum = 0;
    int ordered = 1;
    while (fread(&v, sizeof v, 1, f) == 1) {
        if (count > 0 && v < prev) ordered = 0;
        prev = v;
        sum += v;
        count++;
    }
    fclose(f);
    NX_ASSERT_MSG(ordered, "the external sort's output is not in order");
    NX_ASSERT_EQ_INT((long long)count, (long long)n);

    /* Same multiset as the input. */
    FILE *g = fopen(in, "rb");
    long long insum = 0;
    while (fread(&v, sizeof v, 1, g) == 1) insum += v;
    fclose(g);
    NX_ASSERT_MSG(insum == sum, "the external sort lost or duplicated elements");

    remove(in);
    remove(out);
}

static void test_external_cleans_up_run_files(void)
{
    const char *in = "build/ext2_in.bin";
    const char *out = "build/ext2_out.bin";
    write_random_file(in, 50000);
    NX_ASSERT_EQ_INT(sort_external(in, out, 64 * 1024), 0);

    /* Temporary run files are named <out>.runN. None may survive. */
    char probe[512];
    int leftovers = 0;
    for (int i = 0; i < 64; i++) {
        snprintf(probe, sizeof probe, "%s.run%d", out, i);
        FILE *f = fopen(probe, "rb");
        if (f) { leftovers++; fclose(f); remove(probe); }
    }
    NX_ASSERT_EQ_INT(leftovers, 0);
    remove(in);
    remove(out);
}

static void test_external_empty_input(void)
{
    const char *in = "build/ext3_in.bin";
    const char *out = "build/ext3_out.bin";
    FILE *f = fopen(in, "wb"); fclose(f);
    NX_ASSERT_EQ_INT(sort_external(in, out, 64 * 1024), 0);
    remove(in);
    remove(out);
}

int main(void)
{
    printf("\nLAB-P1-W01 · sorting & search toolkit\n\n");

    NX_RUN_AT(1, test_is_sorted);
    NX_RUN_AT(1, test_select_sorts);
    NX_RUN_AT(1, test_select_edge_cases);
    NX_RUN_AT(1, test_select_is_a_permutation);
    NX_RUN_AT(1, test_binary_search_finds);
    NX_RUN_AT(1, test_binary_search_absent);
    NX_RUN_AT(1, test_binary_search_all_equal_terminates);

    NX_RUN_AT(2, test_merge_sorts);
    NX_RUN_AT(2, test_merge_edge_cases);
    NX_RUN_AT(2, test_merge_odd_length);
    NX_RUN_AT(2, test_merge_large_and_is_permutation);
    NX_RUN_AT(2, test_merge_agrees_with_select);
    NX_RUN_AT(2, test_search_over_sorted_million);

    NX_RUN_AT(3, test_external_sort);
    NX_RUN_AT(3, test_external_cleans_up_run_files);
    NX_RUN_AT(3, test_external_empty_input);

    return NX_SUMMARY();
}
