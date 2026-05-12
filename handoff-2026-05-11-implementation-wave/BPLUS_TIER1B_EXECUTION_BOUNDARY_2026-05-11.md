---
schema_version: 1
title: "B+ Tier 1B Execution Boundary"
date: 2026-05-11
type: compute-boundary
tier: working
status: CLASSIFICATION_ONLY
confidence: 0.89
tags: [b-plus, sign-cluster, mertens-restricted, finite-compute]
---

# B+ Tier 1B Execution Boundary

Status: `CLASSIFICATION_ONLY`.

## Verdict

Lean-canonical B+ Mertens-restricted positivity is false.

Counterexamples:

```text
p=237733, M(p)=-20, B(p)=-3.018492026640170e10
p=243799, M(p)=-3,  B(p)=-9.190201299936827e9
```

`T(p-1)` is not a sign proxy: `p=243799` has `T(p-1)<0` and `B(p)<0`.

## Next Compute

Run tier 1B bridge only after accepting the compute cost:

```text
237733 <= p <= 243799
p prime
M(p) <= -3
expected MR rows: 468
estimated workload: about 9.94 core-hours
```

Goal: classify maximal certified `B(p)` sign clusters in MR-prime order.

Do not run tier 1C until tier 1B answers whether the two negative anchors are
one sign run or separate islands.

## Implementation Boundary

The execution spec is already frozen in:

```text
handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md
```

This implementation wave does not launch the 9.94-core-hour sweep. It keeps
the computation as a bounded explicit job and forbids analytic positivity
revival.

## Boundary

Do not claim:

- B+ positivity;
- MERTENS-LB;
- `T` sign as a B sign proxy;
- boundaries from legacy `bprime_*` scans.

