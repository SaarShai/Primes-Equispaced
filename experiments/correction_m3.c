/*
 * correction_m3.c
 * Compute correction/C ratio for ALL primes with M(p) = -3 up to a given limit.
 *
 * For M(p) = -3, we have B = C - 2*Term2 where Term2 is the Abel correction.
 * The bound correction/C < 0.5 is equivalent to B > 0.
 *
 * We compute B and C by iterating over all Farey fractions a/b with b <= p-1.
 * This avoids generating the full Farey sequence in order.
 *
 * For each denominator b (1 <= b <= N = p-1), for each a coprime to b (1 <= a < b):
 *   rank(a/b) is needed for D(a/b) = rank - n*(a/b)
 *   delta(a/b) = (a - (p*a mod b)) / b
 *
 * Computing rank(a/b) requires knowing how many Farey fractions <= a/b,
 * which is expensive. Instead, we generate the Farey sequence in order
 * using the mediant algorithm (O(n) time, O(1) space).
 *
 * For p up to ~5000, the Farey sequence has ~7.5M elements -- feasible.
 * For larger p, we need a smarter approach.
 *
 * APPROACH: For p <= 5000, use direct Farey generation.
 * For p > 5000, use the per-denominator sum approach with rank computation.
 *
 * Actually, for this problem we can use a streaming Farey approach:
 * generate F_N in order, compute rank as we go, compute delta for each fraction.
 *
 * Compile: cc -O3 -o correction_m3 correction_m3.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_N 100001

static int mu_arr[MAX_N];
static int M_vals[MAX_N];
static int phi_arr[MAX_N];

void sieve(int n) {
    int *primes = malloc(n * sizeof(int));
    int *is_composite = calloc(n + 1, sizeof(int));
    int num_primes = 0;

    mu_arr[1] = 1; phi_arr[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) {
            primes[num_primes++] = i;
            mu_arr[i] = -1;
            phi_arr[i] = i - 1;
        }
        for (int j = 0; j < num_primes && (long long)i * primes[j] <= n; j++) {
            int ip = i * primes[j];
            is_composite[ip] = 1;
            if (i % primes[j] == 0) {
                mu_arr[ip] = 0;
                phi_arr[ip] = phi_arr[i] * primes[j];
                break;
            } else {
                mu_arr[ip] = -mu_arr[i];
                phi_arr[ip] = phi_arr[i] * (primes[j] - 1);
            }
        }
    }

    M_vals[0] = 0;
    for (int i = 1; i <= n; i++) M_vals[i] = M_vals[i - 1] + mu_arr[i];

    free(primes); free(is_composite);
}

/*
 * Compute B and C for prime p using streaming Farey generation.
 * Returns B, C, and the correction ratio = Term2/C = (C - B) / (2*C).
 */
void compute_correction(int p, double *B_out, double *C_out, double *ratio_out, long *n_out) {
    int N = p - 1;

    /* Compute Farey size */
    long n = 1; /* for 0/1 */
    for (int k = 1; k <= N; k++) n += phi_arr[k];

    /* Stream through Farey sequence using mediant algorithm */
    double B_raw = 0.0;
    double C_raw = 0.0;
    double sum_x_delta = 0.0;

    /* Start: 0/1 -> skip (D=0, delta=0 for boundary) */
    int a = 0, b = 1, c = 1, d = N;
    long rank = 0; /* rank of 0/1 is 0 */

    /* Process 0/1: D(0/1) = 0 - n*0 = 0, delta(0/1) = (0 - 0)/1 = 0 */
    /* Skip -- contributes nothing */

    while (!(a == 1 && b == 1)) {
        /* Generate next fraction */
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        /* Now process a/b at position rank */
        if (a == 0 || (a == 1 && b == 1)) continue; /* skip boundaries */

        double f = (double)a / b;
        double D = (double)rank - (double)n * f;

        /* delta = (a - (p*a mod b)) / b */
        int pa_mod_b = (int)(((long long)p * a) % b);
        double delta = (double)(a - pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;
        sum_x_delta += f * delta;
    }

    /* Process 1/1: D(1/1) = (n-1) - n = -1, delta(1/1) = (1 - p%1)/1 = 0 */
    /* Skip -- delta = 0 at boundary */

    *B_out = B_raw;
    *C_out = C_raw;
    *n_out = n;

    /* Term2 = (C - B) / 2 (for M(p) = -3 specifically) */
    /* correction/C = Term2/C = (C - B) / (2*C) */
    if (C_raw > 0) {
        *ratio_out = (C_raw - B_raw) / (2.0 * C_raw);
    } else {
        *ratio_out = 0.0;
    }
}

int main(int argc, char *argv[]) {
    int MAX_P = 5000;
    if (argc > 1) MAX_P = atoi(argv[1]);

    fprintf(stderr, "Sieving to %d...\n", MAX_P);
    sieve(MAX_P);
    fprintf(stderr, "Finding M(p) = -3 primes and computing correction...\n");

    printf("p,n,M_p,B,C,Term2,correction_over_C,margin\n");

    int count = 0;
    int count_m3 = 0;
    double worst_ratio = -1e30;
    int worst_p = 0;

    for (int p = 2; p <= MAX_P; p++) {
        /* Check primality */
        if (p > 2 && p % 2 == 0) continue;
        int is_prime = 1;
        if (p > 2) {
            for (int q = 3; (long long)q * q <= p; q += 2) {
                if (p % q == 0) { is_prime = 0; break; }
            }
        }
        if (!is_prime) continue;

        if (M_vals[p] != -3) continue;
        count_m3++;

        double B, C, ratio;
        long n;
        compute_correction(p, &B, &C, &ratio, &n);

        double Term2 = (C - B) / 2.0;
        double margin = 0.5 - ratio;  /* margin from the 0.5 threshold */

        printf("%d,%ld,-3,%.10f,%.10f,%.10f,%.6f,%.6f\n",
               p, n, B, C, Term2, ratio, margin);
        fflush(stdout);

        if (ratio > worst_ratio) {
            worst_ratio = ratio;
            worst_p = p;
        }

        count++;
        if (count % 50 == 0) {
            fprintf(stderr, "Done %d M(p)=-3 primes, last p=%d, worst ratio=%.6f at p=%d\n",
                    count, p, worst_ratio, worst_p);
        }
    }

    fprintf(stderr, "\nTotal M(p)=-3 primes found: %d\n", count);
    fprintf(stderr, "Worst correction/C ratio: %.6f at p=%d\n", worst_ratio, worst_p);
    fprintf(stderr, "Margin from 0.5: %.6f\n", 0.5 - worst_ratio);

    return 0;
}
