/*
 * R_bound_fast.c  — compute R = 2·ΣD·δ / Σδ² for all primes up to LIMIT
 *
 * Key quantities (all per-prime p, N = p-1):
 *   delta_sq   = Σ_{b=2}^{N} Σ_{gcd(a,b)=1} ((a - pa mod b)/b)²
 *   sum_D_delta = Σ_{b=2}^{N} Σ_{gcd(a,b)=1} D(a/b)·(a - pa mod b)/b
 *   R          = 2·sum_D_delta / delta_sq
 *
 * D(a/b) = rank(a/b) - n·(a/b)
 *
 * We compute rank(a/b) by sorting all Farey fractions and scanning them in
 * order. This is O(n log n) per prime, but we use the Farey mediant algorithm
 * for O(n) generation and direct accumulation.
 *
 * Strategy: Generate F_N using mediant algorithm, accumulate D(f)·δ(f) and δ²
 * simultaneously. O(n) per prime = O(N²) total.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAXN 4000

static int mu[MAXN + 1];
static int M_arr[MAXN + 1];  // Mertens function

void compute_mertens(int limit) {
    int sp[MAXN + 1];
    memset(sp, 0, sizeof(sp));
    for (int i = 2; i <= limit; i++) {
        if (sp[i] == 0) {
            for (int j = i; j <= limit; j += i)
                if (sp[j] == 0) sp[j] = i;
        }
    }
    mu[1] = 1;
    for (int n = 2; n <= limit; n++) {
        int p = sp[n];
        if ((n / p) % p == 0) mu[n] = 0;
        else mu[n] = -mu[n / p];
    }
    int s = 0;
    for (int i = 1; i <= limit; i++) {
        s += mu[i];
        M_arr[i] = s;
    }
}

int is_prime_check[MAXN + 1];
int primes[MAXN];
int n_primes;

void sieve(int limit) {
    memset(is_prime_check, 1, sizeof(is_prime_check));
    is_prime_check[0] = is_prime_check[1] = 0;
    for (int i = 2; (long long)i * i <= limit; i++)
        if (is_prime_check[i])
            for (int j = i * i; j <= limit; j += i)
                is_prime_check[j] = 0;
    n_primes = 0;
    for (int i = 2; i <= limit; i++)
        if (is_prime_check[i]) primes[n_primes++] = i;
}

/* Compute rank of a/b in F_N (number of Farey fractions strictly less than a/b).
 * Uses the formula: rank(a/b) = Σ_{d=1}^{N} #{j : j/d < a/b, gcd(j,d)=1}
 *                             = Σ_{d=1}^{N} Σ_{j=1}^{floor((a*d-1)/b)} [gcd(j,d)=1]
 * This is O(N * N/b) per fraction — too slow for direct use.
 *
 * FASTER: generate all Farey fractions in order and count rank inline. */

/* We build F_N via mediant algorithm, compute rank as we go,
   and for each fraction compute D(f)*delta(f). */
double compute_R(int p, long long *out_Mval) {
    int N = p - 1;
    *out_Mval = M_arr[p];

    double delta_sq = 0.0;
    double sum_D_delta = 0.0;

    /* Farey sequence generation: a/b → c/d using mediants */
    /* rank starts at 0 (for 0/1) */
    long long n_farey = 0;
    /* Count |F_N| first */
    {
        /* phi sieve for small N */
        int phi[MAXN + 1];
        for (int i = 0; i <= N; i++) phi[i] = i;
        for (int i = 2; i <= N; i++)
            if (phi[i] == i)  /* prime */
                for (int j = i; j <= N; j += i)
                    phi[j] -= phi[j] / i;
        n_farey = 1;
        for (int k = 1; k <= N; k++) n_farey += phi[k];
    }
    double n_f = (double)n_farey;

    int a0 = 0, b0 = 1, a1 = 1, b1 = N;
    int rank = 0;

    /* Process 0/1 */
    /* D(0/1) = 0 - n*0 = 0; delta(0/1) = 0; skip */

    /* Iterate Farey */
    while (a1 <= N) {
        rank++;
        int a = a1, b = b1;
        double f_val = (double)a / (double)b;
        double D_val = (double)rank - n_f * f_val;

        if (b >= 2) {
            int sigma = ((long long)p * a) % b;
            double delta = (double)(a - sigma) / (double)b;
            delta_sq += delta * delta;
            sum_D_delta += D_val * delta;
        }

        int k = (N + b0) / b1;
        int a2 = k * a1 - a0;
        int b2 = k * b1 - b0;
        a0 = a1; b0 = b1;
        a1 = a2; b1 = b2;
    }

    if (delta_sq < 1e-15) return 0.0;
    return 2.0 * sum_D_delta / delta_sq;
}

int main(void) {
    int LIMIT = 3000;
    compute_mertens(LIMIT);
    sieve(LIMIT);

    printf("p,M_p,R,B_plus_C_sign,margin_above_neg1\n");

    double min_R = 1e18, max_R = -1e18;
    int violations = 0;
    int count = 0;

    for (int i = 0; i < n_primes; i++) {
        int p = primes[i];
        if (p < 11 || p > LIMIT) continue;

        long long Mp;
        double R = compute_R(p, &Mp);

        double margin = R + 1.0;  /* R > -1 means margin > 0 */
        int BpC_positive = (margin > 0) ? 1 : 0;

        if (!BpC_positive) violations++;
        if (R < min_R) min_R = R;
        if (R > max_R) max_R = R;
        count++;

        printf("%d,%lld,%.6f,%d,%.6f\n", p, Mp, R, BpC_positive, margin);
    }

    fprintf(stderr, "\n=== SUMMARY ===\n");
    fprintf(stderr, "Primes tested (11..%d): %d\n", LIMIT, count);
    fprintf(stderr, "R range: [%.4f, %.4f]\n", min_R, max_R);
    fprintf(stderr, "Violations (B+C <= 0, i.e. R <= -1): %d\n", violations);
    fprintf(stderr, "Min margin (R+1): %.4f\n", min_R + 1.0);

    return 0;
}
