# [ OPSEC RADIO ]

## [ OVERVIEW ]

Checks Wi-Fi, Bluetooth, WWAN, monitor mode, NFC, and supported modem location state.

## [ USAGE ]

```bash
sudo ph4ntxm-opsec-radio
```

## [ RUNTIME ]

Uses host utilities such as nmcli, rfkill, iw, and mmcli. Supported findings offer interactive radio-disable or monitor-mode remediation.
Available checks depend on installed utilities, running services, and hardware. Disabling a radio can interrupt the current connection.

## [ SOURCE ]

[ph4ntxm-opsec-radio](../tools/ph4ntxm-opsec-radio) · [Installation](../INSTALLATION.md)
