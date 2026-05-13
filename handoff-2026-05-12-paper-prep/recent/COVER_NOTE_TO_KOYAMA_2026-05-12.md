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
together with three appendices (proofs of the corrected `B_∞`
identity and the local Perron double-pole residue, plus a verbatim
citations appendix), and a short status note on the Lean 4
inventory.

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
sense in mind.

If you had a different sense in mind (e.g. Lean ↔ numerical
cross-check, or two independent symbolic derivations of the
identity itself), I can adjust.

**Other status notes.**

* The Lean 4 formalisation inventory now compiles cleanly under
  `leanprover/lean4:v4.28.0` + Mathlib `8f9d9cff…`. **Nine `sorry`s
  across nine files** remain, each annotated `MATHLIB-PREREQ:` or
  `RESEARCH-OPEN:`. Three files are fully proved (0 `sorry`):
  - **`LocalPerronResidue.lean`** — Lemma X.3.1, machine-verified
    end-to-end (unconditional).
  - **`CorrectedBInfty.lean`** — **Theorem X.4.1 (the paper's
    headline algebraic identity), machine-verified conditional on
    a single named `h_convergence` hypothesis that packages the
    four analytic inputs of Appendix A (Akatsuka 2013 eq. (2.5),
    log-Euler-product expansion, imprimitive-induction Euler-factor
    identity, geometric-series tails).** Closed via Aristotle
    dispatch 2026-05-12.
  - **`DPAC_closure_attempt.lean`** — proves DPAC unconditionally
    for $K \in \{2, 3, 4\}$, reformulates the general case as
    `FiniteLogRatioLI`, and records the precise obstruction
    certificate (Pólya 1913 discreteness + a single open avoidance
    statement at $\zeta$-zero ordinates). General-$K$ DPAC remains
    open, comparable to the Linear Independence Hypothesis.

  The full inventory is in `LEAN_SORRY_STATUS.md`.
* The four "open challenges" (SP-L, conductor-confounded trend, the
  `Sym² / ⟨f,f⟩` normalisation, GL(2) reciprocal-derivative control)
  are each stated with the precise input that would close them,
  rather than left informal.
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
