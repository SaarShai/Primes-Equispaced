#!/usr/bin/env python3
"""
Chowla conjecture test using the UNWEIGHTED mu(n) spectrum.

F_u(gamma) = |sum_{n=1}^N mu(n) * exp(-i*gamma*log(n))|^2

This corresponds to evaluating |1/zeta(i*gamma)|^2, which DIVERGES at zeta zeros.
We handle normalization two ways:
  A) Exclude windows around zeros, normalize by Euler product in inter-zero regions.
  B) Smooth envelope at sigma=0.1 off the critical line.
"""

import numpy as np
import time

# ── 1. Mobius sieve ──────────────────────────────────────────────────────────
def mobius_sieve(N):
    """Compute mu(n) for n=0..N using linear sieve."""
    mu = np.zeros(N + 1, dtype=np.int8)
    mu[1] = 1
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    smallest_prime = np.zeros(N + 1, dtype=np.int32)

    for p in range(2, N + 1):
        if is_prime[p]:
            smallest_prime[p] = p
            for j in range(2 * p, N + 1, p):
                is_prime[j] = False
                if smallest_prime[j] == 0:
                    smallest_prime[j] = p

    # Compute mu via factorization
    mu[1] = 1
    for n in range(2, N + 1):
        p = smallest_prime[n]
        m = n // p
        if m % p == 0:
            mu[n] = 0  # p^2 divides n
        else:
            mu[n] = -mu[m]
    return mu

# ── 2. Compute unweighted spectroscope ──────────────────────────────────────
def compute_unweighted_spectrum(mu, gammas, N):
    """F_u(gamma) = |sum mu(n) * exp(-i*gamma*log(n))|^2"""
    ns = np.arange(1, N + 1)
    mu_vals = mu[1:N + 1].astype(np.float64)
    log_ns = np.log(ns)

    # Only use nonzero mu values
    mask = mu_vals != 0
    mu_nz = mu_vals[mask]
    log_nz = log_ns[mask]
    print(f"  Nonzero mu values: {len(mu_nz)} out of {N}")

    F = np.zeros(len(gammas))
    chunk = 500  # process gammas in chunks
    for i in range(0, len(gammas), chunk):
        g = gammas[i:i + chunk]
        # shape: (len(g), len(mu_nz))
        phases = np.outer(g, log_nz)
        S = np.sum(mu_nz[None, :] * np.exp(-1j * phases), axis=1)
        F[i:i + chunk] = np.abs(S) ** 2
    return F

# ── 3. Euler product envelopes ──────────────────────────────────────────────
def euler_product_envelope(gammas, P_max=1000, sigma=0.0):
    """
    |prod_{p<=P_max} (1 - p^{-sigma-i*gamma})|^2
    sigma=0 for on-axis, sigma=0.1 for smoothed.
    """
    primes = []
    sieve = np.ones(P_max + 1, dtype=bool)
    for p in range(2, P_max + 1):
        if sieve[p]:
            primes.append(p)
            for j in range(p * p, P_max + 1, p):
                sieve[j] = False

    env = np.ones(len(gammas))
    for p in primes:
        # |1 - p^{-sigma - i*gamma}|^2 = 1 - 2*p^{-sigma}*cos(gamma*log(p)) + p^{-2*sigma}
        lp = np.log(p)
        p_neg_sig = p ** (-sigma)
        factor = 1 - 2 * p_neg_sig * np.cos(gammas * lp) + p_neg_sig ** 2
        env *= factor
    return env

# ── 4. Known zeta zeros ─────────────────────────────────────────────────────
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044
]

def inter_zero_mask(gammas, zeros, exclusion=2.0):
    """True where gamma is NOT within ±exclusion of any zero."""
    mask = np.ones(len(gammas), dtype=bool)
    for z in zeros:
        mask &= np.abs(gammas - z) > exclusion
    return mask

# ── 5. Main ─────────────────────────────────────────────────────────────────
def main():
    N = 200000
    n_gamma = 15000
    gamma_min, gamma_max = 5.0, 60.0

    print(f"=== Chowla Unweighted Spectrum Test ===")
    print(f"N={N}, gammas: {n_gamma} points in [{gamma_min}, {gamma_max}]\n")

    # Step 1: Mobius sieve
    t0 = time.time()
    mu = mobius_sieve(N)
    print(f"[1] Mobius sieve: {time.time()-t0:.2f}s")
    print(f"    mu(1)={mu[1]}, mu(2)={mu[2]}, mu(6)={mu[6]}, mu(4)={mu[4]}")

    gammas = np.linspace(gamma_min, gamma_max, n_gamma)

    # Step 2: Unweighted spectrum
    t0 = time.time()
    print(f"\n[2] Computing unweighted spectrum F_u(gamma)...")
    F_u = compute_unweighted_spectrum(mu, gammas, N)
    print(f"    Done: {time.time()-t0:.2f}s")
    print(f"    F_u range: [{F_u.min():.2f}, {F_u.max():.2f}], mean={F_u.mean():.2f}")

    # Step 3a: On-axis Euler product (sigma=0)
    print(f"\n[3a] Euler product envelope (sigma=0, P_max=1000)...")
    env_onaxis = euler_product_envelope(gammas, P_max=1000, sigma=0.0)
    print(f"     Envelope range: [{env_onaxis.min():.6f}, {env_onaxis.max():.2f}]")

    # Step 3b: Smoothed Euler product (sigma=0.1)
    print(f"\n[3b] Smoothed envelope (sigma=0.1)...")
    env_smooth = euler_product_envelope(gammas, P_max=1000, sigma=0.1)
    print(f"     Envelope range: [{env_smooth.min():.6f}, {env_smooth.max():.2f}]")

    # Step 4: Inter-zero mask
    iz_mask = inter_zero_mask(gammas, ZETA_ZEROS, exclusion=2.0)
    n_interzero = np.sum(iz_mask)
    print(f"\n[4] Inter-zero mask: {n_interzero}/{n_gamma} points retained (exclusion=±2)")

    # ── Method A: On-axis normalization in inter-zero regions ────────────────
    print(f"\n{'='*60}")
    print(f"METHOD A: On-axis Euler product, inter-zero regions only")
    print(f"{'='*60}")

    # The on-axis envelope approximates |1/zeta(igamma)|^2 which diverges at zeros.
    # Away from zeros, F_u / env_onaxis should be ~ constant if Chowla holds.
    R_A = F_u[iz_mask] / env_onaxis[iz_mask]
    R_A_valid = R_A[np.isfinite(R_A) & (R_A > 0)]
    print(f"  Valid ratio points: {len(R_A_valid)}/{n_interzero}")
    if len(R_A_valid) > 0:
        log_R = np.log(R_A_valid)
        mean_A = np.mean(log_R)
        std_A = np.std(log_R)
        cv_A = std_A / np.abs(mean_A) if mean_A != 0 else float('inf')
        print(f"  log(R_A): mean={mean_A:.4f}, std={std_A:.4f}, CV={cv_A:.4f}")
        print(f"  R_A: median={np.median(R_A_valid):.2f}, mean={np.mean(R_A_valid):.2f}")

    # ── Method B: Smoothed normalization (sigma=0.1) ─────────────────────────
    print(f"\n{'='*60}")
    print(f"METHOD B: Smoothed envelope (sigma=0.1), full range")
    print(f"{'='*60}")

    R_B = F_u / env_smooth
    R_B_valid = R_B[np.isfinite(R_B) & (R_B > 0)]
    print(f"  Valid ratio points: {len(R_B_valid)}/{n_gamma}")

    # Inter-zero stats
    R_B_iz = R_B[iz_mask]
    R_B_iz_valid = R_B_iz[np.isfinite(R_B_iz) & (R_B_iz > 0)]
    log_RB = np.log(R_B_iz_valid)
    mean_B = np.mean(log_RB)
    std_B = np.std(log_RB)
    cv_B = std_B / np.abs(mean_B) if mean_B != 0 else float('inf')
    print(f"  Inter-zero log(R_B): mean={mean_B:.4f}, std={std_B:.4f}, CV={cv_B:.4f}")
    print(f"  Inter-zero R_B: median={np.median(R_B_iz_valid):.2f}, mean={np.mean(R_B_iz_valid):.2f}")

    # Near-zero stats (should show peaks)
    near_mask = ~iz_mask
    R_B_near = R_B[near_mask]
    R_B_near_valid = R_B_near[np.isfinite(R_B_near) & (R_B_near > 0)]
    if len(R_B_near_valid) > 0:
        print(f"  Near-zero R_B: median={np.median(R_B_near_valid):.2f}, "
              f"mean={np.mean(R_B_near_valid):.2f}, max={np.max(R_B_near_valid):.2f}")
        # Ratio of near-zero to inter-zero
        ratio_enhancement = np.median(R_B_near_valid) / np.median(R_B_iz_valid)
        print(f"  Enhancement near zeros: {ratio_enhancement:.2f}x")

    # ── Null comparison: shuffled mu ─────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"NULL TEST: Shuffled mu(n)")
    print(f"{'='*60}")

    n_null = 5
    null_cvs_A = []
    null_cvs_B = []
    rng = np.random.default_rng(42)

    for trial in range(n_null):
        mu_shuf = mu.copy()
        perm = rng.permutation(N) + 1
        mu_shuf[1:N + 1] = mu[perm]
        F_null = compute_unweighted_spectrum(mu_shuf, gammas, N)

        # Method A null
        R_null_A = F_null[iz_mask] / env_onaxis[iz_mask]
        R_null_A = R_null_A[np.isfinite(R_null_A) & (R_null_A > 0)]
        if len(R_null_A) > 0:
            log_null = np.log(R_null_A)
            cv_null_A = np.std(log_null) / np.abs(np.mean(log_null)) if np.mean(log_null) != 0 else float('inf')
            null_cvs_A.append(cv_null_A)

        # Method B null
        R_null_B = F_null[iz_mask] / env_smooth[iz_mask]
        R_null_B = R_null_B[np.isfinite(R_null_B) & (R_null_B > 0)]
        if len(R_null_B) > 0:
            log_null = np.log(R_null_B)
            cv_null_B = np.std(log_null) / np.abs(np.mean(log_null)) if np.mean(log_null) != 0 else float('inf')
            null_cvs_B.append(cv_null_B)

        print(f"  Null trial {trial+1}: CV_A={null_cvs_A[-1]:.4f}, CV_B={null_cvs_B[-1]:.4f}")

    print(f"\n  Null CV_A: mean={np.mean(null_cvs_A):.4f} ± {np.std(null_cvs_A):.4f}")
    print(f"  Null CV_B: mean={np.mean(null_cvs_B):.4f} ± {np.std(null_cvs_B):.4f}")
    print(f"  Real CV_A: {cv_A:.4f}  (ratio to null: {cv_A/np.mean(null_cvs_A):.3f})")
    print(f"  Real CV_B: {cv_B:.4f}  (ratio to null: {cv_B/np.mean(null_cvs_B):.3f})")

    # ── Unexpected peaks check ───────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"PEAK ANALYSIS")
    print(f"{'='*60}")

    # Find peaks in F_u that are NOT near zeta zeros
    threshold = np.mean(F_u[iz_mask]) + 5 * np.std(F_u[iz_mask])
    peak_mask = (F_u > threshold) & iz_mask
    peak_gammas = gammas[peak_mask]
    peak_vals = F_u[peak_mask]
    print(f"  Threshold (inter-zero mean + 5*std): {threshold:.2f}")
    print(f"  Peaks above threshold in inter-zero region: {len(peak_gammas)}")
    if len(peak_gammas) > 0:
        top_idx = np.argsort(peak_vals)[::-1][:10]
        for i in top_idx:
            print(f"    gamma={peak_gammas[i]:.4f}, F_u={peak_vals[i]:.2f}")

    # Peaks near zeros (expected)
    near_peak_mask = (F_u > threshold) & ~iz_mask
    print(f"  Peaks near zeta zeros (expected): {np.sum(near_peak_mask)}")

    # ── Spectral shape near zeros ────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"SPECTRAL SHAPE NEAR ZETA ZEROS")
    print(f"{'='*60}")
    for z in ZETA_ZEROS[:6]:
        window = np.abs(gammas - z) < 1.0
        if np.any(window):
            F_window = F_u[window]
            g_window = gammas[window]
            peak_idx = np.argmax(F_window)
            print(f"  Zero ~{z:.2f}: peak at gamma={g_window[peak_idx]:.4f}, "
                  f"F_u={F_window[peak_idx]:.2f}, "
                  f"ratio to inter-zero mean={F_window[peak_idx]/np.mean(F_u[iz_mask]):.1f}x")

    # ── VERDICT ──────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"VERDICT")
    print(f"{'='*60}")

    chowla_pass_A = cv_A < 2 * np.mean(null_cvs_A) if null_cvs_A else False
    chowla_pass_B = cv_B < 2 * np.mean(null_cvs_B) if null_cvs_B else False

    print(f"  Method A (on-axis, inter-zero): CV={cv_A:.4f}, null={np.mean(null_cvs_A):.4f}")
    print(f"    -> {'PASS' if chowla_pass_A else 'FAIL'}: real CV {'<' if chowla_pass_A else '>='} 2x null CV")
    print(f"  Method B (smoothed sigma=0.1): CV={cv_B:.4f}, null={np.mean(null_cvs_B):.4f}")
    print(f"    -> {'PASS' if chowla_pass_B else 'FAIL'}: real CV {'<' if chowla_pass_B else '>='} 2x null CV")

    if chowla_pass_A and chowla_pass_B:
        print(f"\n  OVERALL: CONSISTENT WITH CHOWLA (both methods)")
        print(f"  The unweighted test AGREES with the weighted test.")
    elif chowla_pass_A or chowla_pass_B:
        print(f"\n  OVERALL: MIXED — one method passes, one fails.")
        print(f"  Partial agreement with weighted test.")
    else:
        print(f"\n  OVERALL: INCONSISTENT — both methods show excess variation.")
        print(f"  Unweighted test DISAGREES with weighted test.")

    # Return key results for report
    return {
        'cv_A': cv_A, 'cv_B': cv_B,
        'null_cv_A': np.mean(null_cvs_A), 'null_cv_B': np.mean(null_cvs_B),
        'pass_A': chowla_pass_A, 'pass_B': chowla_pass_B,
        'n_unexpected_peaks': len(peak_gammas),
        'F_u_range': (F_u.min(), F_u.max()),
        'enhancement_near_zeros': ratio_enhancement if 'ratio_enhancement' in dir() else None,
    }

if __name__ == '__main__':
    results = main()
