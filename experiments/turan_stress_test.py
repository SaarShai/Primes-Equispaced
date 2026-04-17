#!/usr/bin/env python3
from mpmath import mp

mp.dps = 50


def mobius(n):
    """
    Compute the Möbius function mu(n) by trial division.
    mu(n) = 0 if n has a squared prime factor.
    Otherwise mu(n) = (-1)^(number of distinct prime factors).
    """
    if n == 1:
        return mp.mpf(1)

    x = n
    num_prime_factors = 0
    p = 2

    while p * p <= x:
        if x % p == 0:
            num_prime_factors += 1
            x //= p
            if x % p == 0:
                return mp.mpf(0)
            while x % p == 0:
                return mp.mpf(0)
        p = 3 if p == 2 else p + 2

    if x > 1:
        num_prime_factors += 1

    return mp.mpf(-1 if num_prime_factors % 2 else 1)


def precompute_mobius(max_k):
    return {k: mobius(k) for k in range(1, max_k + 1)}


def c_k(s, K, mu_cache):
    total = mp.mpc(0)
    for k in range(2, K + 1):
        mu_k = mu_cache[k]
        if mu_k != 0:
            total += mu_k * mp.power(k, -s)
    return total


def mean(values):
    n = len(values)
    return sum(values) / n


def stddev(values):
    n = len(values)
    if n == 0:
        return mp.mpf(0)
    m = mean(values)
    return mp.sqrt(sum((v - m) ** 2 for v in values) / n)


def mpfmt(x, digits=20):
    return mp.nstr(x, digits)


def main():
    ks_main = [10, 20, 50]
    ks_table = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
    max_k = max(max(ks_main), max(ks_table))

    mu_cache = precompute_mobius(max_k)

    print("============================================================")
    print("Turán non-vanishing theorem numerical verification")
    print("mp.dps =", mp.dps)
    print("============================================================")
    print()

    print("SECTION 0. Möbius sanity check via trial factorization")
    for k in range(2, 16):
        print(f"mu({k:2d}) = {int(mu_cache[k])}")
    print()

    print("SECTION 0b. Cross-check: c_2(s) = -2^{-s}")
    rho1 = mp.zetazero(1)  # returns 0.5 + i*gamma_1
    gamma1 = rho1.imag      # extract gamma_1 (real)
    s1 = mp.mpf("0.5") + mp.j * gamma1  # = rho1
    c2_rho1 = c_k(s1, 2, mu_cache)
    abs_c2_rho1 = abs(c2_rho1)
    expected = mp.mpf(1) / mp.sqrt(2)
    print(f"gamma_1 = {mpfmt(gamma1, 25)}")
    print(f"|c_2(1/2 + i*gamma_1)| = {mpfmt(abs_c2_rho1, 25)}")
    print(f"1/sqrt(2)              = {mpfmt(expected, 25)}")
    print(f"difference             = {mpfmt(abs(abs_c2_rho1 - expected), 25)}")
    print()

    print("SECTION 1. First 100 nontrivial zeta zeros")
    zeros = [mp.zetazero(j).imag for j in range(1, 101)]  # extract gamma (real)
    for K in ks_main:
        abs_vals = []
        tiny_js = []
        for j, gamma_j in enumerate(zeros, start=1):
            s = mp.mpf("0.5") + mp.j * gamma_j  # s = 1/2 + i*gamma_j = rho_j
            val = c_k(s, K, mu_cache)
            aval = abs(val)
            abs_vals.append(aval)
            if aval < mp.mpf("1e-10"):
                tiny_js.append(j)

        min_val = min(abs_vals)
        min_j = abs_vals.index(min_val) + 1
        mean_val = mean(abs_vals)
        std_val = stddev(abs_vals)

        print(f"--- K = {K} ---")
        print(f"min_j |c_K(rho_j)| = {mpfmt(min_val, 20)} at j = {min_j}")
        print(f"mean |c_K(rho_j)|  = {mpfmt(mean_val, 20)}")
        print(f"std  |c_K(rho_j)|  = {mpfmt(std_val, 20)}")
        if tiny_js:
            print(f"any |c_K| < 1e-10? yes, at j = {tiny_js}")
        else:
            print("any |c_K| < 1e-10? no")
        print()

    print("SECTION 2. 500 evenly spaced t in [0, 5000]")
    t_values = [mp.mpf(5000) * i / 499 for i in range(500)]
    for K in ks_main:
        min_abs = None
        min_t = None
        for t in t_values:
            s = mp.mpf("0.5") + mp.j * t
            aval = abs(c_k(s, K, mu_cache))
            if min_abs is None or aval < min_abs:
                min_abs = aval
                min_t = t
        print(f"--- K = {K} ---")
        print(f"global min over 500 sampled t values: {mpfmt(min_abs, 20)}")
        print(f"attained at t = {mpfmt(min_t, 20)}")
        print()

    print("SECTION 3. |c_K(rho_1)| for increasing K")
    print(f"{'K':>8}  {'|c_K(rho_1)|':>25}  {'|c_K(rho_1)| / log(K)':>28}")
    print("-" * 66)
    for K in ks_table:
        val = abs(c_k(s1, K, mu_cache))
        ratio = val / mp.log(K)
        print(f"{K:8d}  {mpfmt(val, 18):>25}  {mpfmt(ratio, 18):>28}")
    print()

    print("SECTION 4. Summary")
    print("1. Möbius values were computed from scratch by trial factorization.")
    print("2. The cross-check c_2(s) = -2^{-s} matches |c_2(1/2 + i*gamma_1)| = 1/sqrt(2).")
    print("3. For K = 10, 20, 50 the script reports the first-100-zero statistics, including")
    print("   the minimum, mean, standard deviation, and whether any values fall below 1e-10.")
    print("4. For K = 10, 20, 50 the script also reports the minimum over 500 sampled points on")
    print("   the line Re(s) = 1/2 for t in [0, 5000].")
    print("5. The K-table for |c_K(rho_1)| is printed with the normalization by log(K).")
    print("6. All computations use mpmath at 50-digit precision.")
    print("============================================================")


if __name__ == "__main__":
    main()
