#!/usr/bin/env python3
"""B2 v2 — fast high-κ test."""
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

print(f"{'N':>4} {'κ':>6} {'samp':>5} {'E|S|²':>10} {'|EminS|²':>10} {'Var(S)':>10} {'α=Var/I_ON':>12} {'dt':>5}")
N = 250  # fixed N, focus on κ scan
for kappa in [10.0, 20.0, 39.48, 60.0, 100.0]:
    n_samples = 200
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
    dt = time.time() - t0
    print(f"{N:>4} {kappa:>6.2f} {n_samples:>5} {E_abs2:>10.4f} {abs(E_S)**2:>10.4f} "
          f"{Var_S:>10.4f} {alpha_emp:>12.4f} {dt:>4.0f}s", flush=True)
