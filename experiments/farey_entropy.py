#!/usr/bin/env python3
"""
INFORMATION-THEORETIC ANALYSIS OF THE FAREY-MERTENS BRIDGE
============================================================

The bridge identity  sum_{b<=p} sum_{a: gcd(a,b)=1} e^{2*pi*i*a*p/b} = M(p) + 2
compresses ~3p^2/pi^2 geometric data points into one integer.

This script computes:
1. Shannon entropy of Farey gap distributions and its growth
2. Mutual information I(M(p); delta_W(p))
3. Kolmogorov complexity estimates (description length analysis)
4. Rate-distortion analysis for predicting delta_W
5. Error-correcting code structure of the bridge identity
"""

import numpy as np
from math import gcd, sqrt, pi, log, log2, floor, ceil
import csv
import os
import json
from collections import Counter, defaultdict
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CORE NUMBER-THEORETIC FUNCTIONS
# ============================================================

def compute_mobius_sieve(limit):
    """Compute mu(n) for all n <= limit."""
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
    """Compute phi(n) for all n <= limit."""
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i
    return phi


def mertens_array(mu, N):
    """M(k) = sum_{j=1}^k mu(j) for k=0..N."""
    M = np.zeros(N + 1, dtype=int)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M


def farey_sequence_gaps(N):
    """Compute all gaps f_{j+1} - f_j in the Farey sequence F_N."""
    # Use the mediant-based generator for exact arithmetic
    gaps = []
    a, b, c, d = 0, 1, 1, N
    prev_val = 0.0
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        curr_val = a / b
        gaps.append(curr_val - prev_val)
        prev_val = curr_val
    return gaps


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
# SECTION 1: ENTROPY OF FAREY GAP DISTRIBUTIONS
# ============================================================

def analyze_farey_entropy():
    """
    Compute H(N) = -sum g_j * log(g_j) for Farey sequences.
    Also track H change at primes vs composites.
    """
    print("=" * 70)
    print("SECTION 1: ENTROPY OF FAREY GAP DISTRIBUTIONS")
    print("=" * 70)

    # Compute entropy for a range of N values
    # We need to go up to moderate N (Farey sequence generation is O(N^2))
    N_values = list(range(2, 302))  # up to 301
    entropies = {}

    print("Computing Farey gap entropies for N = 2 to 301...")
    for N in N_values:
        gaps = farey_sequence_gaps(N)
        # Shannon entropy using gaps as probability weights (they sum to 1)
        H = 0.0
        for g in gaps:
            if g > 0:
                H -= g * log2(g)
        entropies[N] = H

    # Extract data
    Ns = sorted(entropies.keys())
    Hs = [entropies[N] for N in Ns]

    # Fit H(N) ~ a * log(N) + b
    log_Ns = [log(N) for N in Ns]
    slope_log, intercept_log, r_log, _, _ = stats.linregress(log_Ns, Hs)

    # Fit H(N) ~ a * N + b
    slope_lin, intercept_lin, r_lin, _, _ = stats.linregress(Ns, Hs)

    # Fit H(N) ~ a * log^2(N) + b * log(N) + c
    log_Ns_arr = np.array(log_Ns)
    Hs_arr = np.array(Hs)
    coeffs_log2 = np.polyfit(log_Ns_arr, Hs_arr, 2)
    Hs_pred_log2 = np.polyval(coeffs_log2, log_Ns_arr)
    ss_res = np.sum((Hs_arr - Hs_pred_log2)**2)
    ss_tot = np.sum((Hs_arr - np.mean(Hs_arr))**2)
    r2_log2 = 1 - ss_res / ss_tot

    print(f"\n--- Entropy Growth Fits ---")
    print(f"H(N) ~ {slope_log:.4f} * log(N) + {intercept_log:.4f}  (R = {r_log:.6f})")
    print(f"H(N) ~ {slope_lin:.6f} * N + {intercept_lin:.4f}  (R = {r_lin:.6f})")
    print(f"H(N) ~ {coeffs_log2[0]:.4f} * log^2(N) + {coeffs_log2[1]:.4f} * log(N) + {coeffs_log2[2]:.4f}  (R^2 = {r2_log2:.6f})")

    # Sample values
    print(f"\n--- Sample Entropies ---")
    for N in [10, 20, 50, 100, 200, 300]:
        if N in entropies:
            n_fracs = sum(1 for _ in farey_sequence_gaps(N))
            print(f"  H({N}) = {entropies[N]:.4f} bits  ({n_fracs} gaps, max possible = log2({n_fracs}) = {log2(n_fracs):.2f})")

    # Entropy CHANGE at primes vs composites
    mu, is_prime, primes = compute_mobius_sieve(302)
    M = mertens_array(mu, 302)

    delta_H = {}
    for N in range(3, 302):
        delta_H[N] = entropies[N] - entropies[N - 1]

    prime_dH = [(N, delta_H[N], M[N]) for N in range(3, 302) if is_prime[N]]
    composite_dH = [(N, delta_H[N], M[N]) for N in range(4, 302) if not is_prime[N]]

    prime_dH_vals = [x[1] for x in prime_dH]
    composite_dH_vals = [x[1] for x in composite_dH]

    print(f"\n--- Entropy Change at Primes vs Composites ---")
    print(f"  Primes:     mean dH = {np.mean(prime_dH_vals):.6f}, std = {np.std(prime_dH_vals):.6f}")
    print(f"  Composites: mean dH = {np.mean(composite_dH_vals):.6f}, std = {np.std(composite_dH_vals):.6f}")

    # Correlation of dH at primes with M(p)
    prime_dH_arr = np.array(prime_dH_vals)
    prime_M_arr = np.array([x[2] for x in prime_dH])
    prime_p_arr = np.array([x[0] for x in prime_dH])

    corr_dH_M, pval_dH_M = stats.pearsonr(prime_dH_arr, prime_M_arr)
    print(f"\n  Correlation dH(p) vs M(p):  r = {corr_dH_M:.4f}  (p-value = {pval_dH_M:.2e})")

    # Also check correlation of dH with delta_W for small primes
    # Use the CSV data for primes that overlap
    csv_path = os.path.join(SCRIPT_DIR, "wobble_primes_100000.csv")
    wobble_data = load_wobble_data(csv_path)
    wobble_by_p = {d['p']: d for d in wobble_data}

    matched = [(N, delta_H[N], wobble_by_p[N]['delta_w'], wobble_by_p[N]['mertens_p'])
               for N in range(3, 302) if is_prime[N] and N in wobble_by_p]

    if len(matched) > 5:
        dH_matched = np.array([x[1] for x in matched])
        dW_matched = np.array([x[2] for x in matched])
        corr_dH_dW, pval_dH_dW = stats.pearsonr(dH_matched, dW_matched)
        print(f"  Correlation dH(p) vs dW(p): r = {corr_dH_dW:.4f}  (p-value = {pval_dH_dW:.2e})")

    results = {
        'growth_fit_log': {'slope': slope_log, 'intercept': intercept_log, 'R': r_log},
        'growth_fit_linear': {'slope': slope_lin, 'intercept': intercept_lin, 'R': r_lin},
        'growth_fit_log2': {'coeffs': list(coeffs_log2), 'R2': r2_log2},
        'prime_dH_mean': float(np.mean(prime_dH_vals)),
        'composite_dH_mean': float(np.mean(composite_dH_vals)),
        'corr_dH_M': float(corr_dH_M),
        'corr_dH_M_pval': float(pval_dH_M),
        'sample_entropies': {N: entropies[N] for N in [10, 20, 50, 100, 200, 300]},
    }
    if len(matched) > 5:
        results['corr_dH_dW'] = float(corr_dH_dW)
        results['corr_dH_dW_pval'] = float(pval_dH_dW)

    return results


# ============================================================
# SECTION 2: MUTUAL INFORMATION I(M(p); delta_W(p))
# ============================================================

def analyze_mutual_information():
    """
    Compute mutual information between M(p) and various aspects of delta_W(p).
    Uses the full CSV dataset for large-sample statistics.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: MUTUAL INFORMATION  I(M(p); delta_W(p))")
    print("=" * 70)

    csv_path = os.path.join(SCRIPT_DIR, "wobble_primes_100000.csv")
    data = load_wobble_data(csv_path)

    mertens_vals = np.array([d['mertens_p'] for d in data])
    delta_w_vals = np.array([d['delta_w'] for d in data])
    p_vals = np.array([d['p'] for d in data])

    # Sign analysis
    sign_M = np.sign(mertens_vals)
    sign_dW = np.sign(delta_w_vals)

    # Sign agreement rate
    agree = np.sum(sign_M * sign_dW > 0)
    disagree = np.sum(sign_M * sign_dW < 0)
    zero_M = np.sum(sign_M == 0)
    zero_dW = np.sum(sign_dW == 0)
    total_nonzero = agree + disagree
    agreement_rate = agree / total_nonzero if total_nonzero > 0 else 0

    print(f"\n--- Sign Analysis ---")
    print(f"  sign(M) == sign(dW): {agree}/{total_nonzero} = {agreement_rate:.4f}")
    print(f"  M(p) = 0 cases: {zero_M}, dW = 0 cases: {zero_dW}")

    # 2a. Mutual information between sign(M) and sign(dW)
    # Build joint distribution (excluding zeros for clean binary MI)
    mask = (sign_M != 0) & (sign_dW != 0)
    sM = sign_M[mask]
    sW = sign_dW[mask]

    # Joint probabilities
    joint_counts = Counter(zip(sM.tolist(), sW.tolist()))
    n_total = len(sM)
    joint_probs = {k: v / n_total for k, v in joint_counts.items()}

    # Marginals
    p_M_neg = sum(v for (m, w), v in joint_probs.items() if m == -1)
    p_M_pos = sum(v for (m, w), v in joint_probs.items() if m == 1)
    p_W_neg = sum(v for (m, w), v in joint_probs.items() if w == -1)
    p_W_pos = sum(v for (m, w), v in joint_probs.items() if w == 1)

    marg_M = {-1: p_M_neg, 1: p_M_pos}
    marg_W = {-1: p_W_neg, 1: p_W_pos}

    # H(sign(M)), H(sign(dW))
    H_M = -sum(p * log2(p) for p in marg_M.values() if p > 0)
    H_W = -sum(p * log2(p) for p in marg_W.values() if p > 0)

    # H(sign(M), sign(dW))
    H_joint = -sum(p * log2(p) for p in joint_probs.values() if p > 0)

    # I(sign(M); sign(dW)) = H(M) + H(W) - H(M,W)
    I_sign = H_M + H_W - H_joint

    print(f"\n--- Mutual Information (Sign Channel) ---")
    print(f"  H(sign(M))  = {H_M:.4f} bits")
    print(f"  H(sign(dW)) = {H_W:.4f} bits")
    print(f"  H(joint)    = {H_joint:.4f} bits")
    print(f"  I(sign(M); sign(dW)) = {I_sign:.4f} bits")
    print(f"  Channel capacity (max I for binary) = 1.0 bit")
    print(f"  Fraction of capacity used: {I_sign:.4f}")

    # 2b. Mutual information using quantized M(p) and quantized |delta_W|
    # Bin M(p) into categories and |delta_W| into quantiles
    M_bins = np.digitize(mertens_vals, bins=[-np.inf, -10, -5, -2, 0, 2, 5, 10, np.inf])

    # Quantize delta_W into sign + magnitude bins
    dW_sign = np.sign(delta_w_vals)
    dW_abs = np.abs(delta_w_vals)
    dW_quantiles = np.percentile(dW_abs[dW_abs > 0], [25, 50, 75])
    dW_mag_bin = np.digitize(dW_abs, bins=[0] + list(dW_quantiles) + [np.inf])
    # Combined: sign * mag_bin  (gives ~8 categories)
    dW_combined = (dW_sign * 10 + dW_mag_bin).astype(int)

    # Compute MI using discrete estimator
    def discrete_mutual_info(X, Y):
        """Compute I(X;Y) from discrete arrays."""
        n = len(X)
        joint = Counter(zip(X.tolist(), Y.tolist()))
        margX = Counter(X.tolist())
        margY = Counter(Y.tolist())

        mi = 0.0
        for (x, y), count in joint.items():
            pxy = count / n
            px = margX[x] / n
            py = margY[y] / n
            if pxy > 0 and px > 0 and py > 0:
                mi += pxy * log2(pxy / (px * py))
        return mi

    I_M_dW_full = discrete_mutual_info(M_bins, dW_combined)

    # Also compute MI between just M and |dW| (magnitude only)
    I_M_dW_mag = discrete_mutual_info(M_bins, dW_mag_bin)

    print(f"\n--- Mutual Information (Quantized Channels) ---")
    print(f"  I(M_binned; sign*mag_dW) = {I_M_dW_full:.4f} bits")
    print(f"  I(M_binned; |dW| bins)   = {I_M_dW_mag:.4f} bits  (magnitude only)")

    # 2c. How many bits does M(p) transmit about delta_W?
    # Compare with entropy of delta_W's sign
    H_dW_sign = -sum(p * log2(p) for p in [p_W_neg, p_W_pos] if p > 0)
    print(f"\n--- Information Budget ---")
    print(f"  H(sign(dW))              = {H_dW_sign:.4f} bits (max possible sign info)")
    print(f"  I(sign(M); sign(dW))     = {I_sign:.4f} bits  (M transmits this about sign)")
    print(f"  Remaining uncertainty     = {H_dW_sign - I_sign:.4f} bits")
    print(f"  Total I(M; sign+mag dW)  = {I_M_dW_full:.4f} bits (sign + magnitude)")

    # 2d. Conditional entropy: H(dW | M) vs H(dW)
    # Estimate by binning
    dW_fine_bins = np.digitize(delta_w_vals, bins=np.percentile(delta_w_vals, np.linspace(0, 100, 21)))
    H_dW = discrete_mutual_info(dW_fine_bins, dW_fine_bins)  # This is just H(dW) via self-MI = H
    # Actually compute H(dW) directly
    dW_counts = Counter(dW_fine_bins.tolist())
    n_total_dw = len(dW_fine_bins)
    H_dW_binned = -sum((c/n_total_dw) * log2(c/n_total_dw) for c in dW_counts.values() if c > 0)

    I_M_dW_fine = discrete_mutual_info(M_bins, dW_fine_bins)

    print(f"\n  H(dW, 20-bin)            = {H_dW_binned:.4f} bits")
    print(f"  I(M_binned; dW_20-bin)   = {I_M_dW_fine:.4f} bits")
    print(f"  H(dW | M) ~ {H_dW_binned - I_M_dW_fine:.4f} bits (residual uncertainty)")

    results = {
        'agreement_rate': float(agreement_rate),
        'H_sign_M': float(H_M),
        'H_sign_dW': float(H_W),
        'I_sign': float(I_sign),
        'I_M_dW_full': float(I_M_dW_full),
        'I_M_dW_mag': float(I_M_dW_mag),
        'H_dW_binned': float(H_dW_binned),
        'I_M_dW_fine': float(I_M_dW_fine),
        'joint_probs': {str(k): v for k, v in joint_probs.items()},
    }
    return results


# ============================================================
# SECTION 3: KOLMOGOROV COMPLEXITY / DESCRIPTION LENGTH
# ============================================================

def analyze_kolmogorov():
    """
    Analyze description complexity of delta_W(p).
    - Given M(p): just need residual ~ small correction
    - Without M(p): need full Farey-level computation
    """
    print("\n" + "=" * 70)
    print("SECTION 3: KOLMOGOROV COMPLEXITY / DESCRIPTION LENGTH")
    print("=" * 70)

    csv_path = os.path.join(SCRIPT_DIR, "wobble_primes_100000.csv")
    data = load_wobble_data(csv_path)

    p_vals = np.array([d['p'] for d in data])
    delta_w_vals = np.array([d['delta_w'] for d in data])
    mertens_vals = np.array([d['mertens_p'] for d in data])
    farey_sizes = np.array([d['farey_size_p'] for d in data])

    # Description length analysis:
    # To describe delta_W(p) you need:
    # (a) Without M(p): specify all |F_p| Farey fractions = O(p^2) data
    # (b) With M(p): specify M(p) (log2(|M(p)|) bits) + residual

    # Compression ratio at each prime
    print(f"\n--- Compression via Bridge Identity ---")
    print(f"{'p':>7} {'|F_p|':>8} {'bits(F_p)':>10} {'M(p)':>6} {'bits(M)':>8} {'ratio':>8}")
    print("-" * 55)

    compressions = []
    for i in range(0, min(len(data), 20)):  # First 20 primes for display
        d = data[i]
        p = d['p']
        fp_size = d['farey_size_p']
        M = d['mertens_p']
        bits_farey = fp_size * log2(fp_size) if fp_size > 1 else 1  # entropy of uniform dist over F_p
        bits_M = log2(abs(M) + 1) + 1 if M != 0 else 1  # sign + magnitude
        ratio = bits_farey / bits_M if bits_M > 0 else float('inf')
        compressions.append({'p': p, 'bits_farey': bits_farey, 'bits_M': bits_M, 'ratio': ratio})
        print(f"{p:>7d} {fp_size:>8d} {bits_farey:>10.1f} {M:>6d} {bits_M:>8.2f} {ratio:>8.0f}:1")

    # Statistics over all primes
    all_bits_farey = []
    all_bits_M = []
    all_ratios = []
    for d in data:
        p = d['p']
        fp_size = d['farey_size_p']
        M = d['mertens_p']
        bf = fp_size * log2(fp_size) if fp_size > 1 else 1
        bm = log2(abs(M) + 1) + 1 if M != 0 else 1
        all_bits_farey.append(bf)
        all_bits_M.append(bm)
        all_ratios.append(bf / bm if bm > 0 else 0)

    print(f"\n--- Compression Statistics (all {len(data)} primes) ---")
    print(f"  Mean compression ratio:   {np.mean(all_ratios):,.0f}:1")
    print(f"  Median compression ratio: {np.median(all_ratios):,.0f}:1")
    print(f"  Max compression ratio:    {np.max(all_ratios):,.0f}:1  (at p={data[np.argmax(all_ratios)]['p']})")

    # Residual complexity: how much info is NOT in M(p)?
    # Normalize delta_W by expected scale: delta_W * p^2
    dW_normalized = delta_w_vals * p_vals**2

    # Predict delta_W sign from M(p)
    sign_pred = -np.sign(mertens_vals)  # M(p) < 0 => dW > 0
    sign_actual = np.sign(delta_w_vals)
    sign_errors = np.sum(sign_pred != sign_actual)
    sign_accuracy = 1 - sign_errors / len(data)

    # Residual after removing M(p) sign prediction
    # Fit: dW_normalized ~ alpha * M(p) + residual
    slope, intercept, r_val, _, _ = stats.linregress(mertens_vals, dW_normalized)
    residual = dW_normalized - (slope * mertens_vals + intercept)

    # Information in residual vs original
    H_original = np.std(dW_normalized)
    H_residual = np.std(residual)
    variance_explained = 1 - (H_residual**2 / H_original**2)

    print(f"\n--- Residual Complexity ---")
    print(f"  Sign prediction accuracy from M(p): {sign_accuracy:.4f}")
    print(f"  Linear fit dW*p^2 ~ alpha*M(p): R = {r_val:.4f}")
    print(f"  Variance explained by M(p): {variance_explained:.4f}")
    print(f"  std(dW*p^2):          {H_original:.4f}")
    print(f"  std(residual):        {H_residual:.4f}")
    print(f"  Residual fraction:    {H_residual/H_original:.4f}")

    # Effective bits: how many bits of precision does M(p) give?
    # If M predicts sign with p_correct accuracy, MI bits:
    p_correct = sign_accuracy
    p_wrong = 1 - p_correct
    if 0 < p_correct < 1:
        bits_from_sign = 1 + p_correct * log2(p_correct) + p_wrong * log2(p_wrong)
    else:
        bits_from_sign = 1.0
    print(f"  Effective sign bits from M(p): {bits_from_sign:.4f} of 1.0 possible")

    results = {
        'mean_compression_ratio': float(np.mean(all_ratios)),
        'median_compression_ratio': float(np.median(all_ratios)),
        'max_compression_ratio': float(np.max(all_ratios)),
        'sign_accuracy': float(sign_accuracy),
        'linear_R': float(r_val),
        'variance_explained': float(variance_explained),
        'effective_sign_bits': float(bits_from_sign),
        'residual_fraction': float(H_residual / H_original),
    }
    return results


# ============================================================
# SECTION 4: RATE-DISTORTION ANALYSIS
# ============================================================

def analyze_rate_distortion():
    """
    Rate-distortion: how many bits to predict delta_W(p) to accuracy epsilon?
    """
    print("\n" + "=" * 70)
    print("SECTION 4: RATE-DISTORTION ANALYSIS")
    print("=" * 70)

    csv_path = os.path.join(SCRIPT_DIR, "wobble_primes_100000.csv")
    data = load_wobble_data(csv_path)

    mertens_vals = np.array([d['mertens_p'] for d in data])
    delta_w_vals = np.array([d['delta_w'] for d in data])
    p_vals = np.array([d['p'] for d in data])
    farey_sizes = np.array([d['farey_size_p'] for d in data])

    # Normalize: work with dW * p^2 (roughly O(1) quantity)
    dW_norm = delta_w_vals * p_vals**2

    print(f"\n--- Normalized delta_W * p^2 statistics ---")
    print(f"  Mean:   {np.mean(dW_norm):.4f}")
    print(f"  Std:    {np.std(dW_norm):.4f}")
    print(f"  Range:  [{np.min(dW_norm):.4f}, {np.max(dW_norm):.4f}]")

    # Level 0: No information (just predict mean)
    mse_0 = np.var(dW_norm)  # variance = MSE of predicting mean

    # Level 1: M(p) sign only (1 bit)
    # Predict: dW_norm > 0 if M(p) < 0, dW_norm < 0 if M(p) > 0
    pred_1 = np.where(mertens_vals < 0, np.mean(dW_norm[mertens_vals < 0]),
                      np.where(mertens_vals > 0, np.mean(dW_norm[mertens_vals > 0]),
                               np.mean(dW_norm)))
    mse_1 = np.mean((dW_norm - pred_1)**2)

    # Level 2: M(p) value (linear regression, ~4-5 bits for typical M values)
    slope, intercept, _, _, _ = stats.linregress(mertens_vals, dW_norm)
    pred_2 = slope * mertens_vals + intercept
    mse_2 = np.mean((dW_norm - pred_2)**2)
    bits_M = np.mean([log2(abs(m) + 1) + 1 for m in mertens_vals])

    # Level 3: M(p) + M(p)/sqrt(p) (adds scale info, ~1 more bit)
    m_over_sqrt = np.array([d['m_over_sqrt_p'] for d in data])
    X3 = np.column_stack([mertens_vals, m_over_sqrt])
    # Manual least squares
    X3_aug = np.column_stack([X3, np.ones(len(X3))])
    beta3, _, _, _ = np.linalg.lstsq(X3_aug, dW_norm, rcond=None)
    pred_3 = X3_aug @ beta3
    mse_3 = np.mean((dW_norm - pred_3)**2)

    # Level 4: M(p) + previous M values (2-history, ~8-10 bits)
    mu, _, primes = compute_mobius_sieve(100001)
    M_arr = mertens_array(mu, 100001)

    # Get M(p-1) for each prime
    M_pm1 = np.array([int(M_arr[d['p'] - 1]) for d in data])
    X4 = np.column_stack([mertens_vals, M_pm1, m_over_sqrt, p_vals])
    X4_aug = np.column_stack([X4, np.ones(len(X4))])
    beta4, _, _, _ = np.linalg.lstsq(X4_aug, dW_norm, rcond=None)
    pred_4 = X4_aug @ beta4
    mse_4 = np.mean((dW_norm - pred_4)**2)

    # Build rate-distortion table
    print(f"\n--- Rate-Distortion Table ---")
    print(f"{'Level':>6} {'Description':>30} {'~Bits':>8} {'MSE':>12} {'RMSE':>10} {'% var reduced':>14}")
    print("-" * 85)

    levels = [
        (0, "No information", 0, mse_0),
        (1, "sign(M(p)) only", 1, mse_1),
        (2, "M(p) value (linear)", bits_M, mse_2),
        (3, "M(p) + M/sqrt(p)", bits_M + 1, mse_3),
        (4, "M(p) + M(p-1) + p + M/sqrt", bits_M + bits_M + log2(50000), mse_4),
    ]

    for lvl, desc, bits, mse in levels:
        rmse = sqrt(mse)
        var_red = (1 - mse / mse_0) * 100
        print(f"{lvl:>6d} {desc:>30s} {bits:>8.1f} {mse:>12.4f} {rmse:>10.4f} {var_red:>13.1f}%")

    # What gives the "next bits" after M(p)?
    # Analyze residual after linear M(p) prediction
    residual = dW_norm - pred_2
    print(f"\n--- What gives the next bits after M(p)? ---")
    print(f"  Residual std after M(p) linear: {np.std(residual):.4f}")

    # Candidates: mu(p+1), gap to next prime, p mod small numbers
    candidates = {}

    # mu(p+1) = Mobius at p+1
    mu_pp1 = np.array([mu[d['p'] + 1] for d in data])
    corr, pval = stats.pearsonr(residual, mu_pp1)
    candidates['mu(p+1)'] = (corr, pval)

    # Gap to next prime
    prime_set = set(primes)
    gaps = []
    for d in data:
        p = d['p']
        g = 1
        while p + g not in prime_set and p + g < 100002:
            g += 1
        gaps.append(g)
    gaps = np.array(gaps)
    corr, pval = stats.pearsonr(residual[:len(gaps)], gaps[:len(residual)])
    candidates['prime gap'] = (corr, pval)

    # p mod 6
    p_mod6 = p_vals % 6
    corr, pval = stats.pearsonr(residual, p_mod6.astype(float))
    candidates['p mod 6'] = (corr, pval)

    # Previous dW (autoregressive)
    corr, pval = stats.pearsonr(residual[1:], residual[:-1])
    candidates['residual lag-1'] = (corr, pval)

    # |M(p)| (magnitude)
    corr, pval = stats.pearsonr(residual, np.abs(mertens_vals))
    candidates['|M(p)|'] = (corr, pval)

    # M(p)^2
    corr, pval = stats.pearsonr(residual, mertens_vals**2)
    candidates['M(p)^2'] = (corr, pval)

    # Wobble at p-1
    wobble_pm1 = np.array([d['wobble_pm1'] for d in data])
    corr, pval = stats.pearsonr(residual, wobble_pm1)
    candidates['W(p-1)'] = (corr, pval)

    print(f"\n  Candidate predictors for residual (after M(p) linear):")
    for name, (corr, pval) in sorted(candidates.items(), key=lambda x: -abs(x[1][0])):
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"    {name:>20s}: r = {corr:+.4f}  (p = {pval:.2e}) {sig}")

    results = {
        'mse_levels': {desc: float(mse) for _, desc, _, mse in levels},
        'bits_M_average': float(bits_M),
        'residual_std': float(np.std(residual)),
        'candidate_correlations': {name: {'r': float(c), 'p': float(p)} for name, (c, p) in candidates.items()},
    }
    return results


# ============================================================
# SECTION 5: ERROR-CORRECTING CODE STRUCTURE
# ============================================================

def analyze_ecc_structure():
    """
    The bridge identity as an error-correcting code:
    phi(b) unit vectors -> mu(b) in {-1, 0, +1} for each b.
    This is like a repetition code: message is mu(b), codeword is the phi(b) exponentials.

    Analyze: rate, distance, and coding-theoretic parameters.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: ERROR-CORRECTING CODE STRUCTURE")
    print("=" * 70)

    mu, is_prime, primes = compute_mobius_sieve(1000)
    phi = euler_totient_sieve(1000)
    M = mertens_array(mu, 1000)

    # For each prime p, the bridge identity says:
    #   sum_{b=1}^{p} sum_{a: gcd(a,b)=1} e^{2*pi*i*a*p/b} = M(p) + 2
    # This is a sum of phi(b) terms for each b, grouped by b.
    # For each b, the inner sum = mu(b) * (Ramanujan sum).
    # So we have p "blocks" of sizes phi(1), phi(2), ..., phi(p).
    # The block for b transmits mu(b) via phi(b) unit vectors.

    print(f"\n--- Code Parameters at Sample Primes ---")
    print(f"{'p':>5} {'n=|F_p|':>8} {'k=p':>5} {'rate k/n':>10} {'phi_max':>8} {'phi_min':>8} {'M(p)':>6}")
    print("-" * 55)

    code_params = []
    for p in [11, 23, 47, 97, 197, 397, 503, 997]:
        if not is_prime[p]:
            continue
        n_codeword = sum(phi[b] for b in range(1, p + 1))  # total codeword length
        k_message = p  # number of mu(b) symbols
        rate = k_message / n_codeword
        phi_vals = [phi[b] for b in range(1, p + 1)]
        code_params.append({
            'p': p, 'n': n_codeword, 'k': k_message,
            'rate': rate, 'phi_max': max(phi_vals), 'phi_min': min(phi_vals),
            'M': int(M[p])
        })
        print(f"{p:>5d} {n_codeword:>8d} {k_message:>5d} {rate:>10.6f} {max(phi_vals):>8d} {min(phi_vals):>8d} {M[p]:>6d}")

    # The "message" alphabet is {-1, 0, +1} (ternary).
    # How many symbols of each type?
    print(f"\n--- Message Symbol Distribution (mu values up to p) ---")
    for p in [97, 197, 503, 997]:
        if not is_prime[p]:
            continue
        mu_vals = [mu[b] for b in range(1, p + 1)]
        c_neg = mu_vals.count(-1)
        c_zero = mu_vals.count(0)
        c_pos = mu_vals.count(1)
        total = c_neg + c_zero + c_pos
        H_msg = 0
        for c in [c_neg, c_zero, c_pos]:
            if c > 0:
                p_c = c / total
                H_msg -= p_c * log2(p_c)
        print(f"  p={p:>4d}: mu=-1: {c_neg:>4d} ({c_neg/total:.3f}), "
              f"mu=0: {c_zero:>4d} ({c_zero/total:.3f}), "
              f"mu=+1: {c_pos:>4d} ({c_pos/total:.3f}), H={H_msg:.4f} bits/symbol")

    # Repetition structure: each mu(b) is "repeated" phi(b) times
    # The effective repetition factor
    print(f"\n--- Repetition Factors ---")
    for p in [97, 997]:
        if not is_prime[p]:
            continue
        reps = [(b, phi[b], mu[b]) for b in range(1, p + 1)]
        nonzero_reps = [(b, ph, m) for b, ph, m in reps if m != 0]
        rep_factors = [ph for _, ph, _ in nonzero_reps]
        mean_rep = np.mean(rep_factors)
        total_symbols = sum(ph for _, ph, _ in nonzero_reps)
        n_messages = len(nonzero_reps)
        print(f"  p={p}: {n_messages} nonzero mu symbols, "
              f"mean repetition = {mean_rep:.1f}, "
              f"total codeword symbols = {total_symbols}")

    # Destructive interference analysis
    # The sum of phi(b) unit vectors for each b gives mu(b).
    # This means (phi(b) - |mu(b)|) vectors "cancel out" through interference.
    print(f"\n--- Destructive Interference (Cancellation) ---")
    print(f"{'p':>5} {'total phi':>10} {'|sum|=|M+2|':>12} {'cancelled':>10} {'cancel%':>10}")
    print("-" * 50)

    for p in [11, 23, 47, 97, 197, 397, 503, 997]:
        if not is_prime[p]:
            continue
        total_phi = sum(phi[b] for b in range(1, p + 1))
        sum_val = abs(int(M[p]) + 2)
        cancelled = total_phi - sum_val
        cancel_pct = cancelled / total_phi * 100
        print(f"{p:>5d} {total_phi:>10d} {sum_val:>12d} {cancelled:>10d} {cancel_pct:>9.4f}%")

    # Channel model: the bridge identity as a noisy channel
    # "True signal" = M(p) + 2, "noise" = the individual exponential sums
    # SNR analysis
    print(f"\n--- Signal-to-Noise Ratio ---")
    csv_path = os.path.join(SCRIPT_DIR, "wobble_primes_100000.csv")
    data = load_wobble_data(csv_path)

    p_vals = np.array([d['p'] for d in data])
    M_vals = np.array([d['mertens_p'] for d in data])
    fp_sizes = np.array([d['farey_size_p'] for d in data])

    # Signal power: (M(p)+2)^2, Noise power: |F_p| (variance of sum of unit vectors)
    signal_power = (M_vals + 2)**2
    noise_power = fp_sizes  # each phi(b) exponential has variance ~1, sum has var ~ n
    snr = signal_power / noise_power
    snr_db = 10 * np.log10(snr + 1e-10)

    print(f"  Mean SNR:    {np.mean(snr):.6f} ({np.mean(snr_db):.1f} dB)")
    print(f"  Median SNR:  {np.median(snr):.6f} ({np.median(snr_db):.1f} dB)")
    print(f"  SNR at p=97: {snr[list(p_vals).index(97)]:.6f}")

    # Despite incredibly low SNR, the sum is EXACT (not noisy).
    # This is the miracle: perfect interference gives exact integer.
    print(f"\n  KEY INSIGHT: Despite SNR -> 0 as p -> inf, the bridge")
    print(f"  identity gives EXACT integers. This is because the 'noise'")
    print(f"  is not random -- it is structured by number theory.")
    print(f"  The code has distance = infinity in coding theory terms:")
    print(f"  no 'errors' are possible because the identity is algebraic.")

    results = {
        'code_params': code_params,
        'snr_mean': float(np.mean(snr)),
        'snr_median': float(np.median(snr)),
    }
    return results


# ============================================================
# MAIN
# ============================================================

def main():
    print("INFORMATION-THEORETIC ANALYSIS OF THE FAREY-MERTENS BRIDGE")
    print("=" * 70)
    print()

    all_results = {}

    # Section 1: Farey Entropy
    all_results['farey_entropy'] = analyze_farey_entropy()

    # Section 2: Mutual Information
    all_results['mutual_information'] = analyze_mutual_information()

    # Section 3: Kolmogorov Complexity
    all_results['kolmogorov'] = analyze_kolmogorov()

    # Section 4: Rate-Distortion
    all_results['rate_distortion'] = analyze_rate_distortion()

    # Section 5: ECC Structure
    all_results['ecc_structure'] = analyze_ecc_structure()

    # Save results
    results_path = os.path.join(SCRIPT_DIR, "farey_entropy_results.json")
    with open(results_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nResults saved to {results_path}")
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = main()
