import os, io, json, time, hashlib, traceback, textwrap
from typing import List, Optional
from pathlib import Path

import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Video processing libs
import cv2
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.video_manager import VideoManager
from scenedetect.stats_manager import StatsManager

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip

# Pillow for subtitles
from PIL import Image, ImageDraw, ImageFont

# Optional whisper for transcription
try:
    from faster_whisper import WhisperModel  # type: ignore
    _HAS_FASTER = True
except Exception:
    WhisperModel = None  # type: ignore
    _HAS_FASTER = False

try:
    import whisper  # type: ignore
    _HAS_WHISPER = True
except Exception:
    whisper = None  # type: ignore
    _HAS_WHISPER = False

# --------------------------------------------------
# Config
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
STORE_DIR = BASE_DIR / "store"
STORE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="SmartCut Studio Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/store", StaticFiles(directory=STORE_DIR), name="store")


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def hash_file(f: UploadFile) -> str:
    h = hashlib.sha1()
    while True:
        chunk = f.file.read(8192)
        if not chunk:
            break
        h.update(chunk)
    f.file.seek(0)
    return h.hexdigest()[:16]


def format_srt_time(t: float) -> str:
    t = max(0.0, float(t))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def detect_scenes(video_path: str):
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    scene_manager.add_detector(ContentDetector())
    base_timecode = None

    try:
        video_manager.set_downscale_factor()
        video_manager.start()
        base_timecode = video_manager.get_base_timecode()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(base_timecode)
    finally:
        video_manager.release()

    results = []
    for idx, (start, end) in enumerate(scene_list):
        s = start.get_seconds()
        e = end.get_seconds()
        results.append({
            "index": idx,
            "start": float(s),
            "end": float(e),
            "duration": float(max(0.0, e - s)),
            "thumb": None,
            "objects": [],
            "interesting_score": float(np.random.rand()),
        })
    return results


def make_thumb(video_path: str, sec: float, out_path: str):
    cap = cv2.VideoCapture(video_path)
    try:
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, sec) * 1000.0)
        ok, frame = cap.read()
        if ok and frame is not None:
            cv2.imwrite(out_path, frame)
    finally:
        cap.release()


def transcribe_audio(video_path: str, lang_hint: str = "") -> Optional[dict]:
    if _HAS_FASTER:
        try:
            model = WhisperModel("base")
            segments_gen, info = model.transcribe(video_path, language=lang_hint or None)
            segments = []
            full_text = []
            for seg in segments_gen:
                start = float(seg.start) if seg.start is not None else 0.0
                end = float(seg.end) if seg.end is not None else start
                text = seg.text or ""
                segments.append({"start": start, "end": end, "text": text})
                full_text.append(text)
            return {"text": " ".join(full_text).strip(), "segments": segments}
        except Exception:
            pass

    if _HAS_WHISPER:
        try:
            model = whisper.load_model("base")
            result = model.transcribe(video_path, language=lang_hint or None)
            segs = []
            for seg in result.get("segments", []):
                segs.append({"start": float(seg["start"]), "end": float(seg["end"]), "text": seg["text"]})
            return {"text": result.get("text", "").strip(), "segments": segs}
        except Exception:
            return None

    return None


def _find_video_file(video_id: str) -> Optional[Path]:
    exts = [".mp4", ".mov", ".mkv", ".avi", ".webm"]
    for ext in exts:
        p = STORE_DIR / f"{video_id}{ext}"
        if p.exists():
            return p
    return None


def _load_json(path: Path) -> Optional[dict]:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _save_json(path: Path, obj: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)


# --------------------------------------------------
# API Endpoints
# --------------------------------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...),
                  transcribe: str = Form("false"),
                  language: str = Form("")):
    try:
        vid = hash_file(file)
        ext = os.path.splitext(file.filename or "")[-1].lower() or ".mp4"
        video_path = STORE_DIR / f"{vid}{ext}"
        with open(video_path, "wb") as out:
            out.write(await file.read())

        scenes = detect_scenes(str(video_path))
        if not scenes:
            try:
                clip_tmp = VideoFileClip(str(video_path))
                dur = float(clip_tmp.duration or 0.0)
                clip_tmp.close()
            except Exception:
                dur = 0.0
            scenes = [{
                "index": 0, "start": 0.0, "end": dur, "duration": dur,
                "thumb": None, "objects": [], "interesting_score": 0.5
            }]

        for s in scenes:
            mid = (s["start"] + s["end"]) / 2.0
            thumb_path = STORE_DIR / f"{vid}_scene{s['index']}.jpg"
            make_thumb(str(video_path), mid, str(thumb_path))
            s["thumb"] = f"/store/{thumb_path.name}"

        last_end = max((s["end"] for s in scenes), default=0.0)
        beats = list(map(float, np.linspace(0.0, last_end, num=10))) if last_end > 0 else []

        _save_json(STORE_DIR / f"{vid}_scenes.json", {"scenes": scenes})
        _save_json(STORE_DIR / f"{vid}_beats.json", {"beats": beats})

        transcript = None
        if transcribe.lower() == "true":
            tr = transcribe_audio(str(video_path), language.strip())
            if tr:
                srt_path = STORE_DIR / f"{vid}.srt"
                txt_path = STORE_DIR / f"{vid}.txt"
                with open(srt_path, "w", encoding="utf-8") as f:
                    for i, seg in enumerate(tr.get("segments", []), 1):
                        f.write(f"{i}\n")
                        f.write(f"{format_srt_time(seg['start'])} --> {format_srt_time(seg['end'])}\n")
                        f.write(f"{seg['text'].strip()}\n\n")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(tr.get("text", ""))
                transcript = {
                    "srt_url": f"/store/{srt_path.name}",
                    "txt_url": f"/store/{txt_path.name}",
                    "segments": tr.get("segments", []),
                }
                _save_json(STORE_DIR / f"{vid}_transcript.json", transcript)

        return JSONResponse({
            "video_id": vid,
            "scenes": scenes,
            "beats": beats,
            "transcript": transcript,
        })
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/render")
async def render(video_id: str = Form(...),
                 selections: str = Form(...),
                 transition: str = Form("cut"),
                 transition_sec: float = Form(0.5),
                 align_to_beats: str = Form("false"),
                 subtitles: str = Form("true")):
    clip = None
    final = None
    try:
        video_path = _find_video_file(video_id)
        if not video_path:
            return JSONResponse({"error": "Video not found"}, status_code=404)

        meta = _load_json(STORE_DIR / f"{video_id}_scenes.json") or {}
        scenes = {s["index"]: s for s in meta.get("scenes", [])}
        beats_meta = _load_json(STORE_DIR / f"{video_id}_beats.json") or {}
        beats = beats_meta.get("beats", [])
        transcript_meta = _load_json(STORE_DIR / f"{video_id}_transcript.json") or {}

        arr = json.loads(selections)
        if not isinstance(arr, list) or not arr:
            return JSONResponse({"error": "No selections provided"}, status_code=400)

        clip = VideoFileClip(str(video_path))
        clips = []
        for idx in arr:
            if idx not in scenes:
                continue
            s = scenes[idx]
            start = max(0.0, float(s["start"]))
            end = max(start, float(s["end"]))

            if align_to_beats.lower() == "true" and beats:
                def _snap(x, pool, thr=0.25):
                    nb = min(pool, key=lambda b: abs(b - x))
                    return nb if abs(nb - x) <= thr else x
                start = _snap(start, beats)
                end = _snap(end, beats)

            if end - start <= 0:
                continue
            sub = clip.subclip(start, end)
            clips.append(sub)

        if not clips:
            if clip:
                clip.close()
            return JSONResponse({"error": "No valid clips to render"}, status_code=400)

        if transition == "crossfade" and len(clips) > 1 and transition_sec > 0:
            clips_cf = [clips[0]]
            for c in clips[1:]:
                clips_cf.append(c.crossfadein(transition_sec))
            try:
                final = concatenate_videoclips(clips_cf, method="compose", padding=-float(transition_sec))
            except TypeError:
                final = concatenate_videoclips(clips_cf, method="compose")
        else:
            final = concatenate_videoclips(clips, method="compose")

        # ✅ Subtitles with auto-wrap
        if subtitles.lower() == "true" and transcript_meta.get("segments"):
            subs = []
            try:
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()

            W, H = final.size
            max_width = int(W * 0.9)

            for seg in transcript_meta["segments"]:
                txt = seg.get("text", "").strip()
                if not txt:
                    continue

                # wrap text to fit screen width
                wrapped = textwrap.fill(txt, width=40)

                # measure text height
                dummy_img = Image.new("RGB", (W, 200))
                draw = ImageDraw.Draw(dummy_img)
                bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
                text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

                # background box
                box_h = text_h + 20
                img = Image.new("RGBA", (W, box_h), (0, 0, 0, 150))
                draw = ImageDraw.Draw(img)

                draw.multiline_text(((W - text_w) / 2, 10), wrapped, font=font, fill="white", align="center")

                subtitle_clip = (ImageClip(np.array(img), duration=max(0.1, seg["end"] - seg["start"]))
                                 .set_start(seg["start"])
                                 .set_position(("center", "bottom")))
                subs.append(subtitle_clip)

            if subs:
                final = CompositeVideoClip([final, *subs])

        out_path = STORE_DIR / f"{video_id}_edit.mp4"
        final.write_videofile(str(out_path), codec="libx264", audio_codec="aac",
                              temp_audiofile=str(STORE_DIR / f"{video_id}_temp-audio.m4a"),
                              remove_temp=True)

        return JSONResponse({"download_url": f"/store/{out_path.name}"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        try:
            if final:
                final.close()
        except Exception:
            pass
        try:
            if clip:
                clip.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5200,
        reload=True
    )
