# Unconditional Universality via Variance Argument

## Source: Codex analysis (2026-04-09)

## Key Insight
Don't detect WHERE zeros are — prove the spectroscope has MORE VARIANCE than a zero-free model.

## Theorem Sketch
For any [A,B] containing a zeta zero:
  integral_A^B F_N(gamma) dgamma > c_1 * (log N)^{c_2}
whereas under zero-free model: O(1).

## Why Siegel zeros don't matter
A Siegel zero at gamma~0 contributes to variance near gamma=0, NOT near gamma_1~14.
Band [10,18] is safe.

## Proof ingredients (all unconditional):
1. Explicit formula (Perron + residues, unconditional identity)
2. Large sieve (Montgomery-Vaughan, unconditional)
3. Riemann-von Mangoldt zero density (unconditional)
4. Diagonal dominance: zero contributions dominate cross terms

## Strategy
- Lead with integral lower bound (clean statement)
- Prove via variance mechanism
- Cross-correlation of two spectroscopes as corollary
- Hybrid computation as second corollary

## Critical Lemma Needed
Diagonal dominance of zero contributions in variance of truncated Dirichlet polynomials, unconditionally, using large sieve.
