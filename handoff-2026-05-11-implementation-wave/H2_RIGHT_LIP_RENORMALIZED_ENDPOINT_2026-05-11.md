---
schema_version: 1
title: "H2 Right-Lip Renormalized Endpoint"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_ENDPOINT_NO_THEOREM_PROMOTED
confidence: 0.80
tags: [h2, sym2, right-lip, endpoint, ec-ndc]
---

# H2 Right-Lip Renormalized Endpoint

Status: `CONDITIONAL_ENDPOINT_NO_THEOREM_PROMOTED`.

## Verdict

The first H2 theorem target should retain or subtract the full right-lip term:

```text
log P_E,W(K) + r loglogK - R_S1^+(K;E,W,eta,c)
  = B_H2(E,W) + o(1).
```

This is safer than the unprofiled pointwise theorem because current sources do
not neutralize right branches.

## Closed Algebra

The exact local decomposition remains:

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

The good-prime tail and bad-prime constant are closed local algebra.

## Lemmas To Write Next

Minimal theorem-grade route:

```text
RegularLogLeftEdge(E,W,eta;c)
S1-CutPlane-RenormalizedLogGrowth(E,W,eta;c)
ExactGoodPrimeSym2FinitePart(E,W)
Sym2-ZeroLedger-RegularLog(E,W,eta;c)
WeightedGoodPrimeMertens(E,W)
```

For the unprofiled theorem, add:

```text
R_S1^+(K;E,W,eta,c) + Z_sym,E,W(K)/2 = o(1).
```

That cancellation is not currently proved.

## Boundary

Do not claim:

- right-branch cancellation;
- pointwise H2 without profile/subtraction;
- H1 residue control from H2 branch damping;
- fixed-curve EC theorem from H2 alone.

H2 branch terms are `1/u`-damped. H1 reciprocal residues are not.

