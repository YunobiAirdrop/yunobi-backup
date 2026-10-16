#!/usr/bin/env python3
"""Rakit 3 video Jejak Buddha — VERSI OPTIMAL: sedikit panggilan ffmpeg.
Setiap video: 1 call VO + 1 call video-segmen (filter_complex) + 1 call ambient + 1 call final.
Penggunaan: python3 assemble_fast.py [long|s1|s2|all]
"""
import subprocess, os, sys, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
GAP = 0.4

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:6]), "\n", r.stderr[-2500:]); sys.exit(1)
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

def build(name, W, H, beats, texts, audio_dir, outname, titlecard=None):
    os.chdir(ROOT)
    segs = f"segs_{name}"
    if os.path.exists(segs): shutil.rmtree(segs)
    os.makedirs(segs, exist_ok=True)

    clips = {}
    for _, c, _ in beats:
        p = f"clips/{c}.mp4"
        assert os.path.exists(p), f"klip hilang: {p}"
        clips[c] = p
    clip_dur = {k: dur(p) for k, p in clips.items()}

    # --- ukur durasi VO per beat ---
    beat_durs, starts = [], []
    t = 0.0
    for (b, _, _) in beats:
        key = f"beat-{b:03d}" if isinstance(b, int) else b
        ap = f"{audio_dir}/{key}.mp3"
        d = dur(ap); beat_durs.append(d); starts.append(t)
        t += d + GAP
    total_vo = t - GAP
    nbeats = len(beats)

    # --- CALL 1: VO concat ---
    vo_path = f"{segs}/vo.mp3"
    inputs, fc = [], []
    for i, (b, _, _) in enumerate(beats):
        key = f"beat-{b:03d}" if isinstance(b, int) else b
        inputs += ["-i", f"{audio_dir}/{key}.mp3"]
        fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    fc.append("".join(f"[a{i}]" for i in range(nbeats)) +
              f"amix=inputs={nbeats}:normalize=0,aresample=44100,apad=pad_dur=1.5[vo]")
    run([FQ, "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vo]",
         "-c:a", "libmp3lame", "-b:a", "160k", "-t", str(total_vo + 1.5), vo_path])
    print(f"[{name}] VO {total_vo:.1f}s OK")

    # --- CALL 2: segmen video via filter_complex (batch bila banyak) ---
    used = {}
    seginfo = []  # (clip, off, segdur)
    for idx, (b, clip, use_n) in enumerate(beats):
        cd = clip_dur[clip]; bd = beat_durs[idx] + 0.8
        off = used.get(clip, 0.0)
        if off + bd > cd - 0.5: off = 0.0
        used[clip] = off + bd
        seginfo.append((clip, off, bd))
    BATCH = 15
    batch_files = []
    for bi in range(0, nbeats, BATCH):
        chunk = seginfo[bi:bi+BATCH]
        uniq = list(dict.fromkeys(c for c, _, _ in chunk))
        ci = {c: i for i, c in enumerate(uniq)}
        vinputs = []
        for c in uniq:
            vinputs += ["-i", clips[c]]
        vf_parts, vlabels = [], []
        for j, (clip, off, bd) in enumerate(chunk):
            vlabels.append(f"[v{j}]")
            vf_parts.append(
                f"[{ci[clip]}:v]trim=start={off:.2f}:duration={bd:.2f},setpts=PTS-STARTPTS,"
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"eq=contrast=1.06:saturation=0.94:brightness=-0.015,"
                f"noise=alls=6:allf=t,vignette=PI/6,setsar=1[v{j}]")
        vf_parts.append("".join(vlabels) + f"concat=n={len(chunk)}:v=1:a=0[vout]")
        bf = f"{segs}/vbatch{bi//BATCH:02d}.mp4"
        run([FQ, "-y", *vinputs, "-filter_complex", ";".join(vf_parts),
             "-map", "[vout]", "-c:v", "libx264", "-preset", "veryfast", "-r", "30",
             "-an", bf])
        batch_files.append(bf)
        print(f"[{name}] batch {bi//BATCH+1}/{(nbeats+BATCH-1)//BATCH} OK")
    vcat = f"{segs}/vcat.mp4"
    if len(batch_files) == 1:
        os.rename(batch_files[0], vcat)
    else:
        lst = f"{segs}/vlist.txt"
        with open(lst, "w") as f:
            for bf in batch_files: f.write(f"file '{os.path.abspath(bf)}'\n")
        run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vcat])
    total_v = sum(beat_durs) + 0.8 * nbeats
    print(f"[{name}] video {total_v:.1f}s OK")

    # --- caption ASS ---
    def esc(s): return s.replace("\\", "\\\\")
    FS = 52 if H > W else 34
    MV = 300 if H > W else 90
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
           "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           f"Style: cap,DejaVu Sans,{FS},&H00FFFFFF,&H99000000,-1,0,1,3,1,2,40,40,{MV},1",
           f"Style: big,DejaVu Sans,{FS+20},&H0000FFFF,&H99000000,-1,0,1,4,1,8,40,40,40,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Text"]
    for idx, (b, _, _) in enumerate(beats):
        key = f"beat-{b:03d}" if isinstance(b, int) else b
        chunks = chunk_words(texts[key])
        for j, ch in enumerate(chunks):
            st = starts[idx] + (beat_durs[idx]/len(chunks))*j
            en = starts[idx] + (beat_durs[idx]/len(chunks))*(j+1) + 0.05
            ass.append(f"Dialogue: 0,{ts(st)},{ts(en)},cap,{esc(ch)}")
    if titlecard:
        ass.append(f"Dialogue: 1,0:00:00.30,0:00:03.20,big,{{\\pos({W//2},{int(H*0.33)})}}{titlecard}")
    ass.append(f"Dialogue: 1,{ts(total_v-2.6)},{ts(total_v-0.1)},big,{{\\pos({W//2},{int(H*0.44)})}}JEJAK BUDDHA")
    open(f"{segs}/caption.ass", "w").write("\n".join(ass))

    # --- CALL 3: ambient ---
    afc, parts, ainputs = [], [], []
    # ekstrak audio tiap klip sesuai seginfo (reuse offset yang sama)
    for idx, (clip, off, bd) in enumerate(seginfo):
        ainputs += ["-ss", f"{off:.2f}", "-t", f"{bd:.2f}", "-i", clips[clip]]
    for idx, (clip, off, bd) in enumerate(seginfo):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                            "-show_entries", "stream=index", "-of", "csv=p=0", clips[clip]],
                           capture_output=True, text=True)
        if r.stdout.strip():
            afc.append(f"[{idx}:a]aresample=44100,volume=0.12,apad=whole_dur={bd:.2f}[m{idx}]")
        else:
            afc.append(f"anullsrc=r=44100:cl=stereo:d={bd:.2f},volume=0[m{idx}]")
        parts.append(f"[m{idx}]")
    afc.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,aresample=44100[amb]")
    amb_path = f"{segs}/amb.mp3"
    run([FQ, "-y", *ainputs, "-filter_complex", ";".join(afc), "-map", "[amb]",
         "-c:a", "libmp3lame", "-b:a", "96k", amb_path])
    print(f"[{name}] ambient OK")

    # --- CALL 4: final ---
    run([FQ, "-y", "-i", vcat, "-i", vo_path, "-i", amb_path,
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

L_BEATS = [
    (1,"bintang2",0),(29,"istana",0),(30,"istana",1),(31,"lilin",0),(2,"istana",2),
    (32,"pohon",0),(33,"pohon",1),(34,"istana",3),(3,"istana",4),(6,"hutan",0),
    (36,"istana",5),(37,"gunung",0),(7,"gunung",1),(8,"gurun",1),
    (40,"gurun",2),(9,"badai",0),(41,"badai",1),(42,"badai",2),(10,"api",0),
    (43,"api",1),(44,"api",2),(11,"petir",0),(12,"hutan",1),(47,"hutan",2),
    (13,"sunrise",0),(48,"hutan",3),(14,"lilin",1),(49,"bintang2",1),(15,"badai",3),
    (50,"bintang2",2),(51,"bintang2",3),(52,"bintang2",4),(16,"bintang2",5),(53,"bintang2",6),
    (17,"bintang2",7),(54,"lilin",2),(55,"bintang2",8),(18,"bintang2",9),(57,"bintang2",10),
    (58,"sungai",0),(19,"sungai",1),(20,"sungai",2),(61,"sungai",3),(21,"hutan",4),
    (63,"hutan",5),(22,"hutan",6),(23,"gurun",3),(66,"hutan",8),
    (67,"gurun",4),(24,"sunrise",1),(69,"sunrise",2),(70,"sunrise",3),(25,"lilin",3),
    (71,"hutan",9),(26,"pohon",2),(27,"sunrise",4),(72,"sunrise",5),(28,"sunrise",6),
    (73,"sunrise",7),
]
S1_BEATS = [
    (1,"beringin",0),(2,"beringin",1),(3,"badai",0),(4,"petir",0),(5,"hutan",0),
    (6,"badai",1),(7,"gunung",0),(8,"sunrise",0),(9,"beringin",2),
]
S2_BEATS = [
    (1,"badai",0),(2,"hutan",0),(3,"badai",1),(4,"api",0),(5,"gurun",0),
    (6,"pohon",0),(7,"hutan",1),(8,"sunrise",0),(9,"lilin",0),(10,"sunrise",1),
]

def load_texts(pyvar):
    import importlib.util
    spec = importlib.util.spec_from_file_location("gv", f"{ROOT}/gen_vo.py")
    gv = importlib.util.module_from_spec(spec); spec.loader.exec_module(gv)
    arr = {"LONG": gv.LONG, "S1": gv.S1, "S2": gv.S2}[pyvar]
    return {f"beat-{i+1:03d}": t for i, t in enumerate(arr)}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "s1"):
        d, s = build("s1", 1080, 1920, S1_BEATS, load_texts("S1"), "audio_s1",
                     "jejakbuddha-2026-10-16-shorts1.mp4", titlecard="PASUKAN IBLIS\\NVS 1 ORANG")
        print(f"S1 SELESAI: {d:.0f}s, {s:.1f}MB")
    if which in ("all", "s2"):
        d, s = build("s2", 1080, 1920, S2_BEATS, load_texts("S2"), "audio_s2",
                     "jejakbuddha-2026-10-16-shorts2.mp4", titlecard="999 KORBAN,\\NKURANG 1 LAGI")
        print(f"S2 SELESAI: {d:.0f}s, {s:.1f}MB")
    if which in ("all", "long"):
        d, s = build("long", 1280, 720, L_BEATS, load_texts("LONG"), "audio_long",
                     "jejakbuddha-2026-10-16-long.mp4", titlecard="PANGERAN INI KABUR\\NTENGAH MALAM")
        print(f"LONG SELESAI: {d:.0f}s ({d/60:.1f} mnt), {s:.1f}MB")
    print("SELESAI", which)
