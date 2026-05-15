import subprocess

def result(ok, message=None, error=None):
    return {
        "ok": ok,
        "message": message,
        "error": error
    }

def run(command, timeout=10):
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        if proc.returncode != 0:
            return result(
                False,
                error=proc.stderr.strip() or proc.stdout.strip()
            )

        return result(
            True,
            message=proc.stdout.strip()
        )

    except Exception as exc:
        return result(False, error=str(exc))

def disable_bluetooth():
    return run([
        "rfkill",
        "block",
        "bluetooth"
    ])

def disable_wifi():
    return run([
        "nmcli",
        "radio",
        "wifi",
        "off"
    ])

def disable_modem():
    return run([
        "nmcli",
        "radio",
        "wwan",
        "off"
    ])

def disable_monitor_mode():
    try:
        iw = subprocess.run(
            ["iw", "dev"],
            capture_output=True,
            text=True,
            check=False
        )

        interfaces = []
        current_iface = None

        for line in iw.stdout.splitlines():
            line = line.strip()

            if line.startswith("Interface"):
                current_iface = line.split()[1]

            if "type monitor" in line and current_iface:
                interfaces.append(current_iface)

        if not interfaces:
            return result(
                True,
                message="No monitor mode interfaces found"
            )

        for iface in interfaces:
            subprocess.run(
                ["ip", "link", "set", iface, "down"],
                check=False
            )

            subprocess.run(
                ["iw", iface, "set", "type", "managed"],
                check=False
            )

            subprocess.run(
                ["ip", "link", "set", iface, "up"],
                check=False
            )

        return result(
            True,
            message="Monitor mode disabled"
        )

    except Exception as exc:
        return result(False, error=str(exc))

def disable_nfc():
    return run([
        "rfkill",
        "block",
        "nfc"
    ])

def disable_gps():
    try:
        modem_check = subprocess.run(
            ["mmcli", "-L"],
            capture_output=True,
            text=True,
            check=False
        )

        if "No modems were found" in modem_check.stdout:
            return result(
                True,
                message="No modem available"
            )

        return run([
            "mmcli",
            "-m",
            "0",
            "--location-disable-gps"
        ])

    except Exception as exc:
        return result(False, error=str(exc))

REMEDIATIONS = {
    "bluetooth_on": {
        "label": "Disable Bluetooth RF",
        "description": "Reduce Bluetooth discoverability",
        "severity": "warn",
        "action": disable_bluetooth,
    },

    "wifi_on": {
        "label": "Disable WiFi RF",
        "description": "Reduce wireless network exposure",
        "severity": "warn",
        "action": disable_wifi,
    },

    "modem_active": {
        "label": "Disable WWAN/Modem",
        "description": "Reduce cellular network exposure",
        "severity": "warn",
        "action": disable_modem,
    },

    "monitor_mode_active": {
        "label": "Disable Monitor Mode",
        "description": "Return wireless interface to managed mode",
        "severity": "bad",
        "action": disable_monitor_mode,
    },

    "nfc_enabled": {
        "label": "Disable NFC",
        "description": "Reduce near-field communication exposure",
        "severity": "warn",
        "action": disable_nfc,
    },

    "gps_location_active": {
        "label": "Disable GPS Location Services",
        "description": "Prevent modem-assisted geolocation",
        "severity": "bad",
        "action": disable_gps,
    },
}