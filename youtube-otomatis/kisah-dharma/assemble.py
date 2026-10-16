#!/usr/bin/env python3
"""
Assembly Kisah Dharma 2026-10-16 (LONG).
- Mengunduh klip Pexels dari CLIPS (url, durasi_estimasi, label)
- Verifikasi frame: simpan 3 frame per klip ke frames/ untuk inspeksi manual
- Segmen per beat: pilih klip menutupi durasi voiceover beat, scale 1280x720,
  film grain halus, audio ambien asli klip volume rendah
- Title card 4 detik di depan (zoom halus)
- Semua render via ~/workspace/youtube-otomatis/ffmpeg-queue.sh
"""
import json, os, subprocess, sys, urllib.request

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

# DIISI dari hasil child agent (url mp4 langsung Pexels, durasi detik, label isi)
CLIPS = [
    # ("https://videos.pexels.com/video-files/...mp4", 20, "lilin"),
]

# beat -> indeks klip (boleh dipakai 2x bila klip bersih < 18)
BEAT_CLIPS = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

def run(cmd, **kw):
    print("+", " ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
    return r

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def download():
    os.makedirs(f"{BASE}/clips", exist_ok=True)
    for i, (url, _, label) in enumerate(CLIPS):
        out = f"{BASE}/clips/c{i:02d}_{label}.mp4"
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            print(f"skip {out} (ada)")
            continue
        print(f"download {label} ...")
        urllib.request.urlretrieve(url, out)
        print(" ", os.path.getsize(out), "bytes")

def verify_frames():
    """Ekstrak 3 frame per klip untuk inspeksi visual manual."""
    os.makedirs(f"{BASE}/frames", exist_ok=True)
    for i, (_, dur, label) in enumerate(CLIPS):
        src = f"{BASE}/clips/c{i:02d}_{label}.mp4"
        d = probe(src)
        for k, frac in enumerate((0.15, 0.5, 0.85)):
            t = d * frac
            out = f"{BASE}/frames/c{i:02d}_{label}_f{k}.jpg"
            run([FQ, "-y", "-ss", f"{t:.1f}", "-i", src, "-frames:v", "1",
                 "-q:v", "4", out])

def build():
    # 1. durasi tiap beat
    beats = []
    for i in range(1, 9):
        beats.append(probe(f"{BASE}/audio/beat{i}.mp3"))
    print("beat durations:", [round(b, 1) for b in beats],
          "total:", round(sum(beats), 1))

    # 2. susun segmen video per beat
    seg = 0
    segfiles = []
    for bi, dur in enumerate(beats, 1):
        need = dur + 0.6
        acc = 0.0
        parts = []
        for ci in BEAT_CLIPS[bi]:
            if acc >= need:
                break
            url, cdur, label = CLIPS[ci]
            src = f"{BASE}/clips/c{ci:02d}_{label}.mp4"
            take = min(cdur, need - acc)
            if take < 3:
                continue
            part = f"{BASE}/seg_{seg:02d}.mp4"
            # scale+crop 1280x720, grain halus, ambil 'take' detik dari tengah klip
            start = max(0, (cdur - take) / 2)
            run([FQ, "-y", "-ss", f"{start:.1f}", "-i", src, "-t", f"{take:.1f}",
                 "-vf", "scale=1280:720:force_original_aspect_ratio=increase,"
                        "crop=1280:720,noise=alls=6:allf=t",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 "-c:a", "aac", "-b:a", "96k", part])
            parts.append(part); acc += take; seg += 1
        if acc < need - 1:
            print(f"PERINGATAN beat {bi}: klip kurang ({acc:.1f}/{need:.1f})"); sys.exit(1)
        segfiles.extend(parts)

    # 3. title card 4 detik dengan zoom halus
    run([FQ, "-y", "-loop", "1", "-i", f"{BASE}/titlecard.png",
         "-vf", "scale=1280:720,zoompan=z='1+0.02*on':d=100:s=1280x720:fps=25,"
                "noise=alls=6:allf=t",
         "-t", "4", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-an", f"{BASE}/seg_title.mp4"])

    # 4. concat semua segmen video
    with open(f"{BASE}/concat_list.txt", "w") as f:
        f.write(f"file '{BASE}/seg_title.mp4'\n")
        for s in segfiles:
            f.write(f"file '{s}'\n")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", f"{BASE}/concat_list.txt",
         "-c", "copy", f"{BASE}/video_nosound.mp4"])

    # 5. audio: gabung beat + jeda 0.8s, + ambien dari klip (vol 0.08)
    vdur = probe(f"{BASE}/video_nosound.mp4")
    # rangkai voiceover
    run([FQ, "-y",
         "-i", f"{BASE}/audio/beat1.mp3", "-i", f"{BASE}/audio/beat2.mp3",
         "-i", f"{BASE}/audio/beat3.mp3", "-i", f"{BASE}/audio/beat4.mp3",
         "-i", f"{BASE}/audio/beat5.mp3", "-i", f"{BASE}/audio/beat6.mp3",
         "-i", f"{BASE}/audio/beat7.mp3", "-i", f"{BASE}/audio/beat8.mp3",
         "-filter_complex",
         "[0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a]concat=n=8:v=0:a=1,"
         "aresample=44100,adelay=4000|4000[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "128k",
         f"{BASE}/vo_full.m4a"])
    # ambien: audio asli klip-klip yang dipakai, volume rendah, loop hingga durasi video
    used = sorted({c for lst in BEAT_CLIPS.values() for c in lst})
    inputs, amaps, vols = [], [], []
    for j, ci in enumerate(used):
        _, _, label = CLIPS[ci]
        inputs += ["-i", f"{BASE}/clips/c{ci:02d}_{label}.mp4"]
        amaps.append(f"[{j}:a]volume=0.08,aresample=44100,apad[a{j}]")
        vols.append(f"[a{j}]")
    fc = ";".join(amaps) + ";" + "".join(vols) + \
         f"amix=inputs={len(used)}:normalize=0,aloop=loop=-1:size=2e9,atrim=0:{vdur:.1f}[amb]"
    run([FQ, "-y"] + inputs + ["-filter_complex", fc, "-map", "[amb]",
         "-c:a", "aac", "-b:a", "96k", f"{BASE}/amb_full.m4a"])
    # 6. mux final: video + VO + ambien, bitrate dinamis target ~88MB (<100MB)
    vo_dur = probe(f"{BASE}/vo_full.m4a")
    target_bytes = 88 * 1024 * 1024
    vbr = max(600, int((target_bytes * 8 / vo_dur - 128000) / 1000))
    print(f"durasi VO {vo_dur:.1f}s -> video bitrate {vbr}k")
    run([FQ, "-y", "-i", f"{BASE}/video_nosound.mp4",
         "-i", f"{BASE}/vo_full.m4a", "-i", f"{BASE}/amb_full.m4a",
         "-filter_complex", "[1:a][2:a]amix=inputs=2:normalize=0[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{vbr}k",
         "-maxrate", f"{int(vbr*1.4)}k", "-bufsize", f"{vbr*2}k",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", f"{BASE}/kisahdharma-2026-10-16.mp4"])
    print("FINAL:", f"{BASE}/kisahdharma-2026-10-16.mp4",
          os.path.getsize(f"{BASE}/kisahdharma-2026-10-16.mp4"), "bytes")

if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("all", "download"):
        download()
    if step in ("all", "verify"):
        verify_frames()
    if step in ("all", "build"):
        build()
