# SmartCut Studio

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-blue?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

> AI-assisted video editing with automatic scene detection, beat-synced transitions, and Whisper transcription.

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

## ⚠️ Known Issues

- Large video files may take time to process
- FFmpeg must be in system PATH
- Some video codecs may require additional encoding

## 📄 License

MIT License - see LICENSE file for details.

## 👤 Author

Amit Kumar

## 🙏 Acknowledgments

- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) - Scene detection
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) - Fast transcription
- [OpenCV](https://opencv.org/) - Computer vision

