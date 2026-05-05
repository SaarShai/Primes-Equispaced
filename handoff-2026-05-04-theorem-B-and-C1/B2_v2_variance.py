#!/usr/bin/env python3
"""B2 v2 — VARIANCE (not raw second moment) of S vs theory.

Insight: at κ=0, S = Σ M_W(iy_j) has a NON-ZERO mean (= ∫M_W(iy)·ρ_Palm(y) dy),
so E|S|² = Var(S) + |E S|². The Palm second-moment kernel ∫|φ|²(1-sinc²(πy))dy
gives the VARIANCE Var(S) (the connected 2-point cumulant), not E|S|².

So the correct test is:
  Var(S) → ∫|M_W(iy)|²·(1-sinc²(πy)) dy = 2.3147 = α_ratio · I_ON
with α_ratio = 1.

For κ ≠ 0, e^{iκy}·M_W(iy) is oscillatory, so its mean ∫M_W(iy)e^{iκy}dy → 0
as κ→∞ (Riemann-Lebesgue), leaving E|S|² = Var(S) → ∫|M_W|²(1-sinc²)dy.
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
    N = len(angles)
    diffs = angles - angles[idx]
    mask = np.arange(N) != idx
    d = diffs[mask]
    y = N * d / (2*np.pi)
    return np.sum(MW(y) * np.exp(1j * kappa * y))

I_ON, _ = quad(lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2), -300, 300, limit=600)
print(f"Theoretical I_ON = ∫|M_W|²(1-sinc²) dy = {I_ON:.6f}")
print()

# Mean of M_W under Palm: note Palm density at y=0 is 0 (the y_i is excluded).
# But ⟨S⟩ = N · E[M_W(iy_*)·e^{iκy_*}] for a uniform random y_* (away from y_i).
# In bulk: density of remaining N-1 points at scale y = N·θ/(2π) is uniform = 1
# (per unit y), modified by the sine-kernel hole around y=0.
# So E[S] = ∫_(-∞)^∞ M_W(iy)·e^{iκy} · (1 - sinc²(πy)) dy (Palm mean)
print("Theoretical E[S] under bulk Palm:")
for kappa in [0.0, 0.5, 1.0, 2.0, 5.0]:
    re_part, _ = quad(
        lambda y: (MW(y) * np.exp(1j*kappa*y) * (1 - np.sinc(y)**2)).real,
        -100, 100, limit=400)
    im_part, _ = quad(
        lambda y: (MW(y) * np.exp(1j*kappa*y) * (1 - np.sinc(y)**2)).imag,
        -100, 100, limit=400)
    mean_S = re_part + 1j*im_part
    print(f"  κ={kappa}: E[S] = {mean_S:.4f}, |E[S]|² = {abs(mean_S)**2:.4f}")

print()
print("="*60)
print("Test: Var(S) should match ∫|M_W|²(1-sinc²) for any κ")
print("="*60)

rng = np.random.default_rng(31415)
print(f"\n{'N':>4} {'κ':>5} {'E|S|²':>10} {'|E[S]|²':>10} {'Var(S)':>10} {'Var/I_ON':>10}")
for kappa in [0.0, 0.5, 1.0, 2.0, 5.0]:
    for N in [200, 400]:
        n_samples = 400
        S_vals = []
        t0 = time.time()
        for _ in range(n_samples):
            ang = cue_eigenangles(N, rng)
            i_idx = N//2
            S_vals.append(compute_S_bulk(ang, i_idx, kappa))
        S_arr = np.array(S_vals)
        E_S = np.mean(S_arr)
        E_abs2 = np.mean(np.abs(S_arr)**2)
        Var_S = E_abs2 - abs(E_S)**2
        ratio = Var_S / I_ON
        print(f"{N:>4} {kappa:>5} {E_abs2:>10.4f} {abs(E_S)**2:>10.4f} "
              f"{Var_S:>10.4f} {ratio:>10.4f}")
