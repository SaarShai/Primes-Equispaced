#!/usr/bin/env python3
"""B2 v2 — high-κ limit. With κ → ∞, Var(S) → ∫|M_W|²(1-sinc²)dy = I_ON."""
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
print(f"I_ON = {I_ON:.6f}")
print()
rng = np.random.default_rng(31415)

# Physical L↔CUE: κ = log K · 2π/N. If N = (log K)/(2π), then κ = (2π)² ≈ 39.48
print(f"{'N':>4} {'κ':>6} {'E|S|²':>10} {'|E[S]|²':>10} {'Var(S)':>10} {'α=Var/I_ON':>12}")
for kappa in [10.0, 20.0, 39.48, 80.0]:
    for N in [200, 400, 600]:
        n_samples = 300
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
        alpha_emp = Var_S / I_ON
        print(f"{N:>4} {kappa:>6.2f} {E_abs2:>10.4f} {abs(E_S)**2:>10.4f} "
              f"{Var_S:>10.4f} {alpha_emp:>12.4f}")
