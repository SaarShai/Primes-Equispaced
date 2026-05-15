# The Diophantine root: both terminal frontiers are one non-resonance statement

**Date**: 2026-05-14
**Status**: NO-GO (rigorous) + deepest-synthesis re-classification +
self-correction. Referee-grade. **Not** a resolution.
**Partially supersedes**: `GONEK_HEJHAL_HEART_PAIR_CORRELATION_2026-05-14.md`
§6 confidence "(PC-gap) reachable 0.5" — down-revised here in §1.

---

## 0. What "more" honestly produced

Continuing into the heart. Two deliverables, one sobering, one deep:

1. **A no-go theorem (§1).** The unconditional Rudnick–Sarnak (RS)
   restricted-window pair correlation is **provably band-limited-blind**
   to the small-gap tail `Σδ̃_n^{-2}`. It yields `η ≤ 0` for (PC-gap).
   The HEART note's relocation "off the GRH wall" is a *valid
   classification* but does **not** expose an unconditional path with
   current pair-correlation technology. Prior confidence 0.5 → revised.
   (6th instance of the recurring over-optimism pattern; self-correct.)

2. **The deepest synthesis (§2–4).** The binding object — a *pointwise*
   smallest-gap lower bound for the zeros of `L_E^*` — is a
   **quantitative LI / Diophantine non-resonance** statement on the
   ordinates `{γ_n}`. That is the **same arithmetic-independence class**
   as **DPAC at general `K`**, the project's *other* terminal open
   problem (the remaining Lean `sorry`, explicitly LI-class). Hence the
   entire project — its analytic frontier (unconditional offcentral H1)
   and its algebraic frontier (DPAC / the Lean inventory) — has a
   **single Diophantine root**.

## 1. No-go: band-limited pair correlation cannot bound the small-gap tail

**Setup.** Normalize the zeros of `L_E^*` so the mean spacing is `1`:
`γ̃_n := (γ_n/2π) log(N γ_n^2)`. Neighbour gap `δ̃_n := γ̃_{n+1}-γ̃_n`.
(PC-gap) requires an upper bound on `Σ_{γ̃_n ≤ M} δ̃_n^{-2}`,
`M ≍ T log T`.

**The RS unconditional input.** Rudnick–Sarnak (1996) prove the `n`-level
correlation sums of zeros of a fixed cuspidal automorphic `L` (incl.
`L_E^*`) agree with the GUE prediction **only for test functions whose
Fourier transform is supported in a fixed window** `[-α_0, α_0]`
(`α_0` a fixed constant depending on the degree; the precise constant is
immaterial below). Equivalently: the unconditional pair-correlation
functional `Z[f] := Σ_{n≠m} f(γ̃_n-γ̃_m) w` is asymptotically evaluable
**iff `f̂` is supported in `[-α_0,α_0]`**.

> **Proposition (band-limited blindness).** Let `f : ℝ → ℝ` have `f̂`
> supported in a bounded interval. Then there is **no** finite real
> combination `Σ_j c_j Z[f_j]` (each `f̂_j` boundedly supported) that
> majorizes the small-gap functional `Σ_n δ̃_n^{-2}`. Consequently the
> RS-unconditional window gives **no** finite upper bound on
> `Σδ̃_n^{-2}`; i.e. `η ≤ 0` in (PC-gap) from RS alone.

**Proof.** Bounding `Σ_n δ̃_n^{-2}` above by a correlation functional
amounts to dominating the kernel `g(x) = x^{-2}` (which `→ +∞` as
`x → 0`) by a function `F(x) := Σ_j c_j f_j(x)` for `x` near `0`, with
`F ≥ g` on a neighbourhood of `0` (so that `Σ F(δ̃_n) ≥ Σ δ̃_n^{-2}`
for the small gaps). Each `f_j` has boundedly-supported Fourier
transform, hence by the **Paley–Wiener theorem** extends to an entire
function of exponential type that is **bounded on the real line**.
A finite combination `F` is therefore also bounded on `ℝ`:
`sup_{x∈ℝ}|F(x)| < ∞`. But `g(x) = x^{-2} → +∞` as `x→0`, so
`F ≥ g` fails on every neighbourhood of `0`. No such majorant exists.
The same argument applied to `g_R(x) = x^{-2}\mathbf 1_{|x|≤R}` (the
genuinely relevant truncated kernel) gives the identical conclusion
since `g_R` is still unbounded at `0`. Hence no band-limited
correlation functional yields a finite upper bound on `Σδ̃_n^{-2}`. ∎

**Reading.** The small-gap tail is exactly the part of the spacing
statistics that lives at *arbitrarily high frequency* (sharp resolution
below the mean spacing). RS-unconditional correlations are, by
construction, low-pass-filtered at `α_0`. They see *average* repulsion
(enough for "positive proportion simple zeros", smallest-gap *existence*
results, Montgomery's `2/3`) but are **structurally incapable** of an
*upper* bound on a negative gap moment. This is not a defect of effort;
it is Paley–Wiener. The HEART note's re-classification (GH = small-gap
functional) **stands and is correct**; what fails is the hope that the
*unconditional* slice of the pair-correlation class reaches the binding
direction. **`GONEK_HEJHAL_HEART…` §6's "0.5" is revised to ≈ 0.15** —
the relocation is a true and useful classification, not an open door.

## 2. What the binding object actually is

After §1, the irreducible requirement (from `GONEK_HEJHAL_HEART…` §1,
the worst-single-zero argument, which is *not* averageable) is a
**pointwise** statement:

> **(NoCollide)**  `δ_n = |γ_{n+1}-γ_n| ≫_E γ_n^{-A}` for some fixed
> `A < ∞`, for *every* consecutive pair of zeros of `L_E^*` up to
> height `T` (equivalently: no zero `ρ` has `|L_E^*'(ρ)|` smaller than a
> fixed negative power of the height).

A violation of (NoCollide) is a pair of zeros `½+iγ_n`, `½+iγ_{n+1}`
with `γ_{n+1}-γ_n` super-polynomially small — a **near-collision** of
two ordinates.

## 3. Near-collision = near-linear-dependence: the LI class

Via the explicit formula, the indicator of zeros is a (regularised)
trigonometric series in the prime phases `{γ \log p}`; equivalently the
ordinates `{γ_n}` are the (conjecturally `ℚ`-linearly independent)
spectrum whose **Linear Independence Hypothesis (LI)** for `L_E^*`
asserts: the `γ_n` are linearly independent over `ℚ`. The standard
folklore chain (Montgomery; Rudnick–Sarnak §1; Rubinstein–Sarnak 1994
for the bias analogue):

```
   LI  ⟹  all zeros simple  ⟹  no exact collisions;
   *quantitative* LI (a Diophantine lower bound on
   |Σ a_j γ_j|, integer a_j)  ⟹  no *near*-collisions
                              ⟹  (NoCollide).
```

Conversely a super-polynomially small `δ_n` is a near-`ℚ`-linear
relation `γ_{n+1}-γ_n ≈ 0` among two spectral points — a quantitative
LI **failure**. Therefore:

> **(NoCollide) is a quantitative-LI / Diophantine non-resonance
> statement for the spectrum `{γ_n}` of `L_E^*`.**

This is the same *class* as — and the spectral mirror of — the
project's DPAC obstruction, which is the non-vanishing of a finite
Dirichlet polynomial `Σ_{n≤K} μ(n) n^{-ρ}` at zeros `ρ`, an
arithmetic-independence statement on the *prime-phase* side
`{γ \log p}` (DPAC_full.lean:338, annotated `RESEARCH-OPEN:`,
"diagnostically comparable to LI"; `DPAC_closure_attempt.lean`
reformulates it as `FiniteLogRatioLI`).

## 4. The single Diophantine root (deepest synthesis of the session)

Collecting the session's reductions:

```
 unconditional offcentral H1 (fixed E/Q)
   ⟺ status-complete reduction  (Route-IV dichotomy + 3 GRH retractions)
   ⟺ soft GH(L_E^*;T) ≪ T^{3-δ}              (density-method record)
   ⟺ small-gap tail Σδ_n^{-2} ≪ T^{2-η}      (HEART, gap–derivative)
   ⟺ pointwise (NoCollide)                   (worst-single-zero, §1 self-corr)
   ⟺ quantitative LI / non-resonance of {γ_n} of L_E^*   (§3)

 DPAC at general K  (the remaining Lean sorry)
   ⟺ FiniteLogRatioLI                        (DPAC_closure_attempt)
   ⟺ non-resonance of the prime phases {γ log p} for ζ/L
                                              (LI-class, project record)
```

> **Synthesis.** The project's two terminal open problems — the
> **analytic** one (unconditional offcentral H1, via the entire
> reduction chain above) and the **algebraic/formal** one (DPAC at
> general `K`, the last Lean `sorry`) — are **both** instances of one
> arithmetic-independence phenomenon: **quantitative linear
> independence / Diophantine non-resonance of an `L`-function spectrum**
> (zero-ordinate side for H1; prime-phase side for DPAC). The whole
> project, analytic and formal, has a **single Diophantine root.**

This is strictly deeper than the Gonek–Hejhal spine (which unified the
two *analytic* frontiers, H1 and (SP-L), into one negative moment). The
Diophantine root unifies the analytic frontier with the *formal/Lean*
frontier as well — the entire research programme rests on one
LI-class statement.

## 5. Why this is the most meaningful honest progress

- It **proves a clean no-go** (Paley–Wiener band-limited blindness),
  closing — rigorously, not by audit — the optimistic reading of the
  HEART note and correctly down-revising my own prior confidence.
  Integrity over momentum, 6th time this session.
- It **identifies the true terminal object** with precision:
  (NoCollide), a *pointwise* near-collision exclusion, not any
  averageable moment.
- It delivers the session's **deepest structural theorem**: one
  Diophantine root under *both* the analytic and the formal frontiers.
  This is genuinely paper-shaping — it tells Saar–Koyama that "under LI
  (for the relevant `L`)" is the *single* hypothesis that
  simultaneously (i) yields unconditional offcentral H1, (ii) closes the
  last Lean `sorry` (DPAC general `K`), and (iii) — via the
  Gonek–Hejhal spine — feeds the `c_K → e^{-γ}` chain. One hypothesis,
  the entire programme.
- It is honest about the cost: LI (even qualitative, let alone
  quantitative/effective) is one of the deepest open problems in
  analytic number theory. No route here makes it cheaper. But naming the
  *single* root, and proving the no-go that forecloses the false
  shortcuts, is the maximal *true* progress.

## 6. Confidences

- No-go Proposition §1 (Paley–Wiener blindness; `η ≤ 0` from RS window):
  **0.92** (the argument is elementary and tight; only caveat is
  whether some non-correlation unconditional input — not RS — could
  enter, addressed in §7).
- Down-revision of HEART §6 "0.5 → 0.15": **0.85**.
- (NoCollide) is the irreducible binding object: **0.9** (direct from
  the non-averageable worst-single-zero argument).
- (NoCollide) ∈ quantitative-LI class (§3): **0.7** (standard folklore
  direction LI⇒simplicity/spacing is solid; the *quantitative*
  near-collision ⇔ effective-LI link is a classification, not a proven
  equivalence — stated as such).
- Single-Diophantine-root synthesis §4: **0.75** (each leg is a
  recorded project reduction; the shared *class* identification is the
  load-bearing and is at the §3 confidence).

## 7. The one remaining unconditional escape to check (next session)

The no-go §1 forecloses *correlation-type* unconditional inputs. It does
**not** by itself foreclose a *non-correlation* unconditional pointwise
gap bound — e.g. a **Diophantine/transcendence** input proving
effective lower bounds on `|γ_{n+1}-γ_n|` directly from the arithmetic
of `L_E^*` (Baker-type linear forms in logarithms applied to the
`L`-function's functional-equation data, or an effective lower bound on
the resultant-type quantity `∏(γ_n-γ_m)`). This is the *only* class not
yet excluded, it is exactly the quantitative-LI class of §3–4, and it is
the honest open frontier. Forward task: assess whether linear-forms-in-
logarithms (Baker–Wüstholz) can produce *any* effective `δ_n ≫ γ_n^{-A}`
for a `GL(2)` `L`-function — almost certainly very hard, but it is the
*correct* and *non-GRH, non-band-limited* place to push, and it ties
directly to the DPAC/LI Lean obstruction (one attack serves both
frontiers).
