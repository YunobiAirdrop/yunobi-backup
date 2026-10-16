#!/usr/bin/env python3
"""Synthesize a dark ambience bed (brown noise, heavy lowpass) locally with numpy.
NOTE: no downloadable real recordings were used; this bed is 100% synthesized locally.
Bed sits ~-26dB below the voiceover (voice clearly dominant)."""
import numpy as np, subprocess, os, wave, struct

WORK = os.path.dirname(os.path.abspath(__file__))
SR = 44100

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

FFQ = "/home/hatch/workspace/youtube-otomatis/ffmpeg-queue.sh"

def decode(path):
    r = subprocess.run([FFQ, "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32)

voice_path = os.path.join(WORK, "audio", "voiceover_full.mp3")
vdur = dur(voice_path)
voice = decode(voice_path)
voice_rms = float(np.sqrt(np.mean(voice ** 2))) or 1e-6

n = int((vdur + 1.0) * SR)
rng = np.random.default_rng(19871122)
white = rng.standard_normal(n).astype(np.float64)
# brown-ish noise via leaky integrator
brown = np.zeros(n)
leak = 0.998
for i in range(1, n):
    brown[i] = (brown[i - 1] + 0.02 * white[i]) * leak
# heavy lowpass: one-pole at ~120 Hz
alpha = 1 - np.exp(-2 * np.pi * 120 / SR)
filt = np.zeros(n)
for i in range(1, n):
    filt[i] = filt[i - 1] + alpha * (brown[i] - filt[i - 1])
bed = filt / (np.max(np.abs(filt)) + 1e-9)
# slow swells for a "dark room tone" feel
t = np.arange(n) / SR
swell = 0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * t + 1.0)
bed = bed * swell
# fades
fi = int(2.0 * SR)
bed[:fi] *= np.linspace(0, 1, fi)
bed[-fi:] *= np.linspace(1, 0, fi)
# scale: bed RMS = voice RMS * 10^(-26/20)  (approx -26dB under voice)
bed_rms = float(np.sqrt(np.mean(bed ** 2))) or 1e-9
bed = bed * (voice_rms * 10 ** (-26 / 20) / bed_rms)
stereo = np.stack([bed, bed], axis=1).astype(np.float32)
bed_wav = os.path.join(WORK, "audio", "bed.wav")
with wave.open(bed_wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(4); w.setframerate(SR)
    w.writeframes(stereo.tobytes())

print(f"bed: {vdur + 1.0:.1f}s, voice RMS={voice_rms:.4f}, bed RMS={float(np.sqrt(np.mean(bed**2))):.5f}")
print("BED_OK", bed_wav)
