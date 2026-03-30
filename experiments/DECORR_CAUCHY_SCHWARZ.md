# Decorrelation via Cauchy-Schwarz: Analysis and Exact Identity

**Date:** 2026-03-30
**Status:** RESOLVED -- approach fails, but exact identity discovered
**Verdict:** B = 1/n - C < 0 for all N >= 3 (proved exactly)

---

## 1. Setup

Let f_1 < f_2 < ... < f_n be the Farey fractions of order N in (0, 1].

- **Discrepancy:** D(f_k) = k/n - f_k
- **Gap:** delta_k = f_k - f_{k-1} (with f_0 = 0)
- **Linear regression:** D(f) = alpha * (f - 1/2) + D_err(f), where alpha = sum(D * (f-1/2)) / sum((f-1/2)^2)
- **C** = sum(delta_k^2)
- **S** = sum(D_err_k * delta_k)
- **B** = alpha * C + 2 * S

**Goal:** Prove |S| = o(C), which would give B >= 0 for large N.

---

## 2. Three Exact Identities (All Proved)

### Identity 1: sum(D_k) = 0

**Proof:** By the pairing symmetry f <-> 1-f of Farey fractions in (0,1]:

    sum(k/n) = (n+1)/2
    sum(f_k) = (n+1)/2    (from the symmetric pairing, with 1/2 and 1/1 unpaired)

Therefore sum(D_k) = (n+1)/2 - (n+1)/2 = 0. QED

### Identity 2: sum(D_k * delta_k) = 1/(2n) - C/2

**Proof:** Telescoping the squared discrepancy. Since D_0 = 0 and D_n = 0:

    0 = D_n^2 - D_0^2 = sum_{k=1}^n [D_k^2 - D_{k-1}^2]

Using D_k = D_{k-1} + (1/n - delta_k):

    D_k^2 = D_{k-1}^2 + 2*D_{k-1}*(1/n - delta_k) + (1/n - delta_k)^2

Summing and using sum(D_{k-1}) = 0 (Identity 1):

    0 = -2*sum(D_{k-1} * delta_k) + sum(1/n - delta_k)^2
    sum(D_{k-1} * delta_k) = (1/2)*(C - 1/n)

Then sum(D_k * delta_k) = sum(D_{k-1} * delta_k) + sum((1/n - delta_k) * delta_k):

    sum(D_k * delta_k) = (C - 1/n)/2 + 1/n - C = 1/(2n) - C/2

QED

### Identity 3: sum((f_k - 1/2) * delta_k) = C/2

**Proof:** Expand sum(f_k * delta_k) = sum(f_k^2 - f_k * f_{k-1}).

From C = sum(f_k - f_{k-1})^2 = sum(f_k^2) + sum(f_{k-1}^2) - 2*sum(f_k * f_{k-1}):

    C = 2*sum(f_k^2) - 1 - 2*sum(f_k * f_{k-1})

(using sum_{k=0}^{n-1} f_k^2 = sum_{k=1}^n f_k^2 - f_n^2 + f_0^2 = sum f_k^2 - 1)

Therefore:

    sum(f_k * f_{k-1}) = sum(f_k^2) - (C+1)/2

And:

    sum(f_k * delta_k) = sum(f_k^2) - sum(f_k * f_{k-1}) = (C+1)/2

So sum((f_k - 1/2) * delta_k) = (C+1)/2 - 1/2 = C/2. QED

**Verified with exact rational arithmetic for p = 13, 29, 53.**

---

## 3. The Critical Cancellation: B = 1/n - C

Combining the three identities:

    S = sum(D_err * delta) = sum(D * delta) - alpha * sum((f-1/2) * delta)
      = [1/(2n) - C/2] - alpha * [C/2]
      = 1/(2n) - C*(1 + alpha)/2

    B = alpha*C + 2*S
      = alpha*C + 1/n - C*(1 + alpha)
      = alpha*C + 1/n - C - alpha*C
      = 1/n - C

**The alpha terms cancel completely. B = 1/n - C, independent of alpha.**

This is verified to machine precision for all primes tested and proved exactly with rational arithmetic:

| p | n | C | 1/n | B = 1/n - C | B/C |
|---|---|---|-----|-------------|-----|
| 2 | 2 | 0.5000 | 0.5000 | 0 | 0 |
| 3 | 4 | 0.2778 | 0.2500 | -0.0278 | -0.100 |
| 13 | 58 | 0.0276 | 0.0172 | -0.0104 | -0.375 |
| 29 | 270 | 0.00693 | 0.00370 | -0.00323 | -0.466 |
| 53 | 882 | 0.00237 | 0.00113 | -0.00123 | -0.521 |
| 97 | 2902 | 7.94e-4 | 3.45e-4 | -4.49e-4 | -0.566 |
| 199 | 12152 | 2.12e-4 | 8.23e-5 | -1.29e-4 | -0.611 |
| 503 | 77200 | 3.77e-5 | 1.30e-5 | -2.47e-5 | -0.656 |
| 997 | 302646 | 1.04e-5 | 3.30e-6 | -7.14e-6 | -0.684 |

**B < 0 for all N >= 3.** B = 0 only at N = 2 (where F_2 = {1/2, 1/1}).

---

## 4. Why Cauchy-Schwarz Cannot Work

The Cauchy-Schwarz approach tries to prove |S| <= (alpha/2)*C.

But we showed S = 1/(2n) - C*(1+alpha)/2 ~ -C/2, so |S| ~ C/2.

Meanwhile alpha ~ 1/n (empirically alpha*n stays bounded), so (alpha/2)*C ~ C/(2n).

The ratio |S| / ((alpha/2)*C) ~ n -> infinity.

**The error term |S| is order C, not o(C).** Cauchy-Schwarz gives |S| <= sqrt(sum D_err^2) * sqrt(C), which is even weaker.

### Scaling of key ratios:

| p | alpha*n | |S/C| | (alpha/2) | |S/C|/(alpha/2) |
|---|---------|-------|-----------|-----------------|
| 13 | 3.64 | 0.219 | 0.031 | 7.0 |
| 97 | 4.92 | 0.284 | 8.5e-4 | 334 |
| 997 | 9.77 | 0.342 | 1.6e-5 | 21189 |

---

## 5. What This Means

### The decomposition B = alpha*C + 2*S is a **dead end** for proving B >= 0.

The two terms alpha*C and 2*S cancel to give B = 1/n - C, which is:
- Exactly computable
- Negative for N >= 3
- Converging to B/C -> -1 as N -> infinity (since nC -> infinity)

### For ΔW theory:
If B = 1/n - C enters a formula where we need B >= 0, then either:
1. **The formula is wrong** -- recheck the derivation of B
2. **B >= 0 is not needed** -- perhaps a weaker condition suffices
3. **A different decomposition is needed** -- one where the cross-term is genuinely small

### The identity B = 1/n - C is itself a clean result:
- It's unconditional (no RH, no asymptotics)
- It holds for ALL Farey sequences F_N, not just prime N
- It connects the second moment of gaps (C) to the count (1/n) in a sharp way

---

## 6. Growth of nC (for reference)

The product nC = n * sum(delta^2) grows slowly:

| p | n | nC |
|---|---|-----|
| 7 | 18 | 1.39 |
| 13 | 58 | 1.60 |
| 53 | 882 | 2.09 |
| 199 | 12152 | 2.57 |
| 997 | 302646 | 3.16 |

Empirically nC ~ c * log(N) for some constant c. This is consistent with the known asymptotics for sum of squared Farey gaps.

Since B/C = 1/(nC) - 1, and nC -> infinity, we get B/C -> -1 monotonically.

---

## 7. Proof Summary (Self-Contained)

**Theorem.** For the Farey sequence F_N in (0,1] with n fractions, let D_k = k/n - f_k, delta_k = f_k - f_{k-1}, C = sum(delta_k^2), and let alpha be the least-squares slope of D vs (f - 1/2). Define D_err = D - alpha*(f - 1/2) and B = alpha*C + 2*sum(D_err * delta). Then:

    B = 1/n - C

for all N >= 1.

**Proof.** Three identities:
1. sum(D_k) = 0 by Farey symmetry.
2. sum(D_k * delta_k) = 1/(2n) - C/2 by telescoping D_n^2 - D_0^2 = 0 and (1).
3. sum((f_k - 1/2) * delta_k) = C/2 by algebraic manipulation of sum(f * delta).

Then S = sum(D * delta) - alpha * sum((f-1/2) * delta) = [1/(2n) - C/2] - alpha*C/2, and B = alpha*C + 2*S = alpha*C + 1/n - C - alpha*C = 1/n - C. QED

**Corollary.** B < 0 for all N >= 3, since C > 1/n whenever n >= 3.

---

## 8. Next Steps

The Cauchy-Schwarz decorrelation approach is definitively ruled out. To make progress on B >= 0 (if that's actually needed), one must:

1. **Re-examine whether B >= 0 is the correct target.** Perhaps the ΔW analysis needs a different decomposition where B is defined differently.
2. **Look for cancellation within sum(D_err * delta) at a finer scale.** The bulk average is -C/2, but there may be sub-sums with better behavior.
3. **Abandon the linear regression decomposition** and work directly with D and delta, using the exact identity sum(D * delta) = 1/(2n) - C/2.
