# [ INSTALLATION ]

PH4NTXM-OpSec-ConnWatch is a lightweight inbound connection monitoring utility for Linux environments. It is designed to operate fully within a live session while keeping minimal footprint and consistent runtime behavior.

## [ OVERVIEW ]

The module consists of a user-facing launcher, a privileged monitoring backend, and an optional systemd service for persistent runtime monitoring.

## [ REQUIREMENTS ]

Required packages:

tcpdump
python3
python3-gi
gir1.2-gtk-3.0

## [ INSTALL BINARY ]

Copy the main launcher into /usr/local/bin and set execution:

sudo cp ph4ntxm-opsec-connwatch /usr/local/bin/
sudo chmod +x /usr/local/bin/ph4ntxm-opsec-connwatch

## [ INSTALL MONITORING BACKEND ]

Copy the monitoring backend into /usr/local/sbin and set execution:

sudo cp ph4ntxm-opsec-connwatch.sh /usr/local/sbin/
sudo chmod +x /usr/local/sbin/ph4ntxm-opsec-connwatch.sh

## [ INSTALL SERVICE ]

Copy the service file into /etc/systemd/system:

sudo cp ph4ntxm-opsec-connwatch.service /etc/systemd/system/

Reload systemd:

sudo systemctl daemon-reload

Enable the service:

sudo systemctl enable ph4ntxm-opsec-connwatch

Start the service:

sudo systemctl start ph4ntxm-opsec-connwatch

## [ VERIFY SERVICE STATUS ]

Check the service status:

sudo systemctl status ph4ntxm-opsec-connwatch

## [ NOTES ]

The monitoring backend requires elevated privileges for packet inspection using tcpdump.
