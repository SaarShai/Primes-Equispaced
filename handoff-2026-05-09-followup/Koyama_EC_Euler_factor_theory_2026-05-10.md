# Koyama EC Euler-Factor Theory - Agent C

Date: 2026-05-10
Scope: elliptic-curve NDC local constants at `s = 1`.
Write target: this file only.

Inputs read:
- `handoff-2026-05-09-followup/Koyama_EC_NDC_sweep.md`
- `handoff-2026-05-09-followup/Koyama_EC_NDC.py`
- `handoff-2026-05-09-followup/Koyama_EC_NDC.csv`
- `experiments/NDC_EC_AFE_COMPUTATION.md`
- `experiments/LIT_RANKIN_SELBERG_NDC.md`
- `koyama-shared/scripts/ndc_gl2_full_test.py`

Note: no file named `Koyama_EC_NDC_sweep.py` exists in this checkout.  The
present companion script is `handoff-2026-05-09-followup/Koyama_EC_NDC.py`.

## Executive decision

For the newer EC sweep convention

```text
mu_E(p)   = -a_p
mu_E(p^2) = p
mu_E(p^k) = 0, k >= 3        good p
```

the natural finite correction is not `L(2,E)`.  The first nontrivial local
constant comes from the square of the GL(2) Satake roots, hence from
Sym^2/Rankin-Selberg data at `2s = 2`, with an additional zeta/Mertens
deconvolution and higher local power corrections.  So the right answer is:

```text
mixed adjoint/Sym^2 local correction, not bare L(2,E), not bare Sym^2.
```

`L(Sym^2 E,2)` is the leading recognisable standard L-function piece.
Full Rankin-Selberg data is useful for diagnostics, but it contains zeta
diagonal factors that must be removed before comparing to this EC NDC
normalization.

## Local-factor derivation

At a good prime,

```text
L_p(E,s)^(-1) = 1 - a_p p^(-s) + p^(1-2s)
              = (1 - alpha_p p^(-s))(1 - beta_p p^(-s)),

alpha_p + beta_p = a_p,
alpha_p beta_p = p.
```

Thus the inverse-L coefficient convention in the new sweep is exactly the
coefficient convention of this reciprocal local factor:

```text
mu_E(p)   = -a_p,
mu_E(p^2) = alpha_p beta_p = p.
```

At `s = 1`, put `lambda_p = a_p / sqrt(p)`.  The Euler-product factor used in
the sweep is

```text
E_p(1) = (1 - a_p/p + 1/p)^(-1)
       = (1 - alpha_p/p)^(-1)(1 - beta_p/p)^(-1).
```

Taking logs gives the usable local expansion:

```text
log E_p(1)
  = sum_{m >= 1} (alpha_p^m + beta_p^m) / (m p^m)
  = lambda_p / sqrt(p)
    + (lambda_p^2 - 2)/(2p)
    + (lambda_p^3 - 3 lambda_p)/(3 p^(3/2))
    + O(1/p^2).
```

Equivalently, in unnormalised `a_p` notation,

```text
log E_p(1)
  = a_p/p
    + (a_p^2 - 2p)/(2p^2)
    + (a_p^3 - 3p a_p)/(3p^3)
    + O(1/p^2).
```

The linear term `a_p/p` is the term whose prime sum feels the zero/order of
`L(E,s)` at `s = 1`.  The first local-constant term is the second term

```text
(a_p^2 - 2p)/(2p^2) = (alpha_p^2 + beta_p^2)/(2p^2).
```

This is the key discriminator:

- `L(2,E)` has local log beginning `a_p/p^2 + O(p^-3)`.  That is too small
  and has the wrong shape.
- `L(Sym^2 E,2)` has local first trace
  `(alpha_p^2 + alpha_p beta_p + beta_p^2)/p^2 = (a_p^2 - p)/p^2`.
- The EC NDC expansion needs `alpha_p^2 + beta_p^2 = a_p^2 - 2p`, i.e. the
  same-root square terms with the middle `alpha_p beta_p = p` term removed.
- Full Rankin-Selberg has even more diagonal/zeta contribution.  It is the
  right family of data, but not the final normalization without deconvolution.

The exact finite local residual after removing the linear prime-zero term is

```text
R_p(E) = exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1)

log R_p(E)
  = (a_p^2 - 2p)/(2p^2)
    + (a_p^3 - 3p a_p)/(3p^3)
    + ...
```

This `R_p` is the clean mixed correction: leading Sym^2/adjoint behaviour plus
all higher local powers.  Bad primes should be carried as finite local factors;
they do not decide the infinite-prime normalisation.

## Consequence for constants

The old question "should the EC constant be `zeta(2)`, `L(2,E)`,
`L(Sym^2 E,2)`, or Rankin-Selberg?" should be refined:

```text
zeta(2)             GL(1) baseline; insufficient for EC data.
L(2,E)              reject: wrong local expansion.
L(Sym^2 E,2)        leading proxy, but incomplete.
Rankin-Selberg      useful source of second moments, but too much zeta diagonal.
mixed correction    recommended: exact local residual R_p, with Mertens regularisation.
```

A computationally useful finite version is

```text
C_mix(K)
  = (e^gamma log K)^(1/2)
    * product_{p <= K, p good} exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1)
    * C_bad(E),
```

where `C_bad(E)` is the finite product of the chosen bad-prime residuals.  The
`(e^gamma log K)^(1/2)` factor is the Mertens regularisation for the removed
middle/zeta contribution.  If the data says this over-regularises, keep both
raw and regularised columns; the main point is that the residual must be local
and adjoint/Sym^2-shaped, not `L(2,E)`-shaped.

The recommended normalized observable is therefore

```text
D_mix(K) = D_K^E * zeta(2) / C_mix(K).
```

Target comparison: test whether `D_mix(K)` is flatter and more curve-universal
than raw `D_K^E * zeta(2)`.

## Current EC sweep readout

From `Koyama_EC_NDC.csv` at `K = 100000`:

```text
37a1:   D_K*zeta(2) = 0.6178615552, c_K/log K       = 3.093373205
11a1:   D_K*zeta(2) = 1.1840970395, c_K             = 4.004756112
389a1:  D_K*zeta(2) = 0.1927028966, c_K/(log K)^2   = 0.729899001
```

The Aoki-Koyama `c_K` scaling is plausible, especially for 37a1.  The raw
`zeta(2)` NDC constant is not universal across ranks/curves at this range.
This is exactly what the local expansion predicts: ECs have a real GL(2)
second-root correction missing from the GL(1) normalisation.

## Convention reconciliation

The newer EC sweep and the older GL2 script are not using the same `mu`.

New EC sweep, `Koyama_EC_NDC.py`:

```text
good p:
  mu_E(p)   = -a_p
  mu_E(p^2) = p
  mu_E(p^k) = 0 for k >= 3

E_p(s) = (1 - a_p p^(-s) + p^(1-2s))^(-1)
rho = 1 for the BSD central point/zero
sharp c_K cutoff n <= K
Euler product p <= K
no Gamma factor
```

Older GL2 script, `koyama-shared/scripts/ndc_gl2_full_test.py`:

```text
good p:
  mu_script(p)   = -a_p
  mu_script(p^2) = a_p^2 - p
```

But `a_p^2 - p` is the ordinary Hecke coefficient `a_{p^2}`, not the
coefficient of `1/L(E,s)`.  The older script therefore computes a hybrid
Hecke-coefficient object, not the inverse-L coefficient object in Saar's EC
NDC conjecture.

The older script also changes several other variables at once:

```text
rho = 1 + i t complex zero, not BSD real rho = 1
exponential smoothing in c_K
Euler product p <= 5K
D_K multiplied by N^(rho/2) (2pi)^(-rho) Gamma(rho)
absolute values reported
389a1 complex zero only guessed in-script
different bad-prime powers
```

## Invalid comparisons until reconciled

Do not compare the following as evidence for or against the new EC sweep:

1. Raw `D_K*zeta(2)` values from `ndc_gl2_full_test.py` versus
   `Koyama_EC_NDC.csv`.
2. Trends from the old complex-zero Gamma-corrected script versus the BSD
   `rho = 1` sweep.
3. Any constant inferred from `mu(p^2)=a_p^2-p` against a conjecture stated
   with `mu(p^2)=p`.
4. Any rank-2 conclusion from the old `389a1` block until the zero ordinate is
   verified and the coefficient convention is replaced.
5. Any claim that `L(2,E)` is supported by the newer sweep; the local expansion
   rules it out before numerics.

What remains valid from the old script: it is a useful reminder that Gamma
factors, smoothing, and product/sum synchronisation matter for complex zeros.
It is not a valid numerical comparison for this `rho = 1` EC handoff.

## Recommendation

Push this normalization computationally:

```text
D_mix(K) = D_K^E * zeta(2) / C_mix(K)

C_mix(K)
  = (e^gamma log K)^(1/2)
    * product_{p <= K, p good} exp(-a_p/p) * (1 - a_p/p + 1/p)^(-1)
    * C_bad(E).
```

Implementation notes:
- add columns for raw residual product, Mertens-regularised residual product,
  and `D_mix(K)`;
- keep the new inverse convention `mu_E(p^2)=p`;
- first test 37a1, 11a1, 389a1 at the existing checkpoints, then push 37a1
  and 11a1 to `K = 10^6`;
- do not add Gamma factors for the BSD `rho = 1` comparison.

Fallback normalization:

```text
C_2(K)
  = (e^gamma log K)^(1/2)
    * exp( sum_{p <= K, p good} (a_p^2 - 2p)/(2p^2) )

D_2(K) = D_K^E * zeta(2) / C_2(K).
```

This keeps only the `m = 2` Sym^2/adjoint term.  It is less faithful than
`C_mix(K)` but simpler and should reveal quickly whether the missing EC
constant is genuinely second-moment/Rankin-Selberg-shaped.
