---
schema_version: 1
title: "Agent 01 H1 rank-one anti-small-derivative packet"
date: 2026-05-11
agent: "Agent 01 -- EC H1 Rank-One Anti-Small-Derivative"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
tags: [ec-ndc, h1, rank-one, reciprocal-derivative, layer-cake]
---

# Agent 01 H1 Rank-One Anti-Small-Derivative

## Verdict

No fixed-curve EC theorem is promoted.

For analytic rank

```text
r = ord_(s=1) L(E,s) = 1,
```

the current absolute simple-zero target remains

```text
R_E,1(T)
 = sum_(T<|gamma|<=2T, simple)
     |L'(E,1+i gamma)|^(-1)
 = o(T^2).
```

Status: `RIGOROUS_REDUCTION`.

This packet proves exact reductions to layer-cake tails, sparse-exception
budgets, local minimum-modulus/near-multiple-zero exclusions, and the pointwise
threshold

```text
|L'(E,1+i gamma)| >= h(T) log T / T,    h(T)->infinity.
```

It does not prove any of those anti-small-derivative inputs for a fixed curve.

External theorem claims: none. No external theorem is cited in this packet.
All zero-count, contour, and height statements below are either local packet
inputs or explicitly stated as hypotheses.

## Local Context Read

- `start.md`
- `token-economy.yaml`
- `L0_rules.md`
- `L1_index.md`
- `primes-equispaced/L0_rules.md`
- `primes-equispaced/L1_index.md`
- `primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-all-in-wave/H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md`
- `primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md`
- `primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md`
- `primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`

## Rank-One Reduction

Assume the local H1 finite-box contour mode, smoothstep-scale decay

```text
|W_hat(it)| << (1+|t|)^(-2),
```

and legal moving heights

```text
T_box(u)=exp(Cu+O(1)),    u=log K.
```

For dyadic shells define

```text
A_W(T)=sum_(T<|gamma|<=2T, simple)
  |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1).
```

Then

```text
A_W(T) << T^(-2) R_E,1(T).
```

If `R_E,1(T)=o(T^2)`, then `A_W(2^j)=o(1)`. Since
`#{j:2^j<=T_box(u)}=O(u)`, Cesaro summation of nonnegative shells gives

```text
sum_(2^j<=T_box(u)) A_W(2^j)=o(u).
```

For analytic rank one this is exactly the absolute simple-zero condition
needed for the H1 offcentral residue aggregate to be `o(u)`, below the central
term `u/L'(E,1)`.

Status: `RIGOROUS_REDUCTION`.

Important refinement: the pointwise dyadic target is sufficient, not necessary.
The actual finite-box absolute condition is

```text
sum_(j<=N) 2^(-2j) R_E,1(2^j)=o(N),    N ~= log T_box(u).
```

Thus sparse bad dyadic shells are allowed only if their weighted shell budget
has Cesaro mean `o(1)`.

## Layer-Cake Route

Let

```text
X_gamma=|L'(E,1+i gamma)|^(-1),
N_E(T;V)=#{T<|gamma|<=2T, simple: X_gamma>V}.
```

For a finite shell,

```text
R_E,1(T)=int_0^infty N_E(T;V) dV.
```

Under the local zero-count input

```text
N_E(T,2T) << T log T,
```

the range `0<=V<=1` contributes `O(T log T)=o(T^2)`. Therefore

```text
R_E,1(T)=o(T^2)
```

is equivalent to

```text
int_1^infty N_E(T;V) dV=o(T^2).
```

Status: `RIGOROUS_REDUCTION`.

Sufficient theorem candidates:

```text
Power tail:
  N_E(T;V) <= C T^2 Phi(T)^(-1) V^(-1-alpha)
  for V>=1, alpha>0, Phi(T)->infinity.

Conclusion:
  R_E,1(T)=o(T^2).
```

```text
Borderline capped tail:
  N_E(T;V) <= C T^2 Phi(T)^(-1) V^(-1)
  for 1<=V<=C_T,
  X_gamma<=C_T,
  log C_T=o(Phi(T)).

Conclusion:
  R_E,1(T)=o(T^2).
```

For a polynomial cap `C_T=T^A`, the borderline route needs

```text
Phi(T)/log T -> infinity.
```

No-go: a `V^(-1)` tail without a cap or extra logarithmic saving gives a
divergent layer-cake integral. It does not prove the rank-one target.

Status: `NO_GO` for uncapped borderline tails.

## Pointwise Route

Assume the local zero-count input and the pointwise lower bound

```text
|L'(E,1+i gamma)| >= h(T) log T / T
```

for every simple zero in `T<|gamma|<=2T`, with `h(T)->infinity`. Then

```text
R_E,1(T)
 <= N_E(T,2T) T/(h(T) log T)
 << T^2/h(T)
 = o(T^2).
```

Status: `RIGOROUS_REDUCTION`.

This identifies the exact rank-one pointwise scale available from zero count:
a diverging factor above `log T/T` is enough. A fixed constant multiple of
`log T/T` only gives `R_E,1(T)=O(T^2)`, which is not enough for rank one by the
absolute route.

Status: `NO_GO` for non-diverging `h(T)` unless a separate cancellation/PV
theorem replaces absolute control.

## Sparse-Exception Budget

Let

```text
V_0(T)=T/(h(T) log T),    h(T)->infinity.
```

If all but a bad set `B_T` satisfy `X_gamma<=V_0(T)`, then the good part is

```text
<< T log T * T/(h(T) log T) = O(T^2/h(T)) = o(T^2).
```

The bad part is harmless exactly when it has reciprocal budget

```text
sum_(gamma in B_T) X_gamma=o(T^2).
```

A checkable sufficient version is

```text
#B_T <= B(T),
X_gamma <= C(T) on B_T,
B(T) C(T)=o(T^2).
```

Status: `RIGOROUS_REDUCTION`.

No-go: cardinality sparsity alone is false. Even one bad simple zero can
destroy `R_E,1(T)=o(T^2)` if `|L'(rho)|^(-1)` is not capped. Thus claims of
"rare near-multiple behavior" must include a product budget or a layer-cake
tail, not only a count of exceptions.

Status: `NO_GO` for count-only sparse exceptions.

## Near-Multiple-Zero Mechanism

For a simple zero `rho=1+i gamma`, write

```text
L(E,s)=(s-rho) g_rho(s),    g_rho(rho)=L'(E,rho).
```

If for some radius `r_T` the disk boundary is zero-free and satisfies

```text
min_(|s-rho|=r_T) |L(E,s)| >= m_T,
```

then on the boundary

```text
|g_rho(s)| >= m_T/r_T.
```

By the maximum principle applied to `1/g_rho`,

```text
|L'(E,rho)|=|g_rho(rho)| >= m_T/r_T.
```

With

```text
r_T=T^(-kappa)(log T)^(-b),
m_T=T^(-mu)(log T)^(-B),
```

this gives

```text
|L'(E,rho)| >= T^(-(mu-kappa))(log T)^(b-B).
```

To imply the rank-one pointwise route, it is enough that

```text
T^(1-(mu-kappa)) (log T)^(b-B-1) -> infinity.
```

Equivalently, either `mu-kappa<1`, or `mu-kappa=1` with logarithmic surplus
`b-B>1`.

Status: `RIGOROUS_REDUCTION`.

Interpretation: near-multiple zeros are dangerous because they obstruct a
zero-free circle around `rho`; but separation alone is insufficient. The route
needs both a zero-free radius and a boundary minimum-modulus lower bound.

No-go: pair spacing, simplicity, or pair-correlation data alone cannot rule
out small `L'(rho)`. They do not lower-bound the nonzero local factor
`g_rho(rho)`.

Status: `NO_GO` for spacing-only near-multiple control.

## Actual Multiple Zeros

The target `R_E,1(T)` sums simple zeros only. It does not handle true
offcentral multiple zeros.

From the local Laurent algebra, an offcentral zero of multiplicity `m` and
kernel zero order `h_rho` has generic effective degree

```text
d_rho=m-1-h_rho.
```

For analytic rank one, pointwise H1 needs every unretained offcentral
exceptional degree to be `<1`. Hence a multiple zero is harmless only if

```text
m <= h_rho+1
```

after exact kernel killing or same-frequency cancellation, or else it is
retained/profiled/averaged in the theorem mode. With no kernel zero at that
frequency, this allows only simple zeros.

Status: `NO_GO` for using `R_E,1(T)=o(T^2)` to absorb actual multiple-zero
Laurent terms.

## Obstruction Map

| Route | Status | Exact obstruction |
|---|---:|---|
| `R_E,1(T)=o(T^2)` | `RIGOROUS_REDUCTION` | Sufficient for rank-one simple-zero absolute H1, but unproved for fixed EC. |
| Dyadic Cesaro shell budget | `RIGOROUS_REDUCTION` | Weaker than pointwise shell little-o; still needs reciprocal budgets for all bad shells below `T_box(u)`. |
| Layer-cake power tail | `RIGOROUS_REDUCTION` | Needs a real small-derivative anti-concentration theorem. |
| Borderline `V^(-1)` tail | `NO_GO` | Needs cap/log surplus; uncapped integral diverges. |
| Pointwise `h(T)logT/T` | `RIGOROUS_REDUCTION` | Sharp zero-count scale; fixed `h` gives only `O(T^2)`. |
| Sparse exception count | `NO_GO` | Count alone omits reciprocal magnitude; need `sum_bad X_gamma=o(T^2)` or `B(T)C(T)=o(T^2)`. |
| Near-multiple exclusion | `RIGOROUS_REDUCTION` | Works only with zero-free circle plus boundary minimum modulus. |
| Spacing/pair correlation alone | `NO_GO` | Does not control local nonzero factor `g_rho(rho)`. |
| Actual multiple zeros | `NO_GO` | Simple-zero target omits Laurent polynomial terms. |
| H2 branch damping | `NO_GO` | H2 endpoint damping cannot be imported into H1 reciprocal poles. |
| Selected contour heights | `DIAGNOSTIC_ONLY` | They route horizontal contour size, not `1/L'(rho)` tails. |
| Fixed-weight PV cancellation | `DIAGNOSTIC_ONLY` | Could replace absolute l1 only after a uniform fixed-weight phase theorem. |

## Exact Next Theorem Candidates

Candidate A, tail theorem:

```text
For fixed E of analytic rank one, prove
int_1^infty N_E(T;V) dV=o(T^2).
```

This is equivalent to `R_E,1(T)=o(T^2)` under local zero count.

Candidate B, pointwise theorem:

```text
For fixed E, prove
min_(T<|gamma|<=2T, simple)
  |L'(E,1+i gamma)| >= h(T) log T/T,
h(T)->infinity.
```

This directly implies the rank-one target.

Candidate C, sparse-exception theorem:

```text
For fixed E, prove
X_gamma <= T/(h(T)logT) outside B_T,
h(T)->infinity,
and sum_(gamma in B_T) X_gamma=o(T^2).
```

The product-budget version `#B_T*C(T)=o(T^2)` is enough but not necessary.

Candidate D, local minimum-modulus theorem:

```text
For every simple zero rho in the shell, find a zero-free circle
|s-rho|=r_T with min |L(E,s)|>=m_T and
m_T/r_T >= h(T)logT/T, h(T)->infinity.
```

This is the clean near-multiple-zero exclusion route.

## Verification Notes

- Used analytic rank only.
- Did not import H2 branch damping into H1 reciprocal-pole control.
- Did not draft or reference Koyama correspondence.
- Did not cite any external theorem; no `curl`/`pdftotext` source claim was
  needed for this packet.
- Created the parent directory only if needed.
- Wrote only the requested Agent 01 file.

## Changed Files

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT01_H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_2026-05-11.md`
