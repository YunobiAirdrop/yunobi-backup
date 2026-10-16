#!/usr/bin/env python3
"""Enumerate abandoned-attempt candidates in a Descript block dump.

Pass 1 of the cut is mechanical, so it should not depend on an agent noticing
things. This finds every repeated run and every truncation mark, so the cut
list can be audited: each candidate is either a needle or a dismissal.

A repeat's span runs from the first attempt to the START of the last one, so
cutting the whole span keeps the final attempt whole. It is searched over the
joined script rather than block by block, because a restart lands in the
paragraph after the one it abandons.

Usage:
    # the raw script straight off a doc dump - `pnpm descript doc <project> --out doc.json`
    python3 candidates.py doc.json --comp "<name or id>"

    # blocks from the editor (a JSON array of strings), or plain text one block per line
    python3 candidates.py blocks.json
    python3 candidates.py transcript.txt

    # which candidates the cut list does not cover, block by block
    python3 candidates.py doc.json --check needles.json

    # the re-run on a finished cut: live taus only
    python3 candidates.py doc.json --live

Exit status is 1 when --check finds an uncovered candidate.
"""
import json
import re
import sys

import schema

WINDOW = 400        # a restart lands within this many characters of its attempt
SHINGLE = 3         # words per repeated run
TRUNCATION = re.compile(r"\S*(?:--|\.\.\.)(?=\s|$)|\b[A-Za-z]{1,3}-(?=\s)")

# Phrases that OPEN a digression rather than being one. The author, 2 Sep 2026: "when I say 'you could
# potentially' it's often the digression, this needs to be cut."
#
# WHY THIS IS A CANDIDATE AND NOT A CUT, unlike the sentence-opening `now` / `so` and the phrase
# "and what that means is that" in `recut2.py`. Those two ARE the filler: bounded, four words at
# most, and what remains after them is the sentence. This one is a SIGNPOST to a span whose end
# nothing in the text marks. His own example ran "you could potentially add another custom field
# with their email address, for example, or you could add your--" and died on a truncation; the one
# still live in EC49 runs a full sentence past the marker and into the next. Cutting to a guessed
# end would delete real teaching, and cutting only the marker leaves the digression behind with its
# opening gone, which is worse than leaving it whole.
#
# So it is surfaced EVERY time with a proposed span - marker to the truncation that follows, or to
# the end of the sentence - and `--check` exits 1 while the cut list does not cover it. Mechanical
# to notice, judged to bound. Add a phrase here the way this one arrived: he says it, it gets cut
# by hand once, and then it goes in the list.
DIGRESSIONS = re.compile(r"\byou could potentially\b", re.I)


def load(path, comp=None, cut=False):
    """Blocks from a doc dump, a JSON array of strings, or one block per line.

    Pass 1 reads the RAW script, blocked taus included, because a cut already made is the evidence
    for the one still missing beside it. `--live` is the re-run on a finished cut.
    """
    raw = open(path).read()
    if not path.endswith(".json"):
        return [ln for ln in raw.split("\n") if ln.strip()]
    doc = json.loads(raw)
    if isinstance(doc, list):
        return [b if isinstance(b, str) else b.get("text", "") for b in doc]
    comps = doc["compositions"]
    c = next((x for x in comps if comp in (x["id"], x["name"])), comps[0]) if comp else comps[0]
    taus = c["timeline"]["superTau"]["taus"]
    return [t["text"]["string"] for t in taus if not (cut and t.get("isBlocked"))]


def words(text):
    """Tokens with their character offsets, normalised for comparison."""
    return [(m.group(0).lower().strip(".,!?\"'"), m.start())
            for m in re.finditer(r"\S+", text)]


def joined(blocks):
    """The script as ONE string, with each block's (start, end) inside it.

    Detection runs over the whole script, never block by block. A restart lands in the paragraph
    AFTER the one it abandons - Descript breaks a paragraph at the pause the speaker took to start
    again - so a per-block search cannot see the thing it is looking for. FC38 opened with four
    attempts at one sentence spread over three paragraphs and reported zero candidates; the edit
    that followed kept attempt 2's head and attempt 4's tail. `references/what-to-cut.md`.
    """
    spans, at = [], 0
    for text in blocks:
        spans.append((at, at + len(text)))
        at += len(text) + 1
    return " ".join(blocks), spans


def where(spans, pos):
    """Block index and offset within that block, for a position in the joined script."""
    for bi, (a, b) in enumerate(spans):
        if pos <= b:
            return bi, max(0, pos - a)
    return len(spans) - 1, 0


def slices(spans, a, b):
    """Every (block, start, end) a cut of the joined range [a, b) has to remove.

    A needle cannot cross a paragraph break, so a span over three paragraphs is three needles and
    the cut list is only covered when it has all three. This is what `--check` counts.
    """
    out = []
    for bi, (s, e) in enumerate(spans):
        lo, hi = max(a, s), min(b, e)
        if hi - lo > 3:
            out.append((bi, lo - s, hi - s))
    return out


def repeats(text):
    """Spans that start a run the speaker abandoned and said again.

    The span runs from the FIRST attempt to the start of the LAST one, so what survives a cut of it
    is the final attempt whole. Never the other way round.
    """
    toks = words(text)
    at = {}
    for i in range(len(toks) - SHINGLE + 1):
        key = " ".join(t for t, _ in toks[i:i + SHINGLE])
        if any(c.isalpha() for c in key):
            at.setdefault(key, []).append(toks[i][1])

    # One key, one span: from its first hit to its LAST, chained while each hit is within WINDOW of
    # the one before. Four attempts at a sentence give one span that ends where the fourth begins.
    spans = []
    for hits in at.values():
        run = [hits[0]]
        for p in hits[1:]:
            if p - run[-1] > WINDOW:
                if len(run) > 1:
                    spans.append([run[0], run[-1]])
                run = []
            run.append(p)
        if len(run) > 1:
            spans.append([run[0], run[-1]])

    # The same attempts seen through a LATER shingle are the same cut, shifted. Merging the two -
    # what this did until 11 Sep 2026 - pushes the end past the start of the final attempt, and the
    # final attempt is the one that has to survive. So an overlapping span is dropped, never merged.
    spans.sort(key=lambda s: (s[0], -s[1]))
    kept = []
    for a, b in spans:
        if kept and a < kept[-1][1]:
            continue
        kept.append([a, b])
    return kept


def candidate(kind, spans, a, b, text):
    bi, at = where(spans, a)
    return {"kind": kind, "b": bi, "at": at, "g": a, "t": text[a:b],
            "keep": text[b:b + 70], "slices": slices(spans, a, b)}


def find(blocks):
    text, spans = joined(blocks)
    out = []
    for a, b in repeats(text):
        out.append(candidate("repeat", spans, a, b, text))
    for m in DIGRESSIONS.finditer(text):
        # To the truncation that follows it, or to the end of the sentence - whichever comes
        # first. That is a PROPOSAL: the span is the half a person still has to agree with.
        rest = text[m.end():]
        stop = TRUNCATION.search(rest)
        dot = re.search(r"[.?!](?=\s|$)", rest)
        ends = [x.end() for x in (stop, dot) if x]
        end = m.end() + (min(ends) if ends else len(rest))
        out.append(candidate("digression", spans, m.start(), end, text))
    for m in TRUNCATION.finditer(text):
        a = max(0, text.rfind(" ", 0, max(0, m.start() - 60)) + 1)
        out.append(candidate("truncation", spans, a, m.end() + 1, text))
    # a truncation inside a repeat run is the same cut, reported twice
    kept = []
    for c in sorted(out, key=lambda c: c["g"]):
        prev = kept[-1] if kept else None
        if prev and c["g"] < prev["g"] + len(prev["t"]):
            continue
        kept.append(c)
    return kept


def masks(blocks, needles):
    """Where the cut list removes text, one mark per block.

    A needle cuts ONE place - the CLI refuses one that reads twice - so each is resolved to the
    first block it reads in, and a needle written twice takes the next block after that. The same
    resolution the cut itself does, so the coverage below is the cut's own.
    """
    marks, used = [bytearray(len(b)) for b in blocks], {}
    for n in needles:
        if len(n.strip()) < 4:
            continue
        for bi in range(used.get(n, 0), len(blocks)):
            i = blocks[bi].find(n)
            if i < 0:
                continue
            marks[bi][i:i + len(n)] = b"\x01" * len(n)
            used[n] = bi + 1
            break
    return marks


def live(c, blocks, marks):
    """The prose inside a candidate's span that the cut list leaves standing, block by block.

    Head-matching was the old test and it passed the FC38 opening: needles covered the first
    attempt and the third, and the SECOND sat untouched between them, so the finished sentence
    read as attempt 2's head spliced onto attempt 4's tail.
    """
    out = []
    for bi, s, e in c["slices"]:
        rest = "".join(ch for j, ch in enumerate(blocks[bi][s:e]) if not marks[bi][s + j])
        rest = re.sub(r"[\s.,!?\"'-]+", " ", rest).strip()
        if len(rest) > 4:
            out.append((bi, rest))
    return out


def main():
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    comp = argv[argv.index("--comp") + 1] if "--comp" in argv else None
    if comp in args:
        args.remove(comp)
    blocks = load(args[0], comp, cut="--live" in argv)
    cands = find(blocks)
    chars = sum(len(b) for b in blocks)

    if "--check" in sys.argv:
        needles = [schema.needle_text(n) for n in schema.load(args[1], "needles")]
        marks = masks(blocks, needles)
        missed = [(c, rest) for c in cands if (rest := live(c, blocks, marks))]
        for c, rest in missed:
            print(f"UNCOVERED b{c['b']} {c['kind']}: {c['t'][:110]!r}")
            for bi, piece in rest:
                print(f"    still live in b{bi}: {piece[:96]!r}")
            if c["kind"] == "repeat":
                print(f"    the keep is the LAST attempt: {c['keep'][:96]!r}")
        cut = sum(len(n) for n in needles if any(n in b for b in blocks))
        print(f"\n{len(cands)} candidates, {len(missed)} uncovered")
        print(f"cut list removes {cut} of {chars} chars = {100 * cut / chars:.1f}%")
        return 1 if missed else 0

    for c in cands:
        print(f"b{c['b']:<3} {c['kind']:<10} {c['t'][:110]!r}")
        if c["kind"] == "repeat":
            last = c["slices"][-1][0]
            print(f"{'':<15}keep {c['keep'][:96]!r}   (cut spans b{c['b']}-b{last})")
    print(f"\n{len(cands)} candidates over {chars} chars", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
