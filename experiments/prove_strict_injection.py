#!/usr/bin/env python3
"""
THEOREM (Strict Injection): For prime p ≥ 3, each gap of F_{p-1} receives 
AT MOST ONE new fraction k/p.

PROOF:
Let (a/b, c/d) be consecutive fractions in F_{p-1}, so bc - ad = 1.
The new fractions k/p in (a/b, c/d) satisfy a/b < k/p < c/d.

The number of such k equals floor(pc/d) - ceil(pa/b) + 1
= floor(pc/d) - floor(pa/b + 1) + 1  [when pa/b is not integer]
= floor(pc/d) - floor(pa/b) - 1 + 1
= floor(pc/d) - floor(pa/b).

Now pc/d - pa/b = p(bc - ad)/(bd) = p/(bd).

Since (a/b, c/d) are consecutive in F_{p-1}, we have b, d ≤ p-1 and b + d > p-1.
(The Farey neighbor condition: b + d > N iff a/b, c/d are consecutive in F_N.)

So b + d ≥ p, which means bd ≥ b(p-b).
For 1 ≤ b ≤ p-1: b(p-b) ≥ p-1 (minimum at b=1 or b=p-1).

Actually, MORE PRECISELY:
b + d > p - 1 (consecutive in F_{p-1}) ⟹ b + d ≥ p.
So d ≥ p - b.
Then bd ≥ b(p - b).

For b ≥ 1: b(p-b) = bp - b² ≥ p - 1 (at b=1: p-1; at b=p-1: p-1).
Minimum is at b=1 or b=p-1, giving bd ≥ p-1.

So p/(bd) ≤ p/(p-1) = 1 + 1/(p-1) < 2 for p ≥ 3.

The number of k values = floor(pc/d) - floor(pa/b) ≤ floor(p/(bd) + {pa/b}) 
where {pa/b} < 1.

Since p/(bd) < 2 and {pa/b} < 1:
p/(bd) + {pa/b} < 3.

So count ≤ 2. But can it equal 2?
Count = 2 ⟺ p/(bd) + {pa/b} ≥ 2
⟺ {pa/b} ≥ 2 - p/(bd).

Since p/(bd) ≤ p/(p-1) = 1 + 1/(p-1):
Need {pa/b} ≥ 2 - 1 - 1/(p-1) = 1 - 1/(p-1) = (p-2)/(p-1).

So {pa/b} ≥ (p-2)/(p-1).

{pa/b} = (pa mod b)/b. For this to be ≥ (p-2)/(p-1):
(pa mod b)/b ≥ (p-2)/(p-1).

This requires pa mod b ≥ b(p-2)/(p-1).

CAN THIS HAPPEN? Let's check with bd = p-1 (minimum case).
Then b + d = p (since bd = p-1 forces specific b,d).
Wait, b + d ≥ p and bd = p-1.
b + d ≥ p and bd = p-1.
b and d are roots of x² - (b+d)x + (p-1) = 0.
For b+d = p: x² - px + (p-1) = 0 → x = (p ± √(p²-4p+4))/2 = (p ± (p-2))/2.
So b=1, d=p-1 or b=p-1, d=1.

For (b,d) = (1, p-1): the gap is (a/1, c/(p-1)) with a·(p-1) = bc - 1... 
wait, (a,b) = (a,1) means a/b = a, so a ∈ {0,1}.
If a=0, b=1: the gap is (0/1, 1/(p-1)). Then c=1, d=p-1.
p/(bd) = p/(p-1) = 1 + 1/(p-1).
{pa/b} = {0} = 0.
Count = floor(1 + 1/(p-1) + 0) = 1. ✓

If a=1, b=1: gap is (1/1, ...) — but 1/1 is the last fraction. No gap after.

For (b,d) = (p-1, 1): gap is (a/(p-1), c/1) where c/1 = 1.
So c=1, d=1. Then bc-ad=1 → (p-1)·1 - a·1 = 1 → a = p-2.
Gap is ((p-2)/(p-1), 1/1). p/(bd) = p/(p-1).
{pa/b} = {p(p-2)/(p-1)} = {(p²-2p)/(p-1)} = {p - p/(p-1)} = {-p/(p-1)} = {-1-1/(p-1)}
= {-(p-1+1)/(p-1)} = {-1 - 1/(p-1)} = 1 - 1/(p-1) = (p-2)/(p-1).

Wait! So {pa/b} = (p-2)/(p-1) EXACTLY at this gap.
And p/(bd) + {pa/b} = p/(p-1) + (p-2)/(p-1) = (p + p - 2)/(p-1) = (2p-2)/(p-1) = 2.

So count = floor(2) = 2??? But our computation showed count = 1!

Let me check directly: gap is ((p-2)/(p-1), 1/1).
k/p > (p-2)/(p-1) ⟺ k(p-1) > p(p-2) ⟺ k > p(p-2)/(p-1) = p - 2p/(p-1) = p - 2 - 2/(p-1).
Since k is integer: k ≥ p-2 (for p ≥ 3, 2/(p-1) < 1).
k/p < 1 ⟺ k < p, so k ≤ p-1.
k ∈ {p-2, p-1} — that's 2 fractions!

BUT WAIT: Is (p-2)/p in F_p? Only if gcd(p-2, p) = 1.
Since p is prime: gcd(p-2, p) = 1 always. ✓
And (p-1)/p: gcd(p-1, p) = 1. ✓

So the gap ((p-2)/(p-1), 1/1) receives BOTH (p-2)/p and (p-1)/p.
That's 2 fractions in one gap!

But our COMPUTATION showed multi_gaps = 0 for all tested primes!
Something is wrong with the computation or the analysis.

Let me debug:
"""

from math import gcd
from fractions import Fraction

def farey_list(N):
    a, b, c, d = 0, 1, 1, N
    result = [(a, b)]
    while c <= N:
        result.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return result

p = 11
F = farey_list(p - 1)
print(f"Last 5 fractions in F_{p-1}:")
for a, b in F[-5:]:
    print(f"  {a}/{b} = {a/b:.6f}")

print(f"\nLast gap: ({F[-2][0]}/{F[-2][1]}, {F[-1][0]}/{F[-1][1]})")

a_gap, b_gap = F[-2]
c_gap, d_gap = F[-1]
print(f"bc - ad = {b_gap * c_gap - a_gap * d_gap}")
print(f"b·d = {b_gap * d_gap}")
print(f"p/(bd) = {p / (b_gap * d_gap):.6f}")

# Direct count for this gap
print(f"\nFractions k/{p} in ({a_gap}/{b_gap}, {c_gap}/{d_gap}):")
for k in range(1, p):
    f_k = Fraction(k, p)
    f_lo = Fraction(a_gap, b_gap)
    f_hi = Fraction(c_gap, d_gap)
    if f_lo < f_k < f_hi:
        print(f"  k={k}: {k}/{p} = {float(f_k):.6f}")

# Now let me also check the gap before (p-2)/(p-1) in F_{p-1}:
# What is the Farey neighbor before (p-2)/(p-1)?
for i in range(len(F) - 1):
    if F[i+1] == (p-2, p-1):
        print(f"\nGap before ({p-2}/{p-1}): ({F[i][0]}/{F[i][1]}, {p-2}/{p-1})")
        a_g, b_g = F[i]
        # Count fractions in this gap
        for k in range(1, p):
            f_k = Fraction(k, p)
            f_lo = Fraction(a_g, b_g)
            f_hi = Fraction(p-2, p-1)
            if f_lo < f_k < f_hi:
                print(f"  k={k}: {k}/{p}")

# AH WAIT - is (p-2)/(p-1) even in F_{p-1}? Only if p-2 < p-1 and gcd(p-2,p-1)=1.
print(f"\ngcd({p-2}, {p-1}) = {gcd(p-2, p-1)}")
# gcd(p-2, p-1) = gcd(p-2, 1) = 1 for all p. So yes, always in F_{p-1}.

# The issue: my computation code had a bug for the LAST gap.
# Let me recheck:
print(f"\n\n=== DEBUGGING gap count for p={p} ===")
for i in range(len(F) - 1):
    a, b = F[i]
    c, d = F[i + 1]
    
    # Count k/p in (a/b, c/d) exactly using Fraction
    count = 0
    fracs_in_gap = []
    for k in range(1, p):
        f_k = Fraction(k, p)
        if Fraction(a, b) < f_k < Fraction(c, d):
            count += 1
            fracs_in_gap.append(k)
    
    # My original code
    k_lo = (p * a) // b + 1
    if c == d:  # c/d = 1
        k_hi = p - 1
    else:
        k_hi = (p * c - 1) // d
    
    count_code = max(0, k_hi - k_lo + 1)
    
    if count != count_code:
        print(f"  BUG at gap ({a}/{b}, {c}/{d}): exact={count}, code={count_code}, "
              f"k_lo={k_lo}, k_hi={k_hi}, fracs={fracs_in_gap}")
    elif count >= 2:
        print(f"  MULTI at ({a}/{b}, {c}/{d}): {count} fracs, k={fracs_in_gap}")

# NOW CHECK: p=11, gap (9/10, 1/1). 
# Exact: k/11 > 9/10 ⟺ 10k > 99 ⟺ k > 9.9 ⟺ k ≥ 10.
# k/11 < 1 ⟺ k < 11 ⟺ k ≤ 10.
# So k = 10. ONE fraction. ✓
# 
# What about k=11? That's 11/11 = 1 = c/d. But k ≤ p-1 = 10.
# 
# My analysis was WRONG: (p-2)/p and (p-1)/p both in (a/b, 1/1)
# only if a/b < (p-2)/p.
# The second-to-last fraction in F_{p-1} is (p-2)/(p-1).
# Is (p-2)/(p-1) < (p-2)/p? Yes! Since p-1 < p → 1/(p-1) > 1/p → (p-2)/(p-1) > (p-2)/p.
# WRONG! (p-2)/(p-1) > (p-2)/p. So the gap ((p-2)/(p-1), 1) CONTAINS (p-2)/p.
# And also (p-1)/p.
# So the gap gets TWO fractions: (p-2)/p and (p-1)/p.

# But wait, let me verify for p=11:
# F_10: ..., 9/10, 1/1
# Gap (9/10, 1/1). Fractions k/11: k/11 > 9/10 and k < 11.
# 10k > 99 → k ≥ 10. And k ≤ 10. So k=10 only. ONE fraction.
# 
# Why not k=9? 9/11 = 0.818... < 9/10 = 0.9. Not in gap.
# Why does (p-2)/(p-1) = 9/10 and (p-2)/p = 9/11 = 0.818 < 9/10?
# Because 9/11 < 9/10! The fraction (p-2)/p is NOT in the gap ((p-2)/(p-1), 1/1).
# My error: (p-2)/p < (p-2)/(p-1) always (since p > p-1 → 1/p < 1/(p-1)).
# So (p-2)/p is in an EARLIER gap, not in the last gap.

# Let me recheck the general formula:
# Gap ((p-2)/(p-1), 1/1):
# k/p > (p-2)/(p-1) ⟺ k(p-1) > p(p-2) ⟺ kp - k > p² - 2p ⟺ k > (p²-2p)/(p-1) = p - 2p/(p-1).
# Hmm wait: p(p-2)/(p-1) = (p²-2p)/(p-1).
# For p=11: (121-22)/10 = 99/10 = 9.9. So k ≥ 10. And k ≤ p-1 = 10. ONE fraction.
# For p=5: (25-10)/4 = 15/4 = 3.75. k ≥ 4. k ≤ 4. ONE fraction.
# For p=101: (10201-202)/100 = 9999/100 = 99.99. k ≥ 100. k ≤ 100. ONE fraction.
# For p=3: (9-6)/2 = 3/2 = 1.5. k ≥ 2. k ≤ 2. ONE fraction.

# In general: p(p-2)/(p-1) = p - 2p/(p-1) = p - 2 - 2/(p-1).
# Since 0 < 2/(p-1) < 1 for p ≥ 4: k ≥ p-2+1 = p-1 and k ≤ p-1. ONE fraction.
# For p=3: 2/(p-1) = 1, so p-2-2/(p-1) = 3-2-1 = 0. k ≥ 1. k ≤ 2. TWO fractions!

print(f"\n\n=== THEOREM PROOF ===")
print(f"For p ≥ 5 prime:")
print(f"The last gap ((p-2)/(p-1), 1/1) receives exactly 1 fraction: (p-1)/p.")
print(f"Proof: k/p > (p-2)/(p-1) ⟺ k > p(p-2)/(p-1) = p - 2 - 2/(p-1).")
print(f"For p ≥ 5: 0 < 2/(p-1) < 1, so the smallest integer k is p-1.")
print(f"And k ≤ p-1. So exactly 1 fraction.")
print(f"")
print(f"For p=3: the gap (1/2, 1/1) receives k=1 AND k=2 (i.e., 1/3 and 2/3).")
print(f"But wait: 1/3 = 0.333... < 1/2 = 0.5. So 1/3 is NOT in (1/2, 1).")
print(f"Only k=2: 2/3 > 1/2 ✓. So still 1 fraction.")

# Let me now verify the GENERAL theorem more carefully.
# For ANY Farey gap (a/b, c/d) in F_{p-1}:
# Number of k in (pa/b, pc/d) = floor(pc/d) - ceil(pa/b)
# = floor(pc/d) - floor(pa/b) - [1 if pa/b is not integer, else 0] + 1 ... 
# Hmm, let me just use the EXACT formula.

# The key: pc/d - pa/b = p/(bd).
# And b + d > p-1 (Farey neighbor condition), so b + d ≥ p.
# For b,d ≥ 1: bd ≥ ? given b + d ≥ p.
# By AM-GM: bd ≤ (b+d)²/4, but we need a LOWER bound.
# bd = b(b+d-b) ≥ ... For fixed b+d = s: bd is minimized at b=1, d=s-1.
# min(bd) = s-1 ≥ p-1.
# 
# So bd ≥ p-1, giving p/(bd) ≤ p/(p-1) < 2 for p ≥ 3.
# 
# Number of integers in an interval of length L < 2: it's either 0, 1, or possibly 2
# (if the interval spans two integers).
# But the interval is OPEN: (pa/b, pc/d).
# Number of integers = floor(pc/d - ε) - ceil(pa/b + ε) + 1 for small ε
# = floor(pc/d) - ceil(pa/b) + 1  [when endpoints are not integers]
# 
# Since p is prime and b, d ≤ p-1:
# pa/b is an integer iff b | pa iff b | a (since gcd(p,b)=1) iff a=0 or a=b.
# pa/b integer: only at a=0 (giving pa/b = 0) or a=b (giving pa/b = p, but a≤b).
# So the only integer endpoint is pa/b = 0 when a = 0.
# Similarly pc/d = integer iff c=0 or c=d. c=0 only for c/d = 0/1 (first fraction).
# c=d for c/d = 1/1 (last fraction, pc/d = p).
#
# For interior gaps (a > 0 and c < d):
# Neither endpoint is integer.
# Number of integers in (pa/b, pc/d) = floor(pc/d) - floor(pa/b).
# (Standard formula for non-integer endpoints of OPEN interval.)
# 
# Since pc/d - pa/b = p/(bd) < 2:
# floor(pc/d) - floor(pa/b) ≤ 1.  
# (Because the interval has length < 2 and doesn't contain endpoints,
#  it can contain at most 1 integer.)
# 
# WAIT: An open interval of length < 2 can contain 0 or 1 integer.
# Proof: If it contained 2 integers m and m+1, then the length ≥ 1 + ε 
# (for the interval to strictly contain both). But actually (m-ε, m+1+ε) 
# has length 1+2ε, which is < 2. And it contains m AND m+1.
# So an interval of length < 2 CAN contain 2 integers if the endpoints
# are very close to integers. E.g., (0.01, 1.99) has length 1.98 < 2 
# and contains 1.
# 
# Actually (0.01, 1.99) contains only k=1. You need length ≥ 2 to 
# contain 2 integers in an open interval... NO! 
# (0.5, 2.5) has length 2 and contains 1 and 2.
# (0.01, 1.99) has length 1.98 and contains only 1.
# (m - ε, m + 1 + ε) has length 1 + 2ε and contains m and m+1? 
# No, we need m > m - ε (yes) and m+1 < m + 1 + ε (yes if ε > 0).
# So (m-ε, m+1+ε) contains both m and m+1.
# Length = 1 + 2ε. For any ε > 0, this is > 1 but can be < 2.
# So YES, an open interval of length 1 < L < 2 can contain 2 integers!
#
# EXAMPLE: (0.999, 2.001) has length 1.002 and contains 1 and 2.
#
# So p/(bd) < 2 does NOT rule out 2 integers in the gap.
# We need p/(bd) ≤ 1 to guarantee at most 1 integer.
# That requires bd ≥ p.
# 
# b + d ≥ p (Farey neighbor condition).
# bd ≥ p iff b + d ≥ p AND bd ≥ p.
# The minimum of bd subject to b + d ≥ s is at b=1, d=s-1: bd = s-1.
# So min(bd | b+d ≥ p) = p-1.
# 
# p/(bd) ≤ p/(p-1). For p/(p-1) ≤ 1? Only if p ≤ p-1. Never.
# So p/(bd) > 1 when bd = p-1 (minimum case).
# 
# BUT: the interval is (pa/b, pc/d), not [pa/b, pc/d].
# And we showed pa/b and pc/d are NOT integers for interior gaps.
# 
# KEY: floor(y) - floor(x) = 1 iff there exists an integer in (x,y) and y-x < 2.
# floor(y) - floor(x) = 0 iff no integer in [ceil(x), floor(y)].
# 
# So we need: are there 2 integers in (pa/b, pc/d) when p/(bd) ∈ (1, 2)?
# This happens iff floor(pc/d) - ceil(pa/b) ≥ 1, i.e., 
# there exists integer m with ceil(pa/b) ≤ m < m+1 ≤ floor(pc/d).
# i.e., floor(pc/d) ≥ ceil(pa/b) + 1.
# 
# floor(pc/d) - floor(pa/b) ≥ 2 requires pc/d - pa/b ≥ 2.
# But pc/d - pa/b = p/(bd) < 2 (strictly, since bd ≥ p-1 > 0 and p/(p-1) < 2).
# 
# Hmm wait: floor(y) - floor(x) depends on where x,y sit relative to integers.
# If x = 3.01 and y = 4.99: floor(y) - floor(x) = 4 - 3 = 1. One integer (4) in (x,y).
# If x = 2.99 and y = 4.01: floor(y) - floor(x) = 4 - 2 = 2. Two integers (3,4) in (x,y)? 
# Yes! 3 and 4 are both in (2.99, 4.01). And 4.01 - 2.99 = 1.02 < 2.
# 
# So floor(y) - floor(x) = 2 is possible with y - x < 2.
# But floor(y) - floor(x) ≤ ceil(y-x). Since y-x < 2: ceil(y-x) ≤ 2.
# So max is 2. But can it happen for our specific (pa/b, pc/d)?
# 
# For 2 integers in (pa/b, pc/d): need {pa/b} > {pc/d}.
# (i.e., the fractional part "wraps around" twice.)
# Since pc/d = pa/b + p/(bd), and p/(bd) ∈ (1, 2):
# {pc/d} = {pa/b + p/(bd)} = {{pa/b} + {p/(bd)} + floor(p/(bd))}
# Since floor(p/(bd)) = 1 (as p/(bd) ∈ (1,2)):
# {pc/d} = {{pa/b} + {p/(bd)}}
# 
# 2 integers in interval ⟺ floor(pc/d) - floor(pa/b) = 2
# ⟺ pa/b + p/(bd) has floor 2 more than pa/b
# ⟺ the sum crosses TWO integer boundaries
# ⟺ {pa/b} + p/(bd) ≥ 2
# 
# Since p/(bd) < 2 and {pa/b} < 1: {pa/b} + p/(bd) < 3.
# But we need ≥ 2: {pa/b} ≥ 2 - p/(bd) = 2 - p/(bd).
# Since p/(bd) > 1: 2 - p/(bd) < 1. So this is possible.
# 
# SPECIFICALLY: 2 fractions in gap ⟺ {pa/b} + p/(bd) ≥ 2.
# 
# But we OBSERVED 0 multi-fraction gaps for all tested primes!
# So {pa/b} + p/(bd) < 2 for ALL Farey gaps.
# Can we PROVE this?

# The condition {pa/b} + p/(bd) < 2 for all Farey neighbors (a/b, c/d) in F_{p-1}.
# Since p/(bd) = p/(bd) and bd ≥ p-1:
# p/(bd) ≤ p/(p-1).
# Need {pa/b} < 2 - p/(p-1) = (p-2)/(p-1).
# 
# {pa/b} = (pa mod b)/b.
# For b = p-1 (the maximum denominator):
# pa mod (p-1) = pa - (p-1)·floor(pa/(p-1)).
# p ≡ 1 (mod p-1), so pa ≡ a (mod p-1).
# Therefore pa mod (p-1) = a (mod p-1) = a (since 0 ≤ a < p-1).
# {pa/(p-1)} = a/(p-1).
# We need a/(p-1) < (p-2)/(p-1), i.e., a < p-2.
# 
# For the gap ((p-2)/(p-1), 1/1):
# a = p-2, b = p-1.
# {pa/b} = (p-2)/(p-1). And p/(bd) = p/((p-1)·1) = p/(p-1).
# {pa/b} + p/(bd) = (p-2)/(p-1) + p/(p-1) = (2p-2)/(p-1) = 2.
# EXACTLY 2! So {pa/b} + p/(bd) = 2, not > 2.
# floor(pc/d) - floor(pa/b) = floor(p/1) - floor(p(p-2)/(p-1))
# = p - floor((p²-2p)/(p-1)) = p - floor(p - 2/(p-1)) 
# For p ≥ 4: 0 < 2/(p-1) < 1, so floor(p - 2/(p-1)) = p-1.
# Count = p - (p-1) = 1. ONE fraction.
# 
# The boundary case: {pa/b} + p/(bd) = 2 gives count = 1 (not 2)
# because the formula is floor, and we get floor(2) - something = 1.
# 
# MORE PRECISELY: The count of integers in OPEN interval (x, x+L) where L < 2:
# If {x} + L < 2: count = floor(L + {x}) (either 0 or 1)
# If {x} + L = 2: count = 1 (the interval is (x, x+2-{x}) and contains floor(x)+1 only,
#   because x+L = x + 2 - {x} = ceil(x) + 1, but the interval is OPEN so ceil(x)+1 is excluded)
# Wait: x + L = floor(x) + {x} + L. If {x} + L = 2: x + L = floor(x) + 2.
# The open interval (x, floor(x)+2) contains floor(x)+1 (if x < floor(x)+1, which requires {x} > 0).
# Does it contain floor(x)+2? No, since the interval is open on the right.
# So count = 1 when {x} + L = 2 and {x} > 0. ✓

# THEREFORE: For Farey neighbors in F_{p-1} with p prime:
# Since {pa/b} + p/(bd) ≤ 2 (with equality only at specific boundary gaps):
# Each gap receives AT MOST 1 new fraction k/p.
# 
# But we need to verify {pa/b} + p/(bd) ≤ 2 for ALL gaps.
# We proved p/(bd) ≤ p/(p-1) and showed the worst case is equality = 2.
# But what if bd = p-1 for some OTHER gap with {pa/b} large?

# When bd = p-1 with b+d = p (the only way), we need b·d = p-1 and b+d = p.
# This gives b and d as roots of t² - pt + (p-1) = 0, so {b,d} = {1, p-1}.
# So the ONLY gaps with bd = p-1 are those involving denominator 1 or p-1.
# These are the first and last gaps.

# For all OTHER gaps: bd ≥ p, giving p/(bd) ≤ 1, and then:
# {pa/b} + p/(bd) < 1 + 1 = 2. So count ≤ 1. QED for interior gaps.

# For the boundary gaps (involving b=1 or d=1):
# Gap (0/1, 1/N): bd = N = p-1. Count = 1 (shown above).  
# Gap ((p-2)/(p-1), 1/1): bd = p-1. Count = 1 (shown above).

# THEOREM PROVED! ✓

print("\n" + "=" * 70)
print("THEOREM (PROVED): Strict Injection Principle")
print("=" * 70)
print("""
THEOREM: For prime p >= 3, each gap of F_{p-1} receives at most one new fraction k/p.

PROOF OUTLINE:
1. For consecutive fractions (a/b, c/d) in F_{p-1}: bc - ad = 1 and b + d >= p.
2. The number of integers k in (pa/b, pc/d) equals floor({pa/b} + p/(bd)).
3. Since b + d >= p and min(bd | b+d >= p) = p-1:
   p/(bd) <= p/(p-1) < 2.
4. For INTERIOR gaps (bd >= p): p/(bd) <= 1, so count <= floor(1 + {pa/b}) = 1. Done.
5. For BOUNDARY gaps (bd = p-1): {pa/b} + p/(bd) = 2 exactly, but the open 
   interval at a non-integer boundary gives count = 1.
6. Therefore every gap receives at most 1 new fraction. QED.

COROLLARY: The p-1 new fractions k/p land in exactly p-1 distinct gaps of F_{p-1}.
The remaining |F_{p-1}| - 1 - (p-1) = |F_{p-1}| - p gaps remain empty.
""")

# Verify with larger primes:
print("Extended verification:")
for p in [503, 997, 1009, 1999, 2003]:
    F = farey_list(p - 1)
    n = len(F)
    max_count = 0
    for i in range(n - 1):
        a, b = F[i]
        c, d = F[i + 1]
        k_lo = (p * a) // b + 1
        if c == d:
            k_hi = p - 1
        else:
            k_hi = (p * c - 1) // d
        count = max(0, k_hi - k_lo + 1)
        max_count = max(max_count, count)
    print(f"  p={p}: |F_{{p-1}}|={n}, max per gap = {max_count} ✓")

