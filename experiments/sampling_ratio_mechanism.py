#!/usr/bin/env python3
"""
Understanding WHY the Riemann sum at k/p doubles the integral.

E(x) = N_{F_N}(x) - nx is piecewise linear with slope -n between jumps of +1
at each Farey fraction. The integral of E^2 is well-approximated by sum_D^2/n.

The Riemann sum at equally-spaced k/p points DOUBLES the integral.

Hypothesis: The doubling comes from the JUMPS at Farey fractions.

At a Farey fraction f = a/b, E(x) jumps by +1. The point k/p that is closest
to f sees E(k/p) at the "post-jump" value, which is higher than the average
of E across the interval. The squared contribution at these points is enhanced.

But this can't be the whole story since EVERY k/p is close to some Farey fraction
(the gaps are O(1/N^2)).

Alternative hypothesis: The sawtooth decomposition shows the mechanism.

E(k/p) = (p-k)/p - (1/p) sum_m c_m (mk mod p)

The sum of sawtooth values {mk/p} for k=1,...,p-1 samples each sawtooth at
the p-rational grid. The key: the squared sum of a single sawtooth {mx} at
x=k/p for k=1,...,p-1 is (p-1)(2p-1)/(6p^2) ~ p/3, while the integral of
{x}^2 is 1/3. The Riemann sum matches the integral! No factor of 2 there.

But the CROSS terms {mx}{m'x} contribute. The sum is T(r)/p^2 where r=m'/m,
while the integral is:
integral_0^1 {mx}{m'x} dx for m != m' (mod p).

The integral of {mx}{m'x} over [0,1]:
For coprime m,m': = 1/4 - 1/(12 max(m,m')^2) approximately... Actually this
is a well-known Dedekind sum integral.

integral_0^1 {ax}{bx} dx = 1/4 for a != b (well, for a,b coprime integers)
Actually not exactly. Let me compute this correctly.

{ax} = ax - floor(ax). The product {ax}{bx} has a complicated integral.
For a,b positive integers:
integral_0^1 {ax}{bx} dx = 1/4 - sum_{d|gcd(a,b)} phi(d)/(12d^2) / something...

Actually, let me just compute it numerically for a few cases and compare with T(r)/p^2.
"""

import numpy as np
from fractions import Fraction
from math import gcd

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

# Compute integral of {ax}{bx} over [0,1] for various a,b
# and compare with T(b*a^{-1} mod p) / p^2

def integral_sawtooth_product(a, b, n_pts=100000):
    """Numerical integral of {ax}{bx} over [0,1]."""
    x = np.linspace(0, 1, n_pts, endpoint=False) + 0.5/n_pts
    fa = (a * x) % 1
    fb = (b * x) % 1
    return np.mean(fa * fb)

# For the E(x) decomposition, the integral of {mx}{m'x} matters.
# The Riemann sum sum_{k=1}^{p-1} {mk/p}{m'k/p} = T(m'/m mod p) / p^2.
# The integral I(m,m') = integral_0^1 {mx}{m'x} dx.

# For m = m': integral {mx}^2 = 1/12 + 1/(4m^2) ... no.
# integral_0^1 {mx}^2 dx = (1/m) sum_{j=0}^{m-1} integral_0^1 (mx-j)^2/(m^2) *m dx
# = integral_0^1 t^2 dt = 1/3... no that's wrong too.
# {mx} has period 1/m. On [j/m, (j+1)/m], {mx} = mx - j goes from 0 to 1.
# Wait, it goes from 0 to 1 (exclusive). So integral of {mx}^2 on [0,1]:
# = m * integral_0^{1/m} (mx)^2 dx = m * [m^2 x^3/3]_0^{1/m} = m * m^2/(3m^3) = 1/3.
# Hmm, that's wrong. {mx} on [j/m, (j+1)/m] is mx - j, ranging from 0 to 1.
# integral_{j/m}^{(j+1)/m} (mx-j)^2 dx = [1/(3m^3)] * [(j+1)^3 - j^3] wait no
# Let u = mx - j, du = m dx, dx = du/m.
# integral_0^1 u^2 du/m = 1/(3m)
# Sum over j=0,...,m-1: m * 1/(3m) = 1/3.
# OK so integral {mx}^2 = 1/3 for any m >= 1. Not 1/12.

# And the Riemann sum: (1/(p-1)) sum_{k=1}^{p-1} {mk/p}^2
# = (1/(p-1)) sum_{j=1}^{p-1} (j/p)^2 = (2p-1)/(6p) -> 1/3.
# So NO factor of 2 for the diagonal terms!

# What about cross terms? For m != m' (coprime):
# Riemann sum: (1/(p-1)) * T(m'/m) / p^2
# = (1/(p-1)) * [p(p-1)(3p-1)/12 average for off-diag] / p^2
# = (3p-1)/(12p) -> 1/4 (for average off-diagonal r)

# Integral: integral {mx}{m'x} for coprime m,m'
# This equals... let me compute for specific cases.

print("Integral of {mx}{m'x} vs Riemann sum at k/p:\n")
p = 89
print(f"Using p = {p}\n")
print(f"{'m':>4} {'m_pr':>4} {'integral':>10} {'riemann/(p-1)':>14} {'ratio':>8}")

for m, mp in [(1,2), (1,3), (1,5), (2,3), (2,5), (3,5), (3,7), (5,7), (1,10), (7,11)]:
    # Integral
    I = integral_sawtooth_product(m, mp, 1000000)

    # Riemann sum
    RS = sum(((m*k) % p) * ((mp*k) % p) for k in range(1, p)) / (p**2 * (p-1))

    print(f"{m:>4} {mp:>4} {I:>10.6f} {RS:>14.6f} {RS/I:>8.4f}")

# Same for diagonal
for m in [1, 2, 3, 5, 10, 20]:
    I = integral_sawtooth_product(m, m, 1000000)
    RS = sum(((m*k) % p)**2 for k in range(1, p)) / (p**2 * (p-1))
    print(f"{m:>4} {m:>4} {I:>10.6f} {RS:>14.6f} {RS/I:>8.4f}")

print("\n\n=== THE REAL MECHANISM ===\n")
# The factor of 2 does NOT come from individual sawtooth terms.
# It comes from the WEIGHTING by c_m = M(floor(N/m)) values.
#
# The key: c_m values are NOT generic. They have special structure:
# - c_m = M(floor(N/m)) is constant on blocks where floor(N/m) is constant
# - The blocks have sizes ~ N/m^2 (by hyperbolic spacing)
# - The LARGE c_m values cluster near m=1 (where M(N) contributes)
#
# E(k/p) = (p-k)/p - (1/p) sum_m c_m (mk mod p)
#
# The squared sum involves the quadratic form in c_m weighted by T(r):
# sum_E^2 = (1/p^2) [sum(p-k)^2 - 2*cross + sum T(r)*C(r)]
#
# The dominant term is sum T(r)*C(r) which involves the autocorrelation C(r).
#
# C(1) = sum c_m^2 >> C(r) for r != 1
# So the diagonal T(1)*C(1) dominates.
#
# But the FIRST term (sum(p-k)^2 / p^2) and the cross term also matter.
# Let me track all three terms and see which gives factor 2.

print("Tracking the three terms in sum_E^2 = (1/p^2)[T1 - 2*Term2 + Term3]")
print("and comparing with 2*(p-1)/n * sum_D^2")
print()

def farey_sequence(N):
    fracs = set()
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def mertens_values(N):
    mu = [0] * (N + 1)
    mu[1] = 1
    for i in range(1, N + 1):
        for j in range(2*i, N + 1, i):
            mu[j] -= mu[i]
    M = [0] * (N + 1)
    for k in range(1, N + 1):
        M[k] = M[k-1] + mu[k]
    return M, mu

for p in [47, 89, 127]:
    if not is_prime(p): continue
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    M, mu = mertens_values(N)
    c = [0]*(N+1)
    for m in range(1,N+1): c[m] = M[N//m]

    sum_D_sq = sum(float(Fraction(i,1) - n*f)**2 for i,f in enumerate(F_N))
    target = 2*(p-1)/n * sum_D_sq

    # E(k/p) = (p-k)/p - S(k)/p where S(k) = sum_m c_m (mk mod p)
    S_vals = []
    for k in range(1, p):
        S_vals.append(sum(c[m]*((m*k)%p) for m in range(1, N+1)))

    # Term 1: sum (p-k)^2 = p(p-1)(2p-1)/6
    t1 = sum((p-k)**2 for k in range(1, p))

    # Term 2: sum (p-k)*S(k)
    t2 = sum((p-k)*S_vals[k-1] for k in range(1, p))

    # Term 3: sum S(k)^2
    t3 = sum(s**2 for s in S_vals)

    sum_E_sq = (t1 - 2*t2 + t3) / p**2

    print(f"p={p}: n={n}")
    print(f"  T1/p^2 = {t1/p**2:.4f} (the 'k^2' term)")
    print(f"  2*T2/p^2 = {2*t2/p**2:.4f} (the cross term)")
    print(f"  T3/p^2 = {t3/p**2:.4f} (the S^2 term)")
    print(f"  sum_E^2 = {sum_E_sq:.4f}")
    print(f"  target = {target:.4f}")
    print(f"  ratio = {sum_E_sq/target:.6f}")

    # Now: what is the analog for sum_D^2?
    # sum_D^2 = sum_{f in F_N} D(f)^2
    # D(f) = rank(f) - n*f
    # For f = a/b, rank(f) = 1 + sum_m M(N/m) floor(ma/b)... this is the same structure

    # Actually the Franel identity: sum D(f)^2 = sum related to M(N/m)^2 values
    # specifically: sum (f_j - j/n)^2 involves M(N/m)

    # The key conceptual point:
    # E(k/p) for k=1,...,p-1 is the SAME function E(x) evaluated at p-1 equally-spaced points
    # D(f) for f in F_N is E(x) evaluated at n UNequally-spaced Farey points
    #
    # sum_D^2 = sum_{f in F_N} E(f)^2 (exact, since E(f) = D(f) for f in F_N)
    # sum_E^2 = sum_{k=1}^{p-1} E(k/p)^2
    #
    # The ratio sum_E_sq / [(p-1)/n * sum_D_sq]
    # = [mean of E^2 at p-grid] / [mean of E^2 at Farey grid]
    #
    # For an ARBITRARY function g, (1/(p-1)) sum g(k/p) ~ integral g
    # and (1/n) sum g(f_j) ~ integral g (by equidistribution of Farey fractions)
    # So the ratio should be 1, not 2!
    #
    # The factor of 2 arises because E(x) is NOT a smooth function --
    # it has JUMPS at the Farey fractions, and the Farey fractions form
    # the SAME set that defines E. This creates a systematic bias.

    # E(f_j^+) - E(f_j^-) = +1 for each Farey fraction f_j
    # D(f_j) = E(f_j) uses the RIGHT limit (post-jump).
    # Between Farey fractions, E decreases linearly with slope -n.

    # So the Farey-point average of E^2 OVERSEES the peaks (right after jumps)
    # compared to the continuous average (integral), which sees the full sawtooth.

    # Actually: the integral of E^2 = sum_D^2/n + something...
    # Let me check: integral E^2 vs sum_D^2/n more carefully.

    # integral E^2 from the piecewise formula
    integral = 0
    for j in range(len(F_N)-1):
        a = float(F_N[j])
        b_val = float(F_N[j+1])
        c_j = j + 1  # E(x) = c_j - n*x on (f_j, f_{j+1}]
        integral += c_j**2*(b_val-a) - c_j*n*(b_val**2-a**2) + n**2*(b_val**3-a**3)/3

    # And E(f_j) = j - n*f_j = D(f_j) is the LEFT-continuous value
    # Actually E(f_j) uses the count of fractions <= f_j, which includes f_j itself.
    # So E(f_j) = j + 1 - n*f_j... wait, I need to be careful.
    # E(x) = #{f in F_N : f <= x} - nx. At x = f_j (the j-th fraction, 0-indexed):
    # #{f <= f_j} = j + 1 (since 0-indexed, f_0,...,f_j are j+1 fractions)
    # So E(f_j) = (j+1) - n*f_j
    # But D(f_j) = rank(f_j) - n*f_j where rank starts at 0: rank(f_j) = j
    # So D(f_j) = j - n*f_j = E(f_j) - 1.

    # Hmm! D(f) = E(f) - 1? That changes things.
    # Let me recheck. E(x) = N_{F_N}(x) - nx where N counts fractions <= x.
    # At x = f_j: N(f_j) = j+1 (for 0-indexed f_0,...,f_{n-1}).
    # D(f_j) = rank(f_j) - n*f_j = j - n*f_j.
    # So E(f_j) = j + 1 - n*f_j = D(f_j) + 1.

    # That means sum_{f in F_N} E(f)^2 = sum (D(f)+1)^2 = sum_D^2 + 2*sum_D + n
    # and sum_D = sum (j - n*f_j) = sum j - n*sum f_j = n(n-1)/2 - n*n/2 = -n/2
    # (since sum f_j = n/2 by symmetry of Farey sequence)
    # So sum E(f)^2 = sum_D^2 + 2*(-n/2) + n = sum_D^2 - n + n = sum_D^2.
    # Great, so sum E(f_j)^2 = sum D(f_j)^2 despite the shift by 1, because the cross term cancels!

    E_at_farey = [(j+1) - n*float(F_N[j]) for j in range(n)]
    sum_E_at_farey = sum(e**2 for e in E_at_farey)
    print(f"\n  sum E(f_j)^2 = {sum_E_at_farey:.4f}, sum D^2 = {sum_D_sq:.4f}")

    # So the question is really: why does the p-grid average of E^2 differ from
    # the Farey-grid average by factor 2?
    #
    # Grid average of E^2 at p-points: (1/(p-1)) sum_k E(k/p)^2
    # Grid average of E^2 at Farey points: (1/n) sum_j E(f_j)^2 = sum_D^2/n
    # Continuous average: integral_0^1 E(x)^2 dx
    #
    # Empirically:
    # integral ~ sum_D^2/n (Farey equidistribution: E at Farey points ~ continuous avg)
    # p-grid avg ~ 2 * integral (the factor of 2!)

    grid_avg = sum_E_sq / (p - 1)
    farey_avg = sum_D_sq / n
    print(f"  p-grid avg E^2 = {grid_avg:.4f}")
    print(f"  Farey avg E^2 = {farey_avg:.4f}")
    print(f"  integral E^2 = {integral:.4f}")
    print(f"  p-grid / integral = {grid_avg / integral:.6f}")
    print(f"  Farey / integral = {farey_avg / integral:.6f}")
    print()

    # KEY FINDING: Farey avg ~ integral (both ~ 1.0), p-grid avg ~ 2*integral.
    # The factor of 2 is a RIEMANN SUM PHENOMENON for the specific function E(x)
    # evaluated at the specific grid k/p.

    # WHY does the Riemann sum double?
    # E(x) is a sawtooth with jumps at Farey fractions. Between consecutive
    # Farey fractions f_j, f_{j+1} (gap ~ 1/N^2), E decreases from ~D(f_j)+1
    # to ~D(f_{j+1}).
    #
    # A point k/p falls in ONE Farey gap. The value E(k/p) depends on WHERE
    # in the gap it falls. If uniformly distributed, E(k/p)^2 should average
    # to the integral of E^2 over that gap.
    #
    # But k/p is NOT uniformly placed in Farey gaps! The relationship between
    # the p-grid and the Farey grid is STRUCTURED (not random).
    #
    # Specifically: k/p falls in the gap (a1/b1, a2/b2) where a1/b1, a2/b2 are
    # Farey neighbors with b1+b2 > N but b1,b2 <= N. The distance from k/p to
    # the nearer endpoint is related to |a1*p - k*b1|/p.

    # Actually, the factor of 2 was already observed in PROOF_BREAKTHROUGH.md
    # and attributed to the BOUNDARY terms E(1/p) and E((p-1)/p) which are
    # large because E(x) has its global extrema near x=0 and x=1.

    # Let me quantify: what fraction of sum_E^2 comes from the two boundary points?
    E_1 = E_at_farey[0] if len(E_at_farey) > 0 else 0  # This is E at f_0=0, not k=1
    # No, we need E(1/p) and E((p-1)/p)
    E_k1 = float(sum(1 for f in F_N if f <= Fraction(1,p)) - n*Fraction(1,p))
    E_kpm1 = float(sum(1 for f in F_N if f <= Fraction(p-1,p)) - n*Fraction(p-1,p))
    bdy_sq = E_k1**2 + E_kpm1**2
    bdy_frac = bdy_sq / sum_E_sq
    interior_sq = sum_E_sq - bdy_sq
    interior_avg = interior_sq / (p - 3)

    print(f"  E(1/p) = {E_k1:.4f}, E((p-1)/p) = {E_kpm1:.4f}")
    print(f"  Boundary sum / total = {bdy_frac:.4f}")
    print(f"  Interior per-point avg = {interior_avg:.4f}")
    print(f"  Farey avg = {farey_avg:.4f}")
    print(f"  Interior / Farey = {interior_avg / farey_avg:.4f}")
    print(f"  Each boundary E^2 / sum_D^2 = {E_k1**2 / sum_D_sq:.4f}")

    # So boundary contributes ~ 55% of total, and each boundary point has E^2 ~ sum_D^2.
    # The interior (p-3 points) has average ~ farey average.
    # Total = 2 * (sum_D^2) + (p-3) * (sum_D^2/n) approx
    # = sum_D^2 * (2 + (p-3)/n)
    # = sum_D^2 * (2 + p/n) approximately
    # Ratio = sum_E^2 / ((p-1)/n * sum_D^2) = n/(p-1) * (2 + p/n) = 2n/(p-1) + p/(p-1)
    # For large p: 2 * (3p^2/pi^2) / p + 1 = 6p/pi^2 + 1 >> 2.
    # That's too big! So the boundary contribution is NOT as simple as E^2 ~ sum_D^2.

    print(f"  E(1/p)^2 = {E_k1**2:.4f}, n*farey_avg = {n*farey_avg:.4f}")
    print(f"  E(1/p)^2 / (n*farey_avg) = {E_k1**2 / (n*farey_avg):.4f}")
    # E(1/p) ~ n/p (since N_{F_N}(1/p) ~ 1 for p > N, so E(1/p) ~ 1 - n/p)
    # Actually E(1/p) = #{f <= 1/p} - n/p. The fractions <= 1/p in F_N are: 0/1
    # and possibly 1/b for b >= p (but b <= N = p-1 < p). So 1/b > 1/p for all b <= N.
    # Wait, 1/N = 1/(p-1) > 1/p. And 1/(N-1) = 1/(p-2) > 1/p. So all 1/b > 1/p for b <= N.
    # Hence #{f <= 1/p} = 1 (just 0/1). So E(1/p) = 1 - n/p ~ -3p/pi^2.
    # E(1/p)^2 ~ 9p^2/pi^4.
    # And n*farey_avg = sum_D^2/1 ... wait, n * farey_avg = sum_D^2.
    # E(1/p)^2 / sum_D^2 ~ 9p^2/pi^4 / (n * C_W) ~ 9p^2 / (pi^4 * 3p^2/pi^2 * C_W)
    # = 9 / (3 * pi^2 * C_W) = 3/(pi^2 C_W).
    # For C_W ~ 0.5: ~ 0.6. So E(1/p)^2 ~ 0.6 * sum_D^2. This checks out!

    print()
