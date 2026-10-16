# The product CTA, and what QuickTime Animation charges for it

`CtaProduct` is the one shape in the kit whose subject is an object rather than an action. There is
one per sellable system - six of them - and they live in `src/product-ctas/`, not
`glass/`. It stands on `CtaHero`'s pane unchanged -
radius 102, `40px 100px` padding, 84px statement, 25px indication - because the ask is the same
weight as the discovery call and drawing it differently would say it was not. Only the left padding
grows, to 92, so the type clears the box standing in front of the pane rather than an icon disc
sitting inside it.

## The box is geometry, not a packshot

A packshot is one frozen angle. A CTA has about a second to make a product read as something you
could pick up, and off a bitmap the only camera move available is a fake parallax that reads as a
sticker. So the box is three CSS 3D faces with one animated `rotateY`, and the light lands
differently on each because they genuinely face different ways.

Three things fall out of that, and none of them is available from an image:

- **The product signs with its own mark where it has one, and with a considered glyph where it does
  not.** The shipped packshots carried a placeholder rocket and a placeholder grid on the two
  products that *do* have marks, and the decision to replace them outlived the pixels because the
  pixels were baked. The recording-backgrounds builder already owns which mark each
  signs with - the angular AM monogram, the ClickUp symbol - and `product-ctas/marks.tsx` is a
  transcription of its geometry, plus the Claude asterisk. Re-key from there, never the other way
  round. The three products with no mark of their own take a Phosphor glyph from the kit's one icon
  home, `glass/icons.tsx`, rather than a second icon module. What is banned is a stock glyph
  standing in for a mark that exists.
- **`PRODUCT_ART` is the one home for name, spine, tile, surface and bloom.** `surface` picks the
  foot lockup - "FOR CLICKUP" with the ClickUp gradient, "FOR CLAUDE" with the asterisk in clay -
  and `bloom` is a full colour rather than a hue angle, because at thumbnail size it is the only
  thing separating six otherwise identical boxes. Names break where the packshots break them, and
  the name's size is chosen from the line count, so one word and three words fill the same block.
- **The box hangs from the block's bottom edge, not centred on `BLOCK_CENTRE_Y`.** A 440px object
  centred there puts its foot and its contact shadow inside YouTube's controls. Only the box moves;
  the pane stays exactly where every other CTA's pane is.
- **The same component renders the shelf's still**, at packshot scale on transparency, under
  the motion project's `render:product-boxes` script. That is the whole reason the still
  composition exists: the clip and the still cannot show two different objects.

The box overhangs the pane rather than sitting inside it. A product that fits neatly in its
container reads as an illustration of a product. That also sidesteps the concentric radius rule
rather than breaking it: the box is in front of the pane, not a round child inside it, so there is
no second curve to share a centre with.

## Three 3D mechanics the rest of the kit never needs

- **A face transform must be `transform`, not the individual properties.** A face is
  `rotateY(-90deg) translateZ(...)` *in that order*, and `rotate`/`translate`/`scale` apply in the
  fixed order translate, rotate, scale. There is no way to say "rotate, then walk along the new
  normal" with them. Face transforms are static, so no keyframe is lost.
- **An animated rotation about Y must also be `transform`.** Remotion's string `interpolate()`
  parses only a bare `<n>deg`, so `["y 48deg", "y 23deg"]` throws *"y" is not a supported scale,
  translate, or rotate value* - it cannot tell an axis keyword from a unit. A **static**
  `rotate: "x 5deg"` is plain CSS and Chrome takes it; an animated one names the axis in the
  template.
- **Scale the stage, never anything inside the 3D chain.** CSS `scale` is 2D and leaves z alone, so
  scaling the box shrinks the faces while the depth stays put and the box comes out deeper than it
  is. Scaling the whole perspective container scales the projection instead, shadow included.

Two more, from the same family of silent failures: Chrome drops a `box-shadow` on any child of a
`transform-style: preserve-3d` parent, so the contact shadow is a painted radial-gradient element;
and `backdrop-filter` returns the blur of nothing on an alpha overlay, so the box is opaque and the
glass is rebuilt out of parts that survive an alpha render.

## The size budget, which is real and which nobody sees coming

The shelf deploys to Cloudflare Workers, whose static assets are capped at **25MiB each**. A clip
over that ships everywhere except production. Three measurements, all on the Agency Master clip:

- **ffmpeg's qtrle encoder writes a full keyframe every 12 frames.** On a clip that is dead still
  after frame 19 that is ~1MB of pure redundancy, ten times over. `-g 600` in the mux step takes
  the *whole kit* down by about a third - the end card went 14.8MB to 8.7MB - with identical
  pixels. This is in `render:youtube-ctas-mov` now; do not drop it.
- **A dense gradient in ARGB has no runs, so an opaque box is stored raw while it moves.** The
  pane, whose rows are long flat runs, costs almost nothing by comparison. The budget is therefore
  *box area multiplied by the number of frames the box is in motion*, and nothing else in the clip
  is close.
- **The pane, not the box, is usually the bill.** Frost grain has no runs at all, so every frame a
  pane fades or scales through is stored whole - and a `CtaProduct` pane is the widest in the kit
  because its statement carries a product name. On Build Your Own Software the kit's standard
  18-frame settle was **14.1MB of a 30.5MB file by itself**, more than the box the clip exists to
  show. A 10-frame settle takes it to 23.3MB.
- That is what sets this shape's clock: the type resolves at frame 6, the box waits until 18 so it
  is the only thing repainting while it lands at 32, a **10-frame settle** and an **8-frame exit**
  rather than the kit's 18 and 16, and `BOX_SCALE` at 0.8. Waiting also stages better: the surface
  arrives, then the product lands on it, which is the order the subscribe unit uses for its button.

- **The glass sweep was the other half, and it is the kit's, not this shape's.** Thirty frames of a
  light band crossing a wide frosted pane repaints the grain under it every frame: 14MB of a 24MB
  file on `cta-call` and `cta-coaching-call`, which is what kept both over the ceiling after the
  settle was already fixed. Eighteen frames takes them to 22.8 and 22.5MiB, and a glint that took a
  full second was reading as a wash anyway.

The order to check things in, because the first guess has been wrong every time: **measure the
per-frame packet sizes before changing any art.** `ffprobe -show_entries packet=size` over the MOV
and bin it by phase. Still frames cost zero, so the bill is always some region moving, and it has
turned out to be the pane twice and the box never.

`scripts/verify-youtube-ctas.sh` gates the ceiling now, because nothing local shows it: over 25MiB
wrangler rejects the upload and **the whole app's deploy fails**, not just that clip.

Still frames cost zero bytes, so **duration is free and motion is not**. A continuous six-degree
drift across the hold - added first on the argument that an object on screen for four seconds goes
dead without one - cost 8MB and bought nothing the pane's own sweep and the box's specular pass at
frame 34 do not already give. In this format, stillness is a budget.

## Levels

Stacking `sweep` on `shine` and the tail of `snap` peaked the mix at -7.9 dBFS against the kit's
-9.0. `sweep` at 0.5 puts it back at -8.2. Measure rather than listen once; the check is in
`scripts/verify-youtube-ctas.sh`.
