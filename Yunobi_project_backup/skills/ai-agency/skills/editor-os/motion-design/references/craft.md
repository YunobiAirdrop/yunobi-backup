# Craft: how a clip is built

How a clip is rendered in a Remotion motion project: finishing, the primitives that exist because something
failed without them, the motion vocabulary, the frame, the grounds, the alpha cut, type, and who may
nudge what. SKILL.md holds the judgment; this holds the mechanics. Names like `Shot`, `Backdrop`, `tokens.ts`
and `motion.ts` are the shared pieces of one project's kit. Build your own equivalents, one file each,
so every clip pulls from the same place.

## Finishing: what makes it look photographed, not composited

Three things, all in `Shot.tsx`, and every new clip gets them by being wrapped in `<Shot>`.

**Grain over the whole frame, graphics included.** The backdrop's shader noise sits *under* the
graphics, so clean elements over a grained ground read as composited rather than shot. One pass over
the composite puts everything in the same air; it cannot be done inside `<Backdrop>`. The seed changes
every frame (static grain is dirt on the lens), it goes through `feColorMatrix saturate 0`
(feTurbulence is per-channel, so at any opacity it is coloured confetti), and it blends `overlay` so
it bites in the midtones where banding lives.

**One key light per shot, positioned where the subject is.** Glow used to be a property of individual
elements, so a set of them had no light source at all. A light that does not follow the subject lands
on the wrong half of the frame off-centre, so `<Shot lightY={...}>` takes it.

**A specular top edge.** A vignette and a key light alone make the frame a blob. One brighter edge
gives the light a direction: "there is a glow here" versus "this is lit from above".

## Panels and impacts go through the primitives

Two failures were structural, so they are fixed in `primitives.tsx` and nothing new should hand-roll
either:

- **`Plate`** is a lit panel drawn *behind* its content. `filter` applies to an element's whole
  subtree, so a glow on the container that holds a label glows the label and the text goes soft.
  Content is an unfiltered sibling laid over the plate.
- **`Landing`** puts a `Ripple` at a point. `Ripple` is absolutely positioned with no offsets and
  relies on a zero-size flex parent; give it a `width: 100%` parent instead and the ring hangs down
  and right of whatever landed, silently.

And a rule that is not a component: **say "this one" with colour, not with more light**, and
cross-fade two plates rather than switching a colour with a ternary. A threshold on a moving value
flips inside one frame and pops; a colour cannot be interpolated inside a CSS string.

## One motion language

Continuity between clips is not a shared palette, it is shared physics: the eye reads acceleration
before colour, so three clips that each picked their own spring inline are visibly by three different
hands however well they match on hue. `motion.ts` is the one home for the vocabulary:

- `ENTER` (16/130) arrives and takes its place; the default in an empty frame
- `ARRIVE` (13/190) lands on a surface, shorter and snappier
- `SETTLE` (damping 200) no overshoot, for opacity and light; overshoot on a fade flickers
- `DEPART` (22/90) weight leaving, heavier than it arrived
- `TRAVEL` (inOut cubic) journeys between two known positions
- `ANTICIPATE` (4 frames) the load before a big move; from dead rest reads as dragged
- `HOLD` (18 frames) floor for the tail after the last element resolves

**Journeys interpolate, arrivals spring.** A spring at every waypoint turns a route into a series of
arrivals. A curve that is not there is added to `motion.ts` with its own WHY; inlining one starts the
drift again.

**Both ends of a clip are designed, never only the entry.** Verbatim, 27 Aug 2026: **"Always think of
the entry and exit animation of a motion. Always."** A clip built entry-first arrives beautifully,
resolves, and then sits there until the render runs out. It does not end, it stops. Every element with
an `ENTER` has an exit chosen with the same care, written into the header comment beside it, one of:

- **Depart.** The subject leaves under `DEPART`. For anything that was the whole subject of the frame.
- **Resolve and hold.** The last element settles, then `HOLD` so the payoff is not stepped on.
- **Hand over.** Everything goes except the one mark the next clip inherits, which makes the
  through-line a join rather than a cut. The default in a set.

An alpha clip has no ground to hide behind, so its exit is the difference between an overlay and a pop.
A long take runs on the camera's own four (`TAU`, `dolly`, `countTo`, `wordFlow`), measured rather than
chosen, never mixed with these; [long-take.md](long-take.md) has the measurements and the boundary.

## The frame

- 1080x1920. Keep the subject between roughly y=300 and y=1650. Below that is where TikTok, Reels and
  Shorts put captions and the handle.
- **y=1650 is the composition floor, not the occlusion line.** The platform's UI reaches higher and
  comes in from the RIGHT: the action rail sits over the middle-right, where a card lands.
  `scripts/deadzone.py` measures ink inside the per-platform rectangles and exits non-zero. Run it on
  every portrait render:

  ```bash
  python3 scripts/deadzone.py out/Clip.mp4 --for reels --sheet
  ```

  Written after `out/explainers/n-plus-one.mp4` passed the 300/1650 band and failed this: its payoff
  sat below y=1436, covered by the caption block on Reels and TikTok. The numbers are a conservative
  intersection of disagreeing third-party guides; `--calibrate` replaces them off a real screenshot.
- That band is a floor, not a composition. Work out the full extent of everything the clip draws and
  centre *that*, or a design that grows downward ends up top-heavy with a dead third underneath.
- Type has almost no horizontal room in portrait. Check a label's rendered width against 1080.
- Colours come from `tokens.ts`, a transcription of your brand palette. Do not invent values.
- Every clip carries its own `<Backdrop />`; clips are cut in individually and never inherit one.
- Brand colours are exempt from the palette, not from contrast: a mark darker than the backdrop needs
  a light substitute for its border, glow and wires or it renders permanently unlit. Notion is
  `#000000`.

## Every landscape clip ships in two frames

A full-frame clip is a cutaway: it replaces the picture. The author also cuts the same graphic **beside**
himself, keyed over the empty half of the room or as a split screen, and that is a second frame.

- **1920x1080** is the cutaway. Opaque for a straight cut, alpha for keying over the whole picture.
- **960x1080** is the beside-the-face frame. `NARROW_W` and `NARROW_H` live next to the landscape frame constants.

Four files per clip, all deliverables, and the render scripts come in pairs: `render:<set>` /
`render:<set>-mov` and `<set>-narrow` / `<set>-narrow-mov`.

**The narrow frame is exactly half the wide one and is committed to neither side**: a graphic composed
into the left half of a 1920 frame has already chosen the left half. A 960x1080 file drops onto a
split screen at 1:1.

**It is a re-layout, not a scale.** 45 percent of a 32px label is 14px, unreadable at 1080p. The figure
is stood on end: a row of stations becomes a column, a wall becomes horizontal. What must not change
is which element carries which claim.

**One `Layout` object per clip, two members, chosen by a `narrow?: boolean` prop.** A second set of
x/y constants is how the two versions drift. A single track is `along`/`cross`, swapped by
`pt(along, cross)`.

**The key light is named per variant, never computed from the layout.** Deriving `lightX` from a
card's centre changed the *approved wide render* of two clips by moving their key light. **Prove the
wide render did not move**: render its still before and after adding the narrow variant and compare
the hashes. Byte-identical is the pass.

Register four compositions: `X`, `XAlpha`, `XNarrow`, `XNarrowAlpha`, the narrow pair taking
`defaultProps={{ narrow: true }}` and the alpha both flags.

## Two grounds, and the overlay cut

`<Shot ground="grid">` is the original world: ink, two parallaxing grids, a vignette. Every
already-approved clip stands on it, and it stays the default so nothing ships a silent restyle.

`<Shot ground="bloom">` is the indigo noise field in `NoiseField.tsx`: a soft bloom of brand colour on
ink, dithered hard at 0.30. It is a material rather than a finish; at low grain it is a stock gradient,
and the grain kills the banding a gradient shows across 1920px of near-black.

`<Shot ground="daylight">` is the pale ground: a lit mid-grey wall from `daylightEdge` to
`daylightCore`, panels lighter than the wall, ink type. It changes three things, because a ground built
for ink does the wrong thing over grey: the key light goes white and drops to about a fifth (the wall
carries its own hotspot) and `Ambient` comes out. It belongs to the long take only.

**`<Shot alpha>` is a different deliverable, not a different look.** It renders with no ground, for a
clip keyed over his screen recording. The grain and specular edge come out with the backdrop: `Grain`
is a full-frame rect at `mixBlendMode: overlay`, and over transparent it composites into the alpha
channel as a boiling haze across every pixel that should be empty. `Ambient` is a cream gradient down
the top quarter, a white wash over footage. The key light stays at about a third strength, the one pass
that makes a graphic look like it is in the same room. Register the alpha version as its **own
composition** with `defaultProps={{ alpha: true }}` and `calculateMetadata={alphaPreviewWebm}`, not as
a render flag: the editor needs a file per option.

**The alpha deliverable is always a `.mov`.** Remotion cannot write a keyed QuickTime, so every route
is ProRes 4444 through `remotion.prores.config.ts` and then ffmpeg. A WebM is a preview, never the file
an editor is handed. The author, 8 Sep 2026, after a clip shipped as one: **"you cannot use webm. You need
to use MOV if you want an alpha layer."**

**Anything going into Descript is `qtrle`/`argb`**: HEVC alpha lands on black there, and its
importer refuses it. A shelf clip whose subject is a capture (a browser window, a screen, a photograph) goes to **HEVC with alpha**:
`-c:v hevc_videotoolbox -pix_fmt bgra -alpha_quality 0.95 -b:v 40M -tag:v hvc1`, the way a browser-window clip should. qtrle on a photograph degenerates towards raw: one 23-second
clip was 560MB as qtrle and 97MB as HEVC.

**ffprobe cannot see an HEVC alpha layer.** It reports `yuv420p` on a correct file, so a flattened key
and a good one measure identically. a small AVFoundation script that saves a frame decoded through it is the only check that reads
the layer on a Mac; a corner must come back `srgba(0,0,0,0)`.

## Type

Most clips have no words at all, and that is the default. Add type only when the read names something
the viewer is being sent away to find. "API, CLI or MCP" is jargon, it is the search term, and no shape
can say it. When you do: labels only, uppercase, tracked out, never a sentence. A viewer reading prose
has stopped listening.

**That rule covers a clip that replaces the picture, and only that.** An overlay keyed over his face is
the case where the sentence is the point: he is reading the list out loud and the words on screen are
what he is saying, in sentence case, in the brand face, set to be read. `figures.md` holds the split
and the three failures that only happen over footage.

Load the brand font once, in one file, through `delayRender`. A font loaded inside one clip family
is how the other clips end up in the system stack.

## Who may fine-tune: the constants-versus-Studio call

Remotion Studio can write edits back into the source, but only where it can read the markup: inline
`style` objects, inline `interpolate()` calls with hardcoded ranges, `scale`/`translate`/`rotate`
instead of `transform`, inline `defaultProps`, `Interactive.Div` with a hardcoded `name`. A value
behind a constant, a spread or any arithmetic goes grey in the Studio. `remotion`
(remotion-interactivity/REFERENCE.md) has the full list.

That conflicts with the two rules above it, resolved by what the clip is for:

- **A set of clips cut into one read keeps the constants.** Named frame numbers in `beats.ts` and
  named springs in `motion.ts` are what make fifteen clips look like one hand. Retiming stays one edit.
- **A one-off the owner will nudge by eye takes the inline form.** Overlays, CTAs, a title card: no
  siblings to stay continuous with, so the faster loop beats the abstraction. Colour still comes from
  `tokens.ts`, pasted inline with the token name in a comment beside it.

Never mix the two inside one composition. Half-interactive markup reads as broken rather than
deliberate, because the greyed-out control gives no reason for being grey.
