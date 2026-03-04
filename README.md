# SmartCut Studio

AI-assisted video editing application with automatic scene detection, beat-synced transitions and optional transcription. Lightweight FastAPI backend paired with a simple HTML/JS frontend.

---

##  Project Overview

SmartCut Studio lets users upload videos, automatically analyzes scenes and audio beats, and renders edited clips with optional subtitles. The backend exposes a minimal REST API (`/analyze` and `/render`), while the frontend demonstrates usage via a static page. Designed as a student portfolio project, it showcases fast prototyping, multimedia processing, and web APIs.

---

##  Features

- Automatic scene detection using **PySceneDetect**
- Beat-synced transitions for music videos
- Whisper transcription with SRT subtitle output
- Multiple transition types (cut, crossfade)
- REST API compatible with any client
- Simple browser-based demo UI

---

##  Architecture

```
SmartCut-Studio/
 smartcut-backend/   # FastAPI application + processing logic
    app.py
    store/          # outputs (ignored by git)

 smartcut-frontend/  # Static HTML/CSS/JS user interface
    index.html
    script.js
    style.css

 requirements.txt
 README.md           # this file
 LICENSE
```

Backend responsibilities:
- Handle uploads and store incoming videos
- Detect scenes, beats and transcribe audio
- Render final video with selected scenes and transitions
- Serve resulting files from `/store`

Frontend responsibilities:
- Provide a minimal interface for upload, selection and download
- Interact with backend API via `fetch()` calls

---

##  Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/ambrosiusamit/SmartCut-Studio.git
   cd SmartCut-Studio
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** (required for video processing):
   - Windows: `winget install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

5. **Run backend server**
   ```bash
   cd smartcut-backend
   python app.py
   ```

6. **Open frontend**
   - Open `smartcut-frontend/index.html` directly in browser
   - or visit `http://localhost:5200/docs` for API docs

---

##  API Endpoints

### `POST /analyze`
Uploads a video and returns analysis results.
- Parameters: `file` (video), `transcribe` (`true`/`false`), `language`
- Response includes `video_id`, `scenes`, `beats`, `transcript` URLs.

### `POST /render`
Creates edited video from selected scenes.
- JSON body: `video_id`, `selections`, `transition`, etc.
- Returns `download_url`, `duration`, and status.

> The API is intentionally simple; refer to inline comments in `app.py` for details.

---

##  Future Improvements

- User authentication & per-user storage
- Background job queue with progress updates
- Docker support and CI/CD pipeline
- Unit tests, linting and continuous integration
- More advanced editing features (filters, effects)
- Support for cloud storage (S3/GCS)
- Improved frontend with React/Vue or similar

---

##  Recommended Folder Structure

```
SmartCut-Studio/
 smartcut-backend/
    app.py
    requirements.txt   # optionally keep here
    store/             # gitignored
 smartcut-frontend/
    index.html
    script.js
    style.css
 README.md
 LICENSE
 .gitignore
```

Keep all project logic in the two primary directories; move configuration (requirements.txt) into backend if desired.

---

##  Files to Delete

To simplify the repository for portfolio use, you can safely remove the following:

- `API.md`  
- `ARCHITECTURE.md`  
- `DEVELOPMENT.md`  
- `INSTALLATION.md`  
- `QUICK_START.md`  
- `PUSH.md`  

Optionally, merge any relevant notes from `CONTRIBUTING.md` into the README and then delete `CONTRIBUTING.md` as well.

Maintenance files like `.gitignore`, `requirements.txt`, and `LICENSE` should remain.

---

##  Professionalization Suggestions

- Add a simple README with badges (build status, license).
- Include a `requirements.txt` and ensure its kept minimal.
- Add a `gitignore` ignoring virtualenvs and output files.
- Write concise inline comments in `app.py` for readability.
- Add a small test video or instructions in README for demo.
- Use semantic versioning tags when releasing.
- Display screenshots or a GIF in README showing the UI.
- Optionally include a Dockerfile for easy deployment.

These changes keep the repo clean, approachable for recruiters, and showcase your ability to structure a project clearly.
