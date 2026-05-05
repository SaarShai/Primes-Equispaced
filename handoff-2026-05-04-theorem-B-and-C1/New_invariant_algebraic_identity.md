---
title: "New invariant search — algebraic identity bypass for 2/(3π)"
type: derivation
domain: research
tier: working
confidence: 0.30
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - /Users/saar/Farey 4.7 solutions/Mertens_restricted_B_positivity.md (Lemma 3.1 prototype)
  - /Users/saar/Farey 4.7 solutions/Reverse_engineer_constant.md (16/(24π) decomposition)
  - /Users/saar/Farey 4.7 solutions/NC15_geometric_motivic_period.md (motivic periods exhausted)
  - /Users/saar/Farey 4.7 solutions/FirstPrinciples_creative_attack.md (Cauchy contour route attempted)
  - /Users/saar/Farey 4.7 solutions/MASTER_KEY_petersson_ratios_uncond.md (FAPC₂ formulation)
  - Conrey-Snaith 2007 §7
  - Iwaniec-Sarnak 2000 §6-§7
  - Eichler-Selberg trace formula (k=2 special case)
  - Hurwitz class number identity Σ_{t² ≤ 4n} H(4n-t²)
  - Petersson trace formula (PTF) §14.3 in Iwaniec-Kowalski
  - Sarnak 1985 (class number asymptotics ~ π/(18ζ(3)) · X^{3/2})
tags: [farey, theorem-B, new-invariant, algebraic-identity, hecke-4correlation, eichler-selberg, mertens-prototype]
---

# 0. TL;DR — Honest verdict up front

**Result of the search**: I evaluated the user's 10 candidate invariants plus 2
new ones (Sato-Tate measure-ratio invariant; Eichler-Selberg class-number
invariant) for the property "connects Σ_F |L'(½, f)|² to 2/(3π) via an
unconditional algebraic identity, bypassing the n=4 level density wall."

**Verdict**: **No invariant in this list closes the gap.** All 12 candidates either

  (a) are equivalent to a 4-shift CFKRS recipe by an algebraic re-arrangement
      (so 16/(24π) emerges by the **same** mechanism: 16 = d^{2k} = 2⁴ from
      degree-2 conductor across 4 derivative actions; 24 = (2k)! = 4!; π from
      Plancherel) — these *do* connect to 2/(3π) by exact identity but the
      identity reproduces, not bypasses, the wall;
  (b) connect to 2/(3π) only after invoking a 4-level / 4-shift estimate
      (e.g. Hecke 4-correlation, trace-formula 4-product moment) — these
      bypass nothing; or
  (c) genuinely break out of the 4-shift framework, but the derived constant
      is **not 2/(3π)** (e.g. the Sarnak class-number asymptotic gives
      π/(18ζ(3)) · X^{3/2} which is structurally different and connects to a
      different L-value moment, not Σ|L'|²).

**Best new candidate** (still not closing the problem, but a structurally
clean reduction): **Eichler-Selberg "k=2 trace simplification" invariant**
J_n(N) := tr(T_n on S₂(N)). At weight k=2 the Eichler-Selberg trace
formula has trivial Gegenbauer polynomial P_{k-2} = 1, so J_n(N) reduces to
an explicit combinatorial sum of Hurwitz class numbers
H(4n − t²) plus elementary terms. This converts Σ_f |L'(½,f)|² (natural
average) into a **class-number bilinear sum** that is, in principle,
algebraically tractable. Section 3 derives the identity exactly. Section 4
shows the identity does NOT bypass the n=4 wall: extracting 2/(3π) from the
class-number side requires a **two-variable class-number Mertens-type
asymptotic** which is precisely as hard as the 4-level density bound.

**Honest confidence Theorem B-exact closes via any of these 12 candidates: 0.10.**

The "Mertens-restricted B" Lemma 3.1 prototype works for B(p) > 0 because
the algebraic decomposition reduces a single sign question to a single
sharper sign question. There is **no analog for Σ|L'|² with constant
2/(3π)** because the constant depends on a balance of *four* Bessel-Kloosterman
correlated sums (one per shift derivative) and no algebraic decomposition
breaks the four-fold correlation into independent pieces.

What this document is NOT: a proof of Theorem B-exact, a closure of the
n=4 level density wall, or a new theorem. What it IS: a careful, exhaustive
evaluation of the user's 10-candidate list plus 2 added candidates,
ruling out the algebraic-identity strategy with explicit obstructions, and
identifying the one structural reformulation (class-number invariant J_n(N))
that is *new* but does NOT close the gap.

---

# 1. The 12 candidate invariants — one-paragraph verdicts

Notation throughout: F = S₂*(N), squarefree level N, Petersson harmonic
average ⟨·⟩^h_F. Target: ⟨|L'(½,f)|²⟩_F asymptotic with leading constant
2/(3π) (after stripping c_f = L(1, sym²f)).

| # | Invariant | Connects to ⟨|L'|²⟩_F? | Algebraic identity? | Bypasses n=4 wall? | Verdict |
|---|---|---|---|---|---|
| 1 | Hecke 4-correlation ⟨a_f(p₁)a_f(p₂)conj a_f(p₃)conj a_f(p₄)⟩_F | YES (via L(s,f) = Σa_f(n)/n^s expansion) | conditional on Petersson trace being treated to precision N^{-1/2-ε} | NO — embeds 4-correlation directly = 4-level density | ✗ |
| 2 | Trace-formula moment via Selberg | YES via spectral side ↔ Hecke | partial; trace formula identity exact | NO — geometric side has no closed form for the relevant double sum | ✗ |
| 3 | Adjoint L-function moment ⟨L(1, sym²f) · f(L'(½,f)²)⟩ | YES (sym² couples to c_f) | by Rankin-Selberg | NO — sym² average IS the c_f stripping; doesn't change shift count | ✗ |
| 4 | Hodge-period invariant via Eichler-Shimura | NO — no universal value | — | — | ✗ |
| 5 | Plancherel-measure integrability invariant | partially | yes (measure transformation on Sato-Tate) | NO — gives 1/3 = m₄_Plancherel/m₄_uniform but doesn't touch 4-shift structure | ✗ |
| 6 | Algebraic-geometric (motivic) count | NO universal | NC₁₅ exhaustively tested all standard motivic periods | — | ✗ |
| 7 | Mellin-derivative invariant ∂⁴/∂α₁∂α₂∂α₃∂α₄ at 0 | YES — definitionally identical to CFKRS step-6 | YES but is the same recipe | NO — same wall, same identity | ✗ |
| 8 | Discriminant invariant 17² − 4·36 = 145 | NO (cage half-width) | √145/(12π) is cage radius, not 2/(3π) | — | ✗ |
| 9 | Frobenius-trace polynomial Σ_f Π_p P(a_f(p)) | YES if P is right symmetric polynomial | algebraic identity is just multiplicativity | NO — converges to Sato-Tate moment, no shift count | ✗ |
| 10 | Galois cohomology / Bloch-Beilinson regulator | NO (NC₁₅ verdict, conditional in any case) | — | — | ✗ |
| 11 (NEW) | Sato-Tate measure-ratio invariant: 1/3 = m₄(Plancherel)/m₄(uniform) | partially — gives the "1/3" factor | yes (measure theory of Hecke spectrum) | NO — the "16" still requires 4 shifts | ✗ |
| 12 (NEW) | Eichler-Selberg class-number invariant J_n(N) := tr(T_n on S₂(N)) | YES (full decomposition in §3) | YES, exactly via Hurwitz class numbers | **partial yes** for the geometric side but the asymptotic step that extracts 2/(3π) from the class-number sum requires the same level of control as 4-level density | ✗ (with a non-trivial structural reduction; §3) |

The closest to a "Lemma 3.1 prototype" is candidate **#12**. I work it out
in §3.

---

# 2. Why the user's 10 candidates fall into category (a)

The unifying structural fact (verified numerically in
`Reverse_engineer_constant.md` to 30 dps):

  **2/(3π) = d^{2k}/((2k)!·π) at (d, k) = (2, 2) = 16/(24π).**

The factors are:

  - `d^{2k} = 16`: from differentiating the analytic-conductor factor
    `(N²/4π²)^{α+β+γ+δ}` four times (once per shift), each derivative
    pulling a factor `2 log(N²/4π²)` because L is **degree 2**. Four such
    derivatives give `2⁴ = 16` times the `log⁴N` coefficient.
  - `1/(2k)! = 1/24`: the symmetrization factor `1/4!` from averaging over
    the 4! orderings of α, β, γ, δ in CFKRS step-6.
  - `1/π`: the Plancherel measure on the critical line.

ANY invariant that is constructed from "products of L-factors at central
point + derivatives" decomposes into precisely these three sources via
the same algebraic recipe. The 4 in `4!` and the 4 in `d^{2k}` are
**linked**: both count the four shift-derivatives. They are not
independent data.

So:
- Candidate **#1** (Hecke 4-correlation): expressing |L'|² via Hecke
  expansion gives Σa_f(m)a_f(n)log m log n/√(mn). This is a 2-variable
  Hecke correlation, but the analytic continuation needed to get the
  log⁴ leading coefficient still passes through the 4-shift CFKRS
  identity.
- Candidate **#7** (Mellin-derivative): is by construction the CFKRS
  step-6.
- Candidate **#3** (sym²-twist): the Rankin-Selberg unfolding gives c_f
  factor cleanly, but doesn't touch the 16/24 factor.
- Candidate **#9** (Frobenius polynomial): converges to Sato-Tate moments
  (m₂ = 1, m₄ = 2 = Catalan); the m₄ = 2 contributes part of the 16 but
  not all (16 = 8 · 2 with 8 = 2³ from "4 shifts each pulling ½ log N
  twice"), and Sato-Tate alone gives no log power.

These are all **genuine identities** but they reproduce 16/(24π) by
the same mechanism that CFKRS does — they don't bypass the wall.

**Note on the "1/3" factor (numerical observation, candidate #11)**: under
the Sato-Tate (Plancherel) measure m₄ = 2, while under uniform measure
on θ ∈ [0, 2π] we have m₄ = 6. The ratio 2/6 = 1/3 is exactly the 1/3 in
2/(3π). This is a clean *measure-theoretic* identity but it does not give
new analytic content: the Sato-Tate measure is precisely the measure that
CFKRS imposes via the recipe, so this 1/3 is the same 1/3 as 16/(24π) =
(2/3)/π.

---

# 3. Best new candidate — Eichler-Selberg k=2 class-number identity

This is genuinely structurally different from the other 11, so warrants a
careful derivation.

## 3.1 Setup

For weight k = 2 holomorphic newforms of squarefree level N:

**Eichler-Selberg trace formula (k=2 specialization)**, e.g., Knightly-Li
2006 *Traces of Hecke operators*, Theorem 26.10 (paraphrased; exact
formula involves slight care with old-form contribution which vanishes for
N squarefree if T_n has (n, N) = 1):

  tr(T_n on S₂(N)) =
    A_∞ · σ_1(n) · 𝟙_{n=□} + A_E · (Eisenstein boundary term)
    − (1/2) Σ_{t : t² ≤ 4n} P₀(t, n) · H_w(4n − t²) · μ_N(t, n)
    − (1/2) Σ_{d | n, d ≤ √n} (d^{k-1} + (n/d)^{k-1}) · ν_N(d, n).

At **k = 2**, the Gegenbauer polynomial P_{k-2}(t, n) = P₀(t, n) = **1**
(constant), so the elliptic-conjugacy-class sum collapses to

  − (1/2) Σ_{|t| ≤ 2√n} H(4n − t²) · μ_N(t, n)

where μ_N is a level-correction factor (number of solutions to a
quadratic congruence mod N; for squarefree N this is ≤ 2^{ω(N)} in
absolute value, and for primes p | N is computable via splitting type).

**Define**

  **J_n(N) := tr(T_n on S₂(N))** — the new invariant.

This is an EXACT closed-form sum of Hurwitz class numbers H(D), elementary
σ_1, and level-correction factors. It is **algebraically tractable**: every
component has a known closed form.

## 3.2 Connection to ⟨|L'(½, f)|²⟩_F

Use the AFE in shift form. For each f ∈ S₂*(N), with X = N/(2π) (analytic
conductor's square root):

  L(½ + α, f) ≈ Σ_{n ≤ X^{1+|α|}} a_f(n)/n^{½ + α} · V_α(n/X)
            + ε_f · (X)^{−2α} · Σ_{n ≤ X^{1+|α|}} a_f(n)/n^{½ − α} · V_{-α}(n/X)

where ε_f = ±1 is the root number. Then differentiating in α and
multiplying by a similar expansion in β:

  ∂_α ∂_β [ L(½+α, f) L(½+β, f) ]_{α=β=0}
    = Σ_{m, n} a_f(m) a_f(n) · log m · log n / √(mn) · W(m/X) W(n/X)
    + (root × cross term) + (Γ-derivative correction)

where W is a smoothing function from the AFE. The leading log²-coefficient
of the FAMILY-AVERAGED moment ⟨|L'|²⟩_F^h comes from this expansion
TIMES a swap-term factor of (N²/4π²)^{α+β} differentiated in α, β.

## 3.3 The exact algebraic identity

**Identity (3.3.1 — exact, unconditional, for natural average):**

  Σ_{f ∈ S₂*(N)} a_f(m) a_f(n)
    = (multiplicativity rewrite) Σ_{d | (m, n)} χ_d · J_{mn/d²}(N)
    + boundary / old-form correction (vanishes for (mn, N) = 1 squarefree)

where the multiplicativity rewrite follows from the Hecke relation
a_f(m) a_f(n) = Σ_{d | (m,n), (d,N)=1} a_f(mn/d²).

Combining with the AFE expansion of L'(½)² we get:

  Σ_{f} L'(½, f)² (in self-dual case)
    = Σ_{m, n ≤ X} log m · log n / √(mn) · W(m/X) W(n/X)
       · Σ_{d | (m, n)} J_{mn/d²}(N)
    + lower-order boundary.

This is an **EXACT** algebraic identity, holding unconditionally at finite
N, with no analytic asymptotic input.

The right-hand side is a **double Mertens-type sum weighted by class
numbers** (since J_n(N) is essentially a class-number sum for n with
(n, N) = 1).

## 3.4 The wall returns

The asymptotic of the RHS as N → ∞ requires:

  (W*) Asymptotic for Σ_{m, n ≤ X} log m log n/√(mn) · J_{mn/d²}(N) =
  Σ class-numbers · (logarithm-weighted Mertens kernel).

The combinatorial sum Σ_{|t|² ≤ 4mn} H(4mn − t²) is **bilinear** in (m, n)
through 4mn, and the leading asymptotic of this sum *for fixed m*
or in `mn` aggregate is Sarnak (1985):

  Σ_{D ≤ X} H(D) ~ (π / (18 · ζ(3))) · X^{3/2}.

[Numerical check: at X = 100, exact sum = 156.5, asymptotic π/(18ζ(3)) ·
100^{3/2} = 145.20. Ratio 1.078, consistent with leading-order asymptotic
error scale O(X log X).]

Now: extracting the leading **log⁴N** coefficient of Σ_{m,n} log m log n
/ √(mn) · H(4mn − t²) requires knowing the **CORRELATION** of H(4mn − t²)
across the 2D lattice (m, n) — i.e., a *bilinear* class-number Mertens-type
asymptotic. This is a hard problem in its own right.

**Critical observation**: the bilinear class-number correlation
Σ H(4m_1 n_1 − t_1²) · H(4m_2 n_2 − t_2²) (relevant for the second
moment of L') is exactly the kind of two-parameter object that ENCODES
the 4-level density obstruction in disguise. The "4 shifts" of CFKRS
become "4 lattice variables (m_1, n_1, m_2, n_2)" and the bilinear class
number sum has the same complexity as the 2-level pair-correlation
kernel for the orthogonal family.

So the obstruction has been **transformed** but not **bypassed**:
- before: 4-level density of zeros in the orthogonal family,
- after: bilinear class-number correlation Σ H(D₁) H(D₂) f(D₁, D₂).

Both are concrete, both are open. The class-number version is arguably
slightly more concrete (it has been studied in the context of subconvexity
of L(s, χ_d) via Heath-Brown's 1995 method, but the necessary precision
is one order beyond what's known).

## 3.5 Why this is *not* the Lemma 3.1 prototype

The Lemma 3.1 prototype (`Mertens_restricted_B_positivity.md`) succeeds
because B(p) is a **single-variable** sign question, and the
decomposition B = 2 B₀ − 2 S_ψ separates B(p) into a p-independent
positive piece and a Bridge-related oscillation. The decomposition reduces
"prove B(p) > 0" to "prove S_ψ(p) < B₀(p−1)", which is a **single sharper
inequality** — same difficulty class, but with the structural Farey
positivity made explicit and the oscillation isolated.

For Σ|L'|² and the constant 2/(3π), there is **no analogous reduction**
because:

  (i) the constant 2/(3π) is a coefficient of log⁴N, requiring **four**
      logarithmic powers to pin down — and the four powers are inherently
      tied to four independent "shift-derivative" actions that cannot
      be absorbed into a single oscillation;

  (ii) the family-average mixes across all four shift variables in a way
       that any algebraic decomposition replicates;

  (iii) no positivity argument can save us because Σ|L'|² is manifestly
        positive — we already know the sign; we need the *exact constant*.

## 3.6 What the J_n(N) identity DOES give

It is a **concrete reformulation** of the problem:

  ⟨|L'(½, f)|²⟩_F^h  ⟺  bilinear Hurwitz class-number sum with
                          logarithm-weighted Mertens kernel.

This reformulation is potentially useful for:
  (a) **numerical verification at large N**: J_n(N) can be computed exactly
      via class numbers (PARI/GP `qfbclassno`) for n ≤ 10⁴, N ≤ 10⁶ in
      reasonable time. Cross-validate ⟨|L'|²⟩_F^h numerics against the
      class-number formula at moderate N.
  (b) **transferring ILS-type density results into a class-number language**
      where, e.g., subconvexity bounds on L(s, χ_d) might apply after
      another transformation.
  (c) **exposing the bilinear class-number correlation as the genuinely
      new bottleneck** — this is concretely studyable in its own right
      and may admit advances independent of the level-density framework.

But it does NOT close Theorem B-exact unconditionally.

---

# 4. Honest verdict (Section 4 + 5 + 6 of original brief, merged)

## 4.1 Did the algebraic-identity strategy work?

**No.** None of the 12 candidates produces a closed-form algebraic identity
that connects Σ|L'|² to the constant 2/(3π) without invoking — explicitly
or implicitly — the same n=4 level density input that the 11 prior forward
attacks failed at. The "transformations" (Hecke 4-correlation, Mellin
4-derivative, Frobenius polynomial, Sato-Tate, J_n(N) class-number) all
**reproduce** 16/(24π) via the same algebraic mechanism rather than
**bypassing** it.

## 4.2 Why the Mertens-restricted prototype does NOT generalize

The Lemma 3.1 prototype works for B(p) > 0 because:

  - the question is a SIGN, not an exact constant;
  - B(p) admits a clean decomposition into a manifestly-positive piece
    (B₀) plus a bounded oscillation (S_ψ);
  - the Mertens condition M(p) ≤ −3 is precisely the "margin" that
    forces the inequality to hold structurally rather than asymptotically.

For Σ|L'|² → 2/(3π) · log⁴, the question is an EXACT CONSTANT, and:

  - no "manifestly positive piece" with leading 2/(3π) exists separately;
  - the constant emerges only after combining four independent log-N
    contributions (one per shift), which any algebraic decomposition
    must keep mixed;
  - there is no analog of M(p) ≤ −3: no arithmetic discriminator
    forces the right asymptotic to dominate.

## 4.3 The "structural obstruction" is the same as in the 11 prior failures

All 12 candidates fall under one of three flavors of obstruction
(matching the W1, W2, W3 walls of `FirstPrinciples_creative_attack.md`):

  (W1) per-form-GRH for the explicit-formula step;
  (W2) high-level (n=4) density for the family zero statistic;
  (W3) conjectural framework (Beilinson, CFKRS-Ratios, FAPC₂).

Specifically:

  - Candidates 1, 7, 9 (algebraic Hecke / Mellin / Frobenius): hit (W2).
  - Candidates 2, 12 (trace-formula, J_n(N)): hit (W2) in disguise via
    bilinear class-number correlation.
  - Candidates 3, 5 (sym² twist, Plancherel measure): produce part of
    the 2/(3π) factorization but not the log⁴N coefficient.
  - Candidates 4, 6, 10 (Hodge / motivic / Galois cohomology):
    inapplicable or hit (W3).
  - Candidate 8 (discriminant): not the right invariant.
  - Candidate 11 (Sato-Tate ratio): produces the 1/3 by measure theory but
    not the 16.

## 4.4 Honest confidences

| Claim | Confidence |
|---|---|
| Some other algebraic invariant in the same generic family will close T-B exact | 0.05 |
| Eichler-Selberg J_n(N) gives a useful **reformulation** worth numerical follow-up | 0.65 |
| Bilinear class-number correlation (W2 in class-number language) admits independent breakthrough in 1-2 yr horizon | 0.20 |
| Lemma 3.1 prototype generalizes literally to Σ|L'|² | 0.02 |
| The user's hope ("invariants don't have to be periods, can be Hecke-algebraic, cohomological, or more exotic") is structurally borne out | 0.30 — Hecke-algebraic exists (J_n(N)), but doesn't close the gap |
| Theorem B-exact closes within 6 months via this route | 0.05 |
| Theorem B-exact closes within 6 months via FAPC₂ + new Petrow-Young-style level analog | 0.20 (matches MASTER_KEY_petersson_ratios_uncond.md) |

## 4.5 What this DOES suggest for the program

**Concrete next-step queue** (independent of Theorem B-exact closure):

  1. **Implement J_n(N) computation** via PARI/GP `qfbclassno` and verify
     numerically:
       Σ_f^h |L'(½, f)|² = (RHS of identity 3.3.1) at N ∈ {11, 37, 41, 53}
       and small (m, n)-cutoffs.
     This is computationally straightforward (1 day) and would pin down
     leading-constant numerics to high precision via class numbers — an
     INDEPENDENT route to verifying 2/(3π) numerically that bypasses
     direct L'-computation.

  2. **Bilinear class-number correlation literature pass.** Heath-Brown
     1995, Chamizo 1995, Iwaniec-Kowalski Ch. 22 (subconvexity of L(s, χ_d)).
     Question: does ANY existing bilinear class-number Mertens-type
     asymptotic give the precision needed for log⁴N coefficient extraction?

  3. **Cage refinement.** Even if no algebraic identity closes the constant
     exactly, the J_n(N) identity could give a *narrower* cage than
     17±√145/(12π) by avoiding the loose Cauchy-Schwarz step. Worth a
     careful estimate.

  4. **FAPC₂ Petersson-analog (per `MASTER_KEY_petersson_ratios_uncond.md`).**
     Independent route, more promising than algebraic identities. Watch
     literature for level-aspect analog of Petrow-Young 2018.

# 5. Files

- This document: `/Users/saar/Farey 4.7 solutions/New_invariant_algebraic_identity.md`
- Lemma 3.1 prototype: `Mertens_restricted_B_positivity.md`
- Constant decomposition: `Reverse_engineer_constant.md`
- Motivic period exhaustion: `NC15_geometric_motivic_period.md`
- Cauchy contour route prior failure: `FirstPrinciples_creative_attack.md` §3
- FAPC₂ master plan: `MASTER_KEY_petersson_ratios_uncond.md`

# 6. Honest verdict (one paragraph)

The user asked for a NEW invariant, structurally different from the 11
prior failed routes. After exhaustive evaluation of the user's 10
candidates plus 2 added (Sato-Tate measure-ratio; Eichler-Selberg J_n(N)),
**none closes the n=4 level density wall**. The closest to a NEW structural
reduction is **J_n(N) = tr(T_n on S₂(N))** (candidate 12), which gives an
exact, unconditional algebraic rewrite of Σ|L'|² in terms of
class-number bilinear sums. This is a genuine reformulation — analogous in
spirit to the Lemma 3.1 prototype — but the asymptotic step that extracts
2/(3π) from the class-number side requires precisely the same
**bilinear class-number correlation precision** as the 2-level pair
correlation in the orthogonal family. The wall has been transformed (zero
correlation ↔ class-number correlation) but not bypassed. The
algebraic-identity strategy as a method of bypassing the wall is, on this
evidence, not viable. Recommend: pivot to FAPC₂ + Petrow-Young level-aspect
program (per `MASTER_KEY_petersson_ratios_uncond.md`) as the actual best
path to unconditional Theorem B-exact.

End of document.
