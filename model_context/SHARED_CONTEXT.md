# Shared Context for Local Models
Updated: 2026-04-06

## Project: Farey Research
Independent researcher (Saar Shai) studying per-step Farey discrepancy and its connection to Riemann zeta zeros.

## Two Papers
1. Paper 1: "The Geometric Signature of Primes in Farey Sequences" — ready for arXiv
2. Paper 2: "The Compensated Mertens Spectroscope" — in development

## Key Objects
- ΔW(N) = W(F_{N-1}) - W(F_N): per-step Farey discrepancy (NOVEL object)
- F_comp(γ) = γ²·|Σ M(p)/p · e^{-iγ log p}|²: compensated Mertens spectroscope
- R(p) = ΣD·δ/Σδ²: Farey insertion-deviation correlation ratio

## Key Results (verified)
- Spectroscope detects 20/20 zeta zeros (local z-score)
- γ² matched filter: NOVEL (no prior art in number theory)
- M(p)/√p weight 1.7x better than R(p) (bootstrap verified)
- Psi spectroscope edges Mertens for higher zeros
- Universality: any prime subset works (NOVEL)
- GUE pair correlation: RMSE=0.066 vs Wigner surmise
- 25M primes optimal (19/20, 0.26% error)
- Amplitude anti-correlates (r=-0.44): cross-zero interference
- Siegel zero: 465M sigma sensitivity for q≤13

## CRITICAL: Novelty
Fourier duality primes↔zeros is CLASSICAL (cite Csoka 2015, Planat et al).
Our novel contributions: γ² filter, local z, Farey connection, universality, quantitative analysis.

## File Locations
- Paper: ~/Desktop/Farey-Local/paper/main.tex
- Experiments: ~/Desktop/Farey-Local/experiments/
- Figures: ~/Desktop/Farey-Local/figures/
- Wiki: ~/Documents/Spark Obsidian Beast/Farey Research/wiki/
- R(p) data: ~/Desktop/Farey-Local/experiments/R_bound_200K_output.csv

## Output Convention
- Write results to ~/Desktop/Farey-Local/experiments/YOUR_TASK_NAME.md
- Include: date, method, key findings, limitations, next steps
- Be honest about what is proved vs computational vs speculative
