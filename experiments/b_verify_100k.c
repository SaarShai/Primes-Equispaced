/*
 * b_verify_100k.c
 * Verify B' > 0 for ALL primes p with M(p) = -3 up to p = 100,000.
 *
 * For each such prime:
 *   - Generate Farey sequence F_{p-1} via mediant algorithm (streaming, O(1) space)
 *   - Compute B' = 2 * sum_{b>1} D(a/b) * delta(a/b)
 *   - Compute C' = sum_{b>1} delta(a/b)^2
 *   - Compute five-block sum S_5(p)
 *   - Check B' > 0
 *
 * Uses double-precision floats (sufficient since B'/C' >= 0.12).
 *
 * Compile: cc -O3 -o b_verify_100k b_verify_100k.c -lm -lpthread
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX_N 100001

static int mu_arr[MAX_N];
static int M_vals[MAX_N];
static int phi_arr[MAX_N];
static char is_prime_arr[MAX_N];

void sieve(int n) {
    int *primes = malloc(n * sizeof(int));
    int num_primes = 0;

    memset(is_prime_arr, 1, n + 1);
    is_prime_arr[0] = is_prime_arr[1] = 0;

    mu_arr[1] = 1; phi_arr[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (is_prime_arr[i]) {
            primes[num_primes++] = i;
            mu_arr[i] = -1;
            phi_arr[i] = i - 1;
        }
        for (int j = 0; j < num_primes && (long long)i * primes[j] <= n; j++) {
            int ip = i * primes[j];
            is_prime_arr[ip] = 0;
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

    free(primes);
}

/*
 * Compute B' and C' for prime p using streaming Farey generation.
 * Also computes the five-block sum S_5.
 *
 * Five-block partition of [0,1]: [0,1/5), [1/5,2/5), [2/5,3/5), [3/5,4/5), [4/5,1].
 * S_5 = sum over blocks of |sum of delta in block|.
 */
void compute_bc(int p, double *B_out, double *C_out, double *ratio_out,
                long *n_out, double *S5_out, double *min_Bprime_running) {
    int N = p - 1;

    /* Compute Farey size */
    long n = 1; /* for 0/1 */
    for (int k = 1; k <= N; k++) n += phi_arr[k];

    /* Stream through Farey sequence using mediant algorithm */
    double B_raw = 0.0;
    double C_raw = 0.0;

    /* Five-block sums of delta */
    double block_delta[5] = {0, 0, 0, 0, 0};

    int a = 0, b = 1, c = 1, d = N;
    long rank = 0;

    while (!(a == 1 && b == 1)) {
        /* Generate next fraction */
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        /* Now process a/b at position rank */
        if (b <= 1) continue; /* skip 0/1 and 1/1 (delta=0 at boundaries) */

        double f = (double)a / b;
        double D = (double)rank - (double)n * f;

        /* delta = (a - (p*a mod b)) / b */
        long long pa_mod_b = ((long long)p * a) % b;
        double delta = (double)(a - (int)pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;

        /* Five-block classification */
        int block;
        if (5 * a < b) block = 0;
        else if (5 * a < 2 * b) block = 1;
        else if (5 * a < 3 * b) block = 2;
        else if (5 * a < 4 * b) block = 3;
        else block = 4;
        block_delta[block] += delta;
    }

    *B_out = B_raw;
    *C_out = C_raw;
    *n_out = n;

    if (C_raw > 0) {
        *ratio_out = (C_raw - B_raw) / (2.0 * C_raw);
    } else {
        *ratio_out = 0.0;
    }

    /* S_5 = sum of |block sums| */
    double s5 = 0;
    for (int i = 0; i < 5; i++) s5 += fabs(block_delta[i]);
    *S5_out = s5;

    *min_Bprime_running = B_raw;
}

int main(int argc, char *argv[]) {
    int MAX_P = 100000;
    if (argc > 1) MAX_P = atoi(argv[1]);

    time_t start = time(NULL);
    fprintf(stderr, "B' verification for M(p)=-3 primes up to %d\n", MAX_P);
    fprintf(stderr, "Sieving to %d...\n", MAX_P);
    sieve(MAX_P);
    fprintf(stderr, "Sieve done.\n");

    /* Count M(p)=-3 primes */
    int total_m3 = 0;
    for (int p = 2; p <= MAX_P; p++) {
        if (is_prime_arr[p] && M_vals[p] == -3) total_m3++;
    }
    fprintf(stderr, "Found %d primes with M(p) = -3 up to %d\n", total_m3, MAX_P);

    printf("p,n,M_p,B_prime,C_prime,correction_over_C,margin,S5,B_positive\n");
    fflush(stdout);

    int count = 0;
    int violations = 0;
    double worst_ratio = -1e30;
    int worst_p = 0;
    double min_B = 1e30;
    int min_B_p = 0;
    double min_margin = 1e30;

    for (int p = 2; p <= MAX_P; p++) {
        if (!is_prime_arr[p]) continue;
        if (M_vals[p] != -3) continue;
        count++;

        double B, C, ratio, S5, min_Br;
        long n;
        compute_bc(p, &B, &C, &ratio, &n, &S5, &min_Br);

        double margin = 0.5 - ratio;
        int B_pos = (B > 0) ? 1 : 0;

        printf("%d,%ld,-3,%.10f,%.10f,%.6f,%.6f,%.10f,%d\n",
               p, n, B, C, ratio, margin, S5, B_pos);

        if (count % 100 == 0) {
            fflush(stdout);
            time_t now = time(NULL);
            fprintf(stderr, "  [%lds] Processed %d/%d primes (p=%d)\n",
                    (long)(now - start), count, total_m3, p);
        }

        if (!B_pos) {
            violations++;
            fprintf(stderr, "  *** VIOLATION: B' <= 0 at p=%d, B'=%.10f ***\n", p, B);
        }

        if (ratio > worst_ratio) { worst_ratio = ratio; worst_p = p; }
        if (B < min_B) { min_B = B; min_B_p = p; }
        if (margin < min_margin) min_margin = margin;
    }

    fflush(stdout);
    time_t end = time(NULL);

    fprintf(stderr, "\n=== SUMMARY ===\n");
    fprintf(stderr, "Total M(p)=-3 primes checked: %d\n", count);
    fprintf(stderr, "Violations (B' <= 0): %d\n", violations);
    fprintf(stderr, "Worst correction/C ratio: %.6f at p=%d\n", worst_ratio, worst_p);
    fprintf(stderr, "Minimum B': %.10f at p=%d\n", min_B, min_B_p);
    fprintf(stderr, "Minimum margin (0.5 - ratio): %.6f\n", min_margin);
    fprintf(stderr, "Total time: %ld seconds\n", (long)(end - start));

    if (violations == 0) {
        fprintf(stderr, "\n*** ALL %d PRIMES VERIFIED: B' > 0 ***\n", count);
    } else {
        fprintf(stderr, "\n*** FAILED: %d VIOLATIONS FOUND ***\n", violations);
    }

    return violations;
}
