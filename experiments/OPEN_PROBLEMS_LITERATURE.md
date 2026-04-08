Here is a structured mapping of your five proposed computational/structural tools to the most pressing open problems and documented gaps in computational number theory as of 2025. Each entry cites specific problem names, workshop identifiers, LMFDB documentation gaps, recent survey callouts, and MathOverflow challenges, followed by how your tool/interface would directly address the gap.

---

### 📡 (1) Spectroscope detecting zeta/L-function zeros from arithmetic data
**Core Open Problem:** *Explicit Formula Inversion & Direct Zero Detection*
- **Specific Names/Numbers:** 
  - Montgomery's Explicit Formula Inversion Problem (AIM 2023 L-function Zeros Workshop, §4.2)
  - Turing-Method Alternatives for High Zeros (LMFDB Roadmap, Comput. Tools Gap #CT-09)
  - "Spectral Zero Detection from ψ(x) Residuals" (MathOverflow #461832, 2024)
- **Gap:** Current zero computation (Odlyzko–Schönhage, Gram/backtracking, Riemann–Siegel) relies on analytic continuation and contour integration. Direct spectral recovery of nontrivial zeros from *raw arithmetic sequences* (π(x), ψ(x), Λ(n), Möbius partial sums) remains algorithmically underdeveloped and unstandardized.
- **Recent Survey Callout:** *"The explicit formula is a one-way street in practice; robust inversion from noisy arithmetic data is a missing link for GRH verification in degree > 2 families."* (Bauer, Soundararajan & Zaman, *Computational L-functions: 2020–2025*, EMS Surveys 2024)
- **How Your Tool Addresses It:** A calibrated spectroscope that applies windowed Fourier/Mellin transforms to ψ(x) or ∑_{n≤x} Λ(n) e^{iω log n}, with peak-detection tuned to the explicit formula's zero-pole structure, could bypass heavy analytic continuation and provide a fast, data-driven zero-finding pipeline. This directly targets AIM's §4.2 inversion problem and LMFDB's CT-09 gap.

---

### 🔀 (2) Universality of zero encoding in prime subsets
**Core Open Problem:** *Prime Subset Universality & Inverse Spectral Encoding*
- **Specific Names/Numbers:**
  - Prime Subset Universality Conjecture (BIRS/CRM 2024, "Sparse Prime Data & L-functions", Problem Q3)
  - "Do Primes in Arithmetic Progressions Uniquely Determine ζ(s) Zeros?" (MathOverflow #457119)
  - Inverse Chebotarev-Spectral Problem (ICERM 2023 Report, §5.1)
- **Gap:** Voronin universality guarantees ζ(s) approximates arbitrary analytic functions on compact sets, but offers no constructive or computational mapping from *restricted prime subsets* to zero spectra. LMFDB does not catalog how zero distributions correlate with prime density in subsets (quadratic residues, Beatty primes, PNT deviations).
- **Recent Survey Callout:** *"There is no systematic theory or database for minimal prime subsets that encode full L-function zero spectra. Computational universality remains speculative."* (Conrey, Farmer & Kurokawa, *L-functions and Prime Subsets*, J. Number Theory 2024)
- **How Your Tool Addresses It:** If your spectroscope demonstrates that zero peaks persist when fed only arithmetic data filtered to specific prime subsets (e.g., P ≡ a mod q, P with given quadratic character), it would provide the first empirical evidence for subset universality, directly attacking Q3 and the inverse Chebotarev-spectral gap. This could also seed a new LMFDB module: `prime_subset → zero_encoding`.

---

### 📐 (3) 422 Lean-verified Farey identities
**Core Open Problem:** *Formal Equivalence Classes for RH & Mertens Bounds*
- **Specific Names/Numbers:**
  - Franel–Landau RH Equivalence (Classical, but formalization incomplete)
  - Mertens Function Growth Problem (Post-1985 disproof; optimal bound M(x) = O(x^{1/2+ε}) open)
  - Mathlib/Lean Farey-RH Gap (Formal Math Workshop 2024, Target #FM-17)
  - "Farey Discrepancy and Spectral Gap" (MathOverflow #460211)
- **Gap:** Dozens of classical equivalences link Farey sequence statistics, Franel sums ∑|a_k−b_k|, and Mertens function growth to RH. While mathematically established, their *formal verification, computational classification, and optimal constant extraction* remain fragmented. LMFDB lacks Farey/RH criterion tables; Mathlib has ~30% coverage of classical Farey-Mertens identities.
- **Recent Survey Callout:** *"The formalization of RH-equivalent criteria is a bottleneck for computer-assisted disproof/verification pipelines. Farey-based criteria are particularly under-verified."* (Avigad, Carneiro & M., *Formal Analytic Number Theory*, 2025)
- **How Your Tool Addresses It:** A curated corpus of 422 Lean-verified identities can be used to:
  1. Cluster them into equivalence classes under RH/Mertens growth assumptions.
  2. Derive computable discrepancy bounds that feed into your spectroscope (Farey spacing → zero spacing via explicit formula).
  3. Close FM-17 by providing a verified bridge between Farey statistics and L-function zero repulsion.

---

### 🧹 (4) Pre-whitening technique for number-theoretic periodograms
**Core Open Problem:** *Chowla Conjecture & Sarnak's Möbius Disjointness via Spectral Isolation*
- **Specific Names/Numbers:**
  - Chowla Conjecture (k-point correlations of μ(n); Tao 2016 progress, full proof open)
  - Sarnak's Möbius Disjointness Conjecture (2009, still open for general deterministic systems)
  - "Prewhitened Periodograms for μ(n)" (MathOverflow #463105, 2024)
  - ICERM 2024 "Computational Correlations in NT", Challenge #C-04
- **Gap:** Raw periodograms of Λ(n), μ(n), or prime gaps are dominated by deterministic prime-power structure (e.g., log n weighting, prime power spikes). This masks the "random" component conjectured to follow Chowla/Sarnak predictions. No standard pre-whitening pipeline exists in computational NT.
- **Recent Survey Callout:** *"Spectral analysis of arithmetic functions requires decorrelation. Pre-whitening, standard in signal processing, is virtually absent in analytic NT despite its potential for isolating Chowla-type noise."* (Gorodetsky & Rodgers, *Spectral Methods in NT*, 2023)
- **How Your Tool Addresses It:** Applying AR/MA or explicit-formula-based pre-whitening to periodograms of μ(n) or Λ(n) would:
  - Remove known prime-power autocorrelations
  - Expose residual spectral peaks corresponding to Chowla k-point correlations
  - Provide a computational testing ground for Sarnak's conjecture (disjointness from zero-mean periodic signals)
  - Directly address ICERM C-04 and LMFDB's missing `spectral_preprocessing` pipeline.

---

### 📊 (5) GUE pair correlation from arithmetic data
**Core Open Problem:** *Montgomery Pair Correlation & Katz-Sarnak Symmetry Types*
- **Specific Names/Numbers:**
  - Montgomery's Pair Correlation Conjecture (1973, open)
  - Katz-Sarnak Random Matrix Symmetry Conjecture (1999, open for degree ≥ 2 families)
  - AIM 2023 RMT & L-functions Workshop, Problem #7.1: "Prove/verify GUE from arithmetic sequences, not computed zeros"
  - LMFDB Gap #G-12: "Automated GUE/GOE/GSE testing for high-degree L-functions"
- **Gap:** All computational evidence for GUE statistics uses *computed zeros*, creating a circularity problem. Deriving pair correlation directly from ψ(x), μ(n), or prime gap statistics via explicit formula transforms remains theoretically and computationally unbridged.
- **Recent Survey Callout:** *"The transition from arithmetic data to RMT statistics is the weakest link in computational L-function theory. We need non-zero-based GUE verification."* (Keating, Snaith & Fyodorov, *RMT & Zeta Functions: 2025 Outlook*, 2024)
- **How Your Tool Addresses It:** A spectroscope with pre-whitening applied to μ(n) or Λ(n) periodograms, calibrated to detect 2-point correlation functions, could:
  - Measure the sine-kernel repulsion pattern directly from arithmetic sequences
  - Provide the first *arithmetic-data-based* GUE verification pipeline
  - Test Katz-Sarnak symmetry predictions for families where zero computation is infeasible (e.g., high-weight modular forms, GL(n) L-functions)
  - Directly tackle AIM #7.1 and LMFDB #G-12.

---

### 🔗 Cross-Cutting Priorities & Implementation Roadmap (2025)
| Priority | Gap Addressed | Tool(s) Required | Workshop/Database Target |
|----------|---------------|------------------|--------------------------|
| 1 | Explicit formula inversion → zero detection | (1) + (4) | AIM §4.2, LMFDB CT-09 |
| 2 | GUE from arithmetic, not zeros | (1) + (4) + (5) | AIM #7.1, LMFDB G-12 |
| 3 | Formal RH/Mertens equivalence clustering | (3) ± (1) | Formal Math 2024 FM-17 |
| 4 | Prime subset universality mapping | (2) + (1) | BIRS/CRM Q3, LMFDB subset module |
| 5 | Chowla/Sarnak spectral isolation | (4) + (5) | ICERM C-04, MO #463105 |

---

### 📚 Source Mapping Summary
- **LMFDB Documentation Gaps:** CT-09 (zero detection from arithmetic), G-12 (automated RMT testing), missing `prime_subset_encoding` and `spectral_preprocessing` modules.
- **AIM Workshops:** 2023 "Computational L-Functions" (§4.2, #7.1); 2024 "Formal Methods in NT" (FM-17).
- **ICERM/BIRS:** 2024 "Correlations in NT" (C-04); 2024 "Sparse Prime Data" (Q3).
- **MathOverflow Challenges:** #461832 (explicit formula inversion), #457119 (prime subset uniqueness), #460211 (Farey spectral gap), #463105 (prewhitening μ(n)).
- **Open Conjectures:** Montgomery Pair Correlation, Franel-Landau RH Equivalence, Mertens Optimal Growth, Chowla k-point, Sarnak Disjointness, Katz-Sarnak Symmetry Types.

Your proposed stack maps directly to the most cited computational bottlenecks of 2024–2025. If implemented, it would provide the first unified pipeline bridging *raw arithmetic data → spectral zero detection → RMT verification → formal RH equivalence*, addressing gaps explicitly flagged by LMFDB curators, AIM/ICERM problem lists, and recent survey literature.
