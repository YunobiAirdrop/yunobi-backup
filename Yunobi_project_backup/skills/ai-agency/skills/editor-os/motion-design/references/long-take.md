# The long take, and the live screen

Two landscape registers, each measured frame by frame off a reference film rather than recalled.
Where the b-roll rules describe a **cutaway** - three to six seconds, one subject, a fresh empty frame
every time - the long take is a **continuous canvas** the camera travels for ten to fifteen seconds
with no cut, and the live screen is a **static real interface** whose own state change is the beat.
Neither replaces the cutaway; each is the register the cutaway cannot do.

## The long take

Read it when a beat is an argument with more than one step, when a set plays as a slideshow of correct
diagrams, or when a graphic must carry a number, a comparison and a conclusion in one breath.

**The reference is `youtube.com/watch?v=5-EFvUKqZmA` from 1:14**, torn down with `ffmpeg` frame
extraction and phase correlation. The camera move is the argument's connective tissue: "and that
means" is not said, it is 900 pixels of travel to the right, and the cut back to his face comes after
the payoff, never inside it.

**What the teardown found:**

1. **The camera never comes to rest.** Phase-correlated residual is never zero across four sampled
   sequences: 0.10-0.31% of frame width per frame, ~0.2% typical. A frame that stops reads as a slide;
   one that never stops reads as a camera.
2. **The settle constant is τ ≈ 0.5s, shared by everything.** A dolly accelerates 15 frames (0.5s) to
   a peak then decays exponentially, τ measured at 0.28-0.76s across sequences. The same constant
   drives a counting number and settling type. Roughly 1 part acceleration, 4 parts settle.
3. **Two speeds, not five.** Big travel 4.0-4.2%/frame ("going somewhere new"), drift 2.8%/frame
   ("following the argument"), residual 0.1-0.3% ("alive").
4. **The ground is mid-grey, panels are the light thing.** `#6F6F6F` to `#C8C8C8`, two gradients
   multiplied (not one radial: a single ellipse cannot give both the horizontal swing and vertical
   softness). The hotspot moves between shots, matching `<Shot lightY>` on a pale ground.
5. **Type is a live text flow, laid out per word.** Words arrive 100-170ms apart, each larger, lighter
   and blurred, travelling into place while it darkens and shrinks; the block re-lays out as each word
   lands. This is sentence-case, set-to-be-read type - legal here because the sentence is the
   **conclusion the read has not reached yet**, landing after the evidence, not alongside it.
6. **A counter starts at half the target, accelerates, decays on τ, lands exactly on the round
   number** - $5,006 to $10,000 over 2.3s. Starting at half rather than zero makes the first frame a
   plausible number rather than a spinner.
7. **A comparison is a visual rhyme, not a split screen.** Same card, position and connector geometry
   twice, recoloured, so the difference *is* the content. The same device runs at film scale: one rail
   built once, revisited four times at different tiles.
8. **The real UI, rebuilt as vector, not a screenshot** - so it can be lit, blurred, moved in depth
   and typed into with a live caret. Promoted to the whole frame with the camera held still, it becomes
   [the live screen](#the-live-screen) below.
9. **A held comparison, camera barely moving, gains labels on the word rather than travelling.**
   Measured off a second reference at 1:30-2:11: every slot drawn empty before it fills; one label per
   phrase landing within about two tenths of its own word; the label is the compressed noun, never the
   clause ("40x more followers", not the sentence); the move between two objects is a fast blurred
   whip, not a dolly. Built at 12s against a 41s reference, an early cut lost the two **return** legs -
   the camera conceding one point before the second overturns it. The author, 28 Aug 2026: "the anchor
   comparison lasted more than half a minute." The fix used five stations, not three, and a label
   every 50 frames rather than every 18. Reach for this shape when the read spends thirty seconds or
   more on one comparison; reach for the travelling shape when the argument moves through places.

**Building one.** `src/specimens/LongTake.tsx` is the worked example. Ground:
`<Shot ground="daylight" cameraX cameraY>`, key light white and dropped to about a fifth (the wall
carries its own hotspot), `Ambient` swapped to a white wash. Camera: one `<Canvas>` per sequence wider
than the frame, elements at absolute world coordinates; the camera is a transform on the canvas, never
per-element - elements do not enter, the camera arrives at them, and nothing in the world has an
entrance (a fade-in timed to the camera's arrival renders as a grey wall with a line across it
mid-move). Three primitives, all in `motion.ts`: `settle(frame, from, to, at)` at τ=0.45s; `countTo`
(starts at half, decays on τ, lands exact); `wordFlow` (the measured per-word transform and blur, laid
out in a real wrapping flex row). Never hard-cut the camera inside a sequence.

**The clock**: establish 15%, build (elements land, numbers count, connectors draw) 45%, conclude
(sentence writes itself) 25%, pull back and hold 15%. `HOLD` (18 frames) is still the floor on the
tail.

**What does not carry over**: the palette is Meta's because the subject was Meta - map the structure
onto brand tokens directly, never copy the hex. A long take costs more than four cutaways: one per
video, on the beat that carries the argument.

**Measurement kit**: `python3 scripts/teardown.py sheet|camera|ground src.mp4` reproduces the whole
teardown in about ten minutes, and camera/ground both take a `--ss` timestamp. Run it on your own
render too, not only the reference - `SpecLongTake` measures 0 hard cuts, τ=0.46s, a residual that
never rests, and a ground swing of 75 against the reference's 76.

## The live screen

A real product interface, at poster scale, filling the frame, where the interface's own state change
is the whole beat - no window, no ground, no shadow, no pointer. The viewer is put inside the page,
not shown it. Read it when the proof of a claim is a screen somebody will recognise.

**The reference is `youtube.com/watch?v=SFRXddv7XfE` at 2:29.67-2:45.70**, measured frame by frame.
Sixteen seconds, two cuts total, both around a face beat:

| | frames | what it is |
|---|---|---|
| Visit one | 295 (9.83s) | page arrives empty, gets annotated, then loads. No cut. |
| Face beat | 32 (1.07s) | full-frame face |
| Visit two | 154 (5.13s) | same page, pushed in, section swap, selection lands |

**What the teardown found:**

1. **The page is the frame and is cropped on two sides.** Roughly 250% zoom with the window thrown
   away - a screenshot is looked *at*, a page at this scale is stood *in*, and it survives a phone.
2. **The query is already typed.** No typing, no pointer, nobody operating anything - the screen is
   caught mid-use, never demonstrated.
3. **The annotation is a second voice and the only thing that glows.** Monospace mint (`#2EE3BF`),
   one-lit-thing spent on the layer that is ours, not the product. A lead line reveals one whole word
   every 6 frames; notes under it reveal one character per frame, both at the same underlying ~22
   chars/sec so neither reads as a different speed. A note starts before the line above it finishes.
4. **The annotation clears, then nothing happens for 17 more frames** before results arrive - deleting
   this pause is the first cut a session makes and the one that breaks the beat.
5. **The page loads the way a page loads**: three rows land three frames apart, the whole plate
   settling up about 5% of frame height, complete 27 frames after the first row.
6. **Then dead still for 99 frames**, no drift, no breathing - only a blinking caret at a 32-frame
   period keeps it from reading as a screenshot.
7. **The only cut is the one that lets the page move** without the viewer seeing it move between
   visits.
8. **The section swaps by cross-dissolve over 24 frames, and the old page never fully leaves** - still
   faintly readable (~12%) eighteen frames later. The one cross-dissolve this register allows, because
   it is a page replacing itself, not a shot transition.
9. **The selection is the payoff and lands before the sentence names it** - a highlight band arrives
   in 4 frames (never a left-right drag), seven tenths of a second **before** the matching words are
   spoken, so the graphic gets there first.
10. **The plate**: ground `#383A40` to `#2E3034`, a 90% falloff; a 2px scanline at five levels,
    invisible on a still; not tilted (0.009° measured); the only saturated things are favicons and
    link blue.

**Where the reference gets it wrong**: its annotation restates the read nearly verbatim at 2:29,
breaking the redundancy principle in the most expensive place. Copy the device, not the copy - the
annotation carries what the screen cannot show and the read does not say.

**Building one.** `src/anchors/LiveScreen.tsx` is the worked example; `design.ts` section C carries
every number above. Frame is `1920x1080`. `screenCore/Edge/Panel/Ink/InkMuted/Scanline` in `tokens.ts`
are the measured plate, with no hue - do not tint them. `MONO_FONT` for the annotation: a fixed
character advance is what makes a one-character-per-frame reveal read as a machine writing. No alpha
variant - the frame *is* the screen, there is no ground to key out. Words are props (query, lead,
notes, rows, answer, citation) - re-render with your own content rather than forking the file.

**The one thing to get right first: the artefact has to be the real thing.** Real favicons, URLs,
titles, answer text - a plausible search naming real companies is a forgery whatever it was built for.
Take real ones off a real search before the clip ships.

**What does not carry over**: it runs under a continuous voice - timed against silence it is 30% too
slow. The face beat needs the raw take marked out at the right size.

**Measurement kit**: `python3 scripts/teardown.py cuts|palette|sheet ref.mp4`. For a reveal type
(word vs character), sample the rightmost lit pixel per line band per frame - a staircase landing on
word boundaries is a word reveal, a straight ramp is a character reveal.
