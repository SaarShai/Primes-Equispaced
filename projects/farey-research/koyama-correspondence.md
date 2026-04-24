---
schema_version: 2
title: Koyama Correspondence
type: project
domain: project
tier: semantic
confidence: 0.9
created: 2026-04-24
updated: 2026-04-24
verified: 2026-04-24
sources:
  - raw/farey-archive/state-docs/KOYAMA_REPLY_DRAFT_V3.md.txt
  - raw/farey-archive/state-docs/KOYAMA_FOLLOWUP_QUESTIONS.md.txt
  - raw/farey-archive/state-docs/KOYAMA_CORRECTION_AND_WINS.md.txt
  - raw/farey-archive/handoff/complete_farey_handoff.md.txt
supersedes: []
superseded-by: 
tags: [farey, koyama, correspondence, collaboration]
---

# Koyama Correspondence

## Current State

Prof. Shin-ya Koyama is an active collaborator/contact. The working record now spans the earlier DRH / Farey spectroscope exchange, the EDRH / normalized-duality phase, the GL(2) / elliptic-curve phase, and the current C1 / W2 prime / Dominance-of-`-1` phase.

No email should be sent without explicit user approval.

## Correspondence Arc

### 1. Farey / DRH origin

- Koyama first asked for the full technical draft and exact definitions behind `R(p)`, `ΔW(p)`, and the spectral bridge.
- Saar replied with the Farey spectroscope summary, Lean 4 work, and the repository link.
- Koyama acknowledged the likely DRH relevance and asked for a formal draft rather than an email summary.

### 2. Normalized-duality / Euler-product phase

- Koyama connected the truncated Euler-product side to Aoki-Koyama-style DRH and said the non-trivial character case should show `O((log K)^{-m})` decay.
- Saar reported the additive-side Perron analysis, the duality identity, and the `1/ζ(2)` conjecture.
- Koyama clarified that the trivial-`ζ` case and the non-trivial character case should be treated separately.
- Saar then extended the computations, corrected the character identifications, and reported `D_K` approaching a character-independent constant near `1/ζ(2)`.
- Koyama treated this as a strong empirical indication and suggested pushing to larger `K`.

### 3. GL(2) / elliptic-curve phase

- Koyama suggested a GL(2) completed-L-function formulation with a smooth cutoff, conductor phase correction, and possible `Γ`-factor.
- Saar tested `37a1`, `389a1`, and `Δ`, found that the raw pointwise `1/ζ(2)` story did not survive unchanged, and asked about the exact normalization.
- Koyama guided the next computations, then accepted that the `Γ`-factor and truncation range mattered.
- Saar later reported the post-bugfix `μ_f(p^2)` correction, the repaired values, and the failure of the raw Sym² / Petersson proportionality as originally stated.

### 4. C1 / W2 prime phase

- The current record now centers on the corrected C1 statistic and the W2 prime model:
  - `Δ` anchor around `0.950231842`
  - `37a1`, `389a1`, `5077a1` rank anchors
  - a 22-point fit with a significant `log(N)` term
- Koyama responded positively to the bugfix/recompute process, highlighted the apparent linear-in-rank pattern, and said the result was scientifically valuable even though the original Sym² picture was off.

### 5. Current correspondence

Koyama’s latest email asked for a brief CV / background summary so he can justify a substantial grant budget in Japan. He specifically asked for:

- degrees
- past affiliations
- specific skills, especially Lean 4 and large-scale parallel computation
- whether Saar can be described as a specialist in formal verification and high-performance number theory

He also said the grant can include a senior-level visiting position and that age is not a blocker. The same message introduced the “Dominance of `-1`” challenge and requested verification over much larger scales and, crucially, dynamic `x` ranges rather than just fixed points.

## Latest Reply

Koyama replied positively to the bugfix-and-recompute update, framed the work as scientifically sound, and explicitly highlighted a linear-in-rank pattern in the current data as an interesting structural observation. He also said the age question is not a problem, that a senior visiting position can be included, and that a brief CV/background summary would help him justify the budget and role description.

He then introduced a new challenge, the "Dominance of -1", asking whether we can help verify it at much larger scales than 13 trillion and, importantly, over dynamic ranges of `x`, not just fixed points.

This reply is now the current correspondence anchor for future drafting.

## Must Correct In V4

- Say V3's rank-only/conductor-light phrasing is superseded.
- Present W2 prime: control tests show conductor matters, and the 22-point fit has a significant log-conductor term.
- Keep the raw Sym2 falsification narrow: it falsifies that exact proportionality, not every completed/Deligne variant.
- Keep Delta separate from EC rank discussion: Delta is a clean `0.950231842` anchor.
- Mention the grant-admin request as part of the current correspondence state: brief CV, affiliations, Lean 4 / parallel compute skills, and visiting-position framing.
- Ask for the precise "Dominance of -1" definition before committing compute, and distinguish fixed-point checks from dynamic-range verification.

## Pending Questions For Koyama

- Exact L-function object: finite `L`, completed `Lambda`, or analytic-conductor ratio?
- Coefficient convention: raw `a_p` or normalized `lambda_f(p)`?
- Archimedean gamma factors for Delta in the proposed Sym2 correction.
- Finite-`K` correction term for exponential smoothing.
- Bad-prime treatment for conductor primes such as 389.
- Exact Dominance-of-minus-one setup: modulus, residue class, fixed or dynamic `x`, and verification script.
- Whether the verification should target the 13 trillion baseline first or jump directly to the next dynamic range.
- Admin: Young Researcher age, city/airport, visiting researcher interest.

## Source Archive

All Koyama material was archived under:

- `raw/farey-archive/correspondence/`
- `raw/farey-archive/state-docs/KOYAMA_*`

Use those sources only for provenance or drafting; the current operational summary is this page plus [[people/shin-ya-koyama]].

## Update Rule

When Saar pastes a new Koyama reply together with the email Saar sent, the first step is to spawn a `gpt-5.4-mini` record-updater subagent to refresh this page, [[people/shin-ya-koyama]], the claim ledger, `log.md`, and the task queue as needed. Keep the refresh lean and do not re-import the full thread.
