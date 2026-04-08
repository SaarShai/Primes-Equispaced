Your analysis of the computational bottleneck is correct, but there is a significant statistical issue in your $SNR$ formula that fundamentally changes the "practical limit."

In statistical hypothesis testing for prime distributions, the "noise" is not the denominator of your formula, but the **standard deviation of the counts** in each residue class.

### 1. The Statistical Reality Check
Let $n_a$ be the number of primes $p \le N$ such that $p \equiv a \pmod q$.
The expected number of primes in a residue class is $E = \frac{N}{\phi(q)}$.
The standard deviation (noise) of this count, assuming a Poisson-like distribution for large $N$, is $\sigma = \sqrt{\frac{N}{\phi(q)}}$.

If a Siegel zero exists, it introduces a bias $\beta$. The "Signal" is the deviation from the mean:
$$\text{Signal} = \beta \cdot \frac{N}{\phi(q)}$$
Therefore, the **true SNR** is:
$$SNR = \frac{\text{Signal}}{\text{Noise}} = \frac{\beta \frac{N}{\phi(q)}}{\sqrt{\frac{N}{\phi(q)}}} = \beta \sqrt{\frac{N}{\phi(q)}}$$

**Why your current $SNR$ is misleading:**
Using your numbers ($N=78,000, \beta=0.01, q=1000, \phi(q)=400$):
*   **Your formula:** $SNR \approx 1,950,000$ (Suggesting massive visibility).
*   **Correct formula:** $SNR = 0.01 \cdot \sqrt{\frac{78000}{400}} = 0.01 \cdot \sqrt{195} \approx \mathbf{0.139}$.

**The Verdict:** At $q=1000$, a $1\%$ bias is **completely invisible** in a sample of 78,000 primes. The signal is roughly 7 times smaller than the natural statistical fluctuation. To see a $1\%$ bias at $q=1000$ with $SNR=3$ (detectable), you would need $N \approx 1.8 \times 10^9$ primes.

---

### 2. Assessing the Practical Limits

Since the bottleneck is actually **Sample Size ($N$)** rather than **Computation**, let's re-evaluate $q=100$ and $q=500$ based on your $N=78,000$.

To achieve a detectable signal ($SNR \ge 3$) for a specific $\beta$:
$$\phi(q) \le \frac{N \beta^2}{9}$$

#### Case A: $q=100$ ($\phi(q) \approx 40$)
*   $SNR = 0.01 \cdot \sqrt{78000/40} = 0.01 \cdot \sqrt{1950} \approx \mathbf{0.44}$
*   **Result:** Still invisible. You can only detect biases larger than $\sim 7\%$ at $q=100$.

#### Case B: $q=500$ ($\phi(q) \approx 200$)
*   $SNR = 0.01 \cdot \sqrt{78000/200} = 0.01 \cdot \sqrt{390} \approx \mathbf{0.19}$
*   **Result:** Even harder to detect.

---

### 3. Addressing your Computational Bottleneck
You are correct that for large $q$, identifying the character is the overhead. However, because the $N$ required for large $q$ grows quadratically with the desired precision, the computational cost of the Discrete Log is actually a secondary concern.

**The real computational hierarchy is:**
1.  **Quadratic Characters (Legendre Symbol):** $\mathcal{O}(\log p)$. This is extremely fast. You can scale $q$ to $10^6$ easily.
2.  **Non-Quadratic Characters:** Requires finding a primitive root $g$ and computing $ind_g(a) \pmod{\phi(q)}$. For $q < 10^6$, this is trivial using Baby-step Giant-step (BSGS).
3.  **The Real Wall:** The number of characters to check. For $q=10,000$, you have $4,000$ characters. For each, you must iterate through $N$ primes. Total complexity: $\mathcal{O}(\phi(q) \cdot N \cdot \log p)$.

### 4. Final Recommendation for your Research

If you want to find "anomalies" (Siegel zeros) using your current dataset of $N=78,000$:

1.  **Don't look for $\beta=0.01$.** Your dataset is too small to see 1% fluctuations at $q > 10$.
2.  **Search for "Large" Anomalies:** You are currently only sensitive to $\beta > 0.1$ (10% bias) for $q \approx 100$.
3.  **The Strategy:** 
    *   **Keep $q$ small ($q < 100$):** This keeps the $\phi(q)$ small, maximizing your $SNR$.
    *   **Increase $N$:** If you can expand your prime list to $N=10^7$, your $SNR$ at $q=1000$ jumps to $\approx 1.4$, which is much closer to the realm of scientific significance.
    *   **Focus on Quadratic Residue Bias:** Instead of computing all characters, just test the Legendre symbol $(a/p)$. It is computationally "free" and the most likely place for a Siegel zero to manifest a measurable bias.
