---
schema_version: 1
title: "H1 residue-control acceptance checks"
date: 2026-05-11
type: verification
tier: working
status: COMPLETE
confidence: 0.9
tags: [ec-ndc, h1, residue-control, verification]
---

# H1 Residue-Control Acceptance Checks

## Commands

From `/Users/za/Documents/Farey NOW/primes-equispaced`:

```bash
git diff --check
```

Result: pass.

```bash
rg -n "^status:" handoff-2026-05-11-h1-residue-control-wave/*.md
```

Result: every new wave deliverable has a frontmatter status.

```bash
find handoff-2026-05-11-h1-residue-control-wave -name '*.py' -print
```

Result: no Python scripts in this wave; no compile step needed.

From `/Users/za/Documents/Farey NOW`:

```bash
./te doctor
```

Result: pass, `"ok": true`.

```bash
./te wiki index
```

Result: pass, `indexed: 3557`.

```bash
./te wiki lint --strict --fail-on-error
```

Result: expected existing corpus failure:

```text
broken_links: 26
duplicate_titles: 1910
warnings: 0
pages: 3557
new_h1_residue_broken_links: []
new_h1_residue_duplicate_titles: []
```

Stale-claim grep:

```text
Ran the standard unsafe-phrase scan over HANDOFF, the claim ledger, log, and
the new H1 residue-control wave directory.
```

Result: only qualified/historical/no-promotion hits:

- The corrected GL(1) constant appears only with conditional/dependency-closed
  wording.
- The old B+ target appears only in the qualified sentence that it is false.
- H2-theorem wording appears only in no-promotion or mode-matching warnings.
- Rank-zero constant-limit wording appears only in a "do not call it" rule.

## Acceptance Decision

Accepted as a claim-safe `RIGOROUS_REDUCTION`. No closed EC smoothing claim,
pointwise H1 claim, closed H2 claim, or rank-zero constant limit was promoted.
