# React to Temperature Change

This is very necessary in my opinion because its a server which might heat up depending on demands. and as we're setting the fan speed manually it might either thermally throttle, or worse begin to fail/shutdown.

So we're logging temperatures, which should be reviewed, and we're dynamically adjusting the speeds based on sensor data.

Create the script `/usr/local/bin/fan-control.sh`:

(for contents see fan_control.sh)

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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

```

Create a timer file /etc/systemd/system/fan-control.timer:

```bash
[Unit]
Description=Run Fan Control Script Every 30 Seconds

[Timer]
OnBootSec=1min
OnUnitActiveSec=10s
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
