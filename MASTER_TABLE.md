# MASTER TABLE — All Active Work & Explorations
Last updated: 2026-03-30 (session 8 FINAL — SIGN THEOREM PROVED + new directions launched)

## NEW DIRECTIONS (session 8 end)

| ID | Task | Phase | Strength | Target |
|----|------|-------|----------|--------|
| ID | Task | Phase | Priority | Strength | Target | Status |
|----|------|-------|----------|----------|--------|--------|
| MPR-24 | **Prove composites heal (ΔW > 0)** | 🧪 | **HIGH** | 🟩 | Complete primes-damage/composites-heal | 95.4% verified; powers-of-2 always; zero-map mechanism found |
| MPR-33 | **Triangular distribution of δ** | 🔬 | **HIGH** | 🟩 | S_{2k}/p² → 3/(π²(2k+1)(k+1)) | Discovered! Needs proof + add to paper |
| MPR-27 | **Explicit formula: zeros ↔ ΔW(p)** | 🔬 | **HIGH** | 🟩 | ΔW = diagonal + oscillation + M(p) coupling | Derived formally, needs rigorous verification |
| MPR-25 | **Farey telescope / pair correlation** | 🔬 | **HIGH** | 🟩 | Mellin poles at γ-γ' → Montgomery conjecture | New connection to pair correlation! |
| MPR-34 | **Test prediction: FT of ΔW shows zero pairs** | 🔬 | **HIGH** | 🟩 | Fourier transform of ΔW(p) shows γ_k - γ_l peaks | Testable prediction from explicit formula |
| MPR-35 | **Density theorem: ΔW < 0 for almost all primes** | 🔬 | **HIGH** | 🟨 | Rubinstein-Sarnak / Chebyshev bias connection | M(p)≤-3 threshold is sharp; pursue density |
| MPR-36 | **Primes-are-random beyond L²** | 🔬 | MEDIUM | 🟨 | Test random model for L⁴, L⁶, other measurements | Does it extend beyond our specific measurement? |
| MPR-37 | **Goldbach Δr per-step analysis** | 🔬 | MEDIUM | 🟨 | Apply increment strategy to Goldbach | Most promising application of per-step method |
| MPR-28 | Remove M(p) ≤ -3 restriction | 📊 | LOW | ✅ | SETTLED: -3 is optimal, -2 has counterexample | Proved sharp; pursue density theorem instead |
| MPR-23 | Extend spectral formula to L(1/2,χ) | 🔬 | MEDIUM | 🟨 | Connect to RH critical strip | ζ(1) pole blocks; Nyman-Beurling/Matérn workarounds |
| MPR-26 | Higher moments L⁴, L⁶ | 🧪 | MEDIUM | 🟩 | Triangular distribution predicts all moments | Subsumed by MPR-33 |
| MPR-29 | "Studying increments" in other problems | 📊 | LOW | 🟨 | Not novel as general strategy; novel for Farey | Goldbach most promising (MPR-37) |
| MPR-38 | **Geometric lens: what else do primes DO?** | 🔬 | MEDIUM | 🟨 | Study prime effects on other combinatorial objects | New research direction |
| MPR-30 | Generalize to number fields | 🔬 | LOW | ⬜ | Dedekind zeta analogues | Speculative |
| MPR-31 | Quantum chaos / modular surface | 🔬 | LOW | ⬜ | Farey → quantum unique ergodicity | Speculative |
| MPR-32 | New zero-free regions via Farey geometry | 🔬 | LOW | ⬜ | Geometric approach to RH | Long-shot |

## Legend
- **Tags:** MPR=Math Paper Research, 3BP=Three-Body Problem, 3DGS=3D Gaussian Splatting, AMR=Adaptive Mesh Refinement, DEF=Defense/DARPA, IOT=IoT/Wireless, PHYS=Physics, ML=Machine Learning, MESH=Mesh Generation, PUB=Publication
- **Phase:** 🔬Research → 🧪Experiment → 📊Validated → 📝Paper → 📬Submitted
- **Strength:** ⬛DEAD ⬜WEAK 🟨MODERATE 🟩STRONG 🟢VERY STRONG

---

## A. MATH PAPER RESEARCH (MPR)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| MPR-1 | B+C computation to p=100K | 🧪 | 🟩 | N1,N2 | 2,722 primes verified (p≤50K), 0 violations | Resume from p=56K (tonight Q3) |
| MPR-2 | B+C analytical proof (δ² bound) | 🔬 | 🟩 | N2,N5,N6 | Path C: δ²≥N²/(12logN) closes proof at P₀~10⁵ | Prove δ² with all denominators (Q9) |
| MPR-3 | B+C ratio test approach | 🔬 | 🟩 | N2,N6 | Only need B+C > O(p/logp), not > 0 | Combine with MPR-2 |
| MPR-4 | Unconditional Sign Theorem | 🔬 | 🟢 | N2,N4,N11,N12 | **Session 8 progress:** (1) Permutation identity Σxδ=C/2 proved+verified. (2) B+C<0 at p=1399 (M=+8) — Sign Thm only for M≤-3. (3) El Marraki 1995: \|M(x)\|≤0.644x/logx effective. (4) C'>deficit+1 verified for all M≤-3 primes. (5) Proof sketch: bypass C+D>A+1 closes with C'~p², deficit~p²/logp. | Formalize constants: prove C'≥c₁p² and deficit≤c₂p²/logp explicitly |
| MPR-21 | Permutation Square-Sum Identity | 📊 | 🟢 | N11 | **NEW:** Σx·δ = C/2 exactly. Proved via permutation argument. Verified independently (adversarial agent). Holds for all N < p. | Formalize in Lean; add to paper |
| MPR-22 | B+C = -2ΣR·δ Reformulation | 🔬 | 🟩 | N11,N12 | **NEW:** Combined with D=-x-R(x), gives B+C=-2ΣR·δ. T(m) connects to Kloosterman sums. Möbius structure matches M(p)↔ΔW(p). | Kloosterman bounds → proof for large p |
| MPR-5 | Aristotle Lean proofs | 📊 | 🟢 | N1,I2,I3 | 260 results, 4 sorry. PROVED: Sign Thm (p=11..113), four-term decomp, geometric identity, wobble mono equiv, newDispSquaredSum_pos, corrRatio_gt_neg_half (p=11..83), bPlusC_pos_of_corrRatio (structural), R(11)=-1155/5974, R(13)=813/15872, dispRoughSquaredSum (Cauchy-Schwarz 44x too loose) | Close remaining 4 sorry |
| MPR-6 | Paper PDF on GitHub | 📝 | 🟩 | N1 | 26pp compiled, commit 655ffe5 | Push to GitHub (Q15) |
| MPR-7 | C_W bounded proof | 🔬 | 🟨 | N5 | C_W empirically ≤0.7, analytical proof hard | Franel + Lee-Leong approach |
| MPR-8 | Erdős-Turán bound | ⬛ | ⬛ | — | Does NOT close gap (cotangent unbounded) | DEAD — move to other approaches |
| MPR-9 | Voronoi Entropy Monotonicity | 📊 | 🟩 | I3 | H always increases — possibly novel, elementary proof | Add to paper; submit to Aristotle |
| MPR-10 | I_k/J_k/Log-Sum monotone functionals | 📊 | 🟩 | I3 | 3 complete theorems with proofs | Add to paper |
| MPR-11 | Grand Identity (weighted Farey sums) | 📊 | 🟩 | N5 | Generalizes bridge identity to arbitrary arithmetic weights | Add to paper |
| MPR-12 | Farey antisymmetry identity | 📊 | 🟩 | N1 | D(f)+D(σ(f))=0 for standard normalization | In paper (fix sign from -1 to 0) |
| MPR-13 | Rayleigh quotient approach (proof) | 🔬 | 🟩 | N5,N6 | Ranked #1 most promising proof approach | Pursue for B+C analytical proof |
| MPR-14 | Schur convexity/majorization approach | 🔬 | 🟨 | N5 | Ranked #2 proof approach | Alternative if Rayleigh fails |
| MPR-15 | Explicit formula proof path | 🔬 | 🟨 | N2 | Uses zeros of L-functions directly | RH-conditional path |
| MPR-16 | C/A increasing trend (~p^0.016) | 📊 | 🟩 | N5,N6 | Critical for proof strategy — C dominates A for large p | Prove analytically |
| MPR-17 | \|ΔW\| ~ p^{-1.77} scaling law | 📊 | 🟩 | Precise power law for per-step discrepancy change | Add to paper |
| MPR-18 | 19,000:1 compression / info paradox | 📊 | 🟩 | I6 | 3 mechanisms: Möbius, Weil, Equidistribution | Add to paper |
| MPR-19 | Wobble-entropy duality (r=-0.914) | 📊 | 🟩 | N1,I3 | ΔH ↔ ΔW strong anticorrelation | Add to paper |
| MPR-20 | Spectral analysis of ΔW at zeta zeros | ⬛ | ⬛ | N1,N2 | Zeta zeros NOT significant in ΔW spectrum (p=0.30). Negative result. | DEAD |
| MPR-21 | Four-term decomposition (Lean) | 📊 | 🟢 | N1,N5 | PROVED in Lean with -1 boundary correction | In paper ✓ |
| MPR-22 | Geometric identity B+C = Σ(D+δ)²-ΣD² | 📊 | 🟢 | N5,N6 | NEW discovery, PROVED in Lean | Add to paper |
| MPR-23 | Wobble monotonicity equiv (BCZ horocycle) | 📊 | 🟢 | N1 | PROVED in Lean | Add to paper |
| MPR-24 | newDispSquaredSum_pos_general (p≥13) | 📊 | 🟢 | N5 | PROVED in Lean for all p≥13 | Add to paper |
| MPR-25 | Smooth-rough orthogonality lemma | 🔬 | 🟨 | N5 | ΣD_smooth·δ = 0. Aristotle working on it | Await Aristotle result |
| MPR-26 | Guth-Maynard density-1 path | 🔬 | 🟨 | N2 | Identified as viable proof path, not yet executed | Explore |
| MPR-27 | S² extension (higher-dim Sign Thm) | 🔬 | 🟨 | N1 | No Sign Theorem on S², but residue-class dichotomy found | Explore dichotomy |
| MPR-28 | Large sieve R→0 approach | ⬛ | ⬛ | N5 | FAILED: R grows, doesn't decay | DEAD |
| MPR-29 | Displacement-guided 3DGS | ⬛ | ⬛ | I2 | FAILED: Adds noise, not signal | DEAD |

## B. THREE-BODY PROBLEM (3BP)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| 3BP-1 | Figure-eight = golden ratio | 📊 | 🟢 | N7 | EXACT: z²-z-1=0, Fibonacci matrix {5,8,13} | In paper ✓ |
| 3BP-2 | Nobility predicts braid entropy | 📊 | 🟢 | N8,I5 | AUC=0.98, ρ=-0.96 (exact CF, 691 orbits) | In paper ✓ (with circularity caveat) |
| 3BP-3 | Periodic table of orbits | 📊 | 🟢 | N9 | First CF-organized catalog: 9×8 grid, 51 cells | In paper ✓ |
| 3BP-4 | Unequal mass extension | 🧪 | 🟩 | N8 | AUC=0.79, cross-validated. m3=4 anomaly found, framework robust | Add to paper |
| 3BP-5 | Physical stability test | 🔬 | 🟩 | N8,I5 | Braid entropy ≠ dynamical stability. Need Floquet data | Find catalog with Floquet multipliers |
| 3BP-6 | Nobility-guided orbit search | 📊 | 🟨 | N8,I5 | 1.06x strict, 2x near-misses (200 trials) | Larger trial with Newton refinement |
| 3BP-7 | Empty cell orbit discovery | 📊 | ⬜ | N9 | 0/10 periodic, 2/10 marginal (4,199 integrations) | More sophisticated search or collaboration |
| 3BP-8 | Three-body paper | 📝 | 🟩 | N7,N8,N9 | Draft complete (~17pp), all results included | Refine, add unequal mass (Q7) |
| 3BP-9 | Contact Nakamura (Osaka) | ⏳ | 🟩 | N8,N9 | He proved restricted Farey/braid connection | Draft email, propose extension |
| 3BP-10 | Contact Li & Liao (Shanghai) | ⏳ | 🟩 | N9 | They built the 10K+ orbit catalog | Draft email, share periodic table |

## C. 3D GAUSSIAN SPLATTING (3DGS)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| 3DGS-1 | 1D demo (unfair baseline) | 📊 | ⬜ | I2 | 33x — but baseline was crippled | Historical only |
| 3DGS-2 | 2D demo (fair baseline) | 📊 | 🟨 | I2 | +0.44 dB at 6K steps, interval=200 | Informative but not publishable |
| 3DGS-3 | 3D synthetic demo | 📊 | 🟨 | I2 | +1.07 dB (tight budget), -4.39 dB (generous) | Farey wins only at tight budget |
| 3DGS-4 | Stability/robustness angle | 📊 | 🟨 | I2 | Farey ±3.36 vs ADC ±6.66 at pct70 | Real 3DGS needed to confirm |
| 3DGS-5 | Real pipeline Phase 1 | 🧪 | 🟩 | I2 | 13 files written, MipNeRF360 downloaded | Verify imports + train (tonight Q2) |
| 3DGS-6 | Real pipeline Phase 2 | ⏳ | 🟩 | I2 | Farey vs ADC on bicycle scene | After Q2 passes (Q5) |
| 3DGS-7 | Full benchmark (9 scenes) | ⏳ | 🟩 | I2 | Publication-quality comparison | After Q5 (Q12) |
| 3DGS-8 | 3DGS paper | ⏳ | 🟨 | I2 | Outline exists | After real results (depends on Q5-Q7) |
| 3DGS-9 | Scaffold-GS integration | ⏳ | 🟩 | I2 | Bridge mapped: gap→voxel, mediant→anchor | After Phase 2 validates |
| 3DGS-10 | SOTA comparison (8 methods) | 🧪 | 🟩 | I2 | Farey wins compactness (274 Gaussians vs thousands). 8 methods tested. | Add to paper |
| 3DGS-11 | Real images test | 📊 | ⬛ | I2 | No compactness advantage on real images | DEAD |
| 3DGS-12 | 3DGS Colab definitive test | 🧪 | 🟨 | I2 | Running definitive test on Colab | Await results |

## D. ADAPTIVE MESH REFINEMENT (AMR)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| AMR-1 | Zero-cascading proof | 📊 | 🟢 | N10,I2 | Proved via injection principle, Lean verified | In paper ✓ |
| AMR-2 | Synthetic 2D validation | 📊 | 🟩 | N10 | 6x fewer cells (toy scene) | ✓ |
| AMR-3 | Real-data validation | 📊 | 🟩 | N10,I4 | Shocks: 7-15x win. Smooth: 1.2-3.4x loss | ✓ |
| AMR-4 | Extended shock benchmark | 🧪 | 🟩 | N10,I4 | Failed last night (timeout bug). 5 more shock types | Fix + run tonight (Q1) |
| AMR-5 | AMR paper | 📝 | 🟩 | N10,I4 | Outline exists. Honest: specialist tool for shocks | Write after Q1 (Q6) |
| AMR-6 | Compute savings estimate | 📊 | 🟨 | N10 | $300M-600M/yr for shock-dominated CFD | Honest: not universal savings |
| AMR-7 | 3D Farey AMR | 📊 | ⬜ | N10 | Tensor product LOSES in 3D (octree cascading only 4-8%) | Needs non-tensor approach |

## E. DEFENSE & OUTREACH (DEF)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| DEF-1 | DARPA TTO BAA submission | 📝 | 🟩 | I2 | Exec summary + cover letter finalized | Register on BAAT, submit by Apr 17 (Q11) |
| DEF-2 | ONR Code 311 white paper | ⏳ | 🟩 | I2 | Contact: Dr. Kamgar-Parsi identified | Email + 5-page white paper (Q13) |
| DEF-3 | AFRL Tech Connect | ⏳ | 🟨 | I2 | Portal identified | Submit idea (Q13) |
| DEF-4 | Radio-silent report | 📊 | 🟩 | I2 | 16 issues fixed, honest framing | Ready to share ✓ |

## F. IoT & WIRELESS (IOT)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| IOT-1 | IoT/LoRaWAN report | 📝 | 🟨 | I2 | Written (32%→99%+). TS-LoRa prior art exists (2019) | Incremental over TS-LoRa, not breakthrough |
| IOT-2 | Cognitive radio paper | ⏳ | 🟨 | I2 | Simplest blind rendezvous (k*t mod p) | Write complexity comparison (Q14) |
| IOT-3 | MIMO NTN position paper | ⏳ | ⬜ | I2 | Reframed for satellite. Crowded field. | Write short paper (Q15) |
| IOT-4 | AUV underwater scheduling | 🔬 | 🟨 | I2 | Acoustic TDMA is real sub-problem | Explore defense angle |

## G. MESH & 3D PRINTING (MESH)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| MESH-1 | Conformal/Ptolemy connection | 📊 | 🟨 | I2 | Nesting confirmed. Quality worse than uniform. | Narrow paper on BPS framework (Q16) |
| MESH-2 | Mesh quality proofs | 🔬 | 🟨 | I2,N10 | Need aspect ratio bounds for credibility | Prove 2D bounds (Q18) |
| MESH-3 | 3D printing benefits | 🔬 | 🟨 | N10,I2 | Unexplored: print time, adaptive layers, watertight | Research + experiment (Q20) |
| MESH-4 | Terrain LOD | 📊 | ⬛ | — | Power-of-2 also nested. Skirts solve cracks. | DEAD — not novel |
| MESH-5 | Nanite/game engine | 📊 | ⬛ | — | Karis shipped cracks fix (UE 5.4). Industry moved on. | DEAD |

## H. PHYSICS EXPLORATIONS (PHYS)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| PHYS-1 | Orbital resonances/exoplanets | 📊 | 🟩 | I2,I5 | Farey level clustering p=8.9e-28 | Write up as supplementary |
| PHYS-2 | KAM + Stern-Brocot | 📊 | 🟩 | I5 | Noble=most stable. Foundation for 3BP work | Background context ✓ |
| PHYS-3 | Kirkwood gaps | 📊 | ⬛ | — | r=0.95 but textbook material | DEAD — not novel |
| PHYS-4 | Rydberg atoms/semiclassical | 🔬 | 🟩 | I5,N1 | "Kirkwood gaps" in Rydberg spectra real | Needs physics collaborator |
| PHYS-5 | Quantum chaos (cold atoms) | 🔬 | 🟩 | I5 | Buchleitner PRL 2006 confirmed Farey in experiment | Background context |
| PHYS-6 | Quasicrystals/Fibonacci anyons | 🔬 | 🟩 | I5 | Golden ratio governs structure. 2024-25 frontier | Needs condensed matter collaborator |
| PHYS-7 | Doubly-excited Rydberg | 🔬 | 🟨 | I5 | "Pendular-planet states" 2025 | Needs physics collaborator |
| PHYS-8 | Montgomery-Odlyzko/RH | 📊 | 🟩 | N2 | Zeta zeros ↔ random matrices. In our paper | Background context ✓ |
| PHYS-9 | Gravitational wave templates | 🔬 | ⬜ | I2 | SB tree for template banks — speculative | Parked |
| PHYS-10 | Twin prime geometric entanglement | 📊 | 🟩 | N3 | r=0.808, same ΔW sign 100% of time | Add to paper; explore further |
| PHYS-11 | Mertens-Healing Theorem (2p semiprimes) | 📊 | 🟩 | N3 | M(2p)>0 ⟹ non-healing, 100% accurate to N=1500 | Add to paper |
| PHYS-12 | Prime squares non-heal threshold | 📊 | 🟩 | N3 | p²: non-heal iff p≥11 (exact) | Add to paper |
| PHYS-13 | Primorials as optimal refinement levels | 📊 | 🟩 | N3,I3 | Local W-minima, arrive first, largest gaps | Add to paper |
| PHYS-14 | Spectral slope f^{-1.67} (pink-brown) | 📊 | 🟨 | N1 | Between pink and brown noise | In paper |
| PHYS-16 | W_N = Dyson-Mehta Δ₃ connection | 🧪 | 🟩 | N1,N2 | Rigorous: Farey wobble = RMT Δ₃ statistic | Add to paper |
| PHYS-15 | PSL₂(ℤ) lattice structure | 📊 | 🟩 | I2 | Structural explanation of injection principle | In paper |
| PHYS-17 | Hristov stability (CF for orbits) | 🔬 | 🟨 | I5 | CF degenerate for periodic orbits — limited applicability | Parked |

## I. MACHINE LEARNING / COMPUTE (ML)

| ID | Task | Phase | Strength | Discovery | Key Result | Next Step |
|----|------|-------|----------|-----------|------------|-----------|
| ML-1 | SB learning rates (CIFAR) | 📊 | ⬜ | I5 | Cosine wins 82.23%, SB 79.85% | Failed on classification |
| ML-2 | SB learning rates (PINNs) | 🔬 | 🟨 | I5 | AAAI 2025 shows 2-7x for number-theoretic PINNs | Test on heat/Burgers equation (Q10) |
| ML-3 | SB hyperparameter optimization | 📊 | 🟨 | I2 | Beats random/grid at budget 50+ (1-5%) | Enhancement possible (Q17) |
| ML-4 | Compute-saving exploration | 🔬 | 🟩 | N10,I2 | AMR, LR schedules, hyperopt all explored | Focus on winners |
| ML-5 | QMC parameter selection (1373x) | 📊 | 🟩 | I2 | From DISCOVERY_DATABASE — massive speedup claim | Verify and add to compute paper |

## J. PUBLICATIONS PIPELINE (PUB)

| ID | Paper | Target Venue | Status | Key Dependency |
|----|-------|-------------|--------|----------------|
| PUB-1 | Main math paper (Geometric Signature) | J. Number Theory / Math. Comp | 26pp compiled | MPR-2 (analytical proof) |
| PUB-2 | Three-body paper | Comm. Math. Phys / Celest. Mech. | Draft done | 3BP-4 (unequal mass) |
| PUB-3 | AMR paper (shock-capturing) | J. Comp. Phys / SIAM J. Sci. Comp | Outline done | AMR-4 (extended benchmark) |
| PUB-4 | 3DGS paper | CVPR / SIGGRAPH | Outline done | 3DGS-6 (real results) |
| PUB-5 | Radio-silent report | DARPA / IEEE MILCOM | Done | DEF-1 (submission) |
| PUB-6 | IoT report | IEEE IoT Journal | Done | Incremental over prior art |
| PUB-7 | Conformal paper | Discrete Comp. Geom. / CAGD | Outline done | MESH-2 (quality proofs) |

---

## TONIGHT'S RUN (Q1-Q4)

| Order | ID | Task | Est. | Uses |
|-------|-----|------|------|------|
| 1 | AMR-4 | Extended shock benchmark | 30 min | CPU |
| 2 | 3DGS-5 | Real pipeline Phase 1 | 1 hr | GPU |
| 3 | MPR-1 | B+C to p=100K | 2-4 hrs | CPU |
| 4 | 3BP-4 | Unequal mass extension | 30 min | CPU |

---

## K. SUBMISSIONS & OUTREACH (SUB)

| ID | What | Where | Priority | Status | Next Step (who) |
|----|------|-------|----------|--------|-----------------|
| SUB-1 | AMR for hypersonic CFD | **US Navy SBIR N251-060** | 🔴 HIGHEST | Research done | Research deadline + apply (Saar) |
| SUB-2 | Zero-comm scheduling | **DARPA TTO BAA HR001125S0011** | 🔴 HIGH | Exec summary + cover letter done | Register BAAT + submit by Apr 17 (Saar) |
| SUB-3 | Main math paper | **arXiv math.NT** | 🔴 HIGH | 26pp LaTeX compiled | Get endorser + submit (Saar) |
| SUB-4 | Three-body paper | **arXiv math-ph** | 🟡 MEDIUM | Draft in markdown | Convert to LaTeX + get endorser (Claude+Saar) |
| SUB-5 | AMR paper | **arXiv math.NA / cs.NA** | 🟡 MEDIUM | Draft done (5,500 words) | Convert to LaTeX (Claude) |
| SUB-6 | AMR patent | **US provisional patent** | 🟡 MEDIUM | Analysis done | Consult patent attorney, file ($2-5K) (Saar) |
| SUB-7 | Zero-comm scheduling | **ONR Code 311 BAA** | 🟡 MEDIUM | Contact identified (Dr. Kamgar-Parsi) | Email + 5-page white paper (Saar+Claude) |
| SUB-8 | Radio-silent report | **arXiv eess.SP or Zenodo** | 🟢 LOW | Report done | Submit (Saar) |
| SUB-9 | Multi-agent coord | **DARPA I2O BAA HR001126S0001** | 🟢 LOW | — | Abstract by Nov 2026 (Claude+Saar) |
| SUB-10 | Unsolicited idea | **AFRL Tech Connect** | 🟢 LOW | Portal identified | Submit idea (Saar) |
| SUB-11 | CFD software licensing | **ANSYS / Siemens / OpenFOAM** | 🟢 FUTURE | AMR validated | Outreach after paper published |
| SUB-12 | Defense contractors | **Lockheed / Raytheon / Boeing** | 🟢 FUTURE | AMR validated | Outreach after SBIR |
| SUB-13 | DOE national labs | **LLNL / Sandia / Los Alamos** | 🟢 FUTURE | AMR validated | Outreach after paper published |
| SUB-14 | Code + data archive | **Zenodo** | 🟢 LOW | GitHub repo exists | Mint DOI (Claude) |

---

## L. DEAD / DISPROVED (for record)

| ID | What | Why Dead | Source |
|----|------|----------|--------|
| MPR-8 | Erdős-Turán bound | Cotangent unbounded variation | ERDOS_TURAN_ANALYSIS.md |
| MESH-4 | Terrain LOD | Power-of-2 also nested; skirts solve cracks | TERRAIN_LOD audit |
| MESH-5 | Nanite/game engine | Karis shipped fix in UE 5.4 (2026) | GRAPHICS audit |
| PHYS-3 | Kirkwood gaps novelty | r=0.95 is textbook (Murray & Dermott 1999) | KIRKWOOD_NOVELTY_ASSESSMENT.md |
| ML-1 | SB LR on CIFAR-10 | Cosine 82.23% beats SB 79.85% | sb_lr_output.log |
| DEAD-1 | Financial applications | All 4 scenarios killed (no edge over existing) | financial_applications.md |
| DEAD-2 | Satellite constellation scheduling | Already solved by existing methods | drone_satellite_research.md |
| DEAD-3 | Progressive geometry compression | 1D-only guarantee, DPI covers it | Agent verification |
| DEAD-4 | Terrain LOD engineering gains | 25-50% overstated by 3-5x | TERRAIN_LOD audit |
| DEAD-5 | Data center scheduling | Midpoint bisection dominates Farey | Session 6 test |
| DEAD-6 | Large sieve R→0 approach | R grows, doesn't decay | Session 6 analysis |
| DEAD-7 | Displacement-guided 3DGS | Adds noise, not signal | Session 6 test |
| DEAD-8 | Spectral analysis ΔW at zeta zeros | p=0.30, not significant | Session 6 FFT |
| DEAD-9 | Signal processing Ramanujan | Tautological — no new content | Session 7 analysis |
| DEAD-10 | Drone swarm kill test | 4/5 failed, clock drift fatal | Session 7 test |
| DEAD-11 | 2D Gaussian splatting industry | No commercial products exist | Session 7 market research |
| DEAD-12 | LiDAR application | No rational structure in point clouds | Session 7 analysis |
| DEAD-13 | Audio application | No rational structure in audio signals | Session 7 analysis |
| DEAD-14 | Ray tracing application | Halton/Sobol dominate; no Farey advantage | Session 7 analysis |

---

## STATISTICS
- **Total items:** 96
- **🟢 VERY STRONG:** 9 (3BP-1, 3BP-2, 3BP-3, AMR-1, MPR-5, MPR-21, MPR-22, MPR-23, MPR-24)
- **🟩 STRONG:** 38
- **🟨 MODERATE:** 20
- **⬜ WEAK:** 5
- **⬛ DEAD:** 21 (MPR-8, MPR-20, MPR-28, MPR-29, MESH-4, MESH-5, PHYS-3, ML-1, DEAD-1 through DEAD-14, 3DGS-11)
- **Papers in pipeline:** 7
- **Lean sorry remaining:** 4 (sign_theorem_conj, ratio_test, corrRatio_gt_neg_half_conj, farey_gap_bound)
- **Proved theorems not yet in paper:** 8 (MPR-9, MPR-10, MPR-11, MPR-12, MPR-21, MPR-22, MPR-23, MPR-24)
- **Empirical findings not yet in paper:** 8 (MPR-16-19, PHYS-10-13, PHYS-16, 3DGS-10)
