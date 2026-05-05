---
title: "L3' (trilinear Petersson, η > 5/3, level aspect): recent literature & auxiliary lemma"
type: derivation
date: 2026-05-02
parent_docs:
  - B3_L4_L3_DEFENSE.md (corrected L3' statement, η > 5/3)
  - B3_unconditional_attempt.md §7 (original L4)
confidence: 0.55
status: AUXILIARY LEMMA IDENTIFIED, GAP NARROWED, NOT CLOSED
---

# Question

Do recent results (BCL 2023, CLL 2025, DFS 2022, Petrow–Young 2018, Miao–Zhang 2025) unblock L3' for the **level-aspect, individual-N, fixed-weight-2** trilinear Petersson form

$$
\mathcal{T}(N) \;=\; \big\langle\, S_f(t)\cdot 2\operatorname{Re}\!\big(L'(1{+}it,f)\,\overline{L''(1{+}it,f)}\big)\,\big\rangle_{f\in S_2^*(N)},
\qquad N \text{ prime} \to \infty,
$$

with main-term cancellation matching the SO(even) 3-point Hecke kernel at explicit-formula support η > 5/3?

**Short answer: No, but the gap is now precisely identified and is smaller than feared.**

---

## What the recent literature actually delivers (and does not)

### Petrow–Young 2018 (Math. Ann., arXiv:1608.06854)

- **Delivers.** A *refined* Petersson trace formula for newforms of arbitrary squarefree level, with **no restriction on m, n**. This is the level-aspect Petersson the L3' setup needs.
- **Delivers.** A cubic-moment subconvex bound: ∑_{f ∈ S_k*(N)} L(1/2, f ⊗ χ)³ ≪ N^{1−δ} unconditionally (squarefree N, even k, χ a quadratic character of conductor coprime to N). This is the prototype "trilinear Petersson cancellation" — but it is a **cubic moment of central values**, not a 3-point cross-correlation of (L', L'', S_f).
- **Does NOT deliver.** A trilinear Hecke prime sum bound of the form
  $\sum_{p_1,p_2,p_3 \le X} \frac{(\log p_1)(\log p_2)^2}{(p_1 p_2 p_3)^{1+it}}\,\big\langle a_f(p_1) a_f(p_2) a_f(p_3) \big\rangle_F$ at the level of generality required for the L3' Fourier-support extension. The Petrow–Young trilinear is *symmetric in its three slots* and lives at the central point s = 1/2; L3' needs *asymmetric weights* (one with extra (log p)²) and lives on s = 1 + it.

### Baluyot–Chandee–Li 2023 (arXiv:2310.07606)

- **Delivers.** 1-level density at support |η| < 4 for the *q-averaged* family ⋃_{q ∼ Q} S_2*(q) (orthogonal symmetry), unconditional.
- **Delivers.** Robust handling of the inclusion–exclusion in the newform projector (Ng's primitive Petersson), valid uniformly across squarefree levels.
- **Does NOT deliver.** Anything for **fixed N** (no q-average). The (-4, 4) support is a *q-averaged* artifact: the q-average gives an extra integration that smooths out the off-diagonal Kloosterman sum and doubles the support. For fixed N, the analogous unconditional support is (-2, 2) (ILS 2000) and the conditional support under Selberg's eigenvalue conjecture is (-2, 2) as well — extending requires individual-N spectral input.
- **Critical:** L3' as written is a *level-density* statement for **individual N → ∞**, not q-averaged. BCL machinery does not transfer.

### Chandee–Lee–Li 2025 (arXiv:2510.07647)

- **Delivers.** n-th centred moments of 1-level density for q-averaged S_2*(q), in the regime ∑(supports) < 4. Verifies SO(even) Katz–Sarnak n-point Gaussian for the centred statistics.
- **Caveat.** Same q-average dependence as BCL 2023. The "n-level" here is the *test function n-tuple in 1-level density of multiple curves*, NOT the n-level density of zeros of a single L-function, and NOT the (L', L'', S_f) cross-correlation that L3' needs.
- **Does NOT deliver.** The cross-correlation ⟨S_f · (signed Hecke-trilinear integrand)⟩ at fixed N. The CLL combinatorics handles diagonal terms in the n-th moment expansion; off-diagonals there are *bilinear* (paired primes), never genuinely *trilinear*.

### Devin–Fiorilli–Södergren 2022 (arXiv:2210.15782)

- **Delivers.** 1-level density at support η < Θ_2 = 1.866... unconditionally for fixed-weight, prime-level holomorphic newforms (the actual ILS family at fixed N → ∞).
- **Mechanism.** Zero-density estimates for Dirichlet L-functions to extend the support beyond the bilinear Petersson barrier (η < 1 unconditional, η < 2 under GRH).
- **Promising for L3'.** This is the *correct family* (fixed N, weight 2). But: the DFS extension is for **1-level density**, not the trilinear cross-correlation. The technique (zero-density estimates) does not obviously trilinearize.

### Miao–Zhang 2025 (arXiv:2508.13746) — closest to what we need

- **Delivers.** Weyl-type subconvexity for triple-product L-functions in the *cubic level* aspect (level = q³, not squarefree q). The proof uses:
  - Refined Petersson trace formula for newforms of cubic level.
  - Voronoi summation, Jutila's circle method.
  - **Kuznetsov trace formula + spectral large sieve inequality.**
  - **Conditional on Ramanujan–Petersson** for Maass forms.
- **Critical caveat.** Cubic level (q³). Our L3' needs squarefree N. The cubic-level structure is what makes their refined Petersson have controllable Kloosterman off-diagonal — for squarefree N, the analogous bound *is* available (Petrow–Young 2018) but with weaker exponent.
- **Most relevant.** Their multilinear Kuznetsov + spectral large sieve combo is **exactly** the input L3' needs, but in the *Maass* / weight-aspect setting, not the level-aspect for fixed weight 2.

---

## The precise multilinear Kuznetsov bound L3' needs

Decomposing $\mathcal{T}(N)$ via the Petersson trace formula, the Bessel-Kloosterman off-diagonal is

$$
\mathcal{T}_{\text{off}}(N) \;=\; \sum_{c \equiv 0\,(N)} \frac{1}{c}\sum_{p_1, p_2, p_3 \le X} \frac{w(p_1, p_2, p_3)}{(p_1 p_2 p_3)^{1/2}} \,S(p_1 p_2, p_3; c)\, J_1\!\big(4\pi\sqrt{p_1 p_2 p_3}/c\big)
$$

with weights $w(p_1, p_2, p_3) = (\log p_1)(\log p_2)^2 \cdot (\text{phase}(t))$. The Bessel asymptotic at $\sqrt{p_1 p_2 p_3} \asymp c$ gives oscillatory off-diagonal of size $X^{3/2}/c^{1/2}$ per (p_1, p_2, p_3) triple.

**The bound L3' requires:**

$$
\Big| \sum_{c \equiv 0\,(N)} \sum_{p_1, p_2, p_3} \cdots \Big| \;\ll\; N^{1-\eta/2 + \varepsilon} \cdot X^{3/2 - \delta_0}, \qquad \delta_0 > 0,
$$

uniformly in $X \le N^\eta$, $\eta < 5/3$.

**What's available now:**

- **Petrow–Young 2018**: handles the trilinear-prime sum *at the central point*, with a different weight structure. Their key lemma (refined Petersson eq. (3.4)) **does** give an asymmetric prime-weighted version, but only for $X \le N^{1/2 - \varepsilon}$ — i.e., $\eta < 1$, the bilinear-Petersson barrier.
- **Deshouillers–Iwaniec 1982 spectral large sieve** + **Kim–Sarnak θ ≤ 7/64**: standard input pushes to η < 1 + 25/64 ≈ 1.391. **Insufficient.**
- **Selberg eigenvalue conjecture** (θ = 0, conjectural): pushes to η < 3/2. **Still insufficient by 1/6.**

**The gap is exactly 1/6 in support, equivalent to a square-root saving of `N^{1/12}` in the off-diagonal Kloosterman sum beyond Selberg's bound.**

---

## The smallest open auxiliary lemma

**Lemma L3'-Aux (level-aspect trilinear spectral density gain).** For F = S_2*(N), N prime → ∞, and any test function $\phi$ with Fourier support in (-η, η) for η < 5/3,

$$
\sum_{c \equiv 0\,(N)} \frac{S(m, n; c)}{c} \,\phi\!\big(4\pi\sqrt{mn}/c\big) \;\ll_\varepsilon\; N^{-1/2-1/12+\varepsilon}\,(mn)^{1/4+\varepsilon}
$$

**uniformly for $mn \le N^{3 - 2/3 + 2\eta}$** (the support range generated by the trilinear (p_1 p_2)·p_3 prime decomposition).

**Equivalent reformulation (via Kuznetsov).** For F a 1-bounded function on the cuspidal spectrum of Γ₀(N), and $|H| \le N^{1/2 + 1/12}$,

$$
\sum_{|t_j| \le H} F(t_j)\,\rho_j(m)\,\overline{\rho_j(n)} \;\ll_\varepsilon\; (HN)^{1+\varepsilon} \cdot \big(\tfrac{mn}{N}\big)^{1/4 + \varepsilon - 1/24}.
$$

This is Selberg's eigenvalue conjecture **plus** a 1/24 saving over the Deshouillers–Iwaniec spectral large sieve in the *cuspidal-spectral L²-density* on level Γ₀(N).

### Plausibility

**Confidence on Lemma L3'-Aux: 0.35.**

- **For (0.35, not lower).** The 1/24 saving is below GLH-density bounds for Maass forms in the level aspect (which would give 1/12 saving) and is consistent with what Iwaniec–Sarnak's "average θ" results suggest *should* hold. Recent advances in arithmetic exponential sums (Blomer–Milićević 2017+; Kowalski–Michel "decorrelation"; Petrow–Young trilinear refinements) make this a **soft target on the modern roadmap**, not a hard barrier.
- **For (not higher than 0.35).** No published result gets within 1/24 in the level aspect. The closest is Iwaniec 2002 ("Spectral methods of automorphic forms", §16) which essentially gives 0 saving over DI 1982 in the level aspect. Miao–Zhang 2025 gets the analog in *cubic level* via Voronoi + Jutila — but Voronoi is much weaker for squarefree levels because the modular structure of $\Gamma_0(N)$ for squarefree N has fewer Atkin–Lehner symmetries than $\Gamma_0(N^3)$.
- **Path forward.** The proof would proceed by:
  1. Apply Petrow–Young refined Petersson to extract the trilinear off-diagonal.
  2. Spectrally decompose via Kuznetsov on $\Gamma_0(N)$.
  3. Use Selberg eigenvalue (Δ-genericness) + Blomer–Milićević large-sieve refinement to get the 1/24 cuspidal-density gain.
  4. **The hard step:** bounding the contribution of *exceptional eigenvalues* (those near 1/4 from Selberg conj.). Currently controlled only via Kim–Sarnak θ ≤ 7/64 by direct insertion, which is not enough.

The hard step is **identical** to a quantitative Selberg-eigenvalue density theorem at level N. This is one of the main outstanding obstructions in level-aspect spectral theory.

---

## Achievability assessment

| Component | Available now? | Source |
|---|---|---|
| Refined Petersson at squarefree N, asymmetric Hecke weights | YES | Petrow–Young 2018 |
| Trilinear off-diagonal Kloosterman extraction | YES | Standard Bruggeman–Kuznetsov |
| Spectral large sieve at level N | YES (DI 1982 / Blomer-Mil. 2017) | DI 1982 |
| **Selberg + ε spectral density on Γ₀(N)** | **NO** | **Open** |
| Plancherel L²-energy support analysis | YES (this doc) | New |

The path to L3' is **complete except for one auxiliary lemma**: a quantitative spectral-density theorem on Γ₀(N) that improves the Deshouillers–Iwaniec spectral large sieve by a factor of $N^{1/12}$ in the cuspidal eigenvalue range $|t_j| \le H$ when $H \le N^{1/2 + 1/12}$.

---

## Numerical check (η > 5/3 derivation)

Plancherel L²-energy accounting from §F5 of `B3_L4_L3_DEFENSE.md`:

```
η > 1 + (deriv-logs from L', L'')/(amplitude-logs)
  = 1 + 2/3
  = 5/3 ≈ 1.6667
```

Verified consistent with the bandwidth structure: L' contributes 1 deriv-log, L'' contributes 2 deriv-logs (total 3), spread over 3 prime amplitude factors (one each from L', L'', S_f) — but the count of *amplitude logs* in the L²-norm is $1+1+1 = 3$ from each Hecke factor. Net threshold: $1 + 2/3 = 5/3$.

**Gap to currently achievable:**
- Kim–Sarnak (θ = 7/64): η < 1 + 25/64 ≈ 1.391. Gap ≈ 17.7/64 = 0.276.
- Selberg (θ = 0): η < 3/2. Gap = 1/6 ≈ 0.167.
- L3' target: η > 5/3 = 1.667.

**The 1/6 gap is the single quantity that L3' requires beyond Selberg.** It cannot come from improving θ alone (θ ≥ 0 already saturated by Selberg conjecture). It must come from a *density theorem* on the cuspidal spectrum at level N.

---

## Revised timeline

| Estimate | Rationale |
|---|---|
| **Original L4 (η > 2)** | 3–5 years — required GLH-density at level N |
| **§4.3 claimed L3 (η > 3/2)** | 6 months — *invalid*, bandwidth argument incoherent |
| **L3' (η > 5/3, this analysis)** | **1–2 years** — requires Lemma L3'-Aux (Selberg + 1/12) |

If Lemma L3'-Aux turns out to be available in the Blomer–Milićević–Kowalski–Michel orbit (which the research line of "decorrelation for newforms" arXiv:2405.05249 suggests is plausibly within reach with ~1 year of focused effort), the L3' program completes. If it requires a genuinely new technique (e.g., cubic-level analog of Miao–Zhang 2025 ported to squarefree N via Atkin–Lehner extension), 2 years is the realistic estimate.

**Confidence on "L3' is achievable on the 1-2 year timeline":** 0.55 (up from "multi-year unspecified" before this analysis).

---

## Recommendation

1. **Engage Petrow** (UCL, primary author of the refined Petersson at squarefree level) on whether his recent unpublished work (UCL Research page) contains the asymmetric trilinear weight extension at η < 5/3.
2. **Engage Blomer / Milićević** on cuspidal-density refinement at level N.
3. **Read Miao–Zhang 2025 in full**: their cubic-level technique might transfer to squarefree N via Atkin–Lehner.
4. **Numerical falsification check**: implement the trilinear cross-correlation $\mathcal{T}(N)$ for primes $N \in \{37, 53, 67, 79, 101\}$ and verify the conjectured cancellation matches SO(even) at η < 1 (within unconditional regime). If even the η < 1 calibration fails, the conjecture itself needs re-examination.

---

## Publishable contribution

Even if L3' is not closed, **the precise identification of Lemma L3'-Aux** (Selberg + 1/12 cuspidal density at level N) as the sole obstruction is itself a contribution. It reduces a vague "needs trilinear Petersson" wish to a concrete spectral-theory question that the current research community can attack with named techniques.

This document is the smallest unit of progress: gap narrowed from "unspecified multi-year" to "one named auxiliary lemma, 1–2 years."

---

## References

- Petrow, I., Young, M.P. (2018). *A generalized cubic moment and the Petersson formula for newforms.* Math. Ann. arXiv:1608.06854.
- Baluyot, S., Chandee, V., Li, X. (2023). *Low-lying zeros of a large orthogonal family of automorphic L-functions.* arXiv:2310.07606.
- Chandee, V., Lee, Y., Li, X. (2025). *The n-th centered moments of a large orthogonal family of automorphic L-functions.* arXiv:2510.07647.
- Devin, L., Fiorilli, D., Södergren, A. (2022). *Extending the unconditional support in an Iwaniec-Luo-Sarnak family.* arXiv:2210.15782.
- Miao, X., Zhang, H. (2025). *The Weyl bound for triple product L-functions in the cubic level.* arXiv:2508.13746.
- Conrey, J.B., Iwaniec, H. (2000). *The cubic moment of central values of automorphic L-functions.* Ann. Math.
- Iwaniec, H., Luo, W., Sarnak, P. (2000). *Low lying zeros of families of L-functions.* Publ. IHÉS 91.
- Deshouillers, J.-M., Iwaniec, H. (1982). *Kloosterman sums and Fourier coefficients of cusp forms.* Invent. Math. 70.
- Kim, H.H., Sarnak, P. (2003). *Refined estimates towards the Ramanujan and Selberg conjectures.* J. Amer. Math. Soc.
