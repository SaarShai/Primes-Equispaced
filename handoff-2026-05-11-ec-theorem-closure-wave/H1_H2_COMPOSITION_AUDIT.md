RIGOROUS_REDUCTION

# H1/H2 Composition Audit

Confidence: 0.76.

Verdict: partial compatibility. H1 can use the same smoothing kernel `W` as H2,
but not the same offcentral-zero mechanism. H2's repaired pointwise route is
logarithmic-branch calculus, where a zero `rho=1+i gamma` contributes
`K^(i gamma) W_hat(i gamma)/log K`. H1's reciprocal Perron side is pole
calculus: the same zero contributes a residue with no `1/log K` loss. Therefore
H1 cannot share the H2 pointwise theorem scaffold verbatim.

For positive analytic rank `r>=1`, H1 can still be compatible with a final
pointwise fixed-curve theorem if its pole-residue aggregate is lower than the
central `u^r` scale, `u=log K`. For rank zero, or for high-multiplicity
offcentral reciprocal zeros at the central scale, H1 must be stated as
oscillatory or averaged unless an extra cancellation theorem is proved.

No external theorem is cited in this audit. No cross-curve universality or BSD evidence
is promoted.

## Objects Under Comparison

Use the same admissible compact smoothing kernel as H2:

```text
W_hat(z) = integral_0^infty W(t)t^(z-1)dt,
W_hat(z) = 1/z + holomorphic at z=0,
W_hat(sigma+i tau) = O((1+|tau|)^-2)
```

away from `z=0` on fixed strips, for the smoothstep class in T1/H2E.

H1:

```text
c_E,W(K) = sum_n mu_E(n)/n W(n/K)
         = (1/2 pi i) integral_(sigma)
             K^z W_hat(z) / L(E,1+z) dz.
```

H2 pointwise limit target:

```text
P_E,W(K) = exp(B_E,W) (log K)^(-r) (1+o(1)),
r = ord_{s=1} L(E,s).
```

The desired product target is fixed-curve only:

```text
c_E,W(K) P_E,W(K) -> exp(B_E,W) / L^(r)(E,1).
```

## Precise Mismatch

Let `u=log K`, and let `rho=1+i gamma`, `gamma != 0`, be an offcentral zero of
`L(E,s)`.

In H2/S1, the prime-linear Dirichlet series has a logarithmic branch near
`z=i gamma`:

```text
A_E(z) = c_gamma log(1/(z-i gamma)) + holomorphic.
```

Since `W_hat` is holomorphic at `i gamma`, the branch-cut integral gives

```text
c_gamma K^(i gamma) W_hat(i gamma) / u + O(u^-2).
```

This is the repaired H2 mechanism: fixed offcentral zeros on `Re(s)=1` become
lower order after the log-prime weight is integrated away.

In H1, the integrand contains `1/L(E,1+z)`. If the same zero has multiplicity
`m`, then near `z0=i gamma`,

```text
1/L(E,1+z) = sum_{j=1}^m b_{-j}(z-z0)^(-j) + holomorphic.
```

The Perron integrand has a pole, not a logarithmic branch. Its residue is

```text
K^(i gamma) times a polynomial in u of degree m-1,
```

with coefficients built from `b_{-j}` and derivatives of `W_hat` at
`i gamma`. For a simple zero:

```text
Res = K^(i gamma) W_hat(i gamma) / L'(rho).
```

There is no `1/u` damping. Smoothstep helps by damping high `|gamma|` through
`W_hat(i gamma)`, but it does not remove fixed low-zero oscillations, control
`1/L'(rho)`, or suppress multiplicity powers of `u`.

## Pointwise Compatibility Test

Let the H1 expansion have the form

```text
c_E,W(e^u) = Q_r(u) + Z_c(u) + E_c(u),
Q_r(u) = u^r/L^(r)(E,1) + lower central powers,
```

where `Z_c` is the offcentral reciprocal-zero pole sum. If H2-limit is proved,
then

```text
c_E,W(e^u) P_E,W(e^u)
 = exp(B_E,W) u^(-r) (Q_r(u)+Z_c(u)+E_c(u))(1+o(1)).
```

Thus pointwise product convergence follows from the weaker H1 condition

```text
Z_c(u)+E_c(u) = o(u^r).
```

H1 does not need its offcentral residue sum to be `o(1)` for positive rank.
Bounded simple-zero oscillations are harmless after multiplication by
`u^(-r)` when `r>=1`. This is weaker than T1's rank-1 `o(1)` H1 remainder and
is enough for the final fixed-curve limit, though not for a sharper expansion
of `c_E,W` itself.

Failure cases:

```text
r=0:
  simple offcentral H1 residues are constant scale, so pointwise cP has an
  almost-periodic term unless Z_c(u)=o(1).

m >= r+1:
  an offcentral zero of multiplicity m contributes u^(m-1) e^(i gamma u);
  after H2 multiplication this is at least constant scale when m-1>=r.

non-summable reciprocal residues:
  even simple zeros can fail pointwise control if
  sum |W_hat(i gamma)/L'(rho)| or an equivalent contour/mean-square substitute
  is not controlled.
```

## Theorem Mode Verdict

`H2-limit` plus positive-rank `H1-leading` is compatible pointwise:

```text
r>=1,
H2: log P_E,W(K) = -r log log K + B_E,W + o(1),
H1: c_E,W(K) = (log K)^r/L^(r)(E,1) + o((log K)^r),
```

with all lower central powers and harmless oscillatory terms included in the
`o((log K)^r)` condition. This gives pointwise fixed-curve stabilization.

`H1` cannot use the H2 branch scaffold:

```text
H2 offcentral zero: logarithmic branch -> K^(i gamma) W_hat(i gamma)/log K.
H1 offcentral zero: reciprocal pole -> K^(i gamma) W_hat(i gamma)/L'(rho).
```

So the pointwise package must contain a separate H1 pole-residue theorem, not a
copy of the H2 S1 theorem.

`H1-osc` is mandatory when the normalized residue aggregate is not `o(u^r)`:

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_E,W)u^(-r)(Q_r(u)+Z_c(u)) + o(1)
```

with `Z_c` retained. This is the honest form for rank zero unless a stronger
cancellation theorem is proved.

`H1-avg` is only compatible with an averaged final theorem. If H2 is weakened
to a log-average statement for `log P`, the result is at most a geometric/log
finite-part theorem unless a separate arithmetic average of `c_E,W P_E,W` and
its H1/H2 zero correlations is proved.

## Dependencies

1. Same kernel and scale: H1 and H2 must use the identical `W(p/K)` /
   `W(n/K)` convention and the same Mellin transform normalization.
2. Analytic rank first: `r=ord_{s=1}L(E,s)`. Script/algebraic rank requires an
   explicit equality input.
3. H2-limit closure: S1 branch-only theorem, zero-summability, symmetric-square
   finite part, ordinary weighted prime-Mertens finite part, bad-prime
   constants, and contour tails.
4. H1 pole closure: central residue polynomial, offcentral reciprocal Laurent
   residues, multiple-zero powers, reciprocal derivative growth, and contour
   tails.
5. Positive-rank pointwise composition: prove `Z_c(u)+E_c(u)=o(u^r)`.
6. Rank-zero composition: prove `Z_c(u)=o(1)`, retain `Z_c` explicitly, or
   weaken the final claim to a declared averaged theorem.
7. Full proxy only: add T1 `H3` for the absolutely convergent `L2` factor; this
   does not repair H1/H2 mode mismatches.

## Do Not Promote Unless

- H2 is closed in the exact Agent 3 local-factor convention, with
  `S_1,W`, `S_sym,W`, `M_good,W`, bad-prime constants, and analytic rank.
- H1 is closed separately as a reciprocal-pole theorem; do not import the H2
  `1/log K` branch damping onto `1/L(E,1+z)`.
- The H1 reciprocal-zero aggregate is proved `o((log K)^r)` for positive rank,
  or retained explicitly as an oscillatory term.
- Rank zero is separated. A bounded H1 zero sum is not enough for a pointwise
  limit when `r=0`.
- Multiple offcentral zeros are handled. Any multiplicity `m>=r+1` must be
  ruled out, shown cancelling, retained oscillatory, or averaged.
- The theorem mode is declared once and used throughout: pointwise limit,
  pointwise oscillatory expansion, log/geometric average, or arithmetic average.
- No averaged theorem for `log P` is used to claim ordinary stabilization of
  `c_E,W P_E,W` without a joint arithmetic/correlation theorem.
- Every future external theorem citation follows the required
  `curl + pdftotext + verbatim quote + page/equation` protocol.
- No cross-curve universality, BSD evidence, or cross-curve constant claim is promoted.

## Changed File List

- `handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md`

## Commands Run

```bash
pwd && rg --files -g 'start.md' -g 'HANDOFF.md' -g 'L2_facts/farey-claim-ledger.md' -g 'EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md' -g 'T1_SMOOTHED_PERRON_THEOREM.md' -g 'S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md' -g 'H2_SPRINT_SYNTHESIS_2026-05-11.md'
sed -n '1,220p' ../start.md
sed -n '1,240p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,260p' L1_index.md
sed -n '1,260p' handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
sed -n '1,520p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '1,300p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
sed -n '1,320p' handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
rg -n "H1|H2|pointwise|averag|oscill|offcentral|zero|W_hat|Mellin|reciprocal|Perron" handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
ls -la handoff-2026-05-11-ec-theorem-closure-wave
find handoff-2026-05-11-ec-theorem-closure-wave -maxdepth 1 -type f -print
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/DISPATCH_MANIFEST_2026-05-11.md
sed -n '1,620p' handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
sed -n '1,620p' handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
sed -n '1,620p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
sed -n '1,360p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
sed -n '1,360p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
sed -n '1,330p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1C_ZERO_TERM_ANALYSIS.md
rg -n "1/L|reciprocal|Perron|L'\\(|offcentral|multiple|multiplicity|rank zero|averag|oscill" handoff-2026-05-09-followup handoff-2026-05-11-gpt55-wave handoff-2026-05-11-ec-smoothing-blockers handoff-2026-05-11-ec-h2-mertens-sprint handoff-2026-05-11-ec-s1-explicit-formula-sprint
git status --short
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
tail -n 90 handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
git diff -- handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
find '/Users/za/Documents/Farey NOW' -path '*H1_H2_COMPOSITION_AUDIT.md' -print
pwd; ls -la; ls -la handoff-2026-05-11-ec-theorem-closure-wave 2>/dev/null || true; ls -la '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave' 2>/dev/null || true
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md' '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md'
sed -n '1,40p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
tail -n 70 handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
find '/Users/za/Documents/Farey NOW' -path '*H1_H2_COMPOSITION_AUDIT.md' -print
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
head -n 5 handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
rg -n "^Confidence:|^## Dependencies|^## Do Not Promote Unless|^## Changed File List|^## Commands Run|No external theorem" handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```

Bootstrap note: `./te doctor` and `token-economy.yaml` were absent from the
specified workspace, so the audit proceeded from `../start.md`, local
`L0_rules.md`/`L1_index.md`, and the required handoff files. No `curl` or
`pdftotext` command was run because no external theorem is cited.
