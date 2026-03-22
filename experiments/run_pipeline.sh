#!/bin/bash
# Pipeline: 100K → 200K, each as separate nohup process
# Using nohup so they survive session disconnects

echo "=== Phase 1: N=100K ===" >> pipeline.log
./wobble_primes_only 100000 >> pipeline.log 2>&1
echo "Phase 1 complete at $(date)" >> pipeline.log

echo "=== Phase 2: N=200K ===" >> pipeline.log  
./wobble_primes_only 200000 >> pipeline.log 2>&1
echo "Phase 2 complete at $(date)" >> pipeline.log
