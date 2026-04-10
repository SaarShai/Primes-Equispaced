#!/bin/bash
# Process monitor - checks tracked PIDs every 60 seconds
# Logs deaths immediately and attempts restart
# Usage: nohup bash process_monitor.sh &

MONITOR_FILE=~/Desktop/Farey-Local/experiments/TRACKED_PROCESSES.txt
LOG=~/Desktop/Farey-Local/experiments/monitor_log.txt

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG; echo "$1"; }

log "=== PROCESS MONITOR STARTED ==="

while true; do
    if [ -f "$MONITOR_FILE" ]; then
        while IFS='|' read -r PID NAME RESTART_CMD; do
            PID=$(echo "$PID" | xargs)
            NAME=$(echo "$NAME" | xargs)
            RESTART_CMD=$(echo "$RESTART_CMD" | xargs)
            [ -z "$PID" ] && continue
            [[ "$PID" == \#* ]] && continue
            
            if ! kill -0 "$PID" 2>/dev/null; then
                log "☠️ DEAD: $NAME (PID $PID)"
                log "   Attempting restart: $RESTART_CMD"
                if [ -n "$RESTART_CMD" ]; then
                    eval "$RESTART_CMD" &
                    NEW_PID=$!
                    log "   ✅ Restarted as PID $NEW_PID"
                    # Update the tracked file with new PID
                    # Use space-tolerant pattern since file uses " | " as delimiter
                    sed -i '' "s/^$PID /$NEW_PID /" "$MONITOR_FILE"
                else
                    log "   ⚠️ No restart command provided"
                fi
            fi
        done < "$MONITOR_FILE"
    fi
    sleep 60
done
