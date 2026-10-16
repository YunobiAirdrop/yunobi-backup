#!/usr/bin/env python3
"""Measure a raw take, before anything is cut.

Every number the coaching report prints comes from here or from the app API.
Nothing is estimated, because a coaching note built on a guess is unfalsifiable
and the ledger cannot test it on the next recording.

Usage:
    python3 take-stats.py transcript.txt --duration 1767 > stats.json
    python3 take-stats.py blocks.json    --duration 1767   # a JSON array of strings

`--duration` is the composition duration in seconds from `get_project`. Without
it the pace and the cost-in-seconds numbers are omitted rather than invented.
"""
import argparse
import json
import re
import sys

# A restart lands within this many characters of the attempt it is redoing.
# Same window as descript-script-edit's candidates.py, deliberately: the two
# skills must agree on what counts as a retake or the cut list and the coaching
# note will report different totals for the same take.
WINDOW = 400
SHINGLE = 3

TRUNCATION = re.compile(r"\S*(?:--|\.\.\.)(?=\s|$)|\b[A-Za-z]{1,3}-(?=\s)")

# Spoken fillers only. "So" and "Now" open legitimate sentences in this register
# and are not counted; counting them turns every take into a filler problem.
FILLERS = [
    "um", "uh", "erm", "you know", "i mean", "kind of", "sort of",
    "basically", "actually", "obviously", "literally", "right?",
]

# An ask that sends the viewer out of the video. In-platform asks are listed
# separately because the ask rule allows those early and only ever counts these.
#
# These are CANDIDATES, not verdicts. "they go to sales" matched a bare "go to"
# on the first take this ran against, at 10% of runtime, which would have failed
# D1 for a sentence that asks nobody for anything. The phrases are kept narrow
# for that reason and step 6 still reads each hit in context before judging it.
OUTBOUND = [
    "link in the description", "link in the bio", "link below", "down below",
    "in the description", "go get", "go grab", "head to", "book a call",
    "book a discovery", "sign up", "check out the link", "join the",
]
IN_PLATFORM = ["subscribe", "hit like", "leave a comment", "smash that"]

# D9, the first-person count. "us" is deliberately absent: it collides with "the
# US" in a corpus that quotes US billable rates, and no take has ever turned on it.
FIRST_PERSON = re.compile(
    r"\b(i|i'm|i'll|i've|i'd|me|my|mine|myself|we|we're|we'll|we've|we'd|our|ours)\b")
SECOND_PERSON = re.compile(r"\b(you|you're|you'll|you've|you'd|your|yours|yourself|yourselves)\b")


def load(path):
    raw = open(path).read()
    if path.endswith(".json"):
        blocks = json.loads(raw)
        return [b if isinstance(b, str) else b.get("text", "") for b in blocks]
    return [ln for ln in raw.split("\n") if ln.strip()]


def words(text):
    return [(m.group(0).lower().strip(".,!?\"'"), m.start())
            for m in re.finditer(r"\S+", text)]


def repeats(text):
    """Spans from a first attempt to its last restart, merged.

    Three attempts at one sentence are one span, not three, because that is how
    the edit will remove them and the seconds have to match.
    """
    ws = words(text)
    seen, spans = {}, []
    for i in range(len(ws) - SHINGLE + 1):
        key = tuple(w for w, _ in ws[i:i + SHINGLE])
        start = ws[i][1]
        prev = seen.get(key)
        if prev is not None and start - prev < WINDOW:
            end = ws[min(i + SHINGLE, len(ws)) - 1][1] + len(ws[min(i + SHINGLE, len(ws)) - 1][0])
            if spans and start <= spans[-1][1] + WINDOW:
                spans[-1] = (spans[-1][0], max(spans[-1][1], end))
            else:
                spans.append((prev, end))
        seen[key] = start
    return spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--duration", type=float, default=None,
                    help="composition duration in seconds, from get_project")
    args = ap.parse_args()

    blocks = load(args.path)
    full = "\n".join(blocks)
    # Measured on the joined string, not on the sum of block lengths: the ask
    # offsets are indexes into `full`, and mixing the two put an ask at 100.3%
    # of runtime the first time this ran.
    total_chars = len(full)
    total_words = len(re.findall(r"\S+", full))

    per_block, waste_chars = [], 0
    for i, b in enumerate(blocks):
        spans = repeats(b)
        trunc = TRUNCATION.findall(b)
        cost = sum(e - s for s, e in spans)
        waste_chars += cost
        if spans or trunc:
            per_block.append({
                "block": i,
                "restarts": len(spans),
                "truncations": len(trunc),
                "wasteChars": cost,
                "opens": b[:90],
            })

    low = full.lower().replace("\u2019", "'")

    # Every hit carries the sentence it sits in, because D9 is answered by
    # rewriting that sentence in the second person, never by the count alone.
    def sentence_at(i):
        start = max(low.rfind(".", 0, i), low.rfind("\n", 0, i)) + 1
        end = min([x for x in (low.find(".", i), low.find("\n", i)) if x != -1]
                  or [len(low)])
        return full[start:end + 1].strip()[:160]

    first_hits = [{"word": m.group(0), "atChar": m.start(),
                   "atFraction": round(m.start() / max(total_chars, 1), 4),
                   "sentence": sentence_at(m.start())}
                  for m in FIRST_PERSON.finditer(low)]
    second_total = len(SECOND_PERSON.findall(low))
    filler_counts = {f: len(re.findall(r"\b" + re.escape(f), low)) for f in FILLERS}
    filler_total = sum(filler_counts.values())

    def asks(terms):
        out = []
        for t in terms:
            for m in re.finditer(re.escape(t), low):
                out.append({"phrase": t, "atChar": m.start(),
                            "atFraction": round(m.start() / max(total_chars, 1), 4)})
        return sorted(out, key=lambda a: a["atChar"])

    stats = {
        "blocks": len(blocks),
        "chars": total_chars,
        "words": total_words,
        # The raw count double-counts every restart, so it is never the number
        # judged against the 3,600-4,200 budget. See checks.md D7.
        "deliveredWords": total_words - int(total_words * waste_chars / max(total_chars, 1)),
        "restartSpans": sum(x["restarts"] for x in per_block),
        "truncations": sum(x["truncations"] for x in per_block),
        "wasteChars": waste_chars,
        "wasteRatio": round(waste_chars / max(total_chars, 1), 4),
        "fillerTotal": filler_total,
        "fillerPer1000Words": round(1000 * filler_total / max(total_words, 1), 1),
        "fillers": {k: v for k, v in sorted(filler_counts.items(), key=lambda kv: -kv[1]) if v},
        # D9. The target is zero. A survivor has to do one of four named jobs,
        # which is a judgement the report makes with the sentence in front of it.
        "firstPerson": len(first_hits),
        "secondPerson": second_total,
        "firstPersonHits": first_hits[:15],
        # The open is the first 30 seconds of a long-form take. On a Short that is
        # most of the video, so the window is capped at the first fifth of it and
        # the check falls back to the opening sentence.
        "firstPersonInOpen": [
            h for h in first_hits
            if h["atFraction"] <= (min(0.2, 30.0 / args.duration) if args.duration else 0.02)
        ],
        "outboundAsks": asks(OUTBOUND),
        "inPlatformAsks": asks(IN_PLATFORM),
        "worstBlocks": sorted(per_block, key=lambda x: -x["wasteChars"])[:5],
    }

    if args.duration:
        stats["durationSeconds"] = args.duration
        stats["wordsPerMinute"] = round(total_words / (args.duration / 60), 1)
        cps = total_chars / args.duration
        stats["wasteSeconds"] = round(waste_chars / cps, 1)

    json.dump(stats, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
