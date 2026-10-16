#!/usr/bin/env python3
"""Assembly Kisah Dharma LONG 2026-10-16 (fix).
Menyelesaikan dari aset parsial: 8 voiceover beats + klip Pexels (own + pinjaman).
Semua render via ffmpeg-queue.sh. Target: 1280x720, ~11.3 mnt, <100MB.
"""
import os, subprocess, sys, json

BASE = "/home/hatch/workspace/youtube-otomatis/kisah-dharma"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
JB = "/home/hatch/workspace/youtube-otomatis/jejak-buddha/2026-10-16-shorts/clips"
KA = "/home/hatch/workspace/youtube-otomatis/kisah-alkitab/2026-10-16/footage"

# (path, durasi)
CLIPS = [
    (f"{BASE}/clips/api_unggun.mp4", 21.7),      # 0
    (f"{BASE}/clips/badai_gelap.mp4", 15.5),     # 1
    (f"{BASE}/clips/bukit_kabut.mp4", 8.7),      # 2
    (f"{BASE}/clips/gunung_kabut.mp4", 13.4),    # 3
    (f"{BASE}/clips/gurun_drone.mp4", 10.1),     # 4
    (f"{BASE}/clips/gurun_langit.mp4", 10.0),    # 5
    (f"{BASE}/clips/hutan_cahaya.mp4", 51.5),   # 6
    (f"{BASE}/clips/langit_tenang.mp4", 15.7),  # 7
    (f"{BASE}/clips/lilin_meja.mp4", 26.7),     # 8
    (f"{BASE}/clips/ombak.mp4", 25.1),          # 9
    (f"{BASE}/clips/senja_rumput.mp4", 9.5),    # 10
    (f"{BASE}/clips/sungai_alir.mp4", 14.2),    # 11
    (f"{BASE}/clips/sungai_hutan.mp4", 16.5),   # 12
    (f"{BASE}/clips/sunrise_kabut.mp4", 17.4),  # 13
    (f"{JB}/c01.mp4", 16.8),   # 14 lilin
    (f"{JB}/c02.mp4", 14.0),   # 15
    (f"{JB}/c03.mp4", 8.4),    # 16
    (f"{JB}/c04.mp4", 17.2),   # 17 star trails
    (f"{JB}/c05.mp4", 8.3),    # 18
    (f"{JB}/c06.mp4", 13.2),   # 19
    (f"{JB}/c07.mp4", 14.5),   # 20
    (f"{JB}/c08.mp4", 10.0),   # 21
    (f"{JB}/c09.mp4", 14.5),   # 22
    (f"{JB}/c10.mp4", 12.7),   # 23
    (f"{KA}/clip1.mp4", 12.3), # 24
    (f"{KA}/clip2.mp4", 18.6), # 25 gurun unta
    (f"{KA}/clip3.mp4", 14.8), # 26
    (f"{KA}/clip4.mp4", 8.4),  # 27
    (f"{KA}/clip5.mp4", 27.6), # 28
    (f"{KA}/clip6.mp4", 20.0), # 29
    (f"{KA}/clip7.mp4", 13.6), # 30
    (f"{KA}/clip8.mp4", 15.1), # 31
]

# beat -> daftar indeks klip (urutan pemakaian)
BEAT_CLIPS = {
    1: [1, 5, 25, 7],                    # hook: badai, gurun, unta, langit
    2: [11, 12, 13, 9, 15, 20, 26, 29, 22, 10],  # kelahiran: sungai, sunrise, ombak
    3: [0, 4, 17, 28, 2, 27, 3],        # murid ditolak: api, gurun, bintang
    4: [6, 14, 19, 23, 24, 30, 31, 16, 18],  # turnamen: hutan cahaya, terang
    5: [8, 21, 1, 2],                    # kutukan: lilin, gelap (reuse 1,2)
    6: [5, 9, 0, 10, 3],                 # perang: gurun, ombak, api (reuse)
    7: [8, 13, 14, 7],                   # dharma: lilin, sunrise (reuse)
    8: [11, 12, 6],                      # penutup: sungai, hutan (reuse)
}

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("GAGAL:", " ".join(cmd[:8])); print(r.stderr[-1500:]); sys.exit(1)
    return r

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=index", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())

def main():
    outdir = f"{BASE}/2026-10-16-fix"
    segdir = f"{outdir}/_segs"
    os.makedirs(segdir, exist_ok=True)
    final = f"{outdir}/kisahdharma-2026-10-16-long.mp4"

    beats = [probe(f"{BASE}/audio/beat{i}.mp3") for i in range(1, 9)]
    print("beat:", [round(b, 1) for b in beats], "total:", round(sum(beats), 1), flush=True)

    used_clips = {}  # clip_idx -> berapa kali dipakai (untuk variasi)
    segfiles, seg = [], 0
    for bi, dur in enumerate(beats, 1):
        need = dur + 0.6
        acc = 0.0
        for ci in BEAT_CLIPS[bi]:
            if acc >= need:
                break
            src, cdur = CLIPS[ci]
            take = min(cdur, need - acc)
            if take < 2.5:
                continue
            # variasi untuk pemakaian ulang: hflip + offset beda
            n_use = used_clips.get(ci, 0)
            used_clips[ci] = n_use + 1
            if n_use == 0:
                start = max(0, (cdur - take) / 2)
                flip = ""
            else:
                start = max(0, (cdur - take) * (0.15 + 0.35 * (n_use % 3)))
                flip = "hflip,"
            part = f"{segdir}/s{seg:03d}.mp4"
            vf = (f"{flip}scale=1280:720:force_original_aspect_ratio=increase,"
                  f"crop=1280:720,noise=alls=6:allf=t")
            if not os.path.exists(part) or probe(part) < take * 0.9:
                run([FQ, "-y", "-ss", f"{start:.1f}", "-i", src, "-t", f"{take:.1f}",
                     "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                     "-crf", "20", "-an", part])
            segfiles.append(part); acc += take; seg += 1
        if acc < need - 1:
            print(f"PERINGATAN beat {bi}: kurang {acc:.1f}/{need:.1f}"); sys.exit(1)
        print(f"beat {bi}: {acc:.1f}s dari {len([s for s in segfiles])} segmen", flush=True)

    # title card 4 detik
    run([FQ, "-y", "-loop", "1", "-i", f"{BASE}/titlecard.png",
         "-vf", "scale=1280:720,zoompan=z='1+0.02*on':d=100:s=1280x720:fps=25,"
                "noise=alls=6:allf=t",
         "-t", "4", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-an", f"{segdir}/seg_title.mp4"])

    # concat
    with open(f"{segdir}/list.txt", "w") as f:
        f.write(f"file '{segdir}/seg_title.mp4'\n")
        for s in segfiles:
            f.write(f"file '{s}'\n")
    run([FQ, "-y", "-f", "concat", "-safe", "0", "-i", f"{segdir}/list.txt",
         "-c", "copy", f"{outdir}/video_nosound.mp4"])

    # voiceover gabung (delay 4s untuk title card)
    vdur = probe(f"{outdir}/video_nosound.mp4")
    run([FQ, "-y"] + [x for i in range(1, 9) for x in ("-i", f"{BASE}/audio/beat{i}.mp3")] +
        ["-filter_complex",
         "[0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a]concat=n=8:v=0:a=1,"
         "aresample=44100,adelay=4000|4000[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "128k", f"{outdir}/vo_full.m4a"])

    # ambien dari klip ber-audio, vol rendah
    amb_srcs = [ci for ci in sorted(set(sum(BEAT_CLIPS.values(), [])))
                if has_audio(CLIPS[ci][0])]
    inputs, parts, vols = [], [], []
    for j, ci in enumerate(amb_srcs):
        inputs += ["-i", CLIPS[ci][0]]
        parts.append(f"[{j}:a]volume=0.06,aresample=44100,apad[a{j}]")
        vols.append(f"[a{j}]")
    fc = ";".join(parts) + ";" + "".join(vols) + \
         f"amix=inputs={len(amb_srcs)}:normalize=0,atrim=0:{vdur:.1f}[amb]"
    run([FQ, "-y"] + inputs + ["-filter_complex", fc, "-map", "[amb]",
         "-c:a", "aac", "-b:a", "96k", f"{outdir}/amb_full.m4a"])

    # mux final, bitrate dinamis target ~88MB
    vo_dur = probe(f"{outdir}/vo_full.m4a")
    vbr = max(600, int((88 * 1024 * 1024 * 8 / vo_dur - 128000) / 1000))
    print(f"VO {vo_dur:.1f}s -> vbr {vbr}k", flush=True)
    run([FQ, "-y", "-i", f"{outdir}/video_nosound.mp4",
         "-i", f"{outdir}/vo_full.m4a", "-i", f"{outdir}/amb_full.m4a",
         "-filter_complex", "[1:a][2:a]amix=inputs=2:normalize=0[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{vbr}k",
         "-maxrate", f"{int(vbr*1.4)}k", "-bufsize", f"{vbr*2}k",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         "-shortest", final])
    sz = os.path.getsize(final)
    print(f"FINAL: {final} {sz/1048576:.1f}MB {probe(final):.0f}s", flush=True)
    assert sz < 100 * 1048576, "LEBIH DARI 100MB!"

if __name__ == "__main__":
    main()
