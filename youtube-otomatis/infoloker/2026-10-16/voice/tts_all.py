#!/usr/bin/env python3
"""TTS semua beat via Mudiwa, paralel. Baca voice/beats.json, tulis voice/<id>.mp3."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = "/home/hatch/workspace/youtube-otomatis/infoloker/2026-10-16"
VD = os.path.join(ROOT, "voice")
TTS = "/opt/hatch/bin/tts"

beats = json.load(open(os.path.join(VD, "beats.json")))
jobs = [(bid, txt) for vid in beats.values() for bid, txt in vid.items()]

def one(job):
    bid, txt = job
    out = os.path.join(VD, f"{bid}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return (bid, "skip")
    r = subprocess.run([TTS, "speak", "--text-stdin", "--voice", "mudiwa",
                        "--language", "id", "--speed", "95", "--output", out],
                       input=txt.encode("utf-8"), capture_output=True)
    if r.returncode != 0 or not os.path.exists(out):
        return (bid, "GAGAL: " + r.stderr.decode()[-300:])
    return (bid, "ok")

fails = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for bid, st in ex.map(one, jobs):
        print(bid, st, flush=True)
        if st != "ok" and st != "skip":
            fails.append((bid, st))

print(f"\nSELESAI: {len(jobs)-len(fails)}/{len(jobs)} OK, gagal: {len(fails)}")
sys.exit(1 if fails else 0)
