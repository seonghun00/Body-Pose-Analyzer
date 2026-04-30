import cv2
import mediapipe as mp
from abc import ABC, abstractmethod

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class PoseAnalyzer(ABC):
    def __init__(self):
        # MediaPipe Pose 인스턴스 초기화
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=2
        )
    
    def process(self, frame):
        """프레임을 입력받아 MediaPipe 추론 후, 결과가 오버레이된 프레임을 반환합니다."""
        # 글씨 크기가 일정하도록 이미지 크기를 정규화 (최대 해상도 800px)
        h, w = frame.shape[:2]
        max_dim = max(h, w)
        if max_dim > 800 or max_dim < 600:
            scale = 800.0 / max_dim
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
            
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 기본 랜드마크 뼈대 그리기
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # 자식 클래스에서 구체적인 각도 분석 및 시각화 수행
            image = self.analyze_and_draw(image, results.pose_landmarks.landmark)
            
        return image

    @abstractmethod
    def analyze_and_draw(self, image, landmarks):
        """각 분석기(정면/측면)가 구현해야 할 추상 메서드"""
        pass
        
    def _get_coords(self, landmark, image_width, image_height):
        return int(landmark.x * image_width), int(landmark.y * image_height)
