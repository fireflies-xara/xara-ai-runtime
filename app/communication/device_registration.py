import requests

from app.device.device_identity import (
    get_device_fingerprint,
    save_device_config
)

BACKEND_URL = "http://127.0.0.1:8000/devices/register"


def register_device():

    fingerprint = get_device_fingerprint()

    print(
        "\nSending Fingerprint To Backend\n"
    )

    response = requests.post(
        BACKEND_URL,
        json=fingerprint,
        timeout=10
    )

    if response.status_code != 200:

        raise Exception(
            f"Registration Failed : {response.text}"
        )

    data = response.json()

    config = {

    "registered": True,

    "device_id": data["device_id"],

    "machine_uuid": fingerprint["machine_uuid"],

    "hostname": fingerprint["hostname"],

    "mac_address": fingerprint["mac_address"],

    "camera_serial": fingerprint["camera_serial"],

    "screen_id": "",

    "location_id": "",

    "branch_id": "",

    "company_id": "",

    "last_sync": ""

}

    save_device_config(config)

    print(
        f"\nDevice Registered : "
        f"{data['device_id']}\n"
    )

    return config


if __name__ == "__main__":

    register_device()