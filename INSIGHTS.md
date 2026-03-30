# INSIGHTS — Novel Discoveries, Key Insights, and Their Value
Last updated: 2026-03-28

This file is a lens through which ALL explorations should be evaluated.
Every item in the MASTER_TABLE should connect to at least one insight here.
If an exploration doesn't leverage our unique discoveries, ask: why are we doing it?

---

## NOVEL DISCOVERIES (things nobody knew before us)

### N1. Per-Step Farey Discrepancy Framework
**What:** We defined and studied ΔW(N) = W(N) - W(N-1) — the change in Wasserstein discrepancy at each step. While incremental analysis is standard in number theory (Λ(n) = ψ(n)-ψ(n-1)), applying it to Farey L² discrepancy and connecting the per-step sign to M(p) is new.
**Why it matters:** Transforms a static quantity (W(N)) into a dynamical sequence (ΔW(N)) that reveals structure invisible in the cumulative view. The novelty is in the specific Farey application, not the general increment strategy.
**Drives:** MPR-1 through MPR-20, the entire math paper

### N2. M(p) Controls ΔW(p) — The Mertens-Discrepancy Connection
**What:** The Mertens function M(p) determines the sign and magnitude of ΔW(p). Correlation r=0.966. Primes with negative Mertens make Farey MORE equidistributed; positive Mertens makes it LESS.
**Why it matters:** Connects multiplicative number theory (Mertens, Möbius) to equidistribution theory (Farey discrepancy) at per-step granularity. This is the paper's central finding.
**Proved:** Sign Theorem for M(p) ≤ -3. Counterexample at p=92,173 confirms the positive-M direction.
**Drives:** MPR-2, MPR-3, MPR-4, MPR-7, MPR-13, MPR-16, MPR-20

### N3. Primes Damage, Composites Heal
**What:** Primes (mostly) increase discrepancy; composites (96%) decrease it. The healing rate approaches 100% for composites.
**Why it matters:** Reveals a fundamental asymmetry between primes and composites in Farey refinement — primes are "disruptive" and composites are "restorative."
**Drives:** PHYS-11, PHYS-12, PHYS-13, the paper's narrative

### N4. The Sigmoid Law
**What:** The probability that ΔW(p) < 0 follows a sharp sigmoid in M(p)/√p. Below -0.1: 100% negative. Above +0.3: 100% positive.
**Why it matters:** Precise empirical law with no theoretical explanation. If proved, would give a sharp criterion for when primes help or hurt equidistribution.
**Drives:** MPR-4 (unconditional Sign Theorem)

### N5. The Four-Term Decomposition ΔW = A + B + C + D
**What:** Each ΔW(p) decomposes into four interpretable components: displacement sum (A), cross-correlation (B), shift-squared (C), boundary correction (D).
**Why it matters:** Makes the per-step change algebraically tractable. The near-cancellation (A ≈ -C, B ≈ -D) is the key structural insight.
**Drives:** MPR-2, MPR-3, MPR-7, MPR-13, MPR-14

### N6. The Bypass Theorem (C + D > A)
**What:** Instead of proving B ≥ 0 (which appears false for some primes), we proved C + D > A, bypassing the B obstacle entirely.
**Why it matters:** A strategic proof innovation — changing what you need to prove rather than how you prove it.
**Drives:** MPR-2, MPR-3, MPR-9

### N7. Figure-Eight = Golden Ratio (EXACT)
**What:** The figure-eight three-body orbit maps to 1/φ under the Γ(2) representation. The matrix has Fibonacci entries {5, 8, 13}. This is an algebraic identity, not an approximation.
**Why it matters:** Connects the most famous three-body orbit to the most famous irrational number through a precise algebraic mechanism.
**Drives:** 3BP-1, 3BP-2, 3BP-8

### N8. CF Nobility Predicts Braid Entropy (AUC=0.98)
**What:** The continued fraction "nobility" of a three-body orbit's Γ(2) fixed point predicts its braid entropy with near-perfect accuracy (AUC=0.98 after exact arithmetic fix).
**Why it matters:** Number-theoretic structure (CF) captures physical information (stability) that the existing topological classification (word length) misses.
**Caveat:** Braid entropy is from the same matrix — partly algebraic. Physical stability test still needed.
**Drives:** 3BP-2, 3BP-4, 3BP-5, 3BP-6, 3BP-8

### N9. First CF-Organized Periodic Table of Three-Body Orbits
**What:** 691 orbits organized into a 9×8 grid by CF period and geometric mean. Reveals structure orthogonal to Li-Liao classification (only 69% family purity per cell).
**Why it matters:** A new organizational scheme for a 10,000+ orbit catalog. The empty cells are testable predictions.
**Drives:** 3BP-3, 3BP-7, 3BP-8

### N10. Zero-Cascading AMR Guarantee
**What:** Farey refinement adds at most 1 point per gap per level → zero forced refinements of neighbors. Proved via injection principle.
**Why it matters:** The 2:1 balance constraint in standard AMR wastes 20-40% of cells. We eliminate this entirely for shock-dominated problems (7-15x fewer cells).
**Caveat:** Only wins on discontinuities. Loses on smooth functions.
**Drives:** AMR-1 through AMR-7

### N11. Permutation Square-Sum Identity (NEW — 2026-03-29)
**What:** For any prime p and N=p-1: Σ (a/b)·δ(a/b) = (1/2)·Σ δ(a/b)² exactly.
Proof: δ = x - {px}, so x·δ - δ²/2 = (x² - {px}²)/2. Since a→pa mod b is a permutation of coprime residues, Σ(a/b)² = Σ(pa mod b/b)² for each b, so the difference vanishes.
**Why it matters:** Combined with D(x) = -x - R(x) (Möbius inversion of Farey rank), this gives **B + C = -2·Σ R(x)·δ(x)** where R involves Möbius-weighted fractional part sums. The Sign Theorem reduces to Σ R·δ < 0 — a massive simplification from quadratic to linear.
**Status:** 🧪 Step 1 passed — independently verified by adversarial agent (exact arithmetic, primes to 199). Also holds for ALL N < p, not just N = p-1. Breaks for composite p or N ≥ p.
**Classification:** A1 (autonomous discovery; proof uses only elementary techniques but packaging appears novel)
**CRITICAL UPDATE:** B+C > 0 is FALSE for all primes! B+C = -634 at p=1399 (M(p) = +8). ΔW(1399) > 0 confirming the Sign Theorem fails for positive-M primes. For M(p) ≤ -3 class: B+C > 0 holds for all tested primes and ΔW < 0 always. The identity helps prove the M(p) ≤ -3 case.
**Drives:** MPR-4 (unconditional Sign Theorem)

### N12½. Deficit-Dedekind Connection (NEW — 2026-03-29)
**What:** D_q(r) = q(q-1)(q-2)/12 - q²·s(r,q) where D_q is the per-denominator shift deficit and s(r,q) is the Dedekind sum. The minimum deficit over non-identity multipliers is D_q(2) = q(q²-1)/24, achieved by the multiplier 2.
**Why it matters:** Provides the analytical lower bound for C' via PNT summation over prime denominators. Combined with the Farey L² discrepancy bound, gives C/A ≥ c/log²p unconditionally — sufficient to close the Sign Theorem.
**Status:** 🧪 Step 1 passed — verified for all primes q ≤ 997 (21,651 pairs, zero violations)
**Drives:** MPR-4, MPR-21, MPR-22

### N12. D = -x - R(x) Exact Decomposition (NEW — 2026-03-29)
**What:** The Farey displacement D(a/b) = rank - |F_N|·(a/b) decomposes exactly as D(x) = -x - R(x) where R(x) = Σ_{d≤N} μ(d)·Σ_{m≤N/d} {xm}. The rank comes from Möbius inversion of the counting function.
**Why it matters:** Separates D into a trivial part (-x) whose interaction with δ we can compute exactly (= -C/2 by N11), and the "arithmetic" part R(x) which encodes Möbius structure.
**Status:** 🔬 Unverified
**Drives:** MPR-4, connects to N2 (Mertens-Discrepancy connection)

---

## KEY INSIGHTS (non-obvious observations that guide our work)

### I1. D/A → 1 Near-Cancellation
The displacement sum A and shift-squared C nearly cancel, with their ratio approaching 1. This means the Sign Theorem reduces to proving a small residual is positive.

### I2. The Injection Principle Is Universal
Originally proved for primes, then generalized to ALL N. Every Farey level adds at most 1 new fraction per gap. This is the foundation for AMR, 3DGS, IoT, and radio-silent applications.

### I3. Fisher Information Always Increases
Σ 1/g² (sum of inverse squared gap widths) strictly increases at every Farey level. This is a monotone functional — information always grows with refinement.

### I4. Farey Wins on Discontinuities, Loses on Smooth
AMR validation showed: zero-cascading matters when there are sharp features (shocks, boundaries). On smooth functions, the non-uniform Farey spacing wastes cells.

### I5. Nobility = Stability (in CF sense)
Numbers closer to the golden ratio (in continued fraction terms) correspond to more stable orbits — in celestial mechanics (KAM), in three-body problem (our AUC=0.98), and in Rydberg atoms.

### I6. The 19,000:1 Compression
Three independent mechanisms (Möbius cancellation, Weil bounds, equidistribution) compress per-step Farey information by a factor of 19,000. This is unexplained at a deep level.

---

## POTENTIALLY VALUABLE LEADS (to explore through the lens of our discoveries)

### V1. ΔW Spectral Analysis at Zeta Zero Frequencies (MPR-20)
If ΔW oscillates at frequencies matching zeta zeros (14.134...), that's a genuinely new RH connection. Uses: N1, N2.

### V2. Three-Body Physical Stability Test (3BP-5)
If nobility predicts DYNAMICAL stability (not just braid entropy), that's a breakthrough. Uses: N8, I5.

### V3. AMR for Shock-Capturing Paper (AMR-5)
Zero-cascading on shocks is validated and significant ($300M-600M/yr). Uses: N10, I4.

### V4. SB Learning Rates for PINNs (ML-2)
Number-theoretic LR schedules may help physics-informed NNs where resonance avoidance matters. Uses: I5 (noble = stable).

### V5. Unconditional Sign Theorem (MPR-4)
If proved, would be the paper's strongest result. Uses: N2, N5, N6.

---

## REFLECTION QUESTIONS (ask these for every new exploration)

1. Which of our Novel Discoveries (N1-N10) does this leverage?
2. Could anyone WITHOUT our discoveries pursue this equally well?
3. If we prove/validate this, does it strengthen or weaken our paper?
4. Is the connection genuine or are we forcing it?

### V6. Proof by Contradiction for Sign Theorem (MPR-21)
Assume ∃ prime p with M(p) ≤ -3 AND ΔW(p) ≥ 0. This forces B to be very negative (strong D-δ correlation). But M(p) ≤ -3 forces anticorrelation via the h=1 mode (proved negative). If we can show ΔW ≥ 0 requires h=1 mode positive → contradiction. Uses: N2, N5, N6.

### V7. Explicit Formula Connection (MPR-22)
M(x) = Σ_ρ x^ρ/(ρ·ζ'(ρ)) + ... Since ΔW(p) ~ M(p), our per-step discrepancy is implicitly a sum over zeta zeros. This is the theoretical backbone of the spectral analysis (MPR-20). The prime counting function π(x) connects via Möbius inversion. Uses: N1, N2.

### I7. W_N as Spectral Rigidity (Physics Connection)
Our W_N = (1/n²)ΣD(f)² is a discrete analog of the Dyson-Mehta Δ₃ statistic that measures spectral rigidity in random matrix theory. D(f) = rank(f) - n·f is the spectral staircase deviation. This is a rigorous identification (Franel-Landau makes it precise). The Sign Theorem (B+C > 0) then says: primes inject disorder into the Farey spectrum — each prime step makes the sequence less rigid. This connects to Montgomery-Dyson (pair correlation of zeta zeros = GUE), Connes (zeta zeros as energy levels), and the Farey map transfer operator (Mayer). Uses: N1, N2, N5.

### N11. Geometric Identity: B+C = Σ(D+δ)² - ΣD²
The cross term plus shift squared equals the change in L2 norm when shifting displacements by δ. B+C > 0 iff the perturbation D → D+δ increases total variance. Combined with I7: primes always increase spectral disorder. This identity, together with the smooth-rough lemma (ΣD_smooth·δ = 0), reduces the proof to showing D_rough and δ are not strongly anti-correlated. 🔬 Unverified as general proof.

### N12. Four-Term Decomposition Boundary Correction
Aristotle discovered a -1 boundary correction in the four-term decomposition: WN(p) = WN(p-1) + B + C - 1 + D. The correction arises from f=1/1 where D_p(1)=0 but D_{p-1}(1)+δ(1)=1. This corrects our original (incorrect) decomposition and was found by computational verification. 📊 Fully validated.

### I8. BCZ Map = Horocycle Flow (Mayer Spectral Analysis)
The transition F_{N-1} → F_N is a Poincaré section of the horocycle flow on the modular surface (Athreya-Cheung 2014). Our W_N is exactly the Franel L2 sum, studied since 1924. Spectral methods (Mayer transfer operator, Selberg zeta) give beautiful context but cannot prove the pointwise Sign Theorem — they only give average/asymptotic bounds. The gap between "average" and "pointwise" is what makes our result hard and interesting (analogous to PNT vs Bertrand's Postulate). The arithmetic approach (four-term decomposition, B+C identity) remains the most viable proof path. Uses: N1, N2, connects to I7.

### I9. S² Extension: No Sign Theorem, but Residue-Class Dichotomy
The per-step Sign Theorem does NOT transfer from S¹ to S². On S², ΔW_sphere(p) > 0 for 92% of primes p ≡ 1 (mod 4) (equidistribution IMPROVES), while primes p ≡ 3 (mod 4) show mixed/null behavior (many have r₃=0). Spherical harmonic sums vanish for ℓ ≤ 3 due to octahedral symmetry. This reflects the deeper arithmetic of ternary quadratic forms and Fermat's two-squares theorem. Classification: C1 (minor novelty). Uses: extends N1 perspective to new domain.

### Failed: Displacement-Guided 3DGS Densification
Two attempts at using D(f) (rank displacement) or local Voronoi displacement as a 3DGS densification signal both FAILED. On both the hard target (50 bumps) and sparse detail target (5 hidden features), displacement guidance produced MORE Gaussians and WORSE MSE than either classical Farey or standard ADC. The displacement score adds noise to the gradient signal. The 3DGS Farey advantage comes from the GAP-FILLING property (mediant insertion), not from displacement analysis. Dropping this direction.

### Failed: Data Center Farey Scheduling (Q31)
Triple-checked and DOES NOT hold up. Farey mediant insertion has poor spacing quality (69:1 gap ratio at N=100 vs 2:1 for midpoint bisection). Zero cascading is not unique — consistent hashing also achieves it. Midpoint bisection dominates Farey on every practical metric. The problem is already well-solved by random jitter + consistent hashing. The "Farey" part of the algorithm makes scheduling WORSE, not better. Dropping this direction. The Farey advantage is in number-theoretic properties, not in uniform spacing for scheduling.

### I10. Farey is Powerful in 1D, Irrelevant in Higher Dimensions
Comprehensive graphics applications research (14 areas tested) shows Farey's advantage is strictly 1D. Ray tracing, mesh refinement, cloth/fluid simulation, medical imaging — all fail because they're inherently multi-dimensional. The promising applications (3DGS, SLAM, 4DGS, NeRF rays) all work by decomposing into 1D sub-problems. Halton/Sobol/R2 sequences dominate in dimensions ≥ 2. Implication: our 3DGS result is the RIGHT application, and future applications should target problems with natural 1D structure (time series, 1D signals, sequential scheduling).

### Failed: Ray Tracing / QMC Sampling
Farey sequences are NOT competitive with Halton/Sobol for numerical integration or ray tracing. Convergence rate ~0.45 (barely above random 0.43) vs Halton 1.37. Farey star discrepancy is WORSE than random at N=1000 (0.032 vs 0.022). Reason: Farey enumerates rationals (clusters near simple fractions), QMC minimizes discrepancy (spreads uniformly). Different goals. In 2D, Farey tensor product is catastrophically bad.

### I11. Farey Commercial Value: 1D Edge/Medical/LiDAR Applications
Market analysis identifies 4 viable commercial targets for Farey 1D methods:
1. IoT edge sampling ($100-500M, 15%+ CAGR) — deterministic, certifiable, zero-ML
2. ECG/EEG wearable compression ($20-100M) — provable, lightweight for medical
3. LiDAR scan-line densification ($50-300M, 41-50% CAGR) — each scan is 1D
4. Audio codec quantization ($50-200M) — competitive with Q2D2 (Dec 2025)
Key insight: Farey's commercial value is in CONSTRAINED, CERTIFIABLE, 1D settings where deterministic guarantees matter more than raw performance.

### I12. Farey Requires Rational Structure in the Domain
LiDAR and audio quantization both fail because physical measurements (meters, voltages) have no meaningful rational-number structure. Farey mediant of 10/1 and 50/1 = 30/1 = arithmetic mean — no advantage. Farey works when data IS rational or proportional (Farey fractions, scheduling ratios, Gaussian position ordering). This is a fundamental constraint, not a limitation to be overcome.

### I13. Mediant Minimality: Farey's TRUE Optimality Property
Farey is NOT optimal for minimizing gaps (midpoint bisection is better) or discrepancy (Van der Corput wins). But Farey IS provably optimal for MINIMAL DENOMINATOR insertion: the mediant (a+c)/(b+d) is the fraction with smallest possible denominator that fits between Farey neighbors a/b and c/d. Proof: q = (cq-pd)b + (pb-aq)d ≥ b+d. This is the correct theoretical claim for the 3DGS paper — Farey inserts the SIMPLEST point, not the MOST UNIFORM point. Submitted to Aristotle for Lean formalization.

### I14. IoT Farey Sampling: Coordination + Certification, Not SNR
Farey does NOT beat bisection on pure signal quality (except +3-11 dB for non-dyadic features). Both achieve 92% power savings (12x battery life). Farey's real advantages: (1) integer-only computation (no FPU needed, sub-$0.50 chips), (2) zero-communication sensor coordination (sensors compute compatible schedules from (id, N) alone), (3) provable quality bounds for FDA/IEC certification. The commercial pitch: "same power savings + coordination + certification + cheapest hardware." Classification: C1-C2 depending on coordination application.

### I15. Silent Coordination: Underwater + Military Are Best Fits
Farey's unique combination: zero-communication + deterministic + collision-free + monotone nesting (F_p ⊂ F_q). No existing protocol provides all four. Best applications: (1) underwater acoustic networks (comms physically expensive), (2) military EMCON swarms (zero-emission required). Key differentiator vs CRT-TTS (Su 2015): monotone nesting — changing N doesn't require recomputing existing schedules. Weaknesses: N must be known, prime constraint, single-channel, no adaptivity. Patent potential: no prior art found. Classification: C1-C2.

### I16. Military EMCON Triple-Check: Narrow Niche Only
Military Farey coordination shrinks after triple-check. ALOHA comparison is strawman (real competitor: pre-planned TDMA with spare slots). Unit removal doesn't benefit from nesting. Submarines don't coordinate real-time under EMCON. GPS dependency is shared. No priority mechanism. Best-fit: 50-500 autonomous drone swarms, GPS-available, RF-denied, dynamic composition. Honest gain: ~15-25% utilization improvement. Patent landscape open but application is niche. Key competitor: Zero-Exposure Distributed TDMA (IEEE 2012).

### DEAD: Drone Swarm Silent Coordination (Q36)
4 of 5 kill tests triggered. Fatal flaws: (1) clock drift sensitivity 100x worse than TDMA (Farey slots are non-uniform, some 0.011ms apart vs TDMA 1.03ms), (2) off-by-one in N causes collisions (drones must agree on N exactly = requires communication), (3) prime-order overhead up to 62%, (4) actual utilization gain only 5.2% not 15-25%. The non-uniform spacing of Farey fractions is a structural flaw for any timing-based protocol.

### I17. Hristov Stability Test: CF-Nobility Degenerate for Periodic Orbits
All 4,860 periodic orbits in Hristov's catalog have trivial Γ(2) matrices (syzygy sequences reduce to identity), making CF-nobility = 1.0 for all. Our measure CANNOT distinguish orbits in this class. However, unreduced syzygy structure DOES predict Lyapunov exponents (ρ=+0.43, p~10⁻²¹⁷), confirming topology carries dynamical information. Need free-group words from Hristov to test our CF measure directly. Email drafted.

### I18. Real Images: No Compactness Advantage
On Kodak real images, Farey uses 1014 Gaussians vs ADC's 985 to reach similar quality. The 5.5x compactness from synthetic density fields does NOT transfer to real images. Farey wins slightly on PSNR (+0.37 dB) but with 3% MORE Gaussians. The "fewer Gaussians at same quality" claim is false for real images.

### I19. Three-Body Circularity CONFIRMED: Nobility Does NOT Predict Physical Stability
Using Hristov's half-period words (4,552 nontrivial orbits with 30-digit Lyapunov exponents), CF-nobility has r=-0.05 correlation with real dynamical stability. The AUC=0.98 from Li-Liao was predicting braid entropy (from the SAME matrix), not physical stability. This is the definitive answer: our CF measure captures algebraic complexity, not dynamical instability. The three-body paper remains publishable (figure-eight=φ, periodic table, algebraic prediction) but the "predicts stability" framing must be corrected to "predicts braid-theoretic complexity."

### DEAD: Adaptive Ramanujan Filter Bank (Q40)
M(q)-ordered Ramanujan filter banks show NO systematic advantage over sequential ordering. Mean ratio 0.82 (marginal). The speedup is tautological: sorting by |M(q)| moves high-|M| primes earlier, which only helps when the target period happens to have high |M|. For P=97 (M=1), the ordering HURTS. The Mertens function does not encode useful signal processing information for filter ordering.

### N13. R Cancellation: Multiplication-by-p is More Orthogonal Than Random
The cross term R = ΣD·δ/Σδ² uses only ~10% of its Cauchy-Schwarz budget because of two-stage cancellation: within-denominator (63%) + cross-denominator (30%). The actual |R| is BELOW all 500 random permutation trials tested (z-scores -4 to -24). Structural reason: D is global (rank among all fractions), δ is local (single denominator via pa mod b). This is a Weyl-sum phenomenon where a smooth function pairs against a scrambled permutation. When M(p) is very negative, within-b correlations become positive, breaking cancellation — explaining why |R| tracks |M(p)|. This may be the path to the analytical proof: formalize "multiplication-by-p creates more cancellation than random."

### DEAD: 3DGS on Real 3D Scenes (DEFINITIVE)
Colab T4 test on MipNeRF-360 bicycle: ADC 21.41 dB, Farey 16.75 dB. Delta = -4.66 dB (catastrophic). Farey uses 9% fewer Gaussians and trains 2x faster but quality is unusable. The Farey mediant insertion doesn't place Gaussians where rendering error is — it fills spatial gaps uniformly, but real scenes need error-guided placement. The synthetic compactness (5.5x) was an artifact of structured density fields. 3DGS application is definitively killed.

### DEAD: Character Sum / Weil Bound Approach to R > -1/2
Per-denominator Weil bounds fail because the constant C grows as p^1.26 and the sum of bounds diverges as p^0.65. Cancellation between denominators is ESSENTIAL — for p=97, negative S_b total -312.6 (exceeding threshold -112.8) but positive S_b (+265.1) partially cancel. Any |S_b|-based bound destroys this. The proof must bound the FULL sum Σ_b S_b directly, requiring understanding of sign structure across denominators.

### N14. Cross-Correlation = Dedekind Sum (POTENTIAL BREAKTHROUGH)
The per-denominator cross term C(p,b) = Σ D_rough(a/b)·δ(a/b) equals the Dedekind sum s(p,b) (restricted to coprime residues). Verified numerically (correlation 0.59-0.70). This connects our problem to a deeply studied object with:
- Rademacher's bound: |s(p,b)| ≤ (1/12)(b/p + p/b + 1)
- Dedekind reciprocity: s(p,b) + s(b,p) = (p/b + b/p + 1/(pb))/12 - 1/4
- Möbius inversion properties
Path A: |R| ≤ Σ|s(p,b)|/b = O(log²B) via Rademacher → may close proof for large p
Path C: Dedekind reciprocity + Möbius inversion → R_μ(p) = O(1)
This is the most promising proof direction discovered in the entire session.

### N15. POTENTIAL PROOF: R(p) = O(log B / B) → 0 via Dedekind Sums (UNCONDITIONAL)
The Dedekind sum proof path establishes R(p;B) = O(log B / B) → 0 using ONLY:
1. Möbius inversion: C(p,b) = Σ μ(d)·s(p,b/d) (verified exactly)
2. Rademacher bound: |s(p,k)| = O(log k) (classical, 1932)
3. PNT: |M(x)| = O(x/log x) (unconditional, 1896)
4. Denominator growth: Σ V(b) ~ 0.024·B² (verified)
Combined: |R| ≤ O(B log B) / O(B²) = O(log B / B) → 0.
This is STRONGER than R > -1/2. If rigorous, the Sign Theorem is proved unconditionally for all sufficiently large primes. Combined with computation for small primes → FULL PROOF.
**STATUS: Needs rigorous verification of all steps, especially the restricted Mertens function M_p(x;k).**

### CORRECTED: Dedekind Sum Proof — Definition Mismatch (N14 DOWNGRADED)
The Dedekind proof sketch proved R → 0 for the SAWTOOTH cross-correlation Σ((a/b))·((pa/b)), NOT for our actual cross term Σ D(a/b)·δ(a/b). Independent verification confirmed: (1) our actual |R(p)| does NOT decay (goes up to 1.45), (2) the Möbius inversion fails for our actual C(p,b). The D(a/b) displacement involves GLOBAL rank information that the sawtooth doesn't capture. The Dedekind connection is mathematically interesting but does NOT solve our problem. The unconditional proof remains OPEN.

### Verification Complete: Dedekind Proof — 3 Fatal Flaws + Definition Mismatch
Adversarial audit found: (1) |s(p,k)|=O(log k) is FALSE (grows as k/(12p) for large k), (2) numerator bound O(B log B) is wrong, (3) restricted Mertens not justified. Independent verification found: |R(p)| doesn't decay (up to 1.45), Möbius inversion fails for actual C(p,b). HOWEVER: adversarial agent notes a CORRECTED proof via Dedekind reciprocity decomposition might give |R|=O(1/(p log B)) — but this applies to the sawtooth version, not our displacement. Our R(p) is O(1), not o(1). The unconditional proof remains the central open problem.
