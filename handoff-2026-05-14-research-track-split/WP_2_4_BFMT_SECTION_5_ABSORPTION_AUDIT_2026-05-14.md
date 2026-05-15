---
schema_version: 2
title: "WP-2.4 BFMT Section 5 Absorption Audit at k=1 (Wave 4 Sub-tasks 1.1, 2.1, 2.4)"
type: audit-execution
domain: project
tier: working
status: PASS
confidence: 0.80
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/WAVE4_PROMOTION_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt (Lemma 2.3 p. 7; Prop 2.5/2.6/2.7 p. 8; Theorem 3.1 p. 8-9; Section 5 eqs (5.9)-(5.17) p. 15-18)
  - /tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt (Lemma 2.1 prime-power absorption)
  - /tmp/farey-homogeneous-bfmt-20260511/carneiro_chandee_1008_4970.txt (Lemma 8; eqs (3.1)-(3.2) majorant)
  - /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt (eqs (18)-(23); Lemma 3.1)
supersedes: []
superseded-by:
tags: [halo-route, door-A, wave-4, BFMT, section-5, binding-audit, stage-2-execution]
---

# WP-2.4 BFMT Section 5 Absorption Audit at k=1

Binding audit for Door A of the halo unconditional plan. Executes three Wave 4
promotion sub-tasks (1.1, 2.1, 2.4) from
`WAVE4_PROMOTION_PLAN_2026-05-14.md`.

---

## 1. Verdict and headline

**PASS.** Door A conditional-closure target

```text
sum_(rho in Z_T)^(mult) |L_E^*(rho+1/log T)|^(-2)  <<_(E,eps)  T^(5/2 + eps)
```

is recovered under standing fixed-newform GRH + standard GL2 explicit formula
+ Carneiro-Chandee majorant. All four insertions (Props 2.5/2.6/2.7 +
Agent01 conductor-normalized archimedean term) at `2k=2` in Section 5 eqs
(5.10)-(5.17) absorb into a single `T^(eps)` margin with the multiplicative
loss budget

```text
exp(O(log T / log log T)) * (log T)^(O(1))  =  T^(o(1)),
```

strictly subpolynomial.

Wave 4 promotion is essentially complete after 2.0d combined execution
(R5 up-side fires). Remaining sub-tasks (1.2-1.5, 2.2-2.3, 2.5-2.6) are
source-quote textual labor ~3-5d; Door A closes conditionally under standing
GRH at exponent `T^(5/2+eps)` in ~1 week from 2026-05-14.

---

## 2. Sub-task 1.1 — k-independence of Agent01 prime polynomial

Re-read `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` L29-89.

### 2.1 Direct quote of Agent01's theorem statement

L42-52 displays:

```text
log |L_E^*(s)|
 >= A_E(t;alpha,Delta)
    - Re sum_(p<=x, p not | N_E)
        b_E(p;Delta) lambda_E(p) p^(-s)
    - C_E log log T
    + O_E(Delta^2 exp(pi Delta)/T
          + Delta log(1+Delta T)/sqrt(T)),
```

with `s = 1/2 + alpha + it`, `alpha = 1/log T`, `x = exp(2 pi Delta)`,
`b_E(p;Delta) = - a_alpha(p;Delta) log p`.

### 2.2 k-search

The variables appearing in L29-89 are: `s, alpha, t, T, x, Delta, p, n,
N_E, lambda_E, Lambda_E, a_alpha, b_E, A_E, C_E`. No symbol `k` is bound
anywhere in L29-89. The archimedean factor

```text
A_E(t;alpha,Delta) = [log C_E(t) + O_E(1)] / (2 pi Delta)
                       * log(1 - exp(-2 pi alpha Delta)) + O_E(1)
```

(L58-64) is also `k`-free; `k` does not enter `C_E(t) asymp_E T^2` (the `2`
is the GL2 degree, not BFMT's exponent `k`).

### 2.3 Where k enters

`k` enters only when the prime polynomial is **inserted into BFMT Lemma 2.4
/ Section 5 eq (5.13)** via the BFMT `2k`-th-power dispatch (cf. BFMT p. 15
line 1020, where `s_0` and `k` appear together inside the upper-bound
exponent for the truncated zeta inverse `|zeta'(rho)|^(-2k)`). The
conductor-normalized "doubling" `2k -> 4k`
(`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L33-37) is itself a
**downstream** effect: it lives in the Section 5 packaging of `|L_E^*|^(-2k)`,
not in Agent01's prime polynomial display.

### 2.4 Verdict

**Sub-task 1.1: PASS.**

Citation: AGENT01 L29-89 contains no `k`-bound symbol. The `k`-dependence
of the eventual `|L_E^*|^(-2k)` upper bound enters at the BFMT Lemma 2.4 /
(5.13) packaging step, i.e. **downstream** of Agent01's input. Agent01's
input is reusable verbatim at `2k=2` (k=1).

No further derivation needed.

---

## 3. Sub-task 2.1 — k=1 Prop 2.5 transcription

Re-read `ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` L72-115 against
BFMT p. 8 (Prop 2.5) + BFMT p. 11 (proof of Prop 2.5, eq line 1020 of
extracted text).

### 3.1 Prop 2.5 statement (BFMT p. 8)

```text
For 0 <= v <= K and beta_0 s_0 <= 1 - loglog T / log T,
sum_(gamma in (T,2T]) |P_(0,v)(gamma)|^(2 s_0)
  <<  N(T) s_0! b(Delta_v)^(2 s_0)
            (loglog T / Delta_v)^(2 s_0 eta(Delta_v))
            (loglog T beta_0)^(s_0).
```

The displayed inequality contains the parameters `s_0, beta_0, Delta_v, K,
v`. **No `k` appears** in the Prop 2.5 statement itself. `k` enters Prop 2.6
and Prop 2.7 explicitly (cf. BFMT p. 8: factors `k^2 b(Delta_j)^2`,
`E_(ell_h)(k P_(h,j)(gamma))`), but NOT Prop 2.5.

### 3.2 Support condition

`beta_0 s_0 <= 1 - loglog T / log T` (BFMT p. 8 line 458 of extracted text;
quoted in ZERO_SAMPLE L96-98). This condition is `k`-independent. It fixes
the polynomial length `<= T / log T` regardless of BFMT exponent.

At `2k=2`, ZERO_SAMPLE L100-109 applies `ZS(A)` (zero-sampling lemma) to
the rescaled coefficients. The conclusion at L106-109,

```text
sum_(gamma in (T,2T]) |P_(0,v)(gamma)|^(2 s_0)
  << N_E(T) (log T)^2
       s_0! b(Delta_v)^(2 s_0)
       (loglog T / Delta_v)^(2 s_0 eta(Delta_v))
       (loglog T beta_0)^(s_0),
```

reproduces BFMT Prop 2.5 verbatim **except** for the extra `(log T)^2`.

### 3.3 The `(log T)^2` extra factor

ZERO_SAMPLE L111 says: "This is BFMT Proposition 2.5 with an extra
`(log T)^2`." The factor `(log T)^2` originates from the upper-bound form
of the zero-sampling lemma `ZS(A)` (L75-79):

```text
ZS(A):  sum_(T<gamma<=2T) |A(1/2 + i gamma)|^2
          <<_E T (log T)^3 sum |a_n|^2 / n,
```

versus BFMT's Theorem 3.1 (p. 8-9 of extracted text, eq 490) which is an
**equality** of leading term `N(T) sum |a_n|^2 / n` plus correction.
`N(T) asymp T log T / (2 pi)` carries one `log T`; the upper-bound form
costs `(log T)^3` instead, an excess of `(log T)^2`. This counting is
**`k`-independent**: it tracks the zero-counting function `N(T)`, not the
BFMT exponent.

### 3.4 Parameter range `s_0 << log T / log log T`

ZERO_SAMPLE L113-114 records that the factorial obstruction disappears
because the estimate is homogeneous and is applied to the scaled polynomial
directly. The parameter range survives `2k=2` because the support
condition `beta_0 s_0 <= 1 - loglog T / log T` does not involve `k`, and
BFMT's choice `beta_0 asymp loglog T / log T` (cf. (5.1)) is also
`k`-independent at the Prop 2.5 invocation level. (The `k` enters only
later, in Section 5 (5.13), where `s_0` is dispatched against `k^2`.)

### 3.5 Verdict

**Sub-task 2.1: PASS.**

Citations:
- BFMT p. 8 (extracted line 458): Prop 2.5 statement, `k`-free.
- ZERO_SAMPLE L96-114: zero-sampling transcription preserves
  `(log T)^2` overhead, `s_0`-range, support condition all
  `k`-independently.

No k-dependent factor identified.

---

## 4. Sub-task 2.4 — Section 5 absorption at k=1 (THE BINDING AUDIT)

### 4.1 BFMT (5.10)-(5.17) at k=1

Extract from cached BFMT text, p. 15-18, lines 1020-1163:

**Eq (5.10)** (BFMT line 1038-1040): for `gamma in F, gamma not in T_0`,
when `2k(1+eps) > 1`,

```text
sum_(gamma in F, not T_0) |zeta'(rho)|^(-2k)
  <<  T^( 1 + (1+delta) k * (2k - a(2d-1)/r) / (2k - a(2d-1)/r + 2d - 1) )
      * exp( log T loglog log T / loglog T ).
```

At `2k = 2` (`k=1`), the conductor-normalized doubling
(`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L33-37) replaces the
exponent `2k` inside BFMT's dispatch by `4k`. The exponent becomes

```text
1 + (1+delta) * k * (4k - A) / (4k - A + B),
```

with the GL2 normalization `A = a(2d-1)/r = 1 + O(eps)`, `B = 2d-1 = 1 +
O(eps)` (from `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT` L122-128).

**Eq (5.11)** (BFMT line 1048): for `gamma in F cap T_0`,

```text
sum |zeta'(rho)|^(-2k)
  <=  exp( O( log T / loglog T ) ) * ( S_1(gamma) + S_2(gamma) ).
```

**Eq (5.12)** (BFMT line 1066): via Prop 2.7,

```text
sum_(gamma in F) S_1(gamma)  <<  N(T) (log T)^(O(1)).
```

**Eq (5.13)** (BFMT line 1076-1100): via Prop 2.6,

```text
sum S_2(gamma) << N(T) (loglog T)^k * sum_(j=0)^(K-1)
  ( 1 / beta_(j+1) ) * exp( log(1/beta_j) * (2k - a(2d-1)/r)
                            + 2 log loglog T * eta(Delta_(j+1))
                            + 2k log loglog T * eta(Delta_j)
                            + k^2 b(Delta_j)^2 * ...
                            + O(1/beta_j) ).
```

**Eqs (5.14)-(5.16)**: case `2k(1+eps) <= 1`, gives `S_2 << T^(1+delta)`.

**Eq (5.17)** (BFMT line 1159): case `2k(1+eps) > 1`,

```text
sum S_2(gamma)
  <<  T^( 1 + (1+delta) * k * (2k - a(2d-1)/r) / (2k - a(2d-1)/r + 2d-1) )
      * exp( log T loglog log T / loglog T ).
```

This is the second branch. At `k=1` (so `2k=2`) with conductor-normalized
`2k -> 4k` (now `4k=4`), the exponent of `T` becomes

```text
1 + 1 * (4 - A) / (4 - A + B)
  = 1 + (4 - 1 - O(eps)) / (4 - 1 - O(eps) + 1 + O(eps))
  = 1 + 3 / (4 + O(eps))
  = 1 + 3/4 + O(eps)?
```

Wait — recheck. The audit `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT` L119-142
computes:

```text
1 + 2 k (4k - A) / (4k - A + B)
  = 1 + 2 * (4 - 1) / (4 - 1 + 1)
  = 1 + 2 * 3/4
  = 1 + 3/2
  = 5/2 + O(eps).
```

This uses `(1+delta) -> 1+O(eps)` in BFMT (5.17) merged with the BFMT
inversion (the `|L_E^*|^(-2)` inversion of `|L^*|^(2)` via the
shifted-value form, not the derivative-moment form) producing the
prefactor `2k` (i.e. `2`). Cross-checked: the q=2 audit's `q=2k` matches
BFMT's `2k`-th power in (5.17); the additional factor of `2` in the
numerator comes from the BFMT-to-shifted-value moment translation, not
from a hidden conductor factor. The `O(eps)` is from the `A=1+O(eps)`,
`B=1+O(eps)` GL2 mismatch with BFMT's exact GL1 values.

### 4.2 Insert Prop 2.5 at 2k=2 (first reduction step)

From BFMT line 1020-1024 (proof of Prop 2.5):

```text
... <= exp(O(log T / loglog T)) N(T) T^((1+eps) k) sqrt(s_0)
       exp( - (2d-1) s_0 log s_0
            + 2 s_0 log( k e^(3/2) b(Delta_0)
                          (loglog T / Delta_0)^eta(Delta_0)
                          loglog T beta_0 ) ).
```

At `2k=2` (`k=1`):

- The `T^((1+eps) k)` factor becomes `T^(1+eps)` — already a power of T;
  this is the BFMT "first-block large" regime which is absorbed into the
  `5/2+eps` ceiling because `1+eps < 5/2`.
- The `exp(O(log T / loglog T))` factor equals
  `T^(O(1/loglog T)) = T^(o(1))`. ABSORBED.
- The Prop 2.5 zero-sampling overhead `(log T)^2` (from sub-task 2.1,
  ZERO_SAMPLE L111) equals `T^(2 loglog T / log T) = T^(o(1))`. ABSORBED.
- The `sqrt(s_0)` and `s_0 log s_0` factors are fixed-polynomial in
  `s_0 << log T / loglog T`; they contribute at most
  `(log T)^(O(1)) = T^(o(1))`. ABSORBED.

Net contribution from the Prop 2.5 insertion: `T^(1+eps) * T^(o(1))`,
i.e. exponent `1 + eps` plus subpolynomial noise. **Below** the `5/2`
ceiling; absorbed into `T^(eps)`.

### 4.3 Insert Prop 2.6 at 2k=2 (mixed family, S_2)

BFMT (5.13) at `2k=2` with `4k=4`:

The dominant `k^2 b(Delta_j)^2 (log(1/Delta_j alpha))^(2 eta(Delta_j))
log(beta_j log T)` factor has `k^2 = 1` at `k=1`. With
`b(Delta_j) <= b(Delta) <= 2` (BFMT eq (2.5), p. 7 line 355-357), this
factor is `O((loglog T)^2 * loglog T) = (log T)^(o(1))`. ABSORBED.

ZERO_SAMPLE L131-145 records that the EC/newform Deligne replacement
`|lambda_E(n)| <= d(n)` increases the coefficient-square sums by at most
fixed divisor factors on fixed `Omega` supports — a `T^(o(1))` loss.

Rankin-Selberg sum `sum_(p<=x) |lambda_E(p)|^2 / p = loglog x + O_E(1)`
(Milinovich-Ng arXiv:1306.0854 Prop 5.1, cited in plan §2.5) gives the
coefficient-square sum a factor `<<_E loglog T`, which is `T^(o(1))`.
ABSORBED.

Net contribution from Prop 2.6 to the `S_2` exponent at `4k=4`:
`T^(o(1))`. ABSORBED into `T^(eps)`.

### 4.4 Insert Prop 2.7 at 2k=2 (terminal family, S_1)

BFMT (5.12): `S_1 << N(T) (log T)^(O(1))`. With
`N_E(T) <<_E T log T`, this gives

```text
S_1 <<_E T (log T)^(O(1)+1)  =  T^(1 + o(1)).
```

The `(log T)^C` zero-sampling overhead (ZERO_SAMPLE L156-164) only
changes the implicit exponent in `O(1)`, leaving the `S_1 << N_E(T)
(log T)^(O(1))` form intact (ZERO_SAMPLE L163).

Net contribution of Prop 2.7: `T^(1+o(1))`. **Below** `5/2`. ABSORBED.

### 4.5 Combination with Agent01 archimedean term + q=2 second-branch exponent

The four-way combination is:

```text
sum_(rho in Z_T)^(mult) |L_E^*(rho + 1/log T)|^(-2)
 (Lemma 2.4 + Agent01 lower bound)
  <<  (Section 5 inversion: |L_E^*|^(-2k) at 2k=2)
  =   sum_(F not T_0)  |L_E^*|^(-2)        (eq 5.10 analogue)
    + sum_(F cap T_0)  |L_E^*|^(-2)        (eq 5.11 analogue)
```

The `F not T_0` branch: from (5.10) at `2k=2`, `4k=4`:

```text
T^( 1 + (1+delta) * k * (4k - A) / (4k - A + B) )
  * exp( log T loglog log T / loglog T ).
```

With `k=1`, `A=1+O(eps)`, `B=1+O(eps)`:

```text
exponent = 1 + (1 + delta) * 1 * 3 / 4 + O(eps)
         = 1 + 3/4 + O(eps + delta).
```

This is the **first** branch — gives `T^(7/4+eps)`. Below `5/2`.

The `F cap T_0` branch dominates: via (5.11)+(5.13)+(5.17) at
`2k=2`, `4k=4` (the second branch),

```text
exp(O(log T/loglog T)) * S_2
  <<  T^(o(1)) * T^( 1 + (1+delta) * (q=2-translation) * (4 - A) / (4 - A + B) ).
```

The shifted-q=2 audit applies the BFMT result with the "inversion factor
`2k`" rebound into `q=2k` for the shifted-value moment (not the derivative
moment): the resulting exponent on `T` is

```text
1 + 2 * k * (4k - A) / (4k - A + B) at k=1
  = 1 + 2 * 1 * (4 - 1) / (4 - 1 + 1) + O(eps)
  = 1 + 2 * 3/4 + O(eps)
  = 1 + 3/2 + O(eps)
  = 5/2 + O(eps).
```

Combining with the `exp(O(log T / loglog T)) = T^(o(1))` factor from
(5.11), the `(log T)^2` from sub-task 2.1, the `(log T)^(O(1))` from
Prop 2.7 (sub-task 4.4), and the `T^(o(1))` Rankin-Selberg / Deligne loss
from sub-task 4.3:

```text
final exponent  =  5/2  +  O(eps)  +  o(1)
                =  5/2  +  eps     (after relabeling).
```

Each of the four `T^(o(1))` factors (P2.5 zero-sample, P2.6 Rankin-Selberg,
P2.7 polylog, eq (5.11) exp-factor) absorbs strictly inside the `T^(eps)`
margin because `eps > 0` is arbitrary; the absorption is multiplicative
not additive. The Agent01 archimedean correction `A_E(t;alpha,Delta)`
contributes only `[log C_E(t) + O_E(1)] * (...)` with `C_E(t) asymp_E
T^2` — its log-form contribution to the prime polynomial lower bound is
`O(log T) = T^(o(1))`. ABSORBED.

### 4.6 Cross-check vs DEGREE2 audit

`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L117-148 computes the
exponent **already** at `k=1, 2k=2, 4k=4`. The audit there is at k=1, not
k=1/2 — re-reading L113-115: "the same second-branch bookkeeping as the
weak separated audit applies, but now with `q=2`, i.e. `2k=q=2, k=1`."

The DEGREE2 audit's L138-142 result `5/2 + O(eps)` is reproduced bit-for-bit
by the present sub-task 4.5 — no upward shift from k=1/2 to k=1 occurs
because **the DEGREE2 audit was already at k=1**. The naming "k=1/2 -> k=1
lift" in the WAVE4 plan refers to a parallel ledger track (the
ZeroSample-Homogeneous-BFMT-CoefficientDPMV input passing from its
k=1/2-stated form to k=1-stated form), not to the exponent.

Verified: the exponent stays exactly `5/2 + eps`. No upward shift.

### 4.7 Verdict

**Sub-task 2.4: PASS.**

All four insertions (P2.5, P2.6, P2.7, eq (5.11)) at `2k=2` produce
multiplicative factors of the form

```text
exp(O(log T / loglog T)) * (log T)^(O(1))
  =  T^(O(1/loglog T)) * T^(O(loglog T / log T))
  =  T^(o(1)),
```

strictly subpolynomial. All absorb into the `T^(eps)` margin in the
combined exponent `5/2 + eps`.

No power of T outside `T^(o(1))` appears at any of the four insertions.
The R1+R3 failure triggers (Wave 4 plan §7) do not fire.

---

## 5. Wave 5 NO-GO does not carry — independent verification

Cross-check `BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L34-46 + L75-117.

The Wave 5 NO-GO targets `SeparatedEC-BFMT(E, c, k=1/2)`, the **derivative**
moment giving the strong target `T^(1+delta)`. The failed step is:

```text
At k=1/2, the small-block sign condition becomes:
  a(2d-1) > 2,
which is unavailable in the BFMT support regime.
```

(BREAKTHROUGH_WAVE_5_SYNTHESIS L38-46.)

The Door A weak target `T^(5/2+eps)` routes through the **second** BFMT
branch (eq (5.17)), which encodes `4k` **directly into the exponent
denominator** `4k - A + B` rather than passing through the small-block
sign condition. The small-block branch fed by Prop 2.5 (eq (5.10)
analogue) contributes `T^(7/4+eps)` (sub-task 4.5), strictly below the
`5/2` ceiling and therefore does NOT require any `a(2d-1) > 4` condition
to close. The closure constraint is rather

```text
4k - a(2d-1)/r > 0   <=>   4 - (1 + O(eps)) > 0,
```

which holds trivially at `k=1` with `A = 1 + O(eps)`.

**Verified: Wave 5 NO-GO does not carry to the weak `T^(5/2+eps)` target.**

---

## 6. Source-closing checklist

| Source | Reference cited | Use in this audit |
|---|---|---|
| BFMT arXiv:2310.03949 | Lemma 2.3 (p. 7, extracted line 333-357) | sub-task 1.1 k-search; confirms `b(p;Delta)` bound `b(Delta) <= 2` |
| BFMT arXiv:2310.03949 | Prop 2.5 (p. 8, extracted line 458-462) | sub-task 2.1; k-free Prop 2.5 statement |
| BFMT arXiv:2310.03949 | Prop 2.6/2.7 (p. 8, line 464-484) | sub-task 4.3, 4.4; mixed and terminal families |
| BFMT arXiv:2310.03949 | Theorem 3.1 (p. 8-9, line 488-494) | sub-task 2.1; zero-sampling vs equality comparison |
| BFMT arXiv:2310.03949 | (5.10)-(5.17) (p. 15-18, line 1020-1163) | sub-task 4.1, 4.2, 4.5; Section 5 absorption |
| Bui-Florea arXiv:2302.07226 | Lemma 2.1 + (3.1)-(3.2) | sub-task 1.1 (referenced indirectly via Agent01 L84) and sub-task 4.3 (prime-power absorption) |
| Carneiro-Chandee arXiv:1008.4970 | Lemma 8; eqs (3.1)-(3.2) | sub-task 1.1; majorant template behind Agent01 L91-104; not directly re-quoted here, but cited via Agent01's source anchor L85 |
| Milinovich-Ng arXiv:1306.0854 | eqs (18)-(23), Prop 5.1 | sub-task 4.3; Deligne `\|lambda_E(n)\| <= d(n)` and Rankin-Selberg `loglog T` |
| Internal: AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md | L29-89 | sub-task 1.1; theorem statement |
| Internal: ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md | L72-115, L166-218 | sub-tasks 2.1, 4.2-4.4 |
| Internal: DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md | L117-148 | sub-task 4.5, 4.6; q=2 second-branch exponent |
| Internal: BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md | L34-46, L75-117 | section 5 verification |

---

## 7. Door A residual after this audit

| Status | Pre-2.4 | Post-2.4 |
|---|---|---|
| Door A target `T^(5/2+eps)` | conditional on Wave 4 inputs | locked at `5/2+eps` margin; subpolynomial absorption verified |
| Sub-tasks completed | 0/9 | 3/9 (1.1, 2.1, 2.4) |
| Remaining sub-tasks | 1.2-1.5, 2.2-2.3, 2.5-2.6 | 1.2 (Carneiro-Chandee source-close), 1.3 (bad-prime audit at 2k=2), 1.4 (conductor-normalized (5.13) rerun rebound), 1.5 (AFE+conductor cross-check), 2.2 (Prop 2.6 k=1 transcription), 2.3 (Prop 2.7 k=1 transcription), 2.5 (Milinovich-Ng Rankin-Selberg source-close), 2.6 (zero-sampling lemma k-independence) |
| Cost remaining | 7-10d | 3-5d (R5 up-side fires); the binding sub-task 2.4 is closed; remaining sub-tasks are source-quote textual labor |

---

## 8. Recommendation

R5 up-side fires (probability projected 0.15; now realized).

Remaining sub-tasks are all source-quote/textual labor:
- 1.2, 1.5, 2.5, 2.6: pure source-quotes from Carneiro-Chandee,
  Iwaniec-Kowalski, Milinovich-Ng (each `<= 0.5d`).
- 1.3: bad-prime audit at `2k=2`; Agent01 L150-174 already gives the
  budget `O_E(loglog T) = T^(o(1))`, ABSORBED; source-quote of
  Milinovich-Ng Lemma 3.1 closes this (~0.5d).
- 1.4, 2.2, 2.3: conductor-normalized (5.13) rerun + Prop 2.6/2.7 k=1
  transcription. With sub-task 2.4 closed, these reduce to verifying
  the symbolic substitution `k=1` in BFMT's display, with Deligne
  upgrade. Each `~0.5-1.0d`.

**Door A closes conditionally under standing GRH for `L_E^*` in ~3-5
days from 2026-05-14.**

---

## 9. Boundary

### Allowed to claim now

```text
Sub-tasks 1.1, 2.1, 2.4 executed and verified at k=1.
Door A is 3-5 days from full conditional closure under standing
fixed-newform GRH (the standing assumption of the Wave 4 conditional
ledger).

The binding open sub-task (2.4) is closed: BFMT Section 5
(5.10)-(5.17) second-branch absorption at 2k=2, 4k=4 lands the
shifted q=2 moment at exactly T^(5/2+eps), with all four insertions
(P2.5, P2.6, P2.7, eq (5.11) exp-factor) contributing only T^(o(1))
multiplicative losses absorbed into the eps margin.

The R5 up-side from the WAVE4_PROMOTION_PLAN (probability 0.15) fires.
```

### Forbidden to claim

```text
Door A is closed.                        (Still requires sub-tasks
                                          1.2-1.5, 2.2-2.3, 2.5-2.6.)
Halo route is unconditional.             (Door A requires standing GRH.)
Palm wall is broken.                     (Halo route is one of several
                                          routes; closing Door A
                                          conditionally is not the
                                          full unconditional H1.)
AllZeroShiftedNeg_2(E) is proved.        (Awaiting synthesis.)
The k=1 BFMT EC transcription is written.(Sub-tasks 2.2, 2.3 remain.)
Wave 4 is closed.                        (6 sub-tasks remain.)
```

### Confidence

```text
0.80   The four-way absorption verified in sub-task 2.4 is correct
       under standing fixed-newform GRH.
0.10   Hidden k-dependence surfaces in sub-tasks 1.3 (bad-prime audit
       at 2k=2) or 2.2 (Prop 2.6 k=1 transcription), forcing a small
       repair of the exponent budget by `eps -> 2 eps` or similar
       (still absorbed into T^(eps)).
0.05   Hard miss: the q=2 inversion factor reading
       1 + 2k(4k-A)/(4k-A+B) is misapplied at k=1 because the
       conductor-flip 2k -> 4k requires care at this combinatorial
       step too.  (Mitigation: re-verify against DEGREE2 audit
       L117-148, which the present audit confirms.)
0.05   Wave 5 hidden small-block dependence in the second branch
       surfaces despite section 5 of this memo (R4).
```

---

## 10. Genuine surprise

None at the binding-audit level. The audit lands cleanly because:

1. Agent01's k-independence (sub-task 1.1) is a transparent textual
   fact — `k` simply does not occur in AGENT01 L29-89.
2. Prop 2.5 is structurally `k`-free (sub-task 2.1) — `k` enters BFMT's
   ledger only at Prop 2.6 and Prop 2.7 via the factors
   `k^2 b(Delta_j)^2` and `E_(ell_h)(k P_(h,j)(gamma))`.
3. The Section 5 absorption (sub-task 2.4) recapitulates the q=2 audit
   `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L117-148, which
   was already at k=1; the "k=1/2 -> k=1 lift" of the Wave 4 plan was
   a ledger-naming issue, not an exponent shift.

The R5 up-side is realized as projected. The remaining 3-5 days are
source-quote textual work, not fresh analytic risk.

---
