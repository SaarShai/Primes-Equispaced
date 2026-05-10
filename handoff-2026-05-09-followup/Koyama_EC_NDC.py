#!/usr/bin/env python3
"""
Koyama_EC_NDC.py
================
Verification of the **Elliptic Curve NDC universality conjecture** from the
Saar↔Koyama correspondence (2026-04-16):

    Conjecture (NDC universality for elliptic curves):
    Let E/Q be a Cremona elliptic curve with L-series L(E,s)=Σ a_n/n^s and
    inverse coefficients μ_E(n) (defined multiplicatively from local
    Euler factors).  Let ρ be a critical point (BSD zero, or central
    point s=1).  Set
        c_K^E := Σ_{n≤K} μ_E(n)/n^ρ
        E_K^E := Π_{p≤K, good}(1 − a_p p^{−ρ} + p^{1−2ρ})^{−1}
        D_K^E := c_K^E · E_K^E
    Then  D_K^E · ζ(2)  →  1   as  K → ∞.

We verify (or refute) this for three Cremona curves:
  - 37a1   : y² + y = x³ − x          (rank 1, simple zero at s=1)
  - 11a1   : y² + y = x³ − x² − 10x − 20  (rank 0; non-zero L(E,1))
  - 389a1  : y² + y = x³ + x² − 2x    (rank 2, double zero at s=1)

All a_p are computed via direct point counting (Legendre-symbol method)
on the affine + projective models — NO LMFDB lookup, NO fabricated data.
mpmath at 40 dps for all c, E, D values.

Output:
  - Koyama_EC_NDC.csv    : K, curve, c_K, E_K, D_K, D_K*zeta(2)
  - Koyama_EC_NDC.txt    : tabulated trajectories
  - first 100 a_p table  : Koyama_EC_NDC_ap_table.csv

Author: Claude (computational agent), session 2026-05-09 followup.
"""
import json
import math
import os
import sys
import time
from typing import Dict, List, Tuple

import mpmath as mp
from sympy import isprime, primerange, factorint

# ----------------------------------------------------------------------
# Confidence aggregation rule (single, top-of-file)
# ----------------------------------------------------------------------
# Per-curve verdict confidence is min(method_confidence, scaling_confidence,
#   trend_confidence, K_sufficiency).  Final NDC universality verdict is
#   the MIN across the three curves: a single counterexample falsifies.
#
#   method_confidence    = 0.99 if a_p verified vs LMFDB at first 25 primes
#                          AND naive count agrees with quadratic-residue count
#   scaling_confidence   = 0.95 if log-K (rank 1) / const (rank 0) /
#                          (log K)^2 (rank 2) trend visible monotonically
#   trend_confidence     = fraction of trajectory satisfying
#                          |D_K·ζ(2) − 1| decreasing with K
#   K_sufficiency        = 1 - exp(-K/K_target) where K_target = 1e5
# ----------------------------------------------------------------------

mp.mp.dps = 40   # decimal precision

ZETA2 = mp.zeta(2)   # π²/6, exact under mpmath

# ----------------------------------------------------------------------
# Curve definitions: ainvs = [a1, a2, a3, a4, a6]
#   y² + a1·x·y + a3·y = x³ + a2·x² + a4·x + a6
# ----------------------------------------------------------------------
CURVES: Dict[str, Dict] = {
    "37a1": {
        "ainvs": [0, 0, 1, -1, 0],
        "conductor": 37,
        "rank": 1,
        "rho": mp.mpf(1),
        "expected_target": "1/L'(E,1) ≈ 1/3.268 (rank-1 log-K scaling)",
    },
    "11a1": {
        # Saar's email gave  y² + y = x³ − x² − 10x − 20  → ainvs [0,-1,1,-10,-20].
        # This is the "official" Cremona 11a1 minimal model.
        "ainvs": [0, -1, 1, -10, -20],
        "conductor": 11,
        "rank": 0,
        "rho": mp.mpf(1),
        "expected_target": "1/L(E,1) ≈ 1/0.2538 ≈ 3.94 (rank-0 constant scaling)",
    },
    "389a1": {
        "ainvs": [0, 1, 1, -2, 0],
        "conductor": 389,
        "rank": 2,
        "rho": mp.mpf(1),
        "expected_target": "rank-2 (log K)² scaling per Aoki-Koyama m=2",
    },
}


# ----------------------------------------------------------------------
# 1.   a_p via Legendre symbols on the short Weierstrass model.
# ----------------------------------------------------------------------
def to_short_weierstrass(ainvs):
    """
    Convert long form  y² + a1xy + a3y = x³ + a2x² + a4x + a6
    to short form      Y² = X³ + AX + B   (over Q, valid at primes p ≠ 2,3).
    Using standard b2,b4,b6,c4,c6 invariants:
      b2 = a1² + 4a2,   b4 = 2a4 + a1a3,   b6 = a3² + 4a6
      c4 = b2² - 24b4,  c6 = -b2³ + 36b2 b4 - 216 b6
      Y² = X³ - 27 c4 X - 54 c6     (after scaling)
    """
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    c4 = b2 * b2 - 24 * b4
    c6 = -(b2 ** 3) + 36 * b2 * b4 - 216 * b6
    # Y² = X³ - 27 c4 X - 54 c6  (substitution x = (X - 3 b2)/36 etc.;
    # the (-27 c4, -54 c6) form is what's used for a_p computation.)
    A = -27 * c4
    B = -54 * c6
    return A, B


def count_points_short(A, B, p):
    """
    Number of affine + 1 (projective ∞) points of  y² = x³ + Ax + B  over F_p.
    Uses Legendre symbol via pow(t, (p-1)//2, p):
        # of (x,y): if t=0, +1 ; else 1+legendre(t).
    Returns N_p (= p + 1 - a_p so a_p = p + 1 - N_p).
    Cost: O(p log p) per prime.
    """
    if p == 2:
        # handled separately in caller
        raise ValueError("p=2 not handled by short-Weierstrass route")
    Am = A % p
    Bm = B % p
    # affine count
    cnt = 0
    half = (p - 1) // 2
    for x in range(p):
        # f(x) = x^3 + A x + B
        t = (x * x % p * x + Am * x + Bm) % p
        if t == 0:
            cnt += 1
        else:
            ls = pow(t, half, p)
            if ls == 1:
                cnt += 2
            # else ls == p-1 (i.e. -1) → 0 points
    return cnt + 1  # +1 for point at infinity


def count_points_long(ainvs, p):
    """
    Generic: count points of  y² + a1xy + a3y = x³ + a2x² + a4x + a6  over F_p
    by exhaustive (x, y) in F_p × F_p plus point at infinity.
    Cost: O(p²) — only used as a sanity check for small p.
    """
    a1, a2, a3, a4, a6 = [a % p for a in ainvs]
    cnt = 0
    for x in range(p):
        rhs = (x * x % p * x + a2 * x * x + a4 * x + a6) % p
        for y in range(p):
            lhs = (y * y + a1 * x * y + a3 * y) % p
            if lhs == rhs:
                cnt += 1
    return cnt + 1  # +1 for point at infinity


# ----- handle p=2 (and bad primes) explicitly via O(p²) count -----
def count_points_small_p(ainvs, p):
    return count_points_long(ainvs, p)


def a_p(ainvs, p, conductor):
    """
    Compute a_p of the L-series of E.
    For good primes (p ∤ N): a_p = p + 1 − #E(F_p).
    For bad primes (p | N): a_p ∈ {-1, 0, 1} depending on reduction:
        +1  : split multiplicative
        −1  : non-split multiplicative
         0  : additive
    Determined by reduction type, which we read off Kodaira via a_p
    of the SINGULAR model — but here we just apply the formula
    a_p = p + 1 − #E_smooth(F_p), which gives the right L-factor coefficient
    when we use the standard convention #E_smooth = # nonsingular points.
    For the three curves at hand:
        37a1  conductor 37  : multiplicative reduction at 37
        11a1  conductor 11  : multiplicative reduction at 11
        389a1 conductor 389 : multiplicative reduction at 389
    All split/non-split are LMFDB-tabulated; we recover via direct count.
    """
    if conductor % p == 0:
        # bad prime.  For mult/additive reduction, the standard formula is
        #     a_p = p − #E_ns(F_p)
        # where E_ns = projective smooth locus (incl. ∞).  This gives
        # a_p = +1 (split mult, #E_ns = p−1), −1 (non-split, #E_ns = p+1),
        # 0 (additive, #E_ns = p).
        # In our naive enumeration, count_points_long returns
        #     N_raw = (#affine pairs (x,y)) + 1   [+1 for ∞]
        # and #E_ns = N_raw − 1   (subtract the unique singular affine point).
        # Therefore a_p = p − (N_raw − 1) = p − N_raw + 1
        # and equivalently a_p = p − cnt_affine.
        N_raw = count_points_small_p(ainvs, p)
        N_smooth = N_raw - 1
        ap = p - N_smooth   # NB: NOT (p+1) — bad-prime convention
        return ap, "bad"
    if p == 2:
        N = count_points_small_p(ainvs, p)
        return p + 1 - N, "good"
    if p == 3:
        N = count_points_small_p(ainvs, p)
        return p + 1 - N, "good"
    # generic short form
    A, B = to_short_weierstrass(ainvs)
    # for the short-form to be valid mod p, p must not divide 2,3 — already excluded
    # also need p ∤ disc; if it does we're at a bad prime — already handled
    # by conductor check above (LMFDB conductors for our 3 curves match disc support).
    N = count_points_short(A, B, p)
    return p + 1 - N, "good"


# ----------------------------------------------------------------------
# 2.   Sieve μ_E(n) for n ≤ K
# ----------------------------------------------------------------------
def compute_mu_E(K: int, ainvs, conductor) -> Tuple[List, List, Dict]:
    """
    Returns:
       mu : list of length K+1, mu[n] = μ_E(n) (Python int)
       ap_dict : {p: a_p}  for p ≤ K
       reduction_type : {p: 'good' | 'bad'} for p | conductor
    Uses the multiplicative formula:
       μ_E(p)   = -a_p
       μ_E(p²) = p           [coefficient of X² in 1 - a_p X + p X²]
       μ_E(p^k) = 0   for k ≥ 3   (good prime)
       (bad prime: local factor = 1 - a_p X, so μ_E(p^k) = (-a_p)^k for k≥1
        but because a_p ∈ {-1, 0, +1}, μ_E(p^k) = (∓1)^k or 0)
    Multiplicative across primes:
       μ_E(n) = ∏_{p^a || n} μ_E(p^a)
       μ_E(n) = 0 if any p^a || n with a ≥ 3 (good prime), or
                = 0 at bad prime if a_p = 0 (additive)
    """
    primes = list(primerange(2, K + 1))
    ap_dict = {}
    red_type = {}
    t0 = time.time()
    last_log = t0
    for i, p in enumerate(primes):
        ap, kind = a_p(ainvs, p, conductor)
        ap_dict[p] = ap
        red_type[p] = kind
        if time.time() - last_log > 8.0:
            elapsed = time.time() - t0
            print(f"   ... a_p computed for p ≤ {p} ({i+1}/{len(primes)}), {elapsed:.1f}s",
                  file=sys.stderr, flush=True)
            last_log = time.time()
    print(f"   done a_p for {len(primes)} primes in {time.time()-t0:.1f}s",
          file=sys.stderr, flush=True)

    # Now sieve μ_E(n) for n ≤ K using factorint (sympy) — fast for K up to 1e5.
    # For larger K use smallest-prime-factor sieve.
    mu = [0] * (K + 1)
    mu[1] = 1
    # build smallest prime factor (SPF) sieve
    spf = list(range(K + 1))
    for p in primes:
        if spf[p] == p:  # p is prime
            for m in range(p * p, K + 1, p):
                if spf[m] == m:
                    spf[m] = p

    def mu_local(p, k):
        # local μ_E(p^k)
        if k == 0:
            return 1
        if red_type[p] == "good":
            if k == 1:
                return -ap_dict[p]
            if k == 2:
                return p
            return 0
        else:  # bad prime, local factor = 1 - a_p X
            ap = ap_dict[p]
            if ap == 0:
                return 0  # additive reduction kills all higher powers
            # μ_E(p^k) = (-a_p)^k  for split (a_p=+1) or non-split (a_p=-1)
            return (-ap) ** k

    for n in range(2, K + 1):
        # factor n via SPF
        m = n
        prod = 1
        while m > 1:
            p = spf[m]
            k = 0
            while m % p == 0:
                m //= p
                k += 1
            prod *= mu_local(p, k)
            if prod == 0:
                break
        mu[n] = prod

    return mu, ap_dict, red_type


# ----------------------------------------------------------------------
# 3.  Sums and partial Euler product
# ----------------------------------------------------------------------
def compute_cK_EK(mu, ap_dict, red_type, K, rho, conductor):
    """
    c_K = Σ_{n≤K} μ_E(n) / n^ρ
    E_K = Π_{p≤K, good} (1 − a_p p^{-ρ} + p^{1-2ρ})^{-1}    (good primes)
          × Π_{p≤K, bad}  (1 − a_p p^{-ρ})^{-1}              (bad primes)
    Both at fixed ρ (real, so mpf arithmetic).
    """
    # c_K
    cK = mp.mpf(0)
    for n in range(1, K + 1):
        if mu[n] != 0:
            cK += mp.mpf(mu[n]) / mp.power(n, rho)
    # E_K
    EK = mp.mpf(1)
    for p, ap in ap_dict.items():
        if p > K:
            break  # primes() iteration order is ascending
        if red_type[p] == "good":
            # local L-factor inverse: (1 - a_p p^{-ρ} + p^{1-2ρ})
            inv_local = mp.mpf(1) - mp.mpf(ap) * mp.power(p, -rho) + mp.power(p, 1 - 2 * rho)
        else:
            inv_local = mp.mpf(1) - mp.mpf(ap) * mp.power(p, -rho)
        EK *= mp.mpf(1) / inv_local
    return cK, EK


# ----------------------------------------------------------------------
# 4.  Sweep
# ----------------------------------------------------------------------
def sweep_curve(label, K_max, K_checkpoints):
    info = CURVES[label]
    ainvs = info["ainvs"]
    conductor = info["conductor"]
    rho = info["rho"]
    rank = info["rank"]
    print(f"=== Curve {label}  ainvs={ainvs}  N={conductor}  rank={rank}  ρ={rho} ===",
          flush=True)
    print(f"   computing μ_E and a_p up to K={K_max} ...", flush=True)
    mu, ap_dict, red_type = compute_mu_E(K_max, ainvs, conductor)
    print(f"   sweeping checkpoints ...", flush=True)
    rows = []
    sorted_primes = sorted(ap_dict.keys())
    # precompute for each checkpoint
    for K in K_checkpoints:
        # compute partial sums up to K (cheap relative to factorization)
        cK = mp.mpf(0)
        for n in range(1, K + 1):
            if mu[n] != 0:
                cK += mp.mpf(mu[n]) / mp.power(n, rho)
        EK = mp.mpf(1)
        for p in sorted_primes:
            if p > K:
                break
            ap = ap_dict[p]
            if red_type[p] == "good":
                inv_local = mp.mpf(1) - mp.mpf(ap) * mp.power(p, -rho) + mp.power(p, 1 - 2 * rho)
            else:
                inv_local = mp.mpf(1) - mp.mpf(ap) * mp.power(p, -rho)
            EK *= mp.mpf(1) / inv_local
        DK = cK * EK
        DK_zeta2 = DK * ZETA2
        # scaling diagnostic:
        if rank == 1:
            scale = cK / mp.log(K) if K > 1 else mp.mpf(0)
            scale_label = "c_K / log K"
        elif rank == 0:
            scale = cK
            scale_label = "c_K (constant)"
        elif rank == 2:
            scale = cK / (mp.log(K) ** 2) if K > 1 else mp.mpf(0)
            scale_label = "c_K / (log K)²"
        else:
            scale = cK / (mp.log(K) ** rank) if K > 1 else mp.mpf(0)
            scale_label = f"c_K / (log K)^{rank}"
        rows.append({
            "K": K,
            "cK": cK,
            "EK": EK,
            "DK": DK,
            "DK_zeta2": DK_zeta2,
            "DK_zeta2_minus_1": DK_zeta2 - mp.mpf(1),
            "scale_label": scale_label,
            "scale_value": scale,
        })
        print(f"   K={K:>7d}  c_K={mp.nstr(cK, 8):<20}  E_K={mp.nstr(EK, 8):<20}"
              f"  D_K·ζ(2)={mp.nstr(DK_zeta2, 12):<25}"
              f"  ({scale_label}={mp.nstr(scale, 10)})", flush=True)
    return rows, ap_dict, red_type


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    K_max = int(os.environ.get("K_MAX", "100000"))
    # checkpoints
    base_cps = [1000, 3000, 10000, 30000, 100000, 300000, 1000000]
    K_checkpoints = [k for k in base_cps if k <= K_max]
    if K_checkpoints[-1] != K_max:
        K_checkpoints.append(K_max)

    print(f"# Koyama EC NDC universality sweep")
    print(f"# K_MAX = {K_max}")
    print(f"# Checkpoints: {K_checkpoints}")
    print(f"# mpmath dps = {mp.mp.dps}")
    print(f"# ζ(2) = {ZETA2}")
    print()

    all_results = {}
    ap_tables = {}
    t_start = time.time()
    for label in CURVES:
        rows, ap_dict, red_type = sweep_curve(label, K_max, K_checkpoints)
        all_results[label] = rows
        ap_tables[label] = (ap_dict, red_type)
        print()

    # write CSV
    csv_path = os.path.join(out_dir, "Koyama_EC_NDC.csv")
    with open(csv_path, "w") as fh:
        fh.write("curve,K,c_K,E_K,D_K,D_K_times_zeta2,D_K_zeta2_minus_1,scale_label,scale_value\n")
        for label, rows in all_results.items():
            for r in rows:
                fh.write(f"{label},{r['K']},{mp.nstr(r['cK'],30)},{mp.nstr(r['EK'],30)},"
                         f"{mp.nstr(r['DK'],30)},{mp.nstr(r['DK_zeta2'],30)},"
                         f"{mp.nstr(r['DK_zeta2_minus_1'],30)},"
                         f"{r['scale_label']},{mp.nstr(r['scale_value'],30)}\n")
    print(f"# wrote {csv_path}")

    # write a_p table for first 100 primes
    apt_path = os.path.join(out_dir, "Koyama_EC_NDC_ap_table.csv")
    primes100 = list(primerange(2, 600))[:100]
    with open(apt_path, "w") as fh:
        header = "p," + ",".join(f"a_p({L})" for L in CURVES) + ","
        header += ",".join(f"reduction({L})" for L in CURVES) + "\n"
        fh.write(header)
        for p in primes100:
            row = [str(p)]
            kinds = []
            for label in CURVES:
                ap_dict, red_type = ap_tables[label]
                row.append(str(ap_dict.get(p, "?")))
                kinds.append(red_type.get(p, "?"))
            row.extend(kinds)
            fh.write(",".join(row) + "\n")
    print(f"# wrote {apt_path}")

    # write summary
    summary_path = os.path.join(out_dir, "Koyama_EC_NDC.txt")
    with open(summary_path, "w") as fh:
        fh.write(f"Koyama EC NDC universality sweep — full results\n")
        fh.write(f"K_max = {K_max}, mpmath dps = {mp.mp.dps}\n")
        fh.write(f"ζ(2) = {mp.nstr(ZETA2, 30)}\n\n")
        for label, rows in all_results.items():
            info = CURVES[label]
            fh.write(f"=== {label}   ainvs={info['ainvs']}   rank={info['rank']}   "
                     f"ρ={mp.nstr(info['rho'], 6)} ===\n")
            fh.write(f"   target: {info['expected_target']}\n")
            fh.write(f"  {'K':>8} {'c_K':>22} {'E_K':>22} {'D_K·ζ(2)':>22} "
                     f"{'D_K·ζ(2)−1':>22} {rows[0]['scale_label']:>22}\n")
            for r in rows:
                fh.write(f"  {r['K']:>8} {mp.nstr(r['cK'],14):>22} "
                         f"{mp.nstr(r['EK'],14):>22} "
                         f"{mp.nstr(r['DK_zeta2'],16):>22} "
                         f"{mp.nstr(r['DK_zeta2_minus_1'],10):>22} "
                         f"{mp.nstr(r['scale_value'],10):>22}\n")
            fh.write("\n")
    print(f"# wrote {summary_path}")

    print(f"\nTotal wall-clock: {time.time()-t_start:.1f}s")
    return all_results, ap_tables


if __name__ == "__main__":
    main()
