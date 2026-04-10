# Literature Search: Is "Studying Increments Rather Than Totals" Novel?

**Date:** 2026-03-30
**Question:** Is studying Delta-W(N) = W(N) - W(N-1) for Farey sequences truly a novel perspective, or is the general strategy of studying increments common across number theory?

---

## Executive Summary

**The general strategy of studying increments is NOT novel in number theory.** In many core areas, the "incremental" or "per-step" viewpoint is in fact the *primary* object of study, with summatory functions being derived quantities. However, the specific application to Farey sequence discrepancy -- tracking how discrepancy changes when a single new order is added -- appears to be genuinely underexploited. The novelty is in the *specific combination* (Farey discrepancy + per-step analysis + connection to Mertens/Mobius), not in the general methodology.

**Honest assessment:** Claiming that "studying increments rather than totals" is a novel strategy would be an overstatement. What is potentially novel is applying it to Farey discrepancy specifically, where the classical literature focuses on D_N as a function of N rather than on Delta-D_N.

---

## Area-by-Area Analysis

### 1. Prime Counting: psi(x) - psi(x-1) vs psi(x)

**Verdict: WELL-STUDIED. The increment IS the primary object.**

The Chebyshev function psi(x) = sum_{n <= x} Lambda(n) is the *summatory* function. Its increment psi(x) - psi(x-1) = Lambda(x), the von Mangoldt function, which equals log p when x = p^k and 0 otherwise.

The von Mangoldt function Lambda(n) is one of the most studied objects in all of analytic number theory. The entire explicit formula of von Mangoldt (1895) connects psi(x) to the zeros of the Riemann zeta function. The prime number theorem is equivalent to psi(x) ~ x.

Similarly, pi(n) - pi(n-1) is just the characteristic function of the primes -- the most studied function in mathematics.

**The "incremental" viewpoint here is literally the starting point of the theory.** Nobody would claim novelty in studying Lambda(n) rather than psi(x). The relationship between them is fundamental.

### 2. Sieve Theory: Per-Step Sieving Effects

**Verdict: WELL-STUDIED in algorithmic sieve theory; MIXED in analytic sieve theory.**

In the Sieve of Eratosthenes, the per-step effect of sieving by each prime p is studied explicitly: it removes n/p multiples, and the total sieving time is proportional to n * sum(1/p) ~ n * log(log(n)). The incremental effect of each prime's sieve is well-understood.

In analytic sieve theory (Brun, Selberg, etc.), the framework is about bounding the count of survivors after sieving. The "parity barrier" -- the fundamental inability of sieves to distinguish numbers with odd vs even numbers of prime factors -- is understood as a per-step phenomenon. Kevin Ford's lecture notes show this is well-trodden territory.

Incremental/online sieve constructions are studied algorithmically (Sorenson's "compact incremental prime sieves" being O(1/log log n)-incremental). The concept of incrementality has been formalized in this context.

### 3. Additive Number Theory: Partition Function Increments

**Verdict: PARTIALLY STUDIED. The increment p(n) - p(n-1) is known but not the focus.**

The partition function p(n) is strictly increasing (p(n) > p(n-1) for n >= 2), but the primary recurrence is Euler's pentagonal number theorem:

    p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + ...

This is NOT a simple first-difference formula. The increments p(n) - p(n-1) grow rapidly (exponentially in sqrt(n)) but have no known simple closed form. The field focuses on congruence properties (Ramanujan congruences mod 5, 7, 11) and asymptotics (Hardy-Ramanujan-Rademacher) rather than on the first differences directly.

**The increment p(n) - p(n-1) is not a primary object of study.** But this is because it has no clean closed form -- not because nobody thought to look at it.

### 4. Distribution of Sequences: Per-Term Discrepancy Changes

**Verdict: PARTIALLY STUDIED. This is closest to our claim of novelty.**

The classical theory of equidistribution (Weyl, Erdos-Turan) focuses on the discrepancy D_N of the first N terms of a sequence. The Erdos-Turan inequality bounds D_N in terms of exponential sums.

**What is studied:** D_N as a function of N, its rate of decay, and its connection to the Riemann Hypothesis (Franel-Landau theorem for Farey sequences).

**What is less studied:** Delta-D_N = D_N - D_{N-1}, i.e., how much the discrepancy changes when one more element is added.

For Farey sequences specifically, Dress (1999) proved that the star-discrepancy D_Q = 1/Q exactly. This means Delta-D = 1/N - 1/(N+1) = 1/(N(N+1)) -- a trivially computable quantity for the supremum discrepancy. But the *pointwise* discrepancy at each Farey fraction, and how the insertion of phi(N+1) new fractions redistributes the local errors, is a finer question.

**Key finding:** The "online thinning" literature (Springer, 2018) studies how discrepancy evolves as points are added one at a time. This is directly analogous to the per-step viewpoint. But this work is about random sequences with online selection, not about deterministic number-theoretic sequences like Farey fractions.

**The specific study of how Farey discrepancy decomposes per-step (per prime insertion) appears to be genuinely sparse in the literature.**

### 5. Arithmetic Functions: Delta-f(n) = f(n) - f(n-1)

**Verdict: WELL-STUDIED for specific functions; the general operator is standard.**

The finite difference operator Delta-f(n) = f(n+1) - f(n) is a classical object in discrete calculus and combinatorics. It is the discrete analogue of differentiation.

**For the Mertens function:** M(n) - M(n-1) = mu(n), the Mobius function. This is completely standard -- the Mertens function IS the summatory function of mu. Studying mu(n) is not "studying increments" in any novel sense; it is studying the original function.

**For the Euler totient:** phi(n) - phi(n-1) is highly irregular because consecutive integers have completely different prime factorizations. Heath-Brown (1984) studied the divisor function d(n) at consecutive integers. The behavior of arithmetic functions at consecutive integers is an active research area.

**For the divisor function:** The oscillation of summatory functions is extensively studied. Martin and Yip (2025) published oscillation results for summatory functions of "fake mu's" -- multiplicative functions valued in {-1, 0, 1}.

**The key point:** The difference operator itself is standard. What matters is whether applying it to a *specific* function yields new insight.

---

## The Specific Claim: Delta-W(N) for Farey Sequences

### What the literature covers:
- D_N (total discrepancy of Farey sequence of order N) -- extensively studied (Niederreiter 1973, Dress 1999, Franel-Landau, Koleda, and many others)
- The Franel-Landau connection: sum of |deviations| and sum of squared deviations are equivalent to RH
- How Farey sequences grow: phi(N) new fractions inserted at each step -- well-known
- The mediant property controlling where new fractions are inserted -- classical

### What the literature does NOT obviously cover:
- Decomposing the total discrepancy change Delta-W(N) = W(N) - W(N-1) into contributions from each newly inserted fraction
- Connecting Delta-W(N) specifically to M(N) (the Mertens function evaluated at the order)
- Using the per-step discrepancy as a diagnostic for prime-specific arithmetic behavior
- The "Farey discrepancy as a discrete derivative" perspective as a systematic framework

### Caveats:
- The connection between Farey discrepancy and M(N) is implicit in the Franel-Landau theorem. The theorem literally states that bounds on deviations of Farey fractions are equivalent to bounds on M(N). Our Delta-W may be a repackaging of known relationships.
- Not finding something in a web search does not mean it has not been done. Specialized results in uniform distribution theory may exist in papers by Niederreiter, Dress, Huxley, or others that are not easily searchable.
- The "per-step" framing may be a perspective shift on known material rather than a genuinely new mathematical object.

---

## Analogues in Other Fields

| Domain | Increment | Status |
|--------|-----------|--------|
| Prime counting | Lambda(n) = psi(n) - psi(n-1) | **Primary object**, not novel |
| Mertens function | mu(n) = M(n) - M(n-1) | **Primary object**, not novel |
| Partition function | p(n) - p(n-1) | Known but not primary focus (no closed form) |
| Low-discrepancy seqs | D_N - D_{N-1} | Studied in "online" settings, sparse for Farey |
| Divisor functions at consecutive n | d(n), d(n+1) | Active research area (Heath-Brown 1984, etc.) |
| Sieve per-step effects | Per-prime sieving contribution | Well-studied algorithmically |
| Discrete calculus generally | Delta-f(n) operator | Fully standard framework |

---

## Conclusions

### What IS potentially novel:
1. The specific object Delta-W(N) for Farey discrepancy, decomposed per newly-inserted fraction
2. The empirical connection between Delta-W(N) and M(N) at prime orders as a diagnostic
3. Using per-step analysis to identify which primes are "well-behaved" vs "badly-behaved" for equidistribution

### What is NOT novel:
1. The general strategy of studying increments -- this is standard discrete calculus
2. The idea that f(n) and its summatory function F(n) carry equivalent information -- this is the foundation of Abel summation
3. The connection between Farey discrepancy and the Mertens/Mobius function -- this is Franel-Landau (1924)
4. Studying arithmetic functions at consecutive integers -- active area since at least Heath-Brown (1984)

### Recommended framing:
Do NOT claim: "Studying increments rather than totals is a novel strategy in number theory."
DO claim: "While the incremental viewpoint is standard in many areas of number theory, the specific decomposition of Farey sequence discrepancy changes Delta-W(N) = W(N) - W(N-1) per inserted fraction, and its empirical correlation with the Mertens function at prime orders, appears to be a new application of this classical technique."

### Risk level for overstatement: HIGH
Many of our "novel" findings have previously been overstatements (3DGS, terrain LOD, Kirkwood, etc.). The claim about novelty of increments should be carefully scoped to the specific Farey application, not presented as a general methodological innovation.

---

## Key References

- Franel, J. "Les suites de Farey et le probleme des nombres premiers." (1924)
- Dress, F. "Discrepance des suites de Farey." J. Theor. Nombres Bordeaux (1999)
- Niederreiter, H. "The distribution of Farey points." Math. Ann. (1973)
- Heath-Brown, D.R. "The Divisor Function at Consecutive Integers." Mathematika 31, 141-149 (1984)
- Martin, G. and Yip, C. "Oscillation results for the summatory functions of fake mu's." Canadian J. Math. (2025)
- Tao, T. "The Erdos discrepancy problem." arXiv:1509.05363 (2015)
- Sorenson, J. "Two Compact Incremental Prime Sieves." arXiv:1503.02592 (2015)
- "The power of online thinning in reducing discrepancy." Prob. Theory Rel. Fields (2018)
- "Maximum mean discrepancies of Farey sequences." Acta Math. Hungarica (2025)
- Ford, K. "Sieve Methods Lecture Notes." (2023)
