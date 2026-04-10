#!/usr/bin/env python3
"""
Convert Hristov et al. three-body orbit syzygies to free-group words in F_2.

KEY INSIGHT: All 4860 Hristov syzygies are palindromes (time-reversal symmetric
Euler-configuration orbits). The full-period braid word freely reduces to the
identity (w * w^{-1} = e). The meaningful topological content is in the
HALF-PERIOD word: the first half of the syzygy.

We extract three types of free-group data:
  1. Half-period word: first half of syzygy -> F_2 word -> Gamma(2) matrix
  2. Raw (unreduced) word statistics: letter frequencies, entropy
  3. Conjugacy-class invariants: trace, spectral radius

The syzygy sequence encodes which pair of bodies is closest:
  1 = pair {2,3}, 2 = pair {1,3}, 3 = pair {1,2}

Transition -> generator mapping:
  1->2: a (sigma_1)     2->1: A (sigma_1^{-1})
  2->3: b (sigma_2)     3->2: B (sigma_2^{-1})
  1->3: B               3->1: b

Generator embedding F_2 -> Gamma(2) < SL(2,Z):
  a -> [[1, 2], [0, 1]]   (T^2)
  b -> [[1, 0], [2, 1]]   (ST^2S^{-1})
"""

import numpy as np
from collections import Counter
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path.home() / "Desktop/Farey-Local/experiments/hristov_data"
OUT_DIR = Path.home() / "Desktop/Farey-Local/experiments"

# Generator matrices for Gamma(2)
GENERATORS = {
    'a': np.array([[1, 2], [0, 1]], dtype=np.int64),
    'A': np.array([[1, -2], [0, 1]], dtype=np.int64),
    'b': np.array([[1, 0], [2, 1]], dtype=np.int64),
    'B': np.array([[1, 0], [-2, 1]], dtype=np.int64),
}

TRANSITION_MAP = {
    ('1', '2'): 'a', ('2', '1'): 'A',
    ('2', '3'): 'b', ('3', '2'): 'B',
    ('1', '3'): 'B', ('3', '1'): 'b',
}


def load_syzygies(path):
    """Load syzygy data: list of (syzygy_string, half_length, topo_class)."""
    orbits = []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                orbits.append((parts[0], int(parts[1]), int(parts[2])))
    return orbits


def load_exponents(path):
    """Load Lyapunov exponents: list of (eigenvalue, exponent)."""
    exponents = []
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                exponents.append((float(parts[1]), float(parts[2])))
    return exponents


def syzygy_to_word(syz_string):
    """Convert syzygy string to free-group word (unreduced)."""
    word = []
    for i in range(len(syz_string) - 1):
        if syz_string[i] != syz_string[i + 1]:
            letter = TRANSITION_MAP.get((syz_string[i], syz_string[i + 1]))
            if letter:
                word.append(letter)
    return ''.join(word)


def reduce_word(word):
    """Freely reduce: cancel adjacent inverse pairs."""
    inverse = {'a': 'A', 'A': 'a', 'b': 'B', 'B': 'b'}
    stack = []
    for letter in word:
        if stack and stack[-1] == inverse.get(letter):
            stack.pop()
        else:
            stack.append(letter)
    return ''.join(stack)


def word_to_matrix(word):
    """Map free-group word to Gamma(2) matrix in SL(2,Z).
    Uses pure Python ints for arbitrary precision (avoids int64 overflow)."""
    # Pure Python arbitrary-precision integer arithmetic
    GENS_PY = {
        'a': ((1, 2), (0, 1)),
        'A': ((1, -2), (0, 1)),
        'b': ((1, 0), (2, 1)),
        'B': ((1, 0), (-2, 1)),
    }
    a, b, c, d = 1, 0, 0, 1  # Identity matrix [[a,b],[c,d]]
    for letter in word:
        g = GENS_PY[letter]
        ga, gb, gc, gd = g[0][0], g[0][1], g[1][0], g[1][1]
        a, b, c, d = (a*ga + b*gc, a*gb + b*gd,
                      c*ga + d*gc, c*gb + d*gd)
    return (a, b, c, d)  # Return as tuple of Python ints


def word_entropy(word):
    """Shannon entropy of letter distribution in the word."""
    if not word:
        return 0.0
    counts = Counter(word)
    total = len(word)
    return -sum((c / total) * np.log2(c / total) for c in counts.values())


def cf_period_and_nobility(matrix):
    """
    Compute CF period and nobility from Gamma(2) matrix.
    matrix = (a, b, c, d) as Python ints.
    Returns (period, nobility) or (None, None) if degenerate.
    """
    a, b_val, c, d = matrix
    trace = a + d

    if c == 0 or abs(trace) <= 2:
        return None, None

    disc = trace * trace - 4
    if disc <= 0:
        return None, None

    # Fixed point of Mobius transformation
    sqrt_disc = np.sqrt(float(disc))
    x = ((a - d) + sqrt_disc) / (2.0 * c)
    if x < 0:
        x = -x

    # Compute CF expansion
    coeffs = []
    val = abs(float(x))
    for i in range(100):
        a_i = int(np.floor(val))
        coeffs.append(a_i)
        frac = val - a_i
        if frac < 1e-12:
            return None, None  # rational
        val = 1.0 / frac

    # Detect period by checking repeating patterns in the tail
    # (Skip first few coefficients which may be non-periodic)
    if len(coeffs) < 10:
        return None, None

    for period in range(1, min(30, len(coeffs) // 3)):
        # Check if coefficients repeat with this period starting from position 1
        found = False
        for start in range(1, min(5, len(coeffs) - 3 * period)):
            seg1 = coeffs[start:start + period]
            matches = 0
            for k in range(1, min(5, (len(coeffs) - start) // period)):
                seg_k = coeffs[start + k * period:start + (k + 1) * period]
                if seg_k == seg1:
                    matches += 1
                else:
                    break
            if matches >= 2:  # At least 3 repetitions
                return period, 1.0 / period
    return None, None


def analyze_orbit(syz, half_len, topo_class, lyap):
    """Full analysis of one orbit."""
    # Verify palindrome
    is_palindrome = (syz == syz[::-1])

    # Half-period: first half of the syzygy
    mid = len(syz) // 2
    half_syz = syz[:mid + 1]  # include middle character

    # Full word (should reduce to identity for palindromes)
    full_raw = syzygy_to_word(syz)
    full_reduced = reduce_word(full_raw)

    # Half-period word
    half_raw = syzygy_to_word(half_syz)
    half_reduced = reduce_word(half_raw)

    # Half-period matrix (a, b, c, d) as Python ints
    half_matrix = word_to_matrix(half_reduced)
    ma, mb, mc, md = half_matrix
    half_trace = abs(ma + md)
    half_det = ma * md - mb * mc

    # Spectral radius from trace (for SL(2,Z), eigenvalues are (tr +/- sqrt(tr^2-4))/2)
    tr = ma + md
    disc = tr * tr - 4
    if disc > 0:
        import math
        sqrt_disc = math.sqrt(float(disc))
        lam = (abs(tr) + sqrt_disc) / 2.0
        log_spec = math.log(lam) if lam > 0 else 0.0
    else:
        log_spec = 0.0

    # CF nobility
    cf_per, cf_nob = cf_period_and_nobility(half_matrix)

    # Word statistics on the raw (unreduced) full word
    raw_entropy = word_entropy(full_raw)

    # Letter counts in half word
    half_counts = Counter(half_reduced)

    # Abelianization: net exponents of a and b
    abel_a = half_counts.get('a', 0) - half_counts.get('A', 0)
    abel_b = half_counts.get('b', 0) - half_counts.get('B', 0)

    return {
        'syz': syz,
        'syz_len': len(syz),
        'half_len_file': half_len,
        'topo_class': topo_class,
        'is_palindrome': is_palindrome,
        'full_raw_len': len(full_raw),
        'full_reduced_len': len(full_reduced),
        'half_raw': half_raw,
        'half_reduced': half_reduced,
        'half_raw_len': len(half_raw),
        'half_reduced_len': len(half_reduced),
        'half_matrix': half_matrix,
        'half_trace': half_trace,
        'half_det': half_det,
        'log_spectral_radius': log_spec,
        'cf_period': cf_per,
        'cf_nobility': cf_nob,
        'raw_entropy': raw_entropy,
        'abel_a': abel_a,
        'abel_b': abel_b,
        'lyapunov': lyap,
    }


def main():
    print("=" * 72)
    print("HRISTOV THREE-BODY ORBITS: SYZYGY -> FREE-GROUP WORD CONVERSION")
    print("=" * 72)

    syz_data = load_syzygies(DATA_DIR / "syzygies.txt")
    exp_data = load_exponents(DATA_DIR / "res_exponents.txt")
    print(f"\nLoaded {len(syz_data)} orbits, {len(exp_data)} exponents")

    # --- Step 1: Verify palindrome structure ---
    print("\n" + "=" * 50)
    print("STEP 1: Palindrome verification")
    print("=" * 50)
    pal_count = sum(1 for s, _, _ in syz_data if s == s[::-1])
    print(f"  Palindromic syzygies: {pal_count} / {len(syz_data)} "
          f"({100*pal_count/len(syz_data):.1f}%)")

    # --- Step 2: Transition statistics ---
    print("\n" + "=" * 50)
    print("STEP 2: Transition analysis (first 100 orbits)")
    print("=" * 50)
    all_trans = Counter()
    for syz, _, _ in syz_data[:100]:
        for i in range(len(syz) - 1):
            if syz[i] != syz[i + 1]:
                all_trans[(syz[i], syz[i + 1])] += 1
    for (a, b), c in sorted(all_trans.items()):
        print(f"  {a} -> {b}: {c:5d}  [{TRANSITION_MAP.get((a, b), '?')}]")

    # --- Step 3: Convert all orbits ---
    print("\n" + "=" * 50)
    print("STEP 3: Half-period word conversion")
    print("=" * 50)

    results = []
    errors = 0
    for idx, (syz, half_len, topo_class) in enumerate(syz_data):
        lyap = exp_data[idx][1] if idx < len(exp_data) else None
        try:
            r = analyze_orbit(syz, half_len, topo_class, lyap)
            r['idx'] = idx + 1
            results.append(r)
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  Error on orbit {idx + 1}: {e}")

    print(f"  Converted: {len(results)} / {len(syz_data)}, errors: {errors}")

    # Show examples
    print("\n  First 15 half-period words:")
    print(f"  {'#':>4} {'Half-word (reduced)':>35} {'len':>5} {'|Tr|':>8} {'det':>4} "
          f"{'log(rho)':>10} {'CF_per':>6} {'Lyap':>8}")
    for r in results[:15]:
        w = r['half_reduced']
        w_short = w[:30] + ('...' if len(w) > 30 else '')
        cf_str = str(r['cf_period']) if r['cf_period'] else '-'
        print(f"  {r['idx']:4d} {w_short:>35} {r['half_reduced_len']:5d} "
              f"{r['half_trace']:8d} {r['half_det']:4d} "
              f"{r['log_spectral_radius']:10.4f} {cf_str:>6} "
              f"{r['lyapunov']:8.2f}")

    # --- Step 4: Matrix verification ---
    print("\n" + "=" * 50)
    print("STEP 4: Matrix verification (half-period)")
    print("=" * 50)
    det_counts = Counter(r['half_det'] for r in results)
    print(f"  Determinant distribution: {dict(det_counts)}")

    gamma2 = sum(1 for r in results
                 if r['half_matrix'][0] % 2 == 1 and r['half_matrix'][3] % 2 == 1
                 and r['half_matrix'][1] % 2 == 0 and r['half_matrix'][2] % 2 == 0)
    print(f"  In Gamma(2): {gamma2} / {len(results)}")

    nontrivial = [r for r in results if r['half_reduced_len'] > 0]
    trivial = [r for r in results if r['half_reduced_len'] == 0]
    print(f"  Nontrivial half-words: {len(nontrivial)}")
    print(f"  Trivial half-words (identity): {len(trivial)}")

    hyperbolic = [r for r in results if r['half_trace'] > 2]
    parabolic = [r for r in results if r['half_trace'] == 2 and r['half_reduced_len'] > 0]
    elliptic = [r for r in results if r['half_trace'] < 2]
    identity = [r for r in results if r['half_trace'] == 2 and r['half_reduced_len'] == 0]
    print(f"  Hyperbolic (|tr|>2): {len(hyperbolic)}")
    print(f"  Parabolic  (|tr|=2, w!=e): {len(parabolic)}")
    print(f"  Identity   (|tr|=2, w=e): {len(identity)}")

    # --- Step 5: Correlations ---
    print("\n" + "=" * 50)
    print("STEP 5: Correlation analysis")
    print("=" * 50)

    # Multiple measures to correlate with Lyapunov
    valid_hyp = [r for r in results if r['log_spectral_radius'] > 1e-10 and r['lyapunov'] is not None]
    valid_all = [r for r in results if r['lyapunov'] is not None]

    print(f"\n  A) Hyperbolic orbits only (n={len(valid_hyp)}):")
    if len(valid_hyp) > 10:
        lyap = np.array([r['lyapunov'] for r in valid_hyp])
        log_rho = np.array([r['log_spectral_radius'] for r in valid_hyp])
        wlen = np.array([r['half_reduced_len'] for r in valid_hyp], dtype=float)
        trace = np.array([r['half_trace'] for r in valid_hyp], dtype=float)

        r1, p1 = stats.pearsonr(log_rho, lyap)
        r2, p2 = stats.pearsonr(wlen, lyap)
        r3, p3 = stats.pearsonr(np.log(trace), lyap)
        r4, p4 = stats.pearsonr(log_rho / np.maximum(wlen, 1), lyap)

        print(f"    Corr(log(rho), Lyap)     = {r1:+.4f}  p={p1:.2e}")
        print(f"    Corr(word_len, Lyap)     = {r2:+.4f}  p={p2:.2e}")
        print(f"    Corr(log(|tr|), Lyap)    = {r3:+.4f}  p={p3:.2e}")
        print(f"    Corr(log(rho)/len, Lyap) = {r4:+.4f}  p={p4:.2e}")

        # CF nobility
        cf_valid = [r for r in valid_hyp if r['cf_nobility'] is not None]
        if len(cf_valid) > 10:
            cf = np.array([r['cf_nobility'] for r in cf_valid])
            lyap_cf = np.array([r['lyapunov'] for r in cf_valid])
            r5, p5 = stats.pearsonr(cf, lyap_cf)
            print(f"    Corr(CF_nobility, Lyap)  = {r5:+.4f}  p={p5:.2e} (n={len(cf_valid)})")

    print(f"\n  B) All orbits (n={len(valid_all)}):")
    if len(valid_all) > 10:
        lyap_all = np.array([r['lyapunov'] for r in valid_all])
        hlen_all = np.array([r['half_reduced_len'] for r in valid_all], dtype=float)
        hraw_all = np.array([r['half_raw_len'] for r in valid_all], dtype=float)
        ent_all = np.array([r['raw_entropy'] for r in valid_all])
        syz_len_all = np.array([r['syz_len'] for r in valid_all], dtype=float)
        abel_a_all = np.array([r['abel_a'] for r in valid_all], dtype=float)
        abel_b_all = np.array([r['abel_b'] for r in valid_all], dtype=float)

        for name, arr in [
            ("half_reduced_len", hlen_all),
            ("half_raw_len", hraw_all),
            ("syzygy_length", syz_len_all),
            ("raw_word_entropy", ent_all),
            ("|abel_a|", np.abs(abel_a_all)),
            ("|abel_b|", np.abs(abel_b_all)),
            ("|abel_a|+|abel_b|", np.abs(abel_a_all) + np.abs(abel_b_all)),
        ]:
            r_val, p_val = stats.pearsonr(arr, lyap_all)
            print(f"    Corr({name:25s}, Lyap) = {r_val:+.4f}  p={p_val:.2e}")

    # --- Step 6: By topological class ---
    print("\n" + "=" * 50)
    print("STEP 6: Statistics by topological class")
    print("=" * 50)
    for tc in [1, 2, 3]:
        sub = [r for r in results if r['topo_class'] == tc]
        if sub:
            avg_hlen = np.mean([r['half_reduced_len'] for r in sub])
            avg_trace = np.mean([float(r['half_trace']) for r in sub])
            avg_lspec = np.mean([r['log_spectral_radius'] for r in sub])
            lyap_sub = [r['lyapunov'] for r in sub if r['lyapunov'] is not None]
            avg_lyap = np.mean(lyap_sub) if lyap_sub else float('nan')
            n_hyp = sum(1 for r in sub if r['half_trace'] > 2)
            print(f"  Class {tc}: n={len(sub):4d}, avg_half_word_len={avg_hlen:5.1f}, "
                  f"avg_|tr|={avg_trace:8.1f}, n_hyperbolic={n_hyp:4d}, "
                  f"avg_Lyap={avg_lyap:.2f}")

    # --- Step 7: Save results ---
    print("\n" + "=" * 50)
    print("STEP 7: Saving results")
    print("=" * 50)

    csv_path = OUT_DIR / "hristov_freegroup_results.csv"
    with open(csv_path, 'w') as f:
        f.write("orbit_idx,syz_len,topo_class,is_palindrome,"
                "half_raw_len,half_reduced_len,"
                "half_trace,half_det,log_spectral_radius,"
                "cf_period,cf_nobility,raw_entropy,"
                "abel_a,abel_b,lyapunov,half_reduced_word\n")
        for r in results:
            cf_per = str(r['cf_period']) if r['cf_period'] is not None else ""
            cf_nob = f"{r['cf_nobility']:.8f}" if r['cf_nobility'] is not None else ""
            lyap_str = f"{r['lyapunov']:.10f}" if r['lyapunov'] is not None else ""
            f.write(f"{r['idx']},{r['syz_len']},{r['topo_class']},{int(r['is_palindrome'])},"
                    f"{r['half_raw_len']},{r['half_reduced_len']},"
                    f"{r['half_trace']},{r['half_det']},{r['log_spectral_radius']:.10f},"
                    f"{cf_per},{cf_nob},{r['raw_entropy']:.6f},"
                    f"{r['abel_a']},{r['abel_b']},{lyap_str},"
                    f"{r['half_reduced']}\n")
    print(f"  CSV: {csv_path}")

    write_report(results)
    return results


def write_report(results):
    """Write HRISTOV_WORD_RESULTS.md."""
    report_path = OUT_DIR / "HRISTOV_WORD_RESULTS.md"

    # Precompute stats
    n = len(results)
    pal_count = sum(1 for r in results if r['is_palindrome'])
    n_hyp = sum(1 for r in results if r['half_trace'] > 2)
    n_trivial = sum(1 for r in results if r['half_reduced_len'] == 0)

    valid_hyp = [r for r in results if r['log_spectral_radius'] > 1e-10 and r['lyapunov'] is not None]
    valid_all = [r for r in results if r['lyapunov'] is not None]

    with open(report_path, 'w') as f:
        f.write("# Hristov Three-Body Orbits: Free-Group Word Analysis\n\n")

        f.write("## Method\n\n")
        f.write("1. **All 4860 Hristov syzygies are palindromes** (time-reversal symmetric "
                "Euler-configuration orbits).\n")
        f.write("2. The full-period braid word freely reduces to the identity "
                "(w * w^{-1} = e) for every orbit.\n")
        f.write("3. **Solution:** Use the **half-period word** (first half of syzygy) as the "
                "topologically meaningful free-group element.\n")
        f.write("4. Map half-period words to Gamma(2) matrices via the standard embedding "
                "a -> [[1,2],[0,1]], b -> [[1,0],[2,1]].\n\n")

        f.write("## Transition Mapping\n\n")
        f.write("| Transition | Generator | Interpretation |\n")
        f.write("|:----------:|:---------:|:---------------|\n")
        f.write("| 1 -> 2 | a | sigma_1 (forward) |\n")
        f.write("| 2 -> 1 | A = a^{-1} | sigma_1^{-1} (backward) |\n")
        f.write("| 2 -> 3 | b | sigma_2 (forward) |\n")
        f.write("| 3 -> 2 | B = b^{-1} | sigma_2^{-1} (backward) |\n")
        f.write("| 1 -> 3 | B | skip backward |\n")
        f.write("| 3 -> 1 | b | skip forward |\n\n")

        f.write("## Key Findings\n\n")
        f.write(f"- **Orbits processed:** {n}\n")
        f.write(f"- **Palindromic:** {pal_count}/{n} ({100*pal_count/n:.1f}%)\n")
        f.write(f"- **Nontrivial half-words:** {n - n_trivial}/{n}\n")
        f.write(f"- **Hyperbolic (|trace| > 2):** {n_hyp}/{n} ({100*n_hyp/n:.1f}%)\n")
        f.write(f"- **Trivial half-words:** {n_trivial}/{n}\n\n")

        # Correlations
        f.write("## Correlations with Lyapunov Exponents\n\n")

        if len(valid_hyp) > 10:
            lyap = np.array([r['lyapunov'] for r in valid_hyp])
            log_rho = np.array([r['log_spectral_radius'] for r in valid_hyp])
            wlen = np.array([r['half_reduced_len'] for r in valid_hyp], dtype=float)
            trace = np.array([r['half_trace'] for r in valid_hyp], dtype=float)

            f.write(f"### Hyperbolic orbits (n={len(valid_hyp)})\n\n")
            f.write("| Quantity | Pearson r | p-value |\n")
            f.write("|:---------|:---------:|:-------:|\n")
            for name, arr in [
                ("log(spectral_radius)", log_rho),
                ("half_word_length", wlen),
                ("log(|trace|)", np.log(trace)),
                ("log(rho)/word_len", log_rho / np.maximum(wlen, 1)),
            ]:
                r_val, p_val = stats.pearsonr(arr, lyap)
                f.write(f"| {name} | {r_val:+.4f} | {p_val:.2e} |\n")
            f.write("\n")

        if len(valid_all) > 10:
            lyap_all = np.array([r['lyapunov'] for r in valid_all])

            f.write(f"### All orbits (n={len(valid_all)})\n\n")
            f.write("| Quantity | Pearson r | p-value |\n")
            f.write("|:---------|:---------:|:-------:|\n")
            for name, key_or_fn in [
                ("half_reduced_len", lambda r: r['half_reduced_len']),
                ("half_raw_len", lambda r: r['half_raw_len']),
                ("syzygy_length", lambda r: r['syz_len']),
                ("raw_word_entropy", lambda r: r['raw_entropy']),
                ("|abel_a| + |abel_b|", lambda r: abs(r['abel_a']) + abs(r['abel_b'])),
            ]:
                arr = np.array([key_or_fn(r) for r in valid_all], dtype=float)
                r_val, p_val = stats.pearsonr(arr, lyap_all)
                f.write(f"| {name} | {r_val:+.4f} | {p_val:.2e} |\n")
            f.write("\n")

        # By class
        f.write("## By Topological Class\n\n")
        f.write("| Class | n | Avg half-word len | Avg |trace| | "
                "Hyperbolic | Avg Lyapunov |\n")
        f.write("|:-----:|:---:|:---------:|:----------:|:---------:|:----------:|\n")
        for tc in [1, 2, 3]:
            sub = [r for r in results if r['topo_class'] == tc]
            if sub:
                f.write(f"| {tc} | {len(sub)} | "
                        f"{np.mean([r['half_reduced_len'] for r in sub]):.1f} | "
                        f"{np.mean([float(r['half_trace']) for r in sub]):.1f} | "
                        f"{sum(1 for r in sub if r['half_trace'] > 2)} | "
                        f"{np.mean([r['lyapunov'] for r in sub if r['lyapunov']]):.2f} |\n")

        # Sample words
        f.write("\n## Sample Half-Period Free-Group Words (first 30)\n\n")
        f.write("| # | Class | Half-word | Len | |Trace| | log(rho) | Lyapunov |\n")
        f.write("|:-:|:-----:|:----------|:---:|:------:|:--------:|:--------:|\n")
        for r in results[:30]:
            w = r['half_reduced'][:35] + ('...' if len(r['half_reduced']) > 35 else '')
            f.write(f"| {r['idx']} | {r['topo_class']} | {w} | {r['half_reduced_len']} | "
                    f"{r['half_trace']} | {r['log_spectral_radius']:.3f} | "
                    f"{r['lyapunov']:.2f} |\n")

        f.write(f"\n## Data Files\n\n")
        f.write(f"- Full results: `hristov_freegroup_results.csv`\n")
        f.write(f"- This report: `HRISTOV_WORD_RESULTS.md`\n")

    print(f"  Report: {report_path}")


if __name__ == "__main__":
    results = main()
