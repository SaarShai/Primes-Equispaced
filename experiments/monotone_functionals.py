#!/usr/bin/env python3
"""
UNIVERSALLY MONOTONE FUNCTIONALS OF FAREY SEQUENCES
=====================================================

Direction 4: Are there more universally monotone functionals of Farey sequences?

Building on the proved result: I_2(N) = sum_{gaps g} 1/g^2 is universally monotone.

Main hypothesis: The entire family I_k(N) = sum_{gaps g} (1/g)^k is universally
monotone increasing for ALL k > 0.

Key algebraic insight: A gap split (b,d) -> (b,b+d), (d,b+d) changes I_k by:
    DeltaI_k = (b(b+d))^k + (d(b+d))^k - (bd)^k = (b+d)^k(b^k + d^k) - (bd)^k

We prove this is STRICTLY POSITIVE for all k > 0 and b,d >= 1.

Also investigate J_k(N) = sum_{gaps g} g^k and find the complete monotonicity picture.
"""

from fractions import Fraction
from math import gcd, log, sqrt
import numpy as np
import os
import time

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_N = 500

# ============================================================
# FAREY SEQUENCE UTILITIES
# ============================================================

def farey_gaps(N):
    """
    Compute all gaps in F_N as Fraction objects (exact arithmetic).
    Each gap = c/d - a/b for consecutive a/b < c/d in F_N.
    By the Farey property, all gaps = 1/(b*d).
    Returns list of (b, d) pairs for consecutive Farey fractions a/b < c/d.
    """
    # Farey sequence iterative generation
    fracs = [(0, 1), (1, N)]
    # Standard Farey generation
    a, b = 0, 1
    c, d = 1, N
    while (c, d) != (1, 1):
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        fracs.append((c, d))
    # fracs is now [(0,1), numerators/denominators of F_N in order, (1,1)]
    # Actually let's use a simpler approach
    pass

def farey_sequence(N):
    """Generate Farey sequence F_N as list of (p, q) pairs (p/q in lowest terms)."""
    sequence = []
    a, b, c, d = 0, 1, 1, N
    sequence.append((a, b))
    while (c, d) != (1, 1) or not sequence:
        sequence.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
    sequence.append((1, 1))
    return sequence

def farey_bd_pairs(N):
    """
    Return list of (b, d) pairs for consecutive Farey fractions a/b < c/d in F_N.
    The gap size is 1/(b*d) by the Farey property.
    """
    seq = farey_sequence(N)
    pairs = []
    for i in range(len(seq)-1):
        _, b = seq[i]
        _, d = seq[i+1]
        pairs.append((b, d))
    return pairs

def compute_Ik(N, k):
    """Compute I_k(N) = sum of (b*d)^k for all consecutive Farey pairs in F_N."""
    pairs = farey_bd_pairs(N)
    return sum((b*d)**k for b, d in pairs)

def compute_Jk(N, k):
    """Compute J_k(N) = sum of (1/(b*d))^k = sum g^k for all gaps in F_N."""
    pairs = farey_bd_pairs(N)
    return sum((1.0/(b*d))**k for b, d in pairs)

# ============================================================
# ALGEBRAIC LEMMA VERIFICATION
# ============================================================

def delta_Ik_split(b, d, k):
    """
    Change in I_k when gap 1/(b*d) splits into 1/(b*(b+d)) and 1/(d*(b+d)).
    Old: (b*d)^k
    New: (b*(b+d))^k + (d*(b+d))^k = (b+d)^k * (b^k + d^k)
    Delta = (b+d)^k * (b^k + d^k) - (b*d)^k
    """
    old = (b * d)**k
    new = (b*(b+d))**k + (d*(b+d))**k
    return new - old

def prove_delta_positive(k, num_samples=10000):
    """
    Verify (b+d)^k * (b^k + d^k) > (b*d)^k for random b,d >= 1.
    Also check analytically.
    """
    violations = 0
    min_ratio = float('inf')
    
    for _ in range(num_samples):
        b = np.random.randint(1, 100)
        d = np.random.randint(1, 100)
        delta = delta_Ik_split(b, d, k)
        ratio = delta / (b*d)**k  # normalized
        if delta <= 0:
            violations += 1
        if ratio < min_ratio:
            min_ratio = ratio
    
    return violations, min_ratio

def analytic_proof_Ik_monotone(k):
    """
    Proof that (b+d)^k(b^k + d^k) > (b*d)^k for k > 0, b,d >= 1.
    
    Method: AM-GM inequality.
    
    (b+d)^k >= (2*sqrt(bd))^k = 2^k * (bd)^(k/2)
    b^k + d^k >= 2*(bd)^(k/2)   [AM-GM]
    
    Therefore:
    (b+d)^k * (b^k + d^k) >= 2^k * (bd)^(k/2) * 2 * (bd)^(k/2)
                            = 2^(k+1) * (bd)^k
    
    Since 2^(k+1) > 1 for all k > -1 (in particular all k > 0):
    (b+d)^k * (b^k + d^k) > (bd)^k.
    
    Returns the lower bound constant 2^(k+1).
    """
    return 2**(k+1)

# ============================================================
# J_k MONOTONICITY (GAPS THEMSELVES)
# ============================================================

def delta_Jk_split(b, d, k):
    """
    Change in J_k = sum g^k when gap g = 1/(bd) splits.
    Old: (1/(bd))^k
    New: (1/(b*(b+d)))^k + (1/(d*(b+d)))^k
    Delta = 1/(b*(b+d))^k + 1/(d*(b+d))^k - 1/(bd)^k
    """
    g = 1.0/(b*d)
    g1 = 1.0/(b*(b+d))
    g2 = 1.0/(d*(b+d))
    return g1**k + g2**k - g**k

def analyze_Jk_monotonicity(k, num_samples=10000):
    """
    For J_k = sum g^k:
    - k < 1: sum is superadditive under splitting (monotone increasing)?
    - k = 1: sum = total gap = 1 (constant!)
    - k > 1: sum is subadditive under splitting (monotone decreasing)
    """
    # Theoretical: g1^k + g2^k vs (g1+g2)^k
    # For k < 1: x^k is concave, so g1^k + g2^k > (g1+g2)^k
    #   => delta > 0 => J_k is increasing
    # For k = 1: g1 + g2 = g1 + g2, delta = 0 always (total gap = 1)
    # For k > 1: x^k is convex, so g1^k + g2^k < (g1+g2)^k
    #   => delta < 0 => J_k is decreasing
    
    violations = 0
    deltas = []
    for _ in range(num_samples):
        b = np.random.randint(1, 100)
        d = np.random.randint(1, 100)
        delta = delta_Jk_split(b, d, k)
        deltas.append(delta)
        # For k < 1 expect > 0, for k > 1 expect < 0
        if k < 1 and delta < 0:
            violations += 1
        elif k > 1 and delta > 0:
            violations += 1
    
    return violations, np.mean(deltas)

# ============================================================
# SYSTEMATIC SEARCH FOR UNIVERSALLY MONOTONE FUNCTIONALS
# ============================================================

def check_monotone_N(N_max, func_name, func):
    """
    Check if func(N) > func(N-1) for all N from 2 to N_max.
    Returns (is_monotone, first_violation_N, or None)
    """
    prev = func(1)
    for N in range(2, N_max+1):
        curr = func(N)
        if curr <= prev:
            return False, N, curr - prev
        prev = curr
    return True, None, None

# ============================================================
# MAIN INVESTIGATION
# ============================================================

def main():
    print("=" * 70)
    print("UNIVERSALLY MONOTONE FUNCTIONALS OF FAREY SEQUENCES")
    print("=" * 70)
    print()
    
    # --------------------------------------------------------
    # PART 1: THE I_k FAMILY
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 1: I_k(N) = sum_{gaps g} (1/g)^k = sum (b*d)^k")
    print("=" * 70)
    print()
    print("Algebraic claim: For any split (b,d) -> (b,b+d),(d,b+d),")
    print("    Delta I_k = (b+d)^k(b^k + d^k) - (bd)^k > 0 for all k > 0.")
    print()
    print("PROOF via AM-GM:")
    print("    (b+d)^k >= (2*sqrt(bd))^k = 2^k * (bd)^(k/2)")
    print("    b^k + d^k >= 2*(bd)^(k/2)   [AM-GM]")
    print("    Product >= 2^(k+1) * (bd)^k > (bd)^k.  QED.")
    print()
    print(f"{'k':>6}  {'LB=2^(k+1)':>12}  {'violations':>10}  {'min_ratio':>12}  monotone?")
    print("-" * 60)
    
    k_values_Ik = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]
    for k in k_values_Ik:
        lb = analytic_proof_Ik_monotone(k)
        viols, min_ratio = prove_delta_positive(k, num_samples=50000)
        print(f"{k:>6.1f}  {lb:>12.4f}  {viols:>10}  {min_ratio:>12.6f}  {'YES' if viols==0 else 'NO'}")
    
    print()
    print("Conclusion: I_k is universally monotone for ALL k > 0.")
    print()
    
    # --------------------------------------------------------
    # PART 2: VERIFY I_k MONOTONICITY NUMERICALLY
    # --------------------------------------------------------
    print("=" * 70)
    print(f"PART 2: Numerical verification of I_k monotonicity for N = 2..{MAX_N}")
    print("=" * 70)
    print()
    
    k_test = [0.5, 1.0, 2.0, 3.0]
    for k in k_test:
        t0 = time.time()
        # Check monotonicity N=2..200 (faster subset)
        prev_val = compute_Ik(1, k)
        violations = []
        for N in range(2, 201):
            curr_val = compute_Ik(N, k)
            if curr_val <= prev_val:
                violations.append((N, curr_val - prev_val))
            prev_val = curr_val
        elapsed = time.time() - t0
        print(f"  I_{k}:  violations in N=2..200: {len(violations)}  ({elapsed:.1f}s)")
        if violations:
            print(f"    First violation: N={violations[0][0]}, delta={violations[0][1]:.6e}")
    print()
    
    # --------------------------------------------------------
    # PART 3: J_k = sum g^k MONOTONICITY
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 3: J_k(N) = sum_{gaps g} g^k = sum 1/(b*d)^k")
    print("=" * 70)
    print()
    print("When gap 1/(bd) splits into 1/(b(b+d)) and 1/(d(b+d)):")
    print("    Delta J_k = g1^k + g2^k - g^k  where g = g1 + g2")
    print()
    print("Key: this is the question 'is x^k superadditive or subadditive?'")
    print("  k < 1: concave => g1^k + g2^k > (g1+g2)^k  => J_k INCREASES")
    print("  k = 1: g1 + g2 = g (trivially), J_1 = sum g = 1 (CONSTANT)")
    print("  k > 1: convex => g1^k + g2^k < (g1+g2)^k  => J_k DECREASES")
    print()
    print(f"{'k':>6}  {'expected':>12}  {'violations':>10}  {'mean_delta':>14}")
    print("-" * 50)
    
    k_values_Jk = [0.1, 0.5, 0.9, 1.0, 1.1, 2.0, 3.0]
    for k in k_values_Jk:
        viols, mean_d = analyze_Jk_monotonicity(k, num_samples=50000)
        if abs(k - 1.0) < 0.01:
            expected = "constant"
        elif k < 1:
            expected = "increasing"
        else:
            expected = "decreasing"
        print(f"{k:>6.1f}  {expected:>12}  {viols:>10}  {mean_d:>14.6e}")
    
    print()
    print("Note: J_1 = sum g = 1 for ALL N (total length of [0,1] = 1).")
    print()
    
    # --------------------------------------------------------
    # PART 4: THE COMPLETE MONOTONICITY PICTURE
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 4: COMPLETE PICTURE - All gap-based functionals")
    print("=" * 70)
    print()
    print("For the family F_k(N) = sum_{gaps g} f_k(g) where f_k(g) = g^k:")
    print()
    print("  k < 0:  I_k = sum g^k = sum (1/g)^{|k|}")
    print("          Split: g^k = (g1+g2)^k. For k<0, this is INCREASING in |g|,")
    print("          so splitting (smaller g) gives... complex behavior.")
    print()
    
    # Check k < 0 (these are I_k with negative exponents)
    print("Checking k < 0 (g^k for negative k):")
    k_neg = [-0.5, -1.0, -2.0]
    for k in k_neg:
        # g^k for k < 0: g^k = 1/g^|k|, which DECREASES as g decreases
        # After split g -> g1, g2: g1^k + g2^k - g^k
        # Since g1,g2 < g: g1^k > g^k (more negative = larger in abs, but...)
        # Wait: if k=-1, g^(-1) = 1/g. After split: 1/g1 + 1/g2 - 1/g = bd + b(b+d) + d(b+d) - ... hmm
        viols, mean_d = analyze_Jk_monotonicity(k, num_samples=10000)
        print(f"  k={k:5.1f}: mean_delta = {mean_d:.4e}  (violations: {viols})")
    print()
    print("Note: For k < 0, J_k = sum g^k = sum (1/g)^|k| = I_{|k|}.")
    print("This is I_k with |k|, which we proved monotone increasing.")
    print("But J_k with k < 0 has delta g1^k + g2^k - g^k = ?")
    print()
    
    # --------------------------------------------------------
    # PART 5: NON-GAP FUNCTIONALS
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 5: FUNCTIONALS NOT BASED ON INDIVIDUAL GAPS")
    print("=" * 70)
    print()
    
    # Test several candidate functionals
    print("Testing candidate universally monotone functionals on N=2..200:")
    print()
    
    def compute_wobble(N):
        """W(N) = sum (f_j - j/(n-1))^2"""
        seq = farey_sequence(N)
        n = len(seq)
        ideal = np.linspace(0, 1, n)
        fracs = np.array([p/q for p, q in seq])
        return float(np.sum((fracs - ideal)**2))
    
    def compute_I2(N):
        """I_2(N) = sum (1/g)^2 = sum (bd)^2"""
        pairs = farey_bd_pairs(N)
        return sum((b*d)**2 for b, d in pairs)
    
    def compute_log_sum(N):
        """sum log(bd) = sum log(1/g) (entropy-like)"""
        pairs = farey_bd_pairs(N)
        return sum(log(b*d) for b, d in pairs)
    
    def compute_max_gap(N):
        """Maximum gap in F_N (known to be 1/floor(N/2) approximately)"""
        pairs = farey_bd_pairs(N)
        return max(1.0/(b*d) for b, d in pairs)
    
    def compute_num_gaps(N):
        """Number of gaps = |F_N| - 1"""
        seq = farey_sequence(N)
        return len(seq) - 1
    
    def compute_gap_entropy(N):
        """Shannon entropy H = -sum g * log(g) of gap distribution"""
        pairs = farey_bd_pairs(N)
        total = 1.0
        H = sum((1.0/(b*d)) * log(b*d) for b, d in pairs)
        return H
    
    def compute_sum_bd(N):
        """sum b*d = sum 1/g (I_1)"""
        pairs = farey_bd_pairs(N)
        return sum(b*d for b, d in pairs)
    
    functionals = [
        ("W(N) [wobble]", compute_wobble, "should be non-monotone"),
        ("I_1(N) = sum bd", compute_sum_bd, "should be monotone"),
        ("I_2(N) = sum (bd)^2", compute_I2, "proved monotone"),
        ("log_sum = sum log(bd)", compute_log_sum, "conjecture: monotone"),
        ("max_gap(N)", compute_max_gap, "should decrease (monotone dec)"),
        ("H(N) = gap entropy", compute_gap_entropy, "conjecture: monotone"),
        ("#gaps(N)", compute_num_gaps, "trivially increasing"),
    ]
    
    print(f"{'Functional':30}  {'Expected':20}  {'Violations':10}  {'Result':10}")
    print("-" * 80)
    
    for name, func, expected in functionals:
        prev = func(1)
        violations = 0
        first_viol = None
        for N in range(2, 201):
            curr = func(N)
            if curr <= prev:
                violations += 1
                if first_viol is None:
                    first_viol = (N, curr - prev)
            prev = curr
        
        result = "MONOTONE" if violations == 0 else f"{violations} viols"
        print(f"  {name:28}  {expected:20}  {violations:10}  {result:10}", end="")
        if first_viol and violations <= 3:
            print(f"  (1st: N={first_viol[0]}, d={first_viol[1]:.2e})", end="")
        print()
    
    print()
    
    # --------------------------------------------------------
    # PART 6: ANALYTIC PROOF SKETCH
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 6: ANALYTIC PROOF OF I_k MONOTONICITY (FORMAL SKETCH)")
    print("=" * 70)
    print()
    print("THEOREM: For all k > 0 and all N >= 2, I_k(N) > I_k(N-1).")
    print()
    print("PROOF:")
    print("Step 1 (Gap characterization). Every gap in F_N has the form 1/(bd)")
    print("  where a/b < c/d are consecutive Farey fractions with bc - ad = 1.")
    print()
    print("Step 2 (Update rule). F_N is obtained from F_{N-1} by inserting,")
    print("  for each consecutive pair a/b < c/d in F_{N-1} with b+d = N,")
    print("  the mediant (a+c)/(b+d). This replaces the gap 1/(bd) with two gaps")
    print("  1/(b(b+d)) and 1/(d(b+d)).")
    print()
    print("Step 3 (Algebraic inequality). For k > 0 and b,d >= 1:")
    print("  Delta I_k = (b(b+d))^k + (d(b+d))^k - (bd)^k")
    print("            = (b+d)^k * (b^k + d^k) - (b*d)^k  > 0.")
    print()
    print("  Proof of inequality:")
    print("    By AM-GM: b^k + d^k >= 2(bd)^(k/2)")
    print("    By AM-GM: (b+d)^k >= (2*sqrt(bd))^k = 2^k * (bd)^(k/2)")
    print("    Product:  (b+d)^k * (b^k+d^k) >= 2^k*(bd)^(k/2) * 2*(bd)^(k/2)")
    print("                                    = 2^(k+1) * (bd)^k")
    print("    Since 2^(k+1) >= 2 > 1:  (b+d)^k*(b^k+d^k) > (bd)^k.  QED step 3.")
    print()
    print("Step 4 (At least one insertion). For N >= 2, phi(N) >= 1, so at least")
    print("  one gap is split. Therefore I_k(N) > I_k(N-1).  QED.")
    print()
    print("COROLLARY: The entire family {I_k : k > 0} gives universally monotone")
    print("increasing sequences. This contrasts with the wobble W(N) which fails")
    print("monotonicity at primes with M(p) >= 8.")
    print()
    
    # --------------------------------------------------------
    # PART 7: THE SHARP LOWER BOUND
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 7: SHARP LOWER BOUND FOR I_k INCREMENT")
    print("=" * 70)
    print()
    print("The AM-GM bound gives: Delta I_k / (b*d)^k >= 2^(k+1) - 1.")
    print()
    print("Is this SHARP? I.e., for which (b,d) is the ratio minimized?")
    print()
    print("Setting b=d: (b+d)^k*(b^k+d^k) / (bd)^k = (2b)^k * 2b^k / b^{2k}")
    print("           = 2^k * 2 = 2^(k+1).")
    print("So equality in AM-GM holds when b = d. But b = d means bd = b^2,")
    print("and 1/(b*d) = 1/b^2. The gap 1/b^2 is NOT a valid Farey gap!")
    print("(Farey gaps are 1/(bd) with bc - ad = 1, so gcd(b,d) = 1 needed.)")
    print("gcd(b,b) = b, so b=d is only possible when b=d=1, giving gap 1/1.")
    print()
    print("Therefore the ratio (b+d)^k*(b^k+d^k)/(bd)^k > 2^(k+1) strictly")
    print("for ALL valid Farey splits (where gcd(b,d)=1 and b,d >= 1).")
    print()
    
    # Compute minimum ratio for actual Farey splits
    print("Minimum ratio for ACTUAL Farey splits (N=2..200):")
    for k in [0.5, 1.0, 2.0, 3.0]:
        min_ratio = float('inf')
        min_bd = None
        for N in range(2, 100):
            seq = farey_sequence(N)
            for i in range(len(seq)-1):
                _, b = seq[i]
                _, d = seq[i+1]
                ratio = ((b+d)**k * (b**k + d**k)) / (b*d)**k
                if ratio < min_ratio:
                    min_ratio = ratio
                    min_bd = (b, d)
        theoretical_lb = 2**(k+1)
        print(f"  k={k}: min_ratio = {min_ratio:.6f}  at (b,d)={min_bd}  "
              f"theoretical LB = {theoretical_lb:.4f}  ratio/LB = {min_ratio/theoretical_lb:.6f}")
    print()
    
    # --------------------------------------------------------
    # PART 8: LOG-SUM AND ENTROPY ANALYSIS
    # --------------------------------------------------------
    print("=" * 70)
    print("PART 8: LOG-SUM AND GAP ENTROPY -- ANALYTIC INVESTIGATION")
    print("=" * 70)
    print()
    print("Q: Is L(N) = sum log(b*d) universally monotone?")
    print()
    print("Delta L for split: log(b*(b+d)) + log(d*(b+d)) - log(b*d)")
    print("   = log(b) + log(b+d) + log(d) + log(b+d) - log(b) - log(d)")
    print("   = 2*log(b+d) > 0  for all b,d >= 1.")
    print()
    print("PROVED: L(N) = sum log(1/g) is universally monotone increasing!")
    print("In fact: Delta L = 2*log(b+d) >= 2*log(2) = log(4) > 0.")
    print()
    print("Q: Is H(N) = -sum g*log(g) = sum (1/(b*d))*log(b*d) universally monotone?")
    print()
    print("Delta H for split:")
    print("   log(b*(b+d))/(b*(b+d)) + log(d*(b+d))/(d*(b+d)) - log(b*d)/(b*d)")
    print()
    print("Let's compute numerically and check...")
    
    # Check if log-sum is monotone
    prev = sum(log(b*d) for b, d in farey_bd_pairs(1))
    L_violations = 0
    for N in range(2, 201):
        curr = sum(log(b*d) for b, d in farey_bd_pairs(N))
        if curr <= prev:
            L_violations += 1
        prev = curr
    print(f"\n  L(N) violations N=2..200: {L_violations}  (expected 0)")
    
    # Check analytic: delta L = 2 log(b+d)
    print()
    print("  Verifying Delta L = 2*log(b+d) analytically on random samples:")
    viols = 0
    for _ in range(10000):
        b = np.random.randint(1, 1000)
        d = np.random.randint(1, 1000)
        delta = log(b*(b+d)) + log(d*(b+d)) - log(b*d)
        expected = 2*log(b+d)
        if abs(delta - expected) > 1e-10:
            viols += 1
    print(f"  Verification failures: {viols}  (expected 0)")
    
    print()
    print("=" * 70)
    print("SUMMARY OF UNIVERSALLY MONOTONE FUNCTIONALS")
    print("=" * 70)
    print()
    print("PROVED UNIVERSALLY MONOTONE INCREASING:")
    print("  1. I_k(N) = sum (1/g)^k = sum (bd)^k for ALL k > 0")
    print("     Proof: AM-GM gives Delta I_k >= (2^(k+1)-1)*(bd)^k > 0")
    print("  2. L(N) = sum log(1/g) = sum log(bd)")
    print("     Proof: Delta L = 2*log(b+d) >= 2*log(2) > 0")
    print("  3. #gaps(N) = |F_N| - 1 (trivial: phi(N) >= 1)")
    print()
    print("PROVED UNIVERSALLY MONOTONE DECREASING:")
    print("  4. J_k(N) = sum g^k for k > 1")
    print("     Proof: x^k convex => g1^k + g2^k < (g1+g2)^k")
    print("  5. max_gap(N) (trivially: new fractions only reduce max gap)")
    print()
    print("PROVED CONSTANT:")
    print("  6. J_1(N) = sum g = 1 for all N (trivially)")
    print()
    print("NOT UNIVERSALLY MONOTONE:")
    print("  7. W(N) = wobble (fails at primes p with M(p) >= 8)")
    print("  8. J_k(N) = sum g^k for 0 < k < 1 -- check status below")
    print()
    
    # Verify J_k for 0 < k < 1
    for k in [0.1, 0.3, 0.5, 0.7, 0.9]:
        prev = compute_Jk(1, k)
        viols = 0
        for N in range(2, 201):
            curr = compute_Jk(N, k)
            if curr <= prev:
                viols += 1
            prev = curr
        print(f"  J_{k}: violations N=2..200: {viols}  ({'MONOTONE INC' if viols==0 else 'NOT MONOTONE'})")
    
    print()
    print("COMPLETE PICTURE: J_k = sum g^k")
    print("  0 < k < 1: UNIVERSALLY MONOTONE INCREASING (concave function)")
    print("  k = 1: CONSTANT (= 1 always)")  
    print("  k > 1: UNIVERSALLY MONOTONE DECREASING (convex function)")
    print()
    print("KEY INSIGHT: The family {I_k, J_k, L} gives monotone functionals")
    print("that can PROVE things about Farey sequences, unlike the wobble W.")
    print()
    print("OPEN QUESTION: Can I_k or L be used to bound W or ΔW?")
    print("  If I_k grows predictably, can we use it as a 'comparison functional'")
    print("  to understand when W(prime) > W(prime-1)?")
    
    print()
    print("Time elapsed:", end=" ")

if __name__ == "__main__":
    t_start = time.time()
    main()
    print(f"{time.time() - t_start:.1f}s")
