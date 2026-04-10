This is a fascinating translation of number theory into distributed systems. The **Farey Injection Principle** is essentially a method of **successive refinement** that maintains a specific density property.

In the context of load balancing, your proposal shifts the objective from **Global Minimization** (Least-Loaded) to **Local Smoothness** (Mediant-based).

### 1. Theoretical Analysis: The "Mediant" vs. "Least-Loaded"

To apply Farey logic, we must define the "Mediant" for continuous values. If Server $i$ has load $L_i$ and Server $i+1$ has load $L_{i+1}$, the "Mediant" load is the arithmetic mean: $M = (L_i + L_{i+1})/2$.

**The fundamental tension:**
*   **Least-Loaded (B)** is a **Global Optimizer**. It ignores topology and seeks to minimize the absolute maximum. In a complete graph (where any job can go anywhere), (B) is mathematically unbeatable for minimizing $\max(L)$.
*   **Farey Approach (D)** is a **Topological Smoother**. It treats the servers as a 1D manifold (a ring or a line). It does not care about the global minimum; it cares about the **gradient** (the difference between neighbors).

**Does the Farey approach minimize max load imbalance?**
*   **In a Global Topology (Complete Graph):** **No.** The Farey approach will likely allow "pockets" of high load to form if they are surrounded by even higher loads, whereas Least-Loaded would have targeted them.
*   **In a Constrained Topology (Ring/Line/Mesh):** **Potentially Yes.** In systems where jobs can only be routed to adjacent nodes (to minimize latency/network hops), the Farey approach acts as a **Laplacian Smoother**. It minimizes the "energy" of the system by preventing sharp spikes in load between neighbors.

---

 least-loaded (B) is the gold standard for minimizing the peak, but the Farey approach (D) is a superior strategy for minimizing **system jitter** and **local congestion**.

### 2. Simulation Design

To test this, we need to simulate a stream of jobs with varying weights being assigned to a ring of $N$ servers.

#### The Metric Suite:
1.  **$\max(L)$**: The peak load (Target for Least-Loaded).
2.  **$\sigma(L)$**: Standard deviation of load (Target for Round-Robin/Random).
3.  **$\nabla L$ (Max Gradient)**: $\max|L_i - L_{i+1}|$ (Target for Farey).

#### Python Simulation Implementation

```python
import numpy as np
import random

class LoadBalancerSim:
    def __init__(self, n_servers, strategy='least_loaded'):
        self.n = n_servers
        self.loads = np.zeros(n_servers)
        self.strategy = strategy
        self.rr_index = 0

    def add_job(self, weight):
        if self.strategy == 'random':
            idx = random.randint(0, self.n - 1)
            self.loads[idx] += weight
            
        elif self.strategy == 'least_loaded':
            idx = np.argmin(self.loads)
            self.loads[idx] += weight
            
        elif self.strategy == 'round_robin':
            idx = self.rr_index % self.n
            self.loads[idx] += weight
            self.rr_index += 1
            
        elif self.strategy == 'farey_mediant':
            # Find adjacent pair with the lowest combined load (the 'gap')
            # We treat the servers as a ring
            min_gap_val = float('inf')
            target_pair = (0, 1)
            
            for i in range(self.n):
                next_i = (i + 1) % self.n
                gap_sum = self.loads[i] + self.loads[next_i]
                if gap_sum < min_gap_val:
                    min_gap_val = gap_sum
                    target_pair = (i, next_i)
            
            # Of the two servers in the gap, pick the one that 
            # brings its load closer to the 'mediant' (average of its neighbors)
            i, j = target_pair
            
            def get_mediant_error(idx):
                prev_idx = (idx - 1) % self.n
                next_idx = (idx + 1) % self.n
                mediant = (self.loads[prev_idx] + self.loads[next_idx]) / 2
                return abs((self.loads[idx] + weight) - mediant)

            # Decide whether to add weight to i or j
            if get_mediant_error(i) < get_mediant_error(j):
                self.loads[i] += weight
            else:
                self.loads[j] += weight

    def get_metrics(self):
        max_load = np.max(self.loads)
        std_dev = np.std(self.loads)
        # Max Gradient (Difference between neighbors)
        diffs = np.diff(np.append(self.loads, self.loads[0]))
        max_grad = np.max(np.abs(diffs))
        return max_load, std_dev, max_grad

def run_experiment(n_servers=20, n_jobs=500):
    strategies = ['random', 'least_loaded', 'round_robin', 'farey_mediant']
    results = {}

    for strat in strategies:
        sim = LoadBalancerSim(n_servers, strategy=strat)
        for _ in range(n_jobs):
            weight = random.uniform(0.5, 5.0)
            sim.add_job(weight)
        results[strat] = sim.get_metrics()
    
    print(f"{'Strategy':<15} | {'Max Load':<10} | {'StdDev':<10} | {'Max Grad':<10}")
    print("-" * 55)
    for strat, metrics in results.items():
        print(f"{strat:<15} | {metrics[0]:<10.2f} | {metrics[1]:<10.2f} | {metrics[2]:<10.2f}")

if __name__ == "__main__":
    run_experiment()
```

### 3. Expected Results & Interpretation

| Strategy | Max Load | StdDev | Max Gradient |
| :--- | :--- | :--- | :--- |
| **Random** | High | High | High |
| **Least-Loaded** | **Lowest** | Low | High |
| **Round-Robin** | Moderate | Low | Moderate |
| **Farey-Mediant** | Moderate | Moderate | **Lowest** |

#### Why this happens:
1.  **The Least-Loaded Paradox:** The `least_loaded` strategy will almost always win on **Max Load** and **StdDev**. However, it often creates "steep" gradients. It finds the single emptiest node and hammers it until it's no longer the minimum, creating a "sawtooth" pattern of loads across the ring.
2.  **The Farey Advantage:** The `farey_mediant` strategy ignores the global minimum. Its primary goal is to prevent $L_i$ and $L_{i+1}$ from diverging. Consequently, it will have the **Lowest Max Gradient**. 

### Conclusion for Engineering Application
The Farey Injection Principle is **not** a replacement for global load balancing, but it is a highly effective **local smoothing algorithm**. 

**Use the Farey approach if:**
*   You are working with **Edge Computing** or **P2P Networks** where nodes only know their immediate neighbors.
*   Your cost function is based on **latency variance** (jitter) rather than total throughput.
*   You want to prevent "hotspots" from propagating through a network topology.
