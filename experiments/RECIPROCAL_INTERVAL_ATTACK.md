# Reciprocal-Interval Character Sum Attack

**Date:** 2026-03-29
**Status:** 🔬 Unverified — working through the argument
**Connects to:** N2 (Mertens-discrepancy connection), the Dedekind spectral formula

---

## Goal

Prove
```
Sigma_{chi odd} |L(1,chi)|^2 * |Lambda_p(chi)|^2  >=  c * p^2 * log p
```
which, combined with the spectral formula Q = (p/(pi^2(p-1))) * [this sum],
gives Q >> p * log p, the growth rate needed for the energy lower bound.

---

## 1. Reciprocal-Interval Decomposition of Lambda_p

Recall: lambda_p(m) = M(floor(N/m)) for m = 1, ..., N, with N = p-1.

Group terms by the value of t = floor(N/m). For each t = 1, ..., N,
the values m in the interval (N/(t+1), N/t] all give lambda_p(m) = M(t).

Therefore:
```
Lambda_p(chi) = Sigma_{m=1}^{N} lambda_p(m) chi(m)
             = Sigma_{t=1}^{N} M(t) * Sigma_{N/(t+1) < m <= N/t} chi(m)
             = Sigma_{t=1}^{N} M(t) * S_chi(N/(t+1), N/t)
```

where S_chi(a,b) = Sigma_{a < m <= b} chi(m) is a short character sum
over an interval of length ~ N/t^2.

**Note:** The sum over t is really only up to N (since floor(N/m) ranges
from 1 to N), and most intervals are nonempty only for t <= N.

---

## 2. The Montgomery-Vaughan Fourth Moment

We want to evaluate the "twisted" fourth moment:
```
T = Sigma_{chi mod p} |Sigma_n a_n chi(n)|^2 * |Sigma_m b_m chi(m)|^2
```

The Montgomery-Vaughan large sieve / mean value theorem gives:
```
T = (p-1) [Sigma_n |a_n|^2 * Sigma_m |b_m|^2 + |Sigma_n a_n b_n_bar|^2]
    + O(error terms)
```

More precisely, for a_n and b_m supported on {1, ..., N} with N = p-1:

**Exact orthogonality (since p is prime and N = p-1):**
```
Sigma_{chi mod p} chi(n) chi_bar(m) = (p-1) * 1_{n = m mod p}
```
For n, m in {1, ..., p-1}, this is just (p-1) * delta_{n,m}.

Therefore the exact formula is:
```
Sigma_{chi mod p} |A(chi)|^2 * |B(chi)|^2
= Sigma_{chi} (Sigma_n a_n chi(n))(Sigma_m a_m_bar chi_bar(m))
             * (Sigma_r b_r chi(r))(Sigma_s b_s_bar chi_bar(s))
= Sigma_{n,m,r,s} a_n a_m_bar b_r b_s_bar * Sigma_chi chi(nr_inv * ms_inv)
  ... [not quite right, need to be more careful]
```

Let me be precise. We have:
```
Sigma_{chi mod p} |A(chi)|^2 |B(chi)|^2
= Sigma_{n,m,r,s} a_n conj(a_m) b_r conj(b_s) * (1/(p-1)) Sigma_{chi != chi_0} chi(n) conj(chi(m)) chi(r) conj(chi(s))
```

Wait -- we need to include chi_0 carefully and restrict to odd characters.

### Restricting to odd characters

For odd characters, we use the projector:
```
(1/2) Sigma_{chi} [1 - chi(-1)] ... = Sigma_{chi odd} ...
```

This is more complex. Let me use a cleaner approach.

---

## 3. Direct Inner Product Approach

Instead of the full fourth moment, focus on the CROSS TERM that produces log p.

### The key inner product

Define:
```
I(p) = Sigma_{n=1}^{N} (1/n) * lambda_p(n)
     = Sigma_{n=1}^{N} M(floor(N/n)) / n
```

**Claim:** I(p) ~ c * log(p) for a positive constant c.

### Evaluation of I(p)

Group by t = floor(N/n):
```
I(p) = Sigma_{t=1}^{N} M(t) * Sigma_{N/(t+1) < n <= N/t} (1/n)
     = Sigma_{t=1}^{N} M(t) * [H(floor(N/t)) - H(floor(N/(t+1)))]
```

where H(k) = Sigma_{j=1}^{k} 1/j is the harmonic number.

Using H(k) = log(k) + gamma + O(1/k), we get:
```
H(floor(N/t)) - H(floor(N/(t+1))) = log(N/t) - log(N/(t+1)) + O(t/N)
                                    = log((t+1)/t) + O(t/N)
                                    = 1/t + O(1/t^2) + O(t/N)
```

Therefore:
```
I(p) = Sigma_{t=1}^{N} M(t)/t + Sigma_{t} M(t) * O(1/t^2 + t/N)
```

### The main term: Sigma M(t)/t

This is a CLASSICAL object. We have:
```
Sigma_{t=1}^{X} M(t)/t = ... ?
```

**Key identity (well-known):** By partial summation from Sigma mu(n)/n:
```
Sigma_{n=1}^{X} mu(n)/n = O(1/log X)   (prime number theorem equivalent)
```

And by partial summation:
```
Sigma_{t=1}^{X} M(t)/t = M(X) * H(X) - Sigma_{t=1}^{X-1} M(t) [H(t+1) - H(t)]
                        ≈ M(X) log X - Sigma_{t=1}^{X} M(t)/t
```

Wait, this is circular. Let me use a different approach.

**Better:** The identity relating M(t)/t to mu:
```
Sigma_{t=1}^{X} M(t)/t = 1 + Sigma_{t=2}^{X} (Sigma_{k=1}^{t} mu(k))/t
```

By Abel summation:
```
Sigma_{t=1}^{X} M(t)/t = Sigma_{n=1}^{X} mu(n) Sigma_{t=n}^{X} 1/t
                        = Sigma_{n=1}^{X} mu(n) [H(X) - H(n-1)]
                        = H(X) Sigma mu(n) - Sigma mu(n) H(n-1)
```

The first term is H(X) * (Sigma mu(n)) = H(X) * O(X exp(-c sqrt(log X))) which
is O(X exp(-c sqrt(log X)) * log X). This is NOT small.

**Actually this is wrong.** Let me redo Abel summation correctly.

```
Sigma_{t=1}^{X} M(t)/t = Sigma_{t=1}^{X} (1/t) Sigma_{k=1}^{t} mu(k)
                        = Sigma_{k=1}^{X} mu(k) Sigma_{t=k}^{X} (1/t)
                        = Sigma_{k=1}^{X} mu(k) [H(X) - H(k-1)]
```

So:
```
Sigma M(t)/t = H(X) * Sigma_{k=1}^{X} mu(k) - Sigma_{k=1}^{X} mu(k) H(k-1)
             = H(X) * A(X) - B(X)
```

where A(X) = Sigma mu(k) for k <= X, B(X) = Sigma mu(k) H(k-1).

We know A(X) = M(X) = o(X) unconditionally (PNT).

For B(X): by partial summation,
```
B(X) = Sigma mu(k) H(k) = Sigma mu(k) [log k + gamma + O(1/k)]
     = Sigma mu(k) log k + gamma * M(X) + O(Sigma |mu(k)|/k)
```

The classical identity: Sigma_{k=1}^{X} mu(k) log k / k -> -1 (this is equivalent to PNT).

But we need Sigma mu(k) log k (without the 1/k weight).

**Fact:** Sigma_{k<=X} mu(k) log k = -1 + o(1) ... NO. That's the weighted version.

The unweighted version Sigma_{k<=X} mu(k) log k is related to the derivative
of the zeta function. By partial summation from -zeta'(s)/zeta(s) = Sigma Lambda(n)/n^s:

```
Sigma_{k<=X} mu(k) log k = -1 + error terms from PNT
```

More precisely, differentiating 1/zeta(s) = Sigma mu(n)/n^s:
```
-zeta'(s)/zeta(s)^2 = -Sigma mu(n) log(n) / n^s
```
At s = 1 (formally): zeta has a pole, so this needs care.

**This is getting complicated. Let me try a different approach to I(p).**

---

## 4. Direct Evaluation via Hyperbola Method

```
I(p) = Sigma_{n=1}^{N} M(floor(N/n)) / n
```

Use the identity: M(x) = Sigma_{k<=x} mu(k). So:
```
I(p) = Sigma_{n=1}^{N} (1/n) Sigma_{k=1}^{floor(N/n)} mu(k)
     = Sigma_{n=1}^{N} Sigma_{k=1}^{floor(N/n)} mu(k)/n
```

The condition k <= floor(N/n) is equivalent to kn <= N (approximately).
More precisely, k <= N/n iff kn <= N. So:
```
I(p) = Sigma_{kn <= N} mu(k)/n = Sigma_{k=1}^{N} mu(k) Sigma_{n=1}^{floor(N/k)} 1/n
     = Sigma_{k=1}^{N} mu(k) H(floor(N/k))
```

**(This is the clean form.)**

Now, H(floor(N/k)) = log(N/k) + gamma + O(k/N), so:
```
I(p) = Sigma_{k=1}^{N} mu(k) [log(N/k) + gamma + O(k/N)]
     = log(N) * Sigma mu(k) + gamma * Sigma mu(k) - Sigma mu(k) log(k) + O(N^{-1} Sigma k |mu(k)|)
```

The error term: Sigma_{k<=N} k |mu(k)| <= Sigma k = O(N^2), so divided by N gives O(N). Too big!

**Fix:** Use H(floor(N/k)) more carefully. Write floor(N/k) = N/k - {N/k} where {.} is fractional part.
```
H(floor(N/k)) = log(N/k) + gamma - {N/k}/(N/k) + O(k^2/N^2)
              = log(N/k) + gamma + O(k/N)
```

The O(k/N) error gives:
```
Sigma_{k<=N} |mu(k)| * O(k/N) = O(N^{-1}) * Sigma_{k<=N} k = O(N)
```

This error is O(N), which is too large (we want to show I(p) ~ log N).

**Resolution:** Split the sum at k = sqrt(N).

For k <= sqrt(N): the error per term is O(k/N) = O(1/sqrt(N)), and there are
sqrt(N) terms, so total error is O(1). Good.

For k > sqrt(N): floor(N/k) < sqrt(N), so H(floor(N/k)) <= log(sqrt(N)) + O(1).
The contribution from these terms is:
```
|Sigma_{k > sqrt(N)} mu(k) H(floor(N/k))| <= [log(sqrt(N)) + O(1)] * |Sigma_{sqrt(N) < k <= N} mu(k)|
```

But Sigma mu(k) for k in (sqrt(N), N] = M(N) - M(sqrt(N)), which is o(N) by PNT.

Actually this bound is terrible. We need |M(X)| = o(X) but we're multiplying by log N,
getting o(N log N) which doesn't help.

**The problem is clear:** I(p) involves a sum of mu(k) weighted by log(N/k), and extracting
the main term requires PNT-strength information about mu.

---

## 5. The Main Term IS 1

**Key classical result:**
```
Sigma_{k=1}^{X} mu(k) log(X/k) / k = 1 + o(1)    as X -> infinity
```
This is equivalent to the prime number theorem (it's essentially -zeta'(1)/zeta(1) in Cesaro sense).

But our sum is:
```
I(p) = Sigma_{k=1}^{N} mu(k) H(floor(N/k))
```

which is Sigma mu(k) * [log(N/k) + gamma + ...] (WITHOUT the 1/k weight).

This is a DIFFERENT object. The 1/k-weighted version converges; the unweighted
version involves the full Mertens function M(N), which is wildly oscillating.

**Re-examine:** Write I(p) = Sigma mu(k) H(N/k).

Using the Dirichlet hyperbola method in the OTHER direction:
```
I(p) = Sigma_{kn <= N} mu(k)/n
```

This is the sum of mu(k)/n over the hyperbolic region kn <= N.

By the hyperbola method with cutoff at T:
```
I(p) = Sigma_{k<=T} mu(k) H(N/k) + Sigma_{n<=N/T} (1/n) M(N/n) - M(T) H(N/T)
     = S_1 + S_2 - S_3
```

Taking T = sqrt(N):
```
S_1 = Sigma_{k<=sqrt(N)} mu(k) [log(N/k) + gamma + O(k/N)]
    = (log N + gamma) M(sqrt(N)) - Sigma_{k<=sqrt(N)} mu(k) log k + O(1)

S_2 = Sigma_{n<=sqrt(N)} M(sqrt(N)) / n    ... NO, M(N/n) not M(sqrt(N))
```

**Let me be more careful with S_2:**
```
S_2 = Sigma_{n=1}^{floor(N/T)} (1/n) M(floor(N/n))
```

For n <= sqrt(N), M(N/n) varies. This is essentially the SAME sum we started with
but over a shorter range. This is the self-similar structure of hyperbola sums.

---

## 6. Numerical Computation

Before going further analytically, let's compute I(p) for small primes to see
the actual growth rate.

```
I(p) = Sigma_{k=1}^{N} mu(k) H(floor(N/k))
```

| p   | N   | I(p)   | I(p)/log(p) |
|-----|-----|--------|-------------|
| TBD | TBD | TBD    | TBD         |

**Action needed:** Run a computation of I(p) for primes up to 10000
to determine whether I(p) ~ C log p, and what C is.

---

## 7. The Montgomery-Vaughan Connection (Revisited)

The original strategy was to use the fourth moment identity:
```
Sigma_chi |L(1,chi)|^2 |Lambda(chi)|^2
```

With L(1,chi) = Sigma 1/n * chi(n) (convergent for non-principal chi, but let's use
the partial sums up to N for uniformity), and Lambda_p(chi) = Sigma lambda_p(m) chi(m).

Setting a_n = 1/n and b_m = lambda_p(m), the fourth moment identity gives:
```
Sigma_{chi mod p} |Sigma (1/n) chi(n)|^2 |Sigma lambda_p(m) chi(m)|^2
= (p-1) [Sigma 1/n^2 * Sigma lambda_p(m)^2 + |Sigma lambda_p(n)/n|^2]
```

**Wait -- this uses the FULL character sum including chi_0 and even characters.**

The exact orthogonality identity for all characters mod p:
```
Sigma_{chi mod p} |A(chi)|^2 |B(chi)|^2 = (p-1) Sigma_{n mod p} |a_n|^2 Sigma_{m mod p} |b_m|^2
                                          + (p-1) |Sigma_n a_n conj(b_n)|^2
```

**NO, this is wrong.** The correct identity is more nuanced. Let me state it carefully.

### Exact Fourth Moment Identity

For sequences a = (a_1, ..., a_{p-1}) and b = (b_1, ..., b_{p-1}):
```
(1/(p-1)) Sigma_{chi mod p} |Sigma_n a_n chi(n)|^2 |Sigma_m b_m chi(m)|^2
```

Expand:
```
= (1/(p-1)) Sigma_{n,m,r,s} a_n conj(a_m) b_r conj(b_s) Sigma_chi chi(n) conj(chi(m)) chi(r) conj(chi(s))
= (1/(p-1)) Sigma_{n,m,r,s} a_n conj(a_m) b_r conj(b_s) Sigma_chi chi(nr * (ms)^{-1})
```

where the product and inverse are mod p.

The character sum Sigma_chi chi(x) = (p-1) if x = 1 mod p, and 0 otherwise.

So the condition is: nr ≡ ms (mod p), i.e., n/m ≡ s/r (mod p).

```
= Sigma_{n,m,r,s: nr≡ms} a_n conj(a_m) b_r conj(b_s)
```

This can be decomposed by the "diagonal" nr = ms (as integers, not just mod p)
and the "off-diagonal" terms where nr ≢ ms as integers but nr ≡ ms mod p.

For n, m, r, s in {1, ..., p-1}: nr and ms are in {1, ..., (p-1)^2}.
The condition nr ≡ ms mod p with 1 <= n,m,r,s <= p-1 means either
nr = ms (as integers) or |nr - ms| >= p.

The diagonal nr = ms contributes:
```
D = Sigma_{nr=ms} a_n conj(a_m) b_r conj(b_s)
```

This factors over the divisor structure: nr = ms iff n/m = s/r as rationals.

### Separating diagonal and off-diagonal

For the DIAGONAL (nr = ms as integers):
```
D = Sigma_{d | gcd possibilities} ... [complex combinatorics]
```

A simpler way: if a_n = 1/n and b_m = lambda_p(m), then:
```
D = Sigma_{nr=ms} (1/n)(1/m) lambda_p(r) lambda_p(s)
```

Hmm, this is (Sigma_{nr=ms} ...) which doesn't factor simply.

**Cleaner approach:** For real-valued a_n, b_n:
```
Sigma_{chi} |A(chi)|^2 |B(chi)|^2 = Sigma_{chi} A(chi) conj(A(chi)) B(chi) conj(B(chi))
```

Let's use a DIFFERENT decomposition. Note that:
```
|A|^2 |B|^2 = |A*B|^2 ... NO, |AB|^2 != |A|^2|B|^2 in general.
```

**Instead, use Cauchy-Schwarz as a LOWER bound:**
```
Sigma_chi |A(chi)|^2 |B(chi)|^2 >= |Sigma_chi A(chi) conj(B(chi)) |^2 / (number of chi)
```

... No, that's Cauchy-Schwarz in the wrong direction.

---

## 8. The Clean Lower Bound via Cauchy-Schwarz

**This is the key insight.** By Cauchy-Schwarz:
```
[Sigma_chi |L(1,chi)|^2 |Lambda(chi)|^2] * [Sigma_chi 1]
>= |Sigma_chi |L(1,chi)| * |Lambda(chi)||^2
```

But we want a lower bound on the LHS, and the RHS involves first moments
which are harder to compute.

**Better: Use the inner product directly.**

Define for each chi: f(chi) = L(1,chi), g(chi) = Lambda_p(chi). Then:
```
Sigma |f|^2 |g|^2 >= |Sigma f * conj(g)|^2 / Sigma 1
```

The object Sigma_chi L(1,chi) conj(Lambda_p(chi)) is exactly a "twisted" sum.

By orthogonality:
```
Sigma_{chi mod p} L(1,chi) conj(Lambda_p(chi))
= Sigma_{chi} [Sigma_n chi(n)/n] [Sigma_m lambda_p(m) conj(chi(m))]
= Sigma_{n,m} (lambda_p(m)/n) Sigma_chi chi(n) conj(chi(m))
= (p-1) Sigma_{n=m} lambda_p(n)/n
= (p-1) * I(p)
```

where I(p) = Sigma_{n=1}^{N} lambda_p(n)/n as defined above!

**CAUTION:** L(1,chi) for chi = chi_0 has a pole. We need to handle the principal
character separately. For chi_0: L(1,chi_0) is not well-defined (pole of zeta at s=1).

For chi != chi_0: L(1,chi) = Sigma_{n=1}^{infty} chi(n)/n converges.

So the correct statement restricts to non-principal characters:
```
Sigma_{chi != chi_0} L(1,chi) conj(Lambda_p(chi)) = (p-1) I(p) - L(1,chi_0) conj(Lambda_p(chi_0)) + correction
```

The chi_0 contribution: Lambda_p(chi_0) = Sigma lambda_p(m) = Sigma_{m=1}^{N} M(floor(N/m)).

**This is the Mertens-type sum.** Its value is N (since Sigma_{m<=N} M(N/m) = N by Mobius inversion: this is the well-known identity Sigma_{k<=x} 1 = Sigma_{d<=x} M(x/d) * 1 ... actually Sigma_{d<=x} mu(d) floor(x/d) = 1, not N.)

Actually: Sigma_{m=1}^{N} M(floor(N/m)) = Sigma_{m=1}^{N} Sigma_{k=1}^{floor(N/m)} mu(k)
= Sigma_{km<=N} mu(k) = Sigma_{k<=N} mu(k) floor(N/k) = 1 (by Mobius inversion).

**So Lambda_p(chi_0) = 1.**

And L(1, chi_0) has a pole. However, for the partial sum Sigma_{n=1}^{N} chi_0(n)/n = H(N) - corrections for multiples of p. Since p > N = p-1, there are no multiples of p in {1,...,N}, so Sigma chi_0(n)/n = H(N) = log N + gamma + O(1/N).

So the chi_0 contribution is approximately log(N) * 1 = log N.

The full sum over ALL chi:
```
Sigma_{chi mod p} L_N(1,chi) conj(Lambda_p(chi)) = (p-1) I(p)
```

where L_N(1,chi) = Sigma_{n=1}^{N} chi(n)/n.

And (p-1) I(p) = (p-1) Sigma_{n=1}^{N} lambda_p(n)/n.

---

## 9. Cauchy-Schwarz Lower Bound

Restricting to odd characters chi (since K_hat vanishes on even characters):

**Step 1:** Compute
```
J = Sigma_{chi odd} L(1,chi) conj(Lambda_p(chi))
```

This requires splitting the full sum into odd and even parts.

For odd chi: chi(-1) = -1, so chi(p-n) = -chi(n).
The projector onto odd characters is: (1/2)[Sigma_chi - Sigma_chi chi(-1)].

```
J = (1/2) [(p-1) I(p) - Sigma_chi chi(-1) L_N(1,chi) conj(Lambda_p(chi))]
```

The second sum:
```
Sigma_chi chi(-1) L_N(1,chi) conj(Lambda_p(chi))
= Sigma_{n,m} lambda_p(m)/n * Sigma_chi chi(-1) chi(n) conj(chi(m))
= Sigma_{n,m} lambda_p(m)/n * Sigma_chi chi(-m^{-1} n)   [since chi(-1)chi(n)chi_bar(m) = chi(-n/m)]
= (p-1) Sigma_{n: -n ≡ m mod p} lambda_p(m)/n
= (p-1) Sigma_{n=1}^{N} lambda_p(p-n)/n
```

Since lambda_p(m) = M(floor(N/m)) and p - n ranges over {1, ..., N} as n does (just reversed):
```
= (p-1) Sigma_{n=1}^{N} M(floor(N/(p-n)))/n
= (p-1) Sigma_{n=1}^{N} M(floor(N/(N+1-n)))/n
```

For n = 1: floor(N/N) = 1, M(1) = 1
For n = 2: floor(N/(N-1)) = 1, M(1) = 1
...
For n = N: floor(N/1) = N, M(N)

So this is Sigma M(floor(N/(N+1-n)))/n = Sigma_{j=1}^{N} M(floor(N/j))/(N+1-j)
(substituting j = N+1-n).

This is close to I(p) but with weights 1/(N+1-j) instead of 1/j. For large N,
1/(N+1-j) and 1/j are very different (one emphasizes small j, the other large j).

Define:
```
I^*(p) = Sigma_{j=1}^{N} M(floor(N/j)) / (N+1-j)
```

Then:
```
J = (1/2)(p-1)[I(p) - I^*(p)]
```

**Step 2:** Apply Cauchy-Schwarz:
```
Sigma_{chi odd} |L(1,chi)|^2 |Lambda(chi)|^2  >=  |J|^2 / Sigma_{chi odd} 1
                                                =  |J|^2 / ((p-1)/2)
                                                =  (p-1)/2 * |I(p) - I^*(p)|^2 / 4 * (p-1)^2 / ((p-1)/2)
```

Wait, let me redo this:
```
|J|^2 / ((p-1)/2) = [(p-1)/2]^2 |I(p) - I^*(p)|^2 / ((p-1)/2)
                   = (p-1)/2 * |I(p) - I^*(p)|^2 / 4 ...
```

Hmm, let me just write it cleanly:
```
J = (p-1)/2 * [I(p) - I^*(p)]
|J|^2 = (p-1)^2/4 * |I(p) - I^*(p)|^2
Number of odd chi = (p-1)/2

Sigma_{chi odd} |L|^2 |Lambda|^2 >= |J|^2 / ((p-1)/2)
                                   = (p-1)^2 / 4 * |I(p) - I^*(p)|^2 * 2/(p-1)
                                   = (p-1)/2 * |I(p) - I^*(p)|^2
```

So we need: |I(p) - I^*(p)| >> sqrt(p * log p).

If I(p) ~ C log p and I^*(p) is smaller (or has different sign), this could work.

---

## 10. What Remains to Prove

**The entire argument reduces to understanding two sums:**

```
I(p)   = Sigma_{n=1}^{N} M(floor(N/n)) / n           (forward harmonic Mertens)
I^*(p) = Sigma_{n=1}^{N} M(floor(N/n)) / (N+1-n)     (reversed harmonic Mertens)
```

**Needed:** Show |I(p) - I^*(p)|^2 >> p * log p.

The difference I - I^* emphasizes the asymmetry between small and large n:
```
I(p) - I^*(p) = Sigma_{n=1}^{N} M(floor(N/n)) * [1/n - 1/(N+1-n)]
```

For n << N: 1/n - 1/(N+1-n) ≈ 1/n (dominant)
For n ≈ N/2: 1/n - 1/(N+1-n) ≈ 0 (cancels)
For n >> N/2: 1/n - 1/(N+1-n) ≈ -1/(N-n) (opposite sign)

So I - I^* is dominated by small n where M(floor(N/n)) = M(N/n) involves
large arguments of M, and 1/n is large.

---

## 11. Alternative: Direct Lower Bound on I(p) via Cauchy-Schwarz on All Characters

If we DON'T restrict to odd characters but use ALL non-principal characters:

```
Sigma_{chi != chi_0} |L_N(1,chi)|^2 |Lambda(chi)|^2
>= |Sigma_{chi != chi_0} L_N(1,chi) conj(Lambda(chi))|^2 / (p-2)
```

And:
```
Sigma_{chi != chi_0} L_N(1,chi) conj(Lambda(chi))
= (p-1) I(p) - L_N(1,chi_0) Lambda(chi_0)
= (p-1) I(p) - (log N + gamma + O(1/N)) * 1
```

If I(p) >> 1, then this is ~ (p-1) I(p), giving:
```
Sigma_{chi != chi_0} |L_N|^2 |Lambda|^2 >= (p-1)^2 I(p)^2 / (p-2) ~ (p-1) I(p)^2
```

We need this to be >> p^2 log p, so we need I(p)^2 >> p log p, i.e., I(p) >> sqrt(p log p).

**But this seems unlikely** -- I(p) should be O(log p) or O(sqrt(N)), not O(sqrt(p log p)).

**Conclusion:** The Cauchy-Schwarz approach with L(1,chi) and Lambda(chi) separately
is TOO WEAK by itself. We lose a factor of p because the number of characters is ~ p
but the inner product only captures O(1) of the structure.

---

## 12. Refined Approach: Use K_hat Weights

Since K_hat(chi) = p |L(1,chi)|^2 / pi^2 for odd chi, the spectral sum is:
```
Q = (1/(p-1)) Sigma_{chi odd} K_hat(chi) |Lambda(chi)|^2
  = (p/(pi^2(p-1))) Sigma_{chi odd} |L(1,chi)|^2 |Lambda(chi)|^2
```

By Cauchy-Schwarz with K_hat weights:
```
[Sigma K_hat |Lambda|^2] [Sigma K_hat] >= [Sigma K_hat |Lambda|]^2
```

And:
```
Sigma_{chi odd} K_hat(chi) = (p/pi^2) Sigma_{chi odd} |L(1,chi)|^2
```

The mean value of |L(1,chi)|^2 over odd characters is known:
```
Sigma_{chi odd} |L(1,chi)|^2 = (pi^2/6)(p-1)/2 * [1 + O(1/p)]
```

Actually this needs to be checked: the mean value over ALL non-principal chi is pi^2/6
per character, but odd vs even may differ.

So Sigma K_hat ~ (p/pi^2) * (pi^2/6) * (p-1)/2 = p(p-1)/12.

**To get a good lower bound via this weighted Cauchy-Schwarz, we'd need Sigma K_hat |Lambda| to be large.** This seems hard without more information.

---

## 13. NUMERICAL RESULTS

### Growth of I(p) and I-I*

Computation for primes up to p = 10000 reveals:

```
Power law fit:  |I(p)|   ~ 3.09 * p^{0.162}
                |I-I*|   ~ 4.91 * p^{0.172}
```

Both grow MUCH slower than sqrt(p). The exponent ~0.16 is close to
what one would expect from the Mertens function contribution (since
M(x) ~ x^{1/2+eps} under RH, and the harmonic weighting damps it).

### Cauchy-Schwarz vs Actual

| p   | Actual sum |  CS bound | Ratio (how much CS loses) |
|-----|-----------|-----------|---------------------------|
| 5   | 5.9       | 5.6       | 1.1x                      |
| 17  | 378       | 175       | 2.2x                      |
| 97  | 27328     | 2945      | 9.3x                      |
| 199 | 135825    | 24260     | 5.6x                      |
| 337 | 391380    | 20610     | 19.0x                      |
| 499 | 888285    | 70726     | 12.6x                      |

**The Cauchy-Schwarz bound loses a factor that grows with p** (roughly as p^0.3-0.5).

The actual sum satisfies:
```
Sigma_{chi odd} |L(1,chi)|^2 |Lambda(chi)|^2 / (p^2 logp) -> ~0.58-0.63
```
confirming the growth IS p^2 logp with a constant ~0.6.

But the CS lower bound gives only:
```
CS_bound / (p^2 logp) -> ~0.04  (and decreasing!)
```

### Diagnosis

The Cauchy-Schwarz inequality is:
```
Sigma |L|^2 |Lambda|^2 >= |Sigma L * conj(Lambda)|^2 / ((p-1)/2)
```

The LHS grows as ~0.6 p^2 logp.
The cross-correlation |Sigma L * Lambda_bar|^2 grows as ~(p-1)^2 * |I-I*|^2/4
~ p^2 * p^{0.34} = p^{2.34}.
Dividing by (p-1)/2 gives ~p^{1.34}.

So CS gives p^{1.34} vs actual p^2 logp -- a gap of ~p^{0.66}/logp.

**The inner product Sigma L(1,chi) Lambda_bar(chi) is TOO SMALL** to capture
the full strength of the weighted fourth moment. The correlation between
|L(1,chi)|^2 and |Lambda(chi)|^2 (which was identified in the Dedekind spectral
analysis as ~0.5-0.95 and growing) is NOT captured by the first moment
Cauchy-Schwarz.

---

## 14. WHY CAUCHY-SCHWARZ FAILS AND WHAT WOULD WORK

### The fundamental issue

Cauchy-Schwarz with f = L(1,chi), g = Lambda(chi) captures only the
CORRELATION between L and Lambda, not the correlation between |L|^2 and |Lambda|^2.

For large p, the characters chi where |L(1,chi)|^2 is large are ALSO
the ones where |Lambda(chi)|^2 is large (correlation ~0.9). This means
the product |L|^2 |Lambda|^2 is MUCH larger than |L * Lambda|^2 on average.

In probabilistic terms: if X, Y are positively correlated random variables,
E[X^2 Y^2] >> (E[XY])^2 / n. The ratio grows with the correlation between
X^2 and Y^2 (not just between X and Y).

### What would work

**Approach A: Prove the |L|^2 - |Lambda|^2 correlation directly.**
Show that Sigma_{chi odd} |L(1,chi)|^2 |Lambda(chi)|^2 >= c * [Sigma |L|^2] * [Sigma |Lambda|^2] / ((p-1)/2).
This requires showing the distributions aren't anti-correlated, which should follow
from the arithmetic structure.

If Sigma |L|^2 ~ (pi^2/6)(p-1)/2 and Sigma |Lambda|^2 >= (3/4)(p-1)^2
(proved in ODD_ENERGY_LOWER_BOUND.md), then:
```
Sigma |L|^2 |Lambda|^2 >= c * (pi^2/12)(p-1) * (3/4)(p-1)^2 / ((p-1)/2)
                        = c * (pi^2/8)(p-1)^2
```
This gives p^2 but NOT p^2 logp. So even proving independence (c = 1) is
not enough -- we need the POSITIVE correlation to get the log factor.

**Approach B: Fourth moment identity with off-diagonal terms.**
The full identity Sigma_chi |A|^2 |B|^2 involves the set {(n,m,r,s): nr ≡ ms mod p}.
The diagonal nr = ms gives the "random" contribution. The off-diagonal
nr ≡ ms mod p with nr != ms gives the EXTRA contribution that produces logp.
This requires Kloosterman-type sum estimates.

**Approach C: Hybrid spectral/analytic.**
Use the PROVED identity K_hat(chi) = p|L(1,chi)|^2/pi^2 to rewrite:
```
Q = (1/(pi^2(p-1))) Sigma_{chi odd} K_hat(chi) |Lambda(chi)|^2 * (pi^2/p) * p
```
Then decompose Lambda(chi) using the reciprocal-interval structure and
estimate the resulting double sum directly, avoiding the character sum
orthogonality step entirely.

---

## 15. STATUS AND NEXT STEPS

### Established results:
1. Lambda_p decomposes into character sums over reciprocal intervals (Section 1)
2. I(p) = Sigma lambda_p(n)/n = Sigma mu(k) H(N/k) (key inner product)
3. Lambda_p(chi_0) = 1 (Mobius inversion)
4. **I(p) ~ 3.1 * p^{0.162}** -- grows slowly (COMPUTED)
5. **Cauchy-Schwarz loses a factor ~ p^{0.66}** -- INSUFFICIENT for the bound (COMPUTED)
6. The actual sum Sigma |L|^2 |Lambda|^2 ~ 0.6 * p^2 * logp (CONFIRMED numerically)

### Dead ends:
- **Cauchy-Schwarz on first moments:** Proven numerically insufficient (Section 13-14)
- **Montgomery-Vaughan diagonal only:** Gives p^2 not p^2 logp

### Promising directions:
1. **Prove the positive correlation** between |L(1,chi)|^2 and |Lambda(chi)|^2
   for odd characters -- this is WHERE the logp lives
2. **Off-diagonal fourth moment terms** -- Kloosterman sums control the extra contribution
3. **Direct spectral decomposition** avoiding Cauchy-Schwarz entirely

### Key insight gained:
The logp factor in Sigma |L|^2 |Lambda|^2 comes from the POSITIVE CORRELATION
between |L(1,chi)|^2 and |Lambda(chi)|^2 over odd characters. This correlation
(empirically ~0.5-0.95 and growing) means characters that "see" the primes strongly
(large |L(1,chi)|) also "see" the Mertens oscillations strongly (large |Lambda(chi)|).
This is an arithmetic phenomenon that Cauchy-Schwarz on first moments cannot capture.

---

## Files

- This file: `RECIPROCAL_INTERVAL_ATTACK.md`
- `reciprocal_interval_compute.py` -- I(p) and I*(p) computation
- `reciprocal_interval_scaling.py` -- power law scaling analysis
- `reciprocal_interval_diagnosis.py` -- CS vs actual comparison
- Related: `CHARACTER_SUM_PROOF.md` (prior failed per-denominator approach)
- Related: `DEDEKIND_SPECTRAL_ATTACK.md` (spectral framework, correlation identified)
- Related: `ODD_ENERGY_LOWER_BOUND.md` (Lambda energy bounds)
