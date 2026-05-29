import cv2

from app.camera.camera_stream import (
    get_frame,
    stop_camera
)

from app.detection.person_detector import (
    detect_people
)

from app.processing.json_generator import (
    create_event_json
)


def main():

    while True:

        frame = get_frame()

        if frame is None:
            continue

        output_frame, detections = detect_people(frame)

        event_json = create_event_json(
            detections
        )

        print(event_json)

        cv2.imshow(
            "XARA AI Detection",
            output_frame
        )

        key = cv2.waitKey(1)

        if key == 27 or key == ord("q"):
            print("Exiting XARA AI...")
            break

    stop_camera()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()