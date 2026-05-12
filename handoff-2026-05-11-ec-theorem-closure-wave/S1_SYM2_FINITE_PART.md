RIGOROUS_REDUCTION

# S1 Sym2 Finite-Part Companion

confidence: 0.76

No external theorem is cited as fact in this report. Therefore no
`curl + pdftotext` theorem quote is embedded. The output below is an in-repo
conditional finite-part theorem: the local algebra and constant structure are
proved from the stated Euler product convention; the analytic continuation,
central order, and zero-summability package remain dependencies.

## Dependencies

- Fixed elliptic curve `E/Q`; analytic rank only:
  `r = ord_{s=1} L(E,s)`.
- Agent 3 local factors:
  good `A_p(1)=1-a_p/p+1/p`, bad `A_p(1)=1-a_p/p`.
- Good-prime normalized Satake convention: choose `u_p v_p=1` and
  `u_p+v_p=lambda_p=a_p/sqrt(p)`.
- Admissible kernel `W`: compact support in `[0,1]`, `W(0)=1`,
  Mellin transform `W_hat(z)=1/z+O(1)` at `z=0`, and vertical decay strong
  enough for the stated contour shifts.
- Symmetric-square/adjoint branch package for the exact good-prime object:
  logarithmic continuation near `s=1`, central order `kappa_sym`, and the
  offcentral zero/pole summability stated below.

## Exact Local Convention

For good primes define

```text
lambda_p = a_p/sqrt(p),
chi_sym2(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Then

```text
S_sym,W(K) = sum_{p good} W(p/K) chi_sym2(p)/p.
```

Bad primes are not part of `S_sym,W`. They stay in the finite Agent 3 product
constant

```text
B_bad,E = - sum_{p bad} log(1-a_p/p),
```

with the same positive-real branch convention as the reproducer. If a future
proof uses a global ramified symmetric-square factor, its ramified local logs
must first be removed to return to this good-prime convention.

## Good-Prime Sym2 Object

Define the good-prime adjoint/symmetric-square Euler product by

```text
L_sym,E^good(s)
 = product_{p good}
   (1-u_p^2 p^(-s))^(-1)
   (1-p^(-s))^(-1)
   (1-v_p^2 p^(-s))^(-1).
```

Its first logarithmic prime coefficient is exactly `chi_sym2(p)`. For
`Re(s)>1`,

```text
log L_sym,E^good(s)
 = D_sym,E(s) + H_sym,E(s),

D_sym,E(s) = sum_{p good} chi_sym2(p) p^(-s),

H_sym,E(s)
 = sum_{p good} sum_{m>=2}
   (u_p^(2m) + 1 + v_p^(2m))/(m p^(ms)).
```

The stated Satake-size convention makes `H_sym,E(s)` absolutely convergent at
`s=1`. Thus all non-absolutely-convergent structure in `D_sym,E` comes from
`log L_sym,E^good`.

Let

```text
kappa_sym = ord_{s=1} L_sym,E^good(s),
L_sym,E^*(1) = lim_{s -> 1+} (s-1)^(-kappa_sym) L_sym,E^good(s).
```

Use positive `kappa_sym` for a zero and negative `kappa_sym` for a pole. Along
the real side `s>1`,

```text
log L_sym,E^good(s)
 = kappa_sym log(s-1) + log L_sym,E^*(1) + o(1).
```

Therefore

```text
D_sym,E(s)
 = kappa_sym log(s-1)
   + d_sym,E
   + o(1),

d_sym,E = log L_sym,E^*(1) - H_sym,E(1).
```

Do not set `kappa_sym=0` unless this exact good-prime object has a verified
finite nonzero value at `s=1`.

## Central Finite Part

Mellin inversion gives

```text
S_sym,W(K)
 = (1/(2 pi i)) int_(c)
   K^z W_hat(z) D_sym,E(1+z) dz.
```

The central branch contribution is universal:

```text
(1/(2 pi i)) int_(c) K^z W_hat(z) log z dz
 = -log log K - gamma_E + O_W(1/log K),
```

because `W_hat(z)=1/z+O(1)` at `z=0`. Hence the central finite part is

```text
S_sym,W(K)
 = -kappa_sym log log K
   + C_sym,E
   + Z_sym,E,W(K)
   + o(1),

C_sym,E = d_sym,E - kappa_sym gamma_E
        = log L_sym,E^*(1) - H_sym,E(1) - kappa_sym gamma_E.
```

For the Agent 3 smoothstep class, the central constant is independent of the
transition parameter `alpha`; the transition changes lower-order terms and the
offcentral weights `W_hat(rho-1)`, not the displayed finite part. Keeping the
name `C_sym,E,W` is harmless, but the exact central formula above has no hidden
kernel constant.

## Offcentral Terms

Let `rho != 1` range over zeros or poles of `L_sym,E^good` in the shifted
strip reached by the contour, and let

```text
m_rho = ord_{s=rho} L_sym,E^good(s),
z_rho = rho - 1.
```

Locally,

```text
D_sym,E(1+z) = m_rho log(z-z_rho) + holomorphic.
```

Crossing that logarithmic branch gives the leading term

```text
Z_sym,E,W(K)
 = - (1/log K) sum_{rho != 1}
     m_rho K^(rho-1) W_hat(rho-1)
   + O(E_sym,W(K)),
```

where a sufficient error condition is

```text
E_sym,W(K) << (1/(log K)^2)
  sum_{rho != 1} |m_rho| K^(Re rho - 1)
  (|W_hat(rho-1)| + |W_hat'(rho-1)|)
  + K^(-delta)
```

with the displayed sum finite uniformly in `K`. Consequences:

- If all offcentral singularities have `Re(rho)<=1` and the weighted sum is
  finite, then `Z_sym,E,W(K)=O(1/log K)=o(1)`.
- A singularity on `Re(rho)=1`, `rho != 1`, gives
  `-m_rho K^(i Im rho) W_hat(i Im rho)/log K`, not a persistent
  constant-size oscillation.
- A singularity with `Re(rho)>1` gives `K^(Re rho-1)/log K`; the pointwise
  finite-part theorem is false unless another explicitly identified term
  cancels it.

Thus the symmetric-square companion does not create an extra H2-scale
oscillation once the branch formula and zero sum are proved. The only
`log log K` coefficient is `-kappa_sym`.

## H2 Compatibility

The repaired H2 decomposition is

```text
log P_E,W(K)
 = S_1,W(K)
   + (1/2) S_sym,W(K)
   - (1/2) M_good,W(K)
   + R_ge3,W(K)
   + B_bad,E.
```

The compatible S1 coefficient must be

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + Z_1,E,W(K)
   + o(1).
```

Together with

```text
S_sym,W(K) = -kappa_sym log log K + C_sym,E + Z_sym,E,W(K) + o(1),
M_good,W(K) = log log K + C_M,E,W^good + o(1),
```

the H2 coefficient is exactly

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

The finite product constant is

```text
B_E,W =
  C_1,E,W
  + (1/2) C_sym,E
  - (1/2) C_M,E,W^good
  + C_ge3,E
  + B_bad,E.
```

The pointwise H2-limit follows only when both `Z_1,E,W(K)` and
`Z_sym,E,W(K)` are `o(1)`. If S1 retains an almost-periodic remainder, this
Sym2 term does not cancel it; H2 must then be stated in oscillatory or averaged
form.

## Refutation Boundaries

Refuted: the naive statement

```text
S_sym,W(K) = C + o(1)
```

without first proving `kappa_sym=0` for the exact Agent 3 good-prime object.
The correct central term is `-kappa_sym log log K`.

Also refuted: any pointwise finite-part theorem allowing an uncancelled
offcentral zero/pole with `Re(rho)>1`, or dropping the branch sum without the
weighted zero-summability hypothesis.

Not refuted: the expected Agent 3 case `kappa_sym=0` with
`Z_sym,E,W(K)=O(1/log K)`. That is a valid proof target once the analytic
package is source-verified or proved in-repo.

## Do Not Promote Unless

- The object is `L_sym,E^good` above, or all ramified/global local-factor
  differences are written as finite corrections.
- `kappa_sym = ord_{s=1} L_sym,E^good(s)` is stated before claiming constant
  scale.
- Any claim `kappa_sym=0` is verified for the exact shifted adjoint/Sym2
  normalization with first coefficient `a_p^2/p - 1`.
- The offcentral branch formula is proved, including the `1/log K` factor.
- The weighted zero/pole sum is proved finite, or `Z_sym,E,W(K)` is retained.
- H2 uses analytic rank `ord_{s=1}L(E,s)`, not script/algebraic rank unless
  equality is separately assumed or verified.
- The final H2 package also includes `S_1,W`, `M_good,W`, `R_ge3`, and
  Agent 3 bad-prime constants.
- Any external theorem used later is `curl + pdftotext` verified with a short
  quote and page/equation.

## Changed File List

- `handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`

## Commands Run

- `sed -n '1,220p' ../start.md`
- `./te doctor` attempted in workspace; failed because `./te` is absent there.
- `sed -n '1,180p' ../token-economy.yaml`
- `sed -n '1,220p' L0_rules.md`
- `sed -n '1,260p' L1_index.md`
- `wc -l` on required H2/S1 context files.
- `rg -n` for `sym`, `S_sym`, `finite`, `H2`, `kappa`, `local`, `rank`.
- `sed -n` reads of `HANDOFF.md`, `L2_facts/farey-claim-ledger.md`,
  `H2_SPRINT_SYNTHESIS_2026-05-11.md`, `H2B_ANALYTIC_PROOF_ATTEMPT.md`,
  `H2E_THEOREM_PACKAGING.md`, `S1F_SYM2_COMPANION_TERM.md`,
  `DISPATCH_MANIFEST_2026-05-11.md`.
- `rg -n` and `sed -n` reads of
  `handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py`.
- `git status --short`
- `git diff --name-only -- handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md`
- `find .. -path '*handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md' -print`
- `mv ../handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md`
- `sed -n` verification reads of this deliverable.
- `LC_ALL=C rg -n "[^\\x00-\\x7F]" handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md || true`
