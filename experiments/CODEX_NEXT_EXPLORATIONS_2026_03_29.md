# Codex Next Explorations
## Prioritized agenda for the researchers
## Date
2026-03-29

## Purpose
This is a standalone exploration agenda based on the progress I made. It is
not a rewrite of the existing notes; it is a fresh recommendation list for
what looks genuinely worth pursuing next.

---

## Executive summary

The best live direction is no longer “bound `1-D'/A'` somehow.”
It is:

> understand the sampled discrepancy energy
> `sum_{k=1}^{p-1} E(k)^2`
> on the `p`-grid.

That is where I would concentrate human proof effort now.

---

## Track 1: Prove a lower bound for the sampled second moment
## Priority: highest
## Why
This is the clearest remaining hard object in the new non-circular formulation.

### Target
Try to prove either

```text
sum E(k)^2 >= c1 * p^2
```

or, more ambitiously,

```text
sum E(k)^2 >= c2 * p^2 log p.
```

Even the first would already be important. The second is suggested by the data.

### Most promising entry points

1. Compare the sampled second moment on the `p`-grid with the usual continuous
   Franel-Landau `L^2` discrepancy.

2. Attack the exact pair-count kernel

```text
sum_{f,g} (p-1 - floor(p * max(f,g)))
```

directly, perhaps by rewriting it as a weighted count of pairs near the upper
right corner of the Farey square.

3. Use denominator-class decompositions only after the pair-count rewrite, not
   before. The per-denominator route by itself looked too lossy elsewhere in the
   project.

### Concrete next lemma
A genuinely useful next lemma would be:

```text
There exists c > 0 such that
sum_{k=1}^{p-1} E(k)^2 >= c p^2
for all sufficiently large primes p.
```

That would already make the new route real.

---

## Track 2: Control the explicit correction term
## Priority: high
## Why
Once `sum E(k)^2` is under control, the correction term is the only remaining
obstruction inside the exact `D'` decomposition.

### Exact object

```text
2 sum (k/p)E(k) + sum (k/p)^2.
```

Using the weighted first-moment identity, this becomes an explicit expression
in terms of `n`, `S_2`, and `C_prop`.

### What to try

1. Compute or bound `S_2 = sum_{x in F_N^prop} x^2` asymptotically with an
   explicit main term and error term.

2. Relate `C_prop` to the already better-understood shift-squared term `C`.

3. Prove an upper bound of the shape

```text
|2 sum (k/p)E(k) + sum (k/p)^2| <= Cp^2 / log p
```

or anything comparably smaller than the conjectural `p^2 log p` scale of
`sum E(k)^2`.

### Why this looks plausible
Numerically, the correction term is dramatically smaller than `sum E(k)^2`
already in the low hundreds. So even a fairly crude proof may be enough.

---

## Track 3: Look for a sampled Franel-Landau theorem
## Priority: high
## Why
Conceptually, this may be the right statement behind Gap 2.

### Question
Is there an existing theorem, or can one be proved, saying that the Farey
discrepancy sampled on the mesh `{k/p}` has second moment comparable to the
continuous second moment?

### What to search for

1. Discrete sampling versions of Franel or Landau
2. Farey pair-correlation results that can be specialized to a fixed prime mesh
3. Quadrature or discrepancy results for Farey nodes tested against step functions

### Why this matters
If a sampled `L^2` theorem already exists, Gap 2 may collapse much faster than
the project currently assumes.

---

## Track 4: Revisit the pair-correlation literature with the new kernel
## Priority: medium-high
## Why
The exact pair-count formula is new in the project, and it changes what should
be compared to the literature.

### New kernel to focus on

```text
K_p(f,g) = p - 1 - floor(p * max(f,g)).
```

This is not the standard nearest-neighbor kernel. It is a monotone upper-tail
pair kernel on the Farey square.

### Suggested question
Can known asymptotics for Farey pair statistics be adapted to this kernel,
either directly or after summation by parts?

### Possible payoff
If yes, the second moment `sum E(k)^2` may become a standard asymptotic object
rather than a bespoke one.

---

## Track 5: Computational exploration that is still worth doing
## Priority: medium
## Why
There is still room for smart computation, but it should now be aimed at
the new objects, not more generic `D/A` summaries.

### Recommended computations

1. Extend exact or very-high-precision measurements of

```text
sum E(k)^2 / (p^2 log p)
```

to a substantially larger prime range.

2. Track

```text
correction / p^2, correction * log p / p^2,
sum E(k)^2 / correction.
```

3. Group `E(k)` by intervals, by denominator strata, or by nearby mesh scale
   to see whether the mass is spread smoothly or concentrated.

4. Check whether the candidate constant in

```text
sum E(k)^2 ~ c p^2 log p
```

appears stable across congruence classes or Mertens classes.

### Why this matters
These are the computations most likely to suggest the right theorem statement.

---

## Track 6: Lean targets once the full project is present
## Priority: medium
## Why
Formalization should now follow the cleaner math, not the old circular route.

### Best first targets

1. Formalize

```text
D_new(k/p) = E(k) + k/p
```

2. Formalize

```text
sum E(k) = 0
```

3. Formalize the exact weighted first-moment identity

4. Formalize the pair-count formula for `sum E(k)^2`

### Why this order
These are exact algebraic/discrete statements. They are much more robust Lean
targets than trying to formalize the whole tail proof prematurely.

---

## Track 7: What I would de-prioritize
## Priority: low

### A. More work on the old unconditional-closure sketch
That route is too entangled with the circular `D/A` story.

### B. Per-denominator positivity arguments
The project’s own evidence says the important cancellation is global, not local.

### C. Broad “`B+C>0` for all primes” narratives
The data already show that this is false. Future work should stay sharply tied
to the `M(p) <= -3` regime unless a new theorem justifies a broader claim.

---

## My recommendation

If the team only has bandwidth for one serious next move, I would choose:

> Prove a lower bound for `sum_{k=1}^{p-1} E(k)^2`.

That is the single most promising bridge between the new exact identities and
an actual closure of Gap 2.
