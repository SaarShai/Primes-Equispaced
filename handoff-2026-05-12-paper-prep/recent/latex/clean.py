#!/usr/bin/env python3
"""Post-process pandoc-generated LaTeX for the Saar-Koyama §X bundle.

Fixes the common pandoc-→-LaTeX artefacts in the three raw files
(section_raw.tex, appendix_A_raw.tex, appendix_B_raw.tex) and emits
section_X.tex, appendix_A.tex, appendix_B.tex ready for inclusion.

Idempotent.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

def clean(text: str, kind: str) -> str:
    """kind: 'section' | 'appendix-A' | 'appendix-B'."""
    # 1. Pandoc auto-labels off section headers are noisy; strip them.
    text = re.sub(
        r"\\(section|subsection|subsubsection|paragraph)\{([^}]*)\}\\label\{[^}]*\}",
        r"\\\1{\2}",
        text,
    )

    # 2. Strip the leading "§X. " / "§X.N " markdown crud out of section titles.
    text = re.sub(r"\\section\{§X\. ", r"\\section{", text)
    text = re.sub(r"\\subsection\{X\.(\d+) ", r"\\subsection{X.\1\\quad ", text)
    text = re.sub(r"\\subsubsection\{X\.(\d+\.\d+) ", r"\\subsubsection{X.\1\\quad ", text)

    # 3. Pandoc emits \begin{center}\rule{...} for `---` horizontal rules.
    #    These were markdown section separators; drop them.
    text = re.sub(
        r"\\begin\{center\}\\rule\{[^}]*\}\{[^}]*\}\\end\{center\}\n*",
        "",
        text,
    )

    # 4. Pandoc renders `> *…*` blockquotes as quote environments. Keep
    #    those for the Aoki-Koyama verbatim quote; this is fine.

    # 5. Inline math: pandoc uses \(...\). Both work in LaTeX; leave as-is.

    # 6. Per-appendix title fix.
    if kind == "appendix-A":
        text = re.sub(
            r"\\section\{Appendix A[^}]*\}",
            r"\\section{Full proof of Theorem X.4.1 ($B_\\infty$ identity)}",
            text,
        )
    elif kind == "appendix-B":
        text = re.sub(
            r"\\section\{Appendix B[^}]*\}",
            r"\\section{Full proof of Theorem X.4.2 ($c_K$ leading + subleading identity)}",
            text,
        )

    # 7. Map markdown's A.1, A.2, … and B.1, B.2, … to \subsection.
    #    Pandoc already does this via ## → \subsection, so no extra work.

    # 8. Pandoc sometimes emits `\tightlist` (a memoir-class macro). Drop it
    #    (article class doesn't define it).
    text = text.replace("\\tightlist\n", "")

    # 9. `>` blockquote rendered as `\begin{quote}` — fine; keep.

    # 10. "Q:Perron", "Q:DPAC" etc. used in §X.7 as quasi-labels. Pandoc
    #     leaves them as plain text — that's fine.

    # 11. Pandoc uses `pandocbounded` graphics macros only for images; we have none.

    # 12. Strip trailing whitespace on lines.
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"

    # 13. Collapse triple+ blank lines to double.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


JOBS = [
    ("section_raw.tex", "section_X.tex", "section"),
    ("appendix_A_raw.tex", "appendix_A.tex", "appendix-A"),
    ("appendix_B_raw.tex", "appendix_B.tex", "appendix-B"),
]

for src, dst, kind in JOBS:
    raw = (HERE / src).read_text()
    out = clean(raw, kind)
    (HERE / dst).write_text(out)
    print(f"{src:>22}  →  {dst}  ({len(out.splitlines())} lines)")
