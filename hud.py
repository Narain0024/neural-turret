# src/hud.py
import cv2
import numpy as np
import math
import time

COLOR_PRIMARY = (0, 255, 70)
COLOR_DIM     = (0, 140, 40)
COLOR_LOCK    = (0, 60, 255)
COLOR_AMBER   = (0, 180, 255)

FONT = cv2.FONT_HERSHEY_SIMPLEX


def draw_overlay(frame, state, fps, frame_count):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    _draw_border(frame, w, h, state["is_locked"])
    _draw_static_crosshair(frame, cx, cy)

    if state["tracking"] and state["target"]:
        _draw_target_box(frame, state["target"])

    _draw_turret_crosshair(frame, state["crosshair"], state["is_locked"])
    _draw_status(frame, state, fps)
    _draw_gauges(frame, state["angle_x"], state["angle_y"], w, h)
    _draw_scan_line(frame, frame_count, w, h, state["tracking"])

    return frame


def _draw_border(frame, w, h, locked):
    color = COLOR_LOCK if locked else COLOR_DIM
    L = 40
    t = 2
    cv2.line(frame, (10, 10), (10+L, 10), color, t)
    cv2.line(frame, (10, 10), (10, 10+L), color, t)
    cv2.line(frame, (w-10, 10), (w-10-L, 10), color, t)
    cv2.line(frame, (w-10, 10), (w-10, 10+L), color, t)
    cv2.line(frame, (10, h-10), (10+L, h-10), color, t)
    cv2.line(frame, (10, h-10), (10, h-10-L), color, t)
    cv2.line(frame, (w-10, h-10), (w-10-L, h-10), color, t)
    cv2.line(frame, (w-10, h-10), (w-10, h-10-L), color, t)


def _draw_target_box(frame, target):
    x1, y1, x2, y2 = target["box"]
    conf = target["confidence"]
    label = target["label"]
    color = COLOR_PRIMARY
    b = 20
    t = 2
    cv2.line(frame, (x1, y1), (x1+b, y1), color, t)
    cv2.line(frame, (x1, y1), (x1, y1+b), color, t)
    cv2.line(frame, (x2, y1), (x2-b, y1), color, t)
    cv2.line(frame, (x2, y1), (x2, y1+b), color, t)
    cv2.line(frame, (x1, y2), (x1+b, y2), color, t)
    cv2.line(frame, (x1, y2), (x1, y2-b), color, t)
    cv2.line(frame, (x2, y2), (x2-b, y2), color, t)
    cv2.line(frame, (x2, y2), (x2, y2-b), color, t)
    cv2.putText(frame, f"{label.upper()} {conf*100:.0f}%",
                (x1, y1-8), FONT, 0.5, color, 1)


def _draw_turret_crosshair(frame, pos, locked):
    x, y = pos
    color = COLOR_LOCK if locked else COLOR_AMBER
    radius = 18
    gap = 6
    ll = 22
    t = 2

    # Pulse effect when locked
    if locked:
        pulse = int(radius + 4 * abs(math.sin(time.time() * 6)))
        cv2.circle(frame, (x, y), pulse, color, 1)

    cv2.circle(frame, (x, y), radius, color, t)
    cv2.circle(frame, (x, y), 3, color, -1)
    cv2.line(frame, (x-(radius+ll), y), (x-gap, y), color, t)
    cv2.line(frame, (x+gap, y), (x+(radius+ll), y), color, t)
    cv2.line(frame, (x, y-(radius+ll)), (x, y-gap), color, t)
    cv2.line(frame, (x, y+gap), (x, y+(radius+ll)), color, t)

    if locked:
        cv2.putText(frame, "LOCKED", (x+radius+5, y+5),
                    FONT, 0.5, color, 1)


def _draw_static_crosshair(frame, cx, cy):
    cv2.line(frame, (cx-15, cy), (cx-4, cy), COLOR_DIM, 1)
    cv2.line(frame, (cx+4, cy), (cx+15, cy), COLOR_DIM, 1)
    cv2.line(frame, (cx, cy-15), (cx, cy-4), COLOR_DIM, 1)
    cv2.line(frame, (cx, cy+4), (cx, cy+15), COLOR_DIM, 1)
    cv2.circle(frame, (cx, cy), 8, COLOR_DIM, 1)


def _draw_status(frame, state, fps):
    lines = [
        f"SYS: {'TRACKING' if state['tracking'] else 'SCANNING'}",
        f"FPS: {fps:.1f}",
        f"PAN:  {state['angle_x']:+.1f} deg",
        f"TILT: {state['angle_y']:+.1f} deg",
    ]
    if state["target"]:
        lines.append(f"TGT: {state['target']['label'].upper()}")
        lines.append(f"CONF: {state['target']['confidence']*100:.0f}%")

    for i, line in enumerate(lines):
        color = COLOR_LOCK if (i == 0 and state["tracking"]) else COLOR_PRIMARY
        cv2.putText(frame, line, (18, 35 + i*22), FONT, 0.5, color, 1)


def _draw_gauges(frame, angle_x, angle_y, w, h):
    cx = w // 2
    cy_base = h - 35
    max_angle = 35.0

    for i, (angle, label) in enumerate([(angle_x, "PAN"),
                                         (angle_y, "TILT")]):
        ox = cx + (i * 160) - 80
        cv2.ellipse(frame, (ox, cy_base), (35, 20), 0, 180, 360,
                    COLOR_DIM, 1)
        ratio = max(-1, min(1, angle / max_angle))
        needle_angle = 270 + ratio * 90
        nx = int(ox + 30 * np.cos(np.radians(needle_angle)))
        ny = int(cy_base + 20 * np.sin(np.radians(needle_angle)))
        cv2.line(frame, (ox, cy_base), (nx, ny), COLOR_AMBER, 2)
        cv2.putText(frame, label, (ox-12, cy_base+18),
                    FONT, 0.38, COLOR_DIM, 1)


def _draw_scan_line(frame, frame_count, w, h, tracking):
    if tracking:
        return
    y = int((frame_count * 3) % h)
    cv2.line(frame, (0, y), (w, y), (0, 60, 0), 1)