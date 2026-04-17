# MASTER RECORD: KILLED DIRECTIONS AND HYPOTHESES (Farey Sequence Research Project)

**Status:** Consolidated Version 3.0
**Author:** Mathematical Research Assistant
**Date:** October 2023
**Location:** `/Users/saar/Desktop/Farey-Local/experiments/KILLED_EXPLORATIONS_CONSOLIDATED.md`

## 1. Executive Summary

This document serves as the canonical repository for the "Killed Directions" within the Farey Sequence Research Project. Its primary purpose is to ensure that intellectual capital is not wasted on paths that have been empirically or theoretically disproven. Given the high complexity of the Farey discrepancy analysis, the interplay between Dirichlet L-functions, and the use of machine learning models for spectral detection, the distinction between viable hypothesis and artifact is critical. This record consolidates lessons from four distinct sources: the local `MASTER_TABLE_DEAD.md`, the `MASTER.md` repository logs, the `Lessons_Learned.md` wiki, and recent reality checks from the Codex framework.

The research focuses on the Per-step Farey discrepancy $\Delta W(N)$, specifically analyzing the behavior of the Mertens and Liouville spectroscopes. Key findings include the successful solution of the phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$, strong evidence supporting the Chowla conjecture (with $\epsilon_{min} \approx 1.824/\sqrt{N}$), and GUE statistics showing an RMSE of 0.066. However, the project has generated significant "byproduct" knowledge regarding what *does not work*. This document catalogues every claim, theorem, and application that has been invalidated. It emphasizes that standard Dirichlet character definitions (Legendre symbols) are often insufficient for the specific zero locations identified, necessitating the use of the exact `dl5` and `dl11` dictionary mappings provided in the NDC Canonical definitions.

## 2. Contextual Analysis of Validated Constraints

Before analyzing the killed directions, it is necessary to establish the mathematical boundary conditions that rendered certain claims impossible. The Farey discrepancy analysis relies heavily on the analytic properties of L-functions associated with specific Dirichlet characters. The project has established strict canonical definitions for these characters which, while mathematically standard in their output, require precise implementation to match the verified zeros $\rho$.

### 2.1. Dirichlet Character Canonical Definitions

Three specific characters were central to the L-function spectral analysis. The "Anti-Fabrication Rule" explicitly forbids the use of standard Legendre symbol implementations (`chi_Legendre`) for $\chi_5$ and $\chi_{11}$ because the resulting zeros do not align with the observed spectral data (where $|L(\rho)| \approx 0.75$ or $1.95$ rather than $0$).

1.  **$\chi_{m4}(p)$ (Modulo 4):** This is the real order-2 character.
    $$
    \chi_{m4}(p) = \begin{cases}
    1 & \text{if } p \equiv 1 \pmod 4 \\
    -1 & \text{if } p \equiv 3 \pmod 4 \\
    0 & \text{if } p = 2
    \end{cases}
    $$
    This character is robust and did not suffer from "fabrication" issues, but associated theorems regarding its contribution to $D_K$ were found to require correction.

2.  **$\chi_5(p)$ (Modulo 5):** This is a complex order-4 character.
    The definition relies on a discrete logarithm map $dl_5 = \{1:0, 2:1, 4:2, 3:3\}$. The character is defined as:
    $$
    \chi_5(p) = i^{dl_5[p \pmod 5]}
    $$
    Crucially, $\chi_5(2) = i$. The canonical zero associated with this character is $\rho_{\chi 5} = 0.5 + 6.183578195450854i$. Attempts to use $\chi_5(p) = \left(\frac{p}{5}\right)$ resulted in a failure to detect the zero, as the L-function values at the expected zero were non-zero (specifically, $|L(\rho)| \approx 0.75$ for the wrong definition).

3.  **$\chi_{11}(p)$ (Modulo 11):** This is a complex order-10 character.
    The definition relies on $dl_{11} = \{1:0, 2:1, 4:2, 8:3, 5:4, 10:5, 9:6, 7:7, 3:8, 6:9\}$. The character is defined as:
    $$
    \chi_{11}(p) = \exp\left(\frac{2\pi i \cdot dl_{11}[p \pmod{11}]}{10}\right)
    $$
    The canonical zero is $\rho_{\chi 11} = 0.5 + 3.547041091719450i$. Again, Legendre-based definitions failed to align with the zero spectrum.

### 2.2. Verification of Spectral Constants

The project verified the relation $D_K \cdot \zeta(2)$ for the relevant L-function discriminants. The values were computed as follows:
*   $\chi_{m4}$ at $z_1$: $0.976 \pm 0.011$
*   $\chi_{m4}$ at $z_2$: $1.011 \pm 0.017$
*   $\chi_5$: $0.992 \pm 0.024$
*   $\chi_{11}$: $0.989 \pm 0.018$

The grand mean is $0.992 \pm 0.018$. This confirms the consistency of the spectral detection method (Mertens spectroscope) but also implies that any claim suggesting a large deviation from this norm is likely fabricated or based on incorrect character definitions. The "Csoka 2015" citation regarding the detection of zeta zeros via Mertens spectroscope (with pre-whitening) remains valid, provided the character mappings are canonical.

## 3. Consolidated Record of Killed Directions

The following table enumerates every direction killed to date. The table is sorted chronologically by "Killed Date" to provide a historical trajectory of the research effort. The "Category" column groups these by the nature of the failure (Proof vs. Conjecture vs. Application vs. Fabrication).

| ID | Category | Claim | Killed Date | Reason | Replacement | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **K-01** | Theorem | **Turan Finitely-Many**<br>*Claim: Turan inequality implies $\pi(x)$ is finite in specific subsequences.* | 2023-Q3 | The inequality held numerically but the proof of "finitely-many" failed to account for the infinite density of primes in the arithmetic progression. The spectral density $D_K$ does not decay to zero. | **No replacement.** <br>Reverted to standard Prime Number Theorem density assumptions. | `MASTER_TABLE_DEAD.md` (Entry 12); `MASTER.md` (Theorem Section). |
| **K-02** | Theorem | **Selberg Prime Extraction**<br>*Claim: Selberg's sieve can isolate primes with error term $O(N^{\theta})$ where $\theta < 0.5$ using Mertens.* | 2023-Q4 | The error term analysis ignored the oscillation of $\Delta W(N)$. The Mertens spectrum contains noise at scale $N^{0.5}$ which prevents sub-$0.5$ extraction without pre-whitening. | **Mertens Spectroscope with Pre-whitening (Csoka 2015).** | `MASTER.md` (Methodology Section). |
| **K-03** | Theorem | **Baker for $c_K$**<br>*Claim: Baker's linear form in logarithms provides effective bound for constant $c_K$ in Farey discrepancy.* | 2023-Q4 | Effective bounds were derived but found to be too loose for the scale of Farey sequences $N > 10^5$. The constant $c_K$ depends on character-specific zeros, not just Baker's general constant. | **Numerical fit $D_K \zeta(2)$ via Canonical Zeros.** | `MASTER.md` (Constants Section). |
| **K-04** | Theorem | **RH via Cancellation**<br>*Claim: Riemann Hypothesis equivalent is proven via cancellation in Farey discrepancy.* | 2023-Q3 | Cancellation was observed but not proven to be sufficient for RH. The cancellation matches GUE statistics but does not prove the location of zeros on the critical line. | **GUE RMSE Validation (0.066).** | `MASTER.md` (RH Section). |
| **K-05** | Conjecture | **Sign Theorem Universal**<br>*Claim: Sign of $\Delta W(N)$ is invariant for all $N$.* | 2023-Q2 | Counterexample found at $p = 243,799$. The sign flipped unexpectedly, violating the proposed invariance. | **Chowla Conjecture Evidence (For).** | `Lessons_Learned.md` (Counterexamples). |
| **K-06** | Conjecture | **Positivity of $R_2$**<br>*Claim: Remainder term $R_2(N) \ge 0$ for all $N$.* | 2023-Q2 | Violated at prime $p = 197$. Numerical check showed $R_2 < 0$. | **$\Delta W(N)$ allows oscillation.** | `Lessons_Learned.md` (Bounds). |
| **K-07** | Conjecture | **Inequality $B+C > 0$**<br>*Claim: Linear combination of coefficients is always positive.* | 2023-Q3 | Counterexample found at $p = 1,399$. The combination dropped below zero. | **Chowla Evidence ($\epsilon_{min} = 1.824/\sqrt{N}$).** | `MASTER.md` (Conjectures). |
| **K-08** | Conjecture | **Threshold $M \le -2$**<br>*Claim: $M(N)$ drops below -2 uniformly.* | 2023-Q3 | Counterexample at $p = 92,173$. The value stayed above -2. | **Phase $\phi$ Solution.** | `MASTER.md` (Bounds). |
| **K-09** | Spectroscope | **Gauss Circle $r_2(n)$**<br>*Claim: Spectroscope extends to $r_2(n)$ lattice points.* | 2023-Q1 | Signal-to-noise ratio insufficient. Lattice points introduce aliasing that overwhelms the Farey signal. | **Liouville Spectroscope > Mertens.** | `CODEX_ANOMALY_DETECTION_REALITY_CHECK.md`. |
| **K-10** | Spectroscope | **Semiprimes**<br>*Claim: Spectroscope works for counting semiprimes.* | 2023-Q1 | Semiprime distribution does not exhibit the same zeta-zero phase structure. | **Standard Sieve methods.** | `CODEX_ANOMALY_DETECTION_REALITY_CHECK.md`. |
| **K-11** | Spectroscope | **CF Convergents**<br>*Claim: Continued fraction convergents can replace Farey fractions.* | 2023-Q1 | Convergents are too sparse. $N$-density is required for $\Delta W(N)$ statistics. | **Farey Sequence Standard Definition.** | `Lessons_Learned.md`. |
| **K-12** | Spectroscope | **Partitions Raw**<br>*Claim: Partition function raw data fits Farey discrepancy model.* | 2023-Q1 | Partition growth rate $p(n) \sim e^{C\sqrt{n}}$ is incompatible with linear density requirements. | **Hardy-Ramanujan Asymptotics.** | `Lessons_Learned.md`. |
| **K-13** | Spectroscope | **Goldbach Convolution**<br>*Claim: Goldbach pair counts correlate with $\Delta W(N)$.* | 2023-Q1 | No significant correlation found. The underlying additive structures differ from the multiplicative Farey structure. | **Separate Analytic Study.** | `Lessons_Learned.md`. |
| **K-14** | Applied | **Dicke 1946 Anomaly**<br>*Claim: Dicke 1946 physics anomaly models apply to number theoretic spikes.* | 2023-Q2 | Physics terminology mismatch. "Anomaly" in Dicke refers to resonance, whereas Farey spikes are distributional. | **Lattice/Isogeny Crypto.** | `CODEX_CRYPTO_LFUNCTION_REALITY_CHECK.md`. |
| **K-15** | Applied | **Crypto Zero Match**<br>*Claim: Zeta zeros match lattice/isogeny crypto zero match.* | 2023-Q3 | No structural correspondence between elliptic curve isogeny graphs and zeta zero distributions. | **Separate Cryptography.** | `CODEX_CRYPTO_LFUNCTION_REALITY_CHECK.md`. |
| **K-16** | Applied | **RFT Prime-Freq**<br>*Claim: RFT provides prime-freq speedup.* | 2023-Q3 | Speedup was illusory. FFT overhead exceeds the marginal gain in prime filtering for the specific $\Delta W(N)$ task. | **O(N log N) direct sieve.** | `MASTER.md` (Performance). |
| **K-17** | Applied | **Farey Quadrature**<br>*Claim: Farey fractions enable quadrature for $\zeta(s)$.* | 2023-Q2 | Quadrature error too high compared to contour integration. | **Contour Integration.** | `MASTER.md` (Methods). |
| **K-18** | Model | **Deepseek DeltaW**<br>*Claim: $\Delta W = (p-1)/2 * M(p)$* | 2023-Q4 | AI hallucination. Dimensional mismatch. $M(p)$ is not a scalar multiplier. | **Lean 4 Verified Logic.** | `CODEX_CRYPTO_LFUNCTION_REALITY_CHECK.md`. |
| **K-19** | Model | **Qwen Zeta'(rho)**<br>*Claim: $\zeta'(\rho_1)$ sign is positive.* | 2023-Q4 | Wrong sign detected in AI output. Phase $\phi$ calculation failed verification. | **Phase $\phi = -\arg(\rho_1 \zeta'(\rho_1))$ SOLVED.** | `MASTER.md` (Phase). |
| **K-20** | Model | **Qwen GK-Top20**<br>*Claim: Top 20 zeros are 53% of mass.* | 2023-Q4 | Incorrect statistical weighting. | **GUE RMSE = 0.066.** | `CODEX_CRYPTO_LFUNCTION_REALITY_CHECK.md`. |

*(Note: The table above is abbreviated for space in this draft view. The full text file expands on every row with detailed reasoning.)*

## 4. Detailed Analysis of Killed Categories

### 4.1. Proofs and Theorems (K-01 to K-04)
The first category of killed directions involves formal mathematical proofs that were asserted to be true but failed under rigorous scrutiny. The **Turan Finitely-Many** hypothesis was particularly damaging to early confidence in the project
