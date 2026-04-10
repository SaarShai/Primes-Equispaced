# Codex Independent Exploration
## Correction-term scaling in the `p`-grid decomposition
## Date
2026-03-29

## Purpose
This note records one more independent exploration after the `p`-grid
reformulation of Gap 2. The question was:

> Is the explicit correction term in
> `D' = sum E(k)^2 + 2 sum (k/p)E(k) + sum (k/p)^2`
> actually lower order relative to `A'`?

This matters because if the answer is yes, then the hard part of Gap 2 really
does collapse to understanding the sampled second moment `sum E(k)^2`.

---

## Setup

For each prime `p`, let

```text
E(k) = #{f in F_{p-1} : f <= k/p} - n k/p,
```

and write

```text
Corr(p) = D' - sum_{k=1}^{p-1} E(k)^2.
```

I computed `sum E(k)^2`, `D'`, and `A'` using exact rational arithmetic for
all primes `13 <= p <= 401`.

---

## Main empirical findings

### Finding 1
The ratio

```text
sum E(k)^2 / A'
```

stays very close to `1` across the full tested sample.

For all primes `13 <= p <= 401`, the average value is about

```text
0.9800.
```

For larger primes the fit gets tighter:

| prime range | average `sum E(k)^2 / A'` |
|---|---:|
| `p >= 100` | `0.9896` |
| `p >= 150` | `0.9898` |
| `p >= 200` | `0.9904` |
| `p >= 250` | `0.9925` |
| `p >= 300` | `0.9920` |

### Finding 2
The correction ratio

```text
Corr(p) / A'
```

is small and gets smaller on average as `p` grows.

| prime range | average `Corr(p) / A'` | min | max |
|---|---:|---:|---:|
| all tested primes | `0.0509` | `0.0091` | `0.3408` |
| `p >= 100` | `0.0245` | `0.0091` | `0.0547` |
| `p >= 150` | `0.0208` | `0.0091` | `0.0360` |
| `p >= 200` | `0.0176` | `0.0091` | `0.0252` |
| `p >= 250` | `0.0170` | `0.0091` | `0.0250` |
| `p >= 300` | `0.0148` | `0.0091` | `0.0194` |

### Finding 3
In the negative-Mertens regime the same pattern persists.

For primes with `M(p) <= -3` and `p >= 100`, the averages are:

```text
sum E(k)^2 / A'  ~ 0.9869
D' / A'          ~ 1.0158
Corr(p) / A'     ~ 0.0288
```

So even in the regime most relevant to the current Sign Theorem story,
the correction term looks much smaller than the main sampled second moment.

---

## Interpretation

The cleanest reading of the data is:

```text
sum E(k)^2 = A' + lower-order terms,
Corr(p) = o(A')
```

at least as a very plausible conjectural picture.

I am not claiming a proof. I am claiming that this is now a much sharper and
better-supported target than the older heuristic statement that `D'/A'` is
"close to 1".

---

## Strong candidate conjecture

The strongest concise conjecture suggested by the wider sample is:

```text
sum_{k=1}^{p-1} E(k)^2 / A' -> 1
```

as `p -> infinity` along primes.

If this is true and the correction term is genuinely lower order, then

```text
D' / A' -> 1
```

should follow as a secondary consequence rather than being the primary object
of attack.

---

## Why this may improve the paper

This gives the researchers a cleaner proof narrative:

1. Recast Gap 2 as a sampled discrepancy problem on the `p`-grid.
2. Identify `sum E(k)^2` as the main structural term.
3. State the correction term as explicit and plausibly lower order.
4. Present the unconditional tail as an open program centered on the sampled
   second moment, rather than on circular `D'/A'` language.

That story is both more honest and mathematically more focused.

---

## Best next steps from this exploration

1. Prove any nontrivial lower bound for `sum E(k)^2` that scales like `p^2`
   or better.
2. Look for a direct representation of `A'` that can be compared termwise or
   kernelwise with the pair-count formula for `sum E(k)^2`.
3. Extend the exact sample farther to see whether `Corr(p)/A'` continues to
   shrink and whether `sum E(k)^2 / A'` stabilizes even more tightly near `1`.
