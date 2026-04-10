#!/usr/bin/env python3
"""
Derive the EXACT formula for NC(p,b) = s(p,b) - C(p,b).

NC(p,b) = Σ_{gcd(a,b)>1, 1≤a<b} ((a/b))·((pa/b))

Key insight: if gcd(a,b) = d > 1, then a = d*a', b = d*b',
and ((a/b)) = ((a'/b')), ((pa/b)) = ((pa'/b')).

So NC(p,b) = Σ_{d|b, d>1} Σ_{a'=1, gcd(a',b')=1}^{b'-1} ((a'/b'))·((pa'/b'))
           = Σ_{d|b, d>1} C_coprime(p, b/d)   [if gcd(p, b/d)=1]

Wait, but ((pa/b)) = ((p·d·a'/(d·b'))) = ((pa'/b')).
So NC(p,b) = Σ_{d|b, d>1} [sum over a' coprime to b/d of ((a'/(b/d)))·((pa'/(b/d)))]

But we need gcd(a', b/d) = 1 AND a' ranges from 1 to b/d - 1.
Actually the condition is: a < b, gcd(a,b) = d means a = d*a' with 1 ≤ a' < b/d and gcd(a', b/d) = 1.

So: NC(p,b) = Σ_{d|b, d>1} C(p, b/d)

And therefore: s(p,b) = C(p,b) + NC(p,b) = C(p,b) + Σ_{d|b, d>1} C(p, b/d)
            = Σ_{d|b} C(p, b/d)

By Mobius inversion: C(p,b) = Σ_{d|b} μ(d) · s(p, b/d)

Let's verify this!
"""

from fractions import Fraction
from math import gcd

def sawtooth_exact(x_frac):
    fl = int(x_frac)
    if x_frac < 0 and x_frac != Fraction(fl):
        fl -= 1
    frac_part = x_frac - fl
    if frac_part == 0:
        return Fraction(0)
    return frac_part - Fraction(1, 2)

def coprime_residues(b):
    return [a for a in range(1, b) if gcd(a, b) == 1]

def moebius(n):
    if n == 1:
        return 1
    temp = n
    factors = []
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0
            factors.append(p)
        p += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)

def divisors(n):
    divs = []
    for d in range(1, n+1):
        if n % d == 0:
            divs.append(d)
    return divs

def compute_C_exact(p, b):
    total = Fraction(0)
    for a in coprime_residues(b):
        s1 = sawtooth_exact(Fraction(a, b))
        s2 = sawtooth_exact(Fraction(a * p, b))
        total += s1 * s2
    return total

def compute_s_exact(h, k):
    total = Fraction(0)
    for a in range(1, k):
        s1 = sawtooth_exact(Fraction(a, k))
        s2 = sawtooth_exact(Fraction(a * h, k))
        total += s1 * s2
    return total


def verify_mobius_inversion(primes, B_max=60):
    """
    Verify: s(p,b) = Σ_{d|b} C(p, b/d)
    And:    C(p,b) = Σ_{d|b} μ(d) · s(p, b/d)
    """
    print("MOBIUS INVERSION: C(p,b) = Σ_{d|b} μ(d) · s(p, b/d)")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")
        all_ok = True
        count = 0

        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            # Direct computation
            C_direct = compute_C_exact(p, b)

            # Via Mobius inversion
            C_mobius = Fraction(0)
            for d in divisors(b):
                mu_d = moebius(d)
                if mu_d == 0:
                    continue
                bd = b // d
                if bd < 2:
                    continue  # s(p,1) = 0
                if gcd(p, bd) > 1:
                    # s(p, b/d) when gcd(p, b/d) > 1
                    # This CAN happen even when gcd(p,b)=1
                    pass  # still compute it
                C_mobius += mu_d * compute_s_exact(p, bd)

            if C_direct != C_mobius:
                print(f"  MISMATCH at b={b}: direct={C_direct}, Mobius={C_mobius}")
                all_ok = False
            count += 1

        if all_ok:
            print(f"  VERIFIED for all {count} values of b ≤ {B_max}")

        # Also verify the other direction: s(p,b) = Σ_{d|b} C(p, b/d)
        print(f"  Verifying s(p,b) = Σ_{{d|b}} C(p, b/d)...")
        all_ok2 = True
        for b in range(2, B_max + 1):
            if gcd(p, b) > 1:
                continue

            s_direct = compute_s_exact(p, b)
            s_sum = Fraction(0)
            for d in divisors(b):
                bd = b // d
                if bd < 2:
                    continue
                # C(p, b/d) — but b/d might share factor with p
                if gcd(p, bd) > 1:
                    # In this case C(p, b/d) is still well-defined
                    pass
                s_sum += compute_C_exact(p, bd)

            if s_direct != s_sum:
                print(f"  s-MISMATCH at b={b}: direct={s_direct}, sum={s_sum}")
                all_ok2 = False

        if all_ok2:
            print(f"  s-direction also VERIFIED for all b ≤ {B_max}")


def analyze_implications(primes, B_max=100):
    """
    Now that we know C(p,b) = Σ_{d|b} μ(d)·s(p,b/d), we can write:

    Σ_b C(p,b) = Σ_b Σ_{d|b} μ(d)·s(p,b/d)
               = Σ_k s(p,k) · Σ_{d: dk≤B, gcd(p,dk)=1} μ(d)

    This is a convolution! And the inner sum Σ_{d≤B/k} μ(d) = M(B/k),
    the Mertens function at B/k.

    Similarly for R(p):
    R(p) = Σ_b C(p,b) / Σ_b V(b)
    where V(b) = Σ_{a cop b} ((a/b))^2

    KEY INSIGHT: V(b) = Σ_{a cop b} ((a/b))^2 also has a Mobius inversion:
    Σ_{a=1}^{b-1} ((a/b))^2 = (b-1)(2b-1)/(12b) ≈ b/6

    And V(b) = Σ_{d|b} μ(d) · [(b/d-1)(2b/d-1)/(12·b/d)]

    Actually: Σ_{a=1}^{k-1} ((a/k))^2 = (k^2-1)/(12k) for k ≥ 2
    [Because Σ ((a/k))^2 = Σ (a/k - 1/2)^2 = 1/k^2 · Σ a^2 - 1/k · Σ a + (k-1)/4
     = (k-1)(2k-1)/(6k) - (k-1)/2 + (k-1)/4 = ...]

    Let me just compute.
    """
    print("\n" + "=" * 70)
    print("IMPLICATIONS FOR THE PROOF")
    print("=" * 70)

    # First verify: Σ_{a=1}^{k-1} ((a/k))^2 = (k^2-1)/(12k)
    print("\nVerifying Σ ((a/k))^2 = (k²-1)/(12k):")
    for k in range(2, 20):
        actual = sum(sawtooth_exact(Fraction(a, k))**2 for a in range(1, k))
        predicted = Fraction(k**2 - 1, 12 * k)
        status = "OK" if actual == predicted else f"FAIL: got {actual}"
        print(f"  k={k}: {status}")

    # And V(b) = Σ_{a cop b} ((a/b))^2 by Mobius inversion
    print("\nV(b) = Σ_{a cop b} ((a/b))^2 via Mobius inversion:")
    print("V(b) = Σ_{d|b} μ(d) · ((b/d)²-1)/(12·(b/d))")
    for b in range(2, 25):
        V_direct = sum(sawtooth_exact(Fraction(a, b))**2 for a in coprime_residues(b))
        V_mobius = Fraction(0)
        for d in divisors(b):
            mu_d = moebius(d)
            if mu_d == 0:
                continue
            k = b // d
            if k < 2:
                continue
            V_mobius += mu_d * Fraction(k**2 - 1, 12 * k)

        status = "OK" if V_direct == V_mobius else f"FAIL: direct={V_direct}, mobius={V_mobius}"
        print(f"  b={b}: V={float(V_direct):.6f}, {status}")

    # Now the key ratio analysis
    print("\n" + "=" * 70)
    print("KEY RATIO: R(p) = Σ C(p,b) / Σ V(b)")
    print("Using Mobius inversion on BOTH numerator and denominator")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")

        # Compute R(p) at various B
        for B in [30, 50, 80, 100]:
            sum_C = Fraction(0)
            sum_V = Fraction(0)

            for b in range(2, B + 1):
                if gcd(p, b) > 1:
                    continue
                sum_C += compute_C_exact(p, b)
                sum_V += sum(sawtooth_exact(Fraction(a, b))**2 for a in coprime_residues(b))

            R = sum_C / sum_V if sum_V != 0 else Fraction(0)
            print(f"  B={B}: R(p) = {float(R):.8f}, R > -1/2? {float(R) > -0.5}")

        # Now decompose using Dedekind:
        # Σ_b C(p,b) = Σ_b Σ_{d|b} μ(d) s(p,b/d)
        #            = Σ_k Σ_{d} μ(d) s(p,k)  [where b = dk]
        # For fixed k: contribution = s(p,k) · (Σ_{d≤B/k, gcd(p,dk)=1} μ(d))
        B = 60
        print(f"\n  Decomposition at B={B}:")
        print(f"  Σ_b C(p,b) = Σ_k s(p,k) · M_p(B/k)")
        print(f"  where M_p(x) = Σ_{{d≤x, gcd(pd,k')=1}} μ(d)")

        # Direct computation of the decomposition
        sum_C_direct = Fraction(0)
        for b in range(2, B+1):
            if gcd(p, b) > 1:
                continue
            sum_C_direct += compute_C_exact(p, b)

        # Via s and Mertens-like sum
        sum_C_via_s = Fraction(0)
        for k in range(2, B+1):
            s_pk = compute_s_exact(p, k)
            if s_pk == 0:
                continue
            # Sum μ(d) for d such that dk ≤ B and gcd(p, dk) = 1
            mertens_contrib = Fraction(0)
            for d in range(1, B // k + 1):
                if gcd(p, d * k) > 1:
                    continue
                mu_d = moebius(d)
                mertens_contrib += mu_d
            sum_C_via_s += s_pk * mertens_contrib

        print(f"  Direct: Σ C = {float(sum_C_direct):.8f}")
        print(f"  Via s:  Σ C = {float(sum_C_via_s):.8f}")
        print(f"  Match: {abs(float(sum_C_direct - sum_C_via_s)) < 1e-10}")


def compute_weighted_dedekind_sum(primes):
    """
    For the proof, we need to bound:

    |Σ_b C(p,b)| / Σ_b V(b) < 1/2

    i.e., |Σ_b C(p,b)| < (1/2) Σ_b V(b)

    We know Σ_b V(b) = Σ_b Σ_{d|b} μ(d)(k²-1)/(12k)
    grows like ~B²/12 * (product factor)

    And |Σ_b C(p,b)| = |Σ_k s(p,k) · M_cop(B/k)|

    Using |s(p,k)| ≤ (k-1)/12 [trivial] or |s(p,k)| = O(log k) [Rademacher]:
    |Σ_b C(p,b)| ≤ Σ_k |s(p,k)| · |M_cop(B/k)|

    M_cop(x) ~ 0 on average (by PNT), so there's massive cancellation.
    In fact |M(x)| ≤ x (trivially) and |M(x)| = O(x/log x) unconditionally.

    So: |Σ_b C(p,b)| ≤ Σ_k O(log k) · O(B/(k log(B/k)))

    This is O(B) while Σ V(b) is O(B²), so R(p) → 0 as B → ∞!
    """
    print("\n" + "=" * 70)
    print("GROWTH RATE ANALYSIS: |Σ C| vs Σ V")
    print("=" * 70)

    for p in primes:
        print(f"\n--- Prime p = {p} ---")
        print(f"  {'B':>5} {'|Σ C|':>12} {'Σ V':>12} {'|R|':>12} {'Σ V / B²':>12}")

        for B in [20, 40, 60, 80, 100]:
            sum_C = Fraction(0)
            sum_V = Fraction(0)

            for b in range(2, B + 1):
                if gcd(p, b) > 1:
                    continue
                sum_C += compute_C_exact(p, b)
                sum_V += sum(sawtooth_exact(Fraction(a, b))**2 for a in coprime_residues(b))

            abs_C = abs(float(sum_C))
            V = float(sum_V)
            R = abs_C / V if V > 0 else 0
            V_ratio = V / (B * B)
            print(f"  {B:5d} {abs_C:12.4f} {V:12.4f} {R:12.6f} {V_ratio:12.6f}")


if __name__ == '__main__':
    import time
    t0 = time.time()

    primes = [13, 31, 97]
    verify_mobius_inversion(primes[:2], B_max=40)
    analyze_implications(primes, B_max=100)
    compute_weighted_dedekind_sum(primes)

    print(f"\nTotal time: {time.time()-t0:.1f}s")
