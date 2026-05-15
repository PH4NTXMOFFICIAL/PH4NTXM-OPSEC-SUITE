# [ INSTALLATION ]

PH4NTXM-OpSec is a process-focused operational security module designed for Debian-based systems. It provides runtime checks and optional remediation aligned with PH4NTXM operational assumptions.

## [ REQUIREMENTS ]

Debian-based systems:

sudo apt install python3 python3-pip python3-setuptools python3-wheel

## [ INSTALLATION ]

From inside the module directory:

sudo python3 -m pip install . --break-system-packages --no-user --use-pep517

## [ USAGE ]

Run the module with:

python3 -m ph4ntxm_opsec_proc

## [ CUSTOMIZATION NOTES ]

This module was originally developed for the PH4NTXM operational environment and reflects assumptions, thresholds, and runtime expectations specific to that ecosystem.  
Users deploying the module on external systems may wish to modify scoring logic, adjust thresholds, tune operational assumptions, add or remove checks, or adapt findings to their own environment and workflow requirements.

## [ REMEDIATION SUPPORT ]

The module includes optional remediation actions for responding to suspicious or potentially unsafe process activity.  
Available remediation actions may include terminating suspicious processes, terminating process trees and child processes, or freezing processes using SIGSTOP.  
Some remediation actions may require elevated privileges depending on system configuration and security policy.

## [ NOTES ]

Some checks may require elevated privileges depending on configuration and system policies.
