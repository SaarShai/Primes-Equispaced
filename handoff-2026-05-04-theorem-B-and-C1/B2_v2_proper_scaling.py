#!/usr/bin/env python3
"""B2 v2 — proper bulk-scaling MC.

Key fix: use the PROPER bulk-scaling sum so that the empirical answer →
∫|M_W(iy)|²·(1-sinc²(πy)) dy = 2.3147 directly.

In the bulk-scaling limit:
  S = Σ_{j≠i} M_W(i·y_j) · exp(i·κ·y_j)
  with y_j = N·(θ_j - θ_i)/(2π), κ = log K · 2π/N.

For the SUM (over j) to converge to the INTEGRAL ∫|M_W(iy)|²·(1-sinc²(πy))dy,
we need: E|S|² → ∫|M_W(iy)|²·ρ_pair^Palm(y) dy.

The Palm 2-point density at bulk scaling = 1 - sinc²(πy), with measure dy
(NOT dy/(2π/N)).  So if we compute Σ correctly with the y normalization,
E|S|² → I_ON only if κ = 0 (no oscillation) OR if the kernel kills the
oscillation. With κ ~ O(1), the oscillation phase modulates the integrand.

The PURE Palm-CUE kernel test (κ=0) gives α_ratio = 1 directly. With κ ≠ 0,
the answer is α_ratio = ∫|M_W(iy)|²·(1-sinc²(πy))·e^{... pair-correlation
re-weighting}... actually for the DIAGONAL (Plancherel) part of the second
moment, by CUE Palm formula:

  E[|Σ_{j≠i} φ(y_j)|² | θ_i] = ∫|φ(y)|²·(1-sinc²(πy)) dy + |∫φ(y) dy|²·(...corrections)

Setting φ(y) = M_W(iy)·exp(iκy), and noting ∫M_W(iy)·exp(iκy) dy is bounded
(it's a Fourier transform of a compactly-supported kernel), the leading
term IS ∫|M_W|²·(1-sinc²) dy = 2.3147. The κ dependence is in the SQUARE
TERM which is O(1) and bounded as K→∞.

So PREDICTION: with PROPER bulk normalization, E|S|² → 2.3147 and α_ratio = 1.
"""
import numpy as np
import time
from scipy.integrate import quad

def MW(y):
    w = 1j*y
    return (1 - np.exp(-1 - w))/(1 + w)

def cue_eigenangles(N, rng):
    G = rng.standard_normal((N, N))
    H = rng.standard_normal((N, N))
    M = (G + 1j*H)/np.sqrt(2)
    Q, R = np.linalg.qr(M)
    d = np.diag(R)
    Q = Q * (d/np.abs(d))
    return np.sort(np.angle(np.linalg.eigvals(Q)))

def compute_S_bulk(angles, idx, kappa):
    """S = Σ_{j≠i} M_W(i·y_j) · exp(i·kappa·y_j) with y_j = N·(θ_j - θ_i)/(2π)."""
    N = len(angles)
    diffs = angles - angles[idx]
    mask = np.arange(N) != idx
    d = diffs[mask]
    y = N * d / (2*np.pi)
    return np.sum(MW(y) * np.exp(1j * kappa * y))

# Theoretical integral
I_ON, _ = quad(lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2), -200, 200, limit=400)
print(f"Theoretical: ∫|M_W(iy)|²(1-sinc²(πy)) dy = {I_ON:.6f}")
print()

# Run with kappa = 0 (PURE Palm-CUE pair-correlation, no oscillation):
# this should converge directly to I_ON.
print("="*60)
print("Test A: κ = 0 (no oscillation, pure Palm 2-point)")
print("="*60)
print("Prediction: E|S|² → I_ON = 2.3147 (α_ratio = 1)")
print()
rng = np.random.default_rng(31415)
for N in [100, 200, 400]:
    n_samples = 500 if N < 300 else 200
    vals = []
    t0 = time.time()
    for _ in range(n_samples):
        ang = cue_eigenangles(N, rng)
        i_idx = N//2
        vals.append(abs(compute_S_bulk(ang, i_idx, 0.0))**2)
    m = np.mean(vals); se = np.std(vals)/np.sqrt(n_samples)
    dt = time.time() - t0
    alpha_emp = m / I_ON
    print(f"N={N:4d} samples={n_samples:3d} E|S|²={m:.4f}±{se:.4f} "
          f"α_emp={alpha_emp:.4f} dt={dt:.0f}s")

print()
print("="*60)
print("Test B: κ matched to L↔CUE physical scale")
print("="*60)
print("κ = log K · 2π/N → fix κ across N for stable bulk limit")
print()
# At κ = 0.1, 1.0, 5.0:
for kappa in [0.1, 1.0, 2.0, 5.0]:
    print(f"\nκ = {kappa}:")
    for N in [200, 400]:
        n_samples = 300
        vals = []
        for _ in range(n_samples):
            ang = cue_eigenangles(N, rng)
            i_idx = N//2
            vals.append(abs(compute_S_bulk(ang, i_idx, kappa))**2)
        m = np.mean(vals); se = np.std(vals)/np.sqrt(n_samples)
        # theory: ∫|M_W(iy)|² * (1 - sinc²(πy) * cos²(kappa*y/2)... actually just predict integrand
        # with kappa just shifts the M_W argument:  M_W(iy)·e^{iκy} so |...|² = |M_W(iy)|²
        I_theory, _ = quad(
            lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2),
            -200, 200, limit=400)
        # Plus the |∫ M_W(iy) e^{iκy} dy|² mean piece — for κ>0, F.T. of M_W
        # is supported in finite interval (M_W is finite-energy)
        alpha_emp = m / I_theory
        print(f"  N={N} E|S|²={m:.4f}±{se:.4f} α_emp={alpha_emp:.4f}")
