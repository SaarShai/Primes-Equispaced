To provide a rigorous foundation for your paper, we will first establish a **Fundamental Lemma** that serves as the building block for all four identities.

### The Fundamental Lemma
**Lemma:** The Ramanujan sum $c_b(m)$ can be expressed as:
$$c_b(m) = \sum_{d \mid \gcd(b, m)} d \mu\left(\frac{b}{d}\right)$$

**Proof:**
By definition, $c_b(m) = \sum_{a=1, \gcd(a,b)=1}^b e^{2\pi i \frac{m a}{b}}$.
We use the Mobius inversion property $\sum_{d \mid \gcd(a,b)} \mu(d) = [ \gcd(a,b)=1 ]$:
$$c_b(m) = \sum_{a=1}^b e^{2\pi i \frac{m a}{b}} \sum_{d \mid \gcd(a,b)} \mu(d)$$
Swapping the order of summation:
$$c_b(m) = \sum_{d \mid b} \mu(d) \sum_{k=1}^{b/d} e^{2\pi i \frac{m(kd)}{b}} = \sum_{d \mid b} \mu(d) \sum_{k=1}^{b/d} e^{2\pi i \frac{mk}{b/d}}$$
The inner sum is a sum of roots of unity of the form $\sum_{k=1}^N e^{2\pi i \frac{m k}{N}}$. This sum equals $N$ if $N$ divides $m$, and $0$ otherwise.
Here, $N = b/d$. Therefore, the inner sum is non-zero only if $\frac{b}{d} \mid m$. Since we already have $d \mid b$, the condition $\frac{b}{d} \mid m$ is equivalent to $\frac{b}{d} \mid \gcd(b, m)$.
Let $D = b/d$. As $d$ ranges over the divisors of $b$ such that $b/d$ divides $m$, $D$ ranges over the divisors of $\gcd(b, m)$. Substituting $d = b/D$:
$$c_b(m) = \sum_{D \mid \gcd(b, m)} \mu(b/D) \cdot D = \sum_{D \mid \gcd(b, m)} D \mu\left(\frac{b}{D}\right)$$
$\square$

---

### Identity (4): Multiplicativity
**Claim:** If $\gcd(b_1, b_2) = 1$, then $c_{b_1 b_2}(m) = c_{b_1}(m) c_{b_2}(m)$.

**Proof:**
Let $g = \gcd(b_1 b_2, m)$. Since $\gcd(b_1, b_2) = 1$, we have $g = \gcd(b_1, m) \cdot \gcd(b_2, m)$. Let $g_1 = \gcd(b_1, m)$ and $g_2 = \gcd(b_2, m)$.
Using the Lemma:
$$c_{b_1 b_2}(m) = \sum_{d \mid g_1 g_2} d \mu\left(\frac{b_1 b_2}{d}\right)$$
Every divisor $d$ of $g_1 g_2$ can be uniquely written as $d = d_1 d_2$ where $d_1 \mid g_1$ and $d_2 \mid g_2$. Because $\gcd(b_1, b_2)=1$, we have $\gcd(b_1/d_1, b_2/d_2)=1$, thus $\mu(\frac{b_1}{d_1} \cdot \frac{b_2}{d_2}) = \mu(\frac{b_1}{d_1})\mu(\frac{b_2}{d_2})$.
$$c_{b_1 b_2}(m) = \sum_{d_1 \mid g_1} \sum_{d_2 \mid g_2} d_1 d_2 \mu\left(\frac{b_1}{d_1}\right) \mu\left(\frac{b_2}{d_2}\right)$$
$$c_{b_1 b_2}(m) = \left( \sum_{d_1 \mid g_1} d_1 \mu\left(\frac{b_1}{d_1}\right) \right) \left( \sum_{d_2 \mid g_2} d_2 \mu\left(\frac{b_2}{d_2}\right) \right) = c_{b_1}(m) c_{b_2}(m)$$
$\square$

---

### Identity (1): Evaluation for Squarefree $b$
**Claim:** For squarefree $b$, $c_b(m) = \mu\left(\frac{b}{\gcd(b,m)}\right) \frac{\phi(b)}{\phi\left(\frac{b}{\gcd(b,m)}\right)}$.

**Proof:**
Since $b$ is squarefree, $c_b(m)$ is the product of its values at prime factors $p \mid b$.
For a prime $p$:
1. If $p \mid m$: $c_p(m) = \sum_{d \mid \gcd(p, m)} d \mu(p/d) = 1\mu(p) + p\mu(1) = -1 + p = p-1$.
2. If $p \nmid m$: $c_p(m) = \sum_{d \mid \gcd(p, m)} d \mu(p/d) = 1\mu(p) = -1$.

Let $g = \gcd(b, m)$. The primes $p$ dividing $b$ fall into two sets: $p \mid g$ and $p \mid (b/g)$.
$$c_b(m) = \left( \prod_{p \mid g} (p-1) \right) \left( \prod_{p \mid (b/g)} (-1) \right)$$
Now consider the target expression. Since $b$ is squarefree, $\mu(b/g) = (-1)^{\omega(b/g)}$, where $\omega(b/g)$ is the number of primes in $b/g$. This matches the second product.
For the first product, $\frac{\phi(b)}{\phi(b/g)} = \frac{\prod_{p \mid b} (p-1)}{\prod_{p \mid (b/g)} (p-1)}$. The terms $(p-1)$ for $p \mid (b/g)$ cancel out, leaving exactly $\prod_{p \mid g} (p-1)$.
Thus, $c_b(m) = \mu(b/g) \frac{\phi(b)}{\phi(b/g)}$.
$\square$

---

### Identity (2): Prime $p$ and $b < p$
**Claim:** For prime $p$ and $b < p$, $c_b(p) = \mu(b)$.

**Proof:**
Using the Lemma, $c_b(p) = \sum_{d \mid \gcd(b, p)} d \mu(b/d)$.
Since $p$ is prime and $b < p$, the only common divisor between $b$ and $p$ is $1$. Thus, $\gcd(b, p) = 1$.
The summation contains only one term where $d=1$:
$$c_b(p) = 1 \cdot \mu(b/1) = \mu(b)$$
$\square$

---

### Identity (3): Summation related to Mertens Function $M(N)$
**Claim:** $\sum_{b=1}^N c_b(m) = \sum_{d \mid m} d \cdot M\left(\lfloor N/d \rfloor\right)$, where $M(x) = \sum_{k=1}^x \mu(k)$.

**Proof:**
Expand the sum using the Lemma:
$$\sum_{b=1}^N c_b(m) = \sum_{b=1}^N \sum_{d \mid \gcd(b, m)} d \mu\left(\frac{b}{d}\right)$$
The condition $d \mid \gcd(b, m)$ implies $d \mid b$ and $d \mid m$. We can rewrite the sum by iterating over $d$ first:
$$\sum_{d \mid m} d \sum_{\substack{1 \le b \le N \\ d \mid b}} \mu\left(\frac{b}{d}\right)$$
Let $b = kd$. As $b$ goes from $d$ to $N$ in steps of $d$, $k$ goes from $1$ to $\lfloor N/d \rfloor$:
$$\sum_{d \mid m} d \sum_{k=1}^{\lfloor N/d \rfloor} \mu(k)$$
By definition, the inner sum is the Mertens function $M(\lfloor N/d \rfloor)$.
$$\sum_{b=1}^N c_b(m) = \sum_{d \mid m} d \cdot M\left(\lfloor N/d \rfloor\right)$$
$\square$
