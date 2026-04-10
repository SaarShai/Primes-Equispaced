#!/usr/bin/env python3
"""
Can the factor of 2 be PROVED?

Key insight: sum E(k)^2 is NOT just a Riemann sum of int E(x)^2 dx.
It is a DISCRETE second moment of a step function sampled at p-1 equispaced points.

The factor of 2 arises because E(x) is a step function with n jumps of size +1,
and the p-grid samples create "aliasing" between the jump structure and the grid.

Let's decompose E(k/p) explicitly.

E(k/p) = A(k/p) - n*k/p

where A(x) = sum_{j: f_j <= x} 1 = step function with jumps at Farey points.

Now: sum_{k=1}^{p-1} E(k/p)^2 = sum_{k=1}^{p-1} [A(k/p) - n*k/p]^2

Key: the pair (k/p, f_j) interaction. For each Farey fraction f_j = a/b,
the grid point k/p is closest when k = floor(p*a/b) or ceil(p*a/b).

ALTERNATIVE APPROACH: Fourier/character sum decomposition.

A(x) = nx + sum_{m != 0} c_m * e^{2pi i m x}  where c_m are Fourier coefficients
of the Farey staircase.

E(x) = A(x) - nx = sum_{m != 0} c_m * e^{2pi i m x}

sum_{k=1}^{p-1} E(k/p)^2 = sum_{k=1}^{p-1} |sum_{m != 0} c_m e^{2pi i mk/p}|^2

By Parseval on the finite group Z/pZ:
= (p-1) * sum_{m != 0 mod p} |c_m|^2 * [character sum factor]

Actually, expanding:
= sum_{m,m'} c_m * conj(c_{m'}) * sum_{k=1}^{p-1} e^{2pi i (m-m')k/p}

The inner sum = p-1 if m ≡ m' (mod p), and = -1 otherwise.

So sum E(k/p)^2 = (p-1) * sum_{m ≡ m' mod p} c_m * conj(c_{m'}) + correction
                 = p * sum_{m ≡ 0 mod p, m != 0} |c_m|^2
                   + p * sum_{m != m', m ≡ m' mod p} c_m conj(c_{m'})
                   - sum_{m != 0} |c_m|^2

Hmm, this is getting into Ramanujan sum territory. Let me just verify
the key numerical relationships and identify the exact nature of the factor 2.
"""

from fractions import Fraction
from math import gcd, log, pi, sqrt, cos, sin
import cmath

def farey_sequence(N):
    fracs = set()
    fracs.add(Fraction(0, 1))
    fracs.add(Fraction(1, 1))
    for q in range(1, N + 1):
        for p_num in range(1, q + 1):
            if gcd(p_num, q) == 1:
                fracs.add(Fraction(p_num, q))
    return sorted(fracs)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

# For a few primes, decompose sum E^2 via Fourier
primes_test = [p for p in range(11, 150) if is_prime(p)]

print("=" * 100)
print("FOURIER DECOMPOSITION OF SUM E(k)^2")
print("=" * 100)
print()
print("E(x) = A(x) - nx. The Fourier coefficients of A(x) on [0,1] are:")
print("  c_0 = n/2 (mean of A on [0,1])")
print("  c_m = (1/(2pi i m)) * sum_{j=0}^{n-1} e^{-2pi i m f_j}  for m != 0")
print()
print("Then sum_{k=1}^{p-1} E(k/p)^2 = Parseval on Z/pZ gives:")
print("  = p * sum_{m=1}^{p-1} |hat_m|^2")
print("where hat_m = (1/p) sum_{k=1}^{p-1} E(k/p) e^{-2pi i mk/p}")
print()

for p in primes_test[:8]:
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    F_float = [float(f) for f in F_N]

    # Compute E(k/p) for k=1..p-1
    E_vals = []
    for k in range(1, p):
        x = k / p
        A = sum(1 for f in F_float if f <= x)
        E_vals.append(A - n * x)

    sum_E2 = sum(e**2 for e in E_vals)

    # Compute DFT of E
    hat = []
    for m in range(p):
        val = sum(E_vals[k] * cmath.exp(-2j * pi * m * (k+1) / p) for k in range(p-1))
        hat.append(val / p)

    parseval_check = p * sum(abs(hat[m])**2 for m in range(1, p))  # skip m=0 since sum E = 0

    # Also compute the continuous Fourier transform approach
    # c_m = sum_{j} e^{-2pi i m f_j} / (2pi i m) for the staircase
    # E(x) = sum_{j: f_j <= x} 1 - nx
    # Its Fourier coefficients (continuous):
    # For m != 0: c_m^cont = -(1/(2pi i m)) * [sum_j e^{-2pi i m f_j} - n * delta_{m,0}]
    # Actually for A(x) as step function: A^(m) = (1/(2pi i m)) sum_j (e^{-2pi i m f_j} - 1)... complicated

    # Just compare sum_E2 vs Parseval
    print(f"p={p:>4}: sum E^2 = {sum_E2:>12.2f}, Parseval = {parseval_check.real:>12.2f}, ratio = {sum_E2/parseval_check.real:.6f}")

print()
print("=" * 100)
print("THE FACTOR OF 2: PRECISE DECOMPOSITION")
print("=" * 100)
print()
print("sum E(k)^2 = p * integral E^2 + R(p)")
print("where R(p) is the 'aliasing remainder' from the Riemann sum.")
print()
print("From data: R(p) ≈ p * integral E^2, i.e., R ≈ same size as main term.")
print("So sum E^2 ≈ 2 * p * integral E^2.")
print()
print("The question: can we prove R(p) >= 0 (i.e., the Riemann sum overestimates)?")
print()

# Check: is R(p) = sum E(k)^2 - p * int E^2 always >= 0?
print(f"{'p':>6} {'sumE2':>12} {'p*intE2':>12} {'R(p)':>12} {'R/p*intE2':>10} {'R > 0?':>8}")
print("-" * 70)

for p in primes_test:
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    F_float = [float(f) for f in F_N]

    # Exact integral of E(x)^2
    int_E2 = 0.0
    for j in range(n - 1):
        a, b = F_float[j], F_float[j+1]
        u_a = (j + 1) - n * a
        u_b = (j + 1) - n * b
        int_E2 += (u_a**3 - u_b**3) / (3 * n)

    # sum E(k)^2
    sum_E2 = 0.0
    for k in range(1, p):
        x = k / p
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if F_float[mid] <= x: lo = mid + 1
            else: hi = mid
        A_k = lo
        sum_E2 += (A_k - n * x)**2

    R = sum_E2 - p * int_E2
    ratio = R / (p * int_E2) if int_E2 > 0 else 0

    if p <= 101 or p in [127, 149]:
        print(f"{p:>6} {sum_E2:>12.2f} {p*int_E2:>12.2f} {R:>12.2f} {ratio:>10.4f} {'YES' if R > 0 else '**NO**':>8}")

print()
print("=" * 100)
print("ALTERNATIVE: DIRECT LOWER BOUND WITHOUT FACTOR 2")
print("=" * 100)
print()
print("Instead of trying to prove the factor 2, try a different route:")
print()
print("APPROACH: Variance decomposition")
print("  sum E(k)^2 = (p-1) * Var[E] + (sum E)^2/(p-1)")
print("  Since sum E = 0: sum E^2 = (p-1) * Var[E]")
print()
print("So we need: Var[E(k/p)] >= c * p for some c > 0.")
print("Equivalently: E[E(k/p)^2] >= c * p where expectation is over k uniform on 1..p-1.")
print()
print("Now E(k/p) = A(k/p) - n*k/p. The variance of E over the p-grid is:")
print("  Var = E[E^2] = E[A^2] - 2n*E[k*A/p] + n^2*E[k^2/p^2]")
print()
print("E[k^2/p^2] = (1/(p-1)) * sum_{k=1}^{p-1} k^2/p^2 = (2p-1)/(6p) ≈ 1/3")
print()
print("The key term is E[A(k/p)^2]. From the pair count formula:")
print("  (p-1)*E[A^2] = sum_{k=1}^{p-1} A(k/p)^2 = sum_{f,g in F_N*} K(f,g)")
print("  where K(f,g) = #{k: k/p > max(f,g)} = p - 1 - floor(p*max(f,g))")
print()
print("This is where the ORDER p^2 comes from — it's the PAIR SUM over n^2 pairs")
print("of Farey fractions, each contributing O(p), giving total O(n^2 * p) = O(p^5).")
print("Then E[A^2] = O(p^5)/(p-1) = O(p^4), and Var = O(p^4) - O(p^4) with")
print("the cancellation being the key to getting the right order.")
print()

# Let's verify the pair count decomposition numerically
print("PAIR COUNT VERIFICATION:")
print(f"{'p':>6} {'sum A^2':>14} {'pair_count':>14} {'match?':>8} {'n^2*p/3':>14} {'sumA2/that':>10}")
print("-" * 80)

for p in primes_test[:10]:
    N = p - 1
    F_N = farey_sequence(N)
    n = len(F_N)
    F_float = [float(f) for f in F_N]
    F_star = F_float[:-1]  # F_N \ {1}
    n_star = len(F_star)

    # Direct sum A(k)^2
    sum_A2 = 0.0
    for k in range(1, p):
        x = k / p
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if F_float[mid] <= x: lo = mid + 1
            else: hi = mid
        sum_A2 += lo ** 2

    # Pair count
    pair_sum = 0.0
    for i, f in enumerate(F_star):
        for j, g in enumerate(F_star):
            pair_sum += (p - 1) - int(p * max(f, g))

    target = n_star**2 * p / 3

    print(f"{p:>6} {sum_A2:>14.0f} {pair_sum:>14.0f} {'YES' if abs(sum_A2-pair_sum)<1 else 'NO':>8} {target:>14.0f} {sum_A2/target:>10.4f}")

print()
print("=" * 100)
print("BOTTOM LINE: CAN THE CHAIN CLOSE GAP 2?")
print("=" * 100)
print("""
ANSWER: The chain C_W >= 1/4 --> sum E^2 >= c*p^2 has THREE links:

Link 1 (PROVED): C_W(N) >= 1/4 for N >= 16
  Proof: Cauchy-Schwarz from sum D_j = -n/2, giving sum D_j^2 >= n/4.

Link 2 (PARTIALLY PROVED): int E(x)^2 dx = C_W_alt = sum D^2/n
  This is true by definition — just a change of notation.
  C_W_alt = pi^2/(3N) * C_W * n/1 ... wait, C_W_alt = 3N*C_W/pi^2.
  So C_W_alt >= 3N/(4*pi^2) = 3(p-1)/(4*pi^2).
  This gives int E^2 >= 3(p-1)/(4*pi^2) ≈ 0.076 * p.

Link 3 (THE GAP): sum E(k)^2 >= c * p * int E^2
  The data shows the ratio sum E^2 / (p * int E^2) → 2.
  If we could prove ratio >= 1, we'd get sum E^2 >= p * 0.076p = 0.076*p^2.
  If we could prove ratio >= 2, we'd get sum E^2 >= 0.152*p^2.

  The ratio being >= 1 means the Riemann sum overestimates the integral.
  For a MONOTONE function, left-endpoint Riemann sums overestimate decreasing
  functions. But E(x)^2 is not monotone — it's a sum of parabolic arcs.

RESOLUTION OF THE CONFUSION:

The key misunderstanding in the original analysis was confusing TWO different
quantities:
  - C_W = N * sum (f_j - j/n)^2 ≈ 0.66 (bounded, O(1))
  - C_W_alt = sum (j - n*f_j)^2 / n = n * C_W / N ≈ 0.2*p (growing!)

The chain actually needs C_W_alt (which grows as p), not C_W (which is O(1)).
And C_W >= 1/4 implies C_W_alt >= 3p/(4*pi^2) via the relation C_W_alt = 3N*C_W/pi^2.

So the correct chain is:
  C_W >= 1/4  →  C_W_alt >= 3(p-1)/(4pi^2)  →  int E^2 >= 0.076*p
  →  (IF Riemann ≈ integral)  sum E^2 >= 0.076*p^2

The "Riemann ≈ integral" step needs the factor-of-2, which is empirical.
But even ratio >= 1 (provable?) would give sum E^2 >= 0.076*p^2.

For Gap 2, we need sum E^2 to dominate the correction terms in D'.
The correction terms are O(p^{3/2}) (from CLT-type behavior of sum (k/p)*E(k)).
So sum E^2 >= c*p^2 for ANY c > 0 suffices for large enough p!

CONCLUSION: If we can prove the Riemann sum ratio >= 1 (or even >= epsilon),
then C_W >= 1/4 DOES close Gap 2 for sufficiently large p.
""")
