---
name: youtube-ctas
description: "Builds the evergreen 1920x1080 transparent overlays a finished YouTube edit is dressed with, in Remotion: subscribe, like, comment, book-a-call and link-in-the-description pills, the channel lower third, and the end-screen bed. Use when a CTA, a lower third or an end card is needed, when an overlay renders without its alpha channel, when an overlay has to land where YouTube's own clickable elements go, or when adding a clip to the Design Assets shelf."
tags: [makes, remotion, youtube]
---

# YouTube CTAs

The kit lives in `src/youtube-ctas/` inside a Remotion project, at 1920x1080 rather than
1080x1920. It renders into the app's static folder and shows up on the design room page on the
next page load, and on the shared asset library once the app deploys.

It is not the b-roll skill and does not overlap it:

- Motion-graphic clips cut against a read: `motion-design`. That skill owns the palette, the spring
  vocabulary and the finishing rules, and this one inherits all of them.
- Remotion API questions: the `remotion` router and its references.
- Scheduling, encoding and filing the finished video: `shorts-production`.

## What separates an overlay from b-roll

Three things, and each one flips a rule that `motion-design` states:

1. **There is no read and no clock.** A CTA is dropped wherever the edit wants it. So there is no
   `beats.ts`, and the duration is a property of the ask, not of a sentence.
2. **It is reused for years across every video.** So it is worth more hand-tuning than a clip that
   serves one line once, which is why the whole kit is written in the Studio-editable inline form
   rather than behind shared constants. The reasoning is in `motion-design` under
   "Who is allowed to fine-tune".
3. **It has an alpha channel.** Everything below turns on that.

## Alpha

Every way an overlay loses its alpha channel, and the encode settings that keep it, are in
[`references/alpha.md`](references/alpha.md). This is the failure that survives every preview,
so read it before a render rather than after one.

## Placement and wording

Where each overlay sits against YouTube's own clickable elements, and the words it carries,
are in [`references/placement.md`](references/placement.md).

**An overlay rides the teach, it never interrupts it.** A viewer deep in a video has stopped
noticing they are watching one, and anything that breaks that frame wakes them up: a woken viewer
remembers they have work to do and leaves. So an overlay lands over a sentence that is still
running, never over a pause cut in to accommodate it, and it never gets its own scene.

Which overlay an edit gets is decided by the script, not here: `video-script` names the clips by
file name, and the outbound one belongs in the last twenty seconds. Where an unavoidable non-native
break exists, such as a sponsor read, it goes after the channel's average view duration so the
interruption lands on viewers who were leaving anyway.

## The house rules this kit adds

- **One `interpolate()` per CSS property, with the exit as extra stops.** Two calls on the same
  property means the second silently wins, and in the Studio a property with two sources cannot be
  keyframed at all. Four stops, `[0, in, durationInFrames - n, durationInFrames - 2]`.
- **`boxShadow`, never the `glow()` filter, on anything containing type.** `filter` applies to the
  whole subtree, so a glow on a pill haloes the word inside it and the text goes soft. This is the
  `Plate` lesson from `primitives.tsx`, solved without needing `Plate`.
- **Hierarchy comes from size, and terra marks exactly one clip.** The hero is 204px tall and the
  pill is 116px; that is the hierarchy, and it needs no second hue to state it. Terra appears on the
  discovery call's icon disc and nowhere else, because that is the one ask for money. The whole slab
  in terra was rendered rather than argued about, and it fails: over footage the translucency drags
  it to brick and the glass edge stops reading, which is the banner-ad failure DESIGN.md already
  recorded on the website, in a different room. A sand fill was tried earlier for a secondary ask
  and rendered as a flesh-toned disc that pulled the eye off Subscribe entirely.
- **A handle is never uppercased.** Every other label in this project is tracked-out caps, but a
  YouTube handle is a literal string a viewer types into a search box, and an uppercased one is not that
  string. Type rules stop at anything the viewer has to reproduce.
- **One ring, not a repeating pulse.** A loop needs modulo arithmetic, which the Studio cannot
  keyframe, and a CTA that keeps pinging outlives its welcome inside two seconds. The subscribe unit
  has no ring at all: it would have to sit outside the glass pane, which clips its own sweep, and
  outside the pane it needs absolute coordinates that move with the handle string. A signal that
  silently mislands on one of two clips is worse than no signal.
- **Never build a colour by appending a hex alpha to an `oklch()` string.** `` `${disc}73` `` yields
  `oklch(...)73`, which is invalid, and *one* invalid value drops the whole `box-shadow` list — the
  disc's rim and thickness with it. It renders clean, exits zero, and looks like nothing was set.
  Write the alpha inside the function: `oklch(0.65 0.2 30 / 0.45)`.

Publishing a finished overlay to the shelf is in
[references/publishing.md](references/publishing.md).

## Execution flow

1. **Pick a shape before writing anything.** A new ask is almost always a `CtaPill` or a `CtaHero`
   in `src/youtube-ctas/glass/` with different props, not a fourth component. Write a new one only
   when the ask needs a mechanism the three do not have, the way Subscribe needed a button that
   presses. Inside a shape: inline styles, inline `interpolate()`, `Interactive.Div` with a
   hardcoded `name` on anything worth grabbing. Shared surface values go in `glass/surface.tsx`,
   never copied into a second shape.
2. Register it in `Root.tsx` under the `youtube-ctas` folder, written out rather than mapped, with
   `calculateMetadata={alphaPreviewWebm}` and inline `defaultProps`.
3. `pnpm typecheck`.
4. Render a still at each phase, composite it over a mid-grey, and **look at it**:
   ```bash
   npx remotion still src/index.ts <CompId> out/cta-stills/<CompId>-<frame>.png --frame=<frame>
   ffmpeg -y -f lavfi -i color=c=0x4a5560:s=1920x1080 -i in.png \
     -filter_complex "[0][1]overlay" -frames:v 1 flat.png
   ```
   A CTA reviewed on a white page or on black lies about its contrast, because it is designed for
   neither.
5. Add the beats to the composition with `<Sfx>`, then `pnpm build:sfx` if the kit changed. The
   three sound kits, what separates them and how to generate a sound that no oscillator will write
   are in [references/sound.md](references/sound.md); where the sounds go in a finished edit, how
   loud and how often, is in [references/sound-layout.md](references/sound-layout.md).
6. `pnpm render:youtube-ctas-mov` for the deliverable, `pnpm render:youtube-ctas` for the preview.
7. Run the alpha checks and the transient check above on at least one output.
8. Load `/design/youtube` and confirm the clip plays on the shelf. Deploy the app to put it on the
   shared library at `/assets/youtube` too.

## Verification checklist

- [ ] The MOV reports `qtrle,argb` and an empty corner decodes `srgba(0,0,0,0)`
- [ ] The preview WebM reports `alpha_mode: "1"` and a zero alpha byte in an empty corner
- [ ] An audio track is present and every transient lands on the frame the component names
- [ ] Nothing in the bottom 90px or the top-right corner
- [ ] End-card geometry matches the coordinates above, and it has no exit
- [ ] One `interpolate()` per property, exit folded in as extra stops
- [ ] No `filter` on any element that contains type, frost included
- [ ] Every wrapping curve is concentric with the curve it wraps: inner radius + its padding
- [ ] No colour built by appending a hex alpha to an `oklch()` string
- [ ] Frost grain is at or under 6%
- [ ] A still of every phase was composited over mid-grey and looked at
- [ ] Every MOV is under 25MiB, and any product box carries its own product's mark
- [ ] `gen:design-manifest` was re-run, and the clip plays on `/design/youtube`
