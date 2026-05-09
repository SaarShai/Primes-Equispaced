#!/usr/bin/env python3
"""Cross-Selberg full explicit-formula reproduction.

Decomposition of  F(s) := sum_n mu(n)^2 chi_3(n) / n^s = L(s,chi_3) / [zeta(2s) (1 - 3^{-2s})]

Pole / zero structure of  F(s) M_W(s) N^s :
  * s = 0: simple pole of M_W (Gaussian: M_W(s) = (1/2) Gamma(s/2), residue 1)
           PLUS simple pole of  (1 - 3^{-2s})^{-1}  with residue 1/(2 log 3)
  * s = rho/2 for rho a nontrivial zero of zeta (zeros of zeta(2s)): simple poles of 1/zeta(2s)
  * s = i pi k / log 3, k integer != 0: poles from (1 - 3^{-2s})^{-1} on imaginary axis (away from s=0).
  * s = -k (negative integers): trivial zeros of zeta(2s) at s = -k for k >= 1, contributing trivial-zero series.

Leading prediction (residue at s=0, double pole):
   Res_{s=0} = c_0 log N + (c_1 + c_0 gamma_M) + (something(N) -> 0)
where c_0 = L(0,chi_3) / zeta(0) / log(9) * 1 = (1/3) * (1/(-1/2)) * (1/log 9)
            ?  wait, (1 - 3^{-2s})^{-1} expansion:
    At s = 0: (1 - 3^{-2s})^{-1} = -1 / (2 s log 3) + 1/2 + O(s).  [Residue at s=0 is 1/(2 log 3)]
   And M_W(s) = (1/2) Gamma(s/2) has Laurent at s=0: (1/2) (2/s + (-gamma) + ...) = 1/s - gamma/2 + O(s).
        [Residue of M_W at s=0 is 1.]
   And L(s, chi_3) at s=0: L(0, chi_3) = 1/3 (Hurwitz/Bernoulli).
   And 1/zeta(2s) at s=0: zeta(2s) at s=0 is zeta(0) = -1/2, so 1/zeta(2s)|_{s=0} = -2.

So (factoring out smooth part):
   F(s) = L(s,chi_3) / zeta(2s) * (1 - 3^{-2s})^{-1}
        = G(s) * (1 - 3^{-2s})^{-1}    where G(s) := L(s,chi_3)/zeta(2s) is regular at s=0 with G(0) = (1/3)*(-2) = -2/3.

   F(s) = G(s) * (1 - 3^{-2s})^{-1}.  Near s=0:
      G(s) = -2/3 + G'(0) s + O(s^2)
      (1 - 3^{-2s})^{-1} = -1/(2 s log 3) + 1/2 - s log 3 / 6 + O(s^2)   [check expansion below]

  Thus F(s) = (-2/3) * [-1/(2 s log 3)] + lower order
             = 1/(3 s log 3) * (-1) ??

Wait let me redo expansion of (1 - 3^{-2s})^{-1} carefully.
  3^{-2s} = exp(-2s log 3) = 1 - 2 s log 3 + 2 s^2 (log 3)^2 - (4/3) s^3 (log 3)^3 + ...
  1 - 3^{-2s} = 2 s log 3 - 2 s^2 (log 3)^2 + (4/3) s^3 (log 3)^3 - ...
              = 2 s log 3 (1 - s log 3 + (2/3) s^2 (log 3)^2 - ...)
  (1 - 3^{-2s})^{-1} = 1/(2 s log 3) * (1 + s log 3 - (2/3 - 1) s^2 (log 3)^2 + ...)
                     wait: (1 - x)^{-1} = 1 + x + x^2 + ... with x = (s log 3 - (2/3) s^2 (log 3)^2 + ...)
                     = 1 + s log 3 + s^2 (log 3)^2 - (2/3) s^2 (log 3)^2 + O(s^3)
                     = 1 + s log 3 + (1/3) s^2 (log 3)^2 + O(s^3)
  So (1 - 3^{-2s})^{-1} = 1/(2 s log 3) + 1/2 + (s log 3)/6 + O(s^2).

Therefore F(s) near s=0 is:
   F(s) = G(s) * (1 - 3^{-2s})^{-1}
        = (G(0) + G'(0) s + ...) * (1/(2 s log 3) + 1/2 + (s log 3)/6 + ...)
        = G(0)/(2 s log 3)  +  G'(0)/(2 log 3) + G(0)/2  + O(s)
        = (-2/3)/(2 s log 3) + [G'(0)/(2 log 3) + (-2/3)/2] + O(s)
        = -1/(3 s log 3) + [G'(0)/(2 log 3) - 1/3] + O(s)

So  F(s) = c0/s + c1 + O(s)  with
   c0 = -1/(3 log 3)
   c1 = G'(0)/(2 log 3) - 1/3.

(Note: -1/(3 log 3) = -2/(3 * 2 log 3) = -2/(3 log 9), matching the formula in Delta_machine_multi_L.md.)

The full pole at s=0 of integrand N^s F(s) M_W(s):
  M_W(s) = 1/s - gamma_W/2 + O(s)   [where gamma_W absorbs constants for the Gaussian.]

Actually: M_W(s) = (1/2) Gamma(s/2).  Gamma(s/2) = 2/s - gamma + O(s) where gamma = Euler.
  So M_W(s) = 1/s - gamma/2 + O(s), i.e., gamma_W = gamma here? Let me be precise:
  Gamma(z) = 1/z - gamma + (gamma^2/2 + pi^2/12) z + O(z^2)  near z=0.
  M_W(s) = (1/2) Gamma(s/2)
        = (1/2) [2/s - gamma + (gamma^2/2 + pi^2/12)(s/2) + O(s^2)]
        = 1/s - gamma/2 + (gamma^2/2 + pi^2/12)(s/4) + O(s^2)

  N^s = 1 + s log N + s^2 (log N)^2 / 2 + ...

  N^s F(s) M_W(s) =  (1 + s log N + ...) * (c0/s + c1 + ...) * (1/s - gamma/2 + ...)
       The double-pole expansion:
       (c0/s + c1)(1/s - gamma/2)(1 + s log N + s^2 (log N)^2 / 2)
       = [c0/s^2 + (c1 - c0 gamma/2)/s + (- c1 gamma/2)] * (1 + s log N + s^2 (log N)^2 / 2)
       = c0/s^2 + (c0 log N)/s + c0 (log N)^2 / 2
         + (c1 - c0 gamma/2)/s + (c1 - c0 gamma/2) log N
         - c1 gamma/2 + O(s)

  Coefficient of 1/s (the residue):
     R_0(N) = c0 log N + (c1 - c0 gamma/2)
            ~ c0 log N  +  (G'(0)/(2 log 3) - 1/3 - c0 gamma/2)

So predicted leading: S(N) -> c0 * log N + const,   const = c1 - c0 gamma/2.
In multi-L doc notation, that "const" is c_1 + c_0 gamma_M with gamma_M = -gamma/2 (M_W's Laurent constant), matching.

Plug in numerical c0:
  c0 = -1/(3 log 3) = -0.30341...

Plus oscillating zero contributions:
  Sum over rho (nontriv ζ-zero) of  Res at s = rho/2 of  N^s G(s) M_W(s) / ((1 - 3^{-2s})*zeta(2s))
  = N^{rho/2} * L(rho/2, chi_3) / [(zeta(2s))'(s=rho/2) * (1 - 3^{-rho})] * M_W(rho/2)

where (zeta(2s))'(s=rho/2) = 2 zeta'(rho).

So Z(N) := Sum over zeta-zeros rho of
    N^{rho/2} * L(rho/2, chi_3) * M_W(rho/2) / [2 zeta'(rho) * (1 - 3^{-rho})]
    + complex conjugate.

Each term has |M_W(rho/2)| = (1/2)|Gamma(rho/4 + i gamma/4)|, decaying exponentially in gamma.

If I include enough zero terms, R(N) := S(N) - (c0 log N + const) should match Z(N).

This script computes both numerically.
"""
import mpmath as mp
import math

mp.mp.dps = 40

# === Constants ===
log3 = mp.log(3)
c0 = -1 / (3 * log3)

# G(s) := L(s, chi_3) / zeta(2s)
# G(0) = (1/3) / (-1/2) = -2/3
# G'(0) = ?
def G(s):
    return mp.dirichlet(s, [0,1,-1]) / mp.zeta(2*s)

def Gprime0():
    return mp.diff(G, 0)

# M_W(s) for Gaussian W(x) = exp(-x^2):  M_W(s) = (1/2) Gamma(s/2).
def MW(s):
    return mp.gamma(s/2) / 2

# zeta-zeros (Riemann)
def zeta_zero(k):
    return mp.zetazero(k)

# Cross-Selberg leading prediction: S(N) ~ c0 log N + (c1 - c0 gamma/2)
gamma_em = mp.euler  # Euler-Mascheroni

def main():
    Gprime0_val = Gprime0()
    c1 = Gprime0_val / (2*log3) - mp.mpf(1)/3
    # Constant term
    const_term = c1 - c0 * gamma_em / 2
    print(f"# c0 = {float(c0):+.8f}")
    print(f"# G'(0) = {float(Gprime0_val):+.8f}")
    print(f"# c1 = G'(0)/(2 log 3) - 1/3 = {float(c1):+.8f}")
    print(f"# Constant term = c1 - c0*gamma/2 = {float(const_term):+.8f}")
    print()

    # === Direct sum S(N) ===
    # Use sieved Mobius to compute S(N) directly
    Ns = [100, 300, 1000, 3000, 10000, 30000, 100000, 300000]
    NMAX = 8 * Ns[-1]

    # Sieve mu (only need mu^2)
    print(f"# Sieving mu^2 up to {NMAX}...")
    is_sqfree = [True] * (NMAX + 1)
    is_sqfree[0] = False
    p = 2
    while p*p <= NMAX:
        # mark multiples of p^2 as not squarefree
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

    # === Zero contribution Z(N) using K zeros ===
    K = 30
    print(f"# Computing first {K} zeros of zeta...")
    zeros = [zeta_zero(k) for k in range(1, K+1)]  # 1/2 + i*gamma_k

    def Z(N):
        """Sum over nontrivial zeros rho of zeta of:
           N^{rho/2} * L(rho/2, chi_3) * M_W(rho/2) / [2 zeta'(rho) * (1 - 3^{-rho})]
           + complex conjugate (so 2 Re of sum over upper-half zeros).
        """
        s = mp.mpc(0)
        for rho in zeros:
            term = (N ** (rho/2)) * mp.dirichlet(rho/2, [0,1,-1]) * MW(rho/2) \
                    / (2 * mp.zeta(rho, derivative=1) * (1 - 3**(-rho)))
            s += term + mp.conj(term)
        return s

    print()
    print("# N         S(N)            c0*log N + const   Z(N)               R(N)=S - leading   |R - Z|")
    for N in Ns:
        S = Sum_S(N, min(NMAX, 9*N))
        leading = c0 * mp.log(N) + const_term
        z = Z(N).real  # imaginary part is numerical noise
        R = S - leading
        mismatch = abs(R - z)
        print(f"  N={N:7d}  S={float(S):+10.6f}  lead={float(leading):+10.6f}  Z={float(z):+10.6f}  R={float(R):+10.6f}  |R-Z|={float(mismatch):.4e}")

if __name__ == "__main__":
    main()
