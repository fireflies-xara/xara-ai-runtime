from datetime import datetime

def create_event_json(detections):

    event_data = {
        "camera_id": "CAM_01",
        "timestamp": datetime.now().isoformat(),
        "detections": detections
    }

    return event_data