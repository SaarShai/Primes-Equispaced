#!/usr/bin/env python3
# MPR-41a: Gaussian Farey Fractions & 2D Discrepancy
# Author: Research Assistant
# Date: 2023-10-27
# Constraints: Unconditional, Computational Verification only.

import os
import math
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
N_MAX = 50
OUTPUT_DIR = os.path.expanduser("~/Desktop/Farey-Local/experiments")
SCRIPT_PATH = os.path.join(OUTPUT_DIR, "gaussian_farey.py")
RESULTS_PATH = os.path.join(OUTPUT_DIR, "GAUSSIAN_FAREY_RESULTS.md")
PLOT_PATH = os.path.join(OUTPUT_DIR, "gaussian_farey_N50.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Gaussian Integer Class ---
class GaussianInt:
    def __init__(self, a, b=0):
        self.a = int(a)
        self.b = int(b)
    
    def __repr__(self):
        return f"{self.a}+{self.b}i"
    
    def norm(self):
        return self.a**2 + self.b**2
    
    def __add__(self, other):
        return GaussianInt(self.a + other.a, self.b + other.b)
    
    def __sub__(self, other):
        return GaussianInt(self.a - other.a, self.b - other.b)
    
    def __mul__(self, other):
        return GaussianInt(self.a*other.a - self.b*other.b, self.a*other.b + self.b*other.a)
    
    def __truediv__(self, other):
        # Complex division for float approx
        denom = other.norm()
        return (self.a*other.a + self.b*other.b)/denom, (-self.a*other.b + self.b*other.a)/denom
    
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
    
    def __hash__(self):
        return hash((self.a, self.b))

def gcd_gaussian(a, b):
    """Euclidean algorithm for Z[i]. Returns gcd."""
    while b.norm() > 0:
        # Quotient q = round(a/b)
        qa, qb = a / b
        q = GaussianInt(round(qa), round(qb))
        r = a - q * b
        a, b = b, r
    return a

def is_gaussian_prime(n):
    """Check if integer n is a norm of a Gaussian prime."""
    # Gaussian primes have norms:
    # 1. 2 (from 1+i)
    # 2. p where p is rational prime, p = 2 or p = 1 mod 4 (from a+bi)
    # 3. p^2 where p is rational prime, p = 3 mod 4 (from p)
    # We check if n is a norm of a prime.
    # If n is prime in Z and n=2 or n%4==1 -> Prime norm.
    # If n is square of prime in Z and prime%4==3 -> Prime norm.
    # Note: 1 is not prime.
    if n == 2: return True
    if n == 1: return False
    
    # Check if n is a rational prime
    is_prime_n = True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            is_prime_n = False
            break
    
    if is_prime_n:
        return True # p=2 or p=1 mod 4
    
    # Check if n = p^2 where p=3 mod 4
    root = int(math.sqrt(n))
    if root * root == n:
        p = root
        if p % 4 == 3:
            return True
    return False

def normalize_beta(beta):
    """Normalize beta to first quadrant: Re > 0 or (Re=0, Im > 0)."""
    # Units in Z[i]: 1, -1, i, -i.
    # We want beta in {z : Re(z)>0} U {z : Re(z)=0, Im(z)>0}
    # Multiply by unit u such that u*beta is in sector.
    # Sector covers 0 to 90 degrees.
    # Angle of beta:
    angle = math.atan2(beta.b, beta.a)
    # Map angle to [0, pi/2)
    # If angle in [0, pi/2), keep.
    # If angle in [pi/2, pi), multiply by -i (rotate -90).
    # If angle in [-pi, -pi/2), multiply by -1 (rotate 180).
    # If angle in [-pi/2, 0), multiply by i (rotate 90).
    
    # Simpler: Rotate until Re > 0 or (Re=0, Im>0).
    # Check 4 rotations.
    for u in [GaussianInt(1,0), GaussianInt(0,1), GaussianInt(-1,0), GaussianInt(0,-1)]:
        cand = beta * u
        if cand.a > 0 or (cand.a == 0 and cand.b > 0):
            return cand
    return beta # Should not happen

def enumerate_farey(N):
    """Enumerate Gaussian Farey fractions with denom norm <= N."""
    points = []
    denom_norms = {} # norm -> list of points
    
    # Generate all Gaussian integers beta with 1 <= norm <= N
    betas = []
    for a in range(-int(math.sqrt(N))-1, int(math.sqrt(N))+2):
        for b in range(-int(math.sqrt(N))-1, int(math.sqrt(N))+2):
            z = GaussianInt(a, b)
            if z.norm() == 0: continue
            if z.norm() > N: continue
            
            # Normalize beta
            z_norm = normalize_beta(z)
            if z_norm not in betas:
                betas.append(z_norm)
    
    for beta in betas:
        n = beta.norm()
        # Find alpha such that gcd(alpha, beta)=1 and alpha/beta in [0,1)^2
        # alpha must be in fundamental domain relative to beta.
        # We search a bounding box for alpha.
        # Since alpha/beta in [0,1), alpha approx beta * [0,1).
        # Range for alpha: Re in [0, Re(beta)+1], Im in [0, Im(beta)+1] roughly.
        # Safer: iterate alpha in range [-10, 10] + i[-10, 10]
        
        found_alphas = []
        # Search space for alpha
        # To ensure alpha/beta in [0,1)^2, we need 0 <= Re(alpha/beta) < 1
        # Re(alpha/beta) = (Re(alpha)Re(beta) + Im(alpha)Im(beta)) / |beta|^2
        # This is complex. We iterate alpha and check condition.
        
        # Bounding box for alpha:
        # alpha = beta * (x + iy), x,y in [0,1).
        # alpha approx beta * (0.5 + 0.5i).
        # Range: Re(alpha) in [min(0, Re(beta)-1), max(0, Re(beta)+1)]
        # We use a generous search range.
        limit = int(math.sqrt(N)) + 5
        for ra in range(-limit, limit+1):
            for ia in range(-limit, limit+1):
                alpha = GaussianInt(ra, ia)
                if gcd_gaussian(alpha, beta).norm() != 1:
                    continue
                
                # Check if in fundamental domain [0,1)^2
                # Compute alpha/beta
                # Use float division for check
                qa, qb = alpha / beta
                if 0 <= qa < 1 and 0 <= qb < 1:
                    found_alphas.append(alpha)
                    break # Found one representative for this beta in this quadrant?
                          # Wait, there are phi(beta) such alphas.
                          # We need ALL coprime alphas that map to [0,1)^2.
                          # The loop above breaks too early.
        
        # Correct approach: Iterate alpha in a fundamental domain of Z[i]/beta.
        # But simpler: Iterate alpha in range such that alpha/beta covers [0,1)^2.
        # The set of fractions is { alpha/beta : gcd=1, 0 <= Re < 1, 0 <= Im < 1 }.
        # We iterate alpha in a box large enough to cover the unit square when divided by beta.
        # Box size approx |beta|.
        
        # Re-do search for ALL valid alphas
        valid_alphas = []
        # Search range: alpha = beta * (x + iy).
        # x, y in [0, 1).
        # alpha approx beta * (0.5 + 0.5i).
        # We need to cover the whole unit square.
        # Let's iterate alpha in a box of size |beta| around 0.
        # Actually, just iterate alpha in range [-10, 10] + i[-10, 10] is enough for N=50.
        
        for ra in range(-10, 11):
            for ia in range(-10, 11):
                alpha = GaussianInt(ra, ia)
                if gcd_gaussian(alpha, beta).norm() != 1:
                    continue
                
                qa, qb = alpha / beta
                if 0 <= qa < 1 and 0 <= qb < 1:
                    valid_alphas.append(alpha)
        
        # Store points
        for alpha in valid_alphas:
            qa, qb = alpha / beta
            points.append((qa, qb))
            if n not in denom_norms:
                denom_norms[n] = []
            denom_norms[n].append((qa, qb))
            
    return points, denom_norms

def compute_discrepancy(points):
    """Compute Star Discrepancy D* in [0,1]^2."""
    if not points:
        return 0.0
    
    # Extract coordinates
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    n = len(points)
    
    # Sort for efficient calculation
    # D* = sup_{x,y} | (1/n) sum I(x_i <= x, y_i <= y) - xy |
    # We only need to check x in {x_i} U {0,1} and y in {y_i} U {0,1}
    
    # Optimization: Sort points by x
    sorted_points = sorted(points, key=lambda p: p[0])
    
    max_diff = 0.0
    
    # Iterate over all x thresholds
    # To be efficient, we can use a sweep-line or just iterate all unique x
    unique_x = sorted(list(set(xs + [0.0, 1.0])))
    unique_y = sorted(list(set(ys + [0.0, 1.0])))
    
    for x in unique_x:
        for y in unique_y:
            # Count points in [0,x] x [0,y]
            count = 0
            for p in points:
                if p[0] <= x and p[1] <= y:
                    count += 1
            
            empirical = count / n
            theoretical = x * y
            diff = abs(empirical - theoretical)
            if diff > max_diff:
                max_diff = diff
                
    return max_diff

def main():
    print(f"Enumerating Gaussian Farey fractions with denom norm <= {N_MAX}...")
    points, denom_norms = enumerate_farey(N_MAX)
    
    print(f"Total points found: {len(points)}")
    
    # Analyze Prime Norms
    prime_norms = [n for n in denom_norms if is_gaussian_prime(n)]
    prime_norms.sort()
    
    results = []
    for n in prime_norms:
        count = len(denom_norms[n])
        results.append((n, count))
    
    # Compute Discrepancy
    D_star = compute_discrepancy(points)
    print(f"Star Discrepancy D*: {D_star:.6f}")
    
    # Write Results
    with open(RESULTS_PATH, "w") as f:
        f.write(f"# Gaussian Farey Sequence Results (N={N_MAX})\n\n")
        f.write(f"Total Points: {len(points)}\n")
        f.write(f"Star Discrepancy D*: {D_star:.6f}\n\n")
        f.write("## New Fractions at Gaussian Prime Norms\n")
        f.write("| Norm | Count | Cumulative |\n")
        f.write("|---|---|---|\n")
        
        cumulative = 0
        for n, count in results:
            cumulative += count
            f.write(f"| {n} | {count} | {cumulative} |\n")
            
        f.write("\n## Full Denominator Norm Distribution\n")
        f.write("| Norm | Count |\n")
        f.write("|---|---|\n")
        for n in sorted(denom_norms.keys()):
            f.write(f"| {n} | {len(denom_norms[n])} |\n")
            
    # Plot
    plt.figure(figsize=(10, 10))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    plt.scatter(xs, ys, s=10, alpha=0.6)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title(f"Gaussian Farey Points (N={N_MAX})\nD*={D_star:.4f}")
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.grid(True, alpha=0.3)
    plt.savefig(PLOT_PATH)
    plt.close()
    
    print(f"Results saved to {RESULTS_PATH}")
    print(f"Plot saved to {PLOT_PATH}")

if __name__ == "__main__":
    main()
