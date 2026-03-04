# Quick Start Guide

Get SmartCut Studio running in 5 minutes.

## 30-Second Setup

```bash
# 1. Clone
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio

# 2. Install Python dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Install FFmpeg
# Windows: winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg

# 4. Run
cd smartcut-backend
python app.py

# 5. Open browser to http://localhost:5200
```

---

## Your First Video

1. **Open** `http://localhost:5200` in browser
2. **Upload** any MP4, MOV, or AVI video
3. **Click** "Analyze"
4. **Wait** 1-3 minutes for processing
5. **See** detected scenes, beats, transcript
6. **Select** scenes you want
7. **Click** "Render"
8. **Download** your edited video

---

## Common Commands

```bash
# Activate environment
source venv/bin/activate         # Unix
venv\Scripts\activate            # Windows

# Install transcription (optional)
pip install faster-whisper

# Run with auto-reload (development)
python -m uvicorn app:app --reload

# Deactivate environment
deactivate
```

---

## Quick API Test

```bash
# Test upload and analyze
curl -F "file=@video.mp4" http://localhost:5200/analyze

# Test rendering
curl -X POST http://localhost:5200/render \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "YOUR_ID_HERE",
    "selections": [0, 1, 2],
    "transition": "cut"
  }'
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from python.org, add to PATH |
| "FFmpeg not found" | `winget install ffmpeg` (Windows) or `brew install ffmpeg` (Mac) |
| "Module not found" | Run: `pip install -r requirements.txt` |
| Port 5200 in use | Use different port: `--port 5300` |
| Video upload slow | Use smaller file, check internet connection |

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [INSTALLATION.md](INSTALLATION.md) | Detailed setup for each OS |
| [API.md](API.md) | Complete API reference with examples |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & how it works |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributing & extending |
| [README.md](README.md) | Full feature overview |

---

## Need Help?

- **Setup issues?** See [INSTALLATION.md](INSTALLATION.md)
- **API questions?** See [API.md](API.md)
- **Want to code?** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Technical details?** See [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Ready to go!** 🚀

Open `http://localhost:5200` and start editing videos!
