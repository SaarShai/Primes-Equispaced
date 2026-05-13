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

    # Citation substitutions: convert in-text author-year mentions into
    # \cite{...} calls so the BibTeX bibliography renders.
    #
    # Order matters: longest / most specific patterns first so we don't
    # double-cite.
    cite_patterns = [
        # Aoki--Koyama 2023, eq. (1.4) p. 235
        (r"Aoki--Koyama \(2023, \\emph\{J\. Number Theory\} \\textbf\{245\}, eq\. \(1\.4\), p\. 235\)",
         r"Aoki--Koyama~\\cite[eq.~(1.4), p.~235]{AokiKoyama2023}"),
        (r"Aoki--Koyama \(2023, Proposition 2\.1, p\. 244\)",
         r"Aoki--Koyama~\\cite[Proposition~2.1, p.~244]{AokiKoyama2023}"),
        (r"Aoki--Koyama \(2023\)", r"Aoki--Koyama~\\cite{AokiKoyama2023}"),
        # Akatsuka 2013, Lemma 2.1 / eq. (2.5) — several phrasings
        (r"Akatsuka \(2013, Lemma 2\.1 / eq\. \(2\.5\)\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{AkatsukaH2013EulerProduct}"),
        (r"Akatsuka \(2013\) Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{AkatsukaH2013EulerProduct}"),
        (r"Akatsuka 2013 Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{AkatsukaH2013EulerProduct}"),
        (r"Akatsuka 2013, eq\. \(2\.5\)",
         r"Akatsuka~\\cite[eq.~(2.5)]{AkatsukaH2013EulerProduct}"),
        (r"Akatsuka 2013 eq\. \(2\.5\)",
         r"Akatsuka~\\cite[eq.~(2.5)]{AkatsukaH2013EulerProduct}"),
        (r"\(Akatsuka \(2013\),[^)]*The Euler product[^)]*Lemma 2\.1 and equation \(2\.5\)\)",
         r"(\\cite[Lemma~2.1 \\& eq.~(2.5)]{AkatsukaH2013EulerProduct})"),
        (r"Akatsuka \(2013\)", r"Akatsuka~\\cite{AkatsukaH2013EulerProduct}"),
        (r"\bAkatsuka 2013\b", r"\\cite{AkatsukaH2013EulerProduct}"),
        # Inoue 2021
        (r"Inoue \(2021, Theorem 1\)", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"Inoue \(2021\) Theorem 1", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"\bInoue 2021 Theorem 1\b", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"Inoue \(2021\)", r"Inoue~\\cite{Inoue2021}"),
        (r"\bInoue 2021\b", r"\\cite{Inoue2021}"),
        # Soundararajan 2009 Theorem 1
        (r"Soundararajan \(2009\)[^,.]*Theorem 1", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"Soundararajan \(2009\) Theorem 1", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"\bSoundararajan 2009 Theorem 1\b", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"Soundararajan \(2009\)", r"Soundararajan~\\cite{Soundararajan2009}"),
        (r"\bSoundararajan 2009\b", r"\\cite{Soundararajan2009}"),
        # Hardy & Wright
        (r"Hardy(?: \\&|--| and ) ?Wright[^,.]*Theorem 304", r"Hardy--Wright~\\cite[Theorem~304]{HardyWright2008}"),
        (r"Hardy(?: \\&|--| and ) ?Wright Theorem 304", r"Hardy--Wright~\\cite[Theorem~304]{HardyWright2008}"),
        # Pólya 1913
        (r"P\\'olya \(1913\)", r"P\\'olya~\\cite{Polya1913}"),
        (r"Pólya \(1913\)", r"Pólya~\\cite{Polya1913}"),
        (r"\bPólya 1913\b", r"\\cite{Polya1913}"),
        (r"\bP\\'olya 1913\b", r"\\cite{Polya1913}"),
        # Ng 2004
        (r"\bNg 2004\b", r"Ng~\\cite{Ng2004}"),
        (r"Ng \(2004\)", r"Ng~\\cite{Ng2004}"),
        # Titchmarsh §3.11
        (r"Titchmarsh[^,.]*Theorem 3\.11", r"Titchmarsh~\\cite[Theorem~3.11]{Titchmarsh1986RZF}"),
        (r"Titchmarsh[^,.]*\\S\\,3\.11", r"Titchmarsh~\\cite[§3.11]{Titchmarsh1986RZF}"),
        # Montgomery--Vaughan Theorem 9.4
        (r"Montgomery--Vaughan[^,.]*Theorem 9\.4(?: / Corollary 9\.5)?",
         r"Montgomery--Vaughan~\\cite[Theorem~9.4]{MontgomeryVaughan2007}"),
        (r"Montgomery--Vaughan Thm 9\.4", r"Montgomery--Vaughan~\\cite[Theorem~9.4]{MontgomeryVaughan2007}"),
        # Tenenbaum
        (r"Tenenbaum,[^,.]*Introduction to Analytic and Probabilistic Number Theory,?\s*Chapter II\.5",
         r"Tenenbaum~\\cite[Chapter~II.5]{Tenenbaum2015}"),
        # Davenport
        (r"Davenport[^,.]*MNT[^,.]*", r"Davenport~\\cite{Davenport2000MultiplicativeNumberTheory}"),
    ]
    for pat, repl in cite_patterns:
        text = re.sub(pat, repl, text)

    # Remove the §X-level "References (section)" block from the main
    # section — the BibTeX-rendered bibliography replaces it.
    if kind == "section":
        text = re.sub(
            r"\\subsection\{References \(section\)\}.*?(?=\\section|\Z)",
            "",
            text, flags=re.DOTALL,
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
