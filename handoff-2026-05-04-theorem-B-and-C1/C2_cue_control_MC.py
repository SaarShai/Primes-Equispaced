#!/usr/bin/env python3
"""C2 control: CUE Haar second moment of |Lambda_A(1)|^2 and |Lambda'_A(1)|^2.

For unitary matrices A in U(N), Lambda_A(z) = det(I - z A) has eigenvalues
e^{i phi_j}, j = 1..N (no conjugate pairing).  At z=1:
   Lambda_A(1) = prod_j (1 - e^{i phi_j})
This is complex-valued.  The standard 'derivative moment' of CUE
(Hughes-Mezzadri-Pearce 2003) involves
   d/dz log Lambda_A(z) | _{z=1} = sum_j (-e^{i phi_j} / (1 - e^{i phi_j}))
or equivalently the angle derivative Z'(theta) at the symmetry point.

Hughes-Mezzadri-Pearce (or 'Hughes thesis 2001') CUE result:
   E_{U(N)} |Lambda'_A(1) / Lambda_A(1)|^2  has well-defined N-dependence.
The 1/12 = G(3)^2/G(5) appears as the leading constant of a particular
2nd derivative-moment normalization.

We measure several CUE statistics for cross-comparison with SO(2N) MC:
  1. E[|Lambda(1)|^2]  (CUE value moment - Keating-Snaith)
  2. E[|Lambda'(1)|^2] (raw derivative)
  3. E[|Lambda'(1) / Lambda(1)|^2] (logarithmic derivative -- well-defined
     when |Lambda(1)| > 0 a.s., which holds for CUE).

Compare to SO(2N) coefficients to extract the ratio (should be 8 if the
'at-zeros 1/12 -> 2/3' identification holds).
"""
import numpy as np
import time
import math

def haar_unitary(n, rng):
    """Mezzadri 2007 CUE sampling."""
    Z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z)
    d = np.diagonal(R)
    ph = d / np.abs(d)
    Q = Q * ph
    return Q

def cue_eigangles(Q):
    w = np.linalg.eigvals(Q)
    return np.angle(w)

def main():
    out_lines = []
    def emit(s):
        print(s, flush=True)
        out_lines.append(s)

    emit("# C2 CUE control MC")
    emit("# Compare CUE value moments and derivative log-moments")
    emit("")

    plan = [(50, 10000), (100, 10000), (200, 4000)]
    rng = np.random.default_rng(20260504)

    for (N, K) in plan:
        t0 = time.time()
        # Storage
        lam_abs2 = np.empty(K)         # |Lambda(1)|^2
        lprime_abs2 = np.empty(K)      # |Lambda'(1)|^2
        loglder_abs2 = np.empty(K)     # |Lambda'(1)/Lambda(1)|^2

        for k in range(K):
            Q = haar_unitary(N, rng)
            phi = cue_eigangles(Q)
            # Lambda(1) = prod_j (1 - e^{i phi_j})
            ones_minus_ev = 1.0 - np.exp(1j * phi)
            lam = np.prod(ones_minus_ev)
            # log derivative at z=1: d/dz log Lambda(z) | _1 = sum_j (-e^{i phi_j} / (1 - e^{i phi_j}))
            # = sum_j -1 / (e^{-i phi_j} - 1)
            # rewrite to avoid 1/0 if any phi very close to 0 (no-op for most CUE samples)
            with np.errstate(divide='ignore', invalid='ignore'):
                logder = np.sum(- np.exp(1j * phi) / ones_minus_ev)
            lprime = logder * lam
            lam_abs2[k] = (lam * np.conjugate(lam)).real
            lprime_abs2[k] = (lprime * np.conjugate(lprime)).real
            loglder_abs2[k] = (logder * np.conjugate(logder)).real

        dt = time.time() - t0
        E_lam2 = np.mean(lam_abs2); SE_lam2 = np.std(lam_abs2, ddof=1) / math.sqrt(K)
        E_lp2 = np.mean(lprime_abs2); SE_lp2 = np.std(lprime_abs2, ddof=1) / math.sqrt(K)
        E_ll2 = np.mean(loglder_abs2); SE_ll2 = np.std(loglder_abs2, ddof=1) / math.sqrt(K)

        emit(f"CUE N={N:3d} K={K:5d}  dt={dt:.1f}s")
        emit(f"  E[|Lambda(1)|^2]      = {E_lam2:.4e} +/- {SE_lam2:.2e}")
        emit(f"  E[|Lambda'(1)|^2]     = {E_lp2:.4e} +/- {SE_lp2:.2e}")
        emit(f"  E[|L'/L|^2]           = {E_ll2:.4e} +/- {SE_ll2:.2e}")
        emit(f"  E[|Lambda'|^2] / N^3  = {E_lp2 / N**3:.4e}")
        emit(f"  E[|L'/L|^2] / N^2     = {E_ll2 / N**2:.4e}  -- expect 1/12 ~ {1/12:.4f}? or other")
        emit(f"  E[|L'/L|^2] / N       = {E_ll2 / N:.4e}")
        emit("")

    out_path = "/Users/saar/Farey 4.7 solutions/C2_cue_control_MC.out"
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"Written to {out_path}")

if __name__ == "__main__":
    main()
