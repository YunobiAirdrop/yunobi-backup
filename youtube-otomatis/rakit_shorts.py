#!/usr/bin/env python3
"""Rakit YouTube Shorts 9:16: N gambar (Ken Burns vertikal) + voiceover + film grain + teks hook.
Penggunaan: python3 rakit_shorts.py <dir_gambar> <file_audio> <output> <durasi_json> [hook_text]
  dir_gambar: *.webp (beat-01..N; gambar terakhir = title card/outro)
  durasi_json: {"beat-001": 7.61, ...} — beat terakhir (title card) boleh ditambah manual
  hook_text: teks on-screen besar di beat pertama (opsional)
  Build: 720x1280, -preset veryfast, semua via ffmpeg-queue.sh.
"""
import subprocess, os, glob, sys, json, shutil

FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def font():
    # cari font sans tebal yang tersedia
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return p
    return ""

def kenburns_v(img, seg_dur, idx, out, hook_lines=None):
    total_frames = int(seg_dur * 30)
    mode = idx % 4
    if mode == 0:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30"
    elif mode == 1:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='(iw-iw/zoom)*on/{total_frames}':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30"
    elif mode == 2:
        zp = f"zoompan=z='max(1.15-0.0012*on,1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30"
    else:
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{total_frames}':s=720x1280:fps=30"
    vf = (f"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,{zp},"
          "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
          "noise=alls=6:allf=t,"
          "vignette=PI/5")
    fnt = font()
    if hook_lines and fnt:
        # teks hook multi-baris di zona aman atas; hook_lines = list baris
        for j, ln in enumerate(hook_lines):
            ht = ln.replace(":", "\\:").replace("'", "")
            vf += (f",drawtext=fontfile={fnt}:text='{ht}':fontsize=58:fontcolor=white:"
                   f"borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.20+{j*76}")
    r = subprocess.run([FQ, "-y", "-loop", "1", "-i", img,
                        "-vf", vf, "-t", str(seg_dur),
                        "-c:v", "libx264", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", "-r", "30", out],
                       capture_output=True)
    return r.returncode == 0

def main():
    gdir, audio, out, dur_json = sys.argv[1:5]
    hook_text = sys.argv[5] if len(sys.argv) > 5 else ""
    hook_lines = hook_text.split("|") if hook_text else []
    imgs = sorted(glob.glob(os.path.join(gdir, "beat-*.webp")))
    dj = json.load(open(dur_json))
    seg_durs = [float(dj[f"beat-{i+1:03d}"]) for i in range(len(imgs))]
    print(f"{len(imgs)} gambar, target {sum(seg_durs):.1f}s", flush=True)
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
        ht = hook_lines if i == 0 else []
        for attempt in range(2):
            if kenburns_v(img, seg_durs[i], i, s, ht) and dur(s) >= seg_durs[i] * 0.9:
                break
            print(f"    retry s{i:03d} (attempt {attempt+2})", flush=True)
        else:
            print(f"GAGAL: s{i:03d}"); sys.exit(1)
    segs = [os.path.join(tmpd, f"s{i:03d}.mp4") for i in range(len(imgs))]
    assert all(os.path.exists(s) for s in segs), "masih ada segmen hilang"
    lst = os.path.join(tmpd, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    concat = os.path.join(tmpd, "concat.mp4")
    subprocess.run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", concat], capture_output=True, check=True)
    total = sum(seg_durs)
    # bed ambient gelap halus di bawah voiceover (sintetis, -28dB)
    subprocess.run([FQ, "-y", "-i", concat, "-i", audio,
                    "-f", "lavfi", "-i", f"sine=frequency=55:duration={total:.2f}",
                    "-filter_complex",
                    "[2:a]lowpass=f=200,volume=0.04[bed];[1:a]volume=1.0[vo];[bed][vo]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", out],
                   capture_output=True, check=True)
    print(f"OK: {out} ({dur(out):.1f}s)")
    shutil.rmtree(tmpd)

if __name__ == "__main__":
    main()
