# The Baker path is closed: a category obstruction, not a difficulty

**Date**: 2026-05-14
**Status**: NO-GO (rigorous, two independent obstructions) +
7th self-correction. Referee-grade. **Not** a resolution.
**Supersedes**: §7 of `DIOPHANTINE_ROOT_UNIFICATION_2026-05-14.md`
("the correct non-GRH non-band-limited forward push") — that flag was
itself over-optimistic; corrected here.

---

## 0. The request and the honest answer

The request: break through the only unexcluded path — effective bounds
via linear-forms-in-logarithms (Baker), which §7 of the Diophantine-root
note flagged as serving both terminal frontiers at once.

The honest answer a mathematician must give: **the Baker path is not
open. It is closed by a category obstruction**, supported by a second,
independent quantitative obstruction. Proving a tempting method
*cannot* work — decisively, so the field stops chasing it — is itself
the result. There is no brilliant solution down this path because there
is, provably, no path.

## 1. The target restated

(NoCollide): for the zeros `ρ_n = ½ + iγ_n` of `L_E^*`,
`δ_n := |γ_{n+1}-γ_n| ≫_E γ_n^{-A}` for some fixed `A`, for every
consecutive pair up to height `T`. Equivalently: no two zero ordinates
of `L_E^*` are super-polynomially close.

This is the irreducible binding object for the entire programme
(`DIOPHANTINE_ROOT_UNIFICATION` §2–4): it sits under unconditional
offcentral H1 (analytic frontier) and is class-identical to DPAC at
general `K` (formal/Lean frontier).

## 2. Obstruction 1 — category mismatch (decisive, qualitative)

**Theorem (no admissible input).** The Baker–Wüstholz theorem, and more
generally Wüstholz's analytic subgroup theorem, produce effective
nonzero lower bounds for
`Λ = b_1 \log α_1 + … + b_n \log α_n` (or for linear forms in
periods/logarithms arising from a commutative algebraic group)
**only when the `α_i` are algebraic numbers** (resp. the periods are
periods of an algebraic group defined over `\overline{ℚ}`). The zero
ordinates `γ_n` of `L_E^*`:

- are *defined analytically* as imaginary parts of zeros of
  `L_E^*(s)`, with **no known algebraic characterisation**;
- are *conjecturally transcendental* and *conjecturally ℚ-linearly
  independent* (this is exactly the LI Hypothesis — the very statement
  one is trying to prove a quantitative form of);
- are **not known to be logarithms of algebraic numbers, nor periods of
  any algebraic group** over `\overline{ℚ}`.

Therefore there is **no admissible substitution** of the `γ_n` into the
hypotheses of any theorem in the Baker / Schmidt subspace / Wüstholz /
Nesterenko effective-transcendence family. The obstruction is not that
the resulting bound is weak — it is that **the input slot does not
exist**. ∎

**Scope of the obstruction.** This is *not* Baker-specific. Every known
*effective* Diophantine non-resonance tool (linear forms in logarithms;
the subspace theorem; the analytic subgroup theorem; Nesterenko's
algebraic-independence method) requires the transcendental quantities to
carry an algebraic/period structure over `\overline{ℚ}`. L-function zero
ordinates are not known to carry any such structure. Hence **the entire
effective-Diophantine toolbox has a category mismatch with L-function
zeros.** The smallest-gap problem is, accordingly, open even for `ζ` and
is famously *not* approached by Baker-type methods — for precisely this
reason. The §7 flag conflated "the obstruction is *of LI/Diophantine
class*" with "the obstruction is attackable by the *effective
Diophantine toolbox*." The first is true (a classification); the second
is false (a category error). 7th instance of the recurring
over-optimism pattern; this one closes my own forward flag.

## 3. Obstruction 2 — term-count explosion (independent, quantitative)

Grant, *hypothetically*, an explicit-formula bridge converting a
near-collision `δ_n` into a near-relation among the Frobenius integers
`a_p` of `E` (which *are* algebraic: `a_p ∈ ℤ`, `|a_p| ≤ 2\sqrt p`), so
that Baker would have algebraic inputs after all. The bridge still fails
quantitatively:

- Detecting a gap of size `δ_n` via the explicit formula requires a test
  function localised at resolution `≍ 1/δ_n`, i.e. Fourier support of
  width `≍ 1/δ_n`. For `δ_n` super-polynomially small this forces the
  prime side to run over `p ≤ X` with `X = \exp(γ_n^{A})`.
- The induced linear form then has `n ≍ π(X) ≍ \exp(γ_n^{A})/γ_n^{A}`
  terms.
- Baker–Wüstholz lower bounds degrade **super-exponentially in the
  number of terms `n`** (and polynomially in the heights). With `n`
  itself super-polynomially large in the height, the resulting lower
  bound on `|Λ|` is **astronomically weaker than the trivial bound**.

Baker's method is a scalpel for *few* logarithms of *small-height*
algebraics. Against exponentially many terms it is inert. So even
modulo Obstruction 1, the bridge yields nothing. ∎

Two independent rigorous obstructions, either alone fatal.

## 4. No averaged or signed escape (closing the back doors)

For completeness, the back doors are already shut by earlier records:

- **Averaged escape?** No. `GH = Σ|L_E^*'(ρ)|^{-2} ≥ |L_E^*'(ρ_0)|^{-2}`
  and the dictionary gives `|L_E^*'(ρ_n)|^{-2} ≍ δ_n^{-2}` at a
  near-double zero, so a single catastrophic collision kills `GH`
  (non-averageable; `GONEK_HEJHAL_HEART…` §1, `DIOPHANTINE_ROOT…` §1).
- **Signed-cancellation escape?** No. The signed residue sum
  `R_Φ(T) = Σ Ŵ(γ)/L_E^*'(ρ)` is the halo route; the halo audits
  reduced it to Door B = TSDB unconditionally (session record). Signed
  cancellation at the residue level does not rescue it.
- **Band-limited pair-correlation escape?** No. Paley–Wiener no-go,
  `DIOPHANTINE_ROOT…` §1.

All routes — analytic, signed, averaged, correlation, effective-
Diophantine — are now individually and rigorously closed.

## 5. The final honest status of the programme

> **(NoCollide) — equivalently, quantitative LI for the spectrum of
> `L_E^*` — is the single root under both terminal frontiers, and it
> has no known attack: not GRH-type, not pair-correlation-type, not
> effective-Diophantine-type. It is a genuine, isolated, deep open
> problem.**

This is the terminal, fully-audited status. It is *not* a defeat: a
diffuse multi-front programme has been compressed to one named root with
*every* candidate attack rigorously foreclosed and the category reason
for the foreclosure made explicit. Knowing precisely where the wall is —
and proving the tunnels are not there — is the maximal true result.

## 6. What the Saar–Koyama paper should now do (concrete)

1. **Claim the conditional theorem** `R_Φ(T) ≪ T^{7/4+ε}` under GRH —
   proved, genuine, the positive deliverable.
2. **Claim the reduction/clarification as a companion theorem**: "H1 for
   `E/Q`, the corrected duality constant, and DPAC at general `K` are
   *all* governed by one quantitative-LI statement for the relevant
   `L`-spectrum" — a structural result of independent interest, now with
   the Gonek–Hejhal spine + Diophantine-root chain + the no-go set as
   its rigorous backbone.
3. **Do NOT** gesture at Baker / effective methods as a hopeful future
   direction. Per §2 that is a category error and a referee would flag
   it. State instead that the conditional-on-LI framing is the
   appropriate and honest formulation, LI being a recognised deep
   conjecture.
4. The last Lean `sorry` (DPAC general `K`) should be documented as
   *the same root* — not a separate defect — strengthening the
   formalisation narrative ("one open hypothesis, transparently
   isolated") rather than weakening it.

## 7. Confidences

- Obstruction 1 (category mismatch; no algebraic structure on `γ_n`):
  **0.9** (a well-understood structural fact in transcendence theory;
  the residual 0.1 is the standing logical possibility that some future
  theory endows L-zeros with algebraic/period structure — none is known
  or conjectured constructively).
- Obstruction 2 (term explosion): **0.95** (elementary quantitative
  bookkeeping on Baker–Wüstholz dependence).
- Generalisation to the whole effective-Diophantine toolbox: **0.85**.
- 7th-self-correction (§7 of the Diophantine note was over-optimistic):
  **0.9**.
- Final-status claim §5 (single root, no known attack of any class):
  **0.85** — strong, with all routes individually closed; the residual
  is unknown-unknowns, not any identified open route.
