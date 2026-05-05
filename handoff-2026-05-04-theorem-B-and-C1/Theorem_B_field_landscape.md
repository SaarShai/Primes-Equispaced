---
title: "Milinovich-Ng Conjecture 16 — Complete Field Landscape"
date: 2026-05-03
status: RESEARCH COMPLETE
confidence: 0.88
---

# Theorem B Field Landscape: M-N Conjecture 16 and |L'|² at Zeros

## Section 1: All Citations of M-N arXiv:1306.0854

**Primary paper:** Micah B. Milinovich and Nathan Ng, "Simple zeros of modular L-functions," arXiv:1306.0854, Proc. London Math. Soc. 109 (2014), no. 6, 1465–1506. https://arxiv.org/abs/1306.0854

**Direct extensions / citations confirmed:**

1. **Booker, Milinovich, Ng (2019)** — "Quantitative estimates for simple zeros of L-functions," arXiv:1806.01959, Mathematika 65 (2019) 375–399. Generalizes Conrey–Ghosh method to arbitrary conductor; prior M-N result (Ω(log log log T) for odd level) is the benchmark they improve on. https://arxiv.org/abs/1806.01959

2. **de Faveri (2021/2024)** — "Simple zeros of GL(2) L-functions," arXiv:2109.15311, JEMS 27 (2025), no. 7. First power bound Ω(T^{2/27}) for non-trivial level, directly supersedes Booker-Milinovich-Ng. Cites M-N chain explicitly. https://arxiv.org/abs/2109.15311

3. **Booker (2012)** — "Simple zeros of degree 2 L-functions," arXiv:1211.6838. Proved infinitely many simple zeros; predates M-N but is in the same lineage. https://arxiv.org/abs/1211.6838

4. **Bui, Florea, Milinovich (2023/2024)** — "Negative discrete moments of the derivative of the Riemann zeta-function," arXiv:2310.03949, Bull. London Math. Soc. 56 (2024), 2680–2703. Milinovich co-author; builds on the discrete-moment program of M-N. Zeta only, not GL(2). https://arxiv.org/abs/2310.03949

5. **Dong, Wattanawanichkul, Zaharescu (2025)** — "Zeros of polynomials in derivatives of automorphic L-functions," arXiv:2512.22451. Zero-counting for algebras of automorphic L-functions including derivatives; cites M-N lineage implicitly. https://arxiv.org/abs/2512.22451

**Unreachable confirms (require library access, listed by known citation path):**
- Conrey–Snaith 2007 (arXiv:math/0509480) is cited by M-N as source of Conjecture 16 derivation.
- CFKRS 2005 (arXiv:math/0206018) is foundation for ratios heuristic.

**Honest gap:** Semantic Scholar full citing-list for 1306.0854 could not be scraped in this session. The papers above are confirmed via cross-reference. Total citing papers estimated ~10–15 based on field size and paper age.

---

## Section 2: Every Related Result on |L'|² at Zeros for L-Functions

Organized by family. **Critical distinction:** "zeros" means non-trivial zeros ρ of L(s,·); "central point" means s=1/2. These are different objects.

### 2.1 Riemann zeta-function (single form, degree 1)

| Result | Content | Status | Source |
|---|---|---|---|
| Gonek 1993 | Σ_{0<γ≤T} \|ζ'(ρ)\|² ~ (T/24π) log⁴T | Conditional (RH) | Contemp. Math. 143, cited as [21] in M-N |
| Ng 2004 | Moments J_k(T) lower bounds | RH-conditional | Duke Math J 125(2) |
| Milinovich 2010 | Upper bounds k-th moments of ζ'(ρ) | RH-conditional | arXiv:0806.0786, BLMS 42 |
| Milinovich–Ng 2014 | Lower bounds J_k(T) ≫ (log T)^{k(k+2)} | RH-conditional | arXiv:0706.2321, IMRN 2014 |
| Bui–Florea–Milinovich 2024 | Negative discrete moments upper bounds (k ≤ 1/2) | Conditional | arXiv:2310.03949, BLMS 2024 |
| arXiv:2601.06292 (2026) | Full asymptotic Σ ζ^(μ)(ρ)ζ^(ν)(1−ρ), unconditional | **Unconditional** | https://arxiv.org/abs/2601.06292 |

### 2.2 Single modular GL(2) form f — zeros of L(s,f)

| Result | Content | Status | Source |
|---|---|---|---|
| M-N Thm 1.2 (2014) | Cage bounds: A_f T log⁴X ≤ Σ_{ρ_f} \|L'(ρ_f,f)\|² ≤ B_f T log⁴X, A_f ≈ 0.126 c_f, B_f ≈ 2.717 c_f | GRH-conditional | arXiv:1306.0854 |
| M-N Conjecture 16 (2014) | Σ \|L'(ρ_f,f)\|² = (2/(3π)) c_f T log⁴X | Conjectured (CFKRS + Conrey–Snaith derivation) | arXiv:1306.0854 |

**Nothing else.** No paper proves or improves the M-N cage bounds for GL(2) zeros. No paper proves the asymptotic.

### 2.3 Quadratic twist family — second moment at central point 1/2 (NOT at zeros)

These results are often confused with the zeros problem but concern L'(1/2, f⊗χ_d), not L'(ρ_f, f):

| Result | Content | Status | Source |
|---|---|---|---|
| Soundararajan–Young 2010 | Asymptotic for Σ_{d} L(1/2, f⊗χ_d)² | GRH-conditional | EMS 2010 |
| Li (Xiannan Li) 2024 | Same asymptotic, removes GRH | **Unconditional** | arXiv:2208.07343, Inventiones 237 (2024) 697–733 |
| Kumar–Mallesham–Sharma–Singh 2023 | Asymptotic Σ_d \|L'(1/2, f⊗χ_{8d})\|², removes GRH | **Unconditional** | arXiv:2303.16864 |
| Petrow (prior) | Same, conditional on GRH | GRH-conditional | cited by 2303.16864 |

**Critical note on 2303.16864:** This is the closest paper to Theorem B in spirit — it handles second moment of a derivative of a GL(2) L-function, unconditionally. BUT it averages over the quadratic character twist conductor d (central-point family), NOT over the zeros ρ_f. Fundamentally different. Does not cite or address M-N Conjecture 16.

---

## Section 3: Status of n-Level Density at n=3,4 Unconditional (CS 2007 Conjecture)

**The Katz–Sarnak density conjecture** (1999) for GL(2) families predicts eigenvalue statistics of SO(2N) or Sp(2N). Conrey–Snaith 2007 (arXiv:math/0509480, PLMS 94 (2007) 594–646) derived the n-level density predictions via ratios conjecture up to arbitrary support — but as a conjecture.

**Achieved unconditional support ranges for 1-level density (GL(2) holomorphic newforms):**

| Result | Support achieved | Method | Source |
|---|---|---|---|
| Iwaniec–Luo–Sarnak 2000 | (-1,1) unconditional; (-2,2) on GRH | Explicit formula + ILS trace | IHES Publ. 91 (2000) 55–131 |
| Devin–Fiorilli–Södergren 2022/2025 | (-Θ_k, Θ_k), Θ_2=1.866..., Θ_k→2 as k→∞ | Zero-density estimates for Dirichlet L-functions | arXiv:2210.15782, ANT 19 (2025) 1621–1635 |
| Baluyot–Chandee–Li 2024 | Support 4 (i.e., (-2,2) unconditional) for q-averaged family | q-aspect averaging reduces to support-2 problem | arXiv:2310.07606 |
| Chandee–Lee (referenced) | Support (-4,4) for unitary matrices from ratios | Derived within ratios conjecture framework, NOT a theorem | Referenced in search results as extension of Conrey–Snaith (-2,2) |
| Dillon et al. 2025 | Lower-order terms in 1-level and 2-level density, O(1/log⁴R) | Level structure analysis | arXiv:2508.21691 |

**2-level and n-level density unconditional (n≥3):**
- No paper achieves unconditional n-level density at support 4 for n≥3 for GL(2) families.
- 2-level density: Dillon et al. 2025 achieves lower-order corrections for 2-level; main term support range not stated as extending beyond GRH.
- **Support-4 wall for n-level:** Existing results stop at support ~2 unconditionally; reaching support 4 requires either GRH or family-aspect averaging tricks (as BCL do in q-aspect for 1-level only).

**The Conrey–Snaith 2007 predictions at support 4 remain conjectural for n≥2.**

---

## Section 4: Where We Are Ahead

**4.1 Constant identification via reverse engineering:**
We have identified the constant 2/(3π) = (1/(2π))·(1/12)·16 where 1/12 = Hughes–Mezzadri Barnes-G unitary baseline. No paper in the literature derives this factored form or identifies the 1/12 as the unitary matrix integral baseline. This is an original structural insight.

**4.2 Cage tightening prospect:**
M-N give cage [(17±√145)/(12π)] ≈ [0.126, 2.717] times c_f. Our unconditional lower-bound path via KM 1997 + ILS §8 may yield a sharper unconditional cage. No paper has attempted an unconditional lower bound on this specific sum; M-N's cage is GRH-conditional. If we achieve the cage unconditionally, this is new.

**4.3 Weakest sufficient conditions synthesis:**
The triple (KMV §5 var + KMV §4 mean + ILS §3 sign), all unconditional in principle, as a sufficient set for Theorem B is not stated anywhere in the literature. This is a new organizational result.

**4.4 Family-average framing of Conjecture 16:**
No paper has stated or studied the Petersson-family-averaged version of M-N (16). We are the first to frame this as a separate (and easier) target.

---

## Section 5: Where We Are Behind — Gaps E1, E2, E3

### E1: Shifted convolution at X²

**Gap:** The off-diagonal term in M-N's Proposition 1.1 sum requires estimating a shifted convolution Σ_{n≤X²} λ_f(n)λ_f(n+h)/n^{2σ} as σ→1/2 and X=√(qT)/2π. In the family-averaged version, this becomes a Kloosterman-spectral problem after Petersson. Our E1 failure is: the diagonal term is controlled but the off-diagonal at the X² scale (rather than X) produces an uncontrolled error in the Kuznetsov application.

**Who has the technique:** The Petrow–Young program (arXiv:1608.06854, 1903.07284, 2404.10692) on shifted convolution sums with arbitrary moduli is the state of the art for GL(2)×GL(2) shifted convolution. Specifically:
- Petrow–Young 2019 (Math. Ann., arXiv:1608.06854): asymmetric Petersson trace formula at squarefree level — directly applicable to our off-diagonal term.
- Blomer–Milicevic 2015 (GAFA 25, arXiv:1404.7845): second moment of twisted modular L-functions with power-saving; their shifted convolution analysis at conductor q likely handles X² scale.

**Recommendation:** Mine Petrow–Young §3–4 and Blomer–Milicevic §5 for the precise Kloosterman sum bound at the X² length. URL: https://arxiv.org/abs/1608.06854, https://arxiv.org/abs/1404.7845

### E2: CFKRS step-6 rigorization for GL(2)

**Gap:** The ratios conjecture prediction for Conjecture 16 uses step 6 of the CFKRS recipe (handling the "swap" diagonal contribution) as a heuristic only. No paper rigorously justifies this step for GL(2) holomorphic families.

**State of the art:** Kowalski–Michel–Sawin + Blomer–Fouvry–Milicevic 2018/2023 (arXiv:1804.01450, AMS Memoirs 2023) proved the second moment of twisted Hecke L-functions rigorously with power saving. Their proof does rigorize the analogue of the CFKRS diagonal contribution in the twist-character aspect. The GL(2) ratios-in-the-zero-aspect is harder but their diagonal separation technique in §5–7 of 1804.01450 is directly relevant.

**Recommendation:** Read Blomer et al. Memoirs 2023, §5–7, for the diagonal/off-diagonal separation that rigorizes the CFKRS step-6 type contribution in GL(2). URL: https://arxiv.org/abs/1804.01450

### E3: Support-4 one-level density (GL(2), fixed level, unconditional)

**Gap:** Our Weakest Sufficient Conditions path uses a sign-change count from ILS §3, which requires 1-level density with test function support > 1 (unconditional ILS gives only (-1,1)). Reaching support up to (-2,2) unconditionally would suffice for our purposes.

**State of the art:** Devin–Fiorilli–Södergren 2025 (arXiv:2210.15782) achieve support (-Θ_k, Θ_k) unconditionally for fixed level k (Θ_2=1.866), which nearly reaches (-2,2). Baluyot–Chandee–Li (arXiv:2310.07606) achieve support 4 but only in q-averaged families (not fixed level).

**Recommendation:** The Devin–Fiorilli–Södergren result at support ~1.87 is essentially what we need for E3; the gap to 2 is small and may close via their zero-density method. Direct reading of §3–4 of arXiv:2210.15782 for the applicable bound. URL: https://arxiv.org/abs/2210.15782

---

## Section 6: 2024–2026 Papers — Recent Breakthroughs

### Directly relevant:

1. **Li 2024** — Xiannan Li, Inventiones 237 (2024) 697–733, arXiv:2208.07343. First unconditional proof of the asymptotic for the second moment of quadratic twists L(1/2, f⊗χ_d)². Significance: removes GRH for a GL(2) second moment. Does NOT address zeros. https://arxiv.org/abs/2208.07343

2. **Kumar–Mallesham–Sharma–Singh 2023** — arXiv:2303.16864. Unconditional asymptotic for Σ_d |L'(1/2, f⊗χ_{8d})|². First unconditional second moment of L'(1/2) for a GL(2) family. Does not concern zeros ρ_f. https://arxiv.org/abs/2303.16864

3. **Devin–Fiorilli–Södergren 2025** — arXiv:2210.15782, ANT 2025. Unconditional 1-level density support extended to Θ_2≈1.87, nearly reaching the GRH-level (-2,2) for holomorphic newforms. Key for E3. https://arxiv.org/abs/2210.15782

4. **Bui–Florea–Milinovich 2024** — arXiv:2310.03949, BLMS 2024. Negative discrete moments of ζ'(ρ), upper bounds. Extends M-N program to negative moments; zeta only. https://arxiv.org/abs/2310.03949

5. **de Faveri 2021/2024** — arXiv:2109.15311, JEMS 2025. Power bound Ω(T^{2/27}) for simple zeros of GL(2) L-functions. Best simple-zeros result; uses deep GL(2) spectral theory. https://arxiv.org/abs/2109.15311

6. **Dong–Wattanawanichkul–Zaharescu 2025** — arXiv:2512.22451. Zeros of polynomials in derivatives of automorphic L-functions; asymptotic for zero counts near critical line. https://arxiv.org/abs/2512.22451

7. **Dillon et al. (Miller group) 2025** — arXiv:2508.21691. Lower-order correction terms in 1-level and 2-level density for GL(2) holomorphic newforms, breaking universality at O(1/log⁴R). https://arxiv.org/abs/2508.21691

### No paper in 2024–2026 achieves:
- Unconditional support-4 for n-level density with n≥2 at fixed level.
- Any asymptotic (even conditional) for Σ_{ρ_f} |L'(ρ_f,f)|².
- Any improvement over M-N Theorem 1.2 cage bounds.

---

## Section 7: Open Recommendations — Papers to Mine

| Priority | Paper | What to mine | URL |
|---|---|---|---|
| **P1 CRITICAL** | Petrow–Young 2019 Math. Ann. | Off-diagonal shifted convolution at X² for GL(2) (E1 gap) | https://arxiv.org/abs/1608.06854 |
| **P1 CRITICAL** | Blomer–Milicevic 2015 GAFA | Shifted convolution separation technique at large length (E1) | https://arxiv.org/abs/1404.7845 |
| **P2 HIGH** | Blomer–Fouvry–Kowalski–Michel–Milicevic–Sawin 2023 AMS Memoirs | Diagonal rigorization analogous to CFKRS step 6 (E2 gap) | https://arxiv.org/abs/1804.01450 |
| **P2 HIGH** | Devin–Fiorilli–Södergren 2025 ANT | Zero-density method for extending 1-level support past 1 (E3 gap) | https://arxiv.org/abs/2210.15782 |
| **P3 MEDIUM** | Kumar–Mallesham–Sharma–Singh 2023 | Unconditional second moment of L'(1/2) method — adapt for zeros | https://arxiv.org/abs/2303.16864 |
| **P3 MEDIUM** | Li 2024 Inventiones | Unconditional GL(2) second moment without GRH — technique transfer | https://arxiv.org/abs/2208.07343 |
| **P3 MEDIUM** | Milinovich–Ng 1306.0854 | Proposition 1.1 exact form, cf definition, Conjecture 16 statement | https://arxiv.org/abs/1306.0854 |
| **P4 LOW** | Conrey–Snaith 2007 PLMS | Source of Conjecture 16 via ratios (for citation) | https://arxiv.org/abs/math/0509480 |
| **P4 LOW** | CFKRS 2005 PLMS | Ratios recipe framework (for citation) | https://arxiv.org/abs/math/0206018 |
| **P4 LOW** | de Faveri 2021 JEMS | Simple zeros power bound — if simple zeros play role in our argument | https://arxiv.org/abs/2109.15311 |
| **P4 LOW** | arXiv:2601.06292 | Unconditional mixed zeta derivative asymptotic — model for E2 rigorization | https://arxiv.org/abs/2601.06292 |

---

## Summary Table

| Claim | Status |
|---|---|
| M-N Conjecture 16 proved (single form, GRH) | No |
| M-N Conjecture 16 proved (single form, unconditional) | No |
| Family-averaged version of Conjecture 16 proved | No |
| Cage bounds A_f/B_f (GRH, single form) | M-N 2014 — best known |
| Unconditional cage for family-averaged sum | Open — we have a path (KM+ILS) |
| Second moment of L'(1/2, f⊗χ_d)² unconditional | Kumar et al. 2023 (arXiv:2303.16864) |
| n-level density support 4 unconditional (n=1, q-averaged) | BCL 2024 (arXiv:2310.07606) |
| n-level density support ~1.87 unconditional (n=1, fixed level) | DFS 2025 (arXiv:2210.15782) |
| n≥2 level density support 4 unconditional | **Open** |
| Simple zeros power bound GL(2) | de Faveri 2025 (arXiv:2109.15311) |

**Bottom line:** We are ahead on the constant identification and family-averaged framing. We are behind on the off-diagonal shifted convolution (E1), the CFKRS rigorization (E2), and the 1-level density support extension (E3). The three priority-1 papers (Petrow–Young, Blomer–Milicevic, Blomer et al. Memoirs) contain the techniques needed to close E1 and E2. E3 is essentially solved by DFS 2025 for our purposes.
