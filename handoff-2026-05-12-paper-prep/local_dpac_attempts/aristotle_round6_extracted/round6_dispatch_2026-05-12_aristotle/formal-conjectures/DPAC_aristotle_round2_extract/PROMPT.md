# Aristotle dispatch: close the two remaining `sorry`s in DPAC_full.lean

This is the Dirichlet Polynomial Avoidance Conjecture (DPAC) Lean file.
There are two remaining `sorry`s at lines 164 and 314. Please close them
or report the missing Mathlib prerequisite.

## Context

The earlier `dpac_of_LI` bridge was tombstoned because Linear Independence
of zeta-zero ordinates does not by itself control the finite log-prime
phase vector in the truncated Mobius polynomial. The file now names
explicit phase-avoidance bridge layers; the two remaining `sorry`s are
algebraic/probabilistic steps inside those bridges.

## Protocol

- NO `axiom`. If unclosable in Mathlib v4.28.0, leave as `sorry` with a
  comment naming the missing Mathlib lemma or research-open content.
- Preserve every other theorem in the file. Only edit the two `sorry`
  bodies. If you make progress on one but not the other, ship that.
- The file is the DPAC PR #3716 to `google-deepmind/formal-conjectures`.
