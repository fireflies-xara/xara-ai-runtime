import cv2

def start_camera():

    cap = cv2.VideoCapture(4)

    if not cap.isOpened():
        print("ERROR: Cannot access camera")
        return None

    print("Camera started successfully")

    return cap