#!/usr/bin/env python3
"""Rakit 3 video Jejak Buddha 2026-10-16-fix: 1 long 16:9 + 2 shorts 9:16.
Penggunaan: python3 assemble_all.py [long|s1|s2|all]
Semua render via ffmpeg-queue.sh. VO Mudiwa sudah ada di audio_long/audio_s1/audio_s2.
"""
import subprocess, os, sys, json, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
GAP = 0.4

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:8]), "\n", r.stderr[-2500:]); sys.exit(1)
    return r

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def chunk_words(text, n=4):
    w = text.split()
    return [" ".join(w[i:i+n]) for i in range(0, len(w), n)]

def ts(x):
    h = int(x//3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build(name, W, H, beats, texts, audio_dir, outname, titlecard=None, endcard="JEJAK BUDDHA"):
    """beats: list of (beat_id, clip_name, use_n). texts: dict beat_id -> text."""
    os.chdir(ROOT)
    segs = f"segs_{name}"; os.makedirs(segs, exist_ok=True)
    clips = {}
    for _, c, _ in beats:
        p = f"clips/{c}.mp4"
        assert os.path.exists(p), f"klip hilang: {p}"
        clips[c] = p
    clip_dur = {k: dur(p) for k, p in clips.items()}
    print(f"[{name}] durasi klip:", {k: round(v, 1) for k, v in clip_dur.items()})

    # 1. VO concat dengan jeda
    beat_ids = [b for b, _, _ in beats]
    inputs, fc, beat_durs, starts = [], [], [], []
    t = 0.0
    for i, b in enumerate(beat_ids):
        ap = f"{audio_dir}/beat-{b:03d}.mp3" if isinstance(b, int) else f"{audio_dir}/{b}.mp3"
        # beat id format: "beat-001" string atau int
        inputs += ["-i", ap]
        d = dur(ap); beat_durs.append(d); starts.append(t)
        fc.append(f"[{i}:a]adelay={int(t*1000)}|{int(t*1000)}[a{i}]")
        t += d + GAP
    total_vo = t - GAP
    fc.append("".join(f"[a{i}]" for i in range(len(beats))) +
              f"amix=inputs={len(beats)}:normalize=0,aresample=44100,apad=pad_dur=1.5[vo]")
    run([FQ, "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vo]",
         "-c:a", "libmp3lame", "-b:a", "160k", "-t", str(total_vo + 1.5), f"{segs}/vo.mp3"])
    print(f"[{name}] VO total {total_vo:.1f}s")

    # 2. segmen video per beat
    seg_files, used_offset = [], {}
    vscale = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    for idx, (b, clip, use_n) in enumerate(beats):
        cd = clip_dur[clip]; bd = beat_durs[idx] + 0.8
        off = used_offset.get(clip, 0.0)
        if off + bd > cd - 0.5: off = 0.0
        used_offset[clip] = off + bd
        loops = max(0, int((bd + off) // cd))
        vf = (f"{vscale},eq=contrast=1.06:saturation=0.94:brightness=-0.015,"
              f"noise=alls=6:allf=t,vignette=PI/6,format=yuv420p")
        s = f"{segs}/s{idx:02d}.mp4"
        run([FQ, "-y", "-stream_loop", str(loops), "-ss", str(off), "-i", clips[clip],
             "-vf", vf, "-t", str(bd), "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-r", "30", s])
        seg_files.append(s)
    total_v = sum(beat_durs) + 0.8 * len(beats)

    # 3. concat
    lst = f"{segs}/list.txt"
    with open(lst, "w") as f:
        for s in seg_files: f.write(f"file '{os.path.abspath(s)}'\n")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{segs}/vcat.mp4"])

    # 4. caption ASS
    def esc(s): return s.replace("\\", "\\\\")
    FS = 52 if H > W else 34
    MV = 300 if H > W else 90
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
           "ScaledBorderAndShadow: yes", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           f"Style: cap,DejaVu Sans,{FS},&H00FFFFFF,&H99000000,-1,0,1,3,1,2,40,40,{MV},1",
           f"Style: big,DejaVu Sans,{FS+20},&H0000FFFF,&H99000000,-1,0,1,4,1,8,40,40,40,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Text"]
    for idx, (b, _, _) in enumerate(beats):
        key = f"beat-{b:03d}" if isinstance(b, int) else b
        txt = texts[key]
        chunks = chunk_words(txt)
        for j, ch in enumerate(chunks):
            st = starts[idx] + (beat_durs[idx]/len(chunks))*j
            en = starts[idx] + (beat_durs[idx]/len(chunks))*(j+1) + 0.05
            ass.append(f"Dialogue: 0,{ts(st)},{ts(en)},cap,{esc(ch)}")
    cx, cy = W//2, int(H*0.33)
    if titlecard:
        ass.append(f"Dialogue: 1,0:00:00.30,0:00:03.20,big,{{\\pos({cx},{cy})}}{titlecard}")
    ex, ey = W//2, int(H*0.44)
    ass.append(f"Dialogue: 1,{ts(total_v-2.6)},{ts(total_v-0.1)},big,{{\\pos({ex},{ey})}}{endcard}")
    open(f"{segs}/caption.ass", "w").write("\n".join(ass))

    # 5. ambient dari klip
    uo, seg_offs = {}, []
    for idx, (b, clip, use_n) in enumerate(beats):
        cd = clip_dur[clip]; bd = beat_durs[idx] + 0.8
        off = uo.get(clip, 0.0)
        if off + bd > cd - 0.5: off = 0.0
        uo[clip] = off + bd
        loops = max(0, int((bd + off) // cd))
        seg_offs.append((clip, off, bd, loops))
    amb_inputs = []
    for idx, (clip, off, bd, loops) in enumerate(seg_offs):
        amb_inputs += ["-stream_loop", str(loops), "-ss", str(off), "-t", str(bd), "-i", clips[clip]]
    probe = []
    for idx, (clip, _, _, _) in enumerate(seg_offs):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                            "-show_entries", "stream=index", "-of", "csv=p=0", clips[clip]],
                           capture_output=True, text=True)
        probe.append(bool(r.stdout.strip()))
    afc, parts = [], []
    for idx, has_a in enumerate(probe):
        bd = seg_offs[idx][2]
        if has_a:
            afc.append(f"[{idx}:a]aresample=44100,volume=0.12,apad=whole_dur={bd}[m{idx}]")
        else:
            afc.append(f"anullsrc=r=44100:cl=stereo:d={bd},volume=0[m{idx}]")
        parts.append(f"[m{idx}]")
    afc.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,aresample=44100[amb]")
    run([FQ, "-y", *amb_inputs, "-filter_complex", ";".join(afc), "-map", "[amb]",
         "-c:a", "libmp3lame", "-b:a", "96k", f"{segs}/amb.mp3"])

    # 6. final
    run([FQ, "-y", "-i", f"{segs}/vcat.mp4", "-i", f"{segs}/vo.mp3", "-i", f"{segs}/amb.mp3",
         "-filter_complex",
         "[1:a][2:a]amix=inputs=2:duration=first:dropout_transition=0,aresample=44100[aout]",
         "-vf", f"ass={segs}/caption.ass",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", outname])
    sz = os.path.getsize(outname)/1e6
    d = dur(outname)
    print(f"OK: {outname} {d:.1f}s {sz:.1f}MB")
    assert sz < 100, "file >100MB!"
    shutil.rmtree(segs)
    return d, sz

# ---------------- definisi beat ----------------
# LONG: 28 beat
L_BEATS = [
    (1,"bintang2",0),(2,"istana",0),(3,"istana",1),(4,"pohon",0),(5,"istana",2),
    (6,"hutan",0),(7,"gunung",0),(8,"gurun",0),(9,"badai",0),(10,"api",0),
    (11,"petir",0),(12,"hutan",1),(13,"sunrise",0),(14,"lilin",0),(15,"badai",1),
    (16,"bintang2",1),(17,"bintang2",2),(18,"bintang2",3),(19,"sungai",0),(20,"sungai",1),
    (21,"hutan",2),(22,"hutan",3),(23,"gurun",1),(24,"sunrise",1),(25,"lilin",1),
    (26,"pohon",1),(27,"sunrise",2),(28,"sunrise",3),
]
# SHORTS1: 9 beat (Mara)
S1_BEATS = [
    (1,"beringin",0),(2,"beringin",1),(3,"badai",0),(4,"petir",0),(5,"hutan",0),
    (6,"badai",1),(7,"gunung",0),(8,"sunrise",0),(9,"beringin",2),
]
# SHORTS2: 10 beat (Angulimala)
S2_BEATS = [
    (1,"badai",0),(2,"hutan",0),(3,"badai",1),(4,"api",0),(5,"gurun",0),
    (6,"pohon",0),(7,"hutan",1),(8,"sunrise",0),(9,"lilin",0),(10,"sunrise",1),
]

def load_texts(pyvar):
    import importlib.util
    # teks diambil dari gen_vo.py
    spec = importlib.util.spec_from_file_location("gv", f"{ROOT}/gen_vo.py")
    gv = importlib.util.module_from_spec(spec); spec.loader.exec_module(gv)
    arr = {"LONG": gv.LONG, "S1": gv.S1, "S2": gv.S2}[pyvar]
    return {f"beat-{i+1:03d}": t for i, t in enumerate(arr)}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "long"):
        t = load_texts("LONG")
        d, s = build("long", 1280, 720, L_BEATS, t, "audio_long",
                     "jejakbuddha-2026-10-16-long.mp4",
                     titlecard="PANGERAN INI KABUR\\NTENGAH MALAM")
        print(f"LONG: {d:.0f}s ({d/60:.1f} mnt), {s:.1f}MB")
    if which in ("all", "s1"):
        t = load_texts("S1")
        d, s = build("s1", 1080, 1920, S1_BEATS, t, "audio_s1",
                     "jejakbuddha-2026-10-16-shorts1.mp4",
                     titlecard="PASUKAN IBLIS\\NVS 1 ORANG")
        print(f"S1: {d:.0f}s, {s:.1f}MB")
    if which in ("all", "s2"):
        t = load_texts("S2")
        d, s = build("s2", 1080, 1920, S2_BEATS, t, "audio_s2",
                     "jejakbuddha-2026-10-16-shorts2.mp4",
                     titlecard="999 KORBAN,\\NKURANG 1 LAGI")
        print(f"S2: {d:.0f}s, {s:.1f}MB")
    print("SELESAI ASSEMBLE", which)
