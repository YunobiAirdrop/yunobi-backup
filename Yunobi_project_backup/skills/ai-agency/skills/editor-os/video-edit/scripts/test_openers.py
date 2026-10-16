#!/usr/bin/env python3
"""Prove the sentence-opening filler rule. usage: test_openers.py

The author, 2 Sep 2026: "you always forget to remove 'now' and 'so' - when they start a sentence,
it's often fillers that we need to remove." The rule is POSITIONAL, which is what makes it worth
a test of its own: the same word is a throat-clear at a sentence start and load-bearing three
words later, and a set like `FILLERS` cannot tell the two apart.

Every case below is a real line, taken off EC49 or the sandbox take.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recut2


def toks_for(text):
    """One TAU holding `text`, and the token list `opener_cuts` walks."""
    taus = [{"text": {"string": text}}]
    return taus, recut2.copy_tokens(taus)


def cut_words(text):
    """Everything the filler pass would take: phrases first, then the single-word openers."""
    taus, toks = toks_for(text)
    phrased, _ = recut2.phrase_cuts(taus, toks)
    taken = {i for c in phrased for i in range(c["start"], c["end"])}
    opened, _ = recut2.opener_cuts(taus, toks, taken)
    return [c["text"] for c in sorted(phrased + opened, key=lambda c: c["start"])]


def rewritten(text):
    """The text with the openers and phrases dropped, as the rebuild would leave it."""
    taus, toks = toks_for(text)
    cuts, caps = recut2.phrase_cuts(taus, toks)
    taken = {i for c in cuts for i in range(c["start"], c["end"])}
    opened, ocaps = recut2.opener_cuts(taus, toks, taken)
    cuts = cuts + opened
    caps = caps | ocaps
    # A cut is a RANGE, not a token: a phrase spans five or six of them.
    gone = {i for c in cuts for i in range(c["start"], c["end"])}
    out = []
    for i, t in enumerate(toks):
        if i in gone:
            continue
        w = t[3]
        if i in caps and w and w[0].islower():
            w = w[0].upper() + w[1:]
        out.append(w)
    return " ".join(out)


CUT = [
    # (line, what should be cut)
    ("So anything in ClickUp is a task.", ["So"]),
    ("Now, systems are built upon templates and processes.", ["Now,"]),
    ("Now let's take the example of a design agency.", ["Now"]),
    ("So he spent his nights fixing the mistakes. Now who is it for?", ["So", "Now"]),
    # A paragraph break inside one TAU opens a sentence just as a full stop does.
    ("It ships today.\nSo the team can see it.", ["So"]),
    # "So that's" is the opener plus a contraction, NOT the "so that" subordinator.
    ("So that's the first thing you need to fix.", ["So"]),
]

PHRASES = [
    # The real line, off EC49 - The author cut it by hand, then: "make sure we cut this off every time
    # I say this. This is a filler."
    ("And what that means is that you're gonna be able to trigger those.",
     ["And what that means is that"],
     "You're gonna be able to trigger those."),
    # Without the leading "and", and without the trailing "that".
    ("What that means is you need a system.", ["What that means is"], "You need a system."),
    # NESTING: the longest phrase wins, or a stranded "that" opens the sentence.
    ("And what that means is that it works.", ["And what that means is that"], "It works."),
    # The other half of the family, and his real line: "what this does is it filters out..."
    ("What this does is it filters out the tasks where I have to intervene.",
     ["What this does is"], "It filters out the tasks where I have to intervene."),
    # Same family, other subject and verb - generated, so these come free.
    ("And what it does is that it saves you a week.", ["And what it does is that"],
     "It saves you a week."),
    # Mid-sentence it still goes, and the next word is NOT promoted - it opens nothing.
    ("The board is clean and what that means is you can see it.",
     ["and what that means is"], "The board is clean you can see it."),
]

KEEP = [
    # Mid-sentence, where the word is doing its job. This is the whole reason it is not in FILLERS.
    "It costs more, so I built it myself.",
    "The board is clean now, and the team can see it.",
    # The subordinator: cutting the opener here leaves a fragment.
    "So that you can see it, I put it on one board.",
    "Now that the board is clean, the team can see it.",
    # Nothing follows it, so there is nothing to promote to sentence start.
    "So",
]

REWRITE = [
    ("Now, systems are built upon templates.", "Systems are built upon templates."),
    ("So that's what Agency Master is about.", "That's what Agency Master is about."),
    ("Now it's your choice, it's your decision.", "It's your choice, it's your decision."),
]


def main():
    fails = []

    for line, want in CUT:
        got = cut_words(line)
        if got != want:
            fails.append("cut %r -> %r, wanted %r" % (line, got, want))

    for line in KEEP:
        got = cut_words(line)
        if got:
            fails.append("kept nothing in %r - it cut %r" % (line, got))

    for line, cut, want in PHRASES:
        got = cut_words(line)
        if got != cut:
            fails.append("phrase %r -> cut %r, wanted %r" % (line, got, cut))
        got = rewritten(line)
        if got != want:
            fails.append("phrase %r -> %r, wanted %r" % (line, got, want))

    for line, want in REWRITE:
        got = rewritten(line)
        if got != want:
            fails.append("rewrote %r -> %r, wanted %r" % (line, got, want))

    if fails:
        print("FAIL test_openers\n     - %s" % "\n     - ".join(fails))
        return 1
    print("PASS test_openers  %d cut, %d kept, %d rewritten, %d phrases"
          % (len(CUT), len(KEEP), len(REWRITE), len(PHRASES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
