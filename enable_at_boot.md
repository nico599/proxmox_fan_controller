# Enable desired fan speed at boot

Create a new service file, `/etc/systemd/system/set-fan-speed.service`:

```bash
[Unit]
Description=Set Fan Speed at Boot
After=network.target

[Service]
ExecStart=/usr/bin/ipmitool raw 0x30 0x70 0x66 0x01 0x00 0x10
Type=oneshot
RemainAfterExit=true

[Install]
WantedBy=multi-user.target

```

Reload Systemd and enable the service:

```bash
systemctl daemon-reload
systemctl enable set-fan-speed.service
systemctl start set-fan-speed.service
```
