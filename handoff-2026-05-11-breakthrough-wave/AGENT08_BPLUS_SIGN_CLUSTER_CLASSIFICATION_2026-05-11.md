---
schema_version: 1
title: "Agent 08 - B+ sign-cluster classification"
date: 2026-05-11
agent: "Agent 08"
type: classification-protocol
tier: claim-safe
status: RIGOROUS_REDUCTION
confidence: 0.87
scope: "Dense MR-prime bridge 237733 <= p <= 243799"
sources:
  - start.md
  - L1_index.md
  - primes-equispaced/L1_index.md
  - primes-equispaced/HANDOFF.md
  - primes-equispaced/handoff-2026-05-11/HANDOFF.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-all-in-wave/NEW_SESSION_HANDOFF_PROMPT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_PROGRAM.md
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_counterexamples.md
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify.c
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify_237733.out
  - primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify_243799.out
  - primes-equispaced/handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md
  - primes-equispaced/handoff-2026-05-09-followup/MERTENS_LB_phase_transition_probe_2026-05-11.py
tags: [b-plus, sign-cluster, mertens-restricted, finite-atlas, farey]
---

# Agent 08 - B+ Sign-Cluster Classification

Status enum: `RIGOROUS_REDUCTION`.

## Verdict

No positivity theorem is alive.  The only claim-safe next result is finite
classification of Lean-canonical `B(p)` on dense MR primes.

Recommended bridge:

```text
237733 <= p <= 243799
p prime
M(p) <= -3
```

Known sizing from the all-in packet:

| range | MR rows | T>0 | T<0 | estimated core-hours |
|---|---:|---:|---:|---:|
| `237733-243799` | 468 | 76 | 392 | 9.94 |

The bridge answers one bounded question: do the two canonical negative
anchors lie in one MR-order negative `B` run, or do they split into multiple
negative islands separated by positive MR rows?

## Non-Negotiable Anchors

Use Lean-canonical normalization:

```text
N = p - 1
n = |F_N|
D_N(a/b) = fareyRank_N(a/b) - n*a/b
sigma_p(a/b) = (p*a mod b)/b
delta_p(a/b) = a/b - sigma_p(a/b)
B(p) = 2 sum_{a/b in F_N} D_N(a/b) delta_p(a/b)
B(p)/2 = B0(N) - Spsi(p)
B0(N) = sum D_N(f)(f - 1/2)
Spsi(p) = sum D_N(f)(sigma_p(f) - 1/2)
```

Canonical negatives:

| p | M(p) | T(p-1) | `|F_{p-1}|` | B(p) | B/C | label |
|---:|---:|---:|---:|---:|---:|---|
| 237733 | -20 | +6.657511751192 | 17178971883 | -3.018492026640170e10 | -10.543163714952145 | `baseline-fail` |
| 243799 | -3 | -0.834778256610 | 18066862385 | -9.190201299936827e9 | -3.052438040867344 | `sigma-overrun` |

`T(p-1)` is not a sign proxy.  It is row metadata.

## Row Protocol

Future runner: clone
`primes-equispaced/handoff-2026-05-09-followup/B_plus_direct_verify.c`
to an `AGENT08_` helper only when compute is approved.  Do not use legacy
`bprime_*` outputs for boundaries.

Required runner behavior:

1. Preserve the five Lean anchors `p in {5,11,13,19,23}`.
2. Sieve primes, `mu`, `M`, `phi`, and Farey-size prefix internally through
   `243799`.
3. Generate dense MR rows by `is_prime[p] && M[p] <= -3`; do not sample and
   do not import `MERTENS_LB_MR_verification.tsv` as a boundary source.
4. For each selected `p`, stream all `F_{p-1}` rows in the existing Farey
   traversal with `rank(0/1)=1`.
5. Accumulate with `long double` and Neumaier/Kahan compensation:
   `B`, `C`, `B0_stream`, `Spsi_stream`, `sum_delta`, `sum_D`,
   `abs_B_terms`, `abs_B0_terms`, `abs_Spsi_terms`.
6. Also store chunk partials every `2^20` Farey rows; recombine forward,
   reverse, and pairwise for repeatable summation-order checks.
7. Emit one TSV row per MR prime.

Row TSV schema:

```text
range_id
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
B
C_shift_sq
B_over_C
B0_stream
B0_sign
Spsi_stream
Spsi_sign
margin_B0_minus_Spsi
B_recombine_error
sum_delta
sum_D
B_abs_term_sum
B0_abs_term_sum
Spsi_abs_term_sum
B_sign
overrun_flag
class_primary
class_refined
cert_level
elapsed_seconds
source_sha
compiler_flags
```

Compute:

```text
B_recombine_error = B - 2*(B0_stream - Spsi_stream)
overrun_flag = Spsi_stream > B0_stream
```

The row is internally coherent only if `B_sign` agrees with
`sign(B0_stream - Spsi_stream)`.

## Cluster Protocol

Primary clusters are maximal consecutive runs in MR-prime order with the same
certified `B_sign`.

Cluster TSV schema:

```text
range_id
cluster_id
B_sign
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
B0_pos_count
B0_neg_count
Spsi_pos_count
Spsi_neg_count
M_min
M_max
M_band_histogram
class_histogram
boundary_left_cert
boundary_right_cert
representative_p_min_abs_B_over_C
representative_p_max_abs_B_over_C
cert_level_min
```

Boundary rule:

```text
A cluster boundary is claimable only when the last MR row before it and the
first MR row after it both have certified, non-borderline B signs.
```

If either side is borderline, split the output into certified interior
segments plus an unresolved boundary gap.  Do not infer through the gap.

## Taxonomy

Primary labels:

| label | condition |
|---|---|
| `ordinary-pos` | `B>0`, `T<0` |
| `rescued-pos` | `B>0`, `T>0` |
| `baseline-fail` | `B<0`, `T>0` |
| `sigma-overrun` | `B<0`, `T<0` |
| `borderline` | uncertified `B` sign |

Refined labels use the full key:

```text
(B_sign, T_sign, B0_sign, Spsi_sign, overrun_flag, M_band)
```

with `M_band`:

| M band | condition | purpose |
|---|---|---|
| `edge-MR` | `M(p) = -3` | tests whether the MR threshold itself can host negatives |
| `shallow-MR` | `-9 <= M(p) <= -4` | ordinary negative-Mertens rows |
| `deep-MR` | `M(p) <= -10` | strong Mertens negativity, includes `237733` |

Refined class examples:

| refined class | condition | interpretation |
|---|---|---|
| `B0-pos-contained` | `B>0`, `B0>0`, `Spsi<B0` | favorable baseline survives covariance |
| `B0-pos-overrun` | `B<0`, `B0>0`, `Spsi>B0` | clean covariance overrun; expected near `243799` |
| `B0-neg-unrescued` | `B<0`, `B0<=0` | baseline already bad or weak |
| `B0-neg-rescued` | `B>0`, `B0<=0`, `Spsi<B0` | covariance rescues a bad baseline |
| `M-edge-overrun` | `M=-3`, `B<0`, `Spsi>B0` | threshold-row negative island |

## Certification

Let

```text
epsB = 64*LDBL_EPSILON*B_abs_term_sum + abs(B_recombine_error)
eps0 = 64*LDBL_EPSILON*max(B0_abs_term_sum,Spsi_abs_term_sum)
eps = max(epsB, 2*eps0)
```

Certification levels:

| level | requirement |
|---|---|
| `anchor` | five Lean anchors reproduced |
| `float-wide` | `abs(B) > 100*eps`, recombination sign agrees, and chunk-order recombinations agree |
| `repeat` | `float-wide` plus second compiler/flags run agrees on `B_sign` and `class_primary` |
| `borderline` | sign fails the `float-wide` margin or recombination agreement |

Minimum for bridge cluster claims: `anchor + float-wide`.

Minimum for any surprising isolated sign flip or one-row island: `repeat`.

Rows with `abs(B/C) < 0.05` should be predeclared as repeat candidates even
if the `eps` test passes.  They may be real, but they are bad boundary
witnesses until repeated.

## Execution Order

Do not launch this in the current Agent 08 turn.  When compute is approved:

```text
smoke: anchors + 237733 + 243799
local-left: 237733 through the next 20 MR rows
local-right: previous 20 MR rows through 243799
bridge: all 468 MR rows in 237733-243799
```

Parallelize over primes/chunks at the process level.  Do not parallelize
inside one Farey traversal until the row format and chunk-order certification
are stable.

Expected bridge outputs:

```text
AGENT08_BPLUS_CLUSTER_ROWS_237733_243799.tsv
AGENT08_BPLUS_CLUSTER_SUMMARY_237733_243799.md
AGENT08_BPLUS_CLUSTER_BOUNDARIES_237733_243799.tsv
```

These are future outputs, not created here.

## Theorem Questions

Q1. Finite bridge theorem:

```text
Among all MR primes 237733 <= p <= 243799, what are the maximal certified
B-sign clusters?
```

Q2. Anchor-contiguity theorem:

```text
Do p=237733 and p=243799 lie in the same negative MR-order B cluster?
```

Q3. Overrun theorem:

```text
Does the bridge contain a certified subcluster with T<0, B0>0, and Spsi>B0?
```

This is the cleanest finite witness that favorable `T`/baseline data still
does not control `B`.

Q4. MR-threshold theorem:

```text
Are there edge-MR rows, M(p)=-3, with B<0 and Spsi>B0 in the bridge?
```

`p=243799` already predicts yes at the endpoint; the bridge decides whether
this is isolated or clustered.

Q5. Deep-Mertens non-protection theorem:

```text
Can deep-MR rows, M(p)<=-10, remain B<0 after B0/Spsi decomposition?
```

`p=237733` predicts yes; the bridge measures persistence.

Q6. Baseline-vs-covariance split:

```text
Within the bridge, are negative B rows dominated by B0<=0 baseline failure,
or by Spsi>B0 covariance overrun?
```

This is the paper-useful taxonomy.  It replaces any positivity language.

## Verification Notes

Read and used:

- root `start.md`, `token-economy.yaml`, `L0_rules.md`, `L1_index.md`;
- project `primes-equispaced/L0_rules.md`, `primes-equispaced/L1_index.md`;
- current `primes-equispaced/HANDOFF.md` B+ sections;
- `BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md`;
- `AGENT5_BPLUS_CLUSTER_PROGRAM.md`;
- `B_plus_direct_counterexamples.md`;
- canonical `B_plus_direct_verify.c` and both anchor output files;
- MERTENS phase/disproof context.

Ran no expensive compute.  Inspected code and existing outputs only.

Local status checks showed the target output file did not exist before this
write.  Existing files in the breakthrough-wave directory were left untouched.

No Koyama correspondence or email draft was edited.

## Changed Files

- `primes-equispaced/handoff-2026-05-11-breakthrough-wave/AGENT08_BPLUS_SIGN_CLUSTER_CLASSIFICATION_2026-05-11.md`
