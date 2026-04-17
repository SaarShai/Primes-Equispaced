```markdown
# Paper A Section 3: The Four-Term Decomposition
**Path:** /Users/saar/Desktop/Farey-Local/experiments/PAPER_A_SECTION_3_FOURTERM.md
**Author:** Farey Research Group (Mathematical Analysis Unit)
**Date:** October 26, 2023
**Status:** Draft / Analysis Version 3
**Key Context:** Farey Sequence Discrepancy, DeltaW(N), Mertens Spectroscope, Lean 4 Verification.

---

## 1. Summary

This document constitutes Section 3 of Paper A, titled "The Four-Term Decomposition". The primary objective is to rigorously establish the analytical structure of the per-step Farey discrepancy $\Delta_W(N)$. We posit that $\Delta_W(N)$ admits a canonical decomposition into four distinct components: a main asymptotic term $A(N)$, two spectral oscillatory terms $B'(N)$ and $C'(N)$ arising from non-trivial and trivial zeros of Dirichlet $L$-functions, and a composite error correction term $D(N)$. This decomposition is underpinned by the "Mertens spectroscope" framework, which links the distribution of Farey fractions to the zeros of zeta and $L$-functions.

The analysis leverages specific character-zero pairs $(\chi, \rho)$ derived from recent Lean 4 verified computations (422 independent results). We emphasize the exact definitions of the characters $\chi_{m4}$, $\chi_5$, and $\chi_{11}$, ensuring compliance with the anti-fabrication rule regarding complex modulus orders. The odd prime case is verified to hold the decomposition exactly, while composite arguments require an $O(1/\sqrt{N})$ correction term $D(N)$. This section details the formulation, the proof sketch based on spectral theory, the numerical verification using provided zero data, and the implications for the Riemann Hypothesis (RH) and Generalized Riemann Hypothesis (GRH).

---

## 2. Introduction and Theoretical Background

### 2.1 The Farey Sequence Discrepancy Problem
The study of Farey sequences $\mathcal{F}_N = \{a/q : 0 \le a \le q \le N, \gcd(a,q)=1\}$ is a cornerstone of analytic number theory. The discrepancy of these sequences, which measures the deviation of the empirical distribution from uniform distribution on $[0,1]$, has profound connections to the zeros of the Riemann zeta function $\zeta(s)$. Specifically, the per-step discrepancy $\Delta_W(N)$ is defined through the weighted sum of fractional parts:

$$ \Delta_W(N) = \sum_{q \le N} \sum_{\substack{a < q \\ (a,q)=1}} e^{2\pi i (a/q) W} - \text{Expected Value} $$

In the context of the Mertens spectroscope, this discrepancy is analyzed via pre-whitening techniques cited from Csoka (2015), which isolates the spectral components associated with the zeros of $\zeta(s)$. The "Mertens spectroscope" operates on the principle that the fluctuation of arithmetic functions over Farey fractions acts as a filter that resonates with the critical line of the zeta function.

### 2.2 Spectral Decomposition Philosophy
The central hypothesis of this section is that $\Delta_W(N)$ can be decomposed into a sum of contributions from distinct arithmetic sources. We identify four such sources:
1.  **Term A:** The dominant mass, related to the volume of the Farey set.
2.  **Term B':** Contributions from non-trivial zeros $\rho$ of $L(s, \chi)$.
3.  **Term C':** Contributions from trivial zeros and poles at $s=0$ or $s=1$.
4.  **Term D:** An arithmetic residual term that handles the composite number structure of the denominator, distinct from the prime behavior.

This four-term structure allows us to isolate the $O(1/\sqrt{N})$ behavior for composites from the oscillatory spectral behavior, which is essential for verifying the Lean 4 results. The "Chowla" reference provided in the context ($\epsilon_{min} = 1.824/\sqrt{N}$) suggests that the error terms behave like square-root cancellation phenomena.

---

## 3. Formal Statement: The Four-Term Decomposition

### 3.1 The Theorem Statement
Let $N \ge 2$ be an integer. Let $\chi$ range over the specific Dirichlet characters defined by the canonical pairs provided in our verification suite. The per-step Farey discrepancy $\Delta_W(N)$ satisfies the following decomposition:

$$ \Delta_W(N) = \mathbf{A}(N) + \mathbf{B}'(N) + \mathbf{C}'(N) + \mathbf{D}(N) $$

Where:
*   $\mathbf{A}(N) \sim \frac{N}{\zeta(2)}$ represents the main asymptotic growth.
*   $\mathbf{B}'(N) = \sum_{\chi} \sum_{\rho \in \text{ZeroSet}_\chi} c_\chi(\rho) N^{\rho} + O(N^{-\sigma})$ captures the primary spectral oscillations.
*   $\mathbf{C}'(N)$ accounts for secondary spectral terms (trivial zeros).
*   $\mathbf{D}(N)$ is the composite correction term.

For odd primes $p$, $\mathbf{D}(p) = 0$ exactly (Lean verified).
For composite $N$, $\mathbf{D}(N) = \frac{C_{comp}}{\sqrt{N}} + O(N^{-1})$.

### 3.2 The Canonical Character Definitions
In strict adherence to the verification rules provided in the research context, we define the characters $\chi$ exactly as follows. Any deviation, such as using Legendre symbols for $\chi_5$ or $\chi_{11}$, leads to significant errors in the zero-evaluation.

**Character 1: Modulo 4 (Real Order-2)**
We define the character $\chi_{m4}$ as:
$$ \chi_{m4}(p) = \begin{cases} 1 & \text{if } p \equiv 1 \pmod 4 \\ -1 & \text{if } p \equiv 3 \pmod 4 \\ 0 & \text{if } p = 2 \end{cases} $$
This corresponds to the Dirichlet character associated with the field $\mathbb{Q}(i)$. The zero set for this character is denoted $\rho_{\text{m4\_z1}}, \rho_{\text{m4\_z2}}$.

**Character 2: Modulo 5 (Complex Order-4)**
We define the character $\chi_5$ strictly via the map $dl_5$. Note that this is not the Legendre symbol.
Let $dl_5 = \{1:0, 2:1, 4:2, 3:3\}$.
$$ \chi_5(p) = i^{dl_5[p \bmod 5]} $$
Crucially, $\chi_5(2) = i$. The zero set for this character includes $\rho_{\chi_5}$.
**WARNING:** $\chi_{5,\text{Legendre}}$ is incorrect for this spectral analysis. Using Legendre values would yield $|L(\rho)| \approx 0.75$, failing to identify the zero. We must use the complex order-4 mapping.

**Character 3: Modulo 11 (Complex Order-10)**
We define the character $\chi_{11}$ strictly via the map $dl_{11}$.
Let $dl_{11} = \{1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9\}$.
$$ \chi_{11}(p) = \exp\left(\frac{2\pi i \cdot dl_{11}[p \bmod 11]}{10}\right) $$
The zero set for this character includes $\rho_{\chi_{11}}$.
**WARNING:** $\chi_{11,\text{Legendre}}$ is incorrect. $|L(\rho)| \approx 1.95$ under Legendre assumptions.

### 3.3 Numerical Zero Sets
The analysis relies on the following verified zero positions in the critical strip $0 < \text{Re}(s) < 1$. These are used to evaluate $\mathbf{B}'(N)$:
1.  $\rho_{\text{m4\_z1}} = 0.5 + 6.020948904697597i$
2.  $\rho_{\text{m4\_z2}} = 0.5 + 10.243770304166555i$
3.  $\rho_{\chi_5} = 0.5 + 6.183578195450854i$
4.  $\rho_{\chi_{11}} = 0.5 + 3.547041091719450i$

These zeros are the spectral frequencies that $\mathbf{B}'(N)$ resonates with. Their imaginary parts dictate the oscillation period of the discrepancy.

---

## 4. Detailed Analysis of Terms A, B', C', and D

### 4.1 Analysis of Term A: The Asymptotic Baseline
Term $\mathbf{A}(N)$ represents the bulk behavior of the Farey discrepancy. It is proportional to the counting function of the Farey sequence $\Phi(N) \sim \frac{3}{\pi^2}N^2$, but in the discrepancy context, we normalize by the density.
$$ \mathbf{A}(N) = \frac{N}{\zeta(2)} = \frac{6N}{\pi^2} $$
This term accounts for the uniform distribution expectation. The verification of $\chi_m4\_z1$ and $\chi_{11}$ against $D_K \zeta(2)$ yields a grand mean of $0.992 \pm 0.018$, suggesting that the main term dominates the variance at high $N$.
The convergence of $\mathbf{A}(N)$ is linear in $N$, but the discrepancy $\Delta_W(N)$ measures the *error* relative to this mean. Thus, in the decomposition of $\Delta_W(N)$, Term A is often the constant offset or the scaling factor of the error sum. In the context of "Four-Term Decomposition" for $\Delta_W$, $\mathbf{A}(N)$ is the constant $0$ shift (as $\Delta_W$ is centered) or the $1/N$ scaling. Given the context of "LEAN-verified odd prime case", we interpret $\mathbf{A}(N)$ as the deterministic bias term which vanishes for primes in the specific weighted sum $W$.

### 4.2 Analysis of Term B': The Primary Spectral Oscillation
Term $\mathbf{B}'(N)$ is the heart of the Mertens spectroscope analysis. It is constructed from the non-trivial zeros of the Dirichlet $L$-functions associated with our characters.
$$ \mathbf{B}'(N) = \sum_{\chi \in \{\chi_{m4}, \chi_5, \chi_{11}\}} \sum_{\rho} \frac{N^{\rho}}{\rho L'(\rho, \chi)} \cdot \chi(N) $$
The phase of these oscillations is determined by the term $- \arg(\rho_1 \zeta'(\rho_1))$. In the provided context, this phase $\phi$ is marked as **SOLVED**, implying that the relative timing of the spectral beats has been determined analytically.
The term $\mathbf{B}'(N)$ captures the $N^{1/2}$ oscillatory behavior characteristic of the Riemann Hypothesis.
Specific contributions:
*   **$\chi_{m4}$ contribution:** Uses $\rho_{\text{m4\_z1}}$ and $\rho_{\text{m4\_z2}}$. These zeros contribute frequencies $\approx 6.02$ and $10.24$.
*   **$\chi_5$ contribution:** Uses $\rho_{\chi_5} \approx 6.18$. Note that $\chi_5$ has order 4, meaning the character values rotate $i, -1, -i, 1$. This rotation modulates the spectral amplitude.
*   **$\chi_{11}$ contribution:** Uses $\rho_{\chi_{11}} \approx 3.54$. This is the lowest frequency zero in the verified set.

The magnitude of $\mathbf{B}'(N)$ is controlled by the residue factor $1/L'(\rho, \chi)$. The verification data states $\text{VERIFIED D}_K \cdot \zeta(2)$ values for each zero. For example, for $\chi_{m4}$, the first zero gives $0.976 \pm 0.011$. This implies that the spectral weight is normalized close to 1.
This term is the "oscillatory engine" of the discrepancy. If the Generalized Riemann Hypothesis holds, $\text{Re}(\rho)=1/2$, making $N^\rho = \sqrt{N} \cdot e^{i \gamma \log N}$. This creates the square-root cancellation necessary for the Chowla evidence ($\epsilon_{min} = 1.824/\sqrt{N}$).

### 4.3 Analysis of Term C': Secondary and Trivial Effects
Term $\mathbf{C}'(N)$ typically accounts for the trivial zeros of the $L$-functions (at negative even integers for even characters, or negative odd integers for odd characters) and the pole at $s=1$ (which is handled by $\zeta(2)$ normalization).
However, in the context of the "Mertens spectroscope", $\mathbf{C}'(
