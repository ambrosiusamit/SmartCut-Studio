
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

## 🏗️ Architecture

```
SmartCut Studio/
├── smartcut-backend/          # FastAPI backend
│   ├── app.py                 # Main application (~600 lines)
│   ├── store/                 # Output: rendered videos, thumbnails, transcripts
│   └── storage/               # Temporary processing files
│
├── smartcut-frontend/         # HTML5 frontend
│   ├── index.html             # User interface
│   ├── style.css              # Styling
│   └── script.js              # API integration
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Video Processing | OpenCV, MoviePy, PySceneDetect |
| Transcription | Faster Whisper / OpenAI Whisper |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

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
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **Windows**: `winget install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

### Running the Application

1. **Start the backend**
   ```bash
   cd smartcut-backend
   python app.py
   ```
   API available at `http://localhost:5200`

2. **Open the frontend**
   - Open `smartcut-frontend/index.html` in browser
   - Or visit `http://localhost:5200/docs` for interactive API docs

## 📡 API Endpoints

### POST /analyze
Analyzes video and detects scenes, beats, and optionally transcribes audio.

**Request:**
- `file`: Video file (multipart/form-data)
- `transcribe`: "true" or "false"
- `language`: Language hint (e.g., "en")

**Response:**
```json
{
  "video_id": "abc123",
  "scenes": [{"index": 0, "start": 0.0, "end": 5.2, "duration": 5.2, "thumb": "/store/abc123_thumb_0.jpg"}],
  "beats": [0.0, 2.5, 5.0, 7.5],
  "transcript": {"srt_url": "/store/abc123.srt", "txt_url": "/store/abc123.txt"}
}
```

### POST /render
Renders video from selected scenes.

**Request:**
```json
{
  "video_id": "abc123",
  "selections": [0, 1, 2],
  "transition": "cut" | "crossfade",
  "transition_sec": 1.0,
  "align_to_beats": true,
  "subtitles": true
}
```

**Response:**
```json
{
  "download_url": "/store/abc123_edit.mp4",
  "duration": 18.2,
  "status": "success"
}
```

## 💻 Development

### Running in Development Mode
```bash
cd smartcut-backend
python -m uvicorn app:app --reload --port 5200
```

### Optional: Enable Transcription
```bash
pip install faster-whisper  # Recommended - faster
# OR
pip install openai-whisper
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

Amit Kumar

## 🔮 Future Improvements

- [ ] Add user authentication
- [ ] Implement job queue for background processing
- [ ] Add real-time progress WebSocket updates
- [ ] Cloud storage integration (S3/GCS)
- [ ] Docker containerization
- [ ] Unit tests with pytest
- [ ] Video filters and effects
- [ ] Multi-language subtitle support

