# Prism Independent Verification + Continuation Packet
## Date: 2026-03-30
## Purpose: Single-file researcher handoff (Task 1 completed, Task 2 continued)

## 1) Executive Summary
- I independently audited the current proof chain against the project’s canonical status documents.
- I reconciled manuscript claims to remove/clarify overstatements and align with the documented proof status.
- I compiled the paper successfully after edits.
- I then continued directly to Task 2 and computed exact alpha-decomposition diagnostics for all primes with `M(p) = -3` up to `p = 431`.
- Main Task-2 finding: the residual ratio `r_actual` stays below `1` in tested data, but the Cauchy-Schwarz-only bound is far too weak; also the claimed `alpha ~ N/log N` scaling is not supported by direct computation under the current alpha definition.

---

## 2) Sources Reviewed
- `uploads/PRISM_HANDOFF.md`
- `experiments/CANONICAL_PROOF_STATUS.md`
- `experiments/ELMARRAKI_CORRECTION.md`
- `experiments/ADVERSARIAL_ELMARRAKI.md`
- `experiments/B_EXACT_AUDIT.md`
- `paper/main_new.tex`

---

## 3) Independent Status Assessment

### 3.1 Solid and consistent
- Four-term decomposition and displacement-shift identity are algebraically consistent.
- Bridge identity and permutation square-sum identity are consistent with supporting docs.
- Finite computational Sign result is clear and consistent: all `4,617` primes with `p <= 10^5`, `M(p) <= -3` satisfy `Delta W(p) < 0`.
- Threshold-optimality counterexample `p = 92,173` (`M(p) = -2`, `Delta W(p) > 0`) is consistent across docs.

### 3.2 Overclaim mismatches found (before edits)
- `D/A = 1 + O(1/log p)` was presented as proved theorem while canonical status marks this unresolved analytically.
- `B >= 0` was described as sole gap, while canonical status identifies both `B >= 0` and non-circular `D/A -> 1` as open tail gaps.
- Triangular-section status wording used “fully unconditional” language despite canonical caveat on one writeup-level large-sieve step.

---

## 4) Manuscript Contributions Completed
Updated `paper/main_new.tex` to align with canonical proof status.

### 4.1 Sign-Theorem status reconciliation
- Recast tail claim as a **conditional implication** rather than a completed analytical theorem.
- Replaced near-cancellation theorem status with:
  - empirical observation in tested range,
  - explicit asymptotic conjecture.
- Clarified that tail currently depends on computational inputs (`B >= 0`, empirical `D/A ≈ 1`).

### 4.2 Scope/claim hygiene
- Abstract/introduction language now distinguishes computationally proven range from conditional tail logic.
- Open Questions now list two key tail gaps explicitly:
  1) analytic proof of `B >= 0`,
  2) non-circular analytic proof of `D/A -> 1`.
- Triangular status sentence softened to avoid overclaim.
- Reproducibility line adjusted to avoid implying all scripts are present in this snapshot.

### 4.3 Relevant modified regions (for quick review)
- `paper/main_new.tex:51`
- `paper/main_new.tex:182`
- `paper/main_new.tex:400`
- `paper/main_new.tex:617`
- `paper/main_new.tex:684`
- `paper/main_new.tex:829`
- `paper/main_new.tex:1040`
- `paper/main_new.tex:1573`

---

## 5) Validation
Build command run in `paper/`:
- `pdflatex -interaction=nonstopmode -halt-on-error main_new.tex` (twice)

Result:
- Compile succeeds.
- No fatal errors.
- Remaining messages are non-blocking warnings (overfull boxes, existing hyperref token warning).

---

## 6) Task 2 Continuation (performed immediately)

## 6.1 Computation performed
I computed the alpha-decomposition quantities directly from Farey data (exact rational arithmetic via Python `fractions`) for all primes with `M(p) = -3` up to `p = 431`:

Primes tested:
- `13, 19, 43, 47, 53, 71, 107, 131, 173, 179, 271, 311, 379, 389, 431`

Computed per prime:
- `alpha = (sum D(f)(f-1/2)) / (sum (f-1/2)^2)`
- `C' = sum delta(f)^2` (interior: denominator `>1`)
- `||D_err||^2` where `D_err = D - alpha(f-1/2)`
- `corr = corr(D_err, delta)`
- `r_actual = |2 sum D_err delta| / (alpha (C'+1))`
- `r_CS = 2 ||D_err|| sqrt(C') / (alpha (C'+1))`

## 6.2 Results table
`p,N,n,alpha,Cprime,Derr2,corr,r_actual,r_CS,alpha_log_over_N`
- `13,12,47,1.812051069,5.870995671,28.549805855,-0.383676344,0.797925548,2.079683984,0.375231479`
- `19,18,103,2.515858121,12.859392079,116.609326871,-0.362616492,0.805423106,2.221143062,0.403986959`
- `43,42,543,3.951021591,82.794939490,2130.817124963,-0.256012193,0.649588662,2.537334864,0.351609842`
- `47,46,651,4.031971294,87.396811888,2947.417360392,-0.212691962,0.605753113,2.848030107,0.335586352`
- `53,52,831,4.139734248,121.173459905,4520.880372332,-0.224290593,0.656458056,2.926819381,0.314559595`
- `71,70,1495,4.578181352,217.163281924,11894.379388379,-0.186487701,0.600163574,3.218247473,0.277862596`
- `107,106,3427,5.784066504,508.391382172,46849.547314610,-0.150868259,0.499798321,3.312812941,0.254468319`
- `131,130,5155,5.809719879,806.646942696,93755.252441404,-0.141566352,0.524750473,3.706745757,0.217530859`
- `173,172,9023,6.627320862,1436.921163199,227120.310237331,-0.124950339,0.473738651,3.791415485,0.198337776`
- `179,178,9655,6.599243880,1468.730296305,252788.145411637,-0.120099263,0.477186218,3.973265161,0.192111536`
- `271,270,22205,7.476705929,3644.774692705,955567.198621869,-0.107772621,0.466663974,4.330079105,0.155028721`
- `311,310,29231,7.411365921,4694.399508942,1457633.937664630,-0.094332971,0.448473679,4.754156219,0.137147859`
- `379,378,43467,8.137723266,7121.261372253,2702536.082512509,-0.088623418,0.424250031,4.787109756,0.127768589`
- `389,388,45817,8.819889216,7396.775729667,2941650.218328347,-0.087236497,0.394439738,4.521499065,0.135503626`
- `431,430,56211,7.332913062,9061.605823146,4090980.468056137,-0.082552265,0.478349858,5.794509177,0.103407465`

## 6.3 Immediate implications
1. **Residual ratio passes empirically** in tested set:
   - `r_actual < 1` for every tested `M(p) = -3` prime (max in this table ≈ `0.8054`).

2. **Pure Cauchy-Schwarz bound is unusable** for closure:
   - `r_CS` is between ~`2.08` and `5.79` (>1 everywhere), so CS alone cannot prove positivity.

3. **Decorrelation is visible**:
   - `corr(D_err, delta)` is negative and magnitude decreases from about `0.38` to `0.08` across this range.

4. **Alpha-scaling warning (important)**:
   - Under the current stated definition of `alpha`, data does **not** support `alpha ~ N/log N`.
   - Observed scale is much smaller (roughly logarithmic-size over this range), as shown by the `alpha_log_over_N = alpha*log(N)/N` column trending downward.
   - This is a potential structural issue in the current El-Marraki Part-II argument and likely indicates either:
     - a normalization mismatch in the derivation, or
     - a genuinely incorrect scaling claim.

---

## 7) Practical Researcher Action Items
1. **Check alpha normalization in `ELMARRAKI_CORRECTION.md`** against exact computational definition used in Identity E.
2. **Avoid any proof step requiring CS-only residual control** (`r_CS` evidence rules it out numerically in tested range).
3. **Reframe Task-2 target** as explicit decorrelation bound + explicit norm bound with matched normalization.
4. Keep the current manuscript honesty framing until those two tail inputs are proved analytically.

---

## 8) Current Project State (after this pass)
- Manuscript now reflects honest hybrid/conditional status.
- Single-file packet exists (this file) for direct forwarding.
- Task 2 has new concrete diagnostic data and a narrowed bottleneck:
  - not raw size of `||D_err||` alone,
  - but proving a quantitatively strong correlation-decay bound with correct normalization.

## 9) Additional normalization check on the alpha-proof backbone
I also checked the specific scaling claim in `experiments/ELMARRAKI_CORRECTION.md` that
`-R/2 ~ pi(N)/12 ~ N/(12 log N)` where `R = sum f^2 - n/3`.

Using the stated `R` definition on full `F_N`, I get:

`p,N,n,alpha,R,R_over_n,n_over_logN`
- `13,12,47,1.429803670,-0.238353776,-0.005071357,18.914`
- `19,18,103,2.301546832,-0.380643363,-0.003695567,35.636`
- `43,42,543,3.895517864,-0.649196371,-0.001195573,145.278`
- `71,70,1495,4.555656411,-0.761005378,-0.000509034,351.889`
- `107,106,3427,5.772148735,-0.963528945,-0.000281158,734.865`
- `271,270,22205,7.474413899,-1.247036238,-0.000056160,3966.296`
- `431,430,56211,7.332023369,-1.223056299,-0.000021758,9269.952`

Interpretation:
- `R` stays around order `1` in magnitude (slowly varying), not order `N/log N`.
- Therefore the line “`-R/2 ~ pi(N)/12`” is not compatible with this `R` definition.
- This strongly suggests a normalization/notation mismatch in the current Part-II derivation, which must be resolved before any explicit-constant tail closure can be considered rigorous.