/*
 * wobble_largescale.c
 * ====================
 * Ultra-fast Farey wobble analysis using the O(|F_N|) next-term generator.
 * Computes W(N) = sum (f_j - j/|F_N|)^2 for all N up to max_N.
 *
 * Also computes Mertens function M(N) = sum_{k=1}^{N} mu(k) for correlation.
 *
 * Compile:  cc -O3 -o wobble_largescale wobble_largescale.c -lm
 * Run:      ./wobble_largescale 20000
 *           ./wobble_largescale 50000 > results.txt
 *
 * Output: wobble_c_data.csv with columns:
 *   N, wobble, farey_size, is_prime, delta_w, mertens, mu
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* ---------- sieves ---------- */

static int  *phi;       /* Euler totient */
static int  *mu_arr;    /* Möbius function */
static char *is_prime;  /* primality */
static int  *smallest_prime; /* smallest prime factor */

void compute_sieves(int max_n) {
    phi          = malloc((max_n + 1) * sizeof(int));
    mu_arr       = malloc((max_n + 1) * sizeof(int));
    is_prime     = malloc((max_n + 1) * sizeof(char));
    smallest_prime = malloc((max_n + 1) * sizeof(int));

    for (int i = 0; i <= max_n; i++) {
        phi[i]    = i;
        mu_arr[i] = 1;
        is_prime[i] = 1;
        smallest_prime[i] = 0;
    }
    is_prime[0] = is_prime[1] = 0;
    mu_arr[1] = 1;

    for (int p = 2; p <= max_n; p++) {
        if (phi[p] == p) {          /* p is prime */
            is_prime[p] = 1;
            for (int k = p; k <= max_n; k += p) {
                if (smallest_prime[k] == 0) smallest_prime[k] = p;
                phi[k] -= phi[k] / p;
                /* Mobius: mu(n) = 0 if p^2 | n, else multiply by -1 */
                if ((k / p) % p == 0) {
                    mu_arr[k] = 0;  /* p^2 divides k */
                } else {
                    mu_arr[k] = -mu_arr[k];
                }
            }
        } else {
            is_prime[p] = 0;
        }
    }
    /* mu(1) = 1 */
    mu_arr[1] = 1;
}

/* ---------- Farey wobble ---------- */

/*
 * Generate F_N via next-term recurrence and accumulate
 * W(N) = sum_{j=0}^{|F_N|-1} (f_j - j/|F_N|)^2
 *
 * The generator: start with a/b = 0/1, c/d = 1/N.
 * Next term after a/b, c/d (both in F_N) is:
 *   k = floor((N + b) / d)
 *   next = (k*c - a) / (k*d - b)
 */
double compute_wobble(int N, long long farey_size) {
    long long a = 0, b = 1, c = 1, d = N;
    double w = 0.0;
    long long j = 0;
    double inv_fs = 1.0 / (double)farey_size;

    /* First fraction: 0/1 */
    {
        double delta = 0.0 - (double)j * inv_fs;
        w += delta * delta;
        j++;
    }

    while (c <= N) {
        double f     = (double)c / (double)d;
        double delta = f - (double)j * inv_fs;
        w += delta * delta;
        j++;

        long long k  = (N + b) / d;
        long long nc = k * c - a;
        long long nd = k * d - b;
        a = c; b = d; c = nc; d = nd;
    }
    return w;
}

/* ---------- main ---------- */

int main(int argc, char *argv[]) {
    int max_n = (argc > 1) ? atoi(argv[1]) : 20000;

    printf("Fast C Wobble Analysis up to N = %d\n", max_n);
    printf("Computing sieves...\n");
    compute_sieves(max_n);
    printf("Sieves done.\n");
    printf("=============================================================\n");
    fflush(stdout);

    char outfile[256];
    snprintf(outfile, sizeof(outfile), "wobble_c_data_%d.csv", max_n);
    FILE *fout = fopen(outfile, "w");
    if (!fout) { perror("fopen"); return 1; }
    fprintf(fout, "N,wobble,farey_size,is_prime,delta_w,mertens,mu\n");

    long long farey_size = 1;  /* will become |F_1| = 2 after phi[1]=1 is added */
    double prev_w = -1.0;      /* sentinel: no previous wobble yet */
    long long mertens = 0;     /* M(N) = sum mu(k) */
    int violation_count = 0;
    int prime_count = 0;
    int total_primes_ge11 = 0;

    clock_t t0 = clock();

    for (int N = 1; N <= max_n; N++) {
        farey_size += phi[N];   /* |F_N| = 1 + sum_{k=1}^{N} phi(k) */
        mertens    += mu_arr[N];

        double w     = compute_wobble(N, farey_size);
        double delta = (prev_w >= 0.0) ? (prev_w - w) : 0.0;

        int ip = is_prime[N];
        if (ip) {
            prime_count++;
            if (N >= 11) {
                total_primes_ge11++;
                if (delta > 0.0) violation_count++;
            }
        }

        fprintf(fout, "%d,%.15e,%lld,%d,%.15e,%lld,%d\n",
                N, w, farey_size, ip, delta, mertens, mu_arr[N]);

        if (N % 2000 == 0) {
            double elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
            double rate = (N > 0 && elapsed > 0) ? N / elapsed : 0;
            double eta  = (rate > 0) ? (max_n - N) / rate : 0;
            printf("  N=%7d  |F|=%12lld  W=%.10f  M=%6lld  viol=%d/%d"
                   "  [%.0fs, ~%.0fs left]\n",
                   N, farey_size, w, mertens, violation_count,
                   total_primes_ge11, elapsed, eta);
            fflush(stdout);
        }

        prev_w = w;
    }

    fclose(fout);

    double elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("\nCompleted in %.1fs\n", elapsed);
    printf("Total violations (primes>=11 with delta>0): %d / %d\n",
           violation_count, total_primes_ge11);
    printf("Data written to %s\n", outfile);

    free(phi); free(mu_arr); free(is_prime); free(smallest_prime);
    return 0;
}
