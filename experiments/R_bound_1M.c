/*
 * R_bound_1M.c  —  Compute R(p) for qualifying Farey primes
 *
 * R(p) = 2 · Σ D(f)·δ(f) / Σ δ(f)²
 *
 * CORRECT definitions (matching R_bound_fast.c verified reference):
 *
 *   N     = p - 1
 *   F_N   = Farey sequence of order N  (fractions a/b, gcd(a,b)=1, 0 ≤ a/b ≤ 1, b ≤ N)
 *   n_f   = |F_N| = 1 + Σ_{k=1}^{N} φ(k)    ← Farey CARDINALITY, not N or p-1
 *   rank  = 1-indexed position in F_N (rank of first non-zero fraction = 1)
 *   D(f)  = rank(f) − n_f · f                ← uses n_f (cardinality)
 *   σ     = (p · a) mod b                     ← insertion deviation numerator
 *   δ(f)  = (a − σ) / b  for b ≥ 2           ← insertion deviation (NOT Farey gap)
 *   R(p)  = 2 · (Σ D·δ) / (Σ δ²)
 *
 * The old R_bound_1M.c used δ = 1/(b·d) (the Farey gap) — this is WRONG.
 *
 * Output CSV: p, M_p, R, min_R_so_far
 * Also reports whether R ever goes negative.
 *
 * Special: always computes R(243799) regardless of M(p) value.
 *
 * Usage:  ./R_bound_1M [max_p]   (default max_p = 100000)
 *
 * Complexity: O(p²) per prime (Farey iteration through |F_{p-1}| ≈ 3p²/π² fractions).
 * For p=10000: ~30M iterations ≈ fast. For p=100000: ~3B iterations ≈ slow.
 * Recommended test run: max_p = 1000 or 10000.
 *
 * Compile:  gcc -O2 -o R_bound_1M R_bound_1M.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* ─── Sieve: μ, φ, is_prime ─── */

static signed char *mu_arr   = NULL;
static int         *phi_arr  = NULL;
static char        *isp      = NULL;

static void build_sieve(int N) {
    mu_arr  = (signed char *)calloc(N + 1, sizeof(signed char));
    phi_arr = (int *)calloc(N + 1, sizeof(int));
    isp     = (char *)malloc(N + 1);
    if (!mu_arr || !phi_arr || !isp) { fputs("OOM in sieve\n", stderr); exit(1); }

    memset(isp, 1, N + 1);
    isp[0] = isp[1] = 0;
    mu_arr[1]  = 1;
    phi_arr[1] = 1;

    int *primes = (int *)malloc((N + 2) * sizeof(int));
    if (!primes) { fputs("OOM primes\n", stderr); exit(1); }
    int np = 0;

    for (int i = 2; i <= N; i++) {
        if (isp[i]) {
            primes[np++] = i;
            mu_arr[i]    = -1;
            phi_arr[i]   = i - 1;
        }
        for (int j = 0; j < np; j++) {
            long long ip = (long long)i * primes[j];
            if (ip > N) break;
            isp[(int)ip] = 0;
            if (i % primes[j] == 0) {
                mu_arr[(int)ip]  = 0;
                phi_arr[(int)ip] = phi_arr[i] * primes[j];
                break;
            }
            mu_arr[(int)ip]  = (signed char)(-mu_arr[i]);
            phi_arr[(int)ip] = phi_arr[i] * (primes[j] - 1);
        }
    }
    free(primes);
}

/* |F_N| = 1 + Σ_{k=1}^{N} φ(k) */
static long long farey_cardinality(int N) {
    long long cnt = 1;
    for (int k = 1; k <= N; k++) cnt += phi_arr[k];
    return cnt;
}

/* ─── Core computation: R(p) using CORRECT delta definition ─── */
/*
 * Iterates F_{p-1} via mediant recurrence.
 * At each step (a0/b0, a1/b1) are consecutive fractions; a1/b1 is current.
 * rank starts at 0 for 0/1; we increment before processing each new fraction.
 *
 * δ(a/b) = (a - (p*a mod b)) / b   for b ≥ 2
 *       This is the insertion deviation: floor(p*a/b) - (p-1)*(a/b) rescaled.
 *
 * D(a/b) = rank - n_f * (a/b)       where n_f = |F_{p-1}|
 *
 * R = 2 * Σ(D·δ) / Σ(δ²)
 */
static double compute_R(int p, long long n_farey) {
    const long long N = p - 1;
    const double n_f  = (double)n_farey;

    double sum_D_delta = 0.0;
    double delta_sq    = 0.0;
    long long rank = 0;

    /* Farey iteration: start from (0/1, 1/N)
     * Use long long throughout to avoid overflow for large p (N ~ 243798 would
     * cause k*a1 ~ N^2/4 ~ 1.5e10 which overflows int32). */
    long long a0 = 0, b0 = 1;
    long long a1 = 1, b1 = N;

    while (a1 <= N) {
        rank++;
        long long a = a1, b = b1;

        double D_val = (double)rank - n_f * ((double)a / (double)b);

        if (b >= 2) {
            long long sigma  = ((long long)p * a) % b;
            double delta     = (double)(a - sigma) / (double)b;
            delta_sq        += delta * delta;
            sum_D_delta     += D_val * delta;
        }

        long long k  = (N + b0) / b1;
        long long a2 = k * a1 - a0;
        long long b2 = k * b1 - b0;
        a0 = a1; b0 = b1;
        a1 = a2; b1 = b2;
    }

    if (delta_sq < 1e-15) return 0.0;
    return 2.0 * sum_D_delta / delta_sq;
}

/* ─── Main ─── */

int main(int argc, char *argv[]) {
    int max_p = 100000;
    if (argc >= 2) {
        max_p = atoi(argv[1]);
        if (max_p < 2) { fputs("max_p must be >= 2\n", stderr); return 1; }
    }

    /* Sieve must cover max_p and the special prime 243799 */
    int sieve_lim = (max_p > 243799) ? max_p : 243799;
    fprintf(stderr, "Sieving to %d ...\n", sieve_lim);
    build_sieve(sieve_lim);
    fprintf(stderr, "Sieve done. Scanning qualifying primes (M(p) <= -3) up to %d ...\n", max_p);

    puts("p,M_p,R,min_R_so_far");
    fflush(stdout);

    int  Mertens    = 0;
    int  n_qual     = 0;
    int  n_computed = 0;
    double min_R    = 1e30;
    double max_R    = -1e30;
    int  has_nonpos = 0;

    clock_t t_start = clock();

    for (int n = 1; n <= sieve_lim; n++) {
        Mertens += mu_arr[n];

        if (!isp[n]) continue;
        const int p = n;

        int qualifying = (p <= max_p && Mertens <= -3);
        int force      = (p == 243799);  /* always compute, regardless of M value */

        if (!qualifying && !force) continue;
        if (qualifying) n_qual++;

        long long fc = farey_cardinality(p - 1);
        double R     = compute_R(p, fc);

        if (R < min_R) min_R = R;
        if (R > max_R) max_R = R;
        if (R <= 0.0)  has_nonpos = 1;

        printf("%d,%d,%.8f,%.8f\n", p, Mertens, R, min_R);
        fflush(stdout);
        n_computed++;
    }

    double elapsed = (double)(clock() - t_start) / CLOCKS_PER_SEC;

    fprintf(stderr, "\n=== Summary ===\n");
    fprintf(stderr, "  max_p            : %d\n", max_p);
    fprintf(stderr, "  Qualifying (M<=-3): %d primes\n", n_qual);
    fprintf(stderr, "  R computed        : %d\n", n_computed);
    if (n_computed > 0) {
        fprintf(stderr, "  R range           : [%.6f, %.6f]\n", min_R, max_R);
        fprintf(stderr, "  R ever <= 0       : %s\n", has_nonpos ? "YES — violation!" : "no");
        fprintf(stderr, "  Min R             : %.8f\n", min_R);
    }
    fprintf(stderr, "  Wall time         : %.2f s\n", elapsed);
    return 0;
}
