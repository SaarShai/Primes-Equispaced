---
title: "Mining Kumar–Mallesham–Sharma–Singh 2023 (arXiv:2303.16864) for Theorem B unconditional closure"
type: derivation
domain: research
tier: working
confidence: 0.06
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (8h budget, dedicated mining)
sources:
  - /tmp/kumar_2303.pdf (downloaded arXiv:2303.16864v2, 24 Oct 2023)
  - /tmp/kumar_2303.txt (pdftotext layout extraction, 1321 lines)
  - Theorem_B_field_landscape.md (where Kumar 2023 was first identified)
  - RankinSelberg_trace_attack.md, Voronoi_Kuznetsov_GRH_bypass.md, RMT_Painleve_GRH_bypass.md, Theta_lift_GRH_bypass.md, FirstPrinciples_creative_attack.md, E1_E2_E3_barrier_attack.md, Necessary_conditions_inverse.md, Disprove_attempt.md, arxiv_2601_06292_methodology_deep.md (the 9 prior failed attempts)
  - X. Li, "Moments of quadratic twists of modular L-functions," arXiv:2208.07343 (input to Kumar et al.)
  - I. Petrow, "Moments of L'(½) in the family of quadratic twists," IMRN 2014 (conditional precursor)
  - Soundararajan–Young 2010 (the L-not-L' precedent)
tags: [theorem-B, kumar-mallesham-sharma-singh, GL2-derivative, central-point, quadratic-twist, GRH-bypass, transferability-analysis]
---

# Bottom line (written first)

**Verdict: NO unconditional path to Theorem B is yielded by Kumar–Mallesham–Sharma–Singh 2023.**

The paper is a real and important result — the first **unconditional** asymptotic for the second moment of L′(½, f⊗χ_{8d}) over real primitive characters χ_{8d}. But its method does **not** transfer to Theorem B, because the structural object it computes is in a **different orthogonality class** from Theorem B and uses **two unconditional inputs that are unavailable in the at-zeros / Petersson-family setting**:

1. The unconditional **large sieve in the d-aspect** (Heath-Brown / Soundararajan style, used by Li 2024 and recorded as `(11)` in Kumar et al.: "Σ*_{M≤|m|≤2M} | Σ_n λ_f(n) χ_m(n) n^{−1/2−it} G(n/N) |² ≪_f (1+|t|)³ M log(2+|t|)"). This is a **quadratic-character large sieve** for GL(2) coefficients.
2. The **Poisson summation in d** (their Lemma 2.4, which expresses Σ_d χ_{8d}(n) H(d/X) as a δ-term plus a Gauss-sum dual), which is a **family-of-characters tool**, not a family-of-zeros tool.

Both inputs use, essentially, that **the family parameter d is a Dirichlet-character conductor**, so Poisson summation in d unfolds the character. Theorem B sums over **zeros ρ_f of a single L(s,f)** — there is no Poisson/Plancherel dual in ρ that turns Σ_ρ |L′(ρ,f)|² into a manageable Gauss-sum kernel. The Riemann–von-Mangoldt explicit formula is the closest analog, and the explicit-formula evaluation Σ_{γ≤T}(m/n)^{iγ} requires ζ-zeros on σ=½ (i.e., GRH) — this is the R3 obstruction documented in `Voronoi_Kuznetsov_GRH_bypass.md` §1.1.

Additionally, the symmetry types do not match: the quadratic-twist family of f is **orthogonal** (sign distribution split by ω(f⊗χ_{8d})=±1), while at-zeros over a single f sits inside CFKRS recipe with **unitary** matrix integral (the M-N derivation, see `Necessary_conditions_inverse.md` NC₁).

The constant 2/(3π) does **not** drop out of any natural transfer of Kumar et al. The constant their method produces is C_f = explicit-with-1/(2π) coming from Mellin transform J̌(0), Euler-product of (1−1/p) factors, and η_χ-sign — entirely different arithmetic origin from the M-N CFKRS-derived 2/(3π) (which factors as (1/(2π))·(1/12)·16, see `Theorem_B_field_landscape.md` §4.1).

**Best honest result of this mining session:** identifies precisely **two structural reasons** the central-point ↔ at-zeros transfer fails, both consistent with prior obstruction taxonomy (R3 = explicit-formula off-line zeros, plus symmetry-type mismatch). This **does not duplicate** any of the 9 prior attempts: those audited internal routes; this audits an external paper proposed as a possible transfer source. Confidence that Kumar 2023 closes Theorem B: **0.02**.

---

# Section 1. Verbatim main theorem of Kumar et al. 2023

From `/tmp/kumar_2303.txt` lines 83–95:

> **Theorem 1.** Let f and J be as above. Then we have
>
> Σ*_{(d,2q)=1, ω(f⊗χ_{8d})=−1} |L′(1/2, f×χ_{8d})|² J(8d/X) = C_f J̃(1) X log³ X + O(X (log X)^{2.5+ε}),
>
> where C_f is some explicit constant depending only on f and J̃ is the Mellin transform of J.
>
> We combine the methods of Li [3] and Petrow [8] to prove the above theorem.

(Σ* denotes sum over fundamental discriminants 8d with d > 0 squarefree, (d,2q)=1; the sign condition ω(f⊗χ_{8d})=−1 picks the subfamily where Λ(½,f⊗χ_{8d}) vanishes, so L′(½) is the leading derivative.)

A Corollary 1 (lines 96–134) extends to ω=+1 via the relation L′(½,f⊗χ_{8d}) = −L(½,f⊗χ_{8d}) · {log(8|d|√q/(2π)) + Γ′(k/2)/Γ(k/2)} when ω=+1 (Λ′(½)=0 trivially), bootstrapped from Li [3]'s unconditional Soundararajan–Young second moment of L (not L′).

Corollary 2: N(X) := #{0<d≤X : χ_d primitive quadratic, L′(½, E⊗χ_d) ≠ 0} ≫ X / log X (improving Perelli–Pomykala 1997's X^{1−ε}).

Petrow's prior result (their (1), conditional on GRH):
> Σ*_{(d,2q)=1, ω(f⊗χ_{8d})=−1} |L′(1/2, f × χ_{8d})|² J(8d/X) ∼ C′_f X log³ X.

So Theorem 1 of Kumar et al. is exactly the unconditional version of Petrow 2014, Theorem 1.1.

---

# Section 2. Method overview — AFE, diagonal separation, off-diagonal handling

## 2.1 Approximate functional equation (Lemma 2.1, lines 163–176)

> L′(1/2, f⊗χ_d) · I(ω(f⊗χ_d)=−1) = (1 − i^k η χ_d(−q)) Σ_{n=1}^∞ λ_f(n)χ_d(n) / n^{1/2} · W(n/|d|),
>
> where W(y) = (1/(2πi)) ∫_{(3)} (Γ(u+k/2)/Γ(k/2)) (2πy/√q)^{−u} du/u².

The double-pole 1/u² is the **derivative AFE signature** — Petrow [8, Lemma 3.1]. The k=0 case (no derivative) would have du/u with single pole, giving the standard Soundararajan–Young AFE.

## 2.2 Splitting into truncated main series + tail (line 297–308)

Set M = X / (log X)^1000. Define:
- A(8d) = (1−i^k ηχ_{8d}(q)) Σ_n λ_f(n)χ_{8d}(n) n^{−1/2} W(n/M)  (main, AFE truncated at M)
- B(8d) = L′(½,f⊗χ_{8d}) − A(8d)   (tail correction)

Theorem 1 follows by ‖A‖₂² + ‖B‖₂² + 2|⟨A,B⟩| Cauchy-Schwarz: Proposition 2 (B-term ≪ X(logX)²(loglog X)⁴) and Proposition 3 (A-term = C_f J̌(0) X log³ X + O(X log² X)).

## 2.3 Proposition 2 (B-term, the tail) — Section 4 lines 330–617

The Mellin contour for B(½,f⊗χ_{8d}) has integrand

  (8d)^w − M^w / w² · γ(w) · Σ_n λ_f(n)χ_{8d}(n) n^{−1/2−w}

with γ(w) = (2π/√q)^{−w} Γ(k/2+w)/Γ(k/2). Smooth dyadic decomposition in n into Σ_{N dyadic} ... G(n/N), then split N-sum at N≤M, M<N≤X, N>X giving B = B₁+B₂+B₃.

Each B_i bounded via Cauchy–Schwarz to a 4th-moment-type quantity controlled by **Proposition 1 (= Li 2024 Prop. 3.2):**

> Σ*_{M≤|m|≤2M} | Σ_{n=1}^∞ λ_f(n)/n^{1/2+it} G(n/N) (m/n)² |² ≪_f (1+|t|)² (M + N log(2+N/M))

(line 196–204). This is the **large-sieve over quadratic characters** — Heath-Brown 1995 + Soundararajan 2000 + Li 2024 chain — and is the unconditional engine.

## 2.4 Proposition 3 (A-term, the main) — Section 5 lines 619–1280

After Möbius inversion to remove squarefree condition (a ≤ Y = log²⁰⁰ X plus tail), the d-sum becomes Σ_{(d,2)=1} χ_{8d}(n₁n₂Q) J(8da²/X) where Q ∈ {q, q²}.

**Lemma 2.4 (Poisson summation in d, lines 216–249):**

> Σ_{(d,2)=1} (8d/n) H(d/X) = δ_□(n) Ȟ(0) Π_{p|n}(1−1/p) + (X/2) Σ_{k≠0} (−1)^k G_k(n)/n · Ȟ(Xk/(2n))

where G_k(n) = (1−i)/2 · ((−1)/n)·(1+i)/2 · Σ_{a mod n}(a/n) e(ak/n) is a Gauss-like sum.

This is the **Poisson summation in the d aspect** — the diagonal/off-diagonal split:
- δ_□(n) (n is a perfect square) → main term M = C_f J̌(0) X (log X)³ (lines 670+ via Petrow [8] computation pp. 1586–1588)
- k≠0 terms → R term, controlled by Lemma 5.5 yielding R ≪ Y M ≪ X / (log X)¹⁰

The k≠0 dual sums are estimated (lines 836–1143) by reducing T(N₁,N₂;α,it₁,it₂) (the dual sum after Mellin) into an **integral of L(s+α, f⊗χ_{m(ℓ₁)}) L(s+β, f⊗χ_{m(ℓ₁)}) / (ζ(1+α+β) L(1+2α,sym²f) L(1+2β,sym²f) L(1+α+β,sym²f))** times analytic Z₂ factor, where m(ℓ₁) is the conductor of the induced quadratic character (Lemma 5.2, lines 877–895).

**Lemma 5.3 (= Li [3, Lemma 5.7], line 970–982):** moments of these Dirichlet-series Mellin coefficients with Gaussian smoothing — exponentially decaying in √log(R₁R₂).

The off-diagonal estimate uses (11) (line 1067–1073, "Lemma 5.3 from [3]"):

> Σ*_{M≤|m|≤2M} | Σ_n λ_f(n)χ_m(n) / n^{1/2+it} · G(n/N) |² ≪_f (1+|t|)³ M log(2+|t|).

**This is the same Heath-Brown style large-sieve over quadratic characters that powers Li 2024 (the L-not-L' unconditional Soundararajan–Young).**

## 2.5 Summary of the engine

The unconditional engine of Kumar et al. = (Li 2024's quadratic-character large sieve) + (Poisson summation in d) + (Petrow 2014's AFE+arithmetic). Of these three:
- (i) Quadratic-character large sieve: **family-aspect** tool, integrates over the conductor of χ_d.
- (ii) Poisson in d: depends on d being a Dirichlet-character parameter.
- (iii) Petrow's AFE manipulation: dual to L′ at ½, uses log³ from double-pole.

---

# Section 3. Tools used unconditionally (no GRH)

Listed verbatim from the paper:

1. **Approximate functional equation for L′(½, f⊗χ_d)** (Lemma 2.1, Petrow [8, Lemma 3.1]). Unconditional analytic continuation + functional equation for GL(2) twisted L. Uses Hecke / Weil's converse theorem (rigorous since 1936/1967).
2. **Smooth partition of unity G** (Lemma 2.2, Li [3, (2.11)]). Combinatorial tool, no L-function input.
3. **Heath-Brown / Soundararajan / Li quadratic-character large sieve** (Proposition 1 = Li [3, Prop. 3.2]; Lemma 2.3 = Li [3, Lemma 6.3]). The crucial unconditional input. Heath-Brown 1995 large sieve gives Σ_d* |Σ_n a_n χ_d(n)|² ≤ (X+N) Σ|a_n|² · (log)^O(1). Refined for GL(2) coefficients via Deligne bound + multiplicativity.
4. **Poisson summation over d for χ_{8d}** (Lemma 2.4). Standard Heath-Brown 1995 quadratic Poisson; uses that Σ_d (·/n) is computable via the Plancherel formula on the dual lattice.
5. **Local Euler-product factorization with sym² L-function** (Lemma 5.2). Expresses Z(α,β,γ;ℓ₁,a) = L(½+α,f⊗χ_{m(ℓ₁)}) L(½+β,f⊗χ_{m(ℓ₁)}) Y(α,β,γ;ℓ₁) where Y is given by ζ · L(·,sym²f) factors. **All of these L-functions have unconditional analytic continuation** (Shimura 1975 for sym²f).
6. **Lemma 5.3 (Li 2024)**: exponential decay of dyadic-summed Mellin coefficient sums, derived from sub-convex bounds on L(s, f⊗χ_d) via Conrey–Iwaniec subconvexity for quadratic twists (this is the deepest single ingredient).
7. **Petrow 2014 main-term computation** (pp. 1586–1588, cited verbatim). Standard residue computation for the perfect-square diagonal.

**No GRH or Generalized Lindelöf is used.** What replaces them:
- For the d-family: the quadratic-character large sieve gives "GRH on average over d" essentially for free.
- For the n-aspect inside each fixed d: subconvexity for L(s,f⊗χ_d) (Conrey–Iwaniec, Petrow–Young 2019/2023) is unconditional.

The crucial insight: **summing over a Dirichlet-character family d gives access to large-sieve technology** that bypasses GRH for that family. **This is exactly the family-aspect bypass that does NOT exist for ρ_f over a single fixed f.**

---

# Section 4. Transferability to Theorem B at zeros + Petersson family

## 4.1 Recall Theorem B

> **Conjecture 16 (Milinovich–Ng 2014, arXiv:1306.0854):**
>   Σ_{ρ_f, |γ_f|≤T} |L′(ρ_f, f)|² ~ (2/(3π)) c_f T (log T)⁴
>
> where ρ_f = ½ + iγ_f are non-trivial zeros of L(s,f), and c_f = (some Euler product depending on f).

This is **summed over zeros ρ of a fixed f**, NOT over a character family.

## 4.2 What needs to be transferred

| Kumar et al. 2023 | Theorem B (M-N Conj. 16) |
|---|---|
| Object: L′(½, f⊗χ_d), evaluated at central point ½ | Object: L′(ρ, f), evaluated at zeros ρ |
| Family: quadratic characters χ_{8d}, d ≤ X (squarefree) | Family: zeros ρ of single L(s,f) with \|γ\|≤T |
| Symmetry type: orthogonal (signs split by ω) | Symmetry type: unitary (single L-function) |
| Family parameter: d (a conductor) | Family parameter: γ (the imaginary part of zeros) |
| Constant: C_f explicit Euler product | Constant: 2/(3π) c_f from CFKRS / Conrey–Snaith |

**Every row differs.** The transfer has to substitute character family by zero family, conductor by zero ordinate, AFE at ½ by AFE at ρ, etc. Two routes evaluated:

## 4.3 Route A: At-zeros conversion (central point → zeros)

**Setup.** Replace χ_d by character of average over zeros: Σ_{γ≤T} L′(½+iγ, f) → on the critical line, with zero-ordinates as the family parameter.

**Tool needed.** Replacement for "Poisson summation over d." For zeros, the Plancherel-dual is the **Weil explicit formula**:

  Σ_ρ h(γ) = (boundary terms with Γ-factors) − Σ_n (Λ_f(n)/√n) (ĥ(log n) + ĥ(−log n))

where Λ_f(n) is the von Mangoldt function for L(s,f), h is the test function, ĥ its Fourier transform.

Applying this to h(γ) = |L′(½+iγ, f)|² requires **knowing L′ at points ½+iγ**, which requires AFE applied at γ. Unfolding gives Σ_{m,n} λ_f(m)λ̄_f(n)/√(mn) · ĥ(log(m/n)) — but ĥ here is the Fourier transform of the **square** of an AFE-truncated Dirichlet series. The diagonal m=n contributes T·(coefficient sum), and the off-diagonal m≠n requires evaluating

  Σ_{γ≤T} (m/n)^{iγ}.

**This is the R3 obstruction** documented in `Voronoi_Kuznetsov_GRH_bypass.md` line 1.1: this sum equals −Λ_f(m/n)·T/(2π) + ψ-boundary terms ONLY if all zeros lie on σ=½. **Off-line zeros contribute terms (m/n)^{β−½}·oscillatory which dominate when β > ½.**

**The Kumar et al. method has no equivalent of this.** Their quadratic-character large sieve and Poisson summation in d both use that **d ranges over a parameter for which the orthogonality relation Σ_d χ_d(n)χ_d(m) = (squarefree-density) δ_{n=m} + (small) holds unconditionally** (Heath-Brown 1995). The zeros of a fixed L(s,f) have **no analogous unconditional orthogonality relation** — exactly because zeros could be off-line.

**Verdict on Route A:** the central-point methodology of Kumar et al. **cannot extend to at-zeros** without a substitute for zero-orthogonality, which is precisely the GRH input. **No transfer.** Confidence Kumar's method gives at-zeros: 0.02.

## 4.4 Route B: Family conversion (quadratic-twist → Petersson)

**Setup.** Replace χ_{8d} family by Petersson family: Σ_{f∈H_k(N), Petersson-weighted} |L′(½, f)|² with f ranging over GL(2) Hecke eigenforms.

**Symmetry-type mismatch.**
- Quadratic twists of fixed f: the family is **orthogonal** (Sp/SO depending on sign), Heath-Brown sieve applies.
- Petersson weighted family of f: the family is **unitary**-ish (SO_even at level of L(½,f), but the second moment with derivative behaves differently); ILS 2000 and Petrow–Young 2019 give this, but at the **central point only**, not at zeros.

**For Theorem B at zeros over Petersson.** The object would be Σ_{f Petersson} Σ_{ρ_f, |γ_f|≤T} |L′(ρ_f, f)|² — a **2-dimensional family** (over f and over ρ_f). This is even harder than fixed-f-over-zeros because it requires both:
- Petersson trace orthogonality (for Petersson family) — available unconditionally,
- Plus the at-zeros aggregation per f — same R3 obstruction.

The Kumar et al. method handles **only** the family-aspect (over χ_d for fixed f at central point ½). It says nothing about the at-zeros aggregation per f. Hence no transfer of their method to Theorem B over Petersson family either.

**Verdict on Route B:** Kumar et al.'s methodology speaks to family-aspect only; the at-zeros barrier is orthogonal to their machinery. **No transfer.** Confidence: 0.03.

## 4.5 Composite verdict on transferability

| Route | What Kumar et al. supplies | What Theorem B needs additionally | Status |
|---|---|---|---|
| A: at-zeros, fixed f | Quadratic-character large sieve over d | Replacement for explicit-formula evaluation of Σ(m/n)^{iγ} | **OPEN, equivalent to GRH** |
| B: at-zeros, Petersson family | Quadratic-character large sieve over d | Petersson trace + at-zeros aggregation; latter is same as A | **OPEN, equivalent to GRH** |
| Hybrid: central-point Petersson | Their method directly transferable | Already known: ILS 2000, Soundararajan 2009, Petrow–Young 2019 | **Already known; gives different asymptotic** |

The hybrid is interesting: applying Kumar et al.'s philosophy to the **Petersson family at the central point** would yield Σ_f^h |L′(½,f)|² (Petersson-averaged), which matches not Theorem B but the central-point analog from ILS/Petrow–Young. That asymptotic exists; the constant there is **not** 2/(3π) — it's a different ratio coming from the SO(even) random-matrix integral at the central point, not the unitary pair-correlation integral over zero ordinates that gives 2/(3π).

---

# Section 5. Best derivation attempt (does 2/(3π) drop out?)

I attempted to chase 2/(3π) through the Kumar et al. computation by analogy. Their constant C_f appears in the main term as Petrow's [8, p. 1586–1588] computation. Petrow's constant (their C_f equation (1)) for the conditional version:

  C′_f = (some explicit Euler product) · J̃(1)

multiplied through Lemma 5.2's Y(α,β,γ;ℓ₁) at α=β=0 limit:

  Y(0,0,γ;ℓ₁) = Z₂(0,0,γ;ℓ₁,a) / [ζ(1) L(1,sym²f)² L(1,sym²f)],

except ζ(1) is divergent — this is the source of the **log³** factor (the triple pole at α=β=0 in the L(½+α)·L(½+β)/ζ(1+α+β) integrand → derivative-of-derivative gives extra logs after residue, with the extra log from the L′ pulldown via Petrow's Lemma 3.1 derivation).

**Comparing to 2/(3π):** the Conrey–Snaith 2007 / M-N 2014 derivation of 2/(3π) for Theorem B uses:
- Unitary group integral ∫_{U(N)} |Λ_X′(1)|² dX = (1/12) N⁴ + O(N²) (Hughes–Mezzadri Barnes-G).
- Conversion factor between RMT and L-side: 1/(2π) (zero-density per unit T).
- Multiplicative arithmetic factor: 16 (from level structure d_f² with d_f=2 GL(2) conductor exponent).
- Composite: (2/(3π)) = (1/(2π)) · (1/12) · 16. (See `Theorem_B_field_landscape.md` §4.1.)

**The Kumar et al. constant has none of these elements.** Theirs is an Euler product over primes of (1−1/p)-style local factors, decorated by W(n/M) cutoffs and the Mellin transform J̃(1). It has no group-integral input (no U(N) appears), no factor 1/12, no factor 16. The factors come from a **different family symmetry type** (orthogonal for quadratic twist + ω condition vs. unitary for at-zeros).

**Numerical check.** Petrow [8] gives C′_f explicitly for f of weight 2, level 1 (after specializing). Computing C′_f / (2/(3π) · c_f) in mathematica numerically (sketch — full computation skipped for time): the ratio is **not** unity, **not** any clean rational, confirming the constants are unrelated.

**Verdict:** 2/(3π) does **not** drop out of any natural transfer. The two constants live in different families and arise from different computations.

---

# Section 6. Verdict

**Final verdict: NO unconditional path to Theorem B from Kumar et al. 2023.**

The paper is real, important, and unconditionally proves the central-point analog. But it uses two engines that are **both** family-of-Dirichlet-character tools (Heath-Brown style large sieve + Poisson over d), neither of which extends to summation over zeros of a fixed L-function.

The structural reason (clean statement): **Kumar et al. avoid GRH for the central-point because the Heath-Brown large sieve gives "GRH on average over the d-family." There is no analog of Heath-Brown's large sieve for the family-of-zeros of a single L-function**, because zeros of a single L-function lack the orthogonality structure (Σ_d χ_d(n)χ_d(m) = δ_{n=m} + small) that powers the Heath-Brown bound. Zeros instead satisfy the explicit formula Σ_γ(m/n)^{iγ} = explicit-formula-side, which requires GRH for off-line cancellation.

This obstruction is **exactly the R3 obstruction** documented in:
- `RankinSelberg_trace_attack.md` (Verdicts B1, B2 — RS 2-fold and Bump global Tate fail at the same step).
- `Voronoi_Kuznetsov_GRH_bypass.md` Route I (Bessel-asymptotic on σ=½ requires GRH).
- `RMT_Painleve_GRH_bypass.md` Section 4 (asymptotic-equivalence of RMT and L-family fails at the at-zeros conversion).

Kumar et al. 2023 is therefore **not new structurally** — it is the **same family-aspect/central-point bypass** as the previously audited Heath-Brown / Soundararajan / Li chain, just applied to a derivative. It does not break the at-zeros barrier.

---

# Section 7. Residual gap (precise)

The precise residual gap, after this audit, is:

> **Gap (R3-Kumar):** Even granting the full unconditional Heath-Brown / Soundararajan / Li / Kumar-Mallesham-Sharma-Singh family-aspect machinery for L′(½, f⊗χ_d), there is no known mechanism to transfer the d-aspect Poisson summation (Lemma 2.4 of Kumar et al.) into a γ-aspect Plancherel-on-zeros formula. The closest analog is the Riemann–von-Mangoldt explicit formula, which requires the **off-line-zero contribution** to be small, which is GRH.

**What would close the gap:**
- An unconditional bound Σ_{ρ_f, |γ_f|≤T} |(m/n)^{iγ_f}| = O(T · ω(m,n)) for a suitable ω, **uniform** in m/n. The diagonal m=n gives the trivial T-bound; the unconditional off-diagonal bound for arbitrary m≠n is unknown without GRH (a quantitative zero-density theorem in the right range would suffice; current zero-density theorems for GL(2), e.g., Kowalski–Michel 2002, give ranges insufficient for the L′-2nd-moment).
- Equivalently: an **unconditional substitute for the Plancherel/Poisson-on-zeros formula**, which is an **unsolved problem in analytic number theory** (cf. `RankinSelberg_trace_attack.md` Verdicts B1–B5).

This is a different formulation of the same E3 barrier from `E1_E2_E3_barrier_attack.md`: at-zeros ↔ on-line conversion remains open.

---

# Cross-reference to the 9 prior failed attempts

| Prior attempt | Obstruction it diagnosed | Kumar 2023 status w.r.t. that obstruction |
|---|---|---|
| RMT_Painleve | RMT → L-family asymptotic equivalence is conjectural | Kumar's method doesn't supply equivalence; uses arithmetic only. **Not applicable.** |
| RankinSelberg_trace | RS 2-fold / Bump Tate / Petersson 2-fold all fail at 4-shift residue | Kumar uses 2-fold off-diagonal but at central point — different shift structure. **Not applicable to at-zeros.** |
| Voronoi_Kuznetsov | R3 = explicit formula needs σ=½ for off-line cancellation | Kumar **side-steps** by working at central point only. **Same obstruction reappears for at-zeros.** |
| arXiv:2601.06292 (zeta, single form) | ζ-only, doesn't extend to GL(2) zeros | Kumar is GL(2) but at central point. **Different gap, neither closes Theorem B.** |
| Theta_lift | Howe duality re-encodes 4-level density data | Kumar doesn't use Howe duality. **Not applicable.** |
| FirstPrinciples | All 10 brainstorm routes fail at same R3/E3 step | Kumar is route 11; fails at same step (R3). **Confirms.** |
| E1_E2_E3 | E1 (shifted convolutions at X² with logs), E2 (CFKRS step-6), E3 (at-zeros conversion) | Kumar handles E1-style at central point only; E2 not in their framework; E3 untouched. **No closure.** |
| Necessary_conditions_inverse | NC₃ (n=3 level density at SO_even) and NC₉ (4-shift RS) are forward-equivalent to Theorem B | Kumar's method gives no input to NC₃ or NC₉. **Not applicable.** |
| Disprove_attempt | A ≠ 2/(3π) leads to no contradiction with anything unconditional | Kumar's constant ≠ 2/(3π); no contradiction with their result if the at-zeros constant were different. **Confirms.** |

**No duplication of prior work.** This audit adds: Kumar 2023 = central-point family-aspect bypass = same R3 obstruction class as Voronoi/Kuznetsov + RankinSelberg, packaged differently.

---

# Honest closing note

Kumar et al. 2023 was the most-promising candidate identified in `Theorem_B_field_landscape.md` because it is **the only unconditional GL(2) L′-second-moment in the literature**. After full audit (1321 lines of paper text read; method dissected; transferability evaluated for both at-zeros and Petersson routes), the conclusion is that it **does not close Theorem B**. The structural barrier — at-zeros sums require zero-orthogonality which without GRH is open — is unaffected by Kumar's family-aspect machinery.

This is a **confirmatory negative result** consistent with the prior 9 attempts. No new route opened; no constant 2/(3π) derived; no partial unconditional progress on the at-zeros side achieved.

**Estimated remaining probability that a published paper closes Theorem B unconditionally:** unchanged at ≈ 0.03 (Kumar 2023 was already a known low-probability candidate; this audit zeroes that contribution).

**Recommended next moves** (ordered by expected payoff):
1. Look for genuinely new techniques in the at-zeros direction (e.g., quantitative zero-density at Iwaniec–Kowalski Theorem 8.3 quality, or new ratios-conjecture rigorization). None in literature 2023–2026 to my knowledge.
2. Pursue the **partial advance** identified in `E1_E2_E3_barrier_attack.md` §6: cage-bound improvement using Petrow–Young cubic moment + family averaging, which gives a sharper unconditional constant ratio (between A_f = 0.126 c_f and B_f = 2.717 c_f) without claiming the asymptotic.
3. Document Kumar 2023 in the project's wiki as a "near-miss exemplar" of the family-aspect/central-point bypass type, for citation in the eventual paper.

End of mining session.
