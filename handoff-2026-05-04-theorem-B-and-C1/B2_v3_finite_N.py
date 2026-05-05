#!/usr/bin/env python3
"""B2 v3 — finite-N stability check at N=500, 1000.

Verifies α_ratio → 1 with smaller variance at larger N.
Cf. v2 used N=250.
"""
import numpy as np, time, sys
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

I_ON, _ = quad(lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2), -500, 500, limit=800)
print(f"I_ON = ∫|M_W|²(1−sinc²) dy = {I_ON:.6f}")
print()

rng = np.random.default_rng(31337)
kappa_vals = [30.0, 39.48, 50.0, 70.0]   # 4 anchors; per-N stats fewer to keep time bounded

configs = [
    (500, 300),
    (1000, 150),
]

t0 = time.time()
results = {}
for N, n_samples in configs:
    print(f"=== N={N}, samples per κ={n_samples} ===", flush=True)
    print(f"{'κ':>7} {'Var(S)':>10} {'α_ratio':>10} {'SE_α':>8}")
    alphas = []
    ses = []
    for kappa in kappa_vals:
        S_vals = np.empty(n_samples, dtype=complex)
        for k in range(n_samples):
            ang = cue_eigenangles(N, rng)
            i_idx = N//2
            S_vals[k] = compute_S_bulk(ang, i_idx, kappa)
        E_S = np.mean(S_vals)
        E_abs2 = np.mean(np.abs(S_vals)**2)
        Var_S = E_abs2 - abs(E_S)**2
        SE_var = np.std(np.abs(S_vals)**2)/np.sqrt(n_samples)
        alpha = Var_S / I_ON
        SE_alpha = SE_var / I_ON
        alphas.append(alpha)
        ses.append(SE_alpha)
        print(f"{kappa:>7.2f} {Var_S:>10.4f} {alpha:>10.4f} {SE_alpha:>8.4f}", flush=True)
    mean_a = np.mean(alphas)
    sem_a = np.std(alphas)/np.sqrt(len(alphas))
    print(f"  → mean α = {mean_a:.4f} ± {sem_a:.4f} (across κ)")
    results[N] = (mean_a, sem_a, alphas, ses)
    print(f"  elapsed: {time.time()-t0:.1f}s\n", flush=True)

print("=== Summary: finite-N convergence ===")
for N, (m, s, _, _) in results.items():
    print(f"  N={N:>5}:  α = {m:.4f} ± {s:.4f}")
print()
print("Prediction: α → 1 with shrinking variance as N grows.")
