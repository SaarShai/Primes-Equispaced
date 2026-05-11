---
schema_version: 1
title: "Agent 08 S1 cut-plane log-growth proof attempt"
date: 2026-05-11
agent: "Wave 3 Agent 08"
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
tags: [breakthrough-wave-3, h2, s1, cut-plane, log-growth, endpoint-contour]
---

# Agent 08 S1 Cut-Plane Log-Growth Proof Attempt

## Status

`RIGOROUS_REDUCTION`.

No theorem is promoted. The endpoint contour shift is legal after one precise
repair:

```text
replace literal global-branch left-edge absolute integrability
by renormalized regular-log left-edge integrability,
```

or strengthen the endpoint kernel from `|W_hat| << |t|^-2` to
`|W_hat| << |t|^(-2-epsilon)`.

With the current Wave 2 wording and smoothstep-scale `|W_hat|,|W_hat'| << |t|^-2`,
the local cut terms and truncation sequence are controllable, but a single
global logarithm on the cut plane can accumulate `2 pi i N(t)` on the left edge.
That accumulated branch constant is not absolutely integrable against `t^-2`
from zero counting alone.

## Target

Attack:

```text
S1-CutPlane-LogGrowth(E,W,eta)
```

for fixed elliptic curve `E/Q`, analytic rank only

```text
r = ord_{s=1} L(E,s),
```

endpoint kernel `W` with

```text
W_hat(z)=1/z+O(1),      W_hat,W_hat' << (1+|t|)^(-2)
```

on the shifted strip, and

```text
A_E(z)=sum_{p good} a_p p^(-1-z).
```

Use the branch identity from Wave 2:

```text
A_E(z)
 = log L_good(E,1+z)
   - (1/2) log L_sym,E^good(1+2z)
   + (1/2) log zeta_good(1+2z)
   + Phi_E(z),
```

where `Phi_E` is holomorphic for `Re z > -1/4`.

## Source Protocol

Run directory:

```bash
/tmp/agent08-s1-sources-20260511
```

Commands:

```bash
curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236
curl -L --fail -o ils_math_9901141.pdf https://arxiv.org/pdf/math/9901141
curl -L --fail -o hoffstein_lockhart_maass_siegel.pdf https://www.math.columbia.edu/~goldfeld/CoeffMaassForms.pdf
curl -L --fail -o friedlander_iwaniec_opera_ch1.pdf https://assets.press.princeton.edu/chapters/s8585.pdf
curl -L --fail -o zeta_zero_count_arxiv_2107.06506.pdf https://arxiv.org/pdf/2107.06506
curl -L --fail -o xpdf-tools-mac.tar.gz https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac.tar.gz
./xpdf-tools-mac-4.06/binARM/pdftotext -layout sheth_ec_arxiv_2312.05236.pdf sheth_ec_arxiv_2312.05236.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout ils_math_9901141.pdf ils_math_9901141.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout hoffstein_lockhart_maass_siegel.pdf hoffstein_lockhart_maass_siegel.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout friedlander_iwaniec_opera_ch1.pdf friedlander_iwaniec_opera_ch1.txt
./xpdf-tools-mac-4.06/binARM/pdftotext -layout zeta_zero_count_arxiv_2107.06506.pdf zeta_zero_count_arxiv_2107.06506.txt
```

SHA256:

```text
d764514b3ff1c7713e9bc97ac81c708857f1ba0b38085903850e06a1f665079d  sheth_ec_arxiv_2312.05236.pdf
5072c63324c329250f70c4ef4e2648a0e8ff465d6b9c241c3d3646d4c6759997  ils_math_9901141.pdf
031de26f73977602225ec96b2207f3070cfc7d6b3cfc2371faed52ee254fb632  hoffstein_lockhart_maass_siegel.pdf
080fbff5d5f122678cddd78a1b0561a79952c5fe72b49cf2fbc6b014edc0e8dc  friedlander_iwaniec_opera_ch1.pdf
3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf  zeta_zero_count_arxiv_2107.06506.pdf
```

Checked anchors:

- Sheth, arXiv:2312.05236v4, PDF p. 13, Theorem 3.1:
  `N_E(t)=c_E t(log t+c)+O(log t)`. Use: EC zero-counting for pure
  multiplicity branch sums. Same page, Corollary 3.2: reciprocal-square zero
  sum "converges".
- Iwaniec-Luo-Sarnak, arXiv:math/9901141, PDF p. 11, equations (13)-(15):
  symmetric-square "Euler product of degree 3 is entire"; functional equation
  is equation (14).
- Hoffstein-Lockhart, Annals 140 (1994), PDF p. 3, equations (0.6)-(0.8):
  "adjoint square lift"; `L(s,F)` is "known to be entire".
- Friedlander-Iwaniec chapter, PDF p. 17, Theorem 1.2/equation (1.4.17):
  ordinary Mertens finite part `sum_{p<=x}1/p=log log x+C+o(1)`.
- Hasanalizade-Shen-Wong, arXiv:2107.06506, PDF p. 1, Corollary 1.2/equation
  (1.5): `N(T)` counts "non-trivial zeros" of zeta and satisfies an explicit
  Riemann-von Mangoldt error bound.

No external automorphic logarithm theorem is imported. The selected-height
logarithm lemma below is an in-repo reduction from finite-degree growth plus
zero counts; it is not cited as an external theorem.

Source status of zero ledgers: EC and zeta counts are source-checked above.
Sym2 zero/pole counting is inherited as the finite-degree/Jensen reduction from
Wave 2 Agent 06 using the ILS/Hoffstein-Lockhart anchors; this packet does not
promote a separate external Sym2 zero-count theorem.

## Clause Check

### 1. Horizontal log growth

For each factor `F` in

```text
L_good(E,1+z), L_sym,E^good(1+2z), zeta_good(1+2z),
```

the needed statement is:

```text
there exist T_n -> infinity, avoiding branch ordinates, such that
|Log F(linear z)| << (log T_n)^B
```

uniformly for `-eta <= Re z <= c` on `Im z = +/-T_n`, away from cut
neighborhoods.

Reduction proof under the zero-ledger input for each factor:

1. In each dyadic interval `[T,2T]`, the ledger gives `O(T log T)` branch
   ordinates. This is source-checked for `L(E,s)` and zeta, and reduced to
   finite-degree/Jensen input for Sym2.
2. Partition into unit intervals. At least one interval has `O(log T)` branch
   ordinates.
3. Remove intervals of radius

   ```text
   delta_T = exp(-(log T)^A)
   ```

   around those ordinates. The remaining set is nonempty.
4. On the chosen height, a Jensen/Cartan local factorization gives

   ```text
   Log F(s) = sum_{|gamma-T|<=1} m_gamma log(s-rho) + H_T(s),
   H_T(s) << log T.
   ```

   Since there are `O(log T)` nearby branches and
   `dist(s,rho) >= delta_T`, this gives

   ```text
   |Log F(s)| << (log T)^(A+1).
   ```

Thus the horizontal edges satisfy

```text
int_horizontal K^z W_hat(z) A_E(z) dz
  <<_{K,W} T_n^(-2) (log T_n)^B -> 0
```

for fixed `K` as `n -> infinity`.

This closes the horizontal-truncation mechanism modulo the standard
finite-degree growth input for the three sourced/global objects. It does not
settle right-branch removal.

### 2. Cut-lip integrability

Let `a=beta+i gamma` be a branch point in `-eta <= beta <= c` with local
coefficient

```text
A_E(z)=c_a log(1/(z-a)) + holomorphic.
```

The left-going cut contribution is

```text
I_a(u)
 = c_a K^a int_0^(beta+eta) e^(-u v) W_hat(a-v) dv,
u = log K.
```

The absolute majorant is

```text
|I_a(u)| <= |c_a| K^beta u^(-1)
  sup_{0<=v<=beta+eta} |W_hat(a-v)|.
```

For `beta <= 0`, dyadic zero counting and `|W_hat| << |gamma|^-2` give

```text
sum_a |c_a| sup_v |W_hat(a-v)|
  << sum_j (2^j j) 2^(-2j) < infinity.
```

This proves absolute cut-lip summability for all non-right branches. Branches
with `beta>0` cannot be discarded; they must be retained as

```text
c_a K^a W_hat(a)/log K + lower terms.
```

### 3. Local cut remainders

Taylor expansion on the cut gives

```text
W_hat(a-v) = W_hat(a) + O(v sup_{0<=x<=v}|W_hat'(a-x)|).
```

Therefore

```text
I_a(u)
 = c_a K^a W_hat(a)/u
   + O(|c_a| K^beta M_a/u^2)
   + O(|c_a| K^beta e^(-eta u) M_a),
```

where

```text
M_a = sup_{0<=v<=beta+eta} (|W_hat(a-v)|+|W_hat'(a-v)|).
```

The same dyadic count proves

```text
sum_{beta<=0} |c_a| M_a < infinity.
```

Thus local Watson remainders sum to

```text
O_E,W((log K)^(-2)) + O_E,W(K^(-eta))
```

after excluding or retaining right branches.

### 4. Left-edge decay

This is the only nonlocal obstruction.

If the theorem uses a renormalized regular logarithm

```text
R_F(z) = Log F(z) - sum_{a in strip} m_a log(z-a)
```

with local logarithms fixed independently, then the same finite-degree log input
gives

```text
|R_F(-eta+it)| << (log |t|)^B
```

outside harmless local indentations. Hence

```text
K^(-eta) int_R |W_hat(-eta+it)| |R_F(-eta+it)| dt
  << K^(-eta).
```

But a literal single-valued global branch on the full cut plane is different.
With left-going cuts, the branch value on the left edge changes by

```text
2 pi i * sum_{0<gamma<t} c_(beta+i gamma)
```

as the edge crosses cut endpoints. For the `L(E,s)` zero branches, the
absolute size is bounded below in the model case by a zero-counting term of
size `N_E(t)`. Source-checked zero counting only gives

```text
N_E(t) = O_E(t log t).
```

At smoothstep scale,

```text
int^infinity N_E(t) |W_hat(-eta+it)| dt
  behaves like int^infinity (t log t) t^(-2) dt,
```

which diverges. Therefore literal global-branch absolute left-edge
integrability is not available from the current inputs.

Repair options:

1. State `S1-CutPlane-RenormalizedLogGrowth`: subtract explicit local branch
   logs, integrate only the regular remainder on the left edge, and add branch
   jumps through the cut-lip formula.
2. Strengthen the endpoint kernel to

   ```text
   |W_hat|, |W_hat'| << (1+|t|)^(-2-epsilon).
   ```

   Then even the accumulated global branch constant is absolutely integrable.
3. Keep `|t|^-2` and prove cancellation in the cumulative branch coefficient.
   No such theorem is known here and none was sourced.

### 5. Truncation sequence

The selected heights from Clause 1 also avoid cut endpoints and local disks.
For finite rectangles, Cauchy's theorem applies on the cut plane. Letting
`T_n -> infinity` is legitimate for:

- horizontal edges, by `T_n^-2 polylog(T_n) -> 0`;
- local cut sums, by absolute convergence of `sum |c_a| M_a`;
- renormalized left edge, by the displayed `K^-eta` integral.

It is not legitimate for the literal accumulated global branch at `q=2`
without one of the repairs above.

## Reduced Theorem That Is Actually Usable

The legal replacement is:

```text
S1-CutPlane-RenormalizedLogGrowth(E,W,eta).
```

Hypotheses:

1. The Wave 2 branch identity for `A_E(z)` holds in `Re z > -eta`.
2. All singularities in the strip are logarithmic branches, with coefficients
   `c_a`, plus explicitly listed finite ramified factors.
3. No branch with `Re a>0` is discarded; right branches are absent or retained.
4. The sourced/finite-degree zero ledger gives

   ```text
   sum_a |c_a| sup_{0<=v<=eta}
     (|W_hat(a-v)|+|W_hat'(a-v)|) < infinity.
   ```

5. The regularized logarithmic remainders on the left edge satisfy polylog
   growth or direct `W_hat`-weighted integrability.
6. Selected horizontal heights satisfy the zero-avoidance construction above.

Conclusion:

```text
S_1,W^good(K)
 = c_0 log log K + C_1,E,W
   + (1/log K) sum_{a != 0, Re a <= 0} c_a K^a W_hat(a)
   + retained_right_branch_terms
   + O_E,W((log K)^(-2))
   + O_E,W(K^(-eta)).
```

Here

```text
c_0 = 1/2 + kappa_sym/2 - r,
```

with `r=ord_{s=1}L(E,s)` analytic rank only. Under the Wave 2 source-closed
standard adjoint/Sym2 reconciliation, `kappa_sym=0`; this packet does not
reprove that component.

If all right branches are absent and the `Re a=0` branch sum is absolutely
summable, then the offcentral aggregate is `O(1/log K)` and

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K + C_1,E,W + o(1).
```

## Exact Blocker

`S1-CutPlane-LogGrowth(E,W,eta)` should not be promoted in its literal
global-branch form at `|W_hat| << |t|^-2`.

The blocker is not horizontal growth, not cut-lip summability, and not local
Watson remainders. It is the left-edge branch normalization:

```text
global branch accumulation: 2 pi i N(t)
kernel damping:             t^-2
absolute integral:          int log t / t dt diverges
```

The theorem is salvageable by the renormalized-log statement above. That is the
recommended Wave 3 handoff target for S1 endpoint closure.

## H1 Boundary

This packet concerns logarithmic branch terms in H2/S1 only. The resulting
`1/log K` branch damping is not reciprocal-pole damping for H1 and is not used
to control

```text
1 / L'(E,1+i gamma).
```

No Koyama correspondence or email draft was touched.

## Changed File

```text
primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT08_S1_CUTPLANE_LOG_GROWTH_2026-05-11.md
```
