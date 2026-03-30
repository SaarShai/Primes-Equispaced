# Closing Step 2: Averaged Equidistribution via Weyl's Criterion

**Date:** 2026-03-30
**Status:** Step 2 CLOSED — large sieve bypassed entirely
**Connects to:** TRIANGULAR_DISTRIBUTION_PROOF.md, Section 3

---

## 0. The gap in the original proof

The triangular distribution proof (Section 3) used Koksma-Hlawka with a per-denominator discrepancy bound D_b^* << phi(b)^{-1/3}, then averaged over b. This required verifying that the Ramanujan sum contributions are well-behaved "on average," which was flagged as needing the large sieve.

**Resolution:** Neither the large sieve nor Koksma-Hlawka is needed. Weyl's criterion applied directly to the full Farey sequence closes the argument in a few lines. The key insight: bound the total exponential sum over ALL (a, b) pairs at once, rather than bounding per-b discrepancy and then averaging.

---

## 1. Setup

Fix an odd prime p and let N = p - 1. The Farey-type point set is

    P_N = { (a/b,  (pa mod b)/b) : 1 <= a < b <= N, gcd(a,b) = 1 }

with cardinality |P_N| = |F_N| - 1 = sum_{b=2}^{N} phi(b) ~ (3/pi^2) N^2.

**Goal.** Show that P_N is equidistributed in [0,1]^2 as N -> infinity, which immediately implies moment convergence for all continuous test functions.

---

## 2. The Weyl criterion argument

**Theorem (Closure of Step 2).** The point set P_N is equidistributed in [0,1]^2. That is, for every continuous function f: [0,1]^2 -> R,

    (1/|P_N|) sum_{(x,y) in P_N} f(x, y)  -->  integral_{[0,1]^2} f(x,y) dx dy.

In particular, taking f(x,y) = (x - y)^{2k}:

    m_{2k}(p) --> integral_0^1 integral_0^1 (x - y)^{2k} dx dy = 2/((2k+1)(2k+2)).

**Proof.** By the Weyl equidistribution criterion in dimension 2, it suffices to show that for every (h, k) in Z^2 with (h, k) != (0, 0):

    (1/|P_N|) * | sum_{b=2}^{N} sum_{a: gcd(a,b)=1} e(h * a/b  +  k * (pa mod b)/b) |  -->  0.    (*)

**Step A: Reduce to Ramanujan sums.** Since pa mod b = pa - b*floor(pa/b), we have

    e(k * (pa mod b)/b) = e(k * pa/b)

(the integer floor(pa/b) contributes e(k * integer) = 1). Therefore the inner sum is

    sum_{a: gcd(a,b)=1} e((h + kp) * a / b) = c_b(h + kp),

the Ramanujan sum with argument m := h + kp. (This is the same reduction as in Step 1 of the main proof, Lemma 1.)

**Step B: Bound the Ramanujan sums.** The classical bound (Ramanujan 1918, via the identity c_b(m) = sum_{d | gcd(m,b)} d * mu(b/d)) gives

    |c_b(m)| <= gcd(|m|, b)

for all b >= 1 and all m in Z.

**Step C: Sum over b.** For fixed nonzero m = h + kp:

    | sum_{b=2}^{N} c_b(m) |  <=  sum_{b=1}^{N} |c_b(m)|  <=  sum_{b=1}^{N} gcd(|m|, b).

The sum of gcd(|m|, b) over b = 1, ..., N has the exact evaluation

    sum_{b=1}^{N} gcd(|m|, b) = sum_{d | |m|} phi(d) * floor(N/d) = N * sigma_0(|m|) + O(d(|m|))

where

    sigma_0(|m|) := sum_{d | |m|} phi(d)/d = prod_{q^a || |m|} (1 + a(1 - 1/q)).

(Here d(|m|) = number of divisors of |m|.) In particular, for fixed m != 0:

    sum_{b=1}^{N} gcd(|m|, b) = O_m(N).

**Step D: Conclude.** The left side of (*) is bounded by

    (1/|P_N|) * sum_{b=1}^{N} gcd(|m|, b)  =  O_m(N) / ((3/pi^2) N^2 + O(N log N))  =  O_m(1/N)  -->  0.

Since this holds for every (h, k) != (0, 0), the Weyl criterion gives equidistribution of P_N in [0,1]^2.

**QED.**

---

## 3. Why m = h + kp is nonzero

A minor but necessary check: for (h, k) != (0, 0) with h, k in Z, we need m = h + kp != 0.

- If k = 0: then h != 0, so m = h != 0.
- If k != 0: then m = h + kp. This could be zero only if h = -kp, i.e., p | h. But in the Weyl criterion we consider all nonzero (h, k), including those with |h| arbitrarily large, so m = 0 can occur.

**Resolution.** When m = h + kp = 0, we have c_b(0) = phi(b) for all b. The sum becomes sum phi(b) = |P_N|, and the ratio is 1. But this case corresponds to h = -kp, and the Weyl criterion excludes (h, k) = (0, 0) but not h + kp = 0.

However, the exponential sum test function is e(hx + ky) with (h, k) != (0, 0), not e(mx) for 1D. Even when h + kp = 0, the test function e(hx + ky) = e(h(x - y/p * ... )) is NOT the constant function on [0,1]^2 (it is e(h * a/b + k * pa/b) = e((h+kp)a/b) = 1 for all a, b, which gives sum = phi(b) for each b).

Wait: if h + kp = 0, then e(h * a/b + k * pa/b) = e(0) = 1 for all (a, b), so the exponential sum equals |P_N|, and the average is 1. But the integral of e(hx + ky) over [0,1]^2 is 0 (since (h, k) != (0, 0)), so the criterion would FAIL.

**This needs more care.** Let us re-examine.

The integral is:

    integral_0^1 integral_0^1 e(hx + ky) dx dy  =  (integral_0^1 e(hx) dx)(integral_0^1 e(ky) dy)

This is zero unless h = 0 AND k = 0. Since (h, k) != (0, 0), at least one factor is zero, so the integral is always 0.

The discrete sum when h + kp = 0 (i.e., h = -kp with k != 0):

    sum_{b} sum_{a coprime b} e(h*a/b + k*pa/b) = sum_b sum_a e((-kp + kp)a/b) = sum_b phi(b) = |P_N|

So the discrete average is 1 while the continuous integral is 0. This would mean the Weyl criterion fails!

**The resolution:** The test points (a/b, (pa mod b)/b) are NOT (a/b, pa/b). They are (a/b, {pa/b}) where {x} = x mod 1 is the fractional part. The exponential sum calculation used:

    e(k * {pa/b}) = e(k * pa/b)

because e is 1-periodic. So

    sum_a e(h*a/b + k*{pa/b}) = sum_a e((h + kp)*a/b) = c_b(h + kp).

This is correct: when h + kp = 0, we get c_b(0) = phi(b), and the sum over b gives |P_N|.

But the CONTINUOUS integral we should compare to is:

    integral_{[0,1]^2} e(hx + ky) dx dy = 0     for (h,k) != (0,0).

The fact that the discrete average is 1 for h = -kp seems like a contradiction. What went wrong?

**The resolution is that the points (a/b, {pa/b}) are NOT asymptotically equidistributed in [0,1]^2 for any fixed p.**

Actually, wait. We are NOT letting p be fixed and N -> infinity. In our theorem, N = p - 1 and both grow together. So m = h + kp grows with p (for k != 0), and the Weyl criterion is applied with FIXED (h, k) as N = p - 1 -> infinity. For k != 0, m = h + kp -> infinity, so we cannot treat m as fixed.

**This is the actual subtlety.** Let me redo the argument properly.

---

## 4. The corrected argument

The crucial point: N = p - 1 and p -> infinity simultaneously. So m = h + kp depends on p.

**Case 1: k = 0.** Then m = h (fixed, nonzero). The bound from Step C gives

    |sum_{b<=N} c_b(h)| <= sum gcd(|h|, b) = O_h(N) = O(N).

Ratio with |P_N| ~ (3/pi^2)N^2: this is O(1/N) -> 0. Good.

**Case 2: k != 0.** Then |m| = |h + kp| >= |k|p - |h|, which grows like p. Now m is NOT fixed; it grows with p. The bound |c_b(m)| <= gcd(m, b) is still valid, but summing gcd(m, b) over b <= N with m ~ kp ~ kN is different.

For m growing with N: sum_{b=1}^{N} gcd(m, b). Since gcd(m, b) <= b, the trivial bound is sum b = O(N^2), which gives ratio O(N^2/N^2) = O(1) — useless.

We need a better bound. Write:

    sum_{b=1}^{N} gcd(m, b) = sum_{d | m} phi(d) * floor(N/d) <= N * sum_{d | m, d <= N} phi(d)/d + sum_{d | m, d > N} phi(d)

The key: for m = h + kp with p prime and |k| bounded:

- If k = +/-1: m = h +/- p. This is either prime or has small factors (since |h| is bounded in the Weyl criterion truncation). For the Weyl criterion to work, we need the sum to converge for each FIXED (h, k) as p -> infinity, so we may treat |h| and |k| as fixed constants.

- With |k| fixed and m = h + kp, the divisors of m are controlled by the factorization of h + kp. For "generic" primes p, m = h + kp will have only small divisors (since m is roughly kp and p is prime, m itself tends to be nearly prime or have few factors).

But we need a UNIFORM bound, not just for generic p.

**Refined approach using the Ramanujan sum identity more carefully.**

Instead of bounding |c_b(m)| <= gcd(m, b), use the exact formula:

    c_b(m) = sum_{d | gcd(m,b)} d * mu(b/d).

Since |mu| <= 1:

    |c_b(m)| <= sum_{d | gcd(m,b)} d = sigma_1(gcd(m,b))     ... no, that's >= gcd.

Actually the bound |c_b(m)| <= gcd(m,b) is already tight in the worst case.

**Better approach: use cancellation in the sum over b.**

The sum sum_{b=1}^{N} c_b(m) has an exact evaluation. By the identity c_b(m) = sum_{d|gcd(m,b)} d*mu(b/d), we can swap the order of summation:

    sum_{b=1}^{N} c_b(m) = sum_{d | m} d * sum_{b <= N, d | b} mu(b/d)
                          = sum_{d | m} d * sum_{e <= N/d} mu(e)
                          = sum_{d | m} d * M(N/d)

where M(x) = sum_{n<=x} mu(n) is the Mertens function.

Now |M(x)| <= x (trivially) and much better bounds are known: M(x) = O(x * exp(-c*sqrt(log x))) unconditionally (Walfisz).

So:

    |sum_{b=1}^{N} c_b(m)| <= sum_{d | m} d * |M(N/d)| <= sum_{d | m} d * (N/d) * exp(-c*sqrt(log(N/d)))

For d <= N^{1-epsilon}: N/d >= N^epsilon, so M(N/d) = O(N/d * exp(-c'*sqrt(log N))).
For d > N^{1-epsilon}: these contribute at most sum_{d | m, d > N^{1-eps}} d, which for m = h+kp with fixed k is bounded since the large divisors of m = h+kp are m itself (if m > N^{1-eps}).

For the dominant contribution (d small compared to N):

    sum_{d | m, d <= N^{1-eps}} d * M(N/d) = O(sigma_1(m) * N * exp(-c'*sqrt(log N)))

where sigma_1(m) = sum_{d|m} d.

For m = h + kp with |k| bounded: sigma_1(m) <= m * tau(m)/1 ... more simply, sigma_1(m) <= m * (1 + 1/q_1 + ...) where q_i are prime factors of m. In the worst case sigma_1(m) = O(m * log log m) = O(p * log log p).

The single large divisor d = m = h + kp contributes: d * M(N/d) = (h+kp) * M(N/(h+kp)). Since N/(h+kp) ~ 1/|k| (bounded), M(bounded) = O(1). So this contributes O(p).

Combining: |sum c_b(m)| = O(p * exp(-c*sqrt(log p))) + O(p) = O(p).

And |P_N| ~ (3/pi^2)p^2. So the ratio is O(p/p^2) = O(1/p) -> 0.

**This is correct even for m growing with p.** The key saving is that |sum c_b(m)| = O(|m|) = O(p), while |P_N| = Theta(p^2).

---

## 5. Clean proof (final version)

**Proposition (Step 2 closure).** Let p be an odd prime and N = p - 1. The point set

    P_N = { (a/b, (pa mod b)/b) : 1 <= a < b <= N, gcd(a,b) = 1 }

is equidistributed in [0,1]^2 as p -> infinity. Consequently, for each fixed integer k >= 1:

    m_{2k}(p) := (1/|P_N|) sum_{(a,b)} ((pa mod b)/b - a/b)^{2k}  -->  2/((2k+1)(2k+2)).

**Proof.**

*Step 1 (Weyl reduction).* By the Weyl equidistribution criterion in R^2/Z^2, it suffices to show that for every fixed (h, k) in Z^2 \ {(0,0)}:

    S(h, k; N) := sum_{b=2}^{N} sum_{a=1, gcd(a,b)=1}^{b-1} e(h * a/b + k * (pa mod b)/b) = o(|P_N|).

Since e(k * (pa mod b)/b) = e(kpa/b) (by 1-periodicity of e), we have

    S(h, k; N) = sum_{b=2}^{N} c_b(m),    where m = m(h,k,p) := h + kp

and c_b(m) = sum_{gcd(a,b)=1} e(ma/b) is the Ramanujan sum.

Note m != 0: if k = 0 then m = h != 0; if k != 0 then |m| = |h + kp| >= |k|p - |h| > 0 for p > |h|/|k|.

*Step 2 (Exact evaluation via Mertens function).* By the identity c_b(m) = sum_{d | gcd(m,b)} d * mu(b/d), swapping summation:

    sum_{b=1}^{N} c_b(m) = sum_{d | m} d * sum_{e <= N/d} mu(e) = sum_{d | m} d * M(N/d)     ... (1)

where M(x) = sum_{n <= x} mu(n) is the Mertens function.

*Step 3 (Bounding via Mertens).* We split the sum (1) over divisors d of m into d < N and d >= N.

**Divisors d >= N:** Since d | m and d >= N, we need d <= |m| = |h + kp| <= |h| + |k|p < (|h| + |k|)p. The divisors d >= N of m contribute:

    sum_{d | m, d >= N} d * M(N/d).

For such d, N/d <= 1, so M(N/d) is either M(0) = 0 or M(1) = 1. The only possibility is d = m if |m| >= N, contributing at most |m| * 1 = O(p).

**Divisors d < N:** Each such d satisfies N/d > 1. By the unconditional bound |M(x)| = O(x * exp(-c * sqrt(log x))) (Walfisz 1963):

    |d * M(N/d)| <= d * (N/d) * exp(-c * sqrt(log(N/d))) = N * exp(-c * sqrt(log(N/d))).

For d < N^{1-epsilon}, this gives N * exp(-c * sqrt(epsilon * log N)), which summed over the (at most tau(m)) such divisors gives:

    tau(m) * N * exp(-c' * sqrt(log N)).

Since m = h + kp with h, k fixed: tau(m) = O_epsilon(p^epsilon) for any epsilon > 0 (divisor bound). So the contribution from small d is:

    O(p^epsilon * N * exp(-c' * sqrt(log N))) = o(N)     for any epsilon > 0.

For N^{1-epsilon} <= d < N: there are at most tau(m) = O(p^epsilon) such divisors, each contributing at most N. Total: O(p^epsilon * N) = O(N^{1+epsilon}).

**Combining:** |sum_{b=1}^{N} c_b(m)| = O(p) + o(N) + O(N^{1+epsilon}) = O(N^{1+epsilon}) for any epsilon > 0.

Since |P_N| = (3/pi^2) N^2 + O(N log N):

    |S(h, k; N)| / |P_N| = O(N^{1+epsilon} / N^2) = O(N^{-1+epsilon}) --> 0.

*Step 4 (Moment convergence).* By the Weyl criterion, P_N is equidistributed in [0,1]^2. Since f(x,y) = (x - y)^{2k} is continuous on [0,1]^2:

    m_{2k}(p) --> integral_0^1 integral_0^1 (x - y)^{2k} dx dy = 2 * integral_0^1 t^{2k}(1-t) dt = 2/((2k+1)(2k+2)).

**QED.**

---

## 6. Simpler bound (avoiding Mertens)

The above proof using the Mertens function is rigorous but invokes a deep result. Here is a completely elementary alternative.

**Elementary bound.** For any m != 0:

    |sum_{b=1}^{N} c_b(m)| <= sum_{b=1}^{N} |c_b(m)| <= sum_{b=1}^{N} gcd(|m|, b).

Now sum_{b=1}^{N} gcd(|m|, b) = sum_{d | |m|} phi(d) * floor(N/d). For each divisor d of |m|:

    phi(d) * floor(N/d) <= phi(d) * N/d <= N.

The number of divisors of m = h + kp is tau(|m|). Therefore:

    sum_{b=1}^{N} gcd(|m|, b) <= N * tau(|m|).

For m = h + kp with fixed h, k and p -> infinity: tau(|m|) = O_epsilon(|m|^epsilon) = O_epsilon(p^epsilon) for any epsilon > 0.

Hence:

    |sum_{b=1}^{N} c_b(m)| / |P_N| <= N * p^epsilon / ((3/pi^2)N^2) = O(p^{epsilon-1}) --> 0.

**QED (elementary version).**

**Remark.** The elementary version gives the weaker quantitative bound O(N^{-1+epsilon}) vs. the Mertens-based O(N^{-1} * exp(-c*sqrt(log N))). For the qualitative convergence result, both suffice.

---

## 7. Quantitative error term via Erdos-Turan

For the error in S_{2k}(p), we can use the 2D Erdos-Turan inequality. The star-discrepancy of P_N satisfies:

    D_N^* << (1/H) + (1/|P_N|) * sum_{1 <= max(|h|,|k|) <= H} (1/(r(h)*r(k))) * |sum_b c_b(h+kp)|

where r(n) = max(|n|, 1).

**For h-sum terms (k = 0):** |sum c_b(h)| <= N * sigma_0(|h|) with sigma_0(|h|) = sum_{d||h|} phi(d)/d. Summing over 1 <= |h| <= H:

    sum_{h=1}^{H} (1/h) * N * sigma_0(h) << N * sum_{h=1}^H sigma_0(h)/h << N * (log H)^2.

**For k != 0 terms:** |sum c_b(h + kp)| <= N * tau(|h+kp|). For most (h,k) with |h+kp| > 1, tau is small on average. Summing:

    sum_{k=1}^{H} sum_{h=-H}^{H} (1/(k*max(|h|,1))) * N * tau(|h+kp|).

By the average order of the divisor function (sum tau(n) over an interval of length 2H+1 is O(H log p)):

    << N * sum_{k=1}^H (1/k) * H * log(kp) / H << N * (log H) * log(Hp).

Since p ~ N:

    Total << N * (log H) * log(HN) + N * (log H)^2 << N * (log H) * log(HN).

The Erdos-Turan bound gives:

    D_N^* << 1/H + N * (log H) * log(HN) / N^2 = 1/H + (log H * log(HN)) / N.

Choosing H = N / (log N)^2:

    D_N^* << (log N)^2 / N + (log N)^3 / N << (log N)^3 / N.

By Koksma-Hlawka (with V(f) = O_k(1) for f(x,y) = (x-y)^{2k}):

    |m_{2k}(p) - 2/((2k+1)(2k+2))| << (log p)^3 / p.

Therefore:

    S_{2k}(p) = (3/(pi^2 (2k+1)(k+1))) * p^2 + O_k(p * (log p)^3).

This is MUCH stronger than the O(p^{5/3}) error in the original proof.

---

## 8. Summary

| Approach | Bound on sum c_b(m) / |F_N| | Error in S_{2k} | Status |
|----------|------------------------------|------------------|--------|
| Weyl + triangle ineq + divisor bound | O(N^{-1+epsilon}) | qualitative only | Elementary, rigorous |
| Weyl + Mertens function | O(N^{-1} exp(-c sqrt(log N))) | not extracted | Rigorous (uses Walfisz) |
| Erdos-Turan quantitative | (log N)^3 / N | O(p (log p)^3) | Rigorous (average divisor function) |

**Step 2 of the triangular distribution proof is now CLOSED.** The simplest closure is the elementary Weyl criterion argument (Section 6): the Ramanujan sum bound |c_b(m)| <= gcd(m,b), summed trivially, gives O(N * tau(m)) = O(N^{1+epsilon}), which is o(N^2) = o(|F_N|). No large sieve is needed.

---

## 9. Correction to the original proof

The original TRIANGULAR_DISTRIBUTION_PROOF.md (Section 3) should be updated:

1. **Replace** the Koksma-Hlawka averaging argument (Sections 3.2-3.3) with the direct Weyl criterion approach from Section 5 above.
2. **Replace** the error term O(p^{5/3}) with the improved O(p * (log p)^3) from the Erdos-Turan analysis (Section 7).
3. **Mark** the verification checklist item "Averaged Koksma-Hlawka bound" as CLOSED.
4. **Remove** the dependency on the large sieve inequality (Section 6.2 of the original).

The proof is now complete in all three steps:
- Step 1 (equidistribution for fixed b): Ramanujan sums. Was already rigorous.
- Step 2 (averaging over b): Weyl criterion + Ramanujan sum bound. **NOW CLOSED.**
- Step 3 (moments -> distribution): Moment determinacy. Was already rigorous.
