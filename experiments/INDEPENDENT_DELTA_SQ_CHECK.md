# Independent Verification: Claim Sigma delta^2 = N^2/(2 pi^2) + O(N log N)

**Date:** 2026-03-29
**Verifier:** Independent agent with NO prior context
**Method:** Exact Fraction arithmetic in Python, no floating-point until final display
**Status:** PARTIALLY SUPPORTED -- leading term plausible, not proven

---

## 1. Setup and Definitions

For prime p, N = p - 1. The Farey sequence F_N consists of all a/b with 0 <= a <= b <= N, gcd(a,b) = 1.

For each a/b in F_N with b > 1, define:

    delta(a/b) = (a - (p * a mod b)) / b

The map sigma_p: a -> (p * a mod b) is a permutation of the coprime residues mod b (since p is prime and gcd(p,b) = 1 for b < p).

**Claim:** Sum_{a/b in F_N, b>1} delta(a/b)^2 = N^2/(2 pi^2) + O(N log N)

---

## 2. Exact Computation Results

All sums computed with Python `fractions.Fraction` (exact rational arithmetic). Converted to float only for display.

| p | N | Sum delta^2 (exact float) | Sum/N^2 | 1/(2pi^2) | err/(N log N) |
|---:|---:|---:|---:|---:|---:|
| 11 | 10 | 2.9511 | 0.02951058 | 0.05066059 | -0.091853 |
| 13 | 12 | 5.8710 | 0.04077080 | 0.05066059 | -0.047759 |
| 17 | 16 | 9.4134 | 0.03677127 | 0.05066059 | -0.080152 |
| 23 | 22 | 17.3663 | 0.03588069 | 0.05066059 | -0.105194 |
| 29 | 28 | 31.7377 | 0.04048181 | 0.05066059 | -0.085531 |
| 37 | 36 | 62.4754 | 0.04820631 | 0.05066059 | -0.024656 |
| 53 | 52 | 121.1735 | 0.04481267 | 0.05066059 | -0.076961 |
| 97 | 96 | 451.1372 | 0.04895152 | 0.05066059 | -0.035946 |
| 199 | 198 | 1894.8220 | 0.04833236 | 0.05066059 | -0.087172 |
| 307 | 306 | 4602.9826 | 0.04915826 | 0.05066059 | -0.080319 |
| 503 | 502 | 12290.3026 | 0.04877027 | 0.05066059 | -0.152597 |
| 997 | 996 | 49782.6445 | 0.05018331 | 0.05066059 | -0.068857 |

**Observation:** Sum/N^2 is ALWAYS BELOW 1/(2pi^2), approaching it slowly from below. At p=997 the ratio is 0.0502, still 1% below the target 0.0507.

---

## 3. Sanity Check: p = 11 term-by-term

For p=11, N=10, every term was verified individually. Examples:
- a/b = 1/3: p*a mod b = 11 mod 3 = 2, delta = (1-2)/3 = -1/3, delta^2 = 1/9
- a/b = 1/5: p*a mod b = 11 mod 5 = 1, delta = 0 (since 11 = 1 mod 5)
- a/b = 1/7: p*a mod b = 11 mod 7 = 4, delta = (1-4)/7 = -3/7, delta^2 = 9/49

For b dividing (p-1) = 10 (i.e., b = 2, 5, 10), sigma_p is the identity, so all delta = 0. This is expected since p = 1 mod b means multiplication by p is trivial.

---

## 4. Theoretical Decomposition

### Key identity (verified algebraically):

Since sigma_p permutes coprime residues mod b, we have Sum (sigma(a))^2 = Sum a^2. Therefore:

    Sum_{a coprime to b} delta(a/b)^2 = (2/b^2) [Sum a^2 - T_b]

where T_b = Sum_a a * sigma_p(a) = Sum_a a * (p*a mod b).

### Random permutation model:

If sigma were a RANDOM permutation of coprime residues mod b:

    E[T_b] = S_b^2 / phi(b)

where S_b = Sum_{gcd(a,b)=1, 1<=a<b} a = b * phi(b) / 2.

So E[T_b] = b^2 * phi(b) / 4.

For the sum of squares: Sum a^2 is approximately b^2 * phi(b) / 3 for large b.

Therefore the expected contribution per denominator b is:

    (2/b^2)[b^2 phi(b)/3 - b^2 phi(b)/4] = (2/b^2)(b^2 phi(b)/12) = phi(b)/6

Summing: E[Sum delta^2] ~ Sum_{b=2}^{N} phi(b)/6 ~ (1/6)(3N^2/pi^2) = N^2/(2 pi^2)

using the classical result Sum_{b=1}^{N} phi(b) = 3N^2/pi^2 + O(N log N).

**This derivation is CORRECT and the leading term N^2/(2pi^2) is confirmed for the random model.**

---

## 5. Random Model vs Actual: Comparison

| p | N | actual/N^2 | random/N^2 | 1/(2pi^2) | gap % |
|---:|---:|---:|---:|---:|---:|
| 11 | 10 | 0.02951058 | 0.04270767 | 0.05066059 | -30.90% |
| 37 | 36 | 0.04820631 | 0.04954991 | 0.05066059 | -2.71% |
| 97 | 96 | 0.04895152 | 0.05054798 | 0.05066059 | -3.16% |
| 199 | 198 | 0.04833236 | 0.05071286 | 0.05066059 | -4.69% |
| 503 | 502 | 0.04877027 | 0.05070862 | 0.05066059 | -3.82% |
| 997 | 996 | 0.05018331 | 0.05067618 | 0.05066059 | -0.97% |

**Key finding:** The random model converges perfectly to N^2/(2pi^2). The actual sum is systematically BELOW the random model, but the gap shrinks (from 31% at p=11 to 1% at p=997).

The gap (actual - random) divided by N log N is O(1), suggesting the deviation is O(N log N), absorbed into the error term.

---

## 6. Part 5: Is Sum(actual deficit - expected deficit)/b^2 = o(N^2)?

| p | N | Sum(diff)/b^2 | |diff|/N^2 | |diff|/N log N |
|---:|---:|---:|---:|---:|
| 11 | 10 | -1.3197 | 0.01320 | 0.0573 |
| 97 | 96 | -14.7130 | 0.00160 | 0.0336 |
| 199 | 198 | -93.3250 | 0.00238 | 0.0891 |
| 503 | 502 | -487.3780 | 0.00193 | 0.0784 |
| 997 | 996 | -488.9320 | 0.00049 | 0.0071 |

**|diff|/N^2 is clearly decreasing** (0.013 -> 0.0005), so the answer is YES: the deviation between actual and random model is o(N^2).

However, |diff|/N log N does NOT converge to zero -- it fluctuates around 0.05-0.09, suggesting the deviation is Theta(N log N), not o(N log N).

---

## 7. Verdict

### Is the claim Sum delta^2 = N^2/(2pi^2) + O(N log N) TRUE?

**PARTIALLY SUPPORTED with caveats:**

1. **Leading term N^2/(2pi^2) is correct.** This follows rigorously from the random permutation model: if multiplication by p in (Z/bZ)* behaves like a random permutation, the leading term is exactly N^2/(2pi^2).

2. **The random model itself satisfies the claim exactly:** Random Sum = N^2/(2pi^2) + O(N log N), provably, since it reduces to the totient summatory function.

3. **The actual sum approaches N^2/(2pi^2) from below.** At p=997, the ratio is 99.1% of the target. The convergence is slow and non-monotone.

4. **The error term is negative and appears to be O(N log N).** The ratio error/(N log N) fluctuates but does not blow up, consistent with O(N log N).

5. **However, the claim is NOT PROVEN.** The step from "random model predicts X" to "actual sum equals X + O(N log N)" requires showing that multiplication by p is sufficiently "random" in a precise sense. This is a number-theoretic statement about the distribution of p * a mod b that has NOT been established here.

6. **The deviation (actual - random) is o(N^2) but appears to be Theta(N log N),** meaning it is absorbed into the error term but is a nontrivial correction.

### Classification:
- The random-model derivation: **CORRECT** (rigorous)
- Sum delta^2 ~ N^2/(2pi^2) as leading asymptotics: **EMPIRICALLY SUPPORTED**
- The O(N log N) error bound: **PLAUSIBLE BUT UNPROVEN** -- needs analytic number theory
- Overall status: **Empirical conjecture, not a theorem**
