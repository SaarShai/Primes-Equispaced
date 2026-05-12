# Agent 3: EC-NDC beyond bad primes

Status: `PROOF_CANDIDATE`
Confidence: `0.72`
Dependencies: existing inverse-coefficient EC convention; `Koyama_EC_NDC_extended_sweep.py` trace code; strict gates `cross-ratio < 1.42083`, `max within-CV < 0.08567129`; no external theorem claim used.

## Decision

Promote the **smoothed finite EC-NDC proxy** for future verification.  The prior sharp-cutoff best proxy
`D*zeta(2)/L2E_partial^rank` failed through `K=1000000`; replacing the hard cutoff by a fixed compact `C^1`
smoothstep in the coefficient sum, Euler product, and finite `L(E,2)^rank` denominator passes both gates on the
same three curves and seven-point grid.

Also record a broader no-go: any normalization that only multiplies each sharp-cutoff curve trajectory by a
nonzero `K`-independent curve constant cannot change within-curve CV.  This covers finite bad-prime factors and
also completed/global constants such as conductor/Gamma/period/Tamagawa/BSD-leading-coefficient factors when they
are applied after the same sharp cutoff.

## Exact finite proxy tested

Curves: `37a1` rank `1`, `11a1` rank `0`, `389a1` rank `2`.
Grid: `K = 1000, 3000, 10000, 30000, 100000, 300000, 1000000`.

For `0 <= alpha < 1`, set

```text
W_alpha(t)=1                         if t <= alpha
W_alpha(t)=1-u^2(3-2u), u=(t-alpha)/(1-alpha), if alpha < t < 1
W_alpha(t)=0                         if t >= 1.
```

The tested finite proxy is

```text
X_E,alpha(K)
 = zeta(2) * c_E,alpha(K) * P_E,alpha(1;K) / L2_E,alpha(K)^rank(E)

c_E,alpha(K) = sum_{n <= K} mu_E(n)/n * W_alpha(n/K)
P_E,alpha(1;K) = prod_{p <= K} inv_p(E,1)^(-W_alpha(p/K))
L2_E,alpha(K)  = prod_{p <= K} inv_p(E,2)^(-W_alpha(p/K)).
```

Local inverse factors use the existing sweep convention:

```text
good p: inv_p(E,1)=1-a_p/p+1/p,      inv_p(E,2)=1-a_p/p^2+1/p^3
bad  p: inv_p(E,1)=1-a_p/p,          inv_p(E,2)=1-a_p/p^2.
```

This is a finite smoothed proxy only.  It is not a completed `L`-value theorem and not a BSD claim.

## Computation

Read required sources:
`HANDOFF.md`,
`KOYAMA_GPT55_DEEP_GAP_SYNTHESIS_2026-05-11.md`,
`Koyama_EC_NDC_theory_next_questions_2026-05-11.md`,
`Koyama_EC_NDC_normalization_no_go_2026-05-11.md`,
`Koyama_EC_NDC_extended_sweep_2026-05-11.md`,
`Koyama_EC_NDC_L2E_complete_check_2026-05-11.md`.

Command: inline Python importing `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py`; in-memory forked
`a_p` extension from cache max `99991` to `K=1000000`; no files written.

Run facts:

```text
primes <= 1000000: 78498
extended missing prime traces: 68906
extend_ap time: 338.108s
total time: 350.103s
```

Results:

| `alpha` | max within-CV | cross-curve ratio | gate |
|---:|---:|---:|---|
| `0.00` | `0.066157193795` | `1.406793483248` | PASS |
| `0.25` | `0.061019865232` | `1.378604205131` | PASS |
| `0.50` | `0.063993107979` | `1.359825674272` | PASS |
| `0.65` | `0.066193602570` | `1.359227676258` | PASS |
| `0.75` | `0.063297427335` | `1.347375492996` | PASS |
| `0.85` | `0.059774312813` | `1.367620962312` | PASS |
| `0.92` | `0.066713363080` | `1.392748140810` | PASS |

Recommended verification target: `alpha=0.75`, the last-quarter smoothstep taper.  It has the best tested
cross-curve ratio and a large within-CV margin.

At `alpha=0.75`, curve means are:

```text
37a1: 1.591108702362
11a1: 1.181952525781
389a1: 1.592533867122
```

Within-CVs:

```text
37a1: 0.040314798205
11a1: 0.015589562672
389a1: 0.063297427335
```

## Reduction/no-go class

Let `Y_E(K)` be any already-tested sharp-cutoff trajectory on a fixed `K` grid, and let `C_E != 0` be any
curve-dependent but `K`-independent factor.  Then

```text
mean_K(Y_E/C_E) = mean_K(Y_E)/C_E
std_K(Y_E/C_E)  = std_K(Y_E)/abs(C_E)
CV_K(Y_E/C_E)   = CV_K(Y_E).
```

Therefore the prior finite bad-prime no-go extends to all sharp-cutoff normalizations that are only per-curve
constants on the grid.  This blocks completed-factor and BSD-derivative constants unless they are integrated into
the truncation as `K`-dependent local/global weights.  A partial symmetric-square Euler product is not blocked by
this lemma if it varies with `K`.

## Next tests

1. Re-run the smoothed proxy with a persisted `AGENT3_` script and output CSV so the in-memory `a_p` extension is
   independently auditable.
2. Predeclare a small alpha set, including `0.75`, then extend to `K > 1000000` and more rank/conductor classes.
3. Test whether smoothing only `c_E`, only `P_E`, or only `L2_E` causes the gate pass; this identifies the load-bearing
   part of the normalization.
4. Build the partial symmetric-square variant as a genuinely `K`-dependent product, not a curve constant.
5. Defer complex-zero analogue until actual zero data are available for the same curves and local convention.

## Do not promote unless

- the full-grid smoothed computation is reproduced from a saved script/CSV, not only this inline run;
- `alpha=0.75` or a predeclared alpha family remains stable beyond `K=1000000`;
- the pass survives a larger non-handpicked curve sample;
- the exact finite proxy is stated every time;
- any completed/BSD/symmetric-square theorem claim includes primary-source quote plus page/equation;
- reviewers accept that this is a smoothed finite proxy, not a proof of an EC-NDC constant.
