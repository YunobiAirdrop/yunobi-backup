#!/usr/bin/env python3
"""Rakit Shorts 9:16 Jejak Buddha: footage Pexels asli + VO Mudiwa + grain + SFX ambient asli + caption.
Penggunaan: python3 assemble.py  (dijalankan dari direktori 2026-10-16-shorts/)
  clips/c01.mp4..c08.mp4 = footage Pexels (diunduh), audio/beat-001..011.mp3 = VO.
Semua render via ffmpeg-queue.sh.
"""
import subprocess, os, sys, json, textwrap, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
W, H, FPS = 720, 1280, 30
GAP = 0.35  # jeda antar beat

# beat -> (clip, pakai bagian ke berapa dari klip bila reuse)
BEATS = [
    ("beat-001", "c01", 0),  # hook — lilin 1
    ("beat-002", "c02", 0),  # langit malam 1 (duka)
    ("beat-003", "c03", 0),  # candi angkor (dari rumah ke rumah)
    ("beat-004", "c04", 0),  # star trails (kehampaan duka)
    ("beat-005", "c05", 0),  # kolom kuno tepi laut (menghadap Buddha)
    ("beat-006", "c06", 0),  # lilin 2 (tugas biji sesawi)
    ("beat-007", "c06", 1),  # lilin 2 reuse (tiap rumah berduka)
    ("beat-008", "c08", 0),  # kabut hutan (berhenti & mengerti)
    ("beat-009", "c04", 1),  # star trails reuse (universal: milik semua)
    ("beat-010", "c09", 0),  # sungai tenang
    ("beat-011", "c01", 1),  # lilin 1 (loop seam dgn beat 1)
]
CLIP_TXT = {
    "beat-001": "Bayinya sudah meninggal. Tapi ibu ini bersumpah akan menghidupkannya kembali.",
    "beat-002": "Namanya Kisagotami. Anak satu-satunya meninggal saat masih bayi.",
    "beat-003": "Ia menggendong jasad kecil itu dari rumah ke rumah, memohon agar anaknya dihidupkan.",
    "beat-004": "Semua orang berkata ia sudah gila karena duka.",
    "beat-005": "Lalu seseorang membawanya menghadap Buddha.",
    "beat-006": "Buddha berkata: bawakan Aku segenggam biji sesawi, dari rumah yang tak pernah mengalami kematian.",
    "beat-007": "Ia berlari penuh harap. Tapi di setiap rumah ada cerita kehilangan: ayah, ibu, anak, saudara.",
    "beat-008": "Ia pun berhenti. Dan saat itu, ia akhirnya mengerti.",
    "beat-009": "Kematian bukan musibah yang menimpa dirinya saja. Ia milik semua yang hidup.",
    "beat-010": "Ia menguburkan anaknya, dan hatinya akhirnya sembuh.",
    "beat-011": "Kadang yang kita butuhkan bukan obat, melainkan pengertian.",
}

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:6]), "...\n", r.stderr[-2000:]); sys.exit(1)
    return r

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def chunk_words(text, n=4):
    w = text.split()
    return [" ".join(w[i:i+n]) for i in range(0, len(w), n)]

def main():
    os.chdir(ROOT)
    clips = {f"c{i:02d}": f"clips/c{i:02d}.mp4" for i in range(1, 10)}
    for k, p in clips.items():
        assert os.path.exists(p), f"klip hilang: {p}"
    clip_dur = {k: dur(p) for k, p in clips.items()}
    print("durasi klip:", {k: round(v,1) for k,v in clip_dur.items()})

    # --- 1. gabung VO dengan jeda ---
    segs_dir = "segs"; os.makedirs(segs_dir, exist_ok=True)
    beat_durs, starts = [], []
    t = 0.0
    # siapkan segmen video per beat dulu untuk tau durasi target
    # VO concat: pakai adelay+amix agar jeda presisi
    inputs, fc = [], []
    for i, (beat, _, _) in enumerate(BEATS):
        inputs += ["-i", f"audio/{beat}.mp3"]
        d = dur(f"audio/{beat}.mp3")
        beat_durs.append(d); starts.append(t)
        fc.append(f"[{i}:a]adelay={int(t*1000)}|{int(t*1000)}[a{i}]")
        t += d + GAP
    total_vo = t - GAP
    fc.append("".join(f"[a{i}]" for i in range(len(BEATS))) +
              f"amix=inputs={len(BEATS)}:normalize=0,aresample=44100,apad=pad_dur=1.5[vo]")
    run([FQ, "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vo]",
         "-c:a", "libmp3lame", "-b:a", "160k", "-t", str(total_vo + 1.5), f"{segs_dir}/vo.mp3"])
    print(f"VO total {total_vo:.1f}s")

    # --- 2. segmen video per beat ---
    seg_files = []
    used_offset = {}
    for idx, (beat, clip, use_n) in enumerate(BEATS):
        cd = clip_dur[clip]
        bd = beat_durs[idx] + 0.6  # sedikit napas visual
        # offset: bagi klip jadi beberapa bagian bila reuse
        key = (clip, use_n)
        off = used_offset.get(clip, 0.0)
        if off + bd > cd - 0.5:
            off = 0.0  # loop dari awal bila tak cukup
        used_offset[clip] = off + bd
        loops = max(0, int((bd + off) // cd))  # ulangi klip bila beat > sisa klip
        vf = (f"scale=720:1280:force_original_aspect_ratio=increase,"
              f"crop=720:1280,"
              f"eq=contrast=1.06:saturation=0.94:brightness=-0.015,"
              f"noise=alls=6:allf=t,"
              f"vignette=PI/6,format=yuv420p")
        s = f"{segs_dir}/s{idx:02d}.mp4"
        run([FQ, "-y", "-stream_loop", str(loops), "-ss", str(off), "-i", clips[clip],
             "-vf", vf, "-t", str(bd), "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-r", str(FPS), s])
        seg_files.append(s)
        print(f"  seg {idx:02d} {beat} <- {clip} off={off:.1f} dur={bd:.1f}s")
    json.dump({"offsets": used_offset, "clip": [c for _, c, _ in BEATS],
               "segdur": [beat_durs[i] + 0.6 for i in range(len(BEATS))]},
              open(f"{segs_dir}/offsets.json", "w"))

    # --- 3. concat video ---
    lst = f"{segs_dir}/list.txt"
    with open(lst, "w") as f:
        for s in seg_files: f.write(f"file '{os.path.abspath(s)}'\n")
    total_v = sum(beat_durs) + 0.6*len(BEATS)
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{segs_dir}/vcat.mp4"])

    # --- 4. caption ASS ---
    def esc(s): return s.replace("\\", "\\\\")
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "ScaledBorderAndShadow: yes", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: cap,DejaVu Sans,52,&H00FFFFFF,&H99000000,-1,0,1,3,1,2,40,40,300,1",
           "Style: big,DejaVu Sans,72,&H0000FFFF,&H99000000,-1,0,1,4,1,8,40,40,40,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Text"]
    def ts(x):
        h=int(x//3600); m=int(x%3600//60); s=x%60
        return f"{h}:{m:02d}:{s:05.2f}"
    for idx, (beat, _, _) in enumerate(BEATS):
        chunks = chunk_words(CLIP_TXT[beat])
        cd = len(chunks)
        for j, ch in enumerate(chunks):
            st = starts[idx] + (beat_durs[idx]/cd)*j
            en = starts[idx] + (beat_durs[idx]/cd)*(j+1) + 0.05
            ass.append(f"Dialogue: 0,{ts(st)},{ts(en)},cap,{esc(ch)}")
    # title card hook (3 detik pertama, teks besar)
    ass.append(f"Dialogue: 1,0:00:00.30,0:00:03.20,big,{{\\pos(360,420)}}IBU INI TAK TERIMA\\NANAKNYA MATI")
    # end card
    ass.append(f"Dialogue: 1,{ts(total_v-2.6)},{ts(total_v-0.1)},big,{{\\pos(360,560)}}JEJAK BUDDHA")
    open("caption.ass", "w").write("\n".join(ass))

    # --- 5. ambient asli dari klip (SFX rekaman asli tersinkron) ---
    # ekstrak audio klip dgn offset SAMA seperti segmen video; klip tanpa audio -> sunyi
    uo, seg_offs = {}, []
    for idx, (beat, clip, use_n) in enumerate(BEATS):
        cd = clip_dur[clip]; bd = beat_durs[idx] + 0.6
        off = uo.get(clip, 0.0)
        if off + bd > cd - 0.5: off = 0.0
        uo[clip] = off + bd
        loops = max(0, int((bd + off) // cd))
        seg_offs.append((clip, off, bd, loops))
    amb_inputs = []
    for idx, (clip, off, bd, loops) in enumerate(seg_offs):
        amb_inputs += ["-stream_loop", str(loops), "-ss", str(off), "-t", str(bd), "-i", clips[clip]]
    probe = []
    for idx, (clip, off, bd, loops) in enumerate(seg_offs):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                            "-show_entries", "stream=index",
                            "-of", "csv=p=0", clips[clip]],
                           capture_output=True, text=True)
        probe.append(bool(r.stdout.strip()))
    amb_fc2, parts = [], []
    for idx, has_a in enumerate(probe):
        bd = seg_offs[idx][2]
        if has_a:
            amb_fc2.append(f"[{idx}:a]aresample=44100,volume=0.14,apad=whole_dur={bd}[m{idx}]")
        else:
            amb_fc2.append(f"anullsrc=r=44100:cl=stereo:d={bd},volume=0[m{idx}]")
        parts.append(f"[m{idx}]")
    amb_fc2.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,aresample=44100[amb]")
    run([FQ, "-y", *amb_inputs, "-filter_complex", ";".join(amb_fc2), "-map", "[amb]",
         "-c:a", "libmp3lame", "-b:a", "96k", f"{segs_dir}/amb.mp3"])

    # --- 6. final: video + caption + mix VO & ambient ---
    out = "jejakbuddha-2026-10-16-shorts.mp4"
    run([FQ, "-y", "-i", f"{segs_dir}/vcat.mp4", "-i", f"{segs_dir}/vo.mp3", "-i", f"{segs_dir}/amb.mp3",
         "-filter_complex",
         "[1:a][2:a]amix=inputs=2:duration=first:dropout_transition=0,aresample=44100[aout]",
         "-vf", f"ass=caption.ass",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", out])
    sz = os.path.getsize(out)/1e6
    print(f"OK: {out} {dur(out):.1f}s {sz:.1f}MB")
    assert sz < 100, "file >100MB!"
    shutil.rmtree(segs_dir)

if __name__ == "__main__":
    main()
