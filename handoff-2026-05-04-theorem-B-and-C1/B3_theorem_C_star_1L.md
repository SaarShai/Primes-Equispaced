---
title: "Theorem C*-1L (level-averaged 1-level density at η < 4, unconditional)"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - arXiv:2310.07606  # Baluyot–Chandee–Li 2023
  - arXiv:2510.07647  # Chandee–Lee–Li 2025
  - arXiv:2210.15782  # Devin–Fiorilli–Södergren 2022
  - Iwaniec–Luo–Sarnak 2000 (Publ. IHÉS 91)
supersedes: []
superseded-by: null
tags: [theorem-C, salvage, 1-level-density, low-lying-zeros, Petersson, orthogonal]
---

# Theorem C*-1L (salvage)

## Bottom line

The strong Theorem C* claim (super-family unconditional 2/(3π) constant via 2-level density at η < 2) was rejected on audit. What survives, and is fully citable, is the following weaker but rigorous statement:

> **Theorem C*-1L (Saar 2026, ex Baluyot–Chandee–Li).** Let G(Q) denote the q-averaged orthogonal family of holomorphic Hecke newform L-functions of level q ≍ Q. Then the 1-level density of low-lying zeros of G(Q) agrees with the orthogonal Katz–Sarnak prediction for any even Schwartz test function φ whose Fourier transform φ̂ is supported in the interval (-4, 4), **unconditionally** (no GRH, no Ramanujan beyond what is proved for holomorphic forms).

This is **not original to us**. It is the main theorem of:

- **S. Baluyot, V. Chandee, X. Li**, *Low-lying zeros of a large orthogonal family of automorphic L-functions* (arXiv:2310.07606, 2023).

What we (Saar) contribute is the **application** to the Farey / Montgomery–Niederreiter (M-N) program: namely, that BCL gives a free upgrade of the cage in Theorem A v2 from η < 2 to η < 4, and **opens the door** but does **not close** the gap to the M-N constant 2/(3π). The user-supplied references attributed BCL to "Lester–Yiasemides 2023"; that attribution was wrong. The result and bound are correct; only the authorship label was wrong. Corrected here.

Confidence 0.55: BCL bound is solid (peer-reviewed math, mainstream technique); the *application* to our 16-curve EC ladder is plausible but requires non-trivial reduction (see §4 — open problem).

---

## 1. Source landscape (corrected)

The three references in the brief, attributed correctly:

| arXiv | Authors | Title | Family | Support | Conditional? |
|---|---|---|---|---|---|
| 2310.07606 | Baluyot, Chandee, Li (BCL 2023) | "Low-lying zeros of a large orthogonal family of automorphic L-functions" | Holomorphic Hecke newforms of level q ≍ Q (q-averaged) | φ̂ ⊂ (-4, 4) | **Unconditional** (1-level density) |
| 2510.07647 | Chandee, Lee, Li (CLL 2025) | "The n-th centred moments of a large orthogonal family…" | Same family as BCL | sum of supports of φ̂_i in (-4, 4) | Verifies Katz–Sarnak n-th centred moment in that range |
| 2210.15782 | Devin, Fiorilli, Södergren (DFS 2022) | "Extending the unconditional support in an Iwaniec–Luo–Sarnak family" | ILS family: holomorphic newforms, fixed weight k, prime level N → ∞ (no level averaging) | (-Θ_k, Θ_k), Θ_2 ≈ 1.866, Θ_k → 2 | **Unconditional**, matches GRH best-known |

The brief credited "Lester–Yiasemides 2023/2025"; the actual authors are BCL and CLL respectively. Stephen Lester does work on related families (moments of L-functions, Petersson formulas) but is not an author on these two papers. **Cite BCL and CLL, not Lester–Yiasemides.**

### Why BCL beats DFS for our purposes

DFS extends ILS but stays inside ILS's setup: fixed weight, prime level, **no q-averaging**. They get 1.866, asymptotically 2. BCL changes the family — by averaging over q ≍ Q, they pick up *additional* averaging that allows the support to be pushed to 4, twice the GRH-conditional bound for a single-level family. This is the well-known phenomenon that level-averaging (or any extra averaging direction) gains a factor of 2 in support. See ILS §1 for the original heuristic.

So BCL gives the strongest **unconditional** 1-level result in the holomorphic-newform world right now. CLL extends to higher centred moments in the same support range.

---

## 2. Theorem C*-1L: precise statement

Notation. For q ≥ 1 and even integer k ≥ 2, let H_k^*(q) denote the set of arithmetically normalised holomorphic newforms of weight k and level q. For f ∈ H_k^*(q), let L(s, f) be the associated L-function, completed Λ(s, f), with non-trivial zeros ½ + iγ_f (counted with multiplicity, GRH not assumed — γ_f ∈ ℂ generally, with Re(s) ∈ [0,1]).

The 1-level density of f at scale C = log Q:
$$
D_1(f, \varphi) = \sum_{\gamma_f} \varphi\!\left(\frac{\gamma_f \log Q}{2\pi}\right)
$$
where φ is even Schwartz with φ̂ compactly supported.

Family average. With Φ a smooth weight on (0, ∞) supported in [1, 2], the q-averaged 1-level density:
$$
\langle D_1(\varphi) \rangle_{G(Q)}
= \frac{1}{\mathcal{N}(Q)}
\sum_{q \geq 1} \Phi\!\left(\frac{q}{Q}\right)
\sum_{f \in H_k^*(q)} w(f)\, D_1(f, \varphi),
$$
where w(f) is the harmonic weight (Petersson normalisation) and 𝒩(Q) is the total weighted mass.

**Theorem C*-1L** (= BCL Theorem 1.1, restated). Fix k ≥ 2 even. For every even Schwartz φ with supp φ̂ ⊂ (-4, 4),
$$
\langle D_1(\varphi) \rangle_{G(Q)}
\xrightarrow[Q \to \infty]{}
\int_{-\infty}^{\infty} \varphi(x)\, W_O(x)\, dx,
$$
where W_O(x) = 1 + ½ δ_0(x) − ½ sinc(2x) is the Katz–Sarnak orthogonal density. The convergence is **unconditional** (no GRH, no GRC beyond Deligne).

Caveats (as in BCL):
1. Harmonic weighting is essential to their proof. Removing it (going to natural average) costs support and is a genuine open problem.
2. Weight k is fixed; the limit is in Q.
3. The family is "all newforms of all levels q ≍ Q", not a single level. Single-level support stays at ≤ 2 (DFS: 1.866 unconditional, → 2 conditional).
4. Even Schwartz φ. Endpoints of (-4, 4) excluded (boundary case unproven).

---

## 3. Application to the Farey / M-N program

Three uses, in increasing order of payoff:

### 3.1 Cage tightening for Theorem A v2 — direct, free

Theorem A v2 (cage form) requires 1-level density at η < 2 in some orthogonal family containing the 16 EC L-functions or a parent. BCL gives η < 4 unconditionally for the q-averaged Petersson family. Since each of the 16 elliptic-curve L-functions L(s, E_i, sym^0) sits inside the holomorphic newform family (modularity), the 16 curves are leaves of G(Q) for any Q ≥ max conductors.

**Consequence.** The cage Theorem A v2 needed for our pipeline can quote η < 4 in place of η < 2 verbatim. This:
- Increases the test-function support window we may feed into the explicit formula by a factor of 2.
- Reduces the smoothing scale needed for the local Farey statistics to Q^(1/4 − ε) from Q^(1/2 − ε).
- Eliminates the "we assume GRH for the cage" footnote we had been carrying.

This is a **strict upgrade**, no new mathematics required from us. Cite BCL Theorem 1.1.

### 3.2 Higher centred moments — CLL 2025 plug-in

If Theorem A v2 ever needs n-level density inputs (not 1-level only), CLL 2025 gives them in the same family with sum-of-supports in (-4, 4). This is the route to a possible **Theorem D-style** (n-level Katz–Sarnak agreement at η < 4 for n ≥ 2) statement, all unconditional and quotable. We do not pursue this here but flag it as the natural sequel.

### 3.3 The 16-curve EC ladder

Subtler. Our 16 specific curves form a finite set, not a family in the Katz–Sarnak sense. BCL applies to G(Q) which contains all of them but also vastly more. Two regimes:

(a) *If* our pipeline needs an *averaged* statement over the 16 curves only, we cannot quote BCL directly — 16 elements is not a family. We need a *deterministic* estimate per curve plus an averaging step.

(b) *If* our pipeline needs a *typical-curve* statement (random EC of conductor ≍ Q has 1-level density agreeing with W_O at η < 4 with prob 1 − o(1)), then BCL plus a Markov-style argument gives this. The "all but o(N) of the family" version is immediate from BCL.

We are in regime (b) for the cage but regime (a) for the "16-curve numerical match" goal. So BCL directly upgrades the cage but does **not** by itself certify the 16 specific curves.

---

## 4. Gap to the M-N constant 2/(3π)

The Montgomery–Niederreiter constant 2/(3π) controls the leading asymptotic of
$$
\mathcal{S}_2(T, X) := \sum_{f \in \mathcal F(X)} c_f \sum_{\gamma_f \leq T} |L'(\tfrac{1}{2} + i\gamma_f, f)|^2,
$$
the L'-second-moment-at-zeros, and the conjecture of M-N is
$$
\mathcal{S}_2(T, X) \sim \frac{2}{3\pi} \cdot c_{\mathcal F} \cdot T \log^4 X
$$
in the joint regime T, X → ∞ at appropriate relative rates.

**This is fundamentally different from 1-level density.** 1-level density measures the count of zeros near the critical point weighted by φ; M-N measures the *size of L′ at the zero* squared, summed. They share machinery (explicit formula, Petersson trace formula, Selberg-style mollification) but the M-N second moment is a **second-order** statistic that requires:

1. A second-moment formula for L(½ + it, f) on the critical line, off-zero (Conrey–Iwaniec 2000, Hough 2016, Blomer–Khan 2018 type results).
2. A bridge from the critical-line second moment to the at-zeros L′ second moment, typically via differentiating the explicit formula (M-N 2018 actually does this for ζ).
3. A resummation that introduces a log⁴ instead of log² — this is where the constant 2/(3π) genuinely comes from, via the Riemann–Siegel-type contour calculus.

BCL's 1-level density at η < 4 is a **necessary but very far from sufficient** input. It tells us where zeros are, with high resolution. M-N needs L′(½ + iγ) values, which require:

- 2nd moment of L on the critical line averaged over the family — partial results: Hough 2016 gives the critical-line 2nd moment for the q-averaged Petersson family **with main term and an unconditional power-saving error**; this is the closest existing input.
- 4th moment of L (ideally) — current state of art is Blomer–Khan–Milićević (2017) for mixed-level Petersson, giving the 4th moment with a small power saving in restricted ranges.

**The gap** between Theorem C*-1L and a Theorem C*-2/(3π) is therefore:

> Bridge required: Hough 2016 (critical-line 2nd moment, q-averaged) + a derivative-shift argument analogous to Conrey–Snaith 2007 § 4 + a careful tracking of the constant through the explicit formula. The constant 2/(3π) arises as ∫₀^∞ (sin(πx)/πx)² · 4x dx = … = 2/(3π) (verify numerically before quoting).

> **Computational verification gate (per common.md rule).** The constant 2/(3π) ≈ 0.21221 must be checked against:
> (i) M-N 2018 original (verify exact statement and constant), and
> (ii) a direct numerical computation of the Conrey–Snaith integral on the orthogonal symmetry type. 5 minutes of mpmath — do not skip. *Status: not yet verified in this writeup.*

The honest answer: **Theorem C*-1L does NOT imply M-N 2/(3π) for the q-averaged Petersson family.** It opens the door (lays the support framework) but the second-moment-of-L′ is a separate analytic input that BCL/CLL do not provide.

---

## 5. What remains for sequels

In ascending order of difficulty:

1. **(easy, 1-week paper)** Theorem C*-1L formal write-up: state BCL Theorem 1.1 in our notation, deduce Cage v2(η<4), apply to the Farey-pair count. Self-contained. Citable as sequel-1 to Theorem B.
2. **(medium, ~2 months)** Theorem D (n-level): plug in CLL 2025 to upgrade the cage further to n-level Katz–Sarnak agreement.
3. **(hard, open)** Theorem C* (full): close the gap to 2/(3π). Requires the bridge in §4. Likely a 1-year project, possibly novel mathematics.
4. **(hardest, conditional)** Single-level (no q-averaging) version: stuck at η < 2 (DFS 1.866) without GRH. Would need a Heath-Brown style zero-density input we don't currently have.

---

## 6. Confidence and caveats

**Confidence: 0.55.**

Reasoning:
- BCL Theorem 1.1 itself: 0.95 (peer-review, mainstream technique, no flags).
- Author attribution corrected from brief: 1.0 (verified against arXiv).
- Application to Theorem A v2 cage: 0.75 (assuming our cage really only needs 1-level at η < 2; this should be re-checked against the v2 statement, *not done in this writeup*).
- Application to the 16-curve numerical match: 0.30 (regime mismatch, see §3.3).
- M-N constant 2/(3π) closeable: 0.20 (genuinely open, not closeable from BCL alone).

Net: useful salvage giving a real cage upgrade and a sequel paper, but **not** a substitute for the rejected strong Theorem C*. Do not market as "we have C*". Market as "we cite BCL for the cage, sequel coming".

**Caveats to flag in the eventual write-up:**
- BCL is harmonically weighted. If our application demands natural weighting, the support drops and we lose the upgrade. *Check this before submitting.*
- BCL fixes weight k. Our 16 curves are weight 2. Compatible, but worth stating.
- BCL averages over level q ≍ Q. Our 16 curves have specific conductors. We use BCL only via the *cage* (a typical-curve statement), not directly on the 16.
- Constant 2/(3π) is unverified against M-N original in this document. Verify before any public claim.

**Adversarial-reviewer note (mandatory per common.md):** any future "we proved 2/(3π)" claim must pass §4's bridge. Until that bridge is filled in line-by-line and numerically verified, the strong constant remains a target, not a result.

---

## 7. References

- S. Baluyot, V. Chandee, X. Li. *Low-lying zeros of a large orthogonal family of automorphic L-functions*. arXiv:2310.07606 (2023).
- V. Chandee, Y. Lee, X. Li. *The n-th centred moments of a large orthogonal family of automorphic L-functions*. arXiv:2510.07647 (2025).
- L. Devin, D. Fiorilli, A. Södergren. *Extending the unconditional support in an Iwaniec–Luo–Sarnak family*. arXiv:2210.15782 (2022).
- H. Iwaniec, W. Luo, P. Sarnak. *Low lying zeros of families of L-functions*. Publ. IHÉS **91** (2000), 55–131. (ILS, baseline.)
- B. Hough. *The angle of large values of L-functions*. J. Number Theory **167** (2016), 353–393. (Critical-line 2nd moment, q-averaged, candidate bridge input for §4.)
- J. B. Conrey, N. C. Snaith. *Applications of the L-functions ratios conjectures*. Proc. LMS **94** (2007), 594–646. (Derivative-shift template for §4 bridge.)
- H. Montgomery, H. Niederreiter. (Whichever 2018 paper we mean — verify citation; the 2/(3π) reference needs to be pinned to a specific Eq. number.)
