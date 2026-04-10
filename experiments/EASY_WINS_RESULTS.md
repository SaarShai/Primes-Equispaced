# Easy Wins — Computation Results
# 2026-04-10

## 1. Phase Saturation (k=1..20)

| Terms | R | R² | Δ from previous |
|-------|------|------|-----------------|
| 1 | 0.687 | 0.472 | — |
| 2 | 0.789 | 0.623 | +0.151 |
| 3 | 0.834 | 0.696 | +0.073 |
| 5 | 0.876 | 0.767 | +0.071 |
| 7 | 0.906 | 0.820 | +0.053 |
| 10 | 0.923 | 0.852 | +0.032 |
| 15 | 0.935 | 0.873 | +0.021 |
| 20 | 0.944 | 0.890 | +0.017 |

Saturation: R approaches ~0.95. Diminishing returns clear after k=10.
20 zeros explain 89% of variance in M(p)/√p.

## 2. Detection Curve

IMPORTANT FINDING: Detection with FIRST N primes is much worse than
random subsets from wide range. At N=15000 (P~170K): only 6/20 detected.

Reason: small primes have short log p → poor frequency resolution.
Resolution limit = 2π/log P. Need large P for high zeros.

The "2750 from 25M" claim was about random subsets from [1, 25M],
where the RANGE (log 25M ≈ 17) provides good resolution.
First 2750 primes go up to P~25000 (log P ≈ 10), which is less resolution.

This STRENGTHENS the universality claim: it's not just COUNT that matters,
but RANGE (Σ 1/p divergence = range spanning condition).
The bounded-interval failure we observed is the same phenomenon.
