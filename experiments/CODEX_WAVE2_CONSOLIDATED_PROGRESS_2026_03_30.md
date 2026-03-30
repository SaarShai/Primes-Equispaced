# Codex Consolidated Progress Since Wave 2 Handoff

## Scope

This memo consolidates all work I have done since the Wave 2 handoff in

`/Users/saar/Documents/Codex reviewer/new handoff/CODEX_HANDOFF_WAVE2.md`.

The focus was the remaining analytical gap around `B >= 0` for the
`M(p) <= -3` prime class, with special attention to the `M(p) = -3` subclass.

The main outcome is that the problem now looks much more concrete:

- the `alpha` term has an exact weighted-Mertens formula
- the Abel correction has an exact kernel decomposition
- the first nine kernels `K_1,...,K_9` are now explicit
- on the tested `M(p) = -3` range up to `431`, `K_2,...,K_9` stayed positive

I do **not** claim that this closes the proof yet. The new material sharpens the
remaining obstacle and suggests a more promising route than the original
norm-only ratio approach.

---

## Files Produced or Updated

Research notes:

- `CODEX_WAVE2_R_ALPHA_NOTE_2026_03_30.md`
- `CODEX_WAVE2_NEXT_DIRECTIONS_2026_03_30.md`
- `CODEX_KERNELS_K1_K2_K3_2026_03_30.md`
- `CODEX_K123_BNONNEG_ROUTE_2026_03_30.md`
- `CODEX_DENOMINATOR_DRIFT_ATTACK_2026_03_30.md`
- `CODEX_TRANSPORT_COMPARISON_THEOREM_2026_03_30.md`
- `CODEX_SPECIFIC_SEQUENCE_ATTACK_2026_03_30.md`
- `CODEX_Q1_BLOCK_PROOF_ATTACK_2026_03_30.md`
- `CODEX_Q1_SIX_TERM_BLOCK_PROGRESS_2026_03_30.md`
- `CODEX_WAVE2_CONSOLIDATED_PROGRESS_2026_03_30.md`  (this file)

Exact checker scripts:

- `r_alpha_check.py`
- `k123_kernel_check.py`
- `k89_kernel_check.py`
- `denominator_drift_scan.py`
- `transport_comparison_scan.py`
- `q1_block_scan.py`

Note: `k123_kernel_check.py` now checks `K_1` through `K_5` despite its older
filename, and in the current version it checks `K_1` through `K_7`.

---

## 1. Exact Formula for the Denominator Error, `R(N)`, and `alpha(N)`

I derived the exact denominator-error identity

`e(q) = (1/(6q)) sum_{d|q} mu(d) d`.

This yields the exact weighted-Mertens formula

`R(N) = 1/6 + (1/6) sum_{m<=N} M(floor(N/m))/m`.

That in turn gives the exact formula

`alpha(N) = [-6R(N) + 1/n - 6 C_W(N)/N] / [1 + 12R(N)/n]`.

The practical consequence is that `alpha` is not a vague covariance term. It is
an explicit weighted Mertens object. In exact Farey computations on a sample of
`N`, I checked that `alpha(N)` is numerically extremely close to `-6R(N)`, so
the sign and size of `alpha` are largely governed by `R(N)`.

This shifted my view of the project: the real obstruction is not the positivity
of `alpha`, but the Abel correction.

---

## 2. Exact Kernel Decomposition of the Abel Correction

Let

- `N = p-1`
- `F_N^*` be the interior Farey set
- `K_m(p) = sum_{f in F_N^*} S(f,m) delta_p(f)`
- `C' = sum_{f in F_N^*} delta_p(f)^2`

Then the Abel correction has the exact grouped form

`Term2(p) = sum_{m=1}^N a_m(N) K_m(p) - M(N) K_1(p)`,

where

`a_m(N) = M(floor(N/m)) - M(floor(N/(m+1)))`.

Equivalently,

`Term2(p) = -M(floor(N/2)) K_1 + sum_{m=2}^N a_m(N) K_m`.

For the target `M(p) = -3` class, `M(N) = -2`, so the first few coefficients
are

- coeff(`K_1`) = `-M(floor(N/2))`
- coeff(`K_2`) = `M(floor(N/2)) - M(floor(N/3))`
- coeff(`K_3`) = `M(floor(N/3)) - M(floor(N/4))`
- coeff(`K_4`) = `M(floor(N/4)) - M(floor(N/5))`
- coeff(`K_5`) = `M(floor(N/5)) - M(floor(N/6))`

So the correction is an exact signed linear combination of explicit kernels with
short Mertens-difference coefficients.

This is, in my view, the main structural reduction achieved in this pass.

### How many kernels are there?

For a fixed prime step `p`, there are

`N = p - 1`

possible kernel indices in the exact grouped sum, because `m = floor(N/d)` can
take any value from `1` to `N`.

So:

- for fixed `p`, there are finitely many kernels `K_1,...,K_N`
- across all primes, `{K_m}` is an infinite family

The point of computing `K_1,K_2,...` explicitly is not that only finitely many
exist in principle, but that the early kernels may already dominate the sign of
`Term2`.

---

## 3. Exact Formulas for `K_1`, `K_2`, `K_3`

I first derived and verified:

`K_1 = C'/2`.

`K_2 = 3C'/2 - H_[1/2,1)(p)`.

`K_3 = 3C' + H_[1/3,1/2)(p) + 2 delta_p(2/3) - 3 H_[2/3,1)(p)`.

Here

- `H_I(p) = sum_{f in F_N^* cap I} delta_p(f)`
- `delta_p(2/3) = 0` if `p equiv 1 (mod 3)`
- `delta_p(2/3) = 1/3` if `p equiv 2 (mod 3)`

The subtle point was the exact middle-third symmetry:

`H_[1/2,2/3)(p) = - H_[1/3,1/2)(p) - delta_p(2/3)`.

The `delta_p(2/3)` boundary term is real and must be included.

---

## 4. New Exact Formulas for `K_4`, `K_5`, `K_6`, `K_7`, `K_8`, `K_9`

This was the main new work in the current pass.

### 4.1 Piecewise formula for `S(f,4)`

For `0 < f < 1`,

- `S(f,4) = 10f` on `(0,1/4)`
- `S(f,4) = 10f - 1` on `[1/4,1/3)`
- `S(f,4) = 10f - 2` on `[1/3,1/2)`
- `S(f,4) = 10f - 4` on `[1/2,2/3)`
- `S(f,4) = 10f - 5` on `[2/3,3/4)`
- `S(f,4) = 10f - 6` on `[3/4,1)`

Using `K_1 = C'/2` and the exact symmetry

`H_[2/3,3/4)(p) = - H_[1/4,1/3)(p) + delta_p(2/3) - delta_p(3/4)`,

I get the exact formula

`K_4 = 5C' + 4 H_[1/4,1/3)(p) + 2 H_[1/3,1/2)(p) - delta_p(2/3) + 5 delta_p(3/4) - 6 H_[3/4,1)(p)`.

Here

- `delta_p(3/4) = 0` if `p equiv 1 (mod 4)`
- `delta_p(3/4) = 1/2` if `p equiv 3 (mod 4)`

### 4.2 Piecewise formula for `S(f,5)`

For `0 < f < 1`,

- `S(f,5) = 15f` on `(0,1/5)`
- `S(f,5) = 15f - 1` on `[1/5,1/4)`
- `S(f,5) = 15f - 2` on `[1/4,1/3)`
- `S(f,5) = 15f - 3` on `[1/3,2/5)`
- `S(f,5) = 15f - 4` on `[2/5,1/2)`
- `S(f,5) = 15f - 6` on `[1/2,3/5)`
- `S(f,5) = 15f - 7` on `[3/5,2/3)`
- `S(f,5) = 15f - 8` on `[2/3,3/4)`
- `S(f,5) = 15f - 9` on `[3/4,4/5)`
- `S(f,5) = 15f - 10` on `[4/5,1)`

Using the exact symmetries

- `H_[1/2,3/5)(p) = - H_[2/5,1/2)(p) - delta_p(3/5)`
- `H_[3/5,2/3)(p) = - H_[1/3,2/5)(p) + delta_p(3/5) - delta_p(2/3)`
- `H_[3/4,4/5)(p) = - H_[1/5,1/4)(p) + delta_p(3/4) - delta_p(4/5)`

I get the exact formula

`K_5 = 15C'/2 + 8 H_[1/5,1/4)(p) + 6 H_[1/4,1/3)(p) + 4 H_[1/3,2/5)(p) + 2 H_[2/5,1/2)(p) - delta_p(3/5) - delta_p(2/3) - delta_p(3/4) + 9 delta_p(4/5) - 10 H_[4/5,1)(p)`.

The boundary terms are residue-class dependent:

- `delta_p(2/3)` depends on `p mod 3`
- `delta_p(3/4)` depends on `p mod 4`
- `delta_p(3/5)` and `delta_p(4/5)` depend on `p mod 5`

I did not reduce those four cases further in this memo because the exact formula
above is already correct and checkable.

### 4.3 Piecewise formula for `S(f,6)`

For `0 < f < 1`,

- `S(f,6) = 21f` on `(0,1/6)`
- `S(f,6) = 21f - 1` on `[1/6,1/5)`
- `S(f,6) = 21f - 2` on `[1/5,1/4)`
- `S(f,6) = 21f - 3` on `[1/4,1/3)`
- `S(f,6) = 21f - 5` on `[1/3,2/5)`
- `S(f,6) = 21f - 6` on `[2/5,1/2)`
- `S(f,6) = 21f - 9` on `[1/2,3/5)`
- `S(f,6) = 21f - 10` on `[3/5,2/3)`
- `S(f,6) = 21f - 12` on `[2/3,3/4)`
- `S(f,6) = 21f - 13` on `[3/4,4/5)`
- `S(f,6) = 21f - 14` on `[4/5,5/6)`
- `S(f,6) = 21f - 15` on `[5/6,1)`

Using the exact symmetries

- `H_[1/2,3/5)(p) = - H_[2/5,1/2)(p) - delta_p(3/5)`
- `H_[3/5,2/3)(p) = - H_[1/3,2/5)(p) + delta_p(3/5) - delta_p(2/3)`
- `H_[2/3,3/4)(p) = - H_[1/4,1/3)(p) + delta_p(2/3) - delta_p(3/4)`
- `H_[3/4,4/5)(p) = - H_[1/5,1/4)(p) + delta_p(3/4) - delta_p(4/5)`
- `H_[4/5,5/6)(p) = - H_[1/6,1/5)(p) + delta_p(4/5) - delta_p(5/6)`

I get

`K_6 = 21C'/2 + 13 H_[1/6,1/5)(p) + 11 H_[1/5,1/4)(p) + 9 H_[1/4,1/3)(p) + 5 H_[1/3,2/5)(p) + 3 H_[2/5,1/2)(p) - 2 delta_p(2/3) - delta_p(3/4) - delta_p(3/5) - delta_p(4/5) + 14 delta_p(5/6) - 15 H_[5/6,1)(p)`.

### 4.4 Piecewise formula for `S(f,7)`

For `0 < f < 1`,

- `S(f,7) = 28f` on `(0,1/7)`
- `S(f,7) = 28f - 1` on `[1/7,1/6)`
- `S(f,7) = 28f - 2` on `[1/6,1/5)`
- `S(f,7) = 28f - 3` on `[1/5,1/4)`
- `S(f,7) = 28f - 4` on `[1/4,2/7)`
- `S(f,7) = 28f - 5` on `[2/7,1/3)`
- `S(f,7) = 28f - 7` on `[1/3,2/5)`
- `S(f,7) = 28f - 8` on `[2/5,3/7)`
- `S(f,7) = 28f - 9` on `[3/7,1/2)`
- `S(f,7) = 28f - 12` on `[1/2,4/7)`
- `S(f,7) = 28f - 13` on `[4/7,3/5)`
- `S(f,7) = 28f - 14` on `[3/5,2/3)`
- `S(f,7) = 28f - 16` on `[2/3,5/7)`
- `S(f,7) = 28f - 17` on `[5/7,3/4)`
- `S(f,7) = 28f - 18` on `[3/4,4/5)`
- `S(f,7) = 28f - 19` on `[4/5,5/6)`
- `S(f,7) = 28f - 20` on `[5/6,6/7)`
- `S(f,7) = 28f - 21` on `[6/7,1)`

Using the exact symmetries

- `H_[1/2,4/7)(p) = - H_[3/7,1/2)(p) - delta_p(4/7)`
- `H_[4/7,3/5)(p) = - H_[2/5,3/7)(p) + delta_p(4/7) - delta_p(3/5)`
- `H_[3/5,2/3)(p) = - H_[1/3,2/5)(p) + delta_p(3/5) - delta_p(2/3)`
- `H_[2/3,5/7)(p) = - H_[2/7,1/3)(p) + delta_p(2/3) - delta_p(5/7)`
- `H_[5/7,3/4)(p) = - H_[1/4,2/7)(p) + delta_p(5/7) - delta_p(3/4)`
- `H_[3/4,4/5)(p) = - H_[1/5,1/4)(p) + delta_p(3/4) - delta_p(4/5)`
- `H_[4/5,5/6)(p) = - H_[1/6,1/5)(p) + delta_p(4/5) - delta_p(5/6)`
- `H_[5/6,6/7)(p) = - H_[1/7,1/6)(p) + delta_p(5/6) - delta_p(6/7)`

I get

`K_7 = 14C' + 19 H_[1/7,1/6)(p) + 17 H_[1/6,1/5)(p) + 15 H_[1/5,1/4)(p) + 13 H_[1/4,2/7)(p) + 11 H_[2/7,1/3)(p) + 7 H_[1/3,2/5)(p) + 5 H_[2/5,3/7)(p) + 3 H_[3/7,1/2)(p) - delta_p(4/7) - delta_p(3/5) - 2 delta_p(2/3) - delta_p(5/7) - delta_p(3/4) - delta_p(4/5) - delta_p(5/6) + 20 delta_p(6/7) - 21 H_[6/7,1)(p)`.

### 4.5 Piecewise formula for `S(f,8)`

For `0 < f < 1`,

- `S(f,8) = 36f` on `(0,1/8)`
- `S(f,8) = 36f - 1` on `[1/8,1/7)`
- `S(f,8) = 36f - 2` on `[1/7,1/6)`
- `S(f,8) = 36f - 3` on `[1/6,1/5)`
- `S(f,8) = 36f - 4` on `[1/5,1/4)`
- `S(f,8) = 36f - 6` on `[1/4,2/7)`
- `S(f,8) = 36f - 7` on `[2/7,1/3)`
- `S(f,8) = 36f - 9` on `[1/3,3/8)`
- `S(f,8) = 36f - 10` on `[3/8,2/5)`
- `S(f,8) = 36f - 11` on `[2/5,3/7)`
- `S(f,8) = 36f - 12` on `[3/7,1/2)`
- `S(f,8) = 36f - 16` on `[1/2,4/7)`
- `S(f,8) = 36f - 17` on `[4/7,3/5)`
- `S(f,8) = 36f - 18` on `[3/5,5/8)`
- `S(f,8) = 36f - 19` on `[5/8,2/3)`
- `S(f,8) = 36f - 21` on `[2/3,5/7)`
- `S(f,8) = 36f - 22` on `[5/7,3/4)`
- `S(f,8) = 36f - 24` on `[3/4,4/5)`
- `S(f,8) = 36f - 25` on `[4/5,5/6)`
- `S(f,8) = 36f - 26` on `[5/6,6/7)`
- `S(f,8) = 36f - 27` on `[6/7,7/8)`
- `S(f,8) = 36f - 28` on `[7/8,1)`

Using the reflected-interval symmetries all the way up the ladder, I get

`K_8 = 18C' + 26 H_[1/8,1/7)(p) + 24 H_[1/7,1/6)(p) + 22 H_[1/6,1/5)(p) + 20 H_[1/5,1/4)(p) + 16 H_[1/4,2/7)(p) + 14 H_[2/7,1/3)(p) + 10 H_[1/3,3/8)(p) + 8 H_[3/8,2/5)(p) + 6 H_[2/5,3/7)(p) + 4 H_[3/7,1/2)(p) - delta_p(4/7) - delta_p(3/5) - delta_p(5/8) - 2 delta_p(2/3) - delta_p(5/7) - 2 delta_p(3/4) - delta_p(4/5) - delta_p(5/6) - delta_p(6/7) + 27 delta_p(7/8) - 28 H_[7/8,1)(p)`.

### 4.6 Piecewise formula for `S(f,9)`

For `0 < f < 1`,

- `S(f,9) = 45f` on `(0,1/9)`
- `S(f,9) = 45f - 1` on `[1/9,1/8)`
- `S(f,9) = 45f - 2` on `[1/8,1/7)`
- `S(f,9) = 45f - 3` on `[1/7,1/6)`
- `S(f,9) = 45f - 4` on `[1/6,1/5)`
- `S(f,9) = 45f - 5` on `[1/5,2/9)`
- `S(f,9) = 45f - 6` on `[2/9,1/4)`
- `S(f,9) = 45f - 8` on `[1/4,2/7)`
- `S(f,9) = 45f - 9` on `[2/7,1/3)`
- `S(f,9) = 45f - 12` on `[1/3,3/8)`
- `S(f,9) = 45f - 13` on `[3/8,2/5)`
- `S(f,9) = 45f - 14` on `[2/5,3/7)`
- `S(f,9) = 45f - 15` on `[3/7,4/9)`
- `S(f,9) = 45f - 16` on `[4/9,1/2)`
- `S(f,9) = 45f - 20` on `[1/2,5/9)`
- `S(f,9) = 45f - 21` on `[5/9,4/7)`
- `S(f,9) = 45f - 22` on `[4/7,3/5)`
- `S(f,9) = 45f - 23` on `[3/5,5/8)`
- `S(f,9) = 45f - 24` on `[5/8,2/3)`
- `S(f,9) = 45f - 27` on `[2/3,5/7)`
- `S(f,9) = 45f - 28` on `[5/7,3/4)`
- `S(f,9) = 45f - 30` on `[3/4,7/9)`
- `S(f,9) = 45f - 31` on `[7/9,4/5)`
- `S(f,9) = 45f - 32` on `[4/5,5/6)`
- `S(f,9) = 45f - 33` on `[5/6,6/7)`
- `S(f,9) = 45f - 34` on `[6/7,7/8)`
- `S(f,9) = 45f - 35` on `[7/8,8/9)`
- `S(f,9) = 45f - 36` on `[8/9,1)`

Again simplifying by symmetry yields

`K_9 = 45C'/2 + 34 H_[1/9,1/8)(p) + 32 H_[1/8,1/7)(p) + 30 H_[1/7,1/6)(p) + 28 H_[1/6,1/5)(p) + 26 H_[1/5,2/9)(p) + 24 H_[2/9,1/4)(p) + 20 H_[1/4,2/7)(p) + 18 H_[2/7,1/3)(p) + 12 H_[1/3,3/8)(p) + 10 H_[3/8,2/5)(p) + 8 H_[2/5,3/7)(p) + 6 H_[3/7,4/9)(p) + 4 H_[4/9,1/2)(p) - delta_p(5/9) - delta_p(4/7) - delta_p(3/5) - delta_p(5/8) - 3 delta_p(2/3) - delta_p(5/7) - 2 delta_p(3/4) - delta_p(7/9) - delta_p(4/5) - delta_p(5/6) - delta_p(6/7) - delta_p(7/8) + 35 delta_p(8/9) - 36 H_[8/9,1)(p)`.

---

## 5. Exact Verification and Broader Exact Scan

I ran exact rational checks on the sample

`p = 13, 19, 43, 71, 107, 199`.

For every one of these primes, all formula checks passed exactly:

- `K_1 = C'/2`
- `K_2 = 3C'/2 - H_[1/2,1)`
- `K_3 = 3C' + H_[1/3,1/2) + 2 delta_p(2/3) - 3 H_[2/3,1)`
- the symmetry relations for the middle-third and quarter/fifth intervals
- the new `K_4`, `K_5`, `K_6`, `K_7` formulas above

### Observed kernel ratios on the original sample

| `p` | `K_2/C'` | `K_3/C'` | `K_4/C'` | `K_5/C'` | `K_6/C'` | `K_7/C'` |
|-----|----------|----------|----------|----------|----------|----------|
| 13  | 0.480976 | 0.486064 | 0.415425 | 0.403996 | 0.263752 | 0.296269 |
| 19  | 0.563717 | 0.667255 | 0.639271 | 0.603864 | 0.478107 | 0.550032 |
| 43  | 0.647077 | 0.803321 | 0.828225 | 0.838085 | 0.822940 | 0.887275 |
| 71  | 0.709737 | 0.860336 | 0.916589 | 1.006094 | 1.029834 | 1.080829 |
| 107 | 0.733863 | 0.877817 | 0.966882 | 1.043586 | 1.080693 | 1.144541 |
| 199 | 0.730617 | 0.889263 | 0.993181 | 1.072311 | 1.127461 | 1.204390 |

For the same sample, the new ratios are:

- `K_8/C' = 0.223861, 0.435797, 0.881970, 1.093253, 1.176754, 1.239399`
- `K_9/C' = 0.308583, 0.420896, 0.878626, 1.087360, 1.205892, 1.277643`

So on this target-prime sample:

- `K_2 > 0`
- `K_3 > 0`
- `K_4 > 0`
- `K_5 > 0`
- `K_6 > 0`
- `K_7 > 0`
- `K_8 > 0`
- `K_9 > 0`

This is encouraging. The positivity is not yet proved analytically, but the
first nine kernels all point in the right direction on the exact sample I
checked.

### Broader exact scan on the `M(p) = -3` class up to `431`

I also ran a broader exact scan over all

`p in {13, 19, 43, 47, 53, 71, 107, 131, 173, 179, 271, 311, 379, 389, 431}`

with `M(p) = -3` and checked direct exact values of `K_2,...,K_9`.

Results:

- no kernel sign failures occurred
- the minimum observed ratios were always at `p = 13`

Specifically:

- min `K_2/C' = 0.480976...`
- min `K_3/C' = 0.486064...`
- min `K_4/C' = 0.415425...`
- min `K_5/C' = 0.403996...`
- min `K_6/C' = 0.263752...`
- min `K_7/C' = 0.296269...`
- min `K_8/C' = 0.223861...`
- min `K_9/C' = 0.308583...`

So at least in this exact range, the first nine kernels remain positive across
the whole visible `M(p) = -3` class.

### Observed interval-drift sign pattern

On the same sample, the following signs were stable:

Lower intervals:

- `H_[1/5,1/4) < 0`
- `H_[1/4,1/3) < 0`
- `H_[1/3,2/5) < 0`
- `H_[2/5,1/2) < 0`

Upper intervals:

- `H_[1/2,3/5) > 0`
- `H_[3/5,2/3) > 0`
- `H_[2/3,3/4) > 0`
- `H_[3/4,4/5) > 0`
- `H_[4/5,1) > 0`

I also checked this sign pattern on the full exact `M(p) = -3` scan up to
`431`, and I found no failures there either.

This may be the most important empirical sign signal from the kernel route.
It suggests that the drift terms are themselves organized by the left/right
symmetry of the Farey interval, with predictable signs.

---

## 6. Denominator-by-Denominator Drift Decomposition

This was the strongest new structural idea from the latest pass, and it now
comes with a clean exact theorem.

For any interval `J subset [1/2,1)`, define the fixed-denominator drift

`H_J^{(b)}(p) = sum_{a/b in J, gcd(a,b)=1} delta_p(a/b)`.

Then

`H_J(p) = sum_{b<=N} H_J^{(b)}(p)`.

Let `I = 1 - J` be the reflected lower interval in `(0,1/2]`, with endpoint
conventions chosen so that `a/b in J` corresponds exactly to `u/b in I` under
`a = b - u`. Then the fixed-denominator contribution has the exact form

`H_J^{(b)}(p) = (1/b) sum_{u in U_I(b)} ([pu]_b - u)`,

where

- `U_I(b) = {u : gcd(u,b)=1, u/b in I}`
- `[pu]_b` denotes the least positive residue of `pu mod b`

This is just the identity

`delta_p((b-u)/b) = ([pu]_b - u)/b`.

So upper-half drifts are literally averages of modular increments over a lower
window, denominator by denominator.

### Exact transport theorem

Define

`T_{b,r}(X) = sum_{u<=X, gcd(u,b)=1} ([ru]_b - u)`.

Then for every modulus `b`, every unit `r mod b`, and every
`1 <= X <= b-1`,

`T_{b,r}(X) >= 0`.

The proof is simple: the set

`{[ru]_b : u<=X, gcd(u,b)=1}`

is a subset of the reduced residue system of the same cardinality as the
initial reduced-residue segment

`{u<=X : gcd(u,b)=1}`,

and the initial segment has the minimum possible sum among all subsets of that
cardinality.

### Tail version

For tail intervals `J = [theta,1)`, the formula becomes especially clean:

`H_[theta,1)^{(b)}(p) = (1/b) sum_{1<=u<=(1-theta)b, gcd(u,b)=1} ([pu]_b - u)`.

Examples:

- `H_[1/2,1)^{(b)}(p) = (1/b) sum_{1<=u<=b/2, gcd(u,b)=1} ([pu]_b - u)`
- `H_[2/3,1)^{(b)}(p) = (1/b) sum_{1<=u<=b/3, gcd(u,b)=1} ([pu]_b - u)`
- `H_[3/4,1)^{(b)}(p) = (1/b) sum_{1<=u<=b/4, gcd(u,b)=1} ([pu]_b - u)`
- `H_[4/5,1)^{(b)}(p) = (1/b) sum_{1<=u<=b/5, gcd(u,b)=1} ([pu]_b - u)`

So every upper-tail fixed-denominator drift is nonnegative analytically.

I also brute-force checked `T_{b,r}(X) >= 0` for all `b <= 100`, all units
`r mod b`, and all `1 <= X < b`, with no counterexamples.

On the visible `M(p) = -3` range up to `431`, the pooled denominator counts for
the main upper tails were:

- `[1/2,1)`: `2440` positive, `0` negative, `147` zero
- `[2/3,1)`: `2488` positive, `0` negative, `99` zero
- `[3/4,1)`: `2475` positive, `0` negative, `112` zero
- `[4/5,1)`: `2467` positive, `0` negative, `120` zero

### Why I think this matters

The kernel formulas keep reducing to statements about upper-interval drifts.
This denominator decomposition turns those upper drifts into weighted sums of
the simple modular increment `([pu]_b - u)`, and the transport theorem explains
their sign.

The remaining obstruction is now more sharply isolated: the middle intervals are
differences of such transport sums, and those do not have a uniform
denominator-by-denominator sign.

On the `M(p) = -3` range up to `431` I found:

- for `[1/2,2/3)`: `2038` positive, `371` negative, `178` zero
- for `[1/3,1/2)`: `371` positive, `2048` negative, `168` zero
- for `[1/2,3/5)`: `1729` positive, `648` negative, `210` zero

So the drift attack does not close the whole problem by itself, but it does
reduce it to a more specific monotonicity/comparison problem for transport
sums.

---

## 7. What I Now Think the Best Route Is

I no longer think the best path is a pure norm-only Cauchy-Schwarz closure of
the original ratio `r(p)`.

The better route appears to be:

1. write `Term2` as an exact kernel sum
2. compute explicit formulas for the first several kernels
3. prove sign information for the associated interval drifts
4. combine those with the short Mertens-difference coefficients

In short, the problem is becoming an interval-drift / kernel-sign problem rather
than a soft global-error problem.

### New comparison theorem for middle windows

There is now also a clean exact comparison theorem for the middle-window
transport sums.

For any reduced-residue window `W subset R_b`, define

`Delta_r(W) = sum_{u in W} ([ru]_b - u)`.

Then

`Delta_r(W) + Delta_{-r}(W) = sum_{u in W} (b - 2u)`.

So if `W` lies strictly below `b/2`, the pair-sum is strictly positive. This
applies exactly to the windows defining the upper middle intervals:

- `(b/3, b/2]`
- `(2b/5, b/2]`
- `(b/4, b/3]`

Therefore:

- pointwise monotonicity is false
- but `(+/-)` pairwise comparison under `r -> -r` is true
- negative values cannot outnumber positive values for these windows

I checked this numerically up to `b = 300`, and I found no modulus where
negative values outnumber positive ones for those three special windows.

### Actual-sequence progress

I also pushed one step beyond the all-units comparison and looked at the actual
sequence `r_b = p mod b` as `b` varies.

The strongest new empirical fact is:

- the whole `q = 1` block `p/2 < b < p` gave a positive total contribution to
  the `[1/2,2/3)` window for every tested prime up to `5000`

and on the visible `M(p) = -3` range that `q = 1` block overwhelmingly
dominates the positive mass.

I wrote that up in
`CODEX_SPECIFIC_SEQUENCE_ATTACK_2026_03_30.md`.

---

## 8. Best Next Directions for the Researchers

### Direction A: Continue the kernel ladder

The most straightforward continuation is:

- derive `K_10` and `K_11`
- look for a stable pattern in the coefficients of the drift intervals
- see whether the kernel formulas admit a general induction in `m`

If the first several kernels are all positive or have a controlled lower bound,
that could be enough to force `Term2 < 0` on the `M(p) = -3` class.

### Direction B: Prove interval-drift signs analytically

This now looks central.

The most useful immediate targets are:

- `H_[1/2,1) > 0`
- `H_[1/3,1/2) < 0`
- `H_[2/3,1) > 0`
- `H_[1/4,1/3) < 0`
- `H_[3/4,1) > 0`

Even partial theorems here would give real leverage on `K_2,K_3,K_4`.

### Direction C: Push the denominator-by-denominator drift decomposition

This is now more than a heuristic: the exact formula above shows that upper-tail
drifts are sums of modular increments `([pu]_b - u)/b` over lower windows.

If one can prove those increments have positive mean on the relevant windows,
denominator by denominator or on short `b` averages, then the global drift signs
may become a local modular-counting theorem instead of a global analytic
estimate.

### Direction D: Residue-class packaging of boundary terms

For `K_3,K_4,K_5`, the only non-drift corrections are the explicit boundary
terms `delta_p(2/3)`, `delta_p(3/4)`, `delta_p(3/5)`, `delta_p(4/5)`.

It may be worth tabulating the formulas by `p mod 60`, so that each kernel
becomes a finite collection of residue-class exact formulas with no hidden
ambiguity.

That could make an eventual analytic statement cleaner.

---

## 9. Honest Status

What is fully exact in this pass:

- the formula for `R(N)`
- the formula for `alpha(N)`
- the exact grouped coefficient formula for `Term2`
- the exact formulas for `K_1,...,K_9`
- the exact symmetry corrections with their boundary terms
- the exact checker verification on the sampled `M(p) = -3` primes
- the broader exact positivity scan for `K_2,...,K_9` up to `p = 431`
- the exact denominator-by-denominator drift decomposition for upper intervals

What is still not proved analytically:

- positivity of `K_2,K_3,K_4,K_5` for all target primes
- sign theorems for the interval drifts
- a full unconditional proof that `B >= 0` for all `M(p) <= -3`

So this is real progress, but not closure.

---

## 10. Six-Term `q=1` Block Update

I wrote a separate focused note,

`CODEX_Q1_SIX_TERM_BLOCK_PROGRESS_2026_03_30.md`,

for the six-term mod-`6` block route.

The key new points there are:

- exact Möbius reduction of the reduced block to unrestricted window sums
- an exact floor-sum form for those unrestricted sums
- a rigorous termwise Koksma bound
- an exact six-term continuous lower bound `> 1/12`
- a genuine partial theorem proving positivity of the unrestricted actual block
  in an explicit early subrange of `q=1`
- strong exact scan evidence that the full reduced block stays positive through
  `p <= 20000`
- a new sharp unrestricted surrogate conjecture:
  `U_{p,m} >= p - 2`

I now think the right missing lemma is a six-term cancellation theorem before
taking absolute values, not another single-term estimate.

---

## Bottom Line

The best new message I would hand to the researchers is:

The remaining `B >= 0` gap now has a much sharper structure than before.
The correction term is an exact signed sum of explicit kernels, and the first
nine kernels are now known. On the exact `M(p) = -3` range checked up to
`431`, `K_2,...,K_9` stayed positive, with a very stable lower/upper
interval-drift sign pattern behind them.

If this route works, the proof will likely close through interval-drift sign
control and explicit kernel formulas, not through a single global norm bound.
