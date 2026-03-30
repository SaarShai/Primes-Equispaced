/*
 * b_plus_c_targeted.c
 *
 * Compute EXACT B'/C' for specific large primes where T(N) > 0.
 * Uses streaming Farey generation (mediant algorithm).
 *
 * Usage: ./b_plus_c_targeted <prime_1> <prime_2> ...
 *        or pipe primes from stdin (one per line)
 *
 * For p = 243799, F_{243798} has ~1.8*10^10 fractions.
 * At ~300M operations/sec, ~60 seconds per prime.
 *
 * Compile: cc -O3 -o b_plus_c_targeted b_plus_c_targeted.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* Compute phi(k) on the fly */
int euler_phi(int n) {
    int result = n;
    for (int p = 2; (long long)p * p <= n; p++) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}

/* Compute |F_N| = 1 + sum_{k=1}^{N} phi(k) */
long farey_size(int N) {
    long n = 1;
    for (int k = 1; k <= N; k++) n += euler_phi(k);
    return n;
}

/*
 * Compute B', C', and B'/C' for a given prime p.
 * Uses the standard mediant-based Farey generation (Stern-Brocot).
 */
void compute_for_prime(long long p) {
    int N = (int)(p - 1);

    fprintf(stderr, "p = %lld: Computing Farey size |F_%d|...\n", p, N);
    clock_t t0 = clock();

    long n = farey_size(N);

    clock_t t1 = clock();
    double size_time = (double)(t1 - t0) / CLOCKS_PER_SEC;
    fprintf(stderr, "  |F_%d| = %ld (%.1f sec)\n", N, n, size_time);
    fprintf(stderr, "  Streaming Farey sequence...\n");

    double B_raw = 0.0;
    double C_raw = 0.0;
    long count = 0;

    /* Mediant-based Farey generation */
    int a = 0, b = 1, c = 1, d = N;
    long rank = 0;

    while (!(a == 1 && b == 1)) {
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        if (b <= 1) continue;

        double f = (double)a / b;
        double D = (double)rank - (double)n * f;

        long long pa_mod_b = ((long long)p * a) % b;
        double delta = (double)(a - (int)pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;
        count++;

        if (count % 1000000000L == 0) {
            clock_t tc = clock();
            double elapsed = (double)(tc - t1) / CLOCKS_PER_SEC;
            fprintf(stderr, "  Processed %ld fractions (%.1f sec, %.1fM/s)\n",
                    count, elapsed, count / elapsed / 1e6);
        }
    }

    clock_t t2 = clock();
    double stream_time = (double)(t2 - t1) / CLOCKS_PER_SEC;

    double ratio = (C_raw > 0) ? (B_raw / C_raw) : 0.0;
    double BpC_norm = 1.0 + ratio;  /* (B'+C')/C' = 1 + B'/C' */

    fprintf(stderr, "  Done: %ld interior fractions in %.1f sec (%.1fM/s)\n",
            count, stream_time, count / stream_time / 1e6);

    printf("p=%lld  n=%ld  B'=%.6e  C'=%.6e  B'/C'=%.10f  (1+B'/C')=%.10f  B+C>0: %s\n",
           p, n, B_raw, C_raw, ratio, BpC_norm,
           (BpC_norm > 0) ? "YES" : "**NO**");
    fflush(stdout);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        for (int i = 1; i < argc; i++) {
            long long p = atoll(argv[i]);
            if (p >= 5) compute_for_prime(p);
        }
    } else {
        fprintf(stderr, "Usage: %s <prime1> [prime2] ...\n", argv[0]);
        fprintf(stderr, "Or pipe primes from stdin.\n");
        long long p;
        while (scanf("%lld", &p) == 1) {
            if (p >= 5) compute_for_prime(p);
        }
    }
    return 0;
}
