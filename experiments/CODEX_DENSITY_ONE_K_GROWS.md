# Codex THINKING: Density-One Non-Vanishing with K=(log T)^A
**Date:** 2026-04-13
**Verdict:** K=(log T)^A does NOT work for any fixed A. S_j(K) is the real barrier.

## Main Finding: Nearest-neighbor term kills the approach

For K=(log T)^A:
- Main term: M_j = A log log T / ζ'(ρ_j)
- Perron error E: O((log log T)² / (log T)^{A/2}) → NEGLIGIBLE ✓
- Cross-term S_j: nearest-neighbor contribution ≍ (log T) / |ζ'(ρ_{j+1})|

Ratio |S_j| / |M_j| ≍ (log T) / (A log log T) → ∞ for ALL fixed A.

**No finite A works. Need K ~ T^θ (polynomial) to stand any chance.**

## The New Barrier [Conjectural]

S_j(K) = Σ_{n≠j} K^{i(γ_n−γ_j)} / ((γ_n−γ_j)ζ'(ρ_n))

is a discrete Hilbert transform of {1/ζ'(ρ_n)} with near-diagonal singular kernel.
Existing tech gives moment averages over j, NOT pointwise control.

Need: |S_j(K)| ≤ (1−η) A log log T / |ζ'(ρ_j)| on density-one zeros. MISSING.

## Hypotheses Status

| Claim | Status |
|-------|--------|
| RH + simple zeros: Perron residue formula valid | [Proved] |
| Density-one simplicity of zeros | [Conjectural] |
| Selberg density-one gap ≥ δ/log T | [Needs precise citation — averaged version only] |
| GH moments give pointwise S_j control | [Conjectural — averages only] |
| Uniform S_j cancellation o(log log T / \|ζ'\|) | [OPEN — this is the real problem] |

## What Is Publishable

Conditional theorem: "IF |S_j(K)| = o(log log T / |ζ'(ρ_j)|) on density-one zeros,
THEN |c_K(ρ_j)| > 0 for density-one zeros with K=(log T)^A and A large enough."

State the missing lemma cleanly. This is honest and of interest.

## Implication for Paper C

The density-one result is a CONDITIONAL THEOREM with explicitly stated missing ingredient.
Do NOT claim it as proved. Frame as: "density-one non-vanishing would follow from
cancellation in the Hilbert-transform-like sum S_j(K) — a new open problem."
