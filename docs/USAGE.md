# [ COMMANDS ]

After installation, run the tools from a terminal:

```bash
ph4ntxm-opsec-net
ph4ntxm-opsec-kernel
sudo ph4ntxm-opsec-proc
sudo ph4ntxm-opsec-radio
ph4-shred --help
ph4ntxm-opsec-connwatch
```

Process and Radio offer interactive remediation choices. Review the target before applying an action; Network's Lockdown action opens the PH4NTXM control dialog when installed.
Shredder's help lists queue and overwrite commands. Overwrite is best effort, and failures are reported rather than silently deleting the affected file.
ConnWatch requires its monitor service and permission to read the runtime statistics. Stop the dashboard with Ctrl+C.

## [ RUNTIME ]

The Python tools use the standard library plus host utilities. Checks and scores reflect the PH4NTXM environment, including intentional hardening and identity settings.
The suite does not install PH4NTXM's firewall, identity engine, RAM seeding, or shutdown kernel.
