---
schema_version: 2
title: "Halo Door B — Unconditional Promotion Analysis"
type: analysis
domain: project
tier: working
status: ANALYSIS
confidence: 0.70
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-h1-residue-control-wave/H1_POSITIVE_RANK_CLOSURE.md
  - Iwaniec-Kowalski, "Analytic Number Theory", Ch. 5 (zero-free regions, zero-density)
  - Kim-Sarnak 2003 (refined GL2 zero-free regions)
  - Bombieri 1965 / Forti-Viola 1973 (GL_n zero density)
  - Heath-Brown 1979 (zeta zero density)
  - Mossinghoff-Trudgian-Yang 2024 (explicit zero-free regions)
supersedes: []
superseded-by:
tags: [halo-route, door-B, unconditional, GRH-removal, analysis]
---

# Door B Unconditional Promotion Analysis

Question: can Door B (HaloShiftComparison) be lifted off GRH for `L_E^*`?
Answer below built top-down: verdict, GRH usage point, restructure attempts,
best path, cost, boundary.

## 1. Headline verdict

```text
verdict:  NO  (with PARTIAL fallback under "GRH-up-to-T^{99/100}")
```

The geometric contraction `sqrt(1+A^2) / R_T < 1` per cluster mate is
*structural*: it requires cluster mates to be aligned vertically with
`rho_0`, i.e. `Re rho_j = Re rho_0 = 1/2`. Without that alignment the
real-part offset `(Re rho_0 - Re rho_j)` can dominate the imaginary-part
offset `(gamma_0 - gamma_j)` for nearby zeros, and the product over the
cluster — of arbitrary cardinality `N_{rho_0, A}(T)` — re-exposes the
exact obstruction (`C_A^{N_{rho_0,A}(T)}`) that the geometric step was
designed to kill.

Unconditional inputs (zero-free regions, zero-density estimates) do not
deliver `Re rho_j = 1/2 + O(alpha)` for *every* cluster mate of *every*
offcentral `rho_0` simultaneously, which is what the geometric step
demands.

PARTIAL fallback: a strictly weaker hypothesis ("GRH up to height
`T^{99/100}`", or "density-one critical-line concentration with effective
exceptional-zero rate") suffices for Door B without touching the
downstream halo theorem. Neither is currently known unconditionally, but
the gap is smaller than full GRH.

## 2. Door B's exact GRH usage (the load-bearing line)

From `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` §2.2 (cluster mates):

```text
Under GRH, Re rho_j = Re rho_0 = 1/2, so
  |rho_0 + alpha - rho_j|^2  =  alpha^2 + (gamma_0 - gamma_j)^2
                            <=  alpha^2 (1 + A^2).
Per cluster mate ratio:
  |rho_0 + alpha - rho_j| / |s - rho_j|  <=  sqrt(1+A^2) / R_T  <  1.
Product over cluster (arbitrary size) <= 1.
```

Without GRH, cluster mate `rho_j = beta_j + i gamma_j` with
`beta_j != 1/2` gives

```text
|rho_0 + alpha - rho_j|^2  =  (alpha - (beta_j - 1/2))^2 + (gamma_0 - gamma_j)^2.
```

`s` on `partial Omega_T` still satisfies `|s - rho_j| >= R_T alpha` (the
boundary-arc property is purely metric, GRH-free). But the *numerator*
loses control: if `(beta_j - 1/2) >> alpha = 1/log T`, the ratio per
mate exceeds 1, and the product diverges as `C^{N_{rho_0,A}(T)}`.

The Door B contraction *is* the identification `Re rho_j = 1/2`. Nothing
else uses GRH in §2.

Note: Step 4 of the arc-uniformity audit (§2.4 of
`HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md`) also uses
`|rho_0 - rho_j| = |gamma_0 - gamma_j|` under GRH to bound the inverse-
square sum `sum 1/(gamma_j - gamma_0)^2 ~ (log T)^2 / (pi R)`. But this is
a noncluster sum and is *robust*: dropping GRH only *decreases* the
denominators by an amount `(beta_j - 1/2)^2` which is at worst `O(1)`,
and the off-critical-line zero count is controllable by zero density.
This sub-step is NOT the obstruction. The cluster-mate step §2.2 is.

## 3. Restructure attempts

### 3.1 Attempt §1 — invoke unconditional zero-free region

Best known unconditional zero-free region for a fixed degree-2 cuspidal
L-function (Iwaniec-Kowalski Ch. 5; Kim-Sarnak; Mossinghoff-Trudgian-Yang
explicit): for the newform `L_E^*` of conductor `N_E`,

```text
Re rho  <=  1 - c(E) / log(|gamma| + 2),     (c(E) > 0 effective)
```

equivalently (by functional equation `s -> 1-s`),

```text
beta_j = Re rho_j  in  [ c(E)/log(|gamma_j|+2),  1 - c(E)/log(|gamma_j|+2) ].
```

For `|gamma_j| ~ T`, this gives `|beta_j - 1/2| <= 1/2 - c(E)/log T`.

**Compare to `alpha = 1/log T`:**

```text
|beta_j - 1/2|  may be as large as  1/2 - c(E)/log T  ~  1/2,
                                     >>  alpha = 1/log T.
```

The unconditional region puts off-critical zeros within distance
`1/2 - c/log T` of the critical line — far *exceeds* `alpha`. Useless
for the per-mate contraction. **Attempt fails by ~ factor `log T/2`.**

A zero-free region narrow enough to give `|beta_j - 1/2| << alpha` would
require `Re rho_j <= 1/2 + 1/log T` for all zeros — *that is GRH up to
an `O(1/log T)` strip*, currently unknown.

Verdict §1: **fails**.

### 3.2 Attempt §2 — zero-density inside thin critical strip

Standard zero-density for `GL_2` newform (Bombieri / Forti-Viola; for
zeta, Heath-Brown 1979 gives the sharpest known density exponent):

```text
N(sigma, T)  <<  T^{A (1-sigma)} (log T)^B,
```

with `A = 2` (or better in special ranges). At `sigma = 1/2 + 1/log T`:

```text
N(1/2 + 1/log T, T)  <<  T^{2 - 2/log T} (log T)^B  =  T^2 / T^{2/log T} (log T)^B
                      =  T^2 · e^{-2 log T / log T} (log T)^B
                      =  T^2 / e^2 (log T)^B.
```

This is `Theta(T^2 log^B T)`. The Riemann-von Mangoldt total zero count
to height `T` is `~ T log T`. So the density bound is **larger than the
total zero count** — *vacuous* in this regime.

Sharper question: is there a *thin-strip* bound

```text
#{rho : 1/2 < Re rho <= 1/2 + 1/log T, |Im rho| <= T}  =  o(T log T) ?
```

Such a bound would say "most zeros are at most `1/log T` off the
critical line." It is **not known unconditionally** for `GL_2`. (For
zeta, Selberg's `S(T)` central-limit work and Conrey-Ghosh density-one
results imply almost-all zeros are within distance `(log log T)/log T`
of the critical line *on average* — but the "all but `o(T log T)`"
strengthening is not even known for zeta, let alone `L_E^*`.)

Even granting density-one critical-line concentration, the *every-arc*
Door B statement requires the contraction to hold for the cluster of
**every** offcentral `rho_0`. A density-one statement loses the
remaining `o(T log T)` zeros; those cluster mates are not controlled,
and the bad mate's `rho_0` produces an arbitrary-cluster-size obstruction.

Verdict §2: **fails for pointwise; partial for density-one** (loss is
exactly the offending exceptional bad `rho_0` set).

### 3.3 Attempt §3 — split cluster into good/bad mates

Define

```text
C_A^good(rho_0)  =  { rho_j in C_A(rho_0)  :  |Re rho_j - 1/2|  <=  epsilon alpha },
C_A^bad(rho_0)   =  C_A(rho_0) \ C_A^good(rho_0).
```

For `C_A^good`: per-mate ratio `sqrt(1 + A^2 + epsilon^2)/R_T < 1` if
`R_T > sqrt(1 + A^2 + epsilon^2)`. Absorbed by enlarging `R_T` by
`O(epsilon^2)`. Product `<= 1`.

For `C_A^bad`: per-mate ratio may exceed 1. Need to bound
`n_bad(rho_0) := #C_A^bad(rho_0)`.

**Sub-question.** Is `n_bad(rho_0) = o(log T)` (or even `O(1)`) uniformly
over `rho_0`?

Available inputs:

- *Average*: by zero density (§3.2), summing `n_bad(rho_0)` over
  `rho_0 in Z_T` gives at most a fraction
  `o(1) · T log T = o(T log T)` of pairs. So the *typical* `rho_0` has
  `n_bad(rho_0) = o(1)`.
- *Worst-case*: not controlled. A single offending `rho_0` with
  `n_bad(rho_0) = (log T)^{1+delta}` produces the obstruction
  `C_A^{n_bad}` which blows up.

The repo's existing Wave-4 cluster-size bound
(`CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md` L160-167) gives,
under fixed-newform RH:

```text
N_E(t+u) - N_E(t-u)  <<_E  u log T  +  log T / log log T  +  1.
```

So the *whole* cluster `C_A(rho_0)` has size `<= A + log T/log log T +
O(1)` under GRH. Without GRH, the imaginary-part-only bound on
`N_E(t+u) - N_E(t-u)` follows from Riemann-von Mangoldt (unconditional
to within `O(log T)`), so `|C_A(rho_0)| <= O(log T)` unconditionally —
but this is the *whole* cluster, *not* the bad-only subset.

We have no unconditional handle on `n_bad(rho_0)` uniformly. The thin-
strip zero-density gap is exactly the bad-mate cardinality bound for
`rho_0`'s in the offending sliver, and we've seen (§3.2) that this is
the unsolved problem.

Verdict §3: **fails on the uniform `n_bad(rho_0)` bound**.

A *quantitative refinement*: if a future unconditional bound gives

```text
sup_{rho_0 in Z_T}  n_bad(rho_0)  <=  C log log T,    (HYP-bad)
```

then per-mate ratio bounded by a fixed constant `M` (independent of `T`)
yields total contraction loss `M^{C log log T} = (log T)^{C log M}`,
absorbed into `T^{eps}`. So `(HYP-bad)` is sufficient. But `(HYP-bad)`
is currently *not* a published result.

### 3.4 Attempt §4 — weak supremum bound (replace contraction)

Drop the pointwise contraction `< 1` and accept a global bound
`<= M^{n_cluster}`. Then need `n_cluster = N_{rho_0,A}(T) = o(log T)`
uniformly. Repo's pre-§5.1 form needed exactly this.

Riemann-von Mangoldt local zero count: average density `(log T)/(2 pi)`
per unit imaginary, so average `|C_A(rho_0)| = A/(2 pi)`. Worst-case is
the issue.

Best known unconditional uniform local zero count (Goldston-Gonek 1998
style, and the Conrey-Ghosh "almost-all" results): for *almost all*
`rho_0`,

```text
|C_A(rho_0)|  <=  O(A + log log T).
```

Worst-case bound is `O(log T)` from Riemann-von Mangoldt (this is sharp
in the absence of further hypothesis — a cluster of size `log T/log log T`
is consistent with RvM).

So `n_cluster = O(log T)` is the *best* unconditional uniform bound,
which is *exactly the threshold* at which `M^{n_cluster} = M^{log T} =
T^{log M}` becomes a polynomial loss in `T` — worse than `T^{o(1)}`.

To get `o(log T)` uniformly is the *Selberg / Conrey-Gonek small-gap*
open problem (the famous "no cluster of size `log T/(log log T)^{1/2}`"
question). Conjectural under GUE, unproven unconditionally.

Verdict §4: **fails on the worst-case `n_cluster = o(log T)` bound**.

### 3.5 Attempt §5 — non-geometric Door B (Hadamard / Carleman)

Replace the explicit factorization `L(s) = (s - rho_0) prod_{C_A}(s-rho_j) H_A(s)`
by a *global* harmonic identity on `log |L(s)|`:

```text
log |L(s)|  =  Re sum_rho log(s - rho)  +  (entire-order corrections).
```

Door B asks for `sup_{s in partial Omega_T} |L(s)|^{-1} / |L(rho_0+alpha)|^{-1}`.
Take logs:

```text
log |L(rho_0+alpha)|  -  log |L(s)|
  =  Re sum_rho [ log(rho_0+alpha-rho) - log(s-rho) ]
   +  (lower-order analytic correction).
```

This is a sum over *all* zeros, not partitioned into cluster /
noncluster. Bound by maximum principle:

```text
sup_{s in partial D(rho_0, R_T alpha)}  |log|L(s)|^{-1} - log|L(rho_0)|^{-1}|
  <=  (something involving inverse distances to zeros).
```

The maximum principle gives the same kind of bound as the harmonic
mean-value identity used in §2.3 of the audit. **But the key obstruction
remains identical**: the contribution from each zero `rho_j` is roughly

```text
| log(rho_0 + alpha - rho_j)  -  log(s - rho_j) |.
```

Expand:

```text
log(s-rho_j) = log(rho_0+alpha-rho_j) + log(1 + (s-rho_0-alpha)/(rho_0+alpha-rho_j)).
```

For non-cluster `rho_j` (distance `> R alpha`), the perturbation
`(s-rho_0-alpha)/(rho_0+alpha-rho_j)` is `O(1/R)`, and the harmonic
mean-value argument gives `O_R(1)`. No GRH used. **This sub-step is
unconditional already.**

For cluster `rho_j` (distance `<= R alpha`): the perturbation can be
`O(1)` or larger. **The maximum principle just *re-states* the per-mate
ratio inside a log**: the contribution per mate is

```text
| log(per-mate ratio) |  <=  |log(sqrt(1+A^2)/R_T)|
                          =  log(R_T/sqrt(1+A^2))   under GRH,  bounded.
```

Without GRH, this is the same `(Re rho_0 - Re rho_j)` problem as §2.2,
inside a log. The cluster contribution sums to `O(n_cluster) ·
(typical per-mate log-ratio)`. **No new escape.**

This is just §2.2 dressed up. Maximum principle / Carleman doesn't
deliver a GRH-free contraction; it delivers the same arithmetic in
slightly different form.

Verdict §5: **fails. Same obstruction in different clothing.**

A genuine non-geometric escape would need a *positivity* mechanism — e.g.
Beurling-Selberg majorant for `|L|^{-1}` integrated against a nice
kernel. There is no such known mechanism for shifted `L^{-1}` values.

### 3.6 Attempt §6 — accept partial GRH

Strictly weaker substitutes:

| Hypothesis | Status (2026) | Door B works? |
|---|---|---|
| Full GRH for `L_E^*` | Open | Yes (current) |
| GRH up to height `T^{99/100}` | Open | Yes (cluster mates are at height `T`, fully inside the GRH range) |
| Density-one critical line | Conjectural (Conrey-Ghosh-type) | **No** for pointwise Door B; **Yes** for an average-over-`rho_0` weakening |
| Zero-density `N(1/2+1/log T, T) = o(T log T)` | Open (sharper than known) | Partial (every-`rho_0` still fails; exists-`rho_0` bad set has measure `o(T log T)`) |
| Vinogradov-Korobov for `L_E^*` | Currently unknown for general degree-2 cusp forms (only known for `zeta`, Dirichlet `L`, some special families); see Iwaniec-Kowalski §5.7 | Insufficient — still gives `|beta_j - 1/2| ~ 1/(log T)^{2/3}`, far worse than `1/log T` needed |

**Conclusion**: the *weakest* hypothesis that suffices for Door B as
currently stated is **GRH for `L_E^*` up to height `T`** (or, slightly
weaker, GRH in the thin strip `Re in [1/2, 1/2 + alpha]` up to height
`T`). This is essentially the same as full GRH in the regime relevant to
the halo theorem. No genuinely weaker known hypothesis works.

A more honest framing: **GRH for `L_E^*` up to height `T^{1+epsilon}`**
suffices because the cluster `C_A(rho_0)` only has zeros at heights
within `O(1)` of `gamma_0 in (T, 2T]`. So:

```text
weakest sufficient hypothesis  =  GRH for L_E^* restricted to heights in [T/2, 4T].
```

This is still open — no truncated-GRH unconditional result exists for
fixed degree-2 newforms at this strength.

## 4. Best candidate path forward

The five attempts above are all fundamentally blocked by the same
phenomenon: **the cluster of an arbitrary offcentral zero `rho_0` is an
uncontrolled local object without GRH**, and the per-arc Door B
statement quantifies over every `rho_0`.

Two paths exist, ranked by promise:

### 4.1 Recommended path: weaken Door B's quantifier

**Idea.** Replace "for every offcentral `rho_0` and every arc `s`" by
"for every offcentral `rho_0` *outside an exceptional bad-set*
`B_E(T, eta)` of cardinality `<= T^{1-eta} log T`, for every arc `s`."

Mechanism: combine
- unconditional thin-strip zero density: `N(1/2 + 1/log T, T) <<
  T^{2-c/log T} = T^2 / T^{Theta(1/log T)}` (vacuous as a count) but
- improved on a *log-spaced* scale: `N(1/2 + (log log T)/log T, T) <<
  T^{2 - 2 (log log T)/log T} = T^2 (log T)^{-2}` (still vacuous).

The improvement that *would* work: any unconditional bound of the form

```text
#{ rho_0 in Z_T  :  some cluster mate has |beta_j - 1/2| > alpha }
  <=  T^{1-eta} log T,    for some eta > 0.
```

This is *qualitatively* like a "Bombieri-Vinogradov for thin strips of
zeros", which is open. But the *halo theorem* (downstream of Door B)
ultimately wants to bound

```text
sum_{rho_0 in Z_T offcentral}  |L(rho_0 + alpha)|^{-2}  <<  T^{5/2+eps}.
```

If a bad-set `B_E(T, eta)` of cardinality `T^{1-eta} log T` is allowed,
then the bad-set contribution is

```text
|B_E(T, eta)|  ·  max_{rho_0 in B_E}  |L(rho_0 + alpha)|^{-2}
  <=  T^{1-eta} log T  ·  T^{?}.
```

If the per-zero `|L(rho_0 + alpha)|^{-2}` is bounded *unconditionally* by
`T^{1+eta/2}` (a much weaker pointwise bound than Door A wants), the
bad-set contribution is `T^{2 - eta/2 + o(1)} = o(T^{5/2})`. Then
**Door B becomes ignorable on the bad set**, and the good-set Door B
runs through under the current GRH-style argument (because for good
`rho_0` every cluster mate satisfies `|beta_j - 1/2| <= alpha`).

This restructures the halo theorem to:
- *Good set* (every cluster mate satisfies critical-line approximation):
  use the existing geometric contraction.
- *Bad set* (cluster has off-line mate): bound contribution directly via
  pointwise `|L(rho_0+alpha)|^{-2}` and bad-set cardinality.

Both halves are *unconditional* if we can produce:

```text
(P1)  #{ rho_0 : exists rho_j with |gamma_0 - gamma_j| <= A alpha and
                 |beta_j - 1/2| > alpha }   <=  T^{1-eta} log T.
(P2)  Pointwise  |L_E^*(rho_0 + alpha)|^{-1}  <=  T^{C}  unconditionally,
      for some constant C.
```

**(P2) is unconditional**: by convexity / functional-equation / Phragmen-
Lindelof, `|L_E^*(1/2 + 1/log T + i gamma_0)|^{-1}` is polynomially
bounded in `T` (the dangerous side of the critical line is small
positive shift, where the L-function may be small but not vanishing;
shifted off zero by `alpha = 1/log T` gives a polynomial unconditional
lower bound `|L| >= T^{-C}` from Hadamard product order considerations).
*This is a standard estimate — Iwaniec-Kowalski Ch. 5 / Heath-Brown
unconditional pointwise bounds give `C = O(1)` for fixed conductor.*

**(P1) is hard**: it is essentially asking for an unconditional
thin-strip zero density restricted to a *local cluster* (radius
`A alpha`) around *some* zero. By zero density `N(1/2+alpha, T) <<
T^{2-c/log T}` and crude inflation by `A alpha = O(1/log T)`-windowed
counting, one can show

```text
#{ pairs (rho_0, rho_j) : |gamma_0 - gamma_j| <= A alpha and
                          |beta_j - 1/2| > alpha }
  <=  N(1/2 + alpha, T)  ·  (max cluster width in imaginary)
  <=  T^{2 - c/log T}  ·  O(1)  =  T^{2-o(1)}.
```

This is NOT `T^{1-eta} log T`. Bad-set cardinality is dominated by
`T^{2 - o(1)}`, which gives a bad-set contribution of `T^{3 - o(1) - eta/2}`
to the Door-A sum — worse than the `T^{5/2}` target.

**Verdict**: this path needs a stronger thin-strip density than is
currently known. The gap from `T^{2-o(1)}` (known) to `T^{1-eta}`
(needed) is a factor `T^{1+o(1)}`. *Open problem.*

**Most promising in spirit, not currently executable.**

### 4.2 Fallback path: redefine Door B without the cluster

Reformulate Door B as a *bandlimited* statement: replace `partial Omega_T`
with a coarser set on which the cluster-mate ratio is automatically `O(1)`
in average sense, then use Cauchy-Schwarz with Door A to recover the
halo target. This is a *halo-theorem-level* surgery, not a Door B
surgery, and substantially overlaps with the parallel Door A track. Out
of scope for this analysis.

### 4.3 Recommendation

**Door B should stay conditional under GRH for `L_E^*`.** Promote to
"weakest sufficient hypothesis = GRH for `L_E^*` restricted to heights
`[T/2, 4T]`" in formal statements, but do not attempt unconditional
closure on the current halo plan. Spend the research budget on Doors A,
C, D, which are GRH-agnostic or weakly conditional.

## 5. Quantitative cost estimate

| Path | Required new mathematics | Days estimate | Probability of success in window |
|---|---|---|---|
| §1 (zero-free region) | None new (already enumerated) | 0d (dead) | 0% |
| §2 (zero density) | Thin-strip density `N(1/2+1/log T, T) = o(T log T)` | research blocker (years), no known route | < 5% |
| §3 (split cluster) | `n_bad(rho_0) = o(log T)` uniformly | research blocker — equivalent to Selberg small-gap | < 5% |
| §4 (worst-case cluster) | `n_cluster(rho_0) = o(log T)` uniformly | research blocker — Selberg / GUE-style | < 5% |
| §5 (Hadamard / Carleman) | Genuine `L^{-1}` positivity mechanism | research blocker | < 1% |
| §6 (partial GRH, truncated form) | Statement adjustment only, no new math | 0.5d (re-statement) | 100% (but doesn't change conditionality) |
| §4.1 (weaken quantifier, bad-set) | Thin-strip zero density at `T^{1-eta}` level | research blocker (years) | < 5% |

**Time to attempt the most promising path** (§3, split-cluster with the
hope of an unconditional `n_bad = o(log T)`): **~3 days to formalize the
gap, 3+ months to attempt the underlying small-gap zero-density bound,
likelihood of success < 10% within one year.**

**Time to do the responsible alternative** (re-state Door B with the
weakest sufficient hypothesis as in §6, document the obstruction, move
on to Doors A/C/D): **~0.5 day write-up.**

## 6. Boundary

### Allowed claims

- Door B currently requires GRH for `L_E^*` for cluster mates of every
  offcentral `rho_0`; the obstruction is structural at the cluster-mate
  step (§2.2 of `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md`).
- The weakest *currently sufficient* hypothesis is GRH for `L_E^*`
  restricted to heights in `[T/2, 4T]` (since cluster mates live there).
- Door B's noncluster step (§2.3) is robust under partial GRH or zero
  density; only the cluster-mate step (§2.2) is the obstruction.
- Path §4.1 (bad-set quantifier weakening) is conceptually correct but
  requires unconditional thin-strip zero density not currently known.

### Forbidden claims

- Door B is closable unconditionally with currently known tools. (False.
  Every attempted restructure traces back to an open problem at least
  as hard as Selberg-small-gap or thin-strip zero density.)
- Unconditional zero-free region (Vinogradov-Korobov / Kim-Sarnak) gives
  the per-mate contraction. (False. Off by a factor `log T`.)
- Replacing the geometric step by a Hadamard / Carleman / maximum-
  principle argument removes GRH. (False. The cluster-mate contribution
  is the same arithmetic inside a log.)
- Door B is the easiest unconditional door. (Door C and Door D, both
  GRH-agnostic by construction, are easier targets for unconditional
  closure.)
- Partial GRH (truncated to height `T^{99/100}`) is unconditionally
  known. (False. The truncated form is also open at the relevant
  height.)

### Genuine surprise

The geometric contraction `sqrt(1+A^2)/R_T < 1` is *exactly tight* to
the alignment `Re rho_j = Re rho_0 = 1/2`. Any deviation of size
`> alpha = 1/log T` in real part breaks the per-mate ratio. The
quantitative gap between known unconditional zero-free regions
(`Re rho_j <= 1 - c/log T`, distance from line `~ 1/2`) and the required
`|beta_j - 1/2| <= alpha = 1/log T` is roughly a factor of `(log T) / 2`
— GRH is essentially the *only* known way to close this gap. The
problem is **not** that unconditional inputs are slightly weaker; they
are off by a *full order of magnitude*. Door B's GRH dependence is
**structural**, not cosmetic.

No published result delivers an unconditional Door B substitute.

## 7. Cross-references

| File | Role |
|---|---|
| `HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` §2.2 | The exact GRH usage line; cluster-mate contraction step |
| `HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md` §2.4 | Noncluster sub-step (robust to partial GRH) |
| `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §5.1 / §5.1' / §13.B | Door B original framing, plus alternative `R > A+1` form |
| `CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md` L160-167 | Repo's Wave-4 cluster-size input (GRH-conditional) |
| `H1_POSITIVE_RANK_CLOSURE.md` L171, L225-227 | Downstream zero-counting use |
| Iwaniec-Kowalski Ch. 5 | Unconditional zero-free / zero-density for GL_n |
| Kim-Sarnak 2003 | GL_2 refined zero-free region |
| Mossinghoff-Trudgian-Yang 2024 | Explicit zero-free constants |
| Selberg `S(T)` / Conrey-Ghosh density-one work | Background for §4 small-gap obstruction |
