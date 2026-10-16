#!/usr/bin/env python3
"""Assembly Kisah Dharma LONG single-pass via filter_complex.
SATU pemanggilan ffmpeg untuk seluruh video (hemat antrean).
"""
import os, subprocess, sys

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
JB = "/home/hatch/workspace/youtube-otomatis/jejak-buddha/2026-10-16-shorts/clips"
KA = "/home/hatch/workspace/youtube-otomatis/kisah-alkitab/2026-10-16/footage"
OUT = f"{BASE}/2026-10-16-fix/kisahdharma-2026-10-16-long.mp4"

CLIPS = [
    f"{BASE}/clips/api_unggun.mp4", f"{BASE}/clips/badai_gelap.mp4",
    f"{BASE}/clips/bukit_kabut.mp4", f"{BASE}/clips/gunung_kabut.mp4",
    f"{BASE}/clips/gurun_drone.mp4", f"{BASE}/clips/gurun_langit.mp4",
    f"{BASE}/clips/hutan_cahaya.mp4", f"{BASE}/clips/langit_tenang.mp4",
    f"{BASE}/clips/lilin_meja.mp4", f"{BASE}/clips/ombak.mp4",
    f"{BASE}/clips/senja_rumput.mp4", f"{BASE}/clips/sungai_alir.mp4",
    f"{BASE}/clips/sungai_hutan.mp4", f"{BASE}/clips/sunrise_kabut.mp4",
    f"{JB}/c01.mp4", f"{JB}/c02.mp4", f"{JB}/c03.mp4", f"{JB}/c04.mp4",
    f"{JB}/c05.mp4", f"{JB}/c06.mp4", f"{JB}/c07.mp4", f"{JB}/c08.mp4",
    f"{JB}/c09.mp4", f"{JB}/c10.mp4",
    f"{KA}/clip1.mp4", f"{KA}/clip2.mp4", f"{KA}/clip3.mp4", f"{KA}/clip4.mp4",
    f"{KA}/clip5.mp4", f"{KA}/clip6.mp4", f"{KA}/clip7.mp4", f"{KA}/clip8.mp4",
]
CLIP_DUR = [21.7,15.5,8.7,13.4,10.1,10.0,51.5,15.7,26.7,25.1,9.5,14.2,16.5,17.4,
            16.8,14.0,8.4,17.2,8.3,13.2,14.5,10.0,14.5,12.7,
            12.3,18.6,14.8,8.4,27.6,20.0,13.6,15.1]

BEAT_CLIPS = {
    1: [1, 5, 25, 7],
    2: [11, 12, 13, 9, 15, 20, 26, 29, 22, 10],
    3: [0, 4, 17, 28, 2, 27, 3],
    4: [6, 14, 19, 23, 24, 30, 31, 16, 18],
    5: [8, 21, 27, 1, 2],
    6: [5, 9, 0, 10, 3],
    7: [8, 13, 14, 7],
    8: [11, 12, 6],
}
BEAT_DUR = [55.992, 156.408, 93.528, 146.52, 63.192, 62.208, 57.072, 40.392]

def build_segments():
    """Return list of (clip_idx, start, dur, flip)."""
    segs, used = [], {}
    for bi in range(1, 9):
        need = BEAT_DUR[bi-1] + 0.6
        acc = 0.0
        for ci in BEAT_CLIPS[bi]:
            if acc >= need: break
            cdur = CLIP_DUR[ci]
            take = min(cdur, need - acc)
            if take < 2.5: continue
            n = used.get(ci, 0); used[ci] = n + 1
            if n == 0:
                start, flip = max(0, (cdur - take) / 2), False
            else:
                start, flip = max(0, (cdur - take) * (0.15 + 0.35 * (n % 3))), True
            segs.append((ci, start, take, flip))
            acc += take
        assert acc >= need - 1, f"beat {bi} kurang"
    return segs

def main():
    segs = build_segments()
    total_seg = sum(s[2] for s in segs)
    vdur = 4.0 + total_seg
    print(f"{len(segs)} segmen, video {vdur:.0f}s", flush=True)

    # --- filter_complex ---
    fc = []
    for i, (ci, st, du, flip) in enumerate(segs):
        f = f"[{ci}:v]trim=start={st:.1f}:duration={du:.1f},setpts=PTS-STARTPTS,"
        if flip: f += "hflip,"
        f += ("scale=1280:720:force_original_aspect_ratio=increase,"
              "crop=1280:720,setsar=1"
              f"[s{i}]")
        fc.append(f)
    # title card
    fc.append("[32:v]scale=1280:720,zoompan=z='1+0.02*on':d=100:s=1280x720:fps=25,"
              "noise=alls=6:allf=t,setsar=1[tc]")
    # concat video
    vcat = "".join(f"[s{i}]" for i in range(len(segs)))
    fc.append(f"[tc]{vcat}concat=n={len(segs)+1}:v=1:a=0[vout]")
    # voiceover
    vo_in = "".join(f"[{33+i}:a]" for i in range(8))
    fc.append(f"{vo_in}concat=n=8:v=0:a=1,aresample=44100,adelay=4000|4000[vo]")
    # ambient (hanya klip yang punya audio stream)
    amb_idx = [0, 1, 9, 11, 12]
    for j, ci in enumerate(amb_idx):
        fc.append(f"[{ci}:a]volume=0.06,aresample=44100,apad[am{j}]")
    amix_in = "".join(f"[am{j}]" for j in range(len(amb_idx)))
    fc.append(f"{amix_in}amix=inputs={len(amb_idx)}:normalize=0,"
              f"atrim=0:{vdur:.1f},asetpts=PTS-STARTPTS[amb]")
    fc.append("[vo][amb]amix=inputs=2:normalize=0[aout]")
    filter_complex = ";".join(fc)

    # --- inputs ---
    cmd = [FQ, "-y"]
    for c in CLIPS:
        cmd += ["-i", c]
    cmd += ["-loop", "1", "-t", "4", "-i", f"{BASE}/titlecard.png"]
    for i in range(1, 9):
        cmd += ["-i", f"{BASE}/audio/beat{i}.mp3"]
    vo_dur = sum(BEAT_DUR) + 4.0
    vbr = max(600, int((88 * 1048576 * 8 / vo_dur - 128000) / 1000))
    cmd += ["-filter_complex", filter_complex,
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{vbr}k",
            "-maxrate", f"{int(vbr*1.4)}k", "-bufsize", f"{vbr*2}k",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            "-shortest", OUT]
    print(f"vbr {vbr}k, menjalankan...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
    sz = os.path.getsize(OUT)
    print(f"FINAL: {OUT} {sz/1048576:.1f}MB", flush=True)
    assert sz < 100 * 1048576

if __name__ == "__main__":
    main()
