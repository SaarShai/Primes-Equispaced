Status: RIGOROUS_REDUCTION
Confidence: 0.88 for the cluster program; 0.98 for the two direct counterexamples.
Dependencies: `B_plus_direct_verify.c`; `B_plus_direct_counterexamples.md`; `MERTENS_LB_MR_disproof.md`; `MERTENS_LB_phase_transition_probe_2026-05-11.md`; R1/SP1a/SP2 exact identities. No external theorem claims are used here.

# Agent 5: B+ Counterexample Cluster Program

## Verdict

The B+ positivity theorem is dead in the Lean-canonical `crossTerm` definition. The useful target is now finite, reproducible classification:

> Among primes `p` with `M(p) <= -3`, classify maximal sign clusters of canonical `B(p)` and split them by the quadrant `(sign B(p), sign T(p-1))`.

Known anchors:

| p | M(p) | T(p-1) | `|F_{p-1}|` | B(p) | B/C | class |
|---:|---:|---:|---:|---:|---:|---|
| 237733 | -20 | +6.657511751192 | 17178971883 | -3.018492026640170e10 | -10.543163714952145 | baseline-fail |
| 243799 | -3 | -0.834778256610 | 18066862385 | -9.190201299936827e9 | -3.052438040867344 | sigma-overrun |

The second row is the key decoupling witness: favorable `T(p-1)<0` does not force `B(p)>0`.

## Canonical Identities To Preserve

Use exactly the Lean/R1 normalization:

```text
B(p) = 2 * sum_{f in F_{p-1}} D_{p-1}(f) * delta_p(f)
D_N(f) = fareyRank_N(f) - |F_N| * f
delta_p(a/b) = a/b - frac(p*a/b) = (a - (p*a mod b))/b
```

R1/SP1a/SP2 give the decoupled form:

```text
N = p - 1,  n = |F_N|
B(p)/2 = B0(N) - Spsi(p)
B0(N) = 1/12 - n*T(N)/12 - n*||delta_F||_2^2/2
T(N) = 1 + sum_{k=1}^N M(floor(N/k))/k
Spsi(p) = sum_{f in F_N} D_N(f) * (sigma_p(f) - 1/2)
sigma_p(a/b) = (p*a mod b)/b
```

So `T(N)` controls only the p-independent baseline `B0(N)`. The p-dependent obstruction is `Spsi(p)`, a residue-permutation covariance. Mertens restriction and `T(N)` do not control that covariance.

## Cluster Classes

Primary clusters are maximal consecutive runs in the ordered list

```text
MR(P) = {prime p <= P : M(p) <= -3}
```

with the same certified sign of `B(p)`.

Secondary class labels:

| label | condition | meaning |
|---|---|---|
| `ordinary-pos` | `B>0`, `T<0` | baseline favorable and covariance not fatal |
| `rescued-pos` | `B>0`, `T>0` | positive despite bad/negative `B0` pressure |
| `baseline-fail` | `B<0`, `T>0` | `T` makes `B0` negative or weak; 237733 is here |
| `sigma-overrun` | `B<0`, `T<0` | `Spsi(p)>B0(N)` despite favorable `T`; 243799 is here |
| `borderline` | uncertified sign | requires interval/exact rerun |

## Exact Data Requirements

Do not use `MERTENS_LB_MR_verification.tsv` as a cluster-boundary source; it is sampled after the early range. Regenerate dense lists.

Prime-row TSV, one row per MR prime:

```text
range_id
p
N
prime_index
mr_index
M_p
M_N
T_N
T_sign
T_small_k_10
T_tail_after_10
farey_size_n
B
C_shift_sq
B_over_C
B0_stream
Spsi_stream
B_recombine_error = B - 2*(B0_stream - Spsi_stream)
sum_delta
sum_D
B_sign
cert_level
elapsed_seconds
source_sha
compiler_flags
```

Cluster-row TSV:

```text
range_id
cluster_id
B_sign
start_p
end_p
mr_count
ambient_prime_count
width
min_B
max_B
min_B_over_C
max_B_over_C
T_pos_count
T_neg_count
class_histogram
representative_p
cert_level_min
```

Diagnostic side table, optional but recommended for explanations:

```text
p
b_band
sum_B_band
sum_C_band
sum_B0_band
sum_Spsi_band
D_pos_delta_pos
D_pos_delta_neg
D_neg_delta_pos
D_neg_delta_neg
```

Bands: `b<=10`, `11..100`, `101..1000`, `1001..10000`, `10001..100000`, `>100000`.

## Fastest Feasible Implementation Route

1. Clone `handoff-2026-05-09-followup/B_plus_direct_verify.c` to an `AGENT5_` helper only if implementing. Keep the five Lean anchor checks.
2. Convert output to machine TSV. Disable progress by default. Add streaming accumulators for `B0_stream` and `Spsi_stream`; this costs no new asymptotic work because each Farey fraction already has `D`, `f`, and `p*a mod b`.
3. Use `long double` plus Kahan/Neumaier sums for `B`, `C`, `B0`, `Spsi`, `sum_D`, `sum_delta`. Emit double-compatible values only after storing long-double internals.
4. Generate dense MR prime lists and `T(N)` with the phase-probe/MERTENS routines, not with the sampled MR TSV.
5. Parallelize over primes, not inside one Farey traversal. The existing verifier takes about 75-79 s at `p ~= 240k`; dense first-cluster windows are feasible on a multicore machine, but full `p<=1e6` by direct enumeration is a multi-day CPU job.

Run tiers:

| tier | range | purpose | promotion level |
|---|---|---|---|
| 0 | `p in {237733,243799}` | reproduce anchors | required |
| 1 | dense MR primes `100003 <= p <= 300000` | first negative cluster and post-99991 transition | primary target |
| 2 | dense windows around MR/T flip clusters: `237k-241k`, `565k-573k`, plus any dense T-positive clusters found to `1e6` | recurrence map | secondary |
| 3 | all MR primes `p <= 1e6` | global finite atlas | only if compute budget is explicit |

## Decoupling Explanation

`T(N)` is a Mobius-harmonic statistic of floors `floor(N/k)`. It enters `B(p)` only through `B0(N)`, which is fixed once `N=p-1` is fixed.

`Spsi(p)` is different data: it is the covariance of the same Farey rank deviation `D_N` against the multiplication permutation `a -> p*a mod b` on every reduced denominator `b<=N`.

Therefore:

```text
T(N)<0  => usually B0(N)>0, but B(p)>0 still needs Spsi(p)<B0(N).
T(N)>0  => B0(N) is usually negative/weak, but B(p) still depends on Spsi(p).
```

`p=243799` is the clean witness: `T(p-1)<0`, yet `B(p)<0`, so `Spsi(p)` overruns the favorable baseline. This kills every plan that promotes `T(p-1)` as a sign proxy for `B(p)`.

## Certification Rules

`cert_level`:

| level | requirement |
|---|---|
| `anchor` | five Lean `native_decide` values reproduced |
| `float-wide` | long-double compensated run, recombination check, large margin |
| `repeat` | independent rerun with altered block order or compiler flags |
| `borderline` | `abs(B)` too small for the error policy; not a cluster boundary |

Minimum promotion for cluster boundaries: `anchor + float-wide`. Minimum promotion for surprising isolated rows: `repeat`.

## Do Not Promote Unless

- The MR prime list is dense in the claimed range.
- `B_plus_direct_verify.c` anchors still match `p=5,11,13,19,23`.
- `p=237733` and `p=243799` reproduce with the signs and margins above.
- Every claimed cluster boundary has certified `B` signs on both sides in MR-prime order.
- The deliverable separates `T` sign, `B0`, and `Spsi`; no `T` proxy language survives.
- Any future external theorem citation includes primary-source quote, page/equation, and title check before use.

## Next Concrete Output

Produce:

```text
handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_ROWS_<range>.tsv
handoff-2026-05-11-gpt55-wave/AGENT5_BPLUS_CLUSTER_SUMMARY_<range>.md
```

for tier 1 first. The mathematical result to look for is whether the first negative cluster beginning at or before `p=237733` continues through `p=243799`, splits into multiple MR-prime sign runs, or is one of several nearby sigma-overrun islands.
