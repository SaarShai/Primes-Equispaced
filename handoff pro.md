# Handoff Pro: H1 Displacement / Rooted Palm Wall

Created: 2026-05-12  
Repo root: `/Users/za/Documents/Farey NOW/primes-equispaced`  
Status: wall narrowed, not broken. No theorem is promoted.

This file is intended as a self-contained challenge packet for GPT-5.5 Pro
Extended or another serious research agent. It includes the exact H1 wall,
formula stack, reductions, source gaps, failed routes, conjectural model,
repo references, and challenge definitions.

If in doubt, assume every theorem-like statement below is conditional unless
explicitly marked `proved/reduced in repo`. The source protocol remains
mandatory before promoting anything: retrieve primary source/PDF, cite page or
equation, audit normalization, and run an adversarial pass.

## Executive Challenge

Break the H1 bad-cluster wall.

The highest-priority challenge is:

```text
H1-RootedPalmBox_q3(E,A;W):
  prove PrimeScaleRootedPalmBox_beta(E,A;W)
  for some beta > 3/2,
  for one fixed elliptic curve/newform E,
  for all rooted cluster sizes m,
  with summable constants,
  at normalized scale 1/log T.
```

Paired with the shifted negative moment:

```text
Degree2WeakShiftedNeg_3(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-3)
    <<_(E,eps) T^(7/2+eps),
```

this gives:

```text
R_B(T,c) << T^(11/6+eps+o(1)) = o(T^2).
```

Together with the already conditionally harmless separated branch:

```text
R_F(T,c) << T^(3/2+eps),
```

this closes the rank-one **simple-zero** H1 reciprocal derivative budget:

```text
R_E,1^simp(T)=o(T^2).
```

Full H1 still requires:

```text
H1-MultipleZeroDisposition(E,W,r)
```

and finite-box contour hypotheses. Do not claim full H1 from the simple-zero
wall alone.

## Best Current Verdict

The q=3 displacement route is the best target.

The old hard blocker was the q=2 square Palm condition:

```text
RootedInvProdCorr_2(E,A):
  sum_(rho in S_E(T)) W_A(rho)^2 << T log T.
```

The new weaker wall is:

```text
RootedInvProdCorr_p(E,A),        p = q/(q-1).
```

For:

```text
q=3,        p=3/2,
```

the required singular rooted-cluster integrability is substantially weaker
than q=2, while the final exponent still beats `T^2`:

```text
R_B(T,c) << T^(2 - 1/(2q) + eps + o(1)).
```

At q=3:

```text
2 - 1/(2q) = 2 - 1/6 = 11/6.
```

At q=4:

```text
p=4/3,        R_B(T,c) << T^(15/8+eps+o(1)).
```

q=3 is the main route. q=4 is a fallback if the Palm exponent is easier than
the shifted moment.

Confidence:

```text
0.86: this is the correct current boundary.
0.12: current literature already contains the needed fixed-EC rooted box law
      in all-cluster shrinking-box form.
```

## Notation

Use normalized critical-line notation:

```text
L_E^*(s) = L(E,s+1/2).
```

Zeros of `L_E^*` are written:

```text
rho = 1/2 + i gamma.
```

Dyadic zero shell:

```text
S_E(T) = {simple zeros rho=1/2+i gamma : T < |gamma| <= 2T}.
```

Shift:

```text
alpha = 1/log T.
```

Shifted reciprocal value:

```text
X(rho) = |L_E^*(rho+alpha)|^(-1).
```

Normalized close-root distance:

```text
u(rho0,rho) = log T * |rho-rho0|.
```

Cluster around a root:

```text
C_A(rho0) = {rho_j : 0 < |rho_j-rho0| <= A/log T} union {rho0}.
```

Cluster weight:

```text
W_A(rho0)
 = prod_(rho_j in C_A(rho0)\{rho0})
     |alpha+rho0-rho_j| / |rho0-rho_j|.
```

Under RH/local critical-line normalization:

```text
|alpha+rho0-rho_j| / |rho0-rho_j|
 = sqrt(1+u_j^2)/u_j
 <= C_A/u_j,       0<u_j<=A.
```

So `W_A` is an inverse-product cluster weight.

## H1 Split

For fixed `c>0`, split simple zeros:

```text
S_E(T) = F_E(T,c) union B_E(T,c),
```

where `F_E(T,c)` is the separated set:

```text
F_E(T,c) = {gamma in (T,2T]:
  L(E,1+i gamma)=0 is simple and
  |gamma-gamma'| >= c/log T for every other zero ordinate gamma'}.
```

The bad set `B_E(T,c)` is the close-cluster complement.

Define:

```text
R_E,1^simp(T)
 = sum_(rho simple, T<|gamma|<=2T) |(L_E^*)'(rho)|^(-1)
 = R_F(T,c)+R_B(T,c).
```

Separated branch:

```text
R_F(T,c) <<_(E,c,eps) T^(3/2+eps).
```

Bad branch target:

```text
R_B(T,c) = o(T^2).
```

The wall is entirely in the bad branch.

## Local Displacement / Cluster-Shift Identity

This is the key local theorem. It bypasses a zero-centered minimum-modulus
problem.

Local factorization near a simple bad zero `rho0`:

```text
L_E^*(s) =
  (s-rho0)
  prod_(rho_j in C_A(rho0)\{rho0}) (s-rho_j)
  H_A(s),
```

where `H_A` absorbs noncluster zeros, gamma/conductor factors, and the
holomorphic nonzero quotient.

At `rho0`:

```text
(L_E^*)'(rho0)
 = prod_(rho_j in C_A(rho0)\{rho0}) (rho0-rho_j) * H_A(rho0).
```

At `rho0+alpha`:

```text
L_E^*(rho0+alpha)
 = alpha
   prod_(rho_j in C_A(rho0)\{rho0}) (alpha+rho0-rho_j)
   H_A(rho0+alpha).
```

Divide:

```text
|(L_E^*)'(rho0)|^(-1)
 = alpha
   prod_(rho_j in C_A(rho0)\{rho0})
     |alpha+rho0-rho_j| / |rho0-rho_j|
   * |H_A(rho0+alpha)|/|H_A(rho0)|
   * |L_E^*(rho0+alpha)|^(-1).
```

Noncluster ratio under fixed-newform RH/local zero-count input:

```text
|H_A(rho0+alpha)|/|H_A(rho0)|
  <= exp(O_(E,A)(log T/loglog T))
  = T^o(1).
```

Therefore:

```text
ClusterShiftDerivativeComparison(E,A):
|(L_E^*)'(rho0)|^(-1)
 <= T^o(1) alpha W_A(rho0)
    |L_E^*(rho0+alpha)|^(-1).
```

This is proved/reduced in repo as a conditional local theorem.

Repo:

- [CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md)

## Holder Reduction

For the bad branch:

```text
R_B(T,c)
 <= T^o(1) alpha
    sum_(rho in B_E(T,c)) W_A(rho) X(rho).
```

For conjugate exponents:

```text
q>1,        p=q/(q-1),
```

Holder gives:

```text
sum_B W_A(rho) X(rho)
 <= (sum_B X(rho)^q)^(1/q)
    (sum_B W_A(rho)^p)^(1/p).
```

It suffices to bound over all simple zeros:

```text
sum_B X(rho)^q <= sum_(rho in S_E(T)) X(rho)^q.
```

Assume:

```text
Degree2WeakShiftedNeg_q(E):
  sum_(rho in S_E(T)) X(rho)^q << T^mu_q,
```

and:

```text
RootedInvProdCorr_p(E,A):
  sum_(rho in S_E(T)) W_A(rho)^p << T^nu_p (log T)^C.
```

Then:

```text
R_B(T,c)
 << T^o(1) (logT)^(-1)
    T^(mu_q/q) T^(nu_p/p) (log T)^(C/p).
```

Clean exponent criterion:

```text
mu_q/q + nu_p/p < 2.
```

Natural targets:

```text
mu_q = q + 1/2,
nu_p = 1.
```

Since:

```text
1/p = 1 - 1/q,
```

we get:

```text
mu_q/q + nu_p/p
 = (q+1/2)/q + 1/p
 = 1 + 1/(2q) + 1 - 1/q
 = 2 - 1/(2q)
 < 2.
```

Thus:

```text
R_B(T,c) << T^(2 - 1/(2q) + eps + o(1)).
```

Repo:

- [SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md)
- [H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md](handoff-2026-05-11-implementation-wave/H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md)

## Shifted Negative Moment Side

Target for q=3:

```text
Degree2WeakShiftedNeg_3(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-3)
    << T^(7/2+eps).
```

General target:

```text
Degree2WeakShiftedNeg_q(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-q)
    << T^(q+1/2+eps).
```

q=2 has a conditional pass:

```text
Degree2WeakShiftedNeg_2(E):
  sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-2)
    << T^(5/2+eps).
```

Source mechanism:

BFMT Lemma 2.4 gives a shifted-value reciprocal upper majorant over all zero
ordinates. BFMT Propositions 2.5, 2.6, and 2.7 bound the pieces. The EC/GL2
transcription uses the zero-sampling homogeneous coefficient audit and the
fixed degree-2 conductor:

```text
log C_E(t) = 2 log T + O_E(1).
```

For q=2, i.e. `2k=q=2`, `k=1`, the degree-2 second-branch power becomes:

```text
1 + 2 * (4-1)/(4-1+1)
 = 1 + 3/2
 = 5/2.
```

For q=3, expected/desired:

```text
q=3, k=3/2 -> T^(7/2+eps).
```

For q=4:

```text
q=4, k=2 -> T^(9/2+eps).
```

Important: q=3/q=4 are not source-promoted. They require a separate
BFMT/DPMV coefficient audit. Current agent verdict: no algebraic failure found
for q=3/q=4, but source closure is missing.

Repo:

- [DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md)
- [WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md)
- [ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md](handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md)
- [BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md](handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md)

External:

- Bui-Florea-Milinovich-Turnage-Butterbaugh negative moment work:
  [arXiv:2310.03949](https://arxiv.org/abs/2310.03949)

## Rooted Inverse-Product / Palm Side

For `m>=1`, define:

```text
J_m^(p)(T;A)
 =
 sum_(rho0 in S_E(T))
 sum_(rho1,...,rhom distinct; 0<u_j<=A)
   prod_(j=1)^m u_j^(-p),

u_j = log T * |rho_j-rho0|.
```

Sufficient cluster condition:

```text
RootedInvProdCorr_p(E,A):
  sum_(m>=1) C_A^m/m! * J_m^(p)(T;A)
    <<_(E,A,p) T log T.
```

Equivalent/useful box law:

```text
PrimeScaleRootedPalmBox_beta(E,A;W):
nu_m,T^W(prod_j (0,r_j])
  <= C_m T log T prod_j r_j^beta,

sum_m K_A^m C_m/m! < infinity,
beta > p.
```

For q=3:

```text
p=3/2,
need beta > 3/2.
```

For q=2:

```text
p=2,
need beta > 2.
```

The q=2 square expansion:

```text
W_A(rho0)^2
 <= prod_(rho in C_A'(rho0)) (1 + C_A^2 u(rho0,rho)^(-2)).
```

Expanding:

```text
sum_(rho0 in S_E(T)) W_A(rho0)^2
 <= #S_E(T)
    + sum_(m>=1) C_A^(2m)/m! * J_m^(2)(T;A).
```

Thus:

```text
SquareRootedInvProdExp(E,A):
  sum_(m>=1) C_A^(2m)/m! * J_m^(2)(T;A)
    << T log T
=> RootedInvProdCorr_2(E,A).
```

Repo:

- [ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md)
- [ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md)
- [UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md)

## Pair Layer

Rooted close-pair counting:

```text
Q_1(T;u)
 =
 #{(rho0,rho1): rho0 in S_E(T), rho1 != rho0,
   log T |rho1-rho0| <= u}.
```

Then:

```text
J_1^(p)(T;A) = int_(0,A] u^(-p) dQ_1(T;u).
```

If:

```text
Q_1(T;u) << T log T * u^beta,       0<u<=A,
```

then Stieltjes integration by parts gives:

```text
J_1^(p)(T;A) << T log T
```

provided:

```text
beta > p.
```

For q=2/p=2, need `beta>2`.  
For q=3/p=3/2, need `beta>3/2`.

The GUE/sine-kernel rooted Palm model gives cubic pair mass:

```text
rho_1^Palm(u)
 = 1 - sinc(pi u)^2
 = (pi^2/3)u^2 + O(u^4).
```

So:

```text
int_0^r rho_1^Palm(u) du
 = (pi^2/9)r^3 + O(r^5).
```

This is model exponent:

```text
beta = 3.
```

Pair layer alone is not enough. It proves only `m=1`. The real H1 wall needs
all `m` and summable constants.

## Sine-Kernel Palm Model Crack

In the determinantal sine-kernel model:

```text
S(x) = sin(pi x)/(pi x).
```

The reduced Palm kernel at a root is:

```text
K^0(x,y) = S(x-y) - S(x)S(y).
```

Diagonal:

```text
K^0(u,u) = 1 - S(u)^2 ~ (pi^2/3)u^2.
```

Hadamard bounds imply coordinatewise cubic box decay. For higher `m`, the
local density near the root has the shape:

```text
C_m prod_j u_j^2 prod_(i<j)(u_i-u_j)^2.
```

So the random-matrix/Palm model easily gives:

```text
beta=3,
```

which beats both q=2 and q=3 thresholds.

The missing analytic theorem is the transfer from this model behavior to one
fixed EC/GL2 zero process with uniform shrinking-box control and summable
rooted cluster constants.

## Prime-Scale Displacement Lens

Original lens: prime-step / Farey-delta transitions helped reveal that local
prime-block transitions can expose hidden structure. For H1, the corresponding
local transition object is a prime-scale displacement metric between zeros:

```text
D_{rho,lambda}^{E,W}(T)
 =
 sum_(p good) W(log p/log T) lambda_E(p)^2/p
   |e^(-i gamma_rho log p)-e^(-i gamma_lambda log p)|^2.
```

Here:

```text
lambda_E(p)=a_p(E)/sqrt(p).
```

Important normalization warning:

```text
lambda_E(p)^2/p = a_p(E)^2/p^2.
```

Using raw `a_p(E)^2/p` is fatal unless `a_p` is already normalized.

Milinovich-Ng prime sum:

```text
sum_(p<=x) |lambda_f(p)|^2 (log p)/p = log x + O(1),
sum_(p<=x) |lambda_f(p)|^2 /p = loglog x + O(1).
```

For:

```text
u = (gamma_rho-gamma_lambda) log T,
```

and fixed `|u|<=A`, the displacement has the model:

```text
D_{rho,lambda}^{E,W}(T)
 = 2 int W(y)(1-cos(uy)) dy/y + o(1).
```

For nonnegative `W` supported away from 0, this is comparable to:

```text
u^2
```

for small `u`.

This identifies the right local coordinate but does not itself prove the
rooted inverse-product/Palm law. The gap is the same: all-cluster singular
integrability.

External:

- Milinovich-Ng, *Lower bounds for moments of derivatives of characteristic
  polynomials and L-functions*, fixed newform prime sum adjacency:
  [arXiv:1306.0854](https://arxiv.org/abs/1306.0854)

## Why Restricted n-Level Density Fails

This route was explicitly stress-tested and is `NO_GO` from current
Rudnick-Sarnak/Hejhal support.

Goal: prove rooted box law using positive bandlimited Selberg majorants.

For a rooted box with mates:

```text
0 < u_j <= r_j,
```

choose majorants:

```text
M_j >= 1_(0,r_j].
```

Selberg/Beurling scale:

```text
int M_j = r_j + O(1/Delta_j).
```

To see shrinking mass:

```text
Delta_j ~ 1/r_j.
```

But Rudnick-Sarnak support for fixed degree-2 EC/newform is bounded. In full
n-level variables:

```text
sum_i |xi_i| < 1.
```

If the test depends on differences `x_j-x_0` with Fourier supports
`|eta_j|<=Delta_j`, then:

```text
sum_i |xi_i| = |sum eta_j| + sum |eta_j|
             <= 2 sum Delta_j.
```

Legal EC support forces:

```text
sum Delta_j < 1/2,
```

independent of `r_j`. As `r_j -> 0`, the Selberg error dominates.

Conclusion:

```text
Delta ~ 1/r  => weighted mass ~ r^3      (illegal under RS support)
Delta <= const => weighted mass ~ const  (legal, too weak)
```

Minorants do not rescue the route:

```text
int minorant = r - O(1/Delta),
```

which is useless when `r << 1/Delta`.

External:

- Rudnick-Sarnak, *Zeros of principal L-functions and random matrix theory*,
  Duke Math. J. 81 (1996). PDF:
  [rudnick-sarnak.pdf](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)
- Hejhal, *On the triple correlation of zeros of the zeta function*, IMRN
  1994. [Oxford record](https://academic.oup.com/imrn/article-abstract/1994/7/293/906602)
- Vaaler, *Some extremal functions in Fourier analysis*, Bull. AMS 12 (1985).
  [AMS record](https://www.ams.org/journals/bull/1985-12-02/S0273-0979-1985-15349-2/)

## Why Small-Gap Literature Is Not Enough

Checked adjacent sources support the local model but do not close the needed
uniform upper law.

Needed pair law:

```text
Q_1(T;u) << T log T * u^beta, beta>p, 0<u<=A.
```

Needed higher law:

```text
sum_m C_A^m/m! J_m^(p)(T;A) << T log T.
```

Existing small-gap results often prove existence, proportion, or liminf gaps.
Those are the wrong direction: H1 needs that very small rooted gaps are not too
numerous and do not carry singular inverse-product mass.

Specific checked source packets:

- Chirre-Goncalves pair-correlation estimates: adjacent, not singular rooted
  moment closure.
- Barrett-McDonald-Miller-Ryan-Turnage-Butterbaugh-Winsor GL2 gaps:
  large/small gap existence, not uniform near-zero upper law.
- Inoue 2026 zeta small-gap improvement: existence/liminf, zeta, not fixed EC
  rooted upper law.
- Hall extreme-value evidence: heuristic cubic behavior, not rooted pair-count
  theorem.

Repo:

- [UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md)

External source identifiers checked:

- [arXiv:1810.08843](https://arxiv.org/abs/1810.08843)
- [arXiv:1410.7765](https://arxiv.org/abs/1410.7765)
- [arXiv:2604.05733](https://arxiv.org/abs/2604.05733)
- Hall-related archive pointer in repo packet:
  [White Rose record](https://eprints.whiterose.ac.uk/id/eprint/7669/)

## Why Finite Cluster Truncation Fails From Known Inputs

Finite-M substitute:

```text
n_A(rho) := #{rho' != rho : 0 < logT |rho'-rho| <= A} <= M
```

uniformly for every shell/root, plus:

```text
J_m^(3/2)(T;A) <<_(E,A,m) T log T,      1 <= m <= M.
```

This would suffice.

But without a hard cap, the tail:

```text
sum_(m>M) C_A^m/m! * J_m^(3/2)(T;A)
```

is exactly the missing Palm summability. Known multiplicity results concern
exact multiplicity or proportions, not near-root clusters at scale `1/logT`.
Local zero counts and density-one simplicity are weight-blind; a zero-density
exceptional set can dominate inverse-product weights.

Verdict:

```text
NO-GO for finite-M truncation from known inputs.
```

## Why Direct Reciprocal Tail Bypass Is Harder

Palm-free route:

```text
N_E(T;V)
 = #{T<|gamma|<=2T simple : |L'(E,rho)|^(-1)>V}.
```

Then:

```text
R_E,1(T) = int_0^infty N_E(T;V) dV.
```

Zero count gives:

```text
int_0^1 N_E(T;V)dV = O(T log T)=o(T^2).
```

Needed tail:

```text
int_1^infty N_E(T;V)dV = o(T^2).
```

Sufficient negative reciprocal derivative moment:

```text
NegMoment_p(E):
sum_(T<|gamma|<=2T) |L'(E,rho)|^(-p)
  = o(T^(p+1)/(log T)^(p-1))
```

for some `p>1`.

For p=2:

```text
sum |L'(E,rho)|^(-2) = o(T^3/log T).
```

Stronger WMC-style sufficient condition:

```text
sum_(rho simple) 1/(|rho|^2 |L'(E,rho)|^2) < infinity.
```

No checked fixed-GL2/EC source supplies this.

External:

- BFMT/WMC zeta results: [arXiv:2310.03949](https://arxiv.org/abs/2310.03949)
- Milinovich-Ng fixed newform shifted/positive moment adjacency:
  [arXiv:1306.0854](https://arxiv.org/abs/1306.0854)
- Li-Zaharescu fixed/Selberg-class adjacent but wrong direction:
  [PDF](https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf)
- Booker-Cho-Kim simple zeros: [arXiv:1802.01764](https://arxiv.org/abs/1802.01764)
- de Faveri simple-zero lower bounds:
  [EMS/JEMS record](https://ems.press/journals/jems/articles/14298254)

Verdict:

```text
NO-GO / rigorous reduction only.
Displacement/Palm remains the better route.
```

## Multiple Zeros: Separate Blocker

The simple-zero H1 stack does not handle multiple zeros.

Correct remaining condition:

```text
H1-MultipleZeroDisposition(E,W,r).
```

For every crossed offcentral multiple zero `rho=1+alpha`, let:

```text
m = ord_(s=rho) L(E,s).
```

Laurent residue profile:

```text
P_alpha(u)
  = e^(alpha u) sum_(ell=0)^(D_alpha) A_(alpha,ell)^net u^ell.
```

Every term must be handled by one of:

```text
(A) absent by H1-OffcentralCriticalSimplicity(E);
(B) killed by H1-MultipleZeroKernelKill(E,W);
(C) retained in explicit H1-RetainedMultipleZeroProfile(E,W;T_box);
(D) unretained and central-negligible:
    D_alpha < r, with lower-degree aggregate o(u^r).
```

For rank one `r=1`, central-only pointwise H1 needs:

```text
D_alpha <= 0
```

for every unretained critical-line multiple-zero exponent, plus:

```text
Z_0^mult(u)
 = sum_(Re alpha=0, alpha!=0, mult)
     A_(alpha,0)^net e^(alpha u)
 = o(u).
```

Repo:

- [H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md)

## Full Conditional Simple-Zero Stack

Current simple-zero stack:

```text
WeakSeparatedEC-BFMT-H1(E,c)
+ ClusterShiftDerivativeComparison(E,A)
+ Degree2WeakShiftedNeg_q(E)
+ RootedInvProdCorr_p(E,A), p=q/(q-1)
=> R_E,1^simp(T)=o(T^2).
```

Concrete q=2 version:

```text
WeakSeparatedEC-BFMT-H1(E,c)
+ Degree2WeakShiftedNeg_2(E)
+ RootedPalmRepulsionExpMoment_2(E,A)
=> R_E,1^simp(T)=o(T^2).
```

Concrete q=3 target:

```text
WeakSeparatedEC-BFMT-H1(E,c)
+ Degree2WeakShiftedNeg_3(E)
+ PrimeScaleRootedPalmBox_beta(E,A;W), beta>3/2
=> R_E,1^simp(T)=o(T^2).
```

Repo:

- [H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md)
- [H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md)

## Agent Wave Results Already Tried

Several GPT-5.5/xhigh waves attacked the wall. Condensed outcomes:

### H1 Prime-Scale Displacement

Verdict: promising as coordinate discovery, not proof.

Transition object:

```text
D_{rho,lambda}^{E,W}(T)
 =
 sum_p W(log p/log T) lambda_E(p)^2/p
 |e^(-i gamma_rho log p)-e^(-i gamma_lambda log p)|^2.
```

It identifies normalized local distance through prime phases, but does not
control inverse-product cluster weights alone.

### H1 q=3/q=4 Shifted Moment

Verdict: conditional pass, source gap.

No algebraic failure found for q=3 or q=4. Need explicit
`ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=3/2)` and possibly `k=2`.

### H1 Bad-Cluster Mechanism Classifier

Verdict: useful taxonomy but no theorem.

Mechanisms:

```text
ordinary close pairs,
repeated prime-phase alignment,
high-multiplicity clusters,
multiple-zero effective-degree cases.
```

Mass can hide in higher clusters; pair-only analysis is insufficient.

### Determinantal/Hadamard Template

Verdict: model proves the desired shape; transfer missing.

Sine DPP/Palm gives beta=3 via Schur complement + Hadamard. Fixed GL2 lacks
finite-T determinant, negative association, or uniform Palm majorant.

### Beurling-Selberg / Restricted n-Level Density

Verdict: no-go.

Needs bandwidth `Delta~1/r`; RS/Hejhal support keeps `Delta` bounded.

### Multiplicity / Cluster Truncation

Verdict: no-go from known inputs.

Uniform finite-M cluster cap would suffice but is unavailable.

### Higher-q Escape

Verdict: helps but does not break wall.

Best q=3/p=3/2. Large q makes savings tiny and shifted moment constants worse.
Product-layer p=1 does not imply p=1+eta.

### Direct Reciprocal Tail / l1 Escape

Verdict: no-go / rigorous reduction.

Bypasses Palm only by demanding fixed-GL2 reciprocal derivative negative
moments not currently known.

### Adversarial Referee

Verdict: no source-closed wall break.

Hard kill criteria:

```text
- Uses fixed-test correlations then lets cutoff approach u=0 without uniform error.
- Proves only pair law, not all m with summable constants.
- Lets q grow with T or p->1 without uniform BFMT/Palm constants.
- Fails mu_q/q + 1/p < 2.
- Mixes raw gaps with normalized u=logT|rho-rho0|.
- Ignores multiple zeros or atoms at u=0.
- Changes pointwise central theorem into retained-profile/averaged theorem.
```

Would reverse only with:

```text
1. Degree2WeakShiftedNeg_q(E) for fixed q>2.
2. Fixed-EC rooted Palm box law beta>p, all m, summable constants.
3. Multiple-zero disposition in same theorem mode.
```

## Trap List

Do not spend serious effort on these unless adding a genuinely new ingredient:

1. Ordinary pair correlation alone.
   It only sees `m=1`.

2. Smooth fixed-test n-level density alone.
   It cannot handle singular weights or shrinking boxes.

3. Density-one simplicity.
   A zero-density exceptional set can dominate inverse-product sums.

4. Existence of small gaps.
   Wrong direction.

5. Fixed finite cluster truncation without a hard theorem.
   It hides the same Palm tail.

6. ProductLayer p=1.
   Does not imply p>1.

7. Direct reciprocal derivative l1 tail.
   At least as hard as the Palm wall from known fixed-GL2 sources.

8. H2/GL1 profile smoothing.
   Useful elsewhere, but theorem-mode drift for pointwise H1.

9. Numerical EC evidence.
   Diagnostic only. No numerical result promotes a theorem.

10. Raw `a_p^2/p` prime weights.
    Use normalized `lambda_E(p)^2/p = a_p^2/p^2`.

## Exact Challenge Set For GPT-5.5 Pro Extended

### Challenge 1: Prove Rooted Box Law

Main:

```text
Prove PrimeScaleRootedPalmBox_beta(E,A;W)
for beta>3/2, all m, summable constants.
```

Allowed forms:

```text
1. Direct:
   J_m^(3/2)(T;A) <= C_m T log T,
   sum_m C_A^m C_m/m! < infinity.

2. Box:
   nu_m,T^W(prod_j (0,r_j])
     <= C_m T log T prod_j r_j^beta,
   beta>3/2,
   sum_m K_A^m C_m/m! < infinity.

3. Density majorant:
   dnu_m,T,A(u)
     <= C_m T log T prod_j u_j^2 H_m(u) du,
   with enough integrability and summability.

4. New finite-T determinantal/negative-association substitute for fixed EC/GL2.

5. A new explicit-formula/large-sieve method giving shrinking-box repulsion,
   not just fixed-test correlation.
```

Kill if:

```text
only pair layer,
only fixed-test convergence,
no uniform lower-endpoint control,
constants not summable in m,
or beta<=3/2 for q=3.
```

### Challenge 2: Source-Close Degree2WeakShiftedNeg_3

Prove/audit:

```text
sum_(rho in S_E(T)) |L_E^*(rho+1/logT)|^(-3)
  << T^(7/2+eps).
```

Needed source work:

```text
BFMT/DPMV coefficient audit for k=3/2,
degree-2 conductor normalization,
zero-sampling substitution,
prime-power/bad-prime/polylog losses,
uniformity over zero ordinates.
```

Kill if:

```text
conductor/zero-sampling terms exceed T^(7/2+eps),
constants require q growing with T,
or separated-only inputs are mistakenly used for all zeros.
```

### Challenge 3: Bypass Palm With Fixed-GL2 Reciprocal Tail

Hard alternative:

```text
sum_(T<|gamma|<=2T) |L'(E,rho)|^(-p)
  = o(T^(p+1)/(log T)^(p-1))
```

for some `p>1`.

This would imply simple-zero H1 without rooted Palm. Current assessment:
lower probability than Challenge 1.

### Challenge 4: Multiple-Zero Disposition

Even after simple-zero closure, prove or package:

```text
H1-MultipleZeroDisposition(E,W,r).
```

For rank one, unretained multiple-zero terms need:

```text
D_alpha <= 0,
Z_0^mult(u)=o(u).
```

This is not the first wall but must be kept in scope.

## Claim Ledger

Allowed now:

```text
The H1 displacement method reduces bad simple zeros to:
Degree2WeakShiftedNeg_q(E) + RootedInvProdCorr_p(E,A).
```

Allowed now:

```text
For q=3, p=3/2, these imply
R_B(T,c) << T^(11/6+eps+o(1)).
```

Allowed now:

```text
Sine-kernel Palm model predicts beta=3, enough for q=3.
```

Not allowed:

```text
RootedPalmBox_q3 is known.
Restricted n-level density proves the needed singular rooted law.
Pair repulsion closes H1.
Small-gap existence helps directly.
Direct reciprocal tails are source-closed.
Full H1 follows without multiple-zero and contour hypotheses.
Numerics promote theorem status.
```

## Core Repo Pointers

Root summary:

- [H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md)

Main reductions:

- [CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md)
- [SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/SHIFTED_CLUSTER_WEIGHT_CRITERION_2026-05-11.md)
- [ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/ROOTED_INVPROD_CORR2_REDUCTION_2026-05-11.md)

Source audits:

- [ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/ROOTED_PALM_REPULSION_SOURCE_AUDIT_2026-05-11.md)
- [UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/UNIFORM_SMALL_GAP_SOURCE_HUNT_2026-05-11.md)
- [DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md)
- [WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/WEAK_SEPARATED_BFMT_H1_AUDIT_2026-05-11.md)

Conditional stack and remaining blockers:

- [H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md)
- [H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md](handoff-2026-05-11-post-wave5-pivot/H1_MULTIPLE_ZERO_DISPOSITION_CURRENT_2026-05-11.md)

Related implementation wave:

- [H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md](handoff-2026-05-11-implementation-wave/H1_Q_GT_2_BAD_SET_ROUTE_2026-05-11.md)
- [IMPLEMENTATION_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-implementation-wave/IMPLEMENTATION_SYNTHESIS_2026-05-11.md)

BFMT / zero-sampling background:

- [ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md](handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md)
- [ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md](handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md)
- [BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md](handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md)
- [GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md](handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md)

Earlier wave context:

- [BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md)
- [BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md)
- [TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md](handoff-2026-05-11-top10-challenge-wave/TOP10_CHALLENGE_WAVE_SYNTHESIS_2026-05-11.md)

Wiki/index:

- [index.md](index.md)
- [log.md](log.md)
- [HANDOFF.md](HANDOFF.md)

## External References

Primary/adjacent sources already used or checked:

1. Bui-Florea-Milinovich-Turnage-Butterbaugh, negative moments / reciprocal
   derivative methods:
   [arXiv:2310.03949](https://arxiv.org/abs/2310.03949)

2. Milinovich-Ng, fixed newform prime sums / derivative moment adjacency:
   [arXiv:1306.0854](https://arxiv.org/abs/1306.0854)

3. Rudnick-Sarnak, *Zeros of principal L-functions and random matrix theory*:
   [PDF](https://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/rudnick-sarnak.pdf)

4. Hejhal, *On the triple correlation of zeros of the zeta function*:
   [Oxford record](https://academic.oup.com/imrn/article-abstract/1994/7/293/906602)

5. Vaaler, *Some extremal functions in Fourier analysis*:
   [AMS record](https://www.ams.org/journals/bull/1985-12-02/S0273-0979-1985-15349-2/)

6. GL2 gaps:
   [arXiv:1410.7765](https://arxiv.org/abs/1410.7765)

7. Higher-level correlations / multiplicity adjacency:
   [arXiv:2303.01095](https://arxiv.org/abs/2303.01095)

8. Gap upper-bound adjacency:
   [arXiv:2511.13898](https://arxiv.org/abs/2511.13898)

9. Inoue 2026 small-gap adjacency:
   [arXiv:2604.05733](https://arxiv.org/abs/2604.05733)

10. Li-Zaharescu fixed/Selberg-class reciprocal derivative adjacency:
    [PDF](https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf)

11. Booker-Cho-Kim simple zeros:
    [arXiv:1802.01764](https://arxiv.org/abs/1802.01764)

12. de Faveri simple-zero lower bounds:
    [EMS/JEMS record](https://ems.press/journals/jems/articles/14298254)

## Suggested Work Plan For Pro Extended

1. Re-derive the Holder exponent arithmetic independently.

   Check:

   ```text
   R_B(T,c)
    << T^o(1)(logT)^(-1)
       T^((q+1/2)/q) (TlogT)^(1/p)
    = T^(2-1/(2q)+o(1)).
   ```

2. Choose one target:

   Main:

   ```text
   q=3, p=3/2.
   ```

   Fallback:

   ```text
   q=4, p=4/3.
   ```

3. Try to prove all-cluster rooted box law by a method not killed above.

   The known RS/Hejhal fixed-support route is dead unless you add a uniform
   shrinking-test theorem.

4. If attacking via explicit formula, state exactly how shrinking windows
   avoid the support barrier and how all-m constants stay summable.

5. If attacking via random matrix universality, identify a fixed-curve theorem
   with finite-T uniform error strong enough for singular tests. Ordinary
   convergence is not enough.

6. If attacking q=3 shifted moment, source-close the BFMT k=3/2 coefficient
   ledger. Do not assume q=2 generalizes without audit.

7. Keep multiple-zero and contour hypotheses separate. Do not promote full H1.

## Final Answer Expected From Pro Extended

Return one of:

```text
BREAK:
  A proof/source-closed theorem of PrimeScaleRootedPalmBox_beta(E,A;W)
  for beta>3/2, all m, summable constants,
  or a direct fixed-GL2 reciprocal-tail theorem sufficient for H1.

REDUCTION:
  A strictly sharper named condition than the current rooted box law,
  with exact formula and proof of implication to R_B(T,c)=o(T^2).

KILL:
  A rigorous obstruction showing the q=3 displacement route cannot work
  under plausible fixed-EC assumptions.

SOURCE:
  A primary-source theorem with page/equation-level citation that we missed,
  and a normalization audit proving it implies the needed condition.
```

Anything else is not a wall break.
