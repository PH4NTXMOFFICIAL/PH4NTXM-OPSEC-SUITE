# [ INSTALLATION ]

PH4-shred is a secure deletion utility designed for Debian-based systems. It provides configurable file and disk wiping aligned with PH4NTXM operational assumptions.

## [ REQUIREMENTS ]

Debian-based systems:

sudo apt install python3 python3-pip python3-setuptools python3-wheel

## [ INSTALLATION ]

From inside the module directory:

sudo python3 -m pip install . --break-system-packages --no-user --use-pep517

## [ USAGE ]

Run the module with:

python3 -m ph4-shred --help

## [ CUSTOMIZATION NOTES ]

Users may wish to adjust overwrite passes, modify deletion behavior, adapt wiping logic for specific operational requirements, or integrate the utility into existing workflows or automation environments.  
The module is intentionally lightweight and can be modified or extended where necessary.

## [ NOTES ]

Some checks may require elevated privileges depending on configuration and system policies.