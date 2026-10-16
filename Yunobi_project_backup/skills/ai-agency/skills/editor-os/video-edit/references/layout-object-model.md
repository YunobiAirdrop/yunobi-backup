# What a layout IS: the object model, its sounds and its text

Application mechanics and what goes wrong mid-cut are in [`layout-pack.md`](layout-pack.md). This is the document shape underneath.

## A pin can be sound, drawn by no layer, and the sounds the pack carries

`sweepPins` used to call a pinned scene dead when no card layer drew it. The whoosh an "apply
layout" click brings is registered in the pins track and drawn by nothing, so a later restamp swept
both of the editor's own manual applies out of EC49. A scene is live when a layer draws it **or** the
pins track registers it; what a restamp retires is only the registrations belonging to the card it
replaced.

**One vocabulary, since 8 Sep 2026.** The pack's `Sounds/` folder and the drive library's `Sound Signature` folder used to hold vendor names (`Chime Light`, `Whoosh M`) while the app library and every skill called the same files `chime-soft`, `whoosh-mid`. Both now use the kit's names; media ids did not change, so every pin kept its sound and gain.

**31 sound pins, across 5 of the 9 sequences:** Camera 8, Text 16, Motion 4, Brand 2, Claude 1.
Screen, Shorts, B-roll and CTAs carry none - a card from those four arrives silent.

| what it plays | voice | pins |
| --- | --- | --- |
| a line of text arriving | `readout` | 13 |
| the whip | `whoosh` | 4 |
| the travel | `whoosh-deep` | 4 |
| the flicker | `shuffle` | 3 |
| the payoff | `chime-soft` | 2 |
| six seconds of wind a run of cuts happens inside | `swish` | 2 |
| the climb, a UI event, a mouse click | `riser`, `ui`, `mouse` | 1 each |

**Nine, down from thirteen on 8 Sep 2026.** The author: *"go down to under 10 sounds ... too many
effects to handle."* `chime` and `zoom` were census voices no card played; `whoosh-hi` and
`whoosh-mid` were the same instrument at two more lengths, repointed onto `whoosh-deep`. **A pin
moves to another file with `pnpm descript clip <project> <comp> <pin> --media <file>`** (not
`media swap`, which moves every pin of a file together); it refuses a file shorter than the pin
plays.

**All 31 sit at 100% since 8 Sep 2026, up from a scattered 22-58%.** The author, seeing a pin at 40%:
*"make sure all audios are 100%"*. Those numbers were never chosen: `audioSegment.gain` seeds from
the media's own `defaultGain`, so the panel was showing Descript's analysis, not an edit decision.
`pnpm descript clip <project> <comp> <pin> --gain` sets one. The media itself was NOT swapped for
the levelled kit files: those import with no `defaultGain` until Descript analyses them, and an
auto-level on an already-levelled file is the "file climbs back" trap. Gain is reversible; media is not.

**Every one of the 31 starts within 0.6s of its card, so the pack has no exit sound.** Twenty-three
sit at exactly 0 and the rest at 0.007-0.594s, a nudge and not a beat.

**The exit the text DOES have is a `tailTransition`.** Eleven text pins carry `tailTransition:
{duration: 0.2, effect: com.descript.textFlickerTransition}` and every one ENDS on the card
boundary, so the flicker follows the beat however long it is. A sound cannot follow it from a
pack: a pin sits at its card's start plus a fixed `offsetFromAnchor`, so a tail sound written into
the pack fires mid-beat on a long one and past the end of a short one.

**So the flicker's sound is placed on the CUT, not in the pack**, where the out point is real:

```bash
pnpm descript pin <project> <comp> --media shuffle.wav --at "<card>" --sound --gain 1 --tail 0.2
```

`--tail` answers two traps: `--at` anchors to a WORD, and an anchor past `CARD_TOLERANCE` from the
standing card's own anchor **splits the card** (an unwanted card at 0:05 in the Text sequence, 8 Sep
2026); the offset from the close instead lands the pin on the named card and nudges it to the tail
(`cut: false`). A pack card has no length of its own, so an exit sound is placed when the card is
stamped, never asked of the pack.

## The nine sequences, and what was wrong with them

**The order, since 8 Sep 2026:** Camera, Screen, Text, Motion, B-roll, Claude, Brand, CTAs, Shorts. `pnpm descript mv <pack> comp:<name> . --index <n>` reorders without moving; the `comp:` prefix is not optional, because `Motion`, `Claude`, `Brand` and `CTAs` are also media folder names.

**Motion and Brand were 1920x1080, so their ten cards were invisible in every 4K project** - a pack card is only offered to a project of its own size. Both are 4K now (`pnpm descript resize <pack> <comp> 3840x2160`); the published template carries 39 at 3840x2160 and 5 Shorts at 2160x3840. **Check the size before concluding a card is missing from the picker.**

**Deleting a card is merging it, and `pnpm descript card merge <pack> <comp> <card>` does it.** A
card boundary is what says "a new look starts here"; drop it and the seconds it covered belong to
the card before. The first card of a composition is refused: nothing precedes it. **Pins belonging
to EARLIER cards can `endAnchor` at the boundary being removed**, and dropping it leaves dangling
references the commit gate refuses; they are re-anchored to the boundary that now follows, or to
`endOfComposition` when the merged card was last. `Speaker Bubble`, `Speaker Bubble + Media` and
`Speaker Bubble Exit` existed in both Camera and Motion, same layer counts, different ids,
because the Camera three were unpublished copies; merged away 8 Sep 2026, leaving 41 cards with no
duplicate name.

**Publish carries any of this to the picker**: renaming, retyping or resizing a composition changes
the document only; `layout publish` rebuilds the template, dropping whatever it still offers that
the pack no longer holds.

## What makes an edit dynamic: measured against ES02

`ES02 - Why Your Agency Hits the Ops Ceiling` is the reference for how this channel cuts. Read against
EC49 on 2026-08-31:

| | ES02 (his) | EC49 (a paced ladder) |
|---|---|---|
| runtime | 7.4 min | 24.0 min |
| cards | 91, one every **4.9s** | 104, one every 13.8s |
| pinned elements | 101, **13.7/min** | 30, 1.25/min |

**The dynamism is in the pins, not in the card ladder.** 52 of his 91 cards sit on ONE pack card;
what changes every few seconds is what is pinned over it: 38 b-roll clips, **22 stock sound
effects**, 13 text titles, 4 gifs, 3 shapes and a music bed - a zoom ladder alone gets a video to
about a quarter of that. Three habits: the open is a stack, not a card (ten cards and nine pins
anchored at 0:00); every number gets a card within a second ("50+ agencies" is a `50+` pin and an
`Agencies` pin at 0:09); and b-roll is named by the beat it illustrates.

## Putting words on a layout

The pack publishes 44 cards, and until 2026-08-31 the CLI could stamp only the wordless ones: text
lives on pinned `title` scenes, so stamping `Text Style 1` published the pack's own `Text 1` …
`Text 4` onto the video.

```bash
pnpm descript layout lines "Text Style 1"                     # 4 lines, and what each ships with
pnpm descript layout apply <project> <comp> --card f84d36da \
     --use 909445ab --say "Marketing|Sales|Delivery"           # the 4th line hides itself
```

- Lines come back in **reading** order; the pack stores them in paint order, which runs backwards
  on the stacked styles (`Text Style 1` holds text 4, 3, 2, 1), so they sort on the trailing number.
- **A layout with a line and nothing said is refused**, quoting the placeholder it would publish.
- A line nothing was said on is emptied AND hidden: a hidden layer still holds its words.
- `visual.layout` is the app's cached glyph run and it is dropped on write.
- **`pace` refuses a text layout in a ladder**, which cycles one look over many beats: text is one
  beat at a time, through `apply --say`.

`--say` takes `|` between lines and `\n` inside one, for a bullet list. The words are written in
session, off the transcript, never generated: see the standing rule in the workspace AGENTS.md.

## Pinning a clip, a graphic or a sound effect

```bash
pnpm descript pin <project> <comp> --media "4b [00-24] Two Dials.mp4" --at 1:13 --cards 2
pnpm descript pin <project> <comp> --media "Woosh M" --at 1:07 --sound --gain 0.4
pnpm descript layout register <project>        # repair a project the editor refuses to open
```

Learned by reading `ZZ-TEST PROJECT` (a copy of ES02) on 2026-08-31: the CLI's pin scene,
registration and card layer come back identical to the app's, key for key. Three parts, and the
third is easy to miss:

1. a **pin scene** wrapping the media: `videoMetadata` off the media ref, one tau with an empty
   string, and one `audioSegment` carrying `mediaRefId`, `offset`, `duration` (the ref's **audio**
   duration, not its video one), `gain` and `speed`;
2. a **registration** in the pins track, anchored where it starts and closing on a card boundary;
3. **a layer on every card the pin spans**: 52 of 61 clips carry exactly as many layers as cards
   crossed. FIRST in the list, nearest the viewer, carrying the house look 95 of his ~115 clip
   layers use: `colorAdjustments`, `box {1, 0.5625}`, `shadowPaint`, `shadowBlur`, `shadowOffset`,
   `com.descript.glassBlur`.

**A sound effect has no layer at all.** All 23 of ES02's sit in the pins track drawing nothing,
which is how a whoosh plays over a cut without covering it. And **a media name is not a pin name**:
the pin reads `1b [00-28] Too Many For The Desk`, the media behind it `4a [00-24] Too Many For The
Desk.mp4` - `--media` resolves against the media library, so read the name off `assets` or `doc`,
never off a pin.

**Two fields that look load-bearing and are not:** `timeline.cues` is an empty `cueTrack` on 83 of
ES02's 101 pin scenes (absent on 18), and its `layerOrder` holds 102 ids resolving to nothing in
the document. Z-order is the layer array itself, first entry nearest the viewer.

## What a layout IS, and the document fields that carry it

The person who builds the pack, 31 Aug 2026: **"The layout applies to the image and the sounds."**
A layout is not a look. It is a card carrying:

1. **A layer stack**, in paint order, first nearest the viewer.
2. **Sound**, as pins registered over the card that no layer draws.
3. **Sometimes two camera layers.** A green-screened CAM is placed **above** the text so the
   speaker appears in front of it, with the plain CAM below; where that is not wanted the green
   screen layer is simply removed. Layer stacks vary per layout and must be copied **verbatim**,
   never normalised, and hidden layers (`Script: SCREEN`, eye crossed) are part of the stack.

**Multicam tracks live on `sequenceScenes[].name`**: `CAM-Green-screen`, `CAM`, `SCREEN`. Every
camera layer on a card carries the same `sourceSceneId` and differs **only** by `sequenceSceneId`.
`applyLayout` carries each picture layer's own track name through the stamp
(`template.tracks[index]`) and resolves it per layer with `sequenceNamed`, falling back to the
composition's first sequence only for a layout that recorded no track.

**Transitions are `card.videoFades`**, not a `transition` field:
`{ fadeInDuration, fadeOutDuration, headCurve/tailCurve, head/tailTransitionEffect }`. A negative
duration is the app's own value, not a fault.

**Effects are `layer.effects[]`**, each `{ type, id, keyframes: [{ offset, value }], isDisabled }`.
Measured over 91 cards: geometry (`box` 370, `position` 210, `contentPosition` 179) and looks
(`colorAdjustments` 357, `uplighting` 128, `glassBlur` 123) dominate; `shadowPaint`/`shadowBlur`/
`shadowOffset` run 306 each. `colorAdjustments` is a 10-number vector matching the None/Neutral/
Warm/Cool inspector row. **`box` and `position` are fractions of the frame, not pixels.** `pnpm
descript layer <project> <comp> <card>` prints geometry, `layer set` writes it.

**Text is `layer.textProperties`**: `fontFamily`, `fontStyle`, `fontSize`, `fontWeight`,
`lineHeight`, `textAlign`, `verticalAlign`, `forceUppercase`, `fontMediaRefId`, and a computed
`layout` with per-character spans. **Write the properties and leave `layout` alone** - it is the
app's own measurement cache and it recomputes it.

**Levels are a house rule, not the pack's stored value.** 100% for the audio and 40% for the sound
effect. Packs drift, so `registerSounds` writes `SFX_GAIN = 0.4` on the segment and leaves the
scene gain at 1. Never carry a stored gain forward.
