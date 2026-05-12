---
schema_version: 1
title: "H1 fixed-weight mollifier transfer"
date: 2026-05-11
type: proof-attempt
tier: working
status: NO_GO
confidence: 0.83
dependencies:
  - handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md
  - handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
tags: [ec-ndc, h1, mollifier-transfer, no-go]
---

Confidence: 0.83.

Dependencies:
- `handoff-2026-05-11-h1-residue-control-wave/H1_RECIP_DERIVATIVE_SOURCE_HUNT.md`
- `handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md`
- `handoff-2026-05-11-h1-residue-control-wave/KERNEL_ZERO_FILTERING.md`
- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md`

Do Not Promote Unless:
- A fixed-curve theorem controls the exact H1 shell sums
  `sum_{T<|gamma|<=2T} W_hat(i gamma) exp(i gamma u)/L'(1+i gamma)`
  uniformly in `u`, with dyadically summable errors.
- The theorem handles all dyadic shells, not only the range
  `T >= exp(u/theta)`.
- Approximation residuals are bounded against an upper bound for reciprocal
  derivatives or Laurent coefficients; lower negative moments are not used as
  upper bounds.
- Multiple offcentral zeros are ruled out, kernel-killed, retained, averaged,
  or bounded by Laurent-coefficient analogues.
- The same fixed kernel `W` and Mellin normalization are used in H1 and H2.

# H1 Fixed-Weight Mollifier Transfer

## Target

For simple offcentral zeros, positive-rank H1 needs control of

```text
Z_W(u) = sum_{gamma != 0}
  W_hat(i gamma) exp(i gamma u) / L'(E,1+i gamma),
u = log K.
```

For analytic rank `r >= 1`, bounded `Z_W(u)` plus the H1 contour tail gives
`o(u^r)`. Absolute convergence is sufficient, but not necessary.

The question here is whether Li-Zaharescu-style mollified reciprocal-derivative
moments can be transferred to this fixed H1 weight.

Verdict: direct transfer is not plausible. The method gives asymptotics for a
different and much smaller weight class, with length tied to the zero height
`T`. Converting the fixed H1 weight would require a new uniform upper-bound
theorem, not just the cited lower/mollified asymptotics.

## Li-Zaharescu Weight Class

On a dyadic zero shell `T < gamma <= 2T`, Li-Zaharescu use weights

```text
P_X,Y(gamma) = X(rho) Y(1-rho),
X(s)=sum_{n<=M} x_n n^(-s),
Y(s)=sum_{n<=M} y_n n^(-s).
```

On the critical line this expands as a finite log-ratio exponential polynomial:

```text
P_X,Y(gamma)
 = sum_{m,n<=M} c_{m,n} exp(i gamma log(m/n)),
c_{m,n} = x_n y_m / sqrt(mn)       (normalization harmless under EC shifts).
```

Thus the exact approximation class is:

```text
AP_M = span{ exp(i t log(m/n)) : 1 <= m,n <= M }.
```

A single Li-Zaharescu weight is a rank-one bilinear subfamily of `AP_M`; finite
linear combinations give the full ratio-polynomial class, but with coefficient
norms that must still satisfy the contour error bounds.

## Exact Representation

The target shell weight is

```text
G_u(t) = W_hat(i t) exp(i t u).
```

Exact representation in `AP_M` can occur only in exceptional cases:

```text
G_u(t) = finite sum of exp(i t log(m/n)) with m,n <= M.
```

For a generic fixed smoothing kernel this fails. In log variables,
`W_hat(i t)` is a Fourier transform of the log-kernel; multiplying by
`exp(i t u)` shifts its frequency support by `u`. A compact/smooth log-kernel
therefore gives a continuous superposition of frequencies near `u`, not a
finite log-ratio polynomial.

Even the pure phase `exp(i t u)` is exact only if

```text
u = log(m/n),       m,n <= M.
```

For `u=log K` and integer `K`, this requires `M >= K` by taking `m=K,n=1`.

## Uniform Approximation In u

A stable non-superoscillatory approximation to `exp(i t u)` on a shell of
length `asymp T` needs available frequencies near `u`. Since `AP_M` has
frequencies in `[-log M, log M]`, this forces

```text
u + O_W(1) <= log M.
```

Li-Zaharescu take `M=T^theta`. Therefore the method only reaches

```text
T >= exp((u+O_W(1))/theta).
```

This is fatal for H1. The dyadic shells

```text
1 <= T < exp(u/theta)
```

contain the low and medium zeros whose residues must be controlled in the H1
asymptotic. They are not a harmless tail. Kernel decay damps large `T`, but it
does not remove the need to control these omitted shells.

Truncation lengths:

```text
Core S1 asymptotic:       M = T^theta, theta < 1.
Reciprocal mollifier use: M = T^theta, theta < 1/(2+theta_L)-epsilon;
                          the paper records theta < 2/5 as valid.
Exact phase K=e^u:        needs M >= K, hence T >= exp(u/theta).
```

Thus the reciprocal-mollifier length would require roughly
`T >= exp((5/2+o(1))u)` for the exact phase, leaving an even larger uncontrolled
initial range.

## Approximation Error Needed

Let `P_{T,u} in AP_{T^theta}` approximate `G_u` on `T<|t|<=2T`, and define

```text
eps_T(u) = sup_{T<|t|<=2T} |G_u(t)-P_{T,u}(t)|.
```

The residual is bounded only by

```text
eps_T(u) * sum_{T<|gamma|<=2T} |1/L'(1+i gamma)|.
```

So a transfer theorem needs an upper reciprocal-derivative input. For example,
if

```text
J_2(T) = sum_{T<|gamma|<=2T} |1/L'(1+i gamma)|^2
       <= C T^beta (log T)^B
```

and zero counting gives `N(T,2T) << T log T`, then Cauchy-Schwarz gives

```text
residual_T(u)
 << eps_T(u) T^((beta+1)/2) (log T)^((B+1)/2).
```

Dyadic summation requires

```text
sum_T eps_T(u) T^((beta+1)/2) (log T)^((B+1)/2) < infinity
```

uniformly in `u`, plus summability of the Li-Zaharescu contour errors for the
chosen coefficients. No cited theorem supplies this. Without such an upper
moment, approximation residuals cannot be estimated at all.

## Li-Zaharescu Error After Dyadic Summation

For a usable shell, Li-Zaharescu's Theorem 4.1 has the schematic form

```text
S1(P_X,Y;T)
 = (T2-T1)/(2pi) * diagonal(x,y) + E1(T,M,x,y).
```

To transfer H1 one would need

```text
sum_{dyadic T}
  |E1(T,T^theta,x_{T,u},y_{T,u})|
  = O(1)                         uniformly in u
```

or at least `o(u^r)` after composition. This is not automatic. The `E1` terms
depend on `l1`, `linfty`, and `l2` norms of the approximating coefficients. Any
superoscillatory approximation for `u > log M` would have huge norms and would
destroy the contour error. Restricting to bounded-norm approximants returns the
length barrier `u <= log M`.

If one assumes a friendly approximant with kernel-scale coefficient norms,
smoothstep decay `|W_hat(iT)| << T^(-2)` would plausibly make the large-shell
Li-Zaharescu errors summable for fixed `u`. That still does not address the
uncontrolled shells `T < exp(u/theta)` or the residual term above.

## Upper Bounds Versus Lower/Mollified Asymptotics

Li-Zaharescu do not give the required H1 upper bound.

They provide:

```text
1. lower bounds for negative moments;
2. signed mollified asymptotics for S1;
3. existence of very small L'(rho) in some settings.
```

H1 needs either:

```text
sum_T |sum_{T<|gamma|<=2T} G_u(gamma)/L'(1+i gamma)| < infinity
```

or a pointwise/principal-value theorem proving cancellation uniformly in `u`.
Lower bounds for negative moments point in the opposite direction: they show
large reciprocal derivatives exist on average, not that the fixed H1 residue
aggregate is bounded.

## Transfer Theorem Decision

Direct theorem:

```text
Li-Zaharescu mollifier asymptotics
  => fixed H1 residue bound for W_hat(i gamma) exp(i gamma u)
```

is `NO_GO`.

The most that survives is a conditional research program:

```text
For each dyadic T and u with u <= theta log T - O_W(1),
construct bounded-norm ratio-polynomial approximants P_{T,u};
prove Li-Zaharescu-style signed asymptotics for P_{T,u};
prove an independent upper reciprocal-derivative/Laurent bound for the residual;
sum all shell errors, including the low-shell range not covered by u <= log M.
```

This is a new theorem, not a transfer from existing Li-Zaharescu results.

## Citation Packet

Li-Zaharescu, `Value Distribution Of L'(rho)`.

Fetch/extract:

```bash
mkdir -p /tmp/h1-fixed-weight-mollifier-transfer
curl -L --fail -o /tmp/h1-fixed-weight-mollifier-transfer/li_zaharescu_Lprime_rho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
shasum -a 256 /tmp/h1-fixed-weight-mollifier-transfer/li_zaharescu_Lprime_rho.pdf
curl -L --fail -o /tmp/h1-fixed-weight-mollifier-transfer/xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf /tmp/h1-fixed-weight-mollifier-transfer/xpdf-tools-mac-4.06.tar.gz \
  -C /tmp/h1-fixed-weight-mollifier-transfer
/tmp/h1-fixed-weight-mollifier-transfer/xpdf-tools-mac-4.06/bin64/pdftotext \
  -layout -enc UTF-8 \
  /tmp/h1-fixed-weight-mollifier-transfer/li_zaharescu_Lprime_rho.pdf \
  /tmp/h1-fixed-weight-mollifier-transfer/li_zaharescu_Lprime_rho.pdftotext.txt
```

SHA256:

```text
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
```

Source facts used:

- PDF p. 2, Theorem 1.1: lower bound for the negative moment of `L'(rho)`.
- PDF pp. 3-4, equations (9)-(11): defines `S0`, `S1`, `S2` using
  Dirichlet polynomials `X,Y`; `S1` contains `L'(rho)^(-1)X(rho)Y(1-rho)`.
- PDF p. 7, Theorem 4.1: assumes RH, almost-all simplicity, and
  `M=T^theta, theta<1`, then evaluates `S1` by a diagonal term plus `E1`.
- PDF pp. 13-14, proof of Theorem 1.1: chooses
  `x_n=mu(n)a(n), y_n=x_n` and then restricts
  `theta < 1/(2+theta_L)-epsilon`; the text records `theta<2/5` as valid.

Extraction note: Xpdf drops the prime glyph in parts of the text layer, writing
`L (rho)` where the PDF mathematics is `L'(rho)`. The title, formulas, and
surrounding notation identify the derivative.
