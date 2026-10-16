#!/usr/bin/env python3
"""Synthesize dark ambience bed (brown noise, heavy lowpass, ~-26dBFS RMS) with numpy,
mix under voiceover_full.mp3 via ffmpeg-queue.sh amix -> audio/final_audio.m4a.
NOTE: no downloadable recordings used; bed is fully synthesized locally."""
import subprocess, os
import numpy as np
import wave

WD = "/home/hatch/workspace/youtube-otomatis/mystery-en/2026-10-16/v2/short3"
FFQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"
SR = 44100

def durf(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

os.chdir(os.path.join(WD, "audio"))
dur = durf("voiceover_full.mp3")
print(f"voiceover dur: {dur:.2f}s", flush=True)
n = int(SR * dur)
rng = np.random.default_rng(20261016)

# brown noise: integrate white noise, remove DC drift
white = rng.standard_normal(n)
brown = np.cumsum(white)
brown -= np.linspace(brown[0], brown[-1], n)  # detrend drift

# heavy lowpass: brickwall at 140 Hz via FFT
spec = np.fft.rfft(brown)
freqs = np.fft.rfftfreq(n, 1 / SR)
spec[freqs > 140] = 0
bed = np.fft.irfft(spec, n)

# slow swell LFO for a "breathing" dark room feel (0.07 Hz, +/-20%)
t = np.arange(n) / SR
lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.07 * t)
bed *= lfo

# fades to avoid clicks
fade = int(SR * 1.5)
bed[:fade] *= np.linspace(0, 1, fade)
bed[-fade:] *= np.linspace(1, 0, fade)

# normalize to -26 dBFS RMS
rms = np.sqrt(np.mean(bed ** 2))
bed *= (10 ** (-26 / 20)) / rms
print(f"bed RMS set to -26 dBFS (peak {20*np.log10(np.max(np.abs(bed))):.1f} dBFS)", flush=True)

pcm = np.clip(bed, -1, 1)
pcm16 = (pcm * 32767).astype(np.int16)
with wave.open("bed.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm16.tobytes())
print("bed.wav written", flush=True)

print("mixing (amix, voice dominant)...", flush=True)
r = subprocess.run([FFQ, "-y", "-v", "error",
                    "-i", "voiceover_full.mp3", "-i", "bed.wav",
                    "-filter_complex", "amix=inputs=2:duration=longest:normalize=0",
                    "-c:a", "aac", "-b:a", "128k", "final_audio.m4a"],
                   capture_output=True, text=True)
print("rc:", r.returncode, r.stderr[-300:] if r.stderr else "")
assert r.returncode == 0, "mix failed"
md = durf("final_audio.m4a")
print(f"final_audio.m4a: {md:.2f}s (target {dur:.2f}s)")
assert abs(md - dur) < 0.5, "final audio duration mismatch"
print("OK: audio/final_audio.m4a")
