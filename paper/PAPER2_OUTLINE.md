Here is a structured 8-section paper outline, designed for a computational/analytic number theory or mathematical physics journal. Each section includes a substantive description that explicitly integrates your stated results.

**1. Introduction**
Contextualizes the search for Riemann zeta zeros through harmonic analysis on primes. Introduces the Compensated Mertens Spectroscope as a novel signal-processing framework that converts arithmetic phase data into resolvable spectral peaks. Provides a roadmap of the paper and summarizes the core empirical claims: perfect zero recovery, statistical universality, and robust scaling properties.

**2. Mathematical Construction & The γ²-Matched Filter**
Derives the core observable $F(\gamma) = \gamma^2 \left| \sum_{p} \frac{M(p)}{p} e^{-i\gamma \log p} \right|^2$. Demonstrates why the $\gamma^2$ prefactor acts as a *matched filter*, compensating for the natural $1/\gamma$ decay in the explicit formula and flattening the background spectral density. Proves that $\gamma^2$ multiplication is the critical innovation enabling phase-coherent zero extraction from prime-phase sums.

**3. Zero Detection Performance & Local Z-Scores**
Presents the primary empirical result: $F(\gamma)$ successfully detects 20/20 low-lying Riemann zeta zeros. Introduces a local z-score metric that quantifies peak significance against the non-zero background continuum. Displays confidence intervals, detection thresholds, and false-discovery bounds, confirming that all peaks exceed statistical significance requirements by wide margins.

**4. Spectral Statistics & GUE Universality**
Analyzes the spacing distribution of detected zero ordinates. Computes nearest-neighbor pair correlation and higher-order statistics, comparing empirical histograms against the Gaussian Unitary Ensemble (GUE) prediction. Reports a root-mean-square error of $\text{RMSE}=0.066$ against the Wigner surmise, strongly supporting random-matrix-theory universality for the spectroscope output.

**5. Computational Scaling & The 25M-Prime Optimum**
Investigates the trade-off between computational cost and spectral resolution as the prime cutoff $x$ increases. Identifies $2.5 \times 10^7$ as the operational optimum: at this scale, the spectroscope recovers 19/20 target zeros with only 0.26% relative error in peak positions, while avoiding algorithmic stagnation and memory overflow present at higher cutoffs.

**6. Robustness Testing: Subset Stability vs. Multi-Taper Failure**
Conducts two comparative stress-tests. First, demonstrates that detection persists for *any* prime subset (e.g., congruence classes, sparsely sampled primes), confirming intrinsic algorithmic redundancy. Second, applies standard multi-taper spectral estimation to the same phase data and documents systematic failure to resolve zeros, attributing the breakdown to unweighted phase dispersion and lack of spectral compensation.

**7. Extension to Automorphic L-Functions**
Generalizes the spectroscope kernel to Dirichlet $L$-functions, Hecke $L$-functions, and modular form L-functions. Details necessary modifications: insertion of character coefficients $\chi(p)$, conductor-dependent frequency scaling, and adjusted weight normalizations. Notes that the same $\gamma^2$ compensation architecture recovers low-lying non-trivial zeros across distinct L-families without structural redesign.

**8. The Amplitude Anti-Correlation Anomaly & Conclusion**
Documents a persistent empirical regularity: spectral amplitude at zero peaks systematically anti-correlates with zero height/imaginary part, suggesting a hidden rigidity or cancellation mechanism not yet explained by the explicit formula. Frames this as a primary open problem, proposes possible links to spectral form factors and secondary explicit-formula corrections, and outlines future work on rigorous bounds, higher-rank generalizations, and hardware-accelerated sweeps.
