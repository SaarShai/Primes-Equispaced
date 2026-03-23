/*
 * verify_composites.c
 * Count composites N <= MAX where Delta_W(N) > 0 and M(N) < 0.
 * Uses Farey next-term generator for speed.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX 50001

static int mu[MAX], M_val[MAX], is_prime_arr[MAX];

void sieve(void) {
    // Möbius sieve
    memset(mu, 0, sizeof(mu));
    mu[1] = 1;
    for (int i = 1; i < MAX; i++)
        for (int j = 2*i; j < MAX; j += i)
            mu[j] -= mu[i];

    // Mertens function
    M_val[0] = 0;
    for (int i = 1; i < MAX; i++)
        M_val[i] = M_val[i-1] + mu[i];

    // Prime sieve
    memset(is_prime_arr, 1, sizeof(is_prime_arr));
    is_prime_arr[0] = is_prime_arr[1] = 0;
    for (int i = 2; i*i < MAX; i++)
        if (is_prime_arr[i])
            for (int j = i*i; j < MAX; j += i)
                is_prime_arr[j] = 0;
}

/* Compute wobble W(N) using Farey next-term mediant algorithm */
double compute_wobble(int N) {
    /* Generate Farey sequence F_N using next-term formula */
    /* Count size first */
    long long n = 0;
    int a = 0, b = 1, c = 1, d = N;
    while (a <= N) {
        n++;
        int k = (N + b) / d;
        int a2 = k*c - a;
        int b2 = k*d - b;
        a = c; b = d; c = a2; d = b2;
    }

    /* Now compute W(N) */
    a = 0; b = 1; c = 1; d = N;
    double W = 0.0;
    long long j = 0;
    while (a <= N) {
        double f = (double)a / (double)b;
        double ideal = (double)j / (double)n;
        double diff = f - ideal;
        W += diff * diff;
        j++;
        int k = (N + b) / d;
        int a2 = k*c - a;
        int b2 = k*d - b;
        a = c; b = d; c = a2; d = b2;
    }
    return W;
}

int main(void) {
    sieve();

    int composite_count = 0;
    int counterexamples = 0;

    time_t start = time(NULL);

    for (int N = 4; N < MAX; N++) {
        if (is_prime_arr[N]) continue;

        double W_N = compute_wobble(N);
        double W_Nm1 = compute_wobble(N-1);
        double delta_W = W_Nm1 - W_N;

        composite_count++;
        if (delta_W > 0 && M_val[N] < 0) {
            counterexamples++;
        }

        if (composite_count % 5000 == 0) {
            fprintf(stderr, "  N=%d  [%d composites, %d CE]  %lds\n",
                    N, composite_count, counterexamples,
                    time(NULL) - start);
        }
    }

    printf("Composites 4..%d: %d composites, %d with DeltaW>0 and M<0\n",
           MAX-1, composite_count, counterexamples);

    return 0;
}
