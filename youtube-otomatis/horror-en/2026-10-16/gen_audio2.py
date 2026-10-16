#!/usr/bin/env python3
"""Finish TTS for remaining beats (no ffmpeg), then build durasi.json from
raw beat durations and concat voiceover_full.mp3 in ONE queued ffmpeg call."""
import re, subprocess, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(BASE, "audio")
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:casper"
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

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

def main():
    beats = parse_beats(os.path.join(BASE, "script.md"))
    for name in sorted(beats):
        out = os.path.join(AUD, f"{name}.mp3")
        if os.path.exists(out) and ffprobe_dur(out) > 1:
            print(f"  skip {name} (ada)")
            continue
        print(f"  TTS {name} ...", flush=True)
        r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language",
                            "en", "--speed", "95", "--output", out,
                            "--text-stdin"],
                           input=beats[name].encode(), capture_output=True)
        if r.returncode != 0 or not os.path.exists(out) or ffprobe_dur(out) < 1:
            print(f"GAGAL TTS {name}"); sys.exit(1)
    # durasi.json dari raw mp3
    dur = {}
    for name in sorted(beats):
        d = ffprobe_dur(os.path.join(AUD, f"{name}.mp3"))
        dur[name] = round(d, 2)
    json.dump(dur, open(os.path.join(BASE, "durasi.json"), "w"), indent=1)
    print(f"durasi.json: {sum(dur.values())/60:.1f} mnt")
    # concat SEKALI via queue
    lst = os.path.join(AUD, "rawlist.txt")
    with open(lst, "w") as f:
        for name in sorted(beats):
            f.write(f"file '{os.path.join(AUD, name + '.mp3')}'\n")
    full = os.path.join(AUD, "voiceover_full.mp3")
    subprocess.run([FQ, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", full],
                   capture_output=True, check=True)
    print(f"OK: voiceover_full.mp3 = {ffprobe_dur(full)/60:.1f} mnt")

if __name__ == "__main__":
    main()
