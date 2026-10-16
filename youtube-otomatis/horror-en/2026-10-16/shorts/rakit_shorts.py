#!/usr/bin/env python3
"""Rakit shorts 1080x1920 dari gambar + voiceover.
Penggunaan: python3 rakit_shorts.py <sdir> <output>
  sdir berisi img/beat-*.webp, audio/voiceover_full.mp3, durasi.json
Render SEMUA via ffmpeg-queue.sh, -preset veryfast.
"""
import subprocess, os, glob, sys, json, shutil

FFQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
W, H = 1080, 1920

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def kenburns_916(img, seg_dur, idx, out):
    total_frames = int(seg_dur * 30)
    mode = idx % 4
    if mode == 0:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    elif mode == 1:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='(iw-iw/zoom)*on/{total_frames}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    elif mode == 2:
        zp = f"zoompan=z='max(1.18-0.0015*on,1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30"
    else:
        zp = f"zoompan=z='min(zoom+0.0015,1.18)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{total_frames}':s={W}x{H}:fps=30"
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H},{zp},"
          "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
          "noise=alls=7:allf=t,"
          "vignette=PI/4.5")
    r = subprocess.run([FFQ, "-y", "-loop", "1", "-i", img,
                        "-vf", vf, "-t", str(seg_dur),
                        "-c:v", "libx264", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", "-r", "30", out],
                       capture_output=True)
    return r.returncode == 0

def main():
    sdir, out = sys.argv[1], sys.argv[2]
    imgs = sorted(glob.glob(os.path.join(sdir, "img", "beat-*.webp")))
    audio = os.path.join(sdir, "audio", "voiceover_full.mp3")
    dj = json.load(open(os.path.join(sdir, "durasi.json")))
    assert len(imgs) == len(dj), f"gambar {len(imgs)} != durasi {len(dj)}"
    seg_durs = [float(dj[f"beat-{i+1:03d}"]) for i in range(len(imgs))]
    print(f"{len(imgs)} gambar, target {sum(seg_durs):.1f}s")
    tmpd = os.path.join(os.path.dirname(out), "_tmp_segs")
    os.makedirs(tmpd, exist_ok=True)
    for i, img in enumerate(imgs):
        s = os.path.join(tmpd, f"s{i:03d}.mp4")
        ok = os.path.exists(s) and dur(s) >= seg_durs[i] * 0.9
        if ok:
            continue
        if os.path.exists(s):
            os.remove(s)
        print(f"  render s{i:03d} ({seg_durs[i]:.1f}s)...", flush=True)
        for _ in range(2):
            if kenburns_916(img, seg_durs[i], i, s) and dur(s) >= seg_durs[i] * 0.9:
                break
        else:
            print(f"GAGAL: s{i:03d}"); sys.exit(1)
    segs = [os.path.join(tmpd, f"s{i:03d}.mp4") for i in range(len(imgs))]
    lst = os.path.join(tmpd, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    concat = os.path.join(tmpd, "concat.mp4")
    subprocess.run([FFQ, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", concat], capture_output=True, check=True)
    subprocess.run([FFQ, "-y", "-i", concat, "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", out],
                   capture_output=True, check=True)
    print(f"OK: {out} ({dur(out):.1f}s)")
    shutil.rmtree(tmpd)

if __name__ == "__main__":
    main()
