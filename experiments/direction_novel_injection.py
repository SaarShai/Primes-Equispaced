#!/usr/bin/env python3
"""
NOVEL DISCOVERY: The Injection Principle implies EVERY gap gets exactly 0 or 1 fraction.

From Direction B, we found that filled_gaps = p-1 ALWAYS.
This means each of the p-1 new fractions k/p goes into a DISTINCT gap.
No gap receives 2 or more new fractions!

This is actually the INJECTION PRINCIPLE made precise:
For prime p, the map k → gap(k/p) is INJECTIVE from {1,...,p-1} to gaps of F_{p-1}.

WHY? Because consecutive Farey fractions a/b, c/d satisfy bc - ad = 1.
The interval (a/b, c/d) contains at most one k/p iff p/(bd) ≤ 2.
But for Farey neighbors, bd > p-1 always (since b,d ≤ p-1 and b+d > p-1).
Actually... bd can be as small as 1·2 = 2 (for the gap 0/1, 1/(p-1)).
So this argument doesn't work directly.

Let me investigate more carefully.
"""

from math import gcd
from fractions import Fraction

def farey_generator(N):
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_list(N):
    return list(farey_generator(N))

# For each prime p, examine gaps that receive >1 new fraction
print("=" * 70)
print("GAP FILLING ANALYSIS: Do any gaps get >1 new fraction?")
print("=" * 70)

for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
          101, 127, 149, 151, 173, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]:
    F = farey_list(p - 1)
    n = len(F)
    
    max_in_gap = 0
    multi_gaps = 0
    
    for i in range(n - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        # Count fractions k/p in (a/b, c/d)
        # k/p > a/b ⟺ k > pa/b (since p,b > 0)
        # k/p < c/d ⟺ k < pc/d
        k_lo = (p * a) // b + 1  # smallest k with k/p > a/b
        # For upper: k < pc/d. Since b,c,d coprime stuff...
        # k/p < c/d ⟺ kd < pc ⟺ k < pc/d. 
        # If d | pc: k ≤ pc/d - 1. Else: k ≤ floor(pc/d).
        # Since p prime, d | pc iff d | c (for d < p). d|c iff c=d (since c ≤ d). 
        # c=d means c/d = 1, last fraction.
        if c == d:  # c/d = 1
            k_hi = p - 1  # k < p
        else:
            k_hi = (p * c - 1) // d  # floor((pc-1)/d) = largest k with kd < pc
        
        count = max(0, k_hi - k_lo + 1)
        if count > max_in_gap:
            max_in_gap = count
        if count > 1:
            multi_gaps += 1
            if p <= 97:
                print(f"  p={p}: gap ({a}/{b}, {c}/{d}), bd={b*d}, "
                      f"gets {count} fractions (k={k_lo}..{k_hi})")
    
    total = sum(max(0, ((p * F[i+1][0] - 1) // F[i+1][1] if F[i+1][0] != F[i+1][1] else p-1)
                     - ((p * F[i][0]) // F[i][1] + 1) + 1)
                for i in range(n - 1))
    
    if multi_gaps > 0 or p <= 97:
        print(f"  p={p:3d}: max_per_gap={max_in_gap}, multi_gap_count={multi_gaps}, "
              f"|F_{{p-1}}|={n}, new_fracs={p-1}")

# ============================================================
# THEOREM: The max fractions per gap
# ============================================================
print("\n" + "=" * 70)
print("THEOREM: Max fractions per gap as function of p")
print("=" * 70)

# For Farey neighbors a/b, c/d with bc - ad = 1:
# The gap (a/b, c/d) has width 1/(bd).
# Number of integers k in (pa/b, pc/d) is:
# floor(pc/d) - floor(pa/b) = floor(pc/d) - floor(pa/b).
# Since bc - ad = 1: pc/d - pa/b = p(bc-ad)/(bd) = p/(bd).
# So number of integers ≈ p/(bd).
# 
# For the gap to receive ≥ 2 fractions: need p/(bd) ≥ 2, i.e., bd ≤ p/2.
# This happens when BOTH b and d are small (≤ √(p/2)).
#
# For the gap (0/1, 1/(p-1)): bd = 1·(p-1) = p-1. Gets floor(p/(p-1)) = 1 fraction.
# For the gap (1/(p-1), 1/(p-2)): bd = (p-1)(p-2). Gets 0 fractions for large p.
# For the gap (0/1, 1/N) where N = p-1: gets 1 fraction (k=1, since 1/p < 1/(p-1)).
#
# The SMALLEST bd gaps are near a/b ≈ 1/2 with small b,d.
# E.g., near 1/2: the Farey neighbors are (mediant stuff)...

# Let me look at which gaps get multiple fractions:
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
    F = farey_list(p - 1)
    n = len(F)
    
    for i in range(n - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        k_lo = (p * a) // b + 1
        if c == d:
            k_hi = p - 1
        else:
            k_hi = (p * c - 1) // d
        
        count = max(0, k_hi - k_lo + 1)
        if count >= 2:
            print(f"  p={p:3d}: gap ({a}/{b}, {c}/{d}), bd={b*d:4d}, p/bd={p/(b*d):.2f}, "
                  f"gets {count} fracs, k={k_lo}..{k_hi}")

# ============================================================
# KEY FINDING: Exact characterization
# ============================================================
print("\n" + "=" * 70)
print("EXACT CHARACTERIZATION of multi-fraction gaps")
print("=" * 70)

# For Farey neighbors (a/b, c/d) with bc-ad=1:
# Number of k/p in gap = floor(pc/d) - floor(pa/b)  [when neither is integer]
# = floor((pa+p)/(bd) + pa/b) - floor(pa/b)  [using c/d = (a+?)/? from mediant]
# Actually, since bc-ad=1: c = (1+ad)/b [integer] and d's relationship...
# Better: pc/d - pa/b = p/(bd). So count = floor(pa/b + p/(bd)) - floor(pa/b).
# By the formula for floor sums: this equals floor(p/(bd) + {pa/b}) where {·} is fractional part.
# So count = floor(p/(bd) + {pa/b}).
#
# count ≥ 2 ⟺ p/(bd) + {pa/b} ≥ 2 ⟺ p/(bd) ≥ 2 - {pa/b} > 1.
# So need bd < p. More precisely bd < p and the fractional part is favorable.
#
# count = 0 ⟺ p/(bd) + {pa/b} < 1 ⟺ p/(bd) < 1 - {pa/b} < 1.
# So bd > p guarantees count ∈ {0, 1}.
# For bd = p: count depends on {pa/b}.

# THEOREM: For prime p and Farey neighbors (a/b,c/d) in F_{p-1} with bc-ad=1:
# The number of fractions k/p in the gap equals floor(p/(bd) + {pa/b}).
# 
# Since {pa/b} ∈ [0,1) (and ≠ 0 since gcd(p,b)=1 for 0<a<b):
# - If bd ≥ p: count ∈ {0, 1}
# - If bd < p: count = floor(p/(bd) + {pa/b}) ≥ 1
# - If bd ≤ p/2: count ≥ 2

# Verify this formula:
print("\nVerifying gap formula: count = floor(p/(bd) + {pa/b}):")
for p in [11, 13, 17, 23, 29, 37]:
    F = farey_list(p - 1)
    all_correct = True
    for i in range(len(F) - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        # Direct count
        k_lo = (p * a) // b + 1
        if c == d:
            k_hi = p - 1
        else:
            k_hi = (p * c - 1) // d
        count_direct = max(0, k_hi - k_lo + 1)
        
        # Formula count
        if b == 1 and a == 0:
            frac_part = 0
        else:
            frac_part = (p * a % b) / b  # {pa/b}
        
        count_formula = int(p / (b * d) + frac_part)
        
        if count_direct != count_formula:
            all_correct = False
            print(f"  MISMATCH p={p}: ({a}/{b},{c}/{d}), direct={count_direct}, formula={count_formula}")
    
    if all_correct:
        print(f"  p={p}: all {len(F)-1} gaps correct ✓")

# ============================================================
# NOVEL THEOREM: Total multi-fraction gaps count
# ============================================================
print("\n" + "=" * 70)
print("NOVEL: Number of multi-fraction gaps grows as Σ_{bd<p} 1")
print("=" * 70)

# The number of Farey gaps (a/b,c/d) with bd < p is related to
# the "Farey structure below height √p".
# Specifically, gaps with bd < p come from fractions with b·d < p,
# meaning both b,d < √p (roughly).

for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 89, 97,
          101, 127, 149, 173, 197, 211, 251, 307, 401, 499]:
    F = farey_list(p - 1)
    
    multi = 0
    total_extra = 0
    small_bd = 0
    
    for i in range(len(F) - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        k_lo = (p * a) // b + 1
        if c == d:
            k_hi = p - 1
        else:
            k_hi = (p * c - 1) // d
        count = max(0, k_hi - k_lo + 1)
        
        if b * d < p:
            small_bd += 1
        if count >= 2:
            multi += 1
            total_extra += count - 1
    
    print(f"  p={p:4d}: multi-gaps={multi:4d}, bd<p gaps={small_bd:4d}, "
          f"extra fracs={total_extra:4d}, √p={p**0.5:.1f}")

# ============================================================
# KEY INSIGHT: Injection principle is EXACT
# ============================================================
print("\n" + "=" * 70)
print("KEY INSIGHT: Most gaps that get fractions get EXACTLY 1")
print("=" * 70)

# When p is prime and we insert k/p for k=1,...,p-1:
# Total new fractions = p-1.
# Total gaps with ≥1 fraction = (p-1 - extra_fracs) + multi_gaps... no.
# Actually: filled_gaps = p-1 - total_extra. Let me verify.

for p in [11, 23, 37, 53, 97, 199]:
    F = farey_list(p - 1)
    
    filled = 0
    extra = 0
    for i in range(len(F) - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        k_lo = (p * a) // b + 1
        if c == d:
            k_hi = p - 1
        else:
            k_hi = (p * c - 1) // d
        count = max(0, k_hi - k_lo + 1)
        
        if count >= 1:
            filled += 1
        if count >= 2:
            extra += count - 1
    
    n_gaps = len(F) - 1
    print(f"  p={p:4d}: filled={filled}, extra={extra}, total_new={filled+extra}, "
          f"expected={p-1}, gaps={n_gaps}")
    assert filled + extra == p - 1, f"Sum mismatch at p={p}!"

print("\nVerified: filled + extra = p-1 always ✓")
print("The p-1 new fractions are distributed among the gaps,")
print("with most gaps getting exactly 1 fraction.")

