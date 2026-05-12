RIGOROUS_REDUCTION

# H1 Central Perron Polynomial

Confidence: 0.94.

Verdict: the central H1 Perron residue is exact local algebra once the smoothed
Perron representation is granted. For the repository-normalized admissible
weights with

```text
W_hat(z) = 1/z + holomorphic at z=0,
```

the leading coefficient of the central polynomial is exactly

```text
1 / L^(r)(E,1),
```

not `r!/L^(r)(E,1)`. The reciprocal Laurent coefficient is
`r!/L^(r)(E,1)`, but the top term of `exp(uz)` contributes the cancelling
factor `1/r!`.

No external theorem is cited. No cross-curve universality, BSD, algebraic-rank, or H2
closure claim is promoted.

## Object

Let

```text
r = ord_{s=1} L(E,s),        u = log K,
c_E,W(K) = (1/(2 pi i)) int_(sigma) K^z W_hat(z)/L(E,1+z) dz.
```

The central polynomial is the residue at `z=0`:

```text
Q_r(u) = Res_(z=0) exp(uz) W_hat(z) / L(E,1+z).
```

It is a polynomial of degree at most `r`, and degree exactly `r` when
`W_hat` has nonzero residue at `0`.

## Coefficient Extraction Formula

Write the Laurent expansions at `z=0`

```text
1/L(E,1+z) = sum_{j=-r}^infty a_j z^j,
W_hat(z)  = sum_{m=-1}^infty w_m z^m.
```

For the admissible kernels in T1/H2, `w_-1 = 1`. More generally, `w_-1` is the
residue of `W_hat` at `0`.

Then

```text
Q_r(u)
 = [z^-1] exp(uz) W_hat(z)/L(E,1+z)
 = sum_{ell=0}^r C_ell u^ell,
```

with exact coefficients

```text
C_ell
 = (1/ell!) [z^(-ell-1)] W_hat(z)/L(E,1+z)
 = (1/ell!) sum_{h=0}^{r-ell} a_{-r+h} w_{r-ell-h-1}.
```

Equivalently,

```text
Q_r(u)
 = sum_{ell=0}^r (u^ell/ell!)
     sum_{j+m=-ell-1} a_j w_m,
```

where the inner sum is finite because `j >= -r` and `m >= -1`.

The central polynomial depends only on

```text
a_-r, a_(-r+1), ..., a_0
w_-1, w_0, ..., w_(r-1).
```

## Dependence On L-Derivatives

Write

```text
L(E,1+z) = sum_{n=r}^infty ell_n z^n,
ell_n = L^(n)(E,1)/n!,
ell_r = L^(r)(E,1)/r! != 0.
```

The Laurent coefficients of `1/L(E,1+z)` are fixed by

```text
a_-r = 1/ell_r = r!/L^(r)(E,1),
```

and, for `h >= 1`,

```text
a_(-r+h)
 = -(1/ell_r) sum_{nu=1}^h ell_(r+nu) a_(-r+h-nu).
```

A normalized form is often cleaner. Define

```text
lambda_0 = 1,
lambda_h = ell_(r+h)/ell_r
         = (r!/(r+h)!) L^(r+h)(E,1)/L^(r)(E,1)       for h >= 1,
beta_0 = 1,
beta_h = - sum_{nu=1}^h lambda_nu beta_(h-nu).
```

Then

```text
a_(-r+h) = (r!/L^(r)(E,1)) beta_h,
```

and the polynomial is

```text
Q_r(u)
 = (r!/L^(r)(E,1))
   sum_{ell=0}^r (u^ell/ell!)
     sum_{h=0}^{r-ell} beta_h w_(r-ell-h-1).
```

This form shows the exact finite dependence: for rank `r`, the central
polynomial uses `L^(r)(E,1), ..., L^(2r)(E,1)` and
`w_-1, ..., w_(r-1)`.

## Leading Coefficient

The top coefficient is obtained by taking `ell=r`, `h=0`, and `w_-1`:

```text
C_r
 = (1/r!) a_-r w_-1
 = (1/r!) (r!/L^(r)(E,1)) w_-1
 = w_-1 / L^(r)(E,1).
```

Therefore:

```text
Q_r(u) = (w_-1/L^(r)(E,1)) u^r + lower powers.
```

For the admissible H1/H2 kernels normalized by `W(t)=1` near `0`,

```text
w_-1 = 1,
Q_r(u) = u^r/L^(r)(E,1) + lower powers.
```

The convention `r!/L^(r)(E,1)` belongs to the Laurent coefficient of
`1/L(E,1+z)`, not to the leading coefficient of the Perron residue polynomial.

## Low-Rank Checks

Rank `0`:

```text
Q_0(u) = w_-1 / L(E,1).
```

With normalized `W`, this is `1/L(E,1)`.

Rank `1`:

```text
Q_1(u)
 = (w_-1/L'(E,1)) u
   + w_0/L'(E,1)
   - w_-1 L''(E,1)/(2 L'(E,1)^2).
```

With normalized `W`, the top coefficient is `1/L'(E,1)`.

Rank `2`:

```text
Q_2(u)
 = (w_-1/L''(E,1)) u^2
   + (2 w_0/L''(E,1)
      - 2 w_-1 L'''(E,1)/(3 L''(E,1)^2)) u
   + C_0,
```

where

```text
C_0 = a_-2 w_1 + a_-1 w_0 + a_0 w_-1,
a_-2 = 2/L''(E,1),
a_-1 = -2 L'''(E,1)/(3 L''(E,1)^2),
a_0  = 2 L'''(E,1)^2/(9 L''(E,1)^3)
       - L''''(E,1)/(6 L''(E,1)^2).
```

These checks match the general formula and isolate the factorial convention.

## What This Does And Does Not Close

This closes only the central pole algebra:

```text
c_E,W(e^u) = Q_r(u) + offcentral reciprocal-pole residues + contour tails,
```

provided the Perron shift is legal in the intended theorem mode.

For positive analytic rank, H1/H2 pointwise composition only needs

```text
Z_c(u) + E_c(u) = o(u^r),
```

where `Z_c` is the offcentral residue aggregate and `E_c` is the shifted-contour
tail. The exact lower central powers in `Q_r` are then harmless after
multiplication by the H2 factor `u^-r`.

For rank zero, `Q_0` is constant scale, so simple offcentral reciprocal
residues are also main scale. Rank zero still needs one of:

```text
Z_c(u) = o(1),
an explicit oscillatory formula retaining Z_c,
or a declared averaged theorem.
```

Multiple offcentral zeros remain outside this central calculation. A zero of
multiplicity `m` at `z=i gamma != 0` contributes a polynomial in `u` of degree
`m-1` times `exp(i gamma u)`, with no central factorial cancellation relevant
to the main `z=0` pole.

## Dependencies

1. Analytic rank first: `r=ord_{s=1}L(E,s)`.
2. Same H1/H2 Mellin convention:

   ```text
   W_hat(z) = int_0^infty W(t)t^(z-1)dt.
   ```

3. Central admissibility: `W_hat(z)=w_-1/z+holomorphic` at `0`; repository
   smoothstep kernels have `w_-1=1`.
4. Local analytic expansion of `L(E,1+z)` with exact zero order `r`.
5. Separate H1 proof for legal contour shifting, offcentral reciprocal-pole
   residues, reciprocal derivative/Laurent growth, multiple zeros, and tails.
6. Separate H2 proof in the same pointwise, oscillatory, or averaged mode.

## Do Not Promote Unless

- The H1 theorem includes this `Q_r(u)` with the same `W_hat` normalization.
- The leading coefficient is stated as `w_-1/L^(r)(E,1)`, hence
  `1/L^(r)(E,1)` only when `w_-1=1`.
- The Laurent coefficient `a_-r=r!/L^(r)(E,1)` is not confused with the
  polynomial leading coefficient.
- Offcentral reciprocal-pole residues and contour tails are proved
  `o(u^r)` for positive-rank pointwise composition, or retained explicitly.
- Rank zero is separated.
- Multiple offcentral zeros are handled or retained.
- No algebraic-rank/BSD substitution is made without an explicit equality
  input.
- No cross-curve universality or closed H2 package is inferred from this central
  calculation.
- Any future external theorem citation follows the required
  `curl + pdftotext + quote + page/eq` protocol.

## Changed Files

- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md`

## Commands Run

```bash
pwd && rg --files -g 'start.md' -g 'HANDOFF.md' -g 'L2_facts/farey-claim-ledger.md' -g 'handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md' -g 'H1_H2_COMPOSITION_AUDIT.md' -g 'handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md' -g 'AGENTS.md'
sed -n '1,220p' ../start.md
sed -n '1,220p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
./te doctor
sed -n '1,220p' token-economy.yaml
test -f L0_rules.md && sed -n '1,220p' L0_rules.md || true
test -f L1_index.md && sed -n '1,220p' L1_index.md || true
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,320p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
find handoff-2026-05-11-h1-reciprocal-perron-wave -maxdepth 2 -type f -print 2>/dev/null | sort
sed -n '1,260p' handoff-2026-05-11-h1-reciprocal-perron-wave/DISPATCH_MANIFEST_2026-05-11.md
rg -n "central residue|central polynomial|Q_r|1/L\\^\\(r\\)|r!/L|lambda_E|W_hat\\(z\\)|Mellin|admissible W|H1" handoff-2026-05-11-ec-theorem-closure-wave handoff-2026-05-11-ec-smoothing-blockers handoff-2026-05-11-ec-h2-mertens-sprint handoff-2026-05-11-ec-s1-explicit-formula-sprint handoff-2026-05-11-gpt55-wave handoff-2026-05-09-followup
find .. -name AGENTS.md -print
git status --short -- HANDOFF.md L2_facts/farey-claim-ledger.md log.md handoff-2026-05-11-h1-reciprocal-perron-wave handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,260p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
tail -n 120 handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
git status --short -- HANDOFF.md L2_facts/farey-claim-ledger.md log.md handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md handoff-2026-05-11-h1-reciprocal-perron-wave/DISPATCH_MANIFEST_2026-05-11.md handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
```

Bootstrap note: `./te doctor` and `token-economy.yaml` were absent from the
specified workspace. No `curl` or `pdftotext` command was run because this file
uses only local algebra and local handoff context, with no external theorem
citation.
