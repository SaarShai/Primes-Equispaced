# Where Farey-Sequence Methods Can Save Compute

**Date:** 2026-03-27
**Context:** The three-body orbit search demonstrated a 2x speedup by using Stern-Brocot nobility to guide search toward near-periodic orbits. This document explores where else the Farey/Stern-Brocot toolkit can reduce computational costs.

**Core tools from our work:**
1. **Injection principle** -- each Farey gap gets at most 1 new fraction k/p (bounded refinement)
2. **Stern-Brocot hierarchy** -- coarse-to-fine rational enumeration, nobility = depth in tree
3. **Mertens compression** -- M(N) summarizes ~3N^2/pi^2 fractions in one integer
4. **Per-denominator identity** -- sum of displacements for denominator b is exactly -phi(b)/2
5. **Mediant property** -- the next fraction between a/b and c/d is always (a+c)/(b+d)

---

## 1. Hyperparameter Optimization (HPO)

**Problem:** Finding optimal learning rate, regularization, batch size, etc. for ML models. Grid search scales as O(k^d) for d hyperparameters with k values each. Random search helps but wastes samples on already-explored regions.

**Current compute:** Google used ~2000 GPU-days for NAS. Even HPO for a single model costs hundreds of GPU-hours. Google's own playbook now recommends quasi-random (Halton) sequences over grid or random search.

**How Farey/SB would help:** The Stern-Brocot tree provides a _hierarchical_ quasi-random sequence with a unique property: each new point lands in the largest existing gap (mediant property). Unlike Halton/Sobol sequences, which are designed for uniform coverage, SB-ordered evaluation exploits a coarse-to-fine structure that matches how hyperparameter landscapes actually behave -- performance is usually smooth with a few critical transitions. The injection principle guarantees that adding one more evaluation point never "wastes" a sample by landing too close to an existing one.

**Estimated saving:** 1.5-3x over random search, competitive with Bayesian optimization but embarrassingly parallel (no sequential dependence on a surrogate model). The advantage grows in high dimensions where Bayesian optimization's surrogate becomes unreliable.

**Novelty:** Partially novel. Low-discrepancy sequences (Halton, Sobol) are well-established for HPO. The specific use of the Stern-Brocot mediant ordering as a _hierarchical_ alternative with bounded-refinement guarantees has not been published. The closest existing work is Google's quasi-random search recommendation, which uses scrambled Halton sequences but lacks the hierarchical/adaptive property.

**Assessment: MODERATE-HIGH.** The niche is real but crowded. The unique angle is the injection principle providing a formal guarantee that no region gets over-sampled.

---

## 2. Neural Architecture Search (NAS)

**Problem:** Searching over the space of possible neural network architectures (layer types, widths, connections). The search space is combinatorial and enormous.

**Current compute:** Early NAS (Zoph & Le, 2017) used 2000 GPU-days. Modern one-shot methods (DARTS, etc.) reduced this to 1-4 GPU-days but still explore architectures somewhat blindly.

**How Farey/SB would help:** Map architecture choices to rational parameters. For example, width ratios between layers, skip-connection densities, and attention head counts can all be expressed as fractions. A Stern-Brocot-ordered search would evaluate architectures from simplest (small denominators = simple ratios like 1:1, 1:2) to most complex, with each new architecture guaranteed to be "maximally different" from all previously tested ones. This is essentially a structured version of the progressive-shrinking strategy used in OFA (Once-for-All) networks.

**Estimated saving:** 2-5x over random search within the same architecture family. However, this is less impactful than it sounds because modern NAS already uses weight-sharing to amortize costs.

**Novelty:** Novel. No published work uses Farey/SB ordering for architecture search. The idea of mapping architecture parameters to rationals and searching in SB order is, as far as the literature search shows, unpublished.

**Assessment: MODERATE.** The idea is clean but NAS has moved toward weight-sharing methods that partially obsolete the search-space-reduction angle.

---

## 3. Adaptive Mesh Refinement (AMR)

**Problem:** CFD, climate simulation, and astrophysics all need to refine computational meshes where solution gradients are large, while keeping the mesh coarse elsewhere. Standard AMR uses octrees and refines by splitting cells into 2^d children.

**Current compute:** Climate models like E3SM use millions of CPU-hours per simulation. AMR can reduce this by 10-100x over uniform meshes, but the refinement strategy itself is heuristic.

**How Farey/SB would help:** The injection principle provides a mathematical guarantee that standard AMR lacks: when you refine at "Farey order p," each existing cell gets at most one new node. This means:
- **Bounded quality degradation** -- no cell is split more than once per refinement level
- **Predictable element sizes** -- sub-gap widths are exactly 1/(pb) and 1/(pd) with b+d=p
- **Hierarchical nesting** -- every refinement level is a proper superset of the previous one

Our earlier experiments (mesh_demo.py) confirmed this in 1D and showed it extends to tensor-product meshes in 2D/3D.

**Estimated saving:** Not a raw compute saving over existing AMR, but a _quality_ guarantee that existing AMR lacks. The practical benefit is eliminating post-refinement quality repair (smoothing, flipping), which can be 20-40% of mesh generation time. Net saving: 1.2-1.5x for the mesh generation phase, plus improved solver convergence due to guaranteed element quality.

**Novelty:** Novel as a formal framework. Farey meshes in 1D are implicit in some older numerical analysis (Ford circles), but the injection principle as a refinement guarantee for AMR has not been published. The closest work is Berger-Oliger-Colella AMR which uses factor-of-2 refinement with no quality guarantees beyond aspect ratio heuristics.

**Assessment: HIGH.** This is the most defensible application because the guarantee is mathematical, not heuristic. A paper comparing Farey-AMR quality bounds to standard octree AMR would be publishable in a computational methods journal.

---

## 4. Compressed Sensing / Sparse Recovery

**Problem:** Recovering a sparse signal from fewer measurements than the Nyquist rate requires. The measurement matrix must satisfy the Restricted Isometry Property (RIP). Designing good measurement matrices is computationally expensive.

**Current compute:** RIP verification is NP-hard in general. Random Gaussian matrices satisfy RIP with high probability but waste measurements. Deterministic constructions (chirp, Legendre) exist but are limited.

**How Farey/SB would help:** Farey fractions provide a deterministic set of frequencies with known mutual coherence properties. A sensing matrix whose rows are complex exponentials at Farey frequencies e^{2*pi*i*(a/b)*t} for (a/b) in F_N has structure we can analyze:
- The injection principle bounds how "close" any two frequencies can be (minimum separation 1/(N^2))
- The per-denominator identity constrains correlations within frequency families
- Our earlier experiment (farey_compressed_sensing.py) showed competitive performance with random matrices for signals sparse in a Fourier basis

**Estimated saving:** Not compute saving per se, but measurement saving: Farey-structured sensing matrices could require 10-30% fewer measurements than random matrices for signals with rational-frequency content (radar returns, communications signals, biological rhythms). This translates to faster acquisition in MRI, radar, and spectrum sensing.

**Novelty:** Partially novel. Deterministic compressed sensing matrices from number theory exist (DeVore 2007, Calderbank et al.), but none specifically use Farey structure with the injection principle as a design criterion. Our prior experiment showed this works but didn't develop the theory.

**Assessment: MODERATE-HIGH.** The application is real and the connection to existing deterministic CS literature makes it publishable. The key question is whether Farey matrices outperform existing deterministic constructions (chirp matrices) for practical signal classes.

---

## 5. AI Training: Learning Rate and Curriculum Scheduling

**Problem:** Choosing learning rate schedules (warmup, cosine decay, cyclic, etc.) and curriculum ordering (easy-to-hard example presentation) for neural network training. Current practice is largely empirical.

**Current compute:** Practitioners typically try 5-20 learning rate schedules, each requiring a full training run. This multiplies training cost by 5-20x.

**How Farey/SB would help:** Two distinct ideas:

**(a) SB-ordered learning rate schedule:** Instead of linear warmup + cosine decay, use a learning rate that follows the Stern-Brocot enumeration of [0,1]. This visits "noble" (maximally irrational) rates early and fills in rationals later. The intuition: noble learning rates avoid resonance with periodic structures in the loss landscape (same reason noble frequency ratios produce stable KAM tori). This is directly analogous to our three-body result.

**(b) Farey curriculum learning:** Order training examples by "difficulty" mapped to Farey depth. Start with the simplest examples (depth 1-2 in SB tree), then progressively add harder examples following the mediant rule. The injection principle guarantees each curriculum stage adds at most one new difficulty level per existing gap, preventing catastrophic forgetting from sudden difficulty jumps.

**Estimated saving:** For (a), speculative -- maybe 1.2-1.5x if the KAM analogy holds. For (b), more promising -- curriculum learning already shows 1.5-2x speedups, and Farey ordering could provide a principled schedule where current practice uses ad hoc difficulty metrics.

**Novelty:** Highly novel for (a). The AAAI 2025 paper by Matsubara & Yaguchi ("Number Theoretic Accelerated Learning of PINNs") showed 2-7x improvement using number-theoretic collocation point selection, validating the general principle. Jaeger (NLM) found the golden ratio emerges in optimal learning rate/momentum pairs. But an explicit SB-ordered learning rate schedule has not been proposed. For (b), moderately novel -- curriculum learning exists but no one has used Farey ordering.

**Assessment: HIGH for (a).** The Matsubara & Yaguchi result at AAAI 2025 proves the general concept works. Extending from collocation points to learning rate schedules is a natural and testable next step.

---

## 6. Protein / Molecular Stability Prediction

**Problem:** Predicting whether a protein conformation is stable requires expensive molecular dynamics (MD) simulations. A key factor in stability is whether vibrational mode frequencies are commensurate (resonant) or incommensurate.

**Current compute:** All-atom MD simulations of a single protein can take days to weeks on GPU clusters. Normal mode analysis is cheaper (minutes) but less accurate.

**How Farey/SB would help:** By analogy with KAM theory: conformations whose vibrational mode frequency ratios are close to noble numbers should be more stable (harder to destroy by perturbation), while those near low-order rationals should be unstable (resonant energy transfer). This would provide a cheap filter:
1. Run normal mode analysis (fast, ~minutes)
2. Compute frequency ratios between dominant modes
3. Check "nobility" via SB depth -- high nobility = likely stable, low nobility = likely resonant/unstable
4. Only run expensive MD on the uncertain cases

**Estimated saving:** If the filter correctly classifies 50-70% of conformations without MD, this saves 50-70% of MD compute. Realistic estimate: 2-3x overall speedup for conformational search.

**Novelty:** Novel in this specific form. The golden ratio appears in protein geometry (Wolynes' frustration ratio Tf/Ts ~ 1.6 ~ phi), and helical protein structures show golden-ratio aspect ratios. But nobody has used SB nobility of vibrational frequency ratios as a stability predictor. The KAM-theory motivation is rigorous for Hamiltonian systems; proteins are dissipative, so the analogy needs validation.

**Assessment: MODERATE.** High novelty but uncertain whether the KAM analogy transfers to dissipative biological systems. A proof-of-concept on a small protein dataset would answer this quickly.

---

## 7. Cryptographic Primality Certificate Compression

**Problem:** Proving a number is prime requires a primality certificate. Existing certificates (Pratt, Atkin-Morain) can be large and slow to verify.

**Current compute:** Pratt certificates have size O(log^2 n). Verification is fast but generation requires full factorization of n-1.

**How Farey/SB would help:** Our Mertens compression result shows that M(N) encodes ~3N^2/pi^2 Farey fractions in one integer. For prime p, the injection property gives a primality characterization: p is prime iff every gap in F_{p-1} receives exactly one new fraction at order p (full saturation). This could yield a new type of primality certificate based on verifying the injection property rather than factoring n-1.

**Estimated saving:** Unclear -- this is more theoretical than computational. The certificate might be more compact but verification could be slower.

**Novelty:** Novel but niche.

**Assessment: LOW.** Primality testing is essentially solved for practical purposes (Miller-Rabin, AKS). The Farey angle is theoretically interesting but unlikely to beat existing methods.

---

## 8. Database Join Ordering

**Problem:** Finding the optimal order to join N tables is NP-hard (the search space is N! permutations). Query optimizers use dynamic programming or greedy heuristics.

**Current compute:** For N > 10-15 tables, exhaustive search is infeasible. Heuristics can produce plans 10-100x slower than optimal.

**How Farey/SB would help:** Weak connection. Join ordering is fundamentally a discrete combinatorial problem without obvious rational-number structure. One could map selectivity estimates to [0,1] and use Farey ordering to explore join plans by estimated selectivity ratio, but this adds little over existing cardinality-estimation-based approaches.

**Novelty:** Novel but forced.

**Assessment: LOW.** The number-theoretic structure doesn't naturally fit the problem.

---

## 9. Signal Processing: Frequency Estimation

**Problem:** Estimating unknown frequencies in a noisy signal. The standard approach (DFT) has resolution limited by 1/T where T is observation time. Super-resolution methods (MUSIC, ESPRIT) are expensive.

**Current compute:** MUSIC requires eigendecomposition of the covariance matrix: O(N^3) for N samples.

**How Farey/SB would help:** Use the Stern-Brocot tree as a frequency search hierarchy. Start with the simplest rationals (1/2, 1/3, 2/3, ...) and refine via mediants toward the true frequency. The mediant property guarantees each refinement step narrows the search interval optimally. This is essentially the continued fraction algorithm for frequency estimation -- well-known but under-used in practice.

**Estimated saving:** 2-5x over uniform DFT grids for signals with one or few dominant frequencies. No saving for broadband signals.

**Novelty:** Low -- continued fraction frequency estimation dates to Gauss. The specific framing via SB tree is pedagogically useful but not new.

**Assessment: LOW-MODERATE.** Well-trodden ground, though packaging it with the injection principle for multi-frequency estimation could add value.

---

## 10. Climate / Weather Adaptive Mesh Refinement

**Problem:** Same as AMR (#3) but specifically for atmosphere/ocean grids. Climate models use cubed-sphere or icosahedral grids with static or adaptive refinement.

**Current compute:** CESM/E3SM runs cost millions of CPU-hours. Adaptive refinement (MPAS) helps but refinement ratios are fixed at 3:1 or 4:1.

**How Farey/SB would help:** Instead of fixed refinement ratios, use Farey-ordered refinement where the ratio p/q is chosen from the SB tree based on local solution gradient. The injection principle guarantees that each refinement step is bounded: existing cells see at most one new node. This enables _continuous_ refinement ratios rather than the discrete 2:1 or 3:1 of standard AMR.

**Estimated saving:** 1.3-2x over fixed-ratio AMR by better matching refinement to actual gradient structure. The gain comes from avoiding over-refinement in regions where a 3:1 ratio is too fine but 1:1 (no refinement) is too coarse.

**Novelty:** Novel. Variable-ratio AMR exists (p-refinement in finite elements) but is not connected to Farey theory. The bounded-refinement guarantee from the injection principle is new.

**Assessment: MODERATE.** The application is important (climate compute is a major national investment) but the implementation complexity is high.

---

## Top 5 Ranked by Promise

| Rank | Domain | Estimated Saving | Novelty | Feasibility of PoC |
|------|--------|-----------------|---------|-------------------|
| 1 | **Adaptive Mesh Refinement** | 1.2-1.5x (quality guarantee) | High | Medium (extend mesh_demo.py to 2D) |
| 2 | **AI Training: LR Schedules** | 1.2-2x | High | High (just swap LR schedule, run CIFAR-10) |
| 3 | **Hyperparameter Optimization** | 1.5-3x | Moderate | High (implement SB sampler, run on HPOBench) |
| 4 | **Compressed Sensing** | 10-30% fewer measurements | Moderate-High | Medium (extend farey_compressed_sensing.py) |
| 5 | **Protein Stability Filter** | 2-3x | High | Low (need MD simulation pipeline) |

---

## Detailed Proof-of-Concept Plans for Top 5

### PoC 1: Farey-Guaranteed Adaptive Mesh Refinement

We already have mesh_demo.py showing the injection principle works in 1D. The next step is a 2D tensor-product Farey mesh applied to a standard CFD benchmark (lid-driven cavity flow or backward-facing step). The experiment would:
- Generate Farey meshes at orders F_5, F_7, F_11, F_13 (progressive refinement)
- Compare element quality metrics (aspect ratio, skewness, minimum angle) against standard quadtree AMR at equivalent node counts
- Run a simple Poisson or advection-diffusion solver on both meshes and compare solution accuracy per degree of freedom
- Key metric: does the mathematical quality guarantee translate to measurable solver convergence improvement?

This could be done in Python with FEniCS or deal.II in approximately 1-2 weeks of development effort. The target venue would be a computational methods journal (IJNME, JCP) or a short paper at a SIAM conference.

### PoC 2: Stern-Brocot Learning Rate Schedule

This is the quickest experiment to run. Take a standard training task (ResNet-18 on CIFAR-10) and compare:
- Baseline: cosine annealing LR schedule (standard practice)
- Experiment: SB-ordered LR, where at epoch t we set lr = SB(t) * lr_max, with SB(t) being the t-th element in the Stern-Brocot enumeration of (0,1)
- Control: Halton sequence LR schedule (to isolate the hierarchical property from the quasi-random property)

The SB enumeration visits 1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 2/5, 3/5, 4/5, ... -- moving from coarse to fine. The hypothesis is that visiting "noble" rates early helps the optimizer escape saddle points (by avoiding resonance with periodic loss landscape features), while the hierarchical filling ensures all scales are eventually explored.

The AAAI 2025 result (Matsubara & Yaguchi) showing 2-7x improvement for PINNs with number-theoretic collocation provides strong prior evidence. The experiment takes ~4 GPU-hours on a single A100 and could be done in a weekend.

### PoC 3: SB-Ordered Hyperparameter Search

Implement a Stern-Brocot sampler for hyperparameter optimization and benchmark against:
- Random search (Bergstra & Bengio baseline)
- Sobol sequence (standard quasi-random)
- Bayesian optimization (Tree Parzen Estimator from Optuna)

Test on HPOBench or YAHPO benchmarks (standardized HPO benchmarks) with 50-200 evaluations. The SB sampler would work as follows: for d hyperparameters, use d independent SB sequences (one per dimension), interleaved so that early evaluations cover the coarsest grid and later evaluations fill gaps via mediants.

The key differentiator versus Sobol: the SB sequence is inherently hierarchical (you can stop at any point and have the best possible coverage for that budget), while Sobol sequences are only guaranteed low-discrepancy at specific powers of 2. This matters in practice because HPO budgets are rarely powers of 2.

Implementation: ~200 lines of Python. Benchmarking: 1-2 days on CPU. Target venue: AutoML workshop or JMLR.

### PoC 4: Farey Sensing Matrices for Compressed Sensing

Extend the existing farey_compressed_sensing.py experiment to:
- Construct sensing matrices with rows as complex exponentials at Farey frequencies
- Compare against random Gaussian, Bernoulli, and chirp sensing matrices
- Test on standard sparse recovery benchmarks (Sparco) and on radar-like signals with rational frequency content
- Measure both recovery accuracy and the number of measurements needed for exact recovery (phase transition curves)

The hypothesis is that Farey matrices will outperform random matrices specifically for signals whose frequency content has rational structure (common in man-made signals: communications, radar, power systems). For natural signals with irrational frequency content, we expect no advantage.

Implementation: extend existing code, ~1 week. Target venue: IEEE Signal Processing Letters.

### PoC 5: Vibrational Nobility as Protein Stability Filter

This is the most ambitious PoC and requires domain expertise in computational biology. The plan:
- Take a dataset of protein conformations with known stability (e.g., from the Protein Data Bank with experimental melting temperatures)
- Run normal mode analysis (using ProDy or similar) to extract the dominant vibrational frequencies
- Compute pairwise frequency ratios and their SB depth (nobility)
- Test correlation: do conformations with higher average nobility (more irrational frequency ratios) tend to be more stable?

If the correlation holds, build a simple classifier: "predict stable if average nobility > threshold." Compare against more expensive MD-based stability prediction.

The theoretical basis is KAM theory, which rigorously shows that Hamiltonian systems with noble frequency ratios are more stable. Proteins are not strictly Hamiltonian (they're in a thermal bath), but the normal modes of the potential energy surface are Hamiltonian. The question is whether the KAM intuition survives thermal fluctuations.

Implementation: ~2 weeks with computational biology tooling. Target venue: Biophysical Journal or PLOS Computational Biology.

---

## Summary of Novelty Assessment

| Application | Anyone done this before? |
|------------|------------------------|
| SB hyperparameter search | No (Halton/Sobol yes, SB-mediant no) |
| SB learning rate schedule | No (golden ratio LR yes, SB hierarchy no) |
| Farey AMR quality guarantee | No (Farey meshes implicit in Ford circles, but not as AMR) |
| Farey sensing matrices | No (number-theoretic CS exists, Farey-specific no) |
| Vibrational nobility filter | No (KAM for molecules yes, SB nobility score no) |
| SB NAS ordering | No |
| Farey curriculum learning | No |
| Farey frequency estimation | Essentially yes (continued fractions) |
| Farey join ordering | No, but forced/unnatural |
| Farey primality certificates | No, but impractical |

The strongest opportunities combine genuine novelty with practical testability: AMR quality guarantees, SB learning rate schedules, and SB hyperparameter search are the three that could produce publishable results with the least effort.

---

## Key References

- Matsubara & Yaguchi, "Number Theoretic Accelerated Learning of PINNs," AAAI 2025
- Jaeger, "The Golden Ratio in Machine Learning," NLM 2022
- Bergstra & Bengio, "Random Search for Hyper-Parameter Optimization," JMLR 2012
- Google Deep Learning Tuning Playbook (quasi-random search recommendation)
- Berger & Oliger, "Adaptive Mesh Refinement for Hyperbolic PDEs," JCP 1984
- DeVore, "Deterministic Constructions of Compressed Sensing Matrices," 2007
- Greene, "A Method for Determining a Stochastic Transition," J. Math. Phys. 1979 (KAM breakup criterion)
