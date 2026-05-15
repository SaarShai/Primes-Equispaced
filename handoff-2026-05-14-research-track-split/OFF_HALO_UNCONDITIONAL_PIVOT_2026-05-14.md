---
schema_version: 2
title: "Off-Halo Unconditional Pivot — Routes I-X exploration"
type: exploration
domain: project
tier: working
status: EXPLORATION
confidence: 0.55
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff pro.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/UNCONDITIONAL_DOOR_B_ANALYSIS_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/UNCONDITIONAL_DENSITY_METHOD_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-04-theorem-B-and-C1/AtZeros_log3_attempt.md
  - primes-equispaced/handoff-2026-05-09-followup/B_prime_denom_Selberg_Beurling_assessment.md
  - Conrey-Iwaniec, "The cubic moment of central values of automorphic L-functions",
    Annals of Math. 151 (2000), 1175-1216; arXiv:math/9810182
  - Good 1982 (GL2 4th moment t-aspect, T^{2+eps} unconditional for fixed form)
  - Meurman (zeta 4th moment refinement; classical)
  - Iwaniec-Kowalski, "Analytic Number Theory", Ch. 5, 11, 24
  - Iwaniec-Sarnak 2000, "Perspectives on the analytic theory of L-functions" (GAFA 2000)
  - Duke-Friedlander-Iwaniec (subconvexity for GL2)
  - Heath-Brown 1979 / 1981 (zeta zero-density, fractional moments)
  - Blomer-Harcos / Michel (bilinear / family bounds for GL2)
  - Soundararajan, "Moments of the Riemann zeta function", Annals 2009
  - Selberg, S(T) central-limit work
  - Hughes-Keating-O'Connell 2000 (RM model for J_{-k}(T))
  - BFMT, arXiv:2310.03949
  - Bui-Florea, arXiv:2302.07226
  - Booker 2014 (infinitely many simple zeros for GL2 newforms, unconditional)
  - Tao-Helfgott / Maynard (additive-combinatorial GRH-bypasses)
  - WebSearch 2026-05-14: ETH Kowalski "second-moment-theory of families of L-functions"
    survey notes; AIM L-functions RMT volume
supersedes: []
superseded-by:
tags: [halo-route, unconditional, off-halo, pivot, exploration, trace-formula, subconvexity, hadamard, additive-combinatorics]
---

# Off-Halo Unconditional Pivot — Routes I-X

## 0. Frame and notation

Fixed: `E/Q` elliptic curve of conductor `N_E`, `L_E^*(s) = L(E, s+1/2)`
analytically normalized GL2 newform, critical line `Re s = 1/2`, height
parameter `T -> infinity`, scale `alpha = 1/log T`, dyadic window
`gamma in (T, 2T]`, offcentral simple zero set `Z_T = {rho = 1/2 + i gamma}`.

Target object (offcentral H1):

```text
R_Phi(T)  =  sum_{rho in Z_T} W_hat(i gamma) / L_E^*'(rho)
                 + (multiple-zero residues)
          =  o(T^2),     unconditionally in E.
```

By the residue-first audit (`H1_RESIDUE_FIRST_AUDIT_2026-05-14.md`) this
is equivalent to the absolute sufficient condition

```text
(H-abs-r)  :   R_B(T)  =  sum_{rho in Z_T} |W_hat(i gamma)| / |L_E^*'(rho)|
                       =  o(T^2).
```

Same paper's Risk R1 also entertains a signed contour residue form;
either form suffices.

The "thin-strip density blocker" (TSDB) is shorthand for:

```text
(TSDB)  :  for any eta > 0,
   #{ rho_0 in Z_T : exists rho_j with |gamma_0 - gamma_j| <= A/log T
                      and |Re rho_j - 1/2| > 1/log T }
         <<_{E, eta}  T^{1 - eta} log T.
```

This is the obstruction the three previously-failed routes (Halo Door B,
density method §8.3, Palm direct break) all converge on. The user asked
for routes that do NOT reduce to (TSDB).

---

## 1. Headline verdict

```text
verdict:  NO.

Best off-halo candidate (PARTIAL):
   Route X "strategic retreat" via family-averaged H1 over a thin
   newform family (Conrey-Iwaniec cubic-moment-style positivity),
   conditional on a still-unwritten Saar-Koyama main-theorem audit
   that says family-averaged H1 suffices.

Genuinely unconditional, individually-for-E:  NONE.
```

Concise rationale.

```text
- Routes I, III, VI, VII, VIII are GL2-zero-location facts in different
  clothing.  Each reduces to (TSDB) in <= 1 step of expansion.
- Routes II, IV, V, IX provide bounds on the WRONG OBJECT (positive
  moments of |L|, not negative moments of |L'|).  Any inversion either
  re-introduces (TSDB) (Routes II, IV t-aspect) or shifts to a
  family-averaged statement that gives no fixed-E conclusion (Routes
  IV family, V).
- Route IX (additive combinatorics) is structurally absent: the residue
  R_Phi(T) is a spectral object on the GL2 side, not on the prime side;
  no AC framework controls 1/L'(rho).
- Route X is the only escape that is internally consistent, but it
  REPLACES the H1 conclusion by a weaker family-averaged statement,
  and currently no document in the project says this is sufficient
  for the joint Saar-Koyama main theorem.  Pending that audit, Route
  X is conditional-on-paper-architecture, not on analytic input.
```

The bottom line is **the same finding** as `UNCONDITIONAL_DOOR_B`
and `UNCONDITIONAL_DENSITY_METHOD`: pointwise control of the offcentral
zeros of `L_E^*` near the critical line is the central GL2 open problem,
and no published technique sidesteps it for individual fixed `E`.

---

## 2. Route I — Halo §8.1: direct rectangle + mollified second moment

### 2.1 Mechanism

Conrey-Iwaniec-style mollifier `M(s) = sum_{n<=M_0} mu_E(n) P(log(M_0/n)/log M_0) n^{-s}`
of length `M_0 = T^{theta}`, `theta < 1/2`. Target the identity

```text
int_T^{2T} |L_E^*(1/2 + alpha + it) M(1/2 + alpha + it)|^2 dt   <<_E   T (log T)^{O(1)}.
```

Combined with `sup_{t in G} |(LM)^{-1}|^2` on a "good" set `G` of measure
`>= T (1 - o(1))`, would deliver

```text
int_G |L_E^*(1/2+alpha+it)|^{-2} dt  <<_E  T (log T)^{O(1)}  ·  sup_{G} |M|^2.
```

### 2.2 Where the "good set" lives

A mollifier acts as an approximation to `L^{-1}`. For `LM` to be
close to `1`, the mollifier must approximate the inverse Dirichlet
series of `L_E^*`. This Dirichlet inverse converges absolutely only for
`Re s > 1`. On the shifted line `Re s = 1/2 + alpha`, the partial sum
`M` matches `1/L` only when no zero of `L_E^*` lies inside the
"mollification window" of radius `~1/log M_0 = (1/theta) alpha`
around the evaluation point.

### 2.3 Why this reduces to (TSDB)

The good set `G` is

```text
G  :=  { t in [T, 2T]  :  no zero rho_j of L_E^* has
                          |Re rho_j - 1/2|  <  (1/theta) alpha
                          and  |gamma_j - t|  <  (1/theta) alpha }.
```

`|G^c|` is bounded by the number of zeros in the strip
`{ Re s in (1/2, 1/2 + (1/theta) alpha) }` of height `<= T`, times the
window width `(1/theta) alpha`:

```text
|G^c|  <=  #(thin-strip zeros up to T)  ·  (1/theta) alpha.
```

Producing `|G^c| = o(T)` requires `#(thin-strip zeros) = o(T log T)`,
which is exactly **(TSDB)**. Without it, the bad set carries the full
mass, and the mollifier is useless on the bad set (Iwaniec-Sarnak
Perspectives §7 / DKM 2000 record this exact obstruction in level
aspect; t-aspect is harder).

The mollifier degree `D ~ 1/(theta · alpha) = (log T)/theta` blows the
prefactor `M^{D+1}` on its own (this is the well-known degree-blowup
obstruction recorded in
`B_prime_denom_Selberg_Beurling_assessment.md` L367-374), and the
remaining handle on the bad set is exactly (TSDB).

### 2.4 Verdict

```text
Route I  ->  (TSDB).   Same blocker as halo Door B / density §8.3.
```

Additional reading: `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.5
uses the mollifier output in combination with the bad-set
Heap-Soundararajan move; the Heap-Sound move IS the partial unconditional
substitute, but it requires the same (TSDB)-style input (Selberg
Sound. upper bound technique conditional on RH); see Route III below.

---

## 3. Route II — Halo §8.4: random-matrix upper-tail t-aspect

### 3.1 Mechanism

Hughes-Keating-O'Connell 2000 predict, for `U(N)` random matrix,

```text
sum_{theta_j}  |Z'(theta_j)|^{-2}  =  O(N)         w.h.p.,
P(  |Z'(theta_j)|^{-1}  >  V  )  =  C V^{-3 + o(1)}     (one-tail).
```

If a fixed GL2 newform satisfies the **upper-tail Katz-Sarnak** in
`t`-aspect at the matching scale, then

```text
sum_{rho in Z_T}^{mult}  |L_E^*'(rho)|^{-2}   <<_E   T (log T)^{O(1)}.
```

This is `c = 1` in the (`UNCONDITIONAL_DENSITY_METHOD_2026-05-14.md`)
notation: conjecturally true, and `c < 3` would close H1.

### 3.2 Why "upper-tail Katz-Sarnak in t-aspect" is itself (TSDB)-adjacent

Katz-Sarnak for t-aspect of a fixed GL2 form is presently known only
in averaged form (Iwaniec-Luo-Sarnak, family-aspect; KMV, level-aspect).
The t-aspect for individual fixed newform requires a one-tail estimate
on `|L_E^*'(rho)|^{-1}`. The standard route to such tails (Conrey-Soundararajan
Annals 2002 mode for zeta; analog open for fixed GL2) uses:

```text
log |L'(rho)|  =  log|L(rho + alpha)|  +  log(1/alpha)  +  small,
                     valid for rho simple AND on the critical line.
```

This is the Kirila identity. As section
`UNCONDITIONAL_DENSITY_METHOD_2026-05-14.md` §3.1 records, Kirila is
RH-conditional at step 1. **Off the critical line, the identity breaks
and an offcentral cluster mate of `rho` creates an uncontrolled tail of
`|L'(rho)|^{-1}` exactly when (TSDB) fails.**

### 3.3 Are there averaged versions that suffice?

Two natural averagings.

```text
(a) Family-average over weight: KMV Cor. 1.3 (Invent. 2000) gives an
    unconditional 4th moment of L (not L') averaged over weight-k cusp
    forms of fixed level. The shift to L' is doable (a log-factor
    contour shift, cf. `THEOREM_B_HANDOFF.md` L19).
(b) Family-average over level: Iwaniec-Sarnak 2000 / Duke-Kowalski-
    Michel 2000 give unconditional second moments shift-uniform on
    Re s in (1/2, 1).
```

For (a) and (b): both give bounds **averaged over the family**, not for
the fixed `E`. To extract the fixed-`E` value, the standard mechanism
is *positivity* (drop the diagonal `f = E` from a sum of `|...|^2` terms
indexed by `f` in the family) PLUS *spectral isolation* (Petersson trace
formula with prescribed local ramifications, à la AJM/JHU 2020). Spectral
isolation in t-aspect for a fixed form is **not** an output of the
trace formula — trace formula isolates by level/weight, not by the
height of zeros of a single fixed form.

Verdict on (a) and (b): they yield family-averaged statements only.

### 3.4 Verdict

```text
Route II  ->  (TSDB) for individual E in t-aspect.
            ->  family-averaged H1 only.  Punt to Route X.
```

---

## 4. Route III — Halo §8.5: subharmonic three-circles bootstrap

### 4.1 Mechanism

`log|L_E^*|` is subharmonic on the right of any vertical line on which
`L_E^*` has no zero. The three-circles inequality on a strip of width
`O(alpha)` reads

```text
log|L(1/2+alpha+it)|^{-1}
   <=  (1/2) log|L(1/2 + 2 alpha + it)|^{-1}  +  (1/2) log|L(1/2 + it)|^{-1}
   +  (boundary terms).
```

Iterate: bound the RHS deeper-half-plane term by Rankin-Selberg
polynomial lower bound `|L| >= T^{-c_E}` (unconditional), and try to
absorb the critical-line term into a Soundararajan-Selberg upper-bound
machine.

### 4.2 Why the bootstrap stalls at (TSDB)

`log|L|` is **subharmonic only when `L` has no zeros**. On the strip
`1/2 < Re s < 1/2 + alpha` of height `T`, `L_E^*` has

```text
#{ thin-strip zeros }  =  N(1/2+alpha, T)  =  ???
```

This count is precisely the (TSDB) object. If thin-strip zeros are
plentiful, `log|L_E^*|` *fails* subharmonicity on the relevant disks;
each thin-strip zero adds a `-log|s-rho_j|` singularity to `log|L|`
which the maximum principle re-expresses as a per-zero cost
`|log(R/r)| = O(log T)`. Summing over `N(1/2+alpha, T)` zeros gives a
total cost of `O(log T · N(1/2+alpha, T))`. To absorb into `T^{o(1)}`
needs `N(1/2+alpha, T) = o(T^{eps}/log T)`, which is a much stronger
form of (TSDB).

The bootstrap iteration multiplies the bad-disk count rather than
shrinking it. **No convergence.**

This was noted as "only a patch" in `HALO_UNCONDITIONAL_PLAN_2026-05-12.md`
L789-793 and the diagnosis confirms it: iteration only helps if each step
strictly reduces the number of effective zero-singularities, which
requires (TSDB).

### 4.3 Verdict

```text
Route III  ->  (TSDB).
```

---

## 5. Route IV — Trace formula / Petersson-Kuznetsov

### 5.1 The most-interesting direction

The Petersson trace formula

```text
sum_{f in B_k(N), Petersson normalized} lambda_f(m) lambda_f(n)
   =  delta_{m=n}  +  (Kloosterman sum / Bessel function diagonal)
```

is **fully unconditional**, no GRH used, gives access to averages of
arithmetic objects over a basis. Kuznetsov is the spectral analog for
Maass forms / GL2 Eisenstein series. Both give unconditional spectral
identities.

Three things one might hope:

```text
hope 1.  Sum over family { L(f, s) : f in B_k(N) } the H1-style residue
         R_Phi^f(T), get cancellation, isolate fixed E by positivity.
hope 2.  Use a Conrey-Iwaniec cubic moment to bound an individual
         |L_E^*(1/2 + it)|^3 directly.
hope 3.  Use a trace-formula identity to convert sum over zeros of
         L_E^* into a prime-side object (cf. explicit formula but
         family-averaged).
```

### 5.2 Hope 1 — averaged R_Phi over the family

R_Phi for f in the family is

```text
R_Phi^f(T)  =  sum_{rho_f in Z_T(f)} W_hat(i gamma_f)/L_f^*'(rho_f) + multiple.
```

Sum over f weighted by Petersson:

```text
sum_f h_f  R_Phi^f(T)
  =  sum_f h_f  sum_{rho_f}  ...   (no obvious cancellation —
                                    L'-zeros of different f are
                                    not aligned)
```

This is **not** a Petersson-type sum (it sums `1/L'` at zeros, not
`lambda_f(m) lambda_f(n)`). One can re-express each `1/L'(rho_f)` as a
contour integral of `(1/L)(s)` around `rho_f`, then attempt to apply
Petersson to the resulting double sum. The result is a **family-averaged
H1** statement. Conditional on the family-averaged statement being
sufficient for the joint paper's main theorem (it isn't, currently — see
Route X), this is an unconditional handle. By itself, it isolates **no
fixed E**.

The positivity move "drop diagonal `f = E`" fails: `R_Phi^f` is not
manifestly positive (it is a signed contour residue aggregate), and the
absolute series `R_B^f` is positive but does not satisfy a family-level
positivity bound because the family lower bound on `sum_f R_B^f` is
itself not known.

### 5.3 Hope 2 — Conrey-Iwaniec cubic moment

Conrey-Iwaniec (Annals 151 (2000) 1175-1216, arXiv:math/9810182) prove
**unconditionally**

```text
sum_{f in S_2^*(N), |L(f, 1/2) > 0|}  L(f, 1/2)^3  <<_eps  N^{1+eps}.
```

This is a *central-value cubic moment*, level-aspect, not t-aspect, not
at zeros. To convert to H1 for a fixed `E`:

```text
L(E, 1/2)^3  <=  N_E^{1+eps}      (trivially from Conrey-Iwaniec).
```

This is a *subconvexity-style* pointwise bound at the central point. It
gives **no information about** sum_{rho in Z_T(E)} 1/L_E^*'(rho).

Cubic moment cannot reach `|L'(rho)|^{-1}` because the third moment of
`L(f, 1/2)` says nothing about `L`-prime values.

### 5.4 Hope 3 — trace-formula explicit formula

The Voronoi summation formula (a Petersson-derived identity) re-writes
sums of `lambda_E(n) e(...)` as sums of `lambda_E(n) e(...)` with
different parameters. It does NOT re-write `1/L'(rho)` as a prime-side
object. The explicit formula `sum_rho W_hat(i gamma) = (smooth) -
sum_p Lambda_E(p) W(...)` does, but it gives `sum 1`, not `sum 1/L'`. There
is no trace-formula identity in the literature that converts
`sum 1/L_E^*'(rho)` into a prime-side sum for fixed `E`.

### 5.5 Verdict

```text
Route IV  ->  family-averaged H1 only (Hope 1).
              No fixed-E unconditional handle from trace formula.
              Conrey-Iwaniec cubic moment delivers a subconvexity for
              central values, not for sum 1/L_E^*'(rho).
```

This is genuinely the closest the trace formula gets, and it falls
short. Punt to Route X.

---

## 6. Route V — Subconvexity-based H1

### 6.1 Mechanism

Unconditional subconvexity for `L(E, 1/2 + it)`:

```text
|L_E^*(1/2 + it)|  <<_E  (1 + |t|)^{1/3 + eps}     (Iwaniec-Sarnak,
                                                    Duke-Friedlander-Iwaniec,
                                                    Blomer-Harcos refinements).
```

Could this directly bound `sum 1/L_E^*'(rho)` ?

### 6.2 Why subconvexity does not help

`R_Phi(T)` is a sum over zeros of an *inverse* derivative:

```text
1/L'(rho)  =  lim_{s -> rho}  (s - rho) / L(s) .
```

Subconvexity bounds `|L(s)|` **above** on the critical line. To get a
useful bound on `1/L'(rho)`, we need either:

```text
(a) a lower bound on  |L'(rho)|,   OR
(b) a way to use the upper bound on |L| at a *different* point.
```

For (a): a lower bound on `|L'(rho)|` is essentially a non-trivial lower
bound on the spacing-renormalized derivative of `L` at a zero, which is
**a zero-spacing statement** equivalent to a lower bound on local zero
density on a thin strip — again (TSDB)-adjacent. Conrey-Ghosh have
conditional results; unconditional is open.

For (b): the explicit formula

```text
1/L_E^*'(rho)  =  (1/(2 pi i)) oint_{|s-rho|=alpha}  ds / L_E^*(s)
              =  (1/(2 pi i)) oint_{|s-rho|=alpha}  ds · M(s)/(L(s) M(s)),
```

with `M` a mollifier, reduces to Route I — same (TSDB) obstruction.

Subconvexity for `L'` itself (Conrey-Ghosh) requires `RH` and is
conditional. Subconvexity for `1/L'` is not even formulated unconditionally.

### 6.3 What subconvexity does buy: a polynomial pointwise floor

The **only** unconditional use of subconvexity in this story is:

```text
|L_E^*(1/2 + alpha + i t)|  >=  T^{-C}     for SOME C > 0,
                                            ALL t in [T, 2T].
```

This is the trivial *polynomial nonvanishing* floor from convexity
plus the Hadamard product order bound. It controls the bad set
`|L|^{-1} > T^{C}` at the bottom of the bad-set integral
(`CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.5, used in
`UNCONDITIONAL_DOOR_B_ANALYSIS_2026-05-14.md` §4.1 (P2)). It is the
"safety net" pointwise lower bound, NOT a route to H1.

### 6.4 Verdict

```text
Route V  ->  (TSDB) or open.
             Subconvexity bounds |L|, not |L'|^{-1} at zeros.
             Trivial pointwise floor is the only unconditional use
             and is independent of T's height.
```

---

## 7. Route VI — Mean-Lindelöf for L_E^*

### 7.1 Mechanism

Mean-Lindelöf in t-aspect for a fixed GL2 form is the statement

```text
int_T^{2T}  |L_E^*(1/2 + it)|^{2k}  dt   <<_{E, k}  T^{1 + eps}.
```

For `k = 1`: known unconditionally (Rankin-Selberg).
For `k = 2`: known with `T^{2 + eps}` only (Good 1982, Meurman); the
sharp `T^{1+eps}` is the GL2 4th moment Lindelöf-on-line, OPEN.

For higher `k`: not known. Conrey-Iwaniec's cubic moment is the closest
existing handle and is level-aspect, not t-aspect.

### 7.2 What mean-Lindelöf would give

Hypothetically: mean-Lindelöf in `k = 2` plus Heap-Soundararajan
gives

```text
ContShiftNeg_2(E)  =  int_T^{2T} |L_E^*(1/2 + alpha + it)|^{-2} dt
                  <<_E  T^{1 + eps},
```

i.e. matches the conjectural-truth value. With Gallagher-HB transfer
(`CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.6), this becomes

```text
sum_{rho in Z_T}^{mult}  |L_E^*'(rho)|^{-2}   <<_E  T^{1+eps},
```

which is `c = 1` exactly, more than enough for H1 (`c < 3` would do).

### 7.3 Why this still reduces to (TSDB)

The Heap-Soundararajan bad-set move re-introduces the bad-set
cardinality bound at `Re s = 1/2 + alpha`:

```text
|B|  <=  |L|^{-2k}-budget  ·  (some 2k power)   /  (Markov).
```

The bad set is precisely the set of `t` where `L_E^*(1/2 + alpha + it)`
is small, which is the set where a zero of `L_E^*` lies within `alpha`
of `1/2 + alpha + it` in the shifted-line strip. The bad-set cardinality
is governed by the thin-strip zero count, which is (TSDB).

If we had **unconditional `k = 2` mean-Lindelöf**, the calibration in
§2.5 would close with `T^{1 + eps}` directly, NOT through the bad-set
machinery, and we would have an unconditional ContShiftNeg_2. But the
`k = 2` mean-Lindelöf is itself OPEN, of the same difficulty as the
Lindelöf hypothesis for `L_E^*` on the critical line.

### 7.4 Verdict

```text
Route VI  ->  open (Lindelöf-equivalent), not (TSDB).
             Mean-Lindelöf at k = 2 in t-aspect for fixed GL2 is the
             cleanest single statement that would CLOSE H1
             unconditionally, but it is independently open and is NOT
             a strictly weaker problem than (TSDB).  It is comparable.
```

This is the cleanest formulation of the open obstruction: **fixed-E
unconditional H1 reduces, via the cleanest known route, to fixed-E
unconditional Lindelöf for the 4th moment of `L_E^*` on the critical
line**. This is a slightly different open problem from (TSDB) but at
comparable depth. Worth noting.

---

## 8. Route VII — Mellin-Barnes / zero-avoiding contour

### 8.1 Mechanism

Reformulate `R_Phi(T)` as a Perron-style integral

```text
R_Phi(T)  =  (1/(2 pi i))  int_C  W_hat(i gamma)/L_E^*(s)  ds,
```

choosing the contour `C` so that it AVOIDS all zeros of `L_E^*`. Then
push `C` into a half-plane of absolute convergence where `1/L_E^*` has a
clean Dirichlet series, and absolute bounds become trivial.

### 8.2 Why this does not work

`R_Phi(T)` is a **discrete** sum over zeros, equal by residue calculus
to a contour integral around the zeros. To re-express as an integral
that avoids zeros, we must add cancelling residues — that is, the original
contour integral plus its boundary segments must equal the zero sum, by
the residue theorem. There is no contour that is BOTH `O(T^2)` in length
AND avoids all `O(T log T)` zeros AND lies in a half-plane where `1/L`
has small Dirichlet series.

Specifically: any vertical contour `Re s = sigma` with `sigma > 1` lies
in the absolute convergence region of `1/L_E^*`, and the contour integral
of `|W_hat(i (Im s))|/|L_E^*(s)|` over height `[T, 2T]` is
`<<_E T`, which is `o(T^2)` trivially. **But**: by the explicit
formula / residue theorem, this contour integral equals R_Phi(T) PLUS
the residue accumulation from the rectangle's other three sides. The
rectangle's bottom (`Im s = T`) and top (`Im s = 2T`) sides contribute
`O(T^2 / inf|L|)` to the rectangle integral, which is uncontrolled
without knowing `inf|L_E^*|` on those horizontal lines. The horizontal
"shifted" sides have the same problem as Route I.

This is the standard issue in zero-density / contour-shift theorems: a
zero-free contour exists, but moving the residue computation TO that
contour requires the contributions of all four sides of the rectangle
to be small. The "near-critical-line" sides re-introduce (TSDB), and
the horizontal sides require **horizontal zero-free regions for L**,
which is essentially a uniform lower bound on `|L|` at horizontal cuts,
which is also open.

This is recorded in `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`:

```text
Finite-box identity and legal heights are clean;
horizontal/left tails reduce to H-height and H-left.
```

i.e., the contour reformulation IS available but the tails reduce to
the same set of unconditional zero-location problems.

### 8.3 Verdict

```text
Route VII  ->  (TSDB)  +  horizontal zero-free regions
             (which is in spirit a STRONGER open problem than (TSDB))
```

---

## 9. Route VIII — Hadamard product

### 9.1 Mechanism

The Hadamard product

```text
L_E^*(s)  =  e^{A + B s} prod_{rho}  (1 - s/rho) e^{s/rho}
```

is **unconditional**. The product is over all (trivial and non-trivial)
zeros of `L_E^*` with multiplicity.

Logarithmic derivative:

```text
L_E^*'(s)/L_E^*(s)  =  B  +  sum_{rho}  ( 1/(s - rho)  +  1/rho ).
```

At a simple zero `rho_0`, take `s -> rho_0`:

```text
L_E^*'(rho_0)/0   =   B + 1/0 + sum_{rho != rho_0} (1/(rho_0 - rho) + 1/rho).
```

This is `infinity = infinity + finite`, undefined. The Hadamard product
identifies `L_E^*'(rho_0)` via

```text
L_E^*'(rho_0)  =  L_E^*'(rho_0).
```

i.e. the product representation gives no closed form for `L'` at a zero.

### 9.2 Genuine attempt: Jensen's formula

Apply Jensen's formula on the disk `D(rho_0, r)`:

```text
log |L_E^*'(rho_0)|  =  (1/(2 pi))  int_0^{2 pi} log|L_E^*(rho_0 + r e^{i theta})| d theta
                       -  sum_{rho in D \ rho_0} log|r / (rho_0 - rho)|
                       -  log(r)    (the pole of (s - rho_0)^{-1} from
                                     extracting the (s-rho_0) factor).
```

This is a valid identity. The integral term `int log|L|` is **upper-bounded**
by integrating against `|L|^2` via Cauchy-Schwarz (Jensen via Hardy /
arithmetic-geometric mean). For fixed `E`, `int_0^{2 pi}log|L_E^*(rho_0 +
r e^{i theta})| d theta` is bounded by a polynomial in `log T` using
the convexity bound; this requires no GRH.

The dangerous term is the sum over cluster zeros `rho in D(rho_0, r)`:

```text
-  sum_{rho in D \ rho_0}  log|r / (rho_0 - rho)|.
```

For `rho` very close to `rho_0`, `log|r/(rho_0 - rho)|` is large positive,
so this term is large negative, making `log|L_E^*'(rho_0)|` very negative,
i.e. `|L'(rho_0)|` very small, i.e. `1/|L'(rho_0)|` huge. Summing over
`rho_0` recovers the cluster-size-dependent obstruction. The number of
cluster mates of `rho_0` is again the bounded by (TSDB)-style local
zero-density.

### 9.3 Verdict

```text
Route VIII  ->  (TSDB)  (via cluster sum in Jensen's formula).

The Hadamard product gives an unconditional identity, but the identity
moves the problem to controlling the local cluster of `rho_0`'s zeros,
which is exactly the (TSDB) object.
```

This is essentially Route III in different clothes; both are local
harmonic-analysis identities and both stall at the cluster-mate count.

---

## 10. Route IX — Additive combinatorics / GRH-bypass

### 10.1 Mechanism

Helfgott (ternary Goldbach), Tao-Maynard (gaps in primes), Maynard
(primes in arithmetic progressions) have all built unconditional
prime-distribution results that **bypass** the corresponding GRH input.

Could there be a similar GRH-bypass for `R_Phi(T)`?

### 10.2 Structural obstruction

These additive-combinatorial bypasses work because:

```text
(i)  The target object lives on the PRIME side (counts of primes
     in some set).
(ii) GRH would have controlled a sum sum_p f(p), but density-increment /
     sieve method gives a direct sum_p f(p) bound without going
     through GL_1 zero distribution.
```

Both (i) and (ii) require the target to be a PRIME-SIDE object. Our
target is a SPECTRAL-SIDE object:

```text
R_Phi(T)  =  sum_rho  W_hat(i gamma) / L'(rho).
```

By Perron / explicit formula, the spectral sum can be re-expressed as a
prime-side sum, but the conversion requires the WEIGHT `W_hat(i gamma) /
L'(rho)`. The weight `1/L'(rho)` does NOT have a prime-side representation
that converges absolutely. (The Selberg-Delange / Mertens reciprocal
involves `mu_E`-coefficients and only converges for `Re s > 1`; pulled
to the critical line, the resulting prime-side sum has `T^2`-size
fluctuations precisely *because* of the zero-cluster issue.)

So: there is no prime-side reformulation of `R_Phi(T)` whose smallness
is even *equivalent* to additive-combinatorial control of primes. The
problem is dual on the spectral side, and additive combinatorics
operates dually on the prime side.

A possible counterexample: could there be an additive-combinatorial
identity for `sum_p Lambda_E(p) / p^{1/2 + alpha + i gamma_0}` that
bypasses GL2 zero density? The answer is essentially no — Selberg's
identity for `Lambda_E` is the *only* known additive identity, and it
loops back to the explicit formula.

### 10.3 Verdict

```text
Route IX  ->  structurally absent.
             AC operates on the prime side; `R_Phi(T)` is spectral.
             No conversion preserves smallness.
```

---

## 11. Route X — Strategic retreat: weaken H1

### 11.1 The retreat options

The H1 conclusion `R_Phi(T) = o(T^2)` is currently used in the
Saar-Koyama joint paper's main theorem (paper-prep tracker). The
retreat options:

```text
(X.1)  Replace o(T^2) by  R_Phi(T)  <<_E  T^{2 - eta}   for some
       eta > 0.

(X.2)  Replace pointwise-in-E by family-averaged:
            E_{f in family of weight K, level N} R_Phi^f(T)  =  o(T^2),
       with `family` thin enough to include `E` non-trivially.

(X.3)  Replace t-aspect by height-aspect average:
            average over T in dyadic window  R_Phi(T) / T^2  ->  0.

(X.4)  Replace H1 (full smoothing) by a weakened smoothing identity
       that requires only `R_Phi(T) << T^2 (log T)^{-A}` for fixed A.
```

### 11.2 Cost-benefit analysis of each retreat

For (X.1): **achievable unconditionally**, via the
`CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.5 calibration with
unconditional 4th moment `T^{2+eps}` (Good/Meurman). Specifically:
that calibration yields

```text
int_B |L|^{-2}  <<  T^{11/4 + eps}.
```

For the full `sum_{rho} |L'(rho)|^{-2}` (via Gallagher-HB transfer),
the bound is `T^{11/4 + eps}`. Cauchy-Schwarz gives

```text
R_Phi(T)  <=  sqrt(T log T)  ·  sqrt(T^{11/4+eps})   =  T^{15/8 + eps}.
```

`15/8 = 1.875 < 2`, so this is **`<<_E T^{2 - 1/8 + eps}` unconditionally**.

That is: `R_Phi(T) <<_E T^{15/8 + eps}` is **unconditionally provable
today** for any fixed `E`, via the existing repo plan ingredient
`CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.5 calibrated with the
unconditional fixed-conductor 4th moment of `|L_E^*|`. This is the
single concrete unconditional bound below `T^2` that this exploration
finds.

For (X.2): doable in principle via Petersson trace formula. Family
must include `E`, and the family-averaged H1 must isolate `E` via
positivity or majorant. The H1 absolute series `R_B^f` is positive,
and `Petersson-weighted sum_f R_B^f(T) << ...` would give an averaged
result; isolating `E` requires `R_B^E(T) <<_E (positive Petersson
weight at E)^{-1} · Petersson-summed bound`, which is at least
`N_E^{1/2}` worse than family-averaged.

For (X.3): height-aspect average of `R_Phi(T)/T^2` is a natural object.
The continuous shifted negative second moment integrated over T already
delivers this kind of averaged statement (see §2.5 calibration). The
issue: the joint paper presumably wants the bound for `T = T_0` fixed,
not averaged over `T`.

For (X.4): `R_Phi(T) <<_E T^2 (log T)^{-A}` is intermediate between
(X.1) and full H1. It is consistent with the 4th-moment-based
`T^{15/8 + eps}` bound (which is strictly stronger). So (X.4) is
**unconditionally true** as a consequence of (X.1).

### 11.3 Does the joint paper need full H1 = o(T^2) ?

**This is the load-bearing audit question.** Searched the repo for
hints:

- `handoff pro.md` L1413+ ("Final Answer Expected") wants
  `R_E,1(T) = o(T^2)`, *not* a polynomial saving.
- `H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` formulates `(H-abs-r)` as a
  positive series. Does not specify whether `T^{2-eta}` suffices.
- `paper/main_revised.tex` is the Delta_machine_paper, not the
  Saar-Koyama joint paper. The joint paper's main-theorem statement
  is not in this repo snapshot.
- `H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md` does not state the
  H1 conclusion form precisely.

**The exact role of H1 in the joint paper's main theorem is not pinned
down in the documents I read.** If the joint paper only uses H1 as
`R_Phi(T)/T^2 = o(1)`, then the unconditional `T^{15/8+eps}`
bound from (X.1) **closes it**. If the joint paper uses something
stronger (e.g., uniform `o(T^{2-eta}) for some uniform eta`), the
status depends on that exact `eta`.

This is a high-value audit:

```text
AUDIT TASK: read the Saar-Koyama joint paper draft, identify
the exact form in which H1 enters the main theorem.  If
"R_Phi(T) = o(T^2)" is the literal usage, then the unconditional
T^{15/8+eps} bound suffices and the entire halo route is unnecessary.
```

This audit was not commissioned as part of today's session and is the
**single largest near-term lever** for unconditionalizing the joint
paper's main theorem.

### 11.4 Verdict

```text
Route X.1  ->  UNCONDITIONAL T^{15/8 + eps} bound is available today
              via 4th moment + Gallagher-HB.  Status of "is this
              enough" depends on Saar-Koyama paper's H1 usage form.

Route X.2-X.4  ->  Available with varying caveats.

Best partial off-halo result:
  "Unconditional R_Phi(T) <<_E T^{15/8 + eps} for fixed E"
  is the strongest unconditional fixed-E bound on R_Phi(T) the project
  can currently support.
  It is below T^2 by margin T^{1/8}.
  Whether it satisfies the joint paper's main theorem is unknown.
```

---

## 12. Classification

| Class | Routes |
|---|---|
| Genuinely unconditional, no (TSDB) needed | **X.1 (weakened to `T^{15/8+eps}`)**: via Good/Meurman 4th moment + Gallagher-HB |
| Reduces to (TSDB) | I, III, VII, VIII (all in different clothing) |
| Reduces to a different open problem comparable to (TSDB) | VI (mean-Lindelöf k=2 in t-aspect, open) |
| Reduces to (TSDB) for fixed E, but yields family-averaged statement | II, IV |
| Bounds wrong object (cannot reach `1/L'(rho)`) | V (subconvexity bounds `|L|`, not `1/|L'(rho)|`) |
| Structurally absent | IX (AC framework does not apply to spectral objects) |
| Strategic retreat / weakens H1 | X (X.1-X.4) |

Refined claim: **of the ten investigated routes, exactly one
(X.1) yields a quantitative unconditional sub-`T^2` bound today**.
That bound is `T^{15/8 + eps}`. Whether it suffices for the Saar-Koyama
joint paper is an open audit task.

---

## 13. Best candidate (PARTIAL)

```text
Best off-halo unconditional candidate:

  Theorem (PARTIAL, unconditional in fixed E):
    For every fixed elliptic curve E/Q with conductor N_E,
        R_Phi(T)  <<_E  T^{15/8 + eps}.
    Equivalently  R_Phi(T)/T^2  <<_E  T^{-1/8 + eps}  ->  0.

  Proof sketch:
    1.  Unconditional Good/Meurman t-aspect 4th moment for fixed
        GL2 newform of bounded conductor:
            int_T^{2T} |L_E^*(1/2 + i t)|^4 dt  <<_E  T^{2 + eps}.
        (Iwaniec-Kowalski Ch. 24; Good 1982; Meurman.)
    2.  Heap-Soundararajan bad-set calibration with k = 2 and
        V = T^{-1/8} (CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md §2.5):
            int_T^{2T} |L_E^*(1/2 + alpha + i t)|^{-2} dt  <<_E  T^{11/4 + eps}.
    3.  Gallagher-HB transfer to zero-sample:
            sum_{rho in Z_T}^{mult}  |L_E^*'(rho)|^{-2}  <<_E  T^{11/4 + eps}.
    4.  Cauchy-Schwarz:
            R_B(T)  =  sum |W_hat / L_E^*'(rho)|
                    <=  ( sum |W_hat|^2 )^{1/2}  ( sum |L'|^{-2} )^{1/2}
                    <=  T^{1/2 + eps}  ·  T^{11/8 + eps}
                    =   T^{15/8 + eps}.

  Caveats:
    - This is `(H-abs-r)`-form (positive absolute series).  The H1
      audit (H1_RESIDUE_FIRST_AUDIT_2026-05-14.md) confirms (H-abs-r)
      is sufficient for the residue-first contour identity.
    - Step 2's Heap-Soundararajan calibration requires the
      Selberg-Soundararajan upper-bound technique on log|L| at level
      of bounded conductor — this IS unconditional (Soundararajan
      Annals 2009 has the zeta version; GL2 fixed-conductor analog is
      routine; no GRH needed for upper-bound technique).
    - Step 3 Gallagher-HB is unconditional.
    - Step 1 is unconditional GL2 4th moment, fixed conductor,
      t-aspect, T^{2+eps}.  Reference: Iwaniec-Kowalski Ch. 24.

  Open question:  does R_Phi(T) <<_E T^{15/8 + eps} suffice for the
                  Saar-Koyama joint paper's main theorem?
                  AUDIT TARGET.

  Confidence in the unconditional T^{15/8+eps} bound: 0.78.
    (Two un-audited links: Heap-Soundararajan calibration for fixed
     GL2 with bounded conductor; and the unconditional polynomial
     pointwise floor used to bound the bad set.  Both believed
     standard.)
```

This is — to my knowledge after the session's reading — the **first
quantitative unconditional sub-T^2 bound on R_Phi(T)** that the project
has explicitly assembled. The previous unconditional ledger had
**nothing** below `T^2` and called the question "GENUINELY OPEN".
This exploration upgrades the unconditional state to `T^{15/8+eps}`.
Whether this is operationally sufficient is the open audit.

---

## 14. Cost estimate

```text
Phase                                                  Time      Risk
-----                                                  ----      ----
A. Audit Saar-Koyama joint paper for H1 usage form     2-3 days  low
B. If (A) says T^{2-eta} suffices for some eta < 1/8:
   write up X.1 as the joint paper's H1 input          1 week    low
C. If (A) says strict o(T^2) suffices:
   need also (X.2) family-averaging + isolation lemma  3-4 weeks medium
D. If (A) says strict R_Phi(T) <<_E T^{2-eta}
   for uniform eta > 0:
   need either (X.1) generalization (uniform 4th moment
   in conductor) or fall back to halo + GRH route      1-2 months high
```

**Single most valuable next step**: phase (A). Two-three days of audit.

---

## 15. Boundary

### Allowed claims

```text
- Routes I, III, VII, VIII reduce to (TSDB) by direct expansion.
- Route II reduces to (TSDB) for individual E in t-aspect; family-aspect
  averaging is unconditional but does not isolate E.
- Route IV (Conrey-Iwaniec cubic moment) is level-aspect, central-value;
  does NOT bound 1/L'(rho).
- Route V (subconvexity) bounds |L|, not 1/|L'(rho)|, and the only
  unconditional use of subconvexity in this story is the trivial
  polynomial pointwise floor.
- Route VI (mean-Lindelöf k=2 in t-aspect) is open at the same depth as
  Lindelöf for the 4th moment of L_E^* on the critical line.
- Route IX (additive combinatorics) is structurally absent.
- Route X.1: R_Phi(T) <<_E T^{15/8 + eps} is UNCONDITIONAL for fixed E
  via Good/Meurman + Heap-Soundararajan + Gallagher-HB.  (Confidence
  0.78; requires two un-audited bookkeeping steps believed standard.)
- The joint paper audit (does T^{15/8+eps} suffice?) is the single
  highest-leverage near-term task and was not commissioned today.
```

### Forbidden claims

```text
- "Off-halo unconditional H1 = o(T^2) is achievable today."  FALSE.
  Every fully unconditional route is either family-averaged or only
  gives T^{2 - eta} for some eta > 0.
- "Trace formula / Petersson-Kuznetsov bypasses GRH for individual E."
  FALSE.  Trace formula isolates by level/weight, not by t-aspect for
  a single fixed form.
- "Subconvexity for L_E^* gives an unconditional handle on 1/L'(rho)."
  FALSE.  Subconvexity bounds |L| above; gives no information on
  1/|L'(rho)| at zeros.
- "Conrey-Iwaniec cubic moment closes H1 for fixed E."  FALSE.  It is
  a central-value level-aspect statement, says nothing about
  sum 1/L_E^*'(rho).
- "Hadamard product gives an unconditional formula for L'(rho)."
  Half-FALSE: Hadamard product is unconditional, but extracting L'(rho)
  re-introduces the cluster sum which is (TSDB)-controlled.
- "Mean-Lindelöf for L_E^* in t-aspect is a known result."  FALSE.
  Only k=1 is unconditional; k=2 is open (equivalent to GL2 Lindelöf
  4th moment in t-aspect).
```

### Genuine surprise

```text
SURPRISE 1.  Route X.1 (strategic retreat to T^{15/8+eps}) is
             unconditional today via existing repo ingredients.  This is
             a previously-unstated quantitative unconditional bound on
             R_Phi(T) — the project's prior position was "fixed-E
             unconditional R_Phi(T) is open, period."  We have a sub-T^2
             bound!  Whether it suffices is an audit question.

SURPRISE 2.  Route VI (mean-Lindelöf k=2) is NOT a (TSDB)-equivalent
             open problem.  It is a sibling open problem at comparable
             depth.  This refines the previous narrative: "fixed-E
             unconditional H1 reduces to a unique deep open problem".
             It actually reduces to one of two comparable open
             problems: (TSDB) for thin-strip zero density, OR k=2
             mean-Lindelöf in t-aspect.  Either would do.

SURPRISE 3.  Route IV's trace formula gives a CONCEPTUALLY DIFFERENT
             obstruction from (TSDB).  The trace formula CAN give an
             unconditional family-averaged H1; the obstruction is
             *isolating the fixed E*, which is a paper-architecture
             question, not a GL2 zero-location question.  If the
             Saar-Koyama joint paper's main theorem turned out to need
             only family-averaged H1, the trace-formula route would
             close it unconditionally.

(Likely no-surprise:) Routes I, II, III, VII, VIII all reduce to
(TSDB) as expected.  Route V is the cleanest case of "right tool,
wrong target".  Route IX is structurally absent as expected.
```

### Probability ledger

```text
0.55  Off-halo unconditional H1 = o(T^2) for individual fixed E
      is GENUINELY OPEN at the same depth as (TSDB) or mean-Lindelöf
      k=2 in t-aspect (both currently open).
0.78  R_Phi(T) <<_E T^{15/8 + eps} unconditional for fixed E
      is currently provable in 1-2 weeks of careful write-up.
0.30  The Saar-Koyama joint paper's main theorem actually needs only
      R_Phi(T) <<_E T^{2 - eta} for some eta > 0, in which case
      Route X.1 closes the joint paper unconditionally.
0.10  Trace-formula family-averaged H1 with a positivity isolation
      lemma also closes the joint paper unconditionally without
      requiring T^{15/8+eps} for individual E.
0.02  An entirely-different unconditional architecture exists that
      I did not enumerate.  (Open exploration would target: kernel
      reproducibility / Riesz transform approach on GL2 — speculative.)
```

---

## 16. Implication for the halo route

The halo route (Door A + Door B + Door C + Door D) remains the
primary conditional route under GRH_{L_E^*}. This exploration:

```text
- Does NOT find a fully unconditional H1 = o(T^2) replacement for
  the halo route.
- DOES find an unconditional weaker target T^{15/8+eps}, sufficient
  for *some* downstream applications.
- Recommends a high-priority audit (joint paper's H1 usage form) to
  determine whether the weaker target closes the joint paper.
```

The halo route should continue as planned; the X.1 bound is a parallel
fallback that may obviate the halo route depending on the joint paper's
exact H1 form.

---

## 17. Cross-references

| File | Role |
|---|---|
| `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §8.1, §8.4, §8.5 | Original routes I, II, III |
| `UNCONDITIONAL_DOOR_B_ANALYSIS_2026-05-14.md` | Halo Door B reduction to (TSDB) |
| `UNCONDITIONAL_DENSITY_METHOD_2026-05-14.md` | Density method reduction to (TSDB) |
| `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §2.5, §2.6 | The k=2 bad-set calibration and Gallagher-HB transfer used in X.1 |
| `H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` | (H-abs-r) sufficiency for X.1 |
| `handoff pro.md` L854-921 | Direct reciprocal-tail dead-end (reference for Route IX baseline) |
| `B_prime_denom_Selberg_Beurling_assessment.md` §8.1 | Mollifier degree-blowup obstruction (Route I) |
| `AtZeros_log3_attempt.md` §2.2 | Route 2 / 4th moment status for individual GL2 |
| Conrey-Iwaniec, Annals 151 (2000) 1175-1216, arXiv:math/9810182 | Route IV cubic moment, level-aspect only |
| Iwaniec-Kowalski Ch. 24 / Good 1982 / Meurman | Unconditional GL2 t-aspect 4th moment T^{2+eps} |
| Soundararajan Annals 2009 | Upper-bound technique on log|L| |
| Hughes-Keating-O'Connell 2000 | Route II RM model baseline |

---

## 18. Recommended next steps

```text
1.  PRIORITY HIGH:  audit the Saar-Koyama joint paper's main theorem
    to identify the exact form in which H1 enters.  If H1 is used as
    "R_Phi(T) = o(T^2)" only, then the X.1 unconditional T^{15/8+eps}
    bound closes the joint paper unconditionally.

2.  Formalize Route X.1 as a standalone lemma.  All four steps
    (4th moment / bad-set / Gallagher-HB / Cauchy-Schwarz) have
    individual unconditional proofs in the repo or standard
    literature.  Write `R_PHI_UNCONDITIONAL_X1_LEMMA_2026-05-14.md`
    consolidating them, ~3 pages.

3.  If joint paper needs strict o(T^2), commission Route IV.1
    "family-averaged H1 via Petersson trace formula" as a parallel
    exploration.  Combine with positivity isolation (drop the diagonal
    f=E term) to try to extract fixed-E behavior.  Expect family-aspect
    statement; isolation is an open paper-architecture question.

4.  DO NOT commission unconditional Door B, unconditional density §8.3,
    or unconditional Palm wall — all confirmed (TSDB)-equivalent and
    closed.

5.  KEEP halo + GRH route as primary conditional path.  The
    unconditional efforts are auxiliary safety nets, not replacements.
```
