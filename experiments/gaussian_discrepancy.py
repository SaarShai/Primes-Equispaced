#!/usr/bin/env python3
"""
Gaussian Farey Discrepancy Analysis
Tests oscillatory behavior of 2D star discrepancy against L-function zero prediction.
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import os

# Configuration
TARGET_NORMS = [2, 5, 13, 17, 29, 37, 41, 49]
GAMMA_1 = 6.0209  # First zero of L(s, chi_4)
PHASE_SHIFT = 0.0 # Unknown phase phi'; set to 0 for baseline
N_SAMPLES = 10000 # Monte Carlo samples for discrepancy
OUTPUT_DIR = "~/Desktop/Farey-Local/experiments/"

def gaussian_integers_with_norm(n):
    """Generate Gaussian integers a+bi such that a^2 + b^2 = n."""
    points = []
    limit = int(math.isqrt(n))
    for a in range(-limit, limit + 1):
        b_sq = n - a*a
        if b_sq >= 0:
            b = int(math.isqrt(b_sq))
            if b*b == b_sq:
                points.append((a, b))
                if b != 0:
                    points.append((a, -b))
    return points

def is_coprime(a, b, c, d):
    """Check if Gaussian integer (a+bi) is coprime to (c+di).
    Simplified check: gcd(N(a+bi), N(c+di)) = 1 is necessary but not sufficient.
    For Farey sequences, we require gcd(a+bi, c+di) = 1 in Z[i].
    Approximation: gcd(a^2+b^2, c^2+d^2) = 1 is often used for computational speed.
    Strict check requires Euclidean algorithm in Z[i].
    """
    # Using norm gcd as a proxy for Z[i] gcd for speed in this context
    # Note: This is a heuristic. Strict Z[i] gcd is safer.
    norm_num = a*a + b*b
    norm_den = c*c + d*d
    return math.gcd(norm_num, norm_den) == 1

def compute_star_discrepancy(points, n_samples=N_SAMPLES):
    """
    Compute 2D Star Discrepancy D*(S) via Monte Carlo.
    S is a list of (x, y) in [0, 1)^2.
    """
    if not points:
        return 0.0
    
    points = np.array(points)
    n_points = len(points)
    max_diff = 0.0
    
    for _ in range(n_samples):
        # Sample random rectangle [0, a] x [0, b]
        a = np.random.rand()
        b = np.random.rand()
        
        # Count points in rectangle
        # Vectorized check
        in_rect = (points[:, 0] < a) & (points[:, 1] < b)
        count = np.sum(in_rect)
        
        # Discrepancy contribution
        area = a * b
        diff = abs(count / n_points - area)
        if diff > max_diff:
            max_diff = diff
            
    return max_diff

def get_gaussian_farey_layer(norm):
    """
    Generate fractions a/c with N(c) = norm.
    Map to [0, 1)^2.
    """
    fractions = []
    # Generate denominators c = c_r + i c_i
    denoms = gaussian_integers_with_norm(norm)
    
    # Filter units to avoid duplicates (associates)
    # We want unique fractions. c and u*c generate same fractions if we vary a.
    # Standard Farey: c in fundamental domain? 
    # Simplified: Iterate all c, reduce fraction a/c.
    # To avoid duplicates, we can enforce a canonical representative for c.
    # For this script, we iterate all c and check gcd.
    
    # To ensure uniqueness of fractions a/c, we need to handle associates.
    # We will collect all a/c and use a set to deduplicate.
    seen = set()
    
    for cr, ci in denoms:
        c = complex(cr, ci)
        if c == 0: continue
        
        # Numerators a = ar + i ai
        # Range for a: roughly same magnitude as c to cover [0,1)^2?
        # Farey fractions are usually defined with N(a) < N(c) or similar.
        # For 2D, we consider a/c mod 1.
        # We iterate a in a box around 0.
        # To cover [0,1), we need a/c to cover the torus.
        # We iterate a such that N(a) < N(c) is not strictly required for [0,1),
        # but we need a/c mod 1.
        # We iterate a in range [-c, c] roughly.
        
        # Efficient generation:
        # a/c = (ar + i ai) / (cr + i ci) = ((ar+aii)(cr-ici)) / N(c)
        # Real part: (ar*cr + ai*ci) / N(c)
        # Imag part: (ai*cr - ar*ci) / N(c)
        
        # We need to find a such that gcd(a, c) = 1.
        # We iterate a in a range that covers one period.
        # Period is c. So a in [0, c) roughly.
        # Let's iterate a in a box of size N(c).
        
        # Heuristic: Iterate a_r, a_i in range [-limit, limit]
        limit = int(math.sqrt(norm)) + 1
        for ar in range(-limit, limit):
            for ai in range(-limit, limit):
                a = complex(ar, ai)
                if a == 0: continue
                
                # Check coprimality
                # Strict Z[i] gcd check is expensive. 
                # Using norm gcd as proxy for this experiment.
                if not is_coprime(ar, ai, cr, ci):
                    continue
                
                # Compute fraction
                num = a * np.conj(c)
                den = norm
                x = (num.real / den) % 1.0
                y = (num.imag / den) % 1.0
                
                # Round to avoid float issues
                x = round(x, 10)
                y = round(y, 10)
                
                if (x, y) not in seen:
                    seen.add((x, y))
                    fractions.append((x, y))
                    
    return fractions

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    cumulative_points = []
    results = []
    
    print(f"{'Norm':<6} | {'|S_n|':<8} | {'D*':<10} | {'Delta D*':<10} | {'Pred Sign':<10} | {'Match':<6}")
    print("-" * 60)
    
    prev_D = 0.0
    prev_norm = 0
    
    for n in TARGET_NORMS:
        layer = get_gaussian_farey_layer(n)
        cumulative_points.extend(layer)
        
        # Compute D*
        D_curr = compute_star_discrepancy(cumulative_points)
        delta_D = D_curr - prev_D
        
        # Prediction
        pred_val = math.cos(GAMMA_1 * math.log(n) + PHASE_SHIFT)
        pred_sign = 1 if pred_val > 0 else -1
        
        # Match check (sign of delta D vs sign of pred)
        # Note: D* usually decreases, so delta D is negative.
        # We check if the oscillation in delta D matches the oscillation in pred.
        match = "Yes" if (delta_D < 0 and pred_sign < 0) or (delta_D > 0 and pred_sign > 0) else "No"
        
        results.append({
            'norm': n,
            'size': len(cumulative_points),
            'D_star': D_curr,
            'delta_D': delta_D,
            'pred_val': pred_val,
            'match': match
        })
        
        print(f"{n:<6} | {len(cumulative_points):<8} | {D_curr:<10.6f} | {delta_D:<10.6f} | {pred_sign:<10} | {match:<6}")
        
        prev_D = D_curr
        prev_norm = n

    # Plot
    plt.figure(figsize=(10, 6))
    norms = [r['norm'] for r in results]
    delta_Ds = [r['delta_D'] for r in results]
    preds = [r['pred_val'] for r in results]
    
    plt.subplot(2, 1, 1)
    plt.plot(norms, delta_Ds, 'o-', label='Delta D*')
    plt.ylabel('Delta D*')
    plt.title('Discrepancy Change vs Norm')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(norms, preds, 's-', label='Prediction (cos)', color='orange')
    plt.ylabel('Prediction Sign')
    plt.xlabel('Norm n')
    plt.title('L-function Zero Prediction')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "gaussian_farey_discrepancy_plot.png"))
    plt.close()
    
    # Save Table
    with open(os.path.join(OUTPUT_DIR, "gaussian_farey_discrepancy_table.txt"), "w") as f:
        f.write("Norm\tSize\tD*\tDelta D*\tPred Val\tMatch\n")
        for r in results:
            f.write(f"{r['norm']}\t{r['size']}\t{r['D_star']:.6f}\t{r['delta_D']:.6f}\t{r['pred_val']:.6f}\t{r['match']}\n")
            
    print("\nResults saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
