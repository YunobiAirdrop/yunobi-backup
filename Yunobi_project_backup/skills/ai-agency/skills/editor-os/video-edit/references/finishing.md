# Finishing a cut: reorder, close the air, and the final export check

Reordering sections, then measuring dead air, then the checklist every export ships with. Which attempt at a sentence survives is a different question with one answer: [`what-to-cut.md`](what-to-cut.md).

## Reordering: put the sections in the order that plays, not the order recorded

This is about WHERE a whole section lands. A video recorded intro-twice / outro-twice has its best pieces scattered, and cutting alone leaves
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

Read [`pasteboard.md`](pasteboard.md) before the first run; every trap in it was paid for.

## The silence gate: measure the export, do not trust the cut ratio

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
the cut list is looking for it. When the export misses the gate, the fix is `pnpm descript gaps
close <project> <comp> --over 1`: the app's own gap-shortener, which splits the paragraph either
side of the pause and keeps 0.3s on each side.

**Pass `--edges` on a finished cut, or the longest holes stay.** A pause that ends on a cut carries
`kept: "borders a cut"` and `close` leaves it, so `restore` gets its two slices back contiguous.
That protection is what a viewer hears: the camera keeps rolling where a take was removed, so those
gaps are the longest in the video. FC38 (2026-09-10) held a 21.0s and a 14.4s one, and a plain
`close` recovered 5.5s of internal silence and reported success; `--over 0.7 --keep 0.3 --edges`
took its 20 pauses to none and 89.3s out of a 25-minute cut. Read the `kept` column of `gaps` before
believing a `saved` figure. `unmatched word` stays protected either way - there is no character to
split at - and the price of `--edges` is that a later `restore` comes back beside a hole.

## The final export check

Run this on every video before you export.

```bash
pnpm descript settings <project> [composition]    # every setting, then the gate
pnpm descript settings after.json                 # or a document saved by `doc --out`
```

Points 1 to 13 below read straight off the project, so the command prints them, then the faults,
and it exits red while one is left. 14 to 16 are yours.

### The audio

Select All scenes, every time. Not one scene: set this per scene and you'll fix the same thing 4
times and still miss the 5th.

1. Studio Sound: on, 50%. Go to 60-70% only if the words sound muffled. Above that the voice
   starts sounding like a phone call, which is worse than the room noise you were killing.
2. Lower other audio: on, Volume 10%.
3. Word gaps: everything over 0.7s comes down to 0.3s.
4. One track is live, and it's the microphone. Every other track muted and taken out of the
   script. A muted track that's still in the script is the one that comes back at export.

### The face

The same numbers on CAM and on CAM GS, on every card. This is the one people get wrong, and it's
not their fault: Descript shows you one layer's panel at a time, so a card can look perfect while
the card before it carries a default nobody ever touched. The CRM cut read fine on every card its
editor clicked and was still carrying Descript's default Uplighting on four of them.

5. Uplighting: Strength 10%, Foreground brightness 50%, Background brightness 0%.
6. Skin smoothing: 10%.
7. Blur speaker background: the same value on every card.
8. Color adjustments: None. A grade belongs to the shoot. Left on one card, it's the fault a
   viewer reads as "that shot looks different" without being able to say why.
9. Green screen: on for CAM GS, off for CAM. Never both, never neither.

### The green screen stack

`CAM GS` is the camera, keyed: same take, same clock, background removed. That's what puts a shape
behind the speaker.

10. Order: CAM GS on top, the text or the shape under it, CAM at the back (Layer order > Send
    to back). Index 0 is nearest the viewer, which is why the keyed twin carries the smallest one.
11. CAM GS sits in the same box as CAM. Copy CAM, then Paste attributes onto CAM GS. Don't
    eyeball it, you'll be a few pixels out and the face jumps on the cut. Without the clipboard:
    `pnpm descript layer copy <p> <comp> <card> <layer> --to all`.
12. No leftover duplicate camera layers on a card. A restamp switches the old camera off and
    leaves it there, so a card restamped 3 times carries 3, and the one you can't see is the one
    that comes back.

The twin also has to sit on CAM's clock to half a frame. That gate is `tracks`, and the repair is
`track shift <project> "CAM GS" --to CAM`. See [`audio-and-tracks.md`](audio-and-tracks.md).

### The frame and the finish

13. Project frame is 1920x1080 or larger. Under that, every title and layout is drawn small
    and the export upscales it.
14. Smart transition in and out wherever the shot changes.
15. Names spelled right in every title and caption: ClickUp, Brand, the author.
16. Watch the whole video once, with sound, before you export. Yes, the whole thing.

### Each number, and where it lives in the document

| Setting | Where in the app | The value | In the document |
| --- | --- | --- | --- |
| Studio Sound | All scenes > Audio effects | on, **50%** | `mediaRefs[].audio.speechEnhanceEnabled` + `studioSoundIntensity` |
| Lower other audio | All scenes > Audio effects | on, Volume **10%** | `compositions[].duckingParameters.gainReductionAmount` |
| Shorten word gaps | Underlord | applied, over 0.7s down to 0.3s | `compositions[].features.shorten_word_gaps` |
| Uplighting | Properties > Visual effects | Strength **10%**, Foreground brightness **50%**, Background brightness **0%** | `com.descript.uplighting`, the first 3 numbers |
| Skin smoothing | Properties > Visual effects | **10%** | `com.descript.skinSmoothing[0]` |
| Blur speaker background | Properties > Visual effects | one reading on every card | `com.descript.backgroundBlur[0]` |
| Color adjustments | Properties > Color adjustments | None | `com.descript.colorAdjustments`, 9 zeros |
| Green screen | Properties > Visual effects | on for `CAM GS`, off for `CAM` | `com.descript.backgroundRemoval` |
| Layer order | Layer order > Send to back | twin, graphic, camera | `cards[].layers[]`, index 0 nearest the viewer |
| Frame | Project settings | 1920x1080 or larger | `compositions[].videoMetadata` |

The author set the numbers on camera, 18 Sep 2026, walking an editor through the green screen: *"you
want to put maybe 50% of studio sound, otherwise it looks weird"*, *"lower other audio so that the
other tracks are not too loud"*, and *"the green screen and the regular screen always have the same
settings of uplighting and skin smoothing... I put 10%, then here I put 50%, and then here zero
background brightness"*.

**Shadow, Border and the corner radius are not on the list on purpose.** They belong to the layout
- a shadow falls from an inset clip and from nothing else - so the gate prints them and holds them
to nothing.

**A percentage is a number. It isn't a taste.** That's why a single b-roll clip sitting at 70% Studio
Sound is a fault and not a rounding difference. Half the cards differing on one look row is exactly
the state a human eye reads as "the face flickers", so the gate compares the twins card by card.

### What the command can't see, and you still check

- The key itself. A clean edge on a busy frame is a look, and no number reads it.
- The captions, the chapters and the end card.
- The cut: [descript-script-edit.md](descript-script-edit.md)'s own checks own the script, the gaps and the dressing.

### The repairs, one line each

```bash
pnpm descript studio <p> <track|media> --on --intensity 0.5      # Studio Sound
pnpm descript gaps close <p> <comp> --over 0.7 --keep 0.3 --edges
pnpm descript layer effect <p> <comp> <card> <layer> uplighting --value "[0.1,0.5,0,0.05,-0.05,0]"
pnpm descript layer copy <p> <comp> <card> <layer> --to all      # one look onto every card
pnpm descript layer set <p> <comp> <card> <layer> --to 0         # the stack, 0 is the top
pnpm descript layer sweep <p> <comp>                             # the hidden duplicate cameras
pnpm descript resize <p> <comp> 1920x1080                        # the canvas
pnpm descript track mute <p> <track>                             # leave one live track
```

Lower other audio has no verb: it's one control on All scenes in the app, and it's set once per
composition.
