#!/usr/bin/env python3
"""Better B2 falsifier: mollifier-ON log K scaling test.

Theory (from Opus B2 derivation): with M_W ON,
  E_CUE[|R_neigh|² | θ_i fixed] ~ c_∞ · |Z'(θ_i)|²/Λ_K²

with `c_∞` constant in K (log K power = 0). Λ_K = log K + c_W ≈ log K.

So normalize: E[|S|²] / (log K)² should be CONSTANT across K, with value ≈ c_∞.

Compare K=10²,10³,10⁴: divide E[|S|²] by (log K)² and check stability.
Predicted c_∞ ≈ 2.31 if α_ratio = 1 (Opus's α_ratio coefficient TBD).
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

def compute_S_ON(angles, idx, K):
    diffs = angles - angles[idx]
    log_K = np.log(K)
    mask = np.arange(len(angles)) != idx
    d = diffs[mask]
    return np.sum(np.exp(1j * log_K * d) * MW(d))

def main():
    rng = np.random.default_rng(42)
    out = ["# B2 Better Falsifier — log K scaling with mollifier ON",
           "# theory: E[|S|²]/(log K)² should be ≈ constant ≈ c_∞ ≈ 2.31",
           "# K | N | samples | E[|S|²] | E[|S|²]/(log K)² | dt"]
    for K in [100, 300, 1000, 3000, 10000]:
        log_K = np.log(K)
        N = max(80, int(log_K * 50))
        N_samples = 200 if K < 5000 else 100
        S2 = []
        t0 = time.time()
        for _ in range(N_samples):
            ang = cue_eigenangles(N, rng)
            i = N//2
            S2.append(abs(compute_S_ON(ang, i, K))**2)
        S2_mean = np.mean(S2)
        S2_se = np.std(S2)/np.sqrt(N_samples)
        normalized = S2_mean / log_K**2
        dt = time.time() - t0
        line = f"K={K} N={N} samples={N_samples} E[|S|²]={S2_mean:.3f}±{S2_se:.3f} norm={normalized:.4f} dt={dt:.0f}s"
        print(line, flush=True)
        out.append(line)
    out.append("")
    out.append("# Predicted: norm should be K-independent at large K, value ≈ 2.31 (if α_ratio=1)")
    open("/Users/saar/Farey 4.7 solutions/B2_better_falsifier_results.md","w").write("\n".join(out)+"\n")

if __name__ == "__main__":
    main()
