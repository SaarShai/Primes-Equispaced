---
schema_version: 2
title: "Section 5 Conductor-Normalized Rerun Verification (Sub-tasks 1.1 + 1.4)"
type: theorem-audit
domain: project
tier: working
status: VERIFIED_AT_EQUATION_LEVEL
confidence: 0.86
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/WAVE4_PROMOTION_PLAN_2026-05-14.md
supersedes: []
superseded-by:
tags: [wave-4-promotion, sub-task-1-4, sub-task-1-1, bfmt, section-5, conductor-normalized, k-equals-1, q-equals-2, door-A]
---

# Section 5 Conductor-Normalized Rerun Verification

Sub-tasks 1.1 and 1.4 of `WAVE4_PROMOTION_PLAN_2026-05-14.md`. Equation-level verification, no theorem promoted beyond what the q=2 audit already conditioned on.

## 1. Sub-task 1.1 — Agent01 k-independence (by inspection)

Claim: `GL2-BFMT-PrimePolynomialLowerBound(E)` as stated in `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` L29-89 is structurally k-independent. The k-dependence enters only downstream in BFMT Section 5 when `|L_E^*(s)|^(-2k)` is integrated against the lower bound.

Verification:

- Display at L44-52:
  ```text
  log |L_E^*(s)|
   >= A_E(t;alpha,Delta)
      - Re sum_(p<=x, p not | N_E) b_E(p;Delta) lambda_E(p) p^(-s)
      - C_E log log T
      + O_E(Delta^2 exp(pi Delta)/T + Delta log(1+Delta T)/sqrt(T)).
  ```
  No `k` symbol appears. The display is a uniform-in-(`t, alpha, Delta`) lower bound on `log |L_E^*(s)|`.

- The conductor term L57-64
  ```text
  A_E(t;alpha,Delta) = [log C_E(t) + O_E(1)]/(2 pi Delta) * log(1 - exp(-2 pi alpha Delta)) + O_E(1)
  C_E(t) asymp_E T^2
  ```
  is `k`-independent.

- Prime, prime-square, higher-prime-power, and bad-prime absorption (L132-174) cost `O_E(log log T)` regardless of `k`. The coefficient-square sums in the absorption use Deligne `|lambda_E(n)| <= d(n)`, Rankin-Selberg `sum_{p<=x} |lambda_E(p)|^2 / p = log log x + O_E(1)`, and finite bad-prime cardinality — none depend on `k`.

Conclusion: sub-task 1.1 passes. Agent01's display is usable at `2k=2` (i.e., q=2, k=1) without any new lemma, in exactly the form stated.

## 2. Sub-task 1.4 — Conductor-normalized BFMT (5.13)/(5.17) at q=2, k=1

### 2.1 BFMT zeta original (verbatim from extract L935-1163)

BFMT parameter choice in the case `2k(1+ε) > 1` (the relevant branch for k=1):

Equations (5.4)-(5.7), L944-947:
```text
beta_0 = (2k + 2d - 1 - a(2d-1)/r) log log T / ((1+delta) k log T)
s_0 = 1/beta_0
ell_0 = 2 s_0^d / 2
a = (1 - 3 k eps)/(1 - 2 k eps)
r = 1/(1 - 2 k eps)
d = (2 - 7 k eps)/(2(1 - 3 k eps))
a(2d-1)/r = 1 - 4 k eps.
```

Set `A := a(2d-1)/r`, `B := 2d - 1`. At small `eps`: `A = 1 + O(k eps)`, `B = 1 + O(k eps)`.

BFMT (5.13) at the second branch (L1090-1101): exponential factor maximum at `j=0` is
```text
exp[ log(1/beta_0) (2k - A) ].
```

Substitution of (5.6) for `beta_0` and BFMT pointwise bound (5.8) `|zeta(sigma + i gamma)|^(-1) << (log T)^((1+eps)/2)` yields (5.17) at L1159:
```text
sum_(gamma in F) |zeta'(rho)|^(-2k)
  << T^{ 1 + (1+delta) k (2k - A)/(2k - A + B) } exp(log T log log log T / log log T).
```

The `exp(log T log log log T / log log T)` factor is `T^{o(1)}`.

### 2.2 GL2 conductor flip rule (Wave 5 L100-105, restated)

For one fixed elliptic curve `E/Q` (weight-2 cuspidal newform of level `N_E`), the analytic conductor satisfies
```text
log C_E(t) = 2 log T + O_E(1) on T <= t <= 2T (Iwaniec-Kowalski Ch. 5).
```

This is exactly `2 x` the zeta conductor-log. Wave 5 Agent01 (`AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md`, summarized at `BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L100-105) records that the archimedean main term doubles:
```text
zeta archimedean:       beta_j^(-1) log(1 - exp(-beta_j))
GL2 archimedean:    (2 + o(1)) beta_j^(-1) log(1 - exp(-beta_j)).
```

Since BFMT (5.6) sets `beta_0` from the archimedean main term, the conductor flip enters every BFMT bookkeeping factor that scales with `log T` from the conductor. Effective substitution rule throughout Section 5:
```text
k -> 2k                  (everywhere k appears as a BFMT exponent or buffer).
```

Direct check at the small-block sign condition (Wave 5 L38-46): condition `a(2d-1)/r > 2k` (zeta) becomes `> 4k` (GL2), consistent with `k -> 2k`.

Direct check at the prefactor of (5.17): `(1+delta) k` (zeta) becomes `(1+delta) 2k` (GL2). This is the doubling that takes the q=2 derivative moment from `T^{3/2+eps}` (zeta) to a hypothetical `T^{5/2+eps}` (GL2), and that takes the q=2 shifted moment to `T^{5/2+eps}`.

### 2.3 Branch routing at q=2, k=1

Strong-target / first branch condition (zeta): `2k(1+eps) <= 1`. At k=1: `2(1+eps) > 1`. **Not in first branch.**

Strong-target / first branch condition (GL2, under `k -> 2k`): `4k(1+eps) <= 1`. At k=1: `4(1+eps) > 1`. **Not in first branch.**

Both zeta and GL2 are routed into the second branch (5.17) at k=1. There is no path through (5.16) or the small-block sign route for the q=2 weak target.

This means the small-block sign condition `a(2d-1)/r > 4k = 4` (Wave 5 L38-46 verdict: unavailable in BFMT support regime) is irrelevant for the q=2 weak target — the small-block sign route is not the binding route.

### 2.4 Exponent computation at q=2, k=1

Apply `k -> 2k` substitution to BFMT (5.17):

```text
sum_(gamma in F) |L_E^*'(rho)|^(-2k)
  << T^{ 1 + (1+delta) (2k) (2(2k) - A)/(2(2k) - A + B) } T^{o(1)}.
```

At `k = 1`, `A = 1 + O(eps)`, `B = 1 + O(eps)`:

```text
prefactor:   (1 + delta) (2k)               = (1 + delta) * 2 = 2 + 2 delta
inner num:   2(2k) - A                       = 4 - 1            = 3 + O(eps)
inner denom: 2(2k) - A + B                   = 4 - 1 + 1        = 4 + O(eps)
inner ratio: 3/4 + O(eps)
exponent:    1 + (2 + 2 delta) * 3/4 + O(eps)
           = 1 + 3/2 + (3/2) delta + O(eps)
           = 5/2 + O(delta) + O(eps).
```

After relabeling `delta, eps -> eps`:

```text
sum_(gamma in F) |L_E^*'(rho)|^(-2)  <<_E  T^{5/2 + eps}.
```

This is the q=2 **derivative moment** result over the separated set `F = F_E(T,c)`. Door A's target is the same exponent but for the **shifted negative moment** over all simple critical zeros `S_E(T)`:

```text
sum_(rho in S_E(T)) |L_E^*(rho + 1/log T)|^(-2)  <<_E  T^{5/2 + eps}.
```

The shifted moment is bounded by the derivative moment via the cluster-shift identity (`CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`) for separated zeros, AND by BFMT Lemma 2.4 directly for all zeros (the shifted moment is what Lemma 2.4 actually states, before any separated/bad split). The audit `DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L88-98 confirms this: "BFMT Lemma 2.4 ... is a shifted-value statement over all zero ordinates. It does not use the separated set F."

Hence the same `5/2 + eps` exponent applies to the shifted moment over `S_E(T)`:

```text
Degree2WeakShiftedNeg_2(E):
  sum_(rho in S_E(T)) |L_E^*(rho + 1/log T)|^(-2)  <<_(E, eps)  T^{5/2 + eps}.
```

### 2.5 Verification that no hidden factor blocks the margin

BFMT (5.17) carries the `exp(log T log log log T / log log T)` factor. This is `T^{o(1)}`.

Under `k -> 2k`, this factor becomes `exp(2 log T log log log T / log log T)`. Still `T^{o(1)}`. No fixed-power loss.

Other (5.13) terms:
- `(K-j) (log log T)^k`: unchanged structure, `k -> 2k` doubles `k` in `(log log T)^k`, giving `(log log T)^{2k} = (log log T)^2` at k=1. Absorbed into `T^{eps}`.
- `2k log log T eta(Delta_j)`: doubles to `4k log log T = 4 log log T` at k=1. Absorbed.
- `k^2 b(Delta_j)^2 log(...)^{2eta(Delta_j)}`: `k^2 -> 4k^2 = 4` at k=1. Absorbed.

All polylog factors remain `T^{o(1)}` under `k -> 2k`. Margin to `T^{5/2 + eps}` is intact.

### 2.6 Result

```text
Sub-task 1.4: PASS at equation level.
GL2 conductor-normalized BFMT (5.13)/(5.17) at q=2, k=1 lands at T^{5/2 + eps}.
Branch: second branch (5.17), not first branch (5.16). Small-block sign
condition not on the binding path.
```

## 3. Cross-check against the audit

`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L117-148 computes the exponent as
```text
1 + 2 * (4 - 1)/(4 - 1 + 1) = 1 + 3/2 = 5/2,
```
using `A = a(2d-1)/r = 1 + O(eps)`, `B = 2d-1 = 1 + O(eps)`. This matches §2.4 above modulo the `(1+delta)` factor which the audit relabels away.

The audit's prefactor `2k` (not `(1+delta) k`) is the post-substitution form (k -> 2k applied to BFMT's prefactor `(1+delta)k`, then `(1+delta) -> 1` after relabeling).

The factor-of-2 is the conductor flip; the substitution rule is the BFMT-(5.6)-derived rule `k -> 2k` throughout Section 5; the second-branch routing is verified by `2k(1+eps) > 1` at k=1 for both zeta and GL2 (under `k -> 2k`, condition `4k(1+eps) > 1` also holds).

## 4. Residual risks (after this verification)

| Risk | Verdict |
|---|---|
| R1 (small-block sign fails at k=1 for loose target) | **Retired** by §2.3: the q=2 weak target is routed through second branch (5.17), not the small-block sign branch. |
| R2 (Agent01 prime-polynomial lemma develops k-dependence) | **Retired** by §1: Agent01's display is k-independent by inspection. |
| R3 (bad-prime audit eats Door A exponent margin) | Open. Sub-task 1.3 is the explicit `O_E(log log T)` audit at `2k=2`. The k-independence of the Deligne / Rankin-Selberg / finite-bad-prime absorption (cited in §1) suggests R3 is benign, but explicit `2k=2` polylog accounting is still needed for full sub-task 1.3 closure. |
| R4 (Wave 5 NO-GO carries to weak target) | **Retired** by §2.3: Wave 5 NO-GO targets `2k(1+eps) <= 1` first-branch closure, which is irrelevant for the q=2 weak target. |

Net: sub-task 1.4 closure retires risks R1, R2, R4 explicitly. R3 remains for the bad-prime audit at `2k=2`, but the structural k-independence of the absorption arguments makes it likely benign.

## 5. Downstream effect on Door A closure

After sub-tasks 1.1 and 1.4 verification:

| Door A residual gap | Status after this audit |
|---|---|
| Multiplicity extension `S_E(T) -> Z_T^{mult}` | Retired (`HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md`) |
| RvM multiplicity lemma `m_rho = O_E(log T)` | Retired (`HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md`) |
| Wave 4 sub-task 1.4 (Section 5 conductor rerun at k=1) | **Retired this audit** |
| Wave 4 sub-task 1.1 (Agent01 k-independence) | **Retired this audit** |
| Wave 4 sub-task 1.2 (Carneiro-Chandee majorant source-quote) | Open, 0.5d. Mechanical source-quote. |
| Wave 4 sub-task 1.3 (bad-prime audit at 2k=2) | Open, 1.0d. R3 mitigation. |
| Wave 4 sub-task 1.5 (AFE+conductor cross-check) | Open, 0.5d. Mechanical. |
| Wave 4 sub-tasks 2.1-2.6 (Props 2.5/2.6/2.7 transcription + Section 5 absorption at k=1) | Open. Sub-task 2.4 is the next binding open arithmetic. |
| Synthesis: assemble `AllZeroShiftedNeg_2(E)` statement under standing GRH | Open, 1.0d after 2.4 closes. |

Headline: Wave 4 promotion is now ~3.5 days of source-closing audit (sub-tasks 1.2, 1.3, 1.5, 2.1-2.6, synthesis), down from 7-10 days. The binding open arithmetic shifts from 1.4 to 2.4.

## 6. Boundary

Promote:
```text
Sub-task 1.1 verified by inspection: Agent01 display is k-independent.
Sub-task 1.4 verified at equation level: BFMT (5.13)/(5.17) at q=2, k=1
under the GL2 conductor-flip rule k -> 2k yields S_2(gamma) << T^{5/2+eps},
matching Door A's target.

Risks R1, R2, R4 retired. R3 remains for explicit bad-prime audit at 2k=2.
```

Do not promote:
```text
Door A closed (still requires sub-tasks 1.2, 1.3, 1.5, 2.1-2.6, synthesis).
Sub-task 2.4 closed (the multi-proposition Section 5 absorption check at
                     2k=2 is the next binding open arithmetic).
Unconditional H1 (still under standing GRH for L_E^*).
The Palm wall closed (Door A is the halo-route bypass; the wall itself
                      stands as before).
```

Confidence: 0.86 in this verification. The 0.14 residual is concentrated in sub-tasks 1.3 (bad-prime audit) and 2.4 (multi-proposition absorption).
