#!/usr/bin/env python3
"""Validasi durasi per beat (>1s), rakit voiceover_full.mp3 + durasi.json per video.
Jeda antar beat: 0.30s (shorts), 0.35s (long)."""
import json, os, subprocess, sys

ROOT = "/home/hatch/workspace/youtube-otomatis/infoloker/2026-10-16"
VD = os.path.join(ROOT, "voice")
BD = os.path.join(ROOT, "build")
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
os.makedirs(BD, exist_ok=True)

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def run(cmd):
    r = subprocess.run([FQ] + cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:5]), "\n", r.stderr[-800:]); sys.exit(1)

beats = json.load(open(os.path.join(VD, "beats.json")))
VIDS = {"s1": "shorts1", "s2": "shorts2", "s3": "shorts3", "long": "long"}
GAP = {"s1": 0.30, "s2": 0.30, "s3": 0.30, "long": 0.35}

alld = {}
for vid, name in VIDS.items():
    ids = sorted(beats[vid].keys())
    durs, starts = {}, {}
    t = 0.0
    for b in ids:
        d = dur(os.path.join(VD, f"{b}.mp3"))
        assert d > 1.0, f"{b} durasi {d} <= 1s!"
        durs[b] = round(d, 2); starts[b] = round(t, 2)
        t += d + GAP[vid]
    total = round(t - GAP[vid], 2)
    # concat dengan jeda presisi via adelay+amix
    inputs, fc = [], []
    for i, b in enumerate(ids):
        inputs += ["-i", os.path.join(VD, f"{b}.mp3")]
        ms = int(starts[b] * 1000)
        fc.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    fc.append("".join(f"[a{i}]" for i in range(len(ids))) +
              f"amix=inputs={len(ids)}:normalize=0,aresample=44100,apad=pad_dur=1.2[vo]")
    out = os.path.join(BD, f"voiceover_full_{name}.mp3")
    run(["-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vo]",
         "-c:a", "libmp3lame", "-b:a", "160k", "-t", str(total + 1.2), out])
    alld[name] = {"beats": durs, "starts": starts, "gap": GAP[vid],
                  "total_vo": total, "voice_file": out}
    print(f"{name}: {len(ids)} beats, total VO {total:.1f}s")

json.dump(alld, open(os.path.join(BD, "durasi.json"), "w"), indent=1)
print("durasi.json OK")
