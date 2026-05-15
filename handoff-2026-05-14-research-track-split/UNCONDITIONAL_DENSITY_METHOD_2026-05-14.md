---
schema_version: 2
title: "Density-Method (Halo §8.3) Unconditional Promotion Analysis"
type: analysis
domain: project
tier: working
status: ANALYSIS
confidence: 0.72
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/UNCONDITIONAL_DOOR_B_ANALYSIS_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - Bui-Florea-Milinovich (BFMT), arXiv:2310.03949 (negative discrete moments of zeta')
  - Bui-Florea, arXiv:2302.07226 (negative moments of zeta)
  - Milinovich-Ng, arXiv:1306.0854 (simple zeros of modular L-functions; positive `sum |L'|^2` under GRH_f)
  - Carneiro-Chandee, arXiv:1008.4970 (zeta on the critical line)
  - Gonek, *On negative moments of the Riemann zeta-function*, Mathematika 36 (1989), 71-88
  - Hughes-Keating-O'Connell 2000 (random matrix model for J_{-k}(T))
  - Heap-Li-Zhao, Algebra & Number Theory (lower bounds for discrete negative moments)
  - Gao-Zhao 2023, Mathematika 69, 1081-1103 (lower bounds for negative L' moments, all k>0, under RH + simple zeros)
  - Iwaniec-Kowalski, *Analytic Number Theory*, Ch. 5, 11, 24
  - Booker 2014 (unconditional infinitely-many simple zeros for GL2 newforms)
  - Titchmarsh, Ch. 14 (WMC implies RH, simplicity, sum 1/|rho zeta'(rho)|^2 < infinity)
supersedes: []
superseded-by:
tags: [halo-route, density-method, unconditional, GRH-free, R_B, second-negative-moment, analysis, H1]
---

# Density-Method (Halo §8.3) — Unconditional Analysis

## 1. Headline verdict

```text
verdict:  NO.
```

The density method does **not** give an unconditional route to offcentral
H1 today. The required input — an upper bound

```text
sum_(rho in Z_T)^(mult) |L_E^*'(rho)|^(-2)  <<_E  T^c   with   c < 3
```

for fixed GL2/EC newform — is **strictly stronger than RH for `L_E^*`**.
No published unconditional upper bound on the negative second discrete
derivative moment exists for *any* automorphic L-function (zeta included)
without RH + simplicity. The single dedicated paper on this object
(Bui-Florea-Milinovich, arXiv:2310.03949, BFMT) is RH-conditional
throughout, and explicitly identifies WMC (still unproven, *strictly
stronger* than RH) as the weakest known hypothesis that yields any
upper bound on `J_{-1}(T)` over the full zero family.

The conditional RH-bound for `L_E^*` (i.e. GRH_{L_E^*}) IS within
adaptation reach of BFMT, giving `c = 2 + o(1)` unconditional-modulo-
GRH_{L_E^*}; this is the same regime in which the halo route's Door B
already closes. The density method therefore **does not bypass the
GRH_{L_E^*} blocker**; it relocates it from "Re rho_j = 1/2 for cluster
mates" to "Re rho = 1/2 to apply Selberg-Soundararajan upper-bound
machinery on `log |L|`".

## 2. Best known unconditional c

```text
best known unconditional c  =  + infinity   (no bound exists)
```

Stronger statement: it is currently **not known unconditionally** that
the sum `sum_(rho in Z_T) |L_E^*'(rho)|^(-2)` is even **finite term by
term** — this requires unconditional simplicity of the offcentral zeros
of `L_E^*`, which is open. (Booker 2014 gives infinitely many simple
zeros but not all.)

Even if one restricts to simple zeros (`sum^(simp)` rather than
`sum^(mult)`), no nontrivial unconditional upper bound on the negative
2nd derivative moment is in the literature for any GL_n L-function
including zeta. The closest unconditional facts:

```text
(a)  trivial:  sum_(rho simple, T<gamma<=2T) |L_E^*'(rho)|^(-2)
                  <= N(T)  ·  max_(rho simple) |L_E^*'(rho)|^(-2)
                  <=  T log T  ·  exp(2 max |S_f(t)|),
       which is super-polynomial-by-log; useless even on RH.

(b)  via WMC analog (still unproven, > RH):
       sum_(rho simple) 1 / (|rho| |L_E^*'(rho)|)^2  <  infinity
     would give a *normalized* convergent series but not a T^c bound.

(c)  unconditional positive 2nd derivative moment for GL2:
       sum_(0<gamma_f<=T) |L_E^*'(rho_f)|^2  is  NOT  known
       unconditionally even as an order-of-magnitude bound.
       Milinovich-Ng's Theorem 1.2 (the precise asymptotic
       `~ (cf/12pi)(17 +/- sqrt(145)) T log^4 T`) requires GRH_f.
```

Citations:

```text
- BFMT (arXiv:2310.03949), Theorem 1.1: under RH,
     sum_(gamma in F) |zeta'(rho)|^(-2k)
        <<  T^(1+delta)             if 2k(1+eps) <= 1,
        <<  T^(k+1/2+delta)         if 2k(1+eps) > 1.
  At k=1: T^(3/2+delta) for the subfamily F (RH-conditional).
  (F = zeros with gap >> 1/log T to nearest neighbour; conjectural
  full-density via Montgomery pair correlation.)

- BFMT §1.2 (WMC route): WMC ==>  J_{-1}(T) = o(T^2),
  i.e. c = 2 - eta is conditional on WMC, which is *stronger* than RH.

- Milinovich-Ng (arXiv:1306.0854) Theorem 1.2: under GRH_f,
     sum_(0<gamma_f<=T) |L'(rho_f, f)|^2  ~  C_f T log^4 T.

- Iwaniec-Kowalski Ch. 5 unconditional inputs: Brun-Titchmarsh,
  large-sieve zero-density, log-free zero-density for GL2 cusp forms,
  Kim-Sarnak zero-free region. None of these deliver any direct upper
  bound on |L'(rho)|^(-1) at offcentral rho.
```

Worst-case **lower** bound on `c` (information-theoretic obstruction):
the random-matrix model (Hughes-Keating-O'Connell, Conrey-Snaith)
predicts `J_{-1}(T) ~ C T`, i.e. `c = 1` is the *true* exponent. But
the same model predicts `Omega(T^(2/3-eps))` zeros with
`|zeta'(rho)|^(-1) >> |gamma|^(1/3-eps)` (BFMT pp.1-2, Hughes-Keating);
this `Omega` is barely consistent with `c < 3` and explains why pushing
past `k = 3/2` is the conjectural barrier for the conjectured asymptotic.
Conditionally `c = 2 + delta` is the right target; unconditionally we
have **nothing**.

## 3. Cost to push to c < 3

```text
cost  =  *at minimum* GRH_{L_E^*}  +  multi-month BFMT GL2 transcription.
```

This is the central finding. Let me unpack.

### 3.1 Direct route — adapt BFMT for GL2

BFMT's proof structure (RH-conditional):

```text
step 1.  Kirila's identity (RH):
            log |zeta'(rho)|  =  log |zeta(rho + alpha)| + O(error)
         for alpha = 1/log T and rho in F.
step 2.  reduce to negative continuous shifted moment of zeta on
         line Re s = 1/2 + alpha.
step 3.  apply Bui-Florea (arXiv:2302.07226) upper bound on
            int_T^(2T) |zeta(1/2 + alpha + it)|^(-2k) dt.
step 4.  discrete-to-continuous via Landau-Gonek explicit formula
         (RH-conditional) + a Montgomery-Vaughan-style mean-value.
```

GL2 transcription cost: each step depends on **RH/GRH at a
load-bearing point**:

| Step | RH usage | Unconditional substitute? |
|---|---|---|
| 1 (Kirila) | `1 - rho = bar rho` to invert `L/L'` near zero | NO substitute; zeros off critical line break the identity |
| 2 (reduce to shifted) | `rho + alpha` has `Re = 1/2 + alpha` | NO; shifted target moves into half-plane only on GRH |
| 3 (Bui-Florea continuous neg moment of GL2) | not yet written, but mirror BF: would need analogous Kirila-type identity off-line | NO direct substitute |
| 4 (Landau-Gonek for GL2) | uses RH for cleanest form; unconditional form is much weaker | only unconditional explicit formulae lose `(log T)^B` factors and break the `T^(1+delta)` shape |

**Verdict**: every step uses RH. The transcription gives
`c = 2 + delta` **on GRH_{L_E^*}**, not unconditionally.

### 3.2 Indirect route — Cauchy-Schwarz from positive moments

The task spec already worked through this and concluded "not directly
useful". Confirmed: `(sum 1)^2 <= N · sum |L'|^(-2) · sum |L'|^2`
gives a *lower* bound on the negative second moment, not an upper. No
unconditional Cauchy-Schwarz route exists.

### 3.3 Indirect route — fourth moment of `L` plus inversion

Selberg-Iwaniec-Kowalski Ch. 24 fourth moment

```text
int_T^(2T) |L_E^*(1/2 + it)|^4 dt  <<_E  T (log T)^A
```

is unconditional for fixed GL2 newform. **But** this controls
**positive** moments, not negative ones. Inverting `1/|L'|` against
`|L|` requires either (a) an AFE for `1/L'(rho)` that converges on
the critical line (none known unconditionally) or (b) a Jensen-type
mean-value identity which always needs upper bound on `L` and lower
bound on `L` near rho — i.e. an unconditional positive lower bound on
`|L_E^*(1/2 + it)|` for "most" `t`. Such a bound is essentially the
negative second moment we are trying to prove. Circular.

### 3.4 Indirect route — Heap-Li-Zhao adaptation

Heap-Li-Zhao arXiv:2107.06829 + Gao-Zhao Mathematika 69 (2023):
**lower** bounds for `J_{-k}(T)`, all `k > 0`, **under RH + simple
zeros**. No upper bounds. (And the conclusion is "lower bound", not
useful for our direction.)

### 3.5 Cost summary

```text
unconditional c < 3 for fixed GL2 newform
  via BFMT-style :   2-4 months full-time research, with high
                     probability of failure at step 1 (Kirila
                     identity off RH).
  via direct AFE :   genuine open problem; an unconditional AFE for
                     1/L'(rho) on a generic point of the critical
                     strip would itself imply a strong zero-density
                     improvement essentially equivalent to GRH near
                     the line.
  via WMC analog :   WMC for L_E^* (modular-form Mertens conjecture)
                     is open and is strictly stronger than GRH_{L_E^*}.
                     Not a real route.

  Realistic estimate: NO known route exists today.

unconditional c < 3 for fixed GL2 newform conditional on GRH_{L_E^*}
                  :  ~ 4-8 weeks BFMT transcription, comparable to
                     Stage 2 of halo plan.
```

## 4. Resulting unconditional offcentral H1 statement

```text
The density method does NOT yield unconditional offcentral H1 for
fixed E/Q today.

What it does yield (conditional on GRH_{L_E^*}):
  R_B(T)  =  sum_(rho in Z_T) |L_E^*'(rho)|^(-1)
          <<  sqrt(T log T · T^(2+delta))
          =   T^(3/2 + delta/2 + o(1))
  which beats T^2 with margin T^(1/2).

This is the SAME conditional regime in which the halo route's
Door A target (T^(5/2+eps) for the shifted negative 2nd moment of L)
is reachable. Both routes thus close conditionally on GRH_{L_E^*} and
both fail unconditionally.
```

The Stage 0 audit (`H1_RESIDUE_FIRST_AUDIT_2026-05-14.md`) verified
that the absolute series `R_B` is a *valid sufficient condition*
(H-abs-r) for the H1 conclusion. That part is intact: **if** an
unconditional `c < 3` were available, **then** unconditional H1 would
follow. But the conditional is contrafactual today.

## 5. Compared to halo + GRH: which is preferable?

Both routes:

```text
preconditions       halo+GRH                density+GRH
GRH needed?         yes (Door B structural) yes (Step 1 of BFMT, Kirila)
input target        sum |L(rho+alpha)|^(-2) sum |L'(rho)|^(-2)
                    <<  T^(5/2+eps)         <<  T^(c) with c<3
literature gap to   ~ 3/2 powers above      ~ 1 power above conjectural
  conjectural truth   conjectural truth     truth
direct GL2 source?  no (need BF GL2 transcr) no (need BFMT GL2 transcr)
                                            + Kirila GL2 identity
positivity?         signed contour          absolute series
                    (H-abs-r unneeded)      (H-abs-r used directly)
H1 path stage 0     GREEN (this session)    GREEN (this session)
H1 path stage 1     boundary-arc + numerator (none needed: bypasses
                    audits (in progress)    halo entirely)
H1 path stage 2     Door A target           density's c<3 target
estimated weeks     2-3 (Stage 2 BFMT GL2)  4-8 (full BFMT GL2 +
                                            Kirila GL2 identity)
risk profile        single dependency:      compound dependency:
                    AllZeroShiftedNeg_2     Kirila-GL2 + BF-GL2 + L-G-GL2
```

```text
preference:  halo + GRH  (cheaper, single dependency, in progress).
```

The density method is **strictly worse** as an "unconditional route"
because it needs the same GRH as halo plus more transcription overhead.
It would be a *useful safety net* only if Door B were structurally
broken in the halo route, but Door B is conditionally fine on GRH (the
structural NO is precisely against unconditional Door B). Side-by-side,
the density method has no advantage.

The original halo-plan §8.3 optimism — "unconditional c < 3 should be
very accessible — much cheaper than Stage 2-3" — was **mistaken**. It
silently assumed that small `c` would follow from a Selberg-fourth-moment
or a Heap-Li-Zhao-style absolute-value argument bypassing RH. Both
assumptions are wrong: every published upper bound on a negative
discrete moment of `L'` is RH-conditional, and the conjectural
`c = 1` is itself a Hughes-Keating-O'Connell random-matrix
prediction with no current unconditional shadow.

## 6. Boundary

Allowed to claim now:

```text
- The density method (halo §8.3) is GREEN as a conditional route under
  GRH_{L_E^*}, yielding R_B <<_E T^(3/2+delta+o(1)).
- The density method's H1-compatibility (positive R_B feeds (H-abs-r))
  is confirmed by Stage 0.
- The density method does NOT give an unconditional route to
  offcentral H1 today.
- No published unconditional upper bound on
    sum_(rho) |L_E^*'(rho)|^(-2)
  exists for ANY fixed GL_n L-function (zeta included).
- BFMT (arXiv:2310.03949) is the state of the art and is fully
  RH-conditional. WMC route still requires (a conjecture strictly
  stronger than) RH.
- Milinovich-Ng's positive 2nd moment lower bound is GRH_f-conditional
  for fixed GL2 newform. The unconditional positive 2nd moment for
  GL2 is itself open.
- Halo + GRH and density + GRH have comparable conditional reach.
  Halo is cheaper (single Door A dependency) than density (Kirila-GL2
  + BF-GL2 + L-G-GL2 transcriptions).
```

Not allowed to claim:

```text
- Unconditional c < 3 for sum |L_E^*'(rho)|^(-2) is achievable today.
- Unconditional offcentral H1 via density method.
- Unconditional R_B <<_E o(T^2).
- BFMT or its GL2 analog has an unconditional version.
- The halo-plan §8.3 optimism about "very accessible" unconditional
  c < 3 is correct.
- The density method bypasses the GRH blocker that halo+Door B faces.
```

## 7. Genuine surprise

There is a real surprise here, **but in the opposite direction from
the prompt's hopeful framing**.

```text
SURPRISE:  the density method's apparent "positivity advantage" over
           halo's Door B is illusory at the unconditional layer.

Both routes ultimately require GRH_{L_E^*} for their main analytic
input, and density's input (an upper bound on the negative 2nd
derivative moment) is arguably *harder* to obtain unconditionally than
halo's input (a shifted-line negative 2nd moment) because the negative
derivative-moment problem has been the subject of ten years of
RH-conditional work without escaping RH.
```

The H1 abstract proof-shape suggested that "positivity is cheap and
signed identities are expensive", which is true for **proof
architecture** (positivity = absolute series = no contour
manipulation). But the **analytic content** at the bottom of either
route is governed by the same RH / GRH zero-location facts, and
positivity does not reduce that content.

Stated bluntly:

```text
The density method does NOT make H1 unconditional today, and there
is no near-term route making it do so. The halo + GRH_{L_E^*} stack
remains the primary route. Unconditional offcentral H1 for fixed
E/Q remains GENUINELY open, with the bottleneck at the same point
as for the offcentral zero distribution of L_E^* itself.
```

Confidence breakdown:

```text
0.72  the density method gives no unconditional advantage over halo
0.20  some specialist unconditional bound on  sum_(rho) |L'(rho)|^(-2)
      exists in the literature that we missed (e.g., buried in
      Gonek's unpublished or in a recent preprint not in cache)
0.05  the WMC-for-GL2 (modular Mertens) is closer to proof than we
      think and would yield an unconditional `c = 2 + eta` route
0.03  an entirely different unconditional architecture (e.g., a
      Vinogradov-style large sieve for `1/L'(rho)`) gives c < 3
      directly without going through Kirila
```

The 0.20 residual is the main uncertainty. Retiring it would need
explicit search of: (a) Gonek's unpublished work cited in
Hughes-Keating-O'Connell, (b) Gao-Zhao 2023's complementary upper
bounds if any, (c) Milinovich's individual papers post-2015 on GL2
discrete moments. None are in `/tmp/farey-homogeneous-bfmt-20260511/`.

## 8. Implication for halo plan §8.3 and §10

```text
- Halo plan §8.3 "this may be the cheapest unconditional route" is
  retracted. It is not unconditional; it is comparably-conditional
  to halo+GRH and strictly more expensive.

- Halo plan §10 step 5 ("Density-method side-quest:
  DENSITY_METHOD_RB_LOOSE_2026-05-12.md") should be DOWNGRADED to a
  documentation task. The side-quest's value as a Risk R1 mitigation
  is preserved (it is still a parallel route if residue-first audit
  fails), but its value as an "unconditional safety net" is zero.

- Halo plan §11 claim ledger:
    "The density-method (8.3) provides an alternative unconditional
    route to R_B(T,c) = o(T^2) that does NOT require residue-first
    rewrite, given a loose negative second moment of L'(rho) ..."
  this claim is NOT supported. The "given" clause is not
  unconditionally achievable; making it conditional on GRH_{L_E^*}
  brings the density-method into the same conditional regime as halo.
```

## 9. What this means for the overall track

The session's structural NO at Door B (unconditional) plus this
analysis (unconditional density method) yields:

```text
Unconditional offcentral H1 for fixed E/Q is a GENUINE OPEN PROBLEM,
not closeable by either of the two named routes in the halo
unconditional plan. The bottleneck is identical to the bottleneck
for unconditional zero-density / zero-location near the critical
line for fixed-conductor GL2 L-functions.
```

Conditional offcentral H1 under GRH_{L_E^*} remains the realistic
near-term target, via the halo route's Door A. The density method is
preserved as a documentation-only side-quest, not a research priority.
