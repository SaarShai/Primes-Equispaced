#!/usr/bin/env python3
"""
Compute S(p) = sum_{b=2}^{p-1} [T_b(p) - E[T_b]] / b^2
for M=-3 primes, using exact Fraction arithmetic.

From SIGNED_FLUCTUATION_PROOF.md:
  [T_b(p) - E[T_b]] / b^2 = sum_{d|b} mu(d) * s(p, b/d)

where s(h,k) is the Dedekind sum.

Also compute:
  correction = (C' - B')/2
  sum_R_delta = -(B' + C')/2

And verify: correction < 0 for all p >= 43 with M(p) = -3.

APPROACH: Two independent computations.
1) Direct: compute B', C' from Farey sequence
2) Dedekind: compute S(p) from Dedekind sums

Then verify the relationship between S(p) and correction.
"""

from fractions import Fraction
from math import gcd
import sys

def mobius(n):
    if n == 1: return 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors.append(temp)
    return (-1) ** len(factors)

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def dedekind_sum(h, k):
    """Exact Dedekind sum s(h,k) using Fraction arithmetic."""
    if k <= 1: return Fraction(0)
    s = Fraction(0)
    for r in range(1, k):
        # ((r/k)) = r/k - 1/2 (since r/k is never integer for 0 < r < k)
        # ((hr/k)): hr mod k / k - 1/2
        hr_mod_k = (h * r) % k
        if hr_mod_k == 0:
            saw2 = Fraction(0)
        else:
            saw2 = Fraction(hr_mod_k, k) - Fraction(1, 2)
        saw1 = Fraction(r, k) - Fraction(1, 2)
        s += saw1 * saw2
    return s

def divisors(n):
    divs = []
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            divs.append(d)
            if d != n // d:
                divs.append(n // d)
    return sorted(divs)

def compute_Sp_dedekind(p):
    """Compute S(p) via Dedekind sums: S(p) = sum_{b=2}^{p-1} sum_{d|b} mu(d)*s(p, b/d)."""
    N = p - 1
    S = Fraction(0)
    for b in range(2, N + 1):
        for d in divisors(b):
            mu_d = mobius(d)
            if mu_d == 0: continue
            m = b // d
            S += mu_d * dedekind_sum(p, m)
    return S

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def compute_direct(p):
    """Compute B', C', correction directly from Farey sequence with exact arithmetic."""
    N = p - 1
    F = farey_sequence(N)
    n = len(F)

    B_prime = Fraction(0)
    C_prime = Fraction(0)
    sum_f_delta = Fraction(0)  # sum f*delta for interior fractions

    for j, f in enumerate(F):
        a = f.numerator
        b = f.denominator
        if b <= 1: continue  # skip endpoints

        D_j = Fraction(j) - Fraction(n) * f
        delta = Fraction(a - (p * a % b), b)

        B_prime += D_j * delta
        C_prime += delta * delta
        sum_f_delta += f * delta

    B_prime *= 2  # B' = 2 * sum D*delta

    # Identities to verify:
    # sum_f_delta should equal C'/2 (permutation identity)
    # sum_R_delta = -(B' + C')/2
    # correction = sum_R_delta - M(N)*C'/2 = (C' - B')/2

    M_N = mertens(N)
    sum_R_delta = -(B_prime + C_prime) / 2
    correction = sum_R_delta - M_N * C_prime / 2
    # Alternatively: correction = (C' - B')/2  (let's verify)
    correction_alt = (C_prime - B_prime) / 2
    # Verify: correction_alt = sum_R_delta - M_N*C'/2
    # = -(B'+C')/2 - M_N*C'/2 = -(B' + C'*(1+M_N))/2
    # For M_N = -2: = -(B' - C')/2 = (C' - B')/2 ✓

    return {
        'p': p, 'N': N, 'n': n,
        'M_N': M_N, 'M_p': mertens(p),
        'B_prime': B_prime, 'C_prime': C_prime,
        'sum_f_delta': sum_f_delta,
        'sum_R_delta': sum_R_delta,
        'correction': correction,
        'correction_alt': correction_alt,
        'B_over_C': float(B_prime / C_prime) if C_prime else None,
        'corr_over_C': float(correction / C_prime) if C_prime else None,
    }

def compute_Tb_direct(p, b):
    """Compute T_b(p) = sum_{a coprime to b} a * (pa mod b), exact."""
    T = Fraction(0)
    for a in range(1, b):
        if gcd(a, b) == 1:
            T += a * ((p * a) % b)
    return T

def compute_Sp_direct(p):
    """Compute S(p) directly from T_b definition."""
    N = p - 1
    S = Fraction(0)
    for b in range(2, N + 1):
        T_b = compute_Tb_direct(p, b)
        phi_b = sum(1 for a in range(1, b) if gcd(a, b) == 1)
        E_Tb = Fraction(b * b * phi_b, 4)
        S += (T_b - E_Tb) / Fraction(b * b)
    return S

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0: return False
        d += 6
    return True

# Find M=-3 primes
print("=" * 80)
print("CORRECTION SIGN ANALYSIS FOR M(p) = -3 PRIMES")
print("=" * 80)

# Collect M=-3 primes up to 500
m3_primes = []
for p in range(2, 501):
    if is_prime(p) and mertens(p) == -3:
        m3_primes.append(p)

print(f"\nM(p)=-3 primes up to 500: {m3_primes}")
print(f"Count: {len(m3_primes)}")

print("\n" + "=" * 80)
print("PART 1: Direct computation of B', C', correction")
print("=" * 80)
print(f"{'p':>5} {'M(N)':>5} {'B/C':>10} {'corr/C':>10} {'corr<0?':>8} {'f*delta=C/2?':>12}")
print("-" * 56)

results = []
for p in m3_primes:
    if p > 200:  # limit for exact computation speed
        break
    r = compute_direct(p)
    results.append(r)

    f_delta_check = "YES" if r['sum_f_delta'] == r['C_prime'] / 2 else "NO"
    corr_neg = "YES" if r['correction'] < 0 else "NO"
    print(f"{p:5d} {r['M_N']:5d} {r['B_over_C']:10.4f} {r['corr_over_C']:10.4f} {corr_neg:>8} {f_delta_check:>12}")

    # Verify correction and correction_alt agree
    assert r['correction'] == r['correction_alt'], f"Correction formulas disagree at p={p}!"

print("\n" + "=" * 80)
print("PART 2: S(p) via Dedekind sums vs direct T_b computation")
print("=" * 80)
print(f"{'p':>5} {'S_ded':>14} {'S_dir':>14} {'match':>6} {'S<0?':>5} {'S/p^2':>12}")
print("-" * 56)

for p in m3_primes:
    if p > 120:  # Dedekind computation is O(p^3), limit
        break
    S_ded = compute_Sp_dedekind(p)
    S_dir = compute_Sp_direct(p)
    match = "YES" if S_ded == S_dir else "NO"
    neg = "YES" if S_ded < 0 else "NO"
    print(f"{p:5d} {float(S_ded):14.4f} {float(S_dir):14.4f} {match:>6} {neg:>5} {float(S_ded / (p*p)):12.6f}")

print("\n" + "=" * 80)
print("PART 3: Relationship between S(p) and correction")
print("=" * 80)
print("""
From the signed fluctuation framework:
  S(p) = sum_{b=2}^{N} [T_b - E[T_b]] / b^2

From the four-term decomposition:
  correction = (C' - B') / 2
  sum(R*delta) = -(B' + C') / 2

The correction measures how much sum(R*delta) deviates from M(N)*C'/2.
S(p) measures how much the per-denominator correlations deviate from their expectation.

These are RELATED but not identical:
- S(p) involves T_b (coprime sums over each denominator) normalized by b^2
- correction involves the Farey-level cross term sum(R*delta)

Let's compute both and find the exact relationship.
""")

for p in m3_primes:
    if p > 120:
        break
    r = compute_direct(p)
    S = compute_Sp_direct(p)

    # The connection: sum_{b=2}^{N} deficit_b / b^2 controls C'
    # And sum_{b=2}^{N} [T_b - E[T_b]] / b^2 = S(p)
    #
    # From the Dedekind connection: [T_b - E[T_b]]/b^2 = sum_{d|b} mu(d)*s(p, b/d)
    #
    # The correction = (C' - B')/2
    # B' = 2*sum D*delta, C' = sum delta^2
    #
    # Each delta(a/b) = (a - pa mod b)/b depends on the same permutation sigma_p
    # that defines T_b.

    print(f"p = {p}:")
    print(f"  S(p) = {float(S):.6f}")
    print(f"  S(p)/p^2 = {float(S/(p*p)):.6f}")
    print(f"  correction = {float(r['correction']):.6f}")
    print(f"  correction/C' = {float(r['correction']/r['C_prime']):.6f}")
    print(f"  B'/C' = {float(r['B_prime']/r['C_prime']):.6f}")
    print()

print("\n" + "=" * 80)
print("PART 4: The NON-CIRCULAR proof path")
print("=" * 80)
print("""
KEY INSIGHT: We need to prove correction < 0 for p >= 43 with M(p) = -3.

correction = (C' - B') / 2

This is negative iff B' > C'.

From B' = -(1 + M(N))*C' - 2*correction, for M(N) = -2:
  B' = C' - 2*correction

So correction = (C' - B')/2 is just the definition. CIRCULAR.

NON-CIRCULAR APPROACH: Express B' directly.
  B' = 2*sum D*delta

The sum D*delta decomposes over denominators:
  sum D*delta = sum_{b=2}^{N} sum_{a coprime b} D(a/b) * delta(a/b) / 1

where D(a/b) = rank(a/b) - n*(a/b) and delta(a/b) = (a - pa mod b)/b.

The linear regression decomposition gives:
  B' = alpha * C' + 2 * sum D_err * delta

where alpha = Cov(D,f)/Var(f) > 0 for N >= 7.

So: correction = (C' - B')/2 = (1 - alpha)*C'/2 - sum D_err*delta

For correction < 0 we need:
  (1 - alpha)*C'/2 < sum D_err * delta  ... but D_err*delta can be either sign

BETTER: correction < 0 iff B' > C' iff alpha*C' + 2*sum(D_err*delta) > C'
  iff (alpha - 1)*C' > -2*sum(D_err*delta)
  iff sum(D_err*delta) > (1 - alpha)*C'/2

For alpha > 1: the left side just needs to be > (1-alpha)*C'/2 < 0, which holds
whenever sum(D_err*delta) >= 0 or is not too negative.

For alpha < 1: we need sum(D_err*delta) > (1-alpha)*C'/2 > 0.

Let's compute alpha for M=-3 primes.
""")

print(f"{'p':>5} {'alpha':>10} {'alpha>1?':>8} {'sum_Derr_delta':>16} {'(1-a)C/2':>12} {'corr<0?':>8}")
print("-" * 60)

for p in m3_primes:
    if p > 200:
        break
    N = p - 1
    F = farey_sequence(N)
    n = len(F)

    # Compute D, f, delta
    D_list = []
    f_list = []
    delta_list = []

    for j, f in enumerate(F):
        a = f.numerator
        b = f.denominator
        D_j = Fraction(j) - Fraction(n) * f
        delta = Fraction(a - (p * a % b), b) if b > 0 else Fraction(0)
        D_list.append(D_j)
        f_list.append(f)
        delta_list.append(delta)

    # Compute alpha = Cov(D, f) / Var(f) over interior fractions
    # Actually alpha is over ALL fractions (the regression slope)
    mean_D = sum(D_list) / n
    mean_f = sum(f_list) / n  # = 1/2

    cov_Df = sum((D_list[i] - mean_D) * (f_list[i] - mean_f) for i in range(n)) / n
    var_f = sum((f_list[i] - mean_f)**2 for i in range(n)) / n
    alpha = cov_Df / var_f

    # D_err = D - alpha*(f - mean_f) - mean_D
    # sum(D_err * delta) over interior
    sum_Derr_delta = Fraction(0)
    C_prime = Fraction(0)
    for i in range(n):
        if f_list[i].denominator <= 1: continue
        D_err_i = D_list[i] - mean_D - alpha * (f_list[i] - mean_f)
        sum_Derr_delta += D_err_i * delta_list[i]
        C_prime += delta_list[i]**2

    threshold = (1 - alpha) * C_prime / 2
    correction = (C_prime - Fraction(2) * sum(D_list[i] * delta_list[i]
                  for i in range(n) if f_list[i].denominator > 1)) / 2
    corr_neg = "YES" if correction < 0 else "NO"

    print(f"{p:5d} {float(alpha):10.4f} {'YES' if alpha > 1 else 'NO':>8} "
          f"{float(sum_Derr_delta):16.4f} {float(threshold):12.4f} {corr_neg:>8}")

print("\n" + "=" * 80)
print("PART 5: The Dedekind sum sign argument")
print("=" * 80)
print("""
From SIGNED_FLUCTUATION_PROOF: [T_b - E[T_b]]/b^2 = sum_{d|b} mu(d)*s(p, b/d)

For PRIME denominator b = q: [T_q - E[T_q]]/q^2 = s(p, q) (since only d=1 contributes).

By Dedekind reciprocity: s(p, q) + s(q, p) = (p^2 + q^2 + 1)/(12pq) - 1/4

So s(p, q) = (p^2 + q^2 + 1)/(12pq) - 1/4 - s(q, p)

The leading term (p^2+q^2+1)/(12pq) - 1/4 decomposes as:
  = p/(12q) + q/(12p) + 1/(12pq) - 1/4

For q << p: this is approximately p/(12q) - 1/4, which is POSITIVE for q < p/3.

The correction s(q, p) has magnitude |s(q, p)| <= (p-1)/12 (Rademacher bound),
but more importantly, the SUM of s(q, p) over primes q up to N is controlled.

Let's check: for each M=-3 prime p, what fraction of prime denominators q < p
give s(p, q) > 0?
""")

for p in m3_primes:
    if p > 120:
        break
    N = p - 1
    pos = 0
    neg = 0
    total_s = Fraction(0)
    for q in range(2, N + 1):
        if not is_prime(q): continue
        s_pq = dedekind_sum(p, q)
        total_s += s_pq
        if s_pq > 0: pos += 1
        elif s_pq < 0: neg += 1

    print(f"p={p:4d}: primes q<p with s(p,q)>0: {pos}, s(p,q)<0: {neg}, "
          f"sum s(p,q) = {float(total_s):.4f}")

print("\n\nDONE.")
