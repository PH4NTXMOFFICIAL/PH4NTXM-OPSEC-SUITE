# [ CONNWATCH ]

Run installation commands from the repository root. The monitor requires Bash, systemd, `tcpdump`, `iproute2`, and standard Debian core utilities. Desktop notifications additionally use `libnotify-bin` and an existing `ph4ntxm` user's session bus.

```bash
sudo apt install tcpdump iproute2 libnotify-bin
sudo groupadd --system --force ph4ntxm
sudo usermod -aG ph4ntxm "$USER"
sudo install -D -m 0755 tools/ph4ntxm-opsec-connwatch/ph4ntxm-opsec-connwatch /usr/local/bin/ph4ntxm-opsec-connwatch
sudo install -D -m 0755 tools/ph4ntxm-opsec-connwatch/ph4ntxm-opsec-connwatch.sh /usr/local/sbin/ph4ntxm-opsec-connwatch.sh
sudo install -D -m 0644 tools/ph4ntxm-opsec-connwatch/ph4ntxm-opsec-connwatch.service /etc/systemd/system/ph4ntxm-opsec-connwatch.service
sudo systemctl daemon-reload
sudo systemctl start ph4ntxm-opsec-connwatch.service
```

Log out and back in for the group membership to apply. Without a `ph4ntxm` user, packet monitoring still works but desktop notifications are skipped.

## [ OPERATION ]

Run `ph4ntxm-opsec-connwatch` to view statistics. Check the monitor with `systemctl status ph4ntxm-opsec-connwatch.service`.
Statistics and bounded alert history live under `/run/ph4ntxm-opsec-connwatch`. Observed SYN packets are not proof of accepted connections or malicious activity; the dashboard score is an activity heuristic.
The service starts as root with bounded capabilities. Its PH4NTXM firewall ordering entries do not install or configure a firewall on other systems.

## [ SERVICE LIFECYCLE ]

For desktop boot startup, use `sudo systemctl enable ph4ntxm-opsec-connwatch.service`. To stop and disable it, use `sudo systemctl disable --now ph4ntxm-opsec-connwatch.service`.
Runtime files are temporary, but the system journal can persist according to the host configuration.

## [ SOURCE ]

[ph4ntxm-opsec-connwatch](../tools/ph4ntxm-opsec-connwatch)
