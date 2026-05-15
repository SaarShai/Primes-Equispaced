---
schema_version: 2
title: "H1 Numerator M_T Audit (Stage 1b of Halo Plan, Door D)"
type: audit
domain: project
tier: working
status: PASS
confidence: 0.85
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_CONTOUR_SHIFT_THEOREM.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-breakthrough-proof-wave/H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
supersedes: []
superseded-by:
tags: [halo-route, door-D, numerator-audit, M_T, h1, stage-1b]
---

# Stage 1b — Numerator Audit (Door D)

## Verdict

```text
PASS.
```

For exact `Phi_T` of H1 finite-box identity, with smoothstep kernel
(`q=2`) and admissible contour truncation `T(u) >> e^{sigma u}`
(`sigma > 1/2` — already required by Perron start-line; see
`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` L137-138, L167-169),

```text
M_T := sup_{s in partial Omega_T} |Phi_T(s)|
     <= C T^{-q} e^{O(u/log T)}
     <= C T^{-2} · O(1)
     =  O(T^{-2}).
```

This is far below halo theorem's loose requirement `M_T = o(T^{1/4})`
and even below tight `T^{o(1)}` form. Margin: `T^{2 + 1/4} = T^{9/4}`.

Binding constraint: H1 truncation must be at least exponential in `u`,
`T(u) >= e^{sigma u}` with some `sigma > 0`. Repo H1 already requires
this for an unrelated reason (Perron start-line absolute convergence).
**Door D is bound by a constraint H1 already pays for.**

The 0.10 residual risk from Stage 0 (silent termwise use of `|R_rho|`
downstream) is **RETIRED** — see §8.

## Phi_T Identification

Anchor: `H1_RESIDUE_CONTROL_SYNTHESIS_2026-05-11.md` L48-79,
`H1_POSITIVE_RANK_CLOSURE.md` L77-104, halo plan §2.1 L102-141.

Repo finite-box identity (residue-control synthesis L48-56):

```text
c_{E,W}(e^u) = Q_{E,W}(u)
             + sum_{rho != 1, |Im rho| < T} R_rho(u)
             + vertical/horizontal/truncation errors.
```

Simple-zero residue (positive-rank closure L102-104):

```text
R_rho(u) = e^{i gamma u} W_hat(i gamma) / L'(E, 1 + i gamma),
rho = 1 + i gamma.
```

Halo plan §2.1 (L108-141) writes the same aggregate as a single contour
integral

```text
R_Phi(T) := sum_{rho in Z_T^red} Res_{s=rho} Phi_T(s)/L(s)
          = (1/(2 pi i)) int_{partial Omega_T} Phi_T(s)/L(s) ds.
```

Match residues at simple zero: `Res_{s=rho} Phi_T(s)/L(s) = Phi_T(rho)/L'(rho)`
must equal `e^{i gamma u} W_hat(i gamma)/L'(rho)`. Therefore

```text
Phi_T(s) = e^{u(s-1)} W_hat(s-1).
```

Shifted variable: write `z = s - 1`. Critical line `Re s = 1` becomes
`Re z = 0`; offcentral zeros `rho = 1 + i gamma` become `z = i gamma`;
the kernel evaluation is at `z`, not `s`. The repo's H1 object literally
*is* `c_{E,W}(e^u) = (1/2 pi i) int e^{uz} W_hat(z)/L(E, 1+z) dz`
(`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` L24-25). Match.

Parameter conflations (logged):

| Symbol | Halo plan usage | H1 statement usage | Reconciliation |
|---|---|---|---|
| `T` | dyadic shell height `T<|gamma|<=2T` | contour truncation `|Im rho|<T` | same `T` in dyadic decomposition of finite-box |
| `u` | implicit, fixed while `T->infinity` | `u = log K`, primary variable | halo theorem applied at one `u` per truncation level; admissible schedule pairs `T = T(u)` |
| `Phi_T(s)` | numerator on `Omega_T` boundary | `e^{uz} W_hat(z)` after shift | `Phi_T(s) = e^{u(s-1)} W_hat(s-1)` |

No mismatch. Identification holds.

## Halo Geometry

Anchor: halo plan §2.1 L102-107 and §5.1 L251-303.

```text
alpha = 1/log T,
R_T in [R, 2R],     R > sqrt(1+A^2)   (Door B uses this R; we use same R),
Omega_T = union_{rho in Z_T^red} D(rho, R_T alpha).
```

For `s in partial Omega_T` on the arc assigned to `rho_0 = 1 + i gamma_0`,
`|gamma_0| in (T, 2T]`:

```text
s = rho_0 + R_T alpha e^{i theta},     theta in [0, 2 pi),
s - 1 = i gamma_0 + R_T alpha e^{i theta}.
```

Decompose `s - 1 = i gamma_0 + epsilon` with `epsilon = R_T alpha e^{i theta}`:

```text
Re(s-1) = R_T alpha cos theta        in [-R_T alpha, R_T alpha],
Im(s-1) = gamma_0 + R_T alpha sin theta,
|epsilon| = R_T alpha <= 2 R/log T   = O(1/log T).
```

Since `R = O(1)` (R depends on the fixed cluster parameter A only):
`|epsilon| = O(1/log T)`.

## Computation of |Phi_T|

```text
|Phi_T(s)| = |e^{u(s-1)}| · |W_hat(s-1)|.
```

**Exponential factor.**

```text
|e^{u(s-1)}| = e^{u · Re(s-1)} = e^{u · R_T alpha cos theta}.
sup over theta:  e^{u R_T alpha}  =  e^{u · (2R/log T)}  =  e^{2R u/log T}.
```

So `|e^{u(s-1)}| <= e^{2R u/log T}`. The `Im(s-1) = gamma_0 + O(1/log T)`
contributes only a unit-modulus phase `e^{i u Im(s-1)}` (sanity: critical
line `Re(s-1) = 0` would give pure phase). No growth from `Im`.

**Kernel factor.** Repo kernel decay (`H1_BREAKTHROUGH_PROOF_SYNTHESIS_2026-05-11.md`
L99-126, also `H1_POSITIVE_RANK_CLOSURE.md` L173-178):

```text
|W_hat(i t)| <= C (1+|t|)^{-q},     q = 2 for smoothstep.
```

Extend to a thin neighborhood of imaginary axis. Repo kernel is
Paley-Wiener / smoothstep with compactly supported logarithmic Mellin
data, so `W_hat(z)` is holomorphic on a strip and the decay `(1+|Im z|)^{-q}`
holds uniformly for `|Re z| <= sigma_0` (some fixed strip half-width). For
`s in partial Omega_T`, `|Re(s-1)| <= R_T alpha = O(1/log T) -> 0`, well
inside any fixed strip. Therefore

```text
|W_hat(s-1)| = |W_hat(i gamma_0 + epsilon)|
            <= C (1 + |gamma_0 + Im epsilon|)^{-q}
            <= C (1 + |gamma_0|/2)^{-q}     for T large enough that
                                            |Im epsilon| = O(1/log T) < |gamma_0|/2
            <= C' T^{-q}.
```

(`|gamma_0| > T`, so `(1+|gamma_0|)^{-q} <= C T^{-q}`.)

**Combine.**

```text
M_T = sup_{s in partial Omega_T} |Phi_T(s)|
   <= C' T^{-q} · e^{2R u/log T}.                    (*)
```

For smoothstep `q = 2`:

```text
M_T  <=  C' T^{-2} · e^{2R u/log T}.                 (**)
```

## Regime Table

The exponential factor `e^{2R u/log T}` is the regime-sensitive piece.
Let `lambda := u/log T`. Then `M_T <= C' T^{-q} e^{2R lambda}`.

Door D demands `M_T = o(T^{1/4})`. With `q = 2` the bound is `T^{-2}
e^{2R lambda}`, so demand `e^{2R lambda} = o(T^{1/4 + 2}) = o(T^{9/4})`,
i.e.

```text
2 R lambda  <  (9/4 - o(1)) log T,
lambda < (9/(8R)) - o(1).
```

For `R = sqrt(1+A^2)` with `A = O(1)` (cluster constant from Door B),
`R = O(1)`, so the requirement is `lambda <= C_R` for some constant — a
**bounded** ratio `u/log T`.

| Truncation `T(u)` | `lambda = u/log T` | `M_T` bound (q=2) | Door D verdict |
|---|---|---|---|
| `T = e^{c u}`, c > 0 fixed (exponential) | `1/c` = O(1) | `T^{-2} · e^{2R/c}` = `O(T^{-2})` | **PASS** (margin `T^{9/4}`) |
| `T = u^A`, A > 0 (polynomial) | `u/(A log u) -> infty` | `T^{-2} · e^{u/(A log u)}` | **FAIL** — `e^{u/(A log u)}` beats every polynomial in `u`; needs check vs `T^{9/4} = u^{9A/4}` (polynomial in u). Quasi-polynomial beats polynomial. |
| `T = e^{(log u)^B}`, B > 1 (intermediate) | `u/(log u)^B -> infty` slowly | borderline `e^{u/(log u)^B}` vs `T^{9/4} = e^{(9B/4)(log u)^B}` | needs `u/(log u)^B < (9/4 - eps)(log u)^B`, i.e. `u < (log u)^{2B}`, **FAIL** for any B (since u grows faster than any (log u)^k). |
| `T = e^{c u^delta}`, 0 < delta < 1 | `u^{1-delta}/c -> infty` | `T^{-2} · e^{(2R/c) u^{1-delta}}` vs `T^{9/4} = e^{(9c/4) u^delta}` | **FAIL** iff `1-delta > delta`, i.e. delta < 1/2. **PASS** if delta >= 1/2 + eps (then u^{1-delta} grows slower than u^delta · log-factor). Borderline. |

Conclusion: only truncation regimes `log T(u) >= sigma u` (i.e.
**linear-or-faster in u**) give the bounded-`lambda` regime needed for
PASS by a comfortable margin. All sub-linear-log regimes (polynomial,
sub-exponential with delta < 1/2) fail.

The threshold is exactly the same as the regime needed for
original-line truncation tail (`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md`
L163, L169): `e^{sigma u} T(u)^{1-q} = o(u^r)` with `q = 2` requires
`T(u) >> e^{sigma u}`.

## Repo H1 Statement Consistency Check

Anchor: `H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` L130-172.

```text
"The safe absolute-convergence start is sigma > 1/2 using the usual
 Hasse-size input." (L137-138)
```

Start-line `Re z = sigma > 1/2` forces the original-line truncation
tail bound

```text
|I_sigma(infty,u) - I_sigma(T,u)| <= C e^{sigma u} T^{1-q}.   (L154-157)
```

For smoothstep `q = 2` and any nontrivial `o(u^r)` tail requirement, this
forces (L169):

```text
T(u) >> e^{sigma u} u^{-r} · (diverging factor).
```

So `log T(u) >= sigma u - r log u + omega(1)`, i.e. `lambda = u/log T(u)
<= 1/sigma + o(1) = 2 - eps` (since `sigma > 1/2`, so `1/sigma < 2`).

Plug into halo bound (**):

```text
M_T <= C' T^{-2} · e^{2R · (1/sigma + o(1))}
    = C' T^{-2} · O(1)
    = O(T^{-2}).
```

The repo's H1 truncation regime is **forced exponential by the start-line
tail constraint** (which the repo already takes on board, see
H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md L130-138 "promote only on an
absolute-convergence start line"). Door D's regime requirement is
**automatically inherited**. No new constraint imposed by halo route.

This is a strong consistency check: the halo route does not enlarge the
admissible truncation schedule beyond what the H1 base proof already
needs.

## Recommendation

```text
H1 truncation schedule: log T(u) >= sigma u, sigma > 1/2.
Concretely: T(u) = e^{u}, T(u) = e^{2u}, or any T = e^{c u} with c > 0.

Concrete optimal c: c = 1 (i.e., T = e^u) suffices.
- Start-line tail (q=2):   e^{sigma u} T^{1-q} = e^{sigma u} T^{-1}
                            = e^{(sigma - 1) u} = o(1) for sigma < 1.
                            Choose 1/2 < sigma < 1.
- Door D:                   lambda = u/log T = 1/c = 1, M_T <= O(T^{-2}).

Pin in subsequent Stage-2 / Stage-3 source-closure work:
"T(u) = e^{c u} with 1/2 < c, e.g. c = 1".
```

Pinning this `c` once and for all removes ambiguity from the halo theorem
statement and from any future numerator audit.

## Residual Risk From Stage 0 — Retirement

Stage 0's residual 0.10 risk (`H1_RESIDUE_FIRST_AUDIT_2026-05-14.md`
L201-211):

```text
0.10  some downstream step we have not yet identified silently uses
      |R_rho| termwise (e.g., uniform-in-u argument in the contour
      truncation error analysis).
```

Trace: the only place `|R_rho|` appears in the truncation error analysis
is the start-line tail (`H1_CONTOUR_TAIL_HEIGHT_AVOIDANCE.md` L154-172)
and the horizontal edge bound (L186-188). Both are bounds on the
*contour integral* directly:

```text
start-line tail:     |int_{|Im z|>T, Re z=sigma} e^{uz} W_hat(z)/L(...) dz|
                     <= e^{sigma u} int_T^infty |W_hat(sigma+it)/L(...)| dt.
horizontal edge:     |int_{Im z=+- T} ...| <= (sigma+eta) e^{sigma u}
                                            (1+T)^{-q} M(T).
```

Both contour bounds use `triangle inequality on the integral` —
NOT termwise on a sum of residues. The signed identity is preserved
because the residue sum is *expressed* as a closed contour integral
boundary; the inequality is applied to one integrand on one path, not
to individual residues.

Therefore: even the truncation-error half of the H1 statement uses the
contour integrand `|e^{uz} W_hat(z) / L(z)|` on a *path*, not `|R_rho|`
on *zeros*. The contour identity itself is signed.

```text
Residual risk RETIRED.  Stage 0 confidence raises from 0.86 to ~0.94.
```

The remaining 0.06 covers the meta-risk that the H1 statement under
proof is materially different from the residue-control-synthesis
statement audited — unfixable until the final paper assembles.

## Caveats

```text
1. Kernel order q. Result uses q = 2 (smoothstep). If a different
   W is selected later (e.g., Gevrey/Beurling for stronger decay),
   recompute M_T with new q. Bound becomes M_T <= C' T^{-q} e^{O(u/log T)};
   PASS margin is q + 1/4 powers of T.

2. e^{i gamma u} on critical line. For s exactly on critical line,
   Re(s-1) = 0, so |e^{u(s-1)}| = 1. The growth e^{2R u/log T} comes
   entirely from the halo's O(1/log T) excursion off the critical
   line. Halo radius R = sqrt(1+A^2) is fixed (Door B), so the
   constant 2R = 2 sqrt(1+A^2) is harmless.

3. Multiple-zero residues. For rho of multiplicity m, residue is
   e^{i gamma u} P_rho(u) with deg P_rho <= m-1. P_rho(u) is a sum
   of derivatives of Phi_T at rho. d^k/ds^k (e^{u(s-1)} W_hat(s-1))
   = sum_j (k choose j) u^j e^{u(s-1)} W_hat^{(k-j)}(s-1). Each
   W_hat^{(j)} satisfies its own (1+|t|)^{-q_j} decay
   (positive-rank closure L221-227). Bounded multiplicity M
   (Riemann-von Mangoldt: M <= O(log T) at offcentral height),
   finitely many derivatives, so M_T inflates by polylog and u^M
   factor. With u <= log T/sigma and M = O(log T), worst case
   u^M = e^{O((log T)^2)} — does NOT preserve M_T = O(T^{-q}).
   This is a SEPARATE multiple-zero numerator audit; for simple
   zeros and the bounded-M case standard at fixed-conductor GL2,
   the bound (**) holds with at most polylog inflation. Stage 4
   of the halo plan (multiplicity-aware BFMT) handles this.

4. Constant R. R > sqrt(1+A^2). For the repo's standing A (cluster
   parameter), pin R = 2 (safe for any A < sqrt(3)). The constant
   2R in the exponent is 4. With c = 1 (T = e^u), e^{2R/c} = e^4,
   absolute constant. No T or u dependence.

5. Lower-deck strip width. Step from |W_hat(it)| <= C(1+|t|)^{-q}
   to |W_hat(eps + it)| <= C'(1+|t|)^{-q} for |eps| small uses
   that the smoothstep kernel is Paley-Wiener (holomorphic on a
   strip with the same decay). Verify in kernel construction for
   the chosen W; this is asserted in the repo for all relevant
   kernels but the explicit strip width should be documented in
   the final paper.
```

## Boundary

Allowed to claim now:

```text
For exact Phi_T(s) = e^{u(s-1)} W_hat(s-1) of repo H1 finite-box
identity, with smoothstep kernel (q=2) and admissible H1 truncation
T(u) = e^{c u} (c > 0, already required by Perron start-line), the
halo numerator obeys M_T = O(T^{-2}). Door D PASS with margin T^{9/4}.

For simple zeros only, this bound is uniform in T and saturates the
halo theorem's loose o(T^{1/4}) requirement with two-plus orders to
spare. Bounded-multiplicity case inflates by polylog only.

Stage 0 residual risk (silent termwise |R_rho|) retired: H1
truncation error analysis uses contour-integrand inequalities, not
termwise residue bounds.
```

Not allowed to claim:

```text
M_T = T^{o(1)} unconditionally without specifying the truncation
regime. (Polynomial T(u) regime FAILS.)

Unbounded-multiplicity offcentral case is bounded. (Needs Stage 4
multiplicity audit.)

The halo theorem is unconditionally proved. (Door A still open.)

The numerator bound is sharp. (We use loose sup; true peak of
|Phi_T| on partial Omega_T may be much smaller, but loose bound
already suffices.)
```

## Boundary Marker

Confidence breakdown:

```text
0.85  M_T = O(T^{-2}) for smoothstep, simple zeros, T(u) = e^{c u}
0.10  multiple-zero polylog inflation matters more than claimed
      (deferred to Stage 4)
0.05  the H1 statement under proof uses a non-smoothstep kernel
      with different q, or a different Phi_T encoding
```
