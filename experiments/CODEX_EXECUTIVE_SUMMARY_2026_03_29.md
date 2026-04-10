# Codex Executive Summary
## Session 8 math-paper follow-up
## Date
2026-03-29

## What is solid

- The bounded computational Sign Theorem is strong:
  for all primes `11 <= p <= 100,000` with `M(p) <= -3`,
  the project reports no counterexamples to `Delta W(p) < 0`.
- The exact bridge-identity / permutation infrastructure is mathematically real
  and still looks like the paper’s strongest conceptual contribution.
- The project now has a much cleaner non-circular entry point into Gap 2.

## What is not yet solid

- The unconditional analytical tail is still open.
- The old `D/A` route should not be treated as closed.
- `B+C > 0` is not a universal all-primes statement; it is a negative-Mertens
  phenomenon in the tested regime.

## My main independent progress

I found a better formulation of Gap 2.

For

```text
E(k) = #{f in F_{p-1} : f <= k/p} - n k/p,
```

the new-fraction displacement satisfies

```text
D_new(k/p) = E(k) + k/p.
```

This gives

```text
D' = sum E(k)^2 + 2 sum (k/p)E(k) + sum (k/p)^2.
```

I then derived:

- an exact mean-zero identity `sum E(k) = 0`
- an exact weighted first-moment identity for `sum (k/p)E(k)`
- an exact pair-count formula for `sum E(k)^2`

So the hard part of Gap 2 is now isolated as a discrete second-moment problem
for Farey counting error on the prime mesh.

## Strongest new numerical signal

The quantity

```text
sum E(k)^2 / (p^2 log p)
```

looks surprisingly stable, around `0.06` to `0.067` in the tested range.

This suggests a very plausible next conjecture:

```text
sum E(k)^2 ~ c p^2 log p.
```

I am not claiming this is proved. I am saying it is the strongest new lead I found.

## Strongest new exploration result

I also checked `sum E(k)^2` directly against the dilution scale `A'`.

Empirically:

- `sum E(k)^2 / A'` is already very close to `1`
- `D' / A'` is consistently above `1`
- the explicit correction term is much smaller than either

This suggests a sharper candidate route:

> prove `sum E(k)^2` is already of the same size as `A'`,
> then show the correction term is lower order.

## Best next move for the researchers

If the team focuses on one thing, it should be:

> prove a lower bound for `sum_{k=1}^{p-1} E(k)^2`.

That now looks like the most promising bridge from exact identities to a real
tail proof.

## New deliverables created

- [CODEX_PROGRESS_MEMO_2026_03_29.md](/Users/saar/Documents/Codex reviewer/session8_handoff/codex_deliverables/CODEX_PROGRESS_MEMO_2026_03_29.md)
- [CODEX_NEXT_EXPLORATIONS_2026_03_29.md](/Users/saar/Documents/Codex reviewer/session8_handoff/codex_deliverables/CODEX_NEXT_EXPLORATIONS_2026_03_29.md)
- [CODEX_RESEARCH_NOTE_PGRID_GAP2_2026_03_29.md](/Users/saar/Documents/Codex reviewer/session8_handoff/codex_deliverables/CODEX_RESEARCH_NOTE_PGRID_GAP2_2026_03_29.md)
- [CODEX_FORMAL_DRAFT_PGRID_LEMMAS_2026_03_29.md](/Users/saar/Documents/Codex reviewer/session8_handoff/codex_deliverables/CODEX_FORMAL_DRAFT_PGRID_LEMMAS_2026_03_29.md)
- [CODEX_INDEPENDENT_EXPLORATION_A_VS_DPRIME_2026_03_29.md](/Users/saar/Documents/Codex reviewer/session8_handoff/codex_deliverables/CODEX_INDEPENDENT_EXPLORATION_A_VS_DPRIME_2026_03_29.md)
