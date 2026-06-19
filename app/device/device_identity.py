import socket
import subprocess
import uuid
import pyrealsense2 as rs
import json
from pathlib import Path


def get_hostname():

    return socket.gethostname()


def get_machine_uuid():

    return subprocess.check_output(
        [
            "powershell",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
        ]
    ).decode().strip()


def get_mac_address():

    return ':'.join(
        ['{:02x}'.format(
            (uuid.getnode() >> elements) & 0xff
        ) for elements in range(40, -1, -8)]
    )


def get_camera_serial():

    ctx = rs.context()

    devices = ctx.query_devices()

    for dev in devices:

        return dev.get_info(
            rs.camera_info.serial_number
        )

    return "NOT_CONNECTED"


def get_device_fingerprint():

    return {

        "hostname": get_hostname(),

        "machine_uuid": get_machine_uuid(),

        "mac_address": get_mac_address(),

        "camera_serial": get_camera_serial()
    }


def load_device_config():

    config_path = Path(
        "app/device/device_config.json"
    )

    if not config_path.exists():

        default_config = {

    "registered": False,

    "device_id": "",

    "machine_uuid": "",

    "hostname": "",

    "mac_address": "",

    "camera_serial": "",

    "screen_id": "",

    "location_id": "",

    "branch_id": "",

    "company_id": "",

    "last_sync": ""

}

        save_device_config(
            default_config
        )

        return default_config

    with open(
        config_path,
        "r"
    ) as file:

        return json.load(file)
    

    

def save_device_config(data):

    config_path = Path(
        "app/device/device_config.json"
    )

    with open(
        config_path,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


if __name__ == "__main__":

    print("\nDEVICE FINGERPRINT\n")

    print(get_device_fingerprint())

    print("\nDEVICE CONFIG\n")

    print(load_device_config())