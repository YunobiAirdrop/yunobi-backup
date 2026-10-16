---
name: motion-design
description: "Makes video clips and product films: motion graphics, captions, figures, 3D, CTAs. Use when a video needs a clip that is not the presenter's face, a product needs a film with no voice-over, or on a Remotion or HyperFrames question."
tags: [makes, video, remotion]
lane: visual
---

# Motion design

The clips live in a Remotion project at 30fps in two frames: **1080x1920** for anything cut into a
Short, and **1920x1080** for lessons and long-form YouTube. Keep each frame's size and safe band in
its own constants file, so a portrait clip can never pick up the landscape numbers. A landscape clip
is not a portrait clip rotated: see the frame note in `figures.md`.

**Four of the five registers are built here. The fifth is found.** A meme, a film beat, a piece of
archive is a shot somebody else already made, and a borrowed frame cannot ship where a drawn one can
without a licence check. Keep those clips in their own folder, apart from the ones you draw. The
split is authorship: this skill decides what a beat should show and draws it. The value test, the
literalness ladder and the planning rules below govern both.

It is not a general video skill. Neighbouring jobs: getting clips into the editor, named, filed and
placed at a phrase (`video-edit`); writing the read (`video-script`); a generated still, an animated
clip from it, a found shot, or a hosted-model prompt. Picking Remotion over HyperFrames, the evergreen YouTube CTA kit and the Remotion API itself
are this skill's own branches, below. The vendored Remotion references had every design instruction
stripped out: they are the engine and hold no taste, so one that appears to contradict this file
describes a default, not a decision. This skill is about whether the clip says the thing, and
whether the set says one thing.

## A film with no read is a different job

**This is the headline branch.** A product film in one take, 30 to 60 seconds, no cuts, no voice.
Everything below assumes a read: the clock comes from the transcript, the clip serves a sentence,
and a graphic must not repeat what is being said. **A product film has no read** (no voice-over, no
face, no transcript), so the type is the only voice and the clock comes from the music. Asked for
one with the playbook below, a session builds fifteen beautiful independent scenes and cuts them
together; the reference films have **zero cuts in 95 seconds**. The playbook, and
`scripts/teardown.py all <reference.mp4>` which measures any film's cuts, bar, card cadence and
palette, is in **[references/product-film.md](references/product-film.md)**. It replaces this file's
clock, type and sound rules; the direction gate, real-things-over-abstractions and one motion
language still hold.

## Nothing is built until the look is picked

**Step zero, before the beats are measured and before `plan.md` exists.** Two or three visual
directions for the whole video, one still each of the same beat, in a plain `.html` file on disk
(`scripts/directions.py`), and then you stop and ask the person who owns the video. The gate, the
verdict that forced it, and its four countable rules (one subject, seven marks, glow on one thing,
value before hue) are in **[references/storytelling.md](references/storytelling.md)**. Read it
before the first still: it outranks everything below, since a clip can carry the idea and still
fail at the first thing a viewer does, which is look at it.

## The two failures this skill exists to prevent

**One: a clip that is beautiful, on-palette, correctly timed, and conveys nothing.** Abstraction is
easy to justify and impossible to read: "AI Skill System" shipped eight neutral geometric marks for
eight tools, and nobody recognised their own stack in a hexagon. Recognition was the whole job.
**Draw the actual thing.** Real logos, real words, the real screen. Abstract only when the real
thing does not exist yet, and write down what you gave up. Logos come from simple-icons where the
brand is still in it, else a logo API by domain, never an image search.

**Two: fifteen individually correct clips that are not a video.** Each opens on an empty frame,
draws its own small world, resolves, and is thrown away, so the set plays as a slideshow of
diagrams. The first failure is caught one clip at a time; the second is a property of the set.
**[storytelling.md](references/storytelling.md)** is the whole answer, with Mayer's redundancy
principle behind it: read it before planning a video and before writing any clip's header comment.

## The test every clip has to pass: what does it add

Before building anything, answer in one line: what does the viewer know after this clip that the
sentence did not tell them? The four things a graphic can add, the second question every clip also
answers, and why a right clip on the wrong sentence is a wrong clip:
[references/value-test.md](references/value-test.md). Both answers go in the header comment. The
five registers, the cut's real clock, planning a whole video, one-beat-three-designs and the
timing: [references/planning.md](references/planning.md).

## One motion language, or the set has no continuity

Continuity between clips is shared **physics**, not a shared palette: the eye reads acceleration
before colour, so three clips that each picked their own spring inline are visibly by three hands
however well they match on hue. `motion.ts` is the one home for the vocabulary (`ENTER`, `ARRIVE`,
`SETTLE`, `DEPART`, `TRAVEL`, `ANTICIPATE`, `HOLD`). Journeys interpolate, arrivals spring, and
inlining a curve starts the drift again. Both ends of a clip are designed, never only the entry; the
full vocabulary and the physics a long take runs on are in [craft.md](references/craft.md).
Continuity of *meaning* is the sibling rule, in [storytelling.md](references/storytelling.md).

## Picking Remotion over HyperFrames

Both open Chrome, draw every frame and encode. Remotion takes a React component; HyperFrames
(HeyGen's HTML renderer, Apache-2.0, installs on demand, never vendored) takes an HTML file with a
paused GSAP timeline. Reach for HyperFrames on a source already a web page or GSAP/Lottie file, a
one-off nothing will reuse, or a client-run deliverable; stay in Remotion for anything reusing a
token, scene or component from your own project. Tables and install: [hyperframes-lane.md](references/hyperframes-lane.md).


## The evergreen YouTube CTA kit

A CTA, lower third or end card is a different job from a beat clip: no read and no clock, reused
for years so it earns hand-tuning, and it carries an alpha channel that fails only in the render.
House rules and the alpha checklist: [youtube-ctas.md](references/youtube-ctas.md).

## The craft is next door

The storytelling, planning, product-film, value-test, hyperframes-lane and youtube-ctas references are linked above. The rest:

| Reference | Covers |
|---|---|
| [beat-devices.md](references/beat-devices.md) | Continuity devices, spatial framing models, graphic-to-word timing |
| [craft.md](references/craft.md) | Finishing passes, motion vocabulary, frames and safe bands, grounds and `alpha`, type as labels |
| [figures.md](references/figures.md) | Diagrams, listicle architectures, analogies, overlays, rendered-object register |
| [registers.md](references/registers.md) | Code walk, introduction, hand-drawn house register, paper board |
| [long-take.md](references/long-take.md) | The camera-travels register, and the live screen |
| [sound.md](references/sound.md) | The sfx kit and its six rules, the watch-fix render loop |
| [sound-layout.md](references/sound-layout.md) | Where sounds go in a video, how loud and how often |
| [alpha.md](references/alpha.md) | Transparent overlays and where the alpha silently dies |
| [surface.md](references/surface.md) | The glass surface, seven layers, built to survive an alpha channel |
| [remotion.md](references/remotion.md) | The vendored Remotion API reference router |


## Before designing anything, check what you already built

Most beats repeat. Keep a roster of the clips you have built, each with the line it served, and
search it before you design a new one. A beat that matches is a fill, not a design job.

**A beat that is only text is always alpha**, keyed over the presenter's camera, never a full-frame
card. Full frame is for drawings, charts, real screens and 3D. The keyed-text rules are in
[references/alpha.md](references/alpha.md).
## Execution flow

0. **Build the direction board and wait for a pick.** Two or three looks, one still each of the same
   beat, `scripts/directions.py`, hand over the path. Nothing below starts until the owner answers.
   Storyboard first when the argument is in doubt: `scripts/storyboard.py` draws every beat as
   three keyframes in minutes (draw order is z-order, connectors before the things they connect).
1. Get the raw take and its transcript (an SRT). Check the video's real duration against the
   raw. Write down each beat's start, end and sentence.
2. **Write `plan.md`** per [planning.md](references/planning.md), before any clip exists. It opens
   with the through-line (one world, one motif that changes, the open loop) and carries a story role
   and a register on every beat, per [storytelling.md](references/storytelling.md).
3. Write or update `beats.ts` from those measurements, for the beats built this session.
4. Build three designs per beat. Real logos, real words. Every clip opens with the line it serves,
   its timecode, both answers and its rung on the ladder, plus a `WHY` paragraph per real design
   decision. A structure an earlier beat built is inherited, never redrawn. One subagent per beat
   can draw them in parallel.
5. Cut the sound in the same pass, from the same frame constants.
6. Render a still per phase per clip and look at every one: a clip is not done because it
   typechecked, and silent invisibility survives a clean render and exit code. Fix what is
   invisible, cut off, or unreadable, then typecheck and render the mp4s and the MOVs for anything
   meant to key.
7. Watch every rendered file with `scripts/watch.py`, one review subagent per clip. Fix the list,
   re-render, watch again until a pass returns nothing. Checklist: [sound.md](references/sound.md).
8. Hand the clips to your editor, named `N [mm-ss] Description.mp4` with a letter suffix for
   alternatives on one beat (`2a`, `2b`). Importing a clip is not placing it: put each one on the
   timeline at its phrase and check it sits there.
9. If this run surfaced a failure mode, write it down with today's date and read it before the next.

