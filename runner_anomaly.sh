#!/bin/bash

set -e

python ./auto_mover_clicker.py &
PID1=$!

python mouse_tracker.py --label anomaly &
PID2=$!

trap "kill $PID1 $PID2" SIGINT SIGTERM

wait $PID1 $PID2
