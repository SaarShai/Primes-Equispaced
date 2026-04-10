# Spectral Enhancement by Depth Filtering — Theorem (Opus, 2026-04-04)
## Status: CONDITIONAL (GRH + one heuristic gap)

## Theorem Statement

Under GRH with simple zeros, for the depth-filtered spectral sum
  S_L(p) = Σ_{a: c_m(a/p) ≥ L} D(a/p)·δ(a/p)

we have:
  S_L(p) = p^{-3/2} · Σ_k [T(L,γ_k)/(ρ_k·ζ'(ρ_k))] · p^{iγ_k} + E_L(p)

where T(L,γ) = Σ_{c≥L} c^{-(3/2+iγ)} and |E_L(p)| = O(p^{-3/2}·L^{-1/2}·log²p).

## Key Result: Low-Pass Filter Property

The depth filter suppresses higher spectral modes by factor F_k ≈ γ₁/γ_k:
- F_2 = 0.55 (γ₂ suppressed to 55%)
- F_3 = 0.41
- F_5 = 0.34

## Mechanism

Unfiltered: spectral coefficients involve ζ(3/2+iγ_k) which is BOUNDED and NON-DECAYING.
Filtered (L large): coefficients involve T(L,γ_k) ~ L^{-1/2}/√(1/4+γ_k²) which DECAYS as 1/γ_k.
Transition from non-decaying → decaying IS the low-pass filter.

## The One Gap

D(a/p) ≈ M(q_{m-1}) where q_{m-1} is penultimate convergent denominator.
This is well-motivated (fractions near a/p cluster around 1/q_{m-1} spacing) but NOT proved.
Making this rigorous requires: proving local Möbius sum near q_{m-1} dominates diffuse contributions.

## What IS rigorous
- Tail sum asymptotics T(L,γ) via Euler-Maclaurin: PROVED
- N(c,p) = p/(c(c+1)) + O(1) count of fractions with terminal quotient c: PROVED (p prime)
- Low-pass property F_k = γ₁/γ_k follows from the factorization: PROVED
- Only needs GRH, NOT LI (linear independence of zeros)

## Novelty
- Identification of S_L(p) as a spectral object: NEW
- Depth filtering gives additional 1/γ suppression beyond Mertens: NEW
- Mechanism (ζ(3/2+it) → tail sum): NEW
- Conditional on D ≈ M(q_{m-1}) gap: OPEN PROBLEM

## GAP VERIFICATION (2026-04-04 — computational check)

**D(a/p) ≈ M(q_{m-1}) is FALSE as a pointwise approximation:**
- corr(D, M(q_prev)) = 0.000 for p = 13, 19, 31, 43, 61
- Sign agreement: ~47% (random)
- For large c_m: |D·δ| >> |M(q)·δ| (ratio grows to 17-28x)

**BUT: Deep fractions DO dominate the sum:**
- p=31: c_m=31 alone → 73% of total Σ D·δ
- p=61: c_m=61 alone → 67% of total
- p=97: c_m=97 alone → 65% of total

**The theorem needs a DIFFERENT bridge:**
Not D(a/p) ≈ M(q_{m-1}), but rather:
- Direct spectral expansion of D(a/p) itself (not via M)
- The c_m = p fraction (which is 1/p or (p-1)/p) dominates because its δ = 1/p is large
- The depth-dominance is ALGEBRAIC (large c_m → large δ) not spectral

**Status: The low-pass filter mechanism may be correct but through a different route than D≈M.**

## ADVERSARIAL REVIEW VERDICT: FUNDAMENTALLY FLAWED (2026-04-04)

Codex adversarial review found 3 fatal problems:

1. **Bridge FALSE**: D(a/p) vs M(q_{m-1}) has zero correlation. Not a closable gap.
2. **Data WRONG**: "c_m=p contributes 65-73%" is incorrect:
   - c_m=p fraction is 1/p which has D(1/p)=0 ALWAYS → contributes ZERO
   - Actual dominant: c_m=p-1 → 44.6% at p=13, DROPPING to 17.5% at p=509
   - Single-fraction rescue FAILS (dominance decreases with p)
3. **Low-pass IMPRACTICAL**: T(L,γ) asymptotic correct but needs L >> γ² ≈ 1000.
   At practical L=5: F_5 = 2.92 vs predicted 0.43 (WRONG DIRECTION, 580% error).

**What survives:**
- T(L,γ) ~ L^{-1/2}/√(1/4+γ²) is mathematically correct (Euler-Maclaurin)
- ζ(3/2+it) does not decay (confirmed)
- The QUALITATIVE contrast between filtered (decays) and unfiltered (bounded) is real
- Depth-correlation r≈+0.65 is a real computational finding

**Salvage path:** Reformulate as statistical/computational observation only.
"Depth-filtered Farey sums show enhanced γ₁ coherence" — NOT a theorem.

**Lesson:** The blinded adversarial protocol caught what the prover and reviewer missed.
