# Cross-Field Mathematical Tools for the Ratio Bound Problem

## The Problem (Plain Language)

We have a sequence W(N) that measures how evenly Farey fractions are spread around the circle. When we add a new prime p, W changes by an amount ΔW. We need to prove ΔW < 0 (meaning W decreases, i.e., the points get MORE evenly spread) whenever the Mertens function M(p) ≤ -3.

The difficulty: ΔW splits into 5 terms (A, B, C, D, E). We need B + C + D > A. But A depends on the previous value W(p-1), which we don't know precisely. So the bound becomes a **ratio problem**: we need to bound W(p)/W(p-1).

---

## Tool 1: Rayleigh Quotient Bounds

### What it is
The Rayleigh quotient is a classic tool from linear algebra. Given a matrix M and a vector x, the ratio R(M,x) = (x^T M x) / (x^T x) always lands between the smallest and largest eigenvalues of M. Think of it as: "the ratio of two quadratic expressions is trapped between two constants."

### Key theorems
- **Min-max (Courant-Fischer)**: The Rayleigh quotient achieves its minimum and maximum exactly at the eigenvectors. This gives TIGHT two-sided bounds on any ratio of quadratic forms.
- **Perturbation bounds (Davis-Kahan, Weyl)**: When the matrix changes slightly, eigenvalues can only shift by a bounded amount. This controls how much the ratio can change under perturbation.
- **Monotonicity**: For nested subspaces, the Rayleigh quotient satisfies interlacing inequalities — eigenvalues of a submatrix interlace with eigenvalues of the full matrix.

### How it might apply
W(N) is literally a sum of squared deviations — a quadratic form. W(p)/W(p-1) is a ratio of two quadratic forms in the Farey fractions. If we can express the Farey-point discrepancy as x^T M x for some matrix M (perhaps a Gram matrix of the point configuration), then:
- The ratio W(p)/W(p-1) is bounded by eigenvalue ratios of M_p vs M_{p-1}
- Adding p-1 new Farey fractions is a rank-(p-1) perturbation, and Weyl's inequality bounds how much each eigenvalue can shift
- We might get: W(p)/W(p-1) ≤ 1 - c/p² for some constant c, which is exactly the kind of bound we need

**Verdict**: HIGHLY PROMISING. The Rayleigh quotient is the most natural fit because our problem is literally a ratio of quadratic forms.

**Sources**:
- [Rayleigh quotient (Wikipedia)](https://en.wikipedia.org/wiki/Rayleigh_quotient)
- [Bounds for the Rayleigh Quotient and the Spectrum (MERL)](https://merl.com/publications/docs/TR2013-068.pdf)
- [Lecture 4: Rayleigh Quotients (SJSU)](https://www.sjsu.edu/faculty/guangliang.chen/Math253S20/lec4RayleighQuotient.pdf)
- [Courant-Fischer and Rayleigh quotients (MIT OCW)](https://ocw.mit.edu/courses/18-409-topics-in-theoretical-computer-science-an-algorithmists-toolkit-fall-2009/535add3f6457cc13e51d9774f16bf48f_MIT18_409F09_scribe3.pdf)

---

## Tool 2: Transportation-Entropy Inequality (Marton/Talagrand)

### What it is
Optimal transport asks: what's the cheapest way to move one pile of dirt into the shape of another pile? The "Wasserstein distance" W₂ measures this cost. Talagrand's T₂ inequality says:

> W₂(μ, ν)² ≤ 2C · KL(μ ‖ ν)

In plain language: **the physical distance between two distributions is bounded by how different they are information-theoretically**. If two distributions have similar entropy, they can't be too far apart physically.

### Key theorems
- **Talagrand T₂ inequality**: Wasserstein distance squared ≤ constant × relative entropy (KL divergence). This gives dimension-free Gaussian concentration.
- **Marton's coupling**: Transportation cost inequalities imply concentration of measure — random functions can't deviate too much from their mean.
- **Transport inequalities for point measures**: Recent work extends these to empirical measures (finite point sets), exactly our setting.

### How it might apply
Our W(N) is closely related to the L² Wasserstein distance between the empirical measure of Farey points and the uniform measure on [0,1]. Specifically:

W(N) ≈ W₂(μ_Farey, μ_uniform)²

If the Farey measure satisfies a transportation-entropy inequality, then:
- W(N) is bounded above by the KL divergence between Farey and uniform
- The KL divergence can be computed from the gap distribution
- Adding a prime changes the gap distribution in a way that REDUCES KL divergence (makes it more uniform)
- This would give ΔW < 0 directly via the transport inequality chain

**Verdict**: PROMISING but INDIRECT. The connection W(N) ↔ Wasserstein distance is strong, but we'd need to compute KL divergence changes explicitly. The "from optimal transport to discrepancy" paper by Neumayer-Steidl is directly relevant.

**Sources**:
- [From Optimal Transport to Discrepancy (Neumayer-Steidl)](https://arxiv.org/pdf/2002.01189)
- [Around the entropic Talagrand inequality](https://arxiv.org/abs/1809.02062)
- [Transport inequalities for random point measures (HAL)](https://hal.science/hal-02475798/document)
- [Generalization of Talagrand Inequality (Bobkov-Götze)](https://www.sciencedirect.com/science/article/pii/S0022123699935577/pdf)
- [CLT for empirical transportation cost](https://projecteuclid.org/journals/annals-of-probability/volume-47/issue-2/Central-limit-theorems-for-empirical-transportation-cost-in-general-dimension/10.1214/18-AOP1275.pdf)

---

## Tool 3: Log-Sobolev Inequality

### What it is
The log-Sobolev inequality (LSI) is a stronger cousin of the Poincare inequality. It says:

> Entropy of f² ≤ C · "gradient energy" of f

In plain language: **how spread out a function is (entropy) is controlled by how much it wiggles (gradient)**. The key power of LSI over Poincare is that it gives EXPONENTIAL decay of entropy, not just variance.

### Key theorems
- **Exponential entropy decay**: If a system satisfies LSI with constant C, then entropy decays like e^{-t/C}. This is much faster than the polynomial decay you get from Poincare alone.
- **Modified LSI for discrete settings (Bobkov-Tetali 2006)**: Extends LSI to finite Markov chains and discrete sequences. The modified LSI controls entropy decay rate in discrete systems.
- **Hierarchy**: LSI ⟹ Poincare inequality ⟹ spectral gap. So LSI is the strongest tool in this family.
- **Hypercontractivity**: LSI is equivalent to hypercontractivity of the semigroup, meaning L² norms improve to L⁴ norms over time.

### How it might apply
Think of the evolution F_{p-1} → F_p as one step of a discrete process. If this process satisfies a (modified) log-Sobolev inequality, then:
- The "entropy" of the gap distribution decays exponentially
- Since W(N) is related to the L² discrepancy (which is related to the variance of the gap distribution), LSI would give a bound like W(p) ≤ (1 - c) · W(p-1)
- The constant c would depend on how many new fractions are inserted (φ(p) = p-1 for prime p)
- The exponential decay from LSI would be much stronger than what we need — we only need W(p) < W(p-1)

The challenge is proving the Farey evolution satisfies an LSI. This would require showing that the insertion of p-1 new fractions at each prime step "mixes" the gaps sufficiently.

**Verdict**: POWERFUL IF APPLICABLE. LSI would give more than we need, but proving it holds for the Farey evolution is itself a hard problem. The discrete modified LSI (Bobkov-Tetali) is the right framework.

**Sources**:
- [Modified Log-Sobolev Inequalities in Discrete Settings (Bobkov-Tetali)](https://link.springer.com/article/10.1007/s10959-006-0016-3)
- [Entropy and the log-Sobolev constant (Berkeley lecture)](https://people.eecs.berkeley.edu/~sinclair/cs294/n14.pdf)
- [Entropy and LSI (AMS book chapter)](https://www.ams.org/bookstore/pspdf/cln-28-prev.pdf)
- [Log-Sobolev Inequalities (Waterloo lecture)](https://cs.uwaterloo.ca/~lapchi/cs860-2022/notes/23-log-Sobolev.pdf)
- [Shannon Entropy and Log-Sobolev Inequalities (Nayar)](https://www.mimuw.edu.pl/~nayar/LS.pdf)

---

## Tool 4: Schur Convexity and Majorization

### What it is
Majorization is a way to compare how "spread out" two vectors are. We say x is majorized by y (written x ≺ y) if x is "more mixed" or "more uniform" than y. A function f is Schur-convex if f(x) ≤ f(y) whenever x ≺ y — meaning f increases as things get MORE spread out (less uniform).

### Key theorems
- **Schur-Ostrowski criterion**: A differentiable symmetric function is Schur-convex if and only if (x_i - x_j)(∂f/∂x_i - ∂f/∂x_j) ≥ 0 for all i, j. This is a LOCAL check — you only need to compare pairs of coordinates.
- **Convex + symmetric ⟹ Schur-convex**: Any function that is both convex and symmetric (invariant under permuting arguments) is automatically Schur-convex.
- **Variance is Schur-convex**: The variance Var(x) = Σ(x_i - x̄)² is Schur-convex — it gets larger when the data is more spread out (less uniform).

### How it might apply
The gap vector g = (g_1, g_2, ..., g_n) records the gaps between consecutive Farey fractions. Our W(N) is essentially a function of the gap vector. Here's the key insight:

**When we add a prime p, each old gap of size g_i gets split into smaller sub-gaps.** This makes the gap vector MORE UNIFORM (in the majorization sense). If W(N) is Schur-CONCAVE in the gap vector (decreases when gaps become more uniform), then adding a prime automatically gives ΔW < 0.

More precisely:
- Let g^{old} be the gap vector of F_{p-1} and g^{new} be the gap vector of F_p
- Adding fractions k/p splits large gaps into smaller ones
- This means g^{new} ≺ g^{old} (new gaps are majorized by old gaps — more uniform)
- If W is Schur-convex in gaps, then W(p) ≤ W(p-1), giving ΔW ≤ 0

The crucial question: is W actually Schur-convex or Schur-concave in the gap distribution? Since W = Σ(f_j - j/n)² measures deviation from uniformity, and more uniform gaps mean points closer to equispaced, W should DECREASE. So W should be Schur-CONVEX in the "non-uniformity" of gaps, or equivalently Schur-CONCAVE in the gaps themselves (since more uniform gaps ≺ less uniform gaps).

**Verdict**: VERY PROMISING. This is the most conceptually clean approach. The question reduces to: (a) does adding a prime majorize the gap vector? and (b) is W Schur-convex/concave in the right direction? Both seem likely true but need proof.

**Sources**:
- [Schur-convex function (Wikipedia)](https://en.wikipedia.org/wiki/Schur-convex_function)
- [Majorization: Here, There and Everywhere (Arnold)](https://arxiv.org/pdf/0801.4221)
- [Majorization Theory and Applications (Palomar)](https://palomar.home.ece.ust.hk/papers/2011/WangPalomar_CRCPress2011_majorization.pdf)
- [Fine-Scale Statistics for the Multidimensional Farey Sequence (Marklof)](https://link.springer.com/chapter/10.1007/978-3-642-36068-8_3)
- [Effective Slope Gap Distribution for Lattice Surfaces](https://arxiv.org/html/2409.15660)

---

## Tool 5: Poincare Inequality on the Circle

### What it is
The Poincare inequality on the circle S¹ says:

> Var(f) ≤ (1/λ₁) · ∫|f'|² dx

In plain language: **the variance of a function on the circle is bounded by its "wiggliness"**. The constant 1/λ₁ is determined by the first nonzero eigenvalue (the "spectral gap") of the Laplacian on the circle, which equals (2π)² = 4π².

### Key theorems
- **Spectral gap characterization**: Poincare inequality holds if and only if the spectral gap λ₁ > 0, with optimal constant C = 1/λ₁.
- **Discrete Poincare**: For point sets on the circle, there are discrete analogues where the "gradient" is replaced by differences between neighboring points.
- **Weighted Poincare**: When the measure isn't uniform, weighted versions give spectral gap bounds adapted to the actual distribution.
- **Weak Poincare**: Even when the spectral gap is zero, "weak Poincare inequalities" can give polynomial (rather than exponential) decay rates.

### How it might apply
The Farey fractions sit on [0,1] ≅ S¹ (the circle). The discrepancy function D(x) = #{f_j ≤ x}/|F_N| - x measures how much the empirical distribution deviates from uniform. Our W(N) = ∫|D(x)|² dx is the L² norm of D.

The Poincare inequality on the circle gives:
- ∫|D(x)|² dx ≤ (1/4π²) · ∫|D'(x)|² dx
- D'(x) is related to the density of Farey points minus 1 (the uniform density)
- When we add a prime p, we add p-1 new fractions, changing D'
- If the "gradient energy" ∫|D'|² decreases when adding a prime (because the density becomes more uniform), then W decreases too

The spectral gap version: if the Farey evolution has a positive spectral gap λ₁, then W decays at rate e^{-λ₁} per step, which is more than enough.

The discrete version might be more useful: define a graph on Farey fractions where neighboring fractions are connected. The spectral gap of this graph's Laplacian controls how fast the discrepancy decays.

**Verdict**: MODERATELY PROMISING. Natural setting (circle = [0,1]) but the Poincare inequality might give bounds that are too loose. The spectral gap approach is essentially the same as the Rayleigh quotient approach (Tool 1) viewed differently.

**Sources**:
- [Poincare inequality (Wikipedia)](https://en.wikipedia.org/wiki/Poincar%C3%A9_inequality)
- [Spectral gap and weighted Poincare inequalities](https://www.esaim-ps.org/articles/ps/pdf/2016/01/ps150019.pdf)
- [Weak Poincare inequalities without spectral gaps](https://link.springer.com/article/10.1007/s00023-019-00858-4)
- [Poincare inequality and energy of separating sets](https://arxiv.org/abs/2401.02762)

---

## Ranking: Most to Least Promising

| Rank | Tool | Why |
|------|------|-----|
| 1 | **Rayleigh Quotient** | Directly addresses ratio W(p)/W(p-1) of quadratic forms. Eigenvalue perturbation theory gives explicit bounds. Most natural fit. |
| 2 | **Schur Convexity / Majorization** | Conceptually cleanest: if adding primes majorizes the gap vector and W is Schur-convex, we're done. Needs two things proved but both seem true. |
| 3 | **Transportation-Entropy** | W(N) ≈ Wasserstein distance². Transport inequalities could bound the change, but the connection requires going through KL divergence, adding indirection. |
| 4 | **Log-Sobolev** | Most powerful if it applies (gives exponential decay), but proving the Farey evolution satisfies LSI may be as hard as the original problem. |
| 5 | **Poincare on Circle** | Natural setting but likely gives weaker bounds than Rayleigh quotient. Essentially a special case of Tool 1. |

---

## Suggested Attack Plan

### Approach A: Rayleigh Quotient (most direct)
1. Express W(N) = x^T M x where x encodes Farey fractions and M is a discrepancy matrix
2. Compute eigenvalues of M_p vs M_{p-1} using Weyl's perturbation theorem
3. The rank-(p-1) perturbation from adding φ(p) new fractions gives interlacing bounds
4. Show largest eigenvalue ratio < 1 when M(p) ≤ -3

### Approach B: Majorization (most elegant)
1. Prove that adding fractions k/p splits gaps in a way that majorizes the gap vector
2. Show W(N) is Schur-convex in the non-uniformity of gaps (likely follows from W being a sum of convex symmetric functions of the gaps)
3. Conclude ΔW ≤ 0 whenever gaps become more uniform
4. Show this happens when M(p) ≤ -3 (enough new fractions fill in large gaps)

### Approach C: Hybrid (most practical)
1. Use Schur convexity to reduce the problem to showing majorization of gaps
2. Use Rayleigh quotient bounds to handle the ratio W(p)/W(p-1) in term A
3. Use transport inequalities to bound the "information cost" of the prime insertion
4. Combine to get ΔW < 0

---

## Key Insight Across All Tools

Every tool points to the same underlying truth: **adding a prime p inserts p-1 new fractions that "fill in gaps" and make the distribution more uniform**. The different tools just measure "more uniform" differently:

- Rayleigh: smaller eigenvalues of the discrepancy matrix
- Majorization: gap vector is more mixed
- Transport: Wasserstein distance to uniform decreases
- LSI: entropy of gap distribution decays
- Poincare: gradient energy of discrepancy function decreases

The challenge is always the same: quantifying HOW MUCH more uniform, and showing it's enough to overcome the "denominator effect" (the fact that |F_p| > |F_{p-1}| changes the normalization).
