# The HyperFrames lane

Both open Chrome, draw every frame and encode. Remotion takes a React component; HyperFrames takes
an HTML file with `data-start`/`data-duration` attributes and a **paused** GSAP timeline on
`window.__timelines`. Apache-2.0, from HeyGen, renders locally, no build step.

An addition, not a replacement. If you already have a Remotion project with its tokens, frames and
alpha ProRes route, **never port it**: a machine
translation gets about 80% of a composition across, and the missing 20% is where the taste lives,
so a port costs more than it returns even when it runs.

## Patterns: reach for HyperFrames when

| The job | Why it wins |
| --- | --- |
| The source is already a web page, an HTML prototype, an exported design, a GSAP or Lottie file | It seeks the animation it is handed. Remotion needs a rewrite |
| Captions or graphic cards on footage that already exists | `embedded-captions` and `talking-head-recut` run it end to end, locally, off the transcript |
| One throwaway clip nothing will reuse | One file, no project, no build step, no entry in a composition registry |
| A deliverable a client runs on their own machine | Apache-2.0, no seat count. Remotion is free only up to three people |
| Twenty variants of one card | `--batch rows.json` writes one output per row, and `compare v1/ v2/` diffs them |
| A website, a Figma frame or a GitHub PR is the input | `capture`, `figma` and `pr-to-video` are built in |

## Anti-patterns: keep it in Remotion when

| The job | Why it loses |
| --- | --- |
| The clip reuses a token, a scene or a component from your Remotion project | Typed and colour-correct, and none of it crosses |
| It has to be cut next to an existing Remotion clip | The font and the spring both have to be re-fitted by hand. Budget an hour, not ten minutes |
| The beat is a figure in the house language | That vocabulary is this skill's and it is written in Remotion |
| The video already has a plan and a built set | Consistency inside one video beats a better renderer for one clip |
| The motion is meant to come from class-toggled CSS transitions | They do not seek: see [measured-behavior.md](measured-behavior.md) |
| A composition input has to be typed and validated | Remotion gives that for free; here it is `data-composition-variables` and `--strict-variables` |

## Install on demand, never vendor

The catalogue is 20 skills and about 1100 files. Vendoring it into `ai-doc/` would double the skill
library for one renderer. It installs itself instead:

```bash
npx hyperframes skills check              # read-only: what is installed and stale
npx hyperframes skills update             # the core set, 9 skills, ~6.7 MB
npx hyperframes skills update pr-to-video # one workflow, on demand
```

The installer writes two copies, one per harness root, so
**the files live once in `~/.agents/skills/`, and every `~/.claude/skills/hyperframes*` is a
symlink to it**; a skills browser lists it once, not twice. `skills update` recreates the second
copy, so re-link after. `npx skills add heygen-com/hyperframes --skill <name>` is the same, via
the upstream installer.

Install it globally rather than inside a project, so one copy serves every project and a project sync
never touches it. Remove it the way it arrived: delete the `hyperframes*` and `media-use` folders from
`~/.claude/skills/` and `~/.agents/skills/`.

Ask `/hyperframes` for a video and its router picks the workflow: product launch, faceless
explainer, PR-to-video, captions, recut, music-driven, motion graphic, slideshow, Figma import. It
installs only the workflow it picks, so the full catalogue never sits on disk.

## Dressing an existing recording

Two skills cover the job Descript does by hand:

- **`embedded-captions`**: 35 caption identities, local Whisper, subject matting so a word sits
  *behind* his head, not over it. Footage delivered untouched; split multi-shot footage first.
- **`talking-head-recut`**: timed graphic cards on a clip that plays in full, lower-thirds, data
  callouts, quotes, side panels, picture-in-picture, synced to the transcript.

Plain subtitles are the first one. Designed cards are the second. Cutting the read itself is a
video-editing job, not this one.

## Generating options

This is where it beats the Remotion project outright. One composition, a JSON array of rows, one
output per row:

```bash
npx hyperframes render --variables '{"title":"Hours back"}' -o a.mp4
npx hyperframes render --batch rows.json --json     # one render per row
npx hyperframes compare v1/ v2/                     # frame-by-frame diff
npx hyperframes snapshot --at 0,2,5                 # stills, no encode
```

Read the values inside the composition with `window.__hyperframes.getVariables()`, declare them in
`data-composition-variables`, and add `--strict-variables` so a typo fails the render instead of
silently rendering the default. Use `snapshot` to judge a variant; a render is not needed to look
at a frame.

## What's measured

Render times on this machine, which of four ways to write a move actually seeks under
HyperFrames' capture, and what breaks porting a Remotion clip to match one already built:
[measured-behavior.md](measured-behavior.md).

## Boundaries

- The HTML authoring contract itself: `/hyperframes-core`, installed with the core set.
- A hosted video model instead of a rendered one: that is a prompting job, not a render job.
