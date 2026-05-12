---
schema_version: 1
title: "T1 smoothed Perron theorem/reduction for EC smoothing"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.62
sources:
  - HANDOFF.md
  - L2_facts/farey-claim-ledger.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
  - handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
  - handoff-2026-05-11-ec-smoothing-blockers/DISPATCH_MANIFEST.md
tags: [ec-ndc, smoothing, perron, mellin, euler-product, claim-safe]
---

# T1 Smoothed Perron Theorem/Reduction

Status: `RIGOROUS_REDUCTION`

No theorem is promoted. The strongest honest result is a conditional reduction:
if the smoothed reciprocal-coefficient Perron expansion and the matching
smoothed Euler-product Mertens expansion both hold with explicit off-central
zero control, then `c_E,alpha(K) P_E,alpha(K)` stabilizes for a fixed elliptic
curve. This explains why smoothing can suppress endpoint drift. It does not
explain cross-curve universality, and it does not make `L(E,2)^rank` load-bearing.

No external paper/theorem citation is used here.

## 1. Exact finite objects

For `0 <= alpha < 1`, use the reproducer's smoothstep cutoff

```text
W_alpha(t) = 1                                           for 0 <= t <= alpha,
W_alpha(t) = 1 - u^2(3 - 2u), u=(t-alpha)/(1-alpha)       for alpha < t < 1,
W_alpha(t) = 0                                           for t >= 1.
```

For `alpha = 0`, this is the full-interval cubic taper. For `alpha` close to
`1`, only the endpoint shell is tapered. The tested grid used
`alpha in {0,0.25,0.5,0.65,0.75,0.85,0.92}`.

Let

```text
W_hat(z) = integral_0^infty W_alpha(t) t^(z-1) dt.
```

Then `W_hat(z)` has a simple pole at `z=0` with residue `1`. For the smoothstep
kernel, `W_hat(sigma+i tau) = O_alpha,sigma((1+|tau|)^-2)` on fixed vertical
strips away from `z=0`. The hard cutoff has only `W_hat(z)=1/z`, hence only
`O(1/|tau|)` decay.

For an elliptic curve `E/Q`, use the same local convention as the reproducer.
At good primes,

```text
A_p(1) = 1 - a_p/p + 1/p,
A_p(2) = 1 - a_p/p^2 + 1/p^3.
```

At bad primes,

```text
A_p(1) = 1 - a_p/p,
A_p(2) = 1 - a_p/p^2.
```

Define the reciprocal coefficients by

```text
1/L(E,s) = sum_{n>=1} mu_E(n) n^(-s)
```

in the half-plane where the Dirichlet series is absolutely convergent. Locally
this matches the script:

```text
good p: mu_E(p)=-a_p, mu_E(p^2)=p, mu_E(p^j)=0 for j>=3,
bad  p: mu_E(p^j)=(-a_p)^j.
```

The finite smoothed objects are

```text
c_E,alpha(K)  = sum_{n>=1} mu_E(n)/n * W_alpha(n/K),
P_E,alpha(K)  = product_p A_p(1)^(-W_alpha(p/K)),
L2_E,alpha(K) = product_p A_p(2)^(-W_alpha(p/K)).
```

The reproduced full proxy is

```text
X_E,alpha(K) = zeta(2) * c_E,alpha(K) * P_E,alpha(K)
               / L2_E,alpha(K)^rank(E).
```

The T1 theorem below concerns the stabilization mechanism for
`c_E,alpha(K) P_E,alpha(K)`. The `L2` factor is absolutely convergent and cannot
by itself explain within-curve endpoint stabilization.

## 2. Conditional theorem

Let `r = ord_{s=1} L(E,s)`. Assume `L(E,s)` is holomorphic near `s=1` except
for its zero of exact order `r`, so

```text
L(E,1+z) = lambda_E z^r (1 + O(z)),
lambda_E = L^(r)(E,1) / r!.
```

Fix a smoothstep `W = W_alpha`, `0 <= alpha < 1`.

### Hypotheses

`H1. Reciprocal Perron expansion.`

The smoothed Perron formula

```text
c_E,W(K) = (1/2 pi i) integral_(sigma) K^z W_hat(z) / L(E,1+z) dz
```

can be shifted left far enough to isolate the central pole at `z=0`, and the
off-central residues plus new-contour integrals satisfy

```text
c_E,W(K) = Q_E,W(log K) + R_c(K),
```

where `Q_E,W` is a polynomial of degree `r` with leading term

```text
(log K)^r / L^(r)(E,1),
```

and, for some `delta > 0`,

```text
R_c(K) = O((log K)^(r-1-delta))     if r >= 1,
R_c(K) = O((log K)^(-delta))        if r = 0.
```

Equivalently, every noncentral zero contribution

```text
Res_{z=rho-1} K^z W_hat(z) / L(E,1+z)
```

is either absolutely summable after the `W_hat` damping or cancels in aggregate
below the stated error. If a noncentral zero on `Re(s)=1` has multiplicity `m`,
its residue can contain `(log K)^(m-1) K^{i gamma}`. This hypothesis explicitly
rules out such terms at the main scale.

`H2. Smoothed Euler-product Mertens expansion.`

For the same weight `W`,

```text
log P_E,W(K) = -r log log K + B_E,W + b_E,W/log K
               + O((log K)^(-1-delta)).
```

The coefficient `-r` is essential. It is the product-side counterpart of the
central zero of order `r`. This is not supplied by the computation; it is a
missing analytic input.

`H3. L2 tail.`

The smoothed `s=2` product has a nonzero limit:

```text
L2_E,W(K) = L(E,2) * (1 + O(K^(-1/2+epsilon)))
```

for every fixed `epsilon > 0`, or any comparable power-saving tail bound. This
is the easy part relative to `H1` and `H2`; it only uses the fact that the
`s=2` Euler product is absolutely convergent under standard EC local bounds.

### Conclusion

Under `H1-H3`, if `r >= 1` then

```text
c_E,W(K) P_E,W(K)
  = exp(B_E,W) / L^(r)(E,1) * (1 + O((log K)^(-eta)))
```

for some `eta > 0`.

Consequently

```text
X_E,W(K)
  = zeta(2) * exp(B_E,W)
    / (L^(r)(E,1) * L(E,2)^r)
    * (1 + O((log K)^(-eta))).
```

For `r = 0`, the same conclusion holds only under the rank-zero version of
`H1`, which requires off-central reciprocal-zero residues to be `o(1)`. Without
that stronger rank-zero control, smoothing gives a bounded explicit-formula
expansion but not a pointwise limit.

The limiting constant is curve-dependent. The theorem explains possible
within-curve stabilization. It does not imply that the three curve constants
should match.

## 3. Proof skeleton

1. Start from Mellin inversion. Since `W` is compactly supported and
   `W_hat(z)` is defined for `Re(z)>0`, for `sigma` in the absolute convergence
   region of `1/L(E,1+z)`,

   ```text
   c_E,W(K) = (1/2 pi i) integral_(sigma)
              K^z W_hat(z) / L(E,1+z) dz.
   ```

2. Shift the contour. The pole at `z=0` comes from both the central zero of
   `L(E,s)` and the pole of `W_hat(z)`. Since

   ```text
   1/L(E,1+z) = lambda_E^(-1) z^(-r) (1 + O(z)),
   W_hat(z) = 1/z + kappa_W + O(z),
   K^z = exp(z log K),
   ```

   the central residue is a degree-`r` polynomial in `log K` with leading
   coefficient `1/L^(r)(E,1)`.

3. Bound the noncentral residue aggregate. For the hard cutoff, the residue
   weights decay like `1/|gamma|`. For the smoothstep, they decay like
   `1/|gamma|^2`, before any additional decay from the analytic factors. This
   is the formal endpoint-drift suppression: the high-zero and horizontal-edge
   terms are much less sensitive to truncation height and to the exact endpoint
   `K`.

4. Prove or assume the product-side explicit formula. The logarithm of the
   smoothed Euler product is

   ```text
   log P_E,W(K) = - sum_p W(p/K) log A_p(1).
   ```

   A product-side explicit formula must show that its central term is
   `-r log log K`, with a curve and kernel constant `B_E,W`, and with remaining
   zero/prime-shell terms below `1/log K` scale. This is the direct analogue of
   a smoothed Mertens theorem for the EC Euler product at the central point.

5. Multiply the two expansions. The central powers cancel:

   ```text
   c_E,W(K) ~ (log K)^r / L^(r)(E,1),
   P_E,W(K) ~ exp(B_E,W) / (log K)^r.
   ```

   This gives the fixed-curve constant. The `L2` factor contributes only its
   absolutely convergent limit.

## 4. Why smoothing can help

The smoothstep is not magic. It changes the analytic kernel.

- In the coefficient sum, the hard cutoff has Mellin kernel `1/z`. A `C^1`
  endpoint taper changes this to a kernel with `O(|tau|^-2)` vertical decay.
  This can turn endpoint-sensitive residue sums into stable sums if reciprocal
  zero residues are not too large.

- In the Euler product, hard cutoff jumps whenever a prime enters the product.
  The smoothed product replaces a prime-entry jump by a continuous weight over
  the shell `alpha K < p < K`. This reduces prime-shell variance on sparse
  `K` grids.

- Applying the same scale `K` and kernel to `c` and `P` makes their central
  singular terms compatible: `(log K)^r` from `1/L` can cancel `(log K)^(-r)`
  from the product.

This is enough to explain why smoothing can lower within-curve CV. It is not
enough to prove an asymptotic constant without `H1` and `H2`.

## 5. What the reproduced ablations imply

The saved reproduction reports:

```text
all, alpha=0.75:     ratio 1.3473754929960748, max CV 0.063297427334436704
cP_only, alpha=0.75: ratio 1.3474536199105895, max CV 0.063319173311522384
```

and `P_only`/`PL2_only` also pass old gates for several alphas. This strongly
suggests that the current pass is mostly an endpoint-smoothing/product-shell
effect, not evidence that the `L(E,2)^rank` denominator is the right asymptotic
normalization.

This matches the theorem: `L2_E,W(K)` is an absolutely convergent product, so
it is close to a curve-dependent constant across the tested grid. It can change
cross-curve scale, but it should not be expected to cure within-curve endpoint
drift.

## 6. Obstacles

1. Off-central zeros at the same real part. For elliptic-curve central values,
   noncentral zeros are expected on the same critical line `Re(s)=1`. Their
   reciprocal Perron residues have size `K^{i gamma}`, not decaying powers of
   `K`.

2. Multiplicity. An offcentral zero of multiplicity `m` contributes a polynomial
   of degree `m-1` in `log K`. If `m-1 >= r`, it can match or dominate the
   central rank term.

3. Reciprocal derivative control. Even with simple zeros, the coefficient sum
   needs summability of terms involving reciprocal zero derivatives. Smooth
   `W_hat` helps, but does not by itself bound `1/L'(rho)`.

4. Product-side Mertens theorem. The expansion for `log P_E,W(K)` is a serious
   analytic input. It cannot be read off from the finite script. Prime-square
   and higher local terms are not harmless bookkeeping at `s=1`; they are part
   of the constant and possible logarithmic drift.

5. Rank zero. If `r=0`, the central term in `c_E,W(K)` is only constant scale.
   Any bounded offcentral oscillatory residue is also constant scale. A rank-zero
   pointwise limit therefore needs stronger cancellation than the positive-rank
   stabilization.

6. Finite window. The current `K` grid stops at `1000000` and has only seven
   points. A smooth shell can lower apparent CV on such a grid while leaving a
   nonconvergent almost-periodic zero sum visible at larger `K`.

## 7. Finite-window versus asymptotic readings

Asymptotic reading, conditional:

```text
If H1 and H2 hold, smoothing is a real theorem-level mechanism for fixed-curve
stabilization of c_E,W(K) P_E,W(K).
```

Finite-window reading, currently favored:

```text
The pass may be endpoint damping. The ablations show that smoothing P, and
nearly smoothing cP, reproduces the old gate. The tested L2 denominator is not
load-bearing.
```

The data are compatible with both readings. The theorem reduction says exactly
which analytic facts separate them.

## 8. Do not promote unless

- `H1` is proved or citation-closed for the same smoothed kernel, including
  offcentral residues, possible multiple zeros, contour tails, and reciprocal
  derivative growth.

- `H2` is proved or citation-closed for the same smoothed Euler product at
  `s=1`, with the exact coefficient `-rank(E)` in front of `log log K`.

- Rank-zero curves are handled separately. Either prove offcentral residues are
  `o(1)` for the smoothed reciprocal sum, use a declared logarithmic average,
  or state that rank-zero stabilization is only finite-window evidence.

- The limiting constant is identified. A fixed-curve theorem is not a
  cross-curve universality theorem.

- Holdout curves across rank and conductor pass with a predeclared alpha or a
  predeclared kernel family.

- Larger and denser `K` grids show that the low-zero and endpoint-shell terms
  are not reappearing.

- Ablations become load-bearing. If `P_only` or `cP_only` keeps matching `all`,
  the claim should be "smoothing suppresses endpoint drift", not "`L(E,2)^rank`
  explains the normalization."

- Any external theorem/paper used to close `H1` or `H2` follows the repository
  source protocol: `curl + pdftotext`, verbatim quote, and page/equation number.

## 9. Clean theorem target for the next sprint

Prove the following, for one fixed curve first:

```text
For a fixed elliptic curve E/Q of rank r>=1 and a fixed smoothstep W_alpha,
there exist constants B_E,W and eta>0 such that

c_E,W(K) = (log K)^r/L^(r)(E,1) * (1 + O(1/log K))
P_E,W(K) = exp(B_E,W)/(log K)^r * (1 + O(1/log K))

after all offcentral zero residues are included and shown to be lower order.
```

Then

```text
c_E,W(K) P_E,W(K) = exp(B_E,W)/L^(r)(E,1) + O(1/log K).
```

That theorem would justify fixed-curve asymptotic stabilization. It would still
not justify the present three-curve universal-looking ratio without a separate
constant identity or a successful holdout/ablation program.
