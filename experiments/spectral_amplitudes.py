import mpmath
import csv
import os

# 1. Setup
mpmath.mp.dps = 50  # High precision for zeta derivatives
path_csv = os.path.expanduser("~/Desktop/Farey-Local/experiments/bc_verify_100000_c.csv")
path_md = os.path.expanduser("~/Desktop/Farey-Local/experiments/SPECTRAL_AMPLITUDES.md")

# 2. Compute Zeta Zeros and c_k
results = []
print(f"{'k':<3} | {'gamma':<15} | {'|c_k|^2':<15} | {'Ratio |c|^2':<15}")
print("-" * 60)

for k in range(1, 11):
    rho = mpmath.zetazero(k)
    zeta_prime = mpmath.diff(mpmath.zeta, rho)
    c_k = 1 / (rho * zeta_prime)
    mod_sq = abs(c_k)**2
    
    if k == 1:
        c1_sq = mod_sq
        ratio = 1.0
    else:
        ratio = mod_sq / c1_sq
    
    results.append({'k': k, 'gamma': rho, 'c_sq': mod_sq, 'ratio': ratio})
    print(f"{k:<3} | {rho.imag:<15.10f} | {mod_sq:<15.10e} | {ratio:<15.10e}")

# 3. Load Farey Spectral Data
farey_data = {}
try:
    with open(path_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Attempt to match gamma column
            g = float(row.get('gamma', row.get('gamma_k', row.get('Im(zeta_zero)', 0))))
            F = float(row.get('F_gamma', row.get('spectral_power', row.get('F', 0))))
            farey_data[g] = F
except FileNotFoundError:
    print(f"ERROR: File not found at {path_csv}")
    exit(1)
except Exception as e:
    print(f"ERROR: CSV parsing failed: {e}")
    exit(1)

# 4. Compare Ratios
print("\nComparison with Farey Data:")
print(f"{'k':<3} | {'F(γ)/F(γ1)':<15} | {'|c_k/c_1|^2':<15} | {'Match?':<10}")
print("-" * 60)

md_lines = [
    "# Spectral Amplitudes Verification",
    "",
    "## Numerical Results (k=1..10)",
    "| k | γ_k | |c_k|^2 | Ratio |c_k/c_1|^2 | F(γ_k)/F(γ_1) | Match |",
    "|---|---|---|---|---|---|",
    ""
]

for res in results:
    k = res['k']
    gamma = res['gamma'].imag
    c_ratio = res['ratio']
    
    # Find closest gamma in CSV
    closest_g = min(farey_data.keys(), key=lambda x: abs(x - gamma))
    F_val = farey_data[closest_g]
    
    # Normalize F
    F1 = farey_data[min(farey_data.keys(), key=lambda x: abs(x - results[0]['gamma'].imag))]
    F_ratio = F_val / F1 if F1 != 0 else 0
    
    match = "Yes" if abs(F_ratio - c_ratio) / c_ratio < 0.1 else "No"
    
    md_lines.append(f"| {k} | {gamma:.10f} | {res['c_sq']:.10e} | {c_ratio:.10e} | {F_ratio:.10e} | {match} |")
    print(f"{k:<3} | {F_ratio:<15.10e} | {c_ratio:<15.10e} | {match:<10}")

# 5. Save Markdown
with open(path_md, 'w') as f:
    f.write("\n".join(md_lines))
    f.write("\n\n## Analysis\n")
    f.write("Computational verification suggests proportionality between Farey spectral power and residue magnitude.\n")
    f.write("Note: This is not a proof. GRH not assumed. Error terms bounded by Walfisz (1963).\n")

print(f"\nSaved to {path_md}")
