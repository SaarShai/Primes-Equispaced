---
schema_version: 1
title: "Plan: Technical/Computational section, Saar–Koyama joint paper"
date: 2026-05-12
type: section-plan
tier: working
status: PLAN_ONLY_NO_THEOREM_PROMOTION_NO_SEND
audience: internal (Saar, Saar's local tooling)
deliverable_owner: Saar Shai
manuscript_co_author: Shin-ya Koyama
trigger:
  - "Koyama 2026-05-12: 'Could you start drafting the Technical/Computational section
    (Methodology of the double-verification, the Lean 4 formalization path, and the
    current numerical findings)?'"
sources:
  - correspondence/raw/koyama-2026-05-12-exchange.md
  - handoff-2026-05-09-followup/Koyama_AK_constant_proof.md
  - handoff-2026-05-09-followup/Koyama_B_infty_proof.md
  - handoff-2026-05-09-followup/Koyama_C1_subleading_proof.md
  - handoff-2026-05-09-followup/Koyama_Perron_remainder_theorem_hunt_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_THEOREM_REGISTRY_2026-05-10.md
  - handoff-2026-05-09-followup/Koyama_claimsafe_paper_outline_2026-05-11.md
  - handoff-2026-05-09-followup/KOYAMA_CLAIM_AUDIT_2026-05-11.md
  - HANDOFF.md
  - formal-conjectures/DirichletPolynomialAvoidance.lean
  - formal-conjectures/DPAC_full.lean
  - formal-conjectures/SmoothedDwfFormula_full.lean
  - formal-conjectures/FareyBridgeIdentity.lean
  - formal-conjectures/FareySignPattern.lean
  - formal-conjectures/MertensSpectroscopeUniversality.lean
tags: [koyama, joint-paper, technical-section, computational-section, lean4, double-verification, plan]
---

# Plan — Technical/Computational section of the Saar–Koyama paper

## 0. Scope and posture (read before anything else)

**What this document is.** A self-contained, audit-trail-grade plan for the
Technical/Computational section Koyama requested on 2026-05-12. It freezes
(a) the precise claim status we will print, (b) the double-verification
protocol, (c) the Lean 4 formalization path, (d) the numerical findings to
report, and (e) the adversarial verification protocol we run before the
section text is fixed.

**What this document is not.** A draft of the section itself, an outbound
email, a commit, or a manuscript. No external action is taken without
explicit user approval. No theorem is promoted in this plan.

**Inherited claim posture (must be respected verbatim).**

1. The Aoki–Koyama 2023 constant is `e^{-γ}`, *not* `1/ζ(2)`. The earlier
   `1/ζ(2)` headline is *historical numerical conjecture, superseded*.
   Cite **Aoki–Koyama 2023, J. Number Theory 245 (2023) 233–262, equation
   (1.4), p. 235** with a verbatim quote embedded in the section.
2. `D_K → e^{-γ}` is `CONDITIONAL`: it composes the AK constant with a
   *not-yet-closed* shifted Perron leading theorem. The shifted Perron
   off-target zero residue aggregate (including possible off-target
   multiple zeros) is the live obstruction; this is the manuscript's
   honest "open challenge".
3. The local Perron residue at `w = 0` is `PROVED` (algebraic).
4. The corrected `B_∞` identity with `BPC1 + BPC2 + T_{≥3}` is `PROVED`
   unconditionally (no GRH/DRH/EDRH needed for the identity).
5. The Sym²/⟨f,f⟩ proportionality in its raw tested form is *falsified*;
   a completed or archimedean-corrected normalization is *not ruled out*
   but is not in scope of this paper.
6. The W2 "rank-linear" trend is *conductor-confounded* in the available
   data; report rank coefficient as not isolated, present the empirical
   model with `log N` included.
7. The EC NDC universality `D_K^E · ζ(2) → 1` is *falsified* in its
   simple sharp-cutoff finite form through `K = 10^6`. Smoothed finite
   evidence is reproducible but the previous load-bearing gate is
   demoted by the null-control audit (`cP_only`, `P_only`, `PL2_only`
   pass at α = 0.75).
8. DPAC remains a formalization/conjectural target, not a theorem.
9. The Lean 4 artifacts are *partial formalization scaffolds*. We must
   describe them as such; we must not present `sorry`-bearing files as
   theorems.

**Headline of the section (single sentence we are willing to print).**

> Within the GL(1) Koyama setting the numerical target constant
> `1/ζ(2)` should be replaced by the Mertens / Aoki–Koyama constant
> `e^{-γ}` under Aoki–Koyama 2023 (1.4) and a shifted Perron-leading
> hypothesis; the unconditional new contribution of this section is the
> corrected `B_∞` identity, the local Perron double-pole residue
> formula, an independent / adversarial double-verification protocol,
> and a partial Lean 4 formalization scaffold whose research-open
> obligations are stated explicitly.

**Cross-check on Koyama's "verified at `10^{13}`" framing — RESOLVED.**

See [`SCOPE_AUDIT_10E13_2026-05-12.md`](SCOPE_AUDIT_10E13_2026-05-12.md).
The `10^{13}` evidence is genuine but its scope is the
**Phase-1 Dominance-of-`-1` residue-count replication**: two
independent implementations agreeing on
`π(1.3·10^{13}) = 445{,}831{,}610{,}611` and on every residue count for
`q ∈ {7, 8, 11, 19, 23}` at `x = 1.3·10^{13}`, a second hardware path
through `x = 1.3·10^{12}`, identity (3.1) of `nontriv.pdf` verified
across 495 cells, dominance signal reproduced for `N ∈ {7, 8, 19}`
(with `N = 11` and Table-4 discrepancies pending Koyama's post-Kiban-S
reconciliation). The analytic identities (`B_∞`, `C_1`, `D_K`,
AK-normalization, EC ensemble) are verified at much smaller `K`
(`K ≤ 2·10^6` for `B_∞`/`C_1`, `K ≤ 10^7` for `D_K`, `K ≤ 10^6` for
EC). In the manuscript these two strands are presented as two **clearly
separated subsections**: replication-scale numbers do not inherit
analytic-scale verification language and vice versa.

---

## 1. Section structure (LaTeX skeleton)

This is the section skeleton we will fill. It is laid out so that every
claim is sourced to a packet in this repository.

```
\section{Methodology, formalization, and numerical evidence}
\label{sec:techcomp}

\subsection{Notation and normalizations}
\label{sec:notation}
% From Koyama_track_grounding.md §2 and KOYAMA_THEOREM_REGISTRY_2026-05-10.md.
% Define: chi primitive non-principal; q conductor; rho = 1/2 + i tau simple
% noncentral zero; E_K, c_K, D_K, B_infty exactly. Fix branch of log L(2 rho, psi)
% as analytic continuation through Re(s) > 1. Spell out the
% arithmetic-vs-analytic normalization for EC/Delta: rho = 1 + i gamma for
% weight-2 EC, rho = 6 + i gamma for Delta; never mix analytic 1/2 + i gamma
% with arithmetic coefficients (this is the bug class that invalidated
% pre-2026-04-15 C_1 results).

\subsection{Methodology of double verification}
\label{sec:methodology}
% Top-level: every numerical claim is computed twice, by two independent
% implementations in two languages with two independent algorithmic paths,
% plus one adversarial review pass. See §2 of this plan.

\subsection{Reproducibility manifest}
\label{sec:reprod}
% Versions, seeds, wall-clock, Zenodo DOI, git commit hash, file-by-file
% manifest. See §3 of this plan.

\subsection{Lean 4 formalization path}
\label{sec:lean}
% Statement of what is Lean-formalized today, what is scaffold, what is
% research-open. Lean 4 + Mathlib4 versions, lake-manifest hash. See §4 of
% this plan and the file inventory below.

\subsection{Numerical findings}
\label{sec:numerics}
% Tables, convergence rates, claim-vs-evidence taxonomy. See §5 of this
% plan.

\subsection{Open challenges}
\label{sec:open}
% Shifted Perron remainder, off-target zero residue aggregate,
% conductor-confounded EC trend, archimedean-corrected Sym^2
% normalization, GL(2) reciprocal-derivative control,
% minimum-modulus estimate for L(E,s). See §6 of this plan.

\subsection{Code, data, and certificate availability}
\label{sec:availability}
% Single statement: code at <URL>, data at <Zenodo DOI>, Lean repo at
% <URL>, certificate logs at <S3/Drive>.
```

---

## 2. Methodology of double verification

### 2.1 What "double verification" means in our manuscript

Following current practice in *Forum of Mathematics Pi/Sigma*,
*J. Number Theory*, *Math. Comp.* (post-2024), and the
PFR/Liquid-Tensor formalization tradition (Tao 2023, Buzzard
et al. 2022), we adopt a three-layer verification stack:

| Layer | Description | Independent of layer above |
|---|---|---|
| **L1. Primary computation** | mpmath (Python), 50 dps unless noted. Direct partial-sum Möbius / Euler-product evaluation. Refines zeros by Muller's method to `|L(ρ,χ)| < 10^{-50}` before use. | — |
| **L2. Independent re-implementation** | PARI/GP (separate process, separate language, independent zero-search via `lfunzeros` + Newton refinement, independent partial-Euler-product summation, native exact rational where load-bearing). Must agree with L1 to within `10^{-40}` for absolute quantities, `10^{-20}` for ratios that involve subtraction of nearly-equal quantities. | Yes — different language, different sieve, different `L'` algorithm. |
| **L3. Adversarial referee pass** | A non-author adversarial agent (or human) attempts the strongest possible objections to each promotion-grade claim; authors respond in an audit log. See §2.4. | Yes — different reasoner, different incentive. |

This stack is what we will describe in §\ref{sec:methodology} of the
paper.

### 2.2 Concrete verification budget per object

For every numerical claim of promotion grade we will print, we run:

| Object | L1 implementation | L2 reimplementation | L3 adversarial pass | Acceptance gate |
|---|---|---|---|---|
| Refined zeros of `L(s, χ)` for the four (χ, ρ) pairs | `mpmath.findroot` (Muller), 50 dps | `lfunzeros(charinit(q, idx), T) + bestappr` then Newton, PARI/GP 2.15.x, default precision 250 bits | Adversarial Mimo: "could a fake/displaced zero give the same `|L'|` and `|L''|`?" | Both implementations agree to `≥ 12` decimal digits in `ρ`; `|L'(ρ,χ)|` and `|L''(ρ,χ)|` agree to `≥ 10` decimals. |
| `C_1 = -L''/(2 L'^2)` at each pair | mpmath direct | PARI: `derivnum(s = ρ, lvalue(L, s), 2) / (2 * derivnum(s = ρ, lvalue(L, s), 1)^2)` with sign convention reconciled | Local Ollama (qwen3.6 35b) re-derives Laurent expansion symbolically and checks the sign / order convention | Match to `≥ 8` decimals on `Re(C_1)` and `Im(C_1)`. |
| `c_K = Σ_{n≤K} μ(n)χ(n) n^{-ρ}` at `K = 2 · 10^5, 10^6, 2 · 10^6, 10^7` | mpmath direct partial sum | PARI partial sum with `forprime` and a separately-sieved μ via independent Eratosthenes; or Arb via FLINT for spot-check at `K = 2 · 10^6` | Adversarial Mimo: "is `o(1)` hiding a `log log` factor that disqualifies the leading-term identification?" | Residual `R(K) = c_K - log K/L'(ρ) - C_1` non-monotone but bounded by `(log K)^{5/4}/√K · O(1)`. |
| `E_K log K` for AK at `K = 10^7` | mpmath direct | PARI Euler product with `prodeuler` truncated at `p ≤ K` | Adversarial Mimo: "could a different branch of `log L(2ρ, ψ)` flip the sign / collapse the gap between `e^{-γ}` and `1/ζ(2)`?" | `|E_K log K · ζ(2) / L'|` drifts from `0.992` at `K = 2 · 10^6` toward `≈ 0.923` at `K = 10^7`, matching `ζ(2)/e^γ`. |
| `B_∞` identity residuals across the four pairs at `K = 2 · 10^6` | mpmath direct (per `Koyama_B_infty.py`) | PARI/GP re-implementation of `T_∞ = (1/2) log L(2ρ,ψ) + BPC_1 + BPC_2 + T_{≥3}` from scratch | Local Ollama re-derives `BPC_1` for `χ_{-4}` (only bad-prime case, `p=2`) symbolically | Residual ≤ `3 · 10^{-3}` for `χ_{-4}` pairs, ≤ `5 · 10^{-5}` for `χ_5, χ_{11}` (matches Saar–Koyama 2026-04-16). |
| EC `D_K^E` and smoothed proxy at `K ≤ 10^6` | mpmath/Python ensemble | PARI re-run with `ellap` and independent rank read-off | Mimo + local Ollama: review the null-control gate failure (`cP_only`, `P_only`, `PL2_only` pass at α=0.75) | Section presents EC as *demoted to diagnostic*, not promotion-grade. |
| W2 regression (`E[C_1²] = a + b · rank + c · log N`) on 22 EC points | NumPy/statsmodels OLS | R `lm()` with HC3 SE, plus a small bootstrap (10⁴) for the rank coefficient | Mimo: "what is the leave-one-out range of `b`?" | Report `R² ≈ 0.81`; rank coefficient is *not stable* under leave-one-out; we say so explicitly. |

### 2.3 What we will NOT print

* Any verified scale we did not own. In particular, the phrase "verified
  at `10^{13}`" goes in only if we re-run at that scale with both L1
  and L2 *or* Koyama supplies the verified computation and we attach
  it as supplementary data with a separate audit log.
* Any "proved NDC" wording. The NDC limit `D_K → e^{-γ}` is presented
  conditionally on AK + the unclosed shifted Perron leading hypothesis.
* Any BSD-flavoured EC universality claim. The smoothed evidence is
  *finite, reproducible, and not a proof candidate*.

### 2.4 Adversarial referee protocol

For every promotion-grade claim, before submission we run an explicit
adversarial pass. This is the "L3" layer above. It is *not* a
self-review; it is performed by independent agents/models with no
authorship incentive. Concrete dispatch lanes:

1. **Mimo (Xiaomi MiMo, `mimo-v2.5-pro`)** — flagship 1M-context model
   on a non-Anthropic stack. Used as an adversarial referee for prose
   claims, branch-choice issues, sign-convention pitfalls, and
   "is-this-an-overpromotion?" probes. Pilot dispatch:
   [`ADVERSARIAL_MIMO_2026-05-12.md`](ADVERSARIAL_MIMO_2026-05-12.md).
2. **Local Ollama (`qwen3.6:35b-a3b-q4km` and `deepseek-r1:32b`)** —
   used to re-derive small symbolic identities (Laurent expansions,
   Euler-product log expansions, primitive/imprimitive corrections)
   from scratch. Independent of any Anthropic model. Pilot dispatch:
   [`ADVERSARIAL_OLLAMA_C1_2026-05-12.md`](ADVERSARIAL_OLLAMA_C1_2026-05-12.md).
3. **MLX on M1B (Apple Silicon)** — used for any CPU/PARI batch we want
   to run with native exact rational arithmetic, separately from the
   primary mpmath workstation. Driver: `~/bin/m1b_python_runner.sh`.
   Queue: `~/Library/FareyState/M1B_QUEUE.txt`. When SSH is up, this is
   the venue for L2 PARI re-runs of `c_K`, `D_K`, `E_K log K` at
   `K ≥ 10^7`.
4. **Aristotle async dispatcher (Lean theorem prover assistant)** —
   used to police the Lean 4 scaffolds: which `sorry`s are research-open,
   which are Mathlib-prerequisites in disguise, which were
   axiomatized-and-must-not-ship-as-`axiom`. Pipeline status table
   below. We do not claim Aristotle produces theorems; we claim it
   provides an *audit* of the Lean obligations.

Acceptance rule for L3: the adversarial pass must (a) reproduce the
manuscript claim under its hypotheses, (b) identify any over-promotion
in our prose, and (c) name any objection we cannot answer in writing.
If (c) is non-empty for a load-bearing claim, the claim is *downgraded*
in the section text, not patched over.

### 2.5 Independence checks we explicitly run

* **Language independence:** mpmath (Python) vs PARI/GP (C) vs Arb
  (C/FLINT). At least two of three for every promotion-grade number.
* **Algorithmic independence:** L1 uses Muller's method for zero
  refinement; L2 uses `lfunzeros + Newton`. L1 uses direct partial
  summation; L2 uses Euler-product log expansion with primitive
  induction for `B_∞`.
* **Precision independence:** L1 at 50 dps; L2 at `≥ 200` bits in
  PARI / `≥ 250` bits in Arb. Spot-check at 100 dps for the worst
  case (`χ_{-4}/z1`).
* **Sign / branch independence:** for `log L(2ρ, ψ)`, we record the
  branch chosen by L1 and recompute by L2 starting from
  `Re(s) > 1` and analytically continuing through the corridor
  `Re(s) = 1, s ≠ 1`; check Im part modulo `2π i` is consistent.
* **Adversarial branch flip:** L3 tries the wrong branch and shows
  the resulting residual.

---

## 3. Reproducibility manifest (what we publish)

We will deliver a single self-contained reproducibility bundle. The
bundle is referenced in the paper as "Supplementary material S1".

| Item | Form | Where |
|---|---|---|
| Source code (L1) | Python scripts, mpmath ≥ 1.3, Python 3.12 | GitHub repository `Primes-Equispaced/koyama-paper-2026/`, tagged release `v1.0`. |
| Source code (L2) | PARI/GP scripts, PARI 2.15.x | Same repository, `pari/` subdir. |
| Source code (L2-spot) | Arb-via-FLINT C program, FLINT 3.x | Same repository, `arb/` subdir. |
| Refined zero data | JSON, one file per (χ, ρ) pair, with `ρ` to 100 dps and `L'(ρ, χ)`, `L''(ρ, χ)` to 60 dps | Same repository, `data/zeros/`. |
| Numerical tables | CSV with header + provenance frontmatter | `data/tables/`. |
| Convergence logs | Plain text, wall-clock + memory stamps | `logs/`. |
| Lean 4 artifacts | Lake project, lean-toolchain `leanprover/lean4:v4.28.0`, mathlib commit pinned | `lean/` subdir + GitHub `formal-conjectures/`. |
| Reproducibility manifest | YAML | `MANIFEST.yaml`, hashed. |
| Archived snapshot | Zenodo DOI | Mint at submission. |
| Audit log | The adversarial-referee transcripts (Mimo / Ollama) and the response packets | `audit/` subdir. |

`MANIFEST.yaml` skeleton:

```yaml
manifest_version: 1
title: "Saar–Koyama 2026 — reproducibility bundle"
paper_doi: TBD
zenodo_doi: TBD
git_commit: <fill at release>
lake_manifest_hash: <fill at release>
software:
  python: 3.12.x
  mpmath: ">=1.3.0"
  pari: 2.15.x
  flint: ">=3.0"
  arb: included with FLINT
  lean: leanprover/lean4:v4.28.0
  mathlib: <commit pinned>
verified_ranges:
  dirichlet_C_1_identity:
    K_values: [200000, 1000000, 2000000]
    dps: 50
  dirichlet_B_infty_identity:
    K_values: [200000, 1000000, 2000000]
    dps: 50
  dirichlet_AK_constant_D_K:
    K_values: [2000000, 10000000]
    dps: 40
  elliptic_C_1_squared_ensemble:
    K_values: [10000]
    forms: [Delta_1, 37a1, 389a1, 5077a1, 11a1-24a1 cluster, 37b1-37b2-37b3]
    dps: 30
hardware:
  primary: <fill>
  cross_check: m1b (Apple M1 Max, 32GB, macOS 26.4.1)
seeds:
  numpy: <fill>
  zero_search: deterministic (initial values from LMFDB)
  ec_smoothing_nulls: <fill from EC_KERNEL_NULL_SUITE_2026-05-11.py header>
contact: <Saar email + Koyama email>
```

---

## 4. Lean 4 formalization path

### 4.1 What we present in the manuscript

Following the current journal posture (`research-lite` survey,
2026-05-12) — *Annals / Inventiones / Duke / JAMS* do not yet treat
Lean formalization as a publication-condition; *Forum of Mathematics
Sigma* and *Experimental Mathematics* accept Lean as supporting
evidence; CPP/ITP accept `sorry`-bearing artifacts as primary papers —
our framing is:

> "We include a partial Lean 4 / Mathlib4 formalization of the
> identities and conjectures discussed in §X. The Lean artifacts
> formalize the *statements* (with explicit type signatures and
> normalization conventions) and provide proof skeletons for the
> components where Mathlib v4.28.0 already provides the needed
> primitives. Research-open obligations are marked `sorry` with an
> inline comment naming the missing Mathlib prerequisite or the
> mathematical step still open. We do not claim Lean-verified
> theorems where `sorry` remains."

This is the only honest framing given the current state of the files.

### 4.2 Lean artifact inventory (today)

| File | Object | Lean 4 status | Notes |
|---|---|---|---|
| `formal-conjectures/DirichletPolynomialAvoidance.lean` | DPAC statement | Statement formalized; main proof `sorry` | Submitted as PR #3716 to `google-deepmind/formal-conjectures` (Saar, 2026-04-11). |
| `formal-conjectures/DPAC_full.lean` | DPAC + phase-bridge tombstone | Statement formalized; `dpac_of_LI` tombstoned; phase-avoidance bridge layers named; main DPAC theorem `sorry` | Built with Lean 4.28.0 grammar (single `@[…]` block, `∈` instead of `in`). Output of Aristotle dispatch `59d181d5-b207-4882-a5ba-0786ec51d361` ingested. |
| `formal-conjectures/SmoothedDwfFormula_full.lean` | Smoothed Δw_f explicit formula, `R₀ = -2` anchor | Statement + ≥ 8 supporting lemmas; 8 `sorry`s remain | Aristotle dispatch `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` returned with errors; accepted as scaffolding. Two named Mathlib gaps: uniform Stirling decay on strips, Titchmarsh-style polynomial growth of `1/ζ`. |
| `formal-conjectures/FareyBridgeIdentity.lean` | R1: Farey bridge identity | Statement formalized; algebraic-identity-class proof scaffold | Companion to R1 dispatch `8e608890-f0ba-4a89-bbb0-a63b5bcab697`. |
| `formal-conjectures/FareySignPattern.lean` | Sign-pattern family for `B(p)` | Statement formalized; B+ Mertens-restricted refuted at `p = 237733, 243799`, so this file's *positive* theorem is no longer in scope. | Treat in paper as *negative result + classification target*. |
| `formal-conjectures/MertensSpectroscopeUniversality.lean` | Spectroscope universality candidate | Statement formalized; the strong-form universality is the conjectural target | Aligns with the C1 ensemble narrative; conditional on the Perron-leading hypothesis. |

### 4.3 Blueprint-style structure for the paper

We will adopt the Tao/Massot blueprint convention: each printed
theorem statement in §\ref{sec:numerics} gets a `Blueprint:` line
naming the Lean declaration that formalizes its *statement*, plus a
`Lean status:` line classifying it as `THEOREM` (no `sorry`),
`PROVED-UP-TO-MATHLIB-PREREQ` (one named missing lemma), `SCAFFOLD`
(skeleton only), or `OPEN` (research-open).

Example block we will print:

```
Proposition 4.3 (corrected B_∞ identity).
   T_∞(χ,ρ) = (1/2) log L(2ρ,ψ) + BPC_1 + BPC_2 + T_{≥3}.

   Blueprint: see Lean declaration  B_infty_identity
              in formal-conjectures/CorrectedBInfty.lean (to be added).
   Lean status: PROVED-UP-TO-MATHLIB-PREREQ (Dirichlet primitive-induction
                lemma needed; see Mathlib.NumberTheory.DirichletCharacter
                .Imprimitive, not yet land at v4.28.0 commit <hash>).
   Paper proof: §4 of this paper (rigorous identity).
   Numerical confirmation: Table T2; residual ≤ 3·10⁻³ at K = 2·10⁶.
```

### 4.4 Lean repo discipline before submission

1. Pin `lean-toolchain` (`leanprover/lean4:v4.28.0`) and the mathlib
   commit hash in `lake-manifest.json`. Hash recorded in the
   reproducibility manifest.
2. Every `sorry` is annotated `-- RESEARCH-OPEN: <one-line rationale>`
   or `-- MATHLIB-PREREQ: <name of missing lemma>`. No bare `sorry`s.
3. No `axiom` substitutes for missing Mathlib prerequisites. (Project
   convention; carried over from the SmoothedDwfFormula dispatch.)
4. CI: GitHub Actions runs `lake build` against the pinned mathlib
   commit. Section quotes the green badge.
5. Provide a `README_LEAN.md` per file naming: paper section, theorem
   number, blueprint URL, and the status tag.
6. Adversarial pass (L3) on the Lean repo: Aristotle dispatch surveys
   every `sorry` and classifies it.

### 4.5 What we will explicitly *not* claim about Lean

* That DPAC is Lean-proved (it isn't — `dpac_of_LI` is tombstoned).
* That the shifted Perron remainder is Lean-formalized (it isn't —
  the missing theorem is not stated in Lean either).
* That the AK constant is Lean-proved (the AK theorem is an external
  citation; we Lean-formalize only its specialization to simple
  zeros, conditional on a `Hypothesis_AK` axiom we make visible).
* That Lean acceptance equals mathematical correctness — we are
  explicit that Lean validates the *statements* and the *derivations
  we have closed*, not the *open conjectures*.

---

## 5. Numerical findings — the master ledger

### 5.1 Promotion-grade numerical claims (printed in the paper)

These are the numerical facts we are confident enough to print, with
the verification stack each requires.

**N-1. Refined zeros for the four (χ, ρ) pairs.**

| Pair | ρ (to 12 dec) | `\|L'(ρ,χ)\|` | `\|L''(ρ,χ)\|` |
|---|---|---|---|
| χ_{-4}/z1 | 0.5 + 6.020948904697 i | 1.30932 | (to be filled from `Koyama_C1.out`) |
| χ_{-4}/z2 | 0.5 + 10.243770304166 i | 1.81292 | — |
| χ_5  | 0.5 + 6.183578195450 i | 1.20003 | — |
| χ_{11} | 0.5 + 3.547041091719 i | 1.71505 | — |

Provenance: `Koyama_C1.py` (mpmath 50 dps); cross-check planned via
PARI `lfunzeros + Newton`. **Verification stack: L1 done, L2 to run,
L3 = Mimo branch-choice probe.**

**N-2. Subleading constant `C_1`.**

| Pair | `C_1 = -L''/(2 L'^2)` (mpmath, 50 dps) | `\|C_1\|` |
|---|---|---|
| χ_{-4}/z1 | 0.5203451866 + 0.01845932347 i | 0.52067 |
| χ_{-4}/z2 | 0.5150884772 + 0.05433692967 i | 0.51795 |
| χ_5       | 0.6601814622 + 0.13690196820 i | 0.67423 |
| χ_{11}    | 0.5207614712 + 0.11113668970 i | 0.53249 |

Provenance: `Koyama_C1_subleading_proof.md §7`. **Verification stack:
L1 done, L2 to run via PARI `derivnum`, L3 = Ollama symbolic
re-derivation (background pilot dispatched 2026-05-12).**

**N-3. Local Perron double-pole residue.**

Identity:

```
Res_{w=0} [ K^w / (w · L(w+ρ, χ)) ]
   = log K / L'(ρ,χ) - L''(ρ,χ) / (2 L'(ρ,χ)^2).
```

Status: `PROVED` algebraically. **Verification stack: derivation in
`Koyama_C1_subleading_proof.md §4`, L3 = Ollama symbolic check (in
flight).**

**N-4. The corrected `B_∞` identity (★).**

```
T_∞(χ, ρ)
  = (1/2) log L(2ρ, ψ) + BPC_1 + BPC_2 + T_{≥3},
B_∞(χ, ρ) = exp(T_∞).
```

Components and bad-prime cases:

| Character | conductor `q` | `χ²` | primitive `ψ` inducing `χ²` | `f` | bad primes (for `BPC_1`) |
|---|---:|---|---|---:|---|
| χ_{-4} | 4 | principal mod 4 | trivial (ζ) | 1 | p = 2 |
| χ_5 | 5 | (·/5) | (·/5) | 5 | none |
| χ_{11} | 11 | order-5 mod 11 | order-5 mod 11 | 11 | none |

Identity-residual table at `K = 2 · 10^6`, 50 dps:

| Pair | (½) log L(2ρ,ψ) | BPC_1 | BPC_2 | T_{≥3} | RHS | `T_K` at K=2·10^6 | residual |
|---|---|---|---|---|---|---|---:|
| χ_{-4}/z1 | 0.0448 − 0.2502 i | 0.1360 + 0.1711 i | −0.0051 + 0.0456 i | −0.0455 + 0.0254 i | 0.13017 − 0.00813 i | 0.12750 − 0.00715 i | 2.85·10⁻³ |
| χ_{-4}/z2 | −0.2272 − 0.3626 i | 0.0682 + 0.2252 i | 0.00050 + 0.0111 i | 0.0752 + 0.0434 i | −0.08331 − 0.08284 i | −0.08175 − 0.08341 i | 1.66·10⁻³ |
| χ_5       | −0.0148 + 0.4365 i | 0 | 0.0444 − 0.0456 i | 0.0340 − 0.0929 i | 0.06358 + 0.29804 i | 0.06362 + 0.29802 i | 4.24·10⁻⁵ |
| χ_{11}    | −0.2377 + 0.3292 i | 0 | −0.0333 + 0.0635 i | 0.0270 − 0.0315 i | −0.24404 + 0.36122 i | −0.24400 + 0.36123 i | 3.33·10⁻⁵ |

Convergence rates at `K ∈ {2·10⁵, 10⁶, 2·10⁶}` show `≈ K^{-1/2}/log K`
decay for `χ_5, χ_{11}` (no bad primes; pure conditional-tail
convergence of `Σ_p χ²(p)/p^{1+iτ}`), and a uniformly slower decay for
`χ_{-4}` traced to the `p = 2` bad-prime weight.

Provenance: `Koyama_B_infty_proof.md §7`. **Status: `PROVED`
unconditional identity (no RH/DRH/EDRH); confidence 0.96 aggregated.
Verification stack: L1 done, L2 PARI re-implementation to run, L3 =
Mimo branch-choice probe (in flight) + Ollama bad-prime symbolic
re-derivation.**

**N-5. AK-constant Dirichlet drift `K = 2·10⁶ → 10⁷`.**

| Quantity | K = 2·10⁶ | K = 10⁷ | Limit if NDC = 1/ζ(2) | Limit if NDC = e^{-γ} |
|---|---:|---:|---:|---:|
| Mean `\|D_K\| · ζ(2)` over four pairs | 0.992 | 0.974 | 1.000 | ≈ 0.911 (= ζ(2)·e^{-γ}) |
| Mean `\|E_K log K · e^γ / L'\|` | — | 0.942 | — | 1.000 |

The drift from 0.992 to 0.974 is *consistent* with the AK normalization
(`e^{-γ}`) and inconsistent with the `1/ζ(2)` target at the
`(log K)^{-1}` scale, but does not by itself *prove* the AK
normalization. **Status: `NUMERICAL` evidence for the constant
correction; the AK normalization itself is `CONDITIONAL` on Aoki–Koyama
2023 (1.4). Verification stack: L1 done at K = 10⁷, L2 PARI
re-implementation to schedule on M1B (queue), L3 = Mimo branch / sign
probe.**

**N-6. Spectroscope ensemble `E[C_1²]` (Δ + EC + rank-0 cluster).**

| Form | Rank | Weight | Conductor | Sample | `E[C_1²]` | Status |
|---|---:|---:|---:|---:|---:|---|
| Δ level 1 | n/a | 12 | 1 | 683 zeros | 0.950231842 | confirmed anchor |
| 37a1 | 1 | 2 | 37 | 500 zeros | 2.189911545 | confirmed |
| 389a1 | 2 | 2 | 389 | 500 zeros | 3.113923728 | confirmed |
| 5077a1 | 3 | 2 | 5077 | 500 zeros | 4.617 | confirmed rank-3 anchor |
| 11a1–24a1 rank-0 cluster | 0 | 2 | 11–24 | 200 each | mean 1.886, CV 8.9% | confirmed |
| 37b1/37b2/37b3 | 0 | 2 | 37 | 200 each | mean 2.052 | conductor-control |

Provenance: `L2_facts/farey-current-state.md`,
`koyama-shared/data/` and `koyama-shared/results/`.
**Status: `NUMERICAL`. Verification stack: L1 done (post `μ_f(p²)`
bug-fix at 2026-04-20); L2 to run via PARI `ellap`-based independent
re-implementation; L3 = Mimo / Ollama review of the
arithmetic-vs-analytic normalization (this was the bug class).**

**N-7. W2 empirical model (22 weight-2 EC points).**

```
E[C_1²] = 0.4785 - 0.1668 · rank + 0.4727 · log N,  R² = 0.81.
```

`log N` is significant; the rank coefficient is *not stable* under
leave-one-out resampling. We will print the regression with HC3
standard errors and report leave-one-out and bootstrap ranges for the
rank coefficient — explicitly framed as a *conductor-confounded
trend*, not a rank law.
**Status: `NUMERICAL with explicit conductor confounding`.
Verification stack: L1 (NumPy/statsmodels), L2 (R `lm`), L3 = Mimo
"could the rank effect be entirely absorbed by `log N` after
appropriate non-linear corrections?" probe.**

**N-8. EC NDC sweep through `K = 10⁶`.**

| Family | Tested form of NDC universality | Verdict |
|---|---|---|
| Three-curve grid, sharp cutoff | `D_K^E · ζ(2) → 1` | `FALSIFIED` (per-curve constants do not match 1; `Koyama_EC_NDC_extended_sweep_2026-05-11.md`). |
| Smoothed proxy with `c_E,W(K) · P_E,W(K)` | reproducible finite signal | *Demoted* by null-control gate (`cP_only`, `P_only`, `PL2_only` pass at α=0.75; `EC_NULL_CONTROL_GATES_2026-05-11.md`). |
| Full Sato-Tate G3 run | empirical-p gate | `G3_FAIL`: `iid p_ratio = 0.062378…`, shared `p_score = 0.046512…` — fail empirical p gates. |
| Holdout curves / denser K | not yet run | open |

**Status: print the negative result honestly. Verification stack: L1
done; L2 PARI re-run pending; L3 = Mimo "is there a normalization in
which the sharp-cutoff form survives?" — the answer per
`Koyama_EC_NDC_normalization_no_go_2026-05-11.md` is *no* for the
tested finite class.**

### 5.2 Expansion — new numerical work to run BEFORE submission

This is where we begin to *expand* findings as the user asked. None of
these expansions are required for the section to be honest; they
strengthen the empirical case and serve as L2 cross-checks.

| Expansion | What | Cost | Verifies which printed claim |
|---|---|---|---|
| **E-1.** Push `D_K` to `K = 10⁸` for the four Dirichlet pairs in PARI/GP on M1B; track the `K^{-1/log log K}` drift to confirm the AK normalization. | PARI partial sum + Euler product, M1B batch | ~24 core-hours | N-5 (independent L2). |
| **E-2.** Push `B_∞` identity residual to `K = 10⁷` for `χ_5, χ_{11}` (no bad primes — clean conditional-convergence regime) and confirm `K^{-1/2}` decay slope to two decimals. | mpmath single-host | ~6 core-hours | N-4. |
| **E-3.** Independently re-implement `BPC_1` for `χ_{-4}` in PARI/GP using the imprimitive-`χ²` formula and check the bad-prime contribution at `p = 2` to 30 decimals. | PARI symbolic | <1 hour | N-4 (load-bearing for `χ_{-4}`). |
| **E-4.** Add a fifth Dirichlet character pair (e.g., `χ_7`, two-zero pair) to widen the verification base. | mpmath + PARI | ~6 core-hours | N-1, N-2, N-4, N-5. |
| **E-5.** Compute `E[C_1²]` for one rank-4 and one rank-5 curve (e.g., 234446a1, 19047170a1) to extend the spectroscope ensemble — *labelled exploratory*, not promotion-grade. | mpmath, single host | ~12 core-hours | N-6. |
| **E-6.** Run the EC NDC sweep on three *holdout* curves not used in the original gate to test whether the smoothed proxy is a real signal or curve-fit artifact. | mpmath, single host | ~10 core-hours | N-8. |
| **E-7.** Lean repo CI green build with the pinned mathlib commit, plus an Aristotle audit of every `sorry`. | Lake + GitHub Actions + Aristotle dispatch | ~2 days | §4 of paper. |
| **E-8.** Recompute `C_1` and `c_K - log K/L' - C_1` at `K = 2·10⁶` in Arb at 250 bits as a third-language cross-check. | Arb single-host | ~2 hours | N-2, N-3. |

Each expansion ends with a single decision: *adds to manuscript* or
*goes to supplementary*.

### 5.3 Negative findings we will report (transparency requirement)

* B+ Mertens-restricted positivity is *false* in the Lean-canonical
  `crossTerm` definition. Counterexamples: `B(237733) = -3.02·10¹⁰`,
  `B(243799) < 0`. (Source: `handoff-2026-05-09-followup/B_plus_direct_counterexamples.md`.)
* `(MERTENS-LB)` and `(MERTENS-LB-MR)` are *both false*; fixed
  `K₀ ≤ 100` global negative-tail envelopes are falsified on the `10⁹`
  log grid.
* Direct Li–Zaharescu / mollifier transfer for the H1 fixed-curve
  positive-rank closure is `NO_GO` (see `handoff-2026-05-11-h1-breakthrough-proof-wave/`).
* The Sym²/⟨f,f⟩ proportionality in its raw form is *falsified* (see
  `results/sym2_collapse_analysis.md`); we *do not* dismiss the
  possibility of an archimedean-corrected normalization but it is not
  in scope here.

---

## 6. Open challenges (Koyama: "should be the core of our paper")

Each of these is stated honestly in the paper. Each has a Lean
status entry.

| # | Open challenge | Status | What would close it | Lean status |
|---|---|---|---|---|
| **O-1** | Shifted Perron leading theorem: `c_K = log K/L'(ρ) + o(log K)` unconditionally for any simple noncentral zero ρ. | `DEFER` | A proved off-target-zero residue control: either (a) all crossed off-target zeros simple, plus `Z_simple(K, T_K) = o(log K)`, plus shifted-rectangle/truncation = `o(log K)`, *or* (b) a multiple-zero aggregate bound `(log K)^{m-1}` term cancels in aggregate. | Not Lean-formalized (statement only). |
| **O-2** | Aoki–Koyama (1.4) used as a black-box external citation. | `EXTERNAL` | Verify the verbatim quote on p. 235 of AK 2023 (J. Number Theory 245) is embedded as a footnote with PDF page check. | The hypothesis is named as `Hypothesis_AK` in our Lean scaffold. |
| **O-3** | GL(2) fixed-curve reciprocal-derivative control at off-central zeros (the EC analogue of the AK statement). | `LITERATURE_BLOCKED` | A bound on `\|1/L'(ρ, E)\|` averaged over the relevant zeros, or a minimum-modulus estimate for `L(E, s)` with explicit exponent. | Not Lean-formalized. |
| **O-4** | Conductor confounding in the EC ensemble. | `OPEN, EMPIRICAL` | A controlled experiment varying rank at fixed `log N`, with rank-3 and rank-4 anchors at *matched* conductor — currently the rank/conductor design is collinear in the 22-point set. | Not in scope. |
| **O-5** | Smoothed EC NDC after null-control failure. | `OPEN, EMPIRICAL` | Replace the failed three-curve smoothstep gate with kernel-suite + stochastic null + rank/curve permutation + holdout + denser-K — pre-declared and survival-tested. | Not in scope. |
| **O-6** | DPAC pointwise theorem at ζ ordinates. | `RESEARCH-OPEN` | The phase-bridge layer named in `DPAC_full.lean` (the LI-to-DPAC route is tombstoned). | Lean statement present; main result `sorry`. |

The honest framing in the paper is: *these are the live obstructions
between the corrected `B_∞` identity / local residue (which we prove)
and the full conjectured NDC universality (which remains open). We
state each obstruction precisely so that future work has an exact
target.*

---

## 7. Honesty audit and "verified at 10^{13}" reconciliation

The audit from `KOYAMA_CLAIM_AUDIT_2026-05-11.md` flags several
recurring failure modes. The plan applies them as preflight checks:

| Failure mode | Mitigation in this section |
|---|---|
| DPAC theorem language outruns verification status. | We call DPAC a *formalization/conjectural target* and never write "DPAC is proved". |
| External citations not embedded. | Every external theorem (Aoki–Koyama 2023, Akatsuka 2013, Inoue 2021, Soundararajan 2009, Montgomery–Vaughan Thm 9.4, Hadamard–de la Vallée Poussin) is cited with page/equation and embedded as a verbatim footnote/appendix quote. |
| `L2E^rank` over-naming. | Use `L2E_partial^rank` (finite sharp-cutoff good-prime Euler-product proxy) — *not* completed `L(E, 2)`. |
| Status labels inconsistent. | Each printed identity has one of `PROVED`, `PROVED-UP-TO-MATHLIB-PREREQ`, `CONDITIONAL`, `NUMERICAL`, `FALSIFIED`, `DEFER`. Status is in the statement, not buried in prose. |
| Citation count drift. | Reconcile to exact count before submission; do not print a count we have not just re-counted. |
| "Verified at 10^{13}" inheritance. | **Action:** ask Koyama, in the reply, which numerical experiment he means by "10^{13}" — we have no internal record of a verified `K = 10^{13}` computation. Until clarified, restrict printed verified scales to `K = 10^7` (Dirichlet) and `K = 10^6` (EC). |

---

## 8. Adversarial / independent verification protocol — execution plan

### 8.1 Lanes (all local — m1b is this device)

The plan was originally written with m1b as a remote SSH target. m1b
is in fact **this device** (`zas-MacBook-Pro.local`, Apple M1 Max,
32 GB, macOS 26.4.1). All lanes run locally.

| Lane | Stack | Role |
|---|---|---|
| **L1 primary** | `mpmath` 1.4 / Python 3.9 in `~/farey_offline_venv`, 50 dps; Python 3.13 via `~/.local/bin/python3.13` for heavier scripts | Main numerical evidence. |
| **L2-PARI** | PARI/GP 2.15.x, local | Independent re-implementation in a different language. |
| **L2-Arb** | Arb / FLINT 3.x, local C program | Third-language spot-check for the worst case (`χ_{-4}/z1`). |
| **L3-Mimo** | `mimo-v2.5-pro` via `scripts/dispatch_mimo.sh` (API) | Adversarial referee on prose claims, branch-choice issues, sign pitfalls. Pilot dispatched 2026-05-12; output → [`ADVERSARIAL_MIMO_2026-05-12.md`](ADVERSARIAL_MIMO_2026-05-12.md). |
| **L3-Ollama** | local: `qwen3.6:35b-a3b-q4km`, `deepseek-r1:32b`, `gemma4:26b`, `phi4:14b`, `qwen3:8b` | Independent symbolic re-derivation of small load-bearing identities (Laurent expansions, log-Euler-product, primitive induction). Smoke-test ✓ (`23 · 47 = 1081`). Pilot dispatched 2026-05-12; output → [`ADVERSARIAL_OLLAMA_C1_2026-05-12.md`](ADVERSARIAL_OLLAMA_C1_2026-05-12.md). |
| **L3-MLX** | `~/venvs/gemma4-mtp/bin/python` (mlx + mlx_lm). HF cache holds `mlx-community/DeepSeek-R1-Distill-Llama-70B-4bit`, `Qwen3-Next-80B-A3B-Thinking-4bit`, `Qwen2.5-1.5B-Instruct-4bit`, `gemma-4-E2B/E4B-it-{,assistant-}bf16`. Smoke-test ✓ (Qwen2.5-1.5B loaded and generated 80 tokens). | Independent symbolic re-derivation on a non-Ollama runtime; useful when we want to cross-check the Ollama answer with a different model family on the same hardware. |
| **L3-Aristotle** | Aristotle async dispatcher (API) | Lean obligation audit on every `sorry`. Project IDs already in flight: `424973ae-…SmoothedDwfFormula`, `8e608890-…R1_B_plus`, `59d181d5-…DPAC` (all `COMPLETE_WITH_ERRORS` — read as scaffold tagging). |
| **L4 human** | Adversarial reviewer with no authorship incentive, before submission | Final pass. |

### 8.2 Acceptance criteria

A printed claim moves to *promotion-grade* only when:

1. L1 ✓ and L2 ✓ agree to the precision required (per §2.2);
2. L3 has produced at least one written adversarial objection and a
   written response that resolves it; if unresolved, the claim is
   downgraded;
3. The Lean status tag is consistent with the printed claim (no
   `THEOREM` tag with active `sorry` in scope);
4. Every external citation is PDF-verified, page/equation captured,
   verbatim quote embedded.

### 8.3 Pilot dispatch status (completed 2026-05-12)

| Dispatch | Lane | Object | Status |
|---|---|---|---|
| Mimo `mimo-v2.5-pro` adversarial-referee on the four headline claims | L3-Mimo | Branch/sign/over-promotion probe across B_∞, C_1, AK, NDC | ✓ **COMPLETED.** Returned 6 numbered objections. See [`ADVERSARIAL_MIMO_2026-05-12.md`](ADVERSARIAL_MIMO_2026-05-12.md) for the raw output and [`ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md`](ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md) for the authors' point-by-point response. No fatal objection survives; presentation/wording actions captured. |
| Ollama `qwen3.6:35b-a3b-q4km` symbolic Laurent check | L3-Ollama | Re-derives `Res_{w=0} K^w / (w · L(w+ρ,χ))` for simple zero | ✓ **COMPLETED — INDEPENDENTLY CONFIRMED.** The local model produces the same residue formula `log K / L'(ρ,χ) − L''(ρ,χ)/(2 L'(ρ,χ)²)` from scratch. Lane operational. |
| PARI L2 re-run of `c_K` and `D_K` at `K = 10^7` for χ_{-4} pairs | L2-PARI | Independent Mobius/Euler-product summation | To run locally — m1b is this device. |
| Arb L2-spot at `K = 2·10^6` for χ_{-4}/z1 | L2-Arb | 250-bit independent residual | To dispatch after PARI sanity. |
| Aristotle dispatch survey of `sorry`s | L3-Aristotle | Audit of `DPAC_full.lean`, `SmoothedDwfFormula_full.lean`, `R1_B_plus`, `FareyBridgeIdentity.lean` | Polled via `./scripts/poll_aristotle.sh`. |

**Headline pilot finding (Mimo, O3):** the adversarial pass tried to
reduce the `e^{-γ}` vs `1/ζ(2)` discrepancy to a "normalization swap"
and was correctly defeated by the embedded Aoki–Koyama (1.4) quote and
the `K = 10^7` drift. This is exactly the kind of objection the
adversarial lane is designed to catch — the section must keep the
verbatim AK (1.4) quote in the text, not buried in references.

**Headline pilot finding (Mimo, O4):** the "DEFER" label on the shifted
Perron leading theorem reads as an impossibility claim to a careful
reader. Section will use "open challenge, not impossibility" wording,
matching Koyama's request to frame these as core open challenges.

### 8.4 Local execution (m1b is this device)

The plan was originally written assuming m1b was a remote machine.
It is in fact the host we are running on (`hostname:
zas-MacBook-Pro.local`, Apple M1 Max, 32 GB). No SSH layer is
involved. The `~/Library/FareyState/` queue directory and
`~/bin/m1b_python_runner.sh` driver, where present, are local
artifacts of a prior architecture that imagined m1b as remote.

Local runtime fixtures verified 2026-05-12:

- `mpmath` 1.4.1 available in `~/farey_offline_venv` (Python 3.9).
- `ollama list` returns five models (`qwen3.6:35b-a3b-q4km`,
  `deepseek-r1:32b`, `gemma4:26b`, `phi4:14b`, `qwen3:8b`); smoke
  test `23 · 47 = 1081` returned correctly via `qwen3:8b`.
- `mlx` / `mlx_lm` available in `~/venvs/gemma4-mtp/` (Python 3.13);
  smoke test loaded `mlx-community/Qwen2.5-1.5B-Instruct-4bit` from
  the HuggingFace cache at `~/.cache/huggingface/hub/` and generated
  output.
- HF cache holds in addition: `DeepSeek-R1-Distill-Llama-70B-4bit`,
  `Qwen3-Next-80B-A3B-Thinking-4bit`, `gemma-4-E2B/E4B-it-bf16`.
- PARI/GP and Arb are available on the host (see L2-PARI / L2-Arb
  lanes).

---

## 9. Working timeline (internal — no external commitments)

| Date | Milestone |
|---|---|
| 2026-05-12 | This plan written; pilot adversarial dispatches in flight; claim posture frozen. |
| +1 day | Mimo + Ollama pilot outputs reviewed; section §1–§2 first draft written from this plan. |
| +2 days | Repair M1B; PARI L2 lane scheduled for `c_K, D_K` at `K = 10^7`. |
| +3 days | Arb L2-spot at `K = 2·10^6`; Lean repo CI on the pinned mathlib commit. |
| +5 days | Aristotle obligation audit on `DPAC_full.lean`, `SmoothedDwfFormula_full.lean`, `R1_B_plus`. |
| +7 days | Draft of §3–§7 of the section (numerical findings + open challenges) reviewed against the audit checklist; expansions E-1, E-2, E-3 scheduled. |
| +10 days | Section draft circulated internally; awaiting Koyama's table-discrepancy reconciliation (he expects to do this *after* the Kiban-S deadline 2026-05-20). |
| Post 2026-05-20 | Reconcile Koyama's tables; re-run any affected verification; finalize. |

Nothing in this timeline is communicated externally without explicit
user approval.

---

## 10. Decisions deferred — out of scope for this plan

Journal target and author order are intentionally *not* decided here.
The draft will be journal-agnostic and will use a placeholder
authorship block. Those choices are for the user, separately, after
the draft has been read.

The Lean repository attachment status (peer-reviewable artifact vs.
supporting-code URL) is also left to the user.

---

## 11. Status after the 2026-05-12 plan→draft transition

The plan above is the deliberation artifact. The actual draft of the
Technical/Computational section is in
[`SECTION_DRAFT_2026-05-12.md`](SECTION_DRAFT_2026-05-12.md).

Execution chronology, 2026-05-12:

- [x] Claim posture in §0 frozen.
- [x] `10^{13}` scope audit completed and adopted
      ([`SCOPE_AUDIT_10E13_2026-05-12.md`](SCOPE_AUDIT_10E13_2026-05-12.md)).
      The `10^{13}` evidence is the Phase-1 Dominance-of-`−1`
      residue-count replication (`π(1.3·10^{13}) = 445{,}831{,}610{,}611`);
      no analytic claim is at $K = 10^{13}$. Draft separates the two
      scales in distinct subsections.
- [x] Mimo and Ollama component-identity pilot outputs ingested
      ([`ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md`](ADVERSARIAL_AUDIT_RESPONSE_2026-05-12.md)).
- [x] m1b confirmed as the local device (`hostname:
      zas-MacBook-Pro.local`, Apple M1 Max). Plan §8 rewrote the
      lane table to remove the SSH layer.
- [x] **Ollama** operational locally; smoke test
      `qwen3:8b → 23 · 47 = 1081` ✓. Five models available
      (`qwen3.6:35b-a3b-q4km`, `deepseek-r1:32b`, `gemma4:26b`,
      `phi4:14b`, `qwen3:8b`).
- [x] **MLX** operational locally via `~/venvs/gemma4-mtp/bin/python`;
      smoke test loaded `Qwen2.5-1.5B-Instruct-4bit` ✓. Five MLX
      models cached including `Qwen3-Next-80B-A3B-Thinking-4bit` and
      `DeepSeek-R1-Distill-Llama-70B-4bit`.
- [x] **Lean-memo additions to the draft** (v0.2): `c_W = -γ_E - E_1(1)`
      kernel-constant theorem and Petersson family-average boundary
      formalization added to §X.6 inventory.
- [x] **Two-scales framing** added to §X opening + §X.5 head with
      explicit no-cross-extrapolation guarantee.
- [x] **§X.5.2 table filled** with $L''(\rho, \chi)$ values from
      `Koyama_C1.out` (`dps = 50`).
- [x] **L1b in-language cross-check executed**
      ([`mpmath_L2_crosscheck.py`](mpmath_L2_crosscheck.py); output
      [`L2_CROSSCHECK_2026-05-12.md`](L2_CROSSCHECK_2026-05-12.md)):
      $|\Delta L'|, |\Delta L''| \le 6\cdot 10^{-12}$;
      $|\Delta C_1| \le 5\cdot 10^{-13}$;
      $|R(K)|$ matches L1 reference to all six reported digits at
      $K = 200{,}000$ on all four pairs.
- [x] **L3 adversarial pass against the draft** executed: Mimo
      ([`ADVERSARIAL_MIMO_DRAFT_2026-05-12.md`](ADVERSARIAL_MIMO_DRAFT_2026-05-12.md)),
      Ollama ([`ADVERSARIAL_OLLAMA_DRAFT_2026-05-12.md`](ADVERSARIAL_OLLAMA_DRAFT_2026-05-12.md)),
      MLX ([`ADVERSARIAL_MLX_DRAFT_2026-05-12.md`](ADVERSARIAL_MLX_DRAFT_2026-05-12.md)).
      Mimo returned 10 objections (1 fatal, 4 serious, 5 cosmetic);
      Ollama confirmed all load-bearing algebra it checked;
      MLX (1.5B model) was insufficient and is recorded as a
      calibration point.
- [x] **All 10 Mimo objections addressed in draft v0.3**
      ([`ADVERSARIAL_AUDIT_RESPONSE_DRAFT_2026-05-12.md`](ADVERSARIAL_AUDIT_RESPONSE_DRAFT_2026-05-12.md)):
      L2 lane honestly relabeled L1b vs L2; Lean tags downgraded to
      PLANNED where files do not exist; AK specialization paragraph
      added; (SP-L) failure mechanism stated; $|D_K|$ vs $D_K$
      modulus-only caveat added; EC NDC sweep rewritten as negative
      result; L3 independence claim relaxed to stack-independence +
      adversarial framing; §X opening two-scales separation
      tightened; Akatsuka 2013 unconditional status stated
      explicitly; Q:L2-PARI added to §X.7.
- [x] Journal target and author order left to the user, not decided.
- [x] No outbound email or commit to a public remote is sent without
      explicit user approval.

Open items for the next iteration (recorded in
`SECTION_DRAFT_2026-05-12.md` §TODO): Lean files for Lemma X.3.1
and Theorem X.4.1; Aristotle audit of `sorry`s; L3 re-run after
v0.4 edits with a larger MLX model; optional push of cross-language
$D_K$ verification from $K = 200{,}000$ to $K = 10^7$ in PARI.

**Update — 2026-05-12 v0.4: cross-language L2 lane executed.** PARI/GP
2.17.3 and Arb (via python-flint 0.8.0) were installed via conda-forge
into `~/miniforge3/envs/pari-arb`. PARI L2
([`pari_L2_crosscheck.gp`](pari_L2_crosscheck.gp) →
[`L2_PARI_CROSSCHECK_2026-05-12.md`](L2_PARI_CROSSCHECK_2026-05-12.md))
agrees with L1 to $\ge 11$ decimal digits on $L'$, $L''$, $C_1$ and to
all 6 reported digits on $|R(K)|$ at $K = 200{,}000$ on every pair.
Arb 250-bit spot check ([`arb_L2_spot.py`](arb_L2_spot.py) →
[`ARB_L2_SPOT_2026-05-12.md`](ARB_L2_SPOT_2026-05-12.md)) agrees with
the PARI L2 reference at interval width $\le 3 \cdot 10^{-43}$. Mimo
objection M1 (Fatal) is fully resolved. The §X.2 lane table now reads
all of L1 / L1b / L2 / L3 as **executed**.
