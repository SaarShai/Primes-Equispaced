/*
 * b_plus_c_large.c
 *
 * Compute EXACT B'/C' for specific large primes where T(N) > 0.
 * Uses sieve-based phi computation and streaming Farey generation.
 *
 * For p = 243799: N = 243798, |F_N| ~ 1.8*10^10, expect ~50-100 sec.
 *
 * Also computes T(N) via hyperbola method for comparison.
 *
 * Usage: ./b_plus_c_large <prime1> [prime2] ...
 *
 * Compile: cc -O3 -o b_plus_c_large b_plus_c_large.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

static signed char *mu_arr = NULL;
static int *M_vals = NULL;
static int *phi_arr = NULL;
static int sieve_limit = 0;

void sieve(int n) {
    if (n <= sieve_limit) return;

    free(mu_arr); free(M_vals); free(phi_arr);

    int *primes = malloc((n / 2 + 10) * sizeof(int));
    char *is_composite = calloc(n + 1, 1);
    int num_primes = 0;

    mu_arr = calloc(n + 1, sizeof(signed char));
    M_vals = calloc(n + 1, sizeof(int));
    phi_arr = calloc(n + 1, sizeof(int));

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
    sieve_limit = n;
}

double compute_T(int N) {
    double T = 0.0;
    int sq = (int)sqrt((double)N);

    for (int m = 2; m <= sq; m++) {
        T += (double)M_vals[N / m] / m;
    }

    for (int q = 1; q <= sq; q++) {
        int m_lo = N / (q + 1) + 1;
        int m_hi = N / q;
        if (m_lo <= sq) m_lo = sq + 1;
        if (m_hi < m_lo) continue;

        double harmonic_sum = 0.0;
        for (int m = m_lo; m <= m_hi; m++) {
            harmonic_sum += 1.0 / m;
        }
        T += (double)M_vals[q] * harmonic_sum;
    }

    return T;
}

void compute_for_prime(long long p) {
    int N = (int)(p - 1);

    fprintf(stderr, "\n=== p = %lld ===\n", p);
    clock_t t0 = clock();

    /* Sieve up to N */
    fprintf(stderr, "Sieving to %d...\n", N);
    sieve(N);
    clock_t t1 = clock();
    fprintf(stderr, "Sieve: %.1f sec\n", (double)(t1 - t0) / CLOCKS_PER_SEC);

    /* Check M(p) */
    int Mertens_p = M_vals[N] + mu_arr[N + 1]; /* M(p) = M(N) + mu(p) -- but we need mu(p) */
    /* For prime p, mu(p) = -1. M(p) = M(p-1) + mu(p) = M(N) + (-1) */
    /* But p may be > sieve_limit. In that case we can't directly get mu(p). */
    /* Since we sieved to N = p-1, and p is prime, mu(p) = -1. */
    fprintf(stderr, "M(%d) = %d, M(%lld) = %d\n", N, M_vals[N], p, M_vals[N] - 1);

    /* Compute T(N) */
    double T = compute_T(N);
    double alpha_approx = 1.0 - T;  /* for M(N) = -2 */
    fprintf(stderr, "T(%d) = %.6f, alpha ~ %.6f\n", N, T, alpha_approx);

    /* Compute Farey size */
    long long n_frac = 1;
    for (int k = 1; k <= N; k++) n_frac += phi_arr[k];
    clock_t t2 = clock();
    fprintf(stderr, "|F_%d| = %lld (%.1f sec)\n", N, n_frac, (double)(t2 - t1) / CLOCKS_PER_SEC);

    /* Stream through Farey sequence */
    fprintf(stderr, "Streaming Farey sequence (~%lld fractions)...\n", n_frac);

    double B_raw = 0.0;
    double C_raw = 0.0;
    double sum_f_delta = 0.0;
    double sum_delta = 0.0;
    long long count = 0;

    int a = 0, b = 1, c = 1, d = N;
    long long rank = 0;

    clock_t t3 = clock();

    while (!(a == 1 && b == 1)) {
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        if (b <= 1) continue;

        double f = (double)a / b;
        double D = (double)rank - (double)n_frac * f;

        long long pa_mod_b = ((long long)p * a) % b;
        double delta = (double)((long long)a - pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;
        sum_f_delta += f * delta;
        sum_delta += delta;
        count++;

        if (count % 2000000000LL == 0) {
            clock_t tc = clock();
            double elapsed = (double)(tc - t3) / CLOCKS_PER_SEC;
            fprintf(stderr, "  %lld fractions (%.0f sec, %.1fM/s), B'=%.3e, C'=%.3e\n",
                    count, elapsed, count / elapsed / 1e6, B_raw, C_raw);
        }
    }

    clock_t t4 = clock();
    double stream_time = (double)(t4 - t3) / CLOCKS_PER_SEC;

    double ratio = (C_raw > 0) ? (B_raw / C_raw) : 0.0;
    double BpC = B_raw + C_raw;
    double BpC_norm = (C_raw > 0) ? (1.0 + ratio) : 0.0;
    double rho_computed = ratio - alpha_approx;

    fprintf(stderr, "Done: %lld interior fractions in %.1f sec (%.1fM/s)\n",
            count, stream_time, count / stream_time / 1e6);

    /* Verification: sum_f_delta should be C'/2, sum_delta should be ~0 */
    fprintf(stderr, "CHECK: sum(delta) = %.6e (should be ~0)\n", sum_delta);
    fprintf(stderr, "CHECK: sum(f*delta) = %.6e, C'/2 = %.6e, ratio = %.6f\n",
            sum_f_delta, C_raw / 2.0,
            (C_raw > 0) ? (2.0 * sum_f_delta / C_raw) : 0.0);

    printf("p=%lld  T=%.4f  alpha~%.4f  B'/C'=%.6f  rho~%.4f  (1+B'/C')=%.6f  B+C>0: %s\n",
           p, T, alpha_approx, ratio, rho_computed, BpC_norm,
           (BpC_norm > 0) ? "YES" : "**NO**");
    fflush(stdout);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <prime1> [prime2] ...\n", argv[0]);
        return 1;
    }

    for (int i = 1; i < argc; i++) {
        long long p = atoll(argv[i]);
        if (p >= 5) compute_for_prime(p);
    }

    return 0;
}
