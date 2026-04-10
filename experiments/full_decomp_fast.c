/*
 * full_decomp_fast.c
 * Compute full four-term decomposition for M(p) <= -3 primes.
 * Outputs B/A, C/A, D/A and sum B/A+C/A+D/A.
 *
 * Key:
 *   A = dilution_raw = old_D_sq * (n'^2 - n^2) / n^2
 *   B = B_raw = 2 * sum_{f in F_{p-1}} D(f) * delta(f)
 *   C = delta_sq = sum delta(f)^2
 *   D = new_D_sq = sum_{k=1}^{p-1} D_new(k/p)^2
 *
 * Compile: cc -O3 -o full_decomp_fast full_decomp_fast.c -lm
 * Run: ./full_decomp_fast 5000
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_N 200001

static int mu_arr[MAX_N];
static int M_vals[MAX_N];
static int phi_vals[MAX_N];

void sieve(int n) {
    int *primes = malloc(n * sizeof(int));
    int *is_composite = calloc(n + 1, sizeof(int));
    int num_primes = 0;

    mu_arr[1] = 1; phi_vals[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) {
            primes[num_primes++] = i;
            mu_arr[i] = -1;
            phi_vals[i] = i - 1;
        }
        for (int j = 0; j < num_primes && (long long)i * primes[j] <= n; j++) {
            int ip = i * primes[j];
            is_composite[ip] = 1;
            if (i % primes[j] == 0) {
                mu_arr[ip] = 0;
                phi_vals[ip] = phi_vals[i] * primes[j];
                break;
            } else {
                mu_arr[ip] = -mu_arr[i];
                phi_vals[ip] = phi_vals[i] * (primes[j] - 1);
            }
        }
    }

    M_vals[0] = 0;
    for (int i = 1; i <= n; i++) M_vals[i] = M_vals[i-1] + mu_arr[i];

    free(primes); free(is_composite);
}

int gcd(int a, int b) {
    while (b) { int t = b; b = a%b; a = t; }
    return a;
}

/* Compute all four terms for prime p.
 * Uses Farey sequence generation (O(n) for the sequence, O(p^2) total for delta_sq).
 */
void compute_decomp(int p,
    double *A_out, double *B_out, double *C_out, double *D_out, long *n_out)
{
    int N = p - 1;

    /* Sieve-based arrays for fast gcd at small scale: not needed here */

    /* Generate Farey sequence F_N with Stern-Brocot / mediant method.
     * Store as arrays of numerators and denominators. */
    int a = 0, b = 1, c = 1, d = N;
    long n = 0;

    /* Count Farey size first */
    n = 1;
    for (int k = 1; k <= N; k++) n += phi_vals[k];

    /* Now generate Farey sequence and compute stats */
    /* Store fracs for binary search (for D computation) */
    int *fnum = malloc(n * sizeof(int));
    int *fden = malloc(n * sizeof(int));
    if (!fnum || !fden) { fprintf(stderr, "OOM\n"); exit(1); }

    /* Generate */
    a = 0; b = 1; c = 1; d = N;
    long idx = 0;
    fnum[idx] = 0; fden[idx] = 1; idx++;
    while (1) {
        int k = (N + b) / d;
        int na = k*c - a, nb = k*d - b;
        a = c; b = d; c = na; d = nb;
        fnum[idx] = a; fden[idx] = b; idx++;
        if (a == 1 && b == 1) break;
    }
    /* idx should equal n */

    /* Compute old_D_sq = sum D(f)^2, sum D*delta, delta_sq via one pass */
    double old_D_sq = 0.0;
    double B_raw = 0.0;
    double delta_sq = 0.0;

    for (long j = 0; j < n; j++) {
        int fa = fnum[j], fb = fden[j];
        if (fa == 0 || fa == fb) continue;  /* skip 0/1 and 1/1 (boundary) */

        double f = (double)fa / fb;
        double D = j - (double)n * f;
        old_D_sq += D * D;

        /* delta(fa/fb) = (fa - p*fa mod fb) / fb */
        int pa_mod_b = (int)(((long long)p * fa) % fb);
        double delta = (double)(fa - pa_mod_b) / fb;
        delta_sq += delta * delta;
        B_raw += 2.0 * D * delta;
    }
    /* Add 0/1 and 1/1 */
    /* D(0/1) = 0 - n*0 = 0 */
    /* D(1/1) = (n-1) - n*1 = -1, delta(1/1) = 0 (boundary) */
    old_D_sq += 1.0;  /* D(1)^2 = (-1)^2 = 1 */
    B_raw += 0.0;  /* delta at boundary is 0 */
    delta_sq += 0.0;  /* delta at boundary is 0 */

    /* Compute new_D_sq using binary search */
    /* D_new(k/p) = D_old(k/p) + k/p where D_old is evaluated at k/p
     * D_old(k/p) = #{f in F_{p-1} : f <= k/p} - n * (k/p)
     * The rank is found by binary search in fnum/fden. */
    double new_D_sq = 0.0;
    for (int k = 1; k < p; k++) {
        /* Binary search: find rank = #{j : fnum[j]/fden[j] <= k/p} */
        long lo = 0, hi = n;
        while (lo < hi) {
            long mid = (lo + hi) / 2;
            /* fnum[mid]/fden[mid] <= k/p iff fnum[mid]*p <= k*fden[mid] */
            if ((long long)fnum[mid] * p <= (long long)k * fden[mid])
                lo = mid + 1;
            else
                hi = mid;
        }
        long rank_old = lo;  /* # fractions <= k/p */
        double kp = (double)k / p;
        double D_old = rank_old - (double)n * kp;
        double D_new = D_old + kp;
        new_D_sq += D_new * D_new;
    }

    /* Compute dilution_raw */
    long n_prime = n + (p - 1);
    double dil = old_D_sq * ((double)n_prime * n_prime - (double)n * n) / ((double)n * n);

    *A_out = dil;
    *B_out = B_raw;
    *C_out = delta_sq;
    *D_out = new_D_sq;
    *n_out = n;

    free(fnum); free(fden);
}

int main(int argc, char *argv[]) {
    int MAX_P = 5000;
    if (argc > 1) MAX_P = atoi(argv[1]);

    fprintf(stderr, "Sieving to %d...\n", MAX_P);
    sieve(MAX_P);
    fprintf(stderr, "Computing full decomposition for M(p) <= -3 primes...\n");

    printf("p,M,n,A,B,C,D,B_A,C_A,D_A,BCD_A\n");

    int count = 0;
    for (int p = 11; p <= MAX_P; p += 2) {
        /* Check primality: prime iff mu[p] == -1 AND p is actually squarefree with 1 factor */
        /* For proper primality: use trial division for odd p */
        {
            int is_prime = 1;
            for (int q = 3; (long long)q*q <= p; q += 2) {
                if (p % q == 0) { is_prime = 0; break; }
            }
            if (!is_prime) continue;
        }
        if (M_vals[p] > -3) continue;

        double A, B, C, D;
        long n;
        compute_decomp(p, &A, &B, &C, &D, &n);

        double B_A = B / A;
        double C_A = C / A;
        double D_A = D / A;
        double BCD_A = B_A + C_A + D_A;

        printf("%d,%d,%ld,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               p, M_vals[p], n, A, B, C, D, B_A, C_A, D_A, BCD_A);
        fflush(stdout);

        count++;
        if (count % 20 == 0) {
            fprintf(stderr, "Done %d primes, last p=%d\n", count, p);
        }
    }

    fprintf(stderr, "Total: %d primes with M(p) <= -3\n", count);
    return 0;
}
