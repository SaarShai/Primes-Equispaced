#!/usr/bin/env python3
"""
Verify the key relationship: Σ E(k)² ≈ p · ∫₀¹ E(x)² dx

This checks the Riemann sum connection between the discrete p-grid
sampling and the continuous L² integral of the Farey counting error.
"""

from fractions import Fraction
from math import gcd, log, pi
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as sorted list of Fraction objects."""
    fracs = set()
    fracs.add(Fraction(0, 1))
    fracs.add(Fraction(1, 1))
    for b in range(1, N + 1):
        for a in range(0, b + 1):
            if gcd(a, b) == 1:
                fracs.add(Fraction(a, b))
    return sorted(fracs)

def compute_E_grid(farey, p):
    """Compute E(k) = A(k) - n*k/p for k=1,...,p-1."""
    n = len(farey)
    E_vals = []
    idx = 0
    for k in range(1, p):
        threshold = Fraction(k, p)
        # Count fractions <= k/p
        while idx < n and farey[idx] <= threshold:
            idx += 1
        A_k = idx
        E_k = A_k - Fraction(n * k, p)
        E_vals.append(E_k)
        idx = 0  # reset for next k (inefficient but correct)
    return E_vals

def compute_E_grid_fast(farey, p):
    """Compute E(k) = A(k) - n*k/p for k=1,...,p-1 (fast version)."""
    n = len(farey)
    E_vals = []
    idx = 0
    for k in range(1, p):
        threshold = Fraction(k, p)
        while idx < n and farey[idx] <= threshold:
            idx += 1
        A_k = idx
        E_k_float = A_k - n * k / p
        E_vals.append((E_k_float, A_k))
    return E_vals

def compute_continuous_L2(farey):
    """Compute ∫₀¹ E(x)² dx exactly where E(x) = #{f ≤ x} - n*x.

    Between f_j and f_{j+1}, E(x) = (j+1) - n*x (since f_0=0 counts as one).
    Wait: A(x) = #{f ∈ F_N : f ≤ x}. For x in [f_j, f_{j+1}), A(x) = j+1
    (since f_0, f_1, ..., f_j are all ≤ x, that's j+1 fractions).

    E(x) = (j+1) - n*x for x ∈ [f_j, f_{j+1}).
    """
    n = len(farey)
    integral = Fraction(0)

    for j in range(n - 1):
        f_j = farey[j]
        f_next = farey[j + 1]
        d = f_next - f_j  # gap width

        # E(x) = (j+1) - n*x on [f_j, f_next)
        # E(x)² = (j+1)² - 2(j+1)*n*x + n²*x²
        # ∫ E² dx from f_j to f_next:
        #   = (j+1)²*d - 2(j+1)*n*(f_next² - f_j²)/2 + n²*(f_next³ - f_j³)/3
        #   = (j+1)²*d - (j+1)*n*(f_next² - f_j²) + n²*(f_next³ - f_j³)/3

        a = j + 1  # the count value
        integral += a * a * d
        integral -= a * n * (f_next * f_next - f_j * f_j)
        integral += Fraction(n * n, 3) * (f_next ** 3 - f_j ** 3)

    return integral

def compute_sum_D_squared(farey):
    """Compute Σ D_j² where D_j = j - n*f_j."""
    n = len(farey)
    total = Fraction(0)
    for j, f in enumerate(farey):
        D = j - n * f
        total += D * D
    return total

def main():
    primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
              67, 71, 73, 79, 83, 89, 97, 101, 107, 113, 127, 131, 137, 149,
              151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

    # Limit to primes where exact computation is feasible
    max_p = 200
    primes = [p for p in primes if p <= max_p]

    print(f"{'p':>5} {'n':>6} {'ΣE²':>14} {'p·∫E²':>14} {'ratio':>8} "
          f"{'ΣE²/(p²logp)':>14} {'C_W':>8} {'ΣD²':>12}")
    print("-" * 100)

    for p in primes:
        N = p - 1
        farey = farey_sequence(N)
        n = len(farey)

        # Compute Σ E(k)² on p-grid
        E_data = compute_E_grid_fast(farey, p)
        sum_E2 = sum(e**2 for e, a in E_data)

        # Compute continuous ∫ E(x)² dx (exact rational for small p)
        if p <= 60:
            integral_exact = compute_continuous_L2(farey)
            p_times_integral = float(p * integral_exact)
        else:
            # Use float approximation for larger p
            integral_float = 0.0
            for j in range(n - 1):
                f_j = float(farey[j])
                f_next = float(farey[j + 1])
                d = f_next - f_j
                a = j + 1
                integral_float += a * a * d
                integral_float -= a * n * (f_next**2 - f_j**2)
                integral_float += (n * n / 3) * (f_next**3 - f_j**3)
            p_times_integral = p * integral_float

        # Compute Σ D_j² and C_W
        if p <= 60:
            sum_D2 = float(compute_sum_D_squared(farey))
        else:
            sum_D2 = sum((j - n * float(f))**2 for j, f in enumerate(farey))

        W_N = sum_D2 / (n * n)
        C_W = N * W_N

        ratio = sum_E2 / p_times_integral if p_times_integral > 0 else float('inf')

        logp = log(p)
        normalized = sum_E2 / (p * p * logp)

        print(f"{p:>5} {n:>6} {sum_E2:>14.2f} {p_times_integral:>14.2f} "
              f"{ratio:>8.4f} {normalized:>14.6f} {C_W:>8.4f} {sum_D2:>12.1f}")

    print()
    print("Key relationship: Σ E(k)² ≈ p · ∫₀¹ E(x)² dx")
    print("If ratio ≈ 1, the Riemann sum approximation is accurate.")
    print()
    print("The normalized Σ E(k)²/(p²·log p) should stabilize near ~0.066")
    print("C_W(N) = N·W(N) should be positive and slowly growing")

if __name__ == "__main__":
    main()
