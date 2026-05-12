---
schema_version: 1
title: "H1 breakthrough proof wave acceptance checks"
date: 2026-05-11
type: verification
tier: working
status: COMPLETE
confidence: 0.9
tags: [ec-ndc, h1, breakthrough-wave, verification]
---

# H1 Breakthrough Proof Wave Acceptance Checks

## Commands

From `/Users/za/Documents/Farey NOW/primes-equispaced`:

```bash
git diff --check
```

Result: pass.

```bash
python3 -m py_compile handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py
```

Result: pass.

```bash
python3 handoff-2026-05-11-h1-breakthrough-proof-wave/kernel_filter_moments.py --gammas 1.5,3.25,5.75
```

Result: pass. Residuals:

```text
W_hat(i*1.5) abs=1.383e-16
W_hat(i*3.25) abs=4.224e-17
W_hat(i*5.75) abs=8.674e-18
```

```bash
rg -n "^status:" handoff-2026-05-11-h1-breakthrough-proof-wave/*.md
```

Result: every new wave Markdown deliverable has a frontmatter status.

From `/Users/za/Documents/Farey NOW`:

```bash
./te doctor
```

Result: pass, `"ok": true`.

```bash
./te wiki index
```

Result after this acceptance note: pass, `indexed: 3568`.

```bash
./te wiki lint --strict --fail-on-error
```

Result after this acceptance note: expected existing corpus failure:

```text
broken_links: 26
duplicate_titles: 1910
warnings: 0
pages: 3568
new_h1_breakthrough_broken_links: []
new_h1_breakthrough_duplicate_titles: []
```

Unsafe-phrase scan over `HANDOFF.md`, claim ledger, `log.md`, and this wave:

```text
Only qualified/historical hits remained:
- corrected GL(1) constant appears with conditional/dependency-closed wording;
- old B+ target appears only in the qualified sentence that it is false.
```

## Acceptance Decision

Accepted as a claim-safe `RIGOROUS_REDUCTION`. No closed EC smoothing claim,
fixed-weight H1 claim, H2 closure claim, or rank-zero constant limit was
promoted.
