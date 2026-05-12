---
title: "AGENT01 GL2 BFMT Log Lower Bound"
date: 2026-05-11
type: theorem-reduction
tier: working
status: CONDITIONAL_THEOREM
confidence: 0.90
tags: [breakthrough-wave-4, h1, gl2, elliptic-curve, bfmt, log-lower-bound, prime-polynomial]
---

## Verdict

`GL2-BFMT-PrimePolynomialLowerBound(E)` is available as a fixed-newform
conditional theorem, assuming GRH for the fixed newform and the standard
GL2/Weil explicit formula for the completed newform with the
Carneiro-Chandee majorant test function.

The prime-square, higher-prime-power, and bad-prime Euler terms cost only
`O_E(log log T)` in the BFMT parameter range.  The only non-cosmetic change is
archimedean: BFMT's zeta `log T` term must be replaced by the GL2 analytic
conductor term.  A literal zeta-archimedean `BFMT_error(Delta,T)+O_E(loglogT)`
form is false; the correct replacement is conductor-normalized.

## Theorem Target

Let `L_E^*(s)=L(E,s+1/2)` be the normalized fixed-newform L-function, so the
critical line is `Re s=1/2`.  Put

```text
s = 1/2 + alpha + it,     alpha = 1/log T,     T <= t <= 2T,
x = exp(2 pi Delta).
```

Let `a_alpha(n;Delta)` be the Bui-Florea/Carneiro-Chandee majorant coefficient
from the proof of Bui-Florea Lemma 2.1, supported on `n<=x`, and define the
BFMT-sign prime coefficient

```text
b_E(p;Delta) := - a_alpha(p;Delta) log p       (p not | N_E).
```

Then, uniformly in the BFMT range of `Delta`,

```text
log |L_E^*(s)|
 >= A_E(t;alpha,Delta)
    - Re sum_(p<=x, p not | N_E)
        b_E(p;Delta) lambda_E(p) p^(-s)
    - C_E log log T
    + O_E(Delta^2 exp(pi Delta)/T
          + Delta log(1+Delta T)/sqrt(T)).
```

Here `A_E` is the explicit conductor/gamma term coming from the completed
newform.  With the normalization in Milinovich-Ng,

```text
A_E(t;alpha,Delta)
 = [log C_E(t) + O_E(1)]/(2 pi Delta)
     * log(1 - exp(-2 pi alpha Delta))
   + O_E(1),

C_E(t) asymp_E T^2.
```

Equivalently, before absorbing prime powers,

```text
log |L_E^*(s)|
 >= A_E(t;alpha,Delta)
    + Re sum_(n<=x) Lambda_E(n) a_alpha(n;Delta) n^(-s)
    + O_E(Delta^2 exp(pi Delta)/T
          + Delta log(1+Delta T)/sqrt(T)).
```

Splitting the last sum gives the displayed prime-polynomial form plus only
`O_E(log log T)` loss.

## Source Anchors

- `primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md`: names this lower bound as the remaining local input after zero-sampling closes the coefficient side.
- `primes-equispaced/handoff-2026-05-11-breakthrough-wave-3/AGENT01_GL2_BFMT_ADAPTATION_BLUEPRINT_2026-05-11.md`: isolates prime, prime-square, bad-prime, conductor, and gamma bookkeeping as the major GL2 replacement for BFMT Lemmas 2.3-2.4.
- `/tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt`: BFMT Lemma 2.3 states the zeta prime-polynomial lower bound and the coefficient bound `(2.4)-(2.5)`.
- `/tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt`: Bui-Florea Lemma 2.1 proves the underlying lower bound from the Carneiro-Chandee majorant; its proof explicitly passes through prime powers and then bounds prime squares/cubes.
- `/tmp/farey-homogeneous-bfmt-20260511/carneiro_chandee_1008_4970.txt`: Carneiro-Chandee Lemma 8 gives the extremal majorant; equations `(3.1)-(3.2)` convert the zero sum into gamma/conductor and prime-power terms.
- `/tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt`: equations `(18)-(23)` give the newform Euler product, functional equation, Deligne bounds, and `Lambda_f(p)=lambda_f(p)log p`, `Lambda_f(p^2)=(lambda_f(p^2)-chi(p))log p`, `|Lambda_f(n)|<=2 Lambda(n)`.
- Same Milinovich-Ng source, Lemma 3.1: the fixed-newform zero-count/gamma normalization has density `theta_f'(t)=O_f(log t)` and conductor scale `sqrt(q)t`.

## Proof Attempt

Apply the Carneiro-Chandee majorant `m_Delta` to

```text
f_alpha(u)=log((4+u^2)/(alpha^2+u^2)).
```

The Hadamard factorization of the completed fixed-newform L-function gives the
same inequality as Carneiro-Chandee `(3.1)`, with the zeta gamma factor replaced
by the completed-newform conductor/gamma factor:

```text
log |L_E^*(1/2+alpha+it)|
 >= arch_E(t;alpha) - (1/2) sum_rho m_Delta(t-gamma_rho) + O_E(1).
```

Use the GL2 Weil explicit formula with test function `m_Delta(t-z)`.  The zero
sum becomes:

```text
conductor/gamma contribution
- Re sum_(n<=x) Lambda_E(n) a_alpha(n;Delta) n^(-s)
+ endpoint errors.
```

Moving signs gives

```text
log |L_E^*(s)|
 >= A_E(t;alpha,Delta)
    + Re sum_(n<=x) Lambda_E(n) a_alpha(n;Delta) n^(-s)
    + endpoint errors.
```

The endpoint errors are the same majorant-growth terms as in Bui-Florea:

```text
O_E(Delta^2 exp(pi Delta)/T
    + Delta log(1+Delta T)/sqrt(T)
    + 1).
```

Now split the GL2 von Mangoldt coefficients.

Good primes:

```text
Lambda_E(p)=lambda_E(p) log p,
```

so this is exactly the desired BFMT prime polynomial after setting
`b_E(p;Delta)=-a_alpha(p;Delta)log p`.

Good prime squares:

```text
Lambda_E(p^2)=(lambda_E(p^2)-1)log p,       |lambda_E(p^2)-1|<=2.
```

Bui-Florea's coefficient estimates in the proof of Lemma 2.1 give

```text
sum_(p^2<=x) log p * a_alpha(p^2) / p^(1+2alpha)
  << log log x + 1_(Delta alpha=o(1)) log(1/(Delta alpha))
  << log log T
```

throughout the BFMT range.  Hence the whole prime-square term is
`O_E(log log T)`.

Higher good prime powers use `|Lambda_E(n)|<=2 Lambda(n)` and `m>=3`, giving
an absolutely convergent tail plus the same harmless coefficient factor:

```text
sum_(p^m<=x, m>=3) |Lambda_E(p^m)| a_alpha(p^m) / p^(m(1/2+alpha))
  <<_E log log T.
```

Bad primes are finite.  For `p|N_E`, Milinovich-Ng/Li gives bounded local
Satake data, so

```text
sum_(p|N_E, p^m<=x) |Lambda_E(p^m)| a_alpha(p^m) / p^(m(1/2+alpha))
  <<_E log log T.
```

Finally, Stirling applied to the newform gamma factor in Milinovich-Ng's
functional equation evaluates the conductor/gamma piece as

```text
A_E(t;alpha,Delta)
 = [log C_E(t)+O_E(1)]/(2 pi Delta)
     log(1-exp(-2 pi alpha Delta))
   + O_E(1),
```

with `C_E(t) asymp_E T^2`.  This is not an error term; it is the GL2 analogue
of BFMT's zeta archimedean term.

## Obstruction or Closure

Closure:

```text
GL2-BFMT-PrimePolynomialLowerBound(E)
```

is closed in conductor-normalized form under fixed-newform GRH plus the standard
GL2 Weil explicit formula.

Exact obstruction to the stricter formulation:

```text
zeta BFMT_error(Delta,T) + O_E(log log T)
```

cannot be the literal GL2 statement, because the gamma/conductor term sees
`C_E(t) asymp_E T^2`, not `T`.  This changes the archimedean main term by a
fixed degree factor.  The weakest correct replacement is therefore the theorem
above with `A_E(t;alpha,Delta)`.

No obstruction remains from:

```text
prime squares,
higher prime powers,
bad primes,
Deligne/ramified local bounds.
```

All of those are `O_E(log log T)` in the BFMT ranges.

## Dependency Impact

The separated BFMT stack may now treat the log-lower-bound input as available,
provided Section 5 is run with the GL2 conductor-normalized archimedean term
rather than the literal zeta one.

Together with Agent02's shift-derivative packet and the zero-sampling
coefficient transcription, this closes the separated-zero analytic inputs
modulo that conductor-normalized bookkeeping check.  It still does not touch
`EC-BFMT-BadSetBudget(E,c)`, multiple zeros, or any full H1 reciprocal-tail
claim.
