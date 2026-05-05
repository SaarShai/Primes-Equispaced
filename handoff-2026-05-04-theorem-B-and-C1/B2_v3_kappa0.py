#!/usr/bin/env python3
"""B2 v3 — κ=0 cross-validation MC.

At κ=0, the K^{iy} weight is 1; M_W is the bare mollifier.
Var_Palm(Σ M_W(iy_j)) should still equal I_ON if α_ratio = 1
universally (CUE Palm Plancherel, Soshnikov 2000 Thm 1).

The κ=0 falsifier differs from κ>>1 falsifier in that the
sinc-cross-correlation term:
   ∫ M_W(iy) sinc(πy) dy
is NOT killed by oscillation. We compute that term separately and
check the prediction:

   Var_Palm(S) = ∫|M_W|²(1−sinc²) dy   (Soshnikov closed form)

This is a tighter test than κ>>1 because at κ=0 the sinc²-correction
is at full strength, so the predicted variance and the naive ∫|f|²
differ substantially:

   ∫|M_W|² dy   (no Palm correction)
   ∫|M_W|²(1−sinc²) dy = I_ON  (Palm-corrected)

If MC matches I_ON (and not the larger ∫|M_W|²), Soshnikov is confirmed.
"""
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

def compute_S(angles, idx, kappa):
    N = len(angles)
    diffs = angles - angles[idx]
    mask = np.arange(N) != idx
    d = diffs[mask]
    y = N * d / (2*np.pi)
    return np.sum(MW(y) * np.exp(1j * kappa * y))

I_full, _  = quad(lambda y: abs(MW(y))**2,                    -500, 500, limit=800)
I_ON,   _  = quad(lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2), -500, 500, limit=800)
mean_F, _r = quad(lambda y: MW(y).real,                       -500, 500, limit=800)
mean_Fi,_i = quad(lambda y: MW(y).imag,                       -500, 500, limit=800)
mean_F = complex(mean_F, mean_Fi)
print(f"∫|M_W|²            = {I_full:.6f}   (Soshnikov NAIVE — no Palm)")
print(f"∫|M_W|²(1−sinc²)   = {I_ON:.6f}   (Soshnikov w/ Palm — predicted Var)")
print(f"∫M_W(iy) dy        = {mean_F}        (used for E[S] subtraction)")
print()

rng = np.random.default_rng(42)
N_vals = [250, 500]
n_samples = 500
kappa = 0.0

print(f"κ = {kappa},  samples = {n_samples}")
print(f"{'N':>5} {'E[S]':>22} {'E|S|²':>12} {'Var(S)':>10} {'α_full':>9} {'α_Palm':>9}")

t0 = time.time()
for N in N_vals:
    S_vals = np.empty(n_samples, dtype=complex)
    for k in range(n_samples):
        ang = cue_eigenangles(N, rng)
        i_idx = N//2
        S_vals[k] = compute_S(ang, i_idx, kappa)
    E_S = np.mean(S_vals)
    E_abs2 = np.mean(np.abs(S_vals)**2)
    Var_S = E_abs2 - abs(E_S)**2
    a_full = Var_S / I_full   # ratio vs naive (no Palm)
    a_palm = Var_S / I_ON     # ratio vs Soshnikov-Palm prediction
    SE = np.std(np.abs(S_vals)**2)/np.sqrt(n_samples)
    print(f"{N:>5}  {str(np.round(E_S,3)):>20}  {E_abs2:>10.4f} {Var_S:>10.4f} {a_full:>9.4f} {a_palm:>9.4f}",
          flush=True)
    print(f"        SE(E|S|²) = {SE:.4f}    elapsed: {time.time()-t0:.1f}s")

print()
print("Prediction: α_Palm ≈ 1.0 (Soshnikov w/ Palm), α_full < 1 (sinc² eats fraction).")
print(f"Sinc² correction fraction = (I_full − I_ON)/I_full = {(I_full-I_ON)/I_full:.4f}")
