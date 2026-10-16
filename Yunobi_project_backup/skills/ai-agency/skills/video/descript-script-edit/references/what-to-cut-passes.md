# The two passes, and the ratio gate

Two passes, and the second one is the one that gets skipped. Pass 1 removes the wreckage of
speaking: stutters, restarts, duplicate takes, enumerated mechanically so it does not depend on an
agent noticing things. Pass 2 removes complete, well-formed sentences that carry nothing -
announcements of what the next sentence will say, a second utterance of one idea in new words,
hedges, digressions, and every sentence whose subject is the speaker. A run that does only pass 1 leaves a script with no stutters in it that is
still bloated, which is what M0 L1 shipped as on 2026-08-14: 29 needles, every one of them pass 1.

```bash
python3 scripts/candidates.py blocks.json                       # pass 1 candidates
python3 scripts/candidates.py blocks.json --check needles.json  # uncovered, and the cut ratio
```

**Every mechanical candidate is a needle or a named dismissal, and every sentence faces one test:
delete it, read its two neighbours together, name what the viewer lost.** Nothing lost is a cut.
The ratio is the second gate - a first-take lesson gives up 14-20% of its characters to pass 1 and
22-30% to both. Below that is under-listed, not a clean take.

**Read [`references/what-to-cut.md`](what-to-cut.md) before writing the cut list** - both
passes worked through, the dismissals that look like repeats and are not, the full ratio table.

**Read [`references/what-to-cut.md`](what-to-cut.md) before writing the cut list** - both
passes worked through, the dismissals that look like repeats and are not, the full ratio table.

**Pass 3 is the silence, and no transcript can list it.** `candidates.py` reads the words, so the
two-second hole between two clean sentences is invisible to it - nothing in the document records
one. The audio does, and ffmpeg reads it for free:

```bash
python3 scripts/silences.py calibrate <export.mp4> doc.json "<comp>"   # the threshold this room wants
python3 scripts/silences.py deadair   <export.mp4> doc.json "<comp>" --keep 0.35
```

`--keep` is the style dial: how much pause survives a cut. It runs on the RENDERED composition,
because a tau's offset addresses whatever media it was cut from and in a real project that is a
sequence, while the export is the play clock every anchor already counts on. `calibrate` refuses on
duration before it measures anything, so a stale render cannot be timed against. On the Mini-Course
Intro, a video already tightened by hand, it found 51 pauses over the keep and 7.1s of 171.3s.

Expect the composition to shorten by more than the characters predict: Ignore takes the pause
attached to the words with it. M2 L4 lost 1 895 characters and 252 seconds on 2026-08-15, because
the abandoned takes each sat in their own silence.

Building the cut list from the live DOM rather than the export is in
[references/cut-list.md](cut-list.md).
