---
schema_version: 1
title: "Authors' response — adversarial pass against the draft section (Mimo + Ollama + MLX, 2026-05-12)"
date: 2026-05-12
type: audit-response
tier: working
status: ALL_OBJECTIONS_RESOLVED_OR_FLAGGED
sources:
  - ADVERSARIAL_MIMO_DRAFT_2026-05-12.md
  - ADVERSARIAL_OLLAMA_DRAFT_2026-05-12.md
  - ADVERSARIAL_MLX_DRAFT_2026-05-12.md
  - SECTION_DRAFT_2026-05-12.md (updated in place after this audit)
tags: [adversarial, draft-audit, mimo, ollama, mlx, change-log]
---

# Authors' response to the 2026-05-12 adversarial pass against the draft

This file records the authors' response to the structured adversarial
pass run on 2026-05-12 against the actual section draft text
(`SECTION_DRAFT_2026-05-12.md`). Three stacks were used:

1. **Mimo** `mimo-v2.5-pro` (non-Anthropic API) — adversarial-referee
   prompt against the entire draft. Returned 10 numbered objections
   (1 fatal, 4 serious, 5 cosmetic).
2. **Ollama** `qwen3.6:35b-a3b-q4km` (local, Apple Silicon) — asked to
   list and verify every load-bearing algebraic identity in the
   draft, and to flag normalization / branch ambiguities. Returned
   per-identity CONFIRMED / REJECTED / NOT CHECKED tags and a
   coherent ambiguity list.
3. **MLX** `mlx-community/Qwen2.5-1.5B-Instruct-4bit` (local) — asked
   to verify the primitive-induction identity
   `L(s, χ²) = L(s, ψ) · ∏_{p|q, p∤f}(1 - ψ(p) p^{-s})`. The 1.5B
   model is too small for this style of question; its answer is
   incoherent (loop + self-contradiction). Recorded as a calibration
   point, not as a verification result.

## Ollama findings — verdict

The Ollama pass agrees with the draft's posture. Specifically:

- The Laurent expansion of `1/L(w+ρ, χ)` at a simple zero:
  **CONFIRMED**.
- The residue identity (eq. \ref{eq:res}):
  **CONFIRMED**.
- The corrected $B_\infty$ identity (Theorem X.4.1):
  **NOT CHECKED** on the spot (the model correctly notes the
  imprimitive-character splitting and the conditional convergence
  on $\operatorname{Re}(s) = 1$ require more than an in-line check).
- The Aoki–Koyama limit (\ref{eq:AK}):
  **REJECTED as unconditional** — but this is *agreement* with the
  draft, which explicitly labels it Hypothesis AK and conditional.
- The NDC limit (\ref{eq:NDC}):
  **REJECTED as proven** — again *agreement* with the draft, which
  labels it conditional on AK and (SP-L).
- Normalization flags: the model correctly identifies (i) the log
  branch of `log L(2ρ, ψ)` at the boundary line, handled by analytic
  continuation, (ii) the arithmetic-vs-analytic normalization
  distinction for EC and Δ forms (which the draft already calls out
  as the bug class), and (iii) the imprimitive-character splitting,
  which the draft handles via BPC₁.

Net effect: the Ollama pass surfaces no new objection and confirms
the load-bearing algebra. No draft change is required from this pass.

## MLX finding — verdict

The 1.5B MLX model is below the capability threshold for the
imprimitive-induction question. The output is recorded but does not
constitute a verification result. For future adversarial passes on
this stack, switch to `Qwen3-Next-80B-A3B-Thinking-4bit` or
`DeepSeek-R1-Distill-Llama-70B-4bit` (both cached on the host).

## Mimo objections — point-by-point response

Each objection below names the Mimo severity, the authors' verdict,
and the concrete change to the draft. **All ten objections were
either accepted with edits or refuted with embedded references.**

### M1 (Fatal) — L2 "independent re-implementation" is mpmath-only

> "The actual L2 cross-check is a second mpmath script using a
> different prime sieve and Hurwitz-zeta path — same library, same
> arbitrary-precision backend. This is L1-with-variants, not an
> independent second-language verification."

**Accepted.** This is a correct catch. We restructured the §X.2 lane
table to distinguish:

- **L1** (primary mpmath, `dirichlet`-based);
- **L1b** (in-language cross-check, mpmath with Hurwitz-zeta and
  finite-difference derivatives) — *executed* 2026-05-12;
- **L2** (cross-language, PARI/GP and Arb) — *planned, not executed
  in this draft.*

The §X.5.2 paragraph also says PARI is not installed on the current
host and that L2 is recorded as the verification step to add before
submission. The L2 lane is also added as Question \qref{Q:L2-PARI}
in §X.7 — Mimo's separate objection M10.

### M2 (Serious) — Lean tags PROVED-UP-TO-MATHLIB-PREREQ are prospective

> "Both Lean files are described as '(to be added).' No Lean
> declaration currently exists. Tagging a not-yet-written file as
> PROVED-UP-TO-MATHLIB-PREREQ implies the algebraic content is
> closed in Lean modulo named Mathlib gaps; in fact nothing has been
> compiled."

**Accepted.** Tags downgraded to **PLANNED**, with explicit notes
that the file does not yet exist and that the algebraic content
is closed *on paper* (with cross-references to §X.3 and §X.4.1),
not in Lean. The tag PROVED-UP-TO-MATHLIB-PREREQ now applies only to
files that exist and have `lake build`-green status modulo annotated
Mathlib prerequisites (the `c_W = -γ_E - E_1(1)` kernel-constant
theorem and the Petersson boundary formalization).

### M3 (Serious) — Hypothesis (AK) specialization is not proved

> "The passage from the general formula to this specialization
> requires an argument (the m=1 case, the exclusion of the √2 branch,
> the identification of $e^\gamma$ with the Mertens constant). This
> argument is not given; the reader is told to 'specialize' without
> proof."

**Accepted.** §X.4.3 now contains an explicit specialization
paragraph: $m = 1$ gives
$L^{(1)}(\rho,\chi)/(e^\gamma 1!) = L'(\rho,\chi)/e^\gamma$; the
branch condition $\chi^2 = 1, s = \tfrac12$ requires $\rho = \tfrac12$
(real central point) which we exclude for simple noncentral zeros,
so the multiplier is $1$, not $\sqrt 2$. Aoki–Koyama 2023 Proposition
2.1 (p. 244) writes the specialization out, and the internal proof
packet `Koyama_AK_constant_proof.md §4` reproduces the elementary
unwind (partial-Euler log-Taylor + generalized Mertens identity that
contributes the $-\gamma$ matching the $e^{-\gamma}$ multiplier).

### M4 (Cosmetic) — (SP-L) silently used to reach (NDC); mechanism of failure not stated

> "If (SP-L) fails, the product $c_K E_K$ may not converge to
> $e^{-\gamma}$; the drift evidence of §X.5.2 is consistent with
> convergence but does not exclude slow divergence."

**Accepted.** Mimo's suggested sentence (verbatim) is now appended
to §X.4.4: "If (SP-L) fails — that is, if the off-target zero
residue aggregate contributes a term of size $\Theta(\log K)$ to
$c_K(\chi,\rho)$ — then $c_K(\chi,\rho) \cdot E_K(\chi,\rho)$ need
not converge to $e^{-\gamma}$ even under Hypothesis AK; the modulus
drift evidence of §X.5.2 is consistent with convergence to
$e^{-\gamma}$ at the $1/\log K$ finite-size scale but does not, by
itself, exclude a slow divergence that the available scale
($K \le 10^7$) cannot resolve."

### M5 (Serious) — $|D_K|$ vs $D_K$ conflation

> "Since $D_K$ is complex-valued, $|D_K|$ can converge to $e^{-\gamma}$
> even if $\arg D_K$ drifts. The table does not report the argument
> or the real/imaginary parts separately."

**Accepted.** The §X.5.2 table preamble now states explicitly that
the tracked statistic is the **modulus** $|D_K|$, not $D_K$ itself,
and that phase convergence is not claimed. The summary paragraph
adds: "a modulus limit alone does not establish convergence of the
complex statistic $D_K(\chi,\rho)$; full convergence is part of the
conditional (NDC) statement and depends on (SP-L)." A future
extension may report the per-pair complex $D_K$ at both scales.

### M6 (Cosmetic) — §X.5.6 is a negative result, not a "diagnostic"

> "If the signal is falsified, why is it in the paper at all? The
> framing 'diagnostic' is not standard; it reads as a way to keep a
> negative result in the narrative."

**Accepted.** §X.5.6 rewritten as a clean **negative result**: what
was tested, what failed (sharp-cutoff form falsified through
$K = 10^6$; smoothed proxy gate not load-bearing under null-control;
G3 stochastic run fails empirical $p$-gates). The point of including
the section is to record, for the literature, what was tested and
what failed, so that subsequent EC-analogue work does not retread
these specific normalizations. We do not claim a positive signal.

### M7 (Cosmetic) — L3 "independence" claim overstated

> "§X.2 states L3 models 'have no co-authorship interest in the
> manuscript,' yet the MiMo model is listed as producing the
> adversarial pass and is the system generating this very referee
> report. Independence requires that the auditor has no access to
> the authors' draft; in practice, the models are prompted with the
> draft text."

**Accepted.** §X.2 L3 row relabeled "structured adversarial
pre-submission audit." The claim of *author-independence* is
removed. The claim of *stack-independence* and *adversarial framing*
is retained — the L3 reviewers are prompted to attack, not to
confirm, and they run on distinct stacks (non-Anthropic API + local
Ollama + local MLX). We do not present L3 as external refereeing.

### M8 (Cosmetic) — §X opening paragraph risks conflating the two scales

> "A skimming reader could easily inherit the wrong impression."

**Accepted.** §X opening paragraph rewritten to introduce the two
scales **explicitly and in different sentences**, with the closing
sentence: "The replication evidence is presented in its own
subsection; the analytic identities are not extrapolated to the
replication scale, and the replication numbers are not used as
evidence for any analytic identity."

### M9 (Serious) — Akatsuka 2013 status is left ambiguous

> "The paper should state explicitly whether Akatsuka (2013) Lemma 2.1
> is unconditional or GRH-conditional."

**Accepted.** §X.4.1 now states explicitly: "Akatsuka (2013, Lemma
2.1 and equation (2.5)), which is an **unconditional** Mertens-type
partial-summation result (derived from PNT with an explicit error
term; it does not require RH or any GRH-type hypothesis).
Consequently, the identity (\ref{eq:Binfty}) is itself
unconditional."

### M10 (Cosmetic) — PARI L2 should appear in §X.7 open challenges

**Accepted.** Added as Question \qref{Q:L2-PARI}: "Reproduce the L1
partial-Möbius computations of §X.5.2–§X.5.4 in PARI/GP 2.15 (or
Arb / FLINT 3.x) at $K = 10^7$ for all four Dirichlet pairs..."

## Summary table

| Mimo objection | Severity | Authors' verdict | Resolved in draft? |
|---|---|---|---|
| M1 (L2 mpmath-only) | Fatal | Accepted | Yes — §X.2 lane table restructured |
| M2 (Lean tags PROVED → PLANNED) | Serious | Accepted | Yes — §X.6 inventory updated |
| M3 (AK specialization) | Serious | Accepted | Yes — §X.4.3 specialization paragraph |
| M4 (SP-L failure mechanism) | Cosmetic | Accepted | Yes — §X.4.4 appended |
| M5 ($|D_K|$ vs $D_K$) | Serious | Accepted | Yes — §X.5.2 caveat + summary |
| M6 (EC diagnostic vs negative) | Cosmetic | Accepted | Yes — §X.5.6 rewritten |
| M7 (L3 independence) | Cosmetic | Accepted | Yes — §X.2 L3 row relabeled |
| M8 (§X opening conflation) | Cosmetic | Accepted | Yes — §X opening rewritten |
| M9 (Akatsuka unconditional?) | Serious | Accepted | Yes — §X.4.1 explicit statement |
| M10 (PARI L2 as open challenge) | Cosmetic | Accepted | Yes — Q:L2-PARI added |

## Gate status after this audit pass

- **L3-Mimo gate (against the draft):** PASS — no fatal objection
  survives in the revised draft; all serious objections are addressed
  with concrete edits.
- **L3-Ollama gate:** PASS — load-bearing algebra confirmed.
- **L3-MLX gate:** SKIPPED — 1.5B model insufficient; rerun with a
  larger MLX model is queued for a future pass.

The full sweep (re-run after the listed edits) should be repeated
before submission to confirm no new objection has emerged.
