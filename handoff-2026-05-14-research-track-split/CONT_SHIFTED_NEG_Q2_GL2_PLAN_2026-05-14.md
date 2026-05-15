---
schema_version: 2
title: "ContShiftNeg_2 GL2 Plan (Stage 2 of Halo Plan, Door A)"
type: plan
domain: project
tier: working
status: PLAN
confidence: 0.80
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/H1_NUMERATOR_M_T_AUDIT_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/CLUSTER_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
supersedes: []
superseded-by:
tags: [halo-route, door-A, ContShiftNeg_2, gl2, stage-2, plan]
---

# Stage 2 — ContShiftNeg_2 GL2 Plan (Door A)

Planning document. Not a proof. Structures existing material from halo plan
§6-§8, the q=2 audit, the BFMT zero-sampling ledger, and the Landau-Gonek
split. Door A is only door of halo plan that is genuine analysis (not
bookkeeping). Stages 0, 1a, 1b closed (GREEN/RIGOROUS_REDUCTION/PASS);
modulo tiny Door B arc-uniformity audit running in parallel, Door A stands
between the project and unconditional offcentral H1.

---

## 1. Verdict and headline target

```text
Target (Door A):
  AllZeroShiftedNeg_2(E):
    sum_{rho in Z_T}^{mult} |L_E^*(rho + 1/log T)|^{-2}  <<  T^{5/2+eps}.

Conjectural truth:   T (log T)^{O(1)}.
Gap:                 3/2 powers of T (loose).
```

Feasibility verdict: **FEASIBLE** at the loose `T^{5/2+eps}` level for fixed
GL2 newform / fixed elliptic curve `E`. Two routes (primary §2, fallback §3);
both are within transcription distance of published zeta technique. See §4
for repo cross-check verdict.

---

## 2. Primary route — ContShiftNeg_2 + Gallagher-Heath-Brown transfer

### 2.1 Continuous moment target

```text
ContShiftNeg_2(E):
  int_T^{2T} |L_E^*(1/2 + 1/log T + it)|^{-2} dt  <<_E  T^{3/2+eps}.
```

Conjectural truth `T (log T)^{O(1)}` = `T^{1+o(1)}`. Target loose by factor
`T^{1/2}`. For zeta the analog is essentially Bui-Florea
(arXiv:2302.07226) unconditional. GL2/EC adaptation: bounded-conductor
analytic transcription; no fundamental obstruction.

### 2.2 Approximate functional equation for `1/L_E^*`

Anchor: Iwaniec-Kowalski Ch. 5 (AFE for general GL_n), halo plan
§5.2 / §6 (block L515-528).

```text
1/L_E^*(s) = D_Y(s) + epsilon(s, 1-s) · D_Y(1-s) + error,
D_Y(s) = sum_{n <= Y} mu_E(n) V(n/Y) / n^s,
Y      = T,    V smooth cutoff.
```

Coefficient bound: `mu_E` is Dirichlet inverse of `lambda_E`, multiplicative.

| Place | Value of `mu_E(p^k)` |
|---|---|
| `mu_E(p) = -lambda_E(p)`, `\|lambda_E(p)\| <= 2` (Deligne) | `\|mu_E(p)\| <= 2` |
| `mu_E(p^k)` for `k >= 2`, good `p` | bounded shape, recursion from Euler factor inverse |
| `mu_E(p^k)`, ramified `p` (finite set for fixed `E`) | bounded by Euler factor structure |
| Crude bound | `\|mu_E(n)\| <= d(n) · 2^{Omega(n)}` (halo plan L527) |

Conductor `C_E(t) = (degree-2 archimedean factor) · N_E^2`. Wave 4 Agent01
gives `log C_E(t) = 2 log T + O_E(1)` for `\|t\| ~ T` (q=2 audit L107-108).
This pins `Y = T` rather than `Y = sqrt(C_E(t)) = T`. AFE balances at
`Y = T` to within `T^{eps}`.

### 2.3 Mean-square of partial sum (good set)

Montgomery-Vaughan / large-sieve for the partial sum:

```text
int_T^{2T} |D_Y(1/2+alpha+it)|^2 dt
 = T sum_{n<=Y} |mu_E(n)|^2 n^{-1-2 alpha} + O(coefficient-l^2 error).
```

Coefficient sum: by multiplicativity,

```text
sum_n |mu_E(n)|^2 / n^{1+2 alpha}
 = prod_p (1 + |mu_E(p)|^2 / p^{1+2 alpha} + ...).
```

For good `p`: `mu_E(p) = -lambda_E(p)`, `|mu_E(p)|^2 = lambda_E(p)^2`.
Rankin-Selberg gives `sum_{p<=X} lambda_E(p)^2 / p = log log X + O(1)`,
so the Euler product is `(log Y)^{O(1)}`. For ramified `p`: finite set,
`O(1)` correction. Bad-prime audit `BFMT-CoefficientErrorCheck(E)`
(`GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md` L40-45) tracks the exact
`(log T)^C` exponent — already known to be polylog from the zero-sample
BFMT substitution audit.

Result for partial sum mean-square: `T · (log T)^{O(1)}` = `T^{1+o(1)}`.
**Loose target `T^{3/2+eps}` has `T^{1/2}` margin against this.**

### 2.4 Cross terms and reflection

Atkinson dissection (Heath-Brown 1981, J. LMS, fractional moments).
Cross integral

```text
int_T^{2T} D_Y(1/2+alpha+it) · conj(epsilon · D_Y(1-1/2+alpha-it)) dt
```

splits into off-diagonal exponential-integral sums `sum_{m,n} mu_E(m)
conj(mu_E(n)) (mn)^{-1/2-alpha} I_{m,n}(T)` where `I_{m,n}(T)` is a
stationary-phase integral. Standard saddle-point bound:
`|I_{m,n}(T)| << T^{1/2}` for `mn ~ T`, `|I_{m,n}(T)| << T^{eps}`
otherwise. Total contribution `<< T^{1/2+eps}` after coefficient l^2.

### 2.5 The near-zero (bad set) cure — Heap-Soundararajan move

**Subtle point:** AFE for `1/L` is **not** a uniform pointwise upper
bound on `|L|^{-1}`; near zeros of `L` on the shifted line `Re s =
1/2+alpha`, `|L|^{-1}` blows up while the AFE main terms remain modest.
Cure (halo plan §6 L560-580):

```text
Split [T, 2T] = G cup B,
B = { t in [T,2T] : |L_E^*(1/2+alpha+it)| < V },
V = (log T)^{-A},     A to be calibrated.
```

| Set | Bound used | Source |
|---|---|---|
| `G` (good) | mean-square of `D_Y` (§2.3) | Montgomery-Vaughan + coeff l^2 |
| `B` (bad), measure | `\|B\| · V^{2k} <= int_T^{2T} \|L\|^{2k}` (Markov, k integer) | k=1: Rankin-Selberg / standard 2nd moment; k=2: GL2 fourth moment — Iwaniec-Kowalski Ch. 24, or Conrey-Iwaniec Annals 2000 |
| `B` (bad), pointwise | `\|L\|^{-1} <= T^{O(1)}` from FE + convexity | classical (`|L(s)| >= C T^{-(degree)/4}` on shifted line via FE) |

Bad-set integral budget:

```text
int_B |L|^{-2} dt <= |B| · T^{O(1)} <= T · V^{2k} · T^{O(1)} / T^{?}.
```

Calibrate `V`, `k` for loose target. **At `k = 1`** (= q=2 positive
2nd moment, Rankin-Selberg, no GL2 4th moment needed):

```text
int_T^{2T} |L|^2 dt << T (log T)^{O(1)},
|B| << T (log T)^{O(1)} · V^{-2}.
```

Pick `V = T^{-1/4}` (well above the trivial floor `(log T)^{-A}`):

```text
|B| << T (log T)^{O(1)} · T^{1/2} = T^{3/2 + o(1)}.
int_B |L|^{-2} <= |B| · V^{-2} = T^{3/2 + o(1)} · T^{1/2} = T^{2 + o(1)}.
```

Too loose. Use `k = 2` (GL2 4th moment, Iwaniec-Kowalski Ch. 24): for
fixed-conductor GL2 the t-aspect 4th moment is

```text
int_T^{2T} |L_E^*(1/2+it)|^4 dt << T^{1+eps}     (conjectural; what is
                                                  proved unconditionally
                                                  for fixed GL2 is
                                                  T^{2+eps}, Good 1982,
                                                  Meurman; see I-K
                                                  Ch. 24).
```

Use the **unconditional** GL2 4th moment `T^{2+eps}`:

```text
|B| << T^{2+eps} · V^{-4}.
int_B |L|^{-2} <= |B| · V^{-2} = T^{2+eps} · V^{-6}.
```

Pick `V = T^{-1/8}`:

```text
|B| << T^{2+eps} · T^{1/2} = T^{5/2+eps},
int_B |L|^{-2} <= T^{2+eps} · T^{3/4} = T^{11/4+eps}.
```

Still over `T^{3/2}` target — but **the trivial pointwise** `|L|^{-1} <=
T^{O(1)}` is wasteful. Replace by **Soundararajan upper-bound technique**
(Annals 2009 / Soundararajan-Selberg): on `B`, conditional on a positive
moment hierarchy, `|L|^{-1}` cannot be huge generically. Halo plan §6
L580 marks this as the right adaptation for GL2 with bounded conductor.

**Alternative cleaner calibration** (Heap-Li-Zhao + Bui-Florea):
short-interval negative moments via Selberg-Soundararajan upper-bound
technique. Bui-Florea arXiv:2302.07226 closes the zeta analog of
`ContShiftNeg_2` at `T^{1+eps}` unconditionally — fifteen halves below
loose target. Conjectural-truth-quality bound; loose-target `T^{3/2+eps}`
has `T^{1/2}` margin. For GL2 / fixed-conductor newform: same machinery,
needs:

- Selberg-Soundararajan upper-bound technique on `log |L|` (Annals 2009).
- Unconditional 4th moment of `|L|` (Iwaniec-Kowalski Ch. 24).
- Standard mollifier (Conrey-Iwaniec Annals 2000, for GL2).
- Functional equation + Hadamard convexity.

All ingredients classical; bounded-conductor GL2 inherits them with
explicit constants. **Loose-target margin allows considerable slop.**

### 2.6 Transfer continuous → zero-sampled (Gallagher-Heath-Brown)

Anchor: halo plan §6 L420-432.

```text
Gallagher-HB lemma:
  sum_{rho : T < gamma <= 2T}^{mult} |g(gamma)|^2
   <<  log T  int_T^{2T} |g(t)|^2 dt
    +  (log T)^{-1}  int_T^{2T} |g'(t)|^2 dt.
```

Apply with `g(t) = L_E^*(1/2+alpha+it)^{-1}`.

| Term | Treatment |
|---|---|
| `g(t)`-term: `log T · int \|g\|^2` | `= log T · ContShiftNeg_2(E)` `<< T^{3/2+eps} · log T` |
| `g'(t)`-term: `(log T)^{-1} · int \|g'\|^2` | `g'(t) = -i L'/L · L^{-1}`; bound via Cauchy-Schwarz |

`g' = -i (L'/L) g`, so `|g'|^2 = |L'/L|^2 |g|^2`. Cauchy-Schwarz:

```text
int_T^{2T} |L'/L|^2 |g|^2 dt
 <=  (int |L'/L|^4 dt)^{1/2}  ·  (int |g|^4 dt)^{1/2}
 =   (int |L'/L|^4 dt)^{1/2}  ·  (int |L|^{-4} dt)^{1/2}.
```

| Factor | Unconditional bound for fixed GL2 |
|---|---|
| `int_T^{2T} \|L'/L\|^4 dt` | Mertens-type / log-derivative 4th moment: `T (log T)^{O(1)}` (classical, follows from Hadamard product + zero density on shifted line at distance `alpha`) |
| `int_T^{2T} \|L\|^{-4} dt` = `ContShiftNeg_4(E)` | analogous `T^{?+eps}`; loose bound `T^{2+eps}` from same Heap-Soundararajan with `k=2` |

If `ContShiftNeg_4(E) << T^{2+eps}`:

```text
int |g'|^2 <= (T log T)^{1/2} · T^{1+eps} = T^{3/2+eps}.
(log T)^{-1} · int |g'|^2 << T^{3/2+eps} · (log T)^{-1}.
```

Sum:

```text
sum_{rho}^{mult} |L(rho+alpha)|^{-2} << T^{3/2+eps} log T + T^{3/2+eps}
                                     << T^{3/2+eps}.
```

**Transfer eats nothing past `log T`.** Final bound `T^{3/2+eps}`,
**a full `T^{1}` below the Door A loose target `T^{5/2+eps}`**.

Even pessimistic transfer (eating up to `T^{1/2}` from a worse
`g'`-term): final `T^{2+eps}`, still `T^{1/2}` below target. Halo plan
risk register R2 (transfer eats `T^{1/2}`) is **comfortably absorbed**.

### 2.7 Source list and adaptation difficulty

| Source | Statement | Gap to fixed-conductor GL2 |
|---|---|---|
| Bui-Florea arXiv:2302.07226 | Unconditional neg moments of zeta on shifted line, `T^{1+eps}` | Transcribes; bounded-conductor newform inherits |
| Heap-Li-Zhao arXiv:2107.06829 | Lower bounds (one-sided), neg moments | Companion to Bui-Florea |
| Soundararajan Annals 2009 | Moments of zeta, Selberg-Sound upper-bound technique | Adapts to GL2 with bounded conductor (Mertens + Rankin-Selberg substitutes) |
| Heath-Brown J. LMS 1981 | Fractional moments of zeta | Atkinson dissection, classical 2nd-moment method |
| Iwaniec-Kowalski Ch. 5 | GL_n L-functions, AFE for general degree | Direct |
| Iwaniec-Kowalski Ch. 24 | GL2 4th moment, t-aspect | Direct; unconditional `T^{2+eps}` (Good 1982, Meurman) |
| Conrey-Iwaniec Annals 2000 | Cubic moment, mollifier for GL2 | Mollifier source for §5.1 rectangle + mollified 2nd moment |
| Milinovich-Ng arXiv:1306.0854 | Fixed newform reciprocal-derivative moments | Most directly transferable for §3 fallback |
| Bui-Florea-Milinovich-Turnage-Butterbaugh arXiv:2310.03949 (BFMT) | Negative moment ledger, k=1/2 used in repo | Already partially transcribed (zero-sample audit) |

**Adaptation difficulty:** transcription, not new theorem. Every
ingredient has GL2-fixed-conductor version published or routine extension.
Estimated `2-3 weeks` focused work (halo plan L596-598).

---

## 3. Fallback route — direct zero-sample BFMT k=1

If transfer route hits unexpected obstruction (e.g., `ContShiftNeg_4(E)`
worse than `T^{2+eps}`), pivot to direct zero-sample BFMT with `k=1`. Repo
already passes this **conditionally** at q=2 for the bad-set `S_E(T)`
(`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md`).

### 3.1 Sample `1/L` at zeros via AFE

```text
sum_{rho in Z_T}^{mult} |L(rho+alpha)|^{-2}
 = sum_{rho}^{mult} |D_Y(rho+alpha) + reflection + error|^2.
```

Expand. Diagonal:

```text
sum_{rho}^{mult} sum_n |mu_E(n)|^2 / n^{1+2 alpha}
 = (#Z_T^{mult}) · sum_{n<=Y} |mu_E(n)|^2/n^{1+2 alpha}
 << T log T · (log T)^{O(1)}
 =  T (log T)^{O(1)}.
```

### 3.2 Off-diagonal via Landau-Gonek for GL2

Cite `GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md` Layer 1 (source-closed
for holomorphic newforms via Milinovich-Ng Lemma 3.3). For `m != n`:

```text
sum_{rho : T<gamma<=2T} (m/n)^{i gamma}
 ~ -T Lambda_E(m/n)/(2 pi) · (m/n)^{-1/2}
    + O( |m/n| log(|m/n| T) loglog T )    (Milinovich-Ng L3.3, GL2 form,
                                            transcribed via Wave 4 conductor
                                            normalization).
```

Off-diagonal sum: BFMT Lemma 2.4 plus Propositions 2.5-2.7, zero-sample
substitution at `k=1` (i.e., q=2). All four BFMT layers already pass
`(log T)^{O(1)}` substitution audit at `k=1/2`; the `k=1` extension is
the immediate next step in the BFMT ledger (BFMT-EC-Transcription).

### 3.3 Reflection + error

BFMT Props 2.5, 2.6, 2.7 (PDF p. 11-16). Error from AFE smoothing:
`O(T^{1+eps})`; reflection: handled by FE symmetry plus Propositions 2.5-2.7
applied to the dual sum.

### 3.4 Multiplicity-aware

For fixed GL2 newform, multiplicity at offcentral height bounded by
Riemann-von Mangoldt:

```text
mult(rho) <= O(log T)   for rho with |gamma| in [T, 2T].
```

Multiplicity-weighted sum: each `rho` counted with weight `m(rho)`. Worst-
case inflation: total weight `sum m(rho) <= #Z_T (counted simply) ·
O(log T) << T (log T)^2`. Absorbed by `T^{eps}`. **The simple-zero result
at `T^{5/2+eps}` automatically extends to multiplicity-weighted with
unchanged exponent.**

### 3.5 Cost estimate

```text
3-4 weeks (halo plan L646-647).
vs primary route: 2-3 weeks.
```

Fallback is slightly more expensive only because of the additional BFMT
ledger source-close work; the analytic content is the same.

---

## 4. Independent cross-check — is Door A already conditionally proved?

**Most important question of this plan.**

The q=2 audit (`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L34-37,
L77, L147) gives:

```text
Degree2WeakShiftedNeg_2(E):
  sum_{rho in S_E(T)} |L_E^*(rho+1/log T)|^{-2}  <<_{E,eps}  T^{5/2+eps},

S_E(T) = { simple critical zeros rho = 1/2 + i gamma : T < |gamma| <= 2T },

conditional on:
  GL2-BFMT-PrimePolynomialLowerBound(E) in conductor-normalized form,
  ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1),
  fixed-newform RH/explicit-formula normalization.
```

Door A target (halo plan L230-232):

```text
AllZeroShiftedNeg_2(E):
  sum_{rho in Z_T}^{mult} |L_E^*(rho + 1/log T)|^{-2}  <<  T^{5/2+eps},

Z_T = nontrivial zeros with |Im rho| <= T (no simplicity restriction).
```

### 4.1 The gap, sharp

| Aspect | q=2 audit | Door A |
|---|---|---|
| Domain | simple critical zeros in dyadic shell `(T, 2T]` | all nontrivial zeros up to height `T` |
| Simplicity | restricted to simple | all multiplicities |
| Multiplicity weight | each zero counted once | counted with multiplicity |
| Critical-line restriction | yes (via cluster framework) | implicit (zeros assumed on critical line under standing GRH) |
| Shell vs cumulative | dyadic `(T, 2T]` | cumulative `[0, T]`; standard dyadic decomposition reduces to shells |
| Conditional? | yes — Wave 4 GL2 local inputs + zero-sample transcription | sought unconditional |

### 4.2 What is the genuine gap?

The exponent `5/2+eps` matches Door A exactly. Three differences are
real obstructions:

```text
(a) Simple vs multiple zeros: q=2 audit restricts to S_E(T) = simple
    critical zeros. Door A wants all zeros with multiplicity. For fixed
    GL2 newform, offcentral multiplicity is bounded by O(log T) at height
    T (Riemann-von Mangoldt), so multiplicity-weighting inflates by at
    most a polylog factor. ABSORBED BY T^{eps}.

(b) The audit is over the BAD set (close-cluster) only in name (S_E
    contains all simple zeros of the dyadic shell, not just bad-set
    ones). Re-reading L62-74 of H1_SIMPLE_ZERO_CONDITIONAL_STACK
    confirms: S_E(T) is the FULL set of simple critical zeros in the
    shell; F_E and B_E are subsets. So the audit covers all simple zeros
    of the shell, NOT only B_E.

(c) Conditional on Wave 4 local inputs:
       GL2-BFMT-PrimePolynomialLowerBound(E),
       ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1),
       fixed-newform RH/explicit-formula normalization.
    These are the SAME conditionals Door A must remove. Promoting from
    'conditional pass' to 'unconditional' = closing exactly these
    sources.
```

### 4.3 Verdict

**Door A is conditionally proved in the repo's q=2 audit, modulo:**

```text
(i)  extension from simple zeros to multiplicity-weighted (cost: O(log T)
     polylog; absorbed by T^{eps}; standard Riemann-von Mangoldt local
     mult bound) — ESSENTIALLY FREE;

(ii) source-closing the Wave 4 GL2 local inputs to unconditional:
     - GL2-BFMT-PrimePolynomialLowerBound(E): conditional on Wave 4
       Agent01 transcription audit (degree-2 conductor normalization);
     - ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1): currently at
       k=1/2 in the substitution audit (RIGOROUS_REDUCTION). Extension
       k=1/2 -> k=1 is the immediate next step;
     - fixed-newform RH/explicit-formula normalization: already a
       standing framework assumption in the halo route (GRH for L_E^*).
```

**This collapses Stage 2 from a 2-3 week sprint to a `source-closing
audit` of roughly the same duration but DIFFERENT character: instead of
adapting Bui-Florea / Soundararajan from zeta to GL2, the task is to
promote three already-stated conditional Wave 4 BFMT inputs to
unconditional. The analytic content needed is the same, but the bookkeeping
is much closer to closure than a Stage-2 sprint suggests.**

### 4.4 Recommended Stage-2 framing after this cross-check

Two parallel tracks, low risk:

```text
Track 1 (primary, ~2 weeks):
  Promote the Wave 4 conditionals to unconditional. Three sub-audits:
   - Wave 4 Agent01 GL2-BFMT prime polynomial lower bound (already
     written; verify the transcription is k=1 ready).
   - ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1) extension
     from k=1/2 (already at RIGOROUS_REDUCTION).
   - Multiplicity extension (§3.4 above).

Track 2 (insurance, ~1 week):
  Sketch the Bui-Florea / Soundararajan ContShiftNeg_2 GL2 adaptation
  AT THE CONTINUOUS LEVEL for §2.1, as an independent witness. If the
  Wave 4 path stalls, Track 2 becomes primary at a cost of 1-2 more
  weeks.
```

Total estimated cost: **2-3 weeks of mostly source-closing work, NOT a
fresh research sprint.**

---

## 5. Side angles (lower priority)

### 5.1 Direct rectangle + mollified second moment

Halo plan §7 / §8.1 (L690-707). Replace halo (union of disks) with single
thin rectangle `1/2 - alpha <= Re s <= 1/2 + alpha`, `T <= Im s <= 2T`.
Cleaner geometry; reduces residue aggregate to a *continuous* shifted
moment directly:

```text
sum_{rho} Res = (1/(2 pi i)) int_{partial rectangle} Phi_T(s)/L(s) ds.
```

Avoids halo-arc partitioning entirely; one-page proof if ContShiftNeg_2
closes. **Adopt for paper write-up once §2 is closed.**

Mollifier extension: bound

```text
int |1/L|^2 = int |LM/L^2|^2 / |M|^2  ~  int |LM|^2 · sup |1/(ML)|^2.
```

For Conrey-Iwaniec mollifier `M` of length `T^{theta}`, `int |LM|^2 ~ T`;
sup bounded on a good set. Iwaniec-Soundararajan technique for t-aspect
GL2.

### 5.2 Subharmonic three-circles patch

Halo plan §8.5 (L781-794).

```text
log|L| subharmonic. Hadamard three-circles across strip of width O(alpha):
log|L(1/2+alpha+it)|^{-1}
 <= (1/2) log|L(1/2+2 alpha+it)|^{-1}
  + (1/2) log|L(1/2+it)|^{-1}
  + (boundary terms).
```

First term: `|L|^{-1}` deeper in convergence half-plane, polynomial RS
lower bound on `|L|`. Self-referential in second term; iterative
bootstrap with positive 4th moment sometimes gives gain. **Hold as patch
if §2.6 hits unexpected wall on `int|g'|^2`.**

### 5.3 Halo with weighted boundary

Halo plan §8.6 (L796-803). Weighted halo radius `R_rho` depending on
`rho`: large where `|L|` is large on the boundary, small where small.
Sobolev-type optimization, potential gain when offcentral zeros are
highly clustered. **Future paper-quality optimization, not Stage 2.**

---

## 6. Risk register and abort criteria

Halo plan §9 (L808-839), updated for post-Stage-1 state.

| Risk | Probability (halo plan) | Probability (post-Stage-1) | Mitigation |
|---|---|---|---|
| R1: ResidueFirstH1Rewrite fails | 0.20 | **RETIRED** (Stage 0 GREEN) | density-method (8.3) kept as safety net |
| R2: ContShiftNeg_2 unconditional value > `T^{3/2}` | 0.10 | 0.10 unchanged | §3 fallback (zero-sample BFMT k=1), or weaken halo to q=3 |
| R3: HaloShiftComparison breaks at boundary-arc level | 0.05 | **RETIRED** modulo tiny uniformity audit (Stage 1a RIGOROUS_REDUCTION) | cluster-resummed finite-box (§3.4 of halo plan) |
| R4: `M_T` not `o(T^{1/4})` | 0.05 | **RETIRED** (Stage 1b PASS, margin `T^{9/4}`) | none needed |
| R5 (new): §4 cross-check shows Door A already proved conditionally but Wave 4 inputs cannot be source-closed unconditionally | 0.10 | 0.10 | pivot Track 2 of §4.4 to primary; full Bui-Florea / Soundararajan adaptation |

**Hard abort:** unconditional value of `int |L_E^*|^{-2}` on shifted
line for fixed GL2 found `>= T^{5/2}`. Probability `~0.02`. Would mean
zeta-side technique fails to transfer — fall back to Palm route.

---

## 7. Cost estimate and milestones

```text
Week 1:
  - Read Wave 4 Agent01 transcription audit (GL2-BFMT prime polynomial
    lower bound) in detail.
  - Verify k=1/2 -> k=1 extension of ZeroSample-Homogeneous-BFMT-
    CoefficientDPMV is clean (no new combinatorial obstacle).
  - Write multiplicity-extension sub-audit (§3.4): Riemann-von Mangoldt
    local mult bound + polylog absorption.
  - Output: AllZeroShiftedNeg_2_MULT_EXTENSION_2026-MM-DD.md.

Week 2:
  - Promote Wave 4 conditionals: write the k=1 BFMT transcription with
    all four layers (LG-Explicit-GL2, DPMV-GL2-GeneralA, DPMV-GL2-
    PrimePowerHighMoment, BFMT-CoefficientErrorCheck) source-closed
    for fixed GL2 newform.
  - Output: BFMT_EC_TRANSCRIPTION_K_ONE_2026-MM-DD.md.

Week 3:
  - Synthesize: AllZeroShiftedNeg_2(E) unconditional theorem.
  - Output: ALL_ZERO_SHIFTED_NEG_2_E_2026-MM-DD.md.
  - Begin Track 2 (insurance): sketch Bui-Florea / Soundararajan
    continuous-level adaptation for §2.

Week 4 (buffer):
  - If Track 1 stalls on any Wave 4 conditional, pivot to Track 2.
  - Otherwise: assemble §5 (Door A + B + C + D) and write the
    UNCONDITIONAL_H1_OFFCENTRAL_2026-MM-DD.md synthesis.
```

Sources to chase (full text, not yet in repo extraction):
- Bui-Florea arXiv:2302.07226 (zeta negative moments).
- Heap-Li-Zhao arXiv:2107.06829 (lower bounds, negative moments).
- Soundararajan Annals 2009 (moments of zeta).
- Iwaniec-Kowalski Ch. 5, Ch. 24 (AFE for GL_n, GL2 4th moment).

Sources to transcribe (already in repo extraction, need k=1 promotion):
- BFMT arXiv:2310.03949 (Props 2.5-2.7 at k=1).
- Milinovich-Ng arXiv:1306.0854 (Lemma 3.3, Proposition 4.1).

Sources to adapt (zeta -> bounded-conductor GL2):
- Heath-Brown 1981 J. LMS (Atkinson dissection at GL2 length-T sums).
- Conrey-Iwaniec Annals 2000 (mollifier for GL2; already familiar).

---

## 8. Decision gates

```text
Gate 1 (end of Week 1):
  Pass: k=1/2 -> k=1 extension of CoefficientDPMV clean.
        Multiplicity extension absorbed by T^{eps}.
        Proceed to Week 2 (Wave 4 promotion).
  Fail: pivot immediately to Track 2 (Bui-Florea / Soundararajan
        continuous-level adaptation); Stage 2 extends to 4-5 weeks total.

Gate 2 (end of Week 2):
  Pass: BFMT-EC-Transcription(E, k=1) source-closed unconditionally for
        fixed GL2 newform.
        Proceed to Week 3 synthesis.
  Fail: identify which BFMT layer is the blocker; if Layer 4 (Coefficient
        ErrorCheck), pivot to §2.5 Heap-Soundararajan bad-set cure as
        replacement.

Gate 3 (end of Week 3):
  Pass: AllZeroShiftedNeg_2(E) unconditional theorem.
        Combine with Stages 0/1a/1b/4 for full halo synthesis.
  Fail: drop to density-method (8.3) side-quest as alternative
        unconditional route; revisit Door A in subsequent sprint.

Hard abort (any week):
  Unconditional value of int |L_E^*|^{-2} on shifted line found
  >= T^{5/2}. Fall back to Palm route.
```

---

## 9. Boundary

### Allowed to claim now

```text
Door A target T^{5/2+eps} is loose by 3/2 powers of T against
conjectural truth T^{1+o(1)}. For fixed GL2 newform / fixed EC of
bounded conductor, this is feasible unconditionally via two routes:
  (a) ContShiftNeg_2 continuous + Gallagher-HB transfer
      (Bui-Florea / Soundararajan / Heap-Li-Zhao adaptation);
  (b) Direct zero-sample BFMT at k=1 (extension of repo audit at k=1/2).
```

```text
The repo q=2 audit (Degree2WeakShiftedNeg_2(E)) already conditionally
gives the Door A bound at exactly the same exponent T^{5/2+eps}, over
the simple critical zeros of a dyadic shell. The gap to Door A is:
  (i) extension to multiplicity-weighted: absorbed by T^{eps} via
      Riemann-von Mangoldt local mult bound;
  (ii) promotion of Wave 4 local GL2 inputs from conditional to
       unconditional: the same source-closing problem identified by
       Stage 2 of the halo plan, but framed as ledger promotion rather
       than fresh analytic sprint.
Stage 2 effective cost is therefore 2-3 weeks of source-closing audit,
not a fresh analytic sprint.
```

```text
Risks R1, R3, R4 of halo plan §9 are RETIRED by Stages 0, 1a, 1b.
Only R2 (transfer eats more than T^{1/2}) and R5 (Wave 4 conditionals
not promotable) remain at probability ~0.10 each. Hard-abort
probability ~0.02.
```

### Not allowed to claim

```text
AllZeroShiftedNeg_2(E) is unconditionally proved.
ContShiftNeg_2 for GL2 is in the literature.
The Wave 4 conditionals are unconditionally closed.
The k=1 extension of BFMT zero-sample substitution is written.
Unconditional offcentral H1 for fixed E.
The repo q=2 audit covers Door A as stated (it covers a strict subset
  — simple zeros only — and is conditional).
```

### Confidence breakdown

```text
0.80  primary route feasible at T^{5/2+eps} via Track 1
      (Wave 4 promotion + multiplicity extension)
0.10  primary route stalls on Wave 4 promotion; Track 2 (Bui-Florea /
      Soundararajan adaptation) is the actual sprint
0.08  fallback route §3 (zero-sample BFMT k=1) is needed instead of §2
0.02  hard abort (zeta-side technique fails to transfer)
```

---

## 10. Cross-references

| File | Role |
|---|---|
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §6-§8, §11, §12 | source plan |
| `handoff-2026-05-14-research-track-split/H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` | Stage 0 (Door C) GREEN |
| `handoff-2026-05-14-research-track-split/HALOSHIFTCOMPARISON_LEMMA_2026-05-14.md` | Stage 1a (Door B) RIGOROUS_REDUCTION |
| `handoff-2026-05-14-research-track-split/H1_NUMERATOR_M_T_AUDIT_2026-05-14.md` | Stage 1b (Door D) PASS |
| `handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` | conditional q=2 over `S_E(T)`; §4 cross-check |
| `handoff-2026-05-11-post-wave5-pivot/H1_SIMPLE_ZERO_CONDITIONAL_STACK_2026-05-11.md` L43-130 | simple-zero conditional stack |
| `handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` | k=1/2 BFMT substitution audit (RIGOROUS_REDUCTION) |
| `handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` | k=1/2 EC transcription, target of k=1 promotion |
| `handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md` | LG-Explicit-GL2 source-closed via Milinovich-Ng L3.3 (used by §3.2) |
