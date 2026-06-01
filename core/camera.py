import cv2
from config.settings import (
    CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_INDEX, CAMERA_FPS, DISPLAY_FLIP
)
from utils.logger import get_logger

log = get_logger(__name__)

class Camera:
    def __init__(self):
        self._cap = None

    def open(self):
        self._cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self._cap.isOpened():
            raise RuntimeError(f'Cannot open Camera {CAMERA_INDEX}')
        
        self._cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self._cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

        self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        log.info(f'Camera opened : {w}x{h}')

    def read(self):
        if not self._cap:
            return False, None
        success, frame = self._cap.read()
        if not success:
            return False, None
        if DISPLAY_FLIP:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        if self._cap and self._cap.isOpened():
            self._cap.release()
            log.info('Camera released.')