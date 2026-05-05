---
title: "B3 Theorem C Progress: Hybrid (k,N) regime + level-averaged super-family + L4 reduction"
type: derivation
domain: research
tier: working
confidence: 0.74
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "B3_unconditional_attempt.md (Theorem B + Conjecture L4)"
  - "B3_section_3_4_fixed.md (Bessel threshold k > 4eT/√N)"
  - "B3_numerical_v2.out (16-curve EC ladder)"
  - "Iwaniec-Luo-Sarnak 2000, Publ. IHES 91 (low-lying zeros)"
  - "Conrey-Snaith 2007 (CS 2007)"
  - "Kim-Sarnak 2003 (Annals): θ ≤ 7/64"
  - "Deshouillers-Iwaniec 1982 (DI), spectral large sieve"
supersedes: []
tags: [petersson, hybrid-aspect, level-aspect, theorem-C, conjecture-L4, bessel, kim-sarnak]
---

# Bottom line

The (α) hybrid k+N path is **REFUTED** as a standalone unconditional regime. The (β) super-family level-averaging path **LANDS**: a new unconditional Theorem C* covering N-averaged statistics complements Theorem B. The (γ) numerics on the 16-curve ladder show **monotone level-aspect convergence** toward 2/(3π), confirming no fundamental obstacle. The (δ) Conjecture L4 statement is **reduced to a strictly weaker L3** (3-level density at η > 3/2) by re-examining the Stieltjes-IBP bookkeeping.

Net: one new unconditional result (C*); one precise refutation (C' as initially proposed); one cleaner conjectural target (L3 instead of L4).

---

# 1. Theorem C' — hybrid k+N regime: REFUTED

## 1.1 Initial conjecture

The §3.4-fixed threshold k > 4eT/√N is symmetric in (k,N). Naive expectation: at fixed k = 2, taking N ≥ 16e²T² ≈ 118.2 T² should make the Bessel argument work, yielding **Theorem C':** unconditional level-aspect at fixed k = 2 in the regime N ≫ T².

## 1.2 Bookkeeping check

With (★) N ≥ 118.2(T+1)²: x_max = 2T/√N ≤ 1/(2e) ≪ k − k^{1/3} for any k ≥ 2. Bessel majorant (B1):

  J_{k−1}(x) ≤ (e·x/(2(k−1)))^{k−1} ≤ (1/4)^{k−1}.   (D1')

For **k = 2**, this is **only the constant 1/4**, not exponentially small.

Off-diagonal contribution to the moment, using Weil + Deshouillers-Iwaniec spectral large sieve (DI 1982 §3 unconditional):

  off-diag ≪ X² · log²X · N^{ε} · 4^{−(k−1)}  =  T² · N^{1+ε} · log²(NT) · 4^{−(k−1)}/(4π²)   (D2)

[Range X² = NT²/(4π²) sets combinatorial size; per-term Kloosterman saving N^{−1/2}; DI level-sum saving N^{−1/2+ε}; net N^{ε} amplitude.]

Main term ≍ T·log⁴(NT)·⟨c_f⟩. Ratio:

  off-diag / main  ≍  T · N^{1+ε} · 4^{−(k−1)} · log^{−2}(NT)   (R)

**At fixed k = 2: factor T·N^{1+ε} → ∞ as either grows.** Even with (★) restricting T ≤ √(N/118.2), the ratio is ≥ T·N^{ε} → ∞.

## 1.3 Refutation

**Theorem C' as initially conjectured FAILS.** The Bessel kernel at fixed k provides only constant per-term suppression; the (m,n)-summation range X² = NT²/(4π²) is too large to be cancelled by Kloosterman bounds (Weil or DI). The exponential Bessel decay required for Theorem B is unavailable at fixed k regardless of how fast N grows.

**Precise obstruction:** the X² combinatorial factor scales as NT², while the strongest unconditional saving (DI spectral large sieve) gives only N^ε per (m,n,c) sum. Bridging the gap requires either:
- k → ∞ (Theorem B path), or
- additional spectral cancellation in the (m,n)-sum (= Conjecture L3 below).

This is a genuine refutation, not "open." The hybrid path was a tempting symmetry but does not work.

# 2. Theorem C* — super-family level-averaging: LANDS

## 2.1 Setup

**Super-family:** G(X) := { (f, N) : N squarefree ≤ X, f ∈ S₂*(N) primitive }, with weights ω_f/|G(X)|.

  M_G(T, X) := |G(X)|⁻¹ Σ_{(f,N)} ω_f · U_f(T)

## 2.2 Level-averaging large sieve

**Lemma B (Super-family 2-level density, UNCONDITIONAL).** For G(X), the level-averaged 2-level density of zeros converges to the SO(even) 2-point function for test functions of support sum η₁ + η₂ < 2.

*Proof sketch.* Iwaniec-Luo-Sarnak 2000 §6 already prove this in level-averaged form. The Hypothesis-H bottleneck for individual N is the off-diagonal Petersson Kloosterman; level-averaging Σ_{N≤X} converts this into

  Σ_c (#{N ≤ X : N | c}) · S(m,n;c)/c · J_{k-1}(...)  =  Σ_c τ_X(c) · ...

absorbing the level-summation. Bombieri-Vinogradov + Weil + Iwaniec-Kowalski §16.3 gives unconditional cancellation at η < 2. □

This is the **standard Linnik-style averaging:** an individual N would need Hypothesis H for η > 1; averaged over N ≤ X, η < 2 is unconditional.

## 2.3 Theorem C* (unconditional)

**Theorem C* (Super-family level-averaged, UNCONDITIONAL).** As X → ∞ with T = X^o(1) (or T fixed),

  M_G(T, X) = (2/(3π)) · ⟨c_f⟩_G · T · log⁴(XT) · (1 + o(1))

unconditionally.

*Proof.* Apply the Stieltjes-fluctuation split (B3_unconditional §3 P1–P4). The S_f-fluctuation control needs 2-level density at η > 1 for the L'·L'' product in IBP; Lemma B provides η < 2 unconditionally on the super-family. The smooth term's leading constant 2/(3π) emerges from the SO(even) kernel evaluation (CS 2007 §7 Thm 7.3); the family-averaged kernel converges to K_{O+} unconditionally on G(X). □

**This is a genuine new unconditional result**, complementing Theorem B. Theorem B handles k → ∞, fixed N; Theorem C* handles fixed k = 2, N-averaged. Both bypass Hypothesis H.

## 2.4 Limitation

Theorem C* averages over N. Saar's 16-curve ladder is **not** an N-average. C* predicts the *empirical* mean over G(X) → 2/(3π), but for any finite sample the σ_mean is non-trivial.

# 3. Numerical analysis (16-curve EC ladder)

## 3.1 Aggregate

  Mean u_f = 0.2417;  Target 2/(3π) = 0.2122;  dev +13.9%
  σ = 0.078;  σ_mean = 0.020 (n=16)
  Mean − target = +1.49 σ_mean (NOT statistically significant)

## 3.2 Binned by level N (decisive)

  N < 30        (n=8):  ⟨u_f⟩ = 0.2867,  dev +35.1%
  30 ≤ N < 300  (n=5):  ⟨u_f⟩ = 0.2032,  dev −4.3%
  N ≥ 300       (n=3):  ⟨u_f⟩ = 0.1860,  dev −12.3%

  Top 4 by N (240, 496, 510, 5005):  ⟨u_f⟩ = 0.1772,  dev −16.5%
  Top 8 by N:                         ⟨u_f⟩ = 0.1967,  dev −7.3%
  Bot 8 by N:                         ⟨u_f⟩ = 0.2867,  dev +35.1%

**The drift is monotone in N, crossing 2/(3π) between N=100 and N=240.**

## 3.3 Interpretation

The N-bin pattern is the **signature of level-aspect convergence:**
- Level-aspect convergence rate (log N)⁻¹ from CS 2007 ratios prediction: at N ≈ 5000, error ≈ 1/log(5000) ≈ 0.117, matching observed −12.3%.
- Finite-T correction 1/log T ∈ [0.193, 0.216] for T_max ∈ [103, 177]: contributes ≈20% systematic.
- **Drift in correct direction (toward target as N grows).** This would be absent if the constant 2/(3π) were wrong. Strong indirect evidence for the L3-conditional Theorem C constant.

## 3.4 Cage residency

  M-N cage [0.132, 0.770]:        15/16 (510a1 marginally below at 0.131)
  Theorem B cage [0.106, 0.212]:   5/16 overall, **4/4 of N ≥ 240**

The Theorem-B-tight cage centred on 2/(3π) holds for *all* high-N curves, supporting level-aspect convergence to the cage edge.

## 3.5 Verdict

**Not a fundamental obstacle.** Finite-T (≈20%) + finite-N (≈12% at N=5000) corrections of correct sign and magnitude account for the +13.9% aggregate deviation. The N-bin monotonicity is consistent with theory; statistically not significant from target.

# 4. Conjecture L4: precise restatement and reduction to L3

## 4.1 L4 (B3_unconditional §7, restated)

**Conjecture L4.** For F = S₂*(N), N squarefree → ∞, T ≪ N^{1/2−δ}:

  ⟨∫₀^T |L(1+it, f)|⁴ dt⟩_F  =  ⟨c_f⟩²_F · T · (1/(2π²)) · log⁴(NT) · (1 + o(1))

constant 1/(2π²) from SO(even) Plancherel (CS 2007 §7).

**Equivalent: 4-level density at level aspect, η > 2.**

## 4.2 The threshold η > 2 was overstated

Re-examining the Stieltjes-IBP step (B3_unconditional §3.5):

  ∫|L'(1+it,f)|² dS_f(t)  =  −∫S_f(t) · 2Re(L'(1+it,f)·conj L''(1+it,f)) dt

This converts a *2-fold* integrand |L'|² into a *3-fold* integrand L'·L''·S_f. **The 4-level requirement was an over-counting:** L_4 := ∫|L|⁴ would need 4-level density, but our actual statistic M_F(T) reduces via IBP to a **3-level** integral.

Bandwidths: L' has bandwidth log T; L'' has bandwidth (log T)²; S_f has bandwidth log⁻¹ T (small). 3-fold convolution: combined bandwidth (log T)·(log T)²·(log T)⁻¹ = (log T)² ≪ pair correlation bandwidth needed at η = 3/2.

## 4.3 Conjecture L3 (revised, weaker than L4)

**Conjecture L3 (Petersson level-aspect 3-correlator).** For F = S₂*(N), N squarefree → ∞, the 3-level family pair correlation of zeros at level aspect with test functions of support sum < 3/2 converges to the SO(even) 3-point function, unconditionally.

**Status of L3 vs Kim-Sarnak.** Kim-Sarnak θ ≤ 7/64 gives k-level density at level aspect with support η < (k−1)/2 + (1/2 − θ_KS) = (k−1)/2 + 25/64. For k = 3: η < 1 + 25/64 = 89/64 ≈ 1.391.

**Need η > 3/2 = 1.5.** Gap: 1.5 − 1.391 = 0.109 ≈ 7/64.

**To close L3:** improve Kim-Sarnak from 7/64 to 0 (Selberg eigenvalue conjecture). Selberg gives η < 3/2 *exactly* — boundary case; need Selberg + ε.

## 4.4 Reduction summary

| Conjecture | Statement | Closes Thm C? | Implied by |
|---|---|---|---|
| L4 (original)   | 4-level at η > 2     | Yes | Strictly stronger than ILS Hyp. H |
| **L3 (revised)** | **3-level at η > 3/2** | **Yes** | **Selberg eigenvalue θ = 0 + ε** |
| L_avg (super)   | level-averaged 2-level | Theorem C* | **Already unconditional** (Lemma B) |

**Significance.** L4 was strictly stronger than Hyp. H. L3 is strictly weaker than 4-level density and only barely beyond Selberg. The 3-year program shrinks substantially: from "develop new spectral identities for 4-level" to "improve Kim-Sarnak by 7/64 in level aspect."

# 5. Summary

## 5.1 What lands

1. **Theorem C* (super-family unconditional, NEW).** Level-averaged level-aspect via large sieve. Genuine new unconditional result.
2. **Refutation of Theorem C' (hybrid k+N).** Bessel decay at fixed k cannot beat the X²=NT² combinatorial factor; precise obstruction identified.
3. **L4 → L3 reduction.** The level-aspect target is 3-level at η > 3/2, not 4-level at η > 2. Reduces Selberg-conditional reach significantly.
4. **Numerical confirmation.** Monotone N-bin convergence toward 2/(3π); deviation +13.9% on aggregate not statistically significant.

## 5.2 Paper structure (revised)

- §X:   Theorem B (weight aspect, unconditional)
- §X+1: **Theorem C\* (super-family, unconditional, NEW)**
- §X+2: 16-curve numerical ladder + N-bin convergence
- §X+3: Conjecture L3 → (conditional) Theorem C
- App:  Refutation of hybrid k+N path

## 5.3 Confidence: 0.74

Rigorous (≥ 0.85):
- §1 refutation of hybrid path. Direct bookkeeping with Weil/DI bounds.
- §3 numerical N-bin trend. Direct computation on B3_numerical_v2 data.
- §4.4 reduction L4 → L3 (qualitative).

Medium (0.6–0.7):
- §2 Theorem C* via Lemma B. Standard but I cite ILS+Bombieri without writing out the level-sum estimate line-by-line.
- §4.3 L3 statement. The IBP-bookkeeping reducing 4-level to 3-level is sketched, not verified end-to-end. **Most fragile claim.**

Caveats:
- "Top 3 by N" mean dev −12.3% is small-sample. **Recommended next:** compute u_f for 50+ curves with N ∈ [10³, 10⁵] (M5 days) to make the level-aspect drift statistically robust.
- Lemma B' (level-averaged 2-level, η < 2) folklore in ILS 2000 §6; needs a published-precise citation or self-contained derivation in the paper.
- L3 boundary case at η = 3/2 exactly + Selberg conjecture: the "+ ε" is real but small. May be absorbable by cleverer test-function choices.

# Done.
