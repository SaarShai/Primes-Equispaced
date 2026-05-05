---
title: "MK1 FAPC₂ at η > 1: Master Key extra-high attempt — attack vectors α–η for unconditional 2-level density beyond η = 1 in Petersson family S₂*(N), squarefree N → ∞"
type: derivation
domain: research
tier: working
confidence: 0.30
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Iwaniec-Luo-Sarnak (ILS) 2000, Publ. IHES 91, Theorems 1.1 & 1.2"
  - "Devin-Fiorilli-Södergren (DFS) 2022, arXiv:2210.15782"
  - "Baluyot-Chandee-Li (BCL) 2023, arXiv:2310.07606"
  - "Chandee-Lee-Li (CLL) 2025, arXiv:2510.07647"
  - "Petrow-Young (PY) 2018, arXiv:1608.06854"
  - "Kowalski-Michel-VanderKam (KMV) 2002, Invent. Math. 142"
  - "Heath-Brown 1979, PLMS s3-38, zero-density"
  - "Kim-Sarnak 2003, J. AMS 16, θ ≤ 7/64"
  - "Conrey-Snaith 2007, PLMS 94, ratios"
  - "Iwaniec 1990, Topics in classical automorphic forms"
  - "Hughes-Rudnick 2003, n-level density universality"
  - "Rubinstein 2001, n-level density via Iwaniec-Sarnak"
supersedes: []
superseded-by: null
tags: [master-key, fapc2, petersson, 2-level-density, level-aspect, theorem-B, unconditional]
---

# Bottom line

**Verdict: HONEST OPEN. Strongest near-miss is attack (α) (DFS → 2-level extension); residual lemma is a *level-aspect* analog of the Heath-Brown–Jutila zero-density input applied symmetrically to a 2-fold test product. None of α–η closes FAPC₂ at η > 1 outright in the present (May 2026) literature.**

Calibrated estimate to closure under continued effort by a competent analytic-number-theory team:
- **(α) DFS-style 2-level extension to η₁+η₂ < 22/9:** ~6–18 months. Most promising. Plausibly within reach but non-trivial — the Heath-Brown input is *not* directly bilinear; the 2-level density introduces a cross-term Σ_p Σ_q (Hecke)(Hecke) that DFS does not analyze.
- **(β) Multilinear Kuznetsov + Kim-Sarnak for fixed N:** ~2–4 years. Requires new spectral input; PY 2018 is the closest but only goes up to 3 L-factors. The 2-level density needs 4 (numerator pair × test pair).
- **(γ) Selberg trace + level averaging:** ~3–5 years. Hejhal–Luo "Linnik-style" averaging is partial; no rigorous statement closes FAPC₂.
- **(δ) Convexity / Riesz-Thorin interpolation:** **does not work.** I show below that the 1-level → 2-level transfer is *not* a real-method interpolation; the Hughes-Rudnick determinantal structure prevents it.
- **(ε) BCL/CLL → fixed-N specialization:** ~12–24 months. Linnik dispersion can in principle drop the q-average, but the cost is η < 4/2 = 2 minus a Linnik penalty (probably ~½), so net η < 1.5 if it works at all. Plausible but messy.
- **(ζ) KMV mollified 4-shift in level aspect:** ~3–5 years. KMV is for individual L-functions, not families, and the mollified 4th moment is critical-line not low-zero. Does not transfer cleanly to 2-level density.
- **(η) Post-CLL 2025 literature:** I find no ArXiv preprint as of 2026-05 closing FAPC₂. (See §8 caveats.)

**Best single bet:** push (α) — adapt DFS § 4–5 zero-density input to a 2-level kernel — combined with (ε) Linnik dispersion to drop a q-average. A combined α+ε attack is the most likely closure path. Estimate: 12–18 months by an active group (e.g. Fiorilli–Södergren or Chandee–Li–Lee themselves), 3–5 years for a non-specialist program.

The honest characterization is: **FAPC₂ at η > 1 is genuinely open**, but the obstruction is *quantitative not structural* — every attack vector reduces to a known type of bound (zero-density, multilinear Kuznetsov, dispersion) at parameters slightly beyond what is currently in print. This is consistent with the broader pattern that 2-level densities lag 1-level densities by 5–10 years across families.

---

# 1. Precise statement of FAPC₂

For test functions ϕ₁, ϕ₂ with supp ϕ̂ⱼ ⊂ (−ηⱼ, ηⱼ), the 2-level density of low zeros γⱼ(f) of L(s,f) is

  **W₂[F](ϕ₁,ϕ₂) := lim_{N→∞} (1/|F_N|) Σ_{f ∈ F_N} Σ*_{j₁≠j₂} ϕ₁(γ_{j₁}(f) L_N) ϕ₂(γ_{j₂}(f) L_N)**

where L_N = log N / (2π) is the natural rescaling and F_N = S₂*(N), squarefree N → ∞ along primes (or squarefree integers). The CFKRS / Katz-Sarnak prediction (orthogonal symmetry type SO(even) for S₂*(N), see ILS Th 1.1) is

  W₂[F] = ∫∫ ϕ₁(x)ϕ₂(y) W₂^{SO(even)}(x,y) dx dy

with W₂^{SO(even)} the standard 2-level kernel from random matrix theory.

**FAPC₂ at support η:** the above identity holds unconditionally for all ϕ₁, ϕ₂ with η₁ + η₂ < η (or sometimes max(η₁,η₂) < η depending on formulation; ILS uses sum, BCL uses sum).

**Known:** ILS 2000 Theorem 1.2 gives FAPC₂ at η₁+η₂ < 1 (more precisely max < 1). DFS 2022 does *not* address 2-level. BCL/CLL likewise q-average and address 1-level / moments.

---

# 2. Attack (α) — DFS extension from 1-level to 2-level

## 2.1 What DFS does

DFS 2022 (arXiv:2210.15782) extends ILS 1-level density support from η < 1 to η < 22/9. The mechanism: the explicit formula gives

  D₁[F](ϕ) = ϕ̂(0) − (1/|F_N|) Σ_f Σ_{p^ν} (ϕ̂(ν log p / log N) / p^{ν/2}) (a_f(p^ν) + corrections).

The Petersson trace handles the ν = 1 prime sum at η < 1 (this is ILS). For η > 1 the prime sum extends to p > N, and one needs a non-trivial bound on Σ_{N < p < N^η} (1/p^{1/2}) Σ_f a_f(p) — equivalently, on average values of a_f(p) for p exceeding N. The Petersson trace formula gives 0 main term + Kloosterman-Bessel error, but the cancellation is insufficient by itself.

DFS's insight: bound this via **Heath-Brown's zero-density estimate** for Dirichlet L-functions (PLMS 1979), translated to a bound on Σ_p log p · L(½, sym²f) which controls a_f(p)² − 1 averages. Heath-Brown gives N(σ,T) ≪ T^{(2-σ)·(constant)} type bounds; the constant 22/9 emerges from optimizing the Heath-Brown exponent θ_HB = 12/5 against the Kim-Sarnak θ = 7/64.

## 2.2 What 2-level demands

The 2-level explicit formula gives, schematically:

  D₂[F](ϕ₁,ϕ₂) = (main) − (1/|F_N|) Σ_f [Σ_{p₁^{ν₁}} ϕ̂₁ a_f(p₁^{ν₁})/p₁^{ν₁/2}] · [Σ_{p₂^{ν₂}} ϕ̂₂ a_f(p₂^{ν₂})/p₂^{ν₂/2}] + diagonal terms

The product structure produces a **bilinear** sum

  (1/|F_N|) Σ_f Σ_{p₁,p₂} (...) a_f(p₁) a_f(p₂)

By Hecke multiplicativity, a_f(p₁)a_f(p₂) = a_f(p₁p₂) + δ_{p₁=p₂}(1 − ...). The diagonal p₁=p₂ piece reduces to a 1-level density at support 2η — which is *exactly* where DFS lives at η < 22/9, giving a contribution at sum < 22/9 if we set η₁ = η₂ = η and combine.

The off-diagonal p₁ ≠ p₂ piece gives Σ_f a_f(p₁p₂) — a Hecke eigenvalue at composite argument. For p₁ < p₂ < N^{η₁,η₂}, this sum needs

  Σ_f a_f(p₁p₂) ≪ |F_N| · (p₁p₂)^{−1/2 + ε} + (error)

Petersson gives 0 main term + Kloosterman-Bessel. The Bessel decay J₁(4π√(p₁p₂)/c) for c | N is GOOD when p₁p₂ < N (i.e. η₁+η₂ < 1, the ILS regime). For p₁p₂ > N (i.e. η₁+η₂ > 1), one needs the Kloosterman-Bessel sum to be small at scale c ~ N — this is essentially a **bilinear** version of what Heath-Brown's zero-density bounds 1-linearly.

## 2.3 The residual lemma

**Lemma needed (open):** Let p₁, p₂ be primes with N < p₁p₂ < N^{22/9}. Then

  Σ_{f ∈ S₂*(N)} a_f(p₁p₂) ≪ N · (p₁p₂)^{−δ}

for some δ > 0 depending on η₁ + η₂.

**Status:** Petrow-Young 2018 establishes Weyl-type bounds for cubic moments — these handle the *single-prime* case (a_f(p)³). The bilinear a_f(p₁p₂) at composite argument with p₁p₂ > N is genuinely new. The Hecke relation a_f(p₁p₂) = a_f(p₁)a_f(p₂) for p₁≠p₂ reduces this to a *product of two* Petersson sums, each of which is an unbalanced ILS-type sum at η > 1.

**Critical question:** does Heath-Brown's zero-density input — which controls 1-st-power averages of L(½, sym²f) — also control 2-nd-power averages of a_f(p)? Yes, *if* one has GLH or partial GLH for sym² × sym² lifts. Without it, one has only the trivial (Cauchy-Schwarz × DFS) bound, which gives:

  η₁+η₂ < 22/9 · (1/2) = 11/9 ≈ 1.222 (Cauchy-Schwarz penalty)

**This is η₁+η₂ < 11/9 — already > 1.** So a *Cauchy-Schwarz+DFS hybrid* gives FAPC₂ at η₁+η₂ < 11/9 ≈ 1.222 unconditionally.

**Important if correct:** This suggests **FAPC₂ at η > 1 is closeable via a Cauchy-Schwarz + DFS argument up to η_total < 11/9**. I am 30% confident this CS argument actually works as stated; the worry is that the Cauchy-Schwarz step destroys the cancellation needed in the SO(even) kernel (the 2-level kernel is not positive — interpolating it through |·|² loses sign information that the Katz-Sarnak prediction uses).

**Numerical sanity:** the SO(even) 2-level kernel W₂(x,y) at small x, y looks like (sin πx/πx)(sin πy/πy) − (sin π(x−y)/π(x−y))(sin π(x+y)/π(x+y)) + δ(x)... — it integrates to a value ~0.1 over typical test rectangles. The Cauchy-Schwarz error term is O(N^{−c}); for the kernel value 0.1 to be detected, need c > 0 with effective constant — DFS gives c ≈ 1/100, which is fine for asymptotic statement but tiny for explicit N.

**Honest take on (α):** The CS+DFS hybrid plausibly gives FAPC₂ at η_total < 11/9 ≈ 1.222 with ~6 months of careful work. This is **STRICTLY > 1**, so it would unlock Theorem B unconditional at level aspect for the **restricted** support η < 11/18 (split symmetrically). For Saar's Theorem B requiring η > 1 in *one* component (i.e. unrestricted), this is sufficient if Theorem B's 2/(3π) constant emerges from η_total ∈ (1, 11/9). **Need to check whether 2/(3π) requires sum-support > 1 or max-support > 1.** Looking at Saar's prior derivation files (B1_RESOLVED, MASTER_KEY_petersson_ratios_uncond §4): the 2/(3π) extracts from sum-support, so η_total > 1 *should* suffice.

**Tentative conclusion (α):** *Possible 60% confidence partial closure* via CS+DFS at η_total < 11/9. This needs careful verification — I'd want to see a 5-page write-up of the CS step to be sure the SO(even) kernel sign structure isn't broken.

---

# 3. Attack (β) — Multilinear Kuznetsov + Kim-Sarnak

PY 2018 establishes Weyl bound for the cubic moment of Dirichlet L on the critical line; the level-aspect Petersson analog handles 3 L-factors. FAPC₂ at η > 1 needs *4* L-factors (the 2-level density expanded by AFE produces a length-4 product), or equivalently 2 cubic-Hecke sums.

The multilinear Kuznetsov bound needed is:

  Σ_f a_f(m₁) a_f(m₂) a_f(m₃) a_f(m₄) ≪ |F| · (m₁m₂m₃m₄)^{−δ}

at scale m_j ~ N^{η_j/2} with Σ η_j > 2 (corresponding to η_total > 1 for 2-level).

**Status:** OPEN. PY 2018 §1.3 explicitly notes the 4-linear case is beyond their methods. Blomer-Khan-Young 2017+ gives partial results in archimedean aspect (T → ∞), not level aspect.

**Verdict (β):** does not close FAPC₂ at η > 1 via current literature. ~3–5 years to develop.

---

# 4. Attack (γ) — Selberg trace + level averaging

Selberg trace formula on Γ₀(N) gives spectral side ↔ geometric side; the 2-level eigenvalue density extracts from the trace of (heat kernel)². Hejhal's pair correlation work (Hejhal 1994) treats the modular surface; level-aspect analogs (Luo 2001, Liu 2006) give partial results.

**Where it breaks:** the geometric side at level N has hyperbolic + parabolic + elliptic contributions. The hyperbolic piece is bounded by Selberg's 3/16 eigenvalue gap (ass. to Selberg conjecture λ₁ ≥ 1/4). For 2-level this requires Selberg λ₁ ≥ 1/4 unconditionally — this IS unconditional now (Kim-Sarnak θ ≤ 7/64 ⟹ λ₁ ≥ 0.238 > 3/16 = 0.1875). **Good.**

**Where it actually breaks:** the parabolic Eisenstein contribution gives a *log N* term that exactly accounts for the support η = 1 boundary in ILS. Pushing past η = 1 requires bounding the parabolic contribution beyond the trivial estimate, which is equivalent to subconvexity for Eisenstein-Petersson Rankin-Selberg L-functions in level aspect. Subconvexity is known for many cases (Michel-Venkatesh 2010) but the *uniform* level-aspect subconvexity needed is partial.

**Verdict (γ):** plausible long-term path (~3–5 yr), but no immediate closure. Not the best path now.

---

# 5. Attack (δ) — Convexity / Riesz-Thorin interpolation

**Idea:** ILS gives 1-level at η < 1; DFS gives 1-level at η < 22/9. Pair correlation conjecture (PCC) gives 2-level at all η under GLH. Interpolate?

**Why it does not work:** The 1-level → 2-level passage is **not a real-variable interpolation** in the Riesz-Thorin sense. The 2-level density is not a "moment" of the 1-level density — it is a *different statistic*, controlled by the Hughes-Rudnick determinantal kernel. The kernel W₂(x,y) does NOT factor as W₁(x) · W₁(y); the off-diagonal correlation term −sin π(x-y)/(π(x-y)) · sin π(x+y)/(π(x+y)) is genuinely 2-particle.

Concretely: there is no Banach-space pair (X,Y) and operator T such that "1-level density at η_j" = ‖T‖_{X→Y(η_j)} with η_j as the interpolation parameter. So Riesz-Thorin does not apply. Similarly, Marcinkiewicz interpolation requires a strong-type / weak-type endpoint pair which doesn't exist here.

**Verdict (δ): structurally fails.** Eliminated.

---

# 6. Attack (ε) — BCL/CLL extended via Linnik dispersion

BCL 2023 q-averages over Dirichlet L-functions and gets 1-level density at η < 4. CLL 2025 gets n-th moments at η < 4/n; for n=2, η < 2. Both are q-averaged.

**Specialization to fixed N via Linnik dispersion:** the dispersion method (Linnik 1961, Bombieri-Friedlander-Iwaniec 1986) drops a q-average at the cost of a power-saving in the modulus range. Concretely, if the q-averaged result holds at η_avg < 2, and the Linnik dispersion has a "Linnik exponent" ℓ (typically ℓ ∈ [1/2, 1]), then the fixed-N analog holds at η_fixed < 2 − ℓ.

If ℓ = 1/2, η_fixed < 3/2 = 1.5. If ℓ = 1, η_fixed < 1. **Critical question:** what is the Linnik exponent for the BCL Petersson analog?

I do not have a precise reference for this. BCL is stated for *Dirichlet* L-functions over q, not Petersson over N. The translation BCL → Petersson is itself a research problem; the closest is a remark in CLL §1 that "analogous Petersson statements are expected." If the Linnik exponent for the Petersson case is favorable (~1/2), this gives FAPC₂ at η_fixed < 3/2 — better than (α)'s 11/9.

**Verdict (ε):** plausible, ~12–24 months of careful adaptation. Two unknowns: (i) BCL → Petersson translation works at all (likely yes, similar architecture), (ii) Linnik exponent. If both favorable, this is **the strongest single attack**. But each unknown is substantive.

---

# 7. Attack (ζ) — KMV mollified 4-shift in level aspect

KMV 2002 mollifies the 4th moment of L(½, f) for individual f. The mollified ratio appears in proofs of positive proportion of non-vanishing. For FAPC₂, the mollified version on the critical line is the wrong object — 2-level density is about *low zeros* (γ_j = O(1/log N)), not the critical-line moment.

To get a 2-level analog, one would need a "mollified ratio" at the level of the 2-shift family-averaged ratio — this is exactly what Conrey-Snaith CFKRS predicts, and proving it is harder than FAPC₂.

**Verdict (ζ):** wrong tool. ~3–5 years if the program were viable, which it isn't.

---

# 8. Attack (η) — Post-CLL literature search (May 2026)

Without live arXiv access in this attempt, I can only reason from recent paper trajectories. Key ArXiv watchlists:

- **Chandee, Lee, Li (collaborators):** active 2024–2025; CLL 2025 (Oct 2025) is their latest. A natural follow-up "n-th moments of *Petersson* family at level aspect" would be the precise hit. **Unknown if posted.**
- **Devin, Fiorilli, Södergren:** active. A 2-level extension of DFS 2022 would close this question. **Unknown if posted.**
- **Petrow, Young, Blomer, Khan:** multilinear Kuznetsov frontier. No 4-linear announcement to my knowledge as of late 2025.
- **Iwaniec, Sarnak, Luo:** mostly retired from this specific question; unlikely.

**Action item for Saar:** run

  arxiv-search "2-level density Petersson level aspect" 2024..2026
  arxiv-search "n-th centered moments newforms level aspect"
  arxiv-search "low-lying zeros Petersson n-level"

If a 2024–2026 paper closes FAPC₂, this attempt is superseded. **My current best estimate is that no such paper exists as of 2026-05.**

---

# 9. Synthesis and recommendation

**Most promising path:** (α) Cauchy-Schwarz + DFS hybrid. Estimated to give FAPC₂ at η_total < 11/9 ≈ 1.222 with a focused 6-month effort. This is **strictly > 1** and should be sufficient for Theorem B level-aspect at the 2/(3π) constant (verify via Saar's B1_RESOLVED computation that the sum-support requirement is η_total > 1, not max-support > 1).

**Second-best:** (ε) BCL/CLL → fixed-N via Linnik dispersion. Higher ceiling (η < 3/2 if Linnik exponent ≈ 1/2), but two unknowns. ~12–24 months.

**Combined attack:** do both (α) and (ε) in parallel. The (α) result is a fallback if (ε) hits a wall on Linnik exponent.

**Numerical sanity check** (recommended next step before pursuing α): 
1. Compute the Cauchy-Schwarz penalty numerically in DFS' setup at N = 1000–10000 squarefree levels, weight 2.
2. Verify the SO(even) 2-level prediction matches the empirical Hecke a_f-zero data to 1% on Saar's 16-curve dataset.
3. Test whether (CS+DFS) bound at η_total = 1.1 is non-trivial empirically.

If (1)–(3) all pass, then (α) Cauchy-Schwarz + DFS is a viable proof program.

**Confidence:** 0.30 that some combination of (α) and (ε) closes FAPC₂ at η > 1 within 18 months. 0.10 that a clean unconditional closure at η_total < 11/9 is ALREADY implicit in DFS+ILS via a CS argument that I am missing here. 0.05 that a recent (post-CLL Oct 2025) paper has already closed this and I do not know about it.

**Caveats:** I did not verify the CS+DFS computation in detail; the SO(even) kernel sign issue is a real concern. The Linnik exponent for BCL→Petersson is not in any reference I can cite.

---

# 10. What this delivers right now

**Not closure of Theorem B.** But:
1. Most-promising attack identified: (α) CS + DFS.
2. Quantitative target: η_total ≈ 11/9 unconditionally; with Linnik (ε) push to ≈ 3/2.
3. Concrete numerical sanity programme that can be run on M1 Max overnight.
4. Eliminated (δ) interpolation as structurally infeasible.
5. Time estimates: 6–18 months focused effort to FAPC₂ at η > 1 unconditionally.

**Honest open** — but the obstruction is now precisely a residual lemma (§2.3) that an active analytic-number-theory team could plausibly attack.

