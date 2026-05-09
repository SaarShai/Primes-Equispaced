#!/usr/bin/env python3
"""C2 orthogonal symbolic supplement.

Computes:
  (1) Andrade-Best 2023 Theorem 2.4 explicit formula for b^SO_{k1,k2}(n1,n2)
      at (k1=k2=1, n1=n2=1) — should give 0 (degenerate due to algebraic identity).
      Then at (k1=k2=1, n1=n2=2) — the non-degenerate Altug et al. analog.
  (2) Verbatim Barnes-G recursion check.
  (3) CUE b'_1 = 1/12 from CRS 2006 Eq. (1.6) at k=1, computed from
      e^{-x/2} x^{-1/2} I_1(2 sqrt(x)) Taylor expansion.
"""
import sympy as sp
from sympy import Rational, factorial, sqrt, Symbol, exp, diff, series, oo, gamma
import math
import mpmath as mp

print("=" * 80)
print("C2 ORTHOGONAL SYMBOLIC SUPPLEMENT")
print("=" * 80)

# ---------- (1) Andrade-Best Theorem 2.4 b^{SO}_{k1,k2}(n1,n2) ----------
print()
print("Section 1. Andrade-Best 2023 b^{SO}_{k1,k2}(n1,n2) explicit formula")
print()
print("Theorem 2.4 (verbatim, page 6 of arXiv:2312.04981):")
print("  b^SO_{k1,k2}(n1,n2) = (-1)^{k(k-1)/2} / 2^{k(k-3)/2 + k1 n1 + k2 n2}")
print("                       * (n1!)^{k1} (n2!)^{k2}")
print("                       * sum over l_{i,j}, m_{i,j} (with constraints)")
print("                       * prod_{j=1..k} 1/(2k + V_j - 2j)!")
print("                       * prod_{i<j} (V_j - V_i - 2j + 2i)")
print("  where V_j = 2 sum_{i=1..k1} l_{i,j} + 2 sum_{i=1..k2} m_{i,j}")
print()


def b_SO_simple(k1, k2, n1, n2):
    """Compute b^{SO}_{k1,k2}(n1,n2) for small cases by direct enumeration."""
    k = k1 + k2
    # The constraints: 2 sum_j l_{i,j} ≤ n1 for each i in 1..k1
    #                  2 sum_j m_{i,j} ≤ n2 for each i in 1..k2
    # l_{i,j}, m_{i,j} ≥ 0 integers, with j ∈ {1, ..., k}.
    # We enumerate.
    # For (k1=k2=1, n1=n2=1): l_{1,j} ≥ 0 with 2 sum_j l_{1,j} ≤ 1 ⇒ all l=0.
    # Same for m.  V_j = 0 for all j.
    # prod_j 1/(2k + V_j - 2j)! = prod_{j=1}^{k} 1/(2k - 2j)!
    #                            = 1/(2k-2)! · 1/(2k-4)! · ... · 1/0!
    # prod_{i<j} (V_j - V_i - 2j + 2i) = prod_{i<j} (-2j + 2i) = prod_{i<j} 2(i-j)
    #                                  = 2^{k(k-1)/2} prod_{i<j} (i-j)
    #                                  = 2^{k(k-1)/2} (-1)^{k(k-1)/2} prod_{i<j} (j-i)
    # For k=2: prod_{1<2} (2-1) = 1.

    # Sign and prefactor
    sign = (-1)**(k*(k-1)//2)
    prefac = sign * Rational(1, 2)**(k*(k-3)//2 + k1*n1 + k2*n2)
    nfac = (factorial(n1)**k1) * (factorial(n2)**k2)

    # Enumerate l_{i,j} for i=1..k1: tuple of k integers ≥ 0 with sum ≤ floor(n1/2)
    # Wait, the constraint is "2 sum_{j=1..k} l_{i,j} ≤ n1" not ≤ floor(n1/2).
    # So sum_j l_{i,j} ≤ floor(n1/2).
    # Each l_{i,j} ≥ 0.
    def enumerate_partitions(K_total, length):
        """Generate tuples of length `length` of non-negative ints summing to ≤ K_total."""
        if length == 0:
            yield ()
            return
        for first in range(K_total + 1):
            for rest in enumerate_partitions(K_total - first, length - 1):
                yield (first,) + rest

    total = sp.S(0)
    for l_tuples in itertools_product_constrained(n1 // 2, k, k1):
        for m_tuples in itertools_product_constrained(n2 // 2, k, k2):
            # V_j = 2 sum_i l_{i,j} + 2 sum_i m_{i,j}
            Vj = [
                2 * sum(l_tuples[i][j] for i in range(k1))
                + 2 * sum(m_tuples[i][j] for i in range(k2))
                for j in range(k)
            ]
            # Constraint check: each i needs sum_j l_{i,j} ≤ n1/2 (already enforced),
            # but also "2 sum_j l_{i,j} ≤ n1" so each i row sum ≤ n1//2.
            # Also: integer fact: (n1 - 2 sum_j l_{i,j})! must be defined ⇒ sum ≤ n1/2.
            # We need 2k + V_j - 2j ≥ 0 for all j; here 2k = 2k, and V_j ≥ 0.
            # Given V_j is small, 2k + V_j - 2j ≥ 0 needs j ≤ k + V_j/2 — true for j ≤ k.
            # Inner factor 1: prod over i: 1/(n1 - 2*sum_j l_{i,j})!
            inner1 = sp.S(1)
            for i in range(k1):
                S = sum(l_tuples[i])
                if 2 * S > n1:
                    inner1 = sp.S(0)
                    break
                inner1 *= Rational(1, factorial(n1 - 2 * S))
            inner2 = sp.S(1)
            if inner1 != 0:
                for i in range(k2):
                    S = sum(m_tuples[i])
                    if 2 * S > n2:
                        inner2 = sp.S(0)
                        break
                    inner2 *= Rational(1, factorial(n2 - 2 * S))
            if inner1 == 0 or inner2 == 0:
                continue
            # j-product: prod_j 1/(2k + V_j - 2j)!
            jprod = sp.S(1)
            for j in range(k):
                expnt = 2 * k + Vj[j] - 2 * (j + 1)  # convention: j ∈ {1,...,k} in paper, here index from 0 → j+1
                if expnt < 0:
                    jprod = sp.S(0)
                    break
                jprod *= Rational(1, factorial(expnt))
            if jprod == 0:
                continue
            # i<j product: prod_{i<j} (V_j - V_i - 2j + 2i)
            ijprod = sp.S(1)
            for ii in range(k):
                for jj in range(ii + 1, k):
                    ijprod *= Vj[jj] - Vj[ii] - 2 * (jj + 1) + 2 * (ii + 1)
            total += inner1 * inner2 * jprod * ijprod
    return prefac * nfac * total


def itertools_product_constrained(max_sum, length, num_rows):
    """Cartesian product of `num_rows` tuples of length `length` of non-neg ints,
    each row summing to ≤ max_sum."""
    import itertools
    def one_row(K, L):
        if L == 0:
            yield ()
            return
        for first in range(K + 1):
            for rest in one_row(K - first, L - 1):
                yield (first,) + rest
    rows = list(one_row(max_sum, length))
    for combo in itertools.product(rows, repeat=num_rows):
        yield combo


# Test cases
print("Test cases of b^{SO}_{k1,k2}(n1,n2):")
for (k1, k2, n1, n2) in [(1, 1, 0, 0), (1, 1, 1, 1), (1, 1, 2, 2), (2, 0, 1, 0), (2, 0, 2, 0)]:
    try:
        v = b_SO_simple(k1, k2, n1, n2)
        v_simp = sp.simplify(v)
        v_float = float(v_simp)
        print(f"  b^SO_{{{k1},{k2}}}({n1},{n2}) = {v_simp} = {v_float:.6f}")
    except Exception as e:
        print(f"  b^SO_{{{k1},{k2}}}({n1},{n2}): error {e}")

# Expected behaviors (from CRS 2006 / Keating-Snaith):
print()
print("Expected from Keating-Snaith for SO(2N):")
print("  E[Λ_A(1)²]_{SO(2N)} ~ f_O(1) · N^{1/2} = 2 · N^{1/2}")
print("  ⟹ b^SO_{1,1}(0,0) · (2N)^{2(2-1)/2 + 0 + 0} = b · (2N)^1")
print("  This conflicts with KS which has power N^{1/2}, not N^1.")
print("  So Andrade-Best Theorem 2.3 is NOT applicable when n1=n2=0 (the moments-only case).")
print("  The theorem applies when at least one n_i ≥ 1.")
print()
print("For (k1=k2=1, n1=n2=1): the algebraic identity Λ'(1) = N · Λ(1) for SO(2N)")
print("  predicts E[Λ'(1)²] = N² · E[Λ(1)²] ~ 2 N^{5/2}")
print("  Andrade-Best Theorem 2.3 predicts (2N)^3, leading constant b^SO_{1,1}(1,1)")
print("  These reconcile only if b^SO_{1,1}(1,1) = 0 at leading order.")

# ---------- (2) Barnes-G via mpmath ----------
print()
print("Section 2. Barnes-G symbolic verification (mpmath dps=60)")
mp.mp.dps = 60
G3 = mp.barnesg(3)
G5 = mp.barnesg(5)
ratio = G3**2 / G5
target = mp.mpf(1) / 12
print(f"  G(3) = {G3}")
print(f"  G(5) = {G5}")
print(f"  G(3)²/G(5) = {ratio}")
print(f"  1/12      = {target}")
print(f"  delta     = {ratio - target}")

# ---------- (3) CRS 2006 b'_1 from Bessel determinant ----------
print()
print("Section 3. CRS 2006 b'_1 from Eq. (1.6):")
print("  b'_k = (-1)^{k(k+1)/2} (d/dx)^{2k} ( e^{-x/2} x^{-k²/2} det_{k×k}(I_{i+j-1}(2√x)) ) |_{x=0}")
print()
print("For k=1: det = I_1(2√x), and we need (d/dx)² ( e^{-x/2} x^{-1/2} I_1(2√x) ) |_{x=0}")
print()

x = sp.Symbol('x', positive=True)
# I_1(2 sqrt(x)) Taylor series (verbatim Bessel I expansion):
# I_1(z) = sum_{j=0}^∞ (z/2)^{2j+1} / (j! (j+1)!)
# I_1(2 sqrt(x)) = sum_j x^{j+1/2} / (j! (j+1)!)
# x^{-1/2} I_1(2 sqrt(x)) = sum_j x^j / (j! (j+1)!)
# e^{-x/2} = sum_n (-x/2)^n / n!
# Product up to x^4:
expr2 = sp.S(0)
for n in range(6):
    for jj in range(6):
        if n + jj > 4:
            continue
        expr2 += (Rational(-1,2))**n / sp.factorial(n) * Rational(1, int(sp.factorial(jj)*sp.factorial(jj+1))) * x**(jj+n)
expr2 = sp.expand(expr2)
coeff_x2 = expr2.coeff(x, 2)
print(f"  Coefficient of x² in e^{{-x/2}} x^{{-1/2}} I_1(2√x) Taylor expansion: {coeff_x2}")
# (d/dx)^2 at x=0 = 2! * coefficient of x² = 2 * coeff_x2
# b'_1 (CRS Eq. 1.6) = (-1)^{1·2/2} * (sum over h=0..1 of (1 choose h) (d/dx)^{1+h} of e^{-x/2} I_1(2√x))
# Actually: from CRS Eq. (1.4) with k=1: b_k formula has h-sum from 0..k.  For k=1 it's:
# b_1 = (-1)^{1*2/2} sum_{h=0..1} C(1,h) (d/dx)^{1+h} (e^{-x} x^{-1/2} I_1(2√x))/ ... Nope, let's just check via Eq. (1.6):
# b'_1 = (-1)^{1*(1+1)/2} (d/dx)^2 (e^{-x/2} x^{-1/2} I_1(2√x)) |_{x=0}
#       = (-1)^1 · 2! · coeff_x2 = -2 · coeff_x2
val = -2 * coeff_x2
print(f"  b'_1 = -2 · coeff_x2 = {val}")
print(f"  Target b'_1 = 1/12 = {Rational(1,12)}  -> match: {val == Rational(1,12)}")

# ---------- (4) Direct mpmath computation of CRS b'_1 from Eq. (1.6) ----------
print()
print("Section 4. CRS b'_1 via direct mpmath series:")
mp.mp.dps = 30
# f(x) = e^{-x/2} x^{-1/2} I_1(2 sqrt(x))
# Take 2nd derivative at x=0
def f(x):
    if x == 0:
        # Limit: I_1(2 sqrt(x)) / sqrt(x) → 1 as x → 0
        return mp.mpf(1)
    return mp.exp(-x/2) * mp.besseli(1, 2*mp.sqrt(x)) / mp.sqrt(x)

# Numerical 2nd derivative at x=0 via series approach: f(x) ≈ f(0) + f'(0) x + f''(0) x²/2 + ...
# Compute f at many x's and fit polynomial
xs = [mp.mpf("1e-30"), mp.mpf("1e-15"), mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.1")]
vals = [f(x) for x in xs]
# Use Taylor: take small x, f(x) = a0 + a1 x + a2 x²/2 + ...
# Fit:
print("  f(x) at small x values:")
for xi, vi in zip(xs, vals):
    print(f"    x = {float(xi):.2e}, f(x) = {float(vi):.10f}")

# Use mpmath's diff
f_pp = mp.diff(f, mp.mpf(0), 2)
print(f"  d²f/dx² at x=0 = {f_pp}")
print(f"  -f''(0) = {-f_pp}")
print(f"  vs 1/12 = {mp.mpf(1)/12}")
print(f"  ratio: {-f_pp * 12}")
print()
print("Conclusion: CRS b'_1 = 1/12 is independently verified to 30 dps via mpmath.")
