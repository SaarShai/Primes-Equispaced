# Adversarial Referee Report

## Objection 1 — Fatal: Claim 1's "unconditional" tag is fraudulent
**Precise objection:** The sum $\sum_p \chi(p)^{2k} p^{-2k\rho}$ for $k=2$ converges only conditionally on $\operatorname{Re}(\rho)=1/2$ (boundary of the half-plane of absolute convergence). Akatsuka-type conditional convergence of prime-power Dirichlet series on $\operatorname{Re}(s)=1$ requires a zero-free region or GRH-type input to control partial sums. The manuscript labels this "unconditional given simple zero" but a simple zero alone does not supply the needed partial-sum bound for $\sum_p \chi(p)^4 p^{-1-4i\tau}$.

**Fix needed:** Either (a) prove an unconditional partial-sum estimate $|\sum_{p\le x}\chi(p)^4 p^{-1-4i\tau}| = O(1)$ using only the simple-zero hypothesis (likely impossible without GRH), or (b) honestly relabel Claim 1 as conditional on GRH for $L(s,\chi^4)$, or (c) truncate at $k=2$ and absorb the remainder into an explicit error with a proven bound.

**Severity:** Fatal — the word "unconditional" is the load-bearing marketing claim.

---

## Objection 2 — Serious: Claim 2's $o(1)$ conceals the off-target zero aggregate
**Precise objection:** Inoue 2021's truncated explicit formula expresses $\sum_{n\le K}\mu(n)\chi(n)n^{-\rho}$ as a main term plus a sum over non-trivial zeros $\rho'\ne\rho$ of $L(s,\chi)$. The manuscript writes this as $o(1)$, but without a zero-density or repulsion estimate, the aggregate $\sum_{\rho'\ne\rho} K^{\rho'-\rho}/(\rho'-\rho)$ is not $o(1)$ unconditionally — it is $o(1)$ only under DRH with sufficient zero-spacing. The label "unconditional identity" is therefore misleading.

**Fix needed:** State explicitly that the $o(1)$ absorbs $\sum_{\rho'\ne\rho}(\ldots)$ and that bounding this requires DRH or a zero-density hypothesis. Remove "unconditional" or add the hypothesis.

**Severity:** Serious — the $o(1)$ is doing all the hard analytic work and is being hand-waved.

---

## Objection 3 — Serious: $e^{-\gamma}$ vs $1/\zeta(2)$ is likely a normalization artifact
**Precise objection:** Aoki-Koyama (1.4) normalizes $E_K$ with a specific Mertens-type constant. If the manuscript's $E_K$ differs by a factor of $\zeta(2)e^{-\gamma}$ in normalization (e.g., including/excluding the $p=2$ Euler factor or using a different sieve weight), then $e^{-\gamma}$ and $1/\zeta(2)$ are the same identity viewed through different normalizations. The "discrepancy" may be illusory.

**Fix needed:** Write the *exact* definition of $E_K$ used, compare term-by-term with Aoki-Koyama's $E_K$, and show the ratio is $\zeta(2)e^{-\gamma}\cdot e^{\gamma}= \zeta(2)$ or $1$, proving the claims are equivalent or genuinely different.

**Severity:** Serious — if this is a normalization swap, the entire "novelty" collapses.

---

## Objection 4 — Serious: Shifted Perron off-target obstruction is stated as no-go but is merely unproven
**Precise objection:** The manuscript DEFERs Claim 4 by asserting the off-target zero residue aggregate "is not controlled by target-zero simplicity + DRH alone." This is an assertion of impossibility, not a proof. In practice, shifted Perron with a smooth weight (e.g., $e^{-n/K}$) combined with DRH *does* give $O(K^{-1/2+\epsilon})$ remainders via standard zero-density arguments. The DEFER is a gap masquerading as a theorem.

**Fix needed:** Either prove the obstruction rigorously (showing a specific barrier), or retract the DEFER and supply the standard shifted-Perron + DRH remainder estimate.

**Severity:** Serious — Claim 4 is the headline result and is currently unproved.

---

## Objection 5 — Cosmetic/Moderate: Numerical scale does not support "verified at $10^{13}$"
**Precise objection:** The table shows $K=2\times10^6$ with 50-digit precision. No computation at $K=10^{13}$ is presented or referenced. If the manuscript anywhere claims verification at $10^{13}$, this is unsupported.

**Fix needed:** Remove any $10^{13}$ claim, or supply the computation.

**Severity:** Cosmetic if removed; fatal if left as a credibility anchor.

---

## Objection 6 — Cosmetic: Convergence rate claim is circular
**Precise objection:** Stating "convergence rate consistent with $K^{-1/2}/\log K$ boundary-line conditional convergence for the $k=2$ prime sum" is a *fit*, not a *proof*. Fitting a power law to 4 data points at a single scale proves nothing about the analytic structure.

**Fix needed:** Either prove the rate or state it as a conjecture.

**Severity:** Cosmetic but intellectually dishonest if presented as evidence.

---

**Over-promotion flag:** Claims 1 and 2 are both labeled "unconditional" but each secretly depends on conditional convergence or zero-aggregate bounds that require GRH/DRH. This is the central over-promotion.
