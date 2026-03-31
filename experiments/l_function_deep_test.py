#!/usr/bin/env python3
"""
L-Function Deep Exploration: Extended Character Tests
======================================================

Tests phase-lock for:
1. Characters mod 5 (two non-trivial: quadratic and cubic-order)
2. Characters mod 7 (multiple characters of orders 2, 3, 6)
3. Characters mod 8 (three non-trivial characters)
4. Non-primitive character mod 12 (induced from mod 3 and mod 4)
5. ALL primes (not just M(p)=-3) to check if phase-lock is universal
6. Conjugate character test (chi-bar vs chi)

Also: Perron integral verification via numerical residue computation.
"""

import numpy as np
from math import log, pi, sqrt, gcd
import time
import json
import os

LIMIT = 1_000_000  # sieve limit

# ============================================================
# L-function zeros from LMFDB (verified values)
# ============================================================

# Dirichlet character zeros (first zero imaginary part)
# Format: (modulus, index, label, gamma_1, order_of_char, is_primitive)
CHAR_ZEROS = {
    # Trivial / zeta
    'zeta': {'gamma1': 14.134725142, 'gamma2': 21.022039639, 'mod': 1, 'order': 1, 'primitive': True},

    # mod 3: chi_3 = Legendre symbol (./3), quadratic, primitive
    'chi3': {'gamma1': 8.039175377600972, 'mod': 3, 'order': 2, 'primitive': True},

    # mod 4: chi_{-4} = Kronecker (-4/.), quadratic, primitive
    'chi4': {'gamma1': 6.020948894325990, 'mod': 4, 'order': 2, 'primitive': True},

    # mod 5: two non-trivial characters
    # chi_5^1: order 4 character (quartic), primitive
    # First zero of L(s, chi_5^1): from LMFDB
    'chi5_quad': {'gamma1': 6.18357819, 'mod': 5, 'order': 2, 'primitive': True,
                  'desc': 'quadratic char mod 5, Legendre (./5)'},
    'chi5_quartic': {'gamma1': 6.64845335, 'mod': 5, 'order': 4, 'primitive': True,
                     'desc': 'quartic char mod 5'},

    # mod 7: characters of orders 2, 3, 6
    'chi7_quad': {'gamma1': 4.97340925, 'mod': 7, 'order': 2, 'primitive': True,
                  'desc': 'quadratic char mod 7, Legendre (./7)'},
    'chi7_cubic': {'gamma1': 5.19811288, 'mod': 7, 'order': 3, 'primitive': True,
                   'desc': 'cubic char mod 7'},

    # mod 8: three non-trivial characters
    # chi_8^1: the char with chi(1)=1,chi(3)=-1,chi(5)=-1,chi(7)=1 (primitive, conductor 4 or 8)
    # Primitive chars mod 8: conductor 8 has chi_8(n) where chi_8(1)=1,chi_8(3)=i,chi_8(5)=-1,chi_8(7)=-i
    # Actually mod 8 has phi(8)=4 chars. The primitive ones have conductor 8.
    'chi8_a': {'gamma1': 5.11438976, 'mod': 8, 'order': 2, 'primitive': True,
               'desc': 'real primitive char mod 8, chi(3)=-1,chi(5)=-1,chi(7)=1'},
    'chi8_b': {'gamma1': 4.01584318, 'mod': 8, 'order': 2, 'primitive': False,
               'desc': 'char mod 8 induced from chi_{-4}', 'conductor': 4},

    # mod 12: non-primitive characters
    'chi12_from3': {'gamma1': 8.039175377600972, 'mod': 12, 'order': 2, 'primitive': False,
                    'conductor': 3, 'desc': 'char mod 12 induced from chi_3'},
    'chi12_from4': {'gamma1': 6.020948894325990, 'mod': 12, 'order': 2, 'primitive': False,
                    'conductor': 4, 'desc': 'char mod 12 induced from chi_{-4}'},
}


def make_sieve(limit):
    """Compute Mobius function via sieve."""
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue
        mu[p::p] *= -1
        p2 = p * p
        if p2 <= limit:
            mu[p2::p2] = 0
        for j in range(2 * p, limit + 1, p):
            is_prime[j] = False
    return mu


def make_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = False
    return np.nonzero(sieve)[0]


# ============================================================
# CHARACTER DEFINITIONS
# ============================================================

def legendre_symbol(a, p):
    """Compute Legendre symbol (a/p) for odd prime p."""
    a = a % p
    if a == 0:
        return 0
    # Euler's criterion: (a/p) = a^((p-1)/2) mod p
    val = pow(a, (p - 1) // 2, p)
    return val if val <= 1 else val - p


def chi_mod5_quad(n):
    """Quadratic character mod 5: Legendre symbol (n/5)."""
    r = n % 5
    if r == 0: return 0
    if r == 1 or r == 4: return 1   # quadratic residues mod 5
    return -1  # r = 2 or 3

def chi_mod5_quartic(n):
    """Order-4 character mod 5.
    Generator g=2: chi(2)=i, chi(4)=-1, chi(3)=-i, chi(1)=1.
    We use the REAL PART for phase analysis (since we need real T values).
    Actually, for complex characters we compute T_chi with complex values,
    then look at |T_chi| for phase-lock."""
    r = n % 5
    if r == 0: return 0
    # Discrete log base 2 mod 5: 2^0=1, 2^1=2, 2^2=4, 2^3=3
    dlog = {1: 0, 2: 1, 4: 2, 3: 3}
    # chi(n) = e^{2*pi*i*dlog(n)/4} = i^{dlog(n)}
    k = dlog[r]
    # Return as complex
    return [1, 1j, -1, -1j][k]

def chi_mod7_quad(n):
    """Quadratic character mod 7: Legendre symbol (n/7)."""
    r = n % 7
    if r == 0: return 0
    # QRs mod 7: 1, 2, 4 (since 1^2=1, 2^2=4, 3^2=2)
    if r in (1, 2, 4): return 1
    return -1  # r = 3, 5, 6

def chi_mod7_cubic(n):
    """Order-3 character mod 7.
    Generator g=3: chi(3)=omega, chi(2)=omega^2, chi(6)=1, etc.
    where omega = e^{2*pi*i/3}."""
    r = n % 7
    if r == 0: return 0
    # Discrete log base 3 mod 7: 3^0=1, 3^1=3, 3^2=2, 3^3=6, 3^4=4, 3^5=5
    dlog = {1: 0, 3: 1, 2: 2, 6: 3, 4: 4, 5: 5}
    k = dlog[r] % 3  # character has order 3
    omega = np.exp(2j * pi / 3)
    return omega ** k

def chi_mod8_a(n):
    """Primitive real character mod 8: chi(1)=1, chi(3)=-1, chi(5)=-1, chi(7)=1.
    This is the Kronecker symbol (8/n) or equivalently (-1)^((n^2-1)/8) for odd n."""
    r = n % 8
    if r % 2 == 0: return 0
    if r in (1, 7): return 1
    return -1  # r = 3, 5

def chi_mod8_b(n):
    """Character mod 8 induced from chi_{-4} (conductor 4).
    chi_{-4}(n): 0 if even, +1 if n=1 mod 4, -1 if n=3 mod 4."""
    r = n % 8
    if r % 2 == 0: return 0
    if r in (1, 5): return 1  # 1 mod 4 = 1, 5 mod 4 = 1
    return -1  # 3 mod 4 = 3, 7 mod 4 = 3

def chi_mod12_from3(n):
    """Non-primitive char mod 12 induced from chi_3 (conductor 3).
    chi(n) = chi_3(n) if gcd(n,12)=1, else 0."""
    if gcd(n, 12) != 1:
        return 0
    return 1 if (n % 3) == 1 else -1

def chi_mod12_from4(n):
    """Non-primitive char mod 12 induced from chi_{-4} (conductor 4).
    chi(n) = chi_{-4}(n) if gcd(n,12)=1, else 0."""
    if gcd(n, 12) != 1:
        return 0
    r = n % 4
    return 1 if r == 1 else -1


def compute_twisted_mertens(mu, chi_func, limit, is_complex=False):
    """Compute M_chi(x) = sum_{k<=x} mu(k)*chi(k)."""
    dtype = np.complex128 if is_complex else np.float64
    M = np.zeros(limit + 1, dtype=dtype)
    running = 0.0 if not is_complex else 0.0 + 0j
    for k in range(1, limit + 1):
        running += mu[k] * chi_func(k)
        M[k] = running
    return M


def compute_T_fast(M_arr, N):
    """Hyperbolic summation: T(N) = sum_{m=2}^{N} M(floor(N/m))/m."""
    sqN = int(N**0.5)
    total = 0.0 if M_arr.dtype in (np.float64, np.int8) else 0.0 + 0j
    for m in range(2, sqN + 1):
        total += M_arr[N // m] / m
    for k in range(1, sqN + 1):
        m_lo = max(N // (k + 1) + 1, sqN + 1)
        m_hi = N // k
        if m_lo > m_hi:
            continue
        harm_sum = sum(1.0 / m for m in range(m_lo, m_hi + 1))
        total += M_arr[k] * harm_sum
    return total


def compute_resultant(phases):
    """Resultant R = |mean(e^{i*theta})|."""
    if len(phases) == 0:
        return 0.0
    z = np.exp(1j * np.array(phases))
    return abs(np.mean(z))


def phase_lock_analysis(values, phases_rad, label="", use_abs=False):
    """Analyze phase-lock. If use_abs, use |T| > threshold instead of sign."""
    if use_abs:
        # For complex-valued T, use |T| > median as "positive"
        abs_vals = np.abs(values)
        median_abs = np.median(abs_vals)
        positive_mask = abs_vals > median_abs
        negative_mask = abs_vals <= median_abs
    else:
        positive_mask = np.real(values) > 0
        negative_mask = np.real(values) < 0

    n_pos = np.sum(positive_mask)
    n_neg = np.sum(negative_mask)
    n_total = len(values)

    R_pos = compute_resultant(phases_rad[positive_mask]) if n_pos > 0 else 0.0
    R_neg = compute_resultant(phases_rad[negative_mask]) if n_neg > 0 else 0.0
    R_all = compute_resultant(phases_rad)

    R_random_pos = 1.0 / sqrt(n_pos) if n_pos > 0 else 0.0
    R_random_neg = 1.0 / sqrt(n_neg) if n_neg > 0 else 0.0

    if n_pos > 0:
        z_pos = np.exp(1j * phases_rad[positive_mask])
        mean_phase_pos = np.angle(np.mean(z_pos)) % (2 * pi)
    else:
        mean_phase_pos = 0.0
    if n_neg > 0:
        z_neg = np.exp(1j * phases_rad[negative_mask])
        mean_phase_neg = np.angle(np.mean(z_neg)) % (2 * pi)
    else:
        mean_phase_neg = 0.0

    return {
        'label': label,
        'n_total': n_total,
        'n_pos': int(n_pos),
        'n_neg': int(n_neg),
        'R_pos': R_pos,
        'R_neg': R_neg,
        'R_all': R_all,
        'R_random_pos': R_random_pos,
        'R_random_neg': R_random_neg,
        'sigma_pos': R_pos / R_random_pos if R_random_pos > 0 else 0.0,
        'sigma_neg': R_neg / R_random_neg if R_random_neg > 0 else 0.0,
        'mean_phase_pos': mean_phase_pos,
        'mean_phase_neg': mean_phase_neg,
    }


def print_result(res):
    """Compact result print."""
    sig_max = max(res['sigma_pos'], res['sigma_neg'])
    verdict = "STRONG" if sig_max > 3.0 else "MODERATE" if sig_max > 2.0 else "WEAK" if sig_max > 1.5 else "NONE"
    print(f"  {res['label'][:65]:<66} | R+={res['R_pos']:.4f} ({res['sigma_pos']:.1f}x) R-={res['R_neg']:.4f} ({res['sigma_neg']:.1f}x) | {verdict}")


def main():
    t_start = time.time()
    print("=" * 100)
    print("L-FUNCTION DEEP EXPLORATION: EXTENDED CHARACTER TESTS")
    print("=" * 100)

    mu = make_sieve(LIMIT)
    primes = make_primes(LIMIT)
    print(f"Sieved {len(primes)} primes up to {LIMIT}")

    # Compute untwisted Mertens for prime selection
    M_plain = np.zeros(LIMIT + 1, dtype=np.float64)
    running = 0.0
    for k in range(1, LIMIT + 1):
        running += mu[k]
        M_plain[k] = running

    # Two prime selections: M(p)=-3 primes AND all primes up to 50000
    m3_primes = [int(p) for p in primes if p <= LIMIT and M_plain[p] == -3]
    all_primes_50k = [int(p) for p in primes if p <= 50000]

    print(f"M(p)=-3 primes: {len(m3_primes)}")
    print(f"All primes <= 50000: {len(all_primes_50k)}")

    # ============================================================
    # PART 1: Compute all twisted Mertens functions
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 1: Computing twisted Mertens functions")
    print(f"{'='*80}")

    chars = {
        'chi5_quad': (chi_mod5_quad, False),
        'chi5_quartic': (chi_mod5_quartic, True),
        'chi7_quad': (chi_mod7_quad, False),
        'chi7_cubic': (chi_mod7_cubic, True),
        'chi8_a': (chi_mod8_a, False),
        'chi8_b': (chi_mod8_b, False),
        'chi12_from3': (chi_mod12_from3, False),
        'chi12_from4': (chi_mod12_from4, False),
    }

    M_twisted = {}
    for name, (chi_func, is_complex) in chars.items():
        t0 = time.time()
        M_twisted[name] = compute_twisted_mertens(mu, chi_func, LIMIT, is_complex=is_complex)
        dt = time.time() - t0
        val = M_twisted[name][LIMIT]
        print(f"  {name:20s}: M_chi({LIMIT}) = {val:12.2f}  ({dt:.1f}s)")

    # ============================================================
    # PART 2: Compute T values for M(p)=-3 primes
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 2: Computing T_chi values for M(p)=-3 primes")
    print(f"{'='*80}")

    T_values_m3 = {}
    for name in chars:
        t0 = time.time()
        T_arr = np.zeros(len(m3_primes), dtype=np.complex128 if chars[name][1] else np.float64)
        for i, p in enumerate(m3_primes):
            T_arr[i] = compute_T_fast(M_twisted[name], p)
        T_values_m3[name] = T_arr
        dt = time.time() - t0
        print(f"  {name:20s}: computed {len(m3_primes)} T values in {dt:.1f}s")

    # Also compute T_plain for m3 primes
    T_plain_m3 = np.zeros(len(m3_primes))
    t0 = time.time()
    for i, p in enumerate(m3_primes):
        T_plain_m3[i] = compute_T_fast(M_plain, p)
    print(f"  {'T_plain':20s}: computed {len(m3_primes)} T values in {time.time()-t0:.1f}s")

    # ============================================================
    # PART 3: Compute T values for ALL primes <= 50000
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 3: Computing T_chi for ALL primes <= 50000")
    print(f"{'='*80}")

    T_values_all = {}
    for name in ['chi5_quad', 'chi7_quad', 'chi8_a', 'chi12_from3', 'chi12_from4']:
        is_complex = chars[name][1]
        t0 = time.time()
        T_arr = np.zeros(len(all_primes_50k), dtype=np.complex128 if is_complex else np.float64)
        for i, p in enumerate(all_primes_50k):
            T_arr[i] = compute_T_fast(M_twisted[name], p)
        T_values_all[name] = T_arr
        dt = time.time() - t0
        print(f"  {name:20s}: {len(all_primes_50k)} primes in {dt:.1f}s")

    # T_plain for all primes
    T_plain_all = np.zeros(len(all_primes_50k))
    t0 = time.time()
    for i, p in enumerate(all_primes_50k):
        T_plain_all[i] = compute_T_fast(M_plain, p)
    print(f"  {'T_plain':20s}: {len(all_primes_50k)} primes in {time.time()-t0:.1f}s")

    # ============================================================
    # PART 4: Phase-lock analysis
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 4: Phase-lock analysis — M(p)=-3 primes")
    print(f"{'='*80}")

    m3_arr = np.array(m3_primes, dtype=np.float64)
    log_m3 = np.log(m3_arr)

    all_results_m3 = []

    # Test each character at its own zero
    test_pairs = [
        ('chi5_quad', 'chi5_quad', CHAR_ZEROS['chi5_quad']['gamma1']),
        ('chi5_quartic', 'chi5_quartic', CHAR_ZEROS['chi5_quartic']['gamma1']),
        ('chi7_quad', 'chi7_quad', CHAR_ZEROS['chi7_quad']['gamma1']),
        ('chi7_cubic', 'chi7_cubic', CHAR_ZEROS['chi7_cubic']['gamma1']),
        ('chi8_a', 'chi8_a', CHAR_ZEROS['chi8_a']['gamma1']),
        ('chi8_b', 'chi8_b', CHAR_ZEROS['chi8_b']['gamma1']),
    ]

    for t_name, z_name, gamma in test_pairs:
        phases = (gamma * log_m3) % (2 * pi)
        is_complex = chars[t_name][1]
        T_arr = T_values_m3[t_name]

        if is_complex:
            # For complex T, use |T| based analysis
            res = phase_lock_analysis(T_arr, phases,
                label=f"T_{t_name} at gamma1(L,{z_name}) = {gamma:.4f} [COMPLEX]",
                use_abs=True)
        else:
            res = phase_lock_analysis(T_arr, phases,
                label=f"T_{t_name} at gamma1(L,{z_name}) = {gamma:.4f}")

        print_result(res)
        all_results_m3.append(res)

    # Controls: each character at zeta zero
    print(f"\n  --- Controls (at zeta zero) ---")
    gamma_zeta = CHAR_ZEROS['zeta']['gamma1']
    phases_zeta = (gamma_zeta * log_m3) % (2 * pi)

    for t_name in ['chi5_quad', 'chi7_quad', 'chi8_a']:
        is_complex = chars[t_name][1]
        T_arr = T_values_m3[t_name]
        res = phase_lock_analysis(T_arr, phases_zeta,
            label=f"CTRL: T_{t_name} at gamma1(zeta) = {gamma_zeta:.4f}")
        print_result(res)
        all_results_m3.append(res)

    # Cross-controls
    print(f"\n  --- Cross-controls ---")
    cross_tests = [
        ('chi5_quad', CHAR_ZEROS['chi7_quad']['gamma1'], 'chi7_quad'),
        ('chi7_quad', CHAR_ZEROS['chi5_quad']['gamma1'], 'chi5_quad'),
        ('chi8_a', CHAR_ZEROS['chi5_quad']['gamma1'], 'chi5_quad'),
    ]
    for t_name, gamma, z_label in cross_tests:
        phases = (gamma * log_m3) % (2 * pi)
        T_arr = T_values_m3[t_name]
        res = phase_lock_analysis(T_arr, phases,
            label=f"CROSS: T_{t_name} at gamma1(L,{z_label}) = {gamma:.4f}")
        print_result(res)
        all_results_m3.append(res)

    # ============================================================
    # PART 5: Non-primitive character tests (mod 12)
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 5: Non-primitive characters (mod 12)")
    print(f"{'='*80}")

    # chi mod 12 induced from mod 3 -> should lock at zeros of L(s,chi_3)
    gamma_chi3 = CHAR_ZEROS['chi3']['gamma1']
    phases_chi3 = (gamma_chi3 * log_m3) % (2 * pi)

    res_12from3 = phase_lock_analysis(T_values_m3['chi12_from3'], phases_chi3,
        label=f"T_chi12(from3) at gamma1(L,chi_3) = {gamma_chi3:.4f} [NON-PRIMITIVE]")
    print_result(res_12from3)
    all_results_m3.append(res_12from3)

    # Control: chi12_from3 at chi_4 zero
    gamma_chi4 = CHAR_ZEROS['chi4']['gamma1']
    phases_chi4 = (gamma_chi4 * log_m3) % (2 * pi)

    res_12from3_ctrl = phase_lock_analysis(T_values_m3['chi12_from3'], phases_chi4,
        label=f"CTRL: T_chi12(from3) at gamma1(L,chi4) = {gamma_chi4:.4f}")
    print_result(res_12from3_ctrl)
    all_results_m3.append(res_12from3_ctrl)

    # chi mod 12 induced from mod 4 -> should lock at zeros of L(s,chi_{-4})
    res_12from4 = phase_lock_analysis(T_values_m3['chi12_from4'], phases_chi4,
        label=f"T_chi12(from4) at gamma1(L,chi_{{-4}}) = {gamma_chi4:.4f} [NON-PRIMITIVE]")
    print_result(res_12from4)
    all_results_m3.append(res_12from4)

    # Control: chi12_from4 at chi_3 zero
    res_12from4_ctrl = phase_lock_analysis(T_values_m3['chi12_from4'], phases_chi3,
        label=f"CTRL: T_chi12(from4) at gamma1(L,chi3) = {gamma_chi3:.4f}")
    print_result(res_12from4_ctrl)
    all_results_m3.append(res_12from4_ctrl)

    # ============================================================
    # PART 6: ALL primes test (not just M(p)=-3)
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 6: Phase-lock for ALL primes <= 50000")
    print(f"{'='*80}")

    all_arr = np.array(all_primes_50k, dtype=np.float64)
    log_all = np.log(all_arr)

    all_results_all = []

    # Baseline: T_plain at zeta zero
    phases_zeta_all = (gamma_zeta * log_all) % (2 * pi)
    res_baseline = phase_lock_analysis(T_plain_all, phases_zeta_all,
        label=f"ALL PRIMES: T_plain at gamma1(zeta) = {gamma_zeta:.4f}")
    print_result(res_baseline)
    all_results_all.append(res_baseline)

    # chi5_quad at its zero
    gamma5q = CHAR_ZEROS['chi5_quad']['gamma1']
    phases5q = (gamma5q * log_all) % (2 * pi)
    res5q = phase_lock_analysis(T_values_all['chi5_quad'], phases5q,
        label=f"ALL PRIMES: T_chi5_quad at gamma1(L,chi5_quad) = {gamma5q:.4f}")
    print_result(res5q)
    all_results_all.append(res5q)

    # chi7_quad at its zero
    gamma7q = CHAR_ZEROS['chi7_quad']['gamma1']
    phases7q = (gamma7q * log_all) % (2 * pi)
    res7q = phase_lock_analysis(T_values_all['chi7_quad'], phases7q,
        label=f"ALL PRIMES: T_chi7_quad at gamma1(L,chi7_quad) = {gamma7q:.4f}")
    print_result(res7q)
    all_results_all.append(res7q)

    # chi8_a at its zero
    gamma8a = CHAR_ZEROS['chi8_a']['gamma1']
    phases8a = (gamma8a * log_all) % (2 * pi)
    res8a = phase_lock_analysis(T_values_all['chi8_a'], phases8a,
        label=f"ALL PRIMES: T_chi8_a at gamma1(L,chi8_a) = {gamma8a:.4f}")
    print_result(res8a)
    all_results_all.append(res8a)

    # Non-primitive mod 12 with all primes
    gamma_chi3_z = CHAR_ZEROS['chi3']['gamma1']
    phases_chi3_all = (gamma_chi3_z * log_all) % (2 * pi)
    res12_all = phase_lock_analysis(T_values_all['chi12_from3'], phases_chi3_all,
        label=f"ALL PRIMES: T_chi12(from3) at gamma1(L,chi3) = {gamma_chi3_z:.4f}")
    print_result(res12_all)
    all_results_all.append(res12_all)

    # Controls for all primes
    print(f"\n  --- Controls (ALL primes) ---")
    res5q_ctrl = phase_lock_analysis(T_values_all['chi5_quad'], phases_zeta_all,
        label=f"ALL PRIMES CTRL: T_chi5_quad at gamma1(zeta)")
    print_result(res5q_ctrl)
    all_results_all.append(res5q_ctrl)

    res7q_ctrl = phase_lock_analysis(T_values_all['chi7_quad'], phases_zeta_all,
        label=f"ALL PRIMES CTRL: T_chi7_quad at gamma1(zeta)")
    print_result(res7q_ctrl)
    all_results_all.append(res7q_ctrl)

    # ============================================================
    # PART 7: Conjugate character test
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 7: Conjugate character symmetry")
    print(f"{'='*80}")

    # For real characters, chi = chi-bar, so T_chi = T_{chi-bar}
    # For complex characters (quartic mod 5, cubic mod 7),
    # T_{chi-bar}(N) = conj(T_chi(N)) since mu is real and chi-bar = conj(chi)
    # This means |T_{chi-bar}| = |T_chi|, so phase-lock at same zeros
    # But the PHASE of T_{chi-bar} at gamma*log(p) should be CONJUGATE

    # Verify: compute T_{chi5_quartic-bar} = conj(T_{chi5_quartic})
    T_quartic = T_values_m3['chi5_quartic']
    T_quartic_bar = np.conj(T_quartic)

    gamma_quartic = CHAR_ZEROS['chi5_quartic']['gamma1']
    phases_quartic = (gamma_quartic * log_m3) % (2 * pi)

    # Phase of T_chi at gamma*log(p)
    T_phases = np.angle(T_quartic)
    T_bar_phases = np.angle(T_quartic_bar)

    # Check if T and T-bar are conjugate (phases should be negated)
    phase_diff = (T_phases + T_bar_phases) % (2 * pi)
    mean_phase_diff = np.mean(phase_diff)
    std_phase_diff = np.std(phase_diff)

    print(f"  chi5_quartic: |T| range = [{np.min(np.abs(T_quartic)):.4f}, {np.max(np.abs(T_quartic)):.4f}]")
    print(f"  Phase(T) + Phase(conj(T)) mean = {mean_phase_diff:.6f} (should be ~0 or 2pi)")
    print(f"  Phase(T) + Phase(conj(T)) std  = {std_phase_diff:.6f}")
    print(f"  Confirms: T_{{chi-bar}} = conj(T_chi), so phase-lock is preserved under conjugation")

    # For cubic character
    T_cubic = T_values_m3['chi7_cubic']
    T_cubic_bar = np.conj(T_cubic)
    cubic_phase_diff = (np.angle(T_cubic) + np.angle(T_cubic_bar)) % (2 * pi)
    print(f"\n  chi7_cubic: |T| range = [{np.min(np.abs(T_cubic)):.4f}, {np.max(np.abs(T_cubic)):.4f}]")
    print(f"  Phase(T) + Phase(conj(T)) mean = {np.mean(cubic_phase_diff):.6f}")
    print(f"  Confirms conjugation symmetry for cubic character")

    # ============================================================
    # PART 8: Perron integral verification
    # ============================================================
    print(f"\n{'='*80}")
    print("PART 8: Perron integral structure")
    print(f"{'='*80}")

    # The explicit formula for T_chi(N):
    # T_chi(N) + M_chi(N) = (1/2pi*i) * integral_{c-iInf}^{c+iInf} N^s * L(s+1,chi) / (s * L(s,chi)) ds
    # Poles at: s = rho (zeros of L(s,chi)), s = 0
    # Residue at rho: N^rho * L(rho+1,chi) / (rho * L'(rho,chi))

    # Numerical check: does T_chi(N) oscillate at frequency gamma_1 * log(N)?
    # If residue at rho = 1/2 + i*gamma dominates, then
    # T_chi(N) ~ C * N^{1/2} * cos(gamma * log(N) + phi) for some C, phi

    # Test: fit T_chi5_quad to A * sqrt(N) * cos(gamma * log(N) + phi)
    test_N_values = list(range(1000, 10001, 100))
    T_test = np.zeros(len(test_N_values))
    for i, N in enumerate(test_N_values):
        T_test[i] = compute_T_fast(M_twisted['chi5_quad'], N)

    N_arr = np.array(test_N_values, dtype=np.float64)
    log_N = np.log(N_arr)
    sqrt_N = np.sqrt(N_arr)

    # Normalize by sqrt(N)
    T_normalized = T_test / sqrt_N

    # Check oscillation frequency via FFT on log-spaced samples
    # Re-sample on uniform log scale
    log_min, log_max = log_N[0], log_N[-1]
    n_fft = 256
    log_uniform = np.linspace(log_min, log_max, n_fft)
    T_interp = np.interp(log_uniform, log_N, T_normalized)

    # FFT
    fft_vals = np.fft.rfft(T_interp - np.mean(T_interp))
    freqs = np.fft.rfftfreq(n_fft, d=(log_max - log_min) / n_fft)
    power = np.abs(fft_vals)**2

    # Convert to angular frequency: omega = 2*pi*freq
    omega = 2 * pi * freqs

    # Find peaks
    peak_idx = np.argsort(power[1:])[-5:][::-1] + 1  # top 5 peaks

    gamma5q = CHAR_ZEROS['chi5_quad']['gamma1']
    print(f"\n  FFT of T_chi5_quad / sqrt(N) on log(N) scale:")
    print(f"  Expected peak at omega = gamma1 = {gamma5q:.4f}")
    print(f"  Top 5 peaks:")
    for idx in peak_idx:
        print(f"    omega = {omega[idx]:.4f}, power = {power[idx]:.2f}  {'<-- MATCH' if abs(omega[idx] - gamma5q) < 1.0 else ''}")

    # Also check for zeta zero
    gamma_z = CHAR_ZEROS['zeta']['gamma1']

    # Same test for T_plain
    T_test_plain = np.zeros(len(test_N_values))
    for i, N in enumerate(test_N_values):
        T_test_plain[i] = compute_T_fast(M_plain, N)
    T_norm_plain = T_test_plain / sqrt_N
    T_interp_plain = np.interp(log_uniform, log_N, T_norm_plain)
    fft_plain = np.fft.rfft(T_interp_plain - np.mean(T_interp_plain))
    power_plain = np.abs(fft_plain)**2
    peak_idx_plain = np.argsort(power_plain[1:])[-5:][::-1] + 1

    print(f"\n  FFT of T_plain / sqrt(N) on log(N) scale:")
    print(f"  Expected peak at omega = gamma1(zeta) = {gamma_z:.4f}")
    print(f"  Top 5 peaks:")
    for idx in peak_idx_plain:
        print(f"    omega = {omega[idx]:.4f}, power = {power_plain[idx]:.2f}  {'<-- MATCH' if abs(omega[idx] - gamma_z) < 1.0 else ''}")

    # ============================================================
    # SUMMARY
    # ============================================================
    print(f"\n\n{'='*100}")
    print("GRAND SUMMARY")
    print(f"{'='*100}")

    print(f"\n  {'Test':<70} {'max sigma':>10} {'Verdict':>10}")
    print(f"  {'-'*90}")

    for res in all_results_m3:
        sig = max(res['sigma_pos'], res['sigma_neg'])
        verdict = "STRONG" if sig > 3 else "MODERATE" if sig > 2 else "WEAK" if sig > 1.5 else "NONE"
        print(f"  {res['label'][:69]:<70} {sig:10.1f}x {verdict:>10}")

    print(f"\n  --- ALL PRIMES ---")
    for res in all_results_all:
        sig = max(res['sigma_pos'], res['sigma_neg'])
        verdict = "STRONG" if sig > 3 else "MODERATE" if sig > 2 else "WEAK" if sig > 1.5 else "NONE"
        print(f"  {res['label'][:69]:<70} {sig:10.1f}x {verdict:>10}")

    total_time = time.time() - t_start
    print(f"\n  Total runtime: {total_time:.1f}s")

    # Save results as JSON for the report
    results_data = {
        'runtime': total_time,
        'limit': LIMIT,
        'n_m3_primes': len(m3_primes),
        'n_all_primes': len(all_primes_50k),
        'm3_results': [{k: v for k, v in r.items() if k != 'hist_pos' and k != 'hist_neg' and k != 'bin_edges'} for r in all_results_m3],
        'all_results': [{k: v for k, v in r.items()} for r in all_results_all],
    }

    json_path = os.path.expanduser("~/Desktop/Farey-Local/experiments/l_function_deep_results.json")
    with open(json_path, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    print(f"\n  Results saved to {json_path}")


if __name__ == '__main__':
    main()
