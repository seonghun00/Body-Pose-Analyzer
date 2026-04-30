import cv2
import numpy as np

class VideoCamera:
    def __init__(self, video_source="/data/videos/sample.mp4"):
        self.video_source = video_source
        self.video = cv2.VideoCapture(self.video_source)
        
        # 영상 소스를 열 수 없을 경우 더미 프레임 생성을 위한 플래그
        self.is_dummy = False
        if not self.video.isOpened():
            print(f"Warning: Could not open {self.video_source}. Using a dummy blank canvas generator.")
            self.is_dummy = True
            
    def __del__(self):
        if not self.is_dummy:
            self.video.release()

    def get_frame(self):
        if self.is_dummy:
            # 영상을 찾을 수 없을 때 빈 캔버스에 안내 문구 출력
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Video Source Not Found", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Please provide {self.video_source}", (50, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            return True, frame
            
        success, image = self.video.read()
        if not success:
            # 영상이 끝나면 다시 처음으로 되감기 (무한 반복 루프)
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
            
        return success, image
