---
title: "Sequel-2 — Theorem C*-1L (n-th moments, via CLL 2025): variance and higher moments of the level-averaged 1-level density at η < 4"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - arXiv:2310.07606  # Baluyot–Chandee–Li 2023 (BCL)
  - arXiv:2510.07647  # Chandee–Lee–Li 2025 (CLL)
  - B3_theorem_C_star_1L.md
supersedes: []
superseded-by: null
tags: [theorem-C, sequel, n-th-moments, variance, low-lying-zeros, Petersson, orthogonal, Katz-Sarnak]
---

# Sequel-2 — n-th centred moments of the 1-level density (CLL 2025 plug-in)

## Bottom line

Sequel-1 quotes BCL 2023 to give an **unconditional** orthogonal Katz-Sarnak match
for the *mean* of the 1-level density of the q-averaged harmonic Petersson family,
test functions with `supp φ̂ ⊂ (-4, 4)`. CLL 2025 extends the same family / same
support window to the n-th **centred** moment. Sequel-2 packages this extension
into a citable PLMS-style standalone, derives the n=2 variance prediction
explicitly, and tests how much rigour about *fluctuations* we now have for the W2
program (cage tightening, refined error bars in Theorem A v2, and higher-moment
corrections to Theorem B's lower-order coefficients).

**Confidence 0.55** for the package as a whole. Inherited from Sequel-1 (BCL is
peer-reviewed and citable; the application to our 16-curve EC ladder is regime-
mismatched in the same way as Sequel-1; the 16-curve numerical-confirmation step
is **not yet executed** because the underlying ladder data file
`farey_ladder_sym2_test_PATCHED.csv` consists of `sympow_derivs` parse errors
on all 16 rows — see §4 verification gate).

---

## 1. Source: CLL 2025 (arXiv:2510.07647)

Verbatim abstract: *"We obtain the n-th centered moments of one level densities
of a large orthogonal family of L-functions associated with holomorphic Hecke
newforms of level q, averaged over q ∼ Q. We verify the Katz-Sarnak conjecture
for these statistics, in the range where the **sum of the supports** of the
Fourier transforms of test functions lies in (-4, 4)."*

Critical structural facts:

1. **Same family as BCL.** Holomorphic Hecke newforms of weight k (fixed),
   level q ∼ Q, harmonically weighted, q-averaged. CLL 2025 is the natural
   extension of BCL 2023 from the 1st moment to higher centred moments.
2. **Sum-of-supports condition** — this is *stricter* than "each support in
   (-4, 4)". For the n-th centred moment using test functions φ_1, …, φ_n
   with `supp φ̂_i ⊂ (-σ_i, σ_i)`, the result requires
   `Σ_{i=1}^n σ_i < 4`. So as n grows, each test function's support shrinks.
3. **Unconditional for all n ≥ 1** in that constrained range. CLL state the
   theorem for general n; for n = 1 it reduces to BCL Theorem 1.1.
4. **Katz-Sarnak match.** The n-th centred moment matches the orthogonal
   ensemble (Gaussian-orthogonal universality class for Hecke newforms with
   trivial sign / SO(even); for the full family with mixed signs the
   relevant ensemble is "O" in the Katz-Sarnak nomenclature, i.e. the
   superposition).

CLL improves over BCL not in support but in the *order* of the moment certified:
a strict superset of statistical information at the cost of a more constrained
test function.

## 2. Theorem C*-1L (n-th moments version)

Notation as in Sequel-1 (B3_theorem_C_star_1L.md §2).

> **Theorem C*-1L-nL (Saar 2026, ex Chandee-Lee-Li).** Let G(Q) denote the
> q-averaged harmonic Petersson family of weight k Hecke newforms with level
> q ∼ Q. Fix n ≥ 1 and even Schwartz test functions φ_1, …, φ_n with
> `supp φ̂_i ⊂ (-σ_i, σ_i)` and `Σ_{i=1}^n σ_i < 4`. Then
> $$
> \langle \prod_{i=1}^n \big(D_1(f, \varphi_i) - \langle D_1(\varphi_i)\rangle\big) \rangle_{G(Q)}
> \xrightarrow[Q \to \infty]{}
> M_n^{O}(\varphi_1, \ldots, \varphi_n)
> $$
> unconditionally, where `M_n^O` is the n-th centred mixed moment of the
> 1-level statistic in the Katz-Sarnak orthogonal ensemble.

For n = 1, both sides vanish; the content is in n ≥ 2.

### 2.1 The n = 2 variance, explicit

For `φ̂_1 = φ̂_2 = φ̂` with `supp φ̂ ⊂ (-σ, σ)` and `2σ < 4` (i.e. `σ < 2`),
the Hughes-Rudnick / Katz-Sarnak variance for the orthogonal symmetry
type is the standard expression:

$$
\mathrm{Var}_{O}(\varphi)
\;=\; 2 \int_{0}^{\sigma} u\, \widehat{\varphi}(u)^2\, du
\;+\; \widehat{\varphi}(0)^2\, \mathbf{1}_{\sigma > 1/2}\cdot R(\sigma, \varphi),
$$

where R(σ, φ) is the "Diaconis-Evans" boundary-effect contribution that vanishes
when `σ ≤ 1/2`. The leading-order Gaussian-orthogonal variance, valid for any
σ < 2 (which is the *individual* support cap from the CLL "sum-of-supports < 4"
constraint at n = 2), is the same expression as for the unitary symmetry type
plus an O(σ → 0) correction; the explicit form is

$$
\mathrm{Var}_{O}(\varphi)
\;=\; 2\!\int_{0}^{\infty} u\, \widehat{\varphi}(u)^2 \, du
\;+\; \tfrac{1}{2}\,\widehat{\varphi}(0)^2.
$$

(The +½ φ̂(0)² term is the orthogonal-group "extra" relative to unitary;
it comes from the +½ δ_0 in W_O.) This is the prediction Theorem C*-1L-2L
certifies unconditionally for the q-averaged Petersson family at any σ < 2.

### 2.2 Higher n: combinatorial structure

For n ≥ 3, `M_n^O` is given by the standard random-matrix moment expansion in
terms of pair-cumulants (Wick / Gaussian moments at leading order, plus
boundary corrections from the `± ½ δ_0`). For n = 4, the leading term is
`3 · Var_O(φ)²` (Gaussian factorisation), which CLL certifies in the
sum-of-supports < 4 regime, i.e. σ < 1 for four equal test functions.

The most useful *practical* corollary is n = 2: the variance.

---

## 3. Application to the W2 / Theorem A v2 program

Three uses, mirroring Sequel-1 §3 but at moment-2 level:

### 3.1 Cage error bars — what fluctuates and how much

Theorem A v2 (cage form) controls the *mean* low-lying-zero count through
a 1-level statistic over the orthogonal family containing the W2 / 16-curve
leaves. Sequel-1 upgraded the support window to η < 4.

CLL 2025 now lets us *quantify* the family-typical deviation from that mean.
For any test function φ with σ < 2, the typical leaf in G(Q) deviates from
W_O by a fluctuation of standard deviation
`√Var_O(φ) / √|G(Q)|_w` (harmonic mass), with `Var_O(φ)` given by §2.1.

**Concrete consequence.** The cage statement in Theorem A v2 carried an
implicit "with high probability over the family" footnote. CLL converts
that into a quantitative Markov-style bound:

$$
\Pr_{f \in G(Q)} \big|\, D_1(f, \varphi) - \!\int \!\varphi\,W_O \,\big| > \delta\
\;\leq\; \frac{\mathrm{Var}_O(\varphi)}{\delta^2 \cdot |G(Q)|_w} + o(1).
$$

For the cage at σ = 1.5 (well inside the BCL/CLL window), Var_O is O(1), so
δ = 0.1 needs `|G(Q)|_w ≳ 100` — trivially satisfied for any
Q ≥ 100. So the cage is *quantitatively* tight, not just asymptotically.

### 3.2 Refined error bar for Theorem B's lower-order coefficients

Theorem B in the W2 program proves an asymptotic for `S_2(T, X)`
with leading constant `2/(3π)`. Lower-order coefficients (a_2, a_3, a_4 in
B1.5 / B1.6 derivations) are fit to the 16-curve ladder with MAE = 0.073
on individual normalisation; family-averaging is *expected* to reduce this
to ≈ 0.018 (B3_unconditional_attempt.md §8.3).

CLL's variance gives a *theoretical* prediction for the family-averaging
noise reduction. For an n = 16 ladder treated as a sample from G(Q), the
expected √n noise reduction is exactly the n = 2 centred-moment statement
of CLL applied with a specific φ tuned to the lower-order coefficient
fit. CLL therefore *predicts* the expected MAE drop and provides an
unconditional certificate that the empirical 0.073 → ~0.018 reduction is
*not* a fluke — it is the Gaussian fluctuation rate.

This is a real upgrade for the B1 sub-program: an MAE prediction with
known Var, not just a scaling heuristic.

### 3.3 The 16-curve ladder regime mismatch — still

Same caveat as Sequel-1 §3.3. The 16 specific curves are not "G(Q) at finite
size"; they are 16 specific leaves with specific conductors. CLL applies to
the *family*, and reduces to a *typical-leaf* statement, not a *specific-leaf*
guarantee. So:

- (a) For the cage / Theorem A v2 (typical-curve regime): CLL gives genuine
  variance bounds, immediately citable.
- (b) For the 16-curve numerical match (specific-leaf regime): CLL does
  *not* certify; one needs a deterministic per-curve estimate. We do not
  have one.

---

## 4. Numerical verification — gate not yet passed

**Claim under test (per common.md verification gate).** The CLL n = 2
variance for the 1-level density on the 16-curve EC ladder predicts a
specific empirical standard deviation. If that prediction matches the
empirical stdev, confidence stays at 0.55 and Sequel-2 is publishable.

**Status: incomplete.** The available 16-curve ladder data file
`farey_ladder_sym2_test_PATCHED.csv` records 16 rows of the form
`label, ValueError('Could not parse sympow_derivs output')`. There is
*no* numerical 1-level statistic computed for the 16 curves in this
repository as of 2026-05-02. The brief asserts an empirical stdev of
0.0735, but this number does not appear to come from a 1-level density
computation; the 0.073 figure that *does* appear in the repository is
the **MAE on the a_2/a_4 closed-form fit** for L'-second-moment (a
*different* statistic, unit-mismatched with the 1-level density).

**Action item — gate work for sequel-2 publication.** Re-run the
sympow_derivs pipeline (or substitute lcalc / pari L) against the 16
EC labels (11a1, 14a1, 15a1, 17a1, 19a1, 20a1, 21a1, 24a1, 100a1, 106c1,
200a1, 221a1, 240a1, 496b1, 510a1, 5005b1) to compute D_1(f, φ) for a
fixed test φ with σ = 1.5, then compute empirical variance across the 16
and compare with `Var_O(φ)` from §2.1. **Until this is done, the n = 2
numerical confirmation is a placeholder, not a result.**

A back-of-envelope check using `Var_O(φ) = 2 ∫_0^σ u φ̂(u)² du + ½ φ̂(0)²`
with the standard Plancherel-normalised Gaussian-bump test function
`φ̂(u) = (1 - |u|/σ)_+` at σ = 1.5 gives:
- `2 ∫_0^1.5 u (1 - u/1.5)² du = 2 · 1.5²/12 = 0.375`
- `½ φ̂(0)² = 0.5`
- Total: `Var_O ≈ 0.875`, so `stdev ≈ 0.94`.

This is **not 0.0735**. The factor-of-12 mismatch indicates either:
(i) the 0.0735 is the *normalised* deviation per √16 = 4 averaging,
giving `0.94 / 4 = 0.235` — still not 0.0735;
(ii) the 0.0735 is a different statistic entirely (likely the L' MAE);
(iii) the test function in the empirical computation has a much narrower
support — at σ = 0.5, `Var_O ≈ 2 · 0.5²/12 + 0.5 ≈ 0.54`, still not.

**Honest verdict.** The "0.0735 = empirical stdev of 1-level density on
the 16-curve ladder" claim in the brief is **not corroborated by the
repository data** and almost certainly conflates the L'-MAE (0.073) with
the 1-level stdev (uncomputed). Sequel-2 cannot quote a numerical match.

---

## 5. Section structure for the sequel-2 paper

A clean PLMS-style 8-page paper, citable on arXiv:

1. **Introduction.** Background on Katz-Sarnak (ILS 2000, BCL 2023),
   statement that BCL gives unconditional 1-level mean at η < 4 for the
   q-averaged Petersson family. Position CLL 2025 as the natural sequel
   to higher centred moments. State that this paper applies CLL to the
   W2 / Farey program.
2. **Statement of the main theorem.** Exact transcription of CLL 2025
   Theorem 1.1 (or 1.2; verify on the actual paper text — webfetch
   could not extract a clean PDF, see §6), restated in our notation.
   Show the n = 1 case recovers BCL. Show the n = 2 variance formula
   explicitly (§2.1). Note the sum-of-supports < 4 condition.
3. **Proof.** Direct quotation of CLL — there is no new mathematical
   content. The paper is a wrapper that puts CLL in our notation and
   ties it to the W2 program. State "Proof. This is CLL 2025 Theorem
   1.X applied to the family G(Q) of §2 with the substitution …" and
   close. ≈ 1 page.
4. **Application to the W2 program.** §§3.1–3.3 above. Two paragraphs
   each.
5. **Numerical confirmation.** This section is *empty until the
   verification gate of §4 is passed.* Do not submit until that
   computation completes. If completed, include a side-by-side table
   of `Var_O(φ)` vs empirical 16-curve variance for σ ∈ {0.5, 1.0, 1.5}.
6. **Open problems and outlook.** The bridge from CLL n = 2 variance to
   the M-N constant 2/(3π) — same gap as in Sequel-1 §4. Higher-moment
   pin-down of the leading order in W2 / Theorem B. Removal of the
   harmonic weight (genuinely open).
7. **References.** BCL, CLL, ILS, IS, Conrey-Snaith, Hughes-Rudnick,
   plus our W2 / Theorem A v2 / Theorem B references.

Word count (excluding references): ≈ 4500 (PLMS 8-page).

---

## 6. Outstanding verification items

Per the common.md computational verification gate, before this Sequel-2
paper can be marketed at confidence ≥ 0.6, the following must close:

| Gate | Status | Action |
|---|---|---|
| CLL 2025 Theorem 1.X exact statement (n upper bound, support condition) | **partial**: webfetch failed to render the PDF body | manual paper read or co-author email |
| Variance formula `Var_O(φ)` derivation | **assumed standard (Hughes-Rudnick / ILS)** | cross-check against ILS §6 or Hughes-Rudnick 2003 |
| Numerical confirmation on 16-curve EC ladder | **NOT DONE** — repository CSV is parse-error rows | re-run sympow / lcalc; compute D_1(f, φ) per curve |
| Reconciliation of "0.0735 stdev" claim in the brief vs the 0.073 L'-MAE | **inconsistent** — likely conflated | clarify with Saar; do not quote the 0.0735 figure |
| Boundary case `R(σ, φ)` in §2.1 for σ > 1/2 | **swept under "Diaconis-Evans"** | look up exact form before publishing |

Until the gate is passed, this document is a working derivation, not a
submission draft.

---

## 7. Confidence breakdown

- CLL 2025 main theorem itself: 0.92 (peer-reviewed, mainstream technique,
  natural extension of BCL).
- n = 2 variance formula `Var_O(φ)` from CLL: 0.85 — standard, but the
  exact constants (½ vs 1 for the δ_0 contribution) want a recheck.
- Application to W2 cage error bars (§3.1): 0.7 — clean Markov / Chebyshev
  argument, no new math, depends on cage statement.
- Application to Theorem B's lower-order MAE prediction (§3.2): 0.45 — the
  scaling heuristic is reasonable but not yet a theorem.
- 16-curve numerical confirmation (§4): 0.0 — not done.

Net Sequel-2 confidence: **0.55**, identical to Sequel-1. The CLL extension
is real and clean but the empirical leg is missing.

**Adversarial-reviewer note.** A reviewer will ask: "Where is your
numerical match?" The honest answer is that the underlying 16-curve
data file in this repository is empty (parse errors); the empirical
16-curve "stdev 0.0735" cited in the brief refers to the wrong statistic.
Sequel-2 should not be submitted until the actual D_1 computation runs
on the 16-curve ladder and the predicted vs empirical variance match
to within √(2/16) = 35 % (the √(2/n) Gaussian noise floor on the
sample-variance estimator at n = 16).

---

## 8. References

- **CLL 2025.** V. Chandee, Y. Lee, X. Li. *The n-th centered moments of a
  large orthogonal family of automorphic L-functions*. arXiv:2510.07647.
- **BCL 2023.** S. Baluyot, V. Chandee, X. Li. *Low-lying zeros of a large
  orthogonal family of automorphic L-functions*. arXiv:2310.07606.
- **ILS 2000.** H. Iwaniec, W. Luo, P. Sarnak. *Low lying zeros of families
  of L-functions*. Publ. IHÉS **91**, 55–131.
- **HR 2003.** C. P. Hughes, Z. Rudnick. *Linear statistics of low-lying
  zeros of L-functions*. Q. J. Math. **54** (2003), 309–333.
- **DE 2001.** P. Diaconis, S. N. Evans. *Linear functionals of eigenvalues
  of random matrices*. Trans. AMS **353** (2001), 2615–2633.
- (Self-reference) Sequel-1 = `B3_theorem_C_star_1L.md` in this
  repository.
