PROOF_CANDIDATE

# S1 Zero-Summability And Contour Closure

confidence: `0.78`

dependencies:
- local context: `HANDOFF.md`, `L2_facts/farey-claim-ledger.md`, `S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md`, `S1A_EXPLICIT_FORMULA_DERIVATION.md`, `S1B_SOURCE_AUDIT.md`, `S1C_ZERO_TERM_ANALYSIS.md`, `S1D_AVERAGED_FALLBACK.md`.
- analytic hypotheses below: `W2`, `ZC`, `BC`.
- no external theorem is cited as fact in this note. Zero counting is an explicit hypothesis, not a sourced theorem.

## Verdict

The weighted offcentral zero sum needed by smoothed `S_1,W` closes for the
smoothstep/admissible `C^1` endpoint kernels, provided the zero count is the
standard `T log T` size counted with multiplicity and the branch-only contour
decomposition from S1-A/S1-C is available:

```text
sum_{gamma != 0} |m_gamma W_hat(i gamma)| < infinity.
```

Consequently the offcentral logarithmic-branch aggregate is pointwise lower
order:

```text
-(1/log K) sum_{gamma != 0} m_gamma K^(i gamma) W_hat(i gamma)
  = O_W,E(1/log K).
```

This closes the zero-summability part of the S1 route as a conditional proof
candidate. It does not close source/branch continuation or the symmetric-square
companion.

## Hypotheses

Let `u=log K`. Let `A_E(z)=sum_p a_p p^(-1-z)` initially in its convergence
half-plane.

`W2` kernel decay:
`W` is compactly supported in `[0,1]`, is `C^1` and piecewise `C^2`, has
`W(0)=1` and `W'(0+)=W'(1-)=0` in the relevant endpoint sense, and its Mellin
transform satisfies, on `-eta <= sigma <= c` away from `z=0`,

```text
|W_hat^(j)(sigma+i t)| <= C_j (1+|t|)^(-2),  j=0,1.
```

The Agent 3 smoothstep satisfies this: two integrations by parts give

```text
W_hat(s)=1/(s(s+1)) integral W''(t)t^(s+1)dt
```

on the shifted strip, excluding the central pole at `s=0` and any kernel poles
left of the chosen strip. For `alpha=0`, the extra smoothstep poles at `-2,-3`
are avoided by taking `0<eta<2`.

`ZC` zero counting:
for noncentral zeros `rho=1+i gamma` relevant to `A_E`, counted with
multiplicity `m_gamma`,

```text
N_E(T) := sum_{0<|gamma|<=T} m_gamma
       <= C_E T log(C_E(T+3)).
```

`BC` branch-contour control:
in `-eta <= Re z <= c`, `A_E(z)` has only the central logarithmic branch at
`0`, noncentral logarithmic branches at `z=i gamma`, and a regular remainder
whose product with `K^z W_hat(z)` is integrable on the shifted boundary.
There are no offcentral poles on `Re z >= -eta`. Branch cuts are taken leftward
from each `i gamma`.

## Zero-Sum Proof

The finitely many zeros with `0<|gamma|<1` are harmless. Group the rest
dyadically. For `j>=0`, let

```text
G_j = {gamma: 2^j <= |gamma| < 2^(j+1)}.
```

By `ZC`,

```text
sum_{gamma in G_j} m_gamma
  <= N_E(2^(j+1))
  <= C'_E 2^j (j+1).
```

By `W2`,

```text
|W_hat(i gamma)| <= C_W (1+|gamma|)^(-2).
```

Therefore

```text
sum_{gamma != 0} |m_gamma W_hat(i gamma)|
 <= C_W,E sum_{j>=0} 2^j (j+1) 2^(-2j)
 < infinity.
```

The same argument with `W_hat'` gives

```text
sum_{gamma != 0} m_gamma
 sup_{0<=v<=eta} (|W_hat(i gamma-v)| + |W_hat'(i gamma-v)|)
 < infinity.
```

This stronger form is what the branch-cut expansion needs.

## Branch Integral Estimate

Near a noncentral zero, S1-C gives the singular part

```text
A_E(z) = m_gamma log(z-i gamma) + holomorphic.
```

With the leftward cut `z=i gamma-v`, `v>=0`, its jump contributes

```text
I_gamma(u)
 = -m_gamma e^(i gamma u)
   integral_0^eta e^(-uv) W_hat(i gamma-v) dv
   + O(m_gamma e^(-eta u) M_gamma).
```

Watson expansion plus the summed `W_hat'` bound gives

```text
I_gamma(u)
 = -m_gamma e^(i gamma u) W_hat(i gamma)/u
   + O(m_gamma M_gamma/u^2)
   + O(m_gamma e^(-eta u) M_gamma),
```

where

```text
M_gamma = sup_{0<=v<=eta} (|W_hat(i gamma-v)| + |W_hat'(i gamma-v)|).
```

Summing over all noncentral zeros is legitimate by absolute convergence:

```text
sum_gamma I_gamma(u)
 = -Z_E,W(u)/u + O_E,W(u^(-2)) + O_E,W(e^(-eta u)),
```

with

```text
Z_E,W(u) = sum_{gamma != 0} m_gamma e^(i gamma u) W_hat(i gamma),
|Z_E,W(u)| <= sum_gamma |m_gamma W_hat(i gamma)| < infinity.
```

Thus the full offcentral branch term is pointwise

```text
O_E,W(1/log K).
```

This is stronger than averaged control and is enough for the S1 finite-part
limit once the central and regular contour pieces are closed.

## Contour Shift

Under `BC`, shifting the Mellin integral from `Re z=c` to `Re z=-eta` gives:

```text
S_1,W(K)
 = central branch contribution
   + sum_gamma I_gamma(log K)
   + left-boundary integral
   + kernel-pole residues left of the strip, if any.
```

The left-boundary integral is

```text
O(K^(-eta))
```

by the integrability clause in `BC`. Horizontal truncation vanishes along the
truncation sequence because `W_hat A_reg` is integrable on the vertical
boundaries. Kernel poles at negative real points, such as the `alpha=0`
smoothstep poles at `-2,-3`, contribute only powers `K^-2`, `K^-3`, hence are
smaller than `1/log K`.

Branch cuts do not add uncontrolled terms under `BC`: the jump across a
logarithmic cut is constant, so each branch contribution is exactly the
Laplace integral above. Collisions only change the logarithmic coefficient;
they do not change the `1/log K` scale unless a pole is present.

## Pointwise / Oscillatory / Averaged

Pointwise:
under `W2+ZC+BC`, the zero aggregate is bounded and divided by `log K`, so
offcentral zeros are `O(1/log K)`. S1 may be promoted to pointwise only after
the branch-only continuation and central/regular pieces are proved.

Oscillatory:
the sharper pointwise formula retains

```text
-Z_E,W(log K)/log K.
```

This is an oscillatory correction, but its amplitude tends to zero.

Averaged:
averaging is not needed for this S1 offcentral branch term. It remains the
fallback if `BC` fails, if the zero series is only conditionally controlled, or
if another factor contributes persistent pole terms.

## Sharp Obstructions

1. Hard cutoff obstruction. If `W_hat(i gamma)=1/(i gamma)`, `ZC` gives only

```text
sum_{n} log n / n,
```

which diverges. Pointwise absolute closure cannot be promoted without a new
cancellation theorem.

2. Pole obstruction. If `A_E(z)` has an offcentral pole at `i gamma`, the
contribution is

```text
c_gamma K^(i gamma) W_hat(i gamma),
```

persistent and not `o(1)`. It must be retained or averaged.

3. Right-half-plane obstruction. A branch at `a=beta+i gamma`, `beta>0`, gives

```text
K^beta e^(i gamma log K) W_hat(a)/log K,
```

which grows unless separately cancelled.

4. Branch-continuation obstruction. If `A_E` has extra cuts, natural boundary
behavior, nonintegrable regular remainder, or unverified companion singularities
in the contour strip, the zero-sum estimate alone does not justify the shift.

## Do Not Promote Unless

- `A_E(z)` branch-only continuation is proved in the exact Agent 3 good/bad
  local-factor normalization.
- `ZC` is either proved or source-verified by the repository protocol.
- The symmetric-square/adjoint companion has the same zero-summability and
  contour control, or its offcentral terms are explicitly retained.
- No offcentral pole on `Re z>=0` survives in `S_1,W` or the final H2 package.
- The central coefficient is stated with analytic rank
  `r=ord_{s=1}L(E,s)` before any algebraic-rank substitution.
- H1/H2 composition uses the same theorem mode: pointwise, oscillatory, or
  averaged.
- Any external theorem used later is `curl + pdftotext` verified with a short
  quote and page/equation.

## Changed File List

- `handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md`

## Commands Run

```bash
pwd && rg --files -g 'start.md' -g 'HANDOFF.md' -g 'L2_facts/farey-claim-ledger.md' -g 'S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md' -g 'S1A_EXPLICIT_FORMULA_DERIVATION.md' -g 'S1B_SOURCE_AUDIT.md' -g 'S1C_ZERO_TERM_ANALYSIS.md' -g 'S1D_AVERAGED_FALLBACK.md'
sed -n '1,220p' ../start.md
sed -n '1,240p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,220p' L1_index.md
sed -n '1,260p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
sed -n '1,700p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
sed -n '1,700p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
sed -n '1,700p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1C_ZERO_TERM_ANALYSIS.md
sed -n '1,700p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1D_AVERAGED_FALLBACK.md
rg -n "smoothstep|W_hat|zero|contour|branch|summability|Agent 3|S_1|S1|H2" handoff-2026-05-11-ec-h2-mertens-sprint handoff-2026-05-11-ec-smoothing-blockers -g '*.md'
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/DISPATCH_MANIFEST_2026-05-11.md
sed -n '60,130p' handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
sed -n '317,410p' handoff-2026-05-11-ec-h2-mertens-sprint/H2B_ANALYTIC_PROOF_ATTEMPT.md
sed -n '120,165p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '214,245p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
ls -la handoff-2026-05-11-ec-theorem-closure-wave
git status --short
find /Users/za/Documents/Farey\\ NOW -path '*handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md' -print
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md' 'handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md'
rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave'
sed -n '1,280p' handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
git status --short -- handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
head -n 5 handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md && tail -n 45 handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
rg -n "adjoin|multiplity|external theorem|PROOF_CANDIDATE|Do Not Promote|Pointwise|Averaged|Oscillatory" handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
find '/Users/za/Documents/Farey NOW' -maxdepth 1 -type d -name 'handoff-2026-05-11-ec-theorem-closure-wave' -print
ls -la '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave'
rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-ec-theorem-closure-wave'
git diff -- handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
```
