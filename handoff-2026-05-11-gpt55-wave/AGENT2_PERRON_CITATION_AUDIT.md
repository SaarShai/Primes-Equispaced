---
schema_version: 1
title: "Agent 2 Perron Literature And Citation Audit"
date: 2026-05-11
agent: "GPT-5.5 xhigh Agent 2"
status: AUDIT_ONLY
confidence: 0.92
scope: "Inoue/Soundararajan/Aoki-Koyama/Koyama source audit for Perron-leading and email-safe citations"
---

# Agent 2 Perron Citation Audit

Status: AUDIT_ONLY

Confidence: 0.92. Dependencies: primary PDFs were retrieved/extracted with `pypdf`; Inoue and Soundararajan were freshly downloaded to `/tmp`; Aoki-Koyama, Akatsuka, Koyama book excerpt, and the Saar-Koyama correspondence were read from `/Users/za/Downloads`. Soundararajan journal metadata was verified from De Gruyter, but the quoted theorem text is from arXiv v2, not a De Gruyter PDF.

Verdict: the packet is citation-closed for a negative/claim-safe email pass. Aoki-Koyama supports an `e^{m gamma} m!` denominator in its Euler-product DRH formula and contains no `zeta(2)` constant; Inoue and Soundararajan do not close the shifted Perron nonlocal remainder; Koyama's book excerpt/correspondence do not supply a theorem for `1/zeta(2)` or for the shifted Perron-leading term.

Required local docs read first: `HANDOFF.md`; `KOYAMA_CLAIM_AUDIT_2026-05-11.md`; `Koyama_track_grounding.md`; `Koyama_AK_constant_proof.md`; `Koyama_Perron_remainder_theorem_hunt_2026-05-11.md`; `Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md`.

## Primary Source Ledger

### Aoki-Koyama 2023

Source: Miho Aoki and Shin-ya Koyama, "Chebyshev's bias against splitting and principal primes in global fields", Journal of Number Theory 245 (2023), 233-262, doi `10.1016/j.jnt.2022.10.005`. Retrieved PDF: `/Users/za/Downloads/1-s2.0-S0022314X22002335-main.pdf`.

Verified anchors:

- p.235, eq. (1.4): Dirichlet Euler-product DRH formula has denominator `e^{m gamma} m!`; quoted anchor: "with gamma being the Euler constant".
- p.237-p.238, Conjecture 1.1: DRH(A/B) is stated at the central point `1/2`; quoted anchor: "The limit (1.5) satisfies the following identity".
- p.244, eqs. (2.3)-(2.4): the proof splits the `k >= 3` absolutely convergent term and the `k = 2` central term by generalized Mertens.

Audit result:

- Source-closed: AK gives an `e^{-gamma}`-type Euler-product normalization in the formula it states, not `1/zeta(2)`.
- Source-closed: full extracted AK text has zero hits for `zeta(2)`, `1/zeta(2)`, `6/pi^2`, or equivalent spellings.
- Gap: AK p.235 writes `m = m_chi = ord_{s=1/2} L(s,chi)`, and Conjecture 1.1 is central-point Artin DRH. Using AK (1.4) directly for an arbitrary noncentral zero `rho = 1/2 + it` is not citation-closed from this PDF alone. It needs a cited Dirichlet/Akatsuka-style theorem with `m = ord_{s=rho} L(s,chi)`, or an explicit reduction.

### Akatsuka 2013

Source: Hirotaka Akatsuka, "The Euler product for the Riemann zeta-function in the critical strip", PDF `/Users/za/Downloads/akatsukaDRH3.pdf`.

Verified anchors:

- pp.2-3, Theorem 1, eqs. (1.4)-(1.5): zeta partial Euler product at fixed `s0 = 1/2 + it0`; formula includes `(log x)^m` and the pole-normalizing exponential.
- pp.2-3, Theorem 1 quoted anchor: "conditions 1-3 are equivalent".
- p.23, eq. (7.3): convergence of the Mobius-log sum would require `sum_{n<=x} mu(n) = o(x^{1/2} log x)`.
- p.23, after Soundararajan citation: quoted anchor: "out of our reach even if we assume the Riemann hypothesis."

Audit result:

- Source-closed for zeta: Akatsuka really does treat fixed critical-line points `s0`, unlike the central-point AK Artin statement.
- Gap: this is zeta, not nonprincipal Dirichlet `L(s,chi)` at arbitrary `rho`; it is a model/source pointer, not the missing GL(1) theorem itself.

### Inoue 2021

Source: Shota Inoue, "Some explicit formulas for partial sums of Mobius functions", Journal de Theorie des Nombres de Bordeaux 33 (2021), 273-315, doi `10.5802/jtnb.1162`. Retrieved PDF: `https://www.numdam.org/item/10.5802/jtnb.1162.pdf` to `/tmp/inoue_jtnb_1162.pdf`.

Verified anchors:

- p.274, Theorem 1, formula (1.4): explicit formula for `M*(x;q,a)` with nontrivial-zero residues of Dirichlet `L`-functions modulo `q`.
- p.276, Theorem 2, formulae (2.1)-(2.2): truncated version with error term `R`.
- p.274 and p.276 quoted anchors: "generalization of Bartz's formula"; "following truncated formula".
- p.275 multiplicity warning; quoted anchor: "We do not know even the boundedness of multiplicity at present."

Audit result:

- Source-closed: Inoue is an explicit-formula source for Mobius sums in arithmetic progressions and explicitly carries zero multiplicities.
- Negative for current promotion: Inoue does not state the shifted kernel theorem for `K^w/(w L(rho+w,chi))`, does not remove off-target zero residues, and does not prove `Z_simple(K,T_K)=o(log K)`.
- Practical consequence: citing Inoue for "Perron double-pole local residue" is safe only as contour-framework context. Citing it for the global asymptotic `c_K(chi,rho)=log K/L'(rho,chi)+o(log K)` is not source-closed.

### Soundararajan 2009

Source: K. Soundararajan, "Partial sums of the Mobius function". Publisher metadata: J. Reine Angew. Math. 631 (2009), 141-152, doi `10.1515/CRELLE.2009.044`. Retrieved theorem text from arXiv v2: `https://arxiv.org/pdf/0705.0723`, `/tmp/soundararajan_mobius_0705.0723.pdf`.

Verified anchor:

- arXiv p.1, Theorem 1: quoted anchor: "Assume RH. For large x we have"; formula `M(x) << sqrt(x) exp((log x)^{1/2}(log log x)^14)`.

Audit result:

- Source-closed: Soundararajan supplies an RH-conditional total summatory Mobius upper bound.
- Negative for current promotion: the theorem is far too coarse and global to control the shifted off-target residue aggregate in the Perron problem.
- Gap: if exact journal-page quotation is needed, retrieve the De Gruyter PDF; current audit has arXiv page quotation plus verified journal metadata only.

### Koyama Book Excerpt And Correspondence

Sources:

- Book excerpt: `/Users/za/Downloads/文書名 素数p001-288_念校【240801】 (1).pdf`, 3 PDF pages covering printed pp.44-49.
- Correspondence: `/Users/za/Downloads/Gmail - Weighted prime-bias behavior arising from Farey discrepancy.pdf`, single-page Gmail export of Apr. 2026 thread.

Verified anchors:

- Book printed pp.46-49: Taylor formula `-log(1-X)=X+sum_{k>=2} X^k/k`; inequality `sum_{k>=2} 1/(k p^k) <= 1/(2(p^2-p))`; summed bound `<= 1/2`.
- Apr.15 Koyama email: quoted anchor on `C(rho,chi)=L'(rho,chi)/zeta(2)`: "not a separate theorem".
- Apr.14 Koyama email: quoted anchor: "did not explicitly identify the universal constant".

Audit result:

- Source-closed: the book excerpt proves only the classical Euler/Mertens-style higher-prime-power convergence bound at `X=1/p`; it does not contain the EDRH mechanism at zeros.
- Source-closed: the correspondence treats `1/zeta(2)` as a plausible refinement/new numerical phenomenon, not a theorem already present in AK.
- Gap: the full Koyama book chapters defining EDRH were not retrieved; do not cite the book for a zero-level theorem from this excerpt.

## Perron Claim Audit

Local algebra:

At a simple zero `rho`, the expansion

```text
1/L(rho+w,chi) = 1/(L'(rho,chi)w) - L''(rho,chi)/(2L'(rho,chi)^2) + O(w)
```

gives the local residue of `K^w/(w L(rho+w,chi))` as

```text
log K/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2).
```

This is algebraically source-safe. It is not the global Perron theorem.

Global blocker:

Crossed off-target zeros of `L(s,chi)` contribute residues at `w=lambda-rho`. If an off-target zero has multiplicity `m>=2`, the residue has top degree `(log K)^(m-1)`. If all crossed zeros are simple, the still-missing term is

```text
Z_simple(K,T) = sum_{lambda != rho} K^(lambda-rho)/((lambda-rho)L'(lambda,chi)).
```

No retrieved source proves this is `o(log K)` for the needed shifted rectangle and truncation package.

## Email-Safe Replacement

Use:

```text
After rechecking the sources, I should keep the product constant conditional. Aoki-Koyama (2023), p.235, (1.4), gives an Euler-product normalization with denominator e^{m gamma}m! in its DRH formula and contains no zeta(2) constant. However, I have not found a source-closed shifted Perron theorem proving c_K(rho,chi)=log K/L'(rho,chi)+o(log K), nor a citation-closed lift of AK (1.4) to the arbitrary noncentral zero rho used here. Inoue's explicit formulas and Soundararajan's RH Mobius bound do not control the off-target shifted residue aggregate.
```

Avoid:

```text
E_K(rho,chi) log K -> L'(rho,chi)/e^gamma is an AK theorem at every simple noncentral zero.
The full NDC limit is proved.
D_K -> 1/zeta(2) is supported by Koyama's framework.
Inoue/Soundararajan close the Perron remainder.
```

## Do Not Promote Unless

- A primary source is retrieved for the noncentral Dirichlet Euler-product statement with `m = ord_{s=rho} L(s,chi)`, page/equation quote included, or the reduction from AK central DRH to this statement is written and checked.
- A shifted Perron theorem is retrieved/proved for `K^w/(w L(rho+w,chi))` with off-target residues, horizontal/vertical integrals, zero-avoiding heights, and truncation all `o(log K)` after the local residue.
- Multiple off-target zeros are either globally excluded by an explicit hypothesis/source or their higher-order residue aggregate is proved negligible.
- `1/zeta(2)` is presented only as empirical/new conjectural input unless a primary theorem actually derives it.
- The Koyama book is not cited beyond pp.44-49 unless the relevant EDRH pages are retrieved and quoted.

## Precise Source Gaps

1. Missing theorem: exact shifted Perron nonlocal remainder for `c_K(chi,rho)`.
2. Missing citation: noncentral Dirichlet analogue of Akatsuka/AK with the constant at arbitrary zero `rho`.
3. Missing source: full Koyama book EDRH section.
4. Optional cleanup: Soundararajan publisher PDF if journal-page theorem quotation, rather than arXiv-page quotation, is required.

## Verification Notes

Commands/sources used:

```text
curl -L https://www.numdam.org/item/10.5802/jtnb.1162.pdf
curl -L https://arxiv.org/pdf/0705.0723
python3 pypdf extraction on the six PDFs listed above
De Gruyter metadata page for doi:10.1515/CRELLE.2009.044
```

No code tests apply; this is a markdown literature audit.
