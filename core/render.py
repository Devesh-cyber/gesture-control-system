import cv2
import numpy as np
from config.settings import (
    LANDMARK_RADIUS, LANDMARK_COLOR, CONNECTION_COLOR, CONNECTION_THICKNESS,
    COLOR_NEON_CYAN, COLOR_NEON_GREEN, COLOR_NEON_PURPLE,
    COLOR_OVERLAY_BG, FONT, FONT_SCALE_MEDIUM, FONT_SCALE_SMALL, FONT_THICKNESS
)
from core.hand_tracker import HandData

CONNECTIONS = [
    (0,1), (1,2), (2,3), (3,4),
    (0,5), (5,6), (6,7), (7,8),
    (5,9), (9,10), (10,11), (11,12),
    (9,13), (13,14), (14,15), (15,16),
    (13,17), (17,18), (18,19), (19,20),
    (0,17)
]

class Renderer:
    def draw_hands(self, frame, hand: HandData):
        pts = hand.landmarks_px

        for a, b in CONNECTIONS:
            cv2.line(frame, pts[a], pts[b], CONNECTION_COLOR,
                     CONNECTION_THICKNESS, cv2.LINE_AA)
            
        for i, pt in enumerate(pts):
            r = LANDMARK_RADIUS + 2 if i in (4,8,12,16,20) else LANDMARK_RADIUS
            cv2.circle(frame, pt, r+2, CONNECTION_COLOR, 1, cv2.LINE_AA)
            cv2.circle(frame, pt, r, LANDMARK_COLOR, -1, cv2.LINE_AA)

    def draw_fps(self, frame, fps: float):
        text = f'FPS: {fps:.0f}'
        h, w = frame.shape[:2]
        (tw, th), _ = cv2.getTextSize(text, FONT, FONT_SCALE_MEDIUM, FONT_THICKNESS)
        x, y = 18, h - 55
        cv2.rectangle(frame, (x-8, y-th-6), (x+tw+8, y+6), COLOR_OVERLAY_BG, -1)
        cv2.rectangle(frame, (x-8, y-th-6), (x+tw+8, y+6), COLOR_NEON_CYAN, 1)
        color = COLOR_NEON_GREEN if fps >= 25 else (0,200,255) if fps >= 15 else (50,50,255)
        cv2.putText(frame, text, (x,y), FONT, FONT_SCALE_MEDIUM, color, FONT_THICKNESS, cv2.LINE_AA)

    def draw_hand_label(self, frame, hand: HandData):
        wrist = hand.landmarks_px[0]
        cv2.putText(frame, f'{hand.handedness} {hand.score:.0%}',
                    (wrist[0]-30, wrist[1]+30), FONT, FONT_SCALE_SMALL,
                    COLOR_NEON_PURPLE,  1, cv2.LINE_AA)
        
    def draw_title_bar(self, frame):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0,0), (w,50), COLOR_OVERLAY_BG, -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        cv2.putText(frame, 'GESTURE CONTROL SYSTEM', (16,32), FONT, FONT_SCALE_MEDIUM,
                    COLOR_NEON_CYAN, FONT_THICKNESS, cv2.LINE_AA)
        cv2.line(frame, (0,50), (w,50), COLOR_NEON_CYAN, 1)

    def draw_corner_brackets(self, frame):
        h, w = frame.shape[:2]
        L, t, c = 30, 2, COLOR_NEON_CYAN
        cv2.line(frame, (0,0), (L,0),c,t); cv2.line(frame, (0,0), (0,L), c, t)
        cv2.line(frame,(w,0),(w-L,0),c,t); cv2.line(frame,(w,0),(w,L),c,t)
        cv2.line(frame,(0,h),(L,h),c,t);   cv2.line(frame,(0,h),(0,h-L),c,t)
        cv2.line(frame,(w,h),(w-L,h),c,t); cv2.line(frame,(w,h),(w,h-L),c,t)

    def draw_geature_panel(self, frame, gesture : str) -> None:
        h, w = frame.shape[:2]
        txt_color = (0, 255,218)
        cv2.putText(frame, gesture, (18, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, txt_color, 2, cv2.LINE_AA)