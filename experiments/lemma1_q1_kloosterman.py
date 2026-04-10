"""
K[N] - K[N/2] via Fourier/Kloosterman decomposition.

Key idea: delta_p(a/b) depends on p mod b. Specifically:
  delta_p(a/b) = ([p(b-a)]_b - (b-a)) / b

Let c = b-a. Then delta = ([pc]_b - c)/b.

Now [pc]_b = pc mod b (least positive residue). So:
  delta = (pc mod b - c)/b = ((p-1)c mod b + [something])/b

Actually: pc mod b - c = c(p-1) mod b when we're careful.
Let r = p mod b. Then pc mod b = rc mod b.
So delta = (rc mod b - c)/b = c(r-1) mod b / b ... no, need to be more careful.

pc mod b: this is the unique value in {1,...,b} congruent to pc mod b
(since gcd(c,b) = gcd(b-a,b) = gcd(a,b) = 1, so c is coprime to b).

pc mod b = (p mod b)(c mod b) mod b = r*c mod b where r = p mod b.

So delta(a/b) = (r*c mod b - c) / b where c = b-a and r = p mod b.

This is purely a function of r = p mod b and c = b - a.

For the q=1 block:
K_diff = sum_f [sum_{j=N/2+1}^N {jf}] * delta(f)

The inner sum sum_{j=N/2+1}^N {ja/b} depends on a, b, N.

Let's think about it differently. The KEY insight is:

K_diff = sum_{j=N/2+1}^N DeltaK_j

where DeltaK_j = sum_f {jf} * delta(f).

Now DeltaK_j = sum_{b=2}^N sum_{a coprime to b, a<b} {ja/b} * delta(a/b).

For j coprime to b: as a runs over residues coprime to b,
ja mod b also runs over ALL residues coprime to b.
So sum_{a coprime to b} {ja/b} * delta(a/b) = sum_{a coprime to b} (ja mod b)/b * delta(a/b).

When gcd(j,b) = 1, this equals sum_{a'} (a'/b) * delta(j^{-1}a'/b)
where a' = ja mod b runs over coprime residues.

Hmm, this substitution doesn't simplify much without knowing delta's structure.

Let me try a more direct approach: compute DeltaK_j decomposed by b,
and identify which denominators b contribute positively/negatively.

For b | j: {ja/b} = 0 for all a, so denominator b contributes 0 to DeltaK_j.

For b not dividing j: sum_{a coprime to b, a<b} {ja/b} * delta(a/b) is nonzero.

The key observation from data: DeltaK_j is MORE POSITIVE for j near N
than for j near N/2. Why?

For large j (close to N), more denominators b satisfy b > j (so j < b),
meaning {ja/b} = ja/b (no floor needed since ja < b^2 but ja/b could be > 1).
Actually for j < b, ja < ab < b^2, so {ja/b} is just ja/b minus floor(ja/b).
For j > b, we get wrapping.

The correlation between {jf} and delta should be STRONGER for large j
because both quantities are "modular" and the alignment improves.

Let me test this numerically: is DeltaK_j an increasing function of j?
"""

from fractions import Fraction
import math

def farey_interior(N):
    fracs = set()
    for b in range(2, N+1):
        for a in range(1, b):
            if math.gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def delta_p(f, p):
    a, b = f.numerator, f.denominator
    bma = b - a
    res = (p * bma) % b
    if res == 0:
        res = b
    return Fraction(res - bma, b)

def analyze_deltaK_trend(p):
    N = p - 1
    N2 = N // 2
    fracs = farey_interior(N)
    deltas = {f: delta_p(f, p) for f in fracs}
    Cprime = sum(d*d for d in deltas.values())

    # Compute DeltaK_j for ALL j
    DK = []
    for j in range(1, N+1):
        val = Fraction(0)
        for f in fracs:
            jf = j * f
            fp = jf - int(jf)
            val += fp * deltas[f]
        DK.append(float(val / Cprime))

    # Compute running average
    print(f"\np = {p}, N = {N}")
    print(f"DeltaK_1/C' = {DK[0]:.6f} (should be 0.5 = K_1/C')")

    # Average DeltaK over windows
    w = max(1, N // 10)
    print(f"\nRunning average (window={w}):")
    for start in range(0, N, w):
        end = min(start + w, N)
        avg = sum(DK[start:end]) / (end - start)
        print(f"  j in [{start+1},{end}]: avg DeltaK_j/C' = {avg:.6f}")

    # Cumulative: K_m/C'
    K_vals = []
    cumsum = 0.0
    for j in range(N):
        cumsum += DK[j]
        K_vals.append(cumsum)

    print(f"\nK_N/C' = {K_vals[-1]:.6f}")
    print(f"K_{N2}/C' = {K_vals[N2-1]:.6f}")
    print(f"K_diff/C' = {K_vals[-1] - K_vals[N2-1]:.6f}")

    # Test: is mean DeltaK_j for j > N/2 greater than for j <= N/2?
    first_half_avg = sum(DK[:N2]) / N2
    second_half_avg = sum(DK[N2:]) / (N - N2)
    print(f"\nAvg DeltaK_j/C' for j <= N/2: {first_half_avg:.6f}")
    print(f"Avg DeltaK_j/C' for j > N/2: {second_half_avg:.6f}")

    # The K_diff/C' should equal (N-N2) * second_half_avg
    print(f"Check: (N-N2) * avg = {(N-N2) * second_half_avg:.6f}")

    # Overall mean
    overall_mean = sum(DK) / N
    print(f"Overall mean DeltaK_j/C' = {overall_mean:.6f}")
    print(f"  = K_N / (N * C') = {K_vals[-1] / N:.6f}")

    return DK

for p in [43, 71, 107]:
    analyze_deltaK_trend(p)
