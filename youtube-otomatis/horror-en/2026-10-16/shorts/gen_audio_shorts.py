#!/usr/bin/env python3
"""TTS per-beat EN voiceover untuk 3 shorts horror via /opt/hatch/bin/tts.
Voice: avocado_v2:casper, speed 95 (sama seperti long)."""
import re, subprocess, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:casper"
GAP = 0.4

def ffprobe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def parse_beats(script_path):
    text = open(script_path).read()
    beats = {}
    parts = re.split(r"^### (beat-\d{3})\s*$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        name, body = parts[i], parts[i + 1]
        lines = []
        for ln in body.strip().splitlines():
            ln = ln.strip()
            if not ln:
                continue
            if ln.startswith("**[ON SCREEN:") or ln.startswith("**IMAGE PROMPT:**"):
                continue
            if ln.startswith("**") and ln.endswith("**"):
                continue
            lines.append(ln)
        beats[name] = " ".join(lines)
    return beats

def process_short(sdir):
    aud = os.path.join(sdir, "audio")
    os.makedirs(aud, exist_ok=True)
    beats = parse_beats(os.path.join(sdir, "script.md"))
    print(f"[{os.path.basename(sdir)}] {len(beats)} beats")
    dur = {}
    chunks = []
    for name in sorted(beats):
        out = os.path.join(aud, f"{name}.mp3")
        if not (os.path.exists(out) and ffprobe_dur(out) > 1):
            print(f"  TTS {name} ...", flush=True)
            r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language",
                                "en", "--speed", "95", "--output", out,
                                "--text-stdin"],
                               input=beats[name].encode(), capture_output=True)
            if r.returncode != 0 or not os.path.exists(out):
                print(f"GAGAL TTS {name}: {r.stderr.decode()[:300]}")
                sys.exit(1)
            if ffprobe_dur(out) < 1:
                print(f"GAGAL TTS {name}: durasi 0"); sys.exit(1)
        raw_d = ffprobe_dur(out)
        chunk = os.path.join(aud, f"{name}_chunk.mp3")
        total = raw_d + GAP
        subprocess.run(
            ["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh",
             "-y", "-v", "error", "-i", out, "-af",
             f"apad=whole_dur={total:.2f}", "-c:a", "libmp3lame", "-b:a",
             "128k", chunk],
            capture_output=True, check=True, cwd="/home/hatch/workspace/youtube-otomatis")
        d = ffprobe_dur(chunk)
        dur[name] = round(d, 2)
        chunks.append(chunk)
        print(f"  {name}: {d:.1f}s", flush=True)
    lst = os.path.join(aud, "chunks.txt")
    with open(lst, "w") as f:
        for c in chunks:
            f.write(f"file '{c}'\n")
    full = os.path.join(aud, "voiceover_full.mp3")
    subprocess.run(
        ["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y", "-v",
         "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", full],
        capture_output=True, check=True)
    json.dump(dur, open(os.path.join(sdir, "durasi.json"), "w"), indent=1)
    total_s = sum(dur.values())
    print(f"  OK: voiceover_full.mp3 = {total_s:.1f}s ({total_s/60:.2f} mnt)")

if __name__ == "__main__":
    for s in ["s1-lick", "s2-hitchhiker", "s3-babysitter"]:
        process_short(os.path.join(BASE, s))
    print("SEMUA TTS SELESAI")
