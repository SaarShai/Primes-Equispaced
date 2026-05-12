AUDIT_ONLY

# Dense S1 Agent Review

Confidence: `0.74`

## Verdict

No fatal flaw found in `DENSE_S1_RESIDUAL_DIAGNOSTICS.md` or its saved
`DENSE_S1_model_comparison.csv`.

The diagnostic is correctly scoped as finite evidence only. The CSV supports
the report's compact read:

| curve | zero | best BIC model | delta BIC | CV skill |
|---|---:|---|---:|---:|
| `37a1` | 1 | `damped_zero_plus_1_over_logK` | `-53.38535351679252` | `0.41457125053899757` |
| `37a1` | 2 | `damped_zero_plus_1_over_logK` | `-10.440914827119173` | `0.18287378801577858` |
| `389a1` | 1 | `persistent_zero` | `-53.39955808290722` | `0.40207280160476244` |
| `389a1` | 2 | `damped_zero` | `-28.807945449735143` | `0.26665917238914072` |

Audit read: visible zero-frequency structure, but no robust isolation of
`1/log K` damping. This remains compatible with the theorem-closure synthesis:
S1/H2 is a conditional proof-candidate direction, while fixed-curve EC
stabilization remains blocked by H1 reciprocal-pole residues and exact source
closure.

## Dependencies

- `../start.md`
- `HANDOFF.md`
- `L2_facts/farey-claim-ledger.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv`
- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_metadata.csv`
- `handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md`

Boot note: `./te` and `token-economy.yaml` were absent in this project root;
`L0_rules.md` and `L1_index.md` were present and read.

## Checks

- Script AST parse: `OK`.
- Recorded SHA-256 hashes match the diagnostic report for script, comparison
  CSV, and residual-grid CSV.
- No `__pycache__` was created in the theorem-closure handoff directory.
- I did not rerun `DENSE_S1_residual_diagnostics.py`, because it rewrites CSV
  outputs outside this owned review file.

## Do Not Promote Unless

- Treat this diagnostic only as `AUDIT_ONLY` finite evidence.
- Do not promote EC smoothing, cross-curve universality, BSD evidence, or H2 package
  language from this file.
- Do not claim damping is numerically isolated; `389a1` zero 1 prefers the
  persistent model by BIC.
- Do not use product-level theorem language until H1 reciprocal-pole control,
  exact S1/Sym2/H2 source closure, bad-prime constants, and theorem mode
  selection are all closed.

## Changed Files

- `handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_AGENT_REVIEW.md`

## Commands Run

```bash
sed -n '1,220p' ../start.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,220p' L1_index.md
wc -l HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
git status --short
rg --files | rg 'DENSE_S1_(residual_diagnostics\.py|model_comparison\.csv|RESIDUAL_DIAGNOSTICS\.md|AGENT_REVIEW\.md)'
sed -n '1,220p' HANDOFF.md
sed -n '1,220p' L2_facts/farey-claim-ledger.md
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_RESIDUAL_DIAGNOSTICS.md
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,180p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
sed -n '181,380p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py
sed -n '1,80p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv
sed -n '1,80p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_metadata.csv
shasum -a 256 handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_grid.csv
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import ast,pathlib; ast.parse(pathlib.Path("handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_residual_diagnostics.py").read_text()); print("ast_parse_ok")'
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import csv, collections; rows=list(csv.DictReader(open("handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_model_comparison.csv"))); groups=collections.defaultdict(list); [groups[(r["curve"],r["zero_index"])].append(r) for r in rows]; for key in sorted(groups): b=min(groups[key], key=lambda r: float(r["bic"])); print(key[0], key[1], b["model"], b["delta_bic_vs_constant"], b["cv_skill_vs_constant"])'
find . -name '__pycache__' -type d -path '*handoff-2026-05-11-ec-theorem-closure-wave*' -maxdepth 4
ls -la handoff-2026-05-11-ec-theorem-closure-wave | sed -n '1,120p'
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_AGENT_REVIEW.md
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/DENSE_S1_AGENT_REVIEW.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```
