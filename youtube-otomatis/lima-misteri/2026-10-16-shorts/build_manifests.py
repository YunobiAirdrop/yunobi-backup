#!/usr/bin/env python3
"""Bangun manifest.json untuk rakit_shorts_lm.py dari script.md (caption = [ON SCREEN:])."""
import re, json, os

BASE = "/home/hatch/workspace/youtube-otomatis/lima-misteri/2026-10-16-shorts"

TITLES = {
    "shorts1": "3 Misteri Segitiga Masalembo, Nomor 1 Paling Aneh #misteri #masalembo #shorts",
    "shorts2": "3 Tempat Paling Angker di Indonesia, Nomor 1 Bikin Merinding #misteri #angker #shorts",
    "shorts3": "3 Misteri Candi Kuno, Nomor 1 Tak Terpecahkan #misteri #candi #shorts",
}
OUTS = {
    "shorts1": "lima-misteri-shorts1-masalembo-2026-10-16.mp4",
    "shorts2": "lima-misteri-shorts2-tempat-angker-2026-10-16.mp4",
    "shorts3": "lima-misteri-shorts3-candi-kuno-2026-10-16.mp4",
}

def parse(script_path):
    text = open(script_path).read()
    parts = re.split(r"^## (BEAT \d{3})", text, flags=re.M)
    beats = []
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        cap = ""
        for ln in body.splitlines():
            m = re.match(r"\[ON SCREEN:\s*(.*?)\]", ln.strip())
            if m:
                cap = m.group(1).strip()
                break
        beats.append(cap.replace("\\n", " "))
    return beats

for sub in ["shorts1", "shorts2", "shorts3"]:
    d = os.path.join(BASE, sub)
    caps = parse(os.path.join(d, "script.md"))
    beats = []
    for i, cap in enumerate(caps, 1):
        beats.append({
            "img": os.path.join(d, "img", f"beat-{i:03d}.webp"),
            "audio": os.path.join(d, "audio", f"beat-{i:03d}.mp3"),
            "caption": cap,
        })
    man = {"title": TITLES[sub], "beats": beats,
           "out": os.path.join(BASE, OUTS[sub])}
    # validasi file ada
    for b in beats:
        assert os.path.exists(b["img"]), f"hilang {b['img']}"
        assert os.path.exists(b["audio"]), f"hilang {b['audio']}"
    mp = os.path.join(d, "manifest.json")
    json.dump(man, open(mp, "w"), indent=1)
    print(f"OK {mp} ({len(beats)} beats)")
print("SELESAI")
