"""
Analytical lower bound for K[N] - K[N/2] via Cauchy-Schwarz.

We have:
  K_diff = sum_f H(f) * delta(f)

where H(f) = sum_{j=N/2+1}^N {jf} and delta sums to 0.

Since sum delta = 0, we can write:
  K_diff = sum_f (H(f) - H_mean) * delta(f) = sum_f H(f) * delta(f)

where H_mean = (1/|F|) sum_f H(f) doesn't matter because it multiplies sum delta = 0.

By Cauchy-Schwarz:
  K_diff^2 <= [sum H(f)^2] * [sum delta(f)^2] = [sum H(f)^2] * C'

This gives an UPPER bound, not a lower bound. Not helpful directly.

Instead, let's try to prove positivity via a structural argument.

KEY STRUCTURAL FACT:
  DeltaK_j = sum_f {jf} * delta(f)

For j = 1: DeltaK_1 = sum_f f * delta(f) = C'/2 (PROVED, this is K_1 = C'/2).

For j = N (= p-1):
  DeltaK_N = sum_f {(p-1)f} * delta(f) = sum_f {-f + pf} * delta(f)
           = sum_f {pf - f} * delta(f)

Now pf = p*a/b. Since gcd(a,b)=1 and b<=N=p-1<p:
  p*a/b has fractional part = (pa mod b)/b.

And (p-1)*a/b = pa/b - a/b.
{(p-1)a/b} = {pa/b - a/b}.

Hmm, let me compute DeltaK_N directly.

Actually, {(p-1)a/b} = {-a/b} mod 1 (when p = 1 mod b) ... no, (p-1)a/b:
For b <= p-1, (p-1)a = pa - a.
(pa mod b) = pa - b*floor(pa/b).
((p-1)a mod b) = (pa - a) mod b = (pa mod b - a mod b) mod b.

Since a < b, a mod b = a. And pa mod b = r*a mod b where r = p mod b.
So (p-1)a mod b = ((r-1)*a) mod b.

If r = p mod b = 1 (i.e., b | (p-1) = N, which means b | N):
  (p-1)a mod b = 0, so {(p-1)a/b} = 0 ... wait, but then DeltaK_N for those f is 0.

Actually when b | N, then N*a/b is an integer, so {Na/b} = 0.

So for b | N: the contribution to DeltaK_N is zero.
For b not dividing N: {Na/b} = {(p-1)a/b} is nonzero.

Let me compute something simpler: what fraction of C' comes from denominators
b that divide N? And what does K_diff look like restricted to b not dividing N?
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

def structural_analysis(p):
    N = p - 1
    N2 = N // 2
    fracs = farey_interior(N)
    deltas = {f: delta_p(f, p) for f in fracs}
    Cprime = sum(d*d for d in deltas.values())

    print(f"\n{'='*60}")
    print(f"p = {p}, N = {N}")

    # For each f = a/b, compute:
    #   H(f) = sum_{j=N/2+1}^N {jf}
    #   H(f) - N/4 = fluctuation
    # And also delta(f)^2, H(f)*delta(f)

    # Split by: b <= N/2 vs b > N/2
    K_diff_low_b = Fraction(0)
    K_diff_high_b = Fraction(0)
    Cprime_low = Fraction(0)
    Cprime_high = Fraction(0)

    for f in fracs:
        b = f.denominator
        d = deltas[f]
        H = Fraction(0)
        for j in range(N2+1, N+1):
            jf = j * f
            fp = jf - int(jf)
            H += fp
        contrib = H * d

        if b <= N2:
            K_diff_low_b += contrib
            Cprime_low += d * d
        else:
            K_diff_high_b += contrib
            Cprime_high += d * d

    print(f"C' from b <= N/2: {float(Cprime_low):.4f} ({float(Cprime_low/Cprime):.4f})")
    print(f"C' from b > N/2: {float(Cprime_high):.4f} ({float(Cprime_high/Cprime):.4f})")
    print(f"K_diff from b <= N/2: {float(K_diff_low_b):.4f} ({float(K_diff_low_b/Cprime):.4f} C')")
    print(f"K_diff from b > N/2: {float(K_diff_high_b):.4f} ({float(K_diff_high_b/Cprime):.4f} C')")

    # For b > N/2: j ranges from N/2+1 to N, and b > N/2, so j < 2b.
    # Then ja/b < 2a < 2b, so floor(ja/b) is 0 or 1.
    # {ja/b} = ja/b when ja < b (i.e., j < b/a), and = ja/b - 1 when ja >= b.
    # Since a < b and j < 2b, we have ja < 2b^2/... this is getting complicated.

    # Actually for b > N/2 and j in [N/2+1, N]:
    # j/b < N/b < 2 (since b > N/2). So j < 2b.
    # ja/b < 2a < 2b. So floor(ja/b) can be 0 or 1.
    # {ja/b} = ja/b - floor(ja/b).
    # floor(ja/b) = 1 iff ja >= b, i.e., a >= b/j.
    # For j around N ~ b, a >= b/j ~ 1, so most a contribute floor = 1,
    # except very small a.

    # For b > N/2 specifically, each f=a/b with b > N/2 has at most one
    # "period" in the range [N/2+1, N]. The half-sum H(f) is approximately
    # (N/2)(b-1)/(2b) but with a specific offset.

    # Let's check: for b > N/2, what is sum_{j=N/2+1}^{N} {ja/b}?
    # Since b > N/2, the number of j in [N/2+1, N] is N/2, and b > N/2,
    # so we have fewer than b values of j. The sequence {ja/b} for
    # j = N/2+1, ..., N visits N/2 < b distinct residues.
    # The average is approximately (b-1)/(2b) ~ 1/2.
    # The sum is approximately N/4.

    # Key structural claim: for b > N/2, the correlation between
    # H(f) and delta(f) is governed by the "resonance" between
    # the fractional parts {ja/b} and the modular displacement delta(a/b).

    # Let me check: what is the average of delta(f)^2 for b > N/2?
    # This should be O(1/b) per fraction, contributing O(1) to C' per denominator.
    # Total C' ~ N * O(1) = O(N). (Standard Farey discrepancy scaling.)

    # And K_diff ~ sum over b of (correlation per b) * O(1)
    # If each b contributes O(1) to K_diff, then K_diff ~ O(N) ~ O(C'). QED.

    # But we need the SIGN. Let's investigate the sign pattern.

    # For b > N/2 (which contributes most of C'), compute avg delta*H per b
    print(f"\nPer-b analysis for b > N/2:")
    for b in range(N2+1, N+1):
        cb_val = Fraction(0)
        db_val = Fraction(0)
        n_terms = 0
        for a in range(1, b):
            if math.gcd(a, b) != 1:
                continue
            n_terms += 1
            f = Fraction(a, b)
            d = deltas[f]
            db_val += d * d
            H = Fraction(0)
            for j in range(N2+1, N+1):
                jf = j * f
                fp = jf - int(jf)
                H += fp
            cb_val += H * d

        if n_terms > 0 and float(db_val) > 0.005 * float(Cprime):
            print(f"  b={b}: C_b/D_b = {float(cb_val/db_val):.4f}, "
                  f"D_b/C' = {float(db_val/Cprime):.4f}, "
                  f"C_b/C' = {float(cb_val/Cprime):.4f}")

    return float(K_diff_low_b/Cprime), float(K_diff_high_b/Cprime)

for p in [43, 71, 107, 131]:
    structural_analysis(p)
