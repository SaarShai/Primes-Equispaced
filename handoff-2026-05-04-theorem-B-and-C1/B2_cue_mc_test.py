#!/usr/bin/env python3
"""B2 Q5 falsifier #3 — CUE Monte Carlo for R_neigh with mollifier on/off.

Setup: CUE matrix size N. Eigenangles θ_1,...,θ_N. Pick a fixed pinned angle θ_i.
Compute R_neigh-like sum:
  S_K = Σ_{j ≠ i} K^{i(θ_j − θ_i)} · M_W(i(θ_j − θ_i))   (no Z' weighting first — simplest test)
where M_W(iy) = (1 − exp(-1-iy))/(1+iy).

Compare:
- E_CUE[|S_K|²]  with M_W as above (mollifier ON)
- E_CUE[|S_K|²]  with M_W ≡ 1 (mollifier OFF)

Expected (per Opus B2 derivation): with K^iy localizing on scale 1/log K,
  ON  ~ ∫|M_W(iy)|²·(1−sinc²(πy)) dy = 2.3147  (mpmath verified)
  OFF ~ ∫(1−sinc²(πy)) dy = 1   (Dyson sine-kernel pair correlation)
Ratio ON/OFF should be ≈ 2.31 if leading scaling is right.

Test at K = 100, 1000, 10000 (N matched: N ~ K, since N → ∞ limit).
Samples: 1000 per K. Local run, ≤5 min.
"""
import numpy as np
import time

def MW(y):
    """M_W(iy) = (1 - exp(-1 - iy))/(1+iy)"""
    w = 1j*y
    return (1 - np.exp(-1 - w))/(1 + w)

def cue_eigenangles(N, rng):
    """Sample eigenangles of an N×N CUE matrix (Haar-random unitary)."""
    # standard: A = (G + iH)/sqrt(2), QR decomp, eigenvalues of Q
    G = rng.standard_normal((N, N))
    H = rng.standard_normal((N, N))
    M = (G + 1j*H)/np.sqrt(2)
    Q, R = np.linalg.qr(M)
    # Adjust for QR sign convention: multiply Q by diag(R)/|diag(R)|
    d = np.diag(R)
    ph = d/np.abs(d)
    Q = Q * ph
    # eigenvalues of Q
    ev = np.linalg.eigvals(Q)
    angles = np.angle(ev)  # in (-pi, pi]
    return np.sort(angles)

def compute_S(angles, theta_i_idx, K, mollifier_on=True):
    """Compute S_K = Σ_{j≠i} K^{i(θ_j − θ_i)} · M_W(i(θ_j − θ_i))"""
    N = len(angles)
    diffs = angles - angles[theta_i_idx]  # length N, with one zero
    # focus on near-neighbors (within ±5 in index space — speed)
    # but theoretical formula sums over all j. for log-K localization,
    # main contribution from |Δθ| ~ 1/log K (i.e., few index neighbors)
    result = 0.0 + 0j
    for j in range(N):
        if j == theta_i_idx: continue
        d = diffs[j]
        # K^{id} = exp(i·log(K)·d)
        phase = np.exp(1j * np.log(K) * d)
        if mollifier_on:
            mw_val = MW(d)
        else:
            mw_val = 1.0 + 0j
        result += phase * mw_val
    return result

def main():
    rng = np.random.default_rng(42)
    out_lines = []
    out_lines.append("# B2 Q5 falsifier #3 — CUE MC mollifier-removal test")
    out_lines.append("# theoretical:  ON ~ 2.3147 (·CUE pair-correl factor)")
    out_lines.append("#               OFF ~ 1.0   (·CUE pair-correl factor)")
    out_lines.append("#               ratio ON/OFF should approach 2.31")
    out_lines.append("# (these are the y-integrals only; CUE sin-kernel adds finite-N corrections)")
    out_lines.append("")
    out_lines.append("K, N, samples, E[|S|²]_ON, E[|S|²]_OFF, ratio_ON/OFF")
    for K in [100, 1000]:
        N = max(50, int(np.log(K) * 30))  # heuristic: density 30/log K — enough neighbors
        N_samples = 200
        on_vals = []
        off_vals = []
        t0 = time.time()
        for _ in range(N_samples):
            ang = cue_eigenangles(N, rng)
            i_idx = N//2  # middle
            on = abs(compute_S(ang, i_idx, K, True))**2
            off = abs(compute_S(ang, i_idx, K, False))**2
            on_vals.append(on)
            off_vals.append(off)
        on_mean = np.mean(on_vals)
        off_mean = np.mean(off_vals)
        ratio = on_mean/off_mean if off_mean > 0 else float('nan')
        dt = time.time() - t0
        line = f"K={K} N={N} samples={N_samples} ON={on_mean:.4f} OFF={off_mean:.4f} ratio={ratio:.4f} dt={dt:.1f}s"
        print(line, flush=True)
        out_lines.append(line)
    with open("/Users/saar/Farey 4.7 solutions/B2_cue_mc_results.md", "w") as f:
        f.write("\n".join(out_lines))
    print("\nResults saved.")

if __name__ == "__main__":
    main()
