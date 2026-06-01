import time
import pyautogui
import cv2
from config.settings import (
    CAMERA_WIDTH, CAMERA_HEIGHT, MOUSE_SMOOTHING_FACTOR, MOUSE_MARGIN, CLICK_COOLDOWN_MS
)
from core.hand_tracker import HandData, HandTracker
from utils.math_utils import euclidean, remap
from utils.logger import get_logger

log = get_logger(__name__)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

CLICK_DIST = 25
RCLICK_DIST = 30
SCROLL_SPEED = 12

def is_fist(pts) -> bool:
    tips = [8, 12, 16, 20]    # index, middle, ring, pinky tips
    pips = [6, 10, 14, 18]    # their middle knuckles
    return all(pts[tip][1] > pts[pip][1] for tip, pip in zip(tips, pips))

class MouseController:
    def __init__(self):
        self._sw, self._sh = pyautogui.size()
        self._cx = self._sw / 2
        self._cy = self._sh / 2
        self._last_click = 0.0
        self._prev_iy = 0.0
        self._fist_prev_y  = 0.0
        self._in_fist_mode = False
        log.info(f'MouseController ready - screen {self._sw}x{self._sh}')

    def process(self, hand: HandData) -> str:
        pts = hand.landmarks_px

        index_tip = pts[HandTracker.INDEX_TIP]
        middle_tip = pts[HandTracker.MIDDLE_TIP]
        thumb_tip = pts[HandTracker.THUMB_TIP]
        wrist = pts[HandTracker.WRIST]

        raw_x = remap(index_tip[0], MOUSE_MARGIN, CAMERA_WIDTH - MOUSE_MARGIN, 0, self._sw)
        raw_y = remap(index_tip[1], MOUSE_MARGIN, CAMERA_HEIGHT - MOUSE_MARGIN, 0, self._sh)

        alpha = MOUSE_SMOOTHING_FACTOR
        self._cx = max(10, min(self._sw - 10, self._cx + alpha * (raw_x - self._cx)))
        self._cy = max(10, min(self._sh - 10, self._cy + alpha * (raw_y - self._cy)))

        pyautogui.moveTo(int(self._cx), int(self._cy))

        i_m = euclidean(index_tip, middle_tip)
        i_t = euclidean(index_tip, thumb_tip)
        gesture = 'MOVE'

        if is_fist(pts):
            if not self._in_fist_mode:
                self._fist_prev_y  = index_tip[1]
                self._in_fist_mode = True
                gesture = 'FIST SCROLL'
            else:
                delta = index_tip[1] - self._fist_prev_y
                if delta > 15:
                    pyautogui.scroll(-8)
                    self._fist_prev_y = index_tip[1]
                    gesture = 'SCROLL DOWN ▼'
                elif delta < -15:
                    pyautogui.scroll(8)
                    self._fist_prev_y = index_tip[1]
                    gesture = 'SCROLL UP ▲'
                else:
                    gesture = 'FIST SCROLL'

        elif i_m < 25 and i_t > 40:
            if self._cooldown_ok():
                pyautogui.click()
                self._last_click = time.time()
                gesture = 'LEFT CLICK'

        elif i_t < 25 and i_m > 40:
            if self._cooldown_ok():
                pyautogui.rightClick()
                self._last_click = time.time()
                gesture = 'RIGHT CLICK'
            else:
                gesture = 'RIGHT CLICK'

        else:
            self._in_fist_mode = False
        self._prev_iy = index_tip[1]
        return gesture, i_m, i_t
    
    def _cooldown_ok(self) -> bool:
        return (time.time() - self._last_click) * 1000 >= CLICK_COOLDOWN_MS
