# Koyama EC-NDC Extended Sweep

Date: 2026-05-11

## Status

`NUMERICAL; complete through K=1000000`

## Claim

No normalization promoted.

Promotion rule: cross-curve ratio `< 1.42083` and max within-curve CV `< 0.08567129`.

## Evidence

| normalization | promoted | max within-K CV | cross-curve CV | cross-curve ratio | curve means (37a1, 11a1, 389a1) |
|---|---:|---:|---:|---:|---|
| `D_zeta2_over_L2E_rank` | False | 0.09669211205 | 0.1443648383 | 1.423821385 | 1.646124453, 1.156131288, 1.523157118 |
| `D_zeta2` | False | 0.09670092958 | 0.5934458082 | 5.853565279 | 0.6281479448, 1.156131288, 0.1975089084 |
| `D_2_good` | False | 0.09601279473 | 0.8011347847 | 10.64951807 | 0.338404467, 0.9979918167, 0.09371239241 |
| `D_mix_good` | False | 0.09601227645 | 0.7976745445 | 11.04841098 | 0.2881980436, 0.8264293847, 0.07480074612 |

Complete products: all CSV rows have `product_complete=True`; largest prime used is `999983`.

At K=1000000:

| curve | D*zeta2 | D*zeta2/L2E^rank | D_mix_good | D_2_good | L2E_partial |
|---|---:|---:|---:|---:|---:|
| 37a1 | 0.64436487481 | 1.68869590178 | 0.295574402072 | 0.347071221404 | 0.381575435891 |
| 11a1 | 1.10536976744 | 1.10536976744 | 0.789991412357 | 0.953983875518 | 0.546048009149 |
| 389a1 | 0.196892734571 | 1.51845034256 | 0.0745156770652 | 0.0933570189209 | 0.360092891737 |

## Commands/Timings

- Command: `python3 handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py --max-k 1000000 --workers 6`
- load_inputs: `0.216s`
- extend_ap: `267.953s`
- compute_rows: `3.814s`
- write_outputs: `0.001s`
- total_self_reported: `272.012s`

K=1000000 attempt: included in this run.

## CSV Schema

`curve,K,rank,c_K,E_K,D_K,D_K_zeta2,L2E_partial,L2E_rank_power,D_zeta2_over_L2E_rank,C_mix_good,D_mix_good,C_2_good,D_2_good,p_max,good_prime_count,ap_cache_max,ap_extended_count,product_complete`

Definitions: `D_K_zeta2` is raw `D*zeta(2)`; `D_zeta2_over_L2E_rank` uses the complete partial `L(E,2)^rank`; `D_mix_good` and `D_2_good` use complete good-prime products only.

## Verification

- Existing cache: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/Koyama_EC_NDC_ap_table_100000.csv`.
- Existing base sweep: `/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-09-followup/Koyama_EC_NDC.csv`.
- Output CSV rows: `21`.
- Output max K: `1000000`.
- Product max prime: `999983`.
- 100k raw-D cross-checks vs existing `Koyama_EC_NDC.csv`:
  - `11a1` K=`1000` abs diff `5.107e-15`
  - `11a1` K=`3000` abs diff `6.217e-15`
  - `11a1` K=`10000` abs diff `5.107e-15`
  - `11a1` K=`30000` abs diff `8.882e-16`
  - `11a1` K=`100000` abs diff `2.198e-14`
  - `37a1` K=`1000` abs diff `2.998e-15`
  - `37a1` K=`3000` abs diff `6.328e-15`
  - `37a1` K=`10000` abs diff `1.366e-14`
  - `37a1` K=`30000` abs diff `1.987e-14`
  - `37a1` K=`100000` abs diff `3.875e-14`
  - `389a1` K=`1000` abs diff `5.274e-16`
  - `389a1` K=`3000` abs diff `5.274e-16`
  - `389a1` K=`10000` abs diff `5.551e-17`
  - `389a1` K=`30000` abs diff `2.193e-15`
  - `389a1` K=`100000` abs diff `8.743e-15`

## Changed Files

- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.csv`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md`

## Risks

- Float arithmetic replaces the original mpmath output; 100k raw cross-checks are included.
- No bad-prime-adjusted `D_mix`/`D_2` variant is reported; no finite bad-prime residual was derived here.
- This is a sharp cutoff computation at `rho=1`; it does not test smoothed or complex-zero variants.
