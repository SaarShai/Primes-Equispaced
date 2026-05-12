---
schema_version: 1
title: "GL1 shifted Perron closure path"
date: 2026-05-11
agent: "GL1-Perron"
type: theorem-path
tier: claim-safe
status: "PERRON_REMAINDER_DEFER"
scope: "GL(1) AK/NDC sharp-cutoff Perron obstruction"
tags: [koyama, gl1, perron, ak, mertens, b-infty, residue-obstruction]
---

# GL1 shifted Perron closure path

## Verdict

Do not claim

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K)
```

as a theorem from the current dependency package.

Promote only:

1. the Aoki-Koyama Euler-product constant, under AK DRH/EDRH:

```text
E_K(chi,rho) log K -> L'(rho,chi)/e^gamma;
```

2. the local Perron residue at the target zero:

```text
Res_{w=0} K^w/(w L(rho+w,chi))
  = log K/L'(rho,chi) - L''(rho,chi)/(2 L'(rho,chi)^2);
```

3. the corrected `B_infty` identity with `psi`, `BPC1`, `BPC2`, and
   `T_{>=3}` included.

The corrected NDC limit

```text
D_K(chi,rho) := c_K(chi,rho) E_K(chi,rho) -> e^(-gamma)
```

is a conditional corollary only: AK plus the still-missing shifted Perron
nonlocal remainder theorem.

## Sources inspected

- `handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md`
- `handoff-2026-05-09-followup/Koyama_AK_constant_proof.md`
- `handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md`
- `handoff-2026-05-09-followup/Koyama_B_infty_proof.md`
- `handoff-2026-05-09-followup/Koyama_NDC_constant_correction.md`
- `handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md`
- `handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md`
- `handoff-2026-05-11-gpt55-wave/AGENT1_GL1_SHIFTED_PERRON.md`
- `handoff-2026-05-09-followup/MERTENS_LB_disproof_INDEPENDENT_VERIFICATION.md`
- `handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md`
- `correspondence/KOYAMA.md`
- `projects/farey-research/koyama-correspondence.md`

## Notation

Let `chi` be primitive non-principal. Let

```text
rho = 1/2 + i t
```

be a simple noncentral zero of `L(s,chi)`. Define

```text
E_K(chi,rho) = prod_{p<=K} (1 - chi(p) p^(-rho))^(-1),
c_K(chi,rho) = sum_{n<=K} mu(n) chi(n) n^(-rho),
D_K(chi,rho) = c_K(chi,rho) E_K(chi,rho).
```

Use the shifted Perron kernel

```text
F_K(w) = K^w/(w L(rho+w,chi)).
```

## Recommended statements

### Theorem A: AK constant, conditional

Assume the Aoki-Koyama DRH/EDRH hypotheses for primitive non-principal
Dirichlet `L(s,chi)`. If `rho != 1/2` is a simple zero on `Re s=1/2`, then

```text
E_K(chi,rho) log K -> L'(rho,chi)/e^gamma.
```

This is the simple-zero, noncentral specialization of Aoki-Koyama 2023,
equation (1.4), p.235. It is not `L'(rho,chi)/zeta(2)`.

### Lemma B: local target residue

If `rho` is a simple zero, then

```text
1/L(rho+w,chi)
  = 1/(L'(rho,chi) w)
    - L''(rho,chi)/(2 L'(rho,chi)^2)
    + O(w),
```

and therefore

```text
Res_{w=0} F_K(w)
  = log K/L'(rho,chi)
    - L''(rho,chi)/(2 L'(rho,chi)^2).
```

This is local algebra only. It does not imply the global asymptotic for
`c_K(chi,rho)`.

### Lemma C: off-target residue formula

Let `lambda != rho` be a nontrivial zero of `L(s,chi)` of multiplicity `m`.
Set

```text
w_lambda = lambda - rho.
```

Write

```text
L(lambda+z,chi) = a_m z^m + a_{m+1} z^(m+1) + ...,
a_m = L^(m)(lambda,chi)/m! != 0.
```

Then

```text
Res_{w=w_lambda} F_K(w)
 = K^(w_lambda) sum_{j=0}^{m-1} A_{lambda,j} (log K)^j/j!,
```

where

```text
A_{lambda,j}
 = [z^(m-1-j)] ( z^m/(L(lambda+z,chi) (w_lambda+z)) ).
```

In particular the top term is

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m.
```

For `m=1`, this reduces to

```text
K^(lambda-rho)/((lambda-rho)L'(lambda,chi)).
```

### Lemma D: multiple-zero obstruction

Under DRH, `Re(lambda-rho)=0`. Hence an off-target zero of multiplicity
`m>=2` contributes an unsuppressed oscillatory polynomial in `log K` of
degree `m-1`.

Consequences:

```text
m=2: another log K-scale term.
m>2: a term larger than the target log K scale.
```

Thus target-zero simplicity plus DRH/EDRH is not enough. A leading theorem
must either assume/prove all crossed off-target zeros are simple, or include
and control the full higher-order off-target aggregate.

### Theorem E: exact missing closure theorem

This is the theorem needed to promote Perron-leading.

Let `A>1`, `B>0`, and let

```text
T_K in [K/(log K)^B, 2K/(log K)^B]
```

be zero-avoiding heights for the rectangle with right edge
`Re w = 1/2 + 1/log K` and left edge `Re w = -A`. Assume the truncated Perron
identity for `F_K` with the chosen endpoint convention. Then, after extracting
the `w=0` residue,

```text
R_K :=
  c_K(chi,rho)
  - Res_{w=0} F_K(w)
```

satisfies

```text
R_K = o(log K).
```

Equivalently, the following combined remainder is `o(log K)`:

```text
1. all off-target nontrivial-zero residues, including higher-order residues;
2. all trivial-zero residues;
3. the shifted left vertical integral;
4. both horizontal integrals;
5. Perron truncation and endpoint errors.
```

A cleaner sufficient package is:

```text
all crossed off-target nontrivial zeros are simple,
Z_simple(K,T_K)
  := sum_{lambda != rho, |Im(lambda-rho)|<=T_K}
       K^(lambda-rho)/((lambda-rho)L'(lambda,chi))
   = o(log K),
and the rectangle/truncation terms are o(log K).
```

For the subleading global theorem, replace every `o(log K)` above by `o(1)`.

### Corollary F: conditional corrected NDC

Assume Theorem A and Theorem E. Then

```text
D_K(chi,rho) -> e^(-gamma).
```

Proof:

```text
c_K(chi,rho) = log K/L'(rho,chi) + o(log K),
E_K(chi,rho) = L'(rho,chi)/(e^gamma log K) + o(1/log K).
```

Multiplication gives `e^(-gamma)+o(1)`.

## Proof skeleton for Theorem E

1. Apply truncated Perron to

```text
sum_{n<=K} mu(n) chi(n)n^(-rho)
```

using `F_K(w)`.

2. Shift the contour from `Re w=1/2+1/log K` to `Re w=-A` through
zero-avoiding heights `T_K`.

3. Record the finite-box identity:

```text
c_K = Res_{w=0} F_K
      + Z_off(K,T_K)
      + Z_triv(K,T_K)
      + V_left(K,T_K,A)
      + H_top/bottom(K,T_K,A)
      + E_Perron(K,T_K).
```

4. Use Lemma B for the target residue.

5. Use Lemma C for all off-target residues. If multiplicities are not ruled
out, keep the full polynomial residue expression.

6. Prove:

```text
Z_off(K,T_K) = o(log K),
Z_triv(K,T_K) = o(log K),
V_left + H_top + H_bottom = o(log K),
E_Perron = o(log K).
```

The first line is the hard input. The others are expected contour/truncation
work but still need a source-closed reciprocal-`L` rectangle statement for
this exact shifted kernel.

## Why existing routes do not close it

### Inoue/Soundararajan transfer

Explicit formulas for `M*(x,chi)` transfer the obstruction. Partial summation
turns an off-target simple zero `lambda` into a term containing

```text
K^(lambda-rho)/((lambda-rho)L'(lambda,chi)).
```

A multiple off-target zero produces a polynomial in `log K`. Soundararajan
type total bounds for Mobius sums do not imply the needed pointwise
cancellation of this shifted frequency aggregate.

### Mertens/B+ material

The Mertens factor `e^(-gamma)` is stable on the AK Euler-product side.
The separate `(MERTENS-LB)` and `(MERTENS-LB-MR)` routes are disproved and
do not supply any shifted Perron residue cancellation. They should not be
used as a substitute for Theorem E.

### B_infty

The corrected `B_infty` formula is a real GL(1) theorem:

```text
T_infty
  = (1/2) log L(2rho,psi)
    + BPC1 + BPC2 + T_{>=3}.
```

It controls the `k>=2` Euler-product tail. It does not control the additive
Perron sum `c_K` or the off-target residue aggregate.

## Claim-safe paper wording

Use:

```text
The local Perron double-pole residue is
log K/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2).
The global Perron-leading asymptotic is conditional on a shifted nonlocal
remainder theorem controlling off-target zero residues and contour tails.
Under that additional hypothesis and the AK DRH/EDRH Euler-product formula,
the corrected NDC limit is e^(-gamma).
```

Do not use:

```text
The Perron formula proves c_K = log K/L'(rho,chi)+o(log K).
The C1 note proves c_K = log K/L' - L''/(2L'^2)+o(1).
The NDC theorem is proved.
```

## Unresolved analytic inputs

1. Global simplicity or bounded multiplicity of all crossed off-target zeros,
   or explicit cancellation of higher-order off-target residues.
2. Pointwise cancellation theorem

```text
Z_simple(K,T_K) = o(log K)
```

for the sharp cutoff and the Perron-required moving height.
3. Bounds or moment estimates for reciprocal derivatives `1/L'(lambda,chi)`
   strong enough to support the chosen zero-sum mode.
4. Zero-avoiding heights and reciprocal-`L` bounds for
   `1/L(rho+w,chi)` on the exact shifted rectangle.
5. Perron truncation with endpoint convention for coefficients
   `mu(n) chi(n)n^(-rho)` at a height compatible with the contour bounds.
6. For the global subleading constant, the stronger remainder

```text
R_K = o(1).
```

7. If sharp pointwise cancellation is unavailable, a different theorem mode:
   retain the oscillatory off-target profile, smooth the cutoff with declared
   Mellin decay, or prove an explicitly averaged product theorem.
