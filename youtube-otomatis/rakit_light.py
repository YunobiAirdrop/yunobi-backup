#!/usr/bin/env python3
"""Lanjutkan rakit video dari segmen yang sudah ada (ringan: 1280x720 langsung).
Penggunaan: python3 resume_rakit.py <dir_gambar> <file_audio> <output> <durasi_json>
  Me-render ulang hanya segmen yang hilang/rusak di <outdir>/_tmp_segs, lalu
  concat semua + mux audio.
"""
import subprocess, os, glob, sys, json, shutil

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def kenburns_light(img, seg_dur, idx, out):
    total_frames = int(seg_dur * 30)
    mode = idx % 4
    if mode == 0:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30"
    elif mode == 1:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='(iw-iw/zoom)*on/{total_frames}':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30"
    elif mode == 2:
        zp = f"zoompan=z='max(1.15-0.0012*on,1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30"
    else:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{total_frames}':s=1280x720:fps=30"
    vf = (f"scale=1280:720,{zp},"
          "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
          "noise=alls=6:allf=t,"
          "vignette=PI/5")
    r = subprocess.run(["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y", "-loop", "1", "-i", img,
                        "-vf", vf, "-t", str(seg_dur),
                        "-c:v", "libx264", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", "-r", "30", out],
                       capture_output=True)
    return r.returncode == 0

def main():
    gdir, audio, out, dur_json = sys.argv[1:5]
    imgs = sorted(glob.glob(os.path.join(gdir, "*.webp")))
    dj = json.load(open(dur_json))
    seg_durs = [float(dj[f"beat-{i+1:03d}"]) for i in range(len(imgs))]
    print(f"{len(imgs)} gambar, target {sum(seg_durs)/60:.1f} mnt")
    tmpd = os.path.join(os.path.dirname(out), "_tmp_segs")
    os.makedirs(tmpd, exist_ok=True)
    # validasi + render ulang yang hilang/rusak
    for i, img in enumerate(imgs):
        s = os.path.join(tmpd, f"s{i:03d}.mp4")
        ok = os.path.exists(s) and dur(s) >= seg_durs[i] * 0.9
        if ok:
            continue
        if os.path.exists(s):
            os.remove(s)
        print(f"  render s{i:03d} ({seg_durs[i]:.1f}s)...", flush=True)
        for attempt in range(2):
            if kenburns_light(img, seg_durs[i], i, s) and dur(s) >= seg_durs[i] * 0.9:
                break
            print(f"    retry s{i:03d} (attempt {attempt+2})", flush=True)
        else:
            print(f"GAGAL: s{i:03d}"); sys.exit(1)
        if (i + 1) % 5 == 0:
            print(f"  {i+1}/{len(imgs)} segmen...", flush=True)
    segs = [os.path.join(tmpd, f"s{i:03d}.mp4") for i in range(len(imgs))]
    assert all(os.path.exists(s) for s in segs), "masih ada segmen hilang"
    lst = os.path.join(tmpd, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    concat = os.path.join(tmpd, "concat.mp4")
    subprocess.run(["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", concat], capture_output=True, check=True)
    subprocess.run(["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y", "-i", concat, "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", out],
                   capture_output=True, check=True)
    print(f"OK: {out} ({dur(out)/60:.1f} menit)")
    shutil.rmtree(tmpd)

if __name__ == "__main__":
    main()
