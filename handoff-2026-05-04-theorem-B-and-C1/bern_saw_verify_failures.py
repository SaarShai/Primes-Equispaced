#!/usr/bin/env python3
"""Re-verify p in {1399,1409,1423,1427,1429} with exact rationals."""
from fractions import Fraction
from mpmath import mp, mpf
mp.dps = 40

def farey_seq(N):
    a,b=0,1; c,d=1,N; out=[Fraction(a,b)]
    while c<=N:
        k=(N+b)//d
        a,b,c,d=c,d,k*c-a,k*d-b
        out.append(Fraction(a,b))
    return out

def psi(x: Fraction):
    if x.denominator==1: return Fraction(0)
    fr = x - x.numerator//x.denominator
    if fr<0: fr+=1
    return fr - Fraction(1,2)

def bern_saw_exact(p):
    F = farey_seq(p-1); n = len(F); nm1 = n-1; half=Fraction(1,2)
    Bern=Fraction(0); Saw=Fraction(0)
    for i,f in enumerate(F):
        D = Fraction(i,nm1) - f
        Bern += D*(f-half)
        Saw  += D*psi(p*f)
    return n, Bern, Saw

for p in [1399, 1409, 1423, 1427, 1429, 1433]:  # 1433 as sanity check
    n,B,S = bern_saw_exact(p)
    Bf = mpf(B.numerator)/mpf(B.denominator)
    Sf = mpf(S.numerator)/mpf(S.denominator)
    ratio = abs(Sf)/Bf if Bf>0 else mpf('inf')
    Braw = Bf - Sf
    print(f"p={p:5d} n={n:7d} Bern={mp.nstr(Bf,18)} Saw={mp.nstr(Sf,18)} ratio={mp.nstr(ratio,12)} B_raw={mp.nstr(Braw,18)} sign={'POS' if Braw>0 else 'NEG/ZERO'}")
