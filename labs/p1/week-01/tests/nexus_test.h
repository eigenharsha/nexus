/* nexus_test.h — a 90-line test harness. No dependencies, TAP-ish output.
 *
 *   #include "nexus_test.h"
 *   static void test_thing(void) { NX_ASSERT_EQ_INT(2 + 2, 4); }
 *   int main(void) { NX_RUN(test_thing); return NX_SUMMARY(); }
 *
 * Track gating: the build defines NEXUS_TRACK_LEVEL as 1 (basic), 2 (standard) or 3 (hard).
 *   NX_RUN_AT(2, test_merge_sort);   -> only runs at standard and above
 */
#ifndef NEXUS_TEST_H
#define NEXUS_TEST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef NEXUS_TRACK_LEVEL
#define NEXUS_TRACK_LEVEL 2
#endif

static int nx_pass = 0;
static int nx_fail = 0;
static int nx_skip = 0;
static int nx_case_failed = 0;
static const char *nx_current = "(none)";

#define NX_C_RED   "\033[31m"
#define NX_C_GREEN "\033[32m"
#define NX_C_DIM   "\033[2m"
#define NX_C_OFF   "\033[0m"

static void nx_fail_at(const char *file, int line, const char *expr, const char *detail)
{
    nx_fail++;
    nx_case_failed = 1;
    fprintf(stderr, NX_C_RED "  not ok" NX_C_OFF "  %s\n            %s:%d  %s\n",
            nx_current, file, line, expr);
    if (detail && detail[0]) fprintf(stderr, "            %s\n", detail);
}

#define NX_ASSERT(cond)                                                        \
    do {                                                                       \
        if (cond) { nx_pass++; }                                               \
        else { nx_fail_at(__FILE__, __LINE__, #cond, ""); }                    \
    } while (0)

#define NX_ASSERT_MSG(cond, msg)                                               \
    do {                                                                       \
        if (cond) { nx_pass++; }                                               \
        else { nx_fail_at(__FILE__, __LINE__, #cond, (msg)); }                 \
    } while (0)

#define NX_ASSERT_EQ_INT(a, b)                                                 \
    do {                                                                       \
        long long nx_a = (long long)(a), nx_b = (long long)(b);                \
        if (nx_a == nx_b) { nx_pass++; }                                       \
        else {                                                                 \
            char nx_buf[128];                                                  \
            snprintf(nx_buf, sizeof nx_buf, "expected %lld, got %lld", nx_b, nx_a); \
            nx_fail_at(__FILE__, __LINE__, #a " == " #b, nx_buf);              \
        }                                                                      \
    } while (0)

#define NX_ASSERT_EQ_DBL(a, b, tol)                                            \
    do {                                                                       \
        double nx_a = (double)(a), nx_b = (double)(b);                         \
        if (fabs(nx_a - nx_b) <= (tol)) { nx_pass++; }                         \
        else {                                                                 \
            char nx_buf[160];                                                  \
            snprintf(nx_buf, sizeof nx_buf, "expected %g +/- %g, got %g", nx_b, (double)(tol), nx_a); \
            nx_fail_at(__FILE__, __LINE__, #a " ~= " #b, nx_buf);              \
        }                                                                      \
    } while (0)

#define NX_ASSERT_STR(a, b)                                                    \
    do {                                                                       \
        const char *nx_a = (a), *nx_b = (b);                                   \
        if (nx_a && nx_b && strcmp(nx_a, nx_b) == 0) { nx_pass++; }            \
        else {                                                                 \
            char nx_buf[256];                                                  \
            snprintf(nx_buf, sizeof nx_buf, "expected \"%s\", got \"%s\"",     \
                     nx_b ? nx_b : "(null)", nx_a ? nx_a : "(null)");          \
            nx_fail_at(__FILE__, __LINE__, #a " == " #b, nx_buf);              \
        }                                                                      \
    } while (0)

#define NX_RUN(fn)                                                             \
    do {                                                                       \
        nx_current = #fn;                                                      \
        nx_case_failed = 0;                                                    \
        fn();                                                                  \
        if (!nx_case_failed) printf(NX_C_GREEN "  ok" NX_C_OFF "      %s\n", #fn); \
    } while (0)

#define NX_RUN_AT(level, fn)                                                   \
    do {                                                                       \
        if (NEXUS_TRACK_LEVEL >= (level)) { NX_RUN(fn); }                      \
        else { nx_skip++; printf(NX_C_DIM "  skip    %s (needs track level %d)" NX_C_OFF "\n", #fn, (level)); } \
    } while (0)

static int nx_summary(void)
{
    printf("\n  %d assertions passed, %d failed, %d cases skipped\n", nx_pass, nx_fail, nx_skip);
    if (nx_fail == 0 && nx_pass == 0) {
        fprintf(stderr, NX_C_RED "  no assertions ran — that is a failure, not a pass\n" NX_C_OFF);
        return 1;
    }
    return nx_fail == 0 ? 0 : 1;
}
#define NX_SUMMARY() nx_summary()

#endif /* NEXUS_TEST_H */
