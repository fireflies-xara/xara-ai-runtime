from app.device.device_identity import (
    load_device_config
)

from app.communication.device_registration import (
    register_device
)

from app.device.hardware_monitor import (
    check_hardware_changes
)


def initialize_xara():

    print(
        "\n========== XARA BOOT ==========\n"
    )

    try:

        config = load_device_config()

        if not config.get(
            "registered",
            False
        ):

            print(
                "[INFO] First Boot Detected"
            )

            config = register_device()

        else:

            print(
                "[INFO] Device Already Registered"
            )

            changes = (
                check_hardware_changes()
            )

            if changes:

                print(
                    "\n[HARDWARE CHANGES DETECTED]"
                )

                for change in changes:

                    print(
                        f" - {change}"
                    )

            else:

                print(
                    "[INFO] No Hardware Changes"
                )

        print(
            f"\n[DEVICE ID] "
            f"{config['device_id']}"
        )

        print(
            "\n========== BOOT COMPLETE ==========\n"
        )

    except Exception as e:

        print(
            f"\n[ERROR] {e}"
        )

        print(
            "\nXARA Startup Failed\n"
        )