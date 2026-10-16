#!/usr/bin/env python3
"""The shot pass's second half: the beats a trigger cannot see, read off the whole script.

`sequence.py plan` is pass 1 of the shots and it is deterministic: six triggers, each of
them a surface pattern - a number in the line, a demonstrative phrase, a contrastive
opener, or dead air. What no pattern finds is a sentence that is well formed, carries no
number and names a STRUCTURE, which is most of what a graphic is for. The author, 8 Sep 2026,
on EA20 at 12:09 - "so that ClickUp, your project tool, could talk to Notion, your
documentation tool" - asked why the plan had put a zoom there: "why isn't the descript
skill smart enough to know that this is a visual context?" It is not, and it cannot be:
the line has no digit in it, so the `motion` trigger never fires and `zoom` takes the
stretch as dead air.

So the shots get the same two-pass shape the cuts got: a script enumerates what a script
can find, and a read finds the rest.

    python3 visuals.py brief doc.json --out visuals.txt   # the reader's input
    python3 visuals.py check doc.json briefs.json         # resolve what came back
    python3 visuals.py check doc.json briefs.json --plan pins.json   # and against pass 1

The brief the reader runs on is in `references/sequencing.md`. Exit status is 1 when a
brief does not resolve, or when `--plan` finds the plan is mostly zooms.
"""
import sys

import schema
from sequence import clock, load

# The share of a plan's slots that may be zoom steps before the plan is a zoom ladder with
# opinions. EA20 came in at 29 of 42, 69%, with five motion slots in a 22-minute video.
ZOOM_CEILING = 0.45
# Seconds either side of a brief within which an existing slot counts as covering it.
NEAR = 6.0
ADDS = ("quantity", "consequence", "structure", "recognition")


def mmss(t):
    return "%d:%02d" % (int(t // 60), int(t % 60))


def rows_of(path, n=0):
    taus, cards, scenes, media, name = load(path, n)
    rows, _, total = clock(taus)
    return rows, total, name


def write_brief(rows, total, name, out):
    """One live paragraph per line, indexed and timecoded, the way the pass-2 brief does it."""
    lines = ["# %s - %s, %d live paragraphs" % (name, mmss(total), len(rows))]
    for i, r in enumerate(rows):
        lines.append("[%d] %s  %s" % (i, mmss(r["start"]), r["flat"]))
    text = "\n".join(lines) + "\n"
    if out:
        open(out, "w").write(text)
        print("wrote %s - %d paragraphs, %s of script" % (out, len(rows), mmss(total)))
    else:
        sys.stdout.write(text)


def resolve(rows, briefs):
    """Each brief against the live script. A brief that does not land is dropped, never guessed."""
    ok, bad = [], []
    for b in briefs:
        if isinstance(b, list):
            b = dict(zip(("i", "line", "adds", "shows"), b))
        i, line = b.get("i"), (b.get("line") or "").strip()
        why = None
        if not isinstance(i, int) or not 0 <= i < len(rows):
            why = "no paragraph %r" % (i,)
        elif not line:
            why = "no line"
        elif line not in rows[i]["flat"]:
            why = "not verbatim in [%d]" % i
        elif b.get("adds") not in ADDS:
            why = "adds=%r is not one of %s" % (b.get("adds"), "/".join(ADDS))
        if why:
            bad.append((b, why))
        else:
            ok.append({**b, "at": rows[i]["start"], "line": line})
    return ok, bad


def slots_of(pins, rows):
    """(seconds, trigger) for every slot pass 1 proposed.

    A pin carries no timecode and never should: `plan` anchors on the PHRASE because the cut moves
    everything after it - `references/sequencing.md`, "the bracket is a seed, never the anchor". So
    the clock comes from the same live rows this pass reads, by finding the phrase in them.
    """
    out = []
    for p in pins:
        frm = " ".join(str(p.get("from", "")).split())
        row = next((r for r in rows if frm and frm in r["flat"]), None)
        if row:
            out.append((row["start"], "zoom" if "zoom" in p else (p.get("why") or "?")))
    return out


def main():
    argv = sys.argv[1:]
    if not argv:
        sys.exit(__doc__)
    cmd, args = argv[0], [a for a in argv[1:] if not a.startswith("--")]
    opt = lambda flag: argv[argv.index(flag) + 1] if flag in argv else None
    for flag in ("--out", "--plan", "--comp"):
        if opt(flag) in args:
            args.remove(opt(flag))
    n = int(opt("--comp") or 0)

    rows, total, name = rows_of(args[0], n)

    if cmd == "brief":
        write_brief(rows, total, name, opt("--out"))
        return 0

    if cmd != "check":
        sys.exit("commands: brief, check")

    briefs = schema.load(args[1], "briefs")
    # Checked before any output, so a bad plan never prints half a table.
    plan = schema.load(opt("--plan"), "pins") if opt("--plan") else None
    ok, bad = resolve(rows, briefs)
    for b, why in bad:
        print("DROPPED %r: %s" % (str(b.get("line"))[:60], why))

    slots = slots_of(plan, rows) if plan is not None else []
    graphic = [(t, k) for t, k in slots if k not in ("zoom", "jumpcut", "punch")]

    print("\n%-7s %-12s %-11s %s" % ("at", "adds", "pass 1", "the line"))
    for b in sorted(ok, key=lambda b: b["at"]):
        near = [k for t, k in slots if abs(t - b["at"]) <= NEAR]
        state = "covered" if any(k not in ("zoom", "jumpcut", "punch") for k in near) else (
            "zoom only" if near else "nothing")
        print("%-7s %-12s %-11s %s" % (mmss(b["at"]), b["adds"], state, b["line"][:78]))
        if b.get("shows"):
            print("%-7s %s" % ("", b["shows"][:96]))

    missed = [b for b in ok
              if not any(abs(t - b["at"]) <= NEAR and k not in ("zoom", "jumpcut", "punch")
                         for t, k in slots)]
    print("\n%d briefs, %d resolved, %d dropped" % (len(briefs), len(ok), len(bad)))
    fail = bool(bad)
    if slots:
        zooms = sum(1 for _, k in slots if k == "zoom")
        share = zooms / len(slots)
        print("pass 1: %d slots, %d graphic, %d zoom steps = %.0f%%"
              % (len(slots), len(graphic), zooms, 100 * share))
        print("%d of the %d briefs stand where pass 1 proposed no graphic" % (len(missed), len(ok)))
        if share > ZOOM_CEILING:
            print("OVER the %.0f%% zoom ceiling: the plan is a ladder, not a shot list"
                  % (100 * ZOOM_CEILING))
            fail = True
    print("\nEvery line above is a brief to dispatch in this turn, never a hole to report.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
