#!/usr/bin/env python3
"""
Stern-Brocot and Calkin-Wilf per-level discrepancy computation.
Tests for spectral structure in DeltaW_SB(n) and DeltaW_CW(n).
"""

import numpy as np
from fractions import Fraction
from collections import deque
import time
import json

# ============================================================
# PART 1: Stern-Brocot Tree Generation
# ============================================================

def stern_brocot_levels(max_level):
    """
    Generate the Stern-Brocot tree level by level.
    Level 0: {1/1}
    Level n: mediants inserted between consecutive fractions from level n-1.

    Returns: list of sets, where levels[n] = set of fractions AT level n.
    Also returns cumulative sorted lists S_n.
    """
    # S_n contains all fractions at levels 0..n, sorted
    # We track the sorted sequence and insert mediants

    # Start: the "boundary" is 0/1 and 1/0 (infinity), with 1/1 at level 0
    # But we work with fractions in (0, infinity) — let's restrict to (0,1) for discrepancy
    # Actually, Stern-Brocot generates ALL positive rationals.
    # For discrepancy comparison with Farey, let's restrict to [0,1].
    # Fractions in [0,1] in the Stern-Brocot tree: left subtree gives (0,1), root is 1/1.

    # Alternative: generate the full tree and filter to [0,1].
    # More natural: generate the left half of the Stern-Brocot tree (fractions < 1)
    # plus 0/1 and 1/1 as boundaries.

    # Let's do it properly: generate ALL fractions in the SB tree up to level n,
    # then filter to [0,1] for discrepancy.

    # The SB tree: start with 0/1, 1/0 as sentinels.
    # Level 0: insert mediant(0/1, 1/0) = 1/1
    # Level 1: insert mediant(0/1, 1/1) = 1/2 and mediant(1/1, 1/0) = 2/1
    # etc.

    # For [0,1] restriction: we only need the LEFT subtree.
    # Left subtree: between 0/1 and 1/1.

    # Implementation: maintain sorted list of fractions in [0,1].
    # At each level, insert mediants between consecutive pairs.
    # But only NEW mediants (those not already present).

    # Actually, the SB tree has a clean structure: at level n,
    # the new fractions are exactly the mediants of consecutive fractions in S_{n-1}.
    # And these are always new (never duplicates) — that's a key property of SB.

    # Let's work with [0,1] inclusive.
    # S_0 = [0/1, 1/1]  (boundaries)
    # Actually, the user defined Level 0: {1/1}, Level 1: {1/2, 2/1}
    # Let me follow their convention but restrict to [0,1].

    # For the SB tree restricted to [0,1]:
    # We use 0/1 and 1/1 as fixed boundaries.
    # Level 1: mediant(0/1, 1/1) = 1/2
    # Level 2: mediant(0/1, 1/2) = 1/3, mediant(1/2, 1/1) = 2/3
    # Level 3: 1/4, 2/5, 3/5, 3/4
    # etc.

    # This gives us fractions in (0,1) at each level, plus boundaries 0 and 1.

    print("Generating Stern-Brocot tree levels (restricted to [0,1])...")

    # Store as (numerator, denominator) tuples for speed, use Fraction only when needed
    # sorted_fracs: list of (p,q) in sorted order (as fractions p/q)
    sorted_fracs = [(0, 1), (1, 1)]  # boundaries

    levels_new = [[(1, 1)]]  # level 0 contributes 1/1 (we treat 0/1 as boundary)
    # Actually let's say level 0 = {0/1, 1/1} as the initial sequence
    # and new fractions start at level 1.

    levels_new = [[(0,1), (1,1)]]  # level 0
    cumulative_counts = [2]

    all_fracs_sorted = [(0,1), (1,1)]  # S_0

    S_n_list = [list(all_fracs_sorted)]  # S_0

    for level in range(1, max_level + 1):
        t0 = time.time()
        new_fracs = []
        # Insert mediants between consecutive fractions
        for i in range(len(all_fracs_sorted) - 1):
            a, b = all_fracs_sorted[i], all_fracs_sorted[i+1]
            med = (a[0] + b[0], a[1] + b[1])
            new_fracs.append(med)

        # Merge new_fracs into all_fracs_sorted
        # new_fracs[i] goes between all_fracs_sorted[i] and all_fracs_sorted[i+1]
        merged = []
        for i in range(len(all_fracs_sorted) - 1):
            merged.append(all_fracs_sorted[i])
            merged.append(new_fracs[i])
        merged.append(all_fracs_sorted[-1])

        all_fracs_sorted = merged
        levels_new.append(new_fracs)
        cumulative_counts.append(len(all_fracs_sorted))
        S_n_list.append(list(all_fracs_sorted))

        dt = time.time() - t0
        print(f"  Level {level}: {len(new_fracs)} new fractions, "
              f"|S_{level}| = {len(all_fracs_sorted)}, time={dt:.2f}s")

    return S_n_list, levels_new, cumulative_counts


# ============================================================
# PART 2: Calkin-Wilf Tree Generation
# ============================================================

def calkin_wilf_levels(max_level):
    """
    Generate the Calkin-Wilf tree level by level, restricted to [0,1].

    The CW tree: root = 1/1
    Left child of p/q = p/(p+q)
    Right child of p/q = (p+q)/q

    For [0,1] restriction: only follow left children and left-of-center paths.
    Actually, let's generate all and filter.
    """
    print("\nGenerating Calkin-Wilf tree levels (restricted to [0,1])...")

    # Level 0: 1/1
    # Level 1: 1/2 (left child of 1/1), 2/1 (right child)
    # Level 2: 1/3, 3/2, 2/3, 3/1
    # For [0,1]: 1/3, 2/3

    # BFS generation
    current_level = [(1, 1)]
    all_fracs = set()
    all_fracs.add((1, 1))

    cw_levels_new = [[(1, 1)]]

    for level in range(1, max_level + 1):
        t0 = time.time()
        next_level = []
        for p, q in current_level:
            # Left child: p/(p+q)
            left = (p, p + q)
            # Right child: (p+q)/q
            right = (p + q, q)
            next_level.append(left)
            next_level.append(right)

        # Filter to [0,1]
        new_in_01 = [(p, q) for p, q in next_level if p <= q]
        for f in new_in_01:
            all_fracs.add(f)

        cw_levels_new.append(new_in_01)
        current_level = next_level

        dt = time.time() - t0
        print(f"  Level {level}: {len(new_in_01)} new fractions in [0,1], "
              f"cumulative = {len(all_fracs)}, time={dt:.2f}s")

    # Build cumulative sorted lists
    cumulative = set()
    cumulative.add((0, 1))  # add 0 as boundary
    cumulative.add((1, 1))  # add 1 as boundary

    S_n_list = []
    for level in range(max_level + 1):
        for f in cw_levels_new[level]:
            cumulative.add(f)
        sorted_list = sorted(cumulative, key=lambda x: x[0]/x[1])
        S_n_list.append(list(sorted_list))

    return S_n_list, cw_levels_new


# ============================================================
# PART 3: Discrepancy Computation
# ============================================================

def compute_discrepancy(S_n):
    """
    Compute W(S_n) = (1/N^2) * sum D(f)^2
    where D(f) = rank(f) - N * f, N = |S_n|, rank is 0-indexed position.

    S_n is a sorted list of (p,q) tuples.
    """
    N = len(S_n)
    if N == 0:
        return 0.0

    total = 0.0
    for rank, (p, q) in enumerate(S_n):
        f_val = p / q if q != 0 else float('inf')
        D = rank - N * f_val
        total += D * D

    return total / (N * N)


def compute_all_discrepancies(S_n_list):
    """Compute W_SB(n) for each level n."""
    W = []
    for n, S_n in enumerate(S_n_list):
        t0 = time.time()
        w = compute_discrepancy(S_n)
        dt = time.time() - t0
        W.append(w)
        if n <= 5 or n % 5 == 0:
            print(f"  W({n}) = {w:.10f}, |S_{n}| = {len(S_n)}, time={dt:.2f}s")
    return W


# ============================================================
# PART 4: Spectral Analysis
# ============================================================

def spectral_analysis(delta_W, name="SB"):
    """Compute periodogram of DeltaW sequence."""
    from numpy.fft import fft

    n = len(delta_W)
    if n < 4:
        return None, None

    # Remove mean
    dw = np.array(delta_W)
    dw_centered = dw - np.mean(dw)

    # FFT
    F = fft(dw_centered)
    power = np.abs(F[:n//2+1])**2
    freqs = np.arange(n//2+1) / n  # in cycles per level

    # Also compute in terms of "angular frequency" (radians per level)
    omega = 2 * np.pi * freqs

    return freqs, power, omega


# ============================================================
# MAIN
# ============================================================

def main():
    MAX_LEVEL = 22  # 2^22 ~ 4M fractions at deepest level; cumulative ~ 8M
    # Start conservative, go as high as feasible

    # Try up to level 22; bail if too slow
    try:
        # ---- Stern-Brocot ----
        print("=" * 60)
        print("STERN-BROCOT TREE DISCREPANCY")
        print("=" * 60)

        sb_S_n, sb_levels, sb_counts = stern_brocot_levels(MAX_LEVEL)

        print("\nComputing Stern-Brocot discrepancies...")
        W_sb = compute_all_discrepancies(sb_S_n)

        # DeltaW
        delta_W_sb = [W_sb[n] - W_sb[n-1] for n in range(1, len(W_sb))]

        print("\n--- Stern-Brocot DeltaW values ---")
        for n, dw in enumerate(delta_W_sb, 1):
            print(f"  DeltaW_SB({n}) = {dw:+.10f}")

        # Check oscillation
        signs = ['+' if dw > 0 else '-' for dw in delta_W_sb]
        sign_changes = sum(1 for i in range(1, len(signs)) if signs[i] != signs[i-1])
        print(f"\n  Sign pattern: {''.join(signs)}")
        print(f"  Sign changes: {sign_changes} out of {len(signs)-1} possible")
        oscillates_sb = sign_changes > len(signs) * 0.3
        print(f"  Oscillates? {'YES' if oscillates_sb else 'NO (monotone or weak oscillation)'}")

        # Spectral analysis
        if len(delta_W_sb) >= 6:
            freqs_sb, power_sb, omega_sb = spectral_analysis(delta_W_sb, "SB")

            print("\n--- Stern-Brocot Periodogram ---")
            if power_sb is not None:
                # Find dominant frequency
                # Skip DC (index 0)
                peak_idx = np.argmax(power_sb[1:]) + 1
                peak_freq = freqs_sb[peak_idx]
                peak_omega = omega_sb[peak_idx]
                peak_period = 1.0 / peak_freq if peak_freq > 0 else float('inf')

                print(f"  Peak frequency: {peak_freq:.6f} cycles/level")
                print(f"  Peak angular freq: {peak_omega:.6f} rad/level")
                print(f"  Peak period: {peak_period:.2f} levels")

                print("\n  Top 5 frequencies by power:")
                sorted_idx = np.argsort(power_sb[1:])[::-1] + 1
                for i, idx in enumerate(sorted_idx[:5]):
                    f = freqs_sb[idx]
                    p = power_sb[idx]
                    om = omega_sb[idx]
                    per = 1.0/f if f > 0 else float('inf')
                    print(f"    #{i+1}: freq={f:.6f}, omega={om:.4f}, period={per:.2f}, power={p:.6e}")

                # Compare with known spectral quantities
                print("\n--- Comparison with known spectral quantities ---")
                gamma_1 = 14.134725  # first zeta zero
                lambda_gauss = 0.3036630  # Mayer's eigenvalue
                log_inv_lambda = np.log(1.0 / lambda_gauss)  # ~1.19
                r_selberg = 9.5336  # sqrt(91.14 - 1/4)

                print(f"  Zeta zero gamma_1 = {gamma_1}")
                print(f"  Gauss map log(1/lambda_2) = {log_inv_lambda:.4f}")
                print(f"  Selberg r_1 = {r_selberg:.4f}")

                # Check if any peak matches
                # The natural comparison: does peak_omega / (2*pi) match any of these
                # Or does the period match?
                print(f"\n  Peak omega / (2*pi) = {peak_omega / (2*np.pi):.4f}")
                print(f"  Peak period in levels = {peak_period:.2f}")

                # Try: does DeltaW_SB have a component at frequency gamma_1/(2*pi*n) for some normalization?
                # With only ~20 data points, spectral resolution is limited.
                # Let's also look at the autocorrelation.

        # Autocorrelation
        print("\n--- Stern-Brocot DeltaW Autocorrelation ---")
        dw_arr = np.array(delta_W_sb)
        dw_c = dw_arr - np.mean(dw_arr)
        var = np.var(dw_arr)
        if var > 0:
            acf = np.correlate(dw_c, dw_c, mode='full')
            acf = acf[len(dw_c)-1:] / (var * len(dw_c))
            print(f"  lag 0: {acf[0]:.4f}")
            for lag in range(1, min(10, len(acf))):
                print(f"  lag {lag}: {acf[lag]:+.4f}")

        # ---- Calkin-Wilf ----
        print("\n" + "=" * 60)
        print("CALKIN-WILF TREE DISCREPANCY")
        print("=" * 60)

        cw_S_n, cw_levels = calkin_wilf_levels(MAX_LEVEL)

        print("\nComputing Calkin-Wilf discrepancies...")
        W_cw = compute_all_discrepancies(cw_S_n)

        delta_W_cw = [W_cw[n] - W_cw[n-1] for n in range(1, len(W_cw))]

        print("\n--- Calkin-Wilf DeltaW values ---")
        for n, dw in enumerate(delta_W_cw, 1):
            print(f"  DeltaW_CW({n}) = {dw:+.10f}")

        signs_cw = ['+' if dw > 0 else '-' for dw in delta_W_cw]
        sign_changes_cw = sum(1 for i in range(1, len(signs_cw)) if signs_cw[i] != signs_cw[i-1])
        print(f"\n  Sign pattern: {''.join(signs_cw)}")
        print(f"  Sign changes: {sign_changes_cw} out of {len(signs_cw)-1} possible")

        if len(delta_W_cw) >= 6:
            freqs_cw, power_cw, omega_cw = spectral_analysis(delta_W_cw, "CW")
            if power_cw is not None:
                peak_idx_cw = np.argmax(power_cw[1:]) + 1
                peak_freq_cw = freqs_cw[peak_idx_cw]
                peak_omega_cw = omega_cw[peak_idx_cw]
                peak_period_cw = 1.0 / peak_freq_cw if peak_freq_cw > 0 else float('inf')

                print(f"\n  Peak frequency: {peak_freq_cw:.6f} cycles/level")
                print(f"  Peak angular freq: {peak_omega_cw:.6f} rad/level")
                print(f"  Peak period: {peak_period_cw:.2f} levels")

        # ---- Comparison ----
        print("\n" + "=" * 60)
        print("COMPARISON: STERN-BROCOT vs CALKIN-WILF vs FAREY")
        print("=" * 60)

        # Correlation between DeltaW_SB and DeltaW_CW
        min_len = min(len(delta_W_sb), len(delta_W_cw))
        if min_len >= 3:
            corr = np.corrcoef(delta_W_sb[:min_len], delta_W_cw[:min_len])[0, 1]
            print(f"  Correlation(DeltaW_SB, DeltaW_CW) = {corr:.6f}")

        # Ratio of consecutive DeltaW values (looking for geometric decay)
        print("\n--- Ratio test (geometric decay?) ---")
        print("  Stern-Brocot DeltaW ratios:")
        for i in range(1, len(delta_W_sb)):
            if abs(delta_W_sb[i-1]) > 1e-15:
                ratio = delta_W_sb[i] / delta_W_sb[i-1]
                print(f"    DeltaW({i+1})/DeltaW({i}) = {ratio:+.6f}")

        print("  Calkin-Wilf DeltaW ratios:")
        for i in range(1, len(delta_W_cw)):
            if abs(delta_W_cw[i-1]) > 1e-15:
                ratio = delta_W_cw[i] / delta_W_cw[i-1]
                print(f"    DeltaW({i+1})/DeltaW({i}) = {ratio:+.6f}")

        # ---- Log-scale analysis ----
        print("\n--- Log-scale analysis ---")
        print("  Stern-Brocot |DeltaW| log-linear fit:")
        abs_dw_sb = [abs(d) for d in delta_W_sb if abs(d) > 1e-20]
        if len(abs_dw_sb) >= 3:
            x = np.arange(1, len(abs_dw_sb) + 1)
            log_dw = np.log(abs_dw_sb)
            # Linear fit: log|DeltaW| ~ a*n + b
            coeffs = np.polyfit(x, log_dw, 1)
            print(f"    log|DeltaW_SB| ~ {coeffs[0]:.4f}*n + {coeffs[1]:.4f}")
            print(f"    Decay rate: exp({coeffs[0]:.4f}) = {np.exp(coeffs[0]):.6f} per level")
            print(f"    Compare: Gauss map lambda_2 = 0.3037")
            print(f"    Compare: 1/4 = 0.2500")

        print("  Calkin-Wilf |DeltaW| log-linear fit:")
        abs_dw_cw = [abs(d) for d in delta_W_cw if abs(d) > 1e-20]
        if len(abs_dw_cw) >= 3:
            x = np.arange(1, len(abs_dw_cw) + 1)
            log_dw = np.log(abs_dw_cw)
            coeffs_cw = np.polyfit(x, log_dw, 1)
            print(f"    log|DeltaW_CW| ~ {coeffs_cw[0]:.4f}*n + {coeffs_cw[1]:.4f}")
            print(f"    Decay rate: exp({coeffs_cw[0]:.4f}) = {np.exp(coeffs_cw[0]):.6f} per level")

        # ---- Save all data ----
        results = {
            'W_sb': W_sb,
            'delta_W_sb': delta_W_sb,
            'W_cw': W_cw,
            'delta_W_cw': delta_W_cw,
            'sb_counts': sb_counts if 'sb_counts' in dir() else [len(s) for s in sb_S_n],
        }

        with open('/Users/saar/Desktop/Farey-Local/experiments/stern_brocot_data.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("\nData saved to stern_brocot_data.json")

    except MemoryError:
        print("\nMemoryError: reducing max level")
        raise
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()
