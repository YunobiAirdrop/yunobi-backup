#!/usr/bin/env python3
"""Generate per-beat EN voiceover via /opt/hatch/bin/tts, then build
voiceover_full.mp3 (each beat + 0.5s tail silence) and durasi.json."""
import re, subprocess, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(BASE, "audio")
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:casper"
GAP = 0.5  # seconds of silence appended after each beat

def ffprobe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def parse_beats(script_path):
    text = open(script_path).read()
    beats = {}
    # split on "### beat-NNN" headers
    parts = re.split(r"^### (beat-\d{3})\s*$", text, flags=re.M)
    # parts[0] = header junk, then pairs (name, body)
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
        narration = " ".join(lines)
        beats[name] = narration
    return beats

def main():
    beats = parse_beats(os.path.join(BASE, "script.md"))
    print(f"{len(beats)} beats parsed")
    os.makedirs(AUD, exist_ok=True)
    dur = {}
    chunks = []
    for name in sorted(beats):
        out = os.path.join(AUD, f"{name}.mp3")
        if not (os.path.exists(out) and ffprobe_dur(out) > 1):
            print(f"  TTS {name} ...", flush=True)
            r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language",
                                "en", "--speed", "95", "--output", out,
                                "--text-stdin"],
                               input=beats[name].encode(), capture_output=True)
            if r.returncode != 0 or not os.path.exists(out):
                print(f"GAGAL TTS {name}: {r.stderr.decode()[:300]}")
                sys.exit(1)
            # validate content non-trivial
            if ffprobe_dur(out) < 1:
                print(f"GAGAL TTS {name}: durasi 0"); sys.exit(1)
        # append GAP seconds of silence -> chunk
        raw_d = ffprobe_dur(out)
        chunk = os.path.join(AUD, f"{name}_chunk.mp3")
        total = raw_d + GAP
        subprocess.run(
            ["./ffmpeg-queue.sh" if False else "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh",
             "-y", "-v", "error", "-i", out, "-af",
             f"apad=whole_dur={total:.2f}", "-c:a", "libmp3lame", "-b:a",
             "128k", chunk],
            capture_output=True, check=True, cwd="/home/hatch/workspace/youtube-otomatis")
        d = ffprobe_dur(chunk)
        dur[name] = round(d, 2)
        chunks.append(chunk)
        print(f"  {name}: {d:.1f}s", flush=True)
    # concat chunks -> voiceover_full.mp3
    lst = os.path.join(AUD, "chunks.txt")
    with open(lst, "w") as f:
        for c in chunks:
            f.write(f"file '{c}'\n")
    full = os.path.join(AUD, "voiceover_full.mp3")
    subprocess.run(
        ["/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh", "-y", "-v",
         "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", full],
        capture_output=True, check=True)
    json.dump(dur, open(os.path.join(BASE, "durasi.json"), "w"), indent=1)
    total_min = sum(dur.values()) / 60
    print(f"OK: voiceover_full.mp3 = {ffprobe_dur(full)/60:.1f} mnt, "
          f"durasi.json total {total_min:.1f} mnt")

if __name__ == "__main__":
    main()
