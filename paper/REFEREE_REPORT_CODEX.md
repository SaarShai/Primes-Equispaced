# Referee Report: "The Geometric Signature of Primes in Farey Sequences"

**Referee:** Hostile referee for *Mathematics of Computation*  
**Date:** 2026-04-04  
**Verdict:** MAJOR REVISION REQUIRED — several logical gaps, mislabeled results, and notation inconsistencies must be addressed before publication.

---

## 0. Executive Summary

The paper introduces the per-step Farey discrepancy ΔW(N) = W(N−1) − W(N) and studies its sign pattern as N ranges over primes. The main claim is that this sign is controlled by the Mertens function and phase-locked to the leading zeta zero. The paper contains genuine mathematical content — the Bridge Identity and its generalizations are correct, the Injection Principle is elegant, and the Farey spectroscope is an interesting computational observation. However, several results are presented in a way that obscures the boundary between what is proved and what is computed, multiple "proof sketches" contain gaps that are not flagged as such, and the paper conflates computational verification with proof in at least three places. Below I detail every issue I found, organized by severity.

---

## 1. CRITICAL Mathematical Issues (Must Fix)

### 1.1 The "Sign Theorem" (Theorem 5.1) is computational, not a theorem

**Location:** Section 6, Theorem `thm:sign` (labeled "Computational Sign Theorem")

The paper calls this a "theorem" and gives a "proof" that consists entirely of direct computation in C (double precision). The "proof" on lines ~1740–1770 lists four items:
- (i) D/A ratio claim
- (ii) C > 0 strict positivity
- (iii) C' ≥ cN² asymptotic
- (iv) Computational verification

None of these items, individually or together, constitute a proof. The text itself admits (line ~1770): "whether B + C > 0 ... is not guaranteed analytically." **A result whose proof consists of running a C program is an observation, not a theorem.** The label "Computational Sign Theorem" is an improvement over calling it just "Theorem," but the \begin{theorem} environment and the \begin{proof} environment create the false impression of a mathematical proof.

**Recommendation:** Replace `\begin{theorem}` with `\begin{observation}` or `\begin{computational-result}`. Remove `\begin{proof}` and replace with a description of the computation methodology, precision analysis, and error bounds.

### 1.2 The Bridge Identity proof sketch has a sign error / bookkeeping issue

**Location:** Theorem 3.1 (thm:bridge), proof sketch

The proof claims: "Summing: 2 + Σ_{b=2}^{p-1} μ(b) = 2 + M(p−1) − 1 = M(p) + 2, using M(p−1) = M(p) + 1."

The identity M(p−1) = M(p) + 1 requires μ(p) = −1, i.e., that p is prime and squarefree. This is correct for primes, but the proof sketch does not state this step explicitly. More importantly: Σ_{b=2}^{p-1} μ(b) = M(p−1) − μ(1) = M(p−1) − 1. So the computation reads: 2 + M(p−1) − 1 = 1 + M(p−1) = 1 + (M(p) + 1) = M(p) + 2. This is correct but the intermediate step "2 + M(p−1) − 1" is presented without showing where the −1 comes from (it is μ(1) = 1 being subtracted from M(p−1) to get the sum starting at b=2). The proof sketch is correct but sloppy — for a paper in Math. Comp., the full proof should be given, not a sketch.

**Recommendation:** Provide the full proof, or at minimum make explicit: Σ_{b=2}^{p-1} μ(b) = M(p−1) − μ(1) = M(p−1) − 1.

### 1.3 Theorem 4.11 (Composite Healing Rate) — the "proof" proves nothing

**Location:** Theorem `thm:healing`

The statement claims: "Among composites N ≤ K, the fraction with ΔW(N) > 0 tends to 1 as K → ∞."

The "proof sketch" says: "By a density argument using φ(N)/N → 0 on average over highly composite numbers and the fact that missing numerators create a positive net dilution effect, the fraction of composites with ΔW > 0 approaches 1."

This is not a proof. The claim φ(N)/N → 0 "on average over highly composite numbers" is vague — φ(N)/N does not tend to zero on average over all composites (its average over composites is bounded away from zero). The "net dilution effect" is not defined or proved. The computational evidence cited (147/153 composites up to N=200) is a tiny sample.

**Recommendation:** Either prove this theorem rigorously (which would require quantifying the dilution effect and showing it dominates for large composites), or downgrade to a conjecture. Currently it is stated as a theorem with no valid proof.

### 1.4 Theorem 4.7 (Fisher Information Monotonicity) — proof sketch has a gap

**Location:** Theorem `thm:fisher`

The proof claims: "1/g₁² + 1/g₂² = b²N² + d²N² > b²d² = 1/g², since b² + d² > (bd)²/N² holds for b + d = N with b, d ≥ 1."

The inequality b² + d² > (bd)²/N² when b + d = N is not obvious and not proved. Let me check: with b + d = N, we need b² + d² > b²d²/N². This is equivalent to N²(b² + d²) > b²d². Setting b = N−d: N²((N−d)² + d²) > (N−d)²d². For b = d = N/2: N² · N²/2 > N⁴/16, i.e., N⁴/2 > N⁴/16 ✓. For b = 1, d = N−1: N²(1 + (N−1)²) > (N−1)², i.e., N² > 1 ✓ (after canceling). So the inequality holds, but the proof should be given, not asserted. Also, the proof should verify that the sub-gaps are indeed 1/(bN) and 1/(dN), which requires that the mediant splits the gap exactly as claimed.

**Recommendation:** Provide the algebraic verification that b² + d² > (bd)²/N² for b + d = N, b,d ≥ 1. This is a short AM-GM argument but it should be stated.

### 1.5 Proposition 4.6 (Zero-sum at equispaced points) — proof is incomplete

**Location:** Proposition `prop:zero-sum`

The proof claims Σ D(k/p) = 0 for k = 1,...,p−1, but the proof sketch arrives at −(p−1)/2 from the Farey symmetry pairing and then says there is a "boundary correction at k = p (i.e., f = 1), adjusting the total to zero." But k ranges only from 1 to p−1, so there is no k = p term. The claimed result Σ D(k/p) = 0 appears to contradict the intermediate step Σ = −(p−1)/2. The "boundary correction" is not explained.

Also: the result is stated as "verified for all primes p ≤ 500 by exact computation" rather than proved. This is a simple combinatorial identity that should have a clean proof.

**Recommendation:** Give a complete proof. If the sum is not zero but −(p−1)/2, correct the statement. Clarify what "boundary correction" means.

### 1.6 Theorem 5.3 (Total Shift-Squared Asymptotic) — flagged gap in the proof

**Location:** Theorem `thm:shift-sq-asymp`

The proof sketch honestly admits: "While this step is standard and we expect it to be rigorous, the Kloosterman constant has not been made explicit in our analysis; we flag this as requiring full verification."

**This is commendable honesty.** However, for Math. Comp., the proof must be complete. The step in question is bounding Σ_b |T_b − E[T_b]|/b² using Kloosterman-type estimates. The claim |T_b − E[T_b]| ≤ C·b^{3/2+ε} would follow from the Weil bound, but the paper does not derive this. Moreover, the proof uses "equidistribution of {pa/b} across denominators" without a precise statement or reference.

**Recommendation:** Either complete the proof with explicit Kloosterman bounds and cite the appropriate lemma, or state the result as conditional on the Kloosterman estimate and label it accordingly.

### 1.7 Proposition 6.3 (Spectroscope) — GRH label is misleading

**Location:** Proposition `prop:spectroscope`

The proposition is labeled "[GRH]" and the proof sketch says "Under GRH, the Farey counting error admits E(N) ~ Σ_ρ N^ρ/(ρ·ζ'(ρ))." However, this explicit formula requires not just GRH but also the simplicity of zeros (which is stated in the proposition but buried). More seriously, the step "cross-terms oscillate and remain bounded" is completely unjustified — this is the hard part of any spectral detection argument, and it is exactly where careful analysis of the pair correlation of zeros would be needed.

The claim that F(γ_k) ∝ |(ρ_k·ζ'(ρ_k))^{-1}|² "as the number of primes tends to infinity" is an asymptotic claim with no error term and no rate of convergence.

**Recommendation:** Either provide a rigorous proof (which would be a significant result in its own right, comparable to work of Montgomery and others), or clearly label this as a heuristic prediction supported by computation. The current presentation is in between — it has theorem/proposition formatting but no valid proof.

---

## 2. SIGNIFICANT Issues (Should Fix)

### 2.1 ΔW definition inconsistency

**Location:** Equation (4) and throughout

ΔW(N) is defined as W(N−1) − W(N) (so positive means improvement). But in some places the paper discusses "negative ΔW" meaning "uniformity worsens," while in other places it discusses "ΔW(p) ≤ 0" as the expected behavior for primes with M(p) < 0. This is consistent with the definition, but confusing because the natural convention would be ΔW = W(N) − W(N−1).

**Recommendation:** Add a sentence immediately after (4) clarifying: "We adopt the sign convention that ΔW > 0 means improvement (wobble decreasing) so that primes — which are the 'good actors' geometrically — tend to have ΔW < 0 when M(p) < 0."

Actually wait — re-reading the definition: ΔW(N) = W(N−1) − W(N). If adding N *improves* uniformity, then W(N) < W(N−1), so ΔW > 0. The text says "ΔW(N) > 0 means adding N improves uniformity." This is correct. But then it says "99% of negative-ΔW events come from primes" — meaning primes *worsen* uniformity, which contradicts the geometric intuition that primes are the good actors. The paper later resolves this by showing it depends on M(p), but the initial framing is jarring.

### 2.2 The r = 0.997 correlation claim needs better statistical context

**Location:** Abstract and Section 7

The abstract states "Predicted and observed peak amplitudes correlate at r = 0.997 (p < 10^{-8}, n = 10 zeros)." With n = 10, the degrees of freedom for the t-test are 8. A correlation of r = 0.997 with df = 8 gives t ≈ 36.5, which indeed gives p < 10^{-8}. **The n = 10 is noted**, which is good.

However, the paper does not address the fact that with only 10 data points, the correlation is sensitive to outliers. More importantly, the predicted amplitudes |(ρ_k·ζ'(ρ_k))^{-1}|² decrease roughly monotonically with k (the first zero dominates), and the observed amplitudes also decrease roughly monotonically. Any two monotonically decreasing sequences of length 10 will have high correlation — this is not a strong test of the specific quantitative prediction.

**Recommendation:** Add a note acknowledging that the monotonic trend inflates the correlation, and consider a rank-based test or a test on the deviations from a generic power law.

### 2.3 The Franel-Landau equivalence citation is imprecise

**Location:** Section 1.2

The paper states: "RH holds if and only if W(N) = O(N^{-1+ε})." This is the Franel-Landau theorem restated in terms of W(N). However, the original Franel-Landau theorem is about L¹ discrepancy, not L² discrepancy (wobble). The equivalence for L² is correct but requires a separate (easy) argument via Cauchy-Schwarz. The paper should cite this more carefully.

**Recommendation:** Add a sentence: "The L² equivalence follows from the L¹ version via Cauchy-Schwarz and the classical bound W(N) ≥ (L¹ discrepancy)²/n."

### 2.4 Conjecture 4.3 is labeled "Disproved" in a confusing way

**Location:** Conjecture `conj:disproved`

The paper states a conjecture and immediately labels it "[Disproved]" in the theorem environment. This is unusual formatting. The standard approach would be to state the conjecture as historical motivation and then present the counterexample as a separate observation.

**Recommendation:** Restructure: first state the natural conjecture that emerged from computation, then present Observation 4.4 as the counterexample. Remove the "[Disproved]" tag from the conjecture environment.

### 2.5 "Theorem" vs "Observation" classification inconsistencies

Several results are classified inconsistently:
- Theorem 5.1 (Sign Theorem): purely computational → should be Observation
- Theorem 5.3 (Shift-Squared Asymptotic): has an admitted gap → should be "Theorem (conditional)" or the gap should be filled
- Theorem 4.11 (Composite Healing Rate): no valid proof → should be Conjecture
- Proposition 4.6 (Zero-sum): claimed proof is incomplete → needs fixing
- Observation 6.4 (Healing characterization): correctly labeled as Observation

**Recommendation:** Audit every theorem/proposition/observation and ensure the label matches the level of proof provided.

---

## 3. NOTATION Issues

### 3.1 R is overloaded

The paper uses R for at least four different things:
1. **R** (blackboard bold): the real numbers (via `\R` macro)
2. **R(p)**: the correlation ratio = Σ D·δ / Σ δ²
3. **R(f)**: the Möbius-weighted fractional-part function (Remark 3.6)
4. **R₁(p)** and **R₂(p)**: damage and response ratios (Observation 6.2)

Items 2 and 3 are both used in Remark 3.6 in the *same equation*: "B + C = (−2/n'²)Σ R(f)·δ(f)" where R(f) is the Möbius function, while elsewhere R(p) is the correlation ratio. This is a serious notation clash.

**Recommendation:** Rename the Möbius-weighted function R(f) to something else (e.g., Ψ(f) or M*(f)). Use R exclusively for the correlation ratio.

### 3.2 δ is overloaded

The paper uses δ for:
1. **δ(f)**: the shift function f − {pf} (Definition 2.2)
2. **δ_b**: per-denominator shift sums (Theorem 5.3)
3. **δ₁, δ₂**: in the damage-response decomposition (Observation 6.2)

The connection between δ₁, δ₂ (Observation 6.2) and the original δ(f) is not made explicit. The paper says δ₂(a/b) = (a − pa mod b)/b, which appears to be the same as δ(f) = f − {pf}, but this should be stated.

**Recommendation:** Clarify that δ₂ = δ (the original shift) and define δ₁ explicitly.

### 3.3 ΔW notation in the abstract vs body

The abstract uses ΔW(N) = W(N) − W(N−1) (checking: "sgn(ΔW(p)) ≈ −sgn(cos(...))"), while equation (4) defines ΔW(N) = W(N−1) − W(N). Let me re-read the abstract...

Actually the abstract says: "composites account for 96% of positive-ΔW events" and "primes with M(p) ≤ −3 produce ΔW(p) < 0 in all 4,617 cases." With the definition ΔW = W(N−1) − W(N): positive ΔW means W decreased (improvement), negative means W increased (worsening). For primes with M(p) ≤ −3, ΔW < 0 means W increased — primes make things worse. This is consistent. The sign convention is fine but counterintuitive (one might expect the "improvement" direction to be the default for the object named "ΔW").

### 3.4 D vs D (calligraphic)

The paper introduces 𝓓 (calligraphic D) for the new-fraction discrepancy term, and D(f) for rank discrepancy. This distinction is stated explicitly and is fine. However, in inline text (especially in the proof of Theorem 5.1), D/A appears without always clarifying whether it means 𝓓/A.

**Recommendation:** Always use 𝓓 (calligraphic) for the decomposition term, never plain D in that context.

---

## 4. FIGURE Issues

### 4.1 Figure count and references

The paper references 16 figures:
1. fig:farey-circle — Farey on unit circle ✓
2. fig:wobble-circle — wobble visualization ✓
3. fig:voids — void filling ✓
4. fig:universal — universal formula ✓
5. fig:bridge-vectors — bridge identity vectors ✓
6. fig:sigmoid — sigmoid rate ✓
7. fig:mertens — Mertens function and violation rate ✓
8. fig:delta-w — per-prime ΔW signs ✓
9. fig:shift-map — shift map on circle ✓
10. fig:phase-lock — phase-lock visualization ✓
11. fig:gk-concentration — Gauss-Kuzmin concentration ✓
12. fig:spectroscope — Farey spectroscope ✓
13. fig:juxtaposition — Hardy Z-function vs Farey ✓
14. fig:amplitude-matching — amplitude scatter ✓
15. fig:zero-contributions — zero contribution strengths ✓
16. fig:multi-character — multi-character spectroscope ✓

All 16 figures are referenced in text. Captions appear descriptive and accurate.

### 4.2 Figure 12 (spectroscope) inconsistency

The caption says "2,729 qualifying primes" but the text says "N = 3,829 qualifying primes (p ≤ 83,773)." These are different numbers. Either the figure was generated with 2,729 primes and the text describes a later run with 3,829, or one of the numbers is wrong.

**Recommendation:** Make the figure caption match the text, or explain that they are different runs.

### 4.3 Figure placement

Multiple figures use `[t]` placement but the paper has figures appearing before their first text reference. For Math. Comp. this is typically acceptable but the author should verify during production.

---

## 5. REFERENCE Issues

### 5.1 Missing: Boca-Cobeli-Zaharescu

The Gauss-Kuzmin observation (Observation 6.4) connects to the distribution of Farey fractions studied extensively by Boca, Cobeli, and Zaharescu in their series of papers on the statistical distribution of Farey fractions (e.g., "Distribution of lattice points visible from the origin," Communications in Mathematical Physics, 2000; "On the distribution of the Farey sequence with odd denominators," 2005). These are directly relevant and should be cited.

### 5.2 Missing: Ingham 1942

The paper mentions "Ingham's theorem" (both signs of ΔW occur infinitely often) in the abstract and Remark 5.2, but Ingham is not in the bibliography. The relevant reference is:

A. E. Ingham, "On two conjectures in the theory of numbers," American Journal of Mathematics, vol. 64, pp. 313–319, 1942.

**This must be added.**

### 5.3 Missing: Montgomery-Vaughan or Iwaniec-Kowalski

For the Kloosterman sum / Weil bound arguments invoked in the proof of Theorem 5.3 and in Open Question 11, standard references should be cited (e.g., Iwaniec-Kowalski, "Analytic Number Theory," AMS, 2004).

### 5.4 Garcia 2025 and Parks-Burrus 2020

These are cited in the bibliography but I cannot find where they are referenced in the text. They may have been in cut sections. Dead references should be removed.

### 5.5 El Marraki 1995

Similarly cited in the bibliography but not referenced in the text.

### 5.6 Athreya-Cheung 2014

Cited in bibliography but not referenced in text.

### 5.7 Niederreiter 1992

Cited in bibliography but not referenced in text.

### 5.8 Self-citation

The paper cites "[arxiv-this-paper]" in Remark 5.4 but this is not a real bibitem. This appears to be a placeholder.

**Recommendation:** Either add the arXiv reference or remove the citation.

---

## 6. SPECIFIC CLAIMS VERIFICATION

### 6.1 "D(1/p) = 1 − |F_{p−1}|/p" (Proposition 6.1)

**Location:** Proposition `prop:D1p`

The proof says: "Since 1/(p−1) > 1/p for p ≥ 3, the only fraction in F_{p−1} at most 1/p is 0/1, so rank(1/p, F_{p−1}) = 1."

Wait — the proposition is about D(1/p) in F_p (the fraction 1/p is IN F_p, not F_{p−1}). The rank of 1/p in F_p is the number of fractions in F_p that are ≤ 1/p. These are: 0/1 and 1/p itself, plus possibly 1/(p−1) if p−1 < p (always true) and 1/(p−1) ≤ 1/p (only if p ≤ p−1, which is false). So rank(1/p, F_p) = 2 (just 0/1 and 1/p). Then D(1/p) = rank − n·f = 2 − |F_p|/p.

But the proposition states D(1/p) = 1 − |F_{p−1}|/p. Since |F_p| = |F_{p−1}| + (p−1), this would give D(1/p) = 2 − (|F_{p−1}| + p − 1)/p = 2 − |F_{p−1}|/p − 1 + 1/p = 1 + 1/p − |F_{p−1}|/p.

Hmm, let me re-read. The paper says rank(1/p, F_{p-1}) = 1. But 1/p is NOT in F_{p-1} (since p is the new denominator being added). So D(1/p) should be defined in F_p. The proposition title says "Dominance of 1/p" and defines D(1/p) as rank deviation of the fraction 1/p. Since 1/p ∈ F_p \ F_{p-1}, the rank is in F_p.

Actually, I think the proof is computing the number of old fractions less than 1/p (which is 1, just 0/1), and then using this in the displacement-shift framework. The exact formula D(1/p) = 1 − |F_{p−1}|/p would mean the rank of 1/p in F_p is... Let me compute: D_F_p(1/p) = rank(1/p in F_p) − |F_p| · (1/p). The rank is 2 (0/1 and 1/p). So D = 2 − |F_p|/p = 2 − (|F_{p−1}| + p − 1)/p = 2 − |F_{p−1}|/p − 1 + 1/p = 1 + 1/p − |F_{p−1}|/p. The proposition omits the 1/p term, claiming D(1/p) = 1 − |F_{p−1}|/p. For large p, 1/p is negligible, but the formula as stated appears to be approximate, not exact. The asymptotic D(1/p) ~ −3p/π² is correct regardless.

**Recommendation:** Clarify whether the formula D(1/p) = 1 − |F_{p−1}|/p is exact (in which case the rank computation needs checking) or asymptotic (in which case write ≈ or ~).

### 6.2 "R₂ > 0 for all qualifying primes" (Observation 6.2)

**Status:** Correctly labeled as Observation (computational). The text says "For all 4,617 primes with M(p) ≤ −3 and p ≤ 100,000: R₂(p) > 0 always." And it explicitly states "An analytical proof of R₂ > 0 remains open." **This is properly labeled.**

### 6.3 "r = 0.997 amplitude correlation" with n = 10

**Status:** The n = 10 is noted in the abstract. See issue 2.2 above for the statistical concern.

### 6.4 "3,829 primes detect γ₁, γ₂, γ₃"

**Status:** The spectroscope proposition (Proposition 6.3) gives a GRH-conditional heuristic. The detection claim is clearly computational. The proof sketch is inadequate (see issue 1.7). The numbers are: γ₁ ≈ 14.08 (true: 14.1347, error 0.4%), γ₂ ≈ 20.86 (true: 21.022, error 0.8%), γ₃ ≈ 24.94 (true: 25.011, error 0.3%). These errors are reasonable for the method.

### 6.5 "φ(n)/n < 1/3 → 100% heal" (Conjecture 6.5)

**Status:** Correctly labeled as Conjecture (`conj:healing`). The computational evidence (21/21) is noted. **This is properly labeled.**

### 6.6 "density approaches 1/2" under GRH+LI

**Location:** Remark 5.2

The remark says: "Under GRH + LI, the leading oscillation term is equidistributed, suggesting the density of negative steps approaches 1/2; however, the exact limiting density may differ due to lower-order bias terms (cf. Rubinstein-Sarnak)."

This is appropriately hedged. The GRH+LI conditions are stated. The qualifier "suggesting" and the caveat about lower-order terms are honest. **This is acceptable as stated.**

---

## 7. MINOR Issues

### 7.1 Abstract length
The abstract is approximately 350 words. For Math. Comp., 150–200 words is typical. The abstract contains too many specific numbers and should be shortened.

### 7.2 The paper has no proper Conclusion section
After Open Questions, there are Acknowledgments and References. A brief Conclusion summarizing the main contributions and their status (proved/computational/conjectural) would help the reader.

### 7.3 Authorship
Listing an AI system as a co-author is unconventional and may conflict with journal policy. The footnote describing AI contributions is thorough, but most journals require all authors to be able to take responsibility for the work. This is an editorial decision, not a mathematical one.

### 7.4 MSC codes
11B57 (Farey fractions) and 11M06 (zeta function) are appropriate. 11N37 (asymptotic results on arithmetic functions) is reasonable. 11A25 (arithmetic functions) and 11Y35 (analytic computations) are fine.

### 7.5 Date
The paper is dated "March 2026." Given the current date is April 2026, this is fine.

### 7.6 Lean verification claims
The abstract says "260+ results across fifteen Lean 4 files, one intentional sorry." The text says "258 theorems, lemmas, and definitions." These numbers should be consistent (258 vs 260+).

### 7.7 Proof of Theorem 3.5 (Cross-Term Formula)
The proof says "the Master Involution Principle applies on the interior" but the Master Involution Principle is never stated as a formal result. It appears to be an informal name for the symmetry argument. Either define it formally or use "by the symmetry f ↦ 1−f."

### 7.8 Open Question 6 — Erdős discrepancy problem
The paper mentions the "open multiplicative case of the Erdős discrepancy problem." The Erdős discrepancy problem was solved by Tao (2015) for general sequences. The *multiplicative* version is indeed still open for specific functions. This should be clarified.

---

## 8. OVERALL ASSESSMENT

**Strengths:**
- The per-step Farey discrepancy ΔW(N) appears to be genuinely new.
- The Bridge Identity, its generalizations, and the Universal Farey Exponential Sum are correct and nicely presented.
- The Injection Principle is elegant and the proof is clean.
- The Farey spectroscope is a creative computational observation.
- The formal verification in Lean 4 is a significant effort.
- The paper is generally honest about the computational vs. proved boundary.

**Weaknesses:**
- Multiple "theorems" are actually computational observations (Sign Theorem, Composite Healing Rate).
- Several proof sketches have gaps that are not always flagged.
- Notation is inconsistent (R, δ overloaded).
- The spectroscope proposition's "proof" is a heuristic, not a proof.
- Several references are cited but never used in the text; at least one key reference (Ingham) is missing.
- The paper tries to do too much — it would be stronger as two papers: (1) the identities and injection principle (with full proofs), and (2) the computational phenomena and spectroscope.

**Verdict:** The mathematical content is interesting and some results are correct, but the paper in its current form conflates computation with proof in ways that are unacceptable for Mathematics of Computation. Major revision is required. The most critical items are:
1. Reclassify the Sign Theorem as a computational observation.
2. Either prove or downgrade the Composite Healing Rate.
3. Complete or clearly flag the gap in the Shift-Squared Asymptotic.
4. Fix the notation overloading of R and δ.
5. Add missing references (especially Ingham).
6. Clean up the spectroscope proposition to be honest about what is proved vs. heuristic.
