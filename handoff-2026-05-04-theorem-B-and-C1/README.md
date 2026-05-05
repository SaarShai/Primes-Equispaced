# Farey Handoff Bundle — 2026-05-04

**Two handoff documents for math researcher review:**

- [`THEOREM_B_HANDOFF.md`](THEOREM_B_HANDOFF.md) — Milinovich-Ng family-averaged conjecture (16). Cage uncond 0.97, exact 2/(3π) GRH-cond 0.85, 16 failed unconditional attacks indexed (n=4 density wall structural).
- [`C1_SELF_RESIDUE_HANDOFF.md`](C1_SELF_RESIDUE_HANDOFF.md) — Spectroscope C1 mechanism. Synthesis Identity (E) reduces ratios-conjecture obstruction to single Eisenstein-side residue. B2 R_neigh α_ratio=1 forced by Soshnikov 2000a. F(γ) uniform-in-T 0.88. MK3 universal Spectroscope 0.95. Smoothed Δw_f R₀=-2.

**Δ-machine framework (Compositio submission):**
- [`Delta_machine_paper_bundle.md`](Delta_machine_paper_bundle.md) — 5484-word paper bundle (Theorems 2.1-2.7)
- [`Delta_arithmetic_generalization.md`](Delta_arithmetic_generalization.md) — master theorem + §6 Applications
- [`Delta_machine_extended.md`](Delta_machine_extended.md) — 4 closed extension theorems
- [`Delta_machine_multi_L.md`](Delta_machine_multi_L.md) — Cross-Selberg via Macdonald-Cauchy

**Paper drafts:**
- [`PAPER_DRAFT_TheoremB_WeightAspect.md`](PAPER_DRAFT_TheoremB_WeightAspect.md) — Annals/PLMS draft
- [`Smoothed_Dwf_publishable.md`](Smoothed_Dwf_publishable.md) — Compositio draft (604 lines)

**Lean (compiles in Mathlib 4.28.0):**
- `CageHalfWidth.lean` — √145/(12π) algebra
- `MertensDecomposition.lean` — B(p) = 2·B₀(p-1) − 2·S_ψ(p)
- `SmoothedDwfFormula.lean` — R₀ = -2 via 1/ζ(0)
- + `BridgeIdentityStatement`, `DeltaMachineMaster`, `CFKRSFactorSixteen`, `CageRescaledAlgebra`, `GL2RiemannVonMangoldt`, `MertensRestrictedPosStatement`, `ReverseEngineerDecomp`

323 files total. Author: Saar Shai (independent researcher) + AI-assisted exploration.
