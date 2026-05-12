---
schema_version: 1
title: "Koyama Perron-leading moonshot"
date: 2026-05-11
type: moonshot-gap-audit
tier: claim-safe
status: DEFER
scope: "Shifted Perron-leading for c_K(chi,rho)"
sources:
  - handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
tags: [koyama, gl1, perron, moonshot, shifted-kernel, other-zeros]
---

# Koyama Perron-leading moonshot

## Status

`DEFER`.

I do not promote

```text
c_K(chi,rho) = log K / L'(rho,chi) + o(log K).
```

The local residue is closed. The global shifted-Perron remainder is still not
dependency-closed. The sharp obstruction is the critical-line residue aggregate
from off-target zeros, especially possible off-target multiple zeros.

## Claim

Let `chi` be primitive non-principal and let

```text
rho = 1/2 + i t
```

be a simple noncentral zero of `L(s,chi)`. Define

```text
c_K(chi,rho) = sum_{n <= K} mu(n) chi(n) n^{-rho}.
```

The target claim is:

```text
c_K(chi,rho) = log K / L'(rho,chi) + o(log K).
```

This would follow from the shifted Perron decomposition for

```text
F_K(w) = K^w / (w L(rho+w,chi))
```

if all nonlocal terms after the `w=0` double-pole residue are `o(log K)`.

## Evidence

### Closed local piece

At `w=0`,

```text
1/L(rho+w,chi)
  = 1/(L'(rho,chi) w)
    - L''(rho,chi)/(2 L'(rho,chi)^2)
    + O(w).
```

Therefore

```text
Res_{w=0} K^w / (w L(rho+w,chi))
  = log K / L'(rho,chi)
    - L''(rho,chi)/(2 L'(rho,chi)^2).
```

This is registry `P-0`: `PROVED`.

### Direct rectangle attempt under DRH/EDRH

Use Perron with

```text
kappa = 1/2 + 1/log K,
T = T_K,
F_K(w) = K^w / (w L(rho+w,chi)).
```

Move the contour from `Re w = kappa` to `Re w = -A`, with `A > 1`, through a
zero-avoiding height `T_K`. The formal decomposition is:

```text
c_K(chi,rho)
  = Res_{w=0} F_K(w)
    + Z_K(T_K)
    + Z_K^triv(T_K)
    + V_K(A,T_K)
    + H_K(A,T_K)
    + P_K(T_K),
```

where:

```text
Z_K(T)
  = sum_{lambda != rho, |Im(lambda-rho)| <= T}
      Res_{w=lambda-rho} F_K(w)
```

is the off-target nontrivial-zero aggregate.

The four required pieces behave as follows.

| Piece | Moonshot result | Status |
|---|---|---|
| Other-zero aggregate | Not closed. For simple off-target zeros the terms are `K^{i(gamma-t)}/((lambda-rho)L'(lambda,chi))`; no cited theorem gives `Z_K(T_K)=o(log K)` for the Perron-required moving height. If an off-target zero has multiplicity `m >= 2`, it can contribute a term of size `(log K)^{m-1}`. | `DEFER` |
| Shifted vertical contour | Plausibly controllable by shifting to `Re w=-A` and using the functional equation plus a zero-avoiding line; this is lower order if `T_K < K` by a fixed logarithmic margin and the standard reciprocal bounds are available. Not the load-bearing obstruction, but not independently citation-closed in the read set. | `CONDITIONAL` |
| Horizontal sides | Plausibly controllable at an Inoue-style chosen height `T_nu in [T,2T]`; on the right edge the factor is about `K^{1/2}/T`, and on the left edge the factor is `(T/K)^A`. Needs a published zero-avoiding reciprocal bound for the exact shifted rectangle. | `CONDITIONAL` |
| Perron truncation | With the half-weight endpoint convention, standard truncation gives roughly `O(K^{1/2} log^2 K / T_K) + O(K^{-1/2})`; choosing `T_K >> K^{1/2} log^3 K` makes this `o(log K)`. | `CONDITIONAL` |

Thus a direct rectangle reduces the theorem to the off-target residue aggregate
plus a cited zero-avoiding rectangle package. The read set does not contain
that package.

### Sharp obstruction lemma

**Lemma.** Suppose `lambda != rho` is a nontrivial zero of `L(s,chi)` of
multiplicity `m >= 2`, and set

```text
w_lambda = lambda - rho.
```

Under DRH, `Re w_lambda = 0`. Write

```text
L(lambda+z,chi) = a_m z^m + O(z^{m+1}),   a_m != 0.
```

Then the residue of `F_K(w)` at `w=w_lambda` contains the term

```text
K^{w_lambda} (log K)^{m-1} / ((m-1)! w_lambda a_m)
```

plus lower powers of `log K`.

For `m=2`, this is an additional oscillatory `log K`-scale term. For
`m>2`, it is larger than `log K`. Therefore the Perron-leading claim with
only the target zero assumed simple is not closed under DRH/EDRH alone. It
also needs either:

```text
all off-target nontrivial zeros crossing the rectangle are simple,
```

or a theorem proving that the full higher-order residue aggregate is
`o(log K)`.

This is a method-level no-go for the current dependency set, not a
disproof for actual Dirichlet L-functions.

### Transfer attempt from Inoue/Soundararajan-style M*(x,chi)

Let

```text
M*(x,chi) = sum_{n <= x}' mu(n) chi(n).
```

Partial summation gives, up to the same endpoint convention,

```text
c_K(chi,rho)
  = K^{-rho} M*(K,chi)
    + rho int_1^K M*(x,chi) x^{-rho-1} dx.
```

The target zero term in Inoue's explicit formula,

```text
M*(x,chi) contains x^rho / (rho L'(rho,chi)),
```

transfers to

```text
log K / L'(rho,chi) + O(1).
```

For an off-target simple zero `lambda`, the transfer produces

```text
K^{lambda-rho}/((lambda-rho)L'(lambda,chi))
  - rho/(lambda (lambda-rho) L'(lambda,chi)),
```

which contains the same moving oscillatory aggregate as the shifted Perron
rectangle. For an off-target multiple zero, the same polynomial-in-`log K`
obstruction appears.

Soundararajan-type bounds for `M*(x,chi)` do not by themselves close the
transfer. A bound of the shape

```text
M*(x,chi) << x^{1/2} exp(C sqrt(log x) (log log x)^B)
```

only gives, after partial summation,

```text
int_1^K exp(C sqrt(log x) (log log x)^B) dx/x,
```

which is far larger than `log K` for fixed positive `C`. It is an upper bound
for total size, not a residue-cancellation theorem.

So the Inoue/Soundararajan route transfers the problem; it does not remove it.

## Exact missing external theorem

To close the leading theorem, cite or prove the following exact theorem.

**Shifted Perron nonlocal remainder theorem.** Let `chi` be primitive
non-principal and let `rho=1/2+it` be a simple noncentral zero of `L(s,chi)`.
Assume the intended DRH/EDRH package. There exist constants `A>1`, `B>0` and
heights

```text
T_K in [K/(log K)^B, 2K/(log K)^B]
```

avoiding zeros sufficiently for the rectangle with right edge
`Re w=1/2+1/log K` and left edge `Re w=-A`, such that:

```text
1. Z_K(T_K)
   := sum_{lambda != rho, |Im(lambda-rho)| <= T_K}
        Res_{w=lambda-rho} K^w/(w L(rho+w,chi))
      = o(log K).

2. The shifted left vertical integral is o(log K).

3. The two horizontal integrals are o(log K).

4. The Perron truncation error for
   sum_{n <= K} mu(n) chi(n) n^{-rho}
   with the half-weight endpoint convention is o(log K).
```

The theorem must include higher-order residues if off-target multiple zeros
are not separately excluded. A sufficient cleaner variant is:

```text
all nontrivial zeros of L(s,chi) in the crossed strip are simple,
and
sum_{0<|gamma-t|<=T_K}
  K^{i(gamma-t)} / ((1/2+i gamma-rho) L'(1/2+i gamma,chi))
  = o(log K).
```

No theorem of this exact form is present in the read set. Inoue's explicit
formula for `M*(x,chi)` and Soundararajan's bound for partial sums do not
state this shifted residue cancellation.

## Verification

Read and cross-checked:

```text
handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md
handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
```

Commands run:

```bash
git status --short
wc -l handoff-2026-05-09-followup/KOYAMA_NEXT_SPRINT_SYNTHESIS_2026-05-10.md \
      handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md \
      handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md \
      handoff-2026-05-09-followup/Koyama_AK_constant_proof.md \
      handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
sed -n '...' [the five requested files]
```

No proof was promoted. No code tests are applicable to this markdown-only
handoff.

## Changed files

```text
handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
```

No commit. No push. No other file intentionally modified.

## Risks

1. A published theorem may already imply the shifted residue cancellation, but
   it is not cited in the current handoff set.
2. The contour estimates above are only sketched as a reduction; publication
   use still needs a precise zero-avoiding reciprocal-`L` bound at the chosen
   heights.
3. The target theorem should not be stated under only "target zero simple";
   off-target multiple zeros create possible `log K`-scale residues.
4. Numerical agreement with the leading term does not control the moving
   residue aggregate at theorem level.

## Final packet

Status: `DEFER`.

Claim-safe output:

```text
The shifted local double-pole residue is proved. A direct rectangle and an
Inoue/Soundararajan transfer both reduce Perron-leading to a missing shifted
nonlocal remainder theorem. The sharp obstruction is the off-target zero
aggregate; under DRH/EDRH alone, off-target multiple zeros would produce
additional log-scale residues. Do not promote c_K = log K/L' + o(log K)
until the exact missing theorem above is proved or cited.
```
