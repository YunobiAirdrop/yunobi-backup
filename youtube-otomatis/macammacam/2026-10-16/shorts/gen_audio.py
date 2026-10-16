#!/usr/bin/env python3
"""Generate per-beat ID voiceover (Mudiwa) untuk 3 shorts macammacam."""
import re, subprocess, json, os, sys

BASE = "/home/hatch/workspace/youtube-otomatis/macammacam/2026-10-16/shorts"
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:mudiwa"
GAP = 0.4
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

def ffprobe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0

def parse_beats(script_path):
    text = open(script_path).read()
    beats = {}
    parts = re.split(r"^## (BEAT \d{3})", text, flags=re.M)
    for i in range(1, len(parts), 2):
        name_raw, body = parts[i], parts[i + 1]
        name = "beat-" + name_raw.split()[1]
        lines = []
        for ln in body.strip().splitlines():
            ln = ln.strip()
            if not ln:
                continue
            if ln.startswith("[ON SCREEN:"):
                continue
            if ln.startswith("##"):
                continue
            lines.append(ln)
        narration = " ".join(lines)
        if narration:
            beats[name] = narration
    return beats

def process(d):
    script = os.path.join(d, "script.md")
    aud = os.path.join(d, "audio")
    os.makedirs(aud, exist_ok=True)
    beats = parse_beats(script)
    print(f"[{os.path.basename(d)}] {len(beats)} beats", flush=True)
    dur = {}
    for name in sorted(beats):
        out = os.path.join(aud, f"{name}.mp3")
        if os.path.exists(out) and ffprobe_dur(out) > 1:
            print(f"  skip {name}")
        else:
            print(f"  TTS {name} ...", flush=True)
            r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language",
                                "id", "--speed", "95", "--output", out,
                                "--text-stdin"],
                               input=beats[name].encode(), capture_output=True)
            if r.returncode != 0 or not os.path.exists(out) or ffprobe_dur(out) < 1:
                print(f"GAGAL TTS {name}: {r.stderr.decode()[:300]}")
                sys.exit(1)
        dur[name] = round(ffprobe_dur(out) + GAP, 2)
    # gabung voiceover
    full = os.path.join(aud, "voiceover.mp3")
    inputs, fc_parts = [], []
    for i, name in enumerate(sorted(beats)):
        inputs += ["-i", os.path.join(aud, f"{name}.mp3")]
        fc_parts.append(f"[{i}:a]apad=whole_dur={dur[name]:.2f}[a{i}]")
    fc = ";".join(fc_parts) + ";" + "".join(f"[a{i}]" for i in range(len(beats))) + f"concat=n={len(beats)}:v=0:a=1[out]"
    r = subprocess.run([FQ, "-y"] + inputs + ["-filter_complex", fc,
                       "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "128k", full],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL concat:", r.stderr[-500:]); sys.exit(1)
    json.dump(dur, open(os.path.join(aud, "durasi.json"), "w"), indent=1)
    total = ffprobe_dur(full)
    print(f"  OK voiceover.mp3 = {total:.1f}s", flush=True)

for sub in ["shorts1", "shorts2", "shorts3"]:
    process(os.path.join(BASE, sub))
print("SELESAI SEMUA TTS")
