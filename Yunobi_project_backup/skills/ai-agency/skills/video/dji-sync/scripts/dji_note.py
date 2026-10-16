#!/usr/bin/env python3
"""
dji_note -- turn a DJI lav take into a speech-only file and a transcript.

For solo takes with no video: a walk, a ramble, a thought dumped into the mic.
Silero VAD decides what is speech, everything else is cut, and only the cut file
is ever transcribed. That last part is not an optimisation: fed 20 minutes of
near-silence, whisper locks into a repeat loop and returns nothing real.

Requires: ffmpeg, ffprobe, whisper-cli, whisper-vad-speech-segments, numpy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys
import tempfile
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dji_sync import archive_and_wipe, duration_of, find_card, find_takes, need, run  # noqa: E402

SR = 16000                 # what both VAD and whisper want
PAD_S = 0.25               # keep this much either side of a speech segment
FADE_MS = 10.0             # de-click the joins
MIN_SPEECH_S = 1.0         # below this there is nothing worth transcribing

# WHY: whisper's silence failure mode is to repeat one sentence forever. A real
# ramble does not say the same thing six times, so a dominant repeat is the tell.
LOOP_MIN_REPEATS = 6
LOOP_MIN_SHARE = 0.40

VOICEINK = os.path.expanduser(
    "~/Library/Application Support/com.prakashjoshipax.VoiceInk/WhisperModels")
DEFAULT_MODEL = f"{VOICEINK}/ggml-large-v3-turbo-q5_0.bin"
DEFAULT_VAD = "/Applications/VoiceInk.app/Contents/Resources/ggml-silero-v5.1.2.bin"
DEFAULT_VAULT = "~/Studio/r-hub/vault"


def hms(seconds: float) -> str:
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}m{s:02d}s" if m else f"{s}s"


# ---------------------------------------------------------------- discovery

def pick_take(card: str, explicit: str | None) -> str:
    """Newest take on the card, preferring DJI's noise-cancelled `_edit` twin.

    The Mic 3 writes `_orig` and `_edit` at identical length but different
    content. `_edit` is the processed one and is what VAD and whisper do best on.
    """
    if explicit:
        return os.path.expanduser(explicit)
    takes = find_takes(card)
    if not takes:
        sys.exit("error: no takes on the card")
    edits = [t for t in takes if "_edit" in os.path.basename(t)]
    return max(edits or takes, key=os.path.getmtime)


# ---------------------------------------------------------------- speech

def decode_16k(path: str) -> np.ndarray:
    p = run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-map", "0:a:0",
             "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", "-f", "f32le", "-"])
    if p.returncode != 0:
        sys.exit(f"error: decode failed on {path}: {p.stderr.decode()[:300]}")
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float32)


def vad_segments(wav: str, vad_model: str, threshold: float,
                 min_silence_ms: int) -> list[tuple[float, float]]:
    """Silero speech segments, in seconds.

    No `-ug`: the GPU path aborts on the VAD graph. CPU does 20 minutes in ~2 s.
    """
    p = run(["whisper-vad-speech-segments", "-f", wav, "-vm", vad_model,
             "-vt", str(threshold), "-vsd", str(min_silence_ms), "-np"])
    out = (p.stdout + p.stderr).decode(errors="replace")
    segs = [(float(a) / 100.0, float(b) / 100.0)
            for a, b in re.findall(r"start = ([\d.]+), end = ([\d.]+)", out)]
    if not segs and p.returncode != 0:
        sys.exit(f"error: VAD failed: {out[-400:]}")
    return segs


def merge(segs: list[tuple[float, float]], pad: float,
          total: float) -> list[tuple[float, float]]:
    out: list[list[float]] = []
    for s, e in sorted(segs):
        s, e = max(0.0, s - pad), min(total, e + pad)
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def cut(audio: np.ndarray, segs: list[tuple[float, float]]) -> np.ndarray:
    fade = int(SR * FADE_MS / 1000.0)
    ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
    pieces = []
    for s, e in segs:
        chunk = audio[int(s * SR):int(e * SR)].copy()
        if len(chunk) > 2 * fade:
            chunk[:fade] *= ramp
            chunk[-fade:] *= ramp[::-1]
        pieces.append(chunk)
    return np.concatenate(pieces) if pieces else np.zeros(0, dtype=np.float32)


# ---------------------------------------------------------------- transcript

def transcribe(wav: str, model: str, lang: str, work: str) -> str:
    prefix = os.path.join(work, "tx")
    p = run(["whisper-cli", "-m", model, "-f", wav, "-l", lang, "-np",
             "-otxt", "-of", prefix])
    txt = prefix + ".txt"
    if not os.path.exists(txt):
        sys.exit(f"error: whisper produced nothing: {p.stderr.decode()[-400:]}")
    with open(txt, encoding="utf-8") as fh:
        return fh.read().strip()


def loop_check(text: str) -> tuple[bool, str, int, int]:
    """True when one sentence dominates, which means whisper looped on silence."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return True, "", 0, 0
    norm = [re.sub(r"[^\w\s]", "", ln.lower()).strip() for ln in lines]
    phrase, count = Counter(norm).most_common(1)[0]
    looped = count >= LOOP_MIN_REPEATS and count / len(lines) >= LOOP_MIN_SHARE
    return looped, phrase, count, len(lines)


# ---------------------------------------------------------------- note

def write_note(vault: str, title: str, transcript: str, take: str,
               total: float, speech: float, audio_rel: str, dry: bool) -> str:
    day = dt.datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join(os.path.expanduser(vault), "📥 Raw", "Voicenotes")
    path = os.path.join(folder, f"{day} {title}.md")
    body = (
        "---\n"
        "source: dji-mic\n"
        f"take: {os.path.splitext(os.path.basename(take))[0]}\n"
        f"duration: {hms(total)}\n"
        f"speech: {hms(speech)}\n"
        f"audio: {audio_rel}\n"
        f"created_at: {day}\n"
        f"updated_at: {day}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"Date: {day}\n\n"
        "## Transcript\n\n"
        f"{transcript}\n"
    )
    if dry:
        print(f"  would write note -> {path}")
        return path
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"  note      {path}")
    return path


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--card", help="DJI card path (auto-detected)")
    ap.add_argument("--take", help="force this wav instead of the newest")
    ap.add_argument("--title", help="note title; provisional if omitted")
    ap.add_argument("--vault", default=DEFAULT_VAULT)
    ap.add_argument("--archive", default="~/Movies/dji-archive")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--vad-model", default=DEFAULT_VAD)
    ap.add_argument("--vad-threshold", type=float, default=0.5)
    ap.add_argument("--min-silence-ms", type=int, default=400,
                    help="silence shorter than this stays in, so pauses breathe")
    ap.add_argument("--pad", type=float, default=PAD_S)
    ap.add_argument("--bitrate", default="24k")
    ap.add_argument("--lang", default="auto")
    ap.add_argument("--output", help="explicit .opus path")
    ap.add_argument("--keep-original", action="store_true",
                    help="also archive the full source wav, not just the speech-only file")
    ap.add_argument("--no-note", action="store_true", help="audio + transcript only")
    ap.add_argument("--no-clean", action="store_true", help="do not touch the card")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe", "whisper-cli", "whisper-vad-speech-segments"):
        need(tool)
    for label, path in (("model", args.model), ("VAD model", args.vad_model)):
        if not os.path.exists(path):
            sys.exit(f"error: {label} not found at {path}")

    card = find_card(args.card)
    if not card and not args.take:
        sys.exit("error: no DJI card found (looked for a TX_* folder with wavs)")
    take = pick_take(card, args.take)
    total = duration_of(take)
    print(f"\n=== {os.path.basename(take)}  {hms(total)}  "
          f"{os.path.getsize(take)/1e6:.1f} MB")

    audio = decode_16k(take)
    with tempfile.TemporaryDirectory() as work:
        full = os.path.join(work, "full.wav")
        run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR),
             "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", full], input=audio.tobytes())

        segs = merge(vad_segments(full, args.vad_model, args.vad_threshold,
                                  args.min_silence_ms), args.pad, total)
        speech = sum(e - s for s, e in segs)
        pct = 100.0 * speech / total if total else 0.0
        print(f"  speech    {len(segs)} segment(s), {hms(speech)} of {hms(total)} ({pct:.1f}%)")
        if speech < MIN_SPEECH_S:
            sys.exit("error: no speech found -- refusing to write anything")
        if pct > 95.0:
            print("  note: almost no silence found; check --vad-threshold if the take is quiet")

        cut_wav = os.path.join(work, "cut.wav")
        run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR),
             "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", cut_wav],
            input=cut(audio, segs).tobytes())

        out = os.path.expanduser(args.output) if args.output else os.path.join(
            os.path.expanduser(args.archive),
            dt.datetime.now().strftime("%Y-%m-%d"),
            os.path.splitext(os.path.basename(take))[0] + "-speech.opus")
        if not args.dry_run:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            run(["ffmpeg", "-y", "-v", "error", "-i", cut_wav, "-c:a", "libopus",
                 "-b:a", args.bitrate, "-application", "voip", out])
            print(f"  audio     {out}  ({os.path.getsize(out)/1e3:.0f} KB, "
                  f"{os.path.getsize(take)/max(1, os.path.getsize(out)):.0f}x smaller)")
        else:
            print(f"  would write {out}")

        transcript = transcribe(cut_wav, args.model, args.lang, work)

    looped, phrase, count, lines = loop_check(transcript)
    words = len(transcript.split())
    print(f"  transcript {words} words, {lines} line(s)")
    if looped:
        print(f"\n  HALLUCINATION LOOP: \"{phrase[:60]}\" x{count} of {lines} lines.")
        print("  The transcript is not real. Nothing written, card untouched.")
        print("  Try a lower --vad-threshold, or --take a different file.")
        return 2

    print("\n" + transcript + "\n")

    if not args.no_note:
        title = args.title or f"DJI note {dt.datetime.now().strftime('%H%M')}"
        if not args.title:
            print("  no --title given, filed provisionally -- rename it during the ingest")
        write_note(args.vault, title, transcript, take, total, speech,
                   os.path.relpath(out, os.path.expanduser("~")), args.dry_run)

    if args.no_clean:
        print("  card left alone (--no-clean)")
        return 0

    # WHY: the transcript passed, so the take has served its purpose. Order is
    # dji_sync's: produce -> verify -> archive -> checksum -> delete.
    print("  card:")
    if args.keep_original:
        archive_and_wipe(card, args.archive, args.dry_run)
    else:
        takes = find_takes(card)
        if args.dry_run:
            print(f"  would delete {len(takes)} take(s) from the card "
                  f"({sum(os.path.getsize(t) for t in takes)/1e6:.0f} MB), "
                  "keeping only the speech-only file")
        else:
            freed = 0
            for t in takes:
                freed += os.path.getsize(t)
                os.remove(t)
            print(f"  deleted {len(takes)} take(s), {freed/1e6:.0f} MB")
            vol = card
            while os.path.dirname(vol) != "/Volumes" and vol != "/":
                vol = os.path.dirname(vol)
            trash = os.path.join(vol, ".Trashes")
            if os.path.isdir(trash):
                for entry in glob.glob(os.path.join(trash, "*")):
                    run(["rm", "-rf", entry])
                print("  cleared .Trashes")
            if not find_takes(card):
                try:
                    os.rmdir(card)
                except OSError:
                    pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
