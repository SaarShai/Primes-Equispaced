#!/bin/bash
LOG=~/Desktop/Farey-Local/experiments/strong_tasks_log.txt
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a $LOG; }

log "=== RUNNING VERY STRONG TASKS ==="

# 3BP-4: Unequal mass extension (30 min)
log "--- 3BP-4: Three-body unequal mass ---"
cd ~/Desktop/Farey-Local/experiments
if [ -f threebody_exact_cf.py ]; then
    python3 -u threebody_exact_cf.py --unequal 2>&1 | tee -a $LOG || log "3BP-4: Script doesn't support --unequal, need dedicated script"
fi

# AMR-4: Extended shock benchmark (30 min)
log "--- AMR-4: Extended shock benchmark ---"
cd ~/Desktop/Farey-Local/experiments
if [ -f amr_shock_extended.py ]; then
    python3 -u amr_shock_extended.py 2>&1 | tee -a $LOG
    log "AMR-4 done (exit: $?)"
else
    log "AMR-4: Script not found"
fi

# MPR-1: B+C to p=100K (2-4 hrs)
log "--- MPR-1: B+C extension to p=100K ---"
cd "/Users/saar/Library/CloudStorage/GoogleDrive-saar.shai@gmail.com/My Drive/Farey Folder/experiments"
if [ -f bc_extend_fast2.c ]; then
    # Compile if needed
    if [ ! -f bc_extend_fast2 ] || [ bc_extend_fast2.c -nt bc_extend_fast2 ]; then
        cc -O2 -o bc_extend_fast2 bc_extend_fast2.c -lm
        log "Compiled bc_extend_fast2"
    fi
    ./bc_extend_fast2 2>&1 | tee -a $LOG
    log "MPR-1 done (exit: $?)"
else
    log "MPR-1: C source not found"
fi

log "=== ALL STRONG TASKS COMPLETE ==="
