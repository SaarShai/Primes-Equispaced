# Codex Progress Memo
## Session 8 follow-up
## Date
2026-03-29

## Purpose
This memo is a standalone summary of the progress I made independently of the
existing project notes. It is written to be handed directly to the researchers.

The main point is:

> I did not close the Sign Theorem tail, but I found a cleaner non-circular
> formulation of Gap 2 and pushed it to the point where the remaining hard
> object is now sharply isolated.

---

## 1. What I actually made progress on

### A. I reduced the Gap 2 problem to a sampled Farey-counting error on the `p`-grid

For a prime `p`, let `N = p - 1`, let `F_N` be the Farey sequence of order `N`,
and let `n = |F_N|`.

For `1 <= k <= p-1`, define

```text
A(k) = #{f in F_N : f <= k/p}
E(k) = A(k) - n*k/p.
```

Then the new-fraction displacement satisfies the exact identity

```text
D_new(k/p) = E(k) + k/p
```

for the displacement convention used in the current project:

```text
D(f) = rank(f) - n f.
```

This turns the new-fraction second moment into

```text
D' = sum_{k=1}^{p-1} D_new(k/p)^2
   = sum E(k)^2 + 2 sum (k/p)E(k) + sum (k/p)^2.
```

This is the cleanest non-circular entry point I found for Gap 2.

### B. I proved the sampled error has exact mean zero

The first exact identity is

```text
sum_{k=1}^{p-1} E(k) = 0.
```

Equivalently,

```text
sum_{k=1}^{p-1} A(k) = n(p-1)/2.
```

This is a denominator-by-denominator permutation argument using the fact that
multiplication by `p` permutes reduced residues modulo every `b < p`.

### C. I identified the exact first moment of the new-fraction displacements

With the sign convention above,

```text
sum_{k=1}^{p-1} D_new(k/p) = (p-1)/2.
```

If another note in the project uses the opposite displacement sign convention,
the same magnitude appears with a minus sign. This explains the handoff's
`±(p-1)/2` phenomenon without ambiguity.

### D. I derived an exact weighted first-moment identity

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

This makes the correction term in `D'` explicit rather than heuristic.

### E. I derived an exact pair-count formula for the hard term `sum E(k)^2`

Let `F_N^* = F_N \ {1}`. Then

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

This is the most useful exact reformulation I found: it shows the sampled
second moment is a genuine pair-count object on the `p`-grid, which means it
should be attackable by discrete Franel-Landau / Farey pair-correlation ideas.

---

## 2. The strongest numerical pattern I found

I checked the sampled second moment and the explicit correction term with exact
rational arithmetic for a range of small and medium primes.

### Main observation

The quantity

```text
sum E(k)^2 / (p^2 log p)
```

looks surprisingly stable.

Here is a representative table:

| `p` | `sum E(k)^2 / p^2` | `sum E(k)^2 / (p^2 log p)` | `correction / p^2` | `D' / p^2` |
|---:|---:|---:|---:|---:|
| 31  | 0.2060 | 0.0600 | 0.0341 | 0.2401 |
| 43  | 0.2398 | 0.0638 | 0.0249 | 0.2647 |
| 61  | 0.2730 | 0.0664 | 0.0151 | 0.2881 |
| 97  | 0.3048 | 0.0666 | 0.0096 | 0.3144 |
| 113 | 0.3129 | 0.0662 | 0.0149 | 0.3278 |
| 151 | 0.3272 | 0.0652 | 0.0095 | 0.3367 |
| 199 | 0.3507 | 0.0663 | 0.0122 | 0.3629 |

This suggests the candidate asymptotic

```text
sum E(k)^2 ~ c * p^2 log p
```

with `c` plausibly around `0.06` to `0.067`.

I am **not** claiming this is proved. I am saying it is the most interesting
new numerical signal I found, and it points strongly toward the sampled
second-moment route being viable.

### Relative size of the correction term

The explicit correction term

```text
2 sum (k/p)E(k) + sum (k/p)^2
```

is much smaller than `sum E(k)^2` in the tested range.

For example:

| `p` | `sum E(k)^2 / correction` |
|---:|---:|
| 31  | 6.05 |
| 61  | 18.04 |
| 97  | 31.72 |
| 151 | 34.49 |
| 199 | 28.71 |
| 251 | 43.29 |
| 313 | 60.39 |

Again, this is not a proof, but it is exactly the shape one wants if the goal
is to show the sampled second moment is the dominant piece of `D'`.

---

## 3. What this means for the proof

At this point, the real hard part of Gap 2 can be stated very cleanly:

> Prove a lower bound for the sampled second moment
> `sum_{k=1}^{p-1} E(k)^2`,
> and show the weighted correction term is lower order.

That is much better than the older circular formulations of `1 - D'/A'`.

The problem has now been reduced to something that looks like:

```text
discrete L^2 discrepancy of F_{p-1} on the p-grid.
```

This is the precise mathematical object I would now hand to anyone trying to
finish the proof.

---

## 4. What I did not prove

I want to be explicit about the current limit.

I did **not** prove:

- an unconditional lower bound of the form `sum E(k)^2 >= c p^2`
- an unconditional lower bound of the stronger form
  `sum E(k)^2 >= c p^2 log p`
- a rigorous upper bound on the weighted correction term strong enough to close Gap 2
- the full tail theorem

So this is genuine progress, but it is still progress toward the proof,
not the proof itself.

---

## 5. Deliverables created from this progress

The main technical content above is written out in more detail in the
following new standalone files:

- [DISCRETE_PGRID_IDENTITIES.md](/Users/saar/Documents/Codex reviewer/session8_handoff/experiments/DISCRETE_PGRID_IDENTITIES.md)
- [DISCRETE_PGRID_SECOND_MOMENT_ROADMAP.md](/Users/saar/Documents/Codex reviewer/session8_handoff/experiments/DISCRETE_PGRID_SECOND_MOMENT_ROADMAP.md)

This memo is the compressed version intended for discussion with the
research team.
