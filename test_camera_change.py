from app.device.hardware_monitor import (
    check_hardware_changes
)

changes = check_hardware_changes()

print("\nDetected Changes:\n")

for item in changes:
    print(item)