#!/usr/bin/env python3
"""Prove the digression candidate and the last-retake rule. usage: test_candidates.py

The author, 2 Sep 2026: "when I say 'you could potentially' it's often the digression, this needs to be
cut." He cut that one by hand; this is so the next one is impossible to miss.

IT IS A CANDIDATE, NOT A CUT, and the two cases below are why. The marker is a signpost to a span
whose end nothing in the text marks: one of his ran into a truncation, the other ran a full sentence
and into the next. `--check` exits 1 while the cut list does not cover it, so it gets decided every
time without a guessed span deleting real teaching.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import candidates


# (block, expected candidate kinds, expected digression span)
CASES = [
    # His own line, cut by hand. The span stops at the truncation, not at the far full stop.
    (
        "You could potentially add another custom field with their email address, for example, "
        "or you could add your-- Anyway, the point is the board stays clean.",
        "You could potentially add another custom field with their email address, for example, "
        "or you could add your--",
    ),
    # The one still live in EC49. No truncation, so the sentence bounds it - and it must NOT run on
    # into the sentence after.
    (
        "On the right, the process for it. You could potentially add another custom field with "
        "their email address, for example, their track record here in the comments. So each time "
        "you open it you see the history.",
        "You could potentially add another custom field with their email address, for example, "
        "their track record here in the comments.",
    ),
]

# The word alone is not the marker. Cutting on "potentially" would take the sentence that uses it.
KEEP = [
    "The board is clean, and that is potentially the whole point.",
    "You could add a custom field for that.",
]

# FC38's opening, verbatim, as five paragraphs. Four attempts at one sentence, and the pause the
# speaker took to start again is exactly where Descript broke the paragraph - so a per-block search
# found NOTHING here and the shipped edit kept attempt 2's head on attempt 4's tail. The author,
# 11 Sep 2026: "it never takes the last retake ... always use the last retake."
RETAKE = [
    "Si vous demarrez sur ClickUp",
    "Si vous demarrez sur ClickUp ou que vous voulez",
    "Si vous demarrez sur ClickUp Si vous",
    "demarrez sur ClickUp ou que vous voulez",
    "utiliser plus de fonctionnalites",
]
# What has to survive: the last attempt, whole and unspliced.
RETAKE_KEEP = "Si vous demarrez sur ClickUp ou que vous voulez utiliser plus de fonctionnalites"

# The cut list that shipped: it took the first attempt and the third, and left the second standing
# between them. `--check` has to call that uncovered.
SHIPPED = [
    "Si vous demarrez sur ClickUp",
    "Si vous demarrez sur ClickUp Si vous",
    "demarrez sur ClickUp ou que vous voulez",
]


def retakes(fails):
    got = [c for c in candidates.find(RETAKE) if c["kind"] == "repeat"]
    if len(got) != 1:
        fails.append("expected one repeat over the FC38 opening, got %d" % len(got))
        return
    c = got[0]
    text, _ = candidates.joined(RETAKE)
    if not text[c["g"] + len(c["t"]):].startswith(RETAKE_KEEP):
        fails.append("the span keeps %r\n       wanted %r"
                     % (text[c["g"] + len(c["t"]):][:80], RETAKE_KEEP))
    if [s[0] for s in c["slices"]] != [0, 1, 2]:
        fails.append("the cut spans blocks %s, wanted [0, 1, 2]" % [s[0] for s in c["slices"]])
    if not candidates.live(c, RETAKE, candidates.masks(RETAKE, SHIPPED)):
        fails.append("the shipped cut list read as covered; it leaves attempt 2 standing")
    whole = [RETAKE[0], RETAKE[1], "Si vous demarrez sur ClickUp Si vous"]
    if candidates.live(c, RETAKE, candidates.masks(RETAKE, whole)):
        fails.append("a cut list that removes every earlier attempt read as uncovered")


def main():
    fails = []
    retakes(fails)

    for text, want in CASES:
        got = [c for c in candidates.find([text]) if c["kind"] == "digression"]
        if len(got) != 1:
            fails.append("expected one digression in %r, got %d" % (text[:48], len(got)))
            continue
        if got[0]["t"] != want:
            fails.append("span %r\n       wanted %r" % (got[0]["t"], want))

    for text in KEEP:
        got = [c for c in candidates.find([text]) if c["kind"] == "digression"]
        if got:
            fails.append("flagged a digression in %r: %r" % (text[:48], got[0]["t"]))

    if fails:
        print("FAIL test_candidates\n     - %s" % "\n     - ".join(fails))
        return 1
    print("PASS test_candidates  %d digressions bounded, %d left alone, last retake kept"
          % (len(CASES), len(KEEP)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
