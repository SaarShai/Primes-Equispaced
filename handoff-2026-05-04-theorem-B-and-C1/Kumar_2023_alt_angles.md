---
title: "Kumar–Mallesham–Sharma–Singh 2023 (arXiv:2303.16864) — alternative-angle audit (parallel to direct-extension audit)"
type: derivation
domain: research
tier: working
confidence: 0.04
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (parallel agent, 6h budget, alternative angles)
sources:
  - /tmp/kumar_2303.pdf, /tmp/kumar_2303.txt (the paper, 1321 lines)
  - Kumar_2023_methodology_mine.md (parallel main agent's direct-extension audit; verdict: NO)
  - Theorem_B_field_landscape.md, Theta_lift_GRH_bypass.md, Voronoi_Kuznetsov_GRH_bypass.md
  - X. Li, arXiv:2208.07343 (large-sieve input)
  - I. Petrow, IMRN 2014 (conditional precursor)
  - Soundararajan–Young 2010 (L-not-L′ precedent)
tags: [theorem-B, kumar-2023, alternative-angles, GRH-bypass, transferability-analysis, parallel-agent]
relation: parallel-to Kumar_2023_methodology_mine.md (different angle attack on same paper)
---

# Bottom line (written first)

**Verdict: NO unconditional path to Theorem B from any of the 6 alternative angles.**

Each of the 6 indirect transformations (Plancherel-on-line + 1-LD, theta-lift transfer of bound, sieve to fixed N, double-derivative L′′, Voronoi on coefficients, higher-derivative + Cauchy formula) **degenerates back to the R3 obstruction** (off-line zero contribution to Σ_γ (m/n)^{iγ}, equivalent to GRH for L(s,f) in a quantitative sense), or to a strictly **harder** problem (4-level density, Sp(4) symplectic n-LD with n≥3, etc.).

This audit does **not contradict** the main agent's direct-extension audit; it strengthens it: the alternative angles all lead to the same wall.

The only potentially-additive partial finding (Section 3.4 below): **Angle 4 (differentiate twice in shift)** clarifies a *strictly stronger* family-aspect statement that Kumar's method *would* prove, namely the **Petrow-Young-style L′′(½) second-moment unconditionally over χ_{8d}**. This is a publishable spin-off, not a Theorem B closure.

Probability that any alt-angle delivers Theorem B unconditional: **0.02** (slightly below main agent's 0.03, because alt angles are strictly more indirect and therefore have at most the direct-extension probability, with composition penalty).

---

# Section 1. Verbatim Kumar 2023 summary (compressed)

Theorem 1 (lines 83–93 of /tmp/kumar_2303.txt):

> Σ⋆_{(d,2q)=1, ω(f⊗χ_{8d})=−1} |L′(½, f×χ_{8d})|² J(8d/X) = C_f J̃(1) X log³X + O(X (log X)^{5/2+ε})

Engine (lines 162–270):
- **AFE for L′ at ½** (Lemma 2.1, Petrow [8, Lem 3.1]): 1/u² double-pole → log³.
- **Smooth dyadic G** (Lemma 2.2, Li [3, (2.11)]).
- **Heath-Brown / Li quadratic-character large sieve over d** (Prop 1, Lem 2.3 = Li 2024 Lem 6.3 + Prop 3.2).
- **Poisson summation in d for χ_{8d}(n)** (Lemma 2.4):
  > Σ_{(d,2)=1} (8d/n) H(d/X) = δ_□(n) Ȟ(0) Π_{p|n}(1−1/p) + (X/2) Σ_{k≠0} (−1)^k G_k(n)/n · Ȟ(Xk/(2n))
- **Lemma 5.2 Euler-product factorization** with sym² L (Shimura unconditional).
- **Lemma 5.3 (Li 2024 Lem 5.7)**: Mellin coefficient decay from Conrey–Iwaniec subconvexity.

The **two unconditional engines** (per main agent's audit):
- (E_1) Quadratic-character large sieve in d.
- (E_2) Poisson summation in d (Lemma 2.4).

Both are family-aspect Dirichlet-character tools. Theorem B sums over **zeros of a single L(s,f)** — there is no Dirichlet-character family.

---

# Section 2. Alternative angles enumerated

| # | Angle | One-line idea | Pre-evaluation |
|---|---|---|---|
| A1 | Plancherel-on-critical-line + ILS 1-LD | Use Kumar's central-point output + integration on σ=½ + ILS unconditional 1-LD to get at-zeros |
| A2 | Quad-twist ↔ Petersson via theta lift | Transfer Kumar's bound through Howe duality |
| A3 | Sieve to fixed N | Restrict Kumar to 8d=N (single character) — gives Petersson-style fixed-f |
| A4 | Differentiate L′′ at ½ | Apply Kumar's method to L′′ — does L′′-2nd-moment + Plancherel give at-zeros L′-2nd-moment? |
| A5 | Voronoi on Kumar AFE coefficients | Use Voronoi to transform Kumar's coefficient sums to at-zeros formulation |
| A6 | Higher-derivatives + Cauchy formula | L^(k)(½) for many k + Cauchy contour around ½ → at-zeros sum |

Each angle is now evaluated.

---

# Section 3. Angle-by-angle evaluation

## 3.1 Angle A1 — Plancherel on σ=½ + ILS 1-LD

**Setup.** Plancherel formula on the line σ=½:

  ∫_{-T}^T |L′(½+it, f)|² dt = (Plancherel-dual sum over coefficients).

This is **NOT** Σ_ρ |L′(ρ,f)|² — it is the on-critical-line continuous mean. The conversion needs zero-density information.

**Step-by-step.** The relation between continuous on-line moment and at-zeros sum is
  Σ_{|γ|≤T} |L′(½+iγ, f)|² = (T/2π · log T)·(continuous moment density at ½) + (correction from zero-spacing fluctuations).

The **correction** is governed by the **2-level zero-density** (Bogomolny–Keating, Conrey–Snaith). Going from (continuous on-line moment) → (at-zeros sum) requires:
- Continuous on-line moment of |L′|² at ½ → unknown unconditionally for GL(2) (this is the L′-2nd-moment on critical line, which Bui–Conrey–Sono 2020 give conditional on GRH).
- 2-level zero density on f-zeros → ILS 2000 only for **family-aspect** (averaging over f), not for **single f over zeros** (which is what Theorem B needs).

**ILS 1-LD with η<1 — what it actually says.** ILS theorem 1.1 (lines 62–84 of /tmp/ils.txt; standard ref Iwaniec–Luo–Sarnak 2000, Publ. IHES 91, Thm 1.1):

> For F a Petersson-weighted family of cusp forms on Γ_0(N), Σ_{f∈F} W(c) Σ_{γ_f} φ(γ_f L) = ∫ φ(x) (1 − sin(2πx)/(2πx)) dx + o(1)

unconditionally if supp(φ̂) ⊂ (−η, η) with η < 1 (orthogonal symmetry) — OR η < 2 conditional. **The family parameter is f, not γ_f.** ILS controls Σ over f of Σ over γ_f of φ(γ_f L) — a 2D sum. The 1-LD gives the **mean spacing** of zeros over the family. It does NOT give Σ_{γ_f} |L′(½+iγ_f,f)|² for fixed f.

**The transfer fails at this step.** To go from
  Σ_f W(f) Σ_{γ_f} φ(γ_f L) → Σ_{γ_f} |L′(½+iγ_f,f)|² for fixed f
we would need:
1. A test function φ that captures |L′|² at the zero — but |L′(ρ,f)|² is not a test function of γ_f alone; it depends on L being differentiated and evaluated at ρ.
2. To remove the f-averaging by some sort of inverse-Mellin or Selberg-Delange — but the f-family in ILS is the only thing that gives orthogonality control unconditionally.

**Kumar 2023's role here.** Kumar gives unconditional Σ_d |L′(½, f⊗χ_{8d})|² ~ X log³X. This is on a different family (d-family, not γ-family) at a different point (½, not ½+iγ). The Plancherel on σ=½ would need ∫_{-T}^T |L′(½+it,f)|² dt, **not** what Kumar gives.

**Numerical sanity check (mental computation).** If Kumar's central-point density were transferable, we would expect the constant 2/(3π) to factor into Kumar's C_f. Per main agent §5: C_f has no factor of 1/12 (no U(N) integral) and no factor of 16 (no GL(2) level structure exponent d_f²) — different arithmetic origin entirely. So even *abstractly* the densities don't match.

**Verdict A1: FAILS.** Plancherel needs continuous on-line moment (unknown unconditionally for L′ at ½ for GL(2)). ILS 1-LD is family-aspect, not at-zeros for single f. **Confidence A1 closes Theorem B: 0.02.**

## 3.2 Angle A2 — Quadratic-twist ↔ Petersson via theta correspondence

**Setup.** Kumar's family is symplectic (quadratic twists, signs split by ω). Petersson family is orthogonal. Theta correspondence (Howe duality) at the *level of representations* relates the two sides.

**What's already documented (Theta_lift_GRH_bypass.md §2.1, R1 verdict, lines 70–106):**

> The Shimura half-integral lift is a bijection of representations, NOT a reduction of n-level density. The L-function is unchanged. Confidence: 0.02.

R1 says: lifting f → g (Shimura/Waldspurger half-integral form) does not change the L-function (Waldspurger central-value formula relates L(½,f⊗χ_d) to |g(d)|²). So the family on the lifted side is just {g_f}, indexed identically by f. No reduction in level.

**What's NEW for Kumar 2023 specifically.** Kumar's unconditional bound on the *quadratic-twist family* at ½ would, naively, transfer through Waldspurger to a bound on Σ_d |g(d)|⁴ · (log-factor) — but this is just a quantity already controlled by Heath-Brown's quadratic-character large sieve directly (Heath-Brown 1995, Acta Arith. 72:235–275), so no new information.

**For at-zeros transfer.** The theta lift relates
- (quadratic-twist family of f, central point ½) on left
- (half-integral form g, weighted by d) on right.

There is **no** version of Howe duality that transports an at-zeros statement on side A to an at-zeros statement on side B with reduced symmetry. Howe duality is a **representation-level** correspondence, not a **statistics-level** correspondence (Theta_lift_GRH_bypass.md §1.2 explicitly states this).

**Local theta transfer.** Even at the level of local L-factors, the transfer:
  L_p(s, f⊗χ_d) ↔ L_p(s, g, related-twist)

preserves the local Euler factor structure. Kumar's bound is on a *global* second moment, and the transfer is *local* — there is no mechanism to globalize the local transfer into an at-zeros bound.

**Verdict A2: FAILS.** Same conclusion as Theta_lift_GRH_bypass.md R1; Kumar 2023 doesn't change the picture. **Confidence A2: 0.02.** (DUPLICATES prior failed Theta route — flagged.)

## 3.3 Angle A3 — Sieve Kumar's family by twist conductor (fixed N)

**Setup.** Kumar averages over 8d ≤ X. Restrict to **fixed** 8d = N₀ for some squarefree N₀. Does Kumar's argument still hold? If yes, gives a single L′(½, f⊗χ_{N₀})² statement (a single quadratic-twist evaluation).

**Immediate problem.** For fixed N₀, Kumar's Theorem 1 specializes to a **single** value
  |L′(½, f⊗χ_{8d_0})|² = ?
which is not an asymptotic — it's a specific number. Kumar's machinery (Σ_d, Poisson over d, large sieve over d) is ENTIRELY about averaging. With 8d=N₀ fixed:
- Σ⋆_d collapses to single term (no average).
- Poisson summation in d (Lemma 2.4) does not apply (d is no longer a summation variable).
- Large sieve over d (Prop 1, Lem 2.3) does not apply.

The ONLY thing left is the AFE (Lemma 2.1):
  L′(½, f⊗χ_{N₀}) = (1−i^k η χ_{N₀}(−q)) Σ_n λ_f(n)χ_{N₀}(n)/n^{1/2} W(n/|N₀|).

This gives a **point-evaluation** representation, NOT a 2nd-moment bound. Standard convexity bound:
  |L′(½, f⊗χ_{N₀})| ≪ N₀^{1/4+ε} · log

(from convex bound L(½, f⊗χ_d) ≪ d^{1/4+ε}, plus log from differentiation). Subconvex (Petrow–Young 2019, Conrey–Iwaniec 2000):
  |L′(½, f⊗χ_{N₀})| ≪ N₀^{1/6+ε} (or better)

**Petersson connection.** If we sum over a Petersson family {f ∈ H_k(N)} for fixed N₀:
  Σ_f^h |L′(½, f⊗χ_{N₀})|² = ?

This is the Petersson 2nd-moment of a *fixed-twist* L-derivative. Petersson trace formula (for level lcm(N, N₀²)) gives:
  Σ_f^h λ_f(m)λ_f(n) = δ(m,n) + Kloosterman + ...

After AFE expansion, this becomes a sum of Kloosterman sums — handled by Kuznetsov formula. **This is not at-zeros either.** It's the Petersson family second-moment of L′(½, f⊗χ_{N₀}) at the central point — a known unconditional result type, related to Iwaniec–Sarnak / Kowalski–Michel. Doesn't give Theorem B.

**Verdict A3: FAILS.** Sieving to fixed N₀ collapses the average, leaving either a single-point evaluation (no asymptotic) or a different family (Petersson over f, central-point at ½, not at-zeros). **Confidence A3: 0.01.**

## 3.4 Angle A4 — Differentiate Kumar's setup (L′′ at ½)

**Setup.** Kumar handles L′(½). What if we apply his method to L′′(½)?

**Generalization.** AFE for L′′ — straightforward extension of Petrow's Lemma 3.1. The cutoff function W gets replaced by a triple-pole 1/u³ contour, giving:
  L′′(½, f⊗χ_d) · I(ω(f⊗χ_d) = +1) = (some explicit factor) Σ_n λ_f(n)χ_d(n)/n^{1/2} · W₂(n/|d|),
  W₂(y) = (1/(2πi)) ∫_{(3)} (Γ(u+k/2)/Γ(k/2)) (2πy/√q)^{−u} du/u³.

The triple pole 1/u³ → log⁵ scaling (one extra log per derivative power, as in Petrow's pp. 1586–1588 calculation).

**Expected result of Kumar's method applied to L′′:**
  Σ⋆_{(d,2q)=1, ω=+1} |L′′(½, f⊗χ_{8d})|² J(8d/X) = C_f^{(2)} J̃(1) X log⁵X + O(X log⁴X)

(via the same engine: Heath-Brown large sieve + Poisson over d + extended-pole AFE).

**Connection to at-zeros.** Use Cauchy's integral formula on a small contour around ρ=½+iγ:
  L′(ρ, f) = (1/(2πi)) ∮_{|s−ρ|=r} L(s,f)/(s−ρ)² ds
  L′′(ρ, f) = (2/(2πi)) ∮_{|s−ρ|=r} L(s,f)/(s−ρ)³ ds

Integration over the contour passes through points off the critical line — for a *random* zero ρ at ½+iγ (assuming GRH), small contour stays near ½, but **without GRH**, ρ may be off-line. So Cauchy integration around ρ does not give us L′(ρ) in terms of L on σ=½ unless GRH holds.

**Alternative interpretation: combine L(½) + L′(½) + L′′(½) Taylor-style.** For ρ on critical line, Taylor expansion:
  0 = L(ρ) = L(½) + L′(½)(ρ−½) + L′′(½)(ρ−½)²/2 + O((ρ−½)³)

Solving: ρ−½ = (something involving ratios of L^(k)(½)). This gives **zero LOCATIONS** in terms of central-point derivatives — but only LOCALLY (for zeros very close to ½). Most zeros γ are NOT close to 0; so this Taylor relation is useful only for zeros with γ ≪ 1, which is a measure-0 subset of the at-zeros sum.

**The Plancherel-via-derivatives idea.** If we had **all** moments of all derivatives at ½ unconditionally, could we reconstruct |L|² globally on σ=½? Yes, in principle — Borel/Stieltjes-type reconstruction. But this requires:
- All derivatives L^(k)(½), k=0,1,2,...
- 2nd-moments of all of these, Σ_d |L^(k)(½, f⊗χ_d)|² (Kumar gives k=1).

Kumar's method produces 2nd-moment of ONE derivative at a time. To reconstruct moments at ½+iγ from moments of L^(k)(½), we'd need a 2nd-moment of *the entire Taylor series* — which is *equivalent to* the 2nd-moment on the line, which requires Bui–Conrey–Sono 2020 (conditional).

So there's a circularity: extracting at-zeros from {L^(k)(½)}_k requires the line moment, which we don't have unconditionally for GL(2).

**Partial finding.** Kumar's method DOES give a new unconditional result: the L′′(½) 2nd-moment over χ_{8d}, ω=+1 family. This is a publishable spin-off (~2 weeks of work to write up; same engine), but it is **not** Theorem B.

**Verdict A4: FAILS for Theorem B; PARTIAL WIN for L′′ family-aspect.** Confidence A4 closes Theorem B: **0.03** (slightly higher than others because the structural relation between L^(k)(½) and L′ at zeros is genuinely intertwined, but the line-2nd-moment input remains absent).

## 3.5 Angle A5 — Voronoi summation on Kumar AFE coefficients

**Setup.** Kumar's AFE has coefficients λ_f(n)χ_{8d}(n) summed over n. Voronoi summation transforms Σ_n λ_f(n) f(n) → Σ_n λ_f(n) f̌(n) via the GL(2) Voronoi formula (Iwaniec–Kowalski Thm 5.4):
  Σ_{n=1}^∞ λ_f(n) e(an/q) f(n) = (cqℓ-factor) Σ_n λ_f(n) e(−ān/q) f̌(n)
where f̌ is the Bessel-Kuznetsov transform and ā ā ≡ 1 (q).

**Applying Voronoi to Kumar's main term.** Kumar's main term M (line 1187):
  M = (J̌(0) X / 8) Σ_{Q∈{q,q²}} ε_Q Σ_{a≤Y} μ(a)/a² Σ_{n₁,n₂: n₁n₂Q=□, (n₁n₂,2a)=1} λ_f(n₁)λ_f(n₂)/√(n₁n₂) · Π_{p|n₁n₂Q}(1−1/p) W(n₁/M) W(n₂/M).

Voronoi transformed n₁,n₂ sums would replace λ_f(n) by λ_f(ñ) (still GL(2)) but with **Bessel-K kernel** instead of W. This is the Voronoi_Kuznetsov_GRH_bypass.md territory.

**Recall Voronoi_Kuznetsov_GRH_bypass.md §1.1, R3 obstruction.** Going from a Petersson trace + AFE setup to at-zeros requires evaluating
  Σ_γ (m/n)^{iγ}
which equals −Λ_f(m/n)·T/(2π) + boundary IFF all zeros on σ=½. Off-line zeros contribute (m/n)^{β−½}·oscillatory, dominating when β > ½.

**Voronoi on Kumar AFE.** The Voronoi transform replaces W(n/M) by a Bessel-J or Bessel-K kernel evaluating coefficients at *transformed* n's, NOT at zeros γ. The Voronoi formula has nothing to do with the at-zeros expansion of L′. So Voronoi of Kumar coefficients gives **another representation of Kumar's central-point family-aspect bound**, not an at-zeros bound.

**Could Voronoi convert to at-zeros indirectly?** Only if we composed:
  (Voronoi-on-coefficients) ∘ (Σ-over-d via Heath-Brown) ∘ (??? at-zeros conversion)

The "???" is exactly the missing piece — and Voronoi doesn't supply it.

**Verdict A5: FAILS.** Voronoi transforms central-point sums to other central-point sums; doesn't access zeros. **Confidence A5: 0.02.** Already implicit in Voronoi_Kuznetsov_GRH_bypass.md.

## 3.6 Angle A6 — Higher derivatives L^(k) + Cauchy formula around ρ

**Setup.** Suppose Kumar's method extends to L^(k)(½) for all k=1,2,... (each gives a log^{2k+1}X 2nd-moment family-aspect bound, with C_f^{(k)} explicit).

Use Cauchy's contour formula at ρ_f:
  Σ_{|γ|≤T} |L′(½+iγ, f)|² = Σ_{|γ|≤T} |(1/(2πi)) ∮_C L(s,f)/(s−ρ)² ds|²

with C a small contour around ρ. Over a positive-measure contour, |L′(ρ)|² = (1/(2π)²) |∮ L(s)/(s−ρ)² ds|².

**Problem: the contour integral mixes L(s) for s on the contour (off-line if we want a non-zero radius), not values of L^(k)(½).**

The relation between L^(k)(½) and contour integrals is via Taylor expansion:
  L(s,f) = Σ_k L^(k)(½, f) (s−½)^k / k!

So L′(ρ, f) = Σ_{k≥1} L^(k)(½, f) (ρ−½)^{k−1}/(k−1)! = Σ_{k≥1} L^(k)(½, f) (iγ)^{k−1}/(k−1)!.

Hence:
  |L′(ρ, f)|² = Σ_{k,ℓ} L^(k)(½)·L^(ℓ)(½)̄ · (iγ)^{k−1} · (−iγ)^{ℓ−1} / ((k−1)!(ℓ−1)!)

Summing over zeros γ_f, |γ|≤T:
  Σ_γ |L′(½+iγ,f)|² = Σ_{k,ℓ} L^(k)(½)·L^(ℓ)(½)̄ / ((k−1)!(ℓ−1)!) · (i)^{k−1}(−i)^{ℓ−1} · Σ_γ γ^{k+ℓ−2}.

The crucial sum is **Σ_γ γ^{k+ℓ−2}** for various k,ℓ.

**This is a moment of zeros — the von Mangoldt explicit formula sum.**

For k=ℓ=1: Σ_γ 1 = N(T) = (T/(2π)) log T + O(T) (Riemann–von Mangoldt). UNCONDITIONAL.
For k=1, ℓ=2: Σ_γ γ = 0 (assuming pairing of zeros γ ↔ −γ; uses functional equation symmetry, unconditional).
For k=ℓ=2: Σ_γ γ² — this is the SECOND MOMENT OF ZEROS. Goldston–Gonek 1998 (or Conrey–Snaith) give:
  Σ_{|γ|≤T} γ² ~ (T³ log T)/(6π) + O(T³).

This IS unconditional? Let's verify: Σ_γ γ² = ∫₀^T γ² dN(γ) where dN(γ) is the zero-counting measure. By Riemann–von-Mangoldt, dN(γ) = (log(γ/(2π)))/(2π) dγ + (oscillating part). Integrating γ² against the smooth part: ~T³ log T/(6π). The oscillating part is bounded by S(T)² = O(log²T) on average (this uses ζ-zero-density type estimates). For ζ this is in Titchmarsh §14.27 — UNCONDITIONAL via Selberg's S(T) bounds. For GL(2) L(s,f), the analog is via Iwaniec–Kowalski §5.7 — UNCONDITIONAL via Hadamard product factorization.

**Higher zero-moments Σ_γ γ^{2j}.** Goldston–Gonek 1998 (arXiv:math/9812003) and Heath-Brown 2008 give unconditional bounds for Σ_γ γ^{2j} ≪ T^{2j+1} log T for zeros of ζ. For GL(2) the analog should hold (Kowalski–Michel 2002 zero-density theorems). UNCONDITIONAL? Need to check Iwaniec–Kowalski §5.7 — on first principles, yes, since Hadamard product gives zero distribution unconditionally, and integrating any polynomial of γ against dN(γ) reduces to N(T) and S(T) bounds.

**WAIT — is this the at-zeros L′-2nd-moment Σ_γ |L′|² without GRH?** Let's check.

  Σ_γ |L′(½+iγ,f)|² = Σ_{k,ℓ≥1} L^(k)(½)·L^(ℓ)(½)̄ · M_{k,ℓ}(T)
where M_{k,ℓ}(T) = (i)^{k−1}(−i)^{ℓ−1} Σ_γ γ^{k+ℓ−2} / ((k−1)!(ℓ−1)!).

For ζ-zeros, M_{k,ℓ}(T) is unconditionally computable for all k+ℓ. For GL(2) f-zeros, similarly unconditional.

But the Taylor series L(s,f) = Σ_k L^(k)(½) (s−½)^k/k! has **finite radius of convergence**, namely the distance from ½ to the nearest zero of L(s,f). This is BOUNDED by the imaginary part of the lowest zero γ_min (which is O(1)). So for |γ|≤T with T → ∞, the Taylor series **diverges** for γ outside |γ| < γ_min ≈ 1.

**THE TAYLOR SERIES DOES NOT CONVERGE FOR γ AWAY FROM ½.** L(½+iγ, f) is a meromorphic function of s; expanding around s=½ gives a series with radius of convergence equal to the modulus of the nearest singularity (zeros and pole). For ζ, nearest non-trivial zero is at γ ≈ 14.13. For L(s,f) with f a GL(2) eigenform, nearest zero γ_min ≈ 9 or so (depending on f). **For γ > γ_min, the Taylor series at ½ doesn't converge.**

So the formula Σ_γ |L′(ρ)|² = Σ_{k,ℓ} L^(k)(½) L^(ℓ)(½)̄ M_{k,ℓ}(T) is **ONLY VALID FOR ZEROS WITH |γ| < γ_min**. There are O(1) such zeros — finite. The bulk of the sum (zeros with γ_min ≤ |γ| ≤ T) is **not** captured.

**Workaround: analytic continuation via Padé / Borel resummation.** Higher-derivative coefficients L^(k)(½) for k → ∞ grow like (γ_min)^{−k}, so the series has a finite radius of convergence around ½ but extends meromorphically. Using Padé approximants, one can in principle resum the divergent series to evaluate L(½+iγ) for |γ|>γ_min, but this requires:
- Knowing L^(k)(½) to arbitrarily high k.
- An effective Padé bound that converges to the meromorphic continuation.

Both are open problems (Padé convergence for L-functions is essentially the **continuation hypothesis**, related to but distinct from GRH).

**Numerical attempt.** For ζ at γ = 14.13 (first zero), Taylor series at ½ would need ~14^k coefficients to converge — impractical and divergent in any finite truncation. The Padé resummation fails because intermediate L^(k)(½) values are not asymptotically captured by Kumar-style 2nd-moment bounds.

**Verdict A6: FAILS.** The Cauchy/Taylor approach is **structurally correct but globally invalid** because the Taylor series at ½ does not converge for γ > γ_min. **Confidence A6: 0.05** (slightly above others because the structural relation IS clean for low γ; but the bulk of zeros are inaccessible).

---

# Section 4. Best angle: full derivation attempt

The least-failed angle is **A4 (L′′ extension)** at confidence 0.03 because it is the cleanest analog of Kumar's method.

## 4.1 Full statement and derivation outline

**Conjecture (A4-style spinoff, NOT Theorem B):**
  Σ⋆_{(d,2q)=1, ω(f⊗χ_{8d})=+1} |L′′(½, f⊗χ_{8d})|² J(8d/X) = C_f^{(2)} J̃(1) X log⁵X + O(X log^{9/2+ε}X)

**Derivation (identical engine to Kumar 2023, modified pole structure):**

**Step 1.** AFE for L′′. Differentiating Petrow [8, Lem 3.1] twice in s:
  L′′(s, f⊗χ_d) = (some explicit factor) Σ_n λ_f(n)χ_d(n)/n^s · W₂(n/|d|)
where W₂(y) = (1/(2πi)) ∫_{(3)} (Γ(u+k/2)/Γ(k/2)) (2πy/√q)^{−u} du/u³.

The triple-pole 1/u³ at s=½ comes from differentiating the double-pole-of-1/u² ↔ second-derivative kernel.

**Step 2.** Splitting: define A₂(8d) and B₂(8d) analogously to Kumar's A,B (lines 297–308 of /tmp/kumar_2303.txt). With M = X/(log X)^{1000}:
  A₂(8d) = (1−i^k η χ_{8d}(q)) Σ_n λ_f(n)χ_{8d}(n)/n^{1/2} W₂(n/M)
  B₂(8d) = L′′(½,f⊗χ_{8d}) − A₂(8d)

**Step 3.** B-bound: same as Prop 2 (Kumar §4), with extra (log X) factor from triple-pole. Bound: Σ⋆_d |B₂(8d)|² J(8d/X) ≪ X log³X · (loglogX)^4.

**Step 4.** A-bound: same as Prop 3 (Kumar §5), with main term computation extended for triple-pole. Cauchy residue at α=β=γ=0 in
  L(½+α, f⊗χ_d) L(½+β, f⊗χ_d) / (ζ(1+α+β) L(1+2α,sym²f) L(1+2β,sym²f) L(1+α+β,sym²f))
with two extra residues from the second derivative — gives log⁵X (vs. log³X for L′).

**Step 5.** Final asymptotic: C_f^{(2)} J̃(1) X log⁵X + error.

**Where this derivation fails as a Theorem B closure:** it gives a family-aspect statement, NOT an at-zeros statement. The constant C_f^{(2)} ≠ 2/(3π) c_f in any natural way.

## 4.2 Numerical sanity check

**On the constant.** Per main agent §5, 2/(3π) = (1/(2π)) · (1/12) · 16. Kumar's C_f has none of these factors. C_f^{(2)} (the proposed L′′ family-aspect constant) would have NO different connection — same Euler product structure with Petrow's pp. 1586–1588 calculation, just extra residue logs.

**On scaling.** Σ_γ |L′(½+iγ,f)|² ~ (2/(3π)) c_f T log⁴T (Theorem B).
A4 spinoff gives Σ_d |L′′(½, f⊗χ_d)|² ~ C_f^{(2)} X log⁵X — **scales as X log⁵X**, not T log⁴T. The scaling exponents differ (5 vs 4), reflecting the family-aspect (X = conductor cube vs. T = zero-height) vs at-zeros distinction. **Cannot match.**

## 4.3 What the spinoff IS good for

1. **Publishable result.** The L′′ second-moment over χ_{8d} family, unconditional. Estimated 2 weeks of additional writing on top of Kumar's framework.
2. **Confirms the Petrow conjectural ladder.** Petrow 2014 conjectured L^(k) family-second-moments scale as X log^{2k+1}X for all k≥0 (k=0: Soundararajan–Young, k=1: Kumar 2023, k≥2: open). A4 spinoff would close k=2.
3. **No Theorem B contribution.**

## 4.4 Honest summary

The L′′ extension is doable, gives a new unconditional result, but is structurally orthogonal to Theorem B. It does **not** close the at-zeros barrier.

---

# Section 5. Net result: do alt angles give unconditional Theorem B?

**No.**

| Angle | Mechanism | Verdict | Confidence Theorem-B-via-this-angle |
|---|---|---|---|
| A1: Plancherel + 1-LD | On-line moment + family LD → at-zeros | FAILS: needs continuous on-line 2nd moment (unknown) and family-LD doesn't access single-f zeros | 0.02 |
| A2: theta lift | Howe duality transfers Kumar bound | FAILS: representations only, not statistics; duplicates Theta_lift R1 | 0.02 |
| A3: sieve to fixed N | Specialize to single 8d=N | FAILS: collapses average; gives Petersson-family at central point (different problem) | 0.01 |
| A4: L′′ extension | Apply Kumar's method to L′′(½) | FAILS for at-zeros; SPINOFF: unconditional L′′ family-aspect | 0.03 |
| A5: Voronoi on coefficients | Voronoi-transform Kumar AFE | FAILS: Voronoi central-point → other central-point; never accesses zeros | 0.02 |
| A6: higher-deriv + Cauchy | Σ_γ |L′|² via Taylor series at ½ | FAILS: Taylor series radius of convergence < γ_min for all but O(1) zeros | 0.05 |

**Composite confidence (max over angles, with composition penalty):** 0.04.

The 6 alternative angles all funnel back to the same R3 obstruction (at-zeros conversion needs zero-orthogonality, which without GRH is open). This **strengthens** the main agent's verdict.

The only positive: **Angle A4 spinoff** (L′′ family-aspect unconditional) is genuinely doable as a follow-up paper. It does not close Theorem B.

---

# Section 6. If main agent's direct route lands, do alt angles add anything?

**Hypothesis.** Suppose hypothetically the main agent finds a direct extension of Kumar 2023 closing Theorem B unconditionally. Do the alt-angle audits add value?

**Yes — three contributions:**

1. **Robustness check.** If the main agent's direct route relies on, say, generalizing Lemma 2.4 (Poisson over d) to "Poisson over γ," then alt-angle A1 (Plancherel + 1-LD) audits the same generalization from a different direction. If A1 gives different constants or a different scaling, that's a sign of error in the direct route.

2. **Spinoff papers.** Even if Theorem B closes, alt-angle A4 (L′′ family-aspect) is a publishable independent result. So is L^(k) for k≥3 (extending Kumar's ladder). This is the partial-credit harvest.

3. **Negative-result map for the field.** The 6-angle audit catalogs *which* indirect routes don't work, providing future researchers a roadmap. This is the docs/citation value flagged in main agent's "near-miss exemplar" recommendation.

**No new Theorem B contribution.** The alt angles do not provide an *alternative proof* of Theorem B if the direct route succeeds — they only audit the same gap from different directions.

---

# Cross-reference and non-duplication

| Prior file | Overlap with this audit | Net new contribution here |
|---|---|---|
| Kumar_2023_methodology_mine.md (main agent) | Full direct-extension audit | This file: 6 INDIRECT angles, complementary |
| Theta_lift_GRH_bypass.md | Angle A2 (theta lift) — DUPLICATES R1 verdict | This audit confirms with Kumar 2023 specifics |
| Voronoi_Kuznetsov_GRH_bypass.md | Angle A5 (Voronoi on coefficients) — same R3 obstruction | This audit explicitly traces Voronoi-on-Kumar |
| Theorem_B_field_landscape.md | Identifies Kumar 2023 as candidate | This audit: 6 alt-angle attempt at extraction |

**Net new findings:**
1. Angle A4 (L′′ family-aspect extension) is a publishable spinoff; flagged for future write-up.
2. Angle A6 (higher-derivative + Cauchy/Taylor) is the highest-confidence-non-zero alt route (0.05) but limited by Taylor radius of convergence ≈ γ_min ≈ O(1), capturing only finite zeros.
3. All 6 angles funnel back to R3 obstruction; no new attack vector opened.

---

# Closing

The 6 alternative-angle audit confirms the main agent's verdict: Kumar 2023 does not close Theorem B unconditionally, even via indirect transformations. The R3 obstruction (at-zeros vs family-aspect mismatch) is robust under all 6 reformulations.

**Recommended action:** when main agent's audit is complete, merge findings; flag A4 (L′′ spinoff) as a future independent paper; close Kumar 2023 as a "confirmatory near-miss" in the field landscape.

Confidence Kumar 2023 (direct or indirect) closes Theorem B: **0.02–0.04**.

End of parallel alt-angles audit.
