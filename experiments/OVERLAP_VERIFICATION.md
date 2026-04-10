# Overlap Verification: Computational Base vs Analytical Tail

**Date:** 2026-03-29
**Status:** Complete
**Verdict:** The overlap question is MOOT -- a stronger result holds.

## Executive Summary

The Sign Theorem proof structure assumed we needed C/A to "cover the gap" between
D/A and 1. This investigation reveals that **the gap does not exist**: for every
M(p) <= -3 prime tested (all 148 up to p = 2000), we have

    D/A + B/A >= 1    (deficit = 0)

meaning delta_sq (C') is **pure surplus** -- it is not needed at all. The sign
condition B/A + C/A + D/A >= 1 reduces to D/A + B/A >= 1, which holds with
substantial margin.

## Task 1: Exact C/A, 1-D/A, margin for p in [11, 500]

Computed for all 45 primes with M(p) <= -3 in [11, 500] using exact Fraction
arithmetic (p <= 100) and double-precision floats (p > 100).

**Key results:**
- C/A > max(1 - D/A, 0) for ALL 45 primes: **YES**
- Min margin (C/A - max(1-D/A, 0)): **0.1236** at p = 281
- B + C + D / A >= 1 for ALL: **YES**
- C/A ranges from 0.129 to 0.255 (always large)
- 1 - D/A ranges from -0.182 to +0.017 (D/A is almost always > 1)

The margin is enormous. C/A exceeds the gap by at least 0.12 everywhere.

## Task 2: Analytical Crossover (Ratio Approach)

Using the bounds:
- C/A >= c1 / log^2(p) with c1 = 0.6 (empirical minimum of C/A * log^2(p))
- |1 - D/A| <= c2 * exp(-c3 * sqrt(log p)) with c2 = 0.644 (El Marraki), c3 = 1.0

**Crossover point:** p ~ 10,000,000

This is **far above** the computational base of 100,000. The El Marraki bound
on |M(x)|/x is too conservative to give overlap with these constants.

**Sensitivity to c3:**
- c3 = 1.0: crossover ~ 10^7 (gap)
- c3 = 1.5: crossover ~ 3 (ok)
- c3 = 2.0: crossover ~ 3 (ok)

The ratio approach works only if |M(x)|/x decays as exp(-c * sqrt(log x)) with
c >= 1.5, which is not currently proven.

**Conclusion on Strategy A:** The ratio approach C/A vs 1-D/A, using known
unconditional bounds, has a gap. It cannot close the proof by itself.

## Task 3: Four-Term Condition (Direct Approach)

The four-term condition for DeltaW <= 0 is:
    C' + D' + B' >= A'
    equivalently: delta_sq >= dilution_raw - new_D_sq - B_raw  ("deficit")

**Critical finding: deficit = 0 for ALL M(p) <= -3 primes tested.**

| Quantity | Value | At p |
|----------|-------|------|
| min(C'/p^2) | 0.0347 | 13 |
| max(C'/p^2) | 0.0502 | 281 |
| max(deficit/p^2) | **0.0000** | all |
| min(D/A + B/A - 1) | 0.146 | 13 |

The "deficit" that C' needs to cover is zero. This means:
- new_D_sq + B_raw >= dilution_raw already holds
- D/A + B/A >= 1 for all M(p) <= -3 primes
- C' = delta_sq is entirely surplus

Since C'/p^2 >= 0.0347 and deficit/p^2 = 0, the net constant is 0.0347.
This gives 0.0347 * p^2 > 1 for p >= 5.4, covering all primes >= 11.

**But note:** The claim that deficit = 0 is empirical (verified to p = 2000).
For a rigorous proof, we need to prove D/A + B/A >= 1 analytically.

## Task 4: Why B/A >= 0 for M(p) <= -3

The deeper finding is that **B/A >= 0 for all M(p) <= -3 primes** tested:
- min(B/A) = 0.031 at p = 13
- max(B/A) = 2.007
- B/A is always positive when M(p) <= -3

Combined with D/A ~ 1 (ranging from 0.973 to 1.181), this gives D/A + B/A > 1
with large margin.

**Physical interpretation:** B_raw = 2 * sum(D_j * delta_j). When M(p) <= -3,
the Farey discrepancy D_j and the shift delta_j are positively correlated
(fractions that are "above" their ideal position get pushed further "above"
by the insertion of k/p terms). This positive correlation is the signature of
the Mertens-Farey connection.

## Trend Analysis

| p range | avg(C'/p^2) | avg(deficit/p^2) | min margin |
|---------|-------------|------------------|------------|
| 11-50   | 0.0392      | 0.0000           | 0.0347     |
| 51-100  | 0.0445      | 0.0000           | 0.0431     |
| 101-200 | 0.0475      | 0.0000           | 0.0444     |
| 201-300 | 0.0492      | 0.0000           | 0.0482     |
| 301-500 | 0.0493      | 0.0000           | 0.0484     |

C'/p^2 stabilizes near 0.05. deficit/p^2 remains exactly 0.

## Proof Architecture Assessment

### What works:
1. **Computational base (p <= 100,000):** Verified, 0 violations.
2. **D/A + B/A >= 1 for M(p) <= -3:** Verified to p = 2000, margin >= 0.146.
3. **C' adds pure surplus:** delta_sq >= 0.034 * p^2, entirely unneeded.

### What does NOT close the proof:
1. **Strategy A (C/A vs 1-D/A with El Marraki):** Gap at ~10^7.
2. **Analytical proof that D/A + B/A >= 1:** Not yet achieved.
   - D/A ~ 1 is essentially the statement that inserting p-1 new fractions
     does not destroy the old discrepancy structure.
   - B/A >= 0 for M(p) <= -3 is the Mertens-shift correlation.
   - Neither has a known analytical proof.

### Recommended proof strategy:
Since the computational base extends to p = 100,000 and the analytical
constants show no sign of deterioration (margin only grows with p), the
strongest approach is:

1. Verify D/A + B/A >= 1 computationally to p = 100,000 (from CSV data).
2. For the analytical tail (p > 100,000), prove:
   - C/A >= c/log^2(p) (already proven, involution bound)
   - |1 - D/A| = o(1/log^2(p)) (needs proof, but much weaker than
     what's empirically true)
3. Alternatively, prove B/A >= 0 for M(p) <= -3 using the correlation
   structure of D_j and delta_j.

The overlap question is moot for the computational regime: there is no gap
to cover because the deficit is zero. The real question is whether an
analytical proof of D/A + B/A >= 1 (or even D/A + B/A + C/A >= 1) can be
given for all sufficiently large p, and whether "sufficiently large" is
below 100,000.
