#!/usr/bin/env python3
"""Verify Bern(3299) etc with exact rationals."""
from fractions import Fraction
from mpmath import mp, mpf
mp.dps = 50

def farey_seq(N):
    a,b=0,1; c,d=1,N; out=[(a,b)]
    while c<=N:
        k=(N+b)//d
        a,b,c,d=c,d,k*c-a,k*d-b
        out.append((a,b))
    return out

def psi_pf(p, a, b):
    if b==1: return Fraction(0)
    r = (p*a) % b
    return Fraction(r, b) - Fraction(1, 2)

def bern_saw_exact(p):
    F = farey_seq(p-1); n = len(F); nm1 = n-1; half=Fraction(1,2)
    Bern = Fraction(0); Saw = Fraction(0)
    # Chebyshev form: (1/(n-1)) * sum (i - (n-1)/2)(f_i - 1/2)
    Cheb = Fraction(0)
    for i,(a,b) in enumerate(F):
        f = Fraction(a,b)
        D = Fraction(i, nm1) - f
        Bern += D*(f - half)
        Saw  += D*psi_pf(p, a, b)
        # Chebyshev formulation
        Cheb += (Fraction(2*i - nm1, 2)) * (f - half)
    Cheb_div = Cheb / nm1
    return n, Bern, Saw, Cheb_div

for p in [3299]:
    n,B,S,Cb = bern_saw_exact(p)
    Bf = mpf(B.numerator)/mpf(B.denominator)
    Sf = mpf(S.numerator)/mpf(S.denominator)
    Cf = mpf(Cb.numerator)/mpf(Cb.denominator)
    print(f"p={p} n={n}")
    print(f"  Bern (direct)     = {mp.nstr(Bf,25)}  sign={'POS' if Bf>0 else 'NEG'}")
    print(f"  Saw               = {mp.nstr(Sf,25)}")
    print(f"  Chebyshev form    = {mp.nstr(Cf,25)}  sign={'POS' if Cf>0 else 'NEG'}")
    print(f"  diff (should be 0): {mp.nstr(Bf - Cf, 25)}")
    print(f"  B_raw = Bern-Saw  = {mp.nstr(Bf-Sf,25)}")
