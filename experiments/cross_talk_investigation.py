#!/usr/bin/env python3
"""
Cross-Talk Investigation: Why does L-function cross-talk appear with all primes
but disappear with M(p)=-3 restriction?

HYPOTHESES:
1. Arithmetic coupling via M(p): T_chi7 correlates with M(p), and M(p) correlates
   with T_plain's zeta-zero signal. Fixing M(p) breaks this chain.
2. Shared mu(p)=-1: All primes have mu(p)=-1, creating sample bias.
3. The M(p)=-3 filter decorrelates by fixing cumulative Mobius.

TESTS:
A) Compute correlation between T_chi7(N) and M(p) for all primes
B) Compute partial correlation of T_chi7 with zeta-phase after conditioning on M(p)
C) Test cross-talk for primes with M(p)=0 (different Mertens constraint)
D) Test cross-talk for primes with M(p)=-1 (most common value)
E) Test with RANDOM subsample of same size as M(p)=-3 set
"""

import numpy as np
from math import log, pi, sqrt, gcd
import time
import sys

LIMIT = 1_000_000
PRIME_LIMIT = 50_000

def make_sieve(limit):
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue
        mu[p::p] *= -1
        p2 = p * p
        if p2 <= limit:
            mu[p2::p2] = 0
        for j in range(2 * p, limit + 1, p):
            is_prime[j] = False
    return mu

def make_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = False
    return np.nonzero(sieve)[0]

def chi_mod7_quad(n):
    r = n % 7
    if r == 0: return 0
    if r in (1, 2, 4): return 1
    return -1

def compute_twisted_mertens(mu, chi_func, limit):
    M = np.zeros(limit + 1, dtype=np.float64)
    running = 0.0
    for k in range(1, limit + 1):
        running += mu[k] * chi_func(k)
        M[k] = running
    return M

def compute_T_fast(M_arr, N):
    sqN = int(N**0.5)
    total = 0.0
    for m in range(2, sqN + 1):
        total += M_arr[N // m] / m
    for k in range(1, sqN + 1):
        m_lo = max(N // (k + 1) + 1, sqN + 1)
        m_hi = N // k
        if m_lo > m_hi:
            continue
        harm_sum = sum(1.0 / m for m in range(m_lo, m_hi + 1))
        total += M_arr[k] * harm_sum
    return total

def compute_resultant(phases):
    if len(phases) == 0:
        return 0.0
    z = np.exp(1j * np.array(phases))
    return abs(np.mean(z))

def phase_lock_test(T_vals, phases, label=""):
    """Return sigma for T>0 and T<0 subsets."""
    pos = T_vals > 0
    neg = T_vals < 0
    n_pos = np.sum(pos)
    n_neg = np.sum(neg)

    R_pos = compute_resultant(phases[pos]) if n_pos > 0 else 0.0
    R_neg = compute_resultant(phases[neg]) if n_neg > 0 else 0.0

    sigma_pos = R_pos * sqrt(n_pos) if n_pos > 0 else 0.0
    sigma_neg = R_neg * sqrt(n_neg) if n_neg > 0 else 0.0

    return {
        'label': label,
        'n': len(T_vals), 'n_pos': int(n_pos), 'n_neg': int(n_neg),
        'R_pos': R_pos, 'R_neg': R_neg,
        'sigma_pos': sigma_pos, 'sigma_neg': sigma_neg,
        'max_sigma': max(sigma_pos, sigma_neg),
        'frac_pos': n_pos / len(T_vals) if len(T_vals) > 0 else 0,
    }

def print_test(res):
    verdict = "STRONG" if res['max_sigma'] > 3.0 else "MOD" if res['max_sigma'] > 2.0 else "WEAK" if res['max_sigma'] > 1.5 else "NONE"
    print(f"  {res['label'][:70]:<72} n={res['n']:5d} frac+={res['frac_pos']:.3f} "
          f"sig+={res['sigma_pos']:5.1f}x sig-={res['sigma_neg']:5.1f}x max={res['max_sigma']:5.1f}x [{verdict}]")

def main():
    t_start = time.time()
    print("=" * 120)
    print("CROSS-TALK INVESTIGATION: Why does zeta zero appear in T_chi7 for all primes?")
    print("=" * 120)

    # === SIEVE AND SETUP ===
    print("\n[1/7] Sieving...")
    mu = make_sieve(LIMIT)
    primes = make_primes(LIMIT)
    print(f"  {len(primes)} primes up to {LIMIT}")

    # Compute Mertens function M(n)
    print("[2/7] Computing Mertens M(n) and M_chi7(n)...")
    M_plain = np.zeros(LIMIT + 1, dtype=np.float64)
    running = 0.0
    for k in range(1, LIMIT + 1):
        running += mu[k]
        M_plain[k] = running

    M_chi7 = compute_twisted_mertens(mu, chi_mod7_quad, LIMIT)

    # Prime subsets
    all_p = np.array([int(p) for p in primes if p <= PRIME_LIMIT])
    M_at_p = np.array([M_plain[p] for p in all_p])

    # Various M(p) restricted sets
    m3_mask = M_at_p == -3
    m0_mask = M_at_p == 0
    m1_mask = M_at_p == -1
    m2_mask = M_at_p == -2

    print(f"  All primes <= {PRIME_LIMIT}: {len(all_p)}")
    print(f"  M(p) = -3: {np.sum(m3_mask)}")
    print(f"  M(p) = -2: {np.sum(m2_mask)}")
    print(f"  M(p) = -1: {np.sum(m1_mask)}")
    print(f"  M(p) =  0: {np.sum(m0_mask)}")

    # Distribution of M(p)
    print("\n  M(p) distribution for primes <= 50000:")
    for mv in range(-8, 5):
        cnt = np.sum(M_at_p == mv)
        if cnt > 0:
            print(f"    M(p) = {mv:3d}: {cnt:5d} primes ({100*cnt/len(all_p):.1f}%)")

    # === COMPUTE T VALUES ===
    print(f"\n[3/7] Computing T_plain and T_chi7 for all {len(all_p)} primes...")
    T_plain = np.zeros(len(all_p))
    T_chi7 = np.zeros(len(all_p))
    t0 = time.time()
    for i, p in enumerate(all_p):
        T_plain[i] = compute_T_fast(M_plain, int(p))
        T_chi7[i] = compute_T_fast(M_chi7, int(p))
        if (i + 1) % 1000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (len(all_p) - i - 1) / rate
            print(f"    {i+1}/{len(all_p)} ({elapsed:.0f}s, ETA {eta:.0f}s)", file=sys.stderr)
    dt = time.time() - t0
    print(f"  Done in {dt:.1f}s")

    # === TEST A: CORRELATION BETWEEN T_chi7 AND M(p) ===
    print(f"\n{'='*120}")
    print("TEST A: Correlation between T_chi7(p-1) and M(p)")
    print(f"{'='*120}")

    corr_chi7_M = np.corrcoef(T_chi7, M_at_p)[0, 1]
    corr_plain_M = np.corrcoef(T_plain, M_at_p)[0, 1]
    corr_chi7_plain = np.corrcoef(T_chi7, T_plain)[0, 1]

    print(f"  corr(T_chi7, M(p))    = {corr_chi7_M:.6f}")
    print(f"  corr(T_plain, M(p))   = {corr_plain_M:.6f}")
    print(f"  corr(T_chi7, T_plain) = {corr_chi7_plain:.6f}")

    # Significance of correlations (Fisher z-test)
    n = len(all_p)
    for name, r in [("T_chi7 vs M(p)", corr_chi7_M),
                     ("T_plain vs M(p)", corr_plain_M),
                     ("T_chi7 vs T_plain", corr_chi7_plain)]:
        z = 0.5 * np.log((1 + r) / (1 - r)) * sqrt(n - 3)
        print(f"    {name:25s}: r = {r:.6f}, z = {z:.1f} (significant if |z| > 2)")

    # === TEST B: PHASE-LOCK AT ZETA ZERO, VARIOUS SUBSETS ===
    print(f"\n{'='*120}")
    print("TEST B: T_chi7 phase-lock at ZETA zero (gamma=14.13) for various prime subsets")
    print(f"{'='*120}")

    gamma_zeta = 14.134725142
    gamma_chi7 = 4.97340925

    # All primes
    log_p = np.log(all_p.astype(np.float64))
    phases_zeta = (gamma_zeta * log_p) % (2 * pi)
    phases_chi7 = (gamma_chi7 * log_p) % (2 * pi)

    print("\n  --- T_chi7 at ZETA zero (cross-talk test) ---")
    print_test(phase_lock_test(T_chi7, phases_zeta, "ALL primes"))
    for mv, mask, lbl in [(-3, m3_mask, "M(p)=-3"), (-2, m2_mask, "M(p)=-2"),
                           (-1, m1_mask, "M(p)=-1"), (0, m0_mask, "M(p)=0")]:
        if np.sum(mask) > 20:
            print_test(phase_lock_test(T_chi7[mask], phases_zeta[mask], lbl))

    # Random subsamples of same size as M(p)=-3 set
    n_m3 = int(np.sum(m3_mask))
    print(f"\n  --- Random subsamples (n={n_m3}, 10 trials) ---")
    np.random.seed(42)
    rand_sigmas = []
    for trial in range(10):
        idx = np.random.choice(len(all_p), n_m3, replace=False)
        res = phase_lock_test(T_chi7[idx], phases_zeta[idx], f"Random subsample #{trial+1}")
        rand_sigmas.append(res['max_sigma'])
        if trial < 3:
            print_test(res)
    print(f"  Random subsample max_sigma: mean={np.mean(rand_sigmas):.2f}, std={np.std(rand_sigmas):.2f}")

    # === TEST C: CONTROL - T_chi7 AT OWN ZERO ===
    print(f"\n  --- T_chi7 at OWN zero (gamma={gamma_chi7}) ---")
    print_test(phase_lock_test(T_chi7, phases_chi7, "ALL primes at chi7 zero"))
    for mv, mask, lbl in [(-3, m3_mask, "M(p)=-3"), (-2, m2_mask, "M(p)=-2"),
                           (-1, m1_mask, "M(p)=-1"), (0, m0_mask, "M(p)=0")]:
        if np.sum(mask) > 20:
            print_test(phase_lock_test(T_chi7[mask], phases_chi7[mask], f"{lbl} at chi7 zero"))

    # === TEST D: T_plain at ZETA zero for comparison ===
    print(f"\n  --- T_plain at ZETA zero (baseline) ---")
    print_test(phase_lock_test(T_plain, phases_zeta, "ALL primes"))
    for mv, mask, lbl in [(-3, m3_mask, "M(p)=-3"), (-2, m2_mask, "M(p)=-2"),
                           (-1, m1_mask, "M(p)=-1"), (0, m0_mask, "M(p)=0")]:
        if np.sum(mask) > 20:
            print_test(phase_lock_test(T_plain[mask], phases_zeta[mask], lbl))

    # === TEST E: PARTIAL CORRELATION ===
    print(f"\n{'='*120}")
    print("TEST E: Partial correlation — does conditioning on M(p) remove cross-talk?")
    print(f"{'='*120}")

    # Compute the "zeta signal" = cos(gamma_zeta * log(p))
    # The phase-lock means T_plain's sign correlates with this signal
    zeta_signal = np.cos(gamma_zeta * log_p)

    # Direct correlation of T_chi7 with zeta signal
    corr_direct = np.corrcoef(T_chi7, zeta_signal)[0, 1]

    # Partial correlation: corr(T_chi7, zeta_signal | M(p))
    # Using residuals from linear regression on M(p)
    from numpy.linalg import lstsq

    # Regress T_chi7 on M(p)
    A = np.column_stack([M_at_p, np.ones(n)])
    coef_chi7, _, _, _ = lstsq(A, T_chi7, rcond=None)
    resid_chi7 = T_chi7 - A @ coef_chi7

    # Regress zeta_signal on M(p)
    coef_zeta, _, _, _ = lstsq(A, zeta_signal, rcond=None)
    resid_zeta = zeta_signal - A @ coef_zeta

    corr_partial_linear = np.corrcoef(resid_chi7, resid_zeta)[0, 1]

    print(f"  corr(T_chi7, cos(gamma_zeta*log p))             = {corr_direct:.6f}")
    print(f"  partial corr (linear in M(p))                    = {corr_partial_linear:.6f}")
    print(f"  Reduction: {100*(1 - abs(corr_partial_linear)/abs(corr_direct)):.1f}%")

    # Non-parametric: condition on M(p) by stratification
    print(f"\n  Stratified analysis (within each M(p) stratum):")
    strat_corrs = []
    for mv in range(-8, 5):
        mask = M_at_p == mv
        cnt = np.sum(mask)
        if cnt < 50:
            continue
        r = np.corrcoef(T_chi7[mask], zeta_signal[mask])[0, 1]
        strat_corrs.append((mv, cnt, r))
        print(f"    M(p)={mv:3d}: n={cnt:5d}, corr(T_chi7, zeta_signal) = {r:.6f}")

    # Pooled within-stratum correlation
    if strat_corrs:
        weighted_r = sum(cnt * r for _, cnt, r in strat_corrs) / sum(cnt for _, cnt, _ in strat_corrs)
        print(f"  Weighted within-stratum correlation: {weighted_r:.6f}")

    # === TEST F: SIGN BALANCE ANALYSIS ===
    print(f"\n{'='*120}")
    print("TEST F: Sign balance — is the cross-talk driven by unbalanced T>0/T<0 split?")
    print(f"{'='*120}")

    frac_pos_all = np.mean(T_chi7 > 0)
    print(f"  T_chi7 > 0 fraction (all primes): {frac_pos_all:.4f}")
    for mv, mask, lbl in [(-3, m3_mask, "M(p)=-3"), (-2, m2_mask, "M(p)=-2"),
                           (-1, m1_mask, "M(p)=-1"), (0, m0_mask, "M(p)=0")]:
        if np.sum(mask) > 20:
            frac = np.mean(T_chi7[mask] > 0)
            print(f"  T_chi7 > 0 fraction ({lbl}): {frac:.4f} (n={np.sum(mask)})")

    # Check: does the zeta-zero sigma scale with the imbalance?
    print(f"\n  Phase-lock sigma vs sign imbalance:")
    for mv in range(-8, 5):
        mask = M_at_p == mv
        cnt = int(np.sum(mask))
        if cnt < 50:
            continue
        frac = np.mean(T_chi7[mask] > 0)
        res = phase_lock_test(T_chi7[mask], phases_zeta[mask], f"M(p)={mv}")
        print(f"    M(p)={mv:3d}: n={cnt:5d} frac+={frac:.3f} max_sigma={res['max_sigma']:.2f}")

    # === TEST G: RESAMPLING TEST ===
    print(f"\n{'='*120}")
    print("TEST G: Balanced resampling — subsample all primes to have 50/50 sign split")
    print(f"{'='*120}")

    pos_idx = np.where(T_chi7 > 0)[0]
    neg_idx = np.where(T_chi7 < 0)[0]
    n_min = min(len(pos_idx), len(neg_idx))
    print(f"  Positive: {len(pos_idx)}, Negative: {len(neg_idx)}")
    print(f"  Balancing to {n_min} each")

    np.random.seed(123)
    balanced_sigmas = []
    for trial in range(10):
        sel_pos = np.random.choice(pos_idx, n_min, replace=False)
        sel_neg = np.random.choice(neg_idx, n_min, replace=False)
        sel = np.concatenate([sel_pos, sel_neg])
        res = phase_lock_test(T_chi7[sel], phases_zeta[sel], f"Balanced trial #{trial+1}")
        balanced_sigmas.append(res['max_sigma'])
        if trial < 3:
            print_test(res)
    print(f"  Balanced subsample max_sigma: mean={np.mean(balanced_sigmas):.2f}, std={np.std(balanced_sigmas):.2f}")

    # === TEST H: DIRECT TEST — does T_chi7(p) depend on M(p)? ===
    print(f"\n{'='*120}")
    print("TEST H: T_chi7(p-1) vs M(p) — direct dependence")
    print(f"{'='*120}")

    # Mean T_chi7 stratified by M(p)
    print(f"  Mean T_chi7(p-1) by M(p) stratum:")
    for mv in range(-8, 5):
        mask = M_at_p == mv
        cnt = int(np.sum(mask))
        if cnt < 30:
            continue
        mean_t = np.mean(T_chi7[mask])
        std_t = np.std(T_chi7[mask])
        mean_tp = np.mean(T_plain[mask])
        print(f"    M(p)={mv:3d}: n={cnt:5d} mean(T_chi7)={mean_t:8.4f} std={std_t:.4f} mean(T_plain)={mean_tp:8.4f}")

    # Check: does T_chi7 / sqrt(p) depend on M(p)?
    T_chi7_normalized = T_chi7 / np.sqrt(all_p.astype(np.float64))
    T_plain_normalized = T_plain / np.sqrt(all_p.astype(np.float64))

    print(f"\n  Normalized T_chi7(p-1)/sqrt(p) by M(p) stratum:")
    for mv in range(-8, 5):
        mask = M_at_p == mv
        cnt = int(np.sum(mask))
        if cnt < 30:
            continue
        mean_t = np.mean(T_chi7_normalized[mask])
        std_t = np.std(T_chi7_normalized[mask]) / sqrt(cnt)  # SEM
        print(f"    M(p)={mv:3d}: n={cnt:5d} mean(T_chi7/sqrt(p))={mean_t:10.6f} +/- {std_t:.6f}")

    # === SUMMARY ===
    print(f"\n{'='*120}")
    print("SUMMARY")
    print(f"{'='*120}")
    print(f"  corr(T_chi7, M(p))          = {corr_chi7_M:.6f}")
    print(f"  corr(T_chi7, T_plain)       = {corr_chi7_plain:.6f}")
    print(f"  corr(T_chi7, zeta_signal)   = {corr_direct:.6f}")
    print(f"  partial corr (cond on M(p)) = {corr_partial_linear:.6f}")
    print(f"  Total time: {time.time()-t_start:.0f}s")

if __name__ == '__main__':
    main()
