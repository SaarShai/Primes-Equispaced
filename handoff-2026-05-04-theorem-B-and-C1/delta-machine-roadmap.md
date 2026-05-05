# Δ-Machine Roadmap — Goals + Task Plan

## Goal

Lift Smoothed Δw_f / Δ-arithmetic / Δ-machine / Multi-L results to maximally significant, interesting, valuable outcomes — for math research AND practical applications.

## Top 5 Goals (ranked: significance × realism × value)

| # | Goal | Tier | P(success) | Value |
|---|---|---|---:|---|
| **G1** | **Δ-machine bundled Compositio paper** (~50p): master + extended + multi-L + applications §6 | Compositio | 0.80 | High novelty, citable framework |
| **G2** | **Higher-order polylog conjecture proof** : \|S^{(k)}_ζ(N) − R₀^{(k)}\| = O((log N)^{k−1}) for k≥2 | Compositio sub-paper | 0.55 | New theorem, RMT bridge |
| **G3** | **Lean-verified full Δw_f theorem** (~600 LOC, beyond current stub) via Aristotle | Machine-verified | 0.70 | Math.Comp / formal-math journal |
| **G4** | **GL(3) Δ-machine concrete** via sym²(GL(2)) — companion paper | Inventiones companion | 0.50 | Higher-rank extension |
| **G5** | **Δ-machine computational toolkit** (Sage/SymPy package) — practical | OSS release | 0.85 | Real-world utility, citations |

## Tasks (10 total, parallel where possible)

| Task | Compute | Description | Verify |
|---|---|---|---|
| **T1** | M1B (curated queue) | Extend Smoothed_Dwf numerical to N=10⁶ at 50 digits with 200+ ζ-zeros; confirm 10-digit match | output file mismatch < 10⁻⁹ |
| **T2** | **Aristotle** (priority) | Extend SmoothedDwfFormula.lean from stub → full theorem with R0_eq_neg_two, mellin_transform, contour_shift lemmas (~600 LOC) | `lake build SmoothedDwfFormula` succeeds |
| **T3** | **Aristotle** (priority) | Lean-formalize Δ-machine master theorem (Selberg-class explicit formula) → `DeltaMachineMaster.lean` (~400 LOC) | compile + decide-style verification on ζ case |
| **T4** | M2 (re-enable) + MiMo/Mistral | Higher-order polylog conjecture: extend numerical k=2,3,4 at N=10², 10³, 10⁴, 10⁵ with ≥30 zeros each | residual ≤ C·(log N)^{k-1} for fitted C |
| **T5** | OpenRouter / Cerebras (large context) | Adversarial review of Multi-L paper draft: check Macdonald-Cauchy → plus-tensor RS identification against Murty-Murty 2009, Kaczorowski-Perelli 1999/2010, Liu-Wang-Ye 2005 — confirm novelty | findings file lists prior-art status per claim |
| **T6** | Cohere / Mistral | Lit research: find every Compositio/Inventiones paper using Selberg-class smoothed-sum machinery, build comprehensive bibliography for G1 paper | bibliography file with ≥20 entries, URLs |
| **T7** | M1B + Sage | **Build Sage/SymPy "deltamachine" Python package**: implement μ_L, R₀ extraction, zero-sum truncation; ship with examples for ζ, Dirichlet, Δ, ECs | `pip install -e .` works, examples produce 10-digit match |
| **T8** | Aristotle + MiMo | GL(3) sym²(f) explicit formula concrete derivation: pick f = 11a1 elliptic curve, sym²f is GL(3) automorphic, derive Δ-machine on 1/L(s, sym²f) | symbolic + 5-digit numerical match |
| **T9** | Groq (fast lit-search) / Mistral | Locate 5+ "open problem" applications where Δ-machine adds value: extend Mertens Ω, Sato-Tate uniform-k, μ⋆μ variants. Cross-check with Delta_machine_open_problems.md | new applications file, 5 entries, each with sketch + bound |
| **T10** | Sonnet (synthesis) | Bundle G1 Compositio paper: stitch master + extended + multi-L + §6 + computational toolkit appendix into single coherent ~50-page draft | publication-grade Markdown + LaTeX-ready |

## Done When

- [ ] G1 Compositio paper draft complete (T1+T5+T6+T10)
- [ ] G2 polylog conjecture: proof or rigorous reduction (T4 + currently-running Opus agent)
- [ ] G3 Lean theorem compiles (T2+T3 via Aristotle)
- [ ] G4 GL(3) concrete instance verified (T8)
- [ ] G5 deltamachine package on GitHub (T7)

## API Reachability — Test First

| API | Status | Path | Notes |
|---|---|---|---|
| **Aristotle** | configured | harmonic.fun + key in `~/Documents/Spark Obsidian Beast/Design Claude/wiki/AI-Setup/API Keys & Credentials.md` | **PRIORITIZE — Lean formalization** |
| MiMo | known good | `MIMO_API_KEY` (sk-...), `~/.farey_api_keys` | always set `"thinking":{"type":"disabled"}` else `content` empty |
| Cerebras | known issue | curl with `-A 'Mozilla/5.0'` (Cloudflare blocks urllib) | reachable via wrapper |
| Groq | known issue | same Cloudflare workaround | reachable via wrapper |
| Cohere | **untested** | needs key check in `~/.farey_api_keys` | will test on first dispatch |
| Mistral | **untested** | needs key check | will test on first dispatch |
| OpenRouter | **untested** | needs key check | will test on first dispatch |
| M1B | alive (PID 96832) | `~/bin/compute_control.sh status` shows runner alive, queue empty | ready |
| M2 | **paused** | per `~/bin/compute_control.sh status`: "DISABLED (paused)" | re-enable for T4 |

**Before T4-T9 dispatch**: run `cat ~/.farey_api_keys` to confirm Cohere/Mistral/OpenRouter keys, and `~/bin/compute_control.sh start` to re-enable M2.

## Notes

- **Aristotle prioritized** per user directive — Lean tasks T2, T3, T8 should hit Aristotle first
- **Honest framing**: Annals-tier Theorem B-exact remains GDC-blocked (separate from Δ-machine work)
- **Δ-machine independent of Theorem B**: these goals stand on their own merit; not blocked by 4-level density wall
- **Currently running (background)**: 3 resumed agents (polylog, LMFDB c_f, GL(n)) — outputs feed T2, T4, T8 directly when they land
- **Estimated wall-clock**: G1 paper draft 3-6 weeks; G2 polylog 4-8 weeks; G3 Lean 4-8 weeks Aristotle; G4 GL(3) 6-12 weeks; G5 toolkit 2-4 weeks
