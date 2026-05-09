#!/usr/bin/env python3
"""C2 orthogonal Monte Carlo (EXTENDED) — verify whether the orthogonal
analog of the Hughes-Mezzadri / Conrey-Rubinstein-Snaith Barnes-G constant
b'_1 = G(3)^2/G(5) = 1/12 (the UNITARY leading coefficient of the second
moment of |Z'_A(1)|^2 over U(N)) carries over to O(2N), SO(2N), SO(2N+1).

Citation backbone (verbatim, see deliverable):
  - CRS 2006 (arXiv math/0508378) Theorem 2 + Eq. (1.5)-(1.6):
       ∫_{U(N)} |Z'_A(1)|^{2k} dA_N ~ b'_k * N^{k^2 + 2k}
       for k=1: b'_1 = 1/(2^2 · 3) = 1/12, scaling N^3.
  - CRS 2006 Theorem 1 + Eq. (1.3)-(1.4):
       ∫_{U(N)} |Λ'_A(1)|^{2k} dA_N ~ b_k * N^{k^2 + 2k}
       for k=1: b_1 = 1/3, scaling N^3.
  - The Z and Λ derivative second moments differ by the Hardy-Z rotation
    factor, which has |.|=1 on the unit circle but contributes log-derivative
    terms when differentiated. Specifically:
       Z_A(s) = e^{-iπN/2} e^{i Σθ_n / 2} s^{-N/2} Λ_A(s)
       so on |s|=1: |Z_A(s)| = |Λ_A(s)|
       but |Z'_A(s)|^2 ≠ |Λ'_A(s)|^2 because the s^{-N/2} factor differentiates
       to (-N/2)/s.

Goal of this script:
  (1) CUE baseline at N ∈ {50,100,200,400,800}, K = 10^4 - 4*10^4 samples per N,
      verify b_1 = 1/3 and b'_1 = 1/12 to 3 significant figures.
  (2) Orthogonal O(2N), SO(2N), SO(2N+1) at the same N: extract the leading
      coefficient and power; report deviation from 1/12.
  (3) κ=0 vs κ-matched falsifier on the bulk-scaled linear statistic.
  (4) Alternative-α candidate residual table.

Outputs:
  - per-N stratified JSON of raw samples
  - .out human-readable summary
  - markdown deliverable updated separately
"""
import numpy as np
import math
import json
import time
import os
import sys
from scipy.stats import ortho_group
import mpmath as mp

OUT_DIR = "/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup"
RAW_DIR = os.path.join(OUT_DIR, "raw_samples")
os.makedirs(RAW_DIR, exist_ok=True)


# ---------- High-precision symbolic constants ----------

mp.mp.dps = 60

def symbolic_constants():
    G3 = mp.barnesg(3)
    G5 = mp.barnesg(5)
    ratio = G3**2 / G5
    return {
        "G(3)": str(G3),
        "G(5)": str(G5),
        "G(3)^2/G(5)": str(ratio),
        "1/12 (mpmath 50dps)": str(mp.mpf(1)/12),
        "delta": str(ratio - mp.mpf(1)/12),
    }


# ---------- Haar samplers ----------

def haar_unitary(n, rng):
    """Mezzadri 2007 Lemma 4."""
    Z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = d / np.abs(d)
    Q = Q * ph
    return Q


def haar_orthogonal(n, rng):
    """Mezzadri 2007 Lemma 5: Haar O(n) via QR with sign correction."""
    Z = rng.standard_normal((n, n))
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = np.sign(d)
    ph[ph == 0] = 1.0
    Q = Q * ph
    return Q


def haar_so(n, rng):
    """Haar SO(n): sample O(n), flip first row if det = -1."""
    Q = haar_orthogonal(n, rng)
    if np.linalg.det(Q) < 0:
        Q[0, :] = -Q[0, :]
    return Q


# ---------- Eigenangle extraction ----------

def cue_eigangles(Q):
    w = np.linalg.eigvals(Q)
    return np.angle(w)


def so_pair_angles(Q):
    """For Q in O(n) or SO(n), return half-pairs theta_j in (0, pi)
    of the e^{±i θ_j} eigenvalue pairs (real eigenvalues at ±1 excluded)."""
    w = np.linalg.eigvals(Q)
    angles = np.angle(w)
    eps = 1e-8
    mask = (angles > eps) & (angles < np.pi - eps)
    return np.sort(angles[mask])


# ---------- Λ(1), Z(1), Λ'(1), Z'(1) computations ----------

def cue_lambda_zprime_at_1(Q):
    """For A ∈ U(N) with eigenangles φ_1,...,φ_N:
    Λ_A(s) = ∏_n (1 - s e^{-iφ_n})
    Z_A(s) = e^{-iπN/2} e^{i Σφ_n/2} s^{-N/2} Λ_A(s)

    At s=1:
      Λ_A(1) = ∏_n (1 - e^{-iφ_n})
      d/ds[s^{-N/2}]_{s=1} = -N/2
      Λ'_A(s) = -Σ_m e^{-iφ_m} ∏_{n≠m}(1 - s e^{-iφ_n})
      Λ'_A(1) = -Σ_m e^{-iφ_m} ∏_{n≠m}(1 - e^{-iφ_n})
      Λ'_A(1) / Λ_A(1) = Σ_m -e^{-iφ_m} / (1 - e^{-iφ_m})  (CUE log derivative)
    Then
      Z'_A(1) = e^{-iπN/2} e^{i Σφ_n/2} [Λ'_A(1) - (N/2) Λ_A(1)]
      |Z'_A(1)|^2 = |Λ'_A(1) - (N/2) Λ_A(1)|^2
                 = |Λ_A(1)|^2 |Λ'_A(1)/Λ_A(1) - N/2|^2  if Λ_A(1) ≠ 0
    """
    phi = cue_eigangles(Q)
    N = len(phi)
    e_phi = np.exp(-1j * phi)  # e^{-i φ}
    one_minus = 1.0 - e_phi
    log_lam = np.sum(np.log(one_minus.astype(complex) + 0j))  # complex log
    lam = np.exp(log_lam)
    # log derivative: Λ'/Λ at s=1 = Σ -e^{-iφ}/(1 - e^{-iφ})
    logder = np.sum(-e_phi / one_minus)
    lp = logder * lam  # Λ'_A(1)
    # |Z'(1)|^2 = |Λ'(1) - (N/2) Λ(1)|^2 (rotation phase has unit modulus)
    zp = lp - (N / 2.0) * lam
    return {
        "lam_abs2": float((lam * np.conjugate(lam)).real),
        "lp_abs2": float((lp * np.conjugate(lp)).real),
        "zp_abs2": float((zp * np.conjugate(zp)).real),
    }


def so_even_lambda_at_1(Q):
    """For A ∈ SO(2N) with paired eigenvalues e^{±iθ_j}, j=1..N:
       Λ_A(z) = det(I - zA) = prod_j (1 - 2 cos(θ_j) z + z^2)
       p_j(z) = 1 - 2 cos(θ_j) z + z^2
       p_j(1) = 2 - 2 cos(θ_j) = 4 sin^2(θ_j/2)
       p_j'(1) = -2 cos(θ_j) + 2 = p_j(1)
       So Λ'_A(1)/Λ_A(1) = Σ_j p_j'(1)/p_j(1) = N exactly.
       => |Λ'_A(1)|^2 = N^2 |Λ_A(1)|^2

    For Z_A on |z|=1 in SO(2N) convention (real characteristic polynomial),
    we use the equivalent symmetrized form:
       Z_A(e^{iψ}) = ∏_j (e^{iψ/2} - e^{-iψ/2}·e^{iθ_j})... etc.
    In practice for SO(2N), Λ_A(1) is real; we report |Λ(1)|^2 and |Λ'(1)|^2.
    """
    th = so_pair_angles(Q)
    N = len(th)
    fac = 4.0 * np.sin(th / 2.0)**2  # p_j(1)
    fac = np.maximum(fac, 1e-300)
    log_lam = np.sum(np.log(fac))
    lam_abs2 = math.exp(2.0 * log_lam) if log_lam < 350 else float("inf")
    lp_abs2 = (N * N) * lam_abs2 if lam_abs2 != float("inf") else float("inf")
    return {
        "log_lam_abs": log_lam,
        "lam_abs2": lam_abs2,
        "lp_abs2": lp_abs2,
        "N_pairs": N,
    }


def so_odd_lprime_at_1(Q):
    """For A ∈ SO(2N+1) (forced real eigenvalue +1):
       Λ_A(z) = (1-z) ∏_j p_j(z)
       Λ_A(1) = 0
       Λ'_A(1) = -∏_j p_j(1) = -∏_j 4 sin^2(θ_j/2)
       |Λ'_A(1)|^2 = (∏_j 4 sin^2(θ_j/2))^2  (analog of Z'(1) at the forced zero)
    """
    th = so_pair_angles(Q)
    N = len(th)
    fac = 4.0 * np.sin(th / 2.0)**2
    fac = np.maximum(fac, 1e-300)
    log_lam = np.sum(np.log(fac))
    lp_abs2 = math.exp(2.0 * log_lam) if log_lam < 350 else float("inf")
    return {
        "log_prod": log_lam,
        "lp_abs2": lp_abs2,
        "N_pairs": N,
    }


# ---------- Top-level MC ----------

def run_cue(N, K, rng):
    out = np.empty((K, 3))
    skipped = 0
    k = 0
    while k < K:
        Q = haar_unitary(N, rng)
        try:
            d = cue_lambda_zprime_at_1(Q)
        except Exception:
            skipped += 1
            continue
        out[k, 0] = d["lam_abs2"]
        out[k, 1] = d["lp_abs2"]
        out[k, 2] = d["zp_abs2"]
        k += 1
    return out, skipped


def run_so_even(N, K, rng):
    out = np.empty((K, 2))
    skipped = 0
    k = 0
    while k < K:
        Q = haar_so(2 * N, rng)
        d = so_even_lambda_at_1(Q)
        if d["N_pairs"] != N or not math.isfinite(d["lam_abs2"]):
            skipped += 1
            if skipped > 10 * K:
                raise RuntimeError("too many degenerate SO(2N) samples")
            continue
        out[k, 0] = d["lam_abs2"]
        out[k, 1] = d["lp_abs2"]
        k += 1
    return out, skipped


def run_so_odd(N, K, rng):
    """SO(2N+1): N pair-angles + 1 forced eigenvalue at +1."""
    out = np.empty(K)
    skipped = 0
    k = 0
    while k < K:
        Q = haar_so(2 * N + 1, rng)
        d = so_odd_lprime_at_1(Q)
        if d["N_pairs"] != N or not math.isfinite(d["lp_abs2"]):
            skipped += 1
            if skipped > 10 * K:
                raise RuntimeError("too many degenerate SO(2N+1) samples")
            continue
        out[k] = d["lp_abs2"]
        k += 1
    return out, skipped


# ---------- Robust mean/SE on heavy-tailed positive samples ----------

def robust_stats(x):
    """Sample mean, SE, geometric mean, median, 95% trimmed mean."""
    x = np.asarray(x, dtype=float)
    K = len(x)
    mean = float(np.mean(x))
    se = float(np.std(x, ddof=1) / math.sqrt(K))
    geom = float(math.exp(np.mean(np.log(np.maximum(x, 1e-300)))))
    median = float(np.median(x))
    # Trimmed mean (5% each side)
    qlo, qhi = np.quantile(x, [0.05, 0.95])
    tmask = (x >= qlo) & (x <= qhi)
    trim_mean = float(np.mean(x[tmask])) if tmask.sum() > 0 else float("nan")
    return {
        "K": K,
        "mean": mean,
        "se": se,
        "geom": geom,
        "median": median,
        "trim_mean_5_95": trim_mean,
    }


# ---------- Bulk-scaled linear statistic (κ=0 falsifier) ----------

def MW(y):
    """Mollifier transform from B2 work."""
    w = 1j * y
    return (1 - np.exp(-1 - w)) / (1 + w)


def cue_bulk_S(Q, kappa):
    """Compute S_κ = Σ_{j≠0} M_W(iy_j) e^{iκ y_j} where y_j = N (φ_j - φ_0) / (2π)
    (Palm-conditioned at midpoint eigenangle of CUE)."""
    phi = np.sort(cue_eigangles(Q))
    N = len(phi)
    i0 = N // 2
    diffs = phi - phi[i0]
    y = N * diffs / (2 * math.pi)
    mask = np.arange(N) != i0
    yy = y[mask]
    return np.sum(MW(yy) * np.exp(1j * kappa * yy))


def so_bulk_S(Q, kappa, n_full):
    """Bulk-scaled linear statistic on SO(n) eigenangles, Palm at first
    pair-angle θ_0 ≠ 0,π."""
    th = so_pair_angles(Q)  # in (0, π)
    if len(th) < 4:
        return None
    N = n_full // 2  # density per unit angle is N/π for SO(n=2N) in (0,π)
    i0 = len(th) // 2
    diffs = th - th[i0]
    y = (n_full / (2 * math.pi)) * diffs  # bulk scale: density n/(2π) per unit angle
    mask = np.arange(len(th)) != i0
    yy = y[mask]
    return np.sum(MW(yy) * np.exp(1j * kappa * yy))


# ---------- Main ----------

def main():
    rng = np.random.default_rng(20260509)
    out_lines = []
    raw = {}

    def emit(s):
        print(s, flush=True)
        out_lines.append(s)

    emit("# C2 ORTHOGONAL MC EXTENDED")
    emit(f"# date: 2026-05-09")
    emit(f"# numpy {np.__version__}, scipy.stats.ortho_group")
    emit("")
    emit("=" * 80)
    emit("Section 0. Symbolic Barnes-G verification (mpmath dps=60)")
    emit("=" * 80)
    sc = symbolic_constants()
    for k, v in sc.items():
        emit(f"  {k} = {v}")
    emit("")

    # Sample plan: budget ~30 min total
    # CUE: cheap. SO(2N) ~ 5x faster than CUE at same dim.
    cue_plan = [(50, 8000), (100, 4000), (200, 2000), (400, 800), (800, 300)]
    # SO(2N): heavy tail; same K
    so_plan = [(50, 8000), (100, 4000), (200, 2000), (400, 1000), (800, 400)]

    # Section 1: CUE baseline (verify b_1 = 1/3, b'_1 = 1/12)
    emit("=" * 80)
    emit("Section 1. CUE U(N) baseline: ∫|Λ'(1)|^2 dA_N ~ b_1 N^3, b_1 = 1/3")
    emit("                              ∫|Z'(1)|^2 dA_N ~ b'_1 N^3, b'_1 = 1/12")
    emit("=" * 80)
    cue_results = {}
    for (N, K) in cue_plan:
        t0 = time.time()
        samples, skipped = run_cue(N, K, rng)
        dt = time.time() - t0
        s_lam = robust_stats(samples[:, 0])
        s_lp = robust_stats(samples[:, 1])
        s_zp = robust_stats(samples[:, 2])
        emit(f"\nN={N:4d}  K={K:6d}  skipped={skipped}  dt={dt:.1f}s")
        emit(f"  E[|Lam(1)|^2]    = {s_lam['mean']:.4e} +/- {s_lam['se']:.2e}    /N = {s_lam['mean']/N:.4f}  (KS exact: 1)")
        emit(f"  E[|Lam'(1)|^2]   = {s_lp['mean']:.4e} +/- {s_lp['se']:.2e}    /N^3 = {s_lp['mean']/N**3:.5f}   (b_1 = 1/3 = 0.33333)")
        emit(f"  E[|Z'(1)|^2]     = {s_zp['mean']:.4e} +/- {s_zp['se']:.2e}    /N^3 = {s_zp['mean']/N**3:.5f}   (b'_1 = 1/12 = 0.08333)")
        cue_results[N] = {
            "lam": s_lam, "lp": s_lp, "zp": s_zp,
            "K": K, "skipped": skipped, "dt": dt,
        }
        # Save raw samples
        np.save(os.path.join(RAW_DIR, f"cue_N{N}_K{K}.npy"), samples)

    # Section 2: O(2N), SO(2N), SO(2N+1) extended
    emit("")
    emit("=" * 80)
    emit("Section 2. SO(2N): ∫|Λ(1)|^2 dA_N (and |Λ'(1)|^2 = N^2 |Λ(1)|^2 exactly)")
    emit("=" * 80)
    so_even_results = {}
    for (N, K) in so_plan:
        t0 = time.time()
        samples, skipped = run_so_even(N, K, rng)
        dt = time.time() - t0
        s_lam = robust_stats(samples[:, 0])
        s_lp = robust_stats(samples[:, 1])
        emit(f"\nSO(2N) N={N:4d}  K={K:6d}  skipped={skipped}  dt={dt:.1f}s")
        emit(f"  E[|Lam(1)|^2]    = {s_lam['mean']:.4e} +/- {s_lam['se']:.2e}")
        emit(f"  E[|Lam(1)|^2]/sqrt(N) = {s_lam['mean']/math.sqrt(N):.4f}    (KS f_O(1) = 2 expected)")
        emit(f"  E[|Lam'(1)|^2]   = {s_lp['mean']:.4e} +/- {s_lp['se']:.2e}    /N^3 = {s_lp['mean']/N**3:.5f}")
        emit(f"      vs 1/12 = 0.08333: ratio = {(s_lp['mean']/N**3)/(1/12):.4f}")
        emit(f"      vs 1/3  = 0.33333: ratio = {(s_lp['mean']/N**3)/(1/3):.4f}")
        emit(f"  median(|Lam(1)|^2) = {s_lam['median']:.4e}  trim_mean(5-95) = {s_lam['trim_mean_5_95']:.4e}")
        so_even_results[N] = {
            "lam": s_lam, "lp": s_lp, "K": K, "skipped": skipped, "dt": dt,
        }
        np.save(os.path.join(RAW_DIR, f"so_even_N{N}_K{K}.npy"), samples)

    emit("")
    emit("=" * 80)
    emit("Section 3. SO(2N+1): ∫|Λ'(1)|^2 dA_N (the forced-zero derivative)")
    emit("=" * 80)
    so_odd_results = {}
    for (N, K) in so_plan:
        t0 = time.time()
        samples, skipped = run_so_odd(N, K, rng)
        dt = time.time() - t0
        s = robust_stats(samples)
        emit(f"\nSO(2N+1) N={N:4d}  K={K:6d}  skipped={skipped}  dt={dt:.1f}s")
        emit(f"  E[|Lam'(1)|^2]   = {s['mean']:.4e} +/- {s['se']:.2e}")
        emit(f"  /N^(3/2) = {s['mean']/N**1.5:.4f}    /N^2 = {s['mean']/N**2:.4f}    /N^3 = {s['mean']/N**3:.4f}")
        emit(f"  Hughes thesis predicts ~ Const * N^{{3/2}} for k=1, with constant from Barnes-G")
        emit(f"  vs 1/12 * N^3 = {(1/12)*N**3:.4e}, ratio = {s['mean']/((1/12)*N**3):.4f}")
        so_odd_results[N] = {"lp": s, "K": K, "skipped": skipped, "dt": dt}
        np.save(os.path.join(RAW_DIR, f"so_odd_N{N}_K{K}.npy"), samples)

    # Section 4: log-log fits
    emit("")
    emit("=" * 80)
    emit("Section 4. log-log fits: E ~ C * N^p")
    emit("=" * 80)

    def fit(rs, key):
        Ns = sorted(rs.keys())
        Es = np.array([rs[N][key]["mean"] for N in Ns])
        Ses = np.array([rs[N][key]["se"] for N in Ns])
        ln = np.log(np.array(Ns, dtype=float))
        le = np.log(Es)
        A = np.vstack([ln, np.ones_like(ln)]).T
        p, log_C = np.linalg.lstsq(A, le, rcond=None)[0]
        return Ns, Es, Ses, math.exp(log_C), p

    Ns, Es, Ses, C, p = fit(cue_results, "lp")
    emit(f"CUE  E[|Λ'(1)|^2]:    C = {C:.5f}  power = {p:.4f}    (CRS exact: C=1/3=0.33333, power=3)")
    Ns, Es, Ses, C, p = fit(cue_results, "zp")
    emit(f"CUE  E[|Z'(1)|^2]:    C = {C:.5f}  power = {p:.4f}    (CRS exact: C=1/12=0.08333, power=3)")
    Ns, Es, Ses, C, p = fit(cue_results, "lam")
    emit(f"CUE  E[|Λ(1)|^2]:     C = {C:.5f}  power = {p:.4f}    (KS exact: C=1, power=1)")

    Ns, Es, Ses, C_so, p_so = fit(so_even_results, "lp")
    emit(f"SO(2N) E[|Λ'(1)|^2]:  C = {C_so:.5f}  power = {p_so:.4f}")
    Ns, Es, Ses, C_so_lam, p_so_lam = fit(so_even_results, "lam")
    emit(f"SO(2N) E[|Λ(1)|^2]:   C = {C_so_lam:.5f}  power = {p_so_lam:.4f}    (KS f_O(1)=2, power 1/2)")

    Ns, Es, Ses, C_oo, p_oo = fit(so_odd_results, "lp")
    emit(f"SO(2N+1) E[|Λ'(1)|^2]: C = {C_oo:.5f}  power = {p_oo:.4f}")

    # Section 5: alternative-α candidate residual table (for SO(2N) /N^3)
    emit("")
    emit("=" * 80)
    emit("Section 5. Alternative-α candidate residuals for the SO(2N+1) coefficient")
    emit("(scaled to make |Λ'(1)|^2/N^3 the comparison)")
    emit("=" * 80)
    alphas = {
        "1/12 (HM/CRS unitary Barnes-G)": 1/12,
        "1/3 (CRS unitary |Λ'|^2 leading)": 1/3,
        "1/(2π^2) (Plancherel rough)": 1/(2*math.pi**2),
        "1/π^2": 1/math.pi**2,
        "2/π^2": 2/math.pi**2,
        "1/(4π)": 1/(4*math.pi),
        "1/24": 1/24,
        "1/6": 1/6,
        "2/3 (orth at-zeros)": 2/3,
    }
    # use largest N with reasonable SE
    N_best = max(so_odd_results.keys())
    best = so_odd_results[N_best]["lp"]
    obs = best["mean"] / (N_best ** p_oo)
    emit(f"At N={N_best}: SO(2N+1) E[|Λ'|^2]/N^p with p={p_oo:.3f} = {obs:.4e}")
    emit(f"At N={N_best}: SO(2N+1) E[|Λ'|^2]/N^3                = {best['mean']/N_best**3:.5e}")
    for name, val in alphas.items():
        residual = abs(best['mean']/N_best**3 - val) / val * 100
        emit(f"  vs {name:35s} = {val:.5f}    relative residual {residual:.1f}%")

    # Section 6: kappa=0 vs kappa-matched falsifier (orthogonal bulk)
    emit("")
    emit("=" * 80)
    emit("Section 6. κ=0 vs κ-matched falsifier — orthogonal bulk-scaled S statistic")
    emit("=" * 80)
    emit("Following B2 v3 polished (unitary): predicts Var(S_κ) → I_ON with α_ratio=1")
    emit("for κ ≈ (2π)² ≈ 39.48; very different (smaller) prediction at κ=0.")
    emit("Run on SO(2N) Haar bulk for N ∈ {200, 400}, ~300 samples per κ.")
    emit("")
    from scipy.integrate import quad
    I_ON, _ = quad(lambda y: abs(MW(y))**2 * (1 - np.sinc(y)**2), -200, 200, limit=600)
    emit(f"  I_ON = ∫|M_W|^2 (1 - sinc^2(πy)) dy = {I_ON:.5f}  (analytic prediction for high-κ Var(S))")

    kappa_vals = [0.0, 39.48]
    so_bulk_results = {}
    for N_pairs in [200, 400]:
        n = 2 * N_pairs
        for kappa in kappa_vals:
            n_samples = 300 if N_pairs <= 200 else 150
            S_vals = []
            for _ in range(n_samples):
                Q = haar_so(n, rng)
                S = so_bulk_S(Q, kappa, n)
                if S is not None:
                    S_vals.append(S)
            S_vals = np.array(S_vals, dtype=complex)
            E_S = np.mean(S_vals)
            E_abs2 = np.mean(np.abs(S_vals)**2)
            VarS = E_abs2 - abs(E_S)**2
            SE_var = np.std(np.abs(S_vals)**2) / math.sqrt(len(S_vals))
            emit(f"  SO({n})  κ={kappa:6.2f}  samples={len(S_vals):3d}  Var(S) = {VarS:.4f} +/- {SE_var:.4f}")
            so_bulk_results[(n, kappa)] = (VarS, SE_var)

    # Section 7: write JSON of summary
    summary = {
        "symbolic": sc,
        "cue_results": {k: {kk: vv for kk, vv in v.items() if kk != "dt"} for k, v in cue_results.items()},
        "so_even_results": {k: {kk: vv for kk, vv in v.items() if kk != "dt"} for k, v in so_even_results.items()},
        "so_odd_results": {k: {kk: vv for kk, vv in v.items() if kk != "dt"} for k, v in so_odd_results.items()},
        "fits": {
            "CUE_lp": {"C": float(np.exp(np.polyfit(np.log(sorted(cue_results.keys())), np.log([cue_results[N]['lp']['mean'] for N in sorted(cue_results.keys())]), 1)[1])), "p": "see out"},
        },
        "I_ON": float(I_ON),
        "so_bulk_kappa": {f"n={k[0]}_kappa={k[1]}": {"VarS": float(v[0]), "SE": float(v[1])} for k, v in so_bulk_results.items()},
    }
    with open(os.path.join(OUT_DIR, "C2_orthogonal_MC_extended.summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    out_path = os.path.join(OUT_DIR, "C2_orthogonal_MC_extended.out")
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"\nResults written to {out_path}")
    print(f"Raw samples in {RAW_DIR}/")
    print(f"JSON summary at {os.path.join(OUT_DIR, 'C2_orthogonal_MC_extended.summary.json')}")


if __name__ == "__main__":
    main()
