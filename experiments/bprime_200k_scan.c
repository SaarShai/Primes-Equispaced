/* Scan M=-3 primes from 200K to 250K */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX_N 250001
static int mu_arr[MAX_N], M_vals[MAX_N], phi_arr[MAX_N];
static char is_prime_arr[MAX_N];

void sieve(int n) {
    int *primes = malloc(n * sizeof(int));
    int num_primes = 0;
    memset(is_prime_arr, 1, n+1);
    is_prime_arr[0] = is_prime_arr[1] = 0;
    mu_arr[1] = 1;
    for (int i = 0; i <= n; i++) phi_arr[i] = i;
    for (int i = 2; i <= n; i++) {
        if (phi_arr[i] == i) for (int j = i; j <= n; j += i) phi_arr[j] -= phi_arr[j]/i;
        if (is_prime_arr[i]) { primes[num_primes++] = i; mu_arr[i] = -1; }
        for (int j = 0; j < num_primes && (long long)i*primes[j] <= n; j++) {
            int ip = i*primes[j];
            is_prime_arr[ip] = 0;
            if (i % primes[j] == 0) { mu_arr[ip] = 0; break; }
            else mu_arr[ip] = -mu_arr[i];
        }
    }
    M_vals[0] = 0;
    for (int i = 1; i <= n; i++) M_vals[i] = M_vals[i-1] + mu_arr[i];
    free(primes);
}

void compute_bprime(long p) {
    long N = p - 1;
    long long farey_size = 1;
    for (long k = 1; k <= N; k++) farey_size += phi_arr[k];
    double n_dbl = (double)farey_size;
    
    double B_raw = 0.0, C_raw = 0.0;
    double kB = 0.0, kC = 0.0;
    long a = 0, b = 1, c = 1, d = N;
    long long rank = 0;
    
    while (!(a == 1 && b == 1)) {
        long k = (N + b) / d;
        long na = k*c - a, nb = k*d - b;
        a = c; b = d; c = na; d = nb;
        rank++;
        if (b <= 1) continue;
        double f = (double)a / (double)b;
        double D = (double)rank - n_dbl * f;
        long long pa_mod_b = ((long long)p * (long long)a) % (long long)b;
        double delta = (double)((long long)a - pa_mod_b) / (double)b;
        
        { double y = 2.0*D*delta - kB; double t = B_raw+y; kB = (t-B_raw)-y; B_raw = t; }
        { double y = delta*delta - kC; double t = C_raw+y; kC = (t-C_raw)-y; C_raw = t; }
    }
    
    printf("p=%ld M=%d: |F|=%lld B'=%.6e C'=%.6e B'/C'=%.6f %s\n",
           p, M_vals[p], farey_size, B_raw, C_raw,
           C_raw > 0 ? B_raw/C_raw : 0.0,
           B_raw > 0 ? "POS" : "NEG!");
    fflush(stdout);
}

int main(void) {
    sieve(250000);
    printf("M=-3 primes from 200K to 250K:\n");
    time_t t0 = time(NULL);
    int count = 0;
    for (int p = 200000; p <= 250000; p++) {
        if (!is_prime_arr[p] || M_vals[p] != -3) continue;
        compute_bprime(p);
        count++;
    }
    time_t t1 = time(NULL);
    printf("\nScanned %d M=-3 primes in %ld sec\n", count, (long)(t1-t0));
    return 0;
}
