---
schema_version: 2
title: Koyama Correspondence
type: project
domain: project
tier: semantic
confidence: 0.98
created: 2026-04-24
updated: 2026-05-11
verified: 2026-05-11
sources:
  - raw/farey-archive/correspondence/koyama-gmail-record-2026-05-11.md
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

Prof. Shin-ya Koyama is an active collaborator/contact. Gmail was searched on 2026-05-11 for direct correspondence with `koyama@tmtv.ne.jp`: 54 messages were found across 3 Gmail threads. No direct messages were found for `koyama@toyo.jp`.

The complete message-level Gmail record is now `raw/farey-archive/correspondence/koyama-gmail-record-2026-05-11.md`.

The working record spans:

- opening DRH / Farey spectroscope contact;
- weighted prime-bias / DPAC / EDRH / NDC;
- GL(2), elliptic-curve, C1, rank/conductor, and Delta;
- Dominance-of-`-1`;
- CREST role/budget/application materials;
- Stage-1 Dominance replication and bundle delivery.

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

### 5. Dominance-of-`-1` / CREST phase

- Koyama opened a new Gmail thread on 2026-04-26 with draft `nontriv.pdf`, clarified the Dominance-of-`-1` target, and asked for replication at `10^12` and `13*10^12`, then dynamic extension toward `10^14` or `3*10^14`.
- Saar replied with a two-stage replication/dynamic-extension plan, residue-class caution, reproducibility architecture, applied/social-impact draft, and 12M JPY/year role/budget structure.
- Koyama accepted the 12M JPY/year structure and the "Strategic Research Architect" role title.
- Koyama gave the team list and `koyama@toyo.jp`, but Gmail search found no direct messages to/from that address.
- Koyama requested a Post-Bias Cryptographic Framework, Lean 4 lattice-crypto memo, and Stage-1 replication evidence for the CREST proposal.

### 6. Stage-1 replication / latest state

- Saar sent the Lean 4 memo, then a replication report for Tables 3-7, then a proposal-ready executive one-pager, then the full replication bundle.
- Koyama said the report was a "masterpiece", asked for the bundle as zip/download link, and said the independent-implementation and identity-verification evidence would help CREST feasibility.
- Latest incoming from Koyama: 2026-05-04 19:46:20 +09:00, Gmail message `19df298d07b5d137`.
  - Koyama received the full bundle.
  - He thanked Saar for the professional/comprehensive packaging.
  - He said the reproducibility manifest is a powerful evidence-base addition.
  - He will focus on integrating final proposal parts with Prof. Aoki's team.
  - He will get back after the deadline.
- Latest outgoing from Saar: 2026-05-04 17:45:18 +01:00, Gmail message `19df3e1408b7bfe5`: "Best of luck. Looking forward to updates."

## Latest Correspondence Anchor

Current anchor: Koyama has the full replication bundle and is integrating it into the CREST proposal with Prof. Aoki's team. Wait for his post-deadline update. Table-discrepancy review is deferred until after the Kiban-S deadline on 2026-05-20.

## Must Correct In V4

- Say V3's rank-only/conductor-light phrasing is superseded.
- Present W2 prime: control tests show conductor matters, and the 22-point fit has a significant log-conductor term.
- Keep the raw Sym2 falsification narrow: it falsifies that exact proportionality, not every completed/Deligne variant.
- Keep Delta separate from EC rank discussion: Delta is a clean `0.950231842` anchor.
- Mention that the grant-admin/CV request was answered in the 2026-04-25 email, and that Koyama accepted the 12M JPY/year structure plus "Strategic Research Architect" title on 2026-04-27.
- For Dominance-of-`-1`, distinguish:
  - proposal-ready headline replication evidence already sent;
  - table discrepancies deferred until after 2026-05-20;
  - dynamic extension toward `10^14` / `3*10^14` not yet completed in the Gmail record.

## Pending Questions For Koyama

- Exact L-function object: finite `L`, completed `Lambda`, or analytic-conductor ratio?
- Coefficient convention: raw `a_p` or normalized `lambda_f(p)`?
- Archimedean gamma factors for Delta in the proposed Sym2 correction.
- Finite-`K` correction term for exponential smoothing.
- Bad-prime treatment for conductor primes such as 389.
- Post-2026-05-20 review of the table discrepancies flagged in Saar's replication report.
- Whether the next Dominance run should target `10^14` or `3*10^14`, and on what dynamic grid.
- Whether Koyama wants more CREST proposal text after the internal 2026-05-11 deadline.

## Source Archive

Gmail-derived record now archived under:

- `raw/farey-archive/correspondence/`

Key file: `raw/farey-archive/correspondence/koyama-gmail-record-2026-05-11.md`.

Older state-doc references remain useful as local drafting provenance, but the Gmail record supersedes the previous April-only correspondence summary.

## Update Rule

When Saar pastes a new Koyama reply together with the email Saar sent, the first step is to spawn a `gpt-5.4-mini` record-updater subagent to refresh this page, [[people/shin-ya-koyama]], the claim ledger, `log.md`, and the task queue as needed. Keep the refresh lean and do not re-import the full thread.
