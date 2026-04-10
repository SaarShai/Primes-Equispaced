#!/usr/bin/env python3
"""
Effective Weil constants for the six-term cancellation.

Computes:
  Sigma(m, n) = sum_{t=0}^5 (E_{m+t}(n) - n^2 * I_{m+t})

for n = 100, 200, 500, 1000, 2000, 5000
and all admissible m = 6k+2 with m <= n/2.

Key questions:
1. What is max_m |Sigma(m,n)| / n^{3/2}?  (effective C_eff)
2. What is max_m |Sigma(m,n)| / n?  (if O(n), this should stabilize)
3. For fixed m, what is |Sigma(m,n)| / n?  (should be O(1) => O(n))

Also compute the Weil-type bound from the surviving Fourier harmonics
with explicit constants.
"""

import math
from fractions import Fraction

def E_r(r, n):
    """E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v)"""
    if n <= 0:
        return 0
    total = 0
    lo = n // 3
    hi = n // 2
    for v in range(lo + 1, hi + 1):
        rv_mod_n = (r * v) % n
        total += rv_mod_n - v
    return total

def B2(t):
    """Second Bernoulli polynomial B_2(t) = t^2 - t + 1/6"""
    return t*t - t + 1.0/6.0

def I_r(r):
    """Continuous main term I_r = integral_{1/3}^{1/2} ({rx} - x) dx
    = 1/72 + (B_2({r/2}) - B_2({r/3})) / (2r)
    """
    frac_r2 = (r / 2.0) - math.floor(r / 2.0)  # {r/2}
    frac_r3 = (r / 3.0) - math.floor(r / 3.0)  # {r/3}
    return 1.0/72.0 + (B2(frac_r2) - B2(frac_r3)) / (2.0 * r)

def I_r_exact(r):
    """Exact rational computation of I_r using Fraction"""
    frac_r2 = Fraction(r, 2) - (r // 2)
    frac_r3 = Fraction(r, 3) - (r // 3)
    B2_r2 = frac_r2**2 - frac_r2 + Fraction(1, 6)
    B2_r3 = frac_r3**2 - frac_r3 + Fraction(1, 6)
    return Fraction(1, 72) + (B2_r2 - B2_r3) / (2 * r)

def six_term_error(m, n):
    """Sigma(m, n) = sum_{t=0}^5 (E_{m+t}(n) - n^2 * I_{m+t})"""
    total = 0
    for t in range(6):
        r = m + t
        e = E_r(r, n)
        i = I_r(r)
        total += e - n * n * i
    return total

def six_term_error_exact(m, n):
    """Exact rational version"""
    total_E = 0
    total_I = Fraction(0)
    for t in range(6):
        r = m + t
        total_E += E_r(r, n)
        total_I += I_r_exact(r)
    return float(total_E - n * n * total_I)

# ============================================================
# MAIN COMPUTATION
# ============================================================

print("=" * 90)
print("SIX-TERM CANCELLATION: EFFECTIVE WEIL CONSTANTS")
print("=" * 90)

# ---- Part 1: Fixed small m, varying n ----
print("\n\n--- PART 1: Fixed m, varying n ---")
print("If |Sigma(m,n)| = C(m) * n + lower order, then |Sigma|/n should stabilize.\n")

test_n = [100, 200, 500, 1000, 2000, 5000]
test_m = [2, 8, 14, 20, 50]

print(f"{'m':>5} | ", end="")
for n in test_n:
    print(f"{'n='+str(n):>12}", end=" ")
print()
print("-" * 90)

fixed_m_data = {}
for m in test_m:
    row = []
    for n in test_n:
        if m + 5 > n:
            row.append(None)
            continue
        sig = six_term_error(m, n)
        row.append(sig)
    fixed_m_data[m] = row

    print(f"{m:>5} | ", end="")
    for i, n in enumerate(test_n):
        if row[i] is None:
            print(f"{'N/A':>12}", end=" ")
        else:
            ratio = row[i] / n
            print(f"{ratio:>12.4f}", end=" ")
    print("   (|Sigma|/n)")

print()
print("Checking convergence of |Sigma|/n for fixed m:")
for m in test_m:
    vals = [(test_n[i], fixed_m_data[m][i]) for i in range(len(test_n)) if fixed_m_data[m][i] is not None]
    if len(vals) >= 2:
        ratios = [abs(v)/n for n, v in vals]
        print(f"  m={m}: |Sigma|/n = {', '.join(f'{r:.4f}' for r in ratios)}")
        if len(ratios) >= 2:
            # Check if stabilizing (last two close)
            diff = abs(ratios[-1] - ratios[-2])
            print(f"         Last two differ by {diff:.6f} => {'STABILIZING' if diff < 0.5 else 'NOT YET STABLE'}")

# ---- Part 2: Max over m for each n ----
print("\n\n--- PART 2: Max |Sigma(m,n)| over all admissible m = 6k+2, m <= n/2 ---")
print("This determines the UNIFORM bound.\n")

print(f"{'n':>6} | {'max|Sig|':>12} {'max|Sig|/n':>12} {'max|Sig|/n^{3/2}':>16} {'worst_m':>8} {'sign':>6}")
print("-" * 70)

C_eff_values = {}
for n in test_n:
    max_abs_sig = 0
    worst_m = 0
    worst_sig = 0
    for k in range(0, n // 12 + 1):
        m = 6 * k + 2
        if m + 5 > n:
            break
        sig = six_term_error(m, n)
        if abs(sig) > max_abs_sig:
            max_abs_sig = abs(sig)
            worst_m = m
            worst_sig = sig

    ratio_n = max_abs_sig / n
    ratio_n32 = max_abs_sig / (n ** 1.5)
    sign = "+" if worst_sig > 0 else "-"
    C_eff_values[n] = ratio_n32
    print(f"{n:>6} | {max_abs_sig:>12.2f} {ratio_n:>12.4f} {ratio_n32:>16.6f} {worst_m:>8} {sign:>6}")

print("\nC_eff(n) = max|Sigma|/n^{3/2} values:")
for n in test_n:
    print(f"  n={n:>5}: C_eff = {C_eff_values[n]:.6f}")

# ---- Part 3: Detailed m-scan for n=1000 ----
print("\n\n--- PART 3: All m=6k+2 blocks for n=1000, sorted by |Sigma|/n ---")
n = 1000
all_blocks = []
for k in range(0, n // 12 + 1):
    m = 6 * k + 2
    if m + 5 > n:
        break
    sig = six_term_error(m, n)
    all_blocks.append((m, sig))

all_blocks.sort(key=lambda x: -abs(x[1]))
print(f"{'m':>6} {'Sigma':>12} {'|Sig|/n':>10} {'|Sig|/n^1.5':>12} {'|Sig|/(n*sqrt(m))':>18}")
print("-" * 70)
for m, sig in all_blocks[:20]:
    ratio_n = abs(sig) / n
    ratio_n32 = abs(sig) / (n ** 1.5)
    ratio_nsqrtm = abs(sig) / (n * math.sqrt(m)) if m > 0 else float('inf')
    print(f"{m:>6} {sig:>12.2f} {ratio_n:>10.4f} {ratio_n32:>12.6f} {ratio_nsqrtm:>18.6f}")

# ---- Part 4: Scaling test ----
print("\n\n--- PART 4: Scaling analysis for fixed m/n ratio ---")
print("Fix m = n/4 (rounded to nearest 6k+2). If |Sigma| ~ C*n*sqrt(m) ~ C*n^{3/2}/2,")
print("then |Sigma|/n^{3/2} should stabilize.\n")

print(f"{'n':>6} {'m':>6} {'Sigma':>14} {'|Sig|/n':>10} {'|Sig|/n^1.5':>12} {'|Sig|/(n*sqrt(m))':>18}")
print("-" * 80)
for n in test_n:
    target_m = n // 4
    k = max(0, (target_m - 2) // 6)
    m = 6 * k + 2
    if m + 5 > n:
        continue
    sig = six_term_error(m, n)
    ratio_n = abs(sig) / n
    ratio_n32 = abs(sig) / (n ** 1.5)
    ratio_nsqrtm = abs(sig) / (n * math.sqrt(m)) if m > 0 else 0
    print(f"{n:>6} {m:>6} {sig:>14.2f} {ratio_n:>10.4f} {ratio_n32:>12.6f} {ratio_nsqrtm:>18.6f}")

# ---- Part 5: Explicit Fourier bound computation ----
print("\n\n--- PART 5: Explicit Fourier bound via surviving harmonics ---")
print("After Ramanujan c_6(h) kills non-6|h harmonics, the surviving terms are h=6k.")
print("Bound: |Sigma_frac| <= (n/pi) * sum_{k=1}^M (1/k) * |inner_sum_k|")
print("where inner_sum_k = sum_{v in (n/3,n/2]} e^{2pi i * 6k * m * v / n}\n")

import cmath

def fourier_bound_explicit(m, n, M=None):
    """Compute the actual Fourier sum and compare with Weil-type bounds."""
    if M is None:
        M = n // 6

    # Actual exponential sum
    lo = n // 3
    hi = n // 2
    V = hi - lo  # number of terms

    actual_fourier_err = 0.0
    weil_bound_total = 0.0

    for k in range(1, M + 1):
        h = 6 * k
        # Compute inner sum: sum_{v=lo+1}^{hi} e^{2*pi*i*h*m*v/n}
        inner = 0.0 + 0.0j
        for v in range(lo + 1, hi + 1):
            inner += cmath.exp(2j * cmath.pi * h * m * v / n)
        inner_abs = abs(inner)
        actual_fourier_err += inner_abs / k

        # Weil bound for this harmonic: min(V, n / (2*|sin(pi*h*m/n)|))
        sin_val = abs(math.sin(math.pi * h * m / n))
        if sin_val > 1e-15:
            weil_single = min(V, n / (2.0 * sin_val))
        else:
            weil_single = V  # resonant case
        weil_bound_total += weil_single / k

    return actual_fourier_err, weil_bound_total, V

n = 1000
print(f"n = {n}, testing m = 2, 50, 200, 498:")
for m in [2, 50, 200, 498]:
    actual, weil, V = fourier_bound_explicit(m, n, M=min(100, n // 6))
    # The six-term error from Fourier is (n/pi) * actual (approximately)
    fourier_est = n / math.pi * actual
    print(f"  m={m:>4}: actual_sum={actual:>10.2f}, weil_bound={weil:>10.2f}, "
          f"n/pi*actual={fourier_est:>10.2f}, ratio(actual/weil)={actual/weil:.4f}")

# ---- Part 6: Positivity threshold ----
print("\n\n--- PART 6: Positivity threshold from effective constants ---")
print("Main term: n^2/12. Error: C_eff * n^{3/2}.")
print("Positivity when n^2/12 > C_eff * n^{3/2}, i.e., n > (12 * C_eff)^2.\n")

# Use conservative C_eff
C_max = max(C_eff_values.values())
print(f"Maximum C_eff observed: {C_max:.6f}")
print(f"Conservative C_eff (with 50% safety margin): {1.5 * C_max:.6f}")

N0_tight = (12 * C_max) ** 2
N0_safe = (12 * 1.5 * C_max) ** 2
print(f"Positivity threshold N_0 (tight):  n > {N0_tight:.1f}")
print(f"Positivity threshold N_0 (safe):   n > {N0_safe:.1f}")
print(f"Corresponding prime threshold P_0: p > {2 * N0_safe:.0f} (since n = p - m >= p/2)")

# ---- Part 7: Check for O(n) scaling at fixed m ----
print("\n\n--- PART 7: Definitive O(n) vs O(n^{3/2}) test ---")
print("For FIXED m: |Sigma(m,n)|/n should converge (O(n) scaling)")
print("For WORST-CASE m ~ n/2: |Sigma|/n grows, but |Sigma|/n^{3/2} should converge\n")

big_n_list = [200, 500, 1000, 2000, 5000]
print("Fixed m=2 (O(n) expected):")
for n in big_n_list:
    sig = six_term_error(2, n)
    print(f"  n={n:>5}: |Sigma|={abs(sig):>10.2f}, |Sigma|/n={abs(sig)/n:>8.4f}, |Sigma|/n^1.5={abs(sig)/n**1.5:>10.6f}")

print("\nFixed m=8:")
for n in big_n_list:
    sig = six_term_error(8, n)
    print(f"  n={n:>5}: |Sigma|={abs(sig):>10.2f}, |Sigma|/n={abs(sig)/n:>8.4f}")

print("\nFixed m=50:")
for n in big_n_list:
    if 55 > n:
        continue
    sig = six_term_error(50, n)
    print(f"  n={n:>5}: |Sigma|={abs(sig):>10.2f}, |Sigma|/n={abs(sig)/n:>8.4f}")

print("\nWorst-case m (near n/2):")
for n in big_n_list:
    max_abs = 0
    for k in range(0, n // 12 + 1):
        m = 6 * k + 2
        if m + 5 > n:
            break
        sig = six_term_error(m, n)
        if abs(sig) > max_abs:
            max_abs = abs(sig)
    print(f"  n={n:>5}: max|Sigma|={max_abs:>10.2f}, max/n={max_abs/n:>8.4f}, max/n^1.5={max_abs/n**1.5:>10.6f}")

print("\n\nDONE.")
