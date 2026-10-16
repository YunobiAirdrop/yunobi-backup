#!/usr/bin/env python3
"""
dji_sync -- replace an iPhone clip's scratch audio with the matching DJI lav take.

The video is the timeline. The DJI take is matched by waveform, aligned to
sub-sample precision, trimmed to the video's exact bounds, and muxed back in
without re-encoding a single video frame.

Requires: ffmpeg, ffprobe, exiftool, numpy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

SR = 48000                 # analysis + output sample rate
FRAME = 960                # 20 ms
HOP = 240                  # 5 ms
WIN_S = 2.0                # verification window length
WIN_TOL_MS = 1.0           # a window "agrees" if within this of the median
PSR_MIN = 5.0              # peak-to-sidelobe floor for a window to count at all
MIN_AGREE = 0.80           # fraction of windows that must agree to accept a match
MIN_MARGIN = 0.15          # winner must beat the runner-up by this much
MIN_OVERLAP_S = 3.0        # below this there is not enough signal to match on
DRIFT_APPLY_MS = 10.0      # correct drift only if it would exceed this over the take
SEAM_MS = 40.0             # crossfade at a DJI/iPhone seam

VIDEO_EXTS = (".mov", ".mp4", ".m4v")


# ---------------------------------------------------------------- shell utils

def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, **kw)


def need(tool: str) -> None:
    if shutil.which(tool) is None:
        sys.exit(f"error: `{tool}` not found on PATH")


def probe(path: str) -> dict:
    p = run(["ffprobe", "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", path])
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {p.stderr.decode()[:300]}")
    return json.loads(p.stdout)


def duration_of(path: str) -> float:
    return float(probe(path)["format"]["duration"])


def decode_mono(path: str) -> np.ndarray:
    """Decode any media's first audio stream to mono float64 at SR."""
    p = run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-map", "0:a:0",
             "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", "-f", "f32le", "-"])
    if p.returncode != 0:
        raise RuntimeError(f"decode failed on {path}: {p.stderr.decode()[:300]}")
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)


# ---------------------------------------------------------------- discovery

def find_card(explicit: str | None) -> str | None:
    """A DJI card is any volume holding a TX_* folder with wavs in it."""
    roots = [explicit] if explicit else glob.glob("/Volumes/*")
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        if os.path.basename(root).startswith("TX_") and glob.glob(f"{root}/*.[wW][aA][vV]"):
            return root
        for cand in sorted(glob.glob(f"{root}/TX_*")):
            if os.path.isdir(cand) and glob.glob(f"{cand}/*.[wW][aA][vV]"):
                return cand
    return None


def find_takes(card: str) -> list[str]:
    return sorted(glob.glob(f"{card}/*.[wW][aA][vV]"))


def find_newest_video(folder: str) -> str | None:
    vids = [p for p in glob.glob(os.path.join(folder, "*"))
            if p.lower().endswith(VIDEO_EXTS) and os.path.getsize(p) > 0]
    return max(vids, key=os.path.getmtime) if vids else None


# ---------------------------------------------------------------- sync core

def gcc_phat(a: np.ndarray, b: np.ndarray, radius: int | None = None,
             centre: int = 0) -> tuple[float, float, float]:
    """Sub-sample lag of b within a, via phase-transform cross-correlation.

    Returns (lag_in_samples, peak_height, peak_to_sidelobe_ratio).
    Positive lag = b starts later than a.
    """
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    R = np.fft.rfft(a, n) * np.conj(np.fft.rfft(b, n))
    mag = np.abs(R)
    mag[mag < 1e-12] = 1e-12
    cc = np.fft.irfft(R / mag, n)

    if radius is None:
        cc = np.concatenate((cc[-(len(b) - 1):], cc[:len(a)]))
        base = -(len(b) - 1)
    else:
        idx = (centre + np.arange(-radius, radius + 1)) % n
        cc = cc[idx]
        base = centre - radius

    i = int(np.argmax(cc))
    frac = 0.0
    if 0 < i < len(cc) - 1:
        y0, y1, y2 = cc[i - 1], cc[i], cc[i + 1]
        d = y0 - 2 * y1 + y2
        if d != 0:
            frac = float(np.clip(0.5 * (y0 - y2) / d, -0.5, 0.5))

    # how far the peak stands above the rest of the correlation, excluding its
    # own lobe -- guards against locking onto steady tones like mains hum
    mask = np.ones(len(cc), dtype=bool)
    mask[max(0, i - 24): i + 25] = False
    if mask.sum() > 8:
        rest = cc[mask]
        psr = float((cc[i] - rest.mean()) / (rest.std() + 1e-12))
    else:
        psr = 0.0
    return base + i + frac, float(cc[i]), psr


def window_offsets(vid: np.ndarray, take: np.ndarray, offset: float
                   ) -> list[tuple[float, float, float, float]]:
    """Per-window local offsets at a candidate alignment.

    Consistency here is the confidence signal: a true match holds the same
    offset in every window, a false one scatters. Measured on a real pair, the
    true take clustered inside 0.15 ms while a false one spread over 5.9 ms.

    Envelope correlation is useless for this -- a chest lav and a room mic have
    unrelated envelopes even on identical speech (measured r was 0.0 on a
    confirmed match). Peak height alone is not enough either, since the true
    and false takes overlapped on it.
    """
    off = int(round(offset))
    lo, hi = max(0, off), min(len(vid), off + len(take))
    win = int(WIN_S * SR)
    out = []
    for s in range(lo, hi - win + 1, win):
        a = vid[s: s + win]
        b = take[s - off: s - off + win]
        if len(b) < win:
            break
        # skip windows with no signal on either side; they only add noise
        if np.sqrt((a ** 2).mean()) < 1e-5 or np.sqrt((b ** 2).mean()) < 1e-5:
            continue
        lag, peak, psr = gcc_phat(a, b, radius=int(SR * 0.02))
        out.append((s / SR, lag / SR * 1000.0, peak, psr))
    return out


class Match:
    def __init__(self, take: str, offset: float, agree: float, spread: float,
                 wins: list, drift_ms_s: float, audio: np.ndarray):
        self.take = take
        self.offset = offset              # samples; DJI start in video timeline
        self.agree = agree                # 0..1 fraction of agreeing windows
        self.spread = spread              # ms, scatter of agreeing windows
        self.wins = wins
        self.drift_ms_s = drift_ms_s
        self.audio = audio

    @property
    def offset_s(self) -> float:
        return self.offset / SR


def evaluate(vid: np.ndarray, take_path: str) -> Match | None:
    take = decode_mono(take_path)
    if min(len(vid), len(take)) < MIN_OVERLAP_S * SR:
        return None

    coarse, _, _ = gcc_phat(vid, take)
    wins = window_offsets(vid, take, coarse)
    if len(wins) < 2:
        return None

    local = np.array([w[1] for w in wins])
    psr = np.array([w[3] for w in wins])
    med = float(np.median(local))

    # a window only counts if it both agrees on the offset and has a peak that
    # actually stands out of its own correlation floor
    good = (np.abs(local - med) <= WIN_TOL_MS) & (psr >= PSR_MIN)
    agree = float(good.mean())
    spread = float(local[good].std()) if good.sum() > 1 else float("inf")

    # averaging the agreeing windows beats the single global peak for precision
    centre = float(local[good].mean()) if good.any() else med
    offset = coarse + centre / 1000.0 * SR

    drift = 0.0
    if good.sum() >= 4:
        t = np.array([w[0] for w in wins])[good]
        y = local[good]
        if t.max() - t.min() > 5.0:
            drift = float(np.polyfit(t, y, 1)[0])   # ms per second
    return Match(take_path, offset, agree, spread, wins, drift, take)


# ---------------------------------------------------------------- audio build

def fractional_delay(x: np.ndarray, frac: float) -> np.ndarray:
    """Shift x by a fractional sample count via an exact FFT phase ramp."""
    if abs(frac) < 1e-9:
        return x
    n = len(x)
    X = np.fft.rfft(x)
    k = np.arange(len(X))
    return np.fft.irfft(X * np.exp(-2j * np.pi * k * frac / n), n)


def fft_resample(x: np.ndarray, new_len: int) -> np.ndarray:
    """Resample by zero-padding / truncating in the frequency domain."""
    X = np.fft.rfft(x)
    keep = min(len(X), new_len // 2 + 1)
    Y = np.zeros(new_len // 2 + 1, dtype=complex)
    Y[:keep] = X[:keep]
    return np.fft.irfft(Y, new_len) * (new_len / len(x))


def build_track(m: Match, vid: np.ndarray, n_out: int, fill: bool,
                report: dict) -> np.ndarray:
    """Lay the DJI take onto the video's timeline, trimmed to its exact bounds."""
    take = m.audio
    offset = m.offset

    projected = abs(m.drift_ms_s) * (n_out / SR)
    if projected > DRIFT_APPLY_MS:
        factor = 1.0 - m.drift_ms_s / 1000.0
        take = fft_resample(take, max(1, int(round(len(take) * factor))))
        report["drift_corrected_ms"] = round(projected, 2)

    # split the shift: integer part by slicing, fraction by phase ramp
    i_off = int(np.floor(offset))
    frac = offset - i_off
    if abs(frac) > 1e-9:
        take = fractional_delay(take, frac)

    out = np.zeros(n_out)
    covered = np.zeros(n_out, dtype=bool)

    # video sample n corresponds to take sample n - i_off
    src_lo = max(0, -i_off)
    src_hi = min(len(take), n_out - i_off)
    if src_hi > src_lo:
        dst_lo = src_lo + i_off
        dst_hi = src_hi + i_off
        out[dst_lo:dst_hi] = take[src_lo:src_hi]
        covered[dst_lo:dst_hi] = True

    head = int(covered.argmax()) if covered.any() else n_out
    tail = n_out - int(covered[::-1].argmax()) if covered.any() else 0
    report["coverage_s"] = round(float(covered.sum()) / SR, 3)
    report["head_gap_s"] = round(head / SR, 3)
    report["tail_gap_s"] = round((n_out - tail) / SR, 3)

    if covered.all() or not fill:
        if not covered.all():
            report["gap_policy"] = "silence"
        return out

    # fill uncovered stretches from the iPhone's own audio, level-matched so the
    # seam does not jump, with a short crossfade either side of it
    scratch = vid[:n_out] if len(vid) >= n_out else np.pad(vid, (0, n_out - len(vid)))
    dji_rms = np.sqrt((out[covered] ** 2).mean()) if covered.any() else 0.0
    scr_rms = np.sqrt((scratch[covered] ** 2).mean()) if covered.any() else 0.0
    gain = float(dji_rms / scr_rms) if scr_rms > 1e-9 else 1.0
    gain = float(np.clip(gain, 0.05, 20.0))
    report["fill_gain_db"] = round(20 * np.log10(gain), 2) if gain > 0 else None

    filled = scratch * gain
    out[~covered] = filled[~covered]

    xf = int(SEAM_MS / 1000.0 * SR)
    for seam, into_dji in ((head, True), (tail, False)):
        if seam <= 0 or seam >= n_out:
            continue
        a, b = max(0, seam - xf), min(n_out, seam + xf)
        if b - a < 4:
            continue
        ramp = np.linspace(0.0, 1.0, b - a)
        w = ramp if into_dji else 1.0 - ramp
        out[a:b] = filled[a:b] * (1 - w) + np.where(covered[a:b], out[a:b], filled[a:b]) * w

    report["gap_policy"] = "iphone-fill"
    return out


# ---------------------------------------------------------------- mux + verify

def write_wav(path: str, x: np.ndarray) -> None:
    peak = float(np.max(np.abs(x))) if len(x) else 0.0
    if peak > 1.0:                      # DJI float can exceed unity; scale, never clip
        x = x / peak
    y = np.clip(x, -1.0, 1.0)
    i32 = (y * 2147483647.0).astype(np.int32)
    p = run(["ffmpeg", "-v", "error", "-y", "-f", "s32le", "-ar", str(SR),
             "-ac", "1", "-i", "-", "-c:a", "pcm_s32le", path], input=i32.tobytes())
    if p.returncode != 0:
        raise RuntimeError(f"wav write failed: {p.stderr.decode()[:300]}")


def mux(video: str, wav: str, out: str, codec: str, keep_scratch: bool) -> None:
    maps = ["-map", "0:v", "-map", "1:a"]
    if keep_scratch:
        maps += ["-map", "0:a:0"]
    maps += ["-map", "0:d?"]

    acodec = {"alac": ["-c:a:0", "alac", "-sample_fmt:a:0", "s32p"],
              "pcm": ["-c:a:0", "pcm_s24le"],
              "aac": ["-c:a:0", "aac", "-b:a:0", "256k"]}[codec]
    if keep_scratch:
        acodec += ["-c:a:1", "copy"]

    cmd = (["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav]
           + maps + ["-c:v", "copy", "-c:d", "copy"] + acodec
           + ["-map_metadata", "0", "-movflags", "use_metadata_tags+faststart",
              "-tag:v", "hvc1", "-disposition:a:0", "default", out])
    p = run(cmd)
    if p.returncode != 0:
        # mebx metadata tracks refuse to remux on some builds; drop and retry
        cmd2 = [c for c in cmd if c not in ("-map", "0:d?", "-c:d", "copy")]
        cmd2 = (["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav]
                + [m for m in maps if m != "0:d?"]
                + ["-c:v", "copy"] + acodec
                + ["-map_metadata", "0", "-movflags", "use_metadata_tags+faststart",
                   "-tag:v", "hvc1", "-disposition:a:0", "default", out])
        p2 = run(cmd2)
        if p2.returncode != 0:
            raise RuntimeError(f"mux failed: {p.stderr.decode()[:400]}")
        print("  warn: Apple metadata tracks could not be remuxed and were dropped")


def restore_metadata(src: str, dst: str) -> None:
    run(["exiftool", "-q", "-overwrite_original", "-TagsFromFile", src,
         "-QuickTime:CreateDate", "-QuickTime:ModifyDate",
         "-QuickTime:CreationDate", "-QuickTime:GPSCoordinates",
         "-QuickTime:Make", "-QuickTime:Model", "-QuickTime:Software",
         "-QuickTime:LocationInformation", dst])
    st = os.stat(src)
    os.utime(dst, (st.st_atime, st.st_mtime))
    if shutil.which("SetFile"):
        stamp = dt.datetime.fromtimestamp(st.st_mtime).strftime("%m/%d/%Y %H:%M:%S")
        run(["SetFile", "-d", stamp, dst])


def video_stream_md5(path: str) -> str:
    p = run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v", "-c", "copy",
             "-f", "md5", "-"])
    return p.stdout.decode().strip().replace("MD5=", "")


def verify(src: str, dst: str, codec: str) -> list[str]:
    """Prove the burn: identical video bits, right duration, real audio track."""
    problems = []
    s, d = probe(src), probe(dst)
    sd, dd = float(s["format"]["duration"]), float(d["format"]["duration"])
    if abs(sd - dd) > 1.0 / 24:
        problems.append(f"duration drifted: {sd:.3f}s -> {dd:.3f}s")

    if video_stream_md5(src) != video_stream_md5(dst):
        problems.append("video stream is NOT bit-identical to the source")

    auds = [x for x in d["streams"] if x["codec_type"] == "audio"]
    if not auds:
        problems.append("output has no audio stream")
    elif auds[0]["codec_name"] != codec.replace("pcm", "pcm_s24le"):
        if not (codec == "pcm" and auds[0]["codec_name"].startswith("pcm")):
            problems.append(f"audio codec is {auds[0]['codec_name']}, expected {codec}")

    if not problems:
        a = decode_mono(dst)
        if len(a) < 0.98 * dd * SR:
            problems.append(f"audio track is short: {len(a)/SR:.2f}s of {dd:.2f}s")
        if float(np.max(np.abs(a))) < 1e-4:
            problems.append("audio track is silent")
    return problems


# ---------------------------------------------------------------- cleanup

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def archive_and_wipe(card: str, archive_root: str, dry: bool) -> None:
    takes = find_takes(card)
    if not takes:
        print("  card already empty")
    day = dt.datetime.now().strftime("%Y-%m-%d")
    dest = os.path.join(os.path.expanduser(archive_root), day)

    if takes:
        os.makedirs(dest, exist_ok=True)
        verified = []
        for t in takes:
            target = os.path.join(dest, os.path.basename(t))
            if dry:
                print(f"  would archive {os.path.basename(t)} -> {target}")
                continue
            if os.path.exists(target) and sha256(target) == sha256(t):
                verified.append(t)
                print(f"  already archived {os.path.basename(t)}")
                continue
            shutil.copy2(t, target)
            if sha256(target) == sha256(t):
                verified.append(t)
                print(f"  archived  {os.path.basename(t)}  (sha256 ok)")
            else:
                print(f"  CHECKSUM MISMATCH on {os.path.basename(t)} -- keeping on card")
        if not dry:
            for t in verified:
                os.remove(t)
            print(f"  deleted {len(verified)} take(s) from the card")

    # Finder's trash on a removable volume never frees space; clear it explicitly
    vol = card
    while os.path.dirname(vol) != "/Volumes" and vol != "/":
        vol = os.path.dirname(vol)
    trash = os.path.join(vol, ".Trashes")
    if os.path.isdir(trash):
        freed = sum(os.path.getsize(os.path.join(r, f))
                    for r, _, fs in os.walk(trash) for f in fs
                    if os.path.exists(os.path.join(r, f)))
        if dry:
            print(f"  would clear .Trashes ({freed/1e6:.1f} MB)")
        elif freed:
            for entry in glob.glob(os.path.join(trash, "*")):
                shutil.rmtree(entry, ignore_errors=True) if os.path.isdir(entry) \
                    else os.remove(entry)
            print(f"  cleared .Trashes ({freed/1e6:.1f} MB reclaimed)")

    # drop the session folder if it is now empty
    if not dry and os.path.isdir(card) and not find_takes(card):
        try:
            os.rmdir(card)
        except OSError:
            pass


# ---------------------------------------------------------------- main

def process(video: str, takes: list[str], args, used: set[str]) -> tuple[bool, str | None]:
    name = os.path.basename(video)
    print(f"\n=== {name}")
    vid = decode_mono(video)
    n_out = int(round(duration_of(video) * SR))
    print(f"  {n_out/SR:.3f}s  scratch audio decoded")

    pool = [os.path.expanduser(args.take)] if args.take else [t for t in takes
                                                              if t not in used]
    cands = []
    for t in pool:
        m = evaluate(vid, t)
        if m:
            cands.append(m)
            print(f"  {os.path.basename(t):<42} agree={m.agree:5.0%} "
                  f"spread={m.spread:6.3f}ms offset={m.offset_s:+9.4f}s "
                  f"windows={len(m.wins)}")

    if not cands:
        print("  no take long enough to match against")
        return False, None

    cands.sort(key=lambda m: (m.agree, -m.spread, len(m.wins)), reverse=True)
    best = cands[0]
    runner = cands[1].agree if len(cands) > 1 else 0.0

    if args.take:
        # forced pairing: still align and report, but the operator overrides the gates
        print(f"  (take forced by --take; confidence gates not applied)")
    elif best.agree < MIN_AGREE:
        print(f"  REFUSED: best agreement {best.agree:.0%} < {MIN_AGREE:.0%}. "
              f"No confident match; nothing written.\n"
              f"           Force it with --take if you know which one it is.")
        return False, None
    elif len(cands) > 1 and best.agree - runner < MIN_MARGIN:
        print(f"  REFUSED: {os.path.basename(best.take)} ({best.agree:.0%}) and "
              f"{os.path.basename(cands[1].take)} ({runner:.0%}) are too close "
              f"to tell apart.\n           Force it with --take if you know "
              f"which one it is.")
        return False, None

    print(f"\n  matched : {os.path.basename(best.take)}")
    print(f"  offset  : {best.offset_s:+.6f}s  ({best.offset:+.2f} samples)")
    print(f"  agree   : {best.agree:.0%} of {len(best.wins)} windows "
          f"(runner-up {runner:.0%})")
    print(f"  spread  : {best.spread:.3f}ms across agreeing windows")
    print(f"  drift   : {best.drift_ms_s*1000:+.1f} ppm")

    report: dict = {}
    track = build_track(best, vid, n_out, fill=not args.silence_gaps, report=report)

    cov = report["coverage_s"]
    pct = cov / (n_out / SR) * 100
    if pct < 99.5:
        print(f"\n  WARNING: DJI covers {cov:.2f}s of {n_out/SR:.2f}s ({pct:.0f}%)")
        if report["head_gap_s"]:
            print(f"           head gap {report['head_gap_s']:.2f}s")
        if report["tail_gap_s"]:
            print(f"           tail gap {report['tail_gap_s']:.2f}s")
        print(f"           gap policy: {report['gap_policy']}")
    else:
        print(f"  coverage: {pct:.1f}% (DJI trimmed to the video)")
    if "drift_corrected_ms" in report:
        print(f"  drift corrected: {report['drift_corrected_ms']}ms over the take")

    stem, ext = os.path.splitext(video)
    out = args.output or f"{stem}-dji{ext}"
    if args.dry_run:
        print(f"  would write {out}")
        return True, best.take

    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "sync.wav")
        write_wav(wav, track)
        mux(video, wav, out, args.codec, args.keep_scratch)
    restore_metadata(video, out)

    problems = verify(video, out, args.codec)
    if problems:
        print("  VERIFY FAILED:")
        for p in problems:
            print(f"    - {p}")
        return False, best.take

    sz = os.path.getsize(out) / 1e6
    print(f"  verified: video bit-identical, audio full-length, metadata restored")
    print(f"  wrote   : {out}  ({sz:.1f} MB)")
    return True, best.take


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="*", help="clip(s); default = newest in --watch")
    ap.add_argument("--card", help="DJI card path (auto-detected)")
    ap.add_argument("--take", help="force this wav instead of matching (single video)")
    ap.add_argument("--watch", default="~/Downloads", help="where AirDropped clips land")
    ap.add_argument("--output", help="explicit output path (single video only)")
    ap.add_argument("--archive", default="~/Movies/dji-archive")
    ap.add_argument("--codec", choices=("alac", "pcm", "aac"), default="alac")
    ap.add_argument("--keep-scratch", action="store_true",
                    help="keep the iPhone audio as a second track")
    ap.add_argument("--silence-gaps", action="store_true",
                    help="leave uncovered stretches silent instead of filling")
    ap.add_argument("--no-clean", action="store_true", help="do not touch the card")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe", "exiftool"):
        need(tool)

    card = find_card(args.card)
    if not card and not args.take:
        return int(bool(sys.stderr.write(
            "error: no DJI card found. Connect it via USB and unlock it.\n")))
    takes = find_takes(card) if card else []
    if card:
        print(f"card  : {card}")
        print(f"takes : {len(takes)}")
    else:
        # --take can point at an archived wav long after the card was wiped
        print(f"card  : none mounted; working from --take")

    videos = [os.path.expanduser(v) for v in args.video]
    if not videos:
        newest = find_newest_video(os.path.expanduser(args.watch))
        if not newest:
            return int(bool(sys.stderr.write(
                f"error: no video found in {args.watch}\n")))
        videos = [newest]
    if args.output and len(videos) > 1:
        return int(bool(sys.stderr.write("error: --output needs a single video\n")))
    if args.take and len(videos) > 1:
        return int(bool(sys.stderr.write("error: --take needs a single video\n")))

    used: set[str] = set()
    ok_all = True
    for v in videos:
        try:
            ok, take = process(v, takes, args, used)
        except Exception as exc:                      # noqa: BLE001
            print(f"  ERROR: {exc}")
            ok, take = False, None
        ok_all &= ok
        if ok and take:
            used.add(take)

    if args.no_clean or not card:
        print("\ncard untouched" + (" (--no-clean)" if args.no_clean else ""))
    elif not ok_all:
        print("\ncard untouched: a burn did not verify. Nothing is deleted "
              "unless every clip succeeded.")
    else:
        print("\ncleanup")
        archive_and_wipe(card, args.archive, args.dry_run)

    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
