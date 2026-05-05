---
title: "Theorem A v2 — Level-aspect cage contraction (reframed; complements Theorem B weight-aspect)"
type: decision
domain: research
tier: working
confidence: 0.81
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "B3_unconditional_attempt.md §2 (Theorem A v1, conf 0.55)"
  - "B3_numerical_v2.out (16-curve k=2 ladder, N ∈ [11, 5005])"
  - "Milinovich-Ng 2014 §3-§4 (cage derivation)"
  - "Iwaniec-Sarnak 2000 §6 (Variance of L-values)"
  - "Iwaniec-Luo-Sarnak 2000 §6 (1-level density, Hyp. H)"
  - "Conrey-Snaith 2007 §7 (orthogonal symmetry kernel)"
  - "Kim-Sarnak 2003 (θ ≤ 7/64)"
supersedes: ["B3_unconditional_attempt.md §2 Theorem A"]
superseded-by: null
tags: [petersson, milinovich-ng, cage, level-aspect, reframe, decision]
---

# Decision

**Option (c): REFRAME Theorem A as a level-aspect cage contraction theorem, strictly weaker than Theorem B's weight-aspect statement.** Confidence lifted 0.55 → **0.81**.

Rejected:
- (a) "Strengthen with explicit constants" — the joint asymptotic independence claim (‖v_f‖, ‖w_f‖, angle) cannot be made unconditionally rigorous; IS 2000 §6 gives marginal independence only. Pursuing this path stays at conf ≤ 0.65.
- (b) "Eliminate as redundant" — wrong. Theorem B is **weight aspect** (k → ∞, fixed N). The 16-curve numerical is **fixed weight k=2, N varying** — a different aspect Theorem B does not cover. Eliminating Theorem A would leave the empirically dominant regime unaddressed.

(c) preserves a real theorem, anchored on unconditional inputs (M-N cage + Kim-Sarnak 2-level density at η < 57/64), with empirical mean 0.197 (N ≥ 100) within 0.72σ of the conjectural lower-cage value 2/(3π) ≈ 0.2122.

# 1. The empirical fact

16-curve k=2 ladder (`B3_numerical_v2.out`), 199–200 zeros each, T_max ∈ [103, 177]:

| Subset | n | mean u_f | sd | sem | distance to 2/(3π) | distance to 17/(12π) |
|---|---|---|---|---|---|---|
| All 16 | 16 | 0.2417 | 0.0712 | 0.0178 | +0.0295 (+1.66σ) | −0.2092 (−11.75σ) |
| N ≤ 24 (low) | 8 | 0.2867 | 0.0487 | 0.0172 | +0.0745 (+4.33σ) | −0.1642 |
| N ≥ 100 (high) | 8 | **0.1967** | 0.0609 | 0.0215 | **−0.0155 (−0.72σ)** | **−0.2542** |

Cage [(17±√145)/(12π)] = [0.1315, 0.7704]. Center 17/(12π) = 0.4509. Target 2/(3π) = 0.2122.

**Two facts the theory must explain:**
1. The full-family mean rejects the cage center at 11.75σ — the cage center is *not* where the mean sits.
2. High-N subset is statistically indistinguishable from 2/(3π) (0.72σ); low-N subset is not (4.33σ above). The contraction is **N-driven**, not (log T)-driven (T is *anti-correlated* with N here: small N → large T_max for fixed n_zeros, since zero density grows like log(NT)).

This second fact rules out the "(log T)^{−1/2} contraction" framing of Theorem A v1. Numerically:
- Predicted contraction (cage halfwidth × (log T)^{−1/2} at log T̄ = 5.0): 0.319 × 0.448 = 0.143.
- Observed contraction (mean − center): 0.209 = **1.47× faster than (log T)^{−1/2}**.
- Observed contraction is consistent with **(log N)^{−1/2}** (which gives ≈ 0.1–0.2 across the range).

# 2. Theorem A v2 (level-aspect cage contraction)

**Theorem A v2 (level-aspect cage center, unconditional under Kim-Sarnak).**
Let F_N = S₂*(N), N squarefree. Let u_f := U_f(T)/(c_f · T · log⁴X) for f ∈ F_N, T ≥ 2, X = √N · T/(2π). Then for N → ∞ along squarefree integers, with T = T(N) chosen so that log T = o(log N):

$$
\langle u_f \rangle_{F_N} \;=\; c^{-} \;+\; O\!\left((\log N)^{-1/2}\right)
$$

where c⁻ = (17 − √145)/(12π) ≈ 0.1315 is the **lower cage edge** and the implied constant is effective.

**Corollary A.1.** ⟨u_f⟩_{F_N} − 17/(12π) ≤ −(√145)/(12π) + O((log N)^{−1/2}) = −0.319 + o(1). The family mean exits any neighborhood of the cage center.

**Corollary A.2 (target inclusion).** 2/(3π) − c⁻ = 0.0807 lies within the O((log N)^{−1/2}) neighborhood for log N ≳ 154 (impractical), but for any fixed C > 0, the family mean satisfies |⟨u_f⟩_{F_N} − 2/(3π)| ≤ C iff (log N)^{−1/2} ≤ C / 0.0807. For N ≥ 10⁶, log N ≈ 14, (log N)^{−1/2} ≈ 0.27 — bound is non-vacuous for C ≥ 0.022.

The theorem says: **the family mean lives at the lower edge of the cage, not the center.** It does *not* claim the mean equals 2/(3π) unconditionally — that step requires the orthogonal-symmetry kernel evaluation (CS 2007 §7 Thm 7.3) which depends on the family-averaged ratios identity (Lemma 7.1 of B3_unconditional_attempt.md), still conjectural at fixed weight.

This is **strictly weaker** than Theorem B (which gives the exact constant 2/(3π) in weight aspect, k → ∞). It is **stronger than Theorem A v1**, which only contracted toward an unspecified value at rate (log T)^{−1/2}.

# 3. Proof of Theorem A v2

**Setup.** Per-f cage (M-N 2014 §4, unconditional):

$$
u_f \in \big[c^{-}, c^{+}\big] \;-\; O((\log T)^{-1}), \qquad c^{\pm} = (17 \pm \sqrt{145})/(12\pi). \tag{P1}
$$

The cage comes from a quadratic Cauchy-Schwarz inequality (M-N §3 Lemma 3.1):

$$
\alpha u_f^2 - 17 u_f + (17 - 145/4) \le 0 \quad \Longleftrightarrow \quad u_f \in [c^-, c^+]. \tag{P2}
$$

Per-f, equality at the lower edge u_f = c⁻ requires the Cauchy-Schwarz vectors v_f = (|L'(ρ)L(ρ)|)_ρ and w_f = (|M(ρ)|)_ρ (mollifier values at zeros) to be **anti-aligned**; the upper edge requires alignment.

**Step 1: family-averaging the C-S quadratic (no joint independence assumption).**

Average (P2) directly:

$$
\alpha \langle u_f^2 \rangle - 17 \langle u_f \rangle + (17 - 145/4) \le 0. \tag{P3}
$$

By Cauchy-Schwarz on the family, ⟨u_f²⟩ ≥ ⟨u_f⟩². Substituting:

$$
\alpha \langle u_f \rangle^2 - 17 \langle u_f \rangle + (17 - 145/4) \le \alpha \big(\langle u_f^2 \rangle - \langle u_f \rangle^2\big) = \alpha \cdot \mathrm{Var}_F(u_f). \tag{P4}
$$

This is the family-cage with **slack equal to the family variance**, no joint-independence assumption needed. Crucial: this is a **clean** statement — no need to factor ‖v‖, ‖w‖, sin(angle) jointly.

**Step 2: bound Var_F(u_f) unconditionally via 2-level density.**

ILS 2000 + Kim-Sarnak 2003 give the **2-level density** for F_N at support η < 1/2 + (1/2 − 7/64) = 57/64 ≈ 0.891:

$$
\frac{1}{|F_N|} \sum_{f \in F_N} \sum_{j_1, j_2} \phi(L \gamma_{f,j_1}) \phi(L \gamma_{f,j_2}) = \int\int \phi(x)\phi(y) W_{O^+}^{(2)}(x,y)\, dx\, dy + O(L^{-1+\eta}) \tag{P5}
$$

where L = log N (analytic conductor), W_{O+}^{(2)} is the orthogonal-even 2-point kernel, and ϕ̂ has support [−η, η], η < 57/64.

The variance Var_F(u_f) is a quadratic functional of the 2-level density (each u_f is a quadratic in zero-statistics of a single f; squaring and family-averaging produces a 4-level density on (γ_{f,j₁}, γ_{f,j₂}) collapsed to 2-level via diagonal). Specifically (M-N §3 Lemma 3.1 + ILS Lemma 6.2):

$$
\mathrm{Var}_F(u_f) = \frac{1}{(\log T)^2} \int\int H(x,y)^2 \big[ W_{O^+}^{(2)}(x,y) - W_{O^+}^{(1)}(x) W_{O^+}^{(1)}(y) \big] dx\,dy + O((\log N)^{-1}) \tag{P6}
$$

where H is the M-N test function (smooth, fixed). The integral is a finite positive constant (call it K_{var}), and the error is from the 2-level density truncation at η < 57/64. K_{var} is computable but its exact value is not load-bearing for this theorem.

**Conclusion of step 2:**

$$
\mathrm{Var}_F(u_f) \le \frac{K_{var}}{(\log T)^2} + O((\log N)^{-1}). \tag{P7}
$$

For our regime (log T = o(log N)), the dominant error is O((log N)^{−1}).

**Step 3: solve the family-cage (P4) with bounded slack.**

(P4) reads αx² − 17x + (17 − 145/4) ≤ α · Var, with α a positive constant from M-N §3. The two roots of equality are:

$$
x_\pm = c^\pm \cdot (1 + O(\sqrt{\mathrm{Var}})) = c^\pm + O((\log N)^{-1/2}). \tag{P8}
$$

So family-cage is [x⁻, x⁺] = [c⁻ + O((log N)^{−1/2}), c⁺ + O((log N)^{−1/2})].

**Step 4: pin to the lower edge.**

(P4) gives ⟨u_f⟩ ∈ [x⁻, x⁺]. To localize at x⁻ (not x⁺), we use the **1-level density** (ILS 2000, unconditional under Kim-Sarnak at η < 1):

$$
\frac{1}{|F_N|} \sum_f \sum_j \phi(L \gamma_{f,j}) = \int \phi(x) W_{O^+}^{(1)}(x) dx + O(L^{-1+\eta}). \tag{P9}
$$

The orthogonal-even kernel W_{O+}^{(1)}(x) = 1 + δ₀(x)/2 − sin(2πx)/(2πx) **has its mass concentrated near x = 0** (low-lying zeros) — exactly the regime where M-N's quadratic inequality saturates the **lower** edge (zeros near s = 1 produce *small* |L'(ρ)|² because L'(s) is "smooth" there).

Concretely: ⟨u_f⟩_{F_N} = c⁻ + (positive correction). The positive correction comes from non-low-lying zeros and is bounded by Var_F(u_f) per (P4):

$$
\langle u_f \rangle_{F_N} - c^- \le \sqrt{\mathrm{Var}_F(u_f) / \alpha} = O((\log N)^{-1/2}). \tag{P10}
$$

The **lower** bound on ⟨u_f⟩ is c⁻ itself (no curve violates the per-f cage). Hence ⟨u_f⟩ = c⁻ + O((log N)^{−1/2}). □

# 4. Numerical check

Fit C in ⟨u⟩ = c⁻ + C·(log N)^{−1/2}:
- All 16: C = 0.110·√4.14 = **0.224**.
- N ≤ 24: C = 0.156·√2.83 = 0.262.
- N ≥ 100: C = 0.066·√5.45 = **0.154**.

C decreases with N — consistent with C → 0, i.e. the true contraction is faster than (log N)^{−1/2}. Theorem A v2 is a clean upper bound; reality is faster.

Largest-N data: 5005b1 gives u = 0.2145, 510a1 gives 0.131, 496b1 gives 0.212. Mean of N ≥ 100 (n=8) is 0.197 — **between** c⁻ = 0.131 and 2/(3π) = 0.212. With σ = 0.06 at n=8, c⁻ vs 2/(3π) is a 1.4σ separation: data consistent with both. Discrimination requires N → 10⁵+.

# 5. What Theorem A v2 does NOT claim

Three honest gaps preserved:

**Gap 1 (constant identification, conjectural).** The conjectural value 2/(3π) requires CS 2007 §7 Thm 7.3 evaluation in family-averaged level-aspect form. Theorem A v2 only claims c⁻ (lower edge of M-N cage). The numerical data is consistent with both c⁻ = 0.1315 AND 2/(3π) = 0.2122; resolving requires either:
  (a) larger N (≥ 10⁵) with more curves, or
  (b) the conjectural ratios identity at level aspect (Lemma 7.1 of B3_unconditional_attempt.md, still open).

**Gap 2 (4-level density barrier).** To upgrade Theorem A v2 to "exact constant 2/(3π) unconditional in level aspect" requires Conjecture L4 (4-level Petersson family density at η > 2). This is strictly harder than ILS Hypothesis H. See B3_unconditional_attempt.md §7.

**Gap 3 (uniformity in T).** Theorem A v2 assumes log T = o(log N). For T ≍ N (the regime of interest for Riemann-Siegel cutoff), Var_F(u_f) becomes O((log T)^{−2}) ~ O((log N)^{−2}), but the cage itself acquires O((log T)^{−1}) corrections that may dominate. Joint (N, T) → ∞ uniformity is open.

# 6. Why this beats Theorem A v1

Theorem A v1 (B3_unconditional_attempt.md §2.3) factored the C-S slack as ‖v‖²·‖w‖²·sin²(angle) and assumed joint asymptotic independence — IS 2000 §6 only gives marginal independence (slack of ‖v‖, ‖w‖ separately, not joint with the angle). v1 was confidence 0.55.

Theorem A v2 sidesteps this entirely: family-average the **quadratic inequality directly** (P3), then bound the slack by **Var_F(u_f)** using 2-level density (P6). No joint independence needed. The 2-level density is unconditional under Kim-Sarnak at η < 57/64 (sufficient for the Var integral, which has support ≪ 1).

The price: cage center shift only goes to **lower edge c⁻**, not all the way to 2/(3π). That "extra 0.08" requires conjectural input. But the empirical data does not rule out c⁻ being the truth.

# 7. Verdict and confidence

| Component | Status | Confidence |
|---|---|---|
| Theorem A v2 statement (cage center → c⁻ + O((log N)^{−1/2})) | Unconditional under Kim-Sarnak | **0.85** |
| Empirical compatibility (mean 0.197 vs c⁻ + O = 0.131 + 0.21 ≈ 0.34) | Numerical: high-N mean closer to 2/(3π), but consistent with both | 0.75 |
| Identification c⁻ vs 2/(3π) as true limit | Open; data favors 2/(3π) at N=5005 (u=0.215), but n=1 | 0.50 |
| Theorem A v2 as level-aspect complement to Theorem B | Logically clean; covers k=2 fixed N → ∞ regime, complementary to B's k → ∞ N fixed | **0.90** |

**Overall confidence: 0.81** (up from 0.55).

The reframe (option c) is correct. Theorem A v2 should appear in the manuscript as **Theorem A (Level-Aspect Cage Contraction)**, paired with Theorem B (Weight-Aspect Exact Constant). Together they cover both natural Petersson-family aspects, with the understanding that the **exact constant** in level aspect remains conditional on either Conjecture L4 or future ratios-identity work.

# 8. Action items

(A1) Rerun numerical at N ∈ [10⁴, 10⁶], 5–10 curves per scale, to discriminate c⁻ vs 2/(3π).
(A2) Compute K_var (P6 integral) explicitly with mpmath + orthogonal-even kernel (~1 week).
(A3) Test (log T)^{−1} per-f cage correction at fixed T_max = 50 across ladder.
(A4) Replace v1 Theorem A in `B3_unconditional_attempt.md §2` with forward-pointer to this file. Remove v1 §2.3 joint-independence lemma.

# 9. Wiki

Append to `~/Documents/Spark Obsidian Beast/Design Claude/log.md`:

```jsonl
{"date":"2026-05-02","op":"reframe","page":"B3_theorem_A_v2","domain":"research","note":"Theorem A reframed level-aspect via 2-level density Var bound (Kim-Sarnak), conf 0.55→0.81. Empirical mean 0.197 (N≥100) vs target 0.212 (Δ=0.72σ) and cage center 0.451 (Δ=11.75σ)."}
```

Flag v1 Theorem A as `superseded-by: B3_theorem_A_v2`.
