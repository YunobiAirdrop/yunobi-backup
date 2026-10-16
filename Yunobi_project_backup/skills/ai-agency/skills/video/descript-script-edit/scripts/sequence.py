#!/usr/bin/env python3
"""The rhythm of an edit: how often it cuts, how often the frame changes, how much is covered.

WHY THIS EXISTS: `pins.py` places a clip and `layout apply` stamps a look, but nothing decided
WHERE either belongs, so the cut half of the edit was automated and the shot half stayed manual.
This reads the rhythm off a finished edit (`audit`) and proposes the next one from the surviving
script (`plan`), in the pins.json shape `pins.py` already consumes.

THE CLOCK IS SPEED-ADJUSTED. `audioSegment.duration` is source time; a tau played at speed 1.05
occupies duration/1.05 on the timeline. ES02 sums to 476.83s raw and 454.54s adjusted, and 454.54
is what `get_project` reports. Every second printed here is the adjusted one.

BOTH HOMES OF THE SAME SHAPES. A `doc.json` from the CLI keeps them under
`compositions[].timeline`; the clipboard payload `dscript grab` writes keeps the identical
structures under `data[0]` as `copiedTaus`, `copiedComponents` and `pinTracks`. Either one works,
so the rhythm can be read without a second tool in the loop.

    sequence.py audit <doc.json|grab.json> [--comp N]        what rhythm this edit actually has
    sequence.py plan  <doc.json|grab.json> [--comp N] [--out pins.json]
"""
import json, re, sys

# The gate, measured on two finished edits. references/sequencing.md carries the table.
GATE_DEAD = 12.0        # seconds the frame may sit unchanged
GATE_MEDIAN = 7.0       # median seconds between state changes
GATE_COVER = (0.20, 0.50)   # share of runtime under a visual overlay

LIST_MAX = 2.6          # a clause this short, three in a row, is a micro-cut run
# The zoom ladder ES02 uses, and it returns to 100 between steps: a zoom pin has no closing
# card, so it holds until the next one and two steps in a row read as a drift, not a cut.
LADDER = [110, 100, 120, 100, 130, 100]
SPAN = 5.0              # a b-roll insert runs about this long; ES02's median is 4.7s
SHOW = re.compile(r"\b(this is what|here'?s what|here is what|let me show|i'?ll show|"
                  r"an example of|this is an example|look at|on (the )?screen|what it looks like|"
                  r"what it can look like)\b", re.I)
COUNT = re.compile(r"\b(\d+\s*(\+|plus)?\s*(agencies|clients|people|hours|days|weeks|months|"
                   r"years|percent|k|x)|tens of|hundreds of|thousands of|"
                   r"two|three|four|five)\b", re.I)
CTA = re.compile(r"\b(link is (down|in) (the )?description|down description|book a call|"
                 r"see you on the other side|it'?s your (choice|decision))\b", re.I)
TC = re.compile(r"\[(\d{2})-(\d{2})\]")
# An announcement of what the next sentence will say. Cutting one inside a dead stretch is a
# cheaper fix than a zoom, because it buys the jump cut AND takes the words out: ES02's worst
# stretch (29s at 6:31) is split by ignoring "And one last thing," and nothing is lost.
ANNOUNCE = re.compile(r"^(and |now |so |but )?(one last thing|another thing|the last thing|"
                      r"what i (wanna|want to|will) (say|tell you|explain)|"
                      r"here is the thing|here's the thing|let me explain|"
                      r"before (i|we) (go|move|continue)|the other thing)\b", re.I)
ANNOUNCE_MAX = 3.5      # seconds; a longer tau is carrying an argument, not announcing one


# ---------------------------------------------------------------- the document

def load(path, n):
    """(taus, cards, sceneId->name, mediaRefs, label), from a doc or from a grab payload."""
    raw = json.load(open(path))
    if "compositions" in raw:
        comps = raw["compositions"]
        if n >= len(comps):
            sys.exit("no composition %d of %d" % (n, len(comps)))
        tl = comps[n]["timeline"]
        return (tl["superTau"]["taus"], tl["cards"]["components"],
                {s["id"]: s.get("name") or "?" for s in raw.get("pinScenes") or []},
                raw["mediaLibrary"]["mediaRefs"], comps[n].get("name", "?"))
    d = raw["data"][0]
    return (d["copiedTaus"],
            [c for c in d.get("copiedComponents", []) if c["type"] == "cardBoundaryComponent"],
            {p["id"]: p.get("name") or "?" for p in d.get("pinTracks", [])},
            [m["mediaRef"] for m in d.get("mediaRefsCopyData", [])], "the clipboard")


def clock(taus):
    """Surviving taus on the play clock, speed-adjusted. Blocked taus keep a zero-width start."""
    rows, at, t = [], {}, 0.0
    for i, tau in enumerate(taus):
        seg = tau["audioSegment"]
        if tau.get("isBlocked"):
            at[tau["id"]] = t
            continue
        dur = seg["duration"] / (seg.get("speed") or 1)
        at[tau["id"]] = t
        rows.append({"i": i, "id": tau["id"], "start": t, "dur": dur, "src": seg.get("offset", 0.0),
                     "srcend": seg.get("offset", 0.0) + seg["duration"],
                     "flat": " ".join(tau["text"]["string"].split())})
        t += dur
    return rows, at, t


def cuts(rows):
    """Visible jump cuts: the source jumped, so the frame jumped."""
    n, prev = 0, None
    for r in rows:
        if prev is not None and abs(r["src"] - prev) > 0.05:
            n += 1
        prev = r["srcend"]
    return n


def states(cards, scenes, at, total):
    """The frame state at each card, in time order.

    A card is a whole layer stack and layer order IS z-order, index 0 on top, so what the viewer
    sees is decided by what sits ABOVE the camera. A layer whose sourceSceneId is not a pinScene
    is the camera itself; a full-frame pinned scene above it hides the speaker, and the same scene
    below it is a background plate. Counting plates as b-roll is how a first run read ES02 at 70%
    coverage against the 34% the FCPXML shows.
    """
    rows, looks = [], {}
    for c in cards:
        tid = c["tauAnchor"]["tauId"]
        if tid not in at:
            continue
        layers = c.get("layers") or []
        cam = next((i for i, L in enumerate(layers)
                    if L.get("sourceSceneId") not in scenes), len(layers))
        cover = set()
        for i, L in enumerate(layers):
            if L.get("sourceSceneId") not in scenes:
                continue
            w = next((f["keyframes"][0]["value"].get("width", 0)
                      for f in (L.get("effects") or [])
                      if f.get("type") == "box" and f.get("keyframes")), 0)
            name = scenes[L["sourceSceneId"]]
            w0, c0 = looks.get(name, (0, 0))
            looks[name] = (max(w0, w), c0 + 1)     # every pinned look, for `plan` to clone
            if i < cam and w >= 0.9:               # only above the camera does it HIDE the speaker
                cover.add(name)
        rows.append({"t": round(at[tid] + c.get("offsetFromAnchor", 0), 2), "cover": cover})
    rows.sort(key=lambda r: r["t"])
    for r, nxt in zip(rows, rows[1:] + [{"t": total}]):
        r["end"] = nxt["t"]
    return rows, looks


def overlays(rows):
    """Each run of covered frame, merged: one entry per b-roll insert the viewer sees."""
    out = []
    for r in rows:
        if not r["cover"]:
            continue
        if r["end"] - r["t"] < 0.05:
            continue
        if out and out[-1]["end"] >= r["t"] - 0.01 and out[-1]["cover"] & r["cover"]:
            out[-1]["end"] = r["end"]
            out[-1]["cover"] |= r["cover"]
        else:
            out.append({"start": r["t"], "end": r["end"], "cover": set(r["cover"])})
    for o in out:
        o["dur"] = round(o["end"] - o["start"], 2)
        o["name"] = " + ".join(sorted(o["cover"]))
    return out


def union(spans):
    m = []
    for a, b in sorted(spans):
        if m and a <= m[-1][1]:
            m[-1][1] = max(m[-1][1], b)
        else:
            m.append([a, b])
    return m


def median(xs):
    xs = sorted(xs)
    return 0.0 if not xs else (xs[len(xs) // 2] if len(xs) % 2 else
                               (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2)


def mmss(s):
    return "%d:%02d" % (int(s) // 60, int(s) % 60)


# ---------------------------------------------------------------- audit

def audit(path, n):
    taus, cards, scenes, _refs, label = load(path, n)
    rows, at, total = clock(taus)
    st, _ = states(cards, scenes, at, total)
    ov = overlays(st)
    changes = sorted({s["t"] for s in st})
    gaps = [b - a for a, b in zip(changes, changes[1:])]
    covered = union([(o["start"], o["end"]) for o in ov])
    cover = sum(b - a for a, b in covered)
    marks = sorted(set(changes) | {o["start"] for o in ov} | {o["end"] for o in ov} | {0.0, total})
    dead = [(a, b) for a, b in zip(marks, marks[1:])
            if b - a > GATE_DEAD and not any(x <= a and b <= y for x, y in covered)]

    nc = cuts(rows)
    print("%s  %s  %d surviving taus, %d ignored"
          % (label, mmss(total), len(rows), len(taus) - len(rows)))
    print("  jump cuts       %3d      one every %.1fs" % (nc, total / max(1, nc)))
    print("  state changes   %3d      median gap %.1fs (gate %.0f)"
          % (len(changes), median(gaps), GATE_MEDIAN))
    print("  visual overlays %3d      %.0fs full-frame = %.0f%% of runtime (gate %.0f-%.0f%%)"
          % (len(ov), cover, 100 * cover / total, 100 * GATE_COVER[0], 100 * GATE_COVER[1]))
    print("  median overlay  %.1fs    shortest %.1fs  longest %.1fs"
          % (median([o["dur"] for o in ov]) if ov else 0,
             min([o["dur"] for o in ov], default=0), max([o["dur"] for o in ov], default=0)))

    fails = []
    if median(gaps) > GATE_MEDIAN:
        fails.append("median gap %.1fs over %.0fs" % (median(gaps), GATE_MEDIAN))
    if not GATE_COVER[0] <= cover / total <= GATE_COVER[1]:
        fails.append("coverage %.0f%% outside %.0f-%.0f%%"
                     % (100 * cover / total, 100 * GATE_COVER[0], 100 * GATE_COVER[1]))
    if dead:
        print("\n  the frame sits still (over %.0fs with nothing changing):" % GATE_DEAD)
        for a, b in dead:
            line = next((r["flat"] for r in rows if r["start"] >= a), "")
            print("    %s -> %s  (%.0fs)  %s" % (mmss(a), mmss(b), b - a, line[:70]))
        fails.append("%d dead stretches" % len(dead))
    print("\n%s" % ("PASS" if not fails else "FAIL: " + "; ".join(fails)))
    return 1 if fails else 0


# ---------------------------------------------------------------- plan

def extend(rows, start, want):
    """Run a clip from `start` over whole taus until it has covered about `want` seconds.

    A pin's visible span is set by its two cards, not by `dur`, so a spec with only a `from`
    covers one tau and a 5-second clip flashes for 1.5. The `to` phrase is what gives it a beat.
    """
    it = [r for r in rows if r["start"] >= start - 0.01]
    span = 0.0
    for k, r in enumerate(it):
        span += r["dur"]
        if span >= want or k == len(it) - 1:
            return " ".join(r["flat"].split()[-6:]), span
    return " ".join(it[0]["flat"].split()[-6:]), span


def clause_runs(rows):
    """Three or more short clauses in a row: the place a micro-cut run belongs."""
    runs, cur = [], []
    for r in rows:
        if r["dur"] <= LIST_MAX and r["flat"].rstrip().endswith((",", ";")):
            cur.append(r)
        else:
            if len(cur) >= 3:
                runs.append(cur)
            cur = []
    if len(cur) >= 3:
        runs.append(cur)
    return runs


def plan(path, n, out):
    taus, cards, scenes, refs, _label = load(path, n)
    rows, at, total = clock(taus)
    st, looks = states(cards, scenes, at, total)
    ov = overlays(st)
    held = union([(o["start"], o["end"]) for o in ov])
    # `pins.py` keys its layout catalogue by the name of a clip ALREADY placed, so the look this
    # plan can ask for is one the video already uses. Take the full-frame look off a b-roll run
    # rather than off the widest layer: the background plate is also 1.0 wide and sits above the
    # camera on a blocked tau's card, which is how a first run proposed `image-1` as the layout.
    names = [n for o in ov for n in o["cover"]]
    full = (next((n for n in names if TC.search(n)), None)
            or max(set(names), key=names.count, default=None))
    inset = max((k for k, (w, c) in looks.items() if 0.6 <= w < 0.9),
                key=lambda k: looks[k][1], default=full)

    # media whose house name carries the timecode it was rendered for
    seeds = []
    for r in [r for r in refs if r.get("displayName")]:
        m = TC.search(r["displayName"])
        if m:
            seeds.append((int(m.group(1)) * 60 + int(m.group(2)), r["displayName"]))
    used = set()
    for o in ov:
        used |= o["cover"]

    slots, inrun = [], set()
    for run in clause_runs(rows):
        for r in run:
            inrun.add(r["i"])
            slots.append((r["start"], "list", r["dur"], r["flat"]))
    for r in rows:
        if r["i"] in inrun:
            continue
        f = r["flat"]
        if SHOW.search(f):
            slots.append((r["start"], "screen", r["dur"], f))
        elif CTA.search(f):
            slots.append((r["start"], "cta", r["dur"], f))
        elif COUNT.search(f):
            slots.append((r["start"], "motion", r["dur"], f))
    slots.sort()

    # A dead stretch with no trigger still needs the camera to move. A stretch that already has a
    # slot does not: a zoom under a clip that covers the frame is a move nobody can see.
    taken = {s[0] for s in slots}
    changes = sorted({x["t"] for x in st} | taken)
    prev = 0.0
    for c in changes + [total]:
        if c - prev > GATE_DEAD:
            # Prefer a jump cut. An announcement inside the stretch is words the video does
            # not need, so ignoring it breaks the still frame and shortens the video at once;
            # a zoom only breaks the still frame. Fall back to the zoom when there is none.
            inside = [x for x in rows if prev <= x["start"] < c and x["start"] not in taken]
            cut = next((x for x in inside
                        if x["dur"] <= ANNOUNCE_MAX and ANNOUNCE.match(x["flat"])), None)
            if cut:
                slots.append((cut["start"], "jumpcut", cut["dur"], cut["flat"]))
                taken.add(cut["start"])
            else:
                # Four words minimum: a pin resolves on its `from` phrase, and a one-word
                # anchor matches somewhere else in the take or matches nothing.
                r = next((x for x in inside if x["start"] >= prev + GATE_DEAD * 0.6
                          and len(x["flat"].split()) >= 4), None)
                if r:
                    slots.append((r["start"], "zoom", r["dur"], r["flat"]))
                    taken.add(r["start"])
        prev = c
    slots.sort()

    pins, phrases, ladder, opens = [], [], LADDER[:], 0
    print("%-8s %-7s %-6s %s" % ("at", "trigger", "media", "line"))
    for start, kind, dur, line in slots:
        covered = any(a <= start < b for a, b in held)
        seed = min((s for s in seeds if s[1] not in used), key=lambda s: abs(s[0] - start),
                   default=None) if kind in ("motion", "screen") else None
        if seed and abs(seed[0] - start) > 25:
            seed = None
        print("%-8s %-7s %-6s %s%s"
              % (mmss(start), kind, "cut" if kind == "jumpcut" else "zoom" if kind == "zoom" else
                 "yes" if seed else ("held" if covered else "OPEN"),
                 line[:64], "   <- " + seed[1] if seed else ""))
        frm = " ".join(line.split()[:8])
        if kind == "jumpcut":
            # A jump cut is a cut-list needle, not a pin: it goes through resolve.py and
            # `dscript apply`, which is a different paste from `--pins`.
            phrases.append({"text": line, "pass": 2,
                            "reason": "announcement; the jump cut that breaks a still frame"})
            continue
        if kind == "zoom":
            pins.append({"zoom": ladder[0], "from": frm, "why": "the frame sat still"})
            ladder = ladder[1:] + ladder[:1]
            continue
        if covered:
            continue
        p = {"media": seed[1] if seed else "FILL ME", "in": 0,
             "from": frm, "layout": inset if kind == "screen" else full, "why": kind}
        if kind == "list":
            p["dur"] = round(dur, 1)        # a micro-cut run holds exactly its clause
        else:
            to, span = extend(rows, start, SPAN)
            p["to"], p["dur"] = to, round(span, 1)
        if seed:
            used.add(seed[1])
        else:
            opens += 1
        pins.append(p)

    print("\n%d slots: %d clips bound by name, %d OPEN, %d zoom steps, %d jump cuts"
          % (len(slots), len(pins) - opens - sum(1 for p in pins if "zoom" in p), opens,
             sum(1 for p in pins if "zoom" in p), len(phrases)))
    if full is None:
        print("no clip has ever been placed here, so there is no look to clone: drag one in, "
              "copy again, then fill every layout by hand (pins.py refuses otherwise)")
    if out:
        json.dump(pins, open(out, "w"), indent=1)
        print("wrote %s - replace every FILL ME, then: pins.py resolve %s" % (out, out))
        if phrases:
            side = out.replace(".json", "") + ".phrases.json"
            json.dump(phrases, open(side, "w"), indent=1)
            print("wrote %s - the jump cuts, through resolve.py and `dscript apply`" % side)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, path = sys.argv[1], sys.argv[2]
    argv = sys.argv[3:]
    n = int(argv[argv.index("--comp") + 1]) if "--comp" in argv else 0
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    if cmd == "audit":
        sys.exit(audit(path, n))
    if cmd == "plan":
        sys.exit(plan(path, n, out))
    sys.exit("unknown command %r" % cmd)
