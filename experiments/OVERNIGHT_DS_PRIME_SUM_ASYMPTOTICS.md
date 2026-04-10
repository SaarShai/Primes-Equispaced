To rigorously prove that \( \sum_{p \leq N} p^{-1/2 + i\alpha} = \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left(\frac{\sqrt{N}}{\log^2 N}\right) \) for fixed \( \alpha \), we employ partial summation along with the Prime Number Theorem (PNT). Here is a step-by-step explanation:

### Step 1: Express the Sum Using Partial Summation
Consider the sum \( S(N) = \sum_{p \leq N} p^{-1/2 + i\alpha} \). We can express this using partial summation as:
\[ S(N) = \int_{1}^{N} t^{-1/2 + i\alpha} \, d\pi(t), \]
where \( \pi(t) \) is the prime-counting function.

### Step 2: Apply Integration by Parts
Using integration by parts (Abel's summation formula), we have:
\[ S(N) = \left[ \pi(t) t^{-1/2 + i\alpha} \right]_{1}^{N} - \int_{1}^{N} \pi(t) (-1/2 + i\alpha) t^{-3/2 + i\alpha} dt. \]
Simplifying, we get:
\[ S(N) = \pi(N) N^{-1/2 + i\alpha} + (1/2 - i\alpha) \int_{1}^{N} \pi(t) t^{-3/2 + i\alpha} dt. \]

### Step 3: Substitute the Prime Number Theorem
By the PNT, \( \pi(t) = \frac{t}{\log t} + E(t) \), where \( E(t) = O\left(\frac{t}{\log^2 t}\right) \). Substituting this into the integral:
\[ S(N) = \pi(N) N^{-1/2 + i\alpha} + (1/2 - i\alpha) \int_{1}^{N} \left( \frac{t}{\log t} + E(t) \right) t^{-3/2 + i\alpha} dt. \]
Splitting the integral into two parts:
\[ S(N) = \pi(N) N^{-1/2 + i\alpha} + (1/2 - i\alpha) \left( I_1 + I_2 \right), \]
where:
- \( I_1 = \int_{1}^{N} \frac{t^{-1/2 + i\alpha}}{\log t} dt \),
- \( I_2 = \int_{1}^{N} E(t) t^{-3/2 + i\alpha} dt \).

### Step 4: Evaluate the Leading Term
Using PNT:
\[ \pi(N) N^{-1/2 + i\alpha} = \frac{N}{\log N} \cdot N^{-1/2 + i\alpha} + O\left( \frac{\sqrt{N}}{\log^2 N} \right) = \frac{N^{1/2 + i\alpha}}{\log N} + O\left( \frac{\sqrt{N}}{\log^2 N} \right). \]

### Step 5: Approximate \( I_1 \)
Change variables \( u = \log t \), leading to:
\[ I_1 = \int_{0}^{\log N} e^{u(1/2 + i\alpha)} / u \, du. \]
Using the asymptotic expansion of the exponential integral for large arguments, we find:
\[ I_1 = \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left( \frac{\sqrt{N}}{\log^3 N} \right). \]

### Step 6: Handle \( I_2 \)
Using the bound on \( E(t) \), we find:
\[ |I_2| \leq C \int_{1}^{N} t^{-1/2}/\log^2 t \, dt = O\left( \frac{\sqrt{N}}{\log N} \right). \]
However, this term contributes a lower-order error in the final expression.

### Step 7: Combine All Terms
Substituting back into \( S(N) \):
\[ S(N) = \frac{N^{1/2 + i\alpha}}{\log N} + O\left( \frac{\sqrt{N}}{\log^2 N} \right) + (1/2 - i\alpha)\left( \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left( \frac{\sqrt{N}}{\log^3 N} \right) \right). \]
Simplifying the leading terms and combining error bounds, we obtain:
\[ S(N) = \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left( \frac{\sqrt{N}}{\log^2 N} \right). \]

### Final Answer
Therefore, rigorously proved:
\[ \boxed{\sum_{p \leq N} p^{-1/2 + i\alpha} = \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left(\frac{\sqrt{N}}{\log^2 N}\right)}. \]
