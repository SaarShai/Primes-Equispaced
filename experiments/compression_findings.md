# Multiplicative Compression Beyond Farey Sequences

## The Principle

In Farey sequences, the exponential sum over ~3N^2/pi^2 fractions collapses to M(N)+1 (one integer). This is "multiplicative compression" -- a massive cancellation driven by the Mobius function. We tested whether this phenomenon extends to other mathematical sequences.

## Compression Hierarchy (measured exponents)

For each sequence S_N of size |S_N|, define:
- E(N) = |sum_{s in S_N} exp(2*pi*i*s / period)|
- Compression ratio = E(N) / |S_N|

If ratio ~ N^{-alpha} with alpha > 0, the sequence exhibits compression.

| Sequence | Ratio ~ N^alpha | |E| ~ N^beta | Verdict |
|---|---|---|---|
| **Farey** | N^(-1.82) | N^(+0.17) | **STRONGEST** |
| Square-free | N^(-0.93) | N^(+0.06) | STRONG |
| mu(n)=+1 subset | N^(-0.89) | N^(+0.13) | STRONG |
| mu(n)=-1 subset | N^(-0.85) | N^(+0.11) | STRONG |
| Even Omega | N^(-0.69) | N^(+0.35) | STRONG |
| 2 prime factors | N^(-0.47) | N^(+0.55) | MODERATE |
| Primes | N^(-0.18) | N^(+0.63) | WEAK |
| 1 prime factor | N^(-0.11) | N^(+0.61) | WEAK |
| **Smooth numbers** | ~N^(0) | grows with N | **NONE** |
| **Powerful numbers** | ~N^(0) | grows with N | **NONE** |

## Key Discovery 1: The Grand Identity for Weighted Farey Sums

**Theorem (verified to machine precision):**

For ANY arithmetic function f,

    sum_{a/b in F_N} f(b) * exp(2*pi*i*a/b) = f(1) + sum_{b=1}^N f(b)*mu(b)

This is because:
1. Group Farey fractions by denominator b
2. For each b, the sum over a coprime to b gives the Ramanujan sum c_b(1) = mu(b)
3. Total = sum_{b=1}^N f(b) * mu(b) + f(1) (from the a=0 term)

### Instances verified:

| f(b) | Farey sum = | Known name |
|---|---|---|
| 1 | 1 + M(N) | Mertens function |
| lambda(b) (Liouville) | 1 + Q(N) | **Squarefree count** |
| mu(b) | 1 + Q(N) | Same (since mu*mu on sqfree = 1) |
| (-1)^b | 1 + sum_{odd sqfree} 1 - sum_{even sqfree} 1 | Odd/even sqfree |
| b | 1 + sum b*mu(b) | Euler-type sum |
| phi(b) | 1 + sum phi(b)*mu(b) | Jordan-type sum |

## Key Discovery 2: Liouville-Weighted Farey Sum = Q(N) + 1

**Identity:**

    sum_{a/b in F_N} lambda(b) * exp(2*pi*i*a/b) = Q(N) + 1

where Q(N) is the count of squarefree numbers up to N (~ 6N/pi^2).

**Why it works:** For squarefree b, lambda(b) = mu(b), so lambda(b)*mu(b) = mu(b)^2 = 1. For non-squarefree b, mu(b) = 0. Therefore sum lambda(b)*mu(b) = sum_{sqfree b} 1 = Q(N).

This means: weighting each Farey fraction by the Liouville function of its denominator converts the Mertens function into the squarefree counting function. The exponential sum over O(N^2) terms collapses to a single integer.

## Key Discovery 3: Universal Mechanism = Mobius Inversion

**Thesis:** Compression occurs if and only if the set is definable via Mobius inversion from a "smooth" generating function.

Evidence:

**Sets WITH compression (all Mobius-definable):**
- Squarefree: mu^2(n) = sum_{d^2|n} mu(d)
- k-free numbers: indicator = sum_{d^k|n} mu(d) for any k
- Numbers coprime to q: indicator = sum_{d|gcd(n,q)} mu(d)
- Farey fractions: gcd(a,b)=1 via Mobius inversion

**Sets WITHOUT compression (not Mobius-definable):**
- Smooth numbers (defined by largest prime factor, not Mobius inversion)
- Powerful numbers (defined by MINIMUM prime power, not Mobius inversion)

**Why Mobius inversion causes compression:**
The Mobius function has the property that sum_{d|n} mu(d) = [n=1]. This creates systematic sign alternation in exponential sums. When a set S is defined by S = sum mu(d) * (larger set), the exponential sum over S decomposes into sums over larger sets weighted by mu(d), which cancel due to multiplicative independence.

## Key Discovery 4: Squarefree Exponential Sums Track Q(N) Fluctuations

The exponential sum over squarefree numbers:

    S(1, N) = sum_{n sqfree, n<=N} exp(2*pi*i*n/N)

has the following structure:
- Decomposes as: S = (-1) + sum_{d>=2, mu(d)!=0} mu(d) * (geometric series over N/d^2 terms)
- The d=1 term always contributes -1 (complete cancellation)
- Dominant contributions come from d near sqrt(N) where N/d^2 is small
- |S| grows as ~ N^{0.06}, giving compression ratio ~ N^{-0.93}
- S tracks Q(N) - 6N/pi^2 (fluctuation in squarefree count) with correlation r = 0.935

## Key Discovery 5: Kloosterman Sums -- A Different Compression

Kloosterman sums K(1,1;n) = sum_{x coprime to n} exp(2*pi*i*(x + x^{-1})/n) also exhibit compression:
- Compression ratio ~ n^{-0.46}, close to the Weil bound prediction of n^{-0.5}
- This is a DIFFERENT mechanism: algebraic-geometric (Weil/Deligne) rather than multiplicative (Mobius)
- The Kloosterman sum arises from the structure of the algebraic variety x*y = 1, not from Mobius inversion

## Primitive Roots: Partial Compression

The sum over primitive roots mod p: sum_g exp(2*pi*i*g/p) does NOT collapse to mu(p-1) as initially hypothesized. The values are larger and more complex. However:
- Compression ratio ~ p^{-0.62} (moderate compression)
- The sum has real and imaginary parts that grow as ~ p^{0.4}
- This is related to Gauss sums over generators of (Z/pZ)*

## Smooth Numbers: Why They Don't Compress

10-smooth numbers show INCREASING |E|/|S| ratios as N grows (0.23 -> 0.26 -> 0.31). This is because:
1. Smooth numbers cluster near small values (they thin out for large n)
2. This clustering prevents cancellation in the exponential sum
3. There is no Mobius decomposition to force sign alternation
4. The "density" of smooth numbers decays as rho(log N / log B), giving a biased sum

## Beatty Sequences: Surprising Compression

Beatty sequences {floor(n*alpha)} for irrational alpha show strong compression:
- Compression ratio ~ N^{-0.94} for the golden ratio
- |E| stays O(1) or grows very slowly
- This is NOT due to Mobius inversion but rather Weyl's equidistribution theorem
- The exponential sum cancels because floor(n*alpha) mod P is equidistributed

This represents a THIRD compression mechanism, distinct from both Mobius and Weil:
1. **Mobius compression**: driven by mu(n) sign alternation
2. **Weil compression**: driven by algebraic-geometric cancellation
3. **Equidistribution compression**: driven by irrational rotation

## Summary Table of Compression Mechanisms

| Mechanism | Example | Exponent | Root cause |
|---|---|---|---|
| Mobius inversion | Farey, squarefree, k-free | -0.9 to -1.8 | mu(n) sign alternation |
| Algebraic-geometric | Kloosterman | ~-0.5 | Weil bound on varieties |
| Equidistribution | Beatty | ~-0.9 | Weyl's theorem |
| None | Smooth, powerful | ~0 | Clustering / no sign alt. |

## Files

- `multiplicative_compression.py`: Initial survey of all 10+ sequence types
- `compression_deep_analysis.py`: Deep analysis of winners, scaling laws, identities
