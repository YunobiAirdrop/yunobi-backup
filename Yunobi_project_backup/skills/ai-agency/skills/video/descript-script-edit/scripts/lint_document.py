#!/usr/bin/env python3
"""THE GATE. Nothing is committed to a Descript document until this exits 0.

    python3 lint_document.py doc.json

It checks the three invariants the Descript client checks, because ANY ONE of them makes the client
refuse the WHOLE document: the project stops opening, the editor shows "Oh no! Something's not
working", and the repair cannot be done from the app because the app will not load it.

    1. Every *Id reference resolves to an object that exists.
    2. Every pin a card layer draws is REGISTERED in that composition's timeline.pins.components.
       Existing in the top-level `pinScenes` list is NOT enough - "pinTrack", in the client's error
       text, means the registration, not the scene.
    3. Both the cards track and the pins track are in script order. Appending a component is never
       enough; it has to be sorted in. ("DocumentInvalidError: Components are in incorrect order")

`assetKey` is excluded on purpose: it is a drive asset guid, not a document object id.

Measured on EC49, 2026-08-31. Cards 122, markers 48, pin scenes 71, words 6981 - every count
matched the known-good state and the document would not open. A count proves nothing was deleted.
It says nothing about whether what remains still points at things that exist, in a form the client
recognises. This is the only thing that proves the document loads.
"""
import json, sys

REFERENCE_FIELDS = ("sceneId", "mediaRefId", "roomtoneRefId",
                    "sourceSceneId", "sequenceSceneId", "tauId", "cardBoundaryId")


def faults(doc):
    ids, bad, warn = set(), [], []

    def collect(o):
        if isinstance(o, dict):
            if isinstance(o.get("id"), str):
                ids.add(o["id"])
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
    collect(doc)

    def check(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in REFERENCE_FIELDS and isinstance(v, str) and v and v not in ids:
                    bad.append("%s>%s = %s" % (path, k, v))
                check(v, "%s>%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                check(v, "%s>%d" % (path, i))
    check(doc)

    scenes = {p.get("id") for p in doc.get("pinScenes", [])}
    for n, comp in enumerate(doc.get("compositions", [])):
        tl = comp.get("timeline") or {}
        if not (tl.get("cards") or {}).get("components"):
            continue

        order = {}

        def walk(o):
            if isinstance(o, dict):
                if isinstance(o.get("text"), dict) and isinstance(o["text"].get("string"), str) \
                        and o.get("id") and o["id"] not in order:
                    order[o["id"]] = len(order)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(comp)
        at = lambda c: order.get((c.get("tauAnchor") or {}).get("tauId"), 1 << 30)

        registered = {c.get("sceneId") for c in (tl.get("pins") or {}).get("components", [])}
        for i, card in enumerate((tl.get("cards") or {}).get("components", [])):
            for j, layer in enumerate(card.get("layers") or []):
                scene = layer.get("sourceSceneId")
                if scene in scenes and scene not in registered:
                    bad.append("compositions>%d>timeline>cards>components>%d>layers>%d>sourceSceneId"
                               " = %s (pin is not registered in the pins track)" % (n, i, j, scene))

        for track in ("cards", "pins"):
            keys = [at(c) for c in (tl.get(track) or {}).get("components", [])]
            if keys != sorted(keys):
                bad.append("compositions>%d>timeline>%s>components are not in script order" % (n, track))
    return bad, warn


if __name__ == "__main__":
    bad, warn = faults(json.load(open(sys.argv[1])))
    print("%d fault(s), %d warning(s)" % (len(bad), len(warn)))
    for b in bad[:25]:
        print("  ", b)
    sys.exit(1 if bad else 0)
