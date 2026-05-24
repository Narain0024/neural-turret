# src/main.py
import cv2
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from detector import ObjectDetector
from tracker import TurretTracker
from hud import draw_overlay
from config import FRAME_WIDTH, FRAME_HEIGHT

def main():
    print("[NEURAL-TURRET] Initializing...")

    detector = ObjectDetector()
    tracker = TurretTracker()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[NEURAL-TURRET] System ONLINE. Press Q to quit, P for screenshot.")

    fps = 0.0
    frame_count = 0
    fps_timer = time.time()
    detections = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame read failed.")
            break

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        # Run detection every 2nd frame for performance
        if frame_count % 2 == 0:
            detections = detector.detect(frame)

        tracker.update(detections)
        state = tracker.get_state()

        # Draw secondary detections dimly
        for det in detections[1:]:
            x1, y1, x2, y2 = det["box"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 80, 20), 1)

        frame = draw_overlay(frame, state, fps, frame_count)

        # FPS counter
        frame_count += 1
        if frame_count % 15 == 0:
            fps = 15.0 / (time.time() - fps_timer)
            fps_timer = time.time()

        cv2.imshow("NEURAL-TURRET | AI Tracking System", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/capture_{frame_count}.png"
            cv2.imwrite(path, frame)
            print(f"[INFO] Screenshot saved: {path}")

    cap.release()
    cv2.destroyAllWindows()
    print("[NEURAL-TURRET] Shutdown complete.")

if __name__ == "__main__":
    main()