# [ PH4NTXM OPSEC SUITE ]

The current OpSec tools from [PH4NTXM](https://github.com/PH4NTXMOFFICIAL/PH4NTXM), grouped in one source repository for Debian 13.

## [ MODULES ]

| Tool | Purpose |
| --- | --- |
| [Network](docs/NETWORK.md) | Routes, DNS, sockets, namespace state, and PH4NTXM Lockdown integration. |
| [Kernel](docs/KERNEL.md) | Module inspection, selected sysctl settings, and kernel hardening checks. |
| [Process](docs/PROCESS.md) | Process inspection and identity-checked freeze or termination actions. |
| [Radio](docs/RADIO.md) | Wireless state checks and supported radio disable actions. |
| [Shredder](docs/SHREDDER.md) | Queued, best-effort file overwrite and deletion. |
| [ConnWatch](docs/CONNWATCH.md) | Inbound SYN observations, bounded runtime statistics, and a terminal dashboard. |

## [ INSTALLATION AND USE ]

[Installation](INSTALLATION.md) · [Commands](docs/USAGE.md) · [ConnWatch](docs/CONNWATCH.md) · [Desktop integration](docs/DESKTOP.md)

## [ SCOPE ]

Reports use PH4NTXM assumptions; scores are not proof that a host is secure. Remediation actions change system state and may require elevated privileges.
Network Lockdown requires the PH4NTXM control stack. ConnWatch retains its PH4NTXM group and optional notification-user integration.
On an installed OS, files, shell history, and service logs can persist. Shredder cannot guarantee erasure of snapshots, remapped flash blocks, or backups.

## [ LICENSE ]

[GNU GPL v3.0](LICENSE) · [Trademarks](TRADEMARKS.md)
