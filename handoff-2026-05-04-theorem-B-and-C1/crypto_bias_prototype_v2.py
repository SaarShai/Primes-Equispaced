#!/usr/bin/env python3
"""Crypto Bias Audit prototype v2 — RACE METHODOLOGY (correct).

The right test for Chebyshev / Koyama bias is the RACE / LEAD FRACTION test
(Rubinstein-Sarnak 1994), NOT a deviation-from-uniform single-x test.

For each modulus q, walk samples in order. Maintain running counts per residue.
Track fraction of time each residue is "leading" (highest count). Compare to:
- Pseudo-random null: lead fraction = 1/(# non-residues) per residue
- Koyama Theorem 1.1: -1 leads with specific fraction > 1/(# non-residues - 1)

Validation gates:
1. POSITIVE CONTROL: raw primes ≤ 10^7 (Chebyshev bias for q=4)
   Expected: π(x; 4, 3) > π(x; 4, 1) for ~99.6% of x (Rubinstein-Sarnak)
2. NEGATIVE CONTROL: /dev/urandom 10^6 samples
   Expected: lead fraction → 1/(# non-residues), uniform
"""
import sys, time
from math import gcd
from sympy import primerange, totient

def coprime_residues(q):
    return sorted([a for a in range(1, q) if gcd(a, q) == 1])

def race_test(values, q, sample_log=False):
    """For each step, record which residue leads in count.
    Return: dict mapping residue -> fraction of steps it was leader.
    Also: time series of leaders (downsampled if requested)."""
    coprime = coprime_residues(q)
    counts = {a: 0 for a in coprime}
    lead_count = {a: 0 for a in coprime}
    n_steps = 0
    leader_history = []
    for v in values:
        r = v % q
        if r not in counts:
            continue
        counts[r] += 1
        n_steps += 1
        # Find leader (max count among non-residues if applicable, or all coprime)
        max_count = max(counts.values())
        leaders = [a for a, c in counts.items() if c == max_count]
        # If tie, no single leader; skip
        if len(leaders) == 1:
            lead_count[leaders[0]] += 1
            if sample_log and n_steps % max(1, len(values)//100) == 0:
                leader_history.append((n_steps, leaders[0], counts.copy()))
    fractions = {a: lead_count[a] / n_steps for a in coprime}
    return {
        'q': q,
        'fractions': fractions,
        'final_counts': counts,
        'n_steps_with_leader': sum(lead_count.values()),
        'n_steps_total': n_steps,
        'leader_history': leader_history if sample_log else None,
    }

def chebyshev_race_test(values, q):
    """Specific test for q=4 race between residues 1 and 3.
    Returns fraction of time #{p≡3 mod 4} > #{p≡1 mod 4}.
    Rubinstein-Sarnak predicts 0.9959 for genuine primes.
    """
    n_3, n_1 = 0, 0
    fraction_3_leads = 0
    n_steps = 0
    for v in values:
        if v % 4 == 1:
            n_1 += 1
        elif v % 4 == 3:
            n_3 += 1
        else:
            continue
        n_steps += 1
        if n_3 > n_1:
            fraction_3_leads += 1
    return {
        'fraction_3_leads': fraction_3_leads / n_steps if n_steps else 0,
        'final_n_3': n_3, 'final_n_1': n_1,
        'n_steps': n_steps,
        'rubinstein_sarnak_prediction': 0.9959,
    }

def neg_one_race_test(values, q):
    """Among NON-residues mod q, fraction of time -1 = q-1 is leading.
    Koyama Theorem 1.1 predicts this fraction > 1/(# non-residues)."""
    coprime = coprime_residues(q)
    # Determine quadratic residues / non-residues
    # x is a residue iff there exists y with y^2 ≡ x mod q
    qr = set()
    for y in range(1, q):
        if gcd(y, q) == 1:
            qr.add((y * y) % q)
    qnr = [a for a in coprime if a not in qr]
    if (q - 1) not in qnr:
        return {'note': f'q={q}: -1 is QR (q ≡ 1 mod 4), test not applicable'}
    counts = {a: 0 for a in qnr}
    lead_count = {a: 0 for a in qnr}
    n_steps = 0
    for v in values:
        r = v % q
        if r in counts:
            counts[r] += 1
        if any(counts.values()):
            n_steps += 1
            max_c = max(counts.values())
            leaders = [a for a, c in counts.items() if c == max_c]
            if len(leaders) == 1:
                lead_count[leaders[0]] += 1
    if n_steps == 0:
        return {'error': 'no qnr samples'}
    fractions = {a: lead_count[a] / n_steps for a in qnr}
    uniform_pred = 1.0 / len(qnr)
    return {
        'q': q,
        'qnr': qnr,
        'minus1': q - 1,
        'fractions': fractions,
        'fraction_minus1_leads': fractions[q - 1],
        'uniform_prediction': uniform_pred,
        'koyama_excess': fractions[q - 1] - uniform_pred,
    }

# ============ POSITIVE CONTROL ============

def positive_control(P_max=10**7):
    print(f"\n=== POSITIVE CONTROL: primes ≤ {P_max:,} ===")
    print("Sieving primes...")
    t0 = time.time()
    primes = list(primerange(2, P_max))
    print(f"  Found {len(primes):,} primes in {time.time()-t0:.1f}s")

    print("\n--- Chebyshev race q=4 (a=3 vs a=1) ---")
    cheb = chebyshev_race_test(primes, 4)
    print(f"  fraction(3 leads) = {cheb['fraction_3_leads']:.4f}")
    print(f"  Rubinstein-Sarnak prediction: {cheb['rubinstein_sarnak_prediction']}")
    print(f"  final n_3={cheb['final_n_3']:,}, n_1={cheb['final_n_1']:,}, diff={cheb['final_n_3'] - cheb['final_n_1']:+}")
    sig = "✓ DETECTED" if cheb['fraction_3_leads'] > 0.9 else ("? marginal" if cheb['fraction_3_leads'] > 0.7 else "✗ NOT DETECTED")
    print(f"  {sig}")

    print("\n--- -1 dominance race (Koyama) ---")
    for q in (5, 7, 8, 11, 13, 16):
        result = neg_one_race_test(primes, q)
        if 'note' in result:
            print(f"  q={q}: {result['note']}")
        elif 'error' in result:
            print(f"  q={q}: error: {result['error']}")
        else:
            print(f"  q={q}: -1={result['minus1']}, qnr={result['qnr']}, frac(-1 leads)={result['fraction_minus1_leads']:.4f}, uniform={result['uniform_prediction']:.4f}, excess={result['koyama_excess']:+.4f}")

# ============ NEGATIVE CONTROL ============

def negative_control(K=10**6):
    print(f"\n=== NEGATIVE CONTROL: /dev/urandom, K={K:,} ===")
    print("Reading random bytes...")
    t0 = time.time()
    with open('/dev/urandom', 'rb') as f:
        raw = f.read(K * 8)
    samples = [int.from_bytes(raw[i*8:(i+1)*8], 'big') for i in range(K)]
    print(f"  Got {len(samples):,} 64-bit samples in {time.time()-t0:.1f}s")

    print("\n--- Chebyshev race q=4 ---")
    cheb = chebyshev_race_test(samples, 4)
    print(f"  fraction(3 leads) = {cheb['fraction_3_leads']:.4f}")
    print(f"  Expected (uniform null): ~0.5")
    sig = "✓ NULL" if 0.4 < cheb['fraction_3_leads'] < 0.6 else "FAIL!"
    print(f"  {sig}")

    print("\n--- -1 dominance race ---")
    for q in (5, 7, 8, 11, 13):
        result = neg_one_race_test(samples, q)
        if 'note' in result:
            print(f"  q={q}: {result['note']}")
        elif 'error' in result:
            continue
        else:
            sig = "✓ NULL" if abs(result['koyama_excess']) < 0.05 else "FAIL!"
            print(f"  q={q}: frac(-1 leads)={result['fraction_minus1_leads']:.4f}, uniform={result['uniform_prediction']:.4f}, excess={result['koyama_excess']:+.4f}  {sig}")

if __name__ == "__main__":
    print("Crypto Bias Audit Framework v2 — RACE methodology")
    print("=" * 60)
    positive_control(P_max=10**7)
    negative_control(K=10**6)
    print("\n" + "=" * 60)
    print("DONE.")
