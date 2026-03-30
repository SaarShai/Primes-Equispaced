/*
 * density_patterns.c
 *
 * Compute T(N) for ALL M(p)=-3 primes up to 10^7.
 * Output: CSV with p, T(N), M(N/2), M(N/3), M(N/5), M(N/6), gap_from_prev
 *
 * Uses hyperbolic method for T(N) computation.
 *
 * Compile: gcc -O3 -o density_patterns density_patterns.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define LIMIT 10000000

int main() {
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
            is_prime[i] = 1;
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

    fprintf(stderr, "Computing T(N) for all M(p)=-3 primes...\n");

    /* Header */
    printf("p,N,T_N,M_half,M_third,M_fifth,M_sixth,M_seventh,p_mod6,p_mod12,p_mod30,p_mod24\n");

    long long prev_p = 0;
    long long count = 0;

    for (long long N = 10; N <= LIMIT; N++) {
        if (M[N] != -2) continue;
        long long p = N + 1;
        if (p > LIMIT + 1) break;
        if (!is_prime[p]) continue;
        if (M[p] != -3) continue;

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
        double T = F + 2; /* T(N) = F(N) - M(N) = F(N) + 2 since M(N) = -2 */

        /* Gather M values at key fractions */
        int m_half = M[N / 2];
        int m_third = M[N / 3];
        int m_fifth = (N / 5 >= 1) ? M[N / 5] : 0;
        int m_sixth = (N / 6 >= 1) ? M[N / 6] : 0;
        int m_seventh = (N / 7 >= 1) ? M[N / 7] : 0;

        printf("%lld,%lld,%.10f,%d,%d,%d,%d,%d,%lld,%lld,%lld,%lld\n",
               p, N, T, m_half, m_third, m_fifth, m_sixth, m_seventh,
               p % 6, p % 12, p % 30, p % 24);

        count++;
        prev_p = p;

        if (count % 100 == 0) {
            fprintf(stderr, "  %lld primes processed (p=%lld)\n", count, p);
        }
    }

    fprintf(stderr, "Done. Total M(p)=-3 primes: %lld\n", count);

    free(mu);
    free(M);
    free(H);
    free(is_prime);
    return 0;
}
