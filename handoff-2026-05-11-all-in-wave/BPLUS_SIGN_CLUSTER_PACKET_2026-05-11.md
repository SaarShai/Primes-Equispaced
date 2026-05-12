---
schema_version: 1
title: "B+ MR-prime sign-cluster packet"
date: 2026-05-11
worker: "E"
type: handoff
tier: working
status: BOUNDED_PLAN
confidence: 0.86
tags: [b-plus, sign-cluster, mertens-restricted, atlas, bounded-compute]
---

# B+ Sign-Cluster Packet

## Outcome

No theorem is promoted.

The useful target remains finite classification of Lean-canonical
`B(p)` on MR primes, not positivity.  The minimum honest extension is not
the full `p <= 1e6` atlas.  It is a dense, canonical rerun around the known
negative anchors:

| tier | range | MR rows | T-positive rows | T-negative rows | estimated core-hours | claim allowed |
|---|---:|---:|---:|---:|---:|---|
| 1A-local | `237700 <= p <= 237999` and `243500 <= p <= 244000` | 48 | 24 | 24 | 1.02 | local persistence/island probes only |
| 1B-bridge | `237733 <= p <= 243799` | 468 | 76 | 392 | 9.94 | whether the two canonical negatives lie in one MR-order sign run or split |
| 1C-first-transition | `100003 <= p <= 300000` | 8351 | 85 | 8266 | 128.45 | finite first-transition atlas through 300K |
| defer | `565000 <= p <= 573000` | 193 | 124 | 69 | 23.06 | recurrence probe after tier 1C, not first |

Recommended minimum: **tier 1B**.  Tier 1A is cheap but can only add two
local windows; it cannot answer the cluster-contiguity question between
`p=237733` and `p=243799`.  Tier 1C is the first range that can support a
"first post-99991 transition atlas" claim, but it is a larger compute job.

The T-sign counts above are only sizing data.  They are not B-sign evidence.
`p=243799` already proves `T(p-1)<0` is not a B-sign proxy.

## Current Anchors

Canonical direct verifier anchors:

| p | M(p) | T(p-1) | `|F_{p-1}|` | B(p) | B/C | class |
|---:|---:|---:|---:|---:|---:|---|
| 237733 | -20 | +6.657511751192 | 17178971883 | -3.018492026640170e10 | -10.543163714952145 | baseline-fail |
| 243799 | -3 | -0.834778256610 | 18066862385 | -9.190201299936827e9 | -3.052438040867344 | sigma-overrun |

Legacy March scan also reports a nearby candidate negative:
`p=243703`, `M(p)=-3`, `B/C=-0.562957`, with positives at
`p=243613` and `p=244507`.  Do not promote this as an atlas boundary until
rerun through the May 10 canonical verifier and dense MR-neighbor rows.

## Sources / Paths

- `HANDOFF.md`: current project state; B+ positivity is false and the target is sign-cluster classification.
- `L2_facts/farey-claim-ledger.md`: supersession ledger; B+ cluster program is open, T alone is not a sign proxy.
- `handoff-2026-05-09-followup/B_plus_direct_counterexamples.md`: canonical counterexamples at `237733` and `243799`.
- `handoff-2026-05-09-followup/B_plus_direct_verify.c`: current canonical streaming verifier.
- `handoff-2026-05-09-followup/B_plus_direct_verify_237733.out`: canonical row for `237733`.
- `handoff-2026-05-09-followup/B_plus_direct_verify_243799.out`: canonical row for `243799`.
- `handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_PROGRAM.md`: prior cluster-program packet and TSV schema.
- `handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md`: sampled MR T-flip disproof; not dense enough for B cluster boundaries.
- `handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.md`: post-99991 T-transition mechanism.
- `experiments/B_VERIFY_243799.md` and `experiments/bprime_200k_scan_output.txt`: legacy March scan; useful candidates, lower authority than canonical verifier.

No Koyama email or correspondence draft was edited.

## Tier-1 Sweep Plan

Use a new runner in a later pass, cloned from
`handoff-2026-05-09-followup/B_plus_direct_verify.c`, not from older
`bprime_*` experiments.

Required behavior:

1. Preserve the five Lean anchor checks `p in {5,11,13,19,23}`.
2. Generate dense MR primes from an internal prime/Mobius sieve, not from
   `MERTENS_LB_MR_verification.tsv`.
3. Stream all Farey rows for each selected prime using the Lean rank convention
   `rank(0/1)=1`.
4. Accumulate, with compensated `long double` sums:
   `B`, `C`, `B0_stream`, `Spsi_stream`, `sum_delta`, `sum_D`.
5. Emit one TSV row per MR prime:
   `range_id,p,N,mr_index,M_p,T_N,T_sign,farey_size_n,B,C,B_over_C,B0_stream,Spsi_stream,B_recombine_error,B_sign,cert_level,elapsed_seconds,source_sha,compiler_flags`.
6. Emit one cluster TSV after rows finish:
   maximal consecutive MR-prime runs by certified `B_sign`, with T-sign
   histogram and min/max `B/C`.
7. Mark any row with small `abs(B)` or large recombination error as
   `borderline`; do not use it for a boundary.

Suggested execution order:

| step | command target | accept/reject |
|---|---|---|
| smoke | anchors plus `237733,243799` | must reproduce signs and large margins |
| 1A | `237700-237999`, `243500-244000` | local window report only |
| 1B | `237733-243799` | bridge cluster report |
| 1C | `100003-300000` | first-transition finite atlas |

Parallelize over prime chunks, not inside one Farey traversal.  Use the
observed canonical rate of about `230M` Farey rows/sec/core for estimates.
For tier 1C the exact summed workload over dense MR rows is
`106360431082785` Farey rows, about `128.45` core-hours.

## Verification

Read required files and cluster notes listed above.

Checked current working tree status before writing.  The tree already had
many concurrent modified/untracked files, including Koyama correspondence
material.  I did not revert or edit them.

Ran a read-only/in-memory sizing pass:

- dense MR count and T-sign counts for the proposed ranges;
- exact `|F_{p-1}|` workload sums for compute estimates;
- no TSV, binary, or log file was created.

Project-local `../te doctor` from `primes-equispaced` reports missing
project-local `start.md` and `token-economy.yaml`, but the requested handoff
and ledger files are present and were used as source of truth.

## Confidence

Aggregate confidence: **0.86**.

- `0.98` for the two canonical negative anchors, inherited from the direct
  counterexample packet and reproduced output files.
- `0.95` for MR row counts and compute estimates: generated by an in-memory
  Mobius/prime/phi sieve and exact Farey-size prefix sums to `600000`.
- `0.80` for the recommended tier split: it depends on the current verifier
  speed and assumes no closed form for `B(p)` is introduced before the sweep.
- `0.65` for the legacy `p=243703` candidate as a boundary clue only; it
  predates the May 10 canonical packaging, though `p=243799` matched later.

## Changed Files

- `handoff-2026-05-11-all-in-wave/BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md`

## Risks

- Direct Farey streaming is expensive.  Full `100003-300000` dense tier 1C is
  bounded but not tiny.
- T-sign clusters can mislead.  They size the computation and classify rows
  after B is known; they do not predict B.
- Legacy `bprime_*` scans are useful for candidate selection but must not set
  final boundaries.
- Floating summation remains a residual risk for borderline rows.  Large
  negative margins at `237733` and `243799` are safe; small `B/C` rows need
  repeat or altered-order certification.
- If concurrent workers add a closed-form `B0/Spsi` evaluator, this plan
  should be revised before spending tier 1C compute.
