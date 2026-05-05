#!/usr/bin/env python3
"""B2 v2 — high-precision pin of α_ratio at physical κ = (2π)²."""
import numpy as np, time
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
print(f"I_ON = ∫|M_W|²(1−sinc²) dy = {I_ON:.6f}")
print()

# Average across multiple κ's near (2π)² with high stats — to suppress oscillation
rng = np.random.default_rng(2026)
kappa_vals = [30.0, 35.0, 39.48, 45.0, 50.0, 55.0, 60.0, 70.0, 80.0]
N = 250
n_samples = 800

print(f"N={N}, samples={n_samples}, κ scan:")
print(f"{'κ':>7} {'Var(S)':>10} {'α_ratio':>10} {'SE':>8}")
all_vars = []
for kappa in kappa_vals:
    S_vals = []
    for _ in range(n_samples):
        ang = cue_eigenangles(N, rng)
        i_idx = N//2
        S_vals.append(compute_S_bulk(ang, i_idx, kappa))
    S_arr = np.array(S_vals)
    E_S = np.mean(S_arr)
    E_abs2 = np.mean(np.abs(S_arr)**2)
    Var_S = E_abs2 - abs(E_S)**2
    SE = np.std(np.abs(S_arr)**2)/np.sqrt(n_samples)
    alpha = Var_S / I_ON
    all_vars.append(Var_S)
    print(f"{kappa:>7.2f} {Var_S:>10.4f} {alpha:>10.4f} {SE:>8.4f}", flush=True)

# Mean α_ratio across κ scan
mean_var = np.mean(all_vars)
std_var = np.std(all_vars)/np.sqrt(len(all_vars))
mean_alpha = mean_var / I_ON
print()
print(f"Mean over κ scan: Var(S) = {mean_var:.4f} ± {std_var:.4f}")
print(f"Mean α_ratio    = {mean_alpha:.4f} ± {std_var/I_ON:.4f}")
print()
print(f"PREDICTION: α_ratio = 1 (orthogonal mult 1, universal CUE bulk)")
print(f"DEVIATION:  {abs(mean_alpha - 1.0):.4f} (σ-units: {abs(mean_alpha-1.0)/(std_var/I_ON):.2f})")
