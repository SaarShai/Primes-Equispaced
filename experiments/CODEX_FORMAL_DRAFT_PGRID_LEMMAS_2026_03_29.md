# Codex Formal Draft
## p-grid lemmas for a future Gap 2 proof
## Date
2026-03-29

## Purpose
This file is written in a more formal theorem/lemma style so it can be reused
in project notes or adapted into the manuscript.

---

### Setup

Let `p` be prime, let `N = p - 1`, let `F_N` be the Farey sequence of order
`N`, and let `n = |F_N|`, `n' = |F_p| = n + p - 1`.

For `1 <= k <= p-1`, define

```text
A_p(k) = #{f in F_N : f <= k/p},
E_p(k) = A_p(k) - n k/p.
```

Let `D_p(k/p)` denote the displacement of the new fraction `k/p` in `F_p`
with the convention

```text
D(f) = rank(f) - |F| f.
```

---

## Lemma 1 (Exact p-grid decomposition)

For every `1 <= k <= p-1`,

```text
D_p(k/p) = E_p(k) + k/p.
```

### Proof sketch
The rank of the new fraction `k/p` in `F_p` is

```text
A_p(k) + k,
```

because `A_p(k)` old fractions lie at or below `k/p`, and among the new
fractions `1/p, 2/p, ..., (p-1)/p`, exactly `k` lie at or below `k/p`.
Subtracting `n' k/p` gives the result.

---

## Lemma 2 (Mean-zero identity)

For every prime `p`,

```text
sum_{k=1}^{p-1} E_p(k) = 0.
```

Equivalently,

```text
sum_{k=1}^{p-1} A_p(k) = n(p-1)/2.
```

### Proof sketch
Swap the order of summation in `sum_k A_p(k)`. For each proper old fraction
`a/b` with `b < p`, the number of integers `k` with `a/b <= k/p` equals

```text
p - 1 - floor(pa/b).
```

Summing `floor(pa/b)` over reduced residues modulo a fixed `b` gives

```text
(p-1) phi(b) / 2
```

because multiplication by `p` permutes the reduced residues modulo `b`.
Adding the boundary contributions from `0` and `1` yields the stated formula.

---

## Corollary 3 (First moment of the new displacements)

With the convention above,

```text
sum_{k=1}^{p-1} D_p(k/p) = (p-1)/2.
```

If the opposite sign convention for displacement is used, the same magnitude
appears with a minus sign.

---

## Lemma 4 (Exact weighted first moment)

Let

```text
F_N^prop = F_N \ {0,1},
S_2 = sum_{x in F_N^prop} x^2,
C_prop = sum_{x in F_N^prop} delta(x)^2,
delta(a/b) = a/b - {pa/b}.
```

Then

```text
sum_{k=1}^{p-1} (k/p) E_p(k)
= (p-1)(n(2p-1)-6(p-1)) / (12p)
 - (p-1)^2 S_2 / (2p)
 - C_prop / 2.
```

### Proof sketch
Start from

```text
sum_{k=1}^{p-1} k A_p(k)
= sum_{x in F_N} sum_{k >= px} k.
```

For a proper fraction `x`, the inner sum is

```text
p(p-1)/2 - q_x(q_x+1)/2
```

with `q_x = floor(px)`. Writing `q_x = px - {px}`, expanding
`q_x(q_x+1)`, and using the permutation-square-sum identity to handle the
mixed term yields the stated expression after simplification.

---

## Proposition 5 (Exact second-moment decomposition)

The new-fraction second moment satisfies

```text
D'
= sum_{k=1}^{p-1} E_p(k)^2
 + 2 sum_{k=1}^{p-1} (k/p) E_p(k)
 + (p-1)(2p-1)/(6p).
```

In particular, `D'` is determined by the sampled second moment
`sum E_p(k)^2` plus an explicit correction term.

---

## Proposition 6 (Pair-count formula for the sampled second moment)

Let `F_N^* = F_N \ {1}`. Then

```text
sum_{k=1}^{p-1} A_p(k)^2
  = sum_{f,g in F_N^*} (p-1 - floor(p * max(f,g))).
```

Hence

```text
sum_{k=1}^{p-1} E_p(k)^2
  = sum_{f,g in F_N^*} (p-1 - floor(p * max(f,g)))
    - (2n/p) sum_{k=1}^{p-1} k A_p(k)
    + (n^2/p^2) sum_{k=1}^{p-1} k^2.
```

### Proof sketch
Expand `A_p(k)^2` as a double indicator sum and interchange the order of
summation.

---

## Conjecture 7 (Sampled Farey `L^2` growth)

There exists `c > 0` such that

```text
sum_{k=1}^{p-1} E_p(k)^2 >= c p^2 log p
```

for all sufficiently large primes `p`.

### Practical weaker target
Even the weaker statement

```text
sum_{k=1}^{p-1} E_p(k)^2 >= c_0 p^2
```

would already make the new route into Gap 2 mathematically substantial.

---

## Remark on strategy

The old circular language around `1 - D'/A'` obscures the problem.
The lemmas above suggest a sharper reformulation:

> prove a lower bound for the sampled discrepancy energy
> `sum E_p(k)^2`,
> then control the explicit correction term.

That is the route I would now formalize and investigate first.
