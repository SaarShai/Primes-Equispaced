---
schema_version: 2
title: "Wave 4 Promotion Plan (Door A, Halo Unconditional)"
type: plan
domain: project
tier: working
status: PLAN
confidence: 0.80
created: 2026-05-14
updated: 2026-05-14
verified: 2026-05-14
sources:
  - primes-equispaced/handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md
  - primes-equispaced/handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md
  - primes-equispaced/handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md
supersedes: []
superseded-by:
tags: [halo-route, door-A, wave-4, promotion, stage-2-followon, plan]
---

# Wave 4 Promotion Plan — Door A (Halo Unconditional)

Planning document. Not a proof. Decomposes promotion of the two remaining Wave 4
conditional inputs to unconditional (under standing GRH for `L_E^*`). After
today's `HALO_DOOR_A_MULTIPLICITY_EXTENSION` (retires multiplicity gap) and
`HALO_RVM_MULTIPLICITY_LEMMA` (retires small RvM lemma), Door A stands
conditional only on these two Wave 4 inputs plus standing fixed-newform
RH/explicit-formula normalization.

---

## 1. Verdict and headline target

```text
Wave 4 promotion is 7-10 days of source-closing audit work.
Binding open input: ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k=1)
  with conductor-normalized small-block sign condition a(2d-1) > 4 at 4k=4.
Risk register: R1 (small-block sign fails at k=1 for loose target),
                R2 (BFMT prime polynomial requires new lemma),
                R3 (bad-prime audit eats Door A exponent margin),
                R4 (Wave 5 NO-GO carries to weak target).
```

Headline cross-check (§4): Wave 5's NO-GO targets the **strong** zeta-quality
`T^{1+δ}` derivative moment at `k=1/2`. The Door A target is the **weak**
shifted q=2 moment at `k=1`, exponent `T^{5/2+ε}`. The q=2 audit
(`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L107-148) explicitly does
the conductor-normalized rerun with `4k=4` and lands at `5/2+ε`. Wave 5 NO-GO
does **not** carry to the weak target. Genuine YES with quote (§4).

Genuine surprise (§4.3): Door A is **already conditionally proved at the same
exponent** by the q=2 audit. Wave 4 promotion is ledger source-closing, not
fresh analytic sprint. If `ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1)`
is the only true blocker (R2 retires by inspection of Agent01), Door A closes
in ~3-5 days, not ~10.

---

## 2. Input 1 — GL2-BFMT-PrimePolynomialLowerBound(E)

Current state (Agent01 Wave 4): `CONDITIONAL_THEOREM` at k=1/2 (lines 195-220
of `AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md`); prime squares, higher
prime powers, bad primes all `O_E(log log T)`; archimedean term replaced by
conductor-normalized `A_E(t;alpha,Delta)` with `C_E(t) asymp_E T^2`.

Goal: source-close at k=1 with the same `O_E(log log T)` overhead. Note that
Agent01's theorem statement is **k-independent in the prime polynomial form**;
the k-dependence enters only in BFMT Section 5 packaging. So "k=1/2 -> k=1"
here means "verify Agent01's lower bound is usable with `2k=2` (i.e. `4k=4`
post-conductor) in BFMT Lemma 2.4 / Section 5 (5.13)".

| Sub-task | Day | External source needed | Internal source needed | Output |
|---|---|---|---|---|
| 1.1 | 0.5 | BFMT arXiv:2310.03949 Lemma 2.3 (PDF p. 10) + Bui-Florea arXiv:2302.07226 Lemma 2.1 (proof of prime-square absorption) | AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md L29-89 | one-paragraph k-independence note: Agent01's display is independent of k; the k-dependence is downstream in BFMT Section 5. Pass criterion: cite line numbers, no further derivation needed. |
| 1.2 | 0.5 | Carneiro-Chandee arXiv:1008.4970 Lemma 8 + eqs (3.1)-(3.2) (PDF) | AGENT01 L83-87, BFMT_EC_TRANSCRIPTION_K_HALF L112-126 | source-quote of Carneiro-Chandee majorant `m_Delta`; verify the conductor-normalized archimedean term `A_E(t;alpha,Delta)` of AGENT01 L57-64 matches Carneiro-Chandee (3.1) after gamma-factor substitution. Pass: equation-level match. |
| 1.3 | 1.0 | Milinovich-Ng arXiv:1306.0854 eqs (18)-(23), Lemma 3.1 (PDF) | AGENT01 L86-87, BFMT_EC_TRANSCRIPTION_K_HALF L130-160 | k=1 bad-prime audit: verify the `O_E(log log T)` budget at `2k=2` (i.e. coefficient-square sum `sum_{p^m, m>=2 or p|N_E} |Lambda_E(p^m)|^2 a_alpha(p^m)^2 / p^{m(1+2alpha)} <<_E log log T`). Pass: explicit constant or `O_E(log log T)` bound; failure trigger -> R2. |
| 1.4 | 0.5 | BFMT Section 5 eq (5.13) (PDF p. 16) | DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md L117-148 | conductor-normalized Section 5 (5.13) rerun with `4k=4`. Pass: exponent computation `1 + 2k(4k-A)/(4k-A+B) = 1 + 2*(4-1)/(4-1+1) = 5/2` matches L138-142; failure trigger -> R1. |
| 1.5 | 0.5 | Iwaniec-Kowalski Ch. 5 (AFE for GL_n) | HALO_UNCONDITIONAL_PLAN_2026-05-12.md §5.2 L515-528 | AFE+conductor cross-check: `Y=T` balance at `C_E(t) asymp T^2`. Pass: `Y` choice and conductor balance agree. |

Total Input 1 cost: **3.0 days** (k-independence makes this cheaper than
anticipated; main labor is bad-prime audit 1.3 and conductor rerun 1.4).

---

## 3. Input 2 — ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E, k): k=1/2 → k=1

Current state (`ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md`):
`RIGOROUS_REDUCTION` at k=1/2; BFMT Propositions 2.5, 2.6, 2.7 each transcribe
with extra `(log T)^C` loss; Section 5 absorption works at `k=1/2`.

Goal: promote to k=1 (the version Door A's q=2 audit cites at L44).

### 3.1 The decisive Section 5 coefficient flip

At k=1/2, BFMT (5.13) coefficient `4k = 2`; small-block sign condition is
`a(2d-1) > 2`. Wave 5 NO-GO killed this for the **stronger** `T^{1+δ}` target
because the GL2 conductor doubles `2k -> 4k` (i.e., `2k=1 -> 4k=2`), pushing
the sign condition past the BFMT support regime
(`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L34-46).

At k=1, BFMT (5.13) coefficient `4k = 4`; conductor-normalized small-block
sign condition is `a(2d-1) > 4`. **The Door A target `T^{5/2+ε}` is the
weak q=2 shifted moment**, and the q=2 audit
(`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L117-148) has the second
BFMT branch *already* land at `5/2+ε`, computed with `4k=4`, `A=1+O(eps)`,
`B=1+O(eps)`. The weak target does **not** route through the small-block
sign condition — it uses the second branch directly.

| Sub-task | Day | External source | Internal source | Output |
|---|---|---|---|---|
| 2.1 | 0.5 | BFMT Prop 2.5 proof (PDF p. 11) | ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md L72-115 | k=1 Prop 2.5 transcription: zero-sampling estimate `ZS(A)` applied to `P_{0,v}^E(gamma)^{s_0}` at `2k=2`; verify support condition `beta_0 s_0 <= 1 - loglog T/log T` still applies. Pass: `(log T)^2` extra factor unchanged; `s_0 << log T / loglog T` parameter range survives. |
| 2.2 | 0.5 | BFMT Prop 2.6 proof (PDF p. 12) | ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md L117-145 | k=1 Prop 2.6 transcription: mixed family at `2k=2`. Pass: coefficient-square sum has Deligne `|lambda_E(n)| <= d(n)` Rankin-Selberg factor `<<_E log log T`; total loss `T^{o(1)}`. Failure trigger -> R3. |
| 2.3 | 0.5 | BFMT Prop 2.7 proof (PDF p. 12-13) | ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md L147-165 | k=1 Prop 2.7 transcription: terminal family at `2k=2`. Pass: `S_1 << N_E(T)(log T)^{O(1)}` form preserved; only exponent in `O(1)` changes. |
| 2.4 | 1.0 | BFMT Section 5 eqs (5.10)-(5.17) (PDF p. 16-18) | ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md L166-218, DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT L117-148 | k=1 Section 5 absorption audit: each insertion of Props 2.5/2.6/2.7 at `2k=2`. Verify the `exp(O(log T / loglog T))` and `(log T)^C` factors absorb into final `T^{5/2+eps}` exponent margin. Pass: explicit margin `T^{eps}` survives all four insertions. Failure trigger -> R1 + R3. |
| 2.5 | 0.5 | Milinovich-Ng arXiv:1306.0854 Prop 5.1 + Deligne | BFMT_EC_TRANSCRIPTION_K_HALF L150-162 | k=1 coefficient family Rankin-Selberg audit: `sum_{p<=x} |lambda_E(p)|^2 / p = loglog x + O_E(1)`. Pass: standard, source-quote only. |
| 2.6 | 0.5 | -- | ZERO_SAMPLING_HOMOGENEOUS_BFMT_DPMV_2026-05-11.md | k=1 zero-sampling lemma instance: `sum_{T<gamma<=2T} |A(1/2 + i gamma)|^2 <<_E T (log T)^3 sum |a_n|^2 / n` applied at `2k=2` parameter range. Pass: identical form to k=1/2; the lemma is k-independent. |

Total Input 2 cost: **3.5 days**. Sub-task 2.4 is the **binding open
sub-task** (the audit of Section 5 absorption with all four propositions
inserted at `2k=2` simultaneously, against the conductor-normalized Agent01
archimedean term).

---

## 4. Cross-check: how does this interact with Wave 5's NO-GO?

Wave 5's NO-GO statement (`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md`
L75-117):

```text
GL2-ShiftDerivativeComparison(E,c)
+ GL2-BFMT-PrimePolynomialLowerBound(E), conductor-normalized
+ ZeroSample-Homogeneous-BFMT-CoefficientDPMV(E,k=1/2)
does not imply
SeparatedEC-BFMT(E,c,k=1/2)
...
T^(beta_j) = exp(2 pi Delta_j),    alpha = 1/log T,    2 pi alpha Delta_j = beta_j
...
After inversion and BFMT power 2k, the small-block penalty doubles. At
k=1/2, this creates a fixed-power gap, not a polylogarithmic or T^o(1) loss.
```

The NO-GO target is `SeparatedEC-BFMT(E,c,k=1/2)`, i.e. the **derivative**
moment giving `T^{1+δ}` — the zeta-quality strong target (one full power of T
below Door A's `T^{5/2+ε}`). The failed implication chain ends in the small-
block sign condition `a(2d-1) > 2` (Wave 5 L38-46), which kills the strong
target.

The weak Door A target `T^{5/2+ε}` is a different target:

1. **Different moment**: q=2 *shifted* moment `sum |L(rho+alpha)|^{-2}` over
   `S_E(T)`, not the derivative moment.
2. **Different k**: k=1 (so `2k=2`, `4k=4`).
3. **Different BFMT branch**: the audit
   (`DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` L117-148) uses the
   second BFMT branch with exponent

   ```text
   1 + 2k(4k - A)/(4k - A + B)
     = 1 + 2*(4-1)/(4-1+1)
     = 5/2     (with A = 1 + O(eps), B = 1 + O(eps)).
   ```

   This branch does **not** route through the small-block sign condition that
   Wave 5 killed; it absorbs the conductor flip `2k -> 4k` directly into the
   exponent at `5/2`.
4. **Wave 5's R2 mitigation in Stage 2 plan** (CONT_SHIFTED_NEG_Q2_GL2_PLAN
   §6 risk register L550) prices Wave 5 at probability 0.10 of carrying to
   the weak target via R5 (Wave 4 conditionals not promotable).

**Verdict: Wave 5's NO-GO does NOT carry to the weak `T^{5/2+ε}` target.**
Quote (`BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` L38-46):

```text
At k=1/2, the small-block sign condition becomes:
  a(2d-1) > 2,
which is unavailable in the BFMT support regime.
```

The condition that fails is specific to `k=1/2` *and* to the derivative-moment
small-block branch. The weak q=2 target at `k=1` lands in the second branch
which prices `4k=4` into the exponent itself.

Confidence on this verdict: 0.85. The 0.15 residual is sub-task 2.4 — explicit
verification that Section 5 second-branch absorption is unobstructed at
`4k=4` with all four BFMT propositions inserted simultaneously.

---

## 5. Dependency graph

| Sub-task | Depends on | Blocks |
|---|---|---|
| 1.1 | (start) | 1.2, 1.4, 2.1 |
| 1.2 | 1.1 | 1.3, 1.4 |
| 1.3 | 1.2 | 1.4 |
| 1.4 | 1.1, 1.2, 1.3 | 2.4, synthesis |
| 1.5 | 1.1 | synthesis |
| 2.1 | 1.1 | 2.4 |
| 2.2 | 2.1 | 2.4 |
| 2.3 | 2.2 | 2.4 |
| 2.4 | 1.4, 2.1, 2.2, 2.3, 2.5, 2.6 | synthesis |
| 2.5 | (start) | 2.2, 2.4 |
| 2.6 | (start) | 2.1, 2.2, 2.3 |
| synthesis | 1.4, 1.5, 2.4 | Door A theorem statement |

Critical path: 1.1 -> 1.2 -> 1.3 -> 1.4 -> 2.4 -> synthesis (~5 days serial).
Parallelizable: 2.5, 2.6 run alongside 1.x; 2.1/2.2/2.3 run alongside 1.3/1.4.

---

## 6. External-source acquisition list

Sources to retrieve/quote via repo source protocol (curl + pdftotext + short
quote + page/equation reference).

| Source | Use | Status |
|---|---|---|
| Iwaniec-Kowalski Ch. 5 Thm 5.8 | RvM for GL2 newform; t-aspect zero count | already cited in HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md |
| Iwaniec-Kowalski Ch. 5 (AFE for GL_n) | Sub-task 1.5; `Y=T` AFE balance | needed (not yet quoted in repo with page/eq) |
| BFMT arXiv:2310.03949 Section 5, eqs (5.10)-(5.17) | Sub-tasks 1.4, 2.4; second-branch exponent | extracted at /tmp/farey-homogeneous-bfmt-20260511/bfmt_2310_03949.txt; needs page/eq quote at k=1 |
| BFMT Lemma 2.3 (PDF p. 10) | Sub-task 1.1; zeta prime-polynomial lower bound template | extracted; needs k-independence note |
| BFMT Propositions 2.5, 2.6, 2.7 (PDF p. 11-13) | Sub-tasks 2.1-2.3 | extracted; partial transcription at k=1/2 already done in ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT |
| Bui-Florea arXiv:2302.07226 Lemma 2.1 (PDF) | Sub-task 1.1; prime-square absorption proof | extracted at /tmp/farey-homogeneous-bfmt-20260511/bui_florea_2302_07226.txt |
| Carneiro-Chandee arXiv:1008.4970 Lemma 8, eqs (3.1)-(3.2) | Sub-task 1.2; majorant template | extracted at /tmp/farey-homogeneous-bfmt-20260511/carneiro_chandee_1008_4970.txt |
| Milinovich-Ng arXiv:1306.0854 eqs (18)-(23), Lemma 3.1, Prop 5.1 | Sub-tasks 1.3, 2.5; Deligne, S_f(t) bound, Rankin-Selberg | extracted at /tmp/farey-homogeneous-bfmt-20260511/milinovich_ng_1306_0854.txt |
| Heath-Brown J. LMS 1981 (fourth moment / fractional moments) | NOT needed for Wave 4 promotion; required only by ContShiftNeg_2 fallback (Stage 2 plan §2.5) | optional |
| Bui-Florea arXiv:2302.07226 (negative moments of zeta on shifted line, unconditional) | NOT needed for Wave 4 promotion; recommended for the ContShiftNeg_2 fallback insurance track | optional |
| Soundararajan Annals 2009 (upper-bound mollifier technique) | NOT needed; optional ContShiftNeg_2 fallback | optional |

---

## 7. Risk register

| Risk | Probability | Trigger | Action |
|---|---|---|---|
| R1: k=1/2 → k=1 small-block sign condition `a(2d-1) > 4` genuinely fails at k=1 for the loose target (Wave 5 carries over to the q=2 second branch) | 0.10 | Sub-task 1.4 or 2.4: the second-branch exponent computation produces a power `> 5/2`, OR the small-block branch is reached instead of the second branch | Fall back to direct zero-sample BFMT route (Stage 2 plan §3, fallback) or pivot to ContShiftNeg_2 GL2 adaptation (Stage 2 plan §2.1 with Bui-Florea / Soundararajan adaptation, ~2 extra weeks) |
| R2: BFMT prime polynomial lower bound requires a new lemma at k=1 (Agent01's k-independence claim fails) | 0.05 | Sub-task 1.1 or 1.3: the prime-polynomial display in AGENT01 L29-89 develops k-dependence in the `b(p;Delta)` or `A_E` term not anticipated; or bad-prime audit at `2k=2` exceeds `O_E(log log T)` | Pivot to fresh ConductorNormalized-BFMT-Section5-SignLemma(E, k=1) sub-audit, ~3-5 extra days |
| R3: bad-prime audit reveals an additional `(log T)^C` factor that breaks Door A's exponent margin | 0.05 | Sub-task 1.3 or 2.2: coefficient-square sums exceed `(log T)^{O(1)}` | Inspect whether `C` is fixed (absorbable into `T^{eps}`); if yes, proceed; if no, halt and recompute Door A exponent — likely fall back to ContShiftNeg_2 |
| R4: Wave 5 NO-GO does carry to the weak target despite §4 analysis (hidden small-block dependence in the second branch) | 0.05 | Sub-task 2.4: Section 5 second-branch absorption requires the small-block sign condition implicitly | Pivot to ContShiftNeg_2 + Gallagher-Heath-Brown transfer (Stage 2 plan §2) |
| R5: Door A turns out to be already proved modulo a single external citation (genuine surprise UP-side) | 0.15 | Sub-task 1.1 + 2.1: the k-independence of Agent01 + the homogeneous-DPMV k-independence of Prop 2.5 hold cleanly; Section 5 second-branch exponent locks at 5/2 in one pass | Compress Weeks 2-3 to one synthesis day; Door A closes in ~3-5 days total |

Hard abort (probability 0.02): if sub-task 1.4 conductor-normalized Section 5
audit yields a bound `> T^{5/2}` for the q=2 shifted moment, the Door A target
is genuinely out of reach via the BFMT route; halo route falls back to density-
method side-quest (Stage 2 plan §5.3 / halo plan §8.3).

---

## 8. Cost estimate

| Week | Days | Sub-tasks completed |
|---|---|---|
| Week 1 | 1.0-1.5d | 1.1 (k-independence note), 1.2 (Carneiro-Chandee source-close), 2.5 (Milinovich-Ng / Rankin-Selberg source-close), 2.6 (zero-sampling lemma k-independence). |
| Week 1 (continued) | 1.0-1.5d | 1.3 (bad-prime audit at 2k=2), 2.1 (Prop 2.5 transcription at 2k=2), 2.2 (Prop 2.6 transcription at 2k=2). |
| Week 2 | 2.0-3.0d | 1.4 (conductor-normalized Section 5 (5.13) rerun), 2.3 (Prop 2.7 transcription at 2k=2), 2.4 (Section 5 absorption audit — binding open sub-task). |
| Week 2 (continued) | 0.5-1.0d | 1.5 (AFE+conductor cross-check). |
| Week 3 | 1.0d | Synthesis: assemble Door A unconditional-under-GRH statement (file `ALL_ZERO_SHIFTED_NEG_2_E_2026-MM-DD.md`). |
| Total | 7-10d | All Wave 4 promotion sub-tasks closed, modulo standing GRH. |

Buffer (Week 3, +1-2d): if R1, R3, or R4 triggers, pivot to ContShiftNeg_2
fallback adds 1-2 weeks (Stage 2 plan §2 Bui-Florea / Soundararajan
adaptation). If R5 triggers, compress total to ~3-5 days.

---

## 9. Decision gates

```text
Gate 1 (end of Week 1, after sub-tasks 1.1+1.2+1.3+2.1+2.5+2.6):
  Pass: Agent01 k-independence verified at the prime-polynomial display
        level; Props 2.5 zero-sampling transcribes at 2k=2 with same
        (log T)^C overhead; bad-prime audit stays at O_E(log log T).
        Proceed to Week 2 Section 5 audit.
  Fail (R2): pivot to fresh ConductorNormalized-BFMT-Section5-SignLemma(E,k=1)
             sub-audit; extends Wave 4 promotion by 3-5 days.
  Fail (R3): inspect (log T)^C exponent; absorb into T^{eps} if fixed; halt
             and escalate if growing.

Gate 2 (end of Week 2, after sub-tasks 1.4+1.5+2.2+2.3+2.4):
  Pass: k=1 small-block sign condition either bypassed (second-branch
        absorption) OR satisfied at a(2d-1) > 4. Section 5 second-branch
        exponent locks at 5/2 + eps with eps margin to spare.
        Proceed to Week 3 synthesis.
  Fail (R1, R4): pivot to direct zero-sample BFMT route (Stage 2 plan §3)
                 or ContShiftNeg_2 + Gallagher-HB transfer (Stage 2 plan §2).

Gate 3 (end of Week 3):
  Pass: AllZeroShiftedNeg_2(E) unconditional-under-GRH theorem assembled.
        Combine with Stages 0/1a/1b/Door B for full halo synthesis.
  Fail: drop to density-method side-quest (Stage 2 plan §5.3); revisit
        Door A in subsequent sprint.

Hard abort (any week):
  BFMT (5.13) coefficient at k=1 with bad-prime audit yields a bound
  > T^{5/2}. Probability ~0.02. Door A target genuinely out of reach via
  BFMT; halo route falls back to density-method side-quest.
```

---

## 10. Boundary

### Allowed to claim now

```text
Wave 4 promotion is N days (7-10) of source-closing audit; Door A closes
under standing GRH for L_E^* if all sub-tasks 1.1-1.5, 2.1-2.6, and synthesis
pass.

The Wave 5 NO-GO does not carry to the weak T^{5/2+eps} Door A target; the
weak target uses the second BFMT branch with 4k=4 priced directly into the
exponent (DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT L117-148), bypassing the small-
block sign condition that killed the strong T^{1+delta} target at k=1/2.

The binding open sub-task is 2.4: explicit verification of Section 5 second-
branch absorption at 2k=2 with all four BFMT propositions inserted
simultaneously against the conductor-normalized Agent01 archimedean term.
```

### Not allowed to claim

```text
Wave 4 is closed.
Door A is closed.
The halo route is fully unconditional. (It requires GRH for L_E^*.)
AllZeroShiftedNeg_2(E) is unconditionally proved.
The k=1 BFMT EC transcription is written.
The conductor-normalized Section 5 sign condition is verified at k=1.
```

### Confidence breakdown

```text
0.80  Wave 4 promotion succeeds in 7-10 days, Door A closes under GRH.
0.15  Wave 4 promotion compresses to 3-5 days (R5 up-side surprise).
0.10  Wave 4 promotion stalls on sub-task 2.4 or R1/R4 trigger; fall back
      to ContShiftNeg_2 route adds 1-2 weeks (Stage 2 plan §2).
0.05  R3 triggers; recompute Door A exponent; likely still feasible.
0.02  hard abort (BFMT route fails; density-method side-quest).
```

(Probabilities overlap; R5 up-side and R1/R4 down-side are not mutually
exclusive with the 0.80 baseline.)

---

## 11. Cross-references

| File | Role |
|---|---|
| `handoff-2026-05-14-research-track-split/CONT_SHIFTED_NEG_Q2_GL2_PLAN_2026-05-14.md` §4 | Stage 2 cross-check identifying the two Wave 4 conditionals as the only remaining Door A obstruction |
| `handoff-2026-05-14-research-track-split/HALO_DOOR_A_MULTIPLICITY_EXTENSION_2026-05-14.md` | Retires multiplicity gap (S_E(T) -> Z_T^{mult}) at same exponent |
| `handoff-2026-05-14-research-track-split/HALO_RVM_MULTIPLICITY_LEMMA_2026-05-14.md` | Retires small RvM lemma for offcentral multiplicity bound O(log T) |
| `handoff-2026-05-11-breakthrough-wave-4/BREAKTHROUGH_WAVE_4_SYNTHESIS_2026-05-11.md` | Identifies Wave 4 conditional inputs; current CONDITIONAL_PASS at k=1/2 |
| `handoff-2026-05-11-breakthrough-wave-4/AGENT01_GL2_BFMT_LOG_LOWER_BOUND_2026-05-11.md` | Input 1 conditional theorem packet |
| `handoff-2026-05-11-breakthrough-wave-4/AGENT02_GL2_SHIFT_DERIVATIVE_COMPARISON_2026-05-11.md` | Companion shift-derivative comparison (CONDITIONAL_PASS under fixed-newform RH); not Wave 4 promotion target — only needed by derivative-moment route, not by Door A's shifted-q=2 route |
| `handoff-2026-05-11-homogeneous-bfmt-dpmv/BFMT_EC_TRANSCRIPTION_K_HALF_2026-05-11.md` | k=1/2 EC transcription; target of k=1 promotion |
| `handoff-2026-05-11-homogeneous-bfmt-dpmv/ZERO_SAMPLE_BFMT_SUBSTITUTION_AUDIT_2026-05-11.md` | Input 2 k=1/2 substitution audit (RIGOROUS_REDUCTION) |
| `handoff-2026-05-11-post-wave5-pivot/DEGREE2_WEAK_SHIFTED_NEG_Q2_AUDIT_2026-05-11.md` | q=2 audit giving Door A's `T^{5/2+eps}` over `S_E(T)` (CONDITIONAL_PASS_FOR_SHIFTED_Q2) |
| `handoff-2026-05-11-breakthrough-wave-5/BREAKTHROUGH_WAVE_5_SYNTHESIS_2026-05-11.md` | Wave 5 NO-GO for strong T^{1+delta} target at k=1/2; §4 verifies this does not carry to weak target |
| `handoff-2026-05-11-breakthrough-wave-5/AGENT01_SECTION5_GL2_CONDUCTOR_AUDIT_2026-05-11.md` | Wave 5 Agent01 detail: log C_E(t)=2 log T + O_E(1) drives the 2k -> 4k conductor flip |
| `handoff-2026-05-11-dpmv-continuation/GL2_LANDAU_GONEK_DPMV_SPLIT_2026-05-11.md` | LG-Explicit-GL2 source-closed via Milinovich-Ng L3.3; supports sub-task 1.3 and 2.5 |
| `handoff-2026-05-12-halo-unconditional-plan/HALO_UNCONDITIONAL_PLAN_2026-05-12.md` §6 | Original halo plan Door A target T^{5/2+eps} |
