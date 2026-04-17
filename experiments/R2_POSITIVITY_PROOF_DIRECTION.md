# R₂ Positivity: Proof Direction
**Date:** 2026-04-13
**Status:** Proof direction identified. Needs formalization.

## Definition
R₂ = Σ_{old fracs f_k} [(f_k - k/(n_old-1))² - (f_k - j_k/(n_new-1))²]

where j_k = rank of f_k in the new (finer) Farey sequence.

Equivalently: R₂ = W_old(grid_{n_old}) - W_old(grid_{n_new})
= L² error of old fracs on coarse grid minus L² error on fine grid

## Numerical evidence
- R₂ ≥ 0 for ALL primes p = 3..79 tested
- R₂ = 0 at p = 3 (degenerate: F_2 → F_3 are both perfectly placed)
- R₂ > 0 for all p ≥ 5
- At p=71: 54% of old fracs move FARTHER, but net L² still improves

## Proof sketch
**Theorem:** For N ≥ 5 prime, R₂(N) > 0.

**Proof direction:**
1. Old fracs f_1 < f_2 < ... < f_n are elements of F_{N-1} on [0,1]
2. They have discrepancy D_{N-1} = max_k |f_k - k/n| = O(log N/N)
3. In F_N (n_new > n_old), each f_k gets new rank j_k
4. R₂ = Σ_k [(f_k - k/(n-1))² - (f_k - j_k/(m-1))²]

**Key lemma:** For any monotone sequence x_1 < ... < x_n on [0,1] with discrepancy D,
the L² error to n-point uniform grid is Σ (x_k - k/n)².
Going to m-point grid (m > n) with rank-based assignment:
L²_m ≤ L²_n (finer grid → smaller error)

**Proof of key lemma:** The rank-based assignment on finer grid is equivalent to 
a finer quantile approximation. By the quantile function theory:
- The empirical distribution function F_n(t) = #{k: x_k ≤ t}/n
- L² error = ∫₀¹ (F_n(t) - t)² dt (approximately)
- Finer grid evaluates F_n at more points → better Riemann sum approximation

Alternatively: use Parseval. The L² error on n-point grid is determined by
Fourier coefficients of the empirical distribution at frequencies 1..n.
Finer grid captures more frequencies → smaller residual.

**What makes this nontrivial:** R₂ > 0 is NOT guaranteed for arbitrary sequences.
It uses the fact that Farey fractions are well-distributed (low discrepancy).
For a badly distributed sequence, finer grid could increase L² error under
rank-based (not nearest-point) assignment.

## For Lean formalization
This could be formalized as:
∀ N ≥ 5 prime, R₂(F_{N-1} → F_N) > 0
using the injection principle (each new fraction enters one gap) and
the equidistribution bound D_{N} ≤ C log N/N.
