PROOF_CANDIDATE

Confidence: 0.78 for the conditional branch theorem below; 0.55 for using it as an unconditional EC input without new source/proof closure.

Dependencies: exact Agent-3 good/bad local normalization; analytic rank `r=ord_{s=1} L(E,s)`; an admissible endpoint kernel `W`; branch-only continuation of `A_E(z)=sum_p a_p p^(-1-z)`; weighted branch/zero summability; contour-shift remainders; symmetric-square bookkeeping through `kappa_sym`.

External theorem citations: none. No external theorem is used as a cited fact in this deliverable; all source-level EC continuation/nonvanishing inputs remain dependencies.

# S1 Branch Theorem Candidate

## Verdict

The endpoint-smoothed explicit formula is proved as a conditional contour/branch theorem. It gives the required offcentral suppression:

```text
rho=1+i gamma, gamma != 0
  ->  -m_rho K^(i gamma) W_hat(i gamma)/log K
```

for a non-colliding zero of `L(E,s)`, with the sign convention stated below. This is pointwise lower order once the weighted zero sum is controlled. It is not a source-closed elliptic-curve theorem yet.

## Objects And Branches

Fix an elliptic curve `E/Q`. Let

```text
S_1,W(K) = sum_p W(p/K) a_p/p.
```

The Agent-3 product convention is:

```text
good p: A_p(1) = 1 - a_p/p + 1/p,
bad  p: A_p(1) = 1 - a_p/p.
```

Separate finitely many bad primes. For good primes define

```text
A_E(z) = sum_{p good} a_p p^(-1-z)
```

initially in its convergence half-plane. Bad primes contribute

```text
C_bad(E) = sum_{p bad} a_p/p
```

to the constant when `W(t)=1` near `t=0`.

Let

```text
W_hat(z) = integral_0^infty W(t)t^(z-1)dt.
```

Admissible `W`: compact support in `[0,1]`; `W(t)=1` on `[0,alpha]` for some `alpha<1`; endpoint-smoothed enough that `W_hat` is meromorphic with only a simple pole at `0`, residue `1`, and on fixed vertical strips away from `0`,

```text
W_hat(sigma+i tau) = O_W,sigma((1+|tau|)^(-2-epsilon))
```

or any replacement decay sufficient for the zero-summability hypothesis. The tested smoothstep kernels satisfy the intended endpoint class; this file does not cite an external theorem for that.

Branch convention: every offcentral branch point `a` uses the left-going cut

```text
Gamma_a = {a-t : t >= 0}.
```

The branch of `log(z-a)` is inherited by continuation from the initial right half-plane. Equivalently, write local singularities as

```text
A_E(z) = c_a log(1/(z-a)) + holomorphic.
```

With this convention, a local term `c_a log(1/(z-a))` contributes

```text
c_a K^a W_hat(a)/log K + O_a,W(K^a/(log K)^2).
```

## Conditional Theorem

Let `u=log K`. Assume:

1. Mellin inversion holds for some `c>0`:

   ```text
   S_1,W^good(K) =
     (1/(2 pi i)) integral_(c) K^z W_hat(z) A_E(z) dz.
   ```

2. In a strip `Re z >= -eta`, after removing the left-going cuts, `A_E` has no offcentral poles with `Re z >= 0`; its only relevant singularities are logarithmic branches. Near `z=0`,

   ```text
   A_E(z) = c_0 log(1/z) + h_0(z).
   ```

   At each offcentral branch point `a`,

   ```text
   A_E(z) = c_a log(1/(z-a)) + h_a(z).
   ```

3. The central EC bookkeeping uses the exact good-prime identity

   ```text
   log L_good(E,1+z)
     = A_E(z) + (1/2)B_sym(2z) - (1/2)M_good(2z) + H_E(z),
   ```

   with `H_E` holomorphic at `0`,

   ```text
   log L(E,1+z) = r log z + holomorphic,   r=ord_{s=1}L(E,s),
   B_sym(2z)   = kappa_sym log z + holomorphic,
   M_good(2z)  = log(1/z) + holomorphic.
   ```

   Therefore

   ```text
   c_0 = 1/2 + kappa_sym/2 - r.
   ```

4. The branch aggregate is pointwise summable:

   ```text
   sum_{a != 0, Re a = 0} |c_a W_hat(a)| < infinity,
   ```

   with the corresponding derivative/local-radius summability needed to sum the `O((log K)^(-2))` local Taylor remainders.

5. Horizontal, shifted-line, and far-cut contour remainders are

   ```text
   O(K^(-eta)) + O((log K)^(-2))
   ```

   after the branch contributions are removed.

Then

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + (1/log K) Z_1,E,W(log K)
   + O((log K)^(-2))
   + O(K^(-eta)),
```

where

```text
Z_1,E,W(u) = sum_{a != 0, Re a = 0} c_a W_hat(a) exp(a u),
```

and branch points with `Re a<0` are absorbed into the decaying error or retained as

```text
(1/log K) sum_{Re a<0} c_a W_hat(a) K^a.
```

Since `Z_1,E,W` is bounded under the displayed absolute summability, the pointwise finite-part form follows:

```text
S_1,W(K)
 = (1/2 + kappa_sym/2 - r) log log K
   + C_1,E,W
   + o(1).
```

## Proof Skeleton

Start from Mellin inversion on `Re z=c` and shift the contour left in the cut strip. The shifted line and horizontal edges are errors by Hypothesis 5. The remaining pieces are the central cut at `0` and the offcentral cuts `Gamma_a`.

At `z=0`,

```text
W_hat(z) = 1/z + holomorphic,
A_E(z)  = c_0 log(1/z) + holomorphic.
```

The inverse Mellin/Laplace finite part of `(1/z)log(1/z)` is

```text
log u + constant,  u=log K,
```

so the central branch contributes `c_0 log log K + constant`.

For `a != 0`, `W_hat` is holomorphic at `a`. Around the left-going cut write `z=a-t`, `t>0`. The branch jump of `log(1/(z-a))` gives

```text
c_a K^a integral_0^infty exp(-ut) W_hat(a-t) dt.
```

Taylor expansion of `W_hat(a-t)` at `t=0`, integrated against `exp(-ut)`, yields

```text
c_a K^a ( W_hat(a)/u + O_a,W(u^(-2)) ).
```

The summability hypothesis permits summing these local contributions and their remainders. The holomorphic parts contribute only to `C_1,E,W` plus the contour error. Adding bad primes changes only `C_1,E,W`. This proves the displayed formula.

## Zero Terms

If `rho=1+i gamma`, `gamma != 0`, is a zero of `L(E,s)` of multiplicity `m_rho`, and no symmetric-square/harmonic branch collides at `a=i gamma`, then the `log L` part gives

```text
log L(E,1+z) = m_rho log(z-i gamma) + holomorphic
             = -m_rho log(1/(z-i gamma)) + holomorphic.
```

Thus

```text
c_{i gamma} = -m_rho,
```

and the zero contributes

```text
-m_rho K^(i gamma) W_hat(i gamma)/log K
  + O_gamma,W((log K)^(-2)).
```

Conjugate pairing gives the real leading term

```text
-(2m_rho/log K) Re(K^(i gamma) W_hat(i gamma)).
```

If `W_hat(i gamma)=0`, the leading branch term vanishes and the first possible term is order `(log K)^(-2)`.

If a branch point has `rho=beta+i gamma`, the contribution is

```text
c_{rho-1} K^(beta-1+i gamma) W_hat(rho-1)/log K.
```

If `beta<1`, it power-decays. If `beta=1`, it is oscillatory but `1/log K` suppressed. If `beta>1`, pointwise finite part fails unless another term cancels it.

## Central Contribution

The central zero of `L(E,s)` alone contributes

```text
-r log log K
```

to `S_1,W`. The full S1 central coefficient is not `-r`; it is

```text
1/2 + kappa_sym/2 - r.
```

The extra `+1/2` comes from the prime-harmonic term required when solving for `A_E` from `log L`. The `+kappa_sym/2` term records the central logarithmic order of the symmetric-square companion in the same normalization. H2 can only recover product slope `-r` after adding

```text
(1/2)S_sym,W(K) - (1/2)M_good,W(K).
```

## Pointwise / Oscillatory / Averaged

Pointwise theorem: the displayed `C_1,E,W+o(1)` statement follows from absolute weighted zero summability and contour control.

Oscillatory theorem: if `Z_1,E,W(u)` is defined but not known to be bounded, the honest statement retains

```text
Z_1,E,W(log K)/log K.
```

Averaged theorem: logarithmic averaging may kill nonzero frequencies, but this deliverable does not use averaging and does not claim an averaged theorem without a separate summability/mean-interchange proof.

## No-Go / Gap Map

This is not an unconditional EC theorem. Promotion is blocked at exactly these points:

- prove the branch-only continuation of `A_E(z)` for the exact fixed curve and exact endpoint kernel;
- prove no offcentral pole of `A_E` survives on `Re z=0`;
- prove the weighted zero/branch summability strong enough for termwise branch integration and the `O((log K)^(-2))` remainder;
- prove shifted-contour horizontal and left-edge bounds;
- prove the symmetric-square finite-part theorem in the same normalization before using this inside H2;
- verify any desired claim `kappa_sym=0` for the exact companion object;
- keep analytic rank `ord_{s=1}L(E,s)` unless BSD/rank equality or direct analytic-rank verification is explicitly added.

If any offcentral pole exists on `Re z=0`, the formula gains a persistent term

```text
d_a K^a W_hat(a),
```

and the pointwise `C+o(1)` S1 theorem is false. If the branch sum is not controlled, the theorem is only a formal/truncated explicit formula.

## Do Not Promote Unless

- The exact Agent-3 local factors are retained, including bad primes.
- The theorem states `r=ord_{s=1}L(E,s)` before any rank substitution.
- The S1 central coefficient is `1/2 + kappa_sym/2 - r`, not `-r`.
- Offcentral zeros are proved logarithmic branch terms, not silently treated as residues.
- The zero sum and contour remainders are proved or explicitly assumed.
- `S_sym,W` and `M_good,W` are included before claiming an H2 product coefficient.
- Pointwise, oscillatory, and averaged modes are not mixed.
- Any external theorem used later is reintroduced with `curl + pdftotext` verification, verbatim quote, and page/equation.

## Changed Files

```text
handoff-2026-05-11-ec-theorem-closure-wave/S1_BRANCH_THEOREM_CANDIDATE.md
```

## Commands Run

```text
sed -n '1,220p' ../start.md
./te doctor
sed -n '1,220p' token-economy.yaml
sed -n '1,220p' L0_rules.md
sed -n '1,240p' L1_index.md
sed -n '1,220p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
sed -n '1,220p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1_EXPLICIT_FORMULA_SYNTHESIS_2026-05-11.md
sed -n '1,260p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
sed -n '220,760p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1A_EXPLICIT_FORMULA_DERIVATION.md
sed -n '1,300p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1C_ZERO_TERM_ANALYSIS.md
sed -n '1,260p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
sed -n '220,520p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1F_SYM2_COMPANION_TERM.md
sed -n '1,280p' handoff-2026-05-11-ec-s1-explicit-formula-sprint/S1B_SOURCE_AUDIT.md
sed -n '1,220p' handoff-2026-05-11-ec-h2-mertens-sprint/H2E_THEOREM_PACKAGING.md
sed -n '1,220p' handoff-2026-05-11-ec-theorem-closure-wave/DISPATCH_MANIFEST_2026-05-11.md
rg --files handoff-2026-05-11-ec-theorem-closure-wave handoff-2026-05-11-ec-s1-explicit-formula-sprint
git status --short
```

No `curl`/`pdftotext` theorem verification was run because this file cites no external theorem as a fact.
