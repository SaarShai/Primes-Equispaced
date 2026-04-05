# Verification of Previous Fixes

- **(1) Sign Theorem reclassified from theorem to observation:** **Pass.** The main range-limited statement is now `\begin{observation}`. The surrounding prose still informally calls it the “Sign Theorem,” but the formal statement itself has been downgraded.
- **(2) Composite Healing downgraded from theorem to conjecture:** **Pass.** The statement is now `\begin{conjecture}[Composite Healing Rate]`.
- **(3) Spectroscope proposition downgraded to conjecture with Heuristic label:** **Pass.** The spectroscope claim is now `\begin{conjecture}[Spectral peaks, GRH]` with a following `Heuristic` paragraph.
- **(4) `D(1/p)` proof corrected with exact formula including `1/p` term:** **Pass.** Proposition `D(1/p)` now states and proves `1 + 1/p - |\F_{p-1}|/p`.
- **(5) Ingham / BCZ / Iwaniec--Kowalski references added:** **Pass.** All three bibliography entries are present. Ingham and BCZ are also cited in the body.
- **(6) Shift-Squared labeled conditional:** **Fail.** The theorem itself is now correctly labeled conditional at `main.tex:1537`, but the abstract still describes the same asymptotic as “an unconditional asymptotic” at `main.tex:96-98`.
- **(7) Dead bibliography placeholder removed:** **Pass.** I found no remaining placeholder-style bibliography marker in `main.tex`.
- **(8) Figure caption updated to 3829 primes:** **Fail.** The body text now says `3,829` qualifying primes at `main.tex:1960`, but Figure `\ref{fig:spectroscope}` still says `2,729` in the caption at `main.tex:2002-2005`.

# New Issues Found

- **Core sign convention inconsistency for `\Delta W`.** The abstract defines `\Delta W(N)=W(N)-W(N-1)` at `main.tex:58`, but the paper’s formal definition is `\Delta W(N)=W(N-1)-W(N)` at `main.tex:238-241`. This reverses the meaning of positive and negative steps.
- **Correlation ratio `R(p)` is defined inconsistently.** The abstract and Remark `rem:failure` use `R(p)=2\sum D\cdot\delta / \sum \delta^2` at `main.tex:71-73` and `main.tex:1666-1669`, while Remark `rem:corr-ratio` defines `R(p)=\sum D\cdot\delta / \sum \delta^2` at `main.tex:1782-1785`.
- **Internal contradiction on the sum over new-fraction displacements.** The prose at `main.tex:1129-1133` states `\sum_{k=1}^{p-1} D_{\F_p}(k/p)=-(p-1)/2`, but Proposition `New-fraction discrepancy sum` immediately states `\sum_{k=1}^{p-1} D_{\F_p}(k/p)=1` at `main.tex:1140-1142`.
- **Abstract still overstates the shift-squared result.** This is separate from the checklist item because it affects the submission-facing summary: `main.tex:96-98` still advertises an unconditional asymptotic, contrary to the theorem statement and proof caveat at `main.tex:1537-1556`.

# Remaining Concerns

- **Not-ready source-level contradictions remain in submission-facing text.** The `\Delta W` sign mismatch and `R(p)` normalization mismatch are not cosmetic; they affect interpretation of the main phenomenon and should be made globally consistent before submission.
- **There are still directly visible local source problems.** Examples: the Composite Healing evidence cites `Conjecture~\ref{conj:healing}` instead of the immediately preceding Composite Healing conjecture at `main.tex:1099-1100`; the spectroscope definition points to “Definition 2” even though Definition 2 is the shift `\delta`, not `R_2`, at `main.tex:1932-1933`; and there are leftover textual artifacts such as `both both` at `main.tex:1673-1674` and `see (see supplementary materials on GitHub)` at `main.tex:1799-1802`.
- **There is at least one additional internal mathematical overstatement in the prose.** The remark after Deficit Minimality states `\Delta W(q)=D_q(2)/q=(q^2-1)/24` at `main.tex:1463-1466`, which is not reconciled with the paper’s own normalized wobble notation and scale.
- **Minor consistency cleanup is still needed.** The abstract says `260+` Lean results at `main.tex:110`, while the body repeatedly says `258` at `main.tex:300`, `main.tex:1162`, and `main.tex:1352`; and the spectroscope statistics line uses `($p < 10^{-8}$, n=10 zeros)` at `main.tex:1953-1956`, which appears to be malformed significance notation.

# ArXiv Readiness Assessment

**Recommendation: No, not yet ready for arXiv submission.**

The prior downgrades are mostly in place, but two checklist items are still incomplete (conditional shift-squared wording and the spectroscope figure count), and there are remaining internal contradictions in the sign convention for `\Delta W`, the normalization of `R(p)`, and the stated sum over new-fraction displacements. These are source-verifiable issues in the manuscript text itself, not matters of external mathematical judgment. After those are corrected and the local notation/cross-reference cleanup is done, the paper would be much closer to arXiv-ready.
