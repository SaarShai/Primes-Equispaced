#!/usr/bin/env python3
"""
GAP 2 Chain Proof Verification
================================
Chain: C_W >= 1/4 --> Sigma E(k)^2 bound --> D' bound --> Sign theorem

We verify numerically for primes p = 5, 7, 11, 13, ..., 997:

1. C_W(N) = sum D_j^2 / n  where D_j = j - n*f_j (integer scale)
   Equivalently C_W(N) = N * sum (f_j - j/n)^2

2. The Cauchy-Schwarz bound: C_W(N) >= 1/4
   (from sum D_j = -n/2, Cauchy-Schwarz gives sum D_j^2 >= n/4)

3. E(k) = A(k) - n*k/p  for k=1..p-1
   where A(k) = #{f in F_N : f <= k/p}

4. The "sampling relationship": sum E(k)^2 vs p * C_W(N)
   Check whether sum E(k)^2 ~ 2 * p * C_W or just p * C_W

5. D' = sum D_new(k/p)^2 where D_new(k/p) = E(k) + k/p
   So D' = sum E(k)^2 + 2*sum (k/p)*E(k) + sum (k/p)^2

6. A' = dilution of old fractions (need to compute from 4-term decomposition)

7. Check: does B + C + D > A (equivalently DeltaW < 0)?
"""

from fractions import Fraction
from math import log, pi, sqrt, gcd
import sys

def farey_sequence(N):
    """Generate Farey sequence F_N as list of Fraction objects."""
    fracs = set()
    fracs.add(Fraction(0, 1))
    fracs.add(Fraction(1, 1))
    for q in range(1, N + 1):
        for p_num in range(1, q + 1):
            if gcd(p_num, q) == 1:
                fracs.add(Fraction(p_num, q))
    return sorted(fracs)

def compute_CW(F_N, N):
    """
    Compute C_W(N) = N * sum (f_j - j/n)^2
    Also return sum D_j and sum D_j^2 where D_j = j - n*f_j
    """
    n = len(F_N)
    sum_D = 0
    sum_D2 = 0
    sum_d2 = 0.0  # (f_j - j/n)^2

    for j, f in enumerate(F_N):
        D_j = j - n * float(f)  # integer-scale discrepancy
        d_j = float(f) - j / n  # standard discrepancy
        sum_D += D_j
        sum_D2 += D_j ** 2
        sum_d2 += d_j ** 2

    CW = N * sum_d2
    # Also: CW = sum_D2 / n (should be equivalent up to N vs n scaling)
    CW_alt = sum_D2 / n

    return CW, CW_alt, sum_D, sum_D2, n

def compute_E_and_sums(F_N, p):
    """
    Compute E(k) = A(k) - n*k/p for k=1..p-1.
    Also compute sum E(k)^2, sum (k/p)*E(k), sum (k/p)^2.
    """
    n = len(F_N)

    # A(k) = #{f in F_N : f <= k/p}
    # Pre-sort F_N (already sorted) and use binary search
    F_float = [float(f) for f in F_N]

    E_vals = []
    sum_E2 = 0.0
    sum_kp_E = 0.0
    sum_kp2 = 0.0
    sum_E = 0.0

    for k in range(1, p):
        threshold = k / p
        # Count f <= k/p using binary search
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if F_float[mid] <= threshold:
                lo = mid + 1
            else:
                hi = mid
        A_k = lo  # number of f <= k/p

        E_k = A_k - n * k / p
        E_vals.append(E_k)
        sum_E += E_k
        sum_E2 += E_k ** 2
        sum_kp_E += (k / p) * E_k
        sum_kp2 += (k / p) ** 2

    return E_vals, sum_E, sum_E2, sum_kp_E, sum_kp2

def compute_four_term(F_old, F_new, N_old, N_new):
    """
    Compute A, B, C, D terms of the four-term decomposition.
    A = dilution of old fractions
    B = interaction between old and new
    C = creation (new fractions)
    D = correction

    Actually compute DeltaW = W(N_new) - W(N_old) directly,
    and also D' = sum of squared displacements of NEW fractions.
    """
    n_old = len(F_old)
    n_new = len(F_new)

    # Compute W(N_old) and W(N_new) directly
    W_old = 0.0
    for j, f in enumerate(F_old):
        d = float(f) - j / n_old
        W_old += d * d

    W_new = 0.0
    for j, f in enumerate(F_new):
        d = float(f) - j / n_new
        W_new += d * d

    # Delta W
    DeltaW = W_new - W_old

    # D' = sum of D_new(k/p)^2 for new fractions
    # New fractions are those in F_new but not in F_old
    old_set = set(F_old)
    new_fracs = [f for f in F_new if f not in old_set]

    D_prime = 0.0
    for f in new_fracs:
        j = F_new.index(f)  # rank in F_new
        d = j - n_new * float(f)
        D_prime += d * d

    # A' = sum over old fractions of (D_new_j^2 - D_old_j^2)
    # where D_new_j = rank_in_F_new - n_new * f, D_old_j = rank_in_F_old - n_old * f
    A_prime = 0.0
    j_old = 0
    for j_new, f in enumerate(F_new):
        if f in old_set:
            D_old = j_old - n_old * float(f)
            D_new = j_new - n_new * float(f)
            A_prime += D_new ** 2 - D_old ** 2
            j_old += 1

    return W_old, W_new, DeltaW, D_prime, A_prime, n_old, n_new

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    primes = [p for p in range(5, 500) if is_prime(p)]

    print("=" * 120)
    print("GAP 2 CHAIN PROOF VERIFICATION")
    print("=" * 120)

    # ===== PART 1: Verify C_W >= 1/4 =====
    print("\n" + "=" * 80)
    print("PART 1: C_W(N) >= 1/4 (Cauchy-Schwarz from sum D = -n/2)")
    print("=" * 80)
    print(f"{'p':>6} {'N':>6} {'n':>8} {'C_W':>10} {'C_W>=1/4':>10} {'sumD':>12} {'sumD2':>14} {'sumD2>=n/4':>12}")
    print("-" * 100)

    cw_data = {}

    for p in primes:
        N = p - 1
        F_N = farey_sequence(N)
        CW, CW_alt, sum_D, sum_D2, n = compute_CW(F_N, N)
        cw_data[p] = (F_N, N, CW, CW_alt, sum_D, sum_D2, n)

        # The key check: sum D_j = -n/2 (exact) and sum D_j^2 >= n/4
        expected_sumD = -n / 2
        check_sumD = abs(sum_D - expected_sumD) < 1e-6
        check_D2 = sum_D2 >= n / 4 - 1e-10
        check_CW = CW >= 0.25 - 1e-10

        if p <= 101 or not check_CW:
            print(f"{p:>6} {N:>6} {n:>8} {CW:>10.4f} {'YES' if check_CW else '**NO**':>10} {sum_D:>12.1f} {sum_D2:>14.1f} {'YES' if check_D2 else '**NO**':>12}")

    print(f"\nC_W >= 1/4 holds for all {len(primes)} primes tested: {all(cw_data[p][2] >= 0.25 - 1e-10 for p in primes)}")

    # ===== PART 2: Sampling relationship: sum E(k)^2 vs p * C_W =====
    print("\n" + "=" * 80)
    print("PART 2: Sampling relationship — sum E(k)^2 vs p * C_W(N)")
    print("=" * 80)
    print(f"{'p':>6} {'sumE2':>14} {'p*CW':>14} {'ratio':>10} {'2p*CW':>14} {'ratio2':>10} {'sumE2/p^2':>12} {'sumE2/(p^2*logp)':>18}")
    print("-" * 120)

    e_data = {}

    for p in primes:
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        E_vals, sum_E, sum_E2, sum_kp_E, sum_kp2 = compute_E_and_sums(F_N, p)
        e_data[p] = (E_vals, sum_E, sum_E2, sum_kp_E, sum_kp2)

        pCW = p * CW
        ratio1 = sum_E2 / pCW if pCW > 0 else float('inf')
        ratio2 = sum_E2 / (2 * pCW) if pCW > 0 else float('inf')

        if p <= 101 or p in [199, 499]:
            print(f"{p:>6} {sum_E2:>14.2f} {pCW:>14.2f} {ratio1:>10.4f} {2*pCW:>14.2f} {ratio2:>10.4f} {sum_E2/p**2:>12.6f} {sum_E2/(p**2*log(p)):>18.6f}")

    # Check: is sum_E always 0?
    print(f"\nsum E(k) = 0 for all primes: {all(abs(e_data[p][1]) < 1e-6 for p in primes)}")

    # ===== PART 3: What is the actual relationship? =====
    print("\n" + "=" * 80)
    print("PART 3: Exact relationship between sum E(k)^2 and Farey discrepancy sums")
    print("=" * 80)

    # The key question: is sum E(k)^2 ≈ 2*p*n*W(N) or p*n*W(N) or something else?
    # C_W = N * W(N), so W(N) = C_W / N
    # p * n * W(N) = p * n * C_W / N = p * n * C_W / (p-1)
    # Since n ≈ 3N^2/pi^2 ≈ 3(p-1)^2/pi^2
    # p * n * W(N) ≈ p * 3(p-1)^2/pi^2 * C_W/(p-1) ≈ 3*C_W*p*(p-1)/pi^2

    print(f"{'p':>6} {'sumE2':>14} {'p*n*W':>14} {'ratio':>10} {'3CW*p^2/pi^2':>16} {'ratio':>10}")
    print("-" * 80)

    for p in primes:
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        sum_E2 = e_data[p][2]

        W_N = CW / N
        pnW = p * n * W_N
        formula = 3 * CW * p**2 / pi**2

        if p <= 101 or p in [199, 499]:
            r1 = sum_E2 / pnW if pnW > 0 else float('inf')
            r2 = sum_E2 / formula if formula > 0 else float('inf')
            print(f"{p:>6} {sum_E2:>14.2f} {pnW:>14.2f} {r1:>10.4f} {formula:>16.2f} {r2:>10.4f}")

    # ===== PART 4: Try the direct sampling argument =====
    print("\n" + "=" * 80)
    print("PART 4: Direct sum D^2 sampling argument")
    print("=" * 80)
    print("If E(k) ~ D(k/p) (continuous discrepancy sampled at k/p),")
    print("then sum E(k)^2 ≈ (p/n) * sum D_j^2 = (p/n) * n * C_W_alt = p * C_W_alt")
    print("where C_W_alt = sum D_j^2 / n")
    print()
    print(f"{'p':>6} {'sumE2':>14} {'p*CW_alt':>14} {'ratio':>10} {'sumD2':>14} {'p*sumD2/n':>14} {'ratio':>10}")
    print("-" * 100)

    for p in primes:
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        sum_E2 = e_data[p][2]

        p_sumD2_n = p * sum_D2 / n
        r1 = sum_E2 / (p * CW_alt) if CW_alt > 0 else 0
        r2 = sum_E2 / p_sumD2_n if p_sumD2_n > 0 else 0

        if p <= 101 or p in [199, 499]:
            print(f"{p:>6} {sum_E2:>14.2f} {p*CW_alt:>14.2f} {r1:>10.4f} {sum_D2:>14.1f} {p_sumD2_n:>14.2f} {r2:>10.4f}")

    # ===== PART 5: D' decomposition and check D' > A' =====
    print("\n" + "=" * 80)
    print("PART 5: D' = sumE2 + 2*sum(k/p)*E + sum(k/p)^2  vs  A'")
    print("Check: does D' contribute enough to make B + C + D > A?")
    print("=" * 80)
    print(f"{'p':>6} {'sumE2':>14} {'2*sum_kpE':>14} {'sum_kp2':>14} {'D_prime':>14} {'DeltaW':>14} {'DW<0?':>8}")
    print("-" * 100)

    for p in primes:
        if p > 200:
            continue
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        E_vals, sum_E, sum_E2, sum_kp_E, sum_kp2 = e_data[p]

        # D' from E decomposition
        D_prime_from_E = sum_E2 + 2 * sum_kp_E + sum_kp2

        # Compute actual DeltaW
        F_p = farey_sequence(p)
        n_new = len(F_p)

        W_old = 0.0
        for j, f in enumerate(F_N):
            d = float(f) - j / n
            W_old += d * d

        W_new = 0.0
        for j, f in enumerate(F_p):
            d = float(f) - j / n_new
            W_new += d * d

        DeltaW = W_new - W_old

        # Actual D' from direct computation
        old_set = set(F_N)
        D_prime_actual = 0.0
        for j, f in enumerate(F_p):
            if f not in old_set:
                d = j - n_new * float(f)
                D_prime_actual += d * d

        # Normalize: D_prime_from_E is in units of (integer-scale)^2
        # but E(k) is counting error, not rank-scale. Let me be careful.
        # E(k) = A(k) - n*k/p where A(k) = #{f in F_N : f <= k/p}
        # D_new(k/p) = rank_in_F_p(k/p) - n'*(k/p) where n' = |F_p|
        # rank_in_F_p(k/p) = (# old fracs <= k/p) + (# new fracs <= k/p)
        #                   = A(k) + k  (since new fracs are 1/p, 2/p, ..., k/p)
        # So D_new(k/p) = A(k) + k - n'*k/p = (A(k) - n*k/p) + k - (n'-n)*k/p
        #               = E(k) + k - (p-1)*k/p = E(k) + k*(p-1-p+1)/p... wait
        # n' = n + p - 1, so n' - n = p - 1
        # D_new(k/p) = A(k) + k - n'*k/p = E(k) + n*k/p + k - n'*k/p
        #            = E(k) + k - (n'-n)*k/p = E(k) + k - (p-1)*k/p
        #            = E(k) + k*(p - p + 1)/p = E(k) + k/p
        # YES! D_new(k/p) = E(k) + k/p  (as in Codex Proposition 1)

        # But D_new is in integer scale? Let me check units.
        # D(f) = rank(f) - |F|*f. This is dimensionless (rank is integer, |F|*f is real).
        # E(k) = A(k) - n*k/p is also dimensionless.
        # So D' = sum D_new^2 = sum (E(k) + k/p)^2
        # This should match D_prime_actual (which is in rank-scale, i.e., integer-minus-fraction)

        # D_prime_actual uses d = j - n_new * f which is rank-scale
        # D_prime_from_E = sum (E(k) + k/p)^2
        # These should match IF the convention is D_new(k/p) = rank - n'*f = E(k) + k/p
        # Let's check

        print(f"{p:>6} {sum_E2:>14.2f} {2*sum_kp_E:>14.2f} {sum_kp2:>14.4f} {D_prime_from_E:>14.2f} {DeltaW:>14.6f} {'YES' if DeltaW < 0 else 'NO':>8}")

    # ===== PART 6: The critical question — scaling =====
    print("\n" + "=" * 80)
    print("PART 6: THE CRITICAL SCALING QUESTION")
    print("=" * 80)
    print("sum E(k)^2 grows as what power of p?")
    print("From Codex data: sum E(k)^2 / (p^2 * log p) ≈ 0.066")
    print("So sum E(k)^2 ~ 0.066 * p^2 * log p")
    print()
    print("BUT: can we PROVE a lower bound from C_W >= 1/4?")
    print()
    print("The sampling argument gives:")
    print("  sum E(k)^2 ≈ factor * p * C_W(N)")
    print()
    print("Let's check what 'factor' is numerically:")
    print()

    print(f"{'p':>6} {'sumE2':>14} {'p*CW':>14} {'sumE2/(p*CW)':>14} {'n':>8} {'p*(sumD2/n)':>14} {'sumE2/that':>12}")
    print("-" * 100)

    for p in primes:
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        sum_E2 = e_data[p][2]

        r = sum_E2 / (p * CW) if CW > 0 else 0
        target = p * sum_D2 / n
        r2 = sum_E2 / target if target > 0 else 0

        if p <= 101 or p in [151, 199, 251, 499]:
            print(f"{p:>6} {sum_E2:>14.2f} {p*CW:>14.4f} {r:>14.4f} {n:>8} {target:>14.2f} {r2:>12.4f}")

    # ===== PART 7: What bounds can be proved vs what's needed =====
    print("\n" + "=" * 80)
    print("PART 7: PROVABLE CHAIN ANALYSIS")
    print("=" * 80)
    print()
    print("WHAT WE CAN PROVE from C_W >= 1/4:")
    print("  sum D_j^2 >= n/4")
    print("  C_W = sum D_j^2 / n >= 1/4")
    print()
    print("THE GAP: E(k) samples the CONTINUOUS discrepancy E(x) = A(x) - nx at x=k/p")
    print("  but the p-1 sample points are NOT the n Farey points.")
    print("  There's no simple 'sum E(k)^2 >= (p/n) * sum D_j^2' inequality.")
    print()
    print("HOWEVER, sum E(k)^2 is a Riemann sum:")
    print("  (1/p) * sum E(k)^2 ≈ integral_0^1 E(x)^2 dx = (some constant) * sum D_j^2 / n")
    print("  So sum E(k)^2 ≈ p * integral E(x)^2 dx = p * (sum D_j^2 / n) = p * C_W_alt")
    print()
    print("Let's verify this Riemann sum interpretation:")
    print()

    # Compute integral of E(x)^2 numerically
    print(f"{'p':>6} {'int_E2 (num)':>14} {'sumD2/n':>14} {'ratio':>10} {'(1/p)*sumE2':>14} {'vs int_E2':>10}")
    print("-" * 80)

    for p in primes:
        if p > 200:
            continue
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]
        F_float = sorted([float(f) for f in F_N])

        # Numerical integral of E(x)^2 using fine grid
        M = 10000
        int_E2 = 0.0
        for i in range(1, M + 1):
            x = i / M
            # A(x) = #{f in F_N : f <= x}
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if F_float[mid] <= x:
                    lo = mid + 1
                else:
                    hi = mid
            A_x = lo
            E_x = A_x - n * x
            int_E2 += E_x ** 2 / M

        sum_E2 = e_data[p][2]
        sumD2_over_n = sum_D2 / n

        r1 = int_E2 / sumD2_over_n if sumD2_over_n > 0 else 0
        r2 = (sum_E2 / p) / int_E2 if int_E2 > 0 else 0

        print(f"{p:>6} {int_E2:>14.4f} {sumD2_over_n:>14.4f} {r1:>10.4f} {sum_E2/p:>14.4f} {r2:>10.4f}")

    # ===== PART 8: THE REAL CHAIN =====
    print("\n" + "=" * 80)
    print("PART 8: THE ACTUAL ACHIEVABLE CHAIN")
    print("=" * 80)
    print()
    print("Step 1: sum D_j = -n/2  (exact, proved)")
    print("Step 2: sum D_j^2 >= n/4  (Cauchy-Schwarz, proved)")
    print("Step 3: integral E(x)^2 dx = sum D_j^2 / n >= 1/4  (by definition, C_W = N * integral)")
    print("Step 4: sum_{k=1}^{p-1} E(k)^2 ≈ p * integral E(x)^2 dx  (Riemann sum)")
    print("Step 5: So sum E(k)^2 ≈ p * C_W_alt >= p/4  (lower bound)")
    print()
    print("PROBLEM: This gives sum E(k)^2 >= c*p, but we need sum E(k)^2 >> p")
    print("to dominate corrections in D'.")
    print()
    print("KEY INSIGHT: The factor-of-2 is NOT an aliasing effect but comes from")
    print("the Riemann sum exceeding the integral due to discontinuities in E(x)!")
    print()

    # Check: does sum E(k)^2 >= 0.152 * p^2 hold?
    print("Checking claimed bound sum E(k)^2 >= 0.152 * p^2:")
    print(f"{'p':>6} {'sumE2':>14} {'0.152*p^2':>14} {'holds?':>8} {'actual ratio':>14}")
    print("-" * 60)

    all_hold = True
    for p in primes:
        sum_E2 = e_data[p][2]
        target = 0.152 * p**2
        holds = sum_E2 >= target
        if not holds:
            all_hold = False
        if p <= 101 or not holds:
            print(f"{p:>6} {sum_E2:>14.2f} {target:>14.2f} {'YES' if holds else '**NO**':>8} {sum_E2/p**2:>14.6f}")

    print(f"\nsum E(k)^2 >= 0.152*p^2 for all primes: {all_hold}")

    # Weaker: does sum E(k)^2 >= c * p hold (which is what C_W >= 1/4 gives)?
    print("\nChecking weaker bound sum E(k)^2 >= p/4 (from C_W >= 1/4 + Riemann):")
    print(f"{'p':>6} {'sumE2':>14} {'p/4':>14} {'holds?':>8} {'ratio':>14}")
    print("-" * 60)

    for p in primes[:15]:
        sum_E2 = e_data[p][2]
        print(f"{p:>6} {sum_E2:>14.2f} {p/4:>14.2f} {'YES' if sum_E2 >= p/4 else 'NO':>8} {sum_E2/(p/4):>14.4f}")

    # ===== PART 9: What do we ACTUALLY need for the sign theorem? =====
    print("\n" + "=" * 80)
    print("PART 9: WHAT'S ACTUALLY NEEDED FOR THE SIGN THEOREM")
    print("=" * 80)
    print()
    print("The sign theorem needs: B + C + D > A, i.e., DeltaW(p) < 0")
    print("In the 4-term decomp with n' = n + (p-1):")
    print()
    print("  n'^2 * W(p) = (stuff from old fracs) + D'")
    print("  n^2 * W(N)  = stuff from old fracs at old positions")
    print()
    print("DeltaW(p) = W(p) - W(N)")
    print()
    print("Let's compute DeltaW directly and check if C_W >= 1/4 plays any role:")
    print()

    print(f"{'p':>6} {'W(N)':>12} {'W(p)':>12} {'DeltaW':>14} {'DW<0':>8} {'D_prime':>14} {'A_prime':>14}")
    print("-" * 90)

    for p in primes:
        if p > 200:
            continue
        F_N, N, CW, CW_alt, sum_D, sum_D2, n = cw_data[p]

        F_p = farey_sequence(p)
        n_new = len(F_p)

        W_old = sum([(float(f) - j / n) ** 2 for j, f in enumerate(F_N)])
        W_new = sum([(float(f) - j / n_new) ** 2 for j, f in enumerate(F_p)])

        DeltaW = W_new - W_old

        # D' from E decomposition
        sum_E2 = e_data[p][2]
        sum_kp_E = e_data[p][3]
        sum_kp2 = e_data[p][4]
        D_prime_E = sum_E2 + 2 * sum_kp_E + sum_kp2

        # We need D_prime in the W-scale, not D-scale
        # W = sum d_j^2 where d_j = f_j - j/n
        # D(f) = j - n*f = -n*d_j, so D^2 = n^2 * d^2
        # D_prime (D-scale) = sum (E(k) + k/p)^2
        # D_prime (W-scale) = D_prime (D-scale) / n'^2

        D_prime_W = D_prime_E / n_new**2

        # A' (W-scale): change in old fractions' contribution
        A_prime_W = 0.0
        j_old = 0
        for j_new, f in enumerate(F_p):
            if f in set(F_N):
                d_old = float(f) - j_old / n
                d_new = float(f) - j_new / n_new
                A_prime_W += d_new ** 2 - d_old ** 2
                j_old += 1

        print(f"{p:>6} {W_old:>12.6f} {W_new:>12.6f} {DeltaW:>14.8f} {'YES' if DeltaW < 0 else 'NO':>8} {D_prime_W:>14.8f} {A_prime_W:>14.8f}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
KEY FINDINGS:

1. C_W >= 1/4 is PROVED (Cauchy-Schwarz from sum D = -n/2). Verified for all primes <= 499.

2. The chain C_W >= 1/4 --> sum E(k)^2 >= 0.152*p^2 DOES NOT FOLLOW.
   The correct chain gives: sum E(k)^2 ~ p * C_W_alt ~ p * (constant)
   This is of order p, NOT p^2.

3. The claimed factor "sum E(k)^2 ≈ 2p * n * W(N)" would give order p * n * (1/N) = p * n/N ~ p^2
   but this requires n/N ~ p, which IS true (n ~ 3N^2/pi^2, N = p-1, so n/N ~ 3p/pi^2).

4. THEREFORE: sum E(k)^2 ~ p * integral E(x)^2 dx
   integral E(x)^2 dx = C_W(N)/N = (sum D^2/n)/N ≈ C_W_alt/N
   WAIT — the integral of E(x)^2 over [0,1] is NOT C_W/N. Let me recheck...

   E(x) = A(x) - nx (continuous discrepancy)
   integral_0^1 E(x)^2 dx = sum_{j=0}^{n-1} integral_{f_j}^{f_{j+1}} (j - nx + δ)^2 dx

   This integral is O(n) in the range, not O(1).
   So sum E(k)^2 ~ p * O(n) = O(p*n) = O(p^3). Too big!

   The issue is that integral E(x)^2 dx is NOT the same as sum D_j^2/n or C_W.

5. THE REAL RELATIONSHIP needs more careful analysis — see Part 3 data.
""")

if __name__ == "__main__":
    main()
