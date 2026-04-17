# API Overnight Queue — 2026-04-12

## STATUS: READY TO LAUNCH (do NOT start M5 yet — this is pre-staged)

---

## CODEX-1: DPAC Lower Bound — Uniform Approach
**Priority: HIGH** (Koyama interaction)  
**Mode: THINKING only, no file writes**  
**Subagent: codex:codex-rescue**

**Prompt:**
```
THINKING TASK — no code, pure mathematics.

We have c_K(s) = Σ_{k≤K} μ(k)k^{-s} (truncated Möbius Dirichlet polynomial).
Empirically: |c_K(ρ)| ≥ 4× larger at Riemann zeros ρ than at generic critical line points.

From Perron formula (VERIFIED): c_K(ρ) ~ log(K)/ζ'(ρ) as K→∞ for each fixed zero ρ.

QUESTION: Can we prove |c_K(ρ)| > f(K) > 0 for ALL nontrivial zeros ρ simultaneously (uniform lower bound)?

APPROACH 1 — Perron + error bounds:
c_K(ρ) = log(K)/ζ'(ρ) + E(K,ρ) where E = oscillatory sum over other zeros.
Main term dominates iff log(K)/|ζ'(ρ)| > |E(K,ρ)|.
Problem: |E| involves Σ 1/(|γ_j-γ||ζ'(ρ_j)|) summed over ALL zeros. Under GH moments this sum grows. For fixed K, eventually |E| > log K/|ζ'(ρ)| for bad zeros. What additional bound on ζ'(ρ) is needed?

APPROACH 2 — Counting argument:
c_K(s) is a Dirichlet polynomial of degree K. Its zeros on Re(s)=1/2 in [0,T] number at most N_c(T) = O(T log K) by Jensen/Langer. Zeta zeros: N(T) ~ T log T/2π. If c_K zeros and ζ zeros are "independent" (measure-zero intersection), DPAC would follow. But this is not rigorous.

APPROACH 3 — Product formula:
c_K(s) = Π_{p≤K} (1-p^{-s}) · (1 + Σ_{smooth n>K} μ(n)n^{-s}). The Euler product over primes ≤K vanishes at very specific s values. Are these compatible with ζ zeros?

APPROACH 4 — Algebraic independence:
The polynomial P(z_2,...,z_K) = 1 - z_2 - z_3 - z_5·... (with z_p = p^{-s}) evaluated at ζ zeros. Is P=0 possible? The values z_p = p^{-ρ} are algebraically constrained by ζ(ρ)=0. Can this constraint force P=0?

TASK: Think rigorously about each approach. Identify which is most promising. Find the key lemma needed. State what additional hypotheses (GRH, GH moments, Ramanujan conjecture, etc.) would make each approach work. Do NOT just say "under GRH this holds" — explain the mechanism precisely.
```

---

## CODEX-2: K=5 Zero Existence — Computational Strategy  
**Priority: MEDIUM**  
**Mode: THINKING only**  
**Subagent: codex:codex-rescue**

**Prompt:**
```
THINKING TASK — mathematical analysis.

c_5(ρ) = 1 - 2^{-ρ} - 3^{-ρ} - 5^{-ρ} where ρ = 1/2 + iγ is a Riemann zero.

We proved (by Kronecker equidistribution): there EXIST real γ (not necessarily Riemann zeros) where c_5(1/2+iγ)=0, because {(γ log 2/2π, γ log 3/2π, γ log 5/2π) mod 1} is dense in [0,1]^3.

So c_5 HAS zeros on Re(s)=1/2. The question is: do any of these coincide with Riemann zeros?

Known: the first 100 Riemann zeros γ_k have |c_5(ρ_k)| > 0 (can be numerically verified).

ANALYSIS:
1. What is the density of zeros of c_5 on Re(s)=1/2? By Jensen/Langer counting, c_5 has ~(5/2π) T zeros up to height T (since it's a Dirichlet polynomial of degree 5). Riemann zeros: ~T log T/2π. So c_5 zeros are MUCH SPARSER than ζ zeros.

2. Probability heuristic: if c_5 zeros and ζ zeros were independent, expected number of coincidences up to T is ~(5/2π)T · (1/mean spacing of ζ) · (1/density of c_5 zeros)... actually probability that a given ζ zero γ_k is also a c_5 zero: ~(5/2π)T / T = 5/2π per unit, mean gap between c_5 zeros ~ 2π/5 ≈ 1.26, mean gap between ζ zeros ~ 2π/log(T/2π). For T~14: gap ~3.7. So ζ zeros are sparser than c_5 zeros at first few. Later: c_5 zeros dominate.

3. For large γ: c_5 has ~γ/π zeros up to γ, ζ has ~γ log γ/2π zeros. Eventually c_5 zeros are DENSER than ζ zeros, so coincidences become plausible.

4. QUESTION: Is non-vanishing c_5(ρ_k) for FINITELY MANY vs ALL k an open question? Or is it expected that eventually c_5(ρ_k)=0 for some k?

Think carefully about the implications and whether non-vanishing of c_5 at ALL ζ zeros is provable, disprovable, or open.
```

---

## ARISTOTLE-1: Q-linear Independence of Log Primes  
**Priority: HIGH** (key lemma for K=5 proof)  
**API: ~/.aristotle_api_key**

**Goal:** Lean 4 proof that log 2, log 3, log 5 are Q-linearly independent.

**Lean statement:**
```lean
-- Q-linear independence of {log 2, log 3, log 5}
-- Equivalently: 2^a * 3^b * 5^c = 1 with a,b,c ∈ ℤ implies a=b=c=0
theorem log_primes_Q_independent :
    ∀ (a b c : ℤ), (2 : ℝ)^a * (3 : ℝ)^b * (5 : ℝ)^c = 1 → a = 0 ∧ b = 0 ∧ c = 0 := by
  sorry
```

**Proof sketch:**
- From 2^a * 3^b * 5^c = 1 (real powers, a,b,c ∈ ℤ)
- If a,b,c > 0: by unique factorization in ℤ, 2^a * 3^b * 5^c > 1 (contradiction)
- Handle negative exponents: clear denominators → 2^|a| * 3^|b| * 5^|c| = 2^{a'} * 3^{b'} * 5^{c'} with all non-negative → by FTA all exponents equal → a+a' = a', etc.

**Lean library hints:** Use `Nat.Coprime`, `Nat.Prime`, `Int.eq_zero_of_prime_pow_dvd_pow`, or number theory results in Mathlib.

**Context:** This is the key lemma showing that the Kronecker equidistribution argument in the K=5 non-vanishing proof requires genuine phase coincidence — {γ log p/2π mod 1} dense in [0,1]^3 — which forces the proof to use properties specific to Riemann zeros rather than arbitrary complex numbers.

---

## ARISTOTLE-2: c_K(ρ) Double-Pole Residue  
**Priority: MEDIUM**  
**API: ~/.aristotle_api_key**

**Goal:** Lean 4 formalization that the Perron formula residue at a double pole gives log(K).

**Statement:**
```lean
-- The residue of K^w / (w * ζ(s+w)) at a zero s=ρ of ζ is log(K)/ζ'(ρ)
-- Simpler algebraic version: residue of z^n log z at z=0
-- Or: if f has a simple zero at 0, then Res_{z=0} [g(z)/f(z)^2] = g(0)/f'(0)^2 - g'(0)/f'(0)
-- Applied to K^w/w at w=0 (giving log K) times 1/ζ(s+w) near w=0

-- Simplified: prove Res_{w=0} [log(K)^w / (w * (w * ζ'(ρ) + O(w²)))] = log(K)/ζ'(ρ)
theorem perron_double_pole_residue (K : ℝ) (hK : 1 < K) (ρ : ℂ) (hρ : riemannZeta ρ = 0) 
    (hρ' : deriv riemannZeta ρ ≠ 0) :
    -- The coefficient of 1/(w²) in K^w * (1/w) * (1/ζ'(ρ) * 1/w + higher) is log K / ζ'(ρ)
    True := by trivial -- placeholder
```

**Note:** This may be too hard for full Lean formalization. If so, prove just the algebraic residue computation: `Res_{w=0} [K^w / (w²)] = log K` using the Laurent expansion `K^w = 1 + w log K + O(w²)`.

---

## LAUNCH ORDER (morning)
1. Start M5 Max: `~/bin/compute_control.sh start`
2. Launch CODEX-1 (most important)
3. Launch ARISTOTLE-1 (independent)
4. Check M1 results, then CODEX-2 if needed
5. ARISTOTLE-2 is lowest priority — skip if time-limited

## DO NOT LAUNCH TONIGHT — wait for morning review of M1/M5 results first
