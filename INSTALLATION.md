# [ INSTALLATION ]

Run the following from the repository root on Debian 13. Installation does not change sudo policy or enable monitoring automatically.

## [ DEPENDENCIES ]

```bash
sudo apt install python3 python3-venv python3-setuptools python3-wheel iproute2 procps kmod
```

Radio additionally uses `rfkill`, `iw`, `network-manager`, and `modemmanager`. Missing tools or services are reported by the checks; install these components only where appropriate for the host.

## [ PYTHON MODULES ]

Use a dedicated environment, keeping Debian's system Python packages intact:

```bash
sudo python3 -m venv --system-site-packages /opt/ph4ntxm-opsec-suite
sudo /opt/ph4ntxm-opsec-suite/bin/python -m pip install --no-index --no-deps --no-build-isolation ./tools/ph4ntxm-opsec-{net,kernel,proc,radio,shredder}
sudo install -d /usr/local/bin
for tool in ph4ntxm-opsec-net ph4ntxm-opsec-kernel ph4ntxm-opsec-proc ph4ntxm-opsec-radio ph4-shred; do
    sudo ln -sfn "/opt/ph4ntxm-opsec-suite/bin/$tool" "/usr/local/bin/$tool"
done
```

## [ INTEGRATION ]

Network diagnostics run independently, but the optional Lockdown action requires `/usr/local/bin/ph4ntxm-lockdown` and its PH4NTXM privileged backend. These OS-wide controls are not installed by this repository.
Kernel and Network consult `/run/ph4ntxm/mode` when available. Other hosts retain the source defaults and may produce different findings.

Install the [ConnWatch monitor](docs/CONNWATCH.md) and [desktop launchers](docs/DESKTOP.md) separately when needed.
