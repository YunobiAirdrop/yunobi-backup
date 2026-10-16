#!/usr/bin/env python3
"""All-Python final audio (zero ffmpeg-queue acquisitions):
decode beat mp3s -> speed 1.15x (samplerate) -> concat -> mix brown-noise
bed + heartbeat under beats 008-013 -> 4s heartbeat tail for endcard ->
final_audio.wav. Also writes durasi_115.json (scaled + beat-016: 4.0)
and img/beat-016.webp from endcard.png.

SFX note: heartbeat/bed are synthesized locally (no reachable real
recordings in this environment); documented in the run log.
"""
import json, os, wave
import numpy as np
import miniaudio, samplerate

BASE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(BASE, "audio")
IMG = os.path.join(BASE, "img")
SR = 44100
SPEED = 1.15

def decode_mp3(path):
    d = miniaudio.decode_file(path, output_format=miniaudio.SampleFormat.FLOAT32,
                              nchannels=1, sample_rate=SR)
    return np.frombuffer(d.samples, dtype=np.float32).copy()

def write_wav(path, data):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

def main():
    dur = json.load(open(os.path.join(BASE, "durasi.json")))
    names = sorted(dur)
    # 1-2. decode + speedup
    voice_parts, scaled = [], {}
    for n in names:
        pcm = decode_mp3(os.path.join(AUD, f"{n}.mp3"))
        fast = samplerate.resample(pcm, 1.0 / SPEED, "sinc_best")
        voice_parts.append(fast)
        scaled[n] = round(len(fast) / SR, 2)
        print(f"  {n}: {dur[n]:.1f}s -> {scaled[n]:.1f}s", flush=True)
    voice = np.concatenate(voice_parts)
    total = len(voice) / SR
    print(f"voice total: {total/60:.1f} mnt")

    # 3. brown-noise bed, one-pole lowpass
    rng = np.random.default_rng(7)
    n = len(voice)
    brown = np.cumsum(rng.standard_normal(n).astype(np.float64))
    brown -= np.linspace(brown[0], brown[-1], n)
    brown /= np.max(np.abs(brown))
    bed = np.zeros_like(brown); alpha = 0.02
    for i in range(1, n):
        bed[i] = bed[i-1] + alpha * (brown[i] - bed[i-1])
    bed /= np.max(np.abs(bed)); bed *= 0.05

    # 4. heartbeat under scaled beats 008..013
    hb_start = sum(scaled[x] for x in names if x < "beat-008")
    hb_dur = sum(scaled[x] for x in names if "beat-008" <= x <= "beat-013")
    hb_n = int(hb_dur * SR)
    hb = np.zeros(hb_n, dtype=np.float64)
    t = np.arange(int(0.35 * SR)) / SR
    th1 = np.sin(2*np.pi*55*t) * np.exp(-t*22)
    th2 = np.sin(2*np.pi*50*t) * np.exp(-t*26) * 0.7
    pos, gap = 0.0, 60.0/62.0
    while pos < hb_dur - 0.8:
        i0 = int(pos*SR); i1 = min(hb_n, i0+len(th1)); hb[i0:i1] += th1[:i1-i0]
        j0 = int((pos+0.30)*SR); j1 = min(hb_n, j0+len(th2)); hb[j0:j1] += th2[:j1-j0]
        pos += gap
    hb /= max(1e-9, np.max(np.abs(hb))); hb *= 0.35

    # 5. mix + 4s heartbeat tail (endcard)
    mix = voice.astype(np.float64) + bed
    s0 = int(hb_start*SR)
    mix[s0:s0+hb_n] += hb
    tail_n = 4*SR
    tail = np.zeros(tail_n); pos = 0.0
    while pos < 3.2:
        i0 = int(pos*SR); i1 = min(tail_n, i0+len(th1)); tail[i0:i1] += th1[:i1-i0]
        j0 = int((pos+0.30)*SR); j1 = min(tail_n, j0+len(th2)); tail[j0:j1] += th2[:j1-j0]
        pos += gap
    tail /= max(1e-9, np.max(np.abs(tail))); tail *= 0.4
    # fade tail out over last 1.5s
    f = int(1.5*SR); tail[-f:] *= np.linspace(1, 0, f)
    mix = np.concatenate([mix, tail])

    out = os.path.join(AUD, "final_audio.wav")
    write_wav(out, mix)
    print("OK:", out, f"{len(mix)/SR/60:.1f} mnt")

    scaled["beat-016"] = 4.0
    json.dump(scaled, open(os.path.join(BASE, "durasi_115.json"), "w"), indent=1)

    # endcard -> img/beat-016.webp
    from PIL import Image
    Image.open(os.path.join(BASE, "endcard.png")).save(
        os.path.join(IMG, "beat-016.webp"), "WEBP", quality=90)
    print("OK: img/beat-016.webp, durasi_115.json")

if __name__ == "__main__":
    main()
