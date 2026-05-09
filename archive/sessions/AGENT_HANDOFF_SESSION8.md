# Agent Handoff — Session 8 (2026-03-29)

## Mission
Close the **unconditional analytical proof** of the Sign Theorem:
> For every prime p ≥ 11 with M(p) ≤ -3: ΔW(p) < 0.

The computational verification is solid (4,617 primes to p=100,000, zero failures). The analytical tail argument has identified gaps that need closure.

---

## Current Proof Structure

### Four-Term Decomposition (Lean-verified)
```
ΔW(p) = W(p-1) - W(p) = A - B - C + boundary - D
```
ΔW < 0 iff B' + C' + D' > A' + 1 (unnormalized form, multiply by n'²)

### The Bypass Strategy (avoids proving B ≥ 0)
Show C' + D' > A' + 1, where:
- C' = Σ δ² (shift-squared, unnormalized)
- D' = Σ D²_new (new-fraction discrepancy, unnormalized)
- A' = Σ D²_old · (n'²/n² - 1) (dilution, unnormalized)

### Empirical Status (STRONG but not proof)
- C' ≥ 0.035·p² (min at p=13, stabilizes around 0.049)
- deficit = max(A'-D', 0) ≤ 0.006·p² (usually 0)
- C' - deficit > 1 for all p ≥ 6
- B ≥ 0 for ALL 210 M(p)≤-3 primes to p=3000 (R always positive, min R=+0.060)

---

## Three Gaps to Close (in order of difficulty)

### GAP 1: Prove D_q(2) = q(q²-1)/24 is the minimum deficit (MEDIUM)
**What:** For prime denominator q and multiplier r ≢ 0,1 (mod q):
  D_q(r) = Σ_{a=1}^{q-1} a² - Σ_{a=1}^{q-1} a·(ra mod q) ≥ q(q²-1)/24

The minimum is achieved at r = 2 (and r = q-1 by symmetry). This is:
  D_q(r) = q(q-1)(q-2)/12 - q²·s(r,q) where s(r,q) is the Dedekind sum.

**Status:** Verified for all primes q ≤ 997 (21,651 (q,r) pairs, zero violations).
**Why it matters:** Lower bounds C' = Σ δ² via PNT summation over prime denominators.
**Proof approach:** Use Dedekind sum properties. s(2,q) = (q-1)(q-2)/(12q) for odd prime q (known formula). Then D_q(2) = q(q²-1)/24. For minimality: show s(r,q) ≤ s(2,q) for all r, using Rademacher's bounds on Dedekind sums.
**File:** ~/Desktop/Farey-Local/experiments/CA_RATIO_PROOF.md (Section "Key Lemma")

### GAP 2: Non-circular bound on 1 - D'/A' (HARD — the critical gap)
**What:** Bound |1 - D'/A'| without using ΔW ≤ 0 (which is what we're proving).
**The circularity:** The identity 1 - D/A = (B + C + ΔW)/A uses ΔW, creating a loop.
**NEW FINDING (session 8):** Σ_{k=1}^{p-1} D_{F_p}(k/p) = -(p-1)/2 EXACTLY (non-circular!).
  This means the first moment of D_new is known. Need to bound the SECOND moment Σ D²_new.
**Non-circular formula:** D_{F_p}(k/p) = #{f ∈ F_{p-1} : f ≤ k/p} + k - n'·k/p = E(k) + k/p
  where E(k) is the Farey counting error at x = k/p.
**Approach:** Express Σ D²_new = Σ (E(k) + k/p)² = Σ E² + 2Σ E·k/p + Σ(k/p)².
  The E(k) terms involve Möbius-weighted floor sums, bounded by Farey discrepancy theory.
**Key reference:** Franel-Landau theorem gives bounds on Σ E². The Walfisz/El Marraki bound on M(x) should control the dominant term.
**File:** ~/Desktop/Farey-Local/experiments/BRIDGE_DA_RIGOROUS.md (agent working on this)
**Audit:** ~/Desktop/Farey-Local/experiments/PROOF_ADVERSARIAL_AUDIT.md (Fatal Flaw #2)

### GAP 3: C/A ≥ c/log²p with explicit constant (MEDIUM)
**What:** Prove C/A ≥ c₀/log²(p) for an explicit c₀, unconditionally.
**Ingredients available:**
  - Deficit identity: C' = 2·Σ_b D_b(p)/b²
  - Minimum deficit (GAP 1): D_q(2) = q(q²-1)/24
  - PNT (effective Rosser-Schoenfeld): Σ_{q prime, q≤x} q ≥ x²/(2logx)·(1-c/logx)
  - Farey L² discrepancy: Σ D²_old ≤ C_FL · n² · logN
**Proof sketch (needs formalization):**
  C' ≥ (1/12)·Σ_{good primes q≤N} q ≥ c·N²/logN
  A' ≈ 2(p-1)/n · Σ D²_old ≤ 2(p-1)/n · C_FL·n²·logN ≈ const·n·(p-1)·logN
  C/A ≥ c·N²/(logN · n·(p-1)·logN) = c/(log²N) since n ≈ 3N²/π²
**Status:** Proof sketch complete, constants need tracking. Agent working on rigorous version.
**File:** ~/Desktop/Farey-Local/experiments/CA_LOWER_BOUND_RIGOROUS.md (agent working)

---

## Promising Leads

### 1. Permutation Square-Sum Identity (PROVED)
Σ (a/b)·δ(a/b) = ½·Σ δ(a/b)² for all N < p.
**Proof:** 5 lines, uses permutation argument. Independently verified.
**Consequence:** B + C = -2·Σ R(x)·δ(x) where R is Möbius-weighted fractional parts.
**Files:** ~/Desktop/Farey-Local/experiments/PERMUTATION_IDENTITY.md, ~/Desktop/Farey-Local/experiments/IDENTITY_VERIFICATION.md

### 2. Deficit-Dedekind Connection
D_q(r) = q(q-1)(q-2)/12 - q²·s(r,q) connects shift deficits to Dedekind sums.
Min deficit D_q(2) = q(q²-1)/24 (verified q ≤ 997).
**File:** ~/Desktop/Farey-Local/experiments/CA_RATIO_PROOF.md

### 3. Σ D_new = -(p-1)/2 (NON-CIRCULAR)
The sum of new-fraction displacements is exactly -(p-1)/2 for every prime.
This provides a non-circular handle on D' = Σ D²_new.
**Status:** Just discovered, needs exploitation.

### 4. B+C = -2·Σ R·δ (Möbius Reformulation)
Connects the cross term to Kloosterman sums via T(m).
For M(p) ≤ -3: R is always positive (min R = +0.060).
**Files:** ~/Desktop/Farey-Local/experiments/BREAKTHROUGH_REFORMULATION.md

### 5. El Marraki (1995) Effective Mertens Bound
|M(x)| ≤ 0.6438·x/logx for ALL x > 1.
Ramaré (2013): |M(x)| ≤ 0.013·x/logx for x ≥ 1,078,853.
**File:** ~/Desktop/Farey-Local/experiments/EFFECTIVE_MERTENS_BOUNDS.md

---

## Key Files

### Paper and Core
- **Main paper:** ~/Desktop/Farey-Local/paper/main.tex (updated with permutation identity, El Marraki citation, corrected B+C scope)
- **Lean formalization:** ~/Desktop/Farey-Local/RequestProject/PermutationIdentity.lean (5 proved + 3 Aristotle proofs, 3 sorry for Finset plumbing)
- **Lean main:** ~/Desktop/Farey-Local/RequestProject/SignTheorem.lean
- **Lean cross term:** ~/Desktop/Farey-Local/RequestProject/CrossTermPositive.lean

### Proof Documents
- **Proof closure sketch:** ~/Desktop/Farey-Local/experiments/PROOF_CLOSURE.md
- **Adversarial audit (5 flaws):** ~/Desktop/Farey-Local/experiments/PROOF_ADVERSARIAL_AUDIT.md
- **Proof status overview:** ~/Desktop/Farey-Local/experiments/PROOF_STATUS_2026_03_29.md
- **CA ratio analytical proof:** ~/Desktop/Farey-Local/experiments/CA_RATIO_PROOF.md
- **D/A exact analysis:** ~/Desktop/Farey-Local/experiments/DA_RATIO_EXACT.md
- **Bridge D/A rigorous:** ~/Desktop/Farey-Local/experiments/BRIDGE_DA_RIGOROUS.md (may exist from agent)
- **Effective Mertens bounds:** ~/Desktop/Farey-Local/experiments/EFFECTIVE_MERTENS_BOUNDS.md

### Data and Verification
- **B+C by Mertens class:** ~/Desktop/Farey-Local/experiments/BC_BY_MERTENS_CLASS.md
- **Identity verification:** ~/Desktop/Farey-Local/experiments/IDENTITY_VERIFICATION.md
- **Fresh proof ideas:** ~/Desktop/Farey-Local/experiments/FRESH_PROOF_IDEAS.md
- **Denominator class analysis:** ~/Desktop/Farey-Local/experiments/DENOMINATOR_CLASS_PROOF.md
- **D vs sawtooth:** ~/Desktop/Farey-Local/experiments/D_VS_SAWTOOTH.md
- **Overlap verification:** ~/Desktop/Farey-Local/experiments/OVERLAP_VERIFICATION.md

### Tracking
- **INSIGHTS:** ~/Desktop/Farey-Local/INSIGHTS.md (discoveries N1-N12½)
- **MASTER_TABLE:** ~/Desktop/Farey-Local/MASTER_TABLE.md (96+ items)
- **CLAUDE.md:** ~/Desktop/Farey-Local/.claude/CLAUDE.md (project rules)

---

## What NOT to Do
1. Don't claim "proved" based on empirical constants alone
2. Don't use ΔW ≤ 0 in the proof of ΔW ≤ 0 (circularity!)
3. Don't overstate — the adversarial audit caught 5 fatal flaws in our last attempt
4. Don't forget: B+C < 0 at p=1399 (M=+8), so B+C > 0 is NOT universal

## What TO Do
1. Close GAP 2 first (D/A non-circular bound) — it's the critical path
2. Use Aristotle (harmonic.fun API) for any Lean lemma
3. Verify EVERYTHING with independent agents before claiming
4. Track explicit constants throughout — no hand-waving
5. The Σ D_new = -(p-1)/2 identity is fresh and unexploited — use it!

## Aristotle API
- Endpoint: https://harmonic.fun/api/prove
- Method: POST, Body: {"code": "LEAN_CODE_WITH_SORRY"}
- Works well for closing individual lemmas

## El Marraki Citation
El Marraki, M. (1995). "Fonction sommatoire de la fonction de Möbius, 3." J. Théor. Nombres Bordeaux 7(2), 407-433.
Key: |M(x)| ≤ 0.6437752 · x/log(x) for all x > 1.
