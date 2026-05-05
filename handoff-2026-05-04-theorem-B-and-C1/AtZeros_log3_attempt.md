---
title: "At-zeros (log)^3 attempt: converting Theorem B-weaker (Λ-form, central) to a sum-over-zeros L'-form"
type: original-research-attempt
domain: research
tier: working
confidence: 0.32
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (10h budget, central → at-zeros conversion attempt)
sources:
  - /Users/saar/Farey 4.7 solutions/Theorem_B_weaker_log3.md  (central-point Λ-form, 14/3 (log q̂)^3, UNCONDITIONAL)
  - /Users/saar/Farey 4.7 solutions/B3_Lprime_2nd_moment_RIGOROUS.md  (on-line (1/3)·T·log^3 c(T), unconditional; at-zeros 2/(3π)·T·log^4 disputed)
  - /Users/saar/Farey 4.7 solutions/G2_GRH_bypass.md  (audit: per-form M-N needs RHf via R1/R2/R3; family-averaged → cage only)
  - /Users/saar/Farey 4.7 solutions/Synthesis_Petersson_Voronoi_Selberg.md  (Identity (E); R3 reformulated as parabolic-residue obstruction)
  - /Users/saar/Farey 4.7 solutions/S4_KMV_Mellin_verify.md  (PARI 40-digit residue 7/3 L^3 + ...)
  - /tmp/milinovich_ng.txt  (M-N 2014, Conjecture (16): (2/(3π)) c_f T log^4 X with err O(T log^3 X))
  - "M-N Proposition 4.1 verbatim, /tmp/milinovich_ng.txt L2022, REQUIRES RHf"
  - KMV Crelle 526 (2000) §2 eq. (5)  [unconditional Λ-form (log q̂)^{2k+1}]
  - ILS Publ. IHES 91 (2000)  [sign distribution + zero density]
tags: [at-zeros, log3, theorem-B-weaker, riemann-von-mangoldt, plancherel, RHf-bypass, central-to-zeros, level-aspect, weight-aspect]
---

# Section 1 — Statement of the at-zeros (log)^3 target

## 1.1 The exact target the user proposed

$$
\sum_{f \in S_2^*(q)^h}\;\sum_{|\gamma_f|\le T} \big|L'(\tfrac12+i\gamma_f, f)\big|^{2}
\;=\; c''\,q^{a}\,T^{b}\,(\log NkT)^{3}\;+\;O\!\big((\log NkT)^{2}\big)
\tag{T0}
$$

with explicit `c'', a, b`, **unconditionally**.

(T0) as written has dimension issues: the LHS is summed over the level
family `S_2*(q)`, whose harmonic Petersson average is `Σ^h f ≈ q/(12π²)·(1+o(1))`
zero-density (KMV Crelle 2000 §2 line preceding (5)). Including the zero
sum of length `T·log(qT)/π`, the LHS scales like `q · T · (log)^?`. So
`a = 1, b = 1` are forced by Riemann-von Mangoldt + Petersson density;
the only nontrivial item is `(c'', power of log)`.

I will work with the **harmonic-weighted** version since this is what
KMV / Theorem B-weaker control:

$$
M^{\rm zeros}(q,T) \;:=\; \sum_{f \in S_2^*(q)}^{h}\;\sum_{|\gamma_f|\le T}
\big|L'(\tfrac12+i\gamma_f, f)\big|^{2},
\tag{T1}
$$

where `Σ^h α_f = Σ_{f \in S_2^*(q)} α_f / (4π⟨f,f⟩)`.

## 1.2 Two natural unconditional log-power targets

By analogy with the on-line / at-zeros Stieltjes split for ζ (Conrey
1989 *Crelle* 399), the at-zeros sum splits as

$$
\sum_\gamma |L'(\tfrac12+i\gamma_f,f)|^2
\;=\; \underbrace{\int_0^T |L'(\tfrac12+it,f)|^2\,\frac{dN_f}{dt}\,dt}_{\text{smooth (Riemann-von Mangoldt density)}}
\;+\;\underbrace{\int_0^T |L'(\tfrac12+it,f)|^2\,dS_f(t)}_{\text{fluctuating}}.
\tag{T2}
$$

The smooth term, using the unconditional Riemann-von Mangoldt density
`dN_f/dt = (1/π)·log(c(t)) + O(1)` with `c(t) = √q·k·t/(2π)` (Iwaniec-Kowalski Thm 5.8),
combined with the unconditional **on-line** moment
`⟨|L'(½+it,f)|²⟩^h_{S_2^*(q)} ~ ?·(log NkT)^β`, gives an unconditional asymptotic
of order `(log NkT)^{β+1}`.

So the natural unconditional at-zeros log-power is **one more than the
on-line log-power**. M-N predict `β = 3` for the on-line moment at
`s = ½+it` (cf. their Conjecture (16) with smooth-part + pair-corr both
giving the same `T log^4` order), making the at-zeros prediction `(log)^4`.

**The (log)^3 target the user requests is therefore NOT the natural
at-zeros analog of Theorem B-weaker.** The natural analog is `(log)^4`
(the full M-N prediction). The (log)^3 would arise either as:

- **(T1a)** the on-line analog `Σ^h ∫_0^T |L'(½+it,f)|^2 dt` — this is
  literally the on-line moment, NOT at-zeros, and is what B3 §6 derives
  unconditionally with constant `1/3`. This is well-trodden ground.

- **(T1b)** an at-zeros sum with constant **smaller** than the on-line
  by a factor of `log(NkT)`, i.e. arising from a *different smoothing* of
  the spectral measure. This would happen if the moment of `|L'(½+it,f)|²`
  averaged across zeros (rather than across height) was `(log NkT)^2`
  instead of `(log NkT)^3` (the on-line result). I show in §3 that this
  reduction does not hold unconditionally.

So the precise meaning of the user's (log)^3 target is **ambiguous**,
and I must treat both interpretations carefully.

---

# Section 2 — Five attack routes evaluated

## 2.1 Route 1 (Plancherel inversion on the Γ-function side)

**Claim.** ∫|L'(½+it,f)|² G(t) dt = Σ_γ |L'(½+iγ,f)|² + smooth, for an
appropriate "comb-smoother" Plancherel test function G.

**Reality check.** This is a *backwards* Plancherel: it says the integral
on the line equals the zero-sum plus a smooth piece. The standard
direction is Σ_γ g(γ) = ∫ g(t) (dN_f/dt) dt + ∫ g(t) dS_f(t) (Stieltjes
split). For Plancherel inversion to recover the discrete zero sum, G
must be a smooth "comb" with peaks at the γ_f — which IS the explicit
formula direction.

**Verdict on Route 1.** This is just the explicit formula in disguise.
The "smooth piece" is precisely `∫ g(t) (dN_f/dt) dt` and the "discrete
piece" is `∫ g(t) dS_f(t)`. Same as Route 4 below; not independent.

## 2.2 Route 2 (Explicit formula for Σ_γ g(γ_f))

**Setup.** The standard Weil/Guinand explicit formula for GL₂ newforms
(Iwaniec-Kowalski Thm 5.12):

$$
\sum_{\gamma_f}\,g(\gamma_f)
\;=\; \tfrac{1}{2\pi}\int_{-\infty}^{\infty} g(t)\Big[\tfrac{\Gamma'}{\Gamma}(\tfrac12+it+\tfrac{k-1}{2})
+\log q + \log(2\pi)^{-1}\Big]dt
\;-\; \sum_{n=1}^{\infty}\,\tfrac{\Lambda_f(n)}{\sqrt n}\,\hat g(\tfrac{\log n}{2\pi})\;-\;(\text{trivial-zero contrib}),
\tag{EF}
$$

where `Λ_f(n) = a_f(n) Λ(n)` (sparse, supported on prime powers) and
`ĝ(u) = ∫ g(t) e(-tu) dt`.

**Plug in `g(γ) = |L'(½+iγ_f, f)|²`.** The Fourier transform `ĝ` is the
*autocorrelation* of `Ĺ(½+it,f)` in the t-variable, which itself is a
sum of weighted prime powers. So the prime-side becomes a quadruple sum
of `Λ_f(n)·Λ_f(m)` weighted by autocorrelation kernels.

**Status (UNCONDITIONAL via large sieve?).** A large-sieve bound for the
prime-side gives only `O(q · (log)^?)`, where the `?` exponent depends on
how many `Λ_f(p)` factors are integrated. By Deligne `|Λ_f(p)| ≤ 2 log p`
unconditionally for p ∤ q, so the prime side is bounded by

$$
\sum_n \tfrac{|Λ_f(n)|}{\sqrt n} |\hat g| \le \sum_p \tfrac{2\log p}{\sqrt p}|\hat g(\log p / (2π))|
$$

For `g(γ) = |L'(½+iγ,f)|²`, `ĝ` is a 4th-power-like prime-correlation,
and bounding it requires control of the **4th moment of L on the line**,
which is conditional on Lindelöf/GRH for individual f.

Family-averaged via Petersson with Bessel decay (k > 4eT/√N) the
off-diagonal vanishes — but the explicit-formula manipulation here is
**per-form** before averaging. The Petersson average is applied to
`Σ_γ_f g(γ_f)` not to `g`, and inside the explicit formula `g`'s prime
expansion uses individual Λ_f(p), so the average is on `λ_f(p)·λ_f(q)`
which IS handled by Petersson trace formula.

**Crucial issue (R3 in disguise).** The explicit formula (EF) holds for
a test function `g` which is `g(γ_f) = |L'(½+iγ_f,f)|²` — but this is
defined ONLY at the zeros γ_f. To extend to a test function on R (so
that the Mellin/Fourier machinery applies), one writes
`g(t) := |L'(½+it,f)|²` on the entire line, and uses the explicit
formula's `Σ_γ_f g(γ_f) = (smooth) - (prime-side)`.

This is *fine unconditionally* — no RHf needed for the explicit formula
itself. The issue is bounding the prime-side. The 4th-moment-on-line
input needed is

$$
\int_0^T |L(\tfrac12 + it, f)|^4\,dt = O(T (\log T)^4)\quad\text{unconditionally per form?}
$$

This is the **classical 4th moment bound** for individual GL₂ L-functions
on the central line. Status:
- For individual f, the **subconvexity** bound from Good 1982 gives
  `∫_0^T |L(½+it,f)|² dt ≪ T·log T`, which is the "second-moment"
  unconditional; this is `(log)^1` per unit T.
- The 4th moment for individual f at central line is **open
  unconditionally** (it would imply Lindelöf-on-average); known partial
  results give `O(T·(log)^?)` only on-average (over twists, levels,
  etc.).

**Route 2 verdict.** The explicit formula (EF) is unconditional. Bounding
the prime-side `Σ Λ_f Λ_f / √(mn) · autocorrelation kernel` requires
either: (a) per-form 4th moment bound (open), or (b) a family-averaged
4th moment, which exists (KMV Invent. 2000 Cor. 1.3 *for L not L'*; the
L'-version requires extra log-factor input). The per-form route fails;
the family-averaged route is *route 4 below* in different clothing.

## 2.3 Route 3 (KMV-style Mellin direct at zeros)

**Setup.** Repeat KMV Crelle 2000 §2 eq. (5)'s Mellin variance
computation but with `Λ'` evaluated at zeros `ρ_f = ½+iγ_f` instead of at
the central point `½`.

**Crucial observation.** KMV's Mellin computation
`Σ^h |Λ^{(k)}(f, ½)|² ~ c'_k (log q̂)^{2k+1}` (S4_KMV_Mellin_verify.md PARI
40-digit verified, k=1: 14/3 (log q̂)^3) USES the AFE expansion at the
*single point* s = ½, then squares, then applies Petersson to the
diagonal m=n piece. The Mellin contour is opened at `s = ½` and shifted
to compute the residue at t=0.

To repeat at zeros: we need to compute `Σ_γ |Λ'(ρ_f,f)|²` where
`Λ'(ρ_f,f) = q̂^{ρ_f}·Γ(ρ_f+½)·L'(ρ_f,f)` (since at zeros `L(ρ_f,f) = 0`,
the first term vanishes). At `ρ_f = ½+iγ_f`:

$$
|\Lambda'(\rho_f, f)|^2 = \hat q\cdot |\Gamma(1+i\gamma_f)|^2\cdot |L'(\tfrac12+i\gamma_f, f)|^2.
\tag{Λ-zero}
$$

Note `|Γ(1+iγ)|² = πγ/sinh(πγ)` (reflection formula), which **decays
exponentially** as |γ| → ∞ (≈ 2π|γ|·e^{-π|γ|}). So summing
`|Λ'(ρ_f,f)|²` over ALL zeros γ_f gives an absolutely convergent sum
whose mass is concentrated near γ = 0.

**This means.** The at-zeros sum `Σ_γ |Λ'(ρ_f,f)|²` (no T-cutoff) is
**bounded** by the central-point value times an explicit constant from
the integral `∫₀^∞ (πx/sinh(πx))·(some density) dx`; it is NOT a
height-T-growing quantity. The Λ-form at zeros has fundamentally
different scaling than the L-form at zeros.

**Verdict on Route 3.** Going via the Λ-form at zeros gives a *different
object* than the user's L'-target. The exponential `Γ(1+iγ)` damping
kills the height-T linear growth. The Λ-form is **not** the right
object to convert via this route.

## 2.4 Route 4 (Riemann-von Mangoldt + average value)

**Setup.** By GL₂ Riemann-von Mangoldt (Iwaniec-Kowalski Thm 5.8):

$$
N_f(T) := \#\{\gamma_f : 0 < \gamma_f \le T\} = \tfrac{T}{\pi}\log\tfrac{kT\sqrt q}{2\pi e} + O(\log(qT)),
\tag{RvM}
$$

unconditionally for individual f. So `dN_f/dt = (1/π)·log(c(t))·(1+O(1/log))`
with `c(t) := √q·k·t/(2π)` the analytic conductor.

**Stieltjes split (T2):**

$$
\Sigma^h\sum_{0<\gamma_f\le T}|L'(\tfrac12+i\gamma_f,f)|^2
\;=\; \underbrace{\Sigma^h\int_0^T |L'(\tfrac12+it,f)|^2\,\frac{dN_f}{dt}dt}_{:= \mathrm{Smooth}}
\;+\;\underbrace{\Sigma^h\int_0^T |L'(\tfrac12+it,f)|^2\,dS_f(t)}_{:= \mathrm{Fluct}}
$$

**Smooth term.** Substituting `dN_f/dt = (1/π)log c(t)`:

$$
\mathrm{Smooth} = \tfrac{1}{\pi}\,\Sigma^h\int_0^T |L'(\tfrac12+it,f)|^2 \log c(t)\,dt
\;\sim\; \tfrac{\log c(T)}{\pi}\,\Sigma^h\int_0^T |L'(\tfrac12+it,f)|^2\,dt + (\text{lower})
$$

(the slow variation of log c(t) over [0,T] is absorbed into a lower order)

The **central-line analog** of B3's on-line moment `⟨∫|L'(1+it,f)|²⟩`
(which was at `Re s = 1`!) at the **central line `Re s = ½`** is what
we need. KMV Crelle 2000 §2 eq. (5) for **k = 0**:

> `Σ^h |L(f, ½)|² ~ c'_0 (log q̂)`,  i.e. `c'_0 (log NkT)`

is the central-point 2nd moment of L (not L'). For L' we want:

$$
\Sigma^h\,|L'(\tfrac12+it, f)|^2 \;\stackrel{?}{=}\; D_2(t)\cdot(\log c(t))^?
\tag{D2}
$$

**This is where the (log)^3 question becomes precise.** Recall:
- KMV (5) gives `Σ^h |Λ^{(1)}(f,½)|² ~ 14/3 (log q̂)^3` at the **central
  point** (a one-point statement, no t-integration).
- Translated to L': for the odd subfamily where L(½,f)=0 so
  `Λ'(½,f) = q̂^{1/2} L'(½,f)`, we get `Σ^h_{S_2*(q)^-} |L'(½,f)|² ~
  A^- (log q̂)^3` (Theorem B-weaker odd L'-form, Theorem_B_weaker_log3.md).

**The central-point value `Σ^h |L'(½,f)|²`** has order `(log q̂)^3`.
Differentiating in `t` at fixed q (using the AFE-to-line method of B3 §3):

$$
\Sigma^h\,|L'(\tfrac12+it, f)|^2 \;\sim\; D_2 \cdot \log^3 c(t)
\quad (?!)
\tag{2.4★}
$$

**Open question.** Is (2.4★) the unconditional value at fixed t? OR is
the on-line value lower order, with the central-point being a *peak*?

**This is where the analysis fails for unconditional (log)^3 at zeros.**
The on-line moment `Σ^h |L'(½+it,f)|²` is, on average over t, expected
to be `D_2 · log^3 c(t)` — but this is a **conjectural** statement
matching the central-point case. KMV Crelle 2000 only computes the
central point; KMV Invent. 142 only computes the L (not L') on-line
4th moment at level aspect, which is not what we need.

**The crucial barrier.** To use Route 4, we need the **on-line 2nd
moment of L' at the central line**, family-averaged. This is **NOT** in
KMV. It is the analog of Hughes-Young 2010 *for ζ at the line* but for
GL₂ at the central line, and it is **open** unconditionally.

If we accept the conjectural value `D_2 · log^3 c(t)` for the on-line
moment, then:

$$
\mathrm{Smooth} \;=\; \tfrac{1}{\pi}\cdot D_2\cdot \int_0^T \log^4 c(t)\,dt \;\sim\; \tfrac{D_2}{\pi}\,T\,\log^4(NkT).
$$

This gives **(log)^4 for the smooth term**, NOT (log)^3.

If instead the on-line moment at fixed t is `(log c(t))^2` (one less
than the central-point value), then Smooth gives `(log)^3`. But there
is no reason to expect this drop.

**Verdict on Route 4.** The Riemann-von Mangoldt + on-line moment route
gives **either (log)^4 (matching M-N's conjecture) or (log)^3 if the
on-line moment unexpectedly drops one log-factor**. In either case, the
on-line input is not unconditionally available at the central line for
GL₂ in the level aspect.

## 2.5 Route 5 (Substitute Λ → L direct at zeros)

**Computed in §1 above (Λ-zero relation).** At ρ_f = ½+iγ_f:

$$
|\Lambda'(\rho_f,f)|^2 = \hat q \cdot |\Gamma(1+i\gamma_f)|^2 \cdot |L'(\tfrac12+i\gamma_f, f)|^2.
$$

So
$$
\Sigma^h\sum_\gamma|L'(\tfrac12+i\gamma_f,f)|^2
\;=\; \tfrac{1}{\hat q}\,\Sigma^h\sum_\gamma\frac{|\Lambda'(\rho_f,f)|^2}{|\Gamma(1+i\gamma_f)|^2}.
\tag{ΛL}
$$

Using `|Γ(1+iγ)|² = πγ/sinh(πγ)`:

$$
\Sigma^h\sum_\gamma|L'(\tfrac12+i\gamma_f,f)|^2 \;=\;\tfrac{1}{\pi\hat q}\,\Sigma^h\sum_\gamma \frac{\sinh(\pi\gamma_f)}{|\gamma_f|}\,|\Lambda'(\rho_f,f)|^2.
\tag{ΛL2}
$$

**Critical issue (R3 reappears).** The denominator `1/|Γ(1+iγ_f)|²
= sinh(π|γ|)/(π|γ|)` *grows exponentially* in |γ|. Multiplied by
`|Λ'(ρ_f,f)|²`, which itself is a *zero-evaluated* completed L'-derivative
at on-line zeros (β_f = 1/2, γ_f real) — this is exactly where
**we use RHf**: only on RH does `ρ_f = ½+iγ_f` with γ_f real, making
`|Γ(1+iγ_f)|² = πγ_f/sinh(πγ_f)` real and exponentially small.

Off RHf, the zeros have `ρ_f = β_f + iγ_f` with β_f ∈ [0,1]; the
gamma-factor `Γ(ρ_f + ½)` is complex with phase, and the relation (ΛL)
becomes:

$$
|\Lambda'(\rho_f,f)|^2 = \hat q^{2β_f}\cdot|\Gamma(β_f+1/2+i\gamma_f)|^2\cdot|L'(\rho_f,f)|^2,
$$

introducing a `q̂^{2β_f-1}` factor that is **not** uniformly equal to 1
unless β_f = 1/2 (= RHf).

**This is the R3 obstruction** identified in G2_GRH_bypass.md §1.2.

**However**, KMV's central-point Λ-form result `Σ^h |Λ'(f,½)|² ~ 14/3 q̂(log q̂)^3`
is at a **single point s = ½**, not at zeros. The conversion to at-zeros
requires either:
(i) Per-form RHf to get `ρ_f = ½ + iγ_f` so that the conversion (ΛL) is
clean and Γ-factors are bounded — works for individual f under RHf;
(ii) An identity bridging the Λ-form at central point to a Λ-form
summed over zeros — but the central-point Λ-form is a single scalar,
while the at-zeros Λ-form is a sum, so they are *not directly related*.

**Verdict on Route 5.** The Λ→L conversion at zeros INTRODUCES the R3
obstruction (the gamma-factor at ρ_f). It does NOT bypass it. R5 is the
*motivation* for the user's question, but the conversion fails
unconditionally because the Γ-factor at off-line zeros is not under control.

## 2.6 Route comparison summary

| Route | What it offers | Unconditional? | Gives (log)^3 at zeros? |
|---|---|---|---|
| 1 (Plancherel) | Same as explicit formula | yes for the identity | NO — gives (log)^4 smooth |
| 2 (Explicit formula) | Prime-side bounds | conditional on per-form 4th moment | NO unconditional |
| 3 (KMV at zeros direct) | Mellin shift to zero set | yes for stmt | NO — Λ-form has different scaling |
| 4 (RvM + on-line moment) | Cleanest split | requires on-line 2nd moment of L' on line | (log)^4, not (log)^3 |
| 5 (Λ → L direct) | Bridge to Theorem B-weaker | NO — re-invokes R3 | NO unconditional |

**No route delivers an unconditional (log)^3 at-zeros result.** All
five routes either:
- give (log)^4 (matching M-N's conjecture, but conditional);
- re-invoke R3 (per-form RHf or family-averaged ratios);
- give a different object (Λ-form bounded; not height-growing).

---

# Section 3 — Best route — full derivation under (necessary) conditional inputs

The cleanest route is **Route 4 (RvM + Smooth/Fluct split) under the
conditional input "central-line on-line moment of L'"**. Let me write
out what (Smooth) gives unconditionally and what (Fluct) costs.

## 3.1 Stieltjes split, unconditional via RvM

By Riemann-von Mangoldt (RvM):

$$
\Sigma^h\sum_{|\gamma_f|\le T}|L'(\tfrac12+i\gamma_f,f)|^2
= \mathrm{Sm} + \mathrm{Fl}
\tag{Stieltjes}
$$

with
- `Sm = (1/π) Σ^h ∫_0^T |L'(½+it,f)|² log c(t) dt` (smooth),
- `Fl = Σ^h ∫_0^T |L'(½+it,f)|² dS_f(t)` (fluctuating, `S_f` Selberg).

This split is **identically true** as a Stieltjes integral identity — no
hypothesis used.

## 3.2 The on-line input — what's needed

The on-line moment `M_{on}(t) := Σ^h |L'(½+it,f)|²` is needed at fixed t.

**Known unconditional inputs:**
- KMV Crelle 2000 §2 eq. (5) at k=1: `Σ^h |Λ'(f,½)|² ~ 14/3 q̂ (log q̂)^3`.
  This pins `M_{on}(0)` (the central-point value) for the Λ-form. Translated
  to L' on the odd subfamily: `Σ^h_{S_2^*(q)^-} |L'(½,f)|² ~ A^- (log q̂)^3`.
- For `t ≠ 0`, this is `Σ^h |L'(½+it, f)|²`. The shift `t ≠ 0` moves
  the AFE truncation point but does not change the Mellin diagonal
  computation's leading log-power (which depends on the joint Mellin
  variable, not on t directly). KMV's argument extends with t-dependent
  logs of the analytic conductor `c(t) ≈ q̂·(1+t²)^{1/2}`:

$$
M_{on}(t) \;=\; A_{on}\cdot \log^3 c(t)\,(1+o(1))\quad\text{as } q\to\infty,
\tag{Mon}
$$

with `A_{on} = 14/3` for the Λ-form (translated). This translation is
**plausible but not in the literature**; it requires repeating the KMV
Mellin computation at off-central s = ½+it. The computation is straightforward
in principle (the Mellin integrand picks up `q̂^{2it}` and Γ(1+t)Γ(1+t̄)
phase factors), but I have not done it here.

**Conditional acceptance of (Mon).** Under (Mon) — a plausible
generalization of KMV Crelle 2000 (5) to off-central s — the smooth
piece becomes:

$$
\mathrm{Sm} \;=\; \tfrac{A_{on}}{\pi}\int_0^T \log^4 c(t)\,dt\,(1+o(1))
\;\sim\; \tfrac{A_{on}}{\pi}\cdot T\cdot\log^4(NkT).
$$

**Smooth gives (log)^4, not (log)^3.**

## 3.3 The Fluctuating piece — the key obstruction

`Fl = Σ^h ∫ |L'(½+it,f)|² dS_f(t)` is bounded by Cauchy-Schwarz:

$$
|Fl|^2 \le \Sigma^h\int_0^T S_f(t)^2 dt \cdot \Sigma^h \int_0^T|L'L''|^2(\tfrac12+it,f)\,dt.
$$

- **First factor (S_f² 2nd moment):** unconditionally `S_f² ≪ (log T)²·(log log T)²`
  (M-N Lemma 3.2 unconditional remark, /tmp/milinovich_ng.txt L1153). So
  `∫ S_f² dt ≪ T(log T)²(log log T)²`.
- **Second factor (4th-power-on-line moment of L'):** for individual f
  unconditional at central line is **open**. Family-averaged via Petersson
  (KMV Invent. 142 is for L not L'): not directly available; would require
  an *extension* of KMV Invent. 142 to L'. This extension is plausible
  via Mellin-Barnes contour shifts, but I have not verified.

**Conditional acceptance.** Under the family-averaged 4th-moment-of-L'
input (analog of KMV Invent. 142 Cor. 1.3 for L'), we get
`Σ^h ∫|L'L''|² ≪ T·(log T)^A · q̂` for explicit A ≈ 6.

Then `|Fl| ≪ T^{1/2}·(log T)·(log log T) · √(T·(log T)^A·q̂) =
T·(log T)^{(A+2)/2}·(log log T)·√q̂`.

**This is dominant over Sm when A ≥ 4.** I.e. the Cauchy-Schwarz upper
bound on Fluct is *not* sharp enough to extract a smaller-than-(log)^4
asymptotic. The fluctuation contribution would need to be evaluated
*signed*, not bounded, to get a sub-(log)^4 statement — and signed
evaluation of Fl is precisely the **pair-correlation kernel evaluation**,
which is RHf-conditional or Ratios-conditional (B3 §7, Synthesis_PVS §6.5).

## 3.4 Conclusion of Section 3

Even granting both:
- (Mon) the on-line 2nd-moment-of-L' at central line (translation of
  KMV Crelle 2000 (5) to off-central s);
- the family-averaged 4th-moment-of-L' on the central line (extension of
  KMV Invent. 142 to L');

the cleanest output is `(log NkT)^4`, **matching M-N's prediction at the
SAME log-power**. The (log)^3 target the user requested is **NOT
achievable as the natural smooth-piece of the Stieltjes split** — that
piece gives (log)^4.

The (log)^3 arises only if Fl = -(log)^4 to within (log)^3 of
the Sm value, i.e. the fluctuating piece nearly cancels the smooth.
This is the **pair-correlation-suppression** scenario, which is RHf or
Ratios.

---

# Section 4 — Does R3 obstruction reappear at (log)^3 level?

## 4.1 R3 verbatim from G2

From G2_GRH_bypass.md §1.2 (R3):

> **(R3) Functional-equation symmetry ρ_f = 1−\overline{ρ_f}.** Multiple
> later passes (line 2884, line 3268) write 1 − ρ_f = \overline{ρ_f},
> which holds **only if** β_f = 1/2 for every zero. This is RHf at its
> barest.

R3 is invoked in M-N's contour computation when |L'(ρ_f,f)|² is identified
with |L'(½+iγ_f,f)|² via β_f = 1/2.

## 4.2 R3 analysis at the (log)^3 level

**Question:** does R3 trigger at (log)^3?

The R3 obstruction has **three distinct uses** in M-N (G2 §1.2):

(R3a) Identifying ρ_f with ½+iγ_f for the modulus computation;
(R3b) Pairing |A(ρ_f)|² with the contour orientation in the explicit-formula step;
(R3c) Symmetry under s ↔ 1−s in the Mellin shift.

**For an unconditional (log)^3 result via Route 4:**
- The Smooth piece uses the on-line moment `Σ^h |L'(½+it,f)|²` —
  this is at the *real line t*, not at zeros. **No R3 needed.** The
  (log)^4 from Sm is unconditional given the on-line moment.
- The Fluct piece uses S_f (Selberg's S function) which is bounded
  unconditionally. **No R3 needed for the Cauchy-Schwarz upper bound.**

**Crucial observation.** R3 is needed to **identify the discrete sum
Σ_γ|L'(ρ_f,f)|² with the contour-integral output of M-N's Prop 4.1**,
i.e. for the **per-form** sharp constant. For the family-averaged unconditional
Smooth + Fluct split (Route 4), R3 is needed at the level of
*identifying* the LHS as a meaningful object — but on the LHS we are
*defining* the sum over zeros directly, not computing it via contour.

So **R3 does NOT directly obstruct the (log)^4 unconditional smooth-piece
asymptotic** if we're willing to accept the on-line moment input.

## 4.3 Where R3 reappears: in the on-line moment input

The unconditional inputs needed for the smooth piece are:
(i) RvM zero density (unconditional, IK Thm 5.8);
(ii) On-line 2nd moment of L' at central line, family-averaged, level aspect.

For (ii), the natural derivation is via AFE squared at s = ½+it +
Petersson trace formula (KMV Crelle 2000 method). The KMV result IS at
the central point s = ½. Extending to all t requires:
- Squaring AFE at s = ½+it (straightforward; the AFE at the central
  line is symmetric in s ↔ 1−s on the central line itself, but t-dependent
  Γ-factors enter);
- Off-diagonal Petersson via Bessel/Kloosterman bound (Deshouillers-Iwaniec
  spectral large sieve, unconditional for the level aspect at fixed q);
- Diagonal Mellin computation at off-central s = ½+it.

**R3 is NOT directly invoked in this chain** — the chain operates on the
critical line, not on zeros. The Γ-factor-at-zero issue (Route 5) does
not arise.

**However**, the *interpretation* of the resulting at-zeros sum
`Σ_γ |L'(½+iγ_f,f)|²` AS having β_f = 1/2 (so that the γ_f are real
and the L'(½+iγ_f) values are real-line-valued) **DOES** invoke R3.
Off RHf, the zeros are at ρ_f = β_f + iγ_f with β_f ∈ [0,1], and
`|L'(ρ_f,f)|²` is evaluated at off-line points where the on-line moment
input does not apply.

**The Stieltjes split (Stieltjes) becomes:**

$$
\Sigma^h \sum_{|γ_f|\le T} |L'(\rho_f,f)|^2
= \Sigma^h \int_0^T |L'(\beta_f+it,f)|^2\,dN_f(\beta_f, t)
$$

where `dN_f(β,t)` is the joint distribution of zeros in the (β,γ) plane.
Without RHf, `β_f ≠ 1/2` and the integrand is at off-line points.

**Family-averaged via Kowalski-Michel 1997 zero-density** (G2 §2.3):
`Σ^h_F N_f(σ,T) ≪ (NkT)^{-c(σ-1/2)}` for c < 1/8. So zeros with
`β_f > 1/2 + δ` contribute at most `(NkT)^{-cδ}` of the total.
Choosing `δ = 1/log(NkT)`, off-line contribution is bounded by
`(NkT)^{-c/log(NkT)} ≈ 1 - c·log log(NkT)/log(NkT)`, i.e. negligible
multiplicatively but not absolutely.

For a (log)^3-level statement, we need the off-line contribution to be
`O((log NkT)^2 · q̂T)` after multiplication. From the family-averaged
density, the on-line contribution dominates by a factor `(NkT)^{c/log(NkT)} - 1
≈ c/log(NkT)`, giving multiplicative error `1 + O(1/log(NkT))`. This is
**SMALLER than (log)^3 / (log)^4 = 1/log(NkT)**, so the off-line
contribution **does NOT obstruct a (log)^3 vs. (log)^4 distinction**.

**Verdict on R3 at (log)^3.** The (log)^3 vs (log)^4 distinction is
*not* directly affected by R3 at the family-averaged level — both
statements use the same RvM + on-line moment inputs, with the same
off-line zero correction. R3 affects **per-form sharp constants** (the
2/(3π) vs. cage), not the **leading log-power**.

**HOWEVER**, R3 affects which constant `c''` appears in front of the
(log)^3 (or (log)^4). Without the pair-correlation suppression (RHf or
Ratios), the smooth piece dominates, giving (log)^4 with constant
`14/3 / π ≈ 1.486` (modulo the off-central translation issue).

## 4.4 The critical question: where does (log)^3 come from?

If Sm gives (log)^4 unconditionally (Section 3), then the only way to get
(log)^3 is via **cancellation** of (log)^4 between Sm and Fl. This
cancellation is the *pair-correlation kernel zero* at the orthogonal
1-level density's 0-mode, which is itself **RHf or Ratios-conditional**.

**Therefore, an unconditional (log)^3 at-zeros result REQUIRES** either:
- The on-line moment to be (log)^2 instead of (log)^3 (which would
  contradict the central-point KMV (5));
- OR a structural reason for Sm + Fl to cancel at (log)^4 level
  unconditionally — which is RHf-equivalent.

**Verdict.** R3 reappears at the (log)^3 level **disguised as the
pair-correlation cancellation requirement**. The (log)^3 unconditional
at-zeros target is **not** distinct from the (log)^4 unconditional
target plus a (log)^4-suppression mechanism, which is exactly the same
obstruction G2/Synthesis_PVS identified.

---

# Section 5 — If not: full unconditional at-zeros (log)^3 theorem

NOT APPLICABLE. R3 reappears (Section 4). No unconditional (log)^3
at-zeros theorem of the requested form is achievable via the routes
considered.

The closest unconditional statement is the *Smooth-piece-only* result:

**Theorem 5.1 (conditional).** Under the on-line input (Mon), the smooth
piece of the at-zeros 2nd moment is

$$
\mathrm{Sm}^{(q)}(T) := \tfrac{1}{\pi}\Sigma^h\int_0^T|L'(\tfrac12+it,f)|^2\log c(t)\,dt
\;\sim\; \tfrac{14/3}{\pi}\,T\,\log^4(NkT)\,(1+o(1)).
$$

Note this is **(log)^4 not (log)^3** — and the constant `14/(3π)` is
about `1.486`, not `2/(3π) ≈ 0.212` (M-N's conjectural at-zeros constant).
The factor-7 discrepancy reflects that this is the SMOOTH piece only,
without pair-correlation suppression.

---

# Section 6 — If yes: identify the gap, fall back to central-point

R3 reappears (Section 4 verdict). Falling back:

## 6.1 What survives unconditionally at (log)^3

**Theorem 6.1 (unconditional, Λ-form, central point).** From
Theorem_B_weaker_log3.md:

$$
\Sigma^h\,|\Lambda'(f, \tfrac12)|^2 = \tfrac{14}{3}\hat q(\log\hat q)^3 + O(\hat q(\log\hat q)^2).
$$

This is **central-point** (no zero sum, no T height). It IS at (log)^3
unconditionally. Theorem B-weaker.

**Theorem 6.2 (conditional on on-line moment, smooth piece).** The
smooth piece of the at-zeros sum is `(14/3π)·T·log^4(NkT)`. NOT (log)^3.

**Theorem 6.3 (B3, weight aspect, on-line, unconditional).** B3_Lprime_2nd_moment_RIGOROUS.md
gives `⟨∫|L'(1+it,f)|²⟩_{F_k} ~ (1/3)T·log^3 c(T)` UNCONDITIONALLY at
the line `Re s = 1` in the **weight aspect**. This **IS** (log)^3,
unconditional. But it's at `s = 1`, NOT at zeros.

## 6.2 The honest verdict

The user's at-zeros (log)^3 target does NOT have an unconditional
proof via the routes considered. The closest unconditional statements
are:
- (a) Theorem B-weaker Λ-form at central point, (log q̂)^3 — proven.
- (b) B3 on-line 2nd moment of L' at Re s = 1, weight aspect, (log)^3
  — proven (modulo the C1-C4 caveats in B3).

Neither is at zeros. The conversion central-point → at-zeros introduces
the (log)^4 smooth piece (Section 3), and the (log)^3 result requires
unconditional cancellation = R3 in disguise (Section 4).

## 6.3 Why it is NOT a straightforward conversion

The user's question implicitly assumed the conversion is "free" — that
if (log)^3 holds at central point, it holds at zeros with extra factors
of T. This is **wrong** because:

1. The central-point (log)^3 measures variance in the f-direction
   (level family). The at-zeros sum measures both variance in f AND
   density-of-zeros (RvM gives an extra log per unit T).

2. The Stieltjes density `dN_f/dt` carries one log; multiplied by the
   on-line moment `(log)^?`, the natural at-zeros log-power is `1 + (on-line)`.

3. The on-line moment at central line `Re s = ½` is conjecturally
   `(log)^3` (matching central point), giving at-zeros `(log)^4`.

4. The (log)^3 at-zeros would require on-line `(log)^2`, contradicting
   the central-point computation. So the (log)^3 at-zeros result is
   *false* unconditionally.

---

# Section 7 — Honest verdict + confidence

## 7.1 The verdict

**The unconditional at-zeros (log)^3 theorem proposed by the user
DOES NOT EXIST.** The natural at-zeros log-power is **(log)^4**:

- Smooth-piece (RvM density × on-line moment) gives (log)^4.
- Fluctuating-piece pair-correlation cancellation could reduce this,
  but only RHf-conditionally (or Ratios-conditionally).
- The (log)^3 power would require on-line moment to be (log)^2,
  which contradicts KMV Crelle 2000 (5)'s central-point (log)^3.

**The five attack routes were each examined:**

| Route | Verdict |
|---|---|
| 1. Plancherel inversion | = explicit formula in disguise; unconditional only as identity |
| 2. Explicit formula | needs per-form 4th moment on line (open) or family 4th moment of L' (open) |
| 3. KMV at zeros direct | Λ-form at zeros has Γ-decay; bounded, not height-T-growing |
| 4. RvM + on-line moment | smooth gives (log)^4 conditionally; fluct CS bound dominates |
| 5. Λ → L direct | re-invokes R3 at the Γ-factor-at-zero step |

**No route produces unconditional (log)^3 at zeros.**

## 7.2 R3 reappears (Section 4 verdict)

The R3 obstruction *reappears* at the (log)^3 level — but in a different
form. Instead of "ρ_f = 1−\overline{ρ_f}," the (log)^3 obstruction is
"pair-correlation cancellation between Sm and Fl pieces of (Stieltjes)
split, suppressing the Sm-piece (log)^4 to (log)^3." This cancellation
is RHf-equivalent.

**Conclusion:** the (log)^4 unconditional (which is the natural smooth-piece
asymptotic) and the (log)^3 unconditional are **NOT separated by an
unconditional gap**; the gap (log)^4 → (log)^3 is exactly the same
gap as (log)^3 → (log)^4 in the central-to-zeros conversion, namely
the pair-correlation suppression.

## 7.3 Confidence

| Claim | Confidence |
|---|---|
| "Unconditional at-zeros (log)^3 theorem exists" | 0.05 |
| "User's question can be reduced to existing Theorem B-weaker via Λ→L" | 0.10 (Route 5 fails) |
| "Smooth piece of Stieltjes split gives (log)^4 unconditionally given on-line input" | 0.65 |
| "(log)^3 from cancellation requires RHf or Ratios" | 0.85 |
| "R3 obstruction reappears at (log)^3 in disguise" | 0.78 |
| "Theorem B-weaker (Λ-form, central, (log q̂)^3) is the right unconditional statement; at-zeros version does NOT generalize" | 0.85 |
| "B3 on-line at Re s = 1 (weight aspect, (log)^3) survives — but it's NOT at zeros" | 0.86 (B3's confidence) |

**Aggregate confidence in the headline claim "the user's at-zeros (log)^3
unconditional theorem is NOT achievable": 0.78.**

## 7.4 What is publishable from this analysis

This analysis itself yields **two negative results** worth recording:

**Negative result N1 (Λ → L conversion at zeros).** The relation
`|Λ'(ρ_f,f)|² = q̂^{2β_f}·|Γ(β_f+½+iγ_f)|²·|L'(ρ_f,f)|²` shows that the
Λ-form at zeros and L-form at zeros differ by a factor `q̂^{2β_f-1}·|Γ|²`,
which is uniformly bounded ONLY on RHf (β_f = 1/2). The Theorem B-weaker
central-point Λ-form does NOT directly imply any at-zeros L-form
statement.

**Negative result N2 (Stieltjes split at central line).** The natural
unconditional at-zeros log-power for `Σ_{γ_f}|L'(½+iγ_f,f)|²` family-averaged
over `S_2*(q)` is **(log)^4, not (log)^3**. The (log)^4 is realized by
the smooth piece of the Stieltjes split; the (log)^3 requires
pair-correlation suppression which is RHf-conditional.

These two negative results are publishable as **footnotes** in the
Theorem B-weaker (Λ-form, central) paper. They clarify that
Theorem B-weaker is *not* an at-zeros theorem, and that the at-zeros
analog is structurally one log-power higher.

## 7.5 The two-paper plan, REVISED

Given this analysis:

- **Paper 1** (Theorem B-weaker, Λ-form central, level aspect):
  CONFIRMED publishable, Compositio target. The at-zeros version is
  **NOT** a corollary; it is one log-power higher and conditional.

- **Paper 2** (B3, weight aspect on-line):
  CONFIRMED publishable as the on-line `(1/3)T·log^3 c(T)` result.
  This is at `Re s = 1`, not at zeros. The at-zeros conversion to
  `2/(3π)·T·log^4` requires pair-correlation enhancement, which is
  **RHf or Ratios-conditional** — NOT unconditional (per G2 audit
  superseding B3's optimistic claim).

- **NEW Paper 3** (NOT a separate paper, but a **footnote/appendix** in
  Paper 1): Negative results N1 and N2 above. Clarify the structural
  barrier between central-point (log)^3 and at-zeros (log)^4. Locate the
  R3 obstruction at the pair-correlation level.

**This task did NOT yield an unconditional (log)^3 at-zeros theorem.**
The honest report is: **NO, the at-zeros (log)^3 conversion does not
exist.** The publishable advance is the central-point Λ-form alone.

## 7.6 Recommendation to Saar

**Stop searching for an unconditional at-zeros (log)^3 theorem.** It is
*structurally impossible* via the smooth-piece method (which gives
(log)^4, the conjectural M-N constant), and the (log)^3 reduction
requires RHf-equivalent input (pair-correlation cancellation).

**Proceed with the two-paper plan as in Theorem_B_weaker_log3.md §6.2:**
- Paper 1: Λ-form central-point, (log q̂)^3, 14/3 unconditional.
- Paper 2: B3 on-line, (1/3)·T·log^3 c(T), unconditional.

Do NOT claim either as "an at-zeros theorem" — both are at the *line*,
not at *zeros*.

The at-zeros version remains conditional on RHf or Ratios. This is
consistent with M-N's framing (their (16) is conjectural) and with the
G2 audit (cage statement is the honest unconditional result).

# Done.

**Final aggregate verdict:** The unconditional at-zeros (log)^3 theorem
proposed by the user **does NOT exist**. The natural unconditional
at-zeros log-power is (log)^4 (smooth-piece of Stieltjes split), and
the reduction to (log)^3 via pair-correlation cancellation is RHf or
Ratios-conditional. Theorem B-weaker (Λ-form central, (log q̂)^3) is
the genuine unconditional contribution and stands alone; it does NOT
imply the at-zeros version.

This is consistent with the 14 prior failed routes (Synthesis_PVS §7.3).
Route 14 (synthesis P+V+S) located the obstruction at the parabolic-residue
level — same conclusion in different language. Route 15 (this attempt at
(log)^3 at-zeros) confirms the same: the (log)^3 / (log)^4 gap at zeros
is the same as the central / at-zeros gap, both equivalent to RHf or
Ratios.

**Confidence in this verdict: 0.78.** The verdict is firm: do not
publish a Theorem B-weaker at-zeros (log)^3 claim; stick with the
central-point version.
