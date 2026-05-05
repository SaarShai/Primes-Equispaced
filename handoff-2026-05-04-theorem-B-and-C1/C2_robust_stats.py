#!/usr/bin/env python3
"""C2 robust stats: rerun SO(2N) and CUE Haar MC computing geometric mean
(median of log) and comparison ratios more carefully.

For heavy-tailed distributions, sample mean has very slow convergence.
Geometric mean (= exp E[log X]) is robust and the relationship to E[X]
is determined by the variance of log X (lognormal-like models).

Bourgade-Najnudel-Sodin: log|Lambda_A(1)| for SO(2N) Haar tends to
Gaussian with mean and variance growing logarithmically in N (log-correlated
field with planar / 1D structure).
"""
import numpy as np
import time
import math

def haar_orthogonal(n, rng):
    Z = rng.standard_normal((n, n))
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = np.sign(d); ph[ph == 0] = 1.0
    return Q * ph

def haar_so(n, rng):
    Q = haar_orthogonal(n, rng)
    if np.linalg.det(Q) < 0:
        Q[0, :] = -Q[0, :]
    return Q

def haar_unitary(n, rng):
    Z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = d / np.abs(d)
    return Q * ph

def so_eig_angles(Q):
    w = np.linalg.eigvals(Q)
    angles = np.angle(w)
    eps = 1e-8
    mask = (angles > eps) & (angles < np.pi - eps)
    return np.sort(angles[mask])

def main():
    out = []
    def emit(s):
        print(s, flush=True); out.append(s)

    plan = [(50, 5000), (100, 5000), (200, 2000)]
    rng = np.random.default_rng(20260505)
    emit("# Robust stats: log|Lambda(1)|^2 for SO(2N), CUE U(N), CUE U(2N)")
    emit("# Reports: mean(log), std(log), median(log), various quantiles")
    emit("")

    rows_so = []  # (N, mean_log, std_log, median_log)
    rows_cue_n = []
    rows_cue_2n = []

    for (N, K) in plan:
        # ---- SO(2N) ----
        log_lam_sq_so = np.empty(K); k = 0
        t0 = time.time()
        while k < K:
            Q = haar_so(2*N, rng)
            th = so_eig_angles(Q)
            if len(th) != N: continue
            fac = 4.0 * np.sin(th/2)**2
            log_lam_sq_so[k] = 2 * np.sum(np.log(np.maximum(fac, 1e-300)))
            k += 1
        dt_so = time.time() - t0

        # ---- CUE U(N) ----
        log_lam_sq_cue_n = np.empty(K)
        t0 = time.time()
        for kk in range(K):
            Q = haar_unitary(N, rng)
            phi = np.angle(np.linalg.eigvals(Q))
            mod_sq = 2.0 - 2.0 * np.cos(phi)  # |1-e^{i phi}|^2 = 2-2cos phi
            log_lam_sq_cue_n[kk] = np.sum(np.log(np.maximum(mod_sq, 1e-300)))
        dt_cue_n = time.time() - t0

        # ---- CUE U(2N) ----
        log_lam_sq_cue_2n = np.empty(K)
        t0 = time.time()
        for kk in range(K):
            Q = haar_unitary(2*N, rng)
            phi = np.angle(np.linalg.eigvals(Q))
            mod_sq = 2.0 - 2.0 * np.cos(phi)
            log_lam_sq_cue_2n[kk] = np.sum(np.log(np.maximum(mod_sq, 1e-300)))
        dt_cue_2n = time.time() - t0

        for label, arr, dt in [("SO(2N)", log_lam_sq_so, dt_so),
                                ("CUE U(N)", log_lam_sq_cue_n, dt_cue_n),
                                ("CUE U(2N)", log_lam_sq_cue_2n, dt_cue_2n)]:
            mean_log = float(np.mean(arr))
            std_log = float(np.std(arr, ddof=1))
            median_log = float(np.median(arr))
            q25 = float(np.quantile(arr, 0.25))
            q75 = float(np.quantile(arr, 0.75))
            geom_mean = math.exp(mean_log)
            mean_lin_logspace = math.exp(mean_log + 0.5 * std_log**2)  # if Gaussian
            # Direct sample mean of exp:
            mx = np.max(arr)
            sample_mean = math.exp(mx) * np.mean(np.exp(arr - mx))
            emit(f"{label:10s} N={N:3d} K={K:5d} dt={dt:.1f}s")
            emit(f"           mean(log) = {mean_log:+.4f}  std(log) = {std_log:.4f}")
            emit(f"           median(log) = {median_log:+.4f}  q25 = {q25:+.4f}  q75 = {q75:+.4f}")
            emit(f"           geom_mean = exp(mean log) = {geom_mean:.4e}")
            emit(f"           sample_mean = {sample_mean:.4e}")
            emit(f"           lognormal_mean = exp(mean+sigma^2/2) = {mean_lin_logspace:.4e}")
            emit("")
            if label == "SO(2N)": rows_so.append((N, mean_log, std_log, median_log, sample_mean))
            elif label == "CUE U(N)": rows_cue_n.append((N, mean_log, std_log, median_log, sample_mean))
            elif label == "CUE U(2N)": rows_cue_2n.append((N, mean_log, std_log, median_log, sample_mean))

    # Compare ratios across same matrix size 2N: SO(2N) vs CUE U(2N)
    emit("=" * 80)
    emit("Direct ratio at SAME matrix size 2N: SO(2N)[Lambda^2] / CUE U(2N)[|Lambda|^2]")
    emit("=" * 80)
    for s, c in zip(rows_so, rows_cue_2n):
        N, mlo_s, std_s, med_s, sm_s = s
        N2, mlo_c, std_c, med_c, sm_c = c
        emit(f"N={N:3d}: SO(2N)={sm_s:.3e}, CUE U(2N)={sm_c:.3e}, ratio={sm_s/sm_c:.4f}")
        emit(f"   geom_mean ratio = {math.exp(mlo_s - mlo_c):.4f}")
        emit(f"   median(log) diff = {med_s - med_c:+.4f}")
    emit("")

    # Same matrix dim N comparison:
    emit("=" * 80)
    emit("Same matrix size N: SO(N=2*half) vs CUE U(N=2*half) at half-dim N=50,100,200")
    emit("This is the actual apples-to-apples comparison.")
    emit("=" * 80)

    out_path = "/Users/saar/Farey 4.7 solutions/C2_robust_stats.out"
    with open(out_path, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"Written to {out_path}")

if __name__ == "__main__":
    main()
