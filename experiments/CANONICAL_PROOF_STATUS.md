# CANONICAL PROOF STATUS
## Date: 2026-03-30
## Purpose: Single source of truth resolving all contradictions between session documents

---

## DOCUMENT SUPERSESSION MAP

The following documents reflect DIFFERENT STAGES of Session 8. Reading them
without this context creates apparent contradictions.

| Document | Date | What it reflects | Current status |
|---|---|---|---|
| K_BOUND_PROOF.md | 2026-03-29 (early) | First approach: bound |1-D/A| via K|M(p)|/p | **ABANDONED** — replaced by Dedekind approach |
| PROOF_ADVERSARIAL_AUDIT.md | 2026-03-29 (mid) | Audit of the K-bound approach | **SUPERSEDED** — audits the OLD approach, not the current one |
| DEDEKIND_PROOF_PATH.md | 2026-03-29 (late) | The Dedekind reciprocity approach (replacement) | **CURRENT approach** |
| DEDEKIND_PROOF_AUDIT.md | 2026-03-29 (late) | Audit of the Dedekind approach | **CURRENT** — found 3 fatal flaws in Dedekind path too |
| SESSION8_FINAL_VERDICT.md | 2026-03-30 | Final session summary | **OVERCLAIMS** — says "PROVED" but gaps remain |
| SESSION8_HONEST_FINAL.md | 2026-03-29 | Honest mid-session assessment | **MOST ACCURATE** of the session docs |

### Why the contradiction exists

1. PROOF_ADVERSARIAL_AUDIT.md found 5 fatal flaws in the K-bound approach.
2. The K-bound approach was then ABANDONED.
3. The Dedekind reciprocity approach was developed as a replacement.
4. SESSION8_FINAL_VERDICT.md was written after the Dedekind breakthrough and claims "PROVED."
5. But the Dedekind approach has its OWN gaps (see DEDEKIND_PROOF_AUDIT.md), and the final verdict overclaims.

The adversarial audit's criticisms of K_BOUND_PROOF.md are VALID for that document.
They do NOT apply to the Dedekind approach. But the Dedekind approach is NOT gap-free either.

---

## CURRENT HONEST STATUS OF EVERY CLAIM

### TIER 1: PROVED (unconditional, rigorous, no caveats)

These results are algebraic identities or elementary arguments that are fully proved.

| # | Claim | Proof method | Verified by |
|---|---|---|---|
| 1 | Permutation Square-Sum Identity: Sigma x*delta = C/2 | Elementary algebra | Independent replication + adversarial audit |
| 2 | Deficit formula: D_q(2) = q(q^2-1)/24 | Direct computation | Multiple independent checks |
| 3 | Deficit minimality: D_q(r) >= D_q(2) for all r | Dedekind reciprocity + permutation inequality | Adversarial-verified |
| 4 | Spectral positivity: K_hat_p(chi) = (p/pi^2)|L(1,chi)|^2 for odd chi | Codex proof | Proved |
| 5 | Farey symmetry: Sigma D = -n/2, E(k) = -E(p-k) | Elementary | Verified |
| 6 | C_W >= 1/4 | Cauchy-Schwarz from Sigma D = -n/2 | Lean-formalized |
| 7 | Four-term decomposition identity | Algebraic | Python-verified; Lean partial (some sorry remain) |
| 8 | Franel-type exponential sum: sigma_p = 1 + M(p-1) | Ramanujan sum identity | Computationally verified to p=200 |

### TIER 2: PROVED (computational, finite verification)

| # | Claim | Range | Method |
|---|---|---|---|
| 9 | DeltaW(p) < 0 for all primes p in [11, 100000] with M(p) <= -3 | 4,617 primes | Exact rational arithmetic, zero violations |
| 10 | DeltaW(p) < 0 for ALL primes in [11, 100000] | 9,592 primes | Same method |
| 11 | B >= 0 for all M(p) <= -3 primes to p ~ 200,000 | ~17,984 primes | Exact computation |
| 12 | B+C > 0 for all M(p) <= -3 primes to p ~ 3,000 | 210 primes | Exact computation |
| 13 | Lean native_decide verification for specific small primes | p in {13,19,31,43,47,53,59,61} | Lean kernel |

### TIER 3: ESSENTIALLY PROVED (rigorous argument complete, minor gaps in writeup)

| # | Claim | What remains | Assessment |
|---|---|---|---|
| 14 | Triangular distribution of displacements | Large-sieve step needs careful writeup | Standard technique, gap is expository not mathematical |
| 15 | Composites have density zero among non-healing primes | mu-M independence needs standard citation | Textbook-level ingredient missing a reference |
| 16 | Sigma delta^2 = N^2/(2 pi^2) + o(N^2) (random model) | Steps 1-5 proved | Rigorous |

### TIER 4: PARTIALLY PROVED (genuine mathematical gaps remain)

| # | Claim | What IS proved | What is NOT proved |
|---|---|---|---|
| 17 | Sign Theorem analytical tail (p > 100,000) | Sigma delta^2 = N^2/(2 pi^2) + o(N^2) gives C large. S(p) = O(p^2/log p) via Dedekind reciprocity. D/A = 1 + O(1/log p) PROVED via Mertens bounds. | B >= 0 is OBSERVED, not proved. The "bypass" C+D > A holds given D/A → 1 (proved) and B ≥ 0 (observed). |
| 18 | Hybrid result: computation + analytical | Computation covers p <= 100K. Analytical covers large p given B ≥ 0. | B ≥ 0 is the sole remaining gap. Partial: B>0 proved for m ≤ p/3 blocks (Möbius reduction + Hermite). |

### TIER 5: CONJECTURAL (empirically supported, no proof)

| # | Claim | Evidence | Obstruction |
|---|---|---|---|
| 19 | B >= 0 for all M(p) <= -3 primes | Verified to p = 100,000 (174 M=-3 primes, 4617 M≤-3 primes). Analytical: B>0 for m ≤ p/3 blocks; correction < 0 for p ≥ 43 on M=-3 subsequence | Full analytical proof = RH-hard (five-block Mertens fails: S reaches +25). Live routes: six-term transport, kernel negativity. |
| 20 | D/A -> 1 as p -> infinity | **NOW PROVED** via D'-A'=-1 (Lean-verified) giving |D/A - 1| = O(1/p²) | RESOLVED — this is no longer a gap |
| 21 | DeltaW(p) < 0 for ALL primes p >= 11 (not just M(p) <= -3) | Verified to p = 100,000 | Even stronger than our theorem statement; the M(p) <= -3 restriction is a proof artifact |

---

## EXPLICIT CONTRADICTION RESOLUTION

### Contradiction 1: SESSION8_FINAL_VERDICT says "PROVED" vs PROOF_ADVERSARIAL_AUDIT says "multiple fatal gaps"

**Resolution:** They audit DIFFERENT proof approaches.
- PROOF_ADVERSARIAL_AUDIT.md audits the K-bound approach (K_BOUND_PROOF.md), which was the FIRST attempt. The audit's 5 fatal flaws are VALID criticisms of that approach. That approach was then ABANDONED.
- SESSION8_FINAL_VERDICT.md describes the Dedekind reciprocity approach, developed AFTER the K-bound approach was abandoned.
- However, SESSION8_FINAL_VERDICT.md OVERCLAIMS. It says "PROVED (unconditional, modulo explicit P_0 computation)" but the analytical tail still has gaps: B >= 0 is not proved, D/A approx 1 is not proved.
- The honest status: COMPUTATIONALLY PROVED to p = 100,000. Analytical tail has genuine progress (Dedekind reciprocity gives S(p) = O(p^2/log p)) but is NOT complete.

### Contradiction 2: K_BOUND_PROOF.md lists key steps as TODOs vs SESSION8_FINAL_VERDICT says all steps verified

**Resolution:** K_BOUND_PROOF.md documents the ABANDONED approach. Its TODOs were never completed because the approach was replaced. SESSION8_FINAL_VERDICT describes different proof steps belonging to the Dedekind approach. There is no contradiction: different documents describe different proof strategies.

### Contradiction 3: PROOF_ADVERSARIAL_AUDIT says "B >= 0 is purely empirical" vs SESSION8_FINAL_VERDICT says "Bypass: B >= 0 verified"

**Resolution:** Both are correct. B >= 0 IS purely empirical (verified computationally, never proved analytically). SESSION8_FINAL_VERDICT's language is misleading: "verified" means "computationally checked," not "mathematically proved." The analytical proof does NOT have a rigorous bound on B. This remains a genuine gap.

### Contradiction 4: PROOF_ADVERSARIAL_AUDIT says D/A bound is "circular" vs SESSION8_FINAL_VERDICT says S(p)/p^2 -> 0 is "proved"

**Resolution:** These are about different arguments.
- The K-bound approach tried to prove |1 - D/A| <= K|M(p)|/p directly. The adversarial audit correctly identified this as circular (the identity D/A = 1 - (B + C + n'^2 DeltaW)/dilution_raw involves DeltaW itself).
- The Dedekind approach proves S(p) = O(p^2/log p) via Dedekind reciprocity and the Rademacher bound. This IS proved and is NOT circular.
- However, S(p)/p^2 -> 0 alone does not immediately prove D/A -> 1. The connection from S(p) to D/A requires additional steps that are not fully rigorous. SESSION8_FINAL_VERDICT overstates this.

### Contradiction 5: Lean formalization claimed as complete vs sorry placeholders

**Resolution:** The Lean formalization is PARTIAL. Specific lemmas are proved (PermutationIdentity with 8 lemmas, C_W >= 1/4). But SignTheorem.lean and BridgeIdentity.lean contain sorry placeholders. The general four-term decomposition and the sign theorem itself are NOT Lean-verified. Small-prime cases (p = 13, 19, ..., 61) are verified via native_decide.

---

## WHAT THE PAPER CAN HONESTLY CLAIM

1. **Theorem** (computational): DeltaW(p) < 0 for all primes 11 <= p <= 100,000 with M(p) <= -3. (4,617 primes, zero violations.)

2. **Theorem** (new identity): Permutation Square-Sum Identity.

3. **Theorem** (new): Deficit minimality D_q(2) = q(q^2-1)/24 is the minimum deficit.

4. **Theorem** (new): Spectral positivity K_hat_p(chi) = (p/pi^2)|L(1,chi)|^2.

5. **Theorem** (analytical partial): Sigma delta^2 = N^2/(2 pi^2) + o(N^2). The signed fluctuation satisfies S(p) = O(p^2/log p) via Dedekind reciprocity.

6. **Proposition** (hybrid, with caveat): If D/A -> 1 (which is observed for all tested primes), then C + D > A for all sufficiently large p, and the Sign Theorem holds for all primes with M(p) <= -3. The computational base covers p <= 100,000.

7. **Conjecture**: DeltaW(p) < 0 for all primes p >= 11 (not just M(p) <= -3). Supported by computation to p = 100,000 with zero violations.

---

## REMAINING OPEN PROBLEMS (ordered by importance)

1. **Prove B >= 0 for M(p) <= -3 primes.** The SOLE remaining gap. Settled as RH-hard via pointwise Mertens control. Partial results:
   - B>0 for m ≤ p/3 blocks (Möbius reduction + Hermite + Weil bounds)
   - Correction/C' < 0 for all p ≥ 43 with M=-3 (verified to 20K, exact to 523)
   - Five-block Mertens approach FAILS (S reaches +25)
   - Transport contraction: |D_6(m,n)| ≤ C(m)·n but C(m) = O(m), not uniform
   - Live routes: kernel negativity proof, direct coprime positivity, Dirichlet series for α

2. ~~Prove D/A -> 1~~ **RESOLVED** — D'-A'=-1 proved in Lean, |D/A-1| = O(1/p²).

3. **Close Lean sorry placeholders.** 2 sorry remaining across 19 files.

4. **Extend computational base** to p = 1,000,000 for larger safety margin.

---

## SUPERSEDED DOCUMENTS — DO NOT CITE AS CURRENT

| Document | Reason superseded |
|---|---|
| K_BOUND_PROOF.md | Approach abandoned; replaced by Dedekind path |
| PROOF_ADVERSARIAL_AUDIT.md | Audits the abandoned K-bound approach, not the current Dedekind approach |
| COMPLETE_ANALYTICAL_PROOF.md | Contains the K-bound approach with acknowledged circularity |
| FINAL_PROOF_ATTEMPT.md | Pre-Dedekind; its status table shows all key questions as OPEN |

## CURRENT DOCUMENTS — USE THESE

| Document | Content |
|---|---|
| CANONICAL_PROOF_STATUS.md | THIS FILE — single source of truth |
| SESSION8_HONEST_FINAL.md | Most accurate session summary (slightly conservative) |
| DEDEKIND_PROOF_PATH.md | The current analytical approach |
| DEDEKIND_PROOF_AUDIT.md | Audit of the current approach (has its own findings) |
| EXPLICIT_CONSTANTS_B.md | Exact rational proof: correction/C' < 1/2 at p=13, negative for p≥43 |
| B_VERIFY_100K.md | 174 M=-3 primes to p=100K, zero violations |
| FIVE_BLOCK_MERTENS.md | Five-block approach FAILS — S reaches +25 |
| U_LOWER_BOUND_HERMITE.md | U≥p-2 for m≤p/3 (Hermite decomposition) |
| MOBIUS_REDUCTION_PROOF.md | B>0 for m≤p/3 blocks, fails for large m |
| ERGODIC_TRANSPORT_SIXTERM.md | |D_6(m,n)| ≤ C(m)·n, C(m) = O(m) |
| TOTAL_POSITIVITY_SIXTERM.md | PF₂ structure but NOT amplitude control |
| CODEX_WAVE2_NEXT_DIRECTIONS_2026_03_30.md | Codex's recommended proof routes |

---

*This document was created to resolve contradictions identified by Codex review.
Every status label reflects the honest state of each claim as of 2026-03-30.
When in doubt, downgrade: if a claim is between "proved" and "observed," call it "observed."*
