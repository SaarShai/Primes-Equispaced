---
schema_version: 1
title: "H1 reciprocal Perron contour-shift theorem candidate"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.84
dependencies:
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_CENTRAL_POLYNOMIAL.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
  - handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
tags: [ec-ndc, h1, reciprocal-perron, contour-shift, residue-control]
---

# H1 Reciprocal Perron Contour-Shift Theorem Candidate

Confidence: 0.84.

Dependencies:
- Same H1 convention as the reciprocal Perron wave:
  `c_E,W(K)=(1/(2 pi i)) int K^z W_hat(z)/L(E,1+z) dz`.
- Analytic rank convention: `r=ord_{s=1} L(E,s)`.
- Kernel convention: `W_hat(z)=int_0^infty W(t)t^(z-1)dt`.
- Prior local algebra:
  `H1_CENTRAL_POLYNOMIAL.md`,
  `H1_OFFCENTRAL_RESIDUE_AGGREGATE.md`,
  `H1_MULTIPLE_ZERO_RANK0_NOGO.md`.
- No external theorem is cited here. Citation protocol not triggered.

## Do Not Promote Unless

- The Mellin/Perron identity is proved for the exact fixed kernel `W`.
- A zero-location hypothesis is declared: either no crossed zeros with
  `Re(rho)>1`, or their exponentially growing residues are retained.
- Reciprocal Laurent coefficients at zeros are controlled; Mellin decay alone
  does not control `1/L'(rho)` or higher coefficients.
- Rank zero is separated: bounded offcentral residues are not `o(1)`.
- Multiple offcentral zeros with effective degree `>= r` are ruled out,
  kernel-cancelled, residue-cancelled, retained, or averaged.
- Horizontal, original-line, and shifted-line tails are proved in the same
  truncation mode.
- H1 and H2 use the same `W`, scale `u=log K`, and theorem mode.
- No BSD, algebraic-rank, cross-curve, or finite-window numerical claim is used
  as analytic input.

## Object

Let

```text
F_u(z) = exp(u z) W_hat(z)/L(E,1+z),       u=log K.
```

The target H1 coefficient is

```text
c_E,W(e^u) = (1/(2 pi i)) int_(Re z=sigma) F_u(z) dz,
```

for some `sigma>0`, after the Mellin/Perron identity has been justified.

## Kernel Hypotheses

Fix `eta>0` and `sigma>0`. The strongest clean local class is:

1. `W` is compactly supported in `[0,1]`, locally regular enough for Mellin
   inversion on `Re z=sigma`.
2. `W(t)=1` near `0+` for the repository normalization. Equivalently,

   ```text
   W_hat(z)=1/z + holomorphic at z=0.
   ```

   More generally replace `1` by `w_-1=Res_(z=0) W_hat(z)`.
3. `W_hat` continues meromorphically to the strip

   ```text
   S = {z: -eta <= Re z <= sigma},
   ```

   with no pole in `S` except the simple pole at `0`. If a chosen smoothstep
   has extra Mellin poles, choose `eta` before the first extra pole or add their
   explicit residues.
4. For every derivative order needed below,

   ```text
   |W_hat^(a)(x+it)| <= C_a (1+|t|)^(-q_a)
   ```

   uniformly for `x in [-eta,sigma]` away from `z=0`. For simple-zero residue
   summability only `a=0` is needed. Multiple zeros of order `m` need
   derivatives through `m-1`.

The Agent-3 smoothstep evidence only supports a finite-decay class such as
`q_0=2` on the relevant strip. Any faster decay is a new kernel assumption.

## Analytic Hypotheses

Use only the following as assumptions, not sourced facts:

1. `L(E,s)` is holomorphic in `1+S`, with isolated zeros and no poles there.
2. The central zero has exact order

   ```text
   r = ord_(s=1) L(E,s).
   ```

3. There is a height sequence `T_n -> infinity` such that no zero of
   `L(E,1+z)` and no noncentral pole of `W_hat` lies on `Im z=+-T_n`.
4. The original vertical integral on `Re z=sigma` is the intended H1 object:

   ```text
   c_E,W(e^u) = lim_(T->infty) (1/(2 pi i))
      int_(sigma-iT)^(sigma+iT) F_u(z) dz.
   ```

5. Residue sums and tails below converge in one declared mode: absolute,
   principal value along `T_n`, pointwise with `T=T(u)`, oscillatory profile, or
   averaged. The mode must be fixed before composition with H2.

## Finite-Box Identity

For a legal height `T`, define

```text
I_sigma(T,u) = (1/(2 pi i)) int_(sigma-iT)^(sigma+iT) F_u(z) dz,
V_eta(T,u)   = (1/(2 pi i)) int_(-eta-iT)^(-eta+iT) F_u(z) dz,
H_+(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x+iT) dx,
H_-(T,u)     = (1/(2 pi i)) int_(-eta)^sigma F_u(x-iT) dx.
```

Let `P_T` be the poles of `F_u` inside the rectangle
`-eta<Re z<sigma`, `|Im z|<T`. Then

```text
I_sigma(T,u)
 = sum_(z0 in P_T) Res_(z=z0) F_u(z)
   + V_eta(T,u) + H_+(T,u) - H_-(T,u).
```

This is the core H1 reduction. Everything else is residue algebra plus bounds
making the limit and error term legitimate.

## Central Residue

Write near `z=0`

```text
1/L(E,1+z) = sum_(j=-r)^infty a_j z^j,
W_hat(z)  = sum_(m=-1)^infty w_m z^m.
```

The central contribution is

```text
Q_E,W(u) = Res_(z=0) F_u(z)
         = sum_(ell=0)^r C_ell u^ell,
```

where

```text
C_ell
 = (1/ell!) [z^(-ell-1)] W_hat(z)/L(E,1+z)
 = (1/ell!) sum_(h=0)^(r-ell) a_(-r+h) w_(r-ell-h-1).
```

The leading coefficient is

```text
C_r = w_-1 / L^(r)(E,1).
```

For normalized kernels, `w_-1=1`, so

```text
Q_E,W(u) = u^r/L^(r)(E,1) + lower powers.
```

Rank zero gives `Q_E,W(u)=w_-1/L(E,1)`, hence `1/L(E,1)` in the
normalized case.

## Offcentral Zero Residues

Let `rho` be a noncentral zero of `L(E,s)` in the crossed strip and set

```text
z_rho = rho - 1.
```

Let its multiplicity be `m_rho`. Near `z=z_rho`, write

```text
1/L(E,1+z)
 = sum_(j=1)^(m_rho) b_(rho,-j) (z-z_rho)^(-j)
   + holomorphic.
```

The exact residue is

```text
R_rho(u)
 = exp(u z_rho)
   sum_(j=1)^(m_rho) b_(rho,-j)
     sum_(ell=0)^(j-1)
       u^ell/ell! *
       W_hat^(j-1-ell)(z_rho)/(j-1-ell)!.
```

For a simple zero,

```text
R_rho(u) = exp(u z_rho) W_hat(z_rho)/L'(E,rho).
```

For a critical-line offcentral zero `rho=1+i gamma`,

```text
R_rho(u) = exp(i gamma u) W_hat(i gamma)/L'(E,1+i gamma).
```

For a multiple zero, the top Laurent coefficient is

```text
b_(rho,-m_rho) = m_rho! / L^(m_rho)(E,rho),
```

and if `W_hat(z_rho) != 0`, the top residue term is

```text
exp(u z_rho)
 b_(rho,-m_rho) W_hat(z_rho) u^(m_rho-1)/(m_rho-1)!.
```

If `W_hat` has exact zero order `h_rho<m_rho` at `z_rho`, the effective degree
is

```text
d_rho = m_rho - 1 - h_rho,
```

with leading term

```text
exp(u z_rho)
 b_(rho,-m_rho) W_hat^(h_rho)(z_rho)
 u^d_rho /(h_rho! d_rho!).
```

If `h_rho>=m_rho`, that pole is kernel-cancelled.

## Tails

The finite-box identity is useful only with explicit tail control.

Original-line truncation:

```text
Tail_sigma(T,u)
 = (1/(2 pi)) int_(|t|>T)
   |exp(u(sigma+it)) W_hat(sigma+it)/L(E,1+sigma+it)| dt.
```

Need `Tail_sigma(T,u)->0` for each fixed `u`, or
`Tail_sigma(T(u),u)=o(u^r)` in a pointwise asymptotic theorem.

Horizontal edges obey the direct bound

```text
|H_+(T,u)| + |H_-(T,u)|
 <= ((sigma+eta)/(2 pi)) exp(sigma u)
    sup_(-eta<=x<=sigma, eps=+-1)
    |W_hat(x+eps iT)/L(E,1+x+eps iT)|.
```

Thus a polynomial form

```text
sup_x |1/L(E,1+x+eps iT)| <= C T^A,
sup_x |W_hat(x+eps iT)| <= C T^(-q)
```

gives

```text
|H_+|+|H_-| <= C exp(sigma u) T^(A-q).
```

For fixed `u`, this vanishes along `T_n` if `A<q`. For a moving truncation it
must be imposed as

```text
exp(sigma u) T(u)^(A-q) = o(u^r).
```

The shifted vertical edge satisfies

```text
|V_eta(T,u)|
 <= exp(-eta u)/(2 pi)
    int_(-T)^T |W_hat(-eta+it)/L(E,1-eta+it)| dt.
```

If the full shifted integral is finite, then

```text
V_eta(infty,u) = O(exp(-eta u)).
```

If only a truncated bound is known,

```text
int_(-T)^T |W_hat(-eta+it)/L(E,1-eta+it)| dt <= M_eta(T),
```

then the theorem needs

```text
exp(-eta u) M_eta(T(u)) = o(u^r).
```

These bounds must avoid boundary zeros. If the reciprocal grows near
horizontal lines, the height sequence must include a quantified avoidance
bound.

## Residue Aggregates

The exact finite expansion is

```text
c_E,W(e^u)
 = Q_E,W(u)
   + lim_(T_n->infty) sum_(z_rho != 0, |Im z_rho|<T_n) R_rho(u)
   + lim_(T_n->infty) V_eta(T_n,u)
```

provided the original-line and horizontal tails vanish and the residue limit
exists in the declared mode.

For a pointwise central asymptotic

```text
c_E,W(e^u) = Q_E,W(u) + o(u^r),
```

the minimal analytic condition is exactly

```text
sum_(rho != 1, crossed) R_rho(u) + V_eta(u) + horizontal/original tails
 = o(u^r).
```

A convenient sufficient critical-line condition is:

```text
for every degree d<r, the degree-d coefficient series is absolutely summable;
for every degree d>=r, the net degree-d critical-line coefficient is zero,
kernel-cancelled, explicitly retained, or averaged.
```

Then critical-line terms of degree `<r` are `O(u^(r-1))=o(u^r)`.

For simple zeros this reduces to

```text
sum_(gamma != 0) |W_hat(i gamma)/L'(E,1+i gamma)| < infinity.
```

This is enough for positive rank `r>=1`, because the simple-zero aggregate is
`O(1)=o(u^r)`. It is not enough for rank zero.

For multiple zeros without kernel cancellation, degree is `m_rho-1`. The
generic pointwise danger condition is

```text
m_rho >= r+1.
```

With kernel zero order `h_rho`, replace it by

```text
m_rho >= r+h_rho+1.
```

## Rank-Zero Boundary

When `r=0`,

```text
Q_E,W(u)=w_-1/L(E,1)
```

A nonzero simple critical-line residue contributes

```text
exp(i gamma u) W_hat(i gamma)/L'(E,1+i gamma).
```

This is main scale. Absolute convergence makes an almost-periodic bounded
function, not a decaying error. Therefore a pointwise rank-zero constant
theorem requires one of:

```text
all nonzero-frequency coefficients vanish;
the oscillatory sum is retained explicitly;
the kernel cancels the relevant zeros;
a product-level averaged theorem is stated and proved.
```

## Claim-Safe Theorem Form

Conditional theorem:

```text
Assume the kernel, analytic, residue-control, and tail hypotheses above.
Assume no crossed zero with Re(z_rho)>0 is silently discarded.

Then the finite-box identity holds at every legal height T.
If the tails vanish and residue sums converge in the declared mode, then

  c_E,W(e^u)
   = Q_E,W(u) + Z_E,W(u) + V_E,W(u),

where Q_E,W is the central polynomial, Z_E,W is the sum of the explicit
offcentral residue polynomials R_rho(u), and V_E,W is the shifted-line
remainder.

If, in addition, Z_E,W(u)+V_E,W(u)=o(u^r), then

  c_E,W(e^u) = Q_E,W(u) + o(u^r).
```

This is the strongest claim-safe H1 statement available from the current wave.
The missing assumptions are not cosmetic; they are exactly the reciprocal
Laurent/residue control and contour-tail estimates.

## Minimal Missing Assumptions

1. Fixed-kernel Mellin/Perron identity on `Re z=sigma`.
2. Strip continuation for `W_hat` and `1/L(E,1+z)` with quantified boundary
   avoidance.
3. No hidden `Re(rho)>1` residue, or explicit retention of every such term.
4. Summability or principal-value control of

   ```text
   b_(rho,-j) W_hat^(a)(rho-1)
   ```

   for all crossed zeros and all derivative orders appearing in `R_rho(u)`.
5. For pointwise positive rank: all effective critical-line degrees `>=r`
   vanish, cancel, are kernel-killed, or are moved into the theorem statement.
6. For pointwise rank zero: all nonzero critical-line residues vanish/cancel,
   or the theorem is oscillatory/averaged.
7. Original-line, horizontal, and shifted-line tail bounds strong enough in
   the same truncation scheme.

## Changed Files

```text
handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
```
