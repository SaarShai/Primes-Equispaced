RIGOROUS_REDUCTION

# H1 Averaged/Oscillatory Fallback

Confidence: 0.72.

Verdict: if pointwise H1 reciprocal Perron control fails or remains
inaccessible, the honest replacement is not the original fixed-curve limit. It
is either:

1. a pointwise oscillatory profile theorem retaining H1/H2 zero terms;
2. a logarithmic/geometric finite-part theorem; or
3. an arithmetic averaged theorem with explicit H1/H2 zero-frequency
   correlation constants.

No cross-curve universality, BSD evidence, H2 package closure, or pointwise
stabilization is promoted here. No external theorem is cited.

## Setup

Use the same fixed elliptic curve `E/Q`, same smoothing kernel `W`, same
Mellin normalization, and same log scale

```text
u = log K,
r = ord_{s=1} L(E,s).
```

H1 is the smoothed reciprocal Perron term:

```text
c_E,W(e^u)
 = Q_r(u) + Z_c(u) + E_c(u),

Q_r(u)
 = q_r u^r + q_(r-1) u^(r-1) + ... + q_0,
q_r = 1/L^(r)(E,1)
```

up to the fixed factorial/Laurent convention chosen by the H1 theorem. That
convention must be stated before use; this note tracks only mode compatibility.

For an offcentral zero `rho=1+i gamma` of multiplicity `m`, H1 pole calculus
can contribute

```text
sum_(0 <= j <= m-1) a_(gamma,j) u^j e^(i gamma u),
gamma != 0.
```

H2, in the Agent 3 local-factor convention, has the possible oscillatory form

```text
log P_E,W(e^u)
 = -r log u + B_E,W + Z_P(u) + E_P(u).
```

The pointwise H2 limit package is the special case `Z_P(u)+E_P(u)=o(1)`. The
averaged H2 fallback is only

```text
A_U (log P_E,W + r log log K) -> B_E,W,
```

where

```text
A_U F = (1/U) integral_U^(2U) F(e^u) du.
```

## Oscillatory Pointwise Mode

If H2 has a pointwise oscillatory log expansion and H1 has a reciprocal-pole
expansion, the honest product statement is

```text
c_E,W(e^u) P_E,W(e^u)
 = exp(B_E,W)
   (q_r + sum_(gamma,j) a_(gamma,j) u^(j-r) e^(i gamma u) + o(1))
   exp(Z_P(u))
```

after dropping central lower powers `q_j u^(j-r)` with `j<r`.

This is a profile theorem, not stabilization to a constant. It is bounded only
under explicit size conditions:

```text
a_(gamma,j) terms with j > r:
  absent, cancelling, or retained with a growing profile warning.

a_(gamma,r) terms:
  retained at constant scale.

a_(gamma,j) terms with j < r:
  lower order in the product.
```

Consequences:

- If `r>=1` and all offcentral H1 zeros are simple, bounded H1 oscillations are
  lower order after multiplication by `u^(-r)`.
- If `r=0`, simple H1 residues are already main scale and must be retained
  unless `Z_c(u)=o(1)` is proved.
- If an offcentral zero has multiplicity `m>=r+1`, H1 can create constant-scale
  or larger oscillations in the product and cannot be hidden in `o(1)`.
- If `Z_P` persists, even a pointwise H1 leading theorem gives a product
  profile multiplied by `exp(Z_P(u))`.

The original fixed-curve limit

```text
c_E,W(K) P_E,W(K) -> exp(B_E,W) / L^(r)(E,1)
```

requires the profile to collapse pointwise to that constant. This is an extra
theorem, not a consequence of smoothing.

## Logarithmic/Geometric Average

The dyadic log average kills fixed nonzero Fourier frequencies:

```text
A_U e^(i gamma u)
 = (e^(2 i gamma U) - e^(i gamma U))/(i gamma U),

|A_U e^(i gamma u)| <= 2/(U |gamma|),
gamma != 0.
```

For infinite zero sums, this is usable only if the average can pass through the
sum, for example via

```text
sum_(gamma != 0) |c_gamma|/|gamma| < infinity
```

or a truncation/mean-square tail bound:

```text
2/U * sum_(0 < |gamma| <= Y(U)) |c_gamma|/|gamma|
 + A_U |sum_(|gamma| > Y(U)) c_gamma e^(i gamma u)|
 = o(1).
```

Central frequency `gamma=0` is never killed. It must be part of `-r log u`,
`Q_r(u)`, the finite constant, or an explicit correlation constant.

A geometric theorem for the product needs a logarithm of the product, or
separate logarithms with fixed branch/sign conventions:

```text
A_U (log c_E,W - r log u)
 = log q_r + o(1),

A_U (log P_E,W + r log u)
 = B_E,W + o(1).
```

Then

```text
A_U log(c_E,W P_E,W)
 = B_E,W + log q_r + o(1).
```

This is a finite-part/geometric-mean statement. It does not imply pointwise
stabilization, ordinary arithmetic averaging, or small coefficient of
variation.

Rank-zero warning: when `r=0`, `c_E,W(e^u)=q_0+Z_c(u)+...` may cross zero or
wind in the complex plane. A log/geometric statement then requires a separate
branch/nonvanishing theorem for `q_0+Z_c(u)`, or it must be stated for a chosen
regularized logarithm. Without that, geometric H1 is not well-defined.

## Arithmetic Average And Correlations

The ordinary averaged product is not determined by averaged `log P`. It needs
a joint zero-frequency theorem.

Assume a mean/Fourier expansion for the H2 exponential:

```text
exp(Z_P(u)) = sum_(eta in Lambda_P) d_eta e^(i eta u)
```

in a Besicovitch/Bohr mean or truncation sense, with

```text
d_0 = Mean(exp(Z_P)).
```

Assume the normalized H1 main-scale profile is

```text
H_c(u)
 = q_r + sum_gamma h_gamma e^(i gamma u)
```

where the retained `h_gamma` are exactly the H1 terms with polynomial degree
`j=r`. Terms with `j<r` vanish in the normalized arithmetic mean; terms with
`j>r` must be absent, cancelled, explicitly normalized away, or declared as a
no-go for bounded averaging.

Then the only claim-safe arithmetic constant is

```text
C_E,W^arith
 = exp(B_E,W) Mean(H_c(u) exp(Z_P(u)))

 = exp(B_E,W)
   (q_r d_0 + sum_gamma h_gamma d_(-gamma)),
```

provided the displayed zero-frequency extraction is justified by absolute
summability or a truncation/mean-square limit.

This formula names the exact required correlations:

- H2 self-correlation: `d_0 = Mean(exp(Z_P))`, generally not `1`.
- H1/H2 cross-correlation: each H1 frequency `gamma` at product scale needs the
  matching H2 exponential coefficient `d_(-gamma)`.
- Rank-zero load-bearing terms:

  ```text
  C_E,W^arith
   = exp(B_E,W)
     Mean((q_0 + Z_c(u)) exp(Z_P(u))).
  ```

- If H2 is actually pointwise nonoscillatory, then `d_0=1` and
  `d_eta=0` for `eta != 0`; the arithmetic constant reduces to the H1
  mean-scale constant.
- If H1 is actually lower-order after normalization and H2 oscillates, the
  arithmetic constant is `exp(B_E,W) q_r Mean(exp(Z_P))`, not
  `exp(B_E,W) q_r` unless `Mean(exp(Z_P))=1`.

Therefore the arithmetic averaged theorem must state its own constant. It
cannot borrow the geometric constant unless the extra identities

```text
Mean(exp(Z_P)) = 1,
sum_gamma h_gamma d_(-gamma) = 0
```

are proved in the same averaging convention.

## No-Go: Averaged Log P Plus Pointwise c

The invalid move is:

```text
A_U (log P_E,W + r log u) -> B_E,W
and
c_E,W(e^u) = q_r u^r + o(u^r)
therefore
c_E,W(e^u) P_E,W(e^u) -> exp(B_E,W) q_r.
```

This does not follow. Averaging `log P` only gives a geometric finite part. If

```text
log P_E,W(e^u)
 = -r log u + B_E,W + Z_P(u) + o(1),
A_U Z_P -> 0,
```

then

```text
P_E,W(e^u)
 = exp(B_E,W) u^(-r) exp(Z_P(u)) (1+o(1)).
```

Persistent `Z_P` blocks pointwise convergence. Its arithmetic mean is governed
by `Mean(exp(Z_P))`, not by `Mean(Z_P)`. This is the core mode mismatch.

Allowed replacements:

```text
Geometric:
  A_U log(c_E,W P_E,W)
  = B_E,W + log q_r + o(1).

Arithmetic:
  A_U (c_E,W P_E,W)
  = C_E,W^arith + o(1),
  with C_E,W^arith defined by joint H1/H2 correlations.

Oscillatory:
  c_E,W(e^u) P_E,W(e^u)
  = exp(B_E,W) H_c(u) exp(Z_P(u)) + o(1).
```

## Claim-Safe Theorem Templates

These are the meaningful final claims if pointwise H1 is not closed. They are
strictly fixed-curve statements.

### Template A: Oscillatory Profile

Assume H1 and H2 have same-kernel expansions as above, errors are small
pointwise after product normalization, `Z_P` is bounded, and no H1 term with
degree `j>r` survives. Then

```text
c_E,W(e^u) P_E,W(e^u)
 = exp(B_E,W) H_profile(u) + o(1),

H_profile(u)
 = (q_r + sum_(j=r) a_(gamma,r)e^(i gamma u)) exp(Z_P(u)).
```

This is the honest fixed-curve oscillatory stabilization target. It promotes
only convergence to an explicit profile, not convergence to a constant.

### Template B: Geometric Mean

Assume the product has a well-defined logarithm in the selected branch and

```text
A_U (log c_E,W - r log u) -> log q_r,
A_U (log P_E,W + r log u) -> B_E,W.
```

Then

```text
A_U log(c_E,W P_E,W)
 -> B_E,W + log q_r.
```

This is meaningful as a finite-part/geometric fixed-curve theorem only.

### Template C: Arithmetic Mean

Assume H1/H2 have joint mean expansions in the same dyadic log windows,
`exp(Z_P)` has mean coefficients `d_eta`, H1 has retained normalized
coefficients `h_gamma`, and all nonretained terms are average-small. Then

```text
A_U (c_E,W P_E,W)
 -> exp(B_E,W) (q_r d_0 + sum_gamma h_gamma d_(-gamma)).
```

This is the only averaged theorem about actual proxy values. Its constant is a
correlation constant, not the geometric constant by default.

What is not meaningful: claiming the original constant
`exp(B_E,W)/L^(r)(E,1)` from either Template B or Template C unless the
geometric/arithmetic correction identities are proved in the same mode.

## Dependencies

1. Same fixed curve `E`, same kernel `W`, same scale `u=log K`, and same
   Mellin convention for H1 and H2.
2. Analytic rank `r=ord_{s=1}L(E,s)` used before any algebraic/script rank.
3. Exact Agent 3 H2 local-factor bookkeeping if `B_E,W` is imported:
   `S_1,W`, `S_sym,W`, `M_good,W`, `R_ge3,W`, and bad-prime constants.
4. H1 reciprocal Perron expansion with central polynomial, offcentral Laurent
   residue degrees, derivative/Laurent coefficient control, and contour tails.
5. Declared theorem mode used everywhere: pointwise limit, oscillatory
   profile, log/geometric average, or arithmetic average.
6. For log/geometric mode: fixed nonzero branch/nonvanishing convention for the
   logged quantity.
7. For arithmetic mode: zero-frequency extraction for `exp(Z_P)` and matching
   H1/H2 correlations in the same dyadic windows.
8. Rank-zero separated from positive rank.
9. Multiple offcentral zeros handled by degree: `j<r` lower order, `j=r`
   retained/correlated, `j>r` no-go unless cancelled or renormalized.

## Do Not Promote Unless

- Do not promote pointwise fixed-curve stabilization from averaged `log P`.
- Do not combine averaged H2 with pointwise H1 and call the product pointwise.
- Do not infer arithmetic averages of `P` or `cP` from averages of `log P`.
- Do not set `Mean(exp(Z_P))=1` without proof.
- Do not discard H1/H2 matching-frequency correlations.
- Do not hide rank-zero H1 simple residues in `o(1)`.
- Do not hide offcentral multiplicity terms with degree `j>=r`.
- Do not import H2 branch damping into H1 reciprocal pole residues.
- Do not omit the H2 symmetric-square/quadratic and bad-prime bookkeeping.
- Do not claim cross-curve universality, BSD evidence, cross-curve constants, or closed
  H2/H1 theorems from this fallback.
- Do not cite external theorems without the project source protocol.

## Changed Files

- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md`

## Commands Run

```bash
pwd && ls
sed -n '1,220p' start.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,260p' L1_index.md
sed -n '1,240p' L0_rules.md
sed -n '1,260p' L1_index.md
ls -la handoff-2026-05-11-h1-reciprocal-perron-wave
git status --short
wc -l HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md H1_H2_COMPOSITION_AUDIT.md H2_POINTWISE_THEOREM_PACKAGE.md handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
rg -n "H1|H2|averag|oscillat|frequency|mode|log P|pointwise|cP|Perron|zero|correlation|fixed-curve|stabil" HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md H1_H2_COMPOSITION_AUDIT.md H2_POINTWISE_THEOREM_PACKAGE.md handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
wc -l handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '1,220p' HANDOFF.md
sed -n '1,220p' L2_facts/farey-claim-ledger.md
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '1,380p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
# apply_patch: add H1_AVERAGED_OSCILLATORY_FALLBACK.md
# apply_patch: add meaningful-final-claims note and verification trail
head -n 20 handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
rg -n "^Confidence:|^## Dependencies|^## Do Not Promote Unless|^## Changed Files|^## Commands Run|cross-curve universality|No-Go|Arithmetic Average|Geometric" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
git diff -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
head -n 20 handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
rg -n "^## Claim-Safe Theorem Templates|meaningful final claims|^## Dependencies|^## Do Not Promote Unless|^## Changed Files|^## Commands Run" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
wc -l handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
rg -n 'H2 package closure|pointwise stabilization is promoted|Do not promote pointwise|Mean\(exp\(Z_P\)\)|d_\(-gamma\)|averaged `log P`' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_AVERAGED_OSCILLATORY_FALLBACK.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```
