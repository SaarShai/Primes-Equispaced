#!/usr/bin/env python3
"""
Wasserstein Optimal Transport Approach to W(N) Monotonicity
============================================================

IDEA: Reformulate W(N) as a squared Wasserstein distance.

W(N) = sum_{j=1}^{n} (f_j - j/n)^2

This is n times the squared W_2 distance between two discrete measures:
  - mu_Farey = (1/n) sum delta_{f_j}     (empirical Farey measure)
  - mu_uniform = (1/n) sum delta_{j/n}    (uniform grid measure)

Specifically: W_2^2(mu_Farey, mu_uniform) = (1/n) * W(N)

Since f_1 < f_2 < ... < f_n and j/n is increasing, the optimal transport
coupling is the identity (monotone rearrangement). So W_2^2 = (1/n) sum (f_j - j/n)^2.

TRIANGLE INEQUALITY APPROACH:
When we add prime p, going from F_{p-1} to F_p:
  W_2(mu_new, unif_new) <= W_2(mu_new, mu_old_rescaled) + W_2(mu_old_rescaled, unif_new)

TALAGRAND T_2 INEQUALITY:
  W_2^2(mu, nu) <= (2/rho) * KL(mu || nu)
where rho is the log-Sobolev constant.

This script computes:
1. W_2^2 between Farey and uniform for N = 2..200
2. Triangle inequality decomposition when adding prime p
3. KL divergence of Farey gap distribution vs uniform gaps
4. Whether Talagrand T_2 gives useful bounds on W(N)/n
"""

from fractions import Fraction
from math import gcd, log, sqrt, pi
import numpy as np
from collections import defaultdict


# ── Farey sequence utilities ──────────────────────────────────────────────

def farey_sequence(N):
    """Return F_N as sorted list of Fraction objects."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)


def farey_float(N):
    """Return F_N as sorted numpy array of floats."""
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return np.array([float(f) for f in sorted(fracs)])


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


def compute_W(farr):
    """Compute W(N) = sum (f_j - j/n)^2 from a float array of Farey fractions."""
    n = len(farr)
    ideal = np.arange(n) / n  # j/n for j = 0, 1, ..., n-1
    # Note: using 0-indexed here: f_0=0, f_1, ..., f_{n-1}=1
    # and ideal positions j/n for j=0,...,n-1
    # Some formulations use j/(n-1) -- let's use j/n for consistency with W_2
    return np.sum((farr - ideal) ** 2)


def compute_W2_squared(farr):
    """Compute W_2^2 = (1/n) * sum (f_j - j/n)^2 = W(N)/n."""
    n = len(farr)
    ideal = np.arange(n) / n
    return np.mean((farr - ideal) ** 2)


# ── PART 1: W_2^2 for N = 2..200 ─────────────────────────────────────────

def part1_w2_vs_N():
    """Compute W_2^2(Farey, uniform) for each N."""
    print("=" * 70)
    print("PART 1: W_2^2(Farey, uniform) as a function of N")
    print("=" * 70)
    print()

    results = []
    for N in range(2, 201):
        farr = farey_float(N)
        n = len(farr)
        W = compute_W(farr)
        W2sq = W / n
        results.append((N, n, W, W2sq))

    # Show key values
    print(f"{'N':>4}  {'|F_N|':>7}  {'W(N)':>14}  {'W2^2':>14}  {'W(N) mono?':>10}")
    print("-" * 60)

    prev_W = None
    mono_violations = 0
    for N, n, W, W2sq in results:
        if prev_W is not None:
            mono = "YES" if W <= prev_W else "*** NO ***"
            if W > prev_W:
                mono_violations += 1
        else:
            mono = "---"
        if N <= 30 or is_prime(N) or N % 20 == 0:
            print(f"{N:>4}  {n:>7}  {W:>14.8f}  {W2sq:>14.10f}  {mono:>10}")
        prev_W = W

    print(f"\nW(N) monotonicity violations in [2,200]: {mono_violations}")

    # Check W_2^2 monotonicity too
    prev_W2 = None
    w2_violations = 0
    for N, n, W, W2sq in results:
        if prev_W2 is not None and W2sq > prev_W2:
            w2_violations += 1
        prev_W2 = W2sq

    print(f"W_2^2 monotonicity violations in [2,200]: {w2_violations}")

    # Asymptotic behavior
    print("\nAsymptotic scaling of W_2^2:")
    for N, n, W, W2sq in results:
        if N in [10, 20, 50, 100, 200]:
            # Expected: W ~ 1/(12N^2) asymptotically? Let's check
            ratio_N2 = W2sq * N * N
            ratio_n = W2sq * n
            print(f"  N={N:>3}: W_2^2 = {W2sq:.2e}, W_2^2 * N^2 = {ratio_N2:.6f}, "
                  f"W_2^2 * n = {ratio_n:.6f}")

    return results


# ── PART 2: Triangle inequality when adding prime p ───────────────────────

def part2_triangle_inequality():
    """
    When adding prime p: F_{p-1} -> F_p.

    We decompose via the triangle inequality:
      W_2(mu_p, unif_p) <= W_2(mu_p, mu_{p-1,rescaled}) + W_2(mu_{p-1,rescaled}, unif_p)

    But actually a more natural decomposition uses the "merged" measure.

    Key insight: mu_p is obtained from mu_{p-1} by adding p-1 new points.
    The new measure has n' = n + (p-1) points instead of n.

    We compute the actual transport cost of:
    Term A: Moving old Farey points to their new "ideal" positions in the n'-grid
    Term B: Moving new k/p fractions to their ideal positions
    Term C: The "reshuffling" cost from interleaving
    """
    print("\n" + "=" * 70)
    print("PART 2: Triangle Inequality Decomposition at Primes")
    print("=" * 70)
    print()

    primes = [p for p in range(2, 101) if is_prime(p)]

    print(f"{'p':>4}  {'n_old':>6}  {'n_new':>6}  {'W2_old':>12}  {'W2_new':>12}  "
          f"{'delta':>12}  {'sign':>5}")
    print("-" * 75)

    prev_cache = {}
    for p in primes:
        f_old = farey_float(p - 1) if p > 2 else np.array([0.0, 1.0])
        f_new = farey_float(p)

        n_old = len(f_old)
        n_new = len(f_new)

        W2_old = compute_W2_squared(f_old)
        W2_new = compute_W2_squared(f_new)
        delta = W2_new - W2_old

        sign = "+" if delta > 0 else "-"
        print(f"{p:>4}  {n_old:>6}  {n_new:>6}  {W2_old:>12.8f}  {W2_new:>12.8f}  "
              f"{delta:>12.2e}  {sign:>5}")

    # Now decompose the transport more carefully
    print("\n--- Detailed transport decomposition ---")
    print()

    for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        f_old = farey_float(p - 1)
        f_new = farey_float(p)
        n_old = len(f_old)
        n_new = len(f_new)

        # Ideal grids
        ideal_old = np.arange(n_old) / n_old
        ideal_new = np.arange(n_new) / n_new

        # W_2^2 values
        W2_old = np.mean((f_old - ideal_old) ** 2)
        W2_new = np.mean((f_new - ideal_new) ** 2)

        # Which of the new Farey points came from the old sequence?
        old_set = set()
        for b in range(1, p):
            for a in range(0, b + 1):
                if gcd(a, b) == 1:
                    old_set.add(Fraction(a, b))

        # New fractions: k/p for k=1,...,p-1
        new_fracs = [Fraction(k, p) for k in range(1, p)]

        # In f_new, find positions of old vs new points
        old_positions = []  # positions (indices) of old fractions in f_new
        new_positions = []  # positions of new fractions in f_new
        for i, val in enumerate(f_new):
            frac = Fraction(val).limit_denominator(p)
            # Check if it's an old fraction
            if frac in old_set:
                old_positions.append(i)
            else:
                new_positions.append(i)

        # Cost decomposition:
        # "Relabeling cost": old fractions moved from old ideal to new ideal
        if len(old_positions) == n_old:
            relabel_cost = sum(
                (f_new[old_positions[j]] - ideal_new[old_positions[j]]) ** 2
                for j in range(n_old)
            ) / n_new

            # "Insertion cost": new fractions' deviation from new ideal
            insert_cost = sum(
                (f_new[new_positions[j]] - ideal_new[new_positions[j]]) ** 2
                for j in range(len(new_positions))
            ) / n_new

            print(f"p={p:>3}: W2_old={W2_old:.6e}, W2_new={W2_new:.6e}, "
                  f"relabel={relabel_cost:.6e}, insert={insert_cost:.6e}, "
                  f"ratio(relabel/total)={relabel_cost/W2_new:.4f}")


# ── PART 3: KL divergence of gap distributions ───────────────────────────

def part3_kl_divergence():
    """
    Compute KL divergence between:
    - Farey gap distribution (gaps between consecutive Farey fractions)
    - Uniform gap distribution (all gaps = 1/n)

    Talagrand T_2: W_2^2(mu, nu) <= (2/rho) * KL(mu || nu)
    If we can bound rho (log-Sobolev constant), this gives W_2 bounds.
    """
    print("\n" + "=" * 70)
    print("PART 3: KL Divergence of Gap Distributions")
    print("=" * 70)
    print()

    print(f"{'N':>4}  {'n':>6}  {'KL(gaps||unif)':>14}  {'W2^2':>12}  "
          f"{'ratio W2/KL':>12}  {'max_gap/mean':>12}")
    print("-" * 75)

    results = []
    for N in range(2, 201):
        farr = farey_float(N)
        n = len(farr)

        # Gaps
        gaps = np.diff(farr)
        mean_gap = 1.0 / (n - 1)  # since f goes from 0 to 1

        # KL divergence: KL(empirical_gaps || uniform_gaps)
        # = sum p_i * log(p_i / q_i)
        # where p_i = gap_i / sum(gaps) = gap_i (since sum = 1)
        # and q_i = 1/(n-1) for all i (uniform distribution over gaps)
        #
        # KL = sum gap_i * log(gap_i / (1/(n-1)))
        # = sum gap_i * log((n-1) * gap_i)
        # = sum gap_i * (log(n-1) + log(gap_i))
        # = log(n-1) + sum gap_i * log(gap_i)
        # = log(n-1) - H(gaps)

        # Treat each gap as a probability weight (they sum to 1)
        kl = 0.0
        for g in gaps:
            if g > 0:
                kl += g * log(g * (n - 1))

        W2sq = compute_W2_squared(farr)
        ratio = W2sq / kl if kl > 1e-20 else float('inf')
        max_gap_ratio = max(gaps) / mean_gap

        results.append((N, n, kl, W2sq, ratio, max_gap_ratio))

        if N <= 30 or is_prime(N) or N % 20 == 0:
            print(f"{N:>4}  {n:>6}  {kl:>14.8f}  {W2sq:>12.8e}  "
                  f"{ratio:>12.6f}  {max_gap_ratio:>12.4f}")

    # Check if ratio W2/KL is bounded
    ratios = [r[4] for r in results if r[4] < float('inf')]
    print(f"\nW_2^2 / KL ratio: min={min(ratios):.6f}, max={max(ratios):.6f}")
    print(f"  => If ratio bounded, Talagrand gives: rho >= 2 / max_ratio = "
          f"{2/max(ratios):.4f}")

    # KL monotonicity
    prev_kl = None
    kl_mono_violations = 0
    for N, n, kl, W2sq, ratio, mgr in results:
        if prev_kl is not None and kl > prev_kl:
            kl_mono_violations += 1
        prev_kl = kl
    print(f"KL monotonicity violations: {kl_mono_violations}")

    return results


# ── PART 4: Talagrand T_2 bound analysis ─────────────────────────────────

def part4_talagrand_bound():
    """
    Check if Talagrand T_2 inequality gives useful bounds.

    For measures on [0,1], the log-Sobolev constant rho depends on the
    reference measure. For the uniform measure on [0,1], rho = pi^2/2
    (Poincare constant, which lower-bounds log-Sobolev).

    T_2 inequality: W_2^2(mu, nu) <= (2/rho) * KL(mu || nu)

    We check:
    1. Does W_2^2 <= C * KL for some constant C?
    2. What's the effective rho?
    3. Can we use this to bound delta_W_2^2 when adding a prime?
    """
    print("\n" + "=" * 70)
    print("PART 4: Talagrand T_2 Bound Analysis")
    print("=" * 70)
    print()

    primes = [p for p in range(3, 151) if is_prime(p)]

    print("--- Checking T_2 at transitions (adding prime p) ---")
    print()
    print(f"{'p':>4}  {'KL_old':>12}  {'KL_new':>12}  {'dKL':>12}  "
          f"{'W2_old':>12}  {'W2_new':>12}  {'dW2':>12}")
    print("-" * 90)

    for p in primes[:25]:
        f_old = farey_float(p - 1) if p > 2 else np.array([0.0, 1.0])
        f_new = farey_float(p)
        n_old, n_new = len(f_old), len(f_new)

        # KL for old
        gaps_old = np.diff(f_old)
        kl_old = sum(g * log(g * (n_old - 1)) for g in gaps_old if g > 0)

        # KL for new
        gaps_new = np.diff(f_new)
        kl_new = sum(g * log(g * (n_new - 1)) for g in gaps_new if g > 0)

        W2_old = compute_W2_squared(f_old)
        W2_new = compute_W2_squared(f_new)

        dKL = kl_new - kl_old
        dW2 = W2_new - W2_old

        print(f"{p:>4}  {kl_old:>12.6e}  {kl_new:>12.6e}  {dKL:>12.4e}  "
              f"{W2_old:>12.6e}  {W2_new:>12.6e}  {dW2:>12.4e}")

    # Compute effective log-Sobolev constant
    print("\n--- Effective log-Sobolev constant rho_eff ---")
    print("  rho_eff = 2 * KL / W_2^2   (from T_2: W_2^2 <= 2*KL/rho)")
    print()

    rho_values = []
    for N in range(2, 201):
        farr = farey_float(N)
        n = len(farr)
        gaps = np.diff(farr)
        kl = sum(g * log(g * (n - 1)) for g in gaps if g > 0)
        W2sq = compute_W2_squared(farr)
        if W2sq > 1e-20:
            rho_eff = 2 * kl / W2sq
            rho_values.append((N, rho_eff, kl, W2sq))

    print(f"{'N':>4}  {'rho_eff':>12}  {'KL':>12}  {'W_2^2':>12}")
    print("-" * 50)
    for N, rho, kl, w2 in rho_values:
        if N <= 20 or N in [30, 50, 100, 150, 200]:
            print(f"{N:>4}  {rho:>12.4f}  {kl:>12.6e}  {w2:>12.6e}")

    rhos = [r[1] for r in rho_values]
    print(f"\nrho_eff range: [{min(rhos):.4f}, {max(rhos):.4f}]")
    print(f"For reference: pi^2 = {pi**2:.4f}")
    if min(rhos) > 0:
        print(f"T_2 bound is: W_2^2 <= {2/min(rhos):.6f} * KL")


# ── PART 5: Displacement interpolation perspective ────────────────────────

def part5_displacement_interpolation():
    """
    Use the displacement interpolation viewpoint.

    When inserting p-1 new fractions k/p into F_{p-1}, we can view this as:
    - Old measure: mu_{p-1} supported on n points
    - New measure: mu_p supported on n' = n + (p-1) points

    The "splitting" operation:
    Each gap (f_j, f_{j+1}) in F_{p-1} receives some number of new points k/p.
    This is like a local refinement of the measure.

    Key quantity: for each gap, how many new points fall in?
    By Farey properties, each gap (a/b, c/d) with ad-bc=-1
    receives at most 1 new fraction k/p (when p = b+d, the mediant).
    But for general p, the distribution is more complex.

    We compute:
    - Number of new points per gap
    - Their positioning within each gap
    - The "local W_2" contribution from each gap
    """
    print("\n" + "=" * 70)
    print("PART 5: Displacement Interpolation / Gap Refinement")
    print("=" * 70)
    print()

    for p in [5, 7, 11, 13, 17, 23, 29, 37, 47, 59, 67, 79, 97]:
        f_old = farey_float(p - 1)
        f_new = farey_float(p)
        n_old, n_new = len(f_old), len(f_new)

        # New fractions
        new_vals = set()
        for k in range(1, p):
            new_vals.add(k / p)

        # Count new points per gap
        gap_counts = []
        for i in range(len(f_old) - 1):
            lo, hi = f_old[i], f_old[i + 1]
            count = sum(1 for v in new_vals if lo < v < hi)
            gap_counts.append(count)

        gap_sizes = np.diff(f_old)
        counts = np.array(gap_counts)

        # Statistics
        total_new = sum(counts)
        assert total_new == p - 1, f"Expected {p-1} new, got {total_new}"

        max_count = max(counts)
        avg_count = np.mean(counts)
        empty_gaps = sum(1 for c in counts if c == 0)

        # Local W_2 contribution: for each gap, compute displacement cost
        # of new points from their "ideal" positions
        W2_old = compute_W2_squared(f_old)
        W2_new = compute_W2_squared(f_new)
        delta = W2_new - W2_old

        print(f"p={p:>3}: {total_new:>3} new pts in {n_old-1:>5} gaps, "
              f"max/gap={max_count}, avg={avg_count:.2f}, "
              f"empty={empty_gaps:>4} ({100*empty_gaps/(n_old-1):.1f}%), "
              f"dW2={delta:.2e}")


# ── PART 6: Quantile function approach ────────────────────────────────────

def part6_quantile_approach():
    """
    W_2^2 between two measures on R can be computed via quantile functions:
      W_2^2(mu, nu) = integral_0^1 |F_mu^{-1}(t) - F_nu^{-1}(t)|^2 dt

    For discrete measures, quantile functions are step functions.
    - F_Farey^{-1}(t) = f_j when (j-1)/n < t <= j/n
    - F_uniform^{-1}(t) = t (identity)

    So W_2^2 = integral_0^1 |F_Farey^{-1}(t) - t|^2 dt
             = sum_{j=0}^{n-1} integral_{j/n}^{(j+1)/n} (f_j - t)^2 dt

    This integral form may be better for proving monotonicity!
    Each term: integral_{j/n}^{(j+1)/n} (f_j - t)^2 dt
             = (f_j - j/n)^2 / n - (f_j - j/n)/n^2 + 1/(3n^3)

    So W_2^2(continuous) = W(N)/n^2 - S1/(n^2) + 1/(3n^2)
    where S1 = sum (f_j - j/n)
    """
    print("\n" + "=" * 70)
    print("PART 6: Quantile Function / Continuous W_2^2")
    print("=" * 70)
    print()

    print("Comparing discrete W_2^2 = W/n vs continuous W_2^2 via quantile integral")
    print()
    print(f"{'N':>4}  {'n':>6}  {'W2_discrete':>14}  {'W2_continuous':>14}  "
          f"{'diff':>12}  {'W2c mono':>8}")
    print("-" * 70)

    prev_w2c = None
    w2c_violations = 0
    results = []

    for N in range(2, 201):
        farr = farey_float(N)
        n = len(farr)

        # Discrete W_2^2
        ideal = np.arange(n) / n
        W2_disc = np.mean((farr - ideal) ** 2)

        # Continuous W_2^2 via quantile integral
        # integral_0^1 (Q(t) - t)^2 dt where Q is step function
        W2_cont = 0.0
        for j in range(n):
            fj = farr[j]
            lo = j / n
            hi = (j + 1) / n
            # integral_{lo}^{hi} (fj - t)^2 dt = [(fj-t)^3 / (-3)]_{lo}^{hi}
            # = (1/3) * [(fj - lo)^3 - (fj - hi)^3]
            W2_cont += ((fj - lo) ** 3 - (fj - hi) ** 3) / 3

        diff = W2_cont - W2_disc

        mono = ""
        if prev_w2c is not None:
            if W2_cont > prev_w2c:
                mono = "NO"
                w2c_violations += 1
            else:
                mono = "yes"
        prev_w2c = W2_cont

        results.append((N, n, W2_disc, W2_cont))

        if N <= 30 or is_prime(N) or N % 20 == 0:
            print(f"{N:>4}  {n:>6}  {W2_disc:>14.10f}  {W2_cont:>14.10f}  "
                  f"{diff:>12.4e}  {mono:>8}")

    print(f"\nContinuous W_2^2 monotonicity violations: {w2c_violations}")

    # Check the relationship
    print("\nRelationship: W2_cont = W2_disc - S1/n^2 + 1/(3n^2)")
    print("where S1 = sum(f_j - j/n)")
    for N in [5, 10, 20, 50, 100]:
        farr = farey_float(N)
        n = len(farr)
        ideal = np.arange(n) / n
        S1 = np.sum(farr - ideal)
        W2_disc = np.mean((farr - ideal) ** 2)
        W2_pred = W2_disc - S1 / n**2 + 1 / (3 * n**2)
        W2_cont = results[N - 2][3]
        print(f"  N={N:>3}: S1={S1:.6e}, W2_cont_pred={W2_pred:.10f}, "
              f"W2_cont_actual={W2_cont:.10f}, match={abs(W2_pred-W2_cont)<1e-12}")


# ── PART 7: Entropy-transport duality ─────────────────────────────────────

def part7_entropy_transport():
    """
    The Kantorovich dual of W_2^2 relates to the Legendre transform of
    the entropy functional.

    For W_2^2(mu_Farey, mu_uniform):
    The dual gives: W_2^2 = sup_{phi,psi} { integral phi d_mu + integral psi d_nu }
    subject to phi(x) + psi(y) <= |x-y|^2

    For 1D sorted measures, the optimal phi and psi are related to the
    cumulative distribution functions.

    Key insight: The Kantorovich potential phi(f_j) = 2*(j/n - f_j) tells us
    the "force" that would push each Farey fraction to its ideal position.
    """
    print("\n" + "=" * 70)
    print("PART 7: Kantorovich Potential Analysis")
    print("=" * 70)
    print()

    for N in [10, 20, 50, 100]:
        farr = farey_float(N)
        n = len(farr)
        ideal = np.arange(n) / n

        # Kantorovich potential: phi(f_j) = 2*(j/n - f_j)
        # This is the gradient of the transport map T(x) = x + displacement
        potentials = 2 * (ideal - farr)

        # Statistics
        print(f"N = {N}:")
        print(f"  |potentials|: mean={np.mean(np.abs(potentials)):.6e}, "
              f"max={np.max(np.abs(potentials)):.6e}, "
              f"std={np.std(potentials):.6e}")

        # Potential at Farey neighbors of mediants
        # The potential should be smooth if transport is optimal
        pot_diff = np.diff(potentials)
        print(f"  |d(potential)|: mean={np.mean(np.abs(pot_diff)):.6e}, "
              f"max={np.max(np.abs(pot_diff)):.6e}")

        # Total transport cost = (1/2) sum phi_j * (f_j - j/n) ... no
        # Actually W_2^2 = sum (f_j - j/n)^2 / n
        # = -(1/2n) sum phi_j * (f_j - j/n)  ... let's verify
        check = -0.5 * np.mean(potentials * (farr - ideal))
        W2 = np.mean((farr - ideal) ** 2)
        print(f"  W_2^2 = {W2:.10e}, check via potential = {check:.10e}, "
              f"match = {abs(check - W2) < 1e-14}")
        print()

    # How does the potential change when adding a prime?
    print("--- Potential change when adding prime p ---")
    print()
    for p in [7, 11, 23, 47, 97]:
        f_old = farey_float(p - 1)
        f_new = farey_float(p)
        n_old, n_new = len(f_old), len(f_new)

        pot_old = 2 * (np.arange(n_old) / n_old - f_old)
        pot_new = 2 * (np.arange(n_new) / n_new - f_new)

        print(f"p={p:>3}: pot_old range [{min(pot_old):.4e}, {max(pot_old):.4e}], "
              f"pot_new range [{min(pot_new):.4e}, {max(pot_new):.4e}]")
        print(f"       |pot| mean: old={np.mean(np.abs(pot_old)):.4e}, "
              f"new={np.mean(np.abs(pot_new)):.4e}, "
              f"ratio={np.mean(np.abs(pot_new))/np.mean(np.abs(pot_old)):.6f}")


# ── MAIN ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("WASSERSTEIN OPTIMAL TRANSPORT APPROACH TO W(N) MONOTONICITY")
    print("=" * 70)
    print()

    results1 = part1_w2_vs_N()
    part2_triangle_inequality()
    results3 = part3_kl_divergence()
    part4_talagrand_bound()
    part5_displacement_interpolation()
    part6_quantile_approach()
    part7_entropy_transport()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Key quantities computed:")
    print("  1. W_2^2(Farey, uniform) for N=2..200 -- monotonicity checked")
    print("  2. Triangle inequality decomposition at each prime")
    print("  3. KL divergence of gap distributions -- Talagrand T_2 applicability")
    print("  4. Effective log-Sobolev constant rho_eff")
    print("  5. Gap refinement statistics (displacement interpolation view)")
    print("  6. Continuous W_2^2 via quantile function integral")
    print("  7. Kantorovich potential analysis")
    print()
    print("NEXT STEPS for proof:")
    print("  - If W_2^2 is NOT monotone but W(N) IS, the scaling n matters")
    print("  - KL divergence bound via T_2 could give W_2 decay rate")
    print("  - Quantile integral form may enable induction on N")
    print("  - Kantorovich potential smoothness constrains transport cost")
