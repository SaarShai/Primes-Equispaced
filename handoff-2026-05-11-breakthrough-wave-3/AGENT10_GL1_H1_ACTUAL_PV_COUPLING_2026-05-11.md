---
schema_version: 1
title: "Agent 10 - GL1/H1 Actual PV Coupling"
date: 2026-05-11
agent: "Breakthrough Wave 3 Agent 10"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.88
sources:
  - start.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-3-plan.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BREAKTHROUGH_WAVE_2_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT03_H1_ACTUAL_COEFFICIENT_MOVING_PV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT07_GL1_MOVING_OFFTARGET_PV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT06_ACTUAL_COEFFICIENT_H1_PV_THEOREM_2026-05-11.md
tags: [breakthrough-wave-3, agent10, gl1, h1, actual-coefficients, moving-pv]
---

# Agent 10 - GL1/H1 Actual PV Coupling

status: `RIGOROUS_REDUCTION`

## Verdict

A single abstract deterministic transfer lemma covers the formal moving-PV
part of both problems.

It does not give a single arithmetic hypothesis that closes both problems.
The reusable theorem is a wrapper:

```text
actual shell PV + same-height contour tails + Laurent boundary
  => pointwise leading term.
```

The arithmetic shell PV hypothesis must remain problem-specific:

```text
H1:
  b_gamma = W_hat(i gamma) / L'(E,1+i gamma),
  scale Phi(U)=U^r.

GL1 sharp off-target:
  b_lambda = 1 / ((lambda-rho)L'(lambda,chi))
           = 1 / (i alpha_lambda L'(lambda,chi))
  in the critical-line oscillatory mode,
  scale Phi(U)=U.
```

Thus the correct coupling is:

```text
one abstract theorem;
two genuinely separate coefficient hypotheses.
```

## Abstract Transfer Lemma

`AbstractActualMovingShellPV(Omega,b,H,Phi)`:

Fix dyadic windows `u in [U,2U]`, a legal moving height `H(U)`, and a target
scale `Phi(U) -> infinity`. Let `Omega` be the multiset of nonzero real
frequencies after all same-frequency residues are aggregated. Let `b_omega`
be the actual aggregated coefficient attached to `omega`.

For shells

```text
Omega_j = {omega in Omega: 2^j < |omega| <= 2^(j+1)}
```

define

```text
B_j(U)
  = sup_(u in [U,2U])
      | sum_(omega in Omega_j) b_omega e^(i omega u) |.
```

Assume:

```text
1. moving shell PV:
   sum_(2^j <= H(2U)) B_j(U) = o(Phi(U));

2. lower finite block:
   every frequency not covered by the positive dyadic shells contributes
   o(Phi(U)) on [U,2U];

3. same-height contour identity:
   F(u) = M(u) + Z_(H(U))(u) + L_(H(U))(u) + I_(H(U))(u),

   Z_(H(U))(u)
     = sum_(0 < |omega| <= H(U)) b_omega e^(i omega u);

4. Laurent boundary:
   unretained multiple-zero or higher-order residue terms in L_(H(U)) are
   o(Phi(U)), or are explicitly retained in M(u);

5. contour/truncation tails:
   sup_(u in [U,2U]) |I_(H(U))(u)| = o(Phi(U)).
```

Then

```text
F(u) = M(u) + o(Phi(U))
```

uniformly for `u in [U,2U]`.

Proof:

For `u in [U,2U]`, partition `Z_(H(U))` into the finite lower block plus
dyadic shells with `2^j <= H(U) <= H(2U)`. The triangle inequality gives

```text
sup_(u in [U,2U]) |Z_(H(U))(u)|
  <= lower_block(U) + sum_(2^j <= H(2U)) B_j(U)
  = o(Phi(U)).
```

Insert this in the finite-height identity and use assumptions 4 and 5.
No external theorem is used.

## H1 Specialization

Use analytic rank only:

```text
r = ord_(s=1) L(E,s).
```

The H1 data are:

```text
omega = gamma,
b_gamma(E,W) = W_hat(i gamma) / L'(E,1+i gamma),
Phi(U) = U^r.
```

The abstract shell condition becomes exactly the Wave 2/Wave 3 H1 target:

```text
sum_(2^j <= H(2U))
  sup_(u in [U,2U])
    | sum_(2^j < |gamma| <= 2^(j+1))
        W_hat(i gamma)e^(i gamma u) / L'(E,1+i gamma) |
  = o(U^r).
```

For analytic rank one this is `o(U)`.

The absolute sufficient condition remains H1-specific. If
`|W_hat(i gamma)| <= C_W |gamma|^(-q)` on shells, then it is enough to prove

```text
sum_(2^j <= H(2U)) 2^(-qj) R_E,1(2^j) = o(U^r),

R_E,1(T)
  = sum_(T < |gamma| <= 2T, simple)
      |L'(E,1+i gamma)|^(-1).
```

For the rank-one `q=2` packets, the known clean target is still

```text
R_E,1(T) = o(T^2).
```

This is not a PV theorem. It is absolute domination of the same abstract
shell wrapper.

## GL1 Specialization

For the sharp GL1 off-target problem, fix a simple noncentral target zero

```text
rho = 1/2 + i t
```

and write, in the oscillatory critical-line mode,

```text
lambda = 1/2 + i gamma,
alpha_lambda = gamma - t.
```

After removing the target residue, the simple off-target coefficients are

```text
omega = alpha_lambda,
b_lambda(chi,rho)
  = 1 / (i alpha_lambda L'(lambda,chi)).
```

The abstract scale is

```text
Phi(U) = U,
u = log K.
```

The GL1 shell condition is:

```text
sum_(2^j <= T(e^(2U)))
  sup_(u in [U,2U])
    | sum_(2^j < |alpha_lambda| <= 2^(j+1))
        e^(i alpha_lambda u) /
        (i alpha_lambda L'(lambda,chi)) |
  = o(U).
```

Together with the same-height rectangle/truncation estimates and the
multiple-zero boundary, this yields the conditional sharp leading term from
Wave 2 Agent 07:

```text
c_K(chi,rho)
  = log K/L'(rho,chi) + o(log K)
```

with the constant term from the target residue treated according to the
declared normalization.

The absolute sufficient condition is not the H1 one. It is target-shifted:

```text
sum_(2^j <= T(e^(2U))) 2^(-j) R_chi,rho(2^j) = o(U),

R_chi,rho(T)
  = sum_(T < |alpha_lambda| <= 2T)
      |L'(lambda,chi)|^(-1),
```

with the target removed and small nonzero `alpha_lambda` terms handled in the
finite lower block.

## Why The Arithmetic Hypotheses Do Not Merge

The abstract theorem hides no arithmetic. It only says that if the actual
dyadic shell sums are small, then the residue aggregate is small. The
following differences force separate hypotheses:

1. H1 coefficients contain the chosen Mellin kernel:

```text
W_hat(i gamma) / L'(E,1+i gamma).
```

Changing `W` changes decay, filtering, and even coefficient death.

2. GL1 sharp coefficients contain the target-dependent singular factor:

```text
1 / (alpha_lambda L'(lambda,chi)).
```

This factor is tied to the chosen target `rho`; it is not a fixed global
weight on the zero set.

3. The absolute routes have different moment weights:

```text
H1:   2^(-qj) R_E,1(2^j)
GL1:  2^(-j) R_chi,rho(2^j)
```

so a single reciprocal-derivative moment statement cannot be cited for both
without adding the missing weight and target data.

4. Multiple-zero boundaries differ. In H1, higher-order offcentral Laurent
terms must have effective degree `< r`, be killed, be retained, or be
averaged. In GL1 sharp rank-one scale, an off-target multiplicity `m >= 2`
can produce `log K`-scale or larger oscillatory Laurent terms and must be
excluded or separately retained.

5. Smoothing/filtering changes the theorem. It can create a valid smoothed
GL1 or filtered H1 theorem, but it is not the original sharp GL1 cutoff and
not the fixed-weight H1 pointwise theorem unless the same kernel is declared
and rechecked through the whole contour package.

## No-Go Boundaries

The shared abstract lemma does not imply either arithmetic PV input from:

```text
zero spacing;
non-lattice ordinates;
conjugation symmetry;
square-summable coefficients;
Besicovitch/profile convergence;
log-Cesaro cancellation;
GUE or phase-randomness heuristics;
or H2 branch damping.
```

The harmonic model recorded in the GL1 packet remains the warning case:

```text
sum_(1 <= n <= T) cos(nu)/n
```

has spacing, symmetry, and square-summable shell coefficients, but has
`log T`-scale resonant values. Therefore any proof using only those abstract
features would prove a false moving-sup statement.

The H1 actual coefficients may have special EC structure, and the GL1
Dirichlet coefficients may have special target-zero structure. The read
packets do not contain a theorem converting either structure into the needed
moving shell bound.

## Recommended Naming

Use one wrapper name:

```text
AbstractActualMovingShellPV(Omega,b,H,Phi)
```

Use separate arithmetic inputs:

```text
H1-ActualDyadicShellPV(E,W,r,H)
GL1-ActualMovingShellPV(chi,rho,T)
```

Do not replace either arithmetic input by the wrapper name. The wrapper is the
deterministic final step after the actual coefficient theorem has been proved
or assumed.

## Protocol Check

External theorem claims: none. No `curl + pdftotext` source packet was needed.

Analytic rank only. No BSD or algebraic-rank substitution.

H2 branch damping was not used as H1 reciprocal-pole damping.

No Koyama correspondence or email drafts were used or edited.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT10_GL1_H1_ACTUAL_PV_COUPLING_2026-05-11.md
```
