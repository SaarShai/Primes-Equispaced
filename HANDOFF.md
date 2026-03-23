# HANDOFF PROMPT: PRIME WOBBLE THEOREM — FULL PROJECT CONTEXT

You are reviewing and potentially improving a mathematics research paper. Below is everything you need to know about the project, including what's been done, what's open, what we struggled with, and what the paper claims.

## THE PAPER

Title: "New Identities Connecting Farey Sequences to the Mertens Function via Per-Step Discrepancy"
Authors: Saar Shai (independent researcher) and Anthropic's Claude Opus 4.6
Length: 17 pages, 10 figures, 3 tables, 8 theorems, 8 references, 7 open questions
Repository: https://github.com/SaarShai/Primes-Equispaced

## WHAT THE PAPER PROVES

We study what happens to the uniformity of the Farey sequence F_N (all fractions a/b with 0 ≤ a/b ≤ 1, b ≤ N, gcd(a,b)=1) when you add one more integer N. Nobody had studied this "per-step" behavior before.

The L² discrepancy ("wobble") W(N) = Σ(f_j - j/n)² measures uniformity. We define ΔW(N) = W(N-1) - W(N), so positive means uniformity improved.

### Eight Theorems (all with proof sketches):

1. **Bridge Identity** (Theorem 3.1): Σ_{f∈F_{p-1}} e^{2πipf} = M(p) + 2
   - Connects a Farey geometric quantity to the Mertens function
   - FORMALLY PROVED in Lean 4 with zero sorry (by Aristotle theorem prover)

2. **Generalized Bridge** (Theorem 3.2): For ANY prime m > N: Σ_{f∈F_N} e^{2πimf} = M(N) + 1
   - All primes above the order give the SAME exponential sum
   - The sum depends only on M(N), not on which prime m

3. **Universal Farey Exponential Sum** (Theorem 3.3): For ANY m and N:
   Σ_{f∈F_N} e^{2πimf} = M(N) + 1 + Σ_{d|m, d≥2} d·M(⌊N/d⌋)
   - COMPLETE formula for every frequency-order pair
   - Verified computationally for all m ≤ 40, N ≤ 30

4. **Master Involution Principle** (Theorem 3.4): Σ D(f)·g(f) = -(1/2)Σg(f) for symmetric g
   - Uses the Farey involution σ(f) = 1-f with D(σ(f)) = -D(f) - 1

5. **Displacement-Cosine Identity** (Theorem 3.5): Σ D(f)·cos(2πpf) = -1 - M(p)/2
   - The Fourier coefficient of the rank discrepancy at prime frequency is LINEAR in Mertens

6. **Fractional Parts Sum** (Theorem 3.6): Σ {pf} = (n-2)/2
   - Uses the permutation property of multiplication by p modulo b

7. **Universal δ-Symmetric Identity** (Theorem 3.7): Σ δ(f)·g(f) = g(1) for symmetric g
   - Where δ(f) = f - {pf} (the "shift")

8. **Compact Cross-Term Formula** (Theorem 3.8): Σ D(f)·δ(f)² = -(1/2)Σδ² - 1/2
   - Boundary correction because δ² is not symmetric at f=0,1

### Key Computational Findings:

- **Per-step asymmetry**: Composites improve uniformity 96% of the time; primes cause 99% of ALL damage. This was invisible in cumulative W(N).

- **Sigmoid relationship**: Violation probability (P(ΔW>0)) is a sharp sigmoid function of M(p)/√p:
  - M/√p < -0.1: 0.0% violations (0/3,288)
  - M/√p ∈ [0.1, 0.2): 74.5%
  - M/√p ≥ 0.3: 100.0% (257/257)

- **Counterexample**: At p=92,173 with M=-2: ΔW = +3.56×10⁻¹¹ (positive despite M<0). The ONLY counterexample among 9,588 primes up to 100K.

- **Small primes**: p=3,5,7 are also counterexamples (M<0 but ΔW>0), which is why the conjecture starts at p≥11.

- **Composites**: Among 404 composites N≤500, 294 (73%) have ΔW>0 with M<0. The Mertens correlation is specific to primes.

### Applications in the Paper:

- **Exact quadrature errors**: Bridge gives exact Farey integration error for cos(2πmx), improving standard bounds by 62-693×. "Zero-error primes" where M(p)=-2 give exactly zero error.
- **iCZT spectral leakage**: Universal formula evaluates leakage exactly for Parks-Burrus (2020) inverse Chirp Z-Transform. Choosing N with M(N)=-1 gives zero leakage.
- **Slope quantization bias**: In digital line detection, the Farey rank discrepancy has a flat spectral floor at -(M(N)+1)/2 for all prime frequencies above N.
- **New RH characterization**: RH ⟺ Farey exponential sums at prime frequencies above the order are O(N^{1/2+ε}).
- **O(1) predictor**: M(p)/√p predicts ΔW sign with 94.6% accuracy at O(1) cost (vs O(p²) brute force).
- **Geometric Mertens computation**: M(p) = (Farey cosine sum) - 2, computing arithmetic from geometry.

## FORMAL VERIFICATION (Lean 4)

Four Lean files, 49 total results:
- **PrimeCircle.lean**: 13 results, 0 sorry ✓ (Farey cardinality, Ramanujan sums, sum-of-squares, wobble decomposition)
- **DeltaCosine.lean**: 5 results, 0 sorry ✓ (δ-cosine framework, computational verification for p=5)
- **BridgeIdentity.lean**: 26 results, 0 sorry ✓ (Mertens function, Möbius properties, coprime residue permutation, Ramanujan sum at coprime argument, BRIDGE IDENTITY ITSELF)
- **MertensGrowth.lean**: 5 results, 1 sorry (computational witnesses M(3)=-1 etc. proved; general growth theorem |M(N)|=Ω(√N) stated with sorry — this is a deep analytic result)

The bridge identity was proved AUTONOMOUSLY by the Aristotle theorem prover (https://aristotle.harmonic.fun). The proof chain: coprime residue permutation → Ramanujan sum at coprime argument → bridge identity.

Build command: `export PATH="$HOME/.elan/bin:$PATH" && lake build`
Lean 4 v4.28.0, Mathlib v4.28.0.

## WHAT WE STRUGGLED WITH / OPEN PROBLEMS

### The Anticorrelation Lemma (the main proof gap)
The biggest open problem: prove Σ D(f)·δ(f) < 0 for primes p ≥ 19 with M(p) ≤ 0. This would prove the wobble-Mertens sign correlation. We tried 14+ approaches (Fourier, Cauchy-Schwarz, rearrangement, Abel summation, Dedekind sums, etc.) and all hit the same wall: the margin is only 0.08-2.5% and no standard bound is tight enough. The counterexample at p=92,173 shows the conjecture is FALSE for the original formulation, but the M≤-3 version (4,617 primes, zero counterexamples) remains open.

### Geometric Growth Bound
We identified a potential new geometric proof strategy for |M(N)| = Ω(√N) using the sigmoid: since violations (M>0) and non-violations (M<0) both occur infinitely often, M must oscillate with amplitude ≫√p. But making this rigorous requires proving the sigmoid analytically, which reduces to the anticorrelation problem.

### Multiplicative Discrepancy (Erdős Problem #67)
The open multiplicative case of the Erdős discrepancy problem asks if Σ f(kd) → ∞ for multiplicative f. For f=μ, d=1, this sum is M(m), which our bridge evaluates geometrically. But extending to general multiplicative f or d>1 is open.

### Bridge Generalization
The bridge identity is fundamentally about μ (Möbius function) because Ramanujan sums are defined through μ. We showed the Liouville function L(N) can be expressed through Farey sums via L(N) = Σ M(⌊N/k²⌋), but this just substitutes our bridge into a known classical identity — not a deep generalization.

### Higher Dimensions
For tensor-product Farey sets F_N^d, the exponential sum at prime-vector frequency is (M(N)+1)^d. When M(N)=-1 (e.g., N=10), this vanishes in every dimension. But this is trivial (just products). Non-product Farey sets in higher dimensions don't have standard definitions.

## ERRORS WE FOUND AND FIXED (across 5+ review rounds)

Major errors caught during review:
- "60+ theorems with zero sorry" → was completely false (actual: 49 results, most with sorry initially; now 48 proved, 1 sorry)
- "97 composite counterexamples" → wrong by 30×+ (actual: 294 in first 500 composites)
- Insertion orthogonality Σ D(k/p)cos(2πk/p) = 0 → numerically FALSE (actual value is 0.5); removed from paper
- Figure 2 caption claimed ΔW>0 for p=13 → false (ΔW(13)<0)
- Prime count 17,984 → wrong (actual: 17,980)
- "Eleven orders of magnitude" → wrong (actual: ~40×)
- |ΔW| ≈ 10⁻¹² for tightest M≤-3 case → wrong (actual: 7×10⁻¹¹)
- "Shallowest possible negative M(p)=-2" → wrong (M=-1 occurs at 183 primes)
- p≥11 cutoff never explained → added explanation (p=3,5,7 are counterexamples)
- Sigmoid table had 3,283 → wrong (actual: 3,288)
- Section 3 intro said "partially formalized, 39 proved" → stale after bridge was fully proved

## COMPUTATIONAL DATA

- experiments/wobble_primes_100000.csv: 9,588 primes with ΔW, M, M/√p, violation flag
- experiments/wobble_primes_50000.csv: earlier computation
- experiments/wobble_primes_only.c: C implementation for fast wobble computation
- Compiled: cc -O3 -o wobble_primes_only wobble_primes_only.c -lm
- Run: ./wobble_primes_only 100000

## FIGURES

10 figures in figures/ directory:
1. fig_circle_farey.png — F₁₂ on the unit circle
2. fig_wobble_circle.png — wobble visualization (3 panels: F₅, F₁₂, adding p=13)
3. fig_void_filling.png — primes vs composites filling voids
4. fig_universal_formula.png — exponential sum at all frequencies for F₂₀ (NEW)
5. fig_bridge_vectors.png — bridge identity as vector sum on circle
6. fig_sigmoid.png — violation probability sigmoid function (NEW)
7. fig_mertens_violations.png — Mertens function + rolling violation density
8. fig_mertens_bias_circle.png — cosine coloring on circle
9. fig_delta_w_signs.png — per-prime ΔW bar chart
10. fig_shift_map.png — multiplication-by-p map on circle

## WHAT YOU COULD HELP WITH

1. **Review the paper for errors** — we've done 5+ rounds but might have missed something
2. **The anticorrelation lemma** — the main proof gap. Can you find a way to bound Σ D(f)·δ(f)?
3. **Improve proof sketches** — some are terse; fuller proofs would strengthen the paper
4. **The M≤-3 conjecture** — 4,617 primes, zero counterexamples. Can this be proved?
5. **Additional applications** — we showed iCZT, slope quantization, quadrature. Are there more?
6. **The Erdős connection** — can the bridge identity framework contribute to the multiplicative discrepancy problem?
7. **Lean formalization** — the general growth theorem |M(N)|=Ω(√N) has sorry. Can it be closed?
8. **Writing quality** — the paper went through many edits; fresh eyes on clarity/flow would help

## KEY FILES

- paper/main.tex — the paper (1019 lines)
- paper/main.pdf — compiled PDF (17 pages)
- RequestProject/PrimeCircle.lean — core Lean proofs
- RequestProject/BridgeIdentity.lean — bridge identity proof chain
- RequestProject/DeltaCosine.lean — δ-cosine framework
- RequestProject/MertensGrowth.lean — Mertens growth witnesses
- experiments/wobble_primes_100000.csv — computational data
- experiments/wobble_primes_only.c — C computation code
- figures/*.png — all 10 figures
- README.md — GitHub repository README
