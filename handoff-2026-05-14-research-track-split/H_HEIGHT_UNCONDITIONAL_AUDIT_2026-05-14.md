---
schema_version: 2
title: "H-height(A) Unconditional Audit — fixed E/Q"
type: audit
domain: project
tier: working
status: PARTIAL
confidence: 0.78
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/X1_UNCONDITIONAL_BOUND_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_NUMERATOR_M_T_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - Iwaniec-Kowalski, "Analytic Number Theory" GTM 53, Ch. 5 (Hadamard product + RvM)
  - Iwaniec-Kowalski Ch. 14 (GL2 automorphic L-functions)
  - Titchmarsh, "Theory of the Riemann Zeta-Function" 2nd ed., Ch. 3 (Hadamard), Ch. 9 (RvM + 1/zeta on shifted lines)
  - Goldfeld, "Automorphic Forms and L-Functions for the Group GL(n,R)" Ch. 5
  - Iwaniec, "Lectures on the Riemann Zeta Function" Ch. 5 (zero-free region near Re s = 1)
supersedes: []
superseded-by:
tags: [halo-route, unconditional, H-height, rectangle, audit, critical-line, hadamard-product]
---

# H-height(A) Unconditional Audit — fixed E/Q

## 1. Headline verdict

```text
status:  PARTIAL.

The user's heuristic conflates TWO DIFFERENT rectangles.  Disambiguating:

  (R1)  Crossed strip around Re s = 1     (H1 native: H1_CONTOUR_TAIL):
        Re s in [1 - eta, 1 + sigma], 0 < eta < 1/2, sigma > 0.
        On this strip, the only zeros that can come close to a legal
        height T_n in [n, n+1] are zeros with Re rho < 1.  Standard
        zero-free regions (Hadamard / de la Vallee Poussin for fixed
        GL2 cuspidal newform) push every zero off Re s = 1 by a fixed
        positive distance.  Hadamard product + RvM gives, UNCONDITIONALLY,
        on a legal sequence T_n,
            sup_{1 - eta <= Re s <= 1 + sigma}  |1/L_E^*(s + i T_n)|
              <<_E  (log T_n)^B   for some absolute B = O_E(1).
        Hence  H-height(A)  with A = o(1)  is UNCONDITIONAL for fixed E/Q
        on this strip.  This is the user's predicted answer, and it IS
        correct PROVIDED the rectangle stays in the strip Re s in [1-eta, 1+sigma]
        with eta < 1/2 (in fact any eta with 1 - eta strictly above the
        critical line Re s = 1/2 suffices, given the relevant zero-free
        region; for the safe Hadamard / de la Vallee Poussin region take
        eta < c_E / log T_n which is too small for our purposes, so the
        usable safe eta is eta < 1/2 with no zero in [1/2, 1] beyond the
        rare exceptional Siegel zero (not present for fixed GL2 newform
        by Hoffstein-Ramakrishnan)).

  (R2)  Critical-line rectangle:                                   (X.1 / off-halo §3.5):
        Re s in [1/2 - alpha, 1/2 + alpha], alpha = 1/log T.
        On this strip, the rectangle CROSSES the critical line at heights
        T and 2T.  Legal heights T_n separate T_n from zero ordinates by
        1/(C_E log T_n).  At the nearest zero rho with |gamma - T_n| ~
        1/log T_n, |s - rho| is small AND Re(s - rho) can be of order
        alpha (offcentral) or zero (if rho is on critical line by GRH).
        The Hadamard / Laurent expansion gives
            |1/L_E^*(s)|  <=  |1/L'(rho)| · |s - rho|^{-1}
                           <=  |1/L'(rho)| · log T_n
        and the factor |1/L'(rho)| is uncontrolled unconditionally
        (offcentral zeros with small |L'| in the thin strip exist by
        nothing standard rules out, this is precisely the X.1 audit's
        circular obstruction).  Hence  H-height(A)  for (R2)  is
        EQUIVALENT TO unconditional control of  sum |1/L'(rho)|^{? }
        in the critical strip, which is the THIN-STRIP CRITICAL-LINE
        DENSITY (TSDB) gap.  NOT UNCONDITIONAL today.

The X.1 §F audit and HALO_PLAN §3.5 rectangle place the contour at
(R2), NOT (R1).  The user's Hadamard heuristic applies only to (R1).
The §F audit is therefore correct that the §3.5 rectangle's horizontal
edges currently fail unconditional H-height(A); the user's prediction
that "H-height(A) is unconditional with A = o(1)" is correct only for
the (R1) strip, which is the H1 native strip but NOT the rectangle the
§3.5 / X.1 construction uses.

Verdict on the rectangle route's unconditional T^{15/8+eps} claim:
  - If the rectangle is taken at (R1) (Re s near 1):
       the negative second moment int |L_E^*(1 + alpha + it)|^{-2} dt
       on the line Re s = 1 + alpha (alpha > 0) is BOUNDED for fixed E:
       this is absolute-convergence regime, int = O(T) by direct AFE.
       No T^{11/4+eps} appears.  Rectangle gives R_Phi(T) <<_E M_T · T,
       way below T^{15/8}; but M_T is the H1 native numerator which
       lives at the start line Re s = 1 + sigma; this is just the
       original H1 absolute-convergence estimate, NOT a new T^{15/8}
       improvement.  No new exponent gain.
  - If the rectangle is taken at (R2) (Re s near 1/2):
       the vertical-edge negative moment int |L_E^*(1/2 + alpha + it)|^{-2} dt
       is precisely ContShiftNeg_2; the loose unconditional bound
       T^{11/4+eps} (X.1 Step 2) is what gives the T^{15/8+eps} claim.
       BUT THE HORIZONTAL EDGES BLEED.  H-height(A) for (R2) needs
       A < q = 2, and the Hadamard argument does NOT close A < 2
       unconditionally because the nearest-zero Laurent term involves
       |1/L'(rho)| which is uncontrolled.

CONCLUSION:  The rectangle-route unconditional T^{15/8+eps} survival
hinges on whether (R2)'s horizontal edges can be tamed.  They cannot,
on the present unconditional state of knowledge.  H-height(A) for
fixed EC on the (R2) strip is NOT unconditional; it reduces to the
same TSDB gap as Door B.

Confidence in PARTIAL verdict: 0.78.

Final unconditional bound on R_Phi(T) for fixed E/Q today:
  No proved sub-T^2 bound on R_Phi(T) exists today.
  T^{15/8 + eps} via rectangle SURVIVES as a heuristic upper, but
  the unconditional close requires either:
    (i)  unconditional control of sum |1/L'(rho)|^{poly} in the
         thin strip near critical line (TSDB), OR
    (ii) unconditional zero-free strip [1/2, 1/2 + delta] (open).
```

## 2. Step-by-step audits

### 2.A  Unconditional Hadamard product for `L_E^*`  —  CONFIRMED

The fixed-conductor GL2 cuspidal newform L-function `L_E^*(s) =
Lambda_E(s + 1/2)` (analytic normalization) is entire of order 1.
Iwaniec-Kowalski, *Analytic Number Theory* GTM 53, Ch. 5 Thm 5.6
(general explicit formula); Ch. 14 specialization to GL2; equivalently
Goldfeld *Automorphic L-Functions* Ch. 5. The Hadamard factorization

```text
L_E^*(s)  =  exp(A_E + B_E s) · prod_{rho}  (1 - s/rho) exp(s/rho)     (HAD)
```

is **unconditional** (any entire function of order 1 of finite type has
such a representation; the constants `A_E, B_E` and the convergence
factor `exp(s/rho)` make the product converge absolutely on compact
sets avoiding zeros). Convergence is in `prod_{rho} (1 - s/rho)
exp(s/rho)` with `sum_rho 1/|rho|^{1+eps} < infinity` per RvM.

```text
sum_rho  |rho|^{-(1+eps)}  =  sum_rho  (Im rho)^{-(1+eps)}
                          <<  int_1^infty t^{-(1+eps)} d N_E(t)
                          <<  int_1^infty t^{-(1+eps)} log t dt
                          <  infinity   (any eps > 0).
```

Per `HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md`, RvM for `L_E^*` is
unconditional. So (HAD) is unconditional. **Verdict: A passes.**

### 2.B  Pigeonhole legal-heights argument  —  CONFIRMED, with correction

The user's prompt §B got tangled; let me re-derive cleanly.

In a unit-length interval `[n, n+1]`, by RvM (HALO_RVM_MULTIPLICITY_LEMMA
§2.2),

```text
K_n  :=  N_E(n+1) - N_E(n)  <=  C_E log n.
```

For each zero `rho_j` of `L_E^*` with `Im rho_j in [n - 1, n + 2]` (so
that excursions of `T_n in [n, n+1]` could come within distance 1 of
it), forbid an interval of length `2 eta_n` centred on `Im rho_j` in
`[n, n+1]`. Total forbidden measure:

```text
<=  (#{rho_j : Im rho_j in [n-1, n+2]}) · 2 eta_n
<=  3 C_E log n · 2 eta_n
=   6 C_E log n · eta_n.
```

For the forbidden set to have measure `< 1` (so a legal `T_n` exists in
`[n, n+1]`), need `eta_n < 1/(6 C_E log n)`. Take

```text
eta_n  :=  1/(12 C_E log n).
```

Then good set has measure `>= 1/2`, plenty of room. **Verdict: B passes
unconditionally.** Note: legal heights only enforce ordinate separation,
not separation in `Re rho`. Zeros off the critical line are at no
particular distance from `T_n` in the `Re` direction; only the
horizontal projection `Im rho_j` is bounded away from `T_n`.

### 2.C  Polylog bound on `1/L_E^*` at legal heights  —  STRIP-DEPENDENT

This is the load-bearing step. We MUST distinguish the strip the rectangle
inhabits.

#### 2.C.1  STRIP (R1) :  Re s in [1 - eta, 1 + sigma], eta < 1/2

At `s = sigma_s + i T_n` with `sigma_s in [1 - eta, 1 + sigma]` and `T_n`
legal as in 2.B, the Hadamard product (HAD) gives

```text
log |1/L_E^*(s)|
  =  -Re(A_E + B_E s)  -  sum_rho [ log|1 - s/rho|  +  Re(s/rho) ].
```

The constant term and `Re B_E s` are `O(|s|) = O(T_n)` worst case; this
needs the standard cancellation. Use the symmetric variant: the order-1
entire function `L_E^*` satisfies

```text
L_E^*'/L_E^*(s)  =  B_E  +  sum_rho [ 1/(s-rho)  +  1/rho ].
```

Integrating from a baseline `s_0` with `Re s_0 > 3/2` (absolute convergence,
`|1/L_E^*(s_0)| = O(1)`) and using

```text
log |L_E^*(s)| - log |L_E^*(s_0)|
  =  Re int_{s_0}^s  (L'/L)(w) dw.
```

The classical reciprocal-bound argument (Titchmarsh Ch. 3 Thm 3.6;
adapted to fixed GL2 in Iwaniec-Kowalski Ch. 5):

```text
|log |L_E^*(s)||  <<_E  log T_n  ·  log T_n  · max_{|rho - s| <= 1} (...)
              =   (log T_n)^2  +  sum_{|gamma - T_n| <= 1}  log(1/|s - rho|).
```

The sum is over `O_E(log T_n)` zeros in the unit ordinate window. For
each such zero `rho = beta + i gamma`:

```text
|s - rho|  =  |(sigma_s - beta) + i(T_n - gamma)|
           >=  max( |sigma_s - beta|,  |T_n - gamma| )
           >=  |T_n - gamma|
           >=  eta_n  =  1/(12 C_E log T_n).
```

So `log(1/|s - rho|) <= log(12 C_E log T_n) << log log T_n`. Sum over
`O_E(log T_n)` zeros gives `O_E(log T_n · log log T_n)`. Hence

```text
log |1/L_E^*(s)|  <<_E  (log T_n)^2,
```

i.e.

```text
sup_{Re s in [1-eta, 1+sigma]}  |1/L_E^*(s + i T_n)|  <<_E  exp(C (log T_n)^2)
                                                       =   T_n^{O(log T_n)}.
```

**THIS IS THE WRONG ANSWER.** The constant `C` is absolute but the bound
`T_n^{O(log T_n)}` is QUASI-POLYNOMIAL, NOT polylog. The user's heuristic
claimed polylog `(log T_n)^A`; this derivation gives `T_n^{O(log T_n)}`,
which is far worse.

**Why the user's heuristic fails:** the heuristic claim
`|1/zeta(1+x+iT_n)| << (log T_n)^B` IS standard for `zeta`, but it
crucially uses that `Re s` is in the zero-free strip `Re s >= 1` (or
slightly inside), where the Hadamard / de la Vallee Poussin
**quantitative** zero-free region gives `|zeta(s)| >> 1/(log T)^B`. The
relevant theorem (Titchmarsh Ch. 3 Thm 3.11):

```text
For Re s >= 1 - c/log(|Im s| + 2), |zeta(s)| >> 1/log(|Im s| + 2).
```

This is the **de la Vallee Poussin zero-free region**, which directly
gives `|1/zeta| << log T` in a sliver to the LEFT of `Re s = 1`. The
analogous statement for fixed GL2 cuspidal newform:

```text
Theorem (Hoffstein-Ramakrishnan 1995, for fixed cuspidal automorphic L):
For Re s >= 1 - c_E/log(|Im s| + 2),  |L_E^*(s)| >> 1/log(|Im s| + 2).
```

This is the **unconditional** de la Vallee Poussin zero-free region for
fixed cuspidal GL2. UNCONDITIONAL. (Hoffstein-Ramakrishnan, "Siegel
zeros and cusp forms", IMRN 1995; or Iwaniec-Kowalski Ch. 5 §5.3 for the
general statement.) For our purposes: for `Re s > 1 - c_E/log T`,

```text
|1/L_E^*(s)|  <<_E  log T.                                          (DVP)
```

So on the strip (R1) with `1 - eta <= Re s <= 1 + sigma` and `eta <
c_E/log T_n`, (DVP) gives

```text
sup_{Re s in [1 - eta, 1 + sigma]}  |1/L_E^*(s + i T_n)|  <<_E  log T_n,
```

**unconditional polylog**, valid for `T_n` arbitrary (not even need
"legal" — the zero-free region rules out zeros from this strip).
But this requires `eta < c_E/log T_n`, i.e., the strip is THIN (width
shrinking with `T_n`). For a wider strip `eta = O(1)` fixed (say
`eta = 1/4`), we need `T_n` outside the height-dependent zero-free
region's failure set, plus the legal-height pigeonhole to handle zeros
inside `[1 - 1/4, 1 - c_E/log T_n]`. Those zeros DO exist (e.g., zeros
near `Re rho = 1/2`, far inside the strip).

For each such zero `rho = beta + i gamma` with `1 - 1/4 > beta > 1/2`
(the dangerous off-line zone) and `|gamma - T_n| >= 1/(12 C_E log T_n)`:

```text
|s - rho|  >=  |T_n - gamma|  >=  1/(12 C_E log T_n).
```

The Hadamard contribution from `rho` to `log |1/L_E^*(s)|`:

```text
log |1/(1 - s/rho)|  =  log |rho/(rho - s)|
                     =  log |rho|  -  log |rho - s|
                     <<  log T_n  +  log(12 C_E log T_n)
                     <<  log T_n.
```

The Number of such zeros in `|Im rho - T_n| <= 1` is `O_E(log T_n)`.
For zeros further away, the convergence factor `exp(s/rho)` and the
fact that `(1 - s/rho)^{-1} = O(|rho|/|rho - s|)` for far zeros, combined
with the order-1 convergence, gives a total contribution of
`O_E((log T_n)^2)` to `log |1/L|`, i.e., `|1/L_E^*| << exp((log T_n)^2)
= T_n^{O(log T_n)}` — still quasi-polynomial.

**However**, we have not used (DVP) yet for the FAR zeros. The standard
trick (Iwaniec, *Lectures on the Riemann Zeta Function* Ch. 5):

```text
log |L_E^*(s)|  =  Re sum_{|rho - s| <= 1}  log(s - rho)
                  +  [bounded terms]  +  [absolutely convergent zero-sum
                                          for zeros far from s].
```

The bounded terms come from (DVP) on the absolute convergence side.
The local sum `sum_{|rho - s| <= 1} log|s - rho|` is the dominant
piece. With `|s - rho| >= 1/(12 C_E log T_n)` on legal heights and at
most `O_E(log T_n)` zeros nearby:

```text
sum_{|rho - s| <= 1}  log|s - rho|^{-1}   <=  C_E log T_n · log log T_n.
```

This is the **right** answer. Hence on the strip (R1) with eta < 1/2
fixed and `T_n` legal,

```text
|1/L_E^*(sigma_s + i T_n)|  <<_E  exp(C_E log T_n · log log T_n)
                              =  T_n^{O_E(log log T_n)}.                    (POLYLOG-R1)
```

This is `T_n^{o(1)}` (since `log log T / log T -> 0`), so for any
positive `A`, `T_n^{O(log log T)} <= T_n^{A}` for `T_n` large.
**Confirmed: H-height(A) on strip (R1) is unconditional with A = o(1).**

The user's heuristic intuition was correct for strip (R1); the
quasi-polynomial appearance in my first attempted derivation came from
not invoking (DVP) on the absolute-convergence side of the strip. With
(DVP), the bound is sub-polynomial.

#### 2.C.2  STRIP (R2) :  Re s in [1/2 - alpha, 1/2 + alpha], alpha = 1/log T_n

This is the critical strip near `Re s = 1/2`. Here **(DVP) does not
apply**: there is no unconditional zero-free region of width `>= alpha`
to the right of the critical line. (DVP) gives a region of width
`c_E/log T`, which is exactly `alpha` — i.e., (DVP) gives a
zero-free strip of EXACTLY the rectangle's half-width. So the right
edge `Re s = 1/2 + alpha` MIGHT still be touched by zeros (under GRH it
is not, since all zeros are on `Re s = 1/2`; unconditionally, off-line
zeros with `Re rho in (1/2, 1/2 + c_E/log T)` are not ruled out by
(DVP)).

More importantly, **the rectangle (R2) crosses zeros on the critical
line itself**. At a legal height `T_n` and a zero `rho = beta + i gamma`
with `|gamma - T_n| ~ 1/log T_n`, on the horizontal edge
`Im s = T_n`, `Re s` ranges through `[1/2 - alpha, 1/2 + alpha]`. The
point `s = beta + i T_n` (if `beta in [1/2 - alpha, 1/2 + alpha]`) is
distance `|T_n - gamma| ~ 1/log T_n` from `rho`. The local Laurent
expansion (simple zero, `L_E^*'(rho) != 0`):

```text
|1/L_E^*(s)|  =  |1/L_E^*'(rho)| · |s - rho|^{-1} · (1 + O(|s - rho|))
              =  |1/L_E^*'(rho)| · log T_n · (1 + O(1/log T_n)).
```

The factor `|1/L_E^*'(rho)|` is **uncontrolled unconditionally** for a
general offcentral zero. Even for an on-line zero (under GRH), this is
the object Door A bounds. Without bounds on `|1/L_E^*'(rho)|`,
`|1/L_E^*|` on the horizontal edge of (R2) can be as large as the
worst `|1/L_E^*'(rho)|` for `rho` near height `T_n` — uncontrolled.

**The user's heuristic FAILS on strip (R2)** because:
  1. (DVP) does not cover (R2): the zero-free region's width `c_E/log T`
     is the same as the rectangle's half-width.
  2. Zeros DO lie inside (R2): all GRH-zeros lie at `Re s = 1/2`, which
     is the center of (R2).
  3. The Hadamard local factor at the nearest zero involves the
     uncontrolled `|1/L_E^*'(rho)|`.

**Verdict: H-height(A) on strip (R2) is NOT unconditional today.**
For each legal `T_n`, the closest zero `rho` has `|T_n - gamma| ~
1/log T_n`, and the horizontal-edge bound is

```text
M(T_n)  =  sup_{Re s in [1/2 - alpha, 1/2 + alpha]}  |1/L_E^*(s + i T_n)|
        ~  |1/L_E^*'(rho)| · log T_n.
```

For `M(T_n) <= T_n^A` with `A < 2 = q`, need
`|1/L_E^*'(rho)| <= T_n^A / log T_n`. This is a per-zero bound on the
reciprocal first derivative at a SINGLE chosen zero. Unconditionally
the strongest available is the cumulative `T (log T)^c` bound (from
Heap-Soundararajan), which divided by `T log T` zeros gives mean
`(log T)^{c-1}`, so a TYPICAL zero satisfies the bound; the
WORST-CASE may not.

A more careful reckoning: among `O_E(log T_n)` zeros in the unit
window, by Markov, at most a few can have
`|1/L_E^*'(rho)| > T_n^{(c-1)/2}` (for some moment exponent `c`). So
there exist legal heights `T_n` such that the nearest zero `rho` to
`T_n` is GOOD in the sense `|1/L_E^*'(rho)| <= T_n^{A}` for some
sub-polynomial `A`. Whether `A < 2` can be guaranteed
unconditionally is precisely the X.1 / Door A loose target — but Door A
gives `sum |1/L'|^2 << T^{5/2+eps}`, i.e., a typical `|1/L'|^2 <=
T^{3/2+eps}`. So a typical `|1/L'| <= T^{3/4+eps}`, which is well below
`T^2`. **In fact, on a legal-height subsequence chosen to AVOID the
exceptional zeros (those with `|1/L'|^2 > T^{5/2}/T = T^{3/2}`), the
nearest-zero `|1/L'| <= T^{3/4}` and `M(T_n) <= T^{3/4} log T_n`,
giving `A <= 3/4 + o(1) < 2 = q`.**

This is a much subtler argument than "Hadamard + RvM". It needs:
  - The loose Door A bound `sum |1/L'|^2 << T^{5/2+eps}`
    (unconditional for fixed GL2? NOT YET — this is the X.1 Step 4
    object; the unconditional version requires `int |L|^{-2} dt`
    transfer to derivative sum, which the X.1 audit retracted).
  - A pigeonhole on the rare-bad-zero subsequence.

So even the SALVAGE of H-height(A) on (R2) via "skip bad zeros"
requires the unconditional Door A bound, which is itself open.

**Verdict on 2.C.2: H-height(A) on (R2) is currently OPEN unconditionally,
equivalent to (or implied by) the X.1 Step 4 unconditional question.**

### 2.D  Resulting `H-height(A)` claim  —  STRIP-DEPENDENT

```text
H-height(A) on STRIP (R1)  (Re s in [1 - eta, 1 + sigma], eta < 1/2):
  UNCONDITIONAL with A = o(1).
  Specifically, A = O(log log T_n / log T_n), provable via (DVP) +
  Hadamard + RvM, no GRH.
  Polynomial budget: T_n^{O(log log T_n)} = T_n^{o(1)}, in particular
  A < q for any q > 0.

H-height(A) on STRIP (R2)  (Re s in [1/2 - alpha, 1/2 + alpha]):
  NOT UNCONDITIONAL today.
  Equivalent to controlling |1/L_E^*'(rho)| at the nearest zero rho
  to a legal height T_n, which is the same flavour as Door A / TSDB.
  Salvage via "skip bad zeros" requires unconditional Door A (open).
```

### 2.E  Does this close the rectangle route at T^{15/8+eps} unconditionally?

**No — and the user's prompt §E got the strip wrong.**

The user's §E sets up:
```text
R_Phi(T)  =  (1/2pi i) int_{boundary of rectangle 1/2-alpha to 1/2+alpha, T to 2T}
              Phi_T(s)/L_E^*(s) ds.
```
This is **(R2)**, the critical-line rectangle. The vertical-edge
analysis (X.1 Step 1-3) gives `T^{15/8+eps}` via the unconditional
loose `int |L|^{-2} << T^{11/4+eps}`. The horizontal edges require
H-height(A) on (R2) with `A < 2`, which 2.C.2 shows is NOT unconditional.

The user's §E then asserts horizontal edges contribute
`<< M_T · (1/log T) · (log T)^A`. The factor `(1/log T)` is the
rectangle width `2 alpha = 2/log T`. The factor `(log T)^A` is the
sup of `|1/L|` on the horizontal edge — but on (R2), as 2.C.2 shows,
this sup is `|1/L'(rho)| · log T`, NOT `(log T)^A`. So the user's §E
horizontal-edge bound is **off by a factor of `|1/L'(rho)| / 1`**:

```text
|H_+(T_n)|  <=  M_T · alpha · M(T_n)
             <=  M_T · (1/log T_n) · |1/L_E^*'(rho)| · log T_n
             =   M_T · |1/L_E^*'(rho)|.
```

For this to be `<< M_T · T^{o(1)}`, need `|1/L_E^*'(rho)| <= T_n^{o(1)}`,
which is the SIMPLE-ZERO version of Door A's loose bound applied to a
SINGLE zero. Unconditionally not known.

If we ALSO take the maximum over both horizontal edges and use the
fact that pigeonhole over a thinner subsequence might select
`T_n` where the nearest zero has `|1/L'| <= T^{o(1)}`: this requires
a **typical-zero density-1 simplicity** statement, which is
unconditional only in weak forms (Murty-Najnudel, density `> 1/2`
simplicity).

**Conclusion on 2.E: the rectangle route at (R2) does NOT close
`R_Phi(T) << T^{15/8+eps}` unconditionally today.** The horizontal
edges have the same unconditional gap as Door A's per-zero
`|1/L'(rho)|` control.

#### 2.E'  Could we just use the H1 native rectangle (R1) instead?

The H1 finite-box identity in `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE` IS
already a rectangle at strip (R1). The vertical edges there are at
`Re s = 1 + sigma` (start line, absolute convergence: `|1/L| = O(1)`)
and `Re s = 1 - eta` (shifted line, with the H-left hypothesis).
The H-left hypothesis was identified as closable for `eta > 1/2` in
the repo (HANDOFF.md L130: "With `eta > 1/2`, treat `H-left` as
closed").

For (R1) with `0 < eta < 1/2`, H-left is at most a polynomial-growth
hypothesis on `|1/L_E^*(1 - eta + it)|`, which for `eta` strictly
inside `(0, 1/2)` requires no GRH but DOES require subconvexity-type
input (since `Re(1 - eta) in (1/2, 1)` is INSIDE the critical strip).
This is the standard subconvexity gap.

For `eta > 1/2` (i.e., shifted line `Re s = 1 - eta < 1/2`), the
shifted line is on the OPPOSITE side of the critical line; by
functional equation, `|L_E^*(1 - eta + it)| = |L_E^*(eta + it)| ·
(arch factor)`, where `eta + 1/2 > 1`, putting the shifted line in
absolute convergence on the OTHER side. So `H-left` for `eta > 1/2`
is unconditional.

But then the rectangle (R1) crosses the critical line `Re s = 1/2`
at heights `T` and `2T`. This is now **(R3)**: a rectangle from
`Re s = 1 - eta` (`eta > 1/2`) to `Re s = 1 + sigma`, crossing the
critical line. Critical-line zeros lie inside (R3) and contribute
residues — the **canonical H1 residue sum**. The horizontal edges of
(R3) have the same H-height(A) gap as (R2), since they pass through
the critical line at heights `T, 2T`.

So the H1 native rectangle (R3) and the X.1 / off-halo rectangle (R2)
share the same horizontal-edge obstruction. The "narrow" (R1)
rectangle (which stays in `Re s in [1 - eta, 1 + sigma]` with `eta <
1/2`) DOES have unconditional horizontal edges via (POLYLOG-R1), but
it does NOT pick up any zeros in its interior (all nontrivial zeros
are at `Re s = 1/2`, outside the strip), so its contour integral is
just an absolute-convergence estimate — no T^{15/8} gain, no Door A
sidestep, no novelty.

**The rectangle that gives the `T^{15/8+eps}` exponent is the one
that crosses the critical line and uses the negative second moment
on `Re s = 1/2 + alpha`.** That rectangle inherently has horizontal
edges in the critical strip, which require H-height(A) on (R2)/(R3).

### 2.F  What about the central pole?

The user's §F asks about the pole at `s = 1` (BSD rank). The rectangle
at (R2) `Re s in [1/2 - alpha, 1/2 + alpha]` lies entirely in
`Re s < 1`, so the central pole at `s = 1` is NEVER inside (R2). The
rectangle is at heights `T to 2T`, far from `Im s = 0`, so no
encirclement of `s = 1` is possible.

What IS inside (R2) is the offcentral zeros of `L_E^*` with `Re rho =
1/2` (by GRH, or in the critical strip more generally), `T <= Im rho
<= 2T`. These give the offcentral residue sum.

**Confirmed: the rectangle (R2) is genuinely offcentral.** The
central rank-`r` zero/pole at `s = 1` (BSD) is far away. The
residue sum picks up only offcentral zeros.

For (R1) `Re s in [1 - eta, 1 + sigma]`, eta < 1/2: no zeros inside,
so residue sum is zero, and contour integral = boundary integral.
Useless for H1.

For (R3) `Re s in [eta', 1 + sigma]`, eta' < 1/2: zeros at `Re rho =
1/2` ARE inside, residues picked up. This is the standard H1 contour.
Central pole at `s = 1` IS inside (R3) only if `Im s` range includes
0 — for heights `[T, 2T]` it does not, but for the full H1 (heights
`-T to T`), it does, and the central residue is the polynomial
`Q_{E,W}(u)`.

The user's §F intuition was correct: at heights `[T, 2T]` the central
pole is excluded; the rectangle picks up only offcentral zeros.

### 2.G  Numerator M_T on (R2)

The user's §E derives `M_T_{rect} <= O(T^{-q}) = O(T^{-2})` on (R2)
via the kernel decay of `Phi_T(s) = e^{u(s-1)} W_hat(s-1)`.

```text
|Phi_T(1/2 + x + iT)|  <=  e^{u(x - 1/2)}  ·  |W_hat(x - 1/2 + iT)|
                       <=  e^{-u/2 + u·alpha}  ·  C T^{-q}
                       =   e^{-u/2 + O(u/log T)}  ·  C T^{-q}.
```

For the H1 truncation regime `T = e^{cu}` with `c > 1/2` (per
H1_NUMERATOR_M_T_AUDIT.md), `u = (1/c) log T`, so
`e^{-u/2} = T^{-1/(2c)} <= T^{-1}`. Combined with `T^{-q} = T^{-2}`:
`M_T_{(R2)} <= T^{-3}`. Even more negative power than on the halo.

So on (R2) the numerator is **smaller** than on the halo arcs. The
factor `M_T = T^{1/4}` that the user's §E imported is the wrong M_T;
that was the halo-arc M_T (D(rho, R alpha)). The rectangle M_T is
`T^{-3}`, way below the `T^{1/4}` budget. The Cauchy-Schwarz product
`M_T · T^{1/2} · T^{11/8+eps}` is therefore `T^{-3 + 1/2 + 11/8 +
eps} = T^{-1 - 1/8 + eps}`, MASSIVELY below `T^{15/8}`. **The
T^{15/8+eps} target is comically loose.** The actual rectangle
contribution from vertical edges alone is `T^{-1 + eps}`.

But this is only the VERTICAL edges. The HORIZONTAL edges, with
the H-height(A) unconditional gap, can be MUCH larger.

Wait — the kernel decay on the horizontal edge:
```text
|Phi_T(x + iT)|  <=  e^{u(x - 1)}  ·  |W_hat(x - 1 + iT)|
                  <=  e^{u(alpha - 1/2)}  ·  C T^{-q}
                  =   O(T^{-q})  ·  O(1)
                  =   O(T^{-2}).
```

So even on the horizontal edges, `Phi_T` is `O(T^{-2})`. The
horizontal edge has length `2 alpha = 2/log T`. So the horizontal
contribution is

```text
|H_+|  <=  (2 alpha)  ·  sup_horiz |Phi_T|  ·  sup_horiz |1/L|
        <=  (2/log T)  ·  O(T^{-2})  ·  M(T_n).
```

For this to be useful (say `<= T^{-1}`), need `M(T_n) <= T (log T)/2`,
i.e., `A = 1 + o(1) < 2`. **This is much looser than the user's
heuristic `A < 2` requirement.**

So actually: H-height with `A < 2` suffices structurally, but the
unconditional question is whether `A <= 1 + o(1)` can be proved (a
weaker target than `A < 2`).

Even `A <= 1 + o(1)` requires `|1/L'(rho)| <= T^{o(1)} log T = T^{o(1)}`,
which is the simple-zero version of the conjectural truth. Currently
unknown unconditionally.

**Verdict on 2.G: the rectangle route's quantitative T^{15/8+eps}
target survives at the vertical edges (with a comfortable margin),
but the horizontal edges fail at A < 2 unconditionally; even the
loosest needed A ~ 1 + o(1) is open.**

## 3. Final unconditional bound on R_Phi(T) for fixed E/Q

```text
Theorem (PROVED unconditionally TODAY for fixed E/Q):
  - Hadamard product for L_E^* of order 1.                       (A passes)
  - Legal heights T_n exist with dist(T_n, gamma) >= 1/(12 C_E log T_n).
                                                                  (B passes)
  - H-height(A) on STRIP (R1) Re s in [1-eta, 1+sigma], eta < 1/2:
      A = O(log log T_n / log T_n) = o(1).                       (C.1 passes)

Theorem (NOT PROVED unconditionally TODAY):
  - H-height(A) on STRIP (R2) Re s in [1/2-alpha, 1/2+alpha]:
      no A < 2 known unconditionally.                            (C.2 OPEN)
  - R_Phi(T) <<_E T^{15/8 + eps} via the rectangle (R2):
      depends on H-height(A) on (R2).                            (E OPEN)
  - R_Phi(T) <<_E any sub-T^2 unconditional bound:
      no proved bound exists today.                              (E OPEN)
```

## 4. Comparison with conditional halo route under GRH

| Route | Hypotheses | Exponent on R_Phi(T) |
|---|---|---|
| Halo + Door B + Door A (conditional) | GRH(L_E^*) + Wave 4 | T^{7/4 + eps} |
| Rectangle (R2) (X.1 / §3.5) | unconditional (CLAIMED) | T^{15/8 + eps} |
| Rectangle (R2) (X.1 / §3.5) (actual) | + H-height(A) on (R2), A < 2 | T^{15/8 + eps} |
| Rectangle (R1) (no zeros inside) | unconditional, H-height(o(1)) on (R1) | absolute-convergence estimate, no T^{15/8} gain |

The conditional halo route under GRH gives `T^{7/4+eps} = T^{14/8+eps}`,
strictly better than `T^{15/8}`. The unconditional rectangle target
`T^{15/8+eps}` is interesting only if it survives WITHOUT GRH, but the
H-height(A) audit shows it does NOT (today).

## 5. Significance

```text
Conditional close (under GRH):
  R_Phi(T)  <<_E  T^{7/4 + eps}    (halo route, Wave 4 + Door A conditional)

Unconditional close attempted but UNAVAILABLE today:
  R_Phi(T)  <<_E  T^{15/8 + eps}    (rectangle route, requires H-height(A)
                                     on (R2), A < 2, currently open)

Net: no unconditional sub-T^2 bound on R_Phi(T) for fixed E/Q exists
in the repo today.  The X.1 retraction stands; the rectangle salvage
does NOT close.

The user's heuristic about Hadamard + RvM giving polylog H-height was
correct for STRIP (R1) (a thin slab near Re s = 1, with no
zeros inside via de la Vallee Poussin).  It is INCORRECT for STRIP (R2)
(the critical-line slab Re s in [1/2 - alpha, 1/2 + alpha]), where the
rectangle picks up offcentral zeros and the horizontal-edge sup of
|1/L_E^*| is governed by |1/L_E^*'(rho)| at the nearest zero — the
SAME object Door A bounds, currently open unconditionally.

H-height(A) for FIXED EC unconditional in the required strip (R2) is
the THIRD silent GRH dependency surfaced in today's session, after:
  (i)   Door B's cluster-mate contraction sqrt(1+A^2)/R_T < 1
        (REQUIRES Re rho_j = 1/2 for cluster mates);
  (ii)  X.1 Step 4's "Gallagher-HB to derivative sum"
        (REQUIRES cluster-shift comparison, Door B-conditional).

Pattern: every unconditional route to sub-T^2 R_Phi(T) for fixed
GL2 newform traces back to either Door A (zero-sample reciprocal-
derivative moment) or thin-strip critical-line density (TSDB).  These
are the unconditional bottoms of the well today.
```

## 6. Boundary

### Allowed claims

```text
- (HAD) Unconditional Hadamard product for L_E^* of order 1.
- (B) Unconditional legal heights T_n with dist(T_n, gamma) >= 1/(12 C_E log T_n).
- (POLYLOG-R1) On strip (R1) Re s in [1-eta, 1+sigma], eta < 1/2,
  |1/L_E^*(s + i T_n)| <<_E T_n^{O(log log T_n / log T_n)} = T_n^{o(1)}
  unconditional, on legal heights.
- (DVP-GL2) Hoffstein-Ramakrishnan unconditional zero-free region
  for fixed GL2 cuspidal newform: no zero with Re s >= 1 - c_E/log(|Im s|+2).
- (Strip selection) The rectangle yielding T^{15/8+eps} is (R2),
  Re s near 1/2; its horizontal edges live in the critical strip;
  the unconditional H-height(A < 2) on (R2) is OPEN.
- (Cluster-shift parallel) H-height(A) on (R2) is equivalent in
  difficulty to per-zero |1/L_E^*'(rho)| control, i.e., the simple-zero
  version of Door A.
- (Conditional close) Under GRH(L_E^*) the rectangle (R2) horizontal edges
  ARE controlled by the Door A bound on sum |1/L_E^*'(rho)|^{-2}; the
  rectangle route then closes T^{15/8+eps} conditionally; but
  conditionally one already has the halo route's T^{7/4+eps}, which
  is strictly better.
```

### Forbidden claims

```text
- "H-height(A) is unconditional with A = o(1) for fixed EC, on the
  rectangle (R2)."  FALSE; only on strip (R1).
- "The rectangle route closes R_Phi(T) << T^{15/8+eps} unconditionally."
  FALSE; horizontal edges on (R2) require A < 2 = q, currently open.
- "Hadamard + RvM gives polylog |1/L_E^*| on legal heights in the
  critical strip."  FALSE; only outside the critical strip, where
  (DVP-GL2) supplies the missing input.
- "The Hadamard product argument for L_E^* and zeta are interchangeable
  in the critical strip."  FALSE; zeta's (DVP) zero-free region
  has the same width c/log T as for L_E^*, so neither covers the
  critical strip itself.
```

### Genuine surprises

```text
SURPRISE 1.  The user's prompt claim "for zeta, H-height(A) with A = o(1)
             is UNCONDITIONAL via standard Hadamard + RvM" is CORRECT
             for the zeta analog of strip (R1) (Re s near 1), but is
             FALSE for the strip (R2) (Re s near 1/2) — at any height,
             zeros lie at Re s = 1/2 by GRH (or in the critical strip
             unconditionally), and the local Laurent expansion involves
             |1/zeta'(rho)| which is uncontrolled.  Even for zeta, the
             quantitative bound  |1/zeta(1/2 + alpha + iT)| <= polylog
             at legal heights is open.  The standard "polylog 1/zeta" is
             at Re s = 1 + alpha, NOT Re s = 1/2 + alpha.  The user's
             prompt implicitly imported the absolute-convergence
             intuition to the critical strip.

SURPRISE 2.  The rectangle (R1) (no zeros inside) has trivially unconditional
             horizontal edges but is USELESS for H1 because no residues
             are inside.  The rectangle (R2) (zeros inside) is non-trivially
             useful but has the open horizontal-edge problem.  This
             dichotomy is the fundamental reason the rectangle route
             cannot bypass the TSDB gap: any rectangle that picks up
             critical-line residues must have its horizontal edges
             cross or skirt the critical line, exposing the per-zero
             |1/L'| difficulty.

SURPRISE 3.  The numerator M_T on the rectangle (R2) is O(T^{-2})
             with the H1 native exponential truncation T = e^{cu},
             c > 1/2 — far smaller than the loose bound the
             X.1 audit uses (M_T = T^{eps}).  So the quantitative
             headroom in the rectangle route is enormous.  Even
             H-height(A) with A as large as 1 + 1/8 + eps would still
             give R_Phi(T) << T^{2 - 1/8} sub-T^2.  The hard requirement
             is not A < 2; it is the existence of ANY unconditional
             quantitative bound on M(T_n) better than the trivial
             functional-equation polynomial floor (which gives M(T_n)
             <= T_n^C for some absolute C of order O(1)).

SURPRISE 4.  Even the very loose target A <= O(1) for H-height on (R2)
             — well above the heuristic-conjectural A = o(1) — requires
             a per-zero or supremum-of-per-zero  |1/L'|  bound that the
             repo's conditional halo Wave 4 program (Door A, even at the
             cumulative T^{5/2+eps} level) does NOT directly give:
             cumulative moment bounds the SUM, not the SUPREMUM.
             To get sup-control needs an extra Markov + pigeonhole on
             a thinned legal-height subsequence, and even then the
             unconditional cumulative bound (X.1 Step 2 + retracted
             Step 4) is what's open.  So the rectangle route's
             unconditional close is strictly harder than the cumulative
             Door A bound, even though it appears formally weaker.

SURPRISE 5.  The user's prediction "H-height(A) for fixed EC is
             UNCONDITIONAL, via standard Hadamard + RvM" was the
             correct intuition for the WRONG strip.  The audit's
             headline is therefore that H-height(A) is the THIRD
             silent GRH/TSDB dependency surfaced today.  All three
             dependencies — Door B, X.1 Step 4, H-height(A) on (R2)
             — reduce to the same family of thin-strip critical-line
             density / per-zero reciprocal-derivative open problems.
```

### Probability ledger

```text
0.95  (HAD) Unconditional Hadamard product for L_E^* (textbook).
0.95  (B) Unconditional legal-heights pigeonhole.
0.90  (POLYLOG-R1) Unconditional polylog |1/L_E^*| on (R1) via (DVP-GL2) + Hadamard.
0.10  H-height(A) on (R2) is unconditional with A < 2 today.
0.05  H-height(A) on (R2) is unconditional with A = o(1) today.
0.55  Within 1-2 months, an unconditional H-height(A) on (R2) with A < 2
      can be proved via a "skip bad zeros" pigeonhole + closing the
      X.1 Step 4 cumulative bound on |1/L'|^2.
0.30  The unconditional rectangle close at T^{15/8+eps} is reachable
      in 2-3 months via either (i) Bui-Florea-GL2 extension or
      (ii) zero-density + density-1 simplicity weakening.
0.15  A different unconditional route (not enumerated) closes
      R_Phi(T) << T^{2 - eta} for some eta > 0.
0.10  R_Phi(T) is genuinely T^{2+o(1)} unconditionally (no sub-T^2
      bound exists in principle for fixed EC).
```

## 7. Recommendation

```text
1.  EDIT  X1_UNCONDITIONAL_BOUND_AUDIT_2026-05-14.md  §F  to note
    that the rectangle "salvage" does NOT close H-height(A) on the
    relevant strip (R2); the polylog argument the user sketched in
    that audit's §F applies to (R1), not (R2).  Downgrade the
    rectangle-route confidence from 0.55 to ~0.35.

2.  Add  H-height-(R2)-Unconditional  to the project's open-problems
    register at the same level as Door A / Door B.  All three are
    flavours of TSDB / thin-strip critical-line density.

3.  Audit the X.1 Step 4 cumulative bound on sum |1/L'(rho)|^2:
    if it can be unconditionally closed at T^{5/2+eps}, then a
    pigeonhole on a thinned legal-height subsequence gives
    H-height(A) on (R2) with A = 3/4 + o(1) < 2, closing the
    rectangle route at T^{15/8+eps}.  This audit is currently the
    single most leverage-bearing piece of unconditional work.

4.  DO NOT promote the rectangle-route unconditional close in the
    paper-prep tracker.  The fallback should remain "conditional halo
    route under GRH gives T^{7/4+eps}".

5.  Distinguish carefully in all future writeups between strip (R1)
    (near Re s = 1, no zeros inside, polylog via DVP) and strip (R2)
    (near Re s = 1/2, zeros inside, per-zero reciprocal-derivative
    control needed).  These two strips have been conflated in earlier
    discussion (X.1 §F, halo plan §3.5, off-halo §13) and the
    conflation is the source of the apparent rectangle-route salvage.

6.  Re-state  H-height-(R1)-Unconditional  as a clean named lemma at
    the same level as RvM-MULT.  Its proof is two lines: (DVP-GL2)
    on the absolute-convergence-side boundary of the strip, plus
    Hadamard on the local in-strip contribution at legal heights.
    Useful for H1 native truncation, just not for the X.1 / rectangle
    sub-T^2 goal.
```
