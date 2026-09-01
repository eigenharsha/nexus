/* sorts.h — the toolkit's public surface. Do not change these signatures:
 * tests/test_sorts.c is compiled against this header.
 */
#ifndef SORTS_H
#define SORTS_H

#include <stddef.h>

/* 1 if a[0..n) is non-decreasing, 0 otherwise. n == 0 and n == 1 are sorted. */
int is_sorted(const int *a, size_t n);

/* Selection sort, ascending, in place. */
void sort_select(int *a, size_t n);

/* Merge sort, ascending, in place from the caller's point of view.
 * Returns 0 on success, -1 if the scratch buffer could not be allocated
 * (in which case a[] is left untouched). */
int sort_merge(int *a, size_t n);

/* Index of key in the sorted array a[0..n), or -1 if absent.
 * With duplicates, any matching index is acceptable. */
long binary_search(const int *a, size_t n, int key);

/* External merge sort over a file of native-endian int32 values.
 * Never holds more than mem_budget_bytes of element data in memory.
 * Returns 0 on success, -1 on I/O or allocation failure. */
int sort_external(const char *in_path, const char *out_path, size_t mem_budget_bytes);

#endif /* SORTS_H */
