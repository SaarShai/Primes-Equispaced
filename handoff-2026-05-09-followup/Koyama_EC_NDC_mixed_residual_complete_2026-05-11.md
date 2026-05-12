# Koyama EC-NDC mixed residual audit

Date: 2026-05-11
Outcome: **no normalization promoted**.

## Method

- Sweep source: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/Koyama_EC_NDC.csv`.
- a_p source: `handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv`.
- Requested max K: `100000`; rows available through K=`100000`.
- Product table max prime: `99991`.
- Convention: inverse EC local factor with `mu_E(p^2)=p`.
- `C_bad(E)` not guessed; all reported residual products are good-prime only.
- Promotion rule: require cross-curve ratio below `1.42083` and max within-curve CV below `0.08567129`.

## Limitation

All reported products are complete for their K checkpoints.

## Stability

| normalization | promoted | max within-K CV | cross-curve CV | cross-curve ratio | score | curve means (37a1, 11a1, 389a1) |
|---|---:|---:|---:|---:|---:|---|
| `D_mix_good` | False | 0.084975752 | 0.80138228 | 11.365809 | 0.88635803 | 0.28665988, 0.82354397, 0.072458014 |
| `D_2_good` | False | 0.084965682 | 0.80495901 | 10.955575 | 0.88992469 | 0.33659622, 0.99450979, 0.090776597 |

## K=100000 Rows

| curve | K | D*zeta(2) | p max | complete | good p count | C_mix | D_mix | C_2 | D_2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 37a1 | 100000 | 0.6178615552 | 99991 | True | 9591 | 2.180041222 | 0.2834173726 | 1.856576007 | 0.3327962619 |
| 11a1 | 100000 | 1.184097039 | 99991 | True | 9591 | 1.398920131 | 0.8464364855 | 1.158442487 | 1.022145728 |
| 389a1 | 100000 | 0.1927028966 | 99991 | True | 9591 | 2.643398323 | 0.0728996818 | 2.109907909 | 0.09133237325 |

## Verification

- Command: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 100000 --ap-table handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv --write-report handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md`.
- Wall time: `0.095s`.
- Rows computed: `15`.
- K=300000 command not run in this report: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 300000 --ap-table <complete-ap-table> --write-report <report.md>`.
- Reason: source sweep rows are available only through K=`100000`; K=300000 needs recomputing `D_K*zeta(2)` as well as extending the `a_p` table.

## Residual Rows

| curve | K | D*zeta(2) | p max | complete | C_mix | D_mix | C_2 | D_2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 37a1 | 1000 | 0.7063561658 | 1000 | True | 2.174859716 | 0.3247824035 | 1.852367765 | 0.3813260947 |
| 37a1 | 3000 | 0.6361784015 | 3000 | True | 2.183375644 | 0.291373774 | 1.859393511 | 0.342142961 |
| 37a1 | 10000 | 0.5983826346 | 10000 | True | 2.179941419 | 0.2744948233 | 1.856484447 | 0.3223203058 |
| 37a1 | 30000 | 0.5650544362 | 30000 | True | 2.179733086 | 0.2592310223 | 1.856316763 | 0.3043954823 |
| 37a1 | 100000 | 0.6178615552 | 99991 | True | 2.180041222 | 0.2834173726 | 1.856576007 | 0.3327962619 |
| 11a1 | 1000 | 1.21589614 | 1000 | True | 1.396598145 | 0.8706127421 | 1.156506036 | 1.051353043 |
| 11a1 | 3000 | 1.104174632 | 3000 | True | 1.399790614 | 0.7888141419 | 1.159124488 | 0.9525936544 |
| 11a1 | 10000 | 1.111223955 | 10000 | True | 1.399591003 | 0.7939633456 | 1.159001855 | 0.9587766837 |
| 11a1 | 30000 | 1.144599179 | 30000 | True | 1.399448284 | 0.8178931594 | 1.158876751 | 0.9876798182 |
| 11a1 | 100000 | 1.184097039 | 99991 | True | 1.398920131 | 0.8464364855 | 1.158442487 | 1.022145728 |
| 389a1 | 1000 | 0.1878717966 | 1000 | True | 2.62526499 | 0.07156298405 | 2.095650968 | 0.08964841927 |
| 389a1 | 3000 | 0.2162057165 | 3000 | True | 2.643980693 | 0.08177280459 | 2.110448231 | 0.1024454016 |
| 389a1 | 10000 | 0.1648923938 | 10000 | True | 2.640991702 | 0.06243578641 | 2.10796387 | 0.07822353891 |
| 389a1 | 30000 | 0.1946226918 | 30000 | True | 2.643654332 | 0.07361881221 | 2.11011415 | 0.09223325281 |
| 389a1 | 100000 | 0.1927028966 | 99991 | True | 2.643398323 | 0.0728996818 | 2.109907909 | 0.09133237325 |

## Confidence

Medium for normalization decisions: formulas were implemented directly from the sprint theory note, and the residual products are complete for the source sweep checkpoints through K=100000. High for the negative promotion decision at this checkpoint.

