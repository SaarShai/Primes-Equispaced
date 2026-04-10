#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 100001

static int mu_arr[MAX_N];
static int M_vals[MAX_N];

void sieve(int n) {
    int *primes = malloc(n * sizeof(int));
    int *is_composite = calloc(n + 1, sizeof(int));
    int num_primes = 0;
    mu_arr[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) { primes[num_primes++] = i; mu_arr[i] = -1; }
        for (int j = 0; j < num_primes && (long long)i * primes[j] <= n; j++) {
            int ip = i * primes[j];
            is_composite[ip] = 1;
            if (i % primes[j] == 0) { mu_arr[ip] = 0; break; }
            else mu_arr[ip] = -mu_arr[i];
        }
    }
    M_vals[0] = 0;
    for (int i = 1; i <= n; i++) M_vals[i] = M_vals[i-1] + mu_arr[i];
    free(primes); free(is_composite);
}

int main() {
    sieve(100000);
    int count = 0;
    for (int p = 2; p <= 100000; p++) {
        int is_prime = 1;
        if (p > 2 && p % 2 == 0) continue;
        if (p > 2) for (int q = 3; (long long)q*q <= p; q += 2) if (p % q == 0) { is_prime = 0; break; }
        if (!is_prime) continue;
        if (M_vals[p] == -3) {
            count++;
            if (p <= 50000)
                printf("p=%d M(p)=%d\n", p, M_vals[p]);
        }
    }
    printf("\nTotal M(p)=-3 primes up to 50000: counted above\n");
    printf("Total M(p)=-3 primes up to 100000: %d\n", count);
    return 0;
}
