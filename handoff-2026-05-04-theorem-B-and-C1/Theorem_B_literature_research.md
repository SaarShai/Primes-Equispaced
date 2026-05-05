---
title: "Theorem B Prior Art: Petersson-family-averaged second moment of L'(ρ_f, f)"
date: 2026-05-03
status: RESEARCH COMPLETE
confidence: 0.90
---

# Section 1: Verdict — Does a Proof Exist?

**Single-form M-N Conjecture (16): NO proof exists.**

M-N Conjecture (16) (Milinovich–Ng, arXiv:1306.0854 / PLMS 109 (2014) 1465–1506):

> Let f ∈ H_k(q, χ), c_f as in eq. (1), X = √(qT)/(2π). Then:
>
>     Σ_{0<γ_f≤T} |L'(ρ_f, f)|² = (2/(3π)) c_f T log⁴X + O(T log³X)

This is **stated as a conjecture** (labeled Conjecture, derived via CFKRS ratios heuristic and Conrey–Snaith). It is NOT proved. It is equation (16) in the paper. Source: PDF directly extracted, page 10. URL: https://arxiv.org/abs/1306.0854

**Family-averaged version: NO proof exists.**

No paper in the literature proves (or even states) the Petersson-family-averaged version:

    (1/|F_N|) Σ_{f ∈ F_N} Σ_{0<γ_f≤T} |L'(ρ_f, f)|² ~ (2/(3π)) · (avg c_f) · T log⁴X

with constant 2/(3π). No unconditional proof of any version of (16) was found.

---

# Section 2: Closest Existing Results

## 2.1 M-N Theorem 1.2 (closest to (16), GRH-conditional, single form)

From arXiv:1306.0854, Theorem 1.2 (assuming GRH for L(s,f)):

> "(A_f + o(1)) T log⁴(√qT/2π) ≤ Σ |L'(ρ_f,f)|² ≤ (B_f + o(1)) T log⁴(√qT/2π)"

where A_f = ((17 − √145)/(12π)) c_f ≈ 0.126 c_f and B_f = ((17 + √145)/(12π)) c_f ≈ 2.717 c_f.

These are an upper and lower bound with constant ratio B_f/A_f ≈ 21.6. The conjectured constant 2/(3π) ≈ 0.212 falls strictly between A_f and B_f.

**Status: GRH-conditional bounds, NOT an asymptotic, NOT unconditional.**

## 2.2 Gonek's ζ result (analogue for Riemann zeta, proved under RH)

Gonek (1993, ref [21] in M-N): Σ_{0<γ≤T} |ζ'(ρ)|² = (T/(24π)) log⁴T + O(T log³T), assuming RH.

Constant 1/(24π) ≈ 0.0133 vs. 2/(3π) ≈ 0.212 — the difference by factor ~16 is because ζ is degree-1 and L(s,f) is degree-2. M-N note this explicitly (pp. 10–11): "since L(s,f) is degree two, establishing (16) is comparable to establishing [the degree-4 zeta moment]."

**Status: proved under RH, single form, Riemann zeta only, not modular L-functions.**

## 2.3 Ng 2004/2007 fourth moment of ζ'(ρ) (Duke / Mathematika)

- Ng (2004) Duke Math J 125(2): second moment of ζ'(ρ) (= k=2 case of J_k(T)), lower/upper bounds.
- Ng (2007) Mathematika 54: discrete mean value of ζ' — Dirichlet polynomial mean value theorem techniques, under RH + large zero-free region conjecture for Dirichlet L-functions.

**Status: RH-conditional, zeta only, not modular.**

## 2.4 Milinovich–Ng lower bounds (IMRN 2014)

arXiv:0706.2321; IMRN (2014) no. 12: Assuming RH, J_k(T) ≫ (log T)^{k(k+2)} for k ∈ ℕ.

Uses Rudnick–Soundararajan method adapted for zeros. No upper bound matching the conjecture.

**Status: lower bounds only, RH-conditional, zeta not modular.**

## 2.5 Milinovich (2010): upper bounds for moments of ζ'(ρ) (BLMS 42)

Upper bounds for k-th moments, nearly matching conjectured order. Does NOT achieve the precise constant.

**Status: upper bounds only, RH-conditional, zeta not modular.**

## 2.6 arXiv:2601.06292 — discrete second moment of mixed derivatives (2026)

Full asymptotic expansion for Σ_{0<γ≤T} ζ^(μ)(ρ)ζ^(ν)(1−ρ), unconditional error O(T e^{−C√log T}), or O(T^{1/2+ε}) under RH. Leading coefficient via Laurent series around s=1, not 2/(3π). Riemann zeta only.

**Status: most general zeta result to date; unconditional polynomial in log T; not modular.**

---

# Section 3: Methodology We Can Borrow

## 3.1 Montgomery–Vaughan mean-value theorem for Dirichlet polynomials (M-N's key tool)

M-N avoid explicit formulas and Landau–Gonek sums by using:
- Montgomery–Vaughan Lemma 4.1 (mean-value theorem for Dirichlet polynomials)
- Residue theorem only
- Deligne's bound |λ_f(n)| ≤ d(n)

This is explicitly noted as a novelty in M-N (p. 9): no shifted convolution sums are needed. For family averaging via Petersson, the same Dirichlet polynomial framework applies but with Petersson trace formula replacing individual-form mean-value.

## 3.2 CFKRS ratios heuristic framework (Conrey–Farmer–Keating–Rubinstein–Snaith)

The conjecture (16) itself derived from CFKRS (2005) Proc. London Math. Soc. 91 + Conrey–Snaith (2007). The ratios conjecture framework applies to the family-averaged version analogously, predicting constant 2/(3π) for the Petersson-averaged sum.

## 3.3 Approximate functional equation for L'(s,f)

M-N Proposition 1.1 establishes:

    Σ_{T<γ_f≤2T} |Σ_{n≤X} α_{f,X}(n)/n^{ρ_f}|² = (5/(24π)) c_f T log⁴X + O(T (log T)^{4-2δ})

with δ > 1/18 (GRH). This is the key technical input. For family averaging, sum Σ_f c_f ω_f over the Petersson family and apply Petersson orthogonality.

## 3.4 Petrow–Young refined Petersson (arXiv:1608.06854, Math. Ann. 2019)

Provides asymmetric Petersson trace formula for newforms of squarefree level. Necessary for the off-diagonal analysis in the family-averaged version. Does not by itself prove the family-averaged (16).

## 3.5 Devin–Fiorilli–Södergren (arXiv:2210.15782)

1-level density beyond support 2 for fixed-level families via zero-density estimates. Technique independent from discrete-zero second moments but relevant for spectral estimates.

---

# Section 4: Citation Candidates

| Reference | What to cite for | URL |
|---|---|---|
| Milinovich–Ng (2014) PLMS | Conjecture (16), bounds A_f/B_f, cf definition | https://arxiv.org/abs/1306.0854 |
| Gonek (1993) Contemp. Math 143 | Analogue for ζ: (1/24π)T log⁴T, RH | cited as [21] in M-N; no arXiv |
| Conrey–Snaith (2007) PLMS 94 | Ratios conjecture derivation of (16) | arXiv:math/0509480 |
| CFKRS (2005) PLMS 91 | Integral moments heuristic framework | arXiv:math/0206018 |
| Milinovich–Ng (2014) IMRN | Lower bounds J_k(T) ≫ (log T)^{k(k+2)} | arXiv:0706.2321 |
| Ng (2007) Mathematika | Discrete mean value techniques | arXiv:0706.1763 |
| Petrow–Young (2019) Math. Ann. | Refined Petersson at squarefree level | arXiv:1608.06854 |
| Baluyot–Chandee–Li (2024) | 1-level density at support 4, q-averaged | arXiv:2310.07606 |
| arXiv:2601.06292 (2026) | Unconditional full asymptotic for mixed ζ^(μ)ζ^(ν) at zeros | https://arxiv.org/abs/2601.06292 |
| Devin–Fiorilli–Södergren (2022) | Fixed-N 1-level density beyond ILS | arXiv:2210.15782 |

---

# Section 5: Adjacent Open Problems and How Theorem B Relates

**Gonek's conjecture (second moment of 1/ζ'(ρ)):** Σ 1/|ζ'(ρ)|² ~ (3/π³)T. Milinovich–Ng (2011) proved ≥ half the conjectured value. Theorem B is the "positive" analogue (|L'|² rather than 1/|L'|²).

**Degree-4 zeta moment:** M-N note that proving (16) for f of degree 2 is "comparable" to proving Σ |ζ'(ρ)|⁴ ~ C·T log^9 T. This is open and harder than the degree-1 Gonek result.

**Family average vs. single form:** The Petersson-family-averaged version of (16) is strictly easier than the single-form version (averaging washes out off-diagonal). Our Theorem B targets this easier object, which is why the 2/(3π) constant should be achievable in a family-averaged sense before the individual-form version.

**1-level density:** Proving even the leading constant for the 1-level density at support > 2 for fixed-N families (as opposed to BCL's q-average) requires exactly the same off-diagonal Petersson estimate as the second-moment version. Both problems are controlled by the same Kloosterman-spectral gap.

---

# Section 6: Lean/Aristotle Formalization Status

**No formalization of any moment result for L'(ρ_f,f) exists in Lean or Mathlib.**

- Loeffler–Stoll (arXiv:2503.00959, 2025): formalizes Dirichlet L-functions and ζ in Lean, proves Dirichlet's theorem, states RH. Does NOT include modular L-functions, moments, or derivatives at zeros.
- Narayanan (arXiv:2302.14491): p-adic L-functions in Lean 3. Unrelated.
- B3_theorem_B_lean_scaffold.lean (local): our own scaffold, does not constitute a proof.

No Aristotle-based formalization relevant to Theorem B was found in the literature. The analytic prerequisites (GRH, moment asymptotics) are far beyond current Mathlib scope.

---

# Section 7: Honest Gaps in This Search

1. **Full PDF text of M-N paper was extracted via pdftotext.** Equation (16) confirmed at page 10. High confidence.

2. **Gonek 1993 primary source not verified.** The asymptotic Σ |ζ'(ρ)|² ~ (T/24π) log⁴T is cited in M-N and by other sources consistently, but the 1993 Contemp. Math. paper was not directly fetched. Risk: low (cross-cited by Ng 2007, Milinovich 2010, arXiv:2601.06292).

3. **No systematic search of unpublished preprints (2025–2026) beyond arXiv.** If there exists a very recent conditional proof of (16) not yet on arXiv, this search would miss it. Probability: low, given the difficulty and absence of any preprint announcement.

4. **Family-averaged second moment at zeros vs. second moment of central values.** The search returned many results on Σ_d L'(1/2, f⊗χ_d)² (twisted family averaging over d, central-point). These are DIFFERENT from Σ_{ρ_f} |L'(ρ_f,f)|² (averaging over zeros). arXiv:2503.14680 and arXiv:2303.16864 are the former; they do NOT address Theorem B.

5. **arXiv:2411.07630 withdrawn** (issue in Section 6 computation). The withdrawn paper was about moment of L'(1/2, f⊗χ_{8d})L'(1/2, g⊗χ_{8d}), which is a central-point moment, not at zeros.

6. **No search of MathSciNet or zbMATH.** The free web search may miss papers published only in journals without arXiv preprints. Given the audience (analytic number theorists), arXiv coverage is high.

---

## Summary Verdict

| Question | Answer |
|---|---|
| Unconditional proof of M-N (16) (single form) | **No** |
| GRH-conditional proof of M-N (16) (single form) | **No** (only cage bounds A_f, B_f) |
| Unconditional proof of family-averaged version | **No** |
| Closest unconditional result | arXiv:2601.06292 (Riemann zeta mixed derivatives, not modular) |
| Closest conditional modular result | M-N Theorem 1.2 (cage bounds, GRH) |
| Constant 2/(3π) proved anywhere | **No** (conjectured only, via CFKRS ratios) |
| Lean formalization | **None** |

Theorem B (Petersson-family-averaged, constant 2/(3π)) would be **new** and publishable as a first result toward M-N Conjecture (16) in any setting.
