#!/usr/bin/env python3
"""
ALTERNATIVE PROOF APPROACHES for B+C > 0
=========================================

Four independent analytical strategies, each with concrete numerical computation.

Approach 1: T_b analysis — what fraction of delta_sq comes from "good" denominators?
Approach 2: Probabilistic concentration via variance bounds
Approach 3: Tighter bound on h>=2 Fourier modes via multiplicative structure of S_N(h)
Approach 4: Ratio test — weaker sufficient condition exploiting D/A ~ 1
"""

import time
from math import gcd, isqrt, pi, sqrt, log, cos, sin, floor, ceil
from collections import defaultdict
import sys

start_time = time.time()

def elapsed():
    return time.time() - start_time

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return sieve

def prime_list(limit):
    s = sieve_primes(limit)
    return [i for i in range(2, limit + 1) if s[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def mobius_sieve(limit):
    """Compute mu(n) for n up to limit."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    is_prime = [True] * (limit + 1)
    primes = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def mertens_function(limit, mu=None):
    """Compute M(n) = sum_{k=1}^{n} mu(k) for all n up to limit."""
    if mu is None:
        mu = mobius_sieve(limit)
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i-1] + mu[i]
    return M

def farey_sequence(N):
    """Generate Farey sequence F_N as list of (a,b) pairs."""
    fracs = [(0, 1)]
    a, b, c, d = 0, 1, 1, N
    while c <= N:
        fracs.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return fracs

def analyze_prime_full(p, phi_arr):
    """Compute B_raw, C_raw, D values, and per-denominator decomposition."""
    N = p - 1
    n = 1 + sum(phi_arr[k] for k in range(1, N + 1))

    fracs = farey_sequence(N)

    # Per-denominator accumulators
    denom_delta_sq = defaultdict(float)  # delta^2 by denominator
    denom_D_delta = defaultdict(float)   # D*delta by denominator
    denom_count = defaultdict(int)

    sum_D_sq = 0.0
    sum_D_delta = 0.0
    sum_delta_sq = 0.0

    for idx, (a, b) in enumerate(fracs):
        fv = a / b
        D = idx - n * fv
        pa_mod_b = (p * a) % b
        delta = (a - pa_mod_b) / b

        sum_D_sq += D * D
        sum_D_delta += D * delta
        sum_delta_sq += delta * delta

        if b >= 2:
            denom_delta_sq[b] += delta * delta
            denom_D_delta[b] += D * delta
            denom_count[b] += 1

    B_raw = 2.0 * sum_D_delta
    C_raw = sum_delta_sq

    return {
        'p': p, 'N': N, 'n': n,
        'old_D_sq': sum_D_sq,
        'B_raw': B_raw,
        'C_raw': C_raw,
        'B_plus_C': B_raw + C_raw,
        'denom_delta_sq': dict(denom_delta_sq),
        'denom_D_delta': dict(denom_D_delta),
        'denom_count': dict(denom_count),
    }


# ==============================================================================
# APPROACH 1: T_b analysis — good denominators (b | p^2-1)
# ==============================================================================

def approach1_good_denominators(p, data):
    """
    For b | (p-1): delta = 0 for all a coprime to b (since p ≡ 1 mod b).
    For b | (p+1): T_b >= 0 via involution pairing (proved).

    Question: what fraction of total delta_sq comes from these "good" denominators?
    """
    N = p - 1
    p_sq_minus_1 = p * p - 1  # = (p-1)(p+1)

    total_delta_sq = data['C_raw']

    good_delta_sq = 0.0  # from b | (p^2-1)
    good_D_delta = 0.0
    zero_delta_sq = 0.0   # from b | (p-1) where delta=0
    involution_delta_sq = 0.0  # from b | (p+1) but not b | (p-1)
    bad_delta_sq = 0.0
    bad_D_delta = 0.0

    n_good = 0
    n_bad = 0
    n_zero = 0
    n_involution = 0

    for b, dsq in data['denom_delta_sq'].items():
        if b <= 1:
            continue
        if (p - 1) % b == 0:
            # b | (p-1): p ≡ 1 mod b, so sigma_p = identity, delta = 0
            zero_delta_sq += dsq
            good_delta_sq += dsq
            n_zero += 1
            n_good += 1
        elif p_sq_minus_1 % b == 0:
            # b | (p+1) but not b | (p-1): involution applies, T_b >= 0
            involution_delta_sq += dsq
            good_delta_sq += dsq
            good_D_delta += data['denom_D_delta'].get(b, 0)
            n_involution += 1
            n_good += 1
        else:
            bad_delta_sq += dsq
            bad_D_delta += data['denom_D_delta'].get(b, 0)
            n_bad += 1

    total_denoms = n_good + n_bad

    return {
        'total_delta_sq': total_delta_sq,
        'good_delta_sq': good_delta_sq,
        'zero_delta_sq': zero_delta_sq,
        'involution_delta_sq': involution_delta_sq,
        'bad_delta_sq': bad_delta_sq,
        'good_fraction': good_delta_sq / total_delta_sq if total_delta_sq > 0 else 0,
        'bad_fraction': bad_delta_sq / total_delta_sq if total_delta_sq > 0 else 0,
        'n_good': n_good,
        'n_bad': n_bad,
        'n_zero': n_zero,
        'n_involution': n_involution,
        'total_denoms': total_denoms,
        'bad_D_delta': bad_D_delta,
        'bad_2Ddelta_plus_dsq': 2 * bad_D_delta + bad_delta_sq,
        'good_D_delta': good_D_delta,
    }


# ==============================================================================
# APPROACH 2: Probabilistic concentration — variance of B_raw
# ==============================================================================

def approach2_variance(p, data, phi_arr):
    """
    Model: for each denominator b, the per-denominator contribution X_b = (2/b) * Sum_a D(a/b) * delta(a/b)
    Treat sigma_p as a random permutation on each S_b.

    E[X_b] comes from the h=1 Fourier mode (the correlation of D and the linear function).
    Var[X_b] can be bounded from Sum D(a/b)^2 and Sum a^2.

    Key: if Var[B_raw] << E[B_raw]^2, concentration gives B_raw > 0 whp.
    """
    N = p - 1

    # Per-denominator analysis
    fracs = farey_sequence(N)
    n = len(fracs)

    # Group by denominator
    denom_groups = defaultdict(list)
    for idx, (a, b) in enumerate(fracs):
        fv = a / b
        D = idx - n * fv
        denom_groups[b].append((a, D))

    total_E_X = 0.0
    total_Var_X = 0.0
    denom_details = []

    for b in sorted(denom_groups.keys()):
        if b <= 1:
            continue

        pairs = denom_groups[b]
        k = len(pairs)
        if k <= 1:
            continue

        avals = [a for a, D in pairs]
        Dvals = [D for a, D in pairs]

        # Under random permutation sigma on {a_1,...,a_k}:
        # E[Sum a_i * sigma(a_i)] = (Sum a_i)^2 / k
        # So E[Sum a_i * delta(a_i)] = E[Sum a_i * (a_i - sigma(a_i))/b]
        #     = (1/b) * [Sum a_i^2 - (Sum a_i)^2 / k]
        #     = (1/b) * Var(a) * k  (where Var is sample variance)

        sum_a = sum(avals)
        sum_a2 = sum(a*a for a in avals)
        sum_D = sum(Dvals)
        sum_D2 = sum(D*D for D in Dvals)
        sum_aD = sum(a*D for a, D in pairs)

        # E[X_b] = (2/b) * Cov_perm(a, D) where permutation acts on a
        # For random permutation sigma: E[Sum D_i * a_{sigma(i)}] = sum_D * sum_a / k
        # So E[Sum D_i * (a_i - a_{sigma(i)})] = sum_aD - sum_D * sum_a / k
        # = Cov(a, D) * k / (k-1) * (k-1)  ... let me be precise

        # Under uniform random permutation sigma of {a_1,...,a_k}:
        # E[sigma(a_i)] = sum_a / k for any i
        # E[a_i * sigma(a_i)] = ... this is trickier since sigma permutes the multiset

        # Actually delta(a/b) = (a - pa mod b)/b. Under random permutation model,
        # pa mod b is replaced by a random permutation of {a_1,...,a_k}.
        # So delta_random = (a_i - sigma(a_i))/b.

        # E[X_b] = (2/b) * Sum_i D_i * E[(a_i - sigma(a_i))/b]
        #        = (2/b^2) * Sum_i D_i * (a_i - sum_a/k)
        #        = (2/b^2) * (sum_aD - sum_D * sum_a / k)

        E_X_b = (2.0 / (b * b)) * (sum_aD - sum_D * sum_a / k)

        # Variance of X_b under random permutation:
        # X_b = (2/b) * Sum_i D_i * (a_i - sigma(a_i))/b = (2/b^2) * [sum_aD - Sum_i D_i * sigma(a_i)]
        # Var[X_b] = (4/b^4) * Var[Sum_i D_i * sigma(a_i)]

        # For random permutation sigma of {a_1,...,a_k}:
        # Var[Sum D_i * a_{sigma(i)}] = [1/(k-1)] * [k*sum_D2*sum_a2/k - (sum_D*sum_a)^2/k] / k
        # Standard formula: Var = (1/(k-1)) * [sum_D2 * sum_a2 / k - (sum_D * sum_a / k)^2]

        # Actually the exact formula for permutation variance:
        # Var[Sum_i x_i y_{sigma(i)}] = (1/(k-1)) * [sum(x^2)*sum(y^2)/k - (sum(x)*sum(y)/k)^2] * (k-1)
        # Wait, let me use the standard result:
        # E[Sum x_i y_{sigma(i)}] = sum_x * sum_y / k
        # Var[Sum x_i y_{sigma(i)}] = [1/(k-1)] * [(sum_x2 - sum_x^2/k) * (sum_y2 - sum_y^2/k)]
        #                           = [1/(k-1)] * Var_x * k * Var_y * k / ...

        # Correct formula (see e.g. Hoeffding 1951):
        # Var[Sum_{i=1}^k x_i * y_{pi(i)}] = (1/(k-1)) * S_xx * S_yy
        # where S_xx = Sum (x_i - x_bar)^2, S_yy = Sum (y_i - y_bar)^2

        S_DD = sum_D2 - sum_D * sum_D / k
        S_aa = sum_a2 - sum_a * sum_a / k

        if k > 1:
            var_perm = S_DD * S_aa / (k - 1)
        else:
            var_perm = 0.0

        Var_X_b = (4.0 / (b**4)) * var_perm

        total_E_X += E_X_b
        total_Var_X += Var_X_b

        if b <= 30 or b == N:
            denom_details.append({
                'b': b, 'k': k,
                'E_X_b': E_X_b, 'Var_X_b': Var_X_b,
            })

    # total_E_X should equal B_raw (approximately)
    # Chebyshev: P(B_raw < 0) <= Var / E^2 if E > 0

    E_B_raw = total_E_X  # This is E[B_raw] under the random permutation model
    Var_B_raw = total_Var_X
    std_B_raw = sqrt(Var_B_raw) if Var_B_raw > 0 else 0

    actual_B_raw = data['B_raw']

    # Signal-to-noise ratio
    snr = E_B_raw / std_B_raw if std_B_raw > 0 else float('inf')

    # Chebyshev bound on P(B_raw < 0)
    chebyshev_bound = Var_B_raw / (E_B_raw ** 2) if E_B_raw > 0 else float('inf')

    return {
        'E_B_raw': E_B_raw,
        'Var_B_raw': Var_B_raw,
        'std_B_raw': std_B_raw,
        'actual_B_raw': actual_B_raw,
        'SNR': snr,
        'chebyshev_P_neg': chebyshev_bound,
        'E_over_actual': E_B_raw / actual_B_raw if actual_B_raw != 0 else float('inf'),
    }


# ==============================================================================
# APPROACH 3: Fourier modes — bounding |Sum_{h>=2} B_raw|_h|
# ==============================================================================

def approach3_fourier_modes(p, phi_arr):
    """
    B_raw = Sum_h B_raw|_h where B_raw|_h = S_N(h)/(2*pi) * C_h(p).

    S_N(h) = Sum_{d|h, d<=N} d * M(N/d) uses the Mertens function.
    C_h(p) = Sum_{prime b<=N, b>1} [cot(pi*h*rho_b/b) - cot(pi*h/b)].

    We compute the first few modes exactly and bound the tail.
    """
    N = p - 1
    primes = prime_list(N)
    mu = mobius_sieve(N)
    M = mertens_function(N, mu)

    # Compute S_N(h) for h = 1, ..., H_max
    H_max = min(50, N)

    def compute_S_N(h):
        """S_N(h) = Sum_{d|h, d<=N} d * M(floor(N/d))"""
        s = 0
        for d in range(1, min(h, N) + 1):
            if h % d == 0:
                s += d * M[N // d]
        return s

    def compute_C_h(h, p, primes, N):
        """C_h(p) = Sum_{prime b<=N} [cot(pi*h*rho_b/b) - cot(pi*h/b)]"""
        import math
        total = 0.0
        for b in primes:
            if b <= 1:
                continue
            rho_b = p % b
            if rho_b == 0:
                continue  # p = b, skip

            # cot(pi*h*rho_b/b) - cot(pi*h/b)
            arg1 = pi * h * rho_b / b
            arg2 = pi * h / b

            # Avoid exact multiples of pi
            sin1 = math.sin(arg1)
            sin2 = math.sin(arg2)

            if abs(sin1) < 1e-15 or abs(sin2) < 1e-15:
                continue  # skip degenerate cases

            cot1 = math.cos(arg1) / sin1
            cot2 = math.cos(arg2) / sin2

            total += cot1 - cot2

        return total

    modes = []
    B_raw_from_modes = 0.0
    B_raw_h1 = None
    sum_h_geq_2 = 0.0

    for h in range(1, H_max + 1):
        S = compute_S_N(h)
        C = compute_C_h(h, p, primes, N)
        B_h = S * C / (2 * pi)
        B_raw_from_modes += B_h

        if h == 1:
            B_raw_h1 = B_h
        else:
            sum_h_geq_2 += B_h

        if h <= 20:
            modes.append({
                'h': h, 'S_N_h': S, 'C_h_p': C, 'B_raw_h': B_h,
            })

    delta_sq = sum(phi_arr[b] for b in range(2, N+1)) * 1.0  # rough
    # Actually compute delta_sq properly
    delta_sq = 0.0
    fracs = farey_sequence(N)
    n = len(fracs)
    for idx, (a, b) in enumerate(fracs):
        if b <= 1:
            continue
        pa_mod_b = (p * a) % b
        delta = (a - pa_mod_b) / b
        delta_sq += delta * delta

    return {
        'B_raw_h1': B_raw_h1,
        'sum_h_geq_2': sum_h_geq_2,
        'B_raw_from_modes': B_raw_from_modes,
        'delta_sq': delta_sq,
        'ratio_h1_to_dsq': B_raw_h1 / delta_sq if delta_sq > 0 else 0,
        'ratio_tail_to_dsq': sum_h_geq_2 / delta_sq if delta_sq > 0 else 0,
        'ratio_tail_to_h1': abs(sum_h_geq_2) / abs(B_raw_h1) if B_raw_h1 != 0 else float('inf'),
        'M_N': M[N],
        'modes': modes,
    }


# ==============================================================================
# APPROACH 4: Ratio test — weaker sufficient condition
# ==============================================================================

def approach4_ratio_test(p, data, phi_arr):
    """
    The ratio test: we need (D+B+C)/A > 1, not B+C > 0.

    D/A ~ 1 + O(1/p), so we only need (B+C)/A > -O(1/p).
    Since A ~ N^2 * something, B+C > -O(p) suffices.

    This is MUCH weaker than B+C > 0.
    """
    N = p - 1
    n = data['n']
    n_prime = n + (p - 1)

    # Compute A, D directly
    B_raw = data['B_raw']
    C_raw = data['C_raw']
    old_D_sq = data['old_D_sq']

    # A = old_D_sq * n'^2 / n^2 (dilution term)
    # Actually A = (n'/n)^2 * old_D_sq - old_D_sq = old_D_sq * [(n'^2 - n^2)/n^2]
    # = old_D_sq * [(n' - n)(n' + n)] / n^2

    # Wait: W_old = old_D_sq / n^2.  The dilution gives new wobble if fractions unchanged:
    # W_diluted = old_D_sq / n'^2.
    # So A = W_old - W_diluted = old_D_sq * (1/n^2 - 1/n'^2) = old_D_sq * (n'^2 - n^2) / (n^2 * n'^2)
    # Then DeltaW = (A - B - C - D) / n'^2 ... hmm, let me re-derive.

    # From the framework:
    # W_new = Sum D_new^2 / n'^2
    # W_old = Sum D_old^2 / n^2 = old_D_sq / n^2
    #
    # DeltaW = W_old - W_new
    #
    # The decomposition is:
    # n'^2 * W_new = Sum_{old f} D_new(f)^2 + Sum_{new f} D_new(f)^2
    #             = Sum_{old f} (D_old(f) + delta(f))^2 + D_riemann
    #             = old_D_sq + 2*Sum D*delta + Sum delta^2 + D_riemann
    #             = old_D_sq + B_raw + C_raw + D_riemann
    # where D_riemann = Sum_{k=1}^{p-1} D_old(k/p)^2 (approximately)

    # W_new = (old_D_sq + B_raw + C_raw + D_riemann) / n'^2
    # W_old = old_D_sq / n^2
    #
    # DeltaW = old_D_sq / n^2 - (old_D_sq + B_raw + C_raw + D_riemann) / n'^2
    #        = [old_D_sq * n'^2 - n^2 * (old_D_sq + B_raw + C_raw + D_riemann)] / (n^2 * n'^2)
    #        = [old_D_sq * (n'^2 - n^2) - n^2 * (B_raw + C_raw + D_riemann)] / (n^2 * n'^2)

    # So DeltaW < 0 iff old_D_sq * (n'^2 - n^2) < n^2 * (B_raw + C_raw + D_riemann)
    # i.e., B_raw + C_raw + D_riemann > old_D_sq * (n'^2 - n^2) / n^2 = A_dilution

    A_dilution = old_D_sq * (n_prime**2 - n**2) / (n**2)

    # Compute D_riemann = Sum_{k=1}^{p-1} D_old(k/p)^2
    fracs = farey_sequence(N)
    assert len(fracs) == n

    D_riemann = 0.0
    for k in range(1, p):
        x = k / p
        # Count fractions <= x
        # Binary search in sorted fracs
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if fracs[mid][0] / fracs[mid][1] <= x:
                lo = mid + 1
            else:
                hi = mid - 1
        count = lo  # number of fracs <= x
        D_val = count - n * x
        D_riemann += D_val * D_val

    # The sufficient condition for DeltaW < 0:
    # B_raw + C_raw + D_riemann > A_dilution

    lhs = B_raw + C_raw + D_riemann
    rhs = A_dilution

    # How much slack do we have?
    slack = lhs - rhs

    # The "needed" bound on B+C:
    # B+C > A_dilution - D_riemann
    threshold = A_dilution - D_riemann
    actual_BC = B_raw + C_raw

    # Ratio D_riemann / A_dilution (should be close to 1 for large p)
    DA_ratio = D_riemann / A_dilution if A_dilution > 0 else 0

    # The weaker condition: B+C > threshold = A_dilution - D_riemann
    # Compare threshold to delta_sq and to 0

    return {
        'A_dilution': A_dilution,
        'D_riemann': D_riemann,
        'B_plus_C': actual_BC,
        'DA_ratio': DA_ratio,
        'threshold': threshold,
        'actual_minus_threshold': actual_BC - threshold,
        'slack_over_dsq': (actual_BC - threshold) / data['C_raw'] if data['C_raw'] > 0 else 0,
        'threshold_over_dsq': threshold / data['C_raw'] if data['C_raw'] > 0 else 0,
        'threshold_sign': 'NEGATIVE (easy!)' if threshold < 0 else 'POSITIVE (need B+C > 0+)',
    }


# ==============================================================================
# MAIN: Run all four approaches
# ==============================================================================

def main():
    MAX_P = 500
    if len(sys.argv) > 1:
        MAX_P = int(sys.argv[1])

    print(f"ALTERNATIVE PROOF APPROACHES — Numerical Experiments up to p={MAX_P}")
    print("=" * 80)

    phi_arr = euler_totient_sieve(MAX_P + 10)
    primes = prime_list(MAX_P)

    # Filter to primes >= 11
    test_primes = [p for p in primes if p >= 11]

    # ======================================================================
    # APPROACH 1: Good denominators
    # ======================================================================
    print(f"\n{'='*80}")
    print("APPROACH 1: T_b analysis — Good denominators (b | p^2-1)")
    print(f"{'='*80}\n")

    a1_results = []
    for p in test_primes:
        data = analyze_prime_full(p, phi_arr)
        r1 = approach1_good_denominators(p, data)
        a1_results.append(r1)

        if p <= 101 or p in [197, 199, 211, 499, 503]:
            print(f"p={p:4d}: good_frac={r1['good_fraction']:.4f}, "
                  f"bad_frac={r1['bad_fraction']:.4f}, "
                  f"n_good={r1['n_good']:3d}/{r1['total_denoms']:3d} "
                  f"(zero={r1['n_zero']:2d}, invol={r1['n_involution']:2d}), "
                  f"bad_B+C={r1['bad_2Ddelta_plus_dsq']:.2f}")

    # Summary statistics
    good_fracs = [r['good_fraction'] for r in a1_results]
    print(f"\nSummary (Approach 1):")
    print(f"  Good fraction of delta_sq: min={min(good_fracs):.4f}, "
          f"max={max(good_fracs):.4f}, mean={sum(good_fracs)/len(good_fracs):.4f}")
    print(f"  Interpretation: {sum(1 for g in good_fracs if g > 0.5)}/{len(good_fracs)} "
          f"primes have >50% of delta_sq from good denominators")

    # ======================================================================
    # APPROACH 2: Variance / concentration
    # ======================================================================
    print(f"\n{'='*80}")
    print("APPROACH 2: Probabilistic concentration (random permutation model)")
    print(f"{'='*80}\n")

    a2_results = []
    for p in test_primes:
        data = analyze_prime_full(p, phi_arr)
        r2 = approach2_variance(p, data, phi_arr)
        a2_results.append(r2)

        if p <= 101 or p in [197, 199, 211, 499, 503]:
            print(f"p={p:4d}: E[B_raw]={r2['E_B_raw']:10.2f}, "
                  f"std={r2['std_B_raw']:8.2f}, "
                  f"SNR={r2['SNR']:6.2f}, "
                  f"actual={r2['actual_B_raw']:10.2f}, "
                  f"Cheby_P(neg)<={r2['chebyshev_P_neg']:.4f}")

    snrs = [r['SNR'] for r in a2_results if r['SNR'] < float('inf')]
    cheby = [r['chebyshev_P_neg'] for r in a2_results if r['chebyshev_P_neg'] < float('inf')]
    print(f"\nSummary (Approach 2):")
    print(f"  SNR: min={min(snrs):.4f}, max={max(snrs):.4f}, mean={sum(snrs)/len(snrs):.4f}")
    print(f"  Chebyshev P(B_raw<0): max={max(cheby):.4f}")
    print(f"  All E[B_raw]>0: {all(r['E_B_raw'] > 0 for r in a2_results)}")

    # ======================================================================
    # APPROACH 3: Fourier modes (h>=2 tail bound)
    # ======================================================================
    print(f"\n{'='*80}")
    print("APPROACH 3: Fourier mode decomposition — bounding h>=2 tail")
    print(f"{'='*80}\n")

    # This is slower, so only do a subset
    fourier_primes = [p for p in test_primes if p <= 200]
    a3_results = []
    for p in fourier_primes:
        r3 = approach3_fourier_modes(p, phi_arr)
        a3_results.append(r3)

        if p <= 101:
            print(f"p={p:4d}: B|_h1={r3['B_raw_h1']:10.2f}, "
                  f"Sum_h>=2={r3['sum_h_geq_2']:10.2f}, "
                  f"|tail/h1|={r3['ratio_tail_to_h1']:.4f}, "
                  f"M(N)={r3['M_N']:3d}, "
                  f"h1/dsq={r3['ratio_h1_to_dsq']:.3f}")
            # Print first 5 modes
            for m in r3['modes'][:5]:
                print(f"    h={m['h']:2d}: S_N={m['S_N_h']:6d}, C_h={m['C_h_p']:10.2f}, "
                      f"B|_h={m['B_raw_h']:10.2f}")

    tail_ratios = [r['ratio_tail_to_h1'] for r in a3_results]
    print(f"\nSummary (Approach 3):")
    print(f"  |tail|/|h=1|: min={min(tail_ratios):.4f}, max={max(tail_ratios):.4f}")
    print(f"  All |tail| < |h=1|: {all(t < 1.0 for t in tail_ratios)}")
    print(f"  h1/delta_sq ratios: min={min(r['ratio_h1_to_dsq'] for r in a3_results):.3f}, "
          f"max={max(r['ratio_h1_to_dsq'] for r in a3_results):.3f}")

    # ======================================================================
    # APPROACH 4: Ratio test
    # ======================================================================
    print(f"\n{'='*80}")
    print("APPROACH 4: Ratio test — weaker sufficient condition")
    print(f"{'='*80}\n")

    a4_results = []
    for p in test_primes:
        data = analyze_prime_full(p, phi_arr)
        r4 = approach4_ratio_test(p, data, phi_arr)
        a4_results.append(r4)

        if p <= 101 or p in [197, 199, 211, 499, 503]:
            print(f"p={p:4d}: D/A={r4['DA_ratio']:.6f}, "
                  f"threshold/dsq={r4['threshold_over_dsq']:+.4f}, "
                  f"slack/dsq={r4['slack_over_dsq']:+.4f}, "
                  f"{r4['threshold_sign']}")

    neg_threshold = sum(1 for r in a4_results if r['threshold'] < 0)
    print(f"\nSummary (Approach 4):")
    print(f"  Primes with threshold < 0 (trivially satisfied): {neg_threshold}/{len(a4_results)}")
    print(f"  D/A ratio: min={min(r['DA_ratio'] for r in a4_results):.6f}, "
          f"max={max(r['DA_ratio'] for r in a4_results):.6f}")
    print(f"  threshold/delta_sq: min={min(r['threshold_over_dsq'] for r in a4_results):.4f}, "
          f"max={max(r['threshold_over_dsq'] for r in a4_results):.4f}")
    print(f"  All slack > 0 (DeltaW < 0): {all(r['actual_minus_threshold'] > 0 for r in a4_results)}")

    print(f"\n{'='*80}")
    print(f"Total time: {elapsed():.1f}s")
    print(f"{'='*80}")

    return a1_results, a2_results, a3_results, a4_results


if __name__ == '__main__':
    main()
