---
schema_version: 1
title: "Agent 04 H1 finite-box theorem assembly"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 04 -- H1 Finite-Box Theorem Assembly"
type: theorem-package
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.86
dependencies:
  - start.md
  - token-economy.yaml
  - L0_rules.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/H1_LZ_HEIGHT_VERIFICATION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
tags: [breakthrough-wave-2, h1, finite-box, legal-heights, positive-rank]
---

# Agent 04 H1 Finite-Box Theorem Assembly

status: `RIGOROUS_REDUCTION`

Wave 2 status enum:

```text
THEOREM_PROMOTED
RIGOROUS_REDUCTION
NO_GO
DIAGNOSTIC_ONLY
```

This packet is `RIGOROUS_REDUCTION`. No theorem is promoted.

Input labels below are not promotion statuses:

```text
SOURCE_CLOSED_LOCAL       local algebra/reduction closed in read packets
SOURCE_ROUTED_CONDITIONAL external-source route with explicit caveats
OPEN_INPUT                hypothesis still unproved/source-open
EXCLUDED                  not used in this theorem mode
```

Analytic rank only:

```text
r = ord_(s=1) L(E,s).
```

No BSD rank substitution, H2 damping import, finite numerical evidence, cross-curve
universality, or Koyama correspondence/email material is used.

## Assembled Conditional Theorem

Let `E/Q` be fixed and let `r>=1` be its analytic rank. Let `W` be the fixed H1
kernel used by the contour packet, with

```text
W_hat(z)=w_-1/z + holomorphic at z=0,
```

and with smoothstep-scale strip decay

```text
|W_hat^(a)(x+it)| <= C_a (1+|t|)^(-q_a)
```

for every derivative order used by crossed multiple-zero residues. In the
simple-zero height package use `q_0=2`.

Fix strip parameters

```text
1/2 < eta < 1,
1/2 < sigma < 3/2,
u = log K.
```

Assume the exact fixed-kernel H1 Mellin/Perron identity on `Re z=sigma` and the
finite-height contour shift are valid in one declared pointwise finite-box mode:

```text
c_E,W(e^u) = (1/(2 pi i)) int_(Re z=sigma)
  e^(u z) W_hat(z)/L(E,1+z) dz.
```

For a legal height `T`, define

```text
F_u(z) = e^(u z) W_hat(z)/L(E,1+z),

I_sigma(T,u) = (1/(2 pi i)) int_(sigma-iT)^(sigma+iT) F_u(z) dz,
V_eta(T,u)   = (1/(2 pi i)) int_(-eta-iT)^(-eta+iT) F_u(z) dz,
H_+(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x+iT) dx,
H_-(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x-iT) dx.
```

Then the finite-box identity is

```text
I_sigma(T,u)
 = sum_(z0 in P_T) Res_(z=z0) F_u(z)
   + V_eta(T,u) + H_+(T,u) - H_-(T,u),
```

where `P_T` is the set of crossed poles in
`-eta < Re z < sigma`, `|Im z| < T`.

Now choose a fixed `C>sigma`. Under the conditional Li-Zaharescu H-height route
below, take legal moving heights

```text
T_box(u) in [exp(Cu), exp(Cu)+1].
```

Assume no crossed zero with `Re z>0` is silently discarded: every such term is
absent under the declared zero-location hypothesis, explicitly retained, or
handled in a separately proved theorem mode.

Let the central residue polynomial be

```text
Q_E,W(u) = Res_(z=0) F_u(z)
         = sum_(ell=0)^r C_ell u^ell,
```

with top coefficient

```text
C_r = w_-1/L^(r)(E,1).
```

If all hypotheses in `Source-Routed/Open Inputs` below hold, then

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r)
           = (w_-1/L^(r)(E,1)) u^r + o(u^r).
```

For normalized kernels with `w_-1=1`, the leading term is

```text
u^r/L^(r)(E,1).
```

This is only an H1 statement. It does not assert H1/H2 product stabilization.

## Source-Closed Local Inputs

`SOURCE_CLOSED_LOCAL`: finite-box residue algebra.

The rectangle identity, central polynomial, simple-zero residue

```text
e^(i gamma u) W_hat(i gamma)/L'(E,1+i gamma),
```

and multiple-zero Laurent residue polynomial are local contour/residue algebra
from `H1_CONTOUR_SHIFT_THEOREM.md` and Agent 03. They are valid only after the
declared Mellin/Perron and contour hypotheses.

`SOURCE_CLOSED_LOCAL`: central coefficient normalization.

The top central coefficient is `w_-1/L^(r)(E,1)`, not a factorial-renormalized
variant. With `w_-1=1`, it is `1/L^(r)(E,1)`.

`SOURCE_CLOSED_LOCAL`: legal exponential height arithmetic.

Because the source-safe H1 start line has `sigma>1/2` and the checked kernel
decay is `q_0=2`, the original-line truncation has scale

```text
Tail_sigma(T,u) << e^(sigma u) T^(-1).
```

Thus pointwise moving boxes require exponential height. With
`T_box(u) in [exp(Cu), exp(Cu)+1]` and `C>sigma`,

```text
Tail_sigma(T_box,u) << exp((sigma-C)u) = o(u^r).
```

`SOURCE_CLOSED_LOCAL`: H-left input as used by the read packets.

The legal-height/minimum-modulus packets keep the shifted-left line closed by
choosing `eta>1/2` in the reciprocal-strip setup. In this assembly that is used
only as the H-left tail input

```text
V_eta(T_box,u)=o(u^r)
```

in the same kernel, strip, and pointwise theorem mode. It is not H2 damping.

`SOURCE_CLOSED_LOCAL`: simple-zero legal-height reduction.

For simple critical-line zeros define

```text
R_E,1(T) =
  sum_(T<|gamma|<=2T, simple) |L'(E,1+i gamma)|^(-1),

A_W(T) =
  sum_(T<|gamma|<=2T, simple)
    |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1).
```

With `q_0=2`,

```text
A_W(T) << T^(-2) R_E,1(T).
```

If

```text
R_E,1(T)=o(T^2 (log T)^(r-1)),
```

then the simple-zero residue aggregate below `T_box(u)` is `o(u^r)`. In rank
one the exact target is

```text
R_E,1(T)=o(T^2).
```

This is a reduction, not a proved fixed-curve theorem.

`SOURCE_CLOSED_LOCAL`: multiple-zero effective-degree rule.

For a crossed zero `rho` of multiplicity `m`, put `alpha=rho-1`. If

```text
1/L(E,1+z) =
  sum_(j=1)^m b_(rho,-j)(z-alpha)^(-j) + holomorphic,
```

then

```text
R_rho(u)
 = e^(alpha u) sum_(ell=0)^(m-1) A_(rho,ell) u^ell,

A_(rho,ell)
 = (1/ell!) sum_(j=ell+1)^m
    b_(rho,-j) W_hat^(j-1-ell)(alpha)/(j-1-ell)!.
```

After kernel zeros, internal Laurent/kernel cancellation, and exact
same-exponent netting, define

```text
D_alpha = max { ell : A_(alpha,ell)^net != 0 }.
```

Pointwise central-only positive-rank H1 requires every retained critical-line
effective degree to satisfy

```text
D_alpha < r.
```

The generic sufficient individual-zero condition is

```text
m <= r + nu_rho,
```

where `nu_rho=ord_(z=alpha) W_hat(z)`. This generic condition does not replace
the effective-degree audit.

## Source-Routed/Open Inputs

`SOURCE_ROUTED_CONDITIONAL`: Li-Zaharescu horizontal height.

The LZ route may be used only with its caveat. Under the normalized EC/newform
no-right-half-zero hypothesis, it gives selected unit-interval heights with

```text
M(T) <= exp(A_E log T/loglog T)=T^o(1)
```

on the required horizontal strip after EC center shift and functional-equation
reflection. With `T_box(u)=exp(Cu)+O(1)`, `q_0=2`, and a small `epsilon>0`,

```text
H_horiz(T_box,u)
  << exp((sigma-C(2-epsilon))u)=o(u^r)
```

provided `C(2-epsilon)>sigma`. The original-line tail still requires `C>sigma`.

External citation protocol carried from the verified LZ packet and rechecked
locally:

```text
PDF: /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pdf
SHA256: add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
Text: /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pypdf.txt
```

Short anchors:

- PDF p. 2: holomorphic cusp-form `L`-functions are in the class.
- PDF p. 4, Proposition 3.1: "Each interval [T,T + 1] contains".
- PDF p. 20, Lemma 7.6: "If L(s) has no zeros".

Therefore the assembly may say `conditional horizontal H-height is
source-routed`; it must not say LZ unconditionally closes H1.

`OPEN_INPUT`: exact fixed-kernel H1 Perron identity and contour theorem.

The finite-box identity is local algebra after the object is legitimate. The
exact endpoint-smoothed fixed-kernel Perron identity, legal indentation scheme,
boundary avoidance, and convergence mode remain hypotheses unless supplied by a
separate source-closed packet.

`OPEN_INPUT`: simple-zero reciprocal derivative theorem.

The fixed-curve condition

```text
R_E,1(T)=o(T^2 (log T)^(r-1))
```

is not proved in the checked packets. In rank one this is the live target
`R_E,1(T)=o(T^2)`. Zero count, spacing, LZ selected heights, H2 branch damping,
and finite numerics do not imply it.

`OPEN_INPUT`: multiple-zero Laurent coefficient control.

The local Laurent formula is closed, but the required coefficient sums are not.
For central-only pointwise H1, after every `D_alpha>=r` term is killed,
cancelled, retained, or moved to a proved averaged/PV mode, one still needs

```text
sum_(Re alpha=0) |A_(alpha,ell)^net| < infinity,
0 <= ell < r,
```

or an equivalent bounded/PV/averaged theorem in the declared mode. Kernel decay
alone does not control reciprocal Laurent coefficients.

`OPEN_INPUT`: right-half crossed zeros.

Either assume the same no-right-half-zero hypothesis used by the LZ route, or
retain every crossed `Re z>0` residue. Silent deletion is forbidden.

`EXCLUDED`: H2 branch damping and product stabilization.

No `1/u` branch damping from H2 is imported into H1 reciprocal-pole residues.
H2 would be a separate same-mode input before any product theorem, and no such
product theorem is claimed here.

`EXCLUDED`: rank zero.

This package is positive analytic rank only. Rank zero requires an
oscillatory/profile/averaged theorem unless every nonzero-frequency H1 residue
vanishes, cancels, or is filtered in a proved mode.

## Proof Skeleton

1. Start from the exact fixed-kernel H1 Perron object on `Re z=sigma`.
2. Apply the finite rectangle identity at a legal height `T`.
3. Evaluate the central pole at `z=0`; obtain `Q_E,W(u)` with leading
   coefficient `w_-1/L^(r)(E,1)`.
4. Choose `T_box(u) in [exp(Cu), exp(Cu)+1]`, `C>sigma`. The original-line tail
   is `o(u^r)`.
5. Use conditional LZ selected heights plus EC reflection to bound the
   horizontal edges by `o(u^r)`. Use H-left with `eta>1/2` for the shifted line
   in the same mode.
6. For simple zeros, dyadically sum
   `A_W(T) << T^(-2) R_E,1(T)` up to `T_box(u)`. The open target
   `R_E,1(T)=o(T^2(log T)^(r-1))` gives `o(u^r)`; for `r=1`, this is
   `R_E,1(T)=o(T^2)`.
7. For multiple zeros, use the Laurent residue polynomial. After same-frequency
   netting, require `D_alpha<r` for every central-only retained critical-line
   exponent and bounded/absolutely summable lower-degree aggregates.
8. Combine tails and offcentral residues:

   ```text
   Z_E,W(u) + V_eta(T_box,u) + H_+(T_box,u) - H_-(T_box,u)
     + Tail_sigma(T_box,u) = o(u^r).
   ```

9. Conclude

   ```text
   c_E,W(e^u)=Q_E,W(u)+o(u^r).
   ```

## No-Promotion Boundary

Do not promote any of the following from this packet:

```text
unconditional EC H1 theorem;
rank-one H1 theorem without R_E,1(T)=o(T^2);
positive-rank H1 theorem without R_E,1(T)=o(T^2(log T)^(r-1)) or substitute;
multiple-zero closure from kernel decay alone;
pointwise central-only theorem with a retained D_alpha>=r oscillation;
LZ as unconditional H-height closure;
H1 residue control from H2 branch damping;
rank-zero pointwise constant stabilization;
H1/H2 product theorem without same-mode H2 closure;
anything using BSD rank, finite numerics, cross-curve universality, or Koyama
correspondence/email material as analytic input.
```

## Verification Notes

Read targeted context only:

```text
start.md
token-economy.yaml
L0_rules.md
primes-equispaced/L1_index.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/DISPATCH_MANIFEST_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
primes-equispaced/handoff-2026-05-11-all-in-wave/H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md
primes-equispaced/handoff-2026-05-11-relay02/H1_RANK_ONE_ANTI_SMALL_DERIVATIVE_FRONTIER_2026-05-11.md
primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT03_H1_MULTIPLE_ZERO_LAURENT_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
primes-equispaced/handoff-2026-05-11-gpt55-extra-high-continuation/H1_LZ_HEIGHT_VERIFICATION_2026-05-11.md
primes-equispaced/handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
```

Checks performed:

```text
./te doctor returned ok: true
LZ PDF SHA256 rechecked locally
LZ text anchors searched locally
no archive pages opened
no web search used
no theorem promoted
```

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT04_H1_FINITE_BOX_THEOREM_ASSEMBLY_2026-05-11.md
```
