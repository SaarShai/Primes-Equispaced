#!/usr/bin/env python3
"""
Verify the spectral formula:
  delta_sq_b = (1 / (b^2 * phi(b))) * Sum_{chi != chi_0 mod b} |1 - chi_bar(p)|^2 * |S_1(chi)|^2

where S_1(chi) = Sum_{gcd(a,b)=1} a * chi(a)

Also verify the factorization: f_hat(chi) = (1 - chi_bar(p)) * S_1(chi)
"""

import numpy as np
from math import gcd

def euler_phi(n):
    return sum(1 for a in range(1, n+1) if gcd(a, n) == 1)

def get_characters(b):
    """Get all Dirichlet characters mod b (for prime b, these are powers of a primitive root)."""
    if b == 2:
        return [lambda a, b=b: 1 if gcd(a,b)==1 else 0]

    # Find a primitive root mod b
    for g in range(2, b):
        seen = set()
        val = 1
        for _ in range(b-1):
            seen.add(val)
            val = (val * g) % b
        if len(seen) == b-1:
            prim_root = g
            break

    # Build discrete log table
    dlog = {}
    val = 1
    for k in range(b-1):
        dlog[val] = k
        val = (val * prim_root) % b

    # Characters chi_j(a) = omega^(j * dlog(a)) where omega = e^(2pi i / (b-1))
    phi_b = b - 1  # for prime b
    omega = np.exp(2j * np.pi / phi_b)

    chars = []
    for j in range(phi_b):
        def chi(a, j=j, dlog=dlog, omega=omega, b=b, phi_b=phi_b):
            if gcd(a, b) != 1:
                return 0.0
            return omega ** (j * dlog[a % b])
        chars.append(chi)

    return chars

def delta_sq_direct(b, p):
    """Compute delta_sq_b directly: Sum_{gcd(a,b)=1} ((a - pa mod b) / b)^2"""
    total = 0.0
    for a in range(1, b):
        if gcd(a, b) == 1:
            sigma_p_a = (p * a) % b
            delta = (a - sigma_p_a) / b
            total += delta ** 2
    return total

def delta_sq_spectral(b, p):
    """Compute delta_sq_b via spectral formula:
    (1/(b^2 * phi(b))) * Sum_{chi != chi_0} |1 - chi_bar(p)|^2 * |S_1(chi)|^2
    """
    chars = get_characters(b)
    phi_b = euler_phi(b)

    total = 0.0
    for j, chi in enumerate(chars):
        if j == 0:  # skip trivial character
            continue

        # Compute S_1(chi) = Sum_{gcd(a,b)=1} a * chi(a)
        S1 = sum(a * chi(a) for a in range(1, b))

        # Compute chi_bar(p) = conjugate(chi(p))
        chi_bar_p = np.conj(chi(p))

        # Weight: |1 - chi_bar(p)|^2
        weight = abs(1 - chi_bar_p) ** 2

        total += weight * abs(S1) ** 2

    return total / (b**2 * phi_b)

def verify_fhat_factorization(b, p):
    """Verify f_hat(chi) = (1 - chi_bar(p)) * S_1(chi)

    where f(a) = a - (pa mod b) for gcd(a,b)=1
    """
    chars = get_characters(b)

    max_err = 0.0
    for j, chi in enumerate(chars):
        if j == 0:
            continue

        # Direct f_hat
        fhat_direct = sum((a - (p*a) % b) * chi(a) for a in range(1, b) if gcd(a,b)==1)

        # Factored form
        S1 = sum(a * chi(a) for a in range(1, b))
        chi_bar_p = np.conj(chi(p))
        fhat_factored = (1 - chi_bar_p) * S1

        err = abs(fhat_direct - fhat_factored)
        max_err = max(max_err, err)

    return max_err

def check_averages(b, p):
    """Check the average of |1-chi(p)|^2 and |S_1|^2 over non-trivial chi."""
    chars = get_characters(b)
    phi_b = euler_phi(b)

    weights = []
    S1_sq = []
    products = []

    for j, chi in enumerate(chars):
        if j == 0:
            continue
        w = abs(1 - np.conj(chi(p))) ** 2
        s = abs(sum(a * chi(a) for a in range(1, b))) ** 2
        weights.append(w)
        S1_sq.append(s)
        products.append(w * s)

    avg_w = np.mean(weights)
    avg_s = np.mean(S1_sq)
    avg_prod = np.mean(products)

    # Predicted averages
    pred_w = 2 * (b-1) / (b-2) if b > 2 else 2.0
    pred_s = b * (b-1)**2 / 12

    # Correlation
    corr = np.corrcoef(weights, S1_sq)[0, 1] if len(weights) > 2 else 0

    return avg_w, pred_w, avg_s, pred_s, avg_prod, avg_w * avg_s, corr

print("=" * 80)
print("VERIFICATION OF SPECTRAL FORMULA FOR delta_sq_b")
print("=" * 80)

print("\n--- Test 1: Direct vs Spectral delta_sq_b ---")
print(f"{'b':>5} {'p':>5} {'direct':>14} {'spectral':>14} {'ratio':>10} {'error':>12}")
for b in [3, 5, 7, 11, 13, 17, 19, 23]:
    for p in [11, 13, 17, 29, 37, 97]:
        if p == b or b >= p:
            continue
        d = delta_sq_direct(b, p)
        s = delta_sq_spectral(b, p)
        if d > 1e-15:
            ratio = s / d
            err = abs(s - d) / d
            print(f"{b:5d} {p:5d} {d:14.8f} {s:14.8f} {ratio:10.6f} {err:12.2e}")

print("\n--- Test 2: f_hat factorization verification ---")
print(f"{'b':>5} {'p':>5} {'max_error':>14}")
for b in [3, 5, 7, 11, 13, 17, 19, 23]:
    for p in [11, 13, 29, 97]:
        if p == b or b >= p:
            continue
        err = verify_fhat_factorization(b, p)
        print(f"{b:5d} {p:5d} {err:14.2e}")

print("\n--- Test 3: Average weight and S_1 predictions ---")
print(f"{'b':>5} {'p':>5} {'avg|1-chi|^2':>12} {'predicted':>10} {'avg|S1|^2':>14} {'predicted':>14} {'correlation':>12}")
for b in [5, 7, 11, 13, 17, 23, 29, 37]:
    p = 97
    if b >= p:
        continue
    if p % b == 1:  # skip b dividing p-1 (sigma_p = identity)
        continue
    aw, pw, as_, ps, ap, awas, corr = check_averages(b, p)
    print(f"{b:5d} {p:5d} {aw:12.4f} {pw:10.4f} {as_:14.2f} {ps:14.2f} {corr:12.4f}")

print("\n--- Test 4: Anti-correlation check ---")
print("Checking whether weight-S_1 anti-correlation explains the factor-of-2 gap")
print(f"{'b':>5} {'p':>5} {'delta_sq_b':>12} {'(avg_w*avg_S)/(b^2*phi)':>24} {'ratio':>8}")
for b in [5, 7, 11, 13, 17, 23, 29]:
    p = 97
    if b >= p or p % b == 1:
        continue
    d = delta_sq_direct(b, p)
    aw, pw, as_, ps, ap, awas, corr = check_averages(b, p)
    phi_b = b - 1  # prime b
    uncorr_pred = aw * as_ * (phi_b - 1) / (b**2 * phi_b)  # (b-2) terms, averaged
    actual_spectral = ap * (phi_b - 1) / (b**2 * phi_b)
    if uncorr_pred > 0:
        print(f"{b:5d} {p:5d} {d:12.6f} {uncorr_pred:24.6f} {d/uncorr_pred:8.4f}")

print("\n--- Test 5: Sum over denominators ---")
print("Verify total delta_sq = Sum_b delta_sq_b")
for p in [11, 17, 29, 37, 97]:
    total_direct = 0.0
    total_spectral = 0.0
    N = p - 1
    for b in range(2, N + 1):
        td = delta_sq_direct(b, p)
        total_direct += td
        # Only do spectral for prime b (general case needs more work)
        if all(b % k != 0 for k in range(2, int(b**0.5)+1)) and b > 1:
            ts = delta_sq_spectral(b, p)
            total_spectral += ts

    # Count prime-only contribution
    prime_total = sum(delta_sq_direct(b, p) for b in range(2, N+1)
                      if all(b % k != 0 for k in range(2, int(b**0.5)+1)) and b > 1)

    print(f"p={p:4d}: total_delta_sq = {total_direct:.6f}, "
          f"prime_b_contribution = {prime_total:.6f} ({100*prime_total/total_direct:.1f}%)")
