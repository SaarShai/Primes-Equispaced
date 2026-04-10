# Codex: Can the Theorem Be Unconditional?
# 2026-04-09

## VERDICT: NO. RH is the minimal hypothesis. Simple zeros can be dropped.

## Check Results

A. Divergence Σ p^{β-1} → ∞ for all β > 0: **PASS** (unconditional)
B. Explicit formula unconditional: **PASS** (truncation works without RH)
C. Multiple zeros strengthen resonance: **FAIL** — multiplicity m just multiplies coefficient by m, does NOT create (log N)^{m-1} factor in the standard -ζ'/ζ formula. (NOTE: Opus says it does for the M(x) formula which uses 1/ζ, not -ζ'/ζ. Need to reconcile.)
D. Error sum control without RH: **FAIL** — off-line zeros change coefficients c_j materially. The 0.10 bound is a critical-line estimate.
E. Clean isolation of one zero: **FAIL** — without RH, symmetric quadruples and off-line zeros can have comparable weight.
F. Functional equation reflection: **SUBTLE** — partner zeros at 1-ρ can reinforce or dilute.

## Key Takeaway
- The resonant sum diverges unconditionally (A passes) ✓
- The explicit formula is unconditional (B passes) ✓  
- Simple zeros can be dropped (changes coefficient only) ✓
- BUT: off-resonant interference control FAILS without RH (D, E fail) ✗
- Minimal hypothesis: **RH alone** (not RH + simple zeros)

## Disagreement: Opus vs Codex on multiplicity (C)
- Opus says: M(x) explicit formula gives x^ρ · P_{m-1}(log x) for multiplicity m → (log x)^{m-1} factor
- Codex says: standard -ζ'/ζ gives residue m, not (log x)^{m-1}
- Resolution needed: which explicit formula is relevant for M(x) = Σ μ(n)?
  M(x) uses 1/ζ(s), not -ζ'/ζ(s). For 1/ζ at a zero of order m:
  1/ζ(s) has a POLE of order m at ρ. Residue involves (s-ρ)^{-m} coefficient.
  So M(x) contribution IS x^ρ · polynomial in log x of degree m-1. OPUS IS CORRECT.

## Status for Paper J
Main theorem: **Under RH, F(γ_k)/F_avg → ∞ for each zero γ_k, regardless of multiplicity.**
This is the cleanest statement. Unconditional version remains open (off-line zeros problem).
