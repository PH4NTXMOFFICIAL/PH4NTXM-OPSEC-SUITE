import subprocess

SEVERITY = {
    "bluetooth_on": 10,
    "wifi_on": 10,
    "modem_active": 10,
    "monitor_mode_active": 20,
    "nearby_devices_detected": 20,
    "nfc_enabled": 10,
    "gps_location_active": 30,
}

def result(ok, data=None, error=None, findings=None):
    return {"ok": ok, "data": data or {}, "error": error, "findings": findings or []}

def run(command, timeout=5):
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        if proc.returncode != 0:
            return result(False, error=proc.stderr.strip())
        return result(True, data={"stdout": proc.stdout.strip()})
    except Exception as exc:
        return result(False, error=str(exc))

def check_bluetooth():
    res = run(["rfkill", "list"])

    if not res["ok"]:
        return result(False, error=res["error"])

    out = res["data"]["stdout"].lower()

    if "bluetooth" not in out:
        findings = ["bluetooth_unavailable"]
    elif "soft blocked: yes" in out or "hard blocked: yes" in out:
        findings = ["bluetooth_off"]
    else:
        findings = ["bluetooth_on"]

    return result(True, findings=findings)

def check_wifi():
    res = run(["nmcli", "radio", "wifi"])
    if not res["ok"]: return result(False, error=res["error"])
    findings = ["wifi_on"] if "enabled" in res["data"]["stdout"] else ["wifi_off"]
    return result(True, findings=findings)

def check_modem_state():
    res = run(["mmcli", "-L"])
    if not res["ok"]: return result(False, error=res["error"])
    findings = ["modem_inactive"] if "No modems were found" in res["data"]["stdout"] else ["modem_active"]
    return result(True, findings=findings)

def check_monitor_mode():
    res = run(["iw", "dev"])
    if not res["ok"]: return result(False, error=res["error"])
    findings = ["monitor_mode_active"] if "type monitor" in res["data"]["stdout"] else ["monitor_mode_inactive"]
    return result(True, findings=findings)

def check_nearby_scan():
    res = run(["nmcli", "dev", "wifi", "list"])
    if not res["ok"]: return result(False, error=res["error"])
    findings = ["nearby_devices_detected"] if "SSID" in res["data"]["stdout"] else ["no_nearby_devices"]
    return result(True, findings=findings)

def check_nfc():
    res = run(["nmcli", "device", "show"])
    if not res["ok"]: return result(False, error=res["error"])
    findings = ["nfc_enabled"] if "nfc" in res["data"]["stdout"].lower() else ["nfc_disabled"]
    return result(True, findings=findings)

def check_gps_activity():
    res = run(["mmcli", "-L"])

    if not res["ok"]:
        return result(True, findings=["gps_location_unavailable"])

    out = res["data"]["stdout"].lower()

    if "no modems were found" in out:
        return result(True, findings=["gps_location_unavailable"])

    res2 = run(["mmcli", "-m", "0", "--location-status"])

    if not res2["ok"]:
        return result(True, findings=["gps_location_inactive"])

    out2 = res2["data"]["stdout"].lower()

    findings = (
        ["gps_location_active"]
        if "enabled: yes" in out2 or "gps" in out2
        else ["gps_location_inactive"]
    )

    return result(True, findings=findings)

def assess_radio(results):
    score = 100
    findings = []

    for r in results:
        if not r["ok"]:
            findings.append(f"error: {r.get('error','check_failed')}")
            score -= 20
        else:
            for f in r.get("findings", []):
                findings.append(f)
                score -= SEVERITY.get(f, 0)

    score = max(0, min(score, 100))

    return result(
        True,
        data={
            "score": score,
            "findings": findings,
        },
        findings=findings
    )

def format_finding(f):
    mapping = {
        "bluetooth_on": ("Bluetooth enabled", "warn"),
        "bluetooth_off": ("Bluetooth disabled/blocked", "good"),
        "bluetooth_unavailable": ("Bluetooth hardware unavailable", "good"),

        "wifi_on": ("WiFi enabled", "warn"),
        "wifi_off": ("WiFi disabled", "good"),

        "modem_active": ("Modem active", "warn"),
        "modem_inactive": ("Modem inactive", "good"),

        "monitor_mode_active": ("Monitor Mode enabled", "bad"),
        "monitor_mode_inactive": ("Monitor Mode inactive", "good"),

        "nearby_devices_detected": ("Nearby devices detected", "bad"),
        "no_nearby_devices": ("No nearby devices detected", "good"),

        "nfc_enabled": ("NFC enabled", "warn"),
        "nfc_disabled": ("NFC disabled", "good"),

        "gps_location_active": ("GPS location active", "bad"),
        "gps_location_inactive": ("GPS location inactive", "good"),
        "gps_location_unavailable": ("GPS hardware unavailable", "good"),
    }

    return mapping.get(f, (f.replace("_"," "), "warn"))

checks = [
    check_bluetooth,
    check_wifi,
    check_modem_state,
    check_monitor_mode,
    check_nearby_scan,
    check_nfc,
    check_gps_activity
]

def main():
    results = [check() for check in checks]
    assessment = assess_radio(results)
    return results, assessment

if __name__ == "__main__":
    main()