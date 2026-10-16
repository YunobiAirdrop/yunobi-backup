#!/usr/bin/env python3
"""Mega-render LONG Info Loker: SATU panggilan ffmpeg-queue.sh untuk seluruh video.
- title.mp4 + s00-s09 (cache) + 16 segmen zoompan baru -> concat -> grain/vignette/caption
- VO (49 beat) + 11 SFX tersinkron -> amix
- 1280x720, veryfast, crf 23, <100MB.
Menunggu voiceover_full_long.mp3 selesai dibangun rakit_vo.py (cek durasi).
"""
import json, os, subprocess, sys, time

ROOT = "/home/hatch/workspace/youtube-otomatis/infoloker/2026-10-16"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
FR = os.path.join(ROOT, "frames")
BD = os.path.join(ROOT, "build")
SFXD = os.path.join(BD, "sfx")
TMPD = os.path.join(BD, "_segs_long")
sys.path.insert(0, BD)
from assemble import build_ass, sfx_events, D as _D  # noqa

W, H = 1280, 720
OUT = os.path.join(ROOT, "infoloker-2026-10-16-long.mp4")

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 0.0

def main():
    D = json.load(open(os.path.join(BD, "durasi.json")))
    dd = D["long"]
    assert len(dd["beats"]) == 49, "durasi.json belum 49 beat!"
    import assemble
    beats_txt = assemble.beats_txt
    SEGMENTS = assemble.SEGMENTS["long"]
    assert len(SEGMENTS) == 26

    # 1. caption ASS (49 beat, offset 3.0)
    ass = build_ass("long", W, H, 3.0)
    print("ASS OK", flush=True)

    # 2. bangun command
    inputs = []
    # 0: title, 1-10: s00-s09
    inputs += ["-i", os.path.join(TMPD, "title.mp4")]
    for i in range(10):
        inputs += ["-i", os.path.join(TMPD, f"s{i:02d}.mp4")]
    # 11-26: 16 PNG segmen baru (s10-s25)
    newsegs = SEGMENTS[10:]
    for blist, img in newsegs:
        p = os.path.join(FR, img + ".png")
        assert os.path.exists(p), img
        inputs += ["-i", p]
    # 27-75: 49 beat VO
    bids = sorted(beats_txt["long"].keys())
    VO0 = 27
    for b in bids:
        inputs += ["-i", os.path.join(ROOT, "voice", f"{b}.mp3")]
    # 76-86: 11 SFX
    events = sfx_events("long")  # [(t, wav, vol)] dengan offset 3.0
    SFX0 = VO0 + len(bids)
    for t, wav, vol in events:
        inputs += ["-i", os.path.join(SFXD, wav)]
    print(f"total input: {len(inputs)//2}", flush=True)

    fc = []
    vlabels = ["[0:v]"]
    for i in range(1, 11):
        vlabels.append(f"[{i}:v]")
    # zoompan untuk 16 PNG (input idx 11..26)
    def zv(i, n):
        v = (10 + i) % 4
        cx = "iw/2-(iw/zoom/2)"; cy = "ih/2-(ih/zoom/2)"
        if v == 0: return f"z='1+0.15*on/{n}'", f"x='{cx}'", f"y='{cy}'"
        if v == 1: return f"z='1.15-0.15*on/{n}'", f"x='{cx}'", f"y='{cy}'"
        if v == 2: return f"z='1+0.12*on/{n}'", f"x='(iw-iw/zoom)*on/{n}'", f"y='{cy}'"
        return f"z='1+0.12*on/{n}'", f"x='{cx}'", f"y='(ih-ih/zoom)*(1-on/{n})'"
    for i, (blist, img) in enumerate(newsegs):
        segdur = sum(dd["beats"][b] for b in blist) + 0.6 * len(blist)
        n = max(15, int(round(segdur * 30)))
        z, x, y = zv(i, n)
        ii = 11 + i
        fc.append(
            f"[{ii}:v]scale=1920:1080:force_original_aspect_ratio=increase,"
            f"crop=1920:1080,zoompan={z}:d={n}:{x}:{y}:s={W}x{H}:fps=30,"
            f"format=yuv420p[vn{i}]")
        vlabels.append(f"[vn{i}]")
        print(f"  seg baru {10+i}: {'+'.join(blist)} <- {img} {segdur:.1f}s", flush=True)
    ncat = len(vlabels)
    fc.append("".join(vlabels) + f"concat=n={ncat}:v=1:a=0,"
              f"eq=contrast=1.06:saturation=0.94:brightness=-0.015,"
              f"noise=alls=6:allf=t,vignette=PI/6,format=yuv420p,"
              f"ass={ass}[vcat]")
    # audio: 49 beat VO @ starts+3.0s, lalu SFX
    for j, b in enumerate(bids):
        ii = VO0 + j
        ms = int((dd["starts"][b] + 3.0) * 1000)
        fc.append(f"[{ii}:a]adelay={ms}|{ms}[v{j}]")
    fc.append("".join(f"[v{j}]" for j in range(len(bids))) +
              f"amix=inputs={len(bids)}:normalize=0,aresample=44100[vo]")
    slabels = []
    for j, (t, wav, vol) in enumerate(events):
        si = SFX0 + j
        ms = int(t * 1000)
        fc.append(f"[{si}:a]adelay={ms}|{ms},volume={vol},aresample=44100[s{j}]")
        slabels.append(f"[s{j}]")
    fc.append("".join(slabels) + f"amix=inputs={len(slabels)}:normalize=0[sfx]")
    fc.append("[vo][sfx]amix=inputs=2:duration=first:dropout_transition=0,aresample=44100[aout]")

    cmd = (["-y"] + inputs +
           ["-filter_complex", ";".join(fc),
            "-map", "[vcat]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            "-shortest", OUT])
    print("render final via ffmpeg-queue (1 slot, ~10 mnt encode)...", flush=True)
    r = subprocess.run([FQ] + cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL:\n", r.stderr[-1500:]); sys.exit(1)
    d, sz = dur(OUT), os.path.getsize(OUT) / 1e6
    print(f"OK long: {OUT} {d:.1f}s {sz:.1f}MB")
    assert sz < 100
    json.dump({"long": {"file": OUT, "dur": round(d, 1), "mb": round(sz, 1)}},
              open(os.path.join(BD, "render_result_long.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
