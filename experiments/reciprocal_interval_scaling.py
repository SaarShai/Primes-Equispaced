#!/usr/bin/env python3
"""
Analyze scaling of I(p), I*(p), and the difference.
Focus on: does |I-I*|^2 / (p * logp) converge to a constant?
"""
import numpy as np

# Read the data from the computation and do a clean scaling analysis
def mertens_table(N):
    mu = np.zeros(N+1, dtype=np.int64)
    mu[1] = 1
    for i in range(1, N+1):
        for j in range(2*i, N+1, i):
            mu[j] -= mu[i]
    return np.cumsum(mu)

def compute_sums(N, M):
    Ip = sum(M[N // n] / n for n in range(1, N+1))
    Istar = sum(M[N // n] / (N + 1 - n) for n in range(1, N+1))
    return Ip, Istar

max_N = 10000
M = mertens_table(max_N)

# Collect data at selected primes
from sympy import primerange
import math

primes = list(primerange(100, 10001))
# Sample every 20th prime for cleaner output
sample = primes[::20]

print("Scaling analysis of I(p) and I-I*")
print("="*80)
print(f"{'p':>6} {'I(p)':>10} {'I/sqrt(p)':>10} {'I/p^0.4':>10} "
      f"{'I-I*':>10} {'(I-I*)/sqrt(p)':>15} {'(I-I*)/p^0.4':>13}")
print("-"*80)

data_p = []
data_I = []
data_diff = []

for p in sample:
    N = p - 1
    Ip, Istar = compute_sums(N, M)
    diff = Ip - Istar
    data_p.append(p)
    data_I.append(Ip)
    data_diff.append(diff)
    print(f"{p:6d} {Ip:10.4f} {Ip/math.sqrt(p):10.4f} {Ip/p**0.4:10.4f} "
          f"{diff:10.4f} {diff/math.sqrt(p):15.4f} {diff/p**0.4:13.4f}")

# Fit power law for I(p) and diff
data_p = np.array(data_p, dtype=float)
data_I = np.array(data_I)
data_diff = np.array(data_diff)

# Fit I(p) ~ -C * p^alpha
# Use log-log regression on |I(p)|
mask = data_I < 0  # I(p) is negative
logp = np.log(data_p[mask])
logI = np.log(-data_I[mask])
coeffs_I = np.polyfit(logp, logI, 1)
print(f"\nPower law fit for |I(p)|: exponent = {coeffs_I[0]:.4f}, constant = {np.exp(coeffs_I[1]):.4f}")
print(f"  i.e., |I(p)| ~ {np.exp(coeffs_I[1]):.3f} * p^{coeffs_I[0]:.3f}")

# Fit |I-I*| ~ C * p^alpha
logdiff = np.log(-data_diff)  # diff is negative
coeffs_d = np.polyfit(logp, logdiff[mask], 1)
print(f"\nPower law fit for |I-I*|: exponent = {coeffs_d[0]:.4f}, constant = {np.exp(coeffs_d[1]):.4f}")
print(f"  i.e., |I-I*| ~ {np.exp(coeffs_d[1]):.3f} * p^{coeffs_d[0]:.3f}")

# The key quantity: |I-I*|^2 / (p * logp)
print(f"\n{'p':>6} {'|I-I*|^2/(p*logp)':>20} {'|I-I*|^2/p':>15}")
print("-"*50)
for i, p in enumerate(data_p):
    d = data_diff[i]
    print(f"{int(p):6d} {d**2/(p*math.log(p)):20.6f} {d**2/p:15.6f}")

# What about |I(p)|^2 / (p * logp)?
print(f"\n{'p':>6} {'I(p)^2/(p*logp)':>20} {'I(p)^2/p':>15} {'I(p)^2/p^(2alpha)':>18}")
print("-"*60)
alpha = coeffs_I[0]
for i, p in enumerate(data_p):
    v = data_I[i]
    print(f"{int(p):6d} {v**2/(p*math.log(p)):20.6f} {v**2/p:15.6f} {v**2/p**(2*alpha):18.6f}")
