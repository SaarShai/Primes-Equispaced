---
title: "Agent 1 - GL(1) shifted Perron closure"
date: 2026-05-11
status: NO_GO
scope: "Off-target residue control for F_K(w)=K^w/(w L(rho+w,chi))"
---

# Agent 1 - GL(1) Shifted Perron Closure

Status: `NO_GO`.

Confidence: `0.96`, for the current dependency package only. Aggregation rule:
minimum of formal residue obstruction, checked-source transfer audit, and
promotion-risk audit.

Dependencies: primitive non-principal `chi`; simple noncentral target zero
`rho=1/2+it`; intended DRH/EDRH only where stated. This file does not assert
that Dirichlet `L`-functions have multiple zeros, and does not assert that no
stronger theorem exists under extra hypotheses.

## Verdict

Do not promote

```text
c_K(chi,rho) = sum_{n<=K} mu(n) chi(n) n^(-rho)
             = log K / L'(rho,chi) + o(log K)
```

from target-zero simplicity plus the local residue calculation.

Reason: an off-target zero `lambda != rho` of multiplicity `m>=2` produces a
higher-order pole of

```text
F_K(w)=K^w/(w L(rho+w,chi))
```

at `w_lambda=lambda-rho`. Its residue contains a nonzero top term of size
`(log K)^(m-1)`. Under DRH this term has no power saving in `K`. For `m=2`,
it is another `log K`-scale oscillatory term.

## Local Obstruction Lemma

Let `lambda != rho` be a nontrivial zero of `L(s,chi)` of multiplicity `m`.
Write

```text
z = w - w_lambda,       w_lambda = lambda - rho,
L(lambda+z,chi) = a_m z^m + a_{m+1} z^(m+1) + ...,
a_m = L^(m)(lambda,chi)/m! != 0.
```

Then

```text
1/L(lambda+z,chi) = a_m^(-1) z^(-m) + O(z^(-m+1)),
K^w/w = K^w_lambda exp(z log K)/(w_lambda+z).
```

The residue at `w=w_lambda` is the coefficient of `z^(-1)`, hence has
leading term

```text
K^(lambda-rho) (log K)^(m-1)
---------------------------------------
(m-1)! (lambda-rho) a_m
```

plus lower powers of `log K`.

If DRH holds, `Re(lambda-rho)=0`, so `|K^(lambda-rho)|=1`. Therefore:

```text
m=1:  simple off-target term
      K^(lambda-rho)/((lambda-rho)L'(lambda,chi)).

m=2:  extra log K-scale term.

m>2:  term larger than the target log K scale.
```

This proves that target-zero simplicity alone cannot close the global
Perron-leading theorem. Any closure must either exclude off-target multiple
zeros or prove cancellation of all higher-order off-target residues.

## Exact Remaining Theorem

A sufficient closure theorem would be:

```text
Let chi be primitive non-principal and rho=1/2+it a simple noncentral zero.
Choose a zero-avoiding shifted Perron rectangle with T_K in a Perron-valid
range. After extracting Res_{w=0} F_K(w), the sum of:

1. all off-target nontrivial-zero residues, including higher-order residues;
2. all trivial-zero residues;
3. shifted vertical and horizontal contour integrals;
4. Perron truncation and endpoint errors

is o(log K).
```

A cleaner but still nontrivial sufficient package is:

```text
all crossed off-target nontrivial zeros are simple,
Z_simple(K,T_K)
  := sum_{lambda != rho, |Im(lambda-rho)|<=T_K}
       K^(lambda-rho)/((lambda-rho)L'(lambda,chi))
   = o(log K),
and all shifted rectangle/truncation terms are o(log K).
```

The checked sources do not supply this theorem.

## Primary Source Checks

1. Inoue, "Some explicit formulas for partial sums of Mobius functions",
   Journal de Theorie des Nombres de Bordeaux 33 (2021), 273-315.
   Primary PDF retrieved from
   `https://www.numdam.org/item/JTNB_2021__33_2_273_0.pdf`.

   Relevant facts:

   - Theorem 1, p. 274, equation (1.4), keeps zero multiplicity inside a
     derivative residue term. Verbatim: "m(ρ) indicates the multiplicity of ρ".
   - Theorem 2, p. 276, equation (2.1), is a truncated explicit formula with
     the same multiplicity-sensitive residue structure. Verbatim: "the first
     sum runs over non-trivial zeros".
   - The paper explicitly flags the obstruction. Verbatim, p. 275: "We do not
     know even the boundedness of multiplicity at present."

   Use: Inoue transfers the problem into an explicit zero-residue sum; it does
   not prove the shifted cancellation `Z_simple=o(log K)`, and it explicitly
   does not remove the multiple-zero issue.

2. Soundararajan, "Partial sums of the Mobius function", arXiv:0705.0723v2.
   Primary PDF retrieved from `https://arxiv.org/pdf/0705.0723`.

   Relevant fact:

   - Theorem 1, p. 1, under RH gives the total bound. Verbatim:
     "Theorem 1. Assume RH. For large x we have"; the displayed bound is
     `M(x) << sqrt(x) exp((log x)^(1/2)(log log x)^14)`.

   Use: this is a total Mobius partial-sum bound. Partial summation gives a
   bound far larger than `o(log K)` after isolating the target zero; it gives no
   theorem for the shifted off-target residue aggregate.

## Gap Map

| Item | Finding | Promotion risk |
|---|---|---|
| Target local residue at `w=0` | closed algebra | safe local lemma only |
| Off-target simple residues | exact formula known | missing `Z_simple=o(log K)` |
| Off-target multiple residues | local obstruction proved above | blocks target-simplicity-only theorem |
| Trivial-zero residues | likely lower order | still needs rectangle statement |
| Horizontal/vertical integrals | plausible by zero-avoiding bounds | not citation-closed here |
| Perron truncation | plausible with suitable `T_K` | must be included in theorem |

## Do Not Promote Unless

Do not state `c_K = log K/L'(rho,chi) + o(log K)` unless one of the following
is supplied with primary-source quotes or a full proof:

```text
1. all off-target higher-order residues are included and proved to be o(log K);
or
2. all crossed off-target zeros are assumed/proved simple, Z_simple(K,T_K)=o(log K),
   and the shifted rectangle plus truncation terms are o(log K).
```

Do not treat target-zero simplicity, DRH/EDRH, Inoue explicit formulas, or
Soundararajan-type total Mobius bounds as a substitute for that closure.

## Verification

Read first:

```text
HANDOFF.md
handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
handoff-2026-05-09-followup/Koyama_Perron_moonshot_2026-05-11.md
handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
```

Primary retrieval commands used:

```bash
curl -L -o /tmp/farey_agent1_sources/inoue_jtnb_2021.pdf \
  https://www.numdam.org/item/JTNB_2021__33_2_273_0.pdf
curl -L -o /tmp/farey_agent1_sources/sound_mobius_0705.0723.pdf \
  https://arxiv.org/pdf/0705.0723
```

Text extraction used local `pypdf`/`pdfminer`; `pdftotext` was unavailable.
