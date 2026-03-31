/*
 * multiscale_decomp.c - Decompose T(N) into scale bands for M(p)=-3 primes
 *
 * For each M(p)=-3 prime p <= 10^7 with N=p-1:
 *   T_low(N)  = sum_{m=2}^{10} M(floor(N/m))/m    (large scales: N/2 to N/10)
 *   T_mid(N)  = sum_{m=11}^{sqrt(N)} M(floor(N/m))/m (medium scales)
 *   T_high(N) = sum_{m>sqrt(N)}^{N} M(floor(N/m))/m   (small scales)
 *   T(N)      = T_low + T_mid + T_high
 *
 * Also outputs M(N/k) for k=2..20 for marginal contribution analysis.
 *
 * Compile: gcc -O3 -o multiscale_decomp multiscale_decomp.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define LIMIT 10000001
#define SQRT_LIMIT 3163  /* floor(sqrt(10^7)) */

static signed char mu[LIMIT];       /* Mobius function */
static int M[LIMIT];                /* Mertens function M(n) = sum_{k=1}^n mu(k) */
static char sieve[LIMIT];           /* 0 = prime */

void compute_mobius_and_mertens(void) {
    /* Sieve of Eratosthenes + Mobius function */
    memset(sieve, 0, sizeof(sieve));
    sieve[0] = sieve[1] = 1;

    for (int i = 1; i < LIMIT; i++) mu[i] = 1;

    for (long long p = 2; p < LIMIT; p++) {
        if (sieve[p]) continue;
        /* p is prime */
        for (long long j = p; j < LIMIT; j += p) {
            if (j > p) sieve[j] = 1;
            mu[j] *= -1;
        }
        /* p^2 divides j => mu(j) = 0 */
        long long p2 = p * p;
        for (long long j = p2; j < LIMIT; j += p2) {
            mu[j] = 0;
        }
    }

    /* Mertens function */
    M[0] = 0;
    for (int i = 1; i < LIMIT; i++) {
        M[i] = M[i - 1] + mu[i];
    }
}

int main(void) {
    fprintf(stderr, "Computing Mobius and Mertens functions up to %d...\n", LIMIT - 1);
    compute_mobius_and_mertens();
    fprintf(stderr, "Done. Scanning for M(p)=-3 primes...\n");

    /* Header */
    printf("p,N,T_total,T_low,T_mid,T_high");
    for (int k = 2; k <= 20; k++) {
        printf(",M_N_%d", k);
    }
    printf(",sqrtN\n");

    int count = 0;
    for (int p = 2; p < LIMIT; p++) {
        if (sieve[p]) continue;  /* not prime */
        if (M[p] != -3) continue;

        int N = p - 1;
        int sqrtN = (int)sqrt((double)N);

        /* Compute T_low: m=2..10 */
        double T_low = 0.0;
        int m_low_end = (10 < N) ? 10 : N;
        for (int m = 2; m <= m_low_end; m++) {
            int idx = N / m;
            if (idx >= 0 && idx < LIMIT) {
                T_low += (double)M[idx] / m;
            }
        }

        /* Compute T_mid: m=11..sqrtN */
        double T_mid = 0.0;
        if (sqrtN >= 11) {
            for (int m = 11; m <= sqrtN; m++) {
                int idx = N / m;
                if (idx >= 0 && idx < LIMIT) {
                    T_mid += (double)M[idx] / m;
                }
            }
        }

        /* Compute T_high: m=sqrtN+1..N */
        double T_high = 0.0;
        int m_high_start = sqrtN + 1;
        if (m_high_start <= 10) m_high_start = 11; /* avoid double counting if sqrtN < 10 */
        if (m_high_start <= N) {
            /* Use hyperbolic trick: for m > sqrtN, floor(N/m) takes at most sqrtN distinct values */
            /* Group by value v = floor(N/m). For each v, find range of m. */
            int m = m_high_start;
            while (m <= N) {
                int v = N / m;
                if (v == 0) break;
                /* All m' with floor(N/m') = v: m' in [N/(v+1)+1, N/v] */
                int m_end = N / v;
                if (m_end > N) m_end = N;
                /* Sum 1/m' for m' in [m, m_end] */
                /* H(m_end) - H(m-1) where H is harmonic number */
                double harm_sum = 0.0;
                for (int mm = m; mm <= m_end; mm++) {
                    harm_sum += 1.0 / mm;
                }
                T_high += (double)M[v] * harm_sum;
                m = m_end + 1;
            }
        }

        double T_total = T_low + T_mid + T_high;

        /* M(N/k) for k=2..20 */
        printf("%d,%d,%.10f,%.10f,%.10f,%.10f", p, N, T_total, T_low, T_mid, T_high);
        for (int k = 2; k <= 20; k++) {
            int idx = N / k;
            if (idx >= 0 && idx < LIMIT) {
                printf(",%d", M[idx]);
            } else {
                printf(",0");
            }
        }
        printf(",%d\n", sqrtN);

        count++;
    }

    fprintf(stderr, "Found %d primes with M(p) = -3.\n", count);
    return 0;
}
