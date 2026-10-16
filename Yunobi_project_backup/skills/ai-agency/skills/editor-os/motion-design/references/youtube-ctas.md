# YouTube CTAs

The evergreen 1920x1080 transparent overlays a finished YouTube edit is dressed with: subscribe,
like, a link to a booking page, a product ask. Built in Remotion, reused for years. This isn't a
clip cut to a sentence, so most of this skill's clock and planning rules don't apply, but its
palette, motion vocabulary and finishing rules do.


## What separates an overlay from a clip

1. **There's no read and no clock.** A CTA is dropped wherever the edit wants it, so the duration is
   a property of the ask, not of a sentence.
2. **It's reused for years.** That's worth more hand-tuning than a clip that serves one line once.
   Write it in the inline form (inline `style`, inline `interpolate()` with hardcoded ranges) so you
   can nudge it by eye in Remotion Studio. See [craft.md](craft.md) on who may fine-tune.
3. **It has an alpha channel**, and alpha fails silently. Read [alpha.md](alpha.md) before the first
   render, not after.

## Where it goes

**An overlay rides the teach, it never interrupts it.** A viewer deep in a video has stopped noticing
they're watching one, and anything that breaks that frame wakes them up. A woken viewer remembers they
have work to do and leaves. So an overlay lands over a sentence that's still running, never over a
pause cut in to make room, and it never gets its own scene.

The outbound ask belongs in the last twenty seconds. If a non-native break can't be avoided, such as a
sponsor read, put it after the channel's average view duration so it lands on viewers who were leaving
anyway. Keep the middle of an end card empty if the presenter's face sits there, and keep clear of
YouTube's own clickable elements.

## House rules

- **Three shapes, one hierarchy.** A hero (tall, an ask with an address on a second line), a pill (one
  line, one badge) and a subscribe unit (avatar, handle, a button that presses). Size carries the
  hierarchy, so it needs no second colour to state it. Reserve the one accent for the one ask for money.
- **One `interpolate()` per CSS property, with the exit as extra stops.** Two calls on one property
  means the second silently wins, and Studio can't keyframe a property with two sources.
- **`boxShadow`, never a `filter` glow, on anything containing type.** A filter applies to the whole
  subtree, so a glow on a pill haloes the word inside it and the text goes soft.
- **A handle is never uppercased.** It's a literal string a viewer types into a search box.
- **Nothing touches the frame edge, not even a shadow.** Hang the block clear of the bottom edge, rise
  a few pixels under the fade, and ease the exit in so a spring can't overshoot toward the edge. Check
  that alpha is 0 in a band round the frame on every frame, in and out animations included.
- **One ring, not a repeating pulse.** A loop needs modulo arithmetic Studio can't keyframe, and a CTA
  that keeps pinging outlives its welcome in two seconds.
- **Never build a colour by appending a hex alpha to an `oklch()` string.** `` `${disc}73` `` is
  invalid, one invalid value drops the whole `box-shadow` list, and the render exits zero looking like
  nothing was set. Write the alpha inside the function: `oklch(0.65 0.2 30 / 0.45)`.
- **Review over mid-grey.** Composite a still of every phase over a mid-grey and look at it. A CTA
  reviewed on white or black lies about its contrast, because it's designed for neither.

```bash
npx remotion still src/index.ts <CompId> out/cta-stills/<CompId>-<frame>.png --frame=<frame>
ffmpeg -y -f lavfi -i color=c=0x4a5560:s=1920x1080 -i in.png \
  -filter_complex "[0][1]overlay" -frames:v 1 flat.png
```

## Before it ships

- [ ] Every MOV is `qtrle`/`argb` for a timeline, and a keyed corner decodes `srgba(0,0,0,0)`
- [ ] Alpha is 0 in an 8px band round the frame on every frame (end cards are opaque beds, the exception)
- [ ] An audio track is present and every transient lands on the frame the component names
- [ ] One `interpolate()` per property, exit folded in as extra stops
- [ ] No `filter` on any element that contains type
- [ ] A still of every phase was composited over mid-grey and looked at
- [ ] Every file is under your host's size cap
