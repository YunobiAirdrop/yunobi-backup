# The two variants: faceless and face

Step 3 of the workflow. The choice is made by what the video is about, not by whether a
camera was available.

The measured background, in one line: **a face appears in both bands on eight of nine
channels, so presence is not a lever.** What separates is how big the person is and what
job they are doing. Full counts in [`niche-evidence.md`](niche-evidence.md).

## The decision

Ask one question: **is there a thing that can be photographed or captured?** A board, a
workflow canvas, a document, an inbox, a desk, a device, a printed page.

- **Yes** -> faceless variant. The thing is the subject.
- **No**, the subject is a decision, a position, a change in how someone works ->
  face variant, person small.

Two tie-breakers:

- If the video's promise is *"you can copy this"*, always faceless. The viewer has to
  see the thing they would copy.
- If the promise is *"you should stop doing this"*, face variant works, because a
  position needs somebody holding it.

---

## Faceless variant

The strongest single result in the set: Systems Made Better takes 12 of 15 winners with
no person in the frame at all, against 2 of 12 in his controls. He is the channel whose
subject is closest to ours.

### Composition

- **The artifact fills 60 to 80% of the frame.** Not floating in a corner, not shrunk to
  make room for type. If it is worth a thumbnail it is worth the frame.
- **Photograph it in a real place.** A desk with a mug and a plant, a laptop at an angle,
  a printed page held in two hands. A flat screenshot on a coloured plate is the control
  version of this frame.
- **One label block.** White on a dark plate, black on a light plate, or a solid colour
  tab. Placed on the emptiest third, never over the part of the artifact that carries
  the idea.
- **One arrow, at most.** Hand-drawn or a heavy solid, pointing at the single thing that
  matters. Four of Matt Gray's fifteen winners carry exactly one.
- **Dim what must not be read.** If a screenshot is in frame, blur or darken it to about
  30% behind the words. A readable dashboard is a control marker on five channels.

### What kills it

- A screenshot the viewer is asked to read
- Two artifacts competing, e.g. a board and a phone
- A brand logo larger than about 8% of the frame
- A flat plate colour with nothing photographic in it

### Our assets for this variant

Product boxes, 3D tiles and marks are on the design shelf and are offered to the
concept generator through `THUMBNAIL_ASSET_GROUP_IDS` in
the concept module: `thumbnail-3d`, `product-boxes`,
`product-marks`. Recording backgrounds and CTA overlays are deliberately not on that
list; they are for a timeline, not a still.

---

## Face variant

One person. Never two, and it never runs the other way. No guest, no client, no team, no
testimonial face beside yours. In [`niche-evidence.md`](niche-evidence.md), the count.

Three shapes work, all measured. Pick one.

### Small in a real place (Matt Gray)

The person occupies maybe 15 to 30% of the frame height, inside a room, a landscape or a
studio that is doing the talking. Face close up to camera: 1 winner, 3 controls, so this
is the shape that replaces the close-up.

- Environment first: it has to be somewhere, not a backdrop
- Two to four lowercase white words, no plate
- The person is the scale reference and the proof a human is in it

### Holding the artifact (Ali Abdaal)

Mid-shot, the person holding up something they made: a filled notebook, a hand-drawn
framework on card, a printed page, a book.

- The hands prove the artifact is real, which is the whole job
- The artifact must be legible as an object, even when its content is not readable
- Eyes to camera is fine here; the artifact still owns the frame
- **Never render an empty hand.** A hand holding a card comes back with five correct
  digits; the same plate presenting an empty upturned palm fuses its fingers into one
  blade. The object is what the model solves the hand against. If nothing is being held,
  crop the hand out of the frame.
- **If the words name a count, count the objects in the render.** Five bands under
  "5 spaces" is the claim; six bands is a contradiction the viewer checks first.

### Holding the artifact, with the product behind (the strongest shape we have)

The variant above, plus one 3D product tile floating behind the shoulder. Face, artifact
and product in one frame without adding a fourth thing, because the tile lives on a
different depth plane rather than competing on the subject's.

- Tile at 30 to 60% of frame height, tilted 10 to 15 degrees, its lower or left edge
  hidden behind the head or shoulder, colour spilling onto the shoulder and blooming on
  the wall. At the top of that range let the tile run off the top of the frame: a
  cropped object reads as being in the room, a fully contained one reads as placed in it.
- **Occlusion is what licenses the size, not the size itself.** A tile level with the
  head and touching nothing is a logo bug at any scale. The same tile at 62% of frame
  height, mirrored, gently tilted and with its edge behind the head, reads as a lit
  object standing behind the subject. Judge by whether it is occluded and lit, never by
  a percentage alone.
- Hold a supplied 3D asset near the angle it was handed in, mirroring it first if it
  faces the wrong way. **Mark degradation tracks angular distance from the reference
  pose, not scale**: the same asset survived 62% of frame height at a 12 degree tilt and
  fell apart at 55% on a hard desk rotation. See [`craft.md`](craft.md).

### The two-icon equation (Chase)

Not a portrait at all, but it is the face-variant slot on tooling videos: two app icons
and a plus sign on a solid house colour, with a two-word benefit in caps. Three or more
logos drops it to control.

- Exactly two icons, large, with real drop shadow
- Two words: `GOD MODE`, `INFINITE MEMORY`, `MAX POWER`
- The person, if present, is a small cut-out at the edge, not the subject

### What kills it

- A head filling the frame
- A second person, in any role
- A halo of eight or more unlabelled icons around the head
- A pointing gesture at a floating app window (control marker on Systems Made Better,
  Michele Torti, Jordan Ross, Nick Puru)
- An exaggerated shock face. **No shocked face appears in any winner band in this
  niche**, on any of the ten channels, and neither does a max-saturation palette.

### Our assets for this variant

The live face plates are the iPhone set, browsable in the app at **`/design/shelves/faces`**,
served from `youtube/{faces,broll,portrait}/<expression>/`. Copying a tile
puts the picture itself on the clipboard, so it pastes straight into a composition or a
model call. The set holds 86 face plates in 26 expressions, 15 desk b-roll frames and 10
seated portraits. The older 39-frame webcam set at `~/Pictures/thumbnails-2026-08-19/`
is superseded and nothing reads it programmatically.

Naming is `<expression>-<copy-space>-<nn>`, where copy-space names the **empty** side
the words go on, so `confident-left-07` has the subject on the right.

Given the finding above, prefer `confident`, `smile-confident`, `deadpan`, `thinking`,
`explaining`, `arms-crossed` and `offer-smile`. The loud plates exist (`mindblown`,
`gasp`, `shock-arms`, `angry-shout`, `shout`, `facepalm`) and **nothing in the evidence
supports them in this niche**, see above. The desk b-roll frames are the better raw
material for the faceless variant than a face plate is for this one.

The face is always a **composite, never a generation**: hand the real photograph to the
model and let it build the environment, the separation and the type around it. Asking a
model to change an expression distorts the feature the eye checks first. Detail in
[`rendering.md`](rendering.md).

---

## A/B pairing

The two variants make the cleanest possible A/B pair when the words are held constant.
That is the recommended variant C in the build order: same title, same words, one frame
built each way. YouTube picks on watch-time share rather than raw CTR, so note that when
handing over.
