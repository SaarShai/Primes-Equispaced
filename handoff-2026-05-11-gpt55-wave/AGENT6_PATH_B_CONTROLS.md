---
schema_version: 1
title: "Agent 6 Path B rank/conductor controls"
date: 2026-05-11
agent: "GPT-5.5 xhigh Agent 6"
status: COMPUTE_BLOCKED
confidence: 0.93
dependencies:
  - "External machine with gp on PATH."
  - "pari-elldata installed so ellinit(\"5077a1\") and ellsearch(N) work."
  - "Computed B1/B2 selected-control CSV rows with the exact path_b_20forms.py normalization."
sources:
  - HANDOFF.md
  - handoff-2026-05-09-followup/KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md
  - koyama-shared/results/PATH_B_CONTROL_RUNNER_2026-05-11.md
  - koyama-shared/scripts/path_b_control_queue_runner.py
  - koyama-shared/results/PATH_B_MOONSHOT_DECISION_2026-05-11.md
  - koyama-shared/results/PATH_B_CONTROL_QUEUE_2026-05-10.md
---

# Agent 6 Path B Controls

External theorem claims: none. This packet makes only local computation and
runner-output claims, so no primary theorem quote/page/eq is invoked.

## Decision

No rank-survival claim is available. The control path is executable, but the
local environment is blocked and the control matrix is incomplete.

Observed locally:

```text
python3 -m py_compile koyama-shared/scripts/path_b_control_queue_runner.py: pass
gp: absent
pari_elldata_dirs: none-found
loaded_csvs: koyama-shared/data/PATH_B_20FORMS.csv only
EC rows: 19; Delta excluded
B1 missing: rank0 x3, rank1 x3
B2 missing: rank0 x2, rank1 x2, rank2 x2
```

Current diagnostic remains a failure-to-promote result:

| model | rank beta | 95% CI | P(beta<=0) | LOO beta | max leverage | verdict |
|---|---:|---:|---:|---:|---:|---|
| rank only | 0.585860 | [0.238656, 0.845991] | 0.00005 | [0.358825, 0.621127] | 0.333333 | confounded screen |
| rank+logN | -0.677256 | [-1.221404, 0.091164] | 0.95515 | [-0.786934, -0.253343] | 0.533428 | fail |
| interaction | 0.001435 | [-0.687660, 0.737488] | 0.60730 | [-0.317877, 0.194992] | 0.870262 | fail |

## Executable External Packet

Run only on a GP/PARI machine:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py --emit-gp all
python3 koyama-shared/scripts/path_b_control_queue_runner.py --discover all > /tmp/path_b_b1_b2_discovery.csv
python3 koyama-shared/scripts/path_b_control_queue_runner.py --select-discovery /tmp/path_b_b1_b2_discovery.csv --select-band B1 > /tmp/path_b_B1_selected.txt
python3 koyama-shared/scripts/path_b_control_queue_runner.py --select-discovery /tmp/path_b_b1_b2_discovery.csv --select-band B2 > /tmp/path_b_B2_selected.txt
```

Build the selected-forms CSV from the runner selections:

```bash
printf 'label,rank,weight,conductor\n' > /tmp/path_b_selected_forms.csv
awk -F, '/nearest_target_distance/ {gsub(/^[[:space:]]+/, "", $1); print $1 "," $2 ",2," $3}' \
  /tmp/path_b_B1_selected.txt /tmp/path_b_B2_selected.txt >> /tmp/path_b_selected_forms.csv
```

Compute selected rows with the existing normalization, changing only `FORMS`
and `OUT_CSV` in memory:

```bash
python3 - <<'PY'
import csv, runpy
from pathlib import Path

selected = Path("/tmp/path_b_selected_forms.csv")
out = Path("koyama-shared/data/AGENT6_PATH_B_SELECTED_CONTROLS.csv")
forms = []
with selected.open(newline="") as fh:
    for row in csv.DictReader(fh):
        forms.append((row["label"], int(row["rank"]), int(row["weight"]), int(row["conductor"])))
if len(forms) != 12:
    raise SystemExit(f"expected 12 selected lower-rank controls, got {len(forms)}")
ns = runpy.run_path("koyama-shared/scripts/path_b_20forms.py", run_name="agent6_path_b")
ns["FORMS"] = forms
ns["OUT_CSV"] = out
ns["main"]()
PY
```

Then gate the result:

```bash
python3 koyama-shared/scripts/path_b_control_queue_runner.py \
  --controls-csv koyama-shared/data/AGENT6_PATH_B_SELECTED_CONTROLS.csv \
  --current-diagnostic
```

The selected-control CSV must have:

```text
label,rank,weight,conductor,E_C1,E_C1_sq,N_zeros,error
```

Reject any row with `weight != 2`, `N_zeros < 200`, nonempty `error`, changed
`K=10^4`, changed `rho=1+i gamma`, changed `mu_E(p)=-a_p`, changed
`mu_E(p^2)=p`, or changed denominator `log(K)+EulerGamma`.

## Acceptance Gates

B1 is decision-complete only with 3 rank-0 and 3 rank-1 controls in
`350 <= conductor <= 650`, against the existing rank-2 rows
`389a1,433a1,446d1,571b1`.

B2 is decision-complete only with 2 rank-0, 2 rank-1, and 2 rank-2 controls in
`4500 <= conductor <= 5600`, against `5077a1`.

Required fits:

```text
B1:       y ~ 1 + rank
B1:       y ~ 1 + rank + centered_logN
B2:       y ~ 1 + rank
B2:       y ~ 1 + rank + centered_logN
B1+B2:    y ~ 1 + rank + centered_logN
B1+B2:    y ~ 1 + rank + centered_logN + rank:centered_logN
B1+B2:    y ~ 1 + rank + conductor_tier
```

For every accepted rank sentence: rank beta `> 0`, bootstrap 95% CI lower
endpoint `> 0`, `P(beta <= 0) <= 0.025`, every LOO rank beta `> 0`, and max
leverage `< 0.50`, with seed `20260510`, `B=20000`, row bootstrap.

## Do not promote unless

- GP preflight succeeds and confirms `ellsearch(389)` plus `5077a1` metadata.
- The new CSV contains exactly the 12 lower-rank selected controls above.
- B1 and B2 are both complete; incomplete matrices remain `COMPUTE_BLOCKED`.
- The additive conductor-controlled B1+B2 model passes all gates.
- The archived runner output shows no row parse warnings, no singular LOO, and
  no leverage breach.
- If only B1 passes, say "local rank-2 evidence"; if B2 fails/incomplete, do
  not mention rank-3 survival; if only the interaction model is positive, say
  "conductor-dependent slope", not isolated rank.

## Verdict

Precise blockage: this checkout can audit and gate controls, but cannot compute
B1/B2 because `gp`, `pari-elldata`, and the 12 selected lower-rank control rows
are absent. The next successful artifact is
`koyama-shared/data/AGENT6_PATH_B_SELECTED_CONTROLS.csv` plus a passing runner
transcript; until then Path B remains conductor-confounded.
