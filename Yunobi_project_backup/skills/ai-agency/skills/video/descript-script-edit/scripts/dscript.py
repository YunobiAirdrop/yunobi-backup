#!/usr/bin/env python3
"""dscript - drive a Descript edit through the rich clipboard.

    dscript grab [label]           read the clipboard, archive it, print the state
    dscript words                  indexed transcript of the last grab, for the cut list
    dscript apply cuts.json [opts] rebuild and load the clipboard
                                   (--styles/--typos/--markers/--pins/--delete)
    dscript pins pins.json         place b-roll and zooms only; no cut, no alignment
    dscript history                every payload seen or written, newest first
    dscript restore <id>           put an archived payload back on the clipboard
    dscript check                  read the clipboard back and diff it against the last apply

The user does the two ends: Cmd+A Cmd+C before `grab`, Cmd+A Cmd+V after `apply`.
Nothing here needs AI credits or a browser session.
"""
import json, os, re, sys, datetime, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dclip, recut2, pins as pinmod

HOME = os.path.expanduser("~/.descript-clip")
HIST = os.path.join(HOME, "history")
os.makedirs(HIST, exist_ok=True)

def _stat(p):
    d = p["data"][0]
    taus = d["copiedTaus"]
    seg = [t for t in taus if t.get("audioSegment")]
    plays = sum(t["audioSegment"]["duration"] for t in seg if not t.get("isBlocked"))
    total = sum(t["audioSegment"]["duration"] for t in seg)
    text = "".join(t["text"]["string"] for t in taus)
    return {"project": d.get("projectId"), "track": (d.get("sourceTrack") or {}).get("id"),
            "taus": len(taus), "blocked": sum(1 for t in taus if t.get("isBlocked")),
            "attributes": sum(len(t["text"].get("attributes") or []) for t in taus),
            "words": len(re.findall(r"\S+", text)), "total": round(total, 2),
            "plays": round(plays, 2)}

def _show(s, head=""):
    print("%s%s | track %s" % (head, s["project"], s["track"]))
    print("  taus %d (%d blocked) | words %d | attributes %d | %.1fs total, plays %.1fs (%d:%02d)"
          % (s["taus"], s["blocked"], s["words"], s["attributes"], s["total"],
             s["plays"], s["plays"] // 60, s["plays"] % 60))

def _archive(p, kind, label=""):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = "%s-%s%s" % (ts, kind, ("-" + label) if label else "")
    path = os.path.join(HIST, name + ".json")
    json.dump(p, open(path, "w"))
    s = _stat(p); s["kind"] = kind; s["label"] = label; s["at"] = ts
    json.dump(s, open(os.path.join(HIST, name + ".meta.json"), "w"), indent=1)
    return name

def grab(label=""):
    p, _ = dclip.decode()
    name = _archive(p, "grab", label)
    shutil.copy(os.path.join(HIST, name + ".json"), os.path.join(HOME, "current.json"))
    _show(_stat(p), "GRABBED  ")
    print("  archived as %s" % name)

def words():
    p = json.load(open(os.path.join(HOME, "current.json")))
    text = "".join(t["text"]["string"] for t in p["data"][0]["copiedTaus"])
    out, i = [], 0
    for para in text.split("\n"):
        tk = re.findall(r"\S+", para)
        if not tk: continue
        out.append("[%d] %s" % (i, " ".join(tk))); i += len(tk)
    path = os.path.join(HOME, "words.txt")
    open(path, "w").write("\n\n".join(out))
    print("\n\n".join(out))
    print("\n-- %d words, %d paragraphs -> %s" % (i, len(out), path))

def apply(cuts_path, styles=None, typos=None, markers=None, pins=None, delete=False):
    src = os.path.join(HOME, "current.json")
    cuts = json.load(open(cuts_path))
    fn = recut2.build if delete else recut2.build_ignore
    out, new, toks, _ = fn(cuts, src, typos=json.load(open(typos)) if typos else None)
    if styles:
        out = recut2.apply_styles(new, out, json.load(open(styles)))
    if markers:
        out = recut2.add_markers(out, new, json.load(open(markers)))
    if pins:
        out = pinmod.add_pins(out, new, json.load(open(pins)))
    for t in new:                       # a range must resolve to the phrase it was written for
        for a in (t["text"].get("attributes") or []):
            r = a["range"]
            if r["location"] + r["length"] > len(t["text"]["string"]):
                sys.exit("style range runs past its TAU - refusing to write the clipboard")
    kept = "".join(t["text"]["string"] for t in new if not t.get("isBlocked"))
    open(os.path.join(HOME, "preview.txt"), "w").write(kept)   # read it as prose before pasting
    dclip.write(out, out["text"][0])
    back, _ = dclip.decode()
    if json.dumps(back, sort_keys=True) != json.dumps(out, sort_keys=True):
        sys.exit("clipboard did not round-trip - do not paste")
    name = _archive(out, "apply")
    json.dump(out, open(os.path.join(HOME, "last_apply.json"), "w"))
    _show(_stat(out), "ON CLIPBOARD  ")
    print("  archived as %s" % name)
    print("  surviving script -> %s (read it as prose; an off-by-N cut list looks fine here)"
          % os.path.join(HOME, "preview.txt"))
    print("  -> Cmd+A, Cmd+V in Descript. Do not copy anything else first.")

def place(pins_path):
    """Pins with no cut list.

    The rebuild needs a word alignment; placing a clip does not. A composition
    that is already cut, or whose media carries no alignment, can still take
    b-roll this way.
    """
    p = json.load(open(os.path.join(HOME, "current.json")))
    out = pinmod.add_pins(p, p["data"][0]["copiedTaus"], json.load(open(pins_path)))
    dclip.write(out, out["text"][0] if out.get("text") else "")
    back, _ = dclip.decode()
    if json.dumps(back, sort_keys=True) != json.dumps(out, sort_keys=True):
        sys.exit("clipboard did not round-trip - do not paste")
    name = _archive(out, "pins")
    json.dump(out, open(os.path.join(HOME, "last_apply.json"), "w"))
    _show(_stat(out), "ON CLIPBOARD  ")
    print("  archived as %s" % name)
    print("  -> Cmd+A, Cmd+V in Descript. Do not copy anything else first.")


def history(n=20):
    rows = sorted((f for f in os.listdir(HIST) if f.endswith(".meta.json")), reverse=True)[:n]
    for f in rows:
        m = json.load(open(os.path.join(HIST, f)))
        print("%-34s %-6s taus %3d (%2d blk) words %4d plays %6.1fs  %s"
              % (f[:-10], m["kind"], m["taus"], m["blocked"], m["words"], m["plays"],
                 m.get("label", "")))
    print("\n%d archived in %s" % (len(rows), HIST))

def restore(name):
    p = json.load(open(os.path.join(HIST, name + ".json")))
    dclip.write(p, p["text"][0] if p.get("text") else "")
    _show(_stat(p), "RESTORED TO CLIPBOARD  ")
    print("  -> Cmd+A, Cmd+V to put this state back.")

def check():
    want = json.load(open(os.path.join(HOME, "last_apply.json")))
    got, _ = dclip.decode()
    a, b = _stat(want), _stat(got)
    same = json.dumps(want, sort_keys=True) == json.dumps(got, sort_keys=True)
    print("identical to last apply:", same)
    if not same:
        for k in a:
            if a[k] != b[k]: print("  %-10s applied %-12s clipboard %s" % (k, a[k], b[k]))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    c = a[0]
    if c == "grab": grab(a[1] if len(a) > 1 else "")
    elif c == "words": words()
    elif c == "apply":
        opt = {"styles": None, "typos": None, "markers": None, "pins": None, "delete": False}
        rest = a[2:]
        for i, x in enumerate(rest):
            if x == "--styles": opt["styles"] = rest[i+1]
            elif x == "--typos": opt["typos"] = rest[i+1]
            elif x == "--markers": opt["markers"] = rest[i+1]
            elif x == "--pins": opt["pins"] = rest[i+1]
            elif x == "--delete": opt["delete"] = True
        apply(a[1], **opt)
    elif c == "pins": place(a[1])
    elif c == "history": history(int(a[1]) if len(a) > 1 else 20)
    elif c == "restore": restore(a[1])
    elif c == "check": check()
    else: sys.exit(__doc__)
