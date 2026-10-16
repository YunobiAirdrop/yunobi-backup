# Measured behavior

## Measured on this machine, 26 Aug 2026, v0.8.15

- A 10-second 1080x1920 project rendered in **12.1 s** to 2.3 MB, six workers, no build step. The
  first `npx` call adds about 8 s.
- `--format mov` writes **ProRes 4444, `yuva444p12le`**, which is the alpha format the Remotion
  route already produces. The qtrle conversion for Descript is unchanged. `--format webm` and
  `--format png-sequence` also carry alpha.
- `init` refuses to run non-interactively without an example: pass
  `--example blank --resolution portrait --non-interactive`.
- Rendering one `<template>` sub-composition with `-c` cost **1 m 37 s for three seconds** and
  printed `sub_timeline_readiness_timeout`. Render the project, not the fragment.
- Telemetry is on by default and was disabled here with `npx hyperframes telemetry disable`.
- A scaffolded project pins its own CLI version. `npx hyperframes@latest upgrade --project . --check`
  reports the pin; nothing advances on its own.

## What actually seeks, measured

Rendered a 2-second composition with the same 1200px move written four ways, then read the box
position out of the frames:

| Written as | Seeks |
| --- | --- |
| CSS `@keyframes`, no JavaScript at all | **Yes.** Frame-accurate, identical to GSAP |
| Web Animations API, created and never played | **Yes.** Frame-accurate |
| GSAP on the registered timeline | **Yes.** The documented path |
| A CSS `transition` fired by a class the timeline toggles | **No.** It jumped back to its start mid-render and finished late: frames are captured out of order across six workers and a transition restarts in each one |

**This decides how a UI-motion snippet library is reused.** If its snippets are class-toggled transitions,
the one row that fails. What ports: the durations, cubic-beziers, blur and distance scales, the
open/close asymmetry. What does not: the trigger. Re-express the snippet as
`@keyframes` with an `animation-delay`, or drive the same properties from the GSAP timeline.

None of it pastes into Remotion either: it has no CSS animation to advance, so every snippet has to be
re-authored as `interpolate` and `spring`.

The two stay separate on purpose: a motion file is physics, four springs (ENTER,
ARRIVE, SETTLE, DEPART) giving every clip the same weight; a UI-motion library is durations and beziers,
for opening, closing or swapping. A product-interface clip wants the second;
a clip drawing a figure wants the first. Mixing them is how a set stops looking like one hand.

## Porting a clip that has to match one already built

Measured on an alpha caption overlay rebuilt in HyperFrames from its Remotion original.

- **Ship the face with the project, don't name it.** HyperFrames' Chrome has no installed SF Pro,
  so `-apple-system` fell through to Helvetica: every row came out 5% wide (511px vs 487).
  Reordering the stack changed nothing. Copy `/System/Library/Fonts/SFNS.ttf` into the project,
  load it via `@font-face` with `font-weight: 100 900` (the variable system face), and the row
  lands at 482. Do this first on any clip that sits beside a Remotion one.
- **A Remotion spring has no GSAP equivalent: two answers.** For an arrival that appears and
  stops, fit an ease by eye: `back.out(1.6)` over 0.4s tracks a damping-13/stiffness-190 spring
  closely enough. For anything cut next to the original, sample the rendered clip frame by frame
  and replay the numbers as one keyframe per frame at `ease: "none"`, which took error from nine
  points mid-run to **2px of 620 in every frame**.
- **A full-frame gradient over alpha breaks ProRes compression.** The clip's key light took the
  intermediate from 19 MB to 475 MB; the qtrle deliverable Descript takes is unaffected at 36 MB.
  Render `--format mov`, convert, and keep the intermediate out of git.
