"""Verify the per-b sign counts for the LEMMA1 document."""
from fractions import Fraction
import math

def delta_p(a, b, p):
    bma = b - a
    res = (p * bma) % b
    if res == 0:
        res = b
    return Fraction(res - bma, b)

for p in [43, 71, 107, 131]:
    N = p - 1
    N2 = N // 2
    pos_count = neg_count = zero_count = 0
    for b in range(N2+1, N+1):
        Cb = Fraction(0)
        for a in range(1, b):
            if math.gcd(a, b) != 1:
                continue
            d = delta_p(a, b, p)
            Tb = Fraction(0)
            for j in range(N2+1, N+1):
                ja_mod_b = (j * a) % b
                Tb += Fraction(ja_mod_b, b)
            Cb += Tb * d
        if Cb > 0:
            pos_count += 1
        elif Cb < 0:
            neg_count += 1
        else:
            zero_count += 1
    total = pos_count + neg_count + zero_count
    print(f"p={p}: b > N/2 range has {total} denominators: {pos_count} pos, {neg_count} neg, {zero_count} zero")
