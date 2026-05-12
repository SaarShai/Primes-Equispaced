/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

# Corrected `B_∞` identity (Theorem X.4.1 of the Saar–Koyama paper)

For a primitive non-principal Dirichlet character `χ` of conductor
`q`, a simple noncentral zero `ρ = ½ + iτ` of `L(s, χ)` on the
critical line, and the primitive character `ψ` of conductor `f ∣ q`
inducing `χ²`,

    T_∞(χ, ρ) = ½ · log L(2ρ, ψ) + BPC₁(χ, ρ) + BPC₂(χ, ρ) + T_{≥3}(χ, ρ).

The four right-hand-side components are defined below.  The identity
is *unconditional* given simplicity of `ρ`.  Full pen-and-paper proof
in Appendix A of the joint manuscript
(`APPENDIX_A_BINFTY_PROOF.md`).

In this Lean file we:

* Parametrize a Dirichlet character as a function `chi : ℕ → ℂ`
  zero outside `(ℤ / q)ˣ`. We do **not** use Mathlib's
  `DirichletCharacter` namespace at v4.28.0 directly because the
  API for `IsPrimitive`, `induce`, and `LFunction` has been moving
  across releases; restating in terms of basic functions of
  `ℕ → ℂ` keeps this file `lake build`-stable.

* Define the four components as `noncomputable` partial-sum limits.

* State the identity as a theorem with proof `sorry` (research-open
  Lean obligation; pen-and-paper proof is in Appendix A).
-/

import Mathlib

namespace CorrectedBInfty

open Complex BigOperators

/-- A "Dirichlet-style character", parametrised by an arbitrary
function `ℕ → ℂ`.  Mathlib's `DirichletCharacter` could be used
once its API stabilises across v4.28.0+; for now we keep the file
self-contained. -/
abbrev DChar := ℕ → ℂ

/-- The partial prime-power tail
`T_K(chi, ρ) := Σ_{p ≤ K, p prime} Σ_{k ≥ 2} chi(p)^k / (k · p^(k ρ))`.

The inner `k`-sum has the per-prime closed form
`-log(1 - z) - z` where `z := chi(p) / p^ρ`. -/
noncomputable def T_K (chi : DChar) (ρ : ℂ) (K : ℕ) : ℂ :=
  ∑ p ∈ Finset.filter Nat.Prime (Finset.range (K + 1)),
      let z : ℂ := chi p / (p : ℂ) ^ ρ
      -Complex.log (1 - z) - z

/-- `T_∞(chi, ρ)` is the limit of `T_K(chi, ρ)` as `K → ∞`.
The existence of the limit is part of the Theorem X.4.1 statement;
proof is in Appendix A §A.2–A.4 of the joint manuscript. -/
noncomputable def T_inf (chi : DChar) (ρ : ℂ) : ℂ :=
  Classical.epsilon (fun (S : ℂ) =>
    Filter.Tendsto (T_K chi ρ) Filter.atTop (nhds S))

/-- The absolutely convergent `k ≥ 3` tail
`T_{≥3}(chi, ρ) := Σ_p [-log(1 - z_p) - z_p - z_p² / 2]`,
where `z_p := chi(p) / p^ρ`. -/
noncomputable def T_ge3 (chi : DChar) (ρ : ℂ) : ℂ :=
  ∑' p : { n : ℕ // Nat.Prime n },
      let z : ℂ := chi p.val / (p.val : ℂ) ^ ρ
      -Complex.log (1 - z) - z - z ^ 2 / 2

/-- The bad-prime correction `BPC₁`: for each prime `p` dividing the
conductor `q` of `chi` but *not* dividing the conductor `f` of the
primitive character `psi` inducing `chi²`,

    BPC₁ contributes  ½ · log(1 - psi(p) · p^(-2ρ)).
-/
noncomputable def BPC_1 (psi : DChar) (q f : ℕ) (ρ : ℂ) : ℂ :=
  (1 / 2 : ℂ) *
    ∑ p ∈ Finset.filter
        (fun p => Nat.Prime p ∧ q % p = 0 ∧ f % p ≠ 0)
        (Finset.range (q + 1)),
      Complex.log (1 - psi p / (p : ℂ) ^ (2 * ρ))

/-- The k ≥ 2 BPC₂ residue from the log-Euler-product expansion:

    BPC₂(chi, ρ) := (½) · Σ_p [log(1 - y_p) + y_p],
    where  y_p := chi(p)² / p^(2 ρ).
-/
noncomputable def BPC_2 (chi : DChar) (ρ : ℂ) : ℂ :=
  (1 / 2 : ℂ) *
    ∑' p : { n : ℕ // Nat.Prime n },
        let y : ℂ := (chi p.val) ^ 2 / (p.val : ℂ) ^ (2 * ρ)
        Complex.log (1 - y) + y

/-- `L(s, psi)` for the simple-character primitive `psi` modulo `f`.
We define the L-value via the Dirichlet series in its half-plane of
convergence; for `Re(s) > 1` this converges absolutely.  Analytic
continuation is needed for the boundary line `Re(s) = 1`, which is
provided in the manuscript via Akatsuka 2013, eq. (2.5). -/
noncomputable def L_value (psi : DChar) (s : ℂ) : ℂ :=
  ∑' n : ℕ, psi n / (n : ℂ) ^ s

/--
**Theorem X.4.1 (Corrected `B_∞` identity).**

For `chi` a primitive non-principal Dirichlet character of conductor
`q ≥ 2`, simple noncentral zero `ρ = ½ + iτ` of `L(·, chi)`, and `psi`
the primitive character of conductor `f ∣ q` inducing `chi²`:

    T_∞(chi, ρ) = ½ · log L(2ρ, psi) + BPC₁ + BPC₂ + T_{≥3}.

The statement is *unconditional*.  The pen-and-paper proof is in
Appendix A of the joint manuscript.  The Lean proof requires:

* Akatsuka 2013, eq. (2.5), to handle the boundary-line conditional
  convergence of `Σ_p chi(p)² / p^(2ρ)` at `Re(2ρ) = 1` — this is the
  *only* analytic input.
* Standard textbook tools (Taylor expansion of `-log(1 - z)`, the
  imprimitive-induction Euler-factor identity, geometric-series tail
  bounds for absolute convergence).

None of these are yet in Mathlib v4.28.0 in the precise form needed
for an automated proof of `corrected_B_infty`. We therefore leave
the Lean proof as `sorry` with a *research-open* annotation pointing
to the manuscript's Appendix A.

`MATHLIB-PREREQ`: a quantitative version of the Mertens-type
boundary-line estimate `∑_{p ≤ X} χ²(p) / p^(1 + 2iτ) = c(τ) + O(1/log X)`
(Akatsuka 2013, eq. (2.5)) or the equivalent Dirichlet PNT with
explicit error term.
-/
@[category research_open]
theorem corrected_B_infty
    (chi : DChar) (psi : DChar) (q f : ℕ) (ρ : ℂ)
    (hq : 2 ≤ q) (hf : f ∣ q)
    -- The character `psi` induces `chi²` modulo `q`:
    (h_induces : ∀ n : ℕ, Nat.Coprime n q → (chi n) ^ 2 = psi n)
    -- ρ is on the critical line, not central:
    (h_rho_re : ρ.re = 1 / 2) (h_rho_im : ρ.im ≠ 0) :
    T_inf chi ρ
      = (1 / 2 : ℂ) * Complex.log (L_value psi (2 * ρ))
        + BPC_1 psi q f ρ
        + BPC_2 chi ρ
        + T_ge3 chi ρ := by
  -- MATHLIB-PREREQ: Akatsuka 2013 eq. (2.5) for the boundary-line
  -- convergence of `Σ_p chi²(p) / p^(2ρ)` on `Re(s) = 1, s ≠ 1`.
  -- Pen-and-paper proof in Appendix A of the joint manuscript.
  sorry

end CorrectedBInfty
