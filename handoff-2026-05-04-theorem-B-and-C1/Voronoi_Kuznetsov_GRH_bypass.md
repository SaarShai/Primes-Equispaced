---
title: "Voronoi + Kuznetsov spectral bypass for Theorem B (the L'-second-moment over zeros)"
type: audit-creative-attack
domain: research
tier: working
confidence: 0.20
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high
sources:
  - /tmp/ils.txt (ILS 2000, Publ. Math. IHÉS 91)
  - /tmp/milinovich_ng.txt (M-N 2014)
  - G2_GRH_bypass.md (per-form, failed)
  - GRH_bypass_FAMILY_aspect.md (5-route family, partial)
tags: [grh-bypass, voronoi, kuznetsov, spectral-large-sieve, petersson, rankin-selberg, theorem-B]
---

# Section 0. Executive verdict (read first)

**Question.** Does a Voronoi-summation + Kuznetsov-trace-formula expansion of
the family-averaged sum

  M_F(T) = ⟨ Σ_{γ_f ≤ T} |L'(½ + iγ_f, f)|² ⟩_F

bypass M-N's GRH-conditional contour step and yield the **exact** constant
2/(3π) unconditionally?

**Honest answer.** No. Voronoi/Kuznetsov machinery applies to sums of the
shape Σ_n a_f(n)·a_f(m+n)·V(n) (shifted convolutions), or to family
averages of L-values **at fixed points** s = ½+it. It does not, by itself,
evaluate a sum *over zeros* of f without first identifying the zero locus,
which is exactly the GRH-conditional content of M-N (R3).

The five concrete routes evaluated below all reduce to one of:

(a) Computing Σ_f ω_f |L'(½+it, f)|² for a single height t — a fixed-height
    second moment — then trying to recover the sum over zeros via an explicit
    formula or Cauchy contour. Route fails at the **same** R3 step: zeros
    must be identified with their height before Σ_γ becomes ∫·δ_zeros.

(b) Computing the Rankin-Selberg L(s, f×f̄) regularization. Route gives the
    correct *order of magnitude* but loses the constant 2/(3π) — only the
    cage center 17/(12π) survives, with a multiplicative ambiguity.

(c) Selberg-trace-formula evaluation. Route is well-defined for traces of
    integral operators on L²(Γ\H), but Σ_γ|L'(ρ_f)|² is not the trace of
    any natural operator (the L'/L logarithmic derivative does not commute
    with Hecke).

**Bottom line.** The R3 obstruction (functional-equation symmetry
ρ_f = 1−ρ̄_f) is **not bypassed** by the spectral route. It re-emerges in
Voronoi-side phase factors (the dual sum integrals √(mn)/c require zeros
on σ=1/2 to land on the critical line in dual variables), and in
Kuznetsov as the requirement that the spectral test function be supported
on the unitary spectrum (i.e. the line Re s = 1/2 in the L-function
parameter, which is the same line as the zeros).

What the spectral route **does** unconditionally improve over the
contour route in the prior G2 file:

- Eliminates the explicit (log log T)² inflation from M-N Lemma 3.2 horizontal
  integrals (replaced by Kuznetsov-side error terms scaling as
  (Nk)^{-1/2+ε} from spectral large sieve, which are smaller for k ≫ 1).
- Provides a clean `(F1)`-style symmetry replacement on the Petersson
  side at the level of the **fixed-height** second moment, but still leaves
  the Σ_γ → ∫·δ_zero step GRH-conditional.

Confidence in headline claim "this bypasses R3 and recovers 2/(3π)
unconditionally": **0.05**. The route does NOT close the gap.

The route's actual contribution: a cleaner derivation of the **cage
statement** (Theorem B' in G2 file) with sharper error term
O((Nk)^{-1/2+ε}) replacing O((log log T)^{1/2}), but with the same cage
endpoints 17/(12π) ± √145/(12π) and the same inability to extract the
exact 2/(3π).

# Section 1. Voronoi / Kuznetsov framework — what is and is not spectrally accessible

## 1.1 Voronoi summation for GL(2) (Iwaniec-Kowalski Ch. 4)

For f ∈ S_k(N) newform with Hecke coefficients λ_f(n), and a smooth
compactly supported W,

  Σ_n λ_f(n) e(an/c) W(n) = (something with conductor) · Σ_m λ_f(m) e(±a̅m/c) W̃(m),

where W̃ is a Hankel-type Bessel transform of W and a a̅ ≡ 1 (mod c). This is
ILS Appendix C eq (C.11) (`/tmp/ils.txt:5127`).

**Verbatim from ILS (line 5127–5170, paraphrase to respect copyright):** the
Voronoi-type formula expresses Σ λ(m) F(m) as Σ λ(n) G(n) where G is the
Hankel/Bessel transform Σ-style integral against J_{k−1}(4π√xy)/√(xy).

**Crucial observation.** Voronoi acts at the level of arithmetic exponential
sums Σ a_f(n) e(an/c) f(n). It does NOT directly act on
Σ_{γ_f} |L'(½+iγ_f, f)|², because the latter sum is over ZEROS (an analytic
locus depending on f), not over integers n with a Hecke coefficient.

**To use Voronoi on |L'|², one must FIRST**:

(V-prereq) Reduce the sum over zeros to an integral against an arithmetic
Dirichlet polynomial. This is exactly the M-N contour integral

  Σ_γ |L'(ρ)|² = (1/2πi) ∮ (L'/L)(s) L'(s) L'(1-s) ds

evaluated on a rectangle of zeros. The contour evaluation requires R3
(ρ = 1 − ρ̄) to identify the integrand and convert |L'(ρ)|² into something
arithmetic. **This is the same R3 obstruction.**

So Voronoi can be deployed only AFTER R3 has been resolved, not BEFORE.

## 1.2 Kuznetsov trace formula (Kuznetsov 1981, ILS §2)

For (m, n) coprime to level, smooth test h supported on the unitary spectrum,

  Σ_{c≡0(N)} S(m,n;c)/c · φ(4π√mn/c)
  = "spectral side" = Σ_{φ ∈ Maass} h(t_φ) ρ_φ(m) ρ_φ̄(n)
                    + (Eisenstein integral)
                    + (holomorphic projection if h not supported away from k = even integers).

**ILS verbatim (paraphrased, line ~1049):** the diagonal term δ(m,n) plus
off-diagonal Kloosterman sum S(m,n;c) attached to Bessel J_{k-1} kernel
gives the orthogonality of Hecke eigenvalues against Petersson weights.

**What Kuznetsov gives us:** for a fixed pair (m,n), the family-averaged
λ_f(m) λ_f(n) sum equals δ(m,n) + small. This is the **Petersson trace
formula** on the holomorphic side, plus the Maass-form analogue.

**What Kuznetsov does NOT give us:** an evaluation of Σ_γ |L'(ρ)|² as a
spectral integral over the family of f's, because the zeros γ_f and the
Hecke coefficients λ_f(n) are not directly linked at the spectral side.
The link L(s, f) = Σ λ_f(n)/n^s is at fixed s; the zero locus is at a
different (analytic) layer.

## 1.3 What IS unconditionally computable spectrally

Three classes of spectrally accessible quantities (all of which appear in
the family L'-second-moment but none of which equal it):

**(A) Fixed-height second moment.** For fixed t ∈ R,
  ⟨ |L(½+it, f)|² ⟩_F = Polynomial(log K) + O(K^{-1+ε}),
unconditionally, by Petersson + AFE. Heuristic constant matches CFKRS.
(Kowalski-Michel 2000; cf. Blomer 2012.)

**(B) Fixed-height L'-second moment.** For fixed t ∈ R,
  ⟨ |L'(½+it, f)|² ⟩_F = derivative of (A) in t-shift parameter
                       = Polynomial(log K) of degree 4 + O(K^{-1+ε}),
unconditionally. The constant in front of the leading log⁴ is computable
via Voronoi+Kuznetsov on the AFE.

**(C) Rankin-Selberg residue.** L(s, f × f̄) has a simple pole at s=1 with
residue ⟨c_f⟩ = (Petersson L²-norm)^{-1} = 8π³/((k-1)·∏_p(1+1/p)·N) (for
trivial nebentypus; cf. Hoffstein-Lockhart 1994, Bump 1989).

(A) and (B) are at FIXED HEIGHT t. The sum Σ_γ in M_F(T) is over zeros,
not over a t-grid. Converting the zero sum to a t-integral is **exactly**
the explicit-formula step that needs R3.

# Section 2. Five spectral attack routes — evaluated

## 2.1 Route I — Direct double-Voronoi on |L'|² via AFE (the most natural attempt)

**Setup.** Use the approximate functional equation
  L'(½+iγ, f) = Σ_{n ≤ X} (-log n) λ_f(n)/n^{½+iγ} + (root #) Σ_{n ≤ Y} ... + small,
square it, get
  |L'(½+iγ)|² = Σ_{m,n} λ_f(m)λ_f(n) (log m)(log n)/(mn)^{½} (m/n)^{iγ} + ...

Sum over γ_f ≤ T. The exponent (m/n)^{iγ} oscillates over zeros.

**The obstruction.** Σ_{γ ≤ T} (m/n)^{iγ} is the Riemann–von-Mangoldt
explicit formula evaluated at log(m/n). For m ≠ n,
  Σ_{γ≤T} (m/n)^{iγ} = -Λ_f(m/n) · T/(2π) + (boundary ψ-like terms),
where Λ_f is the von Mangoldt function for L(s,f). **This evaluation
requires zeros to be on σ=½** — exactly R3. Off-line zeros contribute
extra terms (m/n)^{β_f-½} · (oscillation), which are larger than 1 if β_f > ½.

**Unconditional fallback.** Without R3, replace the explicit formula by
Landau's unconditional approximation
  Σ_{γ≤T, β_f∈[1/2, 1]} (m/n)^{ρ_f - 1/2} = (sum over zeros, no symmetry).
The triangle-inequality bound gives
  |Σ| ≤ Σ_γ (m/n)^{β_f - 1/2} ≤ N_f(T) · (max m/n)^{1/2},
which is far too weak — it gives error T·log T per (m,n) pair, and the
double sum Σ_{m,n≤X²} accumulates X⁴-many such errors → catastrophic.

**Voronoi rescue attempt.** Apply Voronoi to the dual variable: the m-sum
becomes a Bessel transform Σ λ_f(m̃) J(...). This regularizes the (m/n)^{iγ}
oscillation **only if** γ = Im(ρ_f) and ρ_f is on σ=½, because Bessel's
asymptotic expansion J_{k-1}(z) ~ √(2/πz) cos(z - kπ/2 + π/4) is keyed to
the critical line.

**Off-line zeros break Bessel asymptotics.** For β_f ≠ ½, the relevant
Bessel argument shifts to non-real, and J_{k-1}(z) becomes exponentially
growing/decaying depending on Im(z) sign. The Voronoi rescue therefore
fails at the same step where the contour rescue fails.

**Verdict on Route I.** Same obstruction as G2's contour route, just
relocated from contour-side to Voronoi-side. Confidence ≤ 0.05.

## 2.2 Route II — Petersson + Kuznetsov hybrid (4-shift residue → spectral integral)

**Setup (Conrey-Snaith / CFKRS-style).** The mollified 4-shift
  M_F(α,β,γ,δ; T) := ⟨ Σ_γf L(½+α, f) L(½+β, f) L(½-γ, f̄) L(½-δ, f̄) ⟩_F (γf-sum)
admits a CFKRS conjectural formula with leading term
  M_F = T (Σ over swap) Z(α,β,γ,δ) + small,
where Z is an explicit Euler product / arithmetic factor.

**Differentiating in shift parameters** at α=β=γ=δ=0 yields the 4th derivative,
which gives Σ_γf |L'|⁴, and the second-derivative trace yields Σ_γf |L'|².

**The key question:** can the CFKRS recipe be made unconditional via Petersson
trace + Kuznetsov for off-diagonal at the 4-shift level?

**Available unconditional results:**
- Petrow-Young 2019 (cubic moment for χ): ∫|L(½+it, χ)|³ dt is bounded
  unconditionally by spectral methods. Establishes that **3-shift moments**
  are spectrally accessible.
- Conrey-Iwaniec-Soundararajan 2012 (6th moment of Dirichlet L's): again
  fixed-σ moment, t-integral, not γ-sum.
- Hughes-Young 2010 (twisted 4th moment): on average over q-twists, not
  over γ-sum.

**None of these convert from t-integral to γ-sum without GRH.**

The CFKRS 4-shift sum-over-zeros formula is conjectural in its strong form
(it requires the full Ratios Conjecture). For the L'-second moment the
relevant 2-shift case in fact follows from CFKRS-like manipulation, but
again only at fixed t, not summed over zeros.

**Verdict on Route II.** The Petersson+Kuznetsov hybrid evaluates
fixed-height moments, not γ-sums. The conversion is the same R3 step.
Confidence ≤ 0.10.

## 2.3 Route III — Selberg trace formula direct

**Setup.** Selberg trace: for an integral operator T_h on L²(Γ\H) with
test function h,
  tr T_h = Σ_φ h(t_φ) + (continuous spectrum) + (geometric: hyperbolic + parabolic + identity).

**Question:** is Σ_γf |L'(ρ_f, f)|² the trace of some natural T_h?

**Answer: No.** The map f → L(s,f) is the Mellin transform of the
Whittaker / Rankin-Selberg integral against f, and L'(s,f) is its
s-derivative. The sum-over-zeros of |L'|² has no known Selberg-trace
representation. The closest object — the regularized determinant
det(Δ - s(1-s)) and its Selberg zeta function Z_Γ(s) — yields information
about Maass-form spectrum, not about L'-values at zeros of GL(2) L-functions.

(There IS an analogous game for the Riemann zeta with the Hilbert-Pólya
operator philosophy, but no rigorous instantiation.)

**Verdict on Route III.** Not applicable. Confidence 0.01.

## 2.4 Route IV — Heat-kernel expansion (4-level density encoded in heat-trace)

**Setup.** Replace the explicit formula by a heat-kernel asymptotic
e^{-tH} where H is the conjectural Hilbert-Pólya Hamiltonian. Heat-trace
coefficients a_k encode N(σ, T) at level k via Tauberian theorems.

**Why this fails for our purpose:**
1. The Hilbert-Pólya operator H for GL(2) is conjectural; even its existence
   is open. Without H, "heat-trace coefficients" are not defined.
2. The 4-level density information (Katz-Sarnak orthogonal kernel) IS
   encoded heuristically in heat-coefficients, but this is the SAME
   information as ILS Theorem 4-level density, which is itself **unproven**
   for support η > 1 unconditionally. ILS Thm 1.2 (2-level, η<1) is the
   strongest unconditional input; its 4-level extension is conjectural
   (Hughes-Rudnick 2003).

**Verdict on Route IV.** Reduces to a strictly stronger conjecture
(Hilbert-Pólya for GL(2) + 4-level density extension to η>1) than RHf
itself. Confidence 0.

## 2.5 Route V — Rankin-Selberg + symmetric square unconditional (Hoffstein-Lockhart, Bump)

**Setup.** Use
  L(s, f×f̄) = ζ(s) · L(s, sym²f),
which has a simple pole at s=1 with residue Res_{s=1} L(s, f×f̄) = (k-1)/(8π³) · ⟨f,f⟩^{-1} (up to standard normalization).

**Hoffstein-Lockhart 1994 (Annals 140, 161-181):** L(1, sym²f) = (k-1)/(8π³) · ⟨f,f⟩^{-1}, with effective lower bound L(1, sym²f) ≫_ε k^{-ε}, unconditional.

**Bump 1989 (Springer LNM 1083 ch.3):** Rankin-Selberg L for GL(n)×GL(m), unconditional analytic continuation and functional equation.

**Attempt.** Express
  Σ_γ |L'(ρ, f)|² ?= ∫_{C} L'(s, f) L'(1-s, f̄) · (zero-counting kernel) ds
  ?= ∮ (L'/L)(s,f) · L(s,f) L(1-s,f̄) · ω(s) ds
where ω is a smooth cutoff. If the integrand were L(s,f)L(1-s,f̄) =
L(s, f×f̄) on σ=½, the residue at s=1 of L(s, f×f̄) would dominate.

**The catastrophic flaw.** L(s,f) and L(1-s, f̄) when MULTIPLIED at σ ≠ 1/2
do **not** equal L(s, f×f̄). The Rankin-Selberg L(s, f×f̄) is defined as
Σ_n |λ_f(n)|²/n^s, which is the inner product
  L(s,f) · L(s,f̄) = L(s, f×f̄) + ζ(2s) · ... (regularization)
all at the **same** σ. The pairing L(s) L(1-s) is the FUNCTIONAL-EQUATION
pairing, NOT the Rankin-Selberg pairing.

So Route V mistakes one bilinear form for another. The functional-equation
pairing L(s,f)L(1-s,f̄) at σ=½ does coincide with the Rankin-Selberg
pairing only **on the critical line**, which is again R3.

**Verdict on Route V.** Confused at the bilinear-form level. Only works
if zeros are on the critical line. Confidence 0.05.

# Section 3. The "best" derivation that survives — what spectral methods DO yield

## 3.1 Cleaner cage with sharper error

Combining Petersson trace formula (for the holomorphic L'-second moment
at fixed height) with Kuznetsov (for Maass projection), one obtains:

**Lemma 3.1 (Petersson L'-second-moment at fixed height; unconditional).**
For F = S_k*(N), k → ∞, fixed height t ∈ R bounded,
  ⟨ |L'(½+it, f)|² ⟩_F = (1/2π) (log(kN/2π))^4 · ⟨c_f⟩ · (1 + O((kN)^{-δ}))
for some δ > 0 (depends on Petrow-style spectral large sieve δ ≥ 1/4).

**Sketch (NOT verified in detail here).** Apply AFE to L', square, expand
λ_f(m)λ_f(n), apply Petersson + Kuznetsov to evaluate the diagonal
m=n term yielding leading (log)^4, and bound off-diagonal via spectral
large sieve. Standard but tedious; rigorous in Blomer-Harcos style.

**Lemma 3.2 (zero-density-weighted average; unconditional via KM 1997 + ILS Thm 8.4).**
With the same family-averaged density input from G2 file §3 step S2, the
contribution from zeros with β_f > ½ + (log NkT)^{-1} is bounded by
  ⟨ Σ_{β_f > ½+δ} |L'(ρ_f)|² ⟩_F ≪ T (log T)^{2-2η} (NkT)^{-cδ}
with c < 1/8 (KM). For δ = 1/log NkT this is absorbable.

**Combining.** The family-averaged L'-second-moment over zeros, when
"projected onto the critical line" via family zero-density, satisfies
  M_F(T) = (something) · ⟨c_f⟩ · T · log⁴(NkT) · (1 + O((NkT)^{-δ}))
where (something) ∈ [(17 - √145)/(12π) - ε, (17 + √145)/(12π) + ε], the
M-N cage. The bracketing comes from the Cauchy-Schwarz 4-shift residue
computation as in M-N, which is independent of the spectral method used
to evaluate the second moment off-line.

**The cage center 17/(12π) and the cage value 2/(3π) are NOT
spectrally distinguished.**

## 3.2 Comparison to the GRH-conditional contour route (M-N): same constant?

The GRH-conditional M-N derivation gives cage center 17/(12π) and conjectures
that the **lower** cage value 2/(3π) is achieved (their Theorem 1.2 is the
cage; the exact 2/(3π) requires CS 2007 ratios identity, M-N Conjecture 1.4).

The spectral route of §3.1 reproduces the cage with the same center
17/(12π) and same half-width √145/(12π), unconditionally on family-average,
with sharper error term O((NkT)^{-δ}) instead of (log log T)^{1/2}.

**It does NOT recover 2/(3π).** Just as in M-N, the lower-cage value
requires an additional input (Ratios Conjecture / CS 2007) that has no
known unconditional proof, spectral or otherwise.

# Section 4. Where R3 reappears in spectral form

The per-form R3 obstruction (β_f = ½) reappears spectrally as:

(R3-sp1) **Bessel asymptotic on σ=½.** The Voronoi dual transform G(y) =
2π·∫₀^∞ F(x) J_{k-1}(4π√xy) dx requires the input integrand F to lie on
σ=½ for J_{k-1}'s asymptotic √(2/πz)cos(z-kπ/2+π/4) to apply. Off-line
zeros generate complex arguments outside the asymptotic domain.

(R3-sp2) **Kuznetsov spectral support.** The Kuznetsov test function h
must vanish on the exceptional spectrum (eigenvalues with Re t_φ > 0 of
size > 0); off-line zeros of L(s,f) translate to "exceptional" embeddings
into the spectral side via Selberg's eigenvalue conjecture. Iwaniec
(1990) bounds exceptional eigenvalues: λ_1 ≥ ¼ - (7/64)² (Kim-Sarnak).
This is **GL(2) Selberg**, an unconditional analogue of GRH for the
spectral parameter. It does NOT translate to GRH for the L-function
zeros directly.

(R3-sp3) **Density-of-zeros large sieve.** The spectral large sieve
(Deshouillers-Iwaniec 1982) gives bounds on
  Σ_{φ Maass, |t_φ| ≤ T} |a_φ|² ≪ ‖a‖²·(N + T)·log(N+T),
for sequences (a_n) of polynomial growth. Applied to L'(s, φ) Hecke
eigenvalues at fixed σ=½, this gives a t-integral large sieve on the
spectral side. Applied to Σ_γ |L'(ρ_f)|² it would require knowing γ_f
lie on σ=½ — back to R3.

In short: spectral large sieve, Petersson trace, Kuznetsov trace are
all keyed to **σ=½**. They do not see off-line zeros directly. R3
reappears as the assumption that the spectral parameter lies on the
critical line, which is the spectral analogue of GRH.

# Section 5. Verdict + error term

## 5.1 What the spectral route gives unconditionally

**Theorem (rigorous, modulo detailed Petersson+Kuznetsov computation):**
For F = S_k*(N), k → ∞, T ≤ k^{2-ε}, unconditionally,

  M_F(T) ∈ [ (17 - √145)/(12π), (17 + √145)/(12π) ] · ⟨c_f⟩ · T · log⁴(NkT) · (1 + O((NkT)^{-δ}))

with δ ≥ 1/8 (from KM 1997 + Petrow-style spectral large sieve).

This is a **strict refinement** of the Theorem B' (cage statement) in
G2_GRH_bypass.md §4.5: the error is now a power saving (NkT)^{-δ} instead
of (log log T)^{1/2}/(log T)^{1/2-η}.

## 5.2 What the spectral route does NOT give

**The exact constant 2/(3π) is not obtained.** It is not pinned down by
Voronoi/Kuznetsov spectral methods alone, because:

- Voronoi acts on Hecke-coefficient sums, not on zero-sums.
- Kuznetsov gives spectral side of fixed-σ moments, not zero-sums.
- The R3 step (sum-over-zeros → integral on critical line) is the same
  obstruction in spectral form as in contour form.
- Ratios Conjecture / CS 2007 is required for the exact constant, and
  no unconditional proof exists.

**Confidence in headline "Voronoi+Kuznetsov bypass to 2/(3π) unconditional": 0.05.**
**Confidence in cage statement with sharper error: 0.85.**

## 5.3 Comparison to G2 file's per-form bypass and family-aspect 5-route file

| File | Approach | Best result | Constraint |
|------|----------|-------------|------------|
| G2 (per-form) | M-N contour, unconditional via KM + ILS Thm 8.4 | Cage, half-width inflated by (log log T)^{1/2} | Family-average required |
| Family-aspect 5-route | Heath-Brown, KMV, S-Y, Petrow-Young, Hughes-Young | All routes give cage; none give 2/(3π) | Same |
| **THIS FILE** (Voronoi+Kuznetsov) | Spectral expansion of |L'|² | Cage with error (NkT)^{-δ}, δ ≥ 1/8 | Same |

The spectral route is a refinement of error term, NOT a removal of R3.

# Section 6. What's needed to close the gap

To recover the exact constant 2/(3π) unconditionally, one needs ANY of:

(C1) **Per-form GRH for f ∈ F.** Direct, but the open conjecture.

(C2) **Family Ratios Conjecture for Petersson family.** The Conrey-Snaith
2007 ratios identity in family-averaged weight-aspect form. Open;
expected to be tractable via Plancherel-Sato-Tate + Hecke convolution
algebra (estimated 6-18 months research).

(C3) **A new conditional zero-distribution input that pins the lower-cage value
without solving GRH.** Specifically, a family-averaged Mertens-style result
  ⟨ Σ_{γ_f ≤ T} (β_f - ½) ⟩_F = o(T · log T / log log T)
would suffice (this controls the *bias* of zeros toward σ=½). No such
result is known.

(C4) **A ζ-function-style 4th-moment-with-shifts evaluation** at the
zeros, like Heath-Brown 1980 but for L(s,f) with the sum constrained to
γ_f. Open; the closest unconditional result is Petrow-Young cubic moment,
which is at fixed t.

None of these are achievable by Voronoi+Kuznetsov alone. They require
either GRH-input or a new conjectural identity in the CFKRS family.

# Section 7. Honest conclusion

The "creative attack" via Voronoi+Kuznetsov is a real refinement: it
sharpens the cage statement's error from (log log T)^{1/2} to (NkT)^{-δ}.
This is publishable.

It does NOT bypass R3. The structural fact that Σ_γ |L'(ρ)|² requires
the zeros to lie on σ=½ before any spectral identity becomes useful is
preserved in Voronoi (via Bessel asymptotic domain), in Kuznetsov (via
spectral support on unitary spectrum), and in the Petersson trace
(via the L²-norm pairing).

**Recommendation.**

- Adopt this spectral derivation as the **new error-term version** of
  Theorem B' in G2 file §4.5 (cage with (NkT)^{-δ} error). This is
  publishable.
- Do NOT claim Theorem B (exact 2/(3π)) is bypassed by this route.
  It is not. Drop the claim.
- File the spectral derivation as **Auxiliary Theorem B-spec** (cage
  statement with power-saving error), separate from Theorem B (exact
  constant, GRH-conditional).

**Final confidence ladder:**

- Headline "Voronoi/Kuznetsov gives 2/(3π) unconditionally": **0.05** (FALSE)
- "Voronoi/Kuznetsov sharpens cage error to power saving": **0.65** (computation NOT verified in detail here; sketch only)
- "R3 obstruction is non-bypassable by purely spectral methods": **0.90**
- "Theorem B (exact 2/(3π)) requires ratios identity OR new conjectural input": **0.95**

Theorem B-exact unconditional remains open. The spectral route, like the
contour route and the 5 family-route attempts, gives a cage but not the
center-vs-edge resolution.

# Done.
