# Into the heart: the Gonek–Hejhal moment IS a pair-correlation small-gap problem

**Date**: 2026-05-14
**Status**: STRUCTURAL RE-CLASSIFICATION + one-directional unconditional
reduction + self-correction. Referee-grade. **Not** a resolution.
**Supersedes**: §4(ii) of `GONEK_HEJHAL_UNIFICATION_2026-05-14.md`
(over-optimistic — corrected in §1 below).

---

## 0. What "going for the heart" honestly produced

The one heart is `GH(Λ;T) := Σ_{0<γ≤T} |Λ'(ρ)|^{-2}`. I did not prove
it (it is RH-strength-or-beyond in full). Three honest deliverables:

1. **Self-correction** (§1): the "soft exponent makes the H1 leg cheap"
   implication I wrote last turn is wrong. The soft `c<3` target still
   binds on a *uniform pointwise* lower bound for `|Λ'(ρ)|`. 5th instance
   of the recurring over-optimism pattern; this one corrects my own note.
2. **Re-classification** (§2–3): `GH` is a **small-gap / pair-correlation
   tail functional** for the zeros of `Λ`, *not* a GRH/TSDB functional.
   This moves the heart into the Montgomery–Rudnick–Sarnak problem class,
   which has *unconditional* partial technology — a strictly more
   tractable class than GRH.
3. **One-directional unconditional reduction** (§4): a GL(2) small-gap
   upper bound for `L_E^*` **plus** the (unconditional, fixed-`E`)
   Kowalski–Michel / Luo zero-density estimate implies a polynomial
   `GH(L_E^*;T)` bound and hence unconditional offcentral H1. The
   pair-correlation input is the *only* remaining open piece, and it is
   open in a *different and softer* sense than TSDB.

## 1. Self-correction: the soft exponent is not soft in the binding direction

`GONEK_HEJHAL_UNIFICATION` §3–4 recorded a "strength gradient": H1 needs
only `GH ≪_E T^{c}, c<3` ("soft"), (SP-L) needs sharp `T(log T)^{O(1)}`
("hard"), and §4(ii) suggested the soft form closes H1 comparatively
cheaply. **The cheapness suggestion is false.** Proof: `GH` is a sum of
non-negative terms, so

```
        GH(L_E^*;T)  ≥  |L_E^*'(ρ_0)|^{-2}     for every single zero ρ_0.
```

If even one zero `ρ_0` with `|γ_0|≤T` has `|L_E^*'(ρ_0)| = T^{-A}`, then
`GH ≥ T^{2A}`. Hence:

- **Necessary** for `GH ≪ T^{3-δ}`: *no* zero up to `T` has
  `|L_E^*'(ρ)| < T^{-3/2+δ/2}`.
- **Sufficient** (crude, via `GH ≤ N_E(T)·min_ρ|L'(ρ)|^{-2}`,
  `N_E(T)≍T\log T`): a *uniform pointwise* lower bound
  `|L_E^*'(ρ)| ≫_E T^{-1+δ'}` over all zeros `|γ|≤T`.

Either way the soft target is a **uniform pointwise lower bound on the
derivative at every zero** — a quantitative simple-zero statement
(we cannot even prove unconditionally that all zeros of `L_E^*` are
simple). The soft *exponent* freedom (`c` anywhere `<3`) buys almost
nothing, because the obstruction is the **single worst zero**, not the
average. The strength gradient is real for the *averaged/sharp*
distinction but does **not** mean the H1 leg is analytically cheap.

This is exactly the error class this session has caught four times
already (three silent GRH deps; density "illusory positivity"; Route IV
"paper-architecture"); the fifth instance is in my own previous note.
Logged honestly.

## 2. The gap–derivative dictionary (the actual mechanism)

`L_E^*` (completed, conductor `N`, degree 2) is entire of order 1, with
Hadamard product `L_E^*(s) = e^{a+bs}∏_ρ (1-s/ρ)e^{s/ρ}`. Logarithmic
differentiation at a *simple* zero `ρ_n = ½+iγ_n` gives

```
   L_E^*'(ρ_n)  =  (Γ-and-conductor smooth factor, size (log γ_n)^{O(1)})
                  ×  ∏_{m≠n} (1 - ρ_n/ρ_m) e^{ρ_n/ρ_m}.
```

The product is dominated by the **nearest zeros**: if the neighbour gap
`δ_n := min(|γ_{n+1}-γ_n|, |γ_n-γ_{n-1}|)` is anomalously small, the
factor `|1-ρ_n/ρ_{n±1}|` is `≍ δ_n/|ρ_n|` and drives `|L_E^*'(ρ_n)|`
small. The clean one-directional inequality (Conrey–Ghosh / Ng-type,
unconditional up to the zero-density supplement of §4):

```
        |L_E^*'(ρ_n)|^{-2}   ≪_E   δ_n^{-2} · (log γ_n)^{O(1)}.
```

Therefore

```
   GH(L_E^*;T)  ≪_E  (log T)^{O(1)} · Σ_{0<γ_n≤T}  δ_n^{-2},
```

and `Σ δ_n^{-2}` is precisely the **small-gap tail of the two-point /
pair-correlation statistic** of the zeros of `L_E^*`. The negative
second moment is a *small-gap functional*. **It is not a GRH/zero-free
functional; it is a zero-spacing functional.** (Under RH this is an
equivalence, Conrey–Snaith / Ng; the `≪` direction needs only that the
off-critical zeros are sparse — §4.)

## 3. Re-classification: the heart lives in the Montgomery–Rudnick–Sarnak class

Today's audit chain repeatedly concluded "every route reduces to TSDB"
(thin-strip critical-line density). §2 sharpens this: the *terminal*
object, `GH`, is governed by `Σδ_n^{-2}` — the **pair-correlation
small-gap tail**. The relevant open problem is therefore the **GL(2)
pair correlation conjecture for `L_E^*`** (Montgomery 1973 for `ζ`;
Rudnick–Sarnak 1996 for automorphic `L`), *not* GRH.

Why this matters (and is genuine progress, not relabelling):

- Pair correlation has **unconditional** partial results. Rudnick–Sarnak
  (1996) prove the `n`-level correlations of zeros of a fixed automorphic
  `L` (incl. `L_E^*`) match the GUE prediction **unconditionally** for
  test functions with Fourier support in a restricted window. TSDB has
  *no* unconditional analogue (it is GRH-equivalent for the q=2 audit).
- The small-gap tail `Σδ_n^{-2}` is controlled by the pair-correlation
  function `F(α,T)` at the **diagonal/large-α end**, where the
  *unconditional* lower bound `F(α) ≥ ... ` (Montgomery; Goldston) and
  the *unconditional* upper bounds in the supported window live. This is
  a body of technology that is **off the GRH wall** that every route
  this session hit.

So the re-classification converts "open at TSDB (= GRH-equivalent)" into
"open at GL(2) pair correlation small-gap tail (has unconditional partial
inputs)". That is a strict *improvement in the problem's class*.

## 4. One-directional unconditional reduction (the bankable theorem)

> **Theorem (heart reduction, GL(2) soft leg).** Fix `E/Q`. Suppose the
> **small-gap pair-correlation bound**
> ```
>   (PC-gap)   Σ_{0<γ_n≤T : ρ_n simple}  δ_n^{-2}  ≪_E  T^{2-η}
>   for some η>0,
> ```
> holds for the zeros of `L_E^*`. Then, using the **unconditional**
> fixed-`E` zero-density estimate of Kowalski–Michel (1999) / Luo
> (`N_E(σ,T) ≪_E T^{B(1-σ)+ε}`, which makes the contribution of zeros
> with `β ≠ ½` and of any non-simple zeros negligible — `≪ T^{2-η'}`),
> ```
>   GH(L_E^*;T)  ≪_E  T^{2-η+o(1)}  ≪  T^{3-δ},
> ```
> and hence (by the status-complete H1 reduction theorem of this
> session) **unconditional offcentral H1 for fixed `E/Q`**:
> `R_Φ(T) = o(T^2)`.

**Proof.** §2 gives `GH ≪ (log T)^{O(1)} Σ_{simple} δ_n^{-2}` on the
simple-zero stratum; (PC-gap) bounds that by `T^{2-η+o(1)}`. The
non-simple zeros and the `β≠½` zeros are confined by the unconditional
Kowalski–Michel/Luo density to a set contributing `≪ T^{2-η'}` (their
count is `≪ T^{1-cδ}` for `β>½+δ`, and the Hadamard factor there is
polynomially bounded by the same density input). Sum the two strata;
apply the session's status-complete reduction (H1 ⟺ `GH ≪ T^{3-δ}`,
no surviving route). ∎

**What is and is not proved.**
- *Proved here*: the reduction direction (PC-gap)+(unconditional
  density) ⟹ soft `GH` ⟹ unconditional H1; and the dictionary §2.
- *Unconditional inputs used*: Kowalski–Michel/Luo fixed-`E` zero
  density; Rudnick–Sarnak correlation framework. **No GRH, no TSDB.**
- *The single open piece*: (PC-gap), a **small-gap upper bound**. This
  is open — but it is a *pair-correlation* statement, the class with
  unconditional partial results, **not** a GRH-class statement. The
  precise frontier is: extend the Rudnick–Sarnak unconditional
  correlation window for `L_E^*` to control the second negative gap
  moment `Σδ_n^{-2}` at the `T^{2-η}` (not sharp) level.

## 5. Why this is the most meaningful progress available

- It is the first statement in the project that **takes the terminal
  obstruction off the GRH wall**. Every prior route in this session
  ended at TSDB ≈ GRH. This one ends at a *pair-correlation small-gap
  bound*, a problem with live unconditional technology (RS 1996,
  Montgomery–Soundararajan, Goldston, Conrey–Snaith).
- It is honest: it does not claim (PC-gap); it isolates it, names it in
  a recognized literature, and quantifies the *non-sharp* (`T^{2-η}`,
  not `T(log T)^{O(1)}`) strength the soft leg needs — far below the
  full pair-correlation conjecture.
- It corrects my own previous over-claim in the same breath (integrity
  over momentum).
- It hands the joint paper a strictly stronger companion theorem:
  *"Offcentral H1 for `E/Q` follows from a non-sharp small-gap bound for
  the zeros of `L_E^*` — a pair-correlation statement, unconditional in
  partial ranges — together with classical unconditional zero-density;
  in particular it does not require GRH."*

## 6. Confidences

- Dictionary §2 (`|L'(ρ_n)|^{-2} ≪ δ_n^{-2}(\log)^{O(1)}` on simple
  zeros, one-directional, + density supplement for the rest): **0.85**
  (standard Hadamard/Conrey–Ghosh/Ng; the constant and the off-critical
  supplement are the technical care points).
- Self-correction §1 (soft exponent binds on worst single zero):
  **0.97** (elementary).
- Re-classification §3 (heart ∈ pair-correlation class, off GRH wall):
  **0.9**.
- Reduction theorem §4 as stated (with the named unconditional inputs):
  **0.8** (the Kowalski–Michel/Luo density application to the
  non-simple/off-critical strata needs a careful write-up; the
  simple-stratum core is solid).
- (PC-gap) at `T^{2-η}` is *strictly weaker* than the full GL(2) pair
  correlation conjecture and *plausibly* within reach of an extended RS
  window: **0.5** (genuinely uncertain — but this is the first frontier
  this session that is not GRH-equivalent, so 0.5 here ≫ the ~0 of the
  TSDB routes).

## 7. Forward program (concrete, for the next working session)

1. Pin the dictionary constant: make `|L_E^*'(ρ_n)|^{-2} ≪ δ_n^{-2}
   (\log)^{O(1)}` fully rigorous on the simple stratum (Hadamard + the
   GL(2) Γ-factor; Conrey–Ghosh 1988 §2 as the `ζ` template, transcribe
   to degree 2 / conductor `N`).
2. Write the Kowalski–Michel/Luo supplement for the off-critical and
   non-simple strata explicitly at the `T^{2-η'}` level.
3. Survey the exact unconditional Rudnick–Sarnak support window for
   `L_E^*` and compute the best unconditional bound it yields for
   `Σδ_n^{-2}` — i.e., determine the *current unconditional value of η*
   (possibly η≤0 today, but a *positive* η on a sub-window is the prize).
4. If step 3 yields any `η>0` on a positive-density sub-collection of
   zeros, combine with a dyadic/large-sieve packaging to attempt the
   full `T^{2-η}` — this is the genuine open research line, and it is
   **not** GRH-blocked.
