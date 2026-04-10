#!/usr/bin/env python3
"""
Factor-of-2 Analysis: Why sum E(k)^2 ≈ 2 * p * (sum D_j^2 / n)?

From the data:
  sum E(k)^2 / (p * sum_D2/n) → 2.0 as p grows

This factor of 2 comes from the step-function nature of E(x).
E(x) = A(x) - nx is a step function that jumps by +1 at each f_j and
decreases linearly with slope -n between jumps.

The integral of E(x)^2 = sum_D2/n (exactly: each step contributes D_j^2/n
to the integral via the "staircase" decomposition).

BUT the Riemann sum at the p-grid OVERESTIMATES the integral by a factor ~2
because:
- E(x) has n ~ 3p^2/pi^2 jump discontinuities
- The p-grid samples p-1 points
- At each grid point, E(k/p) is the LEFT limit (A(k) counts f <= k/p)
- The step function squared has peaks at the left side of each interval

Let's verify this rigorously and check whether the factor 2 can be PROVED.
"""

from fractions import Fraction
from math import gcd, log, pi, sqrt
import sys

def farey_sequence(N):
    fracs = set()
    fracs.add(Fraction(0, 1))
    fracs.add(Fraction(1, 1))
    for q in range(1, N + 1):
        for p_num in range(1, q + 1):
            if gcd(p_num, q) == 1:
                fracs.add(Fraction(p_num, q))
    return sorted(fracs)

def analyze_factor2(p):
    """Detailed analysis of why sum E(k)^2 ≈ 2p * int E(x)^2 dx."""
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    F_float = [float(f) for f in F_N]

    # Compute sum D_j^2
    sum_D2 = sum((j - n * F_float[j])**2 for j in range(n))
    C_W_alt = sum_D2 / n

    # Compute int E(x)^2 dx exactly (piecewise linear on intervals)
    # On interval [f_j, f_{j+1}], E(x) = j - nx (for j = 0,...,n-1 after passing f_j)
    # Wait: E(x) = A(x) - nx. Right after passing f_j, A(x) = j+1 (since f_0=0 counts).
    # At x = f_j+eps: A(x) = j+1, E(x) = j+1 - n*x
    # At x = f_{j+1}-eps: A(x) = j+1, E(x) = j+1 - n*f_{j+1} + n*eps → j+1 - n*f_{j+1}
    # D(f_j) = j - n*f_j (at the Farey point itself)

    # So on [f_j, f_{j+1}]: E(x) = (j+1) - n*x for j = 0,...,n-2
    # E(f_j) [right limit] = j+1 - n*f_j  (but A(f_j) = j+1 since f_j is included)
    # Actually A(x) = #{f in F_N : f <= x}
    # A(f_j) = j+1 (0-indexed, since f_0 = 0/1 counts)
    # Wait, let me be careful. If F_N = [f_0, f_1, ..., f_{n-1}] with f_0 = 0, f_{n-1} = 1
    # Then A(x) = #{f in F_N : f <= x} counts 0-indexed elements from 0.
    # A(f_j) = j + 1 (there are j+1 elements <= f_j)

    # Hmm actually I'm confusing myself. Let's just compute directly.

    int_E2_exact = 0.0
    for j in range(n - 1):
        # On [f_j, f_{j+1}]:
        # A(x) = j + 1 for x in (f_j, f_{j+1})  (j+1 elements: f_0,...,f_j are all <= x)
        # E(x) = (j+1) - n*x
        a = F_float[j]
        b = F_float[j + 1]
        h = b - a
        # integral of ((j+1) - n*x)^2 from a to b
        # let u = (j+1) - n*x, du = -n dx
        # at x=a: u = (j+1) - n*a, at x=b: u = (j+1) - n*b
        u_a = (j + 1) - n * a
        u_b = (j + 1) - n * b
        # integral u^2 * (-dx) from u_a to u_b = (1/n) integral u^2 du from u_b to u_a
        # = (1/n) * (u_a^3 - u_b^3) / 3
        int_E2_exact += (u_a**3 - u_b**3) / (3 * n)

    # Compare with sum_D2/n
    # D_j = j - n*f_j (0-indexed displacement)
    # Note: at f_j, E(f_j) = A(f_j) - n*f_j = (j+1) - n*f_j = D_j + 1
    # where D_j = j - n*f_j

    # Compute sum E(k)^2
    sum_E2 = 0.0
    for k in range(1, p):
        threshold = k / p
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if F_float[mid] <= threshold:
                lo = mid + 1
            else:
                hi = mid
        A_k = lo
        E_k = A_k - n * k / p
        sum_E2 += E_k ** 2

    ratio_riemann = sum_E2 / (p * int_E2_exact) if int_E2_exact > 0 else 0
    ratio_Dsum = int_E2_exact / C_W_alt if C_W_alt > 0 else 0

    return {
        'p': p, 'n': n, 'sum_D2': sum_D2, 'C_W_alt': C_W_alt,
        'int_E2': int_E2_exact, 'sum_E2': sum_E2,
        'ratio_int_vs_CW': ratio_Dsum,
        'ratio_riemann': ratio_riemann,
        'ratio_sumE2_vs_pCW': sum_E2 / (p * C_W_alt) if C_W_alt > 0 else 0,
    }

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

print("=" * 110)
print("FACTOR-OF-2 ANALYSIS")
print("=" * 110)
print()

print(f"{'p':>6} {'n':>8} {'int_E2':>14} {'sum_D2/n':>14} {'int/CW':>10} {'sumE2':>14} {'sumE2/(p*int)':>14} {'sumE2/(p*CW)':>14}")
print("-" * 110)

primes = [p for p in range(5, 300) if is_prime(p)]

for p in primes:
    r = analyze_factor2(p)
    if p <= 101 or p in [151, 199, 251]:
        print(f"{r['p']:>6} {r['n']:>8} {r['int_E2']:>14.4f} {r['C_W_alt']:>14.4f} {r['ratio_int_vs_CW']:>10.6f} {r['sum_E2']:>14.2f} {r['ratio_riemann']:>14.6f} {r['ratio_sumE2_vs_pCW']:>14.6f}")

print()
print("=" * 80)
print("KEY OBSERVATION")
print("=" * 80)
print("""
int E(x)^2 dx ≈ sum_D2/n = C_W_alt  (ratio → 1 as N grows)
sum E(k)^2 ≈ 2 * p * int E(x)^2 dx  (ratio → 2 as p grows)

So: sum E(k)^2 ≈ 2 * p * C_W_alt

The factor of 2 comes from the Riemann sum of a step function.
E(x)^2 is a sum of parabolic arcs. The Riemann sum at the p-grid
samples E at points that are SYSTEMATICALLY biased toward the
high side of each arc (because E(x) = A(x) - nx includes the jump
at the left endpoint of each Farey interval).

This is analogous to the well-known "midpoint vs left-endpoint" bias
for Riemann sums of monotone functions, amplified by the O(n) jump
discontinuities.
""")

# Now the critical question: can we PROVE sum E(k)^2 >= c * p * C_W for some c > 0?
print("=" * 80)
print("LOWER BOUND ANALYSIS: Can we prove sum E(k)^2 >= c * p?")
print("=" * 80)
print()
print("From C_W >= 1/4 and the Riemann sum relation:")
print("  sum E(k)^2 ≈ 2 * p * C_W_alt >= 2 * p * (1/4) = p/2")
print()
print("But the factor 2 is NOT proved — it's the problematic step.")
print("Without the factor 2, we only get:")
print("  sum E(k)^2 >= p * int E(x)^2 dx * (1 - error)")
print("  where the error comes from Riemann sum approximation")
print()
print("For the LOWER bound, we need the Riemann sum to EXCEED the integral.")
print("This is true for left-endpoint sums of DECREASING functions on each subinterval.")
print()

# Check: on each interval between consecutive grid points k/p and (k+1)/p,
# is E(x)^2 decreasing from left to right?
# E(x) = A(x) - nx is DECREASING between Farey points (slope -n)
# So |E(x)| could be increasing or decreasing depending on sign.
# E(x)^2 = (A(x)-nx)^2 where A(x) is constant between Farey points.

# The key: E(k/p)^2 (left endpoint of [k/p, (k+1)/p]) vs average of E^2 on that interval.
# Since E is piecewise linear (constant A, decreasing -nx), E^2 is a parabola opening UP.
# The minimum of E^2 on any constant-A interval is at x = A/n (where E crosses zero).
# The left endpoint value E(k/p)^2 may be above or below the average.

# Actually, for a parabola (a - bx)^2 on [x0, x1]:
# average = a^2 - ab(x0+x1) + b^2(x0^2+x0*x1+x1^2)/3
# left value = (a-bx0)^2
# The left value exceeds the average iff the function is "mostly decreasing" there.

# This is getting complicated. Let's just check the ratio.

print("Check: is sum E(k)^2 >= p * int E^2 for all primes?")
print(f"{'p':>6} {'sumE2':>14} {'p*intE2':>14} {'ratio':>10} {'exceeds?':>10}")
print("-" * 60)

all_exceed = True
for p in primes:
    r = analyze_factor2(p)
    exceeds = r['sum_E2'] >= p * r['int_E2']
    if not exceeds:
        all_exceed = False
    if p <= 101 or not exceeds:
        print(f"{r['p']:>6} {r['sum_E2']:>14.2f} {p*r['int_E2']:>14.2f} {r['ratio_riemann']:>10.4f} {'YES' if exceeds else '**NO**':>10}")

print(f"\nsum E(k)^2 >= p * int E^2 for all primes: {all_exceed}")

# Even without factor 2, does sum E(k)^2 >= p/4 hold?
print()
print("Does sum E(k)^2 >= p/4 hold (weakest bound from C_W >= 1/4)?")
print(f"{'p':>6} {'sumE2':>14} {'p/4':>14} {'ratio':>10} {'holds?':>8}")
print("-" * 60)
for p in primes[:20]:
    r = analyze_factor2(p)
    holds = r['sum_E2'] >= p / 4
    print(f"{r['p']:>6} {r['sum_E2']:>14.2f} {p/4:>14.2f} {r['sum_E2']/(p/4):>10.4f} {'YES' if holds else 'NO':>8}")

# Now: what order is actually NEEDED?
print()
print("=" * 80)
print("WHAT ORDER IS NEEDED FOR GAP 2?")
print("=" * 80)
print()
print("In the 4-term decomposition (W-scale), for DeltaW(p) < 0 we need:")
print("  D'/n'^2 + C'/n'^2 > A'/n'^2")
print()
print("Where:")
print("  D' (D-scale) = sum (E(k) + k/p)^2 = sum E^2 + 2*sum(k/p)*E + sum(k/p)^2")
print("  The dominant term is sum E(k)^2 ~ 0.066 * p^2 * log p")
print("  Correction 2*sum(k/p)*E is O(p^(3/2)) [since E(k) has mean 0, RMS ~ sqrt(p*logp)]")
print("  sum(k/p)^2 = (p-1)(2p-1)/(6p) ≈ p/3")
print()
print("  A' (D-scale) = sum over old fracs of (D_new^2 - D_old^2)")
print("  This is the dilution term from adding p-1 new fractions.")
print("  Each old frac at position j gets shifted to position j + #{new fracs before it}")
print("  A' scales as n * (p-1)^2 / n^2 * something... let's compute directly")
print()

# Compute A' vs D' directly
print(f"{'p':>6} {'D_prime':>14} {'A_prime':>14} {'D-A':>14} {'C_prime':>14} {'net':>14} {'DeltaW':>14}")
print("-" * 100)

for p in primes:
    if p > 101:
        continue
    N = p - 1
    F_N = farey_sequence(N)
    F_p = farey_sequence(p)
    n = len(F_N)
    n_new = len(F_p)
    F_N_set = set(F_N)

    # W(N) and W(p) in d-scale (f_j - j/n)^2
    W_old = sum((float(f) - j / n)**2 for j, f in enumerate(F_N))
    W_new = sum((float(f) - j / n_new)**2 for j, f in enumerate(F_p))
    DeltaW = W_new - W_old

    # D' in D-scale: sum over NEW fractions of (rank_in_Fp - n'*f)^2
    D_prime = 0.0
    # A' in D-scale: sum over OLD fractions of [(rank_in_Fp - n'*f)^2 - (rank_in_FN - n*f)^2]
    A_prime = 0.0
    j_old = 0
    for j_new, f in enumerate(F_p):
        D_new = j_new - n_new * float(f)
        if f in F_N_set:
            D_old = j_old - n * float(f)
            A_prime += D_new**2 - D_old**2
            j_old += 1
        else:
            D_prime += D_new**2

    # The four terms (in W-scale = d-scale):
    # DeltaW = (1/n'^2)*[A' + D'] - W_old * (1 - n^2/n'^2)
    # Wait, let me just use the direct decomposition:
    # n'^2 * W(p) = sum over all f in F_p of (rank - n'*f)^2
    #             = sum over old f of (rank_new - n'*f)^2 + sum over new f of (rank_new - n'*f)^2
    #             = [sum over old f of (rank_old - n*f)^2 + A'] + D'
    #             = n^2 * W(N) + A' + D'
    # So: n'^2 * W(p) - n^2 * W(N) = A' + D'
    # DeltaW = W(p) - W(N) = (A' + D')/n'^2 - W(N)*(n'^2 - n^2)/n'^2
    # i.e. DeltaW = [A' + D' - W(N)*(n'^2 - n^2)] / n'^2

    check = (A_prime + D_prime) / n_new**2 - W_old * (n_new**2 - n**2) / n_new**2
    # This should equal DeltaW

    # For the sign theorem, DeltaW < 0 means:
    # A' + D' < W(N) * (n'^2 - n^2)
    # Or equivalently: D' > |A'| - W(N)*(n'^2-n^2)...
    # Actually let's just look at what drives DeltaW negative

    C_prime = -W_old * (n_new**2 - n**2) / n_new**2  # The "dilution" of W_old
    net = (A_prime + D_prime) / n_new**2 + C_prime

    print(f"{p:>6} {D_prime:>14.2f} {A_prime:>14.2f} {D_prime-abs(A_prime):>14.2f} {C_prime:>14.8f} {net:>14.8f} {DeltaW:>14.8f}")

print()
print("=" * 80)
print("FINAL ANALYSIS")
print("=" * 80)
print("""
CRITICAL FINDING: The chain C_W >= 1/4 --> Gap 2 closure DOES NOT WORK directly.

Here's why:

1. C_W >= 1/4 gives sum D_j^2 >= n/4 (PROVED, Cauchy-Schwarz)

2. int_0^1 E(x)^2 dx ≈ sum D_j^2 / n = C_W_alt (PROVED, exact integral decomposition)
   So int E^2 >= 1/4.

3. sum E(k)^2 ≈ 2 * p * int E^2  (OBSERVED, factor of 2 is EMPIRICAL)
   The factor 2 converges from below: ratio = 0.44 at p=5, 2.00 at p=499.

4. Even WITH factor 2: sum E(k)^2 ≈ 2p * C_W_alt ≈ 2p * (constant ~ 0.5-0.7)
   This is O(p), not O(p^2).

5. But sum E(k)^2 actually grows as p^2 * log(p) * 0.066!
   The discrepancy between "p * C_W_alt" and "p^2 * logp * 0.066" means
   C_W_alt is NOT a constant — it grows as p * logp * 0.066 / 2 ≈ 0.033 * p * logp.

WAIT — C_W_alt = sum_D2/n, and n ~ 3p^2/pi^2. So sum_D2 ~ n * C_W_alt.
If sum E^2 ~ 2p * C_W_alt and sum E^2 ~ 0.066 * p^2 * logp, then
C_W_alt ~ 0.033 * p * logp, which means sum_D2 ~ n * 0.033 * p * logp ~ 0.01 * p^3 * logp.

Let me verify: C_W = N * W(N), where W(N) = sum d_j^2.
C_W_alt = sum D_j^2 / n where D_j = j - n*f_j.
Since d_j = f_j - j/n = -D_j/n, sum d_j^2 = sum D_j^2 / n^2.
So C_W = N * sum D_j^2 / n^2 = N * C_W_alt / n.
Since n ~ 3N^2/pi^2: C_W = N * C_W_alt * pi^2/(3N^2) = pi^2 * C_W_alt / (3N).

If C_W ~ 0.66 (from data at N~100K), then C_W_alt ~ 0.66 * 3N/pi^2 ~ 0.2 * N.
And sum_D2 = n * C_W_alt ~ (3N^2/pi^2) * 0.2N = 0.06 * N^3.

So the relationship is:
  sum E(k)^2 ~ 2p * C_W_alt ~ 2p * (0.2 * N) = 0.4 * p * N = 0.4 * p * (p-1)
  ~ 0.4 * p^2

And 0.066 * p^2 * logp vs 0.4 * p^2: these differ by logp/6 ≈ logp * 0.17.
This checks out! C_W_alt grows as c * N * logN, making sum E^2 ~ p^2 * logp.

THE REAL PICTURE:
- C_W (the normalized quantity) is O(1), hovering near 0.66
- C_W_alt = sum D^2/n grows as c*N (since C_W_alt = n * C_W / N ~ 3N*C_W/pi^2)
- sum E^2 ~ 2p * C_W_alt ~ 2p * (3N*C_W/pi^2) = (6/pi^2) * C_W * p * N ~ (6/pi^2) * 0.66 * p^2
  ≈ 0.4 * p^2

So C_W >= 1/4 gives: sum E^2 >= (6/pi^2) * (1/4) * p * N = (3/(2pi^2)) * p^2 ≈ 0.152 * p^2

THIS IS EXACTLY THE CLAIMED BOUND! 0.152 * p^2!

But wait — from the data, this fails for small p (p <= 17). It only works for p >= 19.
""")

# Verify the exact chain
print("=" * 80)
print("EXACT CHAIN VERIFICATION")
print("=" * 80)
print()
print("Chain: sum E^2 ≈ 2p * C_W_alt = 2p * (n*C_W/N) = 2*C_W*(p*n/N)")
print("Since n ~ 3N^2/pi^2 and N = p-1: p*n/N ≈ 3p^2/pi^2")
print("So sum E^2 ≈ 2 * C_W * 3p^2/pi^2 = (6/pi^2) * C_W * p^2")
print("With C_W >= 1/4: sum E^2 >= (6/(4*pi^2)) * p^2 = (3/(2pi^2)) * p^2 ≈ 0.1520 * p^2")
print()

c_target = 3 / (2 * pi**2)
print(f"Theoretical constant: 3/(2*pi^2) = {c_target:.6f}")
print()

print(f"{'p':>6} {'sumE2/p^2':>12} {'>= 0.152?':>10} {'2*CW*3/pi^2':>14} {'exact CW':>10} {'CW_alt':>12} {'2p*CWalt/p^2':>14}")
print("-" * 90)

for p in primes:
    r = analyze_factor2(p)
    CW = (p - 1) * r['C_W_alt'] / r['n']  # C_W = N * C_W_alt / n = N * sum_d^2
    # Actually C_W = N * sum (f_j - j/n)^2
    N = p - 1
    CW_correct = N * r['int_E2']  # Wait, int_E2 ≈ C_W_alt/1 ... no
    # Let me recompute: C_W = N * W(N) = N * sum d_j^2
    # sum d_j^2 = sum D_j^2 / n^2 = C_W_alt / n
    # C_W = N * C_W_alt / n
    CW_val = N * r['C_W_alt'] / r['n']
    predicted = 2 * CW_val * 3 / pi**2
    actual = r['sum_E2'] / p**2
    ratio = 2 * p * r['C_W_alt'] / p**2

    if p <= 101 or p in [151, 199, 251]:
        print(f"{p:>6} {actual:>12.6f} {'YES' if actual >= c_target else 'NO':>10} {predicted:>14.6f} {CW_val:>10.4f} {r['C_W_alt']:>12.4f} {ratio:>14.6f}")

print()
print("NOTE: The chain has 3 links:")
print("  Link 1: C_W(N) >= 1/4 [PROVED for N >= 16]")
print("  Link 2: sum E^2 ≈ 2 * (3/pi^2) * C_W * p^2 [factor 2 is EMPIRICAL]")
print("  Link 3: therefore sum E^2 >= (3/(2pi^2)) * p^2 ≈ 0.152 * p^2")
print()
print("Link 2 is the WEAK LINK. The factor 2 is observed numerically to approach 2")
print("but has no analytical proof yet.")
print()
print("WITHOUT the factor 2:")
print("  sum E^2 >= (3/(pi^2)) * C_W * p^2 * (1/2) [only getting half]")
print("  ... actually without factor 2, we only get sum E^2 >= p * C_W_alt >= p/4")
print("  which is order p, not p^2.")
print()
print("The factor 2 is what promotes the bound from O(p) to O(p^2).")
print("This is the CENTRAL GAP in the chain.")
