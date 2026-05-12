---
schema_version: 1
title: "H1 Li-Zaharescu height verification"
date: 2026-05-11
agent: "H1-LZ-Height-Verifier"
type: adversarial-verification
tier: working
status: PARTIAL
verdict: "conditional pass for horizontal H-height; fail as unconditional closure"
confidence: 0.80
sources:
  - handoff-2026-05-11-h1-shell-moment-wave/H1_MINIMUM_MODULUS_SUBSTITUTE_2026-05-11.md
  - /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pdf
  - /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pypdf.txt
tags: [ec-ndc, h1, li-zaharescu, minimum-modulus, contour-tail]
---

# H1 Li-Zaharescu Height Verification

Verdict: `PARTIAL`.

The selected-height mechanism is valid for the H1 horizontal contour-height
input after EC normalization and functional-equation reflection, but only as a
conditional source route with the same right-half zero-location hypothesis used
inside the Li-Zaharescu proof. It is not safe to state as an unconditional
`L in S` closure.

Primary-source packet:

```text
PDF: /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pdf
SHA256: add6657d0568e0f07a28698539a335c4a95ecc819e8083dd521150cfaa7da011
Text: /tmp/h1-lz-height-verify-20260511/li_zaharescu_Lprime_rho.pypdf.txt
```

Short anchors:

- PDF p. 2: holomorphic cusp-form L-functions are examples in the class.
- PDF p. 4, Proposition 3.1: "Each interval [T,T + 1] contains a value".
- PDF p. 20, Lemma 7.6: "If L(s) has no zeros".

## Main Adversarial Finding

Proposition 3.1 is stated for `L in S`, but its proof uses Lemma 7.6, whose
hypothesis is no zeros for `Re s > 1/2`. Lemma 7.8 and Corollary 7.9 depend on
that lemma, and the proof of Proposition 3.1 invokes those bounds.

Therefore the safe citation is not:

```text
LZ Proposition 3.1 unconditionally closes H-height.
```

It is:

```text
Under the normalized EC/newform RH/no-right-half-zero hypothesis,
LZ Proposition 3.1 supplies selected unit-interval heights with
|L(sigma+iT)| >= exp(-A_E log T/loglog T) on 1/2 <= sigma <= 2.
```

If the EC theorem already carries this zero-location hypothesis, the contour
height part passes. If it is meant unconditionally, the claim fails.

## EC/Newform Applicability

The source class `S` includes holomorphic cusp-form L-functions. The local note
uses the standard modularity normalization:

```text
F_E(w) = L(E,w+1/2).
```

For an elliptic curve over `Q`, this is the normalized weight-2 newform
L-function, with center `Re w=1/2` and absolute convergence to the right of
`Re w=1`. This matches the Li-Zaharescu normalization. The local note's
applicability claim is acceptable under modularity and the zero-location caveat
above.

## Normalization And Strip

Li-Zaharescu's strip

```text
1/2 <= Re w <= 2
```

maps under `s_E=w+1/2` to

```text
1 <= Re s_E <= 5/2.
```

For H1, `s_E=1+z` and the horizontal rectangle has

```text
1-eta <= Re s_E <= 1+sigma_z.
```

The right half is covered directly if

```text
sigma_z <= 3/2.
```

The left half reflects by the EC functional equation from `s` to `2-s`, so

```text
1-eta <= Re s <= 1
```

becomes

```text
1 <= Re(2-s) <= 1+eta.
```

This is inside the LZ strip if

```text
eta <= 3/2.
```

The recommended working range remains:

```text
1/2 < eta < 1,
1/2 < sigma_z < 3/2,
q = 2.
```

## Reflection And Gamma Factors

Using the EC convention

```text
Lambda(E,s)=N_E^(s/2)(2 pi)^(-s) Gamma(s)L(E,s),
Lambda(E,s)=w_E Lambda(E,2-s),
```

one gets, for `s=a+iT`,

```text
1/L(E,s)
 = O_E,a( |Gamma(a+iT)/Gamma(2-a-iT)| )
   * 1/L(E,2-s).
```

Stirling gives

```text
|Gamma(a+iT)/Gamma(2-a-iT)| ~= T^(2a-2).
```

On the reflected left half `a<=1`, this is bounded or decaying, so there is no
hidden positive power loss. Conductor and `(2pi)` factors are constants in `T`.
For `eta<1`, no gamma pole is crossed on the shifted vertical range relevant to
large `T`.

The reflected point has height `-T`; for EC/newforms with real coefficients,
conjugation gives `|L(x-iT)|=|L(x+iT)|`. Thus the same selected positive height
controls both horizontal edges.

## Selected Heights And Moving Boxes

LZ gives a selected height in every large unit interval. Hence for a moving box
with `Y(u)=exp(Bu)`, choose

```text
T(u) in [Y(u), Y(u)+1].
```

The reciprocal bound is

```text
M(T(u)) <= exp(A_E log T(u)/loglog T(u)) = T(u)^o(1).
```

For the horizontal edge alone,

```text
H_horiz << exp(sigma_z u) T(u)^(-q+epsilon),
```

so with `q=2`, choosing `B > sigma_z/(2-epsilon)` kills that horizontal tail.

Caveat: this is not the full moving-box H1 condition. Original-line truncation,
vertical-line bounds, residue/PV tails, and H2/Sym2 inputs still impose their
own constraints. In particular, for the usual original-line truncation with
`q=2`, one also needs `B>sigma_z`.

## Zeros, Poles, And Losses

- The selected-height lower bound is positive uniformly on the covered strip,
  so the selected horizontal segment avoids L-zeros.
- The EC L-function is entire; there is no zeta-style pole at `s=1`.
- The central zero at `s=1` is not on high horizontal edges.
- Gamma factors in the left-half reflection are bounded or decaying in the
  recommended range, so they do not consume the `q=2` margin.
- This theorem says nothing about reciprocal residues
  `1/L'(E,1+i gamma)` or higher Laurent coefficients at multiple zeros.

## Safe HANDOFF Wording

Use:

```text
H-height(A<2) for the H1 horizontal contour tails is conditionally source-routed:
under the normalized EC/newform RH/no-right-half-zero hypothesis, Li-Zaharescu
Proposition 3.1 gives unit-spaced selected heights with reciprocal bound
exp(A_E log T/loglog T)=T^o(1). After the EC center shift and functional-equation
reflection, this controls the whole horizontal segment for
1/2<eta<1 and sigma_z<3/2. This closes only the horizontal height input, not
H1 residues/PV, multiple-zero Laurent terms, or H2/Sym2 closure.
```

Do not use:

```text
Li-Zaharescu unconditionally closes H-height(A<2) for EC H1.
```

## Bottom Line

`PASS` for the conditional horizontal-tail height mechanism.

`FAIL` for unconditional wording.

Overall status: `PARTIAL`.
