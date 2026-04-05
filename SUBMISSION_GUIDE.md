# Paper Submission & Dissemination Guide
# "The Geometric Signature of Primes in Farey Sequences"
# Created: 2026-04-05

---

## A. arXiv Submission (FIRST PRIORITY)

### Step 1: Get Endorsement
You need an endorser for math.NT (Number Theory).

**Email template for endorsers:**
```
Subject: arXiv endorsement request — Farey sequences and zeta zeros

Dear [Name],

I'm an independent researcher and I've written a paper on per-step
Farey discrepancy and its connection to the Riemann zeta function.
The paper introduces a "Farey Spectroscope" that detects the first
three nontrivial zeros of ζ(s) from Farey sequence data alone, and
establishes a damage/response mechanism explaining why primes improve
rational number regularity. Key results are formally verified in
Lean 4.

Would you be willing to endorse my submission to math.NT on arXiv?
I'm happy to share the manuscript for your review.

The paper is ~15 pages with 16 figures and is available at:
[link to PDF or GitHub]

Best regards,
Saar Shai
```

**Finding endorsers:**
- Go to any paper you cite on arXiv (e.g., Rubinstein-Sarnak 1994)
- Click "Which authors of this paper are endorsers?" at the bottom
- Contact 1-2 endorsers with the email above
- Do NOT mass-email. Contact one at a time.

### Step 2: Prepare Submission Files
- [ ] main.tex (your paper)
- [ ] All .png/.pdf figures (16 files)
- [ ] .bbl file (bibliography) — compile locally first, then upload the .bbl
- [ ] Optional: ancillary files (Lean proofs, Python scripts)

### Step 3: Submit
1. Log in at https://arxiv.org/submit
2. Select category: **math.NT** (Number Theory)
3. Cross-list to: **math.CA** (Classical Analysis), **math.DS** (Dynamical Systems)
4. Upload files (tex + figures)
5. Enter metadata:
   - Title: The Geometric Signature of Primes in Farey Sequences
   - Authors: Saar Shai
   - Abstract: (copy from paper)
   - MSC: 11B57, 11M06, 11N37, 11A25, 11Y35
   - Keywords: Farey sequence, Mertens function, Chebyshev bias, zeta zeros, Lean 4
6. Preview and submit
7. Note: AI assistance is disclosed in the paper's "AI Use Declaration"
   section per STM 2025 guidelines. The human author is sole listed author.
8. Paper appears within 1-2 business days

---

## B. Journal Submission — Experimental Mathematics

### Step 1: Prepare
- [ ] Reformat if needed (Taylor & Francis style — usually minimal changes)
- [ ] Write a cover letter (see template below)

### Step 2: Submit
1. Go to: https://mc.manuscriptcentral.com/uexm (ScholarOne portal)
2. Create account if needed
3. Upload manuscript + figures
4. Select subject area: Number Theory / Computational
5. Suggest reviewers (optional but helpful):
   - Andrew Granville (granville@dms.umontreal.ca)
   - Kannan Soundararajan (ksound@stanford.edu)
   - Michael Rubinstein (mrubinst@uwaterloo.ca)

### Cover letter template:
```
Dear Editors,

Please find our manuscript "The Geometric Signature of Primes in
Farey Sequences" for consideration in Experimental Mathematics.

The paper introduces the per-step Farey discrepancy ΔW(p) — a novel
object — and presents three main contributions:

1. A "Farey Spectroscope" that detects the first three nontrivial
   zeros of ζ(s) from Farey data alone (γ₁, γ₂, γ₃ to within 0.8%),
   extending to L-function zeros via character twisting.

2. A damage/response mechanism explaining why primes improve rational
   regularity, with the exact formula D(1/p) = 1 - |F_{p-1}|/p.

3. A healing characterization showing that composite density
   (measured by φ(n)/n) controls the damage/healing boundary,
   with the fraction 1/p alone causing 65% of all damage.

All core identities are formally verified in Lean 4 (258 results).
The spectroscope's validity is confirmed by null hypothesis
controls (random weights produce no peaks; the signal survives
without the M(p)≤-3 filter). An analytic gap in the shift-squared
asymptotic is honestly identified as involving Dedekind-sum
convolutions rather than Kloosterman sums.

Code, data (5,095 qualifying primes), and all figures are
publicly available at https://github.com/SaarShai/Primes-Equispaced.

Sincerely,
Saar Shai
```

---

## C. Other Journals (after arXiv)

### Mathematics of Computation
- Submit at: https://mc.manuscriptcentral.com/mcom (AMS)
- Best fit for: computational results + formal verification
- Typical review time: 6-12 months

### Journal of Number Theory
- Submit at: https://www.editorialmanager.com/jnt (Elsevier)
- Best fit for: pure number theory results (bridge identity, D(1/p))
- Typical review time: 3-6 months

### Research in Number Theory (Springer)
- Submit at: https://www.springer.com/journal/40993
- Welcomes computational work
- Faster review

---

## D. Other Preprint Servers

### Zenodo (DOI for code+data)
- [ ] Go to https://zenodo.org
- [ ] Log in with GitHub
- [ ] Create new upload
- [ ] Upload: GitHub repo zip, main.pdf, data files
- [ ] Get DOI (e.g., 10.5281/zenodo.XXXXXXX)
- [ ] Add DOI to paper's "Data and Code Availability" section

### HAL (French preprint server)
- [ ] Go to https://hal.science
- [ ] Create account
- [ ] Submit PDF with metadata
- [ ] Good for reaching French NT community (Boca, Zaharescu connections)

### ResearchGate
- [ ] Create/update profile at https://www.researchgate.net
- [ ] Upload paper
- [ ] Tag relevant researchers
- [ ] Answer questions from readers

---

## E. Social Media & Outreach

### Twitter/X Thread
Post a 5-tweet thread:
```
1/ New paper: "The Geometric Signature of Primes in Farey Sequences"
   We detect zeta zeros from Farey sequence data alone — a different
   computational path to the zeros of ζ(s). [spectroscope figure]

2/ The "Farey Spectroscope": F(γ) = |Σ R(p)·p^{-1/2-iγ}|² peaks
   at zeta zero locations. First 3 zeros detected to <1% error
   from 3,829 primes. [juxtaposition figure]

3/ Why do primes improve rational regularity? A damage/response
   mechanism: primes DAMAGE order, but existing fractions
   OVERCOMPENSATE. The fraction 1/p alone causes 65% of the damage.

4/ Formally verified in Lean 4 (258 results). Extends to L-function
   zeros via Dirichlet character twisting. Code + data on GitHub.

5/ Paper: [arXiv link]
   Code: https://github.com/SaarShai/Primes-Equispaced
   Joint work with @AnthropicAI's Claude.
```

### MathOverflow
Post a focused question:
```
Title: "Detecting zeta zeros from Farey discrepancy data"

We computed F(γ) = |Σ_p R(p)·p^{-1/2-iγ}|² where R(p) is the
insertion-deviation correlation ratio for Farey sequences, and
found peaks at γ₁, γ₂, γ₃ of ζ(s). Is this phenomenon known?
The theoretical basis appears to be the explicit formula, but
the specific use of Farey discrepancy data as input is new to us.
```

### YouTube/Blog
- Record a 10-minute explainer showing the spectroscope figure
- Use animations of Ford circles + mediant insertion
- Target: 3Blue1Brown style accessibility

---

## F. People to Contact (with email templates)

### Tier 1: Directly relevant (contact first)

**Jens Marklof** (Bristol) — horocycle equidistribution
```
Subject: Farey per-step discrepancy and horocycle equidistribution

Dear Prof. Marklof,

Your work on Farey sequences and horocycle flows is foundational to
our research. We've introduced a per-step Farey discrepancy ΔW(p)
and discovered it's phase-locked to the first zeta zero, detectable
via a "spectroscope" construction. We believe this connects to your
horocycle equidistribution results.

Paper: [arXiv link]

We would greatly value your perspective on whether this per-step
framework adds to the horocycle picture.

Best regards, Saar Shai
```

**Michael Rubinstein** (Waterloo) — Chebyshev bias
```
Subject: Chebyshev bias in Farey discrepancy

Dear Prof. Rubinstein,

Building on your work with Sarnak on Chebyshev's bias, we've found
an analogous bias in per-step Farey discrepancy: sgn(ΔW(p)) is
phase-locked to cos(γ₁·log(p) + φ) with R = 0.77. We believe the
density → 1/2 under GRH+LI, following your framework.

Paper: [arXiv link]

Would you be interested in discussing this connection?

Best regards, Saar Shai
```

**Florin Boca** (UIUC) — Farey gap distribution
```
Subject: Gauss-Kuzmin concentration in per-step Farey discrepancy

Dear Prof. Boca,

Your work with Cobeli and Zaharescu on Farey gap distribution
inspired our finding that 20% of fractions (by CF depth) contribute
93% of the per-step discrepancy signal. We introduce a "Farey
Spectroscope" that detects zeta zeros from this data.

Paper: [arXiv link]
```

### Tier 2: Broader interest

**Andrew Granville** (Montréal) — analytic NT expert
**Kannan Soundararajan** (Stanford) — multiplicative NT
**Terry Tao** (UCLA) — if spectroscope result is strong enough
**Kevin Ford** (UIUC) — Mertens function expert
**Peter Sarnak** (IAS) — spectral theory, modular surfaces

### Tier 3: Organizations

**OEIS** — Submit sequences:
- R₂(p) for qualifying primes
- D(1/p) values
- min R₂ running minimum

**LMFDB** — Contact about adding Farey spectroscope data

**Wolfram** — Suggest FareySpectroscope[] function for Mathematica

### Tier 4: Companies (AMR applications)

**Cesium** (cesium.com) — planetary terrain LOD
- Contact: engineering@cesium.com
- Pitch: crack-free LOD hierarchy via Farey neighbor property

**Ansys** — CFD shock-capturing
- Contact: innovation team
- Pitch: 7-15x cell reduction via Farey AMR

---

## G. Timeline

| Week | Action |
|------|--------|
| **Week 1** | Get endorser, submit to arXiv, push GitHub |
| **Week 2** | arXiv appears, post Twitter thread, submit to journal |
| **Week 3** | Contact Marklof, Rubinstein, Boca |
| **Week 4** | Post on MathOverflow, submit to Zenodo |
| **Month 2** | Contact broader researchers, blog post |
| **Month 3+** | Conference talks, follow up on journal review |
