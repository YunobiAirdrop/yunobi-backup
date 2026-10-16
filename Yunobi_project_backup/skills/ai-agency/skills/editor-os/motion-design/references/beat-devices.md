# Continuity devices and spatial framing models

Two toolkits, reached for once the through-line is set: which device ties one clip to the next, and
which spatial arrangement anchors an idea before the detail is spoken. The doctrine both serve is in
[storytelling.md](storytelling.md).

## Five continuity devices, cheapest first

A video needs one of these, not five.

1. **Carry-over state.** The next clip opens where the previous resolved. Costs nothing but a shared
   constant, and it is the highest-value change available. Where a passage shares one figure, build
   it as **one clip, not one file per beat**.
2. **The return frame.** One composition that comes back at each boundary with one more thing in it.
   **The library draws it: `ReturnMark`, filled once per section with a higher `at`.**
3. **The match cut.** The last shape of one clip is the first shape of the next, meaning something
   else. Expensive to plan, free to render.
4. **Running position.** One element holds its screen position for the whole video: the client
   always enters from the left, the system always sits right. Nobody notices and everybody feels it.
5. **The 3D spatial carousel (The Canvas / Chapter Hub).** Rather than cutting between chapters,
   place the video's core mental models side-by-side on a continuous curved horizontal plane in 3D
   space. The camera tracks across the x-axis to transition between topics. The active card sits
   front and center; previous and upcoming topics stay visible in peripheral depth-of-field blur.
   Entering a topic dollys into the card, unfolding its internal topology (tree, bullseye, or
   columns) without losing the viewer's place in the mental map.

## Framing an idea: three spatial models

Speech is serial and easily forgotten. A spatial frame anchors an idea before the detail is spoken:

1. **The dichotomy fork (The Two Games).** When framing a decision ("Culturally famous vs Category
   famous"), defocus the speaker's talking head (~25px blur) and drop the two paths side-by-side.
   Branch with curved dashed connectors, zooming into the chosen path while the alternative remains
   visible in the peripheral margin.
2. **Concentric layering (The Bullseye).** For target audience, ideal client, or market scope: 5
   concentric depth rings with leader lines from the tight core out to the broad periphery. Speech
   explains serial steps; the concentric ring proves proximity to revenue instantly.
3. **Architectural metaphor with proof anchors.** When an idea has structural weight (e.g. pillars),
   render physical 3D Doric/Ionic columns in perspective. Never leave a category abstract: dock
   tangible social proof cards (real avatar with story ring, verified badge, handle, category
   subtitle) directly under each station.

## Where a graphic lands against the word

Two laws, torn down on 2026-08-29 off a nineteen-minute reference whose whole b-roll language is
drawn overlays on a talking head (a video model plus an ffmpeg frame-difference sweep). Neither is a
curve; both are offsets between the animation clock and the read.

**A graphic arrives about a third of a second BEFORE the word it serves, and completes on it.** Ten
to fifteen frames. A graphic that lands ON its word is a caption; the same graphic fifteen frames
early is an anticipation. This is why the in-point is part of a clip's spec, not the editor's
discretion.

**It leaves six to ten frames BEFORE the last syllable, not after it.** A graphic held to the end
hands the frame back on a dead beat. Pulled out just early, it throws focal weight back onto the
face for the closing words. This does not tension with `HOLD`, the floor on the tail after the
resolve, which is what moves earlier.

The measured clock those two sit inside: **a distinct visual change every 1.7 to 2.5 seconds**
across a nineteen-minute runtime, 41 in the first sixty seconds, and no static stretch over 5
seconds. The changes are not full cuts: a row lighting, a tool pill popping, a connector line
pulsing, a UI crop spotlighting an input, or a camera punch-in. About seven visible micro-changes
per hard cut.

**The three tiers of beat frequency:**

- **Micro-beats (1.5s - 2.5s cadence)**: Floating brand pills (e.g. Gmail, Calendar, Claude),
  numeric callouts (`20%`, `5 min`), camera punch-ins (1.15x push), and subtle UI spotlights that
  dim everything except the active input field.
- **Meso-beats (5s - 8s cadence)**: Connector travel (data flow across an MCP wire), the active-row
  snap below, side-by-side prompt-versus-output reveals, and step progress markers.
- **Macro-scenes (15s - 45s cadence)**: Full architecture maps (central model hub connected to five
  external apps), complete live tool workflows, or end-to-end automations.

**The primary mechanisms that fill that clock:**

- **A list shows every row from its first frame, and only one is lit.** Inactive rows sit at about
  35% with no border; the active row snaps to full white on the spoken cue. A staggered reveal is
  the wrong default for this case: a row that has not arrived cannot be anticipated. `figures.md`
  keeps the staggered form for a list whose order is the argument.
- **Nothing is ever shown finished.** Charts, fills and connectors draw across one to one and a half
  seconds behind an illuminated leading point. The mark lands *before* the fill reaches it, which
  turns a result into a fate. Give every fill a one-second floor: it is the
  same law as a minimum.
- **Split-focus during live demos.** While showing Claude Desktop or ChatGPT typing, a secondary
  pill or callout card tracks the exact MCP server being invoked in real time, preventing dead
  screen time.
