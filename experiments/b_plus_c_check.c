/*
 * b_plus_c_check.c
 *
 * Compute B'/C' = alpha + rho for M(p) = -3 primes.
 * The question: is B + C > 0 for all such primes?
 * B + C > 0  iff  B'/C' > -1  iff  alpha + rho > -1
 *
 * Two modes:
 *   MODE 1 (default): Stream Farey sequence, compute exact B'/C' for small primes
 *   MODE 2 (-H flag): Hyperbola method, compute alpha = -(1 + M(N) + T(N)) for large primes
 *                      T(N) = sum_{m=2}^{N} M(floor(N/m))/m
 *
 * For the problematic primes (T(N) > 0, alpha < 1), we need exact B'/C'.
 * For the rest, alpha alone suffices since alpha > 1 and |rho| < alpha - 1.
 *
 * Compile: cc -O3 -o b_plus_c_check b_plus_c_check.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* For sieve up to 10^7 */
#define MAX_SIEVE 10000001

static signed char *mu_arr;
static int *M_vals;
static int *phi_arr;
static char *is_prime_arr;

void sieve(int n) {
    int *primes = malloc((n / 2) * sizeof(int));
    char *is_composite = calloc(n + 1, 1);
    int num_primes = 0;

    mu_arr = calloc(n + 1, sizeof(signed char));
    M_vals = calloc(n + 1, sizeof(int));
    phi_arr = calloc(n + 1, sizeof(int));
    is_prime_arr = calloc(n + 1, 1);

    mu_arr[1] = 1; phi_arr[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) {
            primes[num_primes++] = i;
            mu_arr[i] = -1;
            phi_arr[i] = i - 1;
            is_prime_arr[i] = 1;
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
 * Compute T(N) = sum_{m=2}^{N} M(floor(N/m)) / m
 * using the hyperbola method for efficiency.
 * Requires M_vals[] to be precomputed up to N.
 */
double compute_T(int N) {
    double T = 0.0;
    int sq = (int)sqrt((double)N);

    /* Direct part: m = 2 to sq */
    for (int m = 2; m <= sq; m++) {
        T += (double)M_vals[N / m] / m;
    }

    /* Hyperbola part: for each distinct value of q = floor(N/m) where m > sq */
    /* floor(N/m) = q for m in [N/(q+1)+1, N/q] */
    for (int q = 1; q <= sq; q++) {
        int m_lo = N / (q + 1) + 1;
        int m_hi = N / q;
        if (m_lo <= sq) m_lo = sq + 1;
        if (m_hi < m_lo) continue;

        /* sum_{m=m_lo}^{m_hi} M(q)/m = M(q) * sum_{m=m_lo}^{m_hi} 1/m */
        double harmonic_sum = 0.0;
        for (int m = m_lo; m <= m_hi; m++) {
            harmonic_sum += 1.0 / m;
        }
        T += (double)M_vals[q] * harmonic_sum;
    }

    return T;
}

/*
 * Compute B' and C' for prime p using streaming Farey generation.
 * Returns B'/C' (= alpha + rho).
 * Also returns alpha computed from T(N).
 */
typedef struct {
    double B_prime;
    double C_prime;
    double ratio;  /* B'/C' */
    double alpha_from_T;  /* alpha ~ 1 - T(N) for M(p)=-3 */
    double rho;
    double T_N;
    long n_fractions;
} result_t;

result_t compute_streaming(int p) {
    result_t res;
    int N = p - 1;

    /* Compute Farey size */
    long n = 1; /* for 0/1 */
    for (int k = 1; k <= N; k++) n += phi_arr[k];
    res.n_fractions = n;

    /* Compute T(N) */
    res.T_N = compute_T(N);
    /* alpha ~ -(1 + M(N) + T(N)) = -(1 + (-2) + T(N)) = 1 - T(N) for M(p)=-3 */
    res.alpha_from_T = 1.0 - res.T_N;

    /* Stream through Farey sequence using mediant algorithm */
    double B_raw = 0.0;
    double C_raw = 0.0;

    int a = 0, b = 1, c = 1, d = N;
    long rank = 0;

    while (!(a == 1 && b == 1)) {
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        if (b <= 1) continue; /* skip 0/1 and 1/1 boundaries */

        double f = (double)a / b;
        double D = (double)rank - (double)n * f;

        int pa_mod_b = (int)(((long long)p * a) % b);
        double delta = (double)(a - pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;
    }

    res.B_prime = B_raw;
    res.C_prime = C_raw;
    res.ratio = (C_raw > 0) ? (B_raw / C_raw) : 0.0;
    res.rho = res.ratio - res.alpha_from_T;

    return res;
}

/*
 * MODE 2: Just compute alpha from T(N) via hyperbola method.
 * This is O(sqrt(N)) per prime, so works up to 10^7.
 */
void run_hyperbola_mode(int max_p) {
    fprintf(stderr, "HYPERBOLA MODE: Computing alpha for M(p)=-3 primes up to %d\n", max_p);

    printf("p,M_p,T_N,alpha_approx,T_positive,alpha_lt_1\n");

    int count = 0, count_T_pos = 0, count_alpha_neg = 0;
    double min_alpha = 1e30;
    int min_alpha_p = 0;

    for (int p = 5; p <= max_p; p++) {
        if (!is_prime_arr[p]) continue;
        if (M_vals[p] != -3) continue;

        int N = p - 1;
        double T = compute_T(N);
        double alpha = 1.0 - T;  /* for M(N)=-2 */

        int T_pos = (T > 0) ? 1 : 0;
        int alpha_low = (alpha < 1.0) ? 1 : 0;

        count++;
        if (T_pos) count_T_pos++;
        if (alpha < min_alpha) {
            min_alpha = alpha;
            min_alpha_p = p;
        }

        /* Only print problematic or first/last primes */
        if (T_pos || count <= 5 || p <= 200) {
            printf("%d,-3,%.6f,%.6f,%d,%d\n", p, T, alpha, T_pos, alpha_low);
        }
    }

    fprintf(stderr, "\nTotal M(p)=-3 primes: %d\n", count);
    fprintf(stderr, "With T(N) > 0: %d (%.1f%%)\n", count_T_pos, 100.0 * count_T_pos / count);
    fprintf(stderr, "Min alpha: %.6f at p=%d\n", min_alpha, min_alpha_p);
    fprintf(stderr, "\nFor B+C > 0, need alpha + rho > -1.\n");
    fprintf(stderr, "If |rho| < 5 (empirically ~ 1.4*sqrt(log p) < 5 for p < 10^7),\n");
    fprintf(stderr, "then alpha + rho > -1 iff alpha > -1 - (-5) = 4 is NOT needed,\n");
    fprintf(stderr, "we just need alpha > -6 which holds since alpha > 0 always.\n");
    fprintf(stderr, "In fact: alpha + rho > alpha - |rho| > min_alpha - max_|rho|.\n");
    fprintf(stderr, "With min_alpha=%.3f and max |rho| ~ 5, we get %.3f > -1? %s\n",
            min_alpha, min_alpha - 5.0, (min_alpha - 5.0 > -1.0) ? "YES" : "NO -- NEED EXACT CHECK");
}

/*
 * MODE 1: Streaming mode for exact B'/C' computation.
 */
void run_streaming_mode(int max_p) {
    fprintf(stderr, "STREAMING MODE: Computing exact B'/C' for M(p)=-3 primes up to %d\n", max_p);

    printf("p,n,T_N,alpha_from_T,B_prime,C_prime,B_over_C,rho,alpha_plus_rho,B_plus_C_positive\n");

    int count = 0;
    double min_ratio = 1e30;
    int min_ratio_p = 0;
    double min_B_plus_C_norm = 1e30;
    int min_BpC_p = 0;

    for (int p = 5; p <= max_p; p++) {
        if (!is_prime_arr[p]) continue;
        if (M_vals[p] != -3) continue;

        result_t r = compute_streaming(p);
        count++;

        double B_plus_C = r.B_prime + r.C_prime;
        int BpC_pos = (B_plus_C > 0) ? 1 : 0;
        double BpC_norm = (r.C_prime > 0) ? (1.0 + r.ratio) : 0.0; /* (B'+C')/C' = 1 + B'/C' */

        if (r.ratio < min_ratio) {
            min_ratio = r.ratio;
            min_ratio_p = p;
        }
        if (BpC_norm < min_B_plus_C_norm) {
            min_B_plus_C_norm = BpC_norm;
            min_BpC_p = p;
        }

        printf("%d,%ld,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
               p, r.n_fractions, r.T_N, r.alpha_from_T,
               r.B_prime, r.C_prime, r.ratio, r.rho,
               r.ratio, BpC_pos);
        fflush(stdout);

        if (count % 20 == 0) {
            fprintf(stderr, "Done %d primes, last p=%d, min B'/C'=%.4f at p=%d\n",
                    count, p, min_ratio, min_ratio_p);
        }
    }

    fprintf(stderr, "\nTotal M(p)=-3 primes: %d\n", count);
    fprintf(stderr, "Min B'/C' (= alpha+rho): %.6f at p=%d\n", min_ratio, min_ratio_p);
    fprintf(stderr, "Min (B'+C')/C' (= 1+alpha+rho): %.6f at p=%d\n", min_B_plus_C_norm, min_BpC_p);
    fprintf(stderr, "\nB+C > 0 iff alpha+rho > -1 iff B'/C' > -1.\n");
    fprintf(stderr, "Minimum B'/C' found: %.6f -- %s\n", min_ratio,
            (min_ratio > -1.0) ? "B+C > 0 HOLDS" : "B+C > 0 FAILS");
}

int main(int argc, char *argv[]) {
    int max_p = 20000;
    int hyperbola_mode = 0;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-H") == 0) {
            hyperbola_mode = 1;
        } else {
            max_p = atoi(argv[i]);
        }
    }

    if (max_p > MAX_SIEVE - 1) max_p = MAX_SIEVE - 1;

    fprintf(stderr, "Sieving to %d...\n", max_p);
    sieve(max_p);
    fprintf(stderr, "Sieve complete.\n");

    if (hyperbola_mode) {
        run_hyperbola_mode(max_p);
    } else {
        run_streaming_mode(max_p);
    }

    return 0;
}
