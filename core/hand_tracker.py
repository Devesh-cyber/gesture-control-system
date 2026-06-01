import cv2
import mediapipe as mp
from dataclasses import dataclass
from config.settings import (
    MP_MAX_HANDS, MP_DETECTION_CONFIDENCE, MP_TRACKING_CONFIDENCE
)
from utils.logger import get_logger

log = get_logger(__name__)

@dataclass
class HandData:
    landmarks_px: list
    landmarks_norm: list
    handedness: str
    score: float

class HandTracker:
    WRIST = 0
    THUMB_TIP = 4
    INDEX_TIP = 8
    INDEX_MCP = 5
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    FINGER_PIPS = [3,6,10,14,18]

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self._hands = self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = MP_MAX_HANDS,
            min_detection_confidence = MP_DETECTION_CONFIDENCE,
            min_tracking_confidence = MP_TRACKING_CONFIDENCE
        )
        log.info('HandTrcaker ready.')

    def process(self, frame_bgr) -> list:
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        rgb.flags.writeable = False
        results = self._hands.process(rgb)
        rgb.flags.writeable = True

        hands = []

        if not results.multi_hand_landmarks:
            return hands
        
        for lm_list, handedness_info in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            px_pts = [(int(lm.x * w), int(lm.y * h)) for lm in lm_list.landmark]
            norm_pts = [(lm.x, lm.y, lm.z) for lm in lm_list.landmark]
            hands.append(HandData(
                landmarks_px=px_pts,
                landmarks_norm=norm_pts,
                handedness=handedness_info.classification[0].label,
                score=handedness_info.classification[0].score,
            ))
            return hands
        
    def close(self):
        self._hands.close()