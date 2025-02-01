# React to Temperature Change

This is very necessary in my opinion because its a server which might heat up depending on demands. and as we're setting the fan speed manually it might either thermally throttle, or worse begin to fail/shutdown.

So we're logging temperatures, which should be reviewed, and we're dynamically adjusting the speeds based on sensor data.

Create the script `/usr/local/bin/fan-control.sh`:

```bash
#!/bin/bash

# Define temperature thresholds (you may need to adjust these values)
TEMP_THRESHOLD_1=40  # Temperature (in C) for low fan speed
TEMP_THRESHOLD_2=60  # Temperature (in C) for moderate fan speed
TEMP_THRESHOLD_3=80  # Temperature (in C) for high fan speed

# Get the current CPU temperature using ipmitool
CPU_TEMP=$(ipmitool sensor | grep "CPU" | grep -oP '(\d+.\d+)' | head -n 1)

# If no CPU temperature is available, exit
if [ -z "$CPU_TEMP" ]; then
    echo "Error: Could not read CPU temperature."
    exit 1
fi

# Determine fan speed based on temperature
if (( $(echo "$CPU_TEMP < $TEMP_THRESHOLD_1" | bc -l) )); then
    FAN_SPEED="0x08"  # Low fan speed
elif (( $(echo "$CPU_TEMP >= $TEMP_THRESHOLD_1 && $CPU_TEMP < $TEMP_THRESHOLD_2" | bc -l) )); then
    FAN_SPEED="0x10"  # Medium fan speed
elif (( $(echo "$CPU_TEMP >= $TEMP_THRESHOLD_2" | bc -l) )); then
    FAN_SPEED="0x20"  # High fan speed
fi

# Set the fan speed via ipmitool
ipmitool raw 0x30 0x70 0x66 0x01 0x00 $FAN_SPEED

# Optionally log the temperature and fan speed to a file
echo "$(date) - CPU Temp: $CPU_TEMP, Fan Speed: $FAN_SPEED" >> /var/log/fan-control.log
```

After creating the script, make it executable:

```bash
chmod +x /usr/local/bin/fan-control.sh
```

Create a service file /etc/systemd/system/fan-control.service:

```bash
[Unit]
Description=Fan Speed Control Based on CPU Temperature
After=multi-user.target

[Service]
ExecStart=/usr/local/bin/fan-control.sh
Type=simple
Restart=on-failure

[Install]
WantedBy=multi-user.target

```

Create a timer file /etc/systemd/system/fan-control.timer:

```bash
[Unit]
Description=Run Fan Control Script Every 30 Seconds

[Timer]
OnBootSec=5min
OnUnitActiveSec=30s
Unit=fan-control.service

[Install]
WantedBy=timers.target

```

Enable and start the service and timer:

```bash
systemctl daemon-reload
systemctl enable fan-control.service
systemctl enable fan-control.timer
systemctl start fan-control.timer
```

Periodically review the log:

`tail -f /var/log/fan-control.log`
