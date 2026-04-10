# Codex Independent Exploration
## Comparing the sampled second moment to `A'`
## Date
2026-03-29

## Purpose
This file records one additional exploration I ran independently after the
`p`-grid reformulation. The question was:

> How large is the sampled second moment `sum E(k)^2` compared to the
> dilution scale `A'` that appears in Gap 2?

This is directly relevant because the proof obstruction is not just “how large
is `D'`?” but “how does `D'` compare to `A'`?”

---

## Definitions

For a prime `p`, let

```text
A' = old_D_sq * (n'^2 / n^2 - 1),
```

where `old_D_sq = sum_{f in F_{p-1}} D(f)^2`, `n = |F_{p-1}|`, and
`n' = |F_p|`.

Let

```text
E(k) = #{f in F_{p-1} : f <= k/p} - n k/p,
D' = sum_{k=1}^{p-1} D_new(k/p)^2.
```

I computed:

- `sum E(k)^2 / A'`
- `D' / A'`
- `(D' - sum E(k)^2) / A'`

using exact rational arithmetic for a representative prime sample.

---

## Main empirical finding

The most striking pattern is:

```text
sum E(k)^2 / A' ~ 1
```

already quite early, and

```text
D' / A' > 1
```

throughout the sample.

This is stronger and more directly useful than the earlier generic observation
that `D'/A'` is “close to 1”.

---

## Data table

| `p` | `M(p)` | `sum E(k)^2 / A'` | `D' / A'` | `(D' - sum E(k)^2) / A'` |
|---:|---:|---:|---:|---:|
| 13  | -3 | 0.7751 | 1.1158 | 0.3408 |
| 19  | -3 | 0.9323 | 1.1812 | 0.2489 |
| 31  | -4 | 0.9404 | 1.0959 | 0.1555 |
| 43  | -3 | 0.9785 | 1.0801 | 0.1017 |
| 47  | -3 | 0.9840 | 1.0985 | 0.1146 |
| 53  | -3 | 1.0027 | 1.0937 | 0.0910 |
| 71  | -3 | 1.0040 | 1.0790 | 0.0751 |
| 73  | -4 | 0.9435 | 1.0015 | 0.0580 |
| 79  | -4 | 0.9773 | 1.0460 | 0.0687 |
| 83  | -4 | 0.9978 | 1.0678 | 0.0701 |
| 107 | -3 | 0.9967 | 1.0515 | 0.0547 |
| 109 | -4 | 0.9776 | 1.0232 | 0.0455 |
| 113 | -5 | 0.9612 | 1.0070 | 0.0457 |
| 151 | -1 | 0.9909 | 1.0196 | 0.0287 |
| 199 | -8 | 0.9776 | 1.0117 | 0.0341 |

---

## What I think this suggests

### Hypothesis 1
The sampled second moment may already be the main term of `A'`:

```text
sum E(k)^2 = A' + lower-order terms.
```

I am not claiming a proof, but the ratio data make this look plausible.

### Hypothesis 2
The correction term

```text
D' - sum E(k)^2
```

looks genuinely lower order relative to `A'`.

In the sample above it is already around `0.03` to `0.11` times `A'`, with a
general downward trend once `p` is moderately large.

### Hypothesis 3
The more natural target may not be “bound `D'/A'` directly”, but rather:

```text
sum E(k)^2 >= A' - small error.
```

That would be a sharper and more structured statement.

---

## Candidate conjecture

The strongest concise conjecture suggested by this exploration is:

```text
sum_{k=1}^{p-1} E(k)^2 / A' -> 1
```

as `p -> infinity` along primes.

If true, then the full `D'` term should be even easier to place on the correct
side of `A'`, provided the correction term remains lower order.

---

## Why this matters for the researchers

This exploration changes the feel of the problem.

Before:

> control `D'` somehow.

After:

> maybe `sum E(k)^2` is already the right proxy for `A'`,
> and the rest is just correction analysis.

That is a much more concrete research direction.

---

## What I would try next if continuing this line

1. Test `sum E(k)^2 / A'` on a larger exact or high-precision prime sample.
2. Try to express `A'` itself in a way that makes the comparison with
   `sum E(k)^2` more transparent.
3. Look for a shared pair-count or discrepancy representation of both
   quantities.
