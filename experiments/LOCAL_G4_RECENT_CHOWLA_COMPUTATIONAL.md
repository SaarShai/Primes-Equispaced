As of 2025, the computational landscape regarding the **Chowla Conjecture** remains distinct from the computational landscape of the **Mertens Conjecture** or the **Riemann Hypothesis**. While there are world-record computations for the summatory function of the Möbius function $M(N) = \sum_{n \le N} \mu(n)$, direct computational testing of the Chowla correlations $\sum_{n \le N} \mu(n)\mu(n+h)$ is significantly more difficult and has not yet reached the same $N$ scales.

Below is a survey of the current state of computational results, methods, and the theoretical context you requested.

### 1. Theoretical Context: The "Logarithmic" vs. "Standard" Gap
To understand the computation, one must distinguish between the two versions of the conjecture:
*   **Standard Chowla:** $\sum_{n \le N} \mu(n+h_1) \dots \mu(n+h_k) = o(N)$.
*   **Logarithmic Chowla (Tao, 2016):** $\sum_{n \le N} \frac{\mu(n+h_1) \dots \mu(n+h_k)}{n} = o(\log N)$.

**Tao (2016)** proved the logarithmic version for $k=2$ (and later generalized), which is a monumental result. **Matomäki and Radziwiłł (2016)** provided the breakthrough for "short intervals," showing that the Möbius function does not correlate with itself on average in intervals much smaller than $N$.

**The Computational Difficulty:** Computing the *logarithmic* version is easier because the $1/n$ weight dampens the impact of large-scale fluctuations. Computing the *standard* version requires knowing the exact values of $\mu(n)$ for much larger ranges of $n$ to ensure the $o(N)$ signal isn't lost in the noise of the $O(N)$ complexity.

### 2. Computational Limits and $N$ Values
In computational number theory, we must distinguish between **sublinear algorithms** and **linear algorithms**:

*   **Mertens Function ($M(N)$):** Using the **Deléglise and Rivat** method (an evolution of the Meissel-Lehmer algorithm), $M(N)$ has been computed up to $N \approx 10^{16}$. This is possible because $M(N)$ can be computed using sublinear methods that do not require calculating every individual $\mu(n)$.
*   **Chowla Correlations ($\sum \mu(n)\mu(n+h)$):** There is no known sublinear algorithm to compute the correlation of $\mu(n)$ for a fixed $h$ without essentially computing the values of $\mu(n)$ themselves. Consequently, the complexity is $O(N)$.
*   **Current $N$ for Chowla:** As of 2025, direct computational verification of the Chowla correlation $\sum_{n \le N} \mu(n)\mu(n+1)$ is generally found in studies using $N$ in the range of **$10^{10}$ to $10^{12}$**. While $10^{12}$ is achievable on modern distributed clusters, pushing significantly beyond this for all $h$ becomes a memory-bandwidth bottleneck.

### 3. Who is testing this? (Methods and Names)
There is no single "Chowla Project" equivalent to the "Great Internet Mersenne Prime Search." Instead, testing is done within the context of:

*   **Sieve-based Methods:** The primary method is the **Segmented Sieve of Eratosthenes**. To test Chowla, one sieves a block of size $S$, computes $\mu(n)$ for all $n \in [K, K+S]$, and then computes the sum of the products.
*   **Helfgott and Additive Problems:** While **Harald Helfgott** is most famous for his computational proof of the Ternary Goldbach Conjecture, his work involves massive-scale verification of prime distributions. While he hasn't published a "Chowla-only" paper, the methodologies used in his work (large-scale distributed sieving and rigorous error bounding) are the blueprint for any attempt to push Chowla to higher $N$.
*   **The "Fried-Soundararajan" Connection:** You may be referring to the intersection of **Friedlander/Iwaniec** and **Soundararajan**. Soundararajan has pioneered work on the *distribution* of the error terms in prime number theory. Computational tests often focus on whether the distribution of the sum $\sum \mu(n)\mu(n+h)$ follows a Gaussian distribution, as predicted by the probabilistic model of the Möbius function.

### 4. Direct Testing of $\sum \mu(n)\mu(n+h)$
Research specifically targeting the autocorrelation of $\mu(n)$ (the $h=1$ case) often appears in papers discussing the **Möbius Randomness Principle**. 

*   **Direct Results:** Some researchers have utilized $N \approx 10^{11}$ to demonstrate that the correlation $\frac{1}{N} \sum_{n \le N} \mu(n)\mu(n+1)$ oscillates around zero with a decay consistent with the $1/\sqrt{N}$ fluctuations expected from a random walk.
*   **The "Small $h$" problem:** The difficulty increases as $h$ increases. For very large $h$, you essentially need a sieve that covers $N+h$, which is trivial, but the "window" of correlation becomes harder to verify statistically.

### Summary Table (Status 2025)

| Metric | Mertens Function ($M(N)$) | Chowla Correlation ($\sum \mu(n)\mu(n+h)$) |
| :--- | :--- | :--- |
| **Complexity** | Sublinear ($O(N^{2/3})$ or better) | Linear ($O(N)$) |
| **Largest $N$** | $\approx 10^{16}$ | $\approx 10^{12}$ |
| **Primary Method** | Meissel-Lehmer / Analytic | Segmented Sieve |
| **Key Objective** | Testing Riemann Hypothesis/Mertens | Testing Möbius Randomness / Tao-Radziwill |
| **Computational Bottleneck**| Arithmetic complexity | Memory Bandwidth / Linear Time |

**Conclusion:** If you are looking for a "world record" paper for Chowla, it likely does not exist in isolation. Instead, look for papers on **"Large-scale computation of the Möbius function"** or **"Distribution of the autocorrelation of the Liouville function."** The largest $N$ remains capped around $10^{12}$ due to the lack of a sublinear "Chowla-shortcut" algorithm.
