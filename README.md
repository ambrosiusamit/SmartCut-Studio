# SmartCut Studio

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-blue?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

> **Intelligent video editing automation** - Detect scenes, align cuts to music beats, and auto-transcribe speech. Powered by AI for professional-quality edits in minutes.

A full-stack application that combines computer vision, audio analysis, and machine learning to automate video editing workflows. Perfect for content creators, video editors, and automation enthusiasts.

**Table of Contents:** [Features](#-features) • [Quick Start](#-quick-start) • [API](#-api-endpoints) • [Configuration](#%EF%B8%8F-configuration) • [Architecture](#-architecture) • [Development](#-development) • [Troubleshooting](#-troubleshooting) • [Documentation](#-documentation)

## ✨ Features

- **Automatic Scene Detection** - Uses PySceneDetect to find scene boundaries
- **Beat-Synced Transitions** - Align cuts to audio beats for dynamic editing
- **Whisper Transcription** - Automatic speech-to-text with SRT/subtitle support
- **Smart Subtitle Rendering** - Auto-wrapped subtitles with customizable styling
- **Multiple Transition Types** - Straight cuts or crossfade transitions
- **RESTful API** - Built with FastAPI for easy integration
- **CORS Enabled** - Works with any frontend framework

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (required for video processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ambrosiusamit/smartcut-studio.git
   cd smartcut-studio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** (required)
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

### Running the Application

1. **Start the backend server**
   ```bash
   cd smartcut-backend
   python app.py
   ```
   The API will be available at `http://localhost:5200`

2. **Open the frontend**
   - Option 1: Open `smartcut-frontend/index.html` in your browser
   - Option 2: Serve via FastAPI static files (add route in app.py)

## 📡 API Endpoints

### POST /analyze
Analyzes a video file and detects scenes, beats, and optionally transcribes audio.

**Request:**
- `file`: Video file (multipart/form-data)
- `transcribe`: "true" or "false" - enable Whisper transcription
- `language`: Language hint (e.g., "en", "es")

**Response:**
```json
{
  "video_id": "abc123",
  "scenes": [
    {
      "index": 0,
      "start": 0.0,
      "end": 5.2,
      "duration": 5.2,
      "thumb": "/store/abc123_scene0.jpg",
      "interesting_score": 0.75
    }
  ],
  "beats": [0.0, 2.5, 5.0, 7.5],
  "transcript": {
    "srt_url": "/store/abc123.srt",
    "txt_url": "/store/abc123.txt",
    "segments": [...]
  }
}
```

### POST /render
Renders a video from selected scenes.

**Request:**
- `video_id`: ID from analyze response
- `selections`: JSON array of scene indices to include
- `transition`: "cut" or "crossfade"
- `transition_sec`: Crossfade duration in seconds
- `align_to_beats`: "true" or "false"
- `subtitles`: "true" or "false"

**Response:**
```json
{
  "download_url": "/store/abc123_edit.mp4"
}
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Video Processing | OpenCV, MoviePy, PySceneDetect |
| Transcription | Faster Whisper / OpenAI Whisper |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| API | RESTful JSON |

## 📁 Project Structure

```
smartcut-studio/
├── smartcut-backend/
│   ├── app.py              # Main FastAPI application
│   ├── store/              # Uploaded videos and rendered outputs
│   └── storage/            # Temporary processing files
├── smartcut-frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── script.js           # Frontend JavaScript
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Optional: Whisper Transcription

To enable Whisper transcription:

```bash
# Option 1: Faster Whisper (recommended, faster)
pip install faster-whisper

# Option 2: OpenAI Whisper
pip install openai-whisper
```

Then check the transcription checkbox in the UI or set `transcribe=true` in the API call.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in `smartcut-backend/` if needed:

```bash
# Server
HOST=0.0.0.0
PORT=5200
RELOAD=true

# File Storage
STORE_DIR=./store
MAX_FILE_SIZE=1000000000  # 1GB in bytes

# Scene Detection
SCENE_THRESHOLD=27.0  # Lower = more sensitive

# Processing
NUM_WORKERS=4
TIMEOUT_SECONDS=3600  # 1 hour
```

### Scene Detection Parameters

Edit `app.py` to adjust scene detection sensitivity:

```python
# Threshold in 0-255 range (lower = more sensitive)
detector = ContentDetector(threshold=27.0)
```

### Transcription Configuration

The app autodetects the best transcription engine (Faster Whisper > OpenAI Whisper).

- **Languages supported**: English, Spanish, French, German, Chinese, and 95+ more via Whisper
- **Whisper models**: tiny, base, small, medium, large

## 🏗️ Architecture

### How It Works

```
1. User uploads video
   ↓
2. Backend analyzes:
   ├─ Scene detection (PySceneDetect)
   ├─ Audio beat detection
   └─ Transcription (Whisper)
   ↓
3. Frontend displays results:
   ├─ Scene thumbnails
   ├─ Beat timeline
   └─ Transcript with timestamps
   ↓
4. User selects scenes and transition style
   ↓
5. Backend renders final video:
   ├─ Concatenates selected clips
   ├─ Adds transitions & effects
   ├─ Overlays subtitles
   └─ Exports MP4
   ↓
6. User downloads rendered video
```

### Data Flow Diagram

```
┌─────────────────┐
│  Frontend (UI)  │
│ HTML/CSS/JS     │
└────────┬────────┘
         │ (API calls)
         ↓
┌─────────────────────────────┐
│  Backend (FastAPI)          │
│  - Express API              │
│  - Handle uploads           │
│  - Manage processing queue  │
└────────┬────────┬────────────┘
         │        │
         ↓        ↓
    ┌────────────────────┐
    │  Processing        │
    │  - Scene Detect    │
    │  - Beat Analysis   │
    │  - Transcription   │
    │  - Rendering       │
    └────────┬───────────┘
             │
             ↓
    ┌────────────────────┐
    │  Storage           │
    │  /store/ directory │
    │  - Videos          │
    │  - Thumbnails      │
    │  - Transcripts     │
    └────────────────────┘
```

## 💻 Development

### Project Structure Details

```
smartcut-backend/
├── app.py                 # Main application (600+ lines)
│   ├── API Routes:
│   │   ├── POST /analyze      (video upload & processing)
│   │   └── POST /render       (final video export)
│   ├── Core Functions:
│   │   ├── detect_scenes()
│   │   ├── detect_beats()
│   │   ├── transcribe_audio()
│   │   ├── add_subtitles()
│   │   └── render_video()
│   └── Utilities:
│       ├── File management
│       └── Error handling
│
├── store/                 # Output directory (gitignored)
│   ├── *_beats.json      (beat timestamps)
│   ├── *_scenes.json     (scene metadata)
│   ├── *.srt             (subtitle files)
│   ├── *.mp4             (rendered videos)
│   └── *.jpg             (thumbnails)
│
└── storage/              # Temporary processing files

smartcut-frontend/
├── index.html            # Single-page application
│   └── Structure:
│       ├── Video upload form
│       ├── Analysis results display
│       ├── Scene selector
│       ├── Transition settings
│       └── Download preview
│
├── script.js             # Frontend logic (~400 lines)
│   └── Features:
│       ├── API communication
│       ├── UI state management
│       ├── Timeline visualization
│       └── Download handling
│
└── style.css             # Responsive design
    └── Layout:
        ├── Mobile-friendly
        ├── Dark/light themes
        └── Smooth animations
```

### Code Walkthrough

**Key Function: Scene Detection**
```python
def detect_scenes(video_path, threshold=27.0):
    """Find scene boundaries using content analysis"""
    video = VideoManager(video_path)
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video)
    return manager.get_cut_list(video.get_fps())
```

**Key Function: Video Rendering**
```python
def render_video(video_id, selections, transition, transition_sec):
    """Concatenate selected scenes with transitions"""
    clips = [VideoFileClip(scene_path) for scene_path in selection_paths]
    
    if transition == "crossfade":
        final = concatenate_videoclips(clips, method="compose", 
                                       transition=transition)
    else:
        final = concatenate_videoclips(clips)
    
    final.write_videofile(output_path)
```

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Optional: for linting/testing

# Start development server with hot reload
cd smartcut-backend
python -m uvicorn app:app --reload --port 5200
```

### Testing Your Changes

```bash
# Test scene detection
curl -XPOST -F "file=@test_video.mp4" -F "transcribe=false" \
  http://localhost:5200/analyze

# Test rendering
curl -XPOST -H "Content-Type: application/json" \
  -d '{
    "video_id": "test_id",
    "selections": [0, 1, 2],
    "transition": "cut"
  }' \
  http://localhost:5200/render
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### ❌ "FFmpeg not found" Error

**Problem**: FastAPI can't locate FFmpeg executable

**Solutions**:
- **Windows**: 
  - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - Add to PATH: `setx PATH "%PATH%;C:\ffmpeg\bin"`
  - Restart terminal and Python
  
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

**Test**: Run `ffmpeg -version` in terminal

#### ❌ "No module named 'scenedetect'"

**Problem**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

#### ❌ Video Processing Takes Too Long

**Problem**: Scene detection or transcription is slow

**Solutions**:
- Increase `SCENE_THRESHOLD` (less sensitive detection)
- Use `smaller` Whisper model: `faster_whisper.WhisperModel(size="tiny")`
- Process shorter videos for testing
- Check available RAM: `import psutil; psutil.virtual_memory()`

#### ❌ "Codec Issues" - Video Won't Export

**Problem**: Unsupported codec or format

**Solutions**:
```bash
# Convert video to H.264 MP4 first
ffmpeg -i input.mov -vcodec h264 -acodec aac output.mp4

# Then process with SmartCut
```

**Supported formats**: MP4, MOV, AVI, MKV, WebM

#### ❌ Subtitle Rendering Issues

**Problem**: Text overlays missing or incorrect

**Check**:
- Font file exists in system
- Text encoding is UTF-8
- Video resolution is 1080p or higher for clarity

#### ❌ Large File Upload Fails

**Problem**: File size exceeds server limit

**Solutions**:
```python
# Increase in app.py
app = FastAPI(...)  # Max: usually limited by OS/nginx configs
```

- Or compress video: `ffmpeg -i input.mp4 -crf 28 output.mp4`

### Getting Help

- **Check logs**: Backend prints detailed errors to console
- **Browser console**: Press F12 to see frontend errors
- **API responses**: Include error details in JSON responses
- **File permissions**: Ensure write access to `./store/` directory

### Performance Tips

| Operation | Optimization |
|-----------|-------------|
| Scene detection | Lower threshold; shorter videos |
| Transcription | Use Faster Whisper + tiny/base model |
| Video rendering | Reduce resolution; shorter clips |
| Storage | Clean `/store/` regularly; delete old files |

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PySceneDetect Guide](https://www.scenedetect.com/)
- [MoviePy Docs](https://zulko.github.io/moviepy/)
- [Whisper GitHub](https://github.com/openai/whisper)
- [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html)

## � Documentation

Complete documentation is organized by purpose:

### Getting Started

| Document | Purpose | Audience |
|----------|---------|----------|
| [QUICK_START.md](QUICK_START.md) | **5-minute setup** | Everyone |
| [INSTALLATION.md](INSTALLATION.md) | Step-by-step install for each OS | First-time users |

### Using SmartCut Studio

| Document | Purpose | Audience |
|----------|---------|----------|
| [API.md](API.md) | REST API reference with examples | Developers integrating the API |
| README.md (this file) | Feature overview & quick start | Everyone |

### Technical Deep Dives

| Document | Purpose | Audience |
|----------|---------|----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, data flow, tech stack | Developers, architects |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributing, extending, testing | Contributors |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Code of conduct, PR guidelines | Contributors |

### Quick Reference

**I want to...**
- 🚀 Get started immediately → [QUICK_START.md](QUICK_START.md)
- 📦 Install properly on my OS → [INSTALLATION.md](INSTALLATION.md)
- 🔌 Use the API → [API.md](API.md)
- 🏗️ Understand the system → [ARCHITECTURE.md](ARCHITECTURE.md)
- 💻 Add features / contribute → [DEVELOPMENT.md](DEVELOPMENT.md)
- 🆘 Fix problems → [Troubleshooting](#-troubleshooting) section above

---

## �📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Amit Kumar**  
[GitHub](https://github.com/ambrosiusamit) • [LinkedIn](https://linkedin.com/in/ambrosiusamit)

## 🙏 Acknowledgments

- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) - Scene detection
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) - Fast transcription
- [OpenCV](https://opencv.org/) - Computer vision
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

---

**Last Updated**: March 2026  
**Status**: Active Development  
**Contributions**: Welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

