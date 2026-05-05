#!/usr/bin/env python3
"""κ=0 finite-N convergence check.

Predicted Var_Palm(S; κ=0) = 0.2315 from Bourgade-Nikeghbali Palm-Soshnikov.
MC at N=250 gave 0.1397 — significant finite-size deviation.
Run N=500, 1000 to test convergence to 0.2315.
"""
import numpy as np, time

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

def compute_S(angles, idx, kappa):
    N = len(angles)
    diffs = angles - angles[idx]
    mask = np.arange(N) != idx
    d = diffs[mask]
    y = N * d / (2*np.pi)
    return np.sum(MW(y) * np.exp(1j * kappa * y))

PRED_KAPPA0 = 0.2315

rng = np.random.default_rng(7777)
print(f"PREDICTED Var_Palm at κ=0 = {PRED_KAPPA0:.4f}")
print(f"{'N':>5} {'samples':>8} {'E|S|²':>10} {'Var(S)':>10} {'ratio':>8} {'time(s)':>8}")
for N, n in [(250, 800), (500, 400), (1000, 150)]:
    t0 = time.time()
    S = np.empty(n, dtype=complex)
    for k in range(n):
        ang = cue_eigenangles(N, rng)
        S[k] = compute_S(ang, N//2, 0.0)
    Var = np.mean(np.abs(S)**2) - abs(np.mean(S))**2
    print(f"{N:>5} {n:>8} {np.mean(np.abs(S)**2):>10.4f} {Var:>10.4f} {Var/PRED_KAPPA0:>8.4f} {time.time()-t0:>8.1f}", flush=True)
