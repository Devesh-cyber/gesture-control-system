import time
from collections import deque

class FPSCounter:
    def __init__(self, smoothing : int = 10):
        self._time = deque(maxlen=smoothing)
        self._last = time.perf_counter()

    def tick(self) -> float:
        now = time.perf_counter()
        delta = now - self._last
        self._last = now
        if delta > 0:
            self._time.append(delta)
        if not self._time:
            return 0.0
        return 1.0 / (sum(self._time) / len(self._time))