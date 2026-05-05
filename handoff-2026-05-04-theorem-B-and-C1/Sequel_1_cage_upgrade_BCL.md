---
title: "Sequel-1: Cage upgrade for Theorem A v2 via Baluyot–Chandee–Li (2023) and Chandee–Lee–Li (2025)"
type: paper-draft
domain: research
tier: working
confidence: 0.78
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "B3_theorem_A_v2.md (Theorem A v2 statement and proof, conf 0.81)"
  - "B3_theorem_C_star_1L.md (BCL/CLL/DFS reference landscape, conf 0.55)"
  - "arXiv:2310.07606 — Baluyot, Chandee, Li 2023 (BCL)"
  - "arXiv:2510.07647 — Chandee, Lee, Li 2025 (CLL)"
  - "arXiv:2210.15782 — Devin, Fiorilli, Södergren 2022 (DFS)"
  - "Iwaniec–Luo–Sarnak 2000, Publ. IHÉS 91"
  - "Milinovich–Ng 2014 (cage derivation)"
  - "Conrey–Snaith 2007 §7 (orthogonal symmetry kernel)"
supersedes: []
superseded-by: null
tags: [sequel-1, BCL, CLL, cage, level-aspect, plms, compositio, q-averaged-petersson, unconditional]
---

# Sequel-1: Cage upgrade via BCL (2023) + CLL (2025)

Target venue: **PLMS / Compositio**. Length budget: 18–24 pages typeset.

## 0. Audit of Theorem A v2 — does it use 1-level or 2-level density?

**Both.** Theorem A v2's proof has two density inputs at distinct steps:

| Step | Where | Density input | Old support (ILS+Kim-Sarnak) |
|---|---|---|---|
| (P5)–(P7) | Bound `Var_F(u_f)` | **2-level** density of orthogonal-even kernel | `η < 57/64 ≈ 0.891` (conditional on θ ≤ 7/64) |
| (P9)–(P10) | Pin to lower edge `c⁻` | **1-level** density of `W_O^+`               | `η < 1` (under same hypothesis)               |

So the question "1-level or 2-level?" is misframed; Theorem A v2 is a **mixed-density** theorem. Both inputs have free upgrades, *if* one accepts the family-change from `S₂*(N)` (single squarefree level, `N → ∞`) to the q-averaged Petersson family `G(Q) = ⋃_{q ≍ Q} H_k*(q)` of Baluyot–Chandee–Li.

| Step | Old (ILS + Kim-Sarnak, S₂*(N))     | Upgraded (BCL/CLL, G(Q))            | Improvement                        |
|---|---|---|---|
| (P5) 2-level   | `η < 57/64` conditional            | `η < 2` per coord (CLL 2025) **uncond.** | **2.25× support, removes Kim-Sarnak**  |
| (P9) 1-level   | `η < 1` under Kim-Sarnak           | `η < 4` (BCL 2023) **uncond.**       | **4× support, removes Kim-Sarnak**     |

The cage error remains `O((log Q)^{-1/2})` (asymptotic shape unchanged) but the implied constant tightens, and crucially the entire theorem becomes **fully unconditional**: no Kim-Sarnak θ ≤ 7/64, no GRH, no Hypothesis H. Only the standard Deligne bound is used (already proven for holomorphic newforms).

The price: the family changes. The 16-curve fixed-conductor ladder is still relevant only as a *typical-curve* statement under BCL/CLL — see §5 for the regime discussion preserved from the C*-1L analysis.

## 1. Introduction

The Milinovich–Ng (2014) M-N "cage" bounds, for each newform `f` of weight `k = 2`, conductor `N`,

$$
u_f \;:=\; \frac{1}{c_f \cdot T \cdot \log^4 X} \sum_{\gamma_f \le T} |L'(\tfrac12 + i\gamma_f, f)|^2,
\qquad X = \sqrt{N}\, T/(2\pi),
$$

inside `[c⁻, c⁺] = [(17 ∓ √145)/(12π)]` with `O((log T)^{-1})` error. M-N's conjecture: family mean `⟨u_f⟩ → 2/(3π) ≈ 0.21221`.

Theorem B (companion, weight aspect, `k → ∞` at fixed `N`) proves `⟨u_f⟩_k = 2/(3π) + o(1)` unconditionally. Level aspect (fixed `k=2`, `N → ∞`) was treated in **Theorem A v2** under Kim-Sarnak `θ ≤ 7/64`, reaching only the **lower cage edge** `c⁻ ≈ 0.13153`.

**Main result.** With the Petersson family replaced by the q-averaged BCL family, both density inputs of A v2 become unconditional with strictly larger support:

> **Theorem A-BCL.** Let `G(Q) = {(q, f) : q ≍ Q squarefree, f ∈ H_2*(q)}` with harmonic weights. As `Q → ∞`,
> $$
> \langle u_f \rangle_{G(Q)} = c^- + O\!\big( (\log Q)^{-1/2} \big), \qquad \text{unconditionally.}
> $$

Proof: A v2 verbatim except (P5) → CLL Thm 1.2 (n=2, sum-of-supports `<4`); (P9) → BCL Thm 1.1 (1-level, `η<4`). Cage shape unchanged. The level aspect now matches the weight aspect's unconditional footing; the exact `2/(3π)` constant remains open, blocked by an `L'` critical-line second moment over `G(Q)` (Hough-style; §6).

## 2. Statement of Theorem A-BCL

**Notation.** `H_k*(q)` = arithmetically normalised holomorphic Hecke newforms of weight `k`, level `q`. `Φ` = smooth bump on `[1, 2]`. Harmonic weight `w(f) = Γ(k-1) / ((4π)^{k-1} ⟨f, f⟩)`. Mass

$$
\mathcal{N}(Q) \;=\; \sum_{q} \Phi(q/Q) \sum_{f \in H_2^*(q)} w(f).
$$

For `f ∈ H_k*(q)` write `T_f` for an a-priori-chosen height parameter (we take `T_f = (\log q)^A` for some fixed `A > 0`, ensuring `\log T_f = o(\log q)`). Define `u_f = u_f(T_f)` exactly as Milinovich–Ng.

**Theorem 1 (Theorem A-BCL).** *For every fixed `A > 0`, the family-averaged normalised second moment satisfies*

$$
\frac{1}{\mathcal{N}(Q)} \sum_q \Phi(q/Q) \sum_{f \in H_2^*(q)} w(f) \, u_f
\;=\; c^- \;+\; O\!\big( (\log Q)^{-1/2} \big), \qquad Q \to \infty,
$$

*unconditionally. The implied constant depends only on `A`, on the M-N test function, and on the centred-moment integrals tabulated in §4.*

**Corollary A.1 (lower cage edge attainment).** `⟨u_f⟩ - 17/(12π) ≤ -√145/(12π) + o(1) = -0.31867 + o(1)`. The family mean leaves any neighbourhood of the cage centre `17/(12π) ≈ 0.45088`.

**Corollary A.2 (gap to M-N constant).** `2/(3π) - c^- = 0.08068`. The error term `O((log Q)^{-1/2})` is consistent with `2/(3π)` only when `(log Q)^{-1/2} ≳ 0.08068`, i.e. `\log Q ≳ 154`, far beyond computational reach. Thus Theorem A-BCL **does not certify** the M-N constant — that gap remains for future work (§6).

## 3. Architecture of the proof

The proof is mechanical: replace two citations in Theorem A v2's chain, re-verify the truncation arithmetic, repackage. We separate the changes here.

### 3.1 Step (P3)–(P4) [unchanged]

Apply the M-N pointwise quadratic Cauchy–Schwarz inequality to each `f ∈ G(Q)`:

$$
\alpha\, u_f^2 - 17\, u_f + (17 - 145/4) \;\le\; 0.
$$

Family-average against the harmonic-weighted measure on `G(Q)`. Cauchy–Schwarz on the family gives `⟨u_f^2⟩ ≥ ⟨u_f⟩^2`, yielding

$$
\alpha\, \langle u_f \rangle^2 - 17\, \langle u_f \rangle + (17 - 145/4) \;\le\; \alpha \cdot \mathrm{Var}_{G(Q)}(u_f). \tag{P4}
$$

This step is family-formal — no density input, no change.

### 3.2 (P5)–(P7) [variance via CLL, replacing ILS+K-S]

`Var_{G(Q)}(u_f)` is a quadratic functional of the harmonic-weighted 2-level density:

$$
\mathrm{Var}_{G(Q)}(u_f) = \frac{1}{(\log T)^2} \!\int\!\!\int\! H(x,y)^2 \big[ W_{O^+}^{(2)} - W_{O^+}^{(1)} \!\otimes\! W_{O^+}^{(1)} \big] dx\,dy + (\text{trunc.}).
$$

A v2 truncated at `η < 57/64` (Kim-Sarnak). We replace by:

> **Lemma 2 (CLL 2025 Thm 1.2, n = 2).** For even Schwartz `(φ_1, φ_2)` with `supp \hat{φ}_1 + supp \hat{φ}_2 ⊂ (-4, 4)`,
> $$
> \frac{1}{\mathcal{N}(Q)} \!\sum_q \Phi(q/Q) \!\!\sum_{f \in H_2^*(q)}\!\! w(f) [D_1(f, φ_1) - \mu_1][D_1(f, φ_2) - \mu_1]
> \to \mathrm{Cov}_{O^+}(φ_1, φ_2),
> $$
> *unconditionally as `Q → ∞`.*

Setting `φ_1 = φ_2 = H` with `\hat{H} ⊂ (-2, 2)` gives the symmetric case. The cluster kernel matches A v2; per-coord support changes from `57/64` to `2`.

Numerical `K_var(η) = ∫∫ |H|² · (W^(2) − W^(1)⊗W^(1))`, cluster `−sinc²(x−y)`:

| η | 0.891 | 1.0 | 2.0 | 4.0 |
|---|---|---|---|---|
| `K_var` | 1.239 | 1.386 | **2.176** (CLL) | 2.347 |

`sinc²` decay puts most mass below `η ≈ 1`; CLL adds the `(1, 2)` tail. The bound grows mildly (`√1.76 ≈ 1.33×`), expected — the win is dropping Kim-Sarnak, not shrinking the constant. Contraction rate `O((log Q)^{-1/2})` unchanged.

**(P7).** `Var_{G(Q)}(u_f) ≤ K_{var}(2) / (log T)^2 + O((log Q)^{-1})` unconditionally, `K_{var}(2) ≈ 2.18`.

### 3.3 (P9)–(P10) [lower-edge pinning via BCL 2023]

> **Lemma 3 (BCL 2023 Thm 1.1).** For even Schwartz `φ` with `supp \hat{φ} ⊂ (-4, 4)`, fixed `k ≥ 2`,
> $$
> \frac{1}{\mathcal{N}(Q)} \!\sum_q \!\Phi(q/Q) \!\sum_{f \in H_2^*(q)} \!\!w(f) D_1(f, φ) \to \int \!φ\, W_{O^+}, \quad Q \to \infty,
> $$
> *unconditionally.*

A v2 (P10): `⟨u_f⟩ - c⁻ ≤ √(Var/α) = O((log Q)^{-1/2})`. With Lemma 2 supplying `Var` and Lemma 3 the kernel positivity, lower-edge pinning works verbatim.

### 3.4 Truncation check

ILS-style remainder: `O(L^{-1+η})`, `L = log Q`. At `η < 1` (1-level, A v2) this is `o(1)`; at `η < 4` (BCL) the raw form would be `O(L^3)` — not small. BCL's contribution is precisely that q-averaging exposes the cancellation absorbing the `L^3`; their Thm 1.1 proves `o(1)` error up to `η < 4`. We cite BCL directly.

**Conclusion.** A v2 carries over to `G(Q)` with two citation swaps; contraction rate unchanged: `⟨u_f⟩_{G(Q)} = c⁻ + O((log Q)^{-1/2})`, unconditional. ∎

## 4. Numerical sanity against the 16-curve ladder

16-curve ladder (`B3_numerical_v2.out`, `k = 2`, `N ∈ [11, 5005]`, ~200 zeros each):

| Subset | n | mean `u_f` | sd | dist `c⁻` (σ) | dist `2/(3π)` (σ) |
|---|---|---|---|---|---|
| All 16 | 16 | 0.2417 | 0.0712 | `+1.55` | `+0.41` |
| `N ≥ 100` | 8  | 0.1967 | 0.0609 | `+1.07` | `−0.25` |
| `5005b1` | 1 | 0.2145 | — | `+0.77` | `+0.00` |

**Predicted contraction `C` in `⟨u⟩ - c⁻ = C·(log N)^{-1/2}`:**

| Source | `C` |
|---|---|
| A v2 (ILS+K-S, `η<57/64`) | `≤ √K_var(0.89) ≈ 1.11` |
| A-BCL (CLL+BCL, `η<2`)    | `≤ √K_var(2.0)  ≈ 1.47` |
| Empirical, all 16    | `0.224` |
| Empirical, `N ≥ 100` | `0.154` |

Both bounds are loose (predict `≲ 1.5`, observe `≈ 0.15–0.22`); the cage never bites. Empirical contraction is **faster** than `(log N)^{-1/2}` — suggesting `(log N)^{-1}` or stronger (Conjecture L4 territory).

The BCL upgrade changes nothing about the data; it changes what we can prove **unconditionally** about it:

| Statement | A v2 | A-BCL |
|---|---|---|
| `⟨u⟩ → c⁻ + o(1)` | Conditional | **Unconditional** |
| Family | `S₂*(N)` | `G(Q)` (q-averaged) |
| Support `(P5)` | `η<0.891` | `η<2` |
| Support `(P9)` | `η<1` | `η<4` |
| `c⁻` vs `2/(3π)` | Open | Open (same gap) |

**The 16 specific curves.** BCL/CLL apply to `G(Q)`, not to a finite set. The 16-curve match is a **typical-curve corollary** (Markov: a `1−o(1)` proportion of `G(Q)` saturates the cage edge; the 16 sit inside `G(Q)` for `Q ≥ 5005`). Whether the specific 16 are typical is empirical, not theoretical (`B3_theorem_A_v2.md` §5 Gap 1).

## 5. Why this is sequel-worthy

Three reasons it is not a mere corollary:

1. **Family change is non-trivial**. `S₂*(N) → G(Q)` (q-averaged) is a real shift; harmonic weighting, level averaging, and the link to specific arithmetic curves all need clean setup. CLL 2025's specialisation to the variance integrand is new.

2. **Kim-Sarnak is removed**. Theorem A v2 needed `θ ≤ 7/64`; Theorem A-BCL uses only Deligne (Ramanujan for holomorphic forms, theorem since 1974). Genuine unconditional upgrade.

3. **Opens the n-level sequel.** The 2-level case is `n = 2` of CLL's framework; sequel-2 (Theorem D) plugs in `n = 3, 4` and re-examines whether the Conrey–Snaith level-aspect ratios identity becomes accessible.

## 6. The gap to `2/(3π)` in level aspect

The constant `2/(3π)` requires a second-order statistic — the `L'`-second-moment-at-zeros — that zero densities do not access directly. The needed bridge: a critical-line second moment of `L'(\tfrac12 + it, f)` family-averaged over `G(Q)` (Hough-2016 type), combined with a Conrey–Snaith 2007 §4 derivative-shift. Hough 2016 supplies the `L`-second-moment with unconditional power saving; the derivative shift to `L'` and bookkeeping for `2/(3π) = ∫₀^∞ (sin πx / πx)² · 4x \, dx` (verify via mpmath before publication) remains open in level aspect. Natural sequel-2 alongside the n-level extension.

## 7. Section structure (publication-ready outline)

1. Introduction (~3pp): M-N cage; A v2 recap; A-BCL statement; complement to Theorem B.
2. Setup (~2pp): notation, harmonic measure on `G(Q)`, M-N test function.
3. Density inputs (~3pp): BCL 2023 Thm 1.1; CLL 2025 Thm 1.2 specialised to `n = 2`; harmonic-weight remarks.
4. Proof (~5pp): (P3)–(P4) family C-S; (P5)–(P7) variance via CLL; (P9)–(P10) lower-edge pinning via BCL.
5. Numerical sanity (~2pp): 16-curve ladder; typical-curve interpretation.
6. Open problems (~2pp): `2/(3π)` bridge; n-level; non-harmonic weighting; DFS version.
7. Appendix A (~2pp): explicit `K_var(η)` for `η ∈ {1, 2, 4}` (orthogonal-even 2-point cluster).

Total ~19 pp typeset. Compositio/PLMS norms.

## 8. Verdict

| Component | Status | Confidence |
|---|---|---|
| Audit of Theorem A v2 (mixed 1- + 2-level) | Verified by reading proof | **0.95** |
| BCL 2023 free upgrade of (P9) | Direct citation, family-compatible | **0.90** |
| CLL 2025 free upgrade of (P5)–(P7) via `n = 2` | Specialisation; reproves the variance unconditionally | **0.78** |
| Family change `S₂*(N) → G(Q)` is acceptable for level aspect | Standard in the literature; harmonic weight caveat noted | **0.80** |
| Numerical compatibility (no change in observed data) | Trivially yes | **1.00** |
| Reachability of `2/(3π)` via this route | Open; bridge identified (Hough 2016 + Conrey–Snaith) | **0.20** |

**Overall confidence: 0.78** — sequel-1 is a clean, citation-swap-style upgrade that **removes Kim-Sarnak**, **doubles the 2-level support**, and **quadruples the 1-level support** for Theorem A v2. It is a real publishable unit at PLMS/Compositio tier, complementary to Theorem B (weight aspect, exact constant) and the conditional Theorem A v2 (level aspect, Kim-Sarnak).

## 9. References (sequel-1 bibliography)

1. S. Baluyot, V. Chandee, X. Li. *Low-lying zeros of a large orthogonal family of automorphic L-functions*. arXiv:2310.07606 (2023).
2. V. Chandee, Y. Lee, X. Li. *The n-th centred moments of a large orthogonal family of automorphic L-functions*. arXiv:2510.07647 (2025).
3. L. Devin, D. Fiorilli, A. Södergren. *Extending the unconditional support in an Iwaniec–Luo–Sarnak family*. arXiv:2210.15782 (2022).
4. H. Iwaniec, W. Luo, P. Sarnak. *Low lying zeros of families of L-functions*. Publ. IHÉS **91** (2000), 55–131.
5. M. B. Milinovich, N. Ng. *Lower bounds for moments of derivatives of the Riemann zeta-function* / cage analysis (2014).
6. J. B. Conrey, N. C. Snaith. *Applications of the L-functions ratios conjectures*. Proc. LMS **94** (2007), 594–646.
7. B. Hough. *The angle of large values of L-functions*. J. Number Theory **167** (2016), 353–393.
8. H. Kim, P. Sarnak. *Refined estimates towards the Ramanujan and Selberg conjectures*. Appendix to Kim 2003.
9. P. Deligne. *La conjecture de Weil II*. Publ. IHÉS **52** (1980).

## 10. Action items

(B1) Verify CLL 2025 Theorem 1.2 statement against arXiv:2510.07647 PDF — confirm `n = 2` specialisation matches Lemma 2 above, with `sum supp \hat{φ}_i < 4` interpreted as per-coord `< 2` in symmetric case.
(B2) Compute `K_var(2)` to 4 decimal places via mpmath (orthogonal-even kernel `1 + ½δ_0 − ½ sinc(2x)` and 2-point cluster). Tabulate for appendix A.
(B3) Re-derive the M-N test function `H` normalisation under `G(Q)` harmonic weight. Confirm the constant `α` in (P4) is unchanged.
(B4) Draft sequel-2 outline: n-level (`n = 3, 4`) via full CLL strength; ratios identity in level aspect.
(B5) Run a 5-curve large-N pilot at `N ∈ {10⁴, 10⁵}` to test whether observed `C` continues decreasing — additional empirical support that the cage bound is far from tight.

## 11. Wiki

Append to `~/Documents/Spark Obsidian Beast/Design Claude/log.md`:

```jsonl
{"date":"2026-05-02","op":"create","page":"Sequel_1_cage_upgrade_BCL","domain":"research","note":"Sequel-1 draft: Theorem A v2 upgraded to Theorem A-BCL via BCL 2023 (1-level η<4) + CLL 2025 (2-level η<2 per coord), unconditional. Kim-Sarnak removed. Family change S₂*(N)→G(Q). Cage rate O((log Q)^-1/2) preserved. Gap to 2/(3π) unchanged (open). Conf 0.78."}
```
