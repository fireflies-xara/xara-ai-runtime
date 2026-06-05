from app.device.device_identity import (
    load_device_config
)

from app.communication.device_registration import (
    register_device
)


def main():

    print("\n========== XARA BOOT ==========\n")

    try:

        config = load_device_config()

        if not config.get("registered", False):

            print(
                "[INFO] First Boot Detected"
            )

            config = register_device()

        else:

            print(
                "[INFO] Device Already Registered"
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


if __name__ == "__main__":
    main()