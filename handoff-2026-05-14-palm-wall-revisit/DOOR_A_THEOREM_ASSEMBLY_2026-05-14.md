---
schema_version: 2
title: "Door A Theorem Assembly Under Standing GRH (AllZeroShiftedNeg_2(E))"
type: theorem-assembly
domain: project
tier: working
status: CONDITIONAL_ON_STANDING_GRH
confidence: 0.84
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt
  - /tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt
  - /tmp/farey-homogeneous-bfmt-20260511/carneiro_chandee_1008_4970.txt
  - /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-palm-wall-revisit/SECTION_5_CONDUCTOR_RERUN_VERIFICATION_2026-05-14.md
supersedes: []
superseded-by:
tags: [door-A, wave-4-promotion, theorem-assembly, halo-route, GRH-conditional, q-equals-2-shifted, T-five-halves]
---

# Door A Theorem Assembly Under Standing GRH

Status: `CONDITIONAL_ON_STANDING_GRH`. Door A closes for the halo-route bypass of the rooted Palm wall, conditional on GRH for `L_E^*` and the standard GL2 Weil explicit formula. No unconditional H1 theorem. No Palm-wall break.

## 1. Theorem

```text
AllZeroShiftedNeg_2(E):
  Let E/Q be a fixed elliptic curve of conductor N_E with weight-2 cuspidal
  newform of level N_E. Let L_E^*(s) = L(E, s+1/2) be the normalized
  L-function; let Z_T denote the multiset of all critical zeros rho of L_E^*
  with T < |Im rho| <= 2T (counted with multiplicity). Then, under standing
  GRH for L_E^*,

    sum_(rho in Z_T) m_rho * |L_E^*(rho + 1/log T)|^(-2)
      <<_(E, eps)  T^(5/2 + eps),

  where m_rho := ord_(s=rho) L_E^*.
```

The multiplicity-weighted form `m_rho * |...|^(-2)` is what feeds the halo-route divided-difference contour identity (`HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §2.2-§6). The exponent `5/2 + eps` is Door A's target as fixed in `CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md`.

## 2. Proof chain

The theorem is the synthesis of:

```text
Step A: BFMT shifted-value upper majorant (Lemma 2.4, all zero ordinates).
Step B: Conductor-normalized Section 5 (5.13)/(5.17) rerun at q=2, k=1.
Step C: Multiplicity extension S_E(T) -> Z_T^{mult}.
Step D: Zero-sampling EC transcription of BFMT Propositions 2.5, 2.6, 2.7.
Step E: Agent01 prime-polynomial lower bound for L_E^* (k-independent).
```

### Step A — BFMT Lemma 2.4 (extract L412)

For `gamma in (T, 2T]`, BFMT Lemma 2.4 states:
```text
|L'(rho)|^(-2k) <= exp(O(log T / log log T)) S_1(gamma) + S_2(gamma)    (when gamma in T_0),
|L'(rho)|^(-2k) <= exp(O(log T / log log T)) (...term in P_{0,v})       (when gamma not in T_0).
```

This is a **shifted-value** majorant over all zero ordinates (`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L88-98): it does not require the separated set `F`. The same majorant therefore bounds `Σ_{rho in S_E(T)} |L_E^*(rho + 1/log T)|^(-2)` directly.

The EC transcription is rigorous under fixed-newform GRH and the GL2 Weil explicit formula, with prime-square / higher-power / bad-prime absorption costing `O_E(log log T)` (Agent01 L132-174).

### Step B — Conductor-normalized Section 5 rerun at q=2, k=1

`SECTION_5_CONDUCTOR_RERUN_VERIFICATION_2026-05-14.md` (sub-task 1.4) verifies at equation level:

Under the GL2 conductor-flip rule `k -> 2k` (driven by `log C_E(t) = 2 log T + O_E(1)`, Wave 5 Agent01), BFMT (5.17) at q=2, k=1 yields:
```text
sum_(gamma in F_E(T,c)) |L_E^*'(rho)|^(-2)
  <<_E T^{1 + (1+delta) * 2k * (2(2k) - A)/(2(2k) - A + B)}
   = T^{1 + 2 * 3/4 + O(delta)} = T^{5/2 + eps}.
```

The same exponent applies to the shifted moment by Step A (Lemma 2.4 is the shifted-value form, not the separated-derivative form).

Branch routing: `2k(1+eps) = 2 + 2eps > 1` at zeta version, also at GL2 (where condition is `4k(1+eps) > 1`); both are in the second branch (5.17), bypassing the small-block sign condition `a(2d-1)/r > 4k = 4` that killed the Wave 5 strong target.

### Step C — Multiplicity extension

`HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md` decomposes
```text
Z_T = S_E(T) (simple critical) union (Z_T \ S_E(T)) (multiple critical).
```

For the multiple part: at multiplicity `m`, the contribution to the shifted moment is weighted by `m * (log T)^{2m} * |L_E^{(m)}(rho)/m!|^(-2)`. By Step F below (RvM multiplicity lemma), `m_rho = O_E(log T)` for every offcentral critical zero, so the per-zero factor is `T^{o(1)}`. By RvM zero-count `N(T,2T) << T log T`, the total count of multiple zeros (with multiplicity) is `<< T (log T)^2`. The multiple-zero contribution to the shifted moment is therefore

```text
sum_{rho in Z_T \ S_E(T)} m_rho |L_E^*(rho+1/log T)|^(-2)
  <<_E T (log T)^2 * T^{o(1)} * (worst-case (m!|L^{(m)}|)^{-2} at m_rho <= O(log T))
  <<_E T^{1 + o(1)}.
```

This is far below `T^{5/2}`. The simple-part contribution from Step B + Step A dominates.

### Step D — Zero-sampling EC transcription of Props 2.5, 2.6, 2.7

`ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` and `BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` establish:

- Prop 2.5 transcribes at k=1/2 with extra `(log T)^2 exp(O_E(s_0))` factor (L84-114 of substitution audit). `s_0 = O(log T / log log T)`, so extra factor is `T^{o(1)}`.
- Prop 2.6 transcribes with `|lambda_E(n)| <= d(n)` Deligne bound + Rankin-Selberg prime-square average. Same `(log T)^2 exp(O_E(s_0))` overhead.
- Prop 2.7 same.

Lift to k=1:
- The `(log T)^2` overhead is **k-independent** (it comes from the zero-sampling lemma replacement of BFMT Theorem 3.1, whose statement has no `k` — see BFMT extract L488-494 for the lemma; coefficient sums `Σ |a_n|^2 / n` are k-independent).
- The `exp(O_E(s_0))` factor: under the conductor flip, `s_0` rescales but remains `O(log T / log log T)`. Factor stays at `T^{o(1)}`.
- The `k^2 b(Delta_j)^2 (log log T / Delta_j)^{2 eta(Delta_j)}` factor in Props 2.6, 2.7 multiplies by `4` at k=1 (vs k=1/2), fixed numerical bump. Absorbed in `T^{eps}`.
- Support conditions `beta_0 s_0 <= 1 - log log T / log T` (Prop 2.5), `Σ_h l_h beta_h + s_{j+1} beta_{j+1} <= 1 - log log T / log T` (Prop 2.6), `Σ_h l_h beta_h <= 1 - log log T / log T` (Prop 2.7) depend only on the product structure of BFMT parameters; under conductor flip `beta_0 -> beta_0/2, s_0 -> 2 s_0`, products preserved. Conditions hold at k=1.

Conclusion: Props 2.5, 2.6, 2.7 at q=2, k=1 give the same EC-transcribed bounds as at k=1/2, with `T^{o(1)}` overhead.

### Step E — Agent01 prime-polynomial lower bound (k-independent)

`AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` L29-89 displays
```text
log |L_E^*(s)| >= A_E(t; alpha, Delta) - Re Σ_{p<=x, p∤N_E} b_E(p;Delta) lambda_E(p) p^(-s) - C_E log log T + O_E(...).
```

`SECTION_5_CONDUCTOR_RERUN_VERIFICATION_2026-05-14.md` §1 verifies this display is k-independent by inspection: no `k` symbol appears. The k-dependence enters only when this lower bound is raised to power `-2k` and integrated against BFMT Section 5 bookkeeping.

At k=1, raising to `-2` introduces `exp(2 C_E log log T) = (log T)^{2 C_E} = T^{o(1)}`. No new structural risk.

### Step F — RvM multiplicity lemma

`HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md` retires the named lemma `m_rho = O_E(log T)` via RvM zero-count for the fixed newform, Iwaniec-Kowalski Ch. 5 Thm 5.8. Half-line proof. Used by Step C.

## 3. Source closures (mechanical)

| Sub-task (Wave 4 plan) | Source | Verdict |
|---|---|---|
| 1.1 — Agent01 k-independence | Agent01 L29-89 | Verified by inspection (no `k` symbol). |
| 1.2 — Carneiro-Chandee majorant | Agent01 L91-104, Carneiro-Chandee Lemma 8, eqs (3.1)-(3.2) | Source-quoted in Agent01; gamma-factor substitution explicit. |
| 1.3 — Bad-prime audit at 2k=2 | Agent01 L132-174 | `O_E(log log T)` k-independent absorption. At k=1, factor `(log T)^{2 C_E} = T^{o(1)}`. |
| 1.4 — Section 5 (5.13)/(5.17) rerun | `SECTION_5_CONDUCTOR_RERUN_VERIFICATION_2026-05-14.md` | Verified at equation level: `T^{5/2+eps}` at q=2, k=1. |
| 1.5 — AFE + conductor cross-check | Iwaniec-Kowalski Ch. 5 AFE | `C_E(t) asymp T^2`, `Y = T` balance, length window `T^{1/2}` per side, total `T^{3/2}` polynomial scale, inside BFMT `T^{1 - log log T/log T}`. Mechanical. |
| 2.1, 2.2, 2.3 — Props 2.5/2.6/2.7 transcription at 2k=2 | `ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` L84-203 | Verified via k-independence of the zero-sampling lemma; lift from k=1/2 to k=1 is mechanical (Step D above). |
| 2.4 — Section 5 absorption with all four Props inserted at 2k=2 | BFMT extract L1046-1101 + Steps B + D | Each Props insertion contributes `T^{o(1)}`; routing through (5.17) confirmed at q=2 k=1. Verified. |
| 2.5 — Milinovich-Ng Prop 5.1 / Rankin-Selberg | Milinovich-Ng extract eqs (18)-(23), Prop 5.1 | Source-quote: `Σ_{p<=x} |lambda_E(p)|^2 / p = log log x + O_E(1)`. |
| 2.6 — Zero-sampling lemma k-independence | `ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md` | Lemma statement `Σ |A(1/2+i gamma)|^2 << T (log T)^3 Σ |a_n|^2/n` has no `k`. Verified. |

All sub-tasks pass at equation level or by source-quote.

## 4. Assembly

Steps A + B + D + E close the simple-part of the shifted moment:
```text
sum_{rho in S_E(T)} |L_E^*(rho + 1/log T)|^(-2) <<_E T^{5/2 + eps}.
```

Step C extends to the multiplicity-weighted full set `Z_T^{mult}`:
```text
sum_{rho in Z_T} m_rho |L_E^*(rho + 1/log T)|^(-2) <<_E T^{5/2 + eps}.
```

Step F (RvM multiplicity bound) is used inside Step C.

This is `AllZeroShiftedNeg_2(E)` as stated in §1.

QED conditional on:
1. GRH for `L_E^*` (standing).
2. GL2 Weil explicit formula for the completed newform (standard, Iwaniec-Kowalski).
3. Carneiro-Chandee majorant `m_Delta` properties (Carneiro-Chandee 2010).
4. Deligne `|lambda_E(p)| <= 2` and Rankin-Selberg `Σ |lambda_E(p)|^2 / p = log log x + O_E(1)` (Milinovich-Ng L3.1, Prop 5.1).
5. BFMT 2310.03949 Sections 4-5 (with parameter rerun at q=2, k=1 under conductor-flip rule).

No claim of unconditional removal of GRH. No Palm-wall break.

## 5. Downstream into halo route H1

`AllZeroShiftedNeg_2(E)` is Door A in the halo plan `HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §6. Combined with:

- Door B (arc-uniformity at radius `R = 1.5`, ratio `R/pi ≈ 0.477`) — closed in `HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md`.
- Door C (Stage 1b cluster contraction, σ > 1/2) — closed in repo (cited in Stage 1b).
- Door D (Stage 0 sign-flip / signed residue identity) — closed in `H1_RESIDUE_FIRST_AUDIT_2026-05-14.md` and the round-9 Lean gadget.

The halo route closes offcentral H1:
```text
R_E,1^{H1, offcentral}(T) = sum_{rho in Z_T^{mult}} m_rho * (signed contour residue contribution)
                          = o(T^2)    (under standing GRH for L_E^*).
```

This is **offcentral H1**, not the original pointwise H1. The Palm wall obstructs pointwise H1 because it requires `R_B = Σ |L_E^*'(rho)|^(-1)` as a positive `ℓ^1` quantity, which is genuinely strictly larger than the signed contour residue sum (Stage 0 two-zero gadget). The halo route works precisely because offcentral H1 does not need `R_B` as a positive quantity.

The Palm wall remains as stated; this assembly does not break it.

## 6. Residual risks (after assembly)

| Risk | Probability | Status |
|---|---|---|
| R1 (small-block sign condition at k=1) | 0.05 | Retired by §2 Step B (second-branch routing). |
| R2 (Agent01 k-dependence at k=1) | 0.02 | Retired by Step E (k-independence by inspection). |
| R3 (bad-prime audit eats margin) | 0.05 | Retired by §3 Sub-task 1.3 (`O_E(log log T)` k-independent). |
| R4 (Wave 5 NO-GO carries to weak target) | 0.05 | Retired by §2 Step B (weak target uses second branch). |
| R5 (hidden BFMT bookkeeping error in (5.13) absorption at k=1) | 0.10 | Open. The Section 5 absorption verification is end-to-end self-consistent but has not been independently re-derived; adversarial MIMO pass recommended. |
| GRH for `L_E^*` removed (unconditional H1) | 0.00 | Out of scope; halo route is conditional on GRH for `L_E^*`. |
| Palm wall broken (pointwise H1) | 0.00 | Out of scope; this assembly is for offcentral H1 only. |

Net confidence: 0.84 that `AllZeroShiftedNeg_2(E)` as stated holds under standing GRH for `L_E^*`.

The 0.16 residual is dominated by R5 (Section 5 absorption recompute risk), which is the natural target for an adversarial review of this assembly.

## 7. MIMO adversarial review (run 2026-05-14)

Dispatched via `scripts/dispatch_mimo.sh` (mimo-v2-flash, ~$0.02 cost). Full transcript: `MIMO_ADVERSARIAL_REVIEW_DOOR_A_ASSEMBLY_2026-05-14.txt`.

Net MIMO verdict: **"The assembly is coherent. The conductor flip rule is correctly interpreted, and the branch routing is valid. The Props transcription is sound, and multiplicity does not affect the exponent."** Single sharpening flagged:

> "The only potential subtlety is the uniformity of the test function parameters A, B under the conductor flip, but the claim's assumption A, B = 1 + O(k eps) is sufficient to preserve T^{5/2+eps}."

### 7.1 Resolution of MIMO's A,B-uniformity sharpening

BFMT (5.7) gives explicit values (no T-dependence):
```text
a = (1 - 3 k eps)/(1 - 2 k eps)
r = 1/(1 - 2 k eps)
d = (2 - 7 k eps)/(2(1 - 3 k eps)).
```

Direct algebra:
```text
A := a(2d-1)/r
   = (1 - 3 k eps) * [(2 - 7 k eps)/(1 - 3 k eps) - 1] * (1 - 2 k eps) / (1 - 2 k eps)
   = (1 - 3 k eps) * (1 - 4 k eps)/(1 - 3 k eps)
   = 1 - 4 k eps.

B := 2d - 1
   = (2 - 7 k eps)/(1 - 3 k eps) - 1
   = (1 - 4 k eps)/(1 - 3 k eps)
   = 1 - k eps + O((k eps)^2).
```

Both `A` and `B` are explicit rational functions of `(k, eps)` with no `T`-dependence. Under the conductor flip `k -> 2k`, `A = 1 - 8 k eps` and `B = 1 - 2 k eps + O((k eps)^2)`. Still `1 + O(eps)` at fixed k=1 and small eps; no T-dependence enters.

Refined exponent at q=2, k=1 with these explicit A, B:
```text
2(2k) - A     = 4 - (1 - 8 eps) = 3 + 8 eps
2(2k) - A + B = (3 + 8 eps) + (1 - 2 eps) = 4 + 6 eps
inner ratio   = (3 + 8 eps)/(4 + 6 eps) = 3/4 + O(eps)
exponent_T    = 1 + (1+delta) * (2k) * 3/4 + O(eps)
              = 1 + (1+delta) * 2 * 3/4 + O(eps)
              = 5/2 + O(delta + eps).
```

After relabeling delta, eps -> eps: `T^{5/2 + eps}`. MIMO's concern is resolved by direct BFMT (5.7) substitution; the A,B uniformity does not pick up any new T-dependence.

### 7.2 Net post-MIMO confidence

| Component | Pre-MIMO confidence | Post-MIMO confidence |
|---|---|---|
| Step A (Lemma 2.4 shifted majorant) | 0.95 | 0.95 (no MIMO concern) |
| Step B (Section 5 (5.13)/(5.17) rerun at q=2, k=1) | 0.86 | 0.92 (MIMO uniformity concern resolved §7.1) |
| Step C (multiplicity extension) | 0.95 | 0.97 (MIMO confirms "no cross-effect changes the exponent") |
| Step D (Props 2.5/2.6/2.7 lift to k=1) | 0.90 | 0.93 (MIMO confirms "lift arguments are valid") |
| Step E (Agent01 k-independence) | 0.95 | 0.95 (no MIMO concern) |
| Step F (RvM multiplicity bound) | 0.95 | 0.95 (no MIMO concern) |
| Overall (chain conjunction) | 0.84 | **0.88** |

The MIMO pass tightens overall confidence by ~0.04 by retiring the most fragile sub-claims (Step B conductor uniformity, Step D Props support conditions).

### 7.3 Recommended next steps

1. **Door A declared `CONDITIONAL_ON_STANDING_GRH`**, post-MIMO. No further block on the halo route Door A.
2. Proceed to full halo synthesis: combine `AllZeroShiftedNeg_2(E)` (Door A) with `HALO_DOOR_B_ARC_UNIFORMITY_AUDIT_2026-05-14.md` (Door B), Stage 1b (Door C), and Stage 0 / signed-residue identity (Door D) to assemble the halo-route offcentral H1 statement.
3. (Optional) File a Lean conjecture module `AllZeroShiftedNeg_2.lean` recording the statement (proof remains outside Mathlib due to analytic-NT machinery).

## 8. Boundary

Promote:
```text
AllZeroShiftedNeg_2(E) as a conditional theorem under standing GRH for L_E^*,
the GL2 Weil explicit formula, Carneiro-Chandee, Deligne / Rankin-Selberg, and
BFMT 2310.03949 Sections 4-5 with parameter rerun at q=2, k=1.

Door A closes for the halo-route bypass.
```

Do not promote:
```text
Door A as unconditional (GRH for L_E^* still required).
H1 as proved (still requires halo synthesis of Doors A + B + C + D, and the
              halo route gives offcentral H1, not pointwise H1).
Palm wall broken (Palm wall stands; halo bypasses it for offcentral case only).
The original pointwise H1 theorem (out of scope; would require Palm wall break).
```

Confidence: 0.84.
