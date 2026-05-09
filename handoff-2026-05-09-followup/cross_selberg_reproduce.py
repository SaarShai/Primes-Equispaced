#!/usr/bin/env python3
"""Cross-Selberg reproduction: compute S(N) = sum_n mu(n)^2 chi_3(n) W(n/N)
for Gaussian W(x) = e^{-x^2}, and compare to predicted leading log behaviour.

Goal: reproduce the numerical table in Delta_machine_multi_L.md §2.5 / §4 line 462.

Predicted leading: S(N) ~ c_0 * log(N) + (c_1 + c_0 * gamma_M)
where c_0 = -(2/3)/log(9) = -1/(3 log 3) ~= -0.30339.

Then compute several diagnostic functional forms of the residual to discriminate
candidate root causes of the 12-19% slope mismatch:

  R(N) := S(N) - c_0 * log(N)

If R(N) is bounded and varying (oscillation from zero contributions), the leading
slope is correct. If R(N) grows like log(log(N)), or sqrt(log N), or similar, we
have a missing log factor.
"""
import math
from math import log, sqrt
import sys

# Schwartz weight: Gaussian W(x) = exp(-x^2)
def W(x):
    return math.exp(-x*x)

# chi_3 = Kronecker symbol mod 3 (primitive odd, real)
# chi_3(0)=0, chi_3(1)=1, chi_3(2)=-1
def chi3(n):
    r = n % 3
    if r == 0:
        return 0
    if r == 1:
        return 1
    return -1

def mu_sieve(NMAX):
    """Mobius function via sieve up to NMAX inclusive."""
    mu = [1] * (NMAX + 1)
    primes = []
    is_comp = [False] * (NMAX + 1)
    for i in range(2, NMAX + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > NMAX:
                break
            is_comp[i*p] = True
            if i % p == 0:
                mu[i*p] = 0
                break
            else:
                mu[i*p] = -mu[i]
    mu[0] = 0
    mu[1] = 1
    return mu

def smoothed_sum(N, NMAX, mu):
    """S(N) = sum_n mu(n)^2 chi_3(n) W(n/N), summed for n up to NMAX (where Gaussian tail is negligible)."""
    total = 0.0
    invN = 1.0 / N
    for n in range(1, NMAX + 1):
        if mu[n] == 0:
            continue  # mu^2 = 0
        c = chi3(n)
        if c == 0:
            continue
        total += c * W(n * invN)
    return total

def main():
    # Compute up to N = 3e5 with NMAX_global = 8 * Nmax
    Ns = [100, 300, 1000, 3000, 10000, 30000, 100000, 300000]
    NMAX = 8 * Ns[-1]  # tail of Gaussian: n/N up to ~8 makes exp(-64) negligible
    print(f"# Sieving Mobius up to NMAX = {NMAX} ...", flush=True)
    mu = mu_sieve(NMAX)
    print(f"# Done sieving.", flush=True)

    c0 = -1.0 / (3.0 * log(3.0))  # predicted leading slope coefficient
    print(f"# Predicted slope c_0 = -(2/3)/log(9) = -1/(3 log 3) = {c0:.8f}", flush=True)
    print()
    print("# N, S(N), S(N)/log(N), residual R(N) = S(N) - c0*log(N), "
          "R(N)/log log N, R(N)/sqrt(log N), R(N)/(log log N / log N)")
    rows = []
    prev_S, prev_logN = None, None
    for N in Ns:
        if N > NMAX // 8:
            break
        S = smoothed_sum(N, min(NMAX, 9 * N), mu)
        logN = log(N)
        S_over_logN = S / logN
        R = S - c0 * logN
        loglog = log(log(N))
        sqrt_logN = sqrt(logN)
        ratio_loglog_logN = (loglog / logN) if logN > 0 else 0
        rows.append((N, S, S_over_logN, R))
        print(f"  N={N:7d}  S(N)={S:+9.6f}  S/log N={S_over_logN:+8.5f}  "
              f"R={R:+9.6f}  R/log log N={R/loglog:+8.5f}  R/sqrt(log N)={R/sqrt_logN:+8.5f}")

    # Slope estimates
    print()
    print("# Pairwise slope (S(N2)-S(N1))/(log N2 - log N1)")
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            N1, S1, _, _ = rows[i]
            N2, S2, _, _ = rows[j]
            slope = (S2 - S1) / (log(N2) - log(N1))
            print(f"  ({N1:>6d}, {N2:>6d}): slope = {slope:+8.5f}, "
                  f"vs predicted {c0:+.5f}, "
                  f"ratio = {slope/c0:.4f}, "
                  f"deviation = {100*(slope - c0)/c0:+.2f}%")

    # Check whether the residual R(N) tracks a slowly-growing function:
    # candidate 1 (constant offset): R(N) approx const
    # candidate 2 (log log shift):    R(N) approx a + b * log log N
    # candidate 3 (1/log N decay):    R(N) approx a + b / log N
    # Linear regression log N -> R, log log N -> R
    if len(rows) >= 4:
        import statistics
        Ns_ = [r[0] for r in rows]
        Rs_ = [r[3] for r in rows]
        # Variance of R
        meanR = sum(Rs_)/len(Rs_)
        varR = sum((r-meanR)**2 for r in Rs_)/(len(Rs_)-1)
        print()
        print(f"# Mean R = {meanR:+.5f}, std R = {sqrt(varR):.5f}")
        # candidate 2: R = a + b log log N
        xs = [log(log(N)) for N in Ns_]
        n = len(xs); xb = sum(xs)/n; yb = meanR
        Sxx = sum((x-xb)**2 for x in xs)
        Sxy = sum((x-xb)*(y-yb) for x,y in zip(xs, Rs_))
        b = Sxy/Sxx; a = yb - b*xb
        print(f"#   Fit R ~ a + b log log N : a = {a:+.5f}, b = {b:+.5f}")
        residuals = [r - (a + b*x) for r,x in zip(Rs_, xs)]
        print(f"#   Residual std after fit : {math.sqrt(sum(r*r for r in residuals)/(n-2)):.5f}")

if __name__ == "__main__":
    main()
