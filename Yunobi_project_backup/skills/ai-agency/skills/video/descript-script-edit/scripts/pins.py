#!/usr/bin/env python3
"""Place b-roll, overlays and zooms from the script, through the clipboard.

A pin in Descript is three coupled objects, never one:

  pinTrack               the media, and its in/out inside that media
  cardBoundaryComponent  the WHOLE layer stack at one point in the script; the
                         pin is one layer in it, addressed by `sourceSceneId`
  sceneComponent         the span - tauAnchor -> endAnchor{cardBoundaryId}

So an insert is a STATE CHANGE, not an object drop: a card at the in-point that
carries the layer, and a second card at the out-point that does not. Miss the
closing card and the clip runs to the end of the video.

Layer order is z-order, index 0 on top: a background plate sits last, a talking
head over a full-frame clip sits first. Geometry is width-normalised, so a full
16:9 frame is box {width: 1, height: 0.5625}.

Geometry is never invented here. A placement clones the effect stack of a layer
already in the project - shadows, blur, colour and all - so the result matches
whatever layout library the project was built with.

    pins.py catalogue              media, existing pins, and the layouts on offer
    pins.py resolve pins.json      dry run: anchor, media, layout. Writes nothing.
"""
import copy, json, os, re, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from resolve import norm, run, back

HOME = os.path.expanduser("~/.descript-clip")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
GEO = ("box", "contentScale", "contentPosition", "opacity", "cornerRadius")


# ---------------------------------------------------------------- helpers

def fresh_ids(obj):
    """Deep-copy, renaming only the ids the object OWNS.

    A blind uuid rewrite is wrong: `sourceSceneId`, `mediaRefId`, `assetKey` and
    `cardBoundaryId` are references OUT to tracks and media that already exist,
    and renaming them orphans every layer in a cloned card - the clone came back
    with three dead CAMERA layers instead of camera + clip + plate (2026-08-25).
    Only a value under a key literally named "id" is owned, so only those move.
    """
    def walk(o):
        if isinstance(o, dict):
            return {k: (str(uuid.uuid4()) if k == "id" and isinstance(v, str) and UUID_RE.match(v)
                        else walk(v))
                    for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    return walk(copy.deepcopy(obj))


def geometry(layer):
    """The readable geometry of a layer, for the catalogue and for refusals."""
    g = {}
    for f in (layer.get("effects") or []):
        if f.get("type") in GEO and f.get("keyframes"):
            g[f["type"]] = f["keyframes"][0].get("value")
    return g


def live_tokens(taus):
    """(tau_index, char_start, char_end, word) over the SURVIVING script only.

    A pin anchored inside an ignored restart opens on struck-through text, so
    blocked TAUs never take an anchor.
    """
    return [[ti, m.start(), m.end(), m.group(0)]
            for ti, t in enumerate(taus) if not t.get("isBlocked")
            for m in re.finditer(r"\S+", t["text"]["string"])]


def find_span(toks, spec, field):
    """Resolve a phrase to a [start, end) token range, or die naming the fault."""
    nt = [norm(t[3]) for t in toks]
    want = [norm(w) for w in spec[field].split() if norm(w)]
    pre = [norm(w) for w in spec.get("pre", "").split() if norm(w)]
    post = [norm(w) for w in spec.get("post", "").split() if norm(w)]
    hits = [(i, j) for i in range(len(nt))
            for j in [run(nt, i, want)] if j is not None
            and (not pre or back(nt, i, pre))
            and (not post or run(nt, j, post) is not None)]
    if not hits:
        sys.exit("pin %r: no match for %s=%r" % (spec.get("media"), field, spec[field][:80]))
    n = spec.get("nth")
    if n is None:
        if len(hits) > 1:
            sys.exit("pin %r: %d matches for %s=%r - add nth, pre or post"
                     % (spec.get("media"), len(hits), field, spec[field][:80]))
        return hits[0]
    if n > len(hits):
        sys.exit("pin %r: only %d matches, nth=%d" % (spec.get("media"), len(hits), n))
    return hits[n - 1]


def anchor_at(taus, toks, i, end=False):
    """Token index -> {tauId, location}. `end` anchors after the token's last char."""
    ti, c0, c1, _ = toks[i - 1] if end else toks[i]
    return {"tauId": taus[ti]["id"], "location": c1 if end else c0}


def key_of(order, anchor):
    return (order.get(anchor["tauId"], 10 ** 9), anchor["location"])


# ---------------------------------------------------------------- reading

def media_index(d):
    """displayName -> mediaRef, plus the bare stem so an extension is optional."""
    out = {}
    for m in d["mediaRefsCopyData"]:
        r = m["mediaRef"]
        nm = r.get("displayName") or r["id"]
        out[nm] = r
        out.setdefault(os.path.splitext(nm)[0], r)
    return out


def find_media(d, name):
    idx = media_index(d)
    if name in idx:
        return idx[name]
    hits = [k for k in idx if name.lower() in k.lower()]
    uniq = {idx[k]["id"] for k in hits}
    if len(uniq) == 1:
        return idx[hits[0]]
    placed = sorted({(r.get("displayName") or r["id"]) for r in idx.values()})
    sys.exit("media %r %s in this payload.\nThe clipboard only carries media already "
             "ON the timeline. Placeable here:\n  %s"
             % (name, "is ambiguous" if hits else "is not",
                "\n  ".join(placed)))


def base_layer(d, layers):
    """The talking-head layer: the one that is not a pin.

    It points at the composition's own source track, never at a `sequenceTracks`
    id, so matching on sequenceTracks finds nothing and every camera geometry
    reads as absent (2026-08-25).
    """
    pins = {p["id"] for p in d.get("pinTracks", [])}
    return next((l for l in layers if l.get("sourceSceneId") not in pins), None)


def cards_in(d):
    return [c for c in d.get("copiedComponents", []) if c["type"] == "cardBoundaryComponent"]


def layouts(d):
    """Every card that carries a pin layer, keyed by the pin that used it.

    The catalogue is the project's own layout library read back, so a placement
    can only ask for a look that already exists in the video.
    """
    pins = {p["id"]: p["name"] for p in d.get("pinTracks", [])}
    out = {}
    for c in cards_in(d):
        layers = c.get("layers") or []
        for z, l in enumerate(layers):
            sid = l.get("sourceSceneId")
            if sid not in pins:
                continue
            cam = base_layer(d, layers)
            out.setdefault(pins[sid], {
                "card": c, "layer": l, "z": z, "cam": cam,
                "geo": geometry(l), "cam_geo": geometry(cam) if cam else None,
                "stack": [pins.get(x.get("sourceSceneId"), "CAMERA") for x in layers],
            })
    return out


# ---------------------------------------------------------------- writing

def _state_at(cards, order, key):
    """The prevailing layer stack at a script position, and the card it came from."""
    before = [c for c in cards if key_of(order, c["tauAnchor"]) <= key]
    src = max(before, key=lambda c: key_of(order, c["tauAnchor"])) if before else (
        min(cards, key=lambda c: key_of(order, c["tauAnchor"])) if cards else None)
    return src


def _card_from(src, anchor, name=None):
    c = fresh_ids(src)
    c["tauAnchor"] = dict(anchor)
    c.pop("name", None)
    c.pop("layoutType", None)
    if name:
        c["name"] = name
    return c


def _pin_track(template, media, offset, dur, speed):
    p = fresh_ids(template)
    p["name"] = os.path.splitext(media.get("displayName") or media["id"])[0]
    vm = media.get("video") or {}
    if vm:
        p["videoMetadata"] = {"width": vm.get("width"), "height": vm.get("height"),
                              "framerateNumerator": vm.get("framerateNumerator", 30),
                              "framerateDenominator": vm.get("framerateDenominator", 1)}
    taus = p["timeline"]["superTau"]["taus"]
    t = taus[0]
    taus[:] = [t]
    t["text"] = {"string": "", "attributes": []}
    t["audioSegment"] = {"mediaRefId": media["id"], "offset": offset, "duration": dur,
                         "gain": 1, "suppressAutoMerge": False, "speed": speed, "effects": []}
    t["isBlocked"] = False
    return p


def add_pins(payload, new, specs):
    """Place each spec as pinTrack + opening card + closing card + sceneComponent."""
    d = payload["data"][0]
    order = {t["id"]: i for i, t in enumerate(new)}
    toks = live_tokens(new)
    if not toks:
        sys.exit("nothing survives the cut - refusing to place pins")
    cat = layouts(d)
    templates = d.get("pinTracks") or []
    comps = d.setdefault("copiedComponents", [])

    for spec in specs:
        cards = cards_in(d)

        if "zoom" in spec and "media" not in spec:      # a zoom is one card, no span
            a, _ = find_span(toks, spec, "from")
            anchor = anchor_at(new, toks, a)
            src = _state_at(cards, order, key_of(order, anchor))
            card = _card_from(src, anchor, name="Zoom %d%%" % spec["zoom"])
            card["layoutType"] = "camera" if spec["zoom"] == 100 else "zoom"
            cam = base_layer(d, card["layers"])
            if cam is None:
                sys.exit("zoom at %r: no camera layer in the prevailing card" % spec["from"][:60])
            _set_geo(cam, "contentScale", {"x": spec["zoom"] / 100.0, "y": spec["zoom"] / 100.0})
            comps.append(card)
            continue

        if not templates:   # only a MEDIA pin needs a track to clone; a zoom does not
            sys.exit("this payload has no pinTrack to clone from. Place one clip by hand in "
                     "Descript, copy again, then re-run: the clone needs a live example.")
        media = find_media(d, spec["media"])
        look = spec.get("layout")
        if look is None:
            sys.exit("pin %r: no layout. Choose one of: %s"
                     % (spec["media"], ", ".join(sorted(cat)) or "none in this payload"))
        if look not in cat:
            sys.exit("pin %r: layout %r not in this project. Available: %s"
                     % (spec["media"], look, ", ".join(sorted(cat))))
        L = cat[look]

        a, b = find_span(toks, spec, "from")
        start = anchor_at(new, toks, a)
        if "to" in spec:
            _, b2 = find_span(toks, spec, "to")
            end = anchor_at(new, toks, b2, end=True)
        else:
            end = anchor_at(new, toks, b, end=True)
        ks, ke = key_of(order, start), key_of(order, end)
        if ke <= ks:
            sys.exit("pin %r: the out-point is not after the in-point" % spec["media"])

        dur = media.get("video", {}).get("duration") or media.get("audio", {}).get("duration") or 0
        offset = spec.get("in", 0)
        length = spec.get("dur", max(0.0, dur - offset))
        pin = _pin_track(templates[0], media, offset, length, spec.get("speed", 1))
        # Register it BEFORE any layer work: `base_layer` calls anything that is
        # not a known pin the camera, so an unregistered pin gets the camera's
        # geometry and the two swap places (2026-08-25).
        d["pinTracks"].append(pin)

        end_src = _state_at(cards, order, ke)
        end_card = next((c for c in cards if key_of(order, c["tauAnchor"]) == ke), None)
        if end_card is None:
            end_card = _card_from(end_src, end)
            comps.append(end_card)

        start_card = next((c for c in cards if key_of(order, c["tauAnchor"]) == ks), None)
        if start_card is None:
            start_card = _card_from(_state_at(cards, order, ks), start)
            comps.append(start_card)

        layer = fresh_ids(L["layer"])
        layer["sourceSceneId"] = pin["id"]
        for k, v in (spec.get("geo") or {}).items():
            _set_geo(layer, k, v)
        z = spec.get("z", L["z"])
        start_card.setdefault("layers", []).insert(min(z, len(start_card["layers"])), layer)

        if spec.get("cam", True) and L["cam"] is not None:
            # Clone the whole camera layer, not just the geometry keys it happens
            # to carry. Merging keys leaves the previous card's contentScale and
            # contentPosition behind, and the talking head lands in a position
            # that exists in no layout (2026-08-25).
            cam = base_layer(d, start_card["layers"])
            if cam is not None:
                fresh = fresh_ids(L["cam"])
                fresh["sourceSceneId"] = cam["sourceSceneId"]
                start_card["layers"][start_card["layers"].index(cam)] = fresh

        comps.append({"type": "sceneComponent", "id": str(uuid.uuid4()),
                      "offsetFromBaseTime": 0, "offsetFromAnchor": 0,
                      "tauAnchor": dict(start), "sortTiebreaker": 2.5, "isBlocked": False,
                      "baseType": "trackComponent", "shortName": "component",
                      "sceneId": pin["id"],
                      "endAnchor": {"type": "cardBoundary", "cardBoundaryId": end_card["id"]}})
        for m in d["mediaRefsCopyData"]:
            if m["mediaRef"]["id"] == media["id"]:
                m.setdefault("ranges", []).append({"offset": offset, "duration": length})
    return payload


def _set_geo(layer, kind, value):
    for f in (layer.get("effects") or []):
        if f.get("type") == kind:
            f["keyframes"] = [{"offset": 0, "value": value}]
            f["isDisabled"] = False
            return
    layer.setdefault("effects", []).append(
        {"id": str(uuid.uuid4()), "type": kind,
         "keyframes": [{"offset": 0, "value": value}], "isDisabled": False})


# ---------------------------------------------------------------- cli

def _load():
    return json.load(open(os.path.join(HOME, "current.json")))


def catalogue():
    d = _load()["data"][0]
    print("MEDIA placeable from this clipboard (already on the timeline):")
    for r in sorted({m["mediaRef"]["id"]: m["mediaRef"] for m in d["mediaRefsCopyData"]}.values(),
                    key=lambda r: str(r.get("displayName"))):
        v, au = r.get("video") or {}, r.get("audio") or {}
        kind = "video" if v else ("audio" if au else "still")
        print("  %-46s %-6s %ss" % (str(r.get("displayName"))[:46], kind,
                                    round(v.get("duration") or au.get("duration") or 0, 2)))
    cat = layouts(d)
    print("\nLAYOUTS in this project (clone one by name):")
    for k, v in sorted(cat.items()):
        print("  %-40s z%d  stack %s" % (k[:40], v["z"], " / ".join(v["stack"])))
        print("       clip %s" % json.dumps(v["geo"]))
        if v["cam_geo"]:
            print("       cam  %s" % json.dumps(v["cam_geo"]))
    if not cat:
        print("  none - no card in this payload carries a pin layer")


def dry_run(path):
    p = _load()
    d = p["data"][0]
    new = d["copiedTaus"]
    toks = live_tokens(new)
    cat = layouts(d)
    for spec in json.load(open(path)):
        if "zoom" in spec and "media" not in spec:
            a, _ = find_span(toks, spec, "from")
            print("ZOOM %d%%  at ...%s" % (spec["zoom"], " ".join(t[3] for t in toks[a:a + 8])))
            continue
        media = find_media(d, spec["media"])
        a, b = find_span(toks, spec, "from")
        if "to" in spec:
            _, b = find_span(toks, spec, "to")
        look = spec.get("layout")
        if look not in cat:
            sys.exit("layout %r not in this project. Available: %s" % (look, ", ".join(sorted(cat))))
        print("PIN  %-38s layout %-28s" % (str(media.get("displayName"))[:38], look))
        print("     in  ...%s" % " ".join(t[3] for t in toks[max(0, a - 4):a + 10]))
        print("     out ...%s" % " ".join(t[3] for t in toks[max(0, b - 8):b + 4]))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "catalogue":
        catalogue()
    elif a[0] == "resolve":
        dry_run(a[1])
    else:
        sys.exit(__doc__)
