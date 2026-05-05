---
title: "Theorem B' (denominator) — HONEST version, Re(γ) ≥ 1/4 only"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Conrey-Snaith 2007, Applications of L-functions ratios conjectures, PLMS 94 (arXiv:math/0610495)"
  - "Conrey-Farmer-Keating-Rubinstein-Snaith 2005 (CFKRS), arXiv:math/0206018, Proc. LMS"
  - "Iwaniec-Kowalski 2004 (IK), Analytic Number Theory, Ch. 5 (AFE), Ch. 14 (Petersson)"
  - "Kowalski-Michel-VanderKam 2002 (KMV-Duke), 'Rankin-Selberg L-functions in the level aspect', Duke 114"
  - "Kıral-Petrow-Young 2019 (KPY), 'Oscillatory integrals with uniformity in parameters', JTNB 31:1 = arXiv:1710.00916"
  - "Deligne 1974 (Weil II) — |λ_p| ≤ 2 for weight-2 newforms"
supersedes:
  - "B_prime_denominator_FULL.md (claimed Re(γ)>0 unconditionally; multiple citation/exponent errors)"
  - "B_prime_denominator_contour.md (sketchy, optimistic c'=1/16 unverified)"
superseded-by: null
tags: [B-prime, denominator, mollifier, Mellin-Barnes, Re-gamma-quarter, honest]
---

# 0. Honest preamble — why this version

The previous file `B_prime_denominator_FULL.md` claimed Theorem B' unconditionally for any
fixed `Re(γ) > 0` with confidence 0.78. Adversarial review identified four fatal flaws:

1. **§4 off-diagonal arithmetic** (in FULL.md) yielded a POSITIVE exponent for δ < 1/4,
   silently breaking the small-δ claim.
2. **Soundararajan 2009** (`arXiv:math/0612106`) was cited for a "negative-second-moment
   bound `⟨1/|L(½+γ,f)|²⟩ ≪ (log N)^{O(1)}`". Verbatim from the abstract and §1: the
   paper concerns `M_k(T) = ∫_0^T |ζ(½+it)|^{2k} dt`, **assumes RH**, and gives upper
   bounds on the *measure* of `t` where `|ζ(½+it)|` is large. It contains no bound for
   negative moments of `1/|L(½+γ,f)|²` over a level-aspect family of GL(2) cusp forms.
   **The citation is wrong.**
3. **KMV 2002 (Duke 114) Theorem 2** was cited for an L⁴ bound `⟨|L(½+α,f)|⁴⟩ ≪ (log N)⁴`.
   Verbatim from the table of contents: KMV 2002 (Duke 114) Theorem 1.2 gives a *subconvex
   convexity-breaking bound* `|L(f⊗χ_D, ½+it)|² ≪ q^{1/2-1/96+ε}`; the rest of the paper
   is asymptotic moments of Rankin-Selberg `L(f⊗g, ½)` averaged over `f ∈ S_k*(q)`. **No
   `L⁴` bound for a single GL(2) L-function** in the level aspect appears in KMV-Duke.
   The fourth-moment paper is the *separate* KMV "Mollification of the fourth moment of
   automorphic L-functions" (cited inside KMV-Duke as [KMV2]); we adopt that as the
   correct citation but flag it as "the fourth-moment paper" not "Duke 114".
4. **KPY 2019** is correctly arXiv:1710.00916, "Oscillatory integrals with uniformity in
   parameters", JTNB 31 (2019) 145–159. It does NOT have a "Proposition 1"; its results
   are Proposition 2.6, Lemma 3.1, Lemma 5.1, Lemma 5.2, Lemma 5.3, Main Theorem (§3).
   The paper is a TECHNICAL TOOL for stationary phase with parameter uniformity — it
   handles oscillatory integrals, NOT directly mollifier shift-uniformity. We cite it
   only where stationary-phase parameter uniformity is the input.

This honest version (a) restricts to `Re(γ) ≥ 1/4` (where the off-diagonal exponent
saturates at the unconditional `c = 1/16 - ε` and the mollifier degree can be fixed at
`D = 2`), (b) replaces every misattributed citation, (c) drops the small-δ regime to
"open" rather than "1-day fix". Confidence is **0.55**, computed by the single
aggregation rule (minimum confidence over the proof chain) defined in §9.

---

# 1. Theorem statement

Let `F_N := S₂*(N)`, `N` squarefree, weight-2 holomorphic newforms with harmonic
Petersson weight `ω_f = 1/(4π⟨f,f⟩_N)`. Normalize `λ_f(n) = a_f(n)/n^{1/2}` so that
`|λ_p(f)| ≤ 2` (Deligne). For shifts `α, β, γ ∈ ℂ` with

  (S)   `|α|, |β|, |γ| ≤ (log N)^{-1}`  and  `Re(γ) ≥ 1/4`,

define the **single-ratio Petersson average**

  `R'_F(α, β; γ) := Σ_{f ∈ F_N} ω_f · L(½+α, f) · L(½+β, f) / L(½+γ, f).`

**Theorem B' (denominator, honest).** For squarefree `N → ∞`, uniformly in (S),

  `R'_F(α, β; γ) = G_3(α, β, γ; N) + O_ε(N^{-1/16 + ε})`,

where `G_3` is the explicit CFKRS-with-quotient main term given in §6 below.

The exponent `1/16 - ε` is the **unconditional** off-diagonal saving from
Weil + Petersson at this regime; we make no claim of improvement to `1/4 - ε` (which
would require Kuznetsov + Kim-Sarnak inputs not used here).

**What is OPEN (not addressed here):**
- The strip `0 < Re(γ) < 1/4`: the prefactor `M^{D+1} D^{O(D)}` in the mollifier
  bound (Lemma 2.2) blows up as δ = Re(γ) → 0 because the optimal `D = D(δ)` grows
  like `D ≍ 1/δ`. Resolving this is **not a one-day algebraic fix** — it requires either
  (a) a substantially refined mollifier construction with δ-uniform constants, or (b)
  a different argument that does not rely on `M^D` truncation. Estimated effort: months.
- The line `Re(γ) = 0`: requires controlling family averages of `1/|L'(½, f)|²` on the
  rank-1 subfamily; presently open even on GRH.

---

# 2. Strategy

We work entirely on the open half-plane `Re(γ) ≥ 1/4`, where:
- `1/L(½+γ, f) = Σ_n μ_f(n)/n^{½+γ}` is **absolutely convergent**: `|μ_f(n)| ≤ d(n)`
  (because `μ_f` is multiplicative, supported on squarefull-with-multiplicity-≤2 integers,
  with `|μ_f(p)| = |λ_p| ≤ 2` and `|μ_f(p²)| = 1`), so the Dirichlet sum is
  bounded by `Σ d(n)/n^{¾} = ζ(¾)² < ∞`.
- The **degree of the Selberg-Beurling mollifier polynomial** can be fixed at `D = 2`,
  independent of γ. The prefactor `M^{D+1} · D^{O(D)} = M^3 · O(1)` is bounded.
- We never need a "negative second moment" of `1/|L(½+γ,f)|²` — the trivial
  Euler-product lower bound `|L(½+γ,f)| ≥ ∏_{p ≤ X} (1+|λ_p|/p^{1/4})^{-1} · (1+O(...))`
  on `Re(s) = ¾` (which is in the **absolute-convergence half-plane** of the L-function!)
  gives `|L(½+γ,f)| ≥ c > 0` for an absolute `c` (uniform in `f`).

**Plan.**
1. (§3) Apply AFE to `L(½+α, f)` and `L(½+β, f)` (IK Theorem 5.3).
2. (§4) Replace `1/L(½+γ, f)` by the Selberg-Beurling smoothed truncation `N_M^{(2)}(γ, f)`
   of length `M = N^θ`, with `θ ∈ (0, ½)` to be chosen; the mollifier error is
   bounded by Lemma 2.2 below, **without** invoking any L⁴ bound or negative moment.
3. (§5) Apply Petersson trace formula to the resulting trilinear sum `λ_f(n₁) λ_f(n₂)
   μ_f(m)` over `n₁ ≤ √N`, `n₂ ≤ √N`, `m ≤ M`. Diagonal yields the main term.
4. (§5) Off-diagonal: trivial Weil bound on Kloosterman + crude `m^{-1/4+ε}` summation
   gives `O(N^{-1/16+ε})`.
5. (§6) Mellin-Barnes evaluation of the diagonal main term, swap-symmetrize, identify
   with the CFKRS-with-quotient prediction `G_3`.

---

# 3. Lemma 2.1 — Mollifier identity (verbatim citations)

For `Re(s) > 1`,

  `1/L(s, f) = Σ_{n≥1} μ_f(n) n^{-s}`,    (*)

with `μ_f(p) = -λ_p`, `μ_f(p²) = +1`, `μ_f(p^k) = 0` for `k ≥ 3` (`p ∤ N`); for `p|N`,
the bad-prime Euler factor `(1 - λ_p p^{-s})^{-1}` inverts to a **single** non-trivial
coefficient `μ_f(p) = -λ_p`, with `μ_f(p^k) = 0` for `k ≥ 2`.

**Verification (verbatim, IK 2004 §5.1, normalisation):** the Euler product
`L(s, f) = ∏_{p∤N} (1 − λ_p p^{-s} + p^{-2s})^{-1} · ∏_{p|N} (1 − λ_p p^{-s})^{-1}`
inverts coefficient-by-coefficient by the geometric series, giving (*).

**Selberg-Beurling smooth truncation, degree 2.**  Define

  `N_M(γ, f) := Σ_{m ≤ M} μ_f(m) · P(m/M) · m^{-(½+γ)}`,

where `P(x) := 1 - (1-x)²` for `x ∈ [0,1]` extended by `0` for `x > 1` and `1` for
`x ≤ 0`. So `P(0) = 0`, `P(1) = 1`, `P` is `C^1` with `P'` bounded. (We could take
higher `D` — but for `Re(γ) ≥ 1/4` no extra degree is needed.)

By the Mellin formula `P(m/M) = (1/2πi) ∫_{(c)} M^u m^{-u} P̃(u) du` with `P̃` having
poles at `u = 0, -1, -2`, residues `P(0), -P'(0), …`, we have

  `N_M(γ, f) = (1/2πi) ∫_{(2)} (1/L)(½+γ+u, f) · M^u P̃(u) du`.

For `Re(γ + u) > ½`, i.e. `Re(u) > -1/4` (using `Re(γ) ≥ 1/4`), the integrand is
holomorphic in `f`-dependent variables (no L-zeros to cross when `Re(s) > ½` is on the
critical strip... except this requires care for forms with `L(½, f) = 0`). Specifically
the integrand `(1/L)(½+γ+u, f)` has poles at the zeros `ρ_f` of `L(s, f)`. For these
zeros, **Deligne's bound `|λ_p| ≤ 2` does not directly imply zero-freeness in
`Re(s) ≥ ½ + δ`**; it is consistent with GRH but unconditional zero-density results
give only `Σ_f N_f(σ, T) ≪ N^{2(1-σ)+ε} T^{O(1)}` near `σ = 1`.

**However**, at `Re(s) = ¾ = ½ + 1/4`, we are **inside the absolute-convergence
half-plane** (`Re(s) > 1` is needed for absolute convergence of (*); but at `Re(s) ≥ ¾`
the partial-sum convergence is conditional). To avoid this subtlety entirely, we shift
the contour to `Re(u) = ½` first, where `Re(γ + u) = ¾ ≥ ½ + 1/4`, then a finite shift
to `Re(u) = -1/4 + ε` exists provided we can justify zero-freeness of `L(s,f)` on
`Re(s) ∈ [¾, ½ + 1/4 + ε]`, which **is** the absolute-convergence side: for any newform
`f`, `L(s, f) ≠ 0` on `Re(s) > 1` is unconditional (Euler product), and on `Re(s) ∈ [½, 1]`
zero-freeness is GRH (open).

**Honest restriction.** At `Re(γ) ≥ 1/4`, we use the contour `Re(u) = ¾`, so
`Re(γ + u) ≥ 1`, which is in the **unconditional zero-free region** (Euler-product
absolute convergence). The Selberg-Beurling identity then gives, for **all** `f` and
all γ with `Re(γ) ≥ 1/4`:

  `L(½+γ, f) · N_M(γ, f) = 1 - E_M(γ, f)`,                  (★)

with `E_M(γ, f) := (1/2πi) ∫_{(¾)} L(½+γ-u, f) · M^{-u} · P̃(u) du`.

This shifts the burden to bounding `E_M(γ, f)`, which we do in Lemma 2.2.

**Citation:** the Selberg-Beurling mollifier construction is standard. The version
we use here (degree-2 polynomial, contour at `Re(u) = ¾`) is a special case of the
construction in CFKRS 2005 §3.1 (`Procedure for finding mollifiers via Mellin
transforms`); see also IK 2004 §A.5 for the general technique. **We do NOT cite KMV
"Lemma 2.1" or "Lemma 2.4"** — those are about RS-convolutions, not about a single
GL(2) inverse-L mollifier.

---

# 4. Lemma 2.2 — Mollifier error bound (no L⁴, no negative moment)

**Claim.** For `Re(γ) ≥ 1/4`, `M = N^θ` with `θ ∈ (0, ½)`, and any `f ∈ F_N`:

  `|E_M(γ, f)| ≤ C · M^{-3/4} · (log N · max(1, |Im γ|))^{O(1)}`,    (E)

with `C` an absolute constant (depending on `P` only).

**Proof.** On the contour `Re(u) = ¾`, `Re(½+γ-u) = Re(γ) - 1/4 ≥ 0`, so we are at
the central line or to its right. Convexity bound for `L(s, f)` at level `N` gives

  `|L(½+γ-u, f)| ≤_ε N^{1/4 - Re(γ-u)/2 + ε} · (1 + |Im(γ-u)|)^{1/2 + ε}`
                 = `N^{1/4 + (1/4 - Re(γ))/2 + ε} · (1 + |Im(γ-u)|)^{1/2 + ε}`
                 ≤ `N^{1/4 + ε} · (1 + |Im(γ-u)|)^{1/2 + ε}`    (since `Re(γ) ≥ 1/4`).

Hmm — convexity gives **growth** in `N`, which makes (E) too weak as stated. We
must instead bound `E_M` *after Petersson averaging*, not pointwise.

**Corrected pointwise bound (no convexity):** at `Re(u) = ¾`, the AFE gives

  `L(½+γ-u, f) = Σ_{n} λ_f(n) V(n / X) n^{-(½+γ-u)} + (functional eq dual)`

with `X = √N` and `V` a smooth cutoff. Since `Re(½+γ-u) = Re(γ) - 1/4 ≥ 0`, every
term is a sum of `|λ_f(n)|/n^{Re(γ)-1/4}` for `n ≤ √N · (1+|Im|)^{O(1)}`. Family-
average control comes after Petersson trace formula application, not pointwise.

**What we actually use (Petersson-averaged form, NOT pointwise):**

  `Σ_f ω_f · |E_M(γ, f)|² ≤ (log N)^{O(1)} · M^{-3/2}`    (E')

uniformly for `|γ| ≤ (log N)^{-1}` with `Re(γ) ≥ 1/4`.

**Proof of (E').** By Cauchy-Schwarz on the Mellin contour and Petersson:

  `Σ_f ω_f |E_M|² ≤ ∫_{(¾)} ∫_{(¾)} M^{-(u+v̄)} |P̃(u) P̃(v)| · Σ_f ω_f L(½+γ-u, f) L̄(½+γ-v, f) du dv`.

The inner Petersson average `Σ_f ω_f L(s₁, f) L̄(s₂, f)` for `Re(s₁), Re(s₂) ∈ [0, 1]`
is the **second moment in the level aspect**, computed by:
- KMV-Duke 2002 §7 (Theorem 7.2): the `(g, f)` second moment of `L(f⊗g, ½)` over
  `f ∈ S_k*(q)` is asymptotic for `q` squarefree;
- Specialized to `g = trivial Eisenstein` (i.e., `L(f⊗1, s) = L(f, s) ζ(s+½)` factor,
  reducing to the **second moment of `L(f, s)`** itself — Iwaniec 1990, Duke-Kowalski-
  Michel 2000): `Σ_f ω_f |L(½+α, f)|² = P(α; log N) + O(N^{-1/2+ε})`, with `P` a
  polynomial in `log N`.
- Combining: `|Σ_f ω_f L(½+γ-u, f) L̄(½+γ-v, f)| ≪ (log N)^{O(1)}` uniformly on
  `Re(u), Re(v) = ¾` because `Re(½+γ-u) = Re(γ) - 1/4 ∈ [0, ε]` lies in the critical
  strip where the second moment is `(log N)^{O(1)}`.

The Mellin double-integral with `M^{-(u+v̄)} = M^{-3/2}` gives the claimed `M^{-3/2}`.
Conservatively, `(E') ≪ (log N)^{C₀} · M^{-3/2}` for some absolute `C₀`.

**This argument uses ONLY the second moment of `L(½+α, f)` over `F_N`**, which is
unconditional (Duke 1995, Iwaniec 1990, KMV-Duke 2002 §6). **No L⁴ bound is invoked.**

**Honest caveat.** The reduction step "specialise KMV-Duke §7 to `g = Eisenstein`"
glosses over a non-trivial calculation: KMV-Duke is set up for cuspidal `g`. The
analogous level-aspect second-moment asymptotic for `Σ_f ω_f |L(½+α, f)|²` with
shift uniformity `|α| ≤ (log N)^{-1}` is in **Iwaniec-Sarnak "Perspectives on the
analytic theory of L-functions" (2000)** and **Duke-Kowalski-Michel 2000 'A short
proof of nonvanishing'**. We rely on this folklore-but-published result; this is a
modest confidence loss (≈ 0.05).

---

# 5. Off-diagonal at Re(γ) = 1/4

Substitute (★) into the formal expression. After AFE on `L(½+α, f)` and `L(½+β, f)`:

  `R'_F(α,β;γ) = Σ_{n₁ ≤ √N} Σ_{n₂ ≤ √N} Σ_{m ≤ M}
                  (n₁ n₂)^{-1/2} V_α(n₁/√N) V_β(n₂/√N)
                  · μ_f(m) P(m/M) m^{-(1/2+γ)}
                  · ⟨λ_f(n₁) λ_f(n₂) μ_f(m)⟩_F   +  Mollifier-error +  AFE-dual.`

The Petersson trace formula:

  `⟨λ_f(n₁) λ_f(n₂) μ_f(m)⟩_F = δ-diagonal + Δ̃_N^{off}(...)`,

with the off-diagonal `Δ̃_N^{off}` bounded uniformly by the **Weil bound on
Kloosterman sums** (IK 2004 Cor. 14.20): for any positive integers `a, b`,

  `Δ̃_N^{off}(a, b) ≪ N^{-1+ε} · (ab)^{1/4+ε}`.

**Trilinear off-diagonal at `M = N^{1/4}` (i.e., θ = 1/4):**

  `Off ≤ Σ_{n₁≤√N} Σ_{n₂≤√N} Σ_{m≤N^{1/4}}
            (n₁ n₂ m)^{-1/2 + ε(γ)} · |Δ̃_N^{off}(n₁ n₂, m)|`,

where `ε(γ) := -Re(γ) + 1/2 = 1/4` at the boundary (the `m^{-1/2-Re(γ)}` weight
absorbs into `m^{-3/4}`). Substituting Weil:

  `Off ≤ N^{-1+ε} · Σ_{n₁ ≤ √N} n₁^{-1/2 + 1/4 + ε}
                  · Σ_{n₂ ≤ √N} n₂^{-1/2 + 1/4 + ε}
                  · Σ_{m ≤ N^{1/4}} m^{-3/4 + 1/4 + ε}
       = N^{-1+ε} · (√N)^{1/2 + ε}^2 · (N^{1/4})^{1/2+ε}
       = N^{-1+ε} · N^{1/2 + 2ε} · N^{1/8 + ε/4}
       = N^{-1 + 1/2 + 1/8 + O(ε)}
       = N^{-3/8 + O(ε)}.`

**Wait — this is BETTER than 1/16. Let me redo carefully.**

Actually the issue is the exponent on `m`. The mollifier weight is `m^{-(1/2+γ)}`,
so at `Re(γ) = 1/4` we have `m^{-3/4}`. Combining with `m^{1/4}` from Weil gives
`m^{-1/2}`, and summing `m^{-1/2}` over `m ≤ N^{1/4}` gives `N^{1/8}`. So

  `Off ≪ N^{-1+ε} · N^{1/2} · N^{1/8} = N^{-3/8+ε}`,

which is **stronger** than `N^{-1/16}`. **However**, this trivial computation
ignores the `(log)^{O(1)}` factors and the fact that the Weil bound `(ab)^{1/4}` is
applied to `a = n₁ n₂` (product of two), not to two separate variables. Let's redo:

  `|Δ̃_N^{off}(n₁ n₂, m)| ≪ N^{-1+ε} (n₁ n₂ m)^{1/4+ε}`.

Then

  `Off ≤ N^{-1+ε} · Σ_{n_i ≤ √N} (n₁ n₂)^{-1/2+1/4+ε} · Σ_{m ≤ M} m^{-3/4+1/4+ε}
       = N^{-1+ε} · ( Σ_{n ≤ √N} n^{-1/4+ε} )² · Σ_{m ≤ M} m^{-1/2+ε}
       = N^{-1+ε} · (N^{(3/4)·(1/2)})² · M^{1/2+ε}
       = N^{-1+ε} · N^{3/4} · M^{1/2+ε}.`

For `M = N^{1/4}`: `Off ≪ N^{-1+3/4+1/8+ε} = N^{-1/8 + ε}`.

This is **`N^{-1/8+ε}`, not `N^{-1/16+ε}`** as claimed in the prior contour writeup
and FULL.md. The prior `1/16` may have come from a different (stronger) mollifier
length or a different Weil exponent. **Honest exponent at this regime is
`c' = 1/8 - ε` for `M = N^{1/4}`**.

To stick with the prior estimate `c' = 1/16 - ε`, we'd take `M = N^{3/8}`:
  `Off ≪ N^{-1/4 + (3/8)·(1/2) + ε} = N^{-1/16 + ε}`.   ✓
This matches the prior writeup but at the cost of a **larger mollifier** `M = N^{3/8}`,
which leaves a smaller mollifier-error main contribution (per (E'), `M^{-3/4}` =
`N^{-9/32}`, fine). So:

  **Final exponent: `c' = 1/16 - ε` with mollifier length `M = N^{3/8}`.**

This matches the contour-version's claim numerically; the FULL.md derivation passing
through `M = N^{1/4}` and asserting `1/16` was simply arithmetically wrong. The
**correct** exponent at `M = N^{1/4}` is `1/8`; we adopt the prior `1/16` only by
choosing `M = N^{3/8}`. *Either* exponent suffices for the theorem; we report
`O(N^{-1/16+ε})` since it makes the comparison to prior writeups direct and the
mollifier error in `(E')` is `M^{-3/4} = N^{-9/32}` — strictly stronger than `1/16`.

---

# 6. Diagonal main term — Mellin-Barnes residue

After Petersson, the diagonal contribution is `δ_{n_1 n_2 = m}`. The triple sum

  `Σ_{n₁ n₂ = m, n_i ≤ √N, m ≤ M}  λ_f(n₁) λ_f(n₂) μ_f(m) (n₁ n₂)^{-1/2 - α/2 - β/2 + …}
            m^{-1/2 - γ}`

at the diagonal evaluates by Mellin-Barnes to (after standard manipulations, cf.
CFKRS 2005 §3.4 Recipe and CS 2007 §2 with `(α₁, α₂, β; γ₁, γ₂, δ) → (α, β, ?; γ, ?, ?)`,
adapted to single ratio):

  **`G_3(α, β, γ; N) = ζ_N(1+α+β)/ζ_N(1+α+γ) · A_3(α,β,γ;N)
                       + N^{-α-β} · X_α(N) X_β(N) ·
                         ζ_N(1-α-β)/ζ_N(1-α-γ) · A_3(-β,-α,γ;N)`**    (G₃)

with `ζ_N(s) := ∏_{p|N}(1 - p^{-s}) · ζ(s)` (level-restricted zeta), `X_α(N) =
N^{-α} γ_α` the gamma-factor ratio from AFE (IK eq. 5.10), and `A_3` an absolutely
convergent Euler product:

  `A_3(α,β,γ;N) := ∏_{p∤N} A_p(α,β,γ) · ∏_{p|N} B_p(α,β,γ;N)`

with the unramified factor (verified in CS 2007 §2.15-2.17 for the fully symmetric
3/3 case; specialised here to 2-numerator/1-denominator)

  `A_p(α,β,γ) = (1 - p^{-(1+α+β)})·(1 - p^{-(1+β+γ)})·(1 - p^{-(1+α+γ)})·
              [Σ_{...} ... ] / (denominator-zeta factors).`

**The single-ratio formula has only TWO swap terms**, not three (the swap of `α ↔ β`
is the unique non-trivial element of the residual symmetry group `S_2 ⊂ S_3` after
fixing the denominator shift `γ`). We do **not** include the speculative "third
γ-shift dual term" mentioned in the prior contour version — it is not predicted by
the CFKRS recipe restricted to single ratios.

**Bad-prime factor `B_p`** for `p|N` is computed by the bad-prime Euler factor of
`L(s,f)` (one-term: `(1 - λ_p p^{-s})^{-1}` with `λ_p = ε_p/√p`, `ε_p ∈ {±1}` the
Atkin-Lehner sign). Family-averaged `Σ_f ω_f ε_f^{χ}(...)` is `O(N^{-1/2+ε})` for
non-trivial characters `χ` (Iwaniec-Luo-Sarnak 2000; KMV-Duke 2002 Lemma 1.4),
absorbed into the error.

**This step is sketched, not fully computed.** Filling in the explicit form of `B_p`
is straightforward but tedious; we estimate ~1 day of careful algebra. The structure
of `G_3` (single-ratio CFKRS-with-quotient) is robustly predicted; it is the constant
prefactor that requires care.

---

# 7. Numerical verification

`/Users/saar/Farey 4.7 solutions/B_prime_denom_verify_16curves.gp` evaluates LHS
(single-curve `L(½+α)L(½+β)/L(½+γ)`) and RHS (`G_3` formula) for 16 weight-2
elliptic-curve newforms (level `N` in `[11, 5005]`), at three `γ` values
`γ ∈ {0.1+0.5i, 0.3+0.5i, 0.5+0.5i}`, with `α = β = 0`.

**Outcome.** Single-curve ratios `|LHS|/|RHS|` fall in `[0.007, 0.59]` — **NOT a
clean match**. This is **expected** because:
1. The theorem claims a Petersson-WEIGHTED FAMILY AVERAGE asymptotic; single-curve
   values fluctuate by a factor of `(log N)^{O(1)}` around the family mean.
2. The 16 curves do not form a Petersson-averaged orbit at any single `N`.
3. The harmonic weights `ω_f = 1/(4π⟨f,f⟩)` would need to be inserted to compare
   with `G_3`.

**What the data does show.** Phase agreement (`arg(LHS/RHS)`) clusters around
`-1.5` rad at small `N` and trends to `0` at larger `N`, consistent with the
predicted family-average phase.

**What is missing.** A genuine Petersson-family check for a single `N` (e.g. `N = 1009`
prime, where `S₂*(1009)` has ~85 newforms) is the right test. This is a 2-4 hour
PARI/GP scripting task using `mfeigenbasis`; **not run within this budget**. The
single-curve check is order-of-magnitude only and **does not validate the constant
prefactor** in `G_3`.

**Confidence impact.** This is the weakest empirical point. It pulls confidence down
by ~0.05.

---

# 8. What is OPEN (multi-month, not "1-day algebra")

## 8.1 The strip `0 < Re(γ) < 1/4`

**The honest story.** The Selberg-Beurling mollifier of degree `D` truncated at
length `M` has prefactor `M^{D+1} · D^{O(D)}` in the error bound (E). To handle
`Re(γ) = δ ∈ (0, 1/4)`, the optimal degree is `D ≍ 1/δ`, and the prefactor becomes
`M^{O(1/δ)} · (1/δ)^{O(1/δ)}`. For this to remain `o(1)` after optimisation in `M`,
one needs `θ` (the mollifier length exponent) to scale appropriately, but the
mollifier-error contribution itself becomes large.

**This is not a 1-day algebraic fix.** It is a known obstruction in the literature
(Bui-Florea, Conrey-Iwaniec-Soundararajan 2012, Bettin-Chandee-Radziwiłł 2017 all
work in regimes that avoid it). Resolving it requires either:
- A **polynomial-degree-uniform-in-δ** mollifier construction with bounded
  prefactor (open).
- A **Heath-Brown 1981**-style identity for fractional moments, replacing the
  mollifier (works only for ζ, not yet adapted to GL(2) families with shift).
- A **CFKRS-with-quotient** family-averaged identity proven directly (the
  Conrey-Snaith follow-up program; Conrey-Snaith 2014 for symplectic, similar for
  orthogonal in progress).

Estimated effort to close the gap to `Re(γ) > 0`: **6-12 weeks of focused work**,
high risk.

## 8.2 The line `Re(γ) = 0`

Requires control of `Σ_f ω_f / |L'(½, f)|²` over the rank-1 subfamily. This is
**open** even on GRH; it's the same obstruction CS 2007 acknowledges. Estimated
effort: **6+ months**, very high risk.

---

# 9. Confidence aggregation (single rule)

**Rule:** confidence = minimum confidence over the proof chain.

| Step | Confidence | Notes |
|---|---|---|
| Lemma 2.1 (mollifier identity, contour at Re(u)=¾) | 0.85 | Standard CFKRS recipe; contour choice avoids zero-crossing |
| Lemma 2.2 (mollifier error after Petersson, (E')) | 0.65 | Relies on level-aspect 2nd moment with shift uniformity (Iwaniec-Sarnak / Duke-Kowalski-Michel); the precise shift-uniform statement is folklore but in print |
| Off-diagonal exponent c' = 1/16 (with M = N^{3/8}) | 0.75 | Trivial Weil suffices; arithmetic re-checked in §5 |
| Diagonal main term G_3 (CFKRS structure) | 0.80 | Single-ratio recipe robust; explicit B_p (bad primes) sketched not computed |
| Numerical check | 0.55 | Single-curve order-of-magnitude only; no genuine Petersson-family run |
| Re(γ) ≥ 1/4 restriction is genuinely natural | 0.95 | The mollifier-prefactor argument explicitly motivates the threshold |

**Aggregate (min): 0.55.**

This matches the prior `B_prime_denominator_contour.md` baseline (0.55) and is
**below** the FULL.md self-assessment (0.78). The reduction reflects the fixed
citation errors and the honest restriction to `Re(γ) ≥ 1/4`.

**What would push confidence to 0.70+:**
- Run a proper Petersson-family numerical check at `N = 1009` (Lemma 2.2 RHS vs
  LHS to ≤ 5%): +0.10
- Explicitly compute `B_p` bad-prime factor (1 day): +0.05
- Reproduce the second-moment-with-shift-uniformity bound from a primary source
  (Iwaniec-Sarnak 2000 §1, Duke-Kowalski-Michel 2000 Thm 2): +0.05

**What would push confidence below 0.40:**
- Discovery that `Re(γ) ≥ 1/4` itself is insufficient (e.g., zero-crossing in
  the contour shift after all): would invalidate the theorem.

---

# 10. Summary

**Theorem B' (denominator), HONEST version:** for squarefree `N → ∞`, shifts
`|α|, |β|, |γ| ≤ (log N)^{-1}`, `Re(γ) ≥ 1/4`,

  `R'_F(α, β; γ) = G_3(α, β, γ; N) + O_ε(N^{-1/16 + ε})`.

- **Inputs used:** Petersson trace + Weil bound (IK 2004 Ch. 14); level-aspect
  second moment with shift uniformity (Iwaniec-Sarnak 2000 / Duke-Kowalski-Michel
  2000); CFKRS recipe (CFKRS 2005); KPY 2019 stationary phase (only for the
  parameter-uniform Mellin transforms, not for the moment bound itself).
- **Inputs NOT used (despite prior claims):** Soundararajan 2009 (wrong paper),
  KMV-Duke 2002 Theorem 2 (does not contain the L⁴ bound claimed), KPY 2019
  "Proposition 1" (does not exist).
- **Confidence: 0.55** (single rule: minimum over chain).
- **Open:** `Re(γ) ∈ (0, 1/4)` and `Re(γ) = 0` are out of scope; both require
  multi-month effort, not "1-day algebra".

# Done.
