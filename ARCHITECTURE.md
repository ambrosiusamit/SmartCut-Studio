# Architecture & System Design

## System Overview

SmartCut Studio is a full-stack web application that automates video editing through intelligent scene detection, beat analysis, and speech transcription.

```
✓ Frontend (Browser)
  ├─ Single Page Application
  ├─ HTML5 Video Preview
  └─ Interactive Timeline UI
      ↓
✓ Backend API (FastAPI)
  ├─ Async Request Handling
  ├─ File Management
  ├─ Job Queue Processing
  └─ Webhook Responses
      ↓
✓ Processing Engine
  ├─ Video Analysis (PySceneDetect)
  ├─ Audio Analysis (Beat Detection)
  ├─ Speech Recognition (Whisper)
  └─ Video Rendering (MoviePy/OpenCV)
      ↓
✓ Storage Layer
  └─ Files Directory (/store)
      ├─ Source Videos
      ├─ Thumbnails
      ├─ Metadata (JSON)
      ├─ Transcripts (SRT/TXT)
      └─ Rendered Videos
```

## Component Architecture

### Frontend Layer

**Technology**: HTML5, CSS3, JavaScript (Vanilla - No Framework)

**Responsibilities**:
- Video file upload handling
- API communication
- Results visualization
- User interaction management

**Key Files**:
- `index.html` - Structure & markup
- `style.css` - Responsive styling
- `script.js` - Event handlers & API calls

**Browser APIs Used**:
- `FormData` - Multipart upload
- `fetch()` - HTTP requests
- `Canvas` - Timeline rendering
- `Video` element - Playback preview
- `localStorage` - Session caching

### Backend Layer

**Technology**: Python 3.8+, FastAPI 0.100+

**Key Responsibilities**:
- HTTP endpoint management
- Request validation
- File upload processing
- Job orchestration
- Response formatting

**Core Endpoints**:
```
POST /analyze     → Process video file
POST /render      → Generate final video
```

**Middleware**:
- CORS enablement
- Request logging
- Error handling
- Session management

### Processing Engine

This is where the "intelligence" happens.

#### 1. Scene Detection

**Algorithm**: Content-based detection (color histogram analysis)

```python
from scenedetect import VideoManager, SceneManager, ContentDetector

detector = ContentDetector(threshold=27.0)
# threshold: 0-255 (lower = more sensitive)
# Tests each frame against previous frame
# Detects pixel color changes indicating scene breaks
```

**Output**:
```json
{
  "scenes": [
    {
      "index": 0,
      "start": 0.0,
      "end": 5.2,
      "duration": 5.2,
      "interesting_score": 0.75
    }
  ]
}
```

**Use Cases**:
- Multi-camera footage (cuts between cameras)
- Talking head videos (scene changes)
- Action sequences (fast cuts)

**Limitations**:
- Slow transitions (fades) may be missed
- Requires tuning for different content
- Computationally expensive on 4K video

#### 2. Beat Detection

**Algorithm**: Fast Fourier Transform (FFT) on audio

**Process**:
1. Extract audio from video
2. Compute frequency spectrum
3. Identify peaks in amplitude
4. Filter by tempo (BPM)

**Output**:
```json
{
  "beats": [0.0, 2.5, 5.0, 7.5, ...],
  "bpm": 120
}
```

**Use Cases**:
- Music videos
- Montages
- Rhythm-synced editing

#### 3. Transcription

**Algorithm**: Transformer-based speech recognition (Whisper)

**Engines**:
- `faster-whisper` (Optimized - RECOMMENDED)
- `openai-whisper` (Official reference)

**Models**: tiny → small → medium → large
- **tiny**: 39M params, fastest, lowest accuracy
- **large**: 1550M params, slowest, highest accuracy

**Output**:
```json
{
  "transcript": "Hello, this is a test video",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, this is a test video",
      "tokens": [...],
      "temperature": 0.0,
      "avg_logprob": -0.35
    }
  ]
}
```

**Supported Languages**: 95+ (auto-detect or specified)

#### 4. Video Rendering

**Algorithm**: Sequential frame processing with transitions

**Process**:
1. Load selected video clips
2. Extract frame range for each
3. Apply transitions (if crossfade)
4. Composite subtitles
5. Encode to H.264 MP4

**Libraries**:
- `MoviePy` - Composition & concatenation
- `OpenCV` - Frame manipulation
- `Pillow` - Text rendering
- `ffmpeg-python` - Encoding

**Transition Types**:

**Cut** (Frame-perfect):
```
Clip A [Frame N] → Clip B [Frame 1]
```

**Crossfade** (Smooth blend):
```
Clip A    [Frame N]
    ↓     (alpha blend over 1.0s)
Clip B [Frame 1]
```

### Storage Architecture

**Directory Structure**:
```
/store/
├── {video_id}_beats.json       → Beat timestamps
├── {video_id}_scenes.json      → Scene metadata
├── {video_id}_transcript.json  → Full transcript data
├── {video_id}.srt              → Subtitle file
├── {video_id}.txt              → Plain text transcript
└── {video_id}_edit.mp4         → Final rendered video
```

**File Naming**: Uses SHA256 hash of timestamp for uniqueness

**Lifecycle**:
1. Upload → stored temporarily
2. Processing → metadata generated
3. Download → video encoded & stored
4. Cleanup → old files deleted (manual)

## Data Flow

### Analyze Pipeline

```
User Upload
     ↓
Validate file (format, size)
     ↓
Generate video_id (hash)
     ↓
[Parallel Processing]
├─ Scene Detection → /store/{id}_scenes.json
├─ Beat Detection → /store/{id}_beats.json
└─ Transcription → /store/{id}.srt, .txt
     ↓
Generate Thumbnails → /store/{id}_thumb_*.jpg
     ↓
Return JSON Response with all metadata
```

### Render Pipeline

```
Render Request
     ↓
Validate selections (scenes exist)
     ↓
Load selected video clips
     ↓
Create transition composition
     ↓
Load transcript segments
     ↓
Render subtitle overlays
     ↓
Encode video
     ↓
Save to /store/{id}_edit.mp4
     ↓
Return download URL
```

## Performance Considerations

### Bottlenecks

| Operation | Duration | Bottleneck |
|-----------|----------|-----------|
| Scene Detection | 0.1x clip duration | CPU (video decode) |
| Beat Detection | Negligible | Audio extraction |
| Transcription | 0.25x-1x clip duration | GPU/CPU (model inference) |
| Video Rendering | 0.5x-2x clip duration | CPU (encoding) |
| **Total** | ~1-4x video length | Sequential processing |

### Optimization Strategies

**Parallel Processing**:
- Scene detection while reading video
- Transcription while rendering (separate server)

**Caching**:
- Store processed metadata
- Reuse thumbnails
- Cache decoded frames

**Resource Limits**:
- Limit concurrent uploads (queue)
- Memory limits for large videos
- Timeout jobs after 1 hour

## Security Considerations

### File Upload Security

```python
# Validate file extension
ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
if not file.filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
    raise ValueError("Invalid file type")

# Validate file size
MAX_SIZE = 1GB
if file.size > MAX_SIZE:
    raise ValueError("File too large")

# Validate file content (magic bytes)
import magic
mime = magic.from_buffer(file.read(1024), mime=True)
if 'video' not in mime:
    raise ValueError("Not a valid video file")
```

### API Security

```python
# CORS - Restrict to trusted domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
)

# Rate limiting (add to requirements)
# pip install slowapi
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/analyze")
@limiter.limit("5/minute")
async def analyze(file: UploadFile):
    pass
```

### File Access

- Files stored in isolated `/store/` directory
- No direct disk access from frontend
- URLs generated via API endpoints
- Temporary files auto-cleaned

## Scalability

### Current Limitations

- **Single-server deployment**: No job queue or workers
- **Memory-based**: Large videos require RAM
- **Synchronous processing**: Blocks API during processing
- **Local storage**: Files on single disk

### Scaling Strategies

#### For Small Scale (10-50 concurrent users)

```
Current Setup:
┌─────────────┐
│ FastAPI App │ (video processing)
│ (all-in-one)│
└─────────────┘
```

**Changes**: Add load balancer, run multiple processes

#### For Medium Scale (50-1000 users)

```
Proposed:
┌──────────────────┐
│ Load Balancer    │ (nginx)
└────────┬─────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌─────────┐ ┌─────────┐
│FastAPI  │ │FastAPI  │ (API servers)
│(no jobs)│ │(no jobs)│
└────┬────┘ └────┬────┘
     │           │
     └─────┬─────┘
           ↓
   ┌──────────────────┐
   │ Redis Job Queue  │ (Celery)
   └──────────────────┘
           ↑
   ┌──────────────────┐
   │ Worker Processes │ (Processing)
   │ (parallel tasks) │
   └──────────────────┘
           ↑
   ┌──────────────────┐
   │ Object Storage   │ (S3/GCS)
   │ (cloud files)    │
   └──────────────────┘
```

**Implementation**: Add task queue (Celery + Redis)

## Deployment

### Development

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 5200
```

### Production

```bash
# Use gunicorn + uvicorn workers
pip install gunicorn
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5200
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY smartcut-backend/ .
EXPOSE 5200

CMD ["python", "app.py"]
```

## Technology Rationale

| Choice | Reason |
|--------|--------|
| **FastAPI** | Modern, fast, auto-docs, async support |
| **PySceneDetect** | Specialized scene detection library |
| **MoviePy** | Pure Python video composition |
| **Whisper** | SOTA speech recognition, 95+ languages |
| **Vanilla JS** | No dependencies, lightweight frontend |
| **SQLite** (optional) | Persistence without external DB |

---

**Version**: 1.0  
**Last Updated**: March 2026
