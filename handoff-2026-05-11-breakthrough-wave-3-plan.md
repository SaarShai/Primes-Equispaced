---
schema_version: 1
title: "Breakthrough Wave 3 Plan"
date: 2026-05-11
type: plan
tier: working
status: EXECUTED
confidence: 0.84
tags: [breakthrough-wave-3, h1, reciprocal-derivative, h2, s1, gl1]
---

# Breakthrough Wave 3 Plan

## Summary

Wave 2 narrowed the live breakthrough surface. Do not broaden. The next wave
should attack the single highest-leverage theorem target:

```text
Fixed-curve GL2/EC negative first reciprocal derivative moment
with separated-zero plus bad-set budget strong enough to imply
R_E,1(T)=o(T^2)
for analytic-rank-one H1.
```

H2 made real progress in Wave 2: exact good-prime Sym2 finite part is
component source-closed with `kappa_sym=0`. Full H2 is now blocked by one named
S1 contour theorem:

```text
S1-CutPlane-LogGrowth(E,W,eta)
```

Wave 3 should be more surgical than Wave 2. Seven agents go after H1
reciprocal derivatives from different proof angles; two agents close or kill
the S1 cut-plane theorem; one agent keeps GL1 aligned with the H1 PV
obstruction. B+, DPAC, Delta, and EC numerics are out of scope unless a worker
needs them only as negative boundary context.

Output directory used:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/
```

No Koyama correspondence/email drafts touched.

## Agent Assignments

1. **Agent 01 - GL2/EC BFMT Adaptation Blueprint**
   Try to adapt the Bui-Florea-Milinovich negative discrete moment strategy
   from zeta to one fixed elliptic-curve/newform `L(E,s)`. Identify every
   place where zeta-specific input is used: approximate functional equation,
   mollifier length, ratios conjecture input, zero-density, pair-correlation,
   Gonek-type sums, or arithmetic diagonal.  
   Output: `AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md`.

2. **Agent 02 - Fixed-Curve Reciprocal Derivative Source Hunt**
   Search only for source-checked theorems that directly control
   `sum |L'(rho)|^{-1}`, negative moments of `L'(rho)`, or small-derivative
   tails for GL2/newform/elliptic-curve L-functions. Every external theorem
   claim must use `curl + pdftotext`, short quote, and page/equation.  
   Output: `AGENT02_FIXED_CURVE_RECIP_DERIV_SOURCE_HUNT_2026-05-11.md`.

3. **Agent 03 - Separated-Zero Theorem Candidate**
   Prove or reduce a theorem for separated simple zeros:
   for a dyadic set `F_T` with nearest-neighbor spacing at least `c/log T`,
   bound `sum_{gamma in F_T} |L'(E,1+i gamma)|^{-1}` sharply enough for H1.
   Separate unconditional, RH/GRH, pair-correlation, and RMT-only modes.  
   Output: `AGENT03_SEPARATED_ZERO_RECIP_BUDGET_2026-05-11.md`.

4. **Agent 04 - Bad-Set Complement Budget**
   Attack the complement `B_T` of clustered, near-multiple, or locally
   uncontrolled zeros. Convert close-pair counts, zero-density, simplicity
   proportions, minimum-modulus disks, and boundary caps into exact conditions
   for `sum_{gamma in B_T}|L'(rho)|^{-1}=o(T^2)`. Kill any route that only
   controls counts without reciprocal caps.  
   Output: `AGENT04_BAD_SET_COMPLEMENT_BUDGET_2026-05-11.md`.

5. **Agent 05 - Minimum-Modulus Local Factor Route**
   Focus on the local factorization
   `L(s)=(s-rho)g_rho(s)` and try to prove a quantitative lower bound on
   `|g_rho(rho)|=|L'(rho)|` from zero-free circles, Jensen/Cartan, Hadamard
   products, or subharmonic estimates. The deliverable must state exactly what
   exponent is achievable and whether it beats the rank-one H1 threshold.  
   Output: `AGENT05_MINIMUM_MODULUS_LOCAL_FACTOR_2026-05-11.md`.

6. **Agent 06 - Actual-Coefficient H1 PV Theorem Attempt**
   Continue Wave 2 Agent 03, but now prove or kill the exact dyadic theorem
   for `sum W_hat(i gamma)e^(i gamma u)/L'(E,1+i gamma)`. Use actual
   coefficients only. Distinguish pointwise moving-window, log-Cesaro,
   Besicovitch/profile, and product-average modes.  
   Output: `AGENT06_ACTUAL_COEFFICIENT_H1_PV_THEOREM_2026-05-11.md`.

7. **Agent 07 - H1 Finite-Box Paper Theorem Extraction**
   Turn Wave 2 Agent 04 into a compact theorem section with hypotheses named
   exactly as future papers should cite them. It must include central
   polynomial normalization, legal exponential heights, simple-zero
   reciprocal budget, multiple-zero effective-degree rule, and no-promotion
   boundaries.  
   Output: `AGENT07_H1_FINITE_BOX_THEOREM_SECTION_2026-05-11.md`.

8. **Agent 08 - S1 Cut-Plane Log-Growth Proof Attempt**
   Attack `S1-CutPlane-LogGrowth(E,W,eta)` directly. Try to legalize the S1
   endpoint contour shift: log growth on horizontals, left-edge decay,
   cut-lip integrability, local cut remainders, and truncation sequence.
   Source-check any imported automorphic logarithm theorem.  
   Output: `AGENT08_S1_CUTPLANE_LOG_GROWTH_2026-05-11.md`.

9. **Agent 09 - S1 Right-Branch Classification**
   Determine whether right-branch singularities for the exact S1 good-prime
   object are absent, finite and retainable, or an unavoidable obstruction.
   Produce a theorem statement that either proves `NoRightBranch_S1(E,eta)` or
   explicitly retains right-branch terms in H2.  
   Output: `AGENT09_S1_RIGHT_BRANCH_CLASSIFICATION_2026-05-11.md`.

10. **Agent 10 - GL1/H1 Actual PV Coupling**
    Compare the GL1 moving off-target PV and H1 actual-coefficient PV
    problems. Decide whether a single abstract theorem covers both, or whether
    the arithmetic coefficients force genuinely separate hypotheses.  
    Output: `AGENT10_GL1_H1_ACTUAL_PV_COUPLING_2026-05-11.md`.

## Shared Instructions

- Used `gpt-5.5` with `reasoning_effort=xhigh` for dispatch.
- Queue around the host thread limit; launch up to 6 workers first, then fill
  slots as agents complete.
- Each agent owns only its requested output file.
- Allowed statuses: `THEOREM_PROMOTED`, `RIGOROUS_REDUCTION`, `NO_GO`,
  `DIAGNOSTIC_ONLY`.
- Every external theorem claim requires `curl + pdftotext`, short quote, and
  page/equation.
- Analytic rank only; no BSD/algebraic-rank substitution.
- H2 branch damping must never be used as H1 reciprocal-pole damping.
- Numerical EC work remains diagnostic only until H1/H2 theorem closure.
- Do not rerun broad source hunts already killed by Wave 1 or Wave 2 unless
  there is a new, named theorem target.
- No Koyama correspondence/email drafts.

## Coordinator Integration

Integration artifacts written:

```text
DISPATCH_MANIFEST_2026-05-11.md
BREAKTHROUGH_WAVE_3_SYNTHESIS_2026-05-11.md
```

Then update:

```text
HANDOFF.md
index.md
L1_index.md
log.md
L2_facts/farey-claim-ledger.md
```

Update the claim ledger only for verified durable changes.

## Acceptance Criteria

The wave succeeds if it does at least one of:

- source-closes a theorem implying rank-one `R_E,1(T)=o(T^2)`;
- strictly reduces that H1 target to a named fixed-curve GL2/newform theorem
  with all bad-set terms explicit;
- proves `S1-CutPlane-LogGrowth(E,W,eta)` or replaces it with a retained-term
  H2 theorem that is actually legal;
- decisively kills BFMT adaptation, minimum-modulus, or actual-coefficient PV
  routes so future work stops circling them.

No theorem promotion appears without proof and citation protocol.
