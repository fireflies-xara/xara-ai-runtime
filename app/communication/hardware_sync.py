import requests


BACKEND_URL = (
    "http://127.0.0.1:8000/devices/update-hardware"
)


def sync_hardware_changes(
    device_id,
    changes
):

    payload = {

        "device_id": device_id,

        "changes": changes
    }

    response = requests.post(
        BACKEND_URL,
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    return response.json()