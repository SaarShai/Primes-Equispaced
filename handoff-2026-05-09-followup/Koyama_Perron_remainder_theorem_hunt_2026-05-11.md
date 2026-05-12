---
schema_version: 1
title: "Koyama shifted Perron nonlocal remainder theorem hunt"
date: 2026-05-11
type: theorem-hunt
tier: claim-safe
status: DEFER
scope: "Exact shifted Perron remainder for K^w/(w L(rho+w,chi))"
sources:
  - handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
  - handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
tags: [koyama, gl1, perron, shifted-kernel, residues, obstruction]
---

# Koyama shifted Perron nonlocal remainder theorem hunt

## Status

`DEFER`.

The exact shifted Perron nonlocal remainder theorem is not closed. The local
target-zero residue is `PROVED`, but the nonlocal remainder is blocked by the
off-target zero residue aggregate. The sharp formal obstruction is:

```text
target zero simple + DRH/EDRH does not exclude off-target multiple zeros.
```

If an off-target zero has multiplicity `m >= 2`, the shifted kernel contributes
a residue with leading size `(log K)^(m-1)`. For `m=2`, this is another
oscillatory `log K` term, so the target leading theorem cannot be dependency
closed under only target-zero simplicity.

## Claim

Let `chi` be primitive non-principal and let

```text
rho = 1/2 + i t
```

be a simple noncentral zero of `L(s,chi)`. Define

```text
c_K(chi,rho) = sum_{n <= K} mu(n) chi(n) n^(-rho).
```

The desired theorem is:

```text
c_K(chi,rho) = log K / L'(rho,chi) + o(log K).
```

Using Perron with

```text
F_K(w) = K^w / (w L(rho+w,chi)),
```

this is equivalent to proving that, after extracting the double pole at
`w=0`, every nonlocal term in the shifted rectangle is `o(log K)`.

## Evidence

### Local target residue

At a simple zero `rho`,

```text
1/L(rho+w,chi)
  = 1/(L'(rho,chi) w)
    - L''(rho,chi)/(2 L'(rho,chi)^2)
    + O(w).
```

Therefore

```text
Res_{w=0} F_K(w)
  = log K/L'(rho,chi)
    - L''(rho,chi)/(2 L'(rho,chi)^2).
```

This is registry `P-0` and remains `PROVED`. It proves only the local
double-pole coefficient.

### Formal shifted decomposition

For a right edge `Re w = kappa > 1/2`, left edge `Re w = -A`, and zero-avoiding
height `T_K`, the shifted Perron move has the form

```text
c_K(chi,rho)
  = Res_{w=0} F_K(w)
    + Z_simple(K,T_K)
    + Z_multi(K,T_K)
    + Z_triv(K,T_K)
    + I_vert(K,T_K,A)
    + I_horiz(K,T_K,A)
    + E_Perron(K,T_K).
```

The target theorem needs the whole right side after `Res_{w=0}` to be
`o(log K)`.

### Off-target multiple-zero obstruction

Let `lambda != rho` be a nontrivial zero of multiplicity `m >= 2`, and put

```text
w_lambda = lambda - rho.
L(lambda+z,chi) = a_m z^m + a_{m+1} z^(m+1) + ... ,  a_m != 0.
```

Then near `w=w_lambda`,

```text
1/L(rho+w,chi) = a_m^(-1) (w-w_lambda)^(-m) + lower pole orders.
```

Since

```text
K^w / w
  = K^(w_lambda) exp((w-w_lambda) log K) / (w_lambda + (w-w_lambda)),
```

the residue at `w=w_lambda` contains the nonzero top-degree term

```text
K^(w_lambda) (log K)^(m-1) / ((m-1)! w_lambda a_m).
```

Under DRH, `Re(lambda)=Re(rho)=1/2`, so `K^(w_lambda)` is purely oscillatory.
Consequences:

```text
m = 2:  extra oscillatory log K-scale term.
m > 2:  term larger than log K.
```

Thus the theorem is not closed under "rho simple" alone. It must either assume
all crossed off-target zeros are simple, or prove that the full higher-order
off-target aggregate is `o(log K)`. For finitely many off-target multiple
zeros of maximal multiplicity, cancellation would require the corresponding
finite exponential polynomial in `log K` to vanish identically; this is an
extra theorem, not a consequence of DRH/EDRH.

This is a formal dependency no-go, not an asserted counterexample for actual
Dirichlet L-functions.

### Off-target simple-zero aggregate

If all crossed off-target zeros are simple, the remaining nonlocal zero term is

```text
Z_simple(K,T_K)
  = sum_{lambda != rho, |Im(lambda-rho)| <= T_K}
      K^(lambda-rho) / ((lambda-rho) L'(lambda,chi)).
```

Under DRH:

```text
Z_simple(K,T_K)
  = sum_{gamma != t, |gamma-t| <= T_K}
      exp(i(gamma-t) log K) / ((i(gamma-t)) L'(1/2+i gamma,chi)).
```

Each fixed off-target simple zero contributes only `O(1)`, hence no single
simple zero blocks the leading theorem. The blocker is the moving aggregate as
`T_K -> infinity`. The existing files contain no theorem giving

```text
Z_simple(K,T_K) = o(log K)
```

for the Perron-required height. Bounds for `M*(x,chi)` or for total Mobius
partial sums do not imply this pointwise cancellation in the shifted
frequency variable `log K`.

### Rectangle, horizontal, vertical, truncation

These terms look controllable, but only after adding a precise zero-avoiding
reciprocal-`L` package for this exact shifted rectangle.

| Term | Best current reduction | Status |
|---|---|---|
| Perron truncation | With half-weight endpoint convention and `kappa=1/2+1/log K`, standard truncation is expected to be `O(K^(1/2) log^2 K / T_K) + O(K^(-1/2))`; `T_K >> K^(1/2) log^3 K` would make this `o(log K)`. | `CONDITIONAL` |
| Right horizontal edge | Size is about `K^(1/2) T_K^(-1)` times a reciprocal-`L` factor on `Re(rho+w)>1`; harmless for `T_K` near `K/(log K)^B`. | `CONDITIONAL` |
| Left horizontal/vertical edges | Functional equation heuristics give factors like `(T_K/K)^A` times polylogs after shifting to `Re w=-A`; harmless if `T_K <= K/(log K)^B` and `B` is large. | `CONDITIONAL` |
| Zero-avoiding height | Inoue-style heights exist for the unshifted explicit formula, but the exact shifted theorem still needs a stated bound for `1/L(rho+w,chi)` on the chosen rectangle. | `DEFER` |

These contour terms are not the sharp obstruction. The off-target residue
aggregate is.

### Do standard explicit formula theorems imply it?

No theorem found implies the exact shifted statement.

External primary sources checked:

1. Shota Inoue, *Some explicit formulas for partial sums of Mobius functions*,
   Journal de Theorie des Nombres de Bordeaux 33 (2021), 273-315.
   - Theorem 1, formula (1.4), p.274, is an explicit formula for
     `M*(x;q,a)` with residues over zeros of Dirichlet L-functions modulo `q`.
   - Theorem 2, formula (2.1), p.276, is the truncated version with heights
     `T_nu in [T,2T]`.
   - Theorem 3 proof, pp.304-305, under GRH/multiplicity assumptions, still
     leaves the nontrivial-zero sum explicit.
   - Inoue explicitly flags the multiplicity problem on p.275:
     "We do not know even the boundedness of multiplicity at present."
   - URL: https://www.numdam.org/item/JTNB_2021__33_2_273_0.pdf

2. K. Soundararajan, *Partial sums of the Mobius function*,
   J. Reine Angew. Math. 631 (2009), 141-152.
   - Theorem 1, p.1 of arXiv:0705.0723v2, assumes RH and proves
     `M(x) << sqrt(x) exp((log x)^(1/2)(log log x)^14)`.
   - This is a total partial-sum bound. After Abel transfer to
     `c_K(chi,rho)`, it is far too coarse to isolate the target residue, and
     it gives no cancellation theorem for `Z_simple(K,T_K)`.
   - URL: https://arxiv.org/pdf/0705.0723

Partial summation from Inoue's `M*(x,chi)` formula transfers, rather than
removes, the obstruction. A simple off-target zero `lambda` contributes

```text
K^(lambda-rho)/((lambda-rho)L'(lambda,chi))
  - rho/(lambda(lambda-rho)L'(lambda,chi)),
```

and a multiple off-target zero contributes a polynomial in `log K` of degree
`m-1`. Therefore the standard explicit formula route reproduces the same
nonlocal residue aggregate.

## Dependency table

| Dependency | Needed claim | Current status | Decision |
|---|---|---|---|
| Setup | `chi` primitive non-principal; `rho=1/2+it` simple noncentral zero. | `CONDITIONAL` | Accept as working hypothesis. |
| Shifted Perron representation | `c_K` represented by `K^w/(wL(rho+w,chi))` plus truncation. | `CONDITIONAL` | Standard, but exact endpoint/truncation package still must be stated. |
| Local target residue | `Res_{w=0} F_K = log K/L' - L''/(2L'^2)`. | `PROVED` | Closed algebraically. |
| Trivial-zero residues | Trivial zeros give `O(K^(-1/2))`-type tails. | `CONDITIONAL` | Not the blocker; can be closed with routine functional-equation estimates. |
| Off-target multiple zeros | Higher-order poles give `(log K)^(m-1)` residues. | `PROVED` local obstruction | Blocks theorem under target-zero simplicity alone. |
| Off-target simple aggregate | `Z_simple(K,T_K)=o(log K)`. | `DEFER` | Exact missing cancellation theorem. |
| Zero-avoiding rectangle bounds | Horizontal/vertical integrals are `o(log K)`. | `CONDITIONAL` | Needs a cited reciprocal-`L` rectangle theorem for this shifted kernel. |
| Perron truncation | `E_Perron=o(log K)`. | `CONDITIONAL` | Feasible for large `T_K`, but must be included in the theorem statement. |
| AK Euler product | `E_K log K -> L'(rho,chi)/e^gamma`. | `CONDITIONAL` | Aoki-Koyama 2023, (1.4), p.235, under DRH/EDRH. |
| Corrected NDC | `D_K -> e^(-gamma)`. | `CONDITIONAL` | Requires AK plus the still-missing Perron-leading theorem. |

## Missing theorem

The exact theorem still needed is:

**Shifted Perron nonlocal remainder theorem.** Let `chi` be primitive
non-principal and let `rho=1/2+it` be a simple noncentral zero of
`L(s,chi)`. Under the intended DRH/EDRH package, choose `A>1`, `B>0`, and
zero-avoiding heights

```text
T_K in [K/(log K)^B, 2K/(log K)^B].
```

For

```text
F_K(w)=K^w/(wL(rho+w,chi)),
```

after extracting `Res_{w=0} F_K`, the sum of:

```text
1. all off-target nontrivial-zero residues, including higher-order residues;
2. all trivial-zero residues;
3. shifted vertical integral;
4. horizontal integrals;
5. Perron truncation and endpoint error
```

is `o(log K)`.

A cleaner sufficient variant is:

```text
all crossed off-target zeros are simple,
Z_simple(K,T_K)=o(log K),
and the shifted rectangle/truncation terms are o(log K).
```

Without either the higher-order aggregate clause or global off-target
simplicity, the theorem should not be stated.

## Verification

Read:

```text
handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_leading_gap_audit_2026-05-10.md
handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
```

Primary-source checks:

```text
Inoue 2021 JTNB PDF: Theorem 1 (1.4), Theorem 2 (2.1), Theorem 3 proof.
Soundararajan 2009 arXiv PDF: Theorem 1.
```

Commands used locally:

```bash
sed -n '...' [requested handoff files]
rg -n "shifted Perron|nonlocal|other zeros|Gonek|Hejhal|Soundararajan|Perron|zero-avoiding|T_nu|Tν|1/L\\(|K\\^w" handoff-2026-05-09-followup -g '*.md'
find /Users/za/Documents/Farey\ NOW -path '*Koyama_Perron_remainder_theorem_hunt_2026-05-11.md' -print
git diff --check -- handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
git status --short -- handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
```

No numerical or code tests are applicable to this markdown-only theorem hunt.

## Changed files

```text
handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
```

No commit. No push.

## Risks

1. A specialized published theorem may already prove the shifted residue
   cancellation, but it is not in the read set or the checked primary sources.
2. The contour terms are only reduced, not promoted; publication use still
   needs a precise reciprocal-`L` rectangle theorem.
3. The multiple-zero obstruction is conditional on possible off-target
   multiplicity. It proves insufficiency of the current dependency package,
   not existence of such zeros for the target Dirichlet L-functions.
4. Numerics at finite `K` can hide the off-target aggregate; they do not prove
   `Z_simple(K,T_K)=o(log K)`.

## Compact packet

Status: `DEFER`.

Claim-safe conclusion:

```text
The shifted local double-pole residue is proved. The exact Perron-leading
theorem is not closed. Off-target multiple zeros would contribute additional
oscillatory log-scale or larger residues, so target-zero simplicity plus
DRH/EDRH is not enough. If all off-target zeros are assumed simple, the
remaining hard dependency is the pointwise cancellation
Z_simple(K,T_K)=o(log K) for the exact shifted kernel, together with explicit
zero-avoiding rectangle and truncation bounds.
```
