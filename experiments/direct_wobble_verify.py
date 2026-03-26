#!/usr/bin/env python3
"""
DIRECT WOBBLE VERIFICATION
============================

Directly computes W(p-1) and W(p) for small primes to check the sign of ΔW.
Also checks for bugs in the four-term decomposition.
"""

from fractions import Fraction
from math import gcd


def farey_sequence(N):
    """Generate F_N as sorted list of Fractions."""
    fracs = []
    a, b, c, d = 0, 1, 1, N
    fracs.append(Fraction(0))
    while c <= N:
        fracs.append(Fraction(c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return fracs


def wobble(fracs):
    """Compute W = (1/n^2) * sum D(f)^2."""
    n = len(fracs)
    D_sq = sum((j - n * f) ** 2 for j, f in enumerate(fracs))
    return D_sq / n ** 2, D_sq, n


def four_term_decomposition(p):
    """
    Compute the four-term decomposition for prime p.
    Checks: n'^2 * (W(p-1) - W(p)) = dilution_raw - B_raw - delta_sq - new_D_sq
    """
    N = p - 1
    old_fracs = farey_sequence(N)
    new_fracs = farey_sequence(p)

    n = len(old_fracs)
    n_prime = len(new_fracs)

    print(f"\n{'='*60}")
    print(f"p = {p}: N = {N}, n = n_old = {n}, n' = {n_prime}")
    print(f"  n' - n = {n_prime - n} = p-1 = {p-1}")

    # W(p-1) and W(p) directly
    W_old, old_D_sq, _ = wobble(old_fracs)
    W_new, new_D_sq_total, _ = wobble(new_fracs)
    DeltaW = W_old - W_new
    print(f"\n  W(p-1) = {float(W_old):.8f}")
    print(f"  W(p)   = {float(W_new):.8f}")
    print(f"  ΔW = W(p-1) - W(p) = {float(DeltaW):.8f}  {'<= 0 [GOOD]' if DeltaW <= 0 else '> 0 [BAD!]'}")

    # Four-term decomposition
    # For each old fraction f = a/b:
    #   D(f) = rank_old(f) - n * f
    #   delta(f) = tau(f) - (p-1)*f  where tau = #{new fracs < f}
    #   D_p(f) = D(f) + delta(f)

    # Compute delta for each old fraction
    D_old = []  # D values in F_{p-1}
    delta = []  # shifts
    D_p_old = []  # D_p values for old fractions in F_p

    # Build rank lookup for new Farey sequence
    rank_new = {f: j for j, f in enumerate(new_fracs)}

    for j, f in enumerate(old_fracs):
        D_j = j - n * f
        # tau(f) = #{k/p : k/p < f} = floor(p*f) [since f is not a multiple of 1/p,
        # UNLESS f = 0 or 1 or has denominator p which is impossible in F_{p-1}]
        # Actually f in F_{p-1} has denominator b <= p-1 < p, so p*f = p*a/b is not an integer.
        # So tau(f) = floor(p*f).
        a_f = f.numerator
        b_f = f.denominator
        if b_f == 1 and a_f == 1:
            # Special case: 1/1
            tau_f = p - 1  # all k/p < 1
            delta_f = tau_f - (p - 1) * f  # = (p-1) - (p-1)*1 = 0
        elif b_f == 1 and a_f == 0:
            tau_f = 0
            delta_f = 0
        else:
            # f = a/b with b >= 2, b <= p-1
            # p*a/b is not an integer (since b doesn't divide p*a, as gcd(a,b)=1 and b<p so b doesn't divide p)
            # tau(f) = floor(p*a/b)
            tau_f = (p * a_f) // b_f
            delta_f = tau_f - (p - 1) * f

        D_p_f = rank_new[f] - n_prime * f

        D_old.append(D_j)
        delta.append(delta_f)
        D_p_old.append(D_p_f)

    # Verify D_p(f) = D(f) + delta(f) for each old fraction
    errors = [(f, float(D_p_old[j] - D_old[j] - delta[j]))
              for j, f in enumerate(old_fracs)
              if abs(D_p_old[j] - D_old[j] - delta[j]) > 1e-9]
    if errors:
        print(f"\n  !!! BUG: D_p(f) != D(f) + delta(f) for {len(errors)} fractions !!!")
        for f, e in errors[:3]:
            print(f"    f={f}: error={e}")
    else:
        print(f"\n  VERIFIED: D_p(f) = D(f) + delta(f) for all {n} old fractions")

    # Compute sums
    old_D_sq_val = sum(d * d for d in D_old)
    delta_sq_val = sum(d * d for d in delta)
    B_raw_val = 2 * sum(D_old[j] * delta[j] for j in range(n))

    print(f"\n  old_D_sq (sum D_old^2) = {float(old_D_sq_val):.6f}  [should = n^2 * W_old = {float(n**2 * W_old):.6f}]")
    print(f"  delta_sq = {float(delta_sq_val):.6f}")
    print(f"  B_raw    = {float(B_raw_val):.6f}")

    # New fraction discrepancies
    new_frac_set = set(new_fracs) - set(old_fracs)
    new_D_sq_val = sum(
        (j - n_prime * f) ** 2
        for j, f in enumerate(new_fracs)
        if f not in set(old_fracs)
    )
    print(f"  new_D_sq (new fracs only) = {float(new_D_sq_val):.6f}")

    # dilution_raw
    dilution_raw_val = old_D_sq_val * (n_prime ** 2 - n ** 2) / n ** 2
    print(f"  dilution_raw = {float(dilution_raw_val):.6f}")

    # Check the four-term identity
    margin_val = new_D_sq_val + B_raw_val + delta_sq_val - dilution_raw_val
    print(f"\n  Four-term check:")
    print(f"    new_D_sq + B_raw + delta_sq = {float(new_D_sq_val + B_raw_val + delta_sq_val):.6f}")
    print(f"    dilution_raw               = {float(dilution_raw_val):.6f}")
    print(f"    margin = sum - dilution    = {float(margin_val):.6f}  {'>=0 [GOOD]' if margin_val >= 0 else '<0 [BAD!]'}")

    # Cross-check: n'^2 * DeltaW should equal dilution - margin
    nprime_sq_DeltaW = n_prime ** 2 * DeltaW
    print(f"\n    n'^2 * DeltaW = {float(nprime_sq_DeltaW):.6f}")
    print(f"    dilution - margin = {float(dilution_raw_val - margin_val):.6f}")
    print(f"    These should be equal: {abs(float(nprime_sq_DeltaW - (dilution_raw_val - margin_val))) < 1e-6}")

    # R = B_raw / delta_sq
    R = B_raw_val / delta_sq_val if delta_sq_val != 0 else float('inf')
    print(f"\n    R = B_raw/delta_sq = {float(R):.4f}")
    print(f"    1+R = {float(1+R):.4f}  [B+C>0 iff 1+R>0]")
    print(f"    B+C = (B_raw + delta_sq)/n'^2 = {float((B_raw_val + delta_sq_val) / n_prime**2):.8f}")
    print(f"    B+C > 0: {B_raw_val + delta_sq_val > 0}")

    return {
        'DeltaW': float(DeltaW),
        'margin': float(margin_val),
        'B_raw': float(B_raw_val),
        'delta_sq': float(delta_sq_val),
        'new_D_sq': float(new_D_sq_val),
        'dilution_raw': float(dilution_raw_val),
        'R': float(R),
    }


def main():
    print("DIRECT WOBBLE VERIFICATION")
    print("Computes W(p-1) and W(p) exactly using Fraction arithmetic.")
    print()

    primes_to_check = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

    results = {}
    for p in primes_to_check:
        r = four_term_decomposition(p)
        results[p] = r

    print("\n\nSUMMARY:")
    print(f"{'p':>4} {'ΔW':>10} {'margin_r':>10} {'R':>8} {'1+R':>8} {'B+C>0':>7}")
    print("-" * 55)
    for p, r in results.items():
        dil = r['dilution_raw']
        marg_r = r['margin'] / dil if dil != 0 else 0
        bc_ok = "YES" if r['B_raw'] + r['delta_sq'] > 0 else "NO"
        print(f"{p:4d} {r['DeltaW']:10.6f} {marg_r:10.6f} {r['R']:8.4f} {1+r['R']:8.4f} {bc_ok:>7}")

    # Check if DeltaW <= 0 for all (W non-decreasing)
    violations = [p for p, r in results.items() if r['DeltaW'] > 1e-12]
    if violations:
        print(f"\n!!! DeltaW > 0 VIOLATIONS: p = {violations}")
    else:
        print(f"\n  All {len(primes_to_check)} primes have DeltaW <= 0. ✓")


if __name__ == '__main__':
    main()
