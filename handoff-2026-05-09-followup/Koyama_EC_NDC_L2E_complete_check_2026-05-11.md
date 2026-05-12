# Koyama EC-NDC complete L2E proxy check

Date: 2026-05-11
Status: `NUMERICAL`; no normalization promoted.

## Purpose

The previous best EC-NDC proxy, `D*zeta(2)/L2E_partial^rank`, was computed
from the original 100-prime `a_p` table through `p=541`.  After generating
`Koyama_EC_NDC_ap_table_100000.csv`, this check recomputes the same proxy
through the complete prime set needed for `K=100000`.

## Command

```bash
python3 - <<'PY'
import csv, math, statistics
from collections import defaultdict
ZETA2=math.pi*math.pi/6
sweep=list(csv.DictReader(open('handoff-2026-05-09-followup/Koyama_EC_NDC.csv')))
ap=list(csv.DictReader(open('handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv')))
curves=['37a1','11a1','389a1']
ranks={'37a1':1,'11a1':0,'389a1':2}
L2={c:1.0 for c in curves}
for row in ap:
    p=int(row['p'])
    for c in curves:
        a=int(row[f'a_p({c})'])
        if row[f'reduction({c})']=='good':
            inv=1-a/(p*p)+1/(p**3)
        else:
            inv=1-a/(p*p)
        L2[c] *= 1/inv
print(L2)
PY
```

## Complete partial L2E values

| curve | rank | L2E through p=99991 |
|---|---:|---:|
| `37a1` | 1 | `0.3815755540590191` |
| `11a1` | 0 | `0.5460478178909267` |
| `389a1` | 2 | `0.36009310688533147` |

## Stability comparison

| normalization | max within-K CV | cross-curve CV | cross-curve ratio | promoted |
|---|---:|---:|---:|---:|
| `D/L2E_complete^rank` | `0.08567129247` | `0.14191492559` | `1.42129913293` | false |
| `D*zeta(2)/L2E_complete^rank` | `0.08567129247` | `0.14191492559` | `1.42129913293` | false |

The old 100-prime ratio was `1.42083`; the complete-table ratio is
`1.42129913293`.  Thus the earlier benchmark is not a `p=541` artifact, and
the `L2E^rank` proxy remains a numerical proxy only.

## Decision

No promotion.  The complete `L2E` proxy is still much better than the mixed
residual tested on 2026-05-11, but it remains short of the promotion rule and
has no accepted local-factor derivation as the EC NDC constant.
