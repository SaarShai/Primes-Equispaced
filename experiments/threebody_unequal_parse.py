#!/usr/bin/env python3
"""
Parse Li-Liao three-body unequal-mass free-group word data.
Compute Gamma(2) matrices, continued fractions, and nobility.
Test whether equal-mass results generalize to unequal masses.

Data source: https://github.com/sjtu-liao/three-body
"""

import re
import sys
import numpy as np
from fractions import Fraction
from collections import Counter, defaultdict

# ============================================================
# PART 1: Parse the HTML table of free-group words
# ============================================================

def parse_unequal_mass_words(filepath):
    """Parse the HTML table into (class, number, m3, word) tuples."""
    with open(filepath, 'r') as f:
        html = f.read()

    # Pattern: <th>CLASS_INFO (mass)</th> followed by <td>WORD</td>
    # The class info has HTML sub/sup tags
    rows = re.findall(
        r'<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>',
        html, re.DOTALL
    )

    results = []
    for class_info, word in rows:
        # Skip header row
        if 'Free group' in word or 'Class' in class_info:
            continue

        # Clean word (should be just letters)
        word = word.strip()
        if not word or not re.match(r'^[AaBb]+$', word):
            continue

        # Extract class name: strip HTML tags
        clean_class = re.sub(r'<[^>]+>', '', class_info)
        clean_class = clean_class.replace('&nbsp;', ' ').strip()

        # Extract mass ratio m3 from parentheses
        mass_match = re.search(r'\(([\d.]+)\)', clean_class)
        m3 = float(mass_match.group(1)) if mass_match else None

        # Extract class type (e.g., I.A, II.B, etc.) and number
        # Format: I.A^{i.c.}_N (m3)
        class_type_match = re.match(r'([IVX]+\.[A-Z])', clean_class)
        class_type = class_type_match.group(1) if class_type_match else clean_class.split()[0]

        # Extract orbit number
        num_match = re.search(r'(\d+)', clean_class)
        orbit_num = int(num_match.group(1)) if num_match else 0

        results.append({
            'class': class_type,
            'number': orbit_num,
            'm3': m3,
            'word': word,
            'word_len': len(word),
            'raw_class': clean_class
        })

    return results

def parse_equal_mass_words(filepath):
    """Parse the equal-mass HTML table."""
    with open(filepath, 'r') as f:
        html = f.read()

    rows = re.findall(
        r'<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>',
        html, re.DOTALL
    )

    results = []
    for class_info, word in rows:
        if 'Free group' in word or 'Class' in class_info:
            continue
        word = word.strip()
        if not word or not re.match(r'^[AaBb]+$', word):
            continue

        clean_class = re.sub(r'<[^>]+>', '', class_info)
        clean_class = clean_class.replace('&nbsp;', ' ').strip()

        class_type_match = re.match(r'([IVX]+\.[A-Z])', clean_class)
        class_type = class_type_match.group(1) if class_type_match else clean_class.split()[0]

        num_match = re.search(r'(\d+)', clean_class)
        orbit_num = int(num_match.group(1)) if num_match else 0

        results.append({
            'class': class_type,
            'number': orbit_num,
            'm3': 1.0,  # equal mass
            'word': word,
            'word_len': len(word),
            'raw_class': clean_class
        })

    return results


# ============================================================
# PART 2: Gamma(2) matrix computation from free-group words
# ============================================================

# Generators of Gamma(2) < PSL(2,Z):
# Standard choice: L = [[1,0],[2,1]], R = [[1,2],[0,1]]
# Map: A -> L, B -> R, a -> L^{-1}, b -> R^{-1}
# (This is one standard convention; the exact map depends on
#  how the free group of the 3-punctured sphere is presented)

L = np.array([[1, 0], [2, 1]], dtype=np.int64)
R = np.array([[1, 2], [0, 1]], dtype=np.int64)
L_inv = np.array([[1, 0], [-2, 1]], dtype=np.int64)
R_inv = np.array([[1, -2], [0, 1]], dtype=np.int64)

GENERATOR_MAP = {
    'A': L,
    'a': L_inv,
    'B': R,
    'b': R_inv,
}

def word_to_gamma2_matrix(word):
    """Convert a free-group word to its Gamma(2) matrix."""
    M = np.eye(2, dtype=np.int64)
    for letter in word:
        M = M @ GENERATOR_MAP[letter]
    return M

def matrix_to_cf(M):
    """
    Extract continued fraction from a Gamma(2) matrix.
    The matrix M = product of L^{a_i} R^{b_i} gives CF [a1; b1, a2, b2, ...].
    We decompose M back into L/R factors.
    """
    # For a 2x2 matrix [[a,b],[c,d]] in SL(2,Z),
    # we can extract the CF via the Euclidean algorithm on the entries.
    a, b = abs(M[0, 0]), abs(M[0, 1])
    c, d = abs(M[1, 0]), abs(M[1, 1])

    # Use ratio c/a (or d/b) to get the CF
    if a == 0:
        return []

    # CF of c/a
    cf = []
    num, den = c, a
    while den > 0:
        q, r = divmod(num, den)
        cf.append(int(q))
        num, den = den, r

    return cf

def cf_to_nobility(cf):
    """
    Compute the 'nobility' of a continued fraction.
    Nobility = how close to the golden ratio's CF [1;1,1,1,...].
    We use: fraction of CF coefficients that equal 1.
    """
    if not cf:
        return 0.0
    return sum(1 for x in cf if x == 1) / len(cf)

def is_palindrome(word):
    """Check if a word is a palindrome."""
    return word == word[::-1]

def is_reverse_complement(word):
    """
    Check if word is a 'reverse complement' palindrome.
    Swap A<->a, B<->b, then reverse.
    This is the symmetry of Hristov's equal-mass orbits.
    """
    complement = {'A': 'a', 'a': 'A', 'B': 'b', 'b': 'B'}
    rc = ''.join(complement[c] for c in reversed(word))
    return word == rc

def word_exponent_sequence(word):
    """
    Convert word to exponent sequence.
    E.g., BaBabAbA -> [(B,1),(a,1),(B,1),(a,1),(b,1),(A,1),(b,1),(A,1)]
    Compressed: group consecutive same letters.
    """
    if not word:
        return []
    groups = []
    current = word[0]
    count = 1
    for c in word[1:]:
        if c == current:
            count += 1
        else:
            groups.append((current, count))
            current = c
            count = 1
    groups.append((current, count))
    return groups

def braid_entropy_estimate(word):
    """
    Estimate topological entropy from word length and structure.
    For a periodic orbit with word w, the topological entropy is
    roughly log(spectral_radius(M)) / (word_length).
    """
    M = word_to_gamma2_matrix(word)
    # Spectral radius
    trace = abs(M[0,0] + M[1,1])
    if trace <= 2:
        return 0.0  # elliptic/parabolic
    # For hyperbolic: largest eigenvalue ~ (trace + sqrt(trace^2 - 4))/2
    sr = (trace + np.sqrt(trace**2 - 4)) / 2
    return np.log(sr) / len(word) if len(word) > 0 else 0.0


# ============================================================
# PART 3: Parse supplementary data (135K orbits)
# ============================================================

def parse_supplementary_data(filepath, max_rows=None):
    """Parse the non-hierarchical supplementary data file."""
    results = []
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            # Skip header lines
            if line.startswith(('The initial', 'r_1', 'r_3', '---', ' m_1')):
                continue
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            try:
                m1 = float(parts[0])
                m2 = float(parts[1])
                m3 = float(parts[2])
                x1 = float(parts[3])
                v1 = float(parts[4])
                v2 = float(parts[5])
                T = float(parts[6])
                stability = parts[7]
                results.append({
                    'm1': m1, 'm2': m2, 'm3': m3,
                    'x1': x1, 'v1': v1, 'v2': v2,
                    'T': T, 'stability': stability
                })
                if max_rows and len(results) >= max_rows:
                    break
            except (ValueError, IndexError):
                continue
    return results


# ============================================================
# PART 4: Analysis
# ============================================================

def analyze_words(orbits, label=""):
    """Run full analysis on a set of orbits with words."""
    print(f"\n{'='*70}")
    print(f"  ANALYSIS: {label}")
    print(f"  {len(orbits)} orbits")
    print(f"{'='*70}\n")

    # Basic stats
    mass_values = set(o['m3'] for o in orbits if o['m3'] is not None)
    print(f"Mass values (m3): {sorted(mass_values)}")
    print(f"Word lengths: min={min(o['word_len'] for o in orbits)}, "
          f"max={max(o['word_len'] for o in orbits)}, "
          f"mean={np.mean([o['word_len'] for o in orbits]):.1f}")

    # Compute Gamma(2) properties for each orbit
    palindrome_count = 0
    rc_palindrome_count = 0
    nobility_values = []
    entropy_values = []
    identity_count = 0

    class_stats = defaultdict(list)
    mass_stats = defaultdict(list)

    for o in orbits:
        word = o['word']
        M = word_to_gamma2_matrix(word)
        o['matrix'] = M
        o['trace'] = int(M[0,0] + M[1,1])

        # Check if matrix is identity (mod sign)
        is_id = np.array_equal(M, np.eye(2, dtype=np.int64)) or \
                np.array_equal(M, -np.eye(2, dtype=np.int64))
        o['is_identity'] = is_id
        if is_id:
            identity_count += 1

        # CF and nobility
        cf = matrix_to_cf(M)
        o['cf'] = cf
        nob = cf_to_nobility(cf)
        o['nobility'] = nob
        nobility_values.append(nob)

        # Entropy
        ent = braid_entropy_estimate(word)
        o['entropy'] = ent
        entropy_values.append(ent)

        # Palindrome checks
        if is_palindrome(word):
            palindrome_count += 1
            o['palindrome'] = True
        else:
            o['palindrome'] = False

        if is_reverse_complement(word):
            rc_palindrome_count += 1
            o['rc_palindrome'] = True
        else:
            o['rc_palindrome'] = False

        # Exponent sequence
        o['exponents'] = word_exponent_sequence(word)

        # Group by class and mass
        class_stats[o['class']].append(o)
        if o['m3'] is not None:
            mass_stats[o['m3']].append(o)

    print(f"\nGamma(2) MATRIX PROPERTIES:")
    print(f"  Identity matrices: {identity_count}/{len(orbits)} ({100*identity_count/len(orbits):.1f}%)")
    print(f"  Palindromes: {palindrome_count}/{len(orbits)} ({100*palindrome_count/len(orbits):.1f}%)")
    print(f"  Reverse-complement palindromes: {rc_palindrome_count}/{len(orbits)} ({100*rc_palindrome_count/len(orbits):.1f}%)")

    print(f"\nNOBILITY (fraction of CF coefficients = 1):")
    nv = np.array(nobility_values)
    print(f"  Mean: {nv.mean():.4f}")
    print(f"  Median: {np.median(nv):.4f}")
    print(f"  Std: {nv.std():.4f}")
    print(f"  Min/Max: {nv.min():.4f} / {nv.max():.4f}")

    print(f"\nBRAID ENTROPY (per letter):")
    ev = np.array(entropy_values)
    print(f"  Mean: {ev.mean():.4f}")
    print(f"  Median: {np.median(ev):.4f}")
    print(f"  Non-zero: {np.sum(ev > 0)}/{len(ev)}")

    # Nobility vs entropy correlation
    if len(nobility_values) > 5:
        mask = np.array(entropy_values) > 0
        if np.sum(mask) > 5:
            corr = np.corrcoef(np.array(nobility_values)[mask], np.array(entropy_values)[mask])[0, 1]
            print(f"\n  Nobility-Entropy correlation (non-trivial): {corr:.4f}")

    # Per-mass analysis
    if len(mass_stats) > 1:
        print(f"\nPER-MASS BREAKDOWN:")
        for m3 in sorted(mass_stats.keys()):
            orbs = mass_stats[m3]
            nobs = [o['nobility'] for o in orbs]
            pals = sum(1 for o in orbs if o['palindrome'])
            rcs = sum(1 for o in orbs if o['rc_palindrome'])
            ids = sum(1 for o in orbs if o['is_identity'])
            print(f"  m3={m3:6.2f}: {len(orbs):4d} orbits, "
                  f"nobility={np.mean(nobs):.3f}, "
                  f"palindrome={pals}, rc_palindrome={rcs}, identity={ids}")

    # Per-class analysis
    print(f"\nPER-CLASS BREAKDOWN:")
    for cls in sorted(class_stats.keys()):
        orbs = class_stats[cls]
        nobs = [o['nobility'] for o in orbs]
        print(f"  {cls:8s}: {len(orbs):4d} orbits, "
              f"nobility mean={np.mean(nobs):.3f}, "
              f"word_len mean={np.mean([o['word_len'] for o in orbs]):.1f}")

    # Show some example words and their matrices
    print(f"\nSAMPLE ORBITS (first 10):")
    for o in orbits[:10]:
        M = o['matrix']
        print(f"  {o['raw_class']:30s} word={o['word'][:40]:40s} "
              f"tr={o['trace']:6d} nob={o['nobility']:.3f} "
              f"pal={'Y' if o['palindrome'] else 'N'} "
              f"rc={'Y' if o['rc_palindrome'] else 'N'} "
              f"id={'Y' if o['is_identity'] else 'N'}")

    # KEY QUESTION: Are unequal-mass words palindromes?
    # In equal mass, Hristov showed they must be palindromic under
    # the exchange symmetry. With unequal masses, this symmetry breaks.

    return orbits, class_stats, mass_stats


def compare_equal_unequal(equal_orbits, unequal_orbits):
    """Compare properties of equal vs unequal mass orbits."""
    print(f"\n{'='*70}")
    print(f"  COMPARISON: Equal vs Unequal Mass")
    print(f"{'='*70}\n")

    def stats(orbs, label):
        nobs = [o['nobility'] for o in orbs]
        ents = [o['entropy'] for o in orbs]
        pals = sum(1 for o in orbs if o.get('palindrome', False))
        rcs = sum(1 for o in orbs if o.get('rc_palindrome', False))
        ids = sum(1 for o in orbs if o.get('is_identity', False))
        print(f"  {label}:")
        print(f"    Count: {len(orbs)}")
        print(f"    Nobility: {np.mean(nobs):.4f} +/- {np.std(nobs):.4f}")
        print(f"    Entropy:  {np.mean(ents):.4f} +/- {np.std(ents):.4f}")
        print(f"    Palindromes: {pals}/{len(orbs)} ({100*pals/len(orbs):.1f}%)")
        print(f"    RC palindromes: {rcs}/{len(orbs)} ({100*rcs/len(orbs):.1f}%)")
        print(f"    Identity matrices: {ids}/{len(orbs)} ({100*ids/len(orbs):.1f}%)")

    stats(equal_orbits, "Equal mass (m1=m2=m3=1)")
    stats(unequal_orbits, "Unequal mass (m1=m2=1, m3 varies)")

    # Shared class types
    eq_classes = set(o['class'] for o in equal_orbits)
    uneq_classes = set(o['class'] for o in unequal_orbits)
    print(f"\n  Class overlap:")
    print(f"    Equal-only: {eq_classes - uneq_classes}")
    print(f"    Unequal-only: {uneq_classes - eq_classes}")
    print(f"    Shared: {eq_classes & uneq_classes}")

    # Word length distribution comparison
    eq_lens = [o['word_len'] for o in equal_orbits]
    uneq_lens = [o['word_len'] for o in unequal_orbits]
    print(f"\n  Word length distribution:")
    print(f"    Equal:   mean={np.mean(eq_lens):.1f}, max={max(eq_lens)}")
    print(f"    Unequal: mean={np.mean(uneq_lens):.1f}, max={max(uneq_lens)}")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  THREE-BODY PROBLEM: UNEQUAL-MASS ORBIT ANALYSIS")
    print("  Farey/Gamma(2) structure exploration")
    print("=" * 70)

    # Parse unequal-mass words
    print("\n[1] Parsing unequal-mass free-group words...")
    unequal_file = '/tmp/three_body_unequal_words.md'
    unequal_orbits = parse_unequal_mass_words(unequal_file)
    print(f"    Parsed {len(unequal_orbits)} unequal-mass orbits")

    # Parse equal-mass words
    print("\n[2] Parsing equal-mass free-group words...")
    equal_file = '/tmp/three_body_equal_words.md'
    equal_orbits = parse_equal_mass_words(equal_file)
    print(f"    Parsed {len(equal_orbits)} equal-mass orbits")

    # Analyze unequal mass
    unequal_orbits, uneq_class_stats, uneq_mass_stats = analyze_words(
        unequal_orbits, "UNEQUAL MASS ORBITS"
    )

    # Analyze equal mass
    equal_orbits, eq_class_stats, eq_mass_stats = analyze_words(
        equal_orbits, "EQUAL MASS ORBITS"
    )

    # Compare
    compare_equal_unequal(equal_orbits, unequal_orbits)

    # Extended periodic table analysis
    print(f"\n{'='*70}")
    print(f"  EXTENDED PERIODIC TABLE ANALYSIS")
    print(f"{'='*70}\n")

    # The periodic table is indexed by (n_L, n_R) = counts of L and R generators
    # (equivalently, counts of A/a and B/b in the word)

    def word_to_LR_counts(word):
        """Count L-type (A,a) and R-type (B,b) letters."""
        n_L = sum(1 for c in word if c in 'Aa')
        n_R = sum(1 for c in word if c in 'Bb')
        return n_L, n_R

    # Build table for equal mass
    eq_table = defaultdict(list)
    for o in equal_orbits:
        nL, nR = word_to_LR_counts(o['word'])
        eq_table[(nL, nR)].append(o)

    # Build table for unequal mass
    uneq_table = defaultdict(list)
    for o in unequal_orbits:
        nL, nR = word_to_LR_counts(o['word'])
        uneq_table[(nL, nR)].append(o)

    # Find ranges
    all_nL = [k[0] for k in list(eq_table.keys()) + list(uneq_table.keys())]
    all_nR = [k[1] for k in list(eq_table.keys()) + list(uneq_table.keys())]

    print(f"Equal mass: {len(eq_table)} distinct (n_L, n_R) cells")
    print(f"Unequal mass: {len(uneq_table)} distinct (n_L, n_R) cells")
    print(f"n_L range: {min(all_nL)}-{max(all_nL)}")
    print(f"n_R range: {min(all_nR)}-{max(all_nR)}")

    # Which cells are new in unequal mass?
    new_cells = set(uneq_table.keys()) - set(eq_table.keys())
    print(f"\nNew cells from unequal mass: {len(new_cells)}")
    if new_cells:
        for cell in sorted(new_cells)[:20]:
            orbs = uneq_table[cell]
            masses = set(o['m3'] for o in orbs)
            print(f"  ({cell[0]:2d}, {cell[1]:2d}): {len(orbs)} orbits, masses={masses}")

    # Print compact table (show counts per cell)
    max_show = 20
    print(f"\nPERIODIC TABLE (n_L x n_R), counts [equal | +unequal]:")
    header = 'n_L\\n_R'
    print(f"{header:>8}", end="")
    for nR in range(min(all_nR), min(max(all_nR)+1, max_show+1)):
        print(f" {nR:>6}", end="")
    print()

    for nL in range(min(all_nL), min(max(all_nL)+1, max_show+1)):
        print(f"{nL:>8}", end="")
        for nR in range(min(all_nR), min(max(all_nR)+1, max_show+1)):
            eq_count = len(eq_table.get((nL, nR), []))
            uneq_count = len(uneq_table.get((nL, nR), []))
            if eq_count == 0 and uneq_count == 0:
                print(f"     .", end="")
            elif eq_count > 0 and uneq_count > 0:
                print(f" {eq_count}+{uneq_count:>2}", end="")
            elif eq_count > 0:
                print(f"  {eq_count:>3}e", end="")
            else:
                print(f"  {uneq_count:>3}u", end="")
        print()

    print("\n\nDone.")
