# Sound, and verifying by watching

The audio kit, then the loop that catches what a clean render and a clean typecheck cannot: whether
the graphic is actually on screen, on time, and right.

## The sound kit

Keep **one roster of every sound file** with an id and a job per entry, and cut your motion kit's
voices from it, so the sound a clip names is the same sound every time. The kit this skill was
measured on is eleven effect voices cut from twelve sounds that two finished edits actually used,
plus two sine mark voices:

`tick` `dot` `click` | `enter` `exit` `sweep` `climb` `release` | `sub` | `shine` `settle` | `stamp` `bloom`

**Why the oscillators went, 8 Sep 2026.** The kit was seventeen sine voices on one chord: *"I don't
like the sounds used in the motion design. These are not classical YouTube video editing sounds."*
Checkable, not taste - a human edit puts almost nothing in 600-4000Hz (where a voice carries its
intelligibility) and splits its events into air above and weight below, while the sine kit sat at 20%
presence with zero energy above 2.5kHz, reading as UI rather than an edit.

**Six rules the kit is built on:** nothing in 600-4000Hz; the split is by family (every arrival/payoff
is air, every move is weight), not by voice; noise is the instrument, pitch is the exception (the
chimes, at 4-14kHz); no synthesised room, because an oscillator cannot write one a microphone heard; a
voice joins the kit when a finished cut used its source, membership is a census; one name, one
instrument - a quieter or shorter version of an existing voice is `volume` on `<Sfx>`, never a new
name. The one exception to rule 1 is `climb`, a riser that sweeps through the band by nature.

**The kit was then cut from eighteen names to thirteen** (readout, signature, snap, tap, pop merged or
dropped) because five were versions of a voice already there rather than real jobs: `tap` measured
53% inside 600-4000Hz, the band this file exists to keep empty, so it became `dot`; `pop` measured 77%
under 160Hz, so it became `sub` with a transient. A voice's call count is read out of `src/` on every
run, so **a voice at zero is the next one to go**.

**Two alternative kits, cut from a 25-sound Mixkit pool, lost the audition to the census kit**:
*"I think the ones of today are actually good"*, and then, on the census kit itself, *"but maybe we
have a little bit too many"* - the ruling that drove the eighteen-to-thirteen cut above.

Verbatim, 28 Aug 2026, on a trend chart under `sweep`: *"the sounds you added don't convey the right
thing ... here it's not conveying growth. The shape motion should follow the sound."* **Match the
voice's contour to the graphic's shape**, not just its frame: grows/climbs/fills →
`climb` (cut to *end* on the beat); passes/scans/moves laterally → `sweep`; lands/arrives → `click`
(+`sub` with weight); one small repeated event → `tick`; leaves/empties → `release`/`exit`;
resolves/holds → `settle`. A shape no voice matches gets a recorded source added to
the roster, never a new oscillator.

`<Sfx name="click" from={LANDS} />` (one `<Sfx>` component per project). **`from` takes the same named constant the
animation reads, never a literal**, or the sound drifts the frame somebody nudges. The motion is cut
to the sound, not scored after. One voice per event, never one per object (five staggered bricks are
five `click`s; one sweep lighting five cells is one `sweep`). Nothing repeats more than four times in
a clip.

**The licence.** Stock-library tiers differ: a pack cleared for monetised YouTube may need on-screen credit and
usually does not cover a client delivery. **Neither a free nor a creator tier covers a client deliverable or a paid ad** - a
rendered clip carries its sound inside the file. A paid stock plan or a commercial-use free library is the fix.

## Comments carry the reasoning

Every clip opens with the line it serves in quotes, its timecode, and a `WHY` paragraph per real
design decision - not what the code does, why this reading beat the alternative. When the author overrules
one, the comment is rewritten to record the reversal, not deleted.

## Verify by looking

Typecheck proves nothing about whether a graphic appears. Render a still at the frame each phase
resolves and open it:

```bash
npx remotion still src/index.ts <CompId> out/stills/<CompId>-<frame>.png --frame=<frame> --log=error
pnpm typecheck
```

Check every phase, not just the last: anything supposed to be lit, connections supposed to be drawn,
anything off the edge of the frame, anything present that is not a graphic (an unbraced JSX comment
renders as text). **Count the marks** - past about seven the frame has stopped being a diagram, which
fails whatever else it passes; `storytelling.md` holds the count. A still cannot show the encode, the
alpha, the audio or a cut, so the rendered file gets watched too, below.

## Watch the render, then fix, then render again

The loop a human editor runs: render, watch it back, list what looks wrong, fix, render again, until a
pass returns nothing. **Run the mechanical checks first, because they are free and eyes are not**:

```bash
W=scripts/watch.py   # relative to this skill folder
python3 $W out/CompId.mp4 --assert --expect-frames 240   # alpha exists, right length, no empty frame
python3 $W out/alpha/CompId.mov --assert                 # alpha required, from the filename
```

It remembers each file's hash and verdict in `~/.cache/motion-watch`, not beside the render (a sidecar file next to a deployed asset would
deploy with it). A keyed webm keeps its alpha in
a VP9 side channel that `ffprobe` reports only as `alpha_mode=1`; `--assert` forces `libvpx-vp9` to
read it, or an overlay that lost its channel passes silently at 100% opacity everywhere. Cut every
still with the same decoder for the same reason: on 30 Aug 2026, twenty of thirty posters on a style
grid were cut with the default decoder and every one showed a fade or a rule wrong that the clip
itself drew correctly - **measure a finding from a decoded frame and the template's own constants,
never from a contact sheet.**

```bash
python3 $W out/CompId.mp4 --sheet                 # the whole clip at a glance, plus _sheet.jpg
python3 $W out/CompId.mp4 --fps 4 --range 1.5-3   # the stretch a review flagged, in detail
python3 $W out/cta.mov --sheet --bg 0x101820      # alpha, matted over the colour it will key onto
```

Read `_sheet.jpg` first. **Run each clip's review in a subagent**: it opens the frames and hands back
timecoded fixes; the building session never loads the images. In order: present; inside the frame
(nothing below y=1650, nothing under the caption band); readable at size; resolved before the cut;
the idea, not the decoration.Every correction made at final review goes into your own notes before the clip closes out.

**A sheet is not a video.** Late against the read, still moving at the cut, a stretch with no b-roll,
a set that stopped reading as one hand: properties of TIME, invisible to any arrangement of frames.
Hand the whole file, with its audio, to a video-capable model and ask for timecoded notes. **The
verdict is binding.** A note that survives a re-render is either fixed or answered in the WHY
comment; dropping one silently turns the review into theatre. Make it state the file's duration, and
check that against ffprobe: a review that misreports the length did not watch the file.

## Verification checklist

- [ ] Your clip library was searched before any clip was designed
- [ ] `plan.md` exists, covers every sentence in the cut, states the coverage percentage
- [ ] No register repeated past the point where it reads as a template
- [ ] No stretch over 45s without b-roll, none over 25s without his face, no two clips back to back
- [ ] Every clip's header answers what it adds that the sentence did not say
- [ ] Sound is cut from the same named constants as the picture, one voice per event
- [ ] The clock came from the cut's SRT, re-checked before naming
- [ ] Three designs per beat, identical frame counts
- [ ] Real logos and real terms wherever the thing being drawn exists
- [ ] A still was rendered and looked at for every phase of every clip, in both frames
- [ ] Four files exist per landscape clip: wide opaque, wide alpha, narrow opaque, narrow alpha
- [ ] The wide still is byte-identical before and after the narrow variant was added
- [ ] Any borrowed shot is in `sources.json` and its destination check exits zero
- [ ] Every rendered file passed `watch.py --assert` and the last pass returned nothing
- [ ] The joined cut was watched end to end, every note fixed or answered
- [ ] Nothing sits below y=1650 that the viewer needs to see
- [ ] Every portrait render passed `scripts/deadzone.py --for reels` and `--for tiktok`
- [ ] Every clip's last element resolves before the cut, with hold frames after it
- [ ] New failure modes from this run were written into your notes
