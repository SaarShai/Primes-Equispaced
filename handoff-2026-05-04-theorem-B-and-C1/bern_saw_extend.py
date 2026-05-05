#!/usr/bin/env python3
"""
Extend Bern/Saw numerical verification from 35 primes (p ≤ 211) to 200 primes (p ≤ 1019+).
All computation in exact rationals (fractions.Fraction); print 30-digit floats via mpmath.

Definitions (B_geq_0_extra_high_attempt.md §0–§3):
  F_{p-1} = Farey fractions with denominator ≤ p-1, in [0,1] sorted ascending.
  n = |F_{p-1}|.
  D(f_i) = i/(n-1) - f_i  (rank deviation; 0-indexed i=0..n-1).
  psi(x) = {x} - 1/2 if x not integer; 0 if integer.
  Bern(p) = sum_i D(f_i) * (f_i - 1/2)
  Saw(p)  = sum_i D(f_i) * psi(p * f_i)

Output: TSV to bern_saw_extend.tsv with columns
  p, n, Bern, Saw, ratio=|Saw|/Bern, Bern-Saw (= B_raw)
"""
from fractions import Fraction
from sympy import isprime, primerange
from mpmath import mp, mpf, log

mp.dps = 35

def farey_seq(N):
    """Stern-Brocot / mediant generation of F_N in [0,1]."""
    a, b = 0, 1
    c, d = 1, N
    out = [Fraction(a, b)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        out.append(Fraction(a, b))
    return out

def psi_rational(x: Fraction) -> Fraction:
    """sawtooth psi(x) = {x} - 1/2 if x not in Z else 0."""
    if x.denominator == 1:
        return Fraction(0)
    frac = x - x.numerator // x.denominator  # in [0,1)
    if frac < 0:
        frac += 1
    return frac - Fraction(1, 2)

def bern_saw(p: int):
    F = farey_seq(p - 1)
    n = len(F)
    half = Fraction(1, 2)
    Bern = Fraction(0)
    Saw = Fraction(0)
    nm1 = n - 1
    for i, f in enumerate(F):
        D = Fraction(i, nm1) - f
        Bern += D * (f - half)
        Saw += D * psi_rational(p * f)
    return n, Bern, Saw

def main():
    out_path = "/Users/saar/Farey 4.7 solutions/bern_saw_extend.tsv"
    primes = list(primerange(11, 1020))  # primes up to 1019 ~ a couple hundred primes
    print(f"# primes = {len(primes)}, range [{primes[0]}, {primes[-1]}]")
    rows = []
    with open(out_path, "w") as fh:
        fh.write("p\tn\tBern\tSaw\tratio\tB_raw\n")
        max_ratio = mpf(0); max_p = 0
        for p in primes:
            n, Bern, Saw = bern_saw(p)
            B_raw = Bern - Saw
            Bern_f = mpf(Bern.numerator) / mpf(Bern.denominator)
            Saw_f  = mpf(Saw.numerator)  / mpf(Saw.denominator)
            ratio  = abs(Saw_f) / Bern_f if Bern_f > 0 else mpf('inf')
            B_raw_f = Bern_f - Saw_f
            fh.write(f"{p}\t{n}\t{mp.nstr(Bern_f,15)}\t{mp.nstr(Saw_f,15)}\t{mp.nstr(ratio,10)}\t{mp.nstr(B_raw_f,15)}\n")
            fh.flush()
            if ratio > max_ratio:
                max_ratio = ratio; max_p = p
            # progress
            if p in (11, 53, 101, 211, 401, 601, 809, 1019):
                print(f"  p={p:5d}  n={n:7d}  Bern={mp.nstr(Bern_f,8)}  Saw={mp.nstr(Saw_f,8)}  ratio={mp.nstr(ratio,6)}  B_raw>0? {B_raw_f>0}")
        print(f"\nMAX ratio |Saw|/Bern = {mp.nstr(max_ratio,10)} at p={max_p}")
        # Find min B_raw / Bern margin
        # Re-read for summary
    # Summary pass
    import statistics
    ratios = []
    margins = []
    pos_count = 0; total = 0
    with open(out_path) as fh:
        next(fh)
        for line in fh:
            p_,n_,B_,S_,r_,Br_ = line.strip().split("\t")
            ratios.append(float(r_))
            margins.append(1.0 - float(r_))
            if float(Br_) > 0: pos_count += 1
            total += 1
    print(f"All B_raw > 0? {pos_count}/{total}")
    print(f"max ratio = {max(ratios):.6f}, min ratio = {min(ratios):.6f}, mean = {statistics.mean(ratios):.6f}")
    print(f"min margin (1 - ratio) = {min(margins):.6f}")

if __name__ == "__main__":
    main()
