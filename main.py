import cv2

from app.camera.camera_stream import start_camera
from app.detection.person_detector import detect_people
from app.processing.json_generator import create_event_json

def main():

    # Start camera
    cap = start_camera()

    if cap is None:
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Run person detection
        output_frame, detections = detect_people(frame)

        # Print detections
        event_json = create_event_json(detections)

        print(event_json)

        # Display output
        cv2.imshow("XARA AI Detection", output_frame)

        # Press Q to quit
        key = cv2.waitKey(1)

# Press ESC or Q to exit
        if key == 27 or key == ord('q'):
            print("Exiting XARA AI...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()