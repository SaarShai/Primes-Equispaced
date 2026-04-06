# Lean 4 Audit — RequestProject/

**Date**: 2026-04-06
**Method**: Shell-only (ls, grep, wc). No Lean compilation attempted.
**Path**: ~/Desktop/Farey-Local/RequestProject/

## 1. File Listing

30 `.lean` files found (excluding .bak):

AbstractCauchySchwarz.lean, BPlusCFactorization.lean, BridgeIdentity.lean,
CWBound.lean, CauchySchwarzBound.lean, CharacterBridge.lean,
CrossTermPositive.lean, DAConvergence.lean, DeficitMinimality.lean,
DeltaCosine.lean, DenominatorSum.lean, DisplacementShift.lean,
EntropyMonotonicity.lean, FareySymmetry.lean, FourierModeExploration.lean,
GeneralInjection.lean, InjectionPrinciple.lean, MediantMinimality.lean,
MertensGrowth.lean, MulPPerm.lean, PermSum.lean, PermutationIdentity.lean,
PrimeCircle.lean, ShiftSumZero.lean, SignConj.lean, SignTheorem.lean,
SquareSumIdentity.lean, StrictPositivity.lean, SubGapPermutation.lean,
WeilBound.lean

## 2. Per-File Declaration Counts

| File | theorem | lemma | def | prop | corol | total |
|------|---------|-------|-----|------|-------|-------|
| AbstractCauchySchwarz.lean | 1 | 0 | 0 | 0 | 0 | 1 |
| BPlusCFactorization.lean | 0 | 0 | 0 | 0 | 0 | 0 |
| BridgeIdentity.lean | — | — | — | — | — | 26 |
| CWBound.lean | — | — | — | — | — | 10 |
| CauchySchwarzBound.lean | — | — | — | — | — | 2 |
| CharacterBridge.lean | — | — | — | — | — | 10 |
| CrossTermPositive.lean | — | — | — | — | — | 51 |
| DAConvergence.lean | — | — | — | — | — | 26 |
| DeficitMinimality.lean | — | — | — | — | — | 34 |
| DeltaCosine.lean | — | — | — | — | — | 9 |
| DenominatorSum.lean | — | — | — | — | — | 15 |
| DisplacementShift.lean | — | — | — | — | — | 15 |
| EntropyMonotonicity.lean | — | — | — | — | — | 6 |
| FareySymmetry.lean | — | — | — | — | — | 9 |
| FourierModeExploration.lean | — | — | — | — | — | 28 |
| GeneralInjection.lean | — | — | — | — | — | 11 |
| InjectionPrinciple.lean | — | — | — | — | — | 10 |
| MediantMinimality.lean | — | — | — | — | — | 9 |
| MertensGrowth.lean | — | — | — | — | — | 8 |
| MulPPerm.lean | — | — | — | — | — | 1 |
| PermSum.lean | — | — | — | — | — | 1 |
| PermutationIdentity.lean | — | — | — | — | — | 35 |
| PrimeCircle.lean | — | — | — | — | — | 16 |
| ShiftSumZero.lean | — | — | — | — | — | 3 |
| SignConj.lean | — | — | — | — | — | 6 |
| SignTheorem.lean | — | — | — | — | — | 48 |
| SquareSumIdentity.lean | — | — | — | — | — | 1 |
| StrictPositivity.lean | — | — | — | — | — | 15 |
| SubGapPermutation.lean | — | — | — | — | — | 13 |
| WeilBound.lean | — | — | — | — | — | 3 |

## 3. Grand Totals

| Category | Count |
|----------|-------|
| theorem | 266 |
| lemma | 93 |
| definition | 63 |
| proposition | 0 |
| corollary | 0 |
| **TOTAL** | **422** |

## 4. Sorry Audit

### Code `sorry` (non-comment):
1. `MediantMinimality.lean:116` — sorry in proof body
2. `SignTheorem.lean:86` — sorry in proof body
3. `SignTheorem.lean:141` — sorry in proof body

### Comment-only `sorry` (excluded):
1. `BridgeIdentity.lean:341`
2. `SignConj.lean:66`

## 5. Verdict

**The claim "258 results, zero sorry" does NOT hold.**

- Total declarations: **422** (not 258). Overshoot: +164.
- Theorem-only count: **266** (still not 258, overshoot +8).
- Code `sorry` count: **3** (not zero).

### Possible explanations:
- The 258 count may have been from an earlier snapshot of the codebase
- Some files may have been added after the 258 figure was established
- The sorry instances in SignTheorem.lean and MediantMinimality.lean need resolution

### Action items:
- [ ] Update paper to reflect actual count (422 or restrict to theorems: 266)
- [ ] Resolve 3 sorry instances or document them as open conjectures
- [ ] Re-verify after fixes

## VERIFICATION OF SORRY INSTANCES

All 3 sorry instances are inside block comments (`/- ... -/`):
1. MediantMinimality.lean:116 — inside `/- PROBLEM ... -/` block (documenting a FALSE statement)
2. SignTheorem.lean:86 — inside `/-- ... -/` doc comment (DISPROVED conjecture)
3. SignTheorem.lean:141 — inside `/- Original (false) statement: ... -/` block

**Zero sorry in actual compiled Lean code.** All three document FALSE statements.

## COUNT DISCREPANCY
Paper says 258 results. Audit finds 422 declarations (266 theorems, 93 lemmas, 63 definitions).
The 258 likely excluded definitions and counted only theorems+lemmas from an earlier snapshot.
**ACTION: Update paper to say "422 results" or clarify counting methodology.**
