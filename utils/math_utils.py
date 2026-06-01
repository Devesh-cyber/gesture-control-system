import math
import numpy as np

def euclidean(p1, p2) -> float:
    """Straight-line distance between two (x, y) points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def remap(value, in_min, in_max, out_min, out_max) -> float:
    """Map value from one range to another, clamped."""
    value = max(in_min, min(in_max, value))
    ratio = (value - in_min) / (in_max - in_min)
    return out_min + ratio * (out_max - out_min)

def ema_point(current, target, alpha) -> tuple:
    """Exponential moving average for (x, y) — used for cursor smoothing.""" 
    x = current[0] + alpha * (target[0] - current[0])
    y = current[1] + alpha * (target[1] - current[1])
    return (x,y)  