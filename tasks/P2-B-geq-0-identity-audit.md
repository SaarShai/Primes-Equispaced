# P2 — B≥0 Identity Audit: `B·n'²/2 = Bern − Saw` vs Original `B(p)`

**Target model:** Opus 4.7, **extra-high** reasoning mode.
**Repo root context:** `/Users/za/Documents/Farey NOW/primes-equispaced/` (this repo).
**Deliverable file:** `handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md`

---

## Goal (single sentence)

Determine whether the algebraic identity `B(p) · n'²/2 = Bern(p) − Saw(p)` claimed in the Bern/Saw decomposition is **TRUE** as an identity in `B(p)` as defined in [`CrossTermPositive.lean`](../handoff-2026-05-04-theorem-B-and-C1/CrossTermPositive.lean) and [`DisplacementShift.lean`](../handoff-2026-05-04-theorem-B-and-C1/DisplacementShift.lean), or whether the decomposition itself is algebraically wrong, in which case the `Bern(3299) < 0` finding is decomposition-bug, not a counterexample, and the B≥0 conjecture survives.

This single audit determines whether **Paper B's positivity claim** stands or falls.

---

## Context: why this audit matters

Per [`SESSION_SYNTHESIS_extra_high_round.md`](../handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md):

- Mikolas-Farey agent extended exact-rational numerical to p≤4999.
- **42 primes violate `|Saw(p)| ≤ Bern(p)`** (first failure p=1399, ratio reaches 7.05 at p=4889).
- **Bern(p) goes NEGATIVE at p ∈ {3299, 3301, 3307, 3319}** — exact rational verified at p=3299: `Bern = −0.11922733...`.
- Prior "Bern>0 via Chebyshev sum inequality" proof had an algebraic bug: silently used `Σf² = n/4`, but the actual value is `≈ n/3`.
- Confidence "B≥0 closes via Bern/Saw" was demoted **0.45 → 0.02**.
- Confidence "B≥0 itself true" was demoted **0.60 → 0.40**.

The audit must answer:

| Outcome | Implication |
|---|---|
| **Identity is BUGGY** | Decomposition wrong. `Bern(3299) < 0` is a decomposition artifact, not a `B(p)` counterexample. B≥0 conjecture (Mertens-restricted) survives. Paper B positivity claim survives. |
| **Identity is CORRECT** | `B(p) < 0` at `p = 3299` is a real counterexample. B≥0 conjecture (Mertens-restricted) **dies**. Paper B's positivity claim must be reframed as conjecture-with-evidence, not theorem. |

There is no third outcome. The audit is binary.

---

## Mandatory protocol (read before starting; embedded in deliverable)

1. **NO fabrication.** Quote `CrossTermPositive.lean` and `DisplacementShift.lean` verbatim with line numbers. Do not paraphrase the definitions. Same for any cited published result.
2. **Single confidence aggregation rule** stated at start of deliverable, never switched mid-document.
3. **Honest verdict.** State exactly which side of the binary outcome you land on.
4. **Cross-reference prior B_geq_0 files in the bundle** — read all of them before starting:
   - [`B_geq_0_IDENTITY_AUDIT.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_IDENTITY_AUDIT.md) — prior audit attempt
   - [`B_geq_0_v3_honest.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_v3_honest.md)
   - [`B_geq_0_FULL_CLOSURE.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_FULL_CLOSURE.md)
   - [`B_geq_0_dedekind_attack.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_dedekind_attack.md)
   - [`B_geq_0_extra_high_attempt.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_extra_high_attempt.md)
   - [`B_geq_0_hours_close.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_hours_close.md)
   - [`B_geq_0_mu_weighted_attempt.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_mu_weighted_attempt.md)
   - [`B_geq_0_petersson_attack.md`](../handoff-2026-05-04-theorem-B-and-C1/B_geq_0_petersson_attack.md)
   - [`Mertens_restricted_B_positivity.md`](../handoff-2026-05-04-theorem-B-and-C1/Mertens_restricted_B_positivity.md) — the Mertens-restricted version (the actual program claim)
5. **No Family-switching.** B(p) is the **Mertens-restricted** Farey four-term cross term, defined for `p` prime. Stay in this setting.

---

## Inputs and references

### Lean source (load-bearing — quote verbatim with line numbers)

- [`handoff-2026-05-04-theorem-B-and-C1/CrossTermPositive.lean`](../handoff-2026-05-04-theorem-B-and-C1/CrossTermPositive.lean) — original `B(p)` definition. Per [`C1_SELF_RESIDUE_HANDOFF.md`](../handoff-2026-05-04-theorem-B-and-C1/C1_SELF_RESIDUE_HANDOFF.md) §7, lines 41-45 contain:
  ```lean
  def crossTerm (p : ℕ) : ℚ :=
    2 * ∑ ab ∈ fareySet (p - 1), displacement (p - 1) ((ab.1 : ℚ) / ab.2) * shiftFun p ((ab.1 : ℚ) / ab.2)
  ```
  And lines 21-22 say:
  > "The cross term B is NOT nonneg for all primes (e.g., B(5) = −2/9, B(11) = −55/36). However, B IS strictly positive for every prime p with M(p) ≤ −3"
- [`handoff-2026-05-04-theorem-B-and-C1/DisplacementShift.lean`](../handoff-2026-05-04-theorem-B-and-C1/DisplacementShift.lean) — `displacement N f = rank(f) − |F_N|·f`, `shiftFun p f = f − {pf}` per lines 30-36.
- [`handoff-2026-05-04-theorem-B-and-C1/MertensDecomposition.lean`](../handoff-2026-05-04-theorem-B-and-C1/MertensDecomposition.lean) — Lemma 3.1: `B(p) = 2·B_0(p−1) − 2·S_ψ(p)` Lean-verified.
- [`handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean`](../handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean) — `Σ_{f ∈ Farey(p)} e^{2πipf} = M(p) + 2`.

### Existing Python audit scripts in the bundle

These already exist. Read first, then verify or extend:

- [`B_identity_audit_3299.py`](../handoff-2026-05-04-theorem-B-and-C1/B_identity_audit_3299.py) — exact-rational identity audit at p=3299
- [`bern_verify_3299.py`](../handoff-2026-05-04-theorem-B-and-C1/bern_verify_3299.py) — confirms `Bern(3299) < 0`
- [`bern_saw_extend.py`](../handoff-2026-05-04-theorem-B-and-C1/bern_saw_extend.py), [`bern_saw_extend_5k.py`](../handoff-2026-05-04-theorem-B-and-C1/bern_saw_extend_5k.py) — extension to p≤5000
- [`bern_saw_verify_failures.py`](../handoff-2026-05-04-theorem-B-and-C1/bern_saw_verify_failures.py) — verifies the 42 violating primes
- [`mertens_B_verify.py`](../handoff-2026-05-04-theorem-B-and-C1/mertens_B_verify.py), [`mertens_B_extend.py`](../handoff-2026-05-04-theorem-B-and-C1/mertens_B_extend.py)

### Required reading

- [`SESSION_SYNTHESIS_extra_high_round.md`](../handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) §"CRITICAL NEGATIVE RESULT: B≥0 conjecture in serious doubt"
- [`Mertens_restricted_B_positivity.md`](../handoff-2026-05-04-theorem-B-and-C1/Mertens_restricted_B_positivity.md) — what the actual program claim is (NOT B≥0 universal)

---

## Plan (step-by-step)

### Step 1 — read existing audit work

Read the existing `B_geq_0_*.md` and `B_identity_audit_3299.py` files. Report:
- What identity audits have already been attempted
- What conclusions were drawn and on what evidence
- Why a fresh audit is needed (e.g., prior audit didn't reach binary verdict; new evidence; different angle)

### Step 2 — quote the original `B(p)` definition verbatim

From `CrossTermPositive.lean` and `DisplacementShift.lean`:
- Quote `crossTerm` definition with line numbers
- Quote `displacement` and `shiftFun` definitions with line numbers
- State `B(p) := crossTerm(p)` explicitly
- Tabulate `B(p)` for `p ∈ {2, 3, 5, 7, 11, 13, ...}` to ≥30 primes by **direct evaluation** of the Lean definition translated to exact-rational Python (using `fractions.Fraction`). Cross-check against any tabulated `B(p)` values in the prior audit files.

### Step 3 — state the claimed identity

From the Bern/Saw decomposition (cite the source file in the bundle that introduced it):
- Quote the claimed identity `B(p) · n'²/2 = Bern(p) − Saw(p)` verbatim
- Quote the definitions of `Bern(p)` and `Saw(p)` verbatim
- State `n' := p - 1` (verify this is the convention used)

### Step 4 — symbolic identity verification

In sympy with **exact rationals**:
- Symbolically expand `B(p) · n'²/2` for prime `p` symbolic in a pre-fixed regime (e.g., for general `p` symbolic, or for `p` in a class large enough to be representative)
- Symbolically expand `Bern(p) − Saw(p)` similarly
- Compute the symbolic difference. If it is identically zero, identity is TRUE in that regime; else, identity is FALSE and the difference itself is the "bug term."

If a fully symbolic expansion is intractable, use numerical at 30+ digit precision via mpmath (sympy's `nsimplify`) at p ∈ {primes from 2 to 5000}.

### Step 5 — exact-rational direct comparison at every prime up to 5000

For every prime p ∈ {2, 3, 5, ..., 4999}:
- Compute `lhs(p) = B(p) · (p-1)² / 2` from the Lean definition
- Compute `rhs(p) = Bern(p) − Saw(p)` from the bundle's existing `bern_saw_extend_5k.py` or equivalent
- Both as `Fraction`
- Tabulate `delta(p) = lhs(p) − rhs(p)` exactly

If `delta(p) = 0` for ALL p tested → identity holds numerically; combined with Step 4 symbolic, identity is TRUE.

If `delta(p) ≠ 0` for any p → identity is BUGGY. Report the smallest counterexample and the size/structure of the discrepancy.

### Step 6 — diagnostic on the bug (if Step 5 finds delta ≠ 0)

If identity is buggy:
- Inspect the algebraic derivation of the identity in the source doc that introduced it
- Identify the wrong step (most likely candidates per `SESSION_SYNTHESIS`: `Σf² = n/4` was used vs actual `≈ n/3`; or a sign error; or a Cauchy-Schwarz equality assumption that doesn't hold)
- Quote the wrong step with file+line reference
- Propose the corrected identity if there is one (or state no clean correction exists)

### Step 7 — verdict on `B(p)` positivity at p=3299 specifically

Independently of the identity:
- Compute `B(3299)` directly from the Lean `crossTerm` definition, in exact rational arithmetic via Python `fractions.Fraction`
- Report the value
- If `B(3299) ≥ 0`: the Mertens-restricted B≥0 conjecture **survives at p=3299** regardless of the identity status (note: 3299 must satisfy `M(3299) ≤ −3` for the conjecture to apply; check this and report)
- If `B(3299) < 0`: the conjecture **fails at p=3299**, which is a counterexample even without the Bern/Saw framing

### Step 8 — final binary verdict

Combine Steps 5 and 7 into one of the four logical cases:

| Step 5 verdict | Step 7 verdict | Overall verdict |
|---|---|---|
| Identity TRUE | `B(3299) ≥ 0` and `M(3299) ≤ −3` | **B≥0 SURVIVES** at 3299; Bern/Saw decomposition correct; the prior `Bern(3299) < 0` finding implies a different prime triggers the constraint, OR `M(3299)` may not be ≤ −3 (check `M(3299)`) |
| Identity TRUE | `B(3299) < 0` and `M(3299) ≤ −3` | **B≥0 DIES** — direct counterexample |
| Identity BUGGY | `B(3299) ≥ 0` (with `M ≤ −3`) | **B≥0 SURVIVES** — Bern/Saw decomposition was wrong, no longer a refutation route |
| Identity BUGGY | `B(3299) < 0` (with `M ≤ −3`) | **B≥0 DIES** even without the Bern/Saw framing |

Pick the row, state it.

---

## Deliverable specification

Single Markdown file at `handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md` with sections:

1. **Confidence aggregation rule** — stated once
2. **What prior audit work in the bundle established and what is still missing**
3. **Verbatim Lean definitions** (`crossTerm`, `displacement`, `shiftFun`) with line numbers
4. **Verbatim claimed identity** with file+line of original derivation
5. **Symbolic identity verification** — sympy result, identically zero or counterexample
6. **Exact-rational table** — `delta(p)` for primes p ≤ 5000, smallest counterexample (or all zero)
7. **Bug diagnostic** (if identity buggy) — wrong step located and quoted
8. **Direct B(3299) evaluation** — value, with `M(3299)` and Mertens-restricted check
9. **Final binary verdict** — exactly one of the four matrix outcomes from Step 8
10. **Companion files** — `B_geq_0_identity_audit_FINAL.py`, exact-rational extension to p=5000, raw output

---

## Done when

- File exists at the specified path
- All 10 sections present
- Lean definitions quoted verbatim with line numbers
- Symbolic AND exact-rational verification both completed (or symbolic explicitly skipped with justification)
- `B(3299)` directly computed from Lean definition, value reported
- Final binary verdict is one of the four matrix cells stated explicitly
- Python script saved as companion file with reproducible output

## Stop and report immediately if

- `CrossTermPositive.lean` or `DisplacementShift.lean` cannot be parsed (path or syntax issue) — do not invent definitions
- Direct Python translation of the Lean `crossTerm` definition disagrees with any prior tabulated `B(p)` value — flag and stop until the discrepancy is resolved
- The claimed `B(p) · n'²/2 = Bern − Saw` identity cannot be located in any source file in the bundle (the Bern/Saw framing may have been informal; flag this as the audit verdict directly: "identity was never written down, treat as folklore, do not depend on it")
- Exact-rational arithmetic returns floats (i.e., overflow / type coercion bug) — fix before reporting
- ANY citation cannot be verified — flag `UNVERIFIED`

Do **not** publish a verdict if any of the above triggered and is unresolved.
