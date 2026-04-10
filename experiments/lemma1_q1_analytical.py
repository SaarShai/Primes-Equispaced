"""
Analytical decomposition of K[N] - K[N/2].

K_diff = sum_{f in F_N^*} [sum_{j=N/2+1}^N {jf}] * delta(f)

Since sum_f delta(f) = 0, the mean of {jf} cancels:
K_diff = sum_f [sum_{j=N/2+1}^N ({jf} - 1/2)] * delta(f)

Key identity for f=a/b with gcd(a,b)=1:
  sum_{j=1}^m {ja/b} = (m(b-1))/(2b) + correction

The correction involves Dedekind sums. But we can be more direct.

For a FIXED denominator b, the sequence {ja/b} for j=1,...,b is a permutation
of {1/b, 2/b, ..., (b-1)/b, 0}. So over a full period:
  sum_{j=1}^b {ja/b} = (b-1)/2

Over m terms: sum_{j=1}^m {ja/b} = q*(b-1)/2 + sum_{j=1}^r {ja/b}
where m = q*b + r.

The "half-sum" deviation from mean is:
  H(f) = sum_{j=N/2+1}^N ({jf} - 1/2)

Let's compute H(f) and correlate with delta(f), decomposed by denominator.

Also: K_1 = sum_f f*delta(f) = C'/2 (proved).
And K_2 - K_1 = sum_f {2f}*delta(f).

For the q=1 block, we need:
K_diff = sum_f [sum_{j=N/2+1}^N {jf}] * delta(f)

This is a sum of (N - N/2) = N/2 "kernel increments":
K_diff = sum_{j=N/2+1}^N [sum_f {jf} * delta(f)]
       = sum_{j=N/2+1}^N DeltaK_j

where DeltaK_j = K_j - K_{j-1} = sum_f {jf} * delta(f).

So K_diff = sum_{j=N/2+1}^N DeltaK_j.

Question: Is each DeltaK_j positive? Or is it the sum that's positive?
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

def analyze_increments(p):
    """Analyze DeltaK_j = sum_f {jf} * delta(f) for each j."""
    N = p - 1
    N2 = N // 2
    fracs = farey_interior(N)
    deltas = {f: delta_p(f, p) for f in fracs}
    Cprime = sum(d*d for d in deltas.values())

    print(f"\np = {p}, N = {N}")

    # Compute DeltaK_j for j = 1, ..., N
    DeltaK = {}
    for j in range(1, N+1):
        val = Fraction(0)
        for f in fracs:
            jf = j * f
            fp = jf - int(jf)
            if fp < 0:
                fp += 1
            val += fp * deltas[f]
        DeltaK[j] = val

    # Verify K_1
    assert DeltaK[1] == Cprime / 2, f"K_1 check failed"

    # Count positive/negative among j > N/2
    pos_count = 0
    neg_count = 0
    pos_sum = Fraction(0)
    neg_sum = Fraction(0)
    for j in range(N2+1, N+1):
        if DeltaK[j] > 0:
            pos_count += 1
            pos_sum += DeltaK[j]
        elif DeltaK[j] < 0:
            neg_count += 1
            neg_sum += DeltaK[j]

    K_diff = sum(DeltaK[j] for j in range(N2+1, N+1))
    print(f"DeltaK_j for j in [{N2+1}, {N}]: {pos_count} positive, {neg_count} negative")
    print(f"  Positive sum: {float(pos_sum/Cprime):.4f} C'")
    print(f"  Negative sum: {float(neg_sum/Cprime):.4f} C'")
    print(f"  Net: {float(K_diff/Cprime):.4f} C'")

    # Show DeltaK_j / C' for j around N/2 and near N
    print(f"\n  DeltaK_j / C' for first few j > N/2:")
    for j in range(N2+1, min(N2+11, N+1)):
        print(f"    j={j}: {float(DeltaK[j]/Cprime):.6f}")
    print(f"  ...")
    print(f"  DeltaK_j / C' for last few j:")
    for j in range(max(N-4, N2+1), N+1):
        print(f"    j={j}: {float(DeltaK[j]/Cprime):.6f}")

    # Key question: What's special about j that are multiples of denominators?
    # For j = b (a denominator), {j*a/b} = 0, so that Farey fraction contributes 0.
    # For j coprime to b, {ja/b} runs through residues.

    # Average DeltaK_j for j > N/2
    avg = float(K_diff / Cprime) / (N - N2)
    print(f"\n  Average DeltaK_j/C' = {avg:.6f}")
    print(f"  Expected if DeltaK_j ~ C'/(2N): {1.0/(2*N):.6f}")

    # The ratio K_diff/C' should be ~ sum_{j=N/2+1}^N DeltaK_j/C'
    # If DeltaK_j/C' ~ 1/(pi^2 * j) or similar...
    # Let's check the relationship DeltaK_j vs j

    # Group by j and check if DeltaK_j depends on j
    print(f"\n  DeltaK_j/C' averaged over 5-element windows:")
    window = 5
    for start in range(N2+1, N+1, window):
        end = min(start + window, N+1)
        avg_w = sum(float(DeltaK[j]/Cprime) for j in range(start, end)) / (end - start)
        print(f"    j in [{start},{end-1}]: avg = {avg_w:.6f}")

    return DeltaK, Cprime

# Run for small primes
for p in [43, 71, 107]:
    analyze_increments(p)
