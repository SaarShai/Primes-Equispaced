This design proposes the **Mediant-Stream Protocol (MSP)**. Unlike traditional protocols that prioritize bit-rate reduction (compression), MSP prioritizes **information density per packet**, ensuring that the "value" of each transmitted byte is maximized relative to the uncertainty of the signal.

---

### 1. The Protocol Design: Mediant-Stream Protocol (MSP)

**Concept:** We treat the 1D signal as a continuous function $f(x)$ over the domain $x \in [0, 1]$. We define our sampling points using the hierarchy of the Farey Sequence $F_n$.

#### A. The Transmission Order (The Deterministic Logic)
The sender and receiver do not exchange a "map." Instead, they both execute the same generator:
1.  **Start** with $F_1 = \{ \frac{0}{1}, \frac{1}{1} \}$.
2.  **Iterate** through $n = 2, 3, \dots, N$.
3.  For each $n$, identify all new fractions $p/q$ such that $\text{gcd}(p, q) = 1$ and $q = n$. 
4.  **Transmit** the pair $(x_i, y_i)$, where $x_i$ is the normalized position and $y_i$ is the measured value.

*Note: This is equivalent to traversing the Stern-Brocot tree level by level.*

#### B. The Packet Structure
Each packet is a self-contained unit:
`[Packet_ID | Sequence_Index | Normalized_X | Value_Y | Checksum]`
*   `Sequence_Index`: The $k$-th point transmitted.
*   `Normalized_X`: The value $p/q$ (can be compressed using the denominator $q$ and numerator $p$).

#### C. The Reconstruction Algorithm (The Receiver)
At any point $k$ (even if the stream is severed), the receiver:
1.  Maintains a sorted list of received $x_i$ coordinates.
2.  For any $x \in [0, 1]$ not in the set, performs **Linear Interpolation** between the two closest neighbors in the current set $S_k$.
3.  Because of the Farey property, the "gap" between any two points is always being halved or subdivided by a mediant, ensuring the interpolation error is localized.

---

### 2. Comparative Analysis

| Feature | **Mediant-Stream (MSP)** | **Progressive JPEG** | **Van der Corput** | **Random Ordering** |
| :--- | :--- | :--- | :--- | :--- |
| **Domain Focus** | **Spatial/Temporal** (Directly samples $x$) | **Frequency** (Samples coefficients) | **Spatial** (Low-discrepancy) | **Spatial** (Stochastic) |
| **Progressive Nature** | Improves resolution by refining intervals. | Improves clarity by adding high-freq detail. | Improves coverage by filling gaps. | Improves coverage via density. |
| **Structural Logic** | **Hierarchical Mediant**: New points are midpoints of existing ones. | **DCT Coefficients**: Successive bits of frequency coefficients. | **Bit-reversal**: Deterministic but lacks "parent-child" relation. | **No Structure**: No way to predict the next gap. |
| **Optimal Coverage** | **Maximum**: Each point is the "best" possible split. | **Sub-optimal**: High-freqs don't necessarily fill spatial gaps. | **High**: Good for integration, less for interpolation. | **Poor**: High variance in error (clusters and voids). |

---

### 3. Concrete Application: Satellite Temperature Profiling

**Scenario:** A satellite is orbiting Earth, scanning a 1D longitudinal temperature strip across the equator. The sensor captures temperatures $T$ at longitudes $L \in [0, 360^\circ]$.

**Implementation:**
1.  **Normalization:** The satellite maps the longitude to $x = \text{Long}/360$.
2.  **Sampling:** As the satellite moves, it doesn't just sample at fixed intervals. It follows the Farey sequence. 
    *   First, it sends the "anchors": $0^\circ$ and $360^\circ$.
    *   Next, it sends $180^\circ$ (the $1/2$ point).
    *   Next, it sends $120^\circ$ and $240^\circ$ (the $1/3$ and $2/3$ points).
3.  **The "Interruption" Advantage:** If a solar flare interrupts the downlink after $k$ points, the ground station already has a high-fidelity "skeleton" of the Earth's temperature. They don't see a "blocky" image (like JPEG) or "noisy" gaps (like Random); they see a smooth, albeit less detailed, continuous curve.

---

### 4. Mathematical Error Bound

To calculate the error, we assume the temperature profile $f(x)$ is **Lipschitz continuous** with constant $L$ (i.e., $|f(x_1) - f(x_2)| \leq L|x_1 - x_2|$). 

The error $E$ at any point $x$ is the difference between the true value and the linear interpolation of the two nearest received points $x_a$ and $x_b$. The maximum error occurs at the midpoint of the largest gap.

**1. Relation between $k$ and $n$:**
The number of points in a Farey sequence of order $n$ is given by the sum of the totient function:
$$k \approx \sum_{i=1}^n \phi(i) \approx \frac{3n^2}{\pi^2}$$
Thus, the maximum denominator $n$ we have reached is $n \approx \pi \sqrt{\frac{k}{3}}$.

**2. The Maximum Gap:**
In a Farey sequence $F_n$, the maximum distance between any two adjacent points is at most $1/n$ (specifically, the gap is $1/q_i q_{i+1}$, but $1/n$ is the upper bound for the largest interval).

**3. The Error Bound:**
If the maximum gap is $\Delta x_{max} \approx \frac{1}{n}$, the maximum error $\epsilon$ for a Lipschitz function is:
$$\epsilon \leq \frac{L \cdot \Delta x_{max}}{2}$$
Substituting $n$ in terms of $k$:
$$\epsilon \leq \frac{L}{2 (\pi \sqrt{k/3})} = \frac{L \sqrt{3}}{2\pi \sqrt{k}}$$

**Conclusion:** The error bound decays at a rate of $\mathcal{O}(k^{-1/2})$. While this is slower than the $\mathcal{O}(k^{-1})$ of uniform sampling, the **Farey-based approach is superior** because it guarantees that the error is distributed uniformly across the domain, preventing "blind spots" in the satellite's thermal scan.
