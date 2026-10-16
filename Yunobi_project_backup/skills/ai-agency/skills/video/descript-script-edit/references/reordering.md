# Reordering: keep the best take, not the last one

A video recorded intro-twice / outro-twice has its best pieces scattered, and cutting alone leaves
the pain the speaker recorded second sitting after the promise it was meant to set up.
`scripts/arrange.py` takes an **order**: a list of token spans that must tile the whole script
exactly once, and emits the TAUs in that order.

```bash
echo '[[0,166],[461,641],[287,320],[166,287],[320,461],[641,5970]]' > order.json
python3 scripts/arrange.py cuts.json order.json --typos t.json --markers m.json \
                          --styles s.json --pins p.json --write
```

Each TAU carries its own `audioSegment`, so a non-monotonic offset is legal and the picture follows
the words. Cuts still ship as Ignore and a moved span carries its own ignored attempts with it, so
the retakes stay beside the take that beat them. Three refusals guard it: an order that does not
tile `[0, n)`, a span edge that falls inside a segment, and segments that do not reconstruct the
source text. Durations are computed in **spoken** order before the reorder, or a moved span borrows
its neighbour's clock.

The move to look for first is a **second pain recorded after the promise**. Stack the pains, then
promise once: hook, pain, pain, the bet, promise, close. Verified 2026-08-24 on a 40-minute CRM
build, 40:11 -> 29:48, with the profitability pain lifted 300 seconds earlier.

`--styles` paints the **cue legend** the editor reads: blue for b-roll, purple for a diagram drawn
on a transparent layer, green for on-screen text, orange for a CTA. That is the point of the whole
exercise - one paste hands the editor a script already cut, de-filled, spell-corrected and marked
up with where every asset goes.

When something goes wrong, nothing is lost. Every payload seen or written is archived:

```bash
python3 $D history                      # newest first
python3 $D restore 20260820-150802-grab-lesson-1   # that state back on the clipboard, then paste
```

Read [`references/pasteboard.md`](pasteboard.md) before the first run; every trap in it
was paid for.
