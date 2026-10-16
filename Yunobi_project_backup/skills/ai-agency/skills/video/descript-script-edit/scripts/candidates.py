#!/usr/bin/env python3
"""Enumerate abandoned-attempt candidates in a Descript block dump.

Pass 1 of the cut is mechanical, so it should not depend on an agent noticing
things. This finds every repeated run and every truncation mark, so the cut
list can be audited: each candidate is either a needle or a dismissal.

Usage:
    # blocks straight from the editor (a JSON array of strings)
    python3 candidates.py blocks.json

    # plain text, one block per line
    python3 candidates.py transcript.txt

    # which candidates the cut list does not cover
    python3 candidates.py blocks.json --check needles.json

Exit status is 1 when --check finds an uncovered candidate.
"""
import json
import re
import sys

WINDOW = 400        # a restart lands within this many characters of its attempt
SHINGLE = 3         # words per repeated run
TRUNCATION = re.compile(r"\S*(?:--|\.\.\.)(?=\s|$)|\b[A-Za-z]{1,3}-(?=\s)")


def load(path):
    raw = open(path).read()
    if path.endswith(".json"):
        blocks = json.loads(raw)
        return [b if isinstance(b, str) else b.get("text", "") for b in blocks]
    return [ln for ln in raw.split("\n") if ln.strip()]


def words(text):
    """Tokens with their character offsets, normalised for comparison."""
    return [(m.group(0).lower().strip(".,!?\"'"), m.start())
            for m in re.finditer(r"\S+", text)]


def repeats(text):
    """Spans that start a run the speaker abandoned and said again."""
    toks = words(text)
    seen, spans = {}, []
    for i in range(len(toks) - SHINGLE + 1):
        key = " ".join(t for t, _ in toks[i:i + SHINGLE])
        if not any(c.isalpha() for c in key):
            continue
        start = toks[i][1]
        prev = seen.get(key)
        if prev is not None and start - prev <= WINDOW:
            spans.append((prev, start))
        seen[key] = start
    # merge overlapping runs: three attempts at one sentence is one cut
    spans.sort()
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


def find(blocks):
    out = []
    for bi, text in enumerate(blocks):
        for a, b in repeats(text):
            out.append({"kind": "repeat", "b": bi, "at": a,
                        "t": text[a:b]})
        for m in TRUNCATION.finditer(text):
            a = max(0, text.rfind(" ", 0, max(0, m.start() - 60)) + 1)
            out.append({"kind": "truncation", "b": bi, "at": m.start(),
                        "t": text[a:m.end() + 1]})
    # a truncation inside a repeat run is the same cut, reported twice
    kept = []
    for c in sorted(out, key=lambda c: (c["b"], c["at"])):
        prev = kept[-1] if kept and kept[-1]["b"] == c["b"] else None
        if prev and c["at"] < prev["at"] + len(prev["t"]):
            continue
        kept.append(c)
    return kept


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    blocks = load(args[0])
    cands = find(blocks)
    chars = sum(len(b) for b in blocks)

    if "--check" in sys.argv:
        needles = json.load(open(args[1]))
        needles = [n if isinstance(n, str) else n["t"] for n in needles]
        joined = " ".join(needles)
        missed = [c for c in cands
                  if not any(c["t"][:24] in n or n[:24] in c["t"] for n in needles)
                  and c["t"][:24] not in joined]
        for c in missed:
            print(f"UNCOVERED b{c['b']} {c['kind']}: {c['t'][:110]!r}")
        cut = sum(len(n) for n in needles if any(n in b for b in blocks))
        print(f"\n{len(cands)} candidates, {len(missed)} uncovered")
        print(f"cut list removes {cut} of {chars} chars = {100 * cut / chars:.1f}%")
        return 1 if missed else 0

    for c in cands:
        print(f"b{c['b']:<3} {c['kind']:<10} {c['t'][:110]!r}")
    print(f"\n{len(cands)} candidates over {chars} chars", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
