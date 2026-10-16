#!/usr/bin/env python3
"""Assembly 3 Shorts Kisah Dharma 2026-10-16.
Format: 1080x1920, klip Pexels vertikal, voiceover Mudiwa, hook text, film grain.
Semua render via ffmpeg-queue.sh.
"""
import os, subprocess, sys

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma/2026-10-16-fix/shorts"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
BD = "/home/hatch/workspace/browser_downloads"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# klip vertikal 1080x1920
V1 = f"{BD}/sess-2829515890/browser-download-20261016T084824.228427179Z-2-14533256_1080_1920_60fps.mp4"  # 14.8s
V2 = f"{BD}/sess-2829515890/browser-download-20261016T085202.887343183Z-3-7895818-hd_1080_1920_30fps.mp4"  # 8.4s
V3 = f"{BD}/sess-2898572595/browser-download-20261016T085800.404210258Z-1-6566693-hd_1080_1920_30fps.mp4"  # 13.6s
V4 = f"{BD}/sess-2898572595/browser-download-20261016T085856.139725425Z-2-14862729-hd_1080_1920_30fps.mp4"  # 15.1s

SHORTS = [
    {"id": "s1-hanuman", "hook": "EKOR DIBAKAR|MALAH TERTAWA!",
     "clips": [(V1, 14.8), (V4, 15.1), (V3, 13.6)]},
    {"id": "s2-jembatan", "hook": "JEMBATAN 48 KM|DALAM 5 HARI!",
     "clips": [(V2, 8.4), (V1, 14.8), (V4, 11.5)]},
    {"id": "s3-ujianapi", "hook": "MASUK API|KELUAR TANPA LUKA!",
     "clips": [(V3, 13.6), (V2, 8.4), (V1, 15.3)]},
]

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:8])); print(r.stderr[-1500:]); sys.exit(1)
    return r

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def build_one(s):
    sid = s["id"]
    audio = f"{BASE}/{sid}.mp3"
    vo_dur = probe(audio)
    outdir = f"{BASE}/{sid}"
    os.makedirs(f"{outdir}/_segs", exist_ok=True)
    final = f"{BASE}/{sid}-1080x1920.mp4"

    # 1. potong segmen vertikal 1080x1920 + grain
    segfiles, acc = [], 0.0
    for idx, (src, take) in enumerate(s["clips"]):
        if acc >= vo_dur:
            break
        take = min(take, vo_dur - acc)
        part = f"{outdir}/_segs/p{idx:02d}.mp4"
        vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              "noise=alls=6:allf=t,vignette=PI/5")
        # hook text di segmen pertama (3 detik pertama)
        if idx == 0 and os.path.exists(FONT):
            lines = s["hook"].split("|")
            for j, ln in enumerate(lines):
                ht = ln.replace(":", "\\:").replace("'", "")
                vf += (f",drawtext=fontfile={FONT}:text='{ht}':fontsize=72:"
                       f"fontcolor=white:borderw=4:bordercolor=black:"
                       f"x=(w-text_w)/2:y=h*0.18+{j*95}")
        if not os.path.exists(part) or probe(part) < take * 0.9:
            run([FQ, "-y", "-i", src, "-t", f"{take:.1f}", "-vf", vf,
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 "-an", part])
        segfiles.append(part); acc += take

    # 2. title card 2 detik (hitam + teks hook)
    hook_plain = s["hook"].replace("|", " ")
    tc_vf = (f"drawtext=fontfile={FONT}:text='{hook_plain}':fontsize=64:"
             f"fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=(h-text_h)/2")
    run([FQ, "-y", "-f", "lavfi", "-i", "color=black:1080x1920:d=2:r=30",
         "-vf", f"{tc_vf},noise=alls=6:allf=t",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-an", f"{outdir}/_segs/title.mp4"])

    # 3. concat
    with open(f"{outdir}/_segs/list.txt", "w") as f:
        f.write(f"file '{outdir}/_segs/title.mp4'\n")
        for p in segfiles:
            f.write(f"file '{p}'\n")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", f"{outdir}/_segs/list.txt",
         "-c", "copy", f"{outdir}/video_nosound.mp4"])

    # 4. mux dengan voiceover
    run([FQ, "-y", "-i", f"{outdir}/video_nosound.mp4", "-i", audio,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
         "-shortest", "-movflags", "+faststart", final])
    sz = os.path.getsize(final)
    print(f"OK {sid}: {probe(final):.1f}s {sz/1048576:.1f}MB -> {final}", flush=True)
    assert sz < 100 * 1048576

if __name__ == "__main__":
    for s in SHORTS:
        build_one(s)
    print("SELESAI 3 shorts", flush=True)
