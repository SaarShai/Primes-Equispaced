# Route IV — the family-isolation dichotomy (correction to the log headline)

**Date**: 2026-05-14
**Status**: CORRECTION — referee-grade
**Scope**: Whether Route IV (Petersson/Kuznetsov trace formula) is a genuine
exception to "every route to unconditional offcentral H1 for fixed `E/Q`
reduces to TSDB (or its negative-moment-over-family sibling)".

---

## 0. The claim under audit

`log.md` 2026-05-14, line 1292 (strategic summary):

> Route IV (Petersson/Kuznetsov trace formula) gives **unconditional
> family-averaged H1**. The obstruction to fixed-E unconditional is
> **paper-architecture (isolating fixed E from the family), not GL2 zero
> location**.

This headline says the Route IV obstruction is *non-analytic*. That makes
Route IV the lone apparent exception to the session's reduction theorem.

## 1. Verdict

**The headline is an overclaim.** It contradicts its own underlying audit
(`OFF_HALO_UNCONDITIONAL_PIVOT_2026-05-14.md` §5.2, §5.5, lines 373,
832–838), which correctly concludes "family-averaged H1 only — no fixed-E
unconditional handle — punt to Route X." The obstruction to isolating a
fixed `E` is **analytic**, not paper-architecture. Route IV is **not** an
exception: it reduces, via the dichotomy below, to TSDB or to a
negative-moment-over-family statement of the same depth.

This is the **fourth instance today** of one recurring error pattern: an
apparent unconditional escape hatch that collapses once the analytic
content is tracked honestly (cf. the three silent GRH dependencies, and
the density method's "illusory positivity advantage" — same `log.md`).

## 2. The family-isolation dichotomy

The Petersson trace formula over `B_k(N)` yields a sub-trivial bound for
an averaged object **only if the family is asymptotically large** — the
off-diagonal (Kloosterman + Bessel) terms beat the diagonal only as
`k → ∞` or `N → ∞`. Fix an elliptic curve `E/Q` of conductor `N_E`.
`f_E ∈ B_2(N_E)` sits in a family of size `O_E(1)`. Two horns:

**Horn A (small/fixed family containing `E`).**
`B_2(N_E)` has fixed finite size. The Petersson identity is then a finite
identity with **no asymptotic cancellation**. Bounding the fixed-`E` term
`R_Φ^{f_E}(T)` by the (finite, signed) family sum gives nothing better
than the term itself: no unconditional gain. One is back to the pointwise
problem ⇒ **reduces to TSDB**.

**Horn B (family enlarged for trace-formula savings, `N → ∞`).**
Now `f_E` is one form among `≍ N` newforms. A family-averaged bound
`Σ_f h_f R_Φ^f(T) ≪ B_avg(T)` isolates the fixed-`E` term only via

```
R_Φ^{f_E}(T)  ≤  h_{f_E}^{-1} · B_avg(T),
```

and the harmonic Petersson weight at a fixed form satisfies
`h_{f_E}^{-1} ≍ N^{1+o(1)}` as the family grows (pivot audit lines
832–838: "at least `N_E^{1/2}` worse than family-averaged", and in fact
the controlling loss is the full `N`-power as `N → ∞`). The fixed-`E`
conclusion is then `o(T^2)` **iff** `B_avg(T) = o(T^2 / N)` — a
**negative-moment-over-family** statement strictly stronger than the bare
family average, and not delivered by Petersson/Kuznetsov (which controls
`Σ_f λ_f(m)λ_f(n)`, the *positive* arithmetic side, not
`Σ_f 1/L_f^*{}'(ρ_f)`, a *negative discrete moment at zeros* — pivot
audit line 373: "this is **not** a Petersson-type sum"). That required
input is itself open, of the same depth as TSDB.

**Neither horn is paper-architecture.** Horn A is the analytic statement
"no cancellation in a fixed family"; Horn B is the analytic statement "a
negative-moment-over-family bound at the `T^2/N` threshold is unproven."
The two horns are exhaustive (family is either bounded or unbounded in
conductor), so:

> **Route IV reduces to TSDB (Horn A) or to a negative-moment-over-family
> problem of TSDB-depth (Horn B). It is not an exception.**

## 3. Why the positivity drop does not rescue Horn B

The only standard way to extract a single term from a large-family average
is positivity ("drop all `f ≠ E`, each term ≥ 0"). It fails twice here,
both analytically:

1. `R_Φ^f(T)` is a **signed** contour-residue aggregate — not term-wise
   non-negative — so the drop is invalid for the native object.
2. The absolute surrogate `R_B^f(T) ≥ 0` admits the drop, but yields a
   *lower* bound on `Σ_f R_B^f`, whereas H1 needs an *upper* bound on the
   single `R_B^{f_E}`. Converting requires a family **lower** bound that
   is "itself not known" (pivot audit §5.2) — again analytic, not
   architectural.

(Conrey–Iwaniec cubic moment, pivot audit §5.3, is orthogonal: it bounds
`|L(f,1/2)|^3` — a positive central value — and is silent on
`Σ_ρ 1/L_E^*{}'(ρ)`. Not a route to H1.)

## 4. Net effect on the reduction theorem

With the Route IV headline corrected, the session's reduction theorem has
**no surviving exception**:

> Every surveyed route (I, II, III, **IV**, V, VI, VII, VIII, IX, X.1) to
> an unconditional sub-`T^2` bound on `R_Φ(T)` for fixed `E/Q` either
> (i) reduces to thin-strip critical-line density (TSDB) for `L_E^*`,
> (ii) reduces to its negative-moment-over-family sibling of equal depth
> (Route VI t-aspect; Route IV Horn B), or
> (iii) bounds the wrong object / has no framework (V, IX).

The reduction theorem is therefore **status-complete**: there is no known
route, full stop. This *strengthens* the paper-worthy companion result —
the conditional halo theorem `R_Φ(T) ≪ T^{7/4+ε}` under GRH stands as the
genuine positive deliverable; the unconditional bound is open at a single
identified obstruction with no escape hatch.

Confidence the dichotomy is exhaustive and both horns are analytic: **0.9**
(Horn A is elementary; Horn B's `h_{f_E}^{-1} ≍ N` weight loss and the
"not a Petersson-type sum" obstruction are both in the underlying audit).

## 5. Action

`log.md` line ~1292 headline "obstruction is paper-architecture, not
analysis" is **superseded** by this note. The corrected one-liner:

> Route IV gives family-averaged H1 only; isolating fixed `E` faces the
> family-isolation dichotomy (no cancellation in a fixed family ⇒ TSDB; or
> a negative-moment-over-family bound at the `T^2/N` threshold, itself
> open). **Analytic, not paper-architecture. Not an exception.**
