# Aristotle Submission: ratio_test + sign_theorem_conditional

**Date:** 2026-04-13
**Aristotle Job ID:** 51988806-f4cf-4688-9e8d-c66c6a7a7c97
**Status:** IN_PROGRESS (submitted, not waiting)
**Source project:** aristotle_results/f0e8f9af-1943-413e-a291-56f629741338/aristotle_submit_aristotle/

---

## What Was Submitted

Project directory: /tmp/ratio_test_submit (copy of the f0e8f9af project with modified SignTheorem.lean)

### Target 1 (PRIMARY): Close ratio_test sorry

```lean
theorem ratio_test (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (h : newDispSquaredSum p + shiftSquaredSum p ≥ dilution p) :
    deltaWobble p < 0 := by
  sorry
```

Located at SignTheorem.lean lines 115-118 (original) / ~250-260 in submitted version.

### Target 2 (SECONDARY): Add sign_theorem_conditional

New theorem requested:
```lean
theorem sign_theorem_conditional (p : ℕ) (hp : Nat.Prime p) (hp5 : 5 ≤ p)
    (hDS : newDispSquaredSum p + shiftSquaredSum p ≥ dilution p)
    (hB : crossTerm p > 0) :
    deltaWobble p < 0
```

---

## Mathematical Context

### The Algebraic Identity

The key identity connecting deltaWobble to the four-term decomposition:

Let A = wobbleNumerator(p-1), n = fareyCount(p-1), n' = fareyCount(p),
    cross = crossTerm(p), shift = shiftSquaredSum(p), newDisp = newDispSquaredSum(p).

```
deltaWobble p = A/n² - (A + cross + shift + newDisp)/n'²
             = (dilution - cross - shift - newDisp) / n'²
```

where dilution p = A*(n'²-n²)/n².

So: **deltaWobble p < 0 ⟺ cross + shift + newDisp > dilution**

### Why ratio_test May Be Hard

The hypothesis h: newDisp + shift ≥ dilution (≥, not >).
To get strict inequality for deltaWobble < 0, need one of:
- crossTerm p ≥ 0 (not always true: cross < 0 for p=5,7,11,17)
- h is actually strict (> not ≥)
- Additional lemma: newDispSquaredSum p > 0

The modified SignTheorem.lean submitted to Aristotle contains extensive inline commentary
explaining all three approaches and asking Aristotle to try them in order.

### Why sign_theorem_conditional Is Easier

With hB: crossTerm p > 0 as hypothesis:
  cross + shift + newDisp ≥ cross + dilution > dilution
This gives strict inequality directly. Aristotle should close this.

---

## Retrieve Result

```bash
~/.local/bin/aristotle result 51988806-f4cf-4688-9e8d-c66c6a7a7c97 \
  --destination ~/Desktop/Farey-Local/aristotle_results/51988806-f4cf-4688-9e8d-c66c6a7a7c97/
```

Then check: did Aristotle close ratio_test? Did it add sign_theorem_conditional?

---

## Next Steps

1. Wait for Aristotle result (typically 10-60 min)
2. Retrieve and check which sorries were closed
3. If ratio_test closed: integrate into main RequestProject/
4. If only sign_theorem_conditional added: that is still progress — it gives a
   clean conditional form of the Sign Theorem, proved from (DiscrepancyStep + B>0)
5. If neither closed: review Aristotle output for suggestions on missing lemmas

---

## Key Missing Lemma (if Aristotle fails)

The four-term decomposition lemma needed:
```lean
wobbleNumerator p = wobbleNumerator (p-1) + crossTerm p + shiftSquaredSum p + newDispSquaredSum p
```
This should be derivable from CrossTermPositive.lean (dispNewSquaredSum decomposition).
If this lemma is proved, the rest is field_simp + ring + linarith.

