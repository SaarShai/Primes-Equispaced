"""
Lemma 1: The q=1 block K[N] - K[floor(N/2)] is positive and Theta(C').

Compute exactly using Fraction arithmetic for p = 13, 43, 71, 107.

K_m(p) = sum_{f in F_N^*} S(f,m) * delta_p(f)
S(f,m) = sum_{j=1}^m {j*f}

delta_p(a/b) = ([p(b-a)]_b - (b-a)) / b

C'(p) = sum delta_p(f)^2

K[N] - K[floor(N/2)] = sum_f [S(f,N) - S(f,floor(N/2))] * delta_p(f)
                      = sum_f [sum_{j=floor(N/2)+1}^N {j*f}] * delta_p(f)
"""

from fractions import Fraction
import math

def farey_sequence(N):
    """Generate F_N^* (interior Farey fractions, excluding 0/1 and 1/1)."""
    fracs = set()
    for b in range(2, N+1):
        for a in range(1, b):
            if math.gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def delta_p(f, p):
    """Compute delta_p(a/b) = ([p(b-a)]_b - (b-a)) / b."""
    a = f.numerator
    b = f.denominator
    bma = b - a
    residue = (p * bma) % b
    if residue == 0:
        residue = b  # least positive residue
    return Fraction(residue - bma, b)

def frac_part(x):
    """Fractional part {x} = x - floor(x), always in [0,1)."""
    return x - int(x) if x >= 0 else x - int(x) + (0 if x == int(x) else 1)

def frac_part_exact(x):
    """Exact fractional part for Fraction."""
    # {x} = x - floor(x), in [0,1)
    fl = x.__floor__()
    r = x - fl
    if r < 0:
        r += 1
    return r

def S_value(f, m):
    """Compute S(f, m) = sum_{j=1}^m {j*f} exactly."""
    total = Fraction(0)
    for j in range(1, m+1):
        jf = j * f
        fp = jf - int(jf)  # {j*f}
        if fp < 0:
            fp += 1
        total += fp
    return total

def compute_all(p):
    """Compute K[N], K[floor(N/2)], their difference, and C' for prime p."""
    N = p - 1
    N2 = N // 2

    fracs = farey_sequence(N)
    print(f"\n{'='*60}")
    print(f"p = {p}, N = {N}, floor(N/2) = {N2}")
    print(f"|F_N^*| = {len(fracs)}")

    # Compute deltas
    deltas = {}
    for f in fracs:
        deltas[f] = delta_p(f, p)

    # C' = sum delta^2
    Cprime = sum(d*d for d in deltas.values())
    print(f"C' = {float(Cprime):.6f}")

    # K[N] = sum_f S(f, N) * delta(f)
    # K[N2] = sum_f S(f, N2) * delta(f)
    # Difference = sum_f [S(f,N) - S(f,N2)] * delta(f)
    #            = sum_f [sum_{j=N2+1}^N {jf}] * delta(f)

    K_N = Fraction(0)
    K_N2 = Fraction(0)
    K_diff = Fraction(0)

    # Also track the "half-sum" part: sum_{j=N2+1}^N {jf} for each f
    half_sums = {}

    for f in fracs:
        d = deltas[f]

        # Compute S(f, N) and S(f, N2)
        s_N = Fraction(0)
        s_N2 = Fraction(0)

        for j in range(1, N+1):
            jf = j * f
            fp = jf - int(jf)
            if fp < 0:
                fp += 1
            s_N += fp
            if j <= N2:
                s_N2 += fp

        half_sum = s_N - s_N2  # sum_{j=N2+1}^N {jf}
        half_sums[f] = half_sum

        K_N += s_N * d
        K_N2 += s_N2 * d
        K_diff += half_sum * d

    # Verify K_diff = K_N - K_N2
    assert K_diff == K_N - K_N2, "Consistency check failed!"

    print(f"K[N] = {float(K_N):.6f}")
    print(f"K[N/2] = {float(K_N2):.6f}")
    print(f"K[N] - K[N/2] = {float(K_diff):.6f}")
    print(f"(K[N]-K[N/2]) / C' = {float(K_diff / Cprime):.6f}")
    print(f"Sign: {'POSITIVE' if K_diff > 0 else 'NEGATIVE'}")

    # Decompose: which fractions contribute most?
    # K_diff = sum_f half_sum(f) * delta(f)
    # The half_sum averages to (N-N2)/2 = N/4 per term
    # But delta sums to 0, so the leading N/4 cancels

    # Let's compute the "mean-subtracted" version
    mean_half = Fraction(N - N2, 2)  # average of {jf} is 1/2, times (N-N2) terms

    # K_diff = sum_f half_sum(f) * delta(f)
    #        = sum_f [half_sum(f) - mean_half] * delta(f) + mean_half * sum delta(f)
    #        = sum_f [half_sum(f) - mean_half] * delta(f)   [since sum delta = 0]

    sum_delta = sum(deltas.values())
    assert sum_delta == 0, f"Sum delta should be 0, got {sum_delta}"

    fluctuation_contrib = Fraction(0)
    for f in fracs:
        fluctuation_contrib += (half_sums[f] - mean_half) * deltas[f]

    assert fluctuation_contrib == K_diff, "Fluctuation decomposition check failed!"
    print(f"\nMean half-sum = {float(mean_half):.4f}")
    print(f"Fluctuation correlation = {float(K_diff):.6f}")
    print(f"  (confirms: K_diff comes entirely from correlation, not mean)")

    # Correlation coefficient: Corr(half_sum, delta)
    var_half = sum((half_sums[f] - mean_half)**2 for f in fracs) / len(fracs)
    var_delta = Cprime / len(fracs)  # since mean delta = 0
    cov = K_diff / len(fracs)
    if var_half > 0 and var_delta > 0:
        corr = float(cov) / (float(var_half)**0.5 * float(var_delta)**0.5)
        print(f"Correlation(half_sum_deviation, delta) = {corr:.4f}")

    # Decompose by denominator
    print(f"\nContribution by denominator b:")
    by_denom = {}
    for f in fracs:
        b = f.denominator
        if b not in by_denom:
            by_denom[b] = Fraction(0)
        by_denom[b] += (half_sums[f] - mean_half) * deltas[f]

    for b in sorted(by_denom.keys()):
        val = by_denom[b]
        if abs(float(val)) > 0.001 * abs(float(Cprime)):
            print(f"  b={b}: {float(val):.6f} ({float(val/Cprime):.4f} C')")

    # Key insight: for b > N/2, delta = (p mod b - (b-a))/b type terms
    # and half_sum deviates from mean in a structured way

    # Separate positive and negative contributions
    pos_contrib = Fraction(0)
    neg_contrib = Fraction(0)
    for f in fracs:
        c = (half_sums[f] - mean_half) * deltas[f]
        if c > 0:
            pos_contrib += c
        else:
            neg_contrib += c

    print(f"\nPositive contributions: {float(pos_contrib):.6f} ({float(pos_contrib/Cprime):.4f} C')")
    print(f"Negative contributions: {float(neg_contrib):.6f} ({float(neg_contrib/Cprime):.4f} C')")
    print(f"Net (K_diff): {float(K_diff):.6f} ({float(K_diff/Cprime):.4f} C')")

    # Also verify K_1 = C'/2
    K_1 = sum(frac_part_exact(f) * deltas[f] for f in fracs)
    # Wait, K_1 = sum_f S(f,1)*delta(f) = sum_f {f}*delta(f) = sum_f f*delta(f)
    # since for f in (0,1), {f} = f
    K_1_check = sum(f * deltas[f] for f in fracs)
    print(f"\nK_1 = {float(K_1_check):.6f}, C'/2 = {float(Cprime/2):.6f}, match: {K_1_check == Cprime/2}")

    return {
        'p': p, 'N': N, 'Cprime': Cprime,
        'K_N': K_N, 'K_N2': K_N2, 'K_diff': K_diff,
        'ratio': K_diff / Cprime
    }

# Run for requested primes
results = []
for p in [13, 43, 71, 107]:
    r = compute_all(p)
    results.append(r)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
cprime_label = "C'"
ratio_label = "K_diff/C'"
print(f"{'p':>5} {'N':>5} {cprime_label:>12} {'K_diff':>12} {ratio_label:>12} {'Sign':>8}")
for r in results:
    print(f"{r['p']:>5} {r['N']:>5} {float(r['Cprime']):>12.6f} {float(r['K_diff']):>12.6f} {float(r['ratio']):>12.6f} {'POS' if r['K_diff'] > 0 else 'NEG':>8}")
