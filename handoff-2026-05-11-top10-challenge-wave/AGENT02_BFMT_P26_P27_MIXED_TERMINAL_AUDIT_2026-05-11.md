---
schema_version: 1
title: "Agent 02 BFMT Proposition 2.6/2.7 Mixed-Terminal Audit"
date: 2026-05-11
agent: "Top 10 Challenge Wave Agent 02"
type: coefficient-audit
tier: working
status: NO_GO
confidence: 0.86
tags: [top10-challenge-wave, h1, bfmt, dpmv, milinovich-ng, coefficient-audit]
---

# Agent 02 BFMT Proposition 2.6/2.7 Mixed-Terminal Audit

Status: `NO_GO`.

## Verdict

`BFMT-CoefficientErrorCheck` fails for the BFMT Proposition 2.6 mixed families against the available Milinovich-Ng inputs.

Fatal reason:

```text
Milinovich-Ng Proposition 4.1 condition (40) is false for the BFMT
Proposition 2.6 mixed coefficients because the terminal P_{j+1,v}^{s_{j+1}}
factor has s! multinomial coefficients.
```

The same mixed families also exceed the Milinovich-Ng Proposition 4.3 support wall `x^m <= T^(2/3)` at `k=1/2`.

Proposition 2.7 terminal families are not the fatal obstruction by themselves: their BFMT total support is small in the `k=1/2` second branch. But MN Proposition 4.3 still does not directly cover the multi-block terminal product, and MN Proposition 4.1 would still need a separate coefficient partial-sum lemma. Since Proposition 2.6 is required in BFMT's proof, the BFMT-separated GL2 route is dead against MN 4.1/4.3 as currently sourced.

No theorem is promoted.

## Source Protocol

Workspace used:

```bash
/tmp/farey-agent02-bfmt-20260511
```

Commands used:

```bash
curl -L --fail -s -o bfmt_2310_03949.pdf https://arxiv.org/pdf/2310.03949
curl -L --fail -s -o milinovich_ng_1306_0854.pdf https://arxiv.org/pdf/1306.0854
curl -L --fail -s -o bf_2302_07226.pdf https://arxiv.org/pdf/2302.07226
pdftotext -raw/-layout via xpdf-tools-mac-4.06
```

SHA256:

```text
4a6b2f30ef78d9e615141abe54e416760e74ab69507deca8c51116972d1ad36d  bfmt_2310_03949.pdf
7429a8705e1d7e790a925bd7a410338a52e24ab060e890bdb13f9b8780810f10  milinovich_ng_1306_0854.pdf
14740c801f9739340258b66fe09a757abdcd891eb129858f45b54cea8ae1c5d1  bf_2302_07226.pdf
```

Source anchors:

- BFMT, PDF p. 8, Propositions 2.6 and 2.7: support hypotheses contain `<= 1 - log log T/log T`.
- BFMT, PDF p. 15, equations (5.1)-(5.7): parameter choices.
- Milinovich-Ng, PDF p. 18, equations (39)/(40): quote anchor "two conditions".
- Milinovich-Ng, PDF p. 19, Proposition 4.1, equation (41): zero mean-square formula.
- Milinovich-Ng, PDF p. 19, Proposition 4.3: quote anchor `x^m <= T^(2/3)`.
- Milinovich-Ng, PDF p. 12, equation (23): quote anchor `|Lambda_f(n)| <= 2 Lambda(n)`.
- Bui-Florea 2302.07226, PDF pp. 6, 9, equations (2.1), (3.1), (3.2): explicit `b_alpha(p;Delta)` source delegated by BFMT.

Short source quotes:

```text
BFMT p.15: "If 2k(1 + eps) > 1"
MN p.18: "two conditions"
MN p.19: "x^m <= T^(2/3)"
BF p.9: "b_alpha(p; Delta) = -a_alpha(p; Delta) log p"
```

## BFMT Parameters At k = 1/2

Let

```text
L = log T,      L2 = log log T.
```

For `k=1/2` and any fixed positive BFMT `eps`, the first branch `2k(1+eps) <= 1` is not legal. The proof uses BFMT (5.6)-(5.7):

```text
a = (1 - 3eps/2)/(1 - eps),
r = 1/(1 - eps),
d = (4 - 7eps)/(4 - 6eps),
a(2d - 1)/r = 1 - 2eps.
```

Put

```text
B = 2k + 2d - 1 - a(2d - 1)/r
  = 2d - 1 + 2eps
  = 2(1 - 3eps^2)/(2 - 3eps)
  = 1 + 3eps/2 + O(eps^2).
```

Then

```text
beta_0 = 2B/(1 + delta0) * L2/L,
beta_j = r^j beta_0.
```

The second branch has the special initial value

```text
s_0 = floor(1/beta_0),    ell_0 = 2 floor(s_0^d/2).
```

For the mixed `S_2` blocks BFMT still uses, for `j >= 1`,

```text
s_j = floor(a/beta_j),    ell_j = 2 floor(s_j^d/2).
```

This is forced by the later BFMT `S_2` calculation: the terminal mixed factor contributes `s_{j+1} beta_{j+1} = a + O(beta_{j+1})`; otherwise the displayed support inequalities after (5.5) cannot hold.

## Exact Support Exponents

For BFMT Proposition 2.6, the mixed coefficient family

```text
prod_{h=0}^j E_{ell_h}(k P_{h,j}) * P_{j+1,v}^{s_{j+1}}
```

has exact support exponent

```text
theta_mix(j)
  = beta_0 * 2 floor(floor(1/beta_0)^d/2)
    + sum_{h=1}^j beta_h * 2 floor(floor(a/beta_h)^d/2)
    + beta_{j+1} * floor(a/beta_{j+1}).
```

Asymptotically,

```text
theta_mix(j)
  = a + beta_0^(1-d) + a^d sum_{h=1}^j beta_h^(1-d)
    + O(sum_{h<=j+1} beta_h).
```

BFMT's post-(5.5) condition gives

```text
theta_mix(j) <= 1 - L2/L.
```

But for the first mixed block,

```text
theta_mix(0) = a + beta_0^(1-d) + o(1)
             = 1 - eps/(2(1 - eps)) + o(1).
```

Thus, for any small BFMT `eps` used in the theorem, `theta_mix(0) > 2/3`. The mixed family crosses the MN Proposition 4.3 wall immediately.

For BFMT Proposition 2.7, the terminal coefficient family

```text
prod_{h=0}^K E_{ell_h}(k P_{h,K})
```

has exact support exponent

```text
theta_term(K)
  = beta_0 * 2 floor(floor(1/beta_0)^d/2)
    + sum_{h=1}^K beta_h * 2 floor(floor(a/beta_h)^d/2).
```

BFMT's (5.5) condition, with the special `h=0` second-branch term included as `beta_0^(1-d)=o(1)`, gives asymptotically

```text
theta_term(K) <= 1 - a + o(1)
               = eps/(2(1 - eps)) + o(1).
```

So the terminal total support is below `2/3` for the small fixed `eps` regime. The 2/3 wall kills Proposition 2.6 mixed support, not the terminal total-support exponent.

## MN Conditions (39)/(40)

Milinovich-Ng Proposition 4.1 requires unweighted partial sums:

```text
sum_{n<=x} |a(n)|  << x log(xT) (log x)^(-eta),
sum_{n<=x} |a(n)|^2 << x (log(xT))^2.
```

The second condition fails for BFMT Proposition 2.6.

Take `j=0`, `v=1`, and

```text
s = s_1 = floor(a/beta_1),     beta_1 = r beta_0.
```

The terminal factor `P_{1,1}^s` contributes, for squarefree

```text
n = p_1 ... p_s,       p_i in I_1,
```

the coefficient

```text
A(n) = s! * prod_i b(p_i; Delta_1)
```

up to the harmless shift factor `n^(-1/L)`.

The explicit Bui-Florea formula for `b_alpha(p;Delta)` shows that, for primes in a fixed lower subinterval of `I_1`, `|b(p;Delta_1)| >= c_eps > 0` for all large `T`. This is the `alpha Delta -> 0` range; the `j=0` term already gives a positive constant when `log p/(2pi Delta_1) = 1/r + o(1)`.

Choose `s` distinct such primes. Then

```text
log |A(n)|^2
  >= 2s(log s - 1 + log c_eps) + O(log s)
  = ((a/r) * (1 + delta0)/B + o(1)) L.
```

For the same choice,

```text
log n = (a/r + o(1)) L.
```

If `eps` is chosen small relative to `delta0`, then `B < 1 + delta0`, hence

```text
|A(n)|^2 > n (log(nT))^2
```

by a fixed power of `T`. Therefore MN condition (40) is false for the BFMT mixed family.

This is not just an unproved estimate. It is a direct coefficient-size obstruction from the `s!` terminal power in Proposition 2.6.

## Convolution And Off-Diagonal

If a BFMT coefficient family did satisfy MN (39)/(40), the extra GL2 terms in MN Proposition 4.1 would be absorbable at the final `T^(1+delta)` level.

Let

```text
D = sum |a(n)|^2 / n^(1 + O(1/L)).
```

Using Milinovich-Ng (23),

```text
|Lambda_f(n)| <= 2 Lambda(n).
```

Then a standard weighted Cauchy/Young bound gives

```text
sum |(Lambda_f * a)(n)|^2 / n^(1 + 1/L)
  << (log T)^2 D.
```

Thus the MN convolution error is

```text
T log T * sum |(Lambda_f * a)(n)|^2/n^(1+1/L)
  << T (log T)^3 D.
```

The explicit off-diagonal term satisfies

```text
|sum ((Lambda_f * a)(n) conjugate(a(n)))/n|
  << (log T) D,
```

so it is smaller than the main zero-average scale `T log T * D`.

Conclusion: convolution/off-diagonal terms are not the fatal obstruction. The fatal obstruction is that Proposition 2.6 cannot enter MN Proposition 4.1 because condition (40) fails before the formula is available.

## Proposition 4.3 Support Wall

Milinovich-Ng Proposition 4.3 requires

```text
x^m <= T^(2/3).
```

For Proposition 2.6 mixed families, already

```text
theta_mix(0) = 1 - eps/(2(1 - eps)) + o(1) > 2/3
```

for the BFMT small-`eps` regime. Therefore MN Proposition 4.3 cannot reproduce BFMT Proposition 2.6.

For Proposition 2.7 terminal families,

```text
theta_term(K) <= eps/(2(1 - eps)) + o(1),
```

so total support alone is not over the `2/3` wall. But MN Proposition 4.3 is a high-moment estimate for powers of one prime-supported polynomial. The BFMT terminal object is a product of independently truncated blocks. Collapsing it into one prime polynomial up to `T^beta_K` would impose the stronger and wrong condition

```text
beta_K * sum_h ell_h <= 2/3,
```

not the BFMT condition

```text
sum_h beta_h ell_h <= 2/3.
```

Those are not equivalent. MN 4.3 therefore does not directly source-close Proposition 2.7 either, although Proposition 2.7 is not the place where the full BFMT package dies.

## Final Decision

```text
BFMT-CoefficientErrorCheck(E; P2.6/P2.7 mixed-terminal)
  = NO_GO against Milinovich-Ng Proposition 4.1/4.3.
```

What survives:

```text
If one supplies a new GL2 zero-discrete mean-value theorem allowing arbitrary
BFMT coefficients, or a new partial-sum theorem for the P^s mixed coefficients
despite the factorial spike, then the convolution/off-diagonal terms are only
polylogarithmic losses and should be absorbable in the final T^(1+delta) target.
```

What does not survive:

```text
Milinovich-Ng Proposition 4.1/4.3, as stated, cannot replace BFMT Theorem 3.1
for Proposition 2.6. Therefore the BFMT separated-zero route is not source-closed
by the checked MN inputs.
```
