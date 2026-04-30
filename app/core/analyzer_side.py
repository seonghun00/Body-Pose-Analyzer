import cv2
import math
import numpy as np
from .analyzer_base import PoseAnalyzer, mp_pose

def get_cva_severity(angle):
    # CVA (Craniovertebral Angle) - 각도가 작을수록 위험
    if angle >= 55.0:
        return "Level 1: Normal", (0, 255, 0)
    elif angle >= 50.0:
        return "Level 2: Caution", (173, 255, 47)
    elif angle >= 45.0:
        return "Level 3: Early", (0, 255, 255)
    elif angle >= 40.0:
        return "Level 4: Severe", (0, 165, 255)
    else:
        return "Level 5: Dangerous", (0, 0, 255)

class SideAnalyzer(PoseAnalyzer):
    def analyze_and_draw(self, image, landmarks):
        h, w, _ = image.shape
        
        # 측면을 왼쪽으로 보고 있다고 가정 (Left 기준)
        l_ear = self._get_coords(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value], w, h)
        l_sh = self._get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], w, h)
        l_hip = self._get_coords(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value], w, h)
        
        # 거북목 각도 (CVA): 귀와 7번 경추(어깨)를 잇는 선분과 수평선 사이의 각도
        # 수평선 방향을 양의 X축이라 할 때
        dx = l_ear[0] - l_sh[0]
        dy = l_sh[1] - l_ear[1] # Y좌표는 아래로 갈수록 커지므로 반전
        
        # CVA는 수평선 대비 각도 (일반적으로 양수)
        cva_angle = math.degrees(math.atan2(dy, abs(dx) if dx != 0 else 1)) 
        
        # CVA가 만약 음수로 계산된다면, 사람의 귀가 어깨보다 밑에 있다는 의미(비정상 케이스)
        
        # 단계 판별
        status, color = get_cva_severity(cva_angle)
        
        # 시각화
        # 수평 기준선 (어깨에서 앞으로)
        horizontal_pt = (l_sh[0] + 150, l_sh[1]) if dx >= 0 else (l_sh[0] - 150, l_sh[1])
        cv2.line(image, l_sh, horizontal_pt, (0, 255, 0), 2)
        
        cv2.line(image, l_sh, l_ear, color, 3)             # CVA 각도선
        cv2.line(image, l_sh, l_hip, (255, 0, 255), 3)     # 상체(척추) 라인
        
        # 하단 패딩
        padding_height = 200
        padding = np.zeros((padding_height, w, 3), dtype=np.uint8)
        image = np.vstack((image, padding))
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "Mode: Side Profile (CVA)", (20, h + 30), font, 0.9, (255, 255, 255), 2)
        
        # 각도 정보 출력
        cv2.putText(image, f"CVA (Neck Angle): {cva_angle:.1f} deg", (20, h + 80), font, 0.7, (255, 255, 255), 2)
        cv2.putText(image, f"[{status}]", (400, h + 80), font, 0.8, color, 2)
            
        return image
