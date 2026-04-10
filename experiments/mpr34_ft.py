# mpr34_ft_test.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data (Assume bc_verify_100000_c.csv contains 'p', 'DeltaW')
# Ensure data is filtered for qualifying primes (M(p) <= -3)
df = pd.read_csv('bc_verify_100000_c.csv')
p = df['p'].values
dW = df['DeltaW'].values

# 2. Precompute Logarithms and Signs
log_p = np.log(p)
signs = np.sign(dW)  # Corresponds to D(p)/|D(p)| in prediction

# 3. Define Gamma Grid [0, 50]
gammas = np.linspace(0, 50, 5000)
F = np.zeros_like(gammas, dtype=complex)

# 4. Compute Discrete FT (Direct Sum for Non-Uniform Grid)
# F(gamma) = sum_p sgn(DeltaW(p)) * exp(-i * gamma * log(p))
for i, g in enumerate(gammas):
    F[i] = np.sum(signs * np.exp(-1j * g * log_p))

# 5. Plot Power Spectrum |F(gamma)|^2
plt.figure(figsize=(10, 6))
plt.plot(gammas, np.abs(F)**2, label='Spectral Power')
plt.vlines([14.135, 21.022, 25.010], 0, 10000, colors='r', linestyles='--', label='Zeta Zeros')
plt.xlabel('Frequency $\gamma$')
plt.ylabel('$|F(\gamma)|^2$')
plt.title('MPR-34: Farey Discrepancy FT')
plt.legend()
plt.grid(True)
plt.savefig('mpr34_ft_result.png')
plt.show()
