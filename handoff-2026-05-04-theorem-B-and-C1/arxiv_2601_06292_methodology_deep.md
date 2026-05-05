# arXiv:2601.06292 — Methodology Deep Dive & Technical Genealogy

Paper: **"The discrete second moment of mixed derivatives of the Riemann zeta function"**
Authors: Benjamin Durkan, Christopher Hughes, Andrew Pearce-Crump (Jan 2026).

This is a complementary trace to the verification done by parallel agent a50ca139628bb7d78. Focus here: the technique cluster, author arc, and what is borrowable for GL(2).

---

## Section 1 — Author profile + key prior work

### Christopher Hughes (York)
Senior author. Random matrix theory and the Riemann zeta function. Co-author of two foundational papers cited in the cluster:
- **[14]** Hughes, Keating, O'Connell (2000), *Random matrix theory and the derivative of the Riemann zeta function*, Proc. Roy. Soc. A **456**:2611–2627. The seminal RMT-prediction paper for moments of ζ′(ρ).
- The "hybrid model" via Gonek–Hughes–Keating (2007) — used in 2509.07788 to derive complex moment conjectures.

### Andrew Pearce-Crump (Bristol; PhD York under Hughes)
The active researcher building the asymptotic-expansion technique. Dual research life: number theory + group-equivariant neural networks (irrelevant here).

### Benjamin Durkan (Manchester PhD; MSc by Research, York 2025)
First author. The 2601.06292 paper "forms part of the first author's MSc by Research thesis [4] from the University of York" — Hughes is the supervisor. So 2601.06292 is essentially Hughes/Pearce-Crump method applied/extended to mixed derivatives in a master's thesis.

### Pearce-Crump number-theory arc (chronological, all on arXiv)
1. **2106.03005** (2021, w/ Hughes) — *A discrete mean-value theorem for the higher derivatives of the Riemann zeta function.* J. Number Theory 235 (2022). **The methodological foundation.** Establishes the contour-integral / functional-equation / Perron / residue technique for Σ ζ⁽ⁿ⁾(ρ) with full asymptotic expansion.
2. **2111.02756** (2021, solo) — *A further generalisation of sums of higher derivatives of the Riemann zeta function.* Σ ζ⁽ⁿ⁾(ρ)X^ρ (Landau–Gonek style with derivatives).
3. **2305.14253** (2023, w/ Hughes & Greg Martin) — *A heuristic for discrete mean values of the derivatives of the Riemann zeta function.* Sets up RMT/hybrid heuristics that crystallize in the 2025 papers.
4. **2411.05568** (2024, solo) — *Moments of the Riemann zeta function at its local extrema.*
5. **2411.05573** (2024, w/ Hughes & Lugmayer) — *The second moment of the Riemann zeta function at its local extrema.*
6. **2509.07788** (Sep 2025, w/ Hughes) — *Complex moments of the derivative of the Riemann zeta function.* RMT-based conjecture for complex k-th moments of ζ′(ρ), ℜ(k) > −3, using Selberg's integral on U(N) and the Gonek–Hughes–Keating hybrid model.
7. **2509.07792** (Sep 2025, w/ Hughes) — *Integer moments of the derivatives of the Riemann zeta function.* Builds the **integer-moment conjectures of mixed derivatives** via Conrey–Farmer–Zirnbauer Ratios Conjecture and the CFKRS recipe. Conjecture 3 gives the leading order of Σ ζ⁽ⁿ¹⁾(ρ)…ζ⁽ⁿᵏ⁾(ρ).
8. **2601.06292** (Jan 2026, w/ Durkan & Hughes) — **the paper.** Proves the **k=2 case** of the integer-moment conjectures unconditionally + RH, with full asymptotic expansion (not just leading order).
9. **2601.18025** (Jan 2026, w/ Durkan & Hughes) — *Generalisations of the Landau–Gonek Theorem.* Sister paper; proves Σ χ(ρ)X^ρ identities used as building blocks for moment computations via approximate functional equation.

So 2601.06292 sits inside a tight 5-year, ≈9-paper arc.

---

## Section 2 — Citation backward (load-bearing inputs)

Verbatim from the references of 2601.06292:

- **[9] Gonek 1984** *Mean values of the Riemann zeta-function and its derivatives*, Invent. Math. 75:123–142. Originator of the discrete moment Σ ζ⁽μ⁾(ρ)ζ⁽ν⁾(1−ρ) and proved the leading-order asymptotic (1.2). Also provides the I₂ = O(T^{1/2+ε}) bound that the paper relies on.
- **[3] Conrey & Snaith 2007** *Applications of the L-functions ratios conjectures.* The Ratios-Conjecture-derived lower-order terms for Σ|ζ′(ρ)|² that this paper extends to mixed derivatives.
- **[18] Milinovich PhD thesis 2008** *Mean-value estimates for the derivative of the Riemann zeta function.* The first proof under RH of the lower-order terms Conrey–Snaith conjectured for the μ=ν=1 case. Method is the direct technical predecessor of the Hughes–Pearce-Crump contour technique.
- **[13] Hughes & Pearce-Crump 2022** (= arXiv 2106.03005). Source of **Lemma 1** in 2601.06292: the functional equation for ζ⁽ν⁾(1−s) expressed in terms of ζ⁽k⁾(s), 0 ≤ k ≤ ν. This is the workhorse identity.
- **[22] Titchmarsh** — standard reference, used for explicit formula and zero-counting.
- **[19] Montgomery–Vaughan** — for Perron's formula.

The proof has 4 key inputs: functional equation for ζ⁽ν⁾(1−s) [from 2106.03005], stationary phase, truncated Perron's formula, residue calculus around s=1.

Quote of the proof outline from §3:
> "We apply the functional equation for ζ(ν)(1−c−it) so we can write the resulting expression in terms of convergent Dirichlet series … We then use the method of stationary phase to rewrite this integral as the sum Σ_{n₁n₂n₃ ≤ T/(2π)} Λ(n₁)(log n₂)^μ (log n₃)^k (log n₁n₂n₃)^{ν−k} … We evaluate this sum without the (log n₁n₂n₃)^{ν−k} factor through Perron's formula. This gives the sum as the residue of a Dirichlet series at s=1, which in turn is a polynomial of degree μ+ν+2."

---

## Section 3 — Citation forward (extensions / applications)

As of May 2026 the paper is 4 months old and not yet on Google Scholar with citations. Forward-looking adjacencies in the same author cluster:

- **2509.07792** *predicts* (Conjecture 3) the leading order of arbitrary integer moments of mixed derivatives. 2601.06292 **proves** the k=2 case. Conjecture 3 for k ≥ 3 is open and would require a higher moment of ζ at zeros, which is the Conrey–Iwaniec–Soundararajan barrier.
- **2601.18025** (Landau–Gonek generalisation) provides "an alternative proof of Shanks' conjecture" via χ(ρ)X^ρ + approximate functional equation — a complementary technique that may extend higher.
- The paper handles the **2nd moment** of ζ⁽μ⁾, ζ⁽ν⁾ at zeros. **No higher moment** is treated. The 4th moment of ζ′(ρ) was done by **Ng (2004)** [ref 20]; nothing higher exists.

---

## Section 4 — Technical genealogy (5–10 paper arc)

```
Selberg/Ingham (1926) [Mean value theorems]
   ↓
Gonek (1984) [9]   — invents Σ ζ^(μ)(ρ)ζ^(ν)(1−ρ); leading order
   ↓
Hejhal (1989) [12] — log|ζ′(½+it)| distribution, GUE link
   ↓
Hughes–Keating–O'Connell (2000) [14] — RMT predictions for ζ′(ρ) moments
   ↓
Conrey–Farmer–Keating–Rubinstein–Snaith (2003,2005) — CFKRS recipe for L-function moments
   ↓
Conrey–Farmer–Zirnbauer (2008) — Ratios Conjecture
   ↓
Conrey–Snaith (2007) [3] — applies Ratios to Σ|ζ′(ρ)|² lower-order terms
   ↓
Milinovich PhD (2008) [18] — proves Conrey–Snaith conjecture under RH for μ=ν=1
   ↓
Ng (2004) [20] — 4th moment of ζ′(ρ)
   ↓
Hughes–Pearce-Crump (2022) [13] — Σ ζ^(n)(ρ) full asymptotic, all n  ★ method-defining
   ↓
Hughes–Pearce-Crump (Sep 2025, 2509.07788, 2509.07792) — RMT/Ratios conjectures for complex & integer moments of mixed derivatives
   ↓
Durkan–Hughes–Pearce-Crump (Jan 2026, 2601.06292)  — proves the k=2 case unconditionally
   ↓
Durkan–Hughes–Pearce-Crump (Jan 2026, 2601.18025)  — Landau–Gonek generalisations
```

Ancillary cluster (negative moments, parallel research line):
- Heap–Li–Zhao (2022) [11], Gao–Zhao (2023) [5], Bui–Florea–Milinovich (2024) [2] — lower bounds for Σ|ζ′(ρ)|^{−k}. **Not used in the proof** but cited as part of the moment-theory landscape.

---

## Section 5 — What can be borrowed for GL(2)?

### What is ζ-specific (likely hard to port)
1. **Lemma 1 of [13]** = functional equation for ζ⁽ν⁾(1−s) as finite sum involving ζ⁽k⁾(s). For GL(2) automorphic L-functions L(s,f), the functional equation is L(s,f) ↔ L(1−s, f̃) with a different gamma factor (Γ(s/2+a)Γ(s/2+b) vs Γ(s/2)). Differentiating produces a similar finite-sum identity, but the **gamma-factor logarithmic derivatives ψ(s/2+a)+ψ(s/2+b)** appear instead of ψ(s/2). Asymptotic expansions are messier but should be tractable — direct port.
2. **Stationary phase with χ_ζ(s)** (the χ in the functional equation). For GL(2) the χ_f(s) has a different t^{σ-1/2} → t^{2σ-1} scaling (degree-2 L-function). Stationary phase still works but the saddle is at different location, changing the truncation T/(2π) → T²/(2π)² (rough). The companion paper **2601.18025** (Landau–Gonek for χ(ρ)X^ρ) is essentially the GL(1) version of what one would need for GL(2); **its splitting into three regimes (X<T, X≈T, X>T)** is exactly the kind of degree-dependent phenomenon to expect at degree 2.
3. **Perron + residue at s=1**. ζ has a simple pole at s=1; L(s,f) for cusp forms is **entire**. So the "residue at s=1" step disappears for GL(2) automorphic L. This is a **structural difference**: the polynomial-in-log-T main term for ζ comes from this pole. For cusp forms, the analog of Σ L⁽μ⁾(ρ)L⁽ν⁾(1−ρ) has **no log power main term from a pole at 1**; it is governed by Rankin–Selberg L(s, f×f̃) which has a pole at s=1. So one expects the role of ζ(s)ζ(1−s)·ζ′/ζ to be played by L(s,f×f̃) factors. This matches the CFKRS recipe and Conrey–Iwaniec–Soundararajan moment conjectures for GL(2).

### What ports cleanly
- The **Cauchy contour decomposition** I = I₁ + I₂ + I₃ + I₄ around the critical strip — purely complex-analytic, identical for any L-function.
- The use of **convexity bounds + functional equation to handle I₂** (top of contour) — standard for any L-function with subconvex bounds.
- **Stationary phase for χ_L(s)** at the cost of more bookkeeping with degree-2 weights.
- **Truncated Perron's formula** — purely a Mellin tool, ports verbatim.

### What needs to be replaced for GL(2)
- The simple pole of ζ at s=1 → use Rankin–Selberg L(s, f×f̃) and its pole.
- Λ(n)logⁿ(...) sums → become Σ |λ_f(n)|² weights (Hecke eigenvalues squared) — these are sums controlled by the symmetric-square L-function.
- The exact arithmetic factor for ζ becomes the GL(2) arithmetic factor from CFKRS recipe (Euler product over p of a polynomial in p^{-s_i}).

### Highest moment handled
The paper handles only the **2nd moment** Σ ζ⁽μ⁾(ρ)ζ⁽ν⁾(1−ρ). Integer moments k ≥ 3 of derivatives at zeros of ζ remain **open even conjecturally beyond leading order** (only conjectured in 2509.07792, k = 4 fully proved without derivatives by Ng). For GL(2), even the **2nd moment of L⁽μ⁾(ρ_f)L⁽ν⁾(1−ρ_f)** appears not done — would be the natural target.

### GRH-equivalent input?
**No.** The paper proves Theorem 1 unconditionally with error O(T·exp(−C√log T)) (zero-free region of ζ, classical), and improves to O(T^{1/2+ε}) under RH only. So the structural backbone is **unconditional** and uses only the **classical zero-free region**. This is encouraging for GL(2): a similar unconditional result should be possible using the standard zero-free region for cusp-form L-functions.

### RMT / Painlevé / multiplicative chaos?
- 2601.06292 itself **does not use RMT**. Pure Dirichlet-series + contour analysis.
- The companion conjectural papers (2509.07788, 2509.07792) **do** use RMT (Selberg's integral on U(N), Keating–Snaith) and the Gonek–Hughes–Keating hybrid model, but only to **predict** what the proven theorem in 2601.06292 confirms.
- No Painlevé, no multiplicative chaos, no moment-matching beyond comparison with CFKRS predictions.

### Specific lemmas worth porting
| Lemma in 2601.06292 | What it does | GL(2) analog |
|---|---|---|
| Lemma 1 [from HPC 2022, Lemma 4] | ζ^(ν)(1−s) = Σ_{k=0}^ν C(ν,k) χ_{stuff}(s) ζ^(k)(s) + lower order | Need: L^(ν)(1−s,f) = Σ C(ν,k) χ_{f}(s) L^(k)(s, f̃) — derivable from the functional equation for L(s,f) |
| Lemma 2 (Lemma 1 of HPC 2022) | Convexity bound for ζ^(n)(σ+it) | Direct: use convexity for L^(n)(s,f), available |
| Lemma 11 of HPC 2022 | Truncated Perron formula | Identical, no change needed |
| §4 stationary phase eval | Saddle of χ_ζ(s) ≈ (t/2π)^{1/2−s} | Saddle of χ_f(s) for degree-2 L — known (Iwaniec–Kowalski Ch. 5) |

---

## Section 6 — Honest gaps in this trace

1. **No actual reading of [13] (HPC 2022) Lemma 4** verbatim — I confirmed it exists at line 542 of 2601.06292 ("Lemma 1. [13, Lemma 4] For s = σ + it, with σ ≥ 1 and t ≥ 1") but did not read the proof in 2106.03005 in full. The exact form of the finite-sum functional-equation identity should be verified against the GL(2) Hecke functional equation before claiming a clean port.
2. **No forward citations** retrieved (Google Scholar / Semantic Scholar not queried via API). Given paper age (4 months) likely zero citations exist yet.
3. **Conrey–Iwaniec–Soundararajan, Florea, Bui-Heath-Brown** — referenced in user prompt as adjacent literature; I did not pull these. The 2509.07792 reference list (Ratios Conjecture, CFKRS recipe) is the right starting point if pursuing this further; reading the CFKRS 2003 (arXiv math/0208007) and 2005 papers would give the right framework for GL(2) extension.
4. **The GL(2) port discussion is heuristic** — based on standard knowledge of L-function functional equations. No actual arithmetic factor for the GL(2) version was computed.
5. **Durkan's MSc thesis [4]** not located (Univ. of York 2025); may contain a longer version with details not in the arxiv paper.
6. **Milinovich PhD (2008)** [18] not retrieved — this is the immediate technical ancestor of the proof in 2601.06292 for the μ=ν=1 case, and reading it would clarify exactly what the new paper adds.
7. **Garunkštis–Paliulionytė 2025 (arXiv:2512.03297)** — reference [7], very recent, on shifted second moment under RH; would be useful to triangulate.

## Files

- `/tmp/2601.06292.pdf` and `.txt` — the paper.
- `/tmp/2106.03005.pdf` and `.txt` — Hughes–Pearce-Crump 2022 (method foundation).
- `/tmp/2111.02756.{pdf,txt}` — further generalisation by PC.
- `/tmp/2305.14253.{pdf,txt}` — Hughes–Martin–Pearce-Crump heuristic (Shanks).
- `/tmp/2411.05568.{pdf,txt}` — moments at local extrema (PC solo).
- `/tmp/2411.05573.{pdf,txt}` — 2nd moment at local extrema (HLP).
- `/tmp/2509.07788.{pdf,txt}` — complex moments of ζ′(ρ) via RMT.
- `/tmp/2509.07792.{pdf,txt}` — integer moments of mixed derivatives (Ratios Conjecture).
- `/tmp/2601.18025.{pdf,txt}` — Landau–Gonek generalisations (sister paper).

(`/tmp/HPC2022.pdf` — wrong download, ignore; the correct Hughes–Pearce-Crump 2022 paper is `/tmp/2106.03005.pdf`.)
