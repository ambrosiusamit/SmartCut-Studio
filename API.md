# API Documentation

Complete reference for SmartCut Studio REST API.

**Base URL**: `http://localhost:5200`

## Quick Examples

### JavaScript (Fetch)

```javascript
// Analyze video
const formData = new FormData();
formData.append('file', videoFile);
formData.append('transcribe', 'true');
formData.append('language', 'en');

const response = await fetch('http://localhost:5200/analyze', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(data.video_id, data.scenes, data.beats);
```

### Python (Requests)

```python
import requests

files = {'file': open('video.mp4', 'rb')}
data = {'transcribe': 'true', 'language': 'en'}

response = requests.post(
    'http://localhost:5200/analyze',
    files=files,
    data=data
)

result = response.json()
video_id = result['video_id']
```

### cURL

```bash
# Analyze
curl -XPOST \
  -F "file=@video.mp4" \
  -F "transcribe=true" \
  -F "language=en" \
  http://localhost:5200/analyze

# Render
curl -XPOST \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "abc123",
    "selections": [0, 1, 2],
    "transition": "cut"
  }' \
  http://localhost:5200/render
```

---

## Endpoints

### POST /analyze

Analyzes a video file and returns detected scenes, beats, and optionally transcription data.

#### Request

**Content-Type**: `multipart/form-data`

**Parameters**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `file` | File | ✅ | Video file (MP4, MOV, AVI, MKV, WebM) | `video.mp4` |
| `transcribe` | string | ❌ | Enable speech-to-text | `"true"` or `"false"` |
| `language` | string | ❌ | Language hint (ISO 639-1 code) | `"en"`, `"es"`, `"fr"` |

**File Size Limits**:
- Maximum: 1GB (configurable)
- Recommended: < 500MB for faster processing

**Processing Time**: ~1-4x video duration
- 5min video = 5-20 minutes processing
- Depends on: video codec, file size, transcription enabled

#### Response

**Status**: `200 OK`

**Content-Type**: `application/json`

```json
{
  "video_id": "a590a3f31821cb5a",
  "duration": 125.5,
  "width": 1920,
  "height": 1080,
  "fps": 24.0,
  "scenes": [
    {
      "index": 0,
      "start": 0.0,
      "end": 5.2,
      "duration": 5.2,
      "thumb": "/store/a590a3f31821cb5a_thumb_0.jpg",
      "interesting_score": 0.75
    },
    {
      "index": 1,
      "start": 5.2,
      "end": 12.8,
      "duration": 7.6,
      "thumb": "/store/a590a3f31821cb5a_thumb_1.jpg",
      "interesting_score": 0.82
    }
  ],
  "beats": [
    0.0, 2.5, 5.0, 7.5, 10.0, 12.5
  ],
  "transcript": {
    "language": "en",
    "segments": [
      {
        "id": 0,
        "seek": 0,
        "start": 0.0,
        "end": 2.5,
        "text": "Hello, welcome to our channel",
        "tokens": [...],
        "temperature": 0.0,
        "avg_logprob": -0.35,
        "compression_ratio": 1.25,
        "no_speech_prob": 0.01
      }
    ],
    "srt_url": "/store/a590a3f31821cb5a.srt",
    "txt_url": "/store/a590a3f31821cb5a.txt"
  }
}
```

#### Response Fields

**Top Level**:

| Field | Type | Description |
|-------|------|-------------|
| `video_id` | string | Unique identifier for this video (SHA256 based) |
| `duration` | float | Total video length in seconds |
| `width` | int | Video width in pixels |
| `height` | int | Video height in pixels |
| `fps` | float | Frames per second |
| `scenes` | array | Detected scene cuts |
| `beats` | array | Beat timestamps (if audio present) |
| `transcript` | object | Speech transcription data (if enabled) |

**Scene Object**:

| Field | Type | Description |
|-------|------|-------------|
| `index` | int | Scene number (0-indexed) |
| `start` | float | Scene start time (seconds) |
| `end` | float | Scene end time (seconds) |
| `duration` | float | Scene length (seconds) |
| `thumb` | string | URL to scene thumbnail |
| `interesting_score` | float | Confidence score (0.0-1.0) |

**Transcript Segment**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Segment ID |
| `start` | float | Start time (seconds) |
| `end` | float | End time (seconds) |
| `text` | string | Transcribed text |
| `tokens` | array | Token IDs (for advanced analysis) |
| `temperature` | float | Model confidence (0.0 = highest) |
| `avg_logprob` | float | Average log probability |
| `no_speech_prob` | float | Probability segment is non-speech (0.0-1.0) |

#### Error Responses

**400 Bad Request**:
```json
{
  "detail": "File format not supported. Allowed: mp4, mov, avi, mkv, webm"
}
```

**413 Payload Too Large**:
```json
{
  "detail": "File exceeds maximum size of 1GB"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "FFmpeg not found. Please install FFmpeg and add to PATH."
}
```

#### Examples

**Example 1: Basic Video Analysis**

```javascript
// Only detect scenes, no transcription
fetch('http://localhost:5200/analyze', {
    method: 'POST',
    body: (() => {
        const fd = new FormData();
        fd.append('file', document.getElementById('video').files[0]);
        fd.append('transcribe', 'false');
        return fd;
    })()
})
.then(r => r.json())
.then(data => {
    console.log(`Found ${data.scenes.length} scenes`);
    console.log(`Found ${data.beats.length} beats`);
});
```

**Example 2: Full Analysis with Transcription**

```bash
curl -XPOST \
  -F "file=@podcast.mp4" \
  -F "transcribe=true" \
  -F "language=en" \
  http://localhost:5200/analyze \
  | jq '.transcript.segments[0]'
```

Output:
```json
{
  "id": 0,
  "start": 0.0,
  "end": 5.5,
  "text": "Welcome to SmartCut Studio lessons",
  "no_speech_prob": 0.001
}
```

---

### POST /render

Renders a new video by combining selected scenes with specified transitions and subtitles.

#### Request

**Content-Type**: `application/json`

**Parameters**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `video_id` | string | ✅ | From `/analyze` response | `"a590a3f31821cb5a"` |
| `selections` | array | ✅ | Scene indices to include | `[0, 1, 2]` |
| `transition` | string | ❌ | Transition type | `"cut"` or `"crossfade"` |
| `transition_sec` | float | ❌ | Fade duration (for crossfade) | `1.0` (1 second) |
| `align_to_beats` | boolean | ❌ | Snap cuts to beat points | `true` or `false` |
| `subtitles` | boolean | ❌ | Overlay transcription | `true` or `false` |

#### Response

**Status**: `200 OK`

**Content-Type**: `application/json`

```json
{
  "video_id": "a590a3f31821cb5a",
  "download_url": "/store/a590a3f31821cb5a_edit.mp4",
  "duration": 18.2,
  "file_size": 45892150,
  "details": {
    "scenes_included": [0, 1, 2],
    "transition_type": "crossfade",
    "transition_duration": 1.0,
    "subtitles_enabled": true
  },
  "status": "success"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `video_id` | string | Original video ID |
| `download_url` | string | Relative URL to download video |
| `duration` | float | Final video duration (seconds) |
| `file_size` | int | Rendered video file size (bytes) |
| `details` | object | Processing parameters used |
| `status` | string | "success" or "error" |

#### Transition Types

**"cut"** (Frame-perfect cut)
- Instantaneous switch between scenes
- Duration: 0ms
- Use for: Editing with sharp transitions, talk shows, interviews
- Rendertime: Fastest

**"crossfade"** (Smooth blend)
- Linear blend between final frame of Scene A and first frame of Scene B
- Duration: Configurable via `transition_sec` (e.g., 0.5-2.0s)
- Use for: Montages, music videos, creative transitions
- Rendertime: Slower (overlaps frames)

#### Error Responses

**400 Bad Request**:
```json
{
  "detail": "video_id 'invalid' not found in database"
}
```

**422 Unprocessable Entity**:
```json
{
  "detail": "selections must contain valid scene indices. Valid: [0, 1, 2]"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Video rendering failed: ffmpeg subprocess returned 1"
}
```

#### Examples

**Example 1: Simple Cut Edit**

```python
import requests

# Analyze video first
analyze_res = requests.post(
    'http://localhost:5200/analyze',
    files={'file': open('video.mp4', 'rb')},
    data={'transcribe': 'false'}
)
video_id = analyze_res.json()['video_id']

# Render with cuts only
render_res = requests.post(
    'http://localhost:5200/render',
    json={
        'video_id': video_id,
        'selections': [0, 2, 4],  # Include scenes 0, 2, 4 (skip 1, 3)
        'transition': 'cut'
    }
)

download_url = render_res.json()['download_url']
print(f"Download: http://localhost:5200{download_url}")
```

**Example 2: Cinematic Crossfade Edit**

```javascript
const payload = {
    video_id: 'a590a3f31821cb5a',
    selections: [0, 1, 2, 3, 4],
    transition: 'crossfade',
    transition_sec: 1.5,  // 1.5 second fade
    subtitles: true,       // Include transcription
    align_to_beats: true   // Snap to beats
};

fetch('http://localhost:5200/render', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => {
    const link = document.createElement('a');
    link.href = data.download_url;
    link.download = 'edited_video.mp4';
    link.click();
});
```

**Example 3: Beat-Aligned Montage**

```bash
curl -XPOST http://localhost:5200/render \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "a590a3f31821cb5a",
    "selections": [0, 1, 2, 3, 4, 5],
    "transition": "crossfade",
    "transition_sec": 0.5,
    "align_to_beats": true,
    "subtitles": false
  }' \
  | jq '.download_url'
```

---

## Response Codes

| Code | Meaning | Typical Use |
|------|---------|------------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid parameters or file format |
| `413` | Payload Too Large | File exceeds size limit |
| `422` | Unprocessable | Invalid request body |
| `500` | Server Error | FFmpeg missing, disk full, etc. |
| `503` | Service Unavailable | Server busy (optional: with rate limiting) |

---

## Rate Limiting (Optional)

If the server has rate limiting enabled:

```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 4
X-RateLimit-Reset: 1709654400
```

**429 Too Many Requests**:
```json
{
  "detail": "Rate limit exceeded. Max 5 requests per minute."
}
```

Retry-After: 60 seconds

---

## CORS Headers

All responses include CORS headers for browser access:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Data Types

### Timestamps

All times are in **seconds** with millisecond precision:
- `0.0` = start of video
- `5.25` = 5.25 seconds
- `125.5` = 2 minutes 5.5 seconds

### Scores

Confidence/interesting scores are `0.0` to `1.0`:
- `0.0` = lowest confidence
- `0.5` = medium
- `1.0` = highest confidence

### File URLs

Download URLs are relative. Full URLs:

```
http://localhost:5200/store/video_id_filename.mp4
```

---

## Webhooks (Future Feature)

Future versions may support webhooks for progress updates:

```json
{
  "webhook_url": "https://yourapp.com/callback",
  "events": ["analysis_started", "analysis_complete", "render_complete"]
}
```

---

## Performance

### Timeout

Default timeout: 3600 seconds (1 hour)
- Analyze: Typically 1-4 minutes
- Render: Typically 2-10 minutes

### Concurrent Requests

- Recommended: 2-4 concurrent uploads
- Beyond this: Server will queue requests
- Peak performance: Single thread per request

---

## Testing

### Using Postman

1. Import endpoints:
   - POST `http://localhost:5200/analyze`
   - POST `http://localhost:5200/render`

2. For `/analyze`:
   - Body → form-data
   - Key: `file`, Value: [select video file]
   - Key: `transcribe`, Value: `true`

3. For `/render`:
   - Body → raw (JSON)
   - Paste JSON payload

### Using Python

```python
import requests
from pathlib import Path

# Setup
API_URL = "http://localhost:5200"
TEST_VIDEO = Path("test.mp4")

# Analyze
files = {'file': open(TEST_VIDEO, 'rb')}
data = {'transcribe': 'true'}
analyze = requests.post(f"{API_URL}/analyze", files=files, data=data)
print(f"Status: {analyze.status_code}")
print(f"Scenes: {len(analyze.json()['scenes'])}")

# Render
video_id = analyze.json()['video_id']
render_req = {
    'video_id': video_id,
    'selections': [0, 1],
    'transition': 'crossfade'
}
render = requests.post(f"{API_URL}/render", json=render_req)
print(f"Download: {render.json()['download_url']}")
```

---

**API Version**: 1.0  
**Last Updated**: March 2026  
**Support**: Check [TROUBLESHOOTING.md](../README.md#-troubleshooting) for common issues
