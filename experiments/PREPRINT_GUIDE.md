# Preprint Submission Guide for Farey Research Papers

**Date:** 2026-03-28
**Purpose:** Practical, actionable guidance for submitting our work to preprint servers.

---

## 1. arXiv -- The Primary Target

### 1.1 Account Creation and Endorsement

**Creating an account:**
- Go to https://arxiv.org and register with your name, email, affiliation, and ORCID (if available).
- An institutional (.edu) email helps but is NO LONGER sufficient for automatic endorsement as of December 2025 / January 2026.

**New endorsement policy (critical -- updated Jan 2026):**
- Automatic endorsement now requires BOTH:
  1. An institutional/academic email address, AND
  2. Prior authorship of papers already on arXiv in the same endorsement domain.
- If you do not meet both criteria, you MUST get a personal endorsement from an established arXiv author.
- To find endorsers: on any arXiv abstract page, click "Which authors of this paper are endorsers?" at the bottom.
- Good endorser candidates: university collaborators, professors in number theory or mathematical physics who are active on arXiv.
- Do NOT mass-email potential endorsers. One respectful, personalized request with a link to your paper or ORCID profile.
- arXiv staff cannot personally endorse anyone.

**Action item for us:** Since we likely lack prior arXiv papers, we need to secure a personal endorsement BEFORE our first submission. Start reaching out to potential endorsers now -- this is the longest lead-time item.

### 1.2 Format Requirements

**Preferred:** LaTeX source files (strongly preferred over PDF-only).
- arXiv compiles your LaTeX on their servers using TeX Live 2025 (default).
- Upload as .zip or .tar.gz containing all .tex, .bib, and figure files.
- Figures must be .pdf, .jpg, or .png for PDFLaTeX.
- File names are case-sensitive on arXiv's system.
- No embedded JavaScript, no watermarks, no line numbers.
- As of Nov 2025, you can upload .bib files directly (no need to pre-compile .bbl).
- XeLaTeX is now supported (added late 2025).

**PDF-only submissions:** Accepted but discouraged. Must embed all fonts (TrueType/Type1, not bitmap). No copyright statements that block redistribution.

**For our papers:**
- Main math paper (26pp LaTeX): Already in the right format. Verify it compiles cleanly with TeX Live 2025.
- Three-body paper (markdown): Needs LaTeX conversion first. Use pandoc or rewrite in LaTeX.
- Radio-silent report: Convert to LaTeX or submit PDF-only.

### 1.3 Versioning and Updates

- YES, you can update after posting. arXiv archives ALL versions permanently.
- To update: use "Replace" on your submission, do NOT create a new submission.
- No new version is created for edits made before public announcement.
- All versions remain accessible (v1, v2, v3...) with timestamps.
- This is a feature, not a bug -- it helps with priority disputes.

**Common practice:** 2-4 versions is typical. v1 = initial post, v2 = after feedback, v3 = after journal acceptance with final corrections.

### 1.4 Moderation Timeline

- **Standard (no issues):** Submission at 14:00 ET cutoff -> announced same evening at 20:00 ET. Effectively 1 business day.
- **If flagged for moderation:** ~15% of submissions get flagged. Resolution goal is 24 hours, but can take several days to 2 weeks.
- **First-time submitters:** Expect closer scrutiny. Budget 1-2 weeks for the first submission to clear.
- Moderation is NOT peer review. They check: correct category, proper formatting, appears to be refereeable scientific content. They do not assess correctness.

### 1.5 Categories for Our Work

**Primary categories (pick one per paper):**

| Paper | Primary Category | Description |
|-------|-----------------|-------------|
| Main Farey math paper | `math.NT` | Number Theory |
| Three-body paper | `math-ph` | Mathematical Physics |
| AMR/mesh paper | `cs.CG` | Computational Geometry |
| 3DGS paper | `cs.CV` | Computer Vision and Pattern Recognition |
| Radio-silent report | `eess.SP` | Signal Processing |

**Cross-listing (secondary categories):**
- Yes, one paper CAN appear in multiple categories via cross-listing.
- You select a primary category, then add cross-listings one at a time during submission.
- arXiv moderators may alter your category choice.
- Recommended cross-listings:
  - Main math paper: primary `math.NT`, cross-list `math.CO` (Combinatorics)
  - Three-body paper: primary `math-ph`, cross-list `nlin.CD` (Chaotic Dynamics), `astro-ph.EP`
  - AMR paper: primary `cs.CG`, cross-list `cs.NA` (Numerical Analysis)
  - 3DGS paper: primary `cs.CV`, cross-list `cs.GR` (Graphics)

### 1.6 MSC Codes

Mathematics Subject Classification codes (MSC2020) are recommended for math papers:
- **11B57** - Farey sequences; the Stern-Brocot tree
- **11M06** - Zeta and L-functions (for RH connections)
- **11N05** - Distribution of primes
- **70F07** - Three-body problems (for three-body paper)
- **65M50** - Mesh generation/refinement (for AMR paper)

Format in metadata: "Primary: 11B57; Secondary: 11M06, 11N05"

### 1.7 Work-in-Progress Risk

**Low risk for math/physics:** arXiv culture in these fields strongly supports posting early. The physics community built arXiv specifically for sharing work before journal publication.

**Potential concerns:**
- A poorly written v1 is permanently archived. You can replace it, but v1 never disappears.
- Incorrect claims in v1 can damage reputation even if corrected in v2.
- Some reviewers may see your preprint and lose anonymity in double-blind review (mostly a concern in CS, not math).

**Recommendation:** Submit when the results are correct and the writing is clear, even if not journal-polished. Do NOT submit outlines or incomplete drafts.

---

## 2. Other Preprint Servers

### 2.1 Zenodo (CERN)

**Best for:** Code, datasets, supplementary materials, and minting DOIs for non-paper artifacts.

**Key features:**
- Instant DOI minting via DataCite.
- GitHub integration: tag a release and it automatically archives to Zenodo with a DOI.
- Accepts any file type (code, data, PDFs, notebooks).
- API available for programmatic uploads.
- Free, operated by CERN.
- "Concept DOI" (parent DOI) always resolves to the latest version.

**For us:** Use Zenodo for:
- Our computational verification code (C programs, Python scripts).
- The BC verification datasets (CSV files).
- Jupyter notebooks with reproducible experiments.
- Each gets a citable DOI we can reference in arXiv papers.

**Note (2026):** Zenodo reportedly de-ranks records from non-academic submitters in search results.

### 2.2 SSRN (Social Science Research Network)

- Now owned by Elsevier (acquired 2016).
- Originally social sciences, expanding to other fields.
- Less suitable for pure math. No significant advantage over arXiv for our work.
- Some concern about Elsevier ownership and long-term openness.
- **Skip for our papers.**

### 2.3 HAL (French Open Archive)

- Multidisciplinary, accepts PDFs directly (no LaTeX requirement).
- Mandatory for French researchers; international submissions welcome.
- Over 842K documents hosted.
- Could be useful as a secondary deposit for international visibility, especially if we collaborate with French researchers.
- **Lower priority than arXiv. Consider as supplementary.**

### 2.4 Recommendation for Interdisciplinary Work

For applied/interdisciplinary papers (AMR mesh, 3DGS, radio-silent):
1. **arXiv** remains the best primary server -- it covers CS, physics, math, and engineering.
2. **Zenodo** for code/data alongside the arXiv paper.
3. HAL as optional supplementary deposit.
4. SSRN only if targeting economics/finance applications.

---

## 3. Priority Protection

### 3.1 Does arXiv Establish Priority?

**Yes.** This is one of arXiv's core purposes.
- Every submission gets a precise timestamp (date + time of final "Submit" click).
- All versions are permanently archived with their timestamps.
- arXiv founder Paul Ginsparg has stated that arXiv postings are accepted as date-stamped priority claims.
- In a survey of bioRxiv users, only 1.25% reported that posting a preprint negatively affected their priority claim.

### 3.2 Journal Acceptance of Preprint Priority

- Nearly all math and physics journals accept arXiv preprints as evidence of prior work.
- The American Mathematical Society, most Springer/Elsevier math journals, and all major physics journals have no issues with arXiv preprints.
- Some journals (EMBO Press, Review Commons affiliates) explicitly provide "scooping protection" from the date of preprint posting.
- Research shows papers posted to arXiv before review receive ~65% more citations after one year compared to papers posted after acceptance.

### 3.3 Risks

**Scooping:** Extremely low risk in mathematics. The timestamp is your protection. In fields where arXiv is standard (math, physics, CS), attempting to scoop a preprint would be academic misconduct and easily detected.

**Journal policies:** Very few journals refuse previously preprinted work. Check the specific journal's policy, but this is rarely an issue in math/physics. The Sherpa/Romeo database (https://v2.sherpa.ac.uk/romeo/) tracks journal preprint policies.

**De-anonymization:** If submitting to a double-blind review venue (common in CS conferences), your arXiv preprint reveals your identity. Some CS venues have specific policies about this.

---

## 4. Practical Setup

### 4.1 arXiv Submission API

An API exists (https://github.com/arXiv/arxiv-submission-api) supporting:
- Programmatic submission via POST to `/submission/` endpoint.
- Source package upload via PUT to `/submission/{id}/source/`.
- OAuth-based authorization with client credentials.
- Proxy submission (submitting on behalf of another user) and bulk submission modes.

**However:** For our volume (a few papers), the web interface is simpler. The API is designed for conference proceedings and high-volume depositors. Use the web UI.

### 4.2 Can Claude/AI Manage Submission?

**Partially.** Claude can help with:
- Preparing and checking LaTeX source files.
- Writing abstracts and selecting categories/MSC codes.
- Formatting metadata.
- Reviewing submission checklists.

**Claude cannot:**
- Create an arXiv account (requires human identity verification).
- Submit papers (requires authenticated web session).
- Obtain endorsements (requires human relationships).
- Handle CAPTCHA or identity verification steps.

### 4.3 Required Information for Submission

Prepare these before starting:

| Field | Notes |
|-------|-------|
| Title | Exact title as in paper |
| Authors | Full names, affiliations, emails. No anonymous submissions. |
| Abstract | Plain text, can include LaTeX math notation |
| Primary category | e.g., math.NT |
| Cross-list categories | Optional, added after primary selection |
| MSC codes | Primary + secondary, e.g., "11B57; 11M06" |
| Comments | Optional: page count, figure count, "submitted to [journal]" |
| Journal-ref | Only if already published |
| DOI | Only if already has one |
| License | Choose from arXiv's options (CC BY 4.0 recommended) |
| Source files | .zip/.tar.gz of LaTeX + figures + .bib |

---

## 5. Our Specific Papers -- Readiness Assessment

### 5.1 Main Math Paper (26pp LaTeX)

**Status:** Ready or near-ready for arXiv math.NT.

**Checklist:**
- [ ] Verify LaTeX compiles with TeX Live 2025 (test on Overleaf or local install)
- [ ] All figures in .pdf/.png/.jpg format
- [ ] Bibliography complete and well-formatted
- [ ] Abstract is self-contained and clear
- [ ] MSC codes selected (11B57 primary)
- [ ] Secure endorsement for math.NT
- [ ] Final proofread for any incorrect claims

**Priority:** HIGH. Submit this first. It establishes priority for the core results.

### 5.2 Three-Body Paper (Draft Markdown)

**Status:** Needs LaTeX conversion before submission.

**Steps:**
1. Convert markdown to LaTeX (pandoc + manual cleanup)
2. Add proper math formatting, theorem environments
3. Include figures in appropriate format
4. Write formal abstract
5. Target: math-ph primary, cross-list nlin.CD

**Priority:** MEDIUM. Convert and submit after the main paper.

### 5.3 AMR Paper (Outline Only)

**Status:** Too early for arXiv.

**Recommendation:** Do not submit outlines or paper skeletons. arXiv expects content that could be sent to a journal for refereeing. Complete the paper first, including:
- Full methodology section
- Computational results with comparisons
- At least preliminary conclusions

**Priority:** LOW. Finish writing first.

### 5.4 Radio-Silent Technical Report

**Status:** Depends on completeness.

**Options:**
- If it reads as a self-contained technical contribution: arXiv `eess.SP` (Signal Processing).
- If it is more of a dataset/methodology report: Zenodo with DOI.
- If it is an internal report not meant for broad distribution: keep local, do not preprint.

**Priority:** Assess content completeness before deciding.

---

## 6. Common Practices and Norms

### 6.1 Early Drafts vs. Polished Versions

**Both are common, but norms vary by field:**
- **Mathematics:** Culture leans toward posting more polished work. Peer expectations are high for correctness. Posting a paper with errors in proofs can be reputationally costly.
- **Physics:** More tolerant of early-stage work and rapid posting.
- **CS:** Mixed. Conference-driven fields often post near-final versions.

**Our approach:** Post when results are correct and clearly stated. Writing can be improved in v2. Do not wait for perfection, but do not post with known gaps in proofs or results.

### 6.2 Typical Number of Versions

- 2-3 versions is most common.
- v1: Initial submission.
- v2: Corrections after community feedback or reviewer comments.
- v3: Final published version (matching journal version).
- Some active papers go to v5+ over years as results are extended.

### 6.3 Stigma Around Updates

**No stigma for reasonable updates.** Correcting errors, improving exposition, and adding results are all normal and expected. The community appreciates authors who maintain their preprints.

**What to avoid:**
- Submitting a v1 that is clearly unfinished just to claim a timestamp.
- Frequent trivial updates (fixing typos every day). Batch corrections.
- Dramatically changing the paper's claims between versions without clear explanation.

**Best practice:** Include a "Changes in this version" note in the Comments field when updating. Example: "v2: Corrected proof of Theorem 3.2, added Section 5 on applications."

---

## 7. Recommended Submission Sequence

1. **NOW:** Identify and contact a potential arXiv endorser for math.NT.
2. **Week 1:** Verify main math paper LaTeX compiles on TeX Live 2025. Final proofread.
3. **Week 1-2:** Create arXiv account, get endorsement confirmed.
4. **Week 2:** Submit main math paper to arXiv math.NT.
5. **Week 2:** Upload verification code and datasets to Zenodo (get DOIs).
6. **Week 3+:** Begin LaTeX conversion of three-body paper.
7. **Month 2:** Submit three-body paper to arXiv math-ph.
8. **When ready:** Complete and submit AMR paper, radio-silent report.

---

## 8. Key Links

- arXiv submission guide: https://info.arxiv.org/help/submit/index.html
- arXiv endorsement policy: https://info.arxiv.org/help/endorsement.html
- arXiv category taxonomy: https://arxiv.org/category_taxonomy
- arXiv submission schedule: https://info.arxiv.org/help/availability.html
- Zenodo: https://zenodo.org
- MSC2020 codes: https://mathscinet.ams.org/msc/msc2020.html
- Sherpa/Romeo (journal preprint policies): https://v2.sherpa.ac.uk/romeo/
- Overleaf arXiv checklist: https://www.overleaf.com/learn/how-to/LaTeX_checklist_for_arXiv_submissions
- arXiv submission API (GitHub): https://github.com/arXiv/arxiv-submission-api
