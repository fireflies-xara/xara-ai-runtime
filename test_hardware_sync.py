from app.device.hardware_monitor import (
    check_hardware_changes
)

from app.communication.hardware_sync import (
    sync_hardware_changes
)

changes = check_hardware_changes()

print(changes)

response = sync_hardware_changes(
    "DEV-0001",
    changes
)

print(response)