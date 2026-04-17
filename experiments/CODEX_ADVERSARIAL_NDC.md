# Codex Adversarial Review: NDC Conjecture
Date: 2026-04-14
Tokens: 21,889

## VERDICT: Not publishable as stated (10 attack lines)

| Attack | Severity | Key Point |
|---|---|---|
| L(ρ) vs L'(ρ) notation | FATAL | Using L at a zero is nonsense; must be L' |
| Mathematical status dishonesty | FATAL | Computation ≠ proof; don't blur the line |
| Sample size (28 correlated pts) | SERIOUS | Same 4 trajectories, short 1/logK range |
| Richardson with oscillation | SERIOUS | 7 pts + visible oscillation = numerology |
| Character coverage | SERIOUS | Only 3 chars — all low conductor, low order |
| Wrong-zero precedent | SERIOUS | Shows verification pipeline was weak |
| Phase snapshot only | SERIOUS | arg<0.01 at one K, doesn't rule out slow rotation |
| Competing hypotheses incomplete | SERIOUS | Only 2 alternatives tested; space is large |
| GRH conditional unstated | SERIOUS | c_K ~ logK/L' requires GRH — say so |
| AK ratio 0.93 at K=5M | SERIOUS | 7% off is not "close to 1"; secondary needed |

## MINIMUM BEFORE SUBMISSION
1. Fix L(ρ) → L'(ρ) everywhere
2. State GRH-conditional explicitly throughout
3. More characters: higher conductor, genuinely different families, both parities
4. Certify zeros with numerical error bounds (we have |L|<5e-16 ✓)
5. Track arg(D_K) across all K values, show decay rate
6. Derive secondary correction term, show residual bias matches
7. Label every claim: proved / GRH-conditional / empirical conjecture
8. Replace "eliminated" with "not favored by this dataset"

## STRONGEST CLAIM DEFENSIBLE NOW
"For the tested zeros and K-range, D_K·ζ(2) is numerically close to 1 
and approximately real. This is consistent with D_K → 1/ζ(2) but 
does not establish it."

## NOTATION FIX NEEDED IN KOYAMA EMAIL
Check: everywhere we write E_K·logK → L'(ρ,χ)/ζ(2) — we use L' ✓
But the adversarial agent noted the original statement used "L(ρ)" 
which equals 0. Verify draft uses L'(ρ,χ) consistently.
