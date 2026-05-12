---
schema_version: 1
title: "GL1 Sharp Perron Boundary"
date: 2026-05-11
type: theorem-boundary
tier: working
status: SHARP_BLOCKED_PROFILE_MODE_ONLY
confidence: 0.90
tags: [gl1, perron, sharp-cutoff, moving-pv, smoothing]
---

# GL1 Sharp Perron Boundary

Status: `SHARP_BLOCKED_PROFILE_MODE_ONLY`.

## Verdict

The local target residue is closed:

```text
Res_(w=0) K^w/(w L(rho+w,chi))
 = logK/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2).
```

Sharp cutoff still requires:

```text
GL1-ActualMovingShellPV(chi,rho)
```

or a stronger dyadic critical weighted reciprocal-derivative theorem.

Global simplicity is not enough. If all off-target zeros are simple, the
simple-zero moving PV sum remains:

```text
sum_(lambda != rho)
  exp(i(gamma_lambda-gamma_rho)logK)
  / ((i(gamma_lambda-gamma_rho))L'(lambda,chi))
 = o(logK).
```

## Publishable Weaker Mode

Smoothed or finite-filtered kernels can be written as an honest profile
theorem:

```text
c_W,K(chi,rho)
 = target residue + explicit retained off-target profile + tail/error.
```

With `SmoothOffTargetControl(W;chi,rho)`, this becomes a conditional smoothed
leading theorem for the smoothed coefficient only.

It does not transfer to the sharp cutoff. The smoothing limit requires uniform
control of the same harmonic tail that sharp Perron is missing.

## Next Actions

1. Prove or source-hunt `GL1-ActualMovingShellPV`.
2. Separately package `GL1-Sharp-Rectangle` and trivial-residue truncation;
   those are easier but not enough.
3. State fixed-smoothed profile theorem with the tail retained.

## Boundary

Do not use:

- target-zero simplicity;
- LI/spacing alone;
- fixed smooth filtering;
- H1 DPMV progress;
- EC numerics;

as proof of the sharp cutoff.

