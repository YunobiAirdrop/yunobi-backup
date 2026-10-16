#!/usr/bin/env python3
"""Mix voiceover with synthesized dark ambience bed + heartbeat SFX
under the cases section (beats 008-013). Output: audio/final_audio.m4a.

NOTE: SFX are synthesized locally with numpy/ffmpeg (no downloadable
real recordings were reachable in this environment); documented as such.
"""
import json, subprocess, os, wave, struct
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(BASE, "audio")
FQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
SR = 44100

def run(cmd, **kw):
    subprocess.run(cmd, check=True, capture_output=True, **kw)

def main():
    dur = json.load(open(os.path.join(BASE, "durasi.json")))
    names = sorted(dur)
    total = sum(dur.values())
    # heartbeat under beats 008..013 (the three cases = climax)
    start = sum(dur[n] for n in names if n < "beat-008")
    hb_dur = sum(dur[n] for n in names if "beat-008" <= n <= "beat-013")
    print(f"total {total:.1f}s, heartbeat {start:.1f}s -> {start+hb_dur:.1f}s")

    # --- ambience bed: lowpassed brown noise, very quiet ---
    n = int(total * SR)
    white = np.random.default_rng(7).standard_normal(n)
    brown = np.cumsum(white)
    brown = brown - np.linspace(brown[0], brown[-1], n)  # remove drift
    brown /= np.max(np.abs(brown))
    # one-pole lowpass ~ heavy smoothing for rumble
    alpha = 0.02
    bed = np.zeros_like(brown)
    for i in range(1, n):
        bed[i] = bed[i-1] + alpha * (brown[i] - bed[i-1])
    bed /= np.max(np.abs(bed))
    bed *= 0.05  # -26 dB-ish
    bed_path = os.path.join(AUD, "bed.wav")
    write_wav(bed_path, bed)

    # --- heartbeat: lub-dub pairs at ~62 bpm ---
    hb_n = int(hb_dur * SR)
    hb = np.zeros(hb_n)
    beat_gap = 60.0 / 62.0
    t = np.arange(int(0.35 * SR)) / SR
    thump = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 22)
    thump2 = np.sin(2 * np.pi * 50 * t) * np.exp(-t * 26) * 0.7
    pos = 0.0
    while pos < hb_dur - 0.8:
        i0 = int(pos * SR)
        i1 = min(hb_n, i0 + len(thump))
        hb[i0:i1] += thump[:i1-i0]
        j0 = int((pos + 0.30) * SR)
        j1 = min(hb_n, j0 + len(thump2))
        hb[j0:j1] += thump2[:j1-j0]
        pos += beat_gap
    hb /= max(1e-6, np.max(np.abs(hb)))
    hb *= 0.35
    hb_path = os.path.join(AUD, "heartbeat.wav")
    write_wav(hb_path, hb)

    voice = os.path.join(AUD, "voiceover_full.mp3")
    out = os.path.join(AUD, "final_audio.m4a")
    start_ms = int(start * 1000)
    run([FQ, "-y", "-v", "error",
         "-i", voice, "-i", bed_path, "-i", hb_path,
         "-filter_complex",
         f"[2:a]adelay={start_ms}|{start_ms}[hb];"
         "[0:a][1:a][hb]amix=inputs=3:normalize=0:duration=longest[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "128k", out])
    print("OK:", out)

def write_wav(path, data):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

if __name__ == "__main__":
    main()
