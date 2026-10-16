---
name: descript-script-edit
description: "Cuts a Descript composition's script - false starts, retakes, filler and digressions - then plans and places the shots on it: the jump-cut rhythm, the layout each beat calls for, and the b-roll, through the rich clipboard the user pastes back. Use when a raw take is full of restarts, when an edit is cut but has no b-roll or reads flat, when a video needs its sequence cuts and layouts decided, when Descript AI credits are exhausted, or when prompt_project_agent is unavailable."
tags: [makes, descript, video]
---

# Descript Script Edit

This skill covers cutting the **script** of an existing composition. Getting media into the project, named and foldered, is `descript-projects`. Encoding and scheduling is `shorts-production`.

## The CLI cuts now, and it is the first thing to reach for

Since 1 Sep 2026 the cut is a command, spending no AI credits, needing no clipboard and no browser:

```bash
cd <the CLI directory>
pnpm descript script <project> <comp>                 # the script, with cuts, speeds, cards, markers
pnpm descript cut <project> <comp> --from "<words>" [--to "<words>"] --dry
pnpm descript restore <project> <comp> "<cut words>"
pnpm descript speed <project> <comp> 1.1 --from "<words>"
pnpm descript verify <project>                        # open it and prove it still draws
```

It writes the app's own edit: the paragraph SPLITS and the removed half carries `isBlocked: true`,
struck through and reversible, snapped to word boundaries off the transcript's alignment rather than
interpolated. `--dry` prints the seconds and the words before anything is written.

**Run `verify` after every write**, and never write while the user has the project open in a tab.

The whole editing surface is there too - layouts, layers, effects, transitions, markers, elements,
text, highlights, ducking - documented in `vibe-kit/CLIs/descript/README.md`. The clipboard path
below stays for the case where the CLI has no verb for what is wanted, and `prompt_project_agent`
for a whole-pass rewrite.

## The order: credits, then the clipboard, then the browser

`prompt_project_agent` does this job properly, server-side, in one call. Use it whenever it works:

`mcp__claude_ai_Descript__prompt_project_agent`, with the project and composition ids and a prompt
such as "delete every abandoned attempt, keep the last clean version". It is metered on Descript AI
credits and fails clean when they are gone, project untouched. **It always gets 2 things wrong, so put
both in the first prompt**: it leaves the silence where it cuts the words, and it cuts the head
off a kept sentence while reporting that sentence as kept, so read the transcript back. **A top-up
is the user's call, never yours** - give them the `upgrade_url` and stop. Only when they decline
does the clipboard path apply, and the browser only after that. It is also the only API write path,
so do not go looking for a cheaper one: [`references/agent-path.md`](references/agent-path.md).

**The clipboard beats the browser, and it is the one to reach for.** It carries the **edit**, not
the text, so one paste replaces 40 guarded drags, spends no AI credits and runs in whichever
Descript the user is already signed into. Cuts ship as **Ignore** (`isBlocked: true`): struck
through, reversible, text byte-identical, the pauses kept. Verified 2026-08-20 on 3 videos, the
largest 1036.95s -> 270.15s in one paste.

## The coaching pass runs first

`video-coach` reads the raw take against the script it was recorded from and returns one habit to
change on the next recording. It has to run **before** this skill, because the evidence it needs -
the restarts, the abandoned openings, the blocks talked out of existence - is exactly what a cut
removes, and every recording-habit number then reads as a floor rather than a measurement.

## Cut it through the clipboard

The fallback path, for when the CLI has no verb for what is wanted:
[references/clipboard-cut.md](references/clipboard-cut.md).

## Place the b-roll and the layout from the script

`scripts/pins.py` puts clips, overlays and zooms on the timeline through the same paste, so
one run hands the editor a script that is cut, de-filled, marked up **and shot**.

```bash
python3 scripts/pins.py catalogue          # media it can place, layouts it can clone
python3 scripts/pins.py resolve pins.json  # dry run: where each clip lands. Writes nothing.
python3 $D apply cuts.json --pins pins.json    # cut and place in one paste
python3 $D pins pins.json                      # place only: no cut, no alignment needed
```

**A pin is three coupled objects, so an insert is a state change, not an object drop**: a card at
the in-point carrying the layer and a second at the out-point that does not, and a missed closing
card runs the clip to the end of the video. **Run `catalogue` before placing a single zoom** and
read its layout line as a gate, because a zoom clones the prevailing stack and where no card carries
a pin layer every zoom lands as an empty card, which shipped fourteen blank frames into a finished
cut on 2026-08-31. In that state `pnpm descript layout pace` is both the placement and the repair.
The `pins.json` shape, the object model, the z-order and geometry rules and every refusal:
[`references/pins.md`](references/pins.md), read before writing one by hand.

## Where the shots go: the rhythm decides, not the eye

`pins.py` places a clip and the pack stamps a look; neither one decides **when**. `sequence.py`
does, off the payload `grab` already wrote or off `pnpm descript doc`, so a cut script comes back
as a shot list rather than as a file somebody still has to watch through.

```bash
python3 scripts/sequence.py audit ~/.descript-clip/current.json   # the grab payload, or a doc.json
python3 scripts/sequence.py plan  ~/.descript-clip/current.json --out pins.json
```

`audit` exits 1 and names the timecodes when the edit misses any of three: a state change every 7s
median, 20-50% of runtime under a full-frame overlay, and no stretch over 12s where nothing changes.
`plan` reads six triggers off the surviving script and comes out as pins with the zoom ladder filled
in, the jump cuts beside them, and every unbound slot printed as `OPEN`. The measurements behind the
three, and what to read before writing a `pins.json` by hand or when an edit reads flat:
[`references/sequencing.md`](references/sequencing.md).
[`references/layout-pack.md`](references/layout-pack.md) is for when the look a beat needs is one
this video has never used, because `pins.py` can only clone a look already in it.

## An OPEN slot is a brief to dispatch, never a line in the summary

`plan` returns the trigger and the sentence, which is a written brief. Hand each one to the agent
that owns that lane, in the same turn, rather than reporting the hole:

| the slot says | dispatch |
|---|---|
| `motion` on a count, a list or an argument with steps | `motion-design` - Remotion, local, no marginal cost |
| `screen` where the recording exists | place it here; no agent needed |
| a beat that wants a photograph or a material | `broll` for the still, then the two motion lanes below |
| a film beat, a meme, a shot that already exists | `broll-research` |

**A still becomes a clip two ways and both are cheap enough to ship side by side**, so the choice
is made by looking: `pnpm broll:loop <image>` is DepthFlow parallax, local and free, and a hosted
image-to-video model redraws every frame for a beat that needs material physics. Generate the
comparison at 480p: [`references/sequencing.md`](references/sequencing.md).

## Lint the document before every commit. This is a gate, not a check.

```bash
python3 scripts/lint_document.py doc.json     # exits 1 and names every dangling reference
```

**One dangling id makes the whole project unopenable.** Descript refuses the entire document and
the editor shows *"Oh no! Something's not working"* with no route back in, so the repair cannot be
done from the app either. Three invariants, any one of which refuses the whole document: every
`*Id` resolves to an object that exists; every pin a card layer draws is **registered** in that
composition's `timeline.pins.components`; and both the cards track and the pins track are in
**script order**. **A count is not a validation** - cards, markers, pin scenes and words all matched
the known-good state on the document that would not load.

The gate is wired into `commit()` in `CLIs/descript/client.ts`, so an invalid document cannot leave
the machine whoever is driving, and the browser console's `DocumentInvalidError` names the exact
JSON path of every fault. The EC49 lockout it was built from, and what the first linter missed:
[`references/document-lint.md`](references/document-lint.md).

## The order of operations, and it is not negotiable

Two write paths reach one composition and they do not compose. **The clipboard replaces the script
region from a payload built off an older grab; `pnpm descript layout` writes server-side.** So:
cut, markers and pins go in first, as pastes, and every `layout` command runs after. Reversed, the
paste silently discards every stamp.

And the clipboard is not durable: a clipboard-history tool or the next terminal selection
overwrites a built payload between announcing it and pasting it. Check
`osascript -e 'clipboard info'` for the multi-megabyte `HTML` flavour before assuming a copy
happened, and repair with `dscript restore <id>`.

## Reordering: keep the best take, not the last one

`scripts/arrange.py` takes an **order**, token spans that must tile the whole script exactly once,
and emits the TAUs in it, so a take recorded twice keeps its best pieces in the right places. Cuts
still ship as Ignore and a moved span carries its own ignored attempts with it. The move to look for
first is a second pain recorded after the promise. Verified 2026-08-24 on a 40-minute CRM build,
40:11 -> 29:48. The three refusals, the `--styles` cue legend and the archive it writes:
[`references/reordering.md`](references/reordering.md).

## What to cut

Two passes, and the second one is the one that gets skipped. **Pass 1** removes the wreckage of
speaking, enumerated mechanically by `scripts/candidates.py` so it does not depend on an agent
noticing things. **Pass 2** removes complete, well-formed sentences that carry nothing: an
announcement of what the next sentence will say, a second utterance of one idea, a hedge, a
digression, and every sentence whose subject is the speaker.

```bash
python3 scripts/candidates.py blocks.json                       # pass 1 candidates
python3 scripts/candidates.py blocks.json --check needles.json  # uncovered, and the cut ratio
```

**Every sentence faces one test: delete it, read its two neighbours together, name what the viewer
lost.** Nothing lost is a cut. **Run the same test on every clause**, because that is where the last
ten percent hides: a list of examples that proves nothing, a doubled adjective, a trailing clause
restating an earlier beat. A first-take lesson gives up 14-20% of its characters to pass 1 and
22-30% to both, and below that is under-listed rather than a clean take.

**Read [`references/what-to-cut.md`](references/what-to-cut.md) before writing the cut list**, and
[`references/what-to-cut-passes.md`](references/what-to-cut-passes.md) for the run that shipped 29
pass-1 needles and no pass 2.

## Renaming, markers and scenes

A **scene** name and a marker have no API and the browser is the hard way, so
[`references/rename-and-markers.md`](references/rename-and-markers.md) holds that route. A
**composition** name is not this: it is `pnpm descript rename <project> <composition> "<name>"`, and
so are creating, duplicating, filing and removing one (`descript-projects`).

**The clipboard sets both without touching the editor.** Scene boundaries and markers are
`copiedComponents` on a `tauAnchor`; `apply` carries them across a cut, `--markers` adds new ones
and `--pins` adds the clips and the layouts. That is the path to prefer.

## Read the finished transcript for what you never listed

A run reporting every needle landed says nothing about the needles you failed to write. Glued words
mean a needle took both boundary spaces and `[a-z][.,][A-Za-z]` finds them; a surviving restart
means the cut list was short, and only the transcript read as prose finds that. Run `candidates.py`
on the finished export too, and repair with a one-line `fix.json` rather than handing it back:
[`references/what-to-cut.md`](references/what-to-cut.md).

## The silence gate: measure the export, do not trust the cut ratio

The character ratio says the words came out; it says nothing about the **air between them**, and air
is where a tight edit is won. Measure it on the rendered file, never on the document.

```bash
python3 scripts/silences.py deadair <export.mp4> doc.json "<comp>" --keep 0.35
```

**The gate is 5% of runtime.** Above it the cut is not finished, whatever the character ratio says:
ours came in at 9.9% and 7.5% against a competitor's 2.2% and 2.6%. `calibrate`, what it refuses,
and why `deadair`'s number is smaller than the gate's:
[`references/silence-gate.md`](references/silence-gate.md).

## Measure a beat off the document, never off a subtitle export

```bash
pnpm descript doc <project> --out doc.json
python3 scripts/beatclock.py doc.json --beat "first words" "last words"   # start, end, duration
```

The play clock is derived, and each duration is divided by its `speed` because `duration` is
source time. Reading a beat off an SRT is how one video's clips were timed 203.8s wrong.
**Read [`references/the-clock.md`](references/the-clock.md) before writing a timing.**

## Verify with the API, not the screen

The in-page duration readout is mostly ruler ticks, so do not build on it.
`mcp__claude_ai_Descript__get_project` returns `compositions[].duration` and Descript autosaves, so
that is the number to report. **With ignores present it is not the render length**: sum the
unblocked TAU durations, which is what `dscript apply` prints as `plays`.

## The browser fallback

Only when the user cannot copy and paste. The whole cold run is in
[`references/browser-runs.md`](references/browser-runs.md), and four more read before driving the
editor: [`laws.md`](references/laws.md), [`recovery.md`](references/recovery.md),
[`cdp.md`](references/cdp.md) and [`cut-list.md`](references/cut-list.md).

## Learned patterns

This skill appends new failure modes to its own pattern list after each run:
[`references/learned-patterns.md`](references/learned-patterns.md). Append a dated entry after
every run that surprised you.
