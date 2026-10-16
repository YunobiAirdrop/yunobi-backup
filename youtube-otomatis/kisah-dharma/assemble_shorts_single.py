#!/usr/bin/env python3
"""Assembly 3 Shorts Kisah Dharma single-pass (1 ffmpeg per short)."""
import os, subprocess, sys

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma/2026-10-16-fix/shorts"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
BD = "/home/hatch/workspace/browser_downloads"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

V1 = f"{BD}/sess-2829515890/browser-download-20261016T084824.228427179Z-2-14533256_1080_1920_60fps.mp4"
V2 = f"{BD}/sess-2829515890/browser-download-20261016T085202.887343183Z-3-7895818-hd_1080_1920_30fps.mp4"
V3 = f"{BD}/sess-2898572595/browser-download-20261016T085800.404210258Z-1-6566693-hd_1080_1920_30fps.mp4"
V4 = f"{BD}/sess-2898572595/browser-download-20261016T085856.139725425Z-2-14862729-hd_1080_1920_30fps.mp4"

SHORTS = [
    {"id": "s1-hanuman", "hook": "EKOR DIBAKAR|MALAH TERTAWA!",
     "clips": [(V1, 14.8), (V4, 15.1), (V3, 13.6)]},
    {"id": "s2-jembatan", "hook": "JEMBATAN 48 KM|DALAM 5 HARI!",
     "clips": [(V2, 8.4), (V1, 14.8), (V4, 11.5)]},
    {"id": "s3-ujianapi", "hook": "MASUK API|KELUAR TANPA LUKA!",
     "clips": [(V3, 13.6), (V2, 8.4), (V1, 15.3)]},
]

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def build_one(s):
    sid = s["id"]
    audio = f"{BASE}/{sid}.mp3"
    vo_dur = probe(audio)
    final = f"{BASE}/{sid}-1080x1920.mp4"

    fc = []
    acc = 0.0
    vlabels = []
    for i, (src, take) in enumerate(s["clips"]):
        if acc >= vo_dur: break
        take = min(take, vo_dur - acc)
        vf = (f"[{i}:v]trim=duration={take:.1f},setpts=PTS-STARTPTS,"
              f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"noise=alls=6:allf=t,vignette=PI/5,setsar=1")
        if i == 0:
            lines = s["hook"].split("|")
            for j, ln in enumerate(lines):
                ht = ln.replace(":", "\\:").replace("'", "")
                vf += (f",drawtext=fontfile={FONT}:text='{ht}':fontsize=72:"
                       f"fontcolor=white:borderw=4:bordercolor=black:"
                       f"x=(w-text_w)/2:y=h*0.18+{j*95}")
        vf += f"[v{i}]"
        fc.append(vf); vlabels.append(f"[v{i}]"); acc += take
    # title card 2s
    hook_plain = s["hook"].replace("|", " ")
    fc.append(f"[{len(s['clips'])}:v]scale=1080:1920,"
              f"drawtext=fontfile={FONT}:text='{hook_plain}':fontsize=64:"
              f"fontcolor=white:borderw=3:bordercolor=black:"
              f"x=(w-text_w)/2:y=(h-text_h)/2,"
              f"noise=alls=6:allf=t,setsar=1[tc]")
    vcat = "[tc]" + "".join(vlabels)
    fc.append(f"{vcat}concat=n={len(vlabels)+1}:v=1:a=0[vout]")

    cmd = [FQ, "-y"]
    for src, _ in s["clips"]:
        cmd += ["-i", src]
    cmd += ["-f", "lavfi", "-i", "color=black:1080x1920:d=2:r=30",
            "-i", audio,
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", f"{len(s['clips'])+1}:a",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-movflags", "+faststart", final]
    print(f"render {sid}...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
    sz = os.path.getsize(final)
    print(f"OK {sid}: {probe(final):.1f}s {sz/1048576:.1f}MB", flush=True)

if __name__ == "__main__":
    for s in SHORTS:
        build_one(s)
    print("SELESAI 3 shorts", flush=True)
