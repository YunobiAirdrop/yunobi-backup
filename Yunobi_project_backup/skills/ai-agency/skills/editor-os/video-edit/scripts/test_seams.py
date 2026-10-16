#!/usr/bin/env python3
"""Prove the seam rules and the cut spec. usage: test_seams.py

The flagged cases are real joins a worker shipped on 23 Sep 2026.
"""
import os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from seams import bad
import cutspec

FLAGGED = [
    # a list item cut as if it were a retake
    ("to use the right model. So Opus, so Opus is", "when someone has to think, Sonnet when someone has to draft something, and Haiku",
     "when someone has to do 200 mini tasks"),
    # attempt 1's head on attempt 2's tail
    ("So you", "need to think\nSo you really", "need to think of AI as"),
    # a stub left live
    ("Whereas ChatGPT or Glo--", "in between", "It is focused on"),
]
CLEAN = [
    ("that's gonna fill up your session before you even type anything.", "If you start in a fresh session", "If you start a fresh Claude session,"),
    ("you're gonna be limited", "pretty,", "pretty quickly."),                  # filler-free restart, one word
    ("I haven't put,", "uh,", "Fable here"),                                    # filler
    ("to the one that has full context", "to the one that has full context get--", "to the one that has full context ready"),
]


def main():
    fails = 0
    for left, cut, right in FLAGGED:
        if not bad(left, cut, right):
            print(f"FAIL not flagged: …{left[-30:]!r} | {right[:30]!r}")
            fails += 1
    for left, cut, right in CLEAN:
        if left.endswith("limited"):
            continue  # a one-word restart is flagged on purpose: read it
        if bad(left, cut, right):
            print(f"FAIL flagged: …{left[-30:]!r} | {right[:30]!r}")
            fails += 1

    raw = "It's got three places that the version was wrong, and our tension didn't resolve.\nNext line"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("1 | , and our tension .. $\n")
    (a, b, _), = cutspec.resolve(raw, f.name)
    if raw[a - 7:a] != "wrong, " or not raw[a:].startswith("and our"):
        print(f"FAIL a cut opening on a comma must start after it: {raw[a - 7:a + 8]!r}")
        fails += 1
    print("ok" if not fails else f"{fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
