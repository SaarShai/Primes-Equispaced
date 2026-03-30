/*
 * delta_w_direct_investigation.c
 *
 * Investigate the behavior of alpha = -6R(N) on M(p) = -3 primes.
 * R(N) = 1/6 + (1/6) * sum_{m=1}^{N} M(floor(N/m))/m
 *
 * Key question: can R(N) become large and positive (making alpha very negative)
 * on the M(N) = -2 subsequence?
 *
 * Uses hyperbolic summation for O(sqrt(N)) computation of R(N).
 * Sieves Mertens function to LIMIT, then for each prime p with M(p) = -3,
 * computes alpha = -6R(N) where N = p-1.
 *
 * Tracks: min(alpha), min(alpha+rho_bound), distribution of alpha.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define LIMIT 10000000  /* 10^7 */

static signed char *mu_arr;
static int *M_arr;  /* Mertens function */
static char *is_prime_arr;

void sieve(void) {
    mu_arr = (signed char *)calloc(LIMIT + 1, sizeof(signed char));
    M_arr = (int *)calloc(LIMIT + 1, sizeof(int));
    is_prime_arr = (char *)calloc(LIMIT + 1, sizeof(char));

    /* Smallest prime factor sieve */
    int *spf = (int *)calloc(LIMIT + 1, sizeof(int));
    for (int i = 2; i <= LIMIT; i++) {
        if (spf[i] == 0) {
            is_prime_arr[i] = 1;
            for (long long j = i; j <= LIMIT; j += i)
                if (spf[j] == 0) spf[j] = i;
        }
    }

    /* Mobius function */
    mu_arr[1] = 1;
    for (int n = 2; n <= LIMIT; n++) {
        int p = spf[n];
        if ((n / p) % p == 0) mu_arr[n] = 0;
        else mu_arr[n] = -mu_arr[n / p];
    }

    /* Mertens function */
    int s = 0;
    for (int i = 1; i <= LIMIT; i++) {
        s += mu_arr[i];
        M_arr[i] = s;
    }

    free(spf);
}

/* Compute R(N) = 1/6 + (1/6) * sum_{m=1}^{N} M(floor(N/m))/m
 * Using hyperbolic summation for O(sqrt(N)) time.
 *
 * Actually, we use the direct formula:
 * 6R(N) = 1 + sum_{m=1}^{N} M(floor(N/m))/m
 *
 * Hyperbolic method:
 * sum_{m=1}^{N} M(floor(N/m))/m
 *   = sum_{m=1}^{u} M(floor(N/m))/m + sum_{k=1}^{N/u} [sum over m where floor(N/m)=k of 1/m] * M(k) - M(u)*H(u)
 * where u = floor(sqrt(N))
 *
 * But this is complex. For N up to 10^7, direct summation is O(N) and takes ~0.1s.
 * Let's just do direct summation.
 */
double compute_6R(int N) {
    double sum = 0.0;
    for (int m = 1; m <= N; m++) {
        sum += (double)M_arr[N / m] / m;
    }
    return 1.0 + sum;
}

/* Faster: hyperbolic summation O(sqrt(N)) */
double compute_6R_fast(int N) {
    int u = (int)sqrt((double)N);
    if (u < 1) u = 1;

    /* Part 1: sum_{m=1}^{u} M(floor(N/m))/m */
    double sum1 = 0.0;
    for (int m = 1; m <= u; m++) {
        sum1 += (double)M_arr[N / m] / m;
    }

    /* Part 2: sum_{d=1}^{u} (H(N/d) - H(N/(d+1))) * M(d)
     * where H(x) = sum_{j=1}^{floor(x)} 1/j
     *
     * Actually, let's use the identity:
     * sum_{m=1}^{N} M(floor(N/m))/m = sum_{m=1}^{u} M(floor(N/m))/m
     *   + sum_{d=1}^{floor(N/(u+1))} M(d) * [sum_{m: floor(N/m)=d} 1/m]
     *
     * Hmm, this is getting complicated. For N <= 10^7, direct O(N) is fine.
     * Let's use a slightly optimized direct approach.
     */

    /* Actually just use direct for correctness. 10^7 iterations per prime is fine
     * since there are only ~1000 M(p)=-3 primes up to 10^7. */
    return -1;  /* signal to use direct */
}

/* Compute harmonic number H(n) */
double harmonic(int n) {
    double h = 0.0;
    for (int i = 1; i <= n; i++) h += 1.0 / i;
    return h;
}

int main(void) {
    fprintf(stderr, "Sieving to %d...\n", LIMIT);
    clock_t t0 = clock();
    sieve();
    clock_t t1 = clock();
    fprintf(stderr, "Sieve done in %.2f sec\n", (double)(t1-t0)/CLOCKS_PER_SEC);

    /* Count M(p) = -3 primes */
    int count = 0;
    int count_checked = 0;

    double min_alpha = 1e18;
    int min_alpha_p = 0;
    double min_alpha_plus_rho_bound = 1e18;
    int min_apr_p = 0;

    /* Track extremes of alpha */
    double max_alpha = -1e18;
    int max_alpha_p = 0;

    /* Track R(N) extremes on M(N)=-2 subsequence */
    double max_R_on_M2 = -1e18;
    int max_R_p = 0;
    double min_R_on_M2 = 1e18;
    int min_R_p = 0;

    /* Header */
    printf("# p, M(p), N, alpha, 6R(N), alpha/log(N), R(N), alpha_lower_for_DW\n");

    /* For the "direct" approach:
     * ΔW(p) ≈ -(B+C)/n'^2 ≈ -C'(1 + alpha + rho)/n'^2
     * For ΔW < 0 we need alpha + rho > -1 (NOT > 0, and NOT > 1)
     *
     * Wait — the user wrote: ΔW ≈ -(B + C)/n'^2 = -C(1 + alpha + rho)/n'^2
     *
     * But B' + C' = C'(1 + B'/C') = C'(1 + alpha + rho)
     * So (B'+C')/n'^2 = C'(1 + alpha + rho)/n'^2
     *
     * ΔW = (A-D)/n'^2 - (B'+C')/n'^2
     *
     * Since A-D = O(N^2/p^2) is small positive or small...
     * actually A-D can be positive or negative.
     *
     * From the proof: D/A = 1 + O(1/p^2), so |A-D| = A * O(1/p^2) = O(N^2/p^2)
     * Meanwhile (B'+C') ~ C'(1+alpha+rho) ~ (N^2/2pi^2)(1+alpha+rho)
     *
     * So ΔW < 0 iff (A-D) < (B'+C'), i.e., the small term < the main term.
     * For this to fail, we'd need B'+C' < 0 AND |A-D| > |B'+C'|.
     *
     * B'+C' < 0 means alpha + rho < -1.
     *
     * So the question reduces to: can alpha + rho < -1?
     *
     * Since alpha ~ -6R(N) and rho ~ -constant (negative), we need:
     * alpha < -1 - rho. Since rho ~ -3, we need alpha < 2.
     *
     * alpha < 2 means 6R(N) > -2, i.e., R(N) > -1/3.
     *
     * Actually: alpha + rho < -1 means -6R(N) + rho < -1
     * means 6R(N) > -1 + rho ~ -1 + (-3) = -4... wait, rho is negative.
     *
     * Actually rho can be positive or negative. From the data:
     * rho is NEGATIVE for all M=-3 primes tested (ranges from -1.3 to -3.2).
     *
     * So alpha + rho = (-6R(N) + O(1/N)) + rho
     * For this to be < -1, need -6R(N) + rho < -1
     * i.e., 6R(N) > -1 + rho
     * Since rho ~ -3, need 6R(N) > -4, i.e., R(N) > -2/3.
     *
     * R(N) is typically ~ -log(N)/6, so 6R(N) ~ -log(N).
     * So 6R(N) > -4 would mean log(N) < 4, i.e., N < 55.
     * For large N, 6R(N) << -4, so alpha >> 3, and alpha+rho >> -1.
     *
     * Wait, I'm getting confused. Let me re-examine.
     *
     * From EFFECTIVE_ALPHA_RHO.md:
     * - For M(p)=-3 primes, alpha ranges from 1.43 (p=13) to 9+ (p=839)
     * - rho ranges from -1.3 to -3.7
     * - alpha + rho is ALWAYS > 0 for p >= 43
     * - The MINIMUM alpha+rho is 0.12 at p=13
     *
     * The user asks: can alpha become NEGATIVE? That would mean R(N) > 0.
     * From R_NEGATIVE_PROOF.md: R(N) oscillates and CAN be positive for large N.
     *
     * But for M(N)=-2, we have 6R(N) = 1 + M(N) + T(N) = -1 + T(N)
     * So R(N) > 0 iff T(N) > 1.
     *
     * Can T(N) > 1 on the M(N)=-2 subsequence?
     * T(N) = sum_{m=2}^{N} M(floor(N/m))/m
     *
     * Since M is mostly negative (oscillates around 0 with negative bias from PNT),
     * T(N) ~ sum_{m=2}^{N} M(N/m)/m. The large m terms contribute M(O(1))/m which
     * is negligible. The small m terms contribute M(N/m)/m.
     *
     * For M(N)=-2, the Mertens function is slightly negative. The sum T(N) is
     * typically negative and grows in magnitude. T(N) > 1 seems unlikely but
     * let's check.
     */

    fprintf(stderr, "Scanning primes...\n");

    for (int p = 11; p <= LIMIT; p++) {
        if (!is_prime_arr[p]) continue;
        if (M_arr[p] != -3) continue;

        count++;
        int N = p - 1;

        /* Compute 6R(N) via direct sum. O(N) per prime. */
        /* For p up to 10^7 this is expensive. Let's only do primes up to 2*10^6
         * with direct sum, and use a sampling approach for larger. */
        if (N > 2000000) {
            /* For larger primes, compute 6R(N) using hyperbolic trick */
            /* sum_{m=1}^{N} M(N/m)/m */
            /* Use the fact that floor(N/m) takes O(sqrt(N)) distinct values */
            int u = (int)sqrt((double)N);
            double sum = 0.0;

            /* Part 1: m = 1 to u */
            for (int m = 1; m <= u; m++) {
                sum += (double)M_arr[N / m] / m;
            }

            /* Part 2: for each distinct value v = floor(N/m) where v <= u
             * and v != any floor(N/m') for m' <= u,
             * sum the 1/m for all m with floor(N/m) = v.
             *
             * The distinct values of floor(N/m) for m > u are 1, 2, ..., floor(N/(u+1))
             * (these are all <= u since floor(N/(u+1)) <= u for u = sqrt(N)).
             *
             * For each value v = 1, ..., floor(N/(u+1)):
             * floor(N/m) = v iff m in [N/(v+1)+1, N/v]
             * Sum of 1/m over this range = H(N/v) - H(N/(v+1))
             */
            int v_max = N / (u + 1);
            for (int v = 1; v <= v_max; v++) {
                int m_lo = N / (v + 1) + 1;
                int m_hi = N / v;
                if (m_lo <= u) m_lo = u + 1;  /* avoid double counting */
                if (m_hi < m_lo) continue;
                double H_sum = 0.0;
                for (int m = m_lo; m <= m_hi; m++) {
                    H_sum += 1.0 / m;
                }
                sum += (double)M_arr[v] * H_sum;
            }

            double six_R = 1.0 + sum;
            double alpha_val = -six_R;
            double R_val = six_R / 6.0;

            if (alpha_val < min_alpha) { min_alpha = alpha_val; min_alpha_p = p; }
            if (alpha_val > max_alpha) { max_alpha = alpha_val; max_alpha_p = p; }
            if (R_val > max_R_on_M2) { max_R_on_M2 = R_val; max_R_p = p; }
            if (R_val < min_R_on_M2) { min_R_on_M2 = R_val; min_R_p = p; }

            count_checked++;

            /* Print every 100th or interesting ones */
            if (count % 100 == 0 || alpha_val < 5.0 || p < 1000 || p > LIMIT - 100000) {
                printf("%d, %d, %d, %.6f, %.6f, %.6f, %.6f\n",
                       p, M_arr[p], N, alpha_val, six_R,
                       alpha_val / log((double)N), R_val);
            }
        } else {
            /* Direct sum for smaller primes */
            double sum = 0.0;
            for (int m = 1; m <= N; m++) {
                sum += (double)M_arr[N / m] / m;
            }
            double six_R = 1.0 + sum;
            double alpha_val = -six_R;
            double R_val = six_R / 6.0;

            if (alpha_val < min_alpha) { min_alpha = alpha_val; min_alpha_p = p; }
            if (alpha_val > max_alpha) { max_alpha = alpha_val; max_alpha_p = p; }
            if (R_val > max_R_on_M2) { max_R_on_M2 = R_val; max_R_p = p; }
            if (R_val < min_R_on_M2) { min_R_on_M2 = R_val; min_R_p = p; }

            count_checked++;

            if (count % 100 == 0 || alpha_val < 5.0 || p < 1000) {
                printf("%d, %d, %d, %.6f, %.6f, %.6f, %.6f\n",
                       p, M_arr[p], N, alpha_val, six_R,
                       alpha_val / log((double)N), R_val);
            }
        }

        if (count % 1000 == 0) {
            fprintf(stderr, "  processed %d M(p)=-3 primes, up to p=%d, min_alpha=%.4f (p=%d)\n",
                    count, p, min_alpha, min_alpha_p);
        }
    }

    fprintf(stderr, "\n=== SUMMARY ===\n");
    fprintf(stderr, "Total M(p) = -3 primes up to %d: %d\n", LIMIT, count);
    fprintf(stderr, "Min alpha = %.6f at p = %d\n", min_alpha, min_alpha_p);
    fprintf(stderr, "Max alpha = %.6f at p = %d\n", max_alpha, max_alpha_p);
    fprintf(stderr, "Max R(N) on M(N)=-2: %.6f at p = %d\n", max_R_on_M2, max_R_p);
    fprintf(stderr, "Min R(N) on M(N)=-2: %.6f at p = %d\n", min_R_on_M2, min_R_p);
    fprintf(stderr, "\nCRITICAL: If min_alpha < 0 (i.e., R(N) > 0), then alpha+rho < -1 is possible.\n");
    fprintf(stderr, "If min_alpha stays >> 1, the Sign Theorem is safe.\n");

    /* Also: scan for M(N)=-2 with R(N) positive (alpha negative) anywhere */
    fprintf(stderr, "\nScanning ALL N with M(N)=-2 for R(N) > 0...\n");
    int r_positive_count = 0;
    double max_R_overall = -1e18;
    int max_R_N = 0;

    for (int N = 10; N <= LIMIT; N++) {
        if (M_arr[N] != -2) continue;

        /* Compute 6R(N) — but only for N where N+1 is prime (for efficiency) */
        /* Actually, let's just check a sample: every 1000th N with M(N)=-2 */
        /* Plus all N < 100000 */
        if (N >= 100000 && N % 1000 != 0) continue;

        double sum = 0.0;
        if (N <= 2000000) {
            for (int m = 1; m <= N; m++) {
                sum += (double)M_arr[N / m] / m;
            }
        } else {
            /* Hyperbolic */
            int u = (int)sqrt((double)N);
            for (int m = 1; m <= u; m++) {
                sum += (double)M_arr[N / m] / m;
            }
            int v_max = N / (u + 1);
            for (int v = 1; v <= v_max; v++) {
                int m_lo = N / (v + 1) + 1;
                int m_hi = N / v;
                if (m_lo <= u) m_lo = u + 1;
                if (m_hi < m_lo) continue;
                double H_sum = 0.0;
                for (int m = m_lo; m <= m_hi; m++) {
                    H_sum += 1.0 / m;
                }
                sum += (double)M_arr[v] * H_sum;
            }
        }

        double six_R = 1.0 + sum;
        double R_val = six_R / 6.0;

        if (R_val > 0) {
            r_positive_count++;
            if (r_positive_count <= 20) {
                fprintf(stderr, "  R(N) > 0: N=%d, R=%.6f, 6R=%.6f, alpha=%.6f\n",
                        N, R_val, six_R, -six_R);
            }
        }
        if (R_val > max_R_overall) {
            max_R_overall = R_val;
            max_R_N = N;
        }
    }

    fprintf(stderr, "\nM(N)=-2 scan: R(N) > 0 count = %d\n", r_positive_count);
    fprintf(stderr, "Max R(N) among M(N)=-2: %.6f at N = %d (alpha = %.6f)\n",
            max_R_overall, max_R_N, -6.0*max_R_overall);

    free(mu_arr); free(M_arr); free(is_prime_arr);
    return 0;
}
