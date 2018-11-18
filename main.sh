#!/bin/bash

#trap 'jobs -p | xargs kill' EXIT
trap 'kill $(ps aux | grep '"'"'[p]ython3 pi-monitor'"'"' | awk '"'"'{print $2}'"'"')' EXIT

if [ -f data.db ];
then
    rm data.db
fi
python3 pi-monitor-cpu-temperature.py &
python3 pi-monitor-flask.py &
python3 pi-monitor-mem.py &
wait
