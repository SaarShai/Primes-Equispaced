---
title: "Contrarian attempt — assume Theorem B-exact (constant 2/(3π)) is FALSE, derive a contradiction"
type: audit-contrarian
domain: research
tier: working
confidence: 0.05
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (reverse / proof-by-contradiction strategy)
sources:
  - CFKRS_symbolic_verification.md (16 = 2⁴ confirmed sympy)
  - RMT_Painleve_GRH_bypass.md (5 RMT routes failed)
  - RankinSelberg_trace_attack.md (5 RS variants failed)
  - Voronoi_Kuznetsov_GRH_bypass.md (5 spectral routes failed)
  - arxiv_2601_06292_analysis.md + arxiv_2601_06292_alt_GL2_routes.md (DHP-C wrong object)
  - Theta_lift_GRH_bypass.md (Howe duality wrong family)
  - FirstPrinciples_creative_attack.md (10-route brainstorm, all fail)
  - /tmp/milinovich_ng.txt (Milinovich-Ng 2014; conjectural target)
  - /tmp/ils.txt (ILS 2000; 1- and 2-level density unconditional, n≥3 conditional)
tags: [contrarian, proof-by-contradiction, theorem-B, 2-over-3pi, n-level-density, RMT]
---

# Bottom line (honest, written first)

**No route in this contrarian audit produces a genuine contradiction from
the assumption A ≠ 2/(3π).** Every "near-contradiction" identified below
turns out, upon careful inspection, to be a contradiction with a
*conditional* statement (assuming GRH, or assuming n-level density at
n ≥ 3 with full Schwartz support, or assuming the RMT↔L-function
moment-equality conjecture). None of these conditional statements is
known unconditionally for the GL(2) Petersson family at the level needed.

In particular:

1. The cage [(17−√145)/(12π), (17+√145)/(12π)] = [0.131, 0.452] is the
   *only* unconditional pinch on A. It admits all values in this
   interval, so any A in the interval, A ≠ 2/(3π) ≈ 0.212, is
   unconditionally consistent with everything currently known.
2. The RMT prediction 2/(3π) is *unique* on the random-matrix side
   (Hughes 2001, CRS 2006, Conrey-Snaith 2007) — but the uniqueness is
   inside the SO(2N) characteristic-polynomial calculation, NOT inside
   any unconditional L-function statement.
3. CFKRS-symbolic-verification confirms the *recipe* gives 2/(3π); the
   recipe itself is the conjectural input.

**Conclusion.** "A ≠ 2/(3π)" leads to no contradiction with anything
unconditionally proved. Theorem B-exact is genuinely conditional. The
proof-by-contradiction strategy fails — symmetrically and for the same
underlying reason as the seven direct attacks: there is no unconditional
4-level density (or equivalent strength input) on the orthogonal family
of GL(2) Petersson newforms.

---

# Section 1. Attack routes 1–7 evaluated

For each route the question is the same: assuming the actual constant
in M_F(T) ~ A · ⟨c_f⟩ · T · log⁴ X is some A ≠ 2/(3π), does this
contradict an *unconditionally proved* statement?

## Route 1. Higher-moment incompatibility

**Strategy.** The RMT recipe gives, for the SO(2N) family with N ~
log⁴ X, a *full sequence* of moments

  E[|Z'(1)|^{2k}] = M_{O,k}(N), k = 1,2,3,…

If the L-family matches RMT at the second moment with constant
A ≠ 2/(3π), one might expect *some* higher moment 2k ≥ 4 to be
unconditionally proved AND inconsistent with A ≠ 2/(3π).

**Reality check.** Higher moments of |L'(½, f)|^{2k} for k ≥ 2
**are not unconditionally proved**, even at family-averaged level.
The strongest unconditional bound is Soundararajan's
upper-bound-with-extra-log technique (and refinements
Soundararajan-Young, Heap-Soundararajan, Harper) which give *upper*
bounds matching RMT order of magnitude with a possible factor (log
log)^O(1) deficit, NOT asymptotic equality. Lower bounds (Heap-Soundararajan,
Radziwiłł-Soundararajan) match order-of-magnitude unconditionally but
not the constant. **So no higher moment is unconditionally pinned at a
specific RMT constant**, hence no leverage to contradict A ≠ 2/(3π).

**Verdict.** Higher-moment route gives **no contradiction**. The
"leverage" exists only conditionally (under GRH or under the full ratios
conjecture).

Confidence this route yields contradiction: **0.02**.

## Route 2. Functional equation rigidity

**Strategy.** The functional equation L(s,f) = ε_f · q^{1/2-s} · γ(s) /
γ(1-s) · L(1-s,f) is a hard symmetry. The *root number* ε_f = ±1 (real,
trivial central character, weight k ≡ 0 mod 4 sign) gives orthogonal
symmetry type for the family. The constant 2/(3π) is the SO(2N)
4-parameter ratios value at α=β=γ=δ=0. Could orthogonal symmetry FORCE
the constant to be 2/(3π)?

**Reality check.** Orthogonal symmetry forces the *form* of the
log-density polynomial — i.e., it determines that

  ⟨(1/N) Σ_γ φ(γ N)⟩ → ∫ φ(x) (1 - sin(2πx)/(2πx)) dx

(1-level density, ILS 2000, theorem, **unconditional with support of
φ̂ in (-1,1)**). This is a 1-level statement. The constant 2/(3π) is a
4-level statement at α,β,γ,δ → 0 with two derivatives. **Orthogonal
symmetry does NOT force the 4-level limit unconditionally** — it forces
it *conditional* on Schwartz support of φ̂ being arbitrarily large.
ILS Theorem 1.1 explicitly fails beyond ν=2 without enlarging the
support.

What about the functional equation at the level of *moments*? The
fourth moment of L(½, f) over f ∈ F_k is NOT unconditionally
pinned at the CFKRS constant either: only upper/lower bounds with gaps
at the log-power level (Blomer-Khan-Young 2019 gives unconditional
asymptotic for the 4th moment with main term but with a *different*
combinatorial structure than what's needed for L'). The 2nd moment of
**L'** at zeros is qualitatively a different beast — the derivative
forces extra log factors and the at-zero localization forces 4-level
input.

**Verdict.** Functional equation pins the symmetry *type* and the
*structure* of the asymptotic, but not the *exact constant*
unconditionally. No contradiction.

Confidence this route yields contradiction: **0.03**.

## Route 3. Consistency with the on-line second moment

**Strategy.** Define the *on-line* family-averaged moment

  J(T) = ∫₀ᵀ Σ_f^h ω_f |L'(½ + it, f)|² dt.

This is unconditionally evaluable via Petersson + approximate functional
equation + standard Voronoi at the level of leading asymptotic with
constant 1/(3π) (this is the existing project result `B3_*RIGOROUS.md`,
project file confirms unconditional 1/(3π) for the on-line second moment).
Hypothesis: by Plancherel + density arguments, on-line moment + 4-level
density should *force* the at-zeros constant to a specific value, hence
contradiction if not 2/(3π).

**Reality check.** Plancherel-style conversion ∫_t |L'|² dt → Σ_γ |L'(ρ)|²
requires knowing where the zeros are (i.e., GRH for f, or n-level density
input). Concretely:

  Σ_γ |L'(ρ_f)|² = ∫_{(c)} (ζ_f'/ζ_f)(s) · |L'(s,f)|² ds (contour residue)

and the contour shift to ½ requires control over zeros off the line. Without
GRH (per-form) or 4-level density (family), the conversion
*has an error of size T log³ T*, which is exactly the size of the leading
constant times T log⁴ X. So the on-line ↔ at-zero correspondence is
**exactly the GRH gap**.

The constant ratio (at-zeros)/(on-line) = 2 = (2/(3π))/(1/(3π)) is the
RMT-predicted ratio (Hughes 2001 Eq. 4.3.16 — orthogonal vs unitary
factor of 2 at one derivative, and the ratio 2× holds through CRS 2006
Painlevé-IV calculation). The *RMT* prediction gives this 2× cleanly,
and the on-line constant 1/(3π) is unconditional. But the at-zero
*equality* between L-function family and SO(2N) ensemble is exactly
the conjectural input.

**Verdict.** Apparent leverage; on inspection, the leverage *is* the
conjecture itself. No contradiction.

Confidence this route yields contradiction: **0.05**. (Highest of the
seven, but still no genuine contradiction.)

## Route 4. Petersson trace + L(1, sym² f) link

**Strategy.** c_f = L(1, sym² f) is unconditionally computable via
Hoffstein-Lockhart 1994 (lower bound 1/log) and Goldfeld-Hoffstein-Lieman
upper bound. Family-averaged Σ_f c_f is unconditional (Iwaniec-Luo-Sarnak
1999, Kowalski-Michel). The Petersson trace formula links Σ_f a_f(m)·a_f(n)
to a Kloosterman + Bessel sum unconditionally. Could the chain
(Petersson + sym² + L'-derivative-of-Euler-product) FORCE the second-moment
constant?

**Reality check.** The chain produces, on the family-averaged side, the
*shape* M_F(T) = (constant) · ⟨c_f⟩ · T · log⁴ X with
**constant determined by a 4-fold residue** (4-shift CFKRS) — and the 4-shift
residue is exactly the 4-level-density object. The 4-shift residue is
*conjectural* (CFKRS recipe is the conjecture; Conrey-Snaith ratios
conjecture is the conjecture). The Petersson+sym² link gives the *factorization*
M_F(T) = (combinatorial) × ⟨c_f⟩ × T × log⁴ X but does NOT
unconditionally pin the combinatorial factor.

In particular, the symbolic-verification file `CFKRS_symbolic_verification.md`
confirmed via sympy that *if* CFKRS recipe is correct, the constant is
exactly 16/(24π) = 2/(3π). The "if CFKRS" is the gap — CFKRS is a
*recipe* with conjectural input, not an unconditional theorem at the level
of fourth-derivative residues for GL(2).

**Verdict.** No contradiction. Petersson + sym² gives the structure but
not the constant unconditionally.

Confidence this route yields contradiction: **0.03**.

## Route 5. Hughes-Snaith / CRS 2006 RMT uniqueness

**Strategy.** The RMT side calculation (Hughes 2001 PhD; Conrey-Rubinstein-Snaith
2006 Painlevé) gives a UNIQUE answer 2/(3π) for the SO(2N) characteristic-polynomial
moment. If A ≠ 2/(3π), then either:
  (a) RMT calculation has an error — but it's been verified independently
      (CRS 2006 Painlevé-IV, CFKRS recipe, symbolic-verification file).
  (b) The L-function family does NOT match RMT — but ILS 2000 unconditionally
      proves 1-level and 2-level density match SO(even). So mismatch at 4-level
      would be *exotic*: agree at 1- and 2-level, disagree at 4-level.

**Reality check.** Option (b) is logically possible. ILS 2000 proves
1-level (full Schwartz support up to (-2,2) for orthogonal) and 2-level
(restricted support) **unconditionally**. ILS does NOT prove 3-level or
4-level unconditionally; their density results for n ≥ 3 require enlarged
support of φ̂ that's known only conditionally on GRH.

There are rigorous results about families where n-level density agrees
with RMT at low n but where matching at high n is open: this is
**precisely the GL(2) Petersson family situation**. There is no
unconditional theorem saying "1-level + 2-level + functional equation
⇒ all higher levels match." Such a theorem would, in essence, BE the
unconditional Theorem B.

**Verdict.** Option (b) is unconditionally possible. RMT uniqueness
on the *RMT side* doesn't transfer to L-side without the conjectural
matching at 4-level. **No contradiction.**

Confidence this route yields contradiction: **0.04**.

## Route 6. Numerical inconsistency at large T

**Strategy.** If A ≠ 2/(3π) by some δ > 0, family-averaged numerical
data at T = 10⁶–10⁹ should reveal the deviation. The project's
`B2_*` numerical files compute the at-zero second moment for small
N (level 11, 37) and small k (12, 16, 24).

**Reality check.** The convergence to the asymptotic is *logarithmic*
in T because the leading term is T log⁴ X. To distinguish 2/(3π) ≈ 0.2122
from, e.g., 0.2200 numerically with confidence requires
T at which (lower-order corrections) / (leading) < 0.04. Lower-order
corrections include T log³ X (constant ~ 1) and T log² X. Ratio
becomes (log³ X)/(log⁴ X) = 1/log X. For 1/log X < 0.04 we need
log X > 25, i.e., X > e²⁵ ≈ 7·10¹⁰, which means T ~ 10¹⁰ for low-level
forms. This is **beyond any feasible single-form computation** (PARI's
zero-finding for L(½ + iγ, f) at γ ~ 10¹⁰ is not realistic).

Even with family averaging, the per-form computation at T = 10⁹ for
hundreds of forms is infeasible on standard hardware. The project's
B2 numerics at T = 800 already show u_f = 2.63 deviation (not 0.21
target) — interpreted as slow log-rate convergence (factor 1.94
from finite-t conductor), not as evidence A ≠ 2/(3π). Bottom line:
numerics CANNOT pin A to within 4% accuracy at currently feasible T.

**Verdict.** Numerical route is insufficient to refute A ≠ 2/(3π)
nor to confirm 2/(3π) tighter than the cage. **No contradiction
available numerically.**

Confidence this route yields contradiction: **0.01**.

## Route 7. Beilinson-Deligne motivic period uniqueness

**Strategy.** L'(½, f) is conjecturally a Beilinson regulator
(motivic cohomology pairing). Second moment of regulators ↔ height
pairings. If 2/(3π) is a *uniquely determined* motivic period,
deviation A ≠ 2/(3π) would contradict uniqueness.

**Reality check.** Beilinson's conjecture for L'(½, f) is **OPEN**
(proved only in very special cases — Borel for ζ, Beilinson for modular
curves at s=2 — but NOT for L'(½, f), f ∈ S_k(N)). So motivic
uniqueness, even if true, is itself conjectural at the level needed.
Worse: the Beilinson regulator pairing is non-archimedean / archimedean
period; the constant 2/(3π) is a transcendental factor that, in
the conjectural Beilinson framework, is a Q-rational ratio of a
height pairing to a discriminant. The factor *π* in 2/(3π) is the
archimedean-place contribution (Tamagawa-style), and 2/3 is the
combinatorial/RMT factor — these are NOT pinned by motivic uniqueness
in any current rigorous framework.

**Verdict.** Motivic uniqueness route is doubly-conditional
(Beilinson conjecture + identification of constant as Q-rational period).
**No unconditional contradiction.**

Confidence this route yields contradiction: **0.01**.

---

# Section 2. Best route — full derivation

The strongest of the seven (Route 3, on-line moment consistency) deserves
a full derivation, because if any route would yield a contradiction
this would be it. The on-line moment 1/(3π) is unconditional; the
at-zero moment 2/(3π) is double the on-line — an exact factor-of-2
pattern with deep RMT origin.

## Setup

**Unconditional on-line result** (project file `B3_*RIGOROUS.md`):

  J(T) = ∫₀ᵀ Σ_f^h ω_f |L'(½ + it, f)|² dt = (1/(3π)) · ⟨c_f⟩ · T · log⁴ X · (1 + o(1)).

**Conjectural at-zero target** (M-N, Theorem B-exact):

  M_F(T) = Σ_f^h ω_f Σ_{|γ_f|≤T} |L'(½+iγ_f,f)|² = (2/(3π)) · ⟨c_f⟩ · T · log⁴ X · (1 + o(1)).

**Ratio:** M_F(T) / J(T) → 2.

## Conversion attempt (the Plancherel route)

For a single f with full GRH:

  (i)  Σ_γ |L'(½+iγ,f)|² = (1/(2πi)) ∮ (L'/L)(s,f) · L'(s,f) · L'(1-s,f) ds

where the contour encloses zeros in the critical strip with |Im| ≤ T.
The integrand has poles at zeros (from L'/L) plus an extra pole at s=1
(from L'/L's residue 1 there) + at s=0. Shift contour to σ = ½. **The
contour shift requires zeros to lie on σ = ½**, i.e., GRH for f.

**Without GRH per f**: the contour cannot be shifted past zeros off the
line. Family averaging *almost* helps: for the family
{f ∈ F_k} most f satisfy "near-GRH on average" (Bombieri-Vinogradov-style
density theorems for L-functions, e.g., ILS Theorem 1.5: number of
zeros off the line is bounded by a Vinogradov-Korobov-like quantity
on average over the family). But "most f" is not "all f", and the
exception set could contribute non-negligibly to the moment.

**Quantification.** Density estimates (ILS 2000 §10) give:

  #{f ∈ F_k : f has zero in σ ≥ ½ + δ, |Im| ≤ T} ≪ k^{1-cδ} · T^{O(1)}.

The exception-set contribution to M_F(T) is bounded by

  exceptional ≪ k^{1-cδ} · T^{O(1)} · (max |L'|²)

and (max |L'|²) is at most (Soundararajan upper bound)
≪ exp(C log k log T / log log(kT)). Multiplying these, the exception
contribution is *o(M_F(T))* only if cδ > exponent — unconditional δ small,
exception contribution can match the leading order.

This is exactly why on-line ↔ at-zero conversion is called
"conditional on partial-GRH" — partial-GRH is the density estimate at
δ small enough.

**Conclusion of route 3 derivation.** The on-line ↔ at-zero ratio = 2
is forced *only conditionally* on density estimates strong enough to
control the exception set. The strongest unconditional density estimate
(Kowalski-Michel) does not suffice. Hence A ≠ 2/(3π) is consistent
with the unconditional on-line result J(T) = (1/(3π))·…; the assumption
fails to produce a contradiction with anything proved.

---

# Section 3. Does "A ≠ 2/(3π)" lead to a real contradiction?

**No.**

The closest candidate (Route 3) reduces, on careful inspection, to
exactly the same gap as the seven direct attacks: **n-level density
at n ≥ 3 with full Schwartz support for the GL(2) Petersson family
is conjectural, not proved**. Every "rigidity" argument that *seems*
to force A = 2/(3π) — RMT uniqueness, functional-equation symmetry,
on-line ↔ at-zero ratio, motivic period uniqueness, CFKRS recipe
output, Petersson + sym² link — turns out to require, somewhere in
the chain, exactly the same conjectural input.

This is structurally unsurprising: the seven direct attacks failed at
the same wall (4-level density / per-form GRH). The contrarian /
proof-by-contradiction strategy attacks the same wall from the other
side, and predictably hits the same obstruction.

---

# Section 4. If yes (contradiction works) — N/A

This section is empty. No route in §1 produced a genuine contradiction.

---

# Section 5. If no (no contradiction) — what this means

**2/(3π) is genuinely conditional**, in the strong sense that:

(a) The cage [(17−√145)/(12π), (17+√145)/(12π)] = [0.131, 0.452] is the
    only unconditional pinch on A.
(b) Any A in this cage interval is consistent with all unconditional
    results currently known: 1-level density, 2-level density (with
    support restriction), Petersson trace formula, on-line second moment,
    RMT prediction (which does not transfer unconditionally to L-side).
(c) The specific value 2/(3π) ≈ 0.2122 is RMT-predicted, CFKRS-recipe-output,
    and symbolic-verification-confirmed (the recipe's internal arithmetic
    gives this number) — but the recipe itself requires conjectural input
    that is not currently unconditionally established.

**This is consistent with M-N (2014)'s own honest statement** (verbatim,
quoted in `RMT_Painleve_GRH_bypass.md` Appendix B):

> "this result appears to be unattainable using current techniques without
> some significantly new ideas. ... we expect that some substantially new
> ideas are necessary in order to establish the above conjecture for the
> second moment of L'(ρ_f, f)."

---

# Section 6. Honest verdict + confidence

**Verdict.** The contrarian / reductio strategy fails. Assuming
A ≠ 2/(3π) does NOT lead to a contradiction with any unconditionally
proved statement. The conjecture's truth is genuinely conditional.

**Per-route confidence in obtaining a contradiction:**

| Route | Brief description | Confidence |
|---|---|---|
| 1 | Higher-moment incompatibility | 0.02 |
| 2 | Functional equation rigidity | 0.03 |
| 3 | On-line ↔ at-zero consistency | 0.05 |
| 4 | Petersson + sym² link | 0.03 |
| 5 | RMT uniqueness (Hughes-Snaith / CRS) | 0.04 |
| 6 | Numerical at large T | 0.01 |
| 7 | Beilinson-Deligne motivic uniqueness | 0.01 |

**Aggregate confidence** that ANY of the seven contrarian routes produces
an unconditional proof by contradiction: **≤ 0.05**. (Aggregate is not
a sum because the routes are largely correlated — they all hit the
4-level-density / partial-GRH wall.)

**Implication for the two-paper plan.**

- Theorem B-exact (constant 2/(3π)) **stays GRH-conditional** as a
  headline theorem. The eight independent attacks (seven direct +
  one contrarian) provide strong evidence that no easy bypass exists.
- Theorem B' (cage, [0.131, 0.452]) **stays unconditional**.
- The numerical, RMT, CFKRS-symbolic, and on-line results provide
  **converging evidence** that the actual constant is 2/(3π), not
  some other value in the cage — but this is evidence, not proof.
- **Honesty in publication**: the cage is the strongest unconditional
  statement; the exact 2/(3π) is conditional; the conditioning is
  on n-level density at n ≥ 3 with full Schwartz support, equivalently
  per-form GRH-on-average to a strength stronger than current
  Kowalski-Michel.

**Final confidence on the contrarian-route outcome: 0.95** that the
contrarian strategy genuinely fails (i.e., no contradiction exists),
given that all eight independent attacks converge on the same wall and
the wall is structurally tied to a known-open problem in analytic
number theory.

---

# Caveats / what was NOT done

1. **No new computation was launched.** The audit relies on existing
   project files for the seven direct attacks, plus the project's
   on-line second-moment file `B3_*RIGOROUS.md`, plus the CFKRS
   symbolic-verification file. No PARI / sympy / mpmath computation
   was performed in this audit — which is appropriate since the
   contrarian attack is *structural*, not computational. Numerical
   re-verification of 2/(3π) is already in the project's B2 files
   (separate effort).
2. **The Beilinson-Deligne route (Route 7)** could in principle be
   pushed further by an expert in motivic theory; this audit
   relegates it to a low-confidence route based on the known
   conditional status of Beilinson's conjecture for L'(½, f).
3. **No claim is made that the seven failed direct attacks are
   exhaustive.** A genuinely new idea (M-N's "substantially new
   ideas") could in principle bypass the wall. The audit only
   establishes that *the contrarian strategy*, applied to the
   currently known toolkit, does not produce a contradiction.

# Done.
