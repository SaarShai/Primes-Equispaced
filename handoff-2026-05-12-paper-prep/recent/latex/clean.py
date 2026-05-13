#!/usr/bin/env python3
"""Build the LaTeX section + appendices from the markdown source.

Pipeline:
  1. Read each markdown source.
  2. Preprocess: convert LaTeX-style `\\[ ... \\]` display-math blocks
     to `$$ ... $$`.
  3. Pipe through pandoc to LaTeX.
  4. Post-process: strip pandoc auto-labels, drop horizontal-rule
     artefacts, fix section titles, fix encoding issues, etc.

Idempotent.
"""
from __future__ import annotations
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent
PANDOC = "/Users/za/miniforge3/bin/pandoc"


def preprocess_markdown(md: str) -> str:
    md = re.sub(r"^\\\[[ \t]*\n", "$$\n", md, flags=re.MULTILINE)
    md = re.sub(r"^\\\][ \t]*\n", "$$\n\n", md, flags=re.MULTILINE)
    return md


def run_pandoc(md: str) -> str:
    return subprocess.run(
        [PANDOC, "--from", "markdown", "--to", "latex", "--wrap=preserve"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout


def postprocess_latex(text: str, kind: str) -> str:
    text = re.sub(
        r"\\(section|subsection|subsubsection|paragraph)\{([^}]*)\}\\label\{[^}]*\}",
        r"\\\1{\2}", text,
    )
    text = re.sub(r"\\section\{§X\. ", r"\\section{", text)
    text = re.sub(r"\\subsection\{X\.\d+ ", r"\\subsection{", text)
    text = re.sub(r"\\subsubsection\{X\.\d+\.\d+ ", r"\\subsubsection{", text)
    text = re.sub(r"\\subsection\{[AB]\.\d+ ", r"\\subsection{", text)
    text = re.sub(r"\\subsubsection\{[AB]\.\d+\.\d+ ", r"\\subsubsection{", text)
    text = re.sub(
        r"\\begin\{center\}\\rule\{[^}]*\}\{[^}]*\}\\end\{center\}\n*", "", text,
    )
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
    text = text.replace("\\tightlist\n", "")

    # § → \S\, : T1 fontenc maps 0xA7 to ğ; use the textcomp macro.
    text = text.replace("§", "\\S\\,")

    # Pandoc emits \#\#\# Header when a level-3 heading follows display
    # math with no blank line. Recover as a \subsubsection.
    def _subsub(m):
        title = m.group(1)
        title = re.sub(r"^X\.\d+\.\d+ ", "", title)
        title = re.sub(r"^[AB]\.\d+\.\d+ ", "", title)
        return r"\subsubsection{" + title + r"}"
    text = re.sub(r"^\\#\\#\\# ([^\n]+)$", _subsub, text, flags=re.MULTILINE)

    # Broken cross-reference: eq:W2 referenced the OLS regression we
    # removed when compressing §X.5.5. Replace with textual cue.
    text = text.replace(
        r"(\ref{eq:W2})",
        r"(the rank-vs-$\log N$ regression of \S\,X.5.5)",
    )

    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


JOBS = [
    ("SECTION_DRAFT_2026-05-12.md", "section_X.tex", "section"),
    ("APPENDIX_A_BINFTY_PROOF.md", "appendix_A.tex", "appendix-A"),
    ("APPENDIX_B_CK_SUBLEADING_PROOF.md", "appendix_B.tex", "appendix-B"),
]

for src, dst, kind in JOBS:
    md = (SRC / src).read_text()
    md = preprocess_markdown(md)
    latex = run_pandoc(md)
    latex = postprocess_latex(latex, kind)
    (HERE / dst).write_text(latex)
    print(f"{src:>38}  →  {dst}  ({len(latex.splitlines())} lines)")
