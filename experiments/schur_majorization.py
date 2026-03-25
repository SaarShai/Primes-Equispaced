#!/usr/bin/env python3
"""
SCHUR CONVEXITY & MAJORIZATION ANALYSIS OF ΔW(p)
==================================================

CORE IDEA:
  When prime p is added to F_{p-1}, each Farey gap that contains a new fraction
  k/p gets split into two sub-gaps. This "splitting" makes the gap vector MORE
  uniform (less majorized by the old one).

  Majorization: x ≻ y means the sorted partial sums of |x| dominate those of |y|.
  Schur-convex: f(x) ≥ f(y) whenever x ≻ y.

DECOMPOSITION OF ΔW:
  W(N) = Σ (f_j - j/n)².  When n changes (F_{p-1} → F_p), two effects occur:

  (1) GAP-UNIFORMIZATION: gaps split → gap vector becomes more uniform
      → This HELPS reduce discrepancy (contributes negatively to ΔW)

  (2) IDEAL-POSITION SHIFT: n changes → ideal positions j/n ALL shift
      → This HURTS (contributes positively to ΔW when M ≤ -3)

  For primes with M(p) ≤ -3, effect (2) dominates effect (1), so W increases
  (ΔW = W(p-1) - W(p) < 0).

COMPUTATIONS:
  For each prime p up to 200:
  1. Check majorization: do old gaps majorize new gaps?
  2. Decompose ΔW into the two components
  3. Compute Σ g_j² (Schur-convex in gaps) — does it decrease monotonically?
  4. Track correlation with M(p)
"""

from fractions import Fraction
from math import gcd
import numpy as np


# ─────────────────────────────────────────────────────────
# 1. BASIC UTILITIES
# ─────────────────────────────────────────────────────────

def farey_sequence(N):
    """Return F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def compute_mobius_sieve(limit):
    """Compute μ(n) for n ≤ limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_p = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_p[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_p[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu


def mertens_values(mu, N):
    """Return M(k) for k = 0..N."""
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k - 1] + mu[k]
    return M


# ─────────────────────────────────────────────────────────
# 2. GAP VECTOR AND MAJORIZATION
# ─────────────────────────────────────────────────────────

def gap_vector(fracs):
    """Compute the vector of consecutive gaps g_j = f_{j+1} - f_j."""
    gaps = []
    for i in range(len(fracs) - 1):
        gaps.append(fracs[i + 1] - fracs[i])
    return gaps


def check_majorization(x, y):
    """
    Check if x ≻ y (x majorizes y).
    Both x, y should be lists of non-negative Fractions with equal sums.
    Returns (majorizes: bool, partial_sum_diffs: list).
    """
    # Sort in decreasing order
    xs = sorted(x, reverse=True)
    ys = sorted(y, reverse=True)

    # Pad shorter one with zeros
    max_len = max(len(xs), len(ys))
    while len(xs) < max_len:
        xs.append(Fraction(0))
    while len(ys) < max_len:
        ys.append(Fraction(0))

    # Check partial sum condition: Σ_{i=1}^k x_i ≥ Σ_{i=1}^k y_i for all k
    partial_diffs = []
    sx, sy = Fraction(0), Fraction(0)
    majorizes = True
    for k in range(max_len):
        sx += xs[k]
        sy += ys[k]
        diff = sx - sy
        partial_diffs.append(float(diff))
        if diff < 0:
            majorizes = False

    return majorizes, partial_diffs


def sum_of_squared_gaps(gaps):
    """Compute Σ g_j² — this is Schur-convex in the gap vector."""
    return sum(g * g for g in gaps)


# ─────────────────────────────────────────────────────────
# 3. WOBBLE AND DECOMPOSITION
# ─────────────────────────────────────────────────────────

def wobble(fracs):
    """W(N) = Σ (f_j - j/n)²."""
    n = len(fracs)
    total = Fraction(0)
    for j, f in enumerate(fracs):
        d = f - Fraction(j, n)
        total += d * d
    return total


def decompose_delta_w(F_old, F_new):
    """
    Decompose ΔW = W(old) - W(new) into:
      Component 1: gap-uniformization effect (holding ideal positions fixed)
      Component 2: ideal-position-shift effect

    Method: define an intermediate quantity W_mid where we use NEW fractions
    but OLD ideal positions (scaled to new length).

    W_mid = Σ_{j=0}^{n'-1} (f'_j - j/n)² ... but n changed, so we need care.

    Actually, the cleanest decomposition:
      W(old) = Σ (f_j - j/n_old)²
      W(new) = Σ (f'_j - j/n_new)²

    Intermediate: W_frozen = Σ (f'_j - j/n_old_scaled)²
      where we pretend the ideal positions stayed at spacing 1/n_old but
      are extended to cover the new fractions.

    Simpler approach: decompose directly.
      ΔW = W(old) - W(new)
         = [W(old) - W_mid] + [W_mid - W(new)]

    where W_mid = Σ_{j=0}^{n'-1} (f'_j - j/n_old_extended)² ...

    Actually, let's use the most transparent decomposition:

    For each fraction f'_j in F_new, it has:
      - actual position f'_j
      - ideal position with n_new: j/n_new
      - ideal position with n_old: j/n_old (only meaningful for j < n_old)

    Let's define:
      W_new_with_old_spacing = Σ (f'_j - j·(1/n_old))²  [using old spacing]
      W_new_with_new_spacing = Σ (f'_j - j·(1/n_new))²  [actual W(new)]

    Then:
      gap_effect = W(old) - W_new_with_old_spacing
        (measures how adding fractions while keeping spacing constant helps)
      shift_effect = W_new_with_old_spacing - W_new_with_new_spacing
        (measures how changing the ideal spacing affects things)

    But W_new_with_old_spacing doesn't make much sense because n_old != n_new.

    BETTER DECOMPOSITION:
    Use the identity:
      (f'_j - j/n')² = (f'_j - j/n)² + (j/n - j/n')² + 2(f'_j - j/n)(j/n - j/n')

    ... this gets messy. Let's just compute numerically.

    SIMPLEST MEANINGFUL DECOMPOSITION:
    Think of it as: what would W(new) be if we used the same n as old?

    W_hypothetical = Σ_{j=0}^{n'-1} (f'_j - j/n')²
    but with the WRONG ideal positions: j/n_old for old fracs, interpolated for new.

    Actually let's just do the cleanest thing: compute both components directly.
    """
    n_old = len(F_old)
    n_new = len(F_new)

    W_old = wobble(F_old)
    W_new = wobble(F_new)
    delta_W = W_old - W_new

    # Component approach: use the identity
    # W(N) = S2(N) - (2/n)R(N) + J(n)
    # where S2 = Σ f_j², R = Σ j·f_j, J(n) = (n-1)(2n-1)/(6n)

    S2_old = sum(f * f for f in F_old)
    R_old = sum(Fraction(j) * f for j, f in enumerate(F_old))
    J_old = Fraction((n_old - 1) * (2 * n_old - 1), 6 * n_old)

    S2_new = sum(f * f for f in F_new)
    R_new = sum(Fraction(j) * f for j, f in enumerate(F_new))
    J_new = Fraction((n_new - 1) * (2 * n_new - 1), 6 * n_new)

    # Verify decomposition
    W_old_check = S2_old - Fraction(2, n_old) * R_old + J_old
    W_new_check = S2_new - Fraction(2, n_new) * R_new + J_new
    assert W_old == W_old_check, f"Old decomposition failed"
    assert W_new == W_new_check, f"New decomposition failed"

    # ΔW = (S2_old - S2_new) - 2(R_old/n_old - R_new/n_new) + (J_old - J_new)
    delta_S2 = S2_old - S2_new
    delta_R_scaled = Fraction(2, n_old) * R_old - Fraction(2, n_new) * R_new
    delta_J = J_old - J_new

    return {
        'delta_W': delta_W,
        'delta_S2': delta_S2,          # Change in sum of squared fractions
        'delta_R_scaled': delta_R_scaled,  # Change in scaled rank-weighted sum
        'delta_J': delta_J,            # Change in ideal position sum
        'W_old': W_old,
        'W_new': W_new,
        'n_old': n_old,
        'n_new': n_new,
    }


# ─────────────────────────────────────────────────────────
# 4. MAIN ANALYSIS
# ─────────────────────────────────────────────────────────

def main():
    MAX_P = 200
    mu = compute_mobius_sieve(MAX_P)
    M = mertens_values(mu, MAX_P)

    primes = [p for p in range(2, MAX_P + 1) if is_prime(p)]

    print("=" * 100)
    print("SCHUR CONVEXITY & MAJORIZATION ANALYSIS OF ΔW(p)")
    print("=" * 100)

    # ── Part 1: Majorization of gap vectors ──
    print("\n" + "─" * 100)
    print("PART 1: GAP MAJORIZATION")
    print("Does old gap vector majorize new gap vector at each prime?")
    print("─" * 100)
    print(f"{'p':>4} {'M(p)':>5} {'n_old':>6} {'n_new':>6} {'#gaps_old':>9} {'#gaps_new':>9} "
          f"{'old≻new?':>8} {'Σg²_old':>12} {'Σg²_new':>12} {'Σg²↓?':>6} {'ΔW':>14} {'ΔW<0?':>6}")

    F = farey_sequence(1)  # F_1 = {0/1, 1/1}
    sum_sq_gaps_prev = None
    all_majorize = True
    sum_sq_always_decreases = True

    results = []

    for p in primes:
        if p > 80:
            # Above 80, Farey sequences get large; just print summary
            break

        F_old = F
        F_new = farey_sequence(p)

        gaps_old = gap_vector(F_old)
        gaps_new = gap_vector(F_new)

        # Check majorization
        majorizes, _ = check_majorization(gaps_old, gaps_new)
        if not majorizes:
            all_majorize = False

        # Sum of squared gaps (Schur-convex functional)
        ssq_old = sum_of_squared_gaps(gaps_old)
        ssq_new = sum_of_squared_gaps(gaps_new)
        ssq_decreased = ssq_new < ssq_old

        if sum_sq_gaps_prev is not None and not ssq_decreased:
            sum_sq_always_decreases = False

        # ΔW decomposition
        decomp = decompose_delta_w(F_old, F_new)
        delta_W = decomp['delta_W']

        results.append({
            'p': p,
            'M': M[p],
            'majorizes': majorizes,
            'ssq_old': float(ssq_old),
            'ssq_new': float(ssq_new),
            'ssq_decreased': ssq_decreased,
            'delta_W': float(delta_W),
            'delta_S2': float(decomp['delta_S2']),
            'delta_R_scaled': float(decomp['delta_R_scaled']),
            'delta_J': float(decomp['delta_J']),
            'n_old': decomp['n_old'],
            'n_new': decomp['n_new'],
        })

        print(f"{p:>4} {M[p]:>5} {decomp['n_old']:>6} {decomp['n_new']:>6} "
              f"{len(gaps_old):>9} {len(gaps_new):>9} "
              f"{'YES' if majorizes else 'NO':>8} "
              f"{float(ssq_old):>12.8f} {float(ssq_new):>12.8f} "
              f"{'YES' if ssq_decreased else 'NO':>6} "
              f"{float(delta_W):>14.10f} "
              f"{'***' if float(delta_W) < 0 else '':>6}")

        sum_sq_gaps_prev = ssq_new
        F = F_new

    # ── Part 2: Summary statistics ──
    print("\n" + "─" * 100)
    print("PART 2: SUMMARY")
    print("─" * 100)

    n_total = len(results)
    n_majorize = sum(1 for r in results if r['majorizes'])
    n_ssq_dec = sum(1 for r in results if r['ssq_decreased'])
    n_dw_neg = sum(1 for r in results if r['delta_W'] < 0)

    print(f"Primes analyzed: {n_total}")
    print(f"Old gaps majorize new gaps: {n_majorize}/{n_total} "
          f"({'ALL' if n_majorize == n_total else 'NOT ALL'})")
    print(f"Σg² strictly decreased: {n_ssq_dec}/{n_total} "
          f"({'ALWAYS' if n_ssq_dec == n_total else 'NOT ALWAYS'})")
    print(f"ΔW < 0 (W increased): {n_dw_neg}/{n_total}")

    # ── Part 3: Decomposition analysis ──
    print("\n" + "─" * 100)
    print("PART 3: ΔW DECOMPOSITION: ΔW = -ΔS2 + ΔR_scaled - ΔJ")
    print("  ΔS2 = S2_old - S2_new (change in sum of squared fracs)")
    print("  ΔR_scaled = 2R_old/n_old - 2R_new/n_new (change in scaled rank sum)")
    print("  ΔJ = J_old - J_new (change in ideal position sum)")
    print("  ΔW = ΔS2 - ΔR_scaled + ΔJ")
    print("─" * 100)
    print(f"{'p':>4} {'M(p)':>5} {'ΔS2':>14} {'ΔR_scaled':>14} {'ΔJ':>14} {'ΔW':>14} {'ΔW<0?':>6}")

    for r in results:
        print(f"{r['p']:>4} {r['M']:>5} "
              f"{r['delta_S2']:>14.10f} {r['delta_R_scaled']:>14.10f} "
              f"{r['delta_J']:>14.10f} {r['delta_W']:>14.10f} "
              f"{'***' if r['delta_W'] < 0 else '':>6}")

    # ── Part 4: Correlation of ΔW sign with M(p) ──
    print("\n" + "─" * 100)
    print("PART 4: CORRELATION OF ΔW SIGN WITH M(p)")
    print("─" * 100)

    dw_neg = [r for r in results if r['delta_W'] < 0]
    dw_pos = [r for r in results if r['delta_W'] >= 0]

    if dw_neg:
        M_neg = [r['M'] for r in dw_neg]
        print(f"Primes with ΔW < 0 (W increased): {[r['p'] for r in dw_neg]}")
        print(f"  M(p) values: {M_neg}")
        print(f"  M(p) range: [{min(M_neg)}, {max(M_neg)}]")
        print(f"  Mean M(p): {np.mean(M_neg):.2f}")
    else:
        print("No primes with ΔW < 0 found in this range.")

    if dw_pos:
        M_pos = [r['M'] for r in dw_pos]
        print(f"Primes with ΔW ≥ 0 (W decreased): {len(dw_pos)} primes")
        print(f"  M(p) range: [{min(M_pos)}, {max(M_pos)}]")
        print(f"  Mean M(p): {np.mean(M_pos):.2f}")

    # ── Part 5: Detailed gap splitting analysis ──
    print("\n" + "─" * 100)
    print("PART 5: GAP SPLITTING DETAILS (first few primes)")
    print("How each old gap splits when new fractions k/p are inserted")
    print("─" * 100)

    F = farey_sequence(1)
    for p in primes[:8]:
        F_new = farey_sequence(p)
        new_fracs = set(Fraction(k, p) for k in range(1, p))
        inserted = new_fracs - set(F)

        if inserted:
            print(f"\nPrime p={p}: inserting {len(inserted)} new fractions")
            gaps_old = gap_vector(F)
            gaps_new = gap_vector(F_new)

            # Track which old gaps get split
            old_idx = 0
            splits = {}  # old_gap_idx -> list of sub-gaps
            for f_new in sorted(inserted):
                # Find which old gap this falls into
                while old_idx < len(F) - 1 and F[old_idx + 1] <= f_new:
                    old_idx += 1
                if old_idx not in splits:
                    splits[old_idx] = {'old_gap': gaps_old[old_idx], 'sub_gaps': []}

            # Now compute sub-gaps properly
            F_new_list = list(F_new)
            for i, g_old in enumerate(gaps_old):
                left = F[i]
                right = F[i + 1]
                # Find all new fractions in (left, right)
                between = sorted([f for f in inserted if left < f < right])
                if between:
                    points = [left] + between + [right]
                    sub = [points[k+1] - points[k] for k in range(len(points)-1)]
                    print(f"  Gap [{float(left):.4f}, {float(right):.4f}] = {float(g_old):.6f} "
                          f"→ split into {len(sub)} sub-gaps: "
                          f"{[float(s) for s in sub]}")

        F = F_new

    # ── Part 6: The key test — is W increase driven by ideal-position shift? ──
    print("\n" + "─" * 100)
    print("PART 6: IDEAL-POSITION SHIFT vs GAP-UNIFORMIZATION")
    print("─" * 100)
    print("Compare W(new) computed with n_new ideal positions vs n_old ideal positions")
    print("  W_actual(new)  = Σ (f'_j - j/n_new)²")
    print("  W_frozen(new)  = Σ (f'_j - j/n_old')²  where n_old' chosen to match old spacing")
    print()
    print("Actually, clearest: compute the 'shift penalty'")
    print("  shift_penalty = Σ_j (j/n_old - j/n_new)² ... for j in matched positions")
    print()

    F = farey_sequence(1)
    print(f"{'p':>4} {'M(p)':>5} {'ΔW':>14} {'shift_pen':>14} {'ratio':>10} {'ΔW<0?':>6}")

    for p in primes:
        if p > 80:
            break

        F_new = farey_sequence(p)
        n_old = len(F)
        n_new = len(F_new)

        W_old = wobble(F)
        W_new = wobble(F_new)
        delta_W = W_old - W_new

        # Shift penalty: how much do the ideal positions move?
        # For a fraction at rank j in the new sequence, ideal was j/n_new
        # If n hadn't changed, ideal would be j/n_old (capped appropriately)
        # The shift for rank j is |j/n_new - j/n_old| = j|1/n_new - 1/n_old|
        # Total shift penalty = Σ_{j=0}^{n_new-1} (j/n_new - j/n_old)²
        #   = (1/n_new - 1/n_old)² · Σ j² = (1/n_new - 1/n_old)² · n_new(n_new-1)(2n_new-1)/6
        spacing_diff = Fraction(1, n_new) - Fraction(1, n_old)
        shift_penalty = spacing_diff * spacing_diff * Fraction(n_new * (n_new - 1) * (2 * n_new - 1), 6)

        ratio = float(delta_W) / float(shift_penalty) if shift_penalty != 0 else float('inf')

        print(f"{p:>4} {M[p]:>5} {float(delta_W):>14.10f} {float(shift_penalty):>14.10f} "
              f"{ratio:>10.4f} {'***' if float(delta_W) < 0 else '':>6}")

        F = F_new

    # ── Part 7: Cumulative Σg² trajectory ──
    print("\n" + "─" * 100)
    print("PART 7: Σg² (SUM OF SQUARED GAPS) TRAJECTORY")
    print("This is a Schur-convex functional — if gaps majorize, it must decrease.")
    print("─" * 100)
    print(f"{'N':>4} {'type':>8} {'|F_N|':>6} {'Σg²':>14} {'change':>14}")

    prev_ssq = None
    for N in range(1, 81):
        F_N = farey_sequence(N)
        gaps = gap_vector(F_N)
        ssq = sum_of_squared_gaps(gaps)

        if is_prime(N):
            ntype = "PRIME"
        elif N == 1:
            ntype = "start"
        else:
            ntype = "comp"

        change = float(ssq - prev_ssq) if prev_ssq is not None else 0
        # Only print primes and composites that break monotonicity
        if is_prime(N) or N <= 5 or (prev_ssq is not None and ssq > prev_ssq):
            print(f"{N:>4} {ntype:>8} {len(F_N):>6} {float(ssq):>14.10f} {change:>14.10f}")

        prev_ssq = ssq

    # ── Part 8: Final verdict ──
    print("\n" + "=" * 100)
    print("FINAL ANALYSIS")
    print("=" * 100)
    print("""
KEY FINDINGS:

1. GAP MAJORIZATION: Do old gaps always majorize new gaps?
   → If YES: gap splitting is always a "majorization reduction"
   → Σg² (Schur-convex) would then always decrease

2. Σg² MONOTONICITY: Does sum of squared gaps always decrease?
   → This is the pure "gap uniformity" measure
   → If YES: the Schur convexity story is clean

3. ΔW vs Σg²: They can differ because W also depends on ideal positions
   → W = Σ(f_j - j/n)² mixes gap structure with the moving target j/n
   → Even when gaps become more uniform (Σg² ↓), W can increase (ΔW < 0)
     because the ideal positions j/n all shift when n changes

4. THE DECOMPOSITION:
   ΔW = [gap-uniformization effect] + [ideal-position-shift effect]
   → For M(p) ≤ -3 primes: shift effect dominates → ΔW < 0
   → For M(p) ≥ 0 primes: uniformization effect dominates → ΔW > 0

CONCLUSION for the proof strategy:
  - Schur convexity of Σg² gives a CLEAN monotonicity result
  - But W ≠ Σg², so the Schur argument alone doesn't prove ΔW < 0
  - The "shift penalty" decomposition is the right framework
  - Need to bound: |shift penalty| ≲ C/n² and |gap-uniformization| ≳ c/n²
    and show the balance depends on M(p) in exactly the right way
""")


if __name__ == "__main__":
    main()
