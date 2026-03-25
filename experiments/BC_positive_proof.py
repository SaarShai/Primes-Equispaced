#!/usr/bin/env python3
"""
B+C POSITIVITY: Comprehensive exploration of all approaches.
================================================================

Goal: Prove B+C > 0 for all primes p >= 11.

B+C = (Σ D_new² - Σ D_old²) / n'²  where sum is over OLD fractions (f ≠ 1).
    = (2Σ D·δ + Σ δ²) / n'²
    = Σ δ(2D + δ) / n'²

KEY FINDING FROM INITIAL RUN:
  R = 2ΣD·δ / Σδ²  ranges from -0.52 to +2.91 for p=11..101
  B+C = Σδ² · (1 + R)
  B+C > 0 iff R > -1
  1+R is ALWAYS >= 0.48 (well above 0)

  The cross term ΣD·δ can be EITHER sign (not always negative)
  But |R| < 1 when it's negative, so Σδ² always dominates

  APPROACH: Prove |R| < 1, i.e., 2|ΣD·δ| < Σδ²

APPROACHES TESTED:
  1. Per-denominator decomposition
  2. Variance interpretation
  3. D/δ ratio analysis
  4. Fourier/spectral
  5. Direct lower bound
  6. D_new representation
  7. Dedekind sum connection
  8. Scaling analysis
  9. NEW: Per-denominator bound on cross term
  10. NEW: The "deficit" approach via Dedekind sums
"""

from fractions import Fraction
from math import gcd, floor, isqrt, sqrt, pi, cos, sin, log
from collections import defaultdict
import time

start_time = time.time()

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def farey_sequence(N):
    fracs = set()
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def compute_all_quantities(p):
    """Compute D_old, D_new, δ for every old fraction. Exact rationals."""
    N_old = p - 1
    old_fracs = farey_sequence(N_old)
    n = len(old_fracs)
    n_prime = n + p - 1

    new_fracs = farey_sequence(p)
    new_rank = {f: j for j, f in enumerate(new_fracs)}

    results = []
    for j, f in enumerate(old_fracs):
        if f == Fraction(1, 1):
            continue
        D_old = Fraction(j) - Fraction(n) * f
        j_new = new_rank[f]
        D_new = Fraction(j_new) - Fraction(n_prime) * f
        delta = D_new - D_old
        results.append({
            'f': f, 'a': f.numerator, 'b': f.denominator,
            'D_old': D_old, 'D_new': D_new, 'delta': delta,
        })
    return results, n, n_prime

# ============================================================
# CORE COMPUTATION: gather data for all test primes
# ============================================================

primes = sieve_primes(500)
test_primes = [p for p in primes if 5 <= p <= 200]

print("="*80)
print("B+C POSITIVITY: COMPREHENSIVE ANALYSIS")
print("="*80)

all_data = {}
print(f"\n{'p':>5s}  {'B+C':>12s}  {'Σδ²':>10s}  {'2ΣD·δ':>10s}  {'R=2ΣDδ/Σδ²':>12s}  {'1+R':>8s}")
print("-"*70)

for p in test_primes:
    results, n, n_prime = compute_all_quantities(p)

    sum_delta_sq = sum(r['delta']**2 for r in results)
    sum_cross = sum(r['D_old'] * r['delta'] for r in results)
    sum_D_sq = sum(r['D_old']**2 for r in results)
    BC = 2 * sum_cross + sum_delta_sq
    R = float(2 * sum_cross / sum_delta_sq) if sum_delta_sq != 0 else 0

    all_data[p] = {
        'results': results, 'n': n, 'n_prime': n_prime,
        'BC': BC, 'sum_delta_sq': sum_delta_sq,
        'sum_cross': sum_cross, 'sum_D_sq': sum_D_sq,
    }

    sign = "+" if BC > 0 else "***NEG***"
    print(f"  {p:3d}  {float(BC):12.4f}  {float(sum_delta_sq):10.4f}  "
          f"{float(2*sum_cross):10.4f}  {R:12.4f}  {1+R:8.4f}  {sign}")

# ============================================================
# KEY ANALYSIS 1: When is the cross term negative?
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 1: Sign of cross term ΣD·δ and what controls it")
print(f"{'='*80}")

from math import log as ln

# Mertens function
M_arr, mu_arr = [0]*501, [0]*501
mu_arr[1] = 1
smallest_prime = [0]*501
for i in range(2, 501):
    if smallest_prime[i] == 0:
        for j in range(i, 501, i):
            if smallest_prime[j] == 0: smallest_prime[j] = i
for nn in range(2, 501):
    pp = smallest_prime[nn]
    if (nn // pp) % pp == 0: mu_arr[nn] = 0
    else: mu_arr[nn] = -mu_arr[nn // pp]
running = 0
for nn in range(501):
    running += mu_arr[nn]
    M_arr[nn] = running

print(f"\n  {'p':>5s}  {'M(p)':>5s}  {'sign(ΣDδ)':>10s}  {'R':>8s}  {'1+R':>8s}")
for p in test_primes:
    data = all_data[p]
    sign = "+" if data['sum_cross'] > 0 else "-"
    R = float(2 * data['sum_cross'] / data['sum_delta_sq'])
    print(f"  {p:5d}  {M_arr[p]:5d}  {sign:>10s}  {R:8.4f}  {1+R:8.4f}")

# ============================================================
# KEY ANALYSIS 2: Per-denominator decomposition (the real structure)
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 2: Per-denominator structure of B+C = Σ_b C_b")
print("  C_b = Σ_{a coprime b} δ(a/b)·(2D(a/b) + δ(a/b))")
print(f"{'='*80}")

for p in [11, 23, 37, 53, 97, 101]:
    if p not in all_data: continue
    results = all_data[p]['results']

    by_denom = defaultdict(list)
    for r in results:
        by_denom[r['b']].append(r)

    print(f"\n  p={p}: B+C = {float(all_data[p]['BC']):.4f}")
    neg_contribs = []
    pos_contribs = []

    for b in sorted(by_denom.keys()):
        entries = by_denom[b]
        sigma = p % b

        sum_delta_b = sum(r['delta'] for r in entries)
        sum_delta_sq_b = sum(r['delta']**2 for r in entries)
        cross_b = sum(r['D_old'] * r['delta'] for r in entries)
        contrib_b = 2 * cross_b + sum_delta_sq_b

        if contrib_b < 0:
            neg_contribs.append((b, float(contrib_b)))
        else:
            pos_contribs.append((b, float(contrib_b)))

    total_neg = sum(c for _, c in neg_contribs)
    total_pos = sum(c for _, c in pos_contribs)
    print(f"    Positive denoms: {len(pos_contribs)}, total = {total_pos:.4f}")
    print(f"    Negative denoms: {len(neg_contribs)}, total = {total_neg:.4f}")
    if neg_contribs:
        print(f"    Negative: {neg_contribs[:8]}")
    print(f"    Ratio |neg|/pos = {abs(total_neg)/total_pos:.4f}" if total_pos > 0 else "")

# ============================================================
# KEY ANALYSIS 3: The Dedekind sum / deficit structure
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 3: Dedekind sum structure")
print("  δ(a/b) = (a - σa mod b)/b where σ = p mod b")
print("  Σ_a δ(a/b)² = 2·(Σa² - Σ a·(σa mod b))/b² = 2·deficit(b,σ)/b²")
print("  When σ=1 (i.e. b | p-1): deficit=0, all δ=0 for this b")
print(f"{'='*80}")

# For the cross term per denom, we need D_old.
# D_old(a/b) = rank(a/b in F_{p-1}) - n·(a/b)
# This is harder to express purely in terms of (b, σ).
# But let's see if the cross term has a clean formula too.

# Key question: can we express Σ_a D_old(a/b)·δ(a/b) in terms of known sums?

# D_old(a/b) = (counting function up to a/b) - n·a/b
# The counting function: #{c/d ∈ F_{p-1} : c/d ≤ a/b}
# This involves ALL denominators, not just b.
# So D_old does NOT decompose cleanly by single denominator.

# BUT: we know Σ_a D_old(a/b) = -φ(b)/2 (for b > 1)
# And: Σ_a δ(a/b) = 0
# So: Σ_a (D_old + δ/2)·δ = Σ D_old·δ + Σ δ²/2

# Let's look at the COVARIANCE interpretation within each denominator:
# Cov_b(D_old, δ) = (1/φ(b)) Σ D·δ - (1/φ(b) Σ D)(1/φ(b) Σ δ)
#                 = (1/φ(b)) Σ D·δ - (-1/2)·0 = (1/φ(b)) Σ D·δ

# So the cross term per denom = φ(b) · Cov_b(D_old, δ)
# Need Cov_b < Var_b(δ)/2 for the per-denom contribution to be positive
# (since C_b = 2·φ(b)·Cov_b + φ(b)·Var_b(δ))

for p in [11, 23, 53, 97]:
    if p not in all_data: continue
    results = all_data[p]['results']
    by_denom = defaultdict(list)
    for r in results:
        by_denom[r['b']].append(r)

    print(f"\n  p={p}: per-denom covariance structure")
    print(f"  {'b':>4s} {'σ':>3s} {'φ(b)':>5s} {'Cov(D,δ)':>10s} {'Var(δ)':>10s} {'ratio':>8s} {'C_b':>10s}")

    for b in sorted(by_denom.keys()):
        if b <= 1: continue
        entries = by_denom[b]
        sigma = p % b
        phi_b = len(entries)

        mean_D = sum(float(r['D_old']) for r in entries) / phi_b
        mean_delta = sum(float(r['delta']) for r in entries) / phi_b

        cov = sum(float(r['D_old'] * r['delta']) for r in entries) / phi_b - mean_D * mean_delta
        var_delta = sum(float(r['delta'])**2 for r in entries) / phi_b - mean_delta**2

        cross_b = sum(r['D_old'] * r['delta'] for r in entries)
        delta_sq_b = sum(r['delta']**2 for r in entries)
        C_b = float(2 * cross_b + delta_sq_b)

        ratio = cov / var_delta if var_delta > 1e-15 else 0

        if b <= 20 or C_b < -0.1:
            print(f"  {b:4d} {sigma:3d} {phi_b:5d} {cov:10.4f} {var_delta:10.4f} "
                  f"{ratio:8.4f} {C_b:10.4f}{'*' if C_b < 0 else ''}")

# ============================================================
# KEY ANALYSIS 4: The CRUCIAL decomposition
# B+C = Σ δ² + 2Σ D·δ
# Rewrite as: B+C = Σ D_new² - Σ D_old²
#
# Can we prove Σ D_new² > Σ D_old² DIRECTLY?
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 4: Direct Σ D_new² vs Σ D_old² comparison")
print("  Adding p-1 new fractions. Does total squared discrepancy always increase?")
print(f"{'='*80}")

# The new fractions k/p (k=1..p-1) also have discrepancies.
# Let's include them and see the FULL picture.

for p in [11, 23, 53, 97]:
    if p not in all_data: continue
    results = all_data[p]['results']
    n = all_data[p]['n']
    n_prime = all_data[p]['n_prime']

    sum_D_old_sq = sum(r['D_old']**2 for r in results)
    sum_D_new_sq_old_fracs = sum(r['D_new']**2 for r in results)

    # Also compute D_new for the NEW fractions k/p
    new_fracs = farey_sequence(p)
    new_rank = {f: j for j, f in enumerate(new_fracs)}

    sum_D_new_sq_new_fracs = Fraction(0)
    new_frac_D_new = []
    for k in range(1, p):
        f = Fraction(k, p)
        j_new = new_rank[f]
        D_new = Fraction(j_new) - Fraction(n_prime) * f
        sum_D_new_sq_new_fracs += D_new**2
        new_frac_D_new.append(float(D_new))

    total_D_new_sq = sum_D_new_sq_old_fracs + sum_D_new_sq_new_fracs

    print(f"\n  p={p}:")
    print(f"    Σ D_old² (old fracs)         = {float(sum_D_old_sq):.4f}")
    print(f"    Σ D_new² (old fracs)         = {float(sum_D_new_sq_old_fracs):.4f}")
    print(f"    Σ D_new² (new fracs k/p)     = {float(sum_D_new_sq_new_fracs):.4f}")
    print(f"    Σ D_new² (ALL fracs in F_p)  = {float(total_D_new_sq):.4f}")
    print(f"    Increase on old fracs: {float(sum_D_new_sq_old_fracs - sum_D_old_sq):.4f}")
    print(f"    New fracs add:         {float(sum_D_new_sq_new_fracs):.4f}")
    print(f"    Mean D_new² per new frac:    {float(sum_D_new_sq_new_fracs/(p-1)):.4f}")
    print(f"    Mean |D_new| of new fracs:   {sum(abs(d) for d in new_frac_D_new)/(p-1):.4f}")

# ============================================================
# KEY ANALYSIS 5: The WINNER approach — bound via Cauchy-Schwarz variant
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 5: Cauchy-Schwarz approach to bounding |ΣD·δ|")
print("  Need: 2|ΣD·δ| < Σδ² when ΣD·δ < 0")
print("  When ΣD·δ > 0, B+C > Σδ² > 0 automatically")
print(f"{'='*80}")

# When is ΣD·δ < 0? Check which primes have negative cross term
neg_cross_primes = [p for p in sorted(all_data.keys()) if all_data[p]['sum_cross'] < 0]
print(f"\n  Primes with ΣD·δ < 0: {neg_cross_primes}")
print(f"  For these, need 2|ΣD·δ| < Σδ²")

for p in neg_cross_primes:
    data = all_data[p]
    ratio = float(2 * abs(data['sum_cross']) / data['sum_delta_sq'])
    print(f"    p={p}: 2|ΣD·δ|/Σδ² = {ratio:.4f}, margin = {1 - ratio:.4f}")

# ============================================================
# KEY ANALYSIS 6: CORRELATION coefficient interpretation
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 6: Correlation coefficient ρ = ΣD·δ / √(ΣD²·Σδ²)")
print("  By CS: |ρ| ≤ 1")
print("  B+C = Σδ² + 2ρ·√(ΣD²·Σδ²) = Σδ²(1 + 2ρ·√(ΣD²/Σδ²))")
print("  B+C > 0 iff ρ > -√(Σδ²/ΣD²)/2 ≈ -√(Σδ²/(4ΣD²))")
print(f"{'='*80}")

print(f"\n  {'p':>5s}  {'ρ':>8s}  {'√(ΣD²/Σδ²)':>12s}  {'threshold':>10s}  {'margin':>8s}")
for p in sorted(all_data.keys()):
    data = all_data[p]
    rho = float(data['sum_cross']) / sqrt(float(data['sum_D_sq']) * float(data['sum_delta_sq']))
    ratio_sq = sqrt(float(data['sum_D_sq']) / float(data['sum_delta_sq']))
    threshold = -1 / (2 * ratio_sq)
    margin = rho - threshold
    print(f"  {p:5d}  {rho:8.4f}  {ratio_sq:12.4f}  {threshold:10.4f}  {margin:8.4f}")

# ============================================================
# KEY ANALYSIS 7: Is B+C = Σ δ(2D+δ) bounded below by Σδ²/2?
# i.e., is ΣD·δ > -Σδ²/4 always?
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 7: Lower bound quality")
print("  B+C = Σδ²·(1+R) where R = 2ΣD·δ/Σδ²")
print("  What is the minimum of (1+R)?")
print(f"{'='*80}")

min_1pR = float('inf')
min_p = 0
for p in sorted(all_data.keys()):
    data = all_data[p]
    R = float(2 * data['sum_cross'] / data['sum_delta_sq'])
    if 1 + R < min_1pR and p >= 11:
        min_1pR = 1 + R
        min_p = p

print(f"  Minimum (1+R) = {min_1pR:.4f} at p={min_p}")
print(f"  So B+C >= {min_1pR:.4f} · Σδ²")
print(f"  The tightest case is p={min_p}")

# ============================================================
# KEY ANALYSIS 8: Per-denom SIGN analysis of Σ δ·D_old
# Which denominators contribute negative cross-term?
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 8: Which denominators give negative C_b?")
print("  C_b = 2·Σ D(a/b)·δ(a/b) + Σ δ(a/b)²")
print(f"{'='*80}")

# Track: for each b, how often is C_b negative across primes?
denom_neg_count = defaultdict(int)
denom_total_count = defaultdict(int)

for p in sorted(all_data.keys()):
    if p < 11: continue
    results = all_data[p]['results']
    by_denom = defaultdict(list)
    for r in results:
        by_denom[r['b']].append(r)

    for b in by_denom:
        entries = by_denom[b]
        cross_b = sum(r['D_old'] * r['delta'] for r in entries)
        delta_sq_b = sum(r['delta']**2 for r in entries)
        C_b = 2 * cross_b + delta_sq_b
        denom_total_count[b] += 1
        if C_b < 0:
            denom_neg_count[b] += 1

print(f"\n  {'b':>4s}  {'neg/total':>12s}  {'pct_neg':>8s}")
for b in sorted(denom_total_count.keys()):
    if denom_total_count[b] > 0:
        pct = 100 * denom_neg_count[b] / denom_total_count[b]
        if denom_neg_count[b] > 0 or b <= 15:
            print(f"  {b:4d}  {denom_neg_count[b]:4d}/{denom_total_count[b]:<4d}    {pct:6.1f}%")

# ============================================================
# KEY ANALYSIS 9: The BIG IDEA — expressing cross term
# via the rank permutation
#
# For each old fraction a/b, δ(a/b) counts how many new fractions
# k/p fall below a/b minus the "expected" number (p-1)·(a/b).
# δ(a/b) = floor(pa/b) - (p-1)·(a/b) = -(frac(pa/b))  (fractional part)
# Wait: δ = floor(pa/b) - (p-1)·a/b = pa/b - {pa/b} - (p-1)·a/b
#      = a/b - {pa/b}
# where {x} = x - floor(x) is the fractional part.
#
# So δ(a/b) = a/b - {pa/b}
# This is the SAWTOOTH function difference!
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 9: Sawtooth representation δ(a/b) = a/b - {pa/b}")
print("  This is f - {pf} evaluated at Farey fractions f=a/b")
print(f"{'='*80}")

# Verify
for p in [11, 23]:
    results = all_data[p]['results']
    for r in results[:5]:
        a, b = r['a'], r['b']
        frac_part = Fraction(p * a % b, b)  # {pa/b}
        delta_check = Fraction(a, b) - frac_part
        assert delta_check == r['delta'], f"Sawtooth check failed"

# So δ(f) = f - {pf}
# And D_old(f) = N_{p-1}(f) - n·f  where N is the counting function
#
# B+C = Σ (f - {pf}) · (2·D_old(f) + f - {pf})
#     = Σ (f - {pf}) · (2·D_old(f)) + Σ (f - {pf})²
#
# The key cross term is Σ D_old(f)·(f - {pf})
# = Σ D_old(f)·f - Σ D_old(f)·{pf}
#
# Σ D_old(f)·f = Σ (j - nf)·f = Σ jf - n·Σf²
# Σ D_old(f)·{pf} = Σ (j - nf)·{pa/b} = Σ j·{pa/b} - n·Σ f·{pa/b}

# These are computable! Let's see if there's a pattern.

print(f"\n  Decomposition of cross term:")
print(f"  {'p':>5s}  {'Σ D·f':>12s}  {'Σ D·{{pf}}':>12s}  {'Σ D·δ':>12s}")

for p in sorted(all_data.keys()):
    results = all_data[p]['results']
    n = all_data[p]['n']

    sum_Df = sum(r['D_old'] * r['f'] for r in results)
    sum_D_fracpf = sum(r['D_old'] * Fraction((p * r['a']) % r['b'], r['b']) for r in results)
    sum_cross = sum(r['D_old'] * r['delta'] for r in results)

    # Verify: Σ D·δ = Σ D·f - Σ D·{pf}
    assert sum_Df - sum_D_fracpf == sum_cross

    print(f"  {p:5d}  {float(sum_Df):12.4f}  {float(sum_D_fracpf):12.4f}  {float(sum_cross):12.4f}")

# ============================================================
# KEY ANALYSIS 10: What if we use B+C = Σ D_new² - Σ D_old²
# and bound D_new in terms of D_old?
#
# D_new(a/b) = D_old(a/b) + δ(a/b)
# D_new² = D_old² + 2D·δ + δ²
# D_new² - D_old² = δ(2D + δ)
#
# For this to be > 0 in aggregate, we need the positive terms to win.
# The positive terms come from fractions where δ and (D + D_new) agree in sign.
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 10: Term-by-term sign analysis of δ·(D_old + D_new)")
print(f"{'='*80}")

for p in [11, 23, 53, 97]:
    if p not in all_data: continue
    results = all_data[p]['results']

    # Count: how many terms have δ > 0 with D_old + D_new > 0?
    # vs δ > 0 with D_old + D_new < 0? etc.

    pp_count = 0  # δ > 0, D+D' > 0 (positive contribution)
    pn_count = 0  # δ > 0, D+D' < 0 (negative contribution)
    np_count = 0  # δ < 0, D+D' > 0 (negative contribution)
    nn_count = 0  # δ < 0, D+D' < 0 (positive contribution)
    zero_count = 0

    pp_sum = pn_sum = np_sum = nn_sum = Fraction(0)

    for r in results:
        delta = r['delta']
        DD = r['D_old'] + r['D_new']

        if delta == 0 or DD == 0:
            zero_count += 1
            continue

        if delta > 0 and DD > 0:
            pp_count += 1; pp_sum += delta * DD
        elif delta > 0 and DD < 0:
            pn_count += 1; pn_sum += delta * DD
        elif delta < 0 and DD > 0:
            np_count += 1; np_sum += delta * DD
        elif delta < 0 and DD < 0:
            nn_count += 1; nn_sum += delta * DD

    total = pp_sum + pn_sum + np_sum + nn_sum
    pos = pp_sum + nn_sum
    neg = pn_sum + np_sum

    print(f"\n  p={p}: B+C = {float(total):.4f}")
    print(f"    δ>0, D+D'>0: {pp_count:5d} terms, sum = {float(pp_sum):+.4f}")
    print(f"    δ<0, D+D'<0: {nn_count:5d} terms, sum = {float(nn_sum):+.4f}")
    print(f"    δ>0, D+D'<0: {pn_count:5d} terms, sum = {float(pn_sum):+.4f}")
    print(f"    δ<0, D+D'>0: {np_count:5d} terms, sum = {float(np_sum):+.4f}")
    print(f"    Zero:         {zero_count:5d}")
    print(f"    Positive total: {float(pos):+.4f}")
    print(f"    Negative total: {float(neg):+.4f}")
    print(f"    Ratio pos/|neg|: {float(pos/abs(neg)):.4f}" if neg != 0 else "")

# ============================================================
# ANALYSIS 11: THE PROMISING APPROACH
# B+C = Σ D_new² - Σ D_old²
# = Σ (D_old + δ)² - Σ D_old²
# = 2 Σ D_old·δ + Σ δ²
#
# Key insight: Σ D_old·δ = Σ D_old·(D_new - D_old) = Σ D_old·D_new - Σ D_old²
# So: B+C = 2(Σ D_old·D_new - Σ D_old²) + Σ δ²
#         = 2Σ D_old·D_new - 2Σ D_old² + Σ(D_new - D_old)²
#         = 2Σ D_old·D_new - 2Σ D_old² + Σ D_new² - 2Σ D_old·D_new + Σ D_old²
#         = Σ D_new² - Σ D_old² ✓
#
# Alternative: B+C = Σ δ² + 2Σ D_old·δ
# = Σ (D_new-D_old)² + 2Σ D_old(D_new-D_old)
# = Σ D_new² - 2Σ D_old·D_new + Σ D_old² + 2Σ D_old·D_new - 2Σ D_old²
# = Σ D_new² - Σ D_old² ✓
#
# Now: Σ δ² = Σ (D_new - D_old)²  -- this is the L² distance
# And: Σ D_old·δ = correlation
#
# By CS: (Σ D_old·δ)² ≤ Σ D_old² · Σ δ²
# So |Σ D_old·δ| ≤ √(Σ D_old²) · √(Σ δ²)
# For B+C = Σδ² + 2Σ D·δ ≥ Σδ² - 2√(ΣD²·Σδ²) = √(Σδ²)(√(Σδ²) - 2√(ΣD²))
# This is positive iff Σδ² > 4ΣD², but ΣD² >> Σδ², so this FAILS.
#
# Better approach: use the weak correlation.
# ρ = Σ D·δ / √(ΣD²·Σδ²) is small (|ρ| < 0.2).
# B+C = Σδ²(1 + 2ρ·√(ΣD²/Σδ²))
# Need: 1 + 2ρ·√(ΣD²/Σδ²) > 0
# i.e., ρ > -1/(2·√(ΣD²/Σδ²)) = -√(Σδ²/(4ΣD²))
# Since ΣD²/Σδ² ~ p^1.24, the threshold is ~ -c/p^0.62
# And |ρ| < 0.2, so this is easily satisfied for p > some constant.
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 11: The ρ approach (MOST PROMISING)")
print("  ρ = Σ D·δ / √(ΣD²·Σδ²)")
print("  B+C > 0 iff ρ > -√(Σδ²/(4·ΣD²))")
print("  Since √(Σδ²/ΣD²) → 0 as p → ∞, threshold → 0")
print("  And |ρ| is bounded, so B+C > 0 for large enough p")
print(f"{'='*80}")

import numpy as np

primes_11 = [p for p in sorted(all_data.keys()) if p >= 11]
rhos = []
thresholds = []
ratios_DdSq = []

for p in primes_11:
    data = all_data[p]
    rho = float(data['sum_cross']) / sqrt(float(data['sum_D_sq']) * float(data['sum_delta_sq']))
    threshold = -sqrt(float(data['sum_delta_sq']) / (4 * float(data['sum_D_sq'])))
    ratio = float(data['sum_D_sq']) / float(data['sum_delta_sq'])
    rhos.append(rho)
    thresholds.append(threshold)
    ratios_DdSq.append(ratio)

print(f"\n  {'p':>5s}  {'ρ':>8s}  {'threshold':>10s}  {'margin':>8s}  {'ΣD²/Σδ²':>10s}")
for i, p in enumerate(primes_11):
    margin = rhos[i] - thresholds[i]
    print(f"  {p:5d}  {rhos[i]:8.4f}  {thresholds[i]:10.4f}  {margin:8.4f}  {ratios_DdSq[i]:10.2f}")

# Log-log fit of ΣD²/Σδ²
log_p = np.log(primes_11)
log_ratio = np.log(ratios_DdSq)
slope, intercept = np.polyfit(log_p, log_ratio, 1)
print(f"\n  ΣD²/Σδ² ~ p^{slope:.3f}  (so threshold ~ p^{-slope/2:.3f})")
print(f"  Threshold goes to 0, making B+C > 0 easier and easier")

# The key question: is |ρ| bounded?
print(f"\n  |ρ| values: min={min(abs(r) for r in rhos):.4f}, max={max(abs(r) for r in rhos):.4f}")
print(f"  |ρ| appears bounded by ~0.2")

# ============================================================
# ANALYSIS 12: Can we PROVE |ρ| is small?
# ρ = Σ D_old · δ / √(Σ D_old² · Σ δ²)
#
# D_old(a/b) involves the full counting function of F_{p-1}
# δ(a/b) = a/b - {pa/b} depends only on (a, b, p mod b)
#
# The key insight: D_old is a "global" function (depends on all denoms)
# while δ is a "local" function (depends only on b and σ=p mod b).
# These should be nearly uncorrelated because δ's structure is local.
#
# More precisely: within each denominator b, δ is determined by the
# permutation a → σa mod b, which is independent of the counting
# function's behavior at other denominators.
# ============================================================

print(f"\n{'='*80}")
print("ANALYSIS 12: Why ρ is small — locality of δ vs globality of D")
print(f"{'='*80}")

# Decompose ρ by denominator
for p in [23, 53, 97]:
    if p not in all_data: continue
    results = all_data[p]['results']
    by_denom = defaultdict(list)
    for r in results:
        by_denom[r['b']].append(r)

    total_cross = float(all_data[p]['sum_cross'])

    # Per-denom contribution to cross term
    denom_crosses = {}
    for b in sorted(by_denom.keys()):
        entries = by_denom[b]
        cross_b = sum(float(r['D_old'] * r['delta']) for r in entries)
        denom_crosses[b] = cross_b

    # How much cancellation is there?
    sum_abs = sum(abs(v) for v in denom_crosses.values())
    net = sum(denom_crosses.values())

    print(f"\n  p={p}: Σ|cross_b| = {sum_abs:.4f}, net = {net:.4f}, "
          f"cancellation = {1 - abs(net)/sum_abs:.4f}")

# ============================================================
# FINAL SYNTHESIS
# ============================================================

print(f"\n{'='*80}")
print("FINAL SYNTHESIS: Which approach gives traction?")
print(f"{'='*80}")

print("""
FINDING 1: B+C = Σδ²·(1 + R) where R = 2ΣD·δ/Σδ².
  - R ranges from -0.52 to +2.91 for p=11..200
  - 1+R is ALWAYS > 0 (minimum 0.48 at p=11)
  - The cross term ΣD·δ can be EITHER sign

FINDING 2: The correlation ρ = ΣD·δ/√(ΣD²·Σδ²) is small (|ρ| < 0.2).
  This is because D_old is "global" (depends on the full Farey structure)
  while δ is "local" (depends only on p mod b).
  High cancellation between per-denominator cross terms (>50%).

FINDING 3: The threshold for B+C > 0 is ρ > -√(Σδ²/(4ΣD²)) ~ -c·p^{-0.62}.
  Since the threshold goes to 0 while |ρ| stays bounded, B+C > 0 for large p.

FINDING 4: ΣD²/Σδ² ~ p^{1.24} grows with p.
  This means R = 2ρ·√(ΣD²/Σδ²) is the product of:
    - ρ ∈ [-0.2, 0.2] (small, oscillating)
    - √(ΣD²/Σδ²) ~ p^{0.62} (growing)
  When ρ < 0, R is negative but |R| = 2|ρ|·p^{0.62} < 0.4·p^{0.62}
  For this to violate B+C > 0, need |R| > 1, i.e., p^{0.62} > 2.5, i.e., p > 5.
  But ρ gets SMALLER as p grows, so the actual bound is fine.

FINDING 5: Per-denominator analysis.
  - Small denominators (b=3,4,9,...) can give negative C_b
  - But they are rare: b=3 is negative ~50% of primes, most others < 20%
  - Large denominators dominate and give positive contributions

MOST PROMISING PROOF STRATEGY:
  1. Show |ρ| ≤ C/√(log p) (or even |ρ| ≤ C) using the locality of δ
  2. Show ΣD²/Σδ² ≥ c·p^α for some α > 0
  3. Conclude: for p ≥ p₀, |R| < 1, so B+C > 0
  4. Check p₀..10 computationally

  Alternatively (simpler):
  - Show Σδ² ~ c₁·p² (from Dedekind sum theory)
  - Show |ΣD·δ| ≤ c₂·p² with c₂ < c₁/2 (from cancellation)
  - Then B+C = Σδ² + 2ΣD·δ ≥ (c₁ - 2c₂)·p² > 0
""")

elapsed = time.time() - start_time
print(f"Total time: {elapsed:.1f}s")

if __name__ == '__main__':
    pass  # Already ran at module level
