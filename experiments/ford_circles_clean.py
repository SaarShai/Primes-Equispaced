#!/usr/bin/env python3
"""Ford circles verification: hyperbolic equilateral property + Stern-Brocot depth correlation."""
import math
from fractions import Fraction

def farey(n):
    """Generate Farey sequence F_n."""
    a, b, c, d = 0, 1, 1, n
    seq = [Fraction(0, 1)]
    while c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        seq.append(Fraction(a, b))
    return seq

def sb_depth(frac):
    """Stern-Brocot depth = sum of CF partial quotients."""
    if frac == 0: return 1
    if frac == 1: return 1
    a, b = frac.numerator, frac.denominator
    depth = 0
    while b > 0:
        depth += a // b
        a, b = b, a % b
    return depth

def hyp_dist(f1, f2):
    """Hyperbolic distance between two points on real line (Ford circle model)."""
    b1, b2 = f1.denominator, f2.denominator
    dx = abs(float(f2 - f1))
    return 2 * math.asinh(dx * b1 * b2)

N = 31
PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31]

# 1. Verify all Farey neighbors have equal hyperbolic distance
seq = farey(N)
dists = []
for i in range(len(seq) - 1):
    d = hyp_dist(seq[i], seq[i+1])
    dists.append(d)

print(f"F_{N}: {len(seq)} fractions, {len(dists)} neighbor pairs")
print(f"Hyperbolic distances: min={min(dists):.6f}, max={max(dists):.6f}, mean={sum(dists)/len(dists):.6f}")
print(f"All equal? {max(dists) - min(dists) < 1e-10}")
print(f"Value = 2*arcsinh(1) = {2*math.asinh(1):.6f}")
print()

# 2. For each prime step, compute depth vs |ΔW contribution|
for p in PRIMES:
    fp = farey(p)
    fpm1 = farey(p - 1)
    new_fracs = [f for f in fp if f not in set(fpm1)]

    # Compute ΔW contribution for each new fraction
    # D(f) = rank in F_{p-1} (interpolated) - |F_{p-1}|*f
    n_pm1 = len(fpm1)

    depth_contrib = []
    for f in new_fracs:
        depth = sb_depth(f)
        # Find neighbors in F_{p-1}
        fval = float(f)
        # Rank = number of F_{p-1} fractions ≤ f
        rank = sum(1 for x in fpm1 if x <= f)
        D = rank - n_pm1 * fval
        # delta = distance to predecessor in F_p
        idx = fp.index(f)
        if idx > 0:
            delta = float(f - fp[idx-1])
        else:
            delta = float(f)
        contrib = abs(D * delta)
        depth_contrib.append((depth, contrib, D, delta))

    if depth_contrib:
        depths = [x[0] for x in depth_contrib]
        contribs = [x[1] for x in depth_contrib]
        # Correlation
        if len(depths) > 1:
            mean_d = sum(depths)/len(depths)
            mean_c = sum(contribs)/len(contribs)
            cov = sum((d-mean_d)*(c-mean_c) for d,c in zip(depths, contribs))
            var_d = sum((d-mean_d)**2 for d in depths)
            var_c = sum((c-mean_c)**2 for c in contribs)
            if var_d > 0 and var_c > 0:
                corr = cov / math.sqrt(var_d * var_c)
            else:
                corr = 0.0
        else:
            corr = 0.0
        print(f"p={p:3d}: {len(new_fracs):4d} new fracs, avg_depth={sum(depths)/len(depths):.2f}, "
              f"avg_|Dδ|={sum(contribs)/len(contribs):.6f}, corr(depth,|Dδ|)={corr:+.3f}")
