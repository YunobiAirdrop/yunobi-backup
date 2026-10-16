#!/usr/bin/env python3
"""Give the model eyes on a rendered video.

A render exits zero whether or not the graphic is on screen, inside the safe band, readable, or
gone before the cut. Only a picture settles that. This pulls frames out of any mp4, mov or webm,
burns the timecode and the source frame number into each one, and writes them where they can be
read back. The timecode is the point: a review that says "the label is clipped" costs a hunt, and
one that says "clipped at t=3.42s, f=103" is a one-line fix.

Selectors (pick one; --sheet is the default):
  --sheet          frames spread evenly across the clip, plus a contact sheet
  --fps F          sample at F frames per second
  --at T[,T...]    exact instants, seconds or mm:ss.ms
  --frames N[,N…]  exact source frame numbers
  --seams          detect the cuts and sample either side of each one
  --cuts T,T       same, from cut times you already know (the plan, beats.ts, the SRT)

Alpha clips (qtrle/argb, prores 4444, keyed webm) are matted over --bg first, because a
transparent PNG read straight back tells you nothing about what the viewer sees.

  --assert       run the mechanical checks instead: the alpha plane exists, the clip is the length
                 the beat is, no frame is empty, the last element has stopped moving before the cut,
                 and the file has not moved since the last check. Exits non-zero on any failure, so
                 a render loop gates on it and only spends frames on what a machine cannot see.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

FONT = next(
    (f for f in ("/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/System/Library/Fonts/Menlo.ttc",
                 "/Library/Fonts/Arial Unicode.ttf") if os.path.exists(f)),
    None,
)
ALPHA_FMTS = ("argb", "rgba", "abgr", "bgra", "yuva420p", "yuva422p", "yuva444p",
              "yuva444p10le", "yuva422p10le", "yuva420p10le")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_streams",
               "-show_format", "-of", "json", path])
    if out.returncode:
        sys.exit(f"ffprobe failed on {path}:\n{out.stderr.strip()}")
    data = json.loads(out.stdout)
    st = data["streams"][0]
    num, den = (st.get("r_frame_rate") or "25/1").split("/")
    fps = float(num) / float(den or 1)
    dur = float(st.get("duration") or data["format"].get("duration") or 0)
    alpha = st.get("pix_fmt") in ALPHA_FMTS or st.get("tags", {}).get("alpha_mode") == "1"
    return {"fps": fps, "dur": dur, "w": int(st["width"]), "h": int(st["height"]),
            "alpha": alpha, "pix_fmt": st.get("pix_fmt"), "codec": st.get("codec_name")}


def parse_time(s):
    s = s.strip()
    if ":" in s:
        parts = [float(p) for p in s.split(":")]
        out = 0.0
        for p in parts:
            out = out * 60 + p
        return out
    return float(s)


def vf(meta, args, t):
    """Matte the alpha, scale, then burn in the instant this frame was taken at.

    Returns the ffmpeg flags, not just a string, because an alpha clip needs a generated background
    input and therefore -filter_complex, while an opaque one is a plain -vf chain.

    The label is written from the seek time, not the stream clock: seeking with -ss before -i
    restarts the output PTS near zero, so `%{pts}` reports the same 0.02s on every single frame.
    """
    chain = []
    if not args.full:
        chain.append(f"scale={args.width}:-2:flags=lanczos")
    if not args.no_label and FONT:
        size = max(14, int((args.width if not args.full else meta["w"]) / 42))
        pad = size // 3
        label = f"t={t:.3f}s  f={int(round(t * meta['fps']))}"
        chain.append(
            f"drawtext=fontfile='{FONT}':text='{label}':x={pad}:y={pad}:fontsize={size}"
            f":fontcolor=white:box=1:boxcolor=black@0.65:boxborderw={pad}"
        )
    tail = ",".join(chain) if chain else "null"

    if meta["alpha"] and args.bg != "none":
        # A transparent PNG read back tells you nothing about what the viewer sees, so the frame is
        # composited over a flat matte first. drawbox cannot do this: it paints into the frame and
        # leaves the alpha channel alone, so the result is still see-through.
        # setpts and shortest are both load-bearing: seeking leaves the frame's PTS around 1.25s
        # while the generated matte starts at 0, and without them overlay finds no match and hands
        # back a bare grey card that looks like a clip which rendered nothing.
        graph = (f"color=c={args.bg}:s={meta['w']}x{meta['h']}[bg];"
                 f"[0:v]format=rgba,setpts=PTS-STARTPTS[fg];"
                 f"[bg][fg]overlay=shortest=1:format=auto,{tail}[v]")
        return ["-filter_complex", graph, "-map", "[v]"]
    return ["-vf", tail]


def grab(src, times, outdir, meta, args, tag="f"):
    """One ffmpeg call per instant. An accurate seek beats a fast one when the frame is the point."""
    written = []
    for i, t in enumerate(times):
        dst = os.path.join(outdir, f"{tag}{i:03d}_t{t:07.3f}.png")
        r = run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", src,
                 "-frames:v", "1", *vf(meta, args, t), "-y", dst])
        if r.returncode or not os.path.exists(dst):
            tail = r.stderr.strip().splitlines()
            print(f"  ! no frame at t={t:.3f}s: {tail[-1] if tail else 'past the end'}", file=sys.stderr)
            continue
        written.append((t, dst))
    return written


def cuts(src, threshold):
    r = run(["ffmpeg", "-v", "info", "-i", src, "-filter:v",
             f"select='gt(scene,{threshold})',metadata=print:file=-", "-f", "null", "-"])
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stdout + r.stderr)]


def sheet(frames, dst, cols, cell):
    """One image that shows the whole clip at a glance. Read this first; pull single frames after."""
    if not shutil.which("magick") or not frames:
        return None, "ImageMagick `magick` not found"
    cmd = ["magick", "montage"]
    if FONT:  # montage renders its labels through freetype and dies without a configured font
        cmd += ["-font", FONT]
    cmd += [p for _, p in frames]
    cmd += ["-tile", f"{cols}x", "-geometry", f"{cell}x+6+6", "-background", "#101010",
            "-depth", "8", "-quality", "88", dst]
    r = run(cmd)
    if r.returncode or not os.path.exists(dst):
        return None, (r.stderr.strip().splitlines() or ["montage failed"])[-1]
    return dst, None


# ---------------------------------------------------------------------------
# Assertions
#
# The frames above are eyes, and eyes are the only thing that catches a graphic that says the wrong
# thing. They are also the most expensive way to catch a graphic that is not there at all. Five of
# the review checks are mechanical - the alpha plane exists, the clip is the length the beat is, no
# frame is empty, the last element has stopped moving before the cut, the render did not silently
# move - and a mechanical check should never cost a model a picture. These run in about a second and
# exit non-zero, so a render loop can gate on them and only spend frames on what is left.
# ---------------------------------------------------------------------------

KNOWN_FRAMES = {
    (1080, 1920): "portrait, cut into a Short",
    (1920, 1080): "landscape wide, replaces the picture",
    (960, 1080): "landscape narrow, sits beside his face",
}


def sample_stats(path, hz, alpha_plane, meta=None):
    """Mean luma per sampled frame, or mean alpha when reading the alpha plane.

    A frame whose mean is at the floor is a frame with nothing on it. That is the render that exits
    zero having drawn nothing, which is the failure this whole file exists to stop.

    WHY the decoder is sometimes forced: a keyed webm carries its alpha in a VP9 side channel, so
    ffprobe reports pix_fmt yuv420p and the default decoder hands back no alpha at all. The picture
    looks opaque to every filter, `alphaextract` errors, and the check silently measures nothing.
    Only `-c:v libvpx-vp9` unpacks the second channel.
    """
    pre = []
    if alpha_plane and meta and meta.get("codec") == "vp9" and meta.get("pix_fmt") not in ALPHA_FMTS:
        pre = ["-c:v", "libvpx-vp9"]
    chain = f"fps={hz}"
    if alpha_plane:
        chain += ",alphaextract,format=gray"
    chain += ",signalstats,metadata=print:file=-"
    r = run(["ffmpeg", "-v", "error"] + pre + ["-i", path, "-filter:v", chain, "-f", "null", "-"])
    blob = r.stdout + r.stderr
    out, t = [], 0.0
    for line in blob.splitlines():
        m = re.match(r"frame:\d+\s+pts:\S+\s+pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
            continue
        m = re.match(r"lavfi\.signalstats\.YAVG=([0-9.]+)", line)
        if m:
            out.append((t, float(m.group(1))))
    return out


def freezes(path, noise, hold):
    """Every stretch where the picture stops changing, as (start, end) seconds.

    WHY freezedetect and not a scene score: the rule being checked is "the last element settles,
    then holds". A hold IS a freeze, so the filter answers the question directly, and it has been
    in ffmpeg long enough that it is not a version gamble.
    """
    r = run(["ffmpeg", "-v", "info", "-i", path, "-filter:v",
             f"freezedetect=n={noise}:d={hold}", "-map", "0:v:0", "-f", "null", "-"])
    blob = r.stdout + r.stderr
    starts = [float(m) for m in re.findall(r"freeze_start:\s*([0-9.]+)", blob)]
    ends = [float(m) for m in re.findall(r"freeze_end:\s*([0-9.]+)", blob)]
    spans = []
    for i, st in enumerate(starts):
        spans.append((st, ends[i] if i < len(ends) else None))
    return spans


def ledger_lane(video):
    """The lane `source.py` recorded for this file, or None when it was not borrowed."""
    p = os.path.join(os.path.dirname(os.path.abspath(video)), "sources.json")
    if not os.path.exists(p):
        return None
    try:
        rows = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for r in rows:
        if r.get("file") == os.path.basename(video):
            return r.get("lane") or "borrowed"
    return None


def state_path(video, override):
    """Where the last verdict for this file is remembered. Keyed by the absolute path."""
    import hashlib
    root = override or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "motion-watch")
    os.makedirs(root, exist_ok=True)
    key = hashlib.sha256(os.path.abspath(video).encode()).hexdigest()[:16]
    return os.path.join(root, f"{os.path.basename(video)}.{key}.json")


def file_hash(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_render(path, meta, args):
    """Run every mechanical check and print one line each. Returns the number that failed."""
    import datetime
    checks = []

    def ok(name, msg):
        checks.append(("ok", name, msg))

    def bad(name, msg):
        checks.append(("FAIL", name, msg))

    def warn(name, msg):
        checks.append(("warn", name, msg))

    # 1. Frame
    frame = KNOWN_FRAMES.get((meta["w"], meta["h"]))
    (ok if frame else warn)("frame", f"{meta['w']}x{meta['h']}" +
                            (f" is {frame}" if frame else " is not one of the project's frames"))

    # 2. Alpha. Expected from the flag, or from the name, because that is where it is declared.
    name = os.path.basename(path)
    named_alpha = "alpha" in name.lower() or "-alpha" in os.path.dirname(path).lower()
    want_alpha = args.expect_alpha or (named_alpha and not args.expect_opaque)
    if want_alpha and not meta["alpha"]:
        bad("alpha", f"no alpha plane; pix_fmt is {meta['pix_fmt']}. "
                     "The render dropped the channel and the key will composite as a black box.")
    elif want_alpha:
        how = ("VP9 side channel, alpha_mode=1" if meta["pix_fmt"] not in ALPHA_FMTS
               else meta["pix_fmt"])
        ok("alpha", f"alpha plane present ({how})")
    elif args.expect_opaque and meta["alpha"]:
        bad("alpha", f"alpha plane present ({meta['pix_fmt']}) but --expect-opaque was given")
    else:
        ok("alpha", "none, and none expected" if not meta["alpha"] else
                    f"alpha plane present ({meta['pix_fmt']}), not asserted either way")

    # 3. Duration against the beat it was built for
    frames_out = meta["dur"] * meta["fps"]
    if args.expect_frames or args.expect_seconds:
        want = args.expect_frames if args.expect_frames else args.expect_seconds * meta["fps"]
        drift = frames_out - want
        src = "--expect-frames" if args.expect_frames else "--expect-seconds"
        if abs(drift) > 0.5:
            bad("duration", f"{meta['dur']:.3f}s is {frames_out:.1f} frames, "
                            f"{src} says {want:.1f} ({drift:+.1f})")
        else:
            ok("duration", f"{meta['dur']:.3f}s is {frames_out:.0f} frames, as {src} says")
    else:
        ok("duration", f"{meta['dur']:.3f}s, {frames_out:.0f} frames at {meta['fps']:.2f}fps "
                       "(pass --expect-frames to check it against the beat)")

    # 4. Nothing empty. On an alpha clip the empty frame is a transparent one, not a dark one.
    plane = "alpha" if meta["alpha"] else "luma"
    # signalstats reports on the sample range of the format, so a 10-bit clip's black sits near 0
    # but its white sits at 1023. A floor written for 8-bit would pass anything on a ProRes render.
    depth = 4 if "10" in (meta["pix_fmt"] or "") else 16 if "12" in (meta["pix_fmt"] or "") else 1
    floor = (args.alpha_floor if meta["alpha"] else args.luma_floor) * depth
    stats = sample_stats(path, args.assert_hz, meta["alpha"], meta)
    if not stats and meta["alpha"]:
        # The alpha plane could not be read. Measuring the picture instead is still worth doing,
        # but say which plane the number came from or the next reader trusts the wrong check.
        stats = sample_stats(path, args.assert_hz, False, meta)
        plane, floor = "luma", args.luma_floor
        if stats:
            warn("blank", "the alpha plane would not decode; the numbers below are the picture")
    if not stats:
        warn("blank", "signalstats returned nothing; check the ffmpeg build")
    else:
        # An empty frame in the body is a render that drew nothing. An empty frame at the head or
        # the tail is the fade in and the fade out, which every keyed overlay has by design. Only
        # the first is a failure, or every CTA in the kit fails on its own exit.
        edge = args.edge
        empties = [(t, v) for t, v in stats if v < floor]
        body = [(t, v) for t, v in empties if edge <= t <= meta["dur"] - edge]
        lo_t, lo_v = min(stats, key=lambda p: p[1])
        if body:
            at = ", ".join(f"t={t:.2f}s" for t, _ in body[:6])
            bad("blank", f"{len(body)} sampled frames below mean {plane} {floor} inside the body "
                         f"({at}{', ...' if len(body) > 6 else ''}). Nothing is on screen there.")
        elif empties:
            where = " and ".join(
                w for w, hit in (("head", any(t < edge for t, _ in empties)),
                                 ("tail", any(t > meta["dur"] - edge for t, _ in empties))) if hit)
            ok("blank", f"nothing empty in the body; it fades past mean {plane} {floor} at the "
                        f"{where}, inside the {edge}s edge")
        else:
            ok("blank", f"no sampled frame below mean {plane} {floor} "
                        f"(lowest {lo_v:.1f} at t={lo_t:.2f}s)")

    # 5. Resolved before the cut: a hold has to reach the outgoing frame.
    #
    # The rule is about a drawn clip, where a moving element on the outgoing frame reads as a
    # mistake. Live action never holds still, so a borrowed shot is exempt. It says so itself: the
    # `sources.json` ledger `source.py` writes beside it is the record of what is borrowed, and
    # reading it here is cheaper than a flag somebody has to remember.
    borrowed = ledger_lane(path)
    if borrowed:
        checks.append(("ok", "hold", f"borrowed shot ({borrowed}), so the hold rule does not "
                                     "apply; live action is not a settling element"))
    elif args.no_hold:
        ok("hold", "not asserted, --no-hold")
    elif meta["dur"] < args.hold * 2:
        warn("hold", f"clip is {meta['dur']:.2f}s, too short to require a {args.hold}s hold")
    else:
        spans = freezes(path, args.freeze_noise, args.hold)
        tail = [s for s in spans if (s[1] is None or s[1] >= meta["dur"] - 0.05)]
        if tail:
            ok("hold", f"still from t={tail[-1][0]:.2f}s to the outgoing frame "
                       f"({meta['dur'] - tail[-1][0]:.2f}s of hold)")
        elif spans:
            last = spans[-1]
            bad("hold", f"still moving at the outgoing frame; the last hold ran "
                        f"{last[0]:.2f}s to {last[1]:.2f}s and nothing settles after it")
        else:
            bad("hold", f"nothing holds for {args.hold}s anywhere in the clip; "
                        "the last element is still travelling when the cut lands")

    # 6. Unchanged since the last assert, which is the byte-identical check the checklist asks for.
    #
    # WHY the ledger lives in a cache directory and not beside the file: renders can land in
    # a served folder, and a sidecar written there would be deployed with the asset. The question this check answers - has this file moved since I last looked at it - is
    # about one machine's history anyway, so the machine's cache is where it belongs.
    side = state_path(path, args.state)
    digest = file_hash(path)
    prev = None
    if os.path.exists(side):
        try:
            prev = json.load(open(side, encoding="utf-8"))
        except (OSError, ValueError):
            prev = None
    if prev and prev.get("sha256") != digest:
        warn("unchanged", f"the file moved since {prev.get('checked', 'the last run')}; "
                          "if this render was meant to be untouched, it was not")
    elif prev:
        ok("unchanged", f"byte-identical to the render checked {prev.get('checked', 'earlier')}")
    else:
        ok("unchanged", "first check on this file; the hash is now recorded")

    failed = sum(1 for level, _, _ in checks if level == "FAIL")
    print(f"{name}  {meta['w']}x{meta['h']}  {meta['fps']:.2f}fps  {meta['dur']:.2f}s  "
          f"{meta['codec']}/{meta['pix_fmt']}")
    for level, cname, msg in checks:
        print(f"  {level:<4}  {cname:<10} {msg}")

    with open(side, "w", encoding="utf-8") as fh:
        json.dump({"sha256": digest,
                   "checked": datetime.datetime.now().isoformat(timespec="seconds"),
                   "w": meta["w"], "h": meta["h"], "fps": meta["fps"], "dur": meta["dur"],
                   "pix_fmt": meta["pix_fmt"], "alpha": meta["alpha"],
                   "path": os.path.abspath(path),
                   "failed": failed}, fh, indent=2)

    print(f"\n{failed} failed, {sum(1 for l, _, _ in checks if l == 'warn')} warned, "
          f"{sum(1 for l, _, _ in checks if l == 'ok')} passed."
          + ("" if failed else " Nothing mechanical is wrong; now look at the frames."))
    return failed


def main():
    ap = argparse.ArgumentParser(description="Extract labelled frames from a render so they can be looked at.")
    ap.add_argument("video")
    ap.add_argument("--sheet", action="store_true", help="frames spread across the clip + a contact sheet")
    ap.add_argument("-n", "--count", type=int, default=20, help="frames for --sheet (default 20)")
    ap.add_argument("--fps", type=float, help="sample at this many frames per second")
    ap.add_argument("--at", help="exact instants, comma separated: 1.2,3,0:04.5")
    ap.add_argument("--frames", help="exact source frame numbers, comma separated")
    ap.add_argument("--seams", action="store_true", help="sample either side of every detected cut")
    ap.add_argument("--cuts", help="sample either side of these known cut times, comma separated")
    ap.add_argument("--scene", type=float, default=0.08,
                    help="cut detection threshold (default 0.08; our clips share one dark backdrop, "
                         "so a real cut between two of them scores far below ffmpeg's usual 0.3)")
    ap.add_argument("--range", help="restrict to A-B in seconds")
    ap.add_argument("--out", help="output directory (default <video>.watch/)")
    ap.add_argument("--width", type=int, default=960, help="scaled width (default 960)")
    ap.add_argument("--full", action="store_true", help="no downscale")
    ap.add_argument("--bg", default="0x6E6E6E", help="matte for alpha clips, or 'none' (default 0x6E6E6E)")
    ap.add_argument("--no-label", action="store_true", help="do not burn the timecode in")
    ap.add_argument("--cols", type=int, default=5, help="contact sheet columns (default 5)")
    ap.add_argument("--cell", type=int, default=360, help="contact sheet cell width (default 360)")
    ap.add_argument("--assert", dest="do_assert", action="store_true",
                    help="run the mechanical checks instead of extracting frames, and exit "
                         "non-zero if any fails")
    ap.add_argument("--expect-frames", type=float, help="the beat's frame count, for --assert")
    ap.add_argument("--expect-seconds", type=float, help="the beat's length in seconds, for --assert")
    ap.add_argument("--expect-alpha", action="store_true", help="require an alpha plane")
    ap.add_argument("--expect-opaque", action="store_true", help="require no alpha plane")
    ap.add_argument("--hold", type=float, default=0.2,
                    help="how long the last element must sit still before the cut (default 0.2s)")
    ap.add_argument("--assert-hz", type=float, default=4.0,
                    help="frames per second sampled for the blank check (default 4)")
    ap.add_argument("--luma-floor", type=float, default=2.0,
                    help="mean luma below which an opaque frame counts as empty (default 2.0)")
    ap.add_argument("--no-hold", action="store_true",
                    help="skip the hold check; borrowed shots are detected from sources.json "
                         "and skipped without this")
    ap.add_argument("--state", help="where --assert remembers the last verdict "
                                    "(default ~/.cache/motion-watch)")
    ap.add_argument("--edge", type=float, default=0.6,
                    help="head and tail seconds where an empty frame is the fade, not a fault "
                         "(default 0.6)")
    ap.add_argument("--alpha-floor", type=float, default=1.0,
                    help="mean alpha below which a keyed frame counts as empty (default 1.0)")
    ap.add_argument("--freeze-noise", default="0.003",
                    help="freezedetect noise tolerance for the hold check (default 0.003)")
    args = ap.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f"no such file: {args.video}")
    meta = probe(args.video)

    if args.do_assert:
        sys.exit(1 if assert_render(args.video, meta, args) else 0)

    lo, hi = 0.0, meta["dur"]
    if args.range:
        a, _, b = args.range.partition("-")
        lo, hi = parse_time(a), parse_time(b)

    outdir = args.out or os.path.splitext(args.video)[0] + ".watch"
    os.makedirs(outdir, exist_ok=True)
    for old in os.listdir(outdir):
        if old.endswith((".png", ".jpg")):
            os.remove(os.path.join(outdir, old))

    print(f"{os.path.basename(args.video)}  {meta['w']}x{meta['h']}  {meta['fps']:.2f}fps  "
          f"{meta['dur']:.2f}s  {meta['codec']}/{meta['pix_fmt']}"
          f"{'  alpha, matted over ' + args.bg if meta['alpha'] and args.bg != 'none' else ''}")

    made_sheet = False
    if args.at:
        times = [parse_time(t) for t in args.at.split(",")]
    elif args.frames:
        times = [int(n) / meta["fps"] for n in args.frames.split(",")]
    elif args.fps:
        step = 1.0 / args.fps
        times, t = [], lo
        while t < hi:
            times.append(t)
            t += step
    elif args.seams or args.cuts:
        seams = ([parse_time(t) for t in args.cuts.split(",")] if args.cuts
                 else cuts(args.video, args.scene))
        seams = [t for t in seams if lo <= t <= hi]
        if not seams:
            print("no cuts over the threshold. Pass the known cut times with --cuts, or lower "
                  "--scene; an even spread follows.", file=sys.stderr)
            args.sheet = True
            times = []
        else:
            print(f"{len(seams)} cuts: " + ", ".join(f"{t:.2f}s" for t in seams))
            # Before, at, and after: the last element must have resolved by the outgoing frame, and
            # the incoming clip must already read on the frame after the cut.
            times = sorted({max(lo, t + d) for t in seams for d in (-0.10, 0.04, 0.40) if lo <= t + d <= hi})
    else:
        args.sheet = True
        times = []

    if args.sheet and not times:
        span = max(hi - lo, 0.001)
        n = max(1, args.count)
        times = [lo + span * (i + 0.5) / n for i in range(n)]
        made_sheet = True

    frames = grab(args.video, times, outdir, meta, args)
    for t, p in frames:
        print(f"  t={t:7.3f}s  f={int(round(t * meta['fps'])):5d}  {p}")

    if made_sheet:
        s, err = sheet(frames, os.path.join(outdir, "_sheet.jpg"), args.cols, args.cell)
        print(f"  contact sheet: {s}" if s else f"  contact sheet skipped: {err}")

    if not frames:
        sys.exit("no frames written")
    print(f"\n{len(frames)} frames in {outdir}. Read them, then name every fix with its t= and f=.")


if __name__ == "__main__":
    main()
