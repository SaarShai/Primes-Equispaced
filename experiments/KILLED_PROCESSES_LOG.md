# Killed Process Log

## Root Cause
Claude Code background tasks have a timeout (~10 min). Any script taking longer gets SIGTERM (exit 143) or SIGUSR2 (exit 144). This is NOT a memory or OS issue.

## Fix
Use `nohup python3 -u script.py > output.log 2>&1 &` for any process expected to run >10 min.

## Killed Processes (need restart or are completed via nohup)

### 3DGS Series 8-9 (ALL KILLED)
- **b1fvsibw7**: 8a (5 spheres) — 6 seeds done, no deltas
- **b5icsv9l4**: 8b+8c (15+25 sph) — 3 seeds done, no deltas
- **bjcfrdahm**: 8d+8e (50+100 sph) — 3 seeds done, no deltas
- **b2zr36nhc**: 8f+8g (clustered+multiscale) — 4 seeds done, no deltas
- **b77kc9u0y**: Series 9 stability — 4 seeds done, no deltas
- **bvnupblwd**: 8a restart — 1 seed done, no deltas
- **Status**: No completed deltas from any 3DGS experiment
- **Action needed**: Restart with nohup when ready for real 3DGS tests

### SB Learning Rate (KILLED 3x, now running via nohup)
- **banjt6bha**: First attempt — pin_memory bug, killed
- **bi8jlpq27**: Fixed attempt — killed at Run 3/12 after ~1400s
- **PID 47316**: nohup attempt — RUNNING, should complete overnight
- **Status**: 2 complete runs (A_step_decay seeds 42, 123). Full results expected in sb_lr_output.log
- **Action needed**: Check sb_lr_output.log in the morning

### Empty Cell Search (KILLED multiple times)
- **bqu8spjwe**: First attempt — killed (no output)
- **bag1skdp5**: Second attempt — killed (no output)
- **b191oem88**: Third attempt — killed
- **b8dajy33k**: Fast orbit search — killed
- **Agent ad183047c**: Still running? May have its own bash subprocesses killed
- **Status**: No results yet
- **Action needed**: Run with nohup after SB LR finishes

### AMR Demo (KILLED then rerun successfully)
- **bfwifqh5d**: Agent bash killed, but manual rerun succeeded
- **Status**: ✅ COMPLETE — results captured

### SB Hyperopt (KILLED then rerun successfully)
- **bjtmu28zd**: Agent bash killed, but manual rerun succeeded
- **Status**: ✅ COMPLETE — results captured

### Three-body N-body verification
- **btb9keq2i**: Search demo killed (timeout on 1000 samples)
- **Status**: Rerun with 200 samples succeeded
- **Action needed**: None — results captured

## Prevention
For ALL future long-running experiments:
```bash
cd ~/Desktop/Farey-Local/experiments
nohup python3 -u script.py > script_output.log 2>&1 &
echo "PID: $!"
```
