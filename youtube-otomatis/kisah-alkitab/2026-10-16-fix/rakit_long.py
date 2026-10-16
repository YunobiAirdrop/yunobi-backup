#!/usr/bin/env python3
"""Rakit video LONG 16:9 dari footage Pexels + voiceover per-beat.
Pakai: python3 rakit_long.py <workdir> <output.mp4>
Semua render via ffmpeg-queue.sh. Output 1280x720, 30fps, <100MB.
"""
import subprocess, os, sys, json, glob

FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H, FPS = 1280, 720, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD GAGAL:", " ".join(cmd[:6]), "...")
        print(r.stderr[-2000:])
        raise SystemExit(1)
    return r

def adur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def vdur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip().split(",")[0])
    except:
        return adur(path)

# Beat -> (clip, caption). Clips: existing 8 + new 3 (absolute paths, resolved at runtime)
def _clips(base):
    return {
        "d1": os.path.join(base, "../2026-10-16/footage/clip1.mp4"),
        "d2": os.path.join(base, "../2026-10-16/footage/clip2.mp4"),
        "d3": os.path.join(base, "../2026-10-16/footage/clip3.mp4"),
        "d4": os.path.join(base, "../2026-10-16/footage/clip4.mp4"),
        "d5": os.path.join(base, "../2026-10-16/footage/clip5.mp4"),
        "d6": os.path.join(base, "../2026-10-16/footage/clip6.mp4"),
        "d7": os.path.join(base, "../2026-10-16/footage/clip7.mp4"),
        "d8": os.path.join(base, "../2026-10-16/footage/clip8.mp4"),
        "stars": os.path.join(base, "footage/stars_night.mp4"),
        "fire": os.path.join(base, "footage/fire_blaze.mp4"),
        "ocean": os.path.join(base, "footage/ocean_storm.mp4"),
    }
CLIPS = None  # diisi di main()

# 26 beats: (clip_key, ss_offset, caption)
PLAN = [
    ("d1", 2.0, "ANAK DIKORBANKAN?!"),
    ("d2", 3.0, "TINGGALKAN SEMUANYA"),
    ("d3", 1.0, "BERJALAN TANPA PETA"),
    ("stars", 0.5, "SEBANYAK BINTANG"),
    ("d4", 0.5, "25 TAHUN MENUNGGU"),
    ("d5", 5.0, "ISHAK LAHIR!"),
    ("d6", 2.0, "KORBANKAN ISHAK?!"),
    ("d7", 1.0, "3 HARI PERJALANAN"),
    ("d8", 3.0, "ALLAH MENYEDIAKAN"),
    ("d1", 7.0, "PISAU TERANGKAT"),
    ("d5", 12.0, "JANGAN BUNUH DIA!"),
    ("d3", 6.0, "IMAN TERUJI"),
    ("d2", 8.0, "ANAK PERJANJIAN"),
    ("d4", 4.0, "TAAT TANPA TAHU"),
    ("stars", 3.0, "BANGKIT DARI MATI"),
    ("d6", 8.0, "GUNUNG MORIA"),
    ("d7", 5.0, "IMAN = TAAT"),
    ("d8", 7.0, "KRISTUS PENGGENAP"),
    ("d1", 4.0, "TUHAN MENYEDIAKAN"),
    ("d5", 18.0, "JANJI DIGENAPI"),
    ("stars", 5.0, "YAHWEH YIREH"),
    ("d2", 12.0, "IMAN SARA"),
    ("d3", 9.0, "TUHAN DIKENAL"),
    ("d4", 6.0, "TAAT DIHARGAI"),
    ("d6", 12.0, "LEPASKAN DENGAN IMAN"),
    ("d8", 10.0, "TULIS AMIN!"),
]

CAPTIONS = [c for _, _, c in PLAN]

def main():
    workdir = os.path.abspath(sys.argv[1])
    out = os.path.abspath(sys.argv[2])
    global CLIPS
    CLIPS = _clips(workdir)
    os.chdir(workdir)
    tmpd = os.path.join(workdir, "_tmp_long")
    os.makedirs(tmpd, exist_ok=True)

    # 1. kumpulkan durasi beats
    beats = sorted(glob.glob(os.path.join(workdir, "audio/long/beat*.mp3")),
                   key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x)))))
    durs = [adur(b) for b in beats]
    print(f"{len(beats)} beats, total {sum(durs):.1f}s = {sum(durs)/60:.2f} mnt")
    assert len(beats) == len(PLAN), f"beats {len(beats)} != plan {len(PLAN)}"

    # 2. gabung audio
    lst = os.path.join(tmpd, "beats.txt")
    with open(lst, "w") as f:
        for b in beats:
            f.write(f"file '{b}'\n")
    narration = os.path.join(tmpd, "narration.mp3")
    if not os.path.exists(narration):
        run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", narration])

    # 3. render segmen video per beat
    segs = []
    for i, (ckey, ss, cap) in enumerate(PLAN):
        src = CLIPS[ckey]
        cdur = vdur(src)
        dur = durs[i]
        ss = min(ss, max(0.0, cdur - dur - 0.1))
        # jika klip lebih pendek dari beat, loop
        seg = os.path.join(tmpd, f"seg{i:02d}.mp4")
        vf = ("scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
              "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
              "noise=alls=6:allf=t,vignette=PI/5")
        if not (os.path.exists(seg) and adur(seg) >= dur * 0.95):
            if cdur >= dur:
                run([FQ, "-y", "-ss", f"{ss:.2f}", "-t", f"{dur:.2f}", "-i", src,
                     "-vf", vf, "-r", str(FPS),
                     "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                     "-an", seg])
            else:
                # loop klip pendek
                run([FQ, "-y", "-stream_loop", "3", "-ss", f"{ss:.2f}", "-i", src,
                     "-vf", vf, "-t", f"{dur:.2f}", "-r", str(FPS),
                     "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                     "-an", seg])
        segs.append(seg)
        if i % 5 == 0:
            print(f"  seg{i:02d} {ckey} dur={dur:.1f}s")

    # 4. concat segmen
    clst = os.path.join(tmpd, "segs.txt")
    with open(clst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    silent = os.path.join(tmpd, "silent.mp4")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", clst, "-c", "copy", silent])

    # 5. overlay caption + title card
    t = 0.0
    draws = []
    for i, cap in enumerate(CAPTIONS):
        d = durs[i]
        c = cap.replace(":", "\\:").replace("'", "")
        if c:
            draws.append(
                f"drawtext=fontfile={FONT}:text='{c}':fontsize=42:"
                f"fontcolor=white:borderw=3:bordercolor=black:"
                f"x=(w-text_w)/2:y=h*0.78:enable='between(t\\,{t:.2f}\\,{t+d:.2f})'")
        t += d
    # title card di awal (4 detik)
    draws.append(
        f"drawtext=fontfile={FONT}:text='ABRAHAM\\: UJIAN TERBERAT':fontsize=54:"
        f"fontcolor=white:borderw=4:bordercolor=black:"
        f"x=(w-text_w)/2:y=(h-text_h)/2-30:enable='between(t\\,0\\,4)'")
    draws.append(
        f"drawtext=fontfile={FONT}:text='Kejadian 22':fontsize=36:"
        f"fontcolor=yellow:borderw=3:bordercolor=black:"
        f"x=(w-text_w)/2:y=(h-text_h)/2+40:enable='between(t\\,0\\,4)'")
    vf_all = ",".join(draws)

    # 6. mux audio + overlay
    run([FQ, "-y", "-i", silent, "-i", narration,
         "-vf", vf_all,
         "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "128k", "-shortest",
         out])
    print(f"SELESAI: {out} ({adur(out):.1f}s, {os.path.getsize(out)/1e6:.1f}MB)")

if __name__ == "__main__":
    main()
