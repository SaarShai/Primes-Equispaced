#!/usr/bin/env python3
"""
Cross-talk Phase 2: Deeper analysis based on Phase 1 findings.

KEY FINDING FROM PHASE 1:
- corr(T_chi7, T_plain) = -0.62 (strong anticorrelation)
- The 19.4x cross-talk SURVIVES balanced resampling
- Within M(p) strata, cross-talk is 2-4x (moderate but present)
- corr(T_chi7, cos(gamma*log p)) ~ 0 (cross-talk is NOT linear in zeta signal)

NEW HYPOTHESIS: The cross-talk operates through the PHASE-LOCK MECHANISM itself,
not through simple correlation. Both T_plain and T_chi7 have their signs coupled
through shared arithmetic (mu values), and this coupling is COHERENT in the
phase domain even when the LINEAR correlation with the signal is zero.

TESTS:
1. Shuffle test: permute T_chi7 values among primes. Does sigma drop?
   (If yes, the coupling is prime-specific, not just about the distribution)
2. Sign-coupling test: what fraction of primes have sgn(T_chi7) = -sgn(T_plain)?
   How does this fraction depend on gamma*log(p) mod 2pi?
3. The Perron integral cross-term: compute T_chi7 using a DIFFERENT set of mu*chi
   values but keeping the same primes. Does the signal survive?
4. Compute cross-talk for gamma values far from any L-function zero.
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

def sigma_test(T_vals, phases):
    """Return max sigma across T>0 and T<0."""
    pos = T_vals > 0
    neg = T_vals < 0
    n_pos = np.sum(pos)
    n_neg = np.sum(neg)
    R_pos = compute_resultant(phases[pos]) if n_pos > 0 else 0.0
    R_neg = compute_resultant(phases[neg]) if n_neg > 0 else 0.0
    sigma_pos = R_pos * sqrt(n_pos) if n_pos > 0 else 0.0
    sigma_neg = R_neg * sqrt(n_neg) if n_neg > 0 else 0.0
    return max(sigma_pos, sigma_neg), sigma_pos, sigma_neg

def main():
    t_start = time.time()
    print("=" * 120)
    print("CROSS-TALK PHASE 2: Mechanistic Analysis")
    print("=" * 120)

    mu = make_sieve(LIMIT)
    primes = make_primes(LIMIT)

    M_plain = np.zeros(LIMIT + 1, dtype=np.float64)
    running = 0.0
    for k in range(1, LIMIT + 1):
        running += mu[k]
        M_plain[k] = running

    M_chi7 = compute_twisted_mertens(mu, chi_mod7_quad, LIMIT)

    all_p = np.array([int(p) for p in primes if p <= PRIME_LIMIT])
    n = len(all_p)

    print(f"Computing T values for {n} primes...")
    T_plain = np.zeros(n)
    T_chi7 = np.zeros(n)
    for i, p in enumerate(all_p):
        T_plain[i] = compute_T_fast(M_plain, int(p))
        T_chi7[i] = compute_T_fast(M_chi7, int(p))

    log_p = np.log(all_p.astype(np.float64))
    gamma_zeta = 14.134725142
    gamma_chi7 = 4.97340925
    phases_zeta = (gamma_zeta * log_p) % (2 * pi)
    phases_chi7 = (gamma_chi7 * log_p) % (2 * pi)

    # === TEST 1: SHUFFLE TEST ===
    print(f"\n{'='*120}")
    print("TEST 1: Shuffle test — permute T_chi7 among primes")
    print("If cross-talk is prime-specific, shuffling should destroy it.")
    print(f"{'='*120}")

    orig_sigma, _, _ = sigma_test(T_chi7, phases_zeta)
    print(f"  Original sigma (T_chi7 at zeta zero): {orig_sigma:.2f}")

    np.random.seed(42)
    shuffle_sigmas = []
    for trial in range(100):
        perm = np.random.permutation(n)
        s, _, _ = sigma_test(T_chi7[perm], phases_zeta)
        shuffle_sigmas.append(s)
    shuffle_sigmas = np.array(shuffle_sigmas)
    print(f"  Shuffled sigma: mean={np.mean(shuffle_sigmas):.2f}, std={np.std(shuffle_sigmas):.2f}, max={np.max(shuffle_sigmas):.2f}")
    print(f"  Original is {(orig_sigma - np.mean(shuffle_sigmas))/np.std(shuffle_sigmas):.1f} std above shuffled mean")
    print(f"  CONCLUSION: {'Cross-talk is PRIME-SPECIFIC' if orig_sigma > np.mean(shuffle_sigmas) + 3*np.std(shuffle_sigmas) else 'Cross-talk is NOT prime-specific'}")

    # Also shuffle test for T_plain at zeta zero as sanity check
    orig_plain_sigma, _, _ = sigma_test(T_plain, phases_zeta)
    print(f"\n  Sanity: T_plain at zeta zero: {orig_plain_sigma:.2f}")
    shuffle_plain = []
    for trial in range(100):
        perm = np.random.permutation(n)
        s, _, _ = sigma_test(T_plain[perm], phases_zeta)
        shuffle_plain.append(s)
    shuffle_plain = np.array(shuffle_plain)
    print(f"  Shuffled: mean={np.mean(shuffle_plain):.2f}, std={np.std(shuffle_plain):.2f}")

    # === TEST 2: SIGN COUPLING IN PHASE SPACE ===
    print(f"\n{'='*120}")
    print("TEST 2: Sign coupling — does sgn(T_chi7) depend on gamma_zeta * log(p) mod 2pi?")
    print(f"{'='*120}")

    # Bin phases into 8 sectors
    n_bins = 8
    bin_edges = np.linspace(0, 2*pi, n_bins + 1)
    print(f"  Phase bins (8 sectors of width pi/4):")
    print(f"  {'Bin':>6s} {'Phase range':>20s} {'n':>5s} {'frac(T_chi7>0)':>16s} {'frac(T_plain>0)':>16s} {'frac(same sign)':>16s}")
    for b in range(n_bins):
        mask = (phases_zeta >= bin_edges[b]) & (phases_zeta < bin_edges[b+1])
        cnt = np.sum(mask)
        if cnt == 0:
            continue
        frac_chi7_pos = np.mean(T_chi7[mask] > 0)
        frac_plain_pos = np.mean(T_plain[mask] > 0)
        frac_same = np.mean(np.sign(T_chi7[mask]) == np.sign(T_plain[mask]))
        phase_lo = bin_edges[b] / pi
        phase_hi = bin_edges[b+1] / pi
        print(f"  {b:6d} [{phase_lo:.2f}pi, {phase_hi:.2f}pi)  {cnt:5d}    {frac_chi7_pos:16.3f} {frac_plain_pos:16.3f} {frac_same:16.3f}")

    # === TEST 3: FREQUENCY SCAN ===
    print(f"\n{'='*120}")
    print("TEST 3: Frequency scan — test T_chi7 at many gamma values")
    print("Peaks should appear at chi7 zero and possibly zeta zero if cross-talk is real.")
    print(f"{'='*120}")

    gammas = np.linspace(1.0, 30.0, 291)  # every 0.1
    sigmas_chi7 = np.zeros(len(gammas))
    sigmas_plain = np.zeros(len(gammas))
    for ig, g in enumerate(gammas):
        phases = (g * log_p) % (2 * pi)
        sigmas_chi7[ig], _, _ = sigma_test(T_chi7, phases)
        sigmas_plain[ig], _, _ = sigma_test(T_plain, phases)

    # Find peaks
    print(f"\n  Top 10 peaks for T_chi7:")
    top_idx = np.argsort(-sigmas_chi7)[:10]
    for rank, idx in enumerate(top_idx):
        g = gammas[idx]
        s = sigmas_chi7[idx]
        # Check if near a known zero
        near_zeta = abs(g - 14.13) < 0.3
        near_chi7 = abs(g - 4.97) < 0.3
        near_zeta2 = abs(g - 21.02) < 0.3
        label = ""
        if near_zeta: label = " <-- ZETA gamma_1"
        elif near_chi7: label = " <-- CHI7 gamma_1"
        elif near_zeta2: label = " <-- ZETA gamma_2"
        print(f"    #{rank+1}: gamma={g:.2f}, sigma={s:.2f}{label}")

    print(f"\n  Top 10 peaks for T_plain:")
    top_idx = np.argsort(-sigmas_plain)[:10]
    for rank, idx in enumerate(top_idx):
        g = gammas[idx]
        s = sigmas_plain[idx]
        near_zeta = abs(g - 14.13) < 0.3
        near_zeta2 = abs(g - 21.02) < 0.3
        label = ""
        if near_zeta: label = " <-- ZETA gamma_1"
        elif near_zeta2: label = " <-- ZETA gamma_2"
        print(f"    #{rank+1}: gamma={g:.2f}, sigma={s:.2f}{label}")

    # Background level
    # Exclude gamma within 1.0 of known zeros
    known_zeros = [4.97, 6.02, 6.18, 8.04, 14.13, 21.02, 25.01]
    bg_mask = np.ones(len(gammas), dtype=bool)
    for gz in known_zeros:
        bg_mask &= np.abs(gammas - gz) > 1.0
    bg_chi7 = sigmas_chi7[bg_mask]
    bg_plain = sigmas_plain[bg_mask]
    print(f"\n  Background sigma (excluding known zeros):")
    print(f"    T_chi7:  mean={np.mean(bg_chi7):.2f}, std={np.std(bg_chi7):.2f}, max={np.max(bg_chi7):.2f}")
    print(f"    T_plain: mean={np.mean(bg_plain):.2f}, std={np.std(bg_plain):.2f}, max={np.max(bg_plain):.2f}")

    # At specific gammas of interest
    print(f"\n  Sigma at specific gamma values:")
    for g_name, g_val in [("zeta gamma_1", 14.13), ("chi7 gamma_1", 4.97),
                           ("zeta gamma_2", 21.02), ("random 10.0", 10.0),
                           ("random 17.0", 17.0), ("random 23.0", 23.0)]:
        idx = np.argmin(np.abs(gammas - g_val))
        print(f"    gamma={g_val:6.2f} ({g_name:15s}): T_chi7 sigma={sigmas_chi7[idx]:.2f}, T_plain sigma={sigmas_plain[idx]:.2f}")

    # === TEST 4: THE KEY QUESTION ===
    print(f"\n{'='*120}")
    print("TEST 4: Is the cross-talk just the anticorrelation between T_chi7 and T_plain?")
    print("If sgn(T_chi7) ~ -sgn(T_plain), then T_chi7 at zeta zero is just the")
    print("NEGATIVE of T_plain at zeta zero, which trivially inherits the zeta signal.")
    print(f"{'='*120}")

    frac_opposite = np.mean(np.sign(T_chi7) != np.sign(T_plain))
    frac_same = np.mean(np.sign(T_chi7) == np.sign(T_plain))
    # Exclude zeros
    nonzero = (T_chi7 != 0) & (T_plain != 0)
    frac_opp_nz = np.mean(np.sign(T_chi7[nonzero]) != np.sign(T_plain[nonzero]))
    print(f"  frac(sgn(T_chi7) != sgn(T_plain)): {frac_opposite:.4f}")
    print(f"  frac(sgn(T_chi7) == sgn(T_plain)): {frac_same:.4f}")
    print(f"  (excluding zeros): frac opposite = {frac_opp_nz:.4f}")

    # If we FLIP the signs of T_chi7 (use -T_chi7), does it look like T_plain?
    print(f"\n  Phase-lock of -T_chi7 at zeta zero:")
    neg_T_chi7 = -T_chi7
    s_neg, sp, sn = sigma_test(neg_T_chi7, phases_zeta)
    print(f"    max_sigma = {s_neg:.2f} (compare T_plain: {orig_plain_sigma:.2f}, T_chi7: {orig_sigma:.2f})")

    # Now the critical test: RESIDUALIZE T_chi7 against T_plain and test
    # If cross-talk is mediated by T_plain, residuals should show no cross-talk
    print(f"\n  Residualized T_chi7 (regress out T_plain):")
    from numpy.linalg import lstsq
    A = np.column_stack([T_plain, np.ones(n)])
    coef, _, _, _ = lstsq(A, T_chi7, rcond=None)
    resid = T_chi7 - A @ coef
    print(f"    Regression: T_chi7 = {coef[0]:.4f} * T_plain + {coef[1]:.4f}")
    print(f"    corr(resid, T_plain) = {np.corrcoef(resid, T_plain)[0,1]:.6f} (should be ~0)")

    s_resid, _, _ = sigma_test(resid, phases_zeta)
    print(f"    Phase-lock of residualized T_chi7 at zeta zero: sigma = {s_resid:.2f}")

    s_resid_own, _, _ = sigma_test(resid, phases_chi7)
    print(f"    Phase-lock of residualized T_chi7 at chi7 zero: sigma = {s_resid_own:.2f}")

    # Do frequency scan on residuals
    print(f"\n  Frequency scan on residualized T_chi7:")
    resid_sigmas = np.zeros(len(gammas))
    for ig, g in enumerate(gammas):
        phases = (g * log_p) % (2 * pi)
        resid_sigmas[ig], _, _ = sigma_test(resid, phases)

    top_idx = np.argsort(-resid_sigmas)[:10]
    for rank, idx in enumerate(top_idx):
        g = gammas[idx]
        s = resid_sigmas[idx]
        near_zeta = abs(g - 14.13) < 0.3
        near_chi7 = abs(g - 4.97) < 0.3
        label = ""
        if near_zeta: label = " <-- ZETA gamma_1"
        elif near_chi7: label = " <-- CHI7 gamma_1"
        print(f"    #{rank+1}: gamma={g:.2f}, sigma={s:.2f}{label}")

    bg_resid = resid_sigmas[bg_mask]
    print(f"    Background: mean={np.mean(bg_resid):.2f}, std={np.std(bg_resid):.2f}")

    # === SUMMARY ===
    print(f"\n{'='*120}")
    print("FINAL SUMMARY")
    print(f"{'='*120}")
    print(f"""
Key findings:
1. corr(T_chi7, T_plain) = {np.corrcoef(T_chi7, T_plain)[0,1]:.4f}
2. Opposite sign fraction: {frac_opp_nz:.4f}
3. Shuffle destroys cross-talk: {'YES' if orig_sigma > np.mean(shuffle_sigmas) + 3*np.std(shuffle_sigmas) else 'NO'}
4. Balanced resampling preserves cross-talk: YES (from Phase 1: 19.4x)
5. -T_chi7 sigma at zeta: {s_neg:.2f} vs T_plain sigma: {orig_plain_sigma:.2f}
6. Residualized T_chi7 sigma at zeta: {s_resid:.2f}
7. Residualized T_chi7 sigma at chi7: {s_resid_own:.2f}
""")
    print(f"  Total time: {time.time()-t_start:.0f}s")

if __name__ == '__main__':
    main()
