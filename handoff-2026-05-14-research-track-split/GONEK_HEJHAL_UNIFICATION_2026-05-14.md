# The Gonek–Hejhal spine: a single conjecture under both open frontiers

**Date**: 2026-05-14
**Status**: STRUCTURAL THEOREM (reduction + unification) — referee-grade
**Type**: clarifying result for the joint Saar–Koyama paper. Not a
resolution of any open problem; a proof that the paper's two distinct
open analytic inputs are *the same object* at two degrees.

---

## 0. Why this is the highest-value honest move

Today's audit arc proved the H1 reduction theorem is **status-complete**:
every surveyed route to unconditional offcentral H1 for fixed `E/Q`
reduces to thin-strip critical-line density (TSDB) for `L_E^*`, with no
surviving exception (Route IV family-isolation dichotomy, this folder).
Separately, the (SP-L) note (`SP_L_SUFFICIENT_PACKAGES_2026-05-13.md`)
records that the cleanest sufficient package for the shifted Perron
leading theorem — feeding the corrected `B_∞`/`c_K` chain and hence
Appendix A — is a Gonek–Hejhal-type negative second moment for Dirichlet
`L`.

These two facts live in separate notes and have never been stated
together. Doing so is a genuine theorem-grade clarification: it collapses
the joint paper's analytic surface from **two independent open inputs**
to **one named classical conjecture with two instantiations**. This is
the kind of structural statement that strengthens a paper without
claiming anything unproven as proved.

## 1. The two frontiers, normalized to a common object

Write, for an entire `L`-function `Λ` of degree `d` with nontrivial
zeros `ρ = β + iγ`, the **Gonek–Hejhal negative second moment**

```
                       GH(Λ; T)  :=  Σ_{ρ : 0 < γ ≤ T}  |Λ'(ρ)|^{-2}.
```

(For a zero of multiplicity `>1`, `Λ'(ρ)=0` and the term is excluded /
the statement is read on simple zeros; both frontiers already restrict
to the simple-zero stratum — H1 via the two-zero gadget, (SP-L) via the
off-target-simplicity hypothesis (I.a).)

**Frontier H1 (GL(2), `Λ = L_E^*`, t-aspect, `T → ∞`).**
`UNCONDITIONAL_DENSITY_METHOD_2026-05-14` (index l.63) records that
unconditional offcentral H1 for fixed `E/Q` requires exactly

```
        (H1-input)        GH(L_E^*; T)  ≪_E  T^{c},   some  c < 3.
```

The status-complete reduction theorem says: **no surveyed route avoids
(H1-input)** — it is the unique analytic obstruction.

**Frontier (SP-L) (GL(1), `Λ = L(·,χ)`, fixed `χ`, height `T_K`).**
`SP_L_SUFFICIENT_PACKAGES_2026-05-13` §Route I records that (SP-L)
closes given off-target simplicity (I.a) plus the clean substitute (I.b′)

```
        (SPL-input)       GH(L(·,χ); T)  ≪_χ  T (log T)^{O(1)}.
```

(The note's primary (I.b) is a shifted variant `Σ|L(ρ'+α,χ)|^{-2}`; its
own stated clean substitute is precisely the unshifted Gonek–Hejhal
object above, via Cauchy–Schwarz against the `1/|γ'-τ|` weight.)

## 2. The unification theorem

> **Theorem (Gonek–Hejhal spine).** The joint paper's two open analytic
> frontiers are instantiations of a single conjecture — control of the
> Gonek–Hejhal negative second moment `GH(Λ; T)` — at two degrees:
>
> - the offcentral-H1 frontier is the **GL(2)** instantiation
>   `Λ = L_E^*`, requiring the *soft* bound `GH ≪_E T^{c}` for some
>   `c < 3`;
> - the (SP-L) / corrected-`B_∞` frontier is the **GL(1)** instantiation
>   `Λ = L(·,χ)`, requiring the *sharp* bound
>   `GH ≪_χ T (log T)^{O(1)}`.
>
> Consequently the paper has a **single analytic spine**: a uniform
> Gonek–Hejhal conjecture `GH(Λ;T) ≪_Λ T (log T)^{O(1)}`. Its sharp form
> closes (SP-L) (GL(1)); any sub-cubic form `c < 3` closes H1 (GL(2)).

**Proof.** Immediate from the two recorded reductions of §1: (H1-input)
and (SPL-input) are the same functional `GH(·;T)` evaluated at
`L_E^*` and `L(·,χ)` respectively. The H1 reduction's status-completeness
(no surviving route) is established in this folder's audit chain
(three GRH-dependency retractions + Route IV dichotomy). The (SP-L)
reduction is `SP_L…` §Route I. ∎

The content of the theorem is not the algebra (trivial) — it is the
*identification*: two problems that the project tracked as independent
("GL(2) zero density" vs. "Dirichlet shifted moment") are one.

## 3. The strength gradient — stated honestly, not flattened

The two instantiations are the **same object at different strengths**,
and conflating the strengths would repeat exactly the error class this
session has caught four times today. Precisely:

| Frontier | Degree | Aspect | Required strength on `GH(Λ;T)` | Hardness |
|---|---|---|---|---|
| H1 | 2 (`L_E^*`) | t-aspect, `T→∞` | any `≪ T^{3-δ}` | softer |
| (SP-L) | 1 (Dirichlet) | height `T_K`, `K→∞` | sharp `≪ T(log T)^{O(1)}` | harder |

So (SP-L) is the **harder** instantiation (it needs the Gonek–Hejhal
*exact* envelope, the `c → 1` end), and H1 the **softer** (any
sub-cubic exponent). For `ζ`, `GH(ζ;T) ≍ T(log T)^{?}` is the classical
Gonek–Hejhal conjecture, unconditionally known only in restricted
ranges and RH-strength-or-beyond in full; both instantiations inherit
this status. **Neither is proved here.** The theorem is a *reduction and
unification*, explicitly not a resolution.

## 4. What this buys the paper (concretely)

1. **§X.7 (Q:Perron) and the H1/§X.4 discussion** can cite a *single*
   named conjecture (Gonek–Hejhal negative second moment) instead of two
   bespoke "sufficient packages." Referees recognize Gonek–Hejhal; they
   do not recognize "Dirichlet shifted negative second moment summed
   over zeros at a zero-avoiding height."
2. **The conditional results become uniform**: "under the Gonek–Hejhal
   conjecture for the relevant `L`-function" simultaneously delivers the
   sharp `c_K → e^{-γ}` chain (GL(1)) *and* unconditional offcentral H1
   (GL(2), via the soft form, which the GRH-conditional halo theorem
   `R_Φ ≪ T^{7/4+ε}` already over-delivers — see remark below).
3. **The companion theorem writes itself**: "Offcentral H1 for fixed
   `E/Q` and the corrected duality constant are governed by one
   conjecture" is a crisp abstract-worthy sentence; the status-complete
   reduction is its proof.

**Remark (the GRH bookkeeping).** The halo theorem already gives
`R_Φ(T) ≪ T^{7/4+ε}` under standing GRH for `L_E^*`. GRH ⇒ all `β=1/2`,
which is *not* itself `GH ≪ T^{3-δ}`; the halo route reaches `7/4`
through the two-zero gadget + Door A/B under GRH, a *different* and
*stronger-in-exponent* conditional path than the bare Gonek–Hejhal soft
form. So the paper's honest conditional menu is:
(i) under GRH: `R_Φ ≪ T^{7/4+ε}` (halo, proved);
(ii) under the soft Gonek–Hejhal form `GH(L_E^*;T) ≪ T^{c}, c<3`:
unconditional-on-GRH H1 `= o(T^2)` (weaker exponent, but removes the
GRH-shaped hypothesis in favour of a single named moment conjecture);
(iii) under sharp Gonek–Hejhal for Dirichlet `L`: the `c_K → e^{-γ}`
chain. Items (ii) and (iii) are the **same conjecture** at GL(2)/GL(1).

## 5. Confidence and scope

- Identification (§2) — that both inputs are `GH(·;T)`: **0.97**
  (direct from two existing project records; algebra trivial).
- Status-completeness of the H1 leg (no surviving route): **0.9**
  (today's audit chain + Route IV dichotomy).
- That (SP-L)'s clean substitute is exactly the unshifted GH object:
  **0.9** (`SP_L…` §Route I states the Cauchy–Schwarz reduction
  explicitly; the shift `α` is absorbed at the cost the note records).
- The strength gradient (§3) is **not** an artefact to be optimized
  away: it is intrinsic (t-aspect polynomial vs. height-scale sharp).
  Confidence it is intrinsic: **0.85**.

## 6. Action

- Fold §2 statement into §X.7 (Q:Perron) and the H1 discussion as the
  paper's single analytic spine; replace the two bespoke packages with
  "the Gonek–Hejhal conjecture for `L_E^*` (soft form) / for Dirichlet
  `L` (sharp form)."
- Add to the companion-theorem candidate list: *"H1(`E/Q`) and the
  corrected duality constant `D_K → e^{-γ}` are governed by a single
  Gonek–Hejhal negative second moment, at GL(2) and GL(1)
  respectively."*
- No Lean obligation changes: `GH` is a research-open analytic statement,
  same class as the existing conditional hypotheses; not an algebraic
  identity.
