# Koyama EC-NDC normalization no-go

Date: 2026-05-11
Agent: B
Scope: EC-NDC finite/bad-prime normalization at `rho=1`, sharp cutoff, existing data through `K=1000000`.

## Status

`NO-GO` for the tested sharp-cutoff local-factor normalization class.

No theorem promoted.  No new large computation run.  No optional probe script or CSV written.

## Claim

Finite bad-prime corrections cannot promote any tested EC-NDC normalization on the current `K` grid.

More precisely, for any normalization of the form

```text
X_E(K) = base_E(K) / B_E
```

where `B_E` is any nonzero finite product over bad primes of `E`, the within-curve coefficient of variation is unchanged.  Since every tested base normalization already has max within-curve CV above the strict threshold `0.08567129` through `K=1000000`, no bad-prime finite factor can pass the promotion rule.

This includes the natural finite Euler residuals at bad multiplicative primes.  They are also numerically too small to explain the cross-curve constants.

## Evidence

Promotion rule:

```text
cross-curve ratio < 1.42083
max within-curve CV < 0.08567129
```

Existing complete sweep:

```text
source: handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.csv
rows: 21
K grid: 1000, 3000, 10000, 30000, 100000, 300000, 1000000
largest prime: 999983
product_complete: true for all rows
```

Reported sweep metrics:

| normalization | max within-K CV | cross-curve ratio | promoted |
|---|---:|---:|---:|
| `D_zeta2_over_L2E_rank` | `0.09669211205` | `1.423821385` | false |
| `D_zeta2` | `0.09670092958` | `5.853565279` | false |
| `D_2_good` | `0.09601279473` | `10.64951807` | false |
| `D_mix_good` | `0.09601227645` | `11.04841098` | false |

Per-curve obstruction is always `389a1`:

| normalization | CV(`37a1`) | CV(`11a1`) | CV(`389a1`) |
|---|---:|---:|---:|
| `D_zeta2` | `0.06429334789` | `0.04247671608` | `0.09670092958` |
| `D_zeta2_over_L2E_rank` | `0.06422288594` | `0.04247671608` | `0.09669211205` |
| `D_mix_good` | `0.06495086873` | `0.04292542620` | `0.09601227645` |
| `D_2_good` | `0.06491743275` | `0.04292288122` | `0.09601279473` |

Thus every candidate misses the within-curve gate by at least

```text
0.09601227645 - 0.08567129 = 0.01034098645
```

and finite bad-prime constants cannot change that number.

## Formula Derivation

At good primes, with inverse local convention

```text
L_p(E,s)^(-1) = 1 - a_p p^(-s) + p^(1-2s),
mu_E(p) = -a_p,
mu_E(p^2) = p,
```

the local factor at `s=1` is

```text
E_p(1) = (1 - a_p/p + 1/p)^(-1).
```

After removing the linear prime-zero term, the principled good-prime residual is

```text
R_p(E) = exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1),

log R_p(E)
  = (a_p^2 - 2p)/(2p^2)
    + (a_p^3 - 3p a_p)/(3p^3)
    + ...
```

For a multiplicative bad prime, the local inverse factor is

```text
L_p(E,s)^(-1) = 1 - a_p p^(-s),  a_p in {-1, 1}.
```

The analogous finite residual is therefore

```text
R_p_bad(E) = exp(-a_p/p) * (1 - a_p/p)^(-1),

log R_p_bad(E)
  = a_p^2/(2p^2) + a_p^3/(3p^3) + ...
```

The second-order-only bad residual is

```text
C_2_bad(E) = exp(a_p^2/(2p^2)).
```

These are finite constants once `K >= p`.  In the present grid, the largest bad prime is `389`, and the smallest checkpoint is `1000`; therefore every bad-prime Euler factor is already switched on at every checkpoint.

For any per-curve finite factor `B_E != 0`,

```text
mean_K(X_E/B_E) = mean_K(X_E)/B_E
std_K(X_E/B_E)  = std_K(X_E)/abs(B_E)
CV_K(X_E/B_E)   = CV_K(X_E).
```

So finite bad-prime normalization can alter cross-curve ratios, but cannot alter within-curve stability.

## Numerical Checks

Bad-prime data from `Koyama_EC_NDC_ap_table_100000.csv`:

| curve | bad p | a_p | `R_bad` | `C_2_bad` | `L2_bad` |
|---|---:|---:|---:|---:|---:|
| `37a1` | `37` | `-1` | `1.00035884431` | `1.00036529680` | `0.999270072993` |
| `11a1` | `11` | `1` | `1.00441078791` | `1.00414078085` | `1.00833333333` |
| `389a1` | `389` | `1` | `1.00000330991` | `1.00000330424` | `1.00000660851` |

Applying the full bad residual to `D_mix_good` gives:

| normalization | max within-K CV | cross-curve ratio |
|---|---:|---:|
| `D_mix_good / R_bad` | `0.09601227645` | `10.9999291948` |

Applying the second-order bad residual to `D_2_good` gives:

| normalization | max within-K CV | cross-curve ratio |
|---|---:|---:|
| `D_2_good / C_2_bad` | `0.09601279473` | `10.6056376407` |

The bad factors are near `1`; they cannot explain ratios `10+` for the mixed candidates or the remaining `1.423821385` vs `1.42083` miss for the finite `L2E_partial^rank` proxy.

Sharp-truncated bad residual tails also do not rescue the class.  Using

```text
R_bad_trunc(E,K) = exp(sum_{2 <= m <= floor(log K/log p)} a_p^m/(m p^m))
```

changes the `D_mix_good` max within-K CV only to `0.0960114777312`, still above the strict gate.  Its cross-curve ratio remains `11.0004091287`.

## Verification

Read inputs:

- `handoff-2026-05-09-followup/KOYAMA_MOONSHOT_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep.py`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.csv`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_extended_sweep_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_EC_Euler_factor_theory_2026-05-10.md`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual.py`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_mixed_residual_complete_2026-05-11.md`
- `handoff-2026-05-09-followup/Koyama_EC_NDC_L2E_complete_check_2026-05-11.md`

Commands run:

```bash
python3 - <<'PY'
# CSV readback: per-curve means/CVs for D_zeta2, D_zeta2_over_L2E_rank,
# D_mix_good, D_2_good from Koyama_EC_NDC_extended_sweep_2026-05-11.csv.
PY

python3 - <<'PY'
# Bad-prime local residual readback from Koyama_EC_NDC_ap_table_100000.csv.
PY

python3 - <<'PY'
# Full and sharp-truncated bad-residual sanity check against existing CSV.
PY
```

No huge recomputation.  No changes to shared sweep scripts or existing CSVs.

## Changed Files

- `handoff-2026-05-09-followup/Koyama_EC_NDC_normalization_no_go_2026-05-11.md`

## Risks

- This is a no-go only for finite/bad-prime local-factor corrections in the tested sharp-cutoff `rho=1` class.  It does not rule out smoothing, complex-zero/Gamma conventions, new conductor/Tamagawa/period normalizations, or changing the diagnostic.
- The finite `L2E_partial^rank` proxy remains the best numerical proxy, but it still lacks a local-factor derivation for this inverse-coefficient EC-NDC convention and fails both strict gates at `K=1000000`.
- Tail-only checkpoints `K >= 100000` look more stable within each curve; the stated no-go uses the promotion rule actually applied to the full existing `K` grid.
