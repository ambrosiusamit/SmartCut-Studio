# Installation Guide

Complete step-by-step instructions to get SmartCut Studio running on your system.

## Prerequisites Check

Before starting, verify you have:
- ✅ **Python 3.8+** (check: `python --version`)
- ✅ **Git** (check: `git --version`)
- ✅ **A text editor** (VS Code, PyCharm, or similar)

---

## Platform-Specific Installation

### Windows 10/11

#### Step 1: Install Python

1. Go to [python.org](https://python.org/downloads)
2. Download **Python 3.11** or latest
3. Run installer
4. ✅ **CHECK**: "Add Python to PATH"
5. Click "Install Now"

**Verify installation**:
```powershell
python --version
# Expected: Python 3.11.x
```

#### Step 2: Install FFmpeg

**Option A: Using Package Manager (Recommended)**
```powershell
winget install ffmpeg
```

**Option B: Manual Download**
1. Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Download Windows build
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Paste: `C:\ffmpeg\bin`
   - Click OK → OK → OK

**Verify installation**:
```powershell
ffmpeg -version
# Should show FFmpeg version
```

#### Step 3: Install Git

1. Go to [git-scm.com](https://git-scm.com/download/win)
2. Download latest version
3. Run installer (use default settings)

**Verify**:
```powershell
git --version
# Expected: git version 2.x.x
```

#### Step 4: Clone Repository

```powershell
# Navigate to Desktop or desired folder
cd Desktop

# Clone the repository
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio
```

#### Step 5: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Expected output: (venv) in terminal prompt
```

#### Step 6: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- opencv-python
- moviepy
- scenedetect
- numpy
- uvicorn

#### Step 7: (Optional) Install Transcription

```powershell
# Faster Whisper (Recommended - faster)
pip install faster-whisper

# OR

# OpenAI Whisper (Official)
pip install openai-whisper
```

#### Step 8: Run the Application

```powershell
# Navigate to backend
cd smartcut-backend

# Start server
python app.py
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:5200
```

✅ **Success!** Open browser to `http://localhost:5200`

---

### macOS 12+

#### Step 1: Install Homebrew (if needed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
# Expected: Python 3.11.x
```

#### Step 3: Install FFmpeg

```bash
brew install ffmpeg

# Verify
ffmpeg -version
```

#### Step 4: Install Git

```bash
# Usually pre-installed on macOS
git --version

# If needed:
brew install git
```

#### Step 5: Clone Repository

```bash
cd ~/Desktop
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio
```

#### Step 6: Create Virtual Environment

```bash
# Use python3
python3 -m venv venv

# Activate
source venv/bin/activate

# Expected: (venv) in prompt
```

#### Step 7: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

#### Step 8: (Optional) Install Transcription

```bash
# Option 1: Faster Whisper
pip install faster-whisper

# Option 2: OpenAI Whisper
pip install openai-whisper
```

#### Step 9: Run Application

```bash
cd smartcut-backend
python app.py
```

✅ **Access**: Open browser to `http://localhost:5200`

---

### Linux (Ubuntu 20.04+)

#### Step 1: Install Python

```bash
# Update package list
sudo apt-get update

# Install Python 3.8 or newer (usually pre-installed)
sudo apt-get install -y python3 python3-venv python3-pip
```

**Verify**:
```bash
python3 --version
```

#### Step 2: Install FFmpeg

```bash
sudo apt-get install -y ffmpeg

# Verify
ffmpeg -version
```

#### Step 3: Install Git

```bash
sudo apt-get install -y git

# Verify
git --version
```

#### Step 4: Clone Repository

```bash
cd ~
git clone https://github.com/ambrosiusamit/smartcut-studio.git
cd smartcut-studio
```

#### Step 5: Create Virtual Environment

```bash
# Use python3
python3 -m venv venv

# Activate
source venv/bin/activate

# Expected: (venv) in prompt
```

#### Step 6: Install Dependencies

```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 7: (Optional) Install Transcription

```bash
# Faster Whisper (recommended)
pip install faster-whisper

# OR OpenAI Whisper
pip install openai-whisper
```

#### Step 8: Run Application

```bash
cd smartcut-backend
python app.py
```

✅ **Access**: `http://localhost:5200` in browser

---

## Post-Installation Verification

After installation, run these checks:

### Check 1: Python & Packages

```bash
# Should show all installed packages
pip list | grep -E "fastapi|opencv|moviepy|scenedetect"
```

**Expected output**:
```
fastapi              0.104.1
opencv-python        4.8.1
moviepy              1.0.3
scenedetect          0.6.1
```

### Check 2: FFmpeg

```bash
# Should work without errors
ffmpeg -version
```

### Check 3: API Health Check

```bash
# In new terminal, with venv activated:
curl http://localhost:5200/status

# Or visit in browser:
# http://localhost:5200
```

### Check 4: Database Path

Verify `/store` directory exists:

```bash
# Windows
dir smartcut-backend\store

# Unix/Linux
ls smartcut-backend/store/
```

Should be empty initially.

---

## Starting the Application

### Quick Start (Every Time)

**Windows**:
```powershell
cd path\to\smartcut-studio
cd smartcut-backend
venv\Scripts\activate
python app.py
```

**macOS/Linux**:
```bash
cd ~/smartcut-studio
cd smartcut-backend
source venv/bin/activate
python app.py
```

### Using Development Mode

For auto-reloading on code changes:

```bash
cd smartcut-backend
python -m uvicorn app:app --reload --port 5200
```

### Access the Application

1. **Backend API**: `http://localhost:5200`
2. **Frontend Interface**: Open `smartcut-frontend/index.html` in browser
3. **Interactive Docs**: `http://localhost:5200/docs` (auto-generated by FastAPI)

---

## Testing Your Installation

### Test 1: Upload a Test Video

1. Go to `http://localhost:5200` (in Firefox or Chrome)
2. Click "Choose File"
3. Select any `.mp4` video from your computer
4. Click "Analyze"
5. Wait for processing (1-3 minutes for 5 min video)

**Expected result**: Scenes, beats, and optional transcript displayed

### Test 2: API Test with cURL

```bash
# Assuming you have a test.mp4 in current directory
curl -F "file=@test.mp4" http://localhost:5200/analyze
```

Should return JSON with `video_id`, `scenes`, `beats`, etc.

---

## Troubleshooting

### Issue: "Python not found"

**Solution**: Python not in PATH
- Windows: Reinstall Python, check "Add to PATH"
- macOS/Linux: Use `python3` instead of `python`

### Issue: "FFmpeg not found"

**Solution**:
```bash
# Windows (restart terminal after PATH update)
setx PATH "%PATH%;C:\ffmpeg\bin"

# macOS/Linux
which ffmpeg  # Should show path
```

### Issue: "Permission denied" (macOS/Linux)

**Solution**:
```bash
chmod +x smartcut-backend/app.py
```

### Issue: Virtual environment not activating

**Solution**:
- Windows: Use `cd venv\Scripts` then test `python --version`
- Unix: Use `source venv/bin/activate` (not just `venv/bin/activate`)

### Issue: Module 'fastapi' not found

**Solution**:
```bash
# Make sure venv is activated
pip install -r requirements.txt

# Or reinstall
pip install --force-reinstall -r requirements.txt
```

### Issue: "Address already in use" (Port 5200)

**Solution**: Another process using port 5200
```bash
# Find process on port 5200
# Windows: netstat -ano | findstr :5200
# Unix: lsof -i :5200

# Kill it or use different port
python -m uvicorn app:app --port 5300
```

### Issue: Out of Memory

**Solution**: Running out of RAM during video processing
- Use smaller test video first
- Close other applications
- Increase virtual memory (disk swap space)

### Issue: Incomplete Installation

**Complete reinstall**:
```bash
# Remove and recreate virtual environment
rm -rf venv         # Unix/Linux
rmdir /s venv       # Windows

python -m venv venv
source venv/bin/activate  # Unix/Linux
# OR
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## Next Steps

After successful installation:

1. **Read README.md** for features and API overview
2. **Check API.md** for endpoint documentation
3. **Review ARCHITECTURE.md** to understand system design
4. **See DEVELOPMENT.md** if you want to contribute

---

## Getting Help

If installation fails:

1. **Check error message carefully** - often contains the solution
2. **Search GitHub issues** - similar problems may be documented
3. **Open new issue** with:
   - Your OS and Python version
   - Full error message
   - Steps to reproduce

**Helpful command** to share in issues:
```bash
python -V && ffmpeg -version && pip list
```

---

## Installation Verified? ✅

If you can:
- [ ] Run `python --version` (shows 3.8+)
- [ ] Run `ffmpeg -version` (shows FFmpeg info)
- [ ] See `venv/bin/activate` or `venv\Scripts\activate` exists
- [ ] Run `pip list` and see fastapi, opencv-python, scenedetect
- [ ] Access `http://localhost:5200` in browser
- [ ] Upload a test video successfully

**Then you're all set! 🎉**

---

**Installation Guide v1.0**
Last Updated: March 2026
