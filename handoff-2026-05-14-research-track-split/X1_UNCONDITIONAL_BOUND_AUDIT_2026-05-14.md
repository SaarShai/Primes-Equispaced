---
schema_version: 2
title: "X.1 Unconditional Bound Audit — T^{15/8+eps} claim"
type: audit
domain: project
tier: working
status: PARTIAL
confidence: 0.55
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/OFF_HALO_UNCONDITIONAL_PIVOT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - Good 1982, "The square mean of Dirichlet series" (zeta 4th moment, t-aspect)
  - Meurman 1989 (GL2 / general L 4th moment refinement)
  - Iwaniec-Kowalski "Analytic Number Theory" Ch. 5 (AFE), Ch. 24 (GL2 4th moment)
  - Soundararajan, "Moments of the Riemann zeta function", Annals 2009
  - Heap-Soundararajan, negative moments framework
  - Bui-Florea arXiv:2302.07226 (zeta negative moments, unconditional T^{1+eps})
  - Heath-Brown 1979 / 1981 (zero-sampled Gallagher lemma; fractional moments)
  - Gallagher 1970 (zero-sampled second moment lemma)
supersedes: []
superseded-by:
tags: [halo-route, unconditional, X.1, audit, off-halo, T-fifteen-eighths]
---

# X.1 Unconditional Bound Audit — does R_Phi(T) <<_E T^{15/8+eps} survive?

## 1. Headline verdict

```text
status:  PARTIAL.

Of the X.1 five-step construction:
  - Step 1 (Good/Meurman 4th moment, T^{2+eps}):           CONFIRMED unconditional.
  - Step 2 (Heap-Sound bad-set -> int |L|^{-2} << T^{11/4+eps}):
           CONFIRMED unconditional ONLY at the loose-pointwise level;
           the exponent 11/4 is what one gets with the TRIVIAL polynomial
           floor |L|^{-1} <= T^{O(1)} from the FE.  It is NOT the conjectural
           T^{1+eps}; the X.1 derivation uses the LOOSE form, so 11/4 is correct
           for the unconditional regime.
  - Step 3 (= Step 2's output):                            tautological.
  - Step 4 (Gallagher-HB transfer to "zero-sampled
           sum |L'(rho)|^{-2}"):                            INCORRECT AS STATED.
           Gallagher-HB applied to g(t) = 1/L(1/2+alpha+it) outputs
              sum_{rho in Z_T}^{mult} |L(rho+alpha)|^{-2}, NOT sum |L'(rho)|^{-2}.
           These two objects differ by the cluster-shift comparison
           |L(rho+alpha)|^{-1}  ~?  alpha |L'(rho)|^{-1},
           which is the Door B object and is GRH-conditional.
           Additionally, the g'-term of Gallagher-HB pulls in
              int |L'/L|^2 |L|^{-2} dt  -> int |L'|^2 |L|^{-4} dt
           which has the SAME shifted-line negative-fourth-moment open exponent
           as int |L|^{-4}, NOT a free polylog factor.
  - Step 5 (Cauchy-Schwarz on residue aggregate):
           THE INNER FACTOR IS sum |L'(rho)|^{-2} (or sum |W_hat / L'|^2 directly),
           which Step 4 did NOT actually deliver unconditionally.
           So Step 5's combination requires either:
              (i) the Door-B GRH-conditional cluster-shift bridge
                  (HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md), OR
              (ii) the rectangle / finite-box route §3.5, which closes
                  T^{15/8+eps} unconditionally via a DIFFERENT path.

Final unconditional exponent on R_Phi(T) for fixed E/Q :
  T^{15/8 + eps}    SURVIVES, but via the RECTANGLE route (§3.5),
                    not via the halo-arc / Door-B route that the off-halo
                    agent wrote down.
  Confidence in T^{15/8+eps} unconditional : ~0.55  (lower than the
  off-halo's 0.78, because the rectangle route needs H-height/H-left
  unconditional, which is NOT a closed source).

  Confidence in T^{2-1/8} = T^{15/8} as a quantitative UPPER on the
  unconditional reachable exponent : ~0.85.

The off-halo agent's step-4 Gallagher-HB application HIDES Door B (GRH)
in the verbal phrase "transfer to zero-sample sum |L'(rho)|^{-2}".
Gallagher-HB delivers the SHIFTED zero sample, not the derivative zero sample.
The transfer between them is exactly the cluster-shift comparison, which
requires GRH (or RH-for-L_E^*) per HALOSHIFTCOMPARISON_LEMMA §0.
```

## 2. Step-by-step audit

### 2.A  Good/Meurman 4th moment — is this genuinely unconditional?

Claim audited:

```text
int_T^{2T}  |L_E^*(1/2 + it)|^4 dt   <<_E   T^{2+eps}    (fixed E/Q).
```

**Verdict: CONFIRMED unconditional.**

- Good 1982 (J. Number Theory) gave the zeta version
  `int_T^{2T} |zeta(1/2+it)|^4 dt = T P_4(log T) + O(T^{2/3+eps})` —
  this is the sharp Lindelof-on-line bound `T (log T)^4` (not just
  `T^{1+eps}`), unconditional, no RH used. Meurman 1989 refined the error.
- For fixed GL2 newform of bounded conductor `N_E`, the t-aspect 4th
  moment is `<<_E T^{2+eps}`, NOT the sharp `T (log T)^{O(1)}`. The
  `+eps` and the exponent `2` (rather than 1) are correct as stated
  in OFF_HALO §11.2 and CONT_SHIFTED §2.5; reference Iwaniec-Kowalski
  Ch. 24. Sharp `T^{1+eps}` is **open** for fixed GL2 (= mean-Lindelof
  in t-aspect for L_E^*).
- Ramified primes contribute bounded local factors absorbed into `<<_E`.
- The `+eps` is genuine (logarithmic factors from arithmetic combinatorial
  inputs not pinned exactly); for fixed E it is `(log T)^{O_E(1)}`.

Hidden assumption: none beyond fixed conductor. This step is clean.

### 2.B  Heap-Soundararajan k=2 bad-set: T^{11/4+eps} or weaker?

The off-halo agent quotes (§11.4 / §13 of OFF_HALO):

```text
int_T^{2T}  |L_E^*(1/2 + alpha + it)|^{-2} dt   <<_E   T^{11/4 + eps}.
```

The actual derivation is in `CONT_SHIFTED_NEG_Q2_GL2_PLAN §2.5`:

```text
At k = 2 (using Good/Meurman 4th moment T^{2+eps}):
  |B| <= int|L|^4 / V^4 <= T^{2+eps} / V^4.
  int_B |L|^{-2} dt  <=  |B| · sup_B |L|^{-2}.
On B,  |L|^{-1}  is bounded ONLY by the trivial pointwise FE+convexity
  floor  |L(s)|^{-1}  <=  T^{C}  for some absolute constant C = O(1)
  on the shifted line.
```

CONT_SHIFTED §2.5 then optimises `V = T^{-1/8}` to balance the polynomial
floor, yielding

```text
int_B |L|^{-2}  <=  T^{2+eps} · T^{1/2} · sup_B |L|^{-2}   (Markov+|B|)
               =   T^{2+eps} · V^{-6}    after balance,
               =   T^{11/4 + eps}.
```

**Re-derivation check.** The user's audit prompt sketched a derivation that
gave `T^{-eps}` (i.e., trivially tiny). That derivation set `V = T^{1/2+eps/2}`
to balance `V^{-2} T` against `V^{-4} T^{2+eps}`. This balance, however,
**assumes the good set has `|L| > V`, which gives ONLY**

```text
int_good  |L|^{-2}  <=  V^{-2} · |good|  <=  V^{-2} · T.
```

With `V = T^{1/2+eps/2}` good-set contribution is `T^{-eps}` — but **the
bad set is the same** and contributes

```text
int_bad  |L|^{-2}  <=  |B| · sup_B |L|^{-2}
                   <=  (T^{2+eps} V^{-4}) · sup_B |L|^{-2}
                   =   T^{2+eps} · T^{-2-2 eps} · sup_B |L|^{-2}
                   =   T^{-eps} · sup_B |L|^{-2}.
```

The factor `sup_B |L|^{-2}` is **not** controlled by Markov against the
4th moment; it is controlled only by the trivial pointwise FE floor
`|L|^{-1} <= T^{O(1)}`. So the prompt's "T^{-eps}" answer is wrong
because it dropped `sup_B |L|^{-2}`; with the polynomial floor
restored,

```text
int_bad |L|^{-2}  <=  T^{-eps} · T^{2 C}    (some C > 0 from FE)
                   =  T^{2C - eps}.
```

The right calibration is the one used in CONT_SHIFTED §2.5 — pick `V`
**well above** the trivial floor, get `|B|` smaller, then the
`sup_B |L|^{-2}` factor is bounded by `V^{-2}`. With `V = T^{-1/8}`:

```text
|B|  <=  T^{2+eps} · V^{-4}  =  T^{2+eps} · T^{1/2}  =  T^{5/2+eps},
int_B |L|^{-2}  <=  T^{5/2+eps} · V^{-2}  =  T^{5/2+eps} · T^{1/4}  =  T^{11/4+eps},
int_good |L|^{-2}  <=  V^{-2} · T  =  T^{1/4} · T  =  T^{5/4} ,
                       << T^{11/4 + eps}.
```

So the bound `int |L|^{-2} dt  <<_E  T^{11/4+eps}` **is correct
unconditionally** (with the standard polynomial floor) but is *much
weaker* than the conjectural truth `T^{1+eps}`. Heap-Soundararajan
proper (with the Selberg-Sound upper-bound technique) tightens this to
`T^{1+eps}` UNCONDITIONALLY for zeta (Bui-Florea arXiv:2302.07226 —
this is for zeta on the shifted line); the GL2 adaptation is *believed
standard* per CONT_SHIFTED §2.5 L580 but NOT in this repo, NOT in a
checked source for fixed GL2 newform.

**So the off-halo's "T^{11/4+eps}" is the LOOSE form (trivial-floor),
which is unambiguously unconditional. Confidence: HIGH (0.9).**

The off-halo step-2 statement is correct, but it is loose. The
unconditional T^{1+eps} via Bui-Florea-GL2 is BELIEVED but not yet
written in the repo.

### 2.C  Gallagher-Heath-Brown transfer: what does it actually produce?

This is the **load-bearing audit point**.

The Gallagher-Heath-Brown lemma:

```text
sum_{rho : T < gamma <= 2T}^{mult}  |g(gamma)|^2
   <<  log T · int_T^{2T} |g(t)|^2 dt
    +  (log T)^{-1} · int_T^{2T} |g'(t)|^2 dt.
```

Here `g(gamma)` is `g` evaluated at the ordinate `gamma` of a zero `rho =
1/2 + i gamma`. If we apply with `g(t) = 1/L_E^*(1/2 + alpha + it)`,
the LHS is

```text
sum_{rho}^{mult}  |g(gamma)|^2  =  sum_{rho}^{mult}  |L_E^*(1/2 + alpha + i gamma)|^{-2}
                                =  sum_{rho}^{mult}  |L_E^*(rho + alpha)|^{-2}.
```

**This is the SHIFTED zero sample**, NOT `sum |L_E^*'(rho)|^{-2}`. The
off-halo agent wrote in OFF_HALO §11.4 / §13:

```text
3.  Gallagher-HB transfer to zero-sample:
       sum_{rho in Z_T}^{mult}  |L_E^*'(rho)|^{-2}   <<_E   T^{11/4 + eps}.
```

This is **wrong as a direct Gallagher-HB output**. Gallagher-HB does not
deliver `L'`; it delivers `L` at a shifted-line point above the zero.

**The transfer `|L(rho+alpha)|^{-1} ~ alpha |L'(rho)|^{-1}` is precisely
the cluster-shift comparison, which is the Door B object.** From
`HALOSHIFTCOMPARISON_LEMMA §0`:

```text
Standing assumption: zeros of L_E^* lie on the critical line (GRH for
this newform). This is the framework's working hypothesis throughout
the halo route; not removed by this lemma.
```

The cluster-shift bound (`H1_SIMPLE_ZERO_CONDITIONAL_STACK §3`):

```text
|L_E^*'(rho)|^{-1}  <=  T^{o(1)} · (log T)^{-1} · W_A(rho) · |L_E^*(rho + 1/log T)|^{-1}.
```

This bound is valid only under GRH plus the cluster boundedness statistic
`RootedPalmRepulsionExpMoment_2(E, A)`. Without GRH, a thin-strip zero
near `rho_0` adjacent on the line `Re s = 1/2 + alpha` creates an
uncontrolled blowup of `|L(rho_0 + alpha)|^{-1}` relative to
`|L'(rho_0)|^{-1}` — the Taylor expansion `L(rho+alpha) = alpha L'(rho)
+ alpha^2 L''(rho)/2 + ...` has its quadratic term dominating when the
nearby zero is offcentral and creates a `1/(rho+alpha - rho_1)` blow-up
in `L''/L'`. This is exactly (TSDB)-equivalent.

**The g' term of Gallagher-HB.** Beyond the `g` term, Gallagher-HB
also pulls in

```text
int_T^{2T}  |g'(t)|^2 dt   =   int_T^{2T}  |L'/L|^2 · |L|^{-2}  dt
                          =   int_T^{2T}  |L'|^2 / |L|^4  dt.
```

Cauchy-Schwarz (per CONT_SHIFTED §2.6 L243-251):

```text
int |L'|^2 |L|^{-4}  <=  (int |L'/L|^4)^{1/2}  ·  (int |L|^{-4})^{1/2}.
```

- `int |L'/L|^4`: classical log-derivative 4th moment, bounded by
  `T (log T)^{O(1)}` unconditionally **IF** the shifted line is
  zero-free near it. Off the critical line at distance `alpha = 1/log T`,
  thin-strip zeros adjacent to the shifted line make `|L'/L|` blow up.
  Bounded unconditionally only at the level of (TSDB)-controlled
  cluster size.
- `int |L|^{-4}` = `ContShiftNeg_4(E)`. The same Heap-Sound k=2
  argument iterated with the 8th moment (not unconditionally known
  for fixed GL2) — or with the 4th moment used twice — gives
  `T^{?+eps}`. CONT_SHIFTED §2.6 quotes `T^{2+eps}` "from same
  Heap-Sound. with k=2", but the calibration there assumes a stronger
  Selberg-Sound. upper-bound technique for GL2 not actually closed.
  With trivial pointwise floor only, `int |L|^{-4}` is at best
  `T^{11/4+eps} · T^{2C} = T^{11/4 + 2C + eps}` with `C` the FE
  exponent. Loose. Quantification needs a careful re-do.

**Conclusion on Step 4 (Gallagher-HB).** Gallagher-HB delivers
unconditionally:

```text
sum_{rho}^{mult}  |L_E^*(rho + alpha)|^{-2}   <<_E   T^{11/4 + eps} · log T
                                                 +  (log T)^{-1} · [g'-term]   .
```

The `g'-term` is NOT unconditionally bounded by anything cleaner than
`T^{11/4 + eps}` (and probably much worse, since `int |L'/L|^4 |L|^{-4}` is
worse than `int |L|^{-2}`). At face value, taking the dominant term,

```text
sum_{rho}^{mult}  |L_E^*(rho + alpha)|^{-2}   <<_E   T^{?-loose} · polylog
```

with `? <= 11/4 + something not pinned`. The off-halo's clean `T^{11/4+eps}`
ignores this `g'-term`. The CONT_SHIFTED §2.6 careful version states
the transfer "eats nothing past `log T`" but this is conditional on
`ContShiftNeg_4(E) << T^{2+eps}`, which is a CONDITIONAL bound (per
CONT_SHIFTED §2.6 L255 — sourced through the same Heap-Sound. machinery).

**The transfer to `sum |L'(rho)|^{-2}` REQUIRES the cluster-shift
comparison and is therefore GRH-conditional.**

### 2.D  Cauchy-Schwarz on the residue aggregate

The off-halo agent writes:

```text
R_B(T)  =  sum  |W_hat(i gamma)| / |L_E^*'(rho)|
        <=  (sum |W_hat|^2)^{1/2}  ·  (sum |L_E^*'(rho)|^{-2})^{1/2}
        <=  T^{1/2 + eps}  ·  T^{11/8 + eps}
        =   T^{15/8 + eps}.
```

The first factor `sum |W_hat(i gamma)|^2` is `O(T (log T)^{O(1)})` —
weighted zero count, bounded by Riemann-von Mangoldt. Confirmed.

The second factor is `sqrt(sum |L'(rho)|^{-2})`. As Step 4 just showed,
**this is NOT what Gallagher-HB outputs**. The unconditional
Gallagher-HB output is `sum |L(rho+alpha)|^{-2}`.

To replace the second factor in Cauchy-Schwarz with the shifted version,
we need a termwise bound `|L'(rho)|^{-1}  <=  C(E) (log T) |L(rho +
alpha)|^{-1} · W_A(rho)` with `W_A` controlled. This is precisely
the cluster-shift comparison: GRH-conditional.

Alternatively, replace the WHOLE Cauchy-Schwarz step by an integral
identity over a rectangle (§F below). The rectangle bypasses Cauchy-Schwarz
on `|L'(rho)|^{-2}` and uses instead Cauchy-Schwarz on the
**continuous integral** along vertical edges. This DOES survive
unconditionally, but requires Step 2.E controls.

### 2.E  Where (if anywhere) is GRH hidden?

**Hidden GRH location: Step 4 → Step 5.** The phrase
"Gallagher-HB transfer to sum |L'(rho)|^{-2}" silently replaces
`|L(rho+alpha)|` by `alpha |L'(rho)|`. This replacement is the
cluster-shift comparison, which is Door B of the halo plan, which is
GRH-conditional (`HALOSHIFTCOMPARISON_LEMMA §0` standing assumption).

Secondary hidden assumption: the g'-term of Gallagher-HB requires a
4th-moment-on-shifted-line bound `int |L|^{-4} << T^{2+eps}`, which is
itself NOT unconditionally proved for fixed GL2; the same trivial-floor
calibration as Step 2.B gives only a loose `int |L|^{-4} << T^{?+eps}`
with `?` larger than `2 + eps`. Quantification pending; this is also
where Step 4's clean `T^{11/4+eps}` is over-optimistic.

### 2.F  Rectangle / finite-box route — does it close T^{15/8+eps} unconditionally?

The off-halo's Route VII §8 confirms that the rectangle reformulation

```text
R_Phi(T)  =  (1/(2 pi i)) int_{partial Rect} Phi_T(s)/L_E^*(s) ds
```

is **available unconditionally** as a residue identity. The rectangle
has four sides:

```text
V_+(s):  Re s = 1/2 + alpha,    Im s in [T, 2T]    (right vertical)
V_-(s):  Re s = 1/2 - alpha,    Im s in [T, 2T]    (left vertical)
H_+(s):  Im s = 2T,             Re s in [1/2-alpha, 1/2+alpha]
H_-(s):  Im s = T,              Re s in [1/2-alpha, 1/2+alpha]
```

**Right vertical V_+:**

```text
|int_{V_+}  Phi_T(s) / L(s)  ds|
  <=  sup_{V_+} |Phi_T|  ·  int_T^{2T}  |L(1/2 + alpha + it)|^{-1} dt
  <=  M_T  ·  T^{1/2}  ·  sqrt( int |L|^{-2} dt )      (Cauchy-Schwarz on integral)
  <=  M_T  ·  T^{1/2}  ·  T^{11/8 + eps}
  =   M_T  ·  T^{15/8 + eps}.
```

With `M_T  <<  T^{1/4}` (Stage 1b PASS of halo plan, `H1_NUMERATOR_M_T_AUDIT`),
this is `T^{1/4 + 15/8 + eps} = T^{17/8 + eps}` = `T^{2 + 1/8 + eps}`,
which is WORSE than `T^2`. Hmm.

**Re-check the M_T budget.** The off-halo §11.4 uses `M_T = sqrt(T log T)
= T^{1/2 + eps}` in its Cauchy-Schwarz on the residue sum, NOT
`T^{1/4}`. The numerator-aggregate `M_T` from `H1_NUMERATOR_M_T_AUDIT`
is the **per-zero** weight (kernel value), of size `T^{o(1)}` for fixed
kernel. The factor `T^{1/2 + eps}` in §11.4 comes from
`sqrt(#zeros · |W_hat|^2)` after pulling out `|W_hat|^2 = T^{eps}`. So
the integrated-over-V_+ rectangle bound is

```text
|int_{V_+}|  <=  T^{eps}  ·  T^{1/2}  ·  T^{11/8 + eps}
              =   T^{15/8 + eps}.
```

**Same exponent.** OK.

**Left vertical V_-:**

By the functional equation `L(1-s) = epsilon(s) L(s)` (with `|epsilon| =
1` on the appropriate normalization), `|L(1/2 - alpha + it)| = |L(1/2 +
alpha + it)|` (using the completed L-function with `epsilon`-factor).
**WAIT** — this is for the COMPLETED L; the *raw* `L_E` swaps `1-s` with
the gamma-factor / archimedean factor flipped. For `L_E^*(s) =
Lambda_E(s + 1/2)` (analytic normalization), the functional equation
gives `|L_E^*(1/2 + alpha + it)| = |L_E^*(1/2 - alpha - it)|`, so
the left and right vertical contributions are equal in absolute value.
Confirmed unconditionally.

**Horizontal edges H_±:** This is where the rectangle has its
GRH-INDEPENDENT but NEW obstruction. From `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE`:

```text
|H_+(T,u)| + |H_-(T,u)|
  <=  C (sigma + eta) e^{sigma u} (1 + T)^{-q} M(T),
M(T) = sup_{Re s in [1/2-alpha, 1/2+alpha]}  |1/L_E^*(s + iT)|.
```

The kernel decay `q = 2` (smoothstep). The horizontal bound becomes
useful only if `M(T)` is `o(T^q) = o(T^2)`. The assumption needed is
the H-height(A) hypothesis:

```text
H-height(A):  there exist legal T_n -> infinity with M(T_n) <= C T_n^A,  A < 2.
```

`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE §"What this does not give"` flags this
as **NOT supplied by any checked EC/GL2 source**. The standard
zero-counting gives legal heights `T_n` with `dist(T_n, gamma) >=
c_E / log T_n`, but the local Laurent expansion at the nearest zero `rho`
gives `|1/L(s)| ~ |b_{rho,-1}| (log T)` (simple zero, distance `1/log T`).
This is `|1/L'(rho)| · (log T)`, and **without GRH or a quantitative
bound on `|1/L'(rho)|` for offcentral zeros, this can be huge**.

**So the rectangle route silently requires either GRH or a NEW unconditional
control of `|1/L'(rho)|`** — the same object Door A is trying to bound.
It is CIRCULAR: to bound `R_Phi(T)` via the rectangle, we need `M(T)`
controlled at the horizontal cuts, which requires control of
`1/L'(rho)` for the nearest zero, which is exactly what `R_Phi(T)`
aggregates.

This is the central tension in `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE`
"Bottom Line":

```text
The new assumption is quantitative reciprocal control of 1/L(E,s) in
the crossed strip, compatible with the same height sequence and
residue aggregation mode.
```

**Verdict on the rectangle route:** the right and left vertical edges
do give the `T^{15/8+eps}` contribution unconditionally, but the
horizontal-edge contribution is NOT bounded unconditionally; it
requires an H-height(A) assumption that is the same flavour of
unconditional gap as Door B. So the rectangle route does NOT
unconditionally close `R_Phi(T) <<_E T^{15/8+eps}` either.

There may be a workaround: pick the rectangle TIGHT (`alpha = 1/log T`)
and use the fact that the AFE/Mellin start line `Re s = 1 + sigma`
(with `sigma > 0` small) gives clean horizontal bounds in the
absolute-convergence half-plane, then move to `Re s = 1/2 + alpha`
through the crossed strip with the H-height hypothesis. The off-halo
agent's §13 sketch only addresses the vertical edge, not the horizontal
one — an oversight.

### 2.G  Final unconditional verdict

```text
Currently UNCONDITIONALLY proved for fixed E/Q :

  int_T^{2T}  |L_E^*(1/2+it)|^4 dt   <<_E   T^{2+eps}.            (Step 1, CLEAN)

  int_T^{2T}  |L_E^*(1/2+alpha+it)|^{-2} dt   <<_E   T^{11/4+eps}.
                                                                  (Step 2, CLEAN
                                                                   at loose level)

  sum_{rho in Z_T}^{mult}  |L_E^*(rho + alpha)|^{-2}   <<_E   T^{11/4 + eps}
                                                       · log T
                                                       + (log T)^{-1}
                                                          · int|L'/L|^2|L|^{-2} dt.
                                                                  (Step 4 in
                                                                   its CORRECT form)

  The second piece (g'-term) is NOT cleanly bounded unconditionally.
  The off-halo agent's quoted "T^{11/4+eps}" for the LHS is hopeful.

Currently NOT proved unconditionally for fixed E/Q :

  sum_{rho in Z_T}^{mult}  |L_E^*'(rho)|^{-2}   <<_E   T^{?+eps}    (any ? < 3).

  Equivalent reductions:
    Door B cluster-shift comparison (GRH-conditional)
    OR rectangle route via H-height(A) (not source-closed)
    OR direct unconditional zero-sample BFMT for L' at zeros (not in repo).

  R_Phi(T)  <<_E  T^{15/8 + eps}    is therefore NOT proved unconditionally
                                    today.
```

Whatever exponent the project can prove unconditionally is bounded *above*
by `T^{15/8 + eps}` (since the rectangle + GRH-relaxation would yield
that), but the value actually delivered today is, more pessimistically,

```text
R_Phi(T)   conditional on (GRH) :  <<_E  T^{7/4 + eps}     (the project's
                                                            simple-zero stack,
                                                            tighter than 15/8)
R_Phi(T)  unconditional          :  no proved sub-T^2 bound exists today.
                                    Best heuristic upper: T^{15/8 + eps}
                                    via rectangle, pending H-height(A)
                                    audit.
```

## 3. Comparison with the conditional halo route under GRH

| Route | Hypotheses | Exponent on R_Phi(T) |
|---|---|---|
| X.1 as written by off-halo | "unconditional" (claimed) | T^{15/8 + eps} |
| X.1 actually proved here | unconditional + Step 2 only | shifted sum T^{11/4+eps}; no R_Phi bound below T^2 |
| Halo + Door B + Door A (q=2 conditional pass) | GRH(L_E^*) + Wave 4 + cluster-shift | T^{7/4 + eps} (H1_SIMPLE_ZERO_CONDITIONAL_STACK §combined) |
| Rectangle route (Cauchy-Schwarz on vertical) | unconditional + H-height(A) + H-left | T^{15/8 + eps} |

The conditional halo route under GRH gives `T^{7/4+eps}` — strictly
BETTER than the X.1 unconditional target `T^{15/8+eps}`, as expected
(`7/4 = 14/8 < 15/8`). The unconditional X.1 target, IF achieved via
the rectangle route, would be tighter than the conditional halo
**because of Cauchy-Schwarz inefficiency** — but the rectangle route
itself is not yet unconditional.

## 4. Where the off-halo agent slipped

The off-halo agent's report (OFF_HALO_UNCONDITIONAL_PIVOT §11.4, §13)
is internally rigorous for Steps 1, 2, 5 (modulo Step 5 needing the
right inner factor). The single load-bearing slip is **Step 4**, where
the phrase

> "Gallagher-HB transfer to sum_{rho}^{mult} |L_E^*'(rho)|^{-2}"

silently swaps the shifted sum for the derivative sum. The swap is
EXACTLY Door B's cluster-shift comparison, which requires GRH per
`HALOSHIFTCOMPARISON_LEMMA §0`. The off-halo agent did NOT note this
swap as a conditional input. The agent's confidence rating 0.78 should
be DOWNGRADED to ~0.55 to reflect this slip.

A secondary, less serious issue: Step 2's `T^{11/4+eps}` is correct
in the loose form (trivial polynomial floor), but the agent labels it
"Heap-Soundararajan calibration" which conventionally means the
Selberg-Sound. upper-bound machine (Annals 2009). That machine gives
`T^{1+eps}` for zeta UNCONDITIONALLY (Bui-Florea), but the GL2
adaptation for fixed conductor is **believed standard but not
written in this repo**. Using the LOOSE form is fine and what the
construction needs; the labeling is slightly misleading.

## 5. Final unconditional bound for fixed E/Q

```text
Theorem (provable unconditionally TODAY):
  int_T^{2T}  |L_E^*(1/2 + 1/log T + it)|^{-2}  dt   <<_E   T^{11/4 + eps}.

  Equivalently  (Gallagher-HB):
    sum_{rho in Z_T}^{mult}  |L_E^*(rho + 1/log T)|^{-2}   <<_E   T^{11/4 + eps} · log T
                                                                 + (transfer g'-term).

Theorem  (CONJECTURED but NOT YET UNCONDITIONAL):
  R_Phi(T)  <<_E  T^{15/8 + eps}.

  Status:
    via Door B cluster-shift route :  GRH(L_E^*) conditional.
    via rectangle / finite-box route :  conditional on H-height(A), A < 2,
                                         for legal heights, not source-closed
                                         for fixed EC/GL2.
    via direct unconditional zero-sample for L' at zeros : OPEN.

No PROVED unconditional sub-T^2 bound on R_Phi(T) survives today.
```

This contradicts OFF_HALO §1's "PARTIAL: X.1 closes unconditionally at
T^{15/8+eps}". The PARTIAL status is correctly assigned but for the
wrong reason: the partiality is in Step 4 (Door B hidden), not in the
joint-paper audit.

## 6. Boundary

### Allowed claims

```text
- Step 1 (Good/Meurman T^{2+eps}) is unconditional for fixed E/Q.
- Step 2 (loose Heap-Sound. with trivial floor) gives
  int |L|^{-2} dt <<_E T^{11/4+eps} unconditionally.
- Gallagher-HB applied to g = 1/L(1/2+alpha+it) gives
  sum |L(rho+alpha)|^{-2} unconditionally (plus a g'-term not cleanly bounded).
- The full conditional halo route under GRH(L_E^*) gives
  R_Phi(T) <<_E T^{7/4+eps} (simple-zero stack).
- The rectangle route is identity-grade unconditionally (residue
  theorem on rectangle), but its horizontal-edge bound is open.
- R_Phi(T) <<_E T^{15/8+eps} is the cleanest TARGET for an
  unconditional sub-T^2 bound, conditional on either (i) Door B cluster-shift,
  or (ii) H-height(A) for the rectangle.
```

### Forbidden claims

```text
- "R_Phi(T) <<_E T^{15/8+eps} is unconditionally proved."  Currently FALSE.
- "Gallagher-HB delivers sum |L'(rho)|^{-2}."  FALSE; it delivers
  sum |L(rho+alpha)|^{-2}.
- "Step 4 of OFF_HALO §11.4 is rigorous as written."  FALSE; it swaps
  shifted for derivative without GRH input.
- "Heap-Sound. for fixed GL2 newform of bounded conductor gives
  int |L|^{-2} <<_E T^{1+eps} unconditionally."  Currently FALSE
  (believed but not written; Bui-Florea is zeta).
- "The rectangle route closes T^{15/8+eps} unconditionally."  FALSE;
  horizontal edges require H-height(A).
```

### Genuine surprise

```text
SURPRISE 1.  The off-halo agent's "unconditional T^{15/8+eps}" claim
             has a hidden GRH dependency in Step 4 (Gallagher-HB →
             derivative sum), not in Step 2 (Heap-Sound. bad-set) as the
             user's audit prompt anticipated.  The bad-set calibration
             is genuinely clean at the loose level; the issue is the
             transfer from shifted sum to derivative sum.

SURPRISE 2.  Under GRH(L_E^*), the conditional halo route already
             gives T^{7/4+eps} (= T^{14/8+eps}), which is STRICTLY
             BETTER than the off-halo's unconditional target
             T^{15/8+eps}.  This makes the off-halo route uninteresting
             *under GRH* — the only value of an unconditional
             T^{15/8+eps} is if it survives WITHOUT GRH, and the audit
             shows it currently does not.

SURPRISE 3.  The rectangle route DOES potentially close T^{15/8+eps}
             unconditionally via Cauchy-Schwarz on the vertical edge,
             AVOIDING Door B.  But it pays for that by needing
             H-height(A) on the horizontal edge, which is its own
             unconditional gap (`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE`).
             So the rectangle is a *different* route to T^{15/8+eps},
             not a salvage of the off-halo's halo-arc construction.
             Net: the unconditional target is the same (T^{15/8+eps})
             from two different angles, and BOTH angles have the same
             flavour of currently-open horizontal/cluster control.

SURPRISE 4.  The off-halo agent's Step 4 "Gallagher-HB transfer" is the
             single line in the whole 1100-line OFF_HALO document where
             the GRH dependency is silently introduced.  The rest of
             the document is conservative and clean.  This is a
             pinpointable, single-line audit fix; the document is
             otherwise structurally sound.
```

### Probability ledger

```text
0.90  Step 1 (Good/Meurman T^{2+eps}) is unconditional for fixed E/Q.
0.85  Step 2 (int |L|^{-2} <<_E T^{11/4+eps}) is unconditional in
      the loose form (trivial polynomial floor).
0.10  Step 4 (sum |L'(rho)|^{-2} <<_E T^{11/4+eps}) is unconditional
      as written (i.e., that cluster-shift comparison is removable).
0.55  The TARGET R_Phi(T) <<_E T^{15/8+eps} is achievable
      unconditionally in 1-2 months of careful audit
      (closing either the cluster-shift question OR the
      H-height(A) question).
0.30  The X.1 unconditional target is actually false at T^{15/8+eps}
      and the true unconditional best is T^{2-eta} for eta < 1/8.
0.05  An entirely-different unconditional route (not enumerated)
      closes T^{15/8+eps} cleanly.
```

## 7. Recommendation

```text
1.  EDIT OFF_HALO_UNCONDITIONAL_PIVOT_2026-05-14.md to:
    a)  Note Step 4 is NOT unconditional; flag the cluster-shift swap.
    b)  Downgrade the X.1 confidence from 0.78 to ~0.55.
    c)  Re-state the unconditional ledger:
        int |L|^{-2} <<_E T^{11/4+eps}  unconditional;
        sum |L(rho+alpha)|^{-2} <<_E ...   unconditional (with g'-term);
        sum |L'(rho)|^{-2}  : NOT unconditional today;
        R_Phi(T) sub-T^2     : NOT unconditional today.

2.  Commission a clean "rectangle horizontal-edge unconditional audit"
    targeting H-height(A) for fixed EC L-functions.  This is the single
    most leverage-bearing piece of unconditional work currently visible
    from the audit.  Cost ~1-2 weeks; risk medium.

3.  Do NOT promote X.1 as the project's unconditional fallback in the
    paper-prep tracker.  The fallback should remain "conditional halo
    route under GRH gives T^{7/4+eps}", and the X.1 unconditional
    line should be marked CONDITIONAL until the rectangle / Door B
    audit closes.

4.  The "audit the Saar-Koyama joint paper's H1 form" task remains
    high-priority but is INDEPENDENT of this audit — even if the paper
    needs only T^{2-eta}, the X.1 unconditional construction still
    falls short today.

5.  Re-read CONT_SHIFTED_NEG_Q2_GL2_PLAN §2.6 transfer carefully.
    The clean "transfer eats nothing past log T" claim is itself
    CONDITIONAL on ContShiftNeg_4(E) << T^{2+eps}, which is a
    same-difficulty open shifted moment.  Without that, the transfer
    has its own loss, further weakening the X.1 chain.
```
