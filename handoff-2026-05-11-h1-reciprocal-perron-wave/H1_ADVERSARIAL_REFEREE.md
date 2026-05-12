NO_GO

# H1 Adversarial Referee: Reciprocal Perron Route

Confidence: 0.89 for no theorem promotion; 0.80 that H1 remains a coherent
conditional target only after the dependencies below are stated explicitly.

External theorem citations: none. This report uses only repo-local wave files
and source audits. No new `curl`/`pdftotext` packet is attached.

Scope: adversarial review of the H1 reciprocal Perron route for the EC
smoothed fixed-curve stabilization program. The target H1 wave directory was
not present before this file was created, so this report stands independently
from the EC theorem-closure wave plus the H1/H2 audit.

## Executive Verdict

Do not promote H1. Do not promote the EC smoothing theorem. Do not promote EC
universality, BSD evidence, or an `L(E,2)^rank` normalization.

The H1 route is still blocked at the exact place where the closure wave says it
is blocked: offcentral zeros of `L(E,s)` become poles of `1/L(E,1+z)`. They are
not logarithmic branches. Therefore H1 does not inherit the H2/S1
`1/log K` damping. Smoothing improves high-frequency Mellin decay, but it does
not control low offcentral residues, reciprocal zero derivatives, multiple-zero
Laurent coefficients, or rank-zero main-scale oscillation.

Allowed guarded reduction:

```text
For fixed E and fixed W, a pointwise fixed-curve limit for
c_E,W(K) P_E,W(K) follows if:

H1 proves c_E,W(K) = Q_r(log K) + o((log K)^r),
H2 proves P_E,W(K) = exp(B_E,W)(log K)^(-r)(1+o(1)),
r = ord_{s=1}L(E,s),
and rank zero/multiple-zero cases are handled in the same theorem mode.
```

Current status: none of the load-bearing H1 hypotheses are closed.

## Object Under Audit

The H1 object is

```text
c_E,W(K) = sum_n mu_E(n)/n W(n/K)
         = (1/(2 pi i)) integral_(sigma)
             K^z W_hat(z) / L(E,1+z) dz.
```

If

```text
L(E,1+z) = (L^(r)(E,1)/r!) z^r (1 + O(z)),
r = ord_{s=1}L(E,s),
```

then the central residue from `W_hat(z)=1/z+O(1)` is a degree-`r` polynomial
`Q_r(u)`, `u=log K`, with leading term

```text
u^r / L^(r)(E,1).
```

This local central algebra is not the problem. The problem is the global
contour shift and the residues away from `z=0`.

## Fatal Blockers

1. H1 is pole calculus, not H2 branch calculus.

For an offcentral zero `rho=1+i gamma`, `gamma != 0`, with multiplicity `m`,
H1 has a Laurent expansion

```text
1/L(E,1+z) = sum_{j=1}^m b_{-j}(z-i gamma)^(-j) + holomorphic.
```

The residue of

```text
K^z W_hat(z) / L(E,1+z)
```

is

```text
K^(i gamma) times a polynomial in u=log K of degree m-1.
```

For a simple zero it is

```text
K^(i gamma) W_hat(i gamma) / L'(rho).
```

There is no `1/u` loss. The H2/S1 branch theorem has
`K^(i gamma) W_hat(i gamma)/u` because a logarithmic branch cut gives a Laplace
integral. H1 has reciprocal poles. Importing H2 damping into H1 is a fatal
false analogy.

2. Reciprocal derivative bounds are completely missing.

The S1 zero-counting input controls pure multiplicity sums such as

```text
sum_gamma m_gamma |W_hat(i gamma)|.
```

H1 needs at least

```text
sum_gamma |W_hat(i gamma)/L'(1+i gamma)|
```

for simple zeros, or a contour/mean-square substitute strong enough to imply
`Z_c(u)=o(u^r)`. For multiple zeros it needs summability of higher Laurent
coefficients `b_{-j}`, plus `W_hat` derivatives at the zeros. The source packet
explicitly says Sheth-style zero counting is not reciprocal derivative control.

3. Multiple offcentral zeros can survive normalization.

An offcentral zero of multiplicity `m` contributes `u^(m-1) e^(i gamma u)`.
After multiplying by the H2 factor `u^(-r)`, it contributes

```text
u^(m-1-r) e^(i gamma u).
```

Consequences:

```text
m <= r:       lower order if the aggregate is controlled.
m = r+1:     constant-scale oscillation remains.
m > r+1:     normalized product grows along H1 unless cancelled or retained.
```

No current file rules out `m >= r+1`, proves cancellation, or supplies Laurent
coefficient bounds for multiple zeros. A theorem that assumes all offcentral
zeros are simple must say so and still handle `1/L'(rho)`.

4. Rank zero is not a corollary of positive rank.

For `r=0`, the central H1 term is constant scale:

```text
Q_0 = 1/L(E,1) + lower kernel/Taylor constants.
```

A simple offcentral H1 residue is also constant scale. Thus even a bounded
absolutely convergent residue series gives an almost-periodic correction, not
a pointwise limit. Rank-zero H1 needs one of:

```text
Z_c(u)=o(1) pointwise,
an explicit oscillatory expansion,
or a declared averaged theorem for the final product itself.
```

The current reduction does not close any of these.

5. The contour shift is not sourced or proved.

H1 needs a meromorphic contour shift for `1/L(E,1+z)` with infinitely many
poles, not just formal residue extraction. Missing pieces:

```text
vertical-line bounds for 1/L(E,1+z),
horizontal truncation bounds,
small-circle/local-radius control around zeros,
absolute or conditional convergence of the residue aggregate,
control of zeros off Re(s)=1 or an explicit RH-type hypothesis,
kernel derivative decay to the order required by multiplicities,
left-edge decay after crossing the pole set.
```

The source packet labels reciprocal Perron H1 as `LITERATURE_BLOCKED`. Standard
Perron/Mellin background does not close this exact smoothstep theorem.

6. H2 closure would not close H1.

The EC closure wave made H2 more coherent, but H2 remains conditional and uses
different singularity calculus. Even if the S1 branch theorem and Sym2 finite
part were proved tomorrow, H1 would still need its own reciprocal-pole theorem.
The composition audit is right: H1 and H2 can share `W`, but not the mechanism.

7. Averaging is being used too cheaply.

An averaged statement for `log P_E,W` does not imply pointwise stabilization of
`c_E,W P_E,W`. It also does not imply an arithmetic average of the product.
To average the final theorem, one must prove the averaged expansion for

```text
c_E,W(e^u) P_E,W(e^u)
```

or prove compatible H1/H2 oscillatory expansions plus termwise averaging and
zero-frequency/correlation control. Products of H1 residues and H2 terms can
create frequency collisions. Averaging logs and then exponentiating is not a
valid substitute.

## Rank And Normalization Hazards

- Use analytic rank:

  ```text
  r = ord_{s=1}L(E,s).
  ```

  Script rank or algebraic rank may enter only under an explicit equality
  hypothesis or per-curve analytic verification.

- The leading H1 central coefficient is `1/L^(r)(E,1)`, not an unspecified
  BSD constant and not `r!/L^(r)(E,1)` after residue extraction.

- H1 and H2 must use the same `W` and scale convention. Mixing `W(n/K)`,
  `W(p/K)`, hard cutoff, endpoint taper, or Mellin normalizations changes
  constants and residue weights.

- The final fixed-curve constant is curve-dependent. Nothing here implies
  cross-curve universality.

- `L2_E,W(K)^rank` is absolutely convergent at `s=2` and is not the source of
  the H1/H2 central cancellation. It must not be described as load-bearing
  without a separate theorem and ablation evidence.

- Bad-prime and good-prime local factors must stay in the exact Agent-3
  convention if this is composed with the H2 package.

## What A Valid H1 Theorem Must Contain

For `u=log K`, a pointwise positive-rank theorem must prove

```text
c_E,W(e^u) = Q_r(u) + Z_c(u) + E_c(u),
Z_c(u)+E_c(u)=o(u^r),
```

where `Q_r` is the full central polynomial and `Z_c` is the offcentral
reciprocal-pole sum. A stronger theorem may prove `Z_c=O(1)` under simple zeros
and derivative summability; this is enough only for `r>=1`, not for rank zero.

For rank zero, the theorem must instead prove

```text
Z_c(u)=o(1)
```

or retain `Z_c(u)` explicitly or average the final product.

For multiple zeros, the theorem must state and prove bounds for

```text
sum_{rho,m,j} |b_{-j}(rho) W_hat^(ell)(rho-1)|
```

in the form actually needed by the residue polynomial. Pure zero counting is
not enough.

## Source Gaps

Repo-local source status is negative for H1:

- `SOURCE_PACKET.md`: exact fixed-curve endpoint-smoothed S1/H2/H1 theorem is
  `LITERATURE_BLOCKED`.
- The only narrow closed zero input is pure multiplicity zero counting with
  smooth `W_hat` decay.
- Reciprocal-zero derivative/summability for H1 is not sourced.
- Standard Perron background is only background; the exact smoothstep contour
  shift remains an in-repo proof obligation.
- Kuo-Murty/Conrad/Sheth are obstruction or adjacent sources, not H1 closure.

Any future external theorem used to close H1 must follow the project protocol:
`curl`, `pdftotext`, short quote, page/equation, and exact statement matching
the endpoint-smoothed reciprocal object.

## Numerics Do Not Repair H1

The finite three-curve smoothstep pass and the dense S1 diagnostics are
audit-only. Ablations already show that `cP_only`, `P_only`, and `PL2_only`
can pass old finite gates. This supports endpoint/product-shell damping as a
finite-window explanation. It does not prove reciprocal-pole cancellation,
`1/L'(rho)` summability, rank-zero stabilization, or any BSD/universality
claim.

## Dependencies

To change this verdict, close all of the following in one declared theorem
mode.

1. H1 Mellin/Perron theorem for the exact smoothstep `W`, including contour
   shift, residue enumeration, tails, and central polynomial `Q_r`.
2. Reciprocal derivative/Laurent coefficient control for all offcentral zeros
   encountered by the shift.
3. Multiple-zero handling: rule out, bound, retain, or average every
   polynomial residue term.
4. Rank-zero theorem: pointwise cancellation, explicit oscillatory expansion,
   or final-product average.
5. RH/zero-location hypothesis or an unconditional treatment of zeros with
   `Re(rho) != 1`.
6. H2 package in the exact Agent-3 local-factor normalization and the same
   pointwise/oscillatory/averaged mode.
7. Analytic-rank convention, with no silent script/algebraic rank substitution.
8. Source packets for every outside theorem used.

## Do Not Promote Unless

- H1 is closed separately as a reciprocal-pole theorem.
- No H2 `1/log K` branch damping is transferred to H1.
- `Z_c(u)+E_c(u)=o(u^r)` is proved for positive analytic rank, or `Z_c` is
  retained explicitly.
- Rank zero is separated.
- Multiple offcentral zeros are ruled out, controlled, retained, or averaged.
- Reciprocal derivative/Laurent coefficient bounds are proved or sourced.
- The theorem mode is declared once: pointwise, oscillatory, log-average, or
  arithmetic average of the final product.
- An averaged `log P` statement is not used to claim pointwise or product
  stabilization.
- H2 is closed with exact local factors before any composition theorem.
- No cross-curve universality, BSD evidence, cross-curve constant, or `L(E,2)^rank`
  normalization is promoted from this route.

## Changed Files

```text
handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
```

## Commands Run

```bash
pwd && rg --files -g 'start.md' -g 'HANDOFF.md' -g 'L2_facts/farey-claim-ledger.md' -g 'handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md' -g 'H1_H2_COMPOSITION_AUDIT.md' -g 'ADVERSARIAL_REFEREE.md'
ls -la
find handoff-2026-05-11-h1-reciprocal-perron-wave -maxdepth 2 -type f -print | sort
sed -n '1,220p' ../start.md
sed -n '1,260p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,260p' L1_index.md
ls -la ../te ../token-economy.yaml
find .. -maxdepth 2 -name token-economy.yaml -o -name te
../te doctor
sed -n '1,220p' ../token-economy.yaml
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,340p' handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
sed -n '1,340p' handoff-2026-05-11-ec-theorem-closure-wave/S1_SYM2_FINITE_PART.md
rg -n "H1|reciprocal|Perron|1/L|L'|multiple|multiplicity|rank zero|averag|oscill|derivative|Laurent|offcentral|pole" handoff-2026-05-11-ec-theorem-closure-wave handoff-2026-05-11-ec-smoothing-blockers handoff-2026-05-11-ec-h2-mertens-sprint handoff-2026-05-11-ec-s1-explicit-formula-sprint handoff-2026-05-09-followup handoff-2026-05-11-gpt55-wave
sed -n '1,340p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '1,240p' handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
sed -n '1,380p' handoff-2026-05-11-ec-h2-mertens-sprint/H2C_OBSTRUCTION_MAP.md
sed -n '1,240p' handoff-2026-05-11-ec-h2-mertens-sprint/H2_SPRINT_SYNTHESIS_2026-05-11.md
sed -n '340,520p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
mkdir -p handoff-2026-05-11-h1-reciprocal-perron-wave
sed -n '1,80p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
tail -n 90 handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
rg -n "^NO_GO$|^Confidence:|^## Dependencies$|^## Do Not Promote Unless$|^## Changed Files$|^## Commands Run$|cross-curve universality|BSD|H2|rank zero|multiple|derivative|Laurent|averag|source" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
LC_ALL=C rg -n "[^\x00-\x7F]" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
wc -l handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md
git diff --name-only -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_ADVERSARIAL_REFEREE.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
git status --short
```

Bootstrap note: `./te doctor` and project-local `token-economy.yaml` were
absent in the specified workspace. `../te doctor` ran and reported missing
project-local bootstrap files while identifying the repo root correctly. The
review proceeded from `../start.md`, `../token-economy.yaml`, local
`L0_rules.md`/`L1_index.md`, and the required handoff files.
