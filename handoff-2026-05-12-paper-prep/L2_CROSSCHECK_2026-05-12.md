# mpmath-L2 cross-check report

- started: 2026-05-12T16:46:22.676765Z
- finished: 2026-05-12T16:46:39.136531Z
- mpmath dps: 50
- K (Mobius/c_K cross-check): 200000

## Algorithm independence

- **L1 algorithm** (Koyama_C1.py): mpmath `dirichlet()`
  function (Riemann-zeta-based internal recipe), analytic
  derivatives `mp.diff` for L' and L''; sieve from
  `koyama-shared/scripts/`.
- **L2 algorithm** (this script): Hurwitz-zeta sum
  $L(s,\chi) = q^{-s} \sum_{a=1}^{q} \chi(a)\,\zeta(s, a/q)$,
  central-difference numerical derivatives at three independent
  step sizes $h\in\{10^{-12},10^{-15},10^{-18}\}$,
  fresh linear sieve for $\mu(n)$ from scratch.

## Per-pair agreement

| Pair | $|\Delta L'|$ | $|\Delta L''|$ | $|\Delta C_1|$ | $|R(K)|$ (L2) | $|R(K)|$ (L1 ref) |
|---|---|---|---|---|---|
| `chi_-4/z1` | `4.189e-12` | `1.825e-12` | `2.846e-13` | `0.134447` | `0.134447` |
| `chi_-4/z2` | `1.162e-12` | `1.684e-12` | `1.442e-13` | `0.257279` | `0.257279` |
| `chi_5` | `4.068e-12` | `5.833e-12` | `4.976e-13` | `0.245896` | `0.245896` |
| `chi_11` | `2.55e-12` | `2.962e-12` | `2.468e-13` | `0.210102` | `0.210102` |

## Verdict

- L1 vs L2 agreement on `L'`, `L''`, `C_1` is bounded by the
  central-difference step size: at the chosen step sizes the
  agreement should be `~10^{-9}` or better on each component for
  values of magnitude `~1`. Any pair exceeding that is flagged.
- L1 vs L2 agreement on `|R(K)|` should be to many digits because
  the only differences are the (independent) `μ` sieve and the
  (independent) `L'` value used in `log K / L'`. A consistent
  match at `K = 200,000` is the spot-check this lane provides.

- **PARI/GP L2 (true second-language verification)** is not
  available on the current host (no `gp`, `pari`, `cypari2`,
  or `brew` installation). Recorded as the next verification
  step in the reproducibility manifest.
