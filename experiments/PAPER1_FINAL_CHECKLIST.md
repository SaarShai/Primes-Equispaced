# arXiv Submission Checklist: Number Theory (math.NT)

**Paper Subject:** Farey Discrepancy, Exact Identities, Chebyshev Bias, Lean Formalization.
**Target Category:** `math.NT`
**Status:** Pre-Submission

## 1. Administrative & Metadata
*   [ ] **Category Correctness:** Ensure submission category is set to **`math.NT`** (Number Theory).
*   [ ] **MSC Classification:** Select appropriate Mathematical Subject Classification (MSC) codes (e.g., 11N32, 11M26, 11Y55).
*   [ ] **Authors & Affiliations:** Verify all authors are listed with current email addresses and institutional affiliations. Check for any missing co-authors.
*   [ ] **arXiv Submission Form:** Confirm title matches the PDF title exactly.
*   [ ] **License:** Confirm copyright license (e.g., MIT, CC-BY-4.0).

## 2. AI & Tool Usage Disclosure (Critical)
*   [ ] **arXiv AI Declaration:** On the submission form, select **"Yes"** for AI usage if any generative AI tools were used (for drafting, code assistance, proofreading).
*   [ ] **Disclosure Text:** Ensure the specific disclosure statement (if added to the paper itself) aligns with arXiv policy.
*   [ ] **Lean Code:** Acknowledge that "422 Lean results" constitute computer-assisted proofs. Ensure the code repository link is provided in the source PDF or `lean` source file is attached if requested by the arXiv template.

## 3. Abstract & Introduction
*   [ ] **Word Count:** Abstract is **under 300 words**. (Count current total: [Enter Count]).
*   [ ] **Clarity of $\Delta_W(N)$:** The term **per-step Farey discrepancy $\Delta_W(N)$** is clearly defined within the abstract or first paragraph.
*   [ ] **Key Results Summarized:** The abstract explicitly mentions:
    *   The exact identities (Bridge, Injection, Four-term).
    *   The Chebyshev bias value ($R = 0.77$).
    *   The spectroscope finding (3 zeros).
    *   The scope of Lean verification (422 results).
*   [ ] **No Unexplained Metaphors:** The term "spectroscope" is either defined as a metaphor for a detection algorithm or replaced with standard number-theoretic terminology.

## 4. Technical Consistency & Citations
*   [ ] **Definition Order:** Every term is defined before first use (e.g., `R`, `N`, `Bridge`, `Injection`).
*   [ ] **Citation Check (Prior Art):**
    *   [ ] **Csoka (2015):** Verify full bibliographic details (title, journal, DOI).
    *   [ ] **Tomas Garcia (2025):** **CRITICAL VERIFICATION REQUIRED.**
        *   *Is this a preprint with a valid 2025 arXiv ID?*
        *   *Is this a future-dated citation?* (If submission is before 2025, ensure this is marked as "in preparation" or "forthcoming" to avoid rejection for citation of non-existent work).
*   [ ] **Identity Notation:** The exact identities (**Bridge, Injection, Four-term**) are clearly numbered (e.g., Theorem 1, Corollary 2) and referenced consistently in the text.
*   [ ] **Numerical Consistency:**
    *   [ ] Verify $R = 0.77$ is presented with sufficient precision or context (e.g., is it an approximation or an exact rational?).
    *   [ ] Verify "3 zeros" refers to specific locations (e.g., low-lying zeros of a specific L-function).
    *   [ ] Verify "422 Lean results" corresponds to the total number of theorems/proven lemmas in the formalization file.

## 5. Proofs & Formalization
*   [ ] **Logical Completeness:** All "Exact Identities" proofs flow logically from definitions and prior results (Csoka 2015).
*   [ ] **Lean Verification:**
    *   [ ] The `mathlib` or custom libraries used are listed in the bibliography or acknowledgments.
    *   [ ] There is no ambiguity regarding what the Lean code proves (e.g., is it checking the bias $R$ or the Farey discrepancy?).
*   [ ] **Error Check:** Scan for "TODO" comments or "Open Question" placeholders within the text that should be resolved before submission.

## 6. Figures & Tables
*   [ ] **Figure Quality:** All figures (especially the "spectroscope" output and bias plots) are high resolution (≥300 DPI).
*   [ ] **Captions:** Every figure has a descriptive caption.
*   [ ] **References:** Figure labels in the text match the figure numbers (e.g., "See Figure 1").
*   [ ] **Accessibility:** If the paper is long, ensure figures are not too dense to read on a standard screen.

## 7. Final Review & Formatting
*   [ ] **Reviewer Feedback:** If this is a resubmission, ensure all previous reviewer comments have been addressed in a "Response to Reviewers" document attached or included in the cover note.
*   [ ] **Typos & Grammar:** Run a spell-check, paying special attention to mathematical typesetting (no missing `$` symbols or `^\` errors).
*   [ ] **Equation Counting:** Ensure all equations are numbered if referenced later, and non-numbered equations do not need to be referenced.
*   [ ] **Bibliography:** Ensure `.bib` file is clean and matches `.tex` citations. No broken links in citations.

## 8. Submission Flow (Final Step)
*   [ ] **Source Files:** Upload `main.tex` (or `master.tex`), `.bib`, and all image files.
*   [ ] **Compiled PDF:** Confirm the uploaded PDF renders perfectly (no missing characters, fonts substituted).
*   [ ] **Abstract Preview:** Check the arXiv abstract preview window for formatting errors before clicking "Submit."

---

### ⚠️ Critical "Red Flags" to Address Immediately:

1.  **Citation "Tomas Garcia 2025":**
    *   *Action:* If you are submitting in **2024** or early 2025, citing a publication dated 2025 is problematic unless it is a preprint. If the paper was submitted, please verify this is not a typo for **2024** or **2023**. arXiv moderators may flag this as an invalid citation if the work is not yet existant in a public database.
2.  **AI Disclosure:**
    *   *Action:* arXiv now requires mandatory disclosure. If you used AI to summarize or proofread, you *must* check the box on the submission form. Failure to do so can lead to retractions.
3.  **Lean Formalization:**
    *   *Action:* Ensure the "422 Lean results" are accessible. If the code is not uploaded to the arXiv source, you may be required to link a repository (GitHub) in the abstract or introduction.

**Ready to Submit?** [ ] Yes / [ ] No (Revise Sections marked "Critical")
