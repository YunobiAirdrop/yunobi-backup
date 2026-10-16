# Producing the assets a frame is composited from

Step 6b, where the build order's assets that do not exist yet get made, before a single image call is spent.

**The law: anything that has to be exactly right is built and handed in, never described.** The face, a
real logo, words printed on an object, a count of things. A model asked to draw any of them authors
something plausible and different every render, and at 320 pixels a wrong mark and a right one look the same.

## What the model is allowed to author

| | Built, then handed in | The model's job |
| --- | --- | --- |
| The face | A plate from the owned library, unchanged | Light it, put it in a room |
| A brand mark | A 3D tile off the vendor's own SVG | Tilt it, glow it, cast its shadow |
| Words on an object | HTML, screenshotted | Bend it in the hand, take the room's light |
| A count of anything | HTML, screenshotted | Place it, grade it |
| The overlay type | Real Manrope, composited behind the subject | Nothing |
| The room, the depth, the light | | All of it |

A model asked only to light, place and grade is asked for what it is excellent at.

## The whole frame, composited from real pixels, no model at all

The third execution route, beside `--photo` and generation, for a background that is itself a
real artifact worth keeping verbatim: a screenshot, a board, a document, a dashboard. Generating
it invents the on-screen text; handing the face over redraws him. Compositing keeps both real: his face, and the real
data on the screen. On the "Ops Ceiling" frames, 26 Aug 2026: the AI-faced renders were
rejected, the composite of the real face over the real workload screenshot was kept.

**The winning recipe is both moves, not a choice between them.** A flat real screen on a flat `--photo` plate looks amateur; a fully generated frame invents the screen. What was kept, 26 Aug 2026, on both
the "hiring won't fix it" and the Glance "clients see this" frames:

1. **Edit-pass the scene** ([`rendering.md`](rendering.md)): hand the model his real base frame,
   keep the face pixel-for-pixel, generate a dark cinematic studio with a warm rim light, and keep
   one zone (say the left two thirds) **dark, empty and defocused: no screen, panel or object
   there.** That zone is where the real thing goes.
2. **Composite the real screenshot into the cleared zone** as a floating device: a dark bezel, a
   slight tilt, a coloured glow keyed to the content, a drop shadow, sized so it never covers his
   face. His gesturing hand from the base plate then reads as presenting it. Result: the generated
   cinematic depth *and* the real product pixels, the ClickUp board's real 200% bars, the Glance
   portal's real 33% / 3 tasks / 38h.

**The flat composite (screenshot as the whole background) is the fallback**, for when there is no
room to generate and the data has to fill the frame and stay legible. A flat cut-out on a flat
screenshot reads amateur beside a generated frame with real depth: same day: "you're just
slapping the image like that... it looks extremely shit."

Three layers, stacked with `magick`, then the type set through `composeThumbnail`:

```bash
# 1. the real background, filled to frame
magick screenshot.png -resize 1280x720^ -gravity center -extent 1280x720 bg.png
# 2. the real face, cut off its plate with Apple Vision, trimmed to its bounding box
magick static/youtube/faces/<pose>/<plate>.webp face.png
cutout face.png subject.png
magick subject.png -trim +repage subject-trim.png
# 3. lay him in (right third, flush to the bottom); scale by height
magick bg.png \( subject-trim.png -resize x700 \) -gravity SouthEast -geometry +0+0 -composite plate.png
```

Then call `composeThumbnail({plate, out, type, appRoot, work})` from
the compositor for the words: it re-cuts the subject off the composited plate and
tucks the type behind his shoulder, the same depth move as everywhere else. The background
can also **float** as a tilted panel: his hand from an "explaining" plate then reads as
presenting it. File with `render-thumbnail.ts --concept=<uuid> --file-dir=<dir>`, no `--model` named: it files as an upload at **zero cost**, since no image call was made.

Two `magick` gotchas that cost real time on 26 Aug 2026:

- **Rotate greys an alpha-masked PNG.** `-compose CopyOpacity` then `-rotate` returns a
  greyscale panel: the mask contaminates the colorspace through the rotate. Tilt the
  **opaque** screenshot first (`-background none -rotate -6` keeps colour), then add the
  bezel/shadow; sharp corners on a tilted screen read fine.
- **Force truecolour on the way out.** A step that merges a `-shadow` can collapse the panel to
  greyscale; write `PNG32:panel.png` and verify with `magick panel.png -colorspace HSL -channel
  G -separate -format '%[fx:mean]' info:` (near-zero saturation mean means it went grey).

## Declaring a produced asset

A concept's assets carry an optional `build`, the recipe for the file when the library
does not hold it yet
(the concept schema):

```jsonc
{
  "url": "/design/thumbnail-artwork/ops-ceiling-bars.png",
  "role": "The ceiling figure artwork, on transparency. Reproduce it exactly",
  "build": {
    "kind": "artwork",                                   // or "logo3d"
    "source": "artwork/ops-ceiling-bars.html",
    "width": 900,
    "height": 620
  }
}
```

`kind: "logo3d"` swaps `source` for the vendor SVG and adds `tile` (the gradient prompt, e.g.
`"a ClickUp brand gradient from magenta #FF02F0 through orange #F76808 and violet #6647F0 into
blue #0091FF"`) and `symbol` (e.g. `"pure white"`).

Then one command produces everything and renders:

```bash
node scripts/render.mjs --prompt prompt.txt --ref face.webp --out out/a.png
node scripts/render.mjs --prompt prompt.txt --ref face.webp --out out/b.png --passes 3
```

**A named asset that is neither on disk nor buildable is fatal, on purpose.** The
mood board script skips a missing file and renders anyway, which is how a frame comes
back carrying a mark the model invented. Here the run stops and names the file.

## A 3D tile, from the vendor's own SVG

`logo3d:gen` in `website/`, owned by `graphics`' logo-3d branch: rasterises the real SVG, hands it
to the image model as a reference, keys the backdrop off so the mark is relit rather than
recalled. Read that branch before changing a flag: its negative list is load-bearing.
Two rules that bite at composite time:

- **Colour the tile and the symbol separately.** Told only to keep the brand colours,
  the model gives the symbol the tile's own hue: legible at 1024, a smudge at 320.
- **Keep the tile near the angle it was handed in.** It degrades the further rotated or
  blown up: 10-15 degrees and 35% of frame height comes back exact, a hard tilt and 55%
  merges the shapes. `magick <tile> -flop` into the scratchpad, never the owned asset.

## An artwork card, from HTML

Anything with words, rows, colours or a count. A 40-line HTML file is enough, shot at 2x
on a transparent canvas so the model can place it on any ground:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --default-background-color=00000000 --window-size=900,620 \
  --screenshot=card.png "file://$PWD/card.html"
```

Three shapes this covers, the three that used to fail:

- **A printed card**, a list of names, a set of rows. Four prose descriptions of the same
  card produced four different cards, one with the wrong row count.
- **Redaction.** A model asked to blur text obeys about half the time, else returns
  confident fake words. Draw plain grey slabs tracking the real word lengths instead.
- **A figure with a count**, like five bars where one differs from the rest: the copy
  often names the number, and a viewer checks a number before reading anything else.

## The overlay type, which the model draws only when it may

Under four words on a solid tab, the model sets reliably. When the type has to be
exactly the brand's, take it back with the four-step composite in
[`rendering.md`](rendering.md): clean plate, cut the subject out
(the cutout tool), set the real heading face through headless Chrome, stack
plate, type, subject. The type lands *behind* the person, the same depth move as the tile.

**Attaching them, order matters**: a model told "use the attached photograph" with three
attachments picks one at random. The render script numbers them and binds each ordinal
to its role, so image and sentence cannot drift apart:

```
Attached, in order:
  Image 1: Face plate, the subject frowning and pointing to frame left. Use it unchanged.
  Image 2: The ceiling figure artwork, on transparency. Reproduce it exactly.
```

Ask for reproduction, not inspiration: *"reproduce that exact object at almost exactly
the angle it is presented in, do not rotate the mark, do not merge the shapes."*

## Checks that belong to this step

- [ ] Every asset in the build order resolves to a real file after the produce pass
- [ ] A produced 3D tile is checked against its source SVG at full resolution
- [ ] A produced card's words, colours and **row count** match what the copy claims
- [ ] The artwork is on transparency, so the model owns the ground and the light
- [ ] Nothing that had to be exact was left in prose
