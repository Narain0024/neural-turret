<div align="center">

<img src="assets/banner.png" alt="Neural Turret Banner" width="100%"/>

# 🎯 NEURAL-TURRET
### Autonomous AI Object Tracking System

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green?logo=opencv&logoColor=white)](https://opencv.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)](https://ultralytics.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![CI](https://github.com/Narain0024/neural-turret/actions/workflows/ci.yml/badge.svg)](https://github.com/Narain0024/neural-turret/actions)

**Real-time object detection and autonomous tracking system that simulates
an intelligent pan-tilt turret using computer vision and proportional control.**

[Features](#features) • [Demo](#demo) • [Architecture](#architecture) • [Setup](#installation) • [Usage](#usage)

</div>

---

## 📽️ Demo

<div align="center">
<img src="demo/demo.gif" width="80%" alt="Neural Turret Demo"/>
</div>

> The system detects the primary target via YOLOv8, locks the tracking
> crosshair using a proportional controller, and displays real-time
> pan/tilt angle offsets on the tactical HUD.

---

## Overview

Neural-Turret is a software simulation of an autonomous robotic targeting
system. It demonstrates the core perception-action loop found in real
pan-tilt camera gimbals, surveillance drones, and autonomous tracking
platforms — implemented entirely in Python without requiring hardware.

The system runs a YOLOv8 inference pipeline on each webcam frame,
extracts the bounding box of the highest-confidence detection, calculates
the angular error between the target and screen center, and drives a
simulated turret crosshair using proportional control with configurable
smoothing. A custom tactical HUD overlays real-time system state including
angle gauges, lock indicators, and target telemetry.

---

## Features

### Core
- **YOLOv8 real-time inference** — 25+ FPS on CPU with nano model
- **Proportional control tracking** — smooth crosshair pursuit with
  configurable gain and smoothing constants
- **Angular offset calculation** — pixel error converted to degrees
  using FOV-based coordinate mapping
- **Target lock detection** — threshold-based lock acquisition with
  animated visual indicator
- **Object persistence** — target held across missed frames to eliminate flicker

### HUD System
- Military-style corner bracket target boxes
- Dynamic crosshair with gap-style reticle
- Real-time pan/tilt angle arc gauges
- System status panel (FPS, confidence, angles, target class)
- Animated scan line in standby mode
- Pulsing LOCKED indicator on target acquisition

### Engineering
- Modular architecture — detector, tracker, renderer fully decoupled
- Centralized config file for all tunable parameters
- Frame-skip inference for improved throughput
- Screenshot capture with `P` key

---

## Architecture

<div align="center">
<img src="docs/architecture.png" width="75%" alt="System Architecture"/>
</div>

```
Webcam Input
     │
     ▼
Frame Capture → YOLOv8 Inference
                       │
               Detection List
                       │
                Tracker Update
               ↙              ↘
    Angle Calculation    Crosshair Smoothing
               ↘              ↙
               HUD Renderer
                       │
               Display Output
```

### Key Modules

| Module | File | Responsibility |
|---|---|---|
| Detector | `detector.py` | YOLOv8 wrapper — frame in, detection list out |
| Tracker | `tracker.py` | Control loop — error calculation, smoothing, lock logic |
| HUD | `hud.py` | All OpenCV drawing — zero logic, pure rendering |
| Config | `config.py` | Single source of truth for all parameters |
| Main | `main.py` | Pipeline orchestration and capture loop |

---

## Tracking Mathematics

```
pixel_error_x = target_center_x - screen_center_x
pixel_error_y = target_center_y - screen_center_y

pan_angle  = (pixel_error_x / frame_width)  × H_FOV
tilt_angle = (pixel_error_y / frame_height) × V_FOV

crosshair_x += (target_x - crosshair_x) × smoothing_factor
crosshair_y += (target_y - crosshair_y) × smoothing_factor
```

This is the same fundamental control law used in physical gimbal
servo systems. Simulating the software layer in isolation allows
tuning before hardware integration.

---

## Technologies Used

| Technology | Role |
|---|---|
| Python 3.10 | Core application language |
| YOLOv8 (Ultralytics) | Real-time object detection inference |
| OpenCV 4.8 | Frame capture, image processing, HUD rendering |
| NumPy | Array operations and coordinate math |

---

## Installation

### Requirements
- Windows 10/11
- Python 3.10
- Webcam (built-in or USB)

### Setup

```cmd
git clone https://github.com/Narain0024/neural-turret.git
cd neural-turret

python -m venv venv
venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

The YOLOv8 model (`yolov8n.pt`, ~6MB) downloads automatically
on first run.

---

## Usage

```cmd
venv\Scripts\activate
cd src
python main.py
```

### Controls

| Key | Action |
|---|---|
| `Q` | Quit |
| `P` | Save screenshot to `screenshots/` |

### Configuration

All parameters are in `src/config.py`:

```python
CONFIDENCE_THRESHOLD = 0.45   # Detection sensitivity
TARGET_CLASSES = ["person"]   # Filter by class, or [] for all
SMOOTHING_FACTOR = 0.10       # Tracking speed (0.05=slow, 0.20=fast)
HORIZONTAL_FOV = 62.0         # Webcam horizontal FOV in degrees
```

---

## Screenshots

<div align="center">

| Tracking Active | Target Locked |
|---|---|
| <img src="screenshots/tracking_active.png" width="400"/> | <img src="screenshots/locked_state.png" width="400"/> |

| Scanning Mode | Angle Gauges |
|---|---|
| <img src="screenshots/scanning_mode.png" width="400"/> | <img src="screenshots/angle_gauges.png" width="400"/> |

</div>

---

## Project Structure

```
neural-turret/
├── src/
│   ├── main.py          # Entry point
│   ├── config.py        # All parameters
│   ├── detector.py      # YOLO inference
│   ├── tracker.py       # Control logic
│   └── hud.py           # HUD rendering
├── docs/
│   └── architecture.png
├── screenshots/
├── demo/
│   └── demo.gif
├── tests/
├── requirements.txt
└── README.md
```

---

## Roadmap

- [x] YOLOv8 real-time detection pipeline
- [x] Proportional control tracking
- [x] Tactical HUD overlay
- [x] Angular offset calculation
- [x] Object persistence across missed frames
- [ ] Kalman filter tracking
- [ ] Multi-target prioritization
- [ ] Custom-trained detection model
- [ ] Hardware servo integration (ROS2)

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
Built by <a href="https://github.com/Narain0024">Narain</a> · Python • OpenCV • YOLOv8
</div>
