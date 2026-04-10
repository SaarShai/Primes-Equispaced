#!/usr/bin/env python3
"""
Hristov Stability Test: Does "nobility" predict DYNAMICAL stability?
=====================================================================

Tests whether continued-fraction-based measures of three-body orbit words
correlate with the TRUE Lyapunov exponents from Hristov et al. (2025,
arXiv:2503.00432), who computed monodromy eigenvalues to 30 correct digits
for 4,860 free-fall orbits.

The key question: our "nobility" measure (fraction of 1s in the CF period
of the Gamma(2) fixed point) predicts braid entropy with AUC=0.98 — but
braid entropy comes from the SAME matrix as CF (circularity objection).
If nobility also predicts Hristov's independently-computed Lyapunov exponents,
the circularity objection is dead.

Data source: https://db2.fmi.uni-sofia.bg/3bodysym4860/

Approach:
---------
Hristov uses SYZYGY sequences (symbols 1,2,3 = which body is in the middle
at collinearity). These relate to the free group on {1,2,3} with 3 generators.
Our Li-Liao code uses free-group words on Gamma(2) generators {a,b,A,B}.

The mapping: syzygy symbols {1,2,3} correspond to three transpositions of
the bodies. For equal-mass systems, a syzygy of type k means body k is in
the middle. The transition 1->2 or 2->1 corresponds to one generator,
1->3 or 3->1 to another, etc.

We compute MULTIPLE "nobility-like" measures directly from the syzygy sequence:
1. Repetition fraction: fraction of consecutive identical symbols (stutters)
2. Pattern complexity: number of distinct n-grams / maximum possible
3. Algebraic measures: map to braid generators and compute trace/discriminant
4. Entropy rate of the syzygy sequence itself

Then correlate ALL of these with log(|mu_max|) from Hristov's data.

Author: Saar (with Claude)
Date: 2026-03-29
"""

import os
import re
import math
import numpy as np
from scipy import stats
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

# Try mpmath for high-precision floor
try:
    import mpmath
    mpmath.mp.dps = 50
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
DATA_DIR = os.path.join(OUTPUT_DIR, "hristov_data")


# ═══════════════════════════════════════════════════════════════════
# 1. DATA LOADING
# ═══════════════════════════════════════════════════════════════════

def load_syzygies(path):
    """Load syzygy sequences from syzygies.txt.
    Format: <sequence_of_123> <integer> <integer>
    """
    syzygies = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 1:
                seq = parts[0]
                extra = parts[1:] if len(parts) > 1 else []
                syzygies.append({
                    'sequence': seq,
                    'length': len(seq),
                    'extra': extra,
                })
    return syzygies


def load_exponents(path):
    """Load max eigenvalue and Lyapunov exponent from res_exponents.txt.
    Format: N)  <max_abs_eigenvalue>  <lyapunov_exponent>
    """
    exponents = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parse: "1)  0.501...e7  0.154...e2"
            m = re.match(r'(\d+)\)\s+([\d.e+-]+)\s+([\d.e+-]+)', line)
            if m:
                idx = int(m.group(1))
                mu_max = float(m.group(2))
                lyap = float(m.group(3))
                exponents.append({
                    'index': idx,
                    'mu_max': mu_max,
                    'log_mu_max': lyap,  # This IS ln(mu_max)
                })
    return exponents


def load_eigenvalues(path):
    """Load full eigenvalue data from res_eigen.txt.
    Each orbit block: 'i.c. N -->' followed by 4 complex eigenvalues,
    blank line, then 4 absolute values.
    """
    eigenvalues = []
    with open(path, 'r') as f:
        content = f.read()

    blocks = re.split(r'i\.c\.\s+(\d+)\s+-->', content)
    # blocks[0] is before first match, then alternating: index, data
    for i in range(1, len(blocks), 2):
        idx = int(blocks[i])
        data = blocks[i+1].strip()
        lines = [l.strip() for l in data.split('\n') if l.strip()]

        # Parse the 4 complex eigenvalues (first 4 lines)
        complex_eigs = []
        for j in range(min(4, len(lines))):
            line = lines[j]
            # Parse: "0.501...e7  +  0.e0i" or "0.501...e7  +  0.367...e0i"
            m = re.match(r'([-\d.e]+)\s+([+-])\s+([\d.e+-]+)i', line)
            if m:
                real = float(m.group(1))
                sign = 1 if m.group(2) == '+' else -1
                imag = sign * float(m.group(3))
                complex_eigs.append(complex(real, imag))

        # Parse the 4 absolute values (next 4 lines, after blank)
        abs_vals = []
        for j in range(4, min(8, len(lines))):
            try:
                abs_vals.append(float(lines[j]))
            except (ValueError, IndexError):
                pass

        eigenvalues.append({
            'index': idx,
            'complex_eigenvalues': complex_eigs,
            'abs_eigenvalues': abs_vals,
        })

    return eigenvalues


# ═══════════════════════════════════════════════════════════════════
# 2. SYZYGY-BASED MEASURES (direct from the sequence)
# ═══════════════════════════════════════════════════════════════════

def syzygy_measures(seq):
    """Compute various measures from a syzygy sequence string of {1,2,3}."""
    n = len(seq)
    if n == 0:
        return {}

    measures = {}
    measures['length'] = n

    # --- Stutter fraction: consecutive identical symbols ---
    stutters = sum(1 for i in range(1, n) if seq[i] == seq[i-1])
    measures['stutter_frac'] = stutters / (n - 1) if n > 1 else 0

    # --- Symbol frequencies ---
    counts = Counter(seq)
    freq = {s: counts.get(s, 0) / n for s in '123'}
    measures['freq_1'] = freq['1']
    measures['freq_2'] = freq['2']
    measures['freq_3'] = freq['3']
    measures['freq_entropy'] = -sum(f * math.log(f) for f in freq.values() if f > 0)
    measures['freq_max'] = max(freq.values())
    measures['freq_balance'] = 1 - max(freq.values())  # how balanced

    # --- Transition matrix entropy ---
    transitions = defaultdict(int)
    for i in range(n - 1):
        transitions[(seq[i], seq[i+1])] += 1
    total_trans = sum(transitions.values())
    if total_trans > 0:
        trans_probs = {k: v/total_trans for k, v in transitions.items()}
        measures['trans_entropy'] = -sum(p * math.log(p) for p in trans_probs.values() if p > 0)
    else:
        measures['trans_entropy'] = 0

    # --- Reduced word (cancel stutters = free group reduction) ---
    reduced = []
    for ch in seq:
        if reduced and reduced[-1] == ch:
            reduced.pop()  # cancel stutter
        else:
            reduced.append(ch)
    measures['reduced_length'] = len(reduced)
    measures['reduction_ratio'] = len(reduced) / n if n > 0 else 0

    # --- N-gram complexity ---
    for ng_len in [2, 3, 4]:
        if n >= ng_len:
            ngrams = set()
            for i in range(n - ng_len + 1):
                ngrams.add(seq[i:i+ng_len])
            max_possible = min(3**ng_len, n - ng_len + 1)
            measures[f'ngram_{ng_len}_complexity'] = len(ngrams) / max_possible if max_possible > 0 else 0
        else:
            measures[f'ngram_{ng_len}_complexity'] = 0

    # --- Palindrome structure ---
    is_palindrome = seq == seq[::-1]
    measures['is_palindrome'] = 1 if is_palindrome else 0

    # --- Run-length encoding complexity ---
    runs = []
    current = seq[0]
    count = 1
    for i in range(1, n):
        if seq[i] == current:
            count += 1
        else:
            runs.append((current, count))
            current = seq[i]
            count = 1
    runs.append((current, count))
    measures['num_runs'] = len(runs)
    measures['mean_run_length'] = n / len(runs) if runs else 1
    measures['max_run_length'] = max(c for _, c in runs)

    return measures


# ═══════════════════════════════════════════════════════════════════
# 3. BRAID GROUP MAPPING: Syzygy -> Braid -> Gamma(2) -> CF
# ═══════════════════════════════════════════════════════════════════

def syzygy_to_braid_word(seq):
    """
    Map syzygy sequence to braid group generators.

    In the 3-body problem, syzygies correspond to crossings in the braid:
    - When body 2 is in the middle (syzygy type 2): bodies 1 and 3 swap
      -> this is sigma_1 or sigma_1^{-1} depending on direction
    - When body 1 is in the middle (type 1): bodies 2 and 3 swap
      -> sigma_2 or sigma_2^{-1}
    - When body 3 is in the middle (type 3): bodies 1 and 2 swap
      -> sigma_1 or sigma_1^{-1}

    For the Gamma(2) mapping, we use transitions between syzygy types:
    Transition i->j maps to a specific Gamma(2) generator.

    Alternatively: the sequence of syzygy types directly gives a word
    in the free group F_3 = <s1, s2, s3>. The reduced word in F_3
    can be mapped to Gamma(2) via the standard representation.

    For our purposes, we compute the Gamma(2) matrix directly from
    the transition structure.
    """
    # Map transitions to Gamma(2) generators
    # Following Montgomery's convention:
    # The kernel of B_3 -> S_3 is isomorphic to F_2 (free group on 2 generators)
    # which maps to Gamma(2) < SL(2,Z).
    #
    # For equal masses, the syzygy transition i->j (i != j) corresponds to
    # a braid crossing. The pair of transitions determines the Gamma(2) generator.
    #
    # Standard mapping from braid group B_3 to SL(2,Z):
    #   sigma_1 -> [[1, 1], [0, 1]]
    #   sigma_2 -> [[1, 0], [-1, 1]]
    #
    # For Gamma(2):
    #   a = sigma_1^2 -> [[1, 2], [0, 1]]
    #   b = sigma_2^2 -> [[1, 0], [2, 1]]  (note: should be [[1,0],[-2,1]] for inverse)

    # Approach: map consecutive DIFFERENT syzygy symbols to generators
    # Type 1 (body 1 middle) -> sigma_2 crossing
    # Type 2 (body 2 middle) -> sigma_1 crossing  (bodies 1,3 are outer)
    # Type 3 (body 3 middle) -> sigma_1 crossing  (but different orientation)

    # For the Hristov data with central symmetry, transitions have a specific structure.
    # The syzygy sequence encodes the topology. Two orbits with the same
    # reduced syzygy sequence are in the same topological class.

    # We'll use the TRANSITION MATRIX approach:
    # For each consecutive pair (s_i, s_{i+1}) with s_i != s_{i+1}:
    #   1->2 or 2->1: generator a (or A)
    #   1->3 or 3->1: generator b (or B)
    #   2->3 or 3->2: generator ab (composition)

    # Simple approach: map each syzygy symbol to a Gamma(2) generator
    # and multiply. The "nobility" of the resulting matrix is what we test.

    # Following the Li-Liao convention used in our existing code:
    # The free-group word uses {a, b, A, B} where:
    #   a = [[1,2],[0,1]], A = a^{-1} = [[1,-2],[0,1]]
    #   b = [[1,0],[2,1]], B = b^{-1} = [[1,0],[-2,1]]

    # Map syzygy transitions to free-group letters
    word = []
    for i in range(len(seq) - 1):
        s1, s2 = seq[i], seq[i+1]
        if s1 == s2:
            continue  # stutter = identity
        if (s1, s2) in [('1', '2'), ('2', '1')]:
            word.append('a' if s1 < s2 else 'A')
        elif (s1, s2) in [('2', '3'), ('3', '2')]:
            word.append('b' if s1 < s2 else 'B')
        elif (s1, s2) in [('1', '3'), ('3', '1')]:
            word.append('a' if s1 < s2 else 'A')
            word.append('b' if s1 < s2 else 'B')

    return ''.join(word)


def mat_mul(A, B):
    """Multiply 2x2 matrices using Python ints."""
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
    ]


GENERATORS = {
    'a': [[1, 2], [0, 1]],
    'b': [[1, 0], [2, 1]],
    'A': [[1, -2], [0, 1]],
    'B': [[1, 0], [-2, 1]],
}
IDENTITY = [[1, 0], [0, 1]]


def word_to_matrix(word):
    """Multiply generators left to right."""
    M = [row[:] for row in IDENTITY]
    for ch in word:
        if ch not in GENERATORS:
            continue
        M = mat_mul(M, GENERATORS[ch])
    return M


def matrix_trace(M):
    return M[0][0] + M[1][1]


def matrix_det(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]


def exact_cf(M, max_terms=200):
    """Compute CF of the attracting fixed point of the Mobius transform."""
    a, b = M[0][0], M[0][1]
    c, d = M[1][0], M[1][1]

    if c == 0:
        return None

    D = (a + d)**2 - 4
    if D <= 0:
        return None

    isqrt_D = math.isqrt(D)
    if isqrt_D * isqrt_D == D:
        return None  # rational FP, skip

    # Determine attracting FP sign
    if HAS_MPMATH:
        sqrt_D_mp = mpmath.sqrt(D)
        z_plus = (mpmath.mpf(a - d) + sqrt_D_mp) / (2 * mpmath.mpf(c))
        z_minus = (mpmath.mpf(a - d) - sqrt_D_mp) / (2 * mpmath.mpf(c))
        dp = abs(c * z_plus + d)
        dm = abs(c * z_minus + d)
        sign = +1 if dp > dm else -1
    else:
        sqrt_D_f = math.sqrt(D)
        z_plus = ((a - d) + sqrt_D_f) / (2 * c)
        z_minus = ((a - d) - sqrt_D_f) / (2 * c)
        dp = abs(c * z_plus + d)
        dm = abs(c * z_minus + d)
        sign = +1 if dp > dm else -1

    # Set up surd: |z| = (P + q*sqrt(D)) / Q
    P0 = d - a
    q0 = -sign
    R0 = 2 * c

    if HAS_MPMATH:
        val = (mpmath.mpf(P0) + q0 * sqrt_D_mp) / mpmath.mpf(R0)
    else:
        val = (P0 + q0 * math.sqrt(D)) / R0

    if val < 0:
        P0, q0, R0 = -P0, -q0, -R0

    P, q, Q = P0, q0, R0
    cf = []
    states = {}

    if HAS_MPMATH:
        sqrt_D_mp = mpmath.sqrt(D)

    for i in range(max_terms):
        if HAS_MPMATH:
            val_mp = (mpmath.mpf(P) + q * sqrt_D_mp) / mpmath.mpf(Q)
            a_n = int(mpmath.floor(val_mp))
        else:
            val_f = (P + q * math.sqrt(D)) / Q
            a_n = int(math.floor(val_f))

        cf.append(a_n)
        P_rem = P - a_n * Q
        denom_new = D - P_rem * P_rem
        if denom_new == 0:
            break

        Q_next = (D - P_rem * P_rem) // Q
        P_next = -P_rem
        q_next = q

        if Q_next < 0:
            P_next, q_next, Q_next = -P_next, -q_next, -Q_next

        state = (P_next, q_next, Q_next)
        if state in states:
            j = states[state]
            preperiod = cf[:j]
            period = cf[j:]
            return {'cf': cf, 'preperiod': preperiod, 'period': period}

        states[state] = i + 1
        P, q, Q = P_next, q_next, Q_next

    return {'cf': cf, 'preperiod': cf, 'period': []}


def cf_nobility(cf_data):
    """Compute nobility and related measures from CF data."""
    if cf_data is None:
        return None

    period = cf_data.get('period', [])
    full = cf_data.get('cf', [])
    relevant = period if period else full[1:] if len(full) > 1 else [1]
    if not relevant:
        relevant = [1]

    abs_rel = [abs(a) for a in relevant if a != 0]
    if not abs_rel:
        abs_rel = [1]

    nobility = sum(1 for a in abs_rel if a == 1) / len(abs_rel)
    period_mean = sum(abs_rel) / len(abs_rel)
    period_max = max(abs_rel)
    period_gmean = math.exp(sum(math.log(max(a, 1)) for a in abs_rel) / len(abs_rel))

    return {
        'nobility': nobility,
        'period_mean': period_mean,
        'period_max': period_max,
        'period_gmean': period_gmean,
        'period_length': len(period),
    }


# ═══════════════════════════════════════════════════════════════════
# 4. ALTERNATIVE APPROACH: Direct Complexity Measures
# ═══════════════════════════════════════════════════════════════════

def lempel_ziv_complexity(seq):
    """Lempel-Ziv complexity (number of distinct factors in LZ76 parsing)."""
    n = len(seq)
    if n == 0:
        return 0

    i = 0
    c = 1  # complexity count
    l = 1  # current length
    k = 1  # position
    k_max = 1

    while True:
        if seq[i + k - 1] == seq[l + k - 1] if l + k - 1 < n else False:
            k += 1
            if l + k - 1 >= n:
                c += 1
                break
        else:
            if k > k_max:
                k_max = k
            i += 1
            if i == l:
                c += 1
                l += k_max
                if l >= n:
                    break
                i = 0
                k = 1
                k_max = 1
            else:
                k = 1

    return c


def block_entropy(seq, block_size=2):
    """Shannon entropy of blocks of given size."""
    n = len(seq)
    if n < block_size:
        return 0

    blocks = [seq[i:i+block_size] for i in range(n - block_size + 1)]
    counts = Counter(blocks)
    total = len(blocks)
    return -sum((c/total) * math.log(c/total) for c in counts.values())


# ═══════════════════════════════════════════════════════════════════
# 5. MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("HRISTOV STABILITY TEST: Nobility vs Dynamical Lyapunov Exponents")
    print("=" * 70)
    print(f"Data: 4,860 free-fall orbits from Hristov et al. (arXiv:2503.00432)")
    print(f"Source: https://db2.fmi.uni-sofia.bg/3bodysym4860/")
    print()

    # Load data
    print("Loading data...")
    syz_path = os.path.join(DATA_DIR, "syzygies.txt")
    exp_path = os.path.join(DATA_DIR, "res_exponents.txt")
    eigen_path = os.path.join(DATA_DIR, "res_eigen.txt")

    syzygies = load_syzygies(syz_path)
    exponents = load_exponents(exp_path)

    print(f"  Loaded {len(syzygies)} syzygy sequences")
    print(f"  Loaded {len(exponents)} Lyapunov exponents")

    assert len(syzygies) == len(exponents) == 4860, \
        f"Data count mismatch: {len(syzygies)} syz, {len(exponents)} exp"

    # Compute measures for each orbit
    print("\nComputing measures for all 4,860 orbits...")

    results = []
    n_cf_success = 0
    n_cf_fail = 0

    for i in range(4860):
        seq = syzygies[i]['sequence']
        lyap = exponents[i]['log_mu_max']
        mu_max = exponents[i]['mu_max']

        # Direct syzygy measures
        sm = syzygy_measures(seq)

        # Braid/CF measures (may fail for some orbits)
        braid_word = syzygy_to_braid_word(seq)
        cf_data = None
        cf_meas = None

        if braid_word:
            M = word_to_matrix(braid_word)
            tr = matrix_trace(M)
            det_val = matrix_det(M)
            abs_tr = abs(tr)

            if abs_tr > 2:  # hyperbolic
                cf_data = exact_cf(M)
                cf_meas = cf_nobility(cf_data)
                if cf_meas:
                    n_cf_success += 1
                else:
                    n_cf_fail += 1
            else:
                n_cf_fail += 1
        else:
            n_cf_fail += 1
            tr = 0
            abs_tr = 0

        row = {
            'index': i + 1,
            'syzygy': seq,
            'syzygy_length': len(seq),
            'lyap': lyap,
            'log_mu_max': lyap,
            'mu_max': mu_max,
            'braid_word': braid_word,
            'braid_word_length': len(braid_word) if braid_word else 0,
            **sm,
        }

        if braid_word:
            row['matrix_trace'] = tr
            row['abs_trace'] = abs_tr
            row['log_trace'] = math.log(abs_tr) if abs_tr > 0 else 0

        if cf_meas:
            row.update({f'cf_{k}': v for k, v in cf_meas.items()})

        results.append(row)

    print(f"  CF computation: {n_cf_success} succeeded, {n_cf_fail} failed")

    # ── Extract arrays for correlation analysis ──
    lyap_arr = np.array([r['lyap'] for r in results])
    syz_len = np.array([r['syzygy_length'] for r in results])

    # Syzygy-based measures
    stutter_frac = np.array([r.get('stutter_frac', np.nan) for r in results])
    freq_entropy = np.array([r.get('freq_entropy', np.nan) for r in results])
    trans_entropy = np.array([r.get('trans_entropy', np.nan) for r in results])
    reduction_ratio = np.array([r.get('reduction_ratio', np.nan) for r in results])
    ngram2 = np.array([r.get('ngram_2_complexity', np.nan) for r in results])
    ngram3 = np.array([r.get('ngram_3_complexity', np.nan) for r in results])
    num_runs = np.array([r.get('num_runs', np.nan) for r in results])
    mean_run = np.array([r.get('mean_run_length', np.nan) for r in results])
    freq_balance = np.array([r.get('freq_balance', np.nan) for r in results])

    # CF-based measures (where available)
    has_cf = np.array([1 if 'cf_nobility' in r else 0 for r in results], dtype=bool)
    cf_nobility_arr = np.array([r.get('cf_nobility', np.nan) for r in results])
    cf_gmean_arr = np.array([r.get('cf_period_gmean', np.nan) for r in results])
    cf_period_len = np.array([r.get('cf_period_length', np.nan) for r in results])
    cf_period_mean = np.array([r.get('cf_period_mean', np.nan) for r in results])
    cf_period_max = np.array([r.get('cf_period_max', np.nan) for r in results])

    # Matrix trace (where available)
    log_trace_arr = np.array([r.get('log_trace', np.nan) for r in results])
    has_trace = np.array([1 if 'log_trace' in r and r.get('log_trace', 0) > 0 else 0
                          for r in results], dtype=bool)

    # ── CORRELATION ANALYSIS ──
    print("\n" + "=" * 70)
    print("CORRELATION RESULTS: Measure vs Lyapunov Exponent log(|mu_max|)")
    print("=" * 70)

    all_correlations = []

    def report_corr(name, x, y, mask=None):
        if mask is None:
            mask = np.isfinite(x) & np.isfinite(y)
        else:
            mask = mask & np.isfinite(x) & np.isfinite(y)
        n = mask.sum()
        if n < 10:
            print(f"  {name:40s}: SKIP (n={n})")
            return None
        rho, p = stats.spearmanr(x[mask], y[mask])
        r_pearson, p_pearson = stats.pearsonr(x[mask], y[mask])
        sig = "***" if p < 1e-10 else "**" if p < 1e-5 else "*" if p < 0.05 else "ns"
        print(f"  {name:40s}: rho={rho:+.4f} (p={p:.2e}) r={r_pearson:+.4f} n={n} {sig}")
        all_correlations.append({
            'name': name,
            'rho_spearman': rho,
            'p_spearman': p,
            'r_pearson': r_pearson,
            'p_pearson': p_pearson,
            'n': n,
        })
        return rho

    # ── A. BASELINE: Trivial correlations ──
    print("\n--- A. BASELINES (trivial/expected) ---")
    report_corr("syzygy_length vs lyap", syz_len, lyap_arr)
    report_corr("braid_word_length vs lyap",
                np.array([r.get('braid_word_length', np.nan) for r in results]), lyap_arr)

    # ── B. SYZYGY SEQUENCE MEASURES ──
    print("\n--- B. SYZYGY SEQUENCE MEASURES vs lyap ---")
    report_corr("stutter_fraction vs lyap", stutter_frac, lyap_arr)
    report_corr("freq_entropy vs lyap", freq_entropy, lyap_arr)
    report_corr("transition_entropy vs lyap", trans_entropy, lyap_arr)
    report_corr("reduction_ratio vs lyap", reduction_ratio, lyap_arr)
    report_corr("2gram_complexity vs lyap", ngram2, lyap_arr)
    report_corr("3gram_complexity vs lyap", ngram3, lyap_arr)
    report_corr("num_runs vs lyap", num_runs, lyap_arr)
    report_corr("mean_run_length vs lyap", mean_run, lyap_arr)
    report_corr("freq_balance vs lyap", freq_balance, lyap_arr)

    # ── C. LYAPUNOV PER STEP (normalized) ──
    print("\n--- C. NORMALIZED LYAPUNOV (per syzygy step) ---")
    lyap_per_step = lyap_arr / syz_len
    report_corr("stutter_frac vs lyap/step", stutter_frac, lyap_per_step)
    report_corr("freq_entropy vs lyap/step", freq_entropy, lyap_per_step)
    report_corr("trans_entropy vs lyap/step", trans_entropy, lyap_per_step)
    report_corr("reduction_ratio vs lyap/step", reduction_ratio, lyap_per_step)
    report_corr("freq_balance vs lyap/step", freq_balance, lyap_per_step)

    # ── D. CF-BASED MEASURES (where available) ──
    print(f"\n--- D. CF-BASED MEASURES vs lyap (n={has_cf.sum()}) ---")
    report_corr("cf_nobility vs lyap", cf_nobility_arr, lyap_arr, has_cf)
    report_corr("cf_period_gmean vs lyap", cf_gmean_arr, lyap_arr, has_cf)
    report_corr("cf_period_length vs lyap", cf_period_len, lyap_arr, has_cf)
    report_corr("cf_period_mean vs lyap", cf_period_mean, lyap_arr, has_cf)
    report_corr("cf_period_max vs lyap", cf_period_max, lyap_arr, has_cf)

    # ── E. MATRIX TRACE vs LYAPUNOV (algebraic check) ──
    print(f"\n--- E. MATRIX TRACE vs lyap (n={has_trace.sum()}) ---")
    report_corr("log_trace vs lyap", log_trace_arr, lyap_arr, has_trace)

    # ── F. PARTIAL CORRELATIONS (controlling for length) ──
    print("\n--- F. PARTIAL CORRELATIONS (controlling syzygy length) ---")

    def partial_corr(name, x, y, z, mask=None):
        """Spearman partial correlation of x,y controlling for z."""
        if mask is None:
            mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
        else:
            mask = mask & np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
        n = mask.sum()
        if n < 20:
            print(f"  {name:40s}: SKIP (n={n})")
            return None

        # Residualize x and y on z
        from numpy.polynomial.polynomial import polyfit
        cx = np.polyfit(z[mask], x[mask], 1)
        cy = np.polyfit(z[mask], y[mask], 1)
        x_resid = x[mask] - np.polyval(cx, z[mask])
        y_resid = y[mask] - np.polyval(cy, z[mask])

        rho, p = stats.spearmanr(x_resid, y_resid)
        sig = "***" if p < 1e-10 else "**" if p < 1e-5 else "*" if p < 0.05 else "ns"
        print(f"  {name:40s}: rho={rho:+.4f} (p={p:.2e}) n={n} {sig}")
        all_correlations.append({
            'name': f'PARTIAL_{name}',
            'rho_spearman': rho,
            'p_spearman': p,
            'n': n,
        })
        return rho

    partial_corr("stutter_frac vs lyap | length", stutter_frac, lyap_arr, syz_len.astype(float))
    partial_corr("freq_entropy vs lyap | length", freq_entropy, lyap_arr, syz_len.astype(float))
    partial_corr("trans_entropy vs lyap | length", trans_entropy, lyap_arr, syz_len.astype(float))
    partial_corr("reduction_ratio vs lyap | length", reduction_ratio, lyap_arr, syz_len.astype(float))
    partial_corr("freq_balance vs lyap | length", freq_balance, lyap_arr, syz_len.astype(float))

    if has_cf.sum() > 20:
        partial_corr("cf_nobility vs lyap | length", cf_nobility_arr, lyap_arr,
                     syz_len.astype(float), has_cf)
        partial_corr("cf_period_gmean vs lyap | length", cf_gmean_arr, lyap_arr,
                     syz_len.astype(float), has_cf)

    # ── G. STABILITY TYPE ANALYSIS ──
    print("\n--- G. STABILITY TYPE BREAKDOWN ---")
    # From the paper: 4 loxodromic, 198 hyperbolic-elliptic, rest hyperbolic-hyperbolic
    # All unstable, but DEGREE of instability varies enormously
    lyap_sorted = np.sort(lyap_arr)
    print(f"  Lyapunov exponent range: [{lyap_sorted[0]:.2f}, {lyap_sorted[-1]:.2f}]")
    print(f"  Median: {np.median(lyap_arr):.2f}")
    print(f"  Mean: {np.mean(lyap_arr):.2f}")
    print(f"  Std: {np.std(lyap_arr):.2f}")

    # Quartile analysis
    q25, q50, q75 = np.percentile(lyap_arr, [25, 50, 75])
    print(f"  Q25={q25:.2f}, Q50={q50:.2f}, Q75={q75:.2f}")

    # ── H. VERDICT ──
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Find the best non-trivial correlation
    non_trivial = [c for c in all_correlations
                   if 'length' not in c['name'].lower() or 'PARTIAL' in c['name']]
    if non_trivial:
        best = max(non_trivial, key=lambda c: abs(c.get('rho_spearman', 0)))
        print(f"\n  Best non-trivial correlation:")
        print(f"    {best['name']}: rho = {best['rho_spearman']:+.4f} (n={best['n']})")

        rho_best = abs(best['rho_spearman'])
        if rho_best >= 0.5:
            verdict = "STRONG: Nobility-type measures predict dynamical stability. Circularity DEAD."
        elif rho_best >= 0.3:
            verdict = "MODERATE: Some predictive power beyond circularity. Promising but not conclusive."
        elif rho_best >= 0.15:
            verdict = "WEAK: Marginal signal. Circularity objection stands but weakened."
        else:
            verdict = "NULL: No meaningful prediction. Circularity objection confirmed."

        print(f"\n  VERDICT: {verdict}")

    # ── Save full results ──
    print("\n\nSaving results...")

    # Save correlation table
    corr_path = os.path.join(OUTPUT_DIR, "hristov_correlations.csv")
    with open(corr_path, 'w') as f:
        f.write("measure,rho_spearman,p_spearman,r_pearson,p_pearson,n\n")
        for c in all_correlations:
            f.write(f"{c['name']},{c['rho_spearman']:.6f},{c['p_spearman']:.2e},"
                    f"{c.get('r_pearson', '')},{c.get('p_pearson', '')},{c['n']}\n")
    print(f"  Correlations saved to {corr_path}")

    # Return results for report generation
    return results, all_correlations, {
        'lyap_min': float(lyap_sorted[0]),
        'lyap_max': float(lyap_sorted[-1]),
        'lyap_median': float(np.median(lyap_arr)),
        'lyap_mean': float(np.mean(lyap_arr)),
        'n_cf_success': n_cf_success,
        'n_cf_fail': n_cf_fail,
    }


if __name__ == '__main__':
    results, correlations, summary = main()
