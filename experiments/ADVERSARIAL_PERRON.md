# Adversarial Audit: Perron Integral Derivation for T(N) -- SECOND PASS

## Date: 2026-03-31
## Auditor: Hostile Referee (independent agent, adversarial frame)
## Source document: PERRON_INTEGRAL_T.md (2026-03-30)
## Previous audit: ADVERSARIAL_PERRON.md (2026-03-30) -- missed the +2 constant error
## Verdict: ONE ARITHMETIC ERROR FOUND (constant term +2.0 overcounting). Core claims SURVIVE.

---

## Executive Summary

The Perron integral derivation is **mostly correct** but contains one concrete arithmetic error in the explicit formula constant (Section 4.1), plus several presentation issues. The phase prediction (5.208 vs observed 5.28) and the density-1/2 claim are unaffected by the error. The Rubinstein-Sarnak P(T>0) predictions are slightly affected but remain qualitatively valid.

**The previous audit (2026-03-30) missed this error.** That audit rated the document "no fatal flaws found." This second pass found a clear +2.0 arithmetic overcounting, confirmed by brute-force computation.

### Scorecard

| Claim | Verdict | Details |
|-------|---------|---------|
| Perron integral representation | CORRECT | Dirichlet series identity verified analytically and by brute force |
| Double pole residue at s=0 | CORRECT (formula) | Res = -2(logN + gamma) + 2log(2pi). Verified by contour integration to 6+ digits |
| Numerical residue values (Sec 2.3) | MINOR ERROR | N=10^7: document says -29.728, correct value is -29.715 (0.04% off, rounding) |
| Zeta zero coefficients c_k (Sec 3.2) | CORRECT | All 10 values verified independently to 5 significant figures |
| c_1 value | CORRECT | -0.00149 - 0.04851i, |c_1| = 0.04853, arg(c_1) = -1.6016 |
| d_1 value | CORRECT | -0.01089 - 0.08847i, |d_1| = 0.08914, arg(d_1) = -1.6933 |
| Phase prediction 5.208 | CORRECT | gamma_1 * log(2) - arg(d_1) = 5.2076, matches to 4 figures |
| **Explicit formula constant (Sec 4.1)** | **ERROR (+2.0)** | Document claims 6.52 for M(N)=-2; correct value is 4.52 |
| Oscillatory amplitude 2|c_1| | CORRECT | 0.09706, document rounds to 0.0971 |
| sigma from 20 zeros | CORRECT | sigma^2 = 0.01018, sigma = 0.1009 |
| Density 1/2 claim | CORRECT (conditional) | Follows from R-S framework under GRH+LI; argument is sound |
| P(T>0) at N=10^7 | APPROXIMATELY CORRECT | Gaussian approx gives 0.46-0.47 regardless of which constant; matches observation |

---

## Detailed Findings

### 1. Perron Integral Representation (Section 1) -- CORRECT

The Dirichlet series identity is standard and correct:

- mu(n) has Dirichlet series 1/zeta(s)
- The arithmetic function 1/n has Dirichlet series zeta(s+1)
- The Dirichlet convolution h(n) = sum_{d|n} mu(d)/(n/d) has series zeta(s+1)/zeta(s)
- Perron's formula gives sum_{n<=N} h(n) = (1/2pi i) int N^s zeta(s+1)/(s zeta(s)) ds

Verified by brute force: the hyperbolic sum sum_{km<=N} mu(k)/m equals sum_{m=1}^N M(floor(N/m))/m (tested at N=1000, exact match to 10 digits).

**No issues found.**

### 2. Double Pole Residue (Section 2) -- CORRECT

The Laurent expansion verified step by step:

- zeta(s+1) = 1/s + gamma + gamma_1 s + ... : standard
- zeta(s) = -1/2 + zeta'(0) s + ... where zeta'(0) = -log(2pi)/2 : verified numerically
- 1/zeta(s) = -2 + 2 log(2pi) s + ... : verified by computing f'(0) = -zeta'(0)/zeta(0)^2 = 2 log(2pi) = 3.6758. Also verified by numerical difference quotient at h = 10^{-15}.

The residue at s = 0:

    Res_{s=0} F(s) = -2(log N + gamma) + 2 log(2pi) = -2 log N + 2.5213

Verified by numerical contour integration (circular contour, radius 10^{-4}) at N = 1000, 243798, 10^7. All match to 4+ decimal places.

The document's specific value at N = 10^7 has a minor rounding discrepancy (claims -29.728, correct is -29.715), but this is inconsequential.

**No substantive issues.**

### 3. ARITHMETIC ERROR: Constant Term in Section 4.1

**This is the main finding of the audit.**

Section 4.1 states:

    T(N) = [-2 log(N) + 2 - 2 gamma + 2 log(2 pi)] + sum_rho 2 Re[c_rho N^rho] - M(N) + O(1)

And for M(N) = -2:

    T(N) = -2 log(N) + 6.5213 + 0.0971 sqrt(N) cos(14.1347 log(N) - 1.6016) + ...

**The correct formula is:**

    T(N) = [-2 log(N) - 2 gamma + 2 log(2 pi)] + sum_rho 2 Re[c_rho N^rho] - M(N) + O(1)

Note: there is NO "+2" inside the brackets. The Perron residue at s = 0 is exactly -2 log(N) - 2 gamma + 2 log(2pi), with NO additional constant.

**Proof:** The Laurent expansion of F(s) = N^s zeta(s+1)/(s zeta(s)) near s = 0:

    F(s) = (1/s)(1 + s log N + ...)(1/s + gamma + ...)(- 2 + 2 log(2pi) s + ...)
    = (-2/s^2) + (-2 log N - 2 gamma + 2 log(2pi))/s + O(1)

The coefficient of 1/s (i.e., the residue) is -2 log N - 2 gamma + 2 log(2pi). There is no "+2" term.

For M(N) = -2, the correct constant is:

    -2 gamma + 2 log(2pi) + 2 = -1.1544 + 3.6758 + 2 = **4.5214**

NOT 6.5213. The document overcounts by exactly +2.0.

**Confirmed by brute force:** At N = 1000, the Perron formula (residue + 50 zeta zeros) gives F(1000) = -9.088, compared to the exact value F(1000) = -9.193. With M(1000) = 2, T(1000) = -11.193 actual vs -11.088 predicted. The predictions are consistent with a constant of 4.52, NOT 6.52.

**Root cause:** The author most likely computed -M(N) = +2 and also erroneously added a "+2" to the Perron residue, double-counting one factor of 2.

**Impact assessment:**
- Phase prediction: UNAFFECTED (depends only on oscillatory terms)
- Density 1/2: UNAFFECTED (threshold delta(N) -> 0 regardless)
- P(T > 0) finite-N: SLIGHTLY affected. The threshold delta(N) = (2 log N - C)/sqrt(N) changes by 2/sqrt(N), which at N = 10^7 is 6.3 x 10^{-4}, shifting P(T > 0) by approximately 0.003. Qualitative conclusions unchanged.

**Recommended fix:** Remove the "+2" from Section 4.1 brackets. The general formula should be:

    T(N) = Res_{s=0} + sum_rho Res_{rho} - M(N) + O(1)
         = [-2 logN - 2 gamma + 2 log(2pi)] + [oscillatory] - M(N) + O(1)

For M(N) = -2: T(N) = -2 logN + 4.52 + 0.0971 sqrt(N) cos(14.13 logN - 1.60) + ...

### 4. Zeta Zero Coefficients (Section 3) -- CORRECT

All 10 coefficients c_k = zeta(rho_k + 1)/(rho_k zeta'(rho_k)) verified independently using mpmath at 50-digit precision. All |c_k| and arg(c_k) match to the precision given in the table. The formula for the residue at a simple zero of zeta in the denominator is standard. **No issues.**

### 5. Phase Prediction (Section 5) -- CORRECT

- gamma_1 log(2) mod 2pi = 3.5143 : verified
- arg(d_1) = -1.6933 : verified (d_1 = 1/(rho_1 zeta'(rho_1)))
- Predicted phase = 3.5143 - (-1.6933) = 5.2076 : verified
- Observed: 5.28, discrepancy 0.072 rad (1.1%)

**Presentation issue:** Section 5.4 is stream-of-consciousness with a "Wait -- more carefully:" in the middle. The reconciliation between the direct Perron prediction (1.60) and the M(N/2) prediction (5.21) is physically reasonable but needs a cleaner write-up.

### 6. Density 1/2 Claim (Section 6) -- CORRECT under GRH + LI

The Rubinstein-Sarnak framework applies correctly:

1. The explicit formula has the standard form: constant drift + sum of N^{rho} oscillations
2. Under LI (Linear Independence of zeta zero ordinates), the phases gamma_k log N become equidistributed mod 2pi
3. The random variable Y = sum 2|c_k| cos(theta_k + arg(c_k)) is symmetric about 0
4. The threshold delta(N) = O(log N / sqrt(N)) vanishes
5. Therefore P(Y > delta) -> P(Y > 0) = 1/2

**Criticism:** The observed P(T > 0) = 0.462 is measured among M(p) = -3 primes, NOT among all integers. The R-S theory predicts log-density over ALL N. The restriction to M(p) = -3 primes introduces a selection bias. The document acknowledges this (Section 8.3) but the comparison table (Section 6.3) should carry a more prominent caveat.

### 7. Rubinstein-Sarnak P(T > 0) Numerical Check

Using the Gaussian approximation with sigma = 0.1009 from 20 zeros:

| Constant C | delta(10^7) | P(T > 0) Gaussian |
|-----------|-------------|-------------------|
| 2.52 (Res only) | 0.00940 | 0.463 |
| 4.52 (correct, M = -2) | 0.00876 | 0.465 |
| 6.52 (document, erroneous) | 0.00813 | 0.468 |

All values are in range 0.46-0.47. The +2 error shifts the prediction by only 0.003. **The match with observed 0.462 is robust despite the error.**

### 8. Brute Force Cross-Check

F(N) computed by direct summation vs Perron prediction (residue at s = 0 + 50 zeta zero pairs):

| N | F(N) actual | F(N) Perron | Difference | T(N) actual | T(N) Perron |
|---|------------|-------------|------------|------------|-------------|
| 100 | -4.636 | -4.779 | 0.143 | -5.636 | -5.779 |
| 500 | -12.334 | -11.944 | 0.390 | -6.334 | -5.944 |
| 1000 | -9.193 | -9.088 | 0.106 | -11.193 | -11.088 |
| 2000 | -7.596 | -7.831 | 0.235 | -12.596 | -12.831 |

The Perron formula with 50 zeros predicts F(N) to within 0.1-0.4, with accuracy improving as N grows. Remaining error from higher zeros, trivial zeros, and truncation.

---

## Issues Summary

### ERRORS (must fix)

1. **Section 4.1 constant term: +2.0 overcounting.** The explicit formula has an erroneous "+2" in the brackets. Correct constant for M(N) = -2 is 4.52, not 6.52. Downstream impact is minor but the formula as written is wrong.

2. **Section 2.3 minor rounding:** N = 10^7 residue stated as -29.728, correct value is -29.715.

### WARNINGS (should address)

3. **Section 4.1 mixes general and specific.** The general Perron formula and the M(N) = -2 specialization need clearer separation.

4. **Section 5.4 is unfinished.** Contains "Wait -- more carefully:" followed by a confused re-derivation. Needs clean rewrite.

5. **Section 6.3 selection bias.** R-S theory applies to all N; comparing with M(p) = -3 primes is theoretically unjustified without a conditional density argument.

6. **Error terms never bounded.** Acknowledged in Section 8.3 but the O(1) claim is asserted, not proved.

### CONFIRMED CORRECT

7. Perron integral representation (Section 1): analytically and computationally verified.
8. Laurent expansion and residue formula (Section 2): verified by independent contour integration.
9. All zeta zero coefficients (Section 3): verified to 5+ significant figures.
10. Phase prediction 5.208 (Section 5): verified to 4 decimal places.
11. Density 1/2 (Section 6): sound argument under GRH + LI.
12. P(T > 0) ~ 0.47 at N = 10^7 (Section 6.3): robust to constant error.
13. Novelty assessment (Section 8.4): honest and accurate.

---

## Previous Audit Missed the +2 Error -- Why?

The first audit (2026-03-30) verified the residue formula Res_{s=0} = -2(logN + gamma) + 2log(2pi) correctly, and verified all c_k and d_k values. But it did not check whether the constant in the EXPLICIT FORMULA (Section 4.1) matched the residue. The explicit formula introduces an extra "+2" that is not present in the residue, and the first audit did not perform the brute-force cross-check that catches this discrepancy. **Lesson: always cross-check the final formula against direct computation, not just the intermediate steps.**

---

## Referee Recommendation

**Minor revision.** Fix the +2 arithmetic error in Section 4.1, clean up Section 5.4, add a caveat to the M(p) = -3 density comparison. The core mathematical content is sound (conditional on GRH + LI) and the numerical predictions are validated. The honest novelty assessment (Section 8.4) is appreciated.

---

## Verification Script

Independent verification: `adversarial_perron_verify.py` (in this directory).
- mpmath at 50-digit precision
- All constants independently computed
- Contour integration for residue verification
- Brute-force F(N) and T(N) cross-checks at N = 100, 500, 1000, 2000
