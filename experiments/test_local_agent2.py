import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os

# Generate Farey sequence of order 5
farey = []
for b in range(1, 6):
    for a in range(0, b + 1):
        if math.gcd(a, b) == 1:
            farey.append((a, b))

# Sort the fractions
farey_sorted = sorted(farey, key=lambda x: x[0]/x[1])

# Print each fraction
for a, b in farey_sorted:
    print(f"{a}/{b}")

# Save to markdown file
markdown_path = os.path.expanduser('~/Desktop/Farey-Local/experiments/test_local_agent2.md')
os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
with open(markdown_path, 'w') as f:
    for a, b in farey_sorted:
        f.write(f'- {a}/{b}\n')
