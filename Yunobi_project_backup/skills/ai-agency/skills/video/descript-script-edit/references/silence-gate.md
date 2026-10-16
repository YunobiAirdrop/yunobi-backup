# The silence gate: measure the export, do not trust the cut ratio

The character ratio says the words came out. It says nothing about the **air between them**, and
air is where a tight edit is won. Measure it on the rendered file, never on the document:

```bash
python3 scripts/silences.py calibrate <export.mp4> doc.json "<comp>"   # the threshold this room wants
python3 scripts/silences.py deadair   <export.mp4> doc.json "<comp>" --keep 0.35
```

`calibrate` picks the threshold instead of assuming -32dB, because that number is a room and not a
constant, and it refuses on duration first so a stale render can never be measured. `deadair` gives
the **recoverable excess** over the pause the style keeps, per tau, at a timecode - which is a cut
list, where the total below is only a score. On the same two files it returns 7.1s of 171.3s and
73.0s of 1109.5s.

**The gate is 5% of runtime.** Above it the cut is not finished, whatever the character ratio says.

Measured 2026-08-27, on a competitor's edits against ours:

| Video | Runtime | Silence | Share |
|---|---|---|---|
| Competitor, founder VSL | 597s | 13s | **2.2%** |
| Competitor, client channel | 533s | 14s | **2.6%** |
| Ours, `00-intro` | 171s | 17s | 9.9% |
| Ours, `01-day-1` | 1110s | 83s | 7.5% |

83 seconds of dead air in an 18-minute lesson is a minute and a half of a viewer waiting. Ignore
takes the pause attached to its words, so pass 1 and pass 2 pull the ratio down on their own - but
only where a needle landed. What survives is the pause **inside** a kept sentence, and nothing in
the cut list is looking for it. When the export misses the gate, the fix is a third sweep over the
longest surviving silences, cut as Ignore through the same driver like any other needle.
