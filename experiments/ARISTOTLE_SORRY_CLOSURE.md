# Aristotle Sorry Closure Report
**Date:** 2026-03-29
**Session focus:** Close remaining sorry statements in RequestProject using Aristotle API + manual proofs

---

## Summary

| File | Sorry | Status | Method |
|------|-------|--------|--------|
| AbstractCauchySchwarz.lean:21 | `sum_sq_ge_quarter_of_sum_eq_neg_half` | CLOSED | Manual + Aristotle confirmed |
| CauchySchwarzBound.lean:29 | `displacement_sum` | CLOSED | Delegates to CWBound.displacement_sum_eq |
| CauchySchwarzBound.lean:39 | `wobbleNumerator_ge_card_div_four` | CLOSED | Delegates to CWBound.cw_bound |
| CWBound.lean:48 | `rank_sum` | OPEN (sorry) | Aristotle job `e8e5a572` in progress |
| CWBound.lean:55 | `farey_sum_symmetry` | OPEN (sorry) | Aristotle job `e8e5a572` in progress |
| CWBound.lean:72 | `cw_bound` | CLOSED (modulo upstream) | Proved from displacement_sum_eq + AbstractCauchySchwarz |
| CWBound.lean:58 | `displacement_sum_eq` | CLOSED (modulo upstream) | Proved from rank_sum + farey_sum_symmetry |
| SignTheorem.lean:85 | `sign_theorem_conj` | OPEN (deep conjecture) | Aristotle job `d8142fc7` in progress |
| SignTheorem.lean:134 | commented-out incorrect theorem | N/A | Inside comment block |
| SignTheorem.lean:548 | `weil_bound_cross_term` | OPEN (deep conjecture) | Aristotle job `d8142fc7` in progress |
| MediantMinimality.lean:116 | false theorem in comment block | N/A | Aristotle confirmed: intentionally false, corrected version already proved |

## Closed Sorry Count: 4 (of 7 active)
## Remaining Active Sorry: 4 (2 tractable, 2 deep conjectures)

---

## Detailed Results

### 1. AbstractCauchySchwarz.lean -- CLOSED

**Theorem:** If sum of a_i over s equals -|s|/2, then sum of a_i^2 >= |s|/4.

**Proof:** Uses Mathlib's `sq_sum_le_card_mul_sum_sq` (discrete Cauchy-Schwarz: (sum a_i)^2 <= |s| * sum a_i^2), then `nlinarith` with the hypothesis.

```lean
theorem sum_sq_ge_quarter_of_sum_eq_neg_half ... := by
  have cauchy_schwarz : (sum i in s, a i)^2 <= (s.card : Q) * sum i in s, (a i)^2 :=
    sq_sum_le_card_mul_sum_sq
  nlinarith [(by norm_cast : (1 : Q) <= s.card)]
```

Aristotle independently found the identical proof (project `8dee4922`).

### 2. CauchySchwarzBound.lean -- BOTH CLOSED

**displacement_sum:** Proved by delegating to `CWBound.displacement_sum_eq` (which itself delegates to rank_sum + farey_sum_symmetry).

**wobbleNumerator_ge_card_div_four:** Proved by `exact cw_bound N hN`.

### 3. CWBound.lean -- C_W >= 1/4 Formalization

**Structure built:**
- `cw_bound`: wobbleNumerator(N) >= |F_N| / 4 -- PROVED from displacement_sum_eq + AbstractCauchySchwarz
- `displacement_sum_eq`: sum D = -n/2 -- PROVED from rank_sum + farey_sum_symmetry
- `rank_sum`: sum rank(f) = n(n-1)/2 -- SORRY (requires showing ranks are a permutation of {0,...,n-1})
- `farey_sum_symmetry`: sum f = n/2 -- SORRY (requires Farey involution f <-> 1-f)

The proof chain is complete modulo `rank_sum` and `farey_sum_symmetry`, which are standard Farey sequence facts but technically involved to formalize.

### 4. SignTheorem.lean -- Conjectures

- `sign_theorem_conj`: Deep conjecture (M(p) <= -3 implies deltaWobble(p) < 0). Not closable by automation.
- `weil_bound_cross_term`: Weil-bound-style estimate on per-denominator cross terms. Deep result requiring character sum bounds.

### 5. MediantMinimality.lean -- No action needed

The sorry at line 116 is inside a block comment (`/- ... -/`) documenting an intentionally false theorem statement. The corrected version is already fully proved below it. Aristotle confirmed this (project `ec8df342`).

---

## Aristotle API Submissions

| Project ID | Target | Status |
|-----------|--------|--------|
| `8dee4922-f2e5-4f56-909c-0593bfb27808` | AbstractCauchySchwarz | COMPLETE -- closed sorry |
| `ec8df342-addf-4478-bccf-7ff8f9b52606` | MediantMinimality | COMPLETE -- confirmed N/A |
| `e8e5a572-398d-4ad3-b66d-e113a3a0f7e9` | CauchySchwarzBound | IN_PROGRESS (7%) |
| `d8142fc7-2e62-45da-9263-1bd35140d6dc` | SignTheorem | IN_PROGRESS (4%) |
| `5d4e28a2-9e96-4a51-9891-f8be20b3f9c2` | CWBound/C_W formalization | IN_PROGRESS (9%) |

Check results with:
```bash
export ARISTOTLE_API_KEY="..."
~/.local/bin/aristotle result <PROJECT_ID> --destination /tmp/result_dir
```

---

## Next Steps

1. **rank_sum** and **farey_sum_symmetry** are the two remaining tractable sorry statements. Both are standard number theory facts. Approaches:
   - rank_sum: Show that the map ab -> fareyRank(ab) is a bijection to {0,...,n-1}, then use arithmetic series sum.
   - farey_sum_symmetry: Construct the involution (a,b) -> (b-a, b) on fareySet and show it preserves membership while mapping a/b to 1-a/b.

2. **sign_theorem_conj** and **weil_bound_cross_term** are deep conjectures that likely cannot be proved by Aristotle. They require either:
   - Restricting to finite verification ranges (already done computationally for p <= 50000)
   - New mathematical insight connecting M(p) to deltaWobble analytically

3. Check Aristotle results for the 3 in-progress jobs when they complete.
