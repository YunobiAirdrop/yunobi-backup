#!/usr/bin/env python3
"""Dead air in a rendered composition: where the pauses are, and how much of the runtime they cost.

WHY THIS EXISTS: a transcript holds no silence. `candidates.py` enumerates the wreckage of speaking
from the words - stutters, restarts, duplicate takes - and it cannot see the two-second hole between
two clean sentences, because nothing in the document records one. That hole is real runtime and it
is the difference between a cut that is tight and one that is merely correct.

The audio holds it, and ffmpeg reads it for free: no model, no API key, no credits, one decode.
Measured on the ClickUp Mini-Course Intro, an ALREADY CUT composition: 51 pauses over a 0.35s keep,
7.1s recoverable of 171.3s, which is 4.2% of a video somebody had already tightened by hand.

WHY IT RUNS ON THE EXPORT, NOT THE RAW TAKE: a tau's audioSegment.offset addresses whatever media it
was cut from, and in a real project that is a sequence, so raw-take seconds and script seconds are
different numbers. The rendered composition IS the play clock - the one `beatclock.py` computes and
every anchor counts on - so a pause found here is already at the timecode a pin would use.

WHY IT PICKS ITS OWN THRESHOLD: -30dB is not a constant, it is a room. A tau boundary is a pause the
transcriber heard, so the composition supplies its own ground truth: sweep, and keep the threshold
whose pauses best explain the boundaries WITHOUT flooding the take. Measured on the Intro, -32dB /
0.20s explains 74% of boundaries at 0.53 pauses a second; -20dB / 0.15s explains 97% with 230 of
them, which is one every 0.74s and no longer a pause, it is the gaps between words. A density
ceiling throws that row out, which is why the sweep is scored and not just maximised.

TWO THINGS THIS DELIBERATELY DOES NOT DO, both measured and both negative:

- **It is not a word clock.** The hypothesis was to split a tau at its internal pauses, give the
  words to the speech runs, and beat the character interpolation `beatclock.py` and `layout anchor`
  use. Measured against Descript's own SRT for the Intro: median error 0.11s for BOTH clocks over 48
  cues, and 0.39s against 0.44s over the 7 cues sitting more than four seconds into their paragraph.
  Descript already breaks the script at pauses, so a tau rarely holds the structure to exploit.
- **It does not prove an export matches a document.** Pause matching looked like a check and is not:
  the wrong export - Day 1, 1109s - still explained 73.7% of the Intro's 38 boundaries, because at
  1332 pauses over 1109s any timestamp is near one by chance. The check that works is the one
  `beatclock.py` already documents: the script total equals the composition duration. `calibrate`
  gates on that first and refuses before it sweeps anything.

    silences.py detect    <export.mp4> [--noise -24] [--min 0.25]      the pauses, and the speech ratio
    silences.py calibrate <export.mp4> <doc.json> [comp]               the threshold this room wants
    silences.py deadair   <export.mp4> <doc.json> [comp] [--keep 0.35] the cut list the words cannot give

`doc.json` is `pnpm descript doc <project> --out doc.json`, or any payload `dscript.py grab`
archived. `comp` names or indexes the composition; omit it for the first.
"""
import json, os, re, subprocess, sys, statistics
import numpy as np

SWEEP_NOISE = [-20, -24, -28, -32, -36, -40]
SWEEP_MIN = [0.20, 0.25, 0.35, 0.50]
TOL = 0.40          # a tau boundary this close to a pause counts as landing on it
MAX_DENSITY = 0.8   # more pauses per second than this is word gaps, not pauses
DUR_TOL = 0.02      # the export may differ from the script total by this share before it is stale
HOP = 0.01          # the envelope's resolution, seconds


# --- the media ------------------------------------------------------------------------------------

def envelope(media):
    """One decode to a dBFS envelope at 10ms, so a threshold sweep costs nothing after it.

    ffmpeg's own `silencedetect` would need a full decode per threshold - eighteen passes over a
    1109s export is where this script first timed out.
    """
    pcm = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", media,
         "-map", "a:0", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        capture_output=True).stdout
    x = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
    n = int(16000 * HOP)
    x = x[:len(x) // n * n].reshape(-1, n)
    rms = np.sqrt((x * x).mean(axis=1)) + 1e-9
    return 20 * np.log10(rms)


def pauses(env, noise, mind):
    """Every run of frames under the threshold that lasts at least `mind`, as (start, end) seconds."""
    quiet = env < noise
    out, i, n = [], 0, len(quiet)
    while i < n:
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < n and quiet[j]:
            j += 1
        if (j - i) * HOP >= mind:
            out.append((i * HOP, j * HOP))
        i = j
    return out


def duration(media):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", media], capture_output=True, text=True).stdout
    return float(out.strip())


# --- the document ---------------------------------------------------------------------------------

def taus(path, comp=None):
    """Unblocked taus of one composition, each with its play start. An Ignore draws no time."""
    d = json.load(open(path))
    if "compositions" in d:
        c = pick_comp(d["compositions"], comp)
        raw, name = c["timeline"]["superTau"]["taus"], c.get("name", "?")
    else:
        raw, name = d["data"][0]["copiedTaus"], "clipboard"
    rows, play = [], 0.0
    for t in raw:
        if t.get("isBlocked"):
            continue
        text = t["text"]["string"]
        rows.append({"id": t.get("id"), "flat": " ".join(text.split()),
                     "play": play, "dur": t["audioSegment"]["duration"]})
        play += t["audioSegment"]["duration"]
    return rows, play, name


def pick_comp(comps, needle):
    if needle is None:
        return comps[0]
    if needle.isdigit():
        return comps[int(needle)]
    hits = [c for c in comps if needle.lower() in (c.get("name") or "").lower()]
    if len(hits) != 1:
        sys.exit("composition %r matches %d of %d: %s"
                 % (needle, len(hits), len(comps), [c.get("name") for c in comps]))
    return hits[0]


def same_cut(media, total, name):
    """The check that says this export is this script. Duration equality, and nothing softer."""
    dur = duration(media)
    off = dur - total
    if abs(off) > max(1.0, DUR_TOL * total):
        sys.exit("REFUSE: %s is %.1fs of script and this export is %.1fs (%+.1fs). A stale render, "
                 "the wrong composition, or a cut made since. Re-export before timing anything "
                 "against it - a plan on the wrong clock is how twelve clips went out 203.8s wrong."
                 % (name, total, dur, off))
    return dur


# --- the threshold ----------------------------------------------------------------------------------

def score(rows, spans):
    """Share of tau boundaries explained by a pause. Speech resumes at a silence END, and a tau
    starts where speech resumes."""
    ends = sorted(e for _, e in spans)
    if not ends or len(rows) < 2:
        return 0.0, 9.9
    d = [min(abs(e - r["play"]) for e in ends) for r in rows[1:]]
    return sum(1 for x in d if x <= TOL) / len(d), statistics.median(d)


def calibrate(media, doc, comp=None, verbose=True):
    rows, total, name = taus(doc, comp)
    dur = same_cut(media, total, name)
    env = envelope(media)
    if verbose:
        print("%s: %d taus, %.1fs of script, export %.1fs - same cut" % (name, len(rows), total, dur))
    best = None
    for n in SWEEP_NOISE:
        for m in SWEEP_MIN:
            spans = pauses(env, n, m)
            hit, med = score(rows, spans)
            dense = len(spans) / dur
            flag = "  flooded" if dense > MAX_DENSITY else ""
            if verbose:
                print("  %4ddB  d=%.2f  %4d pauses (%.2f/s)  %5.1f%% of boundaries  median %.2fs%s"
                      % (n, m, len(spans), dense, hit * 100, med, flag))
            if dense > MAX_DENSITY:
                continue
            if best is None or (hit, -med) > (best[0], -best[1]):
                best = (hit, med, n, m)
    if best is None:
        sys.exit("every threshold floods this take: the room is louder than the speech")
    hit, med, n, m = best
    if verbose:
        print("\nthis room wants  --noise %d --min %g   (%.1f%% of %d boundaries, median miss %.2fs)"
              % (n, m, hit * 100, len(rows) - 1, med))
    return n, m, env


# --- commands -------------------------------------------------------------------------------------

def tc(t):
    return "%d:%05.2f" % (int(t // 60), t % 60)


def cmd_detect(media, noise, mind):
    noise = noise if noise is not None else -24
    mind = mind if mind is not None else 0.25
    env = envelope(media)
    spans = pauses(env, noise, mind)
    dur = len(env) * HOP
    quiet = sum(e - s for s, e in spans)
    print("%s\n%d pauses at %ddB/%gs, %.1fs of %.1fs quiet, %.0f%% speech, longest %.2fs"
          % (media, len(spans), noise, mind, quiet, dur, 100 * (1 - quiet / dur),
             max((e - s for s, e in spans), default=0)))
    for s, e in spans[:40]:
        print("  %s  %s  %.2fs" % (tc(s), tc(e), e - s))
    if len(spans) > 40:
        print("  ... %d more" % (len(spans) - 40))


def cmd_deadair(media, doc, comp, noise, mind, keep):
    rows, total, name = taus(doc, comp)
    if noise is None or mind is None:
        noise, mind, env = calibrate(media, doc, comp, verbose=False)
    else:
        same_cut(media, total, name)
        env = envelope(media)
    spans = pauses(env, noise, mind)
    found, recover = [], 0.0
    for r in rows:
        a, b = r["play"], r["play"] + r["dur"]
        for s, e in spans:
            s, e = max(s, a), min(e, b)
            if e - s > keep:
                recover += e - s - keep
                found.append((s + keep, e - s - keep, r["flat"][:58]))
    print("%s   noise %ddB  min %gs  keep %.2fs" % (name, noise, mind, keep))
    print("%d pauses over the keep, %.1fs recoverable of %.1fs (%.1f%%)"
          % (len(found), recover, total, 100 * recover / max(total, 1e-9)))
    for at, ex, ctx in sorted(found, key=lambda f: -f[1])[:25]:
        print("  %s  -%.2fs  %s" % (tc(at), ex, ctx))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, rest = argv[0], argv[1:]
    noise = mind = keep = None
    args, i = [], 0
    while i < len(rest):
        if rest[i] == "--noise":
            noise = int(rest[i + 1].replace("dB", "")); i += 2
        elif rest[i] == "--min":
            mind = float(rest[i + 1]); i += 2
        elif rest[i] == "--keep":
            keep = float(rest[i + 1]); i += 2
        else:
            args.append(rest[i]); i += 1
    g = lambda n: args[n] if len(args) > n else None
    if cmd == "detect":
        cmd_detect(args[0], noise, mind)
    elif cmd == "calibrate":
        calibrate(args[0], args[1], g(2))
    elif cmd == "deadair":
        cmd_deadair(args[0], args[1], g(2), noise, mind, keep if keep is not None else 0.35)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
