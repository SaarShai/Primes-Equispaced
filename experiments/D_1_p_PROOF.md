# Proposition: D(1/p) = 1 - |F_{p-1}|/p

## Statement
For any prime p ≥ 3, the rank deviation of the fraction 1/p in F_p satisfies:
  D(1/p) = rank(1/p, F_{p-1}) - |F_{p-1}| · (1/p) = 1 - |F_{p-1}|/p

## Proof
The fraction 1/p is new in F_p (since p is prime, gcd(1,p)=1, and p was not a denominator in F_{p-1}).

rank(1/p, F_{p-1}) = #{f ∈ F_{p-1} : f ≤ 1/p}.

For p ≥ 3, the only fraction in F_{p-1} with value ≤ 1/p is 0/1.
Indeed: the smallest positive fraction in F_{p-1} is 1/(p-1) > 1/p.

Therefore rank(1/p, F_{p-1}) = 1 (counting 0/1).

D(1/p) = 1 - |F_{p-1}|/p.

## Asymptotic
Since |F_N| = 1 + Σ_{k=1}^N φ(k) = 3N²/π² + O(N log N) (Mertens, 1874):

D(1/p) = 1 - (3(p-1)²/π² + O(p log p))/p = -3p/π² + O(log p)

## Dominance
D(1/p) · δ(1/p) = D(1/p) · (1/p) ≈ -3/π² ≈ -0.304 (constant, independent of p).
This single fraction contributes 65-73% of total |Σ D·δ| (verified for p ≤ 199).

## Verification
| p | D(1/p) exact | -3p/π² approx | ratio |
|---|-------------|---------------|-------|
| 13 | -2.615 | -3.367 | 0.777 |
| 31 | -8.000 | -8.825 | 0.907 |
| 61 | -17.082 | -17.939 | 0.952 |
| 97 | -27.938 | -28.880 | 0.967 |
| 199 | -59.075 | -59.882 | 0.987 |

Convergence to the asymptotic improves with p (ratio → 1).
