#!/bin/bash
TASK_FILE="$HOME/Desktop/Farey-Local/experiments/m1max_tasks.txt"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/M1MAX_CONTINUOUS_LOG.md"
END_TIME=$(($(date +%s) + 8 * 3600))

echo "=== M1 Max Continuous $(date) — 8h ===" > "$LOG"

CYCLE=0
while [ $(date +%s) -lt $END_TIME ]; do
    CYCLE=$((CYCLE + 1))
    echo "=== Cycle $CYCLE $(date) ===" >> "$LOG"
    
    while IFS='|' read -r MODEL NAME PROMPT; do
        [ -z "$MODEL" ] && continue
        [ $(date +%s) -ge $END_TIME ] && break
        
        echo "$(date) Starting: $NAME" >> "$LOG"
        ~/bin/remote_ollama.sh "$MODEL" "$NAME" "$PROMPT"
        echo "$(date) Done: $NAME ($(wc -c < "$OUT/${NAME}.md") bytes)" >> "$LOG"
    done < "$TASK_FILE"
done

echo "=== M1 Max stopped $(date) ===" >> "$LOG"
