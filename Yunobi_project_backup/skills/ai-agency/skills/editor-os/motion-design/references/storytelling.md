# Storytelling, and the direction gate

The value test in SKILL.md judges one clip at a time, so the best it can do is throw out the bad
ones; it cannot produce a story, because nothing in it looks at the clip before. This file is the
other half: the direction gate that runs before any clip exists, what a beat draws instead of the
words, and what makes a set continuous. Read it at plan time and again before writing any clip's
header.

This file is the motion application of general storytelling principles (one subject, change as the
unit of attention, an open loop). Where a general principle and this file disagree, the general one
is right about the principle and this file about the register.

## The direction gate comes before `plan.md`

**Nothing is built until the owner has picked a look.** A twenty-clip operations set was designed,
built, rendered, verified and imported before the author saw a frame. Verdict, 2026-08-25:

> "I don't like at all any of the designs we have created sadly. They are all ugly and too complex.
> We need to go a little bit more minimal. It looks amateur if you watch what you do. The skill
> should offer me one or two angles or three angles in the beginning in an HTML."

So step zero, before the beats are even measured:

1. Pick **two or three visual directions** for the video, not three designs of one beat. They have
   to actually disagree: different amount of ink, different subject, different relationship to the
   ground.
2. Render **one still per direction, of the same beat**, so they are comparable. `remotion still` on
   a throwaway composition, or hand-write the SVG.
3. Write them into a **plain `.html` file on disk** and give the owner the path. Not an Artifact - a local
   file is enough and does not put the work on claude.ai. Each direction gets its name, its still,
   one sentence on what it commits to and one on what it gives up.
4. **Stop and ask.** One of the few places a question beats a decision, because the whole session's
   output hangs off the answer.

`scripts/directions.py` writes the page from a small JSON manifest so the gate costs a minute, not
an afternoon. Its `now` panel carries a frame of the current set at a third the width of the
options, because the choice reads as academic without the thing being replaced beside it.

**A board of three designs for ONE BEAT does not satisfy the gate.** A later video ran that board, and every clip in the video was then built in a look nobody had been shown: near-black,
a blue grid measuring nothing, a bloom on each of four objects. The verdict was
"extremely ugly" and "the way we work right now has been beginner" - the same verdict as the
earlier set, sixteen days later, through the gate written to prevent it. The gate is about the
GROUND, the amount of ink and the material. Which of three arrangements a single beat uses is a
different question, asked after.

## What "too complex" measured as

That board carried, in one frame: five lane plates, five client discs, twenty-five work
blocks, five valves, five wires, a gate, a spine, a ceiling of nine segments, five people and up to
three labels. Fifty-odd marks, nearly all outlined in a bright colour on near-black, nearly all
carrying a glow. That is a control panel, the sci-fi HUD default a good eye rejects on sight.

Four rules, and they are countable rather than tasteful:

**One subject, and you can point at it.** Cover everything except the thing the beat is about; if
the rest of the frame is still doing work, cut it.

**Seven marks, not fifty.** Count distinct marks in a still. A repeated element - a row of identical
blocks, five lanes - counts as one. Past about seven the eye stops reading and starts scanning.

**Glow is for one thing.** The subject glows; the room does not. Across a passage it is scarcer
still: one glow in nineteen seconds, held back for the beat the passage was built to reach. A glow
in every beat is a glow in none of them.

**Value before hue.** The eye reads value first. Most of the frame sits at one dim value with the
subject brighter, not five colours competing at the same brightness.

What to do instead: draw fewer things bigger (three blocks at 200px say what twenty-five at 118px
tried); let the ground carry the frame; imply a structure (two rules and a gap say "rows"); cut the
label before the shape; if a beat needs fifty marks, put his face there instead and say so in the
plan.

**This ranks above the value test and the through-line.** A clip that carries the idea, changes
state, inherits its world and is unreadable at a glance has failed at the first thing a viewer does,
which is look at it.

## The two failures, one root

**The clip says the sentence.** He says "three gates" and three boxes appear labelled Gate 1, Gate
2, Gate 3 - a transcript in the brand typeface, describing the read word for word instead of the
idea. **The clips do not know about each other.** Each opens on an empty frame, builds its own small
world, resolves, and is thrown away. Fifteen of those is a slideshow of correct diagrams. Both come
from the same place: the unit of work was the sentence. **The unit of work is the video.**

## Transcription is not neutral, it costs retention

Measured, not taste. Mayer's redundancy principle: when narration and on-screen words carry the same
content, comprehension goes **down**, because reading and listening compete for one channel and
reading wins. A clip that repeats the read takes the beat, spends the budget, and lowers the
retention of the line it was meant to help. His face was the better shot and it was free. Partial
redundancy (keywords beside speech) tests better than the sentence set in type, which is why the
overlay register stays to short labels and never a paragraph.

**Type leads only for a list or a name.** An idea gets a picture.

## The literalness ladder

Every beat sits on one of five rungs. Most drift lands on 0 and 1.

| Rung | What the frame does | Verdict |
| --- | --- | --- |
| **0. Transcription** | His words, set in type | Banned |
| **1. Illustration** | Draws the noun he said (he says database, a cylinder appears) | Only for recognition |
| **2. Structure** | Draws the arrangement speech had to say serially | The floor for a real clip |
| **3. Consequence** | Draws what the sentence left implicit: the cost, the second-order effect | Where the good clips are |
| **4. Meaning carried** | Uses the video's own motif, so the beat lands and the argument advances at once | Decided in the plan, never per clip |

Rung 1 is legal only when the noun is a **recognition**: the real logo, screen or word is the whole
payload. A drawn cylinder is a picture of a word, and legal is not the same as right: a real
docs-app screenshot under "your source of truth for your templates" was genuine and still a picture of
the word *documentation*, because it named the thing a second time instead of showing what it does.

**A count is transcription with the type removed.** "Three main pillars" looks like it hands over a
layout: three columns, done. That layout is the word *three* in rectangles. A count is a property of
speech, which names a list one at a time; it is rarely the structure. Draw the topology and the
number is usually wrong: sales and delivery were the two ends of one loop, and the third thing was
underneath, holding what the loop wrote. The same trap runs on "four steps" and "two sides".

**Name the rung in the clip's header comment.** A set whose rungs are all 1 and 2 is a set of
illustrations however well it renders. Aim for a median of 2 to 3 with two or three beats at 4.

## The through-line: one world, one motif

Decided in `plan.md` before any clip exists, written at the top of it.

**One world.** The domain every figure is drawn from: the kitchen, the machine, the map, the queue.
Fixing it early is what lets beat 9 use a shape beat 3 established. A fresh domain per section
teaches nothing, because none of them compound.

**One motif.** One object that appears in the first minute, changes across the video, and returns at
the end. **It has to change, or it is a watermark.** A rack that fills, a queue that drains, a wall
that turns out to have a door. Pick one world (a kitchen: recipes, the pass, the rack, the same
burger) and extend it before opening a new one.

## Change is the unit of attention

The brain is a change detector, so the per-clip question is not what the clip shows. It is **what it
changes**: what state the previous clip left, what this one makes different, what it hands to the
next. A clip whose honest answer is "nothing, it shows another thing" is a bullet point, not a beat.

**An established structure is never redrawn from zero.** Rebuilding tells the viewer the video has
no memory.

**A scale word is said with a dimension, not with more objects.** "More projects" is the same loop,
wider. A second loop beside the first is a new thing to read.

## One open loop

A video asks one question early and answers it late: a missing box, a link that goes nowhere, a
number with no explanation. Open it on the frame where he opens it in the read. Do not resolve it;
let the video continue past the incompleteness. Pay it off with the same composition, completed, at
the beat where he answers it: recognition is the payoff. Two open loops in one video is neither.

**Which device ties one clip to the next, and which spatial arrangement anchors an idea before the
detail is spoken: the five continuity devices and the three framing models are in
[beat-devices.md](beat-devices.md).**

## The arc the plan writes down

A beat gets a **story role** as well as a register. A plan whose every beat is "explain" is a
lecture and goes flat in the third minute.

- **State.** How things are now. One beat, early.
- **Break.** The change or cost that makes the rest necessary. The beat most often handed to his
  face.
- **Complication.** Why the obvious fix does not work. Skipping it makes an explainer feel
  weightless.
- **Mechanism.** How it does work. Most clips live here, where the motif and carry-over earn a
  place.
- **Payoff.** The motif returning, changed.

## When a passage will not draw, the copy is wrong

A storyboard is the first honest proofread a read gets, because speech carries an ambiguity a frame
cannot. The pillars passage said the system stands on three pillars (sales, delivery, system) and
then said all of it is maintained by a system: the container and one of its parts had the same name.
No frame can draw that. **A beat you cannot draw without inventing a distinction the read does not
make is a beat whose read is missing that distinction.** Send the sentence back before designing
round it.

## Where storytelling is the wrong answer

- **A recognition beat.** Three seconds of the real screen or logo; a metaphor buries the one thing
  it was for.
- **A screen demo.** The evidence is the story; a graphic over it argues with it.
- **A quantity.** Draw the quantity; a metaphor adds a domain to translate back out of.

Reaching for rung 4 on every beat is its own failure: a video that will not say anything plainly.
Both answers to the value test go in the clip's header comment, one line each: what the viewer knows
after this clip that the sentence did not tell them, and what it changes from the clip before and
hands to the clip after. A clip that can only answer the first is correct and inert.

