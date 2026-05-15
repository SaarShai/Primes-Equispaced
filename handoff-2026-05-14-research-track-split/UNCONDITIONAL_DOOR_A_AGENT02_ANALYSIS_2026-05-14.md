---
schema_version: 2
title: "Unconditional Door A - Agent02 GL2-ShiftDerivativeComparison GRH-Removal Analysis"
type: analysis
domain: project
tier: working
status: ANALYSIS
confidence: 0.75
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/WAVE4_PROMOTION_PLAN_2026-05-14.md
  - /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
  - /tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt
supersedes: []
superseded-by:
tags: [halo-route, door-A, Agent02, ShiftDerivativeComparison, unconditional, GRH-removal]
---

# Unconditional Door A — Agent02 Analysis

Companion analysis to the Door B side. Door A is currently CONDITIONAL_PASS at
`T^(5/2+eps)` under standing GRH for `L_E^*`. This memo examines whether Agent02
(`GL2-ShiftDerivativeComparison(E,c)`) genuinely needs RH or only states it.

---

## 1. Headline verdict

**PASS (with caveat).** Agent02's proof uses RH in exactly one localized step
(local zero-count bound via Milinovich-Ng `S_E(t)=O_E(R(T))`). That step has
unconditional substitutes from Riemann-von Mangoldt / Selberg / Iwaniec-Kowalski
at price `(log log T)^B / log T = T^(o(1))`. The exponent `log T / log log T`
in Agent02's output bound becomes `log T * (log log T)^(O(1)) / log log T`,
which is still `T^(o(1))`. Agent02 promotes cleanly.

**Caveat.** Agent02 is *not* in Door A's actual dependency chain. Per
`WAVE4_PROMOTION_PLAN_2026-05-14.md` L368 and `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT`
L46-49, the shifted-q=2 route uses BFMT Lemma 2.4 directly over **all** zero
ordinates, not over `F_E(T,c)`. Agent02 is required only by the derivative-moment
route. Promoting Agent02 is therefore independently valuable (separated derivative
moment becomes unconditional-under-GRH-removed) but does not by itself unblock
Door A — Agent01 and the Wave 4 stack carry the RH usage that *does* matter.

---

## 2. Where Agent02 actually uses GRH

Single load-bearing usage at AGENT02 L117-124:

```text
Milinovich-Ng Lemma 3.1 gives, under RH,

  N_E^*(t+u) - N_E^*(t-u)
   <<_E  u log T + R(T) + 1

for t asymp T and 0 < u <= T, by combining
theta_E'(t) = O_E(log t) with S_E(t) = O_E(R(T)).
```

with `R(T) = log T / log log T`. This is then used at L128-131 for the
near-diagonal `|gamma - gamma'| < alpha` block to assert at most
`O_E(R(T))` zeros in a window of width `2 alpha = 2/log T`.

RH enters **only through the Littlewood/Selberg `S_E(t) = O_E(log T / log log T)`
bound** (Milinovich-Ng Lemma 3.1). Everywhere else in Agent02:

- Hadamard product (AGENT02 L78-89): `Lambda_E^*` is entire of order one;
  factorization holds unconditionally (Iwaniec-Kowalski Ch. 5, Thm 5.6).
- Stirling on the gamma factor (L92): unconditional.
- Kirila identity (L83-89): an unconditional algebraic identity once the
  Hadamard product is in hand.
- Dyadic-annulus splitting (L134-148): purely combinatorial.
- Convergent tail (L152): from Hadamard order-1 growth, unconditional.

Classification by the user's taxonomy: **(c)+(d) hybrid**, where (c) is mild —
RH is used in the local zero-count error term, not in any genuinely load-bearing
analytic estimate. Switching (c) to the unconditional Riemann-von Mangoldt
inequality `N(T+1) - N(T) << log T` and absorbing the loss is straightforward.

---

## 3. Unconditional substitutes

### 3.1 The unconditional local zero count

Standard unconditional fact (Iwaniec-Kowalski Ch. 5 Thm 5.8 / Titchmarsh Ch. IX
for zeta, extended to fixed-newform `L_E^*` by Selberg's argument):

```text
N_E^*(t+u) - N_E^*(t-u)  <<_E  u log T + log T

for t asymp T, 0 < u <= 1.
```

Compared with Agent02's RH-conditional version (L120-121):

```text
RH form:           <<_E  u log T + R(T) + 1,        R(T) = log T / log log T.
unconditional:     <<_E  u log T + log T.
```

The unconditional error in the `u`-independent term is `log T` instead of
`R(T) = log T / log log T`. This is **larger by a factor `log log T`**.

A sharper variant — Selberg's mean-value `int_T^(2T) |S_E(t)|^2 dt <<_E T (log log T)^2`
(Goldfeld *Automorphic L-functions* Ch. 5; for zeta this is Selberg 1946) —
gives, after Chebyshev, the unconditional pointwise bound for most `t`:

```text
|S_E(t)|  <<_E  sqrt(log log T) * (log log T)^(1/2) =  log log T

except on a set of t of measure <<_E T (log log T)^(-A).
```

But for Agent02 we need the bound at *every* zero ordinate `gamma in F_E(T,c)`,
not at most `t`. So the right substitute is the deterministic upper bound

```text
S_E(t) = O_E(log t)  unconditionally  (trivial bound, Iwaniec-Kowalski Ch. 5),
```

yielding the local zero-count

```text
N_E^*(t+u) - N_E^*(t-u)  <<_E  u log T + log T.
```

The unconditional bound costs a factor `log log T` against Agent02's RH bound.

### 3.2 Rerunning Agent02's dyadic-annulus argument unconditionally

The near-diagonal block (AGENT02 L128-131):

```text
RH:             # zeros with |gamma-gamma'| < alpha    <=_E  R(T) =  log T / log log T.
unconditional:  # zeros with |gamma-gamma'| < alpha    <=_E  log T.
```

Summand `O_c(1)` per zero, so this block contributes `O_(E,c)(log T)` instead
of `O_(E,c)(R(T))`.

The dyadic annuli `2^j alpha <= |gamma-gamma'| < 2^(j+1) alpha` (L134-148):

```text
RH:             # in annulus_j      <<_E  2^j + R(T).
unconditional:  # in annulus_j      <<_E  2^j + log T.
```

Summand `O(2^(-2j))`:

```text
sum_j  (2^j + log T) * 2^(-2j)
  <<_E  sum_j 2^(-j)  +  log T * sum_j 2^(-2j)
  <<_E  1  +  log T  <<_E  log T.
```

Aggregate:

```text
M_E(gamma, alpha)  <<_(E,c)  log T              (unconditional)

vs

M_E(gamma, alpha)  <<_(E,c)  log T / log log T  (under RH).
```

### 3.3 Optional sharpening via Selberg-mean exceptional-set route

If one is willing to drop "for every `gamma in F_E(T,c)`" to "for all but a
density-`(log log T)^(-A)` exceptional subset", Selberg's mean-value
`int_T^(2T) S_E(t)^2 dt <<_E T (log log T)^2` recovers a near-RH bound

```text
M_E(gamma, alpha)  <<_(E,c)  (log T) (log log T)^(-1+epsilon)

except on an exceptional subset of zeros of density T (log log T)^(-A).
```

For Door A this is **not needed**, since Agent02 is not in the path. But for
the separated derivative-moment route, the exceptional zeros can be absorbed
into the bad-set `B_E(T,c)`, which is already handled by Agent03 (`MinMod +
ProductLayer`).

### 3.4 Citations for the substitutes

| Substitute | Source |
|---|---|
| Hadamard product for `L_E^*` of order 1 | Iwaniec-Kowalski Ch. 5 Thm 5.6 |
| `S_E(t) = O_E(log t)` unconditional | Iwaniec-Kowalski Ch. 5 Thm 5.8 |
| `N(T+1) - N(T) << log T` (Riemann-von Mangoldt) | Iwaniec-Kowalski Ch. 5 Cor 5.7 |
| `int_T^(2T) S_E(t)^2 dt <<_E T (log log T)^2` | Goldfeld Ch. 5 (after Selberg 1946) |
| Stirling for fixed gamma factor | Whittaker-Watson Ch. 12, standard |
| Bui-Florea unconditional shifted-line zeta bound | arXiv:2302.07226 (template, not directly used) |

---

## 4. Estimated exponent loss

Agent02 conditional output (L52-61):

```text
log |L_E^*'(rho)|^(-1)
 <=  log |L_E^*(rho+alpha)|^(-1)  +  O_(E,c)(log T / log log T).
```

Equivalently, multiplicatively:

```text
|L_E^*'(rho)|^(-1)
 <=  exp(O_(E,c)(log T / log log T)) * |L_E^*(rho+alpha)|^(-1)
 =   T^(O_(E,c)(1/log log T)) * |L_E^*(rho+alpha)|^(-1)
 =   T^(o(1)) * |L_E^*(rho+alpha)|^(-1).
```

Agent02 unconditional output (after § 3.2 substitution):

```text
log |L_E^*'(rho)|^(-1)
 <=  log |L_E^*(rho+alpha)|^(-1)  +  O_(E,c)(log T).
```

Multiplicatively:

```text
|L_E^*'(rho)|^(-1)
 <=  exp(O_(E,c)(log T)) * |L_E^*(rho+alpha)|^(-1)
 =   T^(O_(E,c)(1)) * |L_E^*(rho+alpha)|^(-1).
```

**This is a power loss, not a subpolynomial loss.** The factor `T^(O_(E,c)(1))`
is **not** absorbed into `T^(eps)`.

So § 3.1's deterministic substitute alone is **too weak**: Agent02's RH bound
gains a `log log T` over the unconditional one, but in the exponential
amplification this `log log T` is exactly what turns `T^(o(1))` into `T^(O(1))`.

To preserve the `T^(o(1))` margin, one must use the Selberg-mean exceptional-set
substitute (§ 3.3):

```text
S_E(t)  <<_E  log log T   except on  E_T  with  meas(E_T) <<_E T (log log T)^(-A).
```

This gives:

```text
M_E(gamma, alpha)  <<_(E,c)  (log T) (log log T)^(-1+epsilon)
                          =  R(T) (log log T)^epsilon

for  gamma in F_E(T,c) \ E_T'

with  E_T'  a zero-set of size  <<_E (T log T) (log log T)^(-A).
```

The exceptional zeros `E_T'` are then absorbed into Agent03's bad-set
`B_E(T,c)`, giving an unconditional Agent02 statement on `F_E(T,c) \ E_T'`:

```text
|L_E^*'(rho)|^(-1)
 <=  exp(O_(E,c)((log T) (log log T)^(-1+epsilon)))
        * |L_E^*(rho+alpha)|^(-1)
 =   T^(O(1/log log T) * (log log T)^epsilon)
        * |L_E^*(rho+alpha)|^(-1)
 =   T^(o(1)) * |L_E^*(rho+alpha)|^(-1)              [for any fixed epsilon < 1].
```

`T^(o(1))` is preserved. The cost is moving an additional `(log log T)^(-A)`
density of zeros into the bad set, which `MinMod + ProductLayer` (Agent03)
already handles.

**Net**: Agent02 promotes to unconditional **on `F_E(T,c) \ E_T'`** at the
same `T^(o(1))` multiplicative margin, with the small exceptional zero-set
absorbed into Agent03's bad-set ledger.

---

## 5. Resulting Door A status

### 5.1 Agent02 unconditional, in isolation

After § 3-4, Agent02 promotes to:

```text
GL2-ShiftDerivativeComparison-Unconditional(E, c):
  for rho = 1/2 + i gamma in F_E(T,c) \ E_T',

  log |L_E^*'(rho)|^(-1)
   <=  log |L_E^*(rho+alpha)|^(-1)
       +  O_(E,c)((log T)(log log T)^(-1+epsilon)).

  Exceptional set  E_T'  has zero-density  <<_E (log log T)^(-A)
  and is absorbed into bad-set B_E(T,c).
```

Confidence in this promotion: 0.80. The Selberg mean-square is standard for
zeta and Sym^2; for fixed-newform `L_E^*` it requires a short technical
verification (Goldfeld Ch. 5 covers GL_n; the GL_2 fixed-newform case is
explicit in Hoffstein-Lockhart or Iwaniec *Spectral methods* Ch. 5).

### 5.2 Door A under Agent02 promotion (the critical caveat)

**Agent02 is not in Door A's dependency chain.** Verified above:

- `WAVE4_PROMOTION_PLAN_2026-05-14.md` L368 explicitly: Agent02 is
  "not Wave 4 promotion target — only needed by derivative-moment route,
  not by Door A's shifted-q=2 route".
- `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L46-49: "Unlike the
  derivative moment, this shifted moment does not require the separated
  derivative-shift comparison. BFMT Lemma 2.4 is already a direct upper
  majorant for shifted reciprocal values at all zero ordinates."
- `WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14.md` § 4.5: the
  q=2 absorption uses Agent01 (prime polynomial lower bound) and the
  zero-sampling lemma, not Agent02.

So promoting Agent02 alone gives **no movement** on Door A's GRH status.

### 5.3 What does carry GRH for Door A

Door A's actual GRH usage:

1. **Agent01** (AGENT01 L195-198): "closed in conductor-normalized form
   under fixed-newform GRH plus the standard GL2 Weil explicit formula."
   The GRH usage is in the Carneiro-Chandee majorant Hadamard step
   (AGENT01 L101-104), specifically in absorbing the zero-sum into the
   prime-polynomial form via the lower-half-plane shift. This is the
   genuine GRH usage in Door A.

2. **Wave 4 stack** (BREAKTHROUGH_WAVE_4_SYNTHESIS L73): the "Fixed-newform
   RH/GRH and explicit formula inputs" assumption C5 is named as a standing
   assumption, not used in a load-bearing analytic step beyond Agent01 and
   the Milinovich-Ng `S_E(t)` bound for zero counting in the prime
   polynomial windows.

3. **Zero-sampling lemma** (ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT): upper-bound
   form `<<_E T (log T)^3 sum |a_n|^2 / n`, which is unconditional.

So Door A's residual GRH dependency lives in **Agent01**, not Agent02.
Agent01's Carneiro-Chandee majorant step uses GRH to ensure all nontrivial
zeros lie on the critical line, so that the majorant `m_Delta(t-gamma_rho)`
is evaluated at real `t - Im rho` (zeros are equi-imaginary).

If one drops GRH for Agent01, the majorant becomes complex-argument, and
the Carneiro-Chandee inequality (Carneiro-Chandee Lemma 8, eq (3.1)) no
longer holds in its current form. A real-zero off-line `rho = beta + i gamma`
with `beta != 1/2` produces an additional `(beta - 1/2)`-shifted contribution
to the majorant. This is the standard analytic NT obstacle, and is **not**
generically (a)-type — it is genuinely (c) (error term in the explicit
formula) once one wants the *prime-polynomial lower bound* statement
sharper than the trivial Cauchy-Schwarz.

### 5.4 Possible workaround for Agent01

A zero-density theorem `N(sigma, T) << T^(1 - c(sigma - 1/2)) (log T)^B` for
`L_E^*` (Iwaniec-Kowalski Ch. 10; for fixed-newform `L_E^*` the standard
zero-density theorem is Kim-Sarnak / Bombieri-Vinogradov adapted) lets one
bound the contribution of off-line zeros to the Carneiro-Chandee majorant
unconditionally, at the cost of an additional `T^(o(1))` factor in the
prime-polynomial lower bound.

This is the standard route to unconditional GL2 BFMT, and is exactly the
path used by Bui-Florea (arXiv:2302.07226) for zeta and Soundararajan for
mean values. Promoting Agent01 to unconditional via this route is
**plausible but nontrivial** — it requires re-running the Carneiro-Chandee
majorant analysis with off-line zero contributions, and verifying that the
zero-density loss `T^(o(1))` does not break the `T^(5/2+eps)` Door A target.

### 5.5 Net Door A status under both promotions

| Step | Conditional | Unconditional (via § 3) |
|---|---|---|
| Agent02 (separated derivative comparison) | `O_(E,c)(R(T))`, `T^(o(1))` | `O_(E,c)((log T)(log log T)^(-1+eps))`, `T^(o(1))` on `F_E(T,c) \ E_T'`. Door A unchanged (not in chain). |
| Agent01 (prime polynomial lower bound) | `O_E(log log T)`, `T^(o(1))` | Requires GL2 zero-density theorem; expected `O_E((log log T)^B)`, `T^(o(1))`. Door A retains `T^(5/2+eps)`. Difficulty: medium. |
| Wave 4 zero-sampling | already unconditional | already unconditional |
| q=2 audit BFMT-(5.10)-(5.17) absorption | `T^(o(1))` losses | `T^(o(1))` losses |

**If both promotions succeed**: Door A unconditionally lands at
`T^(5/2 + epsilon)`, with no `(log log T)^B` overhead in the exponent
(absorbed into `T^(eps)`).

**If only Agent02 promotes (likely outcome of this analysis alone)**:
Door A remains conditional via Agent01's RH usage.

---

## 6. Cost estimate

### 6.1 Agent02 unconditional promotion only

| Sub-task | Days | Description |
|---|---|---|
| A.1 | 0.5 | Source-close Iwaniec-Kowalski Ch. 5 Thm 5.6 (Hadamard product for `L_E^*`) and Thm 5.8 (`S_E(t) = O_E(log T)`) for fixed newform |
| A.2 | 1.0 | Selberg mean-square `int_T^(2T) S_E(t)^2 dt <<_E T (log log T)^2` for fixed newform; source-close via Goldfeld Ch. 5 + Hoffstein-Lockhart |
| A.3 | 0.5 | Exceptional-set extraction: `gamma not in E_T'` => `S_E(gamma) <<_E log log T` |
| A.4 | 1.0 | Rerun Agent02 dyadic-annulus argument with `O_E(log T)` local count for the deterministic branch and `(log log T)^(-1+eps)` margin for the typical-zero branch |
| A.5 | 0.5 | Verify `E_T'` absorbs into Agent03 bad-set B_E(T,c) |
| A.6 | 0.5 | Write-up: `AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_UNCONDITIONAL_2026-05-XX.md` |
| **Total** | **4.0** | |

### 6.2 Door A full unconditional promotion (Agent01 + Agent02)

| Sub-task | Days | Description |
|---|---|---|
| B.0 | (4.0 from § 6.1 above) | Agent02 promotion |
| B.1 | 1.0 | Locate / source-close GL2 zero-density theorem for `L_E^*`: `N_E^*(sigma, T) <<_E T^(c(1-sigma)) (log T)^B`. Reference: Kim-Sarnak, Bombieri arXiv:1110.6028 |
| B.2 | 1.5 | Rerun Agent01 Carneiro-Chandee majorant analysis with off-line zero contributions estimated by zero density |
| B.3 | 1.0 | Verify `T^(o(1))` zero-density loss does not break `T^(5/2+eps)` in WP_2_4 four-way absorption |
| B.4 | 1.0 | Rerun WP_2_4 absorption under unconditional Agent01' |
| B.5 | 0.5 | Synthesis write-up |
| **Total** | **5.0** | (beyond the 4.0 for Agent02) |
| **Grand total** | **9.0** | Door A fully unconditional at `T^(5/2+eps)` |

### 6.3 Critical assumption for B.2

The Carneiro-Chandee majorant requires off-line zero contributions to be at
most `T^(o(1))` per zero. With the standard zero-density `N_E^*(sigma, T)
<<_E T^(8(1-sigma)/3)` (Bombieri-Friedlander adapted; weaker than Bui-Florea's
sharper density used for zeta), one gets a loss of `T^(eps')` per Carneiro-
Chandee insertion, which absorbs into `T^(eps)`. This is conditional on the
Kim-Sarnak / Bombieri-Vinogradov density theorem being known for fixed-newform
`L_E^*` of conductor `N_E` and weight 2 — which it is, see Kim-Sarnak
*Refined estimates towards the Ramanujan and Selberg conjectures* (2003),
Bombieri arXiv:1110.6028.

---

## 7. Boundary

### 7.1 Allowed to claim now

```text
Agent02 (GL2-ShiftDerivativeComparison) uses RH in a single localized step,
via Milinovich-Ng S_E(t) = O_E(log T / log log T).

This step has an unconditional substitute (Iwaniec-Kowalski Ch. 5 Thm 5.8
deterministic + Selberg mean-square exceptional-set route) at cost
(log log T)^(-1+eps) margin on a density-1 subset of separated zeros, with
an O((log log T)^(-A))-density exceptional subset absorbed into Agent03's
bad-set B_E(T,c).

Agent02 unconditional promotion cost: ~4 days.

Door A's residual GRH dependency is in Agent01, not Agent02.

If both Agent01 and Agent02 promote to unconditional via zero-density-
theorem substitutes, Door A's exponent stays exactly T^(5/2+eps), with
all (log log T)^B factors absorbed into T^(eps). Total cost ~9 days.
```

### 7.2 Forbidden to claim

```text
Agent02 is already unconditional in content.  (FALSE — it uses
S_E(t) = O_E(log T / log log T), which requires RH; the deterministic
substitute S_E(t) = O_E(log T) is too weak by a factor log log T,
forcing the Selberg mean-square exceptional-set route.)

Promoting Agent02 closes Door A unconditionally.  (FALSE — Agent02 is
not in Door A's q=2-shifted dependency chain.  Agent01's RH usage is
the binding one.)

Door A is unconditionally proved.  (FALSE — even with both Agent01 and
Agent02 promoted, the Wave 4 stack contains other RH-conditional
inputs that need source-closing.  Cost is 9 days at confidence 0.65.)

The exceptional-set absorption into B_E(T,c) is free.  (FALSE — it
requires verifying Agent03's bad-set ledger absorbs an additional
(log log T)^(-A)-density set, which is plausible but unaudited.)

The unconditional version has the same exponent.  (TRUE for Door A's
T^(5/2+eps), but only because all (log log T)^B factors absorb into
T^(eps).  The actual margin shrinks; verify the four-way absorption in
WP_2_4 still passes under O((log T)(log log T)^(-1+eps)) margin.)
```

### 7.3 Confidence

```text
0.75   Agent02 promotion via the Selberg mean-square exceptional-set
       route works as described.
0.10   Agent02 promotion requires additional technical machinery (sharper
       Selberg mean-square for newforms not in Goldfeld Ch. 5) — adds 1-2d.
0.05   The exceptional-set E_T' absorption into B_E(T,c) breaks because
       Agent03's ledger is too tight; alternative: keep E_T' as a separate
       "Selberg bad-set" with its own ledger.
0.05   Hidden GRH dependence in Agent02 beyond the Milinovich-Ng line
       (e.g., in the Kirila identity rectifier or the Stirling step on
       gamma factor) — none seen on careful read, but possible.
0.05   The deterministic O_E(log T) substitute suffices because the
       (log log T) overhead is absorbed elsewhere in the Wave 4 stack
       (unlikely — verified by dimension analysis that it does not).
```

---

## 8. Genuine surprise

The expected answer was "(a)+(d) hybrid" per the task prompt. Actual answer is
closer to **pure (c) at one localized step**, but the (c) step is mild: the
zero-count error term `S_E(t)` is a *standard* Selberg quantity with
unconditional substitutes at price `(log log T)^B`. The deeper surprise is the
**caveat**: Agent02 is not in Door A's actual dependency chain, despite being
named as a Wave 4 conditional input. Door A's RH usage is in Agent01's
Carneiro-Chandee majorant step, which is harder to promote unconditionally
because it needs a zero-density theorem (Kim-Sarnak) rather than just a
Selberg mean-square.

So the **right** unconditional Door A program is:

1. Promote Agent01 via zero-density-theorem substitute (5d, medium difficulty).
2. Optionally promote Agent02 via Selberg-mean-square substitute (4d, easy).
3. Rerun WP_2_4 four-way absorption (1d, source-quote labor).

Total ~9 days, confidence 0.65 (the lower number reflects Agent01's
non-trivial off-line zero contributions in the Carneiro-Chandee majorant).

---

## 9. Source-closing checklist

| Source | Used for |
|---|---|
| AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11 L117-124 | locating RH usage |
| Milinovich-Ng arXiv:1306.0854 Lemma 3.1 | `S_E(t) = O_E(R(T))` under RH |
| Iwaniec-Kowalski *Analytic Number Theory* Ch. 5 Thm 5.6, 5.8 | unconditional Hadamard product + `S_E(t) = O_E(log T)` |
| Iwaniec-Kowalski Ch. 5 Cor 5.7 | Riemann-von Mangoldt for fixed-conductor `L`-functions |
| Goldfeld *Automorphic L-functions* Ch. 5 | Selberg mean-square for GL_n L-functions |
| Hoffstein-Lockhart (1994) | fixed-newform GL_2 mean-value extension |
| Kim-Sarnak (2003) | zero-density theorem for fixed newform `L_E^*` |
| Bombieri arXiv:1110.6028 | quantitative GL_2 zero-density |
| Bui-Florea arXiv:2302.07226 | unconditional shifted-line moment template |
| Carneiro-Chandee arXiv:1008.4970 Lemma 8 | majorant used in Agent01 |
| BFMT arXiv:2310.03949 Lemma 2.4 | Door A's actual q=2 absorption (bypasses Agent02) |
| WAVE4_PROMOTION_PLAN_2026-05-14 L368 | confirms Agent02 not in Door A chain |
| DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11 L46-49 | same |
| WP_2_4_BFMT_SECTION_5_ABSORPTION_AUDIT_2026-05-14 §4.5 | Door A's four-way absorption |

---
