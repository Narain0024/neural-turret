# src/detector.py
from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE_THRESHOLD, TARGET_CLASSES

class ObjectDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)
        print(f"[Detector] Model loaded: {MODEL_PATH}")

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            class_id = int(box.cls[0])
            label = self.model.names[class_id]

            if TARGET_CLASSES and label not in TARGET_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            detections.append({
                "label": label,
                "confidence": confidence,
                "box": (x1, y1, x2, y2),
                "center": (center_x, center_y)
            })

        detections.sort(key=lambda d: d["confidence"], reverse=True)
        return detections