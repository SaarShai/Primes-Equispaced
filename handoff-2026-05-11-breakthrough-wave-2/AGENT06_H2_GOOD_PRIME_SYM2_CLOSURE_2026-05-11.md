---
schema_version: 1
title: "Agent 06 H2 exact good-prime Sym2 closure"
date: 2026-05-11
agent: "Breakthrough Wave 2 Agent 06 - H2 Exact Good-Prime Sym2 Closure"
type: closure-packet
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
tags: [ec-ndc, h2, sym2, good-prime, source-closure]
---

# Agent 06 H2 Exact Good-Prime Sym2 Closure

## Status Enum

- `SOURCE_CLOSED`: source-verified analytic input plus in-repo finite-part transfer.
- `CLOSED`: proved by local algebra or finite correction.
- `CONDITIONAL`: valid from stated hypotheses, not source-promoted here.
- `BLOCKED`: missing source/proof.
- `NOT_PROMOTED`: do not cite as a full EC H2 theorem.

Overall status: `RIGOROUS_REDUCTION`.

Component label: `SOURCE_CLOSED` for the exact good-prime Sym2 finite-part
theorem below; `NOT_PROMOTED` for full H2, because S1 branch-contour closure
is still outside this packet.

## Exact Object

Fix an elliptic curve `E/Q` and use analytic rank only elsewhere:

```text
r = ord_{s=1} L(E,s).
```

For good primes:

```text
lambda_p = a_p / sqrt(p),
u_p v_p = 1,
u_p + v_p = lambda_p,
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

The exact good-prime object is

```text
L_sym,E^good(s)
 = product_{p good}
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1).
```

For `Re(s)>1`,

```text
log L_sym,E^good(s) = D_sym,E(s) + H_sym,E(s),
D_sym,E(s) = sum_{p good} chi_sym2(p) p^(-s),
H_sym,E(s) =
  sum_{p good} sum_{m>=2}
   (u_p^(2m) + 1 + v_p^(2m))/(m p^(ms)).
```

`H_sym,E(s)` is absolutely convergent at `s=1`, since `|u_p|=|v_p|=1` at
good primes and the first retained power is `p^(-2s)`.

## Source Closure

Source anchors, already fetched in `/tmp/agent6-source-packet-20260511`:

- Iwaniec-Luo-Sarnak, arXiv:math/9901141, SHA256
  `5072c63324c329250f70c4ef4e2648a0e8ff465d6b9c241c3d3646d4c6759997`.
  PDF p. 11, equations (13)-(15): "Euler product of degree 3 is entire";
  functional equation displayed.
- Hoffstein-Lockhart, Annals 140 (1994), SHA256
  `031de26f73977602225ec96b2207f3070cfc7d6b3cfc2371faed52ee254fb632`.
  PDF pp. 2-4, equations (0.6)-(0.8): "adjoint square lift";
  `L(s,F)` is "entire, and L(1,F) != 0"; methods are stated to apply to
  holomorphic forms.

Use these as follows. The global adjoint/symmetric-square source gives a
degree-3 automorphic `L_sym,E^glob(s)` whose good-prime Euler factors match
the displayed `L_sym,E^good(s)`. Hoffstein-Lockhart also makes explicit that
the difference from Rankin-Selberg at ramified primes is a finite product over
`p|N_E`.

Therefore write

```text
L_sym,E^glob(s) = L_sym,E^good(s) R_bad,sym,E(s),
```

where `R_bad,sym,E(s)` is a finite product of ramified local factors in the
chosen global convention. For the standard EC adjoint factors,
`R_bad,sym,E(1)` is finite and nonzero. Hence

```text
kappa_sym = ord_{s=1} L_sym,E^good(s) = 0.
```

Do not reuse this value under a different global local-factor convention until
the displayed finite correction is rechecked at `s=1`.

## Finite-Part Theorem

Let `W` be the endpoint kernel used by H2:
compact support in `[0,1]`, `W_hat(z)=1/z+O(1)` at zero, and
`W_hat,W_hat' <<_W (1+|t|)^(-2)` on the shifted strips.

Then

```text
S_sym,W(K) = sum_{p good} W(p/K) chi_sym2(p)/p
           = C_sym,E
             - (1/log K) sum_{rho != 1}
                 m_rho K^(rho-1) W_hat(rho-1)
             + O_W((log K)^(-2)) + O_E,W(K^(-eta)),
```

where `rho` ranges over noncentral zeros/poles of the exact
`L_sym,E^good(s)` in the shifted strip, counted with

```text
m_rho = ord_{s=rho} L_sym,E^good(s).
```

The central constant is

```text
C_sym,E = log L_sym,E^good(1) - H_sym,E(1)
```

under the source-closed `kappa_sym=0` convention, with the logarithm taken by
continuation from the real side `s>1`. If a future convention has central
order `kappa_sym != 0`, replace the theorem by

```text
S_sym,W(K)
 = -kappa_sym log log K
   + log L_sym,E^{good,*}(1) - H_sym,E(1) - kappa_sym gamma_E
   + offcentral branch terms + o(1).
```

## Zero/Pole Summability

Status: `SOURCE_CLOSED` for the global zeros plus `CLOSED` finite ramified
correction.

Reason:

```text
global Sym2/ad L: entire degree 3, fixed E, functional equation;
bad correction: finite product over p|N_E;
kernel: W_hat,W_hat' = O((1+|t|)^(-2)).
```

The global zero count needed here follows by the standard Jensen argument from
the sourced entire finite-degree functional equation:

```text
N_sym,E(T) = O_E(T log T).
```

Even the weaker finite-order bound `O_E(T^(1+epsilon))` would be enough for
the `|t|^-2` kernel. Ramified local correction factors add only finitely many
vertical arithmetic progressions of zeros/poles; their weighted sums also
converge absolutely.

Thus, for every fixed shifted strip used by the H2 contour,

```text
sum_{rho != 1} |m_rho|
  sup_{0<=v<=eta}
  (|W_hat(rho-1-v)| + |W_hat'(rho-1-v)|) < infinity,
```

after excluding any explicitly listed ramified local singularity with
`Re(rho)>1`. For standard EC adjoint local factors no such right-of-one
ramified singularity occurs. If a future source convention produces one, the
finite-part theorem must retain its term; pointwise H2 cannot drop it.

Consequences:

```text
Z_sym,E,W(K)
 = -(1/log K) sum_{rho != 1} m_rho K^(rho-1) W_hat(rho-1)
 = O_E,W(1/log K) = o(1)
```

when all retained singularities satisfy `Re(rho)<=1`. Singularities with
`Re(rho)<1` are power-decaying. Singularities on `Re(rho)=1`, `rho!=1`, are
only `1/log K` oscillations.

## Ramified/Global Reconciliation

Safe workflow for any future citation:

1. Identify the global source convention `L_sym,E^glob`.
2. Write its good-prime factors and verify they match
   `(1-u_p^2p^-s)^(-1)(1-p^-s)^(-1)(1-v_p^2p^-s)^(-1)`.
3. Define the finite correction
   `R_bad,sym,E = L_sym,E^glob / L_sym,E^good`.
4. Check `R_bad,sym,E(1)` is finite nonzero before setting
   `kappa_sym=0`.
5. Add zeros/poles of `R_bad,sym,E` to the offcentral ledger if the proof
   moves contours through their vertical progressions.

This packet closes the exact Agent-3 good-prime normalization because the
quoted adjoint-square source has finite bad-prime factors and a nonzero
central adjoint value. It does not authorize replacing `chi_sym2(p)` by a
global ramified coefficient at bad primes inside `S_sym,W`.

## H2 Compatibility

The closed local H2 identity remains:

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E,W(K).
```

With this packet:

```text
S_sym,W(K) = C_sym,E + o(1).
```

The S1 theorem must still use the same convention:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K + C_1,E,W + o(1).
```

Here `kappa_sym=0`, so the S1 coefficient becomes `1/2-r`. The full H2
coefficient is still

```text
(1/2 - r) + 0 - 1/2 = -r.
```

No H2 damping is imported into H1. This packet concerns logarithmic branch
terms in the Sym2 prime-log sum only.

## Remaining Dependency Map

Closed here:

- exact good-prime Sym2 Euler product with first coefficient
  `chi_sym2(p)=a_p^2/p-1`;
- `kappa_sym=0` for the standard global adjoint/Sym2 reconciliation;
- higher prime-power correction finite at `s=1`;
- Sym2 offcentral zero/pole weighted summability for the endpoint kernel;
- ramified local-factor reconciliation as finite correction.

Still not closed here:

- S1 branch-only continuation and legal endpoint contour shift;
- horizontal/left-edge estimates for `S_1,W`;
- full pointwise H2 theorem;
- any H1 reciprocal-pole estimate;
- any Koyama correspondence or email draft.

## Verification Notes

Commands run:

```text
./te doctor
sed -n '1,220p' start.md
sed -n '1,260p' primes-equispaced/L1_index.md
sed -n targeted H2/Sym2 packets named in the dispatch
rg source-protocol and Sym2 anchors in SOURCE_PACKET.md
pdftotext page checks for ILS and Hoffstein-Lockhart from /tmp source packet
shasum -a 256 ils_math_9901141.pdf hoffstein_lockhart_maass_siegel.pdf
```

Changed files:

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-2/AGENT06_H2_GOOD_PRIME_SYM2_CLOSURE_2026-05-11.md
```
