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
    sequence.py balance <doc.json> [--comp N]                where the dressing sits, and the sound
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

# The gate, measured on two finished edits. references/sequencing.md carries the table.
GATE_DEAD = 12.0        # seconds the frame may sit unchanged
GATE_MEDIAN = 7.0       # median seconds between state changes
GATE_COVER = (0.20, 0.50)   # share of runtime under a visual overlay

# The balance gate. `audit` reads averages, and an average hides where the dressing sits: EC49
# passed within a tenth of a second on the median and still ran four whole minutes with nothing
# on screen and no sound. references/balance.md carries the teardown.
BIN = 60.0              # the window balance is read in. A minute is what a viewer feels
NAKED_DRESS = 6.0       # seconds of clip, graphic or title a minute must carry
NAKED_SFX = 1           # ...unless it carries more sounds than this
GATE_SFX_QUIET = 45.0   # longest stretch with no sound at all. sound-layout.md measures a body
                        # placing one every 7.5-11s, and one reference video every 60s. The MEDIAN
                        # gap is not the gate: EC49's median is 7.1s and passes, while 79% of its
                        # runtime carries no sound, because the sounds arrive in two bursts.
GATE_ARRIVAL_SFX = 0.80 # share of visual arrivals that carry a sound within PAIR seconds
PAIR = 0.6              # how close a sound has to land to count as being on the arrival
GATE_FIFTH = 0.08       # least share of the dressing any fifth of the runtime may hold
CHROME_W = 0.15         # narrower than this, above the camera, is a HUD rather than a shot

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


SPAN = {}   # tauId -> (seconds on the play clock, characters): a card anchored MID-tau needs both


def clock(taus):
    """Surviving taus on the play clock, speed-adjusted. Blocked taus keep a zero-width start."""
    rows, at, t = [], {}, 0.0
    for i, tau in enumerate(taus):
        seg = tau.get("audioSegment")
        if seg is None:
            # A tau with no audio (a title card, an empty paragraph): zero-width, like a blocked one.
            at[tau["id"]] = t
            continue
        if tau.get("isBlocked"):
            at[tau["id"]] = t
            continue
        dur = seg["duration"] / (seg.get("speed") or 1)
        at[tau["id"]] = t
        SPAN[tau["id"]] = (dur, len(tau["text"]["string"]) or 1)
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
        # a split card anchors at a character offset inside its tau: `location` places it
        dur, n = SPAN.get(tid, (0.0, 1))
        mid = dur * (c["tauAnchor"].get("location") or 0) / n
        rows.append({"t": round(at[tid] + mid + c.get("offsetFromAnchor", 0), 2), "cover": cover})
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
        # A layer over the stretch covers a `screen` slot and never a `motion` one: a motion clip
        # is keyed and cuts OVER the plate. See references/sequencing.md.
        covered = any(a <= start < b for a, b in held) and kind != "motion"
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
        schema.dump(out, "pins", pins, indent=1)
        print("wrote %s - replace every FILL ME, then: pins.py resolve %s" % (out, out))
        if phrases:
            side = out.replace(".json", "") + ".phrases.json"
            schema.dump(side, "phrases", phrases, indent=1)
            print("wrote %s - the jump cuts, through resolve.py and `dscript apply`" % side)
    return 0


# ---------------------------------------------------------------- balance

def dressing(path, n):
    """Every pin on the timeline, as (start, end, lane), plus the runtime.

    FIVE LANES, read off the document rather than off a naming convention where one exists.
    A pin whose scene carries no media at all is a `title`: text is drawn on the card, not
    sourced. A pin whose media has audio and no picture is a `sound`. Everything else is a clip,
    and the house name splits it: a rendered graphic carries the timecode bracket it was rendered
    for (`36 [14-19] Sprint Comes Off`), footage does not. That bracket is already this skill's
    naming rule, so nothing new is being assumed here.

    THE FIFTH LANE IS `chrome`, AND IT IS THE ONE THAT MAKES THE COUNT HONEST. A background
    plate and a progress bar are pinned scenes like any other, and a first run of this counted
    them: EC49 came back at 199% title and 83% footage, because a grid plate ran under all
    eighteen minutes and a progress HUD sat on 129 cards. So a scene earns a lane only where it
    sits ABOVE the camera on some card - below it is a plate - and only where it is wider than
    CHROME_W, which is what separates a lower third from a corner dot. Neither is a state change;
    the viewer stops seeing both inside ten seconds.

    A pin's visible span is its anchor card to its closing card. A pin with no closing card runs
    to the end of the video, and it is counted that way because that is what the viewer sees.
    """
    raw = json.load(open(path))
    if "compositions" not in raw:
        sys.exit("balance reads a `pnpm descript doc` export: the clipboard payload carries no "
                 "pinScene timelines, so a sound cannot be told from a clip in it")
    tl = raw["compositions"][n]["timeline"]
    refs = {m["id"]: m for m in raw["mediaLibrary"]["mediaRefs"]}
    scenes = {sc["id"]: sc for sc in raw.get("pinScenes") or []}

    # How wide each scene ever draws, above the camera. `states()` reads the same z-order.
    widest = {}
    for c in tl["cards"]["components"]:
        layers = c.get("layers") or []
        cam = next((i for i, L in enumerate(layers)
                    if L.get("sourceSceneId") not in scenes), len(layers))
        for i, L in enumerate(layers):
            sid = L.get("sourceSceneId")
            if sid not in scenes or i >= cam or L.get("isHidden"):
                continue
            w = next((f["keyframes"][0]["value"].get("width", 0)
                      for f in (L.get("effects") or [])
                      if f.get("type") == "box" and f.get("keyframes")), 0)
            widest[sid] = max(widest.get(sid, 0), w)

    lane = {}
    for sid, sc in scenes.items():
        ids = [t["audioSegment"]["mediaRefId"]
               for t in sc["timeline"]["superTau"]["taus"]
               if (t.get("audioSegment") or {}).get("mediaRefId")]
        m = refs.get(ids[0]) if ids else None
        if m and not m.get("video") and not m.get("image"):
            lane[sid] = "sound"
        elif widest.get(sid, 0) < CHROME_W:
            lane[sid] = "chrome"
        elif not ids:
            lane[sid] = "title"
        else:
            lane[sid] = "graphic" if TC.search(sc.get("name") or "") else "footage"

    taus = tl["superTau"]["taus"]
    _rows, at, total = clock(taus)
    card_at = {c["id"]: at[c["tauAnchor"]["tauId"]] + c.get("offsetFromAnchor", 0)
               for c in tl["cards"]["components"] if c["tauAnchor"]["tauId"] in at}
    out = []
    for p in tl["pins"]["components"]:
        tid = p["tauAnchor"]["tauId"]
        if p.get("isBlocked") or tid not in at:
            continue
        kind = lane.get(p.get("sceneId"), "chrome")
        if kind == "chrome":
            continue
        start = at[tid] + p.get("offsetFromAnchor", 0)
        end = card_at.get(((p.get("endAnchor") or {}).get("cardBoundaryId")), total)
        out.append((start, max(start, end), kind))
    out.sort()
    return out, sorted(card_at.values()), total


def balance(path, n):
    """Where the dressing sits, minute by minute, and whether every arrival was heard.

    `audit` reads the whole video as one number. This reads the distribution, because that is
    what a viewer meets: an edit whose median gap passes and whose middle four minutes carry
    nothing is not an edit with a rhythm, it is two edits joined.
    """
    pins, cards, total = dressing(path, n)
    sounds = [p for p in pins if p[2] == "sound"]
    arrivals = [p for p in pins if p[2] != "sound"]
    nb = int(total // BIN) + 1
    per = [{"graphic": 0.0, "footage": 0.0, "title": 0.0, "sound": 0, "cards": 0}
           for _ in range(nb)]
    for start, end, kind in pins:
        if kind == "sound":
            per[min(nb - 1, int(start // BIN))]["sound"] += 1
            continue
        x = start
        while x < end:                       # a pin that crosses a minute is split across both
            b = int(x // BIN)
            nxt = min(end, (b + 1) * BIN)
            if b < nb:
                per[b][kind] += nxt - x
            x = nxt
    for c in cards:
        per[min(nb - 1, int(c // BIN))]["cards"] += 1

    print("min   graphic footage  title  sound cards")
    naked = []
    for i, r in enumerate(per):
        dress = r["graphic"] + r["footage"] + r["title"]
        window = min(BIN, total - i * BIN)
        bare = window > BIN / 2 and dress < NAKED_DRESS and r["sound"] <= NAKED_SFX
        if bare:
            naked.append(i)
        print("%2d-%-2d %6.1fs %6.1fs %6.1fs %5d %5d   %s"
              % (i, i + 1, r["graphic"], r["footage"], r["title"], r["sound"], r["cards"],
                 "NAKED" if bare else ("thin" if dress < 2 * NAKED_DRESS else "")))

    tot = {k: sum(r[k] for r in per) for k in ("graphic", "footage", "title", "sound")}
    dress_total = tot["graphic"] + tot["footage"] + tot["title"]
    edges = [0.0] + [x[0] for x in sounds] + [total]
    quiet = [(a, b) for a, b in zip(edges, edges[1:]) if b - a > GATE_SFX_QUIET]
    gaps = [b[0] - a[0] for a, b in zip(sounds, sounds[1:])]
    heard = sum(1 for a in arrivals if any(abs(s[0] - a[0]) <= PAIR for s in sounds))
    share = heard / len(arrivals) if arrivals else 1.0
    fifth = [0.0] * 5
    for start, end, kind in pins:
        if kind == "sound":
            continue
        x = start
        while x < end:
            f = min(4, int(x / (total / 5)))
            nxt = min(end, (f + 1) * total / 5)
            fifth[f] += nxt - x
            x = nxt
    worst = min(fifth) / dress_total if dress_total else 0.0

    print()
    print("  graphic %5.0fs %3.0f%%   footage %5.0fs %3.0f%%   title %5.0fs %3.0f%%"
          % (tot["graphic"], 100 * tot["graphic"] / total, tot["footage"],
             100 * tot["footage"] / total, tot["title"], 100 * tot["title"] / total))
    print("  sounds %d, median gap %.1fs, %.0f%% of the runtime carries none   "
          "arrivals heard %d/%d = %.0f%% (gate %.0f%%)"
          % (len(sounds), median(gaps), 100 * sum(b - a for a, b in quiet) / total,
             heard, len(arrivals), 100 * share, 100 * GATE_ARRIVAL_SFX))
    print("  dressing by fifth: %s   thinnest %.0f%% (gate %.0f%%)"
          % (" ".join("%.0f%%" % (100 * f / dress_total if dress_total else 0) for f in fifth),
             100 * worst, 100 * GATE_FIFTH))

    fails = []
    if naked:
        fails.append("%d naked minute%s (%s)"
                     % (len(naked), "" if len(naked) == 1 else "s",
                        ", ".join("%d:00" % i for i in naked)))
    if quiet:
        print("\n  no sound at all (over %.0fs):" % GATE_SFX_QUIET)
        for a, b in quiet:
            print("    %s -> %s  (%.0fs)" % (mmss(a), mmss(b), b - a))
        fails.append("%d silent stretches, longest %.0fs"
                     % (len(quiet), max(b - a for a, b in quiet)))
    if share < GATE_ARRIVAL_SFX:
        fails.append("%.0f%% of arrivals carry a sound, under %.0f%%"
                     % (100 * share, 100 * GATE_ARRIVAL_SFX))
    if worst < GATE_FIFTH:
        fails.append("the thinnest fifth holds %.0f%% of the dressing" % (100 * worst))
    print("\n%s" % ("PASS" if not fails else "FAIL: " + "; ".join(fails)))
    return 1 if fails else 0


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
    if cmd == "balance":
        sys.exit(balance(path, n))
    sys.exit("unknown command %r" % cmd)
