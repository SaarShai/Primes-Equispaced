/*
 * FAST B+C VERIFICATION v2 - with resume support and fflush
 * Extends verification to p <= 50000 for primes with M(p) <= -3
 *
 * Usage: ./bc_extend_fast2 [LIMIT] [START_FROM]
 *   LIMIT: max prime to check (default 50000)
 *   START_FROM: skip primes <= this value (for resuming)
 *
 * Output: CSV to stdout, progress to stderr
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* Sieve of Eratosthenes */
static char *sieve_primes(int limit) {
    char *is_prime = calloc(limit + 1, 1);
    if (!is_prime) { fprintf(stderr, "OOM\n"); exit(1); }
    for (int i = 2; i <= limit; i++) is_prime[i] = 1;
    for (int i = 2; (long long)i * i <= limit; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i)
                is_prime[j] = 0;
        }
    }
    return is_prime;
}

/* Compute Mobius function via smallest prime factor sieve */
static signed char *sieve_mu(int limit) {
    signed char *mu = calloc(limit + 1, 1);
    int *spf = malloc((limit + 1) * sizeof(int));
    if (!mu || !spf) { fprintf(stderr, "OOM\n"); exit(1); }

    for (int i = 0; i <= limit; i++) spf[i] = i;
    for (int i = 2; (long long)i * i <= limit; i++) {
        if (spf[i] == i) {
            for (int j = i * i; j <= limit; j += i) {
                if (spf[j] == j) spf[j] = i;
            }
        }
    }

    mu[1] = 1;
    for (int n = 2; n <= limit; n++) {
        if (spf[n] == n) {
            mu[n] = -1;
        } else {
            int p = spf[n];
            int m = n / p;
            if (m % p == 0) {
                mu[n] = 0;
            } else {
                mu[n] = -mu[m];
            }
        }
    }
    free(spf);
    return mu;
}

/* Compute |F_N| = 1 + sum_{k=1}^N phi(k) */
static long long farey_size(int N) {
    int *phi = malloc((N + 1) * sizeof(int));
    if (!phi) { fprintf(stderr, "OOM phi\n"); exit(1); }
    for (int i = 0; i <= N; i++) phi[i] = i;
    for (int i = 2; i <= N; i++) {
        if (phi[i] == i) {
            for (int j = i; j <= N; j += i) {
                phi[j] -= phi[j] / i;
            }
        }
    }
    long long n = 1;
    for (int k = 1; k <= N; k++) n += phi[k];
    free(phi);
    return n;
}

/* Compute B+C for prime p using Farey mediant traversal */
static void compute_BC(int p, double *out_BC, double *out_Braw, double *out_dsq, long long *out_n) {
    int N = p - 1;
    long long n = farey_size(N);
    *out_n = n;

    double B_raw_half = 0.0;
    double delta_sq = 0.0;

    /* Mediant traversal of F_N: start 0/1, 1/N */
    long long a = 0, b = 1, c = 1, d = N;
    long long rank = 0;

    while (c <= N) {
        rank++;
        double f_val = (double)c / (double)d;
        double D = (double)rank - (double)n * f_val;
        long long sigma = ((long long)p * c) % d;
        double delta_val = (double)(c - sigma) / (double)d;
        B_raw_half += D * delta_val;
        delta_sq += delta_val * delta_val;

        /* Advance to next Farey fraction */
        long long k = (N + b) / d;
        long long new_c = k * c - a;
        long long new_d = k * d - b;
        a = c; b = d;
        c = new_c; d = new_d;
    }

    *out_Braw = 2.0 * B_raw_half;
    *out_dsq = delta_sq;
    *out_BC = *out_Braw + delta_sq;
}

int main(int argc, char **argv) {
    int LIMIT = 50000;
    int START_FROM = 0;
    if (argc > 1) LIMIT = atoi(argv[1]);
    if (argc > 2) START_FROM = atoi(argv[2]);

    fprintf(stderr, "B+C verification for primes with M(p)<=-3, p<=%d (start_from=%d)\n", LIMIT, START_FROM);
    fprintf(stderr, "Sieving...\n");

    char *is_prime = sieve_primes(LIMIT);
    signed char *mu = sieve_mu(LIMIT);

    /* Count target primes */
    int M = 0;
    int n_target = 0, n_skip = 0;
    for (int k = 1; k <= LIMIT; k++) {
        M += mu[k];
        if (is_prime[k] && k >= 11 && M <= -3) {
            n_target++;
            if (k <= START_FROM) n_skip++;
        }
    }

    fprintf(stderr, "Target primes total: %d, skipping: %d, to compute: %d\n",
            n_target, n_skip, n_target - n_skip);
    fprintf(stderr, "Starting computation...\n");

    /* CSV header only if not resuming */
    if (START_FROM == 0) {
        printf("p,M_p,B_plus_C,B_raw,delta_sq,R,n_farey\n");
        fflush(stdout);
    }

    int violations = 0;
    double min_R = 1e30, min_BC = 1e30;
    int min_R_p = 0, min_BC_p = 0;
    int count = 0;

    time_t wall_start = time(NULL);
    time_t last_report = wall_start;

    M = 0;
    for (int k = 1; k <= LIMIT; k++) {
        M += mu[k];
        if (!is_prime[k] || k < 11) continue;
        if (M > -3) continue;
        if (k <= START_FROM) continue;

        int p = k;
        int Mp = M;
        double BC, Braw, dsq;
        long long n_farey;

        compute_BC(p, &BC, &Braw, &dsq, &n_farey);
        double R = (dsq > 0) ? Braw / dsq : 0.0;

        printf("%d,%d,%.10f,%.10f,%.10f,%.10f,%lld\n",
               p, Mp, BC, Braw, dsq, R, n_farey);
        fflush(stdout);

        if (BC <= 0) violations++;
        if (BC < min_BC) { min_BC = BC; min_BC_p = p; }
        if (R < min_R) { min_R = R; min_R_p = p; }

        count++;
        time_t now = time(NULL);
        if (now - last_report >= 10 || count <= 3) {
            double elapsed = difftime(now, wall_start);
            fprintf(stderr, "  p=%d (M=%d): B+C=%.2f, R=%.4f  [%d/%d done, %.0fs elapsed]\n",
                    p, Mp, BC, R, count, n_target - n_skip, elapsed);
            last_report = now;
        }
    }

    double total_time = difftime(time(NULL), wall_start);
    fprintf(stderr, "\n========================================\n");
    fprintf(stderr, "VERIFICATION COMPLETE\n");
    fprintf(stderr, "========================================\n");
    fprintf(stderr, "  Primes computed:     %d\n", count);
    fprintf(stderr, "  Violations (B+C<=0): %d\n", violations);
    fprintf(stderr, "  Min B+C:             %.6f at p=%d\n", min_BC, min_BC_p);
    fprintf(stderr, "  Min R=B_raw/dsq:     %.6f at p=%d\n", min_R, min_R_p);
    fprintf(stderr, "  Total time:          %.0fs\n", total_time);

    if (violations == 0) {
        fprintf(stderr, "\n  *** B+C > 0 VERIFIED for ALL %d primes computed ***\n\n", count);
    } else {
        fprintf(stderr, "\n  *** FAILED: %d violations ***\n\n", violations);
    }

    free(is_prime);
    free(mu);
    return violations > 0 ? 1 : 0;
}
