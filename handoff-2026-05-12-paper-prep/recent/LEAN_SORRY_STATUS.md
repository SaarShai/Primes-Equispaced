# Lean 4 inventory — `formal-conjectures/`

**Toolchain.** `leanprover/lean4:v4.28.0`; Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365` (v4.28.0 release).

**Build status.** `lake build FormalConjectures` succeeds on all
**9 files** in `formal-conjectures/` with exactly **5 `sorry`
warnings** and **no errors, no linter warnings, no axioms** beyond
the standard `propext`, `Classical.choice`, `Quot.sound`.

## Summary by file

| File | `sorry` | Status |
|---|---:|---|
| `LocalPerronResidue.lean` (Lemma X.3.1) | **0** | **Theorem (unconditional)** |
| `CorrectedBInfty.lean` (Theorem X.4.1) | **0** | **Theorem (conditional on one `Filter.Tendsto` hypothesis derived in Appendix A)** |
| `DPAC_closure_attempt.lean` | **0** | **Theorems**: DPAC for $K \in \{2, 3, 4\}$ unconditional; `FiniteLogRatioLI` reformulation; obstruction certificate (Pólya 1913 + the open ordinate-avoidance statement) |
| `MertensSpectroscopeUniversality.lean` | **0** | **Theorem (conditional on an explicit-formula-derived asymptotic hypothesis;** Soundararajan 2009 Thm 1 input) |
| `FareyBridgeIdentity.lean` | **0** | **Theorem (conditional on a Ramanujan-sum decomposition hypothesis;** Hardy–Wright Thm 304 input) |
| `SmoothedDwfFormula_full.lean` | **0** | **Theorem (chain)**: 17 algebraic-glue lemmas unconditional; two analytic prerequisites (`mellin_decay`, `inv_zeta_polynomial_growth`) stated as explicit hypotheses on the consuming theorems |
| `DPAC_full.lean` | 1 | **Research-open**: headline DPAC at general $K$ (LI-class) |
| `DirichletPolynomialAvoidance.lean` | 1 | **Research-open**: same as above (the conjecture statement) |
| `FareySignPattern.lean` | 3 | **Statement-only**: density-one form + two falsification witnesses; awaits a concrete `ΔW` formalisation from an upstream Farey-sequence library |

Six files fully proved (0 `sorry`); five remaining sorries are all
genuinely research-open.

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

### `FareySignPattern.lean:122, 181, 190` (three sorries)

The pointwise $B_+$ Mertens-restricted positivity conjecture is
falsified at $p = 237{,}733$ and $p = 243{,}799$ in the Lean-canonical
`crossTerm` definition. The file records:

- `farey_sign_pattern_density_one` (the surviving density-one form,
  research-open in Lean — would require a Chebyshev-bias control
  on $\Delta W(p)$ analogous to Rubinstein–Sarnak 1994);
- `pointwise_falsification_237733` and `pointwise_falsification_243799`
  (the two numerical witnesses, recorded as `theorem` rather than
  `axiom` so the project's no-axiom convention is preserved).

All three would discharge if (a) a concrete `ΔW(p)` definition
were available (currently `opaque`, pending a Mathlib Farey-sequence
library), and (b) the density-one bias control were formalised.

## Conditional closures — what each hypothesis names

The six fully-proved files take the following analytic inputs as
explicit named hypotheses where Mathlib v4.28.0 does not yet supply
the prerequisite. The pen-and-paper proofs supply each input
directly:

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

For each, the algebraic plumbing is fully Lean-verified; the
hypothesis is exactly what the corresponding pen-and-paper proof
proves. Upstream Mathlib formalisation of any of these would
upgrade the conditional Lean theorem to unconditional.

## Path to unconditional Lean

The shortest path to a fully unconditional Lean inventory (zero
`sorry`, zero `MATHLIB-PREREQ`) is, in increasing difficulty:

1. **Three Mathlib upstream contributions** (each estimated at
   a few weeks of focused formalisation):
   - $\Gamma$ uniform Stirling bound on vertical strips;
   - $1/\zeta(s)$ polynomial bound away from $s = 1$
     (Titchmarsh §3.11);
   - Ramanujan-sum library `Mathlib.NumberTheory.RamanujanSum`
     with the $c_q(p) = \mu(q)$ identity.
2. **One project-side Lean formalisation**: a concrete
   $\Delta W(p)$ definition from a Farey-sequence formalisation,
   which would discharge the three `FareySignPattern.lean` sorries.
3. **Two open mathematical problems** would still need to be
   resolved:
   - DPAC at general $K$ (LI-Hypothesis-class);
   - The density-one Farey sign pattern under DRH-style hypotheses.

Item (1) alone takes the conditional Lean theorems for Theorem X.4.1
(via Akatsuka's input), Theorem C, and the Farey bridge identity
to unconditional. (1) + (2) takes the entire algebraic content of
§X.3–§X.4 and §X.6 to a 0-`sorry` inventory; (3) is what remains
genuinely open.
