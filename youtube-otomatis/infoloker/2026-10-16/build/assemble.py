#!/usr/bin/env python3
"""Rakit 4 video Info Loker Terkini dari stills AI + VO Mudiwa.
- Ken Burns zoompan per beat (pacing variatif), film grain, vignette
- Caption ASS (kata yang diucapkan), title card (long) / hook overlay (shorts)
- SFX tersinkron (thud/ding/coin/typing/paper/whoosh)
- SEMUA ffmpeg via ffmpeg-queue.sh. Output: 1080x1920 shorts, 1280x720 long.
Jalankan dari ~/workspace/youtube-otomatis/infoloker/2026-10-16/
"""
import json, os, subprocess, sys, math

ROOT = "/home/hatch/workspace/youtube-otomatis/infoloker/2026-10-16"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FR = os.path.join(ROOT, "frames")
BD = os.path.join(ROOT, "build")
SFXD = os.path.join(BD, "sfx")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def run(cmd):
    r = subprocess.run([FQ] + cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:6]), "\n", r.stderr[-1200:]); sys.exit(1)
    return r

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

beats_txt = json.load(open(os.path.join(ROOT, "voice", "beats.json")))
D = json.load(open(os.path.join(BD, "durasi.json")))

# beat -> image
IMG = {
 "shorts1": ["s1_01","s1_02","s1_03","s1_04","s1_05","s1_06","s1_06","s1_03","s1_01"],
 "shorts2": ["s2_01","s2_02","s2_03","s2_04","s2_05","s2_06","s2_02","s2_01","s2_01"],
 "shorts3": ["s3_01","s3_02","s3_03","s3_04","s3_05","s3_06","s3_03","s3_03","s3_01"],
 "long":    ["l_01","l_01","l_02","l_02","l_02","l_03","l_06","l_03","l_04","l_07",
             "l_07","l_04","l_04","l_05","l_05","l_05","l_05","l_05","l_04","l_04",
             "l_04","l_06","l_06","l_08","l_08","l_08","l_07","l_07","l_09","l_09",
             "l_09","l_08","l_08","l_10","l_10","l_10","l_09","l_09","l_10","l_10",
             "l_10","l_10","l_11","l_11","l_11","l_11","l_11","l_11","l_11"],
}
BIDS = {"shorts1": [f"s1b{i:02d}" for i in range(1,10)],
        "shorts2": [f"s2b{i:02d}" for i in range(1,10)],
        "shorts3": [f"s3b{i:02d}" for i in range(1,10)],
        "long":    None}  # diisi dinamis dari beats.json (terurut)
BIDS["long"] = sorted(beats_txt["long"].keys())
assert len(IMG["long"]) == len(BIDS["long"]), "IMG long vs beats mismatch"
VKEY = {"shorts1":"s1","shorts2":"s2","shorts3":"s3","long":"long"}
GEO = {"shorts1":(1080,1920), "shorts2":(1080,1920), "shorts3":(1080,1920), "long":(1280,720)}
BREATH = {"shorts1":0.6,"shorts2":0.6,"shorts3":0.6,"long":0.6}

HOOK_BIG = {
 "shorts1": ("JANGAN\\NTRANSFER UANG\\NDULUAN",),
 "shorts2": ("5 PEKERJAAN\\NPALING DICARI\\N2026",),
 "shorts3": ("HRD CUMA\\NBUTUH 6 DETIK",),
}
END_CARD = "INFO LOKER\\NTERKINI"

def zoom_exprs(i, n):
    N = n
    cx = "iw/2-(iw/zoom/2)"; cy = "ih/2-(ih/zoom/2)"
    v = i % 4
    if v == 0:
        return f"z='1+0.15*on/{N}'", f"x='{cx}'", f"y='{cy}'"
    if v == 1:
        return f"z='1.15-0.15*on/{N}'", f"x='{cx}'", f"y='{cy}'"
    if v == 2:
        return f"z='1+0.12*on/{N}'", f"x='(iw-iw/zoom)*on/{N}'", f"y='{cy}'"
    return f"z='1+0.12*on/{N}'", f"x='{cx}'", f"y='(ih-ih/zoom)*(1-on/{N})'"

def seg_image(img, segdur, idx, out, W, H):
    n = max(15, int(round(segdur*30)))
    z, x, y = zoom_exprs(idx, n)
    sw, sh = int(W*1.5), int(H*1.5)
    vf = (f"scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
          f"zoompan={z}:d={n}:{x}:{y}:s={W}x{H}:fps=30,"
          f"eq=contrast=1.06:saturation=0.94:brightness=-0.015,"
          f"noise=alls=6:allf=t,vignette=PI/6,format=yuv420p")
    run(["-y", "-i", os.path.join(FR, img + ".png"), "-vf", vf,
         "-frames:v", str(n), "-r", "30", "-an",
         "-c:v", "libx264", "-preset", "veryfast", out])

def title_card(W, H, out):
    vf = (f"color=c=0x0b0e1a:s={W}x{H}:d=3.0,"
          f"drawtext=fontfile={FONT}:text='8 BIDANG PEKERJAAN':fontcolor=0xf5c542:fontsize=64:"
          f"x=(w-text_w)/2:y=(h-text_h)/2-70,"
          f"drawtext=fontfile={FONT}:text='Paling Dibutuhkan di Indonesia 2026':fontcolor=white:fontsize=32:"
          f"x=(w-text_w)/2:y=(h-text_h)/2+10,"
          f"drawtext=fontfile={FONTN}:text='INFO LOKER TERKINI':fontcolor=0x9aa0b0:fontsize=26:"
          f"x=(w-text_w)/2:y=(h-text_h)/2+70,"
          f"noise=alls=6:allf=t,fade=t=in:st=0:d=0.5,fade=t=out:st=2.5:d=0.5,format=yuv420p")
    run(["-y", "-f", "lavfi", "-i", vf,
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=3.0",
         "-t", "3.0",
         "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "96k", "-shortest", out])

def chunk_words(text, n):
    w = text.split()
    return [" ".join(w[i:i+n]) for i in range(0, len(w), n)]

def ts(x):
    h = int(x//3600); m = int(x%3600//60); s = x%60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_ass(name, W, H, vo_offset):
    vk = VKEY[name]; bids = BIDS[name]; dd = D[name]
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
             "ScaledBorderAndShadow: yes", "",
             "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"]
    if W == 1080:
        lines += ["Style: cap,DejaVu Sans,64,&H00FFFFFF,&H99000000,-1,0,1,3,1,2,60,60,470,1",
                  "Style: big,DejaVu Sans,110,&H0000F5FF,&H99000000,-1,0,1,5,1,8,40,40,40,1"]
    else:
        lines += ["Style: cap,DejaVu Sans,44,&H00FFFFFF,&H99000000,-1,0,1,3,1,2,40,40,80,1"]
    lines += ["", "[Events]", "Format: Layer, Start, End, Style, Text"]
    for b in bids:
        txt = beats_txt[vk][b]
        chunks = chunk_words(txt, 4 if W == 1080 else 6)
        bd = dd["beats"][b]; st0 = dd["starts"][b] + vo_offset
        for j, ch in enumerate(chunks):
            st = st0 + (bd/len(chunks))*j
            en = st0 + (bd/len(chunks))*(j+1) + 0.05
            lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},cap,{ch}")
    if W == 1080:
        lines.append(f"Dialogue: 1,0:00:00.25,0:00:03.20,big,{{\\pos(540,700)}}{HOOK_BIG[name][0]}")
        total_v = vo_offset + dd["total_vo"] + 1.2
        lines.append(f"Dialogue: 1,{ts(total_v-2.4)},{ts(total_v-0.1)},big,{{\\pos(540,700)}}{END_CARD}")
    p = os.path.join(BD, f"caption_{name}.ass")
    open(p, "w").write("\n".join(lines))
    return p

def sfx_track(name, events, total_len, out):
    """events: [(t_seconds, wavfile, volume)]"""
    inputs, fc = [], []
    for i, (t, wav, vol) in enumerate(events):
        inputs += ["-i", os.path.join(SFXD, wav)]
        ms = int(t*1000)
        fc.append(f"[{i}:a]adelay={ms}|{ms},volume={vol}[s{i}]")
    fc.append("".join(f"[s{i}]" for i in range(len(events))) +
              f"amix=inputs={len(events)}:normalize=0,aresample=44100,apad=whole_dur={total_len:.2f}[sfx]")
    run(["-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[sfx]",
         "-c:a", "libmp3lame", "-b:a", "96k", "-t", str(total_len), out])

def sfx_events(name):
    dd = D[name]; st = dd["starts"]; OFF = 3.0 if name == "long" else 0.0
    E = []
    if name == "shorts1":
        E = [(0.05,"thud.wav",0.5),(st["s1b02"]+0.1,"ding.wav",0.4),
             (st["s1b04"],"whoosh.wav",0.35),(st["s1b05"]+0.2,"paper.wav",0.4),
             (st["s1b07"],"ding.wav",0.4),(st["s1b08"],"ding2.wav",0.35)]
    elif name == "shorts2":
        E = [(0.05,"coin.wav",0.5)] + [(st[f"s2b{i:02d}"],"whoosh.wav",0.3) for i in range(2,7)] + \
            [(st["s2b07"],"typing.wav",0.35),(st["s2b08"],"ding2.wav",0.4)]
    elif name == "shorts3":
        E = [(0.05,"thud.wav",0.5),(st["s3b02"],"paper.wav",0.4),
             (st["s3b04"],"typing.wav",0.35),(st["s3b07"],"ding.wav",0.4),
             (st["s3b08"],"whoosh.wav",0.3)]
    else:
        E = [(0.05,"thud.wav",0.5)]
        for b in ["lb03","lb05","lb07","lb09","lb11","lb13","lb15","lb17"]:
            E.append((OFF+st[b],"whoosh.wav",0.28))
        E += [(OFF+st["lb19"],"ding.wav",0.4),(OFF+st["lb21"],"ding2.wav",0.4)]
    return [(t+OFF, w, v) for (t, w, v) in E]

def _singles(name):
    return [([b], img) for b, img in zip(BIDS[name], IMG[name])]

SEGMENTS = {
 "shorts1": _singles("shorts1"),
 "shorts2": _singles("shorts2"),
 "shorts3": _singles("shorts3"),
 # long: 10 beat tunggal (sudah jadi s00-s09) + segmen gabungan s10-s25
 "long": ([([b], img) for b, img in zip(BIDS["long"][:10], IMG["long"][:10])] + [
   (["lb08b"], "l_07"),                          # s10
   (["lb08c", "lb08d"], "l_04"),                 # s11
   (["lb09", "lb10", "lb10b"], "l_05"),          # s12
   (["lb10c", "lb10d"], "l_05"),                 # s13
   (["lb11", "lb12", "lb12b"], "l_04"),          # s14
   (["lb12c", "lb12d"], "l_06"),                 # s15
   (["lb13", "lb14", "lb14b"], "l_08"),          # s16
   (["lb14c", "lb14d"], "l_07"),                 # s17
   (["lb15", "lb16", "lb16b"], "l_09"),          # s18
   (["lb16c", "lb16d"], "l_08"),                 # s19
   (["lb17", "lb18", "lb18b"], "l_10"),          # s20
   (["lb18c", "lb18d"], "l_09"),                 # s21
   (["lb18e", "lb18f", "lb18g"], "l_10"),        # s22
   (["lb19", "lb20"], "l_10"),                   # s23
   (["lb20b", "lb20c"], "l_11"),                 # s24
   (["lb21", "lb21b", "lb21c", "lb22"], "l_11"),  # s25
 ]),
}

def build_one(name, out, seg_lo=None, seg_hi=None, final_only=False):
    W, H = GEO[name]
    dd = D[name]
    tmpd = os.path.join(BD, f"_segs_{name}")
    os.makedirs(tmpd, exist_ok=True)
    segs = SEGMENTS[name]
    if not final_only:
        if name == "long" and seg_lo in (None, 0):
            tc = os.path.join(tmpd, "title.mp4")
            if not (os.path.exists(tc) and dur(tc) >= 2.9):
                print(f"[{name}] title card..."); title_card(W, H, tc)
        lo = seg_lo if seg_lo is not None else 0
        hi = seg_hi if seg_hi is not None else len(segs) - 1
        for i in range(lo, hi + 1):
            blist, img = segs[i]
            assert os.path.exists(os.path.join(FR, img + ".png")), f"gambar hilang: {img}"
            seg = os.path.join(tmpd, f"s{i:02d}.mp4")
            segdur = sum(dd["beats"][b] for b in blist) + BREATH[name] * len(blist)
            if not (os.path.exists(seg) and abs(dur(seg) - segdur) < 0.35):
                seg_image(img, segdur, i, seg, W, H)
            vsegs_note = "+".join(blist)
            print(f"[{name}] seg {i:02d} {vsegs_note} <- {img} {segdur:.1f}s", flush=True)
        return None
    # final: concat + sfx + mux
    vsegs = []
    if name == "long":
        vsegs.append(os.path.join(tmpd, "title.mp4"))
    for i in range(len(segs)):
        vsegs.append(os.path.join(tmpd, f"s{i:02d}.mp4"))
    for s in vsegs:
        assert os.path.exists(s), f"segmen hilang: {s}"
    lst = os.path.join(tmpd, "list.txt")
    with open(lst, "w") as f:
        for s in vsegs: f.write(f"file '{s}'\n")
    vcat = os.path.join(tmpd, "vcat.mp4")
    run(["-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vcat])
    # SFX
    vo_offset = 3.0 if name == "long" else 0.0
    total_a = dd["total_vo"] + vo_offset + 1.2
    sfxf = os.path.join(tmpd, "sfx.mp3")
    sfx_track(name, sfx_events(name), total_a, sfxf)
    ass = build_ass(name, W, H, vo_offset)
    run(["-y", "-i", vcat, "-i", dd["voice_file"], "-i", sfxf,
         "-filter_complex",
         "[1:a]adelay=%d|%d,aresample=44100[vo];[vo][2:a]amix=inputs=2:duration=first:dropout_transition=0,aresample=44100[aout]" % (int(vo_offset*1000), int(vo_offset*1000)),
         "-vf", f"ass={ass}",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", out])
    d, sz = dur(out), os.path.getsize(out)/1e6
    print(f"OK [{name}]: {out} {d:.1f}s {sz:.1f}MB")
    assert sz < 100, "file >100MB!"
    return d, sz

if __name__ == "__main__":
    # mode: assemble.py <name> [seg <lo> <hi> | final]
    #   tanpa mode  = semua (kompatibel lama)
    #   seg lo hi   = render segmen lo..hi saja (untuk paralel 2 waiter)
    #   final       = concat + sfx + mux saja
    args = sys.argv[1:]
    if len(args) >= 2 and args[1] == "seg":
        name, lo, hi = args[0], int(args[2]), int(args[3])
        build_one(name, None, seg_lo=lo, seg_hi=hi)
    elif len(args) >= 2 and args[1] == "final":
        name = args[0]
        out = os.path.join(ROOT, f"infoloker-2026-10-16-{name}.mp4")
        d, sz = build_one(name, out, final_only=True)
        json.dump({name: {"file": out, "dur": round(d,1), "mb": round(sz,1)}},
                  open(os.path.join(BD, "render_result.json"), "w"), indent=1)
        print(f"FINAL [{name}]: {d:.1f}s {sz:.1f}MB")
    else:
        targets = args or ["shorts1", "shorts2", "shorts3", "long"]
        res = {}
        for t in targets:
            out = os.path.join(ROOT, f"infoloker-2026-10-16-{t}.mp4")
            build_one(t, out)  # segmen semua
            d, sz = build_one(t, out, final_only=True)
            res[t] = {"file": out, "dur": round(d,1), "mb": round(sz,1)}
        json.dump(res, open(os.path.join(BD, "render_result.json"), "w"), indent=1)
        print(json.dumps(res, indent=1))
