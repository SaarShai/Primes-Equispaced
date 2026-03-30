/*
 * bprime_243799.c — Compute B'(p) for p = 243799 (N = p-1 = 243798)
 *
 * Uses the EXACT same algorithm as b_verify_100k.c:
 *   D(a/b) = rank - |F_N| * (a/b)     [unnormalized discrepancy]
 *   delta(a/b) = (a - (p*a mod b)) / b  [exact Farey deviation]
 *   B'(p) = 2 * sum_{b>1} D(a/b) * delta(a/b)
 *   C'(p) = sum_{b>1} delta(a/b)^2
 *
 * For N = 243798, |F_N| ~ 1.8*10^10 fractions.
 * At ~10^8 fractions/sec, ~3 minutes.
 *
 * Compile: gcc -O3 -o bprime_243799 bprime_243799.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* Euler phi sieve up to N — needed for |F_N| */
/* N = 243798 — we need phi(k) for k = 1..N */
/* |F_N| = 1 + sum_{k=1}^{N} phi(k) */

#define MAX_N 250000

static int phi_arr[MAX_N + 1];

void compute_phi(int n) {
    for (int i = 0; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i) { /* i is prime */
            for (int j = i; j <= n; j += i) {
                phi_arr[j] -= phi_arr[j] / i;
            }
        }
    }
}

int main(void) {
    long p = 243799;
    long N = p - 1;  /* = 243798 */

    printf("=== B'(p) computation for p = %ld, N = %ld ===\n\n", p, N);
    fflush(stdout);

    time_t t0 = time(NULL);

    /* Compute |F_N| via Euler phi sieve */
    printf("Computing Euler phi sieve up to %ld...\n", N);
    fflush(stdout);
    compute_phi((int)N);

    long long farey_size = 1;  /* counting 0/1 */
    for (long k = 1; k <= N; k++) farey_size += phi_arr[k];

    time_t t1 = time(NULL);
    printf("Sieve done in %ld sec. |F_%ld| = %lld\n", (long)(t1-t0), N, farey_size);
    printf("Expected ~ 3*N^2/pi^2 + 1 = %.0f\n\n", 3.0*(double)N*(double)N/(M_PI*M_PI) + 1.0);
    fflush(stdout);

    double n_dbl = (double)farey_size;

    /* Stream through Farey sequence */
    double B_raw = 0.0;  /* B' = 2*sum(D*delta) */
    double C_raw = 0.0;  /* C' = sum(delta^2) */
    double sum_D2 = 0.0;
    double sum_D = 0.0;
    double sum_delta = 0.0;

    /* Kahan compensation for B and C */
    double kB = 0.0, kC = 0.0;

    long a = 0, b = 1, c = 1, d = N;
    long long rank = 0;
    long long processed = 0;
    long long progress_step = farey_size / 20;
    if (progress_step < 1) progress_step = 1;

    while (!(a == 1 && b == 1)) {
        /* Generate next fraction via mediant */
        long k = (N + b) / d;
        long na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        /* Skip 0/1 and 1/1 (b <= 1) */
        if (b <= 1) continue;

        double f = (double)a / (double)b;
        double D = (double)rank - n_dbl * f;

        /* Exact delta formula: delta(a/b) = (a - (p*a mod b)) / b */
        long long pa_mod_b = ((long long)p * (long long)a) % (long long)b;
        double delta = (double)((long long)a - pa_mod_b) / (double)b;

        /* Kahan sum for B' = 2*sum(D*delta) */
        {
            double y = 2.0 * D * delta - kB;
            double t = B_raw + y;
            kB = (t - B_raw) - y;
            B_raw = t;
        }

        /* Kahan sum for C' = sum(delta^2) */
        {
            double y = delta * delta - kC;
            double t = C_raw + y;
            kC = (t - C_raw) - y;
            C_raw = t;
        }

        sum_D2 += D * D;
        sum_D += D;
        sum_delta += delta;

        processed++;
        if (processed % progress_step == 0) {
            time_t tnow = time(NULL);
            double pct = 100.0 * rank / farey_size;
            printf("  %5.1f%% (%lld / %lld) — %ld sec — B'=%.6e C'=%.6e\n",
                   pct, rank, farey_size, (long)(tnow-t0), B_raw, C_raw);
            fflush(stdout);
        }
    }

    time_t t2 = time(NULL);

    printf("\nComputation done in %ld sec (total %ld sec)\n\n",
           (long)(t2-t1), (long)(t2-t0));

    /* Results */
    double correction_over_C = (C_raw > 0) ? (C_raw - B_raw) / (2.0 * C_raw) : 0.0;
    double B_over_C = (C_raw > 0) ? B_raw / C_raw : 0.0;

    printf("=== RESULTS for p = %ld ===\n", p);
    printf("  |F_N|               = %lld\n", farey_size);
    printf("  Fractions processed = %lld (excl. 0/1 and 1/1)\n", processed);
    printf("\n");
    printf("  B' = 2*sum(D*delta) = %.15e\n", B_raw);
    printf("  C' = sum(delta^2)   = %.15e\n", C_raw);
    printf("  B'/C'               = %.15f\n", B_over_C);
    printf("  correction/C'       = %.15f   (= (C'-B')/(2C'))\n", correction_over_C);
    printf("\n");
    printf("  sum(D^2)            = %.15e\n", sum_D2);
    printf("  sum(D)              = %.15e\n", sum_D);
    printf("  sum(delta)          = %.15e\n", sum_delta);
    printf("\n");

    /* Derived */
    printf("=== DERIVED ===\n");
    printf("  mean(D)             = %.15e\n", sum_D / processed);
    printf("  margin = B'/C'      = %.6f\n", B_over_C);
    printf("\n");

    /* Verdict */
    printf("=== VERDICT ===\n");
    if (B_raw > 0) {
        printf("  B'(%ld) = %.6e > 0  --> POSITIVE\n", p, B_raw);
        printf("  NOT a counterexample. B' > 0 holds at this M(p)=-3 prime.\n");
    } else if (B_raw == 0.0) {
        printf("  B'(%ld) = 0 --> ZERO\n", p);
    } else {
        printf("  B'(%ld) = %.6e < 0  --> NEGATIVE\n", p, B_raw);
        printf("  *** COUNTEREXAMPLE to B' > 0 for M(p) = -3 primes! ***\n");
    }

    printf("\n=== CONTEXT ===\n");
    printf("  This prime has M(p) = -3 and T(N) = +0.165 (alpha ~ 0.835 < 1)\n");
    printf("  The correction negativity proof claimed Term2 < 0 for all p >= 43 with M=-3\n");
    printf("  T(N) > 0 disproves that, but B' > 0 may still hold if rho compensates\n");
    printf("  B'/C' = alpha + rho, and we need this > 0\n");
    printf("  alpha ~ 0.835, so rho must be > -0.835 for B' > 0\n");

    return 0;
}
