---
schema_version: 1
title: "H2/Sym2 proof attempt 2"
date: 2026-05-11
type: proof-attempt
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.77
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H2_SYM2_SOURCE_CLOSURE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
  - handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
  - handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
  - handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
tags: [ec-ndc, h2, sym2, s1, endpoint-smoothing, proof-attempt]
---

# H2/Sym2 Proof Attempt 2

Status: `RIGOROUS_REDUCTION`

Confidence: `0.77`

Dependencies: exact Agent-3 local factors; analytic rank
`r=ord_{s=1}L(E,s)`; fixed endpoint-smoothed kernel `W`; the required S1,
Sym2, zero-sum, and source packets listed in front matter.

## Do Not Promote Unless

- Exact Agent-3 factors stay fixed: good `1-a_p/p+1/p`, bad `1-a_p/p`.
- `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3,W`, and `B_bad,E` all appear.
- `r=ord_{s=1}L(E,s)` is analytic rank; no algebraic-rank substitution.
- The S1 branch theorem is proved for the exact endpoint-smoothed kernel.
- The Sym2 theorem is proved for `chi_sym2(p)=a_p^2/p-1` over good primes.
- Any `Re(rho)>1` S1 or Sym2 branch is either excluded or retained explicitly.
- `kappa_sym=0` is not inserted without source/proof for this exact object.
- H1 is kept separate; no reciprocal-pole claim is imported here.
- New external facts get `curl + pdftotext + SHA + page/eq + short quote`.

## Verdict

The H2/Sym2 side still does not close unconditionally. The second attempt gives
a precise branch package which would close pointwise H2, and it isolates the
remaining blockers:

```text
B1  endpoint-smoothed S1 branch continuation and contour tails;
B2  no unpaired S1 branch/pole with Re(rho)>1;
B3  exact good-prime Sym2 finite part and zero/pole summability;
B4  source/proof for kappa_sym, or convention-safe retention of it.
```

The local algebra is closed. The analytic theorem is a conditional reduction.

## Exact H2 Identity

For good primes set

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K),
```

with

```text
S_1,W    = sum_{p good} W(p/K) a_p/p,
S_sym,W = sum_{p good} W(p/K) chi_sym2(p)/p,
M_good,W= sum_{p good} W(p/K)/p,
B_bad   = -sum_{p bad} W(p/K) log(1-a_p/p).
```

The good-prime Taylor identity is

```text
-log(1-a_p/p+1/p)
 = a_p/p + (1/2)chi_sym2(p)/p - 1/(2p) + R_p,
```

and `sum_{p good} R_p` converges absolutely by Hasse plus the cubic remainder.

## Conditional Branch Package

Let

```text
A_E(z) = sum_{p good} a_p p^(-1-z),
D_sym(s) = sum_{p good} chi_sym2(p) p^(-s).
```

Assume a fixed `eta>0` and the Agent-3 endpoint kernel `W` with
`W_hat(z)=1/z+O(1)` at `0` and vertical decay `O((1+|t|)^(-2))` for
`W_hat,W_hat'` in the shifted strip.

Hypothesis `S1-branch`: Mellin inversion for `S_1,W` may be shifted to
`Re z=-eta`; in the cut strip `A_E(z)` has only logarithmic branches, no
offcentral poles on `Re z>=0`, and shifted-line/horizontal tails are
`O(K^-eta)+O((log K)^-2)`.

Hypothesis `S1-zero`: for branch coefficients `c_a`,

```text
sum_{a != 0, Re a = 0} |c_a W_hat(a)| < infinity
```

with the matching derivative bound. `SOURCE_PACKET.md` supports this only for
pure `L(E,s)` zero multiplicities using Sheth zero counting plus smoothstep
Mellin decay; it does not prove `S1-branch`.

Hypothesis `Sym2-branch`: the exact good-prime object

```text
L_sym,E^good(s)
 = product_{p good}
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1)
```

with `u_p v_p=1`, `u_p+v_p=lambda_p`, satisfies

```text
D_sym(s) = log L_sym,E^good(s) - H_sym(s),
H_sym(1) finite,
kappa_sym = ord_{s=1} L_sym,E^good(s),
```

and the same shifted logarithmic-branch plus weighted zero/pole summability
package. Ramified/global Sym2 factors may be used only after finite local
corrections return to this good-prime normalization.

## Candidate Conclusion Under The Package

Under `S1-branch`, `S1-zero`, and `Sym2-branch`,

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1(log K)/log K
   + o(1),
```

where a noncolliding zero `rho=1+i gamma` of `L(E,s)` contributes

```text
-m_rho K^(i gamma) W_hat(i gamma)/log K.
```

Also

```text
S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E,W
   + Z_sym(log K)/log K
   + o(1).
```

Together with weighted good-prime Mertens,

```text
M_good,W(K) = log log K + C_M,E,W + o(1),
```

this gives

```text
log P_E,W(K)
 = -r log log K + B_H2(E,W)
   + (Z_1(log K) + Z_sym(log K)/2)/log K
   + o(1).
```

If both branch sums are bounded and no `Re(rho)>1` term survives, then

```text
log P_E,W(K) = -r log log K + B_H2(E,W) + o(1).
```

The coefficient check is exact:

```text
(1/2 + kappa_sym/2 - r) + (1/2)(-kappa_sym) - 1/2 = -r.
```

## Sharp Obstruction

The route cannot prove a pointwise finite part from current inputs alone. If
`A_E(z)` has an offcentral logarithmic branch at `a=rho-1` with `Re a>0`, then
`S_1,W` contains

```text
c_a K^a W_hat(a)/log K,
```

which is not `o(1)`. If there is an offcentral pole at `a` with `Re a>=0`, the
term is even larger:

```text
d_a K^a W_hat(a).
```

Thus endpoint smoothing handles logarithmic branches on `Re a=0`; it does not
replace a no-right-branch/no-pole theorem.

## Source Hooks

No new external theorem is used as a fact here. Existing verified hooks are
only those in `SOURCE_PACKET.md`:

- Sheth, arXiv:2312.05236, PDF p. 13, Theorem 3.1/Corollary 3.2: EC zero
  counting and reciprocal-square pure multiplicity summability.
- Friedlander-Iwaniec chapter PDF, PDF p. 17, Theorem 1.2: ordinary
  prime-Mertens; weighted transfer remains in-repo.
- Iwaniec-Luo-Sarnak, arXiv:math/9901141, PDF p. 11 equations (13)-(15):
  adjacent Sym2/GL(3) setup only.
- Hoffstein-Lockhart, Annals 140 (1994), PDF p. 3 equations (0.6)-(0.8):
  adjacent adjoint-square context only.

Unverified but natural next source targets:

```text
Gelbart-Jacquet     Sym2 lift/entireness for GL(2)->GL(3).
Jacquet-Shalika     nonvanishing on Re(s)=1 for GL(n) L-functions.
GL(3) zero count    N_sym(T)=O(T log T) with multiplicity.
Adjoint L(1)        finite nonzero value at s=1 in exact normalization.
```

These are source hooks, not promoted facts, until the mandatory fetch/extract
protocol is run.

## Gap Map

Closed:

```text
Agent-3 local decomposition.
Bad-prime treatment as finite constant.
R_ge3 absolute convergence.
S1 zero-sum boundedness once branch continuation and zero counting are given.
kappa_sym cancellation in the H2 coefficient.
```

Open:

```text
Exact endpoint-smoothed branch theorem for A_E(z).
Proof that no S1 pole/right-branch survives in Re z>=0.
Exact Sym2 finite-part theorem for good primes.
Sym2 zero/pole summability in the same shifted strip.
Source-verified kappa_sym=0, if a constant-scale S_sym theorem is desired.
```

H1 remains outside this file. H2 logarithmic-branch damping gives no control of
H1 reciprocal-pole residues.

## Changed Path

```text
handoff-2026-05-11-h1-breakthrough-proof-wave/H2_SYM2_PROOF_ATTEMPT_2.md
```
