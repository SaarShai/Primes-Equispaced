/*
 * correction_m3_spot.c
 * Spot-check correction/C for a single prime p (given as argument).
 * Uses streaming Farey generation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_N 200001

static int phi_arr[MAX_N];

void compute_phi(int n) {
    phi_arr[1] = 1;
    for (int i = 2; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i) { /* i is prime */
            for (int j = i; j <= n; j += i)
                phi_arr[j] -= phi_arr[j] / i;
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) { fprintf(stderr, "Usage: %s <prime_p>\n", argv[0]); return 1; }
    int p = atoi(argv[1]);
    int N = p - 1;

    fprintf(stderr, "Computing phi up to %d...\n", N);
    compute_phi(N);

    /* Compute Farey size */
    long long n = 1;
    for (int k = 1; k <= N; k++) n += phi_arr[k];
    fprintf(stderr, "Farey F_%d has %lld elements\n", N, n);

    /* Stream through Farey sequence */
    double B_raw = 0.0, C_raw = 0.0;
    long long count = 0;

    int a = 0, b = 1, c = 1, d = N;
    long long rank = 0;

    while (!(a == 1 && b == 1)) {
        int k = (N + b) / d;
        int na = k * c - a, nb = k * d - b;
        a = c; b = d; c = na; d = nb;
        rank++;

        if (a == 0 || (a == 1 && b == 1)) continue;

        double f = (double)a / b;
        double D = (double)rank - (double)n * f;

        int pa_mod_b = (int)(((long long)p * a) % b);
        double delta = (double)(a - pa_mod_b) / b;

        B_raw += 2.0 * D * delta;
        C_raw += delta * delta;

        count++;
        if (count % 50000000 == 0) {
            fprintf(stderr, "  processed %lld fractions (rank=%lld)...\n", count, rank);
        }
    }

    double Term2 = (C_raw - B_raw) / 2.0;
    double ratio = Term2 / C_raw;
    double margin = 0.5 - ratio;

    printf("p=%d, n=%lld, B=%.6f, C=%.6f, Term2=%.6f, correction/C=%.6f, margin=%.6f\n",
           p, n, B_raw, C_raw, Term2, ratio, margin);

    return 0;
}
