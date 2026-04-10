# Independent Verification: K Bound + Dress-El Marraki for GAP 2

## Date: 2026-03-29
## Reviewer: Independent verification agent
## Status: DOES NOT CLOSE GAP 2 RIGOROUSLY (two unproved steps remain)

---

## 0. Executive Summary

The proposed chain is:

    |1 - D'/A'| <= 10 * |M(p)|/p <= 10/2360 = 0.00424    (for p >= 617,973)
    C/A >= 0.59/log(p) >= 0.59/log(617973) = 0.044
    Since 0.00424 < 0.044, the bypass C/A > |1 - D'/A'| closes.

**Arithmetic check: CORRECT.** The numbers 0.00424 and 0.044 are verified:
- 10/2360 = 0.004237...  (matches 0.00424)
- 0.59/log(617973) = 0.59/13.334 = 0.04425  (matches 0.044)
- 0.00424 < 0.044 with a 10.4x margin

**Circularity check: NO CIRCULARITY DETECTED.** The K bound uses Fourier
analysis of Farey sequences (Franel sums, Poisson summation), while
Dress-El Marraki uses zero-free region bounds. These are independent inputs.

**Rigor check: TWO GAPS REMAIN.** The chain fails to be a complete proof
because of two unproved ingredients:

| Step | Claimed | Proved? | Gap |
|------|---------|---------|-----|
| K <= 10 | |1-D'/A'| <= 10|M(p)|/p | NO -- empirical (p <= 499) | Constant-tracking in Fourier analysis |
| Dress-El Marraki | |M(x)| <= x/2360 for x >= 617,973 | YES | Published theorem (1993) |
| C/A >= 0.59/log(p) | Bypass condition | NO -- empirical (p <= 10,000) | Proved bound is 0.023/log^2(p), 25x too weak |

---

## 1. Detailed Verification of Each Step

### Step 1: K <= 10 in |1 - D'/A'| <= K * |M(p)|/p

**What the proof document (K_BOUND_PROOF.md) actually establishes:**

PROVED (rigorously):
- The algebraic decomposition: D'/A' - 1 = (S_virt/A' - 1) + 2X_cross/A' + S_kp/A'
- The Franel exponential sum identity: sigma_p = 1 + M(p-1), verified for p <= 200
- S_kp/A' = O(1/p) with explicit constants
- The STRUCTURE connecting the aliasing error to M(p) via Franel sums

NOT PROVED (empirical or incomplete):
- The bound |S_virt/A' - 1| <= 7|M(p)|/p. The proof attempts three approaches:
  1. Riemann sum vs integral: FAILS (gives S_virt/A' ~ 1/2, contradicting data)
  2. Direct interpolation: encounters O(p) error that is not controlled
  3. Truncated Poisson: identifies correct mechanism but does NOT track constants
     through to get K_1 = 7 explicitly. The document says "gets the right structure
     but the constant K_1 = 7 is only justified by empirical max = 6.16 plus margin."
- The bound |2X_cross/A'| <= 2|M(p)|/p: uses Kloosterman-Weil, asserted not derived
- The total K = 7 + 2 + 1 = 10 is a sum of empirical upper bounds with safety margin

**Computational support:** K_max = 6.16 at p = 359 over all primes p <= 499.
The K = 10 claim provides 62% margin above all observed values. This is strong
empirical evidence but not a proof.

**Assessment:** The proof identifies the correct algebraic/analytic mechanism but
does not close the constant-tracking. This gap appears closable with careful work
-- the structure is there, only the bookkeeping of explicit constants remains.

### Step 2: Dress-El Marraki |M(x)| <= x/2360 for x >= 617,973

**This is a published theorem.** Dress and El Marraki (1993) proved this
unconditionally. It has been superseded by stronger results:
- Cohen, Dress & El Marraki (2007): |M(x)| <= x/4345 for x >= 2,160,535
- Ramare (2013): |M(x)| <= 0.013x/log(x) for x >= 1,078,853

**No issues here.** The constant 2360 and threshold 617,973 are correct.

Note on M(p) vs M(p-1): The Franel identity gives sigma_p = 1 + M(p-1).
Since M(p) = M(p-1) - 1 (as mu(p) = -1 for prime p), we have
|M(p-1)| = |M(p)+1| <= |M(p)| + 1. For p >= 617,973, the additive 1
is negligible compared to |M(p)| <= p/2360 ~ 262. This is fine.

### Step 3: C/A >= 0.59/log(p) (THE CRITICAL GAP)

**This is NOT proved.** The proof document explicitly states:

- Empirical: min(C/A * log(p)) = 0.59 over M(p) <= -3 primes up to p = 10,000
- The PROVED lower bound is C/A >= 0.023/log^2(p), which comes from:
  - C' >= 0.035 * p^2 (proved)
  - A' ~ 6*C_W*p^2/pi^2 (with C_W the Farey discrepancy constant)
  - But C_W ~ 0.6 (empirical), and the proved bound uses a weaker estimate

**The proved bound DOES NOT SUFFICE:**

At p = 617,973:
- Proved C/A >= 0.023/log^2(617973) = 0.023/177.8 = 0.000129
- Needed: C/A > |1-D'/A'| >= 10/2360 = 0.00424
- 0.000129 < 0.00424: THE BYPASS FAILS WITH PROVED CONSTANTS

The empirical C/A ~ 0.59/log(p) is roughly 25*log(p) times larger than the
proved bound 0.023/log^2(p). Closing this gap requires proving that C_W(N)
is bounded above (or at least grows slower than log(N)), which is itself a
non-trivial statement about Farey discrepancy.

---

## 2. The Bypass Inequality: What IS True

### With all empirical constants (not a proof, but informative):

For p >= 617,973:
    |1 - D'/A'| <= 10 * (1/2360) = 0.00424
    C/A >= 0.59/log(617973) = 0.044
    Margin: 10.4x

This is a very comfortable margin. Even if the true K were 50 (far above
the empirical 6.2), the bypass would still hold:
    50/2360 = 0.0212 < 0.044

### With proved constants only:

    |1 - D'/A'| <= (something) * |M(p)|/p   [K not proved]
    C/A >= 0.023/log^2(p)                    [too weak]

Neither ingredient suffices. The chain breaks at Step 3.

### Using stronger Mertens bounds:

With Cohen-Dress-El Marraki (2007), |M(x)| <= x/4345 for x >= 2,160,535:
    |1-D'/A'| <= 10/4345 = 0.00230
    C/A >= 0.59/log(2160535) = 0.0405
    Margin: 17.6x (even better)

With Ramare (2013), |M(x)| <= 0.013x/log(x) for x >= 1,078,853:
    |1-D'/A'| <= 0.13/log(p)
    C/A >= 0.59/log(p)
    Margin: 0.59/0.13 = 4.5x (independent of p!)

The Ramare version is cleaner because both sides scale as 1/log(p), so
the comparison reduces to: 0.13 < 0.59, which is manifestly true.
But 0.59 is still the empirical constant.

---

## 3. What Would Make This Rigorous

### Path 1: Prove C/A >= c/log(p) with c > 0.13

This requires proving C_W(N) <= constant (or C_W(N) = O(1)). The current
proved bound gives C/A ~ 1/log^2(p); need to improve by a factor of log(p).

The key issue: C_W(N) = N * W(F_N) measures the integrated squared discrepancy
of the Farey sequence. While C_W appears empirically bounded (~0.5-0.7), proving
this requires understanding the L^2 norm of the Farey counting function error,
which connects to the distribution of Farey fractions at ALL scales.

### Path 2: Prove K analytically

The K bound proof structure is:
1. Decompose D'/A' - 1 into aliasing + cross + quadratic terms
2. The aliasing connects to sigma_p = 1 + M(p-1) via Franel
3. Each term is bounded by C_i * |M(p)|/p

To make this rigorous, one must:
- Track constants through the Poisson summation formula for D_N^2
- Get explicit Kloosterman-Weil bounds for the cross term
- Handle the m >= 2 aliasing contributions (currently bounded as geometric series)

This appears feasible but tedious. The main difficulty is the factor-of-2
identity (S_virt ~ 2p * old_D_sq / n), which the proof recognizes but
does not derive from first principles.

### Path 3: Computational verification (RECOMMENDED)

Verify the sign theorem directly for ALL primes up to 1,078,853 (or whatever
threshold is needed). The existing C code runs at O(p) per prime; covering
~85,000 primes up to 1.1M requires ~10^11 operations, feasible in minutes
on modern hardware.

Then the analytical bound only needs to cover p > 1,078,853, where the
Ramare bound |M(p)|/p <= 0.013/log(p) is available. But you STILL need
C/A >= c/log(p) analytically for the asymptotic range.

### Path 4: Avoid C/A entirely

If you can prove |1 - D'/A'| < 1 for all sufficiently large p, then
D'/A' > 0, which means D' and A' have the same sign. Combined with the
four-term decomposition structure, this might give DeltaW information
without needing the C/A bypass.

With Dress-El Marraki: |1 - D'/A'| <= 10/2360 = 0.00424 < 1. This would
give D'/A' in (0.996, 1.004), meaning D' ~ A'. If you can show the sign
theorem follows from D' ~ A' without needing C/A, this path avoids the
hardest gap entirely. Worth exploring.

---

## 4. Verification of Specific Constants

| Quantity | Claimed | Verified | Status |
|----------|---------|----------|--------|
| 10/2360 | 0.00424 | 0.004237 | CORRECT |
| 0.59/log(617973) | 0.044 | 0.04425 | CORRECT |
| 0.00424 < 0.044 | bypass holds | 0.00424 < 0.04425 | CORRECT |
| K_max <= 6.2 (p <= 499) | empirical | per K_BOUND_PROOF appendix | VERIFIED |
| sigma_p = 1 + M(p-1) | Franel identity | standard (Ramanujan sums) | CORRECT |
| Dress-El Marraki (1993) | |M(x)| <= x/2360, x >= 617,973 | published | CORRECT |
| C/A >= 0.59/log(p) | empirical | to p = 10,000 only | NOT PROVED |
| Proved C/A | >= 0.023/log^2(p) | per proof document | TOO WEAK |

---

## 5. Conclusion

**The proposed chain is NOT rigorous.** The arithmetic is correct, the Franel
identity is standard, Dress-El Marraki is published, and there is no circularity.
However, two ingredients remain unproved:

1. **K <= 10**: Empirically verified (K_max = 6.16 for p <= 499) but the
   analytical constant-tracking has gaps. The proof identifies the correct
   mechanism (Poisson aliasing + Franel exponential sums) but does not close
   the constants. Assessment: LIKELY PROVABLE with careful work.

2. **C/A >= 0.59/log(p)**: Empirically verified for p <= 10,000 but the
   proved lower bound is C/A >= 0.023/log^2(p), which is ~25*log(p) times
   weaker. Assessment: HARD. Requires proving C_W(N) = O(1), which is a
   substantial analytic number theory result about Farey discrepancy.

**The fatal gap is #2.** Even if K <= 10 is proved, the bypass C/A > |1-D'/A'|
fails with proved constants because 0.000129 < 0.00424.

**Recommended next steps:**
1. Extend computational verification of the sign theorem to p = 1,078,853
   (feasible in minutes). This eliminates the need for C/A bounds in the
   computational range.
2. Focus analytical effort on proving C_W(N) = O(1) or C/A >= c/log(p) with
   explicit c. This is the bottleneck for the asymptotic argument.
3. Alternatively, explore whether D'/A' ~ 1 (from the K bound + Dress-El Marraki)
   suffices for the sign theorem WITHOUT needing C/A at all.
