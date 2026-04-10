import os
import math
import matplotlib.pyplot as plt

# Generate Farey fractions of order 5
fractions = []
for a in range(0, 6):
    for b in range(a, 6):
        if a == 0 and b == 0:
            continue
        if math.gcd(a, b) == 1:
            fractions.append((a, b))

# Sort the fractions by their value
sorted_fractions = sorted(fractions, key=lambda x: x[0]/x[1])

# Take first 10
first_10 = sorted_fractions[:10]

# Print to stdout
print("First 10 Farey fractions of order 5:")
for frac in first_10:
    print(f"{frac[0]}/{frac[1]}")

# Save to markdown file
output_dir = os.path.expanduser('~/Desktop/Farey-Local/experiments')
os.makedirs(output_dir, exist_ok=True)
markdown_path = os.path.join(output_dir, 'test_local_agent.md')
with open(markdown_path, 'w') as f:
    f.write("# First 10 Farey Fractions of Order 5\n\n")
    f.write("### List of fractions:\n\n")
    for frac in first_10:
        f.write(f"- {frac[0]}/{frac[1]}\n")

# Save figure
figures_dir = os.path.expanduser('~/Desktop/Farey-Local/figures')
os.makedirs(figures_dir, exist_ok=True)
fig_path = os.path.join(figures_dir, 'farey_fractions.png')
x = [f[0]/f[1] for f in first_10]
plt.plot(x, 'o', markersize=10)
plt.xlabel('Value')
plt.ylabel('Farey Fraction')
plt.title('First 10 Farey Fractions of Order 5')
plt.grid(True)
plt.savefig(fig_path)
plt.close()
