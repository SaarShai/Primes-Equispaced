# Codex Analysis: Duality Identity at Zeta Zeros

**Date:** 2026-04-13  
**Agent:** ad89cd77bc0c5d125  
**Task:** 5 questions on P_K = c_K(ρ)·Q_K(ρ) → -e^{-γ_E}

---

## QUESTION A — Growth of Σ_{p≤K} p^{-ρ} at a zero ρ

**[PNT only]** Partial summation with π(u) = Li(u) + o(u/log u) gives:

S(K) = ∫₂^K u^{-ρ}/log u du + o(K^{1/2}/log K) = K^{1−ρ}/((1−ρ)log K) · (1+o(1))

So |S(K)| ≍ K^{1/2}/log K.

**[RH]** The RH error term π(u) = Li(u) + O(u^{1/2} log u) does NOT improve the leading size. After partial summation, that error contributes at most O((log K)²), negligible compared with K^{1/2}/log K.

**Codex conclusion**: Σ_{p≤K} p^{-ρ} has magnitude K^{1/2}/log K under both PNT and RH. No log log K cancellation from partial summation alone.

**CAVEAT** (Claude): This gives an UPPER BOUND from partial summation. The actual SIGNED sum Σ_p p^{-1/2}e^{-iγ log p} could be much smaller due to equidistribution of phases γ log p. The primes don't all align with the oscillation. This cancellation is NOT captured by partial summation against Li(u).

---

## QUESTION B — Behavior of Q_K(ρ)

**[Proved from A]** Main term from k=1: log Q_K ~ -Σ_{p≤K} p^{-ρ}. k=2 term: Σ_{p≤K} p^{-1-2iγ} converges to finite constant C_γ (oscillatory, bounded). k≥3: absolutely convergent.

If |Σ p^{-ρ}| ~ K^{1/2}/log K, then Q_K ~ exp(-CK^{1/2}/log K): super-exponentially small.

This would be INCONSISTENT with DRH(A), which requires Q_K ~ 1/log K.

---

## QUESTION C — Equivalence with DRH(A)

**[DRH]** Corrected DRH(A): Q_K(ρ)^{-1} ~ e^{γ_E} log K/ζ'(ρ), i.e. Q_K ~ e^{-γ_E}ζ'(ρ)/log K.

**[Proved]** Given c_K(ρ) ~ -(1/ζ'(ρ)) log K, the duality identity P_K → -e^{-γ_E} is algebraically equivalent to Q_K(ρ) ~ e^{-γ_E}ζ'(ρ)/log K = DRH(A). Strictly equivalent.

---

## QUESTION D — Unconditional proof

**[Conjectural]** No plausible unconditional route. The obstacle: k=1 term in log Q_K has PNT-scale magnitude K^{1/2}/log K. Any proof of P_K → -e^{-γ_E} would require controlling massive cancellation between c_K (size log K) and Q_K (apparently size exp(-K^{1/2}/log K)).

---

## QUESTION E — k=2 term and corrections

**[Proved]** For γ≠0: Σ_{p≤K} p^{-1-2iγ} = C_γ + K^{-2iγ}/(2iγ log K) + O(1/log²K). Only bounded oscillating constant — NOT log log K. Log log K divergence only at γ=0 (the real Mertens theorem). So k=2 does NOT rescue Q_K from super-exponential decay.

---

## THE FUNDAMENTAL TENSION

Codex identifies a genuine puzzle:

1. **Naive PNT estimate**: |Σ_{p≤K} p^{-ρ}| ~ K^{1/2}/log K → Q_K ~ exp(-CK^{1/2}/log K)
2. **DRH(A) requires**: Q_K ~ 1/log K (polynomial decay)

For DRH(A) to hold, Codex proposes three possible resolutions:

1. **[Conjectural]** Σ_{p≤K} p^{-ρ} has anomalous cancellation at the zero → true bound O(log log K). This would be a remarkable, very strong result.
2. **[Conjectural]** DRH is about a differently normalized Euler product (not the naive partial product).
3. **[Proved]** Duality identity as stated (naive Q_K) may be FALSE.

---

## CLAUDE'S RESOLUTION ATTEMPT

The partial summation K^{1/2}/log K is an UPPER BOUND on |Σ_p p^{-ρ}|, but the signed sum Σ_p p^{-1/2}e^{-iγ log p} has:
- Steps of size p^{-1/2} with OSCILLATING PHASES γ log p
- By Weyl equidistribution: phases γ log p are equidistributed mod 2π (for γ irrational)
- Random walk with variance Σ_p p^{-1} ~ log log K → typical size √(log log K)

So the TYPICAL SIZE of |Σ_{p≤K} p^{-ρ}| might be √(log log K), not K^{1/2}/log K. The partial summation bound is an upper bound that doesn't use equidistribution of primes.

**At a specific zero ρ**: there might be RESONANCE (unlike generic γ), giving a larger sum. This is the crux of DRH — understanding the prime sum at zeros.

---

## KEY OPEN QUESTION

**Does Σ_{p≤K} p^{-ρ} at a Riemann zero ρ have anomalous cancellation?**

- If YES (true order ~ log log K): DRH(A) is consistent, duality identity holds.
- If NO (true order ~ K^{1/2}/log K): DRH(A) fails for naive Euler product.

The numerical task M1_DRH_EULER_NUMERICAL will test this: compute Q_K for K up to 5000 and see if it decays like 1/log K or super-exponentially.

---

## STATUS

- Duality identity ≡ DRH(A) given Perron: **CONFIRMED** [Proved]
- Proof of duality identity: **OPEN** (requires DRH or anomalous cancellation result)
- Numerical test: **PENDING** (M1 task running)

