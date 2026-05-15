# Halo-Residue Route — Documentation and Unconditional Plan

Created: 2026-05-12
Status: synthesis of the original packet `handoff pro.md` and the halo-residue
handoff `H1_Palm_Wall_Halo_Handoff_2026-05-12.md`; new staged plan toward an
**unconditional** proof of the offcentral H1 residue contribution `= o(T^2)`.

This file is intended as the single anchor a continuation agent or auditor
should read after `handoff pro.md`. It records:

1. What the original wall was.
2. The chain of reductions in the halo handoff.
3. Why the halo theorem is a genuine structural bypass, not a Palm proof.
4. The exact remaining conditional doors.
5. A new staged plan, with primary and fallback paths, to close each door
   unconditionally for a fixed elliptic curve / GL2 newform.
6. Novel angles not yet tried (rectangle contour, mollified second moment,
   Heap-Soundararajan transfer, density-method).

Notation throughout: `L(s) = L_E^*(s) = L(E,s+1/2)`, `alpha = 1/log T`,
`X(rho) = |L(rho+alpha)|^{-1}`, dyadic shell `S_E(T) = {rho = 1/2+i gamma :
T < |gamma| <= 2T}`.

---

## 1. Original wall (from `handoff pro.md`)

Reducing simple-zero H1 down to a positive `l^1` budget on reciprocal
derivatives:

```text
R_B(T,c) = sum_{rho bad simple} |L'(rho)|^{-1}.
```

The packet's local cluster-shift comparison gives, conditionally on the
existing local noncluster stability theorem,

```text
|L'(rho0)|^{-1}
 <= T^{o(1)} alpha W_A(rho0) X(rho0),
```

where the **cluster weight**

```text
W_A(rho0)
 = prod_{rho_j in C_A(rho0)\{rho0}}
     |alpha+rho0-rho_j| / |rho0-rho_j|
```

is an inverse-product weight on the close-cluster mates. Hölder with
conjugate exponents `q, p = q/(q-1)` then gives the criterion

```text
mu_q/q + nu_p/p < 2,
```

with natural targets

```text
mu_q = q + 1/2,    nu_p = 1.
```

The cheapest target is `q=3, p=3/2`, giving `R_B << T^{11/6+eps}`. The two
remaining source-closing inputs are:

- `Degree2WeakShiftedNeg_3(E)` — a shifted negative `q=3` moment over zeros.
- `RootedInvProdCorr_p(E,A)` with `p=3/2` — a rooted Palm box law / inverse
  product cluster integrability for fixed GL2/EC.

The latter is the **rooted Palm wall**. Every checked source (small-gap
existence, n-level density with bounded support, density-one simplicity,
finite-M truncation) failed to produce uniform shrinking-box repulsion with
summable cluster constants. This is what was meant by "narrowed, not broken".

---

## 2. Halo handoff — the structural pivot

The key observation in `H1_Palm_Wall_Halo_Handoff_2026-05-12.md`:

> The inverse-product weight `W_A` is created by taking absolute values
> zero-by-zero. The actual contour residue contribution is a signed/complex
> sum, in which residues inside a close cluster cancel as divided
> differences.

Concretely, for a cluster `C = {rho_1,...,rho_n}`,

```text
sum_{rho in C} Res_{s=rho} Phi_T(s)/L(s)
 = [rho_1,...,rho_n] (Phi_T / H_C)
```

is the divided difference of `Phi_T / H_C` at the cluster nodes. Individual
reciprocal derivatives blow up like `1/|a-b|` as two zeros collide; the
cluster-summed divided difference stays bounded by a derivative.

**Therefore**: if the H1 proof actually only needs the signed contour
residue contribution, not its termwise absolute value, the rooted Palm wall
is an artifact of taking absolute values too early.

### 2.1 The halo theorem (final form)

Let `Z_T` be the offcentral zeros in a dyadic shell of size `~T`. Choose a
halo radius `R_T in [R, 2R]` (`R > 1` fixed) so that no zero lies on the
boundary of `Omega_T = union_{rho in Z_T^red} D(rho, R_T alpha)`. Then

```text
R_Phi(T) := sum_{rho in Z_T^red} Res_{s=rho} Phi_T(s)/L(s)
         = (1/(2pi i)) int_{partial Omega_T} Phi_T(s)/L(s) ds.
```

Conditional on a **halo shift comparison**

```text
HaloShiftComparison(E,A,R):
 |L(s)|^{-1} <= T^{o(1)} |L(rho+alpha)|^{-1}
 on every halo arc assigned to rho,
```

charging boundary length to halo circles gives

```text
int |L|^{-1} |ds|  <<  T^{o(1)} alpha sum_{rho} X(rho).
```

Cauchy-Schwarz, with `#Z_T^{mult} << T log T` and `q=2` shifted moment
input

```text
sum_{rho}^{mult} X(rho)^2 << T^{5/2+eps},
```

yields

```text
|R_Phi(T)|  <<  M_T T^{7/4+eps+o(1)},
```

where `M_T = sup_halo |Phi_T|`. If `M_T = o(T^{1/4})` then
`R_Phi(T) = o(T^2)`. In particular `M_T = T^{o(1)}` is enough.

### 2.2 What this kills, what it does not

- **Killed**: the rooted Palm wall *as a necessary input to the H1 contour
  contribution*. No `W_A`, no rooted box law, no n-level density obstruction.
- **Not killed**: the *positive* budget `R_B(T,c) = sum |L'(rho)|^{-1}`.
  A deterministic two-zero gadget (`F_delta(s) = (s-a)(s-a-delta)H(s)`,
  `delta -> 0`) shows `R_B` is genuinely larger than the signed residue
  sum, by an arbitrary amount. So Palm-style information is still required
  if one ever tries to prove `R_B = o(T^2)` directly.

---

## 3. Full reduction trail (chronological in the handoff)

For completeness, here is every reduction in the halo handoff, ordered.

### 3.1 Supercritical Palm Spike (SRPS_q)

Only roots with `W_A(rho) > T^{eta_q - sigma}` matter for Hölder, where
`eta_q = 1/(2q)`. Moderate clusters are killed by sheer size. **Reduction**:
need only

```text
sum_{rho : W_A(rho) > T^{eta_q - sigma}} W_A(rho)^p << T^{theta_q - delta+eps}.
```

### 3.2 Correlated Double Spike (CDS_q)

The summand is `W_A · X`, so even large `W_A` is harmless when `X` is small.
**Reduction**: need only joint spike

```text
sum_{rho : W_A > T^{eta_q-tau}, W_A X > T^{1-sigma}} W_A^p
   << T^{theta_q - delta + eps}.
```

### 3.3 Dyadic lower-moment knife

On a dyadic bin `U < W_A <= 2U`, Markov with a shifted moment of order `r`
controls the joint spike when `U` is below a threshold. With `r=2`,
`mu_2 = 5/2`, q=3 double spikes are controlled up to `W_A <= T^{3/14-o(1)}`.
With hypothetical `r=1`, `mu_1 = 3/2`, control extends to
`W_A <= T^{3/10-o(1)}`. The Palm wall after this reduction is only the
**ultra-tail** `W_A > T^{3/14}`.

### 3.4 Cluster-resummed finite-box module (Section 6)

Group close residues into cluster boxes `Q` before taking absolute values:

```text
B_Phi(T) = sum_Q | sum_{rho in Z_Q} Res Phi_T/L |.
```

Under local Cauchy/stability, gives `<< M_T T^{7/4+o(1)}` with q=2 shifted
samples. But still required careful local contour hypotheses per cluster.

### 3.5 Global thin rectangle (Section 7)

A single contour:

```text
1/2-alpha <= Re s <= 1/2+alpha,   T <= Im s <= 2T.
```

Then `sum residues = (1/2pi i) int_{boundary} Phi_T/L ds`. Reduces the
problem to a **continuous** shifted negative moment

```text
ContShiftNeg_q(E):
  int_T^{2T} |L(1/2+alpha+it)|^{-q} dt  <<  T^{q+1/2+eps}.
```

For q=2 this would give `<< M_T T^{7/4+o(1)}`. Clean — but moved the gap
to a different unproved object.

### 3.6 Halo-resummed q=2 (Section 8 — current best)

Replaces the global rectangle with a *union of disks* around the actual
zeros. The boundary length is `O(alpha · #zeros)` automatically. Uses the
already packet-aligned **zero-sampled q=2** moment instead of a continuous
moment.

---

## 4. Remaining conditional doors (verbatim from the handoff)

```text
Door A: AllZeroShiftedNeg_2(E)
        sum_{rho}^{mult} |L(rho+alpha)|^{-2} << T^{5/2+eps}
        (or: simple-zero version + multiple-zero disposition)

Door B: HaloShiftComparison(E,A,R)
        |L(s)|^{-1} <= T^{o(1)} |L(rho+alpha)|^{-1}
        on every halo arc assigned to rho

Door C: ResidueFirstH1Rewrite
        identify the H1 step where R_B is used and replace by the
        signed contour residue contribution

Door D: M_T = o(T^{1/4})  (preferably T^{o(1)})
```

This is the *complete* current ledger.

---

## 5. Door-by-door audit — what each one really demands

### 5.1 Door B is unconditional (under the framework's GRH) with `R > √(1+A²)`

**THEOREM (HaloShiftComparison_clean).** Under the framework's standing
assumption that zeros of `L_E^*` lie on the critical line, let `A > 0` be
fixed, and choose halo radius parameter `R > √(1+A²)`. Then for every
boundary arc `s ∈ ∂Ω_T` assigned to `ρ_0`,

```text
|L(ρ_0 + α)| / |L(s)|  ≤  C(E, A, R) ,
```

with `C(E, A, R)` an absolute constant independent of `T` and of the local
cluster size `N_{ρ_0, A}(T)`.

**Proof sketch.** Factor `L(s) = (s-ρ_0) ∏_{ρ_j ∈ C_A(ρ_0)\{ρ_0}}(s-ρ_j)
H_A(s)`.

*Self.* `|α/(s-ρ_0)| = 1/R_T < 1`. ✓

*Cluster mates.* For each cluster mate `ρ_j`, under GRH
`|γ_j - γ_0| ≤ A α`, so

```text
|ρ_0 + α - ρ_j|² = α² + (γ_0 - γ_j)² ≤ α²(1+A²) .
```

Since `s ∈ ∂Ω_T` is by definition outside every other halo,
`|s - ρ_j| ≥ R_T α`. So per cluster mate

```text
|ρ_0+α - ρ_j|/|s - ρ_j| ≤ √(1+A²)/R_T < 1 ,
```

and the product over the *entire* cluster — of arbitrary size — is `≤ 1`.
**No local zero-count input is needed.**

*Non-cluster (`H_A`).* Both `ρ_0+α` and `s` lie within distance `O(α)` of
`ρ_0` in the cluster-free region. The existing repo lemma
`ClusterShiftDerivativeComparison(E,A)` controls
`|H_A(ρ_0+α)/H_A(ρ_0)| = O(1)`. Lift from point evaluation to a disk of
radius `R α`: by `log|H_A|` harmonic on the cluster-free region, its
variation is bounded by the same sum `Σ (α/d_j)²` over non-cluster zeros,
which equals `1/(2π A) + o(1)` by Riemann–von Mangoldt. ✓

Combining: `|L(ρ_0+α)/L(s)| ≤ (1/R_T) · 1 · O(1) = O(1)`. QED.

**Significance.** The handoff (§13.B, §15.1) flagged Door B as the most
delicate of the four because the naïve factorization argument yielded
`C_A^{N_{ρ_0,A}(T)}`, requiring uniform `N_{ρ_0,A} = o(log T)`. The
geometric observation — that boundary-arc points are *forced* outside
every other halo by the definition of `∂Ω_T` — turns the cluster ratio
into a *contraction* of arbitrary order. Door B is no longer an audit
risk; it is bounded by an absolute constant.

This also tightens the halo theorem's exponent statement: replace
`T^{o(1)}` by `O(1)` in the per-arc bound. No exponent change downstream,
but it removes an apparent ambiguity in the existing statement.

### 5.1' Original conservative statement of Door B (for archival)

The handoff's original Door B route. Choose `R > A+1`. Then for any
boundary arc:

(i) For every other zero `rho_j in Z_T^red`, since `s` is outside
`D(rho_j, R_T alpha)`,

```text
|s - rho_j| >= R_T alpha >= R alpha.
```

(ii) Factor `L(s) = (s-rho_0) prod_{rho_j in cluster, j != 0}(s-rho_j) ·
H_A(s)`. The cluster local factor ratio at `rho_0+alpha` vs at `s`:

```text
|alpha+rho_0 - rho_j| / |s - rho_j|
  <= (A+1) alpha / (R alpha)
  = (A+1)/R  <  1.
```

Product over cluster mates (any size!) gives **ratio <= 1**, not `T^{o(1)}`.
This is even cleaner than required — **no zero-count bound needed**.

(iii) The remaining `H_A(rho_0+alpha)/H_A(s)` ratio is the *same noncluster
ratio* the repo's existing `ClusterShiftDerivativeComparison(E,A)` already
controls as `T^{o(1)}`. The argument is essentially identical: both points
lie within `O(alpha)` of `rho_0` in the cluster-free region.

**Conclusion**: Door B reduces to extending the existing local noncluster
stability lemma from a single sampled point `rho_0 + alpha` to a boundary
arc of radius `R alpha`. This is a uniformity statement, not a new theorem.
It is an **audit task**, not a research blocker.

### 5.2 Door C is a proof surgery, not analysis

The H1 proof currently bounds the offcentral contribution by inserting
absolute values inside an inverse Laplace / Perron-type integral and
hitting `sum |L'(rho)|^{-1}`. The contour version is *literally* the
residue theorem applied one step earlier. The H1 conclusion is a bound on
a *specific* offcentral functional, and that functional is naturally a
signed contour residue. The only risk is that an intermediate step
secretly uses positivity (`R_B` enters something positive that one wants
to dominate). The audit:

1. Find the line where `sum |Phi_T(rho)/L'(rho)|` appears.
2. Confirm the *containing* estimate accepts a signed sum
   `|sum_{rho offcentral} Res_{rho} Phi_T/L|`.
3. If a positivity is genuinely required upstream (e.g. for an `l^1` energy
   identity), the halo route fails and we are back to Palm.

Read of the conditional simple-zero stack in the repo
(`H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md`) and
`WeakSeparatedEC-BFMT-H1(E,c)` suggests the signed form is acceptable. But
this **must** be verified line-by-line.

### 5.3 Door D — numerator audit

For the standard H1 test function arising from explicit-formula /
truncated Perron with a smooth weight, `Phi_T(s)` is typically a product
of a Gamma factor or a smooth cutoff times `X^s` for some `X = T^{theta}`
or smaller, plus mollifier. In the halo region (`s` at distance `O(alpha)`
from the critical line, height `~T`):

```text
|Phi_T(s)| <= |X|^{Re s} · (smooth Gamma factor)
             ~ X^{1/2+O(alpha)} · T^{O(1)·(Stirling)}.
```

If `X = T^{o(1)}` (smooth cutoff small) the sup norm is `T^{o(1)}`.
For the standard H1 weight (which is exactly the kind of `o(1)` smooth
cutoff appearing in pointwise central theorems for rank-one EC), this is
the expected case. **Audit task**: compute `M_T` for the exact `Phi_T` in
the repo's H1 statement, confirm `M_T = T^{o(1)}` or at least `o(T^{1/4})`.

### 5.4 Door A — the real research problem

```text
AllZeroShiftedNeg_2(E):
sum_{rho in Z_T}^{mult} |L_E^*(rho + 1/log T)|^{-2}  <<  T^{5/2+eps}.
```

This is the only door that is not a bookkeeping audit. Below is the plan.

---

## 6. Door A — why `T^{5/2+eps}` is very loose

Conjectural truth (random-matrix heuristic for fixed GL2 newform):

```text
sum_{rho}^{mult} |L(rho+alpha)|^{-2}
  ~  alpha^{-2} sum_rho |L'(rho)|^{-2}
  ~  (log T)^2 · T · (constants),
```

i.e., **`T (log T)^{O(1)}`**, fifteen halves of `T` below the target.

So Door A asks for an *enormously lossy* upper bound: anything below `T^{5/2}`
is enough, and the conjectural truth is `T^{1+o(1)}`. This is the kind of
bound that *should* be unconditional for any decent L-function. Two routes:

### Route A1 — Continuous shifted negative second moment + transfer

Prove

```text
ContShiftNeg_2(E):
  int_T^{2T} |L_E^*(1/2 + 1/log T + it)|^{-2} dt  <<  T^{3/2+eps}.
```

Conjectural truth: `T (log T)^{O(1)}`. Target is `T^{3/2}` — extremely loose.
Then transfer from continuous to zero-sampled with multiplicity via the
*Gallagher / Heath-Brown* lemma: for any L^2 function `g` on `[T,2T]`,

```text
sum_{rho : T < gamma <= 2T}^{mult} |g(gamma)|^2
  <<  log T  int_T^{2T} |g(t)|^2 dt
   +  log T  int_T^{2T} |g'(t)|^2 dt / (log T)^2.
```

Applied to `g(t) = L(1/2+alpha+it)^{-1}`, the derivative term involves
`|L'|/|L|^2 · |L|^{-1}` on the shifted line; treatable by Cauchy-Schwarz
with mean-square `|L'/L|` (Mertens-type) and the same continuous moment.

The continuous moment for **zeta** at this loseness is known
unconditionally (Bui-Florea, [arXiv:2302.07226]). For GL2/EC the extension
plan is below.

### Route A2 — Direct zero-sampled second moment

Apply the **approximate functional equation** for `L^{-1}`:

```text
1/L(s) = sum_{n <= Y} mu_E(n)/n^s + (functional equation reflection)
        + small,    Y = T^{1+o(1)}.
```

Here `mu_E(n)` are the Dirichlet inverse coefficients of `L_E^*` —
multiplicative, with `|mu_E(p)| <= 2` by Deligne, `mu_E(p^k)` of bounded
shape. Sample at zeros:

```text
sum_{rho}^{mult} |L(rho+alpha)|^{-2}
  =  sum_rho^{mult} |sum_n mu_E(n)/n^{rho+alpha}|^2 + (cross terms).
```

Expand and use a zero-sum estimate (Landau / Gonek / Riemann-von Mangoldt
explicit formula) to convert `sum_{rho} n^{-rho}` into a prime-power sum
of length `~Y log T`. This is exactly the BFMT zero-sample strategy, with
`k = 1` (= q=2). The repo audits
`ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` and
`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` mark q=2 as **conditional
pass** but not source-promoted. The plan finishes that audit.

---

## 7. Staged plan toward unconditional proof

### Stage 0 — Confirm the route is wanted

Audit the H1 proof in the repo (Door C). Two outcomes:

- **GREEN**: signed contour residue is acceptable, halo route applies.
- **RED**: positivity is genuinely required; abandon halo, return to
  rooted Palm.

Cost: 0.5 day of careful reading. **Must precede everything else.**

Files:
- `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md`
- `handoff-2026-05-11-post-wave5-pivot/H1_DISPLACEMENT_WALL_SYNTHESIS_2026-05-11.md`
- `handoff-2026-05-11-h1-residue-control-wave/` (relevant to residue form)
- `handoff-2026-05-11-h1-shell-moment-wave/`
- `handoff-2026-05-11-ec-h2-mertens-sprint/` (numerator side)

### Stage 1 — Door B and Door D audits (bookkeeping)

Door B: extend the noncluster stability lemma from sampled point
`rho_0+alpha` to a boundary arc. Key lemma to prove:

```text
For s in partial D(rho_0, R alpha), R > A+1:
|H_A(rho_0+alpha)| / |H_A(s)| <= T^{o(1)}.
```

This uses the same Hadamard-Jensen / explicit-formula machinery as the
existing single-point version. Replace point evaluation by sup over a
disk of radius `R alpha` and absorb into `T^{o(1)}`.

Door D: compute `M_T = sup_halo |Phi_T(s)|` for the *specific* `Phi_T`
in the H1 statement. Expect `M_T = T^{o(1)}`. Document explicitly.

Cost: ~1-2 days. **Pure audit, no new ideas needed.**

### Stage 2 — Door A primary route: ContShiftNeg_2 for fixed EC

**Theorem (target)**: Let `E` be a fixed elliptic curve over Q (or any
fixed cuspidal newform of weight `k_0`). Then

```text
int_T^{2T} |L_E^*(1/2 + 1/log T + it)|^{-2} dt  <<_E  T^{3/2+eps}.
```

The conjectural truth is `T (log T)^{O(1)}`. Plan:

**Step 2.1 — Approximate functional equation for `1/L_E^*`.**

For `s = 1/2 + alpha + it`, `|t| <= 2T`, write

```text
1/L_E^*(s) = D_Y(s) + epsilon(s,1-s) D_Y(1-s) + error,
```

with `D_Y(s) = sum_{n <= Y} mu_E(n) V(n/Y) / n^s` for a smooth cutoff `V`
and `Y = T`. `mu_E` is the Dirichlet inverse of `lambda_E`. Coefficient
bound: `|mu_E(n)| <= d(n) · 2^{Omega(n)}` (multiplicative, bounded shape
on prime powers).

**Step 2.2 — Mean-square of the partial sum.**

Standard Montgomery-Vaughan:

```text
int_T^{2T} |D_Y(1/2+alpha+it)|^2 dt
  =  T sum_{n<=Y} |mu_E(n)|^2 n^{-1-2 alpha} + O(error).
```

Bound `sum_{n<=Y} |mu_E(n)|^2 / n^{1+2 alpha}`. Multiplicativity gives

```text
sum_n |mu_E(n)|^2 / n^{1+2 alpha}
  =  prod_p (1 + |mu_E(p)|^2 / p^{1+2 alpha} + ...).
```

For good primes `mu_E(p) = -lambda_E(p)`, `|mu_E(p)|^2 = lambda_E(p)^2`,
average `1` (Rankin-Selberg). The product behaves like
`(log Y)^{O(1)}`. With `Y = T`, the mean-square is `T (log T)^{O(1)}`.

This is the conjectural-order bound. **`T^{1+eps}`**, much better than the
`T^{3/2+eps}` target.

**Step 2.3 — Cross terms and the reflection.**

The cross `int D_Y · overline(epsilon · D_Y(1-s))` integrates to off-diagonal
contributions of size `O(T^{1/2+eps})` by standard exponential-integral
methods (Atkinson dissection).

**Step 2.4 — Subtle point: does mean-square of `D_Y` actually upper-bound
`int |1/L|^2`?**

Not obviously — the AFE for `1/L` is **not** a uniform upper bound; it
has an error term that gets large when `|L|` is small. The "near-zero"
problem is fundamental.

Cure (Heap-Soundararajan moves):

1. Split `[T,2T] = G ∪ B` where `B = {t : |L(1/2+alpha+it)| < V}` for
   some `V = (log T)^{-A}`.
2. On `G` (good set): mean-square of `D_Y` works.
3. On `B` (bad set): `|B|` is controlled by an upper bound on the
   *positive* second moment via Markov: `|B| · V^{2k} <= int |L|^{2k}`.
   Standard mean-value for `|L|^{2k}` (k=1 trivial; k=2 via approximate FE)
   gives `|B| << T · V^{2k} / T^{some}`.
4. On `B`, use the trivial pointwise bound `|L|^{-1} <= T^{O(1)}` from
   functional equation + convexity. Then `int_B |L|^{-2} <= |B| · T^{O(1)}`.

Calibrating `V`, `k`, get an unconditional polynomial-loss bound that
easily beats `T^{3/2}`. For ζ, Heap-Soundararajan prove the analog
unconditionally with the right `(log T)` power. For GL2 newform of fixed
conductor, all ingredients (functional equation, mean-value `int |L|^{4}`,
zero-density bounds, convexity) are classical and adapt verbatim.

**Step 2.5 — Cite and audit primary sources.**

- Heap, Li, Zhao, *Lower bounds for negative moments of zeta*, Mathematika
  (or arXiv) — unconditional `int |zeta|^{-2k}` over a shifted line.
- Bui-Florea (arXiv:2302.07226) — sharp upper bounds for negative moments
  of zeta on a shifted line, unconditional.
- Heath-Brown, *Fractional moments of the Riemann zeta function*, J. LMS
  1981 — second moment method.
- Soundararajan, *Moments of the Riemann zeta function*, Annals 2009 —
  Soundararajan-Selberg upper-bound technique (generalizes to GL2 with
  bounded conductor).
- Iwaniec-Kowalski, *Analytic Number Theory*, chapter on L-functions —
  for the GL2 fourth moment lemma needed in step 2.4.

**Cost estimate**: 2-3 weeks of focused work, mostly transcription of
known zeta techniques to GL2 with bounded conductor. No new theorem
required, just careful adaptation.

### Stage 3 — Door A fallback: zero-sample second moment (BFMT route)

If ContShiftNeg_2 transfer is harder than expected (e.g., the
Gallagher / HB transfer eats a `T^{1/2}` because of the derivative term),
fall back to **direct** sampling at zeros following BFMT.

**Step 3.1 — Sample 1/L at zeros using its AFE.**

```text
sum_{rho}^{mult} |L(rho+alpha)|^{-2}
 = sum_{rho}^{mult} |D_Y(rho+alpha) + reflection + error|^2.
```

Expand. The main diagonal: `sum_n |mu_E(n)|^2 / n^{1+2 alpha} · #zeros`.
With `#zeros << T log T`, this is `T (log T)^{O(1)}`.

**Step 3.2 — Off-diagonal via Landau-Gonek.**

For `m != n`:

```text
sum_{rho : T < gamma <= 2T} (m/n)^{i gamma}
 ~  -T/(2pi) · Lambda_E(m/n) · m^{-1/2}
    + O(...)
```

if `m/n` is close to an integer, otherwise `O(log T)`. This is exactly the
Landau-Gonek formula for fixed GL2 (repo audit:
`handoff-2026-05-11-ec-s1-explicit-formula-sprint/` and
`GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md`).

**Step 3.3 — Reflection and error analysis.**

Reflection term and error: handled by the same BFMT k=1 ledger that the
packet already conditionally passes. Source-close the ledger:

- BFMT Lemma 2.4 majorant.
- BFMT Props 2.5, 2.6, 2.7 for GL2 with degree-2 conductor.
- Bad-prime / prime-power audit (Euler factor at ramified primes for `E`).

**Multiplicity weighting**: when `rho` is a zero of order `m`,
`|L(rho+alpha)|^{-2}` is at most `|alpha|^{-2m} · |L^{(m)}(rho)/m!|^{-2}`.
Multiplicity-weighted sum: counted with `m` weight. For GL2 newform,
multiplicity at offcentral height is at most `O(log T)` by Riemann-von
Mangoldt — small enough to be absorbed by `T^{eps}`.

**Cost estimate**: 3-4 weeks. The BFMT ledger is technical but
fully recoverable.

### Stage 4 — Multiple-zero disposition (Door A + Door E combined)

For rank-one offcentral H1, two routes:

**Route i**: source-close `AllZeroShiftedNeg_2` *with multiplicity weight*.
Done by Stage 3 with multiplicity in the sum. Then the halo theorem
includes multiples automatically.

**Route ii**: keep `H1-MultipleZeroDisposition` as separate input. For a
fixed EC of rank `r=1`, this requires `D_alpha <= 0` for unretained
offcentral multiple-zero exponents and `Z_0^mult(u) = o(u)`. Effective
multiplicity for GL2 newforms at offcentral height is conjecturally zero;
unconditionally the worst case is bounded multiplicity `O(log T)` plus a
nonzero density, both absorbed.

**Recommendation**: pursue route (i); it costs no extra over Stage 3 if
the BFMT ledger is multiplicity-aware from the start.

### Stage 5 — Assemble

After Stages 0-4:

```text
AllZeroShiftedNeg_2(E)                        [Stage 2 or 3]
+ HaloShiftComparison(E,A,R), R > A+1         [Stage 1]
+ ResidueFirstH1Rewrite                       [Stage 0 audit]
+ M_T = T^{o(1)}                              [Stage 1]
=> offcentral H1 residue contribution = o(T^2)        [halo theorem]
```

Combined with the existing conditionally harmless separated branch
`R_F(T,c) << T^{3/2+eps}` and central-zero handling, this closes
unconditional offcentral H1 for the fixed EC `E`.

---

## 8. Novel angles not pursued in the handoff

These are research-level alternatives that have not been auditioned
against the wall and may, in some cases, give faster routes.

### 8.1 Direct rectangle + mollified second moment

The global thin rectangle (`handoff` Section 7) is **structurally cleaner**
than the halo: no choice of `R_T`, no boundary-arc accounting. Its only
gap is the *continuous* shifted moment. If Stage 2 succeeds, the
rectangle is automatically available and is a one-page proof — preferable
for paper writing.

The mollifier idea: bound

```text
int |L^{-1}|^2  =  int |L M / L^2|^2 / |M|^2
                ~  int |LM|^2 · sup |1/(M L)|^2.
```

For a Conrey-Iwaniec-style mollifier `M` of length `T^{theta}` targeting
`L^{-1}`, `int|LM|^2 ~ T`. The sup is bounded above on a "good" set.
This is precisely Iwaniec-Soundararajan for `t`-aspect GL2.

### 8.2 Pseudo-Borel-Carathéodory on the halo

Instead of comparing `|L(s)|` to `|L(rho+alpha)|` via the explicit
factorization, use a Hadamard-Jensen identity: for `s` and `rho+alpha`
both inside a slightly larger disk on which `L` is bounded,

```text
log |L(rho+alpha)/L(s)|
 = (sum over zeros z in larger disk of log|z-(rho+alpha)| - log|z-s|)
   + (harmonic correction term, T^{o(1)}).
```

The sum is a *signed* difference, not an absolute value. By zero-counting
on the larger disk (Riemann-von Mangoldt local form: `N(rho, A·alpha) << log T`
boundary, with conjectural `o(log T)` for "almost every" rho), the sum is
`<= log T · max log((distance ratios))`. For `s` and `rho+alpha` both at
distance `O(alpha)` from cluster center, `log((dist ratios)) = O(1)`. So
the ratio is `T^{O(log T / log log T)}` worst case — *not* `T^{o(1)}` in
general!

This is why Door B is *not* free without a structural simplification like
`R > A+1`. Worth recording: the explicit factorization route used in
Stage 1 is essentially forced.

### 8.3 Density-method for `R_B` directly

Bypass the residue rewrite entirely:

```text
N(T,V) := #{rho in S_E(T) : |L'(rho)|^{-1} > V}.
R_B(T,c) <= int_0^infty N(T,V) dV.
```

Then `int_0^{V_0} N dV <= V_0 · T log T`, and `int_{V_0}^infty N dV
<= V_0^{-1} sum |L'|^{-2}`. With a *positive* second negative moment
`sum_{rho}^{mult} |L'(rho)|^{-2} << T^{c}`, optimize over `V_0`:

```text
R_B << sqrt( T log T · T^c )  =  T^{(c+1)/2 + o(1)}.
```

To beat `T^2`, need `c < 3`. The conjectural truth `c=1` is enormously
better. Unconditional `c < 3` should be very accessible — much cheaper
than Stage 2-3, *if* the H1 proof tolerates a positive `R_B` bound.

This is essentially Challenge 3 of the original packet (direct reciprocal
tail), but with a much weaker target: `c < 3` instead of `c < 1`. The
packet rated this NO-GO because it implicitly required something close to
the conjectural truth. With `c=3-eta` for any tiny `eta`, the bound
`R_B << T^{2-eta/2}` follows.

**This may be the cheapest unconditional route, *if* the H1 proof
tolerates the absolute-value form.** Stage 0's audit (residue-first vs.
positive-budget) determines whether the halo route or this density route
is preferred.

### 8.4 Probabilistic / random-matrix one-tail

For random matrix `U(N)`, ` sum_{theta_j} |Z'(theta_j)|^{-2}` is `O(N)`
with high probability (Hughes-Keating, Conrey-Snaith). If a fixed
GL2 newform satisfies the **upper-tail** version of Katz-Sarnak in t-aspect
(which is *not* known and is essentially as strong as Lindelöf for the
4th derivative moment), one gets `sum |L'|^{-2} << T (log T)^{O(1)}`
unconditionally for `t`-aspect GL2. This is genuinely an open problem.
Not a near-term route.

### 8.5 Convexity-of-`|L|^{-1}`-on-shifted-line via subharmonicity

`log|L|` is subharmonic. On the shifted line `Re s = 1/2 + alpha`,
applying the standard "Hadamard three-circles" inequality on a strip
of width `O(alpha)` astride the critical line gives:

```text
log|L(1/2+alpha+it)|^{-1}
  <= (1/2) log|L(1/2+2alpha+it)|^{-1} + (1/2) log|L(1/2+it)|^{-1}
        + (boundary terms).
```

The first term has `|L|^{-1}` *deeper* in the half-plane of absolute
convergence, where Rankin-Selberg gives polynomial lower bounds on `|L|`.
The second is the critical-line `|L|^{-1}` — exactly what we want to bound.
This is a *self-referential* inequality and doesn't immediately close,
but combined with a positive 4th moment and an iterative bootstrap, it
sometimes gives gain. Worth exploring as a "patch" if Stage 2 hits a
T^{1/4+eps} wall in the transfer.

### 8.6 Halo with weighted boundary

The halo theorem uses a *uniform* halo radius `R alpha`. A weighted halo,
with `R_rho` depending on `rho`, might give a better trade: large
`R_rho` where `|L|` is large on the boundary, small `R_rho` where
`|L|` is small. This is a *Sobolev-type* optimization. The unconditional
gain is potentially significant when the offcentral zeros are highly
clustered (which is the hard case anyway).

---

## 9. Risk register and abort criteria

### Risk R1: ResidueFirstH1Rewrite fails

Probability ~ 0.2. Mitigation: density-method (8.3) gives an
alternative that does not need residue rewrite, at the cost of needing a
slightly stronger (but still loose) negative second moment of `L'`.

### Risk R2: ContShiftNeg_2 has unconditional value above `T^{3/2}`

Probability ~ 0.1. Mitigation: zero-sample route (Stage 3) instead, or
weaken the halo theorem by adopting a `q=3` shifted moment with the
correspondingly stricter margin.

### Risk R3: HaloShiftComparison breaks at boundary-arc level

Probability ~ 0.05. Mitigation: use cluster-resummed finite-box module
(Section 6 of handoff) instead of halo; this avoids boundary-arc
comparison at the cost of cluster-level cluster-shift comparison (already
proved in repo for sampled point, extendible).

### Risk R4: M_T is *not* `o(T^{1/4})` for the H1 test function

Probability ~ 0.05. Mitigation: examine the H1 test function in detail.
If `M_T = T^{theta}` with `theta in [1/4, 1/2)`, restate halo theorem with
q=3 input (`T^{2 - 1/(2q)} = T^{11/6}` margin = `1/6`, requires
`theta < 1/6`). If still too tight, use stronger input.

### Hard abort: Door A unconditional value found to be `>= T^{5/2}`

Then halo route does not directly close. Fall back to original `q=3` Palm
route, accepting Palm wall as the bottleneck. Probability of this hard
abort: ~ 0.02.

---

## 10. Concrete next steps for the continuation agent

In order:

1. **Stage 0**: read the H1 proof in
   `handoff-2026-05-11-h1-breakthrough-proof-wave/` and
   `H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md`. Determine whether the
   contour residue form is acceptable (Door C audit). Output: a one-page
   memo `H1_RESIDUE_FIRST_AUDIT_2026-05-12.md`.

2. **Stage 1, parallel a**: write `HALOSHIFTCOMPARISON_LEMMA_2026-05-12.md`
   stating and proving HaloShiftComparison with `R > A+1`, reducing to the
   existing noncluster `H_A` lemma extended to a disk of radius `R alpha`.

3. **Stage 1, parallel b**: write `H1_NUMERATOR_M_T_AUDIT_2026-05-12.md`
   computing `M_T` for the exact test function in the H1 proof.

4. **Stage 2 sprint**: write `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-12.md`
   transcribing Heap-Soundararajan + Bui-Florea for fixed-conductor GL2.
   Decompose: AFE for `1/L_E^*`, mean-square of partial sum, off-diagonal
   via Mertens / Rankin-Selberg, near-zero (`bad set`) cure.

5. **Density-method side-quest**: write
   `DENSITY_METHOD_RB_LOOSE_2026-05-12.md` exploring 8.3 as a parallel
   fallback that does not require residue-first.

6. **Synthesis**: a single `UNCONDITIONAL_H1_OFFCENTRAL_2026-MM-DD.md`
   collecting Stages 0-5 and stating the unconditional theorem.

---

## 11. Claim ledger after this plan

Allowed to claim **now** (additions beyond `H1_Palm_Wall_Halo_Handoff`):

```text
HaloShiftComparison(E,A,R) reduces to a boundary-arc extension of the
existing noncluster H_A stability lemma, with R > A+1 trivializing the
cluster-mate ratio. It is an audit task, not a research blocker.
```

```text
AllZeroShiftedNeg_2(E) has target T^{5/2+eps} versus conjectural truth
T^{1+o(1)}. The gap of 3/2 in the exponent is enormous; unconditional
proof for fixed GL2/EC should follow from Heap-Soundararajan-style upper
bounds adapted from zeta, modulo a multi-week BFMT-style audit.
```

```text
The density-method (8.3) provides an alternative unconditional route to
R_B(T,c) = o(T^2) that does NOT require residue-first rewrite, given a
loose negative second moment of L'(rho) (target c < 3 in T^c, conjectural
truth c = 1).
```

Not allowed to claim:

```text
Unconditional H1.
Unconditional R_B.
ContShiftNeg_2 for GL2 is in the literature.
AllZeroShiftedNeg_2 is in the literature.
The H1 proof is known to accept residue-first form.
```

---

## 12. Source list (additions)

Adjacent / target sources for Stage 2-3:

1. Heap-Li-Zhao, *Lower bounds for negative moments of zeta*, Math
   Annalen 2022 / arXiv:2107.06829 (and follow-ups).
2. Bui-Florea, *Negative moments of the Riemann zeta function*,
   arXiv:2302.07226.
3. Bui-Florea-Milinovich-Turnage-Butterbaugh, arXiv:2310.03949.
4. Soundararajan, *Moments of the Riemann zeta function*, Annals 2009.
5. Heath-Brown, *Fractional moments of the Riemann zeta function*,
   J. LMS 1981.
6. Milinovich-Ng, arXiv:1306.0854 (fixed newform reciprocal-derivative
   moments — most directly transferable).
7. Conrey-Iwaniec, *The cubic moment of central values of automorphic
   L-functions*, Annals 2000 (mollifier techniques for GL2).
8. Iwaniec-Kowalski, *Analytic Number Theory*, chapters 5 & 24.

---

## 13. Final synthesis

The halo handoff is correct: the rooted Palm wall is **not** a necessary
input to the H1 contour residue contribution. The remaining four doors
split into three audits (Doors B, C, D) and one genuine analytic task
(Door A).

Door A's target — `T^{5/2+eps}` for the shifted negative second moment —
is **3/2 powers of `T` above the conjectural truth**. For a fixed GL2
newform with bounded conductor, this should be unconditional via
Heap-Soundararajan-style arguments. Two routes (continuous + transfer,
or direct zero-sample BFMT) are both viable.

A parallel safety net: density-method gives an unconditional `R_B = o(T^2)`
under a loose negative second moment of `L'(rho)` (target `T^{c}`,
`c < 3`, conjectural truth `c = 1`), and does **not** need residue-first
rewrite. This is the cheapest path if Stage 0 surfaces a positivity
obstruction.

The next milestone is Stage 0: a one-page memo determining whether H1
accepts residue-first form. Everything downstream branches from that.

```text
Estimated total cost to unconditional offcentral H1:
  Stage 0    : 0.5 d   (read + memo)
  Stage 1    : 1-2 d   (Door B + Door D audits)
  Stage 2    : 2-3 w   (ContShiftNeg_2 for GL2, primary route)
  or Stage 3 : 3-4 w   (zero-sample BFMT k=1, fallback)
  Stage 4    : included in 2 or 3 (multiplicity)
  Stage 5    : 0.5 w   (write-up)
  Total      : 1-2 months of focused work.

Estimated total cost to unconditional R_B via density method (8.3):
  Stage 0    : not needed
  Negative 2nd moment of L' loose : 2-4 w
  Total      : 0.5-1 month, but depends on H1 accepting positive form.
```

The boundary has moved decisively from a Palm/RMT problem to a *shifted
moment* problem with a 3/2-power-of-`T` safety margin. This is the kind
of gap that unconditional analytic number theory routinely closes.
