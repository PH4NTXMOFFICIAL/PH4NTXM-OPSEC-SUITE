# [ OPSEC KERNEL ]

## [ OVERVIEW ]

Inspects loaded modules, selected sysctl values, and kernel hardening state.

## [ USAGE ]

```bash
ph4ntxm-opsec-kernel
```

## [ RUNTIME ]

Reports module findings, lockdown and signature enforcement state, and a kernel assessment. PH4NTXM boot mode is consulted when available.
This tool reports state without changing kernel settings. Missing or restricted kernel interfaces are reported; the score reflects PH4NTXM assumptions.

## [ SOURCE ]

[ph4ntxm-opsec-kernel](../tools/ph4ntxm-opsec-kernel) · [Installation](../INSTALLATION.md)
