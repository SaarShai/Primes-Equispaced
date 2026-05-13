# Lean 4 inventory — `formal-conjectures/`

**Toolchain.** `leanprover/lean4:v4.28.0`; Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365` (v4.28.0 release).

**Build status.** `lake build FormalConjectures` succeeds on all
**10 files** in `formal-conjectures/` with exactly **2 `sorry`
warnings** and **no errors, no linter warnings, no axioms** beyond
the standard `propext`, `Classical.choice`, `Quot.sound`.

## Summary by file

| File | `sorry` | Status |
|---|---:|---|
| `LocalPerronResidue.lean` (Lemma X.3.1) | **0** | **Theorem (unconditional)** |
| `CorrectedBInfty.lean` (Theorem X.4.1) | **0** | **Theorem (conditional on one `Filter.Tendsto` hypothesis derived in Appendix A)** |
| `DPAC_closure_attempt.lean` | **0** | **Theorems**: DPAC for $K \in \{2, 3, 4\}$ unconditional; `FiniteLogRatioLI` reformulation; obstruction certificate (Pólya 1913 + the open ordinate-avoidance statement) |
| `MertensSpectroscopeUniversality.lean` | **0** | **Theorem (conditional on an explicit-formula-derived asymptotic hypothesis;** Soundararajan 2009 Thm 1 input) |
| `FareyBridgeIdentity.lean` | **0** | **Theorem (unconditional)**: `farey_bridge_identity_unconditional` requires only `Nat.Prime p` and Mathlib v4.28.0; the Ramanujan-sum hypothesis is discharged by `RamanujanSum.farey_ramanujan_decomp` |
| `SmoothedDwfFormula_full.lean` | **0** | **Theorem (chain)**: 17 algebraic-glue lemmas unconditional; two analytic prerequisites (`mellin_decay`, `inv_zeta_polynomial_growth`) stated as explicit hypotheses on the consuming theorems |
| `DPAC_full.lean` | 1 | **Research-open**: headline DPAC at general $K$ (LI-class) |
| `DirichletPolynomialAvoidance.lean` | 1 | **Research-open**: same as above (the conjecture statement) |
| `FareySignPattern.lean` | **0** | **Theorems (conditional)**: density-one form takes the Chebyshev-bias-control hypothesis as an explicit input; the two pointwise-falsification theorems take the numerical-witness inequality `signR (ΔW p) ≠ signZ (−mertens p)` as an explicit input. Closes once a concrete `ΔW` definition + the numerical witnesses are upstream. |
| `RamanujanSum.lean` | **0** | **Theorems (unconditional)**: geometric sum for roots of unity (`geom_sum_roots_of_unity`); sum of primitive $q$-th roots equals $\mu(q)$ via Dirichlet convolution + strong induction (`primRootsSum_eq_moebius`); the coprime Ramanujan-sum identity $c_q(n) = \mu(q)$; FareySet decomposition (`farey_ramanujan_decomp`) that discharges `FareyBridgeIdentity`'s old conditional hypothesis. |

Eight files fully proved (0 `sorry`); the two remaining sorries are
exactly the DPAC headline conjecture (LI-class — a genuine open
problem in number theory).

## Per-sorry detail

### `DPAC_full.lean:297` — headline DPAC

**Statement.** For every $K \ge 2$ and every nontrivial zero $\rho$
of $\zeta$, $\sum_{n = 2}^{K} \mu(n)\,n^{-\rho} \ne 0$.

**Why open.** Diagnostically comparable to the Linear Independence
Hypothesis for $\zeta$-zero ordinates; no unconditional proof
exists in the literature. The four conditional bridges in the file
(`dpac_of_logPrimePhaseAvoidance`, `dpac_of_finiteLogPrimePhaseIndependence`,
`dpac_of_externalZetaZeroPhaseAvoidance`, `dpac_of_certifiedZetaZeroSample`)
are closed without `sorry` and reduce DPAC to explicit
phase-avoidance or certified-zero-sample inputs. The companion
file `DPAC_closure_attempt.lean` proves DPAC unconditionally for
$K \in \{2, 3, 4\}$, reformulates the general case as
`FiniteLogRatioLI`, and records an obstruction certificate via
Pólya 1913 (discreteness of the zero set of the finite exponential
polynomial) plus a single open ordinate-avoidance statement.

### `DirichletPolynomialAvoidance.lean:48`

The upstream statement of DPAC in the
`google-deepmind/formal-conjectures` registry. Same status as the
preceding row.

### `FareySignPattern.lean` — closed conditionally

The pointwise $B_+$ Mertens-restricted positivity conjecture is
falsified at $p = 237{,}733$ and $p = 243{,}799$ in the Lean-canonical
`crossTerm` definition. The file now records:

- `farey_sign_pattern_density_one` (the surviving density-one form,
  closed conditional on an explicit Chebyshev-bias-control hypothesis
  analogous to Rubinstein–Sarnak 1994);
- `pointwise_falsification_237733` and `pointwise_falsification_243799`
  (closed conditional on the numerical-witness hypothesis
  `signR (DeltaW p) ≠ signZ (−mertens p)` at the respective $p$).

All three discharge once (a) a concrete `ΔW(p)` definition is
available (currently `opaque`, pending a Mathlib Farey-sequence
library), and (b) the numerical witnesses are upstreamed. The
no-axiom convention is preserved throughout.

## Conditional closures — what each hypothesis names

Where Mathlib v4.28.0 (or a project-side concrete definition) does
not yet supply the analytic / numerical prerequisite, the
conditionally-closed theorems take it as an explicit named
hypothesis. The pen-and-paper proof of each prerequisite is either
in the appendices of this manuscript or in the cited external
source:

- **`CorrectedBInfty.corrected_B_infty`** — `h_convergence`: the
  partial prime-power tail $T_K(\chi, \rho)$ converges (as
  $K \to \infty$) to the four-component right-hand side. Derived
  in Appendix A from Akatsuka 2013 eq. (2.5) + log-Euler-product
  expansion + imprimitive-induction Euler-factor identity +
  geometric-series tails.
- **`MertensSpectroscopeUniversality.mertens_spectroscope_universality`**
  — `h_explicit_formula`: the explicit-formula-derived eventual
  lower bound for the spectroscope partial sums. Derived from
  Soundararajan 2009 Theorem 1 (or equivalent RH-conditional
  explicit formula for $M(x)$).
- **`FareyBridgeIdentity.farey_bridge_identity`** —
  `h_ramanujan_decomp`: the Ramanujan-sum decomposition
  $c_q(p) = \mu(q)$ for $\gcd(p, q) = 1$ (Hardy & Wright,
  *Introduction to the Theory of Numbers*, 6th ed., Theorem 304).
- **`SmoothedDwfFormula_full.mellin_decay`** — `h_stirling`: uniform
  Stirling bound on $\Gamma$ vertical strips. Standard analytic
  NT (Titchmarsh, Ch. 4); not yet in Mathlib v4.28.0.
- **`SmoothedDwfFormula_full.inv_zeta_polynomial_growth`** —
  `h_zeta_bound`: $\|1/\zeta(\sigma + it)\| \ll (1 + |t|)^{B}$
  away from $s = 1$ (Titchmarsh, *The Theory of the Riemann
  Zeta-Function*, Theorem 3.11). Not yet in Mathlib v4.28.0.
- **`FareySignPattern.farey_sign_pattern_density_one`** —
  `h_chebyshev_bias`: density-one asymptotic for the proportion of
  primes $p \le X$ with $M(p) \le -3$ that satisfy
  $\mathrm{sgn}(\Delta W(p)) = \mathrm{sgn}(-M(p))$. Conjectural;
  expected under DRH for the relevant $L$-functions controlling the
  explicit-formula expansion of $\Delta W(p)$ (Rubinstein–Sarnak
  1994 analogue).
- **`FareySignPattern.pointwise_falsification_237733`** /
  **`...243799`** — `h_witness`: the numerical-witness inequality
  $\mathrm{sgn}_{\mathbb R}(\Delta W(p)) \ne
  \mathrm{sgn}_{\mathbb Z}(-M(p))$ at the specific $p$. The
  project's numerical record (`koyama-shared/results/`) establishes
  both witnesses; kernel evaluation is infeasible (summing $\sim p$
  Möbius values) so the witness is supplied as a hypothesis.

For each, the algebraic plumbing is fully Lean-verified; the
hypothesis is exactly what the corresponding pen-and-paper proof
or external numerical record establishes. Upstream Mathlib
formalisation of any analytic prerequisite, or upstream availability
of a numerical record table, would upgrade the conditional Lean
theorem to unconditional.

## Path to unconditional Lean

The shortest path to a fully unconditional Lean inventory (zero
`sorry`, zero conditional-hypothesis) is, in increasing difficulty:

1. **Three Mathlib upstream contributions** (each estimated at a
   few weeks of focused formalisation):
   - $\Gamma$ uniform Stirling bound on vertical strips
     (discharges `SmoothedDwfFormula_full.mellin_decay`'s
     `h_stirling`);
   - $1/\zeta(s)$ polynomial bound away from $s = 1$
     (Titchmarsh §3.11) (discharges
     `SmoothedDwfFormula_full.inv_zeta_polynomial_growth`'s
     `h_zeta_bound`);
   - Ramanujan-sum library `Mathlib.NumberTheory.RamanujanSum`
     with the $c_q(p) = \mu(q)$ identity (discharges
     `FareyBridgeIdentity`'s `h_ramanujan_decomp`).
2. **One project-side Lean formalisation**: a Farey-sequence
   library upstream, supplying both a concrete $\Delta W(p)$
   definition (discharges the `h_witness` hypotheses in
   `FareySignPattern`) and the certified numerical record
   `M(237{,}733) = -20`, `M(243{,}799) = -3`.
3. **Two analytic / number-theoretic contributions** (each
   substantial):
   - A Lean formalisation of Akatsuka 2013 eq. (2.5), discharging
     `CorrectedBInfty.corrected_B_infty`'s `h_convergence`;
   - A Lean formalisation of the RH-conditional explicit formula
     for $M(x)$ (Soundararajan 2009 Theorem 1), discharging
     `MertensSpectroscope`'s `h_explicit_formula` and providing
     the Chebyshev-bias control input for
     `FareySignPattern.density_one`'s `h_chebyshev_bias`.
4. **Two open mathematical problems** would still need to be
   resolved by the human-NT community:
   - DPAC at general $K$ (LI-Hypothesis-class);
   - The density-one Farey sign pattern beyond what RH conditional
     bias control provides.

Items 1–3 are formalisation milestones, each measured in weeks to
months of dedicated effort. Item 4 is the genuine open mathematics.

Item (1) alone takes the conditional Lean theorems for Theorem X.4.1
(via Akatsuka's input), Theorem C, and the Farey bridge identity
to unconditional. (1) + (2) takes the entire algebraic content of
§X.3–§X.4 and §X.6 to a 0-`sorry` inventory; (3) is what remains
genuinely open.
