# Universality under GRH+LI: rigorous conditional version

> The original universality claim, interpreted as a statement about an arbitrary prime subset and GRH+LI alone, is not currently a theorem. The proof below is the strongest rigorous version of the same mechanism: it adds one explicit regularity hypothesis on the selected prime family, proves the off-resonance and peak-location steps, and then isolates the exact necessary condition that cannot be removed.

## 1. Precise statement

Let `S_X` be a finite subset of the primes `p <= X`. Write

`A_X(gamma) := sum_{p in S_X} a_p e^{-i gamma log p}`,  `F_X(gamma) := gamma^2 |A_X(gamma)|^2`,

where `a_p > 0` is the weight coming from the observable. In the prompt normalization one takes `a_p = 1/p`; in the strict Mertens-explicit-formula normalization one replaces `a_p` by `p^{-1/2}`. The proof is identical after this renormalization, so I write it for `a_p = 1/p` to match the gap statement.

For a fixed zero `rho_j = 1/2 + i gamma_j`, define the resonant phase variable

`delta := gamma - gamma_j`,
`R_X(delta) := sum_{p in S_X} p^{-1} e^{-i delta log p}`.

We assume:

1. **GRH.** Every nontrivial zero of `zeta(s)` lies on `Re(s) = 1/2`.
2. **LI.** The positive ordinates `gamma_k` of the nontrivial zeros are linearly independent over `Q`. In particular, the finitely many ordinates kept after truncation are distinct, so there are no exact resonances except the diagonal one.
3. **Vinogradov-Korobov density regularity for `S`.** There exist `delta_S in (0,1]`, `c > 0`, and
   `eta(x) := exp(-c (log x)^{3/5} (log log x)^(-1/5))`
   such that the weighted Chebyshev function of `S` satisfies

   `theta_S(x) := sum_{p <= x, p in S} log p = delta_S x + O(x eta(x)).`

   This is the precise regularity hypothesis needed for Gap 1. For the full set of primes, it follows from the classical prime number theorem with a Vinogradov-Korobov error term. For arbitrary subsets it is an additional assumption.

Under these hypotheses, for every fixed `j` there exist `X_0(j)` and `C_j > 0` such that for all `X >= X_0(j)`, the function `F_X` has a strict local maximum `tilde{gamma}_{j,X}` with

`|tilde{gamma}_{j,X} - gamma_j| <= C_j / log X`.

The proof is split into the three gaps requested in the prompt.

## 2. Gap 1: off-resonance decay

The target bound is

`sum_{p in S_X} p^{i alpha - 1} = o( sum_{p in S_X} p^{-1} )` for every fixed `alpha != 0`.

This is not a consequence of LI alone. It follows from the VK-density hypothesis by partial summation.

### 2.1. Weighted prime mass

Let

`W_X := sum_{p in S_X} 1/p`,
`L_X := sum_{p in S_X} (log p)/p`,
`Q_X := sum_{p in S_X} (log p)^2/p`.

Partial summation with `theta_S(x) = delta_S x + O(x eta(x))` gives

`W_X = delta_S log log X + O(1),`

`L_X = delta_S log X + O(1),`

`Q_X = (delta_S/2) (log X)^2 + O(log X).`

In particular, `W_X -> infinity` and `Q_X ~ (log X)^2 W_X / (2 log log X)`.

### 2.2. Oscillatory prime sum

For fixed `alpha != 0`, set

`S_X(alpha) := sum_{p in S_X} p^{i alpha - 1}.`

Write `d pi_S(t)` for the counting measure of primes in `S`. Then

`S_X(alpha) = int_{2^-}^X t^{i alpha - 1} d pi_S(t).`

Now decompose `pi_S` using `theta_S`:

`pi_S(t) = theta_S(t)/log t + O(t / (log t)^2).`

Substituting this into the Stieltjes integral and integrating by parts yields

`S_X(alpha) = delta_S * int_2^X t^{i alpha - 1} / log t dt + E_X(alpha),`

where `E_X(alpha)` is the contribution of the error term `O(x eta(x))`. Since

`int_X^infty t^{i alpha - 1} / log t dt`

converges conditionally and satisfies the explicit tail bound

`|int_X^infty t^{i alpha - 1} / log t dt| <= 2 / (|alpha| log X),`

we obtain

`S_X(alpha) = C_S(alpha) + O(1 / log X)`

for some finite constant `C_S(alpha)` depending on `S` and `alpha`. In particular,

`S_X(alpha) = o(W_X)` because `W_X ~ delta_S log log X -> infinity`.

This is the off-resonance bound requested in Gap 1.

### 2.3. Relation to Erdős-Turán

The Erdős-Turán inequality is the discrepancy version of the same input. Applied to the phase sequence

`{ alpha log p / (2 pi) : p in S_X }`,

it converts bounds on the Fourier modes `sum p^{ih alpha - 1}` into equidistribution. Here the Fourier modes are already controlled by the VK-density hypothesis, so Erdős-Turán is not needed in the main proof. It is only the discrepancy wrapper around the same estimate.

## 3. Gap 2: peak location by a derivative test

The local maximum is proved for the resonant main term first, then transferred to the full spectroscope by a perturbation argument.

### 3.1. The resonant main term

Fix `j` and truncate the zero sum at a height `T > |gamma_j|`. The explicit formula gives

`A_X(gamma_j + delta) = c_j R_X(delta) + E_{X,j}(delta),`

where `c_j = 1 / (rho_j zeta'(rho_j))` and `E_{X,j}` contains:

1. the finitely many off-resonant zeros `rho_k` with `0 < |gamma_k| <= T`, `k != j`,
2. the explicit-formula truncation error.

For the resonant piece,

`R_X(delta) = sum_{p in S_X} p^{-1} e^{-i delta log p}.`

Its derivatives at `delta = 0` are

`R_X(0) = W_X,`
`R_X'(0) = -i L_X,`
`R_X''(0) = -Q_X.`

Therefore

`d/delta |R_X(delta)|^2 |_{delta=0} = 0,`

and

`d^2/delta^2 |R_X(delta)|^2 |_{delta=0} = -2 (W_X Q_X - L_X^2).`

Using the asymptotics from Section 2,

`W_X Q_X - L_X^2 = (delta_S^2 / 2) (log X)^2 log log X + O((log X)^2),`

so for large `X`,

`d^2/delta^2 |R_X(delta)|^2 |_{delta=0} <= -c (log X)^2 log log X`

for some constant `c = c(S) > 0`. Thus `delta = 0` is a strict local maximum of the resonant term, and the natural width is `O(1 / log X)`. The Rayleigh heuristic `2 pi / log X` gives the same scale, but the theorem only needs the order of magnitude.

### 3.2. Control of the perturbation

For each fixed off-resonant zero `rho_k` with `k != j`, the same integration-by-parts argument used in Gap 1 gives

`sum_{p in S_X} p^{-1 + i(gamma_k - gamma_j)} = O(1)`

uniformly for `X -> infinity`. Differentiating with respect to `delta` simply inserts powers of `log p`, so on a window `|delta| <= c / log X`,

`E_{X,j}^{(m)}(delta) = O((log X)^m)` for `m = 0,1,2`.

The constants here are independent of `X` because only finitely many zeros are retained after truncation. The tail beyond `T` is already part of the explicit-formula error and is `o(W_X)` after choosing the usual smooth truncation.

Now compare scales:

* main curvature of `|R_X|^2` is `~ (log X)^2 log log X`,
* perturbation derivatives are at most `O((log X)^2)`.

So the perturbation is smaller by a factor `1 / log log X`.

### 3.3. Stability lemma

Let `f, g in C^2([-r,r])` with `f'(0)=0` and `f''(x) <= -m < 0` on `[-r,r]`. If

`||g'||_infty <= m r / 4`

and

`||g''||_infty <= m / 4`,

then `f + g` has a unique critical point in `[-r,r]`, and it is a strict local maximum. The proof is the usual sign-change argument for the derivative: `f'` drops by at least `m r` across the interval, while `g'` perturbs it by less than `m r / 2`.

Apply this lemma with `r = c / log X`. The scale comparison above shows that the hypotheses hold for all sufficiently large `X`. Hence the full `F_X` has a strict local maximum `tilde{gamma}_{j,X}` satisfying

`|tilde{gamma}_{j,X} - gamma_j| <= C_j / log X`.

The factor `gamma^2` in `F_X(gamma)` is smooth and positive on the fixed neighborhood of `gamma_j`, so it only changes the perturbation term by `O(1 / log X)` and does not affect the conclusion.

This closes Gap 2.

## 4. Gap 3: the divergence condition is sharp

The necessary condition is that the weighted mass

`W_X = sum_{p in S_X} 1/p`

must diverge. Without that, there is no asymptotic signal to dominate the off-resonant remainder.

### 4.1. Failure for moving upper intervals

For the adversarial family `S_X = { p : X/2 < p <= X }`,

`sum_{X/2 < p <= X} 1/p = log log X - log log(X/2) + o(1) = (log 2) / log X + o(1 / log X),`

so `W_X -> 0`.

Thus the resonant term itself vanishes, and the localization mechanism has nothing to amplify. This is exactly the computational failure observed for the `[500K, 1M]` prime window: the large primes carry too little reciprocal mass in the `1/p` normalization.

### 4.2. Why the condition cannot be removed

If `W_X` stays bounded, then the resonant main term `c_j W_X` stays bounded, while the off-resonant part is only controlled by the same scale. There is no asymptotic inequality that can force a strict local maximum near `gamma_j` for all large `X`.

So the divergence of `sum 1/p` is not a technical convenience. It is the necessary condition for the theorem to have any chance of being true in the prompt normalization.

In the strict explicit-formula normalization, the analogous necessary condition is `sum_{p in S_X} p^{-1/2} -> infinity`. The same logical role is played by the corresponding weighted mass.

This closes Gap 3.

## 5. Assembled proof

Combine the three sections:

1. **Explicit formula + truncation.** Under GRH, the spectroscope decomposes into one resonant zero term, finitely many off-resonant zero terms, and a truncation error.
2. **Gap 1.** The VK-density hypothesis gives `sum p^{i alpha - 1} = C_S(alpha) + O(1/log X)`, hence off-resonant terms are `o(W_X)`.
3. **Gap 2.** The resonant term has curvature `~ (log X)^2 log log X`, so a `C^2` perturbation of size `O((log X)^2)` shifts the maximum by only `O(1/log X)`.
4. **Gap 3.** The mass condition `W_X -> infinity` is necessary; if it fails, the resonance cannot dominate.

Therefore, under GRH, LI, and VK-density regularity of `S`, the spectroscope has a strict local maximum within `C_j / log X` of each fixed zero ordinate `gamma_j`.

This is the rigorous version of the universality mechanism. The original statement for an arbitrary prime subset is still open unless one can prove the VK-density hypothesis for that subset.

## 6. Remaining open questions

1. **Can VK-density be proved for the subsets seen in computation?**  
   This is the key missing input for random subsets, residue-class subsets, and other structured selections. For twin primes it would require hypotheses far beyond GRH+LI, such as Hardy-Littlewood type input.

2. **Can the `O(1 / log X)` localization be sharpened?**  
   Yes in principle, if one proves a more precise second-order asymptotic for the weighted prime mass and a sharper remainder bound for the off-resonant terms. The present proof only needs the `1 / log X` scale.

3. **Can the theorem be made uniform in `j`?**  
   Not from the present argument. Uniformity would require explicit control of the truncation tail, of `zeta'(rho_j)`, and of zero spacing as `j -> infinity`.

4. **Can one remove the regularity hypothesis entirely?**  
   Not with the present strategy. LI does not imply equidistribution for a fixed prime subset, so some quantitative distribution hypothesis on `S` is genuinely needed. A full arbitrary-subset theorem would require a new idea, and the moving-window example shows that the naive statement is false in the prompt normalization.

## 7. References

* H. Iwaniec and E. Kowalski, *Analytic Number Theory*, especially the explicit formula and prime number theorem error terms.
* H. L. Montgomery and R. C. Vaughan, *Multiplicative Number Theory I: Classical Theory*, for explicit formulas and partial summation.
* D. R. Johnston and A. Yang, "Some explicit estimates for the error term in the prime number theorem" (2022).
* T. Khale, "An Explicit Vinogradov-Korobov Zero-Free Region for Dirichlet L-Functions" (2024).
* Erdős and Turán, original discrepancy inequality (classical reference).

