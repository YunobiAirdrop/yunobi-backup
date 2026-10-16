# The product film

A self-contained film, not a clip cut into a read: 60 to 120 seconds, no voice-over, no cuts, one
music bed, the product the only actor. Everything below is measured off one reference, a launch
film for a table-based research product, 95.3s, 60fps. `scripts/teardown.py` reproduces every
number here from any mp4; run it on a film before copying its look, because taste arguments end the
moment somebody has the bar length.

The rest of the skill takes its clock from the cut, and its central law is that a graphic must not
repeat the sentence. Here there is no sentence. The graphic **is** the argument, the type is the
only voice, and the clock comes from the music. Given the clip-cut-to-a-read playbook, a session
builds fifteen independent scenes and cuts them together: the failure this file prevents. The
reference film has **zero cuts in 95 seconds**.

## The five structural laws

### 1. No cuts. One camera, one canvas.
`ffmpeg` scene detection finds zero cuts at a 0.06 threshold across the whole 95 seconds. Not "few
cuts". None. Every change of subject is a **move**: a push in, a pull back, a lateral drift, a rack
focus, or a wipe by the gradient. Build one large canvas and fly a camera over it. A scene that has
to appear from nowhere fades up inside the moving frame rather than replacing it.

**A cut tells the viewer the last shot is finished. A move tells them it is the same world.** That
is the entire reason 95 seconds holds without a face or a voice, the same failure `storytelling.md`
names for a set of clips, at film scale.

### 2. The bar is the edit unit.

Tempo 133.3 BPM, beat 0.450s, **bar 1.80s**. Across 32 measured typographic cards the line-to-line
cycle clusters at 1.70 to 1.78s. One card, one bar. The lines that carry the argument get two bars
(3.47s, 3.57s, 4.32s measured). Nothing gets less than one.

The film is cut to the bar **length**, not snapped to the downbeat: measured phase against the beat
grid scatters ±0.25 beat, and with no cuts there is nothing to snap. The rhythm is carried by **how
long a thing stays**, never by when it hits. Pick the track first, measure its bar, and build
`beats.ts` as multiples of it. Never compose to a round number of seconds and hope the music fits.

### 3. Inside the bar: 0.3 in, 1.0 hold, 0.2 out, 0.2 empty.

Measured on the opening card and consistent through the film. **In 0.3s**, fast, not a leisurely
fade. **Hold 1.0s**, the line sits still and does nothing, most of the bar. **Out 0.2s**, faster
than the in: weight arrives, weight is taken. **Empty 0.2s**, a real gap of blank frame between
lines, measured 0.08 to 0.55s, typically 0.20s.

The empty gap is the one people cut and the one that matters. Crossfading line A into line B reads
as one thought being edited; a gap of nothing reads as a new thought. `DEPART` in `motion.ts` is
heavier than `ENTER` for the same reason; this is its timing version.

### 4. Claim, then proof, seven times over.

The whole 95 seconds is one loop, run seven times: **a typographic claim** (one bar, blank frame,
one centred line, no product visible), then **the product doing exactly that** (four to eight
seconds, real UI at real size, a cursor driving it).

Claims may run in pairs, a setup and its turn: "Don't call the main line." then "Directly." The
reference hits **three in a row twice**, its own ceiling: past three the type has outrun the product
and the film has become a manifesto. Never show a feature without a line naming what it is for.
Measured split: roughly **three seconds of product for every two of type**. The claim is written to
be falsified by the next five seconds, so the viewer reads the screen as evidence rather than a
screenshot. A feature tour without the claim line is a screen recording.

### 5. One word carries the highlight.

Each claim line is plain near-black type except for **one word** that takes a pale tinted rounded
rectangle behind it, wiped on from the left in about 0.2s, landing after the line has already
settled. Measured on `Directly.`, `already` in "Every tool you already use.", `CRM` in "One click
into your CRM", `LinkedIn` in "Reveal them right inside LinkedIn". One word, never two: the
highlight is the film's only emphasis device, so spending it twice spends it on nothing.

The same device does the film's cleverest trick: the highlighted word **swaps in place** while the
rest of the line stays fixed, "Do all your `prospecting` in the product." → `lead research` →
`lead generation` → `go-to-market`, four positionings across three bars, the sentence never moving.
A structure neither a sentence nor a voice-over can do: the fourth item on the value test.

## The six moves, and nothing else

The film's whole transition vocabulary. Reusing them, not inventing a seventh, makes 95 seconds read
as one hand.

1. **Push-in / pull-back.** The workhorse: scale the canvas continuously through a beat. The film's
   best moment is a pull-back from a focused row into the full 247-row table, the same object,
   re-scoped.
2. **The focus stack.** A vertical list: the row at frame centre is sharp, the rest fall off in blur,
   opacity and scale with distance. A depth-of-field rig, not a highlight.
3. **The gradient wipe.** A blue silk mesh gradient sweeps the frame diagonally, covers, uncovers new
   content: the one full-saturation frame in an otherwise near-white film.
4. **The type dissolve.** Characters leave **non-sequentially** ("Introducing" goes to "In rod ci"
   before nothing): random per-character, not a reverse typewriter.
5. **The parallax storm.** Fourteen real logos drifting up past the camera at four depths, sizes and
   speeds, type pinned dead centre. Used **once**, at the loudest bar (54-58s), the film's only crowd.
6. **The cursor handoff.** A rendered cursor with real easing drives the UI: travels to a cell, a
   popover opens, text streams in. It must arrive *before* the thing it triggers, by 3-5 frames, or
   the UI looks self-driving.

## The gradient is punctuation, not wallpaper

The blue mesh gradient is dominant for 11.7s of 95, in exactly four windows: 2.4 to 5.0s (the title),
9.6 to 10.7s (one wipe), 62.3 to 66.6s (the act break), 91.5 to 95.2s (the endcard). It is the only
saturated frame in the film, so it works as a full stop: title, act break, end. Put it anywhere else
and it stops meaning anything. Build it as an animated mesh (a shader gradient, mind the cost per
frame), never a static image with a scale on it: the reference's internal folds move independently,
which is what stops it reading as a gradient PNG.

## Colour: one hue and the product

Ground `#F9FAF5` falling to `#EAEAEC` in the corners, never pure white. Ink `#1A1A1B`, never pure
black. One hue, the blue silk, `#73AFCC` to white. **Every other colour in the film comes from the
product UI itself**: the avatars, the score bars, the real brand logos. That is the discipline: with
no palette beyond a ground, an ink and one blue, anything coloured on screen is automatically the
product, `storytelling.md`'s value before hue at its strictest.

## Type

One weight, sentence case, one line, centred, roughly 4% of frame height. No tracking tricks, no
uppercase, no second size on screen at once, no two-line claims. This contradicts the type rule in
[craft.md](craft.md) (labels only, uppercase, tracked out, never a sentence), which protects a clip
cut against a talking head, where prose competes with a voice. **Here the type is the voice.**
Correct for this register, wrong for the other four.

## The music

**One bed, no stems, no drop, no silence.** Loudness sits −20 to −13 dBFS through the first half and
−13 to −10 through the second; it builds and never breaks, because a drop demands a cut. **Two
lifts, both earned**: 54-58s under the logo storm, 81-94s under the payoff line and endcard. **No
sound effects at all**: an SFX per element across a 95-second continuous move becomes a rattle.
[sound.md](sound.md) governs clips cut into a read; a product film mutes that whole file. The
picture is cut to the track, never the reverse. Choose it before the first frame is built and never
change it after `beats.ts` exists.

## What changes from the rest of the skill

The clock is the track's bar grid, not the SRT. Rung 1 is the film (the real screen **is** the
argument), not rung 2. Type is sentence case, one line, set to be read. Sound is one continuous bed,
no SFX. Cuts are zero. The deliverable is one film whose direction is picked at the gate, not three
interchangeable designs per beat. Unchanged, and non-negotiable: the direction gate in
[storytelling.md](storytelling.md) runs first, real logos and real screens beat abstractions, one
motion language from one shared motion file, every decision carries its WHY.

## The build order

0. **Direction gate**: two or three looks, one still each of the same beat.
1. **Choose the track. Measure its bar**: `python3 scripts/teardown.py tempo <track>`; everything
   downstream is a multiple of that number.
2. **Write the claim lines first, all of them, as a flat list.** Nine to twelve, sentence case. If the
   list does not read as an argument in a text file, no motion will rescue it. Mark the one
   highlighted word per line.
3. **Pair each claim with its proof** (screen, interaction, bars): the storyboard on one page.
4. **Lay the canvas out in space before animating**, so the camera travels between screens uncut.
5. Build the camera path, then the screens, then the type last (pinned to the frame, not the canvas).
6. Render stills at every claim's hold frame and every proof's resolve, and look at all of them.
7. Watch the whole file once at speed with sound on: the only check that catches a bar that drags
   or a move that reads as a cut.

## The three ways this genre fails

**It becomes a slideshow.** Caught by the cut count: `scripts/teardown.py cuts <file>` should read
zero. **The type outruns the product.** Six claims in a row because the lines were fun to write and
the screens were work to build. Caught by the ratio: product time runs about half again the type
time. **The bars drift.** One card at 1.4s, the next at 2.6s, timed by eye. Caught by
`scripts/teardown.py cards <file>` on your own render: the cycle column should be flat.

## A worked build: 39 seconds, zero cuts

The method run end to end on a screen-recorder app: 39.2 seconds at 30fps, no voice, no cuts, no
sound effects, one music bed, 8 claims and 4 live screens.

**The clock is the bar.** The bed measured 124.02 BPM with `teardown.py tempo`, so one bar is
1.935s, or 58.06 frames. Claims and proofs are both whole multiples of it, rounded once per bar
with `Math.round(n * BAR)`. Round per beat instead and a fractional bar summed 30 times drifts a
frame a bar. The first guess borrowed a reference film's 54-frame bar, and the cards sat short of
the music until the bed got measured. The 3 opening lines hold 0.75 of a bar each (2 or 3 words read
in 1.4s), later claims one bar, proofs 2 to 3. The dullest proof, a chat, plays at 1.5x.

Claims and proofs share one canvas, the screens 3000 world pixels apart. While a claim is up the
camera is between 2 stations and neither phone is in frame, so the claim gets a blank frame without
a cut. The camera leaves 22 frames before each claim lands.

**The proofs are live code.** The first cut faded between PNGs in device mockups, so nothing on
screen ever did what the type said. The proofs port the product's own screens: the AI writes a
script, the teleprompter follows a voice, the review strikes retakes and ums, the cut plays inside a
social app. People believe a claim when the next 5 seconds show it happening.

**One camera, critically damped.** Each leg sets a target and a rate, the spring's natural
frequency in 1/frames: 1/12 to travel between stations, 1/40 to push in while a screen works, 1/80
to drift under a claim. The follower keeps position and speed smooth through each change of target,
so a leg the bar grid cuts short never jumps. It never quite arrives, which keeps the frame from
going dead. Scale follows in log space so a push from 0.93 to 2.0 feels even the whole way, and 2
slow sines of a few pixels keep a hold alive.

```ts
// per frame, 4 sub-steps, for x, y and log-scale alike
v += (w * w * (target - pos) - 2 * w * v) * dt;
pos += v * dt;
```

**Fit the film to the music by cutting shots.** The first version ran 29.5 bars, and a slow bar and
a half sat between the last proof and the end card with nothing new on screen. Cutting it, and
starting the bed 8 bars in, put the bed's lift on the last proof. 8 bars is a whole phrase, so the
downbeats stay on the grid. Measure each bar's RMS with `ffmpeg astats` before you pick the start.
No sound effects at all: 14 of them across one camera move became a rattle in the first cut.
