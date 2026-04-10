# Session 8 Final Status — 2026-03-29

## Theorem: For all primes p ≥ 11 with M(p) ≤ -3: ΔW(p) < 0.

## What IS proved (rigorous):
1. ✅ Four-term decomposition (Lean-verified)
2. ✅ Permutation Square-Sum Identity: Σxδ = C/2 (proved + independently verified)
3. ✅ Deficit formula: D_q(2) = q(q²-1)/24 (pure algebra)
4. ✅ Deficit minimality: D_q(r) ≥ D_q(2) for all r (Dedekind reciprocity + permutation inequality)
5. ✅ C/A ≥ c/log²p unconditionally (from items 3+4 + PNT + Farey L² discrepancy)
6. ✅ El Marraki effective Mertens: |M(x)| ≤ 0.644x/logx for all x > 1
7. ✅ Sampling ratio → 2 asymptotically (Poisson summation / aliasing mechanism identified)
8. ✅ ΔW(p) < 0 for all 4,617 M(p)≤-3 primes to p=100,000 (computational)
9. ✅ B+C > 0 for all 210 M(p)≤-3 primes to p≈3000 (exact arithmetic, R always positive)
10. ✅ Lean: 8 lemmas proved + 3 Aristotle proofs, 3 sorry remaining (Finset plumbing)

## What IS NOT proved (the remaining gap):
- ❌ GAP 2: Non-circular effective bound on |1 - D/A| (or equivalently, effective ρ(p) ≥ 2-ε)
  - The asymptotic is proved (ρ → 2 via Poisson/aliasing)
  - The mechanism is understood (critical sampling doubles Farey energy)
  - But the Walfisz constant is INEFFECTIVE, preventing explicit P₀
  - ρ ≥ 0.37 proved unconditionally (insufficient — need ρ close to 2)

## Path to full closure:
1. Use Hurst (2018): |M(x)/√x| < 0.586 for all x ≤ 10^16
   → This makes the Poisson aliasing bound effective for p ≤ 10^16
2. Walfisz (ineffective but asymptotic) covers p > 10^16
3. Need to verify: does Hurst + Walfisz actually close the effective bound?
4. Alternative: push computational verification to p = 10^7 (reducing the gap)

## New discoveries this session:
1. Permutation Square-Sum Identity (N11)
2. B+C = -2ΣR·δ reformulation (Möbius/Kloosterman connection)
3. Deficit-Dedekind connection: D_q(r) = q(q-1)(q-2)/12 - q²·s(r,q)
4. Minimum deficit D_q(2) = q(q²-1)/24 (proved analytically)
5. D_q(2) minimality (proved via Dedekind reciprocity)
6. Σ D_new = -(p-1)/2 exactly (non-circular first moment)
7. Sampling ratio → 2 (Poisson/aliasing, critical sampling regime)
8. B+C < 0 at p=1399 (M=+8) — corrected scope of Sign Theorem
9. El Marraki effective Mertens bound found in literature

## Paper updates:
- Added Theorem (Permutation Square-Sum Identity) with proof
- Added El Marraki citation
- Corrected B+C scope (not universal, holds for M≤-3)
- Updated proof section with explicit constants
- Updated open problems with Kloosterman connection
