# src/tracker.py
from config import (FRAME_WIDTH, FRAME_HEIGHT, SMOOTHING_FACTOR,
                    HORIZONTAL_FOV, VERTICAL_FOV, LOCK_THRESHOLD_PX,
                    MAX_MISSING_FRAMES)

class TurretTracker:
    def __init__(self):
        self.screen_cx = FRAME_WIDTH // 2
        self.screen_cy = FRAME_HEIGHT // 2

        self.crosshair_x = float(self.screen_cx)
        self.crosshair_y = float(self.screen_cy)

        self.target = None
        self.last_target = None
        self.frames_since_detection = 0

        self.angle_x = 0.0
        self.angle_y = 0.0
        self.is_locked = False
        self.tracking = False

    def update(self, detections):
        if detections:
            self.last_target = detections[0]
            self.frames_since_detection = 0
        else:
            self.frames_since_detection += 1
            if self.frames_since_detection > MAX_MISSING_FRAMES:
                self.last_target = None

        self.target = self.last_target

        if not self.target:
            self.tracking = False
            self.is_locked = False
            self.crosshair_x += (self.screen_cx - self.crosshair_x) * 0.05
            self.crosshair_y += (self.screen_cy - self.crosshair_y) * 0.05
            return

        self.tracking = True
        tx, ty = self.target["center"]

        self.crosshair_x += (tx - self.crosshair_x) * SMOOTHING_FACTOR
        self.crosshair_y += (ty - self.crosshair_y) * SMOOTHING_FACTOR

        error_x = tx - self.screen_cx
        error_y = ty - self.screen_cy

        self.angle_x = (error_x / FRAME_WIDTH) * HORIZONTAL_FOV
        self.angle_y = (error_y / FRAME_HEIGHT) * VERTICAL_FOV

        dist = ((self.crosshair_x - tx)**2 +
                (self.crosshair_y - ty)**2) ** 0.5
        self.is_locked = dist < LOCK_THRESHOLD_PX

    def get_state(self):
        return {
            "crosshair": (int(self.crosshair_x), int(self.crosshair_y)),
            "angle_x": self.angle_x,
            "angle_y": self.angle_y,
            "is_locked": self.is_locked,
            "tracking": self.tracking,
            "target": self.target
        }