# Direct Proof Attack: B + C > 0

## Key Identity

**B + C = Sum (D_new)^2 - Sum (D_old)^2** (over old fractions)

where D_new(f) = D_old(f) + delta(f), proved via:
- rank_new(a/b) = rank_old(a/b) + floor(pa/b)
- D_new = rank_new - n'*f = D_old + (a - pa mod b)/b = D_old + delta

Equivalently: B + C = 2*Sum(D*delta) + Sum(delta^2) = Sum(delta^2)*(1+R)
where R = 2*Sum(D*delta)/Sum(delta^2).

**B + C > 0 iff R > -1.**

## Approaches Tried

### 1. Global Cauchy-Schwarz (FAILS)
|R| <= 2*sqrt(Sum D^2 / Sum delta^2). But Sum D^2 / Sum delta^2 ~ O(p^2) -> infinity.

### 2. Centered Cauchy-Schwarz (marginal)
Remove per-denominator mean of D: D_centered(a/b) = D(a/b) - mean_b(D).
|R| <= 2*sqrt(Sum D_centered^2 / Sum delta^2).
Works for p <= 300? **NO**

### 3. Detrended Cauchy-Schwarz (best analytic bound)
Remove per-denominator linear trend: D_fluct = D - alpha - beta*(a/b).
|R| <= 2*sqrt(Sum D_fluct^2 / Sum delta^2).
Works for p <= 300? **NO**

### 4. Per-denominator R_b bound (FAILS individually)
Individual R_b = 2*C_b/S_b can be < -1 for some b.
But the weighted average R = Sum w_b*R_b stays > -1.

### 5. D_new = D_old + delta (KEY IDENTITY)
B + C > 0 iff old fractions have LARGER squared discrepancy in F_p than in F_{p-1}.
Physical meaning: injecting p-1 new fractions (k/p) into the Farey sequence
makes the pre-existing fractions MORE displaced from uniform spacing.

## Computational Results

- Verified B+C > 0 for ALL primes 11 <= p <= 300
- Minimum (1+R) = 0.482295 at p = 11
- R -> 0 as p -> infinity (empirically |R| ~ O(1/sqrt(p)))

## What Remains

To close the proof, we need ONE of:

1. **Effective detrended CS bound**: Show Sum D_fluct^2 / Sum delta^2 < 1/4 for p > P0.
   This requires understanding the asymptotics of D_fluct within each denominator class.

2. **Spectral/Fourier proof**: Express Sum D*delta in terms of Kloosterman sums
   and use Weil bounds to show |Sum D*delta| = o(Sum delta^2).

3. **Combinatorial injection argument**: Show that injecting uniformly-spaced
   fractions k/p always increases the L2 discrepancy of pre-existing fractions.
   This would be a direct proof of Sum D_new^2 > Sum D_old^2.

---
Generated: 2026-03-30 20:29
