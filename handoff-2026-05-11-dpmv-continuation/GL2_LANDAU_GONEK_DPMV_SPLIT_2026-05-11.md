---
schema_version: 1
title: "GL2 Landau-Gonek DPMV Split"
date: 2026-05-11
type: theorem-reduction
tier: working
status: RIGOROUS_REDUCTION
confidence: 0.82
tags: [h1, gl2, landau-gonek, dpmv, reciprocal-derivative, bfmt]
---

# GL2 Landau-Gonek DPMV Split

Status: `RIGOROUS_REDUCTION`. No theorem is promoted.

## Verdict

Wave 3 named the next H1 target:

```text
GL2-LandauGonek-DPMV(E,theta).
```

That target was too compressed. Source checking splits it into four layers:

```text
LG-Explicit-GL2(f)
DPMV-GL2-GeneralA(f,eta)
DPMV-GL2-PrimePowerHighMoment(f,2/3)
BFMT-CoefficientErrorCheck(f,W_BFMT)
```

The first layer is source-closed for holomorphic newforms in the Milinovich-Ng
setting. The second and third layers are source-backed but not yet BFMT-complete.
The fourth layer is the live blocker.

The exact revised target is:

```text
BFMT-CoefficientErrorCheck(E):
  For every Dirichlet polynomial coefficient family produced by the BFMT
  exponential truncation at k=1/2, Milinovich-Ng Proposition 4.1 or an
  equivalent GL2 DPMV gives the same T^(1+delta) separated-zero estimate.
```

If this check fails, the BFMT separated-zero route is dead in its current form.
If it succeeds, Wave 3's bad-set budget remains the independent H1 blocker.

## Source Protocol

Workspace:

```bash
/tmp/farey-dpmv-continuation-20260511
```

Commands:

```bash
curl -L --fail -s -o xpdf-tools-mac-4.06.tar.gz \
  https://dl.xpdfreader.com/xpdf-tools-mac-4.06.tar.gz
tar -xzf xpdf-tools-mac-4.06.tar.gz

curl -L --fail -s -o bfmt_2310_03949.pdf \
  https://arxiv.org/pdf/2310.03949
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  bfmt_2310_03949.pdf bfmt_2310_03949.txt

curl -L --fail -s -o li_zaharescu_DLrho.pdf \
  'https://www.math.ucdavis.edu/~junxian/paper/DL%28rho%29.pdf'
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  li_zaharescu_DLrho.pdf li_zaharescu_DLrho.txt

curl -L --fail -s -o milinovich_ng_1306_0854.pdf \
  https://arxiv.org/pdf/1306.0854
./xpdf-tools-mac-4.06/binARM/pdftotext -layout -enc UTF-8 \
  milinovich_ng_1306_0854.pdf milinovich_ng_1306_0854.txt
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011  li_zaharescu_DLrho.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
```

Source anchors:

- BFMT, PDF p. 8, Theorem 3.1. Quote anchor: "any sequence of complex numbers".
- BFMT, PDF p. 8. Quote anchor: "Landau-Gonek explicit formula".
- BFMT, PDF p. 3. Quote anchor: "simplicity of zeros is not enough".
- Li-Zaharescu, PDF p. 2. Quote anchor: "holomorphic cusp forms".
- Li-Zaharescu, PDF p. 7, Theorem 4.1. Quote anchor: "almost all zeros".
- Milinovich-Ng, PDF p. 14, Lemma 3.3. Quote anchor: "version of the Landau-Gonek explicit formula".
- Milinovich-Ng, PDF p. 19, Proposition 4.1. Quote anchor: "Montgomery and Vaughan's mean-value theorem".

## Layer 1: `LG-Explicit-GL2(f)`

Milinovich-Ng Lemma 3.3 gives the GL2 analogue of the Landau-Gonek explicit
formula for a classical holomorphic newform `f`, under their notation:

```text
sum_{0<gamma_f<=T} x^(rho_f)
  = - T Lambda_f(x)/(2*pi)
    + O( x log(2xT) loglog(3x) )
    + O( log x min(T, x/<x>) )
    + O( log(2T) min(T, 1/log x) ).
```

Here `<x>` denotes the distance to the nearest prime power other than `x`
itself, and `Lambda_f(x)=0` when `x` is not a positive integer.

Decision:

```text
LG-Explicit-GL2(f) is source-closed as a modular-form input.
```

This closes only the explicit-formula ingredient. It does not by itself bound
negative reciprocal moments of `L_f'(rho_f)`.

## Layer 2: `DPMV-GL2-GeneralA(f,eta)`

Milinovich-Ng Proposition 4.1 proves a zero-discrete mean-square formula for

```text
A(s)=sum_{n<=Y} a(n)n^(-s),       Y asymp T,
```

assuming RH for `L(s,f)` and coefficient conditions

```text
sum_{n<=x} |a(n)|       << x log(xT)(log x)^(-eta),
sum_{n<=x} |a(n)|^2     << x(log(xT))^2,
```

with `0 < eta <= 1/2`. The formula has shape

```text
sum_{T<gamma_f<=2T} |A(rho_f)|^2
 = T log X/pi * sum_{n<=Y} |a(n)|^2/n
   - Re sum_{n<=Y} ((Lambda_f * a)(n) conjugate(a(n)))/n
   + error_f(a,T,eta).
```

The important feature is not just the main term. It is the extra convolution
error:

```text
T log T * sum_{n>=1} |(Lambda_f * a)(n)|^2 / n^(1+1/logT),
```

plus `T(logT)^(4-2eta)`.

Decision:

```text
DPMV-GL2-GeneralA(f,eta) is source-backed but not automatically BFMT-ready.
```

The BFMT zeta theorem accepts arbitrary coefficients with a simpler error:

```text
O( x (log(xT))^2 sum_{n<=x} |a_n|^2/n ).
```

Milinovich-Ng has a usable GL2 replacement only after proving that the BFMT
coefficient families satisfy the partial-sum hypotheses and that the GL2
convolution error is small enough on every BFMT block.

## Layer 3: `DPMV-GL2-PrimePowerHighMoment(f,2/3)`

Milinovich-Ng Proposition 4.3 proves high-moment estimates for prime-supported
Dirichlet polynomials over zeros of `L(s,f)`, but with support restriction

```text
x^m <= T^(2/3).
```

This is genuinely useful for Soundararajan-style short prime blocks. It is not
the full BFMT support range. BFMT Section 5 uses parameter choices whose total
Dirichlet-polynomial support is pushed to the `T^(1-o(1))` boundary.

Decision:

```text
Prime-power high moments are source-backed only up to the 2/3 support wall.
```

They may close a weaker separated theorem, but they do not yet reproduce the
BFMT `T^(1+delta)` theorem at `k=1/2`.

## Layer 4: `BFMT-CoefficientErrorCheck(E)`

The next exact work item is now finite and technical.

The BFMT coefficient families to check are now explicit:

```text
P0,v^s0:
  a(n)=s0! b(n;Delta_v) nu(n),
  p|n => p<=T^beta0,
  Omega(n)=s0,
  support exponent beta0*s0.

Mixed S_j block:
  a(n) is a convolution over disjoint prime blocks I_0,...,I_j,I_{j+1},
  with E_{ell_h}(k P_{h,j}) factors and P_{j+1,v}^{sj+1},
  support exponent sum_{h<=j} ell_h beta_h + sj+1 beta_{j+1}.

Terminal S_1 block:
  a(n) is a convolution over I_0,...,I_K from product_h E_{ell_h}(kP_{h,K}),
  support exponent sum_{h<=K} ell_h beta_h.
```

BFMT's own conditions force these support exponents below

```text
1 - loglogT/logT.
```

That is why a GL2 high-moment theorem limited to `x^m<=T^(2/3)` is not enough
by itself.

For every coefficient family `a_BFMT(n)` appearing in BFMT Propositions 2.5,
2.6, and 2.7 after the `k=1/2` parameter choices, prove:

```text
1. Partial sums:
   sum_{n<=x} |a_BFMT(n)|       << x log(xT)(log x)^(-eta),
   sum_{n<=x} |a_BFMT(n)|^2     << x(log(xT))^2.

2. Diagonal:
   T logT * sum |a_BFMT(n)|^2/n
   has the same log-log exponent needed by BFMT.

3. GL2 convolution:
   T logT * sum |(Lambda_f * a_BFMT)(n)|^2 / n^(1+1/logT)
   is absorbed into the BFMT target bound for that proposition.

4. Off-diagonal:
   Re sum ((Lambda_f * a_BFMT)(n) conjugate(a_BFMT(n)))/n
   is either sign-favorable or bounded by the diagonal/error budget.

5. Bad primes:
   finitely many ramified Euler factors are removed from prime blocks or
   absorbed into constants without changing exponents.
```

Only after these checks can the previous Wave 3 theorem be upgraded from

```text
GL2-LandauGonek-DPMV(E,theta)
```

to the more precise source-supported input:

```text
BFMT-CoefficientDPMV(E,k=1/2).
```

## Consequence If Layer 4 Closes

If `BFMT-CoefficientErrorCheck(E)` closes, then Wave 3 Agent 01 gives the
separated-zero estimate

```text
sum_{gamma in F_E(T,c)} |L'(E,1+i gamma)|^(-1)
  <<_{E,c,delta} T^(1+delta).
```

This is enough for the separated good set because `T^(1+delta)=o(T^2)` for
fixed `delta<1`.

It still does not close rank-one H1. The remaining independent target is:

```text
EC-BFMT-BadSetBudget(E,c):
sum_{gamma notin F_E(T,c), simple}
  |L'(E,1+i gamma)|^(-1) = o(T^2).
```

## Consequence If Layer 4 Fails

If the BFMT coefficient families fail Milinovich-Ng's hypotheses or the
convolution error cannot be absorbed, then the BFMT-separated route is dead in
its current form. The fallback is not another broad source hunt. It is one of:

```text
H1-ActualDyadicShellPV(E,W,r,H)
H1-LocalMinMod(E) plus bad reciprocal budget
stronger kernel/support restriction producing a weaker separated theorem
```

The third fallback cannot promote EC stabilization by itself unless its support
restriction is still strong enough for the legal-height H1 finite-box theorem.

## Immediate Audit Checklist

The next packet should be purely mechanical:

```text
1. Transcribe BFMT parameters (5.1)-(5.7) at k=1/2.
2. For each proposition, compute the maximum support exponent.
3. Prove or disprove Milinovich-Ng condition (39) for the BFMT coefficients.
4. Prove or disprove condition (40).
5. Estimate Lambda_f * a_BFMT using |Lambda_f(n)| <= C_E Lambda(n).
6. Compare the resulting error to the exact BFMT target in Proposition 2.5,
   Proposition 2.6, and Proposition 2.7.
7. Mark one of:
   RIGOROUS_REDUCTION or NO_GO.
```

Do not proceed to `EC-BFMT-BadSetBudget(E,c)` until this audit is done.

## No-Promotion Boundary

This packet does not prove `R_E,1(T)=o(T^2)`. It source-closes only the GL2
explicit-formula layer and isolates the remaining DPMV work to a coefficient
audit against Milinovich-Ng Proposition 4.1 and Proposition 4.3.

Analytic rank only. No BSD/algebraic-rank substitution. No H2 branch damping is
used as H1 reciprocal-pole control. No Koyama correspondence or email draft is
touched.
