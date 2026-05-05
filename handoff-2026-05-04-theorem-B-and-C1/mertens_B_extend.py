"""
Extended numerical verification of B(p) > 0 for primes p with M(p) <= -3.

Optimized: B(p) = 2 * sum over (a,b) coprime, 1<=b<=p-1, 0<=a<=b of D(a/b)*delta(a/b).

Use exact rationals (Fraction) but optimize:
- Represent all fractions with common denominator structure: f = a/b. Then p*f = p*a/b,
  frac(p*f) = (p*a mod b)/b. delta(f) = a/b - (p*a mod b)/b = (a - (p*a mod b))/b.
- D(f) = rank - n*f. rank requires sorting; do it once.

For each prime p we work with denominator <= p-1.
Total fractions ~ (3/pi^2) * (p-1)^2.
For p=1000, that's ~300k pairs. Sort cost dominates but tolerable.

Output:
  CSV with columns: p, M(p), n, B_p_numer, B_p_denom, sign(B), len(numer), len(denom)
"""
from fractions import Fraction
from math import gcd
from sympy import mobius, primerange
import time, sys

def mertens_table(N):
    """Mertens M(n) for n=1..N."""
    mu = [0]*(N+1)
    M = [0]*(N+1)
    for n in range(1, N+1):
        mu[n] = int(mobius(n))
    s = 0
    for n in range(1, N+1):
        s += mu[n]
        M[n] = s
    return M

def cross_term_fast(p):
    """Compute B(p) exactly. Returns Fraction."""
    N = p - 1
    # Build all coprime pairs (a,b) with b in 1..N, a in 0..b, gcd(a,b)=1.
    pairs = []
    for b in range(1, N+1):
        if b == 1:
            pairs.append((0, 1))
            pairs.append((1, 1))
        else:
            for a in range(0, b+1):
                if gcd(a, b) == 1:
                    pairs.append((a, b))
    # Note: 0/1 and 1/1 both included; for b=1 we handled separately.
    # But for b>=2 we did 0..b. For b=1, 0/1 and 1/1.
    # Sort by value a/b
    pairs.sort(key=lambda ab: Fraction(ab[0], ab[1]))
    n = len(pairs)
    total = Fraction(0)
    for rank0, (a, b) in enumerate(pairs):
        rank1 = rank0 + 1
        # D = rank1 - n * a/b = (rank1 * b - n*a) / b
        D = Fraction(rank1 * b - n * a, b)
        # delta = a/b - (p*a mod b)/b = (a - (p*a mod b)) / b
        r = (p * a) % b
        delta = Fraction(a - r, b)
        total += D * delta
    return 2 * total

def main(p_max=2000):
    M = mertens_table(p_max)
    # Compute Mertens at p (= sum mu(k) for k=1..p, NOT p-1)
    primes = list(primerange(11, p_max + 1))
    out = open(f"/Users/saar/Farey 4.7 solutions/mertens_B_results_{p_max}.tsv", "w")
    out.write("p\tM(p)\tsign(B)\tB_numer\tB_denom\n")
    print(f"# Computing B(p) for primes 11 <= p <= {p_max}")
    print("# p, M(p), B(p) sign, B(p) numerator, B(p) denominator")
    counterexamples = []
    mertens_relevant = []
    t0 = time.time()
    for p in primes:
        Mp = M[p]
        # We only really need to verify when M(p) <= -3.
        if Mp > -3:
            # Skip — but log occasionally
            continue
        B = cross_term_fast(p)
        sign = 1 if B > 0 else (-1 if B < 0 else 0)
        mertens_relevant.append((p, Mp, B, sign))
        if sign <= 0:
            counterexamples.append((p, Mp, B))
            print(f"COUNTEREXAMPLE: p={p}, M(p)={Mp}, B(p)={B}")
        out.write(f"{p}\t{Mp}\t{sign}\t{B.numerator}\t{B.denominator}\n")
        out.flush()
        print(f"p={p:5d} M={Mp:4d} sign={sign:+d} B≈{float(B):.4e}  ({time.time()-t0:.1f}s)", flush=True)
    print(f"\nDone. Tested {len(mertens_relevant)} primes with M(p) <= -3.")
    print(f"Counterexamples: {len(counterexamples)}")
    return mertens_relevant, counterexamples

if __name__ == "__main__":
    p_max = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    main(p_max)
