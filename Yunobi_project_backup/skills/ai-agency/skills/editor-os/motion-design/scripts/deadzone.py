#!/usr/bin/env python3
"""What the platform's own UI will cover, on a rendered vertical clip.

WHY THIS EXISTS: `craft.md` keeps the subject between y=300 and y=1650 and `carousel` reserves 260
top / 400 bottom. Both are VERTICAL only. Neither has a right-hand bound, and the right-hand action
rail - like, comment, share, the spinning record - is the one that actually eats a graphic, because
it sits over the middle-right of the frame where a card naturally lands.

This is a different constraint from the composition band and does not replace it. The band is about
what reads well; this is about what is OCCLUDED, and it is per destination: a file that is clean for
Shorts can lose a whole card on Reels.

WHERE THE NUMBERS COME FROM, and how far to trust them: no vendor publishes a machine-readable safe
area. TikTok's own help article for it 404s. Third-party guides disagree with each other - for Reels
one says 220 top / 420 bottom, another 108 / 320 / 60 left / 120 right; for TikTok one says 130 top /
484 bottom / 140 right, another repeats the 108 / 320 / 60 / 120. So the map below is the CONSERVATIVE
INTERSECTION of what they claim, not a specification, and it is deliberately pessimistic: a false
alarm costs a glance and a miss costs a card.

**Replace it the moment a real screenshot exists.** `--calibrate <screenshot.png>` prints the map
this file would need to match a frame grabbed from the app itself with the UI showing, which is the
only measurement that settles it.

    deadzone.py <clip.mp4> [--for reels|tiktok|shorts|all] [--fps 2] [--sheet]
    deadzone.py --map [--for reels]
    deadzone.py --calibrate <screenshot.png>

Non-zero exit when anything lands in a zone, so it drops straight into a check.
"""
import os, subprocess, sys
import numpy as np

W, H = 1080, 1920

# left, top, right, bottom insets in pixels of a 1080x1920 frame. Conservative intersection.
ZONES = {
    "reels":  {"top": 220, "bottom": 484, "left": 60, "right": 140},
    "tiktok": {"top": 220, "bottom": 484, "left": 60, "right": 140},
    "shorts": {"top": 140, "bottom": 300, "left": 40, "right": 120},
}
EDGE = 28.0          # gradient magnitude that counts as ink rather than a gradient background
SHARE = 0.004        # share of a zone's pixels that must be ink before it is a hit


def frames(path, fps):
    """Greyscale frames at `fps`, as HxW float arrays, scaled to the reference frame."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", "fps=%g,scale=%d:%d" % (fps, W // 4, H // 4),
         "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = (W // 4) * (H // 4)
    count = len(raw) // n
    if not count:
        sys.exit("no frames read from %s" % path)
    return np.frombuffer(raw[:count * n], dtype=np.uint8).reshape(count, H // 4, W // 4).astype(np.float32)


def ink(frame):
    """Where there is an edge. A flat gradient background has none; type and rules have plenty."""
    gy, gx = np.gradient(frame)
    return np.hypot(gx, gy) > EDGE


def boxes(zone, scale):
    """The four occluded rectangles as slices, in the scaled frame."""
    t, b = int(zone["top"] * scale), int((H - zone["bottom"]) * scale)
    l, r = int(zone["left"] * scale), int((W - zone["right"]) * scale)
    h, w = int(H * scale), int(W * scale)
    return {"top": (slice(0, t), slice(0, w)), "bottom": (slice(b, h), slice(0, w)),
            "left": (slice(t, b), slice(0, l)), "right": (slice(t, b), slice(r, w))}


def check(path, targets, fps, sheet):
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                           capture_output=True, text=True).stdout.strip()
    if probe != "%d,%d" % (W, H):
        sys.exit("%s is %s, not %dx%d. This map is the vertical frame only." % (path, probe, W, H))
    fs = frames(path, fps)
    scale = 0.25
    bad = 0
    for name in targets:
        rects = boxes(ZONES[name], scale)
        worst = {k: (0.0, 0.0) for k in rects}
        for i, f in enumerate(fs):
            e = ink(f)
            for k, (ys, xs) in rects.items():
                patch = e[ys, xs]
                if patch.size == 0:
                    continue
                s = float(patch.mean())
                if s > worst[k][0]:
                    worst[k] = (s, i / fps)
        hits = {k: v for k, v in worst.items() if v[0] > SHARE}
        if hits:
            bad += 1
            print("%-7s FAIL" % name)
            for k, (s, t) in sorted(hits.items(), key=lambda kv: -kv[1][0]):
                print("        %-6s %.2f%% of the zone is ink, worst at t=%.1fs" % (k, s * 100, t))
        else:
            print("%-7s clear (worst %.2f%%)" % (name, 100 * max(v[0] for v in worst.values())))
    if sheet:
        out = os.path.splitext(path)[0] + "_deadzone.png"
        z = ZONES[targets[0]]
        draw = ("drawbox=0:0:%d:%d:red@0.35:t=fill," % (W, z["top"]) +
                "drawbox=0:%d:%d:%d:red@0.35:t=fill," % (H - z["bottom"], W, z["bottom"]) +
                "drawbox=0:%d:%d:%d:red@0.35:t=fill," % (z["top"], z["left"], H - z["top"] - z["bottom"]) +
                "drawbox=%d:%d:%d:%d:red@0.35:t=fill" % (W - z["right"], z["top"], z["right"],
                                                         H - z["top"] - z["bottom"]))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", draw,
                        "-frames:v", "1", out], check=False)
        print("overlay: %s (%s)" % (out, targets[0]))
    return 1 if bad else 0


def calibrate(shot):
    """Print the map a real app screenshot implies. The only measurement that settles the numbers."""
    print("Grab a frame from the app with the UI showing, at %dx%d, then read off:" % (W, H))
    print("  top    = y of the lowest pixel of the top UI")
    print("  bottom = %d - y of the highest pixel of the caption/audio block" % H)
    print("  left   = x of the rightmost pixel of any left-edge UI")
    print("  right  = %d - x of the leftmost pixel of the action rail" % W)
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of", "csv=p=0", shot],
                           capture_output=True, text=True).stdout.strip()
    print("\n%s is %s. Put the four numbers into ZONES in this file and say where they were measured."
          % (shot, probe))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    target, fps, sheet, path = "all", 2.0, False, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--for":
            target = argv[i + 1]; i += 2
        elif a == "--fps":
            fps = float(argv[i + 1]); i += 2
        elif a == "--sheet":
            sheet = True; i += 1
        elif a == "--map":
            for k, v in ZONES.items():
                print("%-7s %s" % (k, v))
            return 0
        elif a == "--calibrate":
            calibrate(argv[i + 1]); return 0
        else:
            path = a; i += 1
    if not path:
        sys.exit(__doc__)
    targets = list(ZONES) if target == "all" else [target]
    for t in targets:
        if t not in ZONES:
            sys.exit("no zone %r. Known: %s" % (t, ", ".join(ZONES)))
    return check(path, targets, fps, sheet)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
