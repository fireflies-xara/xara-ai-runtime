from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

def detect_people(frame):

    results = model(frame)

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            confidence = float(box.conf[0])

            # YOLO class 0 = person
            if cls == 0:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "object": "person",
                    "confidence": round(confidence, 2),
                    "position": {
                        "x": x1,
                        "y": y1
                    }
                })

                # Draw rectangle
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Label
                cv2.putText(
                    frame,
                    f"Person {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    return frame, detections