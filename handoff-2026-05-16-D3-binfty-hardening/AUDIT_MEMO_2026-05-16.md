# D3 numerical-hardening audit memo — corrected B∞ / C₁ / e^{−γ}

**Date:** 2026-05-16  **Scope:** the user's own independent verification
work. Nothing here is sent to Koyama; no push without explicit user
approval (Koyama counterparty unverified — see `project_koyama_risk`).

This memo records what was primary-verified, what was wrong, what was
fixed, and the exact conditional/unconditional boundary. It is written
to be referee-safe: every citation locus was checked at a primary
source this session; every "unconditional" claim was re-audited.

---

## 1. Citation lock (all primary-verified 2026-05-16)

| Cite | Correct bibliographic data (verified) | Source checked | Conditionality of the cited statement |
|---|---|---|---|
| **Akatsuka** (Lemma 2.1 / eq. (2.5)) | "The Euler product for the Riemann zeta-function in the critical strip", *Kodai Math. J.* **40** (2017), 79–101, DOI 10.2996/kmj/1490083225 | Akatsuka publication list (Otaru-UC) + ProjectEuclid + the local published PDF (`akatsukaDRH3.pdf`) read this session | eq. (2.5) for t₀≠0 is **UNCONDITIONAL** — proved (eqs. (2.6)–(2.7)) by integration by parts against PNT with the classical error term π(x)=x/logx+O(x/(logx)²). It is the §2 *preliminary* lemma, logically independent of that paper's RH/DRH-conditional critical-strip Theorem 1. |
| **Aoki–Koyama** (eq. (1.4), Hyp. AK) | "Chebyshev's bias against splitting and principal primes in global fields", *J. Number Theory* **245** (2023), 233–262, DOI 10.1016/j.jnt.2022.10.005, arXiv:2203.12266 | ScienceDirect search + arXiv + the local published PDF (`1-s2.0-S0022314X22002335-main.pdf`) | eq. (1.4) e^{−mγ} limit is **DRH-CONDITIONAL** in characteristic 0 (number-field/Dirichlet setting). Abstract verbatim: "under the assumption of DRH"; "In positive characteristic cases, DRH is proved, and all these results hold unconditionally." |
| **Inoue** (Thm 1, eq. (4.1)) | Shōta Inoue, "Some explicit formulas for partial sums of Möbius functions", *J. Théor. Nombres Bordeaux* **33** (2021), no. 2, 273–315, DOI 10.5802/jtnb.1162, arXiv:1805.05015 | Centre-Mersenne / NUMDAM + arXiv | The paper's explicit formulas are **UNCONDITIONAL** (its stated purpose: make GRH-conditional formulas unconditional). |
| **Soundararajan** (Thm 1) | "Partial sums of the Möbius function", *J. Reine Angew. Math.* (**Crelle**) **631** (2009), 141–152, DOI 10.1515/CRELLE.2009.044, arXiv:0705.0723 | de Gruyter + arXiv | Thm 1 (M(x)≪√x·exp((logx)^{1/2}(loglogx)^{14})) is **RH-CONDITIONAL**. |

---

## 2. Defects found and fixed

### 2.1 Akatsuka year — REAL citation error (FIXED)
There is **no Akatsuka 2013 paper**. His only relevant works are
*Kodai Math. J.* **40** (2017), 79–101 and *J. Number Theory* **132**
(2012), 2242–2257. The prose "Akatsuka (2013)" in Appendix A (5 loci),
`SECTION_DRAFT` (3 loci), `Koyama_B_infty_proof.md`,
`Koyama_AK_constant_proof.md`, `INTRODUCTION_DRAFT`, `SP_L_…`,
`LEAN_SORRY_STATUS`, and `clean.py` was a year error. The live
`references.bib` *metadata* was already correct (`year=2017`), but the
bibkey string `AkatsukaH2013EulerProduct` and the prose were not.
- **Fixed:** Appendix A `.md` master fully corrected (year + full Kodai
  40 (2017) 79–101 cite). Bibkey renamed `AkatsukaH2013EulerProduct →
  Akatsuka2017EulerProduct` across `references.bib`,
  `INTRODUCTION_DRAFT`, `clean.py`. `clean.py` citation patterns
  rewritten for the 2017 phrasings *and* kept legacy 2013 patterns
  (re-pointed to the correct key) so any residual stale prose
  auto-corrects to the right (2017) bibliography entry. `.tex`
  regenerated; `section_X.tex` auto-corrected. (PDF rebuild = user's
  `tectonic` step; no LaTeX engine in this environment.)

### 2.2 P(3/2) arithmetic error — REAL (FIXED)
Appendix A §A.3 and `Koyama_B_infty_proof.md` §5 stated
"P(3/2)=∑ₚp^{−3/2}≈0.45224" and the crude bound "|T≥3|≲0.515".
**0.45224742… is the prime zeta at s=2, not s=3/2.** Verified
(mpmath/Arb): P(3/2)=0.8495626836…, P(2)=0.4522474200…. Corrected
crude bound: |T≥3| ≤ P(3/2)/(3(1−2^{−1/2})) = 1.13807×0.84956 ≈
**0.967**. This is a slack bound on an absolutely convergent quantity
— it does **not** affect the identity — but the printed numeral was
wrong and referee-catchable. Truncation tail re-derived cleanly:
elementary rigorous ∑_{p>K}p^{−3/2} ≤ 2K^{−1/2} ⇒ |T≥3−T≥3,K| ≤
2.276 K^{−1/2}; PNT-sharpened ⇒ ≈4.55 K^{−1/2}/logK (≈3.3·10⁻⁴ at
K=10⁶, ≈2.2·10⁻⁴ at K=2·10⁶). Fixed in Appendix A `.md`+`.tex`;
flagged for `Koyama_B_infty_proof.md` (proof of record).

### 2.3 A.2.3 non-principal-ψ leg — IMPRECISE (TIGHTENED)
The draft wrote "the same partial-summation argument applies with
χ²(p)/p^{1+2iτ} … character orthogonality producing the appropriate
cancellation." Akatsuka eq. (2.5) is *literally* only the trivial
character (ζ). Made precise: χ²-principal (χ₋₄, χ₈) is covered by
eq. (2.5) literally; χ²-non-principal (χ₅,χ₇,χ₁₁,χ₁₃) repeats
Akatsuka's eq. (2.6) integration-by-parts with π(u) → π(u;ψ) and PNT
→ its non-principal analogue ∑_{p≤u}ψ(p)≪u·exp(−c√log u) (de la
Vallée Poussin / Siegel–Walfisz, *fixed* conductor, **unconditional**),
giving an *unconditional* O(exp(−c√log X)) remainder — stronger than
O(1/log X). The conclusion (unconditional convergence) is unchanged;
the citation is now honest.

### 2.4 "Annals 170" — FABRICATED locus, CONTAINED (flagged)
`log.md:1816` (a prior "fix" audit) describes Soundararajan 2009 as
"Ann. of Math. **170** (2009), 1409–1422". That is **wrong** — the
paper is **Crelle 631 (2009), 141–152**. The fabricated Annals datum
appears *only* in `log.md`'s narrative; it did **not** propagate to
the live `references.bib`, Appendix B, or §X (all correctly say
Crelle 631). No artifact fix needed; flagged in memory so a future
agent does not "restore" the wrong Annals data from `log.md`. This is
the project's #1 failure mode appearing *inside the very audit meant
to cure it* — recorded as a cautionary instance.

### 2.5 PARI/GP + 250-bit Arb cross-stack — NOT REPRODUCIBLE HERE (honesty)
§X.5.2/§X.5.4 claim "L2 cross-language PARI/GP 2.17.3 agrees ≥11
digits" and "Arb spot-check at 250 bits within 3·10⁻⁴³", with K=10⁷,
10⁸ residual columns labelled "(L2 = PARI/GP)". In this environment
there is **no `gp` binary** and no native 250-bit Arb run; K=10⁸ was
**not re-run**. The hardening provides a *different, fully
reproducible* independent cross-check: mpmath (dps 50 **and** 80,
precision-doubling) **and** python-flint/Arb 0.6.0 (rigorous ball
arithmetic, proven radii). Recommendation: relabel §X.5.2/§X.5.4 to
state the cross-validation at exactly the strength reproducible here,
or have the user re-run the PARI/Arb legs and keep them only if
independently reproduced. (Action item, not yet applied to §X — see §4.)

---

## 3. The conditional/unconditional boundary (re-audited, authoritative)

1. **B∞ identity (★)** `T∞ = ½logL(2ρ,ψ)+BPC₁+BPC₂+T≥3` —
   **UNCONDITIONAL** given ρ a simple zero. Only boundary-line
   conditional convergence (the k=2 sum) is handled by the
   *unconditional* Akatsuka 2017 eq. (2.5) / its non-principal
   analogue. No RH/GRH/EDRH/DRH. ✔ correctly labelled.
2. **k=2 boundary-sum rate.** χ²-principal: **unconditional**
   O(1/logK) (Akatsuka 2017). χ²-non-principal: **unconditional**
   O(exp(−c√logK)) floor; the *observed* ~K^{−1/2} is the
   RH(L(·,ψ))-**conditional** Soundararajan-character analogue —
   *not* claimed unconditionally. ✔ now precisely stated.
3. **C₁ leading+subleading identity (†)** `c_K = logK/L′(ρ) + C₁ +
   o(1)`, `C₁ = −L″/(2L′²)`. The *identity* is **UNCONDITIONAL**
   given simplicity of ρ (and crossed off-target zeros). The **o(1)
   RATE** is **RH(L(·,χ))-CONDITIONAL** (Soundararajan 2009,
   RH-conditional). ✔ correctly labelled in Appendix B / §X.
4. **Aoki–Koyama e^{−γ} limit (Hyp. AK)** `E_K logK → L′(ρ)/e^γ` —
   **DRH-CONDITIONAL** in char 0; unconditional only in positive
   characteristic. ✔ bib note + §X say "under DRH"; verifier prints
   "[DRH-CONDITIONAL]".
5. **Local Perron residue (Lemma X.3.1 / `LocalPerronResidue.lean`)**
   — the residue *algebra* is **UNCONDITIONAL** (Laurent expansion,
   Lean 0-sorry). ✔.

"Five loci" = the five places Soundararajan 2009 was once mislabelled
"unconditional" (§X.4.2, Appendix B intro, Appendix B §B.4, §X
References, references.bib note). Re-audited: **all five now correctly
say RH-conditional** (general) / unconditional only in the
numerically-verified-RH computational regime. The prior fix's *intent*
was right; only its `log.md` bib datum was fabricated (§2.4).

---

## 4. Residual action items (NOT yet applied; for user decision)

- **§X.5.2 / §X.5.4 PARI/Arb reproducibility** (§2.5): relabel to the
  reproducible-here strength, or user re-runs PARI/Arb. Left to the
  user because it changes the headline numerical-evidence framing and
  the prior handoff asserts those runs were done elsewhere.
- **`Koyama_B_infty_proof.md`** (handoff-2026-05-09-followup, proof of
  record): carries the same P(3/2)≈0.45224 / "Akatsuka 2013" defects.
  Dated correction note added (see that file) rather than silent edit,
  since it is a historical proof artifact.
- **bibkey** fully renamed; if any *external* draft references the old
  key it must be updated (none found in-repo).

---

## 5. What is genuinely established (honest scope ceiling)

The deliverable is **calibrated numerical evidence + an audited
pen-and-paper identity**, specialist tier — *not* a theorem, *not* RH
progress. The B∞ identity is an unconditional algebraic/analytic
identity (the legitimate contribution). The e^{−γ} normalization and
the C₁ o(1) rate remain DRH- / RH-conditional respectively and are
labelled as such everywhere. The K^{−1/2} clean-pair decay is
RH(L(·,ψ))-conditional and is **not** stated unconditionally. No
claim here advances RH/DRH.

---

## 6. Net gain (adversarial / who-cares — applied to this pass itself)

So this pass does not become its own inflation:

- **No new mathematics. Zero.** The B∞ identity was already a correct
  identity; the e^{−γ} correction and the C₁ formula were already
  right. Nothing moved toward RH/DRH. The strategic verdict in
  `project_farey_forward_verdict` is **unchanged**.
- **The gain is negative knowledge + defensibility, not progress.**
  Three referee-catchable errors removed (non-existent "Akatsuka
  2013"; P(3/2)=0.45224 which is actually P(2); a fabricated
  "Annals 170" locus in `log.md`); the conditional/unconditional
  line is now primary-verified rather than agent-asserted; a
  precision bug that made the prior "50-digit" check partly hollow
  is fixed. Net effect: the work can survive a referee and is not
  embarrassing as the user's own independent write-up.
- **Residual soft spots, not papered over.** The non-principal-ψ
  leg of A.2.3 is unconditional but by a *standard* argument
  (Siegel–Walfisz) that is ours, not a cited theorem — labelled as
  such. Two-engine agreement is "0 at displayed precision" with a
  rigorous Arb radius ~1e-65 (the Arb enclosure is rigorous; the
  mpmath side is heuristic but an independent codebase).
  PARI/native-Arb remain non-reproducible here.
- **Most of this value is contingent.** It matters chiefly if the
  Koyama collaboration is real (memory: unverified/risky). Absent
  that, the gain is that the user's standalone note is correct
  rather than refutable. Worth doing — but hygiene, not a result.
  This pass is **specialist-tier error-correction**; a future
  summary must not re-describe it as a breakthrough or as "B∞
  progress".
