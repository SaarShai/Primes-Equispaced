---
schema_version: 1
title: "Agent 04 Bad-Set Complement Budget"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 04 -- Bad-Set Complement Budget"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
dependencies:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md
tags: [breakthrough-wave-3, h1, bad-set, reciprocal-derivative, zero-clusters, minimum-modulus]
---

# Agent 04 Bad-Set Complement Budget

status: `RIGOROUS_REDUCTION`

## Verdict

The bad-set complement can be made theorem-ready, but only as a reciprocal
budget. Count-only control is dead.

For fixed `E` and dyadic shell `T < |gamma| <= 2T`, put

```text
S_T = {simple zeros rho=1+i gamma in the shell},
X_rho = |L'(E,rho)|^(-1),
B_T subset S_T.
```

The exact bad-set target is

```text
R_B(T) = sum_(rho in B_T) X_rho = o(T^2).
```

Every viable route must prove one of:

```text
Direct tail:
  int_1^infinity #{rho in B_T : X_rho > V} dV = o(T^2).

Count plus reciprocal cap:
  B_T subset union_j B_(j,T),
  #B_(j,T) <= M_j(T),
  X_rho <= C_j(T) on B_(j,T),
  sum_j M_j(T) C_j(T) = o(T^2).

Individual certificate:
  X_rho <= c_rho on B_T,
  sum_(rho in B_T) c_rho = o(T^2).
```

Close-pair counts, zero-density estimates, simplicity proportions, and
boundary-cap geometry only become useful after they supply `M_j(T)` in a
count-cap condition or a direct tail integral. They do not imply `R_B(T)=o(T^2)`
alone.

## Standing Inputs

This packet does not source-promote any external theorem. It uses the Wave 2
shell-count input only as a standing local hypothesis:

```text
N_T = #S_T <<_E T log T.
```

If the good set `G_T=S_T\B_T` has

```text
X_rho <= T/(h(T) log T),     h(T) -> infinity,
```

then

```text
sum_(rho in G_T) X_rho
  << T log T * T/(h(T) log T)
  = o(T^2).
```

Thus H1 rank-one closure is reduced exactly to `R_B(T)=o(T^2)` plus separate
handling of actual multiple zeros under the Laurent package. Analytic rank is
the only rank notion used here.

## Exact Layer-Cake Form

For

```text
F_B(T;V) = #{rho in B_T : X_rho > V},
```

one has the identity

```text
R_B(T) = int_0^infinity F_B(T;V) dV.
```

Since `int_0^1 F_B(T;V)dV <= #B_T <= N_T << T log T`, the bad-set target is
equivalent, under the shell count, to

```text
int_1^infinity F_B(T;V) dV = o(T^2).
```

This is the cleanest exact condition. Any proposed bad-set theorem should be
translated into this integral or into a count-cap estimate that implies it.

## General Bucket Lemma

Let

```text
B_T subset union_(j in J_T) B_(j,T).
```

If for each bucket

```text
#B_(j,T) <= M_j(T),
X_rho <= C_j(T) for rho in B_(j,T),
```

then

```text
R_B(T) <= sum_(j in J_T) M_j(T) C_j(T).
```

Therefore a sufficient and exact bookkeeping condition is

```text
sum_(j in J_T) M_j(T) C_j(T) = o(T^2).
```

Without the caps `C_j(T)`, the implication is false. For any nonempty counted
bucket, one zero with arbitrarily small `|L'(rho)|` can make `X_rho` exceed
`T^2` while all cardinality estimates remain true. This is the fundamental
reason count-only routes must be killed.

## Close-Pair Counts

Define nearest-neighbor spacing inside the relevant zero set by

```text
d_rho = min_(rho' != rho) |rho-rho'|.
```

For a cluster threshold `delta_T`, set

```text
C_T(delta_T) = {rho in S_T : d_rho <= delta_T},
P_T(delta_T) = #C_T(delta_T).
```

A close-pair estimate gives only

```text
#(B_T intersect C_T(delta_T)) <= P_T(delta_T).
```

It proves the bad budget only if paired with a reciprocal cap:

```text
P_T(delta_T) C_cl(T) = o(T^2),
X_rho <= C_cl(T) on B_T intersect C_T(delta_T).
```

Useful scale consequences:

```text
P_T(delta_T) << T log T:
  need C_cl(T) = o(T/log T).

P_T(delta_T) << T^(theta) L(T), theta < 2:
  need C_cl(T) = o(T^(2-theta)/L(T)).

P_T(delta_T) = o(T/L(T)):
  allows C_cl(T) = O(T L(T)) only if the little-o is strong enough.
```

### Weighted Pair Version

Close-pair counts become stronger if combined with a local minimum-modulus
factorization.

Assume a disk `|s-rho| <= R` contains exactly two simple zeros, `rho` and
`rho'`, with `d=|rho-rho'|`, and

```text
min_(|s-rho|=R) |L(E,s)| >= m.
```

Writing

```text
L(E,s) = (s-rho)(s-rho') h(s),
```

the nonvanishing factor `h` satisfies on the boundary

```text
|h(s)| >= m/(R(R+d)) >= m/(2R^2)
```

when `d <= R`. Hence

```text
|L'(E,rho)| = d |h(rho)| >= d m/(2R^2),
X_rho <= 2R^2/(m d).
```

Thus pair data can close a cluster budget only in the inverse-spacing form

```text
(2R^2/m) sum_(rho in cluster bucket) 1/d_rho = o(T^2).
```

Dyadic spacing layers `delta_(k+1) < d_rho <= delta_k` give the sufficient
condition

```text
(2R^2/m) sum_k
  #{rho in B_T : delta_(k+1) < d_rho <= delta_k}/delta_(k+1)
  = o(T^2).
```

Plain `P_T(delta_T)` lacks the inverse-spacing weight and is not enough.

### Higher Local Multiplicity

If a disk centered at `rho` contains `k` simple zeros

```text
rho=rho_0, rho_1, ..., rho_(k-1),
```

all within radius `R`, and

```text
min_(|s-rho|=R) |L(E,s)| >= m,
```

then

```text
L(E,s) = product_(a=0)^(k-1) (s-rho_a) h(s)
```

gives

```text
X_rho
  <= R(2R)^(k-1)
     /(m product_(a=1)^(k-1) |rho-rho_a|).
```

So a `k`-cluster route needs a product-distance reciprocal budget:

```text
sum_(rho in k-cluster bucket)
  R(2R)^(k-1)
  /(m product_(a=1)^(k-1) |rho-rho_a|)
  = o(T^2).
```

Local cluster counts or bounded local multiplicity alone do not control this
product.

## Zero-Density Inputs

A zero-density or local-density estimate can only reduce the number of bad
zeros. Let it give

```text
#D_T <= M_den(T)
```

for some density-defined bad bucket `D_T`. The needed condition is still

```text
M_den(T) C_den(T) = o(T^2),
X_rho <= C_den(T) on D_T.
```

If

```text
M_den(T) << T^theta L(T),
```

then the required reciprocal cap is

```text
C_den(T) = o(T^(2-theta)/L(T)).
```

Consequences:

```text
theta = 1 with L(T)=log T:
  need C_den(T)=o(T/log T).

theta < 1:
  polynomially weaker caps can work.

theta >= 2:
  density alone cannot leave room for any growing reciprocal cap.
```

Zero-density data also cannot lower-bound `L'(rho)` at the remaining simple
zeros unless it creates zero-free disks plus boundary lower bounds. Density is
a counting input, not a reciprocal-derivative input.

## Simplicity Proportions

Simplicity information has two separate roles.

Actual multiple zeros are not part of `R_B(T)` because `R_B(T)` sums only over
simple zeros. They remain Laurent terms and must be absent, kernel-killed,
retained, averaged, or shown to have effective degree below the analytic-rank
threshold.

For bad simple zeros, a simplicity proportion is only a count statement. If it
implies an exceptional simple bucket of size

```text
M_sim(T),
```

then the required budget is still

```text
M_sim(T) C_sim(T) = o(T^2),
X_rho <= C_sim(T) on that bucket.
```

In particular, a positive proportion of simple zeros gives no upper bound for

```text
sum_(simple bad rho) |L'(E,rho)|^(-1).
```

It does not prevent a sparse family of simple zeros from having very small
derivative.

## Minimum-Modulus Disks

This is the only local route that directly gives a reciprocal cap.

For a simple zero `rho`, suppose there is a radius `r_rho` such that the
punctured disk

```text
0 < |s-rho| <= r_rho
```

contains no zero, and

```text
min_(|s-rho|=r_rho) |L(E,s)| >= m_rho.
```

Writing

```text
L(E,s) = (s-rho) g_rho(s),
```

the function `1/g_rho` is holomorphic in the disk. The maximum principle gives

```text
X_rho = |g_rho(rho)|^(-1) <= r_rho/m_rho.
```

Thus a minimum-modulus disk theorem closes a bucket `A_T` exactly when

```text
sum_(rho in A_T) r_rho/m_rho = o(T^2).
```

Uniform version:

```text
#A_T <= M_A(T),
r_rho/m_rho <= C_A(T),
M_A(T) C_A(T) = o(T^2).
```

Good-zero threshold:

```text
r_rho/m_rho <= T/(h(T) log T), h(T)->infinity
```

is enough for all but a bad reciprocal budget, because `N_T << T log T`.

Failure of a disk certificate creates an uncontrolled bucket. It cannot be
charged to the minimum-modulus theorem that failed; it needs its own direct
tail or count-cap budget.

## Boundary Caps

Partial boundary control is not a substitute for a full minimum-modulus circle
unless the bad arcs have a lower bound too.

Let

```text
L(E,s)=(s-rho)g_rho(s)
```

and suppose `g_rho` has no zeros in `|s-rho| <= r`. On the boundary, let
`Omega_rho` be a union of bad arcs with normalized angular measure
`epsilon_rho`. Assume

```text
|L(E,s)| >= m                  outside Omega_rho,
|g_rho(s)| >= exp(-H_rho)      on Omega_rho.
```

The harmonic mean formula for `log|g_rho|` gives

```text
log |g_rho(rho)|
  >= (1-epsilon_rho) log(m/r) - epsilon_rho H_rho.
```

Therefore

```text
X_rho
  <= (r/m)^(1-epsilon_rho) exp(epsilon_rho H_rho).
```

A boundary-cap route closes a bucket only if

```text
sum_(rho in cap bucket)
  (r_rho/m_rho)^(1-epsilon_rho)
  exp(epsilon_rho H_rho)
  = o(T^2).
```

Small cap length alone is useless if `H_rho` is absent. With no lower bound on
the cap arcs, `H_rho=infinity`, so there is no reciprocal cap.

Uniform cap version:

```text
#A_T <= M_A(T),
(r/m)^(1-epsilon) exp(epsilon H) <= C_A(T),
M_A(T) C_A(T) = o(T^2).
```

If `M_A(T) << T log T`, this demands

```text
(r/m)^(1-epsilon) exp(epsilon H) = o(T/log T).
```

## Carry-Forward Condition

The usable Wave 3 bad-set theorem input is:

```text
H1-BadSetComplementBudget(E):
  For each dyadic T, the bad simple zeros B_T are covered by finitely or
  countably many buckets:

    B_T subset C_T union D_T union S_T^bad union U_T union Q_T,

  where:

    C_T      = clustered or near-multiple simple zeros,
    D_T      = density-defined exceptional zeros,
    S_T^bad  = simplicity/multiplicity-adjacent simple exceptions,
    U_T      = zeros lacking full local minimum-modulus disks,
    Q_T      = zeros whose boundary control has cap arcs.

  For each bucket A_T in this cover, one proves at least one of:

    int_1^infinity #{rho in A_T : X_rho > V} dV = o_A(T^2),

    #A_T <= M_A(T), X_rho <= C_A(T), M_A(T)C_A(T)=o_A(T^2),

    X_rho <= c_rho and sum_(rho in A_T) c_rho=o_A(T^2).

  The sum of all o_A(T^2) errors is o(T^2).
```

Then

```text
sum_(rho in B_T) |L'(E,rho)|^(-1) = o(T^2).
```

Combined with the good-zero certificate

```text
X_rho <= T/(h(T) log T), h(T)->infinity,
```

and the shell count, this gives

```text
R_E,1(T)=o(T^2)
```

for the simple-zero H1 rank-one reciprocal target. It does not handle actual
multiple-zero Laurent terms; those remain under the separate finite-box
multiple-zero rules.

## Killed Routes

| Route | Decision | Reason |
|---|---:|---|
| Close-pair count only | killed | Counts clustered zeros but gives no cap for `X_rho`. |
| Pair correlation only | killed | Even strong spacing statistics do not bound the zero-free local factor. |
| Zero-density only | killed | Density controls cardinality/locations, not reciprocal derivative size. |
| Positive simplicity proportion only | killed | A sparse simple subfamily with tiny derivative can dominate `R_B(T)`. |
| Local zero count or bounded cluster size only | killed | Product of neighbor distances can still be arbitrarily small. |
| Minimum-modulus disks with full boundary lower bounds | viable reduction | Gives `X_rho <= r_rho/m_rho`; needs summed cap `o(T^2)`. |
| Minimum-modulus disks except uncontrolled arcs | viable only with cap depth | Needs `exp(epsilon H)` budget; arc length alone fails. |
| Direct small-derivative tail | viable reduction | Exactly equivalent by layer cake. |
| H2 branch damping for H1 poles | killed | Not a reciprocal-pole damping mechanism and not used here. |

## Source Protocol Notes

No external theorem was fetched or promoted in this packet. All theorem-shaped
statements above are conditional reductions or elementary local consequences
proved inline from factorization and maximum/harmonic mean principles.

## Verification Notes

Read targeted context only:

```text
start.md
token-economy.yaml
L0_rules.md
L1_index.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md
```

Checks:

```text
./te doctor returned ok:true.
Top-level status is one allowed Wave 3 value.
No theorem promotion.
No external theorem claim needing curl/pdftotext.
Analytic rank only.
No H2 branch damping used as H1 reciprocal-pole damping.
No Koyama correspondence or email draft touched.
Only assigned output file written.
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT04_BAD_SET_COMPLEMENT_BUDGET_2026-05-11.md
```
