The formula you have found is for the function $M(x) = \sum_{n \le x} \mu(n)$.

### The Short Answer
The coefficient of $x^\rho$ in the explicit formula for $M(x)$ is indeed **$\frac{1}{\rho \zeta'(\rho)}$**.

The formula involving **$\rho - 1$** (i.e., $\frac{1}{(\rho-1)\zeta'(\rho)}$) typically appears when dealing with the weighted sum $\sum_{n \le x} \frac{\mu(n)}{n}$ or when deriving $M(x)$ via an integral relation (like $\int_0^\infty M(t)/t^2 \dots$), which shifts the poles.

### Detailed Explanation

The explicit formula for $M(x)$ is derived using **Perron's Formula**.
The Dirichlet series for the Möbius function $\mu(n)$ is:
$$ \sum_{n=1}^{\infty} \frac{\mu(n)}{n^s} = \frac{1}{\zeta(s)} $$
Note that the Dirichlet series for the weighted sum $\frac{\mu(n)}{n}$ is $\frac{1}{\zeta(s+1)}$.

#### 1. For $M(x) = \sum_{n \le x} \mu(n)$
To recover $M(x)$ from its generating function $1/\zeta(s)$, we look at the integral:
$$ \frac{1}{2\pi i} \int_{c-i\infty}^{c+i\infty} \frac{1}{\zeta(s)} \frac{x^s}{s} \, ds $$
The integrand is $f(s) = \frac{x^s}{s \zeta(s)}$.
*   **The Poles:** The function has poles at the zeros of $\zeta(s)$ (the non-trivial zeros $\rho$ and trivial zeros $s=-2k$) and at $s=0$.
*   **Residue at $s=\rho$:** Since $\zeta(\rho)=0$, we have a simple pole at each zero $\rho$. The residue is:
    $$ \text{Res}_{s=\rho} \left( \frac{x^s}{s \zeta(s)} \right) = \lim_{s \to \rho} (s-\rho) \frac{x^s}{s \zeta(s)} = \frac{x^\rho}{\rho \zeta'(\rho)} $$
    Notice the **$\rho$** in the denominator comes from the **$1/s$** term in Perron's formula.

This confirms that for $M(x)$, the coefficient is **$\frac{1}{\rho \zeta'(\rho)}$**.

#### 2. For $\sum_{n \le x} \frac{\mu(n)}{n}$
The generating function for this sum is $\frac{1}{\zeta(s+1)}$. The corresponding Perron integral would be:
$$ \frac{1}{2\pi i} \int_{c-i\infty}^{c+i\infty} \frac{1}{\zeta(s+1)} \frac{x^s}{s} \, ds $$
By substituting $w = s+1$ (so $s = w-1$), this looks like looking at the function $1/\zeta(w)$ but with the integral variable shifted.
*   The pole corresponding to a zero $\rho$ of $\zeta$ is now at $s = \rho - 1$.
*   The residue calculation would involve $\frac{1}{s}$ evaluated at the pole $s = \rho-1$, which gives $\frac{1}{\rho-1}$.
*   Also, the term $x^s$ becomes $x^{\rho-1}$.
So the term in the explicit formula for the weighted sum involves **$\frac{1}{(\rho-1)\zeta'(\rho)}$**.

### Summary of Your Formula
Your formula:
$$ M(x) = -2 + \sum_{\rho} \frac{x^\rho}{\rho \zeta'(\rho)} + \sum_{k=1}^{\infty} \frac{x^{-2k}}{-2k \zeta'(-2k)} $$
is the correct explicit formula for the standard summatory function $M(x)$. The coefficient $\frac{1}{\rho \zeta'(\rho)}$ is robust for $M(x)$. The term with $\rho-1$ belongs to the summatory function of the normalized coefficients $\mu(n)/n$.
