#!/usr/bin/env python3
"""Enumerate pass-2 candidates: the sentences that are clean and carry nothing.

`candidates.py` enumerates pass 1, so pass 1 does not depend on an agent noticing
things. Pass 2 did, and that is why it gets skipped: a first-take lesson comes back
with zero wreckage left and every restatement still in it. This finds the four kinds
that a reader can check, so pass 2 is auditable the same way.

    python3 restate.py doc.json --comp "<name or id>"   # the live script from a doc dump
    python3 restate.py blocks.json                      # or a JSON array of strings
    python3 restate.py doc.json --check needles.json    # what the cut list does not cover

Exit status is 1 when --check finds an uncovered candidate. Every candidate is a
needle or a dismissal, and a dismissal is one word.

The four are the ones `references/what-to-cut.md` names. `restate` is item 2, the same
idea in different words, which is the one that costs the most seconds and the one no
regex finds: it scores content-word overlap between sentences inside a window, so
`create a single source of truth` and `emphasizing on that single source of truth`
both surface. The other three are phrase lists, because they are phrases.
"""
import json
import re
import sys

import schema

WINDOW = 12         # sentences apart, past which two utterances are not each other's echo
OVERLAP = 0.50      # share of the shorter sentence's content words the longer one repeats
MIN_CONTENT = 5     # a sentence with fewer content words is too short to score

STOP = set("""a an and are as at be been but by can could do does for from get go going gonna
had has have here how i if in into is it its it's just like me my no not of on one or our out
so than that the their them then there these they this those to too up us want was we well were
what when where which who will with would you your yours""".split())

ANNOUNCE = re.compile(r"""\b(
    in\s+this\s+video | i'?m\s+gonna\s+show\s+you | i'?ll\s+show\s+you
  | i'?m\s+gonna\s+(share|talk|walk) | what\s+i\s+want\s+you\s+to\s+do
  | (later|in\s+a\s+(second|minute))\s+(in\s+this\s+video)? | before\s+we\s+(get|dive)
  | i'?ve\s+(actually\s+)?(talked|covered)\s+about\s+(it|that)
)\b""", re.I | re.X)

HEDGE = re.compile(r"""(
    it'?s\s+pretty\s+(cool|straightforward|mind-?blowing|simple|easy|crazy|nice)
  | don'?t\s+worry | obviously,? | by\s+the\s+way | ,?\s*fyi\b | just\s+as\s+a\s+reminder
  | this\s+is\s+not\s+a\s+(sales\s+)?pitch | i\s+don'?t\s+want\s+to\s+promise
  | if\s+i\s+wanted | not\s+too\s+bad | or\s+whatever\b | and\s+stuff\b
)""", re.I | re.X)

# Item 5. Every sentence whose subject is the person on camera. The rewrite test is the
# judgement - write the same sentence about the viewer, and cut it when there is not one -
# so this surfaces the sentence and never proposes a span.
SPEAKER = re.compile(r"^\W*(i|i'?(m|ve|ll|d)|my|me|we\s+(actually|really)?\s*(do\s+)?have)\b", re.I)


def content(sentence):
    return {w for w in re.findall(r"[a-z']+", sentence.lower()) if w not in STOP and len(w) > 2}


def sentences(blocks):
    """(block index, char offset in block, text) for every sentence in the live script."""
    out = []
    for bi, text in enumerate(blocks):
        at = 0
        for part in re.split(r"(?<=[.?!])\s+|\n", text):
            if part.strip():
                out.append((bi, text.find(part, at), part.strip()))
                at = text.find(part, at) + len(part)
    return out


def find(blocks):
    sents = sentences(blocks)
    out, paired = [], set()

    for i, (bi, at, s) in enumerate(sents):
        a = content(s)
        if len(a) < MIN_CONTENT:
            continue
        for j in range(i + 1, min(i + 1 + WINDOW, len(sents))):
            bj, atj, t = sents[j]
            b = content(t)
            if len(b) < MIN_CONTENT or j in paired:
                continue
            shared = a & b
            if len(shared) / min(len(a), len(b)) >= OVERLAP:
                paired.add(j)
                out.append({"kind": "restate", "b": bj, "at": atj, "t": t,
                            "echo": s[:70], "shared": " ".join(sorted(shared))})
                break

    for bi, at, s in sents:
        for kind, rx in (("announce", ANNOUNCE), ("hedge", HEDGE)):
            m = rx.search(s)
            if m:
                out.append({"kind": kind, "b": bi, "at": at + m.start(),
                            "t": s if kind == "announce" else m.group(0), "echo": "", "shared": ""})
        if SPEAKER.match(s):
            out.append({"kind": "speaker", "b": bi, "at": at, "t": s, "echo": "", "shared": ""})

    seen, kept = set(), []
    for c in sorted(out, key=lambda c: (c["b"], c["at"], c["kind"])):
        key = (c["b"], c["at"], c["kind"])
        if key in seen:
            continue
        seen.add(key)
        kept.append(c)
    return kept


def live(path, comp=None):
    raw = json.load(open(path))
    if isinstance(raw, list):
        return [b if isinstance(b, str) else b.get("text", "") for b in raw]
    comps = raw["compositions"]
    c = next((x for x in comps if comp in (x["id"], x["name"])), comps[0]) if comp else comps[0]
    return [t["text"]["string"] for t in c["timeline"]["superTau"]["taus"] if not t.get("isBlocked")]


def main():
    argv = sys.argv[1:]
    args = [a for a in argv if not a.startswith("--")]
    comp = argv[argv.index("--comp") + 1] if "--comp" in argv else None
    if comp in args:
        args.remove(comp)
    blocks = live(args[0], comp)
    cands = find(blocks)
    chars = sum(len(b) for b in blocks)

    if "--check" in argv:
        needles = [schema.needle_text(n) for n in schema.load(args[1], "needles")]
        joined = " ".join(needles)
        missed = [c for c in cands
                  if not any(c["t"][:24] in n or n[:24] in c["t"] for n in needles)
                  and c["t"][:24] not in joined]
        for c in missed:
            print(f"UNCOVERED b{c['b']} {c['kind']}: {c['t'][:110]!r}")
        cut = sum(len(n) for n in needles if any(n in b for b in blocks))
        print(f"\n{len(cands)} pass-2 candidates, {len(missed)} uncovered")
        print(f"cut list removes {cut} of {chars} chars = {100 * cut / chars:.1f}%")
        return 1 if missed else 0

    for c in cands:
        line = f"b{c['b']:<4} {c['kind']:<9} {c['t'][:100]!r}"
        if c["echo"]:
            line += f"\n{'':16}echoes {c['echo']!r} on: {c['shared']}"
        print(line)
    print(f"\n{len(cands)} pass-2 candidates over {chars} chars", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
