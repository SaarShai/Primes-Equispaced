# VERIFY_SPECTROSCOPE_AP_CLASSES

## Setup
- N = 10000, primes <= N: 1229
- gamma_1 = 14.134725141734693
- Test F_P(gamma_1) = gamma^2 * |sum_{p in P, p<=N} M(p)/p * exp(-i*gamma*log p)|^2 on prime subsets by residue class mod 7

| Subset | Count | F_P(gamma_1) |
|--------|-------|--------------|
| All primes > 7 | 1225 | 1223.2973 |
| p ≡ 1 (mod 7) | 203 | 37.6165 |
| p ≡ 2 (mod 7) | 202 | 26.8016 |
| p ≡ 3 (mod 7) | 208 | 38.2813 |
| p ≡ 4 (mod 7) | 202 | 18.3840 |
| p ≡ 5 (mod 7) | 210 | 47.2164 |
| p ≡ 6 (mod 7) | 200 | 62.0622 |

## Interpretation
Under universality + Dirichlet primes-in-AP, each residue class a ∈ {1,2,3,4,5,6}
mod 7 has infinitely many primes with density 1/φ(7) = 1/6. Sum 1/p = infinity
for each class. Expected: all 6 classes should have F_P(gamma_1) comparable
(within factor ~6, since each has ~1/6 of the primes).

If some classes show dramatically smaller F, that would contradict universality.
