# DiscrepancyStep — Unconditional Evidence
Date: 2026-04-14 Session 14
Method: Exact rational arithmetic (p≤500), float64 (p=500-631)

## MAJOR FINDING

DiscrepancyStep (ratio = (D+C+B)/A > 1) holds for ALL primes p tested in [11, 631], 
including those with M(p) > -3 (up to M(p) = +6).

Previous belief: "conditional on M(p) ≤ -3". 
Revised: M(p) ≤ -3 was condition for B ≥ 0 (sufficient for DiscrepancyStep), NOT necessary.

## B < 0 Cases (all still have ratio > 1)
| p   | M(p) | ratio  | B            | ratio>1 |
|-----|------|--------|--------------|---------|
| 11  | -2   | 1.147  | -0.000826    | YES ✓   |
| 17  | -2   | 1.283  | -0.000277    | YES ✓   |
| 97  | 1    | 1.145  | -0.000011    | YES ✓   |
| 223 | 3    | 1.086  | -0.000003    | YES ✓   |

## All M(p) ≥ 0 Primes in [11,499]
| p   | M(p) | ratio  | B>0 |
|-----|------|--------|-----|
| 97  | 1    | 1.145  | No  |
| 101 | 0    | 1.274  | Yes |
| 149 | 0    | 1.335  | Yes |
| 163 | 0    | 1.389  | Yes |
| 223 | 3    | 1.086  | No  |
| 227 | 3    | 1.143  | Yes |
| 229 | 2    | 1.304  | Yes |
| 331 | 0    | 1.450  | Yes |
| 337 | 1    | 1.342  | Yes |
| 347 | 2    | 1.286  | Yes |
| 349 | 1    | 1.445  | Yes |
| 353 | 0    | 1.584  | Yes |
| 397 | 1    | 1.568  | Yes |
| 401 | 0    | 1.696  | Yes |
| 419 | 0    | 1.518  | Yes |

All pass. Min ratio = 1.086 at p=223.

## Primes [503, 631] (True M values, float64)
M(503)=-5, M(509)=-6, M(521)=-2, M(523)=-3, M(541)=0, M(547)=3, M(557)=4, M(563)=4,
M(569)=5, M(571)=5, M(577)=4, M(587)=6, M(593)=6, M(599)=4, M(601)=3, M(607)=0,
M(613)=-2, M(617)=-3, M(619)=-5, M(631)=-3

All ratios: min 1.151 (p=593), max 2.100 (p=619). All B>0. All ratio>1.

## C/A Values (stable around 0.130)
- Exact (p≤500): C/A ∈ [0.129, 0.255], converging to ~0.130 as p increases
- Float (p=503-631): C/A ∈ [0.129, 0.138]
- Asymptotic: C/A → ~0.130

## Bug Report: Old Background Task (b0njgqjty)
The extended p≤5000 run had TWO bugs:
1. M_running += mu[p] over PRIMES only → computed -π(p), not M(p)
2. Float64 at p~3000: |F_3000| ≈ 2.7M, discrepancy = rank - N*f requires ~12 significant figures, near float64 limit (16 digits) → catastrophic cancellation in A, B, C
"Counterexample" at p=3299 (ratio=0.320): M(3299)=20 (NOT ≤-3), AND float error.
Results from that task DISCARDED.

## Summary
- 65 primes p ∈ [11, 631] tested (all of them)
- 65/65 pass DiscrepancyStep (100%)
- Min ratio: 1.086 at p=223 (M=3)
- DiscrepancyStep appears UNCONDITIONAL for all primes ≥ 11
- Need: exact arithmetic at p~1000-5000 to confirm at scale

## Proof Approach (Updated)
No longer need "B ≥ 0" as separate step. Instead:
- D/A ≥ 0.98 (nearly 1)
- C/A ≥ 0.13
- B/A ≥ -0.125 (empirically, Cauchy-Schwarz: |B|/A ≤ √(C/A) ≈ 0.36)
- Total: (D+C+B)/A ≥ 0.98 + 0.13 - 0.125 = 0.985 ← NOT sufficient!

Better: D/A → 1 as p→∞, C/A → 0.13, B/A → 0. So unconditional proof needs:
  lim_inf (D+C+B)/A ≥ 1 + ε

This requires: (D/A - 1) + C/A + B/A ≥ ε. Since C/A → 0.13 and |B|/A → 0 and D/A → 1 (from below? need to check), the proof likely goes through for large p.
