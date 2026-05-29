import pyrealsense2 as rs
import numpy as np

pipeline = rs.pipeline()

config = rs.config()

config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.bgr8,
    30
)

pipeline.start(config)


def get_frame():

    frames = pipeline.wait_for_frames()

    color_frame = frames.get_color_frame()

    if not color_frame:
        return None

    return np.asanyarray(
        color_frame.get_data()
    )


def stop_camera():

    pipeline.stop()