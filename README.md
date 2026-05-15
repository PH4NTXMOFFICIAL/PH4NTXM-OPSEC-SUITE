# [ PH4NTXM OPSEC SUITE OFFICIAL REPOSITORY ]

The PH4NTXM OpSec Suite provides on-demand diagnostics across network, kernel, process, radio, and system layers.  
All modules operate read-only with no background telemetry.  
Operators can quickly assess system integrity, identify anomalies, and manage sensitive data securely.  
Every module runs entirely within the current session and leaves no persistent footprint.  

## [ PH4NTXM OPSEC SHREDDER ]

PH4NTXM OpSec Shredder performs military-grade file destruction using DoD 5220.22-M standards.  
It supports marking files and directories, recursive wiping, metadata sanitization, and customizable overwrite passes. 
Operators can execute shredding commands, adjust passes, and view forensic reliability.  
This ensures that sensitive files cannot be recovered even with advanced forensic tools.

## [ PH4NTXM OPSEC NETWORK ]

PH4NTXM OpSec Network inspects system network state including routes, gateways, DNS configuration, external resolver detection, IPv6 exposure, active connections, and suspicious traffic.  
It detects unexpected activity, public connections, and DNS leaks.  
Each run produces a network security score with detailed findings.

## [ PH4NTXM OPSEC KERNEL ]

PH4NTXM OpSec Kernel evaluates kernel security by reviewing loaded modules, hardening status, sysctl parameters, and lockdown mode.  
It detects untrusted modules and misconfigurations.  
Operators receive a kernel security score with detailed findings.

## [ PH4NTXM OPSEC PROCESS ]

PH4NTXM OpSec Process inspects system processes for anomalies such as deleted or ephemeral executables and processes running from untrusted paths.  
It provides a list of suspicious processes and scores system integrity.

## [ PH4NTXM OPSEC RADIO ]

PH4NTXM OpSec Radio audits wireless interfaces, monitoring Bluetooth, Wi-Fi, modem activity, monitor mode, and nearby networks.  
It detects RF leaks or insecure wireless configurations.  
The module outputs a radio security score.

## [ PH4NTXM OPSEC CONNWATCH ]

PH4NTXM OpSec ConnWatch monitors inbound TCP connection attempts in real time.  
It tracks SYN packets, source IPs, repeated or unusual patterns, and logs activity.  
Operators can identify scanning behavior, automated traffic, or suspicious connections.  
Each run provides a connection exposure score.

## [ REMEDIATION ]

Some modules include optional remediation actions for reducing exposure and restoring safer operating states.  
Elevated privileges may be required depending on system configuration and security policy.

## [ SUMMARY ]

The PH4NTXM OpSec Suite enables session-scoped diagnostics, secure file shredding, anomaly detection in real time, ephemeral read-only operation, and fast assessment of system integrity across all critical layers.