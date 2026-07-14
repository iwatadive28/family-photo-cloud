from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

BASE_PATH = "/" + os.environ.get("BASE_PATH", "/photo-frame").strip("/")
PHOTO_FRAME_DIR = Path(os.environ.get("PHOTO_FRAME_DIR", "./sample-photos")).expanduser().resolve()
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
CACHE_DIR = ROOT / "runtime" / "photo-cache"
LITE_IMAGE_MAX_EDGE = int(os.environ.get("LITE_IMAGE_MAX_EDGE", "1280"))
LITE_IMAGE_QUALITY = int(os.environ.get("LITE_IMAGE_QUALITY", "82"))

app = FastAPI(title="Photo Frame Web")


def safe_photo_path(relative_path: str) -> Path:
    candidate = (PHOTO_FRAME_DIR / relative_path).resolve()
    if candidate != PHOTO_FRAME_DIR and PHOTO_FRAME_DIR not in candidate.parents:
        raise HTTPException(status_code=403, detail="invalid photo path")
    return candidate


def list_photos() -> list[dict[str, object]]:
    if not PHOTO_FRAME_DIR.exists():
        return []

    photos: list[dict[str, object]] = []
    for item in PHOTO_FRAME_DIR.rglob("*"):
        if not item.is_file() or item.name.startswith("."):
            continue
        if item.suffix.lower() not in PHOTO_EXTENSIONS:
            continue
        relative = item.relative_to(PHOTO_FRAME_DIR).as_posix()
        stat = item.stat()
        photos.append(
            {
                "path": relative,
                "name": item.name,
                "size": stat.st_size,
                "mtimeMs": stat.st_mtime * 1000,
                "url": f"{BASE_PATH}/photos/{quote(relative)}",
                "liteUrl": f"{BASE_PATH}/photos-lite/{quote(relative)}",
            }
        )
    return sorted(photos, key=lambda photo: float(photo["mtimeMs"]), reverse=True)


def lite_cache_path(photo: Path) -> Path:
    relative = photo.relative_to(PHOTO_FRAME_DIR).as_posix()
    stat = photo.stat()
    key = f"{relative}|{stat.st_mtime_ns}|{stat.st_size}|{LITE_IMAGE_MAX_EDGE}|{LITE_IMAGE_QUALITY}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return CACHE_DIR / f"{digest}.jpg"


def build_lite_photo(photo: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(photo) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.thumbnail((LITE_IMAGE_MAX_EDGE, LITE_IMAGE_MAX_EDGE), Image.Resampling.LANCZOS)
        image.save(output, "JPEG", quality=LITE_IMAGE_QUALITY, optimize=True, progressive=True)


@app.get("/")
def root() -> HTMLResponse:
    return HTMLResponse(f'<meta http-equiv="refresh" content="0; url={BASE_PATH}">')


@app.get(BASE_PATH)
@app.get(BASE_PATH + "/")
def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML, headers={"Cache-Control": "no-store"})


@app.get(BASE_PATH + "/api/photos")
def api_photos() -> JSONResponse:
    photos = list_photos()
    return JSONResponse({"ok": True, "photoDir": str(PHOTO_FRAME_DIR), "count": len(photos), "photos": photos})


@app.get(BASE_PATH + "/photos/{photo_path:path}")
def photo(photo_path: str) -> FileResponse:
    path = safe_photo_path(photo_path)
    if not path.exists() or not path.is_file() or path.suffix.lower() not in PHOTO_EXTENSIONS:
        raise HTTPException(status_code=404, detail="photo is not available")
    return FileResponse(path, headers={"Cache-Control": "public, max-age=300"})


@app.get(BASE_PATH + "/photos-lite/{photo_path:path}")
def photo_lite(photo_path: str) -> FileResponse:
    path = safe_photo_path(photo_path)
    if not path.exists() or not path.is_file() or path.suffix.lower() not in PHOTO_EXTENSIONS:
        raise HTTPException(status_code=404, detail="photo is not available")
    cache = lite_cache_path(path)
    if not cache.exists():
        try:
            build_lite_photo(path, cache)
        except Exception as exc:
            raise HTTPException(status_code=502, detail="failed to build lite photo") from exc
    return FileResponse(cache, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})


INDEX_HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Photo Frame Web</title>
  <style>
    :root { color-scheme: dark; font-family: system-ui, sans-serif; background: #050505; color: #fff; }
    * { box-sizing: border-box; }
    html, body, .app { width: 100%; height: 100%; margin: 0; overflow: hidden; }
    .app { position: relative; background: #050505; cursor: none; touch-action: manipulation; user-select: none; }
    .backdrop {
      position: absolute;
      inset: -5%;
      background-position: center;
      background-size: cover;
      filter: blur(28px);
      opacity: 0;
      transform: scale(1.1);
      transition: opacity 1400ms ease;
    }
    .backdrop.visible { opacity: 0.5; }
    .shade {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at center, rgba(0,0,0,0.05), rgba(0,0,0,0.4));
    }
    .photo {
      position: absolute;
      inset: 0;
      width: 100vw;
      height: 100vh;
      object-fit: contain;
      opacity: 0;
      transition: opacity 1400ms ease;
      animation: kenburns 12s linear infinite;
    }
    .photo.visible { opacity: 1; }
    @keyframes kenburns {
      0% { transform: scale(1.015) translate3d(-0.3%, -0.2%, 0); }
      100% { transform: scale(1.075) translate3d(0.35%, 0.28%, 0); }
    }
    .clock {
      position: absolute;
      top: 18px;
      right: 18px;
      z-index: 3;
      min-width: 150px;
      padding: 12px 15px;
      border-radius: 8px;
      background: rgba(0,0,0,0.24);
      text-align: right;
      text-shadow: 0 1px 12px rgba(0,0,0,0.8);
      opacity: 0;
      pointer-events: none;
      transition: opacity 500ms ease;
    }
    .clock.visible { opacity: 0.86; }
    .time { font-size: 46px; font-weight: 750; line-height: 1; }
    .date { margin-top: 7px; font-size: 18px; font-weight: 650; }
    .controls {
      position: absolute;
      left: 50%;
      bottom: max(14px, env(safe-area-inset-bottom));
      z-index: 4;
      display: flex;
      gap: 8px;
      transform: translateX(-50%);
      padding: 7px;
      border-radius: 999px;
      background: rgba(0,0,0,0.34);
      opacity: 0;
      pointer-events: none;
      transition: opacity 240ms ease;
    }
    .controls.show { opacity: 0.95; pointer-events: auto; }
    button {
      min-width: 74px;
      min-height: 42px;
      border: 0;
      border-radius: 999px;
      padding: 0 13px;
      background: rgba(255,255,255,0.12);
      color: rgba(255,255,255,0.84);
      font: inherit;
      font-weight: 700;
    }
    button.active { background: rgba(190,232,255,0.86); color: #10202a; }
    .empty {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      z-index: 2;
      color: rgba(255,255,255,0.78);
      font-size: 22px;
    }
    html.lite .backdrop { filter: none; transform: scale(1.03); }
    html.lite .backdrop.visible { opacity: 0.34; }
    html.lite .photo { animation: none !important; transition: opacity 700ms ease; }
  </style>
</head>
<body>
  <main id="app" class="app">
    <div id="backdropA" class="backdrop"></div>
    <div id="backdropB" class="backdrop"></div>
    <div class="shade"></div>
    <img id="photoA" class="photo" alt="">
    <img id="photoB" class="photo" alt="">
    <div id="empty" class="empty">写真が見つかりません</div>
    <div id="clock" class="clock">
      <div id="time" class="time"></div>
      <div id="date" class="date"></div>
    </div>
    <nav id="controls" class="controls">
      <button id="clockButton" type="button">時計</button>
      <button id="nextButton" type="button">次へ</button>
    </nav>
  </main>
  <script>
    const liteMode = new URLSearchParams(location.search).get("lite") === "1";
    document.documentElement.classList.toggle("lite", liteMode);

    const app = document.getElementById("app");
    const photos = [document.getElementById("photoA"), document.getElementById("photoB")];
    const backdrops = [document.getElementById("backdropA"), document.getElementById("backdropB")];
    const empty = document.getElementById("empty");
    const controls = document.getElementById("controls");
    const clock = document.getElementById("clock");
    const clockButton = document.getElementById("clockButton");
    const nextButton = document.getElementById("nextButton");
    const timeEl = document.getElementById("time");
    const dateEl = document.getElementById("date");
    let items = [];
    let index = 0;
    let photoLayer = 0;
    let backdropLayer = 0;
    let controlsTimer = null;
    let showClock = localStorage.getItem("photoFrameShowClock") === "true";

    function basePath() { return location.pathname.replace(/\\/$/, ""); }
    function shuffle(list) {
      const copied = [...list];
      for (let i = copied.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copied[i], copied[j]] = [copied[j], copied[i]];
      }
      return copied;
    }
    function photoUrl(photo) {
      const displayUrl = liteMode && photo.liteUrl ? photo.liteUrl : photo.url;
      return `${displayUrl}?v=${Math.floor(photo.mtimeMs)}`;
    }
    function renderClock() {
      const now = new Date();
      const weekdays = ["日", "月", "火", "水", "木", "金", "土"];
      timeEl.textContent = now.toLocaleTimeString("ja-JP", { hour: "2-digit", minute: "2-digit" });
      dateEl.textContent = `${now.getMonth() + 1}/${now.getDate()} (${weekdays[now.getDay()]})`;
    }
    function setClock(visible) {
      showClock = visible;
      localStorage.setItem("photoFrameShowClock", visible ? "true" : "false");
      clock.classList.toggle("visible", visible);
      clockButton.classList.toggle("active", visible);
      renderClock();
    }
    setInterval(renderClock, 1000);
    function showControls() {
      controls.classList.add("show");
      if (controlsTimer) clearTimeout(controlsTimer);
      controlsTimer = setTimeout(() => controls.classList.remove("show"), 3500);
    }
    function showPhoto(nextIndex) {
      if (!items.length) {
        empty.style.display = "grid";
        return;
      }
      index = ((nextIndex % items.length) + items.length) % items.length;
      const url = photoUrl(items[index]);
      const preload = new Image();
      preload.onload = () => {
        empty.style.display = "none";
        const nextBackdrop = 1 - backdropLayer;
        backdrops[nextBackdrop].style.backgroundImage = `url("${url}")`;
        backdrops[nextBackdrop].classList.add("visible");
        backdrops[backdropLayer].classList.remove("visible");
        backdropLayer = nextBackdrop;

        const nextPhoto = 1 - photoLayer;
        photos[nextPhoto].src = url;
        photos[nextPhoto].classList.add("visible");
        photos[photoLayer].classList.remove("visible");
        photoLayer = nextPhoto;
      };
      preload.src = url;
    }
    async function loadPhotos() {
      const response = await fetch(`${basePath()}/api/photos`, { cache: "no-store" });
      const data = await response.json();
      items = shuffle(Array.isArray(data.photos) ? data.photos : []);
      showPhoto(0);
    }
    app.addEventListener("click", (event) => {
      if (event.target.closest(".controls")) return;
      showPhoto(index + 1);
      showControls();
    });
    clockButton.addEventListener("click", (event) => {
      event.stopPropagation();
      setClock(!showClock);
      showControls();
    });
    nextButton.addEventListener("click", (event) => {
      event.stopPropagation();
      showPhoto(index + 1);
      showControls();
    });
    window.addEventListener("keydown", (event) => {
      if (event.key === "c" || event.key === "C") setClock(!showClock);
      if (event.key === " " || event.key === "Enter" || event.key === "ArrowRight") showPhoto(index + 1);
    });
    setClock(showClock);
    loadPhotos().catch((error) => {
      console.error(error);
      empty.textContent = "写真を読み込めません";
      empty.style.display = "grid";
    });
    setInterval(() => showPhoto(index + 1), 10000);
  </script>
</body>
</html>
"""

