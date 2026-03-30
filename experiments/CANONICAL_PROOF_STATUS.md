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
| 11 | B >= 0 for all M(p) <= -3 primes to p = 100,000 | 4,617 primes | Exact computation. **FAILS at p=243,799** (B < 0). |
| 12 | B+C > 0 for all M(p) <= -3 primes to p = 100,000 | 4,617 primes | Exact computation. **FAILS at p=243,799** (B+C < 0). |
| 13 | Lean native_decide verification for specific small primes | p in {13,19,31,43,47,53,59,61} | Lean kernel |

### TIER 3: ESSENTIALLY PROVED (rigorous argument complete, minor gaps in writeup)

| # | Claim | What remains | Assessment |
|---|---|---|---|
| 14 | Triangular distribution of displacements | Large-sieve step needs careful writeup | Standard technique, gap is expository not mathematical |
| 15 | Composites have density zero among non-healing primes | mu-M independence needs standard citation | Textbook-level ingredient missing a reference |
| 16 | Sigma delta^2 = N^2/(2 pi^2) + o(N^2) (random model) | Steps 1-5 proved | Rigorous |

### TIER 4: DISPROVED (claims that turned out to be FALSE)

| # | Claim | Status | Details |
|---|---|---|---|
| 17 | Sign Theorem for all M(p) <= -3 primes | **DISPROVED** at p = 243,799 | DeltaW > 0 (n'^2*DeltaW = +6.65e9). B+C < 0 because alpha = 0.835 (T(N) > 0). See DELTA_W_DIRECT_PROOF.md |
| 18 | B >= 0 for all M(p) <= -3 primes | **DISPROVED** at p = 243,799 | B = -9.19e9. alpha + rho = -3.05. See B_PLUS_C_POSITIVITY.md |
| 19 | B+C > 0 for all M(p) <= -3 primes | **DISPROVED** at p = 243,799 | B+C = -6.18e9. See B_PLUS_C_POSITIVITY.md |
| 20 | DeltaW(p) < 0 for ALL primes p >= 11 | **DISPROVED** at p = 243,799 | The M(p) = -3 version also fails |

### TIER 5: CONJECTURAL (modified after disproof)

| # | Claim | Evidence | Status |
|---|---|---|---|
| 21 | D/A -> 1 as p -> infinity | **PROVED** via D'=A'+1 (Lean-verified) giving |D/A - 1| = O(1/p^2) | RESOLVED |
| 22 | DeltaW(p) < 0 for density-1 set of primes | ~73% of M(p)=-3 primes to 10^7; BDH gives alpha > rho for density-1 | Unproved but likely |
| 23 | DeltaW(p) < 0 for all primes with T(N) < 0 | T(N) < 0 implies alpha > 1, and alpha + rho > -1 for all tested | Partially provable |

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

6. **Theorem** (negative result): The Sign Theorem is FALSE in its universal form. DeltaW(p) > 0 at p = 243,799 (M(p) = -3). The failure mechanism is: Mertens oscillation causes T(N) > 0, collapsing alpha to 0.835, making B + C < 0.

7. **Theorem** (structural): B'/C' = alpha + rho algebraically, where alpha ~ -6R(N) and rho ~ -3.9. The sign of DeltaW is controlled by whether alpha + rho > -(A-D)/C' ~ 0. See DELTA_W_DIRECT_PROOF.md.

8. **Conjecture** (modified): DeltaW(p) < 0 for a density-1 subset of primes with M(p) <= -3. Exceptions occur when T(N) > 0 (~27% of M(p)=-3 primes up to 10^7).

---

## REMAINING OPEN PROBLEMS (ordered by importance)

1. **SIGN THEOREM IS DISPROVED.** The universal claim "DeltaW < 0 for all M(p) <= -3 primes" is FALSE at p = 243,799. New open problems:

   a. **Density theorem:** Prove DeltaW < 0 for a density-1 set of primes. Likely via BDH.
   b. **Characterize exceptions:** Understand exactly which primes have DeltaW > 0. Current: ~27% of M(p)=-3 primes to 10^7 have T(N) > 0 (and hence B+C < 0, likely DeltaW > 0).
   c. **Compute DeltaW at more counterexample primes** to confirm the pattern.

2. ~~Prove D/A -> 1~~ **RESOLVED** -- D'=A'+1 proved in Lean, |D/A-1| = O(1/p^2).

3. **Close Lean sorry placeholders.** 2 sorry remaining across 19 files.

4. ~~Extend computational base~~ **MOOT** -- extending past 243,799 would reveal counterexamples, not support the theorem. The computational theorem (p <= 100K) stands on its own.

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
