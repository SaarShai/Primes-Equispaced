#!/usr/bin/env python3
"""Cross-Selberg full reproduction with the missing log-3-axis poles.

The factor (1 - 3^{-2s})^{-1} has SIMPLE POLES at  s = i pi k / log 3,  for every k in Z.
We include the k=0 pole in the leading double-pole calculation at s=0.
For k != 0, each pole contributes:
    Res_{s = i pi k/log 3} = 1 / (2 log 3)   (residue of (1 - 3^{-2s})^{-1})
times the value of the OTHER factors at that s:
    G(s_k) * M_W(s_k) * N^{s_k}      where  G(s) = L(s, chi_3) / zeta(2s)
                                            s_k = i pi k / log 3

Hence the missing term in the explicit formula is
    Z_axis(N) := sum_{k != 0}  [1/(2 log 3)] * G(s_k) * M_W(s_k) * N^{s_k}
              = (1/log 3) Re[ sum_{k>=1} G(s_k) M_W(s_k) N^{s_k} ]   (since pairs (k, -k) conjugate)

Each term has |N^{s_k}| = 1, but |M_W(s_k)| = (1/2)|Gamma(i pi k / (2 log 3))|
which decays exponentially in |k| via Stirling for imaginary argument.
So the series is rapidly convergent.

Add this to the previous prediction and compare.
"""
import mpmath as mp
import math

mp.mp.dps = 40

log3 = mp.log(3)
c0 = -1 / (3 * log3)

def G(s):
    return mp.dirichlet(s, [0,1,-1]) / mp.zeta(2*s)

def MW(s):
    return mp.gamma(s/2) / 2

def main():
    Gprime0_val = mp.diff(G, 0)
    c1 = Gprime0_val / (2*log3) - mp.mpf(1)/3
    gamma_em = mp.euler
    const_term = c1 - c0 * gamma_em / 2

    # is_sqfree sieve
    Ns = [100, 300, 1000, 3000, 10000, 30000, 100000, 300000]
    NMAX = 9 * Ns[-1]
    print(f"# Sieving squarefree indicator up to {NMAX}...")
    is_sqfree = [True] * (NMAX + 1)
    is_sqfree[0] = False
    p = 2
    while p*p <= NMAX:
        for i in range(p*p, NMAX + 1, p*p):
            is_sqfree[i] = False
        p += 1
    print("# Done.")

    def chi3(n):
        r = n % 3
        if r == 0: return 0
        if r == 1: return 1
        return -1

    def Sum_S(N, NMAX_local):
        total = mp.mpf(0)
        invN = mp.mpf(1)/N
        for n in range(1, NMAX_local + 1):
            if not is_sqfree[n]:
                continue
            c = chi3(n)
            if c == 0:
                continue
            x = n * invN
            total += c * mp.exp(-x*x)
        return total

    # zeros of zeta
    K_zero = 30
    print(f"# Computing first {K_zero} zeros of zeta...")
    zeros = [mp.zetazero(k) for k in range(1, K_zero+1)]
    def Z_zeros(N):
        s = mp.mpc(0)
        for rho in zeros:
            term = (N ** (rho/2)) * mp.dirichlet(rho/2, [0,1,-1]) * MW(rho/2) \
                    / (2 * mp.zeta(rho, derivative=1) * (1 - 3**(-rho)))
            s += term + mp.conj(term)
        return s.real

    # log-3-axis poles
    K_axis = 100
    print(f"# Including {K_axis} log-3-axis pole pairs...")
    def Z_axis(N):
        # Sum over k = 1..K_axis (and conjugate k <-> -k)
        s = mp.mpc(0)
        pre = 1 / (2 * log3)  # residue of (1 - 3^{-2s})^{-1} at s_k
        for k in range(1, K_axis + 1):
            s_k = mp.mpc(0, mp.pi * k / log3)
            # The residue of N^s F(s) M_W(s) at s = s_k is:
            #   N^{s_k} * G(s_k) * M_W(s_k) * pre
            # plus complex conjugate from k -> -k.
            term = pre * G(s_k) * MW(s_k) * (N ** s_k)
            s += term + mp.conj(term)
        return s.real

    print()
    print("# N      S(N)         leading       Z_zeros      Z_axis      pred=lead+Z+Z_axis    R=S-pred")
    for N in Ns:
        S = Sum_S(N, min(NMAX, 9*N))
        leading = c0 * mp.log(N) + const_term
        z = Z_zeros(N)
        za = Z_axis(N)
        pred = leading + z + za
        R = S - pred
        print(f"  N={N:7d} S={float(S):+9.6f}  L={float(leading):+9.6f}  Zζ={float(z):+9.6f}  Z3={float(za):+9.6f}  Pred={float(pred):+9.6f}  R={float(R):+9.6f}")

if __name__ == "__main__":
    main()
