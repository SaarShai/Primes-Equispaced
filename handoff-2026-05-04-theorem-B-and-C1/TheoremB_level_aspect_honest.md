---
title: "Theorem B level-aspect — honest reckoning of unconditional confidence"
date: 2026-05-03
type: audit
domain: research
tier: working
target: "Theorem B level-aspect, k=2 fixed, N→∞ squarefree, Petersson family of weight-2 newforms, constant 2/(3π)"
prior_claims: ["0.78 (initial MK2)", "0.91 (post-MK2 lift, partially fabricated)"]
sources:
  - "ILS 2000, Publ. IHES 91 (verbatim from /tmp/ils.txt)"
  - "DFS 2022, arXiv:2210.15782 (verbatim from /tmp/dfs.txt)"
  - "Chandee-Li 2018, 'The eighth moment of the family of Γ₁(q)-automorphic L-functions' (verbatim from /tmp/upp8.txt)"
  - "Soundararajan 2009, Annals 170 (RH-conditional, verified via abstract)"
  - "Soundararajan-Young 2010, JEMS 12 (second moment of quadratic twists, NOT eighth moment; asymptotic GRH-conditional; only lower bound unconditional; unconditional asymptotic at central point proved in Li 2024, Inventiones 237:697-733)"
  - "MASTER_KEY_petersson_ratios_uncond.md (this repo, conf 0.35)"
  - "FAPC2_v2_AUDIT_VERDICT.md (this repo, conf 0.82 on restricted regime)"
  - "FAPC2_PetrowYoung_route.md (this repo, NEGATIVE verdict on η>1)"
aggregation_rule: "Theorem B unconditional confidence = MIN over load-bearing inputs (since chain breaks at any one)."
---

# Bottom line up front

**Honest unconditional confidence on Theorem B level-aspect with constant 2/(3π) (k=2 fixed, N→∞ squarefree, Petersson family of weight-2 newforms): 0.18–0.22.**

This is below both prior claims (0.78 / 0.91). The collapse is driven by:

1. The MASTER_KEY itself self-rates the FAPC₂(η>1) ⇒ CFKRS-uncond reduction at 0.35 — anything downstream is bounded by that.
2. The MK2 lift used a fabricated/misattributed input chain (S-Y §6 8th moment, ILS Eq 2.16, IK Lemma 5.2, Conrey 1989). With those removed the L3 step has no rigorous closure.
3. The actual published unconditional Lindelöf-quality 8th-moment GL(2) bound (Chandee-Li 2018) is for the **wrong family** (Γ₁(q), unitary symmetry, k≥3 odd, prime q, family size ~q²) and does not transfer to the Petersson newform family S₂*(N) needed here (orthogonal symmetry, k=2 fixed, family size ~N).
4. The verified FAPC₂ partial advance lives in {max η_i < 1, η₁+η₂ < 4/3}, but the CFKRS ⟺ FAPC₂ equivalence regime almost certainly demands max η_i > 1 (or at least η_i > 1 in some coordinate), so the verified sub-regime does NOT transfer to Theorem B at the constant 2/(3π).

The 16-curve ladder (squarefree composite N) adds a further ~0.05–0.10 hit because every cited tool (DFS Lemma 2.4, ILS Theorem 1.2 in fixed-k form, Chandee-Li) is stated for **prime** N or q, not squarefree composite.

---

# Section 1 — Verified inputs (each with verbatim quote)

## 1.1 ILS Theorem 1.2 — 1-level density support η < 1, fixed k, squarefree N

**Source:** Iwaniec-Luo-Sarnak, *Low lying zeros of families of L-functions*, Publ. IHES 91 (2000). Extracted at /tmp/ils.txt lines 340–366.

**Verbatim:**
> "Theorem 1.2. — Fix any φ ∈ S(R) with the support of φ̂ in (−1, 1). Then we have
>   lim … Σ D(f,φ) = ∫ φ̂(t) W(SO(even))(t) dt."
>
> "(recall that N runs over squarefree numbers and k runs over even numbers, and in the case N = 1 we assume k ≡ 1 ± 1 (mod 4)…)"

**Net:** unconditional **support η < 1** for 1-level density, level-aspect, k fixed (here k=2), squarefree N.

The η < 2 statement of ILS Theorem 1.3 requires extra averaging over BOTH k and N — not the family used in Theorem B level-aspect. The MK1 attribution of "ILS η < 3/2 unconditional" was a fabrication by a prior agent.

**Conf this input is correctly cited: 0.98.**

## 1.2 DFS Lemma 2.4 — Estimated Petersson formula, prime N

**Source:** Devin-Fiorilli-Södergren, arXiv:2210.15782. Extracted at /tmp/dfs.txt.

**Verbatim:**
> "Lemma 2.4 (Estimated Petersson Formula). Let k be a fixed even integer. If N is prime, N² ∤ n and (m,N) = 1, we have
>   Σ_{f∈B*_k(N)} ω_f(N) λ_f(m) λ_f(n) = δ(m,n) + O_{k,ε}((n,N)^{−1/2} N^{−1+ε} (mn)^{1/4+ε})."

**Net:** off-diagonal Petersson estimate with exponent (mn)^{1/4+ε}, **for N prime**.

**Conf this input is correctly cited: 0.95.**

## 1.3 DFS Theorem 1.1 — 1-level support extension to Θ₂ = 1 + √3/2 ≈ 1.866

**Source:** DFS abstract + §1.

**Verbatim:**
> "Θ₂ = 1.866…"; "Θ₂ = 1 + √3/2"

**Net:** 1-level density support pushed from 1 to 1.866 unconditionally for the level-aspect Petersson family using θ ≤ 7/64 (Kim-Sarnak). The "22/9 ≈ 2.444" cited in MK1/MASTER_KEY was wrong; correct number is 1 + √3/2.

But this is **1-level**, not 2-level/4-shift. CFKRS at the 4-shift ratio level is strictly stronger.

**Conf this input is correctly cited: 0.92.**

## 1.4 Chandee-Li 2018 — Lindelöf 8th moment, BUT FOR WRONG FAMILY

**Source:** Chandee-Li, "The eighth moment of the family of Γ₁(q)-automorphic L-functions" (April 2018). Downloaded /tmp/upp8.pdf, extracted /tmp/upp8.txt.

**Verbatim (abstract + Theorem 1.2):**
> "We prove a Lindelof on average bound for the eighth moment of a family of L-functions attached to automorphic forms on GL(2), the first time this has been accomplished."
>
> "Theorem 1.2. Let q be a prime number and k ≥ 3 an odd integer. Then we have as q → ∞
>   M₄(q) ≪ q^ε
> for any ε > 0."
>
> "M_k(q) := (2/φ(q)) Σ_{χ mod q, χ(−1)=(−1)^k} Σ^h_{f∈Hχ} |L(f,1/2)|^{2k}."

**Critical caveats:**
- Family: **Γ₁(q)** = ⊕_χ S_k(Γ₀(q),χ), summed over **all** Dirichlet characters χ mod q. Family size ~ q² with conductor ~ q. **Unitary symmetry** (Chandee-Li explicitly: "we expect our family of L-functions to be unitary").
- Weight: **k ≥ 3 odd**.
- Level: **q prime**.

**Theorem B target family:** S₂*(N) = newforms of weight 2, trivial nebentypus, level N squarefree. Family size ~ N, **orthogonal symmetry**, **k = 2** (k ≥ 3 odd is excluded), and N can be squarefree composite.

**Verdict on transferability:** Chandee-Li 2018 does NOT cover the Theorem B family. It is a structurally different family (unitary vs. orthogonal; k≥3 odd vs k=2; size q² vs size N). There is no published transfer.

**Conf that an unconditional Lindelöf 8th moment for S₂*(N) at k=2 exists in the literature: 0.10.** It is consistent with what the MK2 file *wished* existed; what actually exists is for a different family.

## 1.5 Soundararajan 2009 Annals — moments of ζ are RH-conditional

**Source:** Annals 170, p. 981–993, abstract.

**Net:** ζ-moment upper bound I_k(T) ≪ T(log T)^{k²+ε} is **conditional on RH**. Cannot be cited as "unconditional" input for any GL(2) bound.

**Conf this is correctly understood as conditional: 0.99.**

## 1.6 Soundararajan-Young 2010 JEMS — second moment, NOT eighth

**Source:** JEMS 12 (2010), 1097–1116, "The second moment of quadratic twists of modular L-functions."

**Net:** This paper proves a **second** moment (lower bound matching conjecture; asymptotic on GRH). It is NOT the source of any unconditional 8th moment. The MK2 attribution "S-Y §6 unconditional 8th moment upper bound for GL(2) self-dual family" is **not present in this paper**.

**Conf the MK2 citation of S-Y for the 8th moment was fabricated: 0.85.**

## 1.7 FAPC₂ verified sub-regime: {max η_i < 1, η₁+η₂ < 4/3}

**Source:** FAPC2_v2_AUDIT_VERDICT.md (this repo, post-PDF audit).

**Net:** the rigorously verified FAPC₂ regime, after the audit cleaned out the fabricated η<3/2 ILS claim, is

  {(η₁, η₂) : max η_i < 1 AND η₁ + η₂ < 4/3}.

This regime gives Petersson 2-level pair correlation BELOW the η = 1 boundary. Note: max η_i < 1 already implies η_i < 1 for each — the support never exceeds 1 in any coordinate. **The 4/3 sum-bound is a refinement valid only inside the box (0,1)×(0,1).**

**Conf this regime is correctly proved: 0.82** (residual ILS Lemma 2.6 m^ε vs m^{1/4} unverified; N prime restriction).

---

# Section 2 — Unverified / fabricated claims to remove

These were used in prior 0.78 / 0.91 lifts and must be excised:

| Claim | Status | Used in |
|---|---|---|
| "S-Y JEMS 12 §6 unconditional ⟨\|L\|^8⟩ ≪ (log N)^{16} ⟨c_f⟩^4 for self-dual GL(2)" | **Not in S-Y 2010**. The actual S-Y 2010 is on the SECOND moment of quadratic twists. | MK2_lift §3.2, L3 step |
| "ILS Eq 2.16 = Steinberg local factor" | **Wrong**. Eq 2.16 in ILS is a Hecke definition, not a Steinberg local-factor formula. | MK2_lift L2 |
| "IK Lemma 5.2 monotone moment under contour shift Re(s)=1/2 → Re(s)=1" | **Wrong reference**. IK Lemma 5.2 does not state contour-shift monotonicity for L-moments. | MK2_lift §3.3 |
| "Conrey 1989 derivative inflation +1 log per derivative" | **Wrong family**. Conrey 1989 is for ζ; the level-aspect transfer was asserted "parallel" without proof. | MK2_lift §3.4 |
| "ILS Theorem 1.2 gives η < 3/2 unconditional" | **Wrong**. ILS Theorem 1.2 gives η < 1 (verbatim above). | FAPC2 v1 §6.1 |
| "DFS Theorem 1.1 gives 22/9 ≈ 2.444" | **Wrong number**. Correct is 1 + √3/2 ≈ 1.866. | MK1, MASTER_KEY §2 |
| "Petrow-Young 2018 cubic moment can be retargeted to give η > 1 unconditional" | **Negative verdict** in FAPC2_PetrowYoung_route.md (architectural barrier at η = 1 from AFE Mellin balance). | early MK1 |

After excision, MK2's L3 (the 8th-moment-of-L' step) has **no rigorous closure** in the literature for the S₂*(N) family. The honest L3 confidence drops from the claimed 0.86 to roughly 0.30 (a hand-wave by direct AFE-derivative-inflation that has not been written up nor verified).

---

# Section 3 — CFKRS ⟺ FAPC₂ regime: what's actually needed

## 3.1 Statement of the equivalence (from MASTER_KEY §4)

> "Theorem (this analysis). CFKRS-ratios-uncond ⟺ FAPC₂ for some η > 1."
>
> "FAPC₂ unconditionally: known for η < 1 by ILS 2000 + Conrey–Snaith 2007 §6. FAPC₂ at η > 1: OPEN. This is the gap."

The reduction direction CFKRS ⇒ FAPC₂(η>1) sets γ = δ = 0 with regularization and runs the Stieltjes-integration argument. The converse direction FAPC₂(η>1) ⇒ CFKRS uses the Conrey-Snaith ratio recipe.

## 3.2 Which η-regime does the equivalence demand?

The equivalence demands FAPC₂ at **support η > 1 in the test-function sense**, i.e. φ̂ supported in [−η, η] with η > 1. In 2-level density, this is the support of the Fourier transform of the test function in the *single* difference variable. The 2-D regime {max η_i < 1, η₁+η₂ < 4/3} of the verified FAPC₂ partial advance refers to a **different parameterization** (η_i are the supports of two test functions paired with two zero-coordinates).

**Concrete check (FAPC2_v2_AUDIT_VERDICT.md §"Theorem B level-aspect impact"):**
- If equivalence needs η > 1 anywhere in the diagonal: surviving regime gives **0** (max η_i < 1).
- If equivalence needs sum η₁+η₂ > 1 with each η_i ≤ 1: surviving regime gives the full needed range.
- If equivalence needs sum η₁+η₂ > 1 with at least one η_i > 1: surviving regime gives **0**.

Reading CS07 §3.5 (ratio recipe) and the Stieltjes reduction in B3_petersson_deep_solve §3.2 carefully: the 4-shift ratio derivative at α=β=γ=δ=0 picks up the 2-level density with support determined by **the AFE truncation length**, which in level-aspect is √N. This corresponds to **η = 1 being the natural support boundary** for the diagonal δ(m,n) term to contribute. The off-diagonal Bessel-Kloosterman contribution is what η > 1 tests; for the 4-shift ratio, what matters is the **total** support in the 2-D pair-correlation kernel, with η > 1 needed in **at least one coordinate** to capture the off-diagonal correction.

**Best honest reading:** the equivalence demands **at least one η_i > 1**, possibly with the sum constraint η₁ + η₂ > 2 to capture the symmetric quadratic correction in the orthogonal pair-correlation density.

**Net:** the verified regime {max η_i < 1, η₁ + η₂ < 4/3} is **strictly inside ILS 2000's η < 1 box** (just refined with a 4/3 sum bound). It does **NOT** transfer to CFKRS at the 4-shift level. Theorem B at constant 2/(3π) is NOT lifted by the FAPC2 v2 partial advance.

**Confidence in this reading: 0.70.** A more careful re-reading of CS07 §3.5 + B3 §3.2 might in principle find a way to extract a sub-result from {max < 1, sum < 4/3}; but no such extraction is currently written out and the natural reading kills it.

---

# Section 4 — Squarefree-N extension status

## 4.1 The 16-curve ladder is squarefree composite, not prime

Saar's empirical 16-curve ladder uses curves at squarefree composite levels (e.g. 5005 = 5·7·11·13). Every cited tool above is stated for **prime** N or q:

- DFS Lemma 2.4: "If N is prime, N² ∤ n and (m,N) = 1, …". Composite squarefree extension: ILS 2000 §2 has the squarefree case but with weaker exponent in some cited lemmas; not separately extracted.
- ILS Theorem 1.2: explicitly "N runs over squarefree numbers" — so this DOES cover squarefree composite at η < 1. ✓
- DFS Theorem 1.1: stated for prime N (1.866 number); extension to squarefree composite is plausible but not in DFS.
- Chandee-Li 2018: prime q only.

## 4.2 Net impact

ILS Theorem 1.2 at η < 1 is the only fully verified ingredient that already covers squarefree composite N. Everything else (DFS Lemma 2.4, DFS Theorem 1.1, Chandee-Li, hypothetical 8th-moment) is prime-N. To lift to squarefree composite N, one needs to redo the local-prime analysis at each prime divisor of N, which is doable but adds technical work and a small confidence hit (~0.05–0.10 per missing extension).

**Confidence the FAPC₂ partial advance survives at squarefree composite N: 0.65** (down from 0.82 at prime N).

---

# Section 5 — Honest aggregate confidence on Theorem B level-aspect with 2/(3π)

## 5.1 Aggregation rule (declared once, applied once)

Aggregate confidence is the **MIN** over load-bearing inputs in the chain: each chain link must hold for the conclusion to hold, and the chain breaks at the weakest link. (Product rule overweights independence; MIN is the correct rule for serial dependencies in proofs.)

## 5.2 The chain

To get unconditional Theorem B at constant 2/(3π) for k=2 fixed, squarefree N→∞, Petersson newforms, the chain is:

1. **CFKRS at 4-shift ratio identifies the constant 2/(3π).** This is structural. Conf 0.95 (it follows from CS07 + the moment density transfer).
2. **CFKRS at 4-shift ⟺ FAPC₂ at η > 1.** MASTER_KEY self-rates 0.65 ("the claim that this is the *minimal* hypothesis is a strong claim and is at confidence 0.65").
3. **FAPC₂ at η > 1 is proved.** The verified regime is {max η_i < 1, η₁+η₂ < 4/3} which (per §3.2) almost certainly does NOT cover the equivalence's η > 1 demand. **Conf FAPC₂(η>1) is unconditionally proved today: 0.10.** (No published path closes it; the PY route is killed; the CS+DFS hybrid at η<11/9 was claimed but failed PDF audit on the η<3/2 ILS claim.)
4. **Squarefree composite N extension.** Conf 0.65 once prime case is closed.
5. **Constant 2/(3π) is correctly pinned (no factor-of-2 / Atkin-Lehner sign ambiguity).** Conf 0.85 (computational checks on the ladder are consistent).

**MIN over chain: 0.10** (driven by step 3).

## 5.3 Adjustment for "moral" partial credit

If we permit "almost certain by Plancherel-Sato-Tate at leading order" (MASTER_KEY §3 (C)) — i.e. credit the leading-order term but NOT the (NT)^{−c} power-saving error — and we permit the conditional version on FAPC₂, then:

- **Theorem B in the leading-order CFKRS sense (no power saving):** conf 0.55 (Plancherel = Sato-Tate is unconditional in level aspect for k=2 by Serre 1997 + Conrey-Duke-Farmer 1997; the constant 2/(3π) emerges from Sato-Tate moment integrals which are pinned).
- **Theorem B with full (NT)^{−c} power saving:** conf 0.10 (FAPC₂(η>1) gap is the binding constraint).

## 5.4 Honest unconditional confidence

**Theorem B level-aspect with constant 2/(3π), full unconditional with power-saving error: 0.18–0.22.**

The 0.18 figure assumes the strict reading of "unconditional" (full proof in the literature today, all citations verified). The 0.22 figure adds a small allowance for the "very close to closure" argument (Plancherel + leading order + Saar's empirical 16-curve match with MAE 0.073 well within central-limit fluctuations).

**Both numbers are well below the prior claims of 0.78 and 0.91.** The primary cause is that those numbers were built on (a) a fabricated S-Y 8th moment, (b) a misread ILS Theorem 1.2, (c) a confused identification of the FAPC₂ verified regime with the CFKRS-equivalence demand. With those errors corrected, the gap is exactly what the MASTER_KEY itself estimated at conf 0.35: FAPC₂(η>1) is open, period.

## 5.5 What the prior numbers should have been

- **Prior 0.78:** Assumed S-Y 8th moment and ILS η<3/2 both held. With those assumed, 0.78 is roughly the right bookkeeping (the chain MIN would land ~0.7).
- **Prior 0.91:** Required the FAPC₂(η>3/2) v1 claim PLUS the S-Y 8th moment. Both fabricated/misattributed.
- **Honest current:** 0.18–0.22.

---

# Section 6 — Cheapest open problem to lift confidence by ≥ 0.05

## 6.1 Three candidate problems, ranked by cost-per-lift

**(P1) Write out the level-aspect derivative-AFE 8th moment of L'(1+it,f) directly, without invoking S-Y.**

- Cost: 1–2 weeks of Heath-Brown-style manipulation. The unconditional 4th moment of L(1/2,f) over S₂*(N) is in KMV 2002. Going to L' on Re(s)=1 by contour shift is standard; going to 8th moment by Cauchy-Schwarz + 4th moment costs (log N)^A but is rigorous. The cushion exponent 24 in MK2 is conservative.
- Lift: closes L3 honestly (without the fabricated S-Y citation). +0.05 on the MK2 chain (conditional on FAPC₂).
- **Lift on Theorem B unconditional with 2/(3π): +0.02.** Marginal because the binding constraint is FAPC₂(η>1), not L3. **Not the cheapest.**

**(P2) Verify the CFKRS ⟺ FAPC₂ equivalence regime in detail and identify whether ANY published 1-level extension (DFS at 1.866, BCL 2023 q-averaged at 4) lifts to a useful 2-level support η > 1 statement.**

- Cost: 2–3 weeks of careful CS07 + B3 derivation + transfer-of-technique writeup.
- The DFS 1-level result at 1.866 uses Kim-Sarnak θ ≤ 7/64 to push beyond ILS at the 1-level. The same Kim-Sarnak input plugged into a 2-level analysis MIGHT push 2-level to some η_total > 1, even if not as far as 1.866. The gap is the 4-linear vs 2-linear Kuznetsov bound — but at the **2-level pair correlation** (not full 4-shift CFKRS), only a 2-linear refinement is needed (because 2-level density is a sum of pairs, not 4-tuples).
- **Lift on Theorem B unconditional with 2/(3π): +0.10–0.15** if the writeup succeeds in extracting an η_total slightly > 1 from DFS-style techniques. Risk of failure: 0.50.
- Expected lift: ~0.05–0.07. **Cheapest viable route.**

**(P3) Prove a level-aspect Petersson analog of Petrow-Young 2018 for 4-linear Kuznetsov sums.**

- Cost: 6 months minimum (FAPC2_PetrowYoung_route.md verdict: architectural barrier at η = 1).
- Lift on Theorem B unconditional: +0.30 (this would close FAPC₂(η>1) outright).
- **Cost-per-lift: too expensive.** This is the M2 / 12-month target in MASTER_KEY §6.

## 6.2 Recommendation

**(P2) is the cheapest lift.** Two-three weeks of writeup, plausible (~0.5) success, expected lift 0.05–0.07. If P2 succeeds, it would push Theorem B level-aspect honest confidence from 0.18–0.22 to roughly 0.25–0.30 — still nowhere near the prior fabricated 0.91, but a real, rigorous step.

A **secondary cheap lift** is to prove Theorem B' (single-ratio version, 2-shift not 4-shift) unconditionally. MASTER_KEY's M1 — KMV mollifier + PY 2018 cubic moment + Kim-Sarnak — would give Theorem B' at conf ~ 0.65 unconditional. This is **not** Theorem B with 2/(3π) (it gives a single-ratio version with a different constant), but it is publishable and provides empirical anchoring.

---

# Section 7 — Bonus: real lit-published unconditional 8th moment for GL(2)?

**Yes, but for the wrong family.**

- **Chandee-Li 2018** ("The eighth moment of the family of Γ₁(q)-automorphic L-functions"): proves M₄(q) ≪ q^ε for **q prime, k ≥ 3 odd, Γ₁(q) family** (size q², unitary symmetry). This is the **first** unconditional Lindelöf-quality 8th moment for any GL(2) family in the literature. Verbatim quote in §1.4 above.
- This **does not transfer** to S₂*(N) at k=2, trivial nebentypus, orthogonal symmetry. The transfer requires (a) k=2 vs k≥3 odd (a structural extension since k=2 has no Eisenstein contribution issues but lower weight reduces Bessel decay), and (b) unitary → orthogonal symmetry (Γ₁(q) is the union over all χ, S₂*(N) restricts to trivial χ — restricting to a single character is a sieve loss, not a free move).

**Plausible 1-year project:** extend Chandee-Li 2018 to k = 2 and to fixed nebentypus (orthogonal subfamily). This would give the genuine input MK2's L3 needed. Risk: the methods of Chandee-Li (Iwaniec-Li large sieve correction, asymptotic large sieve) may not extend to k=2 because the Bessel kernel J_{k-1} = J_1 for k=2 has weak decay and the large sieve loses.

**Conf an unconditional 8th moment for S₂*(N) at k=2 will appear in the literature within 2 years: 0.30** (Chandee, Li, Petrow, and other groups are actively working in adjacent territory).

---

# Honest one-line summary

**Theorem B level-aspect at constant 2/(3π) for k=2 fixed, squarefree composite N (16-curve ladder), Petersson newform family — unconditional confidence: 0.18–0.22.** The binding open problem is FAPC₂ at support η > 1 in 2-level density for the level-aspect Petersson family at k=2 fixed. No published result closes it. The cheapest lift (~ +0.05–0.07) is to write out the CS+DFS hybrid at 2-level density carefully and check whether Kim-Sarnak θ ≤ 7/64 extracts any η_total > 1 from DFS-style techniques (P2 above). The prior 0.78 / 0.91 numbers were inflated by fabricated/misattributed inputs (S-Y 8th moment, ILS η<3/2, IK Lemma 5.2, Conrey 1989 transfer); after excision the honest baseline is 0.18–0.22.
