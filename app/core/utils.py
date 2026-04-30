import math

def calculate_angle(p1, p2):
    """
    p1, p2: (x, y) 튜플
    두 점을 잇는 선분이 수평선과 이루는 각도를 계산합니다 (도 단위).
    """
    x1, y1 = p1
    x2, y2 = p2
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle

class ExponentialSmoothing:
    """지수 평활법 구현으로 랜드마크 데이터의 떨림을 줄입니다."""
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.last_val = None

    def update(self, val):
        if self.last_val is None:
            self.last_val = val
            return val
        
        # val이 튜플 (x, y)인 경우 각각에 적용
        if isinstance(val, (tuple, list)):
            smoothed = tuple(self.alpha * v + (1 - self.alpha) * lv for v, lv in zip(val, self.last_val))
            self.last_val = smoothed
            return smoothed
        
        smoothed = self.alpha * val + (1 - self.alpha) * self.last_val
        self.last_val = smoothed
        return smoothed
