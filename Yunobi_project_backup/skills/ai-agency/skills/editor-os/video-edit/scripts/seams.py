#!/usr/bin/env python3
"""Every place a cut glues two live pieces together, and the ones that read as unfinished.

A seam is clean when the left piece ends a sentence and the right one starts one, or when all
the cut took out was filler. Anything else is an attempt's head on another's tail, a list item
cut out of a list, or a stump left live: read it, then restore or widen the cut.

Usage:
    python3 seams.py doc.json [--comp "<name or id>"] [--all]

Exit status is 1 while a seam is flagged.
"""
import json
import re
import sys

FILLER = re.compile(r"^(?:[\s,.]*\b(?:uh|um|euh|so|now|like|you know|okay|well|basically)\b[\s,.]*)+$", re.I)
ENDS = re.compile(r"[.?!:][\"')]*\s*$")
STARTS = re.compile(r"^\s*[\"'(]*[A-Z0-9]")
STUMP = re.compile(r"\S*(?:--|\.\.\.)(?=\s|$)")


def taus(path, comp=None):
    doc = json.load(open(path))
    comps = doc["compositions"]
    c = next((x for x in comps if comp in (x["id"], x["name"])), comps[0]) if comp else comps[0]
    return [(t["text"]["string"], bool(t.get("isBlocked"))) for t in c["timeline"]["superTau"]["taus"]
            if t["text"]["string"].strip()]


def seams(ts):
    """(left, cut, right, index) for every run of blocked taus between two live ones."""
    out, i = [], 0
    while i < len(ts):
        if ts[i][1] and i > 0 and not ts[i - 1][1]:
            j = i
            while j < len(ts) and ts[j][1]:
                j += 1
            if j < len(ts):
                out.append((ts[i - 1][0], " ".join(t for t, _ in ts[i:j]), ts[j][0], i))
            i = j
        else:
            i += 1
    return out


def lead(text, n=None):
    return re.findall(r"[a-z']+", text.lower())[:n]


def restart(cut, right):
    """The cut is an abandoned try at the kept words: it stops on a stump, or is their opening."""
    c, r = lead(cut), lead(right)
    if len(c) < 2 or c[:2] != r[:2]:
        return False
    if STUMP.search(cut.rstrip()[-6:]):
        return True
    return c[:-1] == r[:len(c) - 1] and r[len(c) - 1].startswith(c[-1])


def bad(left, cut, right):
    if FILLER.match(cut):
        return None
    if restart(cut, right) and not STUMP.search(left.rstrip()[-40:]):
        return None
    if STUMP.search(left.rstrip()[-40:]):
        return "stump left live"
    if not ENDS.search(left) and not STARTS.match(right):
        return "mid-sentence splice"
    if not ENDS.search(left):
        return "left piece unfinished"
    if not STARTS.match(right):
        return "right piece starts mid-sentence"
    return None


def main():
    argv = sys.argv[1:]
    comp = argv[argv.index("--comp") + 1] if "--comp" in argv else None
    ts = taus(argv[0], comp)
    found = seams(ts)
    flagged = 0
    for left, cut, right, i in found:
        why = bad(left, cut, right)
        if why:
            flagged += 1
        if why or "--all" in argv:
            print(f"t{i:<4} {why or 'clean'}")
            print(f"      …{left[-70:]!r}")
            print(f"  cut  {cut[:110]!r}")
            print(f"      {right[:70]!r}…")
    live = " ".join(t for t, b in ts if not b)
    stumps = STUMP.findall(live)
    print(f"\n{len(found)} seams, {flagged} flagged; {len(stumps)} truncation marks still live")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
