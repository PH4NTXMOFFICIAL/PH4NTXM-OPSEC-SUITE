# [ DESKTOP INTEGRATION ]

The supplied launchers are the current PH4NTXM Xfce launchers. Install the Python modules and ConnWatch first. Run these commands from the repository root:

```bash
sudo apt install xfce4-terminal
sudo install -d /usr/local/share/applications /usr/local/share/icons/hicolor/scalable/apps /usr/local/share/desktop-directories
sudo install -m 0644 desktop/applications/*.desktop /usr/local/share/applications/
sudo install -m 0644 desktop/icons/*.svg /usr/local/share/icons/hicolor/scalable/apps/
sudo install -m 0644 desktop/ph4ntxm-opsec-suite.directory /usr/local/share/desktop-directories/
```

## [ MENU ]

Launchers use the System and Security categories. To add the dedicated suite submenu for the current Xfce user:

```bash
mkdir -p ~/.config/menus/xfce-applications-merged
install -m 0644 desktop/ph4ntxm-opsec-suite.menu ~/.config/menus/xfce-applications-merged/
```

Process and Radio launch through `sudo`; the host's existing authentication policy applies. Shredder opens its help rather than starting a deletion.
