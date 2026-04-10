#!/bin/bash
# Launch Series 4 immediately after Series 3 completes, then Series 5
cd /Users/saar/Desktop/Farey-Local

echo "=== Waiting for Series 3 to complete ==="
while pgrep -f "3dgs_series3_budget" > /dev/null 2>&1; do
    sleep 30
done
echo "=== Series 3 complete. Starting Series 4 ==="

python3 experiments/3dgs_series4_scenes.py 2>&1 | tee experiments/3dgs_results/series4_log.txt

echo "=== Series 4 complete. Starting Series 5 ==="

python3 experiments/3dgs_series5_gap.py 2>&1 | tee experiments/3dgs_results/series5_log.txt

echo "=== ALL SERIES COMPLETE ==="
