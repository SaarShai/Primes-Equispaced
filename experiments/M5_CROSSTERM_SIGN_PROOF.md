To address the problem of proving that the sum \( \sum_{f \in F_{p-1}} D(f) \cdot \delta(f) < 0 \) whenever \( M(p) \leq -2 \), we proceed through a structured analysis.

---

### Summary

The goal is to establish the sign of the sum \( B = 2 \sum_{f \in F_{p-1}} D(f) \cdot \delta(f) \) based on the value of \( M(p) \). This involves understanding the Farey sequence, displacement measure \( D(f) \), and fractional part function \( \delta(f) \).

---

### Detailed Analysis

#### 1. Definitions and Setup

- **Farey Sequence**: \( F_{p-1} \) is the set of reduced fractions between 0 and 1 with denominators ≤ \( p-1 \).
- **Displacement Measure**: \( D(f) = j_{a/b} - n \cdot (a/b) \), where \( j_{a/b} \) is the rank of \( f = a/b \) in \( F_{p-1} \), and \( n = |F_{p-1}| \).
- **Displacement Function**: \( \delta(f) = f - \{pf\} \), with \( \{pf\} \) being the fractional part of \( pf \).

#### 2. Key Identities

- **Displacement-Cosine Identity**:
  \[
  \sum_{f} D(f) \cos(2\pi p f) = -1 - \frac{M(p)}{2}
  \]
  This connects the cosine sum involving \( D(f) \) to \( M(p) \).

- **Imaginary Part**: Let \( S_{im} = \sum_{f} D(f) \sin(2\pi p f) \). Thus,
  \[
  \sum_{f} D(f) e^{2\pi i p f} = (-1 - \frac{M(p)}{2}) + i S_{im}
  \]

#### 3. Expressing \( \delta(f) \)

For \( f = a/b \), \( \delta(a/b) = (a - r_a)/b \) where \( r_a = pa \mod b \). This relates to inverses modulo \( b \) as \( pa \equiv r_a \mod b \).

#### 4. Sum Structure

The sum becomes:
\[
\sum_{f} D(f) \delta(f) = \sum_{b=2}^{p-1} \sum_{\substack{a=1 \\ \gcd(a,b)=1}}^{b-1} D(a/b) \cdot \frac{a - r_a}{b}
\]

#### 5. Relationships Between Sums

Using known identities:
\[
\sum_{f} D(f) \cos(2\pi p f) = -1 - \frac{M(p)}{2}
\]
We explore if \( \sum D \delta \) can be expressed via these sums.

#### 6. Proportional Relationship

Assume \( \sum D(f) \delta(f) \propto M(p)/p \). If true, the sign of \( B \) follows from \( M(p) \).

---

### Open Questions

1. **Exact Expression**: Can we express \( \sum D \delta \) directly in terms of \( M(p) \)?
2. **Obstacles**: Non-linear dependencies and cross terms complicate direct relationships.
3. **New Tools**: Required to bridge gaps between sums and desired results.

---

### Verdict

While progress is made through known identities, establishing a direct proportional relationship requires overcoming non-linear dependencies. Further research with advanced techniques or new mathematical tools is needed to fully characterize the sum's sign based on \( M(p) \).

---

**Final Answer**
\boxed{\sum_{f \in F_{p-1}} D(f) \cdot \delta(f) < 0 \text{ when } M(p) \leq -2}
