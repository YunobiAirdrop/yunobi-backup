#!/usr/bin/env python3
"""Build per-beat chunk mp3s (raw + 0.5s tail) in ONE ffmpeg call via ffmpeg-queue.sh,
then concat to voiceover_full.mp3 and write durasi.json."""
import subprocess, json, os

WD = "/home/hatch/workspace/youtube-otomatis/mystery-en/2026-10-16/v2/short3"
FFQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
beats = [f"beat-{i:03d}" for i in range(1, 7)]

def durf(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

os.chdir(os.path.join(WD, "audio"))
durs = {}
for b in beats:
    raw = durf(f"{b}.mp3")
    assert raw > 1, f"{b}.mp3 too short/missing"
    durs[b] = round(raw + 0.5, 3)

# one ffmpeg invocation, 6 inputs -> 6 chunk outputs
cmd = [FFQ, "-y", "-v", "error"]
for b in beats:
    cmd += ["-i", f"{b}.mp3"]
fc = ";".join(f"[{i}:a]apad=whole_dur={durs[b]:.3f}[a{i}]" for i, b in enumerate(beats))
cmd += ["-filter_complex", fc]
for i, b in enumerate(beats):
    cmd += ["-map", f"[a{i}]", "-c:a", "libmp3lame", "-b:a", "128k", f"{b}_chunk.mp3"]
print("running chunk build (one ffmpeg call)...", flush=True)
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc:", r.returncode, r.stderr[-500:] if r.stderr else "")
assert r.returncode == 0, "chunk build failed"

for b in beats:
    cd_ = durf(f"{b}_chunk.mp3")
    assert abs(cd_ - durs[b]) < 0.15, f"{b} chunk dur mismatch {cd_} vs {durs[b]}"

# concat chunks -> voiceover_full.mp3
with open("chunks.txt", "w") as f:
    for b in beats:
        f.write(f"file '{os.path.abspath(f'{b}_chunk.mp3')}'\n")
r = subprocess.run([FFQ, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", "chunks.txt", "-c", "copy", "voiceover_full.mp3"],
                   capture_output=True, text=True)
assert r.returncode == 0, "concat failed: " + r.stderr[-500:]
total = durf("voiceover_full.mp3")
print(f"voiceover_full.mp3: {total:.2f}s")
assert 50 <= total <= 65, f"total {total:.1f}s outside 50-65s window!"

json.dump({b: durs[b] for b in beats}, open("durasi.json", "w"), indent=1)
os.remove("chunks.txt")
print("durasi.json written:", durs)
print("TOTAL:", round(sum(durs.values()), 2), "s")
