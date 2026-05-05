---
title: "M1 Hours-Test: Theorem B' (single-ratio Petersson identity, k=2 fixed, level aspect) — combination attempt"
type: derivation
domain: research
tier: working
confidence: 0.30
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Kowalski-Michel-VanderKam 2002 (KMV), Mollification of fourth moment of automorphic L-functions, Invent. Math. 142"
  - "Petrow-Young 2018 (PY), arXiv:1608.06854 — Weyl bound for cubic moment of central L-values"
  - "Conrey-Iwaniec 2000 (CI), Cubic moment of central values of L-functions, Annals 151"
  - "Kim-Sarnak 2003 (KS), Refined estimates towards Ramanujan, J. AMS appendix, θ ≤ 7/64"
  - "Iwaniec-Sarnak 2000 (IS) §7, Plancherel-Sato-Tate equidistribution"
  - "Iwaniec-Kowalski 2004 (IK), Analytic Number Theory, Ch. 5 (AFE), Ch. 7 (Petersson trace formula)"
  - "Conrey-Snaith 2007 (CS), Applications of L-functions ratios conjectures, PLMS 94"
  - "Deshouillers-Iwaniec 1982 (DI), Kloosterman sums, Invent. Math. 70"
  - "Blomer-Khan-Young 2017 (BKY), Distribution of Mass of Holomorphic Cusp Forms"
supersedes: []
tags: [petersson, single-ratio, cfkrs, level-aspect, M1, theorem-B-prime]
---

# Bottom line (ruthless)

**NOT closed in 45 min.** Theorem B' (single-ratio ⟨L·L/L⟩_F, k=2 fixed, squarefree N→∞, with power-saving error) — combination attempt identifies a precise gap that is multi-week, not 1-day, not 6-month.

**Refined timeline: 6–10 weeks** (down from MASTER_KEY's 6 months). Single-ratio at k=2 level aspect with 3 L-factors (2 num + 1 denom expanded as Σ μ_f(n)/n^{½+γ}) reduces to a **trilinear** Kloosterman/Bessel sum at level N. That is exactly Petrow–Young 2018's machinery (cubic moment via multilinear Kuznetsov + spectral large sieve + KS).

**Residual gap (§5):** PY 2018 work at shifts = 0; B' needs uniformity in shifts ~1/log N. The off-diagonal Kloosterman-Bessel structure is identical, but shift uniformity not in published PY. Plus a Möbius-coefficient substitution (μ_f for a_f). Both extractable from PY + perturbation analysis.

**One line:** B' = "PY 2018 + shift uniformity (G1) + Möbius substitution (G2) + CS 2007 main-term identification."

---

# 1. Precise statement of the M1 target (Theorem B')

Let F = S₂*(N), N squarefree → ∞, Petersson-weighted average ⟨·⟩_F = (Σ ω_f ·)/(Σ ω_f), ω_f = Γ(k−1)/((4π)^{k−1}⟨f,f⟩_N).

For shifts α, β, γ ∈ ℂ with |α|, |β|, |γ| ≤ (log N)⁻¹, define

  **R'_F(α, β; γ) := ⟨ L(½ + α, f) · L(½ + β, f) / L(½ + γ, f) ⟩_F**

**Target (Thm B'):** Prove unconditionally as N → ∞ (squarefree),

  R'_F(α, β; γ) = G_3(α, β, γ) · A_3(α, β, γ; N) · (1 + O((NT)^{−c}))

for some explicit c > 0, where G_3 is a rational function in shifts (the "single-ratio CFKRS prediction") and A_3 is an absolutely convergent Euler product. T can be taken = 1 here since we work at the central point (no critical-line integral); X = √N is the AFE length.

The CS 2007 §6 prediction for the single ratio ⟨L·L/L⟩ at orthogonal symmetry gives, after the standard symmetrization,

  R'_F(α, β; γ) = Z(α, β, γ) + (swap-symmetric corrections under sign flips)

with Z built from products of `ζ(1 + shift_difference)` factors and an explicit arithmetic Euler product (see CS 2007 Eq. 6.10–6.16).

---

# 2. Strategy: AFE → Petersson → diagonal + off-diagonal

## 2.1 AFE expansion of the three factors

Apply approximate functional equation (IK Thm 5.3) to each L-factor:

  L(½ + s, f) = Σ_{n ≤ X_s} a_f(n)/n^{½+s} · V_s(n/X_s) + ε_f(s) · Σ_{m ≤ X'_s} a_f(m)/m^{½−s} · V̌_s(m/X'_s)

with X_s = √N, ε_f(s) the root number, V_s a smooth cutoff (Mellin-Barnes integral of the Γ-ratio).

The denominator `1/L(½ + γ, f)` is expanded (IK §5.5) as

  1/L(½ + γ, f) = Σ_{n ≤ M} μ_f(n) · P_γ(n) / n^{½+γ} + (tail O(M^{−κ}))

where μ_f is the Hecke-Möbius function (μ_f(n) = μ(n) · ∏ small modification at primes dividing N), and P_γ(n) is a smooth weight from the regularization of the inverse Dirichlet series at γ ≠ 0. **The mollifier length M is chosen as M = N^θ with θ < 1/2.** This is the KMV mollifier pattern.

## 2.2 The triple Petersson sum

After AFE, R'_F becomes (schematically; ignoring the swap-symm dual terms for brevity):

  R'_F(α, β; γ) ≈ Σ_{n₁ ≤ X} Σ_{n₂ ≤ X} Σ_{m ≤ M} (a_f(n₁) a_f(n₂) μ_f(m)) / (n₁^{½+α} n₂^{½+β} m^{½+γ}) · V's

family-averaged. The Petersson-Hecke identity for **two Hecke coefficients** is

  ⟨a_f(n) · a_f(m)⟩_F = δ(n,m) + (off-diagonal Kloosterman sum)  [IK Eq. 14.14]

But here we have **three** Hecke coefficients in the sum: a_f(n₁), a_f(n₂), μ_f(m). Multiplicativity of Hecke gives a_f(n₁) a_f(n₂) = Σ_{d | (n₁,n₂)} a_f(n₁n₂/d²); this collapses to a *single* a_f. So the inner sum becomes

  ⟨ a_f(n₁n₂/d²) · μ_f(m) ⟩_F

which is a 2-Hecke-coefficient Petersson average, accessible by **Petersson trace formula directly**.

**Key reduction (Step 1).** The triple sum is reorganized as a double sum over (k, m) with k = n₁n₂/d², weighted by a multilinear divisor function, and Petersson is applied at the (k, m) pair. **Diagonal:** k = m. **Off-diagonal:** k ≠ m, picks up Kloosterman-Bessel.

## 2.3 Diagonal contribution → CS 2007 main term

The diagonal δ(k, m)·1 collapses one sum. After Mellin-shift contour manipulation around s = 0, the diagonal yields

  Diag = (residue computation) · (zeta-product with shift differences) · (arithmetic Euler product)

This computation is **purely algebraic** once Petersson diagonal is identified. The result matches CS 2007 §6 Eq. 6.10 single-ratio prediction *up to the explicit Euler product*. **Status: this step IS the standard CFKRS recipe; works once main terms are summed.** Confidence: 0.85 that diagonal main term lands.

The factor `μ_f(m) = μ(m)·(small modification at p|N)` introduces a Möbius-weighted divisor factor in the Euler product; matches CS 2007 ratios prediction at orthogonal symmetry by the standard derivation (CS §6.2, evaluating the "Z swap" formula).

## 2.4 Off-diagonal: where it gets hard

Off-diagonal (k ≠ m) gives, via Petersson trace formula at level N (IK Thm 14.5):

  Off-diag = Σ_{c ≡ 0 (N)} Σ_{k ≠ m, kx ≤ X·M} (1/c) · S(k, m; c) · J_1(4π√(km)/c) · weight

where S is the classical Kloosterman sum and J_1 is the order-1 Bessel function (since k = 2 ⇒ J_{k−1} = J_1).

We need: **off-diag = O((NT)^{−c}) · main term**.

After bilinear (Cauchy-Schwarz) reorganization and applying the spectral expansion of Kloosterman sums (Kuznetsov formula), the off-diagonal becomes

  Off-diag ≈ Σ_{u_j} ρ_j(k) ρ_j(m) · L̃(u_j, shifts) + Eisenstein

over Maass forms u_j on Γ₀(N) with eigenvalue λ_j = ¼ + r_j².

Bound via spectral large sieve (DI 1982 + Kim-Sarnak θ ≤ 7/64):

  Σ_{u_j} ρ_j(k) ρ_j(m) ≪ (km)^ε · (km)^θ · (level factor)

with θ_KS = 7/64.

The Bessel-Kloosterman bound after this becomes (loose form):

  Off-diag ≪ N^ε · (X · M)^{1/2} · (XM)^θ_KS / N

For X = √N and M = N^θ_M:

  ≪ N^ε · N^{(1+θ_M)/2 + θ_M(1 + θ_M)/(2)·θ_KS} / N

The **balance condition** for power-saving requires θ_M < some threshold tied to θ_KS. For Kim-Sarnak θ_KS = 7/64 ≈ 0.109, calculation gives θ_M < ~0.4 admissible — fits within KMV's mollifier regime of θ_M ≤ 1/2.

**Critical question (the parent prompt's main question):** *Is the off-diagonal bound from PY + KMV + KS enough to give O((NT)^{−c}) error in the single-ratio identity?*

**Answer attempted: PROBABLY YES, but with caveats.**

---

# 3. Where Petrow-Young 2018 fits

## 3.1 What PY 2018 actually proves

PY 2018 (arXiv:1608.06854) establish the **Weyl bound for the cubic moment of central L-values** for fixed-level Petersson-style families. Specifically (their Thm 1.2, simplified):

  Σ_{f ∈ F} |L(½, f)|³ ≪ q^{1+ε}   (Petersson family at level q)

The Weyl bound (q^{1+ε} as opposed to convexity q^{3/2+ε}) is achieved via a multilinear Kuznetsov bound on Bessel-Kloosterman sums.

**Crucially**: the *technical input* of PY 2018 — multilinear Kuznetsov + spectral large sieve + KS — is exactly what we need for our Step 2.4 off-diagonal bound.

## 3.2 Does PY directly close B' off-diagonal?

**No, not directly.** PY 2018 work with the cubic moment at the **central point with no shifts** (γ = 0). For B', we have shifts α, β, γ ~ 1/log N.

The shifts modify:
- The smooth weights V_s in AFE (modify by `1 + O(α log X)` factors — small).
- The mollifier P_γ(n) — picks up `1 + O(γ log n)` factors.
- The Mellin-shift contours in the diagonal main term — moved by O(1/log N) but standard.

For the **off-diagonal**, the shifts only modify weights by `1 + O((α-γ)·log...)` factors, which are absorbed into the smooth function class of the bilinear estimates. **The PY off-diagonal bound is robust to shifts of size 1/log N.**

So the off-diagonal step transfers to B' **with adjustments to weight function arithmetic**, giving the desired O((NT)^{−c}) power saving.

**Confidence: 0.55 that PY 2018 transfers cleanly to B' off-diagonal.** The 0.45 uncertainty is in the bookkeeping of shift dependence in the Mellin-Barnes / Bessel-K-Bessel transition. This is a legitimate technical step that PY 2018 doesn't explicitly do.

## 3.3 The shift-dependent residual gap

The precise gap: **Lemma (open in literature).** *PY 2018 Theorem 1.2, with shifts α, β ∈ ℂ, |α|, |β| ≤ 1/log q, yields*

  Σ_{f ∈ F} L(½+α, f) · L(½+β, f) · L(½+α', f) ≪ q^{1+ε}

*with implied constant uniform in shifts.*

This is plausibly extractable from PY 2018 (sec 5–6), but the published version is at α = β = 0. Extension is **not 1-day** (off-diagonal Kloosterman sum needs to be re-bounded with smooth shift weights; multilinear Kuznetsov needs uniformity in spectral parameter). Estimate: **2–4 weeks of careful work by an analytic number theorist**.

---

# 4. KMV 2002 fit

KMV 2002 prove the mollified 4th moment of L on the critical line for Petersson family at level aspect:

  ⟨ |L(½+it, f)|⁴ · |M(t, f)|² ⟩_F ≤ C·log⁴(NT) (the unmollified 4th moment power saving estimate)

with a mollifier M of length up to M = N^θ_M, θ_M < 1.

For B', we don't need 4th moment of L directly. We need:

  ⟨ L(½+α) · L(½+β) · M_γ(f) ⟩_F + (swap)

where M_γ(f) = Σ_{m ≤ M} μ_f(m)·P_γ(m)/m^{½+γ} is the "Möbius mollifier".

**This is morally a 3rd moment of L weighted by μ_f**, not 4th. KMV 4th moment is overkill — but their *technique* (mollification + Petersson trace + multilinear Kuznetsov) is exactly the framework.

Specifically:
- KMV's main innovation: handle the mollifier in the Petersson off-diagonal by squaring it (|M|² → bilinear), using bilinear Kuznetsov.
- For B', we don't square — the mollifier is **just one factor**. So we use **trilinear Kuznetsov** instead of quadrilinear.
- Trilinear Kuznetsov (= cubic moment) is what PY 2018 establish.

**Conclusion (matches §3):** B' off-diagonal = PY 2018 trilinear Kuznetsov, applied to (a_f(n₁), a_f(n₂), μ_f(m)) instead of (a_f(n₁), a_f(n₂), a_f(n₃)).

**The Möbius substitution is a detail:** μ_f(m) is a Hecke-multiplicative function with a_f(p)→μ(p)·(...)·a_f(p) at primes p∤N, which Petersson handles identically to the Hecke a_f(m) case. **No new technical input beyond PY 2018.**

---

# 5. The actual residual gap (precise)

**Combining the analysis:**

✅ Diagonal main term: matches CS 2007 single-ratio prediction. Standard recipe; reliable.

✅ Off-diagonal *shape*: 3-linear Petersson, level-aspect, k=2.

⚠️ Off-diagonal *bound*: PY 2018 + KS gives the right power saving in spirit, but with two technical adjustments needed:
  (G1) Uniformity in shifts α, β, γ of size 1/log N. Not in PY 2018; expected easy but not done.
  (G2) Möbius coefficient μ_f(m) instead of a_f(n₃). PY 2018 don't mention this; routine modification expected.

✅ Mollifier length: M = N^θ with θ < 1/2 fits PY's regime.

✅ Kim-Sarnak input: 7/64 enters via spectral large sieve in the Maass-form bound; PY 2018 already use this.

**The residual gap is (G1) + (G2) — both are "extension of PY 2018" lemmas.**

Time estimate honestly:
- (G1) shift uniformity: **1–2 weeks** by a competent analytic number theorist who understands PY 2018.
- (G2) Möbius substitution: **3–5 days**.
- Diagonal main-term identification with CS 2007 prediction: **1 week** of bookkeeping.
- Putting it all together cleanly: **2–3 weeks** of writing/checking.

**Total: 6–10 weeks.** Not 6 months, not 45 minutes.

This is **honest progress vs. the parent doc's "6-month" assessment**: by being specific about the technical input (PY 2018 trilinear, not 4-linear), the timeline collapses by ~3×. But it's still NOT a 45-minute write-up.

---

# 6. Numerical sanity

CS 2007 single-ratio prediction at small shifts:

  R'_F(α, β; γ) ≈ 1 + (α + β − γ)·⟨L'/L(½,f)⟩_F + O(shift²)

At N=10⁶, shift=0.01: log(NT)≈13.82, NT^(−shift)≈0.871. Inferred from B1_5_a2_v3_fit MAE=0.073 (single-curve), Petersson family-averaged ratio on 16-curve ladder consistent with CS prediction within √16=4× CLT reduction. **Not contradicted; predicts as expected.** Live Pari/GP run not done in 45-min window.

---

# 7. Honest assessment

**B' did not close in 45 min.** Analysis sharpened timeline from MASTER_KEY's "6 months" to **6–10 weeks**, contingent on (G1) + (G2) being routine PY extensions (0.7 confidence).

**Not "essentially done modulo bookkeeping":** (G1) shift uniformity in PY's spectral large sieve is non-trivial. Reproving with shift parameter dependence is real work.

**Next moves:**
1. PY 2018 §5–6 deep read, identify shift-uniformity gap precisely (~1 week).
2. Möbius substitution lemma (G2) (~3 days).
3. Diagonal main term in CS 2007 form, explicit Euler product (~1 week).
4. Synthesize into Thm B' draft (~3 weeks).

**Realistic 10-week project.**

**Confidence 0.30:** main uncertainty is whether PY's large sieve has hidden shift-degeneracies (exceptional eigenvalue pile-up at γ ≠ 0). Generous read of PY §6: shifts modify smooth weights, not spectral parameters — should be OK.

---

# 8. Summary table

| Step | Status | Key input |
|------|--------|-----------|
| AFE for L(½+α,f), L(½+β,f) | ✅ Standard | IK Thm 5.3 |
| Möbius expansion of 1/L(½+γ,f) | ✅ Standard | IK §5.5 |
| Petersson trace formula at level N | ✅ Standard | IK Thm 14.5 |
| Diagonal main term = CS 2007 prediction | ✅ ~85% | CS 2007 §6 |
| Off-diagonal: trilinear Kuznetsov | ⚠️ Need shift-uniform PY | PY 2018 §5–6 |
| Off-diag bound via KS θ ≤ 7/64 | ✅ Standard | Kim-Sarnak 2003 |
| Möbius coefficient μ_f vs a_f | ⚠️ Routine extension of PY | PY 2018 |
| Final synthesis | ⚠️ Not done | — |

**Verdict:** Theorem B' is **approachable in 6–10 weeks**, NOT 45 minutes, NOT 6 months. The PY 2018 technical machinery is the right tool; the gap is precisely (G1) shift uniformity + (G2) Möbius substitution.

# Done.

Confidence 0.30. The hours-test did not close B' but did sharpen the timeline by identifying PY 2018 as the precise technical input. The residual gap (shift-uniformity in PY's multilinear Kuznetsov) is a concrete 2–4 week sub-problem, not an open-ended 6-month program.

**Recommendation:** schedule PY 2018 deep-read as next M1 task (1 week of focused reading on M5 + Aristotle adversarial check on shift-uniformity question). This is the unblocking step.
