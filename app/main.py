import cv2
import os
import numpy as np
import time
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from core.analyzer_front import FrontAnalyzer
from core.analyzer_side import SideAnalyzer

app = FastAPI(title="Docker-Pose-Analyzer")

templates = Jinja2Templates(directory="templates")

current_mode = "front"
analyzers = {
    "front": FrontAnalyzer(),
    "side": SideAnalyzer()
}

# 로컬 서버 디렉토리 경로
IMAGE_DIR = "/data/images"
OUTPUT_DIR = "/outputs"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"mode": current_mode})

@app.post("/set_mode/{mode}")
async def set_mode(mode: str):
    global current_mode
    if mode in analyzers:
        current_mode = mode
        return {"status": "success", "mode": current_mode}
    return {"status": "error", "message": "Invalid mode"}

@app.get("/list_images")
async def list_images():
    """/data/images 폴더에 있는 이미지 목록 반환"""
    if not os.path.exists(IMAGE_DIR):
        return JSONResponse(content={"images": []})
        
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)]
    return JSONResponse(content={"images": sorted(files)})

def process_and_save_frame(frame, use_mode, output_filename=None):
    """프레임을 분석하고 지정된 이름으로 outputs 폴더에 저장합니다."""
    analyzer = analyzers.get(use_mode)
    if analyzer:
        frame = analyzer.process(frame)
        
    if output_filename:
        out_path = os.path.join(OUTPUT_DIR, output_filename)
        cv2.imwrite(out_path, frame)
        
    ret, buffer = cv2.imencode('.jpg', frame)
    return ret, buffer

@app.post("/analyze_server_image/{filename}")
async def analyze_server_image(filename: str, mode: str = Form(None)):
    """서버(/data/images)에 있는 파일을 읽어서 분석하고 결과를 반환 및 저장합니다."""
    global current_mode
    use_mode = mode if mode else current_mode
    
    file_path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(file_path):
        return Response(status_code=404, content="File not found")
        
    frame = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if frame is None:
        return Response(status_code=400, content="Invalid image file")
        
    # 출력 파일 이름은 원본 이름에 _result를 붙여서 저장
    name, ext = os.path.splitext(filename)
    out_name = f"{name}_result{ext}"
    
    ret, buffer = process_and_save_frame(frame, use_mode, out_name)
    if not ret:
        return Response(status_code=500, content="Failed to encode image")
        
    return Response(content=buffer.tobytes(), media_type="image/jpeg")

@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...), mode: str = Form(None)):
    """웹 브라우저에서 직접 업로드된 파일을 분석합니다."""
    global current_mode
    use_mode = mode if mode else current_mode
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return Response(status_code=400, content="Invalid image file")
        
    # 업로드된 파일도 outputs에 저장
    timestamp = int(time.time())
    out_name = f"uploaded_{timestamp}.jpg"
    
    ret, buffer = process_and_save_frame(frame, use_mode, out_name)
    if not ret:
        return Response(status_code=500, content="Failed to encode image")
        
    return Response(content=buffer.tobytes(), media_type="image/jpeg")
