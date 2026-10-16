#!/usr/bin/env python3
"""Prove a placement against a real grab. usage: test_pins.py <grab.json> [...]

Derives its own spec from whatever the payload contains - any project, any
layout library - so a new video is a new test case for free.
"""
import copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recut2, pins as P


def check(path):
    before = json.load(open(path))
    if "data" not in before:          # a .meta.json sidecar swept up by a glob
        return True
    b = before["data"][0]
    cat = P.layouts(b)
    if not cat:
        print("SKIP %s - no layout to clone" % os.path.basename(path)); return True
    look = sorted(cat)[0]
    want = cat[look]

    toks = P.live_tokens(b["copiedTaus"])
    mid = len(toks) // 2
    phrase = " ".join(t[3] for t in toks[mid:mid + 9])
    media = next(m["mediaRef"] for m in b["mediaRefsCopyData"] if (m["mediaRef"].get("video") or {}))
    spec = {"media": media["displayName"], "from": phrase, "in": 0, "dur": 4.0,
            "layout": look, "nth": 1}

    n_pin0 = len(b["pinTracks"])
    out, new, _, _ = recut2.build_ignore([], path)
    out = P.add_pins(out, new, [spec])
    d = out["data"][0]
    order = {t["id"]: i for i, t in enumerate(new)}
    pin = d["pinTracks"][n_pin0]

    sc = next(c for c in d["copiedComponents"]
              if c["type"] == "sceneComponent" and c["sceneId"] == pin["id"])
    cards = {c["id"]: c for c in d["copiedComponents"] if c["type"] == "cardBoundaryComponent"}
    endc = cards[sc["endAnchor"]["cardBoundaryId"]]
    startc = next(c for c in cards.values()
                  if any(l.get("sourceSceneId") == pin["id"] for l in c.get("layers") or []))

    fails = []
    if P.key_of(order, endc["tauAnchor"]) <= P.key_of(order, sc["tauAnchor"]):
        fails.append("closing card is not after the opening one")
    if any(l.get("sourceSceneId") == pin["id"] for l in endc.get("layers") or []):
        fails.append("closing card still carries the clip - it would run to the end")
    lay = next(l for l in startc["layers"] if l.get("sourceSceneId") == pin["id"])
    if P.geometry(lay) != want["geo"]:
        fails.append("clip geometry drifted from the cloned layout")
    cam = P.base_layer(d, startc["layers"])
    if want["cam"] is not None and P.geometry(cam) != want["cam_geo"]:
        fails.append("camera geometry drifted from the cloned layout")

    known = {p["id"] for p in d["pinTracks"]} | {
        l.get("sourceSceneId") for c in cards.values() for l in (c.get("layers") or [])
        if l.get("sourceSceneId") not in {p["id"] for p in d["pinTracks"]}}
    for c in cards.values():
        for l in (c.get("layers") or []):
            if l.get("sourceSceneId") not in known:
                fails.append("a layer points at a scene that does not exist"); break
    ids = [c["id"] for c in d["copiedComponents"]] + [p["id"] for p in d["pinTracks"]]
    if len(ids) != len(set(ids)):
        fails.append("duplicate ids")
    ref = before["data"][0]["pinTracks"][0]
    if set(pin.keys()) != set(ref.keys()):
        fails.append("pinTrack key set differs from Descript's own")
    json.loads(json.dumps(out))

    name = os.path.basename(path)
    if fails:
        print("FAIL %s\n     - %s" % (name, "\n     - ".join(fails))); return False
    print("PASS %s  layout %r on %d taus" % (name, look[:34], len(new)))
    return True


if __name__ == "__main__":
    args = sys.argv[1:] or [os.path.expanduser("~/.descript-clip/current.json")]
    sys.exit(0 if all([check(a) for a in args]) else 1)
