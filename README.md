# SmartCut Studio

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-ambrosiusamit-black?style=flat-square&logo=github)](https://github.com/ambrosiusamit)

**Intelligent Video Editing Automation**

Turn hours of manual editing into minutes with AI-powered scene detection, beat alignment, and auto-transcription.

[Quick Start](#-quick-start) • [Features](#-features) • [API](#-api) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 🎯 About

SmartCut Studio automates the boring parts of video editing. Upload a video, and the AI:
- **Detects scene cuts** using content analysis
- **Finds beat points** in audio for rhythm-synced edits  
- **Transcribes speech** and generates subtitles
- **Renders your edit** with chosen transitions

Built as a **student portfolio project** to demonstrate full-stack development: multimedia processing, REST APIs, and seamless backend-frontend integration.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **Scene Detection** | Automatically identifies scene cuts and transitions |
| 🎵 **Beat-Synced Editing** | Align video cuts to music beats for dynamic montages |
| 📝 **Auto-Transcription** | Whisper-powered speech-to-text with SRT subtitles |
| ✂️ **Flexible Transitions** | Frame-perfect cuts or smooth crossfades |
| 🌐 **REST API** | Simple, clean endpoints for programmatic use |
| 🎨 **Demo UI** | Zero-config browser interface included |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **FFmpeg** (system dependency)
- **~5 minutes** of your time

### Setup (5 Steps)

```bash
# 1️⃣ Clone
git clone https://github.com/ambrosiusamit/SmartCut-Studio.git
cd SmartCut-Studio

# 2️⃣ Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3️⃣ Dependencies
pip install -r requirements.txt

# 4️⃣ Install FFmpeg
# Windows: winget install ffmpeg
# macOS:   brew install ffmpeg
# Linux:   sudo apt install ffmpeg

# 5️⃣ Run
cd smartcut-backend && python app.py
```

**That's it!** Open `http://localhost:5200` in your browser.

---

## 📡 API Reference

### Upload & Analyze
```bash
curl -F "file=@video.mp4" \
     -F "transcribe=true" \
     http://localhost:5200/analyze
```

**Response:**
```json
{
  "video_id": "a590a3f3",
  "scenes": [
    {"index": 0, "start": 0.0, "end": 5.2, "duration": 5.2},
    {"index": 1, "start": 5.2, "end": 12.8, "duration": 7.6}
  ],
  "beats": [0.0, 2.5, 5.0, 7.5, 10.0, 12.5],
  "transcript": {
    "srt_url": "/store/a590a3f3.srt",
    "segments": [{"text": "Hello world...", "start": 0.0, "end": 2.5}]
  }
}
```

### Render Edited Video
```bash
curl -X POST http://localhost:5200/render \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "a590a3f3",
    "selections": [0, 1],
    "transition": "crossfade",
    "transition_sec": 1.0,
    "subtitles": true
  }'
```

**Response:**
```json
{
  "download_url": "/store/a590a3f3_edit.mp4",
  "duration": 13.0,
  "status": "success"
}
```

> 💡 See inline comments in `smartcut-backend/app.py` for implementation details.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Browser)              │
│  HTML/CSS/JS - Simple upload/download   │
└──────────────┬──────────────────────────┘
               │ fetch() calls
               ▼
┌─────────────────────────────────────────┐
│      Backend (FastAPI @ :5200)          │
│  ┌──────────────────────────────────┐   │
│  │ POST /analyze → process video    │   │
│  │ POST /render → generate output   │   │
│  └──────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┬───────────┐
      ▼                 ▼           ▼
  ┌────────┐      ┌─────────┐  ┌────────┐
  │ Scene  │      │  Beat   │  │Whisper │
  │Detect  │      │Analysis │  │  ASR   │
  └────────┘      └─────────┘  └────────┘
      │                 │           │
      └────────────┬────┴───────────┘
                   ▼
          ┌─────────────────────┐
          │  MoviePy Rendering  │
          │  (MP4 output)       │
          └─────────────────────┘
```

### Directory Structure
```
SmartCut-Studio/
├── smartcut-backend/
│   ├── app.py              # ~600 lines | All logic here
│   └── store/              # Output videos (gitignored)
├── smartcut-frontend/
│   ├── index.html          # UI markup
│   ├── script.js           # API integration
│   └── style.css           # Styling
├── requirements.txt        # Dependencies
├── README.md              # This file
└── LICENSE                # MIT
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI, Python 3.8+ | REST API & video processing |
| **Video** | OpenCV, MoviePy, FFmpeg | Frame extraction & composition |
| **Analysis** | PySceneDetect | Scene boundary detection |
| **Audio** | Librosa, Whisper | Beat detection & transcription |
| **Frontend** | HTML5, CSS3, Vanilla JS | User interface (no frameworks) |

---

## 📚 Usage Examples

### Python Client
```python
import requests

# Upload and analyze
with open('video.mp4', 'rb') as f:
    resp = requests.post(
        'http://localhost:5200/analyze',
        files={'file': f},
        data={'transcribe': 'true', 'language': 'en'}
    )
    video_id = resp.json()['video_id']
    print(f"Found {len(resp.json()['scenes'])} scenes")

# Render edit
render = requests.post(
    'http://localhost:5200/render',
    json={
        'video_id': video_id,
        'selections': [0, 1, 2],
        'transition': 'crossfade',
        'transition_sec': 0.5
    }
)
print(f"Download: {render.json()['download_url']}")
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', videoFile);
formData.append('transcribe', 'true');

const result = await fetch('http://localhost:5200/analyze', {
    method: 'POST',
    body: formData
}).then(r => r.json());

console.log(`${result.scenes.length} scenes detected`);
```

---

## 🚧 Roadmap

- [ ] User authentication & per-user storage
- [ ] Background job queue for long videos
- [ ] WebSocket progress updates
- [ ] Docker & cloud deployment
- [ ] Additional filters (blur, color, effects)
- [ ] React/Vue frontend upgrade
- [ ] Comprehensive test suite
- [ ] Cloud storage integration (S3/GCS)

---

## 🤝 Contributing

Pull requests welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -m "add: cool feature"`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Amit Kumar**
- GitHub: [@ambrosiusamit](https://github.com/ambrosiusamit)


---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) — Scene detection
- [MoviePy](https://zulko.github.io/moviepy/) — Video composition
- [Whisper](https://github.com/openai/whisper) — Speech recognition
- [OpenCV](https://opencv.org/) — Computer vision

---

<div align="center">



[⬆ Back to top](#smartcut-studio)

</div>
