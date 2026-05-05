#!/usr/bin/env python3
"""C2 verification: Orthogonal RMT 2nd moment of |Lambda'_A(1)|^2 over SO(2N)
AND SO(2N+1) via Haar Monte Carlo at N = 50, 100, 200.

Background (from Reverse_engineer_constant.md):
  Decomposition 2/(3pi) = (1/(2pi)) * (1/12) * 16 was identified, where:
    - 1/(2pi) = Plancherel
    - 1/12 = Hughes-Mezzadri G(3)^2/G(5) UNITARY Barnes-G coefficient (CUE Z'(1))
    - 16 = d^{2k}/(2k)! * (2k)! = d^{2k} = 2^4

Two distinct candidate identities for the orthogonal coefficient appearing
in 2/(3 pi) = (1/pi) * (orthogonal coeff):
  (A) Hughes-Snaith SO(2N+1) derivative second moment leading constant.
      Standard reference: Conrey-Rubinstein-Snaith 2006, RMT_Painleve_GRH_bypass.md
      lines 64-71 cite "f_SO(2)" with translation to (log X)^2 -> 2/(3 pi).
      Predicts E|Lambda'(1)|^2 ~ const * N^{some power}.
  (B) User's C2 framing: orthogonal coeff = 1/12 (unitary baseline) with
      d^{2k}/(2k)! = 16/24 = 2/3 multiplier elsewhere.
      Predicts coefficient 1/12 = 0.0833.

Crucial algebraic fact for SO(2N) (no forced eigenvalue at +1):
  Lambda_A(z) = prod_{j=1}^N (1 - 2 cos(theta_j) z + z^2)
  At z=1: each factor p_j(z) = 1 - 2 cos(theta_j) z + z^2 has p_j'(1) = p_j(1),
  so Lambda'_A(1) / Lambda_A(1) = N exactly (verified in sympy).
  Hence |Lambda'_A(1)|^2 = N^2 * Lambda_A(1)^2 (deterministic ratio).

For SO(2N+1) (forced eigenvalue +1):
  Lambda_A(z) = (1 - z) * prod_j p_j(z), Lambda_A(1) = 0,
  Lambda'_A(1) = - prod_j p_j(1) = - prod_j 4 sin^2(theta_j / 2),
  |Lambda'_A(1)|^2 = (prod_j 4 sin^2(theta_j/2))^2.
  This is the "non-trivial" object - relevant orthogonal derivative moment
  in CFKRS/Hughes-Snaith literature (since orthogonal L-functions with
  root-number -1 have forced zero at the central point).

This MC measures BOTH:
  - For SO(2N): E[Lambda_A(1)^2] (and hence E|Lambda'(1)|^2 via N^2 factor)
  - For SO(2N+1): E|Lambda'_A(1)|^2 directly

then fits leading N-power and reads off the coefficient.

Output: K samples per N per group, fitted leading power and coefficient,
plus comparison to 2/3, 1/12, 1/18.
"""
import numpy as np
import time
import math

# ---------- Haar O(n) sampling and SO(n) projection ----------

def haar_orthogonal(n, rng):
    """Sample Haar from O(n) via Mezzadri 2007 QR trick."""
    Z = rng.standard_normal((n, n))
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = np.sign(d)
    ph[ph == 0] = 1.0
    Q = Q * ph
    return Q

def haar_so(n, rng):
    """Haar on SO(n): sample O(n), flip first row if det = -1."""
    Q = haar_orthogonal(n, rng)
    if np.linalg.det(Q) < 0:
        Q[0, :] = -Q[0, :]
    return Q

def so_eig_angles(Q, expect_real_one=False):
    """Return the unique angles theta_j in (0, pi) for the e^{+/- i theta_j}
    eigenvalue pairs of Q in SO(n).  If expect_real_one (n odd), assume one
    real eigenvalue at +1 (or -1, but for SO(odd) Haar it's +1 generically)."""
    w = np.linalg.eigvals(Q)
    angles = np.angle(w)
    # Keep angles in (eps, pi - eps) so we exclude real eigenvalues
    eps = 1e-8
    mask = (angles > eps) & (angles < np.pi - eps)
    th = angles[mask]
    return np.sort(th)

# ---------- Lambda(1) computation ----------

def log_lambda_factor_at_1(thetas):
    """log of prod_j (4 sin^2(theta_j / 2)) = log of prod_j p_j(1)
    where p_j(z) = 1 - 2cos(theta_j) z + z^2.  Avoids underflow."""
    fac = 4.0 * np.sin(thetas / 2.0)**2
    fac = np.maximum(fac, 1e-300)
    return np.sum(np.log(fac))

# ---------- Main MC ----------

def run_mc_so2n(N, K, rng):
    """Compute samples of log(Lambda_A(1)^2) for A in SO(2N).
    Recall: |Lambda'(1)|^2 = N^2 * Lambda(1)^2 (exact identity)."""
    log_lam_sq = np.empty(K)
    n = 2 * N
    skipped = 0
    k = 0
    while k < K:
        Q = haar_so(n, rng)
        th = so_eig_angles(Q)
        if len(th) != N:
            skipped += 1
            if skipped > 10 * K:
                raise RuntimeError("too many degenerate samples")
            continue
        log_lam = log_lambda_factor_at_1(th)
        log_lam_sq[k] = 2.0 * log_lam
        k += 1
    return log_lam_sq, skipped

def run_mc_so2n1(N, K, rng):
    """Compute samples of log(|Lambda'_A(1)|^2) for A in SO(2N+1).
    For SO(2N+1): |Lambda'(1)|^2 = (prod_j 4 sin^2(theta_j/2))^2."""
    log_lam_prime_sq = np.empty(K)
    n = 2 * N + 1
    skipped = 0
    k = 0
    while k < K:
        Q = haar_so(n, rng)
        th = so_eig_angles(Q)
        if len(th) != N:
            skipped += 1
            if skipped > 10 * K:
                raise RuntimeError("too many degenerate samples")
            continue
        log_lam = log_lambda_factor_at_1(th)
        # |Lambda'(1)|^2 = (prod_j p_j(1))^2 = exp(2 * log_lam)
        log_lam_prime_sq[k] = 2.0 * log_lam
        k += 1
    return log_lam_prime_sq, skipped

def stats_from_log(log_x):
    """Mean and SE of X given samples of log(X) (X >= 0).
    Uses Welford / shift trick to avoid overflow."""
    m = np.max(log_x)
    y = np.exp(log_x - m)
    mean_y = np.mean(y)
    var_y = np.var(y, ddof=1)
    se_y = np.sqrt(var_y / len(log_x))
    log_mean = m + math.log(mean_y) if mean_y > 0 else -np.inf
    log_se = m + math.log(se_y) if se_y > 0 else -np.inf
    return log_mean, log_se, mean_y, se_y, m

def main():
    out_lines = []
    def emit(s):
        print(s, flush=True)
        out_lines.append(s)

    emit("# C2 orthogonal MC: SO(2N) and SO(2N+1) Haar 2nd moments of |Lambda'(1)|^2")
    emit("# Hughes/Conrey-Rubinstein-Snaith literature constants of interest:")
    emit(f"#   2/3   = {2/3:.6f}")
    emit(f"#   1/12  = {1/12:.6f}  (CUE unitary G(3)^2/G(5))")
    emit(f"#   1/18  = {1/18:.6f}  (1/12 * 16/24)")
    emit("# For SO(2N): |Lambda'(1)|^2 = N^2 * Lambda(1)^2 (exact)")
    emit("# For SO(2N+1): |Lambda'(1)|^2 = (prod_j 4 sin^2(theta_j/2))^2")
    emit("")

    # Smaller K for largest N to stay in 6h budget
    plan = [(50, 10000), (100, 10000), (200, 4000)]

    rng = np.random.default_rng(20260503)

    # ---- SO(2N) ----
    emit("=" * 80)
    emit("SO(2N) Haar:  E[Lambda_A(1)^2]  and derived  E|Lambda'(1)|^2 / N^2 = same")
    emit("=" * 80)
    so2n_results = {}
    for (N, K) in plan:
        t0 = time.time()
        log_lam_sq, sk = run_mc_so2n(N, K, rng)
        log_mean, log_se, mean_y, se_y, m = stats_from_log(log_lam_sq)
        # E[Lambda(1)^2] = exp(log_mean) ;  SE = exp(log_se)
        EL2 = math.exp(log_mean)
        SE_EL2 = math.exp(log_se)
        # Also the empirical mean of log_lam_sq (i.e. E[log Lambda^2])
        # for diagnostics - is it bounded as N grows?
        mean_log = float(np.mean(log_lam_sq))
        std_log = float(np.std(log_lam_sq, ddof=1))
        dt = time.time() - t0
        emit(f"N={N:3d} K={K:5d} skipped={sk:3d} dt={dt:.1f}s")
        emit(f"  log_max_seen = {m:+.3f}  (samples are heavy-tailed if log_max large)")
        emit(f"  mean(log L^2) = {mean_log:+.4f}  std(log L^2) = {std_log:.4f}")
        emit(f"  E[Lambda(1)^2] = {EL2:.6e}  +/-  {SE_EL2:.3e}")
        emit(f"     vs 2/3 = 0.6667 : ratio = {EL2 / (2/3):.4f}")
        emit(f"     vs 1/12 = 0.0833: ratio = {EL2 / (1/12):.4f}")
        emit(f"     vs 1/18 = 0.0556: ratio = {EL2 / (1/18):.4f}")
        emit(f"  E|Lambda'(1)|^2 = N^2 * E[L^2] = {N*N * EL2:.4e}")
        emit("")
        so2n_results[N] = (EL2, SE_EL2, mean_log, std_log)

    # ---- SO(2N+1) ----
    emit("=" * 80)
    emit("SO(2N+1) Haar:  E|Lambda'_A(1)|^2 = E[(prod_j 4 sin^2(theta_j/2))^2]")
    emit("=" * 80)
    so2n1_results = {}
    for (N, K) in plan:
        t0 = time.time()
        log_lp_sq, sk = run_mc_so2n1(N, K, rng)
        log_mean, log_se, mean_y, se_y, m = stats_from_log(log_lp_sq)
        ELp2 = math.exp(log_mean)
        SE_ELp2 = math.exp(log_se)
        mean_log = float(np.mean(log_lp_sq))
        std_log = float(np.std(log_lp_sq, ddof=1))
        dt = time.time() - t0
        emit(f"N={N:3d} K={K:5d} skipped={sk:3d} dt={dt:.1f}s")
        emit(f"  log_max_seen = {m:+.3f}")
        emit(f"  mean(log Lp^2) = {mean_log:+.4f}  std(log Lp^2) = {std_log:.4f}")
        emit(f"  E|Lambda'(1)|^2 = {ELp2:.6e}  +/-  {SE_ELp2:.3e}")
        # Check leading power: try N^1, N^2, N^3, N^{3/2}
        for power, label in [(1.0, "N"), (1.5, "N^1.5"), (2.0, "N^2"), (3.0, "N^3")]:
            ratio = ELp2 / (N ** power)
            emit(f"  / {label:5s} = {ratio:.4e}  (compare across N)")
        emit("")
        so2n1_results[N] = (ELp2, SE_ELp2, mean_log, std_log)

    # ---- Fit leading-order coefficient ----
    emit("=" * 80)
    emit("Fits across N (assume E ~ C * N^p)")
    emit("=" * 80)

    # SO(2N)
    Ns = sorted(so2n_results.keys())
    Es = np.array([so2n_results[N][0] for N in Ns])
    SEs = np.array([so2n_results[N][1] for N in Ns])
    log_Ns = np.log(np.array(Ns, dtype=float))
    log_Es = np.log(Es)
    # Linear fit log E = log C + p log N
    A = np.vstack([log_Ns, np.ones_like(log_Ns)]).T
    p, log_C = np.linalg.lstsq(A, log_Es, rcond=None)[0]
    C = math.exp(log_C)
    emit(f"SO(2N)   E[Lambda(1)^2] ~ {C:.4e} * N^{p:+.3f}")
    emit(f"  (for SO(2N), E|Lambda'(1)|^2 = N^2 * E[L^2] ~ {C:.4e} * N^{p+2:+.3f})")
    emit("")

    Ns1 = sorted(so2n1_results.keys())
    Es1 = np.array([so2n1_results[N][0] for N in Ns1])
    log_Ns1 = np.log(np.array(Ns1, dtype=float))
    log_Es1 = np.log(Es1)
    A1 = np.vstack([log_Ns1, np.ones_like(log_Ns1)]).T
    p1, log_C1 = np.linalg.lstsq(A1, log_Es1, rcond=None)[0]
    C1 = math.exp(log_C1)
    emit(f"SO(2N+1) E|Lambda'(1)|^2 ~ {C1:.4e} * N^{p1:+.3f}")
    emit("")

    # ---- Verdict ----
    emit("=" * 80)
    emit("VERDICT")
    emit("=" * 80)
    emit("Reading off leading constants and powers:")
    emit(f"  SO(2N)   coeff (Lambda^2):  C ~ {C:.4f},  power ~ {p:+.3f}")
    emit(f"  SO(2N+1) coeff (|Lambda'|^2): C ~ {C1:.4f}, power ~ {p1:+.3f}")
    emit("")
    emit("For C2 to pass as user-stated (1/12 unitary baseline + d^{2k}/(2k)!=2/3):")
    emit("  Need orthogonal coefficient = 1/18 = 0.0556 [if interpreted multiplicatively]")
    emit("  OR = 1/12 = 0.0833 [if 16/24 already absorbed elsewhere]")
    emit("Hughes-Snaith standard result for SO(2N+1) derivative 2nd moment:")
    emit("  predicts power and constant (compute from Barnes G - check arXiv 0707.4129)")

    out_path = "/Users/saar/Farey 4.7 solutions/C2_orthogonal_MC.out"
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")
    emit(f"\nResults written to {out_path}")

if __name__ == "__main__":
    main()
