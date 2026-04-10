/*
 * ca_ratio_fast.c
 * Compute C/A = delta_sq/dilution_raw for M(p) <= -3 primes
 * to understand asymptotic behavior.
 *
 * Key quantities:
 *   delta_sq = sum_{b=2}^{p-1} (1/b^2) * sum_{a coprime b} (a - pa mod b)^2
 *   old_D_sq = sum_{f in F_{p-1}} D(f)^2  (computed via Farey sequence)
 *   dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
 *   C/A = delta_sq / dilution_raw
 *
 * Compile: cc -O3 -o ca_ratio_fast ca_ratio_fast.c -lm
 * Run: ./ca_ratio_fast 10000
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_N 200001

static int mu[MAX_N];
static int M_vals[MAX_N];  // Mertens function
static int phi_vals[MAX_N];

void sieve_mu_phi(int n) {
    /* Linear sieve for mu and phi */
    static int primes[MAX_N];
    static int is_composite[MAX_N];
    int num_primes = 0;

    mu[1] = 1;
    phi_vals[1] = 1;

    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) {
            primes[num_primes++] = i;
            mu[i] = -1;
            phi_vals[i] = i - 1;
        }
        for (int j = 0; j < num_primes && (long long)i * primes[j] <= n; j++) {
            int ip = i * primes[j];
            is_composite[ip] = 1;
            if (i % primes[j] == 0) {
                mu[ip] = 0;
                phi_vals[ip] = phi_vals[i] * primes[j];
                break;
            } else {
                mu[ip] = -mu[i];
                phi_vals[ip] = phi_vals[i] * (primes[j] - 1);
            }
        }
    }

    /* Mertens function */
    M_vals[0] = 0;
    for (int i = 1; i <= n; i++) {
        M_vals[i] = M_vals[i-1] + mu[i];
    }
}

int gcd(int a, int b) {
    while (b) { int t = b; b = a % b; a = t; }
    return a;
}

/* Compute delta_sq for prime p.
 * delta_sq = sum_{b=2}^{N} sum_{a=1, gcd(a,b)=1}^{b-1} (a - p*a mod b)^2 / b^2
 */
double compute_delta_sq(int p) {
    int N = p - 1;
    double total = 0.0;

    for (int b = 2; b <= N; b++) {
        long long sum = 0;
        for (int a = 1; a < b; a++) {
            if (gcd(a, b) == 1) {
                int pa_mod_b = (int)(((long long)p * a) % b);
                int diff = a - pa_mod_b;
                sum += (long long)diff * diff;
            }
        }
        if (sum > 0) {
            total += (double)sum / ((double)b * b);
        }
    }
    return total;
}

/* Compute old_D_sq and n using Farey sequence generation.
 * Returns n (size of F_{p-1}).
 * Writes old_D_sq to *old_D_sq_out.
 */
long compute_farey_stats(int p, double *old_D_sq_out) {
    int N = p - 1;

    /* Generate Farey sequence F_N and compute D(f) = rank - n*f */
    /* Use O(n) Farey generation: start with 0/1, 1/N */

    /* First compute n = |F_N| */
    long n = 0;
    for (int b = 1; b <= N; b++) {
        n += phi_vals[b];
    }
    n += 1;  /* Add 0/1 */

    /* Now compute old_D_sq via exact Farey generation */
    double sum = 0.0;
    int a = 0, b = 1;
    int c = 1, d = N;
    long rank = 0;

    while (1) {
        /* Current fraction: a/b */
        double f = (double)a / b;
        double D = rank - (double)n * f;
        sum += D * D;

        if (a == 1 && b == 1) break;

        /* Next Farey fraction */
        int k = (N + b) / d;
        int na = k * c - a;
        int nb = k * d - b;
        a = c; b = d;
        c = na; d = nb;
        rank++;
    }

    *old_D_sq_out = sum;
    return n;
}

int main(int argc, char *argv[]) {
    int MAX_P = 10000;
    if (argc > 1) MAX_P = atoi(argv[1]);

    fprintf(stderr, "Sieving to %d...\n", MAX_P);
    sieve_mu_phi(MAX_P);
    fprintf(stderr, "Done. Computing quantities for M(p) <= -3 primes...\n");

    printf("p,M,n,old_D_sq,delta_sq,dilution_raw,C_A,C_W,W\n");

    int count = 0;
    for (int p = 11; p <= MAX_P; p += 2) {
        /* Check if prime */
        if (mu[p] == 0 && p > 2) continue;  /* composite if mu[p] == 0 */
        /* Actually mu[p] = -1 for primes, 0 for composites with repeated factors,
           +/-1 for squarefree composites. Need proper prime check. */
        /* Simple check: is p prime? */
        int is_prime = (mu[p] == -1);  /* True for primes since they're squarefree with 1 factor */
        if (!is_prime) {
            /* Could also be squarefree composite with odd/even prime factors */
            /* Use trial division for small p */
            is_prime = 1;
            for (int q = 3; q * q <= p; q += 2) {
                if (p % q == 0) { is_prime = 0; break; }
            }
        }
        if (!is_prime) continue;
        if (mu[p] != -1) continue;  /* Not prime */

        /* Check Mertens function */
        if (M_vals[p] > -3) continue;

        int N = p - 1;

        /* Compute quantities */
        double old_D_sq;
        long n = compute_farey_stats(p, &old_D_sq);
        long n_prime = n + (p - 1);

        double delta_sq = compute_delta_sq(p);

        double dil = old_D_sq * ((double)n_prime * n_prime - (double)n * n) / ((double)n * n);
        double W = old_D_sq / ((double)n * n);
        double C_W = N * W;
        double C_A = delta_sq / dil;

        printf("%d,%d,%ld,%.6f,%.6f,%.6f,%.6f,%.6f,%.8f\n",
               p, M_vals[p], n, old_D_sq, delta_sq, dil, C_A, C_W, W);
        fflush(stdout);

        count++;
        if (count % 10 == 0) {
            fprintf(stderr, "Processed %d primes, last p=%d\n", count, p);
        }
    }

    fprintf(stderr, "Done. Total: %d primes with M(p) <= -3 up to p=%d\n", count, MAX_P);
    return 0;
}
