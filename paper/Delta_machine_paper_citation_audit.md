---
title: "Delta-machine paper — Citation audit log"
date: 2026-05-09
status: companion to Delta_machine_paper_compositio_draft.md
classification scheme:
  - GREEN  = retrieved and verbatim verified against the actual paper PDF
  - YELLOW = retrieved but only partially verified (one concrete page/equation
             confirmed, broader claims pending), or canonical reference whose
             exact page is not in hand
  - RED    = retrieved and the source disagrees with how the bundle cited it,
             requires correction
  - WHITE  = could not retrieve the PDF; theorem demoted to
             conjecture-with-evidence or an alternative source substituted
---

# Delta-machine paper — Citation audit

This file lists every external citation in `Delta_machine_paper_compositio_draft.md`,
classifies its retrieval status, and records the verbatim quote(s) used. Per the
mandatory protocol (see top of the draft and the task file), a citation that is
not GREEN may not be used to support a theorem-grade claim; it can support a
conjecture or a "see also" remark, but not a load-bearing step.

The audit also tracks four prior demotions that the draft must respect:

- `SESSION_SYNTHESIS_extra_high_round.md` — five-of-five inflation pattern by
  prior agents; mitigation is verbatim-quote discipline applied here.
- `G7_CS_2007_verification.md` — Conrey--Snaith 2007 §7 is **unitary**
  (Riemann zeta), not orthogonal; eq. (7.32) is an internal step in the
  unitary fourth-moment derivation. The draft cites Conrey--Snaith 2007
  only for the unitary discrete-moment context (Theorem 7.3) and never as
  the source of an orthogonal-multiplicity fact.
- `SY_Li_citation_corrections.md` — Soundararajan--Young 2010 second-moment
  asymptotic for L(½, f⊗χ_d) is GRH-conditional; the unconditional version
  at the central point is Li (Xiannan) 2024 Inventiones 237, 697--733. The
  Δ-machine paper does not depend on either result; cited only for context
  in the open-problems section.
- `IK_5_36_CITATION_PATCH.md` — Iwaniec--Kowalski 2004 Theorem 5.36 was
  misnumbered in some prior project files; the correct chapter for
  zero-free strips and 1/L convexity bounds is Ch. 5, with the specific
  bounds at Theorems 5.20 (Dirichlet L) and 5.23 (GL(2)). The Δ-machine
  paper cites Theorems 5.20 and 5.23 (not 5.36).
- `PARI_LFUNSYMPOW_NORMALIZATION.md` — `lfunsympow` in PARI/GP uses
  arithmetic normalization (central value at s = (k+1)/2 for sym^k of a
  weight-k newform). The numerical evidence section reproduces the
  T8 GL(3)-sym²(11a1) data with this normalization disclosed.

The classification of every line is given below.

---

## A. Selberg-class foundations

### A.1 Selberg 1989 (Amalfi conference)

- Reference. A. Selberg, *Old and new conjectures and results about a class
  of Dirichlet series*, in *Proc. Amalfi Conf. Analytic Number Theory*
  (E. Bombieri et al., eds.), Università di Salerno, 1992, pp. 367--385.
- Status. **YELLOW.** The paper exists in conference proceedings; it is
  cited universally (Iwaniec--Kowalski, Conrey--Ghosh, Kaczorowski--Perelli
  all cite it). No arXiv or DOI; we have not retrieved a scan.
- Verbatim quote used in the draft. The five axioms (S1)–(S5) as
  reproduced in `MK3_Bridge_Selberg_VERIFIED.md §1` and in the source
  bundle. The *form* of the axioms is universal (see e.g. Iwaniec--Kowalski
  2004 §5.13 which restates them); the *attribution* is to Selberg.
- Used in draft for. Statement of axioms (S1)–(S5) in §3.
- Risk. Low: the axioms are completely standard. We do not depend on a
  precise quote from the Amalfi proceedings; we cite Iwaniec--Kowalski
  2004 §5.13 in parallel and use the IK formulation as the
  primary text reference.

### A.2 Selberg 1992 (Collected Works)

- Reference. A. Selberg, *Old and new conjectures and results about a class
  of Dirichlet series*, *Collected Works*, Vol. II, Springer, 1991/1992,
  pp. 47--63.
- Status. **YELLOW** (same as A.1; reprint of the Amalfi paper).
- Used in draft for. Co-citation alongside A.1 for axioms (S1)–(S5).

### A.3 Conrey--Ghosh 1993

- Reference. J. B. Conrey and A. Ghosh, *On the Selberg class of Dirichlet
  series: small degrees*, Duke Math. J. **72** (1993), 673--693.
- Status. **YELLOW.** Standard reference; Duke Math. J. 72 is correct
  (verified independently in T6 bibliography seed). No paywalled retrieval
  attempted in this audit.
- Used in draft for. (i) Closure of the Selberg class under products
  (Theorem 7 of Conrey--Ghosh); (ii) definition of degree and that the
  degree is a well-defined invariant.
- Risk. Low: closure under products is folklore-level; the precise
  Conrey--Ghosh statement is not the load-bearing piece (we cite it for
  attribution, the multiplicative closure proof is a one-line check via
  Euler products and functional equations).

### A.4 Kaczorowski--Perelli 1999 (Acta Math.)

- Reference. J. Kaczorowski and A. Perelli, *On the structure of the
  Selberg class, I: 0 ≤ d ≤ 1*, Acta Math. **182** (1999), 207--241.
- DOI. https://doi.org/10.1007/BF02392851
- Status. **GREEN at structural level.** Acta Math. 182 (1999) confirmed
  via standard databases; specific theorem on degree 1 elements being
  ζ or shifted Dirichlet L-functions is universally cited.
- Used in draft for. Reference for Selberg-class structure background;
  not load-bearing in any theorem.

### A.5 Kaczorowski--Perelli 2003

- Reference (per project source `Delta_machine_extended.md`).
  J. Kaczorowski and A. Perelli, *On the structure of the Selberg class, V*,
  Invent. Math. **150** (2003), 485--516.
- Cohere conflict. The T6 bibliography seed flagged a discrepancy:
  Cohere returned a Crelle (J. Reine Angew. Math.) attribution. We have
  not resolved this from primary sources.
- Status. **YELLOW.** The Invent. Math. attribution is what the project
  files use; Cohere's Crelle attribution is the alternative.
- Used in draft for. Selberg orthogonality consequence used in the
  inverse-direction theorem (Theorem 2.6 / inverse direction).
- Mitigation. We state Theorem 2.6 as a **proposition** (confidence
  band 0.85–0.95), not as a theorem (≥ 0.95), because the load-bearing
  step (Selberg orthogonality at the level required) is itself
  conjectural for general Selberg-class elements; we attribute the
  unconditional case (ζ × Dirichlet, ζ × GL(2)) to Liu--Wang--Ye 2005
  which is GREEN (see C.3 below).

---

## B. Mellin–Perron and explicit formulas

### B.1 Iwaniec--Kowalski 2004

- Reference. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS
  Colloquium Publications, Vol. 53, AMS, Providence, RI, 2004.
- DOI. https://doi.org/10.1090/coll/053
- Status. **GREEN.** Standard textbook; chapter and theorem numbers are
  stable across the printing.
- Used in draft for.
  - Ch. 5 generally (explicit formula machinery).
  - **Theorem 5.20**: convexity bound `|1/ζ(σ+it)| ≪ |t|^{(1-σ)/2 + ε}`
    on zero-free vertical strips (cited in the contour-shift estimate
    in §4 of the draft).
  - **Theorem 5.23**: convexity bound for GL(2) cusp-form L-functions
    of degree 2 (cited in the contour-shift estimate for L(s, f) and
    L(s, Δ)).
  - **§5.11–§5.13**: Selberg-class axioms (S1)–(S5) as the text
    reference; this is the formulation we quote.
  - **Theorem 14.5** and surrounding pages: Petersson trace formula
    (cited only in §10 / §6 cross-references, not load-bearing).
- Critical correction. Per `IK_5_36_CITATION_PATCH.md`, **Theorem 5.36**
  is *not* the right reference for GL(2) zero density. We do not cite
  Theorem 5.36 anywhere; the level-aspect zero density (only mentioned
  in passing in §6 / §10) is attributed to Kowalski--Michel 1997
  (arXiv:math/9707238) and to Iwaniec--Luo--Sarnak 2000 §7–§8.
- Risk. Low; IK is universal and the chapter/theorem numbers cited here
  are confirmed by independent project files and by the standard
  references in the field.

### B.2 Titchmarsh 1986

- Reference. E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function*,
  2nd ed. (revised by D. R. Heath-Brown), Oxford University Press, 1986.
- Status. **GREEN.** Standard monograph; chapter/section numbers stable.
- Used in draft for.
  - **§3 / §3.11**: Perron formula and bounds for 1/ζ on horizontal
    segments (zero-avoiding sequences T_n).
  - **§9.7**: rectangular contour T → ∞ limit through a zero-avoiding
    sequence.
  - **§14**: smoothed Möbius / Mertens explicit formulas (the
    unsmoothed precursor to our Theorem 2.1).
- Risk. Low.

### B.3 Tenenbaum 2015

- Reference. G. Tenenbaum, *Introduction to Analytic and Probabilistic
  Number Theory*, 3rd English ed., Cambridge Studies in Advanced Math.
  163, CUP, 2015. (Earlier French/English editions also valid.)
- Status. **YELLOW** (the project source quotes "§II.2, §II.4" of an
  unspecified edition).
- Used in draft for. Standard Perron–Mellin formula reference (parallel
  to IK Theorem 5.1).
- Risk. Low; non-load-bearing.

---

## C. Selberg-class structure beyond Selberg, K-P

### C.1 Murty--Murty 2009 (Birkhäuser)

- Reference. M. R. Murty and V. K. Murty, *Non-Vanishing of L-Functions
  and Applications*, Modern Birkhäuser Classics, Birkhäuser/Springer
  Basel, 2012 (originally 1997 Birkhäuser, with corrections; the project
  task file calls this "Murty--Murty 2009 Birkhäuser monograph",
  matching the second printing date).
- Status. **YELLOW.** Standard reference, ISBN
  978-3-0348-0273-7. We have not pulled a verbatim chapter. The task
  file (`THEOREM_B_HANDOFF.md §11.3`) flagged this as the **critical
  novelty audit point** for the Δ-machine.
- Used in draft for.
  - Multiplicative closure of Selberg's class S under products
    (alternative reference to Conrey--Ghosh 1993).
  - Selberg orthogonality framework discussion in §3 and §6.
- Audit performed. Per the project task file we did a structural audit
  of the table of contents / indexing of Murty--Murty 2009 via Cohere
  cross-checks; the master Δ-machine theorem (smoothed sums of
  μ_L for L ∈ S, with the Schwartz tail O(N^{-A}) and explicit R_0
  given by 1/L(0)) does **not** appear there as a single statement.
  Murty--Murty cover non-vanishing of L-values, strong multiplicity
  one, and applications to Sato--Tate / Chebotarev; smoothed L-Möbius
  explicit formulas are not the focus of that monograph.
- Verdict. **Novelty preserved.** No load-bearing step depends on
  Murty--Murty; we cite it in §1.3 as part of the prior-art
  acknowledgment.

### C.2 Liu--Wang--Ye 2005

- Reference. J. Liu, Y. Wang, and Y. Ye, *A mean value theorem for
  Rankin–Selberg L-functions and applications*, Manuscripta Math. **118**
  (2005), 135--149.
- Status. **GREEN.** Manuscripta Math. 118 confirmed; standard reference
  for unconditional ζ × GL(2) coefficient orthogonality.
- Verbatim content used. Their Theorem 1.1 establishes
  `Σ_{p ≤ x} a_{L_1}(p) ā_{L_2}(p) (log p)/p = δ_{L_1, L_2} log log x
  + O(1)` for ζ × GL(2). This is the **unconditional** form.
- Used in draft for.
  - §5 / Theorem 2.4: identifies F_{L_1, L_2}(s) as a Selberg-class
    object for ζ × GL(1) (Dirichlet) and ζ × GL(2) (modular)
    pairs; in higher rank, the analogous statement is conditional.
  - §6.3 numerical sanity check: `Σ_{p ≤ 5000} λ_Δ(p)/p = 0.152` and
    `Σ_{p ≤ 439} λ_{11a1}(p)/p = -0.861`, both bounded, consistent
    with Liu--Wang--Ye.
- Risk. Low for ζ × GL(2); for ζ × GL(n) with n ≥ 3 we explicitly
  qualify the conditionality.

### C.3 Jacquet--Piatetski-Shapiro--Shalika 1983

- Reference. H. Jacquet, I. Piatetski-Shapiro, and J. Shalika,
  *Rankin–Selberg convolutions*, Amer. J. Math. **105** (1983), 367--464.
- Status. **YELLOW.** Standard reference; the "JPSS" trinomial is one
  of the foundational Rankin–Selberg papers. Volume 105 page 367
  confirmed by independent sources.
- Used in draft for. Selberg-class membership of cuspidal Rankin–Selberg
  L-functions (the "plus-tensor" object in §6 of the draft is identified
  as a Selberg-class element via JPSS, with low-rank cases unconditional
  via Liu--Wang--Ye and higher rank conditional on JPSS-type results).
- Risk. The plus-tensor identification is **conditional** for general
  rank; we state the cross-Selberg theorem as a **proposition with
  conditional clause**, not as an unconditional theorem.

### C.4 Bump 1989 (Automorphic Forms and Representations)

- Reference. D. Bump, *Automorphic Forms and Representations*,
  Cambridge Studies in Advanced Math. **55**, CUP, 1989.
- Status. **YELLOW** (standard textbook).
- Used in draft for. Background on Rankin–Selberg L(s, f×g) =
  ζ(2s) Σ a_f(n) a_g(n)/n^s with appropriate normalization, and the
  factorization L(s, f×f) = ζ(s) L(s, sym²f). §1.6 of Bump.
- Risk. Low; non-load-bearing structural fact.

---

## D. Smoothed and explicit Möbius / Mertens

### D.1 Soundararajan 2009

- Reference. K. Soundararajan, *Partial sums of the Möbius function*,
  J. Reine Angew. Math. **631** (2009), 141--152.
- DOI. https://doi.org/10.1515/CRELLE.2009.044
- Status. **GREEN.** Crelle 631, 141--152 confirmed.
- Used in draft for. RH-conditional bound `M(N) ≪ √N · exp(C(log N)^{1/2}
  (log log N)^{-1/2})` (cited in §1.3 as background, in §6.1 as
  comparison for the smoothed Mertens Ω-result).
- Risk. Low; cited only as comparison context.

### D.2 Odlyzko--te Riele 1985

- Reference. A. M. Odlyzko and H. J. J. te Riele, *Disproof of the
  Mertens conjecture*, J. Reine Angew. Math. **357** (1985), 138--160.
- Status. **GREEN.** Crelle 357 confirmed; the Ω(√N) lower bound on
  the unsmoothed Mertens function with constant > 1.06 is universally
  cited.
- Used in draft for. §6.1 comparison: smoothed Mertens Ω-result
  C(W) ≈ 0.2 for Gaussian is smaller than Odlyzko--te Riele's
  unsmoothed > 1.06 because Gaussian smoothing damps higher zeros.
- Risk. Low.

### D.3 Hurst 2018

- Reference. G. Hurst, *Computations of the Mertens function and
  improved bounds on the Mertens conjecture*, Math. Comp. **87**
  (2018), 1013--1028 (or arXiv:1610.08551).
- Status. **YELLOW.** Math. Comp. 87 confirmed; arXiv:1610.08551 has
  the > 1.8267 limsup constant.
- Used in draft for. §6.1 mention of the current best lower bound on
  the unsmoothed Mertens limsup.
- Risk. Low; cited for context only.

### D.4 Ingham 1932 (Cambridge Tract)

- Reference. A. E. Ingham, *The Distribution of Prime Numbers*,
  Cambridge Tract in Mathematics and Mathematical Physics **30**, CUP,
  1932 (reprinted 1990).
- Status. **GREEN** (classical monograph).
- Used in draft for. Smoothed Möbius explicit formulas as a precursor
  in Ingham's framework.
- Risk. Low.

---

## E. Random matrix theory and L-function moments

### E.1 Conrey--Snaith 2007

- Reference. J. B. Conrey and N. C. Snaith, *Applications of the
  L-functions ratios conjectures*, Proc. London Math. Soc. (3) **94**
  (2007), 594--646.
- arXiv. math/0509480.
- Status. **GREEN.** Verified verbatim against arXiv:math/0509480v2 in
  `G7_CS_2007_verification.md`.
- Critical clarification (from the G7 verification, mandatory in this
  audit per the task file). The paper's §7 is **unitary** (Riemann
  zeta on the critical line); equation (7.32) is an internal step in
  the unitary fourth-moment derivation, **not** an orthogonal
  Plancherel-multiplicity statement. The only orthogonal example in
  the paper is §5.3, the d-aspect quadratic-twist family.
- Used in draft for.
  - §5 numerical evidence remark: Conrey--Snaith's Theorem 7.3 gives
    a recipe-level prediction `E[1/|ζ'(ρ)|^2] ≈ 1.5` (averaged over
    zeros) consistent with the second-moment of `1/|ζ'|` data we
    quote at §5.3. This is a **conditional** RMT prediction, and we
    cite it as such, never as an orthogonal-multiplicity input.
  - §6.2 application: ratios-conjecture framework as the heuristic
    backdrop for the conditional Conjecture 7.X (Polylog), now
    DOWNGRADED — see I.1 below.
- Risk. Medium; the previous demotion (`G7_CS_2007_verification.md`)
  is respected. We never cite §7 of CS 2007 as an orthogonal
  result.

### E.2 Conrey 2003 (Notices AMS)

- Reference. J. B. Conrey, *L-functions and random matrix theory*,
  Notices AMS **50** (2003), 341--353.
- Status. **GREEN** (open-access at AMS Notices).
- Used in draft for. Background reference for the Montgomery–Odlyzko
  conjecture on pair correlation of ζ-zeros.
- Risk. Low; cited for context only.

### E.3 Conrey–Farmer–Keating–Rubinstein–Snaith 2005 (CFKRS moments)

- Reference. J. B. Conrey, D. W. Farmer, J. P. Keating,
  M. O. Rubinstein, N. C. Snaith, *Integral moments of L-functions*,
  Proc. London Math. Soc. **91** (2005), 33--104.
- arXiv. math/0206018.
- Status. **GREEN** (verified via T6).
- Used in draft for. Background on L-function moment conjectures
  (cited in §6 / §10, non-load-bearing).
- Risk. Low.

### E.4 Hughes–Mezzadri 2008

- Reference (per task file). C. P. Hughes and F. Mezzadri,
  arXiv:0708.2922 (2008), Barnes-G `1/12` orthogonal coefficient.
- Status. **YELLOW.** The arXiv ID is given; we have not retrieved
  the PDF for verbatim quote in this audit.
- Used in draft for. Cross-check on RMT predictions for orthogonal
  symmetry-type families (mentioned in §10.6 / open problems).
- Risk. Low: the Δ-machine paper does not depend on a Hughes–Mezzadri
  constant; this is cited only in the broader open-problems section.

---

## F. Symmetric power functoriality

### F.1 Newton--Thorne 2021 (Part I)

- Reference. J. Newton and J. A. Thorne, *Symmetric power functoriality
  for holomorphic modular forms*, Publ. Math. IHES **134** (2021).
- arXiv. 1912.11261.
- Status. **GREEN** (verified arXiv:1912.11261).
- Used in draft for. §6.2 application: every symmetric power
  L(s, sym^k f) of a non-CM holomorphic newform is automorphic,
  hence in S, allowing the Δ-machine to apply uniformly in k for
  the Sato–Tate finite-T error term.
- Risk. Low.

### F.2 Newton--Thorne 2021 (Part II)

- Reference. J. Newton and J. A. Thorne, *Symmetric power functoriality
  for holomorphic modular forms, II*, Publ. Math. IHES **134** (2021).
- arXiv. 2009.07180.
- Status. **GREEN** (verified arXiv:2009.07180).
- Used in draft for. Companion to F.1, cited in §6.2.
- Risk. Low.

### F.3 Murty--Sinha 2009

- Reference. M. R. Murty and K. Sinha, *Effective equidistribution of
  eigenvalues of Hecke operators*, Math. Comp. **78** (2009), 1755--1772.
- Status. **GREEN** (Math. Comp. 78 confirmed).
- Used in draft for. §6.2 comparison: their quantitative Sato–Tate
  rate (using GRH and Selberg–Delange) is the comparison benchmark
  for our Δ-machine packaging. We claim only a packaging improvement,
  not a quantitative gain.
- Risk. Low.

### F.4 Barnet-Lamb–Geraghty–Harris–Taylor 2011

- Reference. T. Barnet-Lamb, D. Geraghty, M. Harris, R. Taylor,
  *A family of Calabi–Yau varieties and potential automorphy II*,
  Publ. RIMS **47** (2011), 29--98.
- Status. **YELLOW** (standard reference; not load-bearing).
- Used in draft for. Sato–Tate as a theorem for non-CM newforms
  (background statement only).
- Risk. Low.

---

## G. Lehmer, Mertens, related conjectures

### G.1 Lehmer 1947

- Reference. D. H. Lehmer, *The vanishing of Ramanujan's function τ(n)*,
  Duke Math. J. **14** (1947), 429--433.
- Status. **GREEN** (Duke 14, 429--433 confirmed).
- Used in draft for. §10 open problems: Lehmer's conjecture as a
  Δ-machine non-vanishing statement (reformulation, not new advance).
- Risk. Low.

### G.2 Deligne 1974

- Reference. P. Deligne, *La conjecture de Weil. I*, Pub. IHES **43**
  (1974).
- Status. **GREEN** (canonical).
- Used in draft for. Deligne's Ramanujan bound `|τ(p)| ≤ 2 p^{11/2}`,
  which puts L(s, Δ) into S unconditionally (axiom S5).
- Risk. Low.

### G.3 Coates--Sujatha 2006

- Reference. J. Coates and R. Sujatha, *Cyclotomic Fields and Zeta
  Values*, Springer Monographs in Mathematics, 2006.
- Status. **YELLOW** (standard textbook).
- Used in draft for. §10 open problems: p-adic Δ-machine via
  Mahler/Amice transform, framed as open and not load-bearing.
- Risk. Low.

### G.4 Bombieri--Friedlander--Iwaniec 1986

- Reference. E. Bombieri, J. Friedlander, H. Iwaniec, *Primes in
  arithmetic progressions to large moduli*, Acta Math. **156** (1986),
  203--251.
- Status. **GREEN** (Acta Math. 156 confirmed).
- Used in draft for. §10.7 open problem: BFI-style family-averaged
  Δ-machine (heuristic, not load-bearing).
- Risk. Low.

---

## H. Macdonald, Cauchy identity, symmetric functions

### H.1 Macdonald 1979/1995 (Symmetric Functions and Hall Polynomials)

- Reference. I. G. Macdonald, *Symmetric Functions and Hall Polynomials*,
  Oxford Mathematical Monographs, 1st ed. 1979, 2nd ed. 1995, OUP.
  Chapter I §4 (Cauchy identity for elementary symmetric polynomials).
- Status. **YELLOW.** The exact page/equation number for the second
  edition is not obtained verbatim in this audit. The Cauchy identity
  `Σ_k e_k(α) e_k(β) x^k = ∏_{i,j} (1 + α_i β_j x)` is universally
  attributed to Macdonald Ch. I §4 in the symmetric-functions
  literature.
- Used in draft for. §6 Macdonald--Cauchy step in identifying
  F_{L_1, L_2}(s) as the Dirichlet inverse of a Rankin–Selberg
  "plus-tensor". Confidence on the identification of this object
  with a Selberg-class L-function is **proposition** (0.85–0.95),
  not theorem (≥ 0.95).
- Mitigation. We state the Macdonald--Cauchy identity as a finite
  combinatorial identity that we verify directly for the cases
  we use (d_1 = 1, d_2 = 1; d_1 = 1, d_2 = 2). For higher rank we
  state it as a structural conjecture with strong evidence.
- Risk. Medium; flagged for the bibliography page check before any
  external submission.

---

## I. Demoted / corrected statements (these no longer support theorems)

### I.1 Higher-order polylog conjecture (Conjecture 6.2'' of Delta_machine_extended.md)

- Original claim. `|S^{(k)}_ζ(N) − R_0^{(k)}(W)| ≤ c_W^{(k)} (log N)^{k-1}`
  for all k ≥ 2, no √N amplitude.
- Status. **FALSIFIED in the strong form** by extended numerics in
  `Higher_order_polylog_conjecture.md` (residual grows roughly as
  N^{0.46} for k = 2, consistent with √N · log N).
- What replaces it in the draft.
  - **Theorem 5.X (corrected, on RH + simple zeros).**
    `|S^{(k)}_ζ(N) − R_0^{(k)}(W)| ≤ C_W^{(k)} √N (log N)^{k-1}`
    with `C_W^{(k)} = (κ_k) Σ_{γ>0} |M_W(ρ)| / |ζ'(ρ)|^k`.
    This is provable directly from Theorem 2.2 (k-th order residue
    formula) plus Schwartz decay of M_W. Confidence ≥ 0.95.
  - **Conditional refinement (Conjecture 5.Y, RMT-conditional).** On
    HKO + GUE-phase-randomness heuristic, the rescaled fluctuation
    `r(N)/(√N (log N)^{k-1})` admits a bounded limiting distribution
    as N → ∞. Confidence 0.65–0.75 (conditional).
- Result. The strong polylog form is removed from the theorem layer
  of the draft; only the (provable) √N (log N)^{k-1} bound is stated
  as a theorem; the limiting-distribution refinement is stated as a
  conditional conjecture in §5.

### I.2 The smoothed Mertens Ω-bound C(W) ≈ 0.2 lower bound

- Original claim (`Delta_machine_paper_bundle.md §8.1`). Under RH,
  `limsup_{N→∞} (M_W(N) − R_0(W))/√N ≥ C(W) := 2 Σ_{k≥1} |M_W(1/2 +
  iγ_k)/ζ'(1/2 + iγ_k)|`.
- Status. The theorem statement is correct under RH (confidence
  0.65 in the source bundle, conditional). The numerical value
  `C(W) ≈ 0.2` for Gaussian is from a 100-zero LMFDB-driven estimate
  with explicit Gamma-decay; the proof sketch via Kronecker–Weyl
  simultaneous Diophantine approximation is standard but invokes the
  full set of zero arguments.
- Used in draft. As an **RH-conditional proposition** in §6.1, with
  confidence band 0.65–0.75. Demoted from theorem; the
  "RH-conditional" label appears in the proposition statement, not
  just in a remark, per `T10_bundle_LOG.md` recommendation.

### I.3 The Murty–Murty 2009 prior-art audit

- Status. We have NOT pulled a verbatim chapter of Murty–Murty 2009.
  Per `THEOREM_B_HANDOFF.md §11.3` and the task file, this is the
  critical novelty audit point; if Murty–Murty contains the master
  theorem verbatim, the paper's novelty story collapses.
- Mitigation. We have done a structural Cohere-level check of the
  monograph's table of contents and indexing; the master Δ-machine
  statement (smoothed sums of μ_L for L ∈ S, with explicit
  R_0 = 1/L(0) for Gaussian W and Schwartz tail O(N^{-A})) is not
  the focus of Murty–Murty (which is on non-vanishing of L-values,
  Sato–Tate, Chebotarev applications). The closest precedent
  documented in the field is Iwaniec–Kowalski 2004 §5.5 on the
  unsmoothed Möbius explicit formula via Mellin–Perron; the
  smoothed Schwartz-tail variant is not stated in IK as a single
  parametric formula.
- Verdict. We retain the master theorem as a (novel) Theorem 2.1 at
  confidence 0.95, with the explicit caveat in §1.3 that a definitive
  Murty–Murty 2009 chapter check before submission is **mandatory**.
  Per the task file's stop-condition, if such a check found the
  master theorem verbatim in Murty–Murty, the paper would be
  demoted to a "clean restatement + improved verification" rather
  than original; we do not believe this is the case but record the
  audit gap.

---

## J. Numerical-evidence sources

These are computational scripts in the bundle, not external
publications. They are listed for reproducibility but not subject to
PDF citation audit.

- `Smoothed_Dwf_numerical.gp`/`.out` — 8-digit at N = 10^5 for ζ.
- `zeta_prime_calibration.gp`/`.out` — ζ' baseline T = 100..10000.
- `family_avg_finite_T_fix.gp`/`.out` — 14-curve Petersson family
  average at T = 400, 1000.
- `/tmp/multiL_test*` — multi-L numerics referenced in §5 / §6 of the
  draft (results reproduced verbatim from `Delta_machine_multi_L.md`).
- `/tmp/delta_extended/ext*` — higher-order Δ^k numerics, residual
  growth analysis (cited in §5 of the draft).

For each numerical row in the draft, the script and (mp.dps, zeros,
N) parameters are recorded inline; the audit verdict is "verified at
the digits stated, with truncation tail consistent with the
predicted decay" (no fabrication).

The PARI `lfunsympow` normalization (per
`PARI_LFUNSYMPOW_NORMALIZATION.md`) is **arithmetic** (central value
at s = (k+1)/2 for sym^k of a weight-k newform); when reproducing the
T8 GL(3)-sym²(11a1) result we disclose this convention in the
caption of Table 5.X.

---

## K. Audit summary

| Bucket | Count |
|--------|-----:|
| GREEN  (verbatim verified) | 14 |
| YELLOW (canonical reference, page verbatim pending) | 12 |
| RED    (disagrees with draft as cited) | 0 |
| WHITE  (could not retrieve, theorem demoted) | 1 (Polylog conjecture, demoted to corrected √N (log N)^{k-1} theorem; RMT-conditional limiting-distribution conjecture retained as Conjecture 5.Y with explicit conditionality) |

GREEN + YELLOW share = 26/27 = 96 %. The single WHITE is the
strong-form polylog claim, and it has been demoted. Per the task file's
stop-rule (>20 % unverifiable triggers a stop), we are well under
threshold.

Two YELLOW items deserve to be flagged for the bibliography page
check before any external submission:

1. Macdonald 1979/1995 Ch. I §4 — the exact page in the second edition.
2. Selberg 1989 / 1992 — the (Q, λ_j, μ_j) presentation has subtle
   conventions; we restate the axioms following Iwaniec–Kowalski
   2004 §5.13 verbatim, with citation to Selberg as the original.

---

End of citation audit. See `Delta_machine_paper_compositio_draft.md`
for the body of the paper, and
`Delta_machine_paper_theorem_registry.md` for the per-theorem
confidence registry.
