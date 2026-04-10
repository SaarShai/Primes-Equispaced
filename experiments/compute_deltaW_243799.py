#!/usr/bin/env python3
"""
Compute ΔW at p = 243799 using the four-term decomposition.

n'^2 * ΔW = A - B' - C' - D

where:
  A = (n'^2/n^2 - 1) * sum(D_{F_N}(f)^2)
  B' = 2*sum(D*delta) over interior fractions
  C' = sum(delta^2) over interior fractions
  D = sum_{k=1}^{p-1} D_{F_p}(k/p)^2

We have B', C', sum(D^2) from the streaming computation.
We need A and D.

For D: D_{F_p}(k/p) is the displacement of k/p in F_p.
This requires knowing the rank of k/p in F_p, which is expensive.

Alternative: use the proved identity D/A = 1 + O(1/p^2).
If D = A(1 + eps) where |eps| << 1, then:
  n'^2 * ΔW = A - B' - C' - D = A - B' - C' - A(1+eps) = -B' - C' - A*eps
  = -(B' + C') - A*eps

Since A*eps is small (O(N^2/p^2) * sum D^2 ~ O(1) * N^2), and B'+C' ~ 10^9-10^10:
  ΔW ≈ -(B' + C')/n'^2

Let me compute this.
"""

import math

p = 243799
N = p - 1  # 243798
n = 18066862385  # |F_N|
n_prime = n + (p - 1)  # |F_p| = n + p - 1

B_prime = -9.190201299936827e+09
C_prime = 3.010774067758968e+09
sum_D_sq = 9.021500911558475e+14

print(f"p = {p}")
print(f"N = {N}")
print(f"n = |F_N| = {n}")
print(f"n' = |F_p| = {n_prime}")
print(f"B' = {B_prime:.6e}")
print(f"C' = {C_prime:.6e}")
print(f"sum(D^2) = {sum_D_sq:.6e}")

# Compute A
# A = (n'^2/n^2 - 1) * sum(D^2)
ratio = (n_prime / n) ** 2
A = (ratio - 1) * sum_D_sq
print(f"\nn'^2/n^2 = {ratio:.15f}")
print(f"n'^2/n^2 - 1 = {ratio - 1:.10e}")
print(f"A = {A:.6e}")

# From the proved identity |D/A - 1| = O(1/p^2):
# D = A + O(A/p^2)
# So A - D = O(A/p^2) which is small
A_over_p2 = A / (p * p)
print(f"A/p^2 = {A_over_p2:.6e} (= O(A-D))")

# B' + C'
BpC = B_prime + C_prime
print(f"\nB' + C' = {BpC:.6e}")
print(f"|B' + C'| = {abs(BpC):.6e}")

# ΔW ≈ -(B'+C')/n'^2 + (A-D)/n'^2
# Lower bound on ΔW (most negative):
# If A - D = -|A/p^2|:
deltaW_upper = (-BpC + abs(A_over_p2)) / (n_prime ** 2)
deltaW_lower = (-BpC - abs(A_over_p2)) / (n_prime ** 2)
deltaW_approx = -BpC / (n_prime ** 2)

print(f"\nn'^2 = {n_prime**2:.6e}")
print(f"\nΔW approximation (ignoring A-D):")
print(f"  ΔW ≈ -(B'+C')/n'^2 = {deltaW_approx:.6e}")
print(f"\nWith A-D correction (|A-D| <= A/p^2 = {abs(A_over_p2):.6e}):")
print(f"  ΔW lower bound: {deltaW_lower:.6e}")
print(f"  ΔW upper bound: {deltaW_upper:.6e}")

# Sanity check: what's the order of magnitude of W(N)?
# W(N) = sum(D^2)/n^2
W_N = sum_D_sq / (n ** 2)
print(f"\nW(N) = sum(D^2)/n^2 = {W_N:.10e}")
print(f"ΔW/W(N) = {deltaW_approx/W_N:.6e}")

# The exact A-D from the D'-A'=-1 identity:
# D' - A' = -1 means sum_{new} D_new^2 - (n'^2/n^2 - 1)*sum_old D_old^2 = -1
# So D = A - 1. EXACTLY.
print(f"\n=== FROM D' - A' = -1 (Lean-verified) ===")
print(f"D = A - 1 = {A - 1:.6e}")
print(f"A - D = 1 (exactly)")

# Therefore:
# n'^2 * ΔW = A - B' - C' - D = A - B' - C' - (A - 1) = 1 - B' - C'
n2_DW = 1 - B_prime - C_prime
deltaW_exact = n2_DW / (n_prime ** 2)

print(f"\nn'^2 * ΔW = 1 - B' - C' = 1 - ({B_prime:.6e}) - ({C_prime:.6e})")
print(f"          = {n2_DW:.6e}")
print(f"ΔW = {deltaW_exact:.6e}")
print(f"ΔW/W(N) = {deltaW_exact / W_N:.6e}")

if deltaW_exact > 0:
    print(f"\n*** ΔW > 0: DISCREPANCY INCREASES at p = {p} ***")
    print(f"*** SIGN THEOREM IS FALSE at this prime! ***")
else:
    print(f"\nΔW < 0: Sign theorem holds at p = {p}")

# Also check: the full decomposition
# n'^2 * W(p) = sum_{F_p} D_{F_p}(f)^2 = sum_old D_new^2 + sum_new D_new^2
# n'^2 * W(p) = n'^2 * W(N) + (n'^2/n^2 - 1)*(-sum D_old^2) + stuff
# Actually, the four-term is:
# n'^2 * [W(p) - W(N)] = n'^2 * W(p) - n'^2 * W(N)
#   = [sum_{F_p} D_{F_p}^2] - (n'/n)^2 * [sum_{F_N} D_{F_N}^2]
# After adding and subtracting the cross terms, we get
# n'^2 * ΔW = A - B' - C' - D
# where D' - A' = -1 gives A - D = 1.
# So n'^2 * ΔW = 1 - B' - C'.

print(f"\n=== FINAL ===")
print(f"n'^2 * ΔW = 1 - B' - C'")
print(f"B' + C' = {BpC:.6e}")
print(f"1 - (B' + C') = {1 - BpC:.6e}")
print(f"ΔW = (1 - B' - C') / n'^2 = {(1 - BpC) / n_prime**2:.6e}")
print(f"Sign of ΔW: {'POSITIVE (BAD)' if 1 - BpC > 0 else 'NEGATIVE (GOOD)'}")
