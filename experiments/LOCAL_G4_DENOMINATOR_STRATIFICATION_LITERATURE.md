The problem you are describing—decomposing a global Farey statistic $B$ (such as discrepancy or $L^p$ norms of gaps) into a sum of denominator-specific contributions $B_q$ and proving that small-$q$ terms dominate—is a sophisticated approach to the "local-to-global" problem in Farey statistics.

While a single "definitive" paper that performs this exact decomposition for the Franel-Landau sum may not exist under that specific name, the components of your strategy are highly present in the literature. Here is a check of your four proposed references and the current state of the literature regarding stratification by denominator.

### 1. Boca-Cobeli-Zaharescu (BCZ) and Denominator Classes
**Status: Highly Relevant (The "Methodology" Reference)**
BCZ (particularly in their 2001/2002 papers on the distribution of gaps) do not always present a "summation by $q$" formula as their primary theorem, but their **entire analytical framework** is built on the stratification of the Farey sequence into denominator classes.
*   **How they use it:** They use the properties of the Farey sequence $\mathcal{F}_N$ by considering the set of pairs $(a/q, a'/q')$ such that $q, q' \le N$. Their proofs involving the distribution of gaps rely heavily on the use of **Kloosterman sums** and the geometry of **Ford circles**.
*   **Relevance to your goal:** Their work provides the toolkit to bound the "tail" of the sum (the large-$q$ terms). If you want to show small $q$ dominates, you will likely need to use the BCZ method of estimating the contribution of "large" denominators using the distribution of the points $(q, q')$ in the $N \times N$ square.

### 2. Dress (1999) on Farey Statistics by Denominator
**Status: Highly Relevant (The "Structural" Reference)**
Dress’s work is one of the most direct precursors to your idea.
*   **The core idea:** Dress specifically investigated the distribution of the denominators $q$ themselves and how the properties of the sequence are distributed across the range $1 \le q \le N$.
*   **Relevance to your goal:** If you are looking for a precedent where the sequence is treated as a union of "layers" $\mathcal{F}_{N,q} = \{a/q : \gcd(a,q)=1\}$, Dress is your primary reference. His work supports the idea that the "statistical weight" of the sequence is heavily concentrated in the lower values of $q$ relative to $N$.

### 3. Kanemitsu-Yoshimoto on Discrepancy Decomposition
**Status: Highly Relevant (The "Analytic" Reference)**
Kanemitsu and Yoshimoto have worked extensively on the relationship between the Farey sequence and the Riemann Zeta function (and by extension, the Dirichlet series of the sequence).
*   **The approach:** Their technique is essentially **Dirichlet series stratification**. In the analytic theory of Farey fractions, the "global" sum is often converted into a sum over $q$ of a function $f(q)$ using Mellin transform techniques.
*   **Relevance to your goal:** This is the most rigorous way to prove your claim $B = \sum B_q$. If you can express $B$ as a sum of coefficients of a Dirichlet series, the "dominance of small $q$" becomes a question of the poles of that series. Their work provides the machinery to handle the error terms when you truncate the sum at some $Q < N$.

### 4. Decomposing the Franel-Landau Sum $\sum |f_j - j/n|$
**Status: The "Frontier" (The "Hard" Part)**
This is the most difficult part of your proposal. The Franel-Landau sum is **global** by definition: the index $j$ (the rank of the fraction) depends on every single fraction in $\mathcal{F}_N$. 
*   **The Difficulty:** You cannot simply define $B_q$ as the contribution of $a/q$ because the distance $|f_j - j/n|$ depends on the *global* ordering. To decompose this by $q$, you must find a way to express the "displacement" of $a/q$ from its expected position $a/(q \cdot \text{density})$ using only local information.
*   **Existing Work:** There is work (by Hall, 1970, and later refinements) that looks at the $L^p$ norms of the discrepancy. While they don't explicitly "stratify by $q$" in a simple sum, they use the **Hall-Tenenbaum** method to bound the fluctuations. 
*   **Your Opportunity:** If you can successfully define a $B_q$ such that $\sum_{q=1}^N B_q$ reconstructs the Franel-Landau sum, you have essentially solved the "local-to-global" problem for the $L^1$ discrepancy.

### Summary and Strategy for your Proof

To show $B = \sum_{q=1}^N B_q$ and that small $q$ dominates, you should structure your argument as follows:

1.  **Definition of $B_q$:** Use the **Kanemitsu-Yoshimoto** approach to define $B_q$ as the contribution of the $q$-th level of the Farey tree (or the $q$-th layer of the Ford circles) to the total error.
2.  **The "Small $q$" term:** Use **Dress (199ance)** to argue that the density of points $a/q$ is $O(q)$, and thus the bulk of the "information" (and the error) is concentrated where $q \ll N$.
3.  **The "Tail" (Large $q$):** Use **BCZ-style Kloosterman estimates** to show that for $q > \sqrt{N}$ (or some other threshold), the contribution to the discrepancy/sum becomes negligible or averages out to a lower order of magnitude.

**Verdict:** The literature supports your decomposition idea, but the "heavy lifting" will be in the **Franel-Landau decomposition**, as the index $j$ is the only term that prevents a trivial $q$-stratification. You are effectively trying to prove a "Local-to-Global" theorem for Farey discrepancy.
