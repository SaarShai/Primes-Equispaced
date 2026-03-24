/*
 * certify_92173.c
 * ================
 * Certify ΔW(92173) > 0 using EXACT rational arithmetic (GMP).
 *
 * Strategy: Compute W(p-1) and W(p) exactly using streaming Farey
 * generation (O(1) memory) with GMP rationals for accumulation.
 *
 * W(N) = Σ (f_j - j/n)² = Σ f_j² - (2/n) Σ j·f_j + (1/n²) Σ j²
 *       = S2 - 2·R/n + n(n-1)(2n-1)/(6n²)
 *
 * where S2 = Σ f_j², R = Σ j·f_j, and Σ j² = n(n-1)(2n-1)/6.
 *
 * We accumulate S2 and R as exact GMP rationals while streaming
 * through the Farey sequence using the mediant/next-term algorithm.
 *
 * Compile: cc -O3 -o certify_92173 certify_92173.c -lgmp
 * Run:     ./certify_92173
 *
 * Expected runtime: ~5-15 minutes (2.58 billion Farey fractions for F_{92172})
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h>

/*
 * Farey next-term algorithm:
 * Given consecutive terms a/b and c/d in F_N,
 * the next term is (k*c - a)/(k*d - b) where k = floor((N + b) / d).
 */

/* Compute W(N) exactly using streaming Farey generation */
void compute_W(unsigned long N, mpq_t W_out) {
    /* We need: S2 = Σ f_j² and R = Σ j * f_j */
    mpq_t S2, R, term, frac;
    mpq_init(S2); mpq_init(R); mpq_init(term); mpq_init(frac);
    mpq_set_ui(S2, 0, 1);
    mpq_set_ui(R, 0, 1);

    /* Farey sequence starts: 0/1, 1/N, ... */
    unsigned long a = 0, b = 1, c = 1, d = N;
    unsigned long long j = 0;
    unsigned long long n = 0; /* will count total */

    /* First term: f = 0/1, j = 0 */
    /* S2 += 0, R += 0 */
    n = 1;

    /* Count total Farey fractions first for the normalization */
    /* Actually we need n = |F_N| which we can compute from Euler totient */
    /* But for streaming we'll just count as we go, then compute W at the end */
    /* Problem: we need n in the formula W = S2 - 2R/n + J(n) */
    /* Solution: accumulate S2 and R, count n, then compute W at the end */

    /* Generate all Farey fractions */
    unsigned long long report_interval = 100000000ULL; /* report every 100M */
    time_t start = time(NULL);

    while (c <= N) {
        unsigned long k = (N + b) / d;
        unsigned long na = c, nb = d;
        unsigned long nc = k * c - a, nd = k * d - b;
        a = na; b = nb; c = nc; d = nd;

        j = n; /* 0-indexed rank */
        n++;

        /* f = a/b */
        /* S2 += (a/b)^2 */
        mpq_set_ui(frac, a, b);
        mpq_canonicalize(frac);
        mpq_mul(term, frac, frac); /* term = (a/b)^2 */
        mpq_add(S2, S2, term);

        /* R += j * (a/b) */
        mpq_set_ui(term, (unsigned long)(j & 0xFFFFFFFF), 1);
        if (j > 0xFFFFFFFF) {
            /* Handle large j: j = hi * 2^32 + lo */
            mpz_t big_j;
            mpz_init(big_j);
            mpz_set_ui(big_j, (unsigned long)(j >> 32));
            mpz_mul_2exp(big_j, big_j, 32);
            mpz_add_ui(big_j, big_j, (unsigned long)(j & 0xFFFFFFFF));
            mpq_set_z(term, big_j);
            mpz_clear(big_j);
        }
        mpq_mul(term, term, frac); /* term = j * (a/b) */
        mpq_add(R, R, term);

        if (n % report_interval == 0) {
            time_t now = time(NULL);
            double elapsed = difftime(now, start);
            double rate = n / elapsed;
            fprintf(stderr, "  n=%llu (%.1f%%), %.0f fracs/sec, ~%.0fs remaining\n",
                    n, 100.0 * n / (3.0 * N * N / 9.8696), rate,
                    (3.0 * N * N / 9.8696 - n) / rate);
        }
    }

    fprintf(stderr, "  Total |F_%lu| = %llu\n", N, n);

    /* W(N) = S2 - 2*R/n + n(n-1)(2n-1)/(6n^2) */
    /* = S2 - 2*R/n + (n-1)(2n-1)/(6n) */

    mpq_t W, two_R_over_n, J;
    mpq_init(W); mpq_init(two_R_over_n); mpq_init(J);

    /* 2*R/n */
    mpq_set(two_R_over_n, R);
    mpq_mul_2exp(two_R_over_n, two_R_over_n, 1); /* 2*R */
    {
        mpz_t big_n;
        mpz_init(big_n);
        mpz_set_ui(big_n, (unsigned long)(n >> 32));
        mpz_mul_2exp(big_n, big_n, 32);
        mpz_add_ui(big_n, big_n, (unsigned long)(n & 0xFFFFFFFF));
        mpq_t n_q;
        mpq_init(n_q);
        mpq_set_z(n_q, big_n);
        mpq_div(two_R_over_n, two_R_over_n, n_q);
        mpq_clear(n_q);
        mpz_clear(big_n);
    }

    /* J = (n-1)(2n-1)/(6n) */
    {
        mpz_t nm1, twonm1, num, den, big_n;
        mpz_init(nm1); mpz_init(twonm1); mpz_init(num); mpz_init(den); mpz_init(big_n);

        mpz_set_ui(big_n, (unsigned long)(n >> 32));
        mpz_mul_2exp(big_n, big_n, 32);
        mpz_add_ui(big_n, big_n, (unsigned long)(n & 0xFFFFFFFF));

        mpz_sub_ui(nm1, big_n, 1); /* n-1 */
        mpz_mul_ui(twonm1, big_n, 2);
        mpz_sub_ui(twonm1, twonm1, 1); /* 2n-1 */
        mpz_mul(num, nm1, twonm1); /* (n-1)(2n-1) */
        mpz_mul_ui(den, big_n, 6); /* 6n */
        mpq_set_num(J, num);
        mpq_set_den(J, den);
        mpq_canonicalize(J);

        mpz_clear(nm1); mpz_clear(twonm1); mpz_clear(num); mpz_clear(den); mpz_clear(big_n);
    }

    /* W = S2 - 2R/n + J */
    mpq_sub(W, S2, two_R_over_n);
    mpq_add(W, W, J);

    mpq_set(W_out, W);

    mpq_clear(S2); mpq_clear(R); mpq_clear(term); mpq_clear(frac);
    mpq_clear(W); mpq_clear(two_R_over_n); mpq_clear(J);
}

int main(void) {
    unsigned long p = 92173;

    printf("Certifying DeltaW(%lu) with exact rational arithmetic (GMP)\n", p);
    printf("================================================================\n\n");

    mpq_t W_prev, W_curr, delta;
    mpq_init(W_prev); mpq_init(W_curr); mpq_init(delta);

    /* First: small test to verify correctness */
    printf("Verification test: p=11\n");
    {
        mpq_t W10, W11, d11;
        mpq_init(W10); mpq_init(W11); mpq_init(d11);
        compute_W(10, W10);
        compute_W(11, W11);
        mpq_sub(d11, W10, W11);
        printf("  W(10) = "); mpq_out_str(stdout, 10, W10); printf("\n");
        printf("  W(11) = "); mpq_out_str(stdout, 10, W11); printf("\n");
        printf("  DeltaW(11) = "); mpq_out_str(stdout, 10, d11); printf("\n");
        printf("  DeltaW(11) = %.10e\n", mpq_get_d(d11));
        printf("  Expected:    -1.224873e-03\n");
        int sign = mpq_sgn(d11);
        printf("  Sign: %s\n\n", sign > 0 ? "POSITIVE" : sign < 0 ? "NEGATIVE" : "ZERO");
        mpq_clear(W10); mpq_clear(W11); mpq_clear(d11);
    }

    /* Now the main event */
    printf("Computing W(%lu) [= W(p-1)]...\n", p - 1);
    time_t t0 = time(NULL);
    compute_W(p - 1, W_prev);
    time_t t1 = time(NULL);
    printf("  Done in %.0f seconds.\n\n", difftime(t1, t0));

    printf("Computing W(%lu) [= W(p)]...\n", p);
    compute_W(p, W_curr);
    time_t t2 = time(NULL);
    printf("  Done in %.0f seconds.\n\n", difftime(t2, t1));

    /* DeltaW = W(p-1) - W(p) */
    mpq_sub(delta, W_prev, W_curr);

    printf("================================================================\n");
    printf("RESULT: DeltaW(%lu)\n", p);
    printf("================================================================\n");
    int sign = mpq_sgn(delta);
    printf("  Sign: %s\n", sign > 0 ? "POSITIVE (counterexample CERTIFIED!)" :
                           sign < 0 ? "NEGATIVE (not a counterexample)" :
                                      "ZERO");
    printf("  Approximate value: %.15e\n", mpq_get_d(delta));
    printf("  M(%lu) = -2 (precomputed)\n", p);

    if (sign > 0) {
        printf("\n  *** CERTIFIED: DeltaW(92173) > 0 with M(92173) = -2 ***\n");
        printf("  *** This is a proved counterexample to the Farey-Mertens  ***\n");
        printf("  *** sign correlation conjecture, certified by exact       ***\n");
        printf("  *** rational arithmetic.                                  ***\n");
    }

    printf("\n  Total time: %.0f seconds.\n", difftime(t2, t0));

    mpq_clear(W_prev); mpq_clear(W_curr); mpq_clear(delta);
    return 0;
}
