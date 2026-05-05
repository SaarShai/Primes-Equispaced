#!/usr/bin/env python3
"""Crypto Bias Audit prototype — validation gates.

Runs:
1. POSITIVE CONTROL: raw primes ≤ 10^7 (small but enough for Chebyshev bias signal)
   Expected: D_q > 0 for q ∈ {4, 5, 7, 8, 11} with statistical significance
2. NEGATIVE CONTROL: /dev/urandom output reduced mod q
   Expected: D_q ≈ 0, p > 0.05 for all q

Per methodology document:
- Test 2 (D_q): n_{-1} − max{n_a : a ≠ ±1, gcd(a,q)=1}
- Variance: 2Kp where p = 1/φ(q) (multinomial covariance)
- Two-sided p-value via standard normal
- Bonferroni correction across q ∈ Q at α=10^-3
"""
import sys, time
from math import gcd, sqrt, log
from sympy import primerange, totient

# Gaussian CDF / one-sided p-value
def normal_cdf(z):
    """Φ(z) via mpmath erfc."""
    from mpmath import erfc, mpf
    return float(0.5 * erfc(-mpf(z) / mpf(2)**0.5))

def two_sided_pvalue(z):
    """2 · (1 − Φ(|z|))"""
    return 2 * (1 - normal_cdf(abs(z)))

def coprime_residues(q):
    return [a for a in range(1, q) if gcd(a, q) == 1]

def D_q_test(values_mod_q, q):
    """Compute D_q test statistic + p-value.

    values_mod_q: list of residues mod q
    q: modulus
    Returns (D, z, p_two_sided)
    """
    K = len(values_mod_q)
    counts = {a: 0 for a in coprime_residues(q)}
    for v in values_mod_q:
        if v in counts:
            counts[v] += 1
    K_eff = sum(counts.values())  # only coprime values
    phi_q = totient(q)
    p = 1.0 / phi_q
    expected = K_eff * p

    n_minus1 = counts.get(q-1, 0)
    competitors = [counts[a] for a in counts if a not in (1, q-1)]
    if not competitors:
        return None
    n_max_other = max(competitors)
    D = n_minus1 - n_max_other

    # Variance under uniform null: Var(n_{-1} - n_a) = 2·K·p (multinomial)
    var = 2 * K_eff * p
    z = D / sqrt(var) if var > 0 else 0.0
    p_val = two_sided_pvalue(z)
    return {
        'q': q, 'K_eff': K_eff, 'K_total': K,
        'D': D, 'expected_var': var, 'z': z, 'p_two_sided': p_val,
        'n_minus1': n_minus1, 'n_max_competitor': n_max_other,
        'fraction_minus1': n_minus1 / K_eff if K_eff > 0 else 0,
        'fraction_uniform': p,
    }

def chi_squared_test(values_mod_q, q):
    """Pearson chi-squared for uniformity over coprime residues."""
    counts = {a: 0 for a in coprime_residues(q)}
    for v in values_mod_q:
        if v in counts:
            counts[v] += 1
    K_eff = sum(counts.values())
    phi_q = totient(q)
    expected = K_eff / phi_q
    chi2 = sum((c - expected)**2 / expected for c in counts.values())
    df = phi_q - 1
    # p-value via mpmath
    from mpmath import gammainc, mpf
    p = float(gammainc(mpf(df)/2, mpf(chi2)/2, regularized=True))
    return {'chi2': chi2, 'df': df, 'p': p, 'K_eff': K_eff}

# ============ POSITIVE CONTROL: raw primes ============

def positive_control(P_max=10**7, q_list=(3, 4, 5, 7, 8, 11)):
    print(f"\n=== POSITIVE CONTROL: primes ≤ {P_max:,} ===")
    print("Sieving primes...")
    t0 = time.time()
    primes = list(primerange(2, P_max))
    print(f"  Found {len(primes):,} primes in {time.time()-t0:.1f}s")

    for q in q_list:
        residues = [p % q for p in primes if gcd(p, q) == 1]
        d = D_q_test(residues, q)
        chi = chi_squared_test(residues, q)
        sig_chi = "***" if chi['p'] < 1e-3 else "  "
        if d is None:
            print(f"  q={q:2d}: (D_q undefined, only 2 coprime residues) | χ²={chi['chi2']:.2f} df={chi['df']} p={chi['p']:.4g} {sig_chi}")
            continue
        sig_d = "***" if d['p_two_sided'] < 1e-3 else "  "
        print(f"  q={q:2d}: D_q={d['D']:+6d}, z={d['z']:+6.2f}, p={d['p_two_sided']:.4g} {sig_d}  | χ²={chi['chi2']:.2f} df={chi['df']} p={chi['p']:.4g} {sig_chi}")
        print(f"          n_-1={d['n_minus1']:,}, n_max_other={d['n_max_competitor']:,}, frac_-1={d['fraction_minus1']:.5f} (uniform={d['fraction_uniform']:.5f})")

# ============ NEGATIVE CONTROL: /dev/urandom ============

def negative_control(K=10**6, q_list=(3, 4, 5, 7, 8, 11)):
    print(f"\n=== NEGATIVE CONTROL: /dev/urandom, K={K:,} ===")
    print("Reading random bytes...")
    t0 = time.time()
    with open('/dev/urandom', 'rb') as f:
        # 8 bytes per sample → 64-bit unsigned int
        raw = f.read(K * 8)
    samples = [int.from_bytes(raw[i*8:(i+1)*8], 'big') for i in range(K)]
    print(f"  Got {len(samples):,} 64-bit samples in {time.time()-t0:.1f}s")

    for q in q_list:
        residues = [s % q for s in samples if gcd(s, q) == 1]
        d = D_q_test(residues, q)
        chi = chi_squared_test(residues, q)
        sig_chi = "FAIL!" if chi['p'] < 1e-3 else "  "
        if d is None:
            print(f"  q={q:2d}: (D_q undefined) | χ²={chi['chi2']:.2f} df={chi['df']} p={chi['p']:.4g} {sig_chi}")
            continue
        sig_d = "FAIL!" if d['p_two_sided'] < 1e-3 else "  "
        print(f"  q={q:2d}: D_q={d['D']:+6d}, z={d['z']:+6.2f}, p={d['p_two_sided']:.4g} {sig_d}  | χ²={chi['chi2']:.2f} df={chi['df']} p={chi['p']:.4g} {sig_chi}")

if __name__ == "__main__":
    print("Crypto Bias Audit Framework — Validation Prototype")
    print("=" * 60)

    P_max = 10**7  # 10M
    print(f"\nConfig: positive control primes ≤ {P_max:,}, negative control 10^6 urandom samples")

    positive_control(P_max)
    negative_control()

    print("\n" + "=" * 60)
    print("DONE.")
    print("Expected: positive control shows D_q > 0 with significance for q where -1 is non-residue.")
    print("          negative control shows null (no significant deviations).")
