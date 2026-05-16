# formal-conjectures PR — readiness package + HONEST verdict (2026-05-16)

User authorized the PR. This documents (a) why I did **not** auto-submit
(hard blockers + an honest fit problem — submitting as-is would be the
project's #1 failure mode, inflation, in a high-visibility Google repo under
the user's name), (b) what is genuinely contributable, (c) the exact steps
only the user can take.

## A. HONEST FIT VERDICT — do not submit the current artifact as a "theorem"

`primes-equispaced/formal-conjectures/FareySignPattern.lean`, read in full:
- The **pointwise** Sign Theorem `sgn(ΔW(p))=sgn(−M(p))` is **FALSIFIED**
  (the file itself records counterexamples p=237733, p=243799).
- The surviving **density-one** statement is **research-open**, and its Lean
  encoding is a **vacuous tautology** `theorem … (h_chebyshev_bias : P) : P
  := h_chebyshev_bias`, with `opaque DeltaW : ℕ → ℝ` (no definition — Farey
  discrepancy is not in Mathlib). A conjecture stated against an `opaque`
  symbol has **no mathematical content** and would (correctly) be rejected by
  formal-conjectures maintainers.
- The "0 sorries / 0 axioms" Lean artifact referenced elsewhere in the
  project is a **different** file (`SignedVsAbsoluteResidueGadget.lean`, the
  Palm-wall two-zero gadget) — NOT the Sign Theorem.

**Verdict: there is no clean proven "Lean Sign Theorem" to contribute.** The
only legitimately contributable item is the **density-one Farey sign
conjecture as an `@[category research open]` conjecture** — and only if it is
(i) restated properly (not the tautology) and (ii) given a *concrete* Lean
definition of the Farey set and its Weyl/L² discrepancy `W(F_N)` so the
statement is meaningful. (ii) is real Mathlib-grade work, **not done**, and is
the actual prerequisite for a credible PR.

## B. HARD BLOCKERS (independent of fit; cannot be done from this machine)

1. **`gh` not installed; no GitHub auth/token present.** Cannot fork, push,
   or open an issue/PR autonomously. (Verified: `gh` command not found.)
2. **Google CLA** must be signed by **you personally** at
   https://cla.developers.google.com/ (legal act; non-delegable). Mandatory
   before any google-deepmind PR is accepted.
3. **Issue-first policy:** formal-conjectures requires opening a GitHub issue
   describing the contribution *before* the PR.

## C. RECOMMENDATION (honest)

**Do not PR the current state.** Options, best→worst:
1. **Hold.** The Sign Theorem is dictionary-tier and the pointwise form is
   falsified; the density-one form is an open conjecture with no concrete Lean
   `ΔW`. Low payoff for the effort + reputational cost of a thin Google PR.
2. **Invest first, then PR.** Formalize the Farey sequence + Weyl L²
   discrepancy `W(F_N)` + `ΔW(p)` concretely in Lean (real work; a genuine
   Mathlib-adjacent contribution in its own right), then submit the
   density-one statement as a proper `@[category research open]` conjecture.
   This is the only path to a *credible* PR.
3. A different, genuinely-clean project result might fit better as
   `@[category research solved]` (e.g. the Bridge Identity
   `Σ_{f∈F_{p−1}} e(pf)=M(p)+2`, IF `FareyBridgeIdentity.lean` actually
   proves it with a <50-line proof — **must be verified first**, not assumed;
   same inflation risk applies).

My recommendation: **option 1 or 2**, your call. Not a quick win; the earlier
"Lean-verified Sign Theorem, ready to PR" framing was over-optimistic and is
corrected here.

## D. EXACT STEPS (if you choose to proceed — only you can do these)

1. Sign the Google CLA: https://cla.developers.google.com/ (once per
   person/employer).
2. Install + auth GitHub CLI: `brew install gh && gh auth login`.
3. Decide fit per §C. If proceeding, first produce a **build-verified** Lean
   file with a concrete `W(F_N)`/`ΔW` (NOT `opaque`) — I can draft this on
   request but it MUST pass `lake build` before PR (I cannot run their build
   here).
4. Open the issue (draft text below), fork, branch, add file under
   `FormalConjectures/Arxiv/` (source = the project's arXiv note once posted)
   or `FormalConjectures/Other/`, `lake build`, PR linked to the issue.

### Ready-to-paste GitHub ISSUE (use only after §C decision + a real statement)
> **Title:** Formalize: density-one Farey discrepancy sign pattern (open conjecture)
>
> **Body:** Proposing an `@[category research open, AMS 11]` conjecture: as
> X→∞, the proportion of primes p ≤ X with Mertens M(p) ≤ −3 for which
> sgn(ΔW(p)) = sgn(−M(p)) tends to 1, where W(F_N) is the L² (Weyl)
> discrepancy of the order-N Farey sequence and ΔW(p)=W(F_{p−1})−W(F_p). The
> pointwise form is *false* (explicit counterexamples); the density-one form
> is the surviving conjecture (numerically ≈73% at X=10⁷; full density-one
> conjectured under the relevant L-function hypotheses). Supporting Farey/
> discrepancy definitions would go in `FormalConjecturesForMathlib`. Source:
> S. Shai, per-step Farey discrepancy note (arXiv: TBD). Requesting guidance
> on whether a concrete in-repo Farey-discrepancy definition is acceptable
> vs. waiting for a Mathlib Farey API.

### PR body skeleton
> Implements the issue #NN conjecture. `@[category research open, AMS 11]`,
> Apache header, reference link, `by sorry`. Concrete `W`/`ΔW` defs in a
> separate `FormalConjecturesForMathlib` file, indexed. `lake build` green.
> CLA signed.

## E. What I DID lock this session (the other authorized task)

KR citation: **LOCKED from primary** (ar5iv + arXiv abstract) — see
`KR_CITATION_LOCK.md`. That BLOCKED-FOR-USER item is resolved (modulo one
soft theorem-number). This formal-conjectures item remains **user-gated** by
the CLA + the honest fit decision above; nothing was submitted.
