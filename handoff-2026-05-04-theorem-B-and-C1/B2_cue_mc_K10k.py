#!/usr/bin/env python3
"""B2 Q5 falsifier #3 EXTENDED — CUE MC for R_neigh at K=10², 10³, 10⁴.
Predicted asymptotic ratio ON/OFF → 2.3147 = ∫|M_W(iy)|²(1−sinc²(πy))dy / ∫(1−sinc²(πy))dy
(both integrals → bulk CUE Dyson sin-kernel pair correlation in N→∞ limit)."""
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

def compute_S(angles, idx, K, mollifier_on=True):
    diffs = angles - angles[idx]
    log_K = np.log(K)
    # vectorized
    mask = np.arange(len(angles)) != idx
    d = diffs[mask]
    phase = np.exp(1j * log_K * d)
    if mollifier_on:
        mw = MW(d)
    else:
        mw = np.ones_like(d, dtype=complex)
    return np.sum(phase * mw)

def main():
    rng = np.random.default_rng(42)
    out = ["# B2 Q5 #3 — CUE MC R_neigh, K=10², 10³, 10⁴",
           "# predicted asymptotic ratio ON/OFF → 2.3147",
           "# K | N | samples | E|S|²_ON | E|S|²_OFF | ratio | dt"]
    for K in [100, 1000, 10000]:
        N = max(80, int(np.log(K) * 50))  # density 50/log K
        N_samples = 100 if K >= 10000 else 200
        on_vals, off_vals = [], []
        t0 = time.time()
        for _ in range(N_samples):
            ang = cue_eigenangles(N, rng)
            i_idx = N//2
            on_vals.append(abs(compute_S(ang, i_idx, K, True))**2)
            off_vals.append(abs(compute_S(ang, i_idx, K, False))**2)
        on_m = np.mean(on_vals); off_m = np.mean(off_vals)
        ratio = on_m/off_m if off_m > 0 else float('nan')
        # std error
        on_se = np.std(on_vals)/np.sqrt(N_samples)
        off_se = np.std(off_vals)/np.sqrt(N_samples)
        dt = time.time() - t0
        line = f"K={K} N={N} samples={N_samples} ON={on_m:.3f}±{on_se:.3f} OFF={off_m:.3f}±{off_se:.3f} ratio={ratio:.4f} dt={dt:.0f}s"
        print(line, flush=True)
        out.append(line)
    open("/Users/saar/Farey 4.7 solutions/B2_cue_mc_K10k_results.md","w").write("\n".join(out)+"\n")

if __name__ == "__main__":
    main()
