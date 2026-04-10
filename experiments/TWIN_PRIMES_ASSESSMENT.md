# Farey Per-Step Discrepancy and Twin Primes: Honest Assessment

**Date:** 2026-03-29
**Verdict: NO meaningful connection. Do not pursue.**

## Summary

We investigated whether our Farey per-step discrepancy discoveries (Sign Theorem, bridge identity, four-term decomposition) have implications for the twin primes conjecture. After computational analysis of 1,222 twin prime pairs up to 100K and analytical examination of the bridge identity, the answer is **clearly negative**. The correlations we observe between twin primes are entirely explained by proximity effects that apply to ALL close prime pairs, with nothing twin-specific.

## Q1: Does DeltaW(p) behave differently at twin primes?

**No.**

We computed DeltaW for twin primes (p, p+2) and compared to cousin primes (gap 4), sexy primes (gap 6), and larger gaps. Results from 100K dataset:

| Gap | Pairs | Same-sign rate | Correlation | Detrended corr |
|-----|-------|---------------|-------------|----------------|
| 2 (twin) | 1,222 | 98.45% | 0.9811 | 0.9997 |
| 4 (cousin) | 1,214 | 97.45% | 0.9827 | 0.9992 |
| 6 (sexy) | 2,445 | 97.79% | 0.9702 | 0.9980 |
| 10 | 1,622 | 97.47% | 0.9468 | 0.9962 |
| 30 | 3,327 | 95.82% | 0.9342 | 0.9863 |
| 50 | 1,644 | 94.46% | 0.9229 | 0.9767 |

**Critical observations:**
- Gap-4 (cousin) primes have HIGHER raw correlation (0.9827) than twin primes (0.9811). Fisher z-test: p = 0.26, not significant.
- The correlation decays smoothly with gap size. There is NO discontinuity or special behavior at gap 2.
- After detrending (removing the 1/p^1.77 power law), ALL gaps show correlation > 0.97. The correlation is dominated by the smooth trend of DeltaW, not by any twin-specific structure.
- The high same-sign rate for twins was already noted in our twin_prime_entanglement.py and correctly attributed to Mertens smoothness.

**Conclusion:** The DeltaW correlation at twin primes is a trivial consequence of DeltaW being a smooth function of p. Any two nearby primes show similar DeltaW. Nothing is special about gap = 2.

## Q2: Does the bridge identity give anything for twin primes?

**No.**

The bridge identity states: sum of e^{2*pi*i*p*f} over F_{p-1} = M(p) + 2.

For twin primes (p, p+2), we have two bridge identities operating on DIFFERENT Farey sequences:
- Over F_{p-1}: gives M(p) + 2
- Over F_{p+1}: gives M(p+2) + 2

We tested the "non-standard" sum of e^{2*pi*i*(p+2)*f} over F_{p-1} (same sequence as p's bridge). It does NOT equal M(p+2) + 2 and shows no useful closed form. For p = 43, it equals -26; for p = 73, it equals -33; for p = 97, it equals -40. These grow roughly linearly and have no identifiable structure.

The sum of e^{2*pi*i*2*f} over F_{p-1} (the "gap factor") is always a small negative integer (typically -3 to -6) but varies irregularly and does not factor the problem.

**Why this fails fundamentally:** Combining bridge identities for p and p+2 requires understanding how exponential sums change when phi(p) + phi(p+1) new fractions are inserted. This is as hard as understanding M(p) itself -- which is equivalent to the prime number theorem and beyond.

## Q3: Connection to Zhang-Maynard-Tao?

**No useful connection.**

The Zhang-Maynard-Tao approach to bounded gaps uses:
1. The Bombieri-Vinogradov theorem (distribution of primes in arithmetic progressions)
2. Selberg sieve with optimized weights
3. Multidimensional sieve methods (Maynard-Tao)

Our per-step analysis gives information about how the Farey sequence changes at primes. Specifically:
- B + C decomposition measures geometric injection effects
- D(f) measures rank deviation
- M(p) controls the sign through the bridge identity

None of these provide sieve-like information. A sieve needs to detect whether n is prime by looking at its divisibility. Our quantities measure how a *known* prime p reorganizes the Farey sequence -- they presuppose primality rather than detecting it.

The M(p) connection is also unhelpful: M(p) and M(p+2) are related by M(p+2) = M(p) + mu(p+1) - 1 (since mu(p+2) = -1 for prime p+2). For twin primes with p >= 5, p+1 is always divisible by 6, so mu(p+1) = 0 about 71% of the time. But this is just the Mertens function, which is already deeply studied and does not yield twin prime results.

## Q4: Known connections in the literature

**None found.**

Web searches for "Farey sequence twin primes", "Farey fractions prime gaps", and "Wasserstein distance prime gaps" found no direct connections. The relevant literature includes:

- Boca-Cobeli-Zaharescu: studied gap distribution of Farey fractions and the BCZ map, with connections to SL(2,Z) and horocycle flows. Their work concerns the *internal* gap structure of Farey sequences, not prime gaps.
- Farey-Riemann connection: the Franel-Landau criterion relates Farey discrepancy to RH, which in turn has implications for prime gaps. But this is through RH as an intermediary -- there is no *direct* Farey-to-twin-primes path that bypasses RH.
- Sieve methods use Farey-adjacent tools (Ramanujan sums, Kloosterman sums) but not the Farey sequence per se.

## Why there is no connection (analytical argument)

The fundamental issue is one of **information content**:

1. **DeltaW(p) is a global statistic** that measures how well the Farey sequence at order p approximates the uniform distribution. It encodes information about ALL primes up to p, not about the local structure around p.

2. **Twin primality is a local property** -- whether p+2 is prime depends on the arithmetic of p+2, not on the cumulative distribution of fractions with denominators up to p.

3. **The bridge identity connects to M(p)**, which is the sum of the Mobius function. Understanding M(p) well enough to detect twin primes would essentially require solving problems at least as hard as the twin prime conjecture itself.

4. **The per-step decomposition WN(p) = WN(p-1) + B + C - 1 + D** depends on how p reorganizes existing fractions. For twin primes, p+2 reorganizes F_{p+1}, which already includes the fractions from p. But the interaction between consecutive prime injections is controlled by the totient function phi(p+1), which for twin primes means phi(p+1) = phi of a composite divisible by 6. This is standard number theory, not a new insight.

## Classification

- **Autonomy:** A (autonomous investigation)
- **Significance:** Level 0 (negative result, no novelty)
- **Verification status:** Fully validated (the negative result is robust -- we checked 1,222 twin pairs and found the null hypothesis holds)

## Recommendation

**Do not pursue this direction.** The per-step discrepancy framework is a tool for understanding how the Farey sequence evolves, not a tool for detecting local prime patterns. Twin primes require sieve methods or L-function machinery, neither of which emerges from our framework.

The only honest statement is: "DeltaW(p) and DeltaW(p+2) are highly correlated for twin primes, but equally correlated for any close prime pair. This is a smoothness property of DeltaW, not a twin prime phenomenon."
