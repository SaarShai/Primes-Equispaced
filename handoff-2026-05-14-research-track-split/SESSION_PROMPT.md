# Separate-session prompt — Farey NOW research track (everything except the Koyama §X draft)

Paste the body below as the first message of a new Claude Code session opened in
`/Users/za/Documents/Farey NOW`. The session you are reading right now keeps
working on the §X technical-section draft for the joint Saar–Koyama paper;
the new session you are about to start picks up the *research* track in
parallel, with no overlap on the draft.

---

## Context

You are continuing the **Farey NOW** math-research project at
`/Users/za/Documents/Farey NOW`. The subproject is **`primes-equispaced/`** — a
joint Saar–Koyama paper on Farey-spectroscope methods for the
Dominance-of-`-1` programme.

Today is **2026-05-14**. Koyama replied 2026-05-12 confirming both scope
questions and granting co-authorship: *"Please go ahead with the technical
draft."* He will re-check the Phase-1 table discrepancies after May 20.

**Two parallel tracks are now active:**

1. **Draft track (NOT yours).** A separate session is preparing the §X
   technical/computational section + appendices for the joint paper. It owns
   everything inside `primes-equispaced/handoff-2026-05-12-paper-prep/recent/`
   and the corresponding LaTeX bundle. **Do not touch those files.**
2. **Research track (yours).** Everything else: closing the halo route to
   unconditional H1, sorry-closing for the Lean inventory, DPAC headline
   research, follow-on numerical and analytic work.

## Where the research stands (read these in order)

- **`primes-equispaced/start.md`** and the project's
  `primes-equispaced/.claude/CLAUDE.md` are the project rules. Caveman-ultra
  output, delegate to local models / Codex / Aristotle / Mimo first, write to
  `log.md` + `index.md` after verified work.
- **`primes-equispaced/index.md`** — wiki catalog (already updated through
  2026-05-14).
- **`primes-equispaced/log.md`** — append-only timeline. The 2026-05-13 and
  2026-05-14 entries cover the most recent work (Aristotle rounds 7-8,
  RamanujanSum closure, axiom audit, halo plan).
- **`primes-equispaced/HANDOFF.md`** — current handoff document if present.
- **`primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md`**
  — the single anchor for the halo route. Four conditional doors (A: shifted
  negative second moment, B: HaloShiftComparison, C: ResidueFirstH1Rewrite,
  D: $M_T = o(T^{1/4})$); Door B already closed under the framework's
  standing GRH with $R > \sqrt{1+A^2}$; staged plan toward unconditional
  offcentral H1; density-method side-quest as a parallel route.

## Concrete next move — Stage 0 of the halo plan

**The gate that decides everything downstream is Stage 0: a one-page audit
determining whether the H1 proof in the repo accepts a *signed contour
residue* contribution (halo route applies) or genuinely requires a *positive*
`R_B` bound (halo fails, density-method side-quest is the alternative).**

Files to read for Stage 0:

- `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md`
- `handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/` (residue-form content)
- `handoff-2026-05-11-h1-shell-moment-wave/`
- `handoff-2026-05-11-ec-h2-mertens-sprint/` (numerator side)

**Deliverable:**
`handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md`
— a one-page memo with two possible verdicts:

- **GREEN**: signed contour residue is acceptable upstream; the halo route
  applies; next move is Stage 1 (Door B boundary-arc extension + Door D
  numerator audit).
- **RED**: positivity is genuinely required upstream; the halo route fails;
  next move is the density-method side-quest (§8.3 of the halo plan), aiming
  for a loose negative second moment of `L'(rho)` with target `T^c`, `c < 3`.

The audit should cite exact lines from the H1 simple-zero conditional stack
where `sum |Phi_T(rho)/L'(rho)|` is used and check whether the containing
estimate accepts a signed sum. If a positivity is required upstream (e.g. for
an `l^1` energy identity), surface it.

## Follow-on items after Stage 0

If GREEN:

1. **Stage 1 parallel a** — write
   `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` stating the boundary-arc
   extension of the existing noncluster `H_A` stability lemma with
   $R > \sqrt{1+A^2}$ (already proved in the plan; this is write-up only).
2. **Stage 1 parallel b** — write `H1_NUMERATOR_M_T_AUDIT_2026-05-14.md`
   computing $M_T = \sup_\text{halo} |\Phi_T(s)|$ for the exact $\Phi_T$ in
   the H1 statement. Expect $M_T = T^{o(1)}$; document.
3. **Stage 2 sprint** — write
   `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` transcribing
   Heap–Soundararajan + Bui–Florea (arXiv:2302.07226) for fixed-conductor
   GL2. Decompose: AFE for $1/L_E^*$, mean-square of partial sum, off-diagonal
   via Mertens / Rankin–Selberg, near-zero (bad-set) cure.

If RED:

1. **Density-method side-quest** — write
   `DENSITY_METHOD_RB_LOOSE_2026-05-14.md` exploring §8.3 of the halo plan
   as a parallel route. Target: $\sum_\rho^{mult} |L'(\rho)|^{-2} \ll T^c$
   with any $c < 3$; conjectural truth $c = 1$.

## Lean inventory (sorry-closing track)

`formal-conjectures/` has **2 sorries** remaining, both the DPAC headline
(LI-class — a genuine open problem). 8 of 10 files fully proved. The most
recent Aristotle dispatch (round-8) decided NOT to attempt round-9 because
the unconditional push on `MertensSpectroscopeUniversality` requires
~2000+ LOC of new Mathlib analytic-NT machinery. **Loop is stopped.** Do
not re-launch unconditional-push rounds without a fresh angle.

If a new opening appears (e.g. an upstream Mathlib formalisation of
Akatsuka 2013 eq. 2.5 or Soundararajan 2009 Theorem 1), discharge the
corresponding `h_convergence` or `h_explicit_formula` hypothesis and log it.

Inventory authority:
`handoff-2026-05-12-paper-prep/recent/LEAN_SORRY_STATUS.md`. **Read this
file — do not write to it.** That file belongs to the draft track. If the
inventory changes, write a fresh per-`sorry` note in the research-track
folder and ping the draft session via a `log.md` entry.

## Boundary with the draft session

- **Off-limits:** anything inside
  `primes-equispaced/handoff-2026-05-12-paper-prep/recent/` (cover note,
  section draft, appendices, LEAN_SORRY_STATUS, midweek update, abstract,
  intro, SP-L packages, LaTeX bundle).
- **Yours:** everything in
  `primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/`,
  `primes-equispaced/handoff-2026-05-14-research-track-split/`, all earlier
  `handoff-2026-05-11-*/` directories, `formal-conjectures/` source files,
  numerical scratch (`*.py`, `*.gp`, `*.lean`, `*_run.log`),
  `koyama_replication_bundle/`.
- **Shared:** `log.md`, `index.md`, `HANDOFF.md`. Both sessions append; keep
  entries dated and tagged with the track (`paper-prep` for the draft
  session, `research` for yours).

If you need a value the draft session has changed, read it; if you need to
change a shared file, append rather than overwrite.

## Conventions

- Caveman-ultra for status output. Tables over paragraphs.
- Delegate to local models / Codex / Aristotle / Mimo before doing
  computation yourself.
- Document only after verified work. Append to `log.md` with operation
  type; update `index.md` if a material page is added.
- Always cite wiki paths / IDs.
- No new file paths unless they fit the project's `handoff-YYYY-MM-DD-*` or
  `formal-conjectures/` patterns.
- No axioms introduced into the Lean project.

## Start

Begin with Stage 0. Output the verdict (GREEN / RED) plus the one-page memo
at the location above, then propose the next concrete step. Stop and ask if
the verdict is ambiguous or if Stage 0 surfaces something that materially
changes the halo plan itself.
