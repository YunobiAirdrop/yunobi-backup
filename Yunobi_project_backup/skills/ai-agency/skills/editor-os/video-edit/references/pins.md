# Placing b-roll, overlays and zooms

## The clock a clip is cut against, before placing anything

A b-roll clip's length is the span between two phrases in the cut. Getting that span from a
subtitle export is how the Glance set ended up timed **203.8 seconds wrong**: a cut took the
composition from 2038.3s to 1834.5s, and the plan written afterwards still carried the old clock.
Twelve clips were designed against timings out by up to 196 seconds, and the error surfaced only
because somebody re-derived them from the document.

```bash
pnpm descript doc <project> --out doc.json
python3 scripts/beatclock.py doc.json                      # every surviving tau, with its start
python3 scripts/beatclock.py doc.json --find "a phrase"    # the taus holding it
python3 scripts/beatclock.py doc.json --beat "first words" "last words"   # start, end, duration
```

It walks the composition's superTau, skips every blocked tau (an Ignore draws no time), and
returns the cumulative play clock. **Its total equals what `get_project` reports as the composition
duration**, which is the check that says this clock is the render's clock. Each duration is
divided by its `speed`, because `duration` is source time, not play time: ES02 is 476.83s
undivided and 454.54s divided, and 454.54 is the truth. Print it once before writing a timing.

**A beat is its own sentence, and its neighbours are a constraint, not context.** Several Glance
beats had been timed past the line they serve: one ran to 37s when its sentence ends at 27.8. Two
beats 2.6 seconds apart cannot both be clips - `motion-design/planning.md` calls that a montage -
so the GAP between measured spans decides the plan as much as the spans do. **A cut is not a
uniform shift**: the Glance drift was 0.85s at the start, 6s at 2:30 and 196s at 29:00, so a plan
"adjusted by the difference in total duration" is wrong everywhere except the end.

**Re-run it after any cut, reorder or paste.** A clip already rendered against an old clock does
not need rebuilding unless its DURATION changed, but check both: a shortened beat whose component
was choreographed for the old length silently loses its last movement, as happened to the Glance
payoff beat (resolve at frame 344 of a 318-frame clip). The in-page readout is mostly ruler ticks;
report a duration from `compositions[].duration`, and with ignores present sum the unblocked tau
durations instead, which is what `pnpm descript script` prints.

## The object model

A pin is three coupled objects, never one:

| object | holds |
|---|---|
| `pinTrack` | the media, and its in/out inside that media (`audioSegment.offset/duration`, `speed`) |
| `cardBoundaryComponent` | the WHOLE layer stack at one point in the script; the clip is one layer, addressed by `sourceSceneId` |
| `sceneComponent` | the span: `tauAnchor` -> `endAnchor {type: "cardBoundary", cardBoundaryId}` |

So an insert is a **state change**, not an object drop: a card at the in-point that
carries the layer, and a second card at the out-point that does not. Miss the closing
card and the clip runs to the end of the video.

`add_pins` reads the prevailing stack at each anchor and clones it, so other pins'
spans are never disturbed. A card that already sits on the anchor is reused rather
than duplicated.

## Geometry

Layer order is z-order, **index 0 on top**: a background plate sits last, a talking
head over a full-frame clip sits first. Geometry is width-normalised, so a full 16:9
frame is `box {width: 1, height: 0.5625}`.

Geometry is never invented. `layout` names a clip already in the project; the whole
effect stack is cloned - box, contentScale, contentPosition, shadowPaint, shadowBlur,
shadowOffset, glassBlur, colorAdjustments - and the camera layer is replaced with a
clone of that layout's camera, not merged key by key. `catalogue` prints the library
read back out of the payload, so a placement can only ask for a look the video already
uses. A zoom is the same object with only `contentScale` changed, and it needs no
closing card: `{"zoom": 130, "from": "..."}`.

Overrides, when a layout is right but one value is not:
`"geo": {"contentScale": {"x": 1.4, "y": 1.4}}`, `"z": 0`, `"cam": false`, `"speed": 2`.

`box` is in FRAME WIDTHS on both axes (full frame is `1 x 0.5625` at 16:9), `position` is 0..1 per
axis and names the centre, and `--anchor` converts between them. `layer place` takes `all` for
`<card>`, which is one commit where a loop would be fifty.

## A b-roll ends where its scene ends

A clip that hides the camera has to run all the way to its card's close. If it's shorter, it
stops early and the frame goes empty for the rest of the scene. The author, 28 Sep 2026, on B01a
stopping 0.2s short: *"when you insert a b-roll you need to make sure that it always ends at the
end of the sequence."* There are two fixes, and which one depends on the gap:

- **A little short: slow it.** `pin` does this itself. When the clip covers at least 85% of the
  card, it sets the speed so the last frame lands on the close and reports `speed` beside
  `holds: 0`. Around 0.9x is invisible on b-roll.
- **A lot short: end the scene earlier.** Below 0.85x, `pin` refuses and asks for `--to` on an
  earlier word. Past that point, slowing it reads as slow motion.

A clip longer than its card is fine: the card trims it, and `holds` prints negative. A motion
overlay keyed over the camera isn't held to this rule, because when it ends early the camera just
comes back. Read `holds` on every pin: anything above 0 on a b-roll is the empty frame this rule
exists to prevent.

## What it refuses, and why

**Media not on the timeline - the CLIPBOARD route only.** `dscript.py pins` needs the
asset guid behind `assetJson.url`, and the clipboard payload only carries it for media
already on the timeline, so through that route a clip rendered but never dragged in
cannot be placed (40 of 43 on EC51 in August). `pnpm descript pin` reads the guid off
the document itself and has no such limit: on 8 Sep 2026 it resolved an EC51 clip
imported fifteen days earlier and never touched. Reach for the CLI first.

**A phrase that no longer exists.** Phrases resolve against the surviving (unblocked)
script only, so a clip never opens on an ignored restart. A phrase taken from the
pre-cut transcript after a reorder is a refusal, not a guess.

**An ambiguous phrase.** Same contract as the cut list: add `nth`, `pre` or `post`.

**No pinTrack to clone.** The pin track is cloned from a live example. A project that
has never had one needs one clip dragged in by hand, then a fresh copy.

**A pin closes on `--to "<phrase>"` where the stretch has no cards.** Default is the next card, and
on a canvas walk that sits on one card the next card is twenty minutes on (EC51, `holds: 398.6`).
`--to` cuts the closing card at that word in the standing look, so the frame after the clip is the
frame before it. Read `ends` against the clip's length in the `--dry` output: a span shorter than
the clip truncates it, longer freezes its last frame.

**An alpha `.mov` needs `--keep-cameras`.** `pin` hides the cameras under anything taking the FULL
FRAME - `camerasHidden` is the count, and a title or a fitted still covers nothing and keeps them.
A keyed clip fills the frame geometrically and is transparent everywhere its graphic is not, so
that box test cannot tell it from a b-roll and switches off the face it exists to key over. There
is no codec worth sniffing, so the caller says it: `--keep-cameras` leaves every camera lit and
prints no `camerasHidden`. Check the card with `descript layer` after any keyed pin.

**A cut where the camera goes off carries NO transition.** The author, 9 Sep 2026: a smart transition
there "creates some weird flicker", because the app dissolves a frame that is half face, half clip
while the camera layer under it is switching off. The same test that hides the cameras clears the
two boundaries that bracket the clip, and `transitionsCleared` counts them. `descript transition
sweep <project> <comp>` is the same clearing over a whole composition, for an edit cut before this
rule; `--dry` first. One boundary on its own is `transition <card> --off`.

## Proving it

`scripts/test_pins.py <grab.json> ...` derives its own spec from whatever the payload
holds, so a new video is a new test case for free. It checks that the closing card
drops the layer and sits after the opening one, that clip and camera geometry match
the layout they cloned, that no layer points at a scene that does not exist, and that
no ids collide.

## The catalogue gate, and the fourteen blank cards

**Run `catalogue` before placing a single zoom, and read the layout line as a gate.** A zoom clones
the prevailing stack; where `catalogue` says `none - no card in this payload carries a pin layer`
there is no stack, so every zoom lands as an **empty card** and the frame goes blank on that word.
It refuses a clip in that state and it does not refuse a zoom, which is the trap. On EC49 on
2026-08-31 that shipped fourteen blank cards into a finished cut. With no layout in the composition
the zooms are not a pin job at all: `pnpm descript layout pace` stamps a real pack look and
**restamps a card that already stands**, so it is both the placement and the repair. On a screen
tour pass `--screen SCREEN`, or every frame of a Screen layout draws the camera and the screen
recording never appears.

## Two details

The filler pass cuts sentence-opening `now` / `so` **positionally**, so `so that` keeps its `so`.
A still needs no duration: `--seconds` is for a clip, and a `pin` of an image holds its slot until
the closing card whatever the number says.

## The shape of a `pins.json`

```json
[{"media": "19 [02-00] Nobody Pointed At It.mp4", "in": 0, "dur": 16.8, "layout": "02 [00-20] Mental Load Fades",
  "from": "Nobody takes care of harnessing that information", "to": "for your sales team and your AI"},
 {"zoom": 130, "from": "The hourly rate is the price divided by the time spent"}]
```

## The transparent plate

`media swap` repoints a pin and `rm` deletes media, but **nothing removes a pin**. The way round is
the project's own alpha convention: Descript composites an alpha `.mov` over the camera, so a fully
transparent HEVC-alpha clip cut to the card's exact length hands that card back to the face
underneath.

```sh
ffmpeg -y -f lavfi -i "color=c=black@0.0:s=1920x1080:r=30:d=<card seconds>,format=argb" \
  -vcodec qtrle -t <card seconds> plate.mov
```

Import it, `media swap` the unwanted clip for it, then `rename` and `mv` the survivor, because a
swap keeps the **old media's id and name** and consumes the new one. Card lengths come from the
document: anchor each card boundary to its tau, add `offsetFromAnchor`, and the gap to the next
boundary is the length. Match it or go a few hundredths over; short media freezes on its last frame.

**Swap by media id, never by name.** A project routinely holds two copies of one stock clip and a
name match silently picks the unplaced one, which looks like a successful swap and changes nothing
on screen.
