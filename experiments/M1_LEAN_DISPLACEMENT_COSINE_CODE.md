# M1_LEAN_DISPLACEMENT_COSINE_CODE.md

## Summary

This document presents a comprehensive analysis and formal verification plan for the Displacement-Cosine Identity within the context of the *Farey-Local* Lean 4 project. The primary objective is to translate the informal mathematical derivation of the identity into a rigorous Lean 4 theorem, utilizing the existing infrastructure of `FareyBasic.lean` and `BridgeIdentity.lean`. The identity connects the rank-discrepancy function of Farey sequences to the Mertens function and trigonometric sums over the Farey set, specifically $\sum_{f \in F_{p-1}} D(f) \cos(2\pi p f) = -1 - M(p)/2$ for odd primes $p$.

The analysis evaluates the feasibility of formalizing this result within the current state of Mathlib and the specific `Farey-Local` repository. It details the necessary Lean definitions, the partitioning strategy for the proof skeleton, and the anticipated challenges regarding real number arithmetic and finite set summations. Furthermore, this report contextualizes the identity within the broader research goals, including the "Mertens spectroscope" and "Per-step Farey discrepancy" initiatives, ensuring alignment with the project's verification standards for the upcoming Paper A.

## Detailed Analysis

### 1. Mathematical Context and Significance

The Displacement-Cosine Identity represents a critical bridge between combinatorial properties of Farey sequences and the analytic properties of the Möbius function. In the context of the *Farey-Local* research program, which aims to verify results related to the Mertens spectroscope and zeta zero detection, establishing this identity formally is a prerequisite for higher-level spectral analysis.

The identity relies on the term $D(f) = \text{rank}(f) - |F_{p-1}| \cdot f$. This is the displacement of the fraction $f$ from its uniform distribution expectation. Summing this displacement weighted by the oscillating term $\cos(2\pi p f)$ isolates specific correlations between the fraction rank and the prime modulus $p$. The right-hand side, $-1 - M(p)/2$, connects this combinatorial sum directly to the arithmetic function $M(p) = \sum_{k=1}^p \mu(k)$. This link is non-trivial; it implies that the "discrepancy" of the Farey sequence at order $p-1$ encodes information about the cumulative Möbius function.

Given the "Mertens spectroscope" context (detecting zeta zeros via pre-whitening), verifying this identity allows us to formally link the geometric structure of $F_{p-1}$ to the analytic behavior of $\zeta(s)$. The provided context mentions "verified $D_K \cdot \zeta(2)$" results for characters $\chi_4, \chi_5, \chi_{11}$. While the Displacement-Cosine Identity deals with the trivial character (or rather, the sum over the full Farey set without character twists), formalizing it creates a foundational "unit test" for the trigonometric sum lemmas required for the more complex character-based verifications. If we cannot verify the basic cosine sum over Farey sequences, the spectral analysis of $L(\rho, \chi)$ (where $\chi$ is $\chi_4, \chi_5$, etc.) cannot be trusted.

### 2. Formalization Strategy in Lean 4

#### (a) Theorem Statement and Types
In Lean 4, natural numbers (`Nat`) and real numbers (`Real`) are distinct types. The Farey sequence elements are typically rationals (`Rat`). We must ensure the rank is a natural number, the order $p$ is a natural number, and the cosine term operates on reals.

The theorem statement must be precise regarding the quantification of $p$.
```lean
theorem displacement_cosine_identity (p : ℕ) (hp_odd : p % 2 = 1) (hp_ge_3 : p >= 3) (hp_prime : Nat.Prime p) :
  (∑ f in FareySeq (p - 1), (FareySeq.rank p f - (FareySeq.card (p - 1) : ℝ) * (f : ℝ)) * Real.cos (2 * Real.pi * (p : ℝ) * (f : ℝ))) 
  = -1 - (MertensFunction p : ℝ) / 2 := by sorry
```
*Note:* We must cast the rank and cardinality to `Real` for multiplication with `cos`. The rank function must return a `Nat`, which requires coercion.

#### (b) Proof Skeleton and Partitioning
The informal proof relies on partitioning the Farey sequence $F_{p-1}$. The key lemma is the symmetry of the Farey sequence: if $f \in F_n$, then $1-f \in F_n$.

1.  **Decomposition Lemma:** We must split the summation over `FareySeq (p-1)` into fixed points and pairs.
    *   Fixed points: $0/1$, $1/1$, $1/2$ (since $p$ is odd, $1/2$ is included).
    *   Pairs: $\{f, 1-f\}$ where $f \in F_{p-1}$ and $0 < f < 1/2$.
    Lean's `Finset.sum` requires us to handle the set splitting explicitly. We will use a helper lemma `FareySeq.partition_by_symmetry` that returns a tuple of the center terms and a `Finset` of representatives for the pairs.

2.  **Displacement Symmetry:** We need to prove $D(f) + D(1-f) = -1$.
    *   This requires establishing the relationship between the rank of $f$ and the rank of $1-f$.
    *   If $|F_n| = N$, and rank is 0-indexed, $rank(1-f) = N-1 - rank(f)$.
    *   Then $D(f) + D(1-f) = (r - Nf) + (N-1-r - N(1-f)) = N - 1 - N = -1$.
    *   This algebraic fact must be formalized as a sublemma `displacement_symmetry`.

3.  **Cosine Symmetry:** $\cos(2\pi p (1-f)) = \cos(2\pi p f)$.
    *   This relies on `Real.cos_periodic` or basic properties of trigonometric functions over integers.
    *   Since $p$ is an integer, $2\pi p (1-f) = 2\pi p - 2\pi p f$. $\cos(A - B) = \cos(B)$ if $A = 2\pi \cdot \text{integer}$.

4.  **Bridge Identity Application:**
    *   The informal proof references `BridgeIdentity.lean` (real part decomposition).
    *   We must assume or define a lemma `sum_cos_over_farey`:
        `∑ f in FareySeq (p-1), Real.cos (2 * Real.pi * p * f) = M(p) + 2`.
    *   This must be instantiated for the sum over pairs. $\sum_{\text{pairs}} \cos = (\sum_{\text{all}} \cos - \text{fixed points}) / 2$.

#### (c) Key Challenges in Lean
*   **Real Arithmetic:** `Real.cos` takes a real argument. `f` is a `Rat`. Converting `f` to `Real` must be done consistently to ensure type correctness. Lean does not automatically treat `Rat` as `Real` in all algebraic simplifications. We must explicitly use `(f : ℝ)`.
*   **Finset Cardinality:** Calculating the rank of a fraction requires the sequence to be ordered. The `FareySeq` definition must expose an ordered list or a finset with a canonical linear order. If `rank` is defined via a list index, we must ensure `Finset` operations respect this order or define `rank` independently.
*   **Parity of $p$:** The condition $p \ge 3$ and odd is critical because it determines which terms exist in $F_{p-1}$ and the value of $\cos(\pi p)$. If $p$ were even, $1/2$ might behave differently or the fixed point set would change. The proof requires `Nat` arithmetic for the cosine phase shifts (e.g., $\cos(\pi p) = -1$ iff $p$ odd).
*   **Coercion of M:** `MertensFunction` returns `ℤ` or `ℕ` (usually `ℤ` for Möbius sums). The RHS requires `ℝ`. Coercions must be inserted correctly: `(MertensFunction p : ℝ)`.

#### (d) Existing Project Integration
The prompt notes existing files: `BridgeIdentity.lean`, `FareyBasic.lean`, `FareyProperties.lean`, `WobbleDecomp.lean`.
*   `FareyBasic.lean`: Likely contains `FareySeq`, `rank`, and basic cardinality properties. We should check if `FareySeq.card` is available and if `rank` is already exposed as a function `ℕ → ℚ → ℤ` or similar.
*   `BridgeIdentity.lean`: This is the source of the sum of cosines result. We can likely import this directly. However, we must verify that `BridgeIdentity` is parameterized by `p` correctly to match the `FareySeq (p-1)` definition used here.
*   `WobbleDecomp.lean`: Might contain decomposition lemmas for sums over subsets. This could be adapted for the `pairs` vs `fixed_points` split.

#### (e) Mathlib Dependencies
*   `Mathlib.Data.Real.Basic`: For `Real.cos`, `Real.pi`.
*   `Mathlib.Data.Finset.Basic`: For summation over `Finset` and set operations (splitting the sum).
*   `Mathlib.Tactic`: For `calc` blocks, `rw`, `simp`.
*   `Mathlib.NumberTheory.LegendreSymbol`: For prime properties (if not already in local project).
*   `Farey-Local`: Local definitions for `MertensFunction` and `FareySeq`.

#### (f) Effort Estimate
*   **Lines of Code:** The theorem statement is ~5 lines. The proof skeleton involves ~15-20 lines of tactics. Sublemmas (displacement symmetry, partition, fixed points) might add ~30-40 lines of proof terms. Total estimated: **60-80 lines of Lean code** (excluding imports and comments).
*   **Time Estimate:** A proficient Lean user with familiarity with the codebase would require:
    *   2 hours to verify the types and import structure.
    *   4 hours to construct the `partition_by_symmetry` lemma (Finset manipulation is verbose in Lean).
    *   4 hours to debug coercions (the most common error source in Lean number theory proofs).
    *   2 hours to write and refine the proof script.
    *   **Total:** **12 hours (approx. 2 days of focused work)**.

#### (g) Prioritization
Should we verify this before Paper A submission?
*   **Verdict:** **YES.**
*   **Reasoning:** Paper A likely discusses the Farey discrepancy $\Delta W(N)$. The Displacement-Cosine Identity provides a direct link between the discrepancy term $D(f)$ and the Mertens function, which is the core of the "Mertens spectroscope." Formalizing this identity demonstrates that the combinatorial core of the spectral analysis is sound. It reduces the "trust horizon" for Paper A. If this basic trigonometric-Farey identity cannot be verified, the more complex character sums (using $\chi_4, \chi_5, \chi_{11}$) are even riskier. Doing it before Paper A allows us to use the verified lemma as a "black box" assumption in the main proofs, streamlining the remaining work.

## Open Questions

1.  **Rank Definition Consistency:** The prompt mentions `rank(f)`. Is this 0-indexed or 1-indexed?
    *   In my analysis, I assumed 0-indexed for the identity to hold ($D(f)+D(1-f)=-1$). If the library uses 1-indexing, the constant term changes (e.g., to 0 or +1). We must inspect `FareyBasic.lean` to confirm `FareySeq.rank` behavior. If 1-indexed, the RHS of the theorem must be adjusted to $-M(p)/2$ or similar. The verification process itself will reveal this.
2
