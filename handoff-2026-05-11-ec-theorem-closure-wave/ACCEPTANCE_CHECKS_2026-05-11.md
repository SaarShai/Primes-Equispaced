---
schema_version: 1
title: "Acceptance checks for EC theorem closure wave"
date: 2026-05-11
type: verification
tier: working
status: PASS_WITH_EXISTING_LINT_FAILURES
confidence: 0.9
tags: [verification, ec-ndc, smoothing]
---

# Acceptance Checks

## Passed

```bash
git diff --check
python3 -m py_compile handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
python3 handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
./te doctor
./te wiki index
```

`./te wiki index` indexed `3537` pages after the diagnostic review and this
acceptance note were added.

## Strict Wiki Lint

```bash
./te wiki lint --strict --fail-on-error
```

Exit: `1`.

Reason: existing corpus failures, not this wave.

Summary from `/tmp/farey_te_lint_20260511.json`:

```text
broken_links: 26
duplicate_titles: 1910
warnings: 0
pages: 3537
new_wave_broken_links: []
new_wave_duplicate_titles: []
```

## Stale Claim Grep

Command family:

```bash
rg -n -F -e <stale-claim-phrases> HANDOFF.md L2_facts/farey-claim-ledger.md log.md handoff-2026-05-11-ec-theorem-closure-wave
```

No unqualified new-wave promotion was found. Remaining hits are qualified or
historical:

- conditional GL(1) Koyama limit language in handoff/ledger/log;
- historical false-positivity language for B+;
- no closed-NDC wording and no closed EC smoothing claim.
