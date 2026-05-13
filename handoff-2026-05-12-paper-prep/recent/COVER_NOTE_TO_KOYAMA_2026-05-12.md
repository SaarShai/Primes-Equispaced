<!--
schema_version: 1
title: "Cover note to S. Koyama accompanying the §X draft"
date: 2026-05-12
type: outgoing-correspondence-draft
tier: working
status: DRAFT_FOR_USER_REVIEW_NOT_SENT
intended_recipient: shin-ya.koyama (per 2026-05-12 ask)
attachments:
  - handoff-2026-05-12-paper-prep/recent/SECTION_DRAFT_2026-05-12.md
  - handoff-2026-05-12-paper-prep/recent/SCOPE_AUDIT_10E13_2026-05-12.md
  - handoff-2026-05-12-paper-prep/recent/APPENDIX_A_BINFTY_PROOF.md
  - handoff-2026-05-12-paper-prep/recent/APPENDIX_B_CK_SUBLEADING_PROOF.md
  - handoff-2026-05-12-paper-prep/recent/LEAN_SORRY_STATUS.md
  # Appendix C kept in reproducibility bundle (citation audit), not as a separate appendix.
tags: [koyama, correspondence, manuscript-prep, scope-confirmation]
-->

# Cover note — draft for user review

**Subject:** First draft of the Technical/Computational section — two scope questions before we go further

---

Dear Shin-ya,

Thank you for your 2026-05-12 note. I'm honoured by the co-authorship
offer and ready to push toward submission.

Attached is a first internal draft of the Technical/Computational
section (§X. Methodology, formalization, and numerical evidence),
together with two appendices (Appendix A: pen-and-paper proof of
the corrected `B_∞` identity, Theorem X.4.1; Appendix B: proof of
the $c_K$ leading + subleading identity, Theorem X.4.2, together
with the Laurent-algebra for the local Perron double-pole residue
in §B.2), the scope-audit note on what `10^{13}` does and does not
verify, and a per-`sorry` inventory for the Lean 4 lake project.

The draft is organised around the four pillars you described as
the core:

1. The `e^{-γ}` correction of the asymptotic target (Aoki–Koyama 2023);
2. The corrected `B_∞` identity and the local Perron residue
   `C₁ = -L''(ρ)/(2 L'(ρ)²)`, both established unconditionally;
3. The open challenges that organise the program forward — the
   shifted Perron leading remainder (SP-L), the conductor-confounded
   elliptic-curve rank trend, the `Sym² / ⟨f,f⟩` normalisation, GL(2)
   reciprocal-derivative control, and DPAC;
4. The rigorous Phase-1 replication of your Dominance-of-`-1`
   residue-count tables at `x = 1.3 · 10^{13}`.

Two scope confirmations before I begin LaTeX conversion:

**1. "Verification at `10^{13}`" — Phase-1 only.** Our `10^{13}`-scale
evidence is the Phase-1 Dominance-of-`-1` replication (two
implementations agreeing on every `π(x; q, a)` count at
`x = 1.3 · 10^{13}` for `N ∈ {7, 8, 11, 19, 23}`; identity (3.1)
verified across 495 cells; bundle sent 2026-05-04). The analytic
identities (`B_∞` residuals, `C_1` subleading, the `|D_K| · ζ(2)`
drift toward `e^{-γ}`) are verified at `K = 2·10^{6}`–`10^{7}` with
50-decimal precision across mpmath / PARI 2.17.3 / Arb 250-bit, and
the manuscript keeps the two scales rigorously separate. Please
confirm this matches your framing.

**2. "Double-verification" — two stacks per claim.** §X.2 uses two
notions: (i) for the analytic identities, the same quantity computed
by mpmath, PARI/GP 2.17.3, and Arb 250-bit via python-flint,
agreeing to all displayed digits at `K = 2·10^{6}` and to
`≈ 10^{-5}` at `K = 10^{7}`; (ii) for the Phase-1 counts, two
independent prime-enumeration implementations (`primesieve` plus a
hand-rolled C segmented sieve), with a second hardware path
agreeing through `1.3 · 10^{12}`. Let me know if you had a different
sense in mind (e.g. Lean ↔ numerical cross-check, or two independent
symbolic derivations of the identity itself).

**Phase-1 cell discrepancies pending your review.** Per your
2026-05-12 note, you offered to resolve the table discrepancies. To
save you a hunt through §X.5.1, here are the substantive ones at
`x = 1.3 · 10^{13}` (74 of 81 cells exact, ~91%, excluding the 11
Table-4 small-`x` rows which look like an `x`-label error):

| Table | $N$ | cell ($a$) | our value | your value | note |
|---|---:|---:|---:|---:|---|
| 3 | 7 | $a = 6$ | — | — | $\Delta = 50$ between our value and yours; clean digit-shift profile |
| 5 | 11 | $a = 10$ | $11{,}503$ | $71{,}711$ | **substantive** — dominance ranking for $N = 11$ at this checkpoint turns on this cell |
| 6 | 19 | $a = 13$ | $24{,}559$ | $55{,}581$ | substantive |
| 6 | 19 | $a = 18$ | $54{,}192$ | $57{,}192$ | substantive (single-digit, could be OCR) |
| 7 | 23 | $a = 19$ | $79{,}327$ | $79{,}227$ | $\Delta = 100$, clean digit-transposition |
| 4 | 8 | (small-`x` rows) | — | — | 11 rows; one row at the supposed $x = 1.3\cdot 10^{12}$ exact-matches our $x = 10^{12}$ row, suggesting an $x$-label error |

The headline qualitative result — `-1 mod N` dominance at
$x = 1.3 \cdot 10^{13}$ — is reproduced for $N \in \{7, 8, 19\}$.
For $N = 11$, reproduction hinges entirely on the Table-5 $a = 10$
cell; with our $11{,}503$, $-1$ ranks 4th of 5 non-residues, with
your reported $71{,}711$, $-1$ ranks 2nd (comfortably in the top
group). For $N = 23$ neither value enters the dominance regime
(your nontriv.pdf attributes this to a low-lying $L$-zero modulo
$23$ and an onset around $e^{33.4} \approx 3 \cdot 10^{14}$).

I'll fold whatever you confirm into §X.5.1 before LaTeX conversion.

**Other status notes.**

* The Lean 4 formalisation inventory now compiles cleanly under
  `leanprover/lean4:v4.28.0` + Mathlib `8f9d9cff…`. **Nine `sorry`s
  across nine files** remain, each annotated `MATHLIB-PREREQ:` or
  `RESEARCH-OPEN:`. Three files are fully proved (0 `sorry`):
  - **`LocalPerronResidue.lean`** — Lemma X.3.1, machine-verified
    end-to-end (unconditional).
  - **`CorrectedBInfty.lean`** — **Theorem X.4.1 (the paper's
    headline algebraic identity), Lean-verified conditional on a
    single named `Filter.Tendsto` hypothesis** asserting that the
    partial prime-power tail $T_K(\chi,\rho)$ converges to the
    four-component right-hand side. The pen-and-paper proof in
    Appendix A establishes exactly that convergence from Akatsuka
    2013 eq. (2.5) + log-Euler-product expansion + the imprimitive
    Euler-factor identity + geometric-series tails; given the
    convergence, the Lean proof is three lines
    (`Classical.epsilon_spec` + `tendsto_nhds_unique`). Closed via
    Aristotle dispatch 2026-05-12.
  - **`DPAC_closure_attempt.lean`** — proves DPAC unconditionally
    for $K \in \{2, 3, 4\}$, reformulates the general case as
    `FiniteLogRatioLI`, and records the precise obstruction
    certificate (Pólya 1913 discreteness + a single open avoidance
    statement at $\zeta$-zero ordinates). General-$K$ DPAC remains
    open, comparable to the Linear Independence Hypothesis.

  The full inventory is in `LEAN_SORRY_STATUS.md`.
* The three primary open challenges in §X.7 (Q:Perron, Q:DPAC,
  Q:EC-recip) are each stated with the precise input that would
  close them; three further EC-side questions (conductor-confound,
  Sym² normalisation, EC-NDC) appear in the "Further questions"
  block at the end of §X.7.
* On the GL(1) halo route, my honest assessment is that a naïve
  transfer of the GL(2) halo theorem yields only `K^{1/2+ε}`, which
  does not reach `o(log K)`. I have written this up as a negative
  finding in `HALO_GL1_SKETCH_2026-05-12.md`; it does not block the
  manuscript but I wanted you to see it before deciding whether to
  include SP-L as an open challenge or attempt a deeper route.

I am happy to start LaTeX conversion as soon as the two scope
questions above are settled. The author-order and journal target
are open placeholders; I defer both to you.

With thanks and best wishes,

Saar

---

## Notes for the human author (not part of the email)

* The two scope questions are the single biggest risk of expectation
  mismatch with Koyama — surfacing them now (before LaTeX) costs
  one email round-trip and avoids potentially rewriting §X.2 and
  §X.5 later.
* If Koyama answers "yes, that matches my framing" to both, we can
  proceed straight to LaTeX + Abstract + Introduction.
* If he answers "I meant something stronger," we re-scope before
  sinking time into format-conversion.
* The Lean-status paragraph is included because Koyama's 2026-05-12
  note specifically asked for "the Lean 4 formalization path." It is
  honest about the remaining sorries; we are not over-claiming.
* The halo-route negative finding is mentioned only because we have
  it; Koyama may or may not want it in the paper. Soft offer, his
  decision.
