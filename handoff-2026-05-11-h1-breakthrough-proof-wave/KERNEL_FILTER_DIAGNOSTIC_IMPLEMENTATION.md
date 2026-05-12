---
schema_version: 1
title: "Kernel-filter diagnostic implementation"
date: 2026-05-11
type: diagnostic
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.78
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RANK_ZERO_OSCILLATORY_PROFILE.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
tags: [ec-ndc, h1, kernel-filtering, diagnostics]
---

# Kernel-Filter Diagnostic Implementation

## Do Not Promote Unless

- Filtering is stated as a signed-kernel diagnostic, not a fixed positive
  smoothing theorem.
- Tail residues after the filtered finite zero set are controlled separately.
- The kernel class is declared; the script uses signed log-Gaussian Schwartz
  kernels, not compactly supported positive kernels.
- Named ordinates are real H1 offcentral zero ordinates from a verified source
  before any curve-specific claim is made.
- The final theorem does not depend on a kernel family secretly chosen from
  unknown zeros unless that dependence is explicitly allowed.

## Verdict

Finite signed filtering is implementation-ready. The attached script
`kernel_filter_moments.py` constructs a signed log-domain Gaussian kernel
whose Mellin transform satisfies

```text
W_hat(0)=1,
W_hat(i gamma_j)=0
```

for any finite list of supplied ordinates.

This is useful for diagnostics:

- kill the first few low H1 reciprocal residues;
- replay finite smoothing measurements;
- see whether the apparent stabilization is low-zero dominated.

It is not a theorem that smoothing alone stabilizes H1.

## Construction

In log variables `t=exp(x)`,

```text
W_hat(z)=int_R Phi(x) exp(zx) dx,
Phi(x)=W(exp(x)).
```

The script chooses

```text
Phi(x)=sum_j c_j exp(-(x-a_j)^2/(2 sigma^2)).
```

For each center `a_j`,

```text
int_R exp(-(x-a_j)^2/(2 sigma^2)) exp(zx) dx
 = sqrt(2pi) sigma exp(z a_j + sigma^2 z^2/2).
```

With `J` positive ordinates, the real constraints are:

```text
W_hat(0)=1,
Re W_hat(i gamma_j)=0,
Im W_hat(i gamma_j)=0,       1<=j<=J.
```

Using `1+2J` centers gives a square real linear system for real coefficients
`c_j`, hence a real signed kernel.

## Smoke Test

Example:

```bash
python3 handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py \
  --gammas 1.5,3.25,5.75
```

Expected behavior: `W_hat(0)` is `1` to floating precision and each requested
`W_hat(i gamma)` is near zero.

## Next Use

Once curve-specific low zero ordinates are available, run:

```bash
python3 handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py \
  --gammas gamma1,gamma2,gamma3
```

Then use the coefficients to replay the H1/H2 finite diagnostic with those
low residues removed. A stabilization improvement supports the oscillatory
profile interpretation; it does not prove tail control.
