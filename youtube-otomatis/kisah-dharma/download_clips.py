#!/usr/bin/env python3
"""Unduh klip Pexels. Coba varian HD dulu (pola nama file Pexels),
fallback ke URL SD yang diberikan. Hanya simpan bila respons video valid."""
import os, re, sys, urllib.request

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma/clips"
os.makedirs(BASE, exist_ok=True)

URLS = [
    ("lilin_meja",      "https://videos.pexels.com/video-files/6343575/6343575-sd_960_506_30fps.mp4"),
    ("gurun_drone",     "https://videos.pexels.com/video-files/19348569/19348569-sd_640_360_30fps.mp4"),
    ("gurun_langit",    "https://videos.pexels.com/video-files/19376560/19376560-sd_640_360_25fps.mp4"),
    ("sunrise_kabut",   "https://videos.pexels.com/video-files/28998963/12542044_640_360_60fps.mp4"),
    ("langit_tenang",   "https://videos.pexels.com/video-files/30125147/12919965_640_360_30fps.mp4"),
    ("sungai_alir",     "https://videos.pexels.com/video-files/5161856/5161856-sd_640_360_24fps.mp4"),
    ("sungai_hutan",    "https://videos.pexels.com/video-files/6582323/6582323-sd_640_360_30fps.mp4"),
    ("gunung_kabut",    "https://videos.pexels.com/video-files/4763085/4763085-sd_640_360_24fps.mp4"),
    ("bukit_kabut",     "https://videos.pexels.com/video-files/29854905/12819743_640_360_30fps.mp4"),
    ("api_unggun",      "https://videos.pexels.com/video-files/6177137/6177137-sd_640_360_30fps.mp4"),
    ("ombak",           "https://videos.pexels.com/video-files/19054843/19054843-sd_640_360_30fps.mp4"),
    ("hutan_cahaya",    "https://videos.pexels.com/video-files/5692315/5692315-sd_640_360_30fps.mp4"),
    ("badai_gelap",     "https://videos.pexels.com/video-files/13309966/13309966-sd_640_360_30fps.mp4"),
    ("senja_rumput",    "https://videos.pexels.com/video-files/6562094/6562094-sd_640_360_30fps.mp4"),
]

def candidates(url):
    """Bangun kandidat HD dari pola nama file Pexels."""
    m = re.match(r"(https://videos\.pexels\.com/video-files/\d+/)(.+)\.mp4", url)
    base, fn = m.group(1), m.group(2)
    cands = []
    # pola: {id}-sd_W_H_{fps}fps atau {id}_W_H_{fps}fps
    mm = re.match(r"(.+?)[-_](?:sd_)?(\d+)_(\d+)_(\d+fps)$", fn)
    if mm:
        stem, w, h, fps = mm.groups()
        w, h = int(w), int(h)
        if w >= h:  # landscape
            for tw, th in [(3840, 2160), (2560, 1440), (1920, 1080), (1280, 720)]:
                if tw > w:
                    sep = "-" if "-" in fn[:len(stem)+1] else "_"
                    # pertahankan gaya pemisah asli
                    if f"{stem}-sd_" in fn or f"{stem}-" in fn:
                        cands.append(f"{base}{stem}-hd_{tw}_{th}_{fps}.mp4")
                        cands.append(f"{base}{stem}-uhd_{tw}_{th}_{fps}.mp4")
                    else:
                        cands.append(f"{base}{stem}_{tw}_{th}_{fps}.mp4")
        break_out = False
        # de-duplikasi & hanya yang resolusinya > asli
    seen = []
    for c in cands:
        if c not in seen:
            seen.append(c)
    seen.append(url)  # fallback SD asli
    return seen

def try_fetch(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ct = r.headers.get("Content-Type", "")
            if r.status != 200 or "video" not in ct:
                return False
            with open(out, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            return os.path.getsize(out) > 200000
    except Exception as e:
        print("   gagal:", str(e)[:100])
        return False

results = {}
for label, url in URLS:
    out = f"{BASE}/{label}.mp4"
    if os.path.exists(out) and os.path.getsize(out) > 200000:
        print(f"skip {label} (sudah ada)")
        results[label] = out
        continue
    print(f"[{label}]")
    ok = False
    for cand in candidates(url):
        print("  coba:", cand.split("/")[-1])
        if try_fetch(cand, out):
            print("  OK:", os.path.getsize(out), "bytes")
            results[label] = out
            ok = True
            break
        elif os.path.exists(out):
            os.remove(out)
    if not ok:
        print("  GAGAL semua kandidat")

print("\nBerhasil:", len(results), "/", len(URLS))
for k, v in results.items():
    print(" ", k, v, os.path.getsize(v))
