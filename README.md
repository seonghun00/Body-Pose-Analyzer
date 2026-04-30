# Docker-Pose-Analyzer (AI 자세 분석 시스템)

AI(인공지능) 컴퓨터 비전 기술을 활용하여 사람의 전신 및 측면 사진을 분석하고, 체형 불균형과 거북목 증후군을 자동으로 진단해 주는 웹 애플리케이션입니다. Docker를 기반으로 구축되어 환경에 구애받지 않고 누구나 쉽게 설치하고 실행할 수 있습니다.

---

## 🚀 주요 기능 (Features)

### 1. 편리한 사진 분석 (Image Upload & Batch Select)
- **PC 즉시 업로드**: 웹 브라우저에서 내 PC에 있는 사진을 바로 업로드하여 1초 만에 분석할 수 있습니다.
- **서버 폴더 연동**: `data/images/` 폴더에 사진들을 모아두면, 웹페이지 좌측 사이드바 목록에 실시간으로 표시되며 클릭 한 번으로 즉시 분석이 가능합니다.
- **자동 결과 저장**: 분석이 완료된 이미지는 뼈대와 각도 수치가 직관적으로 오버레이된 채로 `outputs/` 폴더에 자동 저장됩니다.

### 2. 세밀한 5단계 체형 진단 로직
신체의 핵심 랜드마크(관절)를 추적하여 각도를 계산하고, **정상(초록)부터 위험(빨강)까지 5단계**로 시각화하여 경고 문구와 색상을 제공합니다.
(사진 크기에 구애받지 않도록 내부적으로 해상도를 자동 정규화하여 분석 퀄리티와 텍스트 시인성을 극대화했습니다.)

#### 🎯 정면 대칭 분석 (Frontal Symmetry)
* **어깨 비대칭**: 좌우 어깨를 잇는 선과 수평선 간의 각도 절댓값을 측정합니다.
  * `정상(1.5° 이하) ~ 심각(8.0° 초과)`
* **척추/상체 틀어짐**: 어깨 중앙점과 골반 중앙점을 잇는 척추선이 수직 기준선에서 얼마나 벗어났는지 측정합니다.
  * `정상(2.0° 이하) ~ 중증(20.0° 초과)`

#### 🎯 측면 체형 분석 (Side Profile)
* **거북목 (Forward Head Posture)**: 귀와 제7경추(목 뒤 뼈)를 잇는 선분과 수평선 사이의 각도(CVA)를 측정합니다. 각도가 작을수록 목이 앞으로 심하게 빠졌음을 의미합니다.
  * `정상(55° 이상) ~ 위험(40° 미만)`

---

## 🛠 기술 스택 (Tech Stack)

- **Core AI**: Google MediaPipe (가장 정밀한 `model_complexity=2` 사용)
- **Computer Vision**: OpenCV (`opencv-python-headless`)
- **Backend Web Server**: FastAPI, Uvicorn
- **Frontend UI**: HTML5, Tailwind CSS (반응형 다크 모드 디자인 적용)
- **Infrastructure**: Docker, Docker-Compose (Python 3.11-slim)
  *(※ 불필요한 PyTorch 의존성을 제거한 MediaPipe 버전을 채택하여 컨테이너 빌드 속도가 매우 빠릅니다.)*

---

## 📂 프로젝트 폴더 구조 (Directory Structure)

```text
body-pose-analyzer/
├── app/
│   ├── core/              # MediaPipe 추론 엔진 및 5단계 진단 수학 로직
│   │   ├── analyzer_base.py
│   │   ├── analyzer_front.py
│   │   └── analyzer_side.py
│   ├── templates/         # 웹 UI 화면 구성 (index.html)
│   ├── main.py            # FastAPI 웹 서버 라우팅 (API)
│   └── requirements.txt   # 파이썬 라이브러리 목록
├── data/
│   └── images/            # 분석할 원본 사진들을 넣어두는 폴더 (웹 화면에 동기화됨)
├── outputs/               # 분석이 완료된 결과 사진이 자동 저장되는 폴더
├── docker-compose.yml     # 컨테이너 실행 및 로컬 폴더 연동(Mount) 설정
└── Dockerfile             # 도커 시스템 이미지 빌드 명세서
```

---

## 💻 실행 방법 (How to Run)

1. 터미널을 열고 프로젝트 최상위 경로(`c:\work\body-pose-analyzer`)로 이동합니다.
2. 아래 명령어를 실행하여 백그라운드에서 서버를 켭니다.
   ```bash
   docker-compose up -d --build
   ```
3. 웹 브라우저를 열고 **`http://localhost:8000`** 에 접속합니다.
4. 웹 화면의 사이드바에서 `data/images` 폴더의 사진을 선택하거나 직접 업로드하여 분석 결과를 확인합니다!
