# Koyama EC-NDC mixed residual audit

Date: 2026-05-10
Outcome: **no normalization promoted**.

## Method

- Sweep source: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/Koyama_EC_NDC.csv`.
- a_p source: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table.csv`.
- Requested max K: `100000`; rows available through K=`100000`.
- Product table max prime: `541`.
- Convention: inverse EC local factor with `mu_E(p^2)=p`.
- `C_bad(E)` not guessed; all reported residual products are good-prime only.
- Promotion rule: require cross-curve ratio below `1.42083` and max within-curve CV below `0.08567129`.

## Limitation

The existing `a_p` table stops at p=541, so these are **truncated diagnostics**, not real K=100000 Euler products. No K=300000 product was attempted because the K=100000 product is not complete from the available table.

## Stability

| normalization | promoted | max within-K CV | cross-curve CV | cross-curve ratio | score | curve means (37a1, 11a1, 389a1) |
|---|---:|---:|---:|---:|---:|---|
| `D_mix_good_truncated` | False | 0.16197044 | 0.79989813 | 11.380239 | 0.96186857 | 0.2414961, 0.68973076, 0.060607756 |
| `D_2_good_truncated` | False | 0.16197044 | 0.80359408 | 10.973293 | 0.96556452 | 0.28349382, 0.83291537, 0.075903868 |

## K=100000 Rows

| curve | K | D*zeta(2) | p max | complete | good p count | C_mix | D_mix | C_2 | D_2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 37a1 | 100000 | 0.6178615552 | 541 | False | 99 | 2.947286699 | 0.2096374117 | 2.510665856 | 0.2460946978 |
| 11a1 | 100000 | 1.184097039 | 541 | False | 99 | 1.89345374 | 0.6253635959 | 1.567954355 | 0.755185912 |
| 389a1 | 100000 | 0.1927028966 | 541 | False | 99 | 3.578873658 | 0.05384456538 | 2.857660687 | 0.06743379208 |

## Verification

- Command: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 100000 --write-report Koyama_EC_NDC_mixed_residual_2026-05-10.md`.
- Wall time: `0.003s`.
- Rows computed: `15`.
- K=300000 command not run: `python3 Koyama_EC_NDC_mixed_residual.py --max-k 300000 --write-report Koyama_EC_NDC_mixed_residual_2026-05-10.md`.
- Reason: no complete K=100000 mixed product from available `a_p` source; K=300000 would be table-truncated to p=541.

## Residual Rows

| curve | K | D*zeta(2) | p max | complete | C_mix | D_mix | C_2 | D_2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 37a1 | 1000 | 0.7063561658 | 541 | False | 2.28295846 | 0.3094038627 | 1.94475341 | 0.3632111724 |
| 37a1 | 3000 | 0.6361784015 | 541 | False | 2.457804301 | 0.2588401368 | 2.093697006 | 0.3038540914 |
| 37a1 | 10000 | 0.5983826346 | 541 | False | 2.636133363 | 0.2269925501 | 2.245607809 | 0.2664680058 |
| 37a1 | 30000 | 0.5650544362 | 541 | False | 2.788924839 | 0.2026065487 | 2.375764248 | 0.2378411228 |
| 37a1 | 100000 | 0.6178615552 | 541 | False | 2.947286699 | 0.2096374117 | 2.510665856 | 0.2460946978 |
| 11a1 | 1000 | 1.21589614 | 541 | False | 1.46666296 | 0.8290221906 | 1.214532221 | 1.001123 |
| 11a1 | 3000 | 1.104174632 | 541 | False | 1.578990855 | 0.6992913406 | 1.307550079 | 0.8444606822 |
| 11a1 | 10000 | 1.111223955 | 541 | False | 1.69355651 | 0.6561481407 | 1.402421009 | 0.7923611725 |
| 11a1 | 30000 | 1.144599179 | 541 | False | 1.791715807 | 0.6388285318 | 1.483705962 | 0.7714461004 |
| 11a1 | 100000 | 1.184097039 | 541 | False | 1.89345374 | 0.6253635959 | 1.567954355 | 0.755185912 |
| 389a1 | 1000 | 0.1878717966 | 541 | False | 2.772183615 | 0.06777032935 | 2.21353445 | 0.08487412363 |
| 389a1 | 3000 | 0.2162057165 | 541 | False | 2.984497935 | 0.07244291041 | 2.383063287 | 0.09072596508 |
| 389a1 | 10000 | 0.1648923938 | 541 | False | 3.201041913 | 0.05151210085 | 2.555969421 | 0.06451266296 |
| 389a1 | 30000 | 0.1946226918 | 541 | False | 3.386575742 | 0.05746887318 | 2.704114559 | 0.07197279833 |
| 389a1 | 100000 | 0.1927028966 | 541 | False | 3.578873658 | 0.05384456538 | 2.857660687 | 0.06743379208 |

## Confidence

Low-to-medium for normalization decisions: formulas were implemented directly from the sprint theory note, but the product is truncated at p=541 for every available checkpoint. High for the negative promotion decision on this truncated diagnostic.
