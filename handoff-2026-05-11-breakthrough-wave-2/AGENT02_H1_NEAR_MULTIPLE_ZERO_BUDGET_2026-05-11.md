---
schema_version: 1
title: "Agent 02 H1 near-multiple-zero reciprocal budget"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 02 -- H1 Near-Multiple-Zero Mechanism"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
dependencies:
  - start.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT01_H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
  - primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
tags: [breakthrough-wave-2, ec-ndc, h1, near-multiple-zeros, reciprocal-derivative, minimum-modulus]
---

# Agent 02 H1 Near-Multiple-Zero Budget

status: `RIGOROUS_REDUCTION`

## Verdict

Near-collisions are a real mechanism for small `L'(rho)`, but they do not by
themselves give the H1 reciprocal budget.

For analytic rank

```text
r = ord_(s=1) L(E,s),
```

the rank-one absolute target remains

```text
R_E,1(T)
 = sum_(T<|gamma|<=2T, simple)
     |L'(E,1+i gamma)|^(-1)
 = o(T^2).
```

The near-multiple route is usable only as the following sharper theorem input:

```text
For all simple zeros outside B_T, each rho has a zero-free local circle and
a boundary minimum-modulus certificate giving
  |L'(E,rho)| >= h(T) log T / T,     h(T)->infinity,
and the bad set satisfies
  sum_(rho in B_T) |L'(E,rho)|^(-1) = o(T^2).
```

Known local zero statistics, zero spacing, many-simple-zero theorems, and the
currently sourced minimum-modulus height theorems do not prove this. They give
counts or selected contour heights, not reciprocal derivative tails at zeros.

Thus:

```text
near-collision + local min-modulus + bad reciprocal budget => usable reduction;
spacing/local statistics alone => NO_GO;
known sourced theorems as currently packeted => not enough for R_E,1(T)=o(T^2).
```

## Mechanism Map

Let `rho=1+i gamma` be a simple zero and set

```text
X_rho = |L'(E,rho)|^(-1).
```

### A close neighbor can make `L'(rho)` small

Suppose `L` is analytic in `|s-rho|<=R`, and another zero
`rho'` satisfies

```text
delta = |rho-rho'| <= R/2.
```

Write

```text
L(E,s)=(s-rho)(s-rho')h(s).
```

If

```text
sup_(|s-rho|=R) |L(E,s)| <= M_R,
```

then on the boundary `|h(s)| <= 2 M_R/R^2`, so

```text
|L'(E,rho)| = |rho-rho'| |h(rho)|
            <= 2 delta M_R/R^2.
```

Thus a sufficiently close neighbor can force a small derivative, relative to
the available upper bound for the zero-free factor.

This is only a danger mechanism. It is not a lower-bound mechanism.

### Separation alone does not prevent small `L'(rho)`

If the disk `0<|s-rho|<=r_T` is zero-free, write

```text
L(E,s)=(s-rho)g_rho(s),     g_rho(rho)=L'(E,rho).
```

Zero separation gives a legal disk. It does not lower-bound `g_rho(rho)`.
For that, one needs a boundary lower bound

```text
min_(|s-rho|=r_T) |L(E,s)| >= m_T.
```

Then the minimum principle applied to the nonvanishing holomorphic function
`g_rho` gives

```text
|L'(E,rho)| >= m_T/r_T,
X_rho <= r_T/m_T.
```

With

```text
r_T=T^(-kappa)(log T)^(-b),
m_T=T^(-mu)(log T)^(-B),
```

the certificate gives

```text
|L'(E,rho)| >= T^(-(mu-kappa))(log T)^(b-B).
```

To imply the rank-one pointwise sufficient bound

```text
|L'(E,rho)| >= h(T) log T / T,     h(T)->infinity,
```

it is enough and essentially sharp at this scale that

```text
mu-kappa < 1,
```

or that

```text
mu-kappa = 1 and b-B>1.
```

### True multiple zeros are separate

The sum `R_E,1(T)` is over simple zeros only. A true offcentral multiple zero
has `L'(rho)=0` and contributes Laurent polynomial terms to the H1 contour
expansion. By the Wave 1 Laurent packet, an uncancelled critical-line zero of
multiplicity `m` and kernel zero order `nu_rho` has generic degree

```text
m-1-nu_rho.
```

For positive analytic rank `r`, every unretained effective degree must be
`< r`, and lower-degree coefficient aggregates still need summability or a
proved PV/average mode. The near-collision budget below does not absorb actual
multiple-zero Laurent terms.

## Bad-Set Reciprocal Budget Criteria

Let `G_T` be the simple zeros in `T<|gamma|<=2T` with a valid local
zero-free-circle/minimum-modulus certificate, and let

```text
B_T = {simple shell zeros not certified good}.
```

Assume the local zero count

```text
N_E(T,2T) <<_E T log T.
```

### Criterion 1: direct bad reciprocal budget

If every `rho in G_T` satisfies

```text
X_rho <= T/(h(T)log T),     h(T)->infinity,
```

then

```text
sum_(rho in G_T) X_rho
 << T log T * T/(h(T)log T)
 = o(T^2).
```

Therefore

```text
R_E,1(T)=o(T^2)
```

follows exactly when

```text
sum_(rho in B_T) X_rho=o(T^2).
```

This is the clean near-multiple budget condition.

### Criterion 2: count plus cap

A checkable sufficient version is

```text
#B_T <= B(T),
X_rho <= C(T) for rho in B_T,
B(T) C(T)=o(T^2).
```

Examples:

```text
C(T)=T^A polylog(T), A<1:
  zero count alone gives B(T)<=T log T, so the bad part is o(T^2).

C(T)=T L(T), with L(T) a log-power or other slow factor:
  need #B_T=o(T/L(T)).

C(T)=T^A, A>1:
  need #B_T=o(T^(2-A)).
```

Cardinality sparsity without a cap is invalid. One exceptionally tiny
`L'(rho)` can destroy the shell budget.

### Criterion 3: layer-cake tail

For

```text
F_B(T;V)=#{rho in B_T: X_rho>V},
```

the bad budget is equivalent to

```text
int_1^infty F_B(T;V) dV=o(T^2),
```

since the range `0<V<=1` contributes at most `O(T log T)`.

A sufficient power tail is

```text
F_B(T;V) <= C T^2 Phi(T)^(-1) V^(-1-alpha),
alpha>0, Phi(T)->infinity.
```

A borderline `V^(-1)` tail needs a cap and logarithmic surplus. Without a cap,
the layer-cake integral diverges.

### Criterion 4: close-pair count plus reciprocal cap

Let

```text
P_T(delta)
 = #{rho: T<|Im rho|<=2T, rho simple,
      some rho' != rho has |rho-rho'|<=delta}.
```

If the bad set is defined by a near-collision threshold `delta_T`, then pair
statistics only give

```text
#B_T <= P_T(delta_T).
```

They prove the H1 budget only after a reciprocal cap:

```text
P_T(delta_T) C(T)=o(T^2).
```

No known spacing or pair-correlation statement in the packets supplies the cap
`C(T)`. Pair statistics count near clusters; they do not bound the zero-free
factor `g_rho(rho)`.

### Criterion 5: shell moment substitute

The stronger square reciprocal shell hypothesis

```text
J_E,2(T)
 = sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-2)
 <= C_E T^(3-delta)
```

implies the rank-one `R_E,1` target by Cauchy-Schwarz:

```text
R_E,1(T)
 <= N_E(T,2T)^(1/2) J_E,2(T)^(1/2)
 << T^(2-delta/2)(log T)^(1/2)
 = o(T^2).
```

This is not proved by known sources. It is a named stronger input.

## Known Theorem / Source Status

No new external source was fetched in this packet. The source facts below are
used only through local packets that already record the project protocol:
`curl + pdftotext`, SHA256, short quote, and page/equation anchors.

### What the sources support but do not close

1. EC zero counting.

   Source packet: `H1_SOURCE_AUDIT.md` / `SHELL_MOMENT_SOURCE_AUDIT.md`.
   Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1 quote anchor:
   "number of zeros"; Corollary 3.2 quote anchor: "converges".

   Use here:

   ```text
   N_E(T,2T) <<_E T log T,
   sum 1/|rho|^2 < infinity.
   ```

   Limit: pure zero counts and pure ordinate summability do not control
   `1/L'(rho)`.

2. Some or many simple zeros for GL2/newform L-functions.

   Source packet: `H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`.
   Booker PDF p. 1, Theorem 1 quote anchor: "has infinitely many simple
   zeros". de Faveri PDF p. 2, Theorem 1.1 quote anchor: "Power bound for
   arbitrary level".

   Use here: simplicity occurs often.

   Limit: not all zeros are simple; no bounded multiplicity theorem; no lower
   bounds for `|L'(rho)|`.

3. Li-Zaharescu selected minimum-modulus heights.

   Source packet: `H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md`.
   Li-Zaharescu PDF p. 4, Proposition 3.1: every large unit interval has a
   selected height with a strip lower bound of size
   `exp(-A log T/loglog T)` in the normalized strip.

   Use here: closes the horizontal contour-height blocker after EC
   normalization and reflection, for the fixed contour tail.

   Limit: this gives selected horizontal heights, not local boundary
   minimum-modulus circles around each zero. It does not control
   `|L'(rho)|` or the bad reciprocal budget.

### Adjacent material and model material

4. Li-Zaharescu reciprocal-derivative/mollifier machinery.

   Source packets: `SHELL_MOMENT_SOURCE_AUDIT.md`,
   `H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`,
   `H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md`.
   Li-Zaharescu PDF p. 2, Theorem 1.1 quote anchor: "lower bound for the
   negative moment"; PDF p. 4, equations (9)-(11) include mollified sums with
   `L'(rho)^(-1)`; PDF p. 7, Theorem 4.1 uses Dirichlet-polynomial weights.

   Use here: possible proof template.

   Limit: lower bounds and mollified Dirichlet-polynomial weights do not give
   upper control for

   ```text
   sum W_hat(i gamma) exp(i gamma u)/L'(E,1+i gamma)
   ```

   or for `R_E,1(T)`.

5. Titchmarsh zeta minimum-modulus theorem.

   Source packet: `RECIPROCAL_STRIP_BOUNDS.md`.
   Titchmarsh, zeta text PDF p. 114, Theorem 9.7 quote anchor:
   "There is a constant A".

   Use here: GL1/zeta model for selected-height minimum modulus.

   Limit: not an EC/GL2 local derivative theorem and not a circle
   minimum-modulus theorem around each zero.

6. Zeta negative derivative moments.

   Source packet: `SHELL_MOMENT_SOURCE_AUDIT.md`.
   Bui-Florea-Milinovich PDF p. 1 quote anchor: "conditional upper bounds";
   PDF p. 2 quote anchor: "No upper bounds are known"; PDF p. 3 quote anchor:
   "simplicity of zeros is not enough".

   Use here: difficulty warning.

   Limit: zeta only; conditional/subfamily orientation; no EC/GL2 theorem.

7. RMT/local statistics heuristics.

   Source packet: `SHELL_MOMENT_RMT_HEURISTIC.md`.

   Use here: model predicts the target is plausible and much weaker than the
   expected `J_E,2(T) ~ T polylog(T)`.

   Limit: heuristic only. It cannot be used as a theorem input.

## Decision Table

| Route | Decision | Reason |
|---|---:|---|
| Near neighbor forces small derivative | `RIGOROUS_REDUCTION` | True with an upper bound for the remaining local factor; identifies the bad mechanism. |
| Zero spacing / pair count controls `R_E,1` | `NO_GO` | Counts near pairs only; no cap on `X_rho`. |
| Zero-free circle plus boundary min modulus | `RIGOROUS_REDUCTION` | Gives `|L'(rho)|>=m_T/r_T`; usable if `m_T/r_T >= h(T)logT/T`. |
| Selected contour heights from LZ | `NO_GO` | Controls horizontal contour size, not local derivative values at zeros. |
| EC zero count plus simplicity | `NO_GO` | Does not lower-bound `L'(rho)`. |
| Many/power-many simple zeros | `NO_GO` | Leaves exceptional/multiple zeros and gives no reciprocal cap. |
| Bad set with `sum_B X_rho=o(T^2)` | `RIGOROUS_REDUCTION` | Exactly sufficient after good-zero certification. |
| Shell moment `J_E,2(T)<=T^(3-delta)` | `RIGOROUS_REDUCTION` | Stronger sufficient input; currently not source-closed. |
| Actual multiple-zero absorption by `R_E,1` | `NO_GO` | Laurent polynomial terms are outside the simple-zero reciprocal sum. |

## Sharper Theorem Input To Carry Forward

The useful near-multiple theorem input is:

```text
H1-local-minmod-budget(E):
  There are h(T)->infinity and bad sets B_T of simple shell zeros such that:

  (1) For every simple rho=1+i gamma with T<|gamma|<=2T and rho notin B_T,
      there is a radius r_rho with the punctured disk zero-free and

        min_(|s-rho|=r_rho) |L(E,s)|
          >= r_rho h(T) log T / T.

  (2) The bad reciprocal budget satisfies

        sum_(rho in B_T) |L'(E,rho)|^(-1) = o(T^2).

  (3) Actual multiple zeros are absent, kernel-killed, have effective degree
      < r with coefficient control, or are retained/averaged in the H1
      Laurent theorem mode.
```

Then, for analytic rank one,

```text
R_E,1(T)=o(T^2).
```

For finite-box H1 use, the weaker dyadic Cesaro variant from Wave 1 is also
valid:

```text
sum_(j<=N) 2^(-2j) R_E,1(2^j)=o(N),
N ~= log T_box(u).
```

The near-multiple version replaces `R_E,1(2^j)` by the same good/bad split on
each shell.

## Blockers

1. No fixed-curve EC/GL2 theorem in the read packets gives local
   minimum-modulus circles around every nonbad zero with
   `m_T/r_T >= h(T)logT/T`.

2. No source-checked fixed-curve theorem gives the bad reciprocal tail

   ```text
   int_1^infty F_B(T;V)dV=o(T^2).
   ```

3. Pair-correlation or spacing information, even if sourced later, must be
   coupled to a reciprocal cap. Count-only exceptional sets are not enough.

4. Li-Zaharescu selected heights solve a contour-tail issue, not the local
   derivative budget.

5. True offcentral multiple zeros remain under the Laurent package, not under
   `R_E,1`.

6. H2 branch damping was not used and cannot be imported into H1 reciprocal
   pole residues.

## Verification Notes

Read targeted context only:

```text
start.md
token-economy.yaml
L0_rules.md
L1_index.md
primes-equispaced/L0_rules.md
primes-equispaced/L1_index.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT01_H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/TC_HEIGHT_EXPONENT_AUDIT.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_SOURCE_AUDIT.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_ANALYTIC_ATTEMPT.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/SHELL_MOMENT_RMT_HEURISTIC.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_SHELL_MOMENT_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_FIXED_WEIGHT_PV_NOGO_CONDITIONAL_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/RECIPROCAL_STRIP_BOUNDS.md
primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_LZ_DYADIC_UPPER_BOUND.md
primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_FIXED_WEIGHT_MOLLIFIER_TRANSFER.md
primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_MULTIPLE_ZERO_EXCEPTIONAL_THEOREM.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_SOURCE_AUDIT.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md
```

Checks:

```text
./te doctor returned ok:true.
Status enum is one of the Wave 2 allowed values.
Analytic rank only.
No H2 damping imported.
No Koyama correspondence or email draft touched.
No broad archive loaded.
No external source claim made outside the existing source-packet protocol.
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT02_H1_NEAR_MULTIPLE_ZERO_BUDGET_2026-05-11.md
```
