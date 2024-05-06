#!/bin/bash

if [ -z "$1" ]; then
    echo "Please provide a number as an argument."
    exit 1
fi

MicroXRCEAgent udp4 -p 8888 -v 0 >/dev/null 2>&1 &

num_times=$1
drone_model=${2:-gz_x500}

PX4_SYS_AUTOSTART=4001 PX4_SIM_MODEL="$drone_model" /PX4-Autopilot/build/px4_sitl_default/bin/px4 -i 1 >/dev/null 2>&1 &
sleep 5
for ((i=0; i<=num_times-2; i++)); do

    PX4_SYS_AUTOSTART=$((4001)) PX4_GZ_MODEL_POSE="0,$((1+i))" PX4_SIM_MODEL="$drone_model" /PX4-Autopilot/build/px4_sitl_default/bin/px4 -i $((2+i)) >/dev/null 2>&1 &

done
wait
