"""Final verification of key numbers for the LEMMA1 document."""
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

for p in [43, 71, 107]:
    N = p - 1
    N2 = N // 2
    fracs = farey_interior(N)
    deltas = {f: delta_p(f, p) for f in fracs}
    Cprime = sum(d*d for d in deltas.values())

    pos_total = Fraction(0)
    neg_total = Fraction(0)

    for f in fracs:
        d = deltas[f]
        H = Fraction(0)
        for j in range(N2+1, N+1):
            jf = j * f
            fp = jf - int(jf)
            H += fp
        contrib = H * d
        if contrib > 0:
            pos_total += contrib
        else:
            neg_total += contrib

    K_diff = pos_total + neg_total
    print(f"p={p}: pos={float(pos_total/Cprime):.3f}*C', neg={float(neg_total/Cprime):.3f}*C', net={float(K_diff/Cprime):.3f}*C'")
