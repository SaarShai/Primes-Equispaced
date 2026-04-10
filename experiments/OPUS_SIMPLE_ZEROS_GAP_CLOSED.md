# Opus: Simple Zeros Gap — CLOSED
# 2026-04-09

## Verdict: Simple zeros hypothesis COMPLETELY REMOVED.

The theorem holds under RH alone (no simple zeros needed).

## Key Findings

### 1. Higher multiplicity = STRONGER resonance
- Simple zero (m=1): resonant sum ~ 2N^{1/2}/log N
- Double zero (m=2): resonant sum ~ 2N^{1/2} (log DISAPPEARS from denominator)
- Triple (m=3): ~ 2N^{1/2}·log N / 2
- Each multiplicity increase MULTIPLIES signal by ~log N

### 2. Error sum still converges with multiple zeros
- Off-resonant from ρ_j of multiplicity m_j: ~ (log N)^{m_j-1}/|γ_j-γ_k|
- Ratio: (log N)^{2(m_j-m_k)} / (N · |γ_j-γ_k|²) → 0 for each j
- Even if m_j > m_k: polynomial in log N vs N → still vanishes
- Unconditional multiplicity bound: m(ρ) = O(log γ) (Titchmarsh) — sufficient

### 3. F_avg unaffected by multiplicities
- F_avg controlled by primes (Parseval), not zeros
- Independent of zero multiplicities

### 4. Theorem under RH alone
THEOREM (RH): For any zero ρ_k = 1/2 + iγ_k of ζ(s), regardless of multiplicity:
F(γ_k)/F_avg → ∞ as N → ∞.
If ρ_k has multiplicity m_k ≥ 2, divergence is FASTER by (log N)^{2(m_k-1)}.

### 5. On going unconditional (no RH)
Much harder. Off-line zeros (β ≠ 1/2) change p^{-1/2} to p^{-β}.
The spectroscope is tuned to the critical line.
A generalized spectroscope with variable σ would be needed.
Opus recommends: state under RH for the paper, pursue unconditional separately.

### 6. Zero simplicity literature
- Levinson 1974: ≥ 1/3 of zeros are simple + on critical line
- Conrey 1989: ≥ 2/5
- Bui-Conrey-Young 2011: ≥ 41.05%
- Unconditional multiplicity bound: m(ρ) = O(log |γ|) (Titchmarsh)
- GUE statistics inconsistent with repeated zeros (probability 0)

## Impact on Paper J
Main theorem: RH only (not RH + simple zeros). Cleaner statement.
Multiple zeros only help. Cite Levinson/Conrey as aside.
