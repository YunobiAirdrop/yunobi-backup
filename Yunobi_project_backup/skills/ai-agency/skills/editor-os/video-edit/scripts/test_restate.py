#!/usr/bin/env python3
"""Prove the pass-2 candidates. usage: test_restate.py

The author, 8 Sep 2026, reading a cut that had had pass 1 and nothing else: "Can you just strike through
digressions for example? Here I've repeated myself twice." The pair he found is CASES[0], and it is
the shape no phrase list catches: two clean sentences, different words, one idea. The other three
kinds are phrase lists and are here so a rewrite of the regexes cannot quietly drop one.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import restate


# (blocks, kind that must be reported, text the reported candidate must start with)
CASES = [
    # His own pair. The second sentence is the candidate; the first is what it echoes.
    (
        ["here I've connected my Google Drive account. I have also connected my Gmail, so it's "
         "capable of searching as well inside of Google Drive and Gmail. ",
         "you could also give it the capacity to look into your Gmail, into your Google Drive, "
         "to search the web, and to interact with any other app that would give it useful context."],
        "restate",
        "you could also give it the capacity",
    ),
    # Item 1: the video announcing itself.
    (["In this video, I'm gonna show you how you can make these tools talk to each other."],
     "announce", "In this video"),
    # Item 3: the speaker's reaction standing in for a reason.
    (["it's even generated a few images. It's pretty cool. We have, like, some placeholders."],
     "hedge", "It's pretty cool"),
    # Item 5: the subject is the person on camera.
    (["I've created my own MCPs for my agency to manage parts of my business."],
     "speaker", "I've created my own MCPs"),
]

# Deliberate speech that must NOT come back as a restatement. Anaphora is the classic: the same
# opening is the rhetoric, not a second utterance.
DISMISSED = [
    ["You don't know how to deal with them.",
     "You don't know how to deal with that influx of work."],
]


def main():
    bad = 0
    for blocks, kind, starts in CASES:
        hits = [c for c in restate.find(blocks) if c["kind"] == kind]
        if not any(c["t"].startswith(starts) for c in hits):
            bad += 1
            print(f"MISS {kind}: {starts!r} not in {[c['t'][:50] for c in hits]}")
    for blocks in DISMISSED:
        hits = [c for c in restate.find(blocks) if c["kind"] == "restate"]
        if hits:
            bad += 1
            print(f"FALSE restate: {[c['t'][:60] for c in hits]}")
    print("FAIL" if bad else f"ok, {len(CASES)} kinds and {len(DISMISSED)} dismissals")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
