# Development Guide

Instructions for developers wanting to contribute to or extend SmartCut Studio.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Adding Features](#adding-features)
- [Testing](#testing)
- [Debugging](#debugging)
- [Building & Deployment](#building--deployment)
- [Contributing](#contributing)

---

## Prerequisites

- **Python**: 3.8 or newer
- **Git**: For version control
- **FFmpeg**: System dependency
- **Node.js** (optional): For frontend tooling

### System Setup

#### Windows

```powershell
# Install Python 3.9+
winget install Python.Python.3.11

# Install FFmpeg
winget install ffmpeg

# Verify installations
python --version
ffmpeg -version
```

#### macOS

```bash
# Install Python 3.9+ (via Homebrew)
brew install python@3.11

# Install FFmpeg
brew install ffmpeg

# Verify
python3 --version
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

```bash
# Python usually pre-installed, ensure 3.8+
python3 --version

# Install FFmpeg
sudo apt-get update
sudo apt-get install ffmpeg

# Verify
ffmpeg -version
```

---

## Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Base dependencies
pip install -r requirements.txt

# Optional: Development tools
pip install pytest black flake8 pylint mypy

# Optional: Transcription support
pip install faster-whisper  # Recommended
# OR
pip install openai-whisper
```

### 4. Run Application

```bash
cd smartcut-backend

# Development mode (auto-reload on changes)
python -m uvicorn app:app --reload --host 0.0.0.0 --port 5200

# Or directly
python app.py
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:5200
INFO:     Application startup complete
```

Open browser to `http://localhost:5200` (or open `smartcut-frontend/index.html` directly)

---

## Project Structure

### Backend Structure

```
smartcut-backend/
├── app.py                 # Main application (only file)
│
├── store/                 # Output directory
│   ├── *.mp4             # Rendered videos
│   ├── *.jpg             # Thumbnails
│   ├── *.json            # Metadata
│   └── *.srt             # Subtitles
│
└── storage/              # Temporary files
    ├── models/           # Downloaded ML models
    └── thumbs/           # Processing temp files
```

### Frontend Structure

```
smartcut-frontend/
│
├── index.html            # Markup & page structure
├── style.css             # Styling (no frameworks)
└── script.js             # Event handlers & API calls
```

### File Organization

**All functionality in single file**: `app.py` (~600 lines)

**Sections**:
1. Imports & Config (lines 1-50)
2. Main app initialization (lines 50-75)
3. Scene detection functions (lines 100-200)
4. Beat detection (lines 200-250)
5. Transcription (lines 250-350)
6. Video rendering (lines 350-500)
7. API routes (lines 500-600)

---

## Code Style

### Python

Follow **PEP 8** standards:

```bash
# Auto-format code
black app.py

# Check for style issues
flake8 app.py

# Type checking (optional)
mypy app.py
```

**Style Guidelines**:

```python
# ✓ Good
def analyze_video(video_path: str, threshold: float = 27.0) -> dict:
    """Analyze video and detect scenes.
    
    Args:
        video_path: Path to video file
        threshold: Scene detection threshold (0-255)
        
    Returns:
        Dictionary with scenes, beats, duration
    """
    pass

# ✗ Avoid
def analyzeVideo(videoPath, th=27.0):
    pass
```

**Naming Conventions**:
- Functions: `snake_case` ✓
- Classes: `PascalCase` ✓
- Constants: `UPPER_SNAKE_CASE` ✓
- Private: prefix `_` (e.g., `_internal_function`)

### JavaScript

```javascript
// ✓ Good
const analyzeVideo = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });
    
    return response.json();
};

// ✗ Avoid inline long lines
const x = async (f) => { const fd = new FormData(); fd.append('file', f); return fetch('/analyze', {method: 'POST', body: fd}).then(r => r.json()); };
```

### Comments

```python
# Comment what (not how)

# ✓ Good
# Lower threshold → more sensitive scene detection
threshold = 27.0

# ✗ Over-commenting
threshold = 27.0  # Set threshold to 27
# Create VideoManager object
manager = VideoManager(video_path)
```

---

## Adding Features

### Example: Add New API Endpoint

**Goal**: Add `/status` endpoint that returns server health

**Steps**:

1. **Add to app.py** (after imports):

```python
from datetime import datetime
import psutil

# Add endpoint (around line 580)
@app.get("/status")
async def get_status():
    """Server health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - _START_TIME,
        "memory_usage_mb": psutil.Process().memory_info().rss / 1024 / 1024
    }
```

2. **Test your endpoint**:

```bash
curl http://localhost:5200/status
```

**Expected output**:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-05T10:30:00.123456",
  "uptime": 3600.5,
  "memory_usage_mb": 125.4
}
```

3. **Update documentation**: Add to [API.md](API.md)

### Example: Improve Scene Detection

**Goal**: Make scene detection more tunable

**Current**: Fixed threshold of 27.0

**Changes**:

```python
# Add parameter to /analyze endpoint
@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    transcribe: str = Form("false"),
    language: str = Form("en"),
    scene_threshold: float = Form(27.0)  # NEW
):
    """Analyze video with tunable scene detection"""
    
    # Validate threshold
    if not 0 <= scene_threshold <= 255:
        raise HTTPException(400, "scene_threshold must be 0-255")
    
    # Use in detection
    detector = ContentDetector(threshold=scene_threshold)
    ...
```

**Frontend update** (`script.js`):

```javascript
// In analyze function
const formData = new FormData();
formData.append('file', videoFile);
formData.append('transcribe', true);
formData.append('scene_threshold', 
    document.getElementById('thresholdSlider').value);

await fetch('/analyze', {
    method: 'POST',
    body: formData
});
```

**HTML update** (`index.html`):

```html
<label>Scene Detection Sensitivity:</label>
<input 
    type="range" 
    id="thresholdSlider" 
    min="0" 
    max="100" 
    value="50"
>
<span id="thresholdValue">50</span>
```

### Example: Add Database Support

**Goal**: Persist video metadata to SQLite (instead of storing only in memory)

**Setup**:

```bash
pip install sqlalchemy
```

**Code**:

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
engine = create_engine('sqlite:///./smartcut.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define model
class VideoAnalysis(Base):
    __tablename__ = "videos"
    
    video_id = Column(String, primary_key=True)
    filename = Column(String)
    duration = Column(Float)
    scene_count = Column(int)
    created_at = Column(DateTime, default=datetime.now)
    metadata_path = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Use in analyze endpoint
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # ... existing analysis code ...
    
    # Store in database
    db = SessionLocal()
    record = VideoAnalysis(
        video_id=video_id,
        filename=file.filename,
        duration=duration,
        scene_count=len(scenes),
        metadata_path=metadata_file
    )
    db.add(record)
    db.commit()
    
    return result
```

---

## Testing

### Unit Testing

```bash
pip install pytest
```

**Create** `test_app.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_analyze_endpoint_exists():
    """Test endpoint is registered"""
    # This should not 404
    assert True  # Placeholder

def test_invalid_file_format():
    """Test rejection of invalid file"""
    files = {'file': ('test.txt', b'not a video')}
    response = client.post("/analyze", files=files)
    assert response.status_code == 400

def test_render_requires_video_id():
    """Test render validation"""
    response = client.post("/render", json={
        'selections': [0, 1]
        # Missing video_id
    })
    assert response.status_code == 422

def test_scene_detection_algorithm():
    """Test scene detection returns sensible results"""
    # Would need a test video
    pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Run tests**:

```bash
pytest test_app.py -v
```

### Manual Testing

**Test video creation** (10 seconds of black):

```bash
ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=10 -f lavfi -i sine=f=440:d=10 test.mp4
```

**Upload and analyze**:

```bash
curl -XPOST \
  -F "file=@test.mp4" \
  -F "transcribe=false" \
  http://localhost:5200/analyze | jq .
```

---

## Debugging

### Enable Debug Logging

**In app.py**:

```python
import logging

# Add before FastAPI init
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In functions
logger.info(f"Processing video: {video_id}")
logger.debug(f"Scene threshold: {threshold}")
logger.error(f"FFmpeg failed: {error}")
```

**Run with logging**:

```bash
python app.py 2>&1 | tee debug.log
```

### Debugging in VS Code

**Create** `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app:app", "--reload"],
            "jinja": true,
            "justMyCode": true,
            "cwd": "${workspaceFolder}/smartcut-backend"
        }
    ]
}
```

**Start debugging**: Press F5

### Browser DevTools

**Frontend debugging**:
1. Open browser to `http://localhost:5200`
2. Press F12 → Console
3. Check for JavaScript errors
4. Network tab → watch API calls

**Check network requests**:
```javascript
// In browser console
fetch('http://localhost:5200/status').then(r => r.json()).then(console.log)
```

### Common Bugs & Solutions

| Issue | Debug Steps |
|-------|-----------|
| Video won't upload | Check file size, format; check browser console |
| Scene detection returns 0 scenes | Lower threshold; verify video has content changes |
| API times out | Large video; long transcription; check CPU usage |
| Subtitles missing | Check fonts installed; verify transcript exists |
| Memory leaks | Monitor with `psutil`; check for unclosed files |

---

## Building & Deployment

### Local Build

```bash
# Create distribution
pip install build
python -m build
```

### Docker Deployment

**Create** `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY smartcut-backend/ ./smartcut-backend/
COPY smartcut-frontend/ ./smartcut-frontend/
WORKDIR /app/smartcut-backend

# Run
EXPOSE 5200
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5200"]
```

**Build and run**:

```bash
docker build -t smartcut-studio .
docker run -p 5200:5200 -v $(pwd)/store:/app/smartcut-backend/store smartcut-studio
```

### Production Deployment

**Use gunicorn** (production ASGI server):

```bash
pip install gunicorn

cd smartcut-backend
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5200 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
```

### Nginx Reverse Proxy

**nginx config**:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
    }

    location /store {
        alias /path/to/smartcut-backend/store;
    }
}
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

**Quick reference**:

1. Fork repo
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes following code style above
4. Run tests: `pytest`
5. Commit: `git commit -m "Add: my feature"`
6. Push: `git push origin feature/my-feature`
7. Open Pull Request

---

**Happy coding! 🚀**

For questions, open an issue on GitHub.
