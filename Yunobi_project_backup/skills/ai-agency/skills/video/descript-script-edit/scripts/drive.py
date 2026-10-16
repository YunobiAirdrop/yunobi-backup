#!/usr/bin/env python3
"""Apply a list of script cuts to a Descript composition via Orca's browser.

Usage:
    export DESCRIPT_PAGE=<browserPageId from `orca tab create --json`>
    python3 drive.py needles.json            # all cuts
    python3 drive.py needles.json 4 7 12     # only these indices

A needle is either a plain string (searched across the whole script) or
{"b": <block index>, "t": "<text>"} to confine it to one paragraph. Use the
object form for any needle a second paragraph could also contain. The index is
a hint, not an address: an Ignore can split a paragraph, so every cut re-reads
the blocks and takes the candidate nearest the recorded index.

Add "g" when the span contains a marker: "t" is the DOM text, which includes the
marker's pin glyph, and "g" is what getSelection() reports, which does not.
Without it the drag lands and the law 6 guard then refuses its own selection.

Prerequisites (see SKILL.md):
    orca tab create --url "https://web.descript.com/<project>/<short>" --json
    orca exec  --page "$DESCRIPT_PAGE" --command "set viewport 1600 11500"
    orca eval  --page "$DESCRIPT_PAGE" --expression "$(cat helpers.js)" --json

Idempotent: a needle already ignored reports not-found and is skipped.
"""
import json
import os
import subprocess
import sys
import time

PAGE = os.environ.get("DESCRIPT_PAGE")
if not PAGE:
    sys.exit("set DESCRIPT_PAGE to the browserPageId first")


def run(args, timeout=90):
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return p.stdout.strip(), p.stderr.strip()


def ev(expr):
    out, err = run(["orca", "eval", "--page", PAGE, "--expression", expr, "--json"])
    try:
        return json.loads(out).get("result", {}).get("result")
    except Exception:
        return None


def ab(cmd):
    return run(["orca", "exec", "--command", cmd, "--page", PAGE, "--json"])


def jparse(v):
    try:
        return json.loads(v)
    except Exception:
        return {"unparsed": v}


def blocks():
    return jparse(ev("JSON.stringify(window.__blocks().map(b=>window.__map(b).text))")) or []


def resolve(needle, block):
    """Current index of the block holding `needle`.

    An Ignore can split a paragraph in two, so an index recorded when the cut
    list was written goes stale mid-run. Re-read the blocks and pick the one
    nearest the recorded index among those that still contain the text.
    """
    hits = [i for i, t in enumerate(blocks()) if needle in t]
    if not hits:
        return None
    if block is None:
        return hits[0] if len(hits) == 1 else None
    return min(hits, key=lambda i: abs(i - block))


def drag(r, waypoints=1, reverse=False):
    """Law 2: a drag, never click + shift-click. Only a drag mounts the toolbar.

    Law 8 opens it: release first, because a `mouse up` that did not register
    leaves the button held and the next move extends one selection across every
    paragraph in between - which anything typed then overwrites.
    """
    sx, sy, ex, ey = r["sx"], r["sy"], r["ex"], r["ey"]
    if reverse:
        sx, sy, ex, ey = ex, ey, sx, sy

    ab("mouse up")
    ab(f"mouse move {sx} {sy}")
    ab("mouse down")
    for k in range(1, waypoints + 1):
        ab(f"mouse move {round(sx + (ex - sx) * k / waypoints)} "
           f"{round(sy + (ey - sy) * k / waypoints)}")
        time.sleep(0.15)
    ab("mouse up")


def cut(item, idx):
    needle = item["t"] if isinstance(item, dict) else item
    block = item.get("b") if isinstance(item, dict) else None
    # A marker inside the span puts characters in the DOM text that
    # getSelection() never reports (its pin glyph and a doubled space), so the
    # string that finds the range and the string the guard compares against are
    # not the same one. Optional "g" carries the selection text for the guard.
    guard = item.get("g", needle) if isinstance(item, dict) else needle
    n = json.dumps(needle)
    g = json.dumps(guard)
    here = resolve(needle, block)
    scope = n if here is None else f"{n},{here}"
    r = jparse(ev(f"JSON.stringify(window.__find({scope}))"))
    if not r.get("ok"):
        return {"i": idx, "status": "not-found-or-done"}
    if not r.get("onscreen"):
        # Law 7: grow the viewport rather than trying to scroll.
        return {"i": idx, "status": "offscreen", "top": r.get("top")}

    res = {}
    # A one-jump drag sometimes collapses into a click and selects only the
    # first word, deterministically - a plain retry reproduces it exactly.
    # Slowing the drag fixes most of those, reversing it fixes the rest.
    for waypoints, reverse in ((1, False), (5, False), (5, True)):
        drag(r, waypoints, reverse)

        # The toolbar mounts late; retry until it exists or the guard rejects.
        for _ in range(10):
            time.sleep(0.8)
            res = jparse(ev(f"JSON.stringify(window.__igIfSync({g}))"))
            if res.get("clicked") or res.get("mismatch"):
                break

        if res.get("clicked"):
            break
        # Escalate only on a collapsed selection. A selection LARGER than the
        # needle is a stale coordinate (law 6) - dragging harder makes it worse.
        if res.get("gotLen", 0) >= len(guard):
            break

    # Never leave a live selection behind (law 8).
    ab("mouse up")
    ev("(window.getSelection().removeAllRanges(),1)")

    res["i"] = idx
    res["status"] = "ignored" if res.get("clicked") else "blocked"
    return res


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    needles = json.loads(open(sys.argv[1]).read())
    idxs = [int(x) for x in sys.argv[2:]] or range(len(needles))
    done = blocked = skipped = 0
    for i in idxs:
        out = cut(needles[i], i)
        print(json.dumps(out), flush=True)
        if out["status"] == "ignored":
            done += 1
        elif out["status"] == "blocked":
            blocked += 1
        else:
            skipped += 1
    print(json.dumps({"ignored": done, "blocked": blocked, "skipped": skipped}))


if __name__ == "__main__":
    main()
