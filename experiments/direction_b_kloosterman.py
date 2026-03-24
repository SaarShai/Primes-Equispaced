#!/usr/bin/env python3
"""
DIRECTION B: Kloosterman sum connection and closed forms

The per-denominator covariance cov_b(D,δ) was claimed to have Kloosterman structure.
Let's make this precise.

SETUP:
For prime p, the new fractions are k/p for k=1,...,p-1.
For each OLD fraction a/b ∈ F_{p-1}, the displacement is D(a/b) = rank(a/b) - n·(a/b).
The shift δ(a/b) = a/b - {p·a/b}.

The cross term Σ D(a/b)·δ(a/b) summed over F_{p-1} controls the sign of ΔW(p).

Per-denominator decomposition: group by denominator b.
For each b ≤ p-1:
  Σ_{a: gcd(a,b)=1, 0≤a≤b} D(a/b)·δ(a/b)

Now δ(a/b) = a/b - {pa/b}.
Since gcd(p,b)=1 (as p is prime and b < p), pa mod b runs over all coprime residues.
Let pa ≡ r (mod b), so {pa/b} = r/b (since 0 < a < b → 0 < r < b).
Then δ(a/b) = a/b - r/b = (a - r)/b = (a - pa mod b)/b.

KEY: the map a → pa mod b is a PERMUTATION of coprime residues mod b.
So Σ_{a} δ(a/b) = Σ (a - pa mod b)/b = (Σa - Σ(pa mod b))/b = 0 
(since the same values are summed in different order).

For the cross term with D: we need to understand D(a/b) for fixed b.
D(a/b) = rank(a/b) - n·(a/b) where n = |F_{p-1}|.
rank(a/b) = #{(a',b') ∈ F_{p-1} : a'/b' ≤ a/b}.

The KLOOSTERMAN connection: 
Kloosterman sum K(m,n;c) = Σ_{x mod c, gcd(x,c)=1} e^{2πi(mx + n·x̄)/c}
where x̄ = modular inverse of x.

Our cross term involves Σ (a/b)·(a - pa mod b)/b 
= (1/b²)·Σ a·(a - pa mod b)
= (1/b²)·[Σ a² - Σ a·(pa mod b)]

The second part: Σ_{a coprime to b} a·(pa mod b).
Let r = pa mod b, so a = p⁻¹·r mod b (where p⁻¹ is the inverse of p mod b).
Then Σ a·r = Σ (p⁻¹r mod b)·r.

This IS a Kloosterman-type sum! Specifically:
Σ_{r coprime to b} r·(p⁻¹r mod b) = Σ_{r} r·{p⁻¹r·b⁻¹}·b  [approximately]

Actually let me compute this precisely.
"""

from math import gcd, floor
from fractions import Fraction
import numpy as np

def farey_sequence(N):
    """Return F_N as sorted list of (a,b) tuples with Fraction values."""
    fracs = []
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: Fraction(x[0], x[1]))
    return fracs

def mertens(N):
    """Compute M(N) via sieve."""
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2 * i, N + 1, i):
            mu[j] -= mu[i]
    return sum(mu[1:N+1])

def modinv(a, m):
    """Modular inverse via extended Euclidean."""
    if m == 1:
        return 0
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def kloosterman_sum(m, n, c):
    """Classical Kloosterman sum K(m,n;c)."""
    s = 0j
    for x in range(1, c):
        if gcd(x, c) == 1:
            x_inv = modinv(x, c)
            s += np.exp(2j * np.pi * (m * x + n * x_inv) / c)
    return s.real  # K is real when m,n are real

print("=" * 70)
print("KLOOSTERMAN SUM CONNECTION")
print("=" * 70)

# For each prime p and denominator b < p, compute:
# C_b = Σ_{a coprime to b, 0<a<b} a · (pa mod b)
# and compare to Kloosterman sums K(1,p;b)

for p in [5, 7, 11, 13, 17, 19, 23]:
    print(f"\np = {p}:")
    F = farey_sequence(p - 1)
    n = len(F)
    
    for b in range(2, p):
        if b == 1:
            continue
        # Coprime residues mod b
        coprime_a = [a for a in range(1, b) if gcd(a, b) == 1]
        if len(coprime_a) == 0:
            continue
        
        # Compute C_b = Σ a · (pa mod b) over coprime a
        C_b = sum(a * ((p * a) % b) for a in coprime_a)
        
        # Σ a² over coprime a
        sum_a_sq = sum(a * a for a in coprime_a)
        
        # Kloosterman sum K(p, p; b) = Σ e^{2πi(px + p·x⁻¹)/b}
        K_pp = kloosterman_sum(p, p, b)
        
        # Also try K(1, p²; b) 
        K_1p2 = kloosterman_sum(1, p*p % b, b)
        
        # Dedekind sum s(p, b)
        # s(h,k) = Σ_{r=1}^{k-1} ((r/k))·((hr/k)) where ((x)) = {x}-1/2 if x∉Z, else 0
        def dedekind_s(h, k):
            s = Fraction(0)
            for r in range(1, k):
                x1 = Fraction(r, k) - Fraction(1, 2)
                hr_mod = (h * r) % k
                if hr_mod == 0:
                    x2 = Fraction(0)
                else:
                    x2 = Fraction(hr_mod, k) - Fraction(1, 2)
                s += x1 * x2
            return s
        
        ds = dedekind_s(p, b)
        
        if b <= 12:
            print(f"  b={b}: C_b={C_b}, Σa²={sum_a_sq}, K(p,p;b)={K_pp:.4f}, "
                  f"s(p,b)={float(ds):.4f}")

# ============================================================
# EXACT KLOOSTERMAN IDENTITY
# ============================================================
print("\n" + "=" * 70)
print("EXACT IDENTITY: Cross term as Dedekind/Kloosterman sum")
print("=" * 70)

# Let me compute the FULL cross term Σ D·δ and decompose it.
# D(a/b) = rank(a/b) - n·(a/b)
# δ(a/b) = a/b - {pa/b}

for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    # Compute rank, D, δ for each fraction
    cross_total = Fraction(0)
    cross_by_b = {}
    
    for j, (a, b) in enumerate(F):
        f_val = Fraction(a, b)
        D_val = j - n * f_val
        
        # δ = a/b - {pa/b}
        pa_mod_b = (p * a) % b
        frac_part = Fraction(pa_mod_b, b)
        delta_val = f_val - frac_part
        
        product = D_val * delta_val
        cross_total += product
        
        if b not in cross_by_b:
            cross_by_b[b] = Fraction(0)
        cross_by_b[b] += product
    
    # Try to express cross_by_b[b] in terms of Kloosterman/Dedekind sums
    # 
    # The Dedekind sum s(h,k) = Σ_{r=1}^{k-1} ((r/k))·((hr/k))
    # where ((x)) is the sawtooth function.
    #
    # Our δ(a/b) = (a - pa mod b)/b is closely related to ((pa/b)):
    # {pa/b} = (pa mod b)/b, so δ(a/b) = a/b - {pa/b}
    # ((pa/b)) = {pa/b} - 1/2 = (pa mod b)/b - 1/2
    # So δ(a/b) = a/b - ((pa/b)) - 1/2 = ((a/b)) + 1/2 - ((pa/b)) - 1/2 = ((a/b)) - ((pa/b))
    # Wait: ((a/b)) = a/b - 1/2 for gcd(a,b)=1, 0 < a < b.
    # And δ = a/b - (pa mod b)/b.
    # So δ = ((a/b)) + 1/2 - ((pa/b mod b/b)) - 1/2 = ((a/b)) - ((pa/b))
    # where ((pa/b)) means the sawtooth at pa/b.
    # Since pa mod b ≠ 0 (because gcd(p,b)=1 and 0<a<b):
    # ((pa/b)) = (pa mod b)/b - 1/2.
    # So δ(a/b) = ((a/b)) - ((pa/b)). This is EXACT for interior fractions!
    
    # Now D(a/b) = rank(a/b) - n·(a/b).
    # The Farey counting function N_{p-1}(x) ≈ 3x(p-1)²/π² = n·x (approximately).
    # D(a/b) is the ERROR in this approximation.
    
    print(f"p={p:3d}: Σ D·δ = {float(cross_total):12.6f}, "
          f"n={n}, M(p)={mertens(p)}")

# ============================================================
# THE SAWTOOTH DECOMPOSITION
# ============================================================
print("\n" + "=" * 70)
print("SAWTOOTH DECOMPOSITION: δ(a/b) = ((a/b)) - ((pa/b))")
print("=" * 70)

# This is a key structural insight:
# δ(a/b) = ((a/b)) - ((pa/b))  [difference of sawtooth functions]
# where ((x)) = {x} - 1/2 for x ∉ Z, 0 for x ∈ Z.
#
# For a/b with gcd(a,b)=1 and 0 < a < b:
# ((a/b)) = a/b - 1/2
# ((pa/b)) = (pa mod b)/b - 1/2
#
# So: δ = (a - pa mod b)/b ✓ (matches our definition)
#
# Now the cross term Σ D·δ = Σ D·((a/b)) - Σ D·((pa/b))
# 
# The FIRST part Σ D·((a/b)) involves the sawtooth of the fraction itself.
# Since D measures how far a/b is from its "expected" position,
# and ((a/b)) = a/b - 1/2, this is:
# Σ D·((a/b)) = Σ D·(f - 1/2) = Σ D·f - (1/2)·Σ D
# 
# We know Σ D = 0 (D sums to 0 by definition).
# And Σ D·f = Σ (rank - n·f)·f = Σ rank·f - n·Σ f² = R/n_new... complicated.
#
# The SECOND part Σ D·((pa/b)) is:
# Σ_{(a,b)∈F_{p-1}} D(a/b)·((pa/b))
# = Σ_b Σ_{a coprime to b} D(a/b)·((pa/b))
# 
# For fixed b: the map a → pa mod b permutes coprime residues.
# So ((pa/b)) = ((r/b)) where r = pa mod b.
# And D(a/b) = D at the position of a/b in the Farey sequence.
# 
# KEY: This is NOT a standard Kloosterman sum because D depends on the GLOBAL
# position of a/b in F_{p-1}, not just on a and b.
# 
# HOWEVER: If we APPROXIMATE D(a/b) ≈ some function of (a,b) alone,
# then the sum becomes a classical sum.

# Let me compute the EXACT sawtooth decomposition and verify:
for p in [11, 13, 17]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    sum_D_saw = Fraction(0)   # Σ D·((f))
    sum_D_psaw = Fraction(0)  # Σ D·((pf))
    sum_D_delta = Fraction(0) # Σ D·δ
    
    for j, (a, b) in enumerate(F):
        f_val = Fraction(a, b)
        D_val = j - n * f_val
        
        # Sawtooth ((f)) for f = a/b
        if a == 0 or a == b:
            saw_f = Fraction(0)
        else:
            saw_f = f_val - Fraction(1, 2)
        
        # Sawtooth ((pf)) 
        pa_mod_b = (p * a) % b
        if pa_mod_b == 0:  # happens only for a=0 (since gcd(p,b)=1 and 0<a<b)
            saw_pf = Fraction(0)
        else:
            saw_pf = Fraction(pa_mod_b, b) - Fraction(1, 2)
        
        # δ = ((f)) - ((pf))
        delta_val = saw_f - saw_pf
        
        # For endpoints a=0: f=0, saw_f=0, pa mod b = 0, saw_pf = 0, δ=0
        # For a=b (f=1, b=1): saw_f=0, p mod 1 = 0, saw_pf = 0, δ=0
        
        sum_D_saw += D_val * saw_f
        sum_D_psaw += D_val * saw_pf
        sum_D_delta += D_val * delta_val
    
    print(f"p={p}: Σ D·((f))={float(sum_D_saw):.6f}, "
          f"Σ D·((pf))={float(sum_D_psaw):.6f}, "
          f"δ decomp check: {float(sum_D_saw - sum_D_psaw):.6f} vs "
          f"Σ D·δ = {float(sum_D_delta):.6f}")

# ============================================================
# GAP FILLING PATTERN
# ============================================================
print("\n" + "=" * 70)
print("GAP FILLING: Closed form for filled vs skipped gaps")
print("=" * 70)

# When going from F_{p-1} to F_p, each consecutive pair (a/b, c/d) in F_{p-1}
# has a "gap" of size 1/(bd). A new fraction k/p falls in this gap iff
# a/b < k/p < c/d, i.e., ap/b < k < cp/d.
# Since these are Farey neighbors: bc - ad = 1 (mediant property).
# The interval (ap/b, cp/d) has length p/(bd).
# Number of integers in this interval = ⌊cp/d⌋ - ⌈ap/b⌉ + 1... approximately p/(bd).
# 
# For a Farey gap of size 1/(bd), we get exactly ⌊p/(bd)⌋ or ⌈p/(bd)⌉ new fractions.
#
# INJECTION PRINCIPLE (proved): each gap gets at most ⌊p/(bd) + 1⌋ fractions.
# More precisely: the number is ⌊p·c/d⌋ - ⌊p·a/b⌋ - 1 + [mediant correction].

# QUESTION: Can we get a CLOSED FORM for:
# (a) Total number of filled gaps (gaps that receive ≥ 1 new fraction)
# (b) Total number of skipped gaps (gaps that receive 0 new fractions)

# Note: gap (a/b, c/d) receives 0 new fractions iff no integer in (ap/b, cp/d),
# i.e., ⌊cp/d⌋ = ⌈ap/b⌉ - 1, i.e., ⌊cp/d⌋ < ⌈ap/b⌉.
# Since ap/b < cp/d and the interval has length p/(bd),
# the gap is empty iff p/(bd) < 1, i.e., bd > p.
# (This is approximate; the exact condition depends on the fractional parts.)

# When bd > p: the gap might or might not receive a fraction.
# When bd ≤ p: the gap ALWAYS receives at least one fraction.
# When bd ≤ p/2: the gap receives at least 2 fractions (approximately).

for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    filled_gaps = 0
    empty_gaps = 0
    total_new = 0
    
    for i in range(len(F) - 1):
        a, b = F[i]
        c, d = F[i + 1]
        
        # Count new fractions k/p in (a/b, c/d)
        lo = a * p  # a/b = lo/bp, so k/p > a/b iff k > ap/b iff k ≥ ⌊ap/b⌋ + 1
        hi = c * p  # k/p < c/d iff k < cp/d iff k ≤ ⌈cp/d⌉ - 1
        
        k_lo = lo // b + 1  # smallest k with k/p > a/b
        k_hi = (hi - 1) // d  # largest k with k/p < c/d (since cp might be divisible by d)
        # More carefully: k/p < c/d iff kd < cp iff k ≤ (cp-1)//d (if d∤cp)
        # or k ≤ cp/d - 1 (if d|cp). Since p is prime and d < p, d|cp iff d|c.
        # But c < d (Farey fractions have a ≤ b), so d|c only if c=0 (impossible for c/d > 0).
        # Actually c/d is a Farey fraction with 0 < c/d, so c ≥ 1 and c ≤ d.
        # d|c iff c=d, i.e., c/d = 1. The only such case is the last gap (?/?, 1/1).
        
        count = max(0, k_hi - k_lo + 1)
        
        if count > 0:
            filled_gaps += 1
        else:
            empty_gaps += 1
        total_new += count
    
    # Theoretical: total new = p-1 (since φ(p) = p-1 for prime p)
    gap_count = len(F) - 1
    fill_ratio = filled_gaps / gap_count if gap_count > 0 else 0
    
    # Count gaps with bd > p and bd ≤ p
    large_gaps = sum(1 for i in range(len(F)-1) if F[i][1] * F[i+1][1] <= p)
    small_gaps = gap_count - large_gaps
    
    print(f"p={p:3d}: gaps={gap_count:5d}, filled={filled_gaps:5d} ({fill_ratio:.3f}), "
          f"empty={empty_gaps:5d}, bd≤p={large_gaps:5d}, new_fracs={total_new}")

# ============================================================
# CLOSED FORM ATTEMPT
# ============================================================
print("\n" + "=" * 70)
print("CLOSED FORM: Number of filled gaps as function of p")
print("=" * 70)

# From the data above, the fill ratio appears to approach a limit.
# Let's look at the ratio filled_gaps / (n-1) where n = |F_{p-1}|.
# And the ratio filled_gaps / (p-1) (new fractions per filled gap).

filled_data = []
for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
          101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    filled = 0
    for i in range(len(F) - 1):
        a, b = F[i]
        c, d = F[i + 1]
        lo = a * p
        hi = c * p
        k_lo = lo // b + 1
        k_hi = (hi - 1) // d
        if k_hi >= k_lo:
            filled += 1
    
    gap_count = n - 1
    filled_data.append((p, filled, gap_count, n))
    
print(f"{'p':>5} {'filled':>7} {'gaps':>7} {'fill%':>7} {'filled/(p-1)':>13} {'gaps/(p-1)':>11}")
for p, filled, gaps, n in filled_data:
    print(f"{p:5d} {filled:7d} {gaps:7d} {filled/gaps*100:6.1f}% {filled/(p-1):13.4f} {gaps/(p-1):11.4f}")

# ============================================================
# KLOOSTERMAN BOUND ON THE CROSS TERM
# ============================================================
print("\n" + "=" * 70)
print("KLOOSTERMAN BOUND on Σ D·δ")
print("=" * 70)

# We showed δ(a/b) = ((a/b)) - ((pa/b)) for interior fractions.
# The sawtooth ((x)) has Fourier expansion: ((x)) = -(1/π) Σ_{k=1}^∞ sin(2πkx)/k.
# So δ(a/b) = -(1/π) Σ_k [sin(2πka/b) - sin(2πkpa/b)] / k
#
# And Σ D(a/b)·δ(a/b) = -(1/π) Σ_k (1/k) · [Σ D·sin(2πka/b) - Σ D·sin(2πkpa/b)]
#
# But we know from the displacement-cosine identity that:
# Σ D·cos(2πmf) = -1 - M(m)/2  (for prime m, via bridge identity)
# Is there a similar identity for Σ D·sin(2πmf)?
# 
# The Farey involution σ(f) = 1-f gives D(σ(f)) = -D(f) - 1.
# sin(2πm(1-f)) = -sin(2πmf) when m is integer.
# So Σ D(f)·sin(2πmf) = Σ D(σ(f))·sin(2πm·σ(f))
#                      = Σ (-D(f)-1)·(-sin(2πmf))
#                      = Σ D(f)·sin(2πmf) + Σ sin(2πmf)
# 
# Therefore: 0 = Σ sin(2πmf) [over Farey fractions]
# Wait that means: Σ D·sin = Σ D·sin + Σ sin → Σ sin = 0.
# This is consistent since Im(S(m,N)) = 0 for integer m (verified!).
# So Σ sin(2πmf) = 0 over F_N.
# 
# But from D(σ(f)) = -D(f) - 1:
# Σ D·sin(2πmf) = Σ (D(f)+1)·sin(2πmf) = Σ D·sin + Σ sin = Σ D·sin
# So Σ D·sin(2πmf) is UNCONSTRAINED by the involution. We need another approach.
# 
# Actually: Σ D·e^{2πimf} = Σ D·cos + i·Σ D·sin.
# We know Σ_{f∈F_N} e^{2πimf} = S(m,N) (real). 
# And Σ D·e^{2πimf} = Σ (rank - n·f)·e^{2πimf} = Σ rank·e^{2πimf} - n·S(m,N).
# 
# The sum Σ rank·e^{2πimf} = Σ_{j=0}^{n-1} j·e^{2πimf_j} where f_j is the j-th Farey fraction.
# This is the "rank-weighted" Farey sum. Its real part gives Σ D·cos after subtracting n·Re(S).

# Let me compute Σ D·sin and Σ D·cos for verification:
for p in [11, 13, 17, 19, 23]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    for m in [p, 2, 3, 5]:
        sum_D_cos = Fraction(0)
        sum_D_sin = 0.0
        
        for j, (a, b) in enumerate(F):
            f_val = Fraction(a, b)
            D_val = float(j - n * f_val)
            angle = 2 * np.pi * m * float(f_val)
            sum_D_cos += D_val * np.cos(angle)
            sum_D_sin += D_val * np.sin(angle)
        
        M_m = mertens(m) if m <= 200 else 0
        expected_cos = -1 - M_m / 2 if m > p - 1 else None
        print(f"  p={p}, m={m}: Σ D·cos={float(sum_D_cos):10.4f}, "
              f"Σ D·sin={sum_D_sin:10.4f}, "
              f"-1-M({m})/2={-1-M_m/2 if m<=200 else '?'}")

# ============================================================
# NOVEL: DEDEKIND SUM REPRESENTATION
# ============================================================
print("\n" + "=" * 70)
print("DEDEKIND SUM REPRESENTATION of the cross term")
print("=" * 70)

# The Dedekind sum s(h,k) = Σ_{r=1}^{k-1} ((r/k))·((hr/k))
# = Σ_{r coprime to k} (r/k - 1/2)·(hr mod k / k - 1/2)  [approximately]
# Actually for general r, not just coprime.
#
# Our per-denominator sum involves only COPRIME a, and uses D(a/b) instead
# of ((a/b)). So it's a "twisted Dedekind sum" where one sawtooth is
# replaced by the Farey discrepancy function.
#
# But D(a/b) ≈ -n·((a/b)) + correction (since D measures deviation from uniform).
# If we use D ≈ -n·((a/b)):
# Σ D·δ ≈ -n · Σ ((a/b))·[((a/b)) - ((pa/b))]
#        = -n · [Σ ((a/b))² - Σ ((a/b))·((pa/b))]
#        = -n · [Σ ((a/b))² - s*(p,b)]
# where s*(p,b) is the "coprime Dedekind sum" (restricted to gcd(a,b)=1).
#
# The coprime Dedekind sum differs from the standard one by excluding
# a with gcd(a,b) > 1. For prime b, all a are coprime so s* = s.
#
# For prime b:
# s*(p,b) = s(p,b) = standard Dedekind sum
# Σ ((a/b))² = Σ_{a=1}^{b-1} (a/b - 1/2)² = (b-1)(b+1)/(12b) ← standard

# Let's verify this approximation:
print("\nApproximation D ≈ -n·((f)) for the cross term:")
for p in [11, 13, 17, 19, 23, 29, 31]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    exact_cross = Fraction(0)
    approx_cross = Fraction(0)
    
    for j, (a, b) in enumerate(F):
        f_val = Fraction(a, b)
        D_val = j - n * f_val
        
        pa_mod_b = (p * a) % b
        if a > 0 and a < b:
            saw_f = f_val - Fraction(1, 2)
            saw_pf = Fraction(pa_mod_b, b) - Fraction(1, 2)
        else:
            saw_f = Fraction(0)
            saw_pf = Fraction(0)
        
        delta_val = saw_f - saw_pf
        exact_cross += D_val * delta_val
        
        # Approximation: D ≈ -n·((f))
        D_approx = -n * saw_f
        approx_cross += D_approx * delta_val
    
    print(f"  p={p:3d}: exact={float(exact_cross):10.4f}, "
          f"approx(-n·((f)))={float(approx_cross):10.4f}, "
          f"ratio={float(approx_cross)/float(exact_cross):.4f}" if float(exact_cross) != 0 else "")

# ============================================================
# NOVEL: Express cross term via Ramanujan-Dedekind hybrid
# ============================================================
print("\n" + "=" * 70)
print("RAMANUJAN-DEDEKIND HYBRID")
print("=" * 70)

# Using the Fourier expansion of ((x)):
# ((x)) = -(1/π) Σ_{k=1}^∞ sin(2πkx)/k
# 
# δ(a/b) = ((a/b)) - ((pa/b)) = -(1/π) Σ_k [sin(2πka/b) - sin(2πkpa/b)]/k
#
# Σ_{f∈F_N} D(f)·δ(f) = -(1/π) Σ_k (1/k)·[Σ D·sin(2πkf) - Σ D·sin(2πkpf)]
#
# From the universal formula (imaginary part):
# Im(S(k,N)) = Σ sin(2πkf) = 0 (since S is always real for integer k)
# Im(Σ D·e^{2πikf}) = Σ D·sin(2πkf) = Im(Σ j·e^{2πikf_j}) (since n·Im(S)=0)
#
# Let T(k,N) = Σ_{j=0}^{n-1} j·e^{2πikf_j} [rank-weighted Farey sum]
# Then Σ D·cos(2πkf) = Re(T(k,N)) - n·Re(S(k,N))/(2πk)... wait, let me be more careful.
#
# Σ D·e^{2πikf} = T(k,N) - n·S(k,N) [since D = rank - n·f, but this isn't right either]
# Actually D(f_j) = j - n·f_j, so Σ_j D(f_j)·e^{2πikf_j} = T(k,N) - n·Σ f_j·e^{2πikf_j}
# Hmm, Σ f_j·e^{2πikf_j} is a DIFFERENT sum.

# Let me just compute T(k,N) = Σ j·e^{2πikf_j} for several N and k:
for p in [11, 13]:
    F = farey_sequence(p - 1)
    n = len(F)
    
    print(f"\np={p}, n={n}:")
    for k in range(1, 8):
        T_k = sum(j * np.exp(2j * np.pi * k * a / b) for j, (a, b) in enumerate(F))
        S_k = sum(np.exp(2j * np.pi * k * a / b) for _, (a, b) in enumerate(F))
        
        # Σ D·e^{2πikf} = T_k - n·(Σ f·e^{2πikf})
        f_weighted = sum(a/b * np.exp(2j * np.pi * k * a / b) for _, (a, b) in enumerate(F))
        D_sum = T_k - n * f_weighted
        
        print(f"  k={k}: T={T_k.real:8.3f}+{T_k.imag:8.3f}i, "
              f"S={S_k.real:8.3f}+{S_k.imag:8.3f}i, "
              f"Σ D·e={D_sum.real:8.3f}+{D_sum.imag:8.3f}i")

