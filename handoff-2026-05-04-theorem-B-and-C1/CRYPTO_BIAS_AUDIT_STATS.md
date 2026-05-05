# Statistical Methodology — Koyama -1 Dominance Audit of Cryptographic Randomness

**Author:** Saar Shai
**Date:** 2026-05-03
**Status:** Methodology design (pre-registration draft)

---

## 1. Scope and reframing

Koyama's -1 Dominance generalizes Chebyshev's bias: among primes, residue class `-1 mod q` is over-represented relative to other non-residue classes, with magnitude `~ x^{1/2}/log(x)` modulated by `L(1, χ)` for the relevant Dirichlet character.

Cryptographic randomness sources fall into two regimes:

- **Prime-source mode** (RSA modulus primes, Diffie–Hellman safe primes, ECC base-point orders): outputs ARE primes. The null is "primes drawn uniformly from a distribution that respects the analytic structure of `π(x)`." -1 Dominance is a *predicted* signal; absence of it is suspicious (e.g. a backdoor that flattens the bias).
- **Pseudorandom-source mode** (drand BLAKE2 hashes, NIST Beacon SHA-512, RANDAO mixes, Algorand VRF): outputs are uniform mod `q` by design. -1 Dominance is *not* expected. Any statistically significant deviation mod `q` is suspicious.

This split governs hypothesis direction: prime-source uses a one-sided test FOR the bias; pseudorandom-source uses a two-sided test against uniform.

---

## 2. Notation

- `K`: number of samples.
- `q`: modulus, with `q ∈ Q = {3, 4, 5, 7, 8, 11, 12, 13}`.
- `φ(q)`: Euler totient (number of reduced residue classes).
- `n_a`: observed count of samples `≡ a (mod q)` with `gcd(a, q) = 1`.
- `E_a = K · 1/φ(q)`: expected count under uniform-on-coprime-residues null. (For pseudorandom outputs we use uniform on ALL classes mod `q`, `E_a = K/q`; for prime sources only coprime classes are populated.)
- `χ_4`: non-trivial Dirichlet character mod 4. For general `q`, the relevant non-principal real character.

---

## 3. Test 1 — Chi-squared uniformity mod q

**Statistic.**

```
T_q = Σ_{a coprime to q} (n_a - E_a)^2 / E_a
```

**Null `H_0`:** outputs uniform on reduced residues mod `q`. `T_q ~ χ^2_{φ(q)-1}`.

**Alternative `H_1`:** non-uniform distribution (any direction).

**Decision.** Reject `H_0` at level `α` when `T_q > χ^2_{φ(q)-1, 1-α}`. We pre-register `α = 10^{-3}` and apply Bonferroni across `|Q| = 8` moduli, so per-modulus threshold is `α/8 = 1.25·10^{-4}`.

**Use.** Omnibus screen. Catches any deviation, not just -1 Dominance.

---

## 4. Test 2 — One-sided -1 Dominance statistic

**Statistic.**

```
S_q = n_{-1 mod q}  -  max{ n_a : a coprime to q, a ≠ ±1 }
```

(Subtract the second-best non-trivial class, NOT `n_{+1}`, because `+1` carries its own well-known bias from Linnik-type effects. The Koyama prediction is that `-1` outranks all non-trivial competitors.)

**Null distribution.** Under uniform null on coprime classes, with `K` large, the joint vector `(n_a)` is approximately multinomial. Write `p = 1/φ(q)`. Each `n_a` is `~ N(Kp, Kp(1-p))`. The differences `n_{-1} - n_a` for `a` coprime, `a ∉ {±1}` are jointly Gaussian with:

- Mean 0
- Var(`n_{-1} - n_a`) `= 2Kp(1-p) - 2·(-Kp^2) · I[a≠-1] = 2Kp` (using `Cov(n_a, n_b) = -Kp^2` for `a≠b`)
- Wait — re-derive: `Var(n_{-1} - n_a) = Var(n_{-1}) + Var(n_a) - 2Cov = 2Kp(1-p) + 2Kp^2 = 2Kp`.

So each pairwise difference has SD `σ_pair = √(2Kp)`. The maximum over `m = φ(q) - 2` competitors is approximately Gumbel with scale `σ_pair` and location `σ_pair · √(2 log m)` (extreme-value theory). Hence:

```
E[max difference under H_0]  ≈  σ_pair · √(2 log m)
SD[S_q under H_0]             ≈  σ_pair · π / √(6 · 2 log m)
```

For small `m` (e.g. `q=4`, `m=0`; `q=5`, `m=2`) we use Monte Carlo calibration of `S_q`'s null distribution rather than the asymptotic approximation. **Pre-register: 10^7 multinomial draws per `(q, K)` pair to tabulate critical values.**

**Alternative `H_1` (prime-source mode):** `S_q > 0` with magnitude consistent with Koyama's `~ K · L(1,χ) / (φ(q) · log K_max)` scaling, where `K_max` is the largest sampled prime.

**Decision.** One-sided test: reject `H_0` at `α = 10^{-3}` (Bonferroni across `|Q|`).

---

## 5. Test 3 — Bias hierarchy correlation

**Setup.** For each `q ∈ Q`, compute observed bias:

```
β_obs(q) = (n_{-1 mod q} - K/φ(q)) / √(K · (1-1/φ(q))/φ(q))
```

(z-score of the -1 class.) Compute predicted bias from Koyama theory:

```
β_pred(q) = c · L(1, χ_q) / log(K_max)
```

where `c` is a fitted constant and `χ_q` is the relevant real non-principal character mod `q`. Use `L(1, χ_4) = π/4`, `L(1, χ_3) = π/(3√3)`, `L(1, χ_8) = (log(1+√2))/√2 · ...` — values from `mpmath.dirichlet` at 30 digits (per CRITICAL VERIFICATION GATE: never trust LM-recalled special values).

**Statistic.** Spearman rank correlation `ρ(β_obs, β_pred)` across the 8 moduli, plus weighted least-squares regression `β_obs ~ a + b · β_pred`.

**Null `H_0`:** `ρ = 0` (no relationship).
**Alternative `H_1` (prime-source):** `ρ > 0` with slope `b ≈ 1` after proper normalization.
**Alternative `H_1` (pseudorandom-source):** `ρ = 0` expected; `ρ ≠ 0` is a red flag.

**Decision.** Permutation test (10^4 permutations of `q`-labels) for p-value of `ρ`.

---

## 6. Test 4 — Cross-modulus consistency

If `q | q'` (e.g. `q=4`, `q'=8` or `q'=12`), the bias mod `q'` should project consistently onto the bias mod `q`. Specifically, residue class `-1 mod q` is the union of `φ(q')/φ(q)` classes mod `q'`, one of which is `-1 mod q'`.

**Statistic.** Correlation `ρ_proj(q, q')` between observed counts when `q'` data is reduced mod `q`, vs. directly observed mod `q` counts. Should approach 1.

**Decision.** Flag inconsistency if `|1 - ρ_proj| > 3·SE` (jackknife SE over `K`-blocks).

This catches *structured* backdoors that bias one modulus but not its divisors.

---

## 7. Sample-size analysis

**Setup.** Treat output as integer `X` with `X mod q` uniform on `{0, 1, ..., q-1}` (pseudorandom-source). Bias of magnitude `δ` means one class has probability `1/q + δ/K` rather than `1/q`. (We parametrize bias as an additive count excess.)

**Detection threshold (Test 1, chi-squared).** Non-centrality parameter `λ = δ^2 · q / K` (when one class is shifted by `+δ` count, others compensate). For 80% power at `α = 10^{-3}` with `df = q - 1`:

- `q = 4`: `λ_crit ≈ 22`, so detectable `δ ≈ √(22 · K / 4) = √(5.5 K)`.
- `q = 12`: `λ_crit ≈ 30`, so `δ ≈ √(2.5 K)`.

**Detection threshold (Test 2, -1 Dominance one-sided).** Detect `S_q = δ` against null SD `σ_pair · √(2 log m)`-corrected. For `K = 10^7`, `q = 4` (no competitors so `S_4 = n_{-1} - n_1`, a single difference): SD `= √(2 · 10^7 · 0.5) = √(10^7) ≈ 3162`. So 3-sigma detection threshold is `δ_min ≈ 9500`, which is a fractional bias of `9500 / (10^7 / 2) = 1.9·10^{-3}`.

**Smallest detectable fractional bias `ε = δ / (K/φ(q))` as a function of `K`:**

```
For q = 4 (φ=2, single competitor):
  ε_min(K) ≈ 3 · √(2 · 0.5 / K) · 2 = 3 · √(2/K)
       K=10^6  → ε_min ≈ 4.2·10^{-3}
       K=10^7  → ε_min ≈ 1.3·10^{-3}
       K=10^8  → ε_min ≈ 4.2·10^{-4}
       K=10^9  → ε_min ≈ 1.3·10^{-4}
```

These thresholds are *generous*; tightening to 4-sigma costs `4/3` factor in `δ`, i.e. ~78% more samples for same `ε`.

---

## 8. Worked example — drand mod 4 with K = 10^7

**Setup.** drand outputs are 32-byte BLAKE2 hashes, treated as integers in `[0, 2^256)`. Take `X mod 4` over `K = 10^7` samples.

**Expected counts under null:** `E_0 = E_1 = E_2 = E_3 = 2.5 · 10^6`.

**Test 1 (chi-squared, `df=3`).** Reject at `α = 10^{-3}` if `T_4 > 16.27`. Power 80% to detect a uniform shift of `λ = 16.27 + 6.25 ≈ 22.5` non-centrality, i.e. excess count `δ ≈ √(22.5 · 10^7 / 4) ≈ 7500`. Fractional excess `≈ 3·10^{-3}`.

**Test 2 (-1 Dominance: `n_3 - n_1`).** Under `H_0`: `n_3 - n_1 ~ N(0, 2 · 10^7 · 0.25) = N(0, 5·10^6)`, SD `≈ 2236`. One-sided rejection at `α = 10^{-3}`: `n_3 - n_1 > 3.09 · 2236 ≈ 6909`. Fractional bias detected: `6909 / 2.5·10^6 ≈ 2.8·10^{-3}`.

**Power.** To detect a true bias of `1·10^{-3}` (i.e. `δ_true = 2500`) with 80% power at `α = 10^{-3}`, we need:

```
K_required = ((z_{1-α} + z_{0.8})·σ / δ_true)^2 · K_old
           = ((3.09 + 0.84) · 2236 / 2500)^2 · 10^7
           = (3.51)^2 · 10^7 ≈ 1.2 · 10^8
```

So **`K = 1.2·10^8` drand samples** detect a 0.1% bias mod 4 at `p<10^{-3}` with 80% power. drand has produced `~10^7` rounds; reaching `10^8` requires either pooling beacon networks or accepting the current `~3·10^{-3}` floor.

**Ethereum RANDAO** (`~10^9` available) gets `ε_min ≈ 1.3·10^{-4}` — best detection power of any current source.

---

## 9. Power summary table

| Source | K available | Test 2 ε_min (q=4) | Test 1 ε_min (q=12) |
|---|---|---|---|
| drand | 10^7 | 2.8·10^{-3} | 1.6·10^{-3} |
| NIST Beacon | 10^7 | 2.8·10^{-3} | 1.6·10^{-3} |
| RANDAO | 10^9 | 2.8·10^{-4} | 1.6·10^{-4} |
| Algorand VRF | 10^9 | 2.8·10^{-4} | 1.6·10^{-4} |
| /dev/urandom | 10^{12} | 2.8·10^{-6} | 1.6·10^{-6} |

`/dev/urandom` is the gold-standard positive control: at `K=10^{12}` we should see no bias to within `~10^{-6}`. Any positive detection there indicates a flaw in the test pipeline, not the RNG.

---

## 10. Positive controls (prime-source mode)

To validate the pipeline, run Tests 1–3 on:

- **Primes ≤ 10^{10}** (sieve of Eratosthenes; ~4.55·10^8 primes). Test 2 should yield `S_4 > 0` at extreme significance (`p < 10^{-100}`), with `β_obs(q)` tracking `L(1, χ_q)` per Koyama.
- **First 10^7 RSA-2048 moduli** from public Certificate Transparency logs. Each modulus is a product of two primes; test the primes themselves if available, else the moduli (in which case the bias signature is the *convolution* of two prime biases, predictable from theory).

A pipeline that fails to reproduce Chebyshev's bias on raw primes is not yet trustworthy for crypto auditing.

---

## 11. Multiple-comparisons control

- 8 moduli × 4 tests = 32 nominal comparisons. Bonferroni at family-wise `α = 10^{-3}` requires per-test `p < 3·10^{-5}`.
- Alternatively, Benjamini–Hochberg FDR at `q* = 10^{-3}` is more powerful and pre-registered as the secondary criterion.

---

## 12. Caveats and confidence

- **Caveat 1.** Treating 256-bit hash outputs as "uniform mod q" is only true to within `q/2^{256}`, i.e. negligible for `q ≤ 2^{200}`. The modular reduction itself introduces no detectable bias.
- **Caveat 2.** Test 2's null calibration via Monte Carlo for small `m = φ(q)-2` is critical; the asymptotic Gumbel is wrong for `q ∈ {3, 4, 5}`. Pre-register MC tables.
- **Caveat 3.** RANDAO outputs are *not* independent across slots — a validator's contribution biases the next mix slightly. Effective sample size `K_eff < K`. Conservative correction: `K_eff = K / 2`.
- **Caveat 4.** Koyama's `L(1, χ)` modulation is rigorous under GRH; without GRH there is `O(x^{1/2-ε})` slack. For audit purposes the *rank order* of `β_pred(q)` is robust regardless of GRH.

**Confidence in methodology:** HIGH for Tests 1, 2, 4 (textbook multinomial/extreme-value theory). MEDIUM for Test 3 (relies on Koyama's prediction structure being correctly computed for each `q` — verify each `L(1, χ_q)` numerically before use, see CRITICAL gates).

**Confidence in detection capability:** With current-scale data (`10^7`), only biases ≥ `10^{-3}` are detectable for `q=4`. A backdoor producing a `10^{-5}` bias would survive these tests on drand/NIST. Higher-volume sources (RANDAO, /dev/urandom) push the floor down to `10^{-4}` and `10^{-6}` respectively.

---

## 13. Pre-registered analysis plan

1. Verify `L(1, χ_q)` values for `q ∈ Q` via mpmath at 30 digits. Fail-fast on any discrepancy from Koyama tables.
2. Run Tests 1–4 on positive control (primes ≤ 10^{10}). Pipeline accepted only if Chebyshev's bias is recovered with `S_4 z-score > 100`.
3. Run Tests 1–4 on `/dev/urandom` at `K = 10^{10}`. Pipeline accepted only if no test rejects at `α = 10^{-3}`.
4. Apply pipeline to drand, NIST, RANDAO, Algorand VRF at maximum available `K`.
5. Report all p-values; do not cherry-pick.

End of methodology.
