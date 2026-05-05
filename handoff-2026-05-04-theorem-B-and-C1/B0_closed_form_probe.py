"""
Probe whether B0(N) := Σ_{f∈F_N} D_N(f) (f - 1/2) has a clean closed form.

D(f) = rank(f) - n*f.
B0 = Σ rank(f)*(f - 1/2) - n * Σ f*(f - 1/2)
   = T1 - n * T3
where
  T1 = Σ_{k=1..n} k * (f_k - 1/2)
  T3 = Σ f * (f - 1/2) = Σ f² - (1/2) Σ f

By symmetry f ↔ 1-f of F_N, Σ f = n/2 (for n even; for n odd the median 1/2 is
absorbed). So Σ f² is a known sum:
  Σ_{f ∈ F_N} f² = Σ_{b=1}^N (1/b²) Σ_{a: gcd(a,b)=1, 0<=a<=b} a²
                 = Σ_b (1/b²) [some Möbius-Jordan totient stuff].

T1 = Σ k * f_k - (1/2) * Σ k = Σ k f_k - n(n+1)/4.

Σ k*f_k is "Farey rank-position covariance" = Σ_{f∈F_N} rank(f)*f. By
reflection f ↔ 1-f and rank ↔ n+1-rank, k*f_k + (n+1-k)*(1-f_k) symmetric...
Hmm. Let's just compute and tabulate.

If B0(N) ~ c·N², the constant c is an interesting Farey constant.
"""
from fractions import Fraction
from math import gcd
import sys

def farey_pairs(N):
    pairs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a,b)==1:
                pairs.append((a,b))
    pairs.sort(key=lambda ab: Fraction(ab[0], ab[1]))
    return pairs

def B0_probe(N):
    pairs = farey_pairs(N)
    n = len(pairs)
    s = Fraction(0)
    sum_f = Fraction(0)
    sum_f2 = Fraction(0)
    sum_kf = Fraction(0)
    for k0,(a,b) in enumerate(pairs):
        k = k0+1
        f = Fraction(a,b)
        s += (k - n*f) * (f - Fraction(1,2))
        sum_f += f
        sum_f2 += f*f
        sum_kf += k*f
    return s, n, sum_f, sum_f2, sum_kf

if __name__ == "__main__":
    print("# N, n=|F_N|, B0(N), B0/n^2, Σf, Σf², Σ k*f_k")
    for N in [2,3,5,7,10,15,20,30,50,75,100,150,200]:
        b0, n, sf, sf2, skf = B0_probe(N)
        print(f"N={N:3d} n={n:6d} B0={float(b0):+12.4f} B0/n²={float(b0/n**2):+.6f} Σf={float(sf):.4f} (n/2={n/2}) Σf²={float(sf2):.4f} (n/3≈{n/3:.4f})")
