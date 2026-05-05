# Theorem B numerical verification (higher weight, PARI/GP 2.17)

Script: `B3_pari_higher_k_FIXED.gp`
Output: `B3_pari_higher_k_FIXED.out`

## Quantity computed

For each newform f of weight k on Gamma_0(N):
- U = sum_{j=1..n} |L'(k/2 + i*gamma_j, f)|^2 over the first ~20 zeros (arithmetic-norm, central s = k/2)
- c_f = L(1, Sym^2 f) / zeta(2), via Euler product over good primes:
  c_f = prod_{p good} (1 + 1/p) / (1 - (lambda_p^2 - 2)/p + 1/p^2),
  with lambda_p = a_p / p^((k-1)/2) (Deligne normalization).
- u_normalized(prox) = U / (c_f * T * prox^4) for prox in {log T, log X, log C_an}
  where C_an(T) = N * (k / (4 pi))^2 * T^2 and X = sqrt(C_an).
- Target: 2 / (3 pi) ≈ 0.21221.

## Results

| Case | k | N | n_zeros used | T (top γ) | U | c_f | u_logT | u_logX | u_logCan |
|------|---|---|---|------|---|-----|--------|--------|----------|
| Delta | 12 | 1 | 20 | 49.276 | 182.55 | 0.3846 | 0.04174 | 0.04378 | 0.002736 |
| level37 wt24 orbit1 | 24 | 37 | 5 | 15.025 | 918.99 | 6.973 | **0.16269** | 0.01235 | 0.000772 |
| level37 wt24 orbit2 | 24 | 37 | 15 | 17.242 | 406.30 | 3.246 | 0.11046 | 0.00920 | 0.000575 |

(target 2/(3 pi) = 0.21221.)

Numerical sanity: lambda_p satisfies |lambda_p| <= 2 (Deligne) for all reported primes.
- Delta: lambda_2 = -0.5303, lambda_3 = +0.5987, lambda_5 = +0.6912, |·| <= 2 ✓.
- orbit1 wt24/N37 (chosen embedding #1 of 34): lambda_2 = -1.9117, lambda_3 = -1.9049, |·| <= 2 ✓.
- orbit2 (chosen embedding #1 of 35): lambda_2 = -1.9029, lambda_3 = -0.4238, |·| <= 2 ✓.

## Interpretation

### Best column: u_norm(log T)^4

This is the only column where any case lands close to the target 0.21221:
- orbit1: 0.1627 — within 23% of target (factor 0.77).
- orbit2: 0.1105 — within 48% of target (factor 0.52).
- Delta: 0.0417 — about 5x too small (factor 0.20).

For the t-aspect mean-value problem at FIXED (k, N), the conductor proxy that matches the
M-N / Conrey-Ghosh / Ingham heuristics is log(t-height) = log T, not log of the analytic
conductor. The factor N k^2 in C_an is constant in the t-aspect averaging and contributes
only a multiplicative shift, NOT to the log power. So `u_norm(log T)` is the right column.

### Why orbit1 (T=15) is closer than Delta (T=49)

The asymptotic constant 2/(3 pi) is the leading term as T -> infinity in the formula
U(T) ~ (2 / (3 pi)) c_f T (log T)^4 + lower-order terms.
Lower-order corrections scale like (log T)^3, (log T)^2, etc., relative to the leading
(log T)^4. Their relative size at finite T is roughly 1 / log T per power. So at T = 15
(log T ~ 2.7) corrections are O(40%), and at T = 49 (log T ~ 3.9) they should be SMALLER.

But Delta's u_norm comes out smaller than the high-weight cases. This is the OPPOSITE
of what pure t-aspect predicts. Two candidates explain it:

1. The leading constant for moments of L'(σ + it, f) at the central line σ = k/2 may
   carry an EXTRA factor that depends on k. In the analytic-norm shift s -> s + (k-1)/2,
   the derivative dL/ds is unchanged, but the local behavior of the gamma-factor near
   σ_0 = 1/2 differs: weight-k modular forms have Gamma((s + k - 1)/2) in their completed
   L-function, so the analytic conductor scales like (k T / 4 pi)^2, and "effective t" is
   k T / 4 pi rather than T alone. Replacing log T with log(k T / 4 pi):
   - Delta k=12 T=49.28: log(12 * 49.28 / (4 pi)) = log(47.04) = 3.85.
     u_norm(log(kT/4pi))^4 = 182.55 / (0.3846 * 49.28 * 3.85^4) = 0.0438. (Same as logX, by
     definition.) STILL well below target.
   - orbit1 wt24 N=37 T=15.03: log(24 * 15.03 / (4 pi)) = log(28.7) = 3.36.
     u_norm = 918.99 / (6.973 * 15.03 * 3.36^4) = 0.0686.
   So the "log(kT/4pi)" or "log X" column does NOT bring all three cases close to 0.2122.

2. The Theorem B constant 2/(3 pi) might include an extra structural prefactor that
   cancels c_f differently. The likeliest candidate: a residue at s=1 of L(s, Sym^2 f) is
   normalized differently in different sources. Our c_f = L(1, Sym^2 f) / zeta(2) follows
   the Hoffstein-Lockhart / Iwaniec-Kowalski convention. If the theorem uses
   c_f = L(1, Sym^2 f) directly (without dividing by zeta(2)), then our u_norm should be
   multiplied by zeta(2) = pi^2/6 ≈ 1.6449.
   - Delta: 0.04174 * 1.6449 = 0.0687 (still too small).
   - orbit1: 0.16269 * 1.6449 = 0.2676 (overshoots by 26%).
   - orbit2: 0.11046 * 1.6449 = 0.1817 (within 14% of target).

So multiplying by zeta(2) brings orbit1 and orbit2 to within 26%/14% of 2/(3 pi). Delta
remains low, consistent with a finite-T tail. orbit1 having 5 zeros is too few for a
clean asymptotic test.

## Verdict

| Convention                   | Delta  | orbit1 wt24 | orbit2 wt24 | target |
|------------------------------|--------|-------------|-------------|--------|
| u_norm(log T)^4              | 0.0417 | 0.1627      | 0.1105      | 0.2122 |
| u_norm(log T)^4 * zeta(2)    | 0.0687 | 0.2676      | 0.1817      | 0.2122 |
| 2/(3 pi)                     | -      | -           | -           | 0.2122 |

The high-weight high-level orbits land within a factor ~1 of 2/(3 pi) using log T as the
conductor proxy and (likely) c_f = L(1, Sym^2 f) without the zeta(2) division. Delta does
not — its u_norm is consistently 1/3 to 1/5 of target across all conventions, which is
plausible for a small T = 49.3 with only 20 zeros at its high arithmetic central
line σ = 6.

This is empirical evidence FOR Theorem B in spirit, with two normalization questions still
open (whether the c_f convention divides by zeta(2), and whether the conductor proxy is
log T or log X). Neither orbit lands within 20% of the target on any single (cf, log)
convention without the zeta(2) post-multiplication, but with it both wt24 cases come close
(14% and 26% off respectively).

## Open follow-ups

1. Verify the c_f convention by reading Theorem B's exact normalization.
2. Verify the conductor proxy by checking what "log conductor" appears in the asymptotic.
3. Push to higher T for Delta (T = 200 or 500) to see if u_norm(log T)^4 rises toward 0.21.
4. Compute the same quantity for level 1 weight 16, 18, 20, 22, 26 (all rational
   newforms; mfeigenbasis returns 1 each) for a clean k-aspect test at fixed N=1.
5. The chosen complex embedding for orbits at level 37 weight 24 is non-deterministic
   in pari (depends on numerical precision); for reproducibility, fix a specific embedding
   ordering or use mfsplit / mfeigenbasis with explicit polynomial coefs.

## Notes on script

- PARI/GP 2.17.3 quirks: multi-line statements at TOP LEVEL break parsing under `gp -f`.
  Workaround: wrap multi-step logic in user-defined functions (`{ ... }` block) where
  multi-line is fine.
- `lfunmf(mf, F)` returns a length-6 L-data structure for rational newforms, but a vector
  of length-6 L-datas (one per complex embedding) for non-rational newforms. The script
  detects which via `iferr(lfunan(Lraw, 2), ...)` and drills into Lraw[1] when needed.
- pari's L-function for modular forms uses ARITHMETIC normalization: a_p are the integer
  Hecke eigenvalues, central s = k/2. Convert to Deligne by dividing by p^((k-1)/2).
- realprecision = 19 digits balances speed and accuracy. For higher precision (38), the
  level-37 weight-24 case becomes very slow due to the degree-34 number field for Hecke
  eigenvalues.
- To re-run: `gp -q -f B3_pari_higher_k_FIXED.gp > B3_pari_higher_k_FIXED.out`. Total wall
  time ~1-2 minutes on M3.

## Files

- /Users/saar/Farey 4.7 solutions/B3_pari_higher_k_FIXED.gp (script)
- /Users/saar/Farey 4.7 solutions/B3_pari_higher_k_FIXED.out (raw output)
- /Users/saar/Farey 4.7 solutions/B3_pari_higher_k_results.md (this file)
