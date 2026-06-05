import pyrealsense2 as rs

ctx = rs.context()

devices = ctx.query_devices()

if len(devices) == 0:
    print("NO CAMERA DETECTED")

else:

    print("CAMERA FOUND")

    for dev in devices:

        print(
            dev.get_info(
                rs.camera_info.name
            )
        )

        print(
            dev.get_info(
                rs.camera_info.serial_number
            )
        )