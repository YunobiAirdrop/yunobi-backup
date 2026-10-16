#!/usr/bin/env python3
"""Cut AND reorder a Descript script in one paste.

`recut2.build_ignore` can only emit the take in the order it was spoken, so a
video recorded intro-twice / outro-twice keeps its retakes where they landed.
This takes an ORDER: an ordered list of token spans that must tile the whole
script exactly once. Cuts still ship as Ignore; a moved span carries its own
ignored attempts with it.

    order.json  [[0,166],[461,641],[287,320],[166,287],[320,461],[641,5970]]

usage: arrange.py cuts.json order.json [--typos t.json] [--styles s.json]
                     [--markers m.json] [--pins p.json] [--write]
"""
import json, os, re, sys, copy, uuid, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recut2, dclip

HOME = os.path.expanduser("~/.descript-clip")

def main():
    cuts = json.load(open(sys.argv[1]))
    order = json.load(open(sys.argv[2]))
    typos = json.load(open(sys.argv[sys.argv.index("--typos") + 1])) if "--typos" in sys.argv else {}

    p, als = recut2.load(os.path.join(HOME, "current.json"))
    taus = p["data"][0]["copiedTaus"]
    toks = recut2.copy_tokens(taus)
    t2a = recut2.map_to_alignment(toks, als, taus)
    real = [i for i, t in enumerate(toks) if recut2.norm(t[3])]
    agree = sum(1 for i in real if i in t2a and recut2.norm(toks[i][3]) == recut2.norm(t2a[i]["word"]))
    if agree < len(real) - 4:
        sys.exit("mapping unsafe: only %d/%d tokens agree" % (agree, len(real)))
    print("mapping: %d/%d tokens agree on the word" % (agree, len(real)))

    n = len(toks)
    cuts = list(cuts) + [{"start": i, "end": i + 1, "pass": 1, "reason": "filler"}
                         for i, t in enumerate(toks) if recut2.is_filler(t[3])]
    cut = {x for c in cuts for x in range(c["start"], c["end"])}
    # An Ignore already in the composition must SURVIVE a second pass. Building
    # `blocked` from the new cut list alone un-ignores every earlier cut: on a
    # take already cut to 25:30, an EMPTY cut list rebuilt to 34:41 and handed
    # back nine minutes of struck-through restarts (2026-08-25).
    was = [taus[t[0]].get("isBlocked", False) for t in toks]
    blocked = [was[i] or i in cut for i in range(n)]

    flat = sorted(order, key=lambda s: s[0])
    if [x for s in flat for x in s] != [x for i, s in enumerate(flat)
                                        for x in ([0, s[1]] if i == 0 else [flat[i-1][1], s[1]])] \
       or flat[0][0] != 0 or flat[-1][1] != n:
        sys.exit("the order does not tile [0,%d) exactly once: %s" % (n, flat))

    # boundaries: a blocked-flag change, a source TAU change, or a span edge
    edge = {0, n} | {s[0] for s in order} | {s[1] for s in order}
    for i in range(1, n):
        if blocked[i] != blocked[i - 1] or toks[i][0] != toks[i - 1][0]:
            edge.add(i)
    marks = sorted(edge)

    segs = []                       # in SPOKEN order, so the durations stay honest
    for a, b in zip(marks, marks[1:]):
        ti = toks[a][0]
        src = taus[ti]["text"]["string"]
        first = a == 0 or toks[a - 1][0] != ti
        last = b >= n or toks[b][0] != ti
        c0 = 0 if first else toks[a][1]
        c1 = len(src) if last else toks[b][1]
        ra, rb = recut2.real_at(t2a, a, n), recut2.real_at(t2a, b, n)
        t0 = t2a[ra]["startTime"] if ra in t2a else taus[ti]["audioSegment"]["offset"]
        t1 = (t2a[rb]["startTime"] if not last and rb < n
              else taus[ti]["audioSegment"]["offset"] + taus[ti]["audioSegment"]["duration"])
        seg = taus[ti]["audioSegment"]
        segs.append({"a": a, "b": b, "id": str(uuid.uuid4()),
                     "text": {"string": src[c0:c1], "attributes": []},
                     "audioSegment": recut2.reseg(seg, t0, max(t1 - t0, 0.01)),
                     "ignoreAlignment": False, "isBlocked": bool(blocked[a])})

    new = []
    for lo, hi in order:
        new += [s for s in segs if s["a"] >= lo and s["b"] <= hi]
    if len(new) != len(segs):
        sys.exit("a span edge fell inside a segment - refusing")

    kept_src = "".join(s["text"]["string"] for s in sorted(segs, key=lambda s: s["a"]))
    if kept_src != "".join(t["text"]["string"] for t in taus):
        sys.exit("the segments do not reconstruct the source text - refusing")

    for s in new:
        s.pop("a"); s.pop("b")
        s["text"]["string"] = re.sub(r"\b(\w{1,3})-(\1\w*)\b", r"\2", s["text"]["string"], flags=re.I)
        for bad, good in typos.items():
            s["text"]["string"] = re.sub(r"\b%s\b" % re.escape(bad), good, s["text"]["string"])

    out = copy.deepcopy(p)
    d = out["data"][0]
    live = [t for t in new if not t["isBlocked"]]
    for c in d.get("copiedComponents", []):     # one card boundary; it opens the video
        if c.get("tauAnchor"):
            c["tauAnchor"] = {"tauId": (live or new)[0]["id"], "location": 0}
    if "--styles" in sys.argv:
        out = recut2.apply_styles(new, out, json.load(open(sys.argv[sys.argv.index("--styles") + 1])))
    if "--markers" in sys.argv:
        out = recut2.add_markers(out, new, json.load(open(sys.argv[sys.argv.index("--markers") + 1])))
    d["copiedTaus"] = new
    if "--pins" in sys.argv:
        import pins as pinmod
        out = pinmod.add_pins(out, new, json.load(open(sys.argv[sys.argv.index("--pins") + 1])))
        d = out["data"][0]
    for t in new:                   # a range must resolve to the phrase it was written for
        for a in (t["text"].get("attributes") or []):
            r = a["range"]
            if r["location"] + r["length"] > len(t["text"]["string"]):
                sys.exit("style range runs past its TAU - refusing to write the clipboard")
    out["text"] = ["".join(t["text"]["string"] for t in new)]

    plays = sum(t["audioSegment"]["duration"] for t in new if not t["isBlocked"])
    total = sum(t["audioSegment"]["duration"] for t in new)
    open(os.path.join(HOME, "preview.txt"), "w").write(
        "".join(t["text"]["string"] for t in new if not t["isBlocked"]))
    print("%d TAUs (%d ignored) | %.1fs total, plays %.1fs (%d:%02d of %d:%02d)"
          % (len(new), len(new) - len(live), total, plays, plays // 60, plays % 60,
             total // 60, total % 60))
    print("preview -> %s" % os.path.join(HOME, "preview.txt"))

    if "--write" in sys.argv:
        dclip.write(out, out["text"][0])
        back, _ = dclip.decode()
        if json.dumps(back, sort_keys=True) != json.dumps(out, sort_keys=True):
            sys.exit("clipboard did not round-trip - do not paste")
        json.dump(out, open(os.path.join(HOME, "last_apply.json"), "w"))
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        json.dump(out, open(os.path.join(HOME, "history", "%s-arrange.json" % ts), "w"))
        json.dump({"kind": "arrange", "label": "", "at": ts, "taus": len(new),
                   "blocked": len(new) - len(live), "plays": round(plays, 2),
                   "words": len(re.findall(r"\S+", out["text"][0])),
                   "project": d.get("projectId"), "track": (d.get("sourceTrack") or {}).get("id")},
                  open(os.path.join(HOME, "history", "%s-arrange.meta.json" % ts), "w"), indent=1)
        print("ON CLIPBOARD -> Cmd+A, Cmd+V in Descript. Do not copy anything else first.")

if __name__ == "__main__":
    main()
