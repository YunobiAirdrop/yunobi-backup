#!/usr/bin/env python3
"""Measure a beat off the live project document, on the clock the render is cut against.

WHY THIS EXISTS: a subtitle export is a second clock read by eye, and reading it by eye is how
the Glance set ended up timed 200 seconds wrong. This computes the play clock from the document
itself - the cumulative duration of the unblocked taus, which is exactly what `get_project`
reports as the composition duration - so a beat's in and out points are derived, never typed.

WHY CHARACTER-PROPORTIONAL WITHIN A TAU: a tauAnchor is {tauId, location} where location is a
character offset, so a pin already starts mid-tau. The document carries no per-word timing, so a
position inside a tau is interpolated across its characters, which is the same approximation the
subtitle export makes.

    beatclock.py doc.json                       every surviving tau, with its start
    beatclock.py doc.json --find "a phrase"     the taus holding it
    beatclock.py doc.json --beat "from phrase" "to phrase"    start, end, duration
"""

"""Usage:

  python3 beatclock.py <doc.json>                       # the whole clock
  python3 beatclock.py <doc.json> --beat "<phrase>" [nth]  # one beat's in and out
"""
import json, sys

def load(path):
    doc = json.load(open(path))
    taus = doc["compositions"][0]["timeline"]["superTau"]["taus"]
    rows, t = [], 0.0
    for i, tau in enumerate(taus):
        if tau.get("isBlocked"):
            continue
        # `duration` is SOURCE time. A tau played at speed 1.05 occupies duration/1.05 on the
        # timeline, so dividing is what makes the total equal the composition duration the API
        # reports: ES02 sums to 476.83s undivided and 454.54s divided, and 454.54 is the truth.
        seg = tau["audioSegment"]
        dur = seg["duration"] / (seg.get("speed") or 1)
        raw = tau["text"]["string"]
        rows.append({"i": i, "start": t, "dur": dur, "raw": raw, "flat": " ".join(raw.split())})
        t += dur
    return rows, t

def at(rows, needle, end=False, nth=1):
    """The play-clock second where `needle` starts (or ends), interpolated inside its tau."""
    key = " ".join(needle.lower().split())
    hits = [r for r in rows if key in r["flat"].lower()]
    if not hits:
        sys.exit("no tau holds %r" % needle)
    if len(hits) < nth:
        sys.exit("only %d matches for %r, nth=%d" % (len(hits), needle, nth))
    if len(hits) > 1 and nth == 1:
        print("  warning: %d taus hold %r, taking the first" % (len(hits), needle), file=sys.stderr)
    r = hits[nth - 1]
    pos = r["flat"].lower().index(key) + (len(key) if end else 0)
    return r["start"] + r["dur"] * (pos / max(1, len(r["flat"])))

if __name__ == "__main__":
    rows, total = load(sys.argv[1])
    if "--beat" in sys.argv:
        k = sys.argv.index("--beat")
        a, b = at(rows, sys.argv[k + 1]), at(rows, sys.argv[k + 2], end=True)
        print(f"start {a:8.2f}   end {b:8.2f}   duration {b - a:6.2f}s")
    elif "--find" in sys.argv:
        k = sys.argv.index("--find")
        key = " ".join(sys.argv[k + 1].lower().split())
        for r in rows:
            if key in r["flat"].lower():
                print(f'{r["start"]:8.2f} (+{r["dur"]:6.2f}s) #{r["i"]}  {r["flat"][:140]}')
    else:
        for r in rows:
            print(f'{r["start"]:8.2f} (+{r["dur"]:6.2f}s) #{r["i"]}  {r["flat"][:110]}')
        print(f"\nsurviving taus: {len(rows)}   plays: {total:.2f}s")
