<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=80&section=header" width="100%" />
</p>

##### [English](README.md) | **한국어**

# 🤖 인공지능 포즈 분석 시스템
> **AI 인공지능 기술을 활용한 전신 자세 및 체형 불균형 분석 솔루션.**

<p align="left">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat&logo=opensourceinitiative&logoColor=white"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white"></a>
  <a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white"></a>
</p>

AI 컴퓨터 비전 기술을 활용하여 사람의 정면 및 측면 사진을 분석하고, 체형 불균형과 거북목 증후군을 자동으로 진단해 주는 웹 애플리케이션입니다.

---

## 🛠️ Tech Stack (기술 스택)
* **MediaPipe** : model_complexity=2를 활용한 정밀한 관절 포인트 추론 수행.
* **FastAPI** : 고성능 백엔드 웹 서버 구축 및 실시간 이미지 처리 API 담당.
* **Docker** : Docker-Compose를 통한 OS 독립적인 컨테이너 기반 실행 환경 제공.

---

## 📁 Project Structure (파일 구조)
```text
body-pose-analyzer/
├── app/
│   ├── core/               # MediaPipe 추론 엔진 및 5단계 진단 수학 로직
│   ├── templates/          # 웹 UI 화면 구성 (FastAPI Jinja2 & Tailwind CSS)
│   ├── main.py             # 웹 서버 실행 및 API 엔드포인트 정의
│   └── requirements.txt    # 프로젝트 의존성 라이브러리 목록
├── data/images/            # 분석 대상 원본 사진 보관 및 실시간 동기화 폴더
├── outputs/                # 분석 완료된 결과 이미지 자동 저장 폴더
├── docker-compose.yml      # 컨테이너 서비스 정의 및 로컬 볼륨 마운트 설정
└── Dockerfile              # 컨테이너 빌드를 위한 시스템 이미지 명세
```

---

## 🔄 Workflow (워크플로우)
<p align="center">
<img src="https://github.com/user-attachments/assets/50b7331c-3074-4de6-8d64-f51cbe360902" width="100%" alt="실행 결과">
<sub><em>▲ 이미지 입력부터 분석, 최종 진단 결과 저장까지의 전체 흐름도</em></sub>
</p>

---

## 📊 Result (실행 결과)
<p align="center">
<img src="https://github.com/user-attachments/assets/33c2f601-baca-4c56-a90d-875e91d07d11" width="100%" alt="실행 결과">
<sub><em>▲ 측면 분석 모드에서 거북목(CVA) 각도를 측정하고 위험도를 시각화한 결과 화면</em></sub>
</p>

---

## 🚀 Getting Started (실행 방법)
### 사전 준비
* Docker 및 Docker Compose 설치 완료.
* 분석에 사용할 정면 또는 측면 사진 준비.

### 설치 및 실행
1. 프로젝트 최상위 경로로 이동.
2. 아래 명령어를 입력하여 Docker 서비스 빌드 및 실행.
   ```bash
   docker-compose up -d --build
   ```
3. 웹 브라우저에서 **`http://localhost:8000`** 접속.
4. 사이드바에서 이미지를 선택하거나 파일을 직접 업로드하여 분석 수행.

---

© 2026 Seong-hun Bae.
