#!/usr/bin/env python3
"""Sintesis SFX sederhana (rekaman-asli-tersinkron) -> build/sfx/*.wav
thud, ding, coin, typing, paper, whoosh. 44.1kHz stereo."""
import numpy as np, os, wave

SR = 44100
OUT = "/home/hatch/workspace/youtube-otomatis/infoloker/2026-10-16/build/sfx"
os.makedirs(OUT, exist_ok=True)

def save(name, mono):
    mono = mono / max(1e-9, np.abs(mono).max()) * 0.9
    st = np.stack([mono, mono], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("sfx:", name, f"{len(mono)/SR:.2f}s")

def thud():
    t = np.arange(int(SR*0.7)) / SR
    s = np.sin(2*np.pi*75*t) * np.exp(-t*9)
    s += 0.3*np.sin(2*np.pi*150*t) * np.exp(-t*14)
    s[:int(SR*0.02)] += np.random.randn(int(SR*0.02))*0.4*np.exp(-t[:int(SR*0.02)]*200)
    save("thud.wav", s)

def ding(freq=880, dur=0.6, name="ding.wav"):
    t = np.arange(int(SR*dur)) / SR
    s = np.sin(2*np.pi*freq*t)*np.exp(-t*6) + 0.4*np.sin(2*np.pi*freq*2*t)*np.exp(-t*9)
    save(name, s)

def coin():
    t = np.arange(int(SR*0.7)) / SR
    s = np.sin(2*np.pi*880*t)*np.exp(-np.maximum(0,t-0.0)*8)*(t<0.25)
    s += np.sin(2*np.pi*1320*t)*np.exp(-np.maximum(0,t-0.25)*8)*(t>=0.25)
    save("coin.wav", s)

def typing():
    n = int(SR*2.2); s = np.zeros(n)
    rng = np.random.default_rng(7)
    times = np.sort(rng.uniform(0.05, 2.05, 11))
    for tt in times:
        i = int(tt*SR); L = int(SR*0.03)
        click = np.random.randn(L) * np.exp(-np.arange(L)/(SR*0.006))
        click *= 0.5 + rng.random()*0.5
        s[i:i+L] += click[:max(0, min(L, n-i))]
    # lowpass kasar via moving average
    k = np.ones(8)/8
    s = np.convolve(s, k, mode="same")
    save("typing.wav", s)

def paper():
    n = int(SR*0.5); s = np.random.randn(n)
    k = np.ones(24)/24
    s = np.convolve(s, k, mode="same")
    env = np.minimum(1, np.arange(n)/(SR*0.05)) * np.exp(-np.arange(n)/(SR*0.35))
    save("paper.wav", s*env)

def whoosh():
    n = int(SR*0.8); s = np.random.randn(n)
    k = np.ones(60)/60
    s = np.convolve(s, k, mode="same")
    t = np.arange(n)/n
    env = np.sin(np.pi*t)**1.5
    save("whoosh.wav", s*env)

thud(); ding(); ding(1174, 0.5, "ding2.wav"); coin(); typing(); paper(); whoosh()
print("SEMUA SFX OK")
