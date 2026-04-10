#!/usr/bin/env python3
"""
Full Abel decomposition for Lemma 3: Term2 < 0 for M(p)=-3 primes, p >= 43.

Computes:
1. Term-by-term Abel sum for p=43 (tightest case)
2. q-block decomposition for p=43, 71, 107, 173
3. Positive/negative budget analysis
4. Structural bounds for the analytical proof
"""
from fractions import Fraction
from math import gcd

def mertens_table(limit):
    mu = [0] * (limit + 1); mu[1] = 1
    is_prime = [True] * (limit + 1); primes = []
    for i in range(2, limit + 1):
        if is_prime[i]: primes.append(i); mu[i] = -1
        for pp in primes:
            if i * pp > limit: break
            is_prime[i * pp] = False
            if i % pp == 0: mu[i * pp] = 0; break
            else: mu[i * pp] = -mu[i]
    M = [0] * (limit + 1)
    for n in range(1, limit + 1): M[n] = M[n-1] + mu[n]
    return M, mu

def farey_sequence(N):
    fracs = []
    for b in range(2, N + 1):
        for a in range(1, b):
            if gcd(a, b) == 1: fracs.append(Fraction(a, b))
    fracs.sort()
    return fracs

def delta_p_frac(a, b, p):
    u = b - a
    pu_mod_b = (p * u) % b
    if pu_mod_b == 0: pu_mod_b = b
    return Fraction(pu_mod_b - u, b)

def analyze_prime(p, M_big, verbose=True):
    N = p - 1
    fs = farey_sequence(N)
    deltas = {f: delta_p_frac(f.numerator, f.denominator, p) for f in fs}
    Cp = sum(d*d for d in deltas.values())

    # Compute all kernels K_1 .. K_N
    K = {}
    K[1] = sum(f * deltas[f] for f in fs)
    for m in range(1, N):
        j = m + 1
        inc = Fraction(0)
        for f in fs:
            jf = j * f
            frac_part = jf - int(jf)
            if frac_part < 0: frac_part += 1
            inc += frac_part * deltas[f]
        K[m+1] = K[m] + inc

    # Also compute H_{[1/2,1)}
    H_half = sum(deltas[f] for f in fs if f >= Fraction(1,2))

    if verbose:
        print(f"\n{'='*80}")
        print(f"p = {p}, N = {N}")
        print(f"{'='*80}")
        print(f"C'(p) = {float(Cp):.8f}")
        print(f"K_1/C' = {float(K[1]/Cp):.6f}  (= 1/2 by formula)")
        print(f"K_2/C' = {float(K[2]/Cp):.6f}")
        print(f"(K_2 - K_1)/C' = {float((K[2]-K[1])/Cp):.6f}")
        print(f"H_[1/2,1)/C' = {float(H_half/Cp):.6f}")
        print(f"Check: K_2 - K_1 = C' - H_[1/2,1)? {K[2]-K[1] == Cp - H_half}")

    # Abel sum: term by term
    if verbose:
        print(f"\n--- Abel sum, significant terms ---")
        hdr = "  m   m+1  q=N/(m+1)  M(q)    DK/C'      Contrib/C'   Cumul/C'"
        print(hdr)

    cumul = Fraction(0)
    for m in range(1, N):
        q = N // (m+1)
        Mq = M_big[q]
        dk = K[m+1] - K[m]
        contrib = Mq * dk
        cumul += contrib
        if verbose and abs(float(dk/Cp)) > 0.005:
            print(f"  {m:>3} {m+1:>4}  {q:>9}  {Mq:>4}  {float(dk/Cp):>10.5f}  {float(contrib/Cp):>11.5f}  {float(cumul/Cp):>11.5f}")

    if verbose:
        print(f"  Total Term2/C' = {float(cumul/Cp):.6f}")

    # q-block decomposition
    total = Fraction(0)
    pos_total = Fraction(0)
    neg_total = Fraction(0)
    blocks = []
    seen = set()
    for q in range(1, N):
        if q in seen: continue
        end_m1 = min(N // q, N)
        start_m1 = max(N // (q + 1) + 1, 2)
        if start_m1 > end_m1: continue
        seen.add(q)
        Mq = M_big[q]
        block_dk = K[end_m1] - K[start_m1 - 1]
        contrib = Mq * block_dk
        total += contrib
        if float(contrib) > 0: pos_total += contrib
        else: neg_total += contrib
        blocks.append((q, Mq, start_m1, end_m1, block_dk, contrib))

    blocks.sort(key=lambda x: float(x[5]))

    if verbose:
        print(f"\n--- q-block decomposition (ALL blocks) ---")
        for q, Mq, s, e, dk, c in blocks:
            print(f"  q={q:>3}: M(q)={Mq:>3}, m+1 in [{s},{e}], "
                  f"DK/C'={float(dk/Cp):>8.5f}, contrib/C'={float(c/Cp):>10.5f}")
        print(f"\n  Positive total / C' = {float(pos_total/Cp):+.6f}")
        print(f"  Negative total / C' = {float(neg_total/Cp):+.6f}")
        print(f"  Net Term2/C'        = {float(total/Cp):+.6f}")
        print(f"  Ratio |neg|/pos     = {abs(float(neg_total/pos_total)):.4f}")

    # Key structural data
    q1_block = None
    qN2_block = None
    qN3_block = None
    for q, Mq, s, e, dk, c in blocks:
        if q == 1: q1_block = (dk, c)
        if q == N//2: qN2_block = (dk, c, Mq)
        if q == N//3: qN3_block = (dk, c, Mq)

    if verbose:
        print(f"\n--- Key structural data ---")
        if q1_block:
            print(f"  q=1 block (positive): DK/C' = {float(q1_block[0]/Cp):.5f}, contrib/C' = {float(q1_block[1]/Cp):+.5f}")
        if qN2_block:
            print(f"  q=N/2={N//2} block: M(q)={qN2_block[2]}, DK/C' = {float(qN2_block[0]/Cp):.5f}, contrib/C' = {float(qN2_block[1]/Cp):+.5f}")
        if qN3_block:
            print(f"  q=N/3={N//3} block: M(q)={qN3_block[2]}, DK/C' = {float(qN3_block[0]/Cp):.5f}, contrib/C' = {float(qN3_block[1]/Cp):+.5f}")

    # M(q) values at key denominators
    if verbose:
        print(f"\n--- Mertens values at hyperbolic denominators ---")
        for j in range(2, min(15, N)):
            q = N // j
            if q >= 1:
                print(f"  j={j:>2}: q=N/{j} = {q:>3}, M(q) = {M_big[q]:>3}")

    return {
        'p': p, 'N': N, 'Cp': Cp,
        'term2_over_Cp': float(total/Cp),
        'pos_over_Cp': float(pos_total/Cp),
        'neg_over_Cp': float(neg_total/Cp),
        'K1_over_Cp': float(K[1]/Cp),
        'K2_over_Cp': float(K[2]/Cp),
        'DK12_over_Cp': float((K[2]-K[1])/Cp),
        'H_half_over_Cp': float(H_half/Cp),
        'blocks': blocks,
        'K': K,
    }


def main():
    M_big, mu_big = mertens_table(500)

    # Detailed analysis of p=43 (tightest case)
    r43 = analyze_prime(43, M_big, verbose=True)

    # Analysis of larger primes to see the trend
    for p in [47, 53, 71, 107, 131, 173, 179]:
        r = analyze_prime(p, M_big, verbose=True)

    # Summary table
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"{'p':>5} {'Term2/C':>10} {'Pos/C':>10} {'Neg/C':>10} {'|Neg|/Pos':>10} {'DK12/C':>10} {'H_half/C':>10}")
    for p in [43, 47, 53, 71, 107, 131, 173, 179]:
        r = analyze_prime(p, M_big, verbose=False)
        print(f"{p:>5} {r['term2_over_Cp']:>10.4f} {r['pos_over_Cp']:>10.4f} {r['neg_over_Cp']:>10.4f} "
              f"{abs(r['neg_over_Cp']/r['pos_over_Cp']):>10.4f} {r['DK12_over_Cp']:>10.4f} {r['H_half_over_Cp']:>10.4f}")

    # Check M(N/2) values for all tested primes
    print(f"\n--- M(floor(N/2)) for M(p)=-3 primes ---")
    mp3_primes = [p for p in range(3, 500) if M_big[p] == -3 and all(p % d != 0 for d in range(2, int(p**0.5)+1))]
    for p in mp3_primes:
        N = p - 1
        q_half = N // 2
        print(f"  p={p:>4}, N={N:>4}, N/2={q_half:>4}, M(N/2)={M_big[q_half]:>3}, "
              f"M(N/3)={M_big[N//3]:>3}, M(N/4)={M_big[N//4]:>3}")

if __name__ == "__main__":
    main()
