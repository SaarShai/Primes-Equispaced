# P3a / G1 — Δ-Machine Compositio Paper Bundle (~50pp Synthesis)

**Target model:** Opus 4.7, **extra-high** reasoning mode. Fallback (if rate-limited): MIMO `thinking:disabled`, then OpenRouter Claude Opus.
**Repo root context:** `/Users/za/Documents/Farey NOW/primes-equispaced/` (this repo).
**Deliverable file:** `paper/Delta_machine_paper_compositio_draft.md` (publication-grade Markdown, LaTeX-ready)

---

## Goal (single sentence)

Stitch the existing Δ-machine source materials into a single coherent ~50-page Compositio-tier paper draft, internally consistent, with theorems numbered 2.1–2.7 + extension theorems + multi-L convolution + applications §6 + computational toolkit appendix, every theorem either provable from cited references or stated explicitly as a conjecture-with-evidence. **No fabrication, no overclaim, no theorem stated as theorem unless proof or citation is in hand.**

---

## Context: why now

Per [`delta-machine-roadmap.md`](../handoff-2026-05-04-theorem-B-and-C1/delta-machine-roadmap.md):
- **G1 confidence: 0.80**. The Δ-machine framework is mature (master theorem + 4 closed extensions + multi-L). The Compositio bundle source `Delta_machine_paper_bundle.md` is already 5484 words. The remaining work is synthesis, internal consistency, citation verbatim verification, and §6 applications expansion.
- **Independent of Theorem B's GDC wall** — this paper ships regardless of P1/P2 verdicts.
- **Estimated wall-clock 3–6 weeks** for first complete draft.

---

## Mandatory protocol (read before starting; embedded in deliverable)

1. **NO fabrication.** Every cited theorem must be verified by `curl + pdftotext` on actual paper, with verbatim quote + page or equation number. If a citation cannot be verified, mark the theorem `UNVERIFIED` and either remove it or downgrade to conjecture-with-evidence.
2. **Single confidence aggregation rule** stated at start of deliverable, never switched mid-document. For paper-grade: only theorems with confidence ≥ 0.95 are stated as theorems. 0.80–0.95 are stated as propositions or conjectures-with-strong-evidence. <0.80 are open conjectures or omitted.
3. **Honest verdict per section.** If a theorem in a source file is over-claimed, demote it. If a section relies on a fabricated citation, flag and either fix the citation or cut the section.
4. **Cross-reference prior failures and demotions:**
   - [`SESSION_SYNTHESIS_extra_high_round.md`](../handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) — 5-of-5 inflation pattern; you must NOT repeat
   - [`G7_CS_2007_verification.md`](../handoff-2026-05-04-theorem-B-and-C1/G7_CS_2007_verification.md) — CS 2007 §7 was unitary not orthogonal
   - [`SY_Li_citation_corrections.md`](../handoff-2026-05-04-theorem-B-and-C1/SY_Li_citation_corrections.md) — S-Y/Li conditional vs unconditional fixes
   - [`IK_5_36_CITATION_PATCH.md`](../handoff-2026-05-04-theorem-B-and-C1/IK_5_36_CITATION_PATCH.md) — IK Theorem 5.36 wrong chapter
   - [`PARI_LFUNSYMPOW_NORMALIZATION.md`](../handoff-2026-05-04-theorem-B-and-C1/PARI_LFUNSYMPOW_NORMALIZATION.md) — `lfunsympow` normalization audit
5. **Don't cite from memory.** Every theorem statement quoted verbatim from a downloaded PDF, no paraphrase.

---

## Inputs and references

### Source files to synthesize (ALL in the bundle)

- [`Delta_machine_paper_bundle.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_machine_paper_bundle.md) — 5484-word existing draft, the **base** for the synthesis
- [`Delta_arithmetic_generalization.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_arithmetic_generalization.md) — master theorem + §6 Applications
- [`Delta_machine_extended.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_machine_extended.md) — 4 closed extension theorems
- [`Delta_machine_multi_L.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_machine_multi_L.md) — Cross-Selberg via Macdonald-Cauchy → plus-tensor Rankin-Selberg
- [`Delta_machine_higher_rank.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_machine_higher_rank.md)
- [`Delta_machine_open_problems.md`](../handoff-2026-05-04-theorem-B-and-C1/Delta_machine_open_problems.md) — open problems for §7
- [`Smoothed_Dwf_explicit_formula_VERIFIED.md`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_explicit_formula_VERIFIED.md) — `R₀ = −2` derivation, Smoothed Δw_f
- [`Smoothed_Dwf_publishable.md`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_publishable.md) — 604-line publishable manuscript section
- [`MK3_Bridge_Selberg_VERIFIED.md`](../handoff-2026-05-04-theorem-B-and-C1/MK3_Bridge_Selberg_VERIFIED.md) — universal Selberg-class kernel
- [`Higher_order_polylog_conjecture.md`](../handoff-2026-05-04-theorem-B-and-C1/Higher_order_polylog_conjecture.md) — `|S^{(k)}_ζ(N) − R₀^{(k)}| = O((log N)^{k−1})`
- [`T6_Delta_machine_bibliography.md`](../handoff-2026-05-04-theorem-B-and-C1/T6_Delta_machine_bibliography.md) — bibliography seed
- [`T9_Delta_open_problems_5plus.md`](../handoff-2026-05-04-theorem-B-and-C1/T9_Delta_open_problems_5plus.md)
- [`T10_bundle_LOG.md`](../handoff-2026-05-04-theorem-B-and-C1/T10_bundle_LOG.md) — provenance map + gap list. Read first to know what's already audited.

### Numerical evidence files (for §5 Numerical Evidence)

- [`Smoothed_Dwf_numerical.gp`](../handoff-2026-05-04-theorem-B-and-C1/Smoothed_Dwf_numerical.gp), `.out` — 8-digit at N=10⁵
- [`zeta_prime_calibration.gp`](../handoff-2026-05-04-theorem-B-and-C1/zeta_prime_calibration.gp), `.out` — ζ' baseline T=100..10000
- [`family_avg_finite_T_fix.gp`](../handoff-2026-05-04-theorem-B-and-C1/family_avg_finite_T_fix.gp), `.out` — 14-curve T=400, 1000

### Lean files for §8 Formalization

- [`SmoothedDwfFormula.lean`](../handoff-2026-05-04-theorem-B-and-C1/SmoothedDwfFormula.lean) — `R0_value : R0 = -2 := rfl` + existence axiom
- [`DeltaMachineMaster.lean`](../handoff-2026-05-04-theorem-B-and-C1/DeltaMachineMaster.lean) — master theorem (algebraic backbone)
- [`BridgeIdentityStatement.lean`](../handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean) — Bridge identity statement

### Source papers to retrieve and verbatim-cite

You MUST retrieve and `pdftotext` these before citing anything from them:

- Selberg 1989/1992 — *Old and new conjectures and results about a class of Dirichlet series* (Selberg class axioms S1–S5). Cite via Collected Works Vol II.
- Bruggeman 1983 — *Fourier coefficients of cusp forms*, Lecture Notes in Math. 865. (For verifying claimed novelty of Synthesis Identity (E) — though that lives in C1 handoff, not Δ-machine.)
- Iwaniec 2002 — *Spectral methods of automorphic forms*, GSM 53.
- Murty-Murty 2009 — *Problems in Analytic Number Theory*, Birkhäuser. **Critical for novelty audit** per [`THEOREM_B_HANDOFF.md`](../handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md) §11.3.
- Kaczorowski-Perelli 1999/2010 — Selberg class structure papers
- Hughes-Mezzadri 2008 — Barnes-G `1/12` orthogonal coefficient (also in P1b reference set)
- Conrey-Snaith 2007 — *Applications of the L-functions ratios conjectures*, `arXiv:math/0610495`
- Liu-Wang-Ye 2005 — orthogonality of Hecke eigenvalues

---

## Plan (step-by-step)

### Step 1 — read all source files in the bundle

Build a one-page map: theorem → source file → claimed confidence. Identify duplicated or contradictory statements between sources.

### Step 2 — citation audit pass 1

For every external citation in the source files, attempt to retrieve the cited paper. For each citation:
- Found and verified verbatim → green
- Found, but verbatim disagrees with how source files cite it → red, fix
- Cannot retrieve → yellow, downgrade dependent theorem to "pending citation verification"

This is the most important pass. Per `SESSION_SYNTHESIS_extra_high_round.md`, this is where the prior round failed.

### Step 3 — outline the paper

Standard Compositio shape:

1. **Introduction** — motivation, statement of master theorem, road map
2. **Notation and Selberg class axioms** — S1–S5 verbatim from Selberg 1989/1992
3. **Master theorem** (Theorems 2.1–2.7) — Δ-arithmetic generalization
4. **Extension theorems** — higher-order Δ^k, cross-Selberg, functoriality, inverse direction
5. **Numerical evidence** — ζ, Dirichlet, Δ, EC at 10–32 digits
6. **Applications (§6)** — Mertens Ω, Sato-Tate uniform-k, μ⋆μ variants, others from `T9_Delta_open_problems_5plus.md`
7. **Open problems** — Higher-order polylog conjecture, GL(3) sym² extension
8. **Lean formalization** — `SmoothedDwfFormula`, `DeltaMachineMaster` status
9. **Computational toolkit appendix** — `deltamachine` Sage/SymPy package outline (pulls from G5; if package not yet built, describe API)
10. **Bibliography** — every cite verbatim-verified

### Step 4 — write each section, draft 1

For each section, draft 1:
- State theorems verbatim
- Quote sources verbatim with page/equation numbers
- Tabulate numerical evidence with explicit N, dps, residual, sample size
- Mark every confidence: theorem (≥0.95), proposition (0.85–0.95), conjecture-with-evidence (0.65–0.85), open conjecture (<0.65)

### Step 5 — internal consistency pass

Cross-section checks:
- Same notation used everywhere
- Same theorem numbering everywhere
- Conventions for Mellin transform, contour, family parameters consistent across §3, §4, §5

### Step 6 — adversarial reviewer pass

Review your own draft as if you are a Compositio referee. For every claim, ask: "would this be caught by a referee?" Mark red flags. Either fix or downgrade.

Particular targets per `T10_bundle_LOG.md` and `SESSION_SYNTHESIS_extra_high_round.md`:
- Macdonald-Cauchy → plus-tensor Rankin-Selberg identification — confirmed novel against Murty-Murty 2009?
- `1/L` polynomial growth on zero-free strips — UNCONDITIONAL for ζ, Dirichlet, GL(2) per IK Thm 5.20–5.23 — verify exact theorem numbers
- Liu-Wang-Ye 2005 orthogonality — verify (already in `MK3_Bridge_Selberg_VERIFIED.md` numerical: `Σ λ_Δ(p)/p = 0.152` for p≤5000)

### Step 7 — final pass: LaTeX-ready Markdown

Output Markdown that converts cleanly to LaTeX:
- Math mode `$...$` and `$$...$$`
- Theorem environments via Markdown blockquotes with `**Theorem 2.X.**` headers
- Citations as `[Author Year, Thm X.Y]` in text, with full bibliography at end

---

## Deliverable specification

Single Markdown file at `paper/Delta_machine_paper_compositio_draft.md` of length ≥ 40 pages (rough estimate at 12pt: ≥ 30,000 words), with:

1. **Confidence aggregation rule** — stated once at top, applied everywhere
2. Sections 1–9 (intro through computational toolkit appendix) per the outline in Step 3
3. **Citation audit log** — companion file `paper/Delta_machine_paper_citation_audit.md` listing every external citation in the draft, with PDF retrieval status (verbatim-verified / disagrees / cannot-retrieve), verbatim quote + page or equation number for each
4. **Theorem-confidence registry** — companion file `paper/Delta_machine_paper_theorem_registry.md` listing every theorem/proposition/conjecture in the draft with its confidence and the source file it came from

Every theorem must have:
- A verbatim citation in the audit log if depending on prior work
- An explicit confidence ≥ 0.95 if stated as theorem (else demoted)

---

## Done when

- Draft file exists at the specified path
- ≥ 40 pages (estimate by word count or `pandoc` + LaTeX page count)
- All 9 sections present
- Citation audit log complete (every external citation classified)
- Theorem-confidence registry complete
- Internal consistency pass run (notation, numbering, conventions)
- Adversarial reviewer pass run (red flags addressed)
- LaTeX compiles via `pandoc -f markdown -t latex` without errors

## Stop and report immediately if

- A core source file in the bundle is missing or unreadable
- A core theorem (e.g. master theorem 2.1) cannot be derived from cited references AND has no clean proof in the source files (downgrade to conjecture, but state explicitly)
- More than 20% of external citations cannot be PDF-verified (this would mean the paper rests on too-much fabrication risk; flag and stop)
- Internal consistency pass finds contradictions between source files that cannot be resolved without picking a side (flag the contradictions and stop for user decision)
- Murty-Murty 2009 prior-art check finds the master theorem appears verbatim there (flag — this would change the novelty story)

Do **not** submit a draft as "publication-grade" if any of the above triggered.
