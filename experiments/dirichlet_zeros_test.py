#!/usr/bin/env python3
"""
Farey Spectroscope: Twisted Dirichlet L-function Zero Detection (χ₄)
Tests: F_χ(γ) = |Σ_p χ(p)·R(p)·p^{-1/2-iγ}|²
Note: This is a COMPUTATIONAL heuristic. Finite prime sums do not constitute proof.
"""
import numpy as np
import pandas as pd
import mpmath
import os
import sys

# ----------------------------------------------------------------------------
# 1. LOAD & PREPROCESS DATA
# ----------------------------------------------------------------------------
CSV_PATH = os.path.expanduser("~/Desktop/Farey-Local/experiments/bc_verify_100000_c.csv")
if not os.path.exists(CSV_PATH):
    print(f"ERROR: CSV not found at {CSV_PATH}"); sys.exit(1)

df = pd.read_csv(CSV_PATH)
# Flexible column detection
p_col = next((c for c in ['p', 'prime', 'P'] if c in df.columns), None)
R_col = next((c for c in ['R', 'R_val', 'farey_R'] if c in df.columns), None)
if p_col is None or R_col is None:
    print("ERROR: CSV must contain columns for primes ('p') and Farey weights ('R')."); sys.exit(1)

p = df[p_col].values.astype(float)
R = df[R_col].values.astype(float)
p_int = p.astype(int)

# χ₄(p): 0 if p=2, +1 if p≡1 (mod 4), -1 if p≡3 (mod 4)
chi4 = np.where(p_int == 2, 0.0,
                np.where(p_int % 4 == 1, 1.0, -1.0))

mask = chi4 != 0
p, R, chi4 = p[mask], R[mask], chi4[mask]

# Precompute weights and logs
weights = chi4 * R * p**(-0.5)
log_p = np.log(p)

# ----------------------------------------------------------------------------
# 2. COMPUTE TWISTED SPECTRAL FUNCTION F_χ(γ)
# ----------------------------------------------------------------------------
gamma_vals = np.linspace(0, 10, 2000)
# Vectorized: Σ w_p * exp(-i γ log p)
exponent = np.outer(log_p, gamma_vals)
complex_sum = np.sum(weights[:, None] * np.exp(-1j * exponent), axis=0)
F_chi = np.abs(complex_sum)**2

# Peak detection (simple numpy implementation, no scipy dependency)
from scipy.signal import find_peaks
peaks, props = find_peaks(F_chi, height=np.percentile(F_chi, 90))
peak_gammas = gamma_vals[peaks]

# ----------------------------------------------------------------------------
# 3. HIGH-PRECISION L-FUNCTION ZERO COMPARISON (mpmath)
# ----------------------------------------------------------------------------
mpmath.mp.dps = 30

def L_chi4(s):
    return mpmath.dirichlet_beta(s)  # L(s, χ₄) = β(s)

# Refine first zero near 6.02 using phase-rotated real part crossing
def real_part_y(y):
    y_mp = mpmath.mpf(str(y))
    s = mpmath.mpc('0.5', y_mp)
    val = L_chi4(s)
    # Hardy Z-function equivalent: rotate to real axis on critical line
    theta = 0.5 * mpmath.mp.pi * 0.5  # Approx phase for χ₄; exact root finding is more robust via abs minimization
    return mpmath.re(val * mpmath.exp(-mpmath.j * theta))

# Safer: locate zero by minimizing |L(0.5+iy)|² on a fine grid, then refine
y_grid = np.linspace(5.5, 6.5, 200)
L_vals = [abs(L_chi4(mpmath.mpc('0.5', str(y)))) for y in y_grid]
y_min = y_grid[np.argmin(L_vals)]

# Refine with mpmath.findroot on |L|² derivative sign change or direct complex solve
# Here we use a bracketed real root finder on Re(L) for stability
zero_gamma = mpmath.findroot(real_part_y, y_min)
print(f"✓ mpmath refined first zero: γ = {zero_gamma}")

# ----------------------------------------------------------------------------
# 4. COMPARISON & OUTPUT
# ----------------------------------------------------------------------------
if len(peak_gammas) > 0:
    first_peak = peak_gammas[0]
    offset = abs(first_peak - float(zero_gamma))
    print(f"✓ Spectral peak 1: γ = {first_peak:.6f}")
    print(f"  Offset from true zero: {offset:.4e}")
else:
    print("✗ No significant peaks detected in [0, 10]. Check R(p) normalization or p_max.")

# ----------------------------------------------------------------------------
# ⚠️ CRITICAL MATHEMATICAL CAVEATS
# ----------------------------------------------------------------------------
print("\n--- MATHEMATICAL ASSESSMENT ---")
print("1. COMPUTATION ≠ PROOF: Peak correlation with L(s,χ₄) zeros is a numerical heuristic.")
print("   It does not prove the Farey spectrum encodes L-function zeros.")
print("2. TRUNCATION ERROR: The sum is cut at p_max ≈ 10⁵. By standard prime sum bounds,")
print("   the tail introduces O(N^{-1/2}) phase noise. No unconditional Walfisz-style")
print("   bound exists for twisted Farey sums.")
print("3. R(p) DEPENDENCE: If R(p) ≁ (log p)^(-1) or lacks explicit-formula kernel structure,")
print("   apparent peaks may be accidental or driven by prime density fluctuations.")
print("4. NO GRH ASSUMPTION: This test is unconditional. Conditional bounds were not invoked.")
