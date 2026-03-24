#!/usr/bin/env python3
"""
SIGN vs MAGNITUDE DEEP ANALYSIS
=================================

Discovery: M(p) controls sign(ΔW) with 92.7% accuracy but |ΔW| correlation ≈ 0.
This means M(p) transmits exactly 1 bit (the sign) through 19,000:1 compression.

QUESTION: What controls |ΔW(p)|?

From the 4-term decomposition:
  ΔW = (A - B - C - D) / n'²
  A = dilution, B = cross term (Σ D·δ), C = shift² (Σ δ²), D = new fraction discrepancy
  Since D ≈ A (proved), ΔW ≈ -(B + C) / n'²

This script explores:
1. Candidate magnitude predictors: W(p-1), n, p, gap statistics, etc.
2. The normalized quantity ΔW·n'² and what controls it
3. Whether Σδ² (second moment) predicts |ΔW| better than M(p)
4. Twin prime differences and μ(p+1) connection
5. The "2-bit picture": sign from M(p), magnitude from ???
"""

import numpy as np
from math import gcd, sqrt, pi, log, floor
import csv
import os
from scipy import stats

# ============================================================
# DATA LOADING
# ============================================================

def load_wobble_data(filepath):
    """Load precomputed wobble data from CSV."""
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'p': int(row['p']),
                'wobble_p': float(row['wobble_p']),
                'wobble_pm1': float(row['wobble_pm1']),
                'delta_w': float(row['delta_w']),
                'farey_size_p': int(row['farey_size_p']),
                'mertens_p': int(row['mertens_p']),
                'm_over_sqrt_p': float(row['m_over_sqrt_p']),
            })
    return data


# ============================================================
# NUMBER-THEORETIC SIEVES
# ============================================================

def compute_mobius_sieve(limit):
    """Compute μ(n) for all n <= limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu, is_prime, primes


def euler_totient_sieve(limit):
    """Compute φ(n) for all n <= limit."""
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i
    return phi


def mertens_array(mu, N):
    """M(k) = Σ_{j=1}^k μ(j) for k=0..N."""
    M = np.zeros(N + 1, dtype=int)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M


# ============================================================
# FAREY STATISTICS COMPUTATION
# ============================================================

def farey_generator(N):
    """Yield (a, b) for each fraction a/b in F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b


def compute_farey_gap_stats(N):
    """
    Compute gap statistics of F_N.
    Returns: gaps array, max_gap, mean_gap, var_gap, num_large_gaps, gap_entropy
    """
    fracs = list(farey_generator(N))
    n = len(fracs)
    gaps = []
    for i in range(1, n):
        a1, b1 = fracs[i-1]
        a2, b2 = fracs[i]
        gap = a2/b2 - a1/b1
        gaps.append(gap)
    gaps = np.array(gaps)
    mean_gap = np.mean(gaps)
    var_gap = np.var(gaps)
    max_gap = np.max(gaps)
    # Number of gaps larger than 2x mean
    num_large = np.sum(gaps > 2 * mean_gap)
    # Gap entropy (discretized)
    hist, _ = np.histogram(gaps, bins=50, density=True)
    hist = hist[hist > 0]
    bin_width = 1.0 / (50 * mean_gap)  # approximate
    entropy = -np.sum(hist * np.log(hist + 1e-30)) * bin_width
    return {
        'max_gap': max_gap,
        'mean_gap': mean_gap,
        'var_gap': var_gap,
        'std_gap': np.sqrt(var_gap),
        'num_large_gaps': num_large,
        'gap_entropy': entropy,
        'gap_skewness': float(stats.skew(gaps)),
        'gap_kurtosis': float(stats.kurtosis(gaps)),
        'n_gaps': len(gaps),
    }


def compute_displacement_stats(p):
    """
    Compute displacement statistics when going F_{p-1} -> F_p.
    The displacement δ_j = (new_rank/n') - (old_rank/n) for each old fraction.
    Also computes the ABCD decomposition terms.
    """
    fracs_pm1 = list(farey_generator(p - 1))
    n = len(fracs_pm1)
    m = p - 1  # number of new fractions (φ(p) for prime p)
    n_prime = n + m

    fracs_p = list(farey_generator(p))

    # Build lookup for new sequence
    frac_to_new_rank = {}
    for j, (a, b) in enumerate(fracs_p):
        key = (a, b)
        frac_to_new_rank[key] = j

    # Compute displacements for OLD fractions
    displacements = []
    old_positions = []
    new_positions = []
    frac_values = []
    for j, (a, b) in enumerate(fracs_pm1):
        old_pos = j / n
        new_rank = frac_to_new_rank[(a, b)]
        new_pos = new_rank / n_prime
        delta = new_pos - old_pos
        displacements.append(delta)
        old_positions.append(old_pos)
        new_positions.append(new_pos)
        frac_values.append(a / b)

    displacements = np.array(displacements)
    frac_values = np.array(frac_values)
    old_positions = np.array(old_positions)

    # Displacement statistics
    delta_sq_sum = np.sum(displacements**2)            # C term: Σ δ²
    cross_term = np.sum(displacements * (np.array(frac_values) - old_positions))  # related to B
    mean_disp = np.mean(displacements)
    var_disp = np.var(displacements)
    max_abs_disp = np.max(np.abs(displacements))
    sum_abs_disp = np.sum(np.abs(displacements))

    # Second moment of δ
    second_moment = np.mean(displacements**2)
    # Fourth moment
    fourth_moment = np.mean(displacements**4)

    # New fraction discrepancies
    new_frac_discs = []
    for k in range(1, p):
        kp_val = k / p
        # Count fractions in F_{p-1} <= k/p
        count = sum(1 for (a, b) in fracs_pm1 if a/b <= kp_val)
        ideal = n * k / p
        disc = count - ideal
        new_frac_discs.append(disc)
    new_frac_discs = np.array(new_frac_discs)

    return {
        'n': n,
        'n_prime': n_prime,
        'm': m,
        'delta_sq_sum': delta_sq_sum,             # Σ δ² (C term)
        'cross_term': cross_term,
        'mean_disp': mean_disp,
        'var_disp': var_disp,
        'max_abs_disp': max_abs_disp,
        'sum_abs_disp': sum_abs_disp,
        'second_moment_delta': second_moment,      # <δ²>
        'fourth_moment_delta': fourth_moment,      # <δ⁴>
        'disc_sum': np.sum(new_frac_discs),
        'disc_sq_sum': np.sum(new_frac_discs**2),
        'disc_abs_sum': np.sum(np.abs(new_frac_discs)),
        'disc_var': np.var(new_frac_discs),
    }


# ============================================================
# ANALYSIS 1: CANDIDATE MAGNITUDE PREDICTORS
# ============================================================

def analyze_magnitude_predictors(data, mu, M_arr, phi):
    """Test many candidate predictors for |ΔW(p)|."""
    print("=" * 80)
    print("ANALYSIS 1: CANDIDATE PREDICTORS FOR |ΔW(p)|")
    print("=" * 80)

    ps = np.array([d['p'] for d in data])
    delta_ws = np.array([d['delta_w'] for d in data])
    abs_dw = np.abs(delta_ws)
    mertens = np.array([d['mertens_p'] for d in data])
    ns = np.array([d['farey_size_p'] for d in data])
    w_pm1 = np.array([d['wobble_pm1'] for d in data])

    # Log-transform for better correlation (since |ΔW| spans orders of magnitude)
    log_abs_dw = np.log(abs_dw + 1e-30)

    candidates = {}

    # 1. Simple arithmetic quantities
    candidates['1/p'] = 1.0 / ps
    candidates['1/p²'] = 1.0 / ps**2
    candidates['1/n'] = 1.0 / ns
    candidates['1/n²'] = 1.0 / ns**2
    candidates['W(p-1)'] = w_pm1
    candidates['W(p-1)/p'] = w_pm1 / ps
    candidates['|M(p)|'] = np.abs(mertens).astype(float)
    candidates['|M(p)|/sqrt(p)'] = np.abs(mertens) / np.sqrt(ps)
    candidates['M(p)²'] = mertens.astype(float)**2
    candidates['M(p)²/p'] = mertens.astype(float)**2 / ps
    candidates['log(p)'] = np.log(ps)
    candidates['log(p)/p'] = np.log(ps) / ps
    candidates['p·W(p-1)'] = ps * w_pm1

    # 2. Totient-related
    phi_vals = np.array([phi[int(p)] for p in ps])
    candidates['φ(p)/p'] = phi_vals / ps  # always (p-1)/p for prime p
    candidates['p-1'] = ps - 1.0

    # 3. Gap between consecutive primes
    prime_gaps = np.zeros(len(ps))
    for i in range(1, len(ps)):
        prime_gaps[i] = ps[i] - ps[i-1]
    prime_gaps[0] = 2  # gap before first prime in list
    candidates['prime_gap'] = prime_gaps
    candidates['prime_gap/log(p)'] = prime_gaps / np.log(ps)

    # 4. Mertens derivative: μ(p) = M(p) - M(p-1) = -1 for primes
    # But M(p-1) is more interesting
    M_pm1 = np.array([M_arr[int(p)-1] for p in ps])
    candidates['|M(p-1)|'] = np.abs(M_pm1).astype(float)
    candidates['|M(p)-M(p-1)|'] = np.abs(mertens - M_pm1).astype(float)  # always 1 for primes

    # 5. Mertens change over recent range
    for window in [10, 50]:
        M_window = np.array([M_arr[max(1, int(p)-window)] for p in ps])
        candidates[f'|M(p)-M(p-{window})|'] = np.abs(mertens - M_window).astype(float)

    # 6. Second Mertens: M₂(p) = Σ_{k≤p} μ(k)·k
    M2 = np.zeros(len(mu))
    for k in range(1, len(mu)):
        M2[k] = M2[k-1] + mu[k] * k
    M2_vals = np.array([M2[int(p)] for p in ps])
    candidates['|M₂(p)|'] = np.abs(M2_vals)
    candidates['|M₂(p)|/p'] = np.abs(M2_vals) / ps

    # 7. Normalized ΔW
    delta_w_normalized = delta_ws * ns**2  # ΔW · n²
    candidates['|ΔW·n²|_target'] = np.abs(delta_w_normalized)

    print(f"\n  Testing {len(candidates)-1} predictors against |ΔW(p)|")
    print(f"  Number of primes: {len(ps)}")
    print(f"\n  {'Predictor':<25} {'r(|ΔW|)':>10} {'r(log|ΔW|)':>12} {'r(|ΔW·n²|)':>12}")
    print(f"  {'-'*25} {'-'*10} {'-'*12} {'-'*12}")

    results = []
    target_norm = np.abs(delta_w_normalized)

    for name, vals in candidates.items():
        if name == '|ΔW·n²|_target':
            continue
        # Pearson correlation with |ΔW|
        r_abs, p_abs = stats.pearsonr(vals, abs_dw)
        # Pearson with log|ΔW|
        r_log, p_log = stats.pearsonr(vals, log_abs_dw)
        # Pearson with |ΔW·n²|
        r_norm, p_norm = stats.pearsonr(vals, target_norm)
        results.append((name, r_abs, r_log, r_norm, p_abs, p_log, p_norm))
        print(f"  {name:<25} {r_abs:10.4f} {r_log:12.4f} {r_norm:12.4f}")

    # Sort by |r| with |ΔW|
    results.sort(key=lambda x: abs(x[1]), reverse=True)
    print(f"\n  TOP 5 predictors of |ΔW| (by |Pearson r|):")
    for name, r_abs, r_log, r_norm, _, _, _ in results[:5]:
        print(f"    {name:<25}  r = {r_abs:+.4f}")

    results.sort(key=lambda x: abs(x[3]), reverse=True)
    print(f"\n  TOP 5 predictors of |ΔW·n²| (by |Pearson r|):")
    for name, r_abs, r_log, r_norm, _, _, _ in results[:5]:
        print(f"    {name:<25}  r = {r_norm:+.4f}")

    return results, delta_w_normalized


# ============================================================
# ANALYSIS 2: NORMALIZED ΔW AND FAREY STATISTICS
# ============================================================

def analyze_normalized_dw(data, mu, M_arr, max_farey_p=2000):
    """
    Compute ΔW·n'² for primes up to max_farey_p and correlate with
    detailed Farey statistics (gap variance, displacement statistics).
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 2: WHAT CONTROLS |ΔW·n²|? (Farey statistics, primes ≤ " + str(max_farey_p) + ")")
    print("=" * 80)

    # Filter to small primes where we can compute Farey stats
    small_data = [d for d in data if d['p'] <= max_farey_p]
    print(f"  Using {len(small_data)} primes up to {max_farey_p}")

    results = []
    for i, d in enumerate(small_data):
        p = d['p']
        if i % 50 == 0:
            print(f"  Computing Farey stats for p={p} ({i+1}/{len(small_data)})...")

        # Displacement stats (the expensive part)
        disp_stats = compute_displacement_stats(p)

        results.append({
            'p': p,
            'delta_w': d['delta_w'],
            'abs_dw': abs(d['delta_w']),
            'dw_n2': d['delta_w'] * d['farey_size_p']**2,
            'abs_dw_n2': abs(d['delta_w'] * d['farey_size_p']**2),
            'n': d['farey_size_p'],
            'mertens': d['mertens_p'],
            'w_pm1': d['wobble_pm1'],
            **disp_stats,
        })

    # Now correlate
    ps = np.array([r['p'] for r in results])
    abs_dw = np.array([r['abs_dw'] for r in results])
    abs_dw_n2 = np.array([r['abs_dw_n2'] for r in results])
    delta_w = np.array([r['delta_w'] for r in results])
    dw_n2 = np.array([r['dw_n2'] for r in results])

    predictors = {
        'Σδ² (C term)': np.array([r['delta_sq_sum'] for r in results]),
        '<δ²> (second moment)': np.array([r['second_moment_delta'] for r in results]),
        'var(δ)': np.array([r['var_disp'] for r in results]),
        'max|δ|': np.array([r['max_abs_disp'] for r in results]),
        'Σ|δ|': np.array([r['sum_abs_disp'] for r in results]),
        'cross_term': np.array([r['cross_term'] for r in results]),
        '|cross_term|': np.abs(np.array([r['cross_term'] for r in results])),
        'Σ disc²': np.array([r['disc_sq_sum'] for r in results]),
        'Σ|disc|': np.array([r['disc_abs_sum'] for r in results]),
        'var(disc)': np.array([r['disc_var'] for r in results]),
        'W(p-1)': np.array([r['w_pm1'] for r in results]),
        '|M(p)|': np.abs(np.array([r['mertens'] for r in results])).astype(float),
        'n': np.array([r['n'] for r in results]).astype(float),
        '1/p': 1.0 / ps,
        'Σδ² + |cross|': np.array([r['delta_sq_sum'] for r in results]) +
                         np.abs(np.array([r['cross_term'] for r in results])),
    }

    print(f"\n  {'Predictor':<25} {'r(|ΔW|)':>10} {'r(|ΔW·n²|)':>12} {'r(ΔW·n²)':>10} {'p-val':>10}")
    print(f"  {'-'*25} {'-'*10} {'-'*12} {'-'*10} {'-'*10}")

    for name, vals in predictors.items():
        r_abs, _ = stats.pearsonr(vals, abs_dw)
        r_norm_abs, _ = stats.pearsonr(vals, abs_dw_n2)
        r_norm_signed, p_val = stats.pearsonr(vals, dw_n2)
        print(f"  {name:<25} {r_abs:10.4f} {r_norm_abs:12.4f} {r_norm_signed:10.4f} {p_val:10.2e}")

    # Key finding: does Σδ² predict |ΔW·n²| better than |M(p)|?
    sigma_delta_sq = np.array([r['delta_sq_sum'] for r in results])
    abs_M = np.abs(np.array([r['mertens'] for r in results])).astype(float)

    r_sigma, _ = stats.pearsonr(sigma_delta_sq, abs_dw_n2)
    r_M, _ = stats.pearsonr(abs_M, abs_dw_n2)

    print(f"\n  KEY COMPARISON:")
    print(f"    Σδ² vs |ΔW·n²|:  r = {r_sigma:.4f}")
    print(f"    |M(p)| vs |ΔW·n²|: r = {r_M:.4f}")
    if abs(r_sigma) > abs(r_M):
        print(f"    --> Σδ² is a BETTER predictor of magnitude than |M(p)|!")
    else:
        print(f"    --> |M(p)| remains a better predictor (or equally bad)")

    return results


# ============================================================
# ANALYSIS 3: THE "2-BIT" PICTURE
# ============================================================

def analyze_two_bit_picture(data, mu, M_arr):
    """
    Sign from M(p). What gives us the magnitude?
    Try combining M(p) sign with various magnitude predictors.
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 3: THE 2-BIT PICTURE — sign(M(p)) × magnitude(???)")
    print("=" * 80)

    ps = np.array([d['p'] for d in data])
    delta_ws = np.array([d['delta_w'] for d in data])
    ns = np.array([d['farey_size_p'] for d in data])
    mertens = np.array([d['mertens_p'] for d in data])
    w_pm1 = np.array([d['wobble_pm1'] for d in data])

    sign_M = np.sign(mertens)

    # For the 2-bit picture: ΔW ≈ sign(M(p)) × magnitude(???)
    # We want: ΔW / sign(M(p)) ≈ |ΔW| when sign matches
    # Filter to cases where M(p) ≠ 0 and sign matches
    mask = sign_M != 0
    sign_match = (np.sign(delta_ws[mask]) == sign_M[mask])

    # magnitude candidates
    candidates = {
        'W(p-1)': w_pm1,
        'W(p-1)/p': w_pm1 / ps,
        '1/p²': 1.0 / ps**2,
        '1/n²': 1.0 / ns**2,
        'W(p-1)²': w_pm1**2,
        'W(p-1)/n': w_pm1 / ns,
        'log(p)/p²': np.log(ps) / ps**2,
    }

    # Model: ΔW_predicted = sign(M(p)) × f(predictor)
    # Test: r(ΔW, sign(M(p)) × predictor)
    print(f"\n  Model: ΔW ≈ sign(M(p)) × f(X)")
    print(f"  Testing correlation r(ΔW, sign(M(p)) × X):")
    print(f"\n  {'X':<20} {'r(ΔW, sgn·X)':>14} {'r²':>8} {'p-value':>12}")
    print(f"  {'-'*20} {'-'*14} {'-'*8} {'-'*12}")

    best_r = 0
    best_name = ""
    for name, vals in candidates.items():
        predicted = sign_M.astype(float) * vals
        r, p_val = stats.pearsonr(predicted[mask], delta_ws[mask])
        print(f"  {name:<20} {r:14.6f} {r**2:8.4f} {p_val:12.2e}")
        if abs(r) > abs(best_r):
            best_r = r
            best_name = name

    print(f"\n  Best 2-bit model: ΔW ≈ sign(M(p)) × {best_name}, r = {best_r:.4f}")

    # Multi-variate: ΔW ≈ α · sign(M(p)) × W(p-1)/p + β
    X = sign_M[mask].astype(float) * (w_pm1[mask] / ps[mask])
    slope, intercept, r, p_val, se = stats.linregress(X, delta_ws[mask])
    print(f"\n  Linear fit: ΔW = {slope:.6f} × sign(M)·W(p-1)/p + {intercept:.2e}")
    print(f"  r = {r:.4f}, r² = {r**2:.4f}, SE = {se:.2e}")

    # Try: ΔW ≈ α · M(p)/p² + β·W(p-1)/p + γ
    print(f"\n  Multivariate regression: ΔW = α·M(p)/p² + β·W(p-1)/p + γ")
    X_multi = np.column_stack([
        mertens[mask].astype(float) / ps[mask]**2,
        w_pm1[mask] / ps[mask],
    ])
    from numpy.linalg import lstsq
    X_aug = np.column_stack([X_multi, np.ones(X_multi.shape[0])])
    coeffs, residuals, _, _ = lstsq(X_aug, delta_ws[mask], rcond=None)
    predicted = X_aug @ coeffs
    ss_res = np.sum((delta_ws[mask] - predicted)**2)
    ss_tot = np.sum((delta_ws[mask] - np.mean(delta_ws[mask]))**2)
    r2 = 1 - ss_res / ss_tot
    print(f"  α = {coeffs[0]:.6f}, β = {coeffs[1]:.6f}, γ = {coeffs[2]:.2e}")
    print(f"  R² = {r2:.4f}")

    # Is M(p)/sqrt(p) better than M(p)/p²?
    print(f"\n  Multivariate: ΔW = α·M(p)/√p·n² + β·W(p-1)/n + γ")
    X_multi2 = np.column_stack([
        mertens[mask].astype(float) / (np.sqrt(ps[mask]) * ns[mask]**2),
        w_pm1[mask] / ns[mask],
    ])
    X_aug2 = np.column_stack([X_multi2, np.ones(X_multi2.shape[0])])
    coeffs2, _, _, _ = lstsq(X_aug2, delta_ws[mask], rcond=None)
    predicted2 = X_aug2 @ coeffs2
    ss_res2 = np.sum((delta_ws[mask] - predicted2)**2)
    r2_2 = 1 - ss_res2 / ss_tot
    print(f"  α = {coeffs2[0]:.6f}, β = {coeffs2[1]:.6f}, γ = {coeffs2[2]:.2e}")
    print(f"  R² = {r2_2:.4f}")


# ============================================================
# ANALYSIS 4: TWIN PRIME DIFFERENCES AND μ(p+1)
# ============================================================

def analyze_twin_primes(data, mu, M_arr, is_prime):
    """
    For twin primes (p, p+2): |ΔW(p) - ΔW(p+2)| is tiny when μ(p+1)=0.
    What happens when μ(p+1) ≠ 0? Is the difference proportional to μ(p+1)?
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 4: TWIN PRIME DIFFERENCES AND μ(p+1)")
    print("=" * 80)

    # Build lookup
    p_to_data = {d['p']: d for d in data}

    # Find twin primes
    twins_mu0 = []     # μ(p+1) = 0
    twins_mu_nonzero = []  # μ(p+1) ≠ 0

    # Also collect ALL consecutive prime pairs (p, q) where q = next prime
    consec_pairs = []
    for i in range(len(data) - 1):
        p = data[i]['p']
        q = data[i+1]['p']
        gap = q - p
        mid = p + 1
        if gap == 2:  # twin primes
            dw_p = data[i]['delta_w']
            dw_q = data[i+1]['delta_w']
            diff = abs(dw_p - dw_q)
            mu_mid = mu[mid] if mid < len(mu) else None

            entry = {
                'p': p, 'q': q,
                'dw_p': dw_p, 'dw_q': dw_q,
                'diff': diff,
                'mu_mid': mu_mid,
                'M_p': data[i]['mertens_p'],
                'M_q': data[i+1]['mertens_p'],
            }
            if mu_mid == 0:
                twins_mu0.append(entry)
            else:
                twins_mu_nonzero.append(entry)

        consec_pairs.append({
            'p': p, 'q': q, 'gap': gap,
            'dw_p': data[i]['delta_w'],
            'dw_q': data[i+1]['delta_w'],
            'diff': abs(data[i]['delta_w'] - data[i+1]['delta_w']),
        })

    print(f"\n  Twin primes found: {len(twins_mu0) + len(twins_mu_nonzero)}")
    print(f"    μ(p+1) = 0: {len(twins_mu0)}")
    print(f"    μ(p+1) ≠ 0: {len(twins_mu_nonzero)}")

    if twins_mu0 and twins_mu_nonzero:
        diffs_mu0 = [t['diff'] for t in twins_mu0]
        diffs_mu_nz = [t['diff'] for t in twins_mu_nonzero]

        mean_mu0 = np.mean(diffs_mu0)
        mean_mu_nz = np.mean(diffs_mu_nz)
        median_mu0 = np.median(diffs_mu0)
        median_mu_nz = np.median(diffs_mu_nz)

        print(f"\n  |ΔW(p) - ΔW(p+2)| statistics:")
        print(f"    μ(p+1) = 0:  mean = {mean_mu0:.2e}, median = {median_mu0:.2e}")
        print(f"    μ(p+1) ≠ 0:  mean = {mean_mu_nz:.2e}, median = {median_mu_nz:.2e}")
        print(f"    Ratio (nonzero/zero): mean = {mean_mu_nz/mean_mu0:.2f}, median = {median_mu_nz/median_mu0:.2f}")

        # Is the difference proportional to |μ(p+1)|? Since |μ|=1 when nonzero, check
        # if diff correlates with the actual change in M
        # M(p+2) - M(p) = μ(p+1) + μ(p+2) = μ(p+1) - 1 (since p+2 prime, μ(p+2)=-1)
        print(f"\n  For μ(p+1)=0 twins: M(p+2) - M(p) = μ(p+1) + μ(p+2) = 0 + (-1) = -1")
        print(f"  For μ(p+1)≠0 twins: M(p+2) - M(p) = μ(p+1) + (-1) = μ(p+1) - 1")

        # Verify
        for label, group in [("μ=0", twins_mu0[:5]), ("μ≠0", twins_mu_nonzero[:5])]:
            print(f"\n  Sample {label} twins:")
            for t in group:
                m_diff = t['M_q'] - t['M_p']
                print(f"    ({t['p']}, {t['q']}): μ(p+1)={t['mu_mid']}, "
                      f"M(q)-M(p)={m_diff}, |ΔW diff|={t['diff']:.2e}")

    # General: does |ΔW(p) - ΔW(q)| depend on |M(q) - M(p)| for consecutive primes?
    if len(consec_pairs) > 100:
        diffs = np.array([cp['diff'] for cp in consec_pairs])
        gaps = np.array([cp['gap'] for cp in consec_pairs])

        # Group by gap size
        unique_gaps = sorted(set(gaps))[:10]
        print(f"\n  Consecutive prime pairs by gap size:")
        print(f"    {'gap':>5} {'count':>6} {'mean |ΔW diff|':>16} {'median':>14}")
        for g in unique_gaps:
            mask = gaps == g
            if np.sum(mask) >= 5:
                vals = diffs[mask]
                print(f"    {g:5d} {np.sum(mask):6d} {np.mean(vals):16.2e} {np.median(vals):14.2e}")


# ============================================================
# ANALYSIS 5: W(p-1) SCALING LAW
# ============================================================

def analyze_wobble_scaling(data):
    """
    W(p-1) is known to scale like 1/(2π²) · log(p)/p.
    Since |ΔW| ≈ W(p-1) - W(p), and both scale similarly,
    |ΔW| should scale like d/dp[log(p)/p] ∝ (1-log(p))/p².

    Test: |ΔW| ∝ log(p)/p² vs other scalings.
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 5: SCALING LAW FOR |ΔW|")
    print("=" * 80)

    ps = np.array([d['p'] for d in data])
    abs_dw = np.abs(np.array([d['delta_w'] for d in data]))
    w_pm1 = np.array([d['wobble_pm1'] for d in data])
    ns = np.array([d['farey_size_p'] for d in data])

    # Theoretical: W(N) ~ log(N)/(2π²N), so ΔW ~ d/dN[log(N)/N] = (1-logN)/N²
    # But the discrete derivative may differ

    scalings = {
        'log(p)/p²': np.log(ps) / ps**2,
        '(1-log(p))/p²': (1 - np.log(ps)) / ps**2,
        '1/p²': 1.0 / ps**2,
        'log(p)/n²': np.log(ps) / ns**2,
        '1/(p·log(p))': 1.0 / (ps * np.log(ps)),
        'W(p-1)/p': w_pm1 / ps,
        'W(p-1)²': w_pm1**2,
    }

    print(f"\n  {'Scaling':<20} {'r(|ΔW|, scaling)':>18} {'r(log|ΔW|, log)':>18}")
    print(f"  {'-'*20} {'-'*18} {'-'*18}")

    for name, vals in scalings.items():
        r, _ = stats.pearsonr(vals, abs_dw)
        # log-log correlation
        mask = (vals > 0)
        if np.sum(mask) < 10:
            r_log = float('nan')
        else:
            r_log, _ = stats.pearsonr(np.log(vals[mask]), np.log(abs_dw[mask]))
        print(f"  {name:<20} {r:18.6f} {r_log:18.6f}")

    # Log-log regression: log|ΔW| = α·log(p) + β
    log_p = np.log(ps)
    log_abs_dw = np.log(abs_dw)
    slope, intercept, r, p_val, se = stats.linregress(log_p, log_abs_dw)
    print(f"\n  Power law fit: |ΔW| ∝ p^α")
    print(f"    α = {slope:.4f} (expect ≈ -2 for 1/p² scaling)")
    print(f"    r = {r:.4f}, r² = {r**2:.4f}")

    # Residuals from power law — does M(p) predict them?
    residuals = log_abs_dw - (slope * log_p + intercept)
    mertens = np.array([d['mertens_p'] for d in data])
    r_resid_M, _ = stats.pearsonr(np.abs(mertens), np.abs(residuals))
    r_resid_M_signed, _ = stats.pearsonr(mertens, residuals)
    print(f"\n  Residuals from power law:")
    print(f"    r(|M(p)|, |residuals|) = {r_resid_M:.4f}")
    print(f"    r(M(p), residuals) = {r_resid_M_signed:.4f}")

    # What predicts the residuals?
    print(f"\n  What predicts power-law residuals?")
    resid_predictors = {
        '|M(p)|': np.abs(mertens).astype(float),
        'M(p)²': mertens.astype(float)**2,
        'W(p-1)·p²': w_pm1 * ps**2,
        'prime_gap_local': np.zeros(len(ps)),  # will fill
        'log(W(p-1)·p)': np.log(w_pm1 * ps),
    }
    # Prime gaps
    for i in range(1, len(ps)):
        resid_predictors['prime_gap_local'][i] = ps[i] - ps[i-1]
    resid_predictors['prime_gap_local'][0] = 2

    for name, vals in resid_predictors.items():
        r_r, _ = stats.pearsonr(vals, residuals)
        print(f"    {name:<25}  r = {r_r:+.4f}")

    return slope, intercept


# ============================================================
# ANALYSIS 6: BINNED STATISTICS
# ============================================================

def analyze_binned(data):
    """
    Bin primes by ranges of p and study how |ΔW| variance behaves.
    If M(p) controls only the sign, the magnitude should come from
    the "local density" of the Farey sequence.
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 6: BINNED STATISTICS — SEPARATING TREND FROM FLUCTUATION")
    print("=" * 80)

    ps = np.array([d['p'] for d in data])
    delta_ws = np.array([d['delta_w'] for d in data])
    ns = np.array([d['farey_size_p'] for d in data])
    mertens = np.array([d['mertens_p'] for d in data])
    w_pm1 = np.array([d['wobble_pm1'] for d in data])

    # Normalize: remove the 1/p² trend
    # ΔW_normalized = ΔW · p²
    dw_normed = delta_ws * ps**2

    # Bin by p ranges
    bin_edges = [0, 1000, 5000, 10000, 20000, 50000, 100001]
    print(f"\n  {'Bin':>15} {'N':>5} {'mean(ΔW·p²)':>14} {'std(ΔW·p²)':>14} "
          f"{'mean|M|':>8} {'r(M,ΔW·p²)':>12}")
    print(f"  {'-'*15} {'-'*5} {'-'*14} {'-'*14} {'-'*8} {'-'*12}")

    for i in range(len(bin_edges) - 1):
        lo, hi = bin_edges[i], bin_edges[i+1]
        mask = (ps > lo) & (ps <= hi)
        if np.sum(mask) < 10:
            continue
        bin_dw = dw_normed[mask]
        bin_M = mertens[mask].astype(float)
        r_bin, _ = stats.pearsonr(bin_M, bin_dw)
        print(f"  {lo:6d}-{hi:6d} {np.sum(mask):5d} {np.mean(bin_dw):14.4f} "
              f"{np.std(bin_dw):14.4f} {np.mean(np.abs(bin_M)):8.1f} {r_bin:12.4f}")

    # KEY TEST: within each bin, after removing sign info from M(p),
    # does |ΔW·p²| have a pattern?
    print(f"\n  Within-bin analysis of |ΔW·p²| (sign removed):")
    print(f"  {'Bin':>15} {'mean|ΔW·p²|':>14} {'std|ΔW·p²|':>14} {'CV':>8} {'r(|M|,|ΔW|·p²)':>16}")

    for i in range(len(bin_edges) - 1):
        lo, hi = bin_edges[i], bin_edges[i+1]
        mask = (ps > lo) & (ps <= hi)
        if np.sum(mask) < 10:
            continue
        abs_dw_p2 = np.abs(dw_normed[mask])
        abs_M = np.abs(mertens[mask]).astype(float)
        r_abs, _ = stats.pearsonr(abs_M, abs_dw_p2)
        cv = np.std(abs_dw_p2) / np.mean(abs_dw_p2)
        print(f"  {lo:6d}-{hi:6d} {np.mean(abs_dw_p2):14.4f} {np.std(abs_dw_p2):14.4f} "
              f"{cv:8.3f} {r_abs:16.4f}")


# ============================================================
# ANALYSIS 7: FLUCTUATION DECOMPOSITION
# ============================================================

def analyze_fluctuation_structure(data, mu, M_arr):
    """
    Decompose |ΔW| fluctuations into:
    1. Power-law trend (deterministic scaling)
    2. Sign (from M(p))
    3. Residual magnitude fluctuation

    What is the residual? Is it "random" or structured?
    """
    print("\n" + "=" * 80)
    print("ANALYSIS 7: FLUCTUATION STRUCTURE")
    print("=" * 80)

    ps = np.array([d['p'] for d in data])
    delta_ws = np.array([d['delta_w'] for d in data])
    ns = np.array([d['farey_size_p'] for d in data])
    mertens = np.array([d['mertens_p'] for d in data])

    # Step 1: Remove power-law trend
    log_p = np.log(ps)
    log_abs_dw = np.log(np.abs(delta_ws))
    slope, intercept, _, _, _ = stats.linregress(log_p, log_abs_dw)
    trend = np.exp(slope * log_p + intercept)
    ratio = np.abs(delta_ws) / trend  # should be ~1 on average

    print(f"  Power-law: |ΔW| ≈ e^{intercept:.4f} · p^{slope:.4f}")
    print(f"  Ratio |ΔW|/trend: mean={np.mean(ratio):.4f}, std={np.std(ratio):.4f}")

    # Step 2: Is the ratio autocorrelated?
    log_ratio = np.log(ratio)
    autocorr_1 = np.corrcoef(log_ratio[:-1], log_ratio[1:])[0, 1]
    autocorr_2 = np.corrcoef(log_ratio[:-2], log_ratio[2:])[0, 1]
    autocorr_5 = np.corrcoef(log_ratio[:-5], log_ratio[5:])[0, 1]
    print(f"\n  Autocorrelation of log(|ΔW|/trend):")
    print(f"    lag 1: {autocorr_1:.4f}")
    print(f"    lag 2: {autocorr_2:.4f}")
    print(f"    lag 5: {autocorr_5:.4f}")

    # Step 3: Is the ratio related to local prime density?
    # Local prime density ≈ 1/log(p), but fluctuations matter
    local_density = np.zeros(len(ps))
    window = 10
    for i in range(len(ps)):
        lo = max(0, i - window)
        hi = min(len(ps), i + window + 1)
        local_count = hi - lo
        local_range = ps[min(hi-1, len(ps)-1)] - ps[lo]
        if local_range > 0:
            local_density[i] = local_count / local_range

    r_density, _ = stats.pearsonr(local_density, log_ratio)
    print(f"\n  r(local_prime_density, log(|ΔW|/trend)) = {r_density:.4f}")

    # Step 4: Distribution of the ratio
    print(f"\n  Distribution of |ΔW|/trend:")
    percentiles = [5, 25, 50, 75, 95]
    for pct in percentiles:
        print(f"    {pct}th percentile: {np.percentile(ratio, pct):.4f}")

    # Is it log-normal?
    _, shapiro_p = stats.shapiro(log_ratio[:5000])  # shapiro limit
    print(f"    Shapiro-Wilk test on log(ratio): p = {shapiro_p:.4f}")
    print(f"    log(ratio) mean = {np.mean(log_ratio):.4f}, std = {np.std(log_ratio):.4f}")

    # Step 5: Spectral analysis of the fluctuations
    fft_vals = np.fft.rfft(log_ratio - np.mean(log_ratio))
    power_spectrum = np.abs(fft_vals)**2
    freqs = np.fft.rfftfreq(len(log_ratio))

    # Find dominant frequencies
    top_freq_idx = np.argsort(power_spectrum[1:])[-5:] + 1  # skip DC
    print(f"\n  Top 5 spectral peaks (frequency in units of 1/prime_index):")
    for idx in top_freq_idx[::-1]:
        print(f"    freq = {freqs[idx]:.6f}, period ≈ {1/freqs[idx]:.1f} primes, "
              f"power = {power_spectrum[idx]:.2f}")

    # Is the spectrum flat (white noise) or colored?
    # Test: power ∝ 1/f^α
    valid = (freqs > 0) & (power_spectrum > 0)
    if np.sum(valid) > 10:
        log_f = np.log(freqs[valid])
        log_P = np.log(power_spectrum[valid])
        spec_slope, _, r_spec, _, _ = stats.linregress(log_f, log_P)
        print(f"\n  Spectral slope: P(f) ∝ f^{spec_slope:.2f} (r={r_spec:.3f})")
        if abs(spec_slope) < 0.5:
            print(f"    -> Nearly white noise (magnitude fluctuations are random)")
        elif spec_slope < -0.5:
            print(f"    -> Red/pink noise (long-range correlations in magnitude)")
        else:
            print(f"    -> Blue noise (anti-correlated magnitude fluctuations)")


# ============================================================
# MAIN
# ============================================================

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base, 'wobble_primes_100000.csv')

    print("Loading data...")
    data = load_wobble_data(csv_path)
    print(f"Loaded {len(data)} primes, range p={data[0]['p']} to p={data[-1]['p']}")

    max_p = data[-1]['p'] + 10
    print(f"Computing sieves up to {max_p}...")
    mu, is_prime, primes_list = compute_mobius_sieve(max_p)
    phi = euler_totient_sieve(max_p)
    M_arr = mertens_array(mu, max_p)

    # Analysis 1: Candidate predictors (fast, uses precomputed data)
    results1, dw_norm = analyze_magnitude_predictors(data, mu, M_arr, phi)

    # Analysis 3: The 2-bit picture
    analyze_two_bit_picture(data, mu, M_arr)

    # Analysis 4: Twin primes
    analyze_twin_primes(data, mu, M_arr, is_prime)

    # Analysis 5: Scaling law
    slope, intercept = analyze_wobble_scaling(data)

    # Analysis 6: Binned statistics
    analyze_binned(data)

    # Analysis 7: Fluctuation structure
    analyze_fluctuation_structure(data, mu, M_arr)

    # Analysis 2: Detailed Farey stats (SLOW - limited to small primes)
    print("\n" + "=" * 80)
    print("Starting Analysis 2 (detailed Farey displacement stats)...")
    print("This is slow — computing for primes up to 1000...")
    results2 = analyze_normalized_dw(data, mu, M_arr, max_farey_p=1000)

    print("\n" + "=" * 80)
    print("ALL ANALYSES COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
