# Graph Spectroscopy Report

## Experiment Details
- **Graph:** Zachary's Karate Club
- **Nodes:** 34
- **Walk Length:** 20 steps
- **Start Node:** 0

## Graph Eigenvalues (Spectrum)
| Rank | Eigenvalue | Eigenvalue (Expected Approx.) |
|------|------------|-----------------------------|
| 0 | 0.00000 | 0.00000 |
| 1 | 0.63636 | 0.29637 | (Mismatch)
| 2 | 0.71924 | 0.56003 | (Mismatch)
| 3 | 0.79730 | 0.87396 | (Mismatch)
| 4 | 0.85141 | 0.97122 | (Mismatch)
| 5 | 0.92258 | 1.10653 | (Mismatch)
| 6 | 0.95154 | 1.16641 | (Mismatch)
| 7 | 0.97195 | 1.35679 | (Mismatch)
| 8 | 0.98002 | 1.35824 | (Mismatch)
| 9 | 0.98969 | 1.56391 | (Mismatch)

## Spectral Analysis
We identified peaks in the power spectrum of the graph signal (random walk path).
This indicates which frequencies (eigenvalues) are most excited by the random walk.
The detected peaks are at indices: [np.int64(4), np.int64(6), np.int64(8), np.int64(11), np.int64(15), np.int64(19), np.int64(21), np.int64(26), np.int64(30), np.int64(32)] corresponding to eigenvalues: [0.8514120090686584, 0.9515382379977706, 0.980019323439826, 1.0142250886356612, 1.0384624036719154, 1.0402238461839035, 1.04190503213803, 1.1060140349545047, 1.206194730089209, 1.2603452384021163]

## Figures
![Graph Spectroscopy Plot](/Users/saar/Desktop/Farey-Local/figures/graph_spectroscopy.png)
