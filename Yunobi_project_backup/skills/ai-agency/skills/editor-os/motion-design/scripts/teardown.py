#!/usr/bin/env python3
"""Measure a motion film instead of arguing about it.

Reverse-engineers the numbers that decide whether a product film works: how many cuts it has,
what the music's bar is, how long each typographic card stays on screen, and what the palette
actually is. Every figure in references/product-film.md came out of this script.

Run it on a reference before copying its look, and on your own render before calling it done.

    python3 teardown.py all      <file.mp4>       # everything below, in one pass
    python3 teardown.py cuts     <file.mp4>       # hard-cut count; a product film wants 0
    python3 teardown.py tempo    <file.mp4|.wav>  # BPM, beat, bar -- the unit beats.ts is built in
    python3 teardown.py cards    <file.mp4>       # every centred-text card: length, gap, cycle
    python3 teardown.py palette  <file.mp4>       # ground, ink and the saturated windows
    python3 teardown.py sheet    <file.mp4>       # 1fps contact sheets, to read the beat map by eye
    python3 teardown.py camera   <file.mp4> --ss 174 --t 12   # camera velocity, settle tau, residual
    python3 teardown.py ground   <file.mp4> --ss 181          # vignette profile and accent clusters

Needs ffmpeg, ffprobe and numpy. Nothing else.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

# The centred-text band, as a fraction of the frame. A claim line sits on the middle third and
# nothing else in a product film does, so cropping to it separates type from product UI.
BAND_TOP, BAND_HEIGHT = 0.45, 0.10
BAND_LEFT, BAND_WIDTH = 0.15, 0.70


def run(args: list[str]) -> bytes:
    p = subprocess.run(args, capture_output=True)
    if p.returncode != 0 and not p.stdout:
        sys.exit(f"ffmpeg failed: {p.stderr.decode()[-600:]}")
    return p.stdout


def probe(path: str) -> tuple[float, int, int, float]:
    """duration, width, height, fps"""
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,r_frame_rate", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1", path]).decode()
    d = dict(line.split("=", 1) for line in out.strip().splitlines() if "=" in line)
    num, den = d["r_frame_rate"].split("/")
    return float(d["duration"]), int(d["width"]), int(d["height"]), float(num) / float(den)


def raw_gray(path: str, vf: str, w: int, h: int,
             ss: float | None = None, t: float | None = None) -> np.ndarray:
    """Decode a filtered stream straight to a (frames, h, w) uint8 array.

    `ss`/`t` trim before decoding, so a camera measurement over one 12-second sequence does not
    have to pull an eight-minute film through memory.
    """
    trim = ([] if ss is None else ["-ss", str(ss)]) + ([] if t is None else ["-t", str(t)])
    buf = run(["ffmpeg", "-v", "error", *trim, "-i", path, "-vf", vf,
               "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    n = w * h
    frames = len(buf) // n
    return np.frombuffer(buf, dtype=np.uint8)[: frames * n].reshape(frames, h, w)


# --------------------------------------------------------------------------- cuts

def cmd_cuts(path: str, threshold: float = 0.06) -> int:
    """Hard cuts. A product film should return zero: every change is a move, never a cut.

    TWO THINGS HERE ARE LOAD-BEARING AND BOTH LOOK LIKE NOISE. `-fps_mode` rather than `-vsync`,
    because ffmpeg 9 removed `-vsync` and the whole command then exits before it decodes a frame;
    and `-v info` rather than the `-v error` every other call in this file uses, because `showinfo`
    logs at info and its lines are the only output this function reads.

    Either one wrong and ffmpeg prints nothing this regex matches, which lands in the `else` branch
    below and reports **"Continuous. Every transition is a camera move."** - a confident false
    negative on a film with visible cuts in it. Found on 28 Aug 2026 measuring a reference with five
    of them. A measurement script that cannot fail loudly is worse than no script, so the return
    code is checked now rather than trusted.
    """
    proc = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-vf",
                           f"select='gt(scene,{threshold})',showinfo", "-fps_mode", "vfr",
                           "-f", "null", "-"], capture_output=True)
    err = proc.stderr.decode()
    if proc.returncode != 0:
        sys.exit(f"ffmpeg failed, so the cut count would be a lie:\n{err[-600:]}")
    times = [float(m) for m in re.findall(r"pts_time:([\d.]+)", err)]
    # The first decoded frame always passes the scene filter. It is not a cut.
    times = times[1:]
    print(f"cuts above scene={threshold}: {len(times)}")
    if times:
        print("  at:", " ".join(f"{t:.2f}" for t in times[:40]))
        print("\n  A product film wants 0. Anything above that is a slideshow with good scenes.")
    else:
        print("  Continuous. Every transition is a camera move.")
    return len(times)


# --------------------------------------------------------------------------- tempo

def cmd_tempo(path: str, lo: float = 60.0, hi: float = 190.0) -> float:
    """BPM by spectral-flux comb, then the bar -- the number beats.ts is built in multiples of."""
    wav = Path(path).with_suffix(".teardown.wav")
    run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1",
         "-acodec", "pcm_s16le", "-ar", "44100", str(wav), "-y"])
    import wave
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    wav.unlink(missing_ok=True)

    hop, win = 256, 1024
    hann = np.hanning(win)
    n = (len(d) - win) // hop
    spec = np.empty((n, win // 2 + 1), dtype=np.float32)
    for i in range(n):
        spec[i] = np.abs(np.fft.rfft(d[i * hop: i * hop + win] * hann))
    flux = np.maximum(0, np.diff(spec, axis=0)).sum(1)
    flux = (flux - flux.mean()) / (flux.std() or 1)
    fps = sr / hop

    # Score on the middle of the track: intros and outros are often free-time and skew the comb.
    a, b = int(len(flux) * 0.25), int(len(flux) * 0.75)
    seg = flux[a:b] - flux[a:b].mean()

    # Normalised autocorrelation. WHY not a plain comb: a comb scored by mean() samples fewer
    # points at slow tempos, so its average rises as the tempo falls and it lands on 80 BPM for a
    # 133 BPM track. Autocorrelation normalised by overlap has no such bias, and the harmonic
    # term plus the log-normal prior around 120 BPM settle the octave the way ear does.
    ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
    ac /= np.maximum(np.arange(len(ac), 0, -1), 1)
    ac /= (ac[0] or 1)

    def at(lag: int) -> float:
        return float(ac[lag]) if 0 < lag < len(ac) else 0.0

    best = (-1e9, 0.0)
    for bpm in np.arange(lo, hi, 0.1):
        lag = 60.0 / bpm * fps
        prior = np.exp(-0.5 * (np.log2(bpm / 120.0) / 0.9) ** 2)
        score = prior * (at(round(lag)) + 0.5 * at(round(2 * lag)) + 0.25 * at(round(4 * lag)))
        if score > best[0]:
            best = (score, float(bpm))

    # Refine to 0.02 BPM with a fixed-sample comb, so every candidate is scored on equal terms.
    coarse = best[1]
    best = (-1e9, coarse)
    for bpm in np.arange(coarse - 3, coarse + 3, 0.02):
        per = 60.0 / bpm * fps
        count = int((len(seg) - 1) / per)
        if count < 8:
            continue
        for phase in np.arange(0, per, per / 12):
            idx = np.round(phase + np.arange(count) * per).astype(int)
            score = seg[idx[idx < len(seg)]].mean()
            if score > best[0]:
                best = (score, float(bpm))

    bpm = best[1]
    beat = 60 / bpm
    print(f"BPM {bpm:.2f}")
    print(f"  beat        {beat:.4f}s")
    print(f"  bar (4/4)   {beat * 4:.4f}s   <- one typographic card")
    print(f"  2 bars      {beat * 8:.4f}s   <- a line that carries the argument")
    print(f"  8-bar phrase{beat * 32:.3f}s  <- an act")
    for fps_out in (30, 60):
        print(f"  at {fps_out}fps: bar = {beat * 4 * fps_out:.1f} frames")
    return bpm


# --------------------------------------------------------------------------- cards

def cmd_cards(path: str) -> None:
    """Every centred-text card, with its length, the empty gap after it, and the cycle.

    The cycle column is the one that matters: in a film cut to music it is flat and equal to
    the bar. Cards timed by eye scatter, and the scatter is what makes a film feel amateur.
    """
    dur, W, H, fps = probe(path)
    cw, chh = int(W * BAND_WIDTH), int(H * BAND_HEIGHT)
    sw, sh = 240, 20
    vf = (f"crop={cw}:{chh}:{int(W * BAND_LEFT)}:{int(H * BAND_TOP)},"
          f"scale={sw}:{sh},format=gray")
    d = raw_gray(path, vf, sw, sh)
    ink = (d < 150).sum(axis=(1, 2))
    present = ink > 25

    segs, start = [], None
    for i, on in enumerate(present):
        if on and start is None:
            start = i
        if not on and start is not None:
            if i - start > 12:  # under 0.2s is a flicker, not a card
                segs.append((start / fps, (i - 1) / fps, int(ink[start:i].max())))
            start = None
    if start is not None:
        segs.append((start / fps, (len(present) - 1) / fps, int(ink[start:].max())))

    print(f"{len(segs)} text cards in {dur:.1f}s\n")
    print(f"{'start':>7} {'end':>7} {'len':>6} {'gap':>6} {'cycle':>6}   ink")
    cycles, prev = [], None
    for s, e, peak in segs:
        gap = "" if prev is None else f"{s - prev[1]:6.2f}"
        cyc = ""
        if prev is not None:
            cycles.append(s - prev[0])
            cyc = f"{s - prev[0]:6.2f}"
        print(f"{s:7.2f} {e:7.2f} {e - s:6.2f} {gap:>6} {cyc:>6}   {peak}")
        prev = (s, e)
    if cycles:
        c = np.array(cycles)
        tight = c[c < np.median(c) * 1.6]  # drop the long product stretches between claims
        print(f"\nmedian cycle {np.median(tight):.2f}s   spread {tight.std():.2f}s")
        print("  Flat and near the bar means it is cut to the track. Scattered means cut by eye.")


# --------------------------------------------------------------------------- palette

def cmd_palette(path: str) -> None:
    """Ground, ink, and where the film lets itself be saturated."""
    dur, W, H, fps = probe(path)
    sw, sh = 160, 90
    buf = run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps=10,scale={sw}:{sh}",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    n = sw * sh * 3
    f = len(buf) // n
    a = np.frombuffer(buf, dtype=np.uint8)[: f * n].reshape(f, sh * sw, 3).astype(int)

    flat = a.reshape(-1, 3)
    hexof = lambda v: "#%02x%02x%02x" % tuple(int(x) for x in v)

    # The ground is the film's MOST COMMON colour, not its brightest.
    #
    # This used to read `flat[flat.sum(1) > 690]` and call that the ground, which is only true of a
    # film with a light ground - the daylight and paper-board registers this script was first
    # written against. Point it at the live-screen register, whose whole frame is a dark screen,
    # and the bright group is empty: numpy warns "Mean of empty slice", `hexof` is handed nan and
    # the command dies with a traceback. Found 28 Aug 2026. A mode works on either register and
    # needs no threshold at all.
    bins = (flat // 16).astype(np.int64)
    key = bins[:, 0] * 289 + bins[:, 1] * 17 + bins[:, 2]
    ground_key = np.bincount(key).argmax()
    ground = flat[key == ground_key]
    print(f"ground  {hexof(ground.mean(0))}   ({len(ground) * 100 // len(flat)}% of pixels)")

    # Ink is whatever sits furthest from the ground in luminance, in whichever direction the film
    # actually goes. On a light ground that is the dark type; on a dark one it is the light type.
    lum = flat @ np.array([0.2126, 0.7152, 0.0722])
    ground_lum = float(ground.mean(0) @ np.array([0.2126, 0.7152, 0.0722]))
    far = flat[np.abs(lum - ground_lum) > 90]
    if len(far):
        print(f"ink     {hexof(far.mean(0))}   ({len(far) * 100 // len(flat)}% of pixels)")
    else:
        print("ink     none: nothing in the film is 90 levels off the ground")

    sat = a.max(2) - a.min(2)
    strong = (sat > 25).mean(1) * 100
    segs, start = [], None
    for i in range(f):
        on = strong[i] > 45
        if on and start is None:
            start = i
        if not on and start is not None:
            if i - start > 5:
                segs.append((start / 10, (i - 1) / 10))
            start = None
    if start is not None:
        segs.append((start / 10, (f - 1) / 10))
    total = sum(b - s for s, b in segs)
    print(f"\nsaturated windows ({total:.1f}s of {dur:.1f}s, {total / dur * 100:.0f}%):")
    for s, b in segs:
        print(f"  {s:6.1f} -> {b:6.1f}   ({b - s:.1f}s)")
    print("\n  Few windows means the colour is punctuation. Many means it is wallpaper.")


# --------------------------------------------------------------------------- sheet

# ------------------------------------------------------------------------- camera

def _shift(a: np.ndarray, b: np.ndarray) -> tuple[int, int]:
    """Whole-pixel translation from b to a, by phase correlation.

    WHY phase correlation rather than block matching: it uses the whole frame, so a slow dolly
    over a near-empty pale ground -- where there is nothing a feature tracker would call a
    feature -- still resolves to the pixel. The Hann window kills the wrap-around edge response
    that otherwise pins every answer to (0, 0).
    """
    win = np.hanning(a.shape[0])[:, None] * np.hanning(a.shape[1])[None, :]
    fa = np.fft.fft2((a - a.mean()) * win)
    fb = np.fft.fft2((b - b.mean()) * win)
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    peak = np.fft.ifft2(r).real
    dy, dx = np.unravel_index(int(np.argmax(peak)), peak.shape)
    if dy > a.shape[0] // 2:
        dy -= a.shape[0]
    if dx > a.shape[1] // 2:
        dx -= a.shape[1]
    return int(dx), int(dy)


def cmd_camera(path: str, ss: float = 0.0, t: float = 12.0) -> None:
    """Per-frame camera velocity, the peak, the fitted settle constant and the residual drift.

    This is what settles whether a reference's motion is "smooth": it is a number, and the two
    that matter are the exponential time constant of the decay and whether the velocity ever
    reaches zero. In the long-take reference both are house constants -- tau near 0.45s, and a
    residual that never stops. See references/long-take.md.
    """
    _, _, _, fps = probe(path)
    # WHY 960 and not 480: the correlation resolves whole pixels, so a proxy that halves the frame
    # also halves the sensitivity. At 480 the reference film's residual drift quantises to zero and
    # the tool reports "comes to rest" on a shot that is visibly still moving.
    W, H = 960, 540
    g = raw_gray(path, f"scale={W}:{H},format=gray", W, H, ss=ss, t=t).astype(float)
    if len(g) < 4:
        sys.exit("not enough frames in that window")

    vx = [_shift(g[i], g[i - 1])[0] for i in range(1, len(g))]
    vy = [_shift(g[i], g[i - 1])[1] for i in range(1, len(g))]
    # Magnitude, not |dx|+|dy|: a diagonal drift is one move, and the taxicab sum overstates it
    # by up to 41%, which is enough to put a correct film over the "too fast" line.
    speed = [float(np.hypot(x, y)) for x, y in zip(vx, vy)]

    # A single-frame spike of tens of pixels is a hard cut, not a camera move. Drop it from the
    # fit or one cut poisons every figure below.
    cuts = [i for i, s_ in enumerate(speed) if s_ > W * 0.12]
    clean = [(i, s_) for i, s_ in enumerate(speed) if i not in cuts]
    peak_i, peak_v = max(clean, key=lambda p: p[1]) if clean else (0, 0)

    print(f"window {ss:.2f}s +{t:.2f}s at {fps:.2f}fps, {len(g)} frames, proxy {W}x{H}")
    print(f"hard cuts at frame(s): {cuts if cuts else 'none'}")
    print(f"peak speed  {peak_v:.1f}px/frame = {peak_v / W * 100:.2f}% of frame width per frame")

    # The residual floor first, because tau is meaningless without it. A long take decays from its
    # peak towards a floor it never reaches, so fitting the raw tail measures mostly the floor and
    # returns a tau several times too long: 2.9s on a film whose real settle is under half a second.
    late = [s_ for i, s_ in clean if i > peak_i + int(fps * 1.5)]
    floor = float(np.median(late)) if late else 0.0

    # Smoothed before the fit: whole-pixel correlation is quantised, so one noisy frame that dips
    # into the floor would end the tail three frames after the peak and report "never decays".
    sm = np.convolve(np.array(speed), np.ones(3) / 3, mode="same")
    tail = []
    for i, _ in clean:
        if i <= peak_i:
            continue
        excess = float(sm[i]) - floor
        if excess <= max(0.15 * (peak_v - floor), 0.5):
            break                      # decayed into the floor; everything after is drift
        tail.append(excess)
    if len(tail) > 6:
        k = np.polyfit(np.arange(len(tail)), np.log(np.array(tail)), 1)[0]
        tau = (-1.0 / k) / fps if k < 0 else float("inf")
        print(f"settle tau  {tau:.2f}s  (fit over {len(tail)} frames, peak down to the floor)")
    else:
        print("settle tau  -- the move never decays inside this window")

    if late:
        # Phase correlation sees translation only. A slow push, or elements building inside a
        # locked-off frame, both correlate to (0, 0) while the picture is plainly still changing,
        # so the verdict has to consult the raw frame difference before calling anything a slide.
        churn = float(np.mean(np.abs(np.diff(g[peak_i + int(fps * 1.5):], axis=0)))) if len(
            g) > peak_i + int(fps * 1.5) + 2 else 0.0
        verdict = ("never rests" if floor >= 0.5
                   else "not translating, but the frame is still changing (a push, or a build)"
                   if churn > 0.6
                   else "COMES TO REST -- reads as a slide")
        print(f"residual    {floor:.2f}px/frame = {floor / W * 100:.2f}% of frame width per frame"
              f"  ({verdict})")

    print("\nframe  speed  dx   dy")
    for i, (x, y) in enumerate(zip(vx, vy)):
        print(f"{i + 1:5d}  {speed[i]:5.1f}  {x:3d}  {y:3d}")


def cmd_ground(path: str, ss: float = 0.0) -> None:
    """The vignette profile and the accent clusters of one frame.

    A ground that samples flat is paper. A ground with a 70-level swing between its centre and its
    corners is a lit wall, which is what the long-take reference has and what makes its panels
    read as lit rather than as pasted on.
    """
    _, W, H, _ = probe(path)
    raw = run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", path, "-frames:v", "1",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    a = np.frombuffer(raw, dtype=np.uint8)[: W * H * 3].reshape(H, W, 3).astype(int)

    row, col = a[int(H * 0.04)], a[:, int(W * 0.016)]
    hprof = [int(row[x].mean()) for x in range(0, W, max(1, W // 8))]
    vprof = [int(col[y].mean()) for y in range(0, H, max(1, H // 8))]
    print("horizontal (top row, L->R): ", hprof)
    print("vertical   (left col, T->B):", vprof)

    # WHY the verdict reads the profile and not the frame's min/max: min/max spans the panels and
    # the type, so one white card and one black glyph score "lit wall" over a ground that is
    # perfectly flat. The question is what the *ground* does across the frame, which is the strip
    # sampled above, and the reference answers 111 to 187 across the width -- 76 levels.
    swing = max(hprof) - min(hprof)
    print(f"ground swing {swing} levels across the width"
          f"   ({'lit wall' if swing > 45 else 'FLAT -- reads as paper, not as a lit room'})"
          f"   [reference: 76]")

    sat = a.max(2) - a.min(2)
    ys, xs = np.where(sat > 55)
    if len(xs):
        from collections import Counter
        c = Counter(tuple((a[y, x] // 16 * 16)) for y, x in zip(ys, xs))
        print("accents:", ", ".join(f"#{r:02x}{g:02x}{b:02x}({n})" for (r, g, b), n in c.most_common(6)))
    else:
        print("accents: none above threshold -- the frame is neutral")


def cmd_sheet(path: str, out: str = "sheets") -> None:
    """1fps contact sheets. The fastest way to read a film's beat map by eye."""
    Path(out).mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-i", path, "-vf", "fps=1,scale=320:-1,tile=8x6",
         f"{out}/sheet_%02d.png", "-y"])
    made = sorted(Path(out).glob("sheet_*.png"))
    print(f"{len(made)} sheet(s) in {out}/ -- open them and write the beat map:")
    for m in made:
        print(f"  {m}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command",
                    choices=["all", "cuts", "tempo", "cards", "palette", "sheet",
                             "camera", "ground"])
    ap.add_argument("file")
    ap.add_argument("--ss", type=float, default=0.0, help="start of the window, seconds")
    ap.add_argument("--t", type=float, default=12.0, help="length of the window, seconds")
    args = ap.parse_args()

    if not Path(args.file).exists():
        sys.exit(f"no such file: {args.file}")

    if args.command == "all":
        for name, fn in (("CUTS", cmd_cuts), ("TEMPO", cmd_tempo),
                         ("CARDS", cmd_cards), ("PALETTE", cmd_palette)):
            print(f"\n=== {name} " + "=" * (60 - len(name)))
            fn(args.file)
    elif args.command == "camera":
        cmd_camera(args.file, ss=args.ss, t=args.t)
    elif args.command == "ground":
        cmd_ground(args.file, ss=args.ss)
    else:
        {"cuts": cmd_cuts, "tempo": cmd_tempo, "cards": cmd_cards,
         "palette": cmd_palette, "sheet": cmd_sheet}[args.command](args.file)


if __name__ == "__main__":
    main()
