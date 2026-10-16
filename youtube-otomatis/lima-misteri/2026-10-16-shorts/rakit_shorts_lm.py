#!/usr/bin/env python3
"""Rakit YouTube Shorts 1080x1920 utk Lima Misteri: N gambar (Ken Burns portrait)
+ voiceover per-beat + film grain + grading + caption on-screen per beat + tag channel.
SEMUA ffmpeg via ffmpeg-queue.sh. Jangan pakai bare ffmpeg.

Penggunaan: python3 rakit_shorts_st.py <manifest.json>
  manifest: {"title": "...",
             "beats": [{"img": "...", "audio": "...", "caption": "BARIS1\\nBARIS2"}, ...],
             "out": "<path mp4 final>"}
"""
import subprocess, os, sys, json, shutil

FFQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 1080, 1920

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")

def kenburns(img, seg_dur, idx, caption, out):
    total_frames = max(1, int(seg_dur * 30))
    mode = idx % 4
    if mode == 0:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    elif mode == 1:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='(iw-iw/zoom)*on/{total_frames}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    elif mode == 2:
        zp = f"zoompan=z='max(1.18-0.0015*on,1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    else:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom/2)':s={W}x{H}:fps=30"
    cap = esc(caption)
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{zp},"
        "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
        "noise=alls=6:allf=t,"
        "vignette=PI/5,"
        f"drawtext=fontfile={FONT}:text='{cap}':fontcolor=white:fontsize=64:"
        "borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-430:line_spacing=12,"
        "drawtext=fontfile=" + FONT + ":text='LIMA MISTERI':fontcolor=white@0.85:fontsize=34:"
        "borderw=2:bordercolor=black@0.7:x=40:y=260"
    )
    r = subprocess.run([FFQ, "-y", "-loop", "1", "-i", img,
                        "-vf", vf, "-t", f"{seg_dur:.2f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                        "-pix_fmt", "yuv420p", "-r", "30", out],
                       capture_output=True, text=True)
    return r.returncode == 0

def main():
    man_path = os.path.abspath(sys.argv[1])
    man = json.load(open(man_path))
    beats, out = man["beats"], man["out"]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    # tmp dir unik per manifest (bukan per outdir) — anti tabrakan saat
    # beberapa shorts dirender paralel ke outdir yang sama
    tmpd = os.path.join(os.path.dirname(man_path), "_tmp_segs")
    os.makedirs(tmpd, exist_ok=True)

    seg_files, aud_files = [], []
    for i, b in enumerate(beats):
        d = dur(b["audio"])
        if d <= 0:
            print(f"GAGAL: audio beat-{i+1} tidak terbaca"); sys.exit(1)
        seg_d = d + 0.35
        aud_files.append(b["audio"])
        s = os.path.join(tmpd, f"s{i:03d}.mp4")
        if not (os.path.exists(s) and dur(s) >= seg_d * 0.9):
            if os.path.exists(s):
                os.remove(s)
            print(f"  render s{i:03d} ({seg_d:.1f}s)...", flush=True)
            ok = False
            for _ in range(2):
                if kenburns(b["img"], seg_d, i, b["caption"], s) and dur(s) >= seg_d * 0.9:
                    ok = True
                    break
                print(f"    retry s{i:03d}", flush=True)
            if not ok:
                print(f"GAGAL: s{i:03d}"); sys.exit(1)
        seg_files.append(s)

    lst = os.path.join(tmpd, "list.txt")
    with open(lst, "w") as f:
        for s in seg_files:
            f.write(f"file '{os.path.abspath(s)}'\n")
    concat = os.path.join(tmpd, "concat.mp4")
    subprocess.run([FFQ, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", concat], capture_output=True, check=True)
    alst = os.path.join(tmpd, "alist.txt")
    with open(alst, "w") as f:
        for a in aud_files:
            f.write(f"file '{os.path.abspath(a)}'\n")
    aconcat = os.path.join(tmpd, "audio.m4a")
    subprocess.run([FFQ, "-y", "-f", "concat", "-safe", "0", "-i", alst,
                    "-c:a", "aac", "-b:a", "128k", aconcat],
                   capture_output=True, check=True)
    subprocess.run([FFQ, "-y", "-i", concat, "-i", aconcat,
                    "-c:v", "copy", "-c:a", "copy",
                    "-shortest", "-movflags", "+faststart", out],
                   capture_output=True, check=True)
    shutil.rmtree(tmpd, ignore_errors=True)

    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", out], capture_output=True, text=True)
    size_mb = os.path.getsize(out) / 1e6
    print(f"OK: {out}")
    print(f"  res: {r.stdout.strip()} | size: {size_mb:.1f}MB | dur: {dur(out):.1f}s")
    wh = r.stdout.strip().split(",")
    assert wh[0] == "1080" and wh[1] == "1920", "resolusi bukan 1080x1920!"
    if size_mb >= 100:
        print("  >100MB — kompres ulang crf 28")
        tmp = out + ".small.mp4"
        subprocess.run([FFQ, "-y", "-i", out, "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "28", "-c:a", "copy", "-movflags", "+faststart", tmp],
                       capture_output=True, check=True)
        os.replace(tmp, out)
        print(f"  setelah kompres: {os.path.getsize(out)/1e6:.1f}MB")

if __name__ == "__main__":
    main()
