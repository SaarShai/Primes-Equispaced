NO_GO

# H1 Multiple-Zero And Rank-Zero No-Go

Confidence: 0.88 for the local residue obstruction; 0.78 for the final
composition guardrail because it assumes a standard H1 contour-shift expansion
and a pointwise H2 product asymptotic as hypotheses.

External theorem citations: none. This file uses local Laurent algebra and
conditional Perron-residue bookkeeping only. No `curl`/`pdftotext` source packet
is attached because no outside theorem is promoted.

Scope: fixed curve, fixed smoothing kernel, analytic rank

```text
r = ord_{s=1} L(E,s).
```

No cross-curve universality, BSD/rank equality, closed H2 package, or claim that actual
EC zeros have the multiplicities below is asserted.

## Executive Verdict

Pointwise H1 composition has two hard no-go boundaries.

1. Rank zero with a nonzero simple offcentral reciprocal residue is already at
   main scale. If H2 gives only a constant product factor, the term

   ```text
   e^(i gamma u) W_hat(i gamma)/L'(1+i gamma),   u=log K,
   ```

   survives in `c_E,W(e^u) P_E,W(e^u)`. Pointwise stabilization fails unless
   the net residue at that frequency cancels, the kernel kills it, the term is
   retained in an oscillatory formula, or the theorem is weakened to a proved
   averaged statement.

2. For positive rank `r`, an offcentral zero of multiplicity `m` generically
   contributes

   ```text
   e^(i gamma u) u^(m-1) b_{rho,-m} W_hat(i gamma)/(m-1)!.
   ```

   After multiplying by the H2 factor `u^(-r)`, this is constant-scale or worse
   whenever

   ```text
   m >= r+1.
   ```

   Thus the pointwise limit is blocked unless those multiple-zero terms are
   ruled out, kernel-cancelled, residue-cancelled, explicitly retained, or
   handled by a declared averaging/finite-part theorem strong enough for the
   remaining polynomial degree.

This is a no-go boundary, not an EC zero claim.

## Setup

Use the H1 convention from the closure wave:

```text
c_E,W(K)
  = (1/(2 pi i)) int_(Re z=sigma)
      K^z W_hat(z) / L(E,1+z) dz.
```

Write

```text
u = log K.
```

Assume the H1 contour shift, if available, gives a central residue polynomial
plus offcentral reciprocal-pole residues plus an error:

```text
c_E,W(e^u) = Q_0(u) + Z_c(u) + E_c(u).
```

The central term is

```text
Q_0(u)
  = Res_{z=0} e^(uz) W_hat(z)/L(E,1+z),
```

and, because `W_hat(z)=1/z+holomorphic` at `0`,

```text
Q_0(u) = u^r/L^(r)(E,1) + lower powers of u       if r>=1,
Q_0(u) = 1/L(E,1)                                  if r=0.
```

Assume also the pointwise H2 product target:

```text
P_E,W(e^u) = exp(B_E,W) u^(-r)(1+o(1)).
```

Then

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_E,W) u^(-r)(Q_0(u)+Z_c(u)+E_c(u))(1+o(1)).
```

Therefore a pointwise product limit requires, at minimum,

```text
Z_c(u)+E_c(u) = o(u^r).
```

For rank zero this means `Z_c(u)=o(1)`, not merely bounded.

## Exact Offcentral Residue Formula

Let

```text
rho = 1+i gamma,   gamma != 0,
z0 = i gamma,
```

be an offcentral zero of `L(E,s)` of multiplicity `m`. Locally,

```text
1/L(E,1+z)
  = sum_{j=1}^m b_{rho,-j}(z-z0)^(-j) + holomorphic.
```

Here

```text
b_{rho,-m} = m!/L^(m)(E,rho) != 0.
```

Since `W_hat` is holomorphic at `z0`, the H1 residue contributed by `rho` is

```text
R_rho(u)
 = e^(z0 u)
   sum_{j=1}^m b_{rho,-j}
     sum_{ell=0}^{j-1}
       u^ell/ell! *
       W_hat^(j-1-ell)(z0)/(j-1-ell)!.
```

Equivalently,

```text
R_rho(u) = e^(i gamma u) P_rho(u),
```

where `P_rho` is a polynomial of degree at most `m-1`.

For a simple zero:

```text
R_rho(u) = e^(i gamma u) W_hat(i gamma)/L'(E,rho).
```

For a multiple zero with `W_hat(i gamma) != 0`, the leading term is

```text
R_rho(u)
 = e^(i gamma u)
   b_{rho,-m} W_hat(i gamma) u^(m-1)/(m-1)!
   + O(u^(m-2)).
```

More generally, if `W_hat` has a zero of exact order `q` at `i gamma`, then the
pole is reduced. If `q<m`, the degree becomes `m-1-q` and the leading term is

```text
e^(i gamma u)
 b_{rho,-m} W_hat^(q)(i gamma) u^(m-1-q)
 /(q!(m-1-q)!).
```

If `q>=m`, this particular pole is kernel-cancelled.

## No-Go Theorem

Assume:

- the H1 residue expansion above is valid with error `E_c(u)=o(u^r)` after the
  displayed offcentral terms are included;
- H2 has the pointwise form

  ```text
  P_E,W(e^u)=exp(B_E,W)u^(-r)(1+o(1));
  ```

- there is a nonzero net offcentral H1 residue term after combining all zeros
  with the same frequency and polynomial degree.

Then:

### A. Rank-Zero Simple-Residue No-Go

If `r=0` and a simple offcentral zero `rho=1+i gamma` has nonzero net
coefficient

```text
A_gamma = W_hat(i gamma)/L'(E,rho)
```

after same-frequency cancellations, then the product has the form

```text
c_E,W(e^u)P_E,W(e^u)
 = exp(B_E,W)(
     1/L(E,1) + A_gamma e^(i gamma u)
   )
   + lower/off-frequency terms + o(1).
```

For real coefficients and real `W`, the conjugate pair contributes

```text
2 exp(B_E,W) Re(A_gamma e^(i gamma u)).
```

If `A_gamma != 0`, this term has no pointwise limit as `u -> infinity`.
Choosing phases with `gamma u + arg A_gamma = 0 mod 2 pi` and
`gamma u + arg A_gamma = pi mod 2 pi` gives two subsequential limits differing
by `4 exp(B_E,W)|A_gamma|` in the conjugate-pair case.

Thus rank-zero pointwise stabilization is false unless the net simple-residue
aggregate is actually `o(1)` or the theorem changes mode.

### B. Positive-Rank Multiple-Zero No-Go

Let `r>=1`. Suppose an offcentral zero `rho=1+i gamma` has multiplicity `m` and
`W_hat(i gamma) != 0`. Its normalized contribution to the product is

```text
exp(B_E,W)
 e^(i gamma u)
 b_{rho,-m} W_hat(i gamma)
 u^(m-1-r)/(m-1)!
 + O(u^(m-2-r)).
```

If

```text
m >= r+1,
```

then `m-1-r >= 0`.

- If `m=r+1`, the obstruction is a nonzero constant-scale oscillation.
- If `m>r+1`, the obstruction grows like `u^(m-1-r)` along suitable phase
  subsequences.

Either way, the pointwise product limit cannot be the central constant

```text
exp(B_E,W)/L^(r)(E,1)
```

unless the leading net coefficient cancels, the kernel has a zero at the
offcentral point of sufficient order, the oscillation is retained explicitly,
or the theorem is weakened to an averaging/finite-part statement that is proved
for this polynomial degree.

With kernel vanishing order `q` at `i gamma`, replace the generic boundary by

```text
m >= r+q+1.
```

Equivalently, the exact condition is:

```text
degree(P_rho) >= r
```

for a nonzero net residue polynomial after all same-frequency cancellations.

## Finite Sums And Cancellation

A finite exponential polynomial

```text
T(u)=sum_n C_n e^(i gamma_n u),   gamma_n != 0,
```

cannot converge pointwise as `u -> infinity` unless all nonzero-frequency
coefficients cancel. Direct check: if `T(u)` had a finite limit `L`, then

```text
(1/U) int_0^U |T(u)-L|^2 du -> 0.
```

But termwise integration gives the limiting mean square as the sum of the
squared moduli of the nonconstant coefficients, plus the squared constant
mismatch. Hence every nonzero-frequency coefficient must be zero.

For polynomial-exponential terms, first divide by the highest surviving power
of `u`. The same argument applies to the leading exponential polynomial. Hence
different frequencies do not rescue pointwise convergence. Only exact
same-frequency coefficient cancellation, kernel zeros, explicit subtraction, or
a changed theorem mode can remove the obstruction.

For an infinite zero aggregate, a theorem must prove the corresponding
summability and cancellation statement directly. Decay of `W_hat(i gamma)` is
not enough by itself because H1 also contains reciprocal Laurent coefficients
such as `1/L'(rho)` or higher analogues.

## Formal Constructions

These are local models for the Perron integrand. They are not claims about EC
zeros.

### Rank Zero

Take a formal model with

```text
L_model(1+z)=C(1+z^2/gamma^2),   C != 0.
```

Then `r=0` and there are simple offcentral zeros at `z=+-i gamma`. If
`W_hat(i gamma) != 0`, the H1 residues give

```text
c_model(e^u)P_model(e^u)
 = exp(B)/C
   + 2 exp(B) Re(A e^(i gamma u))
   + o(1),
```

with `A != 0` generically. This has no pointwise limit.

### Positive Rank With Borderline Multiplicity

For any `r>=1`, take

```text
L_model(1+z)=C z^r (1+z^2/gamma^2)^(r+1).
```

Then the central zero has rank `r`, while each offcentral zero has multiplicity
`m=r+1`. If `W_hat(i gamma) != 0`, the H1 offcentral residue has degree `r`.
After H2 multiplication by `u^(-r)`, a constant-scale oscillation survives.
Thus the central limit is not pointwise unless the oscillation is removed by an
extra mechanism.

### Positive Rank With Higher Multiplicity

If

```text
L_model(1+z)=C z^r (1+z^2/gamma^2)^m,   m>r+1,
```

the normalized offcentral term grows like

```text
u^(m-1-r) e^(i gamma u)
```

up to a nonzero generic coefficient. A plain pointwise theorem is then even
farther away: the raw product is not merely nonconvergent, it is not bounded
along phase subsequences.

## Averaging Escape Hatches

Averaging is a different theorem mode, not a cosmetic fix.

- Constant-scale terms (`degree(P_rho)=r`) can disappear under a proved
  logarithmic/Cesaro average in `u`, because averages of `e^(i gamma u)` vanish
  for `gamma != 0`.
- Growing terms (`degree(P_rho)>r`) are not automatically cured by a first
  average. A finite-part average, repeated integration, explicit subtraction,
  or stronger damping must be stated and proved.
- Averaging `log P` alone does not average `cP`. The H1/H2 product needs its
  own averaged or correlation theorem.

Thus future claims must declare one of:

```text
pointwise limit:        prove Z_c(u)=o(u^r);
oscillatory expansion:  retain all non-o(u^r) residues explicitly;
averaged theorem:       define the average and prove it kills the residues;
kernel-cancelled mode:  choose W with zeros of sufficient order at named zeros.
```

## Dependencies

1. Same H1/H2 kernel and Mellin normalization, including
   `W_hat(z)=1/z+holomorphic` at `0`.
2. Analytic rank convention `r=ord_{s=1}L(E,s)`.
3. H1 contour-shift expansion with central polynomial, offcentral Laurent
   residues, reciprocal derivative/Laurent coefficient control, and contour
   error.
4. H2 pointwise product expansion
   `P_E,W(e^u)=exp(B_E,W)u^(-r)(1+o(1))`.
5. Same-frequency cancellation accounting for conjugate zero pairs and any
   repeated frequencies.
6. Infinite zero aggregates controlled by an explicit summability, truncation,
   or averaged theorem.
7. No substitution of algebraic rank, BSD, cross-curve universality, or actual
   multiple-zero assertions without separate sourced proof.

## Do Not Promote Unless

- Rank zero is separated and the H1 reciprocal residue aggregate is proved
  `o(1)`, explicitly retained, kernel-cancelled, or averaged.
- For positive rank, every offcentral zero with effective residue degree
  `>= r` is ruled out, cancelled, retained, or averaged.
- The generic danger case `m>=r+1` is handled; with a kernel zero of order `q`,
  the corrected danger case `m>=r+q+1` is handled.
- The exact residue polynomial

  ```text
  R_rho(u)
   = e^(i gamma u)
     sum_{j=1}^m b_{rho,-j}
       sum_{ell=0}^{j-1}
         u^ell/ell! *
         W_hat^(j-1-ell)(i gamma)/(j-1-ell)!
  ```

  appears in the H1 theorem or is replaced by a source-verified equivalent.
- Reciprocal derivative/Laurent coefficient growth is controlled; Mellin decay
  of `W_hat` alone is not claimed to control `1/L'(rho)`.
- H2 is closed in the exact Agent-3 local-factor convention before composing.
- The theorem mode is declared once: pointwise, oscillatory, averaged, or
  kernel-cancelled.
- No finite-window EC smoothing diagnostic is used as theorem evidence.
- Every external theorem used later follows the repository protocol:
  `curl + pdftotext + short quote + page/equation`.

## Changed Files

```text
handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
```

## Commands Run

```bash
sed -n '1,220p' ../start.md
sed -n '1,240p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,260p' H1_H2_COMPOSITION_AUDIT.md
sed -n '1,260p' ADVERSARIAL_REFEREE.md
./te doctor
sed -n '1,220p' token-economy.yaml
test -f L0_rules.md && sed -n '1,220p' L0_rules.md || true
test -f L1_index.md && sed -n '1,220p' L1_index.md || true
sed -n '1,280p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,300p' handoff-2026-05-11-ec-theorem-closure-wave/ADVERSARIAL_REFEREE.md
ls -la handoff-2026-05-11-h1-reciprocal-perron-wave
test -f handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md && sed -n '1,260p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md || true
rg -n "H1_MULTIPLE|rank zero|multiple zero|offcentral|reciprocal pole|Laurent|m>=r|m >= r|H1 reciprocal" handoff-2026-05-11-h1-reciprocal-perron-wave handoff-2026-05-11-ec-theorem-closure-wave handoff-2026-05-11-ec-smoothing-blockers handoff-2026-05-11-gpt55-wave handoff-2026-05-09-followup
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave HANDOFF.md L2_facts/farey-claim-ledger.md log.md
sed -n '1,240p' handoff-2026-05-11-h1-reciprocal-perron-wave/DISPATCH_MANIFEST_2026-05-11.md
sed -n '280,380p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md
sed -n '80,135p' handoff-2026-05-11-ec-theorem-closure-wave/H2_POINTWISE_THEOREM_PACKAGE.md
sed -n '88,140p' handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
sed -n '1,150p' handoff-2026-05-11-ec-smoothing-blockers/EC_SMOOTHING_BLOCKER_SYNTHESIS_2026-05-11.md
find '/Users/za/Documents/Farey NOW' -path '*H1_MULTIPLE_ZERO_RANK0_NOGO.md' -print
pwd; ls -la '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave' 2>/dev/null || true; ls -la '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave'
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md' '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md'
rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave'
sed -n '1,260p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
sed -n '260,560p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
rg -n "^NO_GO$|^Confidence:|^External theorem citations:|^## Dependencies$|^## Do Not Promote Unless$|^## Changed Files$|^## Commands Run$|m >= r\\+1|rank zero|Rank-Zero|R_rho|W_hat\\(i gamma\\)/L'" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
perl -ne 'print $. . ":" . $_ if /[^\\x00-\\x7F]/' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md
git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_MULTIPLE_ZERO_RANK0_NOGO.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```

Bootstrap note: `./te doctor` failed because `./te` is absent in the specified
workspace, and `token-economy.yaml` is absent there. The root-level
`H1_H2_COMPOSITION_AUDIT.md` and `ADVERSARIAL_REFEREE.md` paths were also
absent, so I read the requested files at their nested theorem-closure paths.
