#!/usr/bin/env python3
"""
B_identity_audit_3299.py

Compute B(p) DIRECTLY from primary Lean definition:
    B(p) = 2 · Σ_{f ∈ F_{p-1}} D_{p-1}(f) · δ_p(f)
where
    D_N(f) = rank(f, F_N) - |F_N| · f          (Lean: displacement)
    δ_p(f) = f - {p·f}                         (Lean: shiftFun)

Then compute the extra_high.md "B" via the Bern/Saw decomposition:
    Bern(p) = Σ D_extra(f) · (f - 1/2)
    Saw(p)  = Σ D_extra(f) · ψ(p·f)
    where D_extra(f) = i/(n-1) - f,  ψ(x) = {x} - 1/2  (or 0 if x∈Z)
and check the claimed identity:
    B(p) · n'² / 2 == Bern(p) - Saw(p)  ?

Also: compute Σ f² and Σ f(f-1/2) to verify the algebraic gap diagnosed in v3_honest §5.

All exact rationals via fractions.Fraction.
"""
from fractions import Fraction
import sys

def farey_seq(N):
    """Stern-Brocot Farey sequence F_N from 0/1 to 1/1, inclusive."""
    a, b = 0, 1
    c, d = 1, N
    out = [(a, b)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        out.append((a, b))
    return out

def frac_part(num, den):
    """{num/den} as Fraction in [0,1)."""
    if den == 0:
        raise ValueError
    r = num % den
    if r < 0:
        r += den
    return Fraction(r, den)

def psi(num, den):
    """ψ(x) = {x} - 1/2 if x not integer, else 0."""
    if den == 0:
        return Fraction(0)
    r = num % den
    if r == 0:
        return Fraction(0)
    return Fraction(r, den) - Fraction(1, 2)

def compute_B_primary(p):
    """B(p) = 2 Σ_{f ∈ F_{p-1}} D_{p-1}(f) · δ_p(f), exact rational."""
    F = farey_seq(p - 1)
    n = len(F)  # |F_{p-1}|
    half = Fraction(1, 2)
    B = Fraction(0)
    sum_D_sq = Fraction(0)
    sum_delta_sq = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        rank = i + 1  # 1-indexed rank in Lean
        D = Fraction(rank) - Fraction(n) * f       # primary displacement
        # δ(f) = f - {p f}.  pf = p*a/b; {p*a/b} = ((p*a) mod b)/b
        if b == 1:
            frac_pf = Fraction(0) if (p*a) % 1 == 0 else None  # always int
        else:
            frac_pf = Fraction((p*a) % b, b)
        delta = f - frac_pf
        B += D * delta
        sum_D_sq += D * D
        sum_delta_sq += delta * delta
    B *= 2
    return n, B, sum_D_sq, sum_delta_sq

def compute_bern_saw(p):
    """Bern, Saw with D_extra = i/(n-1) - f."""
    F = farey_seq(p - 1)
    n = len(F)
    nm1 = n - 1
    half = Fraction(1, 2)
    Bern = Fraction(0)
    Saw = Fraction(0)
    sum_f = Fraction(0)
    sum_f_sq = Fraction(0)
    sum_f_times_fm12 = Fraction(0)
    for i, (a, b) in enumerate(F):
        f = Fraction(a, b)
        D_extra = Fraction(i, nm1) - f
        Bern += D_extra * (f - half)
        Saw  += D_extra * psi(p * a, b)
        sum_f += f
        sum_f_sq += f * f
        sum_f_times_fm12 += f * (f - half)
    return n, Bern, Saw, sum_f, sum_f_sq, sum_f_times_fm12

def to_float(x):
    # safe for huge numerators/denominators
    if x == 0:
        return 0.0
    num, den = x.numerator, x.denominator
    sign = -1 if (num < 0) ^ (den < 0) else 1
    num, den = abs(num), abs(den)
    # scale down via bit-shift
    nb = num.bit_length()
    db = den.bit_length()
    shift = max(nb, db) - 100
    if shift > 0:
        num >>= shift
        den >>= shift
        if den == 0:
            return float('inf') * sign
    return sign * (num / den)

def main():
    primes = [11, 17, 97, 223, 1399, 1423, 3299]
    for p in primes:
        print(f"\n{'='*70}")
        print(f"p = {p}")
        n_prim, B_primary, sumD2, sumdel2 = compute_B_primary(p)
        n_eh, Bern, Saw, Sf, Sf2, Sf_fm12 = compute_bern_saw(p)
        assert n_prim == n_eh, "n mismatch"
        n = n_prim
        n_prime = n + (p - 1)  # |F_p|
        print(f"  n = |F_(p-1)| = {n}, n' = |F_p| = {n_prime}")
        # Primary B
        Bf = to_float(B_primary)
        print(f"  B(p) [primary, Lean def]    = {Bf:.10g}")
        print(f"     sign = {'POSITIVE' if Bf > 0 else 'NEGATIVE' if Bf < 0 else 'ZERO'}")
        # Extra-high claimed: B = (2/n'^2) (Bern - Saw)
        Bern_minus_Saw = Bern - Saw
        # The extra_high doc states: B(p) · n'²/2 = Bern - Saw
        # If true: Bern - Saw should equal B · n'^2 / 2
        lhs = B_primary * Fraction(n_prime, 1) ** 2 / 2
        rhs = Bern_minus_Saw
        diff = lhs - rhs
        print(f"  Bern(p) (extra_high)         = {to_float(Bern):.10g}")
        print(f"  Saw(p)  (extra_high)         = {to_float(Saw):.10g}")
        print(f"  Bern - Saw                   = {to_float(Bern_minus_Saw):.10g}")
        print(f"  B(p) · n'^2 / 2              = {to_float(lhs):.10g}")
        print(f"  diff [LHS - RHS]             = {to_float(diff):.10g}")
        print(f"  Identity B·n'^2/2 = Bern-Saw HOLDS? {'YES' if diff == 0 else 'NO'}")
        # If not, what's the relation?
        if diff != 0 and B_primary != 0:
            ratio = Bern_minus_Saw / B_primary
            print(f"  (Bern-Saw)/B = {to_float(ratio):.10g}  vs n'^2/2 = {n_prime**2 / 2:.10g}")
        # Algebraic checks for v3_honest §5
        print(f"  Σ f                          = {to_float(Sf):.10g}   (claim: n/2 = {n/2})")
        print(f"  Σ f^2                        = {to_float(Sf2):.10g}   (claim §7: n/4 = {n/4})")
        print(f"  Σ f(f-1/2)                   = {to_float(Sf_fm12):.10g}   (claim §7: 0)")
        # Bern via Chebyshev form would equal Bern only if Σ f(f-1/2) == 0
        # ChebForm = Bern + Σ f(f-1/2)
        # (Bern = (1/(n-1))·Σ i(f_i-1/2) - Σ f(f-1/2);  ChebForm = (1/(n-1))·Σ (i-(n-1)/2)(f-1/2) = (1/(n-1))·Σ i(f-1/2) (since Σ(f-1/2)=0))
        # So Bern - ChebForm = - Σ f(f-1/2)

if __name__ == "__main__":
    main()
