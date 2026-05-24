# src/config.py

# Model
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.45
TARGET_CLASSES = ["person"]  # Change to [] to track any object

# Display
FRAME_WIDTH = 960
FRAME_HEIGHT = 540

# Tracking
SMOOTHING_FACTOR = 0.10
LOCK_THRESHOLD_PX = 20
HORIZONTAL_FOV = 62.0
VERTICAL_FOV = 48.0

# Persistence
MAX_MISSING_FRAMES = 8