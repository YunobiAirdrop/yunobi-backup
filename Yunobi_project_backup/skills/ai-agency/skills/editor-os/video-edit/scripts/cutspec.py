#!/usr/bin/env python3
"""A whole cut written against the raw script's line numbers, checked before it touches Descript.

Spec lines, one cut each, in script order:
    12                     the whole of line 12
    4-8                    lines 4 to 8
    9 | ^ .. inst--        line 9, from its start through the first "inst--"
    54 | And if you .. $   from that phrase to the end of the line
    60 | exact words       just those words (the first after the previous cut in that line)
    83 | ~So .. $          "~" takes the LAST occurrence in the line
    12 | ... #ok           the seam this cut leaves was read and is fine
    # a comment

Usage:
    python3 cutspec.py raw doc.json raw.txt              # the raw script, one Descript line per line
    python3 cutspec.py check raw.txt spec.txt            # resolve, print flagged seams, the ratio
    python3 cutspec.py check raw.txt spec.txt --read     # also print the surviving script
    python3 cutspec.py edits raw.txt spec.txt out.json   # the batch for `pnpm descript edits`

`edits` is written for a composition still holding the raw script as ONE paragraph: cuts go back
to front, scoped to the first line, so every needle reads in one paragraph only. After a bad pass,
`pnpm descript undo <project> <n>` back to raw first, never a pile of restores.

The method. A candidate from `candidates.py` isn't a cut: it flags lists as well as retakes, and
on 23 Sep 2026 a worker that cut all 299 left 187 broken joins ("Opus is when someone has to do
200 mini tasks"). So Claude reads the raw script and writes this spec. Keep the last attempt whole.
`check` flags every join that isn't a sentence boundary, filler, or an abandoned try at the kept
words. Read each one, mark the fine ones `#ok`, and ship at 0 unread. Then `pnpm descript edits
<project> <comp> out.json --dry` (0 refused), the real run, and `seams.py` on a fresh dump.

A cut never starts on a comma glued to the word before it: the CLI snaps back over that word's
audio, so the start moves past it here. A stub glued to a word (`G-it's`) stays, for the same reason.
"""
import json
import re
import sys

from seams import bad


def resolve(raw, spec):
    lines = raw.split("\n")
    starts, at = [], 0
    for ln in lines:
        starts.append(at)
        at += len(ln) + 1
    cursor = {}
    ranges = []
    for n, row in enumerate(open(spec).read().splitlines(), 1):
        ok = row.rstrip().endswith("#ok")
        row = row.split(" #")[0].strip() if not row.lstrip().startswith("#") else ""
        if not row:
            continue
        head, _, body = row.partition("|")
        head = head.strip()
        if not body:
            a, _, b = head.partition("-")
            a, b = int(a), int(b or a)
            ranges.append((starts[a - 1], starts[b - 1] + len(lines[b - 1]), n, ok))
            continue
        li = int(head) - 1
        text, base = lines[li], starts[li]
        frm, sep, to = body.strip().partition(" .. ")
        c = cursor.get(li, 0)
        if frm == "^":
            a = 0
        elif frm.startswith("~"):
            frm = frm[1:]
            a = text.rfind(frm)
        else:
            a = text.find(frm, c)
            if a < 0:
                sys.exit(f"spec line {n}: {frm!r} not in line {li + 1} after col {c}")
        if not sep:
            b = a + len(frm)
        elif to == "$":
            b = len(text)
        else:
            e = text.find(to, a + (0 if frm == "^" else len(frm)))
            if e < 0:
                sys.exit(f"spec line {n}: {to!r} not in line {li + 1} after {frm!r}")
            b = e + len(to)
        # A cut opening on punctuation glued to the word before it snaps back over that word's audio.
        while a < b and text[a] in ",.;:!? ":
            a += 1
        cursor[li] = b
        ranges.append((base + a, base + b, n, ok))
    ranges.sort()
    for (a1, b1, n1, _), (a2, b2, n2, _) in zip(ranges, ranges[1:]):
        if a2 < b1:
            sys.exit(f"spec lines {n1} and {n2} overlap")
    # Neighbouring cuts with only whitespace between them are one cut.
    merged = []
    for a, b, n, ok in ranges:
        if merged and not raw[merged[-1][1]:a].strip():
            merged[-1][1] = b
            merged[-1][2] = merged[-1][2] or ok
        else:
            merged.append([a, b, ok])
    return merged


def check(raw, ranges, show=False):
    flagged, read, prev = 0, 0, 0
    for a, b, ok in ranges:
        left = raw[prev:a].rstrip()[-70:]
        prev = b
        right = raw[b:b + 70].lstrip()
        if b >= len(raw.rstrip()) or not left:
            continue
        why = bad(left, raw[a:b], right)
        if why and ok:
            read += 1
        elif why:
            flagged += 1
            line = raw.count("\n", 0, a) + 1
            print(f"L{line:<4} {why}\n      …{left!r}\n  cut  {raw[a:b][:100]!r}\n      {right!r}…")
    cut = sum(b - a for a, b, _ in ranges)
    live, at = [], 0
    for a, b, _ in ranges:
        live.append(raw[at:a])
        at = b
    live.append(raw[at:])
    print(f"\n{len(ranges)} cuts, {flagged} seams flagged, {read} read (#ok); {cut} of {len(raw)} chars = {100 * cut / len(raw):.1f}%")
    if show:
        print("\n" + re.sub(r"\n\s*\n", "\n", "".join(live)))
    return flagged


def edits(raw, ranges):
    scope = raw.split("\n")[0]
    out = []
    for a, b, _ in reversed(ranges):
        needle = raw[a:b]
        head = raw[:b].lower()
        low, nth, i = needle.lower(), 0, -1
        while True:
            i = head.find(low, i + 1)
            if i < 0 or i > a:
                break
            nth += 1
        step = {"verb": "cut", "from": needle, "in": scope}
        if nth > 1:
            step["nth"] = nth
        out.append(step)
    return out


def main():
    cmd, *args = sys.argv[1:] or ["--help"]
    if cmd in ("-h", "--help"):
        print(__doc__)
        return 0
    if cmd == "raw":
        doc = json.load(open(args[0]))
        taus = doc["compositions"][0]["timeline"]["superTau"]["taus"]
        open(args[1], "w").write("".join(t["text"]["string"] for t in taus))
        return 0
    raw = open(args[0]).read()
    ranges = resolve(raw, args[1])
    if cmd == "check":
        return 1 if check(raw, ranges, "--read" in args) else 0
    if cmd == "edits":
        json.dump(edits(raw, ranges), open(args[2], "w"), ensure_ascii=False, indent=1)
        print(f"{len(ranges)} cuts written to {args[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
