PROOF_CANDIDATE

# H2 Pointwise Theorem Package

Confidence: 0.66.

Verdict: one conditional pointwise H2 candidate is coherent for the exact
Agent 3 `P` factor, but it is not closed. The theorem depends on pointwise
`o(1)` offcentral control for both the trace and symmetric-square finite
parts. If that control is not proved, replace this package by the oscillatory
or logarithmically averaged version below.

External theorem citations: none. Ordinary Mertens/PNT, S1 explicit formula,
and symmetric-square finite-part inputs are named dependencies, not cited as
facts. Therefore no `curl + pdftotext` source packet is attached here.

## Exact Object

Fix an elliptic curve `E/Q`. Let

```text
r = ord_{s=1} L(E,s)
```

be the analytic rank. Do not replace `r` by algebraic/script rank unless a
rank-equality hypothesis is explicitly added.

For Agent 3's local inverse factor,

```text
A_p(1) = 1 - a_p/p + 1/p    if p is good,
A_p(1) = 1 - a_p/p          if p is bad.
```

The smoothed product is

```text
P_E,W(K) = product_p A_p(1)^(-W(p/K)),
log P_E,W(K) = - sum_p W(p/K) log A_p(1),
```

with the real positive log branch used by the reproducer.

The admissible `W` is the Agent 3 smoothstep class: compact support in `[0,1]`,
`W(t) -> 1` as `t -> 0+`, `W(1)=W'(1)=0`, and Mellin transform `W_hat(z)` with
residue `1` at `z=0` and enough vertical decay for the named zero sums.

## Exact Decomposition

At a good prime set

```text
lambda_p = a_p/sqrt(p),
chi_sym(p) = lambda_p^2 - 1 = a_p^2/p - 1.
```

Define

```text
S1_W(K)    = sum_{p good} W(p/K) a_p/p,
Ssym_W(K) = sum_{p good} W(p/K) chi_sym(p)/p,
Mgood_W(K)= sum_{p good} W(p/K)/p,

Rge3_W(K) = sum_{p good} W(p/K) R_p,
R_p       = -log(1 - a_p/p + 1/p)
            - a_p/p
            - (a_p^2 - 2p)/(2p^2),

Bbad_W(K) = - sum_{p bad} W(p/K) log(1 - a_p/p).
```

Then, for the exact Agent 3 factors,

```text
log P_E,W(K)
 = S1_W(K)
   + (1/2) Ssym_W(K)
   - (1/2) Mgood_W(K)
   + Rge3_W(K)
   + Bbad_W(K).
```

This identity is the load-bearing bookkeeping. Omitting `Ssym_W`, `Mgood_W`,
`Rge3_W`, or `Bbad_W` loses the exact Agent 3 product.

## Named Dependencies

`D0 Local/log convention.` The good and bad local factors above are positive
for the real branch used in `log P_E,W(K)`.

`D1 S1 branch finite part.` For some `kappa_sym` and constant `C1_E,W`,

```text
S1_W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C1_E,W
   + e1_W(K),
e1_W(K) = o(1)
```

pointwise. The allowed proof route is the S1 branch formula in which each
offcentral zero `rho=1+i gamma` contributes only

```text
K^(i gamma) W_hat(i gamma)/log K
```

and the weighted zero sum is bounded/summable.

`D2 Symmetric-square finite part.` For the same `kappa_sym`,

```text
Ssym_W(K)
 = -kappa_sym log log K
   + Csym_E,W
   + esym_W(K),
esym_W(K) = o(1)
```

pointwise, with all symmetric-square/adjoint offcentral terms either lower
order or already absorbed into `esym_W`.

`D3 Ordinary good-prime harmonic finite part.`

```text
Mgood_W(K) = log log K + CM_E,W + eM_W(K),
eM_W(K) = o(1).
```

Removing finitely many bad primes changes only `CM_E,W`.

`D4 Higher local powers.`

```text
Rge3_W(K) = Cge3_E + ege3_W(K),
ege3_W(K) = o(1),
```

where `Cge3_E = sum_{p good} R_p`. This is the absolute-convergence tail
obligation for the `m >= 3` good-prime local-log terms.

`D5 Bad primes.`

```text
Bbad_W(K) = Bbad_E + ebad_W(K),
Bbad_E    = - sum_{p bad} log(1 - a_p/p),
ebad_W(K) = o(1).
```

If `W=1` on `[0,alpha]` with `alpha>0`, this is eventually exact once
`K > max(p bad)/alpha`; otherwise it follows from `W(p/K) -> 1`.

## Pointwise H2 Candidate

Assume `D0` through `D5`. Then

```text
log P_E,W(K)
 = -r log log K + B_H2(E,W) + o(1),
```

where

```text
B_H2(E,W)
 = C1_E,W
   + (1/2) Csym_E,W
   - (1/2) CM_E,W
   + Cge3_E
   + Bbad_E.
```

Equivalently,

```text
P_E,W(K) = exp(B_H2(E,W)) (log K)^(-r) (1 + o(1)).
```

Coefficient check:

```text
(1/2 + kappa_sym/2 - r)
  + (1/2)(-kappa_sym)
  - 1/2
= -r.
```

Thus `kappa_sym` may shift mass between `S1_W` and `Ssym_W`, but cancels out of
the exact Agent 3 product coefficient.

## Proof Skeleton

1. Use the good-prime logarithm

   ```text
   -log(1 - a_p/p + 1/p)
    = a_p/p + chi_sym(p)/(2p) - 1/(2p) + R_p.
   ```

2. Sum with weight `W(p/K)` over good primes and add the finite bad-prime
   term using Agent 3's bad factor `1-a_p/p`.

3. Insert `D1` through `D5`.

4. The `log log K` coefficient is exactly `-r`; all remaining finite parts
   combine into `B_H2(E,W)`.

This proves the candidate only after the dependencies are proved. It does not
source-close S1, symmetric-square finite parts, or ordinary Mertens.

## If Offcentral Terms Persist

If `D1` or `D2` gives persistent pointwise oscillation instead of `o(1)`, the
honest pointwise statement is

```text
log P_E,W(K)
 = -r log log K
   + B_H2(E,W)
   + Z_H2(log K)
   + o(1),
```

with

```text
Z_H2(u) = Z1(u) + (1/2) Zsym(u).
```

Then the non-oscillatory pointwise theorem above is a no-go. A compatible
averaged fallback is

```text
(1/T) int_T^(2T)
  (log P_E,W(exp u) + r log u) du
  -> B_H2(E,W),
```

provided the zero series can be averaged termwise and has no noncentral
zero-frequency leakage.

## Rank And Agent 3 L2 Warning

This package concerns only Agent 3's `P` factor. The reproducer's `L2^rank`
normalization is separate and absolutely convergent at `s=2`; it does not
create the `log log K` coefficient in H2. Any later composition using
`L2^rank` must either use `r` in that exponent or assume equality between
script/algebraic rank and `ord_{s=1}L(E,s)`.

## Minimal Blocker List

- `S1_W` branch continuation and weighted zero-summability are not closed.
- `Ssym_W` finite part, with the same `kappa_sym`, is not closed.
- `Mgood_W` finite part has not been source-verified in this package.
- Persistent offcentral terms would force the oscillatory or averaged form.
- No external theorem may be cited for any dependency until verified by
  `curl + pdftotext` with a short quote and page/equation.

## Do Not Promote Unless

- The exact Agent 3 good and bad local factors remain unchanged.
- The theorem uses analytic rank `ord_{s=1}L(E,s)`.
- `S1_W`, `Ssym_W`, `Mgood_W`, `Rge3_W`, and `Bbad_W` are all present.
- Offcentral terms are proved lower-order pointwise, explicitly retained as
  `Z_H2`, or removed by a declared logarithmic average.
- The bad-prime constant uses `1-a_p/p`, not a completed local factor.
- H1 composition uses the same pointwise/oscillatory/averaged mode as H2.
- Any external theorem citation has the required source-verification packet.

## Changed File List

- `handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md`

## Commands Run

```text
pwd && sed -n '1,220p' ../start.md
./te doctor
sed -n '1,220p' token-economy.yaml
test -f L0_rules.md && sed -n '1,220p' L0_rules.md || true
test -f L1_index.md && sed -n '1,220p' L1_index.md || true
test -f ../token-economy.yaml && sed -n '1,220p' ../token-economy.yaml || true
test -x ../te && ../te doctor || true
rg --files | rg '(^HANDOFF\.md$|^L2_facts/farey-claim-ledger\.md$|handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11\.md$|H2B_ANALYTIC_PROOF_ATTEMPT\.md$|H2C_OBSTRUCTION_MAP\.md$|H2E_THEOREM_PACKAGING\.md$|handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11\.md$|handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE\.md$)'
wc -l HANDOFF.md
wc -l L2_facts/farey-claim-ledger.md
wc -l handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
wc -l handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
wc -l handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
wc -l handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
wc -l handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
ls -la handoff-2026-05-11-ec-theorem-closure-wave
sed -n '1,220p' HANDOFF.md
sed -n '1,220p' L2_facts/farey-claim-ledger.md
sed -n '1,260p' handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
sed -n '1,240p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
sed -n '1,240p' handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
sed -n '241,520p' handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
sed -n '1,220p' handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
sed -n '221,420p' handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
sed -n '1,240p' handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
sed -n '241,460p' handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
rg -n "inv_p1|log_P|A_p|P_only|L2|bad|good|smoothstep|rank" handoff-2026-05-11-gpt55-wave/AGENT3_ec_smoothed_reproducer.py
sed -n '1,220p' handoff-2026-05-11-gpt55-wave/AGENT3_EC_SMOOTHED_PROXY_SUMMARY_2026-05-11.md
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/DISPATCH_MANIFEST_2026-05-11.md
find /Users/za/Documents/Farey\ NOW -name H2_POINTWISE_THEOREM_PACKAGE.md -print
mv /Users/za/Documents/Farey\ NOW/handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md /Users/za/Documents/Farey\ NOW/primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
rmdir /Users/za/Documents/Farey\ NOW/handoff-2026-05-11-ec-theorem-closure-wave
find /Users/za/Documents/Farey\ NOW/handoff-2026-05-11-ec-theorem-closure-wave -maxdepth 2 -type f -print
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
wc -l handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
git diff -- handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '261,340p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
```
