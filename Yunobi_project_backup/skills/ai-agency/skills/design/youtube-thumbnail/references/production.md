# Producing the frame: depth, assets, handoff and critique

Steps 5b to 8 of the workflow in `SKILL.md`. They run once the variant, the words and the
plate are settled, and they are followed in order.

## 5b. Build the depth and the light

Steps 2 to 5 decide **what is in the frame**, not why two frames holding the same things
look one professional and one homemade. That is the craft layer: [`craft.md`](craft.md),
read before writing a prompt or a designer spec. The four that carry most of it:

- **Clean means depth, not fewer things.** Three planes: a defocused ground, the sharp
  subject, one object floating between them. One plane reads cluttered at two elements.
- **Separation is light, never a cutout.** A rim light down the shoulder and jaw puts a
  figure in a room; its absence makes a composite look pasted at 320 pixels.
- **A floating object must occlude, tilt, glow and cast.** All four, or it is a sticker.
- **Craft transfers between niches; claims do not.** Lighting and layering from any
  channel; subject, expression and words only from your own banded evidence.

## 6. Write the build order

Output exactly this, before anything is drawn or rendered:

```
THUMBNAIL BUILD ORDER
Title:        <video title as published>
Promise:      <one sentence>
Variant:      face | faceless
The one thing:<what the eye lands on, and what it tells the viewer>
Frame:        <what is photographed or composited, framing, where the subject sits>
Depth:        <what is on each of the three planes: far / subject / floating>
Light:        <key direction, where the rim runs, what the floating object spills onto>
Words:        "<2-4 words>"  | placement | plate colour
Plate:        <background, the two working colours with hex>
Assets:       <exact files, by path, each marked owned or produced>
Not in frame: <what was deliberately left out and why>
Why it wins:  <which finding in niche-evidence.md this bets on>
```

Then two variants, changing **one** variable each, so a YouTube A/B test gives a clean
signal: variant B changes the words only, variant C changes the variant (face <-> faceless)
with the same words.

## 6b. Produce the assets the frame is composited from

The build order named its assets. Some do not exist yet, and that is normal: **anything that
has to be exactly right is built and handed in, never described.** The face, a real logo,
words on an object, a count of things. A model asked to draw any of those authors something
plausible and different every render, and at 320 pixels a wrong mark and a right one look the
same.

Two producers, both wired into the render script so a missing file is made rather than
skipped: a **3D tile** from the vendor's own SVG through `logo3d:gen`, and an **artwork
card** from an HTML file through headless Chrome. The recipe rides on the asset as a `build`
block. Full contract and checks: [`composites.md`](composites.md).

```bash
export GOOGLE_API_KEY=...
node scripts/render.mjs --prompt prompt.txt --ref face.webp --out out/a.png   # one frame
node scripts/render.mjs --prompt prompt.txt --ref face.webp --out out/b.png --passes 3
node scripts/render.mjs --text "<the edit instruction>" --ref out/a.png --out out/a-edit.png
```

An asset that is neither on disk nor buildable stops the run and names the file, deliberately:
the mood-board script skips a missing reference and renders anyway, which is how a frame comes
back carrying a mark nobody supplied.

## 7. Execute: designer handoff or programmatic render

**Programmatic render.** Nano Banana 2 through the app's own client, with the owned face
plates and 3D tiles handed in as reference images so identity is photographic and free:
[`rendering.md`](rendering.md).

**Designer handoff.** For a person building the frame in Photoshop, Figma or Affinity. Nothing
is re-decided downstream: a designer given "make it pop, systems vibe, our purple" invents a
composition and hunts for assets, where one given the sheet below opens the named files and
executes. Deliver it as one markdown file or a ClickUp task, with the reference images attached.

```markdown
# Thumbnail: <video title>
Due: <date> · Variant: face | faceless · Canvas: 1280×720 px, sRGB, JPEG ≤ 2 MB

## The one thing
The eye lands on <X>, and that tells the viewer <Y>. Everything below serves that sentence.

## Elements, in z-order
1. Background: <file path or "photograph: brief">. Treatment: <blur radius, dim %>.
2. Subject: <file path>. Scale: <% of frame height>. Position: <thirds intersection>.
3. Label: see Words below.
4. Accent: <one arrow / one badge / none>. Never more than one.
Total elements: two or three. A winner here carries one or two; our own control band
carries five to eight, the biggest single difference between our wall and theirs.

## Words
| | |
| --- | --- |
| String, exactly | `THE 2 MINUTE HABIT` |
| Case | ALL CAPS / lowercase / Sentence |
| Font | Manrope ExtraBold 800 (display). Never Satoshi on a thumbnail. |
| Size | Cap height ≥ 90 px at 1280 wide, so it survives 320 px |
| Fill | `#FBF3EF` Parchment |
| Plate | Solid tab `#F0503D` Terra Signal, 24 px padding, no radius |
| Placement | Top-left third, baseline on the upper third line |
| Second text block | **None.** |

## Colour
| Role | Hex | Note |
| --- | --- | --- |
| Working colour 1 | `#000515` Abyss Ink | background / plate |
| Working colour 2 | `#FBF3EF` Parchment | type |
| Accent, once only | `#414FD2` Command Indigo | arrow, badge, one glyph |
Two colours doing work, a third once. The frame has to fight the white YouTube UI.

## Assets
| Role | File |
| --- | --- |
| Face plate | the face shelf, filed by expression, e.g. `confident/confident-left-07.webp` |
| Product box | the owned-asset shelf |
| 3D tile | the 3D shelf |
| Screen capture | `<path>`: dim to 30%, must not be readable |
Copy-space in a face-plate filename names the **empty** side where the words go, so
`confident-left-07` has the subject on the right.

## Not in frame
The anti-patterns below. Why it wins: <the niche-evidence finding this bets on>

## Deliverables
- `thumb-<slug>-a.jpg`: this sheet
- `thumb-<slug>-b.jpg`: identical, words changed to `<string B>`
- `thumb-<slug>-c.jpg`: identical words, other variant (face ↔ faceless)
- Layered source file
```

## 8. Critique before delivery

Run this on the finished frame, not on the plan:

- [ ] At 320x180 the one thing from step 2 is unmistakable
- [ ] One or two elements, not five
- [ ] Exactly one person, or none. No second face anywhere
- [ ] Words obey the count law in [`copy.md`](copy.md), make a claim, and are not a restatement of the title
- [ ] No hype adjective, no client money, no numbered ramp of generic icons
- [ ] Nothing readable is asked of the viewer: no legible dashboard, chart or spreadsheet
- [ ] Two working colours; the plate fights the white YouTube UI
- [ ] Bottom-right 15% clear
- [ ] A rim light runs down the subject; the figure is not an evenly lit cutout
- [ ] Every floating object occludes, tilts, glows onto its neighbours and casts a shadow
- [ ] **Hands and any real logo checked at full resolution**, cropped and counted, not on
      the thumbnail-sized preview where a plausible silhouette reads as correct
- [ ] No mangled hands, eyes or glyphs
- [ ] Distinct from the last three published frames
- [ ] Every frame the run produced is filed on the concept, not only the pick
- [ ] New failure modes appended to Learned Patterns

Two or more failures means rebuild, not retouch. Review at 320×180 side by side and send one
consolidated list: three rounds of one note each and a designer stops reading. Two questions
settle most rounds: what the eye lands on first, and how many elements are competing.

## Anti-patterns

Each of these is a measured control marker in this niche, not an opinion:

- A second person in the frame
- A head filling the frame
- Somebody else's money: client MRR, a Stripe or PayPal notification, a revenue curve, cash
- A numbered ramp of generic icons: "PHASE 1..5", "STEP 1..4", "Stage 1 / 2 / 3"
- A halo of eight or more unlabelled icons around a head
- An adjective with no object
- A screenshot the viewer is asked to read
- A category label where a claim belongs
- Five to eight elements competing (our own house fault)
- Series numbering as the promise: "MINI COURSE DAY 1"
- Reusing one **layout** for every upload; CTR decays from pattern fatigue. Reusing the
  **treatment** (light recipe, palette, type system) is what makes a wall recognisable. See
  [`craft.md`](craft.md).
- Asking the user for reference thumbnails when `thumbnails.ts` builds both bands
- Copying a winner's composition without reading that channel's control band first

**This list is enforced, not just written down.** Every fault above has an id in
one fault list the generator reads, and a frame on the concepts page is crossed off
against them rather than deleted. The counts across the whole wall are handed to the concept
generator on the next draw, worst offender first. The anti-patterns measured on competitors
live here; the ones OUR frames keep shipping with are counted in the app. Add a fault in both
files in the same session.

And three craft faults, which are not claim faults:

- A subject with no rim light, sitting on the background as an evenly lit cutout
- An object beside the head at head scale, square-on to camera: a logo bug
- Everything on one depth plane, then deleting elements to fix the clutter
