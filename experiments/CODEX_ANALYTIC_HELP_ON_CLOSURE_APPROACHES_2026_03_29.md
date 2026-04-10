# Codex Analytic Help
## New progress on the closure approaches
## Date
2026-03-29

## Executive summary

Yes. I can now help concretely with two of the four closure routes:

- the **sampled `L^2`** route
- the **pair-correlation / pair-kernel** route

I do **not** currently have an honest proof of the `K`-bound

```text
|1 - D/A| <= K |M| / p
```

and I do not think I should pretend otherwise.

What I do have is:

1. an exact new Möbius-sawtooth expansion for the sampled error `E(k)`,
2. an exact Dedekind-sum kernel formula for `sum E(k)^2`,
3. an unconditional explicit lower bound

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 28
```

for every prime `p >= 11`.

I also get a stronger large-`p` variant:

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 9
```

for every prime `p >= 67`.

That lower bound is crude, but it is fully analytic and non-circular.

---

## 1. Setup

Let `p` be prime, `N = p-1`, `F_N` the Farey sequence of order `N`, and

```text
n = |F_N|.
```

For `1 <= k <= p-1`, define the sampled Farey counting error

```text
E(k) = #{f in F_N : f <= k/p} - n k/p.
```

This is the same object appearing in the new `p`-grid reformulation of Gap 2.

---

## 2. Exact Möbius-sawtooth expansion

Define the sawtooth on nonintegral arguments by

```text
beta(x) = 1/2 - {x}.
```

Then for every `1 <= k <= p-1`,

```text
E(k) = sum_{m=1}^{p-1} lambda_p(m) beta(mk/p),
```

where

```text
lambda_p(m) = M(floor((p-1)/m)) + 1_{m=1}.
```

### Proof sketch

Use the standard Farey counting identity

```text
#{f in F_N : f <= x}
 = 1 + sum_{d<=N} mu(d) sum_{m<=N/d} floor(mx).
```

At `x = k/p` with `1 <= k <= p-1`, no `mk/p` is an integer because `m < p`.
So

```text
floor(mk/p) = mk/p - {mk/p}.
```

Subtracting `n k/p` and rewriting `{y} = 1/2 - beta(y)` gives

```text
E(k) = beta(k/p) + sum_{d<=N} mu(d) sum_{m<=N/d} beta(mk/p).
```

Reindex by `m` to get the coefficient

```text
sum_{d<=N/m} mu(d) = M(floor(N/m)).
```

This is the exact expansion above.

### Why this matters

This turns the sampled-`L^2` problem into a **finite structured quadratic form**
with explicit Möbius coefficients. It is a much cleaner analytic entry point
than the older circular `D'/A'` language.

---

## 3. Exact endpoint identities

### Proposition 3.1

```text
E(1) = 1 - n/p.
```

### Proof

The only Farey fraction in `F_N` at or below `1/p` is `0`, because the
smallest positive element of `F_N` is `1/N = 1/(p-1) > 1/p`.

So

```text
#{f in F_N : f <= 1/p} = 1,
```

hence

```text
E(1) = 1 - n/p.
```

### Proposition 3.1b

For every odd prime `p`,

```text
E(2) = (p+1)/2 - 2n/p.
```

### Proof

The Farey fractions in `F_{p-1}` at or below `2/p` can only have numerator
`0` or `1`.

- If `a >= 3`, then

```text
a/b >= 3/(p-1) > 2/p.
```

- If `a = 2`, then

```text
2/b <= 2/p
```

would force `b >= p`, impossible because `b <= p-1`.

So the only positive fractions counted are `1/b` with `b >= p/2`, and there
are exactly `(p-1)/2` of them. Including `0`, we get

```text
#{f in F_N : f <= 2/p} = (p+1)/2,
```

hence

```text
E(2) = (p+1)/2 - 2n/p.
```

### Proposition 3.2

For every `1 <= k <= p-1`,

```text
E(p-k) = -E(k).
```

### Proof

No old Farey fraction equals `k/p`, since all old denominators are `< p`.
If

```text
A(k) = #{f in F_N : f <= k/p},
```

then Farey symmetry `f -> 1-f` gives

```text
A(p-k) = n - A(k).
```

Therefore

```text
E(p-k)
 = A(p-k) - n(p-k)/p
 = -(A(k) - nk/p)
 = -E(k).
```

### Corollary 3.3

```text
sum_{k=1}^{p-1} E(k)^2
 >= 2(1 - n/p)^2.
```

This is immediate from the contributions of `k=1` and `k=p-1`.

### Corollary 3.4

Whenever

```text
n >= p(p+1)/4,
```

we also have

```text
sum_{k=1}^{p-1} E(k)^2
 >= 2(1 - n/p)^2 + 2((p+1)/2 - 2n/p)^2.
```

This uses the additional contributions of `k=2` and `k=p-2`, together with
the fact that in that range `E(2) <= 0`, so a lower bound on `n` yields a
lower bound on `|E(2)|`.

---

## 4. A fully analytic lower bound for the sampled `L^2` term

### Theorem 4.1

For every prime `p >= 11`,

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 28.
```

### Proof

Let

```text
C_N = #{(a,b) in [1,N]^2 : gcd(a,b)=1}.
```

By symmetry,

```text
C_N = 2 sum_{m<=N} phi(m) - 1.
```

Now non-coprime pairs lie in the union over primes `q` of pairs divisible by
`q`. Hence by the union bound,

```text
N^2 - C_N
 <= sum_{q prime} floor(N/q)^2
 <= N^2 sum_{q prime} 1/q^2.
```

Also

```text
sum_{q prime} 1/q^2
 <= 1/4 + sum_{n odd, n>=3} 1/n^2
 = 1/4 + (pi^2/8 - 1)
 = pi^2/8 - 3/4.
```

Therefore

```text
C_N >= (7/4 - pi^2/8) N^2.
```

So

```text
sum_{m<=N} phi(m)
 >= (7/8 - pi^2/16) N^2 + 1/2.
```

Set

```text
kappa = 7/8 - pi^2/16 ≈ 0.2581497.
```

Then

```text
n = 1 + sum_{m<=N} phi(m) >= kappa N^2 + 3/2.
```

With `N = p-1`, Corollary 3.3 gives

```text
sum E(k)^2
 >= 2( n/p - 1 )^2
 >= 2( (kappa (p-1)^2 + 3/2)/p - 1 )^2.
```

Define

```text
g_28(p)
 = 2( (kappa (p-1)^2 + 3/2)/p - 1 )^2 - p^2/28.
```

A direct derivative check gives

```text
g_28'(p) > 0
```

for all `p >= 11`, so `g_28` is increasing on `[11, infinity)`.
At `p = 11`,

```text
g_28(11) > 0
```

because

```text
2( (kappa 10^2 + 3/2)/11 - 1 )^2 ≈ 4.399
```

while

```text
11^2 / 28 = 121/28 ≈ 4.321,
```

so `g_28(11) > 0`. Hence `g_28(p) > 0` for every `p >= 11`, and we obtain

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 28
```

for all primes `p >= 11`.

### Theorem 4.2 (large-`p` strengthening)

For every prime `p >= 67`,

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 9.
```

### Proof

The same coprime-pair argument gives

```text
n >= kappa (p-1)^2 + 3/2.
```

So by Corollary 3.3,

```text
sum E(k)^2
 >= 2( (kappa (p-1)^2 + 3/2)/p - 1 )^2.
```

Define

```text
g_9(p)
 = 2( (kappa (p-1)^2 + 3/2)/p - 1 )^2 - p^2/9.
```

Again, a direct derivative check gives

```text
g_9'(p) > 0
```

for all `p >= 67`, so `g_9` is increasing there.
At `p = 67` it is already positive, since

```text
2( (kappa 66^2 + 3/2)/67 - 1 )^2 ≈ 501.17
```

while

```text
67^2 / 9 = 4489/9 ≈ 498.78.
```

Therefore

```text
sum_{k=1}^{p-1} E(k)^2 >= p^2 / 9
```

for all primes `p >= 67`.

---

## 5. Exact pair-kernel / Dedekind-sum formula

Write the classical sawtooth

```text
((x)) = {x} - 1/2
```

for nonintegral `x`, so `beta(x) = -((x))`.

For coprime `h,p`, the Dedekind sum is

```text
s(h,p) = sum_{k=1}^{p-1} ((k/p)) ((hk/p)).
```

Since `beta = -((·))`, we get

```text
sum_{k=1}^{p-1} beta(ak/p) beta(bk/p)
 = s(ba^{-1}, p)
```

for `a,b` nonzero mod `p`.

Combining this with the exact expansion of `E(k)` gives:

### Proposition 5.1

```text
sum_{k=1}^{p-1} E(k)^2
 = sum_{a=1}^{p-1} sum_{b=1}^{p-1}
   lambda_p(a) lambda_p(b) s(ba^{-1}, p).
```

This is an exact positive quadratic form with kernel `s(r,p)` on the
multiplicative group `(Z/pZ)^x`.

### Immediate spectral corollary

Because the kernel depends only on `ba^{-1}`, multiplicative characters
diagonalize it. If

```text
K_p(r) = s(r,p),
Lambda_p(chi) = sum_{a=1}^{p-1} lambda_p(a) chi(a),
```

then

```text
sum_{k=1}^{p-1} E(k)^2
 = (1/(p-1)) sum_{chi mod p} Khat_p(chi) |Lambda_p(chi)|^2,
```

where

```text
Khat_p(chi) = sum_{r=1}^{p-1} s(r,p) chi(r).
```

This is the cleanest exact version of the **pair-correlation / BCZ-type**
route that I have found so far.

---

## 6. Exact reciprocal-interval decomposition of the coefficients

Because

```text
lambda_p(m) = M(floor((p-1)/m)) + 1_{m=1},
```

the coefficients are constant on reciprocal intervals:

```text
floor((p-1)/m) = t
```

whenever

```text
(p-1)/(t+1) < m <= (p-1)/t.
```

So for every multiplicative character `chi`,

```text
Lambda_p(chi)
 = chi(1)
   + sum_{t=1}^{p-1} M(t)
     sum_{(p-1)/(t+1) < m <= (p-1)/t} chi(m).
```

This reduces the spectral side to **character sums over reciprocal intervals**.
That feels much closer to something attackable with classical character-sum
technology than the older formulations.

---

## 7. What this helps, approach by approach

### A. Sampled `L^2`

This is the clearest new progress.

I now have a genuine unconditional theorem:

```text
sum E(k)^2 >= p^2 / 28
```

for all primes `p >= 11`, and in fact

```text
sum E(k)^2 >= p^2 / 9
```

for all primes `p >= 67`.

That still does not by itself prove `D' > A'`, but it is a real non-circular
`c_0 p^2` lower bound and gives the sampled-`L^2` route a concrete analytic
base.

### B. Pair correlation / BCZ kernel

This is also materially improved.

The exact Dedekind-kernel formula shows that the problem is not vaguely
"pair-correlation-like" but literally an exact quadratic form on
`(Z/pZ)^x` with kernel `s(r,p)`. The next step is to understand the character
eigenvalues `Khat_p(chi)` and the reciprocal-interval character sums
`Lambda_p(chi)`.

### C. Direct deficit

The new theorem does not prove

```text
max(A' - D', 0) <= 0.01 p^2.
```

But if the researchers can prove that direct-deficit statement, then the new
sampled-`L^2` bound gives extra headroom rather than forcing all the burden
onto `C'`.

### D. `K`-bound

I do not currently have a credible analytic route to

```text
|1 - D/A| <= K |M| / p
```

with explicit `K <= 50`.

At the moment, the sampled-`L^2` and pair-kernel formulations look more
natural and more structurally grounded than the `K`-bound route.

---

## 8. Bottom line

The best honest answer is:

- **yes**, I can help the sampled-`L^2` route right now, and I already have
  explicit theorems `sum E(k)^2 >= p^2/28` for all `p >= 11` and
  `sum E(k)^2 >= p^2/9` for all `p >= 67`
- **yes**, I can help the pair-correlation route, because there is now an
  exact Dedekind-kernel / multiplicative-spectral reformulation
- **no**, I do not yet have a proof of the `K`-bound

If I were choosing the next technical target, I would push the pair-kernel
formula together with the reciprocal-interval character sums. That now looks
like the cleanest structural bridge between the Möbius coefficients and the
sampled `L^2` growth.
