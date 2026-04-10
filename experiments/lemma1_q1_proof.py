"""
Analytical proof of K[N] - K[N/2] > 0 and = Theta(C').

KEY IDENTITY:
K_diff = sum_{b=2}^{N} sum_{a: gcd(a,b)=1, a<b} [sum_{j=N/2+1}^N {ja/b}] * delta_p(a/b)

For fixed b, the inner sum over j is:
  T_b(a) := sum_{j=N/2+1}^N {ja/b}

Since {ja/b} depends only on (ja mod b)/b, and as j ranges over N/2+1,...,N
(that's N/2 consecutive values), T_b(a) can be computed via the periodicity mod b.

Write N/2 = q*b + r. Then T_b(a) sums over q full periods plus r extra terms.
Over one full period sum_{j=1}^b {ja/b} = (b-1)/2.
So the "mean" contribution is (N/2)(b-1)/(2b) = N(b-1)/(4b).

The deviation T_b(a) - N(b-1)/(4b) is a Dedekind-type quantity.

But we need the CORRELATION of T_b with delta, summed over a coprime to b.

Let's compute the per-b contribution:
  C_b = sum_{a coprime to b, a<b} T_b(a) * delta(a/b)

And verify:
  K_diff = sum_b C_b

Also compute:
  D_b = sum_{a coprime to b, a<b} delta(a/b)^2  (contribution to C')

If C_b / D_b is roughly constant, that gives us the proof.
"""

from fractions import Fraction
import math

def delta_p(a, b, p):
    bma = b - a
    res = (p * bma) % b
    if res == 0:
        res = b
    return Fraction(res - bma, b)

def compute_per_b(p):
    N = p - 1
    N2 = N // 2

    results = []
    total_Cb = Fraction(0)
    total_Db = Fraction(0)

    for b in range(2, N+1):
        Cb = Fraction(0)
        Db = Fraction(0)
        count = 0

        for a in range(1, b):
            if math.gcd(a, b) != 1:
                continue
            count += 1

            d = delta_p(a, b, p)
            Db += d * d

            # T_b(a) = sum_{j=N2+1}^N {ja/b}
            Tb = Fraction(0)
            for j in range(N2+1, N+1):
                ja_mod_b = (j * a) % b
                Tb += Fraction(ja_mod_b, b)

            Cb += Tb * d

        if count > 0 and Db > 0:
            total_Cb += Cb
            total_Db += Db
            if abs(float(Cb)) > 0.01:
                ratio = float(Cb / Db) if Db > 0 else 0
                results.append((b, count, float(Cb), float(Db), ratio))

    Cprime = float(total_Db)
    K_diff = float(total_Cb)
    print(f"\np = {p}, N = {N}")
    print(f"K_diff = {K_diff:.6f}, C' = {Cprime:.6f}, ratio = {K_diff/Cprime:.6f}")

    # Show per-b ratios C_b / D_b
    print(f"\n{'b':>4} {'phi(b)':>6} {'C_b':>12} {'D_b':>12} {'C_b/D_b':>10} {'D_b/Cp':>8}")
    for b, cnt, cb, db, ratio in sorted(results, key=lambda x: -abs(x[2])):
        if abs(cb) > 0.5:
            print(f"{b:>4} {cnt:>6} {cb:>12.4f} {db:>12.4f} {ratio:>10.4f} {db/Cprime:>8.4f}")

    # Key check: is C_b/D_b ~ constant?
    # If so, K_diff/C' ~ that constant.
    ratios_weighted = []
    for b, cnt, cb, db, ratio in results:
        if db > 0.01 * Cprime:  # significant contributors
            ratios_weighted.append((ratio, db / Cprime))
            print(f"  b={b}: C_b/D_b = {ratio:.4f} (weight {db/Cprime:.3f})")

    return results

for p in [43, 71, 107]:
    compute_per_b(p)
