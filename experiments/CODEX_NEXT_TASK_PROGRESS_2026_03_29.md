# Codex Progress on the Next Task
## Dedekind eigenvalues, `Λ_p` mean square, and small-`k` formulas
## Date
2026-03-29

## Purpose
This note responds to the follow-up task in
[CODEX_NEXT_TASK.md](/Users/saar/Desktop/Farey-Local/CODEX_NEXT_TASK.md).

The most important outcome is that the Dedekind-kernel spectrum is now much
cleaner than it first appeared:

- it vanishes on the entire even character sector,
- it is a positive square on the odd sector,
- and for odd characters it is exactly proportional to `|L(1,χ)|^2`.

That is a genuine structural breakthrough for the pair-correlation route.

---

## 1. Dedekind-kernel eigenvalues

Let

```text
K_p(r) = s(r,p),
```

where `s(r,p)` is the Dedekind sum, and for a Dirichlet character `χ mod p`
define

```text
Khat_p(χ) = sum_{r=1}^{p-1} s(r,p) χ(r).
```

Also define

```text
B_1,p(χ) = sum_{a=1}^{p-1} χ(a) ((a/p)),
```

with `((x)) = {x} - 1/2` on nonintegral arguments.

### Proposition 1.1

For every character `χ mod p`,

```text
Khat_p(χ) = B_1,p(χ) B_1,p(conj χ).
```

### Proof

Using the classical expression

```text
s(r,p) = sum_{a=1}^{p-1} ((a/p)) ((ra/p)),
```

we get

```text
Khat_p(χ)
 = sum_{r=1}^{p-1} χ(r) sum_{a=1}^{p-1} ((a/p)) ((ra/p))
 = sum_{a=1}^{p-1} ((a/p)) sum_{r=1}^{p-1} χ(r) ((ra/p)).
```

For fixed `a`, multiplication by `a` permutes `(Z/pZ)^x`, so with `m = ra`
we have

```text
sum_{r=1}^{p-1} χ(r) ((ra/p))
 = χ(a^{-1}) sum_{m=1}^{p-1} χ(m) ((m/p))
 = conj χ(a) B_1,p(χ).
```

Substituting back,

```text
Khat_p(χ)
 = B_1,p(χ) sum_{a=1}^{p-1} conj χ(a) ((a/p))
 = B_1,p(χ) B_1,p(conj χ).
```

This is exact.

### Corollary 1.2

- If `χ` is even, then `Khat_p(χ)=0`.
- If `χ` is odd, then `Khat_p(χ)=|B_1,p(χ)|^2 >= 0`.

### Reason

For even `χ`, pairing `a` with `p-a` gives cancellation because

```text
(( (p-a)/p )) = -((a/p))
```

while `χ(p-a)=χ(-1)χ(a)=χ(a)`.

For odd `χ`, `B_1,p(conj χ)=conj(B_1,p(χ))`, so Proposition 1.1 becomes a
nonnegative square.

### Corollary 1.3

For every nonprincipal odd character `χ mod p`,

```text
Khat_p(χ) = (p / pi^2) |L(1,χ)|^2.
```

### Reason

Every nonprincipal character mod prime `p` is primitive. For primitive odd
characters, the functional equation gives

```text
L(1,χ) = (pi i / p) tau(χ) B_1,p(conj χ),
```

and `|tau(χ)|^2 = p`. Therefore

```text
|B_1,p(χ)|^2 = (p / pi^2) |L(1,χ)|^2.
```

Combining with Corollary 1.2 gives the claim.

### Consequence

The hoped-for positivity is true:

```text
Khat_p(χ) >= 0
```

for every character, with exact vanishing on the even sector.

This is much stronger than a mere numerical observation.

---

## 2. Exact spectral identities

### Proposition 2.1

The total spectral mass is

```text
sum_{χ mod p} Khat_p(χ)
 = (p-1) s(1,p)
 = (p-1)^2 (p-2) / (12p).
```

### Proof

By character orthogonality,

```text
sum_χ Khat_p(χ)
 = sum_{r=1}^{p-1} s(r,p) sum_χ χ(r).
```

Only `r=1` survives, so

```text
sum_χ Khat_p(χ) = (p-1) s(1,p).
```

The standard formula

```text
s(1,p) = (p-1)(p-2)/(12p)
```

gives the result.

### Corollary 2.2

Since only odd characters contribute,

```text
sum_{χ odd} Khat_p(χ)
 = (p-1)^2 (p-2) / (12p).
```

Hence the average odd eigenvalue is

```text
avg_{χ odd} Khat_p(χ) = (p-1)(p-2)/(6p) ~ p/6.
```

Equivalently,

```text
avg_{χ odd} |L(1,χ)|^2
 = (pi^2 / p) avg_{χ odd} Khat_p(χ)
 = pi^2 (p-1)(p-2) / (6p^2)
 -> pi^2/6.
```

This exact average is useful context for the spectral route.

---

## 3. Small-prime numerical checks

I numerically checked `p = 11, 13, 17, 23`.

### Observations

- every even-character eigenvalue was numerically zero,
- every odd-character eigenvalue was positive,
- `Khat_p(χ)` matched `B_1,p(χ) B_1,p(conj χ)` to machine precision,
- and the odd spectrum was symmetric under `j <-> p-1-j`.

### Table

| `p` | `#even/#odd` | `sum Khat_p(χ)` | min odd `Khat` | max odd `Khat` |
|---:|---:|---:|---:|---:|
| 11 | 5/5 | `75/11 = 6.818182` | `0.641430` | `2.267661` |
| 13 | 6/6 | `132/13 = 10.153846` | `0.472584` | `2.604339` |
| 17 | 8/8 | `320/17 = 18.823529` | `0.354317` | `4.680840` |
| 23 | 11/11 | `848/23 = 36.826087` | `0.765007` | `9.000000` |

Representative odd-character eigenvalues:

| `p` | distinct odd eigenvalues up to symmetry |
|---:|---|
| 11 | `2.267661, 0.641430, 1.000000` |
| 13 | `2.604339, 2.000000, 0.472584` |
| 17 | `4.680840, 1.689516, 0.354317, 2.687092` |
| 23 | `6.643165, 2.751411, 0.765007, 2.458189, 1.295271, 9.000000` |

This is strong evidence that the exact formulas above are the right
spectral framework.

---

## 4. Exact Parseval identities for `Λ_p`

Recall

```text
Lambda_p(χ) = sum_{a=1}^{p-1} lambda_p(a) χ(a),
lambda_p(a) = M(floor((p-1)/a)) + 1_{a=1}.
```

Set `N = p-1`.

### Proposition 4.1 (total mean square)

```text
sum_{χ mod p} |Lambda_p(χ)|^2
 = (p-1) sum_{a=1}^{N} lambda_p(a)^2.
```

This is just character orthogonality on `(Z/pZ)^x`.

### Exact interval form

If

```text
c_t(N) = floor(N/t) - floor(N/(t+1)),
```

then

```text
sum_{a=1}^{N} lambda_p(a)^2
 = sum_{t=1}^{N} c_t(N) M(t)^2 + 2M(N) + 1.
```

So the total `Λ_p` energy is exactly a weighted Mertens-square sum.

### Proposition 4.2 (odd-character mean square)

Let the sum run only over odd characters `χ(-1)=-1`. Then

```text
sum_{χ odd} |Lambda_p(χ)|^2
 = (p-1)/2 * [ M(N)^2 + sum_{a=2}^{N/2} ( M(floor(N/a)) - 1 )^2 ].
```

Equivalently, grouping by `t = floor(N/a)`,

```text
sum_{χ odd} |Lambda_p(χ)|^2
 = (p-1)/2 * [ M(N)^2 + sum_{t=2}^{N/2} c_t(N) (M(t)-1)^2 ].
```

### Proof sketch

The odd spectral side sees only the antisymmetric part under `a <-> p-a`.
Since

```text
lambda_p(p-a) = 1
```

for `1 <= a <= N/2`, the antisymmetric difference is

```text
lambda_p(a) - lambda_p(p-a)
 = M(floor(N/a)) - 1
```

for `a >= 2`, while the pair `{1,p-1}` contributes `M(N)`.
Parseval on the odd subspace gives the formula.

### Immediate lower bound

Using only the interval where `floor(N/a)=2`, namely `N/3 < a <= N/2`,

```text
sum_{χ odd} |Lambda_p(χ)|^2 >= (p-1)^2 / 12.
```

Indeed, on that interval `M(2)=0`, so `(M(2)-1)^2 = 1`, and the interval
contains at least `N/6` integers.

### Important heuristic

The interval form shows where a `log p` could come from.

If one had an average law of the shape

```text
M(t)^2 on average ~ const * t,
```

then with `c_t(N) ~ N/t^2` the odd-energy sum would look like

```text
(p-1)/2 * sum_{t<=N} (N/t^2) * t
 ~ const * p^2 log p.
```

So the `log p` may be more naturally visible in the spectral `Lambda_p`
energy than in the first few small-`k` evaluations alone.

This is not a theorem here, but it is a plausible mechanism.

---

## 5. Exact small-`k` counting formulas

Let

```text
A_k(p) = #{ f in F_{p-1} : f <= k/p }.
```

Then

```text
E(k) = A_k(p) - k n / p,
```

with `n = |F_{p-1}|`.

### General exact formula for fixed `k`

For fixed `k < p`,

```text
A_k(p)
 = 1 + sum_{a=1}^{k-1} sum_{d|a} mu(d)
     [ floor((p-1)/d) - floor((ap-1)/(kd)) ].
```

This comes from counting reduced fractions `a/b <= k/p` by numerator `a`
and then using inclusion-exclusion on `gcd(a,b)=1`.

For `k=3,4,5`, this simplifies to short residue-class formulas.

### Exact formula for `A_3(p)`

For primes `p > 3`,

```text
if p ≡ 1 (mod 6):  A_3(p) = (5p + 1)/6
if p ≡ 5 (mod 6):  A_3(p) = (5p - 1)/6
```

### Exact formula for `A_4(p)`

For primes `p > 3`,

```text
if p ≡ 1  (mod 12):  A_4(p) = (7p - 1)/6
if p ≡ 5  (mod 12):  A_4(p) = (7p + 1)/6
if p ≡ 7  (mod 12):  A_4(p) = (7p - 7)/6
if p ≡ 11 (mod 12):  A_4(p) = (7p - 5)/6
```

### Exact formula for `A_5(p)`

For primes `p > 5`,

```text
if p ≡ 1  (mod 30):  A_5(p) = (22p - 7)/15
if p ≡ 7  (mod 30):  A_5(p) = (22p - 19)/15
if p ≡ 11 (mod 30):  A_5(p) = (22p - 2)/15
if p ≡ 13 (mod 30):  A_5(p) = (22p - 16)/15
if p ≡ 17 (mod 30):  A_5(p) = (22p - 14)/15
if p ≡ 19 (mod 30):  A_5(p) = (22p - 28)/15
if p ≡ 23 (mod 30):  A_5(p) = (22p - 11)/15
if p ≡ 29 (mod 30):  A_5(p) = (22p - 23)/15
```

These were independently checked against exact Farey counts.

---

## 6. What these small-`k` formulas suggest

Using the standard lower bound already present elsewhere in the project,

```text
n = |F_{p-1}| >= 3(p-1)^2/pi^2 - (p-1) + 1,
```

the exact formulas above make `E(2), E(3), E(4), E(5)` explicit linear upper
bounds in `p`, residue class by residue class.

### Empirical threshold pattern from those exact formulas

- `E(2)` is forced negative by that lower bound from `p >= 37`
- `E(3)` from `p >= 61`
- `E(4)` from `p >= 127`
- `E(5)` from `p >= 137`

So from `p >= 137`, the first five exact mesh points all already contribute
with the correct sign under the classical totient lower bound.

I have not turned this yet into a polished theorem in this note, but it
reduces the stronger sampled-`L^2` bound to finitely many explicit
residue-class inequalities.

### Important caution

The first few small-`k` terms do strengthen the `p^2` lower bound, but by
themselves they do **not** yet convincingly explain a full `p^2 log p`
growth. The spectral `Lambda_p` interval formula looks more like the natural
home for the `log p` mechanism.

---

## 7. Best next steps

### 1. Turn Proposition 1.1 into the main spectral lemma

This should now be treated as the core exact identity:

```text
Khat_p(χ) = 0   for even χ,
Khat_p(χ) = (p/pi^2)|L(1,χ)|^2   for odd χ.
```

That gives automatic positivity and a direct bridge to analytic number theory.

### 2. Work on lower-bounding odd-character `Lambda_p` energy

The exact formula

```text
sum_{χ odd} |Lambda_p(χ)|^2
 = (p-1)/2 * [ M(N)^2 + sum_{t=2}^{N/2} c_t(N)(M(t)-1)^2 ]
```

is the strongest concrete next target I found. If this can be shown to be
`gg p^2 log p`, then the positivity of `Khat_p(χ)` becomes genuinely useful.

### 3. Keep extending the exact small-`k` library

`A_3(p), A_4(p), A_5(p)` are now explicit. The same inclusion-exclusion method
should also produce `A_6(p), A_7(p), ...`, though the residue bookkeeping
gets more complicated.

### 4. Don’t overclaim yet

What is proved here:

- exact positivity/vanishing structure of `Khat_p(χ)`
- exact Parseval formulas for `Lambda_p`
- exact small-`k` formulas through `k=5`

What is **not** yet proved here:

- a full lower bound strong enough by itself to close Gap 2
- a theorem of size `sum E(k)^2 gg p^2 log p`
- a rigorous conversion of spectral positivity into the final inequality

---

## Bottom line

The Dedekind-kernel route is now materially stronger than before.

It is no longer just “maybe pair correlation helps.” It is now:

```text
exact positive spectrum on odd characters
+ exact L(1,χ) formula
+ exact weighted Mertens-energy formula for Lambda_p.
```

That feels like the cleanest current path for serious further work.
