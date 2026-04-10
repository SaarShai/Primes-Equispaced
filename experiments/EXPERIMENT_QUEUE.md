# Experiment & Task Queue
Last updated: 2026-03-28

## TONIGHT (March 28-29) — Priority Order

### Q1. AMR Extended Shock Benchmark ⏱️30min
- Script: amr_shock_extended.py (fix timeout→gtimeout)
- 5 shock problems × 5 tolerances + 3 2D problems
- Validates "Farey wins on discontinuities"

### Q2. 3DGS Real Pipeline Phase 1 ⏱️1hr
- Verify imports, load bicycle scene, vanilla train 7K iter
- Pipeline at farey_3dgs/ (13 files)

### Q3. B+C Extension to p=100K ⏱️2-4hrs
- Resume bc_extend_fast2.c from p=56,209
- Extends verified range for paper

### Q4. Three-Body Unequal Mass ⏱️30min
- Extend CF analysis to 1,223 unequal-mass orbits
- Test if nobility-stability holds across mass ratios

## THIS WEEK — Priority Order

### Q5. 3DGS Phase 2: Farey vs ADC on Bicycle ⏱️8-12hrs
- Needs Q2 to pass first
- Compare at 7K and 30K iterations

### Q6. AMR Paper ⏱️writing
- "Farey AMR for Shock-Capturing"
- Outline at AMR_PAPER_OUTLINE.md

### Q7. Three-Body Paper Refinement ⏱️writing
- Draft at THREE_BODY_PAPER.md
- Add periodic table, AUC, golden ratio proof

### Q8. Aristotle Lean Submissions
- Fisher Info, Mediant, Tensor Product
- NEEDS API key setup

### Q9. B+C Analytical Proof - δ² Lower Bound ⏱️math
- Prove δ² ≥ N²/(12 log N) with all denominators
- Closes proof with Q3 computation

### Q10. SB Learning Rate on PINNs ⏱️2hrs
- CIFAR failed (cosine wins). Try physics-informed NN instead

### Q11. DARPA BAA Submission ⏱️action
- Register on BAAT, submit by April 17

## EXPLORATION BACKLOG

### Q12. 3DGS Full Benchmark (5-7 days)
### Q13. ONR White Paper
### Q14. Cognitive Radio Paper
### Q15. MIMO NTN Paper
### Q16. Conformal/Ptolemy Paper
### Q17. SB Hyperopt Enhancement
### Q18. Mesh Quality Proofs
### Q19. Compute-Saving Research (E3 broader)

## COMPLETED
- [x] SB LR CIFAR-10: Cosine 82.23%, SB 79.85%
- [x] SB Hyperopt: SB wins budget 50+ (1-5%)
- [x] AMR Demo: Zero cascading, 6x synthetic 2D
- [x] AMR Validation: Shocks 7-15x, smooth 2x loss
- [x] Three-body: AUC=0.98, figure-8=φ, periodic table
- [x] Kirkwood: r=0.95 (not novel)
- [x] Exoplanet: Farey clustering p=8.9e-28
- [x] Radio-silent report fixed
- [x] IoT report written
- [x] DARPA summary drafted
- [x] Paper: 26pp compiled
- [x] B+C to p=50K: 2,722 primes, 0 violations
- [x] Conformal: nesting yes, quality worse
- [x] Erdős-Turán: doesn't close gap

### Q20. 3D Printing Benefits Exploration ⏱️research+experiment
- Does Farey mesh reduce print time? (fewer/better triangles = faster slicing)
- Does zero-cascading help with adaptive layer height?
- Test: generate STL with Farey vs uniform mesh, compare slicer output
- Metrics: triangle count, slice time, estimated print time, watertight guarantee
- Research: current pain points in AM mesh generation

### Q21. Guth-Maynard RH Approach — Lessons for Our Proof ⏱️research
- Study Guth & Maynard's 2024 breakthrough: they proved large values of Dirichlet
  polynomials are rare, getting closer to RH without proving it
- Key technique: they bounded how often |Σ aₙ n⁻ˢ| can be large on Re(s)=1/2
- Connection to us: our Sign Theorem is equivalent to effective Franel-Landau bounds,
  which are RH-adjacent. Their "mollifier" and "large values" machinery may apply
  to bounding ΣD·δ (our cross term) or the Erdős-Turán exponential sums
- Specific questions:
  1. Can their mollifier technique sharpen our C/A lower bound?
  2. Does their "large values estimate" give a density-1 unconditional Sign Theorem?
  3. Can we adapt their approach to prove |R| < 1 for "most" primes?
- Papers: Guth-Maynard arXiv:2405.20552, Soundararajan's smooth approx to μ(n)
- This is RESEARCH ONLY — read, understand, identify if any technique transfers

### Q22. Density-1 Sign Theorem via Large Sieve ⏱️proof (HIGH PRIORITY)
- The large sieve gives: |ΣD·δ| << p · polylog(p), while Σδ² ~ p²/(12π²)
- This means R = ΣD·δ/Σδ² → 0 as p → ∞ 
- Therefore R > -1 for all sufficiently large p, giving B+C > 0
- Combined with native_decide for p ≤ 113, this would close the Sign Theorem
  for ALL primes p ≥ 11 (not just M(p) ≤ -3)
- Key step: make the large sieve constant EXPLICIT so P₀ is determined
- This is the most promising path to an unconditional proof
- Formalize in Lean with Aristotle's help

### Q23. Physics Connection: Farey Map, Quantum Chaos, and Zeta Zeros ⏱️research (HIGH INTEREST)
- Montgomery pair correlation → GUE statistics of zeta zeros
- Dyson identified this as random matrix theory (unitary ensemble)
- Connes: zeta zeros = spectrum of an unknown quantum Hamiltonian
- Keating-Snaith: RMT predicts moments of ζ and L-functions
- The Farey map is a KNOWN quantum chaotic system (transfer operator → ζ)
- **Our contribution:** ΔW(p) as a perturbation spectrum
  - D(f) = level spacing (deviation from mean density)
  - D+δ = perturbed spectrum after adding prime p
  - B+C = Σ(D+δ)² - ΣD² = change in spectral variance
  - Sign Theorem = "every prime injection increases spectral disorder"
- Specific questions:
  1. Does ΔW(p) correlate with the Farey map's Lyapunov exponent?
  2. Can the four-term decomposition be interpreted as a trace formula?
  3. Does the -1 boundary correction correspond to a "zero mode" in the perturbation?
  4. Is there an operator H_p whose spectrum encodes our D(f) values?
  5. Can Keating-Snaith moment formulas predict the distribution of R(p)?
- Papers: Boca-Cobeli-Zaharescu (Farey fractions & billiards), 
  Lewis-Zagier (period functions), Mayer (transfer operator of Gauss/Farey map)
- This could elevate the paper from "computational discovery" to "conceptual framework"

### Q24. Perturbation Positivity Proof: Σ(D+δ)² > ΣD² ⏱️proof (HIGH PRIORITY, Aristotle)
- Geometric identity: B+C = Σ(D+δ)² - ΣD²
- B+C > 0 ⟺ adding δ to D increases L2 norm
- Physical interpretation: prime perturbation increases spectral disorder
- This is equivalent to: Cov(D, δ) > -Var(δ)/2
- Proof strategies:
  1. Show D and δ are "nearly orthogonal" (weak correlation)
     - Smooth-rough lemma: ΣD_smooth·δ = 0 exactly
     - Only D_rough contributes to cross term
     - D_rough has smaller L2 than D, so cross term is bounded
  2. Show δ is "small" relative to D in the right norm
     - δ depends on LOCAL structure (p mod b)
     - D depends on GLOBAL structure (all denominators)
     - Independence argument → Cov ≈ 0
  3. Direct: show Σ(D+δ)²/ΣD² > 1 using the bridge identity
     - Σe^{2πipf} = M(p)+2 constrains the Fourier structure
- Formalize in Lean with Aristotle's help
- Already submitted geometric identity to Aristotle (task 71338a14)
- Next: submit the orthogonality/independence argument

### Q25. Displacement-Guided 3DGS Densification ⏱️experiment (HIGH PRIORITY)
- Current Farey 3DGS uses classical mediant insertion (gap-filling)
- Novel idea: use D(f) = rank(f) - n·f as a LOCAL ERROR ESTIMATOR
  - High |D(f)| at a Gaussian → poor approximation → densify here
  - This directly connects our ΔW theory to the practical application
  - Makes the 3DGS method genuinely leverage our novel discoveries, not just classical Farey
- Implementation:
  1. After each densification step, compute D(f) for each Gaussian position
  2. Gaussians with high |D| get priority for splitting/cloning
  3. Compare D-guided vs pure mediant-guided vs standard ADC
- Expected benefit: smarter allocation of Gaussian budget to under-resolved regions
- This would be the first 3DGS method with NUMBER-THEORETIC error guidance
- Uses: N1 (per-step discrepancy), N3 (injection principle)

### Q26. Circle to Sphere: Higher-Dimensional Farey Equidistribution ⏱️research
- Our discoveries live on S¹ (Farey fractions on [0,1])
- Can we extend to S² (sphere)?
- Direction A: Tensor product (Farey × Farey on torus T²) — already started
- Direction B: Rational points on S² via sum-of-squares (Duke's theorem)
  - Points (a/q, b/q, c/q) with a²+b²+c² = q²
  - Equidistribution proved by Duke (1988) — but per-step analysis (our ΔW) is new
  - r₃(n) = number of representations connects to Mertens-like sums
- Direction C: SL(3,ℤ) / higher-rank groups → Farey-like structures on symmetric spaces
- Direction D: Spherical harmonics bridge identity
  - On S¹: Σ e^{2πipf} = M(p)+2 (our bridge identity)
  - On S²: Σ Y_ℓ^m(rational points) = ??? (new identity?)
  - Would connect to automorphic forms on GL(3)
- Key question: does our per-step discrepancy ΔW have an analog for sphere packing?
  - If yes: applications to crystallography, wireless antenna arrays, etc.
- Papers: Duke (1988), Linnik (ergodic method), Iwaniec (spectral methods)

### Q27. Rational Points on S² — Per-Step Equidistribution ⏱️research+experiment
- Duke (1988) proved rational points (a/q, b/q, c/q) with a²+b²+c²=q² equidistribute on S²
- Our novel angle: per-step analysis (ΔW analog) as q increases through primes
- Compute: for each prime p, how does the "spherical wobble" change when adding points at level p?
- Key formula: r₃(p) = number of representations p = a²+b²+c² (connects to class numbers)
- Bridge identity analog: Σ Y_ℓ^m(rational points at level q) = ??? 
- If ΔW_sphere(p) < 0 for all primes: extends our Sign Theorem to S²
- Practical applications: antenna arrays, satellite constellations, molecular structures
- Papers: Duke (1988), Linnik ergodic method, Iwaniec spectral methods
- Start with: compute r₃(p) for primes, plot equidistribution, measure spherical discrepancy

### Q28. SL(3,ℤ) Farey Structures on Modular Surface ⏱️research (extends Mayer)
- Our Farey sequences connect to SL(2,ℤ) acting on H² (hyperbolic plane)
- The Farey tessellation IS a fundamental domain decomposition of H²/SL(2,ℤ)
- Extension: SL(3,ℤ) acts on the symmetric space SL(3,ℝ)/SO(3)
- "Higher Farey fractions" = cusps of SL(3,ℤ)\SL(3,ℝ)/SO(3)
- The Mayer transfer operator generalizes to higher-rank groups (Mayer-Mühlenbruch)
- Key question: does the BCZ horocycle flow have an SL(3) analog?
  - If yes: our per-step ΔW might generalize to a higher-dimensional spectral rigidity
- This connects to Langlands program (automorphic forms on GL(3))
- Extends the Mayer spectral analysis (MAYER_SPECTRAL_PROOF.md)
- Papers: Mayer-Mühlenbruch (higher Selberg zeta), Goldfeld (automorphic forms on GL(3))

### Q29. Duke-Linnik-Waldspurger Deep Dive ⏱️research (QUEUED FOR LATER)
- Duke's theorem (1988): equidistribution of lattice points on S² via half-integral weight forms
- Linnik's ergodic method: original approach to S² equidistribution via ergodic theory
- Waldspurger formula: connects central L-values to Fourier coefficients of half-integral weight forms
- Connection to us: theta series θ_P(z) = Σ r₃(n,P) q^n is a modular form
  - This is the S² analog of our bridge identity
  - The per-step analysis ΔW_sphere(p) would use changes in theta coefficients at primes
- Not urgent — depends on Q27 (S² computation) results first
- Papers: Duke (Inventiones 1988), Waldspurger (J. Math. Pures Appl. 1981),
  Iwaniec "Spectral Methods of Automorphic Forms" (2002)

### Q30. 3DGS Real Benchmark Pipeline ⏱️experiment (REQUIRED FOR PUBLICATION)
- Must test on standard benchmarks: Mip-NeRF 360 (9 scenes), Tanks & Temples (2), Deep Blending (2)
- Multiple seeds: 5 random seeds per config, report mean ± std
- Budget-matched comparison: compare all methods at EQUAL Gaussian count
- Real rendering pipeline: gsplat or diff-gaussian-rasterization, not density field matching
- Metrics: PSNR, SSIM, LPIPS, Gaussian count, training time
- This is non-negotiable for publication — synthetic results alone won't be accepted

### Q31. Silent Coordination for Chip/Data-Center Architecture ⏱️research+prototype (HIGH VALUE)
- On-chip (NoC): Farey-scheduled core access → zero arbitration overhead
- Cache coherence: deterministic Farey schedule replaces reactive snooping
- Data centers: cross-DC coordination without messages (50-150ms latency eliminated)
- RDMA/CXL: contention-free access to pooled memory
- Key property: zero communication + zero collision + zero cascading on node add/remove
- Prototype: simulate a 16-core NoC with Farey vs round-robin vs random scheduling
- Measure: arbitration cycles saved, power reduction, throughput improvement
- Patent potential: "Method for communication-free resource coordination using number-theoretic scheduling"
- NOT quantum — purely classical shared-schedule coordination

### Q32. 3D Point Cloud via Hilbert Curve + Farey ⏱️experiment (QUICK TEST)
- Map 3D point cloud to 1D via Hilbert curve ordering
- Apply Farey densification along the 1D ordering
- Map back to 3D
- Compare to direct 3D densification and random insertion
- HilComp (ICIC 2025) validates Hilbert ordering preserves spatial coherence
- Estimated: 1-2 days. Quick kill-or-promote test.

### Q33. IoT Edge Farey Sampling Prototype ⏱️prototype (HIGH MARKET VALUE)
- Target: adaptive sampling on constrained IoT devices
- Farey properties: deterministic, lightweight (no ML), certifiable, zero-communication
- Prototype: simulate N sensors sampling a 1D signal at Farey-scheduled positions
- Compare to uniform, random, and simple adaptive (Nyquist-based)
- Metrics: reconstruction SNR, sample count, computational overhead
- Market: $100-500M addressable, 15%+ CAGR

### Q34. ECG/EEG Farey Compression Test ⏱️experiment (MEDICAL VALUE)  
- Farey-based adaptive sampling of ECG/EEG signals
- Use PhysioNet MIT-BIH dataset (free, standard benchmark)
- Compare to wavelet compression and CS (compressed sensing)
- Key advantage: provable reconstruction + lightweight for wearables
- Market: $20-100M, fast growth in wearable health

### Q35. LiDAR Scan-Line Densification ⏱️experiment (AUTONOMOUS DRIVING)
- Each LiDAR scan line is 1D — Farey's sweet spot
- Densify sparse scan lines using Farey mediant insertion
- Compare to bilinear interpolation and learned upsampling
- Use KITTI or nuScenes dataset (standard AV benchmarks)
- Market: $50-300M, 41-50% CAGR

### Q36. Silent Coordination: The Surviving Unique Application ⏱️research+prototype (PRIORITY)
- Farey's ONE truly unique property: N agents compute non-colliding schedules independently
- Each agent needs only (my_id, N) — no communication, no coordinator, no GPS
- Adding agent N+1: slots into largest gap, ZERO disruption to existing agents
- F_N ⊂ F_{N+1} guarantees backward compatibility
- Target domains:
  1. Underwater sensor networks (acoustic comm is 1500 m/s, expensive)
  2. Satellite constellations (light-speed delays)
  3. Military radio silence scenarios
  4. Swarm robotics (bandwidth-limited)
  5. Emergency/disaster networks (no infrastructure)
- Compare to: TDMA (rigid), ALOHA (37% efficiency), GPS-sync (requires GPS)
- Key claim: 100% utilization + zero disruption + zero communication
- This merges IoT coordination + the scheduling angle
- Prototype: simulate N=100 underwater sensors, measure utilization vs TDMA/ALOHA

### Q37. Physics Framing: Gutzwiller + BCZ + Spectral Rigidity ⏱️paper (ADD TO MAIN PAPER)
- Add subsection connecting four-term decomposition to Gutzwiller trace formula structure
- Cite BCZ weak mixing result (2024) as evidence Farey dynamics are genuinely chaotic
- State conjecture: "Sign Theorem = discrete analog of spectral rigidity monotonicity in quantum chaotic systems"
- This is FRAMING for broader audience (physicists), not new theorems
- Target: Section 4.X in main.tex

### Q38. Convergence Rate Theorem for Stern-Brocot Insertion ⏱️proof (Aristotle)
- After K Stern-Brocot insertions, what is max_gap(K)?
- Known: midpoint gives max_gap = 1/2^{ceil(log2(K+1))}
- Farey: max_gap(K) = ? (should be expressible via Stern-Brocot tree depth)
- This gives a quantitative guarantee for 3DGS: "after K densification steps, coverage gap ≤ f(K)"
- Formalize in Lean with Aristotle

### Q39. Ramanujan Signal Processing Connection ⏱️research (PROMISING)
- Vaidyanathan & Tenneti (Caltech): "Farey dictionaries" for periodic signal detection
- Ramanujan filter banks use c_q(n) — exactly our bridge identity's building blocks
- Our bridge: Σ e^{2πipf} = M(p)+2 = Σ_{q≤p-1} c_q(p) + 2
- Could our per-step analysis ΔW(p) improve Ramanujan period estimation?
- Read: Vaidyanathan 2020 Phil. Trans. paper, ICASSP Farey dictionary paper
- This is a REAL research community (IEEE Signal Processing) we could contribute to

### Q40. Adaptive Ramanujan Filter Bank Proof-of-Concept ⏱️experiment (1 week)
- Use M(q) ordering to prioritize Ramanujan filters (instead of sequential q=1,2,3...)
- The Sign Theorem tells us: primes with M(p)≤-3 have the strongest spectral impact
- Test: synthetic periodic signal in noise, compare:
  - Sequential ordering: apply filters q=1,2,3,...,Q until period detected
  - M(q)-ordered: apply filters sorted by |M(q)| descending (strongest impact first)
- Metric: how many filters needed for 95% detection accuracy?
- KILL if: <10% savings. GO if: >10% savings → target ICASSP
- Note: bridge identity itself is known (Planat 2002). OUR contribution is the adaptive ordering.

### Q41. R > -1/2 Proof: Per-Denominator Approach ⏱️proof (Aristotle)
### Q42. R > -1/2 Proof: Fourier h=1 Dominance ⏱️proof (Aristotle)
### Q43. R Cancellation Structure Analysis ⏱️research (Agent)
### Q44. 3BP Extended Periodic Table with Unequal Mass ⏱️analysis (Agent)
### Q45. 3BP New Orbit Discovery via CF Framework ⏱️experiment (Agent)
### Q46. Density-1 Computational Verification ⏱️proof (Aristotle)
### Q47. 3BP m3=4 Correlation Reversal Investigation ⏱️analysis (part of Q44)
### Q48. Hristov Free-Group Words (email or compute) ⏱️action
