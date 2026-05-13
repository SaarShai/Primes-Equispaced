<!--
schema_version: 1
title: "Cover note to S. Koyama accompanying the §X draft"
date: 2026-05-12
type: outgoing-correspondence-draft
tier: working
status: DRAFT_FOR_USER_REVIEW_NOT_SENT
intended_recipient: shin-ya.koyama (per 2026-05-12 ask)
attachments:
  - handoff-2026-05-12-paper-prep/SECTION_DRAFT_2026-05-12.md
  - handoff-2026-05-12-paper-prep/SCOPE_AUDIT_10E13_2026-05-12.md
  - handoff-2026-05-12-paper-prep/APPENDIX_A_BINFTY_PROOF.md
  - handoff-2026-05-12-paper-prep/APPENDIX_B_CK_SUBLEADING_PROOF.md
  - handoff-2026-05-12-paper-prep/APPENDIX_C_CITATIONS.md
  - handoff-2026-05-12-paper-prep/LEAN_SORRY_STATUS.md
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

Before I polish further or begin LaTeX conversion, **two scope
questions** where I want to make sure we are aligned:

**1. What "verification at `10^{13}`" means in the manuscript.**

Internally, our `10^{13}`-scale evidence is **only** the Phase-1
Dominance-of-`-1` replication: two independent implementations
(`primesieve` plus a hand-rolled C segmented sieve) agree on every
`π(x; q, a)` count at `x = 1.3 · 10^{13}` for
`N ∈ {7, 8, 11, 19, 23}`, identity (3.1) of *nontriv.pdf* is verified
across 495 `(N, x, a)` cells, and the qualitative dominance signal
is reproduced for `N ∈ {7, 8, 19}`. This is the bundle we sent on
2026-05-04.

The **analytic identities** (`B_∞` residuals, `C_1` subleading,
the `|D_K| · ζ(2)` drift toward `e^{-γ}`) are verified at much
smaller `K`: `K = 2·10^{6}` to `10^{7}` with 50-decimal precision
across mpmath / PARI 2.17.3 / Arb 250-bit. They do *not* extend to
`10^{13}` with any current technology, and the manuscript keeps
the two scales rigorously separate.

If your mental picture of "`10^{13}` rigor" matches the Phase-1
replication scope above, we are aligned. If you had a stronger
sense in mind (e.g. an analytic identity verified at `10^{13}`),
please let me know and I will re-scope.

**2. What "double-verification" means in §X.2.**

I have drafted §X.2 with two notions of "double-verification":

* **Analytic stack:** the same identity computed by three independent
  numerical stacks (mpmath, PARI/GP 2.17.3, Arb 250-bit via
  python-flint) with the per-prime closed-form expansion to avoid
  truncation drift; agreement is to all displayed digits at
  `K = 2·10^{6}` and to within `≈ 10^{-5}` at `K = 10^{7}`,
  consistent with `K^{-1/2}/\log K` decay.
* **Phase-1 stack:** the same residue counts computed by two
  independent prime-enumeration implementations (`primesieve` library
  and a hand-rolled C segmented sieve), with a second hardware path
  agreeing through `1.3 · 10^{12}`.

If you had a different sense in mind (e.g. Lean ↔ numerical
cross-check, or two independent symbolic derivations of the
identity itself), I can adjust.

**Other status notes.**

* The Lean 4 formalisation inventory now compiles cleanly under
  `leanprover/lean4:v4.28.0` + Mathlib `8f9d9cff…`. **Ten `sorry`s
  across nine files** remain, each annotated `MATHLIB-PREREQ:` or
  `RESEARCH-OPEN:`. Two files are fully proved (0 `sorry`):
  - **`LocalPerronResidue.lean`** — Lemma X.3.1 is now
    machine-verified end-to-end (closed via Aristotle dispatch on
    2026-05-12).
  - **`DPAC_closure_attempt.lean`** — proves DPAC unconditionally
    for $K \in \{2, 3, 4\}$ using only $0 < \mathrm{Re}(\rho) < 1$,
    reformulates the general case as `FiniteLogRatioLI`, and
    records the precise obstruction certificate (Pólya 1913
    discreteness of the finite exponential-polynomial zero set,
    plus a single open avoidance statement at $\zeta$-zero
    ordinates). The general-$K$ DPAC remains open, diagnostically
    comparable to the Linear Independence Hypothesis for
    $\zeta$-zero ordinates.

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
