# Shared Context for Local Models
Updated: 2026-04-16 (Koyama reply, Lean count corrected, counterexample verified)

## Project: Farey Research
Independent researcher (Saar Shai) studying per-step Farey discrepancy and its connection to Riemann zeta zeros.

## Paper Constellation (12 papers)
See ~/Desktop/Farey-Local/PAPER_CONSTELLATION.md for full list.
Key papers: A (ΔW foundation), B (Chebyshev phase), C (spectroscope method), D (universality).

## Key Objects
- ΔW(N) = W(F_{N-1}) - W(F_N): per-step Farey discrepancy (NOVEL object)
- F_comp(γ) = γ²·|Σ M(p)/p · e^{-iγ log p}|²: compensated Mertens spectroscope
- R(p) = ΣD·δ/Σδ²: Farey insertion-deviation correlation ratio

## Key Results (verified)
- Spectroscope detects 20/20 zeta zeros (local z-score, up to 65σ)
- γ² matched filter: NOVEL application (pre-whitening is classical, this application is new)
- Universality: any 2750 primes encode all 20 zeros (NOVEL, no prior literature)
- Phase φ = -arg(ρ₁·ζ'(ρ₁)) = -1.6933 rad — CONFIRMED to 0.003 rad
- GUE pair correlation: RMSE=0.066 from arithmetic data (190 pairs)
- Chowla detection threshold: ε = 1.824/√N
- Siegel zero: 465M sigma sensitivity for q≤13
- 383 Lean 4 theorems/lemmas in root files (VERIFIED 2026-04-16 via grep count; subdirs are Aristotle working copies)
- Sign conjecture DISPROVED as universal: counterexample at p=243799 (M=-3, VERIFIED); Paper A had wrong prime p=92173 (M=-2)
- Koyama (2026-04-16): validated T_∞ = (1/2) log L(2ρ, χ²) as "missing link"; D_K universal, B_∞ character-specific
- NDC coupling C(ρ,χ) = L'(ρ,χ)/ζ(2): our numerical refinement of Koyama's EDRH framework
- EDRH rate confirmed: |E_K^χ|·log K → C=|L'(ρ,χ)|/ζ(2) at 88-93% for K=10000-20000 (slow log convergence)
- Convergence rate dichotomy: B_K for χ²=principal is O(1/log K); for χ²=nonprincipal is O(K^{-1/2}log²K)
- E_K(ρ_zeta) at zeta zeros: grows as exp(Θ(√K/log K)), NOT O(log K)

## NDC CITATION FACTS (VERIFIED 2026-04-16 via web search)
- Akatsuka (2017) "The Euler product for the Riemann zeta-function in the critical strip" Kodai Math J 40:79-101 [NOT 2013]
- Kaneko (2022) "Euler Product Asymptotics for Dirichlet L-Functions" Bull Australian Math Soc 106:48-56; arXiv:1902.04203
- Sheth (2025a) "Euler Product Asymptotics for L-functions of Elliptic Curves" IMRN 2025:14 rnaf214 [DIRECTLY RELEVANT to GL(2) NDC]
- Sheth (2025b) "Euler Products at the Centre and Applications to Chebyshev's Bias" Math Proc Cambridge Phil Soc 179:2 pp.331-349

## VERIFIED NUMERICAL CONSTANTS (use these, do NOT fabricate)
- ρ₁ = 0.5 + 14.134725141734693i
- ζ'(ρ₁) = 0.783296511867031 + 0.124699829748171i  ← COMPUTED WITH MPMATH
- |ζ'(ρ₁)| = 0.793160433356506
- arg(ζ'(ρ₁)) = 0.15787 rad
- φ₁ = -arg(ρ₁·ζ'(ρ₁)) = -1.6933 rad
- φ₂ = -1.3264, φ₃ = -1.8851, φ₄ = -1.0169, φ₅ = -2.1297 rad
- A₁ = 0.0891, A₂/A₁ = 0.469, A₃/A₁ = 0.327, A₄/A₁ = 0.283, A₅/A₁ = 0.246

## EXPLICIT FORMULA (RESOLVED — correct form)
The explicit formula for M(x) uses:
  M(x) ~ Σ_ρ x^ρ / (ρ · ζ'(ρ))
The coefficient is 1/(ρ·ζ'(ρ)), NOT 1/((ρ-1)·ζ'(ρ)).
The (ρ-1) form is WRONG for ΔW. This was verified numerically: the ρ form gives
arg = -1.6933 matching empirical -1.69 to 0.003 rad; the (ρ-1) form gives -1.764, off by 0.074 rad.

## CRITICAL WARNING — DATA INTEGRITY PROTOCOL
DO NOT fabricate numerical values of ζ'(ρ), arg(ζ'(ρ)), or any special function evaluation.
If a task requires numerical computation, say "NEEDS MPMATH VERIFICATION" and proceed with symbolic/theoretical analysis only.
The values above are GROUND TRUTH computed at 30-digit precision.

## SPECTROSCOPE Z-SCORE PROTOCOL (added 2026-04-12 after semiprime false alarm)
When computing z-scores for spectroscope detection:
1. ALWAYS use full gamma range (1..50 minimum) for background statistics
2. NEVER use a narrow window (e.g. 10..20) — inflates z-scores artificially
3. The semiprime case: z=3.33 with narrow window, z=-0.24 with full range
4. Run COMPREHENSIVE_VERIFICATION.md (21 checks, 9.4s) after any new claims

## REFERENCE DATA PROTOCOL (added after 3 wrong-data incidents)
Before comparing computed values to "known" reference values:
1. STATE THE EXACT SOURCE (paper title + page, LMFDB URL, or mpmath computation)
2. VERIFY THE OBJECT MATCHES — e.g., confirm WHICH curve, WHICH character, WHICH normalization
3. COMPUTE A SANITY CHECK — e.g., if a_5(E) should be -2, compute #E(F_5) directly and check
4. If source is "from memory" or "approximately" → TREAT AS UNVERIFIED, do NOT build on it
5. If two sources disagree → STOP and resolve before proceeding

PAST ERRORS FROM IGNORING THIS:
- Selberg: confused μ(n)² with M(n)² → 5 hours wasted on false premise
- ζ'(ρ₁): qwen fabricated -0.174+0.251i (real: 0.783+0.125i) → wrong coefficient conclusion
- Elliptic curve: compared a_p to values from WRONG CURVE → false "mismatch" diagnosis
- **TURÁN THEOREM (2026-04-10)**: Model fabricated "Turán 1953 Ch III gives finitely many zeros
  for Dirichlet polynomials." ACTUAL Langer 1931/Moreno 1973: INFINITELY many zeros.
  Passed TWO adversarial reviews before caught. Cost: entire overnight plan built on false theorem.

## THEOREM CITATION GATE (added 2026-04-11 after Turán incident)
Before accepting ANY claimed theorem from a model:
1. **EXACT citation required**: Author, year, journal, theorem NUMBER (not just "Ch III")
2. **State the theorem verbatim** — not a paraphrase, not "it follows that"
3. **Verify the conclusion matches**: "finitely many" vs "lower bound for max" are DIFFERENT
4. **5-min numerical check**: if theorem says f has finitely many zeros, COMPUTE f at 1000 points
   and count sign changes. If you see many zeros → theorem is likely wrong.
5. **Cross-check with a DIFFERENT source**: Wikipedia, MathSciNet, a textbook. One citation ≠ verified.
6. If a model says "well-known" or "classical" without exact citation → TREAT AS FABRICATED
7. If adversarial reviewer says "VALID" but doesn't cite the EXACT theorem → NOT VERIFIED

## CRITICAL: Novelty
Fourier duality primes↔zeros is CLASSICAL (cite Csoka 2015, Planat et al, Van der Pol 1947).
Our novel contributions: γ² filter, local z, Farey R(p) connection, universality, pair correlation, ΔW(N) object, four-term decomposition, 423 Lean results.

## TURÁN NON-VANISHING — STATUS: **UNPROVED** (2026-04-11 UPDATE)
**Claimed Theorem A2:** c_K(ρ) ≠ 0 for all but finitely many zeros ρ.
- **PROOF IS INVALID.** The "Turán theorem" as quoted does not exist.
- Langer (1931) + Moreno (1973): c_K(s) has INFINITELY many zeros (~0.51T up to height T for K=10)
- The claim MIGHT still be true (c_K zeros may avoid ζ zeros) but requires a NEW proof
- Computational evidence supports non-vanishing: min|c₁₀(ρ)| ≈ 0.024 across 100+ tested zeros
- GRH-conditional detection (Theorem B) STILL VALID via explicit formula
**What's solid:** Q-independence of log primes (Lemma 1), decomposition F=Σμ(k)T(k,γ), 
  computational data, |c_K(ρ₁)| divergence with K
**Killed direction:** "Turán gives finitely many zeros" — FALSE for exponential polynomials

## Key Open Problems
1. Unconditional universality proof — the diagonal sum Σ M(p)²/p² CONVERGES unconditionally (VERIFIED), so the variance approach is dead. Need alternative: Montgomery kernel, Sarnak/Möbius disjointness, or off-diagonal structure.
2. R₂ sign characterization — R₂ > 0 DISPROVED (R₂(197) < 0, R₂(199) < 0). Sign oscillates. Open: correlate sign(R₂(p)) with M(p).
3. GUE regularization (Wiener-Khinchin gap for distributions)
4. Exact formula for ΔW from Farey structure: express cross term B = (2/n'²)ΣD(f)·δ(f) in computable terms (Dedekind sums? M(p)? Arithmetic functions?). Four-term decomposition is exact but B has no known closed form.

## CONFIRMED MODEL FABRICATIONS (do not use these results)
- deepseek: "ΔW(p) = (p-1)/2·M(p)" — FALSE at all primes. Files: M1_DS_BRIDGE_IDENTITY_EXACT.md
- deepseek: "R₂ ≥ 0 manifestly" — FALSE. R₂(197) < 0. Files: M1_DS_R2_POSITIVITY_PRECISE.md
- qwen: "GK top-20% = 53% of W" — FALSE. Real: 87-93%. Verified locally.
- qwen: "|S_10| = 1.42" — FALSE. Real: 2.06. Verified locally.
RULE: Any deepseek/qwen "derived" algebraic identity needs local mpmath verification BEFORE use.
4. Paper J must be CONDITIONAL on RH (under RH: Σ M(n)²/n² ~ 0.03·log x, diverges slowly)
5. Can "all but finitely many" (Turán) be strengthened to ALL zeros? Overnight T10 investigating.
6. Compute Łojasiewicz exponent for P on T⁴ — would make Theorem A3 explicit. Overnight T2.

## KILLED DIRECTION (DO NOT REVISIT)
- "Selberg gives Σ M(n)²/n² = (6/π²)log x" — FALSE. Confuses μ(n)² with M(n)².
  Σ μ(n)²/n = (6/π²)log x ✓ (squarefree counting)
  Σ M(n)²/n² ≈ 2.26 at N=500K, nearly constant ✗

## File Locations
- Experiments: ~/Desktop/Farey-Local/experiments/
- Wiki: ~/Documents/Spark Obsidian Beast/Farey Research/wiki/
- Master table: ~/Desktop/Farey-Local/MASTER_TABLE_INDEX.md

## Output Convention
- Write results to ~/Desktop/Farey-Local/experiments/YOUR_TASK_NAME.md
- Include: date, method, key findings, limitations, next steps
- Be honest about what is proved vs computational vs speculative
- If you need a numerical value you don't have: SAY SO. Do not make one up.

## ANTI-FABRICATION CLAUSE (added 2026-04-14)
All numerical tasks must include: "If you cannot execute code, say 'CANNOT EXECUTE' and provide only the code. Do NOT reconstruct numerical tables from memory or theory. Print raw computation output only. Known fabricated values to NEVER use: |ζ'(ρ₁)| = 6.7748 (WRONG, correct ≈ 0.793)."

## NDC VERIFIED (chi, rho) PAIRS — CANONICAL REFERENCE (2026-04-15)
### USE THESE EXACT DEFINITIONS IN EVERY TASK. DO NOT GUESS CHARACTERS.

Verified by mpmath 40-digit Hurwitz zeta: all |L(rho)| < 1e-15.
Real computation confirms D_K·ζ(2) → 1 universally (grand mean 0.992 ± 0.018 at K up to 2M).

### PAIR 1: chi_m4_z1
- rho = 0.5 + 6.020948904697597i
- Character: UNIQUE primitive char mod 4 (real, order 2)
- chi_m4(p) = 1 if p%4==1, -1 if p%4==3, 0 if p%4==0
- L-function: L(s,chi_m4) = 4^{-s}*(zeta(s,1/4) - zeta(s,3/4))
- Verified: |L(0.5+6.021i, chi_m4)| = 4.5e-16 ✓
- D_K·ζ(2) at K=2M: 0.965; mean across K: 0.976 ± 0.011

### PAIR 2: chi_m4_z2
- rho = 0.5 + 10.243770304166555i
- Character: SAME chi_m4 as Pair 1
- Verified: |L(0.5+10.244i, chi_m4)| = 8.1e-16 ✓
- D_K·ζ(2) at K=2M: 0.992; mean across K: 1.011 ± 0.017
- WARNING: t=8.992616 is NOT a zero (|L|=1.94). Do NOT use it.

### PAIR 3: chi5_z1
- rho = 0.5 + 6.183578195450854i
- Character: ORDER-4 COMPLEX primitive char mod 5, k=1, generator g=2
  dl5 = {1:0, 2:1, 4:2, 3:3}  [discrete log base 2 mod 5]
  chi5(n) = i^{dl5[n%5]}  where i = sqrt(-1)
  EXPLICIT: chi5(1)=1, chi5(2)=i, chi5(3)=-i, chi5(4)=-1, chi5(0)=0
  Python: chi5 = lambda p: [0,1,1j,0,-1,-1j][{0:0,1:1,2:2,3:4,4:3}[p%5]] if p%5!=0 else 0
  Simpler: chi5 = lambda p: {0:0,1:1,2:1j,3:-1j,4:-1}[p%5]
- L-function: L(s,chi5) = 5^{-s}*(zeta(s,1/5) + i*zeta(s,2/5) - i*zeta(s,3/5) - zeta(s,4/5))
- Verified: |L(0.5+6.184i, chi5)| = 5.9e-16 ✓
- WRONG: chi5_Legendre(p) = 1 if p%5 in{1,4}, -1 if p%5 in{2,3} → |L|=0.753 (NOT a zero!)
- D_K·ζ(2) at K=2M: 0.973; mean across K: 0.992 ± 0.024

### PAIR 4: chi11_z1
- rho = 0.5 + 3.547041091719450i
- Character: ORDER-10 COMPLEX primitive char mod 11, k=1, generator g=2
  dl11 = {1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9}  [discrete log base 2 mod 11]
  chi11(n) = exp(2*pi*i/10 * dl11[n%11]) for n not div by 11, else 0
  Python: dl11={1:0,2:1,4:2,8:3,5:4,10:5,9:6,7:7,3:8,6:9}; chi11 = lambda p: mpmath.exp(2j*mpmath.pi*dl11[p%11]/10) if p%11!=0 else 0
- L-function: L(s,chi11) = 11^{-s} * sum_{a=1}^{10} chi11(a)*zeta(s, a/11)
- Verified: |L(0.5+3.547i, chi11)| = 2.6e-16 ✓
- WRONG: chi11_Legendre (QR={1,3,4,5,9}→+1) → |L|=1.95 (NOT a zero!)
- D_K·ζ(2) at K=2M: 0.976; mean across K: 0.989 ± 0.018

### COPY-PASTE PYTHON BLOCK (use in every NDC computation task):
```python
import mpmath
mpmath.mp.dps = 40

def chi_m4(p):
    r = p % 4
    return mpmath.mpc(1) if r==1 else (mpmath.mpc(-1) if r==3 else mpmath.mpc(0))

dl5 = {1:0, 2:1, 4:2, 3:3}
def chi5_complex(p):
    r = p % 5
    return mpmath.mpc(0) if r==0 else mpmath.power(mpmath.mpc(0,1), dl5[r])

dl11 = {1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9}
def chi11_complex(p):
    r = p % 11
    return mpmath.mpc(0) if r==0 else mpmath.exp(2*mpmath.pi*mpmath.mpc(0,1)*dl11[r]/10)

# Verified zeros:
rho_m4_z1 = mpmath.mpc(0.5, 6.020948904697597)
rho_m4_z2 = mpmath.mpc(0.5, 10.243770304166555)
rho_chi5  = mpmath.mpc(0.5, 6.183578195450854)
rho_chi11 = mpmath.mpc(0.5, 3.547041091719450)
```

### NDC ACTUAL DATA (real computation, K=10K to 2M):
| Case | |A_K| (stable) | |B_K|·ζ(2) (stable) | D_K·ζ(2) mean |
|------|-------------|----------------|---------------|
| chi_m4_z1 | ~0.52 | ~1.87 | 0.976 ± 0.011 |
| chi_m4_z2 | ~0.66 | ~1.51 | 1.011 ± 0.017 |
| chi5_z1   | ~0.56 | ~1.75 | 0.992 ± 0.024 |
| chi11_z1  | ~0.77 | ~1.29 | 0.989 ± 0.018 |
Grand mean D_K·ζ(2) = 0.992 ± 0.018 (24 data points, all K up to 2M).
NOTE: A_K and B_K are individually messy (character-specific). Only their PRODUCT D_K is universal.
Full data: ~/Desktop/Farey-Local/experiments/AK_BK_REAL_NUMERICAL.md

## VERIFIED L-FUNCTION ZEROS (LMFDB, verified 2026-04-14, |L(rho)| < 1e-28)
### χ₋₄ (mod 4, primitive, real)
t1 = 6.02094890469759665490251152161
t2 = 10.2437703041665545521377574791
t3 = 12.98809801231242250745310978956
t4 = 16.34260710458722219497686148345
t5 = 18.29199319612353483852600427759
### χ₃ (mod 3, primitive, real)
t1 = 8.03973715568146668171362321417
t2 = 11.24920620777293524970502567886
t3 = 15.70461917672162556516555088043
t4 = 18.26199749569312756892441409359
t5 = 20.45577080774249285344502583131

## ZERO VERIFICATION RULE (added 2026-04-14 after wrong-zero incident)
BEFORE using any L-function zero t in computation:
1. Source MUST be LMFDB (https://lmfdb.org) or equivalent database — NEVER a model's estimate
2. Run: python3 ~/bin/verify_zero.py → must show |L(1/2+it)| < 1e-5
3. Wrong zeros cause: (a) E_K*logK ratio off by 5-9%, (b) D_K not converging, (c) wild oscillations
PAST ERROR: χ₃ zero2 was 12.1734 (WRONG, fabricated); correct is 11.24921. χ₋₄ zero2 was 10.2437478 (off by 2e-5); correct is 10.2437703.
CHARACTER MISMATCH ERROR (2026-04-15): chi5_Legendre (p%5 in{1,4}→+1) used instead of chi5_complex (order-4). chi11_Legendre (Jacobi) used instead of chi11_complex (order-10). Both wrong — wasted overnight compute + fabricated email data. FIX: ALWAYS use the canonical Python block above.
Verification tool: ~/bin/verify_zero.py

## 2026-04-16 UPDATES (Session 11 — Koyama Reply)

### T_inf Definitive Values (Hurwitz zeta, 50-digit — CANONICAL)
- T_inf(chi_0, rho_1): -0.17036 (from Im(log zeta(1+28.269i))/2 = -0.34071/2)
- T_inf(chi_m4, rho_m4): -0.07909 (from Im(log L(1+12.042i, chi_m4^2))/2)
- T_inf(chi_5, rho_chi5): +0.43654 (Hurwitz zeta 50-digit — DEFINITIVE)
  WRONG (do NOT use): +0.43706 (Euler product at K=10000, not converged, discrepancy 0.001)
- B_K errors (|B_K - 2*T_inf| at K=500): chi_0=0.004, chi_m4=0.015, chi_5=0.0012

### NDC GL(2) — 37a1 Status: INCONCLUSIVE
- Cesaro mean of |D_K^E*zeta(2)| at K=200: 0.45 (was 1.72 at K=50, trending DOWN toward 0, not 1)
- Near-zero Euler factor at p=359: |factor|=1.92e-3, inverse spikes 521x, drives 8 OOM oscillation
- Re(c_K^E)/log K: negative throughout for K<=2000 (wrong sign for NDC convergence)
- Exception at K=1000: Re(c_K)/log K = +3.18 (within 2.6% of target 1/L'(E,1)=3.268) — likely coincidental given K=500 was -0.91
- BLOCKED: need correct Koyama c_K^E definition (questions sent to Koyama 2026-04-16)

### deepseek-r1:32b on M1 Max — BROKEN for complex tasks
- Success rate 2026-04-16: 0/4 (all timed out at 90 min with 0 bytes)
- Failed: EDRH_COUPLING, B_INF_UNIVERSALITY, COUNTEREXAMPLE_PRIME_VERIFY, P2_FOURTERM
- Only qwen3.5:35b producing output on M1 Max today
- Action: route future deepseek tasks to Codex API or simplify prompts

### C formula denominator: ζ(2) vs e^γ
- Aoki-Koyama framework: C = |L'(ρ,χ)|/ζ(2) (our formula, K=10000-20000 at 88-93%)
- Codex suggested e^γ citing Sheth 2025 (central zeros at s=1/2) — different context
- C = √2*|L'|/e^γ (Codex for principal χ²): RULED OUT (data at 67%, implausible at K=20K)
- Cannot distinguish ζ(2) vs e^γ (without √2) from current K≤20000 data; need K~10^5

### Koyama Correspondence Status
- Apr 16 reply received: EDRH+T_inf "truly ground-breaking"; C(rho,chi) new result
- Questions sent: exact c_K^E definition, role of Lambda(s,E) vs L(s,E), conductor/period normalization
- Awaiting Koyama's GL(2) formula before proceeding with EC computation
