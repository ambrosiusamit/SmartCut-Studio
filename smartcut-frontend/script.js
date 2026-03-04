// Auto-pick backend: prefer same origin (if served via /web), else localhost:5200
let API = "";
if (location.pathname.startsWith("/web")) {
  API = location.origin; // e.g., http://localhost:5200
} else {
  API = "http://localhost:5200";
}

const fileInput = document.getElementById("file");
const doTranscribe = document.getElementById("doTranscribe");
const langHint = document.getElementById("lang");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const sceneListEl = document.getElementById("sceneList");
const renderBtn = document.getElementById("renderBtn");
const transitionSel = document.getElementById("transition");
const transitionSec = document.getElementById("transitionSec");
const alignBeats = document.getElementById("alignBeats");
const downloadBox = document.getElementById("downloadBox");
const transcriptBox = document.getElementById("transcriptBox");
const transcriptPreview = document.getElementById("transcriptPreview");
const transcriptLinks = document.getElementById("transcriptLinks");

let analysis = null;
let selected = new Set();

function setStatus(msg) { statusEl.textContent = msg; }

analyzeBtn.onclick = async () => {
  const f = fileInput.files[0];
  if (!f) { alert("Pick a video first!"); return; }

  analyzeBtn.disabled = true;
  setStatus("Uploading & analyzing…");

  const fd = new FormData();
  fd.append("file", f);
  fd.append("transcribe", doTranscribe.checked ? "true" : "false");
  fd.append("language", (langHint.value || "").trim());

  try {
    const r = await fetch(`${API}/analyze`, { method: "POST", body: fd });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    if (data.error) throw new Error(data.error);
    analysis = data;
    renderScenes();
    resultsEl.classList.remove("hidden");
    setStatus(`Found ${data.scenes.length} scenes. Beats detected: ${data.beats.length}.`);

    if (data.transcript) {
      transcriptBox.classList.remove("hidden");
      const preview = (data.transcript.segments || []).slice(0, 20).map(s => s.text).join(" ");
      transcriptPreview.textContent = preview || "(No speech detected)";
      transcriptLinks.innerHTML = `
        <p>Downloads:
          <a href="${API}${data.transcript.srt_url}" download>Transcript (.srt)</a> ·
          <a href="${API}${data.transcript.txt_url}" download>Plain text (.txt)</a>
        </p>
      `;
    } else {
      transcriptBox.classList.add("hidden");
    }
  } catch (e) {
    console.error(e);
    alert("Analyze failed: " + e.message);
    setStatus("Analyze failed.");
  } finally {
    analyzeBtn.disabled = false;
  }
};

function renderScenes() {
  sceneListEl.innerHTML = "";
  selected = new Set(analysis.scenes.map(s => s.index)); // select all by default
  analysis.scenes.forEach(s => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${API}${s.thumb}" alt="thumb ${s.index}" />
      <div class="meta"><b>Scene ${s.index}</b> · ${s.duration.toFixed(2)}s · ${s.start.toFixed(2)}s → ${s.end.toFixed(2)}s</div>
      <div class="tags"><span class="tag">Score ${(s.interesting_score || 0).toFixed(2)}</span></div>
      <div style="margin-top:8px; padding:0 10px 12px;">
        <label><input type="checkbox" data-idx="${s.index}" checked> Include</label>
      </div>
    `;
    card.querySelector("input[type=checkbox]").onchange = (ev) => {
      const idx = parseInt(ev.target.dataset.idx, 10);
      if (ev.target.checked) selected.add(idx); else selected.delete(idx);
    };
    sceneListEl.appendChild(card);
  });
}

renderBtn.onclick = async () => {
  if (!analysis) return;
  const arr = Array.from(selected).sort((a,b)=>a-b);
  if (arr.length === 0) { alert("Select at least one scene."); return; }

  renderBtn.disabled = true;
  setStatus("Rendering your rough cut…");

  const fd = new FormData();
  fd.append("video_id", analysis.video_id);
  fd.append("selections", JSON.stringify(arr));
  fd.append("transition", transitionSel.value);
  fd.append("transition_sec", parseFloat(transitionSec.value || "0.5"));
  fd.append("align_to_beats", alignBeats.checked ? "true" : "false");

  try {
    const r = await fetch(`${API}/render`, { method: "POST", body: fd });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    if (data.error) throw new Error(data.error);
    const url = `${API}${data.download_url}`;
    downloadBox.classList.remove("hidden");
    downloadBox.innerHTML = `<p><a href="${url}" download>⬇️ Download Edited Video</a></p>`;
    setStatus("Render complete.");
  } catch (e) {
    console.error(e);
    alert("Render failed: " + e.message);
    setStatus("Render failed.");
  } finally {
    renderBtn.disabled = false;
  }
};
