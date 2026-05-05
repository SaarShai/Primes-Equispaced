"""
Decomposition probe: B(p) = 2*B0 - 2*Sψ(p), where
  B0 = Σ_{f ∈ F_{p-1}} D(f) · (f - 1/2)            [p-independent in form, but n=|F_{p-1}| varies]
  Sψ(p) = Σ_{f ∈ F_{p-1}} D(f) · ψ(p f)            [p-dependent oscillation]
  ψ(x) = {x} - 1/2

Claim: δ(f) = f - {pf} = (f - 1/2) - ψ(pf), so
  B(p) = 2 Σ D(f) δ(f) = 2 Σ D(f)(f-1/2) - 2 Σ D(f) ψ(pf) = 2 B0(N) - 2 Sψ(p; N), N = p-1.

Note B0 depends on N = p-1 (the Farey order), not on p itself. This separates
the structural Farey statistic from the prime-multiplicative wobble.

We also probe:
  - B0(N) closed form / sign for N = 2..1000.
  - Bridge: Σ_f e^{2πi p f} = M(p) + 2  ⇒  Re part Σ cos(2πpf) = M(p)+2.
  - The bilinear sum Σ D(f) sin(2π m p f) / m at low m.
"""
from fractions import Fraction
from math import gcd
import math, cmath, sys
from sympy import mobius, primerange

def farey_pairs(N):
    pairs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a,b)==1:
                pairs.append((a,b))
    # Note: this gives (0,1) and (1,1) for b=1, plus (a,b) coprime for b>=2 with 0<=a<=b.
    # For b>=2, a=0 is excluded (gcd(0,b)=b≠1 unless b=1). a=b excluded (gcd(b,b)=b≠1).
    # So effectively b=1 gives 0/1 and 1/1; b>=2 gives 1<=a<b coprime.
    pairs.sort(key=lambda ab: Fraction(ab[0], ab[1]))
    return pairs

def displacements(pairs):
    n = len(pairs)
    out = []
    for rank0,(a,b) in enumerate(pairs):
        rank1 = rank0+1
        D = Fraction(rank1*b - n*a, b)
        out.append((a,b,D))
    return out, n

def B0(N):
    pairs = farey_pairs(N)
    disp, n = displacements(pairs)
    s = Fraction(0)
    for a,b,D in disp:
        s += D * (Fraction(a,b) - Fraction(1,2))
    return s, n

def Spsi(p, N):
    """Σ D(f) ψ(p f), ψ(x) = {x} - 1/2."""
    pairs = farey_pairs(N)
    disp, n = displacements(pairs)
    s = Fraction(0)
    for a,b,D in disp:
        # ψ(p*a/b): if (p*a) % b == 0, then ψ = 0 - 1/2 = -1/2 IF we adopt {x}=0 for integer x.
        # Convention: {x} = x - floor(x), so {integer}=0, hence ψ(integer) = -1/2.
        # BUT Lean docstring of crossTerm uses Int.fract, so {integer}=0, so ψ=-1/2.
        # For Farey f = a/b with b>=2, p*a/b is an integer only if b | p*a; since gcd(a,b)=1, b|p.
        # For b<p prime, b|p forces b=1 (excluded since b>=2) or b=p (excluded since b<=p-1).
        # So for our Farey set F_{p-1}, p*f never integer for b>=2. Only b=1 cases: f=0/1, f=1/1.
        # f=0: p*0=0, ψ(0) = 0 - 1/2 = -1/2.
        # f=1: p*1=p, ψ(p) = 0 - 1/2 = -1/2.
        if b == 1:
            psi = Fraction(-1,2)
        else:
            r = (p*a) % b
            psi = Fraction(r,b) - Fraction(1,2)
        s += D * psi
    return s

def cross_term(p):
    """B(p) = 2 Σ D δ. δ(f) = f - {pf}. {integer}=0."""
    N = p-1
    pairs = farey_pairs(N)
    disp, n = displacements(pairs)
    s = Fraction(0)
    for a,b,D in disp:
        if b == 1:
            # f = 0 or 1; p*f integer; {pf}=0; δ = f.
            delta = Fraction(a,b)
        else:
            r = (p*a) % b
            delta = Fraction(a-r, b)
        s += D * delta
    return 2*s

def mertens(n):
    return sum(int(mobius(k)) for k in range(1, n+1))

if __name__ == "__main__":
    print("# Sanity: B(p) = 2*B0(p-1) - 2*Sψ(p, p-1)?")
    # Note δ(f) = f - {pf} = (f - 1/2) - ψ(pf) holds when {pf} = ψ(pf) + 1/2,
    # i.e., for non-integer pf. For integer pf (b=1: f=0 or 1), {pf}=0, so δ=f,
    # while (f-1/2) - ψ(pf) = (f-1/2) - (-1/2) = f. So actually it DOES hold!
    # Great. So decomposition is exact.
    for p in [5, 7, 11, 13, 17, 19, 23, 31, 43]:
        Bp = cross_term(p)
        b0, n = B0(p-1)
        sp = Spsi(p, p-1)
        Mp = mertens(p)
        recombined = 2*b0 - 2*sp
        match = "OK" if recombined == Bp else "FAIL"
        print(f"p={p:3d} M={Mp:+3d} n={n:5d} B(p)={float(Bp):+.6f} B0={float(b0):+.4f} Sψ={float(sp):+.4f} 2(B0-Sψ)={float(recombined):+.6f} [{match}]")
