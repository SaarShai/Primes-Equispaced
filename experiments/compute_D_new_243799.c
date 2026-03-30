/*
 * compute_D_new_243799.c
 *
 * Compute D_new = sum_{k=1}^{p-1} D_{F_p}(k/p)^2 for p = 243799.
 *
 * D_{F_p}(k/p) = rank(k/p in F_p) - n' * k/p
 *              = N_{p-1}(k/p) + k - 1 - n'*k/p
 *
 * where N_{p-1}(x) = #{f in F_{p-1} : f <= x}.
 *
 * N_N(k/p) for p prime, 1 <= k <= p-1:
 *   = 1 + sum_{b=1}^{N} #{a: 1 <= a < b, gcd(a,b)=1, a/b <= k/p}
 *     + #{b: b <= N, gcd(b,b)=1, b/b <= k/p}   (i.e., +1 if k/p >= 1, but k < p so k/p < 1)
 *
 * Actually: N_N(k/p) = 1 + sum_{b=1}^{N} floor(bk/p) - sum_{b=1}^{N} sum_{d|b, d>1} mu(d)*floor(bk/(pd))
 *
 * Simpler: N_N(x) for x not in F_N is:
 *   N_N(x) = 1 + sum_{b=1}^{N} sum_{a=1, gcd(a,b)=1}^{floor(bx)} 1
 *          = 1 + sum_{b=1}^{N} sum_{d|b} mu(d) * floor(floor(bx)/d)
 *
 * For x = k/p: floor(b*k/p) = floor(bk/p). Since p is prime and b < p, bk/p is never integer
 * (when gcd(b,p)=1, i.e., always for b < p).
 *
 * N_N(k/p) = 1 + sum_{b=1}^{N} sum_{d|b} mu(d) * floor(bk/(pd))
 *
 * This is O(N * max_divisors(N)) per k, and there are p-1 values of k.
 * Total: O(N * p * max_div) ~ O(N^2 * max_div) which is too slow for N = 243798.
 *
 * FASTER APPROACH: Use the Mobius inversion formula:
 *
 * N_N(k/p) = 1 + sum_{d=1}^{N} mu(d) * sum_{m=1}^{floor(N/d)} floor(mk/(pd))
 *
 * Wait, let's think again.
 *
 * sum_{b=1}^{N} #{a: 1<=a<=floor(bk/p), gcd(a,b)=1}
 * = sum_{b=1}^{N} sum_{d|gcd(a,b)} mu(d) ... (Mobius inversion)
 * = sum_{d=1}^{N} mu(d) * sum_{b': 1<=b'<=floor(N/d)} floor(b'd*k/(pd))
 *   ... hmm this is wrong
 *
 * Let me use a different approach. For each k, compute N_{p-1}(k/p) using:
 *
 * N_N(x) = 1 + sum_{b=1}^{N} Phi(floor(b*x), b)
 *
 * where Phi(m, b) = #{a: 1 <= a <= m, gcd(a,b) = 1} = sum_{d|b} mu(d) * floor(m/d).
 *
 * For x = k/p: floor(b*k/p) = F. Then Phi(F, b) = sum_{d|b} mu(d)*floor(F/d).
 *
 * We precompute for each b, its divisors d where mu(d) != 0.
 * Then for each k, for each b, compute F = floor(bk/p), then
 *   Phi(F,b) = sum_{d|b, mu(d)!=0} mu(d) * floor(F/d).
 *
 * This is O(N * avg_divisors) per k, and p values of k.
 * With N = p-1 = 243798, avg_divisors ~ 10, this is
 * O(243798 * 10 * 243798) ~ 6*10^11 operations. Way too slow.
 *
 * MUCH FASTER: Use the hyperbolic counting trick.
 *
 * N_N(x) - 1 = sum_{b=1}^{N} sum_{d|b} mu(d) * floor(bx/d)
 *
 * Wait, that's not right either. Let me start from scratch.
 *
 * N_N(x) = #{a/b : 0 <= a/b <= x, 1 <= b <= N, gcd(a,b) = 1}
 *
 * For x = k/p with 0 < k < p:
 *   = #{(a,b): 0 <= a <= bk/p, 1 <= b <= N, gcd(a,b) = 1}
 *   = sum_{b=1}^{N} sum_{a=0}^{floor(bk/p)} [gcd(a,b) = 1]
 *
 * The a=0 term: gcd(0,b) = b, so [gcd(0,b)=1] = [b=1]. So the b=1 term
 * contributes a=0 (the fraction 0/1) and possibly a=1 if k/p >= 1 (no).
 * Actually for b=1: floor(1*k/p) = floor(k/p) = 0 (since k < p). So a ranges from 0 to 0.
 * gcd(0,1) = 1, so it contributes 1.
 *
 * For b >= 2: a ranges from 0 to floor(bk/p). The a=0 term has gcd(0,b) = b >= 2,
 * so it doesn't count.
 *
 * So: N_N(k/p) = 1 + sum_{b=2}^{N} #{a: 1 <= a <= floor(bk/p), gcd(a,b) = 1}
 *
 * Using Mobius:
 * #{a: 1 <= a <= m, gcd(a,b)=1} = sum_{d|b} mu(d) * floor(m/d)
 *
 * So: N_N(k/p) = 1 + sum_{b=2}^{N} sum_{d|b} mu(d) * floor(floor(bk/p) / d)
 *
 * Rewrite: let e = b/d (since d|b), so b = de, d >= 1, e >= 1, de <= N.
 *
 * = 1 + sum_{d=1}^{N} mu(d) * sum_{e=1}^{floor(N/d)} floor(floor(dek/p) / d)
 *   minus the b=1 correction (b=1 means d=1, e=1, giving floor(floor(k/p)/1) = 0,
 *   and this doesn't over-count since the sum starts at b=2 but (d,e)=(1,1) gives b=1).
 *
 * Hmm, actually (d,e)=(1,1) gives b=1 which should be excluded from the sum starting at b=2.
 * And for d >= 2 with e = 1, b = d >= 2.
 * For d=1, e >= 2, b = e >= 2.
 *
 * So the double sum over d >= 1, e >= 1 with de >= 2 covers all b >= 2.
 *
 * N_N(k/p) = 1 + sum_{d=1}^{N} mu(d) * [sum_{e=1}^{floor(N/d)} floor(dek/p / d)]
 *            - mu(1) * floor(floor(k/p)/1)
 *          = 1 + sum_{d=1}^{N} mu(d) * sum_{e=1}^{floor(N/d)} floor(ek/p) - 0
 *
 * Wait: floor(floor(dek/p)/d) = floor(dek/(pd)) -- is this true?
 * Actually floor(dek/p) / d is not necessarily an integer.
 * Let me think again.
 *
 * For b = de: floor(bk/p) = floor(dek/p). And floor(floor(dek/p)/d) is not floor(ek/p).
 *
 * Example: d=2, e=3, k=5, p=13. b=6. floor(6*5/13) = floor(30/13) = 2.
 * floor(2/2) = 1. But floor(3*5/13) = floor(15/13) = 1. So it matches here.
 *
 * General: floor(floor(de*k/p)/d) = floor(ek/p) when p is prime and doesn't divide de.
 * Since p is prime and b = de < p, p doesn't divide de. So dek/p is not an integer.
 * dek/p = e*k/p * d. floor(dek/p) = d*floor(ek/p) + floor(d*{ek/p}).
 * floor(floor(dek/p)/d) = floor(ek/p) + floor(floor(d*{ek/p})/d).
 * The second term = floor(d*{ek/p}/d) = floor({ek/p}) = 0 (since {ek/p} < 1).
 * Wait: floor(d*{ek/p}) could be 0, 1, ..., d-1.
 * floor(floor(d*{ek/p})/d) = 0 always (since 0 <= floor(d*{ek/p}) <= d-1, so floor/d = 0).
 *
 * So floor(floor(dek/p)/d) = floor(ek/p). YES!
 *
 * Therefore:
 * N_N(k/p) = 1 + sum_{d=1}^{N} mu(d) * [sum_{e=1}^{floor(N/d)} floor(ek/p)] - [d=1,e=1 term]
 *          = 1 + sum_{d=1}^{N} mu(d) * sum_{e=2}^{floor(N/d)} floor(ek/p)
 *            + sum_{d=2}^{N} mu(d) * floor(k/p)
 *            + 1 * floor(k/p)
 *
 * Hmm, wait. The b=1 case gives d=1, e=1. floor(1*k/p) = 0. floor(0/1) = 0.
 * So the (d,e)=(1,1) term contributes mu(1)*floor(floor(k/p)/1) = 0.
 * So we DON'T need to subtract anything!
 *
 * N_N(k/p) = 1 + sum_{d=1}^{N} mu(d) * sum_{e=1}^{floor(N/d)} floor(ek/p)
 *
 * But the b=1 term (d=1, e=1) contributes floor(k/p) = 0, which is correct
 * (for b=1, the only coprime fraction is 0/1, and we counted it as the "1").
 *
 * Wait, I'm double counting. Let me restart cleanly.
 *
 * We want: N_N(k/p) = #{(a,b): 0 <= a/b <= k/p, 1 <= b <= N, gcd(a,b)=1, 0 <= a}
 *
 * = sum_{b=1}^{N} sum_{a=0}^{floor(bk/p)} [gcd(a,b)=1]
 *
 * Using Mobius: sum_{a=0}^{m} [gcd(a,b)=1] = 1_{b=1} + sum_{d|b} mu(d)*floor(m/d)
 *   (the 1_{b=1} accounts for a=0: gcd(0,b)=1 iff b=1)
 *
 * Hmm, actually sum_{a=0}^{m} [gcd(a,b)=1] = [b=1] + #{a: 1<=a<=m, gcd(a,b)=1}
 *                                            = [b=1] + sum_{d|b} mu(d)*floor(m/d)
 *
 * So: N_N(k/p) = [b=1 contributes 1] + sum_{b=1}^{N} sum_{d|b} mu(d)*floor(floor(bk/p)/d)
 *
 * = 1 + sum_{d=1}^{N} mu(d) * sum_{e=1}^{floor(N/d)} floor(ek/p)   [using b=de, floor(floor(dek/p)/d)=floor(ek/p)]
 *
 * But the b=1 term (d=1,e=1): mu(1)*floor(1*k/p)=floor(k/p)=0.
 * So the "1" comes from the [b=1] indicator, not the sum. And the sum starts fresh.
 *
 * N_N(k/p) = 1 + sum_{d=1}^{N} mu(d) * F(floor(N/d), k, p)
 *
 * where F(M, k, p) = sum_{e=1}^{M} floor(ek/p).
 *
 * F(M, k, p) is a well-known function: it equals (floor sum of an arithmetic sequence mod p).
 * F(M, k, p) = ((M * floor(Mk/p) + ...) -- there's a closed-form via the reciprocity formula.
 *
 * F(M, k, p) = sum_{e=1}^{M} floor(ek/p) = (M*k - s(k,p,M)) / p
 * where s(k,p,M) = sum_{e=1}^{M} (ek mod p) = sum of residues.
 *
 * Actually: floor(ek/p) = (ek - (ek mod p)) / p.
 * So F(M,k,p) = (k*M*(M+1)/2 - sum_{e=1}^{M} (ek mod p)) / p.
 * Wait: sum ek = k * sum e = k*M*(M+1)/2.
 * F = sum floor(ek/p) = (sum ek - sum (ek mod p)) / p = (k*M*(M+1)/2 - sum (ek mod p)) / p.
 *
 * The sum of (ek mod p) for e=1..M when gcd(k,p)=1 (always since p prime, k<p) is:
 * If M >= p: complete cycles plus remainder.
 * If M < p: it's the sum of a permutation of {k, 2k, ..., Mk} mod p,
 *   = sum of the first M elements of {k, 2k, ...} mod p.
 *   Since k is coprime to p, {ek mod p : e=1..p-1} = {1, 2, ..., p-1}.
 *   So for M = p-1: sum = p(p-1)/2.
 *   For M < p-1: sum = sum of M distinct elements from {1,...,p-1}.
 *
 * This doesn't simplify nicely. For our purposes, we can compute F(M,k,p) directly
 * in O(M) per (k, M), but we need it for many values of M = floor(N/d).
 *
 * TOTAL COMPLEXITY:
 * sum_{d=1}^{N} [mu(d)!=0] * floor(N/d) ~ N * sum_{d=1}^{N} 1/d ~ N*log(N)
 *
 * For N = 243798: ~ 243798 * 12.4 ~ 3*10^6. This is for a SINGLE k.
 * For all k=1..p-1: 243798 * 3*10^6 ~ 7.3*10^11. Too slow.
 *
 * BETTER APPROACH: precompute D_new using a different method.
 *
 * Since D_{F_p}(k/p) = N_{p-1}(k/p) + k - 1 - n'*k/p, and
 * D_new = sum_k [N_{p-1}(k/p) + k - 1 - n'*k/p]^2,
 *
 * we can compute it if we can evaluate N_{p-1}(k/p) for each k.
 *
 * The counting function N_N(x) is piecewise constant with jumps at Farey fractions.
 * Between consecutive Farey fractions a/b and c/d, N_N(x) is constant.
 *
 * A PRACTICAL APPROACH: generate F_{p-1} using the mediant algorithm (O(n) time),
 * and for each Farey fraction, update the counting function and process the new
 * fractions k/p in that interval.
 *
 * Since both F_{p-1} and {k/p} are sorted, we can merge-walk them in O(n + p) time.
 *
 * For N = 243798, n = |F_{p-1}| ~ 18 billion. This is O(18 billion) — takes ~ 60 seconds
 * at 300M ops/sec.
 *
 * Let's do this.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

static int *phi_arr = NULL;

void sieve_phi(int n) {
    phi_arr = (int *)calloc(n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i) { /* i is prime */
            for (int j = i; j <= n; j += i) {
                phi_arr[j] = phi_arr[j] / i * (i - 1);
            }
        }
    }
}

int main(void) {
    long long p = 243799;
    long long N = p - 1;

    fprintf(stderr, "Computing D_new for p = %lld, N = %lld\n", p, N);
    clock_t t0 = clock();

    /* Sieve phi */
    fprintf(stderr, "Sieving phi to %lld...\n", N);
    sieve_phi((int)N);
    clock_t t1 = clock();
    fprintf(stderr, "Sieve done: %.1f sec\n", (double)(t1-t0)/CLOCKS_PER_SEC);

    /* Compute n = |F_N| */
    long long n = 1;
    for (int i = 1; i <= N; i++) n += phi_arr[i];
    long long n_prime = n + (p - 1);
    fprintf(stderr, "|F_N| = %lld, |F_p| = %lld\n", n, n_prime);

    /* Generate F_N via mediant algorithm and merge with k/p fractions */
    /* We walk through F_N in order and process new fractions between consecutive entries */

    double D_new_sum = 0.0;
    double old_D_sq = 0.0;
    double B_raw = 0.0;
    double delta_sq = 0.0;
    long long count_new = 0;

    /* Farey mediant walk */
    int a = 0, b = 1, c = 1, d = (int)N;
    long long rank_old = 0;  /* rank in F_N (0-indexed) */

    /* Current new fraction index: next_k/p */
    int next_k = 1;

    /* Process new fractions before 0/1: none (0/1 is the first) */
    /* Process new fractions between 0/1 and next fraction */

    /* First: handle 0/1 */
    /* old_D_sq: D(0/1) = 0 - n*0 = 0 */
    old_D_sq += 0.0;
    /* delta(0/1) = 0 */

    long long progress = 0;
    long long total = n;

    while (!(a == 1 && b == 1)) {
        /* Advance to next Farey fraction */
        int k_med = ((int)N + b) / d;
        int na = k_med * c - a, nb = k_med * d - b;

        /* Before moving: process new fractions k/p in (a/b, c/d) */
        /* next_k/p is the next unprocessed new fraction */
        /* a/b < next_k/p < c/d iff a*p < next_k*b and next_k*d < c*p */
        while (next_k < p) {
            /* Check if next_k/p < c/d, i.e., next_k*d < c*p */
            if ((long long)next_k * d < (long long)c * p) {
                /* next_k/p is between a/b and c/d in F_N */
                /* rank of next_k/p in F_p (0-indexed):
                 * = N_{p-1}(next_k/p) + next_k - 1
                 * N_{p-1}(next_k/p) = rank_old + 1 (= number of F_N fracs <= next_k/p)
                 * because we're between a/b (included, rank=rank_old) and c/d (not yet)
                 */
                long long N_pm1 = rank_old + 1;  /* #{f in F_{p-1}: f <= next_k/p} */
                double kp = (double)next_k / p;
                double D_fp = (double)(N_pm1 + next_k - 1) - (double)n_prime * kp;
                D_new_sum += D_fp * D_fp;
                count_new++;
                next_k++;
            } else {
                break;
            }
        }

        /* Move to next Farey fraction c/d */
        a = c; b = d; c = na; d = nb;
        rank_old++;

        if (b > 1) {
            double f = (double)a / b;
            double D = (double)rank_old - (double)n * f;
            old_D_sq += D * D;

            long long pa_mod_b = ((long long)p * a) % b;
            double delta = (double)((long long)a - pa_mod_b) / b;
            delta_sq += delta * delta;
            B_raw += 2.0 * D * delta;
        } else {
            /* 1/1: D = (n-1) - n*1 = -1 */
            old_D_sq += 1.0;
        }

        progress++;
        if (progress % 2000000000LL == 0) {
            clock_t tc = clock();
            fprintf(stderr, "  %lld / %lld (%.1f%%), %.0f sec, D_new=%.4e, count_new=%lld\n",
                    progress, total, 100.0*progress/total,
                    (double)(tc-t0)/CLOCKS_PER_SEC, D_new_sum, count_new);
        }
    }

    /* Process any remaining new fractions after 1/1 (there shouldn't be any since p-1/p < 1/1) */
    while (next_k < p) {
        long long N_pm1 = rank_old + 1;
        double kp = (double)next_k / p;
        double D_fp = (double)(N_pm1 + next_k - 1) - (double)n_prime * kp;
        D_new_sum += D_fp * D_fp;
        count_new++;
        next_k++;
    }

    clock_t t2 = clock();
    fprintf(stderr, "Streaming done: %.1f sec, %lld old fracs, %lld new fracs\n",
            (double)(t2-t0)/CLOCKS_PER_SEC, progress, count_new);

    /* Compute A */
    double A = old_D_sq * ((double)n_prime * n_prime / ((double)n * n) - 1.0);

    /* Four-term: n'^2 * DeltaW = A - B_raw - delta_sq - D_new_sum */
    double n2_DeltaW = A - B_raw - delta_sq - D_new_sum;
    double DeltaW = n2_DeltaW / ((double)n_prime * n_prime);

    printf("p = %lld\n", p);
    printf("N = %lld\n", N);
    printf("|F_N| = %lld\n", n);
    printf("|F_p| = %lld\n", n_prime);
    printf("\n");
    printf("A (dilution)     = %.6e\n", A);
    printf("B (cross)        = %.6e\n", B_raw);
    printf("C (shift)        = %.6e\n", delta_sq);
    printf("D_new            = %.6e\n", D_new_sum);
    printf("D_new/A          = %.10f\n", D_new_sum / A);
    printf("B + C            = %.6e\n", B_raw + delta_sq);
    printf("B + C + D        = %.6e\n", B_raw + delta_sq + D_new_sum);
    printf("A - B - C - D    = %.6e\n", n2_DeltaW);
    printf("DeltaW           = %.6e\n", DeltaW);
    printf("Sign: %s\n", (n2_DeltaW < 0) ? "NEGATIVE (theorem holds)" : "POSITIVE (theorem FAILS)");

    printf("\nVerification:\n");
    printf("  sum(delta) check: C' = %.6e\n", delta_sq);
    printf("  B'/C' = %.6f\n", B_raw / delta_sq);
    printf("  new fracs processed = %lld (expected %lld)\n", count_new, p - 1);

    free(phi_arr);
    return 0;
}
