# [ OPSEC SHREDDER ]

## [ OVERVIEW ]

Queues files and directories for best-effort overwrite and deletion.

## [ USAGE ]

```bash
ph4-shred --help
```

## [ RUNTIME ]

Supports marking and unmarking paths, queue inspection, and one to seven overwrite passes. The default is three passes, and execution requires confirmation.
Files are retained when overwrite fails. Logical overwrite cannot guarantee removal from SSD remapped blocks, snapshots, copy-on-write storage, or backups.

## [ SOURCE ]

[ph4ntxm-opsec-shredder](../tools/ph4ntxm-opsec-shredder) · [Installation](../INSTALLATION.md)
