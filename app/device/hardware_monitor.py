from app.device.device_identity import (
    get_device_fingerprint,
    load_device_config
)


def check_hardware_changes():

    config = load_device_config()

    current = get_device_fingerprint()

    changes = []

    if config.get("hostname") != current["hostname"]:

        changes.append({
            "field": "hostname",
            "old": config.get("hostname"),
            "new": current["hostname"]
        })

    if config.get("mac_address") != current["mac_address"]:

        changes.append({
            "field": "mac_address",
            "old": config.get("mac_address"),
            "new": current["mac_address"]
        })

    if config.get("camera_serial") != current["camera_serial"]:

        changes.append({
            "field": "camera_serial",
            "old": config.get("camera_serial"),
            "new": current["camera_serial"]
        })

    return changes