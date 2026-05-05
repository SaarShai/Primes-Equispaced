# B2 Better Falsifier — log K scaling with mollifier ON
# theory: E[|S|²]/(log K)² should be ≈ constant ≈ c_∞ ≈ 2.31
# K | N | samples | E[|S|²] | E[|S|²]/(log K)² | dt
K=100 N=230 samples=200 E[|S|²]=12.408±0.356 norm=0.5851 dt=13s
K=300 N=285 samples=200 E[|S|²]=38.597±0.806 norm=1.1864 dt=21s
K=1000 N=345 samples=200 E[|S|²]=45.122±1.017 norm=0.9456 dt=34s
K=3000 N=400 samples=200 E[|S|²]=56.746±1.128 norm=0.8853 dt=45s
K=10000 N=460 samples=100 E[|S|²]=14.974±0.934 norm=0.1765 dt=32s

# Predicted: norm should be K-independent at large K, value ≈ 2.31 (if α_ratio=1)
