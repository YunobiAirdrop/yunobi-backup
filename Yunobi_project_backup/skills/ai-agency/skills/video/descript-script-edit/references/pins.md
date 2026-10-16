# Placing b-roll, overlays and zooms

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

## What it refuses, and why

**Media not on the timeline.** Every `mediaRef` carries an `assetKey` and an
`assetJson.url` naming a real uploaded asset - all derived from one guid, with the URL
`https://assets.descript.com/lookupKey/<guid>`. `get_project` lists media by display
path and exposes neither, so a clip rendered but never dragged in cannot be placed.
On the EC51 project that was 40 of 43 rendered clips. The refusal prints what IS
placeable. Learning the guids needs Descript's private frontdoor call captured with
ego-lite, `clickup-browser` style; not built yet.

**A phrase that no longer exists.** Phrases resolve against the surviving (unblocked)
script only, so a clip never opens on an ignored restart. A phrase taken from the
pre-cut transcript after a reorder is a refusal, not a guess.

**An ambiguous phrase.** Same contract as the cut list: add `nth`, `pre` or `post`.

**No pinTrack to clone.** The pin track is cloned from a live example. A project that
has never had one needs one clip dragged in by hand, then a fresh copy.

## Proving it

`scripts/test_pins.py <grab.json> ...` derives its own spec from whatever the payload
holds, so a new video is a new test case for free. It checks that the closing card
drops the layer and sits after the opening one, that clip and camera geometry match
the layout they cloned, that no layer points at a scene that does not exist, and that
no ids collide.

## The catalogue gate, and the fourteen blank cards

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

**Run `catalogue` before placing a single zoom, and read the layout line as a gate.** A zoom clones
the prevailing stack; where `catalogue` says `none - no card in this payload carries a pin layer`
there is no stack, so every zoom lands as an **empty card** and the frame goes blank on that word.
It refuses a clip in that state and it does not refuse a zoom, which is the trap. On EC49 on
2026-08-31 that shipped fourteen blank cards into a finished cut and cost a round trip to find.
With no layout in the composition the zooms are not a pin job at all: `pnpm descript layout pace`
stamps a real pack look and **restamps a card that already stands**, so it is both the placement
and the repair. On a screen tour pass `--screen SCREEN`, or every frame of a Screen layout draws
the camera and the screen recording never appears.

## The shape of a `pins.json`

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

```json
[{"media": "19 [02-00] Nobody Pointed At It.mp4", "in": 0, "dur": 16.8, "layout": "02 [00-20] Mental Load Fades",
  "from": "Nobody takes care of harnessing that information", "to": "for your sales team and your AI"},
 {"zoom": 130, "from": "The hourly rate is the price divided by the time spent"}]
```

**A pin is three coupled objects, so an insert is a state change, not an object drop** - a card at
the in-point carrying the layer and a second at the out-point that does not; miss the closing card
and the clip runs to the end of the video. Read [`references/pins.md`](pins.md) before
writing a `pins.json`: the object model, the z-order and geometry rules, every refusal and what
clears it. `scripts/test_pins.py` proves it.

**Run `catalogue` before placing a single zoom, and read the layout line as a gate.** A zoom
clones the prevailing stack, so where `catalogue` reports no card carrying a pin layer every zoom
lands as an **empty card** and the frame goes blank on that word. It refuses a clip in that state
and does not refuse a zoom, which is the trap: fourteen blank cards shipped into a finished cut on
2026-08-31. With no layout in the composition this is not a pin job at all, and
`pnpm descript layout pace` is both the placement and the repair.
[`references/pins.md`](pins.md) has the run it cost and the `--screen SCREEN` rule.
