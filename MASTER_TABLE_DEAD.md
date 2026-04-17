# DEAD / DISPROVED Archive
Moved from MASTER_TABLE.md 2026-04-04 for context efficiency.

| ID | What | Why Dead | Source |
|----|------|----------|--------|
| MPR-2 | B+C analytical proof (δ² bound) | B+C NOT universally >0. p=243,799 counterexample. All 8 proof paths killed. | Session 10 |
| MPR-3 | B+C ratio test approach | Same — target is false | Session 10 |
| MPR-4 | Unconditional Sign Theorem | DISPROVED at p=243,799. R=-3.052 → ΔW>0 | Session 10 |
| MPR-8 | Erdos-Turan bound | Cotangent unbounded variation | ERDOS_TURAN_ANALYSIS.md |
| MPR-13 | Rayleigh quotient proof | Target (B+C>0) is false | Session 10 |
| MPR-14 | Schur convexity proof | Same | Session 10 |
| MPR-20 | Spectral analysis ΔW at zeta zeros | p=0.30, not significant | Session 6 |
| MPR-28 (A.sect) | Large sieve R→0 | R grows, doesn't decay | Session 6 |
| MPR-29 (A.sect) | Displacement-guided 3DGS | Adds noise, not signal | Session 6 |
| 3DGS-1-12 | ALL 3DGS densification | User decision 2026-04-04. No real-image advantage. | Session 10 |
| MESH-4 | Terrain LOD | Power-of-2 also nested | TERRAIN_LOD audit |
| MESH-5 | Nanite/game engine | Karis shipped fix UE 5.4 | GRAPHICS audit |
| PHYS-3 | Kirkwood gaps novelty | Textbook material | Murray & Dermott 1999 |
| ML-1 | SB LR CIFAR-10 | Cosine wins 82.23% vs 79.85% | sb_lr_output.log |
| DEF-1-4 | All defense/silent-coord | Clock drift structural flaw | DEAD-15, Session 7 |
| PUB-4 | 3DGS paper | Direction killed | Session 10 |
| SUB-2 | DARPA TTO BAA | Clock drift | Session 10 |
| DEAD-1 | Financial applications | No edge over existing | financial_applications.md |
| DEAD-2 | Satellite scheduling | Already solved | drone_satellite_research.md |
| DEAD-3 | Progressive geometry compression | 1D only | Agent verification |
| DEAD-4 | Terrain LOD engineering gains | Overstated 3-5x | TERRAIN_LOD audit |
| DEAD-5 | Data center scheduling | Midpoint bisection dominates | Session 6 |
| DEAD-6-8 | Large sieve, 3DGS displacement, ΔW spectrum | Various failures | Session 6 |
| DEAD-9-14 | Ramanujan, drones, 2DGS, LiDAR, audio, ray tracing | No structure/advantage | Session 7 |
| DEAD-15 | Silent coordination (ALL defense) | Clock drift 0.011ms vs 1.03ms TDMA. Structural, unfixable. | Session 7 |
| DEAD-16-23 | 8 B+C proof paths | Fourier k=p negative, induction fails, Weil mismatch, partial sums oscillate, delta-cosine false, six-term unproved, ergodic magnitude-only, Abel 4000x weak | Sessions 9-10 |
| DEAD-24 | Sign Theorem universality | DISPROVED p=243,799 (R=-3.052) | Session 10 |
| DEAD-25 | B+C > 0 universally | DISPROVED same prime | Session 10 |
| DEAD-26 | Hamiltonian decomposition | No math connection to Farey | Session 10 |
| DEAD-27 | Perfect numbers | σ(n) vs φ(n) — different NT | Session 10 |
| DEAD-28 | Farey primality testing | O(p²) vs O(log²n) | Session 10 |
| DEAD-29 | Spectral Enhancement Theorem (MPR-48) | Bridge D≈M(q_{m-1}) is FALSE (zero correlation). Supporting data wrong (c_m=p has D=0). Low-pass needs L>1000, impractical. Codex adversarial review. | Session 10, SPECTRAL_ENHANCEMENT_ADVERSARIAL_REVIEW.md |
| DEAD-30 | MPR-46: Depth→γ₁ structural proof | Depended on Spectral Enhancement Theorem (DEAD-29). Bridge D≈M(q) is false. No viable alternative bridge. | Session 10, adversarial review |
| DEAD-31 | R>0 via permutation identity Σf·δ=C/2 | Symmetry: Σ rank·δ = (n+1)/2 · Σδ EXACTLY. Gives equality, not strict inequality. Cannot prove R>0 this way. | task_115, overnight run |
