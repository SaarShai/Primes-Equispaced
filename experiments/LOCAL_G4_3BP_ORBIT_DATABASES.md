To find a dataset large enough to test a "periodic table" of orbits, you are looking for high-density orbital catalogs. Currently, the field is fragmented because most researchers publish "discoveries" rather than "databases."

Here many the specifics regarding your requested sources and the current state of larger datasets.

### 1. Suvakov-Dmitrasinović (2013)
*   **Orbit Count:** This study identified approximately **150 to 200** periodic orbits.
*   **Context:** While groundbreaking for using genetic algorithms to navigate the phase space, it was significantly smaller than the Li-Liao catalog. It focused more on the "stability" and "diversity" of the orbits found rather than an exhaustive brute-force search. It serves as the structural predecessor to the Li-Liao work.

### 2. Li-Liao Extended Catalogs
*   **Status:** As of the most recent major publications, the **695 orbits** in the Li-Liao (2017) catalog remain the standard "large" benchmark for equal-mass choreographies.
*   **Extension:** There is no widely recognized "Li-Liao 2000" catalog. However, researchers are currently attempting to extend this by using **Neural Networks (NN)** to predict initial conditions. If you are looking for "extended" versions, you must look for papers specifically using "Deep Learning for the Three-Body Problem," as these are the only ones capable of pushing the count toward the thousands.

### 3. Hristov et al.
*   **Focus:** Hristov’s work (often involving Carles or Simó) focuses less on "raw lists of orbits" and more on **Topological Classification (Braid Theory)**.
*   **Utility:** Hristov provides the "rules" for what orbits *can* exist. His work is better for validating whether your periodic table respects the topological invariants (braid group indices) rather than providing a massive CSV of orbital parameters.

### 4. Montgomery (Figure-Eight Family)
*   **The "Family" Concept:** Montgomery and Chenciner didn't provide a database; they provided a **mathematical template**. The "Figure-Eight family" refers to the fact that the figure-eight orbit is a single point in a continuous manifold of periodic solutions.
*   **Limitation:** You cannot use the "Figure-Eight family" as a database of different orbits, because they are all essentially "deformations" of the same fundamental topological shape.

### 5. Any database with >1000 orbits?
Currently, **no single, peer-reviewed, verified database of >1000 distinct, stable, periodic three-body orbits exists in a single downloadable format.**

The bottleneck is **Verification**. Finding a candidate orbit is easy; proving it is periodic and stable via high-precision integration (to ensure it isn't just a long-period transient) is computationally expensive. 
*   **The "Hidden" 1000+:** There are likely thousands of orbits existing in the "numerical noise" of recent AI-driven searches, but they lack the "Gold Standard" verification required to be included in a formal catalog like Li-Liao.

### 6. Any with unequal masses?
**This is your best path to a larger dataset.** 
The Li-Liao catalog is heavily constrained by $m_1 = m_2 = m_3$. If you relax the mass constraint, the dimensionality of the search space increases, but the number of possible periodic solutions explodes.

To find a larger "periodic table," you should look for:
*   **Mass-Ratio Scans:** Look for papers focusing on **"Mass-ratio variation in the three-body problem."** 
*   **The $m_1 \gg m_2, m_3$ regime:** There are much larger catalogs of "Hierarchical" orbits (where two bodies form a tight binary and the third is distant). These can easily exceed 1,000 orbits because they behave more like perturbed Keplerian problems.
*   **Key Researchers to follow:** Look for recent work involving **Symplectic Integrators** applied to **Mass-Ratio Space**.

### Summary Recommendation for your "Periodic Table" Testing:

| If you need... | Look for... |
| :--- | :--- |
| **High-quality, verified base** | Li-Liao (695 orbits) |
| **Structural/Topological rules** | Hristov / Braid Group Theory |
| **Scalability (Mass variation)** | Papers on "Mass-ratio-dependent periodic orbits" |
| **Potential for >1000 orbits** | AI/Machine Learning-driven searches (Search terms: "Neural Network Three-Body Orbit Discovery") |

**Strategy Tip:** If you are testing a "periodic table" (implying a pattern in the orbital properties), you should attempt to generate your own synthetic dataset by taking the Li-Liao orbits and applying a **mass-perturbation script**. This will allow you to create a "synthetic" catalog of 1,000+ orbits where you already know the "ground truth" of the underlying physics.
