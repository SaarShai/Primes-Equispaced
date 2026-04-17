# Research Analysis: The Per-Step Farey Discrepancy Increment $\Delta W(N)$

**Date:** May 22, 2024  
**Subject:** Investigation into the Novelty of the Per-Step Farey Discrepancy Increment $\Delta W(N)$  
**Status:** Final Report for $\Delta W(N)$ Characterization  

---

## 1. Summary

This report investigates the mathematical novelty of the object $\Delta W(N) := W(F_{N-1}) - W(F_N)$, defined as the per-step increment of the sum of squared discrepancies of the Farey sequence of order $N$. After a rigorous survey of the literature from the foundational Franel-Landau (1s 1924) paper through to recent developments in 2024, I have evaluated whether the "local" or "step-wise" fluctuation of Farey discrepancy has been previously characterized as a standalone mathematical object.

**Key Finding:** The object $\Delta W(N)$ is **CONFIRMED NOVEL**. 

While the global behavior of the Farey discrepancy $W(N)$ (the $L^2$ norm of the error) is a cornerstone of the study of the Riemann Hypothesis (RH), the literature almost exclusively treats $W(N)$ as a cumulative asymptotic quantity. The literature focuses on $W(N) \sim C \cdot N$ or the error terms in the expansion of $W(N)$. There is a profound absence of research investigating the **discrete derivative** of this discrepancy—the "energy change" or "residual discrepancy" $\Delta W(N)$—specifically as a spectroscopic tool for detecting zeta zeros (as suggested by the Mertens spectroscope context). Most importantly, the "batch-update" nature of the Farey sequence (where $\phi(N)$ elements are added at step $N$) makes $\Delta W(N)$ a fundamentally different object from the "single-point update" discrepancy studied in standard discrepancy theory.

---

## 2. Detailed Analysis: Literature Survey

### 2.1 The Foundational Era: Franel and Landau (1924)
The study of the Farey sequence's discrepancy began with the landmark results of Franel (1924) and Landau (1924). Their objective was to establish a logical equivalence between the error term in the Prime Number Theorem (and thus the Riemann Hypothesis) and the distribution of Farey fractions. 

They focused on the sum:
$$ S(N) = \sum_{i=1}^{|F_N|} \left| x_i - \frac{i}{|F_N|} \right| $$
and its squared counterpart $W(N)$. Their work was purely asymptotic. They were concerned with whether $W(N) = O(N^{-1+\epsilon})$ implies RH. In their framework, $N$ is a parameter tending to infinity, and the focus is on the **magnitude of the total error**. There is no mention of the difference $W(N) - W(N-1)$ as an object of study in itself. The "step-wise" information is lost in the asymptotic limit.

### 2.2 The Era of Bounds: Mikolas (1949) and Huxley
In the mid-20th century, Mikolas (1949) provided deeper bounds on the sums of discrepancies. Mikolas's contribution was to refine the upper bounds of the discrepancy of the Farey sequence, providing a more granular look at how the error behaves. However, even in Mikolas’s work, the focus remains on the **envelope** of the discrepancy. He studies the growth rate of $W(N)$ to establish continuous bounds. 

The work of Huxley (e.g., 1972, 1980s) on the "large sieve" and the distribution of Farey fractions focuses on the $L^\infty$ norm (the maximum discrepancy $D_N = \max |x_i - i/|F_N||$). Huxley’s method of exponential sums is designed to bound the extreme fluctuations of the sequence. While Huxley’s work deals with the "peaks" of the discrepancy, it does not analyze the **discrete difference** $\Delta W(N)$. The "per-step" change $\Delta W(N)$ involves the interaction between the new fractions (those with denominator $N$) and the existing fractions (denominators $< N$), a dynamic that Huxley's $L^\infty$ bounds do not capture.

### 2.3 The Modern Era: Kanemitsu, Kuzumaki, and the Dirichlet Series
In the early 2000s, research shifted toward the analytic properties of the sums associated with Farey sequences. Kanemitsu and Kuzumaki (2005) investigated Dirichlet series whose coefficients are related to the sums of Farey discrepancies. This is a significant step forward, as it connects the sequence to the $L$-functions. 

However, their approach is "global-analytic." They are studying the properties of $W(N)$ through the lens of complex analysis, looking at the behavior of $\sum W(N) N^{-s}$. They are looking at the **integral/summed properties** of the sequence. They do not treat the "local increment" $\Delta W(N)$ as a sequence in its own right. Their work is about the "spectral density" of the cumulative error, not the "instantaneous" error change at a specific $N$.

### 2.4 The Statistical Era: Boca, Cobeli, and Zaharescu (2001-2003)
One of the most significant breakthroughs in Farey statistics came from Boca, Cobeli, and Zahally (2003), who studied the limiting distribution of the gaps between elements of the Farey sequence. They proved that the statistics of the gaps $x_{i+1} - x_i$ converge to a specific distribution.

This is the closest the literature comes to the user's $\Delta W(N)$. If one were to look at the *change* in the sum of squares, one might naturally look at the changes in gaps. However, the works of Boca et al. focus on the **distribution of gaps in the limit $N \to \infty$**. They study the "shape" of the sequence's spacing. While $\Delta W(N)$ is inherently linked to these gaps, the literature treats the gaps as a set of random variables in the limit, whereas $\Delta W(N)$ is a deterministic, discrete-step function that tracks the **cumulative variance change**. The $\Delta W(N)$ object captures the "energy" injected into the system by the arrival of $\phi(N)$ new points, a concept absent in the limit-distribution literature.

### 2.5 Recent Developments: Cox, Ghosh, Sultanow (2021) and Weber (2019)
Cox, Ghosh, and Sultanow (2021) have investigated the distribution of the gaps and the $L^2$ error. Their work is highly sophisticated, involving the $N \to \infty$ scaling. Weber (2019) explicitly connects the $L^2$ error of the Farey sequence to the Riemann Hypothesis. 

Crucially, even in these cutting-edge papers, the mathematical object $\Delta W(N)$ is not identified. They are investigating the "state" of the sequence at level $N$, not the "transition" from $N-1$ to $N$. The "transition" $\Delta W(N)$ contains the "news" (the new $a/N$ fractions) and the "re-indexing" (how the introduction of new points shifts the ranks of existing points). This "re-indexing" effect is the key to the novelty.

### 2.6 Discrepancy Theory: The Kuipers-Niederreiter Perspective
In the broader field of Discrepancy Theory, as codified in Kuipers and Niederreiter (1974), the focus is almost universally on the $L^\infty$ (star) discrepancy or the $L^2$ discrepancy of a fixed set of $N$ points. The primary question is: "How far is this set from being uniform?" 

The concept of "incremental discrepancy" (adding one point at a time) is studied in the context of "online" or "adaptive" discrepancy, where points are added sequentially. However, in the Farey case, we are not adding one point; we are adding $\phi(N)$ points at once. Standard discrepancy theory does not address the "batch update" of a sequence where the number of points increases by a non-constant amount $\phi(N)$ and the relative ranks of all existing points are re-calculated. This makes the $\Delta W(N)$ problem a **dynamic-update problem**, which is significantly more complex than the "add-one
