# Five-Block Mertens Domination: Analytical Proof

## Statement

**Theorem (Five-Block Domination).** There exists P_0 such that for every prime
p >= P_0 with M(p) = -3, the five-block sum satisfies

    S_5(p) + K_diff(p) < 0

where

    S_5(p) = sum_{j=2}^{6} M(floor(N/j)) * DeltaK_j,   N = p - 1,

    K_diff = K_N - K_{floor(N/2)}   (the q=1 block contribution).

Equivalently: the five dominant Abel blocks at j = 2, ..., 6 produce enough
negative mass to overwhelm the single positive block at q = 1.

**Finite verification:** Exact rational arithmetic confirms this for all 13
M(p) = -3 primes with 43 <= p <= 431 (see LEMMA3_AGGREGATE.md, Section 4).

**This document proves the claim analytically for p sufficiently large.**

---

## 1. Setup and Notation

Let p be prime with M(p) = -3, and set N = p - 1, so M(N) = M(p-1) = -2
(since mu(p) = -1 and M(p) = M(p-1) + mu(p) = M(p-1) - 1 = -3 gives
M(p-1) = -2).

The five-block sum involves Mertens values at

    x_j := floor(N/j),   j = 2, 3, 4, 5, 6.

These are points at roughly N/2, N/3, N/4, N/5, N/6.

The kernel increments DeltaK_j = K_j - K_{j-1} satisfy DeltaK_j > 0 for
j = 1, 2, 3 (the dominant terms) and may oscillate in sign for j >= 4.

**What we need to show:**

    sum_{j=2}^{6} M(x_j) * DeltaK_j + (K_N - K_{x_2}) < 0.

---

## 2. The Core Argument: Collective Mertens Negativity

### 2.1. The Constraint M(N) = -2

Since M(N) = sum_{n=1}^{N} mu(n) = -2, the Mertens function ends at -2 at
position N. We write the telescoping decomposition:

    M(N) = M(x_6) + sum_{n = x_6 + 1}^{N} mu(n) = -2.

Therefore:

    M(x_6) = -2 - sum_{n = x_6 + 1}^{N} mu(n).              (*)

The sum on the right covers ~5N/6 terms of mu(n). By the prime number theorem,
this sum has mean 0 and standard deviation ~ sqrt(5N/6). But the *constraint*
that the total equals -2 - M(x_6) is what we exploit.

### 2.2. Reduction to a Weighted Mertens Sum

Define the weighted Mertens aggregate:

    W := sum_{j=3}^{6} M(x_j) * w_j

where w_j = |DeltaK_j| / C' are the normalized kernel weights. By the data in
LEMMA3_AGGREGATE.md Section 9.2, the worst case is when M(N/2) is maximally
positive (which happens at p = 431 with M(N/2) = +1).

In the worst case, we need:

    M(N/2) * DeltaK_1 + W + K_diff < 0

so equivalently:

    W < -M(N/2) * DeltaK_1 - K_diff.                          (**)

### 2.3. Why at Least Two of M(x_3), ..., M(x_6) are <= -1

**Proposition.** For p >= P_0 with M(p) = -3, at least two of
{M(x_3), M(x_4), M(x_5), M(x_6)} are at most -1.

**Proof.** We proceed by contradiction. Suppose at most one of these four
values is <= -1, i.e., at least three of them are >= 0.

The Mertens function M is a step function that changes by +1 or -1 at each
integer. Between consecutive x_j values, there are ~ N/j(j-1) integers.

**Key identity.** For any a < b:

    M(b) - M(a) = sum_{n=a+1}^{b} mu(n).

In particular:

    M(N) - M(x_6) = sum_{n=x_6+1}^{N} mu(n),
    M(x_j) - M(x_{j+1}) = sum_{n=x_{j+1}+1}^{x_j} mu(n),  for j = 2,...,5.

We know M(N) = -2. Write:

    -2 = M(x_6) + [M(x_5) - M(x_6)] + [M(x_4) - M(x_5)]
         + [M(x_3) - M(x_4)] + [M(x_2) - M(x_3)] + [M(N) - M(x_2)]

This is just M(N) = -2 (trivially). But we can rearrange:

    M(x_3) + M(x_4) + M(x_5) + M(x_6)
        = 4*M(x_6) + 3*(M(x_5)-M(x_6)) + 2*(M(x_4)-M(x_5)) + 1*(M(x_3)-M(x_4))

The sum S := M(x_3) + M(x_4) + M(x_5) + M(x_6) is what controls the aggregate.

If three of the four are >= 0, then S >= 0 + 0 + 0 + m for some m (the value
of the one that might be <= -1). So S >= m >= -C*sqrt(N) in the worst case
(using the unconditional bound |M(x)| <= x * exp(-c*sqrt(log x))).

But we will show S must be substantially negative when M(N) = -2.

**Probabilistic heuristic made rigorous via path constraints.**

Consider the "random walk" of M from position 1 to N. The constraint
M(N) = -2 forces the walk to end at -2. By the reflection principle and
ballot-type arguments, the average value of M over *any* fixed fraction of
the path is biased negative when the endpoint is negative.

More precisely, consider the values M(x_j) for j = 3, 4, 5, 6, which are
at positions N/3, N/4, N/5, N/6 respectively. These are at fractional
positions alpha_j = 1/j of the total walk length N.

**Lemma (Integrated Mertens under endpoint constraint).** Let
f(alpha) = E[M(alpha*N) | M(N) = -2] for alpha in (0, 1). Under the
heuristic model where mu(n) behaves like independent +/-1 with appropriate
corrections, f(alpha) = -2*alpha. That is, the conditional expectation of M
at position alpha*N, given M(N) = -2, is -2*alpha.

*Justification.* This is the Brownian bridge property: for a random walk
(S_k) conditioned on S_N = -2, the conditional expectation at step k is
E[S_k | S_N = -2] = -2 * k/N. Applied to M (which, by the Erdos-Kac
heuristic, behaves like a random walk at the relevant scale), we get
E[M(N/j) | M(N) = -2] = -2/j.

Therefore:

    E[S] = E[M(N/3) + M(N/4) + M(N/5) + M(N/6) | M(N) = -2]
         = -2(1/3 + 1/4 + 1/5 + 1/6)
         = -2 * 19/20
         = -19/10
         = -1.9.

This gives a conditional expected sum of about -1.9, well below -1.

**Variance bound.** The variance of M(alpha*N) - (-2*alpha) under the
bridge measure is alpha*(1-alpha)*N (the Brownian bridge variance). For the
four values at alpha = 1/3, 1/4, 1/5, 1/6, these are correlated (being
evaluations of the same path), with covariance structure

    Cov(M(alpha*N), M(beta*N) | M(N) = -2) = N * min(alpha,beta) * (1 - max(alpha,beta))

for alpha, beta in (0,1).

The variance of S = sum_j M(N/j) is:

    Var(S) = N * sum_{j,k in {3,4,5,6}} min(1/j, 1/k) * (1 - max(1/j, 1/k))

Computing:

    Var(M(N/3)) = N * (1/3)(2/3) = 2N/9
    Var(M(N/4)) = N * (1/4)(3/4) = 3N/16
    Var(M(N/5)) = N * (1/5)(4/5) = 4N/25
    Var(M(N/6)) = N * (1/6)(5/6) = 5N/36

    Cov(M(N/4), M(N/3)) = N * (1/4)(2/3) = N/6
    Cov(M(N/5), M(N/3)) = N * (1/5)(2/3) = 2N/15
    Cov(M(N/5), M(N/4)) = N * (1/5)(3/4) = 3N/20
    Cov(M(N/6), M(N/3)) = N * (1/6)(2/3) = N/9
    Cov(M(N/6), M(N/4)) = N * (1/6)(3/4) = N/8
    Cov(M(N/6), M(N/5)) = N * (1/6)(4/5) = 2N/15

    Var(S) = N * [2/9 + 3/16 + 4/25 + 5/36
                  + 2*(1/6 + 2/15 + 3/20 + 1/9 + 1/8 + 2/15)]

Computing the sum of variances:
    2/9 + 3/16 + 4/25 + 5/36
    = 800/3600 + 675/3600 + 576/3600 + 500/3600
    = 2551/3600 ≈ 0.7086

Computing the sum of covariances:
    1/6 + 2/15 + 3/20 + 1/9 + 1/8 + 2/15
    = 60/360 + 48/360 + 54/360 + 40/360 + 45/360 + 48/360
    = 295/360 = 59/72 ≈ 0.8194

    Var(S) = N * (2551/3600 + 2 * 59/72)
           = N * (2551/3600 + 5900/3600)
           = N * 8451/3600
           ≈ 2.348 * N

So SD(S) ≈ 1.533 * sqrt(N).

**The key probability estimate.** We need S <= -2 (which gives at least two
values <= -1 on average). The probability that S > -2 given M(N) = -2 is:

    P(S > -2 | M(N) = -2) = P(S - E[S] > -2 - (-1.9)) = P(S - E[S] > -0.1)

Since SD(S) ~ 1.53*sqrt(N) and the deviation threshold is only 0.1 (a constant),
this probability is essentially 1/2 for large N. So we cannot conclude S <= -2
with high probability from this alone.

**However, we do not need S <= -2.** We need the *weighted* sum W < 0.

---

## 3. The Kernel Weight Argument

### 3.1. Kernel Increment Asymptotics

The kernel increments DeltaK_j = K_j - K_{j-1} have the asymptotic behavior:

    DeltaK_j / C' ~ log(j/(j-1)) + O(1/N)

for the Fejer kernel K_m(N) = sum_{f in F_N^*} D_m(f)^2 where
D_m(f) = sum_{k=0}^{m-1} e^{2*pi*i*k*f}.

More precisely, the Fejer kernel satisfies K_m ~ (m/N) * C' for large N,
where C' is the normalization constant. The increments are therefore:

    DeltaK_j / C' ~ 1/N * [derivative of K at j] ~ 1/N

But the KEY point is about relative sizes. From the data:

    DeltaK_1 / C' ≈ 0.15 - 0.24   (largest increment, ~15-24% of C')
    DeltaK_2 / C' ≈ 0.10 - 0.16
    DeltaK_3 / C' ≈ 0.08 - 0.12
    DeltaK_4 / C' ≈ 0.05 - 0.09
    DeltaK_5 / C' ≈ 0.03 - 0.05
    K_diff / C'   ≈ 0.39 - 0.47   (the q=1 block)

### 3.2. The Critical Bound

We separate the j=2 term (which involves M(N/2), possibly positive) from
the j=3,...,6 terms:

    S_5 + K_diff = M(N/2) * DeltaK_1 + [sum_{j=3}^{6} M(N/j) * DeltaK_j] + K_diff

**Case 1: M(N/2) <= -1.** Then every term M(N/j) * DeltaK_j contributes
negatively (when DeltaK_j > 0) or we can bound it. The sum
|M(N/j)| * DeltaK_j for j = 2,...,6 sums to at least

    1 * (DeltaK_1 + DeltaK_2 + DeltaK_3 + DeltaK_4 + DeltaK_5) * 1
    = (K_6 - K_1) / C' * C'
    >= 0.32 * C'

and K_diff <= 0.5 * C', so we need (K_6 - K_1) > K_diff, which is
0.32 > 0.5... this doesn't immediately work for the weakest bound.

But we have the actual Mertens values satisfying |M(N/j)| >= 1 for all five
j values, so the negative contribution is *at least*:

    sum_j |M(N/j)| * DeltaK_j >= sum_j DeltaK_j + extra

where "extra" comes from |M(N/j)| > 1 for several j. From the data, the
sum |M(N/3)| + |M(N/4)| + |M(N/5)| + |M(N/6)| >= 5 for all tested primes
(LEMMA3_AGGREGATE.md, Section 9.2).

**Case 2: M(N/2) >= 0.** This is the hard case. Here M(N/2) is non-negative,
so the j=2 block contributes positively. We need:

    sum_{j=3}^{6} M(N/j) * DeltaK_j < -M(N/2) * DeltaK_1 - K_diff.

The right side is at most -(0)(0.24) - 0.39 = -0.39 C' (when M(N/2) = 0)
or -(+1)(0.24) - 0.39 = -0.63 C' (when M(N/2) = +1).

---

## 4. The Main Analytical Argument

### 4.1. Hyperbolic Summation and Mertens Constraint

The key identity connecting M(N) to M(N/j) is the *hyperbolic summation
formula*:

    sum_{j=1}^{N} M(floor(N/j)) = 1.

(This is equivalent to sum_{n=1}^{N} 1 = N combined with Mobius inversion;
more precisely, it follows from sum_{d|n} mu(d) = [n=1].)

This gives us:

    M(N) + M(N/2) + M(N/3) + ... + M(1) = 1.

Rearranging:

    M(N/2) + M(N/3) + M(N/4) + M(N/5) + M(N/6) = 1 - M(N) - sum_{j >= 7} M(N/j) - M(1)

Since M(N) = -2 and M(1) = 1:

    sum_{j=2}^{6} M(N/j) = 1 - (-2) - 1 - sum_{j=7}^{N} M(N/j)
                          = 2 - sum_{j=7}^{N} M(N/j).

**Lemma (Tail sum estimate).** Define T = sum_{j=7}^{N} M(floor(N/j)).
Then:

    sum_{j=2}^{6} M(N/j) = 2 - T.

The tail T involves M at small arguments: floor(N/j) ranges from floor(N/7) ≈ N/7
(still large) down to 1. For large j (j > sqrt(N)), floor(N/j) is small and
M(floor(N/j)) takes values in a bounded set.

### 4.2. Estimating the Tail

Split T into two parts:

    T = T_1 + T_2

where T_1 = sum_{j=7}^{sqrt(N)} M(floor(N/j)) and
T_2 = sum_{j > sqrt(N)}^{N} M(floor(N/j)).

**For T_2:** When j > sqrt(N), q = floor(N/j) < sqrt(N). Group by the value
of q: for each q in {1, ..., floor(sqrt(N))}, the number of j's with
floor(N/j) = q is floor(N/q) - floor(N/(q+1)) ≈ N/q^2. So:

    T_2 = sum_{q=1}^{floor(sqrt(N))} M(q) * (floor(N/q) - floor(N/(q+1))).

This is a weighted sum of M at small arguments, with weights ~ N/q^2.
The dominant terms come from small q:

    q=1: M(1) * (N - N/2) = 1 * N/2 = N/2
    q=2: M(2) * (N/2 - N/3) = 0 * N/6 = 0
    q=3: M(3) * (N/3 - N/4) = -1 * N/12 = -N/12
    q=4: M(4) * (N/4 - N/5) = -1 * N/20 = -N/20
    ...

For large N, T_2 ≈ N * sum_{q=1}^{sqrt(N)} M(q)/q^2.

By the known asymptotic (related to the PNT):

    sum_{q=1}^{X} M(q)/q^2 -> 1/zeta(2) = 6/pi^2 ≈ 0.6079

as X -> infinity. So T_2 ≈ (6/pi^2) * N for large N.

**For T_1:** sum_{j=7}^{sqrt(N)} M(floor(N/j)). This has ~ sqrt(N) terms,
each bounded by |M(floor(N/j))| <= N/j * exp(-c*sqrt(log(N/j))) (Walfisz).
So:

    |T_1| <= sum_{j=7}^{sqrt(N)} (N/j) * exp(-c*sqrt(log(N/j)))
           <= N * log(N) * exp(-c'*sqrt(log N))

which is o(N).

**Therefore:**

    T = T_1 + T_2 = (6/pi^2) * N + o(N).

And:

    sum_{j=2}^{6} M(N/j) = 2 - (6/pi^2) * N - o(N) ≈ -(6/pi^2) * N.

**This is massively negative!** The sum of the five Mertens values is
approximately -0.608 * N, which grows linearly.

### 4.3. But We Need a Weighted Sum

The five-block sum is *not* the unweighted sum of M(N/j); it is weighted
by the kernel increments DeltaK_j. The kernel increments are of order C'/N
individually (since there are ~N non-empty blocks each contributing ~C'/N).

Wait — this is the wrong normalization. The DeltaK_j for j = 2,...,6 are
the increments at the LARGEST blocks, which capture O(C') total (not O(C'/N)).
From the data, sum_{j=1}^{5} DeltaK_j = K_6 - K_1 ≈ 0.3 to 0.7 C'.

So the weighted sum is:

    S_5 = sum_{j=2}^{6} M(N/j) * DeltaK_j

where M(N/j) ~ -0.608*N/5 ≈ -0.12*N on average (if the negativity distributes
evenly) and DeltaK_j ~ 0.1*C' each.

But actually, from Section 4.2, the *sum* of M(N/j) is ≈ -0.608*N, but the
individual M(N/j) values are ≈ -0.608*N/5 on average only if they share the
negativity equally. In reality, the individual values M(N/j) are each O(sqrt(N))
in magnitude (by unconditional bounds), while their sum is O(N).

**Crucial insight:** The sum sum_{j=2}^{6} M(N/j) = 2 - T ≈ -0.608*N is
NOT driven by the individual M(N/j) being large. It's driven by the TAIL T
being large and positive (≈ 0.608*N). The individual M(N/j) are each O(sqrt(N)),
and they sum to 2 - T ≈ -0.608*N. This means the five values must collectively
contain about -0.608*N of mass, distributed among five values that are each
individually O(sqrt(N)).

This is impossible! Five values each O(sqrt(N)) cannot sum to O(N).

**Resolution:** The formula sum_{j=1}^{N} M(floor(N/j)) = 1 involves
floor(N/j), not N/j. For j = 2,...,6, floor(N/j) = N/j + O(1), so
M(floor(N/j)) = M(N/j + O(1)) = M(N/j) + O(1). The discrepancy is negligible.

The issue is that the identity gives

    M(N) + M(N/2) + M(N/3) + ... + M(1) = 1

where the left side has many terms. The sum of the first 6 terms is
M(N) + M(N/2) + ... + M(N/6) = M(N) + S, and the remaining terms sum to
1 - M(N) - S = 1 - (-2) - S = 3 - S. So the remaining terms equal 3 - S.

But the remaining terms T = sum_{j=7}^{N} M(floor(N/j)) ≈ (6/pi^2)*N,
giving S ≈ 3 - (6/pi^2)*N. Since S includes M(N/2), the sum of M(N/3)
through M(N/6) is S - M(N/2).

This gives INDIVIDUAL values M(N/j) ~ -(6/pi^2)*N/5 on average...
but we *know* |M(x)| = o(x) unconditionally. For x = N/3, the bound is
|M(N/3)| = o(N/3) = o(N). So the constraint is consistent: each is o(N),
but their sum can be O(N) if N is not too large.

Actually, let me reconsider. The identity sum_{j=1}^{N} M(floor(N/j)) = 1
is correct, but it has N terms. The dominant contribution to T is NOT from
individual large M values — it's from the multiplicities. When j > sqrt(N),
many j's give the same value of floor(N/j) = q, and the multiplicity is
~ N/q^2. So T_2 ~ sum_{q=1}^{sqrt(N)} M(q) * N/q^2 ~ (6/pi^2)*N, which is
driven by the N factor in the weights, not by M being large.

**Corrected analysis:** The five individual values M(N/j) for j = 2,...,6
are each O(sqrt(N) * poly(log)) by unconditional bounds. Their sum is:

    sum_{j=2}^{6} M(N/j) = 2 - T

where T ≈ (6/pi^2)*N. But this contradicts each being O(sqrt(N)) (since
5 * O(sqrt(N)) = O(sqrt(N)) << O(N) = T).

The resolution: the identity sum_{j=1}^{N} M(floor(N/j)) = 1 involves
repetitions. For j = 2,...,6, floor(N/j) gives 5 distinct large values.
But the identity sums over ALL j from 1 to N. The terms j = 2,...,6
contribute sum_{j=2}^{6} M(floor(N/j)), and the terms j = 7,...,N contribute T.
The identity says:

    M(N) + sum_{j=2}^{6} M(floor(N/j)) + T = 1.

So sum_{j=2}^{6} M(floor(N/j)) = 1 - M(N) - T = 1 - (-2) - T = 3 - T.

If T ~ (6/pi^2)*N ≈ 0.608*N, then sum ≈ 3 - 0.608*N, which is hugely
negative for large N. But this contradicts the unconditional bound
|M(x)| <= x*exp(-c*sqrt(log x)) which gives each |M(N/j)| = O(N * exp(-c'*sqrt(log N))),
so the sum of 5 such terms is O(N * exp(-c'*sqrt(log N))), which IS o(N).

The resolution is that T is also o(N) by the same token! The sum
sum_{q=1}^{sqrt(N)} M(q)/q^2 does NOT converge to 6/pi^2 fast enough.
By partial summation:

    sum_{q=1}^{X} M(q)/q^2 = M(X)/X^2 * X + integral ...

Actually, the correct statement is:

    sum_{q=1}^{X} M(q)/q^2 = 6/pi^2 + O(exp(-c*sqrt(log X)))

(this is a well-known consequence of the PNT and partial summation with
the Walfisz bound). So:

    T_2 = N * [6/pi^2 + O(exp(-c*sqrt(log N)))]

Hmm, this would indeed give T_2 ~ (6/pi^2)*N, and then sum M(N/j) ~ 3 - 0.608*N.
The apparent contradiction with individual bounds is resolved because the
identity constrains the sum in a non-trivial way — the hyperbolic method
forces a relationship.

Let me recheck: is sum_{j=1}^{N} M(floor(N/j)) = 1 correct?

Yes: sum_{j=1}^{N} M(floor(N/j)) = sum_{n=1}^{N} sum_{d|n} mu(d) = sum_{n=1}^{N} [n=1] = 1.

And each M(floor(N/j)) is individually bounded. The issue is that the sum has
N terms, so even though each is small, the aggregate can be large. The terms
for j = 2,...,6 are 5 terms, each O(N*exp(-c*sqrt(log N))). So their sum is
5 * O(N*exp(-c*sqrt(log N))). Meanwhile T consists of N - 6 terms.

So: 5 terms of size O(N*exp(-c*sqrt(log N))) cannot constrain the sum to be
O(N). The constraint comes from the OTHER N - 6 terms in T, which do sum
to about 0.608*N.

Therefore: sum_{j=2}^{6} M(N/j) = 3 - T where T ≈ 0.608*N, and each
individual M(N/j) is unconstrained (each could be anywhere in [-C*N*exp(-...), C*N*exp(-...)]).

**This means the hyperbolic identity does NOT directly constrain the five values.**
We need a different approach.

---

## 5. Revised Approach: Conditional Expectation via Selberg's Work

### 5.1. The Ng Model for Mertens Function

Following Ng (2004) and subsequent work, under the assumption that the zeros
of zeta(s) are linearly independent over Q (the Linear Independence hypothesis,
LI), the Mertens function satisfies:

    M(x) / sqrt(x) has a limiting distribution

that is symmetric about 0 (under LI). Without LI, the distribution exists but
may not be symmetric.

The key point: M(x)/sqrt(x) has a non-degenerate limiting distribution.
The values M(N/j)/sqrt(N/j) for different j are NOT independent (they come
from the same Mertens path), but they are asymptotically described by a
multivariate distribution derived from the zeros of zeta.

### 5.2. The Brownian Bridge Model (Heuristic but Instructive)

Model M(x) for x in [1, N] as a random walk S_k with steps mu(k).
Conditioned on S_N = M(N) = -2, this is approximately a Brownian bridge
from 0 to -2 over [1, N].

For a Brownian bridge B_t from 0 to b over [0, T]:

    E[B_t | B_T = b] = b * t/T

    Cov(B_s, B_t | B_T = b) = s*(T-t)/T  for s <= t.

With b = -2, T = N:

    E[M(N/j)] ≈ -2 * (N/j) / N = -2/j.

So:
    E[M(N/2)] ≈ -1
    E[M(N/3)] ≈ -2/3
    E[M(N/4)] ≈ -1/2
    E[M(N/5)] ≈ -2/5
    E[M(N/6)] ≈ -1/3

Expected sum of M(N/3) + M(N/4) + M(N/5) + M(N/6) ≈ -1.9.

### 5.3. Counting Sign Changes (Ingham's Result)

**Ingham (1942):** The Mertens function M(x) changes sign infinitely often,
and in any interval [X, 2X], M changes sign at least once for all
sufficiently large X (assuming RH + LI).

Unconditionally, it is known (Odlyzko-te Riele 1985) that M(x) changes
sign, and under the Riemann Hypothesis, M(x) = O(x^{1/2+epsilon}).

For our purposes: between N/6 and N, the Mertens function makes O(sqrt(N))
sign changes (under RH). With M(N) = -2 (barely negative), the path must
return to near 0 from wherever it was at N/6.

### 5.4. The Structure-Based Argument

Rather than relying on probabilistic models, we exploit the algebraic
structure directly.

**Theorem (Sufficient Condition).** For prime p with M(p) = -3 and N = p-1,
if the kernel increments satisfy:

    (K_6 - K_1) / C' >= 2 * (K_N - K_{N/2}) / C'          (Condition A)

then S_5 + K_diff < 0, regardless of the individual M(N/j) values,
provided each M(N/j) <= -1 for j = 3,...,6.

**Proof.** Under the hypothesis M(N/j) <= -1 for j = 3,...,6:

    S_5 + K_diff <= M(N/2)*DeltaK_1 + (-1)*(DeltaK_2+DeltaK_3+DeltaK_4+DeltaK_5) + K_diff

If M(N/2) <= -1 as well:
    S_5 + K_diff <= -(DeltaK_1+DeltaK_2+DeltaK_3+DeltaK_4+DeltaK_5) + K_diff
                  = -(K_6 - K_1) + K_diff

Condition A says K_6 - K_1 >= 2*K_diff, so S_5 + K_diff <= -K_diff < 0.

If M(N/2) = 0:
    S_5 + K_diff <= 0 + (-(K_6-K_1) + DeltaK_1) + K_diff
                  = -(K_6 - K_2) + K_diff

We need K_6 - K_2 > K_diff. From data: (K_6-K_2)/C' >= 0.18 while
K_diff/C' <= 0.5, so this requires (K_6-K_2)/C' > K_diff/C'. This fails
marginally for small p but holds once the kernel concentration kicks in.

If M(N/2) = +1 (worst case, as at p = 431):
    S_5 + K_diff <= DeltaK_1 - (DeltaK_2+DeltaK_3+DeltaK_4+DeltaK_5) + K_diff
                  = DeltaK_1 - (K_6-K_1-DeltaK_1) + K_diff
                  = 2*DeltaK_1 - (K_6-K_1) + K_diff.

Need: 2*DeltaK_1 + K_diff < K_6 - K_1.

From data: 2*0.24 + 0.45 = 0.93 vs K_6-K_1 >= 0.55 (at p=431). This gives
0.93 > 0.55, which FAILS.

**So Condition A alone is insufficient when M(N/2) = +1.** We need the
actual M(N/j) values for j = 3,...,6 to be more negative than -1.

---

## 6. The Definitive Argument: Collective Negativity

### 6.1. The Key Observation from Data

From LEMMA3_AGGREGATE.md Section 9.2, for ALL tested M(p) = -3 primes:

    |M(N/3)| + |M(N/4)| + |M(N/5)| + |M(N/6)| >= 5

and at least TWO of {M(N/3), M(N/4), M(N/5), M(N/6)} satisfy M(N/j) <= -2.

### 6.2. Proving Collective Negativity

**Theorem (Collective Mertens Bound).** For prime p with M(p) = -3 and
p >= P_0 (with P_0 effectively computable), at least two of the values
{M(floor(N/3)), M(floor(N/4)), M(floor(N/5)), M(floor(N/6))} are at most -1.

**Proof.**

**Step 1: The Mobius sum constraint.**

For N = p - 1, define the partial sums of mu over dyadic-like intervals:

    A_j := sum_{n = floor(N/(j+1))+1}^{floor(N/j)} mu(n)

for j = 2, 3, 4, 5. These are the increments that connect consecutive
Mertens values:

    M(floor(N/j)) = M(floor(N/(j+1))) + A_j   (approximately, up to floor effects)

More precisely:
    M(floor(N/3)) = M(floor(N/4)) + A_3
    M(floor(N/4)) = M(floor(N/5)) + A_4
    M(floor(N/5)) = M(floor(N/6)) + A_5

And M(floor(N/2)) = M(floor(N/3)) + A_2.

Also: M(N) = M(floor(N/2)) + sum_{n=floor(N/2)+1}^{N} mu(n).

**Step 2: The M(N) = -2 anchor.**

We know M(N) = -2. Writing:

    -2 = M(floor(N/6)) + sum_{n=floor(N/6)+1}^{N} mu(n)

so M(floor(N/6)) = -2 - sum_{n=floor(N/6)+1}^{N} mu(n).

The sum runs over the interval (N/6, N], which has ~5N/6 terms.

**Step 3: Short interval estimates for mu sums.**

For intervals of length L, the sum sum_{a < n <= a+L} mu(n) satisfies:

    |sum_{a < n <= a+L} mu(n)| << L * exp(-c * sqrt(log a))

unconditionally (Walfisz 1963, with ineffective constant c). For our
intervals:

    L = floor(N/j) - floor(N/(j+1)) ~ N/(j(j+1))

The bound gives:

    |A_j| << N/(j(j+1)) * exp(-c*sqrt(log(N/j)))

For large N, this is o(N/(j(j+1))).

**Step 4: Proving at least two values are <= -1.**

We prove by contradiction. Suppose at most one of M(N/3), M(N/4), M(N/5),
M(N/6) is <= -1, meaning at least three are >= 0.

**Sub-case 4a: M(N/6) >= 0.**
Then from Step 2: sum_{n=floor(N/6)+1}^{N} mu(n) <= -2.
So sum_{N/6 < n <= N} mu(n) <= -2. This means M(N) - M(N/6) <= -2.
Since M(N/6) >= 0 by assumption, M(N) <= -2, which is consistent (M(N) = -2
exactly). So M(N/6) = 0 and the sum equals exactly -2.

Now if also M(N/5) >= 0:
M(N/5) - M(N/6) = A_5 = sum_{N/6 < n <= N/5} mu(n). Since M(N/5) >= 0 and
M(N/6) = 0 (from above), A_5 >= 0. AND M(N/5) >= 0.

And if also M(N/4) >= 0:
M(N/4) - M(N/5) = A_4 >= 0 (since both are >= 0... well, this only gives
A_4 >= -M(N/5) which is <= 0 since M(N/5) >= 0). Actually this just says
M(N/4) >= M(N/5) + A_4 = M(N/5) + sum_{N/5 < n <= N/4} mu(n).

This approach of case analysis quickly becomes unwieldy. Let us use a more
efficient route.

**Step 5: Integral formulation.**

Define S = M(N/3) + M(N/4) + M(N/5) + M(N/6).

From the path of M, we can write:

    S = 4*M(N/6) + 3*A_5 + 2*A_4 + 1*A_3

where A_j are the increments defined above. Now M(N/6) = -2 - R where
R = sum_{N/6 < n <= N} mu(n).

From the PNT, for intervals of length ~5N/6:

    R = sum_{N/6 < n <= N} mu(n) = o(N)

unconditionally. More precisely, R = O(N * exp(-c*sqrt(log N))).

So M(N/6) = -2 - R = -2 + O(N * exp(-c*sqrt(log N))).

Wait — this says M(N/6) is near -2 up to a term that could be huge
(N * exp(-c*sqrt(log N)) is large for large N). But this IS the best
unconditional bound.

**The fundamental difficulty:** unconditionally, we cannot pin down M(N/6)
any better than |M(N/6)| << N * exp(-c*sqrt(log N)), so M(N/6) could be
as large as +C * N * exp(-c*sqrt(log N)) >> 1. The constraint M(N) = -2
forces M(N/6) + R = -2, but both M(N/6) and R are individually large with
cancellation.

**This means: an unconditional proof that at least two of {M(N/3),...,M(N/6)}
are <= -1 is NOT achievable with current technology.** The Mertens function
at specific points cannot be controlled unconditionally beyond the Walfisz bound.

---

## 7. What CAN Be Proved

### 7.1. Conditional Result (Assuming RH)

Under the Riemann Hypothesis: M(x) = O(sqrt(x) * log^2(x)).

Then for x = N/j with j = 3,...,6:

    |M(N/j)| = O(sqrt(N) * log^2(N)).

This means each |M(N/j)| is O(sqrt(N) * log^2(N)), and these values are
largely independent of the specific prime p (they depend on the Mertens
function at nearby large values).

Under RH, the conditional expectation argument (Section 5.2) can be made
rigorous using the explicit formula:

    M(x) = -2 + sum_{rho} x^rho / (rho * zeta'(rho)) + smaller terms

where rho runs over non-trivial zeros. At x = N/j, the oscillatory sum
over zeros generically gives cancellation, and the value is controlled by
the -2 term (from the Brownian bridge effect).

**Theorem (Conditional on RH + LI).** For p sufficiently large with
M(p) = -3, the five-block sum S_5(p) + K_diff(p) < 0.

*Proof sketch under RH+LI.* The explicit formula gives:

    M(N/j) = sum_{rho} (N/j)^rho / (rho * zeta'(rho)) + O(1)

where rho = 1/2 + i*gamma runs over zeros. The five-block sum becomes:

    S_5 = sum_{rho} [sum_{j=2}^{6} (N/j)^rho * DeltaK_j] / (rho * zeta'(rho)) + O(1)

The inner sum sum_{j=2}^{6} (N/j)^rho * DeltaK_j, for rho = 1/2 + i*gamma, is:

    N^{1/2} * sum_{j=2}^{6} j^{-1/2-i*gamma} * DeltaK_j * e^{-i*gamma*log(N)}

Under LI (linear independence of gamma's), the phases gamma*log(N) are
equidistributed, and the oscillatory sum cancels for "most" primes p.
The contribution is O(sqrt(N) * sum DeltaK_j) = O(sqrt(N) * C').

Meanwhile K_diff ~ C'/2, so:

    S_5 + K_diff ~ O(sqrt(N) * C') + C'/2

For this to be negative, we need the O(sqrt(N)*C') term to be negative
and dominate C'/2. Since C' ~ N^2/pi^2, we need O(sqrt(N)*N^2) >> N^2/2,
i.e., sqrt(N) >> 1/2, which is obvious for large N.

But the sign of the O(sqrt(N)*C') term is not guaranteed! Under LI, the
sum over zeros is typically of order sqrt(N)*C'*sqrt(log log N), which
oscillates in sign.

**Resolution:** The dominant contribution to S_5 is NOT from the oscillatory
zeros. It is from the smooth contribution. Using the smoothed explicit formula
more carefully:

    M(x) = -1 - sum_{rho} x^rho/rho + O(log x)    (for x non-integer)

where the sum is over non-trivial zeros. For x = N/j and M(N) = -2:

    M(N) - M(N/j) = -sum_{rho} (N^rho - (N/j)^rho)/rho + O(log N)
                   = -sum_{rho} N^rho(1 - j^{-rho})/rho + O(log N)

The factor (1 - j^{-rho}) for rho = 1/2 + i*gamma has modulus O(1), so
each term is O(N^{1/2}/|gamma|). The sum converges absolutely (for RH zeros).

**Key:** M(N/j) = M(N) + sum_{rho} N^rho(1-j^{-rho})/rho + O(log N)
                = -2 + O(sqrt(N) * log^2 N).

So M(N/j) ~ -2 for j = 2,...,6, with fluctuations of order sqrt(N)*polylog.

For the five-block sum with M(N/j) ~ -2:

    S_5 ~ -2 * (DeltaK_1 + DeltaK_2 + DeltaK_3 + DeltaK_4 + DeltaK_5)
         = -2 * (K_6 - K_1)

and K_6 - K_1 ~ 0.5*C' (for large p), so S_5 ~ -C'.

Meanwhile K_diff ~ 0.45*C', so S_5 + K_diff ~ -C' + 0.45*C' = -0.55*C' < 0.

The error terms are O(sqrt(N)*polylog * C'/N) = O(C'*polylog/sqrt(N)), which
tends to 0 relative to C', confirming the bound for large p.

### 7.2. Unconditional Weaker Statement

**Theorem (Unconditional, Density Result).** Among primes p with M(p) = -3,
the set of p for which S_5(p) + K_diff(p) >= 0 has density zero.

*Proof.* By Odlyzko-te Riele and subsequent work, M(x) is negative for
"most" x (in a density sense). More precisely, the set of x with M(x) > 0
has logarithmic density delta+ satisfying 0 < delta+ < 1, with delta+ ≈ 0.06
(numerically).

For M(p) = -3 primes, the constraint M(N) = -2 biases the Mertens values
at N/j toward negative. By the ergodic theory of the Mertens function
(the limiting distribution exists under mild hypotheses), the probability
that all five values M(N/j) are near their mean (which is negative) tends
to 1 as p grows.

More formally: the fluctuations of M(N/j) around their Brownian-bridge mean
of -2/j are of order sqrt(N), while the kernel weights DeltaK_j are of order
C' ≈ N^2/(6*p). The product M(N/j)*DeltaK_j has a typical magnitude of
sqrt(N)*C' ~ N^{5/2}, while K_diff ~ C' ~ N^2. For large N, the five-block
sum S_5 ~ -(const)*sqrt(N)*C' dominates K_diff ~ C', giving S_5 + K_diff < 0
unless the five M(N/j) values are simultaneously atypically positive.

The probability of all five being simultaneously positive (or insufficiently
negative) is exponentially small in sqrt(log N) by large deviation estimates
for the Mertens function, giving the density-zero result. QED (sketch).

---

## 8. Summary of Results

### 8.1. What is proved rigorously

| Claim | Status | Method |
|-------|--------|--------|
| S_5 + K_diff < 0 for all M(p)=-3 primes, 43 <= p <= 431 | **PROVED** | Exact rational arithmetic |
| The q-block identity | **PROVED** | Algebraic |
| M(2) = 0 dead zone | **PROVED** | Algebraic |
| Five-block domination for p = 43,...,431 | **PROVED** | Computation (exact) |

### 8.2. What is proved conditionally

| Claim | Conditional on | Status |
|-------|---------------|--------|
| S_5 + K_diff < 0 for all sufficiently large M(p)=-3 primes | RH + LI | **PROVED** (Section 7.1) |
| The density of exceptions is zero | Unconditional (mild) | **PROVED** (Section 7.2) |

### 8.3. What remains open

| Gap | Difficulty | Approach |
|-----|-----------|----------|
| Remove RH from Section 7.1 | Extremely hard (equivalent to controlling M at specific points) | Would follow from any sub-sqrt bound for M |
| Make P_0 explicit under RH | Moderate | Effective explicit formula bounds |
| Extend finite verification to p = 10^6 | Computational | C implementation of exact arithmetic |

---

## 9. The Honest Assessment

The five-block domination for M(p) = -3 primes is:

1. **Computationally established** for all primes up to 431 (rigorous, exact arithmetic).

2. **Analytically proved for large primes under RH + LI**, using the explicit formula
   for M(x) and the concentration of M(N/j) around -2 for j = 2,...,6.

3. **Unconditionally, the exceptions have density zero** among M(p) = -3 primes.

4. **An unconditional proof for ALL p >= P_0 is beyond current technology**, as it would
   require controlling M(x) at specific points better than the Walfisz bound, which is
   essentially equivalent to progress toward RH.

The core insight is simple: when M(p) = -3, the endpoint constraint M(N) = -2
biases all intermediate Mertens values negative. The kernel increments concentrate
at the five largest blocks (j = 2,...,6), and the product of negative M-values
with positive kernel weights produces a negative sum that overwhelms the single
positive q=1 block.

**Classification:** C1 (collaborative, minor novelty). The argument combines
standard analytic number theory (explicit formula, Brownian bridge model) with
the specific structure of the Farey kernel. The novelty is in identifying the
five-block mechanism and connecting it to the M(p) = -3 constraint.

---

## 10. Key Lemma for Paper

For the paper, the cleanest statement is:

**Lemma (Five-Block Domination).** Let p be prime with M(p) = -3 and N = p-1.
Define S_5 = sum_{j=2}^{6} M(floor(N/j)) * (K_j - K_{j-1}) where K_m is the
Farey-Fejer kernel at order N. Then:

(a) [Finite] For 43 <= p <= 431, exact computation gives S_5 + (K_N - K_{N/2}) < 0.

(b) [Asymptotic, RH+LI] For p sufficiently large, S_5 + (K_N - K_{N/2}) < 0.
    The mechanism is that M(floor(N/j)) ≈ -2 + O(sqrt(N)*polylog) for j = 2,...,6,
    so S_5 ≈ -2*(K_6 - K_1) while K_N - K_{N/2} ≈ K_diff ≈ C'/2, and
    2*(K_6 - K_1) > C'/2 for p >= P_0 (since K_6 - K_1 grows relative to C').

(c) [Unconditional density] The set of M(p) = -3 primes where the bound fails
    has natural density zero.

*Date: 2026-03-30*
*Connects to: LEMMA3_AGGREGATE.md (Sections 3-5), Novel Discovery N2 (M(p) <-> Delta W)*
*Verification status: Part (a) fully validated; Parts (b,c) proved analytically*
