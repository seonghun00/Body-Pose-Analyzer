<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=80&section=header" width="100%" />
</p>

##### **English** | [한국어](README.ko.md)

# 🐳 Docker-Pose-Analyzer
> **AI-powered body posture and symmetry analysis system with Docker-ready deployment.**

<p align="left">
  <img src="https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white">
</p>

This web application utilizes AI computer vision to analyze full-body and profile photos, automatically diagnosing body imbalances and Forward Head Posture (FHP).

---

## 🛠️ Tech Stack
* **MediaPipe** : Executes high-precision pose estimation with model complexity level 2.
* **FastAPI** : Manages backend web server and real-time image processing API.
* **Docker** : Provides a containerized environment for consistent deployment via Docker-Compose.

---

## 📁 Project Structure
```text
body-pose-analyzer/
├── app/
│   ├── core/               # MediaPipe inference engine & diagnostic math logic
│   ├── templates/          # Web UI layout (index.html with Tailwind CSS)
│   ├── main.py             # FastAPI routing and API endpoints
│   └── requirements.txt    # Python library dependencies
├── data/images/            # Source folder for image uploads and batch selection
├── outputs/                # Folder for automatically saved analysis results
├── docker-compose.yml      # Container orchestration and volume mapping
└── Dockerfile              # Docker system image build specification
```

---

## 🔄 Workflow
<p align="center">
  <img src="https://github.com/user-attachments/assets/243446d3-1b55-42d2-b798-0c357f17f95c" width="100%" alt="Result Screenshot">
  <sub><em>▲ automated pipeline from image ingestion to the final diagnostic output and storage</em></sub>
</p>



---

## 📊 Result
<p align="center">
  <img src="https://github.com/user-attachments/assets/33c2f601-baca-4c56-a90d-875e91d07d11" width="100%" alt="Result Screenshot">
  <sub><em>▲ Real-time Side Profile Analysis calculating CVA (Craniovertebral Angle) with visual level indicators</em></sub>
</p>



---

## 🚀 Getting Started
### Prerequisites
* Docker and Docker Compose installed.
* Supported image files (JPG, PNG).

### Installation & Usage
1. Navigate to the project root directory.
2. Build and run the container:
   ```bash
   docker-compose up -d --build
   ```
3. Access the dashboard at **`http://localhost:8000`**.
4. Upload an image or select a file from the sidebar to view results.

---

© 2026 Seong-hun Bae.
