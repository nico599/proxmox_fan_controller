#!/bin/bash

# Define temperature thresholds and corresponding fan speeds
TEMP_THRESHOLDS=(27 28 29 30 31 32 33 34 35 36 40 60 80)
FAN_SPEEDS=("0x08" "0x09" "0x0A" "0x0B" "0x0C" "0x0D" "0x0E" "0x0F" "0x10" "0x11" "0x12" "0x18" "0x20")

# File to store the last fan speed setting
LAST_FAN_SPEED_FILE="/tmp/last_fan_speed"

log () {
    logfile="/var/log/fan-control.log"
    # This function will log any line sent to your defined logfile
    # For example:
    # > log "example"
    # would create the following log entry
    # > 2025-02-02_00-27-18: example 
    echo "$(date +"%Y-%m-%d_%H-%M-%S"): $1" | tee -a "$logfile"
}

# Get the current CPU temperature using ipmitool
CPU_TEMP=$(ipmitool sensor | grep "CPU" | grep -oP '(\d+.\d+)' | head -n 1)

# If no CPU temperature is available, exit
if [ -z "$CPU_TEMP" ]; then
    log "Error: Could not read CPU temperature."
    exit 1
fi

# Determine fan speed based on temperature
FAN_SPEED="0x08"  # Default to the lowest fan speed
for i in "${!TEMP_THRESHOLDS[@]}"; do
    if (( $(echo "$CPU_TEMP < ${TEMP_THRESHOLDS[$i]}" | bc -l) )); then
        FAN_SPEED=${FAN_SPEEDS[$i]}
        break
    fi
done

# Read the last fan speed setting from the file
if [ -f "$LAST_FAN_SPEED_FILE" ]; then
    LAST_FAN_SPEED=$(cat "$LAST_FAN_SPEED_FILE")
else
    LAST_FAN_SPEED=""
fi

# Set the fan speed only if it has changed or if it's the first run
if [ "$FAN_SPEED" != "$LAST_FAN_SPEED" ]; then
    ipmitool raw 0x30 0x70 0x66 0x01 0x00 $FAN_SPEED
    echo "$FAN_SPEED" > "$LAST_FAN_SPEED_FILE"
    log "CPU Temp: $CPU_TEMP, Fan Speed: $FAN_SPEED"
fi