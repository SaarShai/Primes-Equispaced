/*
 * t_negativity_verify.c
 *
 * Fast verification that T(N) < 0 for all N with M(N) = -2,
 * where T(N) = sum_{m=2}^{N} M(floor(N/m)) / m.
 *
 * Uses the hyperbolic method for O(sqrt(N)) evaluation of T(N) per N.
 *
 * Compile: gcc -O3 -o t_negativity_verify t_negativity_verify.c -lm
 * Run: ./t_negativity_verify [LIMIT]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define DEFAULT_LIMIT 10000000

int main(int argc, char *argv[]) {
    long long LIMIT = DEFAULT_LIMIT;
    if (argc > 1) LIMIT = atoll(argv[1]);

    fprintf(stderr, "T(N) negativity verification up to N = %lld\n", LIMIT);

    /* Allocate arrays */
    signed char *mu = calloc(LIMIT + 1, sizeof(signed char));
    int *M = calloc(LIMIT + 1, sizeof(int));
    double *H = calloc(LIMIT + 1, sizeof(double)); /* harmonic numbers */

    if (!mu || !M || !H) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    /* Sieve for mu */
    fprintf(stderr, "Computing Mobius function...\n");
    mu[1] = 1;
    /* We need a sieve for mu. Use linear sieve. */
    int *smallest_prime = calloc(LIMIT + 1, sizeof(int));
    int *prime_list = calloc(LIMIT / 2 + 100, sizeof(int));
    int num_primes = 0;

    for (long long i = 2; i <= LIMIT; i++) {
        if (smallest_prime[i] == 0) {
            smallest_prime[i] = i;
            prime_list[num_primes++] = i;
            mu[i] = -1;
        }
        for (int j = 0; j < num_primes; j++) {
            long long p = prime_list[j];
            if (p > smallest_prime[i] || i * p > LIMIT) break;
            smallest_prime[i * p] = p;
            if (i % p == 0) {
                mu[i * p] = 0;
            } else {
                mu[i * p] = -mu[i];
            }
        }
    }

    /* Compute Mertens function */
    fprintf(stderr, "Computing Mertens function...\n");
    M[0] = 0;
    for (long long n = 1; n <= LIMIT; n++) {
        M[n] = M[n - 1] + mu[n];
    }

    /* Precompute harmonic numbers */
    fprintf(stderr, "Computing harmonic numbers...\n");
    H[0] = 0.0;
    for (long long n = 1; n <= LIMIT; n++) {
        H[n] = H[n - 1] + 1.0 / n;
    }

    free(smallest_prime);
    free(prime_list);

    /* Now verify T(N) < 0 for all N with M(N) = -2 */
    fprintf(stderr, "Checking T(N) for all N with M(N) = -2...\n");

    long long count_checked = 0;
    long long count_positive = 0;
    double max_T = -1e18;
    long long worst_N = 0;

    /* Also check subset where N+1 is prime */
    long long count_prime_checked = 0;
    double max_T_prime = -1e18;
    long long worst_N_prime = 0;

    /* For fast computation: use hyperbolic method
     * T(N) = sum_{m=2}^{N} M(floor(N/m))/m
     *
     * Using the block structure: floor(N/m) takes at most O(sqrt(N)) distinct values.
     * For each value v = floor(N/m), the range of m is (N/(v+1), N/v].
     * The sum of 1/m over this range is H(floor(N/v)) - H(floor(N/(v+1))).
     *
     * T(N) = sum_{v} M(v) * [H(N/v) - H(N/(v+1))] for v such that some m gives fl(N/m)=v
     *       minus the m=1 contribution (if we started from m=1).
     *
     * Actually, we compute:
     * F(N) = sum_{m=1}^{N} M(fl(N/m))/m
     * Then T(N) = F(N) - M(N) = F(N) + 2.
     *
     * For F(N), use the hyperbolic method:
     * F(N) = sum_{m=1}^{U} M(fl(N/m))/m + sum_{d=1}^{V} mu(d)*H(fl(N/d)) - M(U)*H(V)
     * where U = floor(sqrt(N)), V = floor(N/(U+1)).
     */

    clock_t start = clock();
    long long report_interval = LIMIT / 20;
    if (report_interval == 0) report_interval = 1;

    for (long long N = 10; N <= LIMIT; N++) {
        if (M[N] != -2) continue;

        /* Compute F(N) using hyperbolic method */
        long long U = (long long)sqrt((double)N);
        while ((U + 1) * (U + 1) <= N) U++;
        while (U * U > N) U--;
        /* Now U = floor(sqrt(N)) */

        long long V = N / (U + 1);

        double part1 = 0.0;
        for (long long m = 1; m <= U; m++) {
            part1 += (double)M[N / m] / m;
        }

        double part2 = 0.0;
        for (long long d = 1; d <= V; d++) {
            if (mu[d] != 0) {
                part2 += mu[d] * H[N / d];
            }
        }

        double part3 = (double)M[U] * H[V];

        double F = part1 + part2 - part3;
        double T = F - M[N]; /* = F + 2 */

        count_checked++;
        if (T > max_T) {
            max_T = T;
            worst_N = N;
        }
        if (T >= 0) {
            count_positive++;
            if (count_positive <= 20) {
                printf("POSITIVE: N=%lld, T=%.8f, F=%.8f\n", N, T, F);
            }
        }

        /* Check if N+1 is prime */
        if (N + 1 <= LIMIT && mu[N + 1] != 0 && smallest_prime == NULL) {
            /* Can't easily check primality after free. Skip. */
        }

        if (count_checked % report_interval == 0) {
            fprintf(stderr, "  N=%lld, checked %lld, max_T=%.8f at N=%lld\n",
                    N, count_checked, max_T, worst_N);
        }
    }

    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("\n=== RESULTS ===\n");
    printf("Limit: %lld\n", LIMIT);
    printf("N with M(N)=-2 checked: %lld\n", count_checked);
    printf("Positive T(N) count: %lld\n", count_positive);
    printf("Max T(N): %.10f at N=%lld\n", max_T, worst_N);
    printf("Time: %.2f seconds\n", elapsed);

    if (count_positive == 0 && worst_N >= 42) {
        printf("\nCONFIRMED: T(N) < 0 for all N >= 10 with M(N) = -2, up to N = %lld.\n", LIMIT);
        printf("Worst case: T(%lld) = %.10f\n", worst_N, max_T);
    } else if (count_positive > 0) {
        printf("\nFAILED: Found %lld positive T(N) values.\n", count_positive);
    }

    /* Print worst 10 cases (need to re-scan) */
    printf("\nTop 10 largest T(N) values (N >= 42, M(N)=-2):\n");
    double top_T[10];
    long long top_N[10];
    for (int i = 0; i < 10; i++) { top_T[i] = -1e18; top_N[i] = 0; }

    for (long long N = 42; N <= LIMIT; N++) {
        if (M[N] != -2) continue;

        long long U = (long long)sqrt((double)N);
        while ((U + 1) * (U + 1) <= N) U++;
        while (U * U > N) U--;
        long long V = N / (U + 1);

        double part1 = 0.0;
        for (long long m = 1; m <= U; m++) {
            part1 += (double)M[N / m] / m;
        }
        double part2 = 0.0;
        for (long long d = 1; d <= V; d++) {
            if (mu[d] != 0) part2 += mu[d] * H[N / d];
        }
        double part3 = (double)M[U] * H[V];
        double F = part1 + part2 - part3;
        double T = F + 2;

        /* Insert into top-10 */
        for (int i = 0; i < 10; i++) {
            if (T > top_T[i]) {
                for (int j = 9; j > i; j--) {
                    top_T[j] = top_T[j-1];
                    top_N[j] = top_N[j-1];
                }
                top_T[i] = T;
                top_N[i] = N;
                break;
            }
        }
    }

    for (int i = 0; i < 10; i++) {
        if (top_N[i] > 0) {
            printf("  N=%lld: T(N) = %.10f\n", top_N[i], top_T[i]);
        }
    }

    free(mu);
    free(M);
    free(H);

    return 0;
}
