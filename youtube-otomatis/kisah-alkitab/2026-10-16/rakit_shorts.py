#!/usr/bin/env python3
"""Rakit YouTube Shorts 9:16 dari footage Pexels + voiceover per-beat.
Pakai: python3 rakit_shorts.py <workdir> <plan.json> <output.mp4>
Semua render via ffmpeg-queue.sh. Output 720x1280, 30fps, <100MB.
plan.json: {"beats":[d1..d5], "segments":[{"file","ss","dur","caption"}], "title","subtitle"}
"""
import subprocess, os, sys, json, shutil

FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H, FPS = 720, 1280, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD GAGAL:", " ".join(cmd[:6]), "...")
        print(r.stderr[-2000:])
        raise SystemExit(1)
    return r

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height,duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    w, h, d = r.stdout.strip().split(",")
    return int(w), int(h), float(d)

def adur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def main():
    workdir, plan_path, out = sys.argv[1:4]
    workdir = os.path.abspath(workdir)
    out = os.path.abspath(out)
    plan = json.load(open(plan_path))
    tmpd = os.path.join(workdir, "build", "_tmp")
    os.makedirs(tmpd, exist_ok=True)

    # 1. gabung voiceover beats
    beats = [os.path.join(workdir, "audio", f"beat{i}.mp3") for i in range(1, 6)]
    lst = os.path.join(tmpd, "beats.txt")
    with open(lst, "w") as f:
        for b in beats:
            f.write(f"file '{b}'\n")
    narration = os.path.join(tmpd, "narration.mp3")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", narration])
    total = adur(narration)
    print(f"narasi: {total:.1f}s")

    # 2. render tiap segmen klip
    segs = []
    for i, s in enumerate(plan["segments"]):
        src = os.path.join(workdir, s["file"])
        w, h, cdur = probe(src)
        dur = float(s["dur"])
        ss = min(float(s.get("ss", 0)), max(0.0, cdur - dur - 0.1))
        seg = os.path.join(tmpd, f"seg{i:02d}.mp4")
        if w * 9 >= h * 16:  # landscape/lebih lebar -> crop tengah vertikal
            vf = (f"crop={w}*9/16/2*2:{h}:(in_w-out_w)/2:0,"
                  f"scale={W}:{H}:flags=lanczos,")
        else:  # portrait -> scale isi penuh
            vf = f"scale={W}:{H}:flags=lanczos,"
        vf += ("eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
               "noise=alls=6:allf=t,"          # film grain halus
               "vignette=PI/5")
        if not (os.path.exists(seg) and adur(seg) >= dur * 0.95):
            run([FQ, "-y", "-ss", f"{ss:.2f}", "-t", f"{dur:.2f}", "-i", src,
                 "-vf", vf, "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                 "-an", seg])
        segs.append(seg)
        print(f"  seg{i:02d} {os.path.basename(src)} ss={ss:.1f} dur={dur:.1f}")

    # 3. concat segmen
    clst = os.path.join(tmpd, "segs.txt")
    with open(clst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    silent = os.path.join(tmpd, "silent.mp4")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", clst, "-c", "copy", silent])

    # 4. overlay: title card + caption per beat (zona aman: y 12%-72% tinggi)
    t = 0.0
    draws = []
    for i, s in enumerate(plan["segments"]):
        d = float(s["dur"])
        cap = s.get("caption", "").replace(":", "\\:").replace("'", "")
        if cap:
            draws.append(
                f"drawtext=fontfile={FONT}:text='{cap}':fontsize=38:"
                f"fontcolor=white:borderw=3:bordercolor=black:"
                f"x=(w-text_w)/2:y=h*0.70:enable='between(t\\,{t:.2f}\\,{t+d:.2f})'")
        t += d
    title = plan.get("title", "").replace("'", "")
    sub = plan.get("subtitle", "").replace("'", "")
    if title:
        draws.append(
            f"drawtext=fontfile={FONT}:text='{title}':fontsize=60:"
            f"fontcolor=white:borderw=4:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.16:enable='between(t\\,0\\,3)'")
    if sub:
        draws.append(
            f"drawtext=fontfile={FONT}:text='{sub}':fontsize=36:"
            f"fontcolor=white:borderw=3:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.16+100:enable='between(t\\,0\\,3)'")
    captioned = os.path.join(tmpd, "captioned.mp4")
    run([FQ, "-y", "-i", silent, "-vf", ",".join(draws),
         "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
         "-an", captioned])

    # 5. mux narasi (+ sfx bila ada)
    sfx = plan.get("sfx")
    if sfx and os.path.exists(os.path.join(workdir, sfx)):
        sfxp = os.path.join(workdir, sfx)
        run([FQ, "-y", "-i", captioned, "-i", narration, "-i", sfxp,
             "-filter_complex",
             "[2:a]volume=0.18,aloop=loop=-1:size=2e9[s];[1:a][s]amix=inputs=2:duration=first[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
             "-b:a", "128k", "-shortest", out])
    else:
        run([FQ, "-y", "-i", captioned, "-i", narration,
             "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", out])

    sz = os.path.getsize(out) / 1e6
    print(f"SELESAI: {out} ({sz:.1f} MB, {adur(out):.1f}s)")

if __name__ == "__main__":
    main()
