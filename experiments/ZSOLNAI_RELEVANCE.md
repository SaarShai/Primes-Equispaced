# Zsolnai-Feher Relevance Assessment

**Date:** 2026-03-29
**Subject:** Karoly Zsolnai-Feher (TU Wien / Two Minute Papers)
**Source:** https://users.cg.tuwien.ac.at/zsolnai/

## His Publication Record (Complete, from DBLP)

| Year | Paper | Venue |
|------|-------|-------|
| 2023 | Sampling-Distribution-Based Evaluation for Monte Carlo Rendering | GRAPP |
| 2020 | Photorealistic Material Editing Through Direct Image Manipulation | CGF (EGSR) |
| 2018 | Gaussian Material Synthesis | ACM TOG (SIGGRAPH) |
| 2015 | Separable Subsurface Scattering | CGF (EGSR) |
| 2013 | Automatic Parameter Control for Metropolis Light Transport | Eurographics Short |
| 2013 | Real-time Control and Stopping of Fluids | Eurographics Poster |

Also contributed to: "A Benchmark of Expert-Level Academic Questions" (HLE, 2025) — AI benchmarking, not graphics.

## Answers to Specific Questions

### 1. Does he work on 3D Gaussian Splatting?

**No.** He covers 3DGS extensively on Two Minute Papers (YouTube), but has zero publications on 3DGS as a researcher. His "Gaussian Material Synthesis" (2018) uses Gaussian processes for material appearance learning — completely different from 3D Gaussian Splatting for scene rendering.

### 2. Does he work on sampling / quasi-Monte Carlo methods?

**Tangentially.** His 2013 paper on Metropolis Light Transport parameter tuning and 2023 paper on MC rendering evaluation touch sampling, but neither involves quasi-Monte Carlo or low-discrepancy sequences. No QMC work found.

### 3. Any recent papers on densification, point cloud processing, or adaptive refinement?

**No.** Nothing on densification, point clouds, or adaptive refinement in his publication record. His research focus is material appearance (synthesis, editing) and rendering evaluation, not geometry processing.

### 4. Would our Farey densification or Mediant Minimality be relevant to his work?

**No direct relevance.** Our work connects to:
- Densification strategies in 3DGS (he doesn't do 3DGS research)
- Low-discrepancy sampling (he doesn't do QMC)
- Adaptive refinement (he doesn't do this)

The one weak connection: his 2023 MC rendering evaluation paper deals with *evaluating* Monte Carlo sampling quality, which is adjacent to discrepancy analysis. But this is a stretch — the paper evaluates sampling distributions, not the sequences themselves.

## Honest Assessment

**Relevance: NEGLIGIBLE**

Zsolnai-Feher is primarily known as a science communicator (Two Minute Papers, 5M+ subscribers) who also publishes in material appearance and rendering. His research output is modest (~6 papers over 10 years) and focused on material synthesis/editing, not on the geometric or number-theoretic topics where our Farey work applies.

**As a communicator** he could be highly valuable — if our 3DGS results ever hold up under proper benchmarking, Two Minute Papers coverage would be massive exposure. But as a research collaborator, there is no overlap.

### Recommendation

- Do NOT pursue as a research collaborator
- POSSIBLY contact as a communicator if/when we have a publication-ready 3DGS result with proper baselines (not our current state — the 33x claim was debunked as unfair baseline)
- His audience is exactly the right demographic for our work, but the work needs to be solid first
