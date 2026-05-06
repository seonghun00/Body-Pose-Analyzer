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


