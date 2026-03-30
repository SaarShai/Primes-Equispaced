# Per-Step Increment Strategy Applied to Other Open Problems

**Date:** 2026-03-30
**Context:** Our key methodological insight in Farey discrepancy research was to study
the per-step change DeltaW(N) rather than the cumulative W(N). This revealed the
M(p) <-> DeltaW(p) connection and exposed arithmetic structure invisible in the total.

**Core principle:** When a cumulative quantity is hard to control, study its increments.
The increment may decompose into arithmetic components with tractable structure.

---

## 1. Goldbach's Conjecture

**Standard formulation:** Every even n >= 4 is a sum of two primes.

**Per-step formulation:** Define r(n) = #{(p,q) : p+q = n, p,q prime} (Goldbach
representation count). Study Delta_r(n) = r(n+2) - r(n).

**What this buys you:** The total r(n) is controlled by the singular series S(n) and
is approximately n/log^2(n) times a product over odd prime divisors of n. The
*difference* Delta_r(n) isolates the effect of changing the arithmetic environment
by 2 -- which primes newly become available, which get removed.

**Explicit structure:** When going from n to n+2, the pairs (p, n-p) shift to
(p, n+2-p). A representation is gained when n+2-p becomes prime while n-p was not,
and lost in the reverse case. So:

  Delta_r(n) = #{p prime : n+2-p prime, n-p composite} - #{p prime : n-p prime, n+2-p composite}

This is a *sieve-type* difference. It counts how many primes p have the property that
shifting the complementary slot by 2 crosses a prime/composite boundary.

**Connection to our work:** This is structurally analogous to DeltaW. In Farey
sequences, inserting a new fraction at step N changes the local discrepancy by an
amount controlled by Mobius-weighted terms. Here, the "insertion" is the shift by 2,
and the "Mobius structure" comes from the sieve weights.

**Is this genuinely new?** Partially. The function r(n) and its fluctuations are
well-studied (Hardy-Littlewood, Goldbach-Vinogradov). But framing Delta_r as a
sieve-theoretic *boundary crossing count* is not standard. The closest existing work
is the study of r(n) modulo small primes and the "Goldbach comet" visualization.
The explicit decomposition above as a difference of two prime-counting sums in
complementary residue classes could be new as a formalization.

**Feasibility: 3/5** -- The objects are well-studied, but the per-step decomposition
might yield new conditional results or better heuristics for where r(n) is small.

---

## 2. Twin Prime Conjecture

**Standard formulation:** There are infinitely many primes p with p+2 also prime.

**Per-step formulation:** Define pi_2(x) = #{p <= x : p and p+2 both prime}. The
per-step increment is:

  Delta_pi_2(n) = pi_2(n) - pi_2(n-1) = 1 if n and n+2 are both prime, 0 otherwise.

**Problem:** This is trivially the indicator function of twin primes. The "increment"
is just the thing we want to study. There is no decomposition gain.

**Better reformulation:** Instead, study the *gap function* g(n) = p_{n+1} - p_n
where p_n is the n-th prime. Then study Delta_g(n) = g(n+1) - g(n), the second
difference of the prime sequence. Twin primes correspond to g(n) = 2. The question
becomes: does Delta_g take values that force g to return to 2 infinitely often?

**What this buys you:** Delta_g encodes the "acceleration" of the prime-gap sequence.
Cramer's model predicts g(n) ~ log^2(p_n) on average, but the fluctuations of
Delta_g could reveal oscillatory structure. If Delta_g has a provable tendency to
be negative after large gaps (regression to mean), that would give bounded gaps
unconditionally.

**Connection to Maynard-Tao:** Zhang (2013) and Maynard (2015) proved bounded gaps
via a different approach (GPY sieve). The per-step analysis of Delta_g might
connect to their work by giving a dynamical interpretation of why gaps cannot stay
large forever.

**Is this genuinely new?** The second difference Delta_g is studied in prime gap
statistics, but not typically as a tool for proving bounded gaps. The "regression
to mean" interpretation is heuristic, not rigorous. This is more of a reframing
than a new result.

**Feasibility: 2/5** -- The trivial increment is useless; the second-difference
approach is interesting heuristically but far from yielding new theorems.

---

## 3. Zeros of zeta(s) -- Montgomery Pair Correlation

**Standard formulation:** The Riemann Hypothesis asserts all nontrivial zeros of
zeta(s) lie on Re(s) = 1/2.

**Per-step formulation:** Let gamma_n be the n-th zero on the critical line. Study:

  Delta_gamma(n) = gamma_{n+1} - gamma_n (consecutive spacings)

**Status:** This IS the well-studied problem. Montgomery (1973) conjectured that the
pair correlation of normalized spacings matches GUE random matrices. This was
spectacularly confirmed numerically by Odlyzko (1987).

**What our perspective adds:** In the Farey case, we found that DeltaW decomposes
into Mobius-weighted terms at specific fractions. The analogous question for zeros
is: does Delta_gamma decompose into contributions from specific primes?

Actually, yes -- this is essentially the explicit formula. The zero spacings are
controlled by sums over primes via:

  sum_{gamma} x^{i*gamma} = -sum_{n} Lambda(n)/sqrt(n) * delta(x - log n) + ...

So the spacing between zeros is already understood as a Fourier-dual of the prime
distribution. Our "per-step" insight is exactly the classical explicit formula in
this context.

**Is this genuinely new?** No. This is one of the most developed areas in analytic
number theory. Montgomery pair correlation, GUE hypothesis, Odlyzko's computations,
and the explicit formula connection are all thoroughly studied. Our Farey increment
approach is essentially rediscovering the explicit formula from a different angle.

**Feasibility: 1/5** -- Everything here is known. The value is pedagogical: our
Farey work provides an elementary, concrete model of the same phenomenon that the
explicit formula describes abstractly.

---

## 4. Partition Function p(n)

**Standard formulation:** p(n) counts the number of partitions of n.

**Per-step formulation:** Delta_p(n) = p(n) - p(n-1).

**Combinatorial meaning:** A partition of n either contains the part 1 or it doesn't.
Those that don't are counted by p(n) - p(n-1)... wait, that's not right either.

Actually: p(n) - p(n-1) = #{partitions of n with at least one part equal to 1}?
No. Consider: p(4) = 5 (4, 3+1, 2+2, 2+1+1, 1+1+1+1), p(3) = 3 (3, 2+1, 1+1+1).
Delta = 2. Partitions of 4 containing a 1: {3+1, 2+1+1, 1+1+1+1} = 3. So Delta != that.

**Correct interpretation:** By the generating function, sum p(n)x^n = prod 1/(1-x^k).
Then sum Delta_p(n) x^n = (1-1/x) * prod 1/(1-x^k), which doesn't simplify cleanly.

More useful: p(n) - p(n-1) = #{partitions of n where the smallest part is > 1}...
No, that's also wrong. Let's be precise.

There's a bijection: partitions of n = (partitions of n with smallest part 1) union
(partitions of n with smallest part > 1). If we remove one 1 from each partition
with smallest part 1, we get a partition of n-1. This gives an injection from
{partitions of n with a part 1} -> {partitions of n-1}. It's actually a bijection.
So #{partitions of n with a part 1} = p(n-1).

Therefore: Delta_p(n) = p(n) - p(n-1) = #{partitions of n with no part equal to 1}
                       = q(n), the number of partitions of n into parts >= 2.

**This is clean and known.** But the interesting question is: what does the
*sequence* of Delta_p(n) look like? By Hardy-Ramanujan asymptotics:

  p(n) ~ exp(pi*sqrt(2n/3)) / (4n*sqrt(3))

So Delta_p(n)/p(n) -> 0 (the growth rate slows), and more precisely:

  Delta_p(n) ~ p(n) * pi/(2*sqrt(6n)) [by differentiating the asymptotic]

**Per-step structure:** The ratio Delta_p(n)/p(n) ~ pi/(2*sqrt(6n)) is monotonically
decreasing. Unlike the Farey case where DeltaW oscillates with rich arithmetic
structure, Delta_p is smooth. The partition function lacks the Mobius-type
cancellation that makes DeltaW interesting.

**Where arithmetic enters:** Ramanujan's congruences (p(5n+4) = 0 mod 5, etc.)
suggest studying Delta_p modulo small primes. The per-step change
Delta_p(n) mod 5 = p(n) mod 5 - p(n-1) mod 5 would reveal the "arithmetic texture"
of partition congruences. This IS potentially interesting and connects to Ono's
work on partition congruences.

**Is this genuinely new?** The identity Delta_p = q (partitions into parts >= 2)
is classical. Studying Delta_p mod small primes in connection with Ramanujan
congruences is partially explored but could yield new computational insights.

**Feasibility: 3/5** -- The mod-p per-step analysis is tractable and might reveal
new patterns in partition congruences, even if the continuous asymptotics are smooth.

---

## 5. Erdos Discrepancy Problem

**Standard formulation (Tao 2015):** For any sequence f: N -> {-1, +1} and any C,
there exist n, d such that |sum_{j=1}^{n} f(j*d)| > C.

**Per-step formulation:** Fix d and define S_d(n) = sum_{j=1}^{n} f(j*d). The
per-step increment is:

  Delta S_d(n) = f((n+1)*d) = +/- 1

This is trivially the sequence itself evaluated at multiples of d. No decomposition
gain for fixed d.

**Better approach:** Vary d. For fixed n, define F(d) = sum_{j=1}^{n} f(j*d). Then:

  Delta_d F(d) = F(d+1) - F(d) = sum_{j=1}^{n} [f(j(d+1)) - f(jd)]

This measures how the partial sum changes when we shift the common difference.
Each term f(j(d+1)) - f(jd) compares the sequence at two points separated by j.

**Connection to multiplicativity:** Tao's proof uses the Elliott conjecture and
logarithmic averages of multiplicative functions. The "per-step in d" formulation
connects to how multiplicative structure propagates: if f were completely
multiplicative, then f(jd) = f(j)f(d) and the sums would factor. The failure of
this factoring IS the mechanism Tao exploits.

**What our perspective adds:** In the Farey case, DeltaW decomposes into
contributions from specific denominators. Analogously, Delta_d F decomposes into
contributions from specific "frequency components" j. If f has multiplicative
structure, these components interact via Dirichlet convolution -- the same algebraic
framework as our Mobius-weighted Farey increments.

**Is this genuinely new?** The connection between Erdos discrepancy and
multiplicative number theory is Tao's key insight. Our per-step-in-d formulation
is a modest repackaging. However, the *explicit analogy* between Farey increments
(Mobius-weighted, denominator-by-denominator) and Erdos discrepancy increments
(multiplicative, d-by-d) could be a useful pedagogical bridge and might suggest
quantitative improvements.

**Feasibility: 2/5** -- Tao's proof is highly technical (entropy decrement argument).
The per-step perspective is unlikely to simplify it, but might provide intuition
for extensions (e.g., to other groups or higher-dimensional discrepancy).

---

## 6. Collatz Conjecture

**Standard formulation:** For any n in N, iterating n -> n/2 (if even), n -> 3n+1
(if odd) eventually reaches 1.

**Per-step formulation:** This IS already a per-step problem. The natural question
is not about a cumulative quantity but about the trajectory {n, T(n), T^2(n), ...}.

**The missing piece:** What's the "global functional" analogous to W(N) in Farey
sequences? Define:

  C(N) = #{n <= N : the Collatz sequence starting at n reaches 1}

Then Delta_C(N) = C(N) - C(N-1) = 1 if the Collatz conjecture holds for N, 0
otherwise. Again trivially the thing we want to prove.

**Better global functional:** Consider the *total stopping time* function:

  sigma(n) = min{k : T^k(n) < n}

Then S(N) = sum_{n=1}^{N} sigma(n) is a cumulative "total effort" to verify Collatz
up to N. The per-step increment is Delta_S(N) = sigma(N+1), which again is just
the stopping time of the next number.

**Where structure lives:** The interesting per-step quantity in Collatz is the
*parity sequence*. For a starting value n, the sequence of even/odd decisions
encodes the trajectory completely. The "2-adic" perspective says: the trajectory
is determined by n mod 2^k for increasing k. This IS a per-step decomposition
in the 2-adic digits of n.

**Farey analogue:** In Farey sequences, inserting fractions with denominator N
changes W by an amount determined by Mobius(N) and the position of N in the
Stern-Brocot tree. For Collatz, the analogue would be: the trajectory of N is
determined by N's position in a tree of 2-adic approximations. The "Collatz tree"
(where each n has predecessors 2n and (n-1)/3 if n = 1 mod 3) IS this structure.

**Is this genuinely new?** The 2-adic and tree perspectives on Collatz are known
(Lagarias survey, Kontorovich-Miller). The explicit analogy with Farey insertion
is new but may be superficial -- the algebraic structures (Mobius inversion vs
2-adic valuation) are quite different.

**Feasibility: 1/5** -- Collatz is notoriously resistant to all known techniques.
The per-step perspective doesn't add leverage because the problem is already
inherently per-step. The "global functional" approach might be interesting for
statistical results (Terras, Borovkov-Pfeifer type) but won't crack the conjecture.

---

## 7. ABC Conjecture / Radical Function

**Standard formulation:** For coprime a + b = c, rad(abc) >= c^{1-epsilon} for
all epsilon > 0, with finitely many exceptions.

**Per-step formulation:** Fix a = 1 and study c = b + 1 (consecutive integers).
Define R(n) = rad(n(n+1)). Then:

  Delta_R(n) = rad((n+1)(n+2)) - rad(n(n+1))

Since n+1 appears in both terms, this telescopes partially:

  Delta_R(n) = rad((n+1)(n+2)) - rad(n(n+1))

The radical is NOT additive or multiplicative over products in a useful way, so
this doesn't simplify algebraically. But we can ask: when is Delta_R large negative?
That means rad(n(n+1)) >> rad((n+1)(n+2)), i.e., n(n+1) is "rougher" (more distinct
prime factors) than (n+1)(n+2). This connects to smooth number distribution.

**Better per-step approach:** Study the *quality* q(a,b,c) = log(c)/log(rad(abc))
for the family a = 1, b = n, c = n+1. Then:

  q(n) = log(n+1) / log(rad(n(n+1)))

and Delta_q(n) = q(n+1) - q(n) measures how the "ABC quality" changes at
consecutive integers. High-quality ABC triples (q > 1) are exactly the exceptions
the conjecture allows finitely many of.

**Arithmetic content of Delta_q:** When n+2 is a prime power (smooth radical),
q(n+1) jumps up. When n+2 is squarefree with many factors, q(n+1) drops. The
per-step change is controlled by the factorization of the "new" number n+2
entering the window.

**Connection to our work:** In the Farey case, DeltaW(p) for prime p is controlled
by M(p). Here, Delta_q(n) is controlled by the factorization of n+2. Both are
"local arithmetic data controlling global discrepancy." The analogy is:

  Farey: Mobius function (at denominator N) controls DeltaW(N)
  ABC:   Factorization type (of n+2) controls Delta_q(n)

**Is this genuinely new?** The study of ABC quality along consecutive integers
exists in the computational ABC conjecture literature (Browkin-Brzezinski, de Smit).
The explicit per-step formulation and the analogy with Farey increments appear to
be new, but the connection may be too loose to yield theorems.

**Feasibility: 2/5** -- The analogy is suggestive but the algebraic structures are
too different (Mobius inversion vs radical function) for techniques to transfer.
Could yield interesting computational explorations.

---

## Summary Table

| Problem | Per-step object | Genuine novelty? | Feasibility | Key insight |
|---------|----------------|-------------------|-------------|-------------|
| Goldbach | Delta_r = boundary crossing count | Partially new | 3/5 | Sieve-theoretic decomposition of representation changes |
| Twin primes | Delta_g (2nd difference of primes) | Reframing only | 2/5 | "Regression to mean" interpretation of gap dynamics |
| Zeros of zeta | Consecutive spacings | Known (Montgomery) | 1/5 | Our approach rediscovers the explicit formula |
| Partitions | Delta_p = parts >= 2 count | Classical, but mod p new | 3/5 | Mod-p increments reveal congruence structure |
| Erdos discrepancy | Delta_d F (shift in d) | Modest repackaging | 2/5 | Multiplicative structure as Farey-type decomposition |
| Collatz | Already per-step | Known frameworks | 1/5 | 2-adic tree analogous to Stern-Brocot/Farey |
| ABC conjecture | Delta_q (quality change) | Formulation new, content thin | 2/5 | Factorization type controls local quality, like Mobius controls DeltaW |

---

## Most Promising Directions

**Tier 1 (worth exploring computationally):**
- **Goldbach Delta_r:** The sieve-theoretic boundary crossing decomposition is
  concrete enough to compute and might reveal patterns in where r(n) is small.
  Connection to our work: both involve Mobius-type weights controlling a
  per-step arithmetic change.
- **Partition Delta_p mod p:** The interaction between Ramanujan congruences and
  per-step increments is tractable and connects to active research (Ono, Ahlgren).

**Tier 2 (worth thinking about more):**
- **Erdos discrepancy Delta_d:** The analogy with Farey increments is the most
  structurally faithful. Both involve: (a) a discrepancy measure, (b) arithmetic
  weights (Mobius vs multiplicative), (c) per-step decomposition revealing hidden
  structure. If we could find quantitative improvements to Tao's result using
  this perspective, that would be significant.
- **ABC Delta_q:** Computationally accessible. Could map the "landscape" of ABC
  quality along consecutive integers and look for patterns.

**Tier 3 (pedagogical value only):**
- **Zeros of zeta:** Our Farey increment work is a concrete, elementary model of
  what the explicit formula does abstractly. This has expository value.
- **Twin primes, Collatz:** The per-step perspective doesn't add genuine leverage.

---

## Meta-Observation: When Does the Per-Step Strategy Work?

The per-step increment strategy works best when:

1. **The cumulative quantity has hidden cancellation.** W(N) is small because of
   massive cancellation; DeltaW reveals the cancellation mechanism. Similarly,
   r(n) involves cancellation in the singular series.

2. **The increment decomposes into arithmetic components.** DeltaW decomposes into
   Mobius-weighted terms at specific denominators. For the strategy to work
   elsewhere, the increment must similarly factor through number-theoretic functions.

3. **The problem is NOT already formulated per-step.** Collatz is inherently
   sequential; the per-step view adds nothing. The strategy is powerful precisely
   when it reframes a cumulative/existential question as a dynamical one.

4. **There is a natural parameterization to increment along.** For Farey: the
   order N. For Goldbach: the even number n. For ABC: consecutive integers. The
   choice of parameterization matters -- it determines what arithmetic enters the
   increment formula.

The deepest analogy is with the **explicit formula** in analytic number theory:
zeros <-> primes via Fourier duality. Our DeltaW work is an elementary,
combinatorial shadow of this duality. Problems where the explicit formula is
the natural tool (zeros of zeta, Goldbach via circle method) are exactly where
the per-step strategy has classical analogues. Problems without this structure
(Collatz, ABC) are where the strategy is weakest.

---

**Classification:** C1 (Collaborative, Minor Novelty) -- This is a creative
exploration document, not a research result. The Goldbach and partition
directions could potentially reach C2 if pursued computationally and analytically.
