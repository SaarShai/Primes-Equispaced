/*
 * bprime_243799_long.c — Same computation but with long double for higher precision.
 * Also uses COMPENSATED summation (Kahan) more aggressively.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define MAX_N 250000
static int phi_arr[MAX_N + 1];

void compute_phi(int n) {
    for (int i = 0; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i)
            for (int j = i; j <= n; j += i) phi_arr[j] -= phi_arr[j] / i;
    }
}

int main(void) {
    long p = 243799;
    long N = p - 1;
    printf("=== B'(%ld) with long double + Kahan ===\n\n", p);
    fflush(stdout);

    time_t t0 = time(NULL);
    compute_phi((int)N);

    long long farey_size = 1;
    for (long k = 1; k <= N; k++) farey_size += phi_arr[k];
    long double n_dbl = (long double)farey_size;
    printf("|F_%ld| = %lld\n\n", N, farey_size);
    fflush(stdout);

    long double B_raw = 0.0L, kB = 0.0L;
    long double C_raw = 0.0L, kC = 0.0L;

    long a = 0, b = 1, c = 1, d = N;
    long long rank = 0;
    long long processed = 0;
    long long progress_step = farey_size / 20;

    while (!(a == 1 && b == 1)) {
        long k = (N + b) / d;
        long na = k*c - a, nb = k*d - b;
        a = c; b = d; c = na; d = nb;
        rank++;
        if (b <= 1) continue;

        long double f = (long double)a / (long double)b;
        long double D = (long double)rank - n_dbl * f;
        long long pa_mod_b = ((long long)p * (long long)a) % (long long)b;
        long double delta = (long double)((long long)a - pa_mod_b) / (long double)b;

        /* Kahan for B' */
        {
            long double y = 2.0L * D * delta - kB;
            long double t = B_raw + y;
            kB = (t - B_raw) - y;
            B_raw = t;
        }
        /* Kahan for C' */
        {
            long double y = delta * delta - kC;
            long double t = C_raw + y;
            kC = (t - C_raw) - y;
            C_raw = t;
        }

        processed++;
        if (processed % progress_step == 0) {
            time_t tnow = time(NULL);
            printf("  %5.1Lf%% — %ld sec — B'=%.6Le C'=%.6Le\n",
                   100.0L*(long double)rank/(long double)farey_size,
                   (long)(tnow-t0), B_raw, C_raw);
            fflush(stdout);
        }
    }

    time_t t2 = time(NULL);
    printf("\nDone in %ld sec\n\n", (long)(t2-t0));

    printf("=== RESULTS (long double) ===\n");
    printf("  B' = %.20Le\n", B_raw);
    printf("  C' = %.20Le\n", C_raw);
    printf("  B'/C' = %.15Lf\n", B_raw / C_raw);
    printf("\n");

    if (B_raw > 0.0L) printf("VERDICT: B' > 0 (POSITIVE)\n");
    else if (B_raw < 0.0L) printf("VERDICT: B' < 0 (NEGATIVE — COUNTEREXAMPLE)\n");
    else printf("VERDICT: B' = 0\n");

    return 0;
}
