#!/usr/bin/env python3
"""Prove a cut loop survived. usage: prove_cuts.py doc.json needles.json ["<comp>"]

A cut loop can report a commit ref for every needle and still be gone an hour later: any editor tab
open on the project merges its own copy back over the CLI's writes, and the reverted document reads
as healthy. 42 needles landed on 8 Sep 2026, each with a ref, and every one was live again by the
next dump. Reading the write back inside the loop does not catch it; only a fresh dump does.

So: finish the loop, dump the document again, and run this. It exits 1 while any needle is still in
the live script, which is the only proof the cut is really there.

    pnpm descript doc <project> --out after.json
    python3 prove_cuts.py after.json needles.json
"""
import json
import sys

import schema


def live_taus(path, comp=None):
    d = json.load(open(path))
    comps = d["compositions"]
    c = next((x for x in comps if comp in (x["id"], x["name"])), comps[0]) if comp else comps[0]
    return [t for t in c["timeline"]["superTau"]["taus"] if not t.get("isBlocked")]


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip().splitlines()[0])
        return 2
    comp = sys.argv[3] if len(sys.argv) > 3 else None
    taus = live_taus(sys.argv[1], comp)
    text = "".join(t["text"]["string"] for t in taus)
    runtime = sum(t["audioSegment"]["duration"] / (t["audioSegment"].get("speed") or 1)
                  for t in taus)

    # The shapes are needles.schema.json. A scoped needle ("obviously " under one paragraph) is
    # proven inside the 400 live characters after its `in` anchor, because the same word stands
    # legitimately in ten other paragraphs and a whole-script test would call every one a revert.
    raw = schema.load(sys.argv[2], "needles")
    needles = [(schema.needle_text(n), n.get("in") if isinstance(n, dict) else None) for n in raw]

    def live(n, anchor):
        if not anchor:
            return n.lower() in text.lower()
        at = text.lower().find(anchor.lower())
        return at < 0 or n.lower() in text[at:at + len(anchor) + 400].lower()

    survivors = [n for n, anchor in needles if live(n, anchor)]
    for n in survivors:
        print(f"STILL LIVE: {n[:90]!r}")
    print(f"\n{len(needles) - len(survivors)} of {len(needles)} needles gone, "
          f"live runtime {runtime:.1f}s over {len(taus)} paragraphs")
    if survivors:
        print("A cut loop that reported refs and left needles live is the editor-tab revert: "
              "the runtime is back near its old value. Close every tab on the project and re-drive "
              "the list. Do not re-drive it while somebody is in the document.")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
