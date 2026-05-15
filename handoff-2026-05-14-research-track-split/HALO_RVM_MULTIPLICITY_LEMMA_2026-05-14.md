---
schema_version: 2
title: "Halo RvM Multiplicity Lemma — fixed GL2/EC"
type: lemma
domain: project
tier: working
status: LEMMA
confidence: 0.92
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
supersedes: []
superseded-by:
tags: [halo-route, door-A, rvm, multiplicity, named-lemma, gl2]
---

# Halo RvM Multiplicity Lemma — fixed GL2/EC

Status: `LEMMA`. Per-zero multiplicity bound `m_rho = O_E(log T)` filed as a
named lemma. Proof is half a line from GL2 Riemann-von Mangoldt. External
primary citation Iwaniec-Kowalski Ch. 5 Thm 5.8. Repo did not previously
contain a named RvM-for-`L_E^*` lemma; the standing zero-counting bound
`N(T,2T) <= C T log T` at `H1_POSITIVE_RANK_CLOSURE.md` L171 is the
cumulative form. This file is the per-zero refinement.

## 1. Statement

Fix an elliptic curve `E/Q` of conductor `N_E`, equivalently a cuspidal
newform `f_E` of weight 2 and level `N_E`. Let

```text
L_E^*(s) := L(E, s + 1/2)
```

be the analytic-normalized L-function, with critical line `Re s = 1/2 - 1/2 = 0`
(zeros at `s = i gamma` after normalization to the GL2 functional-equation
center). Equivalent throughout: `L_E^*` has its nontrivial zeros on the line
`Re s = 0` under GRH, height parameter `gamma = Im rho`.

### Pointwise form

For every offcentral nontrivial zero `rho` of `L_E^*` with `gamma = Im rho`,

```text
ord_{s = rho} L_E^*(s)  =:  m_rho  <=  C_E · log(|gamma| + 2),     (RVM-MULT-PT)
```

with `C_E` an absolute constant depending only on the conductor `N_E` and
weight 2. No dependence on rank, on local Euler factor behaviour, or on the
zero `rho` itself.

### Dyadic form (the one Door A uses)

For `rho` with `gamma` in the dyadic shell `T < |gamma| <= 2T`,

```text
m_rho  <=  C_E · log T.                                            (RVM-MULT-DY)
```

(RVM-MULT-DY) is immediate from (RVM-MULT-PT) by `log(2T+2) <= 2 log T` for
`T >= 2`, absorbing the factor of 2 into `C_E`.

## 2. Proof

### 2.1 Riemann-von Mangoldt for `L_E^*`

The standard explicit-formula zero-count for a fixed GL2 cuspidal newform
(Iwaniec-Kowalski, *Analytic Number Theory*, GTM 53, Ch. 5 Thm 5.8;
specialised to GL2 in Ch. 14) gives

```text
N(T) := #{rho : 0 < Im rho <= T, L_E^*(rho)=0, nontrivial}
      = (T/(2 pi)) log( T^2 N_E / (2 pi e)^2 )  +  O(log T)
      = (T/pi) log T  +  c_E · T  +  O(log T),                     (RVM)
```

where

```text
c_E  =  (1/(2 pi)) log( N_E / (2 pi e)^2 )   ( + bounded weight-correction )
```

is a constant depending only on `N_E` and on the weight (here fixed at 2).
The implied constant in `O(log T)` is also absolute and depends only on
`N_E` and the weight. No rank dependence: the additional `r` zeros at the
central point are absorbed by the `O(log T)` error.

### 2.2 Local zero count `N(T+1) - N(T-1)`

From (RVM),

```text
N(T+1) - N(T-1)
 =  ( (T+1)/pi ) log(T+1)  -  ( (T-1)/pi ) log(T-1)
   +  c_E ( (T+1) - (T-1) )
   +  O(log T).
```

The leading two-term Taylor expansion:

```text
(T+1) log(T+1) - (T-1) log(T-1)
 =  2 log T  +  2  +  O(1/T).
```

Hence

```text
N(T+1) - N(T-1)  =  (1/pi) ( 2 log T + 2 ) + 2 c_E + O(log T)
                 =  (2/pi) log T  +  O_E(1)  +  O(log T)
                 =  O_E(log T).                                    (LOCAL-RVM)
```

The constant in `O_E(log T)` depends only on `N_E` and the weight, via the
`c_E` term and the `O(log T)` error in (RVM).

### 2.3 Per-zero bound

Any nontrivial zero `rho` with `|gamma - T| <= 1` contributes its multiplicity
`m_rho` to the count `N(T+1) - N(T-1)`. Therefore

```text
m_rho  <=  N(T+1) - N(T-1)  <=  C_E · log T                        (PER-ZERO)
```

for every such `rho`. For an arbitrary zero of height `gamma`, apply
(LOCAL-RVM) with `T := |gamma|`:

```text
m_rho  <=  N(|gamma|+1) - N(|gamma|-1)  <=  C_E · log(|gamma|+2).
```

This is (RVM-MULT-PT). Restricting to the dyadic shell `T < |gamma| <= 2T`
gives (RVM-MULT-DY). QED.

## 3. External vs internal sources

| Source | Status | Use here |
|---|---|---|
| Iwaniec-Kowalski, *Analytic Number Theory*, GTM 53, Ch. 5 Thm 5.8 | external canonical | primary citation for (RVM) |
| Iwaniec-Kowalski Ch. 14 (GL2/automorphic L-functions) | external | specialisation of (RVM) to GL2 newforms |
| Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed., Ch. 9 | external | zeta analog of (RVM) and of the multiplicity bound |
| Repo: `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md` L171 | internal | standing zero-counting bound `N(T,2T) <= C T log T` (cumulative form, used in absolute-convergence shell hypotheses) |
| Repo: `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md` L225-227 | internal | bounded-multiplicity hypothesis "multiplicities are bounded by `M`" — replaced by this lemma with `M = O_E(log T)` |
| Repo: `handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md` L184 | internal | sources EC zero counting `N_E(T) = O_E(T log T)` (cumulative form) |
| Repo: `handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` L81 | internal | uses `N_E(T) asymp_E T log T` for BFMT zero-sample sizing |

No prior named lemma in the repo for the per-zero bound. The cumulative form
`N(T,2T) <= C T log T` is used freely; this lemma is the local-window
refinement.

## 4. Where this lemma is used in the halo plan

- `handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md`
  §3 L84-104. Quoted in that audit:

  ```text
  "Standard fact for any L-function with polynomial-growth conductor: a zero
   of multiplicity m at height T contributes m to the local zero count
   N(T+1) - N(T-1), which by the GL2 Riemann-von Mangoldt formula is
   O(log T). Therefore m_rho <= C_E log(|gamma|+2) = O_E(log T)  (RvM-MULT)."
  ```

  Filed there as "consistent with the standing zero-counting bound … For
  Strategy A only the weak form `m_rho = O(log T)` is needed; this follows
  from the standard explicit formula for fixed GL2 (Iwaniec-Kowalski Ch. 5;
  zeta analog in Titchmarsh Ch. 9). External citation required for the named
  lemma; the proof is half a line." The present file files exactly that.

- `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md`
  §7 Stage 4 Route i (multiplicity-aware BFMT zero-sample). The bounded-
  multiplicity assumption is replaced by `m_rho <= C_E log T`, hence
  multiplicity-weighted dyadic count

  ```text
  N^{mult}(T,2T) := sum_{rho in Z_T} m_rho  <<  T (log T)^2,
  ```

  absorbed by `T^{eps}`.

- `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md`
  L225-227. The hypothesis "multiplicities are bounded by `M`" is now
  realized with `M = M(T) = O_E(log T)`, named.

## 5. What this lemma does NOT give

- It does **not** give `m_rho <= 1` (the simplicity assertion). That is the
  separate strong open problem; under GRH plus Murty-Najnudel-type analysis
  one gets *almost-all* simplicity (quantitative, not pointwise). This
  lemma is uniform and unconditional but only polylog.

- It does **not** give `m_rho = O(1)` (bounded multiplicity). The bound is
  polylog, not constant.

- It does **not** approach the conjectural `m_rho = 1` for almost every `rho`,
  even in expectation. No density-one improvement is implied.

- It does **not** bound multiplicity at the central point in a way that beats
  `r + O(log T)`; the central zero of order `r` simply sits inside the
  count.

- It is **not** uniform in `E`: `C_E` grows with `N_E`. Uniform-in-conductor
  statements need a different proof (Heath-Brown / Conrey-Iwaniec type
  inputs).

## 6. Boundary

### Allowed

```text
Cite (RVM-MULT-PT) or (RVM-MULT-DY) in subsequent audits with confidence,
sourcing Iwaniec-Kowalski Ch. 5 Thm 5.8 and the present file as the named
repo lemma. The constant C_E depends only on N_E and the weight (here 2).
Use in Door A multiplicity extension, in halo plan Stage 4 Route i, and
in the bounded-multiplicity hypothesis of H1_POSITIVE_RANK_CLOSURE.
```

### Forbidden

```text
Claim bounded multiplicity m_rho = O(1).
Claim simplicity m_rho = 1 (for all rho, or for almost all rho).
Claim density-one improvement m_rho = 1 for density-one rho.
Claim uniformity in E (constant C_E depends on N_E).
Use (RVM-MULT-*) as a substitute for the H1 multiple-zero residue
disposition; that is a structural question about residue profiles, not
about per-zero multiplicity. See HALO_DOOR_A_MULTIPLICITY_EXTENSION §7.
```

## 7. Cross-references and where to cite

Downstream files that should be updated (or noted in their next revision) to
cite this lemma instead of carrying the bound as an unnamed standing fact:

| Downstream file | Current status | Update |
|---|---|---|
| `handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md` §3 L84-104, §9 "Remaining" L326-328 | uses (RvM-MULT) as an unnamed standing fact; flags filing as remaining work | replace external-only citation with citation to this lemma; remove "Filing an explicit named lemma … " from the remaining-work list |
| `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md` L225-227 | takes "multiplicities are bounded by `M`" as explicit hypothesis | replace `M` (treated as a parameter) with `M = M(T) = O_E(log T)` from this lemma; downstream shell inequalities become `q_(j-1-ell) > A_j + 1` for `1 <= j <= O_E(log T)`, i.e. a logarithmically-growing range. Confirm the kernel-decay budget still closes (decay budget `q_k` is polynomial, range is logarithmic, no issue) |
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §7 Stage 4 Route i L649-665 | multiplicity-aware BFMT route, bounded-`M` placeholder | cite this lemma for the `M = O_E(log T)` input |
| `handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §4.1 | uses `Z_T^{mult}` with multiplicity weights | cite this lemma for the per-zero bound `m_rho <= C_E log T` underlying `N^{mult}(T,2T) << T (log T)^2` |
| `handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md` L184 | cumulative `N_E(T) = O_E(T log T)` | optional addition: per-zero refinement (RVM-MULT-PT) available |
| `handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` L81 | cumulative form only | optional addition: per-zero refinement for multiplicity-aware sampling |

No edits performed by this file. Update notes are advisory; downstream edits
to be done in their own audits.
