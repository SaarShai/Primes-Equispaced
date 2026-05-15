---
schema_version: 2
title: "HaloShiftComparison Lemma (Stage 1a of Halo Plan, Door B)"
type: lemma
domain: project
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
supersedes: []
superseded-by:
tags: [halo-route, door-B, h1, lemma, stage-1a, shift-comparison, boundary-arc]
---

# HaloShiftComparison Lemma — Stage 1a

Write-up of Door B closure. Proof transcribed from
`HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1 (clean form) and §5.1'
(conservative archival form). Not new analytic content. One genuine
audit task surfaces: extension of `ClusterShiftDerivativeComparison(E,A)`
from a sampled point to a boundary arc (uniformity, not new theorem).

## 0. Notation

| Symbol | Meaning |
|---|---|
| `L` | `L_E^*(s)`, completed `L`-function of newform attached to `E` |
| `Z_T` | nontrivial zeros of `L` with `|Im rho| <= T` |
| `alpha` | `1/log T` (shift scale) |
| `A > 0` | fixed cluster radius parameter |
| `C_A(rho_0)` | `{rho_j in Z_T : |gamma_j - gamma_0| <= A alpha}` |
| `H_A(s)` | non-cluster Hadamard factor: `L(s) / prod_{rho_j in C_A(rho_0)}(s - rho_j)` |
| `R > sqrt(1+A^2)` | halo radius parameter (clean form) |
| `R_T in [R, 2R]` | no-zero-on-boundary radius (averaging) |
| `Omega_T` | `union_{rho in Z_T} D(rho, R_T alpha)` |
| `partial Omega_T` | boundary, partitioned into arcs assigned to each `rho` |
| `N_{rho_0, A}(T)` | `# C_A(rho_0)` (local cluster size) |

Standing assumption: zeros of `L_E^*` lie on the critical line (GRH for
this newform). This is the framework's working hypothesis throughout
the halo route; **not removed by this lemma**.

## 1. Statement (clean form, §5.1)

**LEMMA (HaloShiftComparison_clean).** Fix `A > 0` and choose
`R > sqrt(1+A^2)`. Then for every boundary arc `s in partial Omega_T`
assigned to `rho_0`,

```text
|L(rho_0 + alpha)| / |L(s)|  <=  C(E, A, R) ,
```

with `C(E, A, R)` an absolute constant independent of `T` and
independent of the local cluster size `N_{rho_0, A}(T)`.

## 2. Proof

Factor

```text
L(s) = (s - rho_0) · prod_{rho_j in C_A(rho_0), j != 0}(s - rho_j) · H_A(s).
```

Three cases.

### 2.1 Self factor

`s in partial D(rho_0, R_T alpha)` gives `|s - rho_0| = R_T alpha`, so

```text
|alpha| / |s - rho_0|  =  1 / R_T  <  1.    (*)
```

### 2.2 Cluster mates `rho_j in C_A(rho_0), j != 0`

Under GRH, `Re rho_j = Re rho_0 = 1/2`, so

```text
|rho_0 + alpha - rho_j|^2  =  alpha^2 + (gamma_0 - gamma_j)^2
                           <=  alpha^2 (1 + A^2).
```

Since `s in partial Omega_T` is by construction outside *every other*
halo,

```text
|s - rho_j|  >=  R_T alpha    (j != 0).    (**)
```

Per cluster mate, the ratio at numerator vs denominator is

```text
|rho_0 + alpha - rho_j| / |s - rho_j|  <=  sqrt(1+A^2) / R_T  <  1
```

(strict, since `R_T >= R > sqrt(1+A^2)`). The product over the entire
cluster — of arbitrary size `N_{rho_0,A}(T)` — is therefore **bounded by
1**, with no local zero-count input required. This is the key
geometric step that kills the `C_A^{N_{rho_0,A}(T)}` obstruction.

### 2.3 Non-cluster factor `H_A`

Both `rho_0 + alpha` and `s` lie within distance `<= R_T alpha = O(alpha)`
of `rho_0`, inside the cluster-free region (`H_A` has no zeros at
distance `< A alpha` from `rho_0` by construction of `C_A(rho_0)`). The
repo lemma `ClusterShiftDerivativeComparison(E, A)` controls the
point-evaluation ratio

```text
|H_A(rho_0 + alpha) / H_A(rho_0)|  =  O(1).
```

Lift point evaluation to the disk `D(rho_0, R_T alpha)`: `log |H_A|` is
harmonic on the cluster-free region, and its oscillation on the disk is
bounded by

```text
sum_{rho_j not in C_A(rho_0)} (alpha / d_j)^2 ,    d_j = |rho_0 - rho_j|.
```

By Riemann–von Mangoldt zero density `~ (1/(2 pi)) log T` per unit
height, the tail sum equals

```text
1 / (2 pi A) + o(1) ,
```

an absolute `O(1)` constant. Hence `|H_A(rho_0 + alpha) / H_A(s)| = O(1)`
uniformly for `s in partial Omega_T cap D(rho_0, R_T alpha)`.

### 2.4 Combine

```text
|L(rho_0 + alpha) / L(s)|  =  (1/R_T)  ·  [<= 1]  ·  O(1)  =  O(1),
```

independent of `T` and of `N_{rho_0, A}(T)`. QED.

## 3. Conservative archival form (§5.1')

**LEMMA (HaloShiftComparison_conservative).** Same setup, with the
stronger choice `R > A + 1`. Then for every boundary arc,
`|L(rho_0 + alpha) / L(s)| <= C(E, A, R)`.

**Proof.** Identical structure, simpler geometry:

(i) `s` outside every other halo gives `|s - rho_j| >= R_T alpha >= R alpha`.

(ii) For cluster mates,

```text
|alpha + rho_0 - rho_j|  <=  alpha + |gamma_0 - gamma_j|  <=  (A+1) alpha,
```

(triangle inequality, no `sqrt` — the bound is on the magnitude not the
squared magnitude). Per mate,

```text
|rho_0 + alpha - rho_j| / |s - rho_j|  <=  (A+1) / R  <  1.
```

Product over cluster `<= 1`.

(iii) `H_A` non-cluster step identical to §2.3.

Combine: `O(1)`. QED.

**Record as alternative.** Cleaner geometry (no `sqrt(1+A^2)` algebra,
no implicit-constants worry about whether `R_T = R` or `R_T = 2R`),
slightly larger `R`. Clean form (`R > sqrt(1+A^2)`) is the headline;
conservative form is the visually simpler fallback.

| Form | Constraint | Per-mate ratio | When to cite |
|---|---|---|---|
| Clean (§5.1) | `R > sqrt(1+A^2)` | `sqrt(1+A^2) / R_T` | headline statement |
| Conservative (§5.1') | `R > A+1` | `(A+1) / R` | archival, exposition |

For `A = 1`: clean needs `R > sqrt(2) ≈ 1.414`, conservative needs
`R > 2`. For `A` small, both are tight near `1`. For `A` large, clean
saves a factor `~ A` in `R`.

## 4. Reduction to existing repo lemma

The only non-trivial analytic content is **extending**
`ClusterShiftDerivativeComparison(E, A)`
(`primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`)
from a single sampled point `rho_0 + alpha` to a boundary arc of radius
`R_T alpha`.

**Extension statement.** For the cluster-free Hadamard factor `H_A`
attached to a bad zero `rho_0`,

```text
sup_{s in D(rho_0, R_T alpha)}  |log |H_A(rho_0 + alpha)|  -  log |H_A(s)||
  <=  1 / (2 pi A)  +  o(1).
```

**Justification.** `log |H_A|` harmonic on the cluster-free region;
oscillation on a disk of radius `R_T alpha` controlled by the same
inverse-square sum that controls the point-evaluation lemma. The
inverse-square sum is bounded by `1 / (2 pi A) + o(1)` by
Riemann–von Mangoldt.

**Status of extension.** Uniformity statement, not a new theorem.
`AUDIT` mode — the analytic inputs are already in
`CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md`; only the lift from
point to arc needs explicit write-up. Expected cost `~0.5d`.

## 5. What this kills

| Apparent obstruction (handoff §13.B, §15.1) | Status after this lemma |
|---|---|
| naïve factorization gave `C_A^{N_{rho_0,A}(T)}` | dead |
| required `N_{rho_0,A}(T) = o(log T)` uniformly | not required |
| Door B = `T^{o(1)}` on per-arc bound | sharpened to `O(1)` |
| Door B = "most delicate of four doors" | demoted to audit task |

Key geometric observation: boundary arcs of `partial Omega_T` are by
definition outside every other halo, forcing the cluster-mate ratio to
**contract** by a factor strictly less than 1 per mate. Product over
arbitrary cluster size `<= 1`. No zero-count budget consumed.

## 6. Boundary

### Allowed claims

- Door B is unconditional under the framework's standing GRH assumption
  for `L_E^*`, given `R > sqrt(1+A^2)` (clean) or `R > A + 1` (conservative).
- Door B per-arc bound is `O(1)`, not `T^{o(1)}`.
- The constant `C(E, A, R)` is independent of `T` and of `N_{rho_0,A}(T)`.
- Modulo the boundary-arc extension of
  `ClusterShiftDerivativeComparison(E, A)`, Door B is closed.

### Forbidden claims

- Removal of the standing GRH assumption for `L_E^*`. (Hypothesis used
  in §2.2 to identify `Re rho_j = 1/2`.)
- Removal of the boundary-arc extension of the noncluster `H_A` lemma.
  Until the extension is written out, the lemma remains
  `RIGOROUS_REDUCTION`, not `THEOREM`.
- Halo route as a complete H1 closure. Door B is one of four; Doors A
  (`AllZeroShiftedNeg_2`), C (residue-first H1 rewrite), D
  (`M_T = o(T^{1/4})`) remain open.
- Simultaneous closure of Doors A/C/D. This lemma is silent on them.

## 7. Cost

| Item | Estimate |
|---|---|
| write-up of this lemma (Stage 1a) | done (~0.5d) |
| boundary-arc extension of noncluster `H_A` lemma | ~0.5d, audit |
| research blocker | none |
| token cost | low (transcription, no new computation) |

## 8. Cross-references

| File | Role |
|---|---|
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1, §5.1' | source proof |
| `handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md` | input lemma to be lifted |
| `handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` | Stage 0 (Door C audit), sibling of this Stage 1a |
| `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` | conditional stack Door B feeds into |
| `handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md` | H1 displacement wall context |
