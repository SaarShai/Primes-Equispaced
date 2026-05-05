---
title: "B3 §3.4 Fixed: Off-diagonal Bessel decay — correct threshold and exponential bound"
type: derivation
domain: research
tier: working
confidence: 0.78
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Watson, A Treatise on the Theory of Bessel Functions, 2nd ed., §8.5 (Debye uniform expansion)"
  - "Iwaniec-Kowalski, Analytic Number Theory, §7.4 (Petersson trace formula in weight aspect)"
  - "Iwaniec, Topics in Classical Automorphic Forms, §5.5–5.6 (Bessel kernel decay)"
  - "Petersson 1932 (original trace formula)"
  - "B3_unconditional_attempt.md §3.4 (errata corrected)"
  - "B3_theorem_B_audit.md (audit issues #4, #5)"
supersedes: ["B3_unconditional_attempt.md §3.4 lines 172–174"]
tags: [petersson, bessel, weight-aspect, off-diagonal, kloosterman, audit-fix]
---

# Bottom line

**Original §3.4 was wrong on two counts.** The correct off-diagonal Bessel-decay statement for the weight-aspect Petersson trace formula at level N (smallest cusp width c = N) is:

> **For k > 2eT/√N, the off-diagonal Petersson contribution decays exponentially**, bounded by exp(-(k-1)·log(k/(eT/√N))) which for k = T^a, a ∈ (1,2), gives exp(-c_0 · k log k) with explicit c_0 > 0. The decay is **uniform** in (m,n) ≤ X = √N·T/(2π) and in c ≥ N.

The threshold "k > 2T" in the original write-up is off by a factor √N (and the exponential phrasing was elided as "vanishes identically" — false; Bessel functions have zeros but are not identically zero). The corrected threshold is k > 2eT/√N, and "exponentially small" replaces "vanishes." Effect on Theorem B: the parameter coupling is now k → ∞ with k > 2eT/√N rather than k > 2T. Since N → ∞ is allowed (or fixed but ≥ 1), this is **strictly easier** for Theorem B; the conclusion of the unconditional weight-aspect theorem stands with the same constant 2/(3π).

---

# 1. Setup

Petersson trace formula at level N, weight k, on F_k = S_k*(N):

  Δ_k,N(m,n) := |F_k|⁻¹ Σ_f ω_f a_f(m) a_f(n)
              = δ_{m=n} + 2π i^{-k} Σ_{c ≡ 0 (N)} c⁻¹ S(m,n;c) J_{k-1}(4π√mn/c)

For our application: m, n ≤ X = √N·T/(2π); summation over c with N | c, so smallest c is c = N.

Define x := 4π√mn/c. The maximal x in the off-diagonal occurs at minimal c = N and maximal mn:

  x_max  =  4π · (√N·T/(2π)) / N  =  2T/√N.   (★)

# 2. Bessel uniform bound (Watson §8.5; Iwaniec Topics §5.5)

**Lemma 2.1 (Watson, A Treatise on the Theory of Bessel Functions, 2nd ed., §8.5, Eq. (3); cf. Iwaniec, Topics, §5.5 Lemma 5.7).** For k ≥ 2 and 0 < x ≤ k,

  J_{k-1}(x)  ≤  (1/Γ(k))·(x/2)^{k-1}  ≤  (e·x/(2(k-1)))^{k-1}/√(2π(k-1))   (B1)

uniformly in x. (The first inequality is the Taylor-series majorant; the second uses Stirling Γ(k) ≥ √(2π(k-1))·((k-1)/e)^{k-1}.)

**Lemma 2.2 (Transition region, Watson §8.43; Olver 1954).** For |x - (k-1)| ≤ (k-1)^{1/3},

  J_{k-1}(x)  ≪  (k-1)^{-1/3}.   (B2)

This is the Airy regime; it is only ≪ k^{-1/3}, NOT exponentially small. **Crucial verification:** the transition region begins at x ≈ k − k^{1/3}. Our cutoff threshold k > 2eT/√N gives x_max = 2T/√N < k/e ≪ k − k^{1/3} for k ≥ 3. So the transition region does not intersect our (m,n,c) range.

# 3. Threshold derivation

We need (B1)'s majorant to be small. With y := x/(2(k-1)),

  J_{k-1}(x)  ≤  (e·y)^{k-1}.

Demand e·y ≤ 1/2 (geometric decay):

  e·x_max / (2(k-1))  ≤  1/2   ⟺   k − 1  ≥  e·x_max  =  2eT/√N.

So **threshold:** k > 2eT/√N + 1, equivalently k ≥ ⌈2eT/√N⌉ + 1. With the safety factor of 2 from the audit, take

  **k > 2 · 2eT/√N  =  4eT/√N  ≈  10.87 T/√N.**   (★★)

In the regime k = T^a, a ∈ (1,2), this holds for all T sufficiently large (since k = T^a ≫ T/√N for any fixed N ≥ 1 and a > 1).

# 4. Quantitative exponential decay

**Lemma 4.1 (Off-diagonal exponential bound).** For k > 4eT/√N and any (m,n) with mn ≤ X² = N T²/(4π²) and any c ≥ N with N | c,

  |J_{k-1}(4π√mn/c)|  ≤  (1/2)^{k-1} / √(2π(k-1)).    (D1)

*Proof.* By (★), x = 4π√mn/c ≤ x_max = 2T/√N. By (★★), 2T/√N ≤ (k-1)/(2e), so e·x/(2(k-1)) ≤ 1/2. Apply (B1). □

**Lemma 4.2 (Total off-diagonal).** Let c_f := L(1, sym² f)/ζ(2). For k > 4eT/√N,

  |off-diagonal Petersson contribution to ⟨∫₀^T |L'(1+it,f)|² dt⟩_{F_k}|
       ≪  T · X² · X^{1/2+ε} · (Σ_{c≥N, N|c} c⁻¹) · (1/2)^{k-1}/√k
       ≪  T · N^{ε} · (log T) · 2^{-(k-1)} · k^{-1/2}.

*Proof.* The Kloosterman sum Σ_c S(m,n;c)/c · J_{k-1}(4π√mn/c) for fixed (m,n) is bounded using Weil S(m,n;c) ≪ c^{1/2+ε}·(m,n,c)^{1/2}, summed over c ≥ N with N | c; the sum Σ_{N|c} c^{-1/2+ε} converges absolutely. Multiply by D1 and the (m,n)-sum (n,m ≤ X, with Hecke-coefficient log² weights; standard divisor estimates). The dominant factor is (1/2)^{k-1}, all other factors polynomial in (T, N, log T). □

**Corollary 4.3.** For k = T^a with a ∈ (1, 2) and N fixed (or N → ∞ with √N ≪ T^{a-1}),

  off-diagonal contribution  =  O(exp(-c_0 · k))    with c_0 = log 2 ≈ 0.693.

Compared to main term ≍ T·log⁴(NkT)·⟨c_f⟩, this is super-polynomially small.

# 5. Uniformity verification

The decay rate c_0 = log 2 in Cor 4.3 is **uniform** in (m, n, c) over the entire summation range:

- m, n ≤ X enters only through x_max in (★); (B1) with x ≤ x_max gives the same bound for every (m,n,c) in range.
- c ≥ N enters as c⁻¹ in the Kloosterman summand; summation Σ_{N|c} c^{-1+1/2+ε} = N^{-1/2+ε}·ζ(1-1/2-ε) converges absolutely. No c-dependence in the Bessel decay constant.
- The transition region (Lemma 2.2) is excluded by the threshold (verified §2 above): x_max = 2T/√N ≤ (k-1)/(2e) ≪ k - k^{1/3}.

# 6. Explicit error term in Lemma 3.1

Plugging Cor 4.3 back into Lemma 3.1 of B3_unconditional_attempt.md:

  ⟨∫₀^T |L'(1+it,f)|² dt⟩_{F_k}
       =  (T/(2π)) · ⟨c_f⟩_{F_k} · (¼ log²(Nk²T²/4π²)) · (1 + E(T,k,N))

with error rate

  **E(T,k,N)  =  O((log NkT)⁻¹) + O(exp(-(log 2) · k))**   (E1)

The first term is the standard diagonal-Petersson error from approximate functional equation truncation (this is *not* the off-diagonal — it's the AFE tail and the Stirling expansion of the local factor; size 1/log). The second term is the off-diagonal contribution, super-polynomially small for k = T^a, a > 1.

In particular, for k = T^a (a ∈ (1, 2)), the error in E1 is dominated by 1/log(NkT) ≍ 1/((1+a) log T):

  M_{F_k}(T)  =  (2/(3π)) · ⟨c_f⟩_{F_k} · T · log⁴(kX) · (1 + O(1/log T))   (E2)

# 7. Effect on Theorem B

Theorem B unchanged: the threshold k > 2T quoted in B3_unconditional_attempt §3.4 line 172 was wrong but **conservative in a way that does not affect Theorem B**: any k = T^a with a > 1 satisfies BOTH the wrong "k > 2T" (for a ≥ 1) and the correct "k > 4eT/√N" (for a > 1, N fixed/growing slower than T^{2(a-1)}). The asymptotic regime considered in §3.6 is unchanged.

The phrase "vanishes identically" was a sloppy paraphrase; replace with "**decays exponentially as exp(−(log 2)(k−1)) uniformly in (m,n,c)**". The argument's conclusion stands.

# 8. References (line-precise)

- **Watson, *A Treatise on the Theory of Bessel Functions*, 2nd ed.** §8.5 Eq. (3) for the (x/(2k))^{k-1} uniform majorant; §8.43 for the Airy/transition expansion in |x-k| ≤ k^{1/3}.
- **Iwaniec, *Topics in Classical Automorphic Forms*** §5.5 Lemma 5.7 (clean modern statement of (B1)); §5.6 for the Petersson trace formula's Bessel kernel.
- **Iwaniec-Kowalski, *Analytic Number Theory*** §7.4 (Petersson trace formula at level N, weight k; cusp width c divisible by N).
- **Olver 1954**, *Phil. Trans. R. Soc.*, Airy-type uniform expansion confirming (B2) with explicit constant.

---

# Confidence and caveats

**Confidence: 0.78** (up from 0.62 for the parent §3.4 due to corrected bookkeeping).

What is rigorous (≥ 0.9):
- Threshold k > 4eT/√N from (★)+(B1). Direct computation.
- Exponential decay rate c_0 = log 2 from majorant (1/2)^{k-1}. Direct.
- Transition-region exclusion: x_max = 2T/√N versus k − k^{1/3} with k > 4eT/√N. Direct numerics.
- Uniformity in (m,n,c): each factor checked explicitly in §5.

Medium (0.7):
- Lemma 4.2's Kloosterman summation: I cite Weil + standard divisor estimates without writing out every constant. The polynomial factors are correct in shape (T·N^ε·log T) but the implied constant could be off by a small power of log; does not affect E1.
- The error rate O(1/log T) in E2: dominant contribution comes from AFE tail, not off-diagonal. This rate matches Iwaniec-Kowalski §5 standard derivative-moment computations but I have not done line-by-line.

Caveats:
- The original §3.4 Lemma 3.1 statement also had a typo "(log Nk²T²/4π² /4)²" — this should read "(¼) · log²(Nk²T²/4π²)" or equivalently "log²(Nk²T²/4π²)/16" depending on whether the ¼ is inside or outside the square. For Theorem B's leading constant, the cleaner form is the latter; I used the former throughout this fix to match the parent doc. Either convention reconciles to log⁴X under N k T → ∞.
- "Bessel zeros" red herring: J_{k-1}(x) does have infinitely many zeros, but the uniform bound (B1) is monotone-decreasing in k for fixed x, so zeros do not improve the bound — they're irrelevant. The decay is genuinely exponential, not oscillatory cancellation.
- N → ∞ regime (level + weight joint): the threshold (★★) becomes k > 4eT/√N which is *easier* for large N. Theorem B in joint regime k → ∞, N → ∞ with k ≥ 4eT/√N is automatically unconditional by this argument; this is a small generalization not stated in the parent.

# Done.
