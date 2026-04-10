# Codex Recommendations
## Paper improvements and next-step research priorities
## Date
2026-03-29

## Purpose
This note separates two questions that should stay distinct:

1. How should the paper be improved right now?
2. What research directions now look most promising for actually closing the
   remaining proof gap?

---

## Part I. Best paper improvements right now

### 1. Make the bounded theorem the stable headline
The safest current headline is the bounded computational Sign Theorem:

```text
for primes 11 <= p <= 100,000 with M(p) <= -3,
no counterexamples to Delta W(p) < 0 were found.
```

That is strong, concrete, and already interesting.

### 2. Present the unconditional tail as an open program
The paper should not imply that the analytical tail is already closed.
Instead, it should say:

- the exact identities are established
- the bounded theorem is established computationally
- the tail proof is open
- the new `p`-grid discrepancy route is the current best candidate

This makes the paper more credible, not less.

### 3. Stop centering the narrative on `D'/A'`
The old `D'/A'` language obscures the real issue and invites circularity.
The stronger narrative is:

- define the sampled error `E(k)`
- show `D_new(k/p) = E(k) + k/p`
- decompose `D'`
- identify `sum E(k)^2` as the core object

That is both cleaner and more mathematically informative.

### 4. Restrict all `B+C` claims to what is actually supported
The repo’s own data show `B+C > 0` is not true for all primes.
Any positive statement about `B+C` should be explicitly limited to the tested
negative-Mertens regime or to whatever range is actually proved or computed.

### 5. Keep formalization and reproducibility claims conservative
If the paper is distributed from partial snapshots, it should say so plainly.
Overstating current Lean or artifact status weakens referee trust much faster
than a candid limitation section does.

---

## Part II. Highest-value research directions

### Direction 1
Prove a lower bound for

```text
sum_{k=1}^{p-1} E(k)^2.
```

This is the best current target.

Even a lower bound of size `c p^2` would be meaningful progress.
A bound of size `c p^2 log p` would be a major breakthrough for the project.

### Direction 2
Find a structural formula for `A'` that can be compared directly with the
pair-count formula for `sum E(k)^2`.

This may be the shortest route to explaining why

```text
sum E(k)^2 / A'
```

appears numerically so close to `1`.

At the moment, the repo already has exact structural formulas on the `D'`
side, including the exact decomposition of `D'` and a pair-count formula for
`sum E(k)^2`, but I do not currently see a matching exact kernel or pair-count
representation for `A'` or `old_D_sq`. That missing representation now looks
like a particularly valuable target.

### Direction 3
Prove that the correction term

```text
D' - sum E(k)^2
```

is lower order relative to `A'`.

The current data strongly suggest this, and it would reduce Gap 2 to the
sampled second moment almost entirely.

### Direction 4
Look for a sampled Franel-Landau type theorem, pair-correlation theorem, or
large-sieve style estimate adapted to the prime mesh `k/p`.

The new discrete formulation suggests that the project now lives closer to a
mesh-sampled discrepancy problem than to the earlier heuristic framing.

### Direction 5
Extend the exact or high-precision numerics for:

- `sum E(k)^2 / (p^2 log p)`
- `sum E(k)^2 / A'`
- `(D' - sum E(k)^2) / A'`

The current evidence is already strong enough to guide conjectures, but a
larger table would help the team choose between competing asymptotic models.

---

## Part III. Concrete next theorem targets

If the researchers want a staged program, I would suggest:

1. Prove the exact `p`-grid lemmas cleanly and isolate the pair-count formula.
2. Prove a robust lower bound for `sum E(k)^2`.
3. Prove a separate upper bound for the correction term.
4. Only then return to the comparison with `A'`.

That ordering avoids circularity and aligns better with the new evidence.

---

## Bottom line

The paper improves most by being narrower and more explicit:

- strong bounded theorem now
- exact identities now
- unconditional tail later
- sampled discrepancy program as the live route forward

That is the version of the project that currently looks strongest to me.
