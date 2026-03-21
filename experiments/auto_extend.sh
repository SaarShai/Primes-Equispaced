#!/bin/bash
# Auto-extend: run N=100K, then 200K, then 500K
echo "=== Starting auto-extend pipeline ==="
echo "Phase 1: N=100K"
./wobble_primes_only 100000
echo "Phase 1 complete. Starting Phase 2: N=200K"
./wobble_primes_only 200000
echo "Phase 2 complete. Starting Phase 3: N=500K"  
./wobble_primes_only 500000
echo "=== All phases complete ==="
