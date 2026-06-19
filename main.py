from app.bootstrap.startup import (
    initialize_xara
)

from app.device.hardware_monitor import (
    check_hardware_changes
)

from app.communication.hardware_sync import (
    sync_hardware_changes
)

from app.device.device_identity import (
    get_device_fingerprint,
    save_device_config
)


if __name__ == "__main__":

    initialize_xara()