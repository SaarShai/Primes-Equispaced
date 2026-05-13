# Mid-week update to Shin-ya (draft, not sent)

A short follow-up note prepared in advance for when the Phase-1
discrepancy reconciliation arrives (week of May 20). Designed to be
sent within 24h of his reply, summarising what has been done in the
interim and surfacing any decisions that need his input before
LaTeX integration.

The note is intentionally short. Three substantive items plus a
forward look.

---

**Subject:** Status update — week before integration

Dear Shin-ya,

Thanks again for your green light. A brief note on what I've done
in the meantime, all building on the technical/computational
section you've seen, none of it altering its claims.

**1. B_∞ identity verified at one more decade.** I extended the
PARI/GP cross-stack verification of the corrected $B_\infty$
identity to $K = 10^{8}$ on the four pairs (≈ 4 min wall-clock).
The clean-character pairs ($\chi_5$ and $\chi_{11}$) now give
residual ratios $3.7$ and $4.3$ from $K = 10^7$ to $K = 10^8$,
bracketing the predicted $\sqrt{10} \approx 3.16$ of the
$K^{-1/2}/\log K$ decay rate (Akatsuka 2013 eq.~(2.5)); the
$\chi_{-4}$ pairs continue to show the slower $\sim 1.15$ ratio per
decade attributable to the bad-prime $p = 2$ contribution to
$\mathrm{BPC}_1$. Across the two decades $K \in
[2 \cdot 10^{6}, 10^{8}]$, the empirical decay envelope is now
verified at three scales. §X.5.4 in the section draft has been
updated.

**2. Lean inventory tightened.** Eight Lean files in
`formal-conjectures/` now compile under Lean 4.28.0 with **two
`sorry`s** remaining (down from five at the time of my first email);
the two remaining are both the headline Dirichlet Polynomial
Avoidance Conjecture itself, diagnostically LI-class. Seven of nine
files are now fully proved. `FareySignPattern.lean` (the file
recording the $p = 237{,}733$ and $p = 243{,}799$ falsifications) is
now closed under explicit named hypotheses naming the numerical
witnesses; the no-`axiom` convention is preserved throughout.

**3. Supplementary drafts ready for your review.** A sketch
Introduction (≈ 900 words, 5 subsections) and three Abstract
variants are now in the bundle as discussion documents. Both are
framed as starting points to react to, not committed prose. The
Introduction has placeholder cues for your authoritative framing of
the Dominance-of-$-1$ programme; the Abstract drafts can be tuned to
whichever venue you prefer.

**Forward look.** I'm ready to begin LaTeX conversion of the
integrated full paper as soon as you signal which discrepancies
resolved. The whole §X bundle (cover note + section + appendices +
Lean inventory + supporting notes) is in
`handoff-2026-05-12-paper-prep/recent/`; the typeset PDF (17 pages)
builds reproducibly via `tectonic paper.tex` from the source.

Best,
Saar

---

## Send-decision criteria

Default: do NOT send this proactively. Send only if Koyama's
discrepancy report arrives ON or BEFORE May 20 with material that
materially changes §X.5.1. If he comes back asking "should we keep
going?", reply with this draft as the substantive answer.

If his reply on May 20 instead just confirms a couple of cells and
declines to flag a major change, the note above over-communicates;
strip items 1–3 to the headline bullets and skip the LaTeX-status
paragraph.

## Variants if he reports a substantive cell flip

If Koyama's reply changes the Table-5 $N=11, a=10$ cell from
$71{,}711$ to $11{,}503$ (i.e., agrees with our value), §X.5.1
should be updated to:

> The qualitative dominance signal at $x = 1.3 \cdot 10^{13}$ is
> reproduced for $N = 8$ (strictly) and for $N = 19$ (top group);
> for $N = 11$, the corrected value $a = 10$ shifts $-1$'s rank
> from 2nd to 3rd of 5 non-residues, *out of the strict top group
> at this checkpoint* — consistent with the Aoki–Koyama framework
> if one allows for a transient low-zero deflection like the one
> Koyama identifies for $N = 19$.

If he instead reaffirms his $71{,}711$, §X.5.1 stays as-is and we
note "joint reconciliation pending" as the entry for that cell.
