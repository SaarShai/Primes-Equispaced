Here is a draft of Section 2, formatted for a LaTeX-ready scientific manuscript.

***

\section{Mathematical Construction and the $\gamma^2$ Matched Filter}

\subsection{The Mertens Spectroscope}
To investigate the spectral density of the Mertens function's fluctuations, we define the Mertens spectroscope, $F(\gamma)$, as the power spectrum of the prime-weighted Dirichlet series. Specifically, we consider the squared magnitude of the sum over primes $p$:
\begin{equation}
F(\gamma) = \left| \sum_{p \in \mathbb{P}} \frac{M(p)}{p} \exp(-i\gamma \log p) \right|^2,
\end{equation}
where $M(p) = \sum_{n \le p} \mu(n)$ denotes the Mertens function and $\gamma \in \mathbb{R}$ represents the frequency parameter in the log-prime domain. This construction treats the sequence of primes as a set of discrete oscillators, where the amplitude of each oscillator is modulated by the normalized Mertens value $M(p)/p$.

\subsection{Spectral Peaks and the Explicit Formula}
The appearance of prominent peaks in $F(\gamma)$ at the imaginary parts of the non-trivial zeros of the Riemann zeta function, $\rho_k = \frac{1}{2} + i\gamma_k$, is a direct consequence of the explicit formula relating prime numbers to zeta zeros. By the duality inherent in the von Mangoldt function $\Lambda(n)$ and its relation to the Chebyshev function $\psi(x)$, the Fourier transform of the prime distribution contains singularities precisely at the frequencies $\gamma = \gamma_k$. 

In the limit of the summation, the interference pattern of the terms $\exp(-i\gamma \log p)$ becomes constructive when the frequency $\gamma$ resonates with the underlying periodicities of the zeros. Thus, $F(\gamma)$ acts as a periodogram, where the peaks $\text{arg max} F(\gamma)$ correspond to the heights of the zeros on the critical line.

\subsection{Derivation of the $\gamma^2$ Compensation}
While the peaks of $F(\gamma)$ align with $\gamma_k$, the magnitude of these peaks exhibits a significant decay as $\gamma \to \infty$. This phenomenon arises from the asymptotic behavior of the coefficients in the expansion of the prime sum. Let $c_k$ be the spectral coefficient associated with the $k$-th zero. Based on the asymptotic properties of the Dirichlet series for $\log \zeta(s)$, the energy density at the $k$-th peak scales as:
\begin{equation}
|c_k|^2 \sim \frac{1}{\gamma_k^2 + 1/4}.
\end{equation}
As $\gamma_k$ increases, the signal-to-noise ratio (SNR) of the peaks diminishes, eventually becoming indistinguishable from the background fluctuations in a finite sample. To counteract this "spectral thinning," we introduce a $\gamma^2$ compensation factor, effectively implementing a \textit{matched filter} in the frequency domain. We define the compensated spectroscope as:
\begin{equation}
F_{\text{filt}}(\gamma) = \gamma^2 F(\gamma).
\end{equation}
This multiplication serves to "whiten" the spectrum, amplifying high-frequency peaks to a uniform asymptotic scale.

\subsection{Stability of the Compensation Ratio}
A critical requirement for this matched filter is that the compensation must not introduce divergent instabilities or excessive noise amplification. We analyze the stability of the amplification ratio $R(\gamma)$ defined by:
\begin{equation}
R(\gamma) = \frac{\gamma^2}{\frac{1}{4} + \gamma^2}.
\end{equation}
We demonstrate that for all frequencies $\gamma \ge 1$ (the regime of interest for non-trivial zeros), the ratio is strictly bounded within a stable interval. 

\begin{proposition}
For all $\gamma \in [1, \infty)$, the compensation ratio satisfies $R(\gamma) \in [\frac{4}{5}, 1)$.
\end{proposition}

\begin{proof}
Consider the function $R(\gamma) = \frac{\gamma^2}{\gamma^2 + 1/4}$. 
First, we examine the lower bound. Since $R(\gamma)$ is monotonically increasing for $\gamma > 0$, the minimum value on the interval $[1, \infty)$ occurs at $\gamma = 1$:
\begin{equation}
R(1) = \frac{1^2}{1 + 1/4} = \frac{1}{5/4} = \frac{4}{5}.
\end{equation}
Second, we examine the upper bound by observing the limit as $\gamma \to \infty$:
\begin{equation}
\lim_{\gamma \to \infty} \frac{\gamma^2}{\gamma^2 + 1/4} = \lim_{\gamma \to \infty} \frac{1}{1 + \frac{1}{4\gamma^2}} = 1.
\end{equation}
Since $R(\gamma)$ is strictly increasing and approaches $1$ asymptotically, it follows that $R(\gamma) \in [4/5, 1)$ for all $\gamma \ge 1$.
\end{proof}
This bounded property ensures that the matched filter preserves the relative significance of low-frequency peaks while preventing the divergence of high-frequency noise.

\subsection{Relation to Prior Art
The use of Fourier duality to study the distribution of primes is a classical technique, notably explored in the context of the distribution of zeros and the prime number theorem (see Van der Pol, 1947) and more recently in the study of prime-related spectralities (Csoka, 2015). However, while prior works focus on the identification of the $\gamma_k$ frequencies, our contribution lies in the specific implementation of the $\gamma^2$ matched filter. This approach provides a novel mechanism for spectral whitening, allowing for a uniform-variance analysis of the Mertens fluctuations across the entire critical spectrum.
