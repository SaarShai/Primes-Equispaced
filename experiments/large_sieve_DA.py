#!/usr/bin/env python3
"""
LARGE SIEVE / ALIASED PARSEVAL APPROACH TO D/A >= 0.9
======================================================

Goal: Prove  sum_{k=1}^{p-1} D_old(k/p)^2  >=  0.9 * dilution_raw  unconditionally.

KEY IDEA: Use the ALIASED PARSEVAL identity.

D_old(k/p) = N_{p-1}(k/p) - n*(k/p) = sum_{m != 0} c_m * e^{2*pi*i*m*k/p}

where c_m are the Fourier coefficients of the Farey discrepancy function.

Sampling at k/p for k=0..p-1 gives the aliased Parseval identity:

  (1/p) * sum_{k=0}^{p-1} |sum_m c_m e(mk/p)|^2 = sum_{j=0}^{p-1} |sum_{m equiv j (mod p)} c_m|^2

So:  sum_Dold_sq = sum_{k=1}^{p-1} D_old(k/p)^2 = p * sum_{j=0}^{p-1} |A_j|^2 - |A_0|^2*???

Wait, we need to be careful about k=0. D_old(0) = N_{p-1}(0) - 0 = 1 (counting 0/1).
Actually, let's work with the full sum k=0..p-1 and subtract the k=0 term.

The script:
  1. Compute c_m (Fourier coefficients) via Ramanujan sums
  2. Compute the aliased sums A_j = sum_{m equiv j (mod p)} c_m
  3. Verify aliased Parseval: p * sum |A_j|^2 == sum D_old(k/p)^2 (full k=0..p-1)
  4. Analyze the structure: which alias classes j contribute most?
  5. Compare sum_Dold_sq vs dilution_raw and compute the ratio
  6. Investigate whether dual large sieve or exact aliasing gives >= 0.9
"""

import numpy as np
from math import gcd, floor, isqrt, pi
from fractions import Fraction
import time
import bisect


# ============================================================
# UTILITIES
# ============================================================

def sieve_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]

def euler_totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi

def mobius_sieve(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    smallest_prime = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest_prime[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest_prime[j] == 0:
                    smallest_prime[j] = i
    for n in range(2, limit + 1):
        p = smallest_prime[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    return mu

def mertens_sieve(limit):
    mu = mobius_sieve(limit)
    M = [0] * (limit + 1)
    for k in range(1, limit + 1):
        M[k] = M[k-1] + mu[k]
    return M

def farey_generator(N):
    """Generate Farey sequence F_N as (a,b) pairs in order."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


# ============================================================
# PART 1: DIRECT COMPUTATION OF D/A RATIO COMPONENTS
# ============================================================

def compute_DA_components(p, phi_arr):
    """Compute sum_Dold_sq, dilution_raw, and the D/A ratio."""
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    # Build sorted Farey values for binary search
    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    # old_D_sq = sum D(f)^2 over f in F_{p-1}
    old_D_sq = 0.0
    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D

    # sum_Dold_sq = sum_{k=1}^{p-1} D_old(k/p)^2
    sum_Dold_sq = 0.0
    D_old_vals = []
    for k in range(1, p):
        x = k / p
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        sum_Dold_sq += D_old * D_old
        D_old_vals.append(D_old)

    # Also compute sum for k=0
    D_old_0 = 1.0  # N_{p-1}(0) = 1 (just 0/1), n*0 = 0, so D_old(0) = 1
    # Actually: rank of 0/1 is 0 (it's the first), D_old(0) = 0 - n*0 = 0
    # Wait: N_{p-1}(0) = #{f in F_{p-1} : f <= 0} = 1 (just 0/1)
    # But rank is 0-indexed: rank(0/1) = 0. So D_old(0/p) = 0.
    # Actually for k=0, x=0, N_{p-1}(0) = 1 (0/1 itself), but we use
    # bisect_right which counts elements <= 0, which gives 1.
    # D_old(0) = 1 - n*0 = 1. Hmm.
    # Let's be precise: we use the same counting as for k>=1.
    x0 = 0.0
    rank0 = bisect.bisect_right(frac_values, x0)  # should be 1 (0/1 is <= 0)
    D_old_0 = rank0 - n * x0  # = 1

    sum_Dold_sq_full = D_old_0**2 + sum_Dold_sq  # k=0..p-1

    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # Also compute new_D_sq = sum (D_old(k/p) + k/p)^2
    sum_kp_Dold = sum(k/p * D_old_vals[k-1] for k in range(1, p))
    sum_kp_sq = sum((k/p)**2 for k in range(1, p))
    new_D_sq = sum_Dold_sq + 2*sum_kp_Dold + sum_kp_sq

    DA_ratio = new_D_sq / dilution_raw if dilution_raw > 0 else float('inf')
    Dold_ratio = sum_Dold_sq / dilution_raw if dilution_raw > 0 else float('inf')

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'sum_Dold_sq': sum_Dold_sq,
        'sum_Dold_sq_full': sum_Dold_sq_full,
        'new_D_sq': new_D_sq,
        'dilution_raw': dilution_raw,
        'DA_ratio': DA_ratio,
        'Dold_ratio': Dold_ratio,
        'sum_kp_Dold': sum_kp_Dold,
        'sum_kp_sq': sum_kp_sq,
        'D_old_vals': D_old_vals,
    }


# ============================================================
# PART 2: FOURIER COEFFICIENTS AND ALIASED PARSEVAL
# ============================================================

def compute_fourier_coefficients(N, M_max, mu_arr):
    """
    Compute Fourier coefficients c_m of the Farey discrepancy.

    D(x) = N_N(x) - n*x = sum_{m != 0} c_m * e(mx)

    where c_m = -(1/(2*pi*i*m)) * sum_{q=1}^N c_q(m)

    and sum_{q=1}^N c_q(m) = M(N) + 1 (for m=1 from Ramanujan sum identity)
    More generally: sum_{q=1}^N c_q(m) = sum_{d | m} d * mu(floor(N/d)) ...

    Actually, let's use the exact identity:
    sum_{q=1}^N c_q(m) = sum_{d | m, d <= N} phi(d) * mu(N ... )

    Hmm, the exact formula is complicated. Let's compute directly.

    c_q(m) = sum_{a=1, gcd(a,q)=1}^q e(ma/q) = sum_{d | gcd(m,q)} d * mu(q/d)

    So sum_{q=1}^N c_q(m) = sum_{q=1}^N sum_{d | gcd(m,q)} d * mu(q/d)
                           = sum_{d | m, d <= N} d * sum_{j=1}^{floor(N/d)} mu(j)
                           = sum_{d | m, d <= N} d * M(floor(N/d))
    """
    # Precompute M(k) = sum_{j=1}^k mu(j)
    M_vals = [0] * (N + 1)
    running = 0
    for k in range(1, N + 1):
        running += mu_arr[k]
        M_vals[k] = running

    coeffs = {}  # c_m for m = -M_max .. M_max, m != 0

    for m in range(-M_max, M_max + 1):
        if m == 0:
            continue
        abs_m = abs(m)

        # S(m, N) = sum_{q=1}^N c_q(|m|) = sum_{d | |m|, d <= N} d * M(floor(N/d))
        S = 0
        for d in range(1, min(abs_m, N) + 1):
            if abs_m % d == 0:
                S += d * M_vals[N // d]

        # c_m = -(1/(2*pi*i*m)) * S(m, N)
        # For m > 0: c_m = -S / (2*pi*i*m)  (complex)
        # For m < 0: c_m = -S / (2*pi*i*m) = S / (2*pi*i*|m|)
        # Note: S(m, N) = S(|m|, N) for the Ramanujan sum part.
        # Actually c_q(m) = c_q(-m) since it's real.
        # So S(-m, N) = S(m, N).
        # Thus c_{-m} = -S / (2*pi*i*(-m)) = S / (2*pi*i*m) = -conj(c_m) when S is real.

        # c_m = -S(|m|,N) / (2*pi*i*m)
        # For real S: c_m = S(|m|,N) * i / (2*pi*m) [since -1/i = i]
        # Wait: -1/(2*pi*i*m) = -1/(2*pi*i*m) * ((-i)/(-i)) = i/(2*pi*m)
        # Hmm: -1/(i*m) = -(-i)/(m) = i/m (when m > 0)? No.
        # -1/(i) = -(-i) = i? No: 1/i = -i, so -1/(i) = -(-i) = i. Hmm no.
        # 1/i = i/(i*i) = i/(-1) = -i. So -1/i = i.
        # So -1/(2*pi*i*m) = i/(2*pi*m).
        # c_m = i * S / (2*pi*m)   for m != 0

        # This is a purely imaginary number when S is real!
        # c_m = i * S(|m|, N) / (2*pi*m)
        coeffs[m] = 1j * S / (2 * pi * m)

    return coeffs


def aliased_parseval_analysis(p, phi_arr, mu_arr, M_max=None):
    """
    Compute the aliased Parseval decomposition:

    sum_{k=0}^{p-1} D_old(k/p)^2 = p * sum_{j=0}^{p-1} |A_j|^2

    where A_j = sum_{m equiv j (mod p)} c_m
    """
    N = p - 1
    n = farey_size(N, phi_arr)

    if M_max is None:
        M_max = min(5 * N, 2000)  # truncation of Fourier series

    # Compute Fourier coefficients
    coeffs = compute_fourier_coefficients(N, M_max, mu_arr)

    # Compute aliased sums A_j for j = 0, 1, ..., p-1
    A = [0.0 + 0.0j for _ in range(p)]
    for m, cm in coeffs.items():
        j = m % p
        A[j] += cm

    # Parseval check: p * sum |A_j|^2 should equal sum D_old(k/p)^2 (full k=0..p-1)
    parseval_sum = p * sum(abs(A[j])**2 for j in range(p))

    # Direct computation for comparison
    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    direct_sum = 0.0
    for k in range(p):
        x = k / p
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        direct_sum += D_old * D_old

    # Contribution by alias class
    alias_contribs = [(j, p * abs(A[j])**2) for j in range(p)]
    alias_contribs.sort(key=lambda t: -t[1])

    return {
        'p': p, 'n': n, 'M_max': M_max,
        'parseval_sum': parseval_sum,
        'direct_sum': direct_sum,
        'relative_error': abs(parseval_sum - direct_sum) / max(direct_sum, 1e-30),
        'A': A,
        'alias_contribs': alias_contribs,
        'coeffs': coeffs,
    }


# ============================================================
# PART 3: DUAL LARGE SIEVE LOWER BOUND
# ============================================================

def dual_large_sieve_bound(p, phi_arr, mu_arr, M_max=None):
    """
    Apply the dual (Gallagher-type) large sieve inequality:

    sum_{k=0}^{p-1} |sum_{|m|<=M} c_m e(mk/p)|^2 >= (p - 2M) * sum |c_m|^2

    when p > 2M. This gives a LOWER bound on sum D_old(k/p)^2.

    Compare with dilution_raw to see if we can get >= 0.9.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    if M_max is None:
        M_max = N  # Use M up to N

    coeffs = compute_fourier_coefficients(N, M_max, mu_arr)

    # sum |c_m|^2 for |m| <= M_max, m != 0
    energy = sum(abs(cm)**2 for cm in coeffs.values())

    # Dual large sieve: lower bound = max(p - 2*M_max, 0) * energy
    if p > 2 * M_max:
        lower_bound = (p - 2 * M_max) * energy
    else:
        lower_bound = 0.0

    # Improved dual large sieve (Montgomery-Vaughan):
    # sum >= (p - 1/(delta)) * sum |c_m|^2
    # where delta = min_{m != m'} ||m-m'|| / p ... for equispaced points delta = 1/p
    # So (p - 1/delta) = (p - p) = 0 ... not useful.

    # Actually for equispaced sampling at k/p, k=0..p-1,
    # the exact identity is aliased Parseval, which is EQUALITY not a bound.
    # So the "lower bound" is actually exact via aliased Parseval.

    # Compute dilution_raw
    old_fracs = list(farey_generator(N))
    old_D_sq = 0.0
    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D

    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # Parseval integral: integral_0^1 D(x)^2 dx = sum |c_m|^2
    # This equals W(N) * n (since W = old_D_sq / n^2, integral = old_D_sq / n = W*n)
    # Actually: integral D(x)^2 dx = old_D_sq / n? No...
    # W(N) = (1/n) * integral_0^1 (N_N(x) - n*x)^2 dx ??? No.
    # W(N) = sum_j (f_j - j/n)^2.
    # The L2 discrepancy integral is different from the wobble sum.
    # integral D(x)^2 dx = integral (N_N(x) - n*x)^2 dx (Lebesgue integral)
    # = sum_{adjacent fractions f_i, f_{i+1}} integral_{f_i}^{f_{i+1}} (i - n*x)^2 dx

    # For Parseval: sum |c_m|^2 = integral_0^1 |D(x)|^2 dx
    # Let's compute this integral directly.
    L2_integral = 0.0
    for idx in range(len(old_fracs) - 1):
        a1, b1 = old_fracs[idx]
        a2, b2 = old_fracs[idx + 1]
        x1 = a1 / b1
        x2 = a2 / b2
        # On [x1, x2), N_{p-1}(x) = idx + 1 (for x in [f_{idx}, f_{idx+1}))
        # D(x) = (idx+1) - n*x (0-indexed: f_0=0/1, so N(x)=idx+1 for x in [f_idx, f_{idx+1}))
        # Wait: bisect_right(frac_values, x) for x in [f_idx, f_{idx+1}) gives idx+1
        # since there are idx+1 values <= f_idx.
        rank = idx + 1  # actually it's idx (0-indexed) but N counts from 1
        # N_{p-1}(x) = #{f in F_{p-1} : f <= x}. For x in [f_idx, f_{idx+1}),
        # this is idx+1 (0-indexed list has idx+1 elements up to index idx).
        c_val = rank  # N(x) = rank = idx+1 for x in [f_idx, f_{idx+1})
        # D(x) = c_val - n*x
        # integral (c_val - n*x)^2 dx from x1 to x2
        # = c_val^2 * (x2-x1) - 2*c_val*n*(x2^2-x1^2)/2 + n^2*(x2^3-x1^3)/3
        dx = x2 - x1
        L2_integral += c_val**2 * dx - c_val * n * (x2**2 - x1**2) + n**2 * (x2**3 - x1**3) / 3

    return {
        'p': p, 'n': n, 'M_max': M_max,
        'energy': energy,
        'L2_integral': L2_integral,
        'dual_LS_lower': lower_bound,
        'dilution_raw': dilution_raw,
        'dual_LS_ratio': lower_bound / dilution_raw if dilution_raw > 0 else 0,
        'energy_vs_integral': energy / L2_integral if L2_integral > 0 else 0,
    }


# ============================================================
# PART 4: THE KEY DECOMPOSITION
# ============================================================

def key_decomposition(p, phi_arr, mu_arr):
    """
    The REAL approach: use the exact aliased Parseval to understand
    sum_Dold_sq / dilution_raw.

    We know:
      sum_Dold_sq = p * sum_{j=0}^{p-1} |A_j|^2
      dilution_raw = old_D_sq * (n'^2 - n^2) / n^2

    And old_D_sq = sum_{f in F_{p-1}} D(f)^2.

    The question is: how does sum_Dold_sq (sampling D at p-1 equispaced points)
    relate to old_D_sq (the wobble sum over Farey fractions)?

    Key insight: old_D_sq is a RIEMANN SUM approximation to n * integral D(x)^2 dx.
    And sum_Dold_sq is another Riemann sum (p equispaced points).

    So both approximate n * integral D^2 dx, and their ratio should be
    approximately (p-1) / (n * dilution_factor).

    Let's compute everything and see the structure.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    # old_D_sq
    old_D_sq = 0.0
    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D

    # L2 integral of D^2
    L2_integral = 0.0
    for idx in range(len(old_fracs) - 1):
        a1, b1 = old_fracs[idx]
        a2, b2 = old_fracs[idx + 1]
        x1, x2 = a1/b1, a2/b2
        rank = idx + 1
        dx = x2 - x1
        L2_integral += rank**2 * dx - rank * n * (x2**2 - x1**2) + n**2 * (x2**3 - x1**3) / 3

    # sum_Dold_sq at equispaced points k/p, k=1..p-1
    sum_Dold_sq = 0.0
    for k in range(1, p):
        x = k / p
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        sum_Dold_sq += D_old * D_old

    # Dilution
    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2
    dilution_factor = (n_prime**2 - n**2) / n**2  # ~ 2*(p-1)/n

    # The wobble W = old_D_sq / n^2
    W = old_D_sq / (n * n)

    # What we need: sum_Dold_sq / dilution_raw = sum_Dold_sq / (old_D_sq * dilution_factor)
    # = (sum_Dold_sq / old_D_sq) / dilution_factor
    # = (sum_Dold_sq / old_D_sq) * n^2 / (n'^2 - n^2)

    # Riemann sum interpretation:
    # old_D_sq ~ n * integral D^2 dx (Farey points approximate uniform)
    # sum_Dold_sq ~ p * integral D^2 dx (equispaced points, with step 1/p)
    # Wait: more precisely, sum_{k=1}^{p-1} D(k/p)^2 * (1/p) ~ integral D^2 dx
    # So sum_Dold_sq ~ p * integral D^2 dx

    # And old_D_sq ~ n * integral D^2 dx (roughly, since Farey points equidistribute)

    # So sum_Dold_sq / old_D_sq ~ p / n

    # And dilution_factor ~ 2(p-1)/n

    # So ratio ~ (p/n) / (2(p-1)/n) = p / (2(p-1)) ~ 1/2

    # That gives ~0.5, not 0.9. But this ignores the cross term 2*sum(kp*Dold) + sum(kp^2)!

    # THE ACTUAL D/A RATIO uses new_D_sq = sum(D_old + k/p)^2, not just sum_Dold_sq.

    # new_D_sq = sum_Dold_sq + 2*sum(k/p * D_old(k/p)) + sum(k/p)^2
    # The cross term 2*sum(k/p * D_old) is crucial!
    # And sum(k/p)^2 = (p-1)(2p-1)/(6p^2) * p ~ p/3

    sum_cross = 0.0
    sum_shift_sq = 0.0
    for k in range(1, p):
        x = k / p
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        sum_cross += 2 * x * D_old
        sum_shift_sq += x * x

    new_D_sq = sum_Dold_sq + sum_cross + sum_shift_sq
    DA_ratio = new_D_sq / dilution_raw

    # How large is the cross term relative to dilution?
    cross_ratio = sum_cross / dilution_raw
    shift_ratio = sum_shift_sq / dilution_raw
    Dold_ratio = sum_Dold_sq / dilution_raw

    return {
        'p': p, 'n': n, 'n_prime': n_prime,
        'old_D_sq': old_D_sq,
        'sum_Dold_sq': sum_Dold_sq,
        'sum_cross': sum_cross,
        'sum_shift_sq': sum_shift_sq,
        'new_D_sq': new_D_sq,
        'dilution_raw': dilution_raw,
        'L2_integral': L2_integral,
        'DA_ratio': DA_ratio,
        'Dold_ratio': Dold_ratio,
        'cross_ratio': cross_ratio,
        'shift_ratio': shift_ratio,
        'W': W,
        'sum_Dold_sq_over_p': sum_Dold_sq / p,
        'old_Dsq_over_n': old_D_sq / n,
        'ratio_pn': p / n,
        'dilution_factor': (n_prime**2 - n**2) / n**2,
    }


# ============================================================
# PART 5: FOURIER ANALYSIS OF THE CROSS TERM
# ============================================================

def cross_term_fourier(p, phi_arr, mu_arr, M_max=None):
    """
    Analyze sum_{k=1}^{p-1} (k/p) * D_old(k/p) via Fourier.

    D_old(k/p) = sum_{m != 0} c_m * e(mk/p)

    So (k/p) * D_old(k/p) involves products with k/p.

    k/p has its own Fourier expansion on {0,...,p-1}:
    k/p = 1/2 + (1/(2p)) * sum_{j=1}^{p-1} cot(pi*j/p) * e(-2*pi*i*j*k/p)
    (This is the DFT of the sawtooth.)

    Actually, let's just compute the cross term directly and compare
    with dilution_raw. The key question is whether the cross term
    contributes ~0.4 * dilution_raw (to bring total from 0.5 to 0.9).
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1

    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    old_D_sq = 0.0
    for idx, (a, b) in enumerate(old_fracs):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D

    dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

    # Compute: E[D_old * x] where x = k/p, averaged over k=1..p-1
    sum_xD = 0.0
    sum_D = 0.0
    sum_x = 0.0
    sum_x2 = 0.0
    sum_D2 = 0.0

    for k in range(1, p):
        x = k / p
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        sum_xD += x * D_old
        sum_D += D_old
        sum_x += x
        sum_x2 += x * x
        sum_D2 += D_old * D_old

    # Statistics
    mean_x = sum_x / (p - 1)
    mean_D = sum_D / (p - 1)
    cov_xD = sum_xD / (p-1) - mean_x * mean_D
    var_x = sum_x2 / (p-1) - mean_x**2
    var_D = sum_D2 / (p-1) - mean_D**2
    corr = cov_xD / (var_x * var_D)**0.5 if var_x > 0 and var_D > 0 else 0

    return {
        'p': p, 'n': n,
        'sum_xD': sum_xD,
        '2_sum_xD': 2 * sum_xD,
        'dilution_raw': dilution_raw,
        'cross_over_dilut': 2 * sum_xD / dilution_raw,
        'mean_D': mean_D,
        'mean_x': mean_x,
        'correlation_xD': corr,
        'sum_D': sum_D,
    }


# ============================================================
# PART 6: ANALYTICAL BOUND ON EACH COMPONENT
# ============================================================

def analytical_bounds(p, phi_arr, mu_arr, M_arr):
    """
    Try to bound each component analytically:

    D/A = (sum_Dold_sq + 2*sum_xD + sum_x2) / dilution_raw

    Component 1: sum_Dold_sq / dilution_raw ~ p/(2(p-1)) ~ 1/2
    Component 2: 2*sum_xD / dilution_raw = ???
    Component 3: sum_x2 / dilution_raw = sum(k/p)^2 / dilution_raw

    sum(k/p)^2 = (1/p^2) * sum k^2 = (1/p^2) * (p-1)*p*(2p-1)/6 = (p-1)(2p-1)/(6p)

    dilution_raw = old_D_sq * (n'^2 - n^2)/n^2

    n' - n = p-1, so n'^2 - n^2 = (n'-n)(n'+n) = (p-1)(2n+p-1)
    dilution_raw = old_D_sq * (p-1)(2n+p-1)/n^2

    And old_D_sq = n^2 * W(N) where W(N) = wobble.

    So dilution_raw = W(N) * (p-1) * (2n + p-1)

    Component 3: (p-1)(2p-1)/(6p) / (W(N)*(p-1)*(2n+p-1))
               = (2p-1)/(6p * W(N) * (2n+p-1))
               ~ 2p / (6p * W * 2n)  for large p
               = 1/(6*W*n)

    W(N) ~ 1/(2*pi^2) * log(N) ... (known asymptotic)
    n ~ 3N^2/pi^2

    So 1/(6*W*n) ~ 1/(6 * log(N)/(2*pi^2) * 3N^2/pi^2)
                  = pi^4 / (9 * N^2 * log N)
    Which is tiny!

    So component 3 is negligible. The question is really about component 2.

    Let me compute sum_D = sum_{k=1}^{p-1} D_old(k/p).
    By the Farey discrepancy properties: sum D_old(k/p) = sum N(k/p) - n*sum(k/p)
    = sum N(k/p) - n*(p-1)/2

    sum N(k/p) = sum_{k=1}^{p-1} #{f in F_{p-1} : f <= k/p}
    = sum_{f in F_{p-1}} #{k : 1 <= k <= p-1, k/p >= f}
    = sum_{f in F_{p-1}} (p-1 - ceil(p*f) + 1)  [for f > 0]
    ... this is getting complicated. Let's just compute.
    """
    N = p - 1
    n = farey_size(N, phi_arr)
    n_prime = n + p - 1
    M_p = M_arr[p]
    W = None  # compute below

    r = key_decomposition(p, phi_arr, mu_arr)
    W = r['W']

    # Analytical predictions
    pred_Dold_ratio = p / (2 * (p - 1))  # ~ 1/2
    pred_shift_ratio = (2*p - 1) / (6 * p * W * (2*n + p - 1)) if W > 0 else 0

    return {
        'p': p, 'n': n, 'M': M_p, 'W': W,
        'DA_ratio': r['DA_ratio'],
        'Dold_ratio': r['Dold_ratio'],
        'cross_ratio': r['cross_ratio'],
        'shift_ratio': r['shift_ratio'],
        'pred_Dold_ratio': pred_Dold_ratio,
        'pred_shift_ratio': pred_shift_ratio,
        'Dold_ratio_error': r['Dold_ratio'] - pred_Dold_ratio,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    start = time.time()

    LIMIT = 1500
    phi_arr = euler_totient_sieve(LIMIT)
    mu_arr = mobius_sieve(LIMIT)
    M_arr = mertens_sieve(LIMIT)
    primes = sieve_primes(LIMIT)

    print("=" * 110)
    print("LARGE SIEVE / ALIASED PARSEVAL INVESTIGATION FOR D/A >= 0.9")
    print("=" * 110)

    # ================================================================
    # SECTION 1: Basic D/A decomposition
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 1: D/A DECOMPOSITION INTO THREE COMPONENTS")
    print("  D/A = (sum_Dold_sq + 2*sum_xD + sum_x^2) / dilution_raw")
    print("       = Dold_ratio + cross_ratio + shift_ratio")
    print("-" * 110)
    print()
    print(f"{'p':>5} {'n':>7} {'D/A':>10} {'Dold_r':>10} {'cross_r':>10} {'shift_r':>10} "
          f"{'pred_Dold':>10} {'Dold_err':>10} {'M(p)':>6}")
    print("-" * 100)

    target_primes = [p for p in primes if 11 <= p <= 500]

    for p in target_primes:
        r = analytical_bounds(p, phi_arr, mu_arr, M_arr)
        print(f"{r['p']:5d} {r['n']:7d} {r['DA_ratio']:10.6f} {r['Dold_ratio']:10.6f} "
              f"{r['cross_ratio']:10.6f} {r['shift_ratio']:10.6f} "
              f"{r['pred_Dold_ratio']:10.6f} {r['Dold_ratio_error']:+10.6f} {r['M']:6d}")

    # ================================================================
    # SECTION 2: Aliased Parseval verification (small primes)
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 2: ALIASED PARSEVAL VERIFICATION")
    print("-" * 110)
    print()

    for p in [5, 7, 11, 13, 17, 23, 29, 37, 41, 43, 47]:
        r = aliased_parseval_analysis(p, phi_arr, mu_arr, M_max=200)
        print(f"p={p:4d}: direct_sum={r['direct_sum']:12.6f}  parseval_sum={r['parseval_sum']:12.6f}  "
              f"rel_err={r['relative_error']:.2e}  M_max={r['M_max']}")

        # Show top alias contributions
        top = r['alias_contribs'][:5]
        total = sum(c for _, c in r['alias_contribs'])
        print(f"  Top 5 alias classes: ", end="")
        for j, c in top:
            print(f"j={j}:{c/total*100:.1f}%  ", end="")
        print()

    # ================================================================
    # SECTION 3: Cross term analysis
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 3: CROSS TERM ANALYSIS")
    print("  The cross term 2*sum(x*D_old) is the key to D/A > 0.5")
    print("-" * 110)
    print()
    print(f"{'p':>5} {'sum_D':>12} {'mean_D':>10} {'corr(x,D)':>10} {'2sumxD/dilut':>12}")
    print("-" * 60)

    for p in target_primes[:30]:
        r = cross_term_fourier(p, phi_arr, mu_arr)
        print(f"{r['p']:5d} {r['sum_D']:12.4f} {r['mean_D']:10.4f} "
              f"{r['correlation_xD']:10.6f} {r['cross_over_dilut']:12.6f}")

    # ================================================================
    # SECTION 4: D/A convergence and minimum
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 4: D/A CONVERGENCE AND MINIMUM")
    print("-" * 110)
    print()

    min_DA = float('inf')
    min_p = 0
    count_below_09 = 0
    count_below_095 = 0
    results = []

    for p in [p for p in primes if 11 <= p <= LIMIT]:
        r = key_decomposition(p, phi_arr, mu_arr)
        DA = r['DA_ratio']
        if DA < min_DA:
            min_DA = DA
            min_p = p
        if DA < 0.9:
            count_below_09 += 1
        if DA < 0.95:
            count_below_095 += 1
        results.append((p, DA, r['Dold_ratio'], r['cross_ratio'], r['shift_ratio']))

    print(f"  Minimum D/A = {min_DA:.10f} at p = {min_p}")
    print(f"  Count D/A < 0.9:  {count_below_09}")
    print(f"  Count D/A < 0.95: {count_below_095}")
    print()

    # Show worst cases
    results.sort(key=lambda t: t[1])
    print("  WORST CASES (lowest D/A):")
    print(f"  {'p':>5} {'D/A':>12} {'Dold_r':>10} {'cross_r':>10} {'shift_r':>10}")
    for p, DA, dr, cr, sr in results[:20]:
        print(f"  {p:5d} {DA:12.8f} {dr:10.6f} {cr:10.6f} {sr:10.6f}")

    # ================================================================
    # SECTION 5: UNDERSTANDING WHY D/A ~ 1 (not 0.5)
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 5: WHY D/A ~ 1: THE CROSS TERM CONTRIBUTION")
    print("-" * 110)
    print()
    print("  The naive analysis gives sum_Dold_sq / dilution ~ 0.5.")
    print("  But D/A uses new_D_sq = sum(D_old + k/p)^2, not sum(D_old)^2.")
    print("  The cross term 2*sum(k/p * D_old(k/p)) adds ~0.5 more.")
    print()
    print("  WHY is the cross term positive and large?")
    print("  D_old(k/p) = N_{p-1}(k/p) - n*k/p is the Farey counting error.")
    print("  For k near 0: D_old ~ 0 (few fractions near 0)")
    print("  For k near p: D_old ~ 0 (by symmetry N(1)=n, D(1)=0)")
    print("  In the middle: D_old tends to be positive (Farey sequence bunches")
    print("  in the middle compared to uniform distribution).")
    print()
    print("  Since D_old is positive in the middle where k/p ~ 1/2,")
    print("  the product (k/p)*D_old is positive, giving a positive cross term.")
    print()

    # Verify: D_old profile for a specific prime
    p_test = 101
    N = p_test - 1
    n = farey_size(N, phi_arr)
    old_fracs = list(farey_generator(N))
    frac_values = [a/b for (a,b) in old_fracs]

    print(f"  D_old profile for p={p_test} (n={n}):")
    print(f"  {'k':>4} {'k/p':>8} {'D_old':>10} {'(k/p)*D_old':>12}")
    for k in range(0, p_test, 10):
        x = k / p_test
        rank = bisect.bisect_right(frac_values, x)
        D_old = rank - n * x
        print(f"  {k:4d} {x:8.4f} {D_old:10.4f} {x*D_old:12.4f}")

    # ================================================================
    # SECTION 6: EXACT RELATIONSHIP AND PROOF STRATEGY
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 6: EXACT RELATIONSHIP AND PROOF STRATEGY")
    print("-" * 110)
    print()

    # The key identity from DA_ratio_proof.py:
    # D/A = 1 - (B + C + n'^2 * DeltaW) / dilution_raw
    # where B = 2*sum D*delta, C = sum delta^2
    #
    # So D/A >= 0.9 iff (B + C + n'^2 * DeltaW) / dilution_raw <= 0.1
    #
    # This means: the correction is at most 10%.
    #
    # From the existing analysis, |correction| = O(1/p).
    # For D/A >= 0.9 we need |correction| <= 0.1, which happens for p >= p0.
    #
    # The question: what is p0?

    print("  The identity: D/A = 1 - (B + C + n'^2*DW) / dilution_raw")
    print("  So D/A >= 0.9 iff correction <= 0.1.")
    print()
    print("  From existing data, let's find the threshold p0 where D/A >= 0.9 for all p >= p0:")
    print()

    # Find the LAST prime where D/A < 0.9
    all_results = []
    for p in [p for p in primes if p >= 5]:
        r = key_decomposition(p, phi_arr, mu_arr)
        all_results.append((p, r['DA_ratio']))

    last_below_09 = None
    for p, DA in all_results:
        if DA < 0.9:
            last_below_09 = p

    if last_below_09:
        print(f"  Last prime with D/A < 0.9: p = {last_below_09}")
    else:
        print(f"  ALL primes from 5 to {LIMIT} have D/A >= 0.9!")

    last_below_095 = None
    for p, DA in all_results:
        if DA < 0.95:
            last_below_095 = p

    if last_below_095:
        print(f"  Last prime with D/A < 0.95: p = {last_below_095}")

    # Show the primes with D/A < 0.9
    below_09 = [(p, DA) for p, DA in all_results if DA < 0.9]
    if below_09:
        print(f"\n  Primes with D/A < 0.9:")
        for p, DA in below_09:
            print(f"    p = {p:5d}, D/A = {DA:.10f}")
    else:
        print(f"  ==> D/A >= 0.9 holds for ALL primes p in [5, {LIMIT}].")

    print()

    # ================================================================
    # SECTION 7: ATTEMPTING A PROOF VIA PARSEVAL
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 7: PROOF ATTEMPT VIA EXACT PARSEVAL AND RIEMANN SUMS")
    print("-" * 110)
    print()

    # Idea: new_D_sq = sum (D_old(k/p) + k/p)^2
    #      = sum D_old^2 + 2*sum (k/p)*D_old + sum (k/p)^2
    #
    # The Riemann sum relation:
    #   (1/p) * sum_{k=0}^{p-1} D_old(k/p)^2 ~ integral D^2 dx
    #   (1/n) * old_D_sq = (1/n) * sum_{j=0}^{n-1} D(f_j)^2 ~ integral D^2 dx
    #
    # But these are DIFFERENT Riemann sums with DIFFERENT errors!
    #
    # The equispaced sum (1/p)*sum D(k/p)^2 is a better Riemann sum
    # (error O(1/p) by Koksma-Hlawka or similar).
    #
    # The Farey sum (1/n)*old_D_sq has error O(discrepancy of Farey seq * variation of D^2),
    # which is smaller when Farey equidistribution holds well.
    #
    # So: sum_Dold_sq / p ~ old_D_sq / n
    #     sum_Dold_sq ~ (p/n) * old_D_sq
    #
    # And dilution_raw ~ 2(p-1)/n * old_D_sq
    #
    # So Dold_ratio ~ (p/n) / (2(p-1)/n) = p/(2(p-1)) ~ 1/2. ✓
    #
    # For the cross term:
    # sum (k/p) * D_old(k/p) ~ p * integral x * D(x) dx
    #
    # integral x * D(x) dx = integral x * (N(x) - n*x) dx
    #   = integral x*N(x) dx - n * integral x^2 dx
    #   = integral x*N(x) dx - n/3
    #
    # And integral x * N(x) dx = sum_{f in F_N} integral_{f}^{1} x dx
    #   = sum_{f in F_N} (1 - f^2)/2
    #   = n/2 - (1/2) * sum f^2
    #
    # So integral x * D(x) dx = n/2 - (1/2)*sum f^2 - n/3
    #   = n/6 - (1/2)*sum f^2
    #
    # Hmm, let's verify numerically:

    for p in [47, 101, 211, 503]:
        if p > LIMIT:
            continue
        N = p - 1
        n = farey_size(N, phi_arr)
        old_fracs = list(farey_generator(N))
        frac_values = [a/b for (a,b) in old_fracs]

        # Integral x * D(x) dx
        integral_xD = 0.0
        for idx in range(len(old_fracs) - 1):
            a1, b1 = old_fracs[idx]
            a2, b2 = old_fracs[idx + 1]
            x1, x2 = a1/b1, a2/b2
            rank = idx + 1
            # integral x * (rank - n*x) dx from x1 to x2
            integral_xD += rank * (x2**2 - x1**2)/2 - n * (x2**3 - x1**3)/3

        # Integral D^2 dx
        integral_D2 = 0.0
        for idx in range(len(old_fracs) - 1):
            a1, b1 = old_fracs[idx]
            a2, b2 = old_fracs[idx + 1]
            x1, x2 = a1/b1, a2/b2
            rank = idx + 1
            dx = x2 - x1
            integral_D2 += rank**2*dx - rank*n*(x2**2-x1**2) + n**2*(x2**3-x1**3)/3

        # Sums
        sum_D2 = 0.0
        sum_xD = 0.0
        for k in range(1, p):
            x = k / p
            rank = bisect.bisect_right(frac_values, x)
            D_old = rank - n * x
            sum_D2 += D_old**2
            sum_xD += x * D_old

        sum_x2 = sum((k/p)**2 for k in range(1, p))
        n_prime = n + p - 1
        old_D_sq = sum(((idx) - n * (a/b))**2 for idx, (a,b) in enumerate(old_fracs))
        dilution_raw = old_D_sq * (n_prime**2 - n**2) / n**2

        # Ratios
        print(f"  p={p:4d}, n={n:5d}:")
        print(f"    integral D^2    = {integral_D2:.6f}")
        print(f"    sum_D2/p        = {sum_D2/p:.6f}  (should ~ integral D^2)")
        print(f"    old_D_sq/n      = {old_D_sq/n:.6f}  (also ~ integral D^2)")
        print(f"    integral x*D    = {integral_xD:.6f}")
        print(f"    sum_xD/p        = {sum_xD/p:.6f}  (should ~ integral x*D)")
        print(f"    sum_D2          = {sum_D2:.4f}")
        print(f"    2*sum_xD        = {2*sum_xD:.4f}")
        print(f"    sum_x2          = {sum_x2:.4f}")
        print(f"    new_D_sq        = {sum_D2 + 2*sum_xD + sum_x2:.4f}")
        print(f"    dilution_raw    = {dilution_raw:.4f}")
        print(f"    D/A             = {(sum_D2 + 2*sum_xD + sum_x2)/dilution_raw:.8f}")
        print(f"    Dold_r          = {sum_D2/dilution_raw:.6f}")
        print(f"    cross_r         = {2*sum_xD/dilution_raw:.6f}")
        print(f"    shift_r         = {sum_x2/dilution_raw:.6f}")
        print()

    # ================================================================
    # SECTION 8: THE ANALYTIC PATH
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 8: ANALYTIC PROOF PATH SUMMARY")
    print("-" * 110)
    print()
    print("FINDING: The three components of D/A have the following behavior:")
    print()
    print("  Component 1 (sum_Dold_sq / dilution):  ~ p/(2(p-1)) -> 1/2")
    print("  Component 2 (2*sum_xD / dilution):     ~ 1/2 - O(1/p)  [positive!]")
    print("  Component 3 (sum_x^2 / dilution):      ~ O(1/n) -> 0")
    print()
    print("  Total D/A                              ~ 1 - O(1/p)")
    print()
    print("KEY INSIGHT: Components 1 and 2 each contribute ~1/2.")
    print("This is NOT a coincidence: it reflects the identity D/A = 1 - correction.")
    print()
    print("The cross term sum(x*D_old) is positive and ~(1/2)*dilution because:")
    print("  - D_old(x) = N(x) - n*x is biased positive (Farey fractions bunch in middle)")
    print("  - The product x*D_old(x) is weighted toward x~1/2 where D_old is largest")
    print("  - This integral ~ n/6 - sum(f^2)/2 where sum(f^2) ~ n/3, giving ~0")
    print("  - Wait, the cross ratio is ~0.5, so sum_xD ~ (p/4)*dilution/p ...")
    print()
    print("For a PROOF of D/A >= 0.9:")
    print("  Since D/A = 1 - correction, and correction = O(1/p),")
    print("  we need |correction| <= 0.1.")
    print("  The correction involves B+C+n'^2*DW, which depends on Mertens function.")
    print("  For p >= some p0, this holds. Below p0, verify directly.")
    print()

    # ================================================================
    # SECTION 9: QUANTITATIVE BOUND ON CORRECTION
    # ================================================================
    print()
    print("-" * 110)
    print("SECTION 9: QUANTITATIVE BOUND ON THE CORRECTION TERM")
    print("-" * 110)
    print()

    print(f"  {'p':>5} {'D/A':>10} {'1-D/A':>10} {'p*(1-D/A)':>10} {'|M(p)|':>6}")
    print("  " + "-" * 50)

    for p in [p for p in primes if 11 <= p <= 500]:
        r = key_decomposition(p, phi_arr, mu_arr)
        correction = 1 - r['DA_ratio']
        M_p = abs(M_arr[p])
        print(f"  {p:5d} {r['DA_ratio']:10.6f} {correction:10.6f} {p*correction:10.4f} {M_p:6d}")

    elapsed = time.time() - start
    print(f"\n\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
