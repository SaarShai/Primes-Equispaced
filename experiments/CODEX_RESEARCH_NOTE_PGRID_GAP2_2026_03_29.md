# Codex Research Note
## A discrete `p`-grid route into Gap 2
## Date
2026-03-29

## Purpose
This note isolates a small set of exact propositions and one explicit
conjecture that seem genuinely worth handing to the research team.

The theme is simple:

> Gap 2 should be reformulated as a discrete second-moment problem for
> Farey counting error on the `p`-grid.

This note is intentionally short and theorem-first.

---

## Setup

Let `p` be prime, let `N = p - 1`, let `F_N` be the Farey sequence of order
`N`, and let

```text
n = |F_N|,   n' = |F_p| = n + p - 1.
```

For `1 <= k <= p-1`, define

```text
A(k) = #{f in F_N : f <= k/p},
E(k) = A(k) - n*k/p.
```

So `E(k)` is the Farey counting error sampled on the mesh

```text
{1/p, 2/p, ..., (p-1)/p}.
```

Throughout, `D_new(k/p)` denotes the displacement of the new fraction `k/p`
in `F_p` using the current project convention

```text
D(f) = rank(f) - |F| f.
```

---

## Proposition 1: Exact new-fraction decomposition

For every `1 <= k <= p-1`,

```text
D_new(k/p) = E(k) + k/p.
```

### Why it matters
This converts the new-fraction second moment into a pure discrete discrepancy
problem:

```text
D' = sum_{k=1}^{p-1} D_new(k/p)^2
   = sum E(k)^2 + 2 sum (k/p)E(k) + sum (k/p)^2.
```

So the real object behind Gap 2 is not `D'/A'` abstractly, but the sampled
second moment `sum E(k)^2`.

---

## Proposition 2: Exact mean-zero identity

For every prime `p`,

```text
sum_{k=1}^{p-1} E(k) = 0.
```

Equivalently,

```text
sum_{k=1}^{p-1} A(k) = n(p-1)/2.
```

### Consequence
With the sign convention above,

```text
sum_{k=1}^{p-1} D_new(k/p) = (p-1)/2.
```

If another draft uses the opposite sign convention for displacement, the same
magnitude appears with the opposite sign.

### Why it matters
This gives a completely non-circular first moment for the new-fraction term.

---

## Proposition 3: Exact weighted first moment

Let

```text
F_N^prop = F_N \ {0,1},
S_2 = sum_{x in F_N^prop} x^2,
C_prop = sum_{x in F_N^prop} delta(x)^2,
delta(a/b) = a/b - {pa/b}.
```

Then

```text
sum_{k=1}^{p-1} (k/p) E(k)
= (p-1)(n(2p-1)-6(p-1)) / (12p)
 - (p-1)^2 S_2 / (2p)
 - C_prop / 2.
```

### Why it matters
The correction term in `D'`

```text
2 sum (k/p)E(k) + sum (k/p)^2
```

is therefore explicit rather than mysterious.

---

## Proposition 4: Exact pair-count formula for the hard term

Let

```text
F_N^* = F_N \ {1}.
```

Then

```text
sum_{k=1}^{p-1} A(k)^2
  = sum_{f,g in F_N^*} (p-1 - floor(p * max(f,g))).
```

Hence

```text
sum E(k)^2
  = sum_{f,g in F_N^*} (p-1 - floor(p * max(f,g)))
    - (2n/p) sum k A(k)
    + (n^2/p^2) sum k^2.
```

### Why it matters
This is the sharpest reformulation I found. It shows that the hard quantity
is a genuine pair statistic on the Farey square, which suggests that pair
correlation / sampled discrepancy methods are the right tools.

---

## Candidate conjecture

### Conjecture (Sampled Farey `L^2` growth on the prime mesh)
There exists an absolute constant `c > 0` such that, for all sufficiently
large primes `p`,

```text
sum_{k=1}^{p-1} E(k)^2 >= c p^2 log p.
```

More ambitiously, there may be an asymptotic

```text
sum_{k=1}^{p-1} E(k)^2 ~ c_* p^2 log p
```

for some positive constant `c_*`.

### Numerical evidence
The quantity

```text
sum E(k)^2 / (p^2 log p)
```

is quite stable in the tested range:

| `p` | `sum E(k)^2 / (p^2 log p)` |
|---:|---:|
| 31  | 0.0600 |
| 43  | 0.0638 |
| 61  | 0.0664 |
| 97  | 0.0666 |
| 113 | 0.0662 |
| 151 | 0.0652 |
| 199 | 0.0663 |

I am **not** asserting this as a theorem. I am asserting that it is the most
suggestive new pattern I found.

---

## Why this conjecture would matter

From Proposition 1,

```text
D' = sum E(k)^2 + explicit correction.
```

The explicit correction term is numerically much smaller than `sum E(k)^2`
in the tested range. So a proof of the conjecture above, together with any
reasonably smaller upper bound on the correction term, would make the
non-circular `D'` route into Gap 2 look very realistic.

In short:

> the problem now seems to be “prove a sampled Franel-Landau lower bound,”
> not “guess another way to bound `1-D'/A'`.”

---

## Recommended next theorem attempt

If the team wants one specific target, I would suggest trying to prove the
weaker but still useful statement:

```text
There exists c0 > 0 such that
sum_{k=1}^{p-1} E(k)^2 >= c0 p^2
for all sufficiently large primes p.
```

That alone would already make the new route mathematically substantial, even
before reaching the stronger `p^2 log p` conjecture.
