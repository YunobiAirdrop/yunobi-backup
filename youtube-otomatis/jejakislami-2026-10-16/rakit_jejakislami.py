#!/usr/bin/env python3
"""Rakit video LONG Jejak Islami dari klip Pexels + voiceover per-beat.
Penggunaan: python3 rakit_jejakislami.py <dir_kerja> <output>
  dir_kerja berisi: footage/*.mp4, clips.json {beat: file}, build/durasi_beats.json,
                   build/voiceover.mp3
  SEMUA ffmpeg lewat ffmpeg-queue.sh (jangan bare ffmpeg).
"""
import subprocess, os, sys, json, glob

FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
W, H = 1280, 720

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def run(args):
    r = subprocess.run([FQ] + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL:", " ".join(args[:6]), "\n", r.stderr[-800:])
        raise SystemExit(1)

def seg_video(clip, seg_dur, idx, out):
    cd = dur(clip)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H},"
          "eq=contrast=1.08:saturation=0.92:brightness=-0.02,"
          "noise=alls=6:allf=t,"  # film grain halus
          "vignette=PI/5")
    if cd >= seg_dur:
        # potong dari tengah klip agar variatif antar beat
        start = max(0.0, (cd - seg_dur) / 2)
        run(["-y", "-ss", f"{start:.2f}", "-i", clip, "-t", f"{seg_dur:.2f}",
             "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", "30", "-an", out])
    else:
        # loop klip pendek sampai cukup
        run(["-y", "-stream_loop", "-1", "-i", clip,
             "-vf", vf, "-t", f"{seg_dur:.2f}",
             "-c:v", "libx264", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", "30", "-an", out])

def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=index",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return bool(r.stdout.strip())

def seg_audio_ambience(clip, seg_dur, out):
    if not has_audio(clip):
        # klip tanpa audio -> sunyi (tetap sinkron durasi)
        run(["-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={seg_dur:.2f}",
             "-c:a", "aac", "-b:a", "96k", out])
        return
    cd = dur(clip)
    # ambil audio asli klip sebagai SFX/ambience rekaman asli, volume rendah
    if cd >= seg_dur:
        start = max(0.0, (cd - seg_dur) / 2)
        run(["-y", "-ss", f"{start:.2f}", "-i", clip, "-t", f"{seg_dur:.2f}",
             "-vn", "-af", "volume=0.18,aresample=44100", "-c:a", "aac", "-b:a", "96k", out])
    else:
        run(["-y", "-stream_loop", "-1", "-i", clip, "-t", f"{seg_dur:.2f}",
             "-vn", "-af", "volume=0.18,aresample=44100", "-c:a", "aac", "-b:a", "96k", out])

def title_card(dur_s, title, subtitle, out):
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    vf = (f"color=c=0x0a0a12:s={W}x{H}:d={dur_s:.1f},format=yuv420p,"
          f"drawtext=fontfile={font}:text='{title}':fontcolor=0xf5c542:fontsize=64:"
          f"x=(w-text_w)/2:y=(h-text_h)/2-40,"
          f"drawtext=fontfile={font}:text='{subtitle}':fontcolor=white:fontsize=30:"
          f"x=(w-text_w)/2:y=(h-text_h)/2+50,"
          "noise=alls=6:allf=t,"
          f"fade=t=in:st=0:d=0.6,fade=t=out:st={dur_s-0.6:.1f}:d=0.6")
    tmpd = os.path.dirname(out)
    tv = os.path.join(tmpd, "title_v.mp4")
    ta = os.path.join(tmpd, "title_a.m4a")
    run(["-y", "-f", "lavfi", "-i", vf,
         "-t", f"{dur_s:.1f}",
         "-c:v", "libx264", "-preset", "veryfast", "-r", "30", tv])
    run(["-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={dur_s:.1f}",
         "-c:a", "aac", "-b:a", "96k", ta])
    run(["-y", "-i", tv, "-i", ta, "-c", "copy", "-shortest", out])

def main():
    work, out = sys.argv[1], sys.argv[2]
    foot = os.path.join(work, "footage")
    mapping = json.load(open(os.path.join(work, "clips.json")))  # beat -> filename
    durs = json.load(open(os.path.join(work, "build", "durasi_beats.json")))
    beats = sorted(durs.keys())
    tmpd = os.path.join(work, "build", "_tmp_segs")
    os.makedirs(tmpd, exist_ok=True)

    vsegs, asegs = [], []
    # 0) title card
    tc = os.path.join(tmpd, "title.mp4")
    if not (os.path.exists(tc) and dur(tc) >= 2.9):
        print("render title card...")
        title_card(3.0, "BILAL BIN RABAH", "Dari Budak menjadi Muadzin Pertama", tc)
    vsegs.append(tc); asegs.append(tc)

    for i, b in enumerate(beats):
        clip = os.path.join(foot, mapping[b])
        sd = float(durs[b])
        v = os.path.join(tmpd, f"v{i:02d}.mp4")
        a = os.path.join(tmpd, f"a{i:02d}.m4a")
        ok = (os.path.exists(v) and dur(v) >= sd * 0.95
              and os.path.exists(a) and dur(a) >= sd * 0.95)
        if not ok:
            print(f"  segmen {b} ({sd:.1f}s) <- {mapping[b]}...", flush=True)
            seg_video(clip, sd, i, v)
            seg_audio_ambience(clip, sd, a)
        vsegs.append(v); asegs.append(a)

    # concat video & ambience
    vlst = os.path.join(tmpd, "vlist.txt"); alst = os.path.join(tmpd, "alist.txt")
    open(vlst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in vsegs))
    # ambience: title card mp4 sudah ada audio; segmen audio .m4a
    amb_inputs = []
    for s in asegs:
        amb_inputs.append(s)
    amb_list = os.path.join(tmpd, "amblist.txt")
    with open(amb_list, "w") as f:
        for s in amb_inputs:
            # ekstrak audio saja bila mp4
            f.write(f"file '{os.path.abspath(s)}'\n")
    vcat = os.path.join(tmpd, "vcat.mp4"); acat = os.path.join(tmpd, "acat.m4a")
    run(["-y", "-f", "concat", "-safe", "0", "-i", vlst, "-c", "copy", vcat])
    # gabung audio: ambil audio dari tiap segmen (v=mp4 berisi audio, a=m4a)
    # cara sederhana: concat demuxer hanya utk audio via -vn
    acat_inputs = []
    cmd = ["-y"]
    for s in amb_inputs:
        cmd += ["-i", s]
    n = len(amb_inputs)
    filt = "".join(f"[{i}:a]aresample=44100[a{i}];" for i in range(n))
    filt += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[aout]"
    cmd += ["-filter_complex", filt, "-map", "[aout]", "-c:a", "aac", "-b:a", "96k", acat]
    print("gabung ambience...")
    run(cmd)

    # mix voiceover + ambience (ambience -14dB di bawah voice)
    vo = os.path.join(work, "build", "voiceover.mp3")
    print("mix voiceover + ambience...")
    run(["-y", "-i", vcat, "-i", acat, "-i", vo,
         "-filter_complex",
         "[1:a]volume=0.20[amb];[2:a]aresample=44100,volume=1.0[vox];[amb][vox]amix=inputs=2:duration=longest:dropout_transition=0[aout]",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
         "-movflags", "+faststart", "-shortest", out])
    d = dur(out)
    sz = os.path.getsize(out) / 1e6
    print(f"OK: {out} ({d/60:.1f} mnt, {sz:.1f} MB)")
    if sz >= 100:
        print("PERINGATAN: >100MB, perlu kompres!")

if __name__ == "__main__":
    main()
