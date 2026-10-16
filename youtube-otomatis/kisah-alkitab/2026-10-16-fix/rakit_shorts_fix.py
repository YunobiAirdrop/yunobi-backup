#!/usr/bin/env python3
"""Rakit Shorts 9:16 dari footage Pexels + voiceover.
Pakai: python3 rakit_shorts_fix.py <workdir> <plan.json> <audio_dir> <audio_prefix> <output.mp4>
Semua render via ffmpeg-queue.sh. Output 1080x1920, 30fps, <100MB.
"""
import subprocess, os, sys, json

FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H, FPS = 1080, 1920, 30

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

def main():
    workdir = os.path.abspath(sys.argv[1])
    plan = json.load(open(sys.argv[2]))
    adir = os.path.abspath(sys.argv[3])
    aprefix = sys.argv[4]
    out = os.path.abspath(sys.argv[5])
    tmpd = os.path.join(workdir, "_tmp_shorts")
    os.makedirs(tmpd, exist_ok=True)

    # 1. gabung audio
    beats = [os.path.join(adir, f"{aprefix}{i}.mp3") for i in range(1, 6)]
    durs = [adur(b) for b in beats]
    print(f"narasi: {sum(durs):.1f}s")
    lst = os.path.join(tmpd, "beats.txt")
    with open(lst, "w") as f:
        for b in beats:
            f.write(f"file '{b}'\n")
    narration = os.path.join(tmpd, "narration.mp3")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", narration])

    # 2. render segmen
    segs = []
    for i, s in enumerate(plan["segments"]):
        src = os.path.join(workdir, s["file"])
        dur = float(s["dur"])
        ss = float(s.get("ss", 0))
        seg = os.path.join(tmpd, f"seg{i:02d}.mp4")
        # crop tengah vertikal 9:16 dari landscape
        vf = (f"crop=ih*9/16:ih:(in_w-out_w)/2:0,"
              f"scale={W}:{H}:flags=lanczos,"
              "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
              "noise=alls=6:allf=t,vignette=PI/5")
        # loop jika klip pendek
        run([FQ, "-y", "-stream_loop", "5", "-ss", f"{ss:.2f}", "-i", src,
             "-vf", vf, "-t", f"{dur:.2f}", "-r", str(FPS),
             "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
             "-an", seg])
        segs.append(seg)
        print(f"  seg{i:02d} dur={dur:.1f}s")

    # 3. concat
    clst = os.path.join(tmpd, "segs.txt")
    with open(clst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    silent = os.path.join(tmpd, "silent.mp4")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", clst, "-c", "copy", silent])

    # 4. overlay caption + title
    t = 0.0
    draws = []
    for i, s in enumerate(plan["segments"]):
        d = float(s["dur"])
        cap = s.get("caption", "").replace(":", "\\:").replace("'", "")
        if cap:
            draws.append(
                f"drawtext=fontfile={FONT}:text='{cap}':fontsize=52:"
                f"fontcolor=white:borderw=4:bordercolor=black:"
                f"x=(w-text_w)/2:y=h*0.70:enable='between(t\\,{t:.2f}\\,{t+d:.2f})'")
        t += d
    title = plan.get("title", "").replace("'", "")
    sub = plan.get("subtitle", "").replace("'", "")
    if title:
        draws.append(
            f"drawtext=fontfile={FONT}:text='{title}':fontsize=64:"
            f"fontcolor=white:borderw=5:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.35:enable='between(t\\,0\\,4)'")
    if sub:
        draws.append(
            f"drawtext=fontfile={FONT}:text='{sub}':fontsize=40:"
            f"fontcolor=yellow:borderw=3:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.42:enable='between(t\\,0\\,4)'")
    vf_all = ",".join(draws)

    run([FQ, "-y", "-i", silent, "-i", narration,
         "-vf", vf_all,
         "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "128k", "-shortest",
         out])
    print(f"SELESAI: {out} ({adur(out):.1f}s, {os.path.getsize(out)/1e6:.1f}MB)")

if __name__ == "__main__":
    main()
