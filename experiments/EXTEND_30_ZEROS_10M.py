import numpy as np

# Known zeros (gamma values)
GAMMA_ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 
               40.9187, 43.3271, 48.0052, 49.7738, 52.9703, 56.4462, 
               59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 
               75.7047, 77.1448, 79.3374, 82.9104, 84.7355, 87.4253, 
               88.8091, 92.4919, 94.6514, 95.8706, 98.8312, 101.318]

N = 10000000
MAX_GAMMA = 120.0
MIN_GAMMA = 5.0
NUM_GAMMA_POINTS = 30000
CHUNK_SIZE = 100000
Z_THRESHOLD = 3.0

# Step 1: Sieve Mobius function up to N using linear sieve
def sieve_mobius_linear(n):
    """Linear sieve to compute Mobius function and primes"""
    mu = np.zeros(n + 1, dtype=np.int8)
    mu[1] = 1
    primes = []
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    
    return mu, primes

mu, primes = sieve_mobius_linear(N)
print(f"Sieved up to {N}, found {len(primes)} primes")

# Step 2: Compute F_comp(gamma) = gamma^2 * |sum M(p)/p * exp(-igamma*log(p))|^2
print("Computing F_comp spectrum...")
gammas = np.linspace(MIN_GAMMA, MAX_GAMMA, NUM_GAMMA_POINTS)
F_comp = np.zeros(len(gammas))

# Precompute log(p) for efficiency
primes_arr = np.array(primes, dtype=np.float64)
log_primes = np.log(primes_arr)

# For primes, μ(p) = -1, so M(p)/p = -1/p
# Process in chunks to manage memory
num_chunks = len(primes_arr) // CHUNK_SIZE + 1

for chunk_idx in range(num_chunks):
    chunk_start = chunk_idx * CHUNK_SIZE
    chunk_end = min(chunk_start + CHUNK_SIZE, len(primes_arr))
    chunk_primes = primes_arr[chunk_start:chunk_end]
    chunk_log_primes = log_primes[chunk_start:chunk_end]
    
    # μ(p) = -1 for all primes
    chunk_mu_p = -np.ones(len(chunk_primes), dtype=np.float64)
    
    # Accumulate contribution to F_comp for each gamma point
    for i, gamma in enumerate(gammas):
        exponent = -1j * gamma * chunk_log_primes
        sum_val = np.sum(chunk_mu_p / chunk_primes * np.exp(exponent))
        F_comp[i] += gamma**2 * np.abs(sum_val)**2

print(f"Computed F_comp for {len(gammas)} gamma points")

# Step 3: Compute z-scores for each known zero
print("Computing z-scores for known zeros...")
results = []

for gamma in GAMMA_ZEROS:
    if gamma < MIN_GAMMA or gamma > MAX_GAMMA:
        results.append((gamma, None, None, None))
        continue
    
    # Find closest gamma point
    idx = np.argmin(np.abs(gammas - gamma))
    F_value = F_comp[idx]
    
    # Compute local z-score using a window around the target gamma
    local_window = 50  # Number of points on each side
    start = max(0, idx - local_window)
    end = min(len(gammas), idx + local_window + 1)
    
    F_local = F_comp[start:end]
    local_mean = np.mean(F_local)
    local_std = np.std(F_local)
    
    if local_std > 1e-10:
        z_score = (F_value - local_mean) / local_std
    else:
        z_score = 0.0
    
    detected = z_score > Z_THRESHOLD
    results.append((gamma, F_value, z_score, detected))

# Step 4: Report results
detected_count = sum(1 for _, _, _, detected in results if detected)

print("\n=== Compensated Mertens Spectroscope Results ===")
print(f"Primes analyzed: {len(primes)}")
print(f"Gamma range: [{MIN_GAMMA}, {MAX_GAMMA}]")
print(f"Gamma points: {len(gammas)}")
print(f"\nZ-score threshold: {Z_THRESHOLD}")
print(f"Zeros detected: {detected_count}/{len(GAMMA_ZEROS)}")

print("\nDetailed Results:")
print(f"{'Gamma':>12} {'F_comp':>12} {'Z-score':>10} {'Detected':>10}")
print("-" * 50)
for gamma, F_val, z_score, detected in results:
    if gamma is not None:
        detected_str = "Yes" if detected else "No"
        print(f"{gamma:>12.4f} {F_val:>12.4f} {z_score:>10.3f} {detected_str:>10}")

print(f"\nTotal detected: {detected_count} out of {len(GAMMA_ZEROS)} zeros")
