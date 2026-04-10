#!/bin/bash
# macOS timeout replacement
DURATION=$1; shift
"$@" &
PID=$!
(sleep $DURATION && kill $PID 2>/dev/null) &
TIMER=$!
wait $PID 2>/dev/null
STATUS=$?
kill $TIMER 2>/dev/null 2>&1
exit $STATUS
