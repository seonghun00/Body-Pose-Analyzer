import cv2
import math
import numpy as np
from .analyzer_base import PoseAnalyzer, mp_pose
from .utils import calculate_angle

def get_shoulder_severity(angle):
    val = abs(angle)
    if val <= 1.5:
        return "Level 1: Normal", (0, 255, 0) # Green
    elif val <= 3.0:
        return "Level 2: Mild", (173, 255, 47) # GreenYellow
    elif val <= 5.0:
        return "Level 3: Suspected", (0, 255, 255) # Yellow
    elif val <= 8.0:
        return "Level 4: Evident", (0, 165, 255) # Orange
    else:
        return "Level 5: Severe", (0, 0, 255) # Red

def get_spine_severity(angle):
    val = abs(angle)
    if val <= 2.0:
        return "Level 1: Normal", (0, 255, 0)
    elif val <= 6.0:
        return "Level 2: Mild", (173, 255, 47)
    elif val <= 10.0:
        return "Level 3: Moderate", (0, 255, 255)
    elif val <= 20.0:
        return "Level 4: Severe", (0, 165, 255)
    else:
        return "Level 5: Dangerous", (0, 0, 255)

class FrontAnalyzer(PoseAnalyzer):
    def analyze_and_draw(self, image, landmarks):
        h, w, _ = image.shape
        
        # 1. 어깨 비대칭
        l_sh = self._get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], w, h)
        r_sh = self._get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], w, h)
        shoulder_angle = calculate_angle(r_sh, l_sh)
        sh_status, sh_color = get_shoulder_severity(shoulder_angle)
        
        # 2. 골반 (시각화용)
        l_hip = self._get_coords(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value], w, h)
        r_hip = self._get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value], w, h)
        
        # 3. 척추/상체 틀어짐 (어깨 중앙점 - 골반 중앙점 수직 각도)
        mid_sh = (int((l_sh[0] + r_sh[0])/2), int((l_sh[1] + r_sh[1])/2))
        mid_hip = (int((l_hip[0] + r_hip[0])/2), int((l_hip[1] + r_hip[1])/2))
        
        dx = mid_sh[0] - mid_hip[0]
        dy = mid_hip[1] - mid_sh[1] # Y축 반전
        spine_horizontal_angle = math.degrees(math.atan2(dy, dx))
        spine_angle = abs(90.0 - abs(spine_horizontal_angle)) # 수직선(90도) 기준 틀어짐 정도
        
        sp_status, sp_color = get_spine_severity(spine_angle)
        
        # --- 시각화 (선 그리기) ---
        cv2.line(image, r_sh, l_sh, sh_color, 3)
        cv2.line(image, r_hip, l_hip, (200, 200, 200), 2)
        cv2.line(image, mid_sh, mid_hip, sp_color, 4)
        cv2.circle(image, mid_sh, 5, (255, 255, 255), -1)
        cv2.circle(image, mid_hip, 5, (255, 255, 255), -1)
        
        # 수직 기준선 그리기 (골반 중앙에서 위로)
        cv2.line(image, mid_hip, (mid_hip[0], mid_hip[1] - 300), (0, 255, 0), 2)
        
        # --- 텍스트 출력 ---
        padding_height = 200
        padding = np.zeros((padding_height, w, 3), dtype=np.uint8)
        image = np.vstack((image, padding))
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, "Mode: Frontal Symmetry", (20, h + 30), font, 0.9, (255, 255, 255), 2)
        
        # 어깨 비대칭 출력
        cv2.putText(image, f"Shoulder: {abs(shoulder_angle):.1f} deg", (20, h + 80), font, 0.7, (255, 255, 255), 2)
        cv2.putText(image, f"[{sh_status}]", (350, h + 80), font, 0.7, sh_color, 2)
        
        # 척추 틀어짐 출력
        cv2.putText(image, f"Spine: {spine_angle:.1f} deg", (20, h + 130), font, 0.7, (255, 255, 255), 2)
        cv2.putText(image, f"[{sp_status}]", (350, h + 130), font, 0.7, sp_color, 2)
            
        return image
