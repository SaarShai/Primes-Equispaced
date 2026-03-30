/*
 * t_negativity_verify2.c
 *
 * Verify T(N) < 0 for N = p-1 where p is prime with M(p) = -3
 * (equivalently M(N) = -2 and M(N+1) = -3, i.e., N+1 prime and mu(N+1) = -1).
 *
 * Also check: T(N) for ALL N with M(N) = -2 (to find positive cases).
 *
 * Uses hyperbolic method for O(sqrt(N)) evaluation.
 *
 * Compile: gcc -O3 -o t_negativity_verify2 t_negativity_verify2.c -lm
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

    fprintf(stderr, "T(N) verification up to N = %lld\n", LIMIT);

    signed char *mu = calloc(LIMIT + 2, sizeof(signed char));
    int *M = calloc(LIMIT + 2, sizeof(int));
    double *H = calloc(LIMIT + 2, sizeof(double));
    char *is_prime = calloc(LIMIT + 2, sizeof(char));

    if (!mu || !M || !H || !is_prime) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    /* Linear sieve for mu and is_prime */
    fprintf(stderr, "Sieving...\n");
    mu[1] = 1;
    int *prime_list = calloc(LIMIT / 2 + 100, sizeof(int));
    int *sp = calloc(LIMIT + 2, sizeof(int));
    int num_primes = 0;

    for (long long i = 2; i <= LIMIT + 1; i++) {
        if (sp[i] == 0) {
            sp[i] = i;
            if (i <= LIMIT + 1) is_prime[i] = 1;
            prime_list[num_primes++] = i;
            mu[i] = -1;
        }
        for (int j = 0; j < num_primes; j++) {
            long long p = prime_list[j];
            if (p > sp[i] || i * p > LIMIT + 1) break;
            sp[i * p] = p;
            if (i % p == 0) {
                mu[i * p] = 0;
            } else {
                mu[i * p] = -mu[i];
            }
        }
    }
    free(sp);
    free(prime_list);

    fprintf(stderr, "Computing M and H...\n");
    M[0] = 0;
    for (long long n = 1; n <= LIMIT + 1; n++) {
        M[n] = M[n - 1] + mu[n];
    }
    H[0] = 0.0;
    for (long long n = 1; n <= LIMIT; n++) {
        H[n] = H[n - 1] + 1.0 / n;
    }

    /* Compute T(N) using hyperbolic method */
    fprintf(stderr, "Checking...\n");

    /* Case 1: N with M(N) = -2 AND N+1 is prime with M(N+1) = -3 */
    long long count_prime = 0;
    long long count_prime_positive = 0;
    double max_T_prime = -1e18;
    long long worst_N_prime = 0;

    /* Case 2: ALL N >= 42 with M(N) = -2 */
    long long count_all = 0;
    long long count_all_positive = 0;
    double max_T_all = -1e18;
    long long worst_N_all = 0;

    /* Case 3: N >= 42 with M(N) = -2, first positive occurrence */
    long long first_positive_N = 0;

    clock_t start = clock();

    for (long long N = 10; N <= LIMIT; N++) {
        if (M[N] != -2) continue;

        /* Compute T(N) via hyperbolic method */
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
        double T = F + 2; /* T(N) = F(N) - M(N) = F(N) + 2 */

        /* Case 2: ALL */
        if (N >= 42) {
            count_all++;
            if (T > max_T_all) {
                max_T_all = T;
                worst_N_all = N;
            }
            if (T >= 0) {
                count_all_positive++;
                if (first_positive_N == 0) first_positive_N = N;
            }
        }

        /* Case 1: N+1 prime with M(N+1) = -3 */
        if (N + 1 <= LIMIT + 1 && is_prime[N + 1] && M[N + 1] == -3) {
            count_prime++;
            if (T > max_T_prime) {
                max_T_prime = T;
                worst_N_prime = N;
            }
            if (T >= 0) {
                count_prime_positive++;
                printf("PRIME POSITIVE: p=%lld (N=%lld), T=%.10f\n", N + 1, N, T);
            }
            if (count_prime <= 30 || count_prime % 100 == 0) {
                fprintf(stderr, "  p=%lld: T=%+.6f (max=%+.6f at N=%lld)\n",
                        N + 1, T, max_T_prime, worst_N_prime);
            }
        }
    }

    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("\n=== CASE 1: N = p-1, M(p) = -3 primes ===\n");
    printf("Primes checked: %lld\n", count_prime);
    printf("Positive T(N) count: %lld\n", count_prime_positive);
    printf("Max T(N): %.10f at N=%lld (p=%lld)\n", max_T_prime, worst_N_prime, worst_N_prime + 1);
    if (count_prime_positive == 0) {
        printf("CONFIRMED: T(N) < 0 for all primes p with M(p)=-3, p <= %lld.\n", LIMIT + 1);
    }

    printf("\n=== CASE 2: ALL N >= 42 with M(N) = -2 ===\n");
    printf("Total checked: %lld\n", count_all);
    printf("Positive T(N) count: %lld (%.2f%%)\n", count_all_positive,
           100.0 * count_all_positive / (count_all > 0 ? count_all : 1));
    printf("Max T(N): %.10f at N=%lld\n", max_T_all, worst_N_all);
    printf("First positive N >= 42: %lld\n", first_positive_N);

    printf("\nTime: %.2f seconds\n", elapsed);

    free(mu);
    free(M);
    free(H);
    free(is_prime);

    return 0;
}
