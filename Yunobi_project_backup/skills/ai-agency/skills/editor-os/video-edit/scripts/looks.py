#!/usr/bin/env python3
"""Change the LAYOUT of the speaker's own scenes, and punch in on a beat.

`pins.py` places borrowed media and refuses to invent geometry, which is right:
a b-roll clip must look like a clip the video already uses. A screen-share demo
has the opposite problem - it holds no pin layer at all, so there is no layout
library to clone, and the camera and the screen sit in one frozen split for the
whole runtime. This emits card boundaries over the scenes that are ALREADY in
the composition, so it needs no pinTrack and no clip dragged in by hand.

    looks.json  [{"look": "screen-full", "from": "So we have a Glance portal"},
                 {"look": "screen-full", "zoom": 130, "from": "the budget is a custom field"},
                 {"look": "camera-full", "from": "That is a ridiculous return"}]

usage: looks.py looks.json [--close-open-pins] [--write]
"""
import json, os, sys, copy, datetime, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pins as P, dclip

HOME = os.path.expanduser("~/.descript-clip")
FRAME = 0.5625                                  # 16:9, width-normalised

# box + position per named look. A hidden layer keeps its geometry and is skipped
# on render, so switching back to it later needs no repair.
LOOKS = {
    "split":       {"camera": ({"width": .5,  "height": .28125}, {"x": .25, "y": .5}),
                    "screen": ({"width": .5,  "height": .28125}, {"x": .75, "y": .5})},
    "camera-full": {"camera": ({"width": 1.0, "height": FRAME},  {"x": .5,  "y": .5}),
                    "screen": None},
    "screen-full": {"camera": None,
                    "screen": ({"width": 1.0, "height": FRAME},  {"x": .5,  "y": .5})},
    "screen-pip":  {"camera": ({"width": .22, "height": .12375}, {"x": .855, "y": .845}),
                    "screen": ({"width": 1.0, "height": FRAME},  {"x": .5,  "y": .5})},
    "camera-pip":  {"camera": ({"width": 1.0, "height": FRAME},  {"x": .5,  "y": .5}),
                    "screen": ({"width": .22, "height": .12375}, {"x": .855, "y": .845})},
}
# index 0 is ON TOP, so the small window is listed first
Z = {"split": ["camera", "screen"], "camera-full": ["camera", "screen"],
     "screen-full": ["screen", "camera"], "screen-pip": ["camera", "screen"],
     "camera-pip": ["screen", "camera"]}


def scene_roles(d):
    """sequenceSceneId -> 'screen' or 'camera', read off the track's own name."""
    role = {}
    for t in d.get("sequenceTracks", []):
        tl = t.get("timeline") or {}
        if not tl.get("superTau"):
            continue
        role[t["id"]] = "screen" if "screen" in str(t.get("name", "")).lower() else "camera"
    return role


def main():
    specs = json.load(open(sys.argv[1]))
    p = json.load(open(os.path.join(HOME, "current.json")))
    d = p["data"][0]
    taus = d["copiedTaus"]
    toks = P.live_tokens(taus)
    order = {t["id"]: i for i, t in enumerate(taus)}
    role = scene_roles(d)
    comps = d.setdefault("copiedComponents", [])
    made = []

    for sp in specs:
        look = sp["look"]
        if look not in LOOKS:
            sys.exit("%r is not a look. Choose one of: %s" % (look, ", ".join(sorted(LOOKS))))
        a, _ = P.find_span(toks, sp, "from")
        anchor = P.anchor_at(taus, toks, a)
        key = P.key_of(order, anchor)
        cards = P.cards_in(d)
        src = P._state_at(cards, order, key)
        if src is None:
            sys.exit("no card boundary to clone from")
        card = next((c for c in cards if P.key_of(order, c["tauAnchor"]) == key), None)
        if card is None:
            card = P._card_from(src, anchor, name=look)
            comps.append(card); made.append(card)
        else:
            card["name"] = look

        by_role = {}
        for l in card.get("layers", []):
            # a card layer names the composition's own source track in
            # `sourceSceneId` and the sequence it shows in `sequenceSceneId`;
            # the role lives on the second (2026-08-25)
            r = role.get(l.get("sequenceSceneId"))
            if r and r not in by_role:
                by_role[r] = l
        missing = [r for r in ("camera", "screen") if r not in by_role]
        if missing:
            sys.exit("%r at %r: the prevailing card has no %s layer"
                     % (look, sp["from"][:50], " and ".join(missing)))

        for r, geo in LOOKS[look].items():
            l = by_role[r]
            if geo is None:
                l["isHidden"] = True
                continue
            l["isHidden"] = False
            box, pos = geo
            P._set_geo(l, "box", dict(box))
            P._set_geo(l, "position", dict(pos))
            scale = sp.get("zoom") if r == sp.get("zoomLayer", "screen") else None
            P._set_geo(l, "contentScale",
                       {"x": scale / 100.0, "y": scale / 100.0} if scale else {"x": 1.0, "y": 1.0})
        # Only the camera/screen PAIR reorders. A b-roll pin in the same stack
        # keeps its own z-slot: appending foreign layers after the pair drops a
        # full-frame plate behind the talking head, and cloning a stack that
        # still holds a pin past its closing card runs the clip to the end of
        # the video (2026-08-25).
        slots = [i for i, l in enumerate(card["layers"]) if l in by_role.values()]
        for slot, layer in zip(slots, [by_role[r] for r in Z[look]]):
            card["layers"][slot] = layer
        if sp.get("zoom"):
            card["name"] = "%s %d%%" % (look, sp["zoom"])

    # An anchor on a TAU the cut blocked opens the card on struck-through text.
    # Descript re-splits TAUs on paste, so a card that was live when it was
    # written can land on a blocked one later: slide it to the next live TAU
    # rather than refusing (2026-08-25).
    cards = P.cards_in(d)
    live = [i for i, t in enumerate(taus) if not t.get("isBlocked")]
    slid = 0
    for c in cards:
        ti = order.get(c["tauAnchor"]["tauId"])
        if ti is None or taus[ti].get("isBlocked"):
            nxt = next((i for i in live if ti is None or i > ti), live[0] if live else None)
            if nxt is None:
                sys.exit("nothing survives the cut - refusing to place cards")
            c["tauAnchor"] = {"tauId": taus[nxt]["id"], "location": 0}
            slid += 1
    if slid:
        print("%d card(s) slid forward off struck-through text" % slid)

    # A clip dragged in as a LAYOUT TEMPLATE arrives as a scene running to
    # `endOfComposition`, so it is full-frame over the whole video and every
    # card a layout pass clones carries it forward. --close-open-pins ends that
    # scene at the first card written here and drops the layer from that card
    # on, which leaves the template in the project to clone from without it
    # covering a frame (2026-08-25).
    if "--close-open-pins" in sys.argv and made:
        first = min(made, key=lambda c: P.key_of(order, c["tauAnchor"]))
        pinids = {t["id"] for t in d.get("pinTracks", [])}
        closed = 0
        for c in comps:
            if (c.get("type") == "sceneComponent" and c.get("sceneId") in pinids
                    and (c.get("endAnchor") or {}).get("type") == "endOfComposition"):
                c["endAnchor"] = {"type": "cardBoundary", "cardBoundaryId": first["id"]}
                closed += 1
        k0 = P.key_of(order, first["tauAnchor"])
        for c in P.cards_in(d):
            if P.key_of(order, c["tauAnchor"]) >= k0:
                c["layers"] = [l for l in c["layers"] if l.get("sourceSceneId") not in pinids]
        if closed:
            print("closed %d open-ended pin scene(s) at the first card" % closed)
    print("%d cards over %d looks (%d anchors)"
          % (len(cards), len(specs), len({P.key_of(order, c['tauAnchor']) for c in cards})))
    for c in sorted(cards, key=lambda c: P.key_of(order, c["tauAnchor"])):
        vis = [role.get(l.get("sequenceSceneId"), "?") for l in c["layers"] if not l.get("isHidden")]
        print("  %-18s %s" % (c.get("name", "(opening)"), "+".join(vis)))

    if "--write" in sys.argv:
        dclip.write(p, p["text"][0] if p.get("text") else
                    "".join(t["text"]["string"] for t in taus))
        back, _ = dclip.decode()
        if json.dumps(back, sort_keys=True) != json.dumps(p, sort_keys=True):
            sys.exit("clipboard did not round-trip - do not paste")
        json.dump(p, open(os.path.join(HOME, "last_apply.json"), "w"))
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        json.dump(p, open(os.path.join(HOME, "history", "%s-looks.json" % ts), "w"))
        json.dump({"kind": "looks", "label": "", "at": ts, "taus": len(taus),
                   "blocked": sum(1 for t in taus if t.get("isBlocked")), "plays": 0,
                   "words": len(re.findall(r"\S+", "".join(t["text"]["string"] for t in taus))),
                   "project": d.get("projectId")},
                  open(os.path.join(HOME, "history", "%s-looks.meta.json" % ts), "w"), indent=1)
        print("ON CLIPBOARD -> Cmd+A, Cmd+V in Descript. Do not copy anything else first.")

if __name__ == "__main__":
    main()
