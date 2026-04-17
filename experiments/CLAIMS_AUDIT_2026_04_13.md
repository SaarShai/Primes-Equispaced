# Claims Audit — Full Discrepancy Report
**Date:** 2026-04-13
**Agent:** Sweep agent (ad248cef3afa71d74)

## CRITICAL FIXES (7)

| # | Issue | Wrong | Correct | Files affected |
|---|-------|-------|---------|---------------|
| 1 | Lean count | 207/258/422 mixed | **434** | main.tex (422+258 internal contradiction), main 2.tex (207), M1_PAPER_C_*.md (422) |
| 2 | zeta'(rho_1) complex | 0.548+0.103i | Verify via mpmath; \|zeta'\|=0.793 | M1_PAPER_C_FULL_DRAFT.md (fabricated) |
| 3 | Phase phi_1 | -1.335 | **-1.6933** | M1_PAPER_C_FULL_DRAFT.md |
| 4 | Duality identity | c_K·Π(1-p^{-ρ}) | **c_K·Π(1-p^{-ρ})^{-1}** | MASTER_TABLE_INDEX.md DRH-1 |
| 5 | Interval certs | 300 | **800** | MASTER_TABLE_INDEX.md line 24 |
| 6 | Claude as co-author | Listed in main 2.tex | **Remove** (STM 2025) | main 2.tex line 44 |
| 7 | Computation range | 100K vs 200K | Verify which is real | main.tex vs main 2.tex |

## ADDITIONAL (3)
- main.tex zeta'(rho_1) comment: 0.783+0.125i → verify exact complex value
- "Franel tradition" vs "our terminology" → keep main.tex version (honest)
- DeltaW scaling: main 2.tex says p^{-1.77}, theory says p^{-2} → resolve with computation
