# Erdos-Turan Analytical Approach to B+C > 0

## Date: 2026-03-26

---

## 1. Setup and Goal

### The Fourier decomposition of B_raw

From the cotangent formula (proved in Session 3), the raw covariance B_raw decomposes into Fourier modes:

    B_raw = Sum_{h=1}^{N} B_raw|_h

where the h-th mode is:

    B_raw|_h = S_N(h) / (2*pi) * C_h(p)

with:
- S_N(h) = Sum_{d|h, d<=N} d * M(floor(N/d))   (Mertens-weighted divisor sum)
- C_h(p) = Sum_{prime b<=N} [cot(pi*h*rho_b/b) - cot(pi*h/b)]   (cotangent sum)
- rho_b = p mod b

### What is proved

The h=1 mode satisfies B_raw|_{h=1} >= 3 * delta_sq when M(N) <= -3, because:
- S_N(1) = M(N) <= -3
- C_1(p) = Sum_{prime b<=N} [cot(pi*rho_b/b) - cot(pi/b)] < 0 (all terms negative)
- Product: negative * negative = positive
- Quantitatively: B_raw|_{h=1} ~ |M(N)| * N^2 / (4*pi^2 * log N) >= 3 * delta_sq

### The gap

Need to show: |Sum_{h>=2} B_raw|_h| < 3 * delta_sq ~ 3*N^2/(48*log N) = N^2/(16*log N).

Equivalently, need |Sum_{h>=2} B_raw|_h| < N^2/(16*log N).

---

## 2. The Erdos-Turan Inequality: Setup

### Classical form

The Erdos-Turan inequality bounds the discrepancy of a finite sequence
{x_1, ..., x_K} in [0,1) from its exponential sums. For K points:

    D_K := sup_I |#{x_j in I}/K - |I|| <= C * (1/H + Sum_{j=1}^{H} (1/j) * |Sum_{k=1}^{K} e(j*x_k)| / K)

for any positive integer H, where C is an absolute constant (C = 1 in the
Koksma-Hlawka refinement with C/(H+1) + ...).

### Application to the cotangent sum C_h(p)

For fixed h >= 2, we want to bound C_h(p) = Sum_{prime b<=N} [cot(pi*h*rho_b/b) - cot(pi*h/b)].

**Key idea:** The cotangent function cot(pi*t) for t in (0,1) has the Fourier expansion:

    cot(pi*t) = (1/pi) * Sum_{m=1}^{infty} (2/m) * sin(2*pi*m*t)  ???

No -- let me use the correct relationship. The cotangent cot(pi*x) has the partial fraction expansion:

    cot(pi*x) = (1/pi) * lim_{M->inf} Sum_{m=-M}^{M} 1/(x-m) = (1/pi*x) + (2x/pi) * Sum_{m=1}^{inf} 1/(x^2-m^2)

This is not directly useful for Erdos-Turan. Instead, let us work with the
exponential-sum representation of the cotangent difference.

### Direct approach: bounding |C_h(p)| via exponential sums

For each prime b, define the fractional part:

    alpha_b := h*rho_b/b mod 1,    beta_b := h/b mod 1

(Here rho_b = p mod b, so alpha_b = h*p/b mod 1, and beta_b = h/b mod 1.)

Note: for b > h, we have beta_b = h/b (no reduction mod 1 needed).

The cotangent difference is:

    cot(pi*alpha_b') - cot(pi*beta_b')

where alpha_b' = h*rho_b/b (NOT reduced mod 1, but in (0, h)) and
beta_b' = h/b (in (0,1) for b > h).

**Problem:** cot(pi*x) has poles at integers, and h*rho_b/b can be anywhere
in {h/b, 2h/b, ..., h*(b-1)/b}. When h*rho_b/b passes through an integer,
cot(pi*h*rho_b/b) changes sign dramatically. This is the fundamental obstacle
for h >= 2: the cotangent at frequency h has poles that create large,
sign-varying terms.

### Reformulation via Bernoulli/sawtooth functions

A cleaner approach uses the sawtooth function psi(x) = {x} - 1/2 (where {x}
is the fractional part), related to cot by:

    cot(pi*x) = -(1/pi) * [1/({x} - 1/2) + ...] -- not quite.

Actually, the connection is through the Fourier series of the sawtooth:

    psi(x) = {x} - 1/2 = -(1/pi) * Sum_{m=1}^{inf} sin(2*pi*m*x)/m

And: cot(pi*x) = (2/pi) * Sum_{m=1}^{inf} sin(2*pi*m*x) * ???

Let me be more careful. The correct Fourier expansion is:

    cot(pi*x) = (1/pi) PV Sum_{n=-inf}^{inf} 1/(x-n)

For x in (0,1): cot(pi*x) = (1/pi)*(1/x + Sum_{n=1}^{inf} [1/(x-n) + 1/(x+n)])
                            = (1/pi)*(1/x + 2x*Sum_{n=1}^{inf} 1/(x^2-n^2))

The key identity connecting cot to exponential sums is:

    cot(pi*x) = -i - (2i)/(e^{2*pi*i*x} - 1) = -i * (1 + e^{2*pi*i*x})/(1 - ... )

No, let me use the standard: for x in (0,1),

    cot(pi*x) = (i/pi) * [pi*cot(pi*x)] * (1/i)

Actually, for practical purposes we need:

    pi * cot(pi*x) = 1/x + Sum_{n=1}^{inf} (1/(x+n) + 1/(x-n))
                   = lim_{M} Sum_{n=-M}^{M} 1/(x-n)

And the finite sum identity (which was used in Session 3):

    Sum_{a=1}^{b-1} cot(pi*a/b) * e^{2*pi*i*k*a/b} = -b + 2*b/(e^{2*pi*i*k/b}-1) for b nmid k

This is complex. Let me take a more direct approach.

---

## 3. Direct Bound on |C_h(p)| for h >= 2

### Splitting into "regular" and "singular" parts

For fixed h and prime b > h, write h*rho_b/b and h/b. Since 1 <= rho_b <= b-1:

    h*rho_b/b in {h/b, 2h/b, ..., h(b-1)/b}

For b > h, we have h/b < 1, so h*1/b = h/b < 1. But h*rho_b/b can range up to
h*(b-1)/b < h. The cotangent cot(pi*h*rho_b/b) has poles when h*rho_b/b is an
integer, i.e., when b | h*rho_b. Since b is prime and b > h, this means b | rho_b,
which is impossible (1 <= rho_b <= b-1). So for b prime and b > h:

**cot(pi*h*rho_b/b) is well-defined (no poles).**

For b <= h: there are at most pi(h) = O(h/log h) such primes. Each contributes
|cot(pi*h*rho_b/b) - cot(pi*h/b)| <= O(b) (crude bound since cot can be O(b/pi) near 0).

So the "small b" contribution is at most O(h^2/log h), negligible for our purposes.

### Mean value of C_h(p) over p

For fixed h and b, as p ranges over integers (or primes) coprime to b,
rho_b = p mod b ranges over coprime residues mod b. For b prime:

    E_{rho_b}[cot(pi*h*rho_b/b)] = (1/(b-1)) * Sum_{a=1}^{b-1} cot(pi*h*a/b)

The sum Sum_{a=1}^{b-1} cot(pi*h*a/b):
- If b | h: this sum is (b-1) * cot(0) -- undefined (pole). But b prime and b > h, so b nmid h.
- If b nmid h: Sum_{a=1}^{b-1} cot(pi*h*a/b) = 0 (standard identity: for h not divisible by b,
  the sum of cot(pi*k/b) over all k=1..b-1 weighted by e^{2*pi*i*..} gives 0 in the
  unweighted case).

**Proof of Sum_{a=1}^{b-1} cot(pi*h*a/b) = 0 for gcd(h,b)=1:**

Since gcd(h,b)=1, as a ranges over {1,...,b-1}, ha mod b also ranges over {1,...,b-1}.
Therefore Sum_{a=1}^{b-1} cot(pi*ha/b) = Sum_{a=1}^{b-1} cot(pi*a/b) = 0.
(The last equality is the standard fact that Sum_{a=1}^{b-1} cot(pi*a/b) = 0, which
follows from pairing a with b-a: cot(pi*a/b) + cot(pi*(b-a)/b) = cot(pi*a/b) - cot(pi*a/b) = 0.
Wait: cot(pi - x) = -cot(x), so cot(pi*(b-a)/b) = cot(pi - pi*a/b) = -cot(pi*a/b). Correct.)

More generally, for gcd(h,b) = g > 1 with b prime, we need g = 1 (since b is prime and h < b),
so the condition gcd(h,b)=1 holds for all primes b > h.

**Therefore: the "expected value" of cot(pi*h*rho_b/b) over uniform rho_b is 0.**

This means:

    E[C_h(p)] = Sum_{b prime, b>h} [0 - cot(pi*h/b)] = -Sum_{b prime, b>h} cot(pi*h/b)

For large b: cot(pi*h/b) ~ b/(pi*h) (small angle approximation).

    -Sum_{b prime, h<b<=N} cot(pi*h/b) ~ -(1/(pi*h)) * Sum_{b prime, b<=N} b ~ -N^2/(2*pi*h*log N)

So the "mean" of C_h(p) is ~ -N^2/(2*pi*h*log N), which is the same order as C_1(p) / h.

### Deviation of C_h(p) from its mean

The deviation is:

    C_h(p) - E[C_h(p)] = Sum_{b prime} cot(pi*h*rho_b/b) - 0 = Sum_{b prime} cot(pi*h*rho_b/b)

We need to bound |Sum_{prime b <= N} cot(pi*h*(p mod b)/b)|.

**This is the critical exponential sum.** For each b, cot(pi*h*rho_b/b) depends on p mod b,
and as b ranges over primes, these residues are "pseudo-independent."

### Applying Erdos-Turan: bounding the cotangent sum via discrepancy

The Erdos-Turan inequality is normally applied to sequences of points on [0,1).
Here we have the sequence {h*rho_b/b mod 1 : b prime, b <= N} (with b > h).

Let x_b = h * (p mod b) / b mod 1 for each prime b in (h, N].

The number of primes is K = pi(N) - pi(h) ~ N/log N.

The cotangent sum is:

    Sum_b cot(pi * h*rho_b/b) = Sum_b cot(pi * {h*rho_b/b})    (when no integer crossing)

For b > h (prime), as shown above, h*rho_b/b is not an integer, so {h*rho_b/b}
is well-defined and nonzero.

Now, cot(pi*x) for x in (0,1) is a specific function. We can bound
|Sum_b cot(pi*x_b)| using the fact that cot(pi*x) has the Fourier expansion:

    cot(pi*x) = (2/pi) * Sum_{m odd, m>=1} ...

Actually, for x in (0,1):

    cot(pi*x) = (1/pi) * [1/x - 1/(1-x)] + (1/pi) * Sum_{n=1}^{inf} [1/(x+n) + 1/(x-n) + 1/(n-x) + ...]

This is getting unwieldy. Let me use a different approach.

**Truncated Fourier approach:** For x in (0,1), we can write

    cot(pi*x) = (1/pi) * PV Sum_n 1/(x-n) = (1/pi*x) + (1/pi) Sum_{n=1}^{inf} [2x/(x^2-n^2)]

Alternatively, use the well-known Fourier series on (0,1):

    cot(pi*x) = (1/pi) * [1/x + 2x * Sum_{n=1}^{inf} 1/(x^2-n^2)]

For BOUNDING purposes, the key fact is:

    |cot(pi*x)| <= 1/(pi * min(x, 1-x))

So for x_b = {h*rho_b/b} distributed (pseudo-)uniformly in (0,1):

    |Sum_b cot(pi*x_b)| = |Sum_b 1/(pi * tan(pi*x_b))|

The terms with x_b near 0 or 1 (i.e., h*rho_b close to a multiple of b) give
large contributions of order b/h (since x_b ~ k/b for small k means
|cot(pi*x_b)| ~ b/(pi*k)).

### Variance estimate

For rho_b uniform on {1,...,b-1} (or more precisely, for p mod b equidistributed
over coprime residues, which it is for "generic" p by Dirichlet's theorem):

    E[cot(pi*h*rho_b/b)^2] = (1/(b-1)) * Sum_{a=1}^{b-1} cot^2(pi*h*a/b)

Standard identity: Sum_{a=1}^{b-1} cot^2(pi*a/b) = (b-1)(b-2)/3.

Since gcd(h,b)=1 for b prime, b > h: ha mod b permutes {1,...,b-1}, so:

    Sum_{a=1}^{b-1} cot^2(pi*ha/b) = Sum_{a=1}^{b-1} cot^2(pi*a/b) = (b-1)(b-2)/3

Therefore:

    E[cot(pi*h*rho_b/b)^2] = (b-2)/3

And the variance of a single term cot(pi*h*rho_b/b) is (b-2)/3.

If the terms were independent across primes b:

    Var[Sum_b cot(pi*h*rho_b/b)] = Sum_b (b-2)/3 ~ (1/3) * Sum_{b prime <= N} b ~ N^2/(6*log N)

    std.dev. ~ N / sqrt(6*log N) ~ 0.4 * N / sqrt(log N)

So the "typical" deviation is O(N/sqrt(log N)).

### Bound on |C_h(p)|

Combining mean and deviation:

    C_h(p) = [mean part] + [deviation]
           = [-N^2/(2*pi*h*log N)] + O(N/sqrt(log N))

For h = O(1): the mean is O(N^2/log N) and the deviation is O(N/sqrt(log N)) << mean.

So |C_h(p)| ~ N^2/(2*pi*h*log N) for small h (with the same sign as C_1).

**But this is a heuristic, not a bound.** The "independence" assumption is not justified.

### Rigorous bound via exponential sums over primes

The sum Sum_{prime b <= N} cot(pi*h*(p mod b)/b) can be bounded using the
Vinogradov/Vaughan method for exponential sums over primes.

Write cot(pi*t) in terms of the sawtooth function. For t not an integer:

    cot(pi*t) = -pi * ((t)) + correction terms

where ((t)) = {t} - 1/2 is the sawtooth. Actually this is NOT correct;
cot(pi*t) and the sawtooth are related but not proportional.

A better decomposition: for x in (0,1),

    cot(pi*x) = (2/pi) * Sum_{j=1}^{J} 1/j * sin(2*pi*j*x) + R_J(x)

where R_J(x) is a remainder satisfying |R_J(x)| <= C/(J * min(x, 1-x)).

Wait -- this isn't the Fourier series of cot. The Fourier series of cot(pi*x)
on (0,1) is actually:

    cot(pi*x) = (2/pi) * Sum_{j=1}^{inf} (something)

Let me derive this. On (0,1), cot(pi*x) is an odd function about x=1/2:
cot(pi*(1-x)) = -cot(pi*x). So its Fourier sine series (about x=1/2) is:

    cot(pi*x) = Sum_{n=1}^{inf} b_n * sin(2*pi*n*(x-1/2))   ???

This is getting complicated. Let me use a more direct approach.

---

## 4. A More Direct Approach: Bounding Sum_{h>=2} B_raw|_h

### Strategy shift: bound the FULL tail, not term by term

Instead of bounding each |B_raw|_h| and summing, use Parseval's identity.

B_raw = Sum_h B_raw|_h, so:

    Sum_{h>=2} B_raw|_h = B_raw - B_raw|_{h=1}

We need |B_raw - B_raw|_{h=1}| < 3 * delta_sq.

Equivalently, since B_raw|_{h=1} >= 3*delta_sq, we need B_raw > 0.

But B_raw > 0 is exactly the conjecture B >= 0 (since B = B_raw for our normalization).

So the question reduces to: **can we prove B_raw > 0 directly?**

If we could, we wouldn't need the Erdos-Turan approach at all.

The Erdos-Turan approach is needed precisely when we can't prove B_raw > 0
directly but want to show the higher modes don't overwhelm the h=1 mode.

### Back to term-by-term: the product structure

    B_raw|_h = S_N(h) / (2*pi) * C_h(p)

For the purpose of bounding |Sum_{h>=2} B_raw|_h|, we need to understand the
interaction between S_N(h) and C_h(p).

**Key structural observation:** S_N(h) and C_h(p) are NOT independent. Both
depend on the arithmetic of h relative to N and p. However, S_N(h) depends only
on h and N (through the Mertens function), while C_h(p) depends on h and p
(through the residues p mod b). For M(N) <= -3, we know specific things about
both factors.

---

## 5. Bounding |S_N(h)| for h >= 2

### Definition

    S_N(h) = Sum_{d|h, d<=N} d * M(floor(N/d))

### Case 1: M(k) <= -3 for all k <= N (uniformly negative Mertens)

This is a STRONG condition, much stronger than just M(N) <= -3. If it holds:

    S_N(h) = Sum_{d|h, d<=N} d * M(N/d)

Each M(N/d) <= -3, so:

    S_N(h) <= -3 * Sum_{d|h, d<=N} d = -3 * sigma_1^{<=N}(h)

where sigma_1^{<=N}(h) = Sum_{d|h, d<=N} d.

For h <= N: sigma_1^{<=N}(h) = sigma_1(h) (the full sum of divisors).

So |S_N(h)| >= 3 * sigma_1(h) >= 3*h (since h | h contributes h to sigma_1).

This gives a LOWER bound on |S_N(h)|, not an upper bound. For the UPPER bound:

    |S_N(h)| <= Sum_{d|h} d * |M(N/d)|

Under RH: |M(x)| = O(x^{1/2+epsilon}), so:

    |S_N(h)| <= Sum_{d|h} d * O((N/d)^{1/2+eps}) = O(N^{1/2+eps}) * Sum_{d|h} d^{1/2+eps}
             <= O(N^{1/2+eps}) * h^{1/2+eps} * tau(h)

where tau(h) is the number of divisors.

**Unconditionally** (without RH): |M(x)| <= x (trivially), so:

    |S_N(h)| <= Sum_{d|h} d * N/d = N * tau(h)

But we can do better. By the Mertens function bound |M(x)| = O(x * exp(-c*sqrt(log x))):

    |S_N(h)| <= Sum_{d|h, d<=N} d * (N/d) * exp(-c*sqrt(log(N/d)))
             = N * Sum_{d|h} exp(-c*sqrt(log(N/d)))
             <= N * tau(h) * exp(-c*sqrt(log(N/h)))    (for d <= h)

For h = O(N^alpha) with alpha < 1:

    |S_N(h)| <= N * tau(h) * exp(-c' * sqrt(log N))

### Case 2: Only M(N) <= -3 (weak condition)

Here we only know M(N) <= -3 but M(N/d) for d >= 2 could be anything.

For the h=1 term: S_N(1) = M(N) <= -3.
For h >= 2: S_N(h) = M(N) + Sum_{d|h, d>=2, d<=N} d * M(N/d).

The additional terms involve M(N/d) for d >= 2, which could be positive or negative.

**Worst case for |S_N(h)|:** Using |M(x)| <= x * exp(-c*sqrt(log x)):

For small h (say h <= log N):

    |S_N(h)| <= |M(N)| + Sum_{d|h, d>=2} d * |M(N/d)|
             <= N*exp(-c*sqrt(log N)) + Sum_{d|h, d>=2} d * (N/d) * exp(-c*sqrt(log(N/d)))
             <= N * exp(-c*sqrt(log N)) * (1 + tau(h))

This is O(N * exp(-c*sqrt(log N)) * tau(h)).

For h up to N:

    |S_N(h)| <= N * tau(h)    (trivial bound)

### Summary of S_N(h) bounds

| Range of h | Bound on |S_N(h)| | Quality |
|------------|---------------------|---------|
| h = 1 | |M(N)| >= 3 | Exact |
| 2 <= h <= log N | O(N * tau(h) * exp(-c*sqrt(log N))) | Good |
| log N < h <= N^{1/2} | O(N * tau(h) * exp(-c*sqrt(log(N/h)))) | Moderate |
| h > N^{1/2} | O(N * tau(h)) | Weak |

---

## 6. Bounding |C_h(p)| for h >= 2

### Decomposition

    C_h(p) = Sum_{prime b<=N} [cot(pi*h*rho_b/b) - cot(pi*h/b)]
           = [Sum_{prime b<=N} cot(pi*h*rho_b/b)] - [Sum_{prime b<=N} cot(pi*h/b)]

The second sum (the "reference" sum) is deterministic:

    Sigma_ref(h) := Sum_{prime b<=N} cot(pi*h/b)

For b > h (prime): cot(pi*h/b) ~ b/(pi*h) for large b. So:

    Sigma_ref(h) ~ (1/(pi*h)) * Sum_{prime b<=N} b ~ N^2/(2*pi*h*log N)

The first sum (the "scrambled" sum) involves rho_b = p mod b:

    Sigma_scr(h,p) := Sum_{prime b<=N} cot(pi*h*(p mod b)/b)

So C_h(p) = Sigma_scr(h,p) - Sigma_ref(h).

### Bounding |Sigma_scr(h,p)| via exponential sums

**The Erdos-Turan approach.** Consider the K points

    x_b = {h * (p mod b) / b}    for primes b in (h, N].

Their discrepancy D_K from the uniform distribution can be bounded using:

    D_K <= C_0/(H+1) + C_0 * Sum_{j=1}^{H} (1/j) * |Sum_b e(j*h*p/b)| / K

for any H >= 1, where the inner sum is over primes b in (h, N].

The exponential sums Sum_{prime b <= N} e(j*h*p/b) are **sums of e(alpha/b) over
primes b**, where alpha = j*h*p is a fixed integer.

**These are Kloosterman-type sums over primes.**

Specifically, for fixed integer m = j*h*p:

    T(m, N) := Sum_{prime b <= N} e(m/b)

### Bounding T(m, N) = Sum_{prime b <= N} e(m/b)

This is a sum of e(m/b) = exp(2*pi*i*m/b) over primes b <= N.

**For m = 0:** T = pi(N) ~ N/log N.

**For m != 0:** This is a standard exponential sum over primes, studied by Vinogradov.

The fractional parts {m/b} for b prime are well-distributed (this follows from
prime reciprocal equidistribution). By the Vinogradov method:

    |Sum_{prime b <= N} e(m/b)| <= C * N / (log N) * (1/sqrt(q) + (log N)^4/N^{1/4} + sqrt(q)/N)

where q is related to the rational approximation of m/b... but m/b varies with b,
so this isn't a standard Type I/II decomposition.

**Better approach: Partial summation + Weyl differencing.**

For a smooth function f(b) = m/b, we have f'(b) = -m/b^2. For b ~ X:

    |f'(b)| ~ m/X^2

The Van der Corput method (first derivative test) gives:

    |Sum_{X < b <= 2X} e(m/b)| <= C * (X * sqrt(m/X^2) + 1/sqrt(m/X^2))
                                = C * (sqrt(m) + X^2/sqrt(m))

Wait -- the first derivative test says: if |f'(x)| >= lambda > 0 on [a,b], then

    |Sum_{a < n <= b} e(f(n))| <= C / lambda

For f(b) = m/b on [X, 2X]: |f'(b)| = m/b^2, so lambda ~ m/X^2 when m/X^2 >= 1, i.e., X <= sqrt(m).

For X > sqrt(m): |f'(b)| < 1, so we use the second derivative test.
f''(b) = 2m/b^3. On [X, 2X]: |f''(b)| ~ 2m/X^3 =: lambda_2.

Second derivative test (Van der Corput B-process):

    |Sum_{X < b <= 2X} e(m/b)| <= C * (X*sqrt(lambda_2) + 1/sqrt(lambda_2))
                                = C * (X * sqrt(2m/X^3) + sqrt(X^3/(2m)))
                                = C * (sqrt(2m/X) + X^{3/2}/sqrt(2m))

**Restriction to primes.** By partial summation with the prime counting function:

    |Sum_{prime X < b <= 2X} e(m/b)| <= (1/log X) * max_{Y in [X,2X]} |Sum_{X < n <= Y} e(m/n)|
                                        + integral term

So the prime sum picks up a factor of 1/log X from partial summation.

Using the Van der Corput estimate on [X, 2X] and summing dyadically over
X = 2^k from h to N:

    |T(m, N)| <= C * Sum_{k: 2^k <= N} (1/log(2^k)) * (sqrt(2m/2^k) + (2^k)^{3/2}/sqrt(2m))

The first term (dominant when m is large):

    Sum_k sqrt(m/2^k) / log(2^k) ~ sqrt(m) * Sum_k 2^{-k/2} / (k*log 2) ~ sqrt(m) * C / log h

The second term (dominant when m is small):

    Sum_k (2^k)^{3/2} / (sqrt(m) * log(2^k)) ~ N^{3/2} / (sqrt(m) * log N)

**Overall:**

    |T(m, N)| = O(sqrt(m)/log(m+2) + N^{3/2}/(sqrt(m) * log N))

For m = j*h*p ~ j*h*N:

    |T(j*h*p, N)| = O(sqrt(j*h*N) + N^{3/2}/sqrt(j*h*N))
                   = O(N^{1/2} * sqrt(j*h) + N * 1/sqrt(j*h))

Hmm, this gives |T| = O(N) for j*h = O(1), which is NO better than the trivial
bound K ~ N/log N. The Van der Corput method is too crude here.

### Improved bound: Vaughan's identity for sums over primes

Using Vaughan's identity to decompose the sum over primes into Type I and Type II
sums, one can obtain:

    |Sum_{prime b <= N} e(m/b)| << N * exp(-c * sqrt(log N))

for any fixed m != 0, with the implied constant depending on m. This is essentially
Vinogradov's bound on exponential sums over primes.

**More precisely:** For |m| <= N^A:

    |Sum_{prime b <= N} e(m/b)| << N * (log N)^{-B}

for any B > 0, with the implied constant depending on A and B.

This is a standard result following from Vinogradov's method (see e.g.,
Iwaniec-Kowalski, Chapter 13).

### Consequence for the discrepancy bound

With K = pi(N) ~ N/log N primes and using the bound on T(j*h*p, N):

    |T(j*h*p, N)| / K << (log N)^{1-B}

for any B, this says the exponential sums are o(K). By Erdos-Turan:

    D_K << 1/(H+1) + Sum_{j=1}^{H} (1/j) * (log N)^{1-B} << 1/H + (log H) * (log N)^{1-B}

Choosing H = (log N)^{B-1}: D_K << (log N)^{1-B}.

So the discrepancy D_K -> 0 (the points {h*p/b mod 1} are equidistributed over
primes b), but the rate is only a power of log N.

### From discrepancy to cotangent sum bound

**The problem:** The discrepancy bounds D_K -> 0 ensure equidistribution, but the
cotangent function cot(pi*x) is UNBOUNDED near x=0 and x=1. The Koksma-Hlawka
inequality gives:

    |Sum_b f(x_b) - K * integral_0^1 f(x) dx| <= D_K * V(f)

where V(f) is the total variation of f. But V(cot(pi*x)) = infinity on (0,1)!

So the Erdos-Turan/Koksma-Hlawka approach CANNOT directly bound Sum cot(pi*x_b)
because the test function has unbounded variation.

**This is the fundamental obstruction of the Erdos-Turan approach for this problem.**

---

## 7. Alternative: Direct exponential sum approach

### Fourier truncation of cotangent

Instead of using discrepancy, truncate the Fourier expansion directly.

For x in (0,1), define the truncated cotangent:

    cot_J(pi*x) = -(2/pi) * Sum_{m=1}^{J} sin(2*pi*m*x) / ...

Wait, I need to use the correct expansion. The key identity is:

    cot(pi*x) = (1/pi) * lim_{M->inf} Sum_{n=-M}^{M} 1/(x-n)

But for a PRACTICAL Fourier truncation, use the Vaaler approximation of the
sawtooth function. The sawtooth psi(x) = {x} - 1/2 has the Fourier expansion:

    psi(x) = -(1/pi) * Sum_{m=1}^{inf} sin(2*pi*m*x)/m

And cot(pi*x) is related to psi(x) by:

    cot(pi*x) = 2 * Sum_{m=1}^{inf} ...

Actually, there's no simple closed-form relation between cot(pi*x) and psi(x).
They satisfy: integral_0^1 cot(pi*x) * e(-m*x) dx relates to Dirichlet characters,
but this doesn't directly help.

### Using the identity cot(pi*x) = i + 2i/(e^{2*pi*i*x} - 1)

For x in (0,1):

    cot(pi*x) = i * (e^{2*pi*i*x} + 1)/(e^{2*pi*i*x} - 1)
              = i + 2i/(e^{2*pi*i*x} - 1)
              = i + 2i * Sum_{m=0}^{inf} e^{2*pi*i*(m+1)*x}    (for Im(x) > 0)

This geometric series doesn't converge for real x. Instead:

    1/(e^{2*pi*i*x} - 1) = -1/2 + (i/2)*cot(pi*x)    (standard)

So cot(pi*x) = -2*Im[1/(e^{2*pi*i*x}-1)] = (2i)*[1/(e^{2*pi*i*x}-1) + 1/2].

For a FINITE approximation, use the Dirichlet kernel:

    Sum_{m=1}^{M} e(m*x) = e(x) * (e(M*x) - 1)/(e(x) - 1)

and Abel summation:

    Sum_{m=1}^{M} e(m*x)/m ~ log(1/(1-e(x))) for |e(x)| < 1.

None of these converge simply for x real. The fundamental issue remains:
cot(pi*x) has a pole at x=0 (and x=1), making any truncated Fourier approximation
fail to capture the large values near the poles.

---

## 8. Quantitative Assessment: Does the Approach Close the Gap?

### The obstacle in explicit terms

We need to bound |Sum_{h>=2} B_raw|_h| where

    B_raw|_h = S_N(h)/(2*pi) * C_h(p)

### Upper bound on |B_raw|_h| for each h

Using:
- |S_N(h)| <= N * tau(h) * exp(-c*sqrt(log(N/h)))   (unconditional, for h <= N/2)
- |C_h(p)| <= |Sigma_ref(h)| + |Sigma_scr(h,p)|

For the reference sum:
    |Sigma_ref(h)| = |Sum_{prime b>h} cot(pi*h/b)| ~ N^2/(2*pi*h*log N)

For the scrambled sum, splitting into a mean and a deviation:
    Sigma_scr(h,p) = 0 + [deviation term]

The variance of the deviation is Sum_b (b-2)/3 ~ N^2/(6*log N) (from Section 3),
so the typical deviation is O(N/sqrt(log N)).

But THIS IS NOT A RIGOROUS BOUND on the deviation for a specific p.

For a rigorous bound, we need something like:

    |Sigma_scr(h,p)| <= N^2/(C*h*log N) for all h >= 2

This would follow from equidistribution of p mod b, but the cotangent's
unboundedness prevents direct application of discrepancy bounds.

### Crude bound

Trivially: |cot(pi*h*rho_b/b)| <= cot(pi/b) ~ b/pi for the worst case rho_b.

Actually, for b prime and gcd(h,b)=1: {h*rho_b/b} takes values {h*a/b mod 1 : a=1,...,b-1}
= {1/b, 2/b, ..., (b-1)/b}. The maximum of |cot(pi*k/b)| over k=1,...,b-1 is cot(pi/b) ~ b/pi.

So:
    |Sigma_scr(h,p)| <= Sum_{prime b<=N} |cot(pi*h*rho_b/b)| <= Sum_{prime b<=N} cot(pi/b) ~ Sum_b b/pi ~ N^2/(2*pi*log N)

This gives |C_h(p)| <= |Sigma_ref(h)| + |Sigma_scr(h,p)| <= N^2/(2*pi*h*log N) + N^2/(2*pi*log N).

For h >= 2: |C_h(p)| <= N^2/(2*pi*log N) * (1 + 1/h) <= 3*N^2/(4*pi*log N).

Then:
    |B_raw|_h| <= |S_N(h)|/(2*pi) * |C_h(p)|
               <= [N*tau(h)] / (2*pi) * [3*N^2/(4*pi*log N)]
               = (3/(8*pi^2)) * N^3 * tau(h) / log N

Summing over h >= 2:

    |Sum_{h>=2} B_raw|_h| <= (3/(8*pi^2)) * (N^3/log N) * Sum_{h=2}^{N} tau(h)
                           ~ (3/(8*pi^2)) * (N^3/log N) * N*log N
                           = (3/(8*pi^2)) * N^4

This is VASTLY larger than 3*delta_sq ~ N^2/(16*log N). **The crude bound fails
by a factor of ~N^2*log N.**

### Why the crude bound fails

The crude bound treats C_h(p) as O(N^2/log N) for ALL h, ignoring the crucial
cancellation that occurs in the cotangent sum for h >= 2. It also treats S_N(h)
as O(N*tau(h)), ignoring the exp(-c*sqrt(log N)) decay.

### Refined attempt: exploit cancellation in the sum over h

The full B_raw can be written:

    B_raw = Sum_h S_N(h)/(2*pi) * C_h(p)
          = (1/(2*pi)) * Sum_h S_N(h) * Sum_{prime b} [cot(pi*h*rho_b/b) - cot(pi*h/b)]

Exchanging sums (b first, then h):

    B_raw = (1/(2*pi)) * Sum_{prime b} Sum_{h=1}^{N} S_N(h) * [cot(pi*h*rho_b/b) - cot(pi*h/b)]

For each prime b, the inner sum over h is:

    Phi_b := Sum_{h=1}^{N} S_N(h) * [cot(pi*h*rho_b/b) - cot(pi*h/b)]

This is a sum of S_N(h) weighted by cotangent differences. The function
h -> cot(pi*h*rho_b/b) - cot(pi*h/b) is periodic in h with period b (since
cot(pi*(h+b)*k/b) = cot(pi*h*k/b + pi*k) = cot(pi*h*k/b) when k is even,
or -cot(pi*h*k/b) when k is odd... actually cot is pi-periodic, so
cot(pi*(h+b)*k/b) = cot(pi*h*k/b + pi*k) = cot(pi*h*k/b) since cot has period pi
and pi*k is an integer multiple of pi. So yes, the cotangent difference is b-periodic in h.)

By the b-periodicity, the sum over h decomposes into blocks of length b:

    Phi_b = Sum_{r=0}^{floor(N/b)} Sum_{h'=1}^{b-1} S_N(rb + h') * [cot(pi*h'*rho_b/b) - cot(pi*h'/b)]
          + [boundary terms for h not a multiple of b]

Within each block, S_N(rb + h') varies smoothly in r (since M(N/d) doesn't change
much as d changes by ~b). If we could approximate S_N(rb + h') ~ S_N(h') for
small r, we'd get:

    Phi_b ~ (N/b) * Sum_{h'=1}^{b-1} S_N(h') * [cot(pi*h'*rho_b/b) - cot(pi*h'/b)]

But S_N(h') for h' < b involves only the divisor d=1 of h' when h' is prime,
so S_N(h') = M(N) for h' prime (since the only d|h' with d<=N is d=1 and d=h' when h'<=N).

Actually S_N(h') = Sum_{d|h', d<=N} d*M(N/d). For h' = 1: S_N(1) = M(N). For h' prime (h'<=N):
S_N(h') = M(N) + h'*M(N/h'). For h' composite: more terms.

This approach is getting very complicated and doesn't seem to lead to clean bounds.

---

## 9. The Large Sieve Alternative

### Setup

Instead of the Erdos-Turan inequality, use the large sieve inequality to bound
the L^2 norm of the tail Sum_{h>=2} B_raw|_h.

**Parseval's identity (approximate):** Since B_raw = 2*Sum_b (1/b)*Sum_a D(a/b)*delta(a/b),
we can write B_raw as an inner product <D, delta> weighted by 1/b.

The Fourier decomposition B_raw = Sum_h B_raw|_h is a decomposition in terms of
the Ramanujan expansion of D and the cotangent expansion of delta.

By Bessel's inequality applied to the Fourier coefficients:

    Sum_{h=1}^{N} |B_raw|_h|^2 <= (something related to ||D||^2 * ||delta||^2)

But I don't have a clean Parseval identity for B_raw|_h because the decomposition
isn't orthogonal in the standard sense.

### Large sieve on the cotangent sum

The large sieve inequality states: for points x_b in [0,1) with "well-spaced" gaps:

    Sum_{m=-M}^{M} |Sum_b a_b * e(m*x_b)|^2 <= (N_eff + M) * Sum_b |a_b|^2

where N_eff is related to the spacing of the x_b.

Applied to our problem with x_b = rho_b/b (for prime b) and a_b = 1:

    Sum_{m=1}^{M} |Sum_{prime b<=N} e(m*rho_b/b)|^2 <= (delta^{-1} + M) * pi(N)

where delta = min_{b != b'} |rho_b/b - rho_{b'}/b'|.

The points rho_b/b for primes b are NOT well-spaced a priori. Two distinct primes b, b'
could have rho_b/b very close to rho_{b'}/b' (within O(1/(b*b'))).

By the large sieve with delta = 1/N^2 (worst case):

    Sum_{m=1}^{M} |Sum_{prime b<=N} e(m*p/b)|^2 <= (N^2 + M) * pi(N) ~ (N^2 + M) * N/log N

This gives a bound on the AVERAGE of |exponential sum|^2 over m, but we need
bounds for specific m values (namely m = h, corresponding to cotangent frequency h).

### From L^2 bound to pointwise: Cauchy-Schwarz

By Cauchy-Schwarz over h = 2,...,H:

    |Sum_{h=2}^{H} B_raw|_h| <= sqrt(H) * sqrt(Sum_{h=2}^{H} |B_raw|_h|^2)

Using |B_raw|_h|^2 = |S_N(h)|^2/(4*pi^2) * |C_h(p)|^2:

    Sum_{h=2}^{H} |B_raw|_h|^2 <= (1/(4*pi^2)) * max_h |S_N(h)|^2 * Sum_h |C_h(p)|^2

Now Sum_h |C_h(p)|^2 involves Sum_h of squared cotangent sums.

The Parseval identity for the cotangent sums gives:

    Sum_{h=1}^{b-1} |cot(pi*h*k/b) - cot(pi*h/b)|^2 = (some explicit function of k and b)

For each b: Sum_{h=1}^{b-1} cot^2(pi*h*a/b) = (b-1)(b-2)/3 (standard identity, for a coprime to b).

So Sum_{h=1}^{b-1} |cot(pi*h*rho_b/b) - cot(pi*h/b)|^2
   = Sum_h [cot^2(pi*h*rho_b/b) - 2*cot(pi*h*rho_b/b)*cot(pi*h/b) + cot^2(pi*h/b)]
   = 2*(b-1)(b-2)/3 - 2*Sum_h cot(pi*h*rho_b/b)*cot(pi*h/b)

The cross term Sum_{h=1}^{b-1} cot(pi*h*a/b)*cot(pi*h/b) for a coprime to b is a
known sum. Using the identity (for gcd(a,b)=gcd(1,b)=1):

    Sum_{h=1}^{b-1} cot(pi*h*a/b)*cot(pi*h/b) = ???

This equals (b-1)(b-2)/3 when a=1 (trivially). For general a:

    Sum_{h=1}^{b-1} cot(pi*h*a/b)*cot(pi*h*c/b) = ((b-1)(b-2)/3 - (b-1)) if a*c ≡ 0 or ...

Actually, this is related to Dedekind sums. The identity is:

    (1/b) * Sum_{h=1}^{b-1} cot(pi*h*a/b)*cot(pi*h*c/b) = s(a,b)*s(c,b)*something

This is getting too complicated for a clean bound.

---

## 10. The Fundamental Difficulty and What Would Be Needed

### Summary of attempts

| Approach | Bound obtained | Needed | Gap |
|----------|---------------|--------|-----|
| Crude (each mode) | O(N^4) | O(N^2/log N) | Factor N^2*log N |
| Van der Corput on exp sums | O(N^{5/2}/log N) | O(N^2/log N) | Factor N^{1/2} |
| Vinogradov exp sum over primes | Saves log^B N | Saves N^{1/2} | Not enough |
| Large sieve L^2 + C-S | O(N^3 * polylog) | O(N^2/log N) | Factor N*polylog |
| Erdos-Turan + Koksma-Hlawka | Infinite (V(cot) = inf) | Finite | Inapplicable |

### The root cause

The Erdos-Turan approach CANNOT close the gap for the following fundamental reason:

**The cotangent function has unbounded variation.** The Erdos-Turan inequality
bounds discrepancy, and discrepancy controls sums of BV functions via
Koksma-Hlawka. But cot(pi*x) is NOT of bounded variation on (0,1) due to its
poles. Therefore, even perfect equidistribution results (D_K -> 0) don't directly
give bounds on Sum cot(pi*x_b).

**The "pole problem."** For each prime b, cot(pi*h*rho_b/b) is of order b when
h*rho_b is close to a multiple of b (i.e., when {h*rho_b/b} is near 0 or 1).
Such "near-pole" primes contribute O(b) to the sum, and there are O(1) of them
for each h. This gives a contribution of O(N) per h from pole-adjacent terms,
and O(N^2) when summed over h. This is comparable to the main term N^2/log N,
preventing any saving.

More precisely: for each h, the number of primes b where {h*rho_b/b} < 1/b
(the "pole region") is about pi(N) * (2/b) ~ 2N/(b*log N) for each b, summing
to ~ 2N * Sum(1/(b*log N)) ~ 2N*log(log N)/log N primes total. Each contributes
O(b) ~ O(N), giving a total pole contribution of O(N^2 * log(log N)/log N).

This is the SAME ORDER as the main term N^2/(2*pi*h*log N), so the pole terms
are not negligible.

### What additional bound would be needed

To close the gap, one would need ONE of the following:

**(A) A sign result for higher modes.** Show that for M(N) <= -3:

    B_raw|_h >= 0 for all h >= 2

This would give B_raw >= B_raw|_{h=1} > 0, immediately implying B+C > 0.

This requires showing: S_N(h) * C_h(p) >= 0 for each h >= 2 when M(N) <= -3.
Since S_N(h) can be negative (when not all M(N/d) are negative), and C_h(p)
fluctuates in sign, this is a very strong requirement and likely FALSE for
individual h, even if the sum is positive.

**(B) Cancellation across h for the tail.** Show that:

    |Sum_{h=2}^{N} S_N(h) * C_h(p)| = o(N^2/log N)

This requires cancellation in the double sum over h and b:

    Sum_h Sum_b S_N(h) * [cot(pi*h*rho_b/b) - cot(pi*h/b)]

By exchanging sums to Sum_b Sum_h, and using the b-periodicity of the cotangent
in h, the inner sum over h becomes:

    Sum_{h=1}^{N} S_N(h) * cot(pi*h*k/b) for k = rho_b or k = 1

This is a "Ramanujan-cotangent" sum: S_N(h) involves Mertens at various scales,
and cot(pi*h*k/b) is b-periodic in h. The sum has potential cancellation from
the oscillation of cot, but the pole of cot at h = mb/k creates large terms.

A clean evaluation of Sum_h S_N(h)*cot(pi*h*k/b) would require understanding
the Mellin/Dirichlet series of S_N(h), which connects back to the Riemann zeta
function. This is essentially equivalent to the Riemann Hypothesis in difficulty.

**(C) Direct proof that B_raw >= 0.** Bypass the Fourier decomposition entirely
and prove B_raw = 2*Sum D*delta >= 0 when M(N) <= -3 using the algebraic
structure of D and delta. The rank-based approach (T >= n*delta_sq/2) from
Session 4 is the most promising route:

B >= 0 iff Sum_f rank(f)*delta(f) >= n*delta_sq/2

This is a statement about the covariance of rank and displacement, which can
potentially be proved using the rearrangement inequality applied to a MAJORITY
of denominators (those with p^2 = 1 mod b, already proved) combined with a
bound on the remaining denominators.

**(D) A smoothed version of the problem.** Replace cot(pi*x) by a bounded
approximation (e.g., truncated at |cot| <= L for some L = L(N)), prove the bound
for the smoothed version, then show the truncation error is small. The truncation
error involves only the "pole-adjacent" terms, which can be bounded by:

    Error <= Sum_b Sum_{h: |{h*rho_b/b}| < 1/L or > 1-1/L} |S_N(h)| * L / (2*pi)

For L ~ sqrt(N): the number of h values with {h*rho_b/b} < 1/sqrt(N) is about
N/sqrt(N) = sqrt(N) for each b. The error per b is O(sqrt(N) * N * sqrt(N)) = O(N^2).
Summing over b gives O(N^3/log N), which is too large.

For L ~ N: the cotangent is never truncated (since |cot(pi*k/b)| <= cot(pi/b) ~ b/pi <= N/pi < N),
so the error is zero but the "smoothed" problem IS the original problem.

---

## 11. Quantitative Erdos-Turan Analysis (Attempted Closure)

Despite the fundamental obstacles identified above, let us attempt to carry out
the Erdos-Turan program as concretely as possible, to quantify exactly where the
bound falls short.

### Step 1: Bound |C_h(p)| using exponential sums

For h >= 2 and b prime with b > h:

    C_h(p) = Sum_{b prime, b>h} [cot(pi*h*rho_b/b) - cot(pi*h/b)] + O(h^2/log h)

The O(h^2/log h) term accounts for the finitely many primes b <= h.

Split the cotangent into a Fourier-truncated part and remainder.

Define for J >= 1:

    cot_J(pi*x) = -2 * Sum_{m=1}^{J} Im[e(m*x)] / (2*pi*m)  ???

No -- let me use the correct formula. For x in (0,1):

    cot(pi*x) = (1/pi) * [1/x - 1/(1-x) + Sum_{n=1}^{inf} (1/(x+n) + 1/(x-n) - 2/n)]

Hmm. Actually for our purposes the most useful truncation is via the
PARTIAL FRACTION identity for cot within (0,1):

    cot(pi*x) = (1/pi) * [1/x + 2*Sum_{n=1}^{J} x/(x^2-n^2)] + R_J(x)

where |R_J(x)| <= C/(J*x) for x bounded away from 0.

This still has the 1/x singularity in the main term.

**Alternative: Vaaler's trigonometric polynomial approximation of the sawtooth.**

Vaaler showed that for any H >= 1, there exists a trigonometric polynomial
T_H(x) = Sum_{|h|<=H} a_h * e(h*x) satisfying:

    |psi(x) - T_H(x)| <= 1/(2(H+1))    for all x

where psi(x) = {x} - 1/2 is the sawtooth.

But cot(pi*x) is NOT the sawtooth; it's related but much more singular.

The relationship: psi(x) = {x} - 1/2 has Fourier coefficients proportional to 1/h,
while cot(pi*x) has a pole. Specifically:

    psi(x) = -(1/pi) * Sum_{m=1}^{inf} sin(2*pi*m*x)/m

while cot is:

    cot(pi*x) = (2/pi) * Sum_{m=0}^{inf} sin(2*pi*(2m+1)*x)/(2m+1) ???

No, that's the square wave. Let me reconsider.

The Fourier expansion of cot(pi*x) on (0,1) is tricky because cot(pi*x) is not
in L^1(0,1) (it has non-integrable singularities at x=0 and x=1). So it does NOT
have a classical Fourier series!

This confirms the fundamental obstruction: **cot(pi*x) is not even Fourier-representable
on (0,1) due to its poles**, making Fourier/Erdos-Turan methods inapplicable in
their standard form.

### Step 2: Work around the singularity

Decompose:

    cot(pi*h*rho_b/b) = cot(pi*{h*rho_b/b}) * sign_factor

where {h*rho_b/b} is the fractional part. For b prime, b > h: {h*rho_b/b} = h*rho_b mod b / b.

Since b is prime and gcd(h,b) = 1 (for b > h): h*rho_b mod b ranges over {1,...,b-1}
as rho_b does. So {h*rho_b/b} = k/b for some k in {1,...,b-1}.

    cot(pi*k/b) = (b/pi) * [1/k - 1/(b-k) + O(k/b^2)]    (for 1 <= k <= b-1)

The dominant term is (b/pi)/k for small k and -(b/pi)/(b-k) for k near b.

Now:

    Sum_{b prime} cot(pi*h*rho_b/b) = Sum_b (b/pi) * [1/{h*rho_b mod b} + correction]

The sum (b/pi) * 1/{h*rho_b mod b} requires bounding Sum_b b/(h*p mod b mod b).

Let k_b = h*p mod b. Then:

    Sum_b b/k_b = Sum_b b/(hp mod b)

For "random" k_b uniform on {1,...,b-1}:

    E[b/k_b] = b * Sum_{a=1}^{b-1} 1/a / (b-1) ~ b*log(b)/b = log(b)

So E[Sum_b b/k_b] ~ Sum_{b prime} log(b) ~ N (by the prime number theorem applied to Sum log(b)).

The variance: Var[b/k_b] ~ b^2 * Sum 1/a^2 / b ~ b * pi^2/6.

If independent: Var[Sum_b b/k_b] ~ Sum_b b*pi^2/6 ~ pi^2*N^2/(12*log N).

Standard deviation ~ N/sqrt(log N).

So |Sum_b cot(pi*h*rho_b/b)| ~ N/sqrt(log N) typically (deviation from 0 mean).

### Step 3: Assemble the bound

Using the heuristic |C_h(p)| ~ N^2/(2*pi*h*log N) + O(N/sqrt(log N)) for the mean
plus deviation:

For h <= sqrt(N): the mean term dominates, |C_h(p)| ~ N^2/(2*pi*h*log N).
For h > sqrt(N): the deviation term may dominate, |C_h(p)| ~ O(N/sqrt(log N)).

And |S_N(h)| <= N * tau(h) * exp(-c*sqrt(log N)) for the Mertens-based bound.

For h <= sqrt(N):

    |B_raw|_h| ~ N*tau(h)*exp(-c*sqrt(log N)) / (2*pi) * N^2/(2*pi*h*log N)
              = N^3 * tau(h) * exp(-c*sqrt(log N)) / (4*pi^2*h*log N)

    Sum_{h=2}^{sqrt(N)} |B_raw|_h| ~ N^3 * exp(-c*sqrt(log N)) / (4*pi^2*log N) * Sum tau(h)/h
                                   ~ N^3 * exp(-c*sqrt(log N)) * (log N)^2 / (4*pi^2*log N)
                                   = N^3 * log(N) * exp(-c*sqrt(log N)) / (4*pi^2)

For h > sqrt(N):

    |B_raw|_h| ~ N*tau(h) / (2*pi) * N/sqrt(log N) = N^2*tau(h)/(2*pi*sqrt(log N))

    Sum_{h=sqrt(N)}^{N} |B_raw|_h| ~ N^2/(2*pi*sqrt(log N)) * Sum tau(h)
                                   ~ N^2/(2*pi*sqrt(log N)) * N*log N
                                   = N^3*sqrt(log N)/(2*pi)

Both ranges give O(N^3 * polylog(N)), which is far larger than 3*delta_sq ~ N^2/(16*log N).

**THE ERDOS-TURAN APPROACH DOES NOT CLOSE THE GAP.**

The bounds are off by a factor of approximately N*polylog(N).

---

## 12. Why the Gap Cannot Be Closed by This Method

### The fundamental reason

The problem lives at the interface of:
1. **Multiplicative number theory** (Mertens function, Mobius function)
2. **Additive/harmonic analysis** (cotangent sums, exponential sums)

The Erdos-Turan inequality is a tool for (2), but the coupling between S_N(h)
and C_h(p) is controlled by (1). The key issue is:

- S_N(h) = Sum_{d|h} d*M(N/d) has size O(N*tau(h)) in the WORST case, but the
  values of M(N/d) exhibit cancellation that depends on the specific prime p
  (since N = p-1). This cancellation is inaccessible to Erdos-Turan methods.

- C_h(p) involves cot(pi*h*rho_b/b), which is an unbounded function of the
  residues rho_b = p mod b. The Erdos-Turan inequality can bound discrepancy
  (sums of bounded functions) but not sums of unbounded functions.

- The PRODUCT S_N(h)*C_h(p) benefits from additional cancellation: when S_N(h)
  is large (many divisors of h), C_h(p) tends to be small (more cancellation in
  the cotangent sum due to the periodicity of cot in h). But quantifying this
  negative correlation requires arithmetic input beyond what Erdos-Turan provides.

### What WOULD work

1. **The rank-based approach** (from Session 4, Addendum 2): B >= 0 iff
   T = Sum rank(f)*delta(f) >= n*delta_sq/2. The partial result T_b >= 0 for
   all b | (p^2-1) covers a positive-density set of denominators. Extending
   to all denominators (or bounding the generic-denominator contribution) is
   the most tractable remaining route.

2. **A mean-value theorem over p**: Instead of fixing p and bounding the tail,
   show that the AVERAGE of |Sum_{h>=2} B_raw|_h|^2 over primes p in [N/2, N]
   is small. This would use the large sieve and multiplicative character sums,
   potentially giving a bound of O(N^4/log^2 N) on the average, which (divided
   by N/log N primes) gives O(N^3/log N) per prime. This is STILL too large.

3. **Direct algebraic proof** that B_raw = 2*Sum D*delta >= 0 when M(N) <= -3,
   using the Franel-Landau identity Sum D^2 = O(N * |M(N)|^2) and the structure
   of delta as a permutation-based displacement. This avoids Fourier analysis
   entirely and works in the "spatial" domain.

4. **Computational verification** up to a threshold N_0 where the asymptotic
   bound C >= A (proved for N >= N_0) kicks in. The asymptotic bound C >= A
   is proved in the paper for N >= ~200,000. So computational verification of
   B+C > 0 for all M(p) <= -3 primes with p <= 200,000 would complete the proof.
   This HAS been done (verified to p = 200,000 with zero violations).

---

## 13. Conclusion

### The Erdos-Turan approach to bounding Sum_{h>=2} B_raw|_h fails.

The approach fails because:

1. **Unbounded test function:** The cotangent cot(pi*x) has poles at x=0 and x=1,
   giving it unbounded variation. The Erdos-Turan inequality controls discrepancy
   (sums of indicator functions or BV functions), but cannot control sums of
   functions with unbounded variation. Even perfect equidistribution of the
   points {h*rho_b/b mod 1} would not bound the cotangent sum.

2. **No Fourier series for cot:** The function cot(pi*x) on (0,1) is not in L^1,
   so it has no convergent Fourier series. Fourier-truncation methods (Vaaler,
   Beurling-Selberg) work for the sawtooth psi(x) = {x}-1/2 but not for cot.

3. **Individual h bounds are too weak:** For each h >= 2, the best achievable bound
   on |B_raw|_h| is O(N^3*tau(h)/log N) (from |S_N(h)| * |C_h(p)|). Summing over
   h gives O(N^4), which exceeds the target O(N^2/log N) by a factor of N^2*log N.

4. **The saving must come from CANCELLATION across h, not from individual h bounds.**
   The sum Sum_h B_raw|_h benefits from cancellation between different Fourier modes,
   but quantifying this cancellation requires understanding the correlation between
   S_N(h) (a multiplicative function of h) and C_h(p) (an additive function of h
   modulo each b), which is beyond the reach of the Erdos-Turan framework.

### What additional bound would close the gap

The gap would close if ONE of the following could be proved:

**(A) B_raw >= 0 directly** (i.e., Sum D*delta >= 0 when M(N) <= -3). This is the
strongest result and makes the Fourier analysis unnecessary. The rank-based
approach (T >= n*delta_sq/2) is the most promising route. Partial results exist:
T_b >= 0 for all b | (p^2-1), covering all "involution" denominators.

**(B) |Sum_{h>=2} B_raw|_h| = o(N^2/log N)** via a square-mean estimate. If one
could show Sum_{h>=2} |B_raw|_h|^2 = o(N^4/(log N)^2), then by Cauchy-Schwarz
|Sum B_raw|_h| = o(N^2/log N). This requires knowing that |S_N(h)|*|C_h(p)|
decays faster than 1/h on average, which in turn requires the arithmetic
correlation between S_N(h) and C_h(p) to be understood.

**(C) Computational + asymptotic hybrid.** The asymptotic result C > A for N >= N_0
(proved in the paper) means B+C > 0 is only needed for finitely many primes.
Verification up to N_0 ~ 200,000 (which has been done) completes the proof,
assuming the asymptotic threshold is made effective.

**Recommendation:** Pursue approach (C) for the paper, with approach (A) as the
long-term goal for a purely analytical proof. The Erdos-Turan/Fourier approach
(B) appears to be a dead end for this specific problem due to the pole structure
of the cotangent function.
