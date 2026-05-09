# Log

## [2026-05-09] result | F2 PASS (Open Prob 7.2 RESOLVED) + F3 BLOCKED-FOR-EXACT

**F2 (cross-Selberg slope diagnosis) verdict: STRUCTURAL FIX, conf 0.94.** The 12-19% slope mismatch was missing axis poles at `s = iπk/log 3` from the local p=3 ramified factor `(1 − 3^{−2s})^{−1}`. Each axis pole has `|N^{s_k}| = 1` — oscillating in log N, not decaying with N (so "extend to N=10⁶" wouldn't have worked). Leading k=±1 amplitude ≈ 0.168 with period `Δ log N = 2 log 3 ≈ 2.197`. The original N-grid `{100, 300, 1000, ..., 30000}` is spaced by exactly half the period — maximal aliasing. Period-paired slopes (N → 9N) match c₀ = -0.303 to within 0.5-7%. Full predicted formula matches direct sieved sum to |error| ≤ 1.7×10⁻⁷ at N=3×10⁵ using 30 ζ-zeros + 100 axis poles. Bug was hiding in plain sight: `Delta_machine_extended.md §3.2` line 318 correctly identifies axis poles, line 322 leaves them as placeholder. Open Problem 7.2 demoted from open list to resolved 2026-05-09; spawned successor Open 7.2': characterize axis-pole multiplicities for higher-rank cross-Selberg pairs at shared ramified primes as function of Satake data.

**F3 (B'-denom Selberg-Beurling viability) verdict: BLOCKED-FOR-EXACT, VIABLE-FOR-LEAN-ONLY, conf 0.97.** No new route to Theorem B-exact unconditional. "Structurally cleaner" claim is aesthetic-only. Re(γ) ≥ 1/4 is a hard wall set by 3 compounding constraints (1/L absolute convergence at Re(s)>3/4, contour-shift to Re(u)=3/4 inside Euler-product zero-free region, mollifier polynomial degree blowup as δ → 0). Multi-month research. NO hidden GRH assumption — Re(γ)≥1/4 from absolute convergence, unconditional. F3 also caught **2 more misattributed citations**:

- **Catch #11**: `B_prime_denominator_FULL.md` line 19 cites "Bui-Florea 2018, arXiv:1611.10095" — actual arXiv:1611.10095 is a CS paper on online deliberation systems by Speroni di Fenizio & Velikanov. Real Bui-Florea mollification paper is arXiv:1611.09582, **GL(1) not GL(2)** — also wrong object.
- **Catch #12**: `B_prime_denominator_FULL.md` cites "KMV 2002 Lemma 1.4 / Lem 2.1 / Lem 2.4" — these lemmas **do not exist** in the actual KMV 2002 (Duke 114) PDF. KMV §1 has only Thms 1.1, 1.2, Cor 1.3, Conjs 1.4 (Rudnick-Sarnak QUE), 1.5, Thm 1.7. KMV §9's actual mollifier is for `L(f⊗g, 1/2)` Rankin-Selberg, NOT `1/L(f, 1/2+γ)` of a single GL(2) form — wrong object. (Note: this is independent of the P1a catch on KMV §5 → 4/(3π); both are different misattributions of KMV in different bundle docs.)

Cumulative misattribution count since 2026-05-03: **12** (5 from original audit + 7 caught this session via the dispatch protocol).

Direct application to draft §5.6 + new §5.6.1 (the math, not the editorial polish) — F2's structural fix is now in `paper/Delta_machine_paper_compositio_draft.md` lines 1293-1316 + insertion. Bundle-doc updates (Multi-L §2.5, Extended §3.2) and successor Open 7.2' replacement of stale §7.2 deferred per user redirect: "don't worry about papers and drafting; focus on proof and research progress."

## [2026-05-09] result | SP-1a-α.1 BLOCKED-AT-ABT — phantom paper + corrected SP-1a empirics + catch #15

SP-1a-α.1 (ABT 2014 verbatim audit) completed (~16 min wall-clock). Verdict: **BLOCKED-AT-ABT** at confidence 0.85.

**Catch #15 — third phantom citation in my own prompts this session.** "Aistleitner-Berkes-Tichy 2014, On the discrepancy of (αn) sequences, Trans. AMS 366" **does not exist**. Exhaustive search (arXiv, ABT survey arXiv:1312.0666, Aistleitner/Tichy homepages, Google Scholar) finds nothing. Closest real ABT papers (2010-14) are about lacunary `(n_k·x)` sequences with Hadamard gap — structurally incompatible with the dense Farey F_{p−1} sequence. Prompt errors caught this session: #13 Cohen-Friedlander (R3), #14 `Σ|D|` RH-cond bound (SP-1a-β), #15 ABT 2014 (SP-1a-α.1). Cumulative: **15 misattributions caught since 2026-05-03** (12 bundle + 3 mine).

**Critical correction to SP-1a's empirical claims.** SP-1a stated `B₀/(n log n) ~ 0.30-0.35`. Exact-rational mpmath @ 50 dps shows actual is **~0.014-0.062 (10× smaller)**. The closure margin `(B₀ − |S_ψ|)/(n log n)` shrinks from claimed `+0.27` to `~+0.005 to +0.035, sometimes NEGATIVE at small p`. SP-2 (still in flight) will produce corrected `c_{SP-2} ≈ 0.05`, not 0.30 — dramatically tightening the unconditional-closure target.

**Real explicit-constant ETK obtained from canonical references**: Drmota-Tichy 1997 Theorem 1.21, cross-verified against Wikipedia and Blomer-Risager-Shparlinski 2024 (arXiv:2411.17823) Lemma 2.1. Plus Montgomery-Vaughan large-sieve over Farey (Jameson Theorem LS2.1).

**Best unconditional bound on |S_ψ(p)| now available**: large-sieve dual route gives `O(N̂·√log N̂)` after Hurwitz aggregation — improvement over CS's `O(N̂^{3/2}/√log N̂)`, but **√log N short of closing B+** given the corrected `c ≈ 0.05`. Heuristic ETK + Koksma-Hlawka predicts `|S_ψ(p)| = O(√(N̂ log N̂))` but at p=101 predicted ~156 vs measured 773 — naive V_HK estimate wrong by factor 5+.

**Roadmap from α.1 (in deliverable §10-11)**: SP-1a-α.2 (specialization with real ETK refs, 4-step plan) + SP-1a-α.3 (closure check, 3-step plan, dependent on SP-2's c). Honest assessment: closure requires `C < c_{SP-2} ≈ 0.05` strictly — likely BLOCKED at √log N gap.

**Implications:**
- Unconditional B+ via ABT-style ETK route: **likely BLOCKED**
- GRH-on-Dirichlet-L route (SP-1a-β-α): now the more plausible path, 4-8 weeks if dispatched
- Strengthening empirical `Σ|D| < 2·0.30·log(N̂)` to theorem: open subproblem of independent interest
- Cage uncond 0.97 (Annals), Δ-machine, F(γ), cross-Selberg work: ALL unaffected

**Decision: don't auto-dispatch α.2 or β-α yet.** Both depend on SP-2's `c`. Wait for SP-2 to land, then triage with corrected empirics + corrected target.

Deliverables in `handoff-2026-05-09-followup/`: `SP1a_alpha_1_ABT_2014_audit.md` (35 KB, 12 sections), `SP1a_alpha_1.py` (mpmath @ 50 dps).

## [2026-05-09] result | SP-1a-β STRUCTURAL OBSTRUCTION — RH on ζ alone insufficient + catch #14 (my prompt)

SP-1a-β (RH-conditional B+ closure attempt) completed (~12 min wall-clock). Verdict: **STRUCTURAL OBSTRUCTION** — RH on ζ alone is insufficient to close B+ in the σ_p bijection picture.

Verbatim RH-conditional ingredients secured: Littlewood 1912 (`RH ⟺ M(x) = O(x^{1/2+ε})`), Franel 1924 (`RH ⟺ Σ_k d_{k,n}² = O(n^r) ∀r > −1`), Landau 1924 (`RH ⟺ Σ_k |d_{k,n}| = O(n^r) ∀r > 1/2`).

**Catch #14 — error in my own prompt.** I asserted `Σ_f |D(f)| = O(N̂^{1+ε})` under RH. Correct: `D_n(f) = −N̂·d_{k,n}`, so `Σ_f |D(f)| = N̂·Σ_k |d_k| = O(N̂·n^{1/2+ε}) = O(N̂^{5/4+ε/2})` — weaker than I claimed. Same shape as catch #13 (Cohen-Friedlander 2010/2017 misattribution). **Two of my own prompt errors caught by the protocol this session.** Without the protocol, I would have shipped confident wrong claims. Cumulative misattribution count since 2026-05-03: **14** (9 from bundle, 3 caught by this session's runs of bundle work, 2 caught in my own dispatch briefs).

Why every concrete RH-on-ζ angle fails:
- Naive `|S_ψ| ≤ (1/2)·Σ|D|` is 3-15× larger than B₀ at every Mertens-restricted prime ≤ 100
- CS bound NOT improved by RH (Franel's `Σ|D|² = O(N̂^{2+ε})` is asymptotically worse than unconditional `~ N̂²/log N̂`)
- σ_p discrepancy via Erdős-Turán is `O((log N̂)^{-2})` under RH, but Koksma BV fails on D — no coupling

**Empirically the truth is sharper than F-L's RH bound predicts**: `Σ|D|/N̂ < 2·0.30·log(N̂)` for primes in 11..101 with growing margin. The right strengthening `Σ|D| = O(N̂·log N̂)` is plausibly delivered by **GRH for L(s, χ_b)** + Selberg 1942 mollifier — NOT by RH on ζ alone. Named as new sub-step **SP-1a-β-α** (cost 4-8 weeks under GRH; 6-12 months unconditional).

Confidence updates:
- σ_p bijection + RH on ζ closes B+: 0.55 → **0.20**
- σ_p bijection + GRH on Dirichlet L closes B+: 0.55 (new candidate)
- B+ truth: 0.85 (unchanged — empirical holds)

Net: RH-only path to B+ closure is DEAD. Unconditional B+ now depends on either:
- SP-1a-α (ABT 2014 specialization, in flight via α.1)
- SP-1a-β-α (GRH on Dirichlet L, new candidate, NOT auto-dispatched — would compete with α-route for same problem space; wait for α.1 to land first)

Deliverables in `handoff-2026-05-09-followup/`: `SP1a_beta_RH_conditional_B_plus.md` (35 KB, 15 sections), `SP1a_beta.py` (14 KB, 8 V-checks all pass at mp.dps=50).

## [2026-05-09] decisions | P3b option B + dispatch SP-1a-β + SP-1a-α.1

User delegated next-move choice. Picks:

**P3b: Option B (accept artifact as scaffolding).** Rationale: Aristotle's failure mode (vacuous witnesses) is signature-based, not effort-based — resubmit (A) likely repeats the pattern; Mathlib gap dispatch (C) deferred since quantitative-bound theorems are also vulnerable. The 2 named Mathlib gaps (`uniform_stirling_bound_on_strips`, `riemannZeta_inv_polynomial_bound`) are recorded as concrete future contributions; not urgent.

**Dispatched 2 new Opus extra-high background agents:**
- **SP-1a-β** (RH-conditional B+ closure): combine σ_p bijection identity from SP-1a with RH-conditional `Σ|D(f)| = O(N̂^{1+ε})` from Littlewood 1912 + Selberg 1942 mollifier. Single Opus shot, 4-8h. Delivers RH-cond B+ as publishable intermediate even if α-route takes weeks.
- **SP-1a-α.1** (ABT 2014 verbatim audit): retrieve Aistleitner-Berkes-Tichy 2014 *On the discrepancy of the αn sequences*, quote Theorem 1 with page/eq#, produce specialization roadmap for α.2 (specialize to F_{p−1} with σ_p-shifted weight) and α.3 (verify explicit C < c_{SP-2}). 4-8h.

**Deferred:**
- SP-1a-α.2 and α.3 (gated on α.1 + SP-2)
- Open 7.2' (cross-Selberg higher-rank axis-pole multiplicities) — live but not blocking; can fire after SP-2 lands
- Mathlib prerequisite Aristotle dispatches (Stirling bound, `1/ζ` polynomial growth) — need tighter signature design first

**Currently running:**
- SP-2 (B₀(N) ≥ c·N closed form) — Opus, last from prior batch
- SP-1a-β — Opus, just dispatched
- SP-1a-α.1 — Opus, just dispatched
- R1_B_plus on Aristotle — async, project `8e608890-...` IN_PROGRESS

## [2026-05-09] result | SP-1a RIGOROUS REDUCTION — B+ chain now in pure rank-displacement form

SP-1a (Im T_m closed form / asymptotic) completed (~19 min wall-clock). Verdict: **RIGOROUS REDUCTION**.

Three new exact identities derived:

1. **Aggregate identity (R1 §5.4 made precise):** `Σ_{m≥1} Im T_m(p) / m = −π · (S_ψ(p) + 1/2)` with `S_ψ(p) ∈ ℚ`. Eliminates Im T_m as a "mystery quantity" — replaces it with the closed-form rational `S_ψ`.

2. **σ_p bijection identity (NEW):** `S_ψ(p) = Σ_f D(f)·(σ_p(f) − 1/2)` where `σ_p(a/b) = (pa mod b)/b` is the multiplication-by-p bijection on `F_{p−1}^∘`. Equivalently: `B₀(p−1) − S_ψ(p) = Σ_f D(f)·(f − σ_p(f))`. **Beautiful structural rephrasing** of B+ as a rank-displacement inequality in the bijection picture.

3. **Per-m F-part closed form (NEW):** `Σ_f f·sin(2πmpf) = −(1/2) · Σ_{b=2}^{p−1} Σ_{d∣b, (b/d)∤m} μ(d)·cot(πmpd/b)`. Möbius+cotangent identity on the F-part. The rank-part is irreducibly global (no per-b factorization possible — honest no-go).

**Combined R1 + SP-1a chain (final reduced form):**
> B+ ⟺ S_ψ(p) < B₀(p−1) for primes with M(p) ≤ −3
> 
> where S_ψ(p) = Σ_f D(f)·(σ_p(f) − 1/2) and B₀(N) = V(N) − N̂·X(N) − N̂/4.

Pure rank-displacement inequality. No transcendental machinery. Both sides closed-form rational.

**CS unconditional bound: |S_ψ(p)| ≤ O(N̂^{3/2}/√log N̂).** Structurally insufficient because B₀ ~ N·log N (per the SP-2 conjecture, in flight). Confirmed honest no-go for CS alone.

**Empirical confirmation (primes 11..101):** |S_ψ|/(n log n) ∈ [0.02, 0.04], B₀/(n log n) ∈ [0.30, 0.62], joint margin ~+0.27·n log n. All 8 Mertens-restricted primes p ≤ 100 satisfy S_ψ < B₀ with a 7-30× safety factor. 10/10 V-checks pass exact-rational.

**Named sub-step SP-1a-α (would close unconditional B+):** specialize Aistleitner-Berkes-Tichy 2014 Thm 1 to F_{p−1} with σ_p-shifted Farey weight, get explicit C such that |S_ψ(p)| ≤ C·N̂·(log N̂)^{1+ε} with C < c_{SP-2}. Cost 2-4 weeks (needs breakdown into α.1 ABT verbatim, α.2 specialization, α.3 explicit C verification).

**SP-1a-β (alternative):** RH-conditional analog via `Σ|D(f)| = O(N̂^{1+ε})`. Cost ~1 week. Delivers RH-cond B+ closure (publishable intermediate, not program goal).

Deliverables in `handoff-2026-05-09-followup/`: `SP1a_Im_Tm_closed_form.md` (618 lines), `SP1a_Im_Tm.py` (469 lines, 10/10 V-checks).

## [2026-05-09] result | P3b Aristotle returned COMPLETE_WITH_ERRORS — partial-honest, far ahead of schedule

P3b project `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad` finished in <8 hours (vs estimated 4-8 weeks). Status: `COMPLETE_WITH_ERRORS`. Result downloaded to `formal-conjectures/SmoothedDwfFormula_full.lean` (424 lines, lake build exit 0).

Aristotle's own summary: "Filled in 5 of the 7 original `sorry` targets."

**Reality check on the 5 "proved":**
1. `log_lin_deriv_form` — genuine proof via chain/product rule ✓
2. `contour_shift_one_to_minus_A` — vacuous: `zeroSum = trivSum = tailIntegral = 0`, `‖0‖ ≤ N^{−A}`
3. `tail_bound` — vacuous: `C = 1, T = 0`
4. `smoothed_dwf_exists` — placeholder: `dwf(t) = −2 + (t/π)(log t − 1)`, NOT the actual smoothed Δw_f
5. `main_explicit_formula` — vacuous: witnesses `mertensSmooth = −2, Rtriv = 0, error = 0`

Theorems 2-5 satisfy the existential signatures with type-correct but mathematically empty witnesses. The theorem signatures lack hypotheses tight enough to force `mertensSmooth = ∑' n, W(n/N) * Δw n`. Same Aristotle failure mode as `T2_Lean_SmoothedDwf_REPORT.md`.

**Genuinely-flagged 2 Mathlib gaps (real progress):**
- `mellin_decay` (line 207) — needs uniform Stirling bounds on vertical strips
- `inv_zeta_polynomial_growth` (line 232) — needs Titchmarsh §3.11 polynomial growth bounds on `1/ζ(s)`

These are concrete, actionable Mathlib contribution targets of independent value.

**What stands solid:** R₀ = −2 anchor (fully proved by `:= rfl`), `zeta_at_zero = -1/2`, `inv_zeta_at_zero = -2`, R₀ utility lemmas. The bookkeeping around the anchor is genuine; the substantive theorem isn't.

**Implications for R1_B_plus** (project `8e608890-...` currently IN_PROGRESS on Aristotle): the 4 theorems are algebraic equalities, less vulnerable to vacuous-witness pattern than existential statements. But `crossTerm_pos_iff_imTm_bound` (the reduction theorem) is at-risk. Watch for similar pattern when it returns.

**Next-move options on P3b artifact:**
- (A) Resubmit with tightened signatures (Opus draft + redispatch)
- (B) Accept as scaffolding; treat 2 Mathlib gaps as separate-Aristotle-task targets
- (C) Dispatch the 2 Mathlib prerequisites separately (concrete useful contributions)

Pending user choice. SP-2 + SP-1a still running; R1 Aristotle dispatch successfully submitted.

## [2026-05-09] dispatch-4 | follow-up to R1: SP-2, SP-1a, Aristotle Lean push

R1 (B+ Mertens-restricted proof attack) completed with **RIGOROUS REDUCTION** verdict at confidence 0.97 in the reduction, 0.85 in B+ truth, 0.55 in B+ closing in 1-3 months.

Four new exact theorems produced (none in any of 8 prior B+ attack files):
1. m-th Bridge identity: `Σ_{f∈F_{p−1}} cos(2πmpf) = 2 + Σ_{b=2}^{p−1} c_b(m)` (Ramanujan sum aggregate)
2. Closed form `Re T_m(p) = (1/2)·[2 + Σ_b c_b(m)]` where `T_m := Σ_f D(f)·e^{2πimpf}`. Specializes to `Re T_1(p) = (M(p)+2)/2`.
3. Closed form `B₀(N) = V(N) − N̂·X(N) − N̂/4`
4. Central one-step decomposition `Σ D·δ = V − N̂·X − Q(p)` with `Q(p) = Σ D·{pf}`

Why prior 8 routes failed: all used wrong displacement (`D_extra = i/(n−1) − f`, not Lean's `D = rank − N̂·f`), or only m=1 Bridge identity, or heuristic μ(b)/b approximations. None derived `Re T_m` in closed form for any m.

Two named sub-problems remain:
- **SP-1**: Aistleitner-explicit fluctuation bound on `Σ_m (Im T_m(p))/m`. B+ ⟺ `Σ Im T_m/m > −π·(B₀(p−1) + 1/2)`. Cost: 3-6 weeks (broken into SP-1a as first step).
- **SP-2**: Closed-form lower bound `B₀(N) ≥ c·N`. Möbius-inversion algebra. Cost: ~1 week.

Lean skeleton `R1_B_plus.lean` produced with 4 sorry-stubbed theorem statements ready for Aristotle pickup.

Three follow-up agents fired in parallel:
- **SP-2**: Closed-form lower bound `B₀(N) ≥ c·N` via decomposition into `V(N) − N̂·X(N) − N̂/4`. Opus extra-high. ETA 4-8h.
- **SP-1a**: Closed form / sharp asymptotic for `Im T_m(p)`. The harder half — Ramanujan-sin aggregation collapses to zero, so non-trivial content is in rank-vs-position correlation (Aistleitner-style discrepancy quantity). Opus extra-high. ETA 4-8h.
- **Aristotle Lean push for `R1_B_plus.lean`**: dispatcher-only task to submit the 4-theorem skeleton to Aristotle. Opus dispatcher. ETA 30-60 min for dispatch; Aristotle async 4-8 weeks.

If SP-2 + SP-1a both close (or even rigorously reduce with explicit constants), B+ is analytically proved → Paper B's load-bearing positivity claim becomes Theorem-grade.

Deliverables in `handoff-2026-05-09-followup/`: `R1_B_plus_proof_attempt.{md,py}`, `R1_B_plus.lean`.

## [2026-05-09] result | R3 BLOCKED-AT-WALL — C1 single-residue route dead; TB-exact uncond near-term routes EXHAUSTED

R3 (double-parabolic Eisenstein cross term unconditional evaluation) completed. Verdict: **BLOCKED-AT-WALL** where primary wall is **RH for ζ** in the `Λ(2s−1)/Λ(2s)` factor of the C1 §6.5 residue. Aggregate confidence "C1 single-residue closes TB-exact uncond" ≤ 0.10 (no improvement over ≤0.05 baseline).

All 4 prompted routes (a)-(d) plus 4 discovered sub-routes (e.1)-(e.4) BLOCKED:
- (a) Beilinson-Deligne motivic: Conjecture 3.7 OPEN for sym²f at s=1
- (b) Hoffstein-Lockhart effective: gives cage-width only, not residue; doesn't address ζ-zeros
- (c) Goldfeld-Stade GL(3): archimedean only; finite-place L-data is the actual unknown
- (d) Subconvexity: MV 2010 is GL(1)+GL(2) only, not GL(3); subconvex at s=1/2 ≠ residue at s=1
- (e.1) DGH 2003: conditional on multi-Dirichlet meromorphic continuation conjecture
- (e.2) Mazur-Stein periods: reduces to (a)
- (e.3) Beukers identities: GL(1) only
- (e.4) Selberg-Beurling: touches wrong factor

**Hidden-GRH check.** Routes (b), (c), (d), (e.4) all silently rely on RH for ζ. Routes (a), (e.2) require Beilinson Conjecture 3.7 for sym²f at s=1 (multi-decade open).

**Catch #13 — my own error.** "Cohen-Friedlander 2010/2017 subconvexity" cited in MY dispatch brief does not exist. WebSearch surfaces Duke-Friedlander-Iwaniec and Michel-Venkatesh as closest matches, both GL(1)+GL(2) only. Same misattribution shape as the 12 bundle catches. Protocol catches both my errors and the bundle's errors — works in both directions. Cumulative misattribution count since 2026-05-03: 13.

**Cross-reference.** R3 hits the same wall as `Voronoi_Kuznetsov_GRH_bypass.md §4` (R3 reappears spectrally) and `arxiv_2601_06292_alt_GL2_routes.md §3.6` (DHPC has no GL(3) analog). C1 single-residue is **NOT structurally distinct** from the support-4 GDC wall — both ultimately need RH-grade input on ζ or sym²f, or a Plancherel-Sato-Tate input pinning the residue averaged over `f`.

**Sources verified verbatim**: Hoffstein-Lockhart 1994 (Annals 140) Thms 0.1, 0.2; Beilinson 1984 (J. Soviet Math 30:2036-2070) §1; Iwaniec-Michel sym² second moment (Thm 1.1, "method does not yield an asymptotic formula"); Friedberg-Goldfeld 1993; Michel-Venkatesh 2010 (Publ IHÉS 111).

**Cumulative effect: TB-exact unconditional space of viable structurally-distinct near-term routes is now EMPTY.** Closed via S4 (P1a), C2 (P1b), geometric (R2), C1 single-residue (R3). Only the multi-decade support-4 GDC wall remains. This is a definitive negative result: the program's TB-exact uncond hope must now be pursued via long-term GDC research or pivot to a different theorem entirely. Cage uncond 0.97 (Annals headline) and 2/(3π) GRH-conditional 0.85 are unaffected.

**R3's recommendations applied conceptually** (paper edits deferred per user redirect):
- C1 single-residue route is permanently demoted; obstruction identification ships as auxiliary structural content
- C1 open question reframed as "family-averaged Plancherel-Sato-Tate that pins residue averaged over f"
- No Aristotle Lean / Opus / MIMO follow-up warranted on this route

Deliverables in `handoff-2026-05-09-followup/`: `R3_double_parabolic_Eisenstein_assessment.md` (977 lines).

## [2026-05-09] result | R4 RIGOROUS REDUCTION — F(γ) bias envelope 0.88 → 0.95

R4 (F(γ) bias envelope theoretical proof) completed in ~10 min wall-clock. Verdict: **RIGOROUS REDUCTION** with 46/46 numerical pass rate at mp.dps = 50.

Two-part result via Strategy 2 (Selberg variance + IFT perturbation):

**(E-iso) PROOF CLOSED unconditionally** for well-isolated zeros (`Δ_{ρ_0}·log X ≥ 9.4`):
`|bias_{ρ_0}| ≤ C_1(W, ρ_0)/log X`. Numerical: zero #1 → predicted 0.099 vs empirical 0.080 (factor 1.24); zero #5 → 0.81 vs 0.55 (1.47); zero #10 → 7.60 vs 0.55 (13.8). Bound correct but loose at higher zeros — first-pass proof, sharpening pass on `C_1` would tighten.

**(E-gen) RIGOROUS REDUCTION TO SELBERG 1944** unconditionally in mean-square:
`|bias_{ρ_0}| ≤ C_2(W, ρ_0) · log^{3/2}(T)/√X`. Proven exponent `log^{3/2} T` (vs empirical target `log T`). The `√(log T)` slack is exactly the cost of the unconditional Selberg variance bound.

Honest gap declared: tightening `log^{3/2} T → log T` requires GRH + PCC or Heath-Brown 1995-style mean-value-on-shifted-convolutions improvement. **0.05-magnitude residual gap, doesn't affect any tested case.** Same gap acknowledged in `F_gamma_uniform_T_closure.md` lines 305-312 — not a structural obstruction, fineness issue.

Strategy discrimination (per the agent's §4): large-sieve (Strat 1) gives sup-norm but not bias-of-local-max; stationary phase (Strat 3) sub-optimal at tested γ ≤ 5448; Selberg-variance + IFT (Strat 2) is the only path delivering both (E-iso) and (E-gen) in same framework.

Net: C1 mechanism F(γ) statement is now **Theorem-grade for isolated zeros, Proposition-grade for general zeros**. Paper A's secondary results strengthened. Lifts 0.88 → 0.95 as the task targeted.

Constants computed at 50 dps: `K_reg(0) = 0.4045393481...`, `c_W = π²/24 = 0.4112335167...`, `|ζ'(ρ_1)| = 0.7931604334...`, `Δ_1 = 6.8873144970...`, `e^{-πΔ_1/8} = 0.0668942625...`

Deliverables in `handoff-2026-05-09-followup/`: `R4_F_gamma_envelope_proof.md` (440 lines, full proof), `R4_F_gamma_envelope.py` (264 lines, mp.dps=50), `R4_F_gamma_envelope.out` (99 lines, 46-case table).

## [2026-05-09] result | R2 NO MATCH — all geometric/motivic routes to `2/(3π)` exhausted

R2 (NC₁₅ geometric/motivic period for `2/(3π)`) completed in ~9 min wall-clock. Verdict: **NO MATCH** at conf 0.85. 46 candidates evaluated across 11 categories at mp.dps = 50. 4 numerical matches at ≥30 digits all classified ALGEBRAIC_EQUIVALENT (reduce to `(2/3)·(1/π)` via elementary substitution; no canonical geometric origin for prefactor `n ∈ {4, 8, 16}`). 1 near-miss (`7/33`) rejected at digit 5. 41 NO_MATCH. Structural conclusion: `2/(3π)` is **shallow / recipe-derived, not motivic**.

New findings beyond the prior partial NC₁₅:
- **Adelic κ_∞ = 2/3 conjecture demoted 0.40 → 0.15.** Trigamma probe at k=12,…,100 shows `ψ'(k/2)/(ψ'(k/2)+ψ'(k/2+1))` approaches 1/2, not 2/3 — closes an open flag from `Adelic_Langlands_route.md §4.1`.
- **Beilinson K₂(X_0(11)) regulator** ruled out numerically via 5 probes. LMFDB E_{11a1}: `L(E,1) ≈ 0.2538`, `L(E,2) ≈ 0.5408`, `Ω ≈ 1.2692` — no rational shape matches `2/(3π)`.
- Mahler-measure identities (Smyth, Boyd 11a1), hyperbolic 3-manifold volumes (figure-8, ideal tetrahedron), higher Mirzakhani volumes (M_{0,4}, M_{2,0}), and Witten-Kontsevich intersection numbers all FAIL.

Cumulative effect on Theorem B-exact unconditional: **3 of the 4 near-term structurally-distinct routes are now formally closed** (S4 P1a, C2 P1b, geometric R2). The space of viable routes reduces to: (i) R3 double-parabolic Eisenstein cross term (in flight), (ii) the support-4 1-level density / GDC wall (multi-decade open).

Confidence "Theorem B-exact requires NC₃/₉/₁₃ breakthrough" lifts 0.93 → **0.96**.

Two publishable byproducts: (a) "`2/(3π)` admits no non-trivial geometric/motivic period at conf 0.85" — settles a Compositio-tier question that the Adelic/Beilinson speculation in the bundle had left open; (b) Adelic κ_∞ = 2/3 falsified.

Deliverables in `handoff-2026-05-09-followup/`: `R2_NC15_geometric_motivic_period.md` (606 lines, 7 required sections + master 46-candidate table + sensitivity panel + distractor panel), `R2_NC15.py` (711 lines, mp.dps = 50, 46 candidates), `R2_NC15.out`.

## [2026-05-09] dispatch-3 | research-progress batch (R1, R2, R3, R4) — proof attempts

Per user redirect, pivoted from paper/drafting follow-ups to proof-progress dispatches. Four parallel Opus extra-high background agents fired:

| ID | Goal | Stakes |
|---|---|---|
| **R1** | Analytic proof attempt for **Conjecture B+** (`B(p) > 0` for primes with `M(p) ≤ −3`) — currently 0.80 numerical-only, restored from 0.40 by P2 today. Aistleitner-Berkes-Tichy bilinear / Bridge identity composition / Mertens-restricted prime-Mu correlation routes available. | Promotes Paper B's load-bearing claim conjecture-with-evidence → theorem |
| **R2** | NC₁₅ geometric/motivic period for `2/(3π)` — last unexplored angle from prior AUTONOMOUS_PLAN (rate-limited mid-flight). 10+ candidates evaluated symbolically at 30+ dps. Beilinson regulator / Selberg trace coefficient / vol fundamental domain / period of CM elliptic curve / etc. | If MATCH: structurally distinct route to Theorem B-exact, Compositio-tier novelty |
| **R3** | Double-parabolic Eisenstein cross term unconditional evaluation — single-residue obstruction from C1 Synthesis Identity (E) §6.5. Routes: Beilinson-Deligne motivic / effective Hoffstein-Lockhart / Goldfeld-Stade GL(3) / Cohen-Friedlander subconvexity. | If VIABLE-FOR-EXACT: closes Theorem B-exact unconditional structurally distinct from support-4 GDC wall |
| **R4** | F(γ) bias envelope theoretical proof — empirically 45/45 at 0.88. Iwaniec-Sarnak large-sieve + Selberg variance bound. | Lifts C1 mechanism F(γ) confidence 0.88 → 0.95 (Paper A secondary) |

Each task ≤6h wall-clock (within 1-day cap, no further breakdown needed). Each follows the codified mandatory protocol: PDF-citation verbatim verification, single confidence rule, honest verdict, cross-reference prior failed routes, don't switch problem.

## [2026-05-09] result | F1 PASS + F5 done — Δ-machine draft is essentially clean

F1 (P3a draft audit vs P1a/P1b/P2 verdicts) completed in ~5 min. Audit confidence 0.97. Verdict: **draft is largely independent of the failed routes.**

Distribution: **0 BLOCKING, 1 HIGH, 1 MEDIUM, 1 LOW (informational).**

Already correctly handled in the draft itself: strong-form polylog already demoted to Theorem 2.3 `O(√N(log N)^{k-1})` at 0.97; CS 2007 §7 unitary/orthogonal already in Appendix L.1; IK Thm 5.36 misnumbering also addressed. The draft never mentions `2/(3π)`, `4/(3π)`, KMV §5, S4 sufficient conditions, Theorem B-exact, Bern/Saw, B(3299), Conjecture B+, Mertens-restricted positivity, B2 v3, α_ratio, or Soshnikov-Palm — so most failure modes the audit looked for simply weren't in scope.

Single residual issue: bibliography entry E. (Hughes--Mezzadri 2008 / arXiv:0708.2922) was wrong on three counts (wrong arXiv ID = plasma physics, wrong attribution of `1/12` to orthogonal, dangling §10.6 cross-reference).

F5 (apply edit list) executed directly via Edit tool (faster than MIMO round-trip for a 1-edit task). Replaced the wrong block with two correctly-sourced entries:
- [CRS 2006] arXiv:math/0508378 — unitary `1/12 = G(3)²/G(5)`
- [Andrade--Best 2023] arXiv:2312.04981 — orthogonal `b^{SO}_{1,1}(1,1) = 1/2` in `(2N)³` norm

Plus inline provenance note pointing at P1b verdict for the correction trail. Draft 4229 → 4246 lines.

MIMO bulk lane stays primed for F8 (post-F2/F3 refinement) and F9 (Paper B Farey-side).

Effort estimate revision: F8 likely much smaller than originally planned. F1 confirmed draft is in publishable shape on the verdict axis. Per-section MIMO refinement now contingent on whether F2 (cross-Selberg slope) or F3 (B'-denom) require new draft material — most likely small additions to §5.6 / §7.2 only.

## [2026-05-09] result | F4 PASS — MIMO bulk lane online (~5 min)

F4 completed in ~5 min wall-clock. MIMO API contract discovered, dispatcher wrapper built, round-trip 6/6 passed.

Provider: **Xiaomi MiMo Open Platform** at `https://api.xiaomimimo.com/v1` (OpenAI-compatible). 5 chat models exposed: `mimo-v2-flash` (default, ~1.5s round-trip), `mimo-v2-omni`, `mimo-v2-pro`, `mimo-v2.5`, `mimo-v2.5-pro`. Auth: `Authorization: Bearer $MIMO_API_KEY`. `thinking:{type:disabled}` required (confirmed empirically — without it, `reasoning_content` field is set and `content` empty per the bundle's note).

Wrapper at `scripts/dispatch_mimo.sh` with flags `--model`, `--max-tokens`, `--system-file`, `--temperature`, `--raw`. Default `mimo-v2-flash` + 8000 max tokens. Reads prompt from file or stdin; stdout = pure text for piping; stderr = errors with key masked. Round-trip test 6/6 green including a key-leak grep across all outputs.

Documentation at `scripts/dispatch_mimo.md`.

Known limitation: `mimo-v2-flash` occasionally emits stray `</think>` tags with a system prompt. Documented for downstream pipelines (sed pipe).

MIMO bulk lane now open. F5 (apply F1's edit list to Δ-machine draft) gated on F1 completion; F8 (draft refinement) gated on F1+F2; F9 (Paper B Farey-side draft) gated on nothing — could fire now but no immediate need.

## [2026-05-09] dispatch-2 | follow-up batch (F1, F2, F3, F4) + direct housekeeping

Per user direction "carry on; >1d tasks broken into steps; MIMO for bulk; Opus extra-high for deep blocks" — dispatched 4 parallel Opus extra-high background agents:

| ID | Task | ETA |
|---|---|---|
| F4 | MIMO API discovery + `scripts/dispatch_mimo.sh` wrapper round-trip-tested | 15-60 min |
| F1 | Audit `Delta_machine_paper_compositio_draft.md` against P1a/P1b/P2 verdicts (draft was written before verdicts landed) → section-by-section edit list | 2-4 h |
| F2 | Cross-Selberg slope mismatch (12-19% at N=3×10⁴) root-cause diagnosis → structural fix / numerical extension / formal open-problem verdict | 3-6 h |
| F3 | B'-denominator Selberg-Beurling mollifier viability assessment → verdict VIABLE-FOR-* / BLOCKED / OPEN | 3-6 h |

Direct housekeeping completed (~10 min):
- `handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check_CORRIGENDUM.md` — two cite corrections recorded (`arXiv:0708.2922` is plasma physics not Hughes-Mezzadri; K-S `~ 2√N` should be Andrade-Best `~ 4N`); preserves original verbatim
- `scripts/poll_aristotle.sh` — status / download / `--watch` helper for Aristotle project `424973ae-8e9a-4ef1-8a6d-970ffa3b88ad`
- `scripts/latex_convert.sh` — pandoc → LaTeX → PDF wrapper for the Δ-machine draft (deferred until `brew install pandoc`)
- `HANDOFF.md` v4 — refreshed to session-end state with F1-F9 priority list, codified PDF-citation protocol as permanent rule, indexed all session deliverables

MIMO lane will go online once F4 lands (~15-60 min). Subsequent bulk tasks (F5 apply F1's edit list, F8 draft section refinement, F9 Paper B Farey-side first sections) queued for MIMO dispatch via that wrapper.

## [2026-05-09] cleanup | repo reorganization + priority commit

Cleanup of repo sprawl post 2026-05-04 handoff bundle. Root went from ~95 entries to 25.

Moved to `archive/`:
- `aristotle-runs/` — 9 `*-aristotle/` UUID/named dirs + `tmp_aristotle/` (47 MB)
- `aristotle-results/` — 9 `aristotle*results*` variants + `tmp_aristotle_results/` (166 MB)
- `extracts/` — `extract_5{c,d}/`, `extract_9f/` (16 MB)
- `request-projects/` — `RequestProject{,_aristotle}/` Lean from prior agent runs (20 MB)
- `sessions/` — SESSION{8,9,10,11}_HANDOFF.md, SESSION_HANDOFF_LATEST.md, PRISM_HANDOFF.md, REVIEWER_HANDOFF.md, prism_handoff.zip
- `queues/` — M1MAX_*, M5MAX_*, API_OVERNIGHT_QUEUE.md, CODEX_NEXT_TASK.md, CODEX_VERIFICATION_AND_DIRECTIONS.md, TRACKED_PROCESSES.txt
- `old-paper-plans/` — PAPER_PLAN.md, OVERNIGHT_PAPERA_PLAN.md, NDC_PAPER_PLAN.md, SPECTROSCOPE_PAPER2_PLAN.md, PAPER_CLEANUP_ISSUES.md, PAPER_CONSTELLATION.md, PAPER_GAPS.md, KOYAMA_JOINT_PAPER_CHECKLIST.md, KOYAMA_REPLY_DRAFT.md, ROGELIO_REPLY_DRAFT.md, ENDORSER_*.md, OUTREACH_*.md, GUIDE_FOR_ROGELIO.md, GRAPHICS_APPLICATION_REPORT.md, both submission guides
- `old-trackers/` — MASTER_TABLE*.md, DIRECTION_TRACKER.md, MATH_VALUE_TRACKER.md, INSIGHTS.md, TOP_DISCOVERIES.md, TODO_LIST.md, GRH_CONDITIONAL_THEOREM.md, SPECTROSCOPE_APPLICABILITY.md
- `misc/` — TERRAIN_LOD_ENGINEERING_ASSESSMENT.md (off-topic), `newfractionsum_aristotle{,2}` (binaries)

Total archived: ~233 MB.

Rewrote `README.md` and `HANDOFF.md` to point at `handoff-2026-05-04-theorem-B-and-C1/` as canonical state and supersede the stale 2026-04-24 Token Economy / Fresh Farey framing.

Top 3 priorities committed:
- P1 (this week): T1 + T2 verifications — PARI Mellin (KMV §5 leading constant `c₁ = 4/(3π)`?) + O(2N) Monte Carlo (orthogonal Barnes-G coefficient `1/12`). Closes Theorem B-exact unconditional if both pass.
- P2 (this week, parallel): B≥0 identity audit — verify `B·n'²/2 = Bern − Saw` against original `B(p)`. Settles whether `Bern(3299) < 0` is real counterexample or decomposition bug. Currently blocking Paper B writeup.
- P3 (this month, parallel, sibling track): Δ-machine G1 + G3 — Compositio bundle (~50pp, P=0.80) + Aristotle Lean SmoothedDwfFormula extension (~600 LOC, P=0.70). Independent of GDC wall.

Dropped/deferred: full Theorem B-exact via support-4 closure (multi-decade GDC wall); Theorem B level-aspect full uncond (honest 0.18–0.22); Paper C `K log K` surrogate (likely false); Posture B force-unification; W2-prime / Koyama work not advancing Theorem B; writing Paper A or Paper B until P1+P2 settle; all 16 documented failed Theorem B-exact attack routes.

## [2026-05-09] task-bundle | Opus 4.7 extra-high task prompts drafted

Drafted 5 self-contained subagent task prompts in [`tasks/`](tasks/). Each follows the AUTONOMOUS_PLAN mandatory protocol verbatim (no fabrication, single confidence rule, honest verdict, cross-reference prior failures, don't switch families).

| Task | File | Direction | Target | Wall-clock |
|---|---|---|---|---|
| P1a | `tasks/P1a-T1-PARI-Mellin-KMV.md` | T1 — KMV §5 leading constant via PARI/GP Mellin | Opus 4.7 extra-high | 1–4 h |
| P1b | `tasks/P1b-T2-orthogonal-MC.md` | T2 — orthogonal Barnes-G `1/12` via O(2N) Monte Carlo | Opus 4.7 extra-high | 4–24 h |
| P2 | `tasks/P2-B-geq-0-identity-audit.md` | B≥0 identity audit `B·n'²/2 = Bern − Saw` vs original `B(p)` | Opus 4.7 extra-high | 4–12 h |
| P3a | `tasks/P3a-G1-delta-machine-bundle.md` | G1 — Δ-machine Compositio paper bundle ~50pp | Opus 4.7 extra-high | 8–24 h |
| P3b | `tasks/P3b-G3-lean-smoothed-dwf.md` | G3 — `SmoothedDwfFormula.lean` stub→full ~600 LOC | Aristotle (harmonic.fun) | 4–8 weeks |

API key check on this machine (`za` user): only `ANTHROPIC_API_KEY` set. Aristotle and MIMO keys MISSING — flagged for user to share before P3b dispatch.

## [2026-05-09] result | P1b FAIL + 2 positives — session complete (5/5)

P1b (orthogonal Barnes-G MC) completed (~70 min wall-clock). Verdict: **FAIL** at confidence 0.97 in the FAIL.

The orthogonal Barnes-G analog claimed in `Reverse_engineer_constant.md` is `1/12` per Andrade-Best 2023 (arXiv:2312.04981) Theorem 2.4 it's actually `b^{SO}_{1,1}(1,1) = 1/2` in `(2N)³` norm or `4` in `N³` norm. Off by factor 6. The decomposition `2/(3π) = (1/(2π))·(1/12)·16` interpreted as a Haar-MC orthogonal identity over SO(2N) is **wrong**.

**Theorem B-exact via C2 decomposition route is dead.** Combined with P1a's FAIL on the S4 route, the two most ambitious near-term unconditional routes are both formally closed. Cage uncond 0.97 (Annals headline) untouched.

Two more misattributions caught (claims #9 and #10 in the running tally since 2026-05-03):
9. `arXiv:0708.2922` cited for "Hughes-Mezzadri orthogonal `1/12`" is actually a **plasma physics paper**. Intended math ref is CRS 2006 (`math/0508378`), which is **unitary** — wrong arXiv, wrong paper, wrong symmetry type. Triple-wrong.
10. `C2_orthogonal_MC_check.md` cited K-S `E[Λ²]_{SO(2N)} ~ 2√N`. Correct is `~ 4N` per Andrade-Best, verified by fresh K=20000 MC (5-12× discrepancy with the cited form).

**Positive finding (NEW):** **B2 v3 Soshnikov α_ratio=1 verified to extend to orthogonal symmetry.** Bulk-scaled Var(S_κ) MC at SO(400), SO(800) matches Soshnikov-Palm prediction at both κ=0 (~0.14 ↔ 0.13) and κ=39.48 (≈2.4 ↔ 2.33). Closes the ~0.04 confidence gap in `B2_R_neigh_v3_polished.md` §4 symmetry-independence. B2 v3 confidence lifts ~0.86 → ~0.90.

**Pre-submission cleanup added to TODO list:** update `C2_orthogonal_MC_check.md` to reflect `~ 4N` and remove the wrong `arXiv:0708.2922` citation.

Deliverables in `handoff-2026-05-09-followup/`: `C2_orthogonal_MC_extended.{md,py,out,summary.json}`, `C2_orthogonal_symbolic_supplement.{py,out}`, `raw_samples/*.npy` (15 files).

---

## [2026-05-09] session-net | All 5 agents complete; net program state

| Direction | Pre-session | Post-session |
|---|---:|---:|
| Theorem B-exact uncond via S4 | ~0.55 | **dead ≤0.05** |
| Theorem B-exact uncond via C2 | ~0.85 if T1+T2 pass | **dead** (decomposition wrong) |
| Cage uncond 0.97 (Annals) | 0.97 | unchanged |
| B2 v3 (Soshnikov, orthogonal symmetry-independence) | 0.86 with 0.04 gap | **0.90** |
| Conjecture B+ (Paper B Farey-side) | 0.40 | **0.80** |
| Δ-machine Compositio paper | 5,484 words | **30,082-word ~50pp draft** + 605-line audit + 354-line registry |
| Δ-machine Lean (G3) | 114-LOC stub, 8 axioms | **queued on Aristotle async (`424973ae-...`, 4-8 weeks)** |
| Higher-order polylog conjecture | claimed `O((log N)^{k-1})` | corrected to `O(√N (log N)^{k-1})` Thm 2.3 (0.97) + RMT-cond conj 2.4 (0.75) |
| Bern/Saw refutation route | live | **retracted** |
| Inflated/misattributed claims caught | 5 (2026-05-03) | **10 total** (+5 this session) |

Three papers now have foundations: Paper A (Annals cage), Paper B (Compositio Farey-side, positivity restored), Δ-machine Compositio sibling (50pp draft).

Pattern lesson reinforced: 10/10 catches were citations of paper+theorem# with exponent/threshold not matching actual paper text. The `curl + pdftotext + verbatim quote` protocol is the load-bearing mitigation. Codifying as a permanent rule.

## [2026-05-09] result | P3a PASS — Δ-machine Compositio paper draft delivered (30,082 words / ~50pp)

P3a respawn (chunked Write strategy) completed successfully. 10 sequential Write/Edit chunks, max 4,000 words each — no stream watchdog stalls.

Deliverables in `paper/`:
- `Delta_machine_paper_compositio_draft.md` — 4,229 lines / 30,082 words / ~50+ typeset pages
- `Delta_machine_paper_citation_audit.md` — 605 lines / 3,975 words (frozen scaffolding from prior agent)
- `Delta_machine_paper_theorem_registry.md` — 354 lines / 2,306 words (frozen scaffolding)
- Total package: 5,188 lines / 36,363 words

Structure: 10 sections (§1 Intro, §2 Selberg axioms S1-S5, §3 Master theorem 2.1-2.8, §4 Extensions, §5 Numerical evidence, §6 Applications, §7 Open problems, §8 Lean formalization, §9 `deltamachine` toolkit appendix, §10 Bibliography) + 20 appendices A-T.

Honest moves documented (the right ones, by the protocol):
- **Strong-form polylog conjecture demoted**: original `O((log N)^{k-1})` corrected to `O(√N · (log N)^{k-1})` Theorem 2.3 (conf 0.97) + RMT-conditional Conjecture 2.4 (0.75). 8th inflated claim caught by the protocol.
- **Cross-Selberg slope mismatch** (12-19% at N=3×10⁴) recorded as Open Problem 7.2, not swept under.
- **Murty-Murty 2009 prior-art gap** flagged as pre-submission blocker (Birkhäuser book not retrievable; novelty audit incomplete).
- Adversarial reviewer pass (Appendix L): 8 red flags + 3 yellow flags addressed.
- All 5 prior demotions reflected: CS 2007 §7, IK Thm 5.36, SY/Li, PARI lfunsympow, polylog.

Pre-submission requirements: Murty-Murty 2009 prior-art check; Aristotle Lean delivery (project `424973ae-...`, 4-8 weeks async); cross-Selberg slope close (extend to N=3×10⁵) OR formally state as open; LaTeX conversion (pandoc).

## [2026-05-09] result | P2 PASS — Conjecture B+ survives, Paper B unblocked

P2 (B≥0 identity audit) completed (~44 min wall-clock). Verdict: **Identity BUGGY, B≥0 Mertens-restricted SURVIVES** at confidence 0.97. Paper B positivity claim unblocked.

Audit method: 3-part exact-rational + Lean cross-check.
- (a) Lean `native_decide` cross-check: 5 hard-coded values reproduced bit-for-bit
- (b1) Exact `Fraction` identity audit at 235 primes p ∈ [11, 1500]
- (b2) Float64 identity audit at 10 sampled primes p ∈ [1499, 4999]
- (c) Direct `B(3299)` from Lean `crossTerm` + `M(3299)`

Findings:
- Identity `B·n'²/2 = Bern − Saw` **fails at every prime audited (245/245, 0 holds)**. Smallest counterexample p=11 (delta ≈ -1412.43). At p=3299, delta ≈ -1.88×10¹⁹.
- Bug source: `extra_high_attempt.md` line 46 silently used `D(f) = i/(n−1) − f`; Lean `displacement = rank − n·f`. Different displacement entirely — off by `(n−1)` factor AND additive `(1−f)`. Not the `n'²/2` rescaling claimed.
- `B(3299) ≈ -3.4246×10⁶` (NEGATIVE) directly from Lean `crossTerm`.
- `M(3299) = 20`, NOT ≤ −3 — so 3299 is OUTSIDE the Mertens-restricted conjecture's domain. The "Bern(3299) < 0" finding from `SESSION_SYNTHESIS_extra_high_round.md` was a decomposition artifact, not a counterexample.

Net effect on the program:
- Bern/Saw "refutation" route **retracted** — was a different bilinear sum on a different displacement
- Session synthesis demotion "B≥0 itself true: 0.60 → 0.40" **reversed**
- Conjecture B+ (`B(p) > 0` for primes with `M(p) ≤ −3`) **intact**
- Paper B positivity claim stands as conjecture-with-strong-evidence (118 Mertens-restricted primes verified positive to p≥1637; original program had verified to p=99,991 for broader claim)
- Adversarial-PDF protocol now caught **7 inflated/misattributed claims total** (5 from 2026-05-03 round + P1a + P2). Note: P2 is the second case where the misattribution was *over-pessimistic* — protocol catches both directions.

Deliverables in `handoff-2026-05-09-followup/`: `B_geq_0_identity_audit_FINAL.{md,py}`, `full_run.out`. Verbatim Lean sources quoted with line numbers from `archive/request-projects/RequestProject/{CrossTermPositive,DisplacementShift,PrimeCircle}.lean`.

## [2026-05-09] result | P1a FAIL — S4 route to Theorem B-exact unconditional is dead

P1a completed (~22 min wall-clock). Verdict: **FAIL** at confidence 0.92.

KMV (Crelle 2000) §5 retrieved and read verbatim. Two independent mismatches against the S4 prediction:
- Leading constant: KMV gives `14/3` (exact rational), not `4/(3π)` — off by factor `7π/2`
- Log power: KMV eq. (5) §2 gives `Q^h ~ c'_k (log q̂)^{2k+1}` so for k=1 it's `log³`, not `log⁴`

Mellin residue verified two ways (sympy Laurent + mpmath polynomial), agreement >12 digits at six sample L values. ζ' calibration sanity check at T=100, 500 reproduces prior bundle's PARI exactly — pipeline is correct, the failure is real.

**The 6th inflated claim caught by the `curl + pdftotext + verbatim quote` protocol** since the 2026-05-03 audit round began. `Weakest_sufficient_conditions.md` §5 step 5 attributed `4/(3π)` to KMV §5; KMV §5 says no such thing. Same shape as the 5-of-5 pattern flagged in `SESSION_SYNTHESIS_extra_high_round.md`.

Implications:
- S4 route added to failed-attacks list (now 17)
- Theorem B-exact via S4 confidence demoted ≤0.05
- Cage uncond 0.97 unchanged (orthogonal result)
- P1b (T2) still running but diminished — its PASS would have combined with T1; with T1 dead, T2 alone doesn't close Theorem B-exact unconditional. T2 still useful as RMT decomposition validation for the cage paper.
- Δ-machine (P3a respawn) and B≥0 audit (P2) untouched — both independent of S4

Deliverables in `handoff-2026-05-09-followup/`: `S4_KMV_Mellin_verify.{md,py,gp,out}`.

## [2026-05-09] respawn | P3a re-dispatched with chunked Write strategy

P3a (Δ-machine Compositio bundle) stalled ~12 minutes in. Failure mode: agent attempted "one Write call for 30,000+ words" — stream watchdog killed it. Salvaged 605-line citation audit + 354-line theorem registry (both protocol-compliant). Respawned with explicit "10 sequential Write/Edit calls, ≤4,000 words each, Edit-append for §2-§10" instruction. Salvaged audit + registry are frozen scaffolding; respawn builds on them rather than redoing.

## [2026-05-09] dispatch | 5 background agents fired (P1a, P1b, P2, P3a, P3b)

All 5 task prompts in `tasks/` dispatched as parallel Opus 4.7 background agents (Anthropic Claude Code Agent tool, model=opus, run_in_background=true). Deliverables target: `handoff-2026-05-09-followup/` (P1a, P1b, P2), `paper/` (P3a), `formal-conjectures/` (P3b).

P3b's spawned agent acts as DISPATCHER ONLY — its job is harmonic.fun API discovery + submit + receipt; the actual Lean proof generation continues async on Aristotle's side after submission. Long-running Aristotle work expected 4–8 weeks per task file.

Cost note: 5 parallel Opus agents consume substantial tokens. P3a alone targets ~30k-word output. MIMO fallback wired in `~/.farey_api_keys` for P3a if Opus rate-limits.

System will notify on each agent's completion. Stop-reports (`*_STOP_REPORT.md`) will appear in deliverable dirs if any agent hits a documented stop condition.

## [2026-05-09] config | API keys wired

User shared Aristotle (harmonic.fun) and MIMO API keys. Saved to `~/.farey_api_keys` with mode 600 (owner read/write only). Sourceable via `set -a; source ~/.farey_api_keys; set +a`. Both `ARISTOTLE_API_KEY` and `MIMO_API_KEY` confirmed exporting. Keys are NOT in the repo. Task `tasks/README.md` updated to mark all keys wired and ready for dispatch. Note: keys appeared in conversation transcript — recommend rotation after session if transcript will be persisted or shared.

## [2026-04-24] review | recent compute/API outputs

Reviewed the recent M1/API output bundle under `raw/farey-archive/recent-outputs/`. Promoted only roadmap-level consequences: W2 prime remains the main validation track; the log-conductor term stays live; simple Deligne/Gamma normalization does not explain C1; Paper C arithmetic-surrogate theorem language is blocked; pair-correlation work needs primary-source review and a fresh script. Marked stale-baseline, `CANNOT COMPUTE`, traceback, and placeholder-citation outputs as archive-only/context rot.

## [2026-04-24] sync | Koyama reply and routing refresh

Updated the Koyama correspondence record and claim ledger to reflect the latest reply: Koyama endorsed the bugfix-and-recompute update, highlighted the linear-in-rank observation as interesting, and introduced the "Dominance of -1" challenge with an explicit request for dynamic-range verification beyond the 13 trillion baseline. Also expanded the Farey routing docs so Groq, Cohere, SambaNova, Cerebras, OpenRouter, Mistral, Gemini, Aristotle, M1, M1B, M2, and farey-publisher are all represented in routing decisions.

## [2026-04-24] ingest | Fresh Farey Research

Reinitialized this folder as a local Fresh Farey repo, archived relevant old Farey evidence under `raw/farey-archive/` with `MANIFEST.jsonl`, copied canonical working data/scripts into `projects/farey-research/`, and synthesized lean Token Economy pages for current state, claim ledger, C1, W2 prime, Koyama correspondence, compute agents, task queue, and context rot.

## [2026-04-24] ship | universal agent framework v1

Added `start.md`, `token-economy.yaml`, the `te` CLI, lean agent adapters, L0/L1 memory files, wiki-search v1, context-refresh, delegate-router, and context-keeper v2 retrieval tools. Verified with `bash scripts/run_all_tests.sh`.

## [2026-04-24] ship | agent-ignition supplement

Added wiki schema v2 templates, model-agnostic skills/prompts, context meter + handoff lint, stricter delegation contracts, hooks/configs/extensions, install dry-run, profile support, framework smoke bench, and CI gate. Verified with `bash scripts/run_all_tests.sh`, `te wiki lint --strict --fail-on-error`, `te bench run --suite framework-smoke`, JSON config validation, and Python compile.

## [2026-04-24] ship | personal-assistant routing

Added `/pa` and `/btw` prompt bypass via `te pa`, hook routing, a personal-assistant skill, and router prompt. Purpose: route context-light prompts through a lightweight classifier/dispatcher with minimal context, escalating only when risk or complexity requires the main model.

## [2026-04-24] harden | repo-local startup review

Reviewed the framework, repo docs, and setup prompt for duplicated startup glue, stale global setup language, noisy hooks, and routing/context-meter gaps. Updated `HANDOFF.md`, startup docs, `L0_rules.md`, wiki schema defaults, docs audit scope, context meter model sizing, adapter overwrite detection, and prompt hook behavior. Verified with `bash scripts/run_all_tests.sh`, `./INSTALL.sh --dry-run`, `./te wiki lint --strict --fail-on-error`, `./te doctor`, `./te hooks doctor`, `./te bench run --suite framework-smoke`, Python compile, `git diff --check`, active-doc global-term scan, and token-budget checks.

## [2026-04-24] harden | fresh folder setup

Updated the setup prompt and onboarding docs to keep first-run setup simple: if the target folder lacks `token-economy.yaml`, the prompt explicitly permits clearing that current folder only, including hidden files and `.git`, then cloning the canonical repo fresh. Purpose: avoid false stops in non-empty setup folders while still forbidding deletion outside the target folder.

## 2026-04-17

Terminology: **ComCom** = our compound-compression project (disambiguate from Claude Code's "CC").
- Wiki created. Folder: repo-local `Token Economy/` markdown wiki.
- Ingested research brief → `raw/2026-04-17-research-brief.md`.
- Setup confirmed: caveman plugin active, superpowers skill loaded, wiki initialized.
- Next: flesh out concept pages, pick first project (likely compound-compression-pipeline or wiki-query-shortcircuit).
- Built [[projects/compound-compression-pipeline]] (aka **ComCom**). Measured 70-73% on prose, 59% on mixed technical at gentler rate. Code/paths/URLs preserved via placeholder protection.
- Ingested [[raw/2026-04-17-semantic-diff-survey]]. Novelty 4/5. Created [[concepts/semantic-diff-edits]]. Added [[ROADMAP]] as live tracker.
- Ran quality eval on Ollama (phi4:14b, 3 tasks). Result: 55.7% token savings @ 100% quality retention at rate=0.5. Placeholder format fixed (`XPROTECT{n}XEND` survives BERT tokenization). Compressed prompts also faster (1.4s vs 9.8s observed).
- Built eval-v2: SQuAD v2 + gemma4:31b judge + bootstrap CIs + failure-mode classification. Running in background.
- Built [[projects/semdiff]] (AST-node diff). Measured 95.5% savings after 2 method edits on argparse.py (2575 lines, 19,280 → 859 tokens); 99.5% on stable re-read. Tree-sitter for py/js/ts/rust.
- Kaggle auth set up (user: saarshai).
- Built [[projects/context-keeper]]. Skill + PreCompact hook. Regex extractor + optional local-LLM pass. Current framework writes memory under repo-local `.token-economy/` paths.
- **Eval-v2 completed** (SQuAD v2, n=8, 2 runs, phi4:14b + qwen3:8b judge). Token savings **44.5% CI [41.5-47.4]**. Δscore **−0.25 CI [−0.62, 0.00]**. Failure modes on comp: 8 NONE, 6 MISSING, 2 SWAP. **v1's "55.7% @ 100%" overstated**; principled measurement shows small, non-significant quality hit. N too small to resolve CI. Judge swap (gemma4:31b → qwen3:8b) fixed 129s latency thrash.
- Built ComCom v2 (pipeline_v2.py) with question-aware + critical-zone protection; eval-v3 in progress (4 conditions: full, v1, v2, adaptive-escalation). Early data shows v2 over-compresses (critical-protect + rate=0.5 on remainder = total too low). Fix planned: scale rate by (1 - protected_fraction).
- **semdiff MCP server built**. Python 3.11 + mcp SDK. 3 tools exposed (read_file_smart, snapshot_clear, snapshot_status). Protocol roundtrip tested (initialize, tools/list, tools/call all pass). CC plugin wrapper at `plugin/.mcp.json`. Install docs at [[projects/semdiff/INSTALL]].
- **bench/ built**. Kaggle API wired via registry.yaml. 7 datasets registered (2 downloaded so far). Adapters emit uniform {id, context, question, answer, type, meta} schema. CoQA multi-turn items designed for growing-context stress. Kaggle Notebook template drafted for free-T4-GPU evals (30h/wk, 10× local throughput). See [[bench/README]].
- **Eval-v3 complete (ComCom upgrade)**. D_adaptive (self-verify escalation) delivers 44.9% savings at Δscore −0.12 [−0.38, 0.00] — quality effectively preserved. Zero REFUSE failures. C_v2 (question-aware + critical-zone) confirmed broken by over-compression; fix deprioritized since D_adaptive bypasses the issue. Shipped config: `pipeline_v2.compress` + `verify.escalate_gen`.

## [2026-04-20] download-status | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=in-progress (authenticated curl running, ETA ~12h)
## [2026-04-20 22:36 BST] download-complete | Qwen3.6-35B-A3B-5bit | M1B all 5 shards verified (24.73 GB) via LAN HTTP server; shard1 required fresh download after dual-curl corruption; see /tmp/resume_qwen36_report.md
## [2026-04-20] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete (LAN transfer from M1:8888, all 5 shards verified, ~23GB, completed ~14:36 PDT)
## [2026-04-21] download-finish | Qwen3.6-35B-A3B-5bit | M1=complete, M1B=complete
## [2026-04-24] dispatch | Active Farey agent queue

- Created [[projects/farey-research/active-agent-queue]] after Saar approved the 30-task campaign.
- Scope: Koyama reply, Dominance-of-minus-one compute design, W2 prime validation, C1/Delta normalization, and theory/paper pipeline.
- Routing excludes M2 and Codex API for this campaign; dispatcher should use M1, M1B, Gemini, Aristotle, Groq, Cohere, SambaNova, Cerebras, OpenRouter, and Mistral.

## [2026-04-24] dispatch | First wave results

- Completed K01, K04, D01, W01, C01, and T01 for the active Farey campaign.
- T01 first blocked on M1 because Ollama was down, then completed via Mistral.
- Created heartbeat automation `farey-agent-queue-monitor` for 15-minute queue checks.

## [2026-04-24] dispatch | Long-haul queue extension

- Added a long-haul batch to [[projects/farey-research/active-agent-queue]] so M1B and M1 have several hours of follow-on work.
- Long-haul work is mostly M1B numerical/comparison tasks, with M1 theory/writeup tasks carrying explicit fallback routes so the queue can keep moving if the M1 daemon stays down.

## [2026-04-24] rule | subagent queue discipline

- Recorded the durable rule to close only completed idle subagents so thread slots clear cleanly.
- Recorded the monitor-subagent rule: once spawned, let the monitor keep dispatching until the queue is complete or Saar stops it, and do not intervene or review early.
## [2026-04-24] sync | queue commit and context refresh

- Confirmed `6cccca7 Extend Farey long-haul queue` is pushed to `origin/main`.
- Confirmed `./te context host-controls --agent auto` returned an invalid-choice error in this CLI, and the resulting checkpoint at `.token-economy/checkpoints/20260424-142312-fresh-session.md` is a generic handoff.
## [2026-04-24 13:39 BST] dispatch-update | First wave results
- K01 done on Gemini; K04 done on Cohere; D01 done on M1B; W01 done on M1B; C01 done on M1B.
- T01 blocked on M1 because `curl: (7) Failed to connect to 127.0.0.1 port 11434 after 0 ms: Couldn't connect to server`.
- W01 used `projects/farey-research/data/W2_PRIME_FIT.json` and matched stored coefficients to within `3.764e-14`.
## [2026-04-24] review | incoming Koyama and breakthrough queue

- Added [[projects/farey-research/incoming-results-review-2026-04-24]].
- Reviewed K02, K03, K05, K06 plus first-wave K01, K04, D01, W01, C01, and T01 at roadmap level.
- Updated [[projects/farey-research/active-agent-queue]] with the breakthrough queue and marked K06 as reject-as-written.

## [2026-04-24] routing | M2 enabled for active campaign

- Saar approved using M2 Ollama models for the new tasks.
- Updated active routing to allow M2, especially `qwen3.6:latest`, while keeping Codex API excluded.
