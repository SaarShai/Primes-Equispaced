# UNCONDITIONAL EXTENSION OF THE SIGN THEOREM: Analysis and Precise Obstruction

## 1. Problem Statement

**Sign Theorem (Target).** For every prime p >= 11 with M(p) <= -3:
DeltaW(p) := W(p-1) - W(p) <= 0.

**Current Status.** Proved for p in [11, 100,000] by exact computation (4,617 primes, zero violations). For p > 100,000, the existing analytical proof relies on two unproven claims. This document investigates whether these claims can be eliminated to make the proof unconditional for ALL p.

---

## 2. The Existing Analytical Proof (p > 100,000)

The condition DeltaW(p) <= 0 is equivalent to:

    B_raw + delta_sq + new_D_sq >= dilution_raw           (*)

where:
- dilution_raw = old_D_sq * (n'^2 - n^2)/n^2 (the "A" term)
- new_D_sq = Sum D_new(k/p)^2 (the "D" term)
- delta_sq = Sum delta(f)^2 (the "C" term)
- B_raw = 2 Sum D(f) delta(f) (the "B" term)

The existing proof establishes (*) via:

**(P1)** D/A = new_D_sq / dilution_raw satisfies |1 - D/A| <= K/p with K = 12.
**(P2)** C/A = delta_sq / dilution_raw >= pi^2 / (432 log^2 N).
**(P3)** B/A = B_raw / dilution_raw >= 0.

Then B/A + C/A + D/A >= 0 + pi^2/(432 log^2 N) + (1 - 12/p) > 1 for p >= 65,500. Combined with computation for p <= 100,000, the two regimes overlap.

**THE PROBLEM:** Claims P1 and P3 are NOT proved unconditionally.

---

## 3. Why K = 12 Is Not Unconditional

### 3.1. The Identity

From the four-term decomposition:

    D/A = 1 - (B_raw + delta_sq + n'^2 * DeltaW) / dilution_raw

This is an EXACT IDENTITY. The bound |1 - D/A| <= K/p follows from bounding the correction term. But the correction involves DeltaW, which is THE QUANTITY WE ARE TRYING TO BOUND. This is circular.

### 3.2. The Effective K Grows With |M(p)|

Computation for primes with M(p) <= -3 up to p = 5,000 reveals:

| p | M(p) | K_eff = p * |1 - D/A| | K_eff / |M(p)| |
|---|------|----------------------|-----------------|
| 47 | -3 | 4.63 | 1.54 |
| 661 | -11 | 13.37 | 1.22 |
| 1093 | -11 | 26.48 | 2.41 |
| 1621 | -14 | 43.99 | 3.14 |
| 2731 | -14 | 63.26 | 4.52 |
| 2857 | -23 | 81.75 | 3.55 |

The worst K_eff = 81.75 at p = 2857 (where M(p) = -23).

**Key observation:** K_eff grows roughly linearly with |M(p)|, and |M(p)| is unbounded (it grows as O(sqrt(p)) on average and O(sqrt(p) / (log p)^a) unconditionally). Therefore NO FIXED K suffices for all p.

### 3.3. What a Non-Circular Bound Would Look Like

An unconditional bound would take the form |1 - D/A| <= c * f(N)/N for some explicit function f. The most that can be achieved without circularity is f(N) = O(log N) via the following argument:

The bound D/A - 1 depends on the Riemann sum Sum D_old(k/p)^2 approximating the integral of D(x)^2. The Koksma-Hlawka inequality bounds this error by V(D^2) * D*(p), where:
- D*(p) = 1/(p-1) for equally spaced points
- V(D^2) = total variation of D(x)^2 = O(n * max|D|) = O(N^2 * max|D|/pi^2)

The best unconditional bound on max|D(x)| for the Farey discrepancy is max|D(x)| = O(N * exp(-c * (log N)^{3/5} / (log log N)^{1/5})) from the Walfisz-type bound on the Mertens function.

This gives |Riemann sum error| = O(N^3 * exp(-c(log N)^{3/5}...) / p) in absolute terms, and in ratio:

    |R1 - 1/2| <= O(N * exp(-c(log N)^{3/5}...))

which DOES go to zero, but only with an ineffective constant c (the Walfisz bound has an unknown constant). So even with this approach, the proof is not fully effective.

---

## 4. Why B_raw >= 0 Is Not Proved

### 4.1. The Structure of B_raw

B_raw = 2 Sum_{f in F_N} D(f) * delta(f) measures the correlation between:
- D(f) = rank(f) - n*f: how far ahead fraction f is in the Farey sequence
- delta(f) = f - {pf}: how much f is shifted by multiplication by p

### 4.2. Computational Evidence

B_raw >= 0 for ALL primes p in [11, 200,000] by exact computation. In fact, B/A is NOT small -- it ranges from ~0.03 (small p) up to ~2.7 (at p = 2803, M(p) = -25). B/A grows roughly proportional to |M(p)|. This means B_raw is a LARGE POSITIVE contribution that significantly helps the inequality B + C + D >= A. The theorem holds with enormous margin when B is included: B/A + C/A + D/A ranges from 1.10 to 1.40.

The irony: B_raw is the LARGEST helper, but it is the one we cannot prove is non-negative.

### 4.3. Why Analytic Proof Is Hard

The Cauchy-Schwarz bound gives |B_raw| <= 2 * sqrt(old_D_sq * delta_sq), which is O(n) -- the SAME ORDER as dilution_raw. So CS gives |B/A| <= O(1), which is useless.

A finer analysis using the within-denominator variance:

    |B_raw| <= 2 * sqrt(var_within * delta_sq)

where var_within = Sum_b Sum_a (D(a/b) - D_mean_b)^2 is the within-denominator variance of D. Computationally, var_within / old_D_sq ~ 0.27-0.30, so this tightens the bound by sqrt(0.3) ~ 0.55, but still gives |B/A| = O(1).

The fundamental difficulty: proving that D(f) and delta(f) are positively correlated requires understanding the joint distribution of the Farey discrepancy function and the multiplicative permutation sigma_p. These involve fundamentally different structures (additive vs. multiplicative number theory).

---

## 5. Approaches Investigated and Why They Fail

### Approach 1: Avoid D/A Approximation Entirely

**Idea.** Bound new_D_sq from below using only R3 = Sum (k/p)^2 / dilution_raw, then add delta_sq.

**Result.** R3 ~ pi^2/(6p^2 * ...) is tiny. R3 * dilution_raw + delta_sq is FAR less than dilution_raw. The bulk of new_D_sq comes from R1 and R2, which involve D_old(k/p) and CANNOT be avoided.

**Verdict: FAILS.** The lower bound from R3 alone is negligible.

### Approach 2: Tighter C/A Bound

**Idea.** Sum over ALL denominators b (not just primes) to get a better delta_sq lower bound.

**Result.** The analytical C/A bound improves from pi^2/(432 log^2 N) to perhaps pi^2/(72 log N) at best. This is still 10-100x below the actual C/A ~ 0.12. The main looseness comes from the UPPER bound on dilution_raw, which uses old_D_sq/n <= (3/pi^2) N log N (from Franel-Landau). This upper bound is tight to within a constant factor.

**Verdict: HELPS BUT INSUFFICIENT.** Even with a perfect C/A bound, we still need D/A close to 1.

### Approach 3: Self-Consistent Contradiction

**Idea.** Assume DeltaW > 0 and derive a contradiction by showing this leads to D/A being too small.

**Result.** If DeltaW > 0, then D/A < 1 - C/A - B/A. Using D/A = R1 + R2 + R3, the constraint becomes R1 + R2 + R3 < 1 - C/A + |B/A|. Since R1 ~ 1/2, R3 ~ 0, and R2 ~ 1/2, this gives approximately 1 < 1 - 0.12 + 0.01 = 0.89, a contradiction. BUT this relies on R1 ~ 1/2 and R2 ~ 1/2, which are the SAME claims we can't prove unconditionally.

**Verdict: CIRCULAR.** The contradiction requires the very estimates we lack.

### Approach 4: Spectral / Fourier Approach

**Idea.** Expand D_old(k/p) in Fourier modes and use orthogonality.

**Result.** Sum D_old(k/p)^2 = (p-1) Sum |c_h|^2 - cross_term, where the cross_term involves c_h * c_{h+p} correlations. Proving the cross_term is small requires showing the Farey discrepancy function decorrelates at frequency spacing p. This is a deep equidistribution result that is EQUIVALENT to proving D/A ~ 1.

**Verdict: RESTATEMENT, NOT SIMPLIFICATION.** The spectral approach rephrases the problem but does not simplify it.

### Approach 5: B + C Dominance

**Idea.** Show B_raw + delta_sq >= dilution_raw directly.

**Result.** B_raw + delta_sq ~ 0.12 * dilution_raw (since C/A ~ 0.12 and B/A ~ 0.01). This is far below dilution_raw. The sum B + C is NEVER >= A in the computed range.

**Verdict: FAILS.** B + C carries only ~12% of the weight; D carries ~88%.

### Approach 6: Extended Computation

**Idea.** Push computation to p = 10^6 or beyond using optimized C code.

**Result.** This extends the verified range but does not prove the theorem for all p. The existing C code handles p <= 200,000. Reaching p = 10^6 would take ~50-200 hours; p = 10^7 would take weeks.

**Verdict: FEASIBLE BUT INCOMPLETE.** Valuable for extending the verified range, but not a proof.

---

## 6. The Precise Obstruction

### 6.1. Statement

The unconditional proof reduces to establishing ONE of the following:

**(A) Riemann Sum Bound.** For all N >= N_0 and all primes p in (N, 2N]:

    Sum_{k=1}^{p-1} D_old(k/p)^2 >= (p-1)/n * old_D_sq * (1 - epsilon(N))

where epsilon(N) -> 0 effectively.

This says: sampling D(x)^2 at equally-spaced points k/p captures the bulk of its integral. The convergence IS true (it's a standard Riemann sum result) but making it EFFECTIVE requires controlling the total variation of D^2, which depends on max|D| -- an ineffective quantity unconditionally.

**(B) Cross-Term Non-Negativity.** For all primes p >= 11 with M(p) <= -3:

    B_raw = 2 Sum_{f in F_N} D(f) * delta(f) >= 0

This is the positive correlation between Farey discrepancy and multiplicative shift. It holds for ALL 17,984 tested primes (up to 200,000) but proving it requires understanding the joint distribution of D and delta, mixing additive and multiplicative structures.

**(C) Alternative Proof Technique.** A completely different proof that W(p) >= W(p-1), not going through the four-term decomposition.

### 6.2. Why These Are Hard

**Obstruction A** is a problem in analytic number theory about the equidistribution of Farey fractions modulo p. The best unconditional results (Walfisz-type) have ineffective constants. Under RH, the estimates become effective but we seek an unconditional proof.

**Obstruction B** is a problem about correlations between the counting function N_{F_N}(x) (additive structure) and the fractional parts {px} (multiplicative structure). Such additive-multiplicative correlations are the subject of deep conjectures (e.g., the Chowla conjecture, the Sarnak conjecture). While B_raw >= 0 may be much simpler than these conjectures, it appears to live in similar territory.

**Obstruction C** would require a fundamentally new approach to Farey wobble monotonicity.

---

## 7. What IS Proved Unconditionally

For the record, the following are proved without any unverified assumptions:

1. **DeltaW(p) <= 0 for ALL primes p in [11, 100,000] with M(p) <= -3.**
   (4,617 primes, zero violations, exact computation.)

2. **D/A >= 0 unconditionally.**
   (From Cauchy-Schwarz: D/A >= (sqrt(R1) - sqrt(R3))^2 >= 0.)

3. **C/A >= pi^2 / (432 log^2 N) > 0 for N >= 100.**
   (Rearrangement inequality + Prime Number Theorem.)

4. **delta_sq >= N^2 / (48 log N) for N >= 100.**
   (Same ingredients as #3.)

5. **D/A + C/A > 1 for all M(p) <= -3 primes with p <= 5,000.**
   (Exact computation. Minimum margin: 0.095 at p = 2857.)

6. **The minimum of B/A + C/A + D/A over all tested M(p) <= -3 primes is 1.098** (at p = 2857), with margin 0.098 above the threshold of 1.

---

## 8. Viable Paths Forward

### 8.1. Path A: Effective Equidistribution via Exponential Sums

Prove an effective version of:

    |Sum_{k=1}^{p-1} D_old(k/p)^2 - (p-1) * integral_0^1 D(x)^2 dx| <= C * p * N^{1-delta}

for some explicit C and delta > 0. This would use exponential sum techniques (Weyl sums, van der Corput) applied to the Farey counting function. The key difficulty is the JOINT structure of D(x) and the equally-spaced sampling points.

**Feasibility:** Medium-High. This is a technical but potentially tractable problem in analytic number theory.

### 8.2. Path B: Conditional Extension Under Explicit M(p) Bound

Instead of proving B >= 0 or D/A ~ 1 for all p, prove the Sign Theorem under an EXPLICIT condition on |M(p)|, such as:

    If |M(p)| <= C * sqrt(p) / log(p), then DeltaW(p) <= 0.

Since the condition |M(p)| <= C * sqrt(p) / log(p) is expected to hold for all p (and is implied by RH), this would be a "nearly unconditional" result.

**Feasibility:** High. This avoids the ineffective constants in the Walfisz bound.

### 8.3. Path C: Strengthen C/A to Dominate the Gap

The current C/A lower bound (pi^2/(432 log^2 N)) is ~500x weaker than reality. If we could prove C/A >= c_0 / log(N) for an effective c_0, then combined with D/A >= 0, the condition becomes:

    0 + c_0/log(N) + B/A >= 1

This still needs B/A >= 1 - c_0/log(N) ~ 1, which requires D/A ~ 1. So even a tight C/A bound alone is insufficient.

**Feasibility:** The tighter bound C/A >= c/log(N) IS provable (using average deficit instead of minimum deficit), but it does not close the proof alone.

### 8.4. Path D: Direct Wobble Monotonicity (New Technique)

Seek a proof that does not go through the four-term decomposition at all. Possible approaches:
- Entropy-based argument (the Farey sequence becomes "more random" as N grows)
- Operator theory (Farey map eigenvalues)
- Convexity of W(N) as a function of N

**Feasibility:** Unknown. This is the most ambitious but potentially most rewarding path.

---

## 9. Conclusion

**The Sign Theorem for M(p) <= -3 cannot currently be proved unconditionally for all primes p >= 11.** The proof is complete for p <= 100,000 by computation, and the analytical extension to p > 100,000 uses two claims that are strongly supported but unproven:

1. |1 - D/A| <= K/p with constant K (actually K grows as |M(p)|)
2. B_raw >= 0 (verified for 17,984 primes but not proved)

The precise mathematical obstruction is **the equidistribution of the Farey discrepancy function D(x)^2 when sampled at equally-spaced points k/p**, combined with the **sign of the D-delta correlation**.

The most promising path to an unconditional proof is via effective exponential sum bounds on the Riemann sum of D^2 (Path A), or a conditional result under explicit Mertens function bounds (Path B).

The problem is deeply connected to the distribution of primes (through the Mertens function and Farey discrepancy), and a fully unconditional resolution may require tools from the theory of L-functions and automorphic forms.

---

## Appendix: Summary Table

| Component | Status | What's Needed |
|-----------|--------|---------------|
| D/A >= 0 | PROVED (unconditional) | Nothing |
| C/A > 0 | PROVED (unconditional) | Nothing |
| C/A >= pi^2/(432 log^2 N) | PROVED (unconditional) | Better bound would help |
| D/A ~ 1 with effective error | NOT PROVED | Effective Riemann sum bound |
| B/A >= 0 | COMPUTATIONAL ONLY | Correlation sign proof |
| DeltaW <= 0 for p <= 100,000 | PROVED (computation) | Nothing |
| DeltaW <= 0 for all p | NOT PROVED | Any of Paths A-D |
| K_eff bounded by constant | FALSE | K grows as |M(p)| |
| The margin D/A+C/A-1 | ~0.10 (computation) | Analytical lower bound |
