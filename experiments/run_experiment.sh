#!/bin/bash
# Standard experiment runner — survives Claude Code timeouts
# Usage: ./run_experiment.sh <script.py> [output_name]

SCRIPT=$1
NAME=${2:-$(basename "$SCRIPT" .py)}
LOG="~/Desktop/Farey-Local/experiments/${NAME}_output.log"

echo "Starting: $SCRIPT"
echo "Log: $LOG"
echo "---"

cd ~/Desktop/Farey-Local/experiments
nohup python3 -u "$SCRIPT" > "${NAME}_output.log" 2>&1 &
PID=$!
echo "PID: $PID"
echo "Monitor: tail -f ${NAME}_output.log"
echo "Kill: kill $PID"
