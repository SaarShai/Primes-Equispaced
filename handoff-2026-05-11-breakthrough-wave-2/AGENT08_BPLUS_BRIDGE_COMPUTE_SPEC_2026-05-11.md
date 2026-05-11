---
schema_version: 1
title: "Agent 08 - B+ bridge compute implementation spec"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 08"
type: compute-implementation-spec
tier: execution-ready
status: RIGOROUS_REDUCTION
confidence: 0.89
scope: "Tier 1B dense MR-prime bridge 237733 <= p <= 243799"
sources:
  - start.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/HANDOFF.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/BREAKTHROUGH_WAVE_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT08_BPLUS_SIGN_CLUSTER_CLASSIFICATION_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_PROGRAM.md
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_counterexamples.md
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify.c
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify_237733.out
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify_243799.out
tags: [b-plus, sign-cluster, bridge-compute, mertens-restricted, finite-atlas]
---

# Agent 08 - B+ Bridge Compute Implementation Spec

Status enum: `RIGOROUS_REDUCTION`.

## Verdict

Do not run the bridge in this turn.

The next B+ job is a bounded compute classification, not a positivity test:

```text
range_id = tier1B_bridge_237733_243799
237733 <= p <= 243799
p prime
M(p) <= -3
expected MR rows = 468
expected direct workload = 9.94 core-hours
```

Allowed claim after the run: maximal certified `B(p)` sign clusters in
MR-prime order across the bridge.  Forbidden claim: any resurrection of
`B(p)>0`, any use of `T(p-1)` as a sign proxy, or any boundary inferred from
legacy `bprime_*` or sampled Mertens TSVs.

## Canonical Inputs

Use the May 10 Lean-canonical verifier as the source:

```text
primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify.c
```

Clone it only when compute is approved.  The future runner name is fixed here:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE.c
```

The runner must preserve:

```text
N = p - 1
n = |F_N|
rank(0/1) = 1
D_N(a/b) = fareyRank_N(a/b) - n*a/b
sigma_p(a/b) = (p*a mod b)/b
delta_p(a/b) = a/b - sigma_p(a/b)
B(p) = 2 * sum D_N(f) * delta_p(f)
B(p)/2 = B0(N) - Spsi(p)
B0(N) = sum D_N(f) * (f - 1/2)
Spsi(p) = sum D_N(f) * (sigma_p(f) - 1/2)
```

For `B0_stream` and `Spsi_stream`, include the `0/1` boundary explicitly:
`D=1`, `f=0`, `sigma=0`, so both receive `-0.5`.  This preserves canonical
component signs while leaving `B` unchanged.

Required anchors:

| p | M(p) | T(p-1) | `|F_{p-1}|` | B(p) | B/C | class |
|---:|---:|---:|---:|---:|---:|---|
| 237733 | -20 | +6.657511751192 | 17178971883 | -3.018492026640170e10 | -10.543163714952145 | `baseline-fail` |
| 243799 | -3 | -0.834778256610 | 18066862385 | -9.190201299936827e9 | -3.052438040867344 | `sigma-overrun` |

Also reproduce the five small Lean anchors `p in {5,11,13,19,23}` before any
MR-row output is considered valid.

## Exact Command Shape

Build contract:

```bash
cd "/Users/za/Documents/Farey NOW"
cc -O3 -std=c11 -Wall -Wextra -pedantic -march=native -fno-fast-math \
  -DBPLUS_CHUNK_LOG2=20 \
  -o primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute \
  primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE.c \
  -lm
```

Anchor-only run:

```bash
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute \
  --mode anchors \
  --range-id anchors_5_23 \
  --p-list 5,11,13,19,23 \
  --max-p 23 \
  --chunk-log2 20 \
  --rows-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_ANCHOR_ROWS_5_23.tsv \
  --chunks-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_ANCHOR_CHUNKS_5_23.tsv \
  --manifest-json primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_ANCHOR_MANIFEST_5_23.json \
  --quiet
```

Smoke run, still not the bridge:

```bash
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute \
  --mode explicit-primes \
  --range-id smoke_237733_243799 \
  --p-list 237733,243799 \
  --max-p 243799 \
  --mr-threshold -3 \
  --chunk-log2 20 \
  --rows-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_SMOKE_ROWS_237733_243799.tsv \
  --chunks-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_SMOKE_CHUNKS_237733_243799.tsv \
  --manifest-json primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_SMOKE_MANIFEST_237733_243799.json \
  --quiet
```

Bridge shard template, one process per shard:

```bash
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute \
  --mode dense-mr-range \
  --range-id tier1B_bridge_237733_243799 \
  --p-min 237733 \
  --p-max 243799 \
  --mr-threshold -3 \
  --shard-mode mr-contiguous \
  --shard-count 8 \
  --shard-index SHARD_INDEX_0_TO_7 \
  --chunk-log2 20 \
  --rows-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_ROWS_237733_243799.shardSHARD_INDEX_0_TO_7.tsv \
  --chunks-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_CHUNKS_237733_243799.shardSHARD_INDEX_0_TO_7.tsv \
  --manifest-json primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_MANIFEST_237733_243799.shardSHARD_INDEX_0_TO_7.json \
  --quiet
```

Merge command contract:

```bash
python3 primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_MERGE.py \
  --range-id tier1B_bridge_237733_243799 \
  --p-min 237733 \
  --p-max 243799 \
  --mr-threshold -3 \
  --expected-mr-rows 468 \
  --rows-glob 'primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_ROWS_237733_243799.shard*.tsv' \
  --chunks-glob 'primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_CHUNKS_237733_243799.shard*.tsv' \
  --out-rows primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_ROWS_237733_243799.tsv \
  --out-chunks primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_CHUNKS_237733_243799.tsv \
  --out-clusters primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_CLUSTERS_237733_243799.tsv \
  --out-boundaries primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_BOUNDARIES_237733_243799.tsv \
  --out-summary primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_SUMMARY_237733_243799.md \
  --out-manifest primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_MERGED_MANIFEST_237733_243799.json
```

Repeat build contract:

```bash
cd "/Users/za/Documents/Farey NOW"
cc -O1 -std=c11 -Wall -Wextra -pedantic -fno-fast-math -fno-vectorize -fno-slp-vectorize \
  -DBPLUS_CHUNK_LOG2=20 -DBPLUS_REPEAT_STRICT=1 \
  -o primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute_repeat \
  primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE.c \
  -lm
```

Repeat candidate command:

```bash
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_bplus_bridge_compute_repeat \
  --mode explicit-primes \
  --range-id repeat_237733_243799 \
  --p-list REPEAT_P_LIST_COMMA_SEPARATED \
  --max-p 243799 \
  --mr-threshold -3 \
  --chunk-log2 20 \
  --sum-order reverse-chunks \
  --rows-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_REPEAT_ROWS_237733_243799.tsv \
  --chunks-tsv primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_REPEAT_CHUNKS_237733_243799.tsv \
  --manifest-json primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/BPLUS_BRIDGE_REPEAT_MANIFEST_237733_243799.json \
  --quiet
```

## Future File Outputs

Bridge outputs:

```text
BPLUS_BRIDGE_ROWS_237733_243799.tsv
BPLUS_BRIDGE_CHUNKS_237733_243799.tsv
BPLUS_BRIDGE_CLUSTERS_237733_243799.tsv
BPLUS_BRIDGE_BOUNDARIES_237733_243799.tsv
BPLUS_BRIDGE_SUMMARY_237733_243799.md
BPLUS_BRIDGE_MERGED_MANIFEST_237733_243799.json
```

Repeat outputs:

```text
BPLUS_BRIDGE_REPEAT_ROWS_237733_243799.tsv
BPLUS_BRIDGE_REPEAT_CHUNKS_237733_243799.tsv
BPLUS_BRIDGE_REPEAT_MANIFEST_237733_243799.json
BPLUS_BRIDGE_REPEAT_DIFF_237733_243799.tsv
```

Every TSV must be UTF-8, tab-delimited, one header row, `\n` line endings,
decimal floats printed with at least `%.18Le` internally converted text or a
lossless enough string for `long double` review.  Missing values use `NA`.

## Row TSV Schema

Exact column order:

```text
range_id
run_id
shard_index
p
N
prime_index_global
mr_index_range
M_p
M_N
M_band
T_N
T_sign
farey_size_n
farey_processed
B
C_shift_sq
B_over_C
B0_stream
B0_sign
Spsi_stream
Spsi_sign
margin_B0_minus_Spsi
B_from_decomp
B_recombine_error
B_chunk_forward
B_chunk_reverse
B_chunk_pairwise
B_chunk_order_error
B0_chunk_order_error
Spsi_chunk_order_error
sum_delta
sum_D
B_abs_term_sum
B0_abs_term_sum
Spsi_abs_term_sum
eps_B
eps_0
eps_final
B_sign
overrun_flag
class_primary
class_refined
cert_level
cert_status
elapsed_seconds
source_sha256
git_head
git_dirty
compiler_id
compiler_flags
host_id
```

Definitions:

| column | definition |
|---|---|
| `prime_index_global` | 1-based prime index of `p` among all primes. |
| `mr_index_range` | 1-based index among dense rows with `p_min <= p <= p_max`, `p prime`, `M(p)<=-3`. |
| `M_band` | `edge-MR` if `M_p=-3`; `shallow-MR` if `-9<=M_p<=-4`; `deep-MR` if `M_p<=-10`. |
| `T_sign` | `pos`, `neg`, or `zero` from `T_N`. |
| `farey_processed` | must equal `farey_size_n`; includes explicit `0/1` boundary plus traversal through `1/1`. |
| `C_shift_sq` | `sum delta_p(f)^2`; includes `1/1`, excludes no nonzero B term. |
| `B_from_decomp` | `2*(B0_stream-Spsi_stream)`. |
| `B_recombine_error` | `B-B_from_decomp`. |
| `B_chunk_order_error` | max absolute disagreement among forward, reverse, pairwise chunk recombinations and direct `B`. |
| `B0_chunk_order_error` | same chunk-order disagreement test applied to `B0_stream`. |
| `Spsi_chunk_order_error` | same chunk-order disagreement test applied to `Spsi_stream`. |
| `overrun_flag` | `true` iff `Spsi_stream > B0_stream`. |
| `B_sign` | `pos`, `neg`, `zero`, or `borderline`. |
| `cert_level` | `anchor`, `float-wide`, `repeat`, `borderline`, or `failed`. |
| `cert_status` | `ok`, `needs-repeat`, `invalid`, or `excluded`. |

Primary classes:

| class | condition |
|---|---|
| `ordinary-pos` | `B>0`, `T<0` |
| `rescued-pos` | `B>0`, `T>0` |
| `baseline-fail` | `B<0`, `T>0` |
| `sigma-overrun` | `B<0`, `T<0` |
| `borderline` | uncertified `B` sign |

Refined class key:

```text
(B_sign,T_sign,B0_sign,Spsi_sign,overrun_flag,M_band)
```

## Chunk TSV Schema

Emit one chunk row per `2^20` Farey rows per prime, plus a final short chunk.
Exact column order:

```text
range_id
run_id
shard_index
p
N
mr_index_range
chunk_log2
chunk_index
rank_start
rank_end
farey_rows_in_chunk
B_partial
C_partial
B0_partial
Spsi_partial
sum_delta_partial
sum_D_partial
B_abs_term_sum_partial
B0_abs_term_sum_partial
Spsi_abs_term_sum_partial
first_fraction
last_fraction
chunk_elapsed_seconds
chunk_order_hash
```

Rules:

- `rank_start` and `rank_end` are inclusive Lean ranks.
- `chunk_order_hash` hashes `(p,chunk_index,rank_start,rank_end,first_fraction,last_fraction)`.
- Merge must reject duplicate chunks, rank gaps, rank overlaps, or chunks whose
  partials do not reproduce the row-level forward recombination.
- Chunk partials are diagnostic and certification data, not cluster rows.

## Cluster TSV Schema

Primary clusters are maximal consecutive runs in MR-prime order with the same
certified `B_sign`.  Exact column order:

```text
range_id
cluster_id
B_sign
cluster_status
start_p
end_p
start_mr_index
end_mr_index
mr_count
ambient_prime_count
width
min_B
max_B
min_B_over_C
max_B_over_C
T_pos_count
T_neg_count
T_zero_count
B0_pos_count
B0_neg_count
B0_zero_count
Spsi_pos_count
Spsi_neg_count
Spsi_zero_count
M_min
M_max
M_band_histogram
class_primary_histogram
class_refined_histogram
boundary_left_cert
boundary_right_cert
representative_p_min_abs_B_over_C
representative_p_max_abs_B_over_C
cert_level_min
repeat_rows_required
```

`cluster_status` enum:

```text
certified
certified-repeat
interior-only
blocked-by-borderline
invalid
```

Boundary rule: a cluster boundary is claimable only when the last MR row
before the boundary and the first MR row after it both have certified,
non-borderline `B_sign`.  If either side is borderline, emit certified
interior segments plus an unresolved boundary gap.

## Boundary TSV Schema

Exact column order:

```text
range_id
boundary_id
left_cluster_id
right_cluster_id
left_p
right_p
left_mr_index
right_mr_index
left_B_sign
right_B_sign
left_cert_level
right_cert_level
left_abs_B_over_C
right_abs_B_over_C
repeat_required
boundary_status
notes
```

`boundary_status` enum:

```text
certified
repeat-required
blocked-by-borderline
invalid
```

## Summary Markdown Schema

`BPLUS_BRIDGE_SUMMARY_237733_243799.md` must contain these sections, in this
order:

```text
frontmatter with status enum
# B+ Bridge Summary 237733-243799
## Verdict
## Command Provenance
## Anchor Reproduction
## Range Inventory
## Runtime Accounting
## Cluster Table
## Boundary Table
## Repeat Certification
## Decoupling Diagnostics
## No-Promotion Boundary
## Output Files
## Changed Files
```

The summary verdict must answer only:

```text
Do 237733 and 243799 lie in the same certified negative MR-order B cluster?
If not, what certified clusters and unresolved gaps separate them?
```

## Certification Policy

Use compensated `long double` sums for:

```text
B
C_shift_sq
B0_stream
Spsi_stream
sum_delta
sum_D
B_abs_term_sum
B0_abs_term_sum
Spsi_abs_term_sum
```

For each row:

```text
eps_B = 64*LDBL_EPSILON*B_abs_term_sum
        + abs(B_recombine_error)
        + B_chunk_order_error

eps_0 = 64*LDBL_EPSILON*max(B0_abs_term_sum,Spsi_abs_term_sum)
        + max(B0_chunk_order_error,Spsi_chunk_order_error)

eps_final = max(eps_B, 2*eps_0)
```

`float-wide` requires all conditions:

```text
five small Lean anchors reproduced in the same binary;
farey_processed == farey_size_n;
abs(B) > 100*eps_final;
sign(B) == sign(B_from_decomp);
sign(B_chunk_forward) == sign(B_chunk_reverse) == sign(B_chunk_pairwise);
abs(sum_delta - 1) <= 1000*LDBL_EPSILON*farey_size_n;
M_p <= -3 and p is prime by internal sieve.
```

`repeat` requires `float-wide` plus strict repeat agreement on:

```text
B_sign
class_primary
overrun_flag
boundary role, if any
```

Rows become repeat candidates when any condition holds:

```text
row is 237733 or 243799;
row touches a proposed cluster boundary;
row is a one-row island;
abs(B/C_shift_sq) < 0.05;
abs(B) <= 1000*eps_final;
class_primary changes across either MR neighbor;
chunk_order_error > 0.01*abs(B);
```

Rows become `borderline` when:

```text
abs(B) <= 100*eps_final;
decomposition sign disagrees with direct sign;
chunk-order signs disagree;
repeat sign disagrees;
internal sieve or Farey row count fails.
```

No cluster boundary may use a `borderline` row.

## Runtime Split

Expected rate comes from the canonical verifier outputs: around `75-79`
seconds for one `p ~= 240k` row with `~1.7e10-1.8e10` Farey rows.

| stage | range | rows | estimate | claim allowed |
|---|---:|---:|---:|---|
| anchors | `{5,11,13,19,23}` | 5 tiny | seconds | implementation sanity only |
| smoke | `{237733,243799}` | 2 | about 3 core-min; budget 5 | anchor reproduction only |
| local-left | `237733` through next 20 MR rows | 21 | about 0.45 core-hours | local persistence only |
| local-right | previous 20 MR rows through `243799` | 21 | about 0.45 core-hours | local persistence only |
| tier 1A windows | packet windows near both anchors | 48 | 1.02 core-hours | local island probes only |
| tier 1B bridge | `237733 <= p <= 243799` dense MR rows | 468 | 9.94 core-hours | bridge cluster theorem |
| repeat pack | boundary/island/borderline candidates | variable | pre-budget 10-25% of bridge | certification upgrade |

Wall-clock planning for tier 1B:

```text
1 worker:  ~10 hours plus merge
4 workers: ~2.5 hours plus stragglers
8 workers: ~1.25 hours plus stragglers
12 workers: ~50 minutes plus stragglers
```

Use 8 shards by default.  Use 12 only if the machine is otherwise idle and
thermal throttling is not a concern.  Do not parallelize inside one Farey
traversal until row, chunk, and repeat formats are stable.

Stop immediately if anchors fail, if the dense MR count differs from `468`, or
if either endpoint anchor loses its large negative sign.

## Verification Notes

Read targeted context only.  No expensive compute was run.  The current
`B_plus_direct_verify.c` is anchor-valid but does not yet emit the bridge
TSV/chunk schemas; this document specifies the future runner contract.

The existing anchor outputs confirm:

```text
p=237733: B=-3.018492026640170e10, B/C=-10.543163714952145
p=243799: B=-9.190201299936827e9, B/C=-3.052438040867344
```

No Koyama correspondence or email draft was read for content or edited.

## Changed Files

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT08_BPLUS_BRIDGE_COMPUTE_SPEC_2026-05-11.md
```
