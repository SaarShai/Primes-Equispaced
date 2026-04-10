# Experimental Protocol: Graph Mertens Spectroscopy

## 1. Objective
To empirically validate the speculative hypothesis: **Can Graph Laplacian eigenvalues be detected as spectral peaks by applying a frequency transform to the spatial residuals of a random walk (the "Graph Mertens Function")?**

## 2. The Hypothesis
*   **Null Hypothesis:** The spatial distribution of random walk residuals ($M_G$) is random noise. No correlation exists between node index features and Laplacian eigenvalues.
*   **Alternative Hypothesis:** There exists a mapping where the node index (or node features) acts as a "spatial frequency" variable, such that the Fourier/Z-transform of the residuals $M_G$ exhibits peaks at magnitudes corresponding to $\lambda_k$ (Laplacian eigenvalues).
*   **Refinement:** Since graphs are not temporal sequences, the "frequency variable" $\omega$ is abstract. We will test two definitions of the frequency variable:
    1.  **Node ID ($i$):** Treating node $1 \dots N$ as a 1D signal (unstructured).
    2.  **Fiedler Coordinate ($\phi_2$):** Treating nodes sorted by their second eigenvector as a signal (structured).

## 3. Materials & Methods

### 3.1 Graph Data
*   **Graph:** Zachary's Karate Club (34 nodes).
*   **Ground Truth:** Compute the combinatorial Laplacian $L = D - A$ and Normalized Laplacian $\mathcal{L} = I - D^{-1/2}AD^{-1/2}$. Extract sorted eigenvalues $\lambda_1, \dots, \lambda_{34}$.

### 3.2 Random Walk Data Generation
*   **Algorithm:** Simple Symmetric Random Walk.
*   **Length ($T$):** $10^6$ steps (sufficient for convergence and high signal-to-noise ratio).
*   **Metric:** For each node $k \in \{0, \dots, 33\}$, count total visits $V_k$.
*   **Expected Visits:** $E_k = T \cdot \frac{\text{deg}(k)}{2|E|}$ (Stationary distribution of RW).
*   **Residuals:** $M_G(k) = V_k - E_k$.

### 3.3 The "Graph Spectroscope"
We treat the residual vector $M_G \in \mathbb{R}^{34}$ as a signal. We apply a generalized Discrete Fourier Transform (DFT) over a continuous frequency parameter $\omega$.

**The Frequency Variable ($f$):**
To test the "node features" requirement, we define the phase base for each node $k$ as $f_k$.
*   **Test A (Naive):** $f_k = k$ (Node Index).
*   **Test B (Spectral Ordering):** Sort nodes by Fiedler vector $\phi_2(k)$, then set $f_k$ based on sorted rank.
*   **Test C (Laplacian Ordering):** Sort nodes by Laplacian eigenvector $\phi_N(k)$.

**The Transform:**
$$ S(\omega) = \left| \sum_{k=0}^{N-1} M_G(k) \cdot e^{-i \omega \cdot f_k} \right| $$
*   **Frequency Sweep:** $\omega \in [0, 10]$ (arbitrary units, normalized).
*   **Output:** A spectral density plot $S(\omega)$.

### 3.4 Validation Criteria
*   **Peak Detection:** Identify local maxima in $S(\omega)$.
*   **Correlation:** Compare the $\omega$-positions of peaks against the normalized Laplacian eigenvalues $\lambda_{Laplacian}$.
*   **Sensitivity:** Check if peaks shift when $T$ (walk length) changes (should stabilize).

---

## 4. Python Implementation

The following script executes the full test design.

```python
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh
from scipy.signal import find_peaks

def run_mertens_spectroscope_test():
    print("--- Loading Zachary's Karate Club ---")
    G = nx.karate_club_graph()
    N = G.number_of_nodes()
    edges = list(G.edges())
    M = len(edges)
    
    # 1. Ground Truth: Laplacian Eigenvalues
    # Compute Normalized Laplacian: L = I - D^(-1/2) A D^(-1/2)
    A = nx.to_numpy_array(G)
    D = np.diag(np.diag(A.sum(axis=1)))
    D_sqrt_inv = np.diag(1 / np.sqrt(np.diag(D) + 1e-9))
    L = np.eye(N) - D_sqrt_inv @ A @ D_sqrt_inv
    
    # Eigenvalues of the Laplacian (sorted ascending)
    # We use numpy.eigvalsh for symmetric matrices
    laplacian_eigs, _ = np.linalg.eigh(L)
    eigenvalues = np.sort(laplacian_eigs)[1:] # Exclude 0 eigenvalue (lambda_1=0)
    
    print(f"Ground Truth Eigenvalues (N={N}, M={M}):")
    print(f"Min: {eigenvalues[1]:.4f}, Max: {eigenvalues[-1]:.4f}")
    print(f"Top 5 Eigenvalues: {eigenvalues[-5:]}")

    # 2. Random Walk Data Generation
    print("\n--- Generating Random Walk Data ---")
    steps = 1000000
    current_node = 0
    visits = np.zeros(N, dtype=int)
    
    # Precompute adjacency indices for speed
    adj_list = np.array(list(G.neighbors(current_node)))
    
    # Warmup
    for _ in range(1000):
        current_node = np.random.choice(G.neighbors(current_node))
    
    # Main Walk
    for t in range(steps):
        current_node = np.random.choice(list(G.neighbors(current_node)))
        visits[current_node] += 1
    
    # 3. Compute Graph Mertens Function M_G
    # Expected visits based on stationary distribution pi_i = deg(i) / 2M
    degrees = np.array([d for n, d in G.degree()])
    stationary_dist = degrees / (2 * M)
    expected_visits = steps * stationary_dist
    
    # Residuals
    M_G = visits - expected_visits
    
    # 4. The Spectroscope
    print("\n--- Running Spectroscope (Transforming M_G) ---")
    
    # We sweep a frequency parameter 'w' to see if peaks emerge
    # Mapping node index to a 'phase' using node features as per prompt
    frequencies_to_test = [
        ("Node Index", lambda k: k),
        ("Fiedler Rank", lambda k: np.argsort(laplacian_eigs)[0][np.argsort(laplacian_eigs)[1][k]]),
    ]
    
    # For Fiedler, we need to sort nodes by eigenvector to establish a linear order
    # We will compute the eigenvectors to map the nodes to a 1D line
    _, phi = eigsh(L, k=2, sigma=1.0, which='SA') # Second eigenvector (Fiedler)
    # Phi[:,1] corresponds to lambda_2. Normalize and get rank
    fiedler_coords = phi[:, 1]
    node_order_fiedler = np.argsort(fiedler_coords)
    
    # Feature mapping function for Fiedler: Map node index -> sorted position
    fiedler_feature_map = {node: idx for idx, node in enumerate(node_order_fiedler)}
    
    feature_types = {
        "Node_Index": lambda n: n,
        "Fiedler_Order": lambda n: fiedler_feature_map[n],
        "Laplacian_Eigenvector": lambda n: fiedler_coords[n] # Using coords directly
    }
    
    results = {}
    
    for name, feat_fn in feature_types.items():
        print(f"\nAnalyzing transform based on feature type: {name}")
        
        # Compute the "Spectrum" over a range of w
        # w is the frequency variable in the exponent e^{i * w * feature}
        w_range = np.linspace(0, 2 * np.pi * 20, 1000)
        spectral_magnitude = []
        phases = []
        
        for w in w_range:
            transform_sum = 0
            for n in range(N):
                feature_val = feat_fn(n)
                # Phase base: e^{i * w * feature_val}
                phase = np.exp(1j * w * feature_val)
                transform_sum += M_G[n] * phase
            spectral_magnitude.append(np.abs(transform_sum))
            phases.append(w)
            
        spectral_magnitude = np.array(spectral_magnitude)
        
        # Find peaks
        # Note: Peaks might be sparse in 1D signal; expect broad structure
        peaks, _ = find_peaks(spectral_magnitude, height=np.max(spectral_magnitude)*0.2)
        peak_positions = np.array(phases)[peaks]
        
        results[name] = {
            "peak_positions": peak_positions,
            "spectrum": spectral_magnitude,
            "w_range": w_range
        }
        
        print(f"Detected {len(peak_positions)} peaks at frequencies: {peak_positions[:5]}...")

    # 5. Visualize Results vs Ground Truth
    plt.figure(figsize=(12, 8))
    
    # Plot Ground Truth Eigenvalues on x-axis
    # But since eigenvalues are not 'frequencies' in the signal, we plot them as markers
    
    for name, res in results.items():
        plt.plot(res['w_range'], res['spectrum'], label=f'{name} Transform')
    
    plt.axhline(0, color='black', linewidth=0.5)
    plt.xlabel("Frequency Variable ($\omega$)")
    plt.ylabel("Magnitude of Mertens Spectroscope")
    plt.title("Graph Mertens Spectroscope: Node Residuals vs Frequency")
    plt.legend()
    plt.grid(True)
    
    # Overlay Ground Truth Eigenvalues as vertical markers
    # We must map Eigenvalues to 'w' axis?
    # Hypothesis: Do peaks align with lambda_k?
    # Since we don't know the scaling, we just plot them as a reference
    # Let's assume eigenvalues might be the frequencies themselves?
    # If lambda ~ 0 to 2, we look for peaks there.
    
    plt.scatter(eigenvalues, np.zeros_like(eigenvalues), c='red', s=100, 
                label='Ground Truth Eigenvalues (Projected)', marker='v')
    
    plt.show()
    
    # 6. Analysis Report
    print("\n--- Analysis Summary ---")
    print("To determine if the hypothesis holds, compare the x-positions of the red triangles (Eigenvalues)")
    print("against the x-positions of the highest peaks in the blue lines (Spectroscope).")
    print("If the spectral peaks align with the eigenvalues, the hypothesis is supported.")
    print("If they are random or uniform, the 'node feature exponent' hypothesis is likely incorrect.")

    return results

if __name__ == "__main__":
    run_mertens_spectroscope_test()
```

---

## 5. Critical Analysis of the Design

### The "Frequency Variable" Challenge
The core theoretical issue here is the mismatch between **Spectral Graph Theory** and **Signal Processing**.
1.  **Laplacian Eigenvalues ($\lambda_k$)** represent *temporal decay rates* of diffusion. They are the poles of the transfer function $H(z) = (zI - L)^{-1}$. They are not frequencies of the node index $k$.
2.  **Mertens Function ($M_G$)** is a spatial vector. Applying a DFT over node indices assumes the nodes are ordered sequentially in a topological sense (like a time series). Karate Club nodes are arbitrary labels (0-33). The "spatial frequency" of the residual $M_G$ tells us about the *smoothness* of the deviation on the graph, not the *eigenvalues*.

### Why Test This?
Despite the theoretical mismatch, the test is designed to be **exploratory**.
*   If the DFT peaks align with eigenvalues, it implies a surprising isomorphism between node-ordered residuals and spectral decay rates (highly unlikely for arbitrary graphs).
*   However, if we use the **Fiedler Order** as the exponent base, we transform the 34 nodes into a 1D line where adjacent nodes are topologically close. In this case, a "spatial frequency" in the Fiedler domain corresponds to the Laplacian eigenvalues of the *line*, which might approximate the graph eigenvalues better than arbitrary indices.

### The Real "Spectroscope" for Random Walks
While the user requested a node-based test, standard Random Walk theory dictates that eigenvalues are detected via **Time-Domain** analysis, not **Node-Domain** analysis.
*   **True Method:** Record the binary state of a single node $X_t$ over time (1 if at node, 0 otherwise).
*   **Power Spectral Density (PSD):** The PSD of $X_t$ will show peaks at frequencies related to $\lambda_k$ of the transition matrix $P$.
*   **Relation:** The spectral density $S(\omega)$ of the walk is approximately $\sum_k \frac{a_k}{1 - \lambda_k \cos(\omega)}$.
*   **Correction:** This implementation tests the user's specific idea (Node-Feature Spectroscope) to validate its failure or unexpected success. I will recommend the Time-Domain approach as the robust alternative in the conclusion.

## 6. Interpretation Plan
After running the code:
1.  **Check Alignment:** Do the peaks of the `Fiedler_Order` transform align with the red `Eigenvalues` markers?
2.  **Check Magnitude:** Do the peaks have significant magnitude relative to the noise floor (indicated by the `Node_Index` transform)?
3.  **Conclusion:**
    *   **Success:** Peaks in `Fiedler_Order` align with Eigenvalues. (Implies nodes sorted by eigenvector have spatial frequencies matching eigenvalues).
    *   **Failure:** No alignment. (Implies Eigenvalues are temporal properties, not spatial ones).
    *   **Recommendation:** Switch to analyzing the **Autocorrelation of the walk**, which is theoretically proven to reveal $\lambda_k$.
