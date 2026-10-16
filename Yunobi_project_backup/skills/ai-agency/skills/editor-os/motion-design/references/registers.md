# Named registers: code walk, introduction, hand-drawn, shorts board

Four registers with their own file because each is a specific, measured recipe rather than a general
rule. Build one worked example of each before using it in a video.

## The code walk

A file at poster scale with no window round it. The camera settles on one line, the rest of the file
drops to 30%, a margin note says why, then nothing moves for three seconds. Twice, at two lines that
make one argument, then it gives the file back. Built 30 Aug 2026.

**Reach for it when** the proof of a claim is code a viewer could check - not a command and its output
(`motion-terminal`), not a diff (a beat, not a graphic).

**What was measured**, torn down off HyperFrames' `code-scroll` at 180 frames/30fps: 21 frames still
before the first move; the travel is 36 frames, 196px, symmetric ease; the dim is 14 frames starting
**2 frames before** the travel ends, to about −14% mean luminance; then 87 frames (2.9s) dead still.
The overlap between move and dim is the one number a redraw gets wrong - started after the move it
reads as two events, two frames early it reads as a consequence of arriving.

**The rules**: no window, no traffic lights, no title bar, no ground - the frame is the file. No
syntax colouring - a theme is a second accent system competing with the spotlight. The camera has one
speed, not one duration: leg length in frames scales off the measured 196px/36 frames. Two stations,
never three - three stops is a tour with no argument. Notes live in a margin, under the line they
cover. It ends on the file, not the line - the dim lifts at the exit. Silent; the person talking over
it is the sound.

## The introduction

Nothing introduces itself. A question is typed into a composer on the pale wall, the assistant thinks
for a beat, the answer that comes back is the product. Built 30 Aug 2026.

**Reach for it when** a video or product showcase has to open. It buys the product a second voice: the
same name returned as an answer to a question the viewer would ask is a claim somebody else made.

**What was measured**, off HyperFrames' `blue-sweater-intro-video`, 288 frames/24fps: the line lands at
2-12, the composer arrives 35-60, typing and send 104-132, and **the hold on the card runs 132-283,
151 frames, 6.3s** - over half the reference. A version that cuts on the click is an ad; the seconds
after are what read as an introduction.

**The rules**: the question asks for the category, never the product ("one tool to see every client
account at once", not "tell me about Acme"). The wait is drawn, not cut past - 36 frames of one
breathing dot. The field leaves before the card lands, or the beat becomes an interface demo. One
pointer, one click - the exception to the live-screen rule that a screen is never operated, because
here the cursor is the payoff. The composer is a generic skin, never a vendor's. It stands on the pale
wall (two tokens, no camera) - the one beat that is not evidence, so it can afford a room.
The clip's length is a function of the question, through `askDuration`.

## The hand-drawn register

Paper, one marker colour, geometry a machine did not make. The author's ruling off a direction board:
"I think we should go for this for all the future design more hand-drawn kind of" - the default
for a new clip; anything else now needs an argument. It takes three pieces: a seeded wobble with the
rough primitives and a one-marker rule, an ink layer (drawing on as the whole motion language, plus a
handwriting wipe), and a paper ground (the tooth, no key light, no vignette).

**Draw the analogy, not the abstraction of it.** Same day: "why don't you simply use the actual
metaphor of the lobster restaurant and stuff?" The redundancy rule bars drawing the WORDS; it never
held against drawing the WORLD, and in a marker drawing the analogy is the idiom, not a decoration.
Logos stay real marks on a rough tile, never drawn by hand - recognition is the one thing a drawing
cannot fake.

**Four things that make it this register**: the wobble is the point (a perfect bezier on paper is a
vector drawing with a beige background, and it has to be seeded so it does not boil across frames);
everything draws on (a frame that fades up was composited, and the viewer reads that in 200ms); no key
light, no vignette, no glow (a drawing has a page, not a lit room); one marker colour per video,
default the brand accent or the product's own mark when the whole video is about one product.

**The failure that cost three passes**: a lobster drawn top-down is a beetle at 45 degrees and a
rabbit at 20, because the claw, tail and antennae all point at the camera or lie flat. Draw a creature
in the angle it is already drawn everywhere else, so the viewer's existing silhouette does the
recognition for free.

## The paper board

The vertical register. A Short where the whole frame is a composited page: a pale gridded ground, the
speaker demoted to a card at the foot, one real screenshot as the subject, one karaoke word between
them. Measured off a 62.5s Instagram Reel, 1080x1920, 24fps; the source lives in `sources.json`, not
here. It is the opposite of the dark-ground registers - the face sits **inside** the graphic, on a
**light** ground, with text on every frame.

**The frame, top to bottom, fixed for the whole 62 seconds**: a two-line headline in black with the
load-bearing half in accent red; the artefact, centred, about half the height, always a real
screenshot; one karaoke word, centred, bold, black on paper or on a black pill over video; the speaker
in a rounded card, about 35% of frame width, bottom centre, never moving.

**What was measured**: 18 hard cuts across 62.5s, median gap 3.46s, alternating only between the
**board** (all four bands) and **full-bleed face**. The karaoke changes about every 0.35-0.40s, one
word at a time, never a phrase. The headline builds in grey before resolving in black and red, arriving
with the point rather than the cut. Palette is four values: paper white, near-black type, one accent
red, and whatever the real screenshot brings.

**The devices**: the artefact is always the real thing, no abstraction anywhere in the register; a
grid of six real thumbnails assembles and a cursor picks one; document panels land and hand-drawn
arrows label them one at a time; logos lock up one at a time as named; the face card is a constant
size and position, so the eye stops tracking it after the second cut.

**Building one needs four things a dark-ground kit does not have**: a light ground; a face plate built against real raw footage rather than standing alone; a karaoke
track, one word per SRT cue with a highlight; screenshots as first-class assets, usually somebody
else's screen, which puts the licence in a sources ledger. **None of it is drawn** - the work is
capture, layout and cadence, not illustration.
