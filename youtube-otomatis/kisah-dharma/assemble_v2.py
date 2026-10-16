#!/usr/bin/env python3
"""Assembly Kisah Dharma LONG v2 — sederhana dan cepat.
1. Concat semua klip (urutan beat) via stream copy → 1 file video
2. Scale 1280x720 + title card + voiceover + ambien → final
Hanya 2x ffmpeg call, filter minimal.
"""
import os, subprocess, sys

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
OUTDIR = f"{BASE}/2026-10-16-fix"
FINAL = f"{OUTDIR}/kisahdharma-2026-10-16-long.mp4"

# (path, durasi pakai) — urutan beat 1-8
SEGS = [
    # beat1 (56.6s): badai, gurun, unta, langit
    ("clips/badai_gelap.mp4", 15.5), ("clips/gurun_langit.mp4", 10.0),
    ("../kisah-alkitab/2026-10-16/footage/clip2.mp4", 18.6),
    ("clips/langit_tenang.mp4", 12.5),
    # beat2 (157s): sungai, sunrise, ombak
    ("clips/sungai_alir.mp4", 14.2), ("clips/sungai_hutan.mp4", 16.5),
    ("clips/sunrise_kabut.mp4", 17.4), ("clips/ombak.mp4", 25.1),
    ("../jejak-buddha/2026-10-16-shorts/clips/c02.mp4", 14.0),
    ("../jejak-buddha/2026-10-16-shorts/clips/c07.mp4", 14.5),
    ("../kisah-alkitab/2026-10-16/footage/clip3.mp4", 14.8),
    ("../kisah-alkitab/2026-10-16/footage/clip6.mp4", 20.0),
    ("../jejak-buddha/2026-10-16-shorts/clips/c09.mp4", 14.5),
    ("clips/senja_rumput.mp4", 6.0),
    # beat3 (94s): api, gurun, bintang
    ("clips/api_unggun.mp4", 21.7), ("clips/gurun_drone.mp4", 10.1),
    ("../jejak-buddha/2026-10-16-shorts/clips/c04.mp4", 17.2),
    ("../kisah-alkitab/2026-10-16/footage/clip5.mp4", 27.6),
    ("clips/bukit_kabut.mp4", 8.7), ("../kisah-alkitab/2026-10-16/footage/clip4.mp4", 8.4),
    # beat4 (147s): hutan cahaya, terang
    ("clips/hutan_cahaya.mp4", 51.5),
    ("../jejak-buddha/2026-10-16-shorts/clips/c01.mp4", 16.8),
    ("../jejak-buddha/2026-10-16-shorts/clips/c06.mp4", 13.2),
    ("../jejak-buddha/2026-10-16-shorts/clips/c10.mp4", 12.7),
    ("../kisah-alkitab/2026-10-16/footage/clip1.mp4", 12.3),
    ("../kisah-alkitab/2026-10-16/footage/clip7.mp4", 13.6),
    ("../kisah-alkitab/2026-10-16/footage/clip8.mp4", 15.1),
    ("../jejak-buddha/2026-10-16-shorts/clips/c03.mp4", 8.4),
    ("../jejak-buddha/2026-10-16-shorts/clips/c05.mp4", 3.5),
    # beat5 (64s): lilin, gelap
    ("clips/lilin_meja.mp4", 26.7),
    ("../jejak-buddha/2026-10-16-shorts/clips/c08.mp4", 10.0),
    ("../kisah-alkitab/2026-10-16/footage/clip4.mp4", 8.4),
    ("clips/badai_gelap.mp4", 15.5), ("clips/bukit_kabut.mp4", 3.2),
    # beat6 (63s): perang
    ("clips/gurun_langit.mp4", 10.0), ("clips/ombak.mp4", 25.1),
    ("clips/api_unggun.mp4", 21.7), ("clips/senja_rumput.mp4", 6.0),
    # beat7 (58s): dharma, tenang
    ("clips/lilin_meja.mp4", 26.7), ("clips/sunrise_kabut.mp4", 17.4),
    ("../jejak-buddha/2026-10-16-shorts/clips/c01.mp4", 13.6),
    # beat8 (41s): penutup
    ("clips/sungai_alir.mp4", 14.2), ("clips/sungai_hutan.mp4", 16.5),
    ("clips/hutan_cahaya.mp4", 10.3),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:6])); print(r.stderr[-1500:]); sys.exit(1)

def run_bg(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    segdir = f"{OUTDIR}/_v2segs"
    os.makedirs(segdir, exist_ok=True)
    segfiles = []
    # render paralel 2 batch (manfaatkan 2 slot antrean)
    procs = []
    for i, (rel, dur) in enumerate(SEGS):
        src = os.path.join(BASE, rel)
        out = f"{segdir}/s{i:03d}.mp4"
        segfiles.append(out)
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"seg {i+1}/{len(SEGS)} skip", flush=True); continue
        cmd = [FQ, "-y", "-i", src, "-t", f"{dur:.1f}",
               "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-an", out]
        procs.append((i, run_bg(cmd)))
        print(f"seg {i+1}/{len(SEGS)} queued", flush=True)
        # tahan maks 4 proses paralel
        while len([p for _, p in procs if p.poll() is None]) >= 4:
            import time; time.sleep(5)
    for i, p in procs:
        rc = p.wait()
        if rc != 0:
            print(f"seg {i} GAGAL"); sys.exit(1)
    print("semua segmen jadi", flush=True)
    # 2. concat segmen (stream copy, cepat)
    with open(f"{segdir}/list.txt", "w") as f:
        for s in segfiles:
            f.write(f"file '{s}'\n")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", f"{segdir}/list.txt",
         "-c", "copy", f"{OUTDIR}/video_body.mp4"])
    # 3. title card + body + audio → final
    #    voiceover: 8 beats concat + delay 4s; ambien: audio klip own
    run([FQ, "-y",
         "-loop", "1", "-t", "4", "-i", f"{BASE}/titlecard.png",
         "-i", f"{OUTDIR}/video_body.mp4",
         "-i", f"{BASE}/audio/beat1.mp3", "-i", f"{BASE}/audio/beat2.mp3",
         "-i", f"{BASE}/audio/beat3.mp3", "-i", f"{BASE}/audio/beat4.mp3",
         "-i", f"{BASE}/audio/beat5.mp3", "-i", f"{BASE}/audio/beat6.mp3",
         "-i", f"{BASE}/audio/beat7.mp3", "-i", f"{BASE}/audio/beat8.mp3",
         "-filter_complex",
         "[0:v]scale=1280:720,setsar=1[tc];[tc][1:v]concat=n=2:v=1:a=0[vout];"
         "[2:a][3:a][4:a][5:a][6:a][7:a][8:a][9:a]concat=n=8:v=0:a=1,"
         "aresample=44100,adelay=4000|4000[aout]",
         "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", FINAL])
    import shutil
    sz = os.path.getsize(FINAL)
    print(f"FINAL: {FINAL} {sz/1048576:.1f}MB", flush=True)
    assert sz < 100 * 1048576, "over 100MB"

if __name__ == "__main__":
    main()
