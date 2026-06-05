from app.device.device_identity import (
    load_device_config
)

from app.communication.device_registration import (
    register_device
)


def initialize_xara():

    print("\n========== XARA BOOT ==========\n")

    config = load_device_config()

    registered = config.get(
        "registered",
        False
    )

    if not registered:

        print(
            "[INFO] Device Not Registered"
        )

        register_device()

        print(
            "[INFO] Registration Completed"
        )

    else:

        print(
            f"[INFO] Device Already Registered : "
            f"{config.get('device_id')}"
        )

    print(
        "\n========== STARTING AI ==========\n"
    )